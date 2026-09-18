from __future__ import annotations

import copy
import gc
import importlib
import inspect
import weakref
from contextlib import contextmanager
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.experiment_execution_binding import bind_experiment_execution
from src.experiment_specification import specify_experiment
from src.follow_up_request import produce_follow_up_request
from src.linked_experiment_execution import (
    LinkedExperimentExecutionResult,
    is_factory_attested_linked_experiment_execution_result,
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


P113B_CONTRACT = "P1_13B_EXPERIMENT_EVALUATION_SUBMISSION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_13B_TEST_CAPTURE_AUTHORITY_V1"


def _historical(tmp_path: Path) -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome="OBSERVED")
        trace = produce_decision_trace(case.evidence, decision, action, result)
        episode = produce_observational_memory_episode(trace, action, result)
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _request(tmp_path: Path):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which experiment evaluation is required?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        assessment,
        scope,
        "REQUEST_NEW_EXPERIMENT",
        "Execute and evaluate the qualified synthetic experiment without promotion.",
    )
    return produce_follow_up_request(revision)


@contextmanager
def _linked_case(tmp_path: Path, *, protocol: str = "Protocol"):
    with synthetic_runtime_case() as case:
        specification = specify_experiment(
            _request(tmp_path),
            hypothesis_statement="H",
            prediction="P",
            falsification_rule="F",
            protocol=protocol,
            measurement_plan="Measure",
        )
        bound = bind_execution_input(
            case.corpus_root,
            case.contract_path,
            case.execution_input.expected_corpus_hash,
            case.execution_input.expected_contract_hash,
        )
        binding = bind_experiment_execution(specification, bound)
        qualified = qualify_experiment_execution_input(binding)
        yield run_linked_experiment(qualified), case


def _p113b():
    try:
        module = importlib.import_module("src.experiment_evaluation_submission")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.13B candidate absent — expected pre-implementation FAIL: "
            "src.experiment_evaluation_submission does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "ExperimentMeasurementClaim",
        "ExperimentEvaluationSubmission",
        "submit_experiment_evaluation",
        "is_factory_attested_experiment_evaluation_submission",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.13B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P113B_CONTRACT
    return module


def _measurement(
    measurement_id="M-1",
    *,
    metric="mean_return",
    observed_value="0.42",
    unit="ratio",
    sample_size=10,
    scope="synthetic",
    rationale="Measured according to submitted method.",
):
    return _p113b().ExperimentMeasurementClaim(
        measurement_id=measurement_id,
        metric=metric,
        observed_value=observed_value,
        unit=unit,
        sample_size=sample_size,
        scope=scope,
        rationale=rationale,
    )


_DEFAULT_MEASUREMENTS = object()


def _submit(
    execution_result,
    *,
    measurements=_DEFAULT_MEASUREMENTS,
    evaluator_id="evaluator:test",
    method_ref="method:test",
    prediction_status="SUPPORTED",
    falsification_status="NOT_FALSIFIED",
    evaluation_rationale="Evaluation submitted without promotion.",
):
    if measurements is _DEFAULT_MEASUREMENTS:
        measurements = (_measurement(),)
    return _p113b().submit_experiment_evaluation(
        execution_result,
        evaluator_id=evaluator_id,
        method_ref=method_ref,
        measurements=measurements,
        prediction_status=prediction_status,
        falsification_status=falsification_status,
        evaluation_rationale=evaluation_rationale,
    )


def test_a0_exact_linked_result_positive(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        submission = _submit(execution_result)
        assert submission.experiment_execution_result_id == execution_result.experiment_execution_result_id
        assert submission.experiment_spec_id == execution_result.experiment_spec_id
        assert _p113b().is_factory_attested_experiment_evaluation_submission(submission)


def test_a1_non_authoritative_result_rejected(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        variants = [
            execution_result.experiment_execution_result_id,
            asdict(execution_result),
            LinkedExperimentExecutionResult(**asdict(execution_result)),
            copy.copy(execution_result),
            copy.deepcopy(execution_result),
            replace(
                execution_result,
                experiment_execution_result_id=execution_result.experiment_execution_result_id,
            ),
        ]
        for value in variants:
            with pytest.raises((TypeError, ValueError)):
                _submit(value)


def test_a2_mutated_then_restored_result_rejected(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        original = execution_result.protocol
        object.__setattr__(execution_result, "protocol", "MUTATED")
        assert not is_factory_attested_linked_experiment_execution_result(execution_result)
        object.__setattr__(execution_result, "protocol", original)
        assert not is_factory_attested_linked_experiment_execution_result(execution_result)
        with pytest.raises((TypeError, ValueError)):
            _submit(execution_result)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p113b().submit_experiment_evaluation)
    assert tuple(sig.parameters) == (
        "execution_result",
        "evaluator_id",
        "method_ref",
        "measurements",
        "prediction_status",
        "falsification_status",
        "evaluation_rationale",
    )
    assert sig.parameters["execution_result"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in tuple(sig.parameters)[1:]:
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_c0_measurements_require_exact_nonempty_tuple(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        for bad in ([], set(), {}, "x", None, ()):
            with pytest.raises((TypeError, ValueError)):
                _submit(execution_result, measurements=bad)


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("measurement_id", ""),
        ("measurement_id", 1),
        ("metric", ""),
        ("metric", 1),
        ("observed_value", ""),
        ("observed_value", 1),
        ("unit", ""),
        ("unit", 1),
        ("scope", ""),
        ("scope", 1),
        ("rationale", ""),
        ("rationale", 1),
        ("sample_size", 0),
        ("sample_size", -1),
        ("sample_size", True),
        ("sample_size", 1.0),
    ],
)
def test_c1_measurement_claim_exactness(tmp_path: Path, field: str, bad) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        kwargs = {
            "measurement_id": "M-1",
            "metric": "metric",
            "observed_value": "1",
            "unit": "unit",
            "sample_size": 1,
            "scope": "scope",
            "rationale": "rationale",
        }
        kwargs[field] = bad
        claim = _p113b().ExperimentMeasurementClaim(**kwargs)
        with pytest.raises((TypeError, ValueError)):
            _submit(execution_result, measurements=(claim,))


def test_c2_duplicate_measurement_ids_rejected(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        with pytest.raises((TypeError, ValueError)):
            _submit(
                execution_result,
                measurements=(_measurement("M-1"), _measurement("M-1")),
            )


def test_c3_measurement_values_preserved_verbatim(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        claim = _measurement(
            "M-x",
            metric="  metric  ",
            observed_value="  0.4200  ",
            unit=" % ",
            scope="  regime A ",
            rationale="  exact rationale  ",
        )
        submission = _submit(execution_result, measurements=(claim,))
        assert submission.measurements[0] == claim


def test_d0_snapshot_preserves_execution_and_experiment(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        submission = _submit(execution_result)
        for name in (
            "experiment_execution_result_id",
            "experiment_execution_input_id",
            "execution_binding_id",
            "experiment_spec_id",
            "request_id",
            "revision_id",
            "audit_id",
            "scope_id",
            "objective",
            "hypothesis_statement",
            "prediction",
            "falsification_rule",
            "protocol",
            "measurement_plan",
            "corpus_root",
            "contract_path",
            "expected_corpus_hash",
            "expected_contract_hash",
            "files_consumed",
            "ticks_consumed",
            "first_timestamp",
            "last_timestamp",
            "stream_sha256",
            "source_verdict",
            "source_completeness_status",
            "source_independence_status",
        ):
            assert getattr(submission, name) == getattr(execution_result, name)


@pytest.mark.parametrize("status", ["SUPPORTED", "NOT_SUPPORTED", "BLOCKED"])
def test_e0_prediction_status_domain_positive(tmp_path: Path, status: str) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        assert _submit(execution_result, prediction_status=status).prediction_status == status


@pytest.mark.parametrize("status", ["FALSIFIED", "NOT_FALSIFIED", "BLOCKED"])
def test_e1_falsification_status_domain_positive(tmp_path: Path, status: str) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        assert _submit(execution_result, falsification_status=status).falsification_status == status


@pytest.mark.parametrize(
    ("field", "bad"),
    [
        ("prediction_status", "MAYBE"),
        ("prediction_status", 1),
        ("falsification_status", "MAYBE"),
        ("falsification_status", 1),
        ("evaluator_id", ""),
        ("evaluator_id", 1),
        ("method_ref", ""),
        ("method_ref", 1),
        ("evaluation_rationale", ""),
        ("evaluation_rationale", 1),
    ],
)
def test_e2_invalid_submission_fields_rejected(tmp_path: Path, field: str, bad) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        with pytest.raises((TypeError, ValueError)):
            _submit(execution_result, **{field: bad})


def test_f0_dangerous_text_remains_inert_and_authority_blocked(tmp_path: Path) -> None:
    dangerous = "AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER"
    with _linked_case(tmp_path, protocol=dangerous) as (execution_result, _case):
        claim = _measurement(
            metric=dangerous,
            observed_value=dangerous,
            rationale=dangerous,
        )
        submission = _submit(
            execution_result,
            measurements=(claim,),
            evaluator_id=dangerous,
            method_ref=dangerous,
            evaluation_rationale=dangerous,
        )
        assert submission.protocol == dangerous
        assert submission.measurements[0].metric == dangerous
        assert submission.measurement_provenance_status == "BLOCKED"
        assert submission.evaluation_authority_status == "BLOCKED"
        for name in ("finding", "hypothesis_verdict", "authorized", "research_run_evidence"):
            assert not hasattr(submission, name)


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p113b().ExperimentEvaluationSubmission)) == (
        "evaluation_submission_id",
        "experiment_execution_result_id",
        "experiment_execution_input_id",
        "execution_binding_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "objective",
        "hypothesis_statement",
        "prediction",
        "falsification_rule",
        "protocol",
        "measurement_plan",
        "corpus_root",
        "contract_path",
        "expected_corpus_hash",
        "expected_contract_hash",
        "files_consumed",
        "ticks_consumed",
        "first_timestamp",
        "last_timestamp",
        "stream_sha256",
        "measurements",
        "prediction_status",
        "falsification_status",
        "evaluation_rationale",
        "evaluator_id",
        "method_ref",
        "measurement_provenance_status",
        "evaluation_authority_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        first = _submit(execution_result)
        second = _submit(execution_result)
        assert first == second and first is not second
        assert first.evaluation_submission_id == second.evaluation_submission_id
        assert _p113b().is_factory_attested_experiment_evaluation_submission(first)
        assert _p113b().is_factory_attested_experiment_evaluation_submission(second)


def test_g2_changed_claim_changes_identity(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        first = _submit(execution_result, measurements=(_measurement("M-1", observed_value="1"),))
        second = _submit(execution_result, measurements=(_measurement("M-1", observed_value="2"),))
        assert first.evaluation_submission_id != second.evaluation_submission_id


def test_g3_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        result = _submit(execution_result)
        cls = _p113b().ExperimentEvaluationSubmission
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(cls(**asdict(result)))
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(copy.copy(result))
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(copy.deepcopy(result))
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(
            replace(result, evaluation_submission_id=result.evaluation_submission_id)
        )


def test_g4_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        result = _submit(execution_result)
        original = result.prediction_status
        object.__setattr__(result, "prediction_status", "MUTATED")
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(result)
        object.__setattr__(result, "prediction_status", original)
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(result)


def test_g5_upstream_result_can_be_collected(tmp_path: Path) -> None:
    with synthetic_runtime_case() as case:
        specification = specify_experiment(
            _request(tmp_path),
            hypothesis_statement="H",
            prediction="P",
            falsification_rule="F",
            protocol="Protocol",
            measurement_plan="Measure",
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
        submission = _submit(execution_result)
        ref = weakref.ref(execution_result)
        del execution_result
        gc.collect()
        assert ref() is None
        assert _p113b().is_factory_attested_experiment_evaluation_submission(submission)


def test_h0_no_findings_evidence_or_operational_surface() -> None:
    module = _p113b()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "produce_finding",
        "produce_findings",
        "create_research_run_evidence",
        "authorize",
        "run_backtest",
        "activate_live",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "ResearchFinding(",
        "ResearchFindings(",
        "ResearchRunEvidence(",
        "from_research_execution(",
        "order_send",
        "MetaTrader5",
        "activate_live(",
        "requests.",
        "socket.",
        "subprocess.",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_h1_submission_id_alone_is_not_authority(tmp_path: Path) -> None:
    with _linked_case(tmp_path) as (execution_result, _case):
        result = _submit(execution_result)
        assert not _p113b().is_factory_attested_experiment_evaluation_submission(
            result.evaluation_submission_id
        )
