"""P1.14B externally pinned witnessed measurement provenance re-attestation.

This boundary verifies a canonical external derivation record and receipt
against one exact P1.12B linked execution and one exact P1.13B evaluation.
It proves only witnessed lineage of the submitted measurement claims to the
exact execution stream and hashed procedures. It does not execute procedures,
recompute metrics, qualify evaluator authority, create findings/evidence, or
authorize operations.
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
from src.linked_experiment_execution import (
    LinkedExperimentExecutionResult,
    is_factory_attested_linked_experiment_execution_result,
)


CONTRACT = "P1_14B_WITNESSED_MEASUREMENT_PROVENANCE_REATTESTATION_BOUNDARY_V1"
RECORD_SCHEMA = "P1_14B_MEASUREMENT_DERIVATION_RECORD_V1"
RECEIPT_SCHEMA = "P1_14B_MEASUREMENT_DERIVATION_RECEIPT_V1"

_HEX = frozenset("0123456789abcdef")
_RECORD_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "evaluation_submission_id",
        "experiment_execution_result_id",
        "experiment_spec_id",
        "stream_sha256",
        "method_ref",
        "derivations",
    }
)
_RECEIPT_KEYS = frozenset(
    {
        "schema",
        "contract_id",
        "authority_id",
        "derivation_nonce",
        "evaluation_submission_id",
        "experiment_execution_result_id",
        "stream_sha256",
        "record_sha256",
        "provenance_qualification_id",
    }
)
_DERIVATION_KEYS = frozenset(
    {
        "measurement_id",
        "metric",
        "observed_value",
        "unit",
        "sample_size",
        "scope",
        "rationale",
        "procedure_ref",
        "procedure_sha256",
        "input_stream_sha256",
    }
)


@dataclass(frozen=True, slots=True)
class WitnessedMeasurementDerivation:
    measurement_id: str
    metric: str
    observed_value: str
    unit: str
    sample_size: int
    scope: str
    rationale: str
    procedure_ref: str
    procedure_sha256: str
    input_stream_sha256: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class WitnessedMeasurementProvenance:
    provenance_qualification_id: str
    evaluation_submission_id: str
    experiment_execution_result_id: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    stream_sha256: str
    method_ref: str
    derivations: tuple[WitnessedMeasurementDerivation, ...]
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


def _provenance_id(
    *,
    authority_id: str,
    derivation_nonce: str,
    evaluation_submission_id: str,
    experiment_execution_result_id: str,
    stream_sha256: str,
    record_sha256: str,
) -> str:
    payload = {
        "contract_id": CONTRACT,
        "authority_id": authority_id,
        "derivation_nonce": derivation_nonce,
        "evaluation_submission_id": evaluation_submission_id,
        "experiment_execution_result_id": experiment_execution_result_id,
        "stream_sha256": stream_sha256,
        "record_sha256": record_sha256,
    }
    return "WMP-" + _sha256(_canonical(payload))[:32]


def _fingerprint(value: WitnessedMeasurementProvenance) -> str:
    payload = asdict(value)
    payload["derivations"] = [asdict(item) for item in value.derivations]
    return _stable_hash({"contract": CONTRACT, "provenance": payload})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[WitnessedMeasurementProvenance], str],
    ] = {}

    def attest(**values: object) -> WitnessedMeasurementProvenance:
        produced = WitnessedMeasurementProvenance(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not WitnessedMeasurementProvenance:
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


_attest_witnessed_measurement_provenance, is_factory_attested_witnessed_measurement_provenance = _build_attestation_api()
del _build_attestation_api


def _validate_upstream_coherence(
    execution_result: LinkedExperimentExecutionResult,
    evaluation_submission: ExperimentEvaluationSubmission,
) -> None:
    pairs = (
        ("experiment_execution_result_id", execution_result.experiment_execution_result_id),
        ("experiment_execution_input_id", execution_result.experiment_execution_input_id),
        ("execution_binding_id", execution_result.execution_binding_id),
        ("experiment_spec_id", execution_result.experiment_spec_id),
        ("request_id", execution_result.request_id),
        ("revision_id", execution_result.revision_id),
        ("audit_id", execution_result.audit_id),
        ("scope_id", execution_result.scope_id),
        ("stream_sha256", execution_result.stream_sha256),
        ("source_verdict", execution_result.source_verdict),
        ("source_completeness_status", execution_result.source_completeness_status),
        ("source_independence_status", execution_result.source_independence_status),
    )
    for field_name, expected in pairs:
        if getattr(evaluation_submission, field_name) != expected:
            raise ValueError(f"P1.14B upstream mismatch: {field_name}")


def reattest_measurement_provenance(
    execution_result,
    evaluation_submission,
    record_path,
    receipt_path,
    *,
    expected_authority_id,
    expected_receipt_sha256,
) -> WitnessedMeasurementProvenance:
    """Verify one externally witnessed derivation lineage without executing it."""
    if type(execution_result) is not LinkedExperimentExecutionResult:
        raise TypeError("P1.14B requires exact LinkedExperimentExecutionResult")
    if not is_factory_attested_linked_experiment_execution_result(execution_result):
        raise ValueError("P1.14B requires currently-attested P1.12B execution result")

    if type(evaluation_submission) is not ExperimentEvaluationSubmission:
        raise TypeError("P1.14B requires exact ExperimentEvaluationSubmission")
    if not is_factory_attested_experiment_evaluation_submission(evaluation_submission):
        raise ValueError("P1.14B requires currently-attested P1.13B evaluation submission")

    _validate_upstream_coherence(execution_result, evaluation_submission)

    if not isinstance(record_path, (str, Path)) or not isinstance(receipt_path, (str, Path)):
        raise TypeError("P1.14B requires record and receipt paths")

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
        raise ValueError("P1.14B derivation record/receipt missing")

    record_bytes = record_file.read_bytes()
    receipt_bytes = receipt_file.read_bytes()
    actual_receipt_sha256 = _sha256(receipt_bytes)
    if not secrets.compare_digest(actual_receipt_sha256, expected_pin):
        raise ValueError("P1.14B external receipt pin mismatch")

    receipt = _strict_json(receipt_bytes, label="measurement receipt")
    if set(receipt) != _RECEIPT_KEYS:
        raise ValueError("P1.14B receipt schema mismatch")
    if receipt["schema"] != RECEIPT_SCHEMA or receipt["contract_id"] != CONTRACT:
        raise ValueError("P1.14B receipt contract mismatch")
    if receipt["authority_id"] != expected_authority_id:
        raise ValueError("P1.14B authority expectation mismatch")

    nonce = receipt["derivation_nonce"]
    if (
        type(nonce) is not str
        or len(nonce) < 32
        or not nonce
        or not set(nonce) <= _HEX
    ):
        raise ValueError("P1.14B invalid derivation nonce")

    record_sha256 = _validate_sha256(receipt["record_sha256"], label="record_sha256")
    actual_record_sha256 = _sha256(record_bytes)
    if not secrets.compare_digest(actual_record_sha256, record_sha256):
        raise ValueError("P1.14B derivation record integrity mismatch")

    record = _strict_json(record_bytes, label="measurement derivation record")
    if set(record) != _RECORD_KEYS:
        raise ValueError("P1.14B record schema mismatch")
    if record["schema"] != RECORD_SCHEMA or record["contract_id"] != CONTRACT:
        raise ValueError("P1.14B record contract mismatch")
    if record["evaluation_submission_id"] != evaluation_submission.evaluation_submission_id:
        raise ValueError("P1.14B record evaluation submission mismatch")
    if record["experiment_execution_result_id"] != execution_result.experiment_execution_result_id:
        raise ValueError("P1.14B record execution result mismatch")
    if record["experiment_spec_id"] != execution_result.experiment_spec_id:
        raise ValueError("P1.14B record experiment specification mismatch")
    if record["stream_sha256"] != execution_result.stream_sha256:
        raise ValueError("P1.14B record stream mismatch")
    if record["method_ref"] != evaluation_submission.method_ref:
        raise ValueError("P1.14B record method mismatch")

    derivations_raw = record["derivations"]
    if type(derivations_raw) is not list:
        raise ValueError("P1.14B derivations must be a JSON array")
    if len(derivations_raw) != len(evaluation_submission.measurements):
        raise ValueError("P1.14B derivations must match measurement claims exactly")

    derivations: list[WitnessedMeasurementDerivation] = []
    for raw, claim in zip(derivations_raw, evaluation_submission.measurements):
        if type(raw) is not dict or set(raw) != _DERIVATION_KEYS:
            raise ValueError("P1.14B derivation schema mismatch")

        expected_claim = {
            "measurement_id": claim.measurement_id,
            "metric": claim.metric,
            "observed_value": claim.observed_value,
            "unit": claim.unit,
            "sample_size": claim.sample_size,
            "scope": claim.scope,
            "rationale": claim.rationale,
        }
        actual_claim = {key: raw[key] for key in expected_claim}
        if actual_claim != expected_claim:
            raise ValueError("P1.14B derivation claim mismatch")

        procedure_ref = _validate_nonempty_str(raw["procedure_ref"], label="procedure_ref")
        procedure_sha256 = _validate_sha256(raw["procedure_sha256"], label="procedure_sha256")
        input_stream_sha256 = _validate_sha256(
            raw["input_stream_sha256"],
            label="input_stream_sha256",
        )
        if input_stream_sha256 != execution_result.stream_sha256:
            raise ValueError("P1.14B derivation input stream mismatch")

        derivations.append(
            WitnessedMeasurementDerivation(
                measurement_id=claim.measurement_id,
                metric=claim.metric,
                observed_value=claim.observed_value,
                unit=claim.unit,
                sample_size=claim.sample_size,
                scope=claim.scope,
                rationale=claim.rationale,
                procedure_ref=procedure_ref,
                procedure_sha256=procedure_sha256,
                input_stream_sha256=input_stream_sha256,
            )
        )

    if receipt["evaluation_submission_id"] != evaluation_submission.evaluation_submission_id:
        raise ValueError("P1.14B receipt evaluation mismatch")
    if receipt["experiment_execution_result_id"] != execution_result.experiment_execution_result_id:
        raise ValueError("P1.14B receipt execution mismatch")
    if receipt["stream_sha256"] != execution_result.stream_sha256:
        raise ValueError("P1.14B receipt stream mismatch")

    expected_provenance_id = _provenance_id(
        authority_id=expected_authority_id,
        derivation_nonce=nonce,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        experiment_execution_result_id=execution_result.experiment_execution_result_id,
        stream_sha256=execution_result.stream_sha256,
        record_sha256=record_sha256,
    )
    if receipt["provenance_qualification_id"] != expected_provenance_id:
        raise ValueError("P1.14B provenance qualification identity mismatch")

    return _attest_witnessed_measurement_provenance(
        provenance_qualification_id=expected_provenance_id,
        evaluation_submission_id=evaluation_submission.evaluation_submission_id,
        experiment_execution_result_id=execution_result.experiment_execution_result_id,
        experiment_execution_input_id=execution_result.experiment_execution_input_id,
        execution_binding_id=execution_result.execution_binding_id,
        experiment_spec_id=execution_result.experiment_spec_id,
        request_id=execution_result.request_id,
        revision_id=execution_result.revision_id,
        audit_id=execution_result.audit_id,
        scope_id=execution_result.scope_id,
        stream_sha256=execution_result.stream_sha256,
        method_ref=evaluation_submission.method_ref,
        derivations=tuple(derivations),
        authority_id=expected_authority_id,
        record_sha256=record_sha256,
        receipt_sha256=actual_receipt_sha256,
        measurement_provenance_status="PASS",
        evaluation_authority_status="BLOCKED",
        finding_status="BLOCKED",
        source_verdict=execution_result.source_verdict,
        source_completeness_status=execution_result.source_completeness_status,
        source_independence_status=execution_result.source_independence_status,
    )
