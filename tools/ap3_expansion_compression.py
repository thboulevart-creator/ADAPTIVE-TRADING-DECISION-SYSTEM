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
EXPECTED_AP2_SHA256 = "4e3c79a5b9c8131f62a8fb7f205712d8a5c4301ff01b7fd3ce7226d8799d9c9f"
EXPECTED_AP0_IDENTITY = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_FILES = 61
EXPECTED_MINUTES = 1_709_180
EXPECTED_SOURCE_TICKS = 376_003_618
EXPECTED_SEGMENTS = 1_606
RECONCILIATION_TOLERANCE = 1e-9
VARIANCE_SHARE_TOLERANCE = 1e-9
MAX_OUTPUT_BYTES = 32 * 1024 * 1024
NY = ZoneInfo("America/New_York")
STATES = ("COMPRESSION", "NORMAL", "EXPANSION")

READ_COLUMNS = ["minute_start_ms_utc", "segment_id", "mid_close"]
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
        raise RuntimeError("AP3 output exceeds 32 MiB.")
    path.write_bytes(raw)


def distribution_summary(values):
    import numpy as np
    x = values[np.isfinite(values)]
    if x.size == 0:
        return {
            "count": 0, "mean": None, "p20": None, "p50": None,
            "p80": None, "p90": None, "p95": None, "p99": None,
            "p99_9": None, "max": None,
        }
    return {
        "count": int(x.size),
        "mean": float(np.mean(x)),
        "p20": float(np.percentile(x, 20, method="linear")),
        "p50": float(np.percentile(x, 50, method="linear")),
        "p80": float(np.percentile(x, 80, method="linear")),
        "p90": float(np.percentile(x, 90, method="linear")),
        "p95": float(np.percentile(x, 95, method="linear")),
        "p99": float(np.percentile(x, 99, method="linear")),
        "p99_9": float(np.percentile(x, 99.9, method="linear")),
        "max": float(np.max(x)),
    }


def ap2_reconciliation_summary(values):
    import numpy as np
    x = values[np.isfinite(values)]
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


def check_reconciliation(observed: dict, expected: dict, label: str) -> None:
    if observed["count"] != expected["count"]:
        raise RuntimeError(f"{label} count mismatch: {observed['count']} != {expected['count']}")
    for key in ("mean", "p50", "p90", "p95", "p99", "p99_9", "max"):
        if abs(float(observed[key]) - float(expected[key])) > RECONCILIATION_TOLERANCE:
            raise RuntimeError(
                f"{label} {key} mismatch: {observed[key]} != {expected[key]}"
            )


def classify(values, lower: float, upper: float):
    import numpy as np
    out = np.full(values.size, -1, dtype=np.int8)
    valid = np.isfinite(values)
    out[valid & (values <= lower)] = 0
    out[valid & (values > lower) & (values < upper)] = 1
    out[valid & (values >= upper)] = 2
    return out


def state_counts(state):
    import numpy as np
    valid = state >= 0
    total = int(np.count_nonzero(valid))
    counts = [int(np.count_nonzero(state == i)) for i in range(3)]
    return {
        "valid_count": total,
        "states": {
            STATES[i]: {
                "count": counts[i],
                "share": (counts[i] / total) if total else None,
            }
            for i in range(3)
        },
    }


def duration_summary(x):
    import numpy as np
    if x.size == 0:
        return {
            "phase_count": 0, "mean_minutes": None, "p50_minutes": None,
            "p90_minutes": None, "p99_minutes": None, "max_minutes": None,
        }
    return {
        "phase_count": int(x.size),
        "mean_minutes": float(np.mean(x)),
        "p50_minutes": float(np.percentile(x, 50, method="linear")),
        "p90_minutes": float(np.percentile(x, 90, method="linear")),
        "p99_minutes": float(np.percentile(x, 99, method="linear")),
        "max_minutes": int(np.max(x)),
    }


def phase_stats(state, minute, segment):
    import numpy as np
    valid = state >= 0
    continuation = (
        valid[1:] &
        valid[:-1] &
        (state[1:] == state[:-1]) &
        (segment[1:] == segment[:-1]) &
        ((minute[1:] - minute[:-1]) == 60_000)
    )
    start_mask = valid.copy()
    end_mask = valid.copy()
    start_mask[1:] &= ~continuation
    end_mask[:-1] &= ~continuation
    starts = np.flatnonzero(start_mask)
    ends = np.flatnonzero(end_mask)
    if starts.size != ends.size:
        raise RuntimeError("Phase boundary count mismatch.")
    if starts.size and np.any(ends < starts):
        raise RuntimeError("Phase end precedes phase start.")
    durations = ends - starts + 1
    run_states = state[starts]
    result = {}
    for i, name in enumerate(STATES):
        result[name] = duration_summary(durations[run_states == i])
    result["all_phase_count"] = int(starts.size)
    result["duration_sum_minutes"] = int(np.sum(durations, dtype=np.int64))
    result["valid_state_minutes"] = int(np.count_nonzero(valid))
    if result["duration_sum_minutes"] != result["valid_state_minutes"]:
        raise RuntimeError("Phase duration conservation failed.")
    return result


def transition_stats(state, minute, segment):
    import numpy as np
    valid_pair = (
        (state[:-1] >= 0) &
        (state[1:] >= 0) &
        (segment[:-1] == segment[1:]) &
        ((minute[1:] - minute[:-1]) == 60_000)
    )
    src = state[:-1][valid_pair]
    dst = state[1:][valid_pair]
    matrix = np.zeros((3, 3), dtype=np.int64)
    np.add.at(matrix, (src, dst), 1)
    probabilities = []
    for i in range(3):
        total = int(matrix[i].sum())
        probabilities.append([
            (float(matrix[i, j] / total) if total else None)
            for j in range(3)
        ])
    return {
        "state_order": list(STATES),
        "valid_transition_count": int(np.count_nonzero(valid_pair)),
        "counts": matrix.tolist(),
        "conditional_probabilities_by_source": probabilities,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="AP3 descriptive expansion/compression census.")
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--ap0-manifest", required=True)
    ap.add_argument("--ap2-report", required=True)
    ap.add_argument(
        "--output",
        default=str(Path(tempfile.gettempdir()) / "ATDS-AP3-EXPANSION-COMPRESSION.json"),
    )
    args = ap.parse_args()

    root = Path(args.ap0_root).expanduser().resolve(strict=False)
    manifest_path = Path(args.ap0_manifest).expanduser().resolve(strict=False)
    ap2_path = Path(args.ap2_report).expanduser().resolve(strict=False)
    output = Path(args.output).expanduser().resolve(strict=False)

    def block(code: str, reason: str) -> int:
        try:
            write_json(output, {"schema":"ATDS_AP3_BLOCKED_V0_1","status":code,"reason":reason})
        except Exception:
            pass
        print(code)
        print(reason)
        print(f"Report: {output}")
        return 2

    if not root.is_dir():
        return block("BLOCKED_AP3_ROOT_NOT_FOUND", str(root))
    if not manifest_path.is_file() or not ap2_path.is_file():
        return block("BLOCKED_AP3_INPUT_NOT_FOUND", "AP0 manifest or AP2 report missing.")
    if sha256_path(manifest_path) != EXPECTED_AP0_MANIFEST_SHA256:
        return block("BLOCKED_AP3_AP0_MANIFEST_SHA", "AP0 manifest SHA mismatch.")
    if sha256_path(ap2_path) != EXPECTED_AP2_SHA256:
        return block("BLOCKED_AP3_AP2_SHA", "AP2 report SHA mismatch.")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        ap2 = json.loads(ap2_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return block("BLOCKED_AP3_JSON_PARSE", str(exc))

    if manifest.get("status") != "AP0_COMPLETE" or manifest.get("output_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP3_AP0_CONTRACT", "AP0 identity/status mismatch.")
    files = manifest.get("files")
    cov = manifest.get("coverage") or {}
    if not isinstance(files, list) or len(files) != EXPECTED_FILES:
        return block("BLOCKED_AP3_AP0_CONTRACT", "AP0 file count mismatch.")
    if cov.get("minute_rows_written") != EXPECTED_MINUTES or cov.get("source_ticks_read") != EXPECTED_SOURCE_TICKS:
        return block("BLOCKED_AP3_AP0_CONTRACT", "AP0 coverage mismatch.")
    if cov.get("segments") != EXPECTED_SEGMENTS:
        return block("BLOCKED_AP3_AP0_CONTRACT", "AP0 segment count mismatch.")

    if ap2.get("status") != "AP2_COMPLETE" or ap2.get("input_identity") != EXPECTED_AP0_IDENTITY:
        return block("BLOCKED_AP3_AP2_CONTRACT", "AP2 status/input mismatch.")
    ap2cov = ap2.get("coverage") or {}
    if ap2cov.get("minute_rows") != EXPECTED_MINUTES or ap2cov.get("segments") != EXPECTED_SEGMENTS:
        return block("BLOCKED_AP3_AP2_CONTRACT", "AP2 coverage mismatch.")
    scope = ap2.get("scope") or {}
    if scope.get("strategy_agnostic") is not True or scope.get("backward_looking_only") is not True:
        return block("BLOCKED_AP3_AP2_CONTRACT", "AP2 epistemic scope mismatch.")

    try:
        import numpy as np
        import pyarrow as pa
        import pyarrow.parquet as pq
    except Exception as exc:
        return block("BLOCKED_AP3_RUNTIME_DEPENDENCY", str(exc))

    minute_chunks, seg_chunks, close_chunks = [], [], []
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
            close = table["mid_close"].combine_chunks().to_numpy(zero_copy_only=False).astype(np.float64, copy=False)

            n = minute.size
            if n != int(rec["rows"]) or n == 0:
                raise RuntimeError(f"Decoded row mismatch/empty: {rel}")
            if np.any(np.diff(minute) <= 0):
                raise RuntimeError(f"Minute order violation: {rel}")
            if previous_minute is not None and int(minute[0]) <= previous_minute:
                raise RuntimeError(f"Global minute order violation: {rel}")
            dseg = np.diff(seg)
            if np.any(dseg < 0) or np.any(dseg > 1):
                raise RuntimeError(f"Segment order violation: {rel}")
            if previous_segment is not None and int(seg[0]) - previous_segment not in (0,1):
                raise RuntimeError(f"Segment boundary violation: {rel}")
            if not np.all(np.isfinite(close)) or np.any(close <= 0):
                raise RuntimeError(f"Invalid mid_close: {rel}")

            minute_chunks.append(minute.copy())
            seg_chunks.append(seg.copy())
            close_chunks.append(close.copy())
            rows += n
            previous_minute = int(minute[-1])
            previous_segment = int(seg[-1])

        if rows != EXPECTED_MINUTES or previous_segment != EXPECTED_SEGMENTS - 1:
            raise RuntimeError("AP3 reconstructed coverage mismatch.")

        minute = np.concatenate(minute_chunks)
        seg = np.concatenate(seg_chunks)
        close = np.concatenate(close_chunks)
        n = minute.size

        signed_1m_log = np.full(n, np.nan, dtype=np.float64)
        valid_1m = (
            (seg[1:] == seg[:-1]) &
            ((minute[1:] - minute[:-1]) == 60_000)
        )
        target_1m = np.flatnonzero(valid_1m) + 1
        signed_1m_log[target_1m] = np.log(close[1:][valid_1m] / close[:-1][valid_1m])

        finite_1m = np.isfinite(signed_1m_log)
        sq = np.where(finite_1m, signed_1m_log * signed_1m_log, 0.0)
        invalid = (~finite_1m).astype(np.int64)
        cs_sq = np.concatenate(([0.0], np.cumsum(sq, dtype=np.float64)))
        cs_invalid = np.concatenate(([0], np.cumsum(invalid, dtype=np.int64)))

        def realized_vol(h: int):
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
            tgt = endpoints[ok]
            values[tgt] = np.sqrt(sums[ok]) * 10000.0
            return values

        rv15 = realized_vol(15)
        rv60 = realized_vol(60)

        observed_rv15 = ap2_reconciliation_summary(rv15)
        observed_rv60 = ap2_reconciliation_summary(rv60)
        check_reconciliation(
            observed_rv15,
            ap2["global"]["realized_vol_15m_bps"],
            "RV15",
        )
        check_reconciliation(
            observed_rv60,
            ap2["global"]["realized_vol_60m_bps"],
            "RV60",
        )

        rv15_dist = distribution_summary(rv15)
        abs_lower = float(rv15_dist["p20"])
        abs_upper = float(rv15_dist["p80"])
        absolute_state = classify(rv15, abs_lower, abs_upper)

        hour_code = minute // 3_600_000
        unique_hours, inverse = np.unique(hour_code, return_inverse=True)
        ny_hour_map = np.empty(unique_hours.size, dtype=np.int16)
        year_map = np.empty(unique_hours.size, dtype=np.int16)
        for i, code in enumerate(unique_hours):
            dt = datetime.fromtimestamp(int(code) * 3600, tz=timezone.utc)
            ny_hour_map[i] = dt.astimezone(NY).hour
            year_map[i] = dt.year
        ny_hour = ny_hour_map[inverse]
        utc_year = year_map[inverse]

        hour_baselines = []
        median_by_hour = np.full(24, np.nan, dtype=np.float64)
        for hour in range(24):
            mask = (ny_hour == hour) & np.isfinite(rv15)
            vals = rv15[mask]
            median = float(np.percentile(vals, 50, method="linear")) if vals.size else None
            if median is not None:
                if median <= 0:
                    raise RuntimeError(f"Nonpositive RV15 hourly median at hour {hour}.")
                median_by_hour[hour] = median
            hour_baselines.append({
                "hour": hour,
                "label": f"{hour:02d}:00 America/New_York",
                "valid_count": int(vals.size),
                "rv15_median_bps": median,
            })

        normalized = np.full(n, np.nan, dtype=np.float64)
        finite_rv15 = np.isfinite(rv15)
        baselines = median_by_hour[ny_hour]
        valid_norm = finite_rv15 & np.isfinite(baselines) & (baselines > 0)
        normalized[valid_norm] = rv15[valid_norm] / baselines[valid_norm]

        norm_dist = distribution_summary(normalized)
        norm_lower = float(norm_dist["p20"])
        norm_upper = float(norm_dist["p80"])
        normalized_state = classify(normalized, norm_lower, norm_upper)

        absolute_counts = state_counts(absolute_state)
        normalized_counts = state_counts(normalized_state)

        absolute_phases = phase_stats(absolute_state, minute, seg)
        normalized_phases = phase_stats(normalized_state, minute, seg)
        absolute_transitions = transition_stats(absolute_state, minute, seg)
        normalized_transitions = transition_stats(normalized_state, minute, seg)

        year_shares = []
        for year in range(2021, 2027):
            mask = utc_year == year
            st = normalized_state[mask]
            counts = state_counts(st)
            year_shares.append({
                "year": year,
                "partial_period": year in (2021, 2026),
                "minute_rows": int(np.count_nonzero(mask)),
                **counts,
            })

        share = np.full(n, np.nan, dtype=np.float64)
        both = np.isfinite(rv15) & np.isfinite(rv60) & (rv60 > 0)
        share[both] = (rv15[both] / rv60[both]) ** 2
        finite_share = share[np.isfinite(share)]
        if finite_share.size:
            if float(np.min(finite_share)) < -VARIANCE_SHARE_TOLERANCE:
                raise RuntimeError("Negative variance share beyond tolerance.")
            if float(np.max(finite_share)) > 1.0 + VARIANCE_SHARE_TOLERANCE:
                raise RuntimeError("Variance share exceeds one beyond tolerance.")
            share[both] = np.clip(share[both], 0.0, 1.0)

        share_global = distribution_summary(share)
        share_by_normalized_state = {}
        for i, name in enumerate(STATES):
            vals = np.where(normalized_state == i, share, np.nan)
            share_by_normalized_state[name] = distribution_summary(vals)

        output_payload = {
            "schema": "ATDS_AP3_EXPANSION_COMPRESSION_V0_1",
            "status": "AP3_COMPLETE",
            "input_identity": EXPECTED_AP0_IDENTITY,
            "binding": {
                "ap0_manifest_sha256": EXPECTED_AP0_MANIFEST_SHA256,
                "ap2_sha256": EXPECTED_AP2_SHA256,
                "ap0_files_rehashed": EXPECTED_FILES,
            },
            "scope": {
                "strategy_agnostic": True,
                "causal_deployable": False,
                "full_sample_descriptive_thresholds": True,
                "future_labels": False,
                "signals_calculated": False,
                "pnl_calculated": False,
                "source_volume_used": False,
            },
            "coverage": {
                "minute_rows": int(n),
                "segments": EXPECTED_SEGMENTS,
                "rv15_valid_count": int(np.count_nonzero(np.isfinite(rv15))),
                "rv60_valid_count": int(np.count_nonzero(np.isfinite(rv60))),
                "normalized_rv15_valid_count": int(np.count_nonzero(np.isfinite(normalized))),
                "variance_share_valid_count": int(np.count_nonzero(np.isfinite(share))),
                "variance_share_zero_rv60_excluded": int(np.count_nonzero(np.isfinite(rv15) & np.isfinite(rv60) & (rv60 <= 0))),
            },
            "reconciliation": {
                "tolerance": RECONCILIATION_TOLERANCE,
                "rv15_observed": observed_rv15,
                "rv15_ap2": ap2["global"]["realized_vol_15m_bps"],
                "rv60_observed": observed_rv60,
                "rv60_ap2": ap2["global"]["realized_vol_60m_bps"],
            },
            "metric_contract": {
                "rv15_bps": "sqrt(sum(last 15 valid 1m log returns squared))*10000",
                "rv60_bps": "sqrt(sum(last 60 valid 1m log returns squared))*10000",
                "absolute_state_thresholds": "full-sample RV15 p20/p80",
                "intraday_baseline": "full-sample median RV15 by America/New_York hour",
                "normalized_rv15": "RV15 / median_RV15_of_same_New_York_hour",
                "normalized_state_thresholds": "full-sample normalized_RV15 p20/p80",
                "compression_rule": "value <= p20",
                "normal_rule": "p20 < value < p80",
                "expansion_rule": "value >= p80",
                "variance_share_15_of_60": "RV15^2 / RV60^2",
                "percentile_method": "linear",
                "optimization": False,
            },
            "absolute_lens": {
                "rv15_distribution": rv15_dist,
                "thresholds": {
                    "compression_max_bps": abs_lower,
                    "expansion_min_bps": abs_upper,
                },
                "state_counts": absolute_counts,
                "phase_durations": absolute_phases,
                "transitions": absolute_transitions,
            },
            "intraday_normalized_lens": {
                "hourly_rv15_medians": hour_baselines,
                "normalized_distribution": norm_dist,
                "thresholds": {
                    "compression_max_ratio": norm_lower,
                    "expansion_min_ratio": norm_upper,
                },
                "state_counts": normalized_counts,
                "phase_durations": normalized_phases,
                "transitions": normalized_transitions,
                "utc_year_state_shares": year_shares,
            },
            "variance_concentration": {
                "global": share_global,
                "by_intraday_normalized_state": share_by_normalized_state,
            },
            "runtime": {
                "numpy_version": np.__version__,
                "pyarrow_version": pa.__version__,
            },
        }

        write_json(output, output_payload)
        print("AP3_COMPLETE")
        print(f"Minute rows: {n}")
        print(f"RV15 valid: {output_payload['coverage']['rv15_valid_count']}")
        print(f"RV60 valid: {output_payload['coverage']['rv60_valid_count']}")
        print(f"Absolute thresholds p20/p80 bps: {abs_lower} / {abs_upper}")
        print(f"Normalized thresholds p20/p80: {norm_lower} / {norm_upper}")
        print(f"Variance share valid: {output_payload['coverage']['variance_share_valid_count']}")
        print(f"Report: {output}")
        return 0

    except Exception as exc:
        return block("BLOCKED_AP3_RUNTIME", str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
