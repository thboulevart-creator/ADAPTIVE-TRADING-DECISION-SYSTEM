"""P1.12B linked experiment execution boundary.

This module executes one exact P1.11B qualified experiment input through the
existing P0.4 deterministic research engine and immediately snapshots the
result with the full experiment provenance. It does not produce research-run
evidence, findings, hypothesis verdicts, or operational authorization.
"""

from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
)
from src.research.execution import (
    QualifiedResearchInput,
    is_qualified_execution_result,
    run_qualified_research,
)


CONTRACT = "P1_12B_LINKED_EXPERIMENT_EXECUTION_BOUNDARY_V1"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class LinkedExperimentExecutionResult:
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


def _identity_payload(
    *,
    experiment_execution_input_id: str,
    execution_binding_id: str,
    experiment_spec_id: str,
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
    corpus_root: str,
    contract_path: str,
    expected_corpus_hash: str,
    expected_contract_hash: str,
    files_consumed: int,
    ticks_consumed: int,
    first_timestamp: datetime | None,
    last_timestamp: datetime | None,
    stream_sha256: str,
    source_verdict: str,
    source_completeness_status: str,
    source_independence_status: str,
) -> dict[str, object]:
    return {
        "contract": CONTRACT,
        "experiment_execution_input_id": experiment_execution_input_id,
        "execution_binding_id": execution_binding_id,
        "experiment_spec_id": experiment_spec_id,
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
        "corpus_root": corpus_root,
        "contract_path": contract_path,
        "expected_corpus_hash": expected_corpus_hash,
        "expected_contract_hash": expected_contract_hash,
        "files_consumed": files_consumed,
        "ticks_consumed": ticks_consumed,
        "first_timestamp": first_timestamp.isoformat() if first_timestamp else None,
        "last_timestamp": last_timestamp.isoformat() if last_timestamp else None,
        "stream_sha256": stream_sha256,
        "source_verdict": source_verdict,
        "source_completeness_status": source_completeness_status,
        "source_independence_status": source_independence_status,
    }


def _result_id(**values: object) -> str:
    return "LER-" + _stable_hash(_identity_payload(**values))[:32]


def _result_fingerprint(value: LinkedExperimentExecutionResult) -> str:
    values = {
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
        "source_verdict": value.source_verdict,
        "source_completeness_status": value.source_completeness_status,
        "source_independence_status": value.source_independence_status,
    }
    return _stable_hash(
        {
            "experiment_execution_result_id": value.experiment_execution_result_id,
            **_identity_payload(**values),
        }
    )


def _build_attestation_api():
    registry: dict[
        int,
        tuple[weakref.ReferenceType[LinkedExperimentExecutionResult], str],
    ] = {}

    def attest(**values: object) -> LinkedExperimentExecutionResult:
        produced = LinkedExperimentExecutionResult(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _result_fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not LinkedExperimentExecutionResult:
            return False
        object_id = id(value)
        entry = registry.get(object_id)
        if entry is None:
            return False
        reference, expected_fingerprint = entry
        if reference() is not value:
            registry.pop(object_id, None)
            return False
        if _result_fingerprint(value) != expected_fingerprint:
            registry.pop(object_id, None)
            return False
        return True

    return attest, verify


_attest_linked_experiment_execution_result, is_factory_attested_linked_experiment_execution_result = _build_attestation_api()
del _build_attestation_api


def run_linked_experiment(
    execution_input,
) -> LinkedExperimentExecutionResult:
    """Execute one exact qualified experiment input and preserve its provenance."""
    if type(execution_input) is not QualifiedExperimentExecutionInput:
        raise TypeError("P1.12B requires exact QualifiedExperimentExecutionInput")
    if not is_factory_attested_qualified_experiment_execution_input(execution_input):
        raise ValueError("P1.12B requires exact currently-attested P1.11B input")

    technical_input = QualifiedResearchInput(
        corpus_root=Path(execution_input.corpus_root),
        contract_path=Path(execution_input.contract_path),
        expected_corpus_hash=execution_input.expected_corpus_hash,
        expected_contract_hash=execution_input.expected_contract_hash,
    )
    technical_result = run_qualified_research(technical_input)
    if not is_qualified_execution_result(technical_result, technical_input):
        raise ValueError("P1.12B requires identity-bound P0.4 execution result")

    values = {
        "experiment_execution_input_id": execution_input.experiment_execution_input_id,
        "execution_binding_id": execution_input.execution_binding_id,
        "experiment_spec_id": execution_input.experiment_spec_id,
        "request_id": execution_input.request_id,
        "revision_id": execution_input.revision_id,
        "audit_id": execution_input.audit_id,
        "scope_id": execution_input.scope_id,
        "objective": execution_input.objective,
        "hypothesis_statement": execution_input.hypothesis_statement,
        "prediction": execution_input.prediction,
        "falsification_rule": execution_input.falsification_rule,
        "protocol": execution_input.protocol,
        "measurement_plan": execution_input.measurement_plan,
        "corpus_root": execution_input.corpus_root,
        "contract_path": execution_input.contract_path,
        "expected_corpus_hash": execution_input.expected_corpus_hash,
        "expected_contract_hash": execution_input.expected_contract_hash,
        "files_consumed": technical_result.files_consumed,
        "ticks_consumed": technical_result.ticks_consumed,
        "first_timestamp": technical_result.first_timestamp,
        "last_timestamp": technical_result.last_timestamp,
        "stream_sha256": technical_result.stream_sha256,
        "source_verdict": execution_input.source_verdict,
        "source_completeness_status": execution_input.source_completeness_status,
        "source_independence_status": execution_input.source_independence_status,
    }
    return _attest_linked_experiment_execution_result(
        experiment_execution_result_id=_result_id(**values),
        **values,
    )
