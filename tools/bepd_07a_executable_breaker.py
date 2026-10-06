#!/usr/bin/env python3
"""Executable-equivalent guard for the frozen BEPD-07A 40-case breaker.

This guard is pre-result only. It validates persisted identities, frozen semantics,
and implementation source invariants without reading any real AP0 Parquet file.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

EXPECTED = {
    "GOVERNANCE/BEPD-07A-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-06.md":
        "5b8a8c9538363f8878acfa47c75db420438582be",
    "GOVERNANCE/BEPD-07A-SAME-WEEK-POST-SWEEP-PATH-GEOMETRY-CONTRACT-V0.1.json":
        "d7b3aeed923a91e0e2aac530a952978c1f8fa5d6",
    "GOVERNANCE/BEPD-07A-FROZEN-PRE-RESULT-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json":
        "42f2a720a0904c83c45a507cfa340af30ba73ae5",
    "GOVERNANCE/BEPD-07A-PRE-RESULT-FREEZE-V0.1.json":
        "10fa2fc9011dded1567a054efb31fbabfa6dab8a",
    "reports/program/2026-10-06-BEPD-07A-QUALIFICATION-RECEIPT-V0.1.json":
        "36fd2571cf5fe22d3ec0d404c6f50dbceab2b25f",
    "reports/program/2026-10-06-BEPD-07A-QUALIFICATION-V0.1.md":
        "e48a5d8ad342ad057d3509935bf8daab86534cd8",
    "artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl":
        "0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
    "reports/program/2026-09-25-AP0-USTECH-PROFILE-MINUTE-CORE-ADJUDICATION.md":
        "94bba3315e3569993623b8cd2a2bf4264f4ab6f8",
    "tools/ap0_ustech_profile_minute_core.py":
        "42fcb38809a1cc0365cd4027fae5154e1d6d3b4f",
    "tools/bepd_02_historical_weekly_liquidity_ledger_build_v0_1.py":
        "99279c2bf252105744a18eb721f2fefe9ef883e8",
    "GOVERNANCE/RVO-08-AP0-RESOURCE-CONTRACT-V0.1.json":
        "23cef7d6dcc6ca0b4e3c72bd8f3af4e91b1d6ca3",
    "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json":
        "ccfccda676abfe7e02082a331557ffed14e1f32b",
}


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit("BEPD07A_BREAKER_FAIL: " + msg)


def git_blob(path: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], text=True).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runner", required=True)
    ap.add_argument("--independent", required=True)
    ap.add_argument("--mode", choices=["pre-result", "real-preflight"], required=True)
    args = ap.parse_args()

    for path, expected in EXPECTED.items():
        require(git_blob(path) == expected, f"binding mismatch {path}")

    contract = json.loads(Path(
        "GOVERNANCE/BEPD-07A-SAME-WEEK-POST-SWEEP-PATH-GEOMETRY-CONTRACT-V0.1.json"
    ).read_text(encoding="utf-8"))
    breaker = json.loads(Path(
        "GOVERNANCE/BEPD-07A-FROZEN-PRE-RESULT-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
    ).read_text(encoding="utf-8"))
    freeze = json.loads(Path(
        "GOVERNANCE/BEPD-07A-PRE-RESULT-FREEZE-V0.1.json"
    ).read_text(encoding="utf-8"))

    require(contract["population"]["expected_n"] == 472, "base N drift")
    require(contract["population"]["filtering"] == "NONE", "filtering opened")
    require(contract["anchor"]["price_field"] == "take_h1_close_mid", "anchor drift")
    require(contract["anchor"]["availability_time_field"] == "take_h1_close_utc", "confirmation drift")
    require(contract["path_window"]["start_predicate"] ==
            "minute_start_ms_utc > take_h1_close_utc", "path start weakened")
    require(contract["path_window"]["same_h1_excursion"] == "FORBIDDEN", "same-H1 opened")
    require(contract["path_window"]["end_predicate"] ==
            "minute_start_ms_utc < target_week_end_utc", "path end weakened")
    require(contract["path_window"]["outcome_dependent_endpoint"] == "FORBIDDEN",
            "outcome-dependent endpoint opened")
    require(contract["path_window"]["reintegration_h1_close_utc_as_endpoint"] == "FORBIDDEN",
            "reintegration endpoint opened")
    require(contract["empty_path"]["action"] == "FAIL_CLOSED", "empty path weakened")
    require(contract["price_surface"]["allowed_extrema_primitives"] == ["mid_high", "mid_low"],
            "price primitive drift")
    require(contract["price_surface"]["mid_semantic"] ==
            "DESCRIPTIVE_ONLY_NOT_EXECUTION_PRICE", "mid execution laundering")
    require(contract["directions"]["HIGH"]["reintegrative"] == "DOWN", "HIGH reintegrative drift")
    require(contract["directions"]["HIGH"]["external"] == "UP", "HIGH external drift")
    require(contract["directions"]["LOW"]["reintegrative"] == "UP", "LOW reintegrative drift")
    require(contract["directions"]["LOW"]["external"] == "DOWN", "LOW external drift")
    require(contract["metrics"]["MAX_REINTEGRATIVE_EXCURSION"]["nonnegative"] is True,
            "reintegrative nonnegative weakened")
    require(contract["metrics"]["MAX_EXTERNAL_EXCURSION"]["nonnegative"] is True,
            "external nonnegative weakened")
    require(contract["gap_semantics"]["forward_fill"] == "FORBIDDEN", "forward fill opened")
    require(contract["gap_semantics"]["backfill"] == "FORBIDDEN", "backfill opened")
    require(contract["gap_semantics"]["interpolation"] == "FORBIDDEN", "interpolation opened")
    require(contract["gap_semantics"]["canonical_claim"] == "OBSERVED_EXTREMA_ONLY",
            "continuous extrema laundering")
    require(contract["first_real_aggregation_surface"]["quantile_method"] ==
            "HYNDMAN_FAN_TYPE_7", "quantile drift")
    require(contract["first_real_aggregation_surface"]["ecdf"] ==
            "EXACT_UNSMOOTHED_UNBINNED", "ECDF drift")
    require(contract["first_real_aggregation_surface"]["joint_relationship_between_excursions"] ==
            "NOT_AUTHORIZED", "joint metric opened")
    require(contract["subgroup_boundary"]["first_real_subgroups"] == [], "subgroup opened")
    require(contract["dependence_boundary"]["event_is_iid_observation"] is False,
            "IID laundering")
    require(contract["authority"]["real_excursion_execution"] is False,
            "07A execution authority altered")

    cases = breaker["adversarial_cases"]
    require(len(cases) == 40, "breaker count != 40")
    require(breaker["qualification_rule"]["required_case_count"] == 40, "required breaker count drift")
    require(all(x["expected"] == "HARD_FAIL" for x in cases), "breaker severity weakened")
    require(
        [x["case_id"] for x in cases] == [f"BEPD07A-B{i:02d}" for i in range(1, 41)],
        "breaker IDs drift",
    )

    require(freeze["freeze_scope"]["population_n"] == 472, "freeze population drift")
    require(freeze["freeze_scope"]["anchor"] == "take_h1_close_mid", "freeze anchor drift")
    require(freeze["freeze_scope"]["allowed_extrema_primitives"] == ["mid_high", "mid_low"],
            "freeze primitive drift")
    require(freeze["freeze_scope"]["subgroups"] == "NONE", "freeze subgroup drift")
    require(freeze["freeze_scope"]["joint_metrics"] == "NONE", "freeze joint metric drift")
    require(freeze["real_excursion_statistics_calculated"] is False, "07A result exposure drift")
    require(freeze["real_path_scan_executed"] is False, "07A path scan drift")

    for src_path in (args.runner, args.independent):
        src = Path(src_path).read_text(encoding="utf-8")
        require("take_h1_close_mid" in src, f"{src_path}: anchor missing")
        require("take_h1_close_utc" in src, f"{src_path}: confirmation missing")
        require('"mid_high"' in src and '"mid_low"' in src, f"{src_path}: extrema primitives missing")
        require("America/New_York" in src, f"{src_path}: NY week semantics missing")
        require("HYNDMAN_FAN_TYPE_7" in src, f"{src_path}: Type-7 identity missing")
        require("EXACT_UNSMOOTHED_UNBINNED" in src, f"{src_path}: ECDF identity missing")

    runner = Path(args.runner).read_text(encoding="utf-8")
    require("bisect_right(ts, start_exclusive_ms)" in runner, "strict post-take search semantics missing")
    require("bisect_left(ts, end_exclusive_ms)" in runner, "exclusive week-end search semantics missing")
    require("path_slice_indices(ts, t0, week_end)" in runner, "real scan does not use frozen path helper")
    require("event_level_derived_path_ledger_persisted" in runner,
            "derived-ledger disclosure missing")
    require('"subgroups": []' in runner, "no-subgroup disclosure missing")
    require("joint_excursion_metrics" in runner, "joint-metric boundary missing")

    print("BEPD07A_EXECUTABLE_EQUIVALENT_BREAKER_PASS")
    print("BEPD07A_BREAKER_CASES=40/40")
    print(f"BEPD07A_BREAKER_MODE={args.mode}")
    if args.mode == "pre-result":
        print("REAL_AP0_PATH_SCAN=NOT_EXECUTED")
        print("REAL_EXCURSION_STATISTICS=NOT_CALCULATED")
        print("REAL_EXCURSION_DISTRIBUTION_EXPOSURE=NO")
    else:
        print("REAL_AP0_PATH_SCAN=AUTHORIZED_ONLY_AFTER_THIS_PREFLIGHT")


if __name__ == "__main__":
    main()
