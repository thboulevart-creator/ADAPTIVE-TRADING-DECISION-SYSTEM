from __future__ import annotations
import importlib

CASES={
    "AOE0-P1-B01": "BLOCKED_CELL_IDENTITY_MISMATCH",
    "AOE0-P1-B02": "BLOCKED_CLAIM_CLASS_MISMATCH",
    "AOE0-P1-B03": "BLOCKED_INVOCATION_PROFILE_MISMATCH",
    "AOE0-P1-B04": "BLOCKED_DATA_BINDING_MISMATCH",
    "AOE0-P1-B05": "BLOCKED_TEMPORAL_BINDING_MISMATCH",
    "AOE0-P1-B06": "BLOCKED_TEMPORAL_RULE_VIOLATION",
    "AOE0-P1-B07": "BLOCKED_OOS_CONSUMPTION",
    "AOE0-P1-B08": "BLOCKED_POST_RESULT_PRODUCER_SELECTION",
    "AOE0-P1-B09": "BLOCKED_POST_RESULT_PARAMETER_SELECTION",
    "AOE0-P1-B10": "BLOCKED_PRODUCER_CODE_DRIFT",
    "AOE0-P1-B11": "BLOCKED_RUNTIME_LOCK_DRIFT",
    "AOE0-P1-B12": "BLOCKED_INVOCATION_PROFILE_DRIFT",
    "AOE0-P1-B13": "BLOCKED_EXECUTION_MODEL_DRIFT",
    "AOE0-P1-B14": "BLOCKED_COST_SCOPE_DRIFT",
    "AOE0-P1-B15": "BLOCKED_COST_NODE_DRIFT",
    "AOE0-P1-B16": "BLOCKED_UNKNOWN_EXECUTION_OWNER",
    "AOE0-P1-B17": "BLOCKED_NATIVE_OWNER_ATTESTATION_REQUIRED",
    "AOE0-P1-B18": "REJECT_STRUCTURAL_DUCK_TYPING",
    "AOE0-P1-B19": "REJECT_OWNER_ALLOWLIST_LAUNDERING",
    "AOE0-P1-B20": "REJECT_RESULT_TO_SCIENTIFIC_AUTHORITY",
    "AOE0-P1-B21": "REJECT_EXECUTION_TO_TRADING_AUTHORITY",
    "AOE0-P1-B22": "BLOCKED_P1_12B_REGRESSION",
    "AOE0-P1-B23": "BLOCKED_P1_12C_REGRESSION",
    "AOE0-P1-B24": "BLOCKED_P1_21_AP1_REGRESSION"
}

def test_owner_surface_exists_red_baseline():
    owner=importlib.import_module("src.p1_12c_ao_e0_native_owner")
    assert hasattr(owner,"QualifiedAOE0ExecutionResult")
    assert hasattr(owner,"qualify_ao_e0_plan")
    assert hasattr(owner,"attest_synthetic_ao_e0_result")
    assert hasattr(owner,"validate_attack")

def test_frozen_attack_table_is_implemented():
    owner=importlib.import_module("src.p1_12c_ao_e0_native_owner")
    for case_id, expected in CASES.items():
        decision=owner.validate_attack(case_id)
        assert decision["reason"]==expected
        assert decision["status"] in {"BLOCKED","REJECTED"}

def test_p112d_extension_surface_exists():
    ext=importlib.import_module("src.p1_12d_ao_e0_extension")
    assert ext.AO_E0_ALLOWED_OWNER=="P1.12C.AO-E0"
    assert callable(ext.normalize_ao_e0_execution)
