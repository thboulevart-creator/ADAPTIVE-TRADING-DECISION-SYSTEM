from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import struct
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dukascopy_usatech_calendar import (
    CALENDAR_CONTRACT,
    CALENDAR_SOURCE_URL,
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    classify_slot,
)


INSTRUMENT = "USATECHIDXUSD"
BASE_URL = "https://datafeed.dukascopy.com/datafeed"
RECORD_SIZE = 20
RECORD_STRUCT = ">IIIff"
PRICE_SCALE = 1000.0
USER_AGENT = "ALGO-Dukascopy-BI5-Corpus-Downloader/1.3"

RESOLVED_STATUSES = {"DOWNLOADED_VALID", "SKIPPED_EXISTING_VALID"}


def url_for(day: date, hour: int) -> str:
    month_zero_based = day.month - 1
    return (
        f"{BASE_URL}/{INSTRUMENT}/{day.year:04d}/{month_zero_based:02d}/"
        f"{day.day:02d}/{hour:02d}h_ticks.bi5"
    )


def output_path(root: Path, day: date, hour: int) -> Path:
    return root / f"{day:%Y/%m/%d}/{hour:02d}h_ticks.bi5"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_bi5(data: bytes, day: date, hour: int) -> tuple[bool, str | None, int]:
    if not data:
        return False, "EMPTY_PAYLOAD", 0
    try:
        raw = lzma.decompress(data, format=lzma.FORMAT_ALONE)
    except Exception as exc:
        return False, f"LZMA_ERROR:{type(exc).__name__}:{exc}", 0
    if not raw:
        return False, "EMPTY_DECOMPRESSED_PAYLOAD", 0
    if len(raw) % RECORD_SIZE != 0:
        return False, f"SIZE_NOT_ALIGNED:{len(raw)}", 0

    count = len(raw) // RECORD_SIZE
    previous_ms: int | None = None
    for offset in range(0, len(raw), RECORD_SIZE):
        ms, ask_raw, bid_raw, ask_vol, bid_vol = struct.unpack_from(
            RECORD_STRUCT, raw, offset
        )
        if ms >= 3_600_000:
            return False, f"INVALID_MILLISECOND_OFFSET:{ms}", count
        ask = ask_raw / PRICE_SCALE
        bid = bid_raw / PRICE_SCALE
        if ask <= 0 or bid <= 0:
            return False, f"INVALID_PRICE:{ask}:{bid}", count
        if ask < bid:
            return False, f"ASK_LT_BID:{ask}:{bid}", count
        if ask_vol < 0 or bid_vol < 0:
            return False, f"NEGATIVE_VOLUME:{ask_vol}:{bid_vol}", count
        if previous_ms is not None and ms < previous_ms:
            return False, f"NON_CHRONOLOGICAL:{previous_ms}->{ms}", count
        previous_ms = ms

    return True, None, count


def iter_hours(start: date, end: date, hour: int | None):
    current = start
    while current <= end:
        if hour is None:
            for current_hour in range(24):
                yield current, current_hour
        else:
            yield current, hour
        current += timedelta(days=1)


def fetch(url: str, timeout: int) -> tuple[int | None, bytes, str | None]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read(), None
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read()
        except Exception:
            body = b""
        return exc.code, body, None
    except Exception as exc:
        return None, b"", f"{type(exc).__name__}:{exc}"


def write_log(log, record: dict) -> None:
    log.write(json.dumps(record, sort_keys=True) + "\n")
    log.flush()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Resumable raw Dukascopy BI5 hourly downloader with pre-network "
            "calendar classification and targeted pass-based reconciliation."
        )
    )
    parser.add_argument("--start-date", required=True, help="UTC date YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="UTC date YYYY-MM-DD")
    parser.add_argument(
        "--hour",
        type=int,
        default=None,
        help="Optional UTC hour 0-23; when omitted, inspect all 24 hours.",
    )
    parser.add_argument("--output", required=True, help="Corpus root")
    parser.add_argument("--manifest", required=True, help="JSONL manifest path")
    parser.add_argument(
        "--max-requests",
        type=int,
        default=None,
        help=(
            "Compatibility pilot limit: cap enumerated target slots before "
            "calendar classification. Closed slots never consume requests."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Timeout for the single network call allowed per open slot per pass.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.25,
        help="Polite delay between expected-open slots inside a pass.",
    )
    parser.add_argument(
        "--reconciliation-passes",
        type=int,
        default=3,
        help="Total passes including the initial pass. Must be >= 1.",
    )
    parser.add_argument(
        "--reconciliation-delay-seconds",
        type=float,
        default=3.0,
        help="Base delay before each reconciliation pass.",
    )
    parser.add_argument(
        "--reconciliation-backoff",
        type=float,
        default=2.0,
        help="Multiplier applied to the delay between reconciliation passes.",
    )
    parser.add_argument(
        "--progress-every",
        type=int,
        default=1,
        help="Print slot progress every N processed expected-open slots.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> tuple[date, date]:
    start = date.fromisoformat(args.start_date)
    end = date.fromisoformat(args.end_date)
    if end < start:
        raise SystemExit("end-date must be >= start-date")
    if args.hour is not None and not 0 <= args.hour <= 23:
        raise SystemExit("hour must be between 0 and 23")
    if args.timeout <= 0:
        raise SystemExit("timeout must be > 0")
    if args.sleep_seconds < 0:
        raise SystemExit("sleep-seconds must be >= 0")
    if args.reconciliation_passes < 1:
        raise SystemExit("reconciliation-passes must be >= 1")
    if args.reconciliation_delay_seconds < 0:
        raise SystemExit("reconciliation-delay-seconds must be >= 0")
    if args.reconciliation_backoff < 1:
        raise SystemExit("reconciliation-backoff must be >= 1")
    if args.progress_every < 1:
        raise SystemExit("progress-every must be >= 1")
    if args.max_requests is not None and args.max_requests < 1:
        raise SystemExit("max-requests must be >= 1 when provided")
    return start, end


def classify_targets(
    targets: list[tuple[date, int]],
) -> tuple[list[tuple[date, int]], list[dict]]:
    expected_open: list[tuple[date, int]] = []
    expected_closed: list[dict] = []

    for day, hour in targets:
        classification = classify_slot(day, hour)
        record = {
            "date": day.isoformat(),
            "hour": hour,
            "classification": classification.status,
            "classification_reason": classification.reason,
            "schedule": classification.schedule,
        }
        if classification.status == EXPECTED_OPEN:
            expected_open.append((day, hour))
        elif classification.status == EXPECTED_CLOSED:
            expected_closed.append(record)
        else:
            raise RuntimeError(
                f"unsupported calendar classification: {classification.status}"
            )

    return expected_open, expected_closed


def attempt_slot(
    *,
    day: date,
    hour: int,
    root: Path,
    args: argparse.Namespace,
    log,
    pass_number: int,
) -> tuple[dict, int]:
    """Attempt one EXPECTED_OPEN slot exactly once for this pass."""
    url = url_for(day, hour)
    destination = output_path(root, day, hour)
    classification = classify_slot(day, hour)
    if classification.status != EXPECTED_OPEN:
        raise RuntimeError(
            "attempt_slot() received non-open slot; pre-network calendar gate bypassed"
        )

    base_record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "pass": pass_number,
        "date": day.isoformat(),
        "hour": hour,
        "classification": classification.status,
        "classification_reason": classification.reason,
        "schedule": classification.schedule,
        "url": url,
        "path": str(destination),
    }

    if destination.exists():
        existing = destination.read_bytes()
        valid, validation_error, count = validate_bi5(existing, day, hour)
        if valid:
            record = {
                **base_record,
                "status": "SKIPPED_EXISTING_VALID",
                "sha256": sha256_bytes(existing),
                "bytes": len(existing),
                "record_count": count,
                "network_calls": 0,
            }
            write_log(log, record)
            return record, 0

        destination.unlink()
        write_log(
            log,
            {
                **base_record,
                "status": "REMOVED_INVALID_EXISTING",
                "error": validation_error,
                "bytes": len(existing),
                "sha256": sha256_bytes(existing),
                "network_calls": 0,
            },
        )

    status, data, error = fetch(url, args.timeout)
    network_calls = 1

    if status != 200:
        state = "TRANSPORT_ERROR" if status is None else f"HTTP_{status}"
        record = {
            **base_record,
            "status": state,
            "http_status": status,
            "error": error,
            "network_calls": network_calls,
        }
        write_log(log, record)
        return record, network_calls

    if not data:
        record = {
            **base_record,
            "status": "EMPTY_PAYLOAD",
            "http_status": status,
            "network_calls": network_calls,
        }
        write_log(log, record)
        return record, network_calls

    valid, validation_error, count = validate_bi5(data, day, hour)
    if not valid:
        record = {
            **base_record,
            "status": "INVALID_PAYLOAD",
            "http_status": status,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "record_count": count,
            "error": validation_error,
            "network_calls": network_calls,
        }
        write_log(log, record)
        return record, network_calls

    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_suffix(destination.suffix + ".part")
    temp.write_bytes(data)
    temp.replace(destination)

    record = {
        **base_record,
        "status": "DOWNLOADED_VALID",
        "http_status": status,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "record_count": count,
        "network_calls": network_calls,
    }
    write_log(log, record)
    return record, network_calls


def validate_expected_open_files(
    root: Path,
    targets: list[tuple[date, int]],
) -> tuple[list[dict], list[dict]]:
    valid_slots: list[dict] = []
    unresolved_slots: list[dict] = []

    for day, hour in targets:
        destination = output_path(root, day, hour)
        if not destination.exists():
            unresolved_slots.append(
                {
                    "date": day.isoformat(),
                    "hour": hour,
                    "path": str(destination),
                    "reason": "MISSING_EXPECTED_OPEN_AFTER_RECONCILIATION",
                }
            )
            continue

        data = destination.read_bytes()
        valid, error, count = validate_bi5(data, day, hour)
        if not valid:
            unresolved_slots.append(
                {
                    "date": day.isoformat(),
                    "hour": hour,
                    "path": str(destination),
                    "reason": "INVALID_EXPECTED_OPEN_AFTER_RECONCILIATION",
                    "error": error,
                }
            )
            continue

        valid_slots.append(
            {
                "date": day.isoformat(),
                "hour": hour,
                "path": str(destination),
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "record_count": count,
            }
        )

    return valid_slots, unresolved_slots


def inspect_expected_closed_files(root: Path, closed_slots: list[dict]) -> list[dict]:
    conflicts: list[dict] = []
    for slot in closed_slots:
        day = date.fromisoformat(slot["date"])
        hour = int(slot["hour"])
        destination = output_path(root, day, hour)
        if destination.exists():
            data = destination.read_bytes()
            conflicts.append(
                {
                    **slot,
                    "path": str(destination),
                    "reason": "UNEXPECTED_FILE_IN_EXPECTED_CLOSED_SLOT",
                    "bytes": len(data),
                    "sha256": sha256_bytes(data),
                }
            )
    return conflicts


def main() -> int:
    args = parse_args()
    start, end = validate_args(args)

    root = Path(args.output).resolve()
    manifest = Path(args.manifest).resolve()

    targets = list(iter_hours(start, end, args.hour))
    if args.max_requests is not None:
        targets = targets[: args.max_requests]

    expected_open, expected_closed = classify_targets(targets)

    print(
        "CALENDAR_CLASSIFICATION "
        f"targets={len(targets)} expected_open={len(expected_open)} "
        f"expected_closed={len(expected_closed)}",
        flush=True,
    )

    if args.dry_run:
        for day, hour in targets:
            classification = classify_slot(day, hour)
            item = {
                "date": day.isoformat(),
                "hour": hour,
                "classification": classification.status,
                "reason": classification.reason,
                "schedule": classification.schedule,
                "url": url_for(day, hour)
                if classification.status == EXPECTED_OPEN
                else None,
            }
            print(json.dumps(item, sort_keys=True))
        summary = {
            "instrument": INSTRUMENT,
            "source": "Dukascopy",
            "format": "BI5",
            "calendar_contract": CALENDAR_CONTRACT,
            "calendar_source": CALENDAR_SOURCE_URL,
            "target_slots": len(targets),
            "expected_open_slots": len(expected_open),
            "expected_closed_slots": len(expected_closed),
            "network_calls": 0,
            "dry_run": True,
        }
        print(json.dumps(summary, indent=2))
        return 0

    root.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    status_counts: dict[str, int] = {}
    network_calls = 0
    pass_summaries: list[dict] = []

    with manifest.open("a", encoding="utf-8") as log:
        for slot in expected_closed:
            day = date.fromisoformat(slot["date"])
            hour = int(slot["hour"])
            record = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                **slot,
                "path": str(output_path(root, day, hour)),
                "status": EXPECTED_CLOSED,
                "network_calls": 0,
            }
            write_log(log, record)
            status_counts[EXPECTED_CLOSED] = (
                status_counts.get(EXPECTED_CLOSED, 0) + 1
            )

        pending = list(expected_open)
        for pass_number in range(1, args.reconciliation_passes + 1):
            if not pending:
                break

            if pass_number > 1:
                delay = args.reconciliation_delay_seconds * (
                    args.reconciliation_backoff ** (pass_number - 2)
                )
                if delay > 0:
                    print(
                        f"RECONCILIATION_PASS_{pass_number}: "
                        f"{len(pending)} unresolved open slots; sleeping {delay:.2f}s",
                        flush=True,
                    )
                    time.sleep(delay)

            current_pending = list(pending)
            next_pending: list[tuple[date, int]] = []
            pass_counts: dict[str, int] = {}
            pass_network_calls = 0

            print(
                f"PASS_{pass_number}_START targets={len(current_pending)}",
                flush=True,
            )

            for slot_index, (day, hour) in enumerate(current_pending, start=1):
                print(
                    f"PASS_{pass_number}_SLOT_START "
                    f"{slot_index}/{len(current_pending)} "
                    f"date={day.isoformat()} hour={hour:02d}",
                    flush=True,
                )

                record, calls = attempt_slot(
                    day=day,
                    hour=hour,
                    root=root,
                    args=args,
                    log=log,
                    pass_number=pass_number,
                )
                network_calls += calls
                pass_network_calls += calls
                status = record["status"]
                status_counts[status] = status_counts.get(status, 0) + 1
                pass_counts[status] = pass_counts.get(status, 0) + 1

                if status not in RESOLVED_STATUSES:
                    next_pending.append((day, hour))

                if (
                    slot_index % args.progress_every == 0
                    or slot_index == len(current_pending)
                ):
                    print(
                        f"PASS_{pass_number}_SLOT_DONE "
                        f"{slot_index}/{len(current_pending)} "
                        f"date={day.isoformat()} hour={hour:02d} "
                        f"status={status} calls={calls} "
                        f"pending_next={len(next_pending)}",
                        flush=True,
                    )

                if args.sleep_seconds > 0:
                    time.sleep(args.sleep_seconds)

            pending = next_pending
            pass_summary = {
                "pass": pass_number,
                "targets": len(current_pending),
                "resolved_this_pass": len(current_pending) - len(pending),
                "unresolved_after_pass": len(pending),
                "network_calls_this_pass": pass_network_calls,
                "status_counts": pass_counts,
            }
            pass_summaries.append(pass_summary)
            print(json.dumps(pass_summary, sort_keys=True), flush=True)

    valid_open, unresolved_open = validate_expected_open_files(root, expected_open)
    closed_conflicts = inspect_expected_closed_files(root, expected_closed)

    invalid_open = sum(
        1
        for item in unresolved_open
        if item["reason"] == "INVALID_EXPECTED_OPEN_AFTER_RECONCILIATION"
    )
    missing_open = sum(
        1
        for item in unresolved_open
        if item["reason"] == "MISSING_EXPECTED_OPEN_AFTER_RECONCILIATION"
    )

    if closed_conflicts:
        verdict = "FAIL"
        reason = "UNEXPECTED_DATA_PRESENT_IN_EXPECTED_CLOSED_SLOT"
        exit_code = 1
    elif invalid_open:
        verdict = "FAIL"
        reason = "INVALID_EXPECTED_OPEN_ARTIFACT_REMAINS_AFTER_RECONCILIATION"
        exit_code = 1
    elif unresolved_open:
        verdict = "BLOCKED"
        reason = "EXPECTED_OPEN_SLOTS_REMAIN_UNRESOLVED_AFTER_RECONCILIATION"
        exit_code = 2
    else:
        verdict = "PASS"
        reason = (
            "ALL_EXPECTED_OPEN_SLOTS_VALID_AND_EXPECTED_CLOSED_SLOTS_SKIPPED_"
            "WITHOUT_NETWORK"
        )
        exit_code = 0

    summary = {
        "instrument": INSTRUMENT,
        "source": "Dukascopy",
        "format": "BI5",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hour_filter": args.hour,
        "calendar_contract": CALENDAR_CONTRACT,
        "calendar_source": CALENDAR_SOURCE_URL,
        "pre_network_calendar_gate": True,
        "target_slots": len(targets),
        "expected_open_slots": len(expected_open),
        "expected_closed_slots": len(expected_closed),
        "valid_open_slots": len(valid_open),
        "unresolved_open_slots": len(unresolved_open),
        "missing_open_final": missing_open,
        "invalid_open_final": invalid_open,
        "closed_slot_conflicts": len(closed_conflicts),
        "network_calls": network_calls,
        "single_network_call_per_slot_per_pass": True,
        "reconciliation_passes_configured": args.reconciliation_passes,
        "reconciliation_passes_executed": len(pass_summaries),
        "status_counts": status_counts,
        "passes": pass_summaries,
        "expected_closed": expected_closed,
        "unresolved_open": unresolved_open,
        "closed_conflicts": closed_conflicts,
        "verdict": verdict,
        "reason": reason,
        "dry_run": False,
    }
    print(json.dumps(summary, indent=2), flush=True)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
