"""P1.13B experiment evaluation submission boundary.

This module records explicit measurement and evaluation claims against one
exact P1.12B linked execution result. It does not prove that submitted
measurements derive from the execution stream and does not establish evaluator
authority, findings, evidence, knowledge, or operational authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass
from datetime import datetime

from src.linked_experiment_execution import (
    LinkedExperimentExecutionResult,
    is_factory_attested_linked_experiment_execution_result,
)


CONTRACT = "P1_13B_EXPERIMENT_EVALUATION_SUBMISSION_BOUNDARY_V1"

_PREDICTION_STATUSES = {"SUPPORTED", "NOT_SUPPORTED", "BLOCKED"}
_FALSIFICATION_STATUSES = {"FALSIFIED", "NOT_FALSIFIED", "BLOCKED"}
_MEASUREMENT_PROVENANCE_STATUS = "BLOCKED"
_EVALUATION_AUTHORITY_STATUS = "BLOCKED"


@dataclass(frozen=True, slots=True)
class ExperimentMeasurementClaim:
    measurement_id: str
    metric: str
    observed_value: str
    unit: str
    sample_size: int
    scope: str
    rationale: str


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ExperimentEvaluationSubmission:
    evaluation_submission_id: str
    experiment_execution_result_id: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    objective: str
    hypothesis_statement: str
    prediction: str
    falsification_rule: str
    protocol: str
    measurement_plan: str
    corpus_root: str
    contract_path: str
    expected_corpus_hash: str
    expected_contract_hash: str
    files_consumed: int
    ticks_consumed: int
    first_timestamp: datetime | None
    last_timestamp: datetime | None
    stream_sha256: str
    measurements: tuple[ExperimentMeasurementClaim, ...]
    prediction_status: str
    falsification_status: str
    evaluation_rationale: str
    evaluator_id: str
    method_ref: str
    measurement_provenance_status: str
    evaluation_authority_status: str
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


def _identity_payload(values: dict[str, object]) -> dict[str, object]:
    payload = dict(values)
    first_timestamp = payload.get("first_timestamp")
    last_timestamp = payload.get("last_timestamp")
    if isinstance(first_timestamp, datetime):
        payload["first_timestamp"] = first_timestamp.isoformat()
    if isinstance(last_timestamp, datetime):
        payload["last_timestamp"] = last_timestamp.isoformat()
    measurements = payload.get("measurements")
    if type(measurements) is tuple:
        payload["measurements"] = [asdict(item) for item in measurements]
    return {"contract": CONTRACT, **payload}


def _submission_id(**values: object) -> str:
    return "EES-" + _stable_hash(_identity_payload(values))[:32]


def _fingerprint(value: ExperimentEvaluationSubmission) -> str:
    values = {
        "evaluation_submission_id": value.evaluation_submission_id,
        "experiment_execution_result_id": value.experiment_execution_result_id,
        "experiment_execution_input_id": value.experiment_execution_input_id,
        "execution_binding_id": value.execution_binding_id,
        "experiment_spec_id": value.experiment_spec_id,
        "request_id": value.request_id,
        "revision_id": value.revision_id,
        "audit_id": value.audit_id,
        "scope_id": value.scope_id,
        "objective": value.objective,
        "hypothesis_statement": value.hypothesis_statement,
        "prediction": value.prediction,
        "falsification_rule": value.falsification_rule,
        "protocol": value.protocol,
        "measurement_plan": value.measurement_plan,
        "corpus_root": value.corpus_root,
        "contract_path": value.contract_path,
        "expected_corpus_hash": value.expected_corpus_hash,
        "expected_contract_hash": value.expected_contract_hash,
        "files_consumed": value.files_consumed,
        "ticks_consumed": value.ticks_consumed,
        "first_timestamp": value.first_timestamp,
        "last_timestamp": value.last_timestamp,
        "stream_sha256": value.stream_sha256,
        "measurements": value.measurements,
        "prediction_status": value.prediction_status,
        "falsification_status": value.falsification_status,
        "evaluation_rationale": value.evaluation_rationale,
        "evaluator_id": value.evaluator_id,
        "method_ref": value.method_ref,
        "measurement_provenance_status": value.measurement_provenance_status,
        "evaluation_authority_status": value.evaluation_authority_status,
        "source_verdict": value.source_verdict,
        "source_completeness_status": value.source_completeness_status,
        "source_independence_status": value.source_independence_status,
    }
    return _stable_hash(_identity_payload(values))


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[ExperimentEvaluationSubmission], str],
    ] = {}

    def attest(**values: object) -> ExperimentEvaluationSubmission:
        produced = ExperimentEvaluationSubmission(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not ExperimentEvaluationSubmission:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_experiment_evaluation_submission, is_factory_attested_experiment_evaluation_submission = _build_attestation_api()
del _build_attestation_api


def _require_nonempty_exact_str(label: str, value: object) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty after strip")
    return value


def _validate_measurements(measurements: object) -> tuple[ExperimentMeasurementClaim, ...]:
    if type(measurements) is not tuple:
        raise TypeError("measurements must be exact tuple")
    if not measurements:
        raise ValueError("measurements must be nonempty")

    seen_ids: set[str] = set()
    normalized: list[ExperimentMeasurementClaim] = []
    for measurement in measurements:
        if type(measurement) is not ExperimentMeasurementClaim:
            raise TypeError("measurements items must be exact ExperimentMeasurementClaim")

        measurement_id = _require_nonempty_exact_str("measurement_id", measurement.measurement_id)
        metric = _require_nonempty_exact_str("metric", measurement.metric)
        observed_value = _require_nonempty_exact_str("observed_value", measurement.observed_value)
        unit = _require_nonempty_exact_str("unit", measurement.unit)
        scope = _require_nonempty_exact_str("scope", measurement.scope)
        rationale = _require_nonempty_exact_str("measurement rationale", measurement.rationale)

        if type(measurement.sample_size) is not int:
            raise TypeError("sample_size must be exact int")
        if measurement.sample_size <= 0:
            raise ValueError("sample_size must be positive")

        if measurement_id in seen_ids:
            raise ValueError("measurement_id must be unique")
        seen_ids.add(measurement_id)

        normalized.append(
            ExperimentMeasurementClaim(
                measurement_id=measurement_id,
                metric=metric,
                observed_value=observed_value,
                unit=unit,
                sample_size=measurement.sample_size,
                scope=scope,
                rationale=rationale,
            )
        )

    return tuple(normalized)


def submit_experiment_evaluation(
    execution_result,
    *,
    evaluator_id,
    method_ref,
    measurements,
    prediction_status,
    falsification_status,
    evaluation_rationale,
) -> ExperimentEvaluationSubmission:
    """Record bounded evaluation claims without promoting them to findings."""
    if type(execution_result) is not LinkedExperimentExecutionResult:
        raise TypeError("P1.13B requires exact LinkedExperimentExecutionResult")
    if not is_factory_attested_linked_experiment_execution_result(execution_result):
        raise ValueError("P1.13B requires currently-attested P1.12B result")

    evaluator_id = _require_nonempty_exact_str("evaluator_id", evaluator_id)
    method_ref = _require_nonempty_exact_str("method_ref", method_ref)
    evaluation_rationale = _require_nonempty_exact_str(
        "evaluation_rationale",
        evaluation_rationale,
    )

    if type(prediction_status) is not str:
        raise TypeError("prediction_status must be exact str")
    if prediction_status not in _PREDICTION_STATUSES:
        raise ValueError("invalid prediction_status")

    if type(falsification_status) is not str:
        raise TypeError("falsification_status must be exact str")
    if falsification_status not in _FALSIFICATION_STATUSES:
        raise ValueError("invalid falsification_status")

    measurements = _validate_measurements(measurements)

    values = {
        "experiment_execution_result_id": execution_result.experiment_execution_result_id,
        "experiment_execution_input_id": execution_result.experiment_execution_input_id,
        "execution_binding_id": execution_result.execution_binding_id,
        "experiment_spec_id": execution_result.experiment_spec_id,
        "request_id": execution_result.request_id,
        "revision_id": execution_result.revision_id,
        "audit_id": execution_result.audit_id,
        "scope_id": execution_result.scope_id,
        "objective": execution_result.objective,
        "hypothesis_statement": execution_result.hypothesis_statement,
        "prediction": execution_result.prediction,
        "falsification_rule": execution_result.falsification_rule,
        "protocol": execution_result.protocol,
        "measurement_plan": execution_result.measurement_plan,
        "corpus_root": execution_result.corpus_root,
        "contract_path": execution_result.contract_path,
        "expected_corpus_hash": execution_result.expected_corpus_hash,
        "expected_contract_hash": execution_result.expected_contract_hash,
        "files_consumed": execution_result.files_consumed,
        "ticks_consumed": execution_result.ticks_consumed,
        "first_timestamp": execution_result.first_timestamp,
        "last_timestamp": execution_result.last_timestamp,
        "stream_sha256": execution_result.stream_sha256,
        "measurements": measurements,
        "prediction_status": prediction_status,
        "falsification_status": falsification_status,
        "evaluation_rationale": evaluation_rationale,
        "evaluator_id": evaluator_id,
        "method_ref": method_ref,
        "measurement_provenance_status": _MEASUREMENT_PROVENANCE_STATUS,
        "evaluation_authority_status": _EVALUATION_AUTHORITY_STATUS,
        "source_verdict": execution_result.source_verdict,
        "source_completeness_status": execution_result.source_completeness_status,
        "source_independence_status": execution_result.source_independence_status,
    }
    return _attest_experiment_evaluation_submission(
        evaluation_submission_id=_submission_id(**values),
        **values,
    )
