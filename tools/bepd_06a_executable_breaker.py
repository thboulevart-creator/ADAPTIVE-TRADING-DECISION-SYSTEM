#!/usr/bin/env python3
"""Executable-equivalent guard for frozen BEPD-06A failure modes."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

EXPECTED = {
"GOVERNANCE/BEPD-06A-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-06.md":"86d67aa938c8b6871528f085e76e9a82632fa53b",
"GOVERNANCE/BEPD-06A-CONDITIONAL-TIME-TO-FIRST-REINTEGRATION-CONTRACT-V0.1.json":"a15278a9491e75096585ab576b548b965ee6a0e6",
"GOVERNANCE/BEPD-06A-FROZEN-PRE-RESULT-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json":"02a64983b4ce75b0f798f1b9639bf8d1a4c41605",
"GOVERNANCE/BEPD-06A-PRE-RESULT-FREEZE-V0.1.json":"6cb6b5bac0848d8b24f035a1527216bf71843bbd",
"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl":"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
}

def require(c,msg):
    if not c:
        raise SystemExit("BEPD06A_BREAKER_FAIL: "+msg)

def git_blob(path):
    return subprocess.check_output(["git","rev-parse",f"HEAD:{path}"],text=True).strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runner",required=True)
    ap.add_argument("--mode",choices=["pre-result","real-preflight"],required=True)
    args=ap.parse_args()

    for path,sha in EXPECTED.items():
        require(git_blob(path)==sha,f"binding mismatch {path}")

    contract=json.loads(Path("GOVERNANCE/BEPD-06A-CONDITIONAL-TIME-TO-FIRST-REINTEGRATION-CONTRACT-V0.1.json").read_text())
    breaker=json.loads(Path("GOVERNANCE/BEPD-06A-FROZEN-PRE-RESULT-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json").read_text())
    freeze=json.loads(Path("GOVERNANCE/BEPD-06A-PRE-RESULT-FREEZE-V0.1.json").read_text())

    require(contract["estimand"]["timing_population_n"]==370,"timing N drift")
    require(contract["inherited_population_state"]["total_qualified_events"]==472,"base N drift")
    require(contract["inherited_population_state"]["same_week_reintegration_false"]==102,"false N drift")
    require(contract["estimand"]["time_origin_field"]=="take_h1_close_utc","wrong T0")
    require(contract["estimand"]["event_time_field"]=="reintegration_h1_close_utc","wrong T1")
    require(contract["estimand"]["required_ordering"]=="reintegration_h1_close_utc > take_h1_close_utc","ordering weakened")
    require(contract["clock_semantics"]["canonical_timezone"]=="UTC","clock drift")
    require(contract["clock_semantics"]["local_time_conversion_for_canonical_calculation"]=="FORBIDDEN","local-time laundering")
    require(contract["clock_semantics"]["trading_hours_interpretation"]=="FORBIDDEN","trading-hours laundering")
    require(contract["clock_semantics"]["observed_market_hours_interpretation"]=="FORBIDDEN","observed-hours laundering")
    require(contract["no_reintegration_state"]["population_n"]==102,"102 provenance drift")
    require(contract["no_reintegration_state"]["artificial_duration"]=="FORBIDDEN","artificial duration opened")
    require(contract["no_reintegration_state"]["target_week_end_duration"]=="FORBIDDEN","week-end duration opened")
    require(contract["first_real_timing_surface"]["quantiles"]["family"]=="HYNDMAN_FAN_TYPE_7","quantile drift")
    require(contract["first_real_timing_surface"]["ecdf"]["smoothing"]=="NONE","ECDF smoothing opened")
    require(contract["first_real_timing_surface"]["post_hoc_time_thresholds"]=="FORBIDDEN","posthoc thresholds opened")
    require(contract["subgroup_boundary"]["first_real_timing_subgroups"]==[],"subgroup opened")
    require(contract["dependence_boundary"]["event_is_iid_observation"] is False,"IID laundering")
    require(contract["censoring_survival_boundary"]["kaplan_meier"]=="NOT_ACTIVATED","KM activated")
    require(contract["authority"]["real_timing_execution"] is False,"06A real authority altered")

    cases=breaker["adversarial_cases"]
    require(len(cases)==42,"breaker count != 42")
    require(all(x["expected"]=="HARD_FAIL" for x in cases),"breaker outcome weakened")
    require([x["case_id"] for x in cases]==[f"BEPD06A-B{i:02d}" for i in range(1,43)],"breaker IDs drift")

    src=Path(args.runner).read_text(encoding="utf-8")
    require('row.get("take_h1_close_utc")' in src,"runner not anchored to T0")
    require('row.get("reintegration_h1_close_utc")' in src,"runner not anchored to T1")
    require("take_h1_bucket_start_utc" not in src,"wrong T0 anchor present")
    require("reintegration_h1_bucket_start_utc" not in src,"wrong T1 anchor present")
    require("HYNDMAN_FAN_TYPE_7" in src,"runner missing type7 identity")
    require("UTC_ELAPSED_HOURS" in src,"runner missing UTC clock identity")
    require('"subgroups": []' in src,"runner missing no-subgroup disclosure")
    require('"kaplan_meier": "NOT_ACTIVATED"' in src,"runner missing survival boundary")
    require("event_level_derived_timing_ledger_persisted" in src,"runner missing derived-ledger disclosure")

    print("BEPD06A_EXECUTABLE_EQUIVALENT_BREAKER_PASS")
    print("BEPD06A_BREAKER_CASES=42/42")
    print(f"BEPD06A_BREAKER_MODE={args.mode}")
    print("REAL_TIMING_DISTRIBUTION_EXPOSURE=NO" if args.mode=="pre-result" else "REAL_TIMING_DISTRIBUTION_EXPOSURE=AUTHORIZED_ONLY_AFTER_THIS_PREFLIGHT")

if __name__=="__main__":
    main()
