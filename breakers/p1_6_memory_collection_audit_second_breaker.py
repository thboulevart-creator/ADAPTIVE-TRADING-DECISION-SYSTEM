from __future__ import annotations

import gc
import weakref
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
    is_factory_attested_historical_memory,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from tests.research_runtime_fixture import CODE_VERSION, synthetic_runtime_case


AUTHORITY_ID = "P1_6_SECOND_BREAKER_AUTHORITY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"


def _episode(
    *,
    decision_payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
    code_version: str = CODE_VERSION,
):
    with synthetic_runtime_case(code_version=code_version) as case:
        decision = produce_decision(case.evidence, context=case.context, decision=decision_payload)
        action = engage_qualification_action(decision, behavior=behavior)
        result = observe_qualification_result(action, outcome=outcome)
        trace = produce_decision_trace(case.evidence, decision, action, result)
        return produce_observational_memory_episode(trace, action, result)


def _historical_from_episode(tmp_path: Path, episode):
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def _historical(
    tmp_path: Path,
    *,
    decision_payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
    code_version: str = CODE_VERSION,
):
    return _historical_from_episode(
        tmp_path,
        _episode(
            decision_payload=decision_payload,
            behavior=behavior,
            outcome=outcome,
            code_version=code_version,
        ),
    )


def _scope(
    memories: tuple[HistoricalMemoryEpisode, ...],
    *,
    bounded: bool = True,
    question: str = "Second-order collection audit.",
    context_fields: tuple[str, ...] = ("context_id", "decision", "behavior"),
):
    expected = tuple(memory.registration_id for memory in memories) if bounded else None
    return create_audit_scope(
        question=question,
        expected_registration_ids=expected,
        context_fields=context_fields,
    )


# I — AuditScope is content-bound value declaration, never stale/collision-permissive.


def test_i0_manual_same_valued_scope_is_equivalent_value_declaration(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    factory = _scope((memory,))
    manual = AuditScope(**asdict(factory))
    assert manual == factory and manual is not factory
    assert audit_memory_collection(manual, (memory,)) == audit_memory_collection(factory, (memory,))


def test_i1_scope_id_copied_to_different_question_is_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    original = _scope((memory,), question="Q1")
    forged = AuditScope(
        scope_id=original.scope_id,
        question="Q2",
        expected_registration_ids=original.expected_registration_ids,
        context_fields=original.context_fields,
    )
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(forged, (memory,))


def test_i2_scope_id_copied_to_different_membership_is_rejected(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    original = _scope((first,))
    forged = AuditScope(
        scope_id=original.scope_id,
        question=original.question,
        expected_registration_ids=tuple(sorted((first.registration_id, second.registration_id))),
        context_fields=original.context_fields,
    )
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(forged, (first, second))


def test_i3_object_setattr_scope_mutation_is_rejected_on_use(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    object.__setattr__(scope, "question", "MUTATED")
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(scope, (memory,))


def test_i4_expected_membership_order_is_canonicalized(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    one = create_audit_scope(
        question="Q",
        expected_registration_ids=(first.registration_id, second.registration_id),
        context_fields=("context_id",),
    )
    two = create_audit_scope(
        question="Q",
        expected_registration_ids=(second.registration_id, first.registration_id),
        context_fields=("context_id",),
    )
    assert one == two
    assert one.scope_id == two.scope_id
    assert one.expected_registration_ids == tuple(sorted(one.expected_registration_ids))


def test_i5_context_field_order_is_explicit_scope_content_not_silently_rewritten(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    one = create_audit_scope(
        question="Q",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("decision", "behavior"),
    )
    two = create_audit_scope(
        question="Q",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("behavior", "decision"),
    )
    assert one.scope_id != two.scope_id
    assert one.context_fields == ("decision", "behavior")
    assert two.context_fields == ("behavior", "decision")


# J — Assessment identities remain exact-object attested and collision resistant.


def test_j0_repeated_identical_audit_mints_equal_distinct_attested_assessments(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    first = audit_memory_collection(scope, (memory,))
    second = audit_memory_collection(scope, (memory,))
    assert first == second
    assert first is not second
    assert first.audit_id == second.audit_id
    assert is_factory_attested_memory_collection_audit(first)
    assert is_factory_attested_memory_collection_audit(second)


def test_j1_manual_assessment_with_same_audit_id_but_changed_verdict_is_not_attested(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    original = audit_memory_collection(_scope((memory,)), (memory,))
    forged = MemoryCollectionAuditAssessment(
        **{
            **asdict(original),
            "verdict": "BLOCKED",
        }
    )
    assert forged.audit_id == original.audit_id
    assert not is_factory_attested_memory_collection_audit(forged)


def test_j2_nested_structural_replacement_invalidates_assessment_attestation(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    assessment = audit_memory_collection(_scope((first, second)), (first, second))
    object.__setattr__(
        assessment,
        "content_groups",
        assessment.content_groups + (("FAKE", ("MREG-FAKE",)),),
    )
    assert not is_factory_attested_memory_collection_audit(assessment)


def test_j3_different_input_collection_changes_audit_identity(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    scope = _scope((first, second))
    complete = audit_memory_collection(scope, (first, second))
    incomplete = audit_memory_collection(scope, (first,))
    assert complete.audit_id != incomplete.audit_id
    assert complete.verdict == "PASS"
    assert incomplete.verdict == "FAIL"


# K — Shared authentic registrations cannot bypass duplicate detection.


def _reattest_capture(capture):
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id=P15_CONTRACT,
        expected_authority_id=AUTHORITY_ID,
        expected_receipt_sha256=capture.receipt_sha256,
    )


def test_k0_two_authentic_objects_same_registration_fail_regardless_input_order(tmp_path: Path) -> None:
    episode = _episode()
    capture = persist_witnessed_memory_episode(tmp_path / "capture", episode, authority_id=AUTHORITY_ID)
    first = _reattest_capture(capture)
    second = _reattest_capture(capture)
    scope = _scope((first,))
    forward = audit_memory_collection(scope, (first, second))
    reverse = audit_memory_collection(scope, (second, first))
    assert forward == reverse
    assert forward.verdict == "FAIL"
    assert forward.duplicate_registration_ids == (first.registration_id,)


def test_k1_invalid_member_is_rejected_before_registration_deduplication(tmp_path: Path) -> None:
    episode = _episode()
    capture = persist_witnessed_memory_episode(tmp_path / "capture", episode, authority_id=AUTHORITY_ID)
    first = _reattest_capture(capture)
    second = _reattest_capture(capture)
    object.__setattr__(second, "authority_id", "MUTATED")
    assert not is_factory_attested_historical_memory(second)
    with pytest.raises((TypeError, ValueError)):
        audit_memory_collection(_scope((first,)), (first, second))


def test_k2_same_content_multiple_registrations_plus_duplicate_tracks_both_dimensions(tmp_path: Path) -> None:
    episode = _episode()
    first = _historical_from_episode(tmp_path / "first", episode)
    second = _historical_from_episode(tmp_path / "second", episode)
    assessment = audit_memory_collection(_scope((first, second)), (first, second, first))
    assert assessment.verdict == "FAIL"
    assert assessment.duplicate_registration_ids == (first.registration_id,)
    assert assessment.unique_episode_ids == (episode.episode_id,)
    assert assessment.content_groups == (
        (episode.episode_id, tuple(sorted((first.registration_id, second.registration_id)))),
    )
    assert assessment.independence_status == "BLOCKED"


# L — Adversarial grouping stays deterministic and scope-controlled.


def test_l0_code_version_dimension_separates_otherwise_similar_memories(tmp_path: Path) -> None:
    code_a = "a" * 40
    code_b = "b" * 40
    first = _historical(tmp_path / "first", code_version=code_a)
    second = _historical(tmp_path / "second", code_version=code_b)
    scope = _scope((first, second), context_fields=("code_version",))
    assessment = audit_memory_collection(scope, (first, second))
    keys = {key for key, _ in assessment.context_groups}
    assert keys == {
        (("code_version", code_a),),
        (("code_version", code_b),),
    }


def test_l1_behavior_dimension_separates_behavior_variants(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", behavior="NO_ACTION")
    second = _historical(tmp_path / "second", behavior="REDUCE")
    scope = _scope((first, second), context_fields=("behavior",))
    assessment = audit_memory_collection(scope, (first, second))
    assert len(assessment.context_groups) == 2


def test_l2_coarse_grouping_does_not_merge_different_decisions_into_one_contradiction(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", decision_payload="HOLD", outcome="WIN")
    second = _historical(tmp_path / "second", decision_payload="EXIT", outcome="LOSS")
    scope = _scope((first, second), context_fields=("context_id",))
    assessment = audit_memory_collection(scope, (first, second))
    assert len(assessment.context_groups) == 1
    assert assessment.contradiction_groups == ()


def test_l3_context_group_key_order_follows_declared_scope_deterministically(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one", decision_payload="HOLD", behavior="NO_ACTION")
    scope = _scope((memory,), context_fields=("behavior", "decision"))
    assessment = audit_memory_collection(scope, (memory,))
    key, registrations = assessment.context_groups[0]
    assert key == (("behavior", "NO_ACTION"), ("decision", "HOLD"))
    assert registrations == (memory.registration_id,)


# M — Contradiction reporting stays descriptive under ambiguous collections.


def test_m0_two_independent_contradiction_subgroups_in_same_context_stay_separate(tmp_path: Path) -> None:
    a1 = _historical(tmp_path / "a1", decision_payload="HOLD", behavior="NO_ACTION", outcome="WIN")
    a2 = _historical(tmp_path / "a2", decision_payload="HOLD", behavior="NO_ACTION", outcome="LOSS")
    b1 = _historical(tmp_path / "b1", decision_payload="EXIT", behavior="REDUCE", outcome="UP")
    b2 = _historical(tmp_path / "b2", decision_payload="EXIT", behavior="REDUCE", outcome="DOWN")
    memories = (a1, a2, b1, b2)
    assessment = audit_memory_collection(
        _scope(memories, context_fields=("context_id",)),
        memories,
    )
    expected = {
        tuple(sorted((a1.registration_id, a2.registration_id))),
        tuple(sorted((b1.registration_id, b2.registration_id))),
    }
    assert set(assessment.contradiction_groups) == expected


def test_m1_same_content_recapture_can_appear_in_contradiction_without_becoming_replication(tmp_path: Path) -> None:
    win_episode = _episode(outcome="WIN")
    win_one = _historical_from_episode(tmp_path / "win-one", win_episode)
    win_two = _historical_from_episode(tmp_path / "win-two", win_episode)
    loss = _historical(tmp_path / "loss", outcome="LOSS")
    memories = (win_one, win_two, loss)
    assessment = audit_memory_collection(
        _scope(memories, context_fields=("context_id",)),
        memories,
    )
    expected = tuple(sorted(memory.registration_id for memory in memories))
    assert expected in assessment.contradiction_groups
    assert len(assessment.unique_episode_ids) == 2
    assert assessment.independence_status == "BLOCKED"


def test_m2_bounded_collection_with_preserved_contradiction_can_still_pass_collection_integrity(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="WIN")
    second = _historical(tmp_path / "second", outcome="LOSS")
    memories = (first, second)
    assessment = audit_memory_collection(
        _scope(memories, context_fields=("context_id",)),
        memories,
    )
    assert assessment.verdict == "PASS"
    assert assessment.completeness_status == "PASS"
    assert assessment.contradiction_groups
    assert assessment.independence_status == "BLOCKED"


# N — Canonicalization and determinism are exact across equivalent executions.


def test_n0_all_structural_outputs_are_input_order_invariant(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="ONE")
    second = _historical(tmp_path / "second", outcome="TWO")
    third = _historical(tmp_path / "third", decision_payload="EXIT", outcome="THREE")
    memories = (first, second, third)
    scope = _scope(memories, context_fields=("context_id", "decision", "behavior"))
    a = audit_memory_collection(scope, memories)
    b = audit_memory_collection(scope, tuple(reversed(memories)))
    assert a == b
    assert a.audit_id == b.audit_id
    assert a.anomalies == tuple(sorted(a.anomalies))
    assert a.unique_episode_ids == tuple(sorted(a.unique_episode_ids))
    assert a.examined_registration_ids == tuple(sorted(a.examined_registration_ids))


def test_n1_duplicate_presence_changes_audit_identity_but_not_unique_membership(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    clean = audit_memory_collection(scope, (memory,))
    duplicate = audit_memory_collection(scope, (memory, memory))
    assert clean.audit_id != duplicate.audit_id
    assert clean.examined_registration_ids == duplicate.examined_registration_ids
    assert clean.verdict == "PASS"
    assert duplicate.verdict == "FAIL"


def test_n2_same_scope_and_same_registration_reverified_produce_same_clean_assessment(tmp_path: Path) -> None:
    episode = _episode()
    capture = persist_witnessed_memory_episode(tmp_path / "capture", episode, authority_id=AUTHORITY_ID)
    first = _reattest_capture(capture)
    scope = _scope((first,))
    first_assessment = audit_memory_collection(scope, (first,))
    del first
    second = _reattest_capture(capture)
    second_assessment = audit_memory_collection(scope, (second,))
    assert first_assessment == second_assessment
    assert first_assessment.audit_id == second_assessment.audit_id


# O — BLOCKED cannot be promoted away by collection shape or object forgery.


def test_o0_unknown_universe_with_contradiction_remains_blocked(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="WIN")
    second = _historical(tmp_path / "second", outcome="LOSS")
    memories = (first, second)
    assessment = audit_memory_collection(
        _scope(memories, bounded=False, context_fields=("context_id",)),
        memories,
    )
    assert assessment.verdict == "BLOCKED"
    assert assessment.completeness_status == "BLOCKED"
    assert assessment.independence_status == "BLOCKED"
    assert assessment.contradiction_groups


def test_o1_unknown_universe_with_duplicate_is_fail_but_blocked_dimensions_stay_blocked(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = audit_memory_collection(_scope((memory,), bounded=False), (memory, memory))
    assert assessment.verdict == "FAIL"
    assert assessment.completeness_status == "BLOCKED"
    assert assessment.independence_status == "BLOCKED"


def test_o2_bounded_many_distinct_contents_never_unblocks_independence(tmp_path: Path) -> None:
    memories = tuple(_historical(tmp_path / f"m{i}", outcome=f"O{i}") for i in range(5))
    assessment = audit_memory_collection(_scope(memories), memories)
    assert assessment.verdict == "PASS"
    assert assessment.completeness_status == "PASS"
    assert assessment.independence_status == "BLOCKED"


def test_o3_manual_same_id_assessment_claiming_independence_pass_is_not_attested(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    original = audit_memory_collection(_scope((memory,)), (memory,))
    forged = MemoryCollectionAuditAssessment(
        **{
            **asdict(original),
            "independence_status": "PASS",
        }
    )
    assert forged.audit_id == original.audit_id
    assert not is_factory_attested_memory_collection_audit(forged)


def test_o4_mutating_attested_assessment_to_unblock_independence_invalidates_it(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = audit_memory_collection(_scope((memory,)), (memory,))
    object.__setattr__(assessment, "independence_status", "PASS")
    assert not is_factory_attested_memory_collection_audit(assessment)


# P — Audit assessment is a historical snapshot; upstream later mutation/GC cannot rewrite it.


def test_p0_upstream_memory_mutation_after_audit_does_not_rewrite_existing_assessment(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = audit_memory_collection(_scope((memory,)), (memory,))
    snapshot = asdict(assessment)
    object.__setattr__(memory.episode, "outcome", "MUTATED_AFTER_AUDIT")
    assert not is_factory_attested_historical_memory(memory)
    assert asdict(assessment) == snapshot
    assert is_factory_attested_memory_collection_audit(assessment)


def test_p1_upstream_memory_collection_can_be_garbage_collected_after_audit(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    registration_id = memory.registration_id
    assessment = audit_memory_collection(scope, (memory,))
    reference = weakref.ref(memory)
    del memory
    gc.collect()
    assert reference() is None
    assert assessment.examined_registration_ids == (registration_id,)
    assert is_factory_attested_memory_collection_audit(assessment)


def test_p2_scope_mutation_after_audit_does_not_rewrite_existing_assessment(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    assessment = audit_memory_collection(scope, (memory,))
    snapshot = asdict(assessment)
    object.__setattr__(scope, "question", "MUTATED_AFTER_AUDIT")
    assert asdict(assessment) == snapshot
    assert is_factory_attested_memory_collection_audit(assessment)
