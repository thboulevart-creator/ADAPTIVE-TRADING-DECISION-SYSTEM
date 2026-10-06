#!/usr/bin/env python3
"""BEPD-07B deterministic real global behavioral excursion runner.

Scientific scope is frozen by BEPD-07A:
- population: all 472 qualified BEPD-02 sweep events, no filtering;
- anchor: take_h1_close_mid;
- path: first AP0 minute strictly after take_h1_close_utc through the
  same canonical target-week end (exclusive);
- extrema: observed AP0 mid_high / mid_low only;
- outputs: two separate descriptive global distributions only.

No event-level derived excursion ledger is persisted.
No subgroup, joint metric, trade, PnL, prediction or OOS logic exists here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timedelta, time, timezone
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from bisect import bisect_left, bisect_right
from pathlib import Path
from zoneinfo import ZoneInfo

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")
ZERO = Decimal(0)
NY = ZoneInfo("America/New_York")
EXPECTED_DATASET = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
EXPECTED_FILE_SET_DIGEST = "1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a"
EXPECTED_FILE_COUNT = 61
EXPECTED_AP0_ROWS = 1709180

PROBS = [
    ("P01", Decimal("0.01")),
    ("P05", Decimal("0.05")),
    ("P10", Decimal("0.10")),
    ("P25", Decimal("0.25")),
    ("P50", Decimal("0.50")),
    ("P75", Decimal("0.75")),
    ("P90", Decimal("0.90")),
    ("P95", Decimal("0.95")),
    ("P99", Decimal("0.99")),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_sha256(obj) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def data02_file_set_digest(files: list[dict]) -> str:
    """Canonical DATA-02 file-set identity: ordered manifest records with size+SHA."""
    material = [
        {
            "relative_path": entry["relative_path"],
            "size_bytes": int(entry["size_bytes"]),
            "sha256": entry["sha256"],
        }
        for entry in files
    ]
    raw = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def q18(x: Decimal) -> str:
    return format(x.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def frac(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def parse_utc_ms(ts: str) -> int:
    if not isinstance(ts, str) or not ts:
        raise ValueError("missing UTC timestamp")
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timestamp must be timezone aware")
    if dt.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp must be UTC")
    return int(dt.timestamp() * 1000)


def target_week_bounds_ms(target_week_id: str) -> tuple[int, int]:
    monday = datetime.strptime(target_week_id, "%Y-%m-%d").date()
    sunday = monday - timedelta(days=1)
    start_local = datetime.combine(sunday, time(18, 0), tzinfo=NY)
    end_local = start_local + timedelta(days=7)
    start_ms = int(start_local.astimezone(timezone.utc).timestamp() * 1000)
    end_ms = int(end_local.astimezone(timezone.utc).timestamp() * 1000)
    return start_ms, end_ms


def type7(values: list[Decimal], p: Decimal) -> Decimal:
    if not values:
        raise ValueError("empty surface")
    ordered = sorted(values)
    n = len(ordered)
    if n == 1:
        return ordered[0]
    h = Decimal(1) + Decimal(n - 1) * p
    j = int(h)
    g = h - Decimal(j)
    if j >= n:
        return ordered[-1]
    return ordered[j - 1] + g * (ordered[j] - ordered[j - 1])


def metric_surface(values: list[Decimal]) -> dict:
    if not values:
        raise ValueError("empty metric population")
    if any(v < ZERO for v in values):
        raise ValueError("negative excursion")
    ordered = sorted(values)
    n = len(ordered)
    qs = {name: q18(type7(ordered, p)) for name, p in PROBS}
    zero_count = sum(1 for v in ordered if v == ZERO)

    support_counts: dict[Decimal, int] = {}
    for v in ordered:
        support_counts[v] = support_counts.get(v, 0) + 1

    cumulative = 0
    ecdf = []
    for support in sorted(support_counts):
        count = support_counts[support]
        cumulative += count
        ecdf.append({
            "support_value": q18(support),
            "support_count": count,
            "cumulative_count": cumulative,
            "cumulative_fraction": frac(cumulative, n),
            "cumulative_decimal": q18(Decimal(cumulative) / Decimal(n)),
        })

    out = {
        "N": n,
        "MINIMUM": q18(ordered[0]),
        "MAXIMUM": q18(ordered[-1]),
        "MEAN": q18(sum(ordered, ZERO) / Decimal(n)),
        "MEDIAN": qs["P50"],
        **qs,
        "ZERO_COUNT": zero_count,
        "ZERO_FRACTION": frac(zero_count, n),
        "ZERO_FRACTION_DECIMAL": q18(Decimal(zero_count) / Decimal(n)),
        "EMPIRICAL_CDF": ecdf,
    }
    if out["P50"] != out["MEDIAN"]:
        raise AssertionError("P50 != MEDIAN")
    if ecdf[-1]["cumulative_count"] != n or ecdf[-1]["cumulative_fraction"] != "1":
        raise AssertionError("ECDF terminal state mismatch")
    return out


def compute_excursions(side: str, anchor, highs, lows) -> tuple[Decimal, Decimal]:
    a = Decimal(str(anchor))
    hi = Decimal(str(max(highs)))
    lo = Decimal(str(min(lows)))
    if side == "HIGH":
        reintegrative = max(ZERO, a - lo)
        external = max(ZERO, hi - a)
    elif side == "LOW":
        reintegrative = max(ZERO, hi - a)
        external = max(ZERO, a - lo)
    else:
        raise ValueError(f"invalid side: {side}")
    if reintegrative < ZERO or external < ZERO:
        raise AssertionError("negative excursion")
    return reintegrative, external


def verify_manifest_and_files(ap0_root: Path, expected_manifest_sha256: str, expected_file_set_digest: str):
    manifest_path = ap0_root / "AP0-MANIFEST.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)
    observed_manifest_sha = sha256_file(manifest_path)
    if observed_manifest_sha != expected_manifest_sha256:
        raise ValueError(f"AP0 manifest SHA mismatch: {observed_manifest_sha}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("output_identity") != EXPECTED_DATASET:
        raise ValueError("AP0 dataset identity mismatch")
    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != EXPECTED_FILE_COUNT:
        raise ValueError("AP0 file count mismatch")
    if manifest.get("coverage", {}).get("minute_rows_written") != EXPECTED_AP0_ROWS:
        raise ValueError("AP0 row count mismatch")

    verified = []
    for entry in files:
        rel = entry["relative_path"]
        expected = entry["sha256"]
        p = ap0_root / Path(rel)
        if not p.is_file():
            raise FileNotFoundError(p)
        actual = sha256_file(p)
        if actual != expected:
            raise ValueError(f"AP0 file SHA mismatch: {rel}")
        if p.stat().st_size != int(entry["size_bytes"]):
            raise ValueError(f"AP0 file size mismatch: {rel}")
        verified.append({
            "relative_path": rel,
            "sha256": expected,
            "size_bytes": int(entry["size_bytes"]),
            "first_minute_ms_utc": int(entry["first_minute_ms_utc"]),
            "last_minute_ms_utc": int(entry["last_minute_ms_utc"]),
            "rows": int(entry["rows"]),
        })
    file_set_digest = data02_file_set_digest(files)
    if file_set_digest != expected_file_set_digest:
        raise ValueError(f"AP0 file-set digest mismatch: {file_set_digest}")
    return manifest, verified, observed_manifest_sha, file_set_digest


def load_ap0_arrays(ap0_root: Path, files: list[dict]):
    import numpy as np
    import pyarrow.parquet as pq

    ts_parts = []
    hi_parts = []
    lo_parts = []
    for entry in files:
        p = ap0_root / Path(entry["relative_path"])
        table = pq.read_table(p, columns=["minute_start_ms_utc", "mid_high", "mid_low"])
        if table.num_rows != entry["rows"]:
            raise ValueError(f"row count drift: {entry['relative_path']}")
        ts_parts.append(table.column("minute_start_ms_utc").to_numpy(zero_copy_only=False))
        hi_parts.append(table.column("mid_high").to_numpy(zero_copy_only=False))
        lo_parts.append(table.column("mid_low").to_numpy(zero_copy_only=False))

    ts = np.concatenate(ts_parts)
    highs = np.concatenate(hi_parts)
    lows = np.concatenate(lo_parts)
    if len(ts) != EXPECTED_AP0_ROWS:
        raise ValueError("concatenated AP0 row count mismatch")
    if not np.all(np.diff(ts) > 0):
        raise ValueError("AP0 minute ordering is not strictly increasing")
    if not np.isfinite(highs).all() or not np.isfinite(lows).all():
        raise ValueError("non-finite AP0 extrema")
    return ts, highs, lows


def path_slice_indices(ts, start_exclusive_ms: int, end_exclusive_ms: int) -> tuple[int, int]:
    """Return [lo, hi) for timestamps strictly after start and strictly before end."""
    return bisect_right(ts, start_exclusive_ms), bisect_left(ts, end_exclusive_ms)


def source_files_for_window(files: list[dict], start_exclusive_ms: int, end_exclusive_ms: int) -> list[str]:
    out = []
    for f in files:
        if f["last_minute_ms_utc"] > start_exclusive_ms and f["first_minute_ms_utc"] < end_exclusive_ms:
            out.append(f["relative_path"])
    return out


def scan_real(events: list[dict], ts, highs, lows, files: list[dict]) -> tuple[list[Decimal], list[Decimal], dict]:
    import numpy as np

    if len(events) != 472:
        raise ValueError(f"BASE_N mismatch: {len(events)}")
    event_ids = [e.get("event_id") for e in events]
    if len(set(event_ids)) != 472 or any(not isinstance(x, str) or not x for x in event_ids):
        raise ValueError("event_id uniqueness failure")

    reintegrative_values: list[Decimal] = []
    external_values: list[Decimal] = []
    diagnostic_rows = []

    for e in events:
        if e.get("dataset_id") != EXPECTED_DATASET:
            raise ValueError("event dataset identity mismatch")
        if e.get("dataset_manifest_sha256") != EXPECTED_MANIFEST_SHA256:
            raise ValueError("event manifest identity mismatch")
        side = e.get("side")
        anchor = e.get("take_h1_close_mid")
        if anchor is None:
            raise ValueError("null take_h1_close_mid")
        t0 = parse_utc_ms(e.get("take_h1_close_utc"))
        week_start, week_end = target_week_bounds_ms(e.get("target_week_id"))
        if not (week_start <= t0 < week_end):
            raise ValueError("take confirmation outside target week")

        lo_idx, hi_idx = path_slice_indices(ts, t0, week_end)
        if hi_idx <= lo_idx:
            raise ValueError(f"EMPTY_PATH:{e['event_id']}")

        path_ts = ts[lo_idx:hi_idx]
        path_high = highs[lo_idx:hi_idx]
        path_low = lows[lo_idx:hi_idx]
        if int(path_ts[0]) <= t0:
            raise AssertionError("strict post-take start violated")
        if int(path_ts[-1]) >= week_end:
            raise AssertionError("target-week end violated")

        reintegrative, external = compute_excursions(side, anchor, path_high, path_low)
        reintegrative_values.append(reintegrative)
        external_values.append(external)

        diffs = np.diff(path_ts)
        gap_mask = diffs > 60000
        gap_count = int(gap_mask.sum())
        max_gap = int(diffs.max()) if len(diffs) else 0
        source_files = source_files_for_window(files, t0, week_end)
        if not source_files:
            raise ValueError("missing source file binding")

        diagnostic_rows.append({
            "event_id": e["event_id"],
            "path_observation_count": int(len(path_ts)),
            "path_first_observed_minute_ms_utc": int(path_ts[0]),
            "path_last_observed_minute_ms_utc": int(path_ts[-1]),
            "internal_gap_count_gt60s": gap_count,
            "max_observed_internal_gap_ms": max_gap,
            "source_file_paths": source_files,
        })

    counts = [x["path_observation_count"] for x in diagnostic_rows]
    gaps = [x["internal_gap_count_gt60s"] for x in diagnostic_rows]
    max_gaps = [x["max_observed_internal_gap_ms"] for x in diagnostic_rows]
    distinct_files = sorted({p for x in diagnostic_rows for p in x["source_file_paths"]})
    summary = {
        "PATH_EVENT_COUNT": len(diagnostic_rows),
        "EMPTY_PATH_EVENTS": 0,
        "FILTERED_EVENTS": 0,
        "DUPLICATE_EVENT_IDS": 0,
        "PATH_OBSERVATION_COUNT_MIN": min(counts),
        "PATH_OBSERVATION_COUNT_MAX": max(counts),
        "PATH_OBSERVATION_COUNT_SUM": sum(counts),
        "EVENTS_WITH_INTERNAL_GAP_GT60S": sum(1 for g in gaps if g > 0),
        "TOTAL_INTERNAL_GAP_COUNT_GT60S": sum(gaps),
        "MAX_OBSERVED_INTERNAL_GAP_MS": max(max_gaps),
        "SOURCE_FILE_BINDING_PASS_EVENTS": len(diagnostic_rows),
        "DISTINCT_SOURCE_FILES_USED": len(distinct_files),
        "DISTINCT_SOURCE_FILES_USED_DIGEST": canonical_sha256(distinct_files),
        "EVENT_LEVEL_PATH_DIAGNOSTICS_DIGEST": canonical_sha256(diagnostic_rows),
        "EVENT_LEVEL_PATH_DIAGNOSTICS_PERSISTED": False,
        "FORWARD_FILLED_VALUES": 0,
        "INTERPOLATED_VALUES": 0,
        "OUTCOME_DEPENDENT_ENDPOINTS": 0,
    }
    return reintegrative_values, external_values, summary


def load_events(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                raise ValueError(f"invalid EVENT_LEDGER JSONL line {n}: {exc}") from exc
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--event-ledger", required=True)
    ap.add_argument("--ap0-root", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--run-manifest", required=True)
    ap.add_argument("--diagnostics", required=True)
    ap.add_argument("--source-event-ledger-blob", required=True)
    ap.add_argument("--contract-blob", required=True)
    ap.add_argument("--breaker-blob", required=True)
    ap.add_argument("--freeze-blob", required=True)
    ap.add_argument("--runner-blob", required=True)
    ap.add_argument("--expected-manifest-sha256", default=EXPECTED_MANIFEST_SHA256)
    ap.add_argument("--expected-file-set-digest", default=EXPECTED_FILE_SET_DIGEST)
    args = ap.parse_args()

    ledger = Path(args.event_ledger)
    ap0_root = Path(args.ap0_root)
    events = load_events(ledger)
    manifest, files, manifest_sha, file_set_digest = verify_manifest_and_files(
        ap0_root, args.expected_manifest_sha256, args.expected_file_set_digest
    )
    ts, highs, lows = load_ap0_arrays(ap0_root, files)
    re_vals, ex_vals, diagnostics = scan_real(events, ts, highs, lows, files)

    if len(re_vals) != 472 or len(ex_vals) != 472:
        raise AssertionError("metric population mismatch")
    if any(v < ZERO for v in re_vals):
        raise AssertionError("negative reintegrative excursion")
    if any(v < ZERO for v in ex_vals):
        raise AssertionError("negative external excursion")

    metrics = {
        "MAX_REINTEGRATIVE_EXCURSION": metric_surface(re_vals),
        "MAX_EXTERNAL_EXCURSION": metric_surface(ex_vals),
    }
    for surface in metrics.values():
        if surface["N"] != 472:
            raise AssertionError("surface N != 472")

    bindings = {
        "source_event_ledger_blob": args.source_event_ledger_blob,
        "bepd07a_contract_blob": args.contract_blob,
        "bepd07a_breaker_blob": args.breaker_blob,
        "bepd07a_freeze_blob": args.freeze_blob,
        "runner_blob": args.runner_blob,
        "ap0_dataset_id": EXPECTED_DATASET,
        "ap0_manifest_sha256": manifest_sha,
        "ap0_file_set_digest": file_set_digest,
        "ap0_file_count": len(files),
        "ap0_row_count": int(manifest["coverage"]["minute_rows_written"]),
    }
    run_id = canonical_sha256(bindings)

    result = {
        "schema": "ATDS_BEPD_07B_FIRST_REAL_GLOBAL_BEHAVIORAL_EXCURSION_RESULT_V0_1",
        "control_id": "BEPD-07B",
        "run_id": run_id,
        "scope": "GLOBAL_ALL_472_QUALIFIED_SWEEP_EVENTS_NO_FILTERING",
        "price_surface": "MID_DESCRIPTIVE_ONLY",
        "mid_price_is_execution_price": False,
        "behavioral_excursion_is_trade_excursion": False,
        "evidence_status": "EXPOSED_EXPLORATORY_ONLY",
        "historical_corpus": "ALREADY_EXPOSED",
        "generalization": "NOT_ESTABLISHED",
        "confirmatory_generalization": "FRESH_OOS_EVIDENCE_REQUIRED",
        "prediction": False,
        "causation": "NOT_ESTABLISHED",
        "edge": False,
        "strategy_validation": False,
        "trading_authority": "NONE",
        "population": {
            "BASE_N": 472,
            "FILTERING": "NONE",
            "WEIGHTING": "ONE_EQUAL_WEIGHT_PER_QUALIFIED_EVENT",
            "subgroups": [],
        },
        "path_contract": {
            "anchor": "take_h1_close_mid",
            "event_confirmation_time": "take_h1_close_utc",
            "path_start": "FIRST_QUALIFIED_AP0_MINUTE_STRICTLY_AFTER_take_h1_close_utc",
            "path_end": "END_OF_SAME_CANONICAL_TARGET_WEEK",
            "session_week_start": "SUNDAY_18:00_America/New_York",
            "interval": "[target_week_start_utc,target_week_end_utc)",
            "extrema_primitives": ["mid_high", "mid_low"],
            "forward_fill": "FORBIDDEN",
            "backfill": "FORBIDDEN",
            "interpolation": "FORBIDDEN",
            "claim": "OBSERVED_EXTREMA_ONLY",
        },
        "dependence": {
            "event_is_iid_observation": False,
            "dependence_keys": ["target_week_id", "sweep_cluster_id"],
            "iid_standard_error": "FORBIDDEN",
            "iid_confidence_interval": "FORBIDDEN",
            "iid_bootstrap": "FORBIDDEN",
        },
        "numerical_contract": {
            "quantile_method": "HYNDMAN_FAN_TYPE_7",
            "p50_equals_median": True,
            "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
            "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
        },
        "metrics": metrics,
        "path_gap_diagnostics": diagnostics,
        "joint_excursion_metrics": "NOT_AUTHORIZED",
        "event_level_derived_path_ledger_persisted": False,
        "forbidden_analytics_executed": False,
        "bindings": bindings,
    }

    output = Path(args.output)
    run_manifest = Path(args.run_manifest)
    diagnostics_out = Path(args.diagnostics)
    for p in (output, run_manifest, diagnostics_out):
        p.parent.mkdir(parents=True, exist_ok=True)

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    diagnostics_out.write_text(json.dumps({
        "schema": "ATDS_BEPD_07B_PATH_GAP_QUALIFICATION_DIAGNOSTICS_V0_1",
        "control_id": "BEPD-07B",
        "run_id": run_id,
        "summary": diagnostics,
        "event_level_path_diagnostics_persisted": False,
        "price_surface": "MID_DESCRIPTIVE_ONLY",
        "claim": "OBSERVED_EXTREMA_ONLY",
    }, indent=2) + "\n", encoding="utf-8")

    manifest_obj = {
        "schema": "ATDS_BEPD_07B_RUN_MANIFEST_V0_1",
        "control_id": "BEPD-07B",
        "run_id": run_id,
        "event_ledger_path": str(ledger),
        "event_ledger_sha256": sha256_file(ledger),
        "source_event_ledger_blob": args.source_event_ledger_blob,
        "ap0_root": str(ap0_root),
        "ap0_manifest_sha256": manifest_sha,
        "ap0_file_set_digest": file_set_digest,
        "ap0_files_verified": len(files),
        "ap0_rows": int(manifest["coverage"]["minute_rows_written"]),
        "runner_blob": args.runner_blob,
        "contract_blob": args.contract_blob,
        "breaker_blob": args.breaker_blob,
        "freeze_blob": args.freeze_blob,
        "result_sha256": sha256_file(output),
        "diagnostics_sha256": sha256_file(diagnostics_out),
        "event_level_derived_path_ledger_persisted": False,
    }
    run_manifest.write_text(json.dumps(manifest_obj, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
