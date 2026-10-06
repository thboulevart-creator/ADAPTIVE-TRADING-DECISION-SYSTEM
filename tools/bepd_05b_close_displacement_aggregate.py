#!/usr/bin/env python3
"""BEPD-05B deterministic global close_displacement aggregation.

This runner consumes only the already-qualified EVENT_LEDGER close_displacement
field. It does not reconstruct the response from market prices and it does not
perform subgroup, inferential, predictive, strategy, PnL, or trading analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 80

Q18 = Decimal("0.000000000000000001")
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


def sign_fraction(n: int, d: int) -> dict:
    return {
        "fraction": f"{n}/{d}",
        "decimal": q18(Decimal(n) / Decimal(d)),
    }


def reduced_fraction(n: int, d: int) -> str:
    f = Fraction(n, d)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def type7(sorted_values: list[Decimal], p: Decimal) -> Decimal:
    if not sorted_values:
        raise ValueError("empty population")
    n = len(sorted_values)
    if n == 1:
        return sorted_values[0]
    h = Decimal(1) + Decimal(n - 1) * p
    j = int(h)  # floor because h >= 1
    gamma = h - Decimal(j)
    if j >= n:
        return sorted_values[-1]
    lo = sorted_values[j - 1]
    hi = sorted_values[j]
    return (Decimal(1) - gamma) * lo + gamma * hi


def load_rows(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line, parse_float=Decimal)
            except Exception as exc:
                raise ValueError(f"invalid JSONL at line {line_no}: {exc}") from exc
            rows.append(row)
    return rows


def aggregate_rows(rows: list[dict], expected_n: int) -> dict:
    if len(rows) != expected_n:
        raise ValueError(f"N mismatch: observed={len(rows)} expected={expected_n}")

    event_ids = []
    values: list[Decimal] = []
    for i, row in enumerate(rows):
        event_id = row.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError(f"missing/invalid event_id at row {i}")
        event_ids.append(event_id)
        if "close_displacement" not in row:
            raise ValueError(f"missing close_displacement at row {i}")
        value = row["close_displacement"]
        if not isinstance(value, Decimal):
            value = Decimal(str(value))
        if not value.is_finite():
            raise ValueError(f"non-finite close_displacement at row {i}")
        values.append(value)

    if len(set(event_ids)) != expected_n:
        raise ValueError("event_id uniqueness failure")

    ordered = sorted(values)
    n = len(ordered)
    total = sum(ordered, Decimal(0))
    mean = total / Decimal(n)

    quantiles = {name: q18(type7(ordered, p)) for name, p in PROBS}
    median = quantiles["P50"]

    positive = sum(1 for x in ordered if x > 0)
    zero = sum(1 for x in ordered if x == 0)
    negative = sum(1 for x in ordered if x < 0)
    if positive + zero + negative != n:
        raise AssertionError("sign count reconciliation failed")

    counts = Counter(ordered)
    cumulative = 0
    ecdf = []
    for support in sorted(counts):
        support_count = counts[support]
        cumulative += support_count
        ecdf.append(
            {
                "support_value": exact_decimal(support),
                "support_count": support_count,
                "cumulative_count": cumulative,
                "cumulative_fraction": reduced_fraction(cumulative, n),
                "cumulative_decimal": q18(Decimal(cumulative) / Decimal(n)),
            }
        )

    if ecdf[-1]["cumulative_count"] != n:
        raise AssertionError("ECDF final cumulative count mismatch")
    if ecdf[-1]["cumulative_fraction"] != "1":
        raise AssertionError("ECDF final cumulative fraction is not 1")

    core = {
        "N": n,
        "MINIMUM": q18(ordered[0]),
        "MAXIMUM": q18(ordered[-1]),
        "MEAN": q18(mean),
        "MEDIAN": median,
        **quantiles,
        "POSITIVE_COUNT": positive,
        "ZERO_COUNT": zero,
        "NEGATIVE_COUNT": negative,
        "POSITIVE_FRACTION": sign_fraction(positive, n),
        "ZERO_FRACTION": sign_fraction(zero, n),
        "NEGATIVE_FRACTION": sign_fraction(negative, n),
        "EMPIRICAL_CDF": ecdf,
    }

    if core["P50"] != core["MEDIAN"]:
        raise AssertionError("P50 != MEDIAN")
    return core


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_run_id(bindings: dict) -> str:
    payload = json.dumps(bindings, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--expected-n", type=int, required=True)
    ap.add_argument("--source-blob", required=True)
    ap.add_argument("--contract-blob", required=True)
    ap.add_argument("--breaker-blob", required=True)
    ap.add_argument("--freeze-blob", required=True)
    ap.add_argument("--runner-blob", required=True)
    args = ap.parse_args()

    source = Path(args.input)
    out = Path(args.output)
    manifest_path = Path(args.manifest)

    rows = load_rows(source)
    core = aggregate_rows(rows, args.expected_n)

    bindings = {
        "source_event_ledger_blob": args.source_blob,
        "bepd05a_contract_blob": args.contract_blob,
        "bepd05a_breaker_blob": args.breaker_blob,
        "bepd05a_freeze_blob": args.freeze_blob,
        "runner_blob": args.runner_blob,
        "expected_n": args.expected_n,
        "quantile_method": "HYNDMAN_FAN_TYPE_7",
        "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
        "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
    }
    run_id = canonical_run_id(bindings)

    result = {
        "schema": "ATDS_BEPD_05B_FIRST_REAL_GLOBAL_CLOSE_DISPLACEMENT_RESULT_V0_1",
        "control_id": "BEPD-05B",
        "run_id": run_id,
        "scope": "GLOBAL_ALL_SIDES_FIXED_HISTORICAL_CORPUS",
        "evidence_status": "EXPOSED_EXPLORATORY_ONLY",
        "pristine_confirmation": False,
        "generalization": "NOT_ESTABLISHED",
        "confirmatory_generalization": "FRESH_OOS_EVIDENCE_REQUIRED",
        "prediction": False,
        "causation": "NOT_ESTABLISHED",
        "edge": False,
        "strategy_validation": False,
        "trading_authority": "NONE",
        "population": {
            "source": "BEPD-02 EVENT_LEDGER",
            "expected_n": args.expected_n,
            "observed_n": len(rows),
            "filtering": "NONE",
            "weighting": "ONE_EQUAL_WEIGHT_PER_QUALIFIED_EVENT",
            "unit": "ONE_QUALIFIED_LEVEL_SWEEP_EVENT",
        },
        "response": {
            "field": "close_displacement",
            "source_policy": "USE_PERSISTED_FIELD_ONLY_NO_MARKET_RECONSTRUCTION",
            "high_semantic": "level_price_mid - target_week_close_mid",
            "low_semantic": "target_week_close_mid - level_price_mid",
            "unit": "USTECH_PRICE_UNITS_AS_PERSISTED",
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
            "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
            "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
        },
        "bindings": bindings,
        "core": core,
        "subgroups_executed": [],
        "forbidden_analytics_executed": False,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    manifest = {
        "schema": "ATDS_BEPD_05B_RUN_MANIFEST_V0_1",
        "run_id": run_id,
        "input_path": str(source),
        "input_git_blob": args.source_blob,
        "input_sha256": sha256_file(source),
        "output_path": str(out),
        "output_sha256": sha256_file(out),
        "expected_n": args.expected_n,
        "observed_n": len(rows),
        "runner_blob": args.runner_blob,
        "contract_blob": args.contract_blob,
        "breaker_blob": args.breaker_blob,
        "freeze_blob": args.freeze_blob,
        "result_exposure": "FIRST_REAL_GLOBAL_CLOSE_DISPLACEMENT_AGGREGATION",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
