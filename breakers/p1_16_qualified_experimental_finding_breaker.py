from __future__ import annotations

import copy
import gc
import hashlib
import importlib
import inspect
import json
import weakref
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_evaluation_submission import (
    ExperimentEvaluationSubmission,
    ExperimentMeasurementClaim,
    submit_experiment_evaluation,
)
from src.experiment_evaluator_authority import (
    CONTRACT as P115B_CONTRACT,
    RECORD_SCHEMA as P115B_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P115B_RECEIPT_SCHEMA,
    QualifiedExperimentEvaluationAuthority,
    reattest_experiment_evaluator_authority,
)
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_measurement_provenance import (
    CONTRACT as P114B_CONTRACT,
    RECORD_SCHEMA as P114B_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P114B_RECEIPT_SCHEMA,
    reattest_measurement_provenance,
)
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.linked_experiment_execution import run_linked_experiment
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.qualified_experiment_execution_input import qualify_experiment_execution_input
from src.research.input_binding import bind_execution_input
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P116_CONTRACT = "P1_16_QUALIFIED_EXPERIMENTAL_FINDING_INTERPRETATION_BOUNDARY_V1"
P116_POLICY = "P1_16_FINDING_INTERPRETATION_POLICY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"

MEMORY_AUTHORITY = "P1_16_TEST_CAPTURE_AUTHORITY_V1"
DERIVATION_AUTHORITY = "measurement-authority:p1.16"
EVALUATION_AUTHORITY = "evaluation-authority:p1.16"
DERIVATION_NONCE = "ab" * 32
EVALUATION_NONCE = "cd" * 32

STATUS_CASES = (
    (
        "SUPPORTED",
        "NOT_FALSIFIED",
        "SUPPORTED",
        "PREDICTION_SUPPORTED_AND_NOT_FALSIFIED",
    ),
    (
        "NOT_SUPPORTED",
        "FALSIFIED",
        "REFUTED",
        "PREDICTION_NOT_SUPPORTED_AND_FALSIFIED",
    ),
    (
        "SUPPORTED",
        "FALSIFIED",
        "NOT_INTERPRETABLE",
        "CONTRADICTORY_EVALUATION_STATUSES",
    ),
    (
        "NOT_SUPPORTED",
        "NOT_FALSIFIED",
        "NOT_INTERPRETABLE",
        "NON_DECISIVE_EVALUATION_STATUSES",
    ),
    (
        "SUPPORTED",
        "BLOCKED",
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    (
        "NOT_SUPPORTED",
        "BLOCKED",
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    (
        "BLOCKED",
        "FALSIFIED",
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    (
        "BLOCKED",
        "NOT_FALSIFIED",
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    (
        "BLOCKED",
        "BLOCKED",
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
)


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p116():
    try:
        module = importlib.import_module("src.qualified_experimental_finding")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.16 candidate absent — expected pre-implementation FAIL: "
            "src.qualified_experimental_finding does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "QualifiedExperimentalFinding",
        "interpret_qualified_experimental_finding",
        "is_factory_attested_qualified_experimental_finding",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.16 candidate surface incomplete: {missing}", pytrace=False)

    assert getattr(module, "CONTRACT", None) == P116_CONTRACT
    assert getattr(module, "POLICY", None) == P116_POLICY
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _p116()


def _historical(tmp_path: Path, *, tag: str) -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="OBSERVED")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)

    authority_id = f"{MEMORY_AUTHORITY}:{tag}"
    capture = persist_witnessed_memory_episode(
        tmp_path,
        episode,
        authority_id=authority_id,
    )
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=authority_id,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _request(tmp_path: Path, *, tag: str):
    memory = _historical(tmp_path / "memory", tag=tag)
    scope = create_audit_scope(
        question=f"Which finding interpretation is valid for {tag}?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    audit = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        audit,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        f"Execute exact experiment for finding interpretation {tag}.",
    )
    return produce_follow_up_request(revision)


def _execution_and_submission(
    tmp_path: Path,
    *,
    tag: str,
    prediction_status: str,
    falsification_status: str,
):
    with synthetic_runtime_case() as case:
        specification = specify_experiment(
            _request(tmp_path, tag=tag),
            hypothesis_statement=f"H:{tag}",
            prediction=f"P:{tag}",
            falsification_rule=f"F:{tag}",
            protocol=f"Protocol:{tag}",
            measurement_plan=f"Measure exact metrics:{tag}",
        )
        bound = bind_execution_input(
            case.corpus_root,
            case.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        binding = bind_experiment_execution(specification, bound)
        qualified = qualify_experiment_execution_input(binding)
        execution_result = run_linked_experiment(qualified)

    measurements = (
        ExperimentMeasurementClaim(
            measurement_id=f"M-{tag}-1",
            metric="mean_return",
            observed_value="0.42",
            unit="ratio",
            sample_size=10,
            scope=f"synthetic:{tag}",
            rationale="Derived under external procedure.",
        ),
        ExperimentMeasurementClaim(
            measurement_id=f"M-{tag}-2",
            metric="max_drawdown",
            observed_value="-0.10",
            unit="ratio",
            sample_size=10,
            scope=f"synthetic:{tag}",
            rationale="Derived under external procedure.",
        ),
    )
    submission = submit_experiment_evaluation(
        execution_result,
        evaluator_id=f"evaluator:{tag}",
        method_ref=f"method:{tag}",
        measurements=measurements,
        prediction_status=prediction_status,
        falsification_status=falsification_status,
        evaluation_rationale=f"Evaluation submitted for {tag}.",
    )
    return execution_result, submission


def _p114b_provenance_id(execution_result, submission, record_sha256: str) -> str:
    payload = {
        "contract_id": P114B_CONTRACT,
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha256,
    }
    return "WMP-" + _sha256(_canonical(payload))[:32]


def _derivations(execution_result, submission):
    return [
        {
            "measurement_id": claim.measurement_id,
            "metric": claim.metric,
            "observed_value": claim.observed_value,
            "unit": claim.unit,
            "sample_size": claim.sample_size,
            "scope": claim.scope,
            "rationale": claim.rationale,
            "procedure_ref": f"procedure:{claim.measurement_id}",
            "procedure_sha256": _sha256(f"procedure:{claim.measurement_id}".encode("utf-8")),
            "input_stream_sha256": execution_result.stream_sha256,
        }
        for claim in submission.measurements
    ]


def _p114b_files(tmp_path: Path, execution_result, submission):
    record = {
        "schema": P114B_RECORD_SCHEMA,
        "contract_id": P114B_CONTRACT,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "experiment_spec_id": execution_result.experiment_spec_id,
        "stream_sha256": execution_result.stream_sha256,
        "method_ref": submission.method_ref,
        "derivations": _derivations(execution_result, submission),
    }
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)

    receipt = {
        "schema": P114B_RECEIPT_SCHEMA,
        "contract_id": P114B_CONTRACT,
        "authority_id": DERIVATION_AUTHORITY,
        "derivation_nonce": DERIVATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha256,
        "provenance_qualification_id": _p114b_provenance_id(
            execution_result,
            submission,
            record_sha256,
        ),
    }
    receipt_bytes = _canonical(receipt)

    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "measurement.record.json"
    receipt_path = tmp_path / "measurement.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


def _p115b_qualification_id(submission, provenance, record_sha256: str) -> str:
    payload = {
        "contract_id": P115B_CONTRACT,
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
    }
    return "QEA-" + _sha256(_canonical(payload))[:32]


def _procedure_bindings(provenance):
    return [
        {
            "measurement_id": item.measurement_id,
            "procedure_ref": item.procedure_ref,
            "procedure_sha256": item.procedure_sha256,
        }
        for item in provenance.derivations
    ]


def _p115b_files(tmp_path: Path, submission, provenance):
    record = {
        "schema": P115B_RECORD_SCHEMA,
        "contract_id": P115B_CONTRACT,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "experiment_execution_result_id": submission.experiment_execution_result_id,
        "experiment_spec_id": submission.experiment_spec_id,
        "request_id": submission.request_id,
        "evaluator_id": submission.evaluator_id,
        "method_ref": submission.method_ref,
        "prediction_status": submission.prediction_status,
        "falsification_status": submission.falsification_status,
        "evaluation_rationale": submission.evaluation_rationale,
        "measurement_ids": [item.measurement_id for item in submission.measurements],
        "procedure_bindings": _procedure_bindings(provenance),
    }
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)

    receipt = {
        "schema": P115B_RECEIPT_SCHEMA,
        "contract_id": P115B_CONTRACT,
        "authority_id": EVALUATION_AUTHORITY,
        "qualification_nonce": EVALUATION_NONCE,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
        "qualification_id": _p115b_qualification_id(
            submission,
            provenance,
            record_sha256,
        ),
    }
    receipt_bytes = _canonical(receipt)

    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "evaluation-authority.record.json"
    receipt_path = tmp_path / "evaluation-authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


def _case(
    tmp_path: Path,
    *,
    tag: str,
    prediction_status: str = "SUPPORTED",
    falsification_status: str = "NOT_FALSIFIED",
):
    execution_result, submission = _execution_and_submission(
        tmp_path / "experiment",
        tag=tag,
        prediction_status=prediction_status,
        falsification_status=falsification_status,
    )

    p114b_record, p114b_receipt, p114b_pin = _p114b_files(
        tmp_path / "provenance",
        execution_result,
        submission,
    )
    provenance = reattest_measurement_provenance(
        execution_result,
        submission,
        p114b_record,
        p114b_receipt,
        expected_authority_id=DERIVATION_AUTHORITY,
        expected_receipt_sha256=p114b_pin,
    )

    p115b_record, p115b_receipt, p115b_pin = _p115b_files(
        tmp_path / "evaluation-authority",
        submission,
        provenance,
    )
    authority = reattest_experiment_evaluator_authority(
        submission,
        provenance,
        p115b_record,
        p115b_receipt,
        expected_authority_id=EVALUATION_AUTHORITY,
        expected_receipt_sha256=p115b_pin,
    )
    return submission, authority


def test_a0_exact_authoritative_chain_positive(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)
    assert result.evaluation_submission_id == submission.evaluation_submission_id
    assert result.evaluation_authority_qualification_id == authority.qualification_id
    assert _p116().is_factory_attested_qualified_experimental_finding(result)


def test_a1_non_authoritative_evaluation_rejected(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    variants = (
        submission.evaluation_submission_id,
        asdict(submission),
        ExperimentEvaluationSubmission(**asdict(submission)),
        copy.copy(submission),
        copy.deepcopy(submission),
        replace(submission, evaluation_submission_id=submission.evaluation_submission_id),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _p116().interpret_qualified_experimental_finding(value, authority)


def test_a2_non_authoritative_authority_rejected(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    variants = (
        authority.qualification_id,
        asdict(authority),
        QualifiedExperimentEvaluationAuthority(**asdict(authority)),
        copy.copy(authority),
        copy.deepcopy(authority),
        replace(authority, qualification_id=authority.qualification_id),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _p116().interpret_qualified_experimental_finding(submission, value)


def test_a3_mutated_upstreams_are_rejected_and_sticky(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")

    original_prediction = submission.prediction_status
    object.__setattr__(submission, "prediction_status", "BLOCKED")
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission, authority)
    object.__setattr__(submission, "prediction_status", original_prediction)
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission, authority)


def test_a4_cross_evaluation_authority_substitution_rejected(tmp_path: Path) -> None:
    submission_a, authority_a = _case(tmp_path / "a", tag="A")
    submission_b, authority_b = _case(tmp_path / "b", tag="B")

    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission_a, authority_b)
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission_b, authority_a)


def test_b0_signature_has_no_override_surface() -> None:
    sig = inspect.signature(_p116().interpret_qualified_experimental_finding)
    assert tuple(sig.parameters) == ("evaluation_submission", "evaluation_authority")
    for name in ("evaluation_submission", "evaluation_authority"):
        assert sig.parameters[name].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        assert sig.parameters[name].default is inspect.Parameter.empty


@pytest.mark.parametrize(
    "prediction_status,falsification_status,expected_finding,expected_code",
    STATUS_CASES,
)
def test_c0_all_nine_status_pairs_are_total_and_exact(
    tmp_path: Path,
    prediction_status: str,
    falsification_status: str,
    expected_finding: str,
    expected_code: str,
) -> None:
    tag = f"{prediction_status}-{falsification_status}"
    submission, authority = _case(
        tmp_path / tag,
        tag=tag,
        prediction_status=prediction_status,
        falsification_status=falsification_status,
    )
    result = _p116().interpret_qualified_experimental_finding(submission, authority)

    assert result.prediction_status == prediction_status
    assert result.falsification_status == falsification_status
    assert result.finding_status == expected_finding
    assert result.interpretation_code == expected_code
    assert result.policy_reference == P116_POLICY


@pytest.mark.parametrize(
    "prediction_status,falsification_status",
    (
        ("SUPPORTED", "FALSIFIED"),
        ("NOT_SUPPORTED", "NOT_FALSIFIED"),
        ("SUPPORTED", "BLOCKED"),
        ("NOT_SUPPORTED", "BLOCKED"),
        ("BLOCKED", "FALSIFIED"),
        ("BLOCKED", "NOT_FALSIFIED"),
        ("BLOCKED", "BLOCKED"),
    ),
)
def test_c1_non_decisive_pairs_never_promote(
    tmp_path: Path,
    prediction_status: str,
    falsification_status: str,
) -> None:
    tag = f"nondecisive-{prediction_status}-{falsification_status}"
    submission, authority = _case(
        tmp_path / tag,
        tag=tag,
        prediction_status=prediction_status,
        falsification_status=falsification_status,
    )
    result = _p116().interpret_qualified_experimental_finding(submission, authority)
    assert result.finding_status == "NOT_INTERPRETABLE"


def test_c2_policy_and_measurements_are_not_caller_overridable() -> None:
    sig = inspect.signature(_p116().interpret_qualified_experimental_finding)
    forbidden = {
        "finding_status",
        "interpretation_code",
        "policy_reference",
        "supporting_measurement_ids",
        "reason",
        "rule_reference",
    }
    assert forbidden.isdisjoint(sig.parameters)


def test_d0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p116().QualifiedExperimentalFinding)) == (
        "finding_id",
        "evaluation_submission_id",
        "evaluation_authority_qualification_id",
        "provenance_qualification_id",
        "experiment_execution_result_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "hypothesis_statement",
        "prediction",
        "falsification_rule",
        "supporting_measurement_ids",
        "prediction_status",
        "falsification_status",
        "finding_status",
        "interpretation_code",
        "policy_reference",
        "evaluator_id",
        "method_ref",
        "evaluation_rationale",
        "measurement_provenance_status",
        "evaluation_authority_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_d1_output_snapshots_exact_chain(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)

    assert result.evaluation_submission_id == submission.evaluation_submission_id
    assert result.evaluation_authority_qualification_id == authority.qualification_id
    assert result.provenance_qualification_id == authority.provenance_qualification_id
    assert result.experiment_execution_result_id == submission.experiment_execution_result_id
    assert result.experiment_spec_id == submission.experiment_spec_id
    assert result.request_id == submission.request_id
    assert result.revision_id == submission.revision_id
    assert result.audit_id == submission.audit_id
    assert result.scope_id == submission.scope_id
    assert result.hypothesis_statement == submission.hypothesis_statement
    assert result.prediction == submission.prediction
    assert result.falsification_rule == submission.falsification_rule
    assert result.supporting_measurement_ids == tuple(
        item.measurement_id for item in submission.measurements
    )
    assert result.evaluator_id == submission.evaluator_id
    assert result.method_ref == submission.method_ref
    assert result.evaluation_rationale == submission.evaluation_rationale
    assert result.measurement_provenance_status == "PASS"
    assert result.evaluation_authority_status == "PASS"


def test_d2_authority_measurement_membership_mutation_rejected(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    object.__setattr__(authority, "measurement_ids", tuple(reversed(authority.measurement_ids)))
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission, authority)


@pytest.mark.parametrize("field", ["evaluator_id", "method_ref"])
def test_d3_authority_identity_mutation_rejected(tmp_path: Path, field: str) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    object.__setattr__(authority, field, "MUTATED")
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission, authority)


@pytest.mark.parametrize(
    "field",
    ["source_verdict", "source_completeness_status", "source_independence_status"],
)
def test_d4_source_provenance_mutation_rejected(tmp_path: Path, field: str) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    object.__setattr__(authority, field, "MUTATED")
    with pytest.raises((TypeError, ValueError)):
        _p116().interpret_qualified_experimental_finding(submission, authority)


def test_e0_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    first = _p116().interpret_qualified_experimental_finding(submission, authority)
    second = _p116().interpret_qualified_experimental_finding(submission, authority)

    assert first == second and first is not second
    assert first.finding_id.startswith("QXF-")
    assert first.finding_id == second.finding_id
    assert _p116().is_factory_attested_qualified_experimental_finding(first)
    assert _p116().is_factory_attested_qualified_experimental_finding(second)


def test_e1_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)
    cls = _p116().QualifiedExperimentalFinding

    assert not _p116().is_factory_attested_qualified_experimental_finding(cls(**asdict(result)))
    assert not _p116().is_factory_attested_qualified_experimental_finding(copy.copy(result))
    assert not _p116().is_factory_attested_qualified_experimental_finding(copy.deepcopy(result))
    assert not _p116().is_factory_attested_qualified_experimental_finding(
        replace(result, finding_id=result.finding_id)
    )


def test_e2_mutation_then_restore_sticky_invalid(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)
    original = result.finding_status

    object.__setattr__(result, "finding_status", "MUTATED")
    assert not _p116().is_factory_attested_qualified_experimental_finding(result)
    object.__setattr__(result, "finding_status", original)
    assert not _p116().is_factory_attested_qualified_experimental_finding(result)


def test_e3_upstreams_can_be_collected(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)

    refs = (weakref.ref(submission), weakref.ref(authority))
    del submission
    del authority
    gc.collect()

    assert all(ref() is None for ref in refs)
    assert _p116().is_factory_attested_qualified_experimental_finding(result)


def test_f0_no_research_container_knowledge_or_operational_surface() -> None:
    module = _p116()
    source = inspect.getsource(module)

    forbidden_attrs = (
        "produce_research_finding",
        "produce_research_findings",
        "create_research_run_evidence",
        "promote_to_knowledge",
        "create_knowledge",
        "authorize",
        "activate_live",
        "run_backtest",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)

    forbidden_tokens = (
        "ResearchFinding(",
        "ResearchFindings(",
        "ResearchRunEvidence(",
        "run_qualified_research",
        "order_send",
        "MetaTrader5",
        "requests.",
        "socket.",
        "subprocess.",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_f1_finding_id_alone_is_not_attestation(tmp_path: Path) -> None:
    submission, authority = _case(tmp_path / "case", tag="A")
    result = _p116().interpret_qualified_experimental_finding(submission, authority)
    assert not _p116().is_factory_attested_qualified_experimental_finding(result.finding_id)
