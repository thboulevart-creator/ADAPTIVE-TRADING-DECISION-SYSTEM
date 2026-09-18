"""P1.9B qualification-only FOLLOW-UP REQUEST to EXPERIMENT SPECIFICATION boundary.

This module records a non-executable experiment specification from one exact
attested EXPERIMENT FollowUpRequest. It does not bind data, execute research,
produce evidence/findings, or grant authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.follow_up_request import (
    FollowUpRequest,
    is_factory_attested_follow_up_request,
)


CONTRACT = "P1_9B_EXPERIMENT_SPECIFICATION_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ExperimentSpecification:
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


def _spec_content(
    *,
    request_id: str,
    revision_id: str,
    audit_id: str,
    scope_id: str,
    objective: str,
    hypothesis_statement: str,
    prediction: str,
    falsification_rule: str,
    protocol: str,
    measurement_plan: str,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, str]:
    return {
        "contract": CONTRACT,
        "request_id": request_id,
        "revision_id": revision_id,
        "audit_id": audit_id,
        "scope_id": scope_id,
        "objective": objective,
        "hypothesis_statement": hypothesis_statement,
        "prediction": prediction,
        "falsification_rule": falsification_rule,
        "protocol": protocol,
        "measurement_plan": measurement_plan,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _experiment_spec_id(**content: str) -> str:
    return "EXS-" + _stable_hash(content)[:32]


def _spec_fingerprint(value: ExperimentSpecification) -> str:
    return _stable_hash({"contract": CONTRACT, "specification": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[ExperimentSpecification], str]] = {}

    def attest(**values: str) -> ExperimentSpecification:
        produced = ExperimentSpecification(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _spec_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if not isinstance(value, ExperimentSpecification):
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _spec_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_experiment_specification, is_factory_attested_experiment_specification = _build_attestation_api()
del _build_attestation_api


def specify_experiment(
    request,
    *,
    hypothesis_statement,
    prediction,
    falsification_rule,
    protocol,
    measurement_plan,
) -> ExperimentSpecification:
    """Record an exact non-executable experiment specification."""
    if not isinstance(request, FollowUpRequest):
        raise TypeError("P1.9B requires full FollowUpRequest")
    if not is_factory_attested_follow_up_request(request):
        raise ValueError("P1.9B requires exact currently-attested P1.8 request")
    if request.request_kind != "EXPERIMENT":
        raise ValueError("P1.9B requires EXPERIMENT request")

    values = {
        "hypothesis_statement": hypothesis_statement,
        "prediction": prediction,
        "falsification_rule": falsification_rule,
        "protocol": protocol,
        "measurement_plan": measurement_plan,
    }
    for name, value in values.items():
        if type(value) is not str:
            raise TypeError(f"{name} must be exact str")
        if not value.strip():
            raise ValueError(f"{name} must be nonempty after strip")

    identity_content = _spec_content(
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        objective=request.specification,
        hypothesis_statement=hypothesis_statement,
        prediction=prediction,
        falsification_rule=falsification_rule,
        protocol=protocol,
        measurement_plan=measurement_plan,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
    return _attest_experiment_specification(
        experiment_spec_id=_experiment_spec_id(**identity_content),
        request_id=request.request_id,
        revision_id=request.revision_id,
        audit_id=request.audit_id,
        scope_id=request.scope_id,
        objective=request.specification,
        hypothesis_statement=hypothesis_statement,
        prediction=prediction,
        falsification_rule=falsification_rule,
        protocol=protocol,
        measurement_plan=measurement_plan,
        source_verdict=request.source_verdict,
        source_completeness_status=request.source_completeness_status,
        source_independence_status=request.source_independence_status,
    )
