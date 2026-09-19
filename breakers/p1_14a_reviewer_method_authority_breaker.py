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
from src.declared_evidence_criteria_assessment import assess_declared_evidence_criteria
from src.evidence_assessment_criteria import declare_evidence_assessment_criteria
from src.evidence_material_binding import bind_evidence_material
from src.evidence_semantic_completeness_review import (
    EvidenceSemanticCompletenessReview,
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
from src.revision import produce_revision_decision
from tests.research_runtime_fixture import synthetic_runtime_case


P114A_CONTRACT = "P1_14A_REVIEWER_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1"
P114A_RECORD_SCHEMA = "P1_14A_REVIEWER_METHOD_AUTHORITY_RECORD_V1"
P114A_RECEIPT_SCHEMA = "P1_14A_REVIEWER_METHOD_AUTHORITY_RECEIPT_V1"
P113A_CONTRACT = "P1_13A_EVIDENCE_SEMANTIC_COMPLETENESS_REVIEW_SUBMISSION_BOUNDARY_V1"
P15_CONTRACT = "P1_5_WITNESSED_DURABLE_MEMORY_REATTESTATION_V1"
MEMORY_AUTHORITY = "P1_14A_TEST_CAPTURE_AUTHORITY_V1"
REVIEW_AUTHORITY = "review-authority:test"
NONCE = "ab" * 32


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _p114a():
    try:
        module = importlib.import_module("src.reviewer_method_authority")
    except ModuleNotFoundError as exc:
        pytest.fail(
            "P1.14A candidate absent — expected pre-implementation FAIL: "
            "src.reviewer_method_authority does not exist",
            pytrace=False,
        )
        raise AssertionError from exc
    required = (
        "ReviewerMethodAuthorityQualification",
        "reattest_reviewer_method_authority",
        "is_factory_attested_reviewer_method_authority_qualification",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"P1.14A candidate surface incomplete: {missing}", pytrace=False)
    assert getattr(module, "CONTRACT", None) == P114A_CONTRACT
    assert getattr(module, "RECORD_SCHEMA", None) == P114A_RECORD_SCHEMA
    assert getattr(module, "RECEIPT_SCHEMA", None) == P114A_RECEIPT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _candidate_must_exist():
    _p114a()


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


def _review_case(tmp_path: Path) -> EvidenceSemanticCompletenessReview:
    memory = _historical(tmp_path / "memory")
    scope = create_audit_scope(
        question="Which evidence review authority is required?",
        expected_registration_ids=(memory.registration_id,),
        context_fields=("context_id", "decision", "behavior"),
    )
    audit = audit_memory_collection(scope, (memory,))
    revision = produce_revision_decision(
        audit,
        scope,
        "REQUEST_NEW_EVIDENCE",
        "Review one exact evidence request.",
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
    semantic = SemanticRequirementReview(
        requirement="verify authenticity",
        status="PASS",
        rationale="Reviewed externally.",
        material_binding_ids=(material.evidence_binding_id,),
    )
    return submit_evidence_semantic_completeness_review(
        assessment,
        criteria,
        (material,),
        reviewer_id="reviewer:test",
        method_ref="method:test",
        semantic_reviews=(semantic,),
        reviewed_criteria_completeness_status="PASS",
        criteria_completeness_rationale="Declared criteria reviewed as complete.",
    )


def _qualification_id(review, record_sha256: str, *, authority_id=REVIEW_AUTHORITY, nonce=NONCE):
    payload = {
        "contract_id": P114A_CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": nonce,
        "review_id": review.review_id,
        "reviewer_id": review.reviewer_id,
        "method_ref": review.method_ref,
        "record_sha256": record_sha256,
    }
    return "RMAQ-" + _sha256(_canonical(payload))[:32]


def _authority_files(
    tmp_path: Path,
    review,
    *,
    authority_id=REVIEW_AUTHORITY,
    nonce=NONCE,
    record_mutator=None,
    receipt_mutator=None,
):
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
    if record_mutator is not None:
        record_mutator(record)
    record_bytes = _canonical(record)
    record_sha256 = _sha256(record_bytes)
    qualification_id = _qualification_id(
        review,
        record_sha256,
        authority_id=authority_id,
        nonce=nonce,
    )
    receipt = {
        "schema": P114A_RECEIPT_SCHEMA,
        "contract_id": P114A_CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": nonce,
        "review_id": review.review_id,
        "reviewer_id": review.reviewer_id,
        "method_ref": review.method_ref,
        "record_sha256": record_sha256,
        "qualification_id": qualification_id,
    }
    if receipt_mutator is not None:
        receipt_mutator(receipt)
    receipt_bytes = _canonical(receipt)
    tmp_path.mkdir(parents=True, exist_ok=True)
    record_path = tmp_path / "authority.record.json"
    receipt_path = tmp_path / "authority.receipt.json"
    record_path.write_bytes(record_bytes)
    receipt_path.write_bytes(receipt_bytes)
    return record_path, receipt_path, _sha256(receipt_bytes)


_DEFAULT_PIN = object()


def _reattest(review, paths, *, authority_id=REVIEW_AUTHORITY, pin=_DEFAULT_PIN):
    record_path, receipt_path, receipt_sha256 = paths
    return _p114a().reattest_reviewer_method_authority(
        review,
        record_path,
        receipt_path,
        expected_authority_id=authority_id,
        expected_receipt_sha256=receipt_sha256 if pin is _DEFAULT_PIN else pin,
    )


def test_a0_exact_review_positive(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    assert result.review_id == review.review_id
    assert result.reviewer_id == review.reviewer_id
    assert result.method_ref == review.method_ref
    assert _p114a().is_factory_attested_reviewer_method_authority_qualification(result)


def test_a1_non_authoritative_review_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review)
    variants = (
        review.review_id,
        asdict(review),
        EvidenceSemanticCompletenessReview(**asdict(review)),
        copy.copy(review),
        copy.deepcopy(review),
        replace(review, review_id=review.review_id),
    )
    for value in variants:
        with pytest.raises((TypeError, ValueError)):
            _reattest(value, paths)


def test_b0_signature_is_exact() -> None:
    sig = inspect.signature(_p114a().reattest_reviewer_method_authority)
    assert tuple(sig.parameters) == (
        "review",
        "record_path",
        "receipt_path",
        "expected_authority_id",
        "expected_receipt_sha256",
    )
    for name in ("review", "record_path", "receipt_path"):
        assert sig.parameters[name].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    for name in ("expected_authority_id", "expected_receipt_sha256"):
        assert sig.parameters[name].kind is inspect.Parameter.KEYWORD_ONLY
        assert sig.parameters[name].default is inspect.Parameter.empty


@pytest.mark.parametrize("bad", ["", " ", 1, None])
def test_c0_expected_authority_exact_nonempty(tmp_path: Path, bad) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review)
    with pytest.raises((TypeError, ValueError)):
        _reattest(review, paths, authority_id=bad)


@pytest.mark.parametrize("bad", ["", "0" * 63, "G" * 64, 1, None])
def test_c1_external_pin_exact_sha256(tmp_path: Path, bad) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review)
    with pytest.raises((TypeError, ValueError)):
        _reattest(review, paths, pin=bad)


def test_c2_wrong_but_well_formed_pin_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review)
    with pytest.raises(ValueError):
        _reattest(review, paths, pin="0" * 64)


def test_c3_noncanonical_record_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    record_path, receipt_path, pin = _authority_files(tmp_path / "auth", review)
    parsed = json.loads(record_path.read_text("utf-8"))
    record_path.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    with pytest.raises(ValueError):
        _reattest(review, (record_path, receipt_path, pin))


def test_c4_noncanonical_receipt_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    record_path, receipt_path, _ = _authority_files(tmp_path / "auth", review)
    parsed = json.loads(receipt_path.read_text("utf-8"))
    receipt_path.write_text(json.dumps(parsed, indent=2), encoding="utf-8")
    pin = _sha256(receipt_path.read_bytes())
    with pytest.raises(ValueError):
        _reattest(review, (record_path, receipt_path, pin))


@pytest.mark.parametrize(
    "field",
    ["review_id", "reviewer_id", "method_ref", "request_id", "scope_id", "review_contract_id"],
)
def test_d0_record_mismatch_rejected(tmp_path: Path, field: str) -> None:
    review = _review_case(tmp_path / "case")
    def mutate(record):
        record[field] = "WRONG"
    paths = _authority_files(tmp_path / "auth", review, record_mutator=mutate)
    with pytest.raises(ValueError):
        _reattest(review, paths)


def test_d1_wrong_authority_in_receipt_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review, authority_id="other-authority")
    with pytest.raises(ValueError):
        _reattest(review, paths, authority_id=REVIEW_AUTHORITY)


@pytest.mark.parametrize("nonce", ["", "ab", "z" * 64])
def test_d2_invalid_nonce_rejected(tmp_path: Path, nonce: str) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review, nonce=nonce)
    with pytest.raises(ValueError):
        _reattest(review, paths)


def test_d3_tampered_qualification_id_rejected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(
        tmp_path / "auth",
        review,
        receipt_mutator=lambda receipt: receipt.__setitem__("qualification_id", "RMAQ-" + "0" * 32),
    )
    with pytest.raises(ValueError):
        _reattest(review, paths)


def test_e0_output_fields_are_exact() -> None:
    assert tuple(field.name for field in fields(_p114a().ReviewerMethodAuthorityQualification)) == (
        "qualification_id",
        "review_id",
        "assessment_id",
        "criteria_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "reviewer_id",
        "method_ref",
        "authority_id",
        "record_sha256",
        "receipt_sha256",
        "review_verdict",
        "review_authority_status",
        "request_fulfillment_status",
        "source_verdict",
        "source_completeness_status",
        "source_independence_status",
    )


def test_e1_authority_pass_but_fulfillment_blocked(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    assert result.review_verdict == review.review_verdict
    assert result.review_authority_status == "PASS"
    assert result.request_fulfillment_status == "BLOCKED"


def test_f0_same_inputs_same_id_distinct_attested_objects(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    paths = _authority_files(tmp_path / "auth", review)
    first = _reattest(review, paths)
    second = _reattest(review, paths)
    assert first == second and first is not second
    assert first.qualification_id.startswith("RMAQ-")
    assert first.qualification_id == second.qualification_id
    assert _p114a().is_factory_attested_reviewer_method_authority_qualification(first)
    assert _p114a().is_factory_attested_reviewer_method_authority_qualification(second)


def test_f1_manual_copy_replace_not_attested(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    cls = _p114a().ReviewerMethodAuthorityQualification
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(cls(**asdict(result)))
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(copy.copy(result))
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(copy.deepcopy(result))
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(
        replace(result, qualification_id=result.qualification_id)
    )


def test_f2_mutation_then_restore_sticky_invalid(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    original = result.review_authority_status
    object.__setattr__(result, "review_authority_status", "MUTATED")
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(result)
    object.__setattr__(result, "review_authority_status", original)
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(result)


def test_f3_upstream_review_can_be_collected(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    ref = weakref.ref(review)
    del review
    gc.collect()
    assert ref() is None
    assert _p114a().is_factory_attested_reviewer_method_authority_qualification(result)


def test_g0_no_authority_producer_or_promotion_surface() -> None:
    module = _p114a()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "create_authority_record",
        "persist_authority",
        "mark_fulfilled",
        "promote_to_knowledge",
        "authorize",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "requests.",
        "socket.",
        "subprocess.",
        "order_send",
        "MetaTrader5",
        "ResearchFinding(",
        "ResearchRunEvidence(",
    )
    assert all(token not in source for token in forbidden_tokens)


def test_g1_qualification_id_alone_is_not_authority(tmp_path: Path) -> None:
    review = _review_case(tmp_path / "case")
    result = _reattest(review, _authority_files(tmp_path / "auth", review))
    assert not _p114a().is_factory_attested_reviewer_method_authority_qualification(
        result.qualification_id
    )
