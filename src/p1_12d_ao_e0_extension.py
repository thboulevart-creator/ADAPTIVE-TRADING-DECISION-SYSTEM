"""Bounded P1.12D normalization extension for the exact AO-E0 native owner.

The historical P1.12D core remains byte-identical. This extension reuses its
factory-attested common envelope and exact QEI matching machinery while
allowlisting only the exact AO-E0 result type/contract.
"""
from __future__ import annotations

import json

from src import p1_12d_qualified_execution_evidence as base
from src.p1_12c_ao_e0_native_owner import (
    CONTRACT as AO_E0_NATIVE_CONTRACT,
    OWNER_ID as AO_E0_ALLOWED_OWNER,
    QualifiedAOE0ExecutionResult,
    is_factory_attested_ao_e0_execution_result,
)

CONTRACT = "P1_12D_AO_E0_EXACT_NATIVE_OWNER_EXTENSION_V0_1"
BASE_P112D_CONTRACT = base.CONTRACT
BASE_ALLOWED_OWNERS = base.ALLOWED_OWNERS


def normalize_ao_e0_execution(execution_result, qualified_input):
    if type(execution_result) is not QualifiedAOE0ExecutionResult:
        raise TypeError("P1.12D AO-E0 extension blocks unknown/structural owner type")
    if not is_factory_attested_ao_e0_execution_result(execution_result):
        raise ValueError("P1.12D AO-E0 extension requires current factory attestation")

    base._verify_qei_match(execution_result, qualified_input)
    experiment_digest = base._experiment_definition_digest(qualified_input)
    native_snapshot = base._native_snapshot_digest(execution_result)

    owner = AO_E0_ALLOWED_OWNER
    native_contract = AO_E0_NATIVE_CONTRACT
    native_type = "QualifiedAOE0ExecutionResult"
    native_id = execution_result.ao_e0_execution_result_id
    measurement_input = execution_result.result_content_identity
    result_content = execution_result.result_content_identity
    procedure_identity = base._digest({
        "owner": owner,
        "native_contract": native_contract,
        "producer_id": execution_result.producer_id,
        "producer_code_blob": execution_result.producer_code_blob,
        "semantic_parameter_digest": execution_result.semantic_parameter_digest,
        "invocation_profile_digest": execution_result.invocation_profile_digest,
        "runtime_lock_digest": execution_result.runtime_lock_digest,
        "execution_model_identity": execution_result.execution_model_identity,
        "cost_scope_identity": execution_result.cost_scope_identity,
    })
    input_refs = {
        "cell_identity": execution_result.cell_identity,
        "claim_class": execution_result.claim_class,
        "data_binding_digest": execution_result.data_binding_digest,
        "temporal_binding_digest": execution_result.temporal_binding_digest,
        "execution_model_identity": execution_result.execution_model_identity,
        "cost_scope_identity": execution_result.cost_scope_identity,
    }
    reconstruction_class = "RUNTIME_ATTESTED_EVIDENCE"
    reconstruction_ref = execution_result.result_content_identity
    verifier_ref = "src.p1_12c_ao_e0_native_owner:is_factory_attested_ao_e0_execution_result"
    owner_refs_json = json.dumps(input_refs, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    normalization_digest = base._digest({
        "contract": base.CONTRACT,
        "extension_contract": CONTRACT,
        "schema": base.SCHEMA,
        "owner": owner,
        "native_contract": native_contract,
        "native_type": native_type,
        "native_id": native_id,
        "native_snapshot_digest": native_snapshot,
        "experiment_definition_digest": experiment_digest,
        "measurement_input_identity": measurement_input,
        "result_content_identity": result_content,
        "execution_procedure_identity": procedure_identity,
        "native_execution_status": execution_result.execution_status,
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
        "input_evidence_identity": base._digest(input_refs),
        "measurement_input_identity": measurement_input,
        "result_content_identity": result_content,
        "execution_procedure_identity": procedure_identity,
        "native_execution_status": execution_result.execution_status,
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
    envelope_id = "QEE-" + base._digest({
        "contract": base.CONTRACT,
        "extension_contract": CONTRACT,
        "envelope": values,
    })[:32]
    return base._attest(execution_evidence_envelope_id=envelope_id, **values)


def validate_owner_candidate(value: object) -> dict:
    if type(value) is not QualifiedAOE0ExecutionResult:
        return {"status":"BLOCKED","reason":"BLOCKED_UNKNOWN_EXECUTION_OWNER"}
    if not is_factory_attested_ao_e0_execution_result(value):
        return {"status":"BLOCKED","reason":"BLOCKED_NATIVE_OWNER_ATTESTATION_REQUIRED"}
    return {"status":"READY","reason":"EXACT_AO_E0_NATIVE_OWNER_ATTESTED"}
