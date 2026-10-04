"""RVO-05 frozen integration breaker.

Materialized before src/rvo_05_cc02_bindings.py exists. The first run must be
an observed 25-case RED. After implementation, every case must preserve the
frozen expected result from the documentary contract.
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE" / "RVO-05-FROZEN-INTEGRATION-BREAKER-CONTRACT-V0.1.json"
EXPECTED_CASES = [f"RVO05-B{i:02d}" for i in range(1, 26)]

FROZEN = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert [x["id"] for x in FROZEN["cases"]] == EXPECTED_CASES
BY_ID = {x["id"]: x for x in FROZEN["cases"]}

def _runtime():
    try:
        return importlib.import_module("src.rvo_05_cc02_bindings")
    except ModuleNotFoundError:
        pytest.fail("RVO05_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)

def _expect(result, case_id):
    assert result["reason"] == BY_ID[case_id]["expected"], result
    return result

def _base_data():
    return {
        "status": "READY_FOR_EXACT_CLAIM",
        "contract": "ATDS_DATA_02_CLAIM_SCOPED_ADMISSION_V0_1",
        "admission_digest": "a" * 64,
        "binding_basis": {
            "claim_scope_id": "CC02_DESCRIPTIVE_MARKET_BEHAVIOR:RETROSPECTIVE_DESCRIPTIVE_ONLY:ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1",
            "dataset_identity": "USTECH_PROFILE_MINUTE_CORE_V0_1",
            "ap0_manifest_sha256": "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce",
            "dataset_file_set_digest": "b" * 64,
            "schema_identity": "c" * 64,
            "source_identity": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
            "transformer_blob": "42fcb38809a1cc0365cd4027fae5154e1d6d3b4f",
            "usage_envelope_id": "DATA01_CC02_AP1_RETROSPECTIVE_V0_1",
        },
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
        "rvo_authority": "NONE",
    }

def _activation(family):
    return {
        "claim_definition_ref": "claim:rvo05:cc02",
        "failure_mode_ref": "failure:" + family,
        "method_family_ref": family,
        "validity_scope_ref": "scope:rvo05:cc02",
        "assumption_set_ref": "assumptions:rvo05:cc02",
        "activation_reason": "pre-result exact first CC02 route",
        "activation_rule": "pre-result",
        "parameter_selection_policy": {"policy": "frozen"},
        "dependency_refs": ["P1-SPEC"],
        "activation_state": "ACTIVATED",
        "activation_digest": "sha256:" + (family[-1] * 64),
    }

def _bundle():
    return {
        "schema": "ATDS_RVO_05_SMF_METHOD_BUNDLE_V0_1",
        "claim_ref": "claim:rvo05:cc02",
        "m01_activation": _activation("M01"),
        "m03_activation": _activation("M03"),
        "qualified_implementation_blob": "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb",
        "p1_method_ref": "RVO05:SMF:M01+M03:EXACT",
        "bundle_digest": "d" * 64,
    }

@pytest.mark.parametrize("case_id", EXPECTED_CASES)
def test_rvo05_frozen_breakers(case_id):
    m = _runtime()
    data = _base_data()
    bundle = _bundle()

    if case_id == "RVO05-B01":
        return _expect(m.validate_data_admission(None, expected_digest="a"*64), case_id)
    if case_id == "RVO05-B02":
        return _expect(m.validate_data_admission(data, expected_digest="f"*64), case_id)
    if case_id == "RVO05-B03":
        data["binding_basis"]["dataset_identity"] = "SUBSTITUTED"
        return _expect(m.validate_data_admission(data, expected_digest="a"*64), case_id)
    if case_id == "RVO05-B04":
        return _expect(m.validate_authority_claims({"scientific": True}, source="DATA"), case_id)
    if case_id == "RVO05-B05":
        return _expect(m.validate_method_bundle({"p1_method_ref":"SMF:M03"}), case_id)
    if case_id == "RVO05-B06":
        return _expect(m.activate_required_smf(result_exposed=True), case_id)
    if case_id == "RVO05-B07":
        bundle["m03_activation"]["method_family_ref"] = "M05"
        return _expect(m.validate_method_bundle(bundle), case_id)
    if case_id == "RVO05-B08":
        bundle["qualified_implementation_blob"] = "0"*40
        return _expect(m.validate_method_bundle(bundle), case_id)
    if case_id == "RVO05-B09":
        return _expect(m.validate_p1_chain_identity({"evaluation_submission_id":"A","finding_evaluation_submission_id":"B"}), case_id)
    if case_id == "RVO05-B10":
        return _expect(m.preserve_native_status("SUPPORTED","REFUTED",owner="P1"), case_id)
    if case_id == "RVO05-B11":
        return _expect(m.preserve_native_status("ACTIVATED","PASS",owner="SMF"), case_id)
    if case_id == "RVO05-B12":
        return _expect(m.preserve_native_status("BLOCKED","FAIL",owner="DATA"), case_id)
    if case_id == "RVO05-B13":
        return _expect(m.preserve_native_status("UNKNOWN","PASS",owner="RVO"), case_id)
    if case_id == "RVO05-B14":
        return _expect(m.preserve_native_status("NOT_APPLICABLE","PASS",owner="TEMPORAL"), case_id)
    if case_id == "RVO05-B15":
        return _expect(m.validate_smf_route({"percentiles":[50,90,95,99]}, activated_families=["M01"]), case_id)
    if case_id == "RVO05-B16":
        return _expect(m.validate_smf_route({"percentiles":[50,90,95,99]}, activated_families=["M01","M03","M05"]), case_id)
    if case_id == "RVO05-B17":
        return _expect(m.validate_temporal_scope({"predictive":True}, "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"), case_id)
    if case_id == "RVO05-B18":
        return _expect(m.validate_reconstruction_claim(runtime_attestation=True,durable_inputs=False), case_id)
    if case_id == "RVO05-B19":
        return _expect(m.validate_pre_post_use(pre_digest="PRE",post_used_as_pre=True), case_id)
    if case_id == "RVO05-B20":
        return _expect(m.validate_global_claim("SCIENTIFIC_PASS"), case_id)
    if case_id == "RVO05-B21":
        return _expect(m.validate_authority_claims({"trading":True}, source="RVO"), case_id)
    if case_id == "RVO05-B22":
        return _expect(m.validate_target_execution_surface(data_family="AP0_PARQUET",p1_engine="BI5ResearchEngine"), case_id)
    if case_id == "RVO05-B23":
        return _expect(m.validate_p1_smf_procedure_binding(
            p1_method_ref=bundle["p1_method_ref"],
            procedure_ref="WRONG",
            smf_bundle=bundle,
            smf_result_binding={"procedure_ref":"EXPECTED","result_digest":"e"*64},
        ), case_id)
    if case_id == "RVO05-B24":
        return _expect(m.validate_smf_route({"percentiles":[50]}, activated_families=["M03"]), case_id)
    if case_id == "RVO05-B25":
        return _expect(m.validate_surface_generalization(
            qualified_surface="SYNTHETIC_BI5",
            target_surface="AP0_PARQUET",
        ), case_id)
    raise AssertionError(case_id)
