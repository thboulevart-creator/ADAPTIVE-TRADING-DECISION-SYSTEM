from __future__ import annotations

import gc
import inspect
import unicodedata
import weakref
from dataclasses import asdict, fields
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
from src.revision import (
    RevisionDecision,
    is_factory_attested_revision_decision,
    produce_revision_decision,
)
from tests.research_runtime_fixture import synthetic_runtime_case


AUTHORITY_ID = "P1_7_SECOND_BREAKER_AUTHORITY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"


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


def _bounded_scope(memories: tuple[HistoricalMemoryEpisode, ...], *, question: str = "Q") -> AuditScope:
    return create_audit_scope(
        question=question,
        expected_registration_ids=tuple(memory.registration_id for memory in memories),
        context_fields=("context_id", "decision", "behavior"),
    )


def _pass_source(tmp_path: Path):
    memory = _historical(tmp_path / "one")
    scope = _bounded_scope((memory,), question="Should the current audited state remain unchanged?")
    assessment = audit_memory_collection(scope, (memory,))
    assert assessment.verdict == "PASS"
    return scope, assessment


def _same_scope_pass_and_fail(tmp_path: Path):
    first = _historical(tmp_path / "first", outcome="ONE")
    second = _historical(tmp_path / "second", outcome="TWO")
    scope = _bounded_scope((first, second), question="How complete is this bounded collection?")
    complete = audit_memory_collection(scope, (first, second))
    incomplete = audit_memory_collection(scope, (first,))
    assert complete.verdict == "PASS"
    assert incomplete.verdict == "FAIL"
    assert complete.scope_id == incomplete.scope_id == scope.scope_id
    assert complete.audit_id != incomplete.audit_id
    return scope, complete, incomplete


def _blocked_source(tmp_path: Path):
    memory = _historical(tmp_path / "one")
    scope = create_audit_scope(
        question="What should happen while completeness is unknown?",
        expected_registration_ids=None,
        context_fields=("context_id", "decision", "behavior"),
    )
    assessment = audit_memory_collection(scope, (memory,))
    assert assessment.verdict == "BLOCKED"
    return scope, assessment


def _detail(disposition: str) -> str:
    return {
        "KEEP_CURRENT_STATE": "Keep the state unchanged while preserving all audit limitations.",
        "REQUEST_NEW_EVIDENCE": "Request additional documentary evidence.",
        "REQUEST_NEW_EXPERIMENT": "Request a separately governed new experiment.",
        "REFORMULATE_QUESTION": "Which narrower question should be audited next?",
    }[disposition]


# I — revision_id cannot be rebound to another authentic audit or payload.


def test_i0_two_authentic_assessments_same_scope_bind_distinct_revision_ids(tmp_path: Path) -> None:
    scope, complete, incomplete = _same_scope_pass_and_fail(tmp_path)
    first = produce_revision_decision(complete, scope, "KEEP_CURRENT_STATE", "Same external detail.")
    second = produce_revision_decision(incomplete, scope, "KEEP_CURRENT_STATE", "Same external detail.")
    assert first.scope_id == second.scope_id
    assert first.audit_id != second.audit_id
    assert first.revision_id != second.revision_id
    assert first.source_verdict == "PASS"
    assert second.source_verdict == "FAIL"


def test_i1_manual_rebinding_of_revision_id_to_other_authentic_audit_is_not_attested(tmp_path: Path) -> None:
    scope, complete, incomplete = _same_scope_pass_and_fail(tmp_path)
    first = produce_revision_decision(complete, scope, "KEEP_CURRENT_STATE", "Same external detail.")
    second = produce_revision_decision(incomplete, scope, "KEEP_CURRENT_STATE", "Same external detail.")
    forged = RevisionDecision(
        revision_id=first.revision_id,
        audit_id=second.audit_id,
        scope_id=second.scope_id,
        disposition=second.disposition,
        detail=second.detail,
        source_verdict=second.source_verdict,
        source_completeness_status=second.source_completeness_status,
        source_independence_status=second.source_independence_status,
    )
    assert not is_factory_attested_revision_decision(forged)


def test_i2_manual_rebinding_of_revision_id_to_changed_detail_is_not_attested(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    original = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason A.")
    forged = RevisionDecision(
        revision_id=original.revision_id,
        audit_id=original.audit_id,
        scope_id=original.scope_id,
        disposition=original.disposition,
        detail="Reason B.",
        source_verdict=original.source_verdict,
        source_completeness_status=original.source_completeness_status,
        source_independence_status=original.source_independence_status,
    )
    assert not is_factory_attested_revision_decision(forged)


def test_i3_mutating_revision_id_invalidates_attestation(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    object.__setattr__(decision, "revision_id", "REV-" + "0" * 32)
    assert not is_factory_attested_revision_decision(decision)


# J — Mutation lifecycle: once an observed mutation invalidates authority, restoring values cannot revive it.


@pytest.mark.parametrize(
    ("field", "mutated"),
    [
        ("detail", "MUTATED"),
        ("source_verdict", "BLOCKED"),
        ("source_independence_status", "PASS"),
        ("disposition", "REQUEST_NEW_EVIDENCE"),
    ],
)
def test_j0_observed_mutation_then_restore_does_not_revive_attestation(
    tmp_path: Path,
    field: str,
    mutated: str,
) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Original detail.")
    original = getattr(decision, field)
    object.__setattr__(decision, field, mutated)
    assert not is_factory_attested_revision_decision(decision)
    object.__setattr__(decision, field, original)
    assert not is_factory_attested_revision_decision(decision)


def test_j1_unmutated_revision_remains_attested_across_repeated_verification(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    assert is_factory_attested_revision_decision(decision)
    assert is_factory_attested_revision_decision(decision)
    assert is_factory_attested_revision_decision(decision)


def test_j2_upstream_assessment_mutation_after_revision_does_not_rewrite_revision_snapshot(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    snapshot = asdict(decision)
    object.__setattr__(assessment, "verdict", "BLOCKED")
    assert not is_factory_attested_memory_collection_audit(assessment)
    assert asdict(decision) == snapshot
    assert is_factory_attested_revision_decision(decision)


def test_j3_upstream_scope_mutation_after_revision_does_not_rewrite_revision_snapshot(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    snapshot = asdict(decision)
    object.__setattr__(scope, "question", "MUTATED AFTER REVISION")
    assert asdict(decision) == snapshot
    assert is_factory_attested_revision_decision(decision)


def test_j4_upstream_objects_can_be_collected_after_revision(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    audit_id = assessment.audit_id
    scope_id = scope.scope_id
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    assessment_ref = weakref.ref(assessment)
    del assessment
    del scope
    gc.collect()
    assert assessment_ref() is None
    assert decision.audit_id == audit_id
    assert decision.scope_id == scope_id
    assert is_factory_attested_revision_decision(decision)


# K — Same-valued scopes remain value declarations, while adversarial stale scopes stay rejected.


def test_k0_fresh_same_valued_scope_reconstruction_produces_same_revision_identity(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    reconstructed = AuditScope(**asdict(scope))
    first = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    second = produce_revision_decision(assessment, reconstructed, "KEEP_CURRENT_STATE", "Reason.")
    assert reconstructed == scope and reconstructed is not scope
    assert first.revision_id == second.revision_id


@pytest.mark.parametrize(
    "mutator",
    [
        lambda scope: AuditScope(
            scope.scope_id,
            scope.question + " ",
            scope.expected_registration_ids,
            scope.context_fields,
        ),
        lambda scope: AuditScope(
            scope.scope_id,
            scope.question,
            scope.expected_registration_ids,
            ("decision",),
        ),
    ],
)
def test_k1_stale_same_id_scope_variants_remain_rejected(tmp_path: Path, mutator) -> None:
    scope, assessment = _pass_source(tmp_path)
    forged = mutator(scope)
    with pytest.raises((TypeError, ValueError)):
        produce_revision_decision(assessment, forged, "KEEP_CURRENT_STATE", "Reason.")


def test_k2_scope_from_other_authentic_assessment_same_question_is_rejected(tmp_path: Path) -> None:
    first_scope, first_assessment = _pass_source(tmp_path / "first")
    second_scope, _ = _pass_source(tmp_path / "second")
    assert first_scope.question == second_scope.question
    assert first_scope.scope_id != second_scope.scope_id
    with pytest.raises((TypeError, ValueError)):
        produce_revision_decision(first_assessment, second_scope, "KEEP_CURRENT_STATE", "Reason.")


# L — Authentic assessment substitution remains visible and cannot silently inherit another audit's statuses.


def test_l0_same_scope_authentic_assessment_substitution_snapshots_actual_source(tmp_path: Path) -> None:
    scope, complete, incomplete = _same_scope_pass_and_fail(tmp_path)
    complete_revision = produce_revision_decision(complete, scope, "REQUEST_NEW_EVIDENCE", "Need evidence.")
    incomplete_revision = produce_revision_decision(incomplete, scope, "REQUEST_NEW_EVIDENCE", "Need evidence.")
    assert complete_revision.audit_id == complete.audit_id
    assert complete_revision.source_verdict == complete.verdict
    assert incomplete_revision.audit_id == incomplete.audit_id
    assert incomplete_revision.source_verdict == incomplete.verdict
    assert complete_revision.revision_id != incomplete_revision.revision_id


def test_l1_same_valued_authentic_assessments_produce_same_content_identity_but_distinct_revision_objects(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _bounded_scope((memory,), question="Q")
    first_assessment = audit_memory_collection(scope, (memory,))
    second_assessment = audit_memory_collection(scope, (memory,))
    assert first_assessment == second_assessment
    assert first_assessment is not second_assessment
    first = produce_revision_decision(first_assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    second = produce_revision_decision(second_assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    assert first == second
    assert first is not second
    assert first.revision_id == second.revision_id
    assert is_factory_attested_revision_decision(first)
    assert is_factory_attested_revision_decision(second)


# M — BLOCKED survives every externally selected disposition and adversarial combination.


@pytest.mark.parametrize(
    "disposition",
    [
        "KEEP_CURRENT_STATE",
        "REQUEST_NEW_EVIDENCE",
        "REQUEST_NEW_EXPERIMENT",
        "REFORMULATE_QUESTION",
    ],
)
def test_m0_blocked_source_stays_blocked_under_every_disposition(tmp_path: Path, disposition: str) -> None:
    scope, assessment = _blocked_source(tmp_path)
    decision = produce_revision_decision(assessment, scope, disposition, _detail(disposition))
    assert decision.source_verdict == "BLOCKED"
    assert decision.source_completeness_status == "BLOCKED"
    assert decision.source_independence_status == "BLOCKED"


def test_m1_fail_source_preserves_fail_and_blocked_independence(tmp_path: Path) -> None:
    scope, _, assessment = _same_scope_pass_and_fail(tmp_path)
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    assert decision.source_verdict == "FAIL"
    assert decision.source_completeness_status == "FAIL"
    assert decision.source_independence_status == "BLOCKED"


def test_m2_manual_claim_that_blocked_independence_became_pass_is_not_attested(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    original = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    forged = RevisionDecision(
        revision_id=original.revision_id,
        audit_id=original.audit_id,
        scope_id=original.scope_id,
        disposition=original.disposition,
        detail=original.detail,
        source_verdict=original.source_verdict,
        source_completeness_status=original.source_completeness_status,
        source_independence_status="PASS",
    )
    assert not is_factory_attested_revision_decision(forged)


# N — Detail is exact external text; ambiguity never becomes hidden semantics.


def test_n0_leading_and_trailing_whitespace_is_preserved_and_changes_identity(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    plain = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    spaced = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "  Reason.  ")
    assert spaced.detail == "  Reason.  "
    assert plain.revision_id != spaced.revision_id


def test_n1_multiline_detail_is_preserved_verbatim(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    detail = "Line one.\nLine two.\n"
    decision = produce_revision_decision(assessment, scope, "REQUEST_NEW_EVIDENCE", detail)
    assert decision.detail == detail


def test_n2_promotional_words_inside_detail_do_not_change_disposition_or_create_authority(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    detail = "AUTHORIZED SUPPORTED RUN_BACKTEST are quoted text only."
    decision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", detail)
    assert decision.disposition == "KEEP_CURRENT_STATE"
    assert decision.detail == detail
    for name in ("authorized", "supported", "backtest_id", "knowledge", "confidence"):
        assert not hasattr(decision, name)


def test_n3_unicode_equivalent_detail_remains_exact_external_text_not_silently_normalized(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    composed = "Caf\u00e9 rationale."
    decomposed = unicodedata.normalize("NFD", composed)
    assert composed != decomposed
    first = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", composed)
    second = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", decomposed)
    assert first.detail == composed
    assert second.detail == decomposed
    assert first.revision_id != second.revision_id


# O — Determinism and canonical output shape.


def test_o0_revision_decision_fields_are_exactly_the_selected_minimal_model() -> None:
    assert tuple(field.name for field in fields(RevisionDecision)) == (
        "revision_id",
        "audit_id",
        "scope_id",
        "disposition",
        "detail",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_o1_same_content_after_fresh_audit_reproduction_has_same_revision_id(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _bounded_scope((memory,), question="Q")
    first_assessment = audit_memory_collection(scope, (memory,))
    second_assessment = audit_memory_collection(scope, (memory,))
    first = produce_revision_decision(first_assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    second = produce_revision_decision(second_assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    assert first.revision_id == second.revision_id
    assert first == second


def test_o2_each_content_component_changes_identity(tmp_path: Path) -> None:
    scope, complete, incomplete = _same_scope_pass_and_fail(tmp_path)
    base = produce_revision_decision(complete, scope, "KEEP_CURRENT_STATE", "Reason.")
    changed_detail = produce_revision_decision(complete, scope, "KEEP_CURRENT_STATE", "Other reason.")
    changed_disposition = produce_revision_decision(complete, scope, "REQUEST_NEW_EVIDENCE", "Reason.")
    changed_audit = produce_revision_decision(incomplete, scope, "KEEP_CURRENT_STATE", "Reason.")
    assert len(
        {
            base.revision_id,
            changed_detail.revision_id,
            changed_disposition.revision_id,
            changed_audit.revision_id,
        }
    ) == 4


# P — Reverse authority remains impossible; revision is an autonomous historical decision snapshot.


def test_p0_revision_cannot_substitute_for_audit_scope(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    revision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(revision, ())


def test_p1_revision_cannot_substitute_for_audit_assessment(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    revision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    with pytest.raises((TypeError, ValueError)):
        produce_revision_decision(revision, scope, "KEEP_CURRENT_STATE", "Reason.")


def test_p2_revision_cannot_substitute_for_historical_memory(tmp_path: Path) -> None:
    scope, assessment = _pass_source(tmp_path)
    revision = produce_revision_decision(assessment, scope, "KEEP_CURRENT_STATE", "Reason.")
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(scope, (revision,))


def test_p3_runtime_has_no_hidden_time_io_network_or_execution_surface() -> None:
    source = inspect.getsource(__import__("src.revision", fromlist=["*"]))
    forbidden = (
        "datetime.now",
        "datetime.utcnow",
        "time.time",
        "Path(",
        "open(",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
        "run_backtest(",
        "activate_live(",
        "submit_order(",
        "create_order(",
    )
    assert all(token not in source for token in forbidden)
