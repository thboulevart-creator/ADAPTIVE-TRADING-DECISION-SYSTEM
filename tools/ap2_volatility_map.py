#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

EXPECTED_AP0_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_AP1_SHA256 = "db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
HORIZONS = (1, 5, 15, 60)
RV_HORIZONS = (5, 15, 60)
NY = ZoneInfo("America/New_York")

READ_COLUMNS = [
    "minute_start_ms_utc",
    "segment_id",
    "mid_open",
    "mid_high",
    "mid_low",
    "mid_close",
]
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


def sha256_path(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    if len(raw) > MAX_OUTPUT_BYTES:
        raise RuntimeError("AP2 output exceeds 32 MiB.")
    path.write_bytes(raw)


def metric_summary(values):
    import numpy as np
    x = values[np.isfinite(values)]
    if x.size == 0:
        return {
            "count": 0, "mean": None, "p50": None, "p90": None,
            "p95": None, "p99": None, "p99_9": None, "max": None,
        }
    return {
        "count": int(x.size),
        "mean": float(np.mean(x)),
        "p50": float(np.percentile(x, 50, method="linear")),
        "p90": float(np.percentile(x, 90, method="linear")),
        "p95": float(np.percentile(x, 95, method="linear")),
        "p99": float(np.percentile(x, 99, method="linear")),
        "p99_9": float(np.percentile(x, 99.9, method="linear")),
        "max": float(np.max(x)),
    }


def bucket_summary(mask, metrics):
    return {name: metric_summary(values[mask]) for name, values in metrics.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description="AP2 strategy-agnostic gap-aware volatility map.")
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument("--ap1-report", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-AP2-VOLATILITY-MAP.json"),
    )
    args = ap.parse_args()

    root = Path(args.ap0_root).expanduser().resolve(strict=False)
    manifest_path = Path(args.ap0_manifest).expanduser().resolve(strict=False)
    ap1_path = Path(args.ap1_report).expanduser().resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)

    def block(code: str, reason: str) -> int:
        try:
            write_json(output, {"schema":"ATDS_AP2_BLOCKED_V0_1","status":code,"reason":reason})
        except Exception:
            pass
        print(code)
        print(reason)
        print(f"Report: {output}")
        return 2

    if not root.is_dir():
        return block("BLOCKED_AP2_ROOT_NOT_FOUND", str(root))
    if not manifest_path.is_file() or not ap1_path.is_file():
        return block("BLOCKED_AP2_INPUT_NOT_FOUND", "AP0 manifest or AP1 report missing.")
    if sha256_path(manifest_path) != EXPECTED_AP0_MANIFEST_SHA256:
        return block("BLOCKED_AP2_AP0_MANIFEST_SHA", "AP0 manifest SHA mismatch.")
    if sha256_path(ap1_path) != EXPECTED_AP1_SHA256:
        return block("BLOCKED_AP2_AP1_SHA", "AP1 report SHA mismatch.")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ap1 = json.loads(ap1_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return block("BLOCKED_AP2_JSON_PARSE", str(exc))

    if manifest.get("status") != "AP0_COMPLETE" or manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP2_AP0_CONTRACT", "AP0 identity/status mismatch.")
    files = manifest.get("files")
    cov = manifest.get("coverage") or {}
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        return block("BLOCKED_AP2_AP0_CONTRACT", "AP0 file count mismatch.")
    if cov.get("minute_rows_written") != EXPECTED_MINUTES or cov.get("source_ticks_read") != EXPECTED_SOURCE_TICKS:
        return block("BLOCKED_AP2_AP0_CONTRACT", "AP0 coverage mismatch.")
    if cov.get("segments") != EXPECTED_SEGMENTS:
        return block("BLOCKED_AP2_AP0_CONTRACT", "AP0 segment count mismatch.")

    if ap1.get("status") != "AP1_COMPLETE" or ap1.get("input_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP2_AP1_CONTRACT", "AP1 status/input mismatch.")
    a1cov = ap1.get("coverage") or {}
    if a1cov.get("minute_rows") != EXPECTED_MINUTES or a1cov.get("source_ticks") != EXPECTED_SOURCE_TICKS:
        return block("BLOCKED_AP2_AP1_CONTRACT", "AP1 coverage mismatch.")
    scope = ap1.get("scope") or {}
    if scope.get("strategy_agnostic") is not True or scope.get("returns_calculated") is not False:
        return block("BLOCKED_AP2_AP1_CONTRACT", "AP1 scope mismatch.")

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        return block("BLOCKED_AP2_RUNTIME_DEPENDENCY", str(exc))

    minute_chunks, seg_chunks = [], []
    open_chunks, high_chunks, low_chunks, close_chunks = [], [], [], []
    rows = 0
    previous_minute = None
    previous_segment = None

    try:
        for rec in files:
            rel = rec["relative_path"]
            p = (root / Path(rel)).resolve(strict=False)
            try:
                if os.path.commonpath([os.path.normcase(str(p)), os.path.normcase(str(root))]) != os.path.normcase(str(root)):
                    raise RuntimeError(f"Path escape: {rel}")
            except ValueError:
                raise RuntimeError(f"Path escape: {rel}")
            if not p.is_file():
                raise RuntimeError(f"Missing AP0 file: {rel}")
            if int(p.stat().st_size) != int(rec["size_bytes"]) or sha256_path(p) != rec["sha256"]:
                raise RuntimeError(f"AP0 file identity mismatch: {rel}")

            pf = pq.ParquetFile(p)
            if int(pf.metadata.num_rows) != int(rec["rows"]):
                raise RuntimeError(f"AP0 row count mismatch: {rel}")
            observed_schema = [(f.name, str(f.type)) for f in pf.schema_arrow]
            if observed_schema != REQUIRED_SCHEMA:
                raise RuntimeError(f"AP0 schema mismatch: {rel}")
            meta = pf.schema_arrow.metadata or {}
            if meta.get(b"dataset_identity") != EXPECTED_AP0_IDENTITY.encode():
                raise RuntimeError(f"AP0 identity metadata mismatch: {rel}")
            if meta.get(b"volumes_used") != b"false":
                raise RuntimeError(f"AP0 volume metadata violation: {rel}")
            if meta.get(b"mid_semantics") != b"descriptive_only_not_execution_price":
                raise RuntimeError(f"AP0 mid semantics mismatch: {rel}")

            table = pf.read(columns=READ_COLUMNS, use_threads=False)
            minute = table["minute_start_ms_utc"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            seg = table["segment_id"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.int64, copy=False)
            op = table["mid_open"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            hi = table["mid_high"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            lo = table["mid_low"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)
            cl = table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

            n = minute.size
            if n != int(rec["rows"]) or n == 0:
                raise RuntimeError(f"Decoded row mismatch/empty: {rel}")
            if np.any(np.diff(minute) <= 0):
                raise RuntimeError(f"Minute order violation: {rel}")
            if previous_minute is not None and int(minute[0]) <= previous_minute:
                raise RuntimeError(f"Global minute order violation: {rel}")
            if np.any(np.diff(seg) < 0) or np.any(np.diff(seg) > 1):
                raise RuntimeError(f"Segment order violation: {rel}")
            if previous_segment is not None and int(seg[0]) - previous_segment not in (0,1):
                raise RuntimeError(f"Segment boundary violation: {rel}")
            if not (np.all(np.isfinite(op)) and np.all(np.isfinite(hi)) and np.all(np.isfinite(lo)) and np.all(np.isfinite(cl))):
                raise RuntimeError(f"Nonfinite OHLC: {rel}")
            if np.any(op <= 0) or np.any(hi <= 0) or np.any(lo <= 0) or np.any(cl <= 0):
                raise RuntimeError(f"Nonpositive OHLC: {rel}")
            if np.any(lo > op) or np.any(lo > cl) or np.any(hi < op) or np.any(hi < cl):
                raise RuntimeError(f"OHLC invariant violation: {rel}")

            minute_chunks.append(minute.copy())
            seg_chunks.append(seg.copy())
            open_chunks.append(op.copy())
            high_chunks.append(hi.copy())
            low_chunks.append(lo.copy())
            close_chunks.append(cl.copy())
            rows += n
            previous_minute = int(minute[-1])
            previous_segment = int(seg[-1])

        if rows != EXPECTED_MINUTES or previous_segment != EXPECTED_SEGMENTS - 1:
            raise RuntimeError("AP2 reconstructed coverage mismatch.")

        minute = np.concatenate(minute_chunks)
        seg = np.concatenate(seg_chunks)
        op = np.concatenate(open_chunks)
        hi = np.concatenate(high_chunks)
        lo = np.concatenate(low_chunks)
        cl = np.concatenate(close_chunks)
        n = minute.size

        metrics = {}
        metrics["minute_range_bps"] = (hi - lo) / op * 10000.0

        valid_counts = {}
        signed_1m_log = np.full(n, np.nan, dtype=np.float64)
        for h in HORIZONS:
            values = np.full(n, np.nan, dtype=np.float64)
            valid = (
                (seg[h:] == seg[:-h]) &
                ((minute[h:] - minute[:-h]) == h * 60_000)
            )
            target = np.flatnonzero(valid) + h
            logret = np.log(cl[h:][valid] / cl[:-h][valid])
            values[target] = np.abs(logret) * 10000.0
            metrics[f"abs_log_return_{h}m_bps"] = values
            valid_counts[f"abs_log_return_{h}m"] = int(target.size)
            if h == 1:
                signed_1m_log[target] = logret

        finite_1m = np.isfinite(signed_1m_log)
        sq = np.where(finite_1m, signed_1m_log * signed_1m_log, 0.0)
        invalid = (~finite_1m).astype(np.int64)
        cs_sq = np.concatenate(([0.0], np.cumsum(sq, dtype=np.float64)))
        cs_invalid = np.concatenate(([0], np.cumsum(invalid, dtype=np.int64)))

        for h in RV_HORIZONS:
            values = np.full(n, np.nan, dtype=np.float64)
            endpoints = np.arange(h, n, dtype=np.int64)
            starts = endpoints - h + 1
            bad = cs_invalid[endpoints + 1] - cs_invalid[starts]
            sums = cs_sq[endpoints + 1] - cs_sq[starts]
            boundary_ok = (
                (seg[endpoints] == seg[endpoints - h]) &
                ((minute[endpoints] - minute[endpoints - h]) == h * 60_000)
            )
            ok = (bad == 0) & boundary_ok
            target = endpoints[ok]
            values[target] = np.sqrt(sums[ok]) * 10000.0
            metrics[f"realized_vol_{h}m_bps"] = values
            valid_counts[f"realized_vol_{h}m"] = int(target.size)

        utc_hour_code = minute // 3_600_000
        unique_hours, inverse = np.unique(utc_hour_code, return_inverse=True)
        ny_hour_map = np.empty(unique_hours.size, dtype=np.int16)
        year_map = np.empty(unique_hours.size, dtype=np.int16)
        for i, code in enumerate(unique_hours):
            dt = datetime.fromtimestamp(int(code) * 3600, tz=timezone.utc)
            ny_hour_map[i] = dt.astimezone(NY).hour
            year_map[i] = dt.year
        ny_hour = ny_hour_map[inverse]
        utc_year = year_map[inverse]

        global_metrics = {name: metric_summary(v) for name, v in metrics.items()}

        ny_buckets = []
        for hour in range(24):
            mask = ny_hour == hour
            ny_buckets.append({
                "code": hour,
                "label": f"{hour:02d}:00 America/New_York",
                "minute_count": int(np.count_nonzero(mask)),
                "metrics": bucket_summary(mask, metrics),
            })

        year_buckets = []
        for year in range(2021, 2027):
            mask = utc_year == year
            year_buckets.append({
                "code": year,
                "label": f"{year} UTC-year",
                "partial_period": year in (2021, 2026),
                "minute_count": int(np.count_nonzero(mask)),
                "metrics": bucket_summary(mask, metrics),
            })

        if sum(x["minute_count"] for x in ny_buckets) != EXPECTED_MINUTES:
            raise RuntimeError("NY-hour minute conservation failed.")
        if sum(x["minute_count"] for x in year_buckets) != EXPECTED_MINUTES:
            raise RuntimeError("Year minute conservation failed.")

        payload = {
            "schema": "ATDS_AP2_VOLATILITY_MAP_V0_1",
            "status": "AP2_COMPLETE",
            "input_identity": EXPECTED_AP0_IDENTITY,
            "binding": {
                "ap0_manifest_sha256": EXPECTED_AP0_MANIFEST_SHA256,
                "ap1_sha256": EXPECTED_AP1_SHA256,
                "ap0_files_rehashed": EXPECTED_FILES,
            },
            "scope": {
                "strategy_agnostic": True,
                "backward_looking_only": True,
                "future_labels": False,
                "signals_calculated": False,
                "pnl_calculated": False,
                "source_volume_used": False,
            },
            "coverage": {
                "minute_rows": int(n),
                "segments": EXPECTED_SEGMENTS,
                "valid_counts": valid_counts,
                "first_minute_ms_utc": int(minute[0]),
                "last_minute_ms_utc": int(minute[-1]),
            },
            "metric_contract": {
                "minute_range_bps": "(mid_high-mid_low)/mid_open*10000",
                "abs_log_return_bps": "abs(log(close_t/close_t-H))*10000",
                "realized_vol_bps": "sqrt(sum(valid_1m_log_return^2))*10000",
                "horizons_minutes": list(HORIZONS),
                "realized_vol_horizons_minutes": list(RV_HORIZONS),
                "window_requires_same_segment": True,
                "window_requires_exact_minute_contiguity": True,
                "percentile_method": "linear",
                "percentiles": [50,90,95,99,99.9],
                "optimization": False,
            },
            "global": global_metrics,
            "new_york_hour": ny_buckets,
            "utc_year": year_buckets,
            "runtime": {
                "numpy_version": np.__version__,
                "pyarrow_version": pa.__version__,
            },
        }

        write_json(output, payload)
        print("AP2_COMPLETE")
        print(f"Minute rows: {n}")
        for k,v in valid_counts.items():
            print(f"{k}: {v}")
        print(f"Global 1m abs return mean bps: {global_metrics['abs_log_return_1m_bps']['mean']}")
        print(f"Global 60m realized vol mean bps: {global_metrics['realized_vol_60m_bps']['mean']}")
        print(f"Report: {output}")
        return 0

    except Exception as exc:
        return block("BLOCKED_AP2_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
