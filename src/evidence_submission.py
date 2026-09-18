"""P1.9A qualification-only FOLLOW-UP REQUEST to EVIDENCE SUBMISSION boundary.

This module records externally supplied bytes against one exact attested
EVIDENCE FollowUpRequest. A submission is not fulfillment, admissibility,
sufficiency, ResearchRunEvidence, knowledge, execution, or authorization.
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


CONTRACT = "P1_9A_EVIDENCE_SUBMISSION_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvidenceSubmission:
    submission_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    source_ref: str
    media_type: str
    content_sha256: str
    content_size: int
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


def _submission_content(
    *,
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


def _submission_id(**content: object) -> str:
    return "EVS-" + _stable_hash(content)[:32]


def _submission_fingerprint(value: EvidenceSubmission) -> str:
    return _stable_hash({"contract": CONTRACT, "submission": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[EvidenceSubmission], str]] = {}

    def attest(**values: object) -> EvidenceSubmission:
        produced = EvidenceSubmission(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _submission_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, EvidenceSubmission):
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _submission_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_evidence_submission, is_factory_attested_evidence_submission = _build_attestation_api()
del _build_attestation_api


def submit_evidence(
    request,
    *,
    source_ref,
    media_type,
    content,
) -> EvidenceSubmission:
    """Record exact external bytes against one exact attested EVIDENCE request."""
    if not isinstance(request, FollowUpRequest):
        raise TypeError("P1.9A requires full FollowUpRequest")
    if not is_factory_attested_follow_up_request(request):
        raise ValueError("P1.9A requires exact currently-attested P1.8 request")
    if request.request_kind != "EVIDENCE":
        raise ValueError("P1.9A requires EVIDENCE request")

    if type(source_ref) is not str:
        raise TypeError("source_ref must be exact str")
    if not source_ref.strip():
        raise ValueError("source_ref must be nonempty after strip")
    if type(media_type) is not str:
        raise TypeError("media_type must be exact str")
    if not media_type.strip():
        raise ValueError("media_type must be nonempty after strip")
    if type(content) is not bytes:
        raise TypeError("content must be exact bytes")

    content_sha256 = hashlib.sha256(content).hexdigest()
    content_size = len(content)
    identity_content = _submission_content(
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        source_ref=source_ref,
        media_type=media_type,
        content_sha256=content_sha256,
        content_size=content_size,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
    return _attest_evidence_submission(
        submission_id=_submission_id(**identity_content),
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        source_ref=source_ref,
        media_type=media_type,
        content_sha256=content_sha256,
        content_size=content_size,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
