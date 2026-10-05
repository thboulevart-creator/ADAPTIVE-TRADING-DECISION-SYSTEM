"""P1.14C common witnessed measurement-provenance re-attestation.

Verifies an externally pinned canonical derivation record/receipt against one
exact P1.12D execution-evidence envelope and one exact P1.13C evaluation. It
does not execute the procedure, create evaluator authority, findings, or
operational authority.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import weakref
from dataclasses import asdict, dataclass
from pathlib import Path

from src.p1_12d_qualified_execution_evidence import (
    QualifiedExecutionEvidenceEnvelope,
    is_factory_attested_qualified_execution_evidence,
)
from src.p1_13c_common_evaluation import (
    CommonExperimentEvaluationSubmission,
    is_factory_attested_common_experiment_evaluation,
)

CONTRACT = "P1_14C_COMMON_WITNESSED_MEASUREMENT_PROVENANCE_V1"
RECORD_SCHEMA = "P1_14C_COMMON_MEASUREMENT_DERIVATION_RECORD_V1"
RECEIPT_SCHEMA = "P1_14C_COMMON_MEASUREMENT_DERIVATION_RECEIPT_V1"
_HEX = frozenset("0123456789abcdef")

_RECORD_KEYS = frozenset({
    "schema","contract_id","evaluation_submission_id","execution_evidence_envelope_id",
    "native_result_id","experiment_spec_id","measurement_input_identity","method_ref","derivations",
})
_RECEIPT_KEYS = frozenset({
    "schema","contract_id","authority_id","derivation_nonce","evaluation_submission_id",
    "execution_evidence_envelope_id","native_result_id","measurement_input_identity",
    "record_sha256","provenance_qualification_id",
})
_DERIVATION_KEYS = frozenset({
    "measurement_id","metric","observed_value","unit","sample_size","scope","rationale",
    "execution_evidence_envelope_id","native_result_id","measurement_input_identity",
    "procedure_ref","procedure_sha256",
})


@dataclass(frozen=True, slots=True)
class CommonWitnessedMeasurementDerivation:
    measurement_id: str
    metric: str
    observed_value: str
    unit: str
    sample_size: int
    scope: str
    rationale: str
    execution_evidence_envelope_id: str
    native_result_id: str
    measurement_input_identity: str
    procedure_ref: str
    procedure_sha256: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CommonWitnessedMeasurementProvenance:
    provenance_qualification_id: str
    evaluation_submission_id: str
    execution_evidence_envelope_id: str
    execution_owner_id: str
    native_result_id: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    experiment_definition_digest: str
    measurement_input_identity: str
    method_ref: str
    derivations: tuple[CommonWitnessedMeasurementDerivation, ...]
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


def _provenance_id(
    *,
    authority_id: str,
    derivation_nonce: str,
    evaluation_submission_id: str,
    execution_evidence_envelope_id: str,
    native_result_id: str,
    measurement_input_identity: str,
    record_sha256: str,
) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "derivation_nonce": derivation_nonce,
        "evaluation_submission_id": evaluation_submission_id,
        "execution_evidence_envelope_id": execution_evidence_envelope_id,
        "native_result_id": native_result_id,
        "measurement_input_identity": measurement_input_identity,
        "record_sha256": record_sha256,
    }
    return "CWMP-" + _sha256(_canonical(payload))[:32]


def _fingerprint(value: CommonWitnessedMeasurementProvenance) -> str:
    payload = asdict(value)
    payload["derivations"] = [asdict(item) for item in value.derivations]
    return _stable({"contract": CONTRACT, "provenance": payload})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[CommonWitnessedMeasurementProvenance], str]] = {}

    def attest(**values: object) -> CommonWitnessedMeasurementProvenance:
        produced = CommonWitnessedMeasurementProvenance(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not CommonWitnessedMeasurementProvenance:
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


_attest, is_factory_attested_common_measurement_provenance = _build_attestation_api()
del _build_attestation_api


_PROVENANCE_REJECTIONS = {
    "RESULT_IDENTITY_AS_PROVENANCE": ("REJECTED", "REJECT_RESULT_IDENTITY_AS_PROVENANCE"),
    "WRONG_NATIVE_RESULT": ("BLOCKED", "BLOCKED_PROVENANCE_RESULT_MISMATCH"),
    "WRONG_MEASUREMENT_INPUT": ("BLOCKED", "BLOCKED_MEASUREMENT_INPUT_IDENTITY_MISMATCH"),
}


def validate_common_provenance_claim(claim: str) -> dict[str, object]:
    if claim not in _PROVENANCE_REJECTIONS:
        return {"contract": CONTRACT, "status": "READY", "reason": "NO_PROVENANCE_LAUNDERING"}
    status, reason = _PROVENANCE_REJECTIONS[claim]
    return {"contract": CONTRACT, "status": status, "reason": reason}


def _validate_upstream(
    envelope: QualifiedExecutionEvidenceEnvelope,
    evaluation: CommonExperimentEvaluationSubmission,
) -> None:
    pairs = (
        ("execution_evidence_envelope_id", envelope.execution_evidence_envelope_id),
        ("execution_owner_id", envelope.execution_owner_id),
        ("native_result_id", envelope.native_result_id),
        ("experiment_execution_input_id", envelope.experiment_execution_input_id),
        ("execution_binding_id", envelope.execution_binding_id),
        ("experiment_spec_id", envelope.experiment_spec_id),
        ("request_id", envelope.request_id),
        ("revision_id", envelope.revision_id),
        ("audit_id", envelope.audit_id),
        ("scope_id", envelope.scope_id),
        ("experiment_definition_digest", envelope.experiment_definition_digest),
        ("measurement_input_identity", envelope.measurement_input_identity),
        ("native_execution_status", envelope.native_execution_status),
    )
    for field, expected in pairs:
        if getattr(evaluation, field) != expected:
            raise ValueError(f"P1.14C upstream mismatch: {field}")


def reattest_common_measurement_provenance(
    execution_evidence,
    evaluation_submission,
    record_path,
    receipt_path,
    *,
    expected_authority_id,
    expected_receipt_sha256,
) -> CommonWitnessedMeasurementProvenance:
    if type(execution_evidence) is not QualifiedExecutionEvidenceEnvelope:
        raise TypeError("P1.14C requires exact QualifiedExecutionEvidenceEnvelope")
    if not is_factory_attested_qualified_execution_evidence(execution_evidence):
        raise ValueError("P1.14C requires currently-attested P1.12D envelope")
    if type(evaluation_submission) is not CommonExperimentEvaluationSubmission:
        raise TypeError("P1.14C requires exact CommonExperimentEvaluationSubmission")
    if not is_factory_attested_common_experiment_evaluation(evaluation_submission):
        raise ValueError("P1.14C requires currently-attested P1.13C evaluation")

    _validate_upstream(execution_evidence, evaluation_submission)

    authority_id = _nonempty(expected_authority_id, label="expected_authority_id")
    expected_pin = _sha(expected_receipt_sha256, label="expected_receipt_sha256")
    record_file = Path(record_path)
    receipt_file = Path(receipt_path)
    if not record_file.is_file() or not receipt_file.is_file():
        raise ValueError("P1.14C record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha, expected_pin):
        raise ValueError("P1.14C receipt pin mismatch")

    record = _strict_json(record_bytes, label="common measurement record")
    receipt = _strict_json(receipt_bytes, label="common measurement receipt")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.14C record schema mismatch")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.14C receipt schema mismatch")
    if record["schema"] != RECORD_SCHEMA or record["contract_id"] != CONTRACT:
        raise ValueError("P1.14C record contract mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["contract_id"] != CONTRACT:
        raise ValueError("P1.14C receipt contract mismatch")
    if receipt["authority_id"] != authority_id:
        raise ValueError("P1.14C authority mismatch")

    nonce = receipt["derivation_nonce"]
    if type(nonce) is not str or len(nonce) < 32 or not set(nonce) <= _HEX:
        raise ValueError("P1.14C invalid derivation nonce")

    record_sha = _sha(receipt["record_sha256"], label="record_sha256")
    if not secrets.compare_digest(record_sha, _sha256(record_bytes)):
        raise ValueError("P1.14C record integrity mismatch")

    expected_top = {
        "evaluation_submission_id": evaluation_submission.evaluation_submission_id,
        "execution_evidence_envelope_id": execution_evidence.execution_evidence_envelope_id,
        "native_result_id": execution_evidence.native_result_id,
        "experiment_spec_id": execution_evidence.experiment_spec_id,
        "measurement_input_identity": execution_evidence.measurement_input_identity,
        "method_ref": evaluation_submission.method_ref,
    }
    for key, expected in expected_top.items():
        if record[key] != expected:
            raise ValueError(f"P1.14C record mismatch: {key}")

    raws = record["derivations"]
    if type(raws) is not list or len(raws) != len(evaluation_submission.measurements):
        raise ValueError("P1.14C derivations must exactly match measurement count")

    derivations = []
    for raw, claim in zip(raws, evaluation_submission.measurements):
        if type(raw) is not dict or set(raw) != _DERIVATION_KEYS:
            raise ValueError("P1.14C derivation schema mismatch")
        expected_claim = {
            "measurement_id": claim.measurement_id,
            "metric": claim.metric,
            "observed_value": claim.observed_value,
            "unit": claim.unit,
            "sample_size": claim.sample_size,
            "scope": claim.scope,
            "rationale": claim.rationale,
        }
        for key, expected in expected_claim.items():
            if raw[key] != expected:
                raise ValueError(f"P1.14C derivation claim mismatch: {key}")
        if raw["execution_evidence_envelope_id"] != execution_evidence.execution_evidence_envelope_id:
            raise ValueError("P1.14C derivation envelope mismatch")
        if raw["native_result_id"] != execution_evidence.native_result_id:
            raise ValueError("P1.14C derivation native result mismatch")
        if raw["measurement_input_identity"] != execution_evidence.measurement_input_identity:
            raise ValueError("P1.14C derivation measurement input mismatch")
        procedure_ref = _nonempty(raw["procedure_ref"], label="procedure_ref")
        procedure_sha = _sha(raw["procedure_sha256"], label="procedure_sha256")
        derivations.append(CommonWitnessedMeasurementDerivation(
            measurement_id=claim.measurement_id,
            metric=claim.metric,
            observed_value=claim.observed_value,
            unit=claim.unit,
            sample_size=claim.sample_size,
            scope=claim.scope,
            rationale=claim.rationale,
            execution_evidence_envelope_id=execution_evidence.execution_evidence_envelope_id,
            native_result_id=execution_evidence.native_result_id,
            measurement_input_identity=execution_evidence.measurement_input_identity,
            procedure_ref=procedure_ref,
            procedure_sha256=procedure_sha,
        ))

    for key in ("evaluation_submission_id","execution_evidence_envelope_id","native_result_id","measurement_input_identity"):
        if receipt[key] != expected_top[key]:
            raise ValueError(f"P1.14C receipt mismatch: {key}")

    expected_id = _provenance_id(
        authority_id=authority_id,
        derivation_nonce=nonce,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        execution_evidence_envelope_id=execution_evidence.execution_evidence_envelope_id,
        native_result_id=execution_evidence.native_result_id,
        measurement_input_identity=execution_evidence.measurement_input_identity,
        record_sha256=record_sha,
    )
    if receipt["provenance_qualification_id"] != expected_id:
        raise ValueError("P1.14C provenance identity mismatch")

    return _attest(
        provenance_qualification_id=expected_id,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        execution_evidence_envelope_id=execution_evidence.execution_evidence_envelope_id,
        execution_owner_id=execution_evidence.execution_owner_id,
        native_result_id=execution_evidence.native_result_id,
        experiment_execution_input_id=execution_evidence.experiment_execution_input_id,
        execution_binding_id=execution_evidence.execution_binding_id,
        experiment_spec_id=execution_evidence.experiment_spec_id,
        request_id=execution_evidence.request_id,
        revision_id=execution_evidence.revision_id,
        audit_id=execution_evidence.audit_id,
        scope_id=execution_evidence.scope_id,
        experiment_definition_digest=execution_evidence.experiment_definition_digest,
        measurement_input_identity=execution_evidence.measurement_input_identity,
        method_ref=evaluation_submission.method_ref,
        derivations=tuple(derivations),
        authority_id=authority_id,
        record_sha256=record_sha,
        receipt_sha256=actual_receipt_sha,
        measurement_provenance_status="PASS",
        evaluation_authority_status="BLOCKED",
        finding_status="BLOCKED",
        scientific_authority=False,
        operational_authority=False,
        trading_authority=False,
        capital_authority=False,
    )
