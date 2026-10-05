from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable

ROOT_DEFAULT = Path(__file__).resolve().parents[1]
CALC_REL = Path("tools/bepd_04b_same_week_reintegration_response_v0_1.py")
FIXTURE_REL = Path("tests/fixtures/bepd_04b_same_week_reintegration_synthetic_v0_1.json")
EXPECTED_CASE_IDS = [f"B04A-B{i:02d}" for i in range(1, 21)]

class BreakerFailure(AssertionError):
    pass


def load_calc(root: Path):
    path = root / CALC_REL
    spec = importlib.util.spec_from_file_location("bepd04b_calc", path)
    if spec is None or spec.loader is None:
        raise BreakerFailure("CALCULATOR_IMPORT_SPEC")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def enrich(row: dict[str, Any], run_id: str) -> dict[str, Any]:
    z = dict(row)
    z["schema_version"] = "ATDS_BEPD_01D_HISTORICAL_LEDGER_SCHEMA_V0_1"
    z["run_id"] = run_id
    return z


def expect_fail(case_id: str, fn: Callable[[], Any], failure_type: type[Exception]) -> str:
    try:
        fn()
    except failure_type:
        return "HARD_FAIL"
    except Exception as exc:
        raise BreakerFailure(f"{case_id}:WRONG_FAILURE:{type(exc).__name__}:{exc}") from exc
    raise BreakerFailure(f"{case_id}:MUTATION_SURVIVED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT_DEFAULT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        mod = load_calc(root)
        fx = json.loads((root / FIXTURE_REL).read_text(encoding="utf-8"))
        base = fx["cases"][2]["rows"]
        syn_context = {
            "execution_scope": "SYNTHETIC_QUALIFICATION",
            "source_ledger_blob": "SYNTHETIC_BEPD04B_LEDGER_V0_1",
            "source_run_id": "SYNTHETIC_BEPD04B_RUN_V0_1",
        }
        syn_rows = [enrich(x, syn_context["source_run_id"]) for x in base]
        base_result = mod.summarize_rows(syn_rows, syn_context)
        outcomes: dict[str, str] = {}

        outcomes["B04A-B01"] = expect_fail("B04A-B01", lambda: mod._validate_context({"execution_scope":"REAL_AUTHORIZED","source_ledger_blob":"WRONG","source_run_id":mod.REAL_RUN_ID,"real_execution_authorized":True}), mod.ResponseFailure)
        outcomes["B04A-B02"] = expect_fail("B04A-B02", lambda: mod.summarize_rows(syn_rows, syn_context, options={"population":"subset"}), mod.ResponseFailure)
        def b03():
            r=copy.deepcopy(base_result); r["reintegration_false_count"]=0; mod.validate_result(r)
        outcomes["B04A-B03"] = expect_fail("B04A-B03", b03, mod.ResponseFailure)
        outcomes["B04A-B04"] = expect_fail("B04A-B04", lambda: mod.summarize_rows(syn_rows, syn_context, options={"denominator":"LEVEL_WEEK_OPPORTUNITY"}), mod.ResponseFailure)
        outcomes["B04A-B05"] = expect_fail("B04A-B05", lambda: mod.summarize_rows(syn_rows, syn_context, options={"take_comparator":">="}), mod.ResponseFailure)
        outcomes["B04A-B06"] = expect_fail("B04A-B06", lambda: mod.summarize_rows(syn_rows, syn_context, options={"reintegration_comparator":"<="}), mod.ResponseFailure)
        outcomes["B04A-B07"] = expect_fail("B04A-B07", lambda: mod.summarize_rows(syn_rows, syn_context, options={"allow_same_bar":True}), mod.ResponseFailure)
        outcomes["B04A-B08"] = expect_fail("B04A-B08", lambda: mod.summarize_rows(syn_rows, syn_context, options={"response_horizon":"AFTER_TARGET_WEEK"}), mod.ResponseFailure)
        def b09():
            rows=copy.deepcopy(syn_rows); rows[0].pop("sweep_cluster_id"); mod.summarize_rows(rows, syn_context)
        outcomes["B04A-B09"] = expect_fail("B04A-B09", b09, mod.ResponseFailure)
        def b10():
            r=copy.deepcopy(base_result); r["dependence_statement"]="EVENT = IID OBSERVATION"; mod.validate_result(r)
        outcomes["B04A-B10"] = expect_fail("B04A-B10", b10, mod.ResponseFailure)
        outcomes["B04A-B11"] = expect_fail("B04A-B11", lambda: mod.summarize_rows(syn_rows, syn_context, options={"false_semantic":"price never reintegrated"}), mod.ResponseFailure)
        def b12():
            r=copy.deepcopy(base_result); r["interpretation"]="TRADE_SUCCESS_RATE"; mod.validate_result(r)
        outcomes["B04A-B12"] = expect_fail("B04A-B12", b12, mod.ResponseFailure)
        outcomes["B04A-B13"] = expect_fail("B04A-B13", lambda: mod.summarize_rows(syn_rows, syn_context, options={"execution_price":"mid"}), mod.ResponseFailure)
        outcomes["B04A-B14"] = expect_fail("B04A-B14", lambda: mod.summarize_rows(syn_rows, syn_context, options={"group_by":"side"}), mod.ResponseFailure)
        outcomes["B04A-B15"] = expect_fail("B04A-B15", lambda: mod.summarize_rows(syn_rows, syn_context, options={"group_by":"take_day_ny"}), mod.ResponseFailure)
        outcomes["B04A-B16"] = expect_fail("B04A-B16", lambda: mod.summarize_rows(syn_rows, syn_context, options={"estimand":"close_displacement"}), mod.ResponseFailure)
        outcomes["B04A-B17"] = expect_fail("B04A-B17", lambda: mod.summarize_rows(syn_rows, syn_context, options={"response_horizon":"+24H"}), mod.ResponseFailure)
        outcomes["B04A-B18"] = expect_fail("B04A-B18", lambda: mod.summarize_rows(syn_rows, syn_context, options={"m05":"ACTIVATE"}), mod.ResponseFailure)
        def b19():
            r=copy.deepcopy(base_result); r["interpretation"]="FUTURE_PREDICTIVE_CAUSAL_EDGE"; mod.validate_result(r)
        outcomes["B04A-B19"] = expect_fail("B04A-B19", b19, mod.ResponseFailure)
        def b20():
            r=copy.deepcopy(base_result); r["strategy"]="AUTHORIZED"; mod.validate_result(r)
        outcomes["B04A-B20"] = expect_fail("B04A-B20", b20, mod.ResponseFailure)

        if list(outcomes) != EXPECTED_CASE_IDS:
            raise BreakerFailure("CASE_ID_DRIFT")
        if any(v != "HARD_FAIL" for v in outcomes.values()):
            raise BreakerFailure("CASE_NOT_HARD_FAIL")
        print(json.dumps({"status":"BEPD04B_EXECUTABLE_BREAKER_PASS","cases":outcomes}, sort_keys=True))
        return 0
    except (BreakerFailure, mod.ResponseFailure if 'mod' in locals() else Exception, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"BEPD04B_EXECUTABLE_BREAKER_FAIL:{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
