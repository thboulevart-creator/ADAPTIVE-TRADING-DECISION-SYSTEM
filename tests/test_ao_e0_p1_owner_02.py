from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess

import pytest

from src import p1_12c_ao_e0_native_owner as owner
from src import p1_12d_ao_e0_extension as ext
from src import ao_e0_b12_consumption_controller as pipe
from tests.p1_18_fixture import build_case

ROOT=Path(__file__).resolve().parents[1]

GOOD40="a"*40
GOOD64="b"*64

EXPECTED={
    "owner01_blob":"524ee6afe0fe2fb49459f70ca4f6612a3bcf2739",
    "p1_12d_blob":"fec520916ca07ee6fe7e6029b4ca611519c39bc2",
    "producer_blob":"981794fedbfd8c9fdac69ba4751540e63a2e5289",
    "data01_adoption_blob":"63530d627ecbafda3fc160a15a52b27207d48c49",
    "data01_receipt":"290065c68a7d37a43d9c80e326575d9eddcfd088",
    "pipe01_adoption_blob":"e4a74a20cd8bf386fab21718bf5c621a91bd92e8",
    "pipe01_receipt":"4ac1555b846ecd205ed1ad682d1fa165e38a9a3d",
    "pipe01_controller_blob":"e9d37a56e33d66b1c43c0a2ca11e96bb703dac0f",
    "b8_blob":"8740bf6255286c3c8d896b6b334d10b78c1899f7",
    "dr01_blob":"848e59ac0ef8e56d16322a17bd3f55a0b6e87e45",
    "b11_r2_receipt":"56f13cdadb625776f67d29a7b8bdc575afd6041c",
    "b11_v01_closure":"4a105b3dcfd49dd8dc50668b4a89bc2e57e5821b",
}

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

def base_case(tmp_path:Path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    return qei,profile,runtime

def real_kwargs():
    return dict(
        b8_closed=True,
        b8_closure_blob=EXPECTED["b8_blob"],
        data01_adoption_blob=EXPECTED["data01_adoption_blob"],
        data01_adoption_receipt=EXPECTED["data01_receipt"],
        pipe01_adoption_blob=EXPECTED["pipe01_adoption_blob"],
        pipe01_adoption_receipt=EXPECTED["pipe01_receipt"],
        pipe01_controller_blob=EXPECTED["pipe01_controller_blob"],
        b12_open=True,
        b12_human_opening_receipt_blob=GOOD40,
        forward_instance_digest=GOOD64,
        cell_identity=pipe.CELL_IDENTITY,
        strategy_version_identity=pipe.STRATEGY_VERSION_IDENTITY,
        dr01_adoption_blob=EXPECTED["dr01_blob"],
        owner_lineage_blob=EXPECTED["owner01_blob"],
        p1_12d_blob=EXPECTED["p1_12d_blob"],
        producer_code_blob=EXPECTED["producer_blob"],
        result_preexposed=False,
        owner_selection_after_result=False,
        parameter_selection_after_result=False,
    )

def real_plan(tmp_path:Path, **overrides):
    qei,profile,runtime=base_case(tmp_path)
    kw=real_kwargs(); kw.update(overrides)
    plan=owner.qualify_ao_e0_real_plan(qei,profile=profile,runtime_lock=runtime,**kw)
    return qei,profile,runtime,plan

def consumed(tmp_path:Path, **overrides):
    qei,profile,runtime,plan=real_plan(tmp_path,**overrides)
    token=owner.attest_ao_e0_first_performance_read(plan,qei)
    return qei,profile,runtime,plan,token

def real_result(tmp_path:Path):
    qei,_,_,plan,token=consumed(tmp_path)
    result=owner.attest_real_ao_e0_result(
        plan,token,qei,
        terminal_package_digest="c"*64,
    )
    return qei,plan,token,result

def assert_block(call, pattern):
    with pytest.raises((owner.AOE0P1OwnerBlocked, pipe.B12ControllerBlocked),match=pattern):
        call()

CASES=[f"OWNER02-{i:02d}" for i in range(1,49)]

@pytest.mark.parametrize("case_id",CASES)
def test_owner02_frozen_breakers(case_id,tmp_path):
    if case_id=="OWNER02-01":
        assert_block(lambda: real_plan(tmp_path,cell_identity="bad"),"CELL_IDENTITY")
    elif case_id=="OWNER02-02":
        assert_block(lambda: real_plan(tmp_path,strategy_version_identity="bad"),"STRATEGY_VERSION")
    elif case_id=="OWNER02-03":
        assert_block(lambda: real_plan(tmp_path,data01_adoption_receipt="0"*40),"DATA01")
    elif case_id=="OWNER02-04":
        assert_block(lambda: real_plan(tmp_path,pipe01_adoption_receipt="0"*40),"PIPE01")
    elif case_id=="OWNER02-05":
        assert_block(lambda: real_plan(tmp_path,b8_closure_blob="0"*40),"B8")
    elif case_id=="OWNER02-06":
        assert_block(lambda: real_plan(tmp_path,dr01_adoption_blob="0"*40),"DR01")
    elif case_id=="OWNER02-07":
        assert_block(lambda: real_plan(tmp_path,b12_open=False),"B12_NOT_HUMAN_OPEN")
    elif case_id=="OWNER02-08":
        assert_block(lambda: real_plan(tmp_path,b12_human_opening_receipt_blob=""),"INVALID_B12")
    elif case_id=="OWNER02-09":
        assert_block(lambda: real_plan(tmp_path,b12_human_opening_receipt_blob="bad"),"INVALID_B12")
    elif case_id=="OWNER02-10":
        assert_block(lambda: real_plan(tmp_path,forward_instance_digest=""),"INVALID_FORWARD")
    elif case_id=="OWNER02-11":
        assert_block(lambda: real_plan(tmp_path,forward_instance_digest="bad"),"INVALID_FORWARD")
    elif case_id=="OWNER02-12":
        assert_block(lambda: real_plan(tmp_path,result_preexposed=True),"RESULT_PREEXPOSED")
    elif case_id=="OWNER02-13":
        assert_block(lambda: real_plan(tmp_path,owner_lineage_blob="0"*40),"OWNER_LINEAGE")
    elif case_id=="OWNER02-14":
        assert_block(lambda: real_plan(tmp_path,producer_code_blob="0"*40),"PRODUCER")
    elif case_id=="OWNER02-15":
        assert_block(lambda: real_plan(tmp_path,p1_12d_blob="0"*40),"P1_12D")
    elif case_id=="OWNER02-16":
        assert "authorized_state" not in owner.qualify_ao_e0_real_plan.__code__.co_varnames
    elif case_id=="OWNER02-17":
        assert not hasattr(owner,"_attest_result")
        assert not hasattr(owner,"_result_attest_raw")
    elif case_id=="OWNER02-18":
        qei,_,_,plan=real_plan(tmp_path)
        forged=copy.copy(plan)
        assert not owner.is_factory_attested_ao_e0_real_plan(forged)
        assert_block(lambda: owner.attest_ao_e0_first_performance_read(forged,qei),"UNATTESTED_REAL_PLAN")
    elif case_id=="OWNER02-19":
        qei,_,_,plan=real_plan(tmp_path)
        vals={f:getattr(plan,f) for f in plan.__dataclass_fields__}
        forged=owner.QualifiedAOE0RealExecutionPlan(**vals)
        assert not owner.is_factory_attested_ao_e0_real_plan(forged)
        assert_block(lambda: owner.attest_ao_e0_first_performance_read(forged,qei),"UNATTESTED_REAL_PLAN")
    elif case_id=="OWNER02-20":
        qei,profile,runtime=base_case(tmp_path)
        data,temporal=owner.expected_bindings()
        spl=owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal)
        fake=owner.QualifiedAOE0ConsumptionToken if hasattr(owner,"QualifiedAOE0ConsumptionToken") else object
        assert_block(lambda: owner.attest_real_ao_e0_result(spl,fake(),qei,terminal_package_digest="c"*64),"REAL_PLAN")
    elif case_id=="OWNER02-21":
        qei,_,_,plan=real_plan(tmp_path)
        out={"schema":owner.OUTPUT_SCHEMA,"status":owner.OUTPUT_STATUS,"producer_id":owner.PRODUCER_ID,"cell_identity":owner.CELL_IDENTITY,"claim_class":owner.CLAIM_CLASS,"parameter_digest":owner.SEMANTIC_PARAMETER_DIGEST,"records_digest":"ab"*32,"synthetic_qualification":True}
        assert_block(lambda: owner.attest_synthetic_ao_e0_result(plan,qei,out),"UNATTESTED_PLAN")
    elif case_id=="OWNER02-22":
        qei,_,_,res=real_result(tmp_path)
        vals={f:getattr(res,f) for f in res.__dataclass_fields__}
        forged=owner.QualifiedAOE0ExecutionResult(**vals)
        assert not owner.is_factory_attested_ao_e0_execution_result(forged)
        with pytest.raises(ValueError,match="factory attestation"): ext.normalize_ao_e0_execution(forged,qei)
    elif case_id=="OWNER02-23":
        qei=build_case(tmp_path/"qei")["qualified_input"]
        class Duck: pass
        with pytest.raises(TypeError,match="unknown/structural"): ext.normalize_ao_e0_execution(Duck(),qei)
    elif case_id=="OWNER02-24":
        qei,_,_,res=real_result(tmp_path)
        class Sub(type(res)): pass
        vals={f:getattr(res,f) for f in res.__dataclass_fields__}
        sub=Sub(**vals)
        with pytest.raises(TypeError,match="unknown/structural"): ext.normalize_ao_e0_execution(sub,qei)
    elif case_id=="OWNER02-25":
        qei,_,_,plan=real_plan(tmp_path)
        dummy=owner.QualifiedAOE0ConsumptionToken if hasattr(owner,"QualifiedAOE0ConsumptionToken") else object
        assert_block(lambda: owner.attest_real_ao_e0_result(plan,dummy(),qei,terminal_package_digest="c"*64),"CONSUMPTION")
    elif case_id=="OWNER02-26":
        qei,_,_,plan,token=consumed(tmp_path)
        assert_block(lambda: owner.attest_ao_e0_first_performance_read(plan,qei),"FIRST_READ")
    elif case_id=="OWNER02-27":
        _,_,_,_,token=consumed(tmp_path)
        assert token.consumption_state=="CONSUMED_EXPOSED"
        assert token.independent_confirmation_eligible is False
    elif case_id=="OWNER02-28":
        _,_,_,_,token=consumed(tmp_path)
        assert token.consumption_state!="PRISTINE"
    elif case_id=="OWNER02-29":
        _,_,_,plan,token=consumed(tmp_path)
        state=pipe.ConsumptionState(state="CONSUMED_EXPOSED",forward_instance_digest=plan.forward_instance_digest,human_opening_receipt_blob=plan.b12_human_opening_receipt_blob,performance_bearing_read_count=1,independent_confirmation_eligible=False)
        r=pipe.replay_semantics(state,plan.forward_instance_digest)
        assert r["new_independent_confirmation"] is False
    elif case_id=="OWNER02-30":
        assert owner.REAL_OUTPUT_SCHEMA=="ATDS_AO_E0_CC05_REAL_OOS_TERMINAL_EVIDENCE_V0_2"
        assert owner.INTERMEDIATE_PERFORMANCE_OUTPUT_USER_VISIBLE is False
    elif case_id=="OWNER02-31":
        _,_,_,res=real_result(tmp_path); assert res.scientific_authority is False
    elif case_id=="OWNER02-32":
        _,_,_,res=real_result(tmp_path); assert res.qualification_decision is False
    elif case_id=="OWNER02-33":
        _,_,_,res=real_result(tmp_path); assert res.trading_authority is False
    elif case_id=="OWNER02-34":
        _,_,_,res=real_result(tmp_path); assert res.capital_authority is False
    elif case_id=="OWNER02-35":
        qei,profile,runtime=base_case(tmp_path); data,temporal=owner.expected_bindings()
        plan=owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,oos_consumption=False)
        assert owner.is_factory_attested_ao_e0_plan(plan)
        assert_block(lambda: owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,oos_consumption=True),"BLOCKED_OOS_CONSUMPTION")
    elif case_id=="OWNER02-36":
        qei,_,_,res=real_result(tmp_path)
        env=ext.normalize_ao_e0_execution(res,qei)
        assert env.native_result_type_id=="QualifiedAOE0ExecutionResult"
        assert env.execution_owner_id=="P1.12C.AO-E0"
    elif case_id=="OWNER02-37":
        assert blob("tools/ao_e0_cc05_e1_producer.py")==EXPECTED["producer_blob"]
    elif case_id=="OWNER02-38":
        assert blob("GOVERNANCE/AO-E0-B12-DATA-01-PROSPECTIVE-FORWARD-INSTANCE-FORMATION-RULE-HUMAN-ADOPTION-2026-10-06.md")==EXPECTED["data01_adoption_blob"]
        assert blob("reports/program/2026-10-06-AO-E0-B12-DATA-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")==EXPECTED["data01_receipt"]
    elif case_id=="OWNER02-39":
        assert blob("GOVERNANCE/AO-E0-B12-PIPE-01-CONTROLLER-SEMANTICS-HUMAN-ADOPTION-2026-10-06.md")==EXPECTED["pipe01_adoption_blob"]
        assert blob("reports/program/2026-10-06-AO-E0-B12-PIPE-01-HUMAN-ADOPTION-RECEIPT-V0.1.json")==EXPECTED["pipe01_receipt"]
    elif case_id=="OWNER02-40":
        assert blob("GOVERNANCE/AO-E0-B8-FINAL-HUMAN-CLOSURE-2026-10-06.md")==EXPECTED["b8_blob"]
    elif case_id=="OWNER02-41":
        assert blob("GOVERNANCE/AO-E0-B8-DR-01-FINAL-QUALIFICATION-DECISION-RULE-HUMAN-ADOPTION-2026-10-06.md")==EXPECTED["dr01_blob"]
    elif case_id=="OWNER02-42":
        assert blob("reports/program/2026-10-05-AO-E0-B11-01-R1-CLOSURE-RECEIPT-V0.1.json")==EXPECTED["b11_v01_closure"]
        assert blob("reports/program/2026-10-06-AO-E0-B11-R2-QUALIFICATION-RECEIPT-V0.1.json")==EXPECTED["b11_r2_receipt"]
    elif case_id=="OWNER02-43":
        assert_block(lambda: real_plan(tmp_path,owner_selection_after_result=True),"POST_RESULT_OWNER_SELECTION")
    elif case_id=="OWNER02-44":
        assert_block(lambda: real_plan(tmp_path,parameter_selection_after_result=True),"POST_RESULT_PARAMETER_SELECTION")
    elif case_id=="OWNER02-45":
        assert owner.OWNER_ID=="P1.12C.AO-E0"
        assert not hasattr(owner,"FALLBACK_REAL_OWNER")
    elif case_id=="OWNER02-46":
        qei,_,_,plan=real_plan(tmp_path); assert plan.forward_instance_digest==GOOD64
    elif case_id=="OWNER02-47":
        qei,_,_,plan=real_plan(tmp_path); assert plan.b12_human_opening_receipt_blob==GOOD40
    elif case_id=="OWNER02-48":
        qei,_,_,plan=real_plan(tmp_path)
        assert owner.is_factory_attested_ao_e0_real_plan(plan)
        assert plan.pipe01_authorized_state=="AUTHORIZED_PENDING_READ"
        assert plan.pipe01_controller_blob==EXPECTED["pipe01_controller_blob"]

def test_owner02_positive_synthetic_capability_path(tmp_path):
    qei,plan,token,result=real_result(tmp_path)
    assert owner.OWNER02_CONTRACT_ID=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_2"
    assert owner.is_factory_attested_ao_e0_real_plan(plan)
    assert owner.is_factory_attested_ao_e0_consumption_token(token)
    assert owner.is_factory_attested_ao_e0_execution_result(result)
    assert result.output_schema==owner.REAL_OUTPUT_SCHEMA
    assert result.output_status==owner.REAL_OUTPUT_STATUS
    env=ext.normalize_ao_e0_execution(result,qei)
    assert env.execution_owner_id=="P1.12C.AO-E0"
    assert env.native_result_type_id=="QualifiedAOE0ExecutionResult"
    assert env.scientific_authority is False
    assert env.trading_authority is False
    assert env.capital_authority is False
