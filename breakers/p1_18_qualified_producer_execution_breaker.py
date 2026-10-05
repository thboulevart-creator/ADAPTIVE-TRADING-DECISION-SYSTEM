"""Executable P1-18 breaker derived from the frozen P1-17 32-case contract.

This file is materialized before P1.12C exists. The first observed run MUST be
32 failures carrying P1_12C_RUNTIME_ABSENT_EXPECTED_RED. After implementation,
the exact case IDs and frozen expected reasons remain unchanged.
"""
from __future__ import annotations

import copy
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FROZEN_PATH = ROOT / "GOVERNANCE" / "P1-17-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"
FROZEN = json.loads(FROZEN_PATH.read_text(encoding="utf-8"))
EXPECTED_IDS = [f"P117-B{i:02d}" for i in range(1, 33)]
assert [row["id"] for row in FROZEN["cases"]] == EXPECTED_IDS
BY_ID = {row["id"]: row for row in FROZEN["cases"]}

def _runtime():
    try:
        return importlib.import_module("src.p1_12c_qualified_producer_execution")
    except ModuleNotFoundError:
        pytest.fail("P1_12C_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)

def _expect(out, case_id):
    assert out["reason"] == BY_ID[case_id]["expected"], out
    assert out["status"] in {"BLOCKED", "REJECTED"}, out

def _plan():
    return {
        "experiment_execution_input_id":"QEI-" + "1"*32,
        "execution_binding_id":"EEB-" + "2"*32,
        "experiment_spec_id":"EXS-" + "3"*32,
        "request_id":"FR-" + "4"*32,
        "revision_id":"REV-" + "5"*32,
        "audit_id":"AUD-" + "6"*32,
        "scope_id":"SCOPE-" + "7"*32,
        "data02_admission_digest":"a"*64,
        "claim_scope_id":"CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1",
        "dataset_identity":"USTECH_PROFILE_MINUTE_CORE_V0_1",
        "dataset_file_set_digest":"b"*64,
        "producer_id":"ATDS_P1_18_SYNTHETIC_PRODUCER_V0_1",
        "producer_code_blob":"c"*40,
        "producer_entrypoint":"__main__",
        "producer_semantic_parameter_digest":"d"*64,
        "producer_invocation_contract_digest":"e"*64,
        "runtime_lock_digest":"f"*64,
        "expected_output_schema":"ATDS_P1_18_SYNTHETIC_PRODUCER_OUTPUT_V0_1",
        "expected_output_status":"SYNTHETIC_COMPLETE",
        "maximum_output_bytes":1048576,
        "result_exposed":False,
        "temporal_scope":"RETROSPECTIVE_DESCRIPTIVE_ONLY",
        "oos_consumption":False,
        "owner_rewrite":False,
        "path_as_identity":False,
    }

def _result(m, plan):
    base = {
        "producer_execution_plan_digest":"9"*64,
        "experiment_execution_input_id":plan["experiment_execution_input_id"],
        "execution_binding_id":plan["execution_binding_id"],
        "experiment_spec_id":plan["experiment_spec_id"],
        "dataset_identity":plan["dataset_identity"],
        "dataset_file_set_digest_before":plan["dataset_file_set_digest"],
        "dataset_file_set_digest_after":plan["dataset_file_set_digest"],
        "producer_id":plan["producer_id"],
        "producer_code_blob":plan["producer_code_blob"],
        "producer_parameter_digest":plan["producer_semantic_parameter_digest"],
        "runtime_lock_digest":plan["runtime_lock_digest"],
        "execution_status":"EXECUTED",
        "exit_code":0,
        "output_schema":plan["expected_output_schema"],
        "output_status":plan["expected_output_status"],
        "output_size_bytes":12,
        "output_sha256":"1"*64,
        "data02_result_binding_digest":"2"*64,
        "producer_stdout_digest":"3"*64,
        "producer_stderr_digest":"4"*64,
        "reconstruction_class":"EVIDENCE_REPLAY",
        "reconstruction_descriptor_digest":"5"*64,
        "producer_mutated_source":False,
        "path_as_identity":False,
    }
    base["result_identity"] = m.compute_result_identity(base)
    return base

@pytest.mark.parametrize("case_id", EXPECTED_IDS)
def test_p1_18_frozen_breakers(case_id):
    m = _runtime()
    plan = _plan()

    if case_id == "P117-B01":
        candidate=copy.deepcopy(plan); candidate.pop("producer_code_blob")
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B02":
        result=_result(m,plan); result.pop("dataset_identity")
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B03":
        candidate=copy.deepcopy(plan); candidate["dataset_identity"]="SUBSTITUTED"
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B04":
        candidate=copy.deepcopy(plan); candidate["producer_semantic_parameter_digest"]="0"*64
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B05":
        candidate=copy.deepcopy(plan); candidate["producer_code_blob"]="0"*40
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B06":
        result=_result(m,plan); result["observed_output_sha256"]="0"*64
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B07":
        result=_result(m,plan); result["output_sha256"]="0"*64
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B08":
        candidate=copy.deepcopy(plan); candidate["experiment_spec_id"]="EXS-"+"0"*32
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B09":
        result=_result(m,plan); result.pop("execution_binding_id")
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B10":
        return _expect(m.validate_boundary_claim("PATH_OR_FILENAME_AUTHORITY"), case_id)
    if case_id == "P117-B11":
        return _expect(m.validate_boundary_claim("RVO_PRODUCER_AUTHORITY"), case_id)
    if case_id == "P117-B12":
        return _expect(m.validate_boundary_claim("DATA_PASS_TO_EXECUTION_PASS"), case_id)
    if case_id == "P117-B13":
        return _expect(m.validate_boundary_claim("EXECUTION_TO_P1_FINDING"), case_id)
    if case_id == "P117-B14":
        return _expect(m.validate_boundary_claim("RESULT_TO_SCIENTIFIC_SUPPORT"), case_id)
    if case_id == "P117-B15":
        return _expect(m.validate_boundary_claim("RUNTIME_ATTESTATION_TO_DURABLE_RECONSTRUCTION"), case_id)
    if case_id == "P117-B16":
        return _expect(m.validate_boundary_claim("EXTERNAL_RESULT_WITHOUT_REPLAY_EVIDENCE"), case_id)
    if case_id == "P117-B17":
        candidate=copy.deepcopy(plan); candidate["result_exposed"]=True
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B18":
        return _expect(m.validate_boundary_claim("DUPLICATE_AP1_LOGIC_INSIDE_P1"), case_id)
    if case_id == "P117-B19":
        return _expect(m.validate_boundary_claim("RELABEL_AP0_AS_BI5"), case_id)
    if case_id == "P117-B20":
        result=_result(m,plan); result["producer_mutated_source"]=True
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B21":
        candidate=copy.deepcopy(plan); candidate["temporal_scope"]="HISTORICAL_TRADABILITY"
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B22":
        candidate=copy.deepcopy(plan); candidate["oos_consumption"]=True
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B23":
        candidate=copy.deepcopy(plan); candidate["owner_rewrite"]=True
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B24":
        return _expect(m.validate_boundary_claim("EXECUTION_GRANTS_TRADING_OR_CAPITAL"), case_id)
    if case_id == "P117-B25":
        return _expect(m.validate_boundary_claim("FORGE_P1_12B_RESULT"), case_id)
    if case_id == "P117-B26":
        return _expect(m.validate_boundary_claim("BYPASS_P1_13B_TYPE_CONTRACT"), case_id)
    if case_id == "P117-B27":
        result=_result(m,plan); result["output_schema"]="WRONG"
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B28":
        candidate=copy.deepcopy(plan); candidate["runtime_lock_digest"]="0"*64
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B29":
        return _expect(m.validate_boundary_claim("DIGEST_ONLY_EXTERNAL_AUTHORITY"), case_id)
    if case_id == "P117-B30":
        candidate=copy.deepcopy(plan); candidate["path_as_identity"]=True
        return _expect(m.validate_plan_candidate(candidate, plan), case_id)
    if case_id == "P117-B31":
        result=_result(m,plan); result["dataset_file_set_digest_after"]="0"*64
        return _expect(m.validate_result_candidate(result, plan), case_id)
    if case_id == "P117-B32":
        result=_result(m,plan); result["output_status"]="NOT_COMPLETE"
        return _expect(m.validate_result_candidate(result, plan), case_id)
    raise AssertionError(case_id)
