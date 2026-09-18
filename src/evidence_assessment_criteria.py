"""P1.11A qualification-only evidence assessment criteria boundary.

This module records externally declared criteria for one exact attested
EVIDENCE FollowUpRequest. It does not inspect evidence material and does not
establish admissibility, sufficiency, fulfillment, knowledge, or authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.follow_up_request import (
    FollowUpRequest,
    is_factory_attested_follow_up_request,
)


CONTRACT = "P1_11A_EVIDENCE_ASSESSMENT_CRITERIA_BOUNDARY_V1"
_CRITERIA_COMPLETENESS_STATUS = "BLOCKED"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvidenceAssessmentCriteria:
    criteria_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    specification: str
    minimum_distinct_materials: int
    require_nonempty_content: bool
    allowed_media_types: tuple[str, ...] | None
    allowed_source_refs: tuple[str, ...] | None
    semantic_requirements: tuple[str, ...]
    criteria_completeness_status: str
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


def _validate_optional_nonempty_string_tuple(label: str, value):
    if value is None:
        return None
    if type(value) is not tuple:
        raise TypeError(f"{label} must be None or exact tuple")
    if not value:
        raise ValueError(f"{label} must be nonempty when provided")
    _validate_string_tuple_items(label, value)
    return value


def _validate_string_tuple_items(label: str, value: tuple[object, ...]) -> None:
    seen: set[str] = set()
    for item in value:
        if type(item) is not str:
            raise TypeError(f"{label} items must be exact str")
        if not item.strip():
            raise ValueError(f"{label} items must be nonempty after strip")
        if item in seen:
            raise ValueError(f"{label} must not contain duplicates")
        seen.add(item)


def _criteria_content(
    *,
    request_id: str,
    revision_id: str,
    audit_id: str,
    scope_id: str,
    specification: str,
    minimum_distinct_materials: int,
    require_nonempty_content: bool,
    allowed_media_types: tuple[str, ...] | None,
    allowed_source_refs: tuple[str, ...] | None,
    semantic_requirements: tuple[str, ...],
    criteria_completeness_status: str,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, object]:
    return {
        "contract": CONTRACT,
        "request_id": request_id,
        "revision_id": revision_id,
        "audit_id": audit_id,
        "scope_id": scope_id,
        "specification": specification,
        "minimum_distinct_materials": minimum_distinct_materials,
        "require_nonempty_content": require_nonempty_content,
        "allowed_media_types": allowed_media_types,
        "allowed_source_refs": allowed_source_refs,
        "semantic_requirements": semantic_requirements,
        "criteria_completeness_status": criteria_completeness_status,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _criteria_id(**content: object) -> str:
    return "EAC-" + _stable_hash(content)[:32]


def _criteria_fingerprint(value: EvidenceAssessmentCriteria) -> str:
    return _stable_hash({"contract": CONTRACT, "criteria": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[EvidenceAssessmentCriteria], str]] = {}

    def attest(**values: object) -> EvidenceAssessmentCriteria:
        produced = EvidenceAssessmentCriteria(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _criteria_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not EvidenceAssessmentCriteria:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _criteria_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_evidence_assessment_criteria, is_factory_attested_evidence_assessment_criteria = _build_attestation_api()
del _build_attestation_api


def declare_evidence_assessment_criteria(
    request,
    *,
    minimum_distinct_materials,
    require_nonempty_content,
    allowed_media_types,
    allowed_source_refs,
    semantic_requirements,
) -> EvidenceAssessmentCriteria:
    """Record explicit criteria without evaluating or fulfilling the request."""
    if type(request) is not FollowUpRequest:
        raise TypeError("P1.11A requires exact FollowUpRequest")
    if not is_factory_attested_follow_up_request(request):
        raise ValueError("P1.11A requires exact currently-attested P1.8 request")
    if request.request_kind != "EVIDENCE":
        raise ValueError("P1.11A requires EVIDENCE request")

    if type(minimum_distinct_materials) is not int:
        raise TypeError("minimum_distinct_materials must be exact int")
    if minimum_distinct_materials < 1:
        raise ValueError("minimum_distinct_materials must be >= 1")

    if type(require_nonempty_content) is not bool:
        raise TypeError("require_nonempty_content must be exact bool")

    allowed_media_types = _validate_optional_nonempty_string_tuple(
        "allowed_media_types",
        allowed_media_types,
    )
    allowed_source_refs = _validate_optional_nonempty_string_tuple(
        "allowed_source_refs",
        allowed_source_refs,
    )

    if type(semantic_requirements) is not tuple:
        raise TypeError("semantic_requirements must be exact tuple")
    _validate_string_tuple_items("semantic_requirements", semantic_requirements)

    values = {
        "request_id": request.request_id,
        "revision_id": request.revision_id,
        "audit_id": request.audit_id,
        "scope_id": request.scope_id,
        "specification": request.specification,
        "minimum_distinct_materials": minimum_distinct_materials,
        "require_nonempty_content": require_nonempty_content,
        "allowed_media_types": allowed_media_types,
        "allowed_source_refs": allowed_source_refs,
        "semantic_requirements": semantic_requirements,
        "criteria_completeness_status": _CRITERIA_COMPLETENESS_STATUS,
        "source_verdict": request.source_verdict,
        "source_completeness_status": request.source_completeness_status,
        "source_independence_status": request.source_independence_status,
    }
    return _attest_evidence_assessment_criteria(
        criteria_id=_criteria_id(**_criteria_content(**values)),
        **values,
    )
