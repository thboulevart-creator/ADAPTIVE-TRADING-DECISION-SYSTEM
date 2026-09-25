#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
MAX_OUTPUT_BYTES = 32 * 1024 * 1024

REQUIRED_SCHEMA = [
    ("minute_start_ms_utc", "int64"),
    ("first_tick_ms", "int64"),
    ("last_tick_ms", "int64"),
    ("tick_count", "int64"),
    ("segment_id", "int64"),
    ("segment_start", "bool"),
    ("gap_before_ms", "int64"),
    ("mid_open", "double"),
    ("mid_high", "double"),
    ("mid_low", "double"),
    ("mid_close", "double"),
    ("spread_mean", "double"),
    ("spread_min", "double"),
    ("spread_max", "double"),
]
READ_COLUMNS = [
    "minute_start_ms_utc",
    "tick_count",
    "segment_id",
    "segment_start",
    "mid_high",
    "mid_low",
    "spread_mean",
    "spread_min",
    "spread_max",
]
NY = ZoneInfo("America/New_York")
WEEKDAY_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(data) > MAX_OUTPUT_BYTES:
        raise RuntimeError(f"AP1 JSON exceeds {MAX_OUTPUT_BYTES} bytes.")
    path.write_bytes(data)


def pct(a, q: float):
    if a.size == 0:
        return None
    return float(__import__("numpy").percentile(a, q))


def summary_for_indices(idx, tick_count, minute_range, spread_mean, spread_max):
    import numpy as np
    n = int(idx.size)
    if n == 0:
        return {
            "minute_count": 0,
            "source_tick_count": 0,
            "tick_count_mean": None,
            "tick_count_p50": None,
            "tick_count_p90": None,
            "tick_count_p99": None,
            "minute_range_mean": None,
            "minute_range_p50": None,
            "minute_range_p90": None,
            "minute_range_p95": None,
            "minute_range_p99": None,
            "spread_tick_weighted_mean": None,
            "spread_mean_p50": None,
            "spread_mean_p90": None,
            "spread_mean_p95": None,
            "spread_mean_p99": None,
            "spread_max_observed": None,
        }

    tc = tick_count[idx]
    rg = minute_range[idx]
    sm = spread_mean[idx]
    sx = spread_max[idx]
    ticks = int(np.sum(tc, dtype=np.int64))
    weighted_spread = float(np.sum(sm * tc, dtype=np.float64) / ticks)

    return {
        "minute_count": n,
        "source_tick_count": ticks,
        "tick_count_mean": float(np.mean(tc)),
        "tick_count_p50": float(np.percentile(tc, 50)),
        "tick_count_p90": float(np.percentile(tc, 90)),
        "tick_count_p99": float(np.percentile(tc, 99)),
        "minute_range_mean": float(np.mean(rg)),
        "minute_range_p50": float(np.percentile(rg, 50)),
        "minute_range_p90": float(np.percentile(rg, 90)),
        "minute_range_p95": float(np.percentile(rg, 95)),
        "minute_range_p99": float(np.percentile(rg, 99)),
        "spread_tick_weighted_mean": weighted_spread,
        "spread_mean_p50": float(np.percentile(sm, 50)),
        "spread_mean_p90": float(np.percentile(sm, 90)),
        "spread_mean_p95": float(np.percentile(sm, 95)),
        "spread_mean_p99": float(np.percentile(sm, 99)),
        "spread_max_observed": float(np.max(sx)),
    }


def summarize_dimension(codes, expected_codes, label_fn, tick_count, minute_range, spread_mean, spread_max):
    import numpy as np
    order = np.argsort(codes, kind="stable")
    sorted_codes = codes[order]
    unique, starts, counts = np.unique(sorted_codes, return_index=True, return_counts=True)
    spans = {int(code): (int(start), int(count)) for code, start, count in zip(unique, starts, counts)}
    out = []
    for code in expected_codes:
        if int(code) in spans:
            start, count = spans[int(code)]
            idx = order[start:start + count]
        else:
            idx = np.empty(0, dtype=np.int64)
        out.append({
            "code": int(code),
            "label": label_fn(int(code)),
            **summary_for_indices(idx, tick_count, minute_range, spread_mean, spread_max),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="AP1 strategy-agnostic intraday and spread census.")
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-AP1-INTRADAY-SPREAD-CENSUS.json"),
    )
    args = ap.parse_args()

    root = Path(args.ap0_root).expanduser().resolve(strict=False)
    manifest_path = Path(args.ap0_manifest).expanduser().resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)

    def block(code: str, reason: str) -> int:
        payload = {
            "schema": "ATDS_AP1_INTRADAY_SPREAD_CENSUS_BLOCKED_V0_1",
            "status": code,
            "reason": reason,
        }
        try:
            write_json(output, payload)
        except Exception:
            pass
        print(code)
        print(reason)
        print(f"Report: {output}")
        return 2

    if not root.is_dir():
        return block("BLOCKED_AP1_ROOT_NOT_FOUND", str(root))
    if not manifest_path.is_file():
        return block("BLOCKED_AP1_MANIFEST_NOT_FOUND", str(manifest_path))
    if sha256_path(manifest_path) != EXPECTED_AP0_MANIFEST_SHA256:
        return block("BLOCKED_AP1_MANIFEST_SHA", "AP0 manifest SHA-256 mismatch.")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return block("BLOCKED_AP1_MANIFEST_PARSE", str(exc))

    if manifest.get("status") != "AP0_COMPLETE":
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 status is not complete.")
    if manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 identity mismatch.")
    files = manifest.get("files")
    cov = manifest.get("coverage") or {}
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 file count mismatch.")
    if cov.get("minute_rows_written") != EXPECTED_MINUTES:
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 minute count mismatch.")
    if cov.get("source_ticks_read") != EXPECTED_SOURCE_TICKS:
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 source tick count mismatch.")
    if cov.get("segments") != EXPECTED_SEGMENTS or cov.get("segment_start_rows") != EXPECTED_SEGMENTS:
        return block("BLOCKED_AP1_MANIFEST_CONTRACT", "AP0 segment count mismatch.")

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        return block("BLOCKED_AP1_RUNTIME_DEPENDENCY", str(exc))

    minute_chunks = []
    tick_chunks = []
    segment_chunks = []
    segment_start_chunks = []
    range_chunks = []
    spread_mean_chunks = []
    spread_max_chunks = []

    actual_rows = 0
    actual_ticks = 0
    actual_segment_starts = 0
    previous_minute = None
    previous_segment = None

    try:
        for rec in files:
            rel = rec["relative_path"]
            path = (root / Path(rel)).resolve(strict=False)
            try:
                if os.path.commonpath([os.path.normcase(str(path)), os.path.normcase(str(root))]) != os.path.normcase(str(root)):
                    raise RuntimeError(f"Path escapes AP0 root: {rel}")
            except ValueError:
                raise RuntimeError(f"Path escapes AP0 root: {rel}")
            if not path.is_file():
                raise RuntimeError(f"Missing AP0 file: {rel}")
            if int(path.stat().st_size) != int(rec["size_bytes"]):
                raise RuntimeError(f"AP0 file size mismatch: {rel}")
            if sha256_path(path) != rec["sha256"]:
                raise RuntimeError(f"AP0 file SHA-256 mismatch: {rel}")

            pf = pq.ParquetFile(path)
            if int(pf.metadata.num_rows) != int(rec["rows"]):
                raise RuntimeError(f"AP0 Parquet row count mismatch: {rel}")

            schema = pf.schema_arrow
            observed_schema = [(field.name, str(field.type)) for field in schema]
            if observed_schema != REQUIRED_SCHEMA:
                raise RuntimeError(f"AP0 schema mismatch: {rel}")
            meta = schema.metadata or {}
            if meta.get(b"dataset_identity") != EXPECTED_AP0_IDENTITY.encode():
                raise RuntimeError(f"AP0 dataset identity metadata mismatch: {rel}")
            if meta.get(b"volumes_used") != b"false":
                raise RuntimeError(f"AP0 volume metadata violation: {rel}")
            if meta.get(b"mid_semantics") != b"descriptive_only_not_execution_price":
                raise RuntimeError(f"AP0 mid semantics mismatch: {rel}")

            table = pf.read(columns=READ_COLUMNS, use_threads=False)
            if table.column_names != READ_COLUMNS:
                raise RuntimeError(f"AP1 column-scope violation: {rel}")

            minute = table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            tick = table["tick_count"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            seg = table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            seg_start = table["segment_start"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.bool_, copy=False)
            high = table["mid_high"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            low = table["mid_low"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            spread_mean = table["spread_mean"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            spread_min = table["spread_min"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            spread_max = table["spread_max"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

            n = minute.size
            if n != int(rec["rows"]):
                raise RuntimeError(f"AP1 decoded row count mismatch: {rel}")
            if n == 0:
                raise RuntimeError(f"Unexpected empty AP0 file: {rel}")
            if np.any(np.diff(minute) <= 0):
                raise RuntimeError(f"Minute order violation: {rel}")
            if previous_minute is not None and int(minute[0]) <= previous_minute:
                raise RuntimeError(f"Global minute order violation: {rel}")
            if np.any(tick <= 0):
                raise RuntimeError(f"Nonpositive tick_count: {rel}")
            if not np.all(np.isfinite(high)) or not np.all(np.isfinite(low)):
                raise RuntimeError(f"Nonfinite mid range field: {rel}")
            if np.any(high < low):
                raise RuntimeError(f"mid_high < mid_low: {rel}")
            if not np.all(np.isfinite(spread_mean)) or not np.all(np.isfinite(spread_min)) or not np.all(np.isfinite(spread_max)):
                raise RuntimeError(f"Nonfinite spread field: {rel}")
            if np.any(spread_min <= 0) or np.any(spread_min > spread_mean) or np.any(spread_mean > spread_max):
                raise RuntimeError(f"Spread invariant violation: {rel}")

            dseg = np.diff(seg)
            if np.any(dseg < 0) or np.any(dseg > 1):
                raise RuntimeError(f"Segment jump violation: {rel}")
            if n > 1 and not np.array_equal(seg_start[1:], dseg == 1):
                raise RuntimeError(f"segment_start mismatch inside file: {rel}")
            if previous_segment is None:
                if int(seg[0]) != 0 or not bool(seg_start[0]):
                    raise RuntimeError("First AP0 row must start segment 0.")
            else:
                delta = int(seg[0]) - previous_segment
                if delta not in (0, 1):
                    raise RuntimeError(f"Segment boundary jump violation: {rel}")
                if bool(seg_start[0]) != (delta == 1):
                    raise RuntimeError(f"Segment boundary start flag mismatch: {rel}")

            minute_range = high - low

            actual_rows += int(n)
            actual_ticks += int(np.sum(tick, dtype=np.int64))
            actual_segment_starts += int(np.count_nonzero(seg_start))
            previous_minute = int(minute[-1])
            previous_segment = int(seg[-1])

            minute_chunks.append(minute.copy())
            tick_chunks.append(tick.copy())
            segment_chunks.append(seg.copy())
            segment_start_chunks.append(seg_start.copy())
            range_chunks.append(minute_range.copy())
            spread_mean_chunks.append(spread_mean.copy())
            spread_max_chunks.append(spread_max.copy())

            del table, minute, tick, seg, seg_start, high, low, spread_mean, spread_min, spread_max, minute_range

        if actual_rows != EXPECTED_MINUTES:
            raise RuntimeError(f"AP1 rows {actual_rows} != {EXPECTED_MINUTES}")
        if actual_ticks != EXPECTED_SOURCE_TICKS:
            raise RuntimeError(f"AP1 source ticks {actual_ticks} != {EXPECTED_SOURCE_TICKS}")
        if actual_segment_starts != EXPECTED_SEGMENTS:
            raise RuntimeError(f"AP1 segment starts {actual_segment_starts} != {EXPECTED_SEGMENTS}")
        if previous_segment != EXPECTED_SEGMENTS - 1:
            raise RuntimeError(f"AP1 last segment {previous_segment} != {EXPECTED_SEGMENTS - 1}")

        minute = np.concatenate(minute_chunks)
        tick = np.concatenate(tick_chunks)
        segment_start = np.concatenate(segment_start_chunks)
        minute_range = np.concatenate(range_chunks)
        spread_mean = np.concatenate(spread_mean_chunks)
        spread_max = np.concatenate(spread_max_chunks)

        utc_hour_code = minute // 3_600_000
        utc_hour = (utc_hour_code % 24).astype(np.int16)

        unique_hours, inverse = np.unique(utc_hour_code, return_inverse=True)
        ny_hour_map = np.empty(unique_hours.size, dtype=np.int16)
        ny_weekday_map = np.empty(unique_hours.size, dtype=np.int16)
        utc_year_map = np.empty(unique_hours.size, dtype=np.int16)

        for i, hour_code in enumerate(unique_hours):
            utc_dt = datetime.fromtimestamp(int(hour_code) * 3600, tz=timezone.utc)
            ny_dt = utc_dt.astimezone(NY)
            ny_hour_map[i] = ny_dt.hour
            ny_weekday_map[i] = ny_dt.weekday()
            utc_year_map[i] = utc_dt.year

        ny_hour = ny_hour_map[inverse]
        ny_weekday = ny_weekday_map[inverse]
        ny_weekday_hour = (ny_weekday * 24 + ny_hour).astype(np.int16)
        utc_year = utc_year_map[inverse]

        all_idx = np.arange(minute.size, dtype=np.int64)
        global_summary = summary_for_indices(all_idx, tick, minute_range, spread_mean, spread_max)
        global_summary["segment_start_count"] = int(np.count_nonzero(segment_start))

        utc_hour_summary = summarize_dimension(
            utc_hour, range(24), lambda x: f"{x:02d}:00 UTC",
            tick, minute_range, spread_mean, spread_max,
        )
        ny_hour_summary = summarize_dimension(
            ny_hour, range(24), lambda x: f"{x:02d}:00 America/New_York",
            tick, minute_range, spread_mean, spread_max,
        )
        ny_weekday_summary = summarize_dimension(
            ny_weekday, range(7), lambda x: WEEKDAY_NAMES[x],
            tick, minute_range, spread_mean, spread_max,
        )
        ny_weekday_hour_summary = summarize_dimension(
            ny_weekday_hour, range(168),
            lambda x: f"{WEEKDAY_NAMES[x // 24]} {x % 24:02d}:00 America/New_York",
            tick, minute_range, spread_mean, spread_max,
        )
        year_summary = summarize_dimension(
            utc_year, range(2021, 2027), lambda x: f"{x} UTC-year",
            tick, minute_range, spread_mean, spread_max,
        )

        for bucket_list in (utc_hour_summary, ny_hour_summary, ny_weekday_summary, ny_weekday_hour_summary, year_summary):
            for item in bucket_list:
                code = item["code"]
                if bucket_list is utc_hour_summary:
                    mask = utc_hour == code
                elif bucket_list is ny_hour_summary:
                    mask = ny_hour == code
                elif bucket_list is ny_weekday_summary:
                    mask = ny_weekday == code
                elif bucket_list is ny_weekday_hour_summary:
                    mask = ny_weekday_hour == code
                else:
                    mask = utc_year == code
                item["segment_start_count"] = int(np.count_nonzero(segment_start[mask]))

        if sum(x["minute_count"] for x in utc_hour_summary) != EXPECTED_MINUTES:
            raise RuntimeError("UTC-hour census row conservation failed.")
        if sum(x["minute_count"] for x in ny_hour_summary) != EXPECTED_MINUTES:
            raise RuntimeError("NY-hour census row conservation failed.")
        if sum(x["minute_count"] for x in ny_weekday_summary) != EXPECTED_MINUTES:
            raise RuntimeError("NY-weekday census row conservation failed.")
        if sum(x["minute_count"] for x in ny_weekday_hour_summary) != EXPECTED_MINUTES:
            raise RuntimeError("NY weekday-hour census row conservation failed.")
        if sum(x["minute_count"] for x in year_summary) != EXPECTED_MINUTES:
            raise RuntimeError("Year census row conservation failed.")

        payload = {
            "schema": "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1",
            "status": "AP1_COMPLETE",
            "input_identity": EXPECTED_AP0_IDENTITY,
            "binding": {
                "ap0_manifest_sha256": EXPECTED_AP0_MANIFEST_SHA256,
                "ap0_files_rehashed": EXPECTED_FILES,
            },
            "scope": {
                "strategy_agnostic": True,
                "returns_calculated": False,
                "signals_calculated": False,
                "pnl_calculated": False,
                "source_volume_used": False,
                "timezone_source": "UTC",
                "intraday_timezone": "America/New_York",
            },
            "coverage": {
                "minute_rows": actual_rows,
                "source_ticks": actual_ticks,
                "segment_start_rows": actual_segment_starts,
                "first_minute_ms_utc": int(minute[0]),
                "last_minute_ms_utc": int(minute[-1]),
            },
            "metric_contract": {
                "minute_range": "mid_high - mid_low",
                "spread_tick_weighted_mean": "sum(spread_mean * tick_count) / sum(tick_count)",
                "spread_distribution_basis": "per-minute spread_mean",
                "percentiles": [50, 90, 95, 99],
                "tick_count_percentiles": [50, 90, 99],
                "optimization": False,
            },
            "global": global_summary,
            "utc_hour": utc_hour_summary,
            "new_york_hour": ny_hour_summary,
            "new_york_weekday": ny_weekday_summary,
            "new_york_weekday_hour": ny_weekday_hour_summary,
            "utc_year": year_summary,
            "runtime": {
                "numpy_version": np.__version__,
                "pyarrow_version": pa.__version__,
            },
        }

        write_json(output, payload)
        print("AP1_COMPLETE")
        print(f"Minute rows: {actual_rows}")
        print(f"Source ticks: {actual_ticks}")
        print(f"Segment starts: {actual_segment_starts}")
        print(f"Global minute range mean: {global_summary['minute_range_mean']}")
        print(f"Global tick-weighted spread mean: {global_summary['spread_tick_weighted_mean']}")
        print(f"Report: {output}")
        return 0

    except Exception as exc:
        return block("BLOCKED_AP1_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
