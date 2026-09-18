from __future__ import annotations

import copy
import gc
import hashlib
import importlib
import inspect
import unicodedata
import weakref
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.follow_up_request import FollowUpRequest, is_factory_attested_follow_up_request, produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import HistoricalMemoryEpisode, persist_witnessed_memory_episode, reattest_persisted_memory_episode
from src.research.execution import QualifiedResearchInput, ResearchExecutionResult
from src.research_findings import ResearchFindings, ResearchMeasurement
from src.research_run_evidence import ResearchRunEvidence
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P19B_CONTRACT = "P1_9B_EXPERIMENT_SPECIFICATION_BOUNDARY_V1"

P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_9_TEST_CAPTURE_AUTHORITY_V1"


def _historical(tmp_path: Path, *, outcome: str = "OBSERVED") -> HistoricalMemoryEpisode:
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome=outcome)
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


def _request(
    tmp_path: Path,
    *,
    request_kind: str,
    source_state: str = "PASS",
    detail: str | None = None,
) -> FollowUpRequest:
    first = _historical(tmp_path / "first", outcome="ONE")
    if source_state == "PASS":
        scope = create_audit_scope(
            question="What follow-up is required?",
            expected_registration_ids=(first.registration_id,),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    elif source_state == "BLOCKED":
        scope = create_audit_scope(
            question="What follow-up is required while completeness is unknown?",
            expected_registration_ids=None,
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    elif source_state == "FAIL":
        second = _historical(tmp_path / "second", outcome="TWO")
        scope = create_audit_scope(
            question="What follow-up is required for this incomplete bounded collection?",
            expected_registration_ids=(first.registration_id, second.registration_id),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    else:
        raise AssertionError(source_state)

    disposition = {
        "EVIDENCE": "REQUEST_NEW_EVIDENCE",
        "EXPERIMENT": "REQUEST_NEW_EXPERIMENT",
    }[request_kind]
    if detail is None:
        detail = (
            "Request exact external evidence."
            if request_kind == "EVIDENCE"
            else "Specify a controlled follow-up experiment."
        )
    revision = produce_revision_decision(assessment, scope, disposition, detail)
    request = produce_follow_up_request(revision)
    assert request.request_kind == request_kind
    assert is_factory_attested_follow_up_request(request)
    return request


def _p19b():
    try:
        module = importlib.import_module("src.experiment_specification")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.9B candidate absent — expected pre-implementation FAIL: "
            "src.experiment_specification does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "ExperimentSpecification",
        "specify_experiment",
        "is_factory_attested_experiment_specification",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.9B candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P19B_CONTRACT
    return module


def _specify(
    request,
    *,
    hypothesis_statement="H",
    prediction="P",
    falsification_rule="F",
    protocol="Protocol",
    measurement_plan="Measure",
):
    return _p19b().specify_experiment(
        request,
        hypothesis_statement=hypothesis_statement,
        prediction=prediction,
        falsification_rule=falsification_rule,
        protocol=protocol,
        measurement_plan=measurement_plan,
    )


# A — exact EXPERIMENT request only.


def test_a0_exact_experiment_request_positive(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    spec = _specify(request)
    assert spec.request_id == request.request_id
    assert _p19b().is_factory_attested_experiment_specification(spec)


def test_a1_evidence_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EVIDENCE")
    with pytest.raises((TypeError, ValueError)):
        _specify(request)


def test_a2_request_id_alone_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    with pytest.raises((TypeError, ValueError)):
        _specify(request.request_id)


def test_a3_dict_manual_copy_replace_are_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    variants = [
        asdict(request),
        FollowUpRequest(**asdict(request)),
        copy.copy(request),
        copy.deepcopy(request),
        replace(request, request_id=request.request_id),
    ]
    for variant in variants:
        with pytest.raises((TypeError, ValueError)):
            _specify(variant)


def test_a4_mutated_and_restored_request_is_rejected(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    original = request.specification
    object.__setattr__(request, "specification", "MUTATED")
    assert not is_factory_attested_follow_up_request(request)
    object.__setattr__(request, "specification", original)
    assert not is_factory_attested_follow_up_request(request)
    with pytest.raises((TypeError, ValueError)):
        _specify(request)


# B — exact signature.


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p19b().specify_experiment)
    assert tuple(sig.parameters) == (
        "request", "hypothesis_statement", "prediction", "falsification_rule",
        "protocol", "measurement_plan",
    )
    assert sig.parameters["request"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in (
        "hypothesis_statement", "prediction", "falsification_rule",
        "protocol", "measurement_plan",
    ):
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


def test_b1_no_objective_execution_or_dataset_override_parameters() -> None:
    sig = inspect.signature(_p19b().specify_experiment)
    forbidden = {
        "objective", "experiment_spec_id", "request_kind", "dataset_id",
        "dataset_version", "corpus_root", "contract_path", "expected_corpus_hash",
        "expected_contract_hash", "execute", "authorized", "backtest", "live",
    }
    assert forbidden.isdisjoint(sig.parameters)


# C — five fields are exact nonempty str and preserved verbatim.


class CustomStr(str):
    pass


DESIGN_FIELDS = (
    "hypothesis_statement",
    "prediction",
    "falsification_rule",
    "protocol",
    "measurement_plan",
)


@pytest.mark.parametrize("field_name", DESIGN_FIELDS)
@pytest.mark.parametrize("value", [None, 1, b"x", CustomStr("x")])
def test_c0_each_design_field_requires_exact_str(tmp_path: Path, field_name: str, value) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    kwargs = {name: name for name in DESIGN_FIELDS}
    kwargs[field_name] = value
    with pytest.raises((TypeError, ValueError)):
        _p19b().specify_experiment(request, **kwargs)


@pytest.mark.parametrize("field_name", DESIGN_FIELDS)
@pytest.mark.parametrize("value", ["", " ", "\t", "\n  "])
def test_c1_each_design_field_rejects_empty_or_whitespace(tmp_path: Path, field_name: str, value: str) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    kwargs = {name: name for name in DESIGN_FIELDS}
    kwargs[field_name] = value
    with pytest.raises((TypeError, ValueError)):
        _p19b().specify_experiment(request, **kwargs)


def test_c2_design_fields_are_preserved_verbatim(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    values = {
        "hypothesis_statement": "  Hypothèse É  ",
        "prediction": "Line 1\nLine 2",
        "falsification_rule": "  Falsify if X  ",
        "protocol": "  Protocol Ω  ",
        "measurement_plan": "Measure Δ\nExactly",
    }
    spec = _p19b().specify_experiment(request, **values)
    for name, value in values.items():
        assert getattr(spec, name) == value


def test_c3_unicode_is_not_normalized(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    composed = "café"
    decomposed = unicodedata.normalize("NFD", composed)
    first = _specify(request, hypothesis_statement=composed)
    second = _specify(request, hypothesis_statement=decomposed)
    assert first.hypothesis_statement != second.hypothesis_statement
    assert first.experiment_spec_id != second.experiment_spec_id


# D — objective is derived exactly from request and cannot be rebound.


def test_d0_objective_equals_request_specification_exactly(tmp_path: Path) -> None:
    detail = "  Exact experiment objective.  "
    request = _request(tmp_path, request_kind="EXPERIMENT", detail=detail)
    spec = _specify(request)
    assert spec.objective == request.specification == detail


def test_d1_different_request_changes_identity_when_payload_changes(tmp_path: Path) -> None:
    first_req = _request(tmp_path / "a", request_kind="EXPERIMENT", detail="Objective A")
    second_req = _request(tmp_path / "b", request_kind="EXPERIMENT", detail="Objective B")
    first = _specify(first_req)
    second = _specify(second_req)
    assert first.experiment_spec_id != second.experiment_spec_id


# E — source snapshots and BLOCKED.


@pytest.mark.parametrize("state", ["PASS", "FAIL", "BLOCKED"])
def test_e0_ids_and_source_statuses_are_preserved(tmp_path: Path, state: str) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT", source_state=state)
    spec = _specify(request)
    assert spec.request_id == request.request_id
    assert spec.revision_id == request.revision_id
    assert spec.audit_id == request.audit_id
    assert spec.scope_id == request.scope_id
    assert spec.source_verdict == request.source_verdict
    assert spec.source_completeness_status == request.source_completeness_status
    assert spec.source_independence_status == request.source_independence_status


def test_e1_blocked_stays_blocked(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT", source_state="BLOCKED"))
    assert spec.source_verdict == "BLOCKED"
    assert spec.source_completeness_status == "BLOCKED"
    assert spec.source_independence_status == "BLOCKED"


# F — non-execution and no downstream objects.


def test_f0_spec_is_not_execution_input_result_evidence_or_findings(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    assert not isinstance(spec, QualifiedResearchInput)
    assert not isinstance(spec, ResearchExecutionResult)
    assert not isinstance(spec, ResearchRunEvidence)
    assert not isinstance(spec, ResearchFindings)
    assert not isinstance(spec, ResearchMeasurement)


def test_f1_output_has_no_execution_dataset_measurement_or_authority_fields(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    forbidden = (
        "experiment_id", "dataset_id", "dataset_version", "corpus_root",
        "contract_path", "expected_corpus_hash", "expected_contract_hash",
        "execution_result", "measurement_id", "finding_id", "authorized",
    )
    assert all(not hasattr(spec, name) for name in forbidden)


def test_f2_runtime_source_has_no_execution_or_external_side_effect_surface() -> None:
    source = inspect.getsource(_p19b())
    forbidden = (
        "bind_execution_input", "run_qualified_research", "QualifiedResearchInput(",
        "ResearchExecutionResult(", "ResearchRunEvidence(", "ResearchFindings(",
        "open(", "Path(", "requests.", "socket.", "subprocess.", "order_send",
        "MetaTrader5", "run_backtest(", "activate_live(",
    )
    assert all(token not in source for token in forbidden)


def test_f3_dangerous_protocol_text_remains_text_only(tmp_path: Path) -> None:
    protocol = "AUTHORIZED RUN_BACKTEST SEND_LIVE_ORDER"
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"), protocol=protocol)
    assert spec.protocol == protocol
    assert not hasattr(spec, "authorized")


# G — exact output, deterministic identity, sticky attestation, GC.


def test_g0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p19b().ExperimentSpecification)) == (
        "experiment_spec_id", "request_id", "revision_id", "audit_id", "scope_id",
        "objective", "hypothesis_statement", "prediction", "falsification_rule",
        "protocol", "measurement_plan", "source_verdict",
        "source_completeness_status", "source_independence_status",
    )


def test_g1_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    first = _specify(request)
    second = _specify(request)
    assert first == second
    assert first is not second
    assert first.experiment_spec_id == second.experiment_spec_id
    assert _p19b().is_factory_attested_experiment_specification(first)
    assert _p19b().is_factory_attested_experiment_specification(second)


@pytest.mark.parametrize("field_name", DESIGN_FIELDS)
def test_g2_changing_each_design_field_changes_identity(tmp_path: Path, field_name: str) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    base_kwargs = {name: name for name in DESIGN_FIELDS}
    base = _p19b().specify_experiment(request, **base_kwargs)
    changed_kwargs = dict(base_kwargs)
    changed_kwargs[field_name] = base_kwargs[field_name] + "-changed"
    changed = _p19b().specify_experiment(request, **changed_kwargs)
    assert base.experiment_spec_id != changed.experiment_spec_id


def test_g3_manual_copy_replace_are_not_attested(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    manual = _p19b().ExperimentSpecification(**asdict(spec))
    assert not _p19b().is_factory_attested_experiment_specification(manual)
    assert not _p19b().is_factory_attested_experiment_specification(copy.copy(spec))
    assert not _p19b().is_factory_attested_experiment_specification(copy.deepcopy(spec))
    assert not _p19b().is_factory_attested_experiment_specification(
        replace(spec, experiment_spec_id=spec.experiment_spec_id)
    )


def test_g4_mutation_then_restore_is_sticky_invalid(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    original = spec.protocol
    object.__setattr__(spec, "protocol", "MUTATED")
    assert not _p19b().is_factory_attested_experiment_specification(spec)
    object.__setattr__(spec, "protocol", original)
    assert not _p19b().is_factory_attested_experiment_specification(spec)


def test_g5_request_can_be_collected_after_specification(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    request_id = request.request_id
    spec = _specify(request)
    ref = weakref.ref(request)
    del request
    gc.collect()
    assert ref() is None
    assert spec.request_id == request_id
    assert _p19b().is_factory_attested_experiment_specification(spec)


# H — reverse authority and cross-branch restraint.


def test_h0_specification_does_not_mutate_request(tmp_path: Path) -> None:
    request = _request(tmp_path, request_kind="EXPERIMENT")
    snapshot = asdict(request)
    _specify(request)
    assert asdict(request) == snapshot
    assert is_factory_attested_follow_up_request(request)


def test_h1_specification_cannot_substitute_for_request(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    with pytest.raises((TypeError, ValueError)):
        _specify(spec)


def test_h2_specification_has_no_execution_methods(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    forbidden = ("run", "execute", "bind", "authorize", "backtest", "submit_order", "promote")
    assert all(not callable(getattr(spec, name, None)) for name in forbidden)


def test_h3_no_implicit_time_fields(tmp_path: Path) -> None:
    spec = _specify(_request(tmp_path, request_kind="EXPERIMENT"))
    forbidden = ("specified_at", "requested_at", "known_from", "valid_from", "executed_at")
    assert all(not hasattr(spec, name) for name in forbidden)
