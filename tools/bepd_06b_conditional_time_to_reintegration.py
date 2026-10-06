#!/usr/bin/env python3
"""BEPD-06B deterministic conditional time-to-first-reintegration aggregation.

Consumes only persisted BEPD-02 EVENT_LEDGER timestamps and the pre-existing
same_week_reintegration state. No market rescan, no survival model, no subgroup
analysis, and no event-level derived timing ledger are produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80
Q18 = Decimal("0.000000000000000001")
HOUR_US = Decimal(3_600_000_000)

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


def q18(value: Decimal) -> str:
    return format(value.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def exact_decimal(value: Decimal) -> str:
    return format(value, "f")


def reduced_fraction(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def parse_utc(ts: str) -> datetime:
    if not isinstance(ts, str) or not ts:
        raise ValueError("timestamp missing")
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware UTC")
    if dt.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp offset must be UTC")
    return dt


def elapsed_hours(t0s: str, t1s: str) -> Decimal:
    t0 = parse_utc(t0s)
    t1 = parse_utc(t1s)
    if not t1 > t0:
        raise ValueError("T1 must be strictly greater than T0")
    delta = t1 - t0
    total_us = (
        Decimal(delta.days) * Decimal(86_400_000_000)
        + Decimal(delta.seconds) * Decimal(1_000_000)
        + Decimal(delta.microseconds)
    )
    return total_us / HOUR_US


def type7(sorted_values: list[Decimal], p: Decimal) -> Decimal:
    if not sorted_values:
        raise ValueError("empty timing population")
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    h = Decimal(1) + Decimal(n - 1) * p
    j = int(h)
    gamma = h - Decimal(j)
    if j >= n:
        return sorted_values[-1]
    lo = sorted_values[j - 1]
    hi = sorted_values[j]
    return (Decimal(1) - gamma) * lo + gamma * hi


def load_rows(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except Exception as exc:
                raise ValueError(f"invalid JSONL at line {line_no}: {exc}") from exc
    return rows


def aggregate_rows(rows: list[dict], expected_base_n: int, expected_true_n: int, expected_false_n: int) -> dict:
    if len(rows) != expected_base_n:
        raise ValueError(f"base N mismatch: observed={len(rows)} expected={expected_base_n}")

    event_ids = []
    timing_values: list[Decimal] = []
    true_n = 0
    false_n = 0

    for i, row in enumerate(rows):
        event_id = row.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError(f"missing/invalid event_id at row {i}")
        event_ids.append(event_id)

        state = row.get("same_week_reintegration")
        t0 = row.get("take_h1_close_utc")
        t1 = row.get("reintegration_h1_close_utc")

        if state is True:
            true_n += 1
            if t0 is None:
                raise ValueError(f"T0 null for reintegrating event at row {i}")
            if t1 is None:
                raise ValueError(f"T1 null for reintegrating event at row {i}")
            timing_values.append(elapsed_hours(t0, t1))
        elif state is False:
            false_n += 1
            if t1 is not None:
                raise ValueError(f"no-reintegration event has non-null T1 at row {i}")
            # No duration is assigned or calculated.
        else:
            raise ValueError(f"invalid same_week_reintegration state at row {i}")

    if len(set(event_ids)) != expected_base_n:
        raise ValueError("event_id uniqueness failure")
    if true_n != expected_true_n:
        raise ValueError(f"reintegration true N mismatch: {true_n} != {expected_true_n}")
    if false_n != expected_false_n:
        raise ValueError(f"reintegration false N mismatch: {false_n} != {expected_false_n}")
    if true_n + false_n != expected_base_n:
        raise AssertionError("370/102 state reconciliation failure")
    if len(timing_values) != expected_true_n:
        raise AssertionError("timing population mismatch")

    ordered = sorted(timing_values)
    n = len(ordered)
    quantiles = {name: q18(type7(ordered, p)) for name, p in PROBS}
    counts = Counter(ordered)
    cumulative = 0
    ecdf = []
    for support in sorted(counts):
        support_count = counts[support]
        cumulative += support_count
        ecdf.append({
            "support_value": exact_decimal(support),
            "support_count": support_count,
            "cumulative_count": cumulative,
            "cumulative_fraction": reduced_fraction(cumulative, n),
            "cumulative_decimal": q18(Decimal(cumulative) / Decimal(n)),
        })

    core = {
        "BASE_N": expected_base_n,
        "REINTEGRATION_TRUE_N": true_n,
        "NO_REINTEGRATION_WITHIN_TARGET_WEEK_N": false_n,
        "N_TIMING": n,
        "MINIMUM_ELAPSED_UTC_HOURS": q18(ordered[0]),
        "MAXIMUM_ELAPSED_UTC_HOURS": q18(ordered[-1]),
        "MEAN": q18(sum(ordered, Decimal(0)) / Decimal(n)),
        "MEDIAN": quantiles["P50"],
        **quantiles,
        "EMPIRICAL_CDF": ecdf,
    }

    if core["P50"] != core["MEDIAN"]:
        raise AssertionError("P50 != MEDIAN")
    if ecdf[-1]["cumulative_count"] != expected_true_n:
        raise AssertionError("ECDF terminal count mismatch")
    if ecdf[-1]["cumulative_fraction"] != "1":
        raise AssertionError("ECDF terminal fraction mismatch")
    return core


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_id(bindings: dict) -> str:
    payload = json.dumps(bindings, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--expected-base-n", type=int, default=472)
    ap.add_argument("--expected-true-n", type=int, default=370)
    ap.add_argument("--expected-false-n", type=int, default=102)
    ap.add_argument("--source-blob", required=True)
    ap.add_argument("--contract-blob", required=True)
    ap.add_argument("--breaker-blob", required=True)
    ap.add_argument("--freeze-blob", required=True)
    ap.add_argument("--runner-blob", required=True)
    args = ap.parse_args()

    source = Path(args.input)
    rows = load_rows(source)
    core = aggregate_rows(rows, args.expected_base_n, args.expected_true_n, args.expected_false_n)

    bindings = {
        "source_event_ledger_blob": args.source_blob,
        "bepd06a_contract_blob": args.contract_blob,
        "bepd06a_breaker_blob": args.breaker_blob,
        "bepd06a_freeze_blob": args.freeze_blob,
        "runner_blob": args.runner_blob,
        "base_n": args.expected_base_n,
        "reintegration_true_n": args.expected_true_n,
        "reintegration_false_n": args.expected_false_n,
        "condition": "same_week_reintegration == true",
        "t0": "take_h1_close_utc",
        "t1": "reintegration_h1_close_utc",
        "clock": "UTC_ELAPSED_HOURS",
        "quantile_method": "HYNDMAN_FAN_TYPE_7",
        "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
    }
    rid = run_id(bindings)

    result = {
        "schema": "ATDS_BEPD_06B_FIRST_REAL_CONDITIONAL_TIME_TO_FIRST_REINTEGRATION_RESULT_V0_1",
        "control_id": "BEPD-06B",
        "run_id": rid,
        "scope": "CONDITIONAL_ON_SAME_WEEK_REINTEGRATION_TRUE",
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
            "base_n": args.expected_base_n,
            "reintegration_true_n": args.expected_true_n,
            "no_reintegration_within_target_week_n": args.expected_false_n,
            "timing_population_n": args.expected_true_n,
            "condition": "same_week_reintegration == true",
            "no_reintegration_semantic": "TIME_TO_REINTEGRATION_NOT_OBSERVED_WITHIN_TARGET_WEEK",
            "no_reintegration_duration_assigned": False,
            "subgroups": [],
        },
        "timing_contract": {
            "t0_field": "take_h1_close_utc",
            "t1_field": "reintegration_h1_close_utc",
            "required_ordering": "T1 > T0",
            "duration": "(T1 - T0) / 1 hour",
            "clock": "UTC_ELAPSED_HOURS",
            "trading_hours_interpretation": False,
            "observed_market_hours_interpretation": False,
            "time_in_position_interpretation": False,
        },
        "dependence": {
            "event_is_iid_observation": False,
            "dependence_keys": ["target_week_id", "sweep_cluster_id"],
            "iid_standard_error": "FORBIDDEN",
            "iid_confidence_interval": "FORBIDDEN",
            "iid_bootstrap": "FORBIDDEN",
        },
        "survival": {
            "kaplan_meier": "NOT_ACTIVATED",
            "survival_function": "NOT_ACTIVATED",
            "hazard_function": "NOT_ACTIVATED",
            "censoring_model": "NOT_ACTIVATED",
        },
        "numerical_contract": {
            "quantile_method": "HYNDMAN_FAN_TYPE_7",
            "p50_equals_median": True,
            "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
            "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
        },
        "bindings": bindings,
        "core": core,
        "event_level_derived_timing_ledger_persisted": False,
        "forbidden_analytics_executed": False,
    }

    out = Path(args.output)
    manifest_path = Path(args.manifest)
    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": "ATDS_BEPD_06B_RUN_MANIFEST_V0_1",
        "run_id": rid,
        "input_path": str(source),
        "input_git_blob": args.source_blob,
        "input_sha256": sha256_file(source),
        "result_path": str(out),
        "result_sha256": sha256_file(out),
        "runner_blob": args.runner_blob,
        "contract_blob": args.contract_blob,
        "breaker_blob": args.breaker_blob,
        "freeze_blob": args.freeze_blob,
        "base_n": args.expected_base_n,
        "reintegration_true_n": args.expected_true_n,
        "reintegration_false_n": args.expected_false_n,
        "event_level_derived_timing_ledger_persisted": False,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
