"""P1.15B externally pinned experiment evaluator/method authority re-attestation.

This boundary verifies an external authority record and receipt against one
exact P1.13B evaluation submission and one exact P1.14B witnessed measurement
provenance qualification. It establishes only evaluator/method/procedure-set
authority for that exact evaluation. It does not produce findings, recompute
measurements, create ResearchRunEvidence, promote knowledge, or authorize
operations.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import weakref
from dataclasses import asdict, dataclass
from pathlib import Path

from src.experiment_evaluation_submission import (
    ExperimentEvaluationSubmission,
    is_factory_attested_experiment_evaluation_submission,
)
from src.experiment_measurement_provenance import (
    WitnessedMeasurementProvenance,
    is_factory_attested_witnessed_measurement_provenance,
)


CONTRACT = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_REATTESTATION_BOUNDARY_V1"
RECORD_SCHEMA = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECORD_V1"
RECEIPT_SCHEMA = "P1_15B_EXPERIMENT_EVALUATOR_METHOD_AUTHORITY_RECEIPT_V1"

_HEX = frozenset("0123456789abcdef")
_RECORD_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "evaluation_submission_id",
        "provenance_qualification_id",
        "experiment_execution_result_id",
        "experiment_spec_id",
        "request_id",
        "evaluator_id",
        "method_ref",
        "prediction_status",
        "falsification_status",
        "evaluation_rationale",
        "measurement_ids",
        "procedure_bindings",
    }
)
_RECEIPT_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "authority_id",
        "qualification_nonce",
        "evaluation_submission_id",
        "provenance_qualification_id",
        "record_sha256",
        "qualification_id",
    }
)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedExperimentEvaluationAuthority:
    qualification_id: str
    evaluation_submission_id: str
    provenance_qualification_id: str
    experiment_execution_result_id: str
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
    return "QEA-" + _sha256(_canonical(payload))[:32]


def _fingerprint(value: QualifiedExperimentEvaluationAuthority) -> str:
    return _stable_hash({"contract": CONTRACT, "qualification": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[QualifiedExperimentEvaluationAuthority], str],
    ] = {}

    def attest(**values: object) -> QualifiedExperimentEvaluationAuthority:
        produced = QualifiedExperimentEvaluationAuthority(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not QualifiedExperimentEvaluationAuthority:
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


_attest_qualified_experiment_evaluation_authority, is_factory_attested_qualified_experiment_evaluation_authority = _build_attestation_api()
del _build_attestation_api


def _validate_upstream_coherence(
    evaluation_submission: ExperimentEvaluationSubmission,
    measurement_provenance: WitnessedMeasurementProvenance,
) -> None:
    pairs = (
        ("evaluation_submission_id", evaluation_submission.evaluation_submission_id),
        ("experiment_execution_result_id", evaluation_submission.experiment_execution_result_id),
        ("experiment_spec_id", evaluation_submission.experiment_spec_id),
        ("request_id", evaluation_submission.request_id),
        ("revision_id", evaluation_submission.revision_id),
        ("audit_id", evaluation_submission.audit_id),
        ("scope_id", evaluation_submission.scope_id),
        ("method_ref", evaluation_submission.method_ref),
        ("source_verdict", evaluation_submission.source_verdict),
        ("source_completeness_status", evaluation_submission.source_completeness_status),
        ("source_independence_status", evaluation_submission.source_independence_status),
    )
    for field_name, expected in pairs:
        if getattr(measurement_provenance, field_name) != expected:
            raise ValueError(f"P1.15B upstream mismatch: {field_name}")

    if measurement_provenance.measurement_provenance_status != "PASS":
        raise ValueError("P1.15B requires measurement_provenance_status PASS")
    if measurement_provenance.evaluation_authority_status != "BLOCKED":
        raise ValueError("P1.15B requires pre-authority evaluation status BLOCKED")
    if measurement_provenance.finding_status != "BLOCKED":
        raise ValueError("P1.15B requires upstream finding status BLOCKED")

    expected_measurement_ids = tuple(
        item.measurement_id for item in evaluation_submission.measurements
    )
    provenance_measurement_ids = tuple(
        item.measurement_id for item in measurement_provenance.derivations
    )
    if provenance_measurement_ids != expected_measurement_ids:
        raise ValueError("P1.15B measurement identities/order mismatch")


def reattest_experiment_evaluator_authority(
    evaluation_submission,
    measurement_provenance,
    record_path,
    receipt_path,
    *,
    expected_authority_id,
    expected_receipt_sha256,
) -> QualifiedExperimentEvaluationAuthority:
    """Verify externally pinned evaluator/method authority for one exact evaluation."""
    if type(evaluation_submission) is not ExperimentEvaluationSubmission:
        raise TypeError("P1.15B requires exact ExperimentEvaluationSubmission")
    if not is_factory_attested_experiment_evaluation_submission(evaluation_submission):
        raise ValueError("P1.15B requires currently-attested P1.13B evaluation")

    if type(measurement_provenance) is not WitnessedMeasurementProvenance:
        raise TypeError("P1.15B requires exact WitnessedMeasurementProvenance")
    if not is_factory_attested_witnessed_measurement_provenance(measurement_provenance):
        raise ValueError("P1.15B requires currently-attested P1.14B provenance")

    _validate_upstream_coherence(evaluation_submission, measurement_provenance)

    if not isinstance(record_path, (str, Path)) or not isinstance(receipt_path, (str, Path)):
        raise TypeError("P1.15B requires record and receipt paths")

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
        raise ValueError("P1.15B authority record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha256 = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha256, expected_pin):
        raise ValueError("P1.15B external receipt pin mismatch")

    receipt = _strict_json(receipt_bytes, label="evaluation authority receipt")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.15B receipt schema mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["contract_id"] != CONTRACT:
        raise ValueError("P1.15B receipt contract mismatch")
    if receipt["authority_id"] != expected_authority_id:
        raise ValueError("P1.15B authority expectation mismatch")

    nonce = receipt["qualification_nonce"]
    if (
        type(nonce) is not str
        or len(nonce) < 32
        or not nonce
        or not set(nonce) <= _HEX
    ):
        raise ValueError("P1.15B invalid qualification nonce")

    record_sha256 = _validate_sha256(receipt["record_sha256"], label="record_sha256")
    actual_record_sha256 = _sha256(record_bytes)
    if not secrets.compare_digest(actual_record_sha256, record_sha256):
        raise ValueError("P1.15B authority record integrity mismatch")

    record = _strict_json(record_bytes, label="evaluation authority record")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.15B record schema mismatch")
    if record["schema"] != RECORD_SCHEMA or record["contract_id"] != CONTRACT:
        raise ValueError("P1.15B record contract mismatch")

    expected_measurement_ids = [
        item.measurement_id for item in evaluation_submission.measurements
    ]
    expected_procedure_bindings = [
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
        "experiment_execution_result_id": evaluation_submission.experiment_execution_result_id,
        "experiment_spec_id": evaluation_submission.experiment_spec_id,
        "request_id": evaluation_submission.request_id,
        "evaluator_id": evaluation_submission.evaluator_id,
        "method_ref": evaluation_submission.method_ref,
        "prediction_status": evaluation_submission.prediction_status,
        "falsification_status": evaluation_submission.falsification_status,
        "evaluation_rationale": evaluation_submission.evaluation_rationale,
        "measurement_ids": expected_measurement_ids,
        "procedure_bindings": expected_procedure_bindings,
    }
    if record != expected_record:
        raise ValueError("P1.15B authority record does not match exact evaluation/provenance")

    if receipt["evaluation_submission_id"] != evaluation_submission.evaluation_submission_id:
        raise ValueError("P1.15B receipt evaluation mismatch")
    if receipt["provenance_qualification_id"] != measurement_provenance.provenance_qualification_id:
        raise ValueError("P1.15B receipt provenance mismatch")

    expected_qualification_id = _qualification_id(
        authority_id=expected_authority_id,
        qualification_nonce=nonce,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        provenance_qualification_id=measurement_provenance.provenance_qualification_id,
        record_sha256=record_sha256,
    )
    if receipt["qualification_id"] != expected_qualification_id:
        raise ValueError("P1.15B qualification identity mismatch")

    procedure_bindings = tuple(
        (item.measurement_id, item.procedure_ref, item.procedure_sha256)
        for item in measurement_provenance.derivations
    )

    return _attest_qualified_experiment_evaluation_authority(
        qualification_id=expected_qualification_id,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        provenance_qualification_id=measurement_provenance.provenance_qualification_id,
        experiment_execution_result_id=evaluation_submission.experiment_execution_result_id,
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
        measurement_ids=tuple(expected_measurement_ids),
        procedure_bindings=procedure_bindings,
        authority_id=expected_authority_id,
        record_sha256=record_sha256,
        receipt_sha256=actual_receipt_sha256,
        measurement_provenance_status="PASS",
        evaluation_authority_status="PASS",
        finding_status="BLOCKED",
        source_verdict=evaluation_submission.source_verdict,
        source_completeness_status=evaluation_submission.source_completeness_status,
        source_independence_status=evaluation_submission.source_independence_status,
    )
