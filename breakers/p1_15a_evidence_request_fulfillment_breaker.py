from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
import weakref
import gc
from dataclasses import asdict, fields, replace
from pathlib import Path

import pytest

from src.action_result_evidence import engage_qualification_action, observe_qualification_result
from src.decision import produce_decision
from src.decision_trace import produce_decision_trace
from src.declared_evidence_criteria_assessment import assess_declared_evidence_criteria
from src.evidence_assessment_criteria import declare_evidence_assessment_criteria
from src.evidence_material_binding import bind_evidence_material
from src.evidence_semantic_completeness_review import (
    SemanticRequirementReview,
    submit_evidence_semantic_completeness_review,
)
from src.evidence_submission import submit_evidence
from src.follow_up_request import produce_follow_up_request
from src.memory_audit import audit_memory_collection, create_audit_scope
from src.memory_episode import produce_observational_memory_episode
from src.memory_interprocess import (
    HistoricalMemoryEpisode,
    persist_witnessed_memory_episode,
    reattest_persisted_memory_episode,
)
from src.reviewer_method_authority import (
    CONTRACT as P114A_CONTRACT,
    RECORD_SCHEMA as P114A_RECORD_SCHEMA,
    RECEIPT_SCHEMA as P114A_RECEIPT_SCHEMA,
    ReviewerMethodAuthorityQualification,
    reattest_reviewer_method_authority,
)
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P115A_CONTRACT = "P1_15A_EVIDENCE_REQUEST_FULFILLMENT_DECISION_BOUNDARY_V1"
P113A_CONTRACT = "P1_13A_EVIDENCE_SEMANTIC_COMPLETENESS_REVIEW_SUBMISSION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
MEMORY_AUTHORITY = "P1_15A_TEST_CAPTURE_AUTHORITY_V1"
REVIEW_AUTHORITY = "review-authority:p1.15a"
NONCE = "ef" * 32


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p115a():
    try:
        module = importlib.import_module("src.evidence_request_fulfillment")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.15A candidate absent — expected pre-implementation FAIL: "
            "src.evidence_request_fulfillment does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "EvidenceRequestFulfillmentDecision",
        "decide_evidence_request_fulfillment",
        "is_factory_attested_evidence_request_fulfillment_decision",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.15A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P115A_CONTRACT
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _p115a()


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


def _review(tmp_path: Path, *, review_verdict: str):
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question=f"Which evidence fulfillment decision is valid for {review_verdict}?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    audit = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        audit,
        scope,
        "REQUEST_NEW_EVIDENCE",
        f"Resolve exact evidence request for {review_verdict}.",
    )
    request = produce_follow_up_request(revision)
    criteria = declare_evidence_assessment_criteria(
        request,
        minimum_distinct_materials=1,
        require_nonempty_content=True,
        allowed_media_types=("application/pdf",),
        allowed_source_refs=("urn:test:evidence",),
        semantic_requirements=("verify authenticity",),
    )
    submission = submit_evidence(
        request,
        source_ref="urn:test:evidence",
        media_type="application/pdf",
        content=b"A",
    )
    material = bind_evidence_material(submission, content=b"A")
    assessment = assess_declared_evidence_criteria(criteria, (material,))

    if review_verdict not in {"PASS", "FAIL", "BLOCKED"}:
        raise ValueError("unsupported review_verdict fixture")

    semantic = SemanticRequirementReview(
        requirement="verify authenticity",
        status=review_verdict,
        rationale=f"Semantic review submitted as {review_verdict}.",
        material_binding_ids=(material.evidence_binding_id,),
    )

    reviewed_completeness = "PASS"
    if review_verdict == "BLOCKED":
        reviewed_completeness = "PASS"

    review = submit_evidence_semantic_completeness_review(
        assessment,
        criteria,
        (material,),
        reviewer_id="reviewer:p1.15a",
        method_ref="method:p1.15a",
        semantic_reviews=(semantic,),
        reviewed_criteria_completeness_status=reviewed_completeness,
        criteria_completeness_rationale="Completeness explicitly reviewed.",
    )
    assert review.review_verdict == review_verdict
    return review


def _qualification_id(review, record_sha256: str) -> str:
    payload = {
        "contract_id": P114A_CONTRACT,
        "authority_id": REVIEW_AUTHORITY,
        "qualification_nonce": NONCE,
        "review_id": review.review_id,
        "reviewer_id": review.reviewer_id,
        "method_ref": review.method_ref,
        "record_sha256": record_sha256,
    }
    return "RMAQ-" + _sha256(_canonical(payload))[:32]


def _authority_files(tmp_path: Path, review):
    record = {
        "schema": P114A_RECORD_SCHEMA,
        "contract_id": P114A_CONTRACT,
        "review_contract_id": P113A_CONTRACT,
        "review_id": review.review_id,
        "assessment_id": review.assessment_id,
        "criteria_id": review.criteria_id,
        "request_id": review.request_id,
        "revision_id": review.revision_id,
        "audit_id": review.audit_id,
        "scope_id": review.scope_id,
        "reviewer_id": review.reviewer_id,
        "method_ref": review.method_ref,
    }
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)
    receipt = {
        "schema": P114A_RECEIPT_SCHEMA,
        "contract_id": P114A_CONTRACT,
        "authority_id": REVIEW_AUTHORITY,
        "qualification_nonce": NONCE,
        "review_id": review.review_id,
        "reviewer_id": review.reviewer_id,
        "method_ref": review.method_ref,
        "record_sha256": record_sha256,
        "qualification_id": _qualification_id(review, record_sha256),
    }
    receipt_bytes = _canonical(receipt)

    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "authority.record.json"
    receipt_path = tmp_path / "authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


def _qualification(tmp_path: Path, *, review_verdict: str = "PASS"):
    review = _review(tmp_path / "review", review_verdict=review_verdict)
    record_path, receipt_path, pin = _authority_files(tmp_path / "authority", review)
    return reattest_reviewer_method_authority(
        review,
        record_path,
        receipt_path,
        expected_authority_id=REVIEW_AUTHORITY,
        expected_receipt_sha256=pin,
    )


def test_a0_exact_authority_positive(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    assert result.qualification_id == qualification.qualification_id
    assert result.request_id == qualification.request_id
    assert _p115a().is_factory_attested_evidence_request_fulfillment_decision(result)


def test_a1_non_authoritative_inputs_rejected(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    variants = (
        qualification.qualification_id,
        asdict(qualification),
        ReviewerMethodAuthorityQualification(**asdict(qualification)),
        copy.copy(qualification),
        copy.deepcopy(qualification),
        replace(qualification, qualification_id=qualification.qualification_id),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _p115a().decide_evidence_request_fulfillment(value)


def test_a2_mutated_upstream_rejected_and_sticky(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    original = qualification.review_authority_status
    object.__setattr__(qualification, "review_authority_status", "BLOCKED")
    with pytest.raises((TypeError, ValueError)):
        _p115a().decide_evidence_request_fulfillment(qualification)
    object.__setattr__(qualification, "review_authority_status", original)
    with pytest.raises((TypeError, ValueError)):
        _p115a().decide_evidence_request_fulfillment(qualification)


def test_b0_signature_has_no_override_surface() -> None:
    sig = inspect.signature(_p115a().decide_evidence_request_fulfillment)
    assert tuple(sig.parameters) == ("authority_qualification",)
    assert sig.parameters["authority_qualification"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert sig.parameters["authority_qualification"].default is inspect.Parameter.empty


@pytest.mark.parametrize(
    "review_verdict,expected",
    [
        ("PASS", "PASS"),
        ("FAIL", "FAIL"),
        ("BLOCKED", "BLOCKED"),
    ],
)
def test_c0_review_verdict_maps_deterministically(
    tmp_path: Path,
    review_verdict: str,
    expected: str,
) -> None:
    qualification = _qualification(tmp_path, review_verdict=review_verdict)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    assert result.review_verdict == review_verdict
    assert result.review_authority_status == "PASS"
    assert result.request_fulfillment_status == expected


def test_c1_upstream_authority_status_must_be_exact_pass(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    object.__setattr__(qualification, "review_authority_status", "FAIL")
    with pytest.raises((TypeError, ValueError)):
        _p115a().decide_evidence_request_fulfillment(qualification)


@pytest.mark.parametrize(
    "field",
    ["source_verdict", "source_completeness_status", "source_independence_status"],
)
def test_c2_source_provenance_mutation_rejected(tmp_path: Path, field: str) -> None:
    qualification = _qualification(tmp_path)
    object.__setattr__(qualification, field, "MUTATED")
    with pytest.raises((TypeError, ValueError)):
        _p115a().decide_evidence_request_fulfillment(qualification)


def test_d0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p115a().EvidenceRequestFulfillmentDecision)) == (
        "fulfillment_decision_id",
        "qualification_id",
        "review_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "criteria_id",
        "reviewer_id",
        "method_ref",
        "authority_id",
        "review_verdict",
        "review_authority_status",
        "request_fulfillment_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_d1_output_is_exact_snapshot(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    assert result.qualification_id == qualification.qualification_id
    assert result.review_id == qualification.review_id
    assert result.request_id == qualification.request_id
    assert result.revision_id == qualification.revision_id
    assert result.audit_id == qualification.audit_id
    assert result.scope_id == qualification.scope_id
    assert result.criteria_id == qualification.criteria_id
    assert result.reviewer_id == qualification.reviewer_id
    assert result.method_ref == qualification.method_ref
    assert result.authority_id == qualification.authority_id
    assert result.source_verdict == qualification.source_verdict
    assert result.source_completeness_status == qualification.source_completeness_status
    assert result.source_independence_status == qualification.source_independence_status


def test_e0_same_input_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    first = _p115a().decide_evidence_request_fulfillment(qualification)
    second = _p115a().decide_evidence_request_fulfillment(qualification)
    assert first == second and first is not second
    assert first.fulfillment_decision_id.startswith("ERF-")
    assert first.fulfillment_decision_id == second.fulfillment_decision_id
    assert _p115a().is_factory_attested_evidence_request_fulfillment_decision(first)
    assert _p115a().is_factory_attested_evidence_request_fulfillment_decision(second)


def test_e1_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    cls = _p115a().EvidenceRequestFulfillmentDecision
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(cls(**asdict(result)))
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(copy.copy(result))
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(copy.deepcopy(result))
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(
        replace(result, fulfillment_decision_id=result.fulfillment_decision_id)
    )


def test_e2_mutation_then_restore_sticky_invalid(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    original = result.request_fulfillment_status
    object.__setattr__(result, "request_fulfillment_status", "MUTATED")
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(result)
    object.__setattr__(result, "request_fulfillment_status", original)
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(result)


def test_e3_upstream_qualification_can_be_collected(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    ref = weakref.ref(qualification)
    del qualification
    gc.collect()
    assert ref() is None
    assert _p115a().is_factory_attested_evidence_request_fulfillment_decision(result)


def test_f0_no_reverse_promotion_or_operational_surface() -> None:
    module = _p115a()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "promote_to_knowledge",
        "create_knowledge",
        "authorize",
        "activate_live",
        "run_backtest",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
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


def test_f1_decision_id_alone_is_not_attestation(tmp_path: Path) -> None:
    qualification = _qualification(tmp_path)
    result = _p115a().decide_evidence_request_fulfillment(qualification)
    assert not _p115a().is_factory_attested_evidence_request_fulfillment_decision(
        result.fulfillment_decision_id
    )
