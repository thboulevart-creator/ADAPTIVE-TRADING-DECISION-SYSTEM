"""P1.16 qualified experimental finding interpretation boundary.

Consumes one exact P1.13B experiment evaluation submission and one exact
P1.15B qualified evaluation authority, verifies their coherence, and applies
the fixed P1.16 interpretation policy. This boundary creates only a qualified
experimental finding snapshot. It does not create research containers,
durable knowledge, decision authority, or operational authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.experiment_evaluation_submission import (
    ExperimentEvaluationSubmission,
    is_factory_attested_experiment_evaluation_submission,
)
from src.experiment_evaluator_authority import (
    QualifiedExperimentEvaluationAuthority,
    is_factory_attested_qualified_experiment_evaluation_authority,
)


CONTRACT = "P1_16_QUALIFIED_EXPERIMENTAL_FINDING_INTERPRETATION_BOUNDARY_V1"
POLICY = "P1_16_FINDING_INTERPRETATION_POLICY_V1"

_INTERPRETATION_TABLE = {
    ("SUPPORTED", "NOT_FALSIFIED"): (
        "SUPPORTED",
        "PREDICTION_SUPPORTED_AND_NOT_FALSIFIED",
    ),
    ("NOT_SUPPORTED", "FALSIFIED"): (
        "REFUTED",
        "PREDICTION_NOT_SUPPORTED_AND_FALSIFIED",
    ),
    ("SUPPORTED", "FALSIFIED"): (
        "NOT_INTERPRETABLE",
        "CONTRADICTORY_EVALUATION_STATUSES",
    ),
    ("NOT_SUPPORTED", "NOT_FALSIFIED"): (
        "NOT_INTERPRETABLE",
        "NON_DECISIVE_EVALUATION_STATUSES",
    ),
    ("SUPPORTED", "BLOCKED"): (
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    ("NOT_SUPPORTED", "BLOCKED"): (
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    ("BLOCKED", "FALSIFIED"): (
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    ("BLOCKED", "NOT_FALSIFIED"): (
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
    ("BLOCKED", "BLOCKED"): (
        "NOT_INTERPRETABLE",
        "BLOCKED_EVALUATION_STATUS",
    ),
}


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedExperimentalFinding:
    finding_id: str
    evaluation_submission_id: str
    evaluation_authority_qualification_id: str
    provenance_qualification_id: str
    experiment_execution_result_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    hypothesis_statement: str
    prediction: str
    falsification_rule: str
    supporting_measurement_ids: tuple[str, ...]
    prediction_status: str
    falsification_status: str
    finding_status: str
    interpretation_code: str
    policy_reference: str
    evaluator_id: str
    method_ref: str
    evaluation_rationale: str
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


def _finding_id(**values: object) -> str:
    return "QXF-" + _stable_hash({"contract": CONTRACT, "finding": values})[:32]


def _fingerprint(value: QualifiedExperimentalFinding) -> str:
    return _stable_hash({"contract": CONTRACT, "finding": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[QualifiedExperimentalFinding], str],
    ] = {}

    def attest(**values: object) -> QualifiedExperimentalFinding:
        produced = QualifiedExperimentalFinding(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not QualifiedExperimentalFinding:
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


_attest_qualified_experimental_finding, is_factory_attested_qualified_experimental_finding = _build_attestation_api()
del _build_attestation_api


def _validate_coherence(
    evaluation_submission: ExperimentEvaluationSubmission,
    evaluation_authority: QualifiedExperimentEvaluationAuthority,
) -> tuple[str, ...]:
    pairs = (
        (
            "evaluation_submission_id",
            evaluation_submission.evaluation_submission_id,
            evaluation_authority.evaluation_submission_id,
        ),
        (
            "experiment_execution_result_id",
            evaluation_submission.experiment_execution_result_id,
            evaluation_authority.experiment_execution_result_id,
        ),
        (
            "experiment_spec_id",
            evaluation_submission.experiment_spec_id,
            evaluation_authority.experiment_spec_id,
        ),
        ("request_id", evaluation_submission.request_id, evaluation_authority.request_id),
        ("revision_id", evaluation_submission.revision_id, evaluation_authority.revision_id),
        ("audit_id", evaluation_submission.audit_id, evaluation_authority.audit_id),
        ("scope_id", evaluation_submission.scope_id, evaluation_authority.scope_id),
        ("evaluator_id", evaluation_submission.evaluator_id, evaluation_authority.evaluator_id),
        ("method_ref", evaluation_submission.method_ref, evaluation_authority.method_ref),
        (
            "prediction_status",
            evaluation_submission.prediction_status,
            evaluation_authority.prediction_status,
        ),
        (
            "falsification_status",
            evaluation_submission.falsification_status,
            evaluation_authority.falsification_status,
        ),
        (
            "source_verdict",
            evaluation_submission.source_verdict,
            evaluation_authority.source_verdict,
        ),
        (
            "source_completeness_status",
            evaluation_submission.source_completeness_status,
            evaluation_authority.source_completeness_status,
        ),
        (
            "source_independence_status",
            evaluation_submission.source_independence_status,
            evaluation_authority.source_independence_status,
        ),
    )
    for field_name, expected, actual in pairs:
        if actual != expected:
            raise ValueError(f"P1.16 upstream mismatch: {field_name}")

    measurement_ids = tuple(
        item.measurement_id for item in evaluation_submission.measurements
    )
    if evaluation_authority.measurement_ids != measurement_ids:
        raise ValueError("P1.16 measurement identities/order mismatch")
    if evaluation_authority.measurement_provenance_status != "PASS":
        raise ValueError("P1.16 requires measurement_provenance_status PASS")
    if evaluation_authority.evaluation_authority_status != "PASS":
        raise ValueError("P1.16 requires evaluation_authority_status PASS")
    if evaluation_authority.finding_status != "BLOCKED":
        raise ValueError("P1.16 requires upstream finding_status BLOCKED")

    return measurement_ids


def interpret_qualified_experimental_finding(
    evaluation_submission,
    evaluation_authority,
) -> QualifiedExperimentalFinding:
    """Apply the fixed P1.16 policy to one exact qualified evaluation chain."""
    if type(evaluation_submission) is not ExperimentEvaluationSubmission:
        raise TypeError("P1.16 requires exact ExperimentEvaluationSubmission")
    if not is_factory_attested_experiment_evaluation_submission(evaluation_submission):
        raise ValueError("P1.16 requires currently-attested P1.13B evaluation")

    if type(evaluation_authority) is not QualifiedExperimentEvaluationAuthority:
        raise TypeError("P1.16 requires exact QualifiedExperimentEvaluationAuthority")
    if not is_factory_attested_qualified_experiment_evaluation_authority(evaluation_authority):
        raise ValueError("P1.16 requires currently-attested P1.15B authority")

    measurement_ids = _validate_coherence(
        evaluation_submission,
        evaluation_authority,
    )

    pair = (
        evaluation_submission.prediction_status,
        evaluation_submission.falsification_status,
    )
    interpretation = _INTERPRETATION_TABLE.get(pair)
    if interpretation is None:
        raise ValueError("P1.16 status pair is outside governed policy")
    finding_status, interpretation_code = interpretation

    values = {
        "evaluation_submission_id": evaluation_submission.evaluation_submission_id,
        "evaluation_authority_qualification_id": evaluation_authority.qualification_id,
        "provenance_qualification_id": evaluation_authority.provenance_qualification_id,
        "experiment_execution_result_id": evaluation_submission.experiment_execution_result_id,
        "experiment_spec_id": evaluation_submission.experiment_spec_id,
        "request_id": evaluation_submission.request_id,
        "revision_id": evaluation_submission.revision_id,
        "audit_id": evaluation_submission.audit_id,
        "scope_id": evaluation_submission.scope_id,
        "hypothesis_statement": evaluation_submission.hypothesis_statement,
        "prediction": evaluation_submission.prediction,
        "falsification_rule": evaluation_submission.falsification_rule,
        "supporting_measurement_ids": measurement_ids,
        "prediction_status": evaluation_submission.prediction_status,
        "falsification_status": evaluation_submission.falsification_status,
        "finding_status": finding_status,
        "interpretation_code": interpretation_code,
        "policy_reference": POLICY,
        "evaluator_id": evaluation_submission.evaluator_id,
        "method_ref": evaluation_submission.method_ref,
        "evaluation_rationale": evaluation_submission.evaluation_rationale,
        "measurement_provenance_status": evaluation_authority.measurement_provenance_status,
        "evaluation_authority_status": evaluation_authority.evaluation_authority_status,
        "source_verdict": evaluation_submission.source_verdict,
        "source_completeness_status": evaluation_submission.source_completeness_status,
        "source_independence_status": evaluation_submission.source_independence_status,
    }
    return _attest_qualified_experimental_finding(
        finding_id=_finding_id(**values),
        **values,
    )
