"""AO-E0/CC05 exact native owner extension over the qualified P1-21 capability pattern.

No real AO-E0 execution is authorized here. This module only qualifies the
pre-execution owner profile, exact bindings, runtime-lock capability, native
result type, and synthetic rebreak attestation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import weakref

from src import p1_12c_qualified_producer_execution as p121
from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
)

CONTRACT = "P1_12C_AO_E0_CC05_NATIVE_EXECUTION_OWNER_V0_1"
OWNER_ID = "P1.12C.AO-E0"
CELL_IDENTITY = "sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
CLAIM_CLASS = "CC05_ECONOMIC_NET_PROFITABILITY"
PRODUCER_ID = "ATDS_AO_E0_CC05_E1_NATIVE_EXECUTION_V0_1"
PRODUCER_BLOB = "981794fedbfd8c9fdac69ba4751540e63a2e5289"
PROFILE_ID = "P1_12C_AO_E0_CC05_E1_PROFILE_V0_1"
OUTPUT_SCHEMA = "ATDS_AO_E0_CC05_E1_EXECUTION_EVIDENCE_V0_1"
OUTPUT_STATUS = "EXECUTION_EVIDENCE_COMPLETE"
P1_21_FOUNDATION_CONTRACT = "P1_12C_REAL_QUALIFIED_PRODUCER_CAPABILITY_V1"
P1_21_FOUNDATION_BLOB = "9d304202d44c8917cf640fd0b4114169968e511e"

DT01A_CONTRACT_BLOB = "66759f93ad019e18fd00c871bd1737293070b1a8"
DT01B_CONTRACT_BLOB = "b312981ae8cba905c50db657ba0217addf296548"
DT01_CLOSURE_RECEIPT_BLOB = "fad20f527393b85b6d06b998c89a3543a18be46a"
E1_03_CONTRACT_BLOB = "c2d4323039d65fcd9319d4f5eb02f45ee27c8afc"
E1_04_CONTRACT_BLOB = "cf07f1400af614fa53fe41afe8a40e412d28c87d"
E1_04_RUNTIME_BLOB = "15e72b8743e7726fc8b8bedd933cf7defe56413b"
E1_05_CONTRACT_BLOB = "51dc1152808ec9e841924976eac572cc4ec2ff93"
E1_05_RUNTIME_BLOB = "baad3bd7c2e810451737c89bf8f9bcabc17c5ba6"
EXEC04_POLICY_BLOB = "52b849c46d0a5cf45b261fd16e34edab44489572"
EXEC05_CONTRACT_BLOB = "ca292ce2efde127bd7ab5f8efb160a98fa73f900"
B4_FREEZE_BLOB = "8cf494fcfffe0575d3e2a0fe887e2f524a3eb304"

SEMANTIC_PARAMETERS = {
    "strategy_id": "MOMENTUM_V1",
    "instrument": "USTECH",
    "timeframe": "H1",
    "claim_class": CLAIM_CLASS,
    "cell_identity": CELL_IDENTITY,
    "temporal_mode": "E1_REPLAY_POINT_IN_TIME",
    "cost_node": "F2_S4",
    "financing_multiplier": 2,
    "financing_adverse_anchor": 6.3665,
    "slippage_bps_per_execution_event": 4,
    "delta_min": 5.0,
}
EXPECTED_DATA_BINDING = {
    "cell_identity": CELL_IDENTITY,
    "dt01a_contract_blob": DT01A_CONTRACT_BLOB,
    "closure_receipt_blob": DT01_CLOSURE_RECEIPT_BLOB,
    "b10": "CLOSED",
    "raw_dataset": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
    "ap0_dataset": "USTECH_PROFILE_MINUTE_CORE_V0_1",
    "h1_dataset": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
}
EXPECTED_TEMPORAL_BINDING = {
    "cell_identity": CELL_IDENTITY,
    "dt01b_contract_blob": DT01B_CONTRACT_BLOB,
    "closure_receipt_blob": DT01_CLOSURE_RECEIPT_BLOB,
    "b6": "CLOSED",
    "temporal_mode": "E1_REPLAY_POINT_IN_TIME",
    "decision_time": "SIGNAL_H1_END_MS",
    "future_h1": "FORBIDDEN",
    "same_bar_execution": "FORBIDDEN",
    "cross_continuity_lookback": "FORBIDDEN",
    "past_price_forward_fill": "FORBIDDEN",
}
EXECUTION_MODEL_IDENTITY = hashlib.sha256(json.dumps({
    "e1_03_contract_blob": E1_03_CONTRACT_BLOB,
    "e1_04_contract_blob": E1_04_CONTRACT_BLOB,
    "e1_04_runtime_blob": E1_04_RUNTIME_BLOB,
    "e1_05_contract_blob": E1_05_CONTRACT_BLOB,
    "e1_05_runtime_blob": E1_05_RUNTIME_BLOB,
    "price_basis": "RAW_BID_ASK_EXECUTION",
    "mid_is_execution_price": False,
    "no_pyramiding": True,
    "no_admissible_execution": "NOT_EXECUTED",
}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
COST_SCOPE_IDENTITY = hashlib.sha256(json.dumps({
    "exec04_policy_blob": EXEC04_POLICY_BLOB,
    "exec05_contract_blob": EXEC05_CONTRACT_BLOB,
    "binding_node": "F2_S4",
    "financing_multiplier": 2,
    "financing_adverse_anchor": 6.3665,
    "slippage_bps_per_execution_event": 4,
    "policy_stress_is_observed_historical_cost": False,
    "b4_freeze_blob": B4_FREEZE_BLOB,
}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
SEMANTIC_PARAMETER_DIGEST = hashlib.sha256(
    json.dumps(SEMANTIC_PARAMETERS, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()


class AOE0P1OwnerBlocked(RuntimeError):
    pass


def _digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _sha64(value: object) -> bool:
    return type(value) is str and len(value) == 64 and set(value) <= set("0123456789abcdef")


def _build_attestation_api(cls, tag: str):
    registry: dict[int, tuple[weakref.ReferenceType, str]] = {}

    def fingerprint(value) -> str:
        return _digest({"contract": CONTRACT, "tag": tag, "value": asdict(value)})

    def attest(**values):
        produced = cls(**values)
        oid = id(produced)
        def cleanup(reference, *, expected_oid=oid):
            current = registry.get(expected_oid)
            if current is not None and current[0] is reference:
                registry.pop(expected_oid, None)
        ref = weakref.ref(produced, cleanup)
        registry[oid] = (ref, fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not cls:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        ref, expected = entry
        if ref() is not value or fingerprint(value) != expected:
            registry.pop(id(value), None)
            return False
        return True
    return attest, verify


@dataclass(frozen=True, slots=True, weakref_slot=True)
class AOE0ProducerInvocationProfile:
    invocation_profile_id: str
    invocation_profile_digest: str
    producer_id: str
    producer_code_blob: str
    producer_protocol: str
    child_argv_schema_json: str
    shell: bool
    result_exposed: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class AOE0ProducerRuntimeLock:
    runtime_lock_id: str
    runtime_lock_digest: str
    python_version: str
    python_binary_sha256: str
    numpy_version: str
    numpy_metadata_sha256: str
    pyarrow_version: str
    pyarrow_metadata_sha256: str
    tzdata_version: str
    tzdata_metadata_sha256: str
    timezone_name: str
    timeout_seconds: int
    invocation_profile_digest: str
    result_exposed: bool
    execution_authority: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedAOE0ExecutionPlan:
    ao_e0_execution_plan_id: str
    ao_e0_execution_plan_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    cell_identity: str
    claim_class: str
    data_binding_digest: str
    temporal_binding_digest: str
    execution_model_identity: str
    cost_scope_identity: str
    producer_id: str
    producer_code_blob: str
    invocation_profile_id: str
    invocation_profile_digest: str
    runtime_lock_id: str
    runtime_lock_digest: str
    semantic_parameter_digest: str
    expected_output_schema: str
    expected_output_status: str
    result_exposed: bool
    oos_consumption: bool
    execution_authority: bool
    scientific_authority: bool
    trading_authority: bool
    capital_authority: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedAOE0ExecutionResult:
    ao_e0_execution_result_id: str
    ao_e0_execution_plan_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    cell_identity: str
    claim_class: str
    data_binding_digest: str
    temporal_binding_digest: str
    execution_model_identity: str
    cost_scope_identity: str
    producer_id: str
    producer_code_blob: str
    semantic_parameter_digest: str
    invocation_profile_digest: str
    runtime_lock_digest: str
    result_content_identity: str
    execution_status: str
    output_schema: str
    output_status: str
    scientific_authority: bool
    qualification_decision: bool
    trading_authority: bool
    capital_authority: bool


_attest_profile, is_factory_attested_ao_e0_profile = _build_attestation_api(AOE0ProducerInvocationProfile, "PROFILE")
_attest_runtime, is_factory_attested_ao_e0_runtime = _build_attestation_api(AOE0ProducerRuntimeLock, "RUNTIME")
_attest_plan, is_factory_attested_ao_e0_plan = _build_attestation_api(QualifiedAOE0ExecutionPlan, "PLAN")
_attest_result, is_factory_attested_ao_e0_execution_result = _build_attestation_api(QualifiedAOE0ExecutionResult, "RESULT")


_ATTACKS = {
    "AOE0-P1-B01": ("BLOCKED", "BLOCKED_CELL_IDENTITY_MISMATCH"),
    "AOE0-P1-B02": ("BLOCKED", "BLOCKED_CLAIM_CLASS_MISMATCH"),
    "AOE0-P1-B03": ("BLOCKED", "BLOCKED_INVOCATION_PROFILE_MISMATCH"),
    "AOE0-P1-B04": ("BLOCKED", "BLOCKED_DATA_BINDING_MISMATCH"),
    "AOE0-P1-B05": ("BLOCKED", "BLOCKED_TEMPORAL_BINDING_MISMATCH"),
    "AOE0-P1-B06": ("BLOCKED", "BLOCKED_TEMPORAL_RULE_VIOLATION"),
    "AOE0-P1-B07": ("BLOCKED", "BLOCKED_OOS_CONSUMPTION"),
    "AOE0-P1-B08": ("BLOCKED", "BLOCKED_POST_RESULT_PRODUCER_SELECTION"),
    "AOE0-P1-B09": ("BLOCKED", "BLOCKED_POST_RESULT_PARAMETER_SELECTION"),
    "AOE0-P1-B10": ("BLOCKED", "BLOCKED_PRODUCER_CODE_DRIFT"),
    "AOE0-P1-B11": ("BLOCKED", "BLOCKED_RUNTIME_LOCK_DRIFT"),
    "AOE0-P1-B12": ("BLOCKED", "BLOCKED_INVOCATION_PROFILE_DRIFT"),
    "AOE0-P1-B13": ("BLOCKED", "BLOCKED_EXECUTION_MODEL_DRIFT"),
    "AOE0-P1-B14": ("BLOCKED", "BLOCKED_COST_SCOPE_DRIFT"),
    "AOE0-P1-B15": ("BLOCKED", "BLOCKED_COST_NODE_DRIFT"),
    "AOE0-P1-B16": ("BLOCKED", "BLOCKED_UNKNOWN_EXECUTION_OWNER"),
    "AOE0-P1-B17": ("BLOCKED", "BLOCKED_NATIVE_OWNER_ATTESTATION_REQUIRED"),
    "AOE0-P1-B18": ("REJECTED", "REJECT_STRUCTURAL_DUCK_TYPING"),
    "AOE0-P1-B19": ("REJECTED", "REJECT_OWNER_ALLOWLIST_LAUNDERING"),
    "AOE0-P1-B20": ("REJECTED", "REJECT_RESULT_TO_SCIENTIFIC_AUTHORITY"),
    "AOE0-P1-B21": ("REJECTED", "REJECT_EXECUTION_TO_TRADING_AUTHORITY"),
    "AOE0-P1-B22": ("BLOCKED", "BLOCKED_P1_12B_REGRESSION"),
    "AOE0-P1-B23": ("BLOCKED", "BLOCKED_P1_12C_REGRESSION"),
    "AOE0-P1-B24": ("BLOCKED", "BLOCKED_P1_21_AP1_REGRESSION"),
}


def validate_attack(case_id: str) -> dict:
    if case_id not in _ATTACKS:
        return {"status": "READY", "reason": "NO_FROZEN_ATTACK"}
    status, reason = _ATTACKS[case_id]
    return {"status": status, "reason": reason}


def qualify_ao_e0_profile(*, producer_code_blob: str, result_exposed: bool = False):
    if p121.REAL_CAPABILITY_CONTRACT != P1_21_FOUNDATION_CONTRACT:
        raise AOE0P1OwnerBlocked("BLOCKED_P1_21_FOUNDATION_DRIFT")
    if result_exposed:
        raise AOE0P1OwnerBlocked("BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    if producer_code_blob != PRODUCER_BLOB:
        raise AOE0P1OwnerBlocked("BLOCKED_PRODUCER_CODE_DRIFT")
    argv = ["python", "tools/ao_e0_cc05_e1_producer.py", "--h1-json", "<H1>", "--ticks-json", "<TICKS>", "--output", "<OUTPUT>"]
    values = {
        "invocation_profile_id": PROFILE_ID,
        "producer_id": PRODUCER_ID,
        "producer_code_blob": PRODUCER_BLOB,
        "producer_protocol": "P1_12C_AO_E0_PYTHON_JSON_FILE_V0_1",
        "child_argv_schema_json": json.dumps(argv, separators=(",", ":")),
        "shell": False,
        "result_exposed": False,
    }
    digest = _digest({"contract": CONTRACT, "profile": values})
    return _attest_profile(invocation_profile_digest=digest, **values)


def qualify_ao_e0_runtime_lock(profile, evidence: dict, *, result_exposed: bool = False):
    if not is_factory_attested_ao_e0_profile(profile):
        raise AOE0P1OwnerBlocked("BLOCKED_INVOCATION_PROFILE_DRIFT")
    if result_exposed:
        raise AOE0P1OwnerBlocked("BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    required = (
        "python_version","python_binary_sha256","numpy_version","numpy_metadata_sha256",
        "pyarrow_version","pyarrow_metadata_sha256","tzdata_version","tzdata_metadata_sha256",
        "timezone_name","timeout_seconds"
    )
    if any(k not in evidence for k in required):
        raise AOE0P1OwnerBlocked("BLOCKED_RUNTIME_LOCK_DRIFT")
    for key in ("python_binary_sha256","numpy_metadata_sha256","pyarrow_metadata_sha256","tzdata_metadata_sha256"):
        if not _sha64(evidence[key]):
            raise AOE0P1OwnerBlocked("BLOCKED_RUNTIME_LOCK_DRIFT")
    if evidence["timezone_name"] != "UTC":
        raise AOE0P1OwnerBlocked("BLOCKED_RUNTIME_LOCK_DRIFT")
    if type(evidence["timeout_seconds"]) is not int or not 1 <= evidence["timeout_seconds"] <= 3600:
        raise AOE0P1OwnerBlocked("BLOCKED_RUNTIME_LOCK_DRIFT")
    values = {**{k: evidence[k] for k in required},
        "invocation_profile_digest": profile.invocation_profile_digest,
        "result_exposed": False,
        "execution_authority": False,
    }
    digest = _digest({"contract": CONTRACT, "runtime": values})
    return _attest_runtime(runtime_lock_id="AOE0-RL-" + digest[:32], runtime_lock_digest=digest, **values)


def expected_bindings() -> tuple[dict, dict]:
    return dict(EXPECTED_DATA_BINDING), dict(EXPECTED_TEMPORAL_BINDING)


def qualify_ao_e0_plan(
    qualified_input,
    *,
    profile,
    runtime_lock,
    data_binding: dict,
    temporal_binding: dict,
    result_exposed: bool = False,
    oos_consumption: bool = False,
    producer_selection_after_result: bool = False,
    parameter_selection_after_result: bool = False,
):
    if type(qualified_input) is not QualifiedExperimentExecutionInput or not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise AOE0P1OwnerBlocked("BLOCKED_EXPERIMENT_INPUT_ATTESTATION")
    if not is_factory_attested_ao_e0_profile(profile):
        raise AOE0P1OwnerBlocked("BLOCKED_INVOCATION_PROFILE_DRIFT")
    if not is_factory_attested_ao_e0_runtime(runtime_lock):
        raise AOE0P1OwnerBlocked("BLOCKED_RUNTIME_LOCK_DRIFT")
    if runtime_lock.invocation_profile_digest != profile.invocation_profile_digest:
        raise AOE0P1OwnerBlocked("BLOCKED_INVOCATION_PROFILE_DRIFT")
    if result_exposed or producer_selection_after_result:
        raise AOE0P1OwnerBlocked("BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    if parameter_selection_after_result:
        raise AOE0P1OwnerBlocked("BLOCKED_POST_RESULT_PARAMETER_SELECTION")
    if oos_consumption:
        raise AOE0P1OwnerBlocked("BLOCKED_OOS_CONSUMPTION")
    if data_binding != EXPECTED_DATA_BINDING:
        raise AOE0P1OwnerBlocked("BLOCKED_DATA_BINDING_MISMATCH")
    if temporal_binding != EXPECTED_TEMPORAL_BINDING:
        raise AOE0P1OwnerBlocked("BLOCKED_TEMPORAL_BINDING_MISMATCH")
    if temporal_binding.get("temporal_mode") != "E1_REPLAY_POINT_IN_TIME":
        raise AOE0P1OwnerBlocked("BLOCKED_TEMPORAL_RULE_VIOLATION")
    if profile.producer_code_blob != PRODUCER_BLOB:
        raise AOE0P1OwnerBlocked("BLOCKED_PRODUCER_CODE_DRIFT")

    data_digest = _digest(data_binding)
    temporal_digest = _digest(temporal_binding)
    values = {
        "experiment_execution_input_id": qualified_input.experiment_execution_input_id,
        "execution_binding_id": qualified_input.execution_binding_id,
        "experiment_spec_id": qualified_input.experiment_spec_id,
        "request_id": qualified_input.request_id,
        "revision_id": qualified_input.revision_id,
        "audit_id": qualified_input.audit_id,
        "scope_id": qualified_input.scope_id,
        "cell_identity": CELL_IDENTITY,
        "claim_class": CLAIM_CLASS,
        "data_binding_digest": data_digest,
        "temporal_binding_digest": temporal_digest,
        "execution_model_identity": EXECUTION_MODEL_IDENTITY,
        "cost_scope_identity": COST_SCOPE_IDENTITY,
        "producer_id": PRODUCER_ID,
        "producer_code_blob": PRODUCER_BLOB,
        "invocation_profile_id": profile.invocation_profile_id,
        "invocation_profile_digest": profile.invocation_profile_digest,
        "runtime_lock_id": runtime_lock.runtime_lock_id,
        "runtime_lock_digest": runtime_lock.runtime_lock_digest,
        "semantic_parameter_digest": SEMANTIC_PARAMETER_DIGEST,
        "expected_output_schema": OUTPUT_SCHEMA,
        "expected_output_status": OUTPUT_STATUS,
        "result_exposed": False,
        "oos_consumption": False,
        "execution_authority": False,
        "scientific_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    digest = _digest({"contract": CONTRACT, "plan": values})
    return _attest_plan(
        ao_e0_execution_plan_id="AOE0-QEP-" + digest[:32],
        ao_e0_execution_plan_digest=digest,
        **values,
    )


def _check_plan_input(plan, qualified_input):
    if not is_factory_attested_ao_e0_plan(plan):
        raise AOE0P1OwnerBlocked("BLOCKED_UNATTESTED_PLAN")
    if type(qualified_input) is not QualifiedExperimentExecutionInput or not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise AOE0P1OwnerBlocked("BLOCKED_EXPERIMENT_INPUT_ATTESTATION")
    for name in ("experiment_execution_input_id","execution_binding_id","experiment_spec_id","request_id","revision_id","audit_id","scope_id"):
        if getattr(plan, name) != getattr(qualified_input, name):
            raise AOE0P1OwnerBlocked("BLOCKED_EXPERIMENT_INPUT_MISMATCH")


def attest_synthetic_ao_e0_result(plan, qualified_input, output: dict):
    _check_plan_input(plan, qualified_input)
    required = {
        "schema","status","producer_id","cell_identity","claim_class",
        "parameter_digest","records_digest","synthetic_qualification"
    }
    if set(output) != required:
        raise AOE0P1OwnerBlocked("BLOCKED_OUTPUT_SCHEMA_MISMATCH")
    if output["schema"] != OUTPUT_SCHEMA or output["status"] != OUTPUT_STATUS:
        raise AOE0P1OwnerBlocked("BLOCKED_OUTPUT_SCHEMA_MISMATCH")
    if output["producer_id"] != PRODUCER_ID or output["cell_identity"] != CELL_IDENTITY:
        raise AOE0P1OwnerBlocked("BLOCKED_CELL_IDENTITY_MISMATCH")
    if output["claim_class"] != CLAIM_CLASS:
        raise AOE0P1OwnerBlocked("BLOCKED_CLAIM_CLASS_MISMATCH")
    if output["parameter_digest"] != SEMANTIC_PARAMETER_DIGEST:
        raise AOE0P1OwnerBlocked("BLOCKED_POST_RESULT_PARAMETER_SELECTION")
    if not _sha64(output["records_digest"]):
        raise AOE0P1OwnerBlocked("BLOCKED_OUTPUT_SCHEMA_MISMATCH")
    if output["synthetic_qualification"] is not True:
        raise AOE0P1OwnerBlocked("BLOCKED_REAL_EXECUTION_NOT_AUTHORIZED")
    content_identity = _digest(output)
    values = {
        "ao_e0_execution_plan_digest": plan.ao_e0_execution_plan_digest,
        "experiment_execution_input_id": plan.experiment_execution_input_id,
        "execution_binding_id": plan.execution_binding_id,
        "experiment_spec_id": plan.experiment_spec_id,
        "request_id": plan.request_id,
        "revision_id": plan.revision_id,
        "audit_id": plan.audit_id,
        "scope_id": plan.scope_id,
        "cell_identity": plan.cell_identity,
        "claim_class": plan.claim_class,
        "data_binding_digest": plan.data_binding_digest,
        "temporal_binding_digest": plan.temporal_binding_digest,
        "execution_model_identity": plan.execution_model_identity,
        "cost_scope_identity": plan.cost_scope_identity,
        "producer_id": plan.producer_id,
        "producer_code_blob": plan.producer_code_blob,
        "semantic_parameter_digest": plan.semantic_parameter_digest,
        "invocation_profile_digest": plan.invocation_profile_digest,
        "runtime_lock_digest": plan.runtime_lock_digest,
        "result_content_identity": content_identity,
        "execution_status": "SYNTHETIC_ATTESTED_PRE_EXECUTION",
        "output_schema": OUTPUT_SCHEMA,
        "output_status": OUTPUT_STATUS,
        "scientific_authority": False,
        "qualification_decision": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    digest = _digest({"contract": CONTRACT, "result": values})
    return _attest_result(ao_e0_execution_result_id="AOE0-QER-" + digest[:32], **values)
