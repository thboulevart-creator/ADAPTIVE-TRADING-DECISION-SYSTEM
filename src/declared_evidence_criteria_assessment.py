"""P1.12A qualification-only declared evidence criteria assessment boundary.

This module evaluates only machine-checkable criteria explicitly recorded by
P1.11A against exact P1.10A bound materials. It does not interpret evidence
content and does not establish admissibility, sufficiency, request fulfillment,
knowledge, or authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.evidence_assessment_criteria import (
    EvidenceAssessmentCriteria,
    is_factory_attested_evidence_assessment_criteria,
)
from src.evidence_material_binding import (
    BoundEvidenceMaterial,
    is_factory_attested_bound_evidence_material,
)


CONTRACT = "P1_12A_DECLARED_EVIDENCE_CRITERIA_ASSESSMENT_BOUNDARY_V1"
_REQUEST_FULFILLMENT_STATUS = "BLOCKED"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DeclaredEvidenceCriteriaAssessment:
    assessment_id: str
    criteria_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    material_binding_ids: tuple[str, ...]
    distinct_material_count: int
    minimum_distinct_materials_status: str
    nonempty_content_status: str
    media_type_status: str
    source_ref_status: str
    semantic_requirements_status: str
    unresolved_semantic_requirements: tuple[str, ...]
    declared_criteria_verdict: str
    criteria_completeness_status: str
    request_fulfillment_status: str
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


def _assessment_id(**content: object) -> str:
    return "DEA-" + _stable_hash({"contract": CONTRACT, **content})[:32]


def _assessment_fingerprint(value: DeclaredEvidenceCriteriaAssessment) -> str:
    return _stable_hash({"contract": CONTRACT, "assessment": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[DeclaredEvidenceCriteriaAssessment], str],
    ] = {}

    def attest(**values: object) -> DeclaredEvidenceCriteriaAssessment:
        produced = DeclaredEvidenceCriteriaAssessment(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _assessment_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not DeclaredEvidenceCriteriaAssessment:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _assessment_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_declared_evidence_criteria_assessment, is_factory_attested_declared_evidence_criteria_assessment = _build_attestation_api()
del _build_attestation_api


def assess_declared_evidence_criteria(
    criteria,
    materials,
) -> DeclaredEvidenceCriteriaAssessment:
    """Evaluate only the explicitly declared, mechanically checkable criteria."""
    if type(criteria) is not EvidenceAssessmentCriteria:
        raise TypeError("P1.12A requires exact EvidenceAssessmentCriteria")
    if not is_factory_attested_evidence_assessment_criteria(criteria):
        raise ValueError("P1.12A requires exact currently-attested P1.11A criteria")

    if type(materials) is not tuple:
        raise TypeError("P1.12A materials must be exact tuple")
    if not materials:
        raise ValueError("P1.12A requires at least one material")

    expected_provenance = (
        criteria.request_id,
        criteria.revision_id,
        criteria.audit_id,
        criteria.scope_id,
        criteria.source_verdict,
        criteria.source_completeness_status,
        criteria.source_independence_status,
    )
    material_binding_ids: list[str] = []
    seen_binding_ids: set[str] = set()

    for material in materials:
        if type(material) is not BoundEvidenceMaterial:
            raise TypeError("P1.12A requires exact BoundEvidenceMaterial values")
        if not is_factory_attested_bound_evidence_material(material):
            raise ValueError("P1.12A requires currently-attested P1.10A materials")

        material_provenance = (
            material.request_id,
            material.revision_id,
            material.audit_id,
            material.scope_id,
            material.source_verdict,
            material.source_completeness_status,
            material.source_independence_status,
        )
        if material_provenance != expected_provenance:
            raise ValueError("P1.12A material provenance does not match criteria")

        if material.evidence_binding_id in seen_binding_ids:
            raise ValueError("P1.12A duplicate evidence_binding_id")
        seen_binding_ids.add(material.evidence_binding_id)
        material_binding_ids.append(material.evidence_binding_id)

    distinct_material_count = len(material_binding_ids)
    minimum_status = (
        "PASS"
        if distinct_material_count >= criteria.minimum_distinct_materials
        else "FAIL"
    )
    nonempty_status = (
        "PASS"
        if not criteria.require_nonempty_content
        or all(material.content_size > 0 for material in materials)
        else "FAIL"
    )
    media_type_status = (
        "PASS"
        if criteria.allowed_media_types is None
        or all(material.media_type in criteria.allowed_media_types for material in materials)
        else "FAIL"
    )
    source_ref_status = (
        "PASS"
        if criteria.allowed_source_refs is None
        or all(material.source_ref in criteria.allowed_source_refs for material in materials)
        else "FAIL"
    )

    unresolved_semantic_requirements = criteria.semantic_requirements
    semantic_status = "PASS" if not unresolved_semantic_requirements else "BLOCKED"

    structural_statuses = (
        minimum_status,
        nonempty_status,
        media_type_status,
        source_ref_status,
    )
    if "FAIL" in structural_statuses:
        declared_verdict = "FAIL"
    elif semantic_status == "BLOCKED":
        declared_verdict = "BLOCKED"
    else:
        declared_verdict = "PASS"

    values = {
        "criteria_id": criteria.criteria_id,
        "request_id": criteria.request_id,
        "revision_id": criteria.revision_id,
        "audit_id": criteria.audit_id,
        "scope_id": criteria.scope_id,
        "material_binding_ids": tuple(material_binding_ids),
        "distinct_material_count": distinct_material_count,
        "minimum_distinct_materials_status": minimum_status,
        "nonempty_content_status": nonempty_status,
        "media_type_status": media_type_status,
        "source_ref_status": source_ref_status,
        "semantic_requirements_status": semantic_status,
        "unresolved_semantic_requirements": unresolved_semantic_requirements,
        "declared_criteria_verdict": declared_verdict,
        "criteria_completeness_status": criteria.criteria_completeness_status,
        "request_fulfillment_status": _REQUEST_FULFILLMENT_STATUS,
        "source_verdict": criteria.source_verdict,
        "source_completeness_status": criteria.source_completeness_status,
        "source_independence_status": criteria.source_independence_status,
    }
    return _attest_declared_evidence_criteria_assessment(
        assessment_id=_assessment_id(**values),
        **values,
    )
