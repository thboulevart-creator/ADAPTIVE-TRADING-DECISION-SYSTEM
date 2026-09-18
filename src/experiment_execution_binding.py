"""P1.10B qualification-only experiment-to-resource binding boundary.

This module links one exact attested P1.9B ExperimentSpecification to one exact
factory-bound, source-revalidated BoundResearchInput. It does not create a
QualifiedResearchInput, execute research, produce a result/evidence, or grant
authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.experiment_specification import (
    ExperimentSpecification,
    is_factory_attested_experiment_specification,
)
from src.research.input_binding import (
    BoundResearchInput,
    is_bound_research_input,
)


CONTRACT = "P1_10B_EXPERIMENT_EXECUTION_BINDING_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ExperimentExecutionBinding:
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


def _binding_content(**values: str) -> dict[str, str]:
    return {"contract": CONTRACT, **values}


def _binding_id(**content: str) -> str:
    return "EEB-" + _stable_hash(content)[:32]


def _binding_fingerprint(value: ExperimentExecutionBinding) -> str:
    return _stable_hash({"contract": CONTRACT, "binding": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[ExperimentExecutionBinding], str]] = {}

    def attest(**values: str) -> ExperimentExecutionBinding:
        produced = ExperimentExecutionBinding(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _binding_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not ExperimentExecutionBinding:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if _binding_fingerprint(value) != expected_fingerprint:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


_attest_experiment_execution_binding, is_factory_attested_experiment_execution_binding = _build_attestation_api()
del _build_attestation_api


def bind_experiment_execution(
    specification,
    bound_input,
) -> ExperimentExecutionBinding:
    """Bind one exact experiment specification to one exact validated resource input."""
    if type(specification) is not ExperimentSpecification:
        raise TypeError("P1.10B requires exact ExperimentSpecification")
    if not is_factory_attested_experiment_specification(specification):
        raise ValueError("P1.10B requires exact currently-attested P1.9B specification")

    if type(bound_input) is not BoundResearchInput:
        raise TypeError("P1.10B requires exact BoundResearchInput")
    if not is_bound_research_input(bound_input, revalidate_sources=True):
        raise ValueError("P1.10B requires exact currently-valid factory-bound research input")

    values = {
        "experiment_spec_id": specification.experiment_spec_id,
        "request_id": specification.request_id,
        "revision_id": specification.revision_id,
        "audit_id": specification.audit_id,
        "scope_id": specification.scope_id,
        "objective": specification.objective,
        "hypothesis_statement": specification.hypothesis_statement,
        "prediction": specification.prediction,
        "falsification_rule": specification.falsification_rule,
        "protocol": specification.protocol,
        "measurement_plan": specification.measurement_plan,
        "corpus_root": str(bound_input.corpus_root.resolve()),
        "contract_path": str(bound_input.contract_path.resolve()),
        "expected_corpus_hash": bound_input.expected_corpus_hash,
        "expected_contract_hash": bound_input.expected_contract_hash,
        "source_verdict": specification.source_verdict,
        "source_completeness_status": specification.source_completeness_status,
        "source_independence_status": specification.source_independence_status,
    }
    return _attest_experiment_execution_binding(
        execution_binding_id=_binding_id(**_binding_content(**values)),
        **values,
    )
