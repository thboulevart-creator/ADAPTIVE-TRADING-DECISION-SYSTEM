"""P1.13A evidence semantic/completeness review submission boundary.

This module records an explicit review over one exact P1.12A assessment,
its exact P1.11A criteria, and the exact bound materials that assessment used.
It does not interpret evidence bytes and does not establish semantic truth,
reviewer authority, request fulfillment, knowledge, or authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.declared_evidence_criteria_assessment import (
    DeclaredEvidenceCriteriaAssessment,
    is_factory_attested_declared_evidence_criteria_assessment,
)
from src.evidence_assessment_criteria import (
    EvidenceAssessmentCriteria,
    is_factory_attested_evidence_assessment_criteria,
)
from src.evidence_material_binding import (
    BoundEvidenceMaterial,
    is_factory_attested_bound_evidence_material,
)


CONTRACT = "P1_13A_EVIDENCE_SEMANTIC_COMPLETENESS_REVIEW_SUBMISSION_BOUNDARY_V1"

_REVIEW_STATUSES = {"PASS", "FAIL", "BLOCKED"}
_REVIEW_AUTHORITY_STATUS = "BLOCKED"
_REQUEST_FULFILLMENT_STATUS = "BLOCKED"


@dataclass(frozen=True, slots=True)
class SemanticRequirementReview:
    requirement: str
    status: str
    rationale: str
    material_binding_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvidenceSemanticCompletenessReview:
    review_id: str
    assessment_id: str
    criteria_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    material_binding_ids: tuple[str, ...]
    minimum_distinct_materials_status: str
    nonempty_content_status: str
    media_type_status: str
    source_ref_status: str
    semantic_reviews: tuple[SemanticRequirementReview, ...]
    reviewed_criteria_completeness_status: str
    criteria_completeness_rationale: str
    review_verdict: str
    declared_criteria_completeness_status: str
    review_authority_status: str
    request_fulfillment_status: str
    reviewer_id: str
    method_ref: str
    source_verdict: str
    source_completeness_status: str
    source_independence_status: str


def _stable_hash(value: object) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _review_id(**values: object) -> str:
    return "ESR-" + _stable_hash({"contract": CONTRACT, **values})[:32]


def _fingerprint(value: EvidenceSemanticCompletenessReview) -> str:
    return _stable_hash({"contract": CONTRACT, "review": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[EvidenceSemanticCompletenessReview], str],
    ] = {}

    def attest(**values: object) -> EvidenceSemanticCompletenessReview:
        produced = EvidenceSemanticCompletenessReview(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not EvidenceSemanticCompletenessReview:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_evidence_semantic_completeness_review, is_factory_attested_evidence_semantic_completeness_review = _build_attestation_api()
del _build_attestation_api


def _require_nonempty_exact_str(label: str, value: object) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty after strip")
    return value


def _validate_semantic_reviews(
    semantic_reviews: object,
    *,
    required_requirements: tuple[str, ...],
    material_binding_ids: tuple[str, ...],
) -> tuple[SemanticRequirementReview, ...]:
    if type(semantic_reviews) is not tuple:
        raise TypeError("semantic_reviews must be exact tuple")

    if not required_requirements:
        if semantic_reviews:
            raise ValueError("semantic_reviews must be empty when no requirements exist")
        return ()

    if len(semantic_reviews) != len(required_requirements):
        raise ValueError("semantic_reviews must cover every requirement exactly once")

    allowed_material_ids = set(material_binding_ids)
    normalized: list[SemanticRequirementReview] = []

    for expected_requirement, review in zip(required_requirements, semantic_reviews):
        if type(review) is not SemanticRequirementReview:
            raise TypeError("semantic_reviews items must be exact SemanticRequirementReview")

        requirement = _require_nonempty_exact_str("requirement", review.requirement)
        if requirement != expected_requirement:
            raise ValueError("semantic review requirements must match criteria exactly and in order")

        if type(review.status) is not str:
            raise TypeError("semantic review status must be exact str")
        if review.status not in _REVIEW_STATUSES:
            raise ValueError("invalid semantic review status")

        rationale = _require_nonempty_exact_str("semantic review rationale", review.rationale)

        if type(review.material_binding_ids) is not tuple:
            raise TypeError("semantic review material_binding_ids must be exact tuple")
        if not review.material_binding_ids:
            raise ValueError("semantic review material_binding_ids must be nonempty")

        seen: set[str] = set()
        ids: list[str] = []
        for material_id in review.material_binding_ids:
            material_id = _require_nonempty_exact_str("semantic review material_binding_id", material_id)
            if material_id in seen:
                raise ValueError("semantic review material_binding_ids must be unique")
            if material_id not in allowed_material_ids:
                raise ValueError("semantic review references unknown material")
            seen.add(material_id)
            ids.append(material_id)

        normalized.append(
            SemanticRequirementReview(
                requirement=requirement,
                status=review.status,
                rationale=rationale,
                material_binding_ids=tuple(ids),
            )
        )

    return tuple(normalized)


def submit_evidence_semantic_completeness_review(
    assessment,
    criteria,
    materials,
    *,
    reviewer_id,
    method_ref,
    semantic_reviews,
    reviewed_criteria_completeness_status,
    criteria_completeness_rationale,
) -> EvidenceSemanticCompletenessReview:
    """Record a bounded review submission without promoting it to fulfillment."""
    if type(assessment) is not DeclaredEvidenceCriteriaAssessment:
        raise TypeError("P1.13A requires exact DeclaredEvidenceCriteriaAssessment")
    if not is_factory_attested_declared_evidence_criteria_assessment(assessment):
        raise ValueError("P1.13A requires currently-attested P1.12A assessment")

    if type(criteria) is not EvidenceAssessmentCriteria:
        raise TypeError("P1.13A requires exact EvidenceAssessmentCriteria")
    if not is_factory_attested_evidence_assessment_criteria(criteria):
        raise ValueError("P1.13A requires currently-attested P1.11A criteria")

    if type(materials) is not tuple:
        raise TypeError("P1.13A materials must be exact tuple")
    if not materials:
        raise ValueError("P1.13A requires at least one material")

    expected_ids = assessment.material_binding_ids
    actual_ids: list[str] = []
    expected_provenance = (
        assessment.request_id,
        assessment.revision_id,
        assessment.audit_id,
        assessment.scope_id,
        assessment.source_verdict,
        assessment.source_completeness_status,
        assessment.source_independence_status,
    )
    for material in materials:
        if type(material) is not BoundEvidenceMaterial:
            raise TypeError("P1.13A requires exact BoundEvidenceMaterial values")
        if not is_factory_attested_bound_evidence_material(material):
            raise ValueError("P1.13A requires currently-attested P1.10A materials")
        provenance = (
            material.request_id,
            material.revision_id,
            material.audit_id,
            material.scope_id,
            material.source_verdict,
            material.source_completeness_status,
            material.source_independence_status,
        )
        if provenance != expected_provenance:
            raise ValueError("P1.13A material provenance does not match assessment")
        actual_ids.append(material.evidence_binding_id)

    if tuple(actual_ids) != expected_ids:
        raise ValueError("P1.13A material identities/order must match P1.12A assessment")

    criteria_identity = (
        criteria.criteria_id,
        criteria.request_id,
        criteria.revision_id,
        criteria.audit_id,
        criteria.scope_id,
        criteria.source_verdict,
        criteria.source_completeness_status,
        criteria.source_independence_status,
    )
    assessment_identity = (
        assessment.criteria_id,
        assessment.request_id,
        assessment.revision_id,
        assessment.audit_id,
        assessment.scope_id,
        assessment.source_verdict,
        assessment.source_completeness_status,
        assessment.source_independence_status,
    )
    if criteria_identity != assessment_identity:
        raise ValueError("P1.13A criteria provenance does not match assessment")

    if assessment.criteria_completeness_status != criteria.criteria_completeness_status:
        raise ValueError("P1.13A criteria completeness snapshot mismatch")
    if assessment.unresolved_semantic_requirements != criteria.semantic_requirements:
        raise ValueError("P1.13A semantic requirements snapshot mismatch")

    reviewer_id = _require_nonempty_exact_str("reviewer_id", reviewer_id)
    method_ref = _require_nonempty_exact_str("method_ref", method_ref)
    criteria_completeness_rationale = _require_nonempty_exact_str(
        "criteria_completeness_rationale",
        criteria_completeness_rationale,
    )

    if type(reviewed_criteria_completeness_status) is not str:
        raise TypeError("reviewed_criteria_completeness_status must be exact str")
    if reviewed_criteria_completeness_status not in _REVIEW_STATUSES:
        raise ValueError("invalid reviewed_criteria_completeness_status")

    semantic_reviews = _validate_semantic_reviews(
        semantic_reviews,
        required_requirements=criteria.semantic_requirements,
        material_binding_ids=expected_ids,
    )

    dimensions = (
        assessment.minimum_distinct_materials_status,
        assessment.nonempty_content_status,
        assessment.media_type_status,
        assessment.source_ref_status,
        *(review.status for review in semantic_reviews),
        reviewed_criteria_completeness_status,
    )
    if "FAIL" in dimensions:
        review_verdict = "FAIL"
    elif "BLOCKED" in dimensions:
        review_verdict = "BLOCKED"
    else:
        review_verdict = "PASS"

    values = {
        "assessment_id": assessment.assessment_id,
        "criteria_id": assessment.criteria_id,
        "request_id": assessment.request_id,
        "revision_id": assessment.revision_id,
        "audit_id": assessment.audit_id,
        "scope_id": assessment.scope_id,
        "material_binding_ids": assessment.material_binding_ids,
        "minimum_distinct_materials_status": assessment.minimum_distinct_materials_status,
        "nonempty_content_status": assessment.nonempty_content_status,
        "media_type_status": assessment.media_type_status,
        "source_ref_status": assessment.source_ref_status,
        "semantic_reviews": semantic_reviews,
        "reviewed_criteria_completeness_status": reviewed_criteria_completeness_status,
        "criteria_completeness_rationale": criteria_completeness_rationale,
        "review_verdict": review_verdict,
        "declared_criteria_completeness_status": assessment.criteria_completeness_status,
        "review_authority_status": _REVIEW_AUTHORITY_STATUS,
        "request_fulfillment_status": _REQUEST_FULFILLMENT_STATUS,
        "reviewer_id": reviewer_id,
        "method_ref": method_ref,
        "source_verdict": assessment.source_verdict,
        "source_completeness_status": assessment.source_completeness_status,
        "source_independence_status": assessment.source_independence_status,
    }
    return _attest_evidence_semantic_completeness_review(
        review_id=_review_id(**values),
        **values,
    )
