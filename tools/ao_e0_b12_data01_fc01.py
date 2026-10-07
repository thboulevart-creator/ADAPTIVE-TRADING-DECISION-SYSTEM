from __future__ import annotations

import argparse
import json
import time
import urllib.error
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


def get_raw_fc01(cache: Path, dt: datetime) -> tuple[bytes, str, int]:
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / cache_name(dt)
    if p.exists():
        return p.read_bytes(), "CACHE_REUSE", 0

    last = None
    attempts = 0
    for delay in (0, 2, 4, 8, 16):
        if delay:
            time.sleep(delay)
        attempts += 1
        req = urllib.request.Request(
            url_for(dt),
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP_{response.status}")
                raw = response.read()
            p.write_bytes(raw)
            return raw, "NETWORK", attempts
        except Exception as exc:
            last = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                break
    raise FC01Blocked(f"BLOCKED_FORWARD_TRANSPORT_UNAVAILABLE {_iso(dt)} {last}")


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
        failure = {
            "schema": "ATDS_AO_E0_B12_DATA01_FC01_FAILURE_V0_1",
            "target_end_exclusive_utc": _iso(target_end),
            "failed_interval_start_utc": _iso(dt),
            "reason": str(exc),
            "b12": "CLOSED",
            "performance_bearing_read": False,
        }
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
