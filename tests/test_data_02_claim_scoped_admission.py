from __future__ import annotations

import copy

from src.data import claim_scoped_admission as data02
from tests.data_02_fixture import (
    CLAIM_CLASS,
    CONSUMER_ID,
    DATASET_IDENTITY,
    make_package,
)

def _binding(decision, result_identity="RESULT-POSITIVE-001"):
    basis = decision["binding_basis"]
    return {
        **basis,
        "data_admissibility_evidence_ref": decision["admission_digest"],
        "result_identity": result_identity,
    }

def test_data02_positive_01_baseline_synthetic_ready(tmp_path):
    package = make_package(tmp_path)
    out = data02.evaluate_synthetic(package)
    assert out["status"] == "READY_FOR_EXACT_CLAIM"
    assert out["reason"] == "PASS_SYNTHETIC_CLAIM_SCOPED_DATA_ADMISSION"
    assert out["scientific_authority"] is False
    assert out["trading_authority"] is False
    assert out["rvo_authority"] == "NONE"

def test_data02_positive_02_deterministic_reconstruction(tmp_path):
    a = data02.evaluate_synthetic(make_package(tmp_path / "a"))
    b = data02.evaluate_synthetic(make_package(tmp_path / "b"))
    assert a["status"] == b["status"] == "READY_FOR_EXACT_CLAIM"
    assert a["binding_basis"] == b["binding_basis"]
    assert a["admission_digest"] == b["admission_digest"]

def test_data02_positive_03_exact_result_binding(tmp_path):
    out = data02.evaluate_synthetic(make_package(tmp_path))
    bound = data02.validate_result_binding(out, _binding(out))
    assert bound["status"] == "BOUND_TO_EXACT_DATASET"
    assert bound["reason"] == "PASS_EXACT_RESULT_DATASET_BINDING"
    assert len(bound["binding_digest"]) == 64

def test_data02_positive_04_pyarrow_double_is_same_float64_semantic_type(tmp_path):
    package = make_package(tmp_path)
    for row in package["observed_schema"]:
        if row[1] == "float64":
            row[1] = "double"
    out = data02.evaluate_synthetic(package)
    assert out["status"] == "READY_FOR_EXACT_CLAIM"

def test_data02_positive_05_exact_surface_selection(tmp_path):
    out = data02.validate_surface_selection(
        DATASET_IDENTITY,
        claim_class=CLAIM_CLASS,
        consumer_id=CONSUMER_ID,
        subminute_required=False,
        universal_sufficiency_claim=False,
    )
    assert out["status"] == "SELECTED"
    assert out["dataset_identity"] == DATASET_IDENTITY

def test_data02_positive_06_temporal_remains_non_authoritative(tmp_path):
    out = data02.evaluate_synthetic(make_package(tmp_path))
    assert out["temporal_status"] == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
    assert out["temporal_authority"] is False
    assert "TEMPORAL_PASS" not in out.values()
    assert "HISTORICAL_PIT_PASS" not in out.values()

def test_data02_positive_07_capability_surface_is_minimal():
    assert data02.CAPABILITIES["read_only_admission"] is True
    assert sum(bool(v) for v in data02.CAPABILITIES.values()) == 1

def test_data02_positive_08_real_adapter_fails_closed_without_corpus(tmp_path):
    out = data02.admit_real_ap0(tmp_path / "missing-root", tmp_path / "missing-manifest.json")
    assert out["status"] == "BLOCKED_ACCESS"
    assert out["real_ap0_qualification"] == "BLOCKED_ACCESS"
    assert out["reason"] == "REAL_AP0_ROOT_NOT_ACCESSIBLE"

def test_data02_positive_09_mutable_commentary_does_not_change_admission_identity(tmp_path):
    package = make_package(tmp_path)
    a = data02.evaluate_synthetic(package)
    package["mutable_commentary"] = "changed"
    b = data02.evaluate_synthetic(package)
    assert a["admission_digest"] == b["admission_digest"]

def test_data02_positive_10_result_identity_changes_binding_not_dataset_admission(tmp_path):
    out = data02.evaluate_synthetic(make_package(tmp_path))
    a = data02.validate_result_binding(out, _binding(out, "RESULT-A"))
    b = data02.validate_result_binding(out, _binding(out, "RESULT-B"))
    assert a["status"] == b["status"] == "BOUND_TO_EXACT_DATASET"
    assert a["binding_digest"] != b["binding_digest"]
    assert out["admission_digest"] == _binding(out, "RESULT-A")["data_admissibility_evidence_ref"]
