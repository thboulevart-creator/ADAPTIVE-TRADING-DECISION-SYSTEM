from __future__ import annotations

import gc
import inspect
import unicodedata
import weakref
from dataclasses import asdict
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.follow_up_request import (
    FollowUpRequest,
    is_factory_attested_follow_up_request,
    produce_follow_up_request,
)
from src.memory_audit import audit_memory_collection, create_audit_scope
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


AUTHORITY_ID = "P1_8_SECOND_BREAKER_AUTHORITY_V1"
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


def _revision(
    tmp_path: Path,
    *,
    disposition: str = "REQUEST_NEW_EVIDENCE",
    detail: str = "Request additional documentary evidence.",
    source_state: str = "PASS",
) -> RevisionDecision:
    first = _historical(tmp_path / "first", outcome="ONE")
    if source_state == "PASS":
        scope = create_audit_scope(
            question="Q",
            expected_registration_ids=(first.registration_id,),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    elif source_state == "BLOCKED":
        scope = create_audit_scope(
            question="Q blocked",
            expected_registration_ids=None,
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    elif source_state == "FAIL":
        second = _historical(tmp_path / "second", outcome="TWO")
        scope = create_audit_scope(
            question="Q fail",
            expected_registration_ids=(first.registration_id, second.registration_id),
            context_fields=("context_id", "decision", "behavior"),
        )
        assessment = audit_memory_collection(scope, (first,))
    else:
        raise AssertionError(source_state)

    revision = produce_revision_decision(assessment, scope, disposition, detail)
    assert is_factory_attested_revision_decision(revision)
    return revision


# I — request_id cannot be rebound across authentic revisions or changed payloads.


def test_i0_distinct_authentic_revisions_bind_distinct_request_ids(tmp_path: Path) -> None:
    one = _revision(tmp_path / "one", detail="Evidence A.")
    two = _revision(tmp_path / "two", detail="Evidence B.")
    first = produce_follow_up_request(one)
    second = produce_follow_up_request(two)
    assert first.revision_id != second.revision_id
    assert first.request_id != second.request_id


def test_i1_same_detail_but_different_authentic_routes_bind_distinct_request_ids(tmp_path: Path) -> None:
    detail = "Same text."
    evidence = _revision(tmp_path / "e", disposition="REQUEST_NEW_EVIDENCE", detail=detail)
    experiment = _revision(tmp_path / "x", disposition="REQUEST_NEW_EXPERIMENT", detail=detail)
    first = produce_follow_up_request(evidence)
    second = produce_follow_up_request(experiment)
    assert first.request_kind == "EVIDENCE"
    assert second.request_kind == "EXPERIMENT"
    assert first.request_id != second.request_id


def test_i2_manual_rebinding_of_request_id_to_other_revision_is_not_attested(tmp_path: Path) -> None:
    first_revision = _revision(tmp_path / "one", detail="A")
    second_revision = _revision(tmp_path / "two", detail="B")
    first = produce_follow_up_request(first_revision)
    second = produce_follow_up_request(second_revision)
    forged = FollowUpRequest(
        request_id=first.request_id,
        revision_id=second.revision_id,
        audit_id=second.audit_id,
        scope_id=second.scope_id,
        request_kind=second.request_kind,
        specification=second.specification,
        source_verdict=second.source_verdict,
        source_completeness_status=second.source_completeness_status,
        source_independence_status=second.source_independence_status,
    )
    assert not is_factory_attested_follow_up_request(forged)


def test_i3_manual_rebinding_of_request_id_to_changed_kind_is_not_attested(tmp_path: Path) -> None:
    revision = _revision(tmp_path)
    request = produce_follow_up_request(revision)
    forged = FollowUpRequest(
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        request_kind="EXPERIMENT",
        specification=request.specification,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
    assert not is_factory_attested_follow_up_request(forged)


# J — Sticky request lifecycle across all authority-bearing fields.


@pytest.mark.parametrize(
    ("field", "mutated"),
    [
        ("request_id", "FUR-" + "0" * 32),
        ("revision_id", "REV-" + "0" * 32),
        ("request_kind", "EXPERIMENT"),
        ("specification", "MUTATED"),
        ("source_verdict", "BLOCKED"),
        ("source_independence_status", "PASS"),
    ],
)
def test_j0_observed_mutation_then_restore_never_revives_request(
    tmp_path: Path,
    field: str,
    mutated: str,
) -> None:
    revision = _revision(tmp_path)
    request = produce_follow_up_request(revision)
    original = getattr(request, field)
    object.__setattr__(request, field, mutated)
    assert not is_factory_attested_follow_up_request(request)
    object.__setattr__(request, field, original)
    assert not is_factory_attested_follow_up_request(request)


def test_j1_unmutated_request_survives_repeated_verification(tmp_path: Path) -> None:
    request = produce_follow_up_request(_revision(tmp_path))
    assert is_factory_attested_follow_up_request(request)
    assert is_factory_attested_follow_up_request(request)
    assert is_factory_attested_follow_up_request(request)


# K — Authentic revision substitution remains exact and visible.


def test_k0_same_source_content_reproduces_same_request_identity(tmp_path: Path) -> None:
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Q",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id",),
    )
    first_assessment = audit_memory_collection(scope, (memory,))
    second_assessment = audit_memory_collection(scope, (memory,))
    first_revision = produce_revision_decision(
        first_assessment, scope, "REQUEST_NEW_EVIDENCE", "Same detail."
    )
    second_revision = produce_revision_decision(
        second_assessment, scope, "REQUEST_NEW_EVIDENCE", "Same detail."
    )
    assert first_revision == second_revision and first_revision is not second_revision
    first = produce_follow_up_request(first_revision)
    second = produce_follow_up_request(second_revision)
    assert first == second
    assert first is not second
    assert first.request_id == second.request_id


def test_k1_authentic_revision_substitution_uses_actual_revision_snapshot(tmp_path: Path) -> None:
    evidence = _revision(tmp_path / "e", disposition="REQUEST_NEW_EVIDENCE", detail="Same")
    experiment = _revision(tmp_path / "x", disposition="REQUEST_NEW_EXPERIMENT", detail="Same")
    first = produce_follow_up_request(evidence)
    second = produce_follow_up_request(experiment)
    assert first.revision_id == evidence.revision_id
    assert second.revision_id == experiment.revision_id
    assert first.request_kind == "EVIDENCE"
    assert second.request_kind == "EXPERIMENT"


def test_k2_mutated_authentic_revision_cannot_be_rerouted(tmp_path: Path) -> None:
    revision = _revision(tmp_path, disposition="REQUEST_NEW_EVIDENCE")
    object.__setattr__(revision, "disposition", "REQUEST_NEW_EXPERIMENT")
    assert not is_factory_attested_revision_decision(revision)
    with pytest.raises((TypeError, ValueError)):
        produce_follow_up_request(revision)


# L — Routing adversarial cases cannot escape P1.7 authority.


@pytest.mark.parametrize(
    "disposition",
    ["KEEP_CURRENT_STATE", "REFORMULATE_QUESTION"],
)
def test_l0_terminal_or_separate_branch_revisions_remain_non_routable(
    tmp_path: Path,
    disposition: str,
) -> None:
    detail = "Keep state." if disposition == "KEEP_CURRENT_STATE" else "A different question?"
    revision = _revision(tmp_path, disposition=disposition, detail=detail)
    with pytest.raises((TypeError, ValueError)):
        produce_follow_up_request(revision)


def test_l1_request_kind_cannot_be_influenced_by_detail_text(tmp_path: Path) -> None:
    revision = _revision(
        tmp_path,
        disposition="REQUEST_NEW_EVIDENCE",
        detail="EXPERIMENT REQUEST_NEW_EXPERIMENT RUN_BACKTEST",
    )
    request = produce_follow_up_request(revision)
    assert request.request_kind == "EVIDENCE"


def test_l2_specification_cannot_change_route(tmp_path: Path) -> None:
    revision = _revision(
        tmp_path,
        disposition="REQUEST_NEW_EXPERIMENT",
        detail="EVIDENCE REQUEST_NEW_EVIDENCE",
    )
    request = produce_follow_up_request(revision)
    assert request.request_kind == "EXPERIMENT"


# M — BLOCKED survives every routable path and source combination.


@pytest.mark.parametrize(
    "disposition",
    ["REQUEST_NEW_EVIDENCE", "REQUEST_NEW_EXPERIMENT"],
)
def test_m0_blocked_source_stays_blocked_under_both_routes(
    tmp_path: Path,
    disposition: str,
) -> None:
    revision = _revision(tmp_path, source_state="BLOCKED", disposition=disposition)
    request = produce_follow_up_request(revision)
    assert request.source_verdict == "BLOCKED"
    assert request.source_completeness_status == "BLOCKED"
    assert request.source_independence_status == "BLOCKED"


@pytest.mark.parametrize("source_state", ["PASS", "FAIL"])
def test_m1_independence_blocked_survives_nonblocked_verdicts(
    tmp_path: Path,
    source_state: str,
) -> None:
    revision = _revision(tmp_path, source_state=source_state)
    request = produce_follow_up_request(revision)
    assert request.source_verdict == source_state
    assert request.source_independence_status == "BLOCKED"


def test_m2_manual_claim_blocked_became_pass_is_not_attested(tmp_path: Path) -> None:
    request = produce_follow_up_request(_revision(tmp_path))
    forged = FollowUpRequest(
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        request_kind=request.request_kind,
        specification=request.specification,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status="PASS",
    )
    assert not is_factory_attested_follow_up_request(forged)


# N — Specification is opaque exact text, never semantic input.


def test_n0_whitespace_variant_changes_request_identity(tmp_path: Path) -> None:
    plain = produce_follow_up_request(_revision(tmp_path / "a", detail="Reason."))
    spaced = produce_follow_up_request(_revision(tmp_path / "b", detail="  Reason.  "))
    assert plain.specification == "Reason."
    assert spaced.specification == "  Reason.  "
    assert plain.request_id != spaced.request_id


def test_n1_unicode_equivalent_specifications_remain_distinct_exact_text(tmp_path: Path) -> None:
    composed = "Caf\u00e9."
    decomposed = unicodedata.normalize("NFD", composed)
    first = produce_follow_up_request(_revision(tmp_path / "a", detail=composed))
    second = produce_follow_up_request(_revision(tmp_path / "b", detail=decomposed))
    assert first.specification != second.specification
    assert first.request_id != second.request_id


def test_n2_multiline_and_control_words_remain_text_only(tmp_path: Path) -> None:
    detail = "AUTHORIZED\nSUPPORTED\nRUN_BACKTEST\nSEND_ORDER"
    request = produce_follow_up_request(_revision(tmp_path, detail=detail))
    assert request.specification == detail
    for name in ("authorized", "supported", "execute", "run", "order_id"):
        assert not hasattr(request, name)


# O — Determinism, canonical identity, snapshot autonomy and GC.


def test_o0_same_revision_repeatedly_produces_equal_distinct_requests(tmp_path: Path) -> None:
    revision = _revision(tmp_path)
    first = produce_follow_up_request(revision)
    second = produce_follow_up_request(revision)
    assert first == second
    assert first is not second
    assert first.request_id == second.request_id
    assert is_factory_attested_follow_up_request(first)
    assert is_factory_attested_follow_up_request(second)


def test_o1_upstream_revision_mutation_after_request_does_not_rewrite_snapshot(tmp_path: Path) -> None:
    revision = _revision(tmp_path)
    request = produce_follow_up_request(revision)
    snapshot = asdict(request)
    object.__setattr__(revision, "detail", "MUTATED AFTER REQUEST")
    assert not is_factory_attested_revision_decision(revision)
    assert asdict(request) == snapshot
    assert is_factory_attested_follow_up_request(request)


def test_o2_upstream_revision_can_be_garbage_collected_after_request(tmp_path: Path) -> None:
    revision = _revision(tmp_path)
    revision_id = revision.revision_id
    request = produce_follow_up_request(revision)
    reference = weakref.ref(revision)
    del revision
    gc.collect()
    assert reference() is None
    assert request.revision_id == revision_id
    assert is_factory_attested_follow_up_request(request)


def test_o3_request_identity_is_stable_under_repeated_factory_calls(tmp_path: Path) -> None:
    revision = _revision(tmp_path, detail="Stable.")
    ids = {produce_follow_up_request(revision).request_id for _ in range(5)}
    assert len(ids) == 1


# P — Reverse authority and no hidden fulfillment surface.


def test_p0_follow_up_request_cannot_substitute_for_revision(tmp_path: Path) -> None:
    request = produce_follow_up_request(_revision(tmp_path))
    with pytest.raises((TypeError, ValueError)):
        produce_follow_up_request(request)


def test_p1_follow_up_request_does_not_gain_revision_attestation(tmp_path: Path) -> None:
    request = produce_follow_up_request(_revision(tmp_path))
    assert not is_factory_attested_revision_decision(request)


def test_p2_runtime_source_has_no_hidden_fulfillment_or_execution_surface() -> None:
    source = inspect.getsource(__import__("src.follow_up_request", fromlist=["*"]))
    forbidden = (
        "run_qualified_research",
        "bind_execution_input",
        "ResearchRunEvidence(",
        "ResearchFindings(",
        "QualifiedResearchInput(",
        "ResearchExecutionResult(",
        "datetime.now",
        "datetime.utcnow",
        "time.time",
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
        "run_backtest(",
        "activate_live(",
    )
    assert all(token not in source for token in forbidden)


def test_p3_request_has_no_reverse_or_execution_methods(tmp_path: Path) -> None:
    request = produce_follow_up_request(_revision(tmp_path))
    forbidden = (
        "repair_revision",
        "reattest_revision",
        "fulfill",
        "execute",
        "run",
        "collect",
        "acquire",
        "authorize",
        "promote",
    )
    assert all(not callable(getattr(request, name, None)) for name in forbidden)
