from __future__ import annotations
import copy
from pathlib import Path
import pytest
from tools import g05_01_workspace_dry_readiness as g

def runtime():
    return {
        "platform":"Windows","architecture":"AMD64","python_version":g.PYTHON_VERSION,
        "python_real_binary_sha256":g.PYTHON_REAL_BINARY_SHA256,
        "dependencies":copy.deepcopy(g.EXPECTED_DEPENDENCIES),
        "timezone_name":"America/New_York","timezone_probe":"PASS",
        "material_environment":dict(g.MATERIAL_ENVIRONMENT),
    }

def test_01_breaker_surface_all_true():
    assert all(g.evaluate_frozen_breaker_case(x) for x in g.CASE_IDS)

def test_02_runtime_exact_accepts():
    g.validate_runtime_observation(runtime())

@pytest.mark.parametrize("field,code",[
    ("python_version","BLOCKED_PYTHON_VERSION_MISMATCH"),
    ("python_real_binary_sha256","BLOCKED_PYTHON_BINARY_IDENTITY_REQUIRED"),
])
def test_03_runtime_identity_fail_closed(field,code):
    r=runtime(); r[field]="wrong"
    with pytest.raises(g.G0501Blocked,match=code): g.validate_runtime_observation(r)

@pytest.mark.parametrize("name",["numpy","pyarrow","tzdata"])
def test_04_dependency_identity_fail_closed(name):
    r=runtime(); r["dependencies"][name]["record_sha256"]="0"*64
    with pytest.raises(g.G0501Blocked): g.validate_runtime_observation(r)

def test_05_material_environment_exact():
    r=runtime(); r["material_environment"]["PYTHONHASHSEED"]="1"
    with pytest.raises(g.G0501Blocked,match="BLOCKED_MATERIAL_ENVIRONMENT_MISMATCH"): g.validate_runtime_observation(r)

def test_06_timeout_is_finite():
    assert 0 < g.TIMEOUT_SECONDS <= 86400

def test_07_manifest_identity_matches_p121():
    assert g.AP0_MANIFEST_SHA256 == g.p12c.DATA02_REAL_MANIFEST_SHA256

def test_08_protected_ap1_identity_matches_p121():
    assert g.PROTECTED_BLOBS["tools/ap1_intraday_spread_census.py"] == g.p12c.AP1_PRODUCER_BLOB

def test_09_p1_profile_is_exact():
    assert g.p12c.AP1_INVOCATION_PROFILE_ID == "P1_12C_AP1_CLAIM_SCOPED_V1"

def test_10_smf_activation_is_pre_result():
    a=g.smf.create_m03_activation(result_exposed=False)
    assert a["activation_state"]=="ACTIVATED"

def test_11_smf_post_result_activation_blocked():
    with pytest.raises(Exception,match="METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE"):
        g.smf.create_m03_activation(result_exposed=True)

def test_12_repository_and_branch_exact():
    assert g.REPOSITORY=="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
    assert g.CANONICAL_BRANCH=="integration/system-v1"

def test_13_workspace_path_never_part_of_static_identity_constants():
    assert "ATDS-WORKTREES" not in g.REPOSITORY

def test_14_no_execution_function_is_called_by_breaker_surface(monkeypatch):
    monkeypatch.setattr(g.smf,"execute_m03_observations",lambda *a,**k: (_ for _ in ()).throw(AssertionError("must not execute")))
    assert g.evaluate_frozen_breaker_case("G0501-B26") is True

def test_15_contract_declares_no_authority():
    assert g.CONTRACT=="ATDS_G05_01_WORKSPACE_DRY_READINESS_V0_1"


def test_16_synthetic_input_shape_does_not_create_legacy_p112c_plan(tmp_path, monkeypatch):
    monkeypatch.setattr(
        g.p12c,
        "qualify_producer_execution_plan",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("legacy P1.12C plan must not be created")),
    )
    qualified=g._build_synthetic_qualified_input(tmp_path/"shape")
    assert g.p12c.is_factory_attested_qualified_experiment_execution_input(qualified)
