from __future__ import annotations

import copy
from pathlib import Path

import pytest

from src import p1_12c_ao_e0_native_owner as owner
from src import p1_12d_ao_e0_extension as ext
from src import p1_12d_qualified_execution_evidence as base12d
from src.p1_13c_common_evaluation import CommonExperimentMeasurementClaim, submit_common_experiment_evaluation
from src.p1_14c_common_measurement_provenance import reattest_common_measurement_provenance
from src.p1_15c_common_evaluator_authority import reattest_common_evaluator_authority
from src.p1_16c_common_qualified_finding import interpret_common_qualified_finding
from tests.p1_18_fixture import build_case
from tests.p1_20_fixture import (
    DERIVATION_AUTHORITY,
    EVALUATION_AUTHORITY,
    _p114c_files,
    _p115c_files,
)
from tools import ao_e0_cc05_e1_producer as producer

ROOT=Path(__file__).resolve().parents[1]


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


def build_owner_case(tmp_path: Path):
    qcase=build_case(tmp_path/"qei")
    qei=qcase["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data_binding,temporal_binding=owner.expected_bindings()
    plan=owner.qualify_ao_e0_plan(
        qei,
        profile=profile,
        runtime_lock=runtime,
        data_binding=data_binding,
        temporal_binding=temporal_binding,
        result_exposed=False,
        oos_consumption=False,
    )
    output={
        "schema":owner.OUTPUT_SCHEMA,
        "status":owner.OUTPUT_STATUS,
        "producer_id":owner.PRODUCER_ID,
        "cell_identity":owner.CELL_IDENTITY,
        "claim_class":owner.CLAIM_CLASS,
        "parameter_digest":owner.SEMANTIC_PARAMETER_DIGEST,
        "records_digest":"ab"*32,
        "synthetic_qualification":True,
    }
    result=owner.attest_synthetic_ao_e0_result(plan,qei,output)
    envelope=ext.normalize_ao_e0_execution(result,qei)
    return {
        "qei":qei,"profile":profile,"runtime":runtime,"data_binding":data_binding,
        "temporal_binding":temporal_binding,"plan":plan,"result":result,"envelope":envelope,
    }


def test_owner_contract_and_p121_foundation():
    assert owner.CONTRACT=="P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_1"
    assert owner.P1_21_FOUNDATION_CONTRACT=="P1_12C_REAL_QUALIFIED_PRODUCER_CAPABILITY_V1"
    assert owner.P1_21_FOUNDATION_BLOB=="9d304202d44c8917cf640fd0b4114169968e511e"
    assert owner.PRODUCER_BLOB=="981794fedbfd8c9fdac69ba4751540e63a2e5289"


def test_producer_is_exact_e1_orchestration_without_scientific_result():
    assert producer.PRODUCER_ID==owner.PRODUCER_ID
    assert producer.SEMANTIC_PARAMETER_DIGEST==owner.SEMANTIC_PARAMETER_DIGEST
    start=1_800_000_000_000
    rows=[
        {
            "h1_start_ms_utc":start+i*3_600_000,
            "source_segment_id":"SYN",
            "continuity_block_id":"B0",
            "continuity_ordinal":i,
            "mid_close":100.0+i,
        }
        for i in range(21)
    ]
    ticks=[{
        "timestamp_ms":start+21*3_600_000,
        "continuity_status":"ALLOWED",
        "bid":120.0,
        "ask":120.5,
    }]
    out=producer.build_execution_evidence(rows,ticks)
    assert out["status"]==producer.OUTPUT_STATUS
    assert out["cell_identity"]==owner.CELL_IDENTITY
    assert out["claim_class"]==owner.CLAIM_CLASS
    assert out["cost_node"]=="F2_S4"
    assert not (producer.FORBIDDEN_SCIENTIFIC_KEYS & set(out))
    assert out["scientific_authority"] is False
    assert out["trading_authority"] is False
    assert out["capital_authority"] is False


def test_native_owner_plan_result_and_p112d_extension(tmp_path: Path):
    case=build_owner_case(tmp_path)
    assert owner.is_factory_attested_ao_e0_plan(case["plan"])
    assert owner.is_factory_attested_ao_e0_execution_result(case["result"])
    assert case["result"].cell_identity==owner.CELL_IDENTITY
    assert case["result"].claim_class==owner.CLAIM_CLASS
    assert case["result"].scientific_authority is False
    assert case["result"].qualification_decision is False
    assert case["result"].trading_authority is False
    assert case["result"].capital_authority is False
    env=case["envelope"]
    assert env.execution_owner_id=="P1.12C.AO-E0"
    assert env.native_execution_contract_id==owner.CONTRACT
    assert env.native_result_type_id=="QualifiedAOE0ExecutionResult"
    assert env.measurement_input_identity==case["result"].result_content_identity
    assert base12d.is_factory_attested_qualified_execution_evidence(env)
    assert env.scientific_authority is False
    assert env.trading_authority is False
    assert env.capital_authority is False


def test_common_downstream_rebreak_p112d_to_p116c(tmp_path: Path):
    case=build_owner_case(tmp_path)
    env=case["envelope"]
    qei=case["qei"]
    measurement=CommonExperimentMeasurementClaim(
        measurement_id="AOE0-P1-OWNER-01-M1",
        metric="synthetic_execution_evidence_identity_length",
        observed_value=str(len(env.measurement_input_identity)),
        unit="hex_chars",
        sample_size=1,
        scope="AO-E0-P1-OWNER-01-SYNTHETIC-ONLY",
        rationale="Lineage-only synthetic rebreak; no market-behavior conclusion.",
    )
    evaluation=submit_common_experiment_evaluation(
        env,qei,
        evaluator_id="evaluator:ao-e0-p1-owner-01",
        method_ref="method:synthetic-lineage-only",
        measurements=(measurement,),
        prediction_status="SUPPORTED",
        falsification_status="NOT_FALSIFIED",
        evaluation_rationale="Synthetic downstream contract rebreak only.",
    )
    p114_record,p114_receipt,p114_pin,_,_=_p114c_files(tmp_path/"p114",env,evaluation)
    provenance=reattest_common_measurement_provenance(
        env,evaluation,p114_record,p114_receipt,
        expected_authority_id=DERIVATION_AUTHORITY,
        expected_receipt_sha256=p114_pin,
    )
    p115_record,p115_receipt,p115_pin,_,_=_p115c_files(tmp_path/"p115",evaluation,provenance)
    authority=reattest_common_evaluator_authority(
        evaluation,provenance,p115_record,p115_receipt,
        expected_authority_id=EVALUATION_AUTHORITY,
        expected_receipt_sha256=p115_pin,
    )
    finding=interpret_common_qualified_finding(evaluation,authority)
    assert env.execution_owner_id==evaluation.execution_owner_id==provenance.execution_owner_id==authority.execution_owner_id==finding.execution_owner_id=="P1.12C.AO-E0"
    assert finding.scientific_authority is False
    assert finding.operational_authority is False
    assert finding.trading_authority is False
    assert finding.capital_authority is False


def test_frozen_attack_table():
    expected={
        "AOE0-P1-B01":"BLOCKED_CELL_IDENTITY_MISMATCH",
        "AOE0-P1-B02":"BLOCKED_CLAIM_CLASS_MISMATCH",
        "AOE0-P1-B03":"BLOCKED_INVOCATION_PROFILE_MISMATCH",
        "AOE0-P1-B04":"BLOCKED_DATA_BINDING_MISMATCH",
        "AOE0-P1-B05":"BLOCKED_TEMPORAL_BINDING_MISMATCH",
        "AOE0-P1-B06":"BLOCKED_TEMPORAL_RULE_VIOLATION",
        "AOE0-P1-B07":"BLOCKED_OOS_CONSUMPTION",
        "AOE0-P1-B08":"BLOCKED_POST_RESULT_PRODUCER_SELECTION",
        "AOE0-P1-B09":"BLOCKED_POST_RESULT_PARAMETER_SELECTION",
        "AOE0-P1-B10":"BLOCKED_PRODUCER_CODE_DRIFT",
        "AOE0-P1-B11":"BLOCKED_RUNTIME_LOCK_DRIFT",
        "AOE0-P1-B12":"BLOCKED_INVOCATION_PROFILE_DRIFT",
        "AOE0-P1-B13":"BLOCKED_EXECUTION_MODEL_DRIFT",
        "AOE0-P1-B14":"BLOCKED_COST_SCOPE_DRIFT",
        "AOE0-P1-B15":"BLOCKED_COST_NODE_DRIFT",
        "AOE0-P1-B16":"BLOCKED_UNKNOWN_EXECUTION_OWNER",
        "AOE0-P1-B17":"BLOCKED_NATIVE_OWNER_ATTESTATION_REQUIRED",
        "AOE0-P1-B18":"REJECT_STRUCTURAL_DUCK_TYPING",
        "AOE0-P1-B19":"REJECT_OWNER_ALLOWLIST_LAUNDERING",
        "AOE0-P1-B20":"REJECT_RESULT_TO_SCIENTIFIC_AUTHORITY",
        "AOE0-P1-B21":"REJECT_EXECUTION_TO_TRADING_AUTHORITY",
        "AOE0-P1-B22":"BLOCKED_P1_12B_REGRESSION",
        "AOE0-P1-B23":"BLOCKED_P1_12C_REGRESSION",
        "AOE0-P1-B24":"BLOCKED_P1_21_AP1_REGRESSION",
    }
    for case_id,reason in expected.items():
        assert owner.validate_attack(case_id)["reason"]==reason


def test_wrong_data_binding_blocks(tmp_path: Path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    data["raw_dataset"]="USTECH_PROFILE_MINUTE_CORE_V0_1"
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_DATA_BINDING_MISMATCH"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal)


def test_retrospective_temporal_substitution_blocks(tmp_path: Path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    temporal["temporal_mode"]="RETROSPECTIVE_DESCRIPTIVE_ONLY"
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_TEMPORAL_BINDING_MISMATCH"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal)


def test_oos_and_post_result_selection_block(tmp_path: Path):
    qei=build_case(tmp_path/"qei")["qualified_input"]
    profile=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    runtime=owner.qualify_ao_e0_runtime_lock(profile,runtime_evidence())
    data,temporal=owner.expected_bindings()
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_OOS_CONSUMPTION"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,oos_consumption=True)
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_POST_RESULT_PRODUCER_SELECTION"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,producer_selection_after_result=True)
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_POST_RESULT_PARAMETER_SELECTION"):
        owner.qualify_ao_e0_plan(qei,profile=profile,runtime_lock=runtime,data_binding=data,temporal_binding=temporal,parameter_selection_after_result=True)


def test_producer_and_runtime_drift_block():
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_PRODUCER_CODE_DRIFT"):
        owner.qualify_ao_e0_profile(producer_code_blob="0"*40)
    good=owner.qualify_ao_e0_profile(producer_code_blob=owner.PRODUCER_BLOB)
    bad=runtime_evidence(); bad["python_binary_sha256"]="not-a-sha"
    with pytest.raises(owner.AOE0P1OwnerBlocked,match="BLOCKED_RUNTIME_LOCK_DRIFT"):
        owner.qualify_ao_e0_runtime_lock(good,bad)


def test_forged_profile_result_and_duck_typing_block(tmp_path: Path):
    case=build_owner_case(tmp_path)
    forged_profile=copy.copy(case["profile"])
    assert not owner.is_factory_attested_ao_e0_profile(forged_profile)
    forged_result=copy.copy(case["result"])
    assert not owner.is_factory_attested_ao_e0_execution_result(forged_result)
    with pytest.raises(ValueError,match="factory attestation"):
        ext.normalize_ao_e0_execution(forged_result,case["qei"])
    class Duck:
        pass
    assert ext.validate_owner_candidate(Duck())=={
        "status":"BLOCKED","reason":"BLOCKED_UNKNOWN_EXECUTION_OWNER"
    }
    with pytest.raises(TypeError,match="unknown/structural"):
        ext.normalize_ao_e0_execution(Duck(),case["qei"])


def test_ap1_profile_is_not_ao_e0_profile():
    assert owner.PROFILE_ID!="P1_12C_AP1_CLAIM_SCOPED_V1"
    assert owner.PRODUCER_ID!="ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    assert owner.OUTPUT_SCHEMA!="ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"


def test_base_p112d_core_and_legacy_allowlist_remain_unchanged():
    assert ext.BASE_P112D_CONTRACT=="P1_12D_QUALIFIED_EXECUTION_EVIDENCE_ENVELOPE_V1"
    assert ext.BASE_ALLOWED_OWNERS==("P1.12B","P1.12C")
    assert ext.AO_E0_ALLOWED_OWNER=="P1.12C.AO-E0"
