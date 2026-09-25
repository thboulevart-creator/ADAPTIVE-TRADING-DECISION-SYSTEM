#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_F1_SHA256 = "2b95780b053e7c83bdb48e10eb6702828e3d80ebf38e1a68eb811890a9523067"
EXPECTED_F1_SCHEMA = "ATDS_E0_SOURCE_B_F1_TIMESTAMP_SCAN_V0_1"
EXPECTED_GAPS = 1605
EXPECTED_ROWS = 376_003_618
NY = ZoneInfo("America/New_York")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def local_dt(day, hour, minute=0):
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=NY)


def closed_intervals_covering(start_utc: datetime, end_utc: datetime):
    # Build exact regular-session closed intervals around the gap.
    # Mon-Thu: daily 16:15 -> 18:00 NY.
    # Fri: 16:15 NY -> Sun 18:00 NY.
    start_day = start_utc.astimezone(NY).date() - timedelta(days=3)
    end_day = end_utc.astimezone(NY).date() + timedelta(days=3)
    day = start_day
    while day <= end_day:
        wd = day.weekday()  # Mon=0 ... Sun=6
        if wd <= 3:
            a = local_dt(day, 16, 15).astimezone(timezone.utc)
            b = local_dt(day, 18, 0).astimezone(timezone.utc)
            yield a, b, "DAILY_BREAK"
        elif wd == 4:
            a = local_dt(day, 16, 15).astimezone(timezone.utc)
            sunday = day + timedelta(days=2)
            b = local_dt(sunday, 18, 0).astimezone(timezone.utc)
            yield a, b, "WEEKEND_BREAK"
        day += timedelta(days=1)


def overlaps_open_interval(gap_start: datetime, gap_end: datetime, closed_start: datetime, closed_end: datetime) -> bool:
    # Gaps are intervals strictly between the last observed tick and next observed tick.
    # Any positive-duration overlap with a scheduled closed interval makes it a
    # regular-session boundary gap.
    return max(gap_start, closed_start) < min(gap_end, closed_end)


def classify_gap(previous_ms: int, current_ms: int):
    start = datetime.fromtimestamp(previous_ms / 1000, tz=timezone.utc)
    end = datetime.fromtimestamp(current_ms / 1000, tz=timezone.utc)
    hits = []
    for a, b, kind in closed_intervals_covering(start, end):
        if overlaps_open_interval(start, end, a, b):
            hits.append({
                "kind": kind,
                "closed_start_utc": a.isoformat(),
                "closed_end_utc": b.isoformat(),
            })
    return ("SESSION_BOUNDARY_GAP" if hits else "TRUE_OPEN_SESSION_GAP"), hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--f1-report", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-E0-SOURCE-B-REGULAR-SESSION-GAPS.json"),
    )
    args = ap.parse_args()

    src = Path(args.f1_report).expanduser().resolve(strict=False)
    out = Path(args.output).expanduser().resolve(strict=False)

    if not src.is_file():
        print("BLOCKED_F1_NOT_FOUND")
        return 2
    if sha256_path(src) != EXPECTED_F1_SHA256:
        print("BLOCKED_F1_SHA256_MISMATCH")
        return 2

    f1 = json.loads(src.read_text(encoding="utf-8"))
    if f1.get("schema") != EXPECTED_F1_SCHEMA or f1.get("status") != "F1_COMPLETE":
        print("BLOCKED_F1_CONTRACT")
        return 2
    summary = f1.get("summary") or {}
    gaps = f1.get("recorded_gaps_gt_60s")
    if summary.get("rows_read") != EXPECTED_ROWS:
        print("BLOCKED_F1_ROW_COUNT")
        return 2
    if summary.get("recorded_gaps_gt_60s") != EXPECTED_GAPS:
        print("BLOCKED_F1_GAP_COUNT")
        return 2
    if not isinstance(gaps, list) or len(gaps) != EXPECTED_GAPS:
        print("BLOCKED_F1_GAP_LIST")
        return 2
    if summary.get("gap_records_truncated") is not False:
        print("BLOCKED_F1_GAP_LIST_TRUNCATED")
        return 2

    rows = []
    counts = {"SESSION_BOUNDARY_GAP": 0, "TRUE_OPEN_SESSION_GAP": 0}
    for idx, g in enumerate(gaps):
        p = int(g["previous_ms"])
        c = int(g["current_ms"])
        if c <= p:
            print("BLOCKED_NONPOSITIVE_GAP")
            return 2
        cls, hits = classify_gap(p, c)
        counts[cls] += 1
        rows.append({
            "gap_index": idx,
            "previous_ms": p,
            "current_ms": c,
            "gap_ms": c - p,
            "previous_utc": datetime.fromtimestamp(p / 1000, tz=timezone.utc).isoformat(),
            "current_utc": datetime.fromtimestamp(c / 1000, tz=timezone.utc).isoformat(),
            "classification": cls,
            "regular_closed_interval_hits": hits,
        })

    payload = {
        "schema": "ATDS_E0_SOURCE_B_REGULAR_SESSION_GAPS_V0_1",
        "status": "COMPLETE",
        "binding": {
            "f1_sha256": EXPECTED_F1_SHA256,
            "raw_clock_semantics": "GMT_UTC_FOR_REGULAR_SESSION_CLASSIFICATION_PASS_WITH_LIMITATION",
            "session_timezone": "America/New_York",
        },
        "regular_session_contract": {
            "weekly_open": "Sunday 18:00 America/New_York",
            "weekly_close": "Friday 16:15 America/New_York",
            "daily_break": "16:15-18:00 America/New_York",
            "holiday_overrides_applied": False,
        },
        "counts": counts,
        "gaps": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("REGULAR_SESSION_GAP_CLASSIFICATION_COMPLETE")
    print(f"SESSION_BOUNDARY_GAP: {counts['SESSION_BOUNDARY_GAP']}")
    print(f"TRUE_OPEN_SESSION_GAP: {counts['TRUE_OPEN_SESSION_GAP']}")
    print(f"Report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
