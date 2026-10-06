#!/usr/bin/env python3
"""Executable-equivalent qualification for the frozen BEPD-05A breaker.

This tool validates that all 41 frozen failure modes remain present and that
the BEPD-05B implementation cannot silently weaken the adopted BEPD-05A
semantics before real aggregation.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

EXPECTED_EVENT_LEDGER_BLOB = "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2"
EXPECTED_SCHEMA_BLOB = "85f5cdda60397fce59efc1e5d36c1128cf9cc185"
EXPECTED_CONTRACT_BLOB = "0a580920ce47885d2bd3277b879b2b888b8d4354"
EXPECTED_BREAKER_BLOB = "c39802f70d83dc249d23fe240b61169bf20ac757"
EXPECTED_FREEZE_BLOB = "30d438ef1daad9acaad170c002d7d5d8426acec4"
EXPECTED_ADJUDICATION_BLOB = "024c7d23210b9c62604b3c6d2379746c1ac736a4"

PATH_EVENT = "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PATH_SCHEMA = "GOVERNANCE/BEPD-01D-HISTORICAL-LEDGER-SCHEMA-V0.1.json"
PATH_CONTRACT = "GOVERNANCE/BEPD-05A-CLOSE-DISPLACEMENT-RESPONSE-SEMANTICS-AGGREGATION-CONTRACT-V0.1.json"
PATH_BREAKER = "GOVERNANCE/BEPD-05A-FROZEN-PRE-AGGREGATION-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
PATH_FREEZE = "GOVERNANCE/BEPD-05A-PRE-AGGREGATION-FREEZE-V0.1.json"
PATH_ADJUDICATION = "GOVERNANCE/BEPD-05A-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-06.md"


def fail(msg: str) -> None:
    raise SystemExit("BEPD05A_BREAKER_FAIL: " + msg)


def git_blob(path: str) -> str:
    out = subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], text=True).strip()
    return out


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(condition: bool, msg: str) -> None:
    if not condition:
        fail(msg)


def check_git_bindings() -> None:
    expected = {
        PATH_EVENT: EXPECTED_EVENT_LEDGER_BLOB,
        PATH_SCHEMA: EXPECTED_SCHEMA_BLOB,
        PATH_CONTRACT: EXPECTED_CONTRACT_BLOB,
        PATH_BREAKER: EXPECTED_BREAKER_BLOB,
        PATH_FREEZE: EXPECTED_FREEZE_BLOB,
        PATH_ADJUDICATION: EXPECTED_ADJUDICATION_BLOB,
    }
    for path, sha in expected.items():
        require(git_blob(path) == sha, f"binding mismatch for {path}")


def check_contract(c: dict) -> None:
    require(c["source_semantics"]["population"] == "ALL_QUALIFIED_BEPD02_EVENT_LEDGER_ROWS", "population drift")
    require(c["source_semantics"]["expected_event_count"] == 472, "N drift")
    require(c["source_semantics"]["filtering"] == "NONE", "filtering introduced")
    require(c["source_semantics"]["response_field"] == "close_displacement", "response field drift")
    require(c["source_semantics"]["source_policy"] == "USE_ALREADY_QUALIFIED_LEDGER_FIELD_ONLY_NO_MARKET_RECONSTRUCTION", "reconstruction policy weakened")
    require(c["source_semantics"]["negative_values"] == "RETAIN", "negative suppression allowed")
    require(c["source_semantics"]["zero_values"] == "RETAIN", "zero suppression allowed")
    require(c["source_semantics"]["no_reintegration_rows"] == "RETAIN", "no-reintegration suppression allowed")

    s = c["sign_semantics"]
    require(s["high_formula"] == "level_price_mid - target_week_close_mid", "HIGH sign drift")
    require(s["low_formula"] == "target_week_close_mid - level_price_mid", "LOW sign drift")
    require(s["profit_loss_interpretation"] == "FORBIDDEN", "PnL laundering opened")
    require(s["side_specific_sign_reversal_after_source"] == "FORBIDDEN", "post-source sign reversal opened")

    agg = c["primary_global_aggregation"]
    require(agg["scope"] == "GLOBAL_ALL_SIDES_ONLY", "subgroup scope opened")
    require(agg["weighting"] == "ONE_EQUAL_WEIGHT_PER_QUALIFIED_EVENT_LEDGER_ROW", "weighting drift")
    require(agg["quantiles"]["family"] == "HYNDMAN_FAN_TYPE_7", "quantile method drift")
    require(agg["quantiles"]["p50_must_equal_median"] is True, "P50/median distinction opened")
    require(agg["empirical_cdf"]["histogram_bins"] == "NONE", "histogram substitution opened")
    require(agg["empirical_cdf"]["smoothing"] == "NONE", "ECDF smoothing opened")
    require(agg["empirical_cdf"]["tail_suppression"] == "FORBIDDEN", "tail suppression opened")

    d = c["dependence_boundary"]
    require(d["event_is_iid_observation"] is False, "IID laundering")
    require(d["dependence_keys"] == ["target_week_id", "sweep_cluster_id"], "dependence key drift")
    require(d["iid_standard_error"] == "FORBIDDEN", "IID SE opened")
    require(d["iid_confidence_interval"] == "FORBIDDEN", "IID CI opened")
    require(d["iid_bootstrap"] == "FORBIDDEN", "IID bootstrap opened")

    require(c["subgroup_boundary"]["first_real_aggregation_subgroups"] == [], "subgroups opened")
    require(c["evidence_status"]["analysis_status"] == "EXPLORATORY_ONLY", "exploratory status lost")
    require(c["evidence_status"]["pristine_confirmation"] is False, "pristine laundering")
    require(c["evidence_status"]["future_confirmatory_claim"] == "FRESH_OOS_EVIDENCE_REQUIRED", "fresh OOS requirement lost")

    a = c["authority"]
    for key in [
        "real_close_displacement_aggregation", "real_distribution_exposure",
        "subgroup_analysis", "uncertainty_inference", "oos_consumption",
        "prediction", "causation", "edge", "strategy", "pnl", "trading", "capital"
    ]:
        require(a[key] is False, f"unauthorized authority enabled: {key}")


def check_breaker(b: dict) -> None:
    cases = b["adversarial_cases"]
    require(len(cases) == 41, "breaker case count != 41")
    require(b["qualification_rule"]["required_case_count"] == 41, "required case count drift")
    expected_ids = [f"BEPD05A-B{i:02d}" for i in range(1, 42)]
    observed_ids = [x["case_id"] for x in cases]
    require(observed_ids == expected_ids, "breaker case IDs/order drift")
    require(all(x["expected"] == "HARD_FAIL" for x in cases), "weakened breaker outcome")
    intents = "\n".join(x["mutation"] for x in cases)
    for phrase in [
        "HIGH sign formula inverted",
        "LOW sign formula inverted",
        "target-week close replaced by take H1 close",
        "reference level replaced by take price",
        "negative close_displacement rows dropped or clipped",
        "zero close_displacement rows dropped",
        "same_week_reintegration=false rows dropped",
        "conditioning on same_week_reintegration introduced",
        "HIGH vs LOW subgroup introduced",
        "EVENT treated as IID observation",
        "naive IID standard error, confidence interval, or bootstrap introduced",
        "close_displacement converted to PnL/ticks/money/risk multiple/TP/SL/trade return",
        "exploratory exposed-corpus result represented as pristine confirmation",
        "historical distribution represented as future probability or prediction",
        "distribution represented as edge or strategy validation",
        "distribution represented as trading or capital authority",
        "real close-displacement aggregate statistic calculated under BEPD-05A authority",
        "OOS data consumed under BEPD-05A authority",
    ]:
        require(phrase in intents, f"mandatory failure mode missing: {phrase}")


def check_freeze(f: dict) -> None:
    scope = f["freeze_scope"]
    require(scope["population"] == "ALL 472 QUALIFIED BEPD-02 EVENT_LEDGER ROWS", "freeze population drift")
    require(scope["response"] == "close_displacement", "freeze response drift")
    require(scope["aggregation"] == "GLOBAL_ALL_SIDES_ONLY", "freeze aggregation drift")
    require(scope["quantile_method"] == "HYNDMAN_FAN_TYPE_7", "freeze quantile drift")
    require(scope["ecdf"] == "EXACT_UNSMOOTHED_EMPIRICAL_CDF", "freeze ECDF drift")
    require(scope["subgroups"] == "NONE", "freeze subgroup drift")
    require(scope["evidence_status"] == "EXPOSED_EXPLORATORY_ONLY", "freeze evidence drift")
    require(f["real_result_exposure"] is False, "pre-result freeze already exposes result")
    require(f["real_aggregation_executed"] is False, "pre-result freeze already executed aggregation")


def check_runner_source(path: str) -> None:
    src = Path(path).read_text(encoding="utf-8")
    require('row["close_displacement"]' in src, "runner does not consume persisted close_displacement")
    require('row["level_price_mid"]' not in src, "runner reconstructs from level_price_mid")
    require('row["target_week_close_mid"]' not in src, "runner reconstructs from target_week_close_mid")
    require("HYNDMAN_FAN_TYPE_7" in src, "runner missing frozen quantile identity")
    require("EXACT_UNSMOOTHED_UNBINNED" in src, "runner missing frozen ECDF identity")
    require("subgroups_executed" in src, "runner missing subgroup disclosure")
    require('"NONE"' in src, "runner missing no-filter declaration")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", default=PATH_CONTRACT)
    ap.add_argument("--breaker", default=PATH_BREAKER)
    ap.add_argument("--freeze", default=PATH_FREEZE)
    ap.add_argument("--runner", required=True)
    ap.add_argument("--mode", choices=["pre-result", "real-preflight"], required=True)
    args = ap.parse_args()

    check_git_bindings()
    check_contract(load_json(args.contract))
    check_breaker(load_json(args.breaker))
    check_freeze(load_json(args.freeze))
    check_runner_source(args.runner)

    print("BEPD05A_EXECUTABLE_EQUIVALENT_BREAKER_PASS")
    print("BEPD05A_BREAKER_CASES=41/41")
    print(f"BEPD05A_BREAKER_MODE={args.mode}")
    print("REAL_RESULT_EXPOSURE=NO" if args.mode == "pre-result" else "REAL_RESULT_EXPOSURE=AUTHORIZED_ONLY_AFTER_THIS_PREFLIGHT")


if __name__ == "__main__":
    main()
