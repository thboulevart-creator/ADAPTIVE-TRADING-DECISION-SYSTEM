from __future__ import annotations

import copy
import importlib
import inspect
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.memory_audit import (
    AuditScope,
    MemoryCollectionAuditAssessment,
    audit_memory_collection,
    create_audit_scope,
    is_factory_attested_memory_collection_audit,
)
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.research_findings import ResearchFindings
from src.research_run_evidence import ResearchRunEvidence
from tests.research_runtime_fixture import synthetic_runtime_case


P17_CONTRACT = "P1_7_AUDIT_REVISION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
AUTHORITY_ID = "P1_7_TEST_CAPTURE_AUTHORITY_V1"

DISPOSITIONS = (
    "KEEP_CURRENT_STATE",
    "REQUEST_NEW_EVIDENCE",
    "REQUEST_NEW_EXPERIMENT",
    "REFORMULATE_QUESTION",
)


def _p17():
    try:
        module = importlib.import_module("src.revision")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.7 candidate absent — expected pre-implementation FAIL: "
            "src.revision does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "RevisionDecision",
        "produce_revision_decision",
        "is_factory_attested_revision_decision",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.7 candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P17_CONTRACT
    return module


def _episode(*, outcome: str = "OBSERVED"):
    with synthetic_runtime_case() as case:
        decision = produce_decision(case.evidence, context=case.context, decision="HOLD")
        action = engage_qualification_action(decision, behavior="NO_ACTION")
        result = observe_qualification_result(action, outcome=outcome)
        trace = produce_decision_trace(case.evidence, decision, action, result)
        return produce_observational_memory_episode(trace, action, result)


def _historical(tmp_path: Path, *, outcome: str = "OBSERVED") -> HistoricalMemoryEpisode:
    episode = _episode(outcome=outcome)
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _pass_source(tmp_path: Path):
    memory = _historical(tmp_path / "pass-memory")
    scope = create_audit_scope(
        question="Should the current audited collection be maintained or investigated further?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    assert assessment.verdict == "PASS"
    return scope, assessment


def _blocked_source(tmp_path: Path):
    memory = _historical(tmp_path / "blocked-memory")
    scope = create_audit_scope(
        question="What should be done while collection completeness remains unknown?",
        expected_registration_ids=None,
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    assert assessment.verdict == "BLOCKED"
    assert assessment.completeness_status == "BLOCKED"
    return scope, assessment


def _fail_source(tmp_path: Path):
    first = _historical(tmp_path / "fail-first", outcome="ONE")
    second = _historical(tmp_path / "fail-second", outcome="TWO")
    scope = create_audit_scope(
        question="How should the incomplete bounded collection be handled?",
        expected_registration_ids=(first.registration_id, second.registration_id),
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (first,))
    assert assessment.verdict == "FAIL"
    assert assessment.completeness_status == "FAIL"
    return scope, assessment


def _detail(disposition: str, scope: AuditScope) -> str:
    if disposition == "KEEP_CURRENT_STATE":
        return "Keep the governed state unchanged while preserving the audit limitations."
    if disposition == "REQUEST_NEW_EVIDENCE":
        return "Request the missing documentary evidence needed to reassess the audited scope."
    if disposition == "REQUEST_NEW_EXPERIMENT":
        return "Request a new separately governed experiment addressing the unresolved audit question."
    if disposition == "REFORMULATE_QUESTION":
        return "Which narrower audit question can be evaluated without the unresolved ambiguity?"
    raise AssertionError(disposition)


def _produce(scope, assessment, *, disposition="KEEP_CURRENT_STATE", detail=None):
    if detail is None:
        detail = _detail(disposition, scope)
    return _p17().produce_revision_decision(assessment, scope, disposition, detail)


# A — Assessment source must be exact P1.6 authority.


def test_a0_exact_attested_assessment_positive(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    assert decision.audit_id == assessment.audit_id
    assert _p17().is_factory_attested_revision_decision(decision)


def test_a1_audit_id_alone_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment.audit_id,
            scope,
            "KEEP_CURRENT_STATE",
            _detail("KEEP_CURRENT_STATE", scope),
        )


def test_a2_dict_assessment_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            asdict(assessment),
            scope,
            "KEEP_CURRENT_STATE",
            _detail("KEEP_CURRENT_STATE", scope),
        )


def test_a3_manual_same_valued_assessment_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    manual = MemoryCollectionAuditAssessment(**asdict(assessment))
    assert manual == assessment and manual is not assessment
    assert not is_factory_attested_memory_collection_audit(manual)
    with pytest.raises((TypeError, ValueError)):
        _produce(scope, manual)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_a4_copy_or_deepcopy_assessment_is_rejected(tmp_path: Path, copier) -> None:
    scope, assessment = _pass_source(tmp_path)
    copied = copier(assessment)
    assert copied == assessment and copied is not assessment
    with pytest.raises((TypeError, ValueError)):
        _produce(scope, copied)


def test_a4_replace_assessment_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    copied = replace(assessment, audit_id=assessment.audit_id)
    assert copied == assessment and copied is not assessment
    with pytest.raises((TypeError, ValueError)):
        _produce(scope, copied)


def test_a5_mutated_assessment_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    object.__setattr__(assessment, "verdict", "BLOCKED")
    assert not is_factory_attested_memory_collection_audit(assessment)
    with pytest.raises((TypeError, ValueError)):
        _produce(scope, assessment)


def test_a6_missing_assessment_is_rejected(tmp_path: Path) -> None:
    scope, _ = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            None,
            scope,
            "KEEP_CURRENT_STATE",
            _detail("KEEP_CURRENT_STATE", scope),
        )


# B — Scope is content-bound value declaration and must match exact audit.


def test_b0_exact_scope_positive(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    assert decision.scope_id == scope.scope_id == assessment.scope_id


def test_b1_manual_same_valued_scope_is_accepted(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    manual = AuditScope(**asdict(scope))
    assert manual == scope and manual is not scope
    decision = _produce(manual, assessment)
    assert decision.scope_id == scope.scope_id


def test_b2_missing_scope_is_rejected(tmp_path: Path) -> None:
    _, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            None,
            "KEEP_CURRENT_STATE",
            "No governed change.",
        )


def test_b3_foreign_scope_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path / "source")
    foreign_memory = _historical(tmp_path / "foreign")
    foreign = create_audit_scope(
        question=scope.question,
        expected_registration_ids=(foreign_memory.registration_id,),
        context_fields=scope.context_fields,
    )
    assert foreign.scope_id != assessment.scope_id
    with pytest.raises((TypeError, ValueError)):
        _produce(foreign, assessment)


def test_b4_stale_scope_id_after_question_change_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    forged = AuditScope(
        scope_id=scope.scope_id,
        question="A different question",
        expected_registration_ids=scope.expected_registration_ids,
        context_fields=scope.context_fields,
    )
    with pytest.raises((TypeError, ValueError)):
        _produce(forged, assessment)


def test_b5_stale_scope_id_after_membership_change_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path / "source")
    extra = _historical(tmp_path / "extra")
    forged = AuditScope(
        scope_id=scope.scope_id,
        question=scope.question,
        expected_registration_ids=tuple(sorted((*scope.expected_registration_ids, extra.registration_id))),
        context_fields=scope.context_fields,
    )
    with pytest.raises((TypeError, ValueError)):
        _produce(forged, assessment)


def test_b6_stale_scope_id_after_context_change_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    forged = AuditScope(
        scope_id=scope.scope_id,
        question=scope.question,
        expected_registration_ids=scope.expected_registration_ids,
        context_fields=("decision",),
    )
    with pytest.raises((TypeError, ValueError)):
        _produce(forged, assessment)


def test_b7_scope_id_alone_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            scope.scope_id,
            "KEEP_CURRENT_STATE",
            _detail("KEEP_CURRENT_STATE", scope),
        )


# C — Disposition is explicit external input, exact and never auto-derived.


@pytest.mark.parametrize("disposition", DISPOSITIONS)
def test_c0_each_exact_disposition_is_accepted(tmp_path: Path, disposition: str) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment, disposition=disposition)
    assert decision.disposition == disposition


@pytest.mark.parametrize(
    "disposition",
    [
        None,
        "",
        "keep_current_state",
        "KEEP",
        "PASS",
        "FAIL",
        "BLOCKED",
        "CHANGE_RULE",
        "UPDATE_KNOWLEDGE",
        "AUTHORIZE_ACTION",
        "RUN_BACKTEST",
        "SEND_ORDER",
        "ACTIVATE_LIVE",
    ],
)
def test_c1_unknown_alias_or_promotional_disposition_is_rejected(tmp_path: Path, disposition) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            scope,
            disposition,
            "External detail.",
        )


def test_c2_producer_signature_is_exact_and_has_no_defaults() -> None:
    signature = inspect.signature(_p17().produce_revision_decision)
    assert tuple(signature.parameters) == ("assessment", "scope", "disposition", "detail")
    assert all(
        parameter.default is inspect.Parameter.empty
        for parameter in signature.parameters.values()
    )


@pytest.mark.parametrize("source_factory", [_pass_source, _fail_source, _blocked_source])
def test_c3_same_source_verdict_allows_multiple_explicit_dispositions(tmp_path: Path, source_factory) -> None:
    scope, assessment = source_factory(tmp_path)
    decisions = tuple(
        _produce(scope, assessment, disposition=disposition)
        for disposition in DISPOSITIONS
    )
    assert {decision.disposition for decision in decisions} == set(DISPOSITIONS)
    assert all(decision.source_verdict == assessment.verdict for decision in decisions)


# D — Detail is explicit text and reformulation must actually differ.


def test_d0_nonempty_detail_is_preserved_exactly(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    detail = "  Preserve this exact external wording.  "
    decision = _p17().produce_revision_decision(
        assessment,
        scope,
        "KEEP_CURRENT_STATE",
        detail,
    )
    assert decision.detail == detail


@pytest.mark.parametrize("detail", [None, "", " ", "\t", "\n  \t"])
def test_d1_missing_empty_or_whitespace_detail_is_rejected(tmp_path: Path, detail) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            scope,
            "KEEP_CURRENT_STATE",
            detail,
        )


def test_d2_identical_reformulation_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            scope,
            "REFORMULATE_QUESTION",
            scope.question,
        )


def test_d3_whitespace_equivalent_reformulation_is_rejected(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            assessment,
            scope,
            "REFORMULATE_QUESTION",
            "   " + scope.question + "   ",
        )


def test_d4_genuinely_different_reformulation_is_accepted(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    new_question = "Which narrower collection question should be audited next?"
    decision = _p17().produce_revision_decision(
        assessment,
        scope,
        "REFORMULATE_QUESTION",
        new_question,
    )
    assert decision.detail == new_question


# E — Source statuses are snapshotted exactly; BLOCKED can never disappear.


@pytest.mark.parametrize("source_factory", [_pass_source, _fail_source, _blocked_source])
def test_e0_source_verdict_is_preserved_exactly(tmp_path: Path, source_factory) -> None:
    scope, assessment = source_factory(tmp_path)
    decision = _produce(scope, assessment)
    assert decision.source_verdict == assessment.verdict
    assert decision.source_completeness_status == assessment.completeness_status
    assert decision.source_independence_status == assessment.independence_status


def test_e1_blocked_completeness_survives_revision(tmp_path: Path) -> None:
    scope, assessment = _blocked_source(tmp_path)
    decision = _produce(scope, assessment, disposition="REQUEST_NEW_EVIDENCE")
    assert decision.source_verdict == "BLOCKED"
    assert decision.source_completeness_status == "BLOCKED"
    assert decision.source_independence_status == "BLOCKED"


def test_e2_pass_collection_still_preserves_blocked_independence(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    assert assessment.verdict == "PASS"
    decision = _produce(scope, assessment)
    assert decision.source_verdict == "PASS"
    assert decision.source_independence_status == "BLOCKED"


def test_e3_no_override_or_force_parameters_exist() -> None:
    signature = inspect.signature(_p17().produce_revision_decision)
    forbidden = {
        "force",
        "override",
        "ignore_blocked",
        "assume_resolved",
        "authorized",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    }
    assert forbidden.isdisjoint(signature.parameters)


# F — Revision records an orientation, never the promoted semantic object.


@pytest.mark.parametrize("disposition", DISPOSITIONS)
def test_f0_revision_has_no_knowledge_rule_authorization_or_execution_fields(
    tmp_path: Path,
    disposition: str,
) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment, disposition=disposition)
    forbidden = (
        "supported",
        "refuted",
        "knowledge",
        "validated_knowledge",
        "confidence",
        "probability",
        "causal",
        "rule",
        "recommended_rule",
        "authorized",
        "authorization",
        "experiment_id",
        "evidence_id",
        "order_id",
        "backtest_id",
    )
    assert all(not hasattr(decision, name) for name in forbidden)


def test_f1_evidence_request_is_not_evidence(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment, disposition="REQUEST_NEW_EVIDENCE")
    assert not isinstance(decision, ResearchRunEvidence)
    assert not isinstance(decision, ResearchFindings)


def test_f2_experiment_request_is_not_experiment_or_research_evidence(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment, disposition="REQUEST_NEW_EXPERIMENT")
    assert not isinstance(decision, ResearchRunEvidence)
    assert not hasattr(decision, "experiment_id")


def test_f3_reformulation_is_not_new_audit_scope_or_hypothesis(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment, disposition="REFORMULATE_QUESTION")
    assert not isinstance(decision, AuditScope)
    assert not hasattr(decision, "hypothesis")


def test_f4_keep_current_state_does_not_claim_validation(tmp_path: Path) -> None:
    scope, assessment = _blocked_source(tmp_path)
    decision = _produce(scope, assessment, disposition="KEEP_CURRENT_STATE")
    assert decision.source_verdict == "BLOCKED"
    for name in ("valid", "validated", "resolved", "safe", "correct"):
        assert not hasattr(decision, name)


# G — RevisionDecision identity and process-local attestation.


def _manual_revision(source):
    return _p17().RevisionDecision(**asdict(source))


def test_g0_positive_revision_is_factory_attested(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    assert _p17().is_factory_attested_revision_decision(decision)


def test_g1_same_inputs_produce_same_id_but_distinct_attested_objects(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    first = _produce(scope, assessment)
    second = _produce(scope, assessment)
    assert first == second
    assert first is not second
    assert first.revision_id == second.revision_id
    assert _p17().is_factory_attested_revision_decision(first)
    assert _p17().is_factory_attested_revision_decision(second)


def test_g2_manual_same_valued_revision_is_not_attested(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    manual = _manual_revision(decision)
    assert manual == decision and manual is not decision
    assert not _p17().is_factory_attested_revision_decision(manual)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_g3_copy_or_deepcopy_revision_is_not_attested(tmp_path: Path, copier) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    copied = copier(decision)
    assert copied == decision and copied is not decision
    assert not _p17().is_factory_attested_revision_decision(copied)


def test_g3_replace_revision_is_not_attested(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    copied = replace(decision, revision_id=decision.revision_id)
    assert copied == decision and copied is not decision
    assert not _p17().is_factory_attested_revision_decision(copied)


def test_g4_mutation_invalidates_revision_attestation(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    object.__setattr__(decision, "detail", "MUTATED")
    assert not _p17().is_factory_attested_revision_decision(decision)


def test_g5_changing_disposition_changes_revision_id(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    keep = _produce(scope, assessment, disposition="KEEP_CURRENT_STATE")
    evidence = _produce(scope, assessment, disposition="REQUEST_NEW_EVIDENCE")
    assert keep.revision_id != evidence.revision_id


def test_g6_changing_detail_changes_revision_id(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    one = _p17().produce_revision_decision(
        assessment, scope, "KEEP_CURRENT_STATE", "Reason one."
    )
    two = _p17().produce_revision_decision(
        assessment, scope, "KEEP_CURRENT_STATE", "Reason two."
    )
    assert one.revision_id != two.revision_id


def test_g7_revision_id_alone_is_not_revision_authority(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    assert not _p17().is_factory_attested_revision_decision(decision.revision_id)


# H — No reverse authority, time repair, operational bypass or hidden mutation.


def test_h0_revision_does_not_mutate_or_repair_upstream_objects(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    scope_snapshot = asdict(scope)
    assessment_snapshot = asdict(assessment)
    _produce(scope, assessment)
    assert asdict(scope) == scope_snapshot
    assert asdict(assessment) == assessment_snapshot
    assert is_factory_attested_memory_collection_audit(assessment)


def test_h1_revision_is_not_audit_memory_or_research_object(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    assert not isinstance(decision, AuditScope)
    assert not isinstance(decision, MemoryCollectionAuditAssessment)
    assert not isinstance(decision, HistoricalMemoryEpisode)
    assert not isinstance(decision, ResearchRunEvidence)
    assert not isinstance(decision, ResearchFindings)


def test_h2_revision_has_no_implicit_time_fields(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    forbidden = ("known_from", "valid_from", "revision_at", "registered_at", "created_at")
    assert all(not hasattr(decision, name) for name in forbidden)


def test_h3_runtime_source_uses_no_local_clock_or_operational_surface() -> None:
    source = inspect.getsource(_p17())
    forbidden = (
        "datetime.now",
        "datetime.utcnow",
        "time.time",
        "order_send",
        "MetaTrader5",
        "mt5.",
        "run_backtest(",
        "activate_live(",
        "submit_order(",
        "create_order(",
        "position_size",
        "lot_size",
        "stop_loss",
        "take_profit",
        "AUTHORIZED",
        "SUPPORTED",
    )
    assert all(token not in source for token in forbidden)


def test_h4_revision_cannot_substitute_for_audit_assessment(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = _produce(scope, assessment)
    with pytest.raises((TypeError, ValueError)):
        _p17().produce_revision_decision(
            decision,
            scope,
            "KEEP_CURRENT_STATE",
            "No change.",
        )


def test_h5_revision_api_exposes_no_behavior_change_or_execution_parameters() -> None:
    signature = inspect.signature(_p17().produce_revision_decision)
    forbidden = {
        "action",
        "behavior",
        "rule",
        "knowledge",
        "confidence",
        "broker",
        "order",
        "backtest",
        "live",
        "execute",
        "experiment",
        "evidence",
    }
    assert forbidden.isdisjoint(signature.parameters)
