from __future__ import annotations

import argparse
import hashlib
import json
import socket
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from tools.ao_e0_b12_data01_acq02 import (
    PROVIDER,
    TRANSPORT,
    INSTRUMENT,
    TRANSFORMATION_ID,
    MULTIPLIER,
    ACQ02Blocked,
    canonical_bytes,
    materialize_ap0_from_ledger,
    materialize_h1_from_ap0,
    read_ledger,
    rolling_raw_manifest,
    seal_raw_object,
)

SCHEMA = "ATDS_AO_E0_B12_DATA01_FC01_HEALTH_V0_1"
BASE_URL = "https://jetta.dukascopy.com/v1/ticks/USATECH.IDX-USD"
UA = "ATDS-FC01/0.1"

WARMUP_START = datetime(2026, 10, 5, 14, tzinfo=timezone.utc)
FORWARD_RAW_START = datetime(2026, 10, 6, 10, tzinfo=timezone.utc)
EVIDENCE_START = datetime(2026, 10, 6, 11, tzinfo=timezone.utc)
FIXED_END = datetime(2027, 10, 6, 11, tzinfo=timezone.utc)
HOUR = timedelta(hours=1)
REPLAY_INTERVAL = timedelta(days=7)
DEFAULT_ROOT = Path(r"C:\Users\Boulevart\ATDS-DATA\DATA01-FC01")

MAX_ERROR_BODY_READ_BYTES = 65536
MAX_TEXT_PREVIEW_BYTES = 2048
MAX_EXCEPTION_TEXT_CHARS = 2048
C07_HEADER_ALLOWLIST = {
    "date",
    "content-type",
    "content-length",
    "retry-after",
    "location",
    "cache-control",
}
C07_TEXTUAL_MEDIA_TYPES = {
    "application/json",
    "application/problem+json",
    "application/xml",
    "application/problem+xml",
}
C07_STRATEGY_FORBIDDEN_TOKENS = {
    "momentum_signal",
    "target_position",
    "recommended_trade",
    "long_short_recommendation",
    "execution_recommendation",
    "strategy_qualification",
    "economic_edge",
}
C07_PERFORMANCE_FORBIDDEN_TOKENS = {
    "trade_count",
    "closed_trade_count",
    "pnl",
    "gross_pnl",
    "net_pnl",
    "returns",
    "expectancy",
    "win_rate",
    "loss_rate",
    "profit_factor",
    "sharpe",
    "sortino",
    "drawdown",
    "mae",
    "mfe",
    "individual_trade_outcomes",
    "entry_price",
    "exit_price",
    "average_winner",
    "average_loser",
    "forward_effect_size",
    "forward_variance",
    "confidence_interval",
    "p_value",
    "bootstrap_inference",
    "support",
    "refute",
}
C07_BREAKERS = {
    "BLOCKED_NON_200_PROMOTED_AS_MARKET_DATA",
    "BLOCKED_ERROR_BODY_WRITTEN_TO_SUCCESS_CACHE",
    "BLOCKED_ERROR_BODY_SEALED_TO_RAW_LEDGER",
    "BLOCKED_UNBOUNDED_ERROR_BODY_CAPTURE",
    "BLOCKED_NON_ALLOWLISTED_HEADER_PERSISTENCE",
    "BLOCKED_MISSING_ATTEMPT_INDEX",
    "BLOCKED_MISSING_STATUS_TRACE",
    "BLOCKED_FAILURE_RECEIPT_IDENTITY_COLLISION",
    "BLOCKED_PERFORMANCE_FIELD_LEAK",
    "BLOCKED_STRATEGY_FIELD_LEAK",
    "BLOCKED_B12_OPENING",
}

FORBIDDEN_HEALTH_KEYS = {
    "trade_count", "closed_trade_count", "pnl", "gross_pnl", "net_pnl",
    "returns", "expectancy", "win_rate", "loss_rate", "profit_factor",
    "sharpe", "sortino", "drawdown", "mae", "mfe",
    "individual_trade_outcomes", "entry_price", "exit_price",
    "average_winner", "average_loser", "forward_effect_size",
    "forward_variance", "confidence_interval", "p_value",
    "bootstrap_inference", "support", "refute", "strategy_qualification",
    "economic_edge", "momentum_signal", "target_position",
    "recommended_trade", "long_short_recommendation",
    "execution_recommendation",
}


class FC01Blocked(RuntimeError):
    pass


class FC01TransportBlocked(FC01Blocked):
    def __init__(self, message: str, *, attempts: list[dict], transport_failure_class: str):
        super().__init__(message)
        self.attempts = attempts
        self.transport_failure_class = transport_failure_class


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")


def _parse_hour(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:00:00Z").replace(tzinfo=timezone.utc)


def floor_complete_hour(now_utc: datetime) -> datetime:
    if now_utc.tzinfo is None:
        raise FC01Blocked("BLOCKED_NAIVE_CLOCK")
    now_utc = now_utc.astimezone(timezone.utc)
    return now_utc.replace(minute=0, second=0, microsecond=0)


def target_end_for(now_utc: datetime) -> datetime:
    return min(floor_complete_hour(now_utc), FIXED_END)


def url_for(dt: datetime) -> str:
    return f"{BASE_URL}/{dt.year}/{dt.month}/{dt.day}/{dt.hour}"


def cache_name(dt: datetime) -> str:
    return f"ticks%2FUSATECH.IDX-USD%2F{dt.year}%2F{dt.month}%2F{dt.day}%2F{dt.hour}.json"


def _redact_location(value: str) -> str:
    try:
        parts = urllib.parse.urlsplit(value)
        if parts.scheme or parts.netloc:
            return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
        return parts.path
    except Exception:
        return ""


def _allowed_headers(headers) -> dict[str, str]:
    if headers is None:
        return {}
    try:
        items = headers.items()
    except Exception:
        return {}
    out = {}
    for key, value in items:
        name = str(key).strip().lower()
        if name not in C07_HEADER_ALLOWLIST:
            continue
        text = str(value)
        if name == "location":
            text = _redact_location(text)
        out[name] = text[:4096]
    return dict(sorted(out.items()))


def _parse_content_length(headers: dict[str, str]) -> int | None:
    raw = headers.get("content-length")
    if raw is None:
        return None
    try:
        value = int(raw)
    except Exception:
        return None
    return value if value >= 0 else None


def _safe_text_preview(raw: bytes, content_type: str | None) -> str | None:
    if not content_type:
        return None
    media_type = content_type.split(";", 1)[0].strip().lower()
    if not (media_type.startswith("text/") or media_type in C07_TEXTUAL_MEDIA_TYPES):
        return None
    preview_bytes = raw[:MAX_TEXT_PREVIEW_BYTES]
    try:
        preview = preview_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return None
    lowered = preview.lower()
    if any(token in lowered for token in FORBIDDEN_HEALTH_KEYS):
        return None
    return preview


def _capture_non200_body(stream, headers: dict[str, str]) -> dict:
    declared_length = _parse_content_length(headers)
    if declared_length is not None and declared_length > MAX_ERROR_BODY_READ_BYTES:
        captured = stream.read(MAX_ERROR_BODY_READ_BYTES)
        truncated = True
    else:
        candidate = stream.read(MAX_ERROR_BODY_READ_BYTES + 1)
        truncated = len(candidate) > MAX_ERROR_BODY_READ_BYTES
        captured = candidate[:MAX_ERROR_BODY_READ_BYTES]

    if truncated:
        body_length = declared_length
        body_sha = None
        prefix_sha = hashlib.sha256(captured).hexdigest()
        capture_status = "TRUNCATED_AT_HARD_LIMIT"
    else:
        body_length = len(captured)
        body_sha = hashlib.sha256(captured).hexdigest()
        prefix_sha = None
        capture_status = "COMPLETE"

    return {
        "body_capture_status": capture_status,
        "response_body_byte_length": body_length,
        "captured_body_byte_length": len(captured),
        "response_body_sha256": body_sha,
        "response_body_prefix_sha256": prefix_sha,
        "response_body_preview": _safe_text_preview(captured, headers.get("content-type")),
    }


def _http_failure_class(status: int) -> str:
    if status == 202:
        return "HTTP_202"
    if status == 429:
        return "HTTP_429"
    if 400 <= status <= 499:
        return "HTTP_4XX_NONRETRYABLE"
    if status in (500, 502, 503, 504):
        return "HTTP_5XX_RETRYABLE"
    return "HTTP_STATUS_OTHER"


def _exception_failure_class(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return _http_failure_class(int(exc.code))
    if isinstance(exc, (socket.timeout, TimeoutError)):
        return "READ_TIMEOUT"
    if isinstance(exc, urllib.error.URLError):
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            return "DNS_FAILURE"
        if isinstance(reason, ssl.SSLError):
            return "TLS_FAILURE"
        if isinstance(reason, (socket.timeout, TimeoutError)):
            return "CONNECT_TIMEOUT"
    if isinstance(exc, ssl.SSLError):
        return "TLS_FAILURE"
    return "UNKNOWN_TRANSPORT_FAILURE"


def _bounded_exception_text(exc: Exception) -> str | None:
    text = str(exc)[:MAX_EXCEPTION_TEXT_CHARS]
    lowered = text.lower()
    if any(token in lowered for token in FORBIDDEN_HEALTH_KEYS):
        return None
    return text


def _new_attempt_base(dt: datetime, attempt_index: int) -> dict:
    return {
        "attempt_index": attempt_index,
        "request_interval_start_utc": _iso(dt),
        "request_interval_end_utc": _iso(dt + HOUR),
        "request_url_identity": url_for(dt),
        "result_class": None,
        "http_status": None,
        "exception_class": None,
        "exception_text": None,
        "allowed_response_headers": {},
        "body_capture_status": None,
        "response_body_byte_length": None,
        "captured_body_byte_length": 0,
        "response_body_sha256": None,
        "response_body_prefix_sha256": None,
        "response_body_preview": None,
        "retry_decision": None,
        "next_retry_delay_seconds": None,
    }


def _validate_attempt_trace(attempts: list[dict]) -> None:
    for expected, attempt in enumerate(attempts, start=1):
        if attempt.get("attempt_index") != expected:
            raise FC01Blocked("BLOCKED_MISSING_ATTEMPT_INDEX")
        result_class = attempt.get("result_class")
        if result_class == "HTTP_STATUS_FAILURE" and attempt.get("http_status") is None:
            raise FC01Blocked("BLOCKED_MISSING_STATUS_TRACE")
        headers = attempt.get("allowed_response_headers", {})
        if any(str(k).lower() not in C07_HEADER_ALLOWLIST for k in headers):
            raise FC01Blocked("BLOCKED_NON_ALLOWLISTED_HEADER_PERSISTENCE")
        if int(attempt.get("captured_body_byte_length", 0)) > MAX_ERROR_BODY_READ_BYTES:
            raise FC01Blocked("BLOCKED_UNBOUNDED_ERROR_BODY_CAPTURE")


def _validate_failed_interval_noncontamination(root: Path, cache: Path, dt: datetime) -> None:
    if (cache / cache_name(dt)).exists():
        raise FC01Blocked("BLOCKED_ERROR_BODY_WRITTEN_TO_SUCCESS_CACHE")
    ledger = read_ledger(root)
    start = _iso(dt)
    stop = _iso(dt + HOUR)
    if any(
        row.get("interval_start_utc") == start and row.get("interval_end_utc") == stop
        for row in ledger
    ):
        raise FC01Blocked("BLOCKED_ERROR_BODY_SEALED_TO_RAW_LEDGER")


def get_raw_fc01(cache: Path, dt: datetime) -> tuple[bytes, str, int]:
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / cache_name(dt)
    if p.exists():
        return p.read_bytes(), "CACHE_REUSE", 0

    delays = (0, 2, 4, 8, 16)
    last = None
    traces: list[dict] = []
    transport_failure_class = "UNKNOWN_TRANSPORT_FAILURE"

    for attempt_index, delay in enumerate(delays, start=1):
        if delay:
            time.sleep(delay)

        req = urllib.request.Request(
            url_for(dt),
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        attempt = _new_attempt_base(dt, attempt_index)

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    status = int(response.status)
                    headers = _allowed_headers(getattr(response, "headers", None))
                    attempt.update(
                        {
                            "result_class": "HTTP_STATUS_FAILURE",
                            "http_status": status,
                            "allowed_response_headers": headers,
                            **_capture_non200_body(response, headers),
                        }
                    )
                    last = RuntimeError(f"HTTP_{status}")
                    transport_failure_class = _http_failure_class(status)
                    retryable = True
                    attempt["exception_class"] = last.__class__.__name__
                    attempt["exception_text"] = _bounded_exception_text(last)
                else:
                    raw = response.read()
                    p.write_bytes(raw)
                    return raw, "NETWORK", attempt_index

        except Exception as exc:
            last = exc
            status = int(exc.code) if isinstance(exc, urllib.error.HTTPError) else None
            attempt["result_class"] = "HTTP_STATUS_FAILURE" if status is not None else "TRANSPORT_EXCEPTION"
            attempt["http_status"] = status
            attempt["exception_class"] = exc.__class__.__name__
            attempt["exception_text"] = _bounded_exception_text(exc)
            transport_failure_class = _exception_failure_class(exc)

            if isinstance(exc, urllib.error.HTTPError):
                headers = _allowed_headers(getattr(exc, "headers", None))
                attempt["allowed_response_headers"] = headers
                try:
                    attempt.update(_capture_non200_body(exc, headers))
                except Exception:
                    attempt["body_capture_status"] = "BODY_CAPTURE_FAILED"
                retryable = exc.code in (429, 500, 502, 503, 504)
            else:
                retryable = True

        is_last = attempt_index == len(delays)
        if retryable and not is_last:
            attempt["retry_decision"] = "RETRY"
            attempt["next_retry_delay_seconds"] = delays[attempt_index]
        else:
            attempt["retry_decision"] = "TERMINAL"
            attempt["next_retry_delay_seconds"] = None

        traces.append(attempt)
        _validate_attempt_trace(traces)

        if not retryable:
            break

    message = f"BLOCKED_FORWARD_TRANSPORT_UNAVAILABLE {_iso(dt)} {last}"
    raise FC01TransportBlocked(
        message,
        attempts=traces,
        transport_failure_class=transport_failure_class,
    )


def _expected_intervals(end: datetime) -> list[tuple[str, str]]:
    rows = []
    dt = WARMUP_START
    while dt < end:
        rows.append((_iso(dt), _iso(dt + HOUR)))
        dt += HOUR
    return rows


def _ensure_exact_coverage(root: Path, end: datetime, now_utc: datetime) -> tuple[list[dict], list[str]]:
    ledger = read_ledger(root)
    actual = [(x["interval_start_utc"], x["interval_end_utc"]) for x in ledger]
    expected = _expected_intervals(end)

    if any(_parse_hour(x[1]) > FIXED_END for x in actual):
        raise FC01Blocked("BLOCKED_POST_HORIZON_CONTAMINATION")
    if any(_parse_hour(x[1]) > floor_complete_hour(now_utc) for x in actual):
        raise FC01Blocked("BLOCKED_FUTURE_OF_CLOCK_EXISTING_OBJECT")

    expected_set = set(expected)
    actual_set = set(actual)
    missing = [start for start, stop in expected if (start, stop) not in actual_set]
    unexpected = [f"{start}->{stop}" for start, stop in actual if (start, stop) not in expected_set]
    if unexpected:
        raise FC01Blocked("BLOCKED_UNEXPECTED_INTERVAL:" + ",".join(unexpected))
    if missing:
        raise FC01Blocked("BLOCKED_MISSING_INTERVAL:" + ",".join(missing))
    if len(actual) != len(set(actual)):
        raise FC01Blocked("BLOCKED_DUPLICATE_INTERVAL")
    return ledger, missing


def _write_json_atomic(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical_bytes(obj)
    if path.exists():
        if path.read_bytes() != raw:
            raise FC01Blocked("BLOCKED_RECEIPT_IDENTITY_COLLISION")
        return
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(raw)
    tmp.replace(path)


def _last_replay_end(root: Path) -> datetime | None:
    health = root / "evidence" / "health"
    if not health.exists():
        return None
    best = None
    for p in health.glob("*.json"):
        try:
            x = json.loads(p.read_text(encoding="utf-8"))
            if x.get("deterministic_replay_status") != "PASS":
                continue
            dt = _parse_hour(x["coverage_end_exclusive_utc"])
            best = dt if best is None or dt > best else best
        except Exception:
            continue
    return best


def _replay_due(root: Path, target_end: datetime, force_replay: bool) -> bool:
    if force_replay:
        return True
    last = _last_replay_end(root)
    return last is None or target_end - last >= REPLAY_INTERVAL or target_end == FIXED_END


def _materialize(root: Path, target_end: datetime) -> tuple[dict, dict]:
    ap0 = materialize_ap0_from_ledger(root)
    (root / "ap0").mkdir(parents=True, exist_ok=True)
    (root / "ap0" / "AP0-ROLLING.json").write_bytes(canonical_bytes(ap0))

    ap0_meta = {
        "identity": ap0["identity"],
        "source_raw_manifest_sha256": ap0["source_raw_manifest_sha256"],
        "ap0_forward_manifest_sha256": ap0["ap0_forward_manifest_sha256"],
        "row_count": len(ap0["rows"]),
        "first_minute_ms": None if not ap0["rows"] else ap0["rows"][0]["minute_start_ms_utc"],
        "last_minute_ms": None if not ap0["rows"] else ap0["rows"][-1]["minute_start_ms_utc"],
        "forward_fill": False,
        "volume_used": False,
        "returns_calculated": False,
        "strategy_calculated": False,
        "pnl_calculated": False,
    }
    (root / "manifests" / "AP0-ROLLING-MANIFEST.json").write_bytes(canonical_bytes(ap0_meta))

    h1 = materialize_h1_from_ap0(
        ap0,
        raw_window_start_ms=int(WARMUP_START.timestamp() * 1000),
        raw_window_end_ms=int(target_end.timestamp() * 1000),
    )
    (root / "h1").mkdir(parents=True, exist_ok=True)
    (root / "h1" / "H1-ROLLING.json").write_bytes(canonical_bytes(h1))

    h1_meta = {k: v for k, v in h1.items() if k != "rows"}
    h1_meta["coverage_start_utc"] = _iso(WARMUP_START)
    h1_meta["coverage_end_exclusive_utc"] = _iso(target_end)
    (root / "manifests" / "H1-ROLLING-MANIFEST.json").write_bytes(canonical_bytes(h1_meta))
    return ap0_meta, h1_meta


def collect_cycle(
    root: Path,
    *,
    now_utc: datetime | None = None,
    fetcher=get_raw_fc01,
    force_replay: bool = False,
) -> dict:
    root = Path(root)
    now_utc = datetime.now(timezone.utc) if now_utc is None else now_utc.astimezone(timezone.utc)
    target_end = target_end_for(now_utc)

    if target_end <= FORWARD_RAW_START:
        raise FC01Blocked("BLOCKED_TARGET_BEFORE_FORWARD_START")

    for name in ("raw", "manifests", "ledger", "ap0", "h1", "evidence", "evidence/health", "evidence/errors"):
        (root / name).mkdir(parents=True, exist_ok=True)

    cache = root / "raw" / "provider-cache"
    dt = WARMUP_START
    sealed = replayed = network = cache_reuse = network_requests = retry_count = 0

    try:
        while dt < target_end:
            raw, source, attempts = fetcher(cache, dt)
            classification = "WARMUP" if dt < FORWARD_RAW_START else "FORWARD_EVIDENCE"
            result = seal_raw_object(
                root,
                interval_start_utc=_iso(dt),
                interval_end_utc=_iso(dt + HOUR),
                raw=raw,
                acquisition_time_utc=now_utc.isoformat().replace("+00:00", "Z"),
                classification=classification,
            )
            sealed += result["status"] == "SEALED"
            replayed += result["status"] == "REPRODUCIBILITY_ONLY"
            network += source == "NETWORK"
            cache_reuse += source == "CACHE_REUSE"
            network_requests += attempts
            if attempts > 1:
                retry_count += attempts - 1
            dt += HOUR
    except Exception as exc:
        attempts = list(exc.attempts) if isinstance(exc, FC01TransportBlocked) else []
        _validate_attempt_trace(attempts)
        if isinstance(exc, FC01TransportBlocked):
            _validate_failed_interval_noncontamination(root, cache, dt)
        failure = {
            "schema": "ATDS_AO_E0_B12_DATA01_FC01_FAILURE_V0_2",
            "target_end_exclusive_utc": _iso(target_end),
            "failed_interval_start_utc": _iso(dt),
            "transport_failure_class": (
                exc.transport_failure_class
                if isinstance(exc, FC01TransportBlocked)
                else "UNKNOWN_TRANSPORT_FAILURE"
            ),
            "attempt_count": len(attempts),
            "attempts": attempts,
            "terminal_reason": str(exc),
            "reason": str(exc),
            "b12": "CLOSED",
            "performance_bearing_read": False,
        }
        serialized = json.dumps(failure, sort_keys=True).lower()
        if any(token in serialized for token in C07_STRATEGY_FORBIDDEN_TOKENS):
            raise FC01Blocked("BLOCKED_STRATEGY_FIELD_LEAK") from exc
        if any(token in serialized for token in C07_PERFORMANCE_FORBIDDEN_TOKENS):
            raise FC01Blocked("BLOCKED_PERFORMANCE_FIELD_LEAK") from exc
        if failure["b12"] != "CLOSED":
            raise FC01Blocked("BLOCKED_B12_OPENING") from exc
        stamp = now_utc.strftime("%Y%m%dT%H%M%SZ")
        _write_json_atomic(root / "evidence" / "errors" / f"{stamp}.json", failure)
        raise

    ledger, missing = _ensure_exact_coverage(root, target_end, now_utc)
    raw_manifest = rolling_raw_manifest(root)
    (root / "manifests" / "RAW-FORWARD-MANIFEST.json").write_bytes(canonical_bytes(raw_manifest))

    ap0_meta, h1_meta = _materialize(root, target_end)

    receipt_name = target_end.strftime("%Y%m%dT%H0000Z") + ".json"
    receipt_path = root / "evidence" / "health" / receipt_name
    existing_health = None
    if receipt_path.exists():
        existing_health = json.loads(receipt_path.read_text(encoding="utf-8"))

    replay = "NOT_DUE"
    if existing_health is not None:
        replay = existing_health.get("deterministic_replay_status", "NOT_DUE")
    elif _replay_due(root, target_end, force_replay):
        ap0_replay, h1_replay = _materialize(root, target_end)
        if (
            ap0_replay["ap0_forward_manifest_sha256"] != ap0_meta["ap0_forward_manifest_sha256"]
            or h1_replay["h1_forward_stream_sha256"] != h1_meta["h1_forward_stream_sha256"]
        ):
            raise FC01Blocked("BLOCKED_DETERMINISTIC_REPLAY_MISMATCH")
        replay = "PASS"

    total_bytes = sum(int(x["size_bytes"]) for x in raw_manifest["inventory"])
    total_ticks = sum(int(x["row_count"]) for x in raw_manifest["inventory"])
    continuity_blocks = int(h1_meta["segment_count"])

    health = {
        "schema": SCHEMA,
        "source": PROVIDER,
        "transport": TRANSPORT,
        "instrument": INSTRUMENT,
        "transformation_id": TRANSFORMATION_ID,
        "multiplier": MULTIPLIER,
        "collection_status": "PASS",
        "coverage_start_utc": _iso(WARMUP_START),
        "coverage_end_exclusive_utc": _iso(target_end),
        "fixed_horizon_end_exclusive_utc": _iso(FIXED_END),
        "fixed_horizon_reached": target_end == FIXED_END,
        "raw_object_count": len(raw_manifest["inventory"]),
        "warmup_object_count": raw_manifest["warmup_objects"],
        "forward_evidence_object_count": raw_manifest["forward_evidence_objects"],
        "raw_byte_count": total_bytes,
        "raw_tick_count": total_ticks,
        "missing_intervals": missing,
        "duplicate_detection": "PASS",
        "ordering": "PASS",
        "schema_validity": "PASS",
        "source_identity": "PASS",
        "raw_manifest_sha256": raw_manifest["raw_forward_manifest_sha256"],
        "raw_inventory_digest": raw_manifest["raw_forward_inventory_digest"],
        "ap0_manifest_sha256": ap0_meta["ap0_forward_manifest_sha256"],
        "ap0_row_count": ap0_meta["row_count"],
        "h1_stream_sha256": h1_meta["h1_forward_stream_sha256"],
        "h1_row_count": h1_meta["h1_row_count"],
        "latest_fully_materialized_h1_boundary_ms": h1_meta["h1_last_boundary"],
        "continuity_block_count": continuity_blocks,
        "raw_ap0_h1_transformation_status": "PASS",
        "deterministic_replay_status": replay,
        "b12": "CLOSED",
        "performance_bearing_read": False,
        "force": False,
    }

    serialized_keys = {str(k).lower() for k in health}
    if serialized_keys.intersection(FORBIDDEN_HEALTH_KEYS):
        raise FC01Blocked("BLOCKED_FORBIDDEN_HEALTH_SURFACE")

    _write_json_atomic(receipt_path, health)

    return {
        "health": health,
        "run_stats": {
            "sealed_new_objects": sealed,
            "replayed_objects": replayed,
            "network_objects": network,
            "cache_reuse_objects": cache_reuse,
            "network_requests": network_requests,
            "network_retry_count": retry_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--force-replay", action="store_true")
    args = parser.parse_args()

    result = collect_cycle(Path(args.root), force_replay=args.force_replay)
    h = result["health"]
    s = result["run_stats"]

    print("FC01=PASS")
    print("B12=CLOSED")
    print("PERFORMANCE_BEARING_READ=FALSE")
    print("STRATEGY_QUALIFIED=NO_CLAIM")
    print("COVERAGE_END_EXCLUSIVE_UTC=" + h["coverage_end_exclusive_utc"])
    print("RAW_OBJECT_COUNT=" + str(h["raw_object_count"]))
    print("RAW_BYTE_COUNT=" + str(h["raw_byte_count"]))
    print("RAW_TICK_COUNT=" + str(h["raw_tick_count"]))
    print("H1_ROW_COUNT=" + str(h["h1_row_count"]))
    print("RAW_MANIFEST_SHA256=" + h["raw_manifest_sha256"])
    print("AP0_MANIFEST_SHA256=" + h["ap0_manifest_sha256"])
    print("H1_STREAM_SHA256=" + h["h1_stream_sha256"])
    print("DETERMINISTIC_REPLAY_STATUS=" + h["deterministic_replay_status"])
    print("NETWORK_OBJECTS=" + str(s["network_objects"]))
    print("NETWORK_RETRY_COUNT=" + str(s["network_retry_count"]))
    print("FIXED_HORIZON_REACHED=" + str(h["fixed_horizon_reached"]).upper())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
