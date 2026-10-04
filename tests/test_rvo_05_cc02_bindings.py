"""RVO-05 positive/negative integration qualification tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src import rvo_05_cc02_bindings as rvo05
from src.data import claim_scoped_admission as data02
from src.linked_experiment_execution import run_linked_experiment
from tests.data_02_fixture import make_package as make_data02_package
from tests.rvo_05_fixture import build_positive_p1_smf_chain, build_target_ap0_preexecution_probe

ROOT = Path(__file__).resolve().parents[1]

def test_rvo05_01_exact_smf_route_is_m01_plus_m03_only():
    out = rvo05.validate_smf_route(
        {"percentiles":[50,90,95,99]},
        activated_families=["M01","M03"],
    )
    assert out["status"] == "READY"
    assert out["required"] == ["M01","M03"]

def test_rvo05_02_required_activations_are_real_smf_owner_records():
    acts = rvo05.activate_required_smf(result_exposed=False)
    assert acts["M01"]["owner_contract"] == "ATDS_SMF03_CORE_FOUNDATION_V0_1"
    assert acts["M03"]["owner_contract"] == "ATDS_SMF03_CORE_FOUNDATION_V0_1"
    assert acts["M01"]["owner_payload"]["method_family_ref"] == "M01"
    assert acts["M03"]["owner_payload"]["method_family_ref"] == "M03"
    assert acts["M01"]["owner_payload"]["activation_state"] == "ACTIVATED"
    assert acts["M03"]["owner_payload"]["activation_state"] == "ACTIVATED"

def test_rvo05_03_method_bundle_is_deterministic_and_exact():
    a = rvo05.build_method_bundle(rvo05.activate_required_smf(result_exposed=False))
    b = rvo05.build_method_bundle(rvo05.activate_required_smf(result_exposed=False))
    assert a == b
    assert a["qualified_implementation_blob"] == "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
    assert a["p1_method_ref"].startswith("RVO05:SMF:M01+M03:")
    assert rvo05.validate_method_bundle(a)["status"] == "READY"

def test_rvo05_04_m03_executes_owner_method_only_after_activation():
    bundle = rvo05.build_method_bundle(rvo05.activate_required_smf(result_exposed=False))
    out = rvo05.execute_m03(bundle, [0.2,0.2], probabilities=(0.5,0.9,0.95,0.99))
    assert out["method_family"] == "M03"
    assert out["qualified_implementation_blob"] == "b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb"
    assert out["owner_result"]["quantiles"]["0.5"] == pytest.approx(0.2)
    assert out["procedure_ref"].endswith("#ecdf_quantiles")
    assert len(out["procedure_sha256"]) == 64
    assert len(out["result_digest"]) == 64

def test_rvo05_05_exact_data02_synthetic_admission_binds(tmp_path: Path):
    package = make_data02_package(tmp_path)
    admission = data02.evaluate_synthetic(package)
    out = rvo05.validate_data_admission(admission, expected_digest=admission["admission_digest"])
    assert out["status"] == "READY"
    assert out["dataset_identity"] == "USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert out["scientific_authority"] is False
    assert out["rvo_authority"] == "NONE"

def test_rvo05_06_real_p1_downstream_plus_smf_chain_binds_synthetically(tmp_path: Path):
    case = build_positive_p1_smf_chain(tmp_path)
    assert case["bound_chain"]["status"] == "READY"
    assert case["bound_chain"]["reason"] == "P1_DOWNSTREAM_CHAIN_BOUND"
    assert case["finding"].finding_status == "SUPPORTED"
    assert case["submission"].method_ref == case["bundle"]["p1_method_ref"]
    assert case["finding"].method_ref == case["bundle"]["p1_method_ref"]
    assert case["provenance"].derivations[0].procedure_ref == case["smf_result"]["procedure_ref"]
    assert case["provenance"].derivations[0].procedure_sha256 == case["smf_result"]["procedure_sha256"]
    assert case["bound_chain"]["scientific_authority"] is False
    assert case["bound_chain"]["rvo_authority"] == "NONE"

def test_rvo05_07_p1_smf_synthetic_chain_is_bi5_scoped_not_ap0(tmp_path: Path):
    case = build_positive_p1_smf_chain(tmp_path)
    out = rvo05.validate_surface_generalization(
        qualified_surface="SYNTHETIC_BI5",
        target_surface="AP0_PARQUET",
    )
    assert out["status"] == "BLOCKED"
    assert out["reason"] == "REJECT_SYNTHETIC_SURFACE_GENERALIZATION"
    assert case["bound_chain"]["status"] == "READY"

def test_rvo05_08_target_ap0_identity_can_bind_preexecution_but_owner_capability_blocks(tmp_path: Path):
    case = build_target_ap0_preexecution_probe(tmp_path)
    out = case["compatibility"]
    assert case["admission"]["status"] == "READY_FOR_EXACT_CLAIM"
    assert out["identity_binding_status"] == "PASS"
    assert out["status"] == "BLOCKED_OWNER_GAP"
    assert out["reason"] == "BLOCKED_P1_TARGET_EXECUTION_SURFACE_UNSUPPORTED"
    assert out["p1_engine"] == "BI5ResearchEngine"

def test_rvo05_09_actual_p1_linked_execution_rejects_ap0_parquet_surface(tmp_path: Path):
    case = build_target_ap0_preexecution_probe(tmp_path)
    with pytest.raises(ValueError, match="at least one BI5 file"):
        run_linked_experiment(case["qualified_input"])

def test_rvo05_10_real_data02_receipt_does_not_close_p1_execution_gap():
    receipt = json.loads(
        (ROOT / "reports/program/2026-10-04-DATA-02-REAL-AP0-READ-ONLY-ADMISSION-RECEIPT-V0.1.json")
        .read_text(encoding="utf-8")
    )
    out = rvo05.readiness_verdict(
        data02_real_status=receipt["status"],
        p1_smf_binding_status="QUALIFIED_SYNTHETIC_BI5_ONLY",
        target_execution_status="BLOCKED",
    )
    assert receipt["status"] == "PASS_REAL_DATA_ADMISSION"
    assert out["status"] == "BLOCKED_OWNER_GAP"
    assert out["next_owner"] == "P1/RESEARCH_EXECUTION"
    assert out["real_cc02_authorized"] is False

def test_rvo05_11_temporal_n_a_is_valid_only_for_exact_retrospective_scope():
    ok = rvo05.validate_temporal_scope(
        {"predictive":False,"historical":False,"oos":False,"profitability":False},
        "NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
    )
    assert ok["status"] == "READY"
    blocked = rvo05.validate_temporal_scope(
        {"historical":True},
        "NOT_APPLICABLE_WITH_EXPLICIT_BASIS",
    )
    assert blocked["reason"] == "BLOCKED_TEMPORAL_OWNER_REQUIRED"

def test_rvo05_12_no_authority_or_global_pass_is_created():
    assert rvo05.validate_authority_claims(
        {"scientific":False,"operational":False,"trading":False,"capital":False},
        source="RVO",
    )["status"] == "READY"
    assert rvo05.validate_global_claim("PACKAGE_COMPLETE")["status"] == "READY"
    assert rvo05.validate_global_claim("SCIENTIFIC_PASS")["status"] == "BLOCKED"
