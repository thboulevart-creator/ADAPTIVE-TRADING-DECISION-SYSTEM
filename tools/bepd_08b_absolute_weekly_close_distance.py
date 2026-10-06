#!/usr/bin/env python3
"""BEPD-08B deterministic global absolute weekly-close distance aggregation.

Consumes only persisted BEPD-02 EVENT_LEDGER.close_displacement and computes
D_CLOSE = abs(close_displacement). No market reconstruction, subgrouping,
threshold search, inference, prediction, strategy, PnL, or trading analysis.
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
    ("P01", Decimal("0.01")), ("P05", Decimal("0.05")),
    ("P10", Decimal("0.10")), ("P25", Decimal("0.25")),
    ("P50", Decimal("0.50")), ("P75", Decimal("0.75")),
    ("P90", Decimal("0.90")), ("P95", Decimal("0.95")),
    ("P99", Decimal("0.99")),
]

EXPECTED_BINDINGS = {
    "event_ledger_blob": "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    "bepd08a_final_adjudication_blob": "553fedc2b538a90750839b6fce8edb9619a4dcb7",
    "bepd08a_contract_blob": "4cfcb983ad64f31b443534d70991f8ddcb11ff8f",
    "bepd08a_breaker_blob": "4d6ada0758a883ab639c93a6caf388e1e11b6d99",
    "bepd08a_freeze_blob": "1b816f5ab7031e40add1d2c515167d5fb1147843",
    "bepd05a_contract_blob": "0a580920ce47885d2bd3277b879b2b888b8d4354",
    "bepd05b_result_blob": "1280156ca949fc48f00e50240aa09cdae11ba4d7",
    "bepd05b_final_adjudication_blob": "811b8e9f58d33cc35c45f714ea99e696d589b147",
}

CANONICAL_POLICY = {
    "source_field": "close_displacement",
    "source_policy": "PERSISTED_FIELD_ONLY",
    "transformation": "abs(close_displacement)",
    "market_reconstruction": False,
    "ap0_read": False,
    "h1_read": False,
    "weekly_reconstruction": False,
    "filtering": "NONE",
    "retain_positive": True,
    "retain_negative": True,
    "retain_zero": True,
    "retain_no_reintegration": True,
    "subgroups": [],
    "sign_conditional": False,
    "threshold_search": False,
    "zero_semantics": "SOURCE_EXACT_ZERO_ONLY",
    "unit": "USTECH_PRICE_UNITS_AS_PERSISTED",
    "event_is_iid": False,
    "prediction": False,
    "edge": False,
    "tp": False,
    "sl": False,
    "strategy_validation": False,
    "pnl": False,
    "trading_authority": "NONE",
}


def q18(value: Decimal) -> str:
    return format(value.quantize(Q18, rounding=ROUND_HALF_EVEN), "f")


def exact_decimal(value: Decimal) -> str:
    return format(value, "f")


def reduced_fraction(n: int, d: int) -> str:
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


def fraction_payload(n: int, d: int) -> dict:
    return {"fraction": reduced_fraction(n, d), "decimal": q18(Decimal(n) / Decimal(d))}


def type7(sorted_values: list[Decimal], p: Decimal) -> Decimal:
    if not sorted_values:
        raise ValueError("empty population")
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


def validate_bindings(bindings: dict) -> None:
    for key, expected in EXPECTED_BINDINGS.items():
        if bindings.get(key) != expected:
            raise ValueError(f"binding mismatch: {key}")


def validate_policy(policy: dict) -> None:
    expected = CANONICAL_POLICY
    for key, value in expected.items():
        if policy.get(key) != value:
            raise ValueError(f"policy mismatch: {key}")


def validate_distance_values(values: list[Decimal]) -> None:
    if any((not v.is_finite()) for v in values):
        raise ValueError("non-finite D_CLOSE")
    if any(v < 0 for v in values):
        raise ValueError("negative D_CLOSE")


def validate_result_surface(core: dict) -> None:
    allowed = {
        "N", "MINIMUM", "MAXIMUM", "MEAN", "MEDIAN",
        "P01", "P05", "P10", "P25", "P50", "P75", "P90", "P95", "P99",
        "ZERO_COUNT", "ZERO_FRACTION", "EMPIRICAL_CDF",
    }
    if set(core) != allowed:
        raise ValueError("unauthorized result surface")
    if core["P50"] != core["MEDIAN"]:
        raise ValueError("P50 != MEDIAN")
    ecdf = core["EMPIRICAL_CDF"]
    if not ecdf or ecdf[-1]["cumulative_count"] != core["N"]:
        raise ValueError("ECDF terminal count mismatch")
    if ecdf[-1]["cumulative_fraction"] != "1":
        raise ValueError("ECDF terminal fraction mismatch")


def load_rows(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line, parse_float=Decimal))
            except Exception as exc:
                raise ValueError(f"invalid JSONL at line {line_no}: {exc}") from exc
    return rows


def distances_from_rows(rows: list[dict], expected_n: int) -> list[Decimal]:
    if len(rows) != expected_n:
        raise ValueError(f"N mismatch: observed={len(rows)} expected={expected_n}")
    event_ids = []
    values = []
    for i, row in enumerate(rows):
        event_id = row.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise ValueError(f"missing/invalid event_id at row {i}")
        event_ids.append(event_id)
        if "close_displacement" not in row:
            raise ValueError(f"missing close_displacement at row {i}")
        raw = row["close_displacement"]
        value = raw if isinstance(raw, Decimal) else Decimal(str(raw))
        if not value.is_finite():
            raise ValueError(f"non-finite close_displacement at row {i}")
        values.append(abs(value))
    if len(set(event_ids)) != expected_n:
        raise ValueError("event_id uniqueness failure")
    validate_distance_values(values)
    return values


def aggregate_rows(rows: list[dict], expected_n: int) -> dict:
    validate_policy(CANONICAL_POLICY)
    values = sorted(distances_from_rows(rows, expected_n))
    n = len(values)
    quantiles = {name: q18(type7(values, p)) for name, p in PROBS}
    zero = sum(v == 0 for v in values)
    counts = Counter(values)
    cumulative = 0
    ecdf = []
    for support in sorted(counts):
        count = counts[support]
        cumulative += count
        ecdf.append({
            "support_value": exact_decimal(support),
            "support_count": count,
            "cumulative_count": cumulative,
            "cumulative_fraction": reduced_fraction(cumulative, n),
            "cumulative_decimal": q18(Decimal(cumulative) / Decimal(n)),
        })
    core = {
        "N": n,
        "MINIMUM": q18(values[0]),
        "MAXIMUM": q18(values[-1]),
        "MEAN": q18(sum(values, Decimal(0)) / Decimal(n)),
        "MEDIAN": quantiles["P50"],
        **quantiles,
        "ZERO_COUNT": zero,
        "ZERO_FRACTION": fraction_payload(zero, n),
        "EMPIRICAL_CDF": ecdf,
    }
    validate_result_surface(core)
    return core


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
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
    ap.add_argument("--bepd08a-final-blob", required=True)
    ap.add_argument("--contract-blob", required=True)
    ap.add_argument("--breaker-blob", required=True)
    ap.add_argument("--freeze-blob", required=True)
    ap.add_argument("--runner-blob", required=True)
    args = ap.parse_args()

    bindings_check = {
        "event_ledger_blob": args.source_blob,
        "bepd08a_final_adjudication_blob": args.bepd08a_final_blob,
        "bepd08a_contract_blob": args.contract_blob,
        "bepd08a_breaker_blob": args.breaker_blob,
        "bepd08a_freeze_blob": args.freeze_blob,
        "bepd05a_contract_blob": EXPECTED_BINDINGS["bepd05a_contract_blob"],
        "bepd05b_result_blob": EXPECTED_BINDINGS["bepd05b_result_blob"],
        "bepd05b_final_adjudication_blob": EXPECTED_BINDINGS["bepd05b_final_adjudication_blob"],
    }
    validate_bindings(bindings_check)

    source = Path(args.input)
    out = Path(args.output)
    manifest_path = Path(args.manifest)
    rows = load_rows(source)
    core = aggregate_rows(rows, args.expected_n)

    run_bindings = {
        **bindings_check,
        "runner_blob": args.runner_blob,
        "expected_n": args.expected_n,
        "source_field": "close_displacement",
        "transformation": "abs(close_displacement)",
        "quantile_method": "HYNDMAN_FAN_TYPE_7",
        "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
        "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
    }
    run_id = canonical_run_id(run_bindings)

    result = {
        "schema": "ATDS_BEPD_08B_FIRST_REAL_GLOBAL_ABSOLUTE_WEEKLY_CLOSE_DISTANCE_RESULT_V0_1",
        "control_id": "BEPD-08B",
        "run_id": run_id,
        "scope": "GLOBAL_ALL_472_QUALIFIED_SWEEP_EVENTS",
        "population": {
            "source": "BEPD-02 EVENT_LEDGER",
            "expected_n": args.expected_n,
            "observed_n": len(rows),
            "filtering": "NONE",
            "weighting": "ONE_EQUAL_WEIGHT_PER_QUALIFIED_EVENT",
        },
        "distance": {
            "name": "D_CLOSE",
            "source_field": "close_displacement",
            "transformation": "abs(close_displacement)",
            "exact_equivalence": "abs(target_week_close_mid - level_price_mid)",
            "source_policy": "PERSISTED_FIELD_ONLY_NO_MARKET_RECONSTRUCTION",
            "unit": "USTECH_PRICE_UNITS_AS_PERSISTED",
            "semantic": "PRICE_DISTANCE",
        },
        "dependence": {
            "event_is_iid_observation": False,
            "dependence_keys": ["target_week_id", "sweep_cluster_id"],
            "iid_standard_error": "NOT_ACTIVATED",
            "iid_confidence_interval": "NOT_ACTIVATED",
            "iid_bootstrap": "NOT_ACTIVATED",
        },
        "numerical_contract": {
            "quantile_method": "HYNDMAN_FAN_TYPE_7",
            "p50_equals_median": True,
            "ecdf": "EXACT_UNSMOOTHED_UNBINNED",
            "scalar_output": "18_DECIMAL_ROUND_HALF_EVEN",
        },
        "bindings": run_bindings,
        "core": core,
        "sign_conditional_outputs": [],
        "subgroups_executed": [],
        "threshold_search_executed": False,
        "broker_conversion_executed": False,
        "tp_sl_executed": False,
        "pnl_executed": False,
        "evidence_status": "EXPOSED_EXPLORATORY_ONLY",
        "historical_corpus": "ALREADY_EXPOSED",
        "generalization": "NOT_ESTABLISHED",
        "confirmatory_generalization": "FRESH_OOS_EVIDENCE_REQUIRED",
        "prediction": False,
        "causation": "NOT_ESTABLISHED",
        "edge": False,
        "strategy_validation": False,
        "trading_authority": "NONE",
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema": "ATDS_BEPD_08B_RUN_MANIFEST_V0_1",
        "run_id": run_id,
        "input_path": str(source),
        "input_git_blob": args.source_blob,
        "input_sha256": sha256_file(source),
        "output_path": str(out),
        "output_sha256": sha256_file(out),
        "expected_n": args.expected_n,
        "observed_n": len(rows),
        "runner_blob": args.runner_blob,
        "bepd08a_final_adjudication_blob": args.bepd08a_final_blob,
        "contract_blob": args.contract_blob,
        "breaker_blob": args.breaker_blob,
        "freeze_blob": args.freeze_blob,
        "result_exposure": "FIRST_REAL_GLOBAL_D_CLOSE_DISTRIBUTION",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
