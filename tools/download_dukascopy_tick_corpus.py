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


INSTRUMENT = "USATECHIDXUSD"
BASE_URL = "https://datafeed.dukascopy.com/datafeed"
RECORD_SIZE = 20
RECORD_STRUCT = ">IIIff"
PRICE_SCALE = 1000.0
USER_AGENT = "ALGO-Dukascopy-BI5-Corpus-Downloader/1.0"


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resumable raw Dukascopy BI5 hourly tick corpus downloader."
    )
    parser.add_argument("--start-date", required=True, help="UTC date YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="UTC date YYYY-MM-DD")
    parser.add_argument(
        "--hour",
        type=int,
        default=None,
        help="Optional UTC hour 0-23; when omitted, process all 24 hours.",
    )
    parser.add_argument("--output", required=True, help="Corpus root")
    parser.add_argument("--manifest", required=True, help="JSONL manifest path")
    parser.add_argument("--max-requests", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep-seconds", type=float, default=0.25)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    start = date.fromisoformat(args.start_date)
    end = date.fromisoformat(args.end_date)
    if end < start:
        raise SystemExit("end-date must be >= start-date")
    if args.hour is not None and not 0 <= args.hour <= 23:
        raise SystemExit("hour must be between 0 and 23")
    if args.retries < 0:
        raise SystemExit("retries must be >= 0")

    root = Path(args.output).resolve()
    manifest = Path(args.manifest).resolve()
    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)
        manifest.parent.mkdir(parents=True, exist_ok=True)

    requests_seen = 0
    downloaded_valid = 0
    skipped_existing = 0
    empty_payloads = 0
    http_errors = 0
    transport_errors = 0
    invalid_payloads = 0

    with manifest.open("a", encoding="utf-8") if not args.dry_run else open("/dev/null", "w") as log:
        for day, hour in iter_hours(start, end, args.hour):
            if args.max_requests is not None and requests_seen >= args.max_requests:
                break

            url = url_for(day, hour)
            destination = output_path(root, day, hour)

            if destination.exists():
                data = destination.read_bytes()
                valid, error, count = validate_bi5(data, day, hour)
                if valid:
                    skipped_existing += 1
                    log.write(json.dumps({
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "date": day.isoformat(), "hour": hour,
                        "url": url, "path": str(destination),
                        "status": "SKIPPED_EXISTING_VALID",
                        "sha256": sha256_bytes(data), "bytes": len(data),
                        "record_count": count,
                    }) + "\n")
                    continue
                destination.unlink()

            if args.dry_run:
                print(url)
                continue

            requests_seen += 1
            status = None
            data = b""
            error = None
            for attempt in range(args.retries + 1):
                status, data, error = fetch(url, args.timeout)
                if status == 200 and data:
                    break
                if attempt < args.retries:
                    time.sleep(args.sleep_seconds * (2 ** attempt))

            if status != 200:
                if status is None:
                    transport_errors += 1
                    state = "TRANSPORT_ERROR"
                else:
                    http_errors += 1
                    state = f"HTTP_{status}"
                log.write(json.dumps({
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "date": day.isoformat(), "hour": hour, "url": url,
                    "path": str(destination), "status": state,
                    "http_status": status, "error": error,
                }) + "\n")
            elif not data:
                empty_payloads += 1
                log.write(json.dumps({
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "date": day.isoformat(), "hour": hour, "url": url,
                    "path": str(destination), "status": "EMPTY_PAYLOAD",
                    "http_status": status,
                }) + "\n")
            else:
                valid, validation_error, count = validate_bi5(data, day, hour)
                if not valid:
                    invalid_payloads += 1
                    log.write(json.dumps({
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "date": day.isoformat(), "hour": hour, "url": url,
                        "path": str(destination), "status": "INVALID_PAYLOAD",
                        "http_status": status, "sha256": sha256_bytes(data),
                        "bytes": len(data), "record_count": count,
                        "error": validation_error,
                    }) + "\n")
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    temp = destination.with_suffix(destination.suffix + ".part")
                    temp.write_bytes(data)
                    temp.replace(destination)
                    downloaded_valid += 1
                    log.write(json.dumps({
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "date": day.isoformat(), "hour": hour, "url": url,
                        "path": str(destination), "status": "DOWNLOADED_VALID",
                        "http_status": status, "sha256": sha256_bytes(data),
                        "bytes": len(data), "record_count": count,
                    }) + "\n")

            time.sleep(args.sleep_seconds)

    summary = {
        "instrument": INSTRUMENT,
        "source": "Dukascopy",
        "format": "BI5",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "hour_filter": args.hour,
        "all_hours_attempted": args.hour is None,
        "downloaded_valid": downloaded_valid,
        "skipped_existing_valid": skipped_existing,
        "empty_payloads": empty_payloads,
        "http_errors": http_errors,
        "transport_errors": transport_errors,
        "invalid_payloads": invalid_payloads,
        "requests_seen": requests_seen,
        "dry_run": args.dry_run,
    }
    print(json.dumps(summary, indent=2))
    return 0 if transport_errors == 0 and http_errors == 0 and invalid_payloads == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
