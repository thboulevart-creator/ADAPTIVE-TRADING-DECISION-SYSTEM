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
from src.experiment_measurement_provenance import (
    CONTRACT as P114B_CONTRACT,
    RECORD_SCHEMA as P114B_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P114B_RECEIPT_SCHEMA,
    WitnessedMeasurementProvenance,
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


P115B_CONTRACT = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1"
P115B_RECORD_SCHEMA = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECORD_V1"
P115B_RECEIPT_SCHEMA = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECEIPT_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
MEMORY_AUTHORITY = "P1_15B_TEST_CAPTURE_AUTHORITY_V1"
DERIVATION_AUTHORITY = "measurement-authority:p1.15b"
EVALUATION_AUTHORITY = "evaluation-authority:p1.15b"
DERIVATION_NONCE = "ab" * 32
EVALUATION_NONCE = "cd" * 32


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p115b():
    try:
        module = importlib.import_module("src.experiment_evaluator_authority")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.15B candidate absent — expected pre-implementation FAIL: "
            "src.experiment_evaluator_authority does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "QualifiedExperimentEvaluationAuthority",
        "reattest_experiment_evaluator_authority",
        "is_factory_attested_qualified_experiment_evaluation_authority",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.15B candidate surface incomplete: {missing}", pytrace=False)

    assert getattr(module, "CONTRACT", None) == P115B_CONTRACT
    assert getattr(module, "RECORD_SCHEMA", None) == P115B_RECORD_SCHEMA
    assert getattr(module, "RECEIPT_SCHEMA", None) == P115B_RECEIPT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _p115b()


def _historical(tmp_path: Path, *, tag: str) -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="OBSERVED")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)

    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=f"{MEMORY_AUTHORITY}:{tag}")
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=f"{MEMORY_AUTHORITY}:{tag}",
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _request(tmp_path: Path, *, tag: str):
    memory = _historical(tmp_path / "memory", tag=tag)
    scope = create_audit_scope(
        question=f"Which evaluator authority is required for {tag}?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    audit = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        audit,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        f"Execute exact experiment {tag}.",
    )
    return produce_follow_up_request(revision)


def _execution_and_submission(tmp_path: Path, *, tag: str):
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
        prediction_status="SUPPORTED",
        falsification_status="NOT_FALSIFIED",
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


def _case(tmp_path: Path, *, tag: str):
    execution_result, submission = _execution_and_submission(tmp_path / "experiment", tag=tag)
    record_path, receipt_path, pin = _p114b_files(tmp_path / "provenance", execution_result, submission)
    provenance = reattest_measurement_provenance(
        execution_result,
        submission,
        record_path,
        receipt_path,
        expected_authority_id=DERIVATION_AUTHORITY,
        expected_receipt_sha256=pin,
    )
    return execution_result, submission, provenance


def _procedure_bindings(provenance):
    return [
        {
            "measurement_id": item.measurement_id,
            "procedure_ref": item.procedure_ref,
            "procedure_sha256": item.procedure_sha256,
        }
        for item in provenance.derivations
    ]


def _qualification_id(submission, provenance, record_sha256: str, *, authority_id=EVALUATION_AUTHORITY, nonce=EVALUATION_NONCE):
    payload = {
        "contract_id": P115B_CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": nonce,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
    }
    return "QEA-" + _sha256(_canonical(payload))[:32]


def _authority_files(
    tmp_path: Path,
    submission,
    provenance,
    *,
    authority_id=EVALUATION_AUTHORITY,
    nonce=EVALUATION_NONCE,
    record_mutator=None,
    receipt_mutator=None,
):
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
    if record_mutator is not None:
        record_mutator(record)

    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)
    receipt = {
        "schema": P115B_RECEIPT_SCHEMA,
        "contract_id": P115B_CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": nonce,
        "evaluation_submission_id": submission.evaluation_submission_id,
        "provenance_qualification_id": provenance.provenance_qualification_id,
        "record_sha256": record_sha256,
        "qualification_id": _qualification_id(
            submission,
            provenance,
            record_sha256,
            authority_id=authority_id,
            nonce=nonce,
        ),
    }
    if receipt_mutator is not None:
        receipt_mutator(receipt)

    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "evaluation-authority.record.json"
    receipt_path = tmp_path / "evaluation-authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


_DEFAULT_PIN = object()


def _reattest(submission, provenance, paths, *, authority_id=EVALUATION_AUTHORITY, pin=_DEFAULT_PIN):
    record_path, receipt_path, receipt_sha256 = paths
    return _p115b().reattest_experiment_evaluator_authority(
        submission,
        provenance,
        record_path,
        receipt_path,
        expected_authority_id=authority_id,
        expected_receipt_sha256=receipt_sha256 if pin is _DEFAULT_PIN else pin,
    )


def test_a0_exact_upstreams_positive(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    assert result.evaluation_submission_id == submission.evaluation_submission_id
    assert result.provenance_qualification_id == provenance.provenance_qualification_id
    assert _p115b().is_factory_attested_qualified_experiment_evaluation_authority(result)


def test_a1_non_authoritative_evaluation_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
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
            _reattest(value, provenance, paths)


def test_a2_non_authoritative_provenance_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
    variants = (
        provenance.provenance_qualification_id,
        asdict(provenance),
        WitnessedMeasurementProvenance(**asdict(provenance)),
        copy.copy(provenance),
        copy.deepcopy(provenance),
        replace(provenance, provenance_qualification_id=provenance.provenance_qualification_id),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _reattest(submission, value, paths)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p115b().reattest_experiment_evaluator_authority)
    assert tuple(sig.parameters) == (
        "evaluation_submission",
        "measurement_provenance",
        "record_path",
        "receipt_path",
        "expected_authority_id",
        "expected_receipt_sha256",
    )
    for name in ("evaluation_submission", "measurement_provenance", "record_path", "receipt_path"):
        assert sig.parameters[name].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("expected_authority_id", "expected_receipt_sha256"):
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_c0_cross_evaluation_provenance_rejected(tmp_path: Path) -> None:
    _, submission_a, provenance_a = _case(tmp_path / "a", tag="A")
    _, submission_b, provenance_b = _case(tmp_path / "b", tag="B")
    paths_a = _authority_files(tmp_path / "authority-a", submission_a, provenance_a)
    with pytest.raises((TypeError, ValueError)):
        _reattest(submission_a, provenance_b, paths_a)
    with pytest.raises((TypeError, ValueError)):
        _reattest(submission_b, provenance_a, paths_a)


@pytest.mark.parametrize(
    "field",
    [
        "evaluator_id",
        "method_ref",
        "prediction_status",
        "falsification_status",
        "evaluation_rationale",
    ],
)
def test_c1_evaluation_claim_mismatch_rejected(tmp_path: Path, field: str) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    def mutate(record):
        record[field] = "WRONG"
    paths = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
        record_mutator=mutate,
    )
    with pytest.raises(ValueError):
        _reattest(submission, provenance, paths)


def test_c2_measurement_ids_order_and_membership_are_exact(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    for mode in ("reverse", "missing", "extra"):
        def mutate(record, mode=mode):
            ids = list(record["measurement_ids"])
            if mode == "reverse":
                record["measurement_ids"] = list(reversed(ids))
            elif mode == "missing":
                record["measurement_ids"] = ids[:-1]
            else:
                record["measurement_ids"] = ids + ["M-EXTRA"]
        paths = _authority_files(
            tmp_path / mode,
            submission,
            provenance,
            record_mutator=mutate,
        )
        with pytest.raises(ValueError):
            _reattest(submission, provenance, paths)


def test_c3_procedure_bindings_are_exact_and_ordered(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    mutations = (
        lambda record: record.__setitem__("procedure_bindings", list(reversed(record["procedure_bindings"]))),
        lambda record: record["procedure_bindings"][0].__setitem__("procedure_ref", "WRONG"),
        lambda record: record["procedure_bindings"][0].__setitem__("procedure_sha256", "0" * 64),
        lambda record: record["procedure_bindings"][0].__setitem__("measurement_id", "WRONG"),
    )
    for index, mutate in enumerate(mutations):
        paths = _authority_files(
            tmp_path / f"mutation-{index}",
            submission,
            provenance,
            record_mutator=mutate,
        )
        with pytest.raises(ValueError):
            _reattest(submission, provenance, paths)


@pytest.mark.parametrize("bad", ["", " ", 1, None])
def test_d0_expected_authority_exact_nonempty(tmp_path: Path, bad) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
    with pytest.raises((TypeError, ValueError)):
        _reattest(submission, provenance, paths, authority_id=bad)


@pytest.mark.parametrize("bad", ["", "0" * 63, "G" * 64, 1, None])
def test_d1_external_pin_exact_sha256(tmp_path: Path, bad) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
    with pytest.raises((TypeError, ValueError)):
        _reattest(submission, provenance, paths, pin=bad)


def test_d2_wrong_but_well_formed_pin_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
    with pytest.raises(ValueError):
        _reattest(submission, provenance, paths, pin="0" * 64)


def test_d3_wrong_authority_in_receipt_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
        authority_id="other-authority",
    )
    with pytest.raises(ValueError):
        _reattest(submission, provenance, paths, authority_id=EVALUATION_AUTHORITY)


@pytest.mark.parametrize("nonce", ["", "cd", "z" * 64])
def test_d4_invalid_nonce_rejected(tmp_path: Path, nonce: str) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
        nonce=nonce,
    )
    with pytest.raises(ValueError):
        _reattest(submission, provenance, paths)


def test_d5_noncanonical_record_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    record_path, receipt_path, pin = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
    )
    parsed = json.loads(record_path.read_text("utf-8"))
    record_path.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    with pytest.raises(ValueError):
        _reattest(submission, provenance, (record_path, receipt_path, pin))


def test_d6_noncanonical_receipt_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    record_path, receipt_path, _ = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
    )
    parsed = json.loads(receipt_path.read_text("utf-8"))
    receipt_path.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    pin = _sha256(receipt_path.read_bytes())
    with pytest.raises(ValueError):
        _reattest(submission, provenance, (record_path, receipt_path, pin))


def test_d7_tampered_qualification_id_rejected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(
        tmp_path / "authority",
        submission,
        provenance,
        receipt_mutator=lambda receipt: receipt.__setitem__("qualification_id", "QEA-" + "0" * 32),
    )
    with pytest.raises(ValueError):
        _reattest(submission, provenance, paths)


def test_e0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p115b().QualifiedExperimentEvaluationAuthority)) == (
        "qualification_id",
        "evaluation_submission_id",
        "provenance_qualification_id",
        "experiment_execution_result_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "evaluator_id",
        "method_ref",
        "prediction_status",
        "falsification_status",
        "evaluation_rationale",
        "measurement_ids",
        "procedure_bindings",
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


def test_e1_authority_pass_but_finding_blocked(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    assert result.measurement_provenance_status == "PASS"
    assert result.evaluation_authority_status == "PASS"
    assert result.finding_status == "BLOCKED"
    assert result.prediction_status == submission.prediction_status
    assert result.falsification_status == submission.falsification_status


def test_e2_output_snapshots_exact_authority_chain(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    assert result.evaluation_submission_id == submission.evaluation_submission_id
    assert result.provenance_qualification_id == provenance.provenance_qualification_id
    assert result.experiment_execution_result_id == submission.experiment_execution_result_id
    assert result.experiment_spec_id == submission.experiment_spec_id
    assert result.request_id == submission.request_id
    assert result.evaluator_id == submission.evaluator_id
    assert result.method_ref == submission.method_ref
    assert result.measurement_ids == tuple(item.measurement_id for item in submission.measurements)
    assert result.procedure_bindings == tuple(
        (item.measurement_id, item.procedure_ref, item.procedure_sha256)
        for item in provenance.derivations
    )


def test_f0_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    paths = _authority_files(tmp_path / "authority", submission, provenance)
    first = _reattest(submission, provenance, paths)
    second = _reattest(submission, provenance, paths)
    assert first == second and first is not second
    assert first.qualification_id.startswith("QEA-")
    assert first.qualification_id == second.qualification_id
    assert _p115b().is_factory_attested_qualified_experiment_evaluation_authority(first)
    assert _p115b().is_factory_attested_qualified_experiment_evaluation_authority(second)


def test_f1_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    cls = _p115b().QualifiedExperimentEvaluationAuthority
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(cls(**asdict(result)))
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(copy.copy(result))
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(copy.deepcopy(result))
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(
        replace(result, qualification_id=result.qualification_id)
    )


def test_f2_mutation_then_restore_sticky_invalid(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    original = result.evaluation_authority_status
    object.__setattr__(result, "evaluation_authority_status", "MUTATED")
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(result)
    object.__setattr__(result, "evaluation_authority_status", original)
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(result)


def test_f3_upstreams_can_be_collected(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    refs = (weakref.ref(submission), weakref.ref(provenance))
    del submission
    del provenance
    gc.collect()
    assert all(ref() is None for ref in refs)
    assert _p115b().is_factory_attested_qualified_experiment_evaluation_authority(result)


def test_g0_no_finding_execution_knowledge_or_operational_surface() -> None:
    module = _p115b()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "produce_finding",
        "produce_findings",
        "create_research_run_evidence",
        "execute_procedure",
        "recompute_measurement",
        "promote_to_knowledge",
        "authorize",
        "activate_live",
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


def test_g1_qualification_id_alone_is_not_attestation(tmp_path: Path) -> None:
    _, submission, provenance = _case(tmp_path / "case", tag="A")
    result = _reattest(
        submission,
        provenance,
        _authority_files(tmp_path / "authority", submission, provenance),
    )
    assert not _p115b().is_factory_attested_qualified_experiment_evaluation_authority(
        result.qualification_id
    )
