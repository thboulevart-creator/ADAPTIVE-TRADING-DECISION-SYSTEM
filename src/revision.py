"""P1.7 qualification-only AUDIT to REVISION boundary.

This module records an externally declared revision orientation against an
exact P1.6 audit assessment and its matching content-bound scope. It performs
no upstream repair, evidence creation, experiment execution, knowledge
promotion, or behavior change.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.memory_audit import (
    AuditScope,
    MemoryCollectionAuditAssessment,
    create_audit_scope,
    is_factory_attested_memory_collection_audit,
)


CONTRACT = "P1_7_AUDIT_REVISION_BOUNDARY_V1"

_DISPOSITIONS = frozenset(
    {
        "KEEP_CURRENT_STATE",
        "REQUEST_NEW_EVIDENCE",
        "REQUEST_NEW_EXPERIMENT",
        "REFORMULATE_QUESTION",
    }
)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RevisionDecision:
    revision_id: str
    audit_id: str
    scope_id: str
    disposition: str
    detail: str
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


def _revision_content(
    *,
    audit_id: str,
    scope_id: str,
    disposition: str,
    detail: str,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, str]:
    return {
        "contract": CONTRACT,
        "audit_id": audit_id,
        "scope_id": scope_id,
        "disposition": disposition,
        "detail": detail,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _revision_id(**content: str) -> str:
    return "REV-" + _stable_hash(content)[:32]


def _revision_fingerprint(value: RevisionDecision) -> str:
    return _stable_hash(
        {
            "contract": CONTRACT,
            "revision": asdict(value),
        }
    )


def _build_revision_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[RevisionDecision], str]] = {}

    def attest(**values: str) -> RevisionDecision:
        produced = RevisionDecision(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _revision_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, RevisionDecision):
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        return reference() is value and _revision_fingerprint(value) == expected_fingerprint

    return attest, verify


_attest_revision_decision, is_factory_attested_revision_decision = _build_revision_attestation_api()
del _build_revision_attestation_api


def produce_revision_decision(
    assessment,
    scope,
    disposition,
    detail,
) -> RevisionDecision:
    """Record one externally declared revision orientation without executing it."""
    if not isinstance(assessment, MemoryCollectionAuditAssessment):
        raise TypeError("P1.7 requires full MemoryCollectionAuditAssessment")
    if not is_factory_attested_memory_collection_audit(assessment):
        raise ValueError("P1.7 requires exact currently-attested P1.6 assessment")

    if not isinstance(scope, AuditScope):
        raise TypeError("P1.7 requires full AuditScope")
    canonical_scope = create_audit_scope(
        question=scope.question,
        expected_registration_ids=scope.expected_registration_ids,
        context_fields=scope.context_fields,
    )
    if canonical_scope != scope:
        raise ValueError("P1.7 AuditScope is not canonical")
    if scope.scope_id != assessment.scope_id:
        raise ValueError("P1.7 AuditScope does not match assessment")

    if not isinstance(disposition, str) or disposition not in _DISPOSITIONS:
        raise ValueError("P1.7 disposition is not permitted")
    if not isinstance(detail, str) or not detail.strip():
        raise ValueError("P1.7 detail must be non-empty")

    if (
        disposition == "REFORMULATE_QUESTION"
        and detail.strip() == scope.question.strip()
    ):
        raise ValueError("P1.7 reformulation must differ from source question")

    content = _revision_content(
        audit_id=assessment.audit_id,
        scope_id=scope.scope_id,
        disposition=disposition,
        detail=detail,
        source_verdict=assessment.verdict,
        source_completeness_status=assessment.completeness_status,
        source_independence_status=assessment.independence_status,
    )
    return _attest_revision_decision(
        revision_id=_revision_id(**content),
        audit_id=assessment.audit_id,
        scope_id=scope.scope_id,
        disposition=disposition,
        detail=detail,
        source_verdict=assessment.verdict,
        source_completeness_status=assessment.completeness_status,
        source_independence_status=assessment.independence_status,
    )
