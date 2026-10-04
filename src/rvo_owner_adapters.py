"""RVO-03 adapters to canonical owner interfaces.

These adapters are intentionally RVO-owned. They do not modify or reinterpret
owner semantics. Native owner payloads/statuses are returned unchanged wherever
possible. Capability gaps fail closed.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict
from pathlib import Path

from src import experiment_specification as p1_spec
from src import mcepr_registry
from src.data import dataset_admissibility
from tools import e1_04_execution_cost_model
from tools import p22_01_pure_state_projector
from tools import p22_02_identity_state_verifier
from tools import p22_03_evidence_envelope_recorder
from tools import smf03_core_foundation

MATRIX_SCHEMA = "ATDS_RVO_03_CANONICAL_OWNER_CAPABILITY_MATRIX_V0_1"
MATRIX_PATH = (
    Path(__file__).resolve().parents[1]
    / "GOVERNANCE"
    / "RVO-03-CANONICAL-OWNER-CAPABILITY-MATRIX-V0.1.json"
)
RVO_AUTHORITY = "NONE"

EXPECTED_OWNER_CONTRACTS = {
    "P1_EXPERIMENT_SPECIFICATION": "P1_9B_EXPERIMENT_SPECIFICATION_BOUNDARY_V1",
    "SMF_CORE_ACTIVATION_M01_M11": "ATDS_SMF03_CORE_FOUNDATION_V0_1",
    "MCEPR_MINIMAL_REGISTRY": "ATDS_MCEPR_REGISTRY_SEGMENT_V0_1",
    "PCP_P22_01_STATE_PROJECTOR": "ATDS_P22_01_PURE_STATE_PROJECTOR_V0_1",
    "PCP_P22_02_IDENTITY_VERIFIER": "ATDS_P22_02_IDENTITY_STATE_VERIFIER_V0_1",
    "PCP_P22_03_EVIDENCE_ENVELOPE": "ATDS_P22_03_EVIDENCE_ENVELOPE_RECORDER_V0_1",
    "EXECUTION_E1_SPECIFIC": "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1",
}


class RVOOwnerBindingError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class RVOOwnerBlocked(RVOOwnerBindingError):
    pass


class RVOOwnerFail(RVOOwnerBindingError):
    pass


def load_capability_matrix() -> dict:
    try:
        value = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RVOOwnerFail("CAPABILITY_MATRIX_UNREADABLE") from exc
    if value.get("schema") != MATRIX_SCHEMA:
        raise RVOOwnerFail("CAPABILITY_MATRIX_SCHEMA_MISMATCH")
    rows = value.get("capabilities")
    if not isinstance(rows, list) or not rows:
        raise RVOOwnerFail("CAPABILITY_MATRIX_EMPTY")
    ids = [row.get("capability_id") for row in rows]
    if any(not isinstance(item, str) or not item for item in ids):
        raise RVOOwnerFail("CAPABILITY_MATRIX_INVALID_ID")
    if len(ids) != len(set(ids)):
        raise RVOOwnerFail("CAPABILITY_MATRIX_DUPLICATE_ID")
    return copy.deepcopy(value)


def capability(capability_id: str) -> dict:
    matrix = load_capability_matrix()
    for row in matrix["capabilities"]:
        if row["capability_id"] == capability_id:
            return copy.deepcopy(row)
    raise RVOOwnerFail("UNKNOWN_CAPABILITY")


def require_qualified(capability_id: str) -> dict:
    row = capability(capability_id)
    if row["state"] != "QUALIFIED":
        raise RVOOwnerBlocked(f"CAPABILITY_NOT_QUALIFIED:{capability_id}:{row['state']}")
    return row


def require_available(capability_id: str) -> dict:
    row = capability(capability_id)
    if row["state"] not in {"AVAILABLE", "QUALIFIED"}:
        raise RVOOwnerBlocked(f"CAPABILITY_NOT_AVAILABLE:{capability_id}:{row['state']}")
    return row


def owner_interface_identities() -> dict[str, str]:
    observed = {
        "P1_EXPERIMENT_SPECIFICATION": p1_spec.CONTRACT,
        "SMF_CORE_ACTIVATION_M01_M11": smf03_core_foundation.CONTRACT,
        "MCEPR_MINIMAL_REGISTRY": mcepr_registry.SEGMENT_CONTRACT,
        "PCP_P22_01_STATE_PROJECTOR": p22_01_pure_state_projector.CONTRACT,
        "PCP_P22_02_IDENTITY_VERIFIER": p22_02_identity_state_verifier.CONTRACT,
        "PCP_P22_03_EVIDENCE_ENVELOPE": p22_03_evidence_envelope_recorder.CONTRACT,
        "EXECUTION_E1_SPECIFIC": e1_04_execution_cost_model.CONTRACT,
    }
    if observed != EXPECTED_OWNER_CONTRACTS:
        raise RVOOwnerFail("OWNER_CONTRACT_IDENTITY_DRIFT")
    return observed


def bind_p1_experiment_specification(specification) -> dict:
    row = require_qualified("P1_EXPERIMENT_SPECIFICATION")
    owner_interface_identities()
    if not isinstance(specification, p1_spec.ExperimentSpecification):
        raise RVOOwnerFail("P1_EXPERIMENT_SPECIFICATION_TYPE")
    if not p1_spec.is_factory_attested_experiment_specification(specification):
        raise RVOOwnerBlocked("P1_EXPERIMENT_SPECIFICATION_NOT_ATTESTED")
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": p1_spec.CONTRACT,
        "experiment_spec_id": specification.experiment_spec_id,
        "request_id": specification.request_id,
        "source_verdict": specification.source_verdict,
        "source_completeness_status": specification.source_completeness_status,
        "source_independence_status": specification.source_independence_status,
        "rvo_authority": RVO_AUTHORITY,
    }


def create_smf_activation(**kwargs) -> dict:
    row = require_qualified("SMF_CORE_ACTIVATION_M01_M11")
    owner_interface_identities()
    record = smf03_core_foundation.create_activation_record(**kwargs)
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": smf03_core_foundation.CONTRACT,
        "owner_payload": copy.deepcopy(record),
        "rvo_authority": RVO_AUTHORITY,
    }


def create_mcepr_synthetic_segment(*, source_blob: str) -> dict:
    row = require_qualified("MCEPR_MINIMAL_REGISTRY")
    owner_interface_identities()
    event = mcepr_registry.make_event(
        {
            "occurred_at_utc": "2026-10-04T00:00:00Z",
            "operator": "RVO-03-SYNTHETIC",
            "nature": "SYNTHETIC_OWNER_INTERFACE_BINDING",
            "declared_purpose": "RVO-03 synthetic integration qualification",
            "source_refs": [f"git_blob:{source_blob}"],
            "asset": None,
            "period_start_utc": None,
            "period_end_utc": None,
            "consultation_intensity": None,
            "information_accessed": None,
            "evidence_refs": [],
        }
    )
    segment = mcepr_registry.make_segment(None, [event], [])
    raw = json.dumps(segment, sort_keys=True, separators=(",", ":"))
    validation = mcepr_registry.validate_registry_files(
        {segment["registry_id"] + ".json": raw},
        git_resolver=lambda ref: True,
        adjudication_basis_allowlist=set(),
    )
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": mcepr_registry.SEGMENT_CONTRACT,
        "event": copy.deepcopy(event),
        "segment": copy.deepcopy(segment),
        "validation": copy.deepcopy(validation),
        "rvo_authority": RVO_AUTHORITY,
    }


def project_pcp_state(snapshot: dict) -> dict:
    row = require_qualified("PCP_P22_01_STATE_PROJECTOR")
    owner_interface_identities()
    output = p22_01_pure_state_projector.project_active_state(copy.deepcopy(snapshot))
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": p22_01_pure_state_projector.CONTRACT,
        "owner_payload": output,
        "rvo_authority": RVO_AUTHORITY,
    }


def verify_pcp_identity(observed: dict, expected: dict) -> dict:
    row = require_qualified("PCP_P22_02_IDENTITY_VERIFIER")
    owner_interface_identities()
    output = p22_02_identity_state_verifier.verify_identity_state(
        copy.deepcopy(observed),
        copy.deepcopy(expected),
    )
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": p22_02_identity_state_verifier.CONTRACT,
        "owner_payload": output,
        "rvo_authority": RVO_AUTHORITY,
    }


def build_pcp_evidence(evidence: dict) -> dict:
    row = require_qualified("PCP_P22_03_EVIDENCE_ENVELOPE")
    owner_interface_identities()
    envelope = p22_03_evidence_envelope_recorder.build_evidence_envelope(
        copy.deepcopy(evidence)
    )
    validation = p22_03_evidence_envelope_recorder.validate_evidence_envelope(envelope)
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": p22_03_evidence_envelope_recorder.CONTRACT,
        "owner_payload": envelope,
        "validation": validation,
        "rvo_authority": RVO_AUTHORITY,
    }


def assess_tick_dataset(
    path,
    *,
    dataset_id,
    dataset_version,
    instrument,
    granularity,
    timezone_storage,
) -> dict:
    row = require_available("DATASET_ADMISSIBILITY_TICK_CSV")
    identity = dataset_admissibility.build_identity(
        path,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        instrument=instrument,
        granularity=granularity,
        timezone_storage=timezone_storage,
    )
    report = dataset_admissibility.assess(path, identity=identity)
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_payload": asdict(report),
        "rvo_authority": RVO_AUTHORITY,
    }


def require_temporal_generic() -> dict:
    return require_qualified("TEMPORAL_GENERIC_POINT_IN_TIME")


def require_execution_generic() -> dict:
    return require_qualified("EXECUTION_GENERIC")


def execute_e1_specific_synthetic(**kwargs) -> dict:
    row = require_qualified("EXECUTION_E1_SPECIFIC")
    owner_interface_identities()
    result = e1_04_execution_cost_model.execute_transition(**kwargs)
    return {
        "capability_id": row["capability_id"],
        "capability_state": row["state"],
        "owner_contract": e1_04_execution_cost_model.CONTRACT,
        "owner_payload": copy.deepcopy(result),
        "cost_scope": copy.deepcopy(e1_04_execution_cost_model.COST_SCOPE),
        "forbidden_claims": tuple(e1_04_execution_cost_model.FORBIDDEN_CLAIMS),
        "generic_for_rvo": row["generic_for_rvo"],
        "rvo_authority": RVO_AUTHORITY,
    }


def unresolved_capability_gaps() -> tuple[str, ...]:
    matrix = load_capability_matrix()
    return tuple(matrix.get("unresolved_gaps", []))
