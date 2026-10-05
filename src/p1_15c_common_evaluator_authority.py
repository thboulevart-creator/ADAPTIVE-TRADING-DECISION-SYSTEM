"""P1.15C common experiment evaluator/method authority re-attestation.

Verifies an externally pinned authority record/receipt against one exact
P1.13C evaluation and one exact P1.14C measurement provenance. It preserves
P1.15B authority semantics without creating findings or operational authority.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import weakref
from dataclasses import asdict, dataclass
from pathlib import Path

from src.p1_13c_common_evaluation import (
    CommonExperimentEvaluationSubmission,
    is_factory_attested_common_experiment_evaluation,
)
from src.p1_14c_common_measurement_provenance import (
    CommonWitnessedMeasurementProvenance,
    is_factory_attested_common_measurement_provenance,
)

CONTRACT = "P1_15C_COMMON_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_V1"
RECORD_SCHEMA = "P1_15C_COMMON_EVALUATION_AUTHORITY_RECORD_V1"
RECEIPT_SCHEMA = "P1_15C_COMMON_EVALUATION_AUTHORITY_RECEIPT_V1"
_HEX = frozenset("0123456789abcdef")
_RECORD_KEYS = frozenset({
    "schema","contract_id","evaluation_submission_id","provenance_qualification_id",
    "execution_evidence_envelope_id","native_result_id","experiment_spec_id","request_id",
    "evaluator_id","method_ref","prediction_status","falsification_status",
    "evaluation_rationale","measurement_ids","procedure_bindings",
})
_RECEIPT_KEYS = frozenset({
    "schema","contract_id","authority_id","qualification_nonce","evaluation_submission_id",
    "provenance_qualification_id","record_sha256","qualification_id",
})


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CommonQualifiedExperimentEvaluationAuthority:
    qualification_id: str
    evaluation_submission_id: str
    provenance_qualification_id: str
    execution_evidence_envelope_id: str
    execution_owner_id: str
    native_result_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    evaluator_id: str
    method_ref: str
    prediction_status: str
    falsification_status: str
    evaluation_rationale: str
    measurement_ids: tuple[str, ...]
    procedure_bindings: tuple[tuple[str, str, str], ...]
    authority_id: str
    record_sha256: str
    receipt_sha256: str
    measurement_provenance_status: str
    evaluation_authority_status: str
    finding_status: str
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8") + b"\n"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _stable(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _strict_json(raw: bytes, *, label: str) -> dict[str, object]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} must be UTF-8") from exc

    def no_duplicates(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"{label} duplicate key: {key}")
            out[key] = value
        return out

    try:
        doc = json.loads(text, object_pairs_hook=no_duplicates)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label} invalid JSON") from exc
    if type(doc) is not dict:
        raise ValueError(f"{label} must be object")
    if _canonical(doc) != raw:
        raise ValueError(f"{label} must be canonical")
    return doc


def _sha(value: object, *, label: str) -> str:
    if type(value) is not str or len(value) != 64 or not set(value) <= _HEX:
        raise ValueError(f"{label} must be lowercase SHA-256")
    return value


def _nonempty(value: object, *, label: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be nonempty exact str")
    return value


def _qualification_id(
    *,
    authority_id: str,
    qualification_nonce: str,
    evaluation_submission_id: str,
    provenance_qualification_id: str,
    record_sha256: str,
) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "qualification_nonce": qualification_nonce,
        "evaluation_submission_id": evaluation_submission_id,
        "provenance_qualification_id": provenance_qualification_id,
        "record_sha256": record_sha256,
    }
    return "CQEA-" + _sha256(_canonical(payload))[:32]


def _fingerprint(value: CommonQualifiedExperimentEvaluationAuthority) -> str:
    return _stable({"contract": CONTRACT, "authority": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[CommonQualifiedExperimentEvaluationAuthority], str]] = {}

    def attest(**values: object) -> CommonQualifiedExperimentEvaluationAuthority:
        produced = CommonQualifiedExperimentEvaluationAuthority(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not CommonQualifiedExperimentEvaluationAuthority:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if _fingerprint(value) != expected:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


_attest, is_factory_attested_common_evaluation_authority = _build_attestation_api()
del _build_attestation_api


def validate_common_authority_claim(claim: str) -> dict[str, object]:
    if claim == "MISMATCHED_PROVENANCE":
        return {"contract": CONTRACT, "status": "BLOCKED", "reason": "BLOCKED_EVALUATOR_AUTHORITY_PROVENANCE_MISMATCH"}
    return {"contract": CONTRACT, "status": "READY", "reason": "NO_AUTHORITY_LAUNDERING"}


def _validate_upstream(
    evaluation: CommonExperimentEvaluationSubmission,
    provenance: CommonWitnessedMeasurementProvenance,
) -> None:
    pairs = (
        ("evaluation_submission_id", evaluation.evaluation_submission_id),
        ("execution_evidence_envelope_id", evaluation.execution_evidence_envelope_id),
        ("execution_owner_id", evaluation.execution_owner_id),
        ("native_result_id", evaluation.native_result_id),
        ("experiment_spec_id", evaluation.experiment_spec_id),
        ("request_id", evaluation.request_id),
        ("revision_id", evaluation.revision_id),
        ("audit_id", evaluation.audit_id),
        ("scope_id", evaluation.scope_id),
        ("method_ref", evaluation.method_ref),
    )
    for field, expected in pairs:
        if getattr(provenance, field) != expected:
            raise ValueError(f"P1.15C upstream mismatch: {field}")
    if provenance.measurement_provenance_status != "PASS":
        raise ValueError("P1.15C requires provenance PASS")
    if provenance.evaluation_authority_status != "BLOCKED":
        raise ValueError("P1.15C requires pre-authority BLOCKED")
    if provenance.finding_status != "BLOCKED":
        raise ValueError("P1.15C requires finding BLOCKED")
    expected_ids = tuple(item.measurement_id for item in evaluation.measurements)
    actual_ids = tuple(item.measurement_id for item in provenance.derivations)
    if expected_ids != actual_ids:
        raise ValueError("P1.15C measurement identities/order mismatch")


def reattest_common_evaluator_authority(
    evaluation_submission,
    measurement_provenance,
    record_path,
    receipt_path,
    *,
    expected_authority_id,
    expected_receipt_sha256,
) -> CommonQualifiedExperimentEvaluationAuthority:
    if type(evaluation_submission) is not CommonExperimentEvaluationSubmission:
        raise TypeError("P1.15C requires exact CommonExperimentEvaluationSubmission")
    if not is_factory_attested_common_experiment_evaluation(evaluation_submission):
        raise ValueError("P1.15C requires currently-attested P1.13C evaluation")
    if type(measurement_provenance) is not CommonWitnessedMeasurementProvenance:
        raise TypeError("P1.15C requires exact CommonWitnessedMeasurementProvenance")
    if not is_factory_attested_common_measurement_provenance(measurement_provenance):
        raise ValueError("P1.15C requires currently-attested P1.14C provenance")

    _validate_upstream(evaluation_submission, measurement_provenance)

    authority_id = _nonempty(expected_authority_id, label="expected_authority_id")
    expected_pin = _sha(expected_receipt_sha256, label="expected_receipt_sha256")
    record_file = Path(record_path)
    receipt_file = Path(receipt_path)
    if not record_file.is_file() or not receipt_file.is_file():
        raise ValueError("P1.15C record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha, expected_pin):
        raise ValueError("P1.15C receipt pin mismatch")

    record = _strict_json(record_bytes, label="common authority record")
    receipt = _strict_json(receipt_bytes, label="common authority receipt")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.15C record schema mismatch")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.15C receipt schema mismatch")
    if record["schema"] != RECORD_SCHEMA or record["contract_id"] != CONTRACT:
        raise ValueError("P1.15C record contract mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["contract_id"] != CONTRACT:
        raise ValueError("P1.15C receipt contract mismatch")
    if receipt["authority_id"] != authority_id:
        raise ValueError("P1.15C authority mismatch")

    nonce = receipt["qualification_nonce"]
    if type(nonce) is not str or len(nonce) < 32 or not set(nonce) <= _HEX:
        raise ValueError("P1.15C invalid qualification nonce")
    record_sha = _sha(receipt["record_sha256"], label="record_sha256")
    if not secrets.compare_digest(record_sha, _sha256(record_bytes)):
        raise ValueError("P1.15C record integrity mismatch")

    procedure_bindings = [
        {
            "measurement_id": item.measurement_id,
            "procedure_ref": item.procedure_ref,
            "procedure_sha256": item.procedure_sha256,
        }
        for item in measurement_provenance.derivations
    ]
    expected_record = {
        "schema": RECORD_SCHEMA,
        "contract_id": CONTRACT,
        "evaluation_submission_id": evaluation_submission.evaluation_submission_id,
        "provenance_qualification_id": measurement_provenance.provenance_qualification_id,
        "execution_evidence_envelope_id": evaluation_submission.execution_evidence_envelope_id,
        "native_result_id": evaluation_submission.native_result_id,
        "experiment_spec_id": evaluation_submission.experiment_spec_id,
        "request_id": evaluation_submission.request_id,
        "evaluator_id": evaluation_submission.evaluator_id,
        "method_ref": evaluation_submission.method_ref,
        "prediction_status": evaluation_submission.prediction_status,
        "falsification_status": evaluation_submission.falsification_status,
        "evaluation_rationale": evaluation_submission.evaluation_rationale,
        "measurement_ids": [item.measurement_id for item in evaluation_submission.measurements],
        "procedure_bindings": procedure_bindings,
    }
    if record != expected_record:
        raise ValueError("P1.15C authority record mismatch")
    if receipt["evaluation_submission_id"] != evaluation_submission.evaluation_submission_id:
        raise ValueError("P1.15C receipt evaluation mismatch")
    if receipt["provenance_qualification_id"] != measurement_provenance.provenance_qualification_id:
        raise ValueError("P1.15C receipt provenance mismatch")

    expected_id = _qualification_id(
        authority_id=authority_id,
        qualification_nonce=nonce,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        provenance_qualification_id=measurement_provenance.provenance_qualification_id,
        record_sha256=record_sha,
    )
    if receipt["qualification_id"] != expected_id:
        raise ValueError("P1.15C qualification identity mismatch")

    return _attest(
        qualification_id=expected_id,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        provenance_qualification_id=measurement_provenance.provenance_qualification_id,
        execution_evidence_envelope_id=evaluation_submission.execution_evidence_envelope_id,
        execution_owner_id=evaluation_submission.execution_owner_id,
        native_result_id=evaluation_submission.native_result_id,
        experiment_spec_id=evaluation_submission.experiment_spec_id,
        request_id=evaluation_submission.request_id,
        revision_id=evaluation_submission.revision_id,
        audit_id=evaluation_submission.audit_id,
        scope_id=evaluation_submission.scope_id,
        evaluator_id=evaluation_submission.evaluator_id,
        method_ref=evaluation_submission.method_ref,
        prediction_status=evaluation_submission.prediction_status,
        falsification_status=evaluation_submission.falsification_status,
        evaluation_rationale=evaluation_submission.evaluation_rationale,
        measurement_ids=tuple(item.measurement_id for item in evaluation_submission.measurements),
        procedure_bindings=tuple((x["measurement_id"], x["procedure_ref"], x["procedure_sha256"]) for x in procedure_bindings),
        authority_id=authority_id,
        record_sha256=record_sha,
        receipt_sha256=actual_receipt_sha,
        measurement_provenance_status="PASS",
        evaluation_authority_status="PASS",
        finding_status="BLOCKED",
        scientific_authority=False,
        operational_authority=False,
        trading_authority=False,
        capital_authority=False,
    )
