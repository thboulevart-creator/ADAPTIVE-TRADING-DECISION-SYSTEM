"""P1.8 qualification-only REVISION to FOLLOW-UP REQUEST boundary.

This module records a non-executable follow-up request from an exact P1.7
RevisionDecision. It creates no evidence, experiment, execution input,
execution result, authorization, knowledge, or behavior change.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.revision import (
    RevisionDecision,
    is_factory_attested_revision_decision,
)


CONTRACT = "P1_8_REVISION_FOLLOWUP_REQUEST_BOUNDARY_V1"

_ROUTING = {
    "REQUEST_NEW_EVIDENCE": "EVIDENCE",
    "REQUEST_NEW_EXPERIMENT": "EXPERIMENT",
}


@dataclass(frozen=True, slots=True, weakref_slot=True)
class FollowUpRequest:
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    request_kind: str
    specification: str
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


def _request_content(
    *,
    revision_id: str,
    audit_id: str,
    scope_id: str,
    request_kind: str,
    specification: str,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, str]:
    return {
        "contract": CONTRACT,
        "revision_id": revision_id,
        "audit_id": audit_id,
        "scope_id": scope_id,
        "request_kind": request_kind,
        "specification": specification,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _request_id(**content: str) -> str:
    return "FUR-" + _stable_hash(content)[:32]


def _request_fingerprint(value: FollowUpRequest) -> str:
    return _stable_hash(
        {
            "contract": CONTRACT,
            "request": asdict(value),
        }
    )


def _build_request_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[FollowUpRequest], str]] = {}

    def attest(**values: str) -> FollowUpRequest:
        produced = FollowUpRequest(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _request_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, FollowUpRequest):
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _request_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_follow_up_request, is_factory_attested_follow_up_request = _build_request_attestation_api()
del _build_request_attestation_api


def produce_follow_up_request(revision) -> FollowUpRequest:
    """Record a non-executable follow-up request from one exact P1.7 revision."""
    if not isinstance(revision, RevisionDecision):
        raise TypeError("P1.8 requires full RevisionDecision")
    if not is_factory_attested_revision_decision(revision):
        raise ValueError("P1.8 requires exact currently-attested P1.7 revision")

    request_kind = _ROUTING.get(revision.disposition)
    if request_kind is None:
        raise ValueError("P1.8 revision disposition is not routable")

    content = _request_content(
        revision_id=revision.revision_id,
        audit_id=revision.audit_id,
        scope_id=revision.scope_id,
        request_kind=request_kind,
        specification=revision.detail,
        source_verdict=revision.source_verdict,
        source_completeness_status=revision.source_completeness_status,
        source_independence_status=revision.source_independence_status,
    )
    return _attest_follow_up_request(
        request_id=_request_id(**content),
        revision_id=revision.revision_id,
        audit_id=revision.audit_id,
        scope_id=revision.scope_id,
        request_kind=request_kind,
        specification=revision.detail,
        source_verdict=revision.source_verdict,
        source_completeness_status=revision.source_completeness_status,
        source_independence_status=revision.source_independence_status,
    )
