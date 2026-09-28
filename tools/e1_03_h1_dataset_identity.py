from __future__ import annotations

import hashlib
import json
import math
import struct
from pathlib import Path


CONTRACT = "ATDS_E1_03_H1_DATASET_IDENTITY_V0_1"

HOUR_MS = 3_600_000
MINUTE_MS = 60_000
OOS_START_MS = 1_748_131_200_000
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
REQUIRED_COLUMNS = (
    "minute_start_ms_utc",
    "first_tick_ms",
    "last_tick_ms",
    "tick_count",
    "segment_id",
    "segment_start",
    "gap_before_ms",
    "mid_close",
)
CANONICAL_PREFIX = b"ATDS_E1_H1_CANONICAL_STREAM_V0_1\\n"


def _blocked(reason: str) -> dict:
    return {"status": "BLOCKED", "reason": reason}


def derive_h1_dataset(
    minute_rows,
    *,
    raw_window_start_ms: int,
    raw_window_end_ms: int,
):
    rows = list(minute_rows)
    if raw_window_end_ms <= raw_window_start_ms:
        return _blocked("INVALID_RAW_WINDOW")

    timestamps = []
    for row in rows:
        if not isinstance(row, dict):
            return _blocked("INVALID_M1_ROW")
        if any(name not in row for name in REQUIRED_COLUMNS):
            return _blocked("MISSING_REQUIRED_M1_FIELD")
        try:
            ts = int(row["minute_start_ms_utc"])
            float(row["mid_close"])
            int(row["segment_id"])
        except (TypeError, ValueError, OverflowError):
            return _blocked("INVALID_M1_VALUE")
        timestamps.append(ts)

    if len(timestamps) != len(set(timestamps)):
        return _blocked("DUPLICATE_M1_TIMESTAMP")

    ordered = sorted(rows, key=lambda r: int(r["minute_start_ms_utc"]))
    buckets: dict[int, list[dict]] = {}
    for row in ordered:
        ts = int(row["minute_start_ms_utc"])
        bucket = (ts // HOUR_MS) * HOUR_MS
        buckets.setdefault(bucket, []).append(row)

    first_boundary_bucket = None
    if raw_window_start_ms % HOUR_MS != 0:
        first_boundary_bucket = (raw_window_start_ms // HOUR_MS) * HOUR_MS

    last_boundary_bucket = None
    if raw_window_end_ms % HOUR_MS != 0:
        last_boundary_bucket = (raw_window_end_ms // HOUR_MS) * HOUR_MS

    candidates: list[tuple[int, int, bool, float]] = []
    for bucket_start in sorted(buckets):
        bucket_rows = buckets[bucket_start]

        if bucket_start == first_boundary_bucket or bucket_start == last_boundary_bucket:
            continue
        if len(bucket_rows) != 60:
            continue

        expected_ts = [bucket_start + i * MINUTE_MS for i in range(60)]
        actual_ts = [int(r["minute_start_ms_utc"]) for r in bucket_rows]
        if actual_ts != expected_ts:
            continue

        segments = {int(r["segment_id"]) for r in bucket_rows}
        if len(segments) != 1:
            continue

        bad_segment_start = any(
            bool(r["segment_start"]) and i != 0
            for i, r in enumerate(bucket_rows)
        )
        if bad_segment_start:
            continue

        close = float(bucket_rows[-1]["mid_close"])
        if not math.isfinite(close):
            return _blocked("NONFINITE_MID_CLOSE")

        candidates.append(
            (
                bucket_start,
                next(iter(segments)),
                bool(bucket_rows[0]["segment_start"]),
                close,
            )
        )

    output_rows: list[dict] = []
    block_id = -1
    ordinal = -1
    previous_start = None
    previous_segment = None

    for bucket_start, segment_id, starts_segment, close in candidates:
        new_block = (
            previous_start is None
            or segment_id != previous_segment
            or bucket_start != previous_start + HOUR_MS
            or starts_segment
        )
        if new_block:
            block_id += 1
            ordinal = 0
        else:
            ordinal += 1

        output_rows.append(
            {
                "h1_start_ms_utc": int(bucket_start),
                "source_segment_id": int(segment_id),
                "continuity_block_id": int(block_id),
                "continuity_ordinal": int(ordinal),
                "mid_close": float(close),
            }
        )
        previous_start = bucket_start
        previous_segment = segment_id

    pre_oos = sum(1 for r in output_rows if r["h1_start_ms_utc"] < OOS_START_MS)
    oos = len(output_rows) - pre_oos
    eligible = sum(1 for r in output_rows if r["continuity_ordinal"] >= 20)

    manifest = {
        "output_identity": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
        "accepted_h1_rows": len(output_rows),
        "pre_oos_h1_rows": pre_oos,
        "oos_h1_rows": oos,
        "momentum_eligible_h1_rows": eligible,
        "continuity_blocks": 0 if not output_rows else max(r["continuity_block_id"] for r in output_rows) + 1,
        "first_admissible_h1": None if not output_rows else output_rows[0]["h1_start_ms_utc"],
        "last_admissible_h1": None if not output_rows else output_rows[-1]["h1_start_ms_utc"],
    }
    return {"status": "PASS", "rows": output_rows, "manifest": manifest}


def canonical_stream_sha256(rows) -> str:
    h = hashlib.sha256()
    h.update(CANONICAL_PREFIX)
    for row in rows:
        h.update(
            struct.pack(
                ">qqqqd",
                int(row["h1_start_ms_utc"]),
                int(row["source_segment_id"]),
                int(row["continuity_block_id"]),
                int(row["continuity_ordinal"]),
                float(row["mid_close"]),
            )
        )
    return h.hexdigest()


def verify_ap0_binding(
    manifest_path,
    ap0_root,
    *,
    expected_manifest_sha256: str,
):
    manifest_path = Path(manifest_path)
    root = Path(ap0_root)
    try:
        manifest_raw = manifest_path.read_bytes()
    except OSError:
        return _blocked("AP0_MANIFEST_UNREADABLE")

    if hashlib.sha256(manifest_raw).hexdigest() != expected_manifest_sha256:
        return _blocked("AP0_MANIFEST_SHA256_MISMATCH")

    try:
        manifest = json.loads(manifest_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _blocked("AP0_MANIFEST_PARSE_ERROR")

    if manifest.get("status") != "AP0_COMPLETE":
        return _blocked("AP0_STATUS_MISMATCH")
    if manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
        return _blocked("AP0_IDENTITY_MISMATCH")

    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != 61:
        return _blocked("AP0_FILE_COUNT_MISMATCH")

    root_resolved = root.resolve(strict=False)
    for rec in files:
        if not isinstance(rec, dict):
            return _blocked("AP0_FILE_RECORD_INVALID")
        rel = rec.get("path")
        expected_sha = rec.get("sha256")
        expected_size = rec.get("size_bytes")
        if not isinstance(rel, str) or not isinstance(expected_sha, str):
            return _blocked("AP0_FILE_RECORD_INVALID")
        path = (root / rel).resolve(strict=False)
        try:
            path.relative_to(root_resolved)
        except ValueError:
            return _blocked("AP0_PATH_ESCAPE")
        try:
            raw = path.read_bytes()
        except OSError:
            return _blocked("AP0_FILE_UNREADABLE")
        if expected_size is not None and len(raw) != int(expected_size):
            return _blocked("AP0_FILE_SIZE_MISMATCH")
        if hashlib.sha256(raw).hexdigest() != expected_sha:
            return _blocked("AP0_FILE_SHA256_MISMATCH")

    return {"status": "PASS", "files_rehashed": 61}
