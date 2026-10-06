from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess

import pytest

from src import p1_12c_ao_e0_native_owner as owner
from src import p1_12d_ao_e0_extension as ext
from src import p1_12d_qualified_execution_evidence as base12d
from src import ao_e0_b12_consumption_controller as pipe
from tests.p1_18_fixture import build_case

ROOT=Path(__file__).resolve().parents[1]

EXPECTED={
    "owner":"524ee6afe0fe2fb49459f70ca4f6612a3bcf2739",
    "ext":"fec520916ca07ee6fe7e6029b4ca611519c39bc2",
    "producer":"981794fedbfd8c9fdac69ba4751540e63a2e5289",
    "data01_adoption":"63530d627ecbafda3fc160a15a52b27207d48c49",
    "data01_receipt":"290065c68a7d37a43d9c80e326575d9eddcfd088",
    "pipe01_adoption":"e4a74a20cd8bf386fab21718bf5c621a91bd92e8",
    "pipe01_receipt":"4ac1555b846ecd205ed1ad682d1fa165e38a9a3d",
    "b8":"8740bf6255286c3c8d896b6b334d10b78c1899f7",
    "b11_receipt":"4a105b3dcfd49dd8dc50668b4a89bc2e57e5821b",
}
CELL="sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
STRATEGY="sha256:0927e983046ef99a01d2a5c165d18ba5d501f69fb863875f72303b95f69b9687"
GOOD40="a"*40
GOOD64="b"*64

def blob(path:str)->str:
    return subprocess.check_output(["git","hash-object",str(ROOT/path)],text=True).strip()

def runtime_evidence():
    return {
        "python_version":"3.12.14",
        "python_binary_sha256":"11"*32,
        "numpy_version":"2.0.0-synthetic-lock",
        "numpy_metadata_sha256":"22"*32,
        "pyarrow_version":"17.0.0-synthetic-lock",
        "pyarrow_metadata_sha256":"33"*32,
        "tzdata_version":"2026.synthetic",
        "tzdata_metadata_sha256":"44"*32,
        "timezone_name":"UTC",
        "timeout_seconds":120,
    }

def owner_case(tmp_path:Path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    plan=owner.qualify_ao_e0_plan(
        qei,profile=profile,runtime_lock=runtime,
        data_binding=data,temporal_binding=temporal,
        result_exposed=False,oos_consumption=False,
    )
    out={
        "schema":owner.OUTPUT_SCHEMA,
        "status":owner.OUTPUT_STATUS,
        "producer_id":owner.PRODUCER_ID,
        "cell_identity":owner.CELL_IDENTITY,
        "claim_class":owner.CLAIM_CLASS,
        "parameter_digest":owner.SEMANTIC_PARAMETER_DIGEST,
        "records_digest":"ab"*32,
        "synthetic_qualification":True,
    }
    result=owner.attest_synthetic_ao_e0_result(plan,qei,out)
    return qei,profile,runtime,data,temporal,plan,result

def gate(**kw):
    d=dict(
        b8_closed=True,b12_open=True,
        b12_human_opening_receipt_blob=GOOD40,
        forward_instance_digest=GOOD64,
        cell_identity=pipe.CELL_IDENTITY,
        strategy_version_identity=pipe.STRATEGY_VERSION_IDENTITY,
        dr01_adoption_blob=pipe.DR01_ADOPTION_BLOB,
        base_owner_blob=pipe.BASE_OWNER_BLOB,
        base_p1_12d_extension_blob=pipe.BASE_P1_12D_EXTENSION_BLOB,
        result_preexposed=False,
    )
    d.update(kw)
    return pipe.Gate(**d)

# B11R2-01
def test_01_wrong_cell_identity_blocks():
    with pytest.raises(pipe.B12ControllerBlocked,match="CELL_IDENTITY"):
        pipe.authorize(pipe.ConsumptionState(),gate(cell_identity="bad"))

# B11R2-02
def test_02_wrong_strategy_version_blocks():
    with pytest.raises(pipe.B12ControllerBlocked,match="STRATEGY_VERSION"):
        pipe.authorize(pipe.ConsumptionState(),gate(strategy_version_identity="bad"))

# B11R2-03
def test_03_data01_adoption_exact():
    assert blob("GOVERNANCE/AO-E0-B12-DATA-01-PROSPECTIVE-FORWARD-INSTANCE-FORMATION-RULE-HUMAN-ADOPTION-2026-10-06.md")==EXPECTED["data01_adoption"]
    assert blob("reports/program/2026-10-06-AO-E0-B12-DATA-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")==EXPECTED["data01_receipt"]

# B11R2-04
def test_04_pipe01_adoption_exact():
    assert blob("GOVERNANCE/AO-E0-B12-PIPE-01-CONTROLLER-SEMANTICS-HUMAN-ADOPTION-2026-10-06.md")==EXPECTED["pipe01_adoption"]
    assert blob("reports/program/2026-10-06-AO-E0-B12-PIPE-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")==EXPECTED["pipe01_receipt"]

# B11R2-05
def test_05_b8_binding_exact():
    assert blob("GOVERNANCE/AO-E0-B8-FINAL-HUMAN-CLOSURE-2026-10-06.md")==EXPECTED["b8"]

# B11R2-06
def test_06_b12_human_open_required():
    with pytest.raises(pipe.B12ControllerBlocked,match="B12_NOT_HUMAN_OPEN"):
        pipe.authorize(pipe.ConsumptionState(),gate(b12_open=False))

# B11R2-07
def test_07_b12_receipt_required():
    with pytest.raises(pipe.B12ControllerBlocked,match="INVALID_B12_HUMAN_OPENING_RECEIPT"):
        pipe.authorize(pipe.ConsumptionState(),gate(b12_human_opening_receipt_blob=""))

# B11R2-08
def test_08_forward_instance_digest_required():
    with pytest.raises(pipe.B12ControllerBlocked,match="INVALID_FORWARD_INSTANCE_DIGEST"):
        pipe.authorize(pipe.ConsumptionState(),gate(forward_instance_digest=""))

# B11R2-09
def test_09_preexposed_result_blocks():
    with pytest.raises(pipe.B12ControllerBlocked,match="RESULT_PREEXPOSED"):
        pipe.authorize(pipe.ConsumptionState(),gate(result_preexposed=True))

# B11R2-10
def test_10_owner_blob_exact():
    assert blob("src/p1_12c_ao_e0_native_owner.py")==EXPECTED["owner"]

# B11R2-11
def test_11_p112d_extension_blob_exact():
    assert blob("src/p1_12d_ao_e0_extension.py")==EXPECTED["ext"]

# B11R2-12
def test_12_producer_blob_exact():
    assert blob("tools/ao_e0_cc05_e1_producer.py")==EXPECTED["producer"]

# B11R2-13
def test_13_unattested_native_result_blocks(tmp_path):
    qei,_,_,_,_,_,result=owner_case(tmp_path)
    forged=copy.copy(result)
    assert not owner.is_factory_attested_ao_e0_execution_result(forged)
    with pytest.raises(ValueError,match="factory attestation"):
        ext.normalize_ao_e0_execution(forged,qei)

# B11R2-14
def test_14_structural_duck_typing_blocks(tmp_path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    class Duck: pass
    assert ext.validate_owner_candidate(Duck())=={"status":"BLOCKED","reason":"BLOCKED_UNKNOWN_EXECUTION_OWNER"}
    with pytest.raises(TypeError,match="unknown/structural"):
        ext.normalize_ao_e0_execution(Duck(),qei)

# B11R2-15
def test_15_private_attestation_laundering_is_not_public_path():
    assert hasattr(owner,"_attest_result")
    assert not hasattr(owner,"attest_real_ao_e0_result")
    public_factories=[n for n in dir(owner) if not n.startswith("_") and n.startswith("attest_") and "result" in n.lower()]
    assert public_factories==["attest_synthetic_ao_e0_result"]

# B11R2-16
def test_16_digest_only_substitution_blocks(tmp_path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    class DigestOnly:
        result_content_identity=GOOD64
    with pytest.raises(TypeError,match="unknown/structural"):
        ext.normalize_ao_e0_execution(DigestOnly(),qei)

# B11R2-17
def test_17_exact_type_bypass_blocks(tmp_path):
    qei,_,_,_,_,_,result=owner_case(tmp_path)
    class Sub(type(result)):
        pass
    # construction can copy values but exact-type check must reject before attestation
    values={f:getattr(result,f) for f in result.__dataclass_fields__}
    sub=Sub(**values)
    with pytest.raises(TypeError,match="unknown/structural"):
        ext.normalize_ao_e0_execution(sub,qei)

# B11R2-18
def test_18_second_first_read_blocks():
    s=pipe.first_performance_bearing_read(pipe.authorize(pipe.ConsumptionState(),gate()))
    with pytest.raises(pipe.B12ControllerBlocked,match="FIRST_READ_REQUIRES_AUTHORIZED_PENDING_READ"):
        pipe.first_performance_bearing_read(s)

# B11R2-19
def test_19_consumed_does_not_return_pristine():
    s=pipe.first_performance_bearing_read(pipe.authorize(pipe.ConsumptionState(),gate()))
    assert s.state=="CONSUMED_EXPOSED"
    assert s.independent_confirmation_eligible is False

# B11R2-20
def test_20_post_consumption_failure_stays_consumed():
    s=pipe.first_performance_bearing_read(pipe.authorize(pipe.ConsumptionState(),gate()))
    s=pipe.technical_failure(s)
    assert s.state=="TECHNICAL_FAILURE_CONSUMED"
    assert s.independent_confirmation_eligible is False

# B11R2-21
def test_21_same_evidence_replay_not_new_confirmation():
    s=pipe.first_performance_bearing_read(pipe.authorize(pipe.ConsumptionState(),gate()))
    r=pipe.replay_semantics(s,GOOD64)
    assert r["new_independent_confirmation"] is False
    assert r["pristine_restored"] is False

# B11R2-22
def test_22_intermediate_output_policy_frozen():
    d=json.loads((ROOT/"GOVERNANCE/AO-E0-B12-PIPE-01-CONSUMPTION-CONTROLLER-CANDIDATE-V0.1.json").read_text())
    assert d["output_policy"]["intermediate_performance_bearing_output_user_visible"] is False
    assert d["output_policy"]["terminal_evidence_package_is_first_governed_observation_surface"] is True

# B11R2-23
def test_23_owner_result_has_no_scientific_authority(tmp_path):
    *_,result=owner_case(tmp_path)
    assert result.scientific_authority is False
    assert result.qualification_decision is False

# B11R2-24
def test_24_owner_result_has_no_trading_authority(tmp_path):
    *_,result=owner_case(tmp_path)
    assert result.trading_authority is False

# B11R2-25
def test_25_owner_result_has_no_capital_authority(tmp_path):
    *_,result=owner_case(tmp_path)
    assert result.capital_authority is False

# B11R2-26
def test_26_p112c_contract_regression_guard():
    assert owner.CONTRACT=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_1"
    assert owner.P1_21_FOUNDATION_BLOB=="9d304202d44c8917cf640fd0b4114169968e511e"

# B11R2-27
def test_27_p112d_contract_regression_guard():
    assert ext.CONTRACT=="P1_12D_AO_E0_EXACT_NATIVE_OWNER_EXTENSION_V0_1"
    assert ext.BASE_P112D_CONTRACT=="P1_12D_QUALIFIED_EXECUTION_EVIDENCE_ENVELOPE_V1"
    assert ext.BASE_ALLOWED_OWNERS==("P1.12B","P1.12C")

# B11R2-28
def test_28_existing_b11_closure_receipt_exact():
    assert blob("reports/program/2026-10-05-AO-E0-B11-01-R1-CLOSURE-RECEIPT-V0.1.json")==EXPECTED["b11_receipt"]

# B11R2-29
def test_29_data01_wait_not_ready_preserved():
    d=json.loads((ROOT/"reports/program/2026-10-06-AO-E0-B12-DATA-01-HUMAN-ADOPTION-RECEIPT-V0.1.json").read_text())
    assert d["instance_state"]["state"]=="WAIT_NOT_READY"
    assert d["instance_state"]["exact_forward_instance"]=="NOT_YET_AVAILABLE"

# B11R2-30
def test_30_pipe01_b12_closed_preserved():
    d=json.loads((ROOT/"reports/program/2026-10-06-AO-E0-B12-PIPE-01-HUMAN-ADOPTION-RECEIPT-V0.1.json").read_text())
    assert d["state"]["b12"]=="CLOSED"
    assert d["authority"]["oos_consumption"] is False

# B11R2-31
def test_31_current_owner_real_oos_plan_must_block(tmp_path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_OOS_CONSUMPTION"):
        owner.qualify_ao_e0_plan(
            qei,profile=profile,runtime_lock=runtime,
            data_binding=data,temporal_binding=temporal,
            oos_consumption=True,
        )

# B11R2-32
def test_32_public_real_result_attestor_absent():
    assert not hasattr(owner,"attest_real_ao_e0_result")
    assert hasattr(owner,"attest_synthetic_ao_e0_result")

# B11R2-33
def test_33_foreign_exact_type_blocks(tmp_path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    class Foreign: pass
    with pytest.raises(TypeError,match="unknown/structural"):
        ext.normalize_ao_e0_execution(Foreign(),qei)

# B11R2-34
def test_34_forged_native_type_blocks_factory_attestation(tmp_path):
    qei,_,_,_,_,_,result=owner_case(tmp_path)
    vals={f:getattr(result,f) for f in result.__dataclass_fields__}
    forged=owner.QualifiedAOE0ExecutionResult(**vals)
    assert type(forged) is owner.QualifiedAOE0ExecutionResult
    assert owner.is_factory_attested_ao_e0_execution_result(forged) is False
    with pytest.raises(ValueError,match="factory attestation"):
        ext.normalize_ao_e0_execution(forged,qei)

# B11R2-35
def test_35_protected_mutation_is_required_for_public_real_native_result_path(tmp_path):
    # Current public plan cannot cross the OOS gate.
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_OOS_CONSUMPTION"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,oos_consumption=True)
    # Current only public native-result factory is synthetic-only.
    assert not hasattr(owner,"attest_real_ao_e0_result")
    src=(ROOT/"src/p1_12c_ao_e0_native_owner.py").read_text()
    assert 'if output["synthetic_qualification"] is not True:' in src
    assert 'raise AOE0P1OwnerBlocked("BLOCKED_REAL_EXECUTION_NOT_AUTHORIZED")' in src
    # P1.12D simultaneously requires this exact factory-attested type.
    ext_src=(ROOT/"src/p1_12d_ao_e0_extension.py").read_text()
    assert "if type(execution_result) is not QualifiedAOE0ExecutionResult:" in ext_src
    assert "if not is_factory_attested_ao_e0_execution_result(execution_result):" in ext_src
