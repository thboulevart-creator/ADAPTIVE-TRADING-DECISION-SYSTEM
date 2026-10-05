"""P1.12D common qualified execution-evidence normalization boundary.

Consumes one exact factory-attested native execution result from an allowlisted
P1 execution owner plus the exact attested P1.11B input, and emits a new
factory-attested common evidence envelope. It does not evaluate the experiment,
derive measurements, create findings, or grant authority.
"""
from __future__ import annotations

import hashlib
import json
import weakref
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from src.linked_experiment_execution import (
    CONTRACT as P112B_CONTRACT,
    LinkedExperimentExecutionResult,
    is_factory_attested_linked_experiment_execution_result,
)
from src.p1_12c_qualified_producer_execution import (
    CONTRACT as P112C_CONTRACT,
    QualifiedProducerExecutionResult,
    is_factory_attested_qualified_producer_execution_result,
)
from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
)

CONTRACT = "P1_12D_QUALIFIED_EXECUTION_EVIDENCE_ENVELOPE_V1"
SCHEMA = "ATDS_P1_12D_QUALIFIED_EXECUTION_EVIDENCE_V1"
ALLOWED_OWNERS = ("P1.12B", "P1.12C")


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedExecutionEvidenceEnvelope:
    execution_evidence_envelope_id: str
    execution_owner_id: str
    native_execution_contract_id: str
    native_result_type_id: str
    native_result_id: str
    native_result_snapshot_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    experiment_definition_digest: str
    input_evidence_identity: str
    measurement_input_identity: str
    result_content_identity: str
    execution_procedure_identity: str
    native_execution_status: str
    input_owner_evidence_refs_json: str
    reconstruction_class: str
    reconstruction_descriptor_ref: str
    native_attestation_verifier_ref: str
    normalization_contract_digest: str
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


def _jsonable(value: object):
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def _native_snapshot_digest(result: object) -> str:
    return _digest({"native_type": type(result).__name__, "snapshot": _jsonable(asdict(result))})


def _module_sha256(relative_path: str) -> str:
    path = Path(__file__).resolve().parents[1] / relative_path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fingerprint(value: QualifiedExecutionEvidenceEnvelope) -> str:
    return _digest({"contract": CONTRACT, "envelope": asdict(value)})


def _build_attestation_api():
    registry: dict[int, tuple[weakref.ReferenceType[QualifiedExecutionEvidenceEnvelope], str]] = {}

    def attest(**values: object) -> QualifiedExecutionEvidenceEnvelope:
        produced = QualifiedExecutionEvidenceEnvelope(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, _fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not QualifiedExecutionEvidenceEnvelope:
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


_attest, is_factory_attested_qualified_execution_evidence = _build_attestation_api()
del _build_attestation_api


def validate_envelope_candidate(candidate: Mapping[str, Any]) -> dict[str, object]:
    if not candidate.get("execution_binding_id"):
        return _decision("BLOCKED", "BLOCKED_EXECUTION_BINDING_IDENTITY_REQUIRED")
    if not candidate.get("experiment_spec_id"):
        return _decision("BLOCKED", "BLOCKED_EXPERIMENT_SPEC_IDENTITY_REQUIRED")
    return _decision("READY", "COMMON_ENVELOPE_MINIMUM_IDENTITIES_PRESENT")


_BOUNDARY_REJECTIONS = {
    "P112C_AS_P112B": ("REJECTED", "REJECT_NATIVE_RESULT_TYPE_FORGERY"),
    "NATIVE_RESULT_IDENTITY_MISMATCH": ("BLOCKED", "BLOCKED_NATIVE_RESULT_IDENTITY_MISMATCH"),
    "ENGINE_SPECIFIC_FIELD_AS_UNIVERSAL": ("REJECTED", "REJECT_ENGINE_SPECIFIC_FIELD_LAUNDERING"),
    "BI5_STREAM_AS_P112C_INPUT": ("REJECTED", "REJECT_BI5_STREAM_IDENTITY_GENERALIZATION"),
    "PRODUCER_FIELDS_AS_P112B_COMMON": ("REJECTED", "REJECT_PRODUCER_FIELD_GENERALIZATION"),
    "NATIVE_STATUS_REWRITE": ("REJECTED", "REJECT_NATIVE_EXECUTION_STATUS_REWRITE"),
    "BLOCKED_TO_FAIL": ("REJECTED", "REJECT_BLOCKED_TO_FAIL_LAUNDERING"),
    "SCIENTIFIC_AUTHORITY": ("REJECTED", "REJECT_COMMON_INTERFACE_SCIENTIFIC_AUTHORITY"),
    "TRADING_CAPITAL_AUTHORITY": ("REJECTED", "REJECT_COMMON_INTERFACE_TRADING_AUTHORITY"),
    "RUNTIME_ATTESTATION_AS_DURABLE": ("BLOCKED", "BLOCKED_RUNTIME_ATTESTATION_NOT_DURABLE"),
    "STRUCTURAL_WITHOUT_NATIVE_ATTESTATION": ("BLOCKED", "BLOCKED_NATIVE_OWNER_ATTESTATION_REQUIRED"),
    "UNKNOWN_EXECUTION_OWNER": ("BLOCKED", "BLOCKED_UNKNOWN_EXECUTION_OWNER"),
    "POST_RESULT_NORMALIZER_SELECTION": ("BLOCKED", "BLOCKED_POST_RESULT_NORMALIZER_SELECTION"),
    "NATIVE_SEMANTIC_REWRITE": ("REJECTED", "REJECT_NATIVE_OWNER_SEMANTIC_REWRITE"),
}


def validate_common_boundary_claim(claim: str) -> dict[str, object]:
    if claim not in _BOUNDARY_REJECTIONS:
        return _decision("READY", "NO_COMMON_BOUNDARY_ESCALATION")
    status, reason = _BOUNDARY_REJECTIONS[claim]
    return _decision(status, reason)


def _verify_qei_match(result: object, qei: QualifiedExperimentExecutionInput) -> None:
    if type(qei) is not QualifiedExperimentExecutionInput:
        raise TypeError("P1.12D requires exact QualifiedExperimentExecutionInput")
    if not is_factory_attested_qualified_experiment_execution_input(qei):
        raise ValueError("P1.12D requires currently-attested P1.11B input")
    for name in (
        "experiment_execution_input_id",
        "execution_binding_id",
        "experiment_spec_id",
        "request_id",
        "revision_id",
        "audit_id",
        "scope_id",
    ):
        if getattr(result, name) != getattr(qei, name):
            raise ValueError(f"P1.12D upstream mismatch: {name}")


def normalize_qualified_execution(
    execution_result,
    qualified_input,
) -> QualifiedExecutionEvidenceEnvelope:
    """Normalize one exact attested native P1 execution result into common evidence."""
    if type(execution_result) is LinkedExperimentExecutionResult:
        if not is_factory_attested_linked_experiment_execution_result(execution_result):
            raise ValueError("P1.12D requires current P1.12B factory attestation")
        owner = "P1.12B"
        native_contract = P112B_CONTRACT
        native_type = "LinkedExperimentExecutionResult"
        native_id = execution_result.experiment_execution_result_id
        measurement_input = execution_result.stream_sha256
        result_content = execution_result.stream_sha256
        procedure_identity = _digest({
            "owner": owner,
            "p1_12b_module_sha256": _module_sha256("src/linked_experiment_execution.py"),
            "research_execution_module_sha256": _module_sha256("src/research/execution.py"),
        })
        native_status = "QUALIFIED_EXECUTION_RESULT_ATTESTED"
        input_refs = {
            "expected_corpus_hash": execution_result.expected_corpus_hash,
            "expected_contract_hash": execution_result.expected_contract_hash,
            "source_verdict": execution_result.source_verdict,
            "source_completeness_status": execution_result.source_completeness_status,
            "source_independence_status": execution_result.source_independence_status,
        }
        reconstruction_class = "RUNTIME_ATTESTED_EVIDENCE"
        reconstruction_ref = _digest({
            "native_result_id": native_id,
            "stream_sha256": execution_result.stream_sha256,
            "p1_12b_module_sha256": _module_sha256("src/linked_experiment_execution.py"),
        })
        verifier_ref = "src.linked_experiment_execution:is_factory_attested_linked_experiment_execution_result"
        input_evidence_identity = _digest({
            "expected_corpus_hash": execution_result.expected_corpus_hash,
            "expected_contract_hash": execution_result.expected_contract_hash,
        })
    elif type(execution_result) is QualifiedProducerExecutionResult:
        if not is_factory_attested_qualified_producer_execution_result(execution_result):
            raise ValueError("P1.12D requires current P1.12C factory attestation")
        owner = "P1.12C"
        native_contract = P112C_CONTRACT
        native_type = "QualifiedProducerExecutionResult"
        native_id = execution_result.producer_execution_result_id
        measurement_input = execution_result.output_sha256
        result_content = _digest({
            "result_identity": execution_result.result_identity,
            "output_sha256": execution_result.output_sha256,
        })
        procedure_identity = _digest({
            "producer_execution_plan_digest": execution_result.producer_execution_plan_digest,
            "producer_code_blob": execution_result.producer_code_blob,
            "producer_parameter_digest": execution_result.producer_parameter_digest,
            "runtime_lock_digest": execution_result.runtime_lock_digest,
        })
        native_status = execution_result.execution_status
        input_refs = {
            "data02_admission_digest": execution_result.data02_admission_digest,
            "dataset_identity": execution_result.dataset_identity,
            "data02_dataset_file_set_digest": execution_result.data02_dataset_file_set_digest,
            "data02_result_binding_digest": execution_result.data02_result_binding_digest,
        }
        reconstruction_class = execution_result.reconstruction_class
        reconstruction_ref = execution_result.reconstruction_descriptor_digest
        verifier_ref = "src.p1_12c_qualified_producer_execution:is_factory_attested_qualified_producer_execution_result"
        input_evidence_identity = _digest(input_refs)
    else:
        raise TypeError("P1.12D blocks unknown execution-result owner/type")

    _verify_qei_match(execution_result, qualified_input)
    experiment_digest = _experiment_definition_digest(qualified_input)
    native_snapshot = _native_snapshot_digest(execution_result)
    owner_refs_json = json.dumps(input_refs, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    normalization_digest = _digest({
        "contract": CONTRACT,
        "schema": SCHEMA,
        "owner": owner,
        "native_contract": native_contract,
        "native_type": native_type,
        "native_id": native_id,
        "native_snapshot_digest": native_snapshot,
        "experiment_definition_digest": experiment_digest,
        "measurement_input_identity": measurement_input,
        "result_content_identity": result_content,
        "execution_procedure_identity": procedure_identity,
        "native_execution_status": native_status,
    })

    values = {
        "execution_owner_id": owner,
        "native_execution_contract_id": native_contract,
        "native_result_type_id": native_type,
        "native_result_id": native_id,
        "native_result_snapshot_digest": native_snapshot,
        "experiment_execution_input_id": qualified_input.experiment_execution_input_id,
        "execution_binding_id": qualified_input.execution_binding_id,
        "experiment_spec_id": qualified_input.experiment_spec_id,
        "request_id": qualified_input.request_id,
        "revision_id": qualified_input.revision_id,
        "audit_id": qualified_input.audit_id,
        "scope_id": qualified_input.scope_id,
        "experiment_definition_digest": experiment_digest,
        "input_evidence_identity": input_evidence_identity,
        "measurement_input_identity": measurement_input,
        "result_content_identity": result_content,
        "execution_procedure_identity": procedure_identity,
        "native_execution_status": native_status,
        "input_owner_evidence_refs_json": owner_refs_json,
        "reconstruction_class": reconstruction_class,
        "reconstruction_descriptor_ref": reconstruction_ref,
        "native_attestation_verifier_ref": verifier_ref,
        "normalization_contract_digest": normalization_digest,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    envelope_id = "QEE-" + _digest({"contract": CONTRACT, "envelope": values})[:32]
    return _attest(execution_evidence_envelope_id=envelope_id, **values)
