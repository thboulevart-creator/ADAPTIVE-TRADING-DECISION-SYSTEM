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
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.linked_experiment_execution import (
    LinkedExperimentExecutionResult,
    run_linked_experiment,
)
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


P114B_CONTRACT = "P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1"
P114B_RECORD_SCHEMA = "P1_14B_MEASUREMENT_DERIVATION_RECORD_V1"
P114B_RECEIPT_SCHEMA = "P1_14B_MEASUREMENT_DERIVATION_RECEIPT_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
MEMORY_AUTHORITY = "P1_14B_TEST_CAPTURE_AUTHORITY_V1"
DERIVATION_AUTHORITY = "measurement-authority:test"
NONCE = "cd" * 32


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p114b():
    try:
        module = importlib.import_module("src.experiment_measurement_provenance")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.14B candidate absent — expected pre-implementation FAIL: "
            "src.experiment_measurement_provenance does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "WitnessedMeasurementDerivation",
        "WitnessedMeasurementProvenance",
        "reattest_measurement_provenance",
        "is_factory_attested_witnessed_measurement_provenance",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.14B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P114B_CONTRACT
    assert getattr(module, "RECORD_SCHEMA", None) == P114B_RECORD_SCHEMA
    assert getattr(module, "RECEIPT_SCHEMA", None) == P114B_RECEIPT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _p114b()


def _historical(tmp_path: Path) -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="OBSERVED")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=MEMORY_AUTHORITY)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=MEMORY_AUTHORITY,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _request(tmp_path: Path):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which experiment measurement provenance is required?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    audit = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        audit,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Execute and evaluate one exact synthetic experiment.",
    )
    return produce_follow_up_request(revision)


def _execution_and_submission(tmp_path: Path):
    with synthetic_runtime_case() as case:
        specification = specify_experiment(
            _request(tmp_path),
            hypothesis_statement="H",
            prediction="P",
            falsification_rule="F",
            protocol="Protocol",
            measurement_plan="Measure mean return.",
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
            measurement_id="M-1",
            metric="mean_return",
            observed_value="0.42",
            unit="ratio",
            sample_size=10,
            scope="synthetic",
            rationale="Derived under external procedure.",
        ),
        ExperimentMeasurementClaim(
            measurement_id="M-2",
            metric="max_drawdown",
            observed_value="-0.10",
            unit="ratio",
            sample_size=10,
            scope="synthetic",
            rationale="Derived under external procedure.",
        ),
    )
    submission = submit_experiment_evaluation(
        execution_result,
        evaluator_id="evaluator:test",
        method_ref="method:test",
        measurements=measurements,
        prediction_status="SUPPORTED",
        falsification_status="NOT_FALSIFIED",
        evaluation_rationale="Evaluation submitted without promotion.",
    )
    return execution_result, submission


def _provenance_id(
    execution_result,
    submission,
    record_sha256: str,
    *,
    authority_id=DERIVATION_AUTHORITY,
    nonce=NONCE,
):
    payload = {
        "contract_id": P114B_CONTRACT,
        "authority_id": authority_id,
        "derivation_nonce": nonce,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha256,
    }
    return "WMP-" + _sha256(_canonical(payload))[:32]


def _derivations(execution_result, submission):
    result = []
    for index, claim in enumerate(submission.measurements, start=1):
        result.append(
            {
                "measurement_id": claim.measurement_id,
                "metric": claim.metric,
                "observed_value": claim.observed_value,
                "unit": claim.unit,
                "sample_size": claim.sample_size,
                "scope": claim.scope,
                "rationale": claim.rationale,
                "procedure_ref": f"procedure:test:{index}",
                "procedure_sha256": _sha256(f"procedure-{index}".encode("utf-8")),
                "input_stream_sha256": execution_result.stream_sha256,
            }
        )
    return result


def _provenance_files(
    tmp_path: Path,
    execution_result,
    submission,
    *,
    authority_id=DERIVATION_AUTHORITY,
    nonce=NONCE,
    record_mutator=None,
    receipt_mutator=None,
):
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
    if record_mutator is not None:
        record_mutator(record)
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)
    provenance_qualification_id = _provenance_id(
        execution_result,
        submission,
        record_sha256,
        authority_id=authority_id,
        nonce=nonce,
    )
    receipt = {
        "schema": P114B_RECEIPT_SCHEMA,
        "contract_id": P114B_CONTRACT,
        "authority_id": authority_id,
        "derivation_nonce": nonce,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "stream_sha256": execution_result.stream_sha256,
        "record_sha256": record_sha256,
        "provenance_qualification_id": provenance_qualification_id,
    }
    if receipt_mutator is not None:
        receipt_mutator(receipt)
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "measurement.record.json"
    receipt_path = tmp_path / "measurement.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


def _reattest(execution_result, submission, paths, *, authority_id=DERIVATION_AUTHORITY, pin=None):
    record_path, receipt_path, receipt_sha256 = paths
    return _p114b().reattest_measurement_provenance(
        execution_result,
        submission,
        record_path,
        receipt_path,
        expected_authority_id=authority_id,
        expected_receipt_sha256=receipt_sha256 if pin is None else pin,
    )


def test_a0_exact_upstreams_positive(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    assert result.evaluation_submission_id == submission.evaluation_submission_id
    assert result.stream_sha256 == execution_result.stream_sha256
    assert _p114b().is_factory_attested_witnessed_measurement_provenance(result)


def test_a1_non_authoritative_execution_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission)
    variants = (
        execution_result.experiment_execution_result_id,
        asdict(execution_result),
        LinkedExperimentExecutionResult(**asdict(execution_result)),
        copy.copy(execution_result),
        copy.deepcopy(execution_result),
        replace(
            execution_result,
            experiment_execution_result_id=execution_result.experiment_execution_result_id,
        ),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _reattest(value, submission, paths)


def test_a2_non_authoritative_submission_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission)
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
            _reattest(execution_result, value, paths)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p114b().reattest_measurement_provenance)
    assert tuple(sig.parameters) == (
        "execution_result",
        "evaluation_submission",
        "record_path",
        "receipt_path",
        "expected_authority_id",
        "expected_receipt_sha256",
    )
    for name in ("execution_result", "evaluation_submission", "record_path", "receipt_path"):
        assert sig.parameters[name].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("expected_authority_id", "expected_receipt_sha256"):
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_c0_cross_execution_submission_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "one")
    foreign_execution, foreign_submission = _execution_and_submission(tmp_path / "two")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission)
    with pytest.raises((TypeError, ValueError)):
        _reattest(foreign_execution, submission, paths)
    with pytest.raises((TypeError, ValueError)):
        _reattest(execution_result, foreign_submission, paths)


@pytest.mark.parametrize("field", ["metric", "observed_value", "unit", "sample_size", "scope", "rationale"])
def test_c1_claim_mismatch_rejected(tmp_path: Path, field: str) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    def mutate(record):
        record["derivations"][0][field] = "WRONG" if field != "sample_size" else 999
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, record_mutator=mutate)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


def test_c2_derivation_order_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    def mutate(record):
        record["derivations"] = list(reversed(record["derivations"]))
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, record_mutator=mutate)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


def test_c3_missing_or_extra_derivation_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    for mode in ("missing", "extra"):
        def mutate(record, mode=mode):
            if mode == "missing":
                record["derivations"] = record["derivations"][:-1]
            else:
                record["derivations"] = record["derivations"] + [dict(record["derivations"][0])]
        paths = _provenance_files(tmp_path / mode, execution_result, submission, record_mutator=mutate)
        with pytest.raises(ValueError):
            _reattest(execution_result, submission, paths)


@pytest.mark.parametrize("field", ["stream_sha256", "method_ref", "experiment_spec_id"])
def test_d0_record_identity_mismatch_rejected(tmp_path: Path, field: str) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    def mutate(record):
        record[field] = "0" * 64 if field == "stream_sha256" else "WRONG"
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, record_mutator=mutate)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


def test_d1_each_derivation_must_bind_exact_stream(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    def mutate(record):
        record["derivations"][0]["input_stream_sha256"] = "0" * 64
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, record_mutator=mutate)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


@pytest.mark.parametrize("field,bad", [
    ("procedure_ref", ""),
    ("procedure_ref", 1),
    ("procedure_sha256", ""),
    ("procedure_sha256", "0" * 63),
    ("procedure_sha256", "G" * 64),
])
def test_d2_procedure_identity_validation(tmp_path: Path, field: str, bad) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    def mutate(record):
        record["derivations"][0][field] = bad
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, record_mutator=mutate)
    with pytest.raises((TypeError, ValueError)):
        _reattest(execution_result, submission, paths)


def test_e0_wrong_external_pin_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths, pin="0" * 64)


def test_e1_wrong_authority_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(
        tmp_path / "prov", execution_result, submission, authority_id="other-authority"
    )
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths, authority_id=DERIVATION_AUTHORITY)


@pytest.mark.parametrize("nonce", ["", "cd", "z" * 64])
def test_e2_invalid_nonce_rejected(tmp_path: Path, nonce: str) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission, nonce=nonce)
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


def test_e3_noncanonical_record_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    record_path, receipt_path, pin = _provenance_files(
        tmp_path / "prov", execution_result, submission
    )
    parsed = json.loads(record_path.read_text("utf-8"))
    record_path.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, (record_path, receipt_path, pin))


def test_e4_tampered_provenance_id_rejected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(
        tmp_path / "prov",
        execution_result,
        submission,
        receipt_mutator=lambda receipt: receipt.__setitem__(
            "provenance_qualification_id", "WMP-" + "0" * 32
        ),
    )
    with pytest.raises(ValueError):
        _reattest(execution_result, submission, paths)


def test_f0_derivation_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p114b().WitnessedMeasurementDerivation)) == (
        "measurement_id",
        "metric",
        "observed_value",
        "unit",
        "sample_size",
        "scope",
        "rationale",
        "procedure_ref",
        "procedure_sha256",
        "input_stream_sha256",
    )


def test_f1_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p114b().WitnessedMeasurementProvenance)) == (
        "provenance_qualification_id",
        "evaluation_submission_id",
        "experiment_execution_result_id",
        "experiment_execution_input_id",
        "execution_binding_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "stream_sha256",
        "method_ref",
        "derivations",
        "authority_id",
        "record_sha256",
        "receipt_sha256",
        "measurement_provenance_status",
        "evaluation_authority_status",
        "finding_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_f2_provenance_pass_but_evaluator_and_finding_blocked(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    assert result.measurement_provenance_status == "PASS"
    assert result.evaluation_authority_status == "BLOCKED"
    assert result.finding_status == "BLOCKED"


def test_g0_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    paths = _provenance_files(tmp_path / "prov", execution_result, submission)
    first = _reattest(execution_result, submission, paths)
    second = _reattest(execution_result, submission, paths)
    assert first == second and first is not second
    assert first.provenance_qualification_id.startswith("WMP-")
    assert first.provenance_qualification_id == second.provenance_qualification_id
    assert _p114b().is_factory_attested_witnessed_measurement_provenance(first)
    assert _p114b().is_factory_attested_witnessed_measurement_provenance(second)


def test_g1_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    cls = _p114b().WitnessedMeasurementProvenance
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(cls(**asdict(result)))
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(copy.copy(result))
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(copy.deepcopy(result))
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(
        replace(result, provenance_qualification_id=result.provenance_qualification_id)
    )


def test_g2_mutation_then_restore_sticky_invalid(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    original = result.measurement_provenance_status
    object.__setattr__(result, "measurement_provenance_status", "MUTATED")
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(result)
    object.__setattr__(result, "measurement_provenance_status", original)
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(result)


def test_g3_upstream_objects_can_be_collected(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    refs = (weakref.ref(execution_result), weakref.ref(submission))
    del execution_result
    del submission
    gc.collect()
    assert all(ref() is None for ref in refs)
    assert _p114b().is_factory_attested_witnessed_measurement_provenance(result)


def test_h0_no_witness_producer_execution_or_promotion_surface() -> None:
    module = _p114b()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "create_derivation_record",
        "persist_measurement_witness",
        "produce_finding",
        "produce_findings",
        "create_research_run_evidence",
        "run_backtest",
        "activate_live",
        "authorize",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "run_qualified_research",
        "ResearchFinding(",
        "ResearchFindings(",
        "ResearchRunEvidence(",
        "order_send",
        "MetaTrader5",
        "requests.",
        "socket.",
        "subprocess.",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_provenance_id_alone_is_not_authority(tmp_path: Path) -> None:
    execution_result, submission = _execution_and_submission(tmp_path / "case")
    result = _reattest(
        execution_result,
        submission,
        _provenance_files(tmp_path / "prov", execution_result, submission),
    )
    assert not _p114b().is_factory_attested_witnessed_measurement_provenance(
        result.provenance_qualification_id
    )
