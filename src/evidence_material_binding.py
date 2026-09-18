"""P1.10A qualification-only evidence material rebinding boundary.

This module proves only that exact bytes match one exact attested P1.9A
EvidenceSubmission. It does not establish authenticity, admissibility,
sufficiency, fulfillment, knowledge, execution, or authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass

from src.evidence_submission import (
    EvidenceSubmission,
    is_factory_attested_evidence_submission,
)


CONTRACT = "P1_10A_EVIDENCE_MATERIAL_BINDING_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class BoundEvidenceMaterial:
    evidence_binding_id: str
    submission_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    source_ref: str
    media_type: str
    content_sha256: str
    content_size: int
    content: bytes
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


def _binding_content(
    *,
    submission_id: str,
    request_id: str,
    revision_id: str,
    audit_id: str,
    scope_id: str,
    source_ref: str,
    media_type: str,
    content_sha256: str,
    content_size: int,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, object]:
    return {
        "contract": CONTRACT,
        "submission_id": submission_id,
        "request_id": request_id,
        "revision_id": revision_id,
        "audit_id": audit_id,
        "scope_id": scope_id,
        "source_ref": source_ref,
        "media_type": media_type,
        "content_sha256": content_sha256,
        "content_size": content_size,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _binding_id(**content: object) -> str:
    return "EBM-" + _stable_hash(content)[:32]


def _binding_fingerprint(value: BoundEvidenceMaterial) -> str:
    return _stable_hash(
        {
            "contract": CONTRACT,
            "evidence_binding_id": value.evidence_binding_id,
            "submission_id": value.submission_id,
            "request_id": value.request_id,
            "revision_id": value.revision_id,
            "audit_id": value.audit_id,
            "scope_id": value.scope_id,
            "source_ref": value.source_ref,
            "media_type": value.media_type,
            "content_sha256": value.content_sha256,
            "content_size": value.content_size,
            "content_hex": value.content.hex(),
            "source_verdict": value.source_verdict,
            "source_completeness_status": value.source_completeness_status,
            "source_independence_status": value.source_independence_status,
        }
    )


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[BoundEvidenceMaterial], str]] = {}

    def attest(**values: object) -> BoundEvidenceMaterial:
        produced = BoundEvidenceMaterial(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _binding_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not BoundEvidenceMaterial:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if _binding_fingerprint(value) != expected_fingerprint:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


_attest_bound_evidence_material, is_factory_attested_bound_evidence_material = _build_attestation_api()
del _build_attestation_api


def bind_evidence_material(
    submission,
    *,
    content,
) -> BoundEvidenceMaterial:
    """Bind exact bytes to one exact currently-attested P1.9A submission."""
    if type(submission) is not EvidenceSubmission:
        raise TypeError("P1.10A requires exact EvidenceSubmission")
    if not is_factory_attested_evidence_submission(submission):
        raise ValueError("P1.10A requires exact currently-attested P1.9A submission")
    if type(content) is not bytes:
        raise TypeError("content must be exact bytes")

    content_sha256 = hashlib.sha256(content).hexdigest()
    content_size = len(content)
    if content_sha256 != submission.content_sha256:
        raise ValueError("P1.10A content hash does not match submission")
    if content_size != submission.content_size:
        raise ValueError("P1.10A content size does not match submission")

    identity_content = _binding_content(
        submission_id=submission.submission_id,
        request_id=submission.request_id,
        revision_id=submission.revision_id,
        audit_id=submission.audit_id,
        scope_id=submission.scope_id,
        source_ref=submission.source_ref,
        media_type=submission.media_type,
        content_sha256=submission.content_sha256,
        content_size=submission.content_size,
        source_verdict=submission.source_verdict,
        source_completeness_status=submission.source_completeness_status,
        source_independence_status=submission.source_independence_status,
    )
    return _attest_bound_evidence_material(
        evidence_binding_id=_binding_id(**identity_content),
        submission_id=submission.submission_id,
        request_id=submission.request_id,
        revision_id=submission.revision_id,
        audit_id=submission.audit_id,
        scope_id=submission.scope_id,
        source_ref=submission.source_ref,
        media_type=submission.media_type,
        content_sha256=submission.content_sha256,
        content_size=submission.content_size,
        content=content,
        source_verdict=submission.source_verdict,
        source_completeness_status=submission.source_completeness_status,
        source_independence_status=submission.source_independence_status,
    )
