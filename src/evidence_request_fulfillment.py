"""P1.15A evidence request fulfillment decision boundary.

This boundary consumes one exact factory-attested P1.14A reviewer/method
authority qualification and deterministically promotes its authoritative
review verdict to the request-level fulfillment status. It does not reinterpret
evidence content, create knowledge, or authorize operations.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.reviewer_method_authority import (
    ReviewerMethodAuthorityQualification,
    is_factory_attested_reviewer_method_authority_qualification,
)


CONTRACT = "P1_15A_EVIDENCE_REQUEST_FULFILLMENT_DECISION_BOUNDARY_V1"

_VERDICT_TO_FULFILLMENT = {
    "PASS": "PASS",
    "FAIL": "FAIL",
    "BLOCKED": "BLOCKED",
}


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvidenceRequestFulfillmentDecision:
    fulfillment_decision_id: str
    qualification_id: str
    review_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    criteria_id: str
    reviewer_id: str
    method_ref: str
    authority_id: str
    review_verdict: str
    review_authority_status: str
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


def _decision_id(**values: object) -> str:
    return "ERF-" + _stable_hash({"contract": CONTRACT, **values})[:32]


def _fingerprint(value: EvidenceRequestFulfillmentDecision) -> str:
    return _stable_hash({"contract": CONTRACT, "decision": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[EvidenceRequestFulfillmentDecision], str],
    ] = {}

    def attest(**values: object) -> EvidenceRequestFulfillmentDecision:
        produced = EvidenceRequestFulfillmentDecision(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not EvidenceRequestFulfillmentDecision:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if _fingerprint(value) != expected_fingerprint:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


_attest_evidence_request_fulfillment_decision, is_factory_attested_evidence_request_fulfillment_decision = _build_attestation_api()
del _build_attestation_api


def decide_evidence_request_fulfillment(
    authority_qualification,
) -> EvidenceRequestFulfillmentDecision:
    """Promote one exact authoritative review verdict to request fulfillment."""
    if type(authority_qualification) is not ReviewerMethodAuthorityQualification:
        raise TypeError("P1.15A requires exact ReviewerMethodAuthorityQualification")
    if not is_factory_attested_reviewer_method_authority_qualification(authority_qualification):
        raise ValueError("P1.15A requires currently-attested P1.14A qualification")
    if authority_qualification.review_authority_status != "PASS":
        raise ValueError("P1.15A requires review_authority_status PASS")

    fulfillment_status = _VERDICT_TO_FULFILLMENT.get(authority_qualification.review_verdict)
    if fulfillment_status is None:
        raise ValueError("P1.15A requires governed review verdict")

    values = {
        "qualification_id": authority_qualification.qualification_id,
        "review_id": authority_qualification.review_id,
        "request_id": authority_qualification.request_id,
        "revision_id": authority_qualification.revision_id,
        "audit_id": authority_qualification.audit_id,
        "scope_id": authority_qualification.scope_id,
        "criteria_id": authority_qualification.criteria_id,
        "reviewer_id": authority_qualification.reviewer_id,
        "method_ref": authority_qualification.method_ref,
        "authority_id": authority_qualification.authority_id,
        "review_verdict": authority_qualification.review_verdict,
        "review_authority_status": authority_qualification.review_authority_status,
        "request_fulfillment_status": fulfillment_status,
        "source_verdict": authority_qualification.source_verdict,
        "source_completeness_status": authority_qualification.source_completeness_status,
        "source_independence_status": authority_qualification.source_independence_status,
    }
    return _attest_evidence_request_fulfillment_decision(
        fulfillment_decision_id=_decision_id(**values),
        **values,
    )
