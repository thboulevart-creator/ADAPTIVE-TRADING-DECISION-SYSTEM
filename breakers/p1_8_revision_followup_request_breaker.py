from __future__ import annotations

import copy
import importlib
import inspect
import unicodedata
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.research.execution import QualifiedResearchInput, ResearchExecutionResult
from src.research_findings import ResearchFindings
from src.research_run_evidence import ResearchRunEvidence
from src.revision import (
    RevisionDecision,
    is_factory_attested_revision_decision,
    produce_revision_decision,
)
from tests.research_runtime_fixture import synthetic_runtime_case


P18_CONTRACT = "P1_8_REVISION_FOLLOWUP_REQUEST_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_8_TEST_CAPTURE_AUTHORITY_V1"


def _p18():
    try:
        module = importlib.import_module("src.follow_up_request")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.8 candidate absent — expected pre-implementation FAIL: "
            "src.follow_up_request does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "FollowUpRequest",
        "produce_follow_up_request",
        "is_factory_attested_follow_up_request",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.8 candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P18_CONTRACT
    return module


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


def _source(
    tmp_path: Path,
    *,
    disposition: str = "REQUEST_NEW_EVIDENCE",
    detail: str = "Request additional documentary evidence.",
    source_state: str = "PASS",
):
    first = _historical(tmp_path / "first", outcome="ONE")

    if source_state == "PASS":
        scope = create_audit_scope(
            question="What follow-up is required?",
            expected_registration_ids=(first.registration_id,),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
        assert assessment.verdict == "PASS"
    elif source_state == "BLOCKED":
        scope = create_audit_scope(
            question="What follow-up is required while completeness is unknown?",
            expected_registration_ids=None,
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
        assert assessment.verdict == "BLOCKED"
    elif source_state == "FAIL":
        second = _historical(tmp_path / "second", outcome="TWO")
        scope = create_audit_scope(
            question="What follow-up is required for this incomplete bounded collection?",
            expected_registration_ids=(first.registration_id, second.registration_id),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
        assert assessment.verdict == "FAIL"
    else:
        raise AssertionError(source_state)

    revision = produce_revision_decision(assessment, scope, disposition, detail)
    assert is_factory_attested_revision_decision(revision)
    return scope, assessment, revision


def _request(revision: RevisionDecision):
    return _p18().produce_follow_up_request(revision)


# A — Revision source must be exact, current P1.7 authority.


@pytest.mark.parametrize("disposition", ["REQUEST_NEW_EVIDENCE", "REQUEST_NEW_EXPERIMENT"])
def test_a0_exact_routable_revision_positive(tmp_path: Path, disposition: str) -> None:
    _, _, revision = _source(tmp_path, disposition=disposition)
    request = _request(revision)
    assert request.revision_id == revision.revision_id
    assert _p18().is_factory_attested_follow_up_request(request)


def test_a1_revision_id_alone_is_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p18().produce_follow_up_request(revision.revision_id)


def test_a2_dict_revision_is_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p18().produce_follow_up_request(asdict(revision))


def test_a3_manual_same_valued_revision_is_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    manual = RevisionDecision(**asdict(revision))
    assert manual == revision and manual is not revision
    assert not is_factory_attested_revision_decision(manual)
    with pytest.raises((TypeError, ValueError)):
        _request(manual)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a4_copy_or_deepcopy_revision_is_rejected(tmp_path: Path, copier) -> None:
    _, _, revision = _source(tmp_path)
    copied = copier(revision)
    assert copied == revision and copied is not revision
    with pytest.raises((TypeError, ValueError)):
        _request(copied)


def test_a4_replace_revision_is_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    copied = replace(revision, revision_id=revision.revision_id)
    assert copied == revision and copied is not revision
    with pytest.raises((TypeError, ValueError)):
        _request(copied)


def test_a5_mutated_revision_is_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    object.__setattr__(revision, "detail", "MUTATED")
    assert not is_factory_attested_revision_decision(revision)
    with pytest.raises((TypeError, ValueError)):
        _request(revision)


def test_a6_invalidated_then_restored_revision_stays_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    original = revision.detail
    object.__setattr__(revision, "detail", "MUTATED")
    assert not is_factory_attested_revision_decision(revision)
    object.__setattr__(revision, "detail", original)
    assert not is_factory_attested_revision_decision(revision)
    with pytest.raises((TypeError, ValueError)):
        _request(revision)


# B — Routing is derived only from P1.7 disposition.


def test_b0_evidence_revision_routes_to_evidence(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, disposition="REQUEST_NEW_EVIDENCE")
    request = _request(revision)
    assert request.request_kind == "EVIDENCE"


def test_b1_experiment_revision_routes_to_experiment(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, disposition="REQUEST_NEW_EXPERIMENT")
    request = _request(revision)
    assert request.request_kind == "EXPERIMENT"


def test_b2_keep_current_state_is_explicitly_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(
        tmp_path,
        disposition="KEEP_CURRENT_STATE",
        detail="Keep the governed state unchanged.",
    )
    with pytest.raises((TypeError, ValueError)):
        _request(revision)


def test_b3_reformulate_question_is_explicitly_rejected(tmp_path: Path) -> None:
    _, _, revision = _source(
        tmp_path,
        disposition="REFORMULATE_QUESTION",
        detail="Which narrower question should be audited next?",
    )
    with pytest.raises((TypeError, ValueError)):
        _request(revision)


def test_b4_factory_signature_is_exactly_one_required_revision_parameter() -> None:
    signature = inspect.signature(_p18().produce_follow_up_request)
    assert tuple(signature.parameters) == ("revision",)
    parameter = signature.parameters["revision"]
    assert parameter.default is inspect.Parameter.empty


def test_b5_output_has_no_noop_or_none_request_kind(tmp_path: Path) -> None:
    _, _, evidence_revision = _source(tmp_path / "e", disposition="REQUEST_NEW_EVIDENCE")
    _, _, experiment_revision = _source(tmp_path / "x", disposition="REQUEST_NEW_EXPERIMENT")
    kinds = {
        _request(evidence_revision).request_kind,
        _request(experiment_revision).request_kind,
    }
    assert kinds == {"EVIDENCE", "EXPERIMENT"}
    assert "NONE" not in kinds and "NOOP" not in kinds


# C — Binding is exact; caller cannot override kind/specification.


def test_c0_specification_equals_revision_detail_exactly(tmp_path: Path) -> None:
    detail = "Request exactly this evidence."
    _, _, revision = _source(tmp_path, detail=detail)
    request = _request(revision)
    assert request.specification == revision.detail == detail


def test_c1_leading_and_trailing_whitespace_is_preserved(tmp_path: Path) -> None:
    detail = "  Request this evidence exactly.  "
    _, _, revision = _source(tmp_path, detail=detail)
    request = _request(revision)
    assert request.specification == detail


def test_c2_multiline_specification_is_preserved(tmp_path: Path) -> None:
    detail = "Line one.\nLine two.\n"
    _, _, revision = _source(tmp_path, detail=detail)
    request = _request(revision)
    assert request.specification == detail


def test_c3_unicode_specification_is_preserved_without_normalization(tmp_path: Path) -> None:
    composed = "Caf\u00e9 evidence."
    decomposed = unicodedata.normalize("NFD", composed)
    assert composed != decomposed
    _, _, first_revision = _source(tmp_path / "a", detail=composed)
    _, _, second_revision = _source(tmp_path / "b", detail=decomposed)
    first = _request(first_revision)
    second = _request(second_revision)
    assert first.specification == composed
    assert second.specification == decomposed


def test_c4_factory_exposes_no_kind_or_specification_override_parameters() -> None:
    signature = inspect.signature(_p18().produce_follow_up_request)
    forbidden = {"request_kind", "kind", "mode", "route", "specification", "force", "override"}
    assert forbidden.isdisjoint(signature.parameters)


def test_c5_same_source_different_detail_changes_request_identity(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Q",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id",),
    )
    assessment = audit_memory_collection(scope, (memory,))
    one_revision = produce_revision_decision(
        assessment, scope, "REQUEST_NEW_EVIDENCE", "Reason one."
    )
    two_revision = produce_revision_decision(
        assessment, scope, "REQUEST_NEW_EVIDENCE", "Reason two."
    )
    one = _request(one_revision)
    two = _request(two_revision)
    assert one.request_id != two.request_id


def test_c6_same_detail_different_routable_disposition_changes_kind_and_identity(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Q",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id",),
    )
    assessment = audit_memory_collection(scope, (memory,))
    detail = "Same external text."
    evidence_revision = produce_revision_decision(
        assessment, scope, "REQUEST_NEW_EVIDENCE", detail
    )
    experiment_revision = produce_revision_decision(
        assessment, scope, "REQUEST_NEW_EXPERIMENT", detail
    )
    evidence = _request(evidence_revision)
    experiment = _request(experiment_revision)
    assert evidence.request_kind == "EVIDENCE"
    assert experiment.request_kind == "EXPERIMENT"
    assert evidence.request_id != experiment.request_id


# D — IDs and source states are preserved exactly.


@pytest.mark.parametrize("source_state", ["PASS", "FAIL", "BLOCKED"])
def test_d0_ids_and_source_verdict_are_preserved(tmp_path: Path, source_state: str) -> None:
    _, assessment, revision = _source(tmp_path, source_state=source_state)
    request = _request(revision)
    assert request.revision_id == revision.revision_id
    assert request.audit_id == revision.audit_id == assessment.audit_id
    assert request.scope_id == revision.scope_id == assessment.scope_id
    assert request.source_verdict == revision.source_verdict == assessment.verdict


@pytest.mark.parametrize("source_state", ["PASS", "FAIL", "BLOCKED"])
def test_d1_completeness_and_independence_snapshots_are_preserved(
    tmp_path: Path,
    source_state: str,
) -> None:
    _, assessment, revision = _source(tmp_path, source_state=source_state)
    request = _request(revision)
    assert request.source_completeness_status == revision.source_completeness_status
    assert request.source_completeness_status == assessment.completeness_status
    assert request.source_independence_status == revision.source_independence_status
    assert request.source_independence_status == assessment.independence_status


def test_d2_blocked_remains_blocked_after_request_creation(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, source_state="BLOCKED")
    request = _request(revision)
    assert request.source_verdict == "BLOCKED"
    assert request.source_completeness_status == "BLOCKED"
    assert request.source_independence_status == "BLOCKED"


def test_d3_pass_collection_still_preserves_independence_blocked(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, source_state="PASS")
    request = _request(revision)
    assert request.source_verdict == "PASS"
    assert request.source_independence_status == "BLOCKED"


# E — FollowUpRequest is not fulfillment, evidence, execution input, or result.


def test_e0_follow_up_request_is_not_research_evidence_or_findings(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    assert not isinstance(request, ResearchRunEvidence)
    assert not isinstance(request, ResearchFindings)


def test_e1_follow_up_request_is_not_qualified_input_or_execution_result(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, disposition="REQUEST_NEW_EXPERIMENT")
    request = _request(revision)
    assert not isinstance(request, QualifiedResearchInput)
    assert not isinstance(request, ResearchExecutionResult)


def test_e2_follow_up_request_has_no_fulfillment_or_execution_fields(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    forbidden = (
        "evidence_id",
        "finding_id",
        "research_run_id",
        "experiment_id",
        "dataset_id",
        "qualified_input",
        "execution_result",
        "evidence_obtained",
        "experiment_completed",
        "execution_allowed",
        "authorized",
        "supported",
        "confidence",
        "requested_at",
    )
    assert all(not hasattr(request, name) for name in forbidden)


def test_e3_follow_up_request_fields_are_exactly_minimal_model() -> None:
    assert tuple(field.name for field in fields(_p18().FollowUpRequest)) == (
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "request_kind",
        "specification",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


# F — Runtime has no execution/authorization surface; dangerous text stays text.


def test_f0_runtime_source_has_no_research_execution_or_external_side_effect_surface() -> None:
    source = inspect.getsource(_p18())
    forbidden = (
        "run_qualified_research",
        "bind_execution_input",
        "ResearchExecutionResult(",
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
        "mt5.",
        "run_backtest(",
        "activate_live(",
        "submit_order(",
        "create_order(",
    )
    assert all(token not in source for token in forbidden)


def test_f1_dangerous_words_in_specification_do_not_create_authority(tmp_path: Path) -> None:
    detail = "RUN_BACKTEST AUTHORIZED SUPPORTED send order live now"
    _, _, revision = _source(tmp_path, detail=detail)
    request = _request(revision)
    assert request.specification == detail
    for name in (
        "authorized",
        "authorization",
        "supported",
        "backtest_id",
        "order_id",
        "execution_allowed",
        "knowledge",
    ):
        assert not hasattr(request, name)


def test_f2_request_has_no_execution_methods(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path, disposition="REQUEST_NEW_EXPERIMENT")
    request = _request(revision)
    forbidden = ("run", "execute", "acquire", "collect", "fetch", "submit", "authorize", "promote")
    assert all(not callable(getattr(request, name, None)) for name in forbidden)


# G — Identity and exact-object attestation, with sticky invalidation from day one.


def _manual_request(source):
    return _p18().FollowUpRequest(**asdict(source))


def test_g0_positive_request_is_factory_attested(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    assert _p18().is_factory_attested_follow_up_request(request)


def test_g1_same_revision_produces_same_id_but_distinct_attested_objects(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    first = _request(revision)
    second = _request(revision)
    assert first == second
    assert first is not second
    assert first.request_id == second.request_id
    assert _p18().is_factory_attested_follow_up_request(first)
    assert _p18().is_factory_attested_follow_up_request(second)


def test_g2_manual_same_valued_request_is_not_attested(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    manual = _manual_request(request)
    assert manual == request and manual is not request
    assert not _p18().is_factory_attested_follow_up_request(manual)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_g3_copy_or_deepcopy_request_is_not_attested(tmp_path: Path, copier) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    copied = copier(request)
    assert copied == request and copied is not request
    assert not _p18().is_factory_attested_follow_up_request(copied)


def test_g3_replace_request_is_not_attested(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    copied = replace(request, request_id=request.request_id)
    assert copied == request and copied is not request
    assert not _p18().is_factory_attested_follow_up_request(copied)


def test_g4_mutation_invalidates_request_attestation(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    object.__setattr__(request, "specification", "MUTATED")
    assert not _p18().is_factory_attested_follow_up_request(request)


def test_g5_observed_mutation_then_restore_does_not_revive_attestation(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    original = request.specification
    object.__setattr__(request, "specification", "MUTATED")
    assert not _p18().is_factory_attested_follow_up_request(request)
    object.__setattr__(request, "specification", original)
    assert not _p18().is_factory_attested_follow_up_request(request)


def test_g6_request_id_alone_is_not_request_authority(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    assert not _p18().is_factory_attested_follow_up_request(request.request_id)


def test_g7_manual_rebinding_of_request_id_to_changed_source_is_not_attested(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    forged = _p18().FollowUpRequest(
        request_id=request.request_id,
        revision_id="REV-" + "0" * 32,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        request_kind=request.request_kind,
        specification=request.specification,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
    assert not _p18().is_factory_attested_follow_up_request(forged)


# H — Reverse authority and temporal restraint.


def test_h0_request_does_not_mutate_or_repair_revision(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    snapshot = asdict(revision)
    _request(revision)
    assert asdict(revision) == snapshot
    assert is_factory_attested_revision_decision(revision)


def test_h1_request_cannot_substitute_for_revision(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    with pytest.raises((TypeError, ValueError)):
        _p18().produce_follow_up_request(request)


def test_h2_request_has_no_implicit_time_fields(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    forbidden = ("requested_at", "known_from", "valid_from", "execution_at", "fulfilled_at")
    assert all(not hasattr(request, name) for name in forbidden)


def test_h3_runtime_uses_no_local_clock() -> None:
    source = inspect.getsource(_p18())
    forbidden = ("datetime.now", "datetime.utcnow", "time.time", "requested_at =")
    assert all(token not in source for token in forbidden)


def test_h4_request_is_not_revision_authority(tmp_path: Path) -> None:
    _, _, revision = _source(tmp_path)
    request = _request(revision)
    assert not is_factory_attested_revision_decision(request)


def test_h5_factory_exposes_no_downstream_execution_or_permission_parameters() -> None:
    signature = inspect.signature(_p18().produce_follow_up_request)
    forbidden = {
        "evidence",
        "experiment",
        "dataset",
        "input",
        "run",
        "execute",
        "authorized",
        "authorization",
        "broker",
        "backtest",
        "live",
    }
    assert forbidden.isdisjoint(signature.parameters)
