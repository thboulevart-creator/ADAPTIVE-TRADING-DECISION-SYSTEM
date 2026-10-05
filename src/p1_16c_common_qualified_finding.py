"""P1.16C common qualified experimental finding interpretation boundary.

Consumes one exact P1.13C evaluation and one exact P1.15C qualified authority.
It reuses the exact legacy P1.16 interpretation table/policy semantics while
preserving common execution-owner identity. It grants no operational authority.
"""
from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.p1_13c_common_evaluation import (
    CommonExperimentEvaluationSubmission,
    is_factory_attested_common_experiment_evaluation,
)
from src.p1_15c_common_evaluator_authority import (
    CommonQualifiedExperimentEvaluationAuthority,
    is_factory_attested_common_evaluation_authority,
)
from src.qualified_experimental_finding import (
    POLICY as LEGACY_POLICY,
    _INTERPRETATION_TABLE as LEGACY_INTERPRETATION_TABLE,
)

CONTRACT = "P1_16C_COMMON_QUALIFIED_EXPERIMENTAL_FINDING_V1"
POLICY = LEGACY_POLICY
_INTERPRETATION_TABLE = dict(LEGACY_INTERPRETATION_TABLE)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CommonQualifiedExperimentalFinding:
    finding_id: str
    evaluation_submission_id: str
    evaluation_authority_qualification_id: str
    provenance_qualification_id: str
    execution_evidence_envelope_id: str
    execution_owner_id: str
    native_result_id: str
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
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


def _stable(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def _fingerprint(value: CommonQualifiedExperimentalFinding) -> str:
    return _stable({"contract": CONTRACT, "finding": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[CommonQualifiedExperimentalFinding], str]] = {}

    def attest(**values: object) -> CommonQualifiedExperimentalFinding:
        produced = CommonQualifiedExperimentalFinding(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not CommonQualifiedExperimentalFinding:
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


_attest, is_factory_attested_common_qualified_finding = _build_attestation_api()
del _build_attestation_api


def validate_common_finding_claim(claim: str) -> dict[str, object]:
    if claim == "MISMATCHED_AUTHORITY":
        return {"contract": CONTRACT, "status": "BLOCKED", "reason": "BLOCKED_FINDING_AUTHORITY_MISMATCH"}
    return {"contract": CONTRACT, "status": "READY", "reason": "NO_FINDING_LAUNDERING"}


def _validate_coherence(
    evaluation: CommonExperimentEvaluationSubmission,
    authority: CommonQualifiedExperimentEvaluationAuthority,
) -> tuple[str, ...]:
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
        ("evaluator_id", evaluation.evaluator_id),
        ("method_ref", evaluation.method_ref),
        ("prediction_status", evaluation.prediction_status),
        ("falsification_status", evaluation.falsification_status),
    )
    for field, expected in pairs:
        if getattr(authority, field) != expected:
            raise ValueError(f"P1.16C upstream mismatch: {field}")

    measurement_ids = tuple(item.measurement_id for item in evaluation.measurements)
    if authority.measurement_ids != measurement_ids:
        raise ValueError("P1.16C measurement identities/order mismatch")
    if authority.measurement_provenance_status != "PASS":
        raise ValueError("P1.16C requires measurement provenance PASS")
    if authority.evaluation_authority_status != "PASS":
        raise ValueError("P1.16C requires evaluation authority PASS")
    if authority.finding_status != "BLOCKED":
        raise ValueError("P1.16C requires pre-finding BLOCKED")
    return measurement_ids


def interpret_common_qualified_finding(
    evaluation_submission,
    evaluation_authority,
) -> CommonQualifiedExperimentalFinding:
    if type(evaluation_submission) is not CommonExperimentEvaluationSubmission:
        raise TypeError("P1.16C requires exact CommonExperimentEvaluationSubmission")
    if not is_factory_attested_common_experiment_evaluation(evaluation_submission):
        raise ValueError("P1.16C requires currently-attested P1.13C evaluation")
    if type(evaluation_authority) is not CommonQualifiedExperimentEvaluationAuthority:
        raise TypeError("P1.16C requires exact CommonQualifiedExperimentEvaluationAuthority")
    if not is_factory_attested_common_evaluation_authority(evaluation_authority):
        raise ValueError("P1.16C requires currently-attested P1.15C authority")

    measurement_ids = _validate_coherence(evaluation_submission, evaluation_authority)
    pair = (evaluation_submission.prediction_status, evaluation_submission.falsification_status)
    interpretation = _INTERPRETATION_TABLE.get(pair)
    if interpretation is None:
        raise ValueError("P1.16C status pair outside governed legacy policy")
    finding_status, interpretation_code = interpretation

    values = {
        "evaluation_submission_id": evaluation_submission.evaluation_submission_id,
        "evaluation_authority_qualification_id": evaluation_authority.qualification_id,
        "provenance_qualification_id": evaluation_authority.provenance_qualification_id,
        "execution_evidence_envelope_id": evaluation_submission.execution_evidence_envelope_id,
        "execution_owner_id": evaluation_submission.execution_owner_id,
        "native_result_id": evaluation_submission.native_result_id,
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
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    finding_id = "CQXF-" + _stable({"contract": CONTRACT, "finding": values})[:32]
    return _attest(finding_id=finding_id, **values)
