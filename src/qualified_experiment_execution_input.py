"""P1.11B qualification-only experiment execution input boundary.

This module preserves one exact P1.10B experiment binding while revalidating
its current corpus and contract identities through the existing P0.4 binding
capability. It does not execute research, produce results/evidence, or grant
authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass

from src.experiment_execution_binding import (
    ExperimentExecutionBinding,
    is_factory_attested_experiment_execution_binding,
)
from src.research.input_binding import bind_execution_input


CONTRACT = "P1_11B_QUALIFIED_EXPERIMENT_EXECUTION_INPUT_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedExperimentExecutionInput:
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


def _input_content(**values: str) -> dict[str, str]:
    return {"contract": CONTRACT, **values}


def _input_id(**content: str) -> str:
    return "QEI-" + _stable_hash(content)[:32]


def _input_fingerprint(value: QualifiedExperimentExecutionInput) -> str:
    return _stable_hash({"contract": CONTRACT, "input": asdict(value)})


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[QualifiedExperimentExecutionInput], str],
    ] = {}

    def attest(**values: str) -> QualifiedExperimentExecutionInput:
        produced = QualifiedExperimentExecutionInput(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _input_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not QualifiedExperimentExecutionInput:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _input_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_qualified_experiment_execution_input, is_factory_attested_qualified_experiment_execution_input = _build_attestation_api()
del _build_attestation_api


def qualify_experiment_execution_input(
    binding,
) -> QualifiedExperimentExecutionInput:
    """Revalidate resources and snapshot one exact experiment execution binding."""
    if type(binding) is not ExperimentExecutionBinding:
        raise TypeError("P1.11B requires exact ExperimentExecutionBinding")
    if not is_factory_attested_experiment_execution_binding(binding):
        raise ValueError("P1.11B requires exact currently-attested P1.10B binding")

    # Reuse P0.4 identity binding. This performs current filesystem/hash/contract
    # revalidation but does not execute the research engine.
    bind_execution_input(
        binding.corpus_root,
        binding.contract_path,
        binding.expected_corpus_hash,
        binding.expected_contract_hash,
    )

    values = {
        "execution_binding_id": binding.execution_binding_id,
        "experiment_spec_id": binding.experiment_spec_id,
        "request_id": binding.request_id,
        "revision_id": binding.revision_id,
        "audit_id": binding.audit_id,
        "scope_id": binding.scope_id,
        "objective": binding.objective,
        "hypothesis_statement": binding.hypothesis_statement,
        "prediction": binding.prediction,
        "falsification_rule": binding.falsification_rule,
        "protocol": binding.protocol,
        "measurement_plan": binding.measurement_plan,
        "corpus_root": binding.corpus_root,
        "contract_path": binding.contract_path,
        "expected_corpus_hash": binding.expected_corpus_hash,
        "expected_contract_hash": binding.expected_contract_hash,
        "source_verdict": binding.source_verdict,
        "source_completeness_status": binding.source_completeness_status,
        "source_independence_status": binding.source_independence_status,
    }
    return _attest_qualified_experiment_execution_input(
        experiment_execution_input_id=_input_id(**_input_content(**values)),
        **values,
    )
