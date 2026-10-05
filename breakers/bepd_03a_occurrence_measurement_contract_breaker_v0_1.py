from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

AUTH = Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-AUTHORIZATION-2026-10-05.md")
DIMS = Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
CONTRACT = Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
ACT = Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
BREAKER_CONTRACT = Path("GOVERNANCE/BEPD-03A-FROZEN-OCCURRENCE-MEASUREMENT-BREAKER-CONTRACT-V0.1.json")

EXPECTED_BLOBS = {
    AUTH: "03d1cf01b41f662280f00c8271bab411b5754b3a",
    DIMS: "b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
    CONTRACT: "e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
    ACT: "53d33074038fa9d971b4672b1d981589da020a1e",
    BREAKER_CONTRACT: "d9c3ce44dbc27703cd1cde007a5f806beb01f221",
}

NY = ZoneInfo("America/New_York")


class BreakerFailure(AssertionError):
    pass


def fail(code: str) -> None:
    print(f"BEPD_03A_BREAKER_FAIL:{code}")
    raise SystemExit(1)


def eq(actual, expected, code: str) -> None:
    if actual != expected:
        raise BreakerFailure(f"{code}: expected={expected!r} actual={actual!r}")


def require(condition: bool, code: str) -> None:
    if not condition:
        raise BreakerFailure(code)


def git_blob(root: Path, rel: Path) -> str:
    cp = subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"HEAD:{rel.as_posix()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if cp.returncode != 0:
        raise BreakerFailure(f"MISSING_BOUND_OBJECT:{rel.as_posix()}")
    return cp.stdout.strip()


def git_json(root: Path, rel: Path) -> dict:
    cp = subprocess.run(
        ["git", "-C", str(root), "show", f"HEAD:{rel.as_posix()}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise BreakerFailure(f"MISSING_BOUND_OBJECT:{rel.as_posix()}")
    return json.loads(cp.stdout.decode("utf-8"))


def pooled_rate(rows: list[dict]) -> float:
    if not rows:
        raise BreakerFailure("EMPTY_SYNTHETIC_ROWS")
    return sum(1 for r in rows if r["swept_this_week"]) / len(rows)


def mean_weekly_rate(rows: list[dict]) -> float:
    weeks: dict[str, list[dict]] = {}
    for row in rows:
        weeks.setdefault(row["target_week_id"], []).append(row)
    vals = [sum(1 for r in xs if r["swept_this_week"]) / len(xs) for xs in weeks.values()]
    return sum(vals) / len(vals)


def age_band(age: int) -> str:
    if age == 1:
        return "AGE_1"
    if age == 2:
        return "AGE_2"
    if 3 <= age <= 4:
        return "AGE_3_4"
    if 5 <= age <= 8:
        return "AGE_5_8"
    if 9 <= age <= 16:
        return "AGE_9_16"
    if 17 <= age <= 32:
        return "AGE_17_32"
    if 33 <= age <= 64:
        return "AGE_33_64"
    if age >= 65:
        return "AGE_65_PLUS"
    raise ValueError("AGE_OUT_OF_DOMAIN")


def month_position(target_week_id: str) -> str:
    d = date.fromisoformat(target_week_id)
    return "EARLY_01_15" if d.day <= 15 else "LATE_16_EOM"


def target_month(target_week_id: str) -> int:
    return date.fromisoformat(target_week_id).month


def target_year(target_week_id: str) -> int:
    return date.fromisoformat(target_week_id).year


def take_day_ny(iso_utc: str) -> str:
    d = datetime.fromisoformat(iso_utc).astimezone(NY)
    names = {
        6: "SUNDAY_OPEN",
        0: "MONDAY",
        1: "TUESDAY",
        2: "WEDNESDAY",
        3: "THURSDAY",
        4: "FRIDAY",
    }
    if d.weekday() not in names:
        raise ValueError("SATURDAY_TAKE_FORBIDDEN")
    return names[d.weekday()]


def test_bindings(root: Path) -> tuple[dict, dict, dict, dict]:
    for rel, expected in EXPECTED_BLOBS.items():
        eq(git_blob(root, rel), expected, f"GIT_BLOB:{rel.as_posix()}")
    dims = git_json(root, DIMS)
    contract = git_json(root, CONTRACT)
    act = git_json(root, ACT)
    bc = git_json(root, BREAKER_CONTRACT)
    return dims, contract, act, bc


def test_breaker_contract(bc: dict) -> None:
    eq(bc["status"], "FROZEN_PRE_RESULT_BREAKER_CANDIDATE", "BREAKER_STATUS")
    ids = [x["id"] for x in bc["cases"]]
    eq(ids, [f"BEPD03A-B{i:02d}" for i in range(1, 31)], "CASE_IDS")
    eq(len(set(ids)), 30, "CASE_UNIQUENESS")
    eq(bc["frozen_principles"]["primary_estimator"], "sum(swept_this_week) / count(LEVEL_WEEK_OPPORTUNITY)", "PRIMARY_ESTIMATOR")
    eq(bc["frozen_principles"]["dependence_key"], "target_week_id", "DEPENDENCE_KEY")
    eq(bc["frozen_principles"]["cross_products"], [], "CROSS_PRODUCTS")
    eq(bc["authority"]["real_occurrence_calculation"], False, "AUTH_REAL_RESULT")
    eq(bc["authority"]["occurrence_map"], False, "AUTH_OCC_MAP")
    eq(bc["authority"]["response_map"], False, "AUTH_RESPONSE_MAP")


def test_estimand(contract: dict) -> None:
    p = contract["primary_estimand"]
    eq(p["outcome"], "Y_i = 1 if swept_this_week=true else 0", "OUTCOME")
    eq(p["numerator"], "sum_i Y_i across all eligible opportunity rows", "NUMERATOR")
    eq(p["denominator"], "N = count of all eligible opportunity rows", "DENOMINATOR")
    eq(p["aggregation"], "ratio of total events to total opportunities, not mean of weekly rates", "AGGREGATION")

    rows = [
        {"target_week_id": "2026-01-05", "swept_this_week": True},
        {"target_week_id": "2026-01-05", "swept_this_week": False},
        {"target_week_id": "2026-01-05", "swept_this_week": False},
        {"target_week_id": "2026-01-12", "swept_this_week": True},
    ]
    eq(pooled_rate(rows), 0.5, "SYNTHETIC_POOLED_RATIO")
    require(mean_weekly_rate(rows) != pooled_rate(rows), "MEAN_WEEKLY_RATE_MUST_DIFFER_SYNTHETIC")


def test_dependence(contract: dict) -> None:
    d = contract["dependence_model"]
    eq(d["within_target_week"], "STRUCTURALLY_DEPENDENT", "WITHIN_WEEK_DEPENDENCE")
    eq(d["dependence_key"], "target_week_id", "DEPENDENCE_KEY_CONTRACT")
    eq(d["iid_opportunity_rows"], False, "IID_OPPORTUNITY")
    eq(d["repeated_level_across_weeks"], "TEMPORAL_REPEATED_MEASURES_PRESENT_UNTIL_CONSUMPTION_OR_CENSORING", "REPEATED_LEVEL")


def view_map(dims: dict) -> dict:
    return {x["id"]: x for x in dims["views"]}


def test_dimensions(dims: dict) -> None:
    views = view_map(dims)
    eq(set(views), {"V00_GLOBAL_ALL_SIDES","V01_SIDE","V02_TARGET_MONTH","V03_TARGET_MONTH_POSITION","V04_TARGET_YEAR","V05_LEVEL_AGE_BAND","V06_TAKE_LOCAL_DAY"}, "VIEW_SET")
    eq(dims["combination_policy"]["initial_occurrence_map"], "MARGINAL_ONLY", "MARGINAL_ONLY")
    eq(dims["combination_policy"]["authorized_cross_products"], [], "NO_CROSS_PRODUCTS")
    eq(views["V01_SIDE"]["categories"], ["HIGH","LOW"], "SIDE_CATEGORIES")
    eq(views["V02_TARGET_MONTH"]["categories"], list(range(1,13)), "MONTH_CATEGORIES")
    eq(views["V03_TARGET_MONTH_POSITION"]["categories"], ["EARLY_01_15","LATE_16_EOM"], "MONTH_POSITION_CATEGORIES")
    eq(views["V06_TAKE_LOCAL_DAY"]["role"], "OUTCOME_CONDITIONAL_EVENT_TIMING_VIEW_NOT_AN_OCCURRENCE_DENOMINATOR", "TAKE_DAY_ROLE")
    require(views["V06_TAKE_LOCAL_DAY"]["occurrence_rate_language_forbidden"] is True, "TAKE_DAY_RATE_FORBIDDEN")

    eq(target_month("2026-01-12"), 1, "MONTH_DERIVATION")
    eq(target_year("2026-01-12"), 2026, "YEAR_DERIVATION")
    eq(month_position("2026-01-15"), "EARLY_01_15", "DAY15_BOUNDARY")
    eq(month_position("2026-01-16"), "LATE_16_EOM", "DAY16_BOUNDARY")

    checks = {
        1:"AGE_1",2:"AGE_2",3:"AGE_3_4",4:"AGE_3_4",5:"AGE_5_8",8:"AGE_5_8",
        9:"AGE_9_16",16:"AGE_9_16",17:"AGE_17_32",32:"AGE_17_32",
        33:"AGE_33_64",64:"AGE_33_64",65:"AGE_65_PLUS",130:"AGE_65_PLUS"
    }
    for age, expected in checks.items():
        eq(age_band(age), expected, f"AGE_BAND_{age}")

    eq(take_day_ny("2026-01-11T23:59:00+00:00"), "SUNDAY_OPEN", "TAKE_DAY_SUNDAY")
    eq(take_day_ny("2026-01-16T20:59:00+00:00"), "FRIDAY", "TAKE_DAY_FRIDAY")

    rp = dims["reporting_policy"]
    require(rp["zero_event_groups_must_be_reported"] is True, "ZERO_GROUP_REPORT")
    require(rp["low_support_groups_must_be_reported"] is True, "LOW_SUPPORT_REPORT")
    require(rp["sort_policy"] == "canonical category order, never by occurrence value", "SORT_POLICY")
    require(rp["best_worst_labels_forbidden"] is True, "BEST_WORST_FORBIDDEN")


def test_uncertainty(contract: dict, act: dict) -> None:
    u = contract["uncertainty_policy"]
    eq(u["historical_fixed_corpus"]["state"], "EXACT_DESCRIPTIVE_SUMMARY", "FIXED_CORPUS_STATE")
    eq(u["historical_fixed_corpus"]["inferential_interval_required"], False, "FIXED_CORPUS_CI")
    g = u["process_generalization"]
    eq(g["state"], "BLOCKED_UNTIL_SEPARATE_ACTIVATION", "GENERALIZATION_STATE")
    eq(g["selected_method_family"], "SMF_M05", "M05_FAMILY")
    eq(g["selected_scheme"], "MOVING_BLOCK", "M05_SCHEME")
    require(g["within_week_dependence_preserved"] is True, "M05_CLUSTER_PRESERVATION")
    require(g["serial_order_preserved_within_blocks"] is True, "M05_SERIAL_ORDER")
    eq(g["no_auto_fallback"], "IID bootstrap, naive binomial interval, or opportunity-row bootstrap may not be substituted", "NO_FALLBACK")

    a = act["activation_record"]
    eq(a["method_family_ref"], "M05", "ACT_M05")
    eq(a["activation_state"], "BLOCKED", "ACT_BLOCKED")
    eq(a["parameter_selection_policy"]["scheme"], "MOVING_BLOCK", "ACT_SCHEME")
    for name in ("interval_method","confidence_level","replications","seed","block_length"):
        eq(a["parameter_selection_policy"][name], "HUMAN_ADJUDICATION_REQUIRED", f"PARAM_BLOCKED_{name}")
    blockers = set(act["blockers"])
    require("UNRESOLVED_NONSTATIONARITY_STATUS" in blockers, "NONSTATIONARITY_BLOCKER")
    require("MATERIAL_BOOTSTRAP_PARAMETERS_NOT_HUMAN_ADJUDICATED" in blockers, "PARAMETER_BLOCKER")
    require("RATIO_OF_SUMS_MOVING_BLOCK_EXECUTABLE_NOT_SEPARATELY_QUALIFIED" in blockers, "EXECUTABLE_SCOPE_BLOCKER")


def test_multiplicity(contract: dict) -> None:
    m = contract["multiplicity_policy"]
    eq(m["initial_map_type"], "DESCRIPTIVE_MARGINAL_ONLY", "MULTIPLICITY_MAP_TYPE")
    eq(m["hypothesis_tests"], 0, "NO_HYPOTHESIS_TESTS")
    eq(m["p_values"], False, "NO_PVALUES")
    eq(m["significance_labels"], False, "NO_SIGNIFICANCE")
    eq(m["cross_products"], [], "NO_CROSS_PRODUCTS_CONTRACT")
    eq(m["ranking"], False, "NO_RANKING")
    eq(m["complete_reporting"], True, "COMPLETE_REPORTING")
    eq(m["interpretation"], "differences across preregistered cells are descriptive heterogeneity only", "DESCRIPTIVE_ONLY")


def test_authority(contract: dict) -> None:
    forbidden = set(contract["forbidden"])
    for phrase in (
        "calculate real occurrence results under BEPD-03A",
        "post-hoc subgroup creation",
        "post-hoc age binning",
        "cross-product fishing",
        "ranking months/days/ages",
        "naive IID binomial inference over opportunity rows",
        "bootstrap individual opportunity rows",
        "infer future probability from historical rate",
        "Response Map",
        "Occurrence x Response",
        "edge/strategy/PnL",
    ):
        require(phrase in forbidden, f"FORBIDDEN_MISSING:{phrase}")
    require(contract["stop_boundary"].startswith("STOP_BEFORE_ANY_REAL_OCCURRENCE"), "STOP_BOUNDARY")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()

    try:
        dims, contract, act, bc = test_bindings(root)
        test_breaker_contract(bc)
        test_estimand(contract)
        test_dependence(contract)
        test_dimensions(dims)
        test_uncertainty(contract, act)
        test_multiplicity(contract)
        test_authority(contract)
    except (BreakerFailure, KeyError, ValueError, json.JSONDecodeError) as exc:
        fail(str(exc))

    print("BEPD_03A_OCCURRENCE_MEASUREMENT_BREAKER_PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
