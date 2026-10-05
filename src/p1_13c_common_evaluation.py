"""P1.13C common experiment evaluation submission boundary.

Consumes one exact P1.12D execution-evidence envelope plus the exact attested
P1.11B experiment input. It records evaluation claims only. It does not prove
measurement derivation, create evaluator authority, findings, or operations.
"""
from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass
from typing import Any

from src.p1_12d_qualified_execution_evidence import (
    QualifiedExecutionEvidenceEnvelope,
    is_factory_attested_qualified_execution_evidence,
)
from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
)

CONTRACT = "P1_13C_COMMON_EXPERIMENT_EVALUATION_SUBMISSION_V1"
_PREDICTION_STATUSES = {"SUPPORTED", "NOT_SUPPORTED", "BLOCKED"}
_FALSIFICATION_STATUSES = {"FALSIFIED", "NOT_FALSIFIED", "BLOCKED"}


@dataclass(frozen=True, slots=True)
class CommonExperimentMeasurementClaim:
    measurement_id: str
    metric: str
    observed_value: str
    unit: str
    sample_size: int
    scope: str
    rationale: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CommonExperimentEvaluationSubmission:
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
    objective: str
    hypothesis_statement: str
    prediction: str
    falsification_rule: str
    protocol: str
    measurement_plan: str
    measurement_input_identity: str
    native_execution_status: str
    measurements: tuple[CommonExperimentMeasurementClaim, ...]
    prediction_status: str
    falsification_status: str
    evaluation_rationale: str
    evaluator_id: str
    method_ref: str
    measurement_provenance_status: str
    evaluation_authority_status: str
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _decision(status: str, reason: str) -> dict[str, object]:
    return {"contract": CONTRACT, "status": status, "reason": reason}


def _experiment_definition_digest(qei: QualifiedExperimentExecutionInput) -> str:
    return _digest({
        "contract": "P1_EXPERIMENT_DEFINITION_DIGEST_V1",
        "experiment_execution_input_id": qei.experiment_execution_input_id,
        "experiment_spec_id": qei.experiment_spec_id,
        "objective": qei.objective,
        "hypothesis_statement": qei.hypothesis_statement,
        "prediction": qei.prediction,
        "falsification_rule": qei.falsification_rule,
        "protocol": qei.protocol,
        "measurement_plan": qei.measurement_plan,
    })


def _fingerprint(value: CommonExperimentEvaluationSubmission) -> str:
    payload = asdict(value)
    payload["measurements"] = [asdict(item) for item in value.measurements]
    return _digest({"contract": CONTRACT, "submission": payload})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[CommonExperimentEvaluationSubmission], str]] = {}

    def attest(**values: object) -> CommonExperimentEvaluationSubmission:
        produced = CommonExperimentEvaluationSubmission(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not CommonExperimentEvaluationSubmission:
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


_attest, is_factory_attested_common_experiment_evaluation = _build_attestation_api()
del _build_attestation_api


_EVALUATION_REJECTIONS = {
    "EXECUTED_TO_SUPPORTED": ("REJECTED", "REJECT_EXECUTION_TO_SUPPORT_LAUNDERING"),
    "MISSING_EXECUTION_ENVELOPE": ("BLOCKED", "BLOCKED_EVALUATION_EXECUTION_BINDING_REQUIRED"),
    "OWNER_SPECIFIC_DUPLICATE_CHAIN": ("REJECTED", "REJECT_OWNER_SPECIFIC_DOWNSTREAM_DUPLICATION"),
}


def validate_common_evaluation_claim(claim: str) -> dict[str, object]:
    if claim not in _EVALUATION_REJECTIONS:
        return _decision("READY", "NO_EVALUATION_LAUNDERING")
    status, reason = _EVALUATION_REJECTIONS[claim]
    return _decision(status, reason)


def _nonempty(label: str, value: object) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty")
    return value


def _measurements(value: object) -> tuple[CommonExperimentMeasurementClaim, ...]:
    if type(value) is not tuple or not value:
        raise ValueError("P1.13C measurements must be nonempty exact tuple")
    seen = set()
    out = []
    for item in value:
        if type(item) is not CommonExperimentMeasurementClaim:
            raise TypeError("P1.13C measurement item type mismatch")
        for label in ("measurement_id","metric","observed_value","unit","scope","rationale"):
            _nonempty(label, getattr(item, label))
        if type(item.sample_size) is not int or item.sample_size <= 0:
            raise ValueError("P1.13C sample_size must be positive exact int")
        if item.measurement_id in seen:
            raise ValueError("P1.13C duplicate measurement_id")
        seen.add(item.measurement_id)
        out.append(item)
    return tuple(out)


def submit_common_experiment_evaluation(
    execution_evidence,
    qualified_input,
    *,
    evaluator_id,
    method_ref,
    measurements,
    prediction_status,
    falsification_status,
    evaluation_rationale,
) -> CommonExperimentEvaluationSubmission:
    if type(execution_evidence) is not QualifiedExecutionEvidenceEnvelope:
        raise TypeError("P1.13C requires exact QualifiedExecutionEvidenceEnvelope")
    if not is_factory_attested_qualified_execution_evidence(execution_evidence):
        raise ValueError("P1.13C requires currently-attested P1.12D envelope")
    if type(qualified_input) is not QualifiedExperimentExecutionInput:
        raise TypeError("P1.13C requires exact QualifiedExperimentExecutionInput")
    if not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise ValueError("P1.13C requires currently-attested P1.11B input")

    for name in (
        "experiment_execution_input_id","execution_binding_id","experiment_spec_id",
        "request_id","revision_id","audit_id","scope_id"
    ):
        if getattr(execution_evidence, name) != getattr(qualified_input, name):
            raise ValueError(f"P1.13C envelope/input mismatch: {name}")
    if execution_evidence.experiment_definition_digest != _experiment_definition_digest(qualified_input):
        raise ValueError("P1.13C experiment definition mismatch")

    evaluator_id = _nonempty("evaluator_id", evaluator_id)
    method_ref = _nonempty("method_ref", method_ref)
    evaluation_rationale = _nonempty("evaluation_rationale", evaluation_rationale)
    if prediction_status not in _PREDICTION_STATUSES:
        raise ValueError("P1.13C invalid prediction_status")
    if falsification_status not in _FALSIFICATION_STATUSES:
        raise ValueError("P1.13C invalid falsification_status")
    claims = _measurements(measurements)

    values = {
        "execution_evidence_envelope_id": execution_evidence.execution_evidence_envelope_id,
        "execution_owner_id": execution_evidence.execution_owner_id,
        "native_result_id": execution_evidence.native_result_id,
        "experiment_execution_input_id": execution_evidence.experiment_execution_input_id,
        "execution_binding_id": execution_evidence.execution_binding_id,
        "experiment_spec_id": execution_evidence.experiment_spec_id,
        "request_id": execution_evidence.request_id,
        "revision_id": execution_evidence.revision_id,
        "audit_id": execution_evidence.audit_id,
        "scope_id": execution_evidence.scope_id,
        "experiment_definition_digest": execution_evidence.experiment_definition_digest,
        "objective": qualified_input.objective,
        "hypothesis_statement": qualified_input.hypothesis_statement,
        "prediction": qualified_input.prediction,
        "falsification_rule": qualified_input.falsification_rule,
        "protocol": qualified_input.protocol,
        "measurement_plan": qualified_input.measurement_plan,
        "measurement_input_identity": execution_evidence.measurement_input_identity,
        "native_execution_status": execution_evidence.native_execution_status,
        "measurements": claims,
        "prediction_status": prediction_status,
        "falsification_status": falsification_status,
        "evaluation_rationale": evaluation_rationale,
        "evaluator_id": evaluator_id,
        "method_ref": method_ref,
        "measurement_provenance_status": "BLOCKED",
        "evaluation_authority_status": "BLOCKED",
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    submission_id = "CEE-" + _digest({
        "contract": CONTRACT,
        "submission": {
            **{k:v for k,v in values.items() if k != "measurements"},
            "measurements":[asdict(item) for item in claims],
        },
    })[:32]
    return _attest(evaluation_submission_id=submission_id, **values)
