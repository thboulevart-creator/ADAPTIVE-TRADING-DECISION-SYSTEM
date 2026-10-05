"""P1-18 positive and runtime fail-closed qualification tests."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from src import p1_12c_qualified_producer_execution as p12c
from src.experiment_evaluation_submission import submit_experiment_evaluation
from src.linked_experiment_execution import LinkedExperimentExecutionResult
from tests.p1_18_fixture import (
    OUTPUT_SCHEMA,
    OUTPUT_STATUS,
    PRODUCER_ID,
    SYNTHETIC_PRODUCER,
    build_case,
)


def test_p118_01_plan_is_factory_attested_and_non_authoritative(tmp_path: Path):
    case = build_case(tmp_path)
    plan = case["plan"]
    assert p12c.is_factory_attested_qualified_producer_execution_plan(plan)
    assert plan.producer_id == PRODUCER_ID
    assert plan.producer_code_blob == "06d48e6253e6f94cb3eebf3aa53f3fd96a5ad7b0"
    assert plan.expected_output_schema == OUTPUT_SCHEMA
    assert plan.expected_output_status == OUTPUT_STATUS
    assert plan.result_exposed is False
    assert plan.scientific_authority is False
    assert plan.trading_authority is False
    assert p12c.CAPABILITIES["real_ap1_authority"] is False


def test_p118_02_positive_synthetic_execution_mints_distinct_p112c_result(tmp_path: Path):
    case = build_case(tmp_path)
    result = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    assert p12c.is_factory_attested_qualified_producer_execution_result(result)
    assert result.execution_status == "EXECUTED"
    assert result.exit_code == 0
    assert result.output_schema == OUTPUT_SCHEMA
    assert result.output_status == OUTPUT_STATUS
    assert result.dataset_file_set_digest_before == result.dataset_file_set_digest_after
    assert result.producer_execution_result_id.startswith("QPER-")
    assert result.result_identity == result.producer_execution_result_id
    assert len(result.data02_result_binding_digest) == 64
    assert result.scientific_authority is False
    assert result.operational_authority is False
    assert result.trading_authority is False
    assert result.capital_authority is False


def test_p118_03_same_plan_source_runtime_and_parameters_replay_identically(tmp_path: Path):
    case = build_case(tmp_path)
    first = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    second = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    assert first.producer_execution_result_id == second.producer_execution_result_id
    assert first.output_sha256 == second.output_sha256
    assert first.reconstruction_descriptor_digest == second.reconstruction_descriptor_digest
    assert first.producer_stdout_digest == second.producer_stdout_digest
    assert first.producer_stderr_digest == second.producer_stderr_digest


def test_p118_04_transport_path_is_not_plan_identity(tmp_path: Path):
    producer_a = tmp_path / "a" / "producer.py"
    producer_b = tmp_path / "b" / "producer.py"
    producer_a.parent.mkdir()
    producer_b.parent.mkdir()
    raw = SYNTHETIC_PRODUCER.read_bytes()
    producer_a.write_bytes(raw)
    producer_b.write_bytes(raw)

    case_a = build_case(tmp_path / "case", producer_path=producer_a)
    # Reuse the same qualified owner inputs and bind an identical producer at another transport path.
    plan_b = p12c.qualify_producer_execution_plan(
        case_a["qualified_input"],
        case_a["admission"],
        producer_id=PRODUCER_ID,
        producer_path=producer_b,
        semantic_parameters={
            "mode": "normal",
            "qualification_scope": "P1-18-SYNTHETIC-ONLY",
            "market_semantics": "NONE",
        },
        expected_output_schema=OUTPUT_SCHEMA,
        expected_output_status=OUTPUT_STATUS,
        expected_output_contract="P1_18_SYNTHETIC_BYTE_INVENTORY_RESULT_V0_1",
        maximum_output_bytes=1024 * 1024,
    )
    assert case_a["plan"].producer_code_blob == plan_b.producer_code_blob
    assert case_a["plan"].producer_execution_plan_digest == plan_b.producer_execution_plan_digest
    assert case_a["plan"].producer_execution_plan_id == plan_b.producer_execution_plan_id
    assert case_a["plan"].producer_path_transport != plan_b.producer_path_transport


def test_p118_05_producer_code_drift_blocks_before_execution(tmp_path: Path):
    producer = tmp_path / "producer.py"
    producer.write_bytes(SYNTHETIC_PRODUCER.read_bytes())
    case = build_case(tmp_path / "case", producer_path=producer)
    producer.write_text(producer.read_text(encoding="utf-8") + "\n# drift\n", encoding="utf-8")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_PRODUCER_CODE_DRIFT"):
        p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])


def test_p118_06_unattested_plan_copy_cannot_execute(tmp_path: Path):
    case = build_case(tmp_path)
    forged = replace(case["plan"])
    assert not p12c.is_factory_attested_qualified_producer_execution_plan(forged)
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_UNATTESTED_PRODUCER_PLAN"):
        p12c.run_qualified_producer(forged, case["qualified_input"], case["admission"])


def test_p118_07_actual_source_mutation_by_test_producer_is_detected(tmp_path: Path):
    case = build_case(tmp_path, mode="mutate_source")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_SOURCE_MUTATION_DURING_PRODUCER_EXECUTION"):
        p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])


def test_p118_08_network_attempt_is_blocked_by_sandbox_runner(tmp_path: Path):
    case = build_case(tmp_path, mode="network_attempt")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_PRODUCER_EXECUTION_FAILED"):
        p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])


def test_p118_09_child_process_attempt_is_blocked_by_sandbox_runner(tmp_path: Path):
    case = build_case(tmp_path, mode="child_process_attempt")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_PRODUCER_EXECUTION_FAILED"):
        p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])


def test_p118_10_invalid_output_status_is_not_executed_result(tmp_path: Path):
    case = build_case(tmp_path, mode="invalid_status")
    with pytest.raises(p12c.P112CBlocked, match="BLOCKED_PRODUCER_OUTPUT_STATUS_MISMATCH"):
        p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])


def test_p118_11_p112c_result_is_not_legacy_p112b_result(tmp_path: Path):
    case = build_case(tmp_path)
    result = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    assert type(result) is not LinkedExperimentExecutionResult


def test_p118_12_existing_p113b_rejects_p112c_result_without_owner_change(tmp_path: Path):
    case = build_case(tmp_path)
    result = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    with pytest.raises(TypeError, match="P1.13B requires exact LinkedExperimentExecutionResult"):
        submit_experiment_evaluation(
            result,
            evaluator_id="p1-18-not-authorized",
            method_ref="not-authorized",
            measurements=(),
            prediction_status="SUPPORTED",
            falsification_status="NOT_FALSIFIED",
            evaluation_rationale="must not reach evaluation validation",
        )


def test_p118_13_data_owner_status_is_not_rewritten_by_execution(tmp_path: Path):
    case = build_case(tmp_path)
    before = dict(case["admission"])
    result = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    assert case["admission"] == before
    assert case["admission"]["status"] == "READY_FOR_EXACT_CLAIM"
    assert result.execution_status == "EXECUTED"


def test_p118_14_runtime_lock_is_pre_result_and_stable_within_environment(tmp_path: Path):
    case = build_case(tmp_path)
    plan = case["plan"]
    lock = p12c.build_current_runtime_lock()
    assert plan.runtime_lock_digest == lock["runtime_lock_digest"]
    assert plan.result_exposed is False
    assert lock["material_third_party_dependencies"] == []
    assert lock["timezone_database_identity"] == "NOT_USED_BY_SYNTHETIC_PRODUCER"


def test_p118_15_semantic_parameter_change_changes_plan_identity(tmp_path: Path):
    case = build_case(tmp_path)
    changed = p12c.qualify_producer_execution_plan(
        case["qualified_input"],
        case["admission"],
        producer_id=PRODUCER_ID,
        producer_path=SYNTHETIC_PRODUCER,
        semantic_parameters={
            "mode": "normal",
            "qualification_scope": "P1-18-SYNTHETIC-ONLY",
            "market_semantics": "NONE",
            "extra": "different",
        },
        expected_output_schema=OUTPUT_SCHEMA,
        expected_output_status=OUTPUT_STATUS,
        expected_output_contract="P1_18_SYNTHETIC_BYTE_INVENTORY_RESULT_V0_1",
        maximum_output_bytes=1024 * 1024,
    )
    assert changed.producer_semantic_parameter_digest != case["plan"].producer_semantic_parameter_digest
    assert changed.producer_execution_plan_digest != case["plan"].producer_execution_plan_digest


def test_p118_16_success_does_not_claim_ap1_or_real_cc02_readiness(tmp_path: Path):
    case = build_case(tmp_path)
    result = p12c.run_qualified_producer(case["plan"], case["qualified_input"], case["admission"])
    assert result.producer_id == PRODUCER_ID
    assert result.producer_id != "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    assert p12c.CAPABILITIES["real_ap1_authority"] is False
    assert p12c.validate_boundary_claim("RESULT_TO_SCIENTIFIC_SUPPORT")["status"] == "REJECTED"
