from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from src import p1_12c_ao_e0_native_owner as owner
from src import p1_12d_ao_e0_extension as ext
from tests.p1_18_fixture import build_case

ROOT=Path(__file__).resolve().parents[1]
GOOD40="a"*40
GOOD64="b"*64

def blob(path):
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

def base_case(tmp_path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    return qei,profile,runtime

def real_plan(tmp_path,b12_open=True):
    qei,profile,runtime=base_case(tmp_path)
    plan=owner.qualify_ao_e0_real_plan(
        qei,
        profile=profile,
        runtime_lock=runtime,
        b8_closed=True,
        b8_closure_blob=owner.B8_CLOSURE_BLOB,
        data01_adoption_blob=owner.DATA01_ADOPTION_BLOB,
        data01_adoption_receipt=owner.DATA01_ADOPTION_RECEIPT,
        pipe01_adoption_blob=owner.PIPE01_ADOPTION_BLOB,
        pipe01_adoption_receipt=owner.PIPE01_ADOPTION_RECEIPT,
        pipe01_controller_blob=owner.PIPE01_CONTROLLER_BLOB,
        b12_open=b12_open,
        b12_human_opening_receipt_blob=GOOD40,
        forward_instance_digest=GOOD64,
        cell_identity=owner.CELL_IDENTITY,
        strategy_version_identity=owner.STRATEGY_VERSION_IDENTITY,
        dr01_adoption_blob=owner.DR01_ADOPTION_BLOB,
        owner_lineage_blob=owner.V01_OWNER_BLOB,
        p1_12d_blob=owner.P1_12D_EXTENSION_BLOB,
        producer_code_blob=owner.PRODUCER_BLOB,
    )
    return qei,plan

def test_01_historical_b11_v01_and_r2_preserved():
    assert blob("reports/program/2026-10-05-AO-E0-B11-01-R1-CLOSURE-RECEIPT-V0.1.json")=="4a105b3dcfd49dd8dc50668b4a89bc2e57e5821b"
    assert blob("GOVERNANCE/AO-E0-B11-R2-COMPATIBILITY-BLOCKER-V0.1.json")=="6b5efdc1f74adf6f551315f5bb565fa12ad72e89"
    assert blob("reports/program/2026-10-06-AO-E0-B11-R2-QUALIFICATION-RECEIPT-V0.1.json")=="56f13cdadb625776f67d29a7b8bdc575afd6041c"

def test_02_owner02_identity_and_lineage():
    assert owner.CONTRACT=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_2"
    assert owner.V01_CONTRACT_ID=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_1"
    assert owner.V01_OWNER_BLOB=="524ee6afe0fe2fb49459f70ca4f6612a3bcf2739"
    assert blob("src/p1_12c_ao_e0_native_owner.py")=="57191ab2892e571807a8ed3f53fd0569de1f739e"

def test_03_protected_p112d_and_producer_exact():
    assert blob("src/p1_12d_ao_e0_extension.py")=="fec520916ca07ee6fe7e6029b4ca611519c39bc2"
    assert blob("tools/ao_e0_cc05_e1_producer.py")=="981794fedbfd8c9fdac69ba4751540e63a2e5289"

def test_04_human_adopted_dependencies_exact():
    assert blob("reports/program/2026-10-06-AO-E0-B12-DATA-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")=="290065c68a7d37a43d9c80e326575d9eddcfd088"
    assert blob("reports/program/2026-10-06-AO-E0-B12-PIPE-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")=="4ac1555b846ecd205ed1ad682d1fa165e38a9a3d"
    assert blob("GOVERNANCE/AO-E0-B8-FINAL-HUMAN-CLOSURE-2026-10-06.md")=="8740bf6255286c3c8d896b6b334d10b78c1899f7"
    assert blob("GOVERNANCE/AO-E0-B8-DR-01-FINAL-QUALIFICATION-DECISION-RULE-HUMAN-ADOPTION-2026-10-06.md")=="848e59ac0ef8e56d16322a17bd3f55a0b6e87e45"

def test_05_b12_closed_gate_still_blocks_real_plan(tmp_path):
    with pytest.raises(Exception,match="B12_NOT_HUMAN_OPEN"):
        real_plan(tmp_path,b12_open=False)

def test_06_synthetic_future_gate_produces_attested_real_plan(tmp_path):
    qei,plan=real_plan(tmp_path)
    assert owner.is_factory_attested_ao_e0_real_plan(plan)
    assert plan.pipe01_authorized_state=="AUTHORIZED_PENDING_READ"
    assert plan.execution_authority is False
    assert plan.scientific_authority is False
    assert plan.trading_authority is False
    assert plan.capital_authority is False

def test_07_first_read_and_terminal_result_preserve_native_type(tmp_path):
    qei,plan=real_plan(tmp_path)
    token=owner.attest_ao_e0_first_performance_read(plan,qei)
    assert owner.is_factory_attested_ao_e0_consumption_token(token)
    assert token.consumption_state=="CONSUMED_EXPOSED"
    result=owner.attest_real_ao_e0_result(plan,token,qei,terminal_package_digest="c"*64)
    assert type(result) is owner.QualifiedAOE0ExecutionResult
    assert owner.is_factory_attested_ao_e0_execution_result(result)
    assert result.output_schema==owner.REAL_OUTPUT_SCHEMA
    assert result.output_status==owner.REAL_OUTPUT_STATUS

def test_08_unchanged_p112d_normalizes_real_native_result(tmp_path):
    qei,plan=real_plan(tmp_path)
    token=owner.attest_ao_e0_first_performance_read(plan,qei)
    result=owner.attest_real_ao_e0_result(plan,token,qei,terminal_package_digest="d"*64)
    env=ext.normalize_ao_e0_execution(result,qei)
    assert env.execution_owner_id=="P1.12C.AO-E0"
    assert env.native_result_type_id=="QualifiedAOE0ExecutionResult"
    assert env.scientific_authority is False
    assert env.trading_authority is False
    assert env.capital_authority is False

def test_09_legacy_synthetic_path_remains_valid(tmp_path):
    qei,profile,runtime=base_case(tmp_path)
    data,temporal=owner.expected_bindings()
    plan=owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,oos_consumption=False)
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
    env=ext.normalize_ao_e0_execution(result,qei)
    assert env.execution_owner_id=="P1.12C.AO-E0"

def test_10_authority_firewall_on_real_result(tmp_path):
    qei,plan=real_plan(tmp_path)
    token=owner.attest_ao_e0_first_performance_read(plan,qei)
    result=owner.attest_real_ao_e0_result(plan,token,qei,terminal_package_digest="e"*64)
    assert result.scientific_authority is False
    assert result.qualification_decision is False
    assert result.trading_authority is False
    assert result.capital_authority is False

def test_11_current_data01_real_state_wait_not_ready():
    import json
    d=json.loads((ROOT/"reports/program/2026-10-06-AO-E0-B12-DATA-01-HUMAN-ADOPTION-RECEIPT-V0.1.json").read_text())
    assert d["instance_state"]["state"]=="WAIT_NOT_READY"
    assert d["instance_state"]["exact_forward_instance"]=="NOT_YET_AVAILABLE"

def test_12_current_pipe01_real_state_b12_closed():
    import json
    d=json.loads((ROOT/"reports/program/2026-10-06-AO-E0-B12-PIPE-01-HUMAN-ADOPTION-RECEIPT-V0.1.json").read_text())
    assert d["state"]["b12"]=="CLOSED"
    assert d["authority"]["oos_consumption"] is False
    assert d["authority"]["real_performance_observation"] is False
