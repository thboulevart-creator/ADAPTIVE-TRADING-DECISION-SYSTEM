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
from src.memory_episode import ObservationalMemoryEpisode, produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    is_factory_attested_historical_memory,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.research_findings import ResearchFindings
from src.research_run_evidence import ResearchRunEvidence
from tests.research_runtime_fixture import CODE_VERSION, synthetic_runtime_case


P16_CONTRACT = "P1_6_MEMORY_COLLECTION_AUDIT_BOUNDARY_V1"
AUTHORITY_ID = "P1_6_TEST_CAPTURE_AUTHORITY_V1"
ALLOWED_CONTEXT_FIELDS = {
    "provenance_id",
    "research_run_id",
    "code_version",
    "configuration_version",
    "dataset_id",
    "dataset_version",
    "context_id",
    "decision",
    "behavior",
}


def _p16():
    try:
        module = importlib.import_module("src.memory_audit")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.6 candidate absent — expected pre-implementation FAIL: "
            "src.memory_audit does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "AuditScope",
        "MemoryCollectionAuditAssessment",
        "create_audit_scope",
        "audit_memory_collection",
        "is_factory_attested_memory_collection_audit",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.6 candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P16_CONTRACT
    return module


def _p14_episode(
    *,
    decision_payload: str = "HOLD",
    behavior: str = "NO_ACTION",
    outcome: str = "OBSERVED",
    code_version: str = CODE_VERSION,
) -> ObservationalMemoryEpisode:
    with synthetic_runtime_case(code_version=code_version) as case:
        decision = produce_decision(case.evidence, context=case.context, decision=decision_payload)
        action = engage_qualification_action(decision, behavior=behavior)
        result = observe_qualification_result(action, outcome=outcome)
        trace = produce_decision_trace(case.evidence, decision, action, result)
        return produce_observational_memory_episode(trace, action, result)


def _historical_from_episode(tmp_path: Path, episode: ObservationalMemoryEpisode) -> HistoricalMemoryEpisode:
    capture = persist_witnessed_memory_episode(tmp_path, episode, authority_id=AUTHORITY_ID)
    return reattest_persisted_memory_episode(
        capture.record_path,
        capture.receipt_path,
        expected_contract_id="P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1",
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
) -> HistoricalMemoryEpisode:
    return _historical_from_episode(
        tmp_path,
        _p14_episode(
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
    question: str = "Audit declared collection membership and grouping.",
    context_fields: tuple[str, ...] = ("context_id", "decision", "behavior"),
):
    expected = tuple(memory.registration_id for memory in memories) if bounded else None
    return _p16().create_audit_scope(
        question=question,
        expected_registration_ids=expected,
        context_fields=context_fields,
    )


def _audit(scope, memories):
    return _p16().audit_memory_collection(scope, memories)


def _content_group_map(assessment) -> dict[str, tuple[str, ...]]:
    return {episode_id: tuple(registrations) for episode_id, registrations in assessment.content_groups}


def _context_groups(assessment):
    return tuple(
        (tuple((name, value) for name, value in key), tuple(registrations))
        for key, registrations in assessment.context_groups
    )


def _manual_historical(source: HistoricalMemoryEpisode) -> HistoricalMemoryEpisode:
    return HistoricalMemoryEpisode(
        episode=ObservationalMemoryEpisode(**asdict(source.episode)),
        registration_id=source.registration_id,
        authority_id=source.authority_id,
        contract_id=source.contract_id,
        record_sha256=source.record_sha256,
        receipt_sha256=source.receipt_sha256,
    )


# A — Scope must be external, immutable, content-bound and non-outcome-dependent.


def test_a0_bounded_external_scope_positive_path_is_collection_pass_with_independence_blocked(
    tmp_path: Path,
) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    assessment = _audit(scope, (memory,))
    assert assessment.verdict == "PASS"
    assert assessment.completeness_status == "PASS"
    assert assessment.independence_status == "BLOCKED"
    assert assessment.scope_id == scope.scope_id
    assert _p16().is_factory_attested_memory_collection_audit(assessment)


def test_a1_scope_is_required_separately_from_collection(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    with pytest.raises((TypeError, ValueError)):
        _p16().audit_memory_collection(None, (memory,))


def test_a2_empty_question_is_rejected() -> None:
    with pytest.raises((TypeError, ValueError)):
        _p16().create_audit_scope(
            question="",
            expected_registration_ids=None,
            context_fields=("context_id",),
        )


def test_a3_duplicate_expected_registration_ids_are_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    with pytest.raises((TypeError, ValueError)):
        _p16().create_audit_scope(
            question="bounded",
            expected_registration_ids=(memory.registration_id, memory.registration_id),
            context_fields=("context_id",),
        )


@pytest.mark.parametrize("field", ["outcome", "result_id", "action_id", "decision_id", "episode_id", "registration_id", "unknown"])
def test_a4_forbidden_or_unknown_context_field_is_rejected(field: str) -> None:
    assert field not in ALLOWED_CONTEXT_FIELDS
    with pytest.raises((TypeError, ValueError)):
        _p16().create_audit_scope(
            question="context grouping",
            expected_registration_ids=None,
            context_fields=(field,),
        )


def test_a5_scope_identity_is_content_bound(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    one = _scope((memory,), question="Q1")
    same = _scope((memory,), question="Q1")
    changed = _scope((memory,), question="Q2")
    assert one.scope_id == same.scope_id
    assert one.scope_id != changed.scope_id

    forged = replace(one, question="Q2")
    assert forged.scope_id == one.scope_id
    with pytest.raises((TypeError, ValueError)):
        _audit(forged, (memory,))


def test_a6_scope_is_frozen_and_uses_tuples(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    assert isinstance(scope.context_fields, tuple)
    assert isinstance(scope.expected_registration_ids, tuple)
    with pytest.raises((AttributeError, TypeError)):
        scope.question = "MUTATED"


def test_a7_audit_api_cannot_derive_or_override_scope_from_collection() -> None:
    signature = inspect.signature(_p16().audit_memory_collection)
    assert set(signature.parameters) == {"scope", "memories"}


# B — Every member must be an exact currently-attested P1.5 historical memory.


def test_b0_exact_p15_historical_memory_is_accepted(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assert is_factory_attested_historical_memory(memory)
    assessment = _audit(_scope((memory,)), (memory,))
    assert assessment.examined_registration_ids == (memory.registration_id,)


def test_b1_manual_same_valued_historical_memory_is_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    forged = _manual_historical(memory)
    assert forged == memory and forged is not memory
    with pytest.raises((TypeError, ValueError)):
        _audit(_scope((memory,)), (forged,))


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_b2_copy_or_deepcopy_historical_memory_is_rejected(tmp_path: Path, copier) -> None:
    memory = _historical(tmp_path / "one")
    copied = copier(memory)
    assert copied == memory and copied is not memory
    with pytest.raises((TypeError, ValueError)):
        _audit(_scope((memory,)), (copied,))


def test_b2_replace_historical_memory_is_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    copied = replace(memory, registration_id=memory.registration_id)
    assert copied == memory and copied is not memory
    with pytest.raises((TypeError, ValueError)):
        _audit(_scope((memory,)), (copied,))


def test_b3_dict_or_json_like_member_is_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    with pytest.raises((TypeError, ValueError)):
        _audit(scope, (asdict(memory),))


def test_b4_raw_p14_episode_is_rejected(tmp_path: Path) -> None:
    episode = _p14_episode()
    memory = _historical_from_episode(tmp_path / "one", episode)
    with pytest.raises((TypeError, ValueError)):
        _audit(_scope((memory,)), (episode,))


@pytest.mark.parametrize("selector", ["registration_id", "episode_id"])
def test_b5_ids_alone_are_rejected_as_members(tmp_path: Path, selector: str) -> None:
    memory = _historical(tmp_path / "one")
    value = memory.registration_id if selector == "registration_id" else memory.episode.episode_id
    with pytest.raises((TypeError, ValueError)):
        _audit(_scope((memory,)), (value,))


def test_b6_mutated_now_unattested_historical_memory_is_rejected(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    object.__setattr__(memory, "authority_id", "MUTATED")
    assert not is_factory_attested_historical_memory(memory)
    scope = _p16().create_audit_scope(
        question="mutated member",
        expected_registration_ids=None,
        context_fields=("context_id",),
    )
    with pytest.raises((TypeError, ValueError)):
        _audit(scope, (memory,))


# C — Duplicates and content groups must not inflate evidence or independence.


def test_c0_same_exact_registration_repeated_is_fail_and_counted_once(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory, memory))
    assert assessment.verdict == "FAIL"
    assert assessment.examined_registration_ids == (memory.registration_id,)
    assert assessment.duplicate_registration_ids == (memory.registration_id,)


def test_c1_two_local_reattestations_of_same_registration_are_duplicates(tmp_path: Path) -> None:
    episode = _p14_episode()
    capture = persist_witnessed_memory_episode(tmp_path / "capture", episode, authority_id=AUTHORITY_ID)

    def reattest():
        return reattest_persisted_memory_episode(
            capture.record_path,
            capture.receipt_path,
            expected_contract_id="P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1",
            expected_authority_id=AUTHORITY_ID,
            expected_receipt_sha256=capture.receipt_sha256,
        )

    first = reattest()
    second = reattest()
    assert first is not second and first.registration_id == second.registration_id
    assessment = _audit(_scope((first,)), (first, second))
    assert assessment.verdict == "FAIL"
    assert assessment.duplicate_registration_ids == (first.registration_id,)
    assert assessment.examined_registration_ids == (first.registration_id,)


def test_c2_two_registrations_same_content_form_one_content_group_not_replications(tmp_path: Path) -> None:
    episode = _p14_episode()
    first = _historical_from_episode(tmp_path / "first", episode)
    second = _historical_from_episode(tmp_path / "second", episode)
    assert first.registration_id != second.registration_id
    assert first.episode.episode_id == second.episode.episode_id
    assessment = _audit(_scope((first, second)), (first, second))
    groups = _content_group_map(assessment)
    assert groups[first.episode.episode_id] == tuple(sorted((first.registration_id, second.registration_id)))
    assert assessment.independence_status == "BLOCKED"
    assert not hasattr(assessment, "independent_count")


def test_c3_different_episode_ids_still_do_not_prove_independence(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="ONE")
    second = _historical(tmp_path / "second", outcome="TWO")
    assert first.episode.episode_id != second.episode.episode_id
    assessment = _audit(_scope((first, second)), (first, second))
    assert assessment.independence_status == "BLOCKED"
    assert len(assessment.unique_episode_ids) == 2


def test_c4_content_groups_and_audit_identity_are_input_order_invariant(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="ONE")
    second = _historical(tmp_path / "second", outcome="TWO")
    scope = _scope((first, second))
    forward = _audit(scope, (first, second))
    reverse = _audit(scope, (second, first))
    assert forward.content_groups == reverse.content_groups
    assert forward.audit_id == reverse.audit_id
    assert forward == reverse


# D — Membership and completeness are relative to the externally declared universe.


def test_d0_exact_bounded_membership_has_completeness_pass(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    assessment = _audit(_scope((first, second)), (first, second))
    assert assessment.completeness_status == "PASS"
    assert assessment.missing_registration_ids == ()
    assert assessment.unexpected_registration_ids == ()
    assert assessment.verdict == "PASS"


def test_d1_missing_expected_member_is_fail(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    assessment = _audit(_scope((first, second)), (first,))
    assert assessment.completeness_status == "FAIL"
    assert assessment.verdict == "FAIL"
    assert assessment.missing_registration_ids == (second.registration_id,)


def test_d2_unexpected_member_in_bounded_scope_is_fail(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first")
    second = _historical(tmp_path / "second", outcome="SECOND")
    assessment = _audit(_scope((first,)), (first, second))
    assert assessment.completeness_status == "FAIL"
    assert assessment.verdict == "FAIL"
    assert assessment.unexpected_registration_ids == (second.registration_id,)


def test_d3_unknown_universe_is_completeness_blocked_and_overall_blocked(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,), bounded=False), (memory,))
    assert assessment.completeness_status == "BLOCKED"
    assert assessment.verdict == "BLOCKED"
    assert assessment.independence_status == "BLOCKED"


def test_d4_all_favorable_memories_with_unknown_universe_remain_blocked(tmp_path: Path) -> None:
    memories = tuple(_historical(tmp_path / f"m{i}", outcome="SUCCESS") for i in range(3))
    assessment = _audit(_scope(memories, bounded=False), memories)
    assert assessment.verdict == "BLOCKED"
    assert assessment.completeness_status == "BLOCKED"
    assert not hasattr(assessment, "supported")


# E — Context groups are controlled only by predeclared admissible dimensions.


def test_e0_different_declared_decision_contexts_form_distinct_groups(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", decision_payload="HOLD")
    second = _historical(tmp_path / "second", decision_payload="EXIT")
    scope = _scope((first, second), context_fields=("decision",))
    assessment = _audit(scope, (first, second))
    groups = _context_groups(assessment)
    assert len(groups) == 2
    keys = {key for key, _ in groups}
    assert (("decision", "HOLD"),) in keys
    assert (("decision", "EXIT"),) in keys


def test_e1_grouping_uses_only_declared_context_fields(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", decision_payload="HOLD", outcome="ONE")
    second = _historical(tmp_path / "second", decision_payload="EXIT", outcome="TWO")
    scope = _scope((first, second), context_fields=("context_id",))
    assessment = _audit(scope, (first, second))
    assert len(assessment.context_groups) == 1


def test_e2_context_groups_are_input_order_invariant(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", decision_payload="HOLD")
    second = _historical(tmp_path / "second", decision_payload="EXIT")
    scope = _scope((first, second), context_fields=("decision", "behavior"))
    assert _audit(scope, (first, second)).context_groups == _audit(scope, (second, first)).context_groups


def test_e3_outcome_cannot_be_used_to_create_post_hoc_context_groups() -> None:
    with pytest.raises((TypeError, ValueError)):
        _p16().create_audit_scope(
            question="forbidden outcome grouping",
            expected_registration_ids=None,
            context_fields=("outcome",),
        )


# F — Contradictions are preserved descriptively; majority never erases them.


def test_f0_same_context_decision_behavior_with_different_outcomes_is_contradiction(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="WIN")
    second = _historical(tmp_path / "second", outcome="LOSS")
    scope = _scope((first, second), context_fields=("context_id",))
    assessment = _audit(scope, (first, second))
    assert tuple(sorted((first.registration_id, second.registration_id))) in assessment.contradiction_groups


def test_f1_majority_does_not_erase_minority_contradiction(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="WIN")
    second = _historical(tmp_path / "second", outcome="WIN")
    third = _historical(tmp_path / "third", outcome="LOSS")
    scope = _scope((first, second, third), context_fields=("context_id",))
    assessment = _audit(scope, (first, second, third))
    expected = tuple(sorted((first.registration_id, second.registration_id, third.registration_id)))
    assert expected in assessment.contradiction_groups


def test_f2_different_declared_context_groups_are_not_merged_into_contradiction(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", decision_payload="HOLD", outcome="WIN")
    second = _historical(tmp_path / "second", decision_payload="EXIT", outcome="LOSS")
    scope = _scope((first, second), context_fields=("decision",))
    assessment = _audit(scope, (first, second))
    assert assessment.contradiction_groups == ()


def test_f3_contradiction_does_not_create_cause_or_knowledge_fields(tmp_path: Path) -> None:
    first = _historical(tmp_path / "first", outcome="WIN")
    second = _historical(tmp_path / "second", outcome="LOSS")
    assessment = _audit(_scope((first, second), context_fields=("context_id",)), (first, second))
    for name in ("cause", "causal", "knowledge", "confidence", "supported", "refuted"):
        assert not hasattr(assessment, name)


# G — Audit output never promotes observations into epistemic or operational authority.


def test_g0_assessment_has_no_epistemic_or_revision_surface(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    forbidden = (
        "supported",
        "refuted",
        "knowledge",
        "validated_knowledge",
        "confidence",
        "probability",
        "causal",
        "recommended_rule",
        "recommendation",
        "revision",
        "authorized",
        "authorization",
        "independent_count",
    )
    assert all(not hasattr(assessment, name) for name in forbidden)


def test_g1_assessment_is_not_research_evidence_or_findings(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    assert not isinstance(assessment, ResearchRunEvidence)
    assert not isinstance(assessment, ResearchFindings)


def test_g2_independence_is_always_blocked_even_for_many_distinct_contents(tmp_path: Path) -> None:
    memories = tuple(_historical(tmp_path / f"m{i}", outcome=f"O{i}") for i in range(4))
    assessment = _audit(_scope(memories), memories)
    assert len(assessment.unique_episode_ids) == 4
    assert assessment.independence_status == "BLOCKED"


def test_g3_source_contains_no_authorized_or_operational_promotion_surface() -> None:
    source = inspect.getsource(_p16())
    forbidden = (
        "AUTHORIZED",
        "order_send",
        "MetaTrader5",
        "mt5.",
        "create_order(",
        "submit_order(",
        "execute_action(",
        "run_backtest(",
        "activate_live(",
        "lot_size",
        "position_size",
        "stop_loss",
        "take_profit",
    )
    assert all(token not in source for token in forbidden)


# H — Temporal restraint, output identity and reverse-authority resistance.


def test_h0_scope_and_assessment_have_no_implicit_time_fields(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    assessment = _audit(scope, (memory,))
    forbidden = ("known_from", "registered_at", "valid_from", "decision_at", "usable_from", "audit_time")
    for value in (scope, assessment):
        assert all(not hasattr(value, name) for name in forbidden)


def test_h1_runtime_uses_no_local_clock_to_repair_missing_time() -> None:
    source = inspect.getsource(_p16())
    forbidden = ("datetime.now", "datetime.utcnow", "time.time", "registered_at =", "known_from =")
    assert all(token not in source for token in forbidden)


def _manual_assessment(source):
    return _p16().MemoryCollectionAuditAssessment(**asdict(source))


def test_h2_manual_same_valued_assessment_is_not_factory_attested(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    forged = _manual_assessment(assessment)
    assert forged == assessment and forged is not assessment
    assert not _p16().is_factory_attested_memory_collection_audit(forged)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_h3_copy_or_deepcopy_assessment_is_not_factory_attested(tmp_path: Path, copier) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    copied = copier(assessment)
    assert copied == assessment and copied is not assessment
    assert not _p16().is_factory_attested_memory_collection_audit(copied)


def test_h3_replace_assessment_is_not_factory_attested(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    copied = replace(assessment, audit_id=assessment.audit_id)
    assert copied == assessment and copied is not assessment
    assert not _p16().is_factory_attested_memory_collection_audit(copied)


def test_h4_mutation_invalidates_assessment_attestation(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    assessment = _audit(_scope((memory,)), (memory,))
    object.__setattr__(assessment, "verdict", "MUTATED")
    assert not _p16().is_factory_attested_memory_collection_audit(assessment)


def test_h5_audit_cannot_repair_or_reattest_invalid_p15_member(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    object.__setattr__(memory, "authority_id", "MUTATED")
    assert not is_factory_attested_historical_memory(memory)
    scope = _p16().create_audit_scope(
        question="cannot repair upstream",
        expected_registration_ids=None,
        context_fields=("context_id",),
    )
    with pytest.raises((TypeError, ValueError)):
        _audit(scope, (memory,))
    assert not is_factory_attested_historical_memory(memory)


def test_h6_audit_api_has_no_raw_record_receipt_or_id_reconstruction_inputs() -> None:
    signature = inspect.signature(_p16().audit_memory_collection)
    assert set(signature.parameters) == {"scope", "memories"}


def test_h7_output_membership_is_derived_from_exact_objects_not_caller_ids(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "one")
    scope = _scope((memory,))
    with pytest.raises((TypeError, ValueError)):
        _audit(scope, (memory.registration_id,))
