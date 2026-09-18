"""P1.14A externally pinned reviewer/method authority re-attestation.

This boundary verifies a canonical external authority record and receipt
against one exact P1.13A review and an independently supplied receipt pin.
It does not create authority records, establish semantic truth, fulfill a
request, promote knowledge, or authorize operations.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import weakref
from dataclasses import asdict, dataclass
from pathlib import Path

from src.evidence_semantic_completeness_review import (
    CONTRACT as P113A_CONTRACT,
    EvidenceSemanticCompletenessReview,
    is_factory_attested_evidence_semantic_completeness_review,
)


CONTRACT = "P1_14A_REVIEWER_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1"
RECORD_SCHEMA = "P1_14A_REVIEWER_METHOD_AUTHORITY_RECORD_V1"
RECEIPT_SCHEMA = "P1_14A_REVIEWER_METHOD_AUTHORITY_RECEIPT_V1"

_HEX = frozenset("0123456789abcdef")
_RECORD_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "review_contract_id",
        "review_id",
        "assessment_id",
        "criteria_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
        "reviewer_id",
        "method_ref",
    }
)
_RECEIPT_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "authority_id",
        "qualification_nonce",
        "review_id",
        "reviewer_id",
        "method_ref",
        "record_sha256",
        "qualification_id",
    }
)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ReviewerMethodAuthorityQualification:
    qualification_id: str
    review_id: str
    assessment_id: str
    criteria_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    reviewer_id: str
    method_ref: str
    authority_id: str
    record_sha256: str
    receipt_sha256: str
    review_verdict: str
    review_authority_status: str
    request_fulfillment_status: str
    source_verdict: str
    source_completeness_status: str
    source_independence_status: str


def _canonical(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        + b"\n"
    )


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _stable_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _strict_json(raw: bytes, *, label: str) -> dict[str, object]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} must be UTF-8") from exc

    def no_duplicates(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{label} contains duplicate key: {key}")
            result[key] = value
        return result

    try:
        document = json.loads(text, object_pairs_hook=no_duplicates)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label} is not valid strict JSON") from exc
    if type(document) is not dict:
        raise ValueError(f"{label} must be a JSON object")
    if _canonical(document) != raw:
        raise ValueError(f"{label} is not canonical")
    return document


def _validate_sha256(value: object, *, label: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if len(value) != 64 or not set(value) <= _HEX:
        raise ValueError(f"{label} must be lowercase SHA-256 hex")
    return value


def _validate_nonempty_str(value: object, *, label: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty")
    return value


def _qualification_id(
    *,
    authority_id: str,
    qualification_nonce: str,
    review_id: str,
    reviewer_id: str,
    method_ref: str,
    record_sha256: str,
) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": qualification_nonce,
        "review_id": review_id,
        "reviewer_id": reviewer_id,
        "method_ref": method_ref,
        "record_sha256": record_sha256,
    }
    return "RMAQ-" + _sha256(_canonical(payload))[:32]


def _fingerprint(value: ReviewerMethodAuthorityQualification) -> str:
    return _stable_hash({"contract": CONTRACT, "qualification": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[ReviewerMethodAuthorityQualification], str],
    ] = {}

    def attest(**values: object) -> ReviewerMethodAuthorityQualification:
        produced = ReviewerMethodAuthorityQualification(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not ReviewerMethodAuthorityQualification:
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


_attest_reviewer_method_authority_qualification, is_factory_attested_reviewer_method_authority_qualification = _build_attestation_api()
del _build_attestation_api


def reattest_reviewer_method_authority(
    review,
    record_path,
    receipt_path,
    *,
    expected_authority_id,
    expected_receipt_sha256,
) -> ReviewerMethodAuthorityQualification:
    """Verify one external reviewer/method authority witness."""
    if type(review) is not EvidenceSemanticCompletenessReview:
        raise TypeError("P1.14A requires exact EvidenceSemanticCompletenessReview")
    if not is_factory_attested_evidence_semantic_completeness_review(review):
        raise ValueError("P1.14A requires currently-attested P1.13A review")

    if not isinstance(record_path, (str, Path)) or not isinstance(receipt_path, (str, Path)):
        raise TypeError("P1.14A requires record and receipt paths")

    expected_authority_id = _validate_nonempty_str(
        expected_authority_id,
        label="expected_authority_id",
    )
    expected_pin = _validate_sha256(
        expected_receipt_sha256,
        label="expected_receipt_sha256",
    )

    record_file = Path(record_path)
    receipt_file = Path(receipt_path)
    if not record_file.is_file() or not receipt_file.is_file():
        raise ValueError("P1.14A authority record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha256 = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha256, expected_pin):
        raise ValueError("P1.14A external receipt pin mismatch")

    receipt = _strict_json(receipt_bytes, label="authority receipt")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.14A receipt schema mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["contract_id"] != CONTRACT:
        raise ValueError("P1.14A receipt contract mismatch")
    if receipt["authority_id"] != expected_authority_id:
        raise ValueError("P1.14A authority expectation mismatch")

    nonce = receipt["qualification_nonce"]
    if (
        type(nonce) is not str
        or len(nonce) < 32
        or not nonce
        or not set(nonce) <= _HEX
    ):
        raise ValueError("P1.14A invalid qualification nonce")

    record_sha256 = _validate_sha256(receipt["record_sha256"], label="record_sha256")
    actual_record_sha256 = _sha256(record_bytes)
    if not secrets.compare_digest(actual_record_sha256, record_sha256):
        raise ValueError("P1.14A authority record integrity mismatch")

    record = _strict_json(record_bytes, label="authority record")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.14A record schema mismatch")

    expected_record = {
        "schema": RECORD_SCHEMA,
        "contract_id": CONTRACT,
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
    if record != expected_record:
        raise ValueError("P1.14A authority record does not match exact review")

    if receipt["review_id"] != review.review_id:
        raise ValueError("P1.14A receipt review mismatch")
    if receipt["reviewer_id"] != review.reviewer_id:
        raise ValueError("P1.14A receipt reviewer mismatch")
    if receipt["method_ref"] != review.method_ref:
        raise ValueError("P1.14A receipt method mismatch")

    expected_qualification_id = _qualification_id(
        authority_id=expected_authority_id,
        qualification_nonce=nonce,
        review_id=review.review_id,
        reviewer_id=review.reviewer_id,
        method_ref=review.method_ref,
        record_sha256=record_sha256,
    )
    if receipt["qualification_id"] != expected_qualification_id:
        raise ValueError("P1.14A qualification identity mismatch")

    return _attest_reviewer_method_authority_qualification(
        qualification_id=expected_qualification_id,
        review_id=review.review_id,
        assessment_id=review.assessment_id,
        criteria_id=review.criteria_id,
        request_id=review.request_id,
        revision_id=review.revision_id,
        audit_id=review.audit_id,
        scope_id=review.scope_id,
        reviewer_id=review.reviewer_id,
        method_ref=review.method_ref,
        authority_id=expected_authority_id,
        record_sha256=record_sha256,
        receipt_sha256=actual_receipt_sha256,
        review_verdict=review.review_verdict,
        review_authority_status="PASS",
        request_fulfillment_status="BLOCKED",
        source_verdict=review.source_verdict,
        source_completeness_status=review.source_completeness_status,
        source_independence_status=review.source_independence_status,
    )
