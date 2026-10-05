"""P1.12C claim-scoped qualified producer execution boundary.

This is a sibling of P1.12B. It binds one exact P1.11B qualified experiment
input to one exact pre-result producer plan, invokes only the bound Python-file
producer protocol, verifies source immutability and exact output identity, and
mints a process-local P1.12C result.

It does NOT create P1.13B evaluations/findings, Data validity, scientific
support, trading authority, or real-execution authority.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import weakref
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping

from src.data import claim_scoped_admission as data02
from src.qualified_experiment_execution_input import (
    QualifiedExperimentExecutionInput,
    is_factory_attested_qualified_experiment_execution_input,
)
from src.research.input_binding import corpus_inventory_hash

CONTRACT = "P1_12C_CLAIM_SCOPED_QUALIFIED_PRODUCER_EXECUTION_V1"
PRODUCER_PROTOCOL = "P1_12C_PYTHON_JSON_FILE_V1"
SYNTHETIC_OUTPUT_SCHEMA = "ATDS_P1_18_SYNTHETIC_PRODUCER_OUTPUT_V0_1"
SYNTHETIC_OUTPUT_STATUS = "SYNTHETIC_COMPLETE"
RVO_AUTHORITY = "NONE"

CAPABILITIES = {
    "qualified_producer_execution": True,
    "generic_arbitrary_command_execution": False,
    "data_validity": False,
    "p1_finding": False,
    "scientific_authority": False,
    "operational_authority": False,
    "trading_authority": False,
    "capital_authority": False,
    "real_ap1_authority": False,
    "oos_consumption": False,
}

_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
_GIT_BLOB_RE = re.compile(r"[0-9a-f]{40}\Z")


class P112CBlocked(RuntimeError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedProducerExecutionPlan:
    producer_execution_plan_id: str
    producer_execution_plan_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    corpus_root_transport: str
    expected_corpus_hash: str
    data02_admission_digest: str
    claim_scope_id: str
    dataset_identity: str
    data02_dataset_file_set_digest: str
    ap0_manifest_sha256: str
    schema_identity: str
    source_identity: str
    usage_envelope_id: str
    producer_id: str
    producer_code_blob: str
    producer_path_transport: str
    producer_entrypoint: str
    semantic_parameters_json: str
    producer_semantic_parameter_digest: str
    producer_invocation_contract_json: str
    producer_invocation_contract_digest: str
    runtime_lock_json: str
    runtime_lock_digest: str
    expected_output_schema: str
    expected_output_status: str
    expected_output_contract: str
    maximum_output_bytes: int
    result_exposed: bool
    temporal_scope: str
    oos_consumption: bool
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedProducerExecutionResult:
    producer_execution_result_id: str
    producer_execution_plan_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    data02_admission_digest: str
    dataset_identity: str
    data02_dataset_file_set_digest: str
    dataset_file_set_digest_before: str
    dataset_file_set_digest_after: str
    producer_id: str
    producer_code_blob: str
    producer_parameter_digest: str
    runtime_lock_digest: str
    execution_status: str
    exit_code: int
    output_schema: str
    output_status: str
    output_size_bytes: int
    output_sha256: str
    result_identity: str
    data02_result_binding_digest: str
    producer_stdout_digest: str
    producer_stderr_digest: str
    reconstruction_class: str
    reconstruction_descriptor_digest: str
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sha256_path(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: str | Path) -> str:
    raw = Path(path).read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _decision(status: str, reason: str, **extra: object) -> dict[str, Any]:
    out: dict[str, Any] = {
        "contract": CONTRACT,
        "status": status,
        "reason": reason,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
        "rvo_authority": RVO_AUTHORITY,
    }
    out.update(extra)
    return out


def build_current_runtime_lock() -> dict[str, Any]:
    executable = Path(sys.executable)
    lock = {
        "schema": "P1_12C_SYNTHETIC_RUNTIME_LOCK_V1",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_executable_sha256": _sha256_path(executable),
        "timezone_database_identity": "NOT_USED_BY_SYNTHETIC_PRODUCER",
        "material_third_party_dependencies": [],
        "deterministic_environment": {
            "PYTHONHASHSEED": "0",
            "TZ": "UTC",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "P1_12C_NETWORK_POLICY": "AUDIT_BLOCKED",
        },
    }
    return {**lock, "runtime_lock_digest": _digest(lock)}


def _runner_path() -> Path:
    return Path(__file__).resolve().parents[1] / "tools" / "p1_12c_sandbox_runner.py"


def _invocation_contract(runner: Path) -> dict[str, Any]:
    body = {
        "protocol": PRODUCER_PROTOCOL,
        "interpreter": "CURRENT_BOUND_CPYTHON",
        "structured_arguments": True,
        "shell": False,
        "network_policy": "PYTHON_AUDIT_HOOK_BLOCK_SOCKET_AND_CHILD_PROCESS",
        "timeout_seconds": 10,
        "working_directory_policy": "REPOSITORY_ROOT",
        "source_transport_identity_authority": False,
        "output_transport_identity_authority": False,
        "sandbox_runner_sha256": _sha256_path(runner),
    }
    return body


def _plan_identity_payload(values: Mapping[str, Any]) -> dict[str, Any]:
    excluded = {
        "producer_execution_plan_id",
        "producer_execution_plan_digest",
        "corpus_root_transport",
        "producer_path_transport",
    }
    return {"contract": CONTRACT, **{k: values[k] for k in sorted(values) if k not in excluded}}


def _plan_fingerprint(value: QualifiedProducerExecutionPlan) -> str:
    return _digest({"contract": CONTRACT, "plan": asdict(value)})


def _result_fingerprint(value: QualifiedProducerExecutionResult) -> str:
    return _digest({"contract": CONTRACT, "result": asdict(value)})


def _build_attestation_api(cls, fingerprint):
    registry: dict[int, tuple[weakref.ReferenceType, str]] = {}

    def attest(**values):
        produced = cls(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not cls:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if fingerprint(value) != expected:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


_attest_plan, is_factory_attested_qualified_producer_execution_plan = _build_attestation_api(
    QualifiedProducerExecutionPlan, _plan_fingerprint
)
_attest_result, is_factory_attested_qualified_producer_execution_result = _build_attestation_api(
    QualifiedProducerExecutionResult, _result_fingerprint
)
del _build_attestation_api


def validate_plan_candidate(candidate: Mapping[str, Any], frozen_reference: Mapping[str, Any]) -> dict[str, Any]:
    if not candidate.get("producer_code_blob"):
        return _decision("BLOCKED", "BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
    if candidate.get("dataset_identity") != frozen_reference.get("dataset_identity"):
        return _decision("BLOCKED", "BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    if candidate.get("producer_semantic_parameter_digest") != frozen_reference.get("producer_semantic_parameter_digest"):
        return _decision("BLOCKED", "BLOCKED_PRODUCER_PARAMETER_DRIFT")
    if candidate.get("producer_code_blob") != frozen_reference.get("producer_code_blob"):
        return _decision("BLOCKED", "BLOCKED_PRODUCER_CODE_DRIFT")
    if candidate.get("experiment_spec_id") != frozen_reference.get("experiment_spec_id"):
        return _decision("BLOCKED", "BLOCKED_EXPERIMENT_SPEC_BINDING_MISMATCH")
    if candidate.get("result_exposed") is True:
        return _decision("BLOCKED", "BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    if candidate.get("temporal_scope") != "RETROSPECTIVE_DESCRIPTIVE_ONLY":
        return _decision("BLOCKED", "BLOCKED_TEMPORAL_SCOPE_ESCALATION")
    if candidate.get("oos_consumption") is True:
        return _decision("BLOCKED", "BLOCKED_OOS_CONSUMPTION")
    if candidate.get("owner_rewrite") is True:
        return _decision("REJECTED", "REJECT_OWNER_REWRITE_FOR_INTEGRATION")
    if not candidate.get("runtime_lock_digest") or candidate.get("runtime_lock_digest") != frozen_reference.get("runtime_lock_digest"):
        return _decision("BLOCKED", "BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    if candidate.get("path_as_identity") is True:
        return _decision("REJECTED", "REJECT_PATH_AS_IDENTITY")
    return _decision("READY", "PLAN_CANDIDATE_PRESERVES_FROZEN_BINDING")


def compute_result_identity(result: Mapping[str, Any]) -> str:
    material_keys = (
        "producer_execution_plan_digest",
        "experiment_execution_input_id",
        "execution_binding_id",
        "experiment_spec_id",
        "dataset_identity",
        "dataset_file_set_digest_before",
        "dataset_file_set_digest_after",
        "producer_id",
        "producer_code_blob",
        "producer_parameter_digest",
        "runtime_lock_digest",
        "execution_status",
        "exit_code",
        "output_schema",
        "output_status",
        "output_size_bytes",
        "output_sha256",
        "data02_result_binding_digest",
        "producer_stdout_digest",
        "producer_stderr_digest",
        "reconstruction_class",
        "reconstruction_descriptor_digest",
    )
    material = {key: result.get(key) for key in material_keys}
    return "QPER-" + _digest({"contract": CONTRACT, "result_identity_material": material})[:32]


def validate_result_candidate(result: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    if not result.get("dataset_identity"):
        return _decision("BLOCKED", "BLOCKED_RESULT_DATASET_IDENTITY_REQUIRED")
    if not result.get("execution_binding_id"):
        return _decision("BLOCKED", "BLOCKED_EXECUTION_BINDING_IDENTITY_REQUIRED")
    if result.get("observed_output_sha256") is not None and result.get("observed_output_sha256") != result.get("output_sha256"):
        return _decision("BLOCKED", "BLOCKED_OUTPUT_IDENTITY_MISMATCH")
    if result.get("producer_mutated_source") is True:
        return _decision("BLOCKED", "BLOCKED_SOURCE_MUTATION_DURING_PRODUCER_EXECUTION")
    if result.get("dataset_file_set_digest_before") != result.get("dataset_file_set_digest_after"):
        return _decision("BLOCKED", "BLOCKED_SOURCE_IMMUTABILITY_FAILURE")
    if result.get("output_schema") != plan.get("expected_output_schema"):
        return _decision("BLOCKED", "BLOCKED_PRODUCER_OUTPUT_SCHEMA_MISMATCH")
    if result.get("output_status") != plan.get("expected_output_status"):
        return _decision("BLOCKED", "BLOCKED_PRODUCER_OUTPUT_STATUS_MISMATCH")
    if result.get("result_identity") != compute_result_identity(result):
        return _decision("BLOCKED", "BLOCKED_RESULT_ID_CONTENT_COLLISION")
    return _decision("READY", "RESULT_CANDIDATE_PRESERVES_FROZEN_BINDING")


_BOUNDARY_REJECTIONS = {
    "PATH_OR_FILENAME_AUTHORITY": ("REJECTED", "REJECT_PATH_OR_FILENAME_AUTHORITY"),
    "RVO_PRODUCER_AUTHORITY": ("REJECTED", "REJECT_RVO_PRODUCER_AUTHORITY"),
    "DATA_PASS_TO_EXECUTION_PASS": ("REJECTED", "REJECT_DATA_TO_EXECUTION_LAUNDERING"),
    "EXECUTION_TO_P1_FINDING": ("REJECTED", "REJECT_EXECUTION_TO_FINDING_LAUNDERING"),
    "RESULT_TO_SCIENTIFIC_SUPPORT": ("REJECTED", "REJECT_RESULT_TO_SCIENCE_LAUNDERING"),
    "RUNTIME_ATTESTATION_TO_DURABLE_RECONSTRUCTION": ("BLOCKED", "BLOCKED_RUNTIME_ATTESTATION_NOT_DURABLE"),
    "EXTERNAL_RESULT_WITHOUT_REPLAY_EVIDENCE": ("BLOCKED", "BLOCKED_EXTERNAL_RESULT_REPLAY_EVIDENCE_REQUIRED"),
    "DUPLICATE_AP1_LOGIC_INSIDE_P1": ("REJECTED", "REJECT_PRODUCER_SEMANTIC_DUPLICATION"),
    "RELABEL_AP0_AS_BI5": ("REJECTED", "REJECT_LEGACY_ENGINE_FORMAT_LAUNDERING"),
    "EXECUTION_GRANTS_TRADING_OR_CAPITAL": ("REJECTED", "REJECT_EXECUTION_AUTHORITY_ESCALATION"),
    "FORGE_P1_12B_RESULT": ("REJECTED", "REJECT_P1_12B_RESULT_SEMANTIC_LAUNDERING"),
    "BYPASS_P1_13B_TYPE_CONTRACT": ("BLOCKED", "BLOCKED_DOWNSTREAM_RESULT_TYPE_CONTRACT"),
    "DIGEST_ONLY_EXTERNAL_AUTHORITY": ("REJECTED", "REJECT_DIGEST_ONLY_EXTERNAL_AUTHORITY"),
}


def validate_boundary_claim(claim: str) -> dict[str, Any]:
    if claim not in _BOUNDARY_REJECTIONS:
        return _decision("READY", "NO_BOUNDARY_ESCALATION")
    status, reason = _BOUNDARY_REJECTIONS[claim]
    return _decision(status, reason)


def qualify_producer_execution_plan(
    qualified_input,
    data_admission: Mapping[str, Any],
    *,
    producer_id: str,
    producer_path: str | Path,
    semantic_parameters: Mapping[str, Any],
    expected_output_schema: str,
    expected_output_status: str,
    expected_output_contract: str,
    maximum_output_bytes: int,
    result_exposed: bool = False,
    temporal_scope: str = "RETROSPECTIVE_DESCRIPTIVE_ONLY",
    oos_consumption: bool = False,
) -> QualifiedProducerExecutionPlan:
    if type(qualified_input) is not QualifiedExperimentExecutionInput:
        raise TypeError("P1.12C requires exact QualifiedExperimentExecutionInput")
    if not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise ValueError("P1.12C requires currently-attested P1.11B input")
    if result_exposed:
        raise P112CBlocked("BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    if temporal_scope != "RETROSPECTIVE_DESCRIPTIVE_ONLY":
        raise P112CBlocked("BLOCKED_TEMPORAL_SCOPE_ESCALATION")
    if oos_consumption:
        raise P112CBlocked("BLOCKED_OOS_CONSUMPTION")
    if data_admission.get("status") != "READY_FOR_EXACT_CLAIM":
        raise P112CBlocked("BLOCKED_DATA02_ADMISSION_REQUIRED")
    basis = data_admission.get("binding_basis")
    if not isinstance(basis, Mapping):
        raise P112CBlocked("BLOCKED_DATA02_ADMISSION_REQUIRED")
    if basis.get("dataset_identity") != data02.DATASET_IDENTITY:
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    if not data_admission.get("admission_digest"):
        raise P112CBlocked("BLOCKED_DATA02_ADMISSION_REQUIRED")

    current_corpus = corpus_inventory_hash(qualified_input.corpus_root)
    if current_corpus != qualified_input.expected_corpus_hash:
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")

    producer = Path(producer_path)
    if not producer.is_file():
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
    producer_blob = git_blob_sha1(producer)
    if _GIT_BLOB_RE.fullmatch(producer_blob) is None:
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")

    if not isinstance(semantic_parameters, Mapping):
        raise TypeError("semantic_parameters must be a mapping")
    semantic_json = json.dumps(dict(semantic_parameters), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    parameter_digest = hashlib.sha256(semantic_json.encode("utf-8")).hexdigest()

    runner = _runner_path()
    if not runner.is_file():
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    invocation = _invocation_contract(runner)
    invocation_json = json.dumps(invocation, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    invocation_digest = hashlib.sha256(invocation_json.encode("utf-8")).hexdigest()

    runtime_lock = build_current_runtime_lock()
    runtime_lock_digest = str(runtime_lock["runtime_lock_digest"])
    runtime_json = json.dumps(runtime_lock, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    if type(maximum_output_bytes) is not int or maximum_output_bytes <= 0:
        raise ValueError("maximum_output_bytes must be positive exact int")

    values: dict[str, Any] = {
        "experiment_execution_input_id": qualified_input.experiment_execution_input_id,
        "execution_binding_id": qualified_input.execution_binding_id,
        "experiment_spec_id": qualified_input.experiment_spec_id,
        "request_id": qualified_input.request_id,
        "revision_id": qualified_input.revision_id,
        "audit_id": qualified_input.audit_id,
        "scope_id": qualified_input.scope_id,
        "corpus_root_transport": str(Path(qualified_input.corpus_root).resolve()),
        "expected_corpus_hash": qualified_input.expected_corpus_hash,
        "data02_admission_digest": str(data_admission["admission_digest"]),
        "claim_scope_id": str(basis["claim_scope_id"]),
        "dataset_identity": str(basis["dataset_identity"]),
        "data02_dataset_file_set_digest": str(basis["dataset_file_set_digest"]),
        "ap0_manifest_sha256": str(basis["ap0_manifest_sha256"]),
        "schema_identity": str(basis["schema_identity"]),
        "source_identity": str(basis["source_identity"]),
        "usage_envelope_id": str(basis["usage_envelope_id"]),
        "producer_id": str(producer_id),
        "producer_code_blob": producer_blob,
        "producer_path_transport": str(producer.resolve()),
        "producer_entrypoint": "__main__",
        "semantic_parameters_json": semantic_json,
        "producer_semantic_parameter_digest": parameter_digest,
        "producer_invocation_contract_json": invocation_json,
        "producer_invocation_contract_digest": invocation_digest,
        "runtime_lock_json": runtime_json,
        "runtime_lock_digest": runtime_lock_digest,
        "expected_output_schema": str(expected_output_schema),
        "expected_output_status": str(expected_output_status),
        "expected_output_contract": str(expected_output_contract),
        "maximum_output_bytes": maximum_output_bytes,
        "result_exposed": False,
        "temporal_scope": temporal_scope,
        "oos_consumption": False,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    plan_digest = _digest(_plan_identity_payload(values))
    plan_id = "QPEP-" + plan_digest[:32]
    return _attest_plan(
        producer_execution_plan_id=plan_id,
        producer_execution_plan_digest=plan_digest,
        **values,
    )


def _validate_execution_bindings(
    plan: QualifiedProducerExecutionPlan,
    qualified_input: QualifiedExperimentExecutionInput,
    data_admission: Mapping[str, Any],
) -> None:
    if not is_factory_attested_qualified_producer_execution_plan(plan):
        raise P112CBlocked("BLOCKED_UNATTESTED_PRODUCER_PLAN")
    if type(qualified_input) is not QualifiedExperimentExecutionInput or not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise P112CBlocked("BLOCKED_EXPERIMENT_SPEC_BINDING_MISMATCH")
    if (
        plan.experiment_execution_input_id != qualified_input.experiment_execution_input_id
        or plan.execution_binding_id != qualified_input.execution_binding_id
        or plan.experiment_spec_id != qualified_input.experiment_spec_id
    ):
        raise P112CBlocked("BLOCKED_EXPERIMENT_SPEC_BINDING_MISMATCH")
    if data_admission.get("admission_digest") != plan.data02_admission_digest:
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    basis = data_admission.get("binding_basis")
    if not isinstance(basis, Mapping):
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")
    if basis.get("dataset_identity") != plan.dataset_identity or basis.get("dataset_file_set_digest") != plan.data02_dataset_file_set_digest:
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")


def _bounded_environment() -> dict[str, str]:
    return {
        "PYTHONHASHSEED": "0",
        "TZ": "UTC",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "P1_12C_NETWORK_POLICY": "AUDIT_BLOCKED",
    }


def run_qualified_producer(
    plan,
    qualified_input,
    data_admission: Mapping[str, Any],
) -> QualifiedProducerExecutionResult:
    if type(plan) is not QualifiedProducerExecutionPlan:
        raise TypeError("P1.12C requires exact QualifiedProducerExecutionPlan")
    _validate_execution_bindings(plan, qualified_input, data_admission)

    producer_path = Path(plan.producer_path_transport)
    if not producer_path.is_file() or git_blob_sha1(producer_path) != plan.producer_code_blob:
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_DRIFT")
    if build_current_runtime_lock()["runtime_lock_digest"] != plan.runtime_lock_digest:
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")

    pre_source = corpus_inventory_hash(qualified_input.corpus_root)
    if pre_source != qualified_input.expected_corpus_hash:
        raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")

    runner = _runner_path()
    invocation = json.loads(plan.producer_invocation_contract_json)
    if _digest(invocation) != plan.producer_invocation_contract_digest:
        raise P112CBlocked("BLOCKED_PRODUCER_PARAMETER_DRIFT")
    if _sha256_path(runner) != invocation.get("sandbox_runner_sha256"):
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")

    parameters = json.loads(plan.semantic_parameters_json)
    if _digest(parameters) != plan.producer_semantic_parameter_digest:
        raise P112CBlocked("BLOCKED_PRODUCER_PARAMETER_DRIFT")

    repository_root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="p1-12c-") as tmp:
        isolated = Path(tmp)
        params_path = isolated / "parameters.json"
        output_path = isolated / "producer-output.json"
        params_path.write_bytes(_canonical_bytes(parameters) + b"\n")

        command = [
            sys.executable,
            "-I",
            str(runner),
            "--producer",
            str(producer_path),
            "--source-root",
            str(Path(qualified_input.corpus_root).resolve()),
            "--parameters",
            str(params_path),
            "--output",
            str(output_path),
            "--producer-id",
            plan.producer_id,
        ]
        try:
            completed = subprocess.run(
                command,
                shell=False,
                cwd=str(repository_root),
                env=_bounded_environment(),
                capture_output=True,
                timeout=int(invocation["timeout_seconds"]),
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise P112CBlocked("BLOCKED_PRODUCER_EXECUTION_TIMEOUT") from exc

        post_source = corpus_inventory_hash(qualified_input.corpus_root)
        if pre_source != post_source:
            raise P112CBlocked("BLOCKED_SOURCE_MUTATION_DURING_PRODUCER_EXECUTION")
        if completed.returncode != 0:
            raise P112CBlocked("BLOCKED_PRODUCER_EXECUTION_FAILED")
        if not output_path.is_file():
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_MISSING")
        raw = output_path.read_bytes()
        if len(raw) > plan.maximum_output_bytes:
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SIZE")
        try:
            output = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SCHEMA_MISMATCH") from exc
        canonical_raw = _canonical_bytes(output) + b"\n"
        if raw != canonical_raw:
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SCHEMA_MISMATCH")
        if output.get("schema") != plan.expected_output_schema:
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SCHEMA_MISMATCH")
        if output.get("status") != plan.expected_output_status:
            raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_STATUS_MISMATCH")
        if output.get("producer_id") != plan.producer_id:
            raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
        if output.get("source_inventory_sha256") != pre_source:
            raise P112CBlocked("BLOCKED_RESULT_DATASET_IDENTITY_REQUIRED")
        if output.get("parameter_digest") != plan.producer_semantic_parameter_digest:
            raise P112CBlocked("BLOCKED_PRODUCER_PARAMETER_DRIFT")

        output_sha = hashlib.sha256(raw).hexdigest()
        basis = data_admission["binding_basis"]
        data_binding = {
            "claim_scope_id": basis["claim_scope_id"],
            "dataset_identity": basis["dataset_identity"],
            "ap0_manifest_sha256": basis["ap0_manifest_sha256"],
            "dataset_file_set_digest": basis["dataset_file_set_digest"],
            "schema_identity": basis["schema_identity"],
            "source_identity": basis["source_identity"],
            "transformer_blob": basis["transformer_blob"],
            "usage_envelope_id": basis["usage_envelope_id"],
            "data_admissibility_evidence_ref": data_admission["admission_digest"],
            "result_identity": output_sha,
        }
        bound = data02.validate_result_binding(data_admission, data_binding)
        if bound.get("status") != "BOUND_TO_EXACT_DATASET":
            raise P112CBlocked("BLOCKED_DATASET_SUBSTITUTION_AFTER_ADMISSION")

        stdout_digest = hashlib.sha256(completed.stdout).hexdigest()
        stderr_digest = hashlib.sha256(completed.stderr).hexdigest()
        reconstruction_material = {
            "experiment_execution_input_id": plan.experiment_execution_input_id,
            "data02_admission_digest": plan.data02_admission_digest,
            "source_inventory_sha256": pre_source,
            "producer_code_blob": plan.producer_code_blob,
            "producer_parameter_digest": plan.producer_semantic_parameter_digest,
            "runtime_lock_digest": plan.runtime_lock_digest,
            "invocation_contract_digest": plan.producer_invocation_contract_digest,
            "output_sha256": output_sha,
        }
        reconstruction_digest = _digest(reconstruction_material)

        candidate: dict[str, Any] = {
            "producer_execution_plan_digest": plan.producer_execution_plan_digest,
            "experiment_execution_input_id": plan.experiment_execution_input_id,
            "execution_binding_id": plan.execution_binding_id,
            "experiment_spec_id": plan.experiment_spec_id,
            "dataset_identity": plan.dataset_identity,
            "dataset_file_set_digest_before": pre_source,
            "dataset_file_set_digest_after": post_source,
            "producer_id": plan.producer_id,
            "producer_code_blob": plan.producer_code_blob,
            "producer_parameter_digest": plan.producer_semantic_parameter_digest,
            "runtime_lock_digest": plan.runtime_lock_digest,
            "execution_status": "EXECUTED",
            "exit_code": completed.returncode,
            "output_schema": str(output["schema"]),
            "output_status": str(output["status"]),
            "output_size_bytes": len(raw),
            "output_sha256": output_sha,
            "data02_result_binding_digest": str(bound["binding_digest"]),
            "producer_stdout_digest": stdout_digest,
            "producer_stderr_digest": stderr_digest,
            "reconstruction_class": "EVIDENCE_REPLAY",
            "reconstruction_descriptor_digest": reconstruction_digest,
        }
        result_identity = compute_result_identity(candidate)
        values = {
            **candidate,
            "producer_execution_result_id": result_identity,
            "result_identity": result_identity,
            "request_id": plan.request_id,
            "revision_id": plan.revision_id,
            "audit_id": plan.audit_id,
            "scope_id": plan.scope_id,
            "data02_admission_digest": plan.data02_admission_digest,
            "data02_dataset_file_set_digest": plan.data02_dataset_file_set_digest,
            "scientific_authority": False,
            "operational_authority": False,
            "trading_authority": False,
            "capital_authority": False,
        }
        return _attest_result(**values)


# ---------------------------------------------------------------------------
# P1-21 — real qualified producer capability (pre-execution only)
# ---------------------------------------------------------------------------

REAL_CAPABILITY_CONTRACT = "P1_12C_REAL_QUALIFIED_PRODUCER_CAPABILITY_V1"
REAL_DATA_BINDING_SCHEMA = "P1_12C_REAL_DATA_OWNER_EVIDENCE_BINDING_V1"
REAL_RUNTIME_LOCK_SCHEMA = "P1_12C_REAL_PRODUCER_RUNTIME_LOCK_V1"
AP1_INVOCATION_PROFILE_ID = "P1_12C_AP1_CLAIM_SCOPED_V1"
AP1_PRODUCER_ID = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
AP1_PRODUCER_BLOB = "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"
AP1_OUTPUT_SCHEMA = "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
AP1_OUTPUT_STATUS = "AP1_COMPLETE"
DATA02_REAL_RECEIPT_BLOB = "ccfccda676abfe7e02082a331557ffed14e1f32b"
DATA02_REAL_EVIDENCE_DIGEST = "d11f6c39fcf9f31336ecc34027abc99c79a9f881d8203a78d6c7ac47c0b3af3b"
DATA02_REAL_MANIFEST_SHA256 = "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
DATA02_REAL_FILE_SET_DIGEST = "1ff14ab4fea11c2480088a322f5bec23ea183de14cbc65ee6c684c7ea185062a"
DATA02_REAL_SCHEMA_IDENTITY = "5c5f5302891567b62024c718d4e7700b766d1ace8f3e40f7a0a29cee6b93bf88"
RVO06_RUNTIME_EVIDENCE_BLOB = "e4e275e8590e3bead9123969c068b036c6c4e1d8"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedDataOwnerEvidenceBinding:
    p1_data_evidence_binding_id: str
    p1_data_evidence_binding_digest: str
    native_data_status: str
    p1_binding_status: str
    data_owner_receipt_blob: str
    data_owner_evidence_digest: str
    dataset_identity: str
    source_identity: str
    ap0_manifest_sha256: str
    dataset_file_set_digest: str
    schema_identity: str
    transformer_blob: str
    usage_envelope_id: str
    temporal_status: str
    file_count: int
    result_exposed: bool
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RealProducerInvocationProfile:
    invocation_profile_id: str
    invocation_profile_digest: str
    producer_id: str
    producer_code_blob: str
    producer_protocol: str
    sandbox_runner_blob: str
    child_argv_schema_json: str
    shell: bool
    output_transport_identity_authority: bool
    result_exposed: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RealProducerRuntimeLock:
    runtime_lock_id: str
    runtime_lock_digest: str
    schema: str
    platform: str
    architecture: str
    python_version: str
    python_binary_sha256: str
    numpy_version: str
    numpy_metadata_sha256: str
    numpy_record_sha256: str
    pyarrow_version: str
    pyarrow_metadata_sha256: str
    pyarrow_record_sha256: str
    tzdata_version: str
    tzdata_metadata_sha256: str
    tzdata_record_sha256: str
    timezone_name: str
    material_environment_json: str
    timeout_seconds: int
    invocation_profile_digest: str
    runtime_evidence_source_ref: str
    result_exposed: bool
    execution_authority: bool


@dataclass(frozen=True, slots=True, weakref_slot=True)
class QualifiedRealProducerExecutionPlan:
    real_producer_execution_plan_id: str
    real_producer_execution_plan_digest: str
    experiment_execution_input_id: str
    execution_binding_id: str
    experiment_spec_id: str
    request_id: str
    revision_id: str
    audit_id: str
    scope_id: str
    p1_data_evidence_binding_id: str
    p1_data_evidence_binding_digest: str
    native_data_status: str
    producer_id: str
    producer_code_blob: str
    producer_path_transport: str
    invocation_profile_id: str
    invocation_profile_digest: str
    runtime_lock_id: str
    runtime_lock_digest: str
    ap0_root_transport: str
    ap0_manifest_transport: str
    output_transport: str
    ap0_manifest_sha256: str
    dataset_file_set_digest: str
    dataset_identity: str
    semantic_parameters_json: str
    semantic_parameter_digest: str
    expected_output_schema: str
    expected_output_status: str
    expected_output_contract: str
    maximum_output_bytes: int
    result_exposed: bool
    execution_authority: bool
    scientific_authority: bool
    operational_authority: bool
    trading_authority: bool
    capital_authority: bool


def _build_p121_attestation_api(cls, fingerprint):
    registry: dict[int, tuple[weakref.ReferenceType, str]] = {}

    def attest(**values):
        produced = cls(**values)
        object_id = id(produced)

        def cleanup(reference, *, expected_object_id: int = object_id) -> None:
            current = registry.get(expected_object_id)
            if current is not None and current[0] is reference:
                registry.pop(expected_object_id, None)

        reference = weakref.ref(produced, cleanup)
        registry[object_id] = (reference, fingerprint(produced))
        return produced

    def verify(value: object) -> bool:
        if type(value) is not cls:
            return False
        entry = registry.get(id(value))
        if entry is None:
            return False
        reference, expected = entry
        if reference() is not value:
            registry.pop(id(value), None)
            return False
        if fingerprint(value) != expected:
            registry.pop(id(value), None)
            return False
        return True

    return attest, verify


def _p121_fingerprint(tag: str, value: object) -> str:
    return _digest({"contract": REAL_CAPABILITY_CONTRACT, "tag": tag, "value": asdict(value)})


_attest_real_data_binding, is_factory_attested_real_data_owner_evidence_binding = _build_p121_attestation_api(
    QualifiedDataOwnerEvidenceBinding, lambda v: _p121_fingerprint("DATA_BINDING", v)
)
_attest_real_profile, is_factory_attested_real_producer_invocation_profile = _build_p121_attestation_api(
    RealProducerInvocationProfile, lambda v: _p121_fingerprint("INVOCATION_PROFILE", v)
)
_attest_real_runtime, is_factory_attested_real_producer_runtime_lock = _build_p121_attestation_api(
    RealProducerRuntimeLock, lambda v: _p121_fingerprint("RUNTIME_LOCK", v)
)
_attest_real_plan, is_factory_attested_qualified_real_producer_execution_plan = _build_p121_attestation_api(
    QualifiedRealProducerExecutionPlan, lambda v: _p121_fingerprint("REAL_PLAN", v)
)
del _build_p121_attestation_api


_P121_ATTACK_REJECTIONS = {
    "P121-B01": ("REJECTED", "REJECT_DATA_OWNER_STATUS_REWRITE"),
    "P121-B02": ("BLOCKED", "BLOCKED_DATA_OWNER_EVIDENCE_DIGEST_REQUIRED"),
    "P121-B03": ("BLOCKED", "BLOCKED_STALE_DATA02_RECEIPT"),
    "P121-B04": ("BLOCKED", "BLOCKED_DATASET_IDENTITY_MISMATCH"),
    "P121-B05": ("BLOCKED", "BLOCKED_AP0_MANIFEST_IDENTITY_MISMATCH"),
    "P121-B06": ("BLOCKED", "BLOCKED_DATASET_FILE_SET_IDENTITY_MISMATCH"),
    "P121-B07": ("BLOCKED", "BLOCKED_DATASET_SCHEMA_IDENTITY_MISMATCH"),
    "P121-B08": ("BLOCKED", "BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED"),
    "P121-B09": ("BLOCKED", "BLOCKED_INVOCATION_PROFILE_MISMATCH"),
    "P121-B10": ("REJECTED", "REJECT_SYNTHETIC_ARGV_FOR_AP1"),
    "P121-B11": ("BLOCKED", "BLOCKED_AP1_MANIFEST_ARGUMENT_REQUIRED"),
    "P121-B12": ("REJECTED", "REJECT_SHELL_INVOCATION"),
    "P121-B13": ("REJECTED", "REJECT_OUTPUT_PATH_AS_RESULT_IDENTITY"),
    "P121-B14": ("BLOCKED", "BLOCKED_PYTHON_BINARY_IDENTITY_REQUIRED"),
    "P121-B15": ("BLOCKED", "BLOCKED_NUMPY_IDENTITY_REQUIRED"),
    "P121-B16": ("BLOCKED", "BLOCKED_PYARROW_IDENTITY_REQUIRED"),
    "P121-B17": ("BLOCKED", "BLOCKED_TIMEZONE_DATABASE_IDENTITY_REQUIRED"),
    "P121-B18": ("REJECTED", "REJECT_VERSION_ONLY_DEPENDENCY_IDENTITY"),
    "P121-B19": ("REJECTED", "REJECT_SYNTHETIC_RUNTIME_LOCK_FOR_REAL_PRODUCER"),
    "P121-B20": ("BLOCKED", "BLOCKED_EXPLICIT_TIMEOUT_REQUIRED"),
    "P121-B21": ("BLOCKED", "BLOCKED_FINITE_TIMEOUT_REQUIRED"),
    "P121-B22": ("BLOCKED", "BLOCKED_POST_RESULT_RUNTIME_SELECTION"),
    "P121-B23": ("BLOCKED", "BLOCKED_POST_RESULT_DATA_EVIDENCE_SELECTION"),
    "P121-B24": ("BLOCKED", "BLOCKED_POST_RESULT_INVOCATION_PROFILE_SELECTION"),
    "P121-B25": ("REJECTED", "REJECT_PLAN_EXECUTION_AUTHORITY"),
    "P121-B26": ("REJECTED", "REJECT_PLAN_SCIENTIFIC_AUTHORITY"),
    "P121-B27": ("REJECTED", "REJECT_PLAN_TRADING_CAPITAL_AUTHORITY"),
    "P121-B28": ("BLOCKED", "BLOCKED_P1_12D_COMPATIBILITY_REGRESSION"),
    "P121-B29": ("BLOCKED", "BLOCKED_LEGACY_SYNTHETIC_P1_12C_REGRESSION"),
}


def validate_real_producer_capability_attack(case_id: str) -> dict[str, Any]:
    if case_id not in _P121_ATTACK_REJECTIONS:
        return _decision("READY", "NO_P1_21_BOUNDARY_ATTACK")
    status, reason = _P121_ATTACK_REJECTIONS[case_id]
    return _decision(status, reason)


def bind_real_data_owner_evidence(
    receipt_path: str | Path,
    *,
    result_exposed: bool = False,
) -> QualifiedDataOwnerEvidenceBinding:
    if result_exposed:
        raise P112CBlocked("BLOCKED_POST_RESULT_DATA_EVIDENCE_SELECTION")
    path = Path(receipt_path)
    if not path.is_file():
        raise P112CBlocked("BLOCKED_STALE_DATA02_RECEIPT")
    if git_blob_sha1(path) != DATA02_REAL_RECEIPT_BLOB:
        raise P112CBlocked("BLOCKED_STALE_DATA02_RECEIPT")
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P112CBlocked("BLOCKED_STALE_DATA02_RECEIPT") from exc

    if receipt.get("status") != "PASS_REAL_DATA_ADMISSION":
        raise P112CBlocked("BLOCKED_DATA_OWNER_NATIVE_STATUS")
    corpus = receipt.get("corpus")
    replay = receipt.get("replay")
    if not isinstance(corpus, Mapping) or not isinstance(replay, Mapping):
        raise P112CBlocked("BLOCKED_DATA_OWNER_EVIDENCE_DIGEST_REQUIRED")
    evidence_digest = replay.get("first_evidence_digest")
    if (
        not isinstance(evidence_digest, str)
        or evidence_digest != DATA02_REAL_EVIDENCE_DIGEST
        or replay.get("second_evidence_digest") != evidence_digest
        or replay.get("exact_equal") is not True
    ):
        raise P112CBlocked("BLOCKED_DATA_OWNER_EVIDENCE_DIGEST_REQUIRED")
    if corpus.get("dataset_identity") != data02.DATASET_IDENTITY:
        raise P112CBlocked("BLOCKED_DATASET_IDENTITY_MISMATCH")
    if corpus.get("manifest_sha256") != DATA02_REAL_MANIFEST_SHA256:
        raise P112CBlocked("BLOCKED_AP0_MANIFEST_IDENTITY_MISMATCH")
    if corpus.get("file_set_digest") != DATA02_REAL_FILE_SET_DIGEST:
        raise P112CBlocked("BLOCKED_DATASET_FILE_SET_IDENTITY_MISMATCH")
    if corpus.get("schema_identity") != DATA02_REAL_SCHEMA_IDENTITY:
        raise P112CBlocked("BLOCKED_DATASET_SCHEMA_IDENTITY_MISMATCH")
    if corpus.get("files_verified") != 61:
        raise P112CBlocked("BLOCKED_DATASET_FILE_SET_IDENTITY_MISMATCH")
    if corpus.get("temporal_status") != "NOT_APPLICABLE_WITH_EXPLICIT_BASIS":
        raise P112CBlocked("BLOCKED_TEMPORAL_SCOPE_ESCALATION")

    exclusions = receipt.get("exclusions")
    if not isinstance(exclusions, Mapping):
        raise P112CBlocked("BLOCKED_DATA_OWNER_NATIVE_STATUS")
    forbidden_true = (
        "market_behavior_result_computed",
        "strategy_statistic_computed",
        "pnl_computed",
        "performance_observed",
        "oos_consumed",
        "data_modified",
        "data_repaired",
        "data_sorted_or_deduplicated",
        "temporal_validity_claimed",
    )
    if any(exclusions.get(name) is not False for name in forbidden_true):
        raise P112CBlocked("BLOCKED_DATA_OWNER_NATIVE_STATUS")

    authority = receipt.get("authority")
    if not isinstance(authority, Mapping) or any(
        authority.get(name) is not False
        for name in ("data_scientific_authority", "temporal_authority", "operational_authority", "trading_authority", "capital_authority")
    ) or authority.get("rvo_authority") != "NONE":
        raise P112CBlocked("BLOCKED_DATA_OWNER_NATIVE_STATUS")

    values = {
        "native_data_status": "PASS_REAL_DATA_ADMISSION",
        "p1_binding_status": "P1_DATA_EVIDENCE_ACCEPTED_FOR_PLAN_BINDING",
        "data_owner_receipt_blob": DATA02_REAL_RECEIPT_BLOB,
        "data_owner_evidence_digest": evidence_digest,
        "dataset_identity": str(corpus["dataset_identity"]),
        "source_identity": str(corpus["source_identity"]),
        "ap0_manifest_sha256": str(corpus["manifest_sha256"]),
        "dataset_file_set_digest": str(corpus["file_set_digest"]),
        "schema_identity": str(corpus["schema_identity"]),
        "transformer_blob": str(corpus["transformer_blob"]),
        "usage_envelope_id": str(corpus["usage_envelope_id"]),
        "temporal_status": str(corpus["temporal_status"]),
        "file_count": int(corpus["files_verified"]),
        "result_exposed": False,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    digest = _digest({"schema": REAL_DATA_BINDING_SCHEMA, **values})
    return _attest_real_data_binding(
        p1_data_evidence_binding_id="P1DE-" + digest[:32],
        p1_data_evidence_binding_digest=digest,
        **values,
    )


def qualify_ap1_invocation_profile(
    producer_path: str | Path,
    *,
    result_exposed: bool = False,
) -> RealProducerInvocationProfile:
    if result_exposed:
        raise P112CBlocked("BLOCKED_POST_RESULT_INVOCATION_PROFILE_SELECTION")
    producer = Path(producer_path)
    if not producer.is_file() or git_blob_sha1(producer) != AP1_PRODUCER_BLOB:
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
    runner = _runner_path()
    if not runner.is_file():
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    runner_blob = git_blob_sha1(runner)
    schema = {
        "child_argv": [
            "{producer_path}",
            "--ap0-root", "{ap0_root_transport}",
            "--ap0-manifest", "{ap0_manifest_transport}",
            "--output", "{output_transport}",
        ],
        "structured_arguments": True,
        "shell": False,
        "producer_path_identity_authority": False,
        "output_path_identity_authority": False,
    }
    values = {
        "producer_id": AP1_PRODUCER_ID,
        "producer_code_blob": AP1_PRODUCER_BLOB,
        "producer_protocol": AP1_INVOCATION_PROFILE_ID,
        "sandbox_runner_blob": runner_blob,
        "child_argv_schema_json": json.dumps(schema, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
        "shell": False,
        "output_transport_identity_authority": False,
        "result_exposed": False,
    }
    digest = _digest({"contract": REAL_CAPABILITY_CONTRACT, "profile": values})
    return _attest_real_profile(
        invocation_profile_id=AP1_INVOCATION_PROFILE_ID,
        invocation_profile_digest=digest,
        **values,
    )


def qualify_real_producer_runtime_lock(
    runtime_evidence: Mapping[str, Any],
    invocation_profile: RealProducerInvocationProfile,
    *,
    runtime_evidence_source_ref: str,
    timeout_seconds: int,
    material_environment: Mapping[str, str],
    result_exposed: bool = False,
) -> RealProducerRuntimeLock:
    if result_exposed:
        raise P112CBlocked("BLOCKED_POST_RESULT_RUNTIME_SELECTION")
    if not is_factory_attested_real_producer_invocation_profile(invocation_profile):
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if invocation_profile.invocation_profile_id != AP1_INVOCATION_PROFILE_ID:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if runtime_evidence.get("status") != "OBSERVED_RUNTIME_EVIDENCE_NOT_P1_12C_RUNTIME_LOCK":
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    if runtime_evidence_source_ref != RVO06_RUNTIME_EVIDENCE_BLOB:
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    if type(timeout_seconds) is not int:
        raise P112CBlocked("BLOCKED_EXPLICIT_TIMEOUT_REQUIRED")
    if timeout_seconds <= 0 or timeout_seconds > 86400:
        raise P112CBlocked("BLOCKED_FINITE_TIMEOUT_REQUIRED")
    if not isinstance(material_environment, Mapping):
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")

    device = runtime_evidence.get("device")
    python_evidence = runtime_evidence.get("python")
    deps = runtime_evidence.get("dependencies")
    if not isinstance(device, Mapping) or not isinstance(python_evidence, Mapping) or not isinstance(deps, Mapping):
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    python_hash = python_evidence.get("real_binary_sha256")
    if not isinstance(python_hash, str) or _SHA256_RE.fullmatch(python_hash) is None:
        raise P112CBlocked("BLOCKED_PYTHON_BINARY_IDENTITY_REQUIRED")

    def dependency(name: str, reason: str) -> tuple[str, str, str]:
        value = deps.get(name)
        if not isinstance(value, Mapping):
            raise P112CBlocked(reason)
        version = value.get("version")
        metadata = value.get("metadata_sha256")
        record = value.get("record_sha256")
        if not isinstance(version, str) or not version:
            raise P112CBlocked(reason)
        if not isinstance(metadata, str) or _SHA256_RE.fullmatch(metadata) is None:
            raise P112CBlocked("REJECT_VERSION_ONLY_DEPENDENCY_IDENTITY")
        if not isinstance(record, str) or _SHA256_RE.fullmatch(record) is None:
            raise P112CBlocked("REJECT_VERSION_ONLY_DEPENDENCY_IDENTITY")
        return version, metadata, record

    numpy_version, numpy_metadata, numpy_record = dependency("numpy", "BLOCKED_NUMPY_IDENTITY_REQUIRED")
    pyarrow_version, pyarrow_metadata, pyarrow_record = dependency("pyarrow", "BLOCKED_PYARROW_IDENTITY_REQUIRED")
    tzdata_version, tzdata_metadata, tzdata_record = dependency("tzdata", "BLOCKED_TIMEZONE_DATABASE_IDENTITY_REQUIRED")

    environment_json = json.dumps(
        {str(k): str(v) for k, v in sorted(material_environment.items())},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    values = {
        "schema": REAL_RUNTIME_LOCK_SCHEMA,
        "platform": str(device.get("platform", "")),
        "architecture": str(device.get("arch", "")),
        "python_version": str(device.get("python_version", "")),
        "python_binary_sha256": python_hash,
        "numpy_version": numpy_version,
        "numpy_metadata_sha256": numpy_metadata,
        "numpy_record_sha256": numpy_record,
        "pyarrow_version": pyarrow_version,
        "pyarrow_metadata_sha256": pyarrow_metadata,
        "pyarrow_record_sha256": pyarrow_record,
        "tzdata_version": tzdata_version,
        "tzdata_metadata_sha256": tzdata_metadata,
        "tzdata_record_sha256": tzdata_record,
        "timezone_name": "America/New_York",
        "material_environment_json": environment_json,
        "timeout_seconds": timeout_seconds,
        "invocation_profile_digest": invocation_profile.invocation_profile_digest,
        "runtime_evidence_source_ref": runtime_evidence_source_ref,
        "result_exposed": False,
        "execution_authority": False,
    }
    if not values["platform"] or not values["architecture"] or not values["python_version"]:
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    digest = _digest({"contract": REAL_CAPABILITY_CONTRACT, "runtime": values})
    return _attest_real_runtime(
        runtime_lock_id="RPRL-" + digest[:32],
        runtime_lock_digest=digest,
        **values,
    )


def qualify_real_producer_execution_plan(
    qualified_input: QualifiedExperimentExecutionInput,
    data_binding: QualifiedDataOwnerEvidenceBinding,
    invocation_profile: RealProducerInvocationProfile,
    runtime_lock: RealProducerRuntimeLock,
    *,
    producer_path: str | Path,
    ap0_root_transport: str,
    ap0_manifest_transport: str,
    output_transport: str,
    expected_output_schema: str = AP1_OUTPUT_SCHEMA,
    expected_output_status: str = AP1_OUTPUT_STATUS,
    expected_output_contract: str = "ATDS_AP1_CANONICAL_JSON_OUTPUT_V1",
    maximum_output_bytes: int,
    result_exposed: bool = False,
) -> QualifiedRealProducerExecutionPlan:
    if result_exposed:
        raise P112CBlocked("BLOCKED_POST_RESULT_PRODUCER_SELECTION")
    if type(qualified_input) is not QualifiedExperimentExecutionInput or not is_factory_attested_qualified_experiment_execution_input(qualified_input):
        raise P112CBlocked("BLOCKED_EXPERIMENT_SPEC_BINDING_MISMATCH")
    if not is_factory_attested_real_data_owner_evidence_binding(data_binding):
        raise P112CBlocked("BLOCKED_DATA02_ADMISSION_REQUIRED")
    if not is_factory_attested_real_producer_invocation_profile(invocation_profile):
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if not is_factory_attested_real_producer_runtime_lock(runtime_lock):
        raise P112CBlocked("BLOCKED_RUNTIME_LOCK_MISSING_OR_DRIFTED")
    if runtime_lock.invocation_profile_digest != invocation_profile.invocation_profile_digest:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if runtime_lock.execution_authority is not False:
        raise P112CBlocked("REJECT_PLAN_EXECUTION_AUTHORITY")
    if data_binding.native_data_status != "PASS_REAL_DATA_ADMISSION":
        raise P112CBlocked("REJECT_DATA_OWNER_STATUS_REWRITE")
    if data_binding.p1_binding_status != "P1_DATA_EVIDENCE_ACCEPTED_FOR_PLAN_BINDING":
        raise P112CBlocked("BLOCKED_DATA02_ADMISSION_REQUIRED")

    producer = Path(producer_path)
    if not producer.is_file() or git_blob_sha1(producer) != AP1_PRODUCER_BLOB:
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
    if invocation_profile.producer_code_blob != AP1_PRODUCER_BLOB or invocation_profile.producer_id != AP1_PRODUCER_ID:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if expected_output_schema != AP1_OUTPUT_SCHEMA or expected_output_status != AP1_OUTPUT_STATUS:
        raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SCHEMA_MISMATCH")
    if type(maximum_output_bytes) is not int or maximum_output_bytes <= 0:
        raise P112CBlocked("BLOCKED_PRODUCER_OUTPUT_SIZE")
    for transport in (ap0_root_transport, ap0_manifest_transport, output_transport):
        if not isinstance(transport, str) or not transport:
            raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")

    semantic_parameters = {
        "claim_scope": "CC02_DESCRIPTIVE_MARKET_BEHAVIOR",
        "semantic_limit": "RETROSPECTIVE_DESCRIPTIVE_ONLY",
        "producer_configuration": "CODE_FROZEN_BY_EXACT_GIT_BLOB",
        "intraday_timezone": "America/New_York",
        "percentile_method": "linear",
        "oos_consumption": False,
    }
    semantic_json = json.dumps(semantic_parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    semantic_digest = hashlib.sha256(semantic_json.encode("utf-8")).hexdigest()

    values = {
        "experiment_execution_input_id": qualified_input.experiment_execution_input_id,
        "execution_binding_id": qualified_input.execution_binding_id,
        "experiment_spec_id": qualified_input.experiment_spec_id,
        "request_id": qualified_input.request_id,
        "revision_id": qualified_input.revision_id,
        "audit_id": qualified_input.audit_id,
        "scope_id": qualified_input.scope_id,
        "p1_data_evidence_binding_id": data_binding.p1_data_evidence_binding_id,
        "p1_data_evidence_binding_digest": data_binding.p1_data_evidence_binding_digest,
        "native_data_status": data_binding.native_data_status,
        "producer_id": AP1_PRODUCER_ID,
        "producer_code_blob": AP1_PRODUCER_BLOB,
        "producer_path_transport": str(producer.resolve()),
        "invocation_profile_id": invocation_profile.invocation_profile_id,
        "invocation_profile_digest": invocation_profile.invocation_profile_digest,
        "runtime_lock_id": runtime_lock.runtime_lock_id,
        "runtime_lock_digest": runtime_lock.runtime_lock_digest,
        "ap0_root_transport": str(ap0_root_transport),
        "ap0_manifest_transport": str(ap0_manifest_transport),
        "output_transport": str(output_transport),
        "ap0_manifest_sha256": data_binding.ap0_manifest_sha256,
        "dataset_file_set_digest": data_binding.dataset_file_set_digest,
        "dataset_identity": data_binding.dataset_identity,
        "semantic_parameters_json": semantic_json,
        "semantic_parameter_digest": semantic_digest,
        "expected_output_schema": expected_output_schema,
        "expected_output_status": expected_output_status,
        "expected_output_contract": str(expected_output_contract),
        "maximum_output_bytes": maximum_output_bytes,
        "result_exposed": False,
        "execution_authority": False,
        "scientific_authority": False,
        "operational_authority": False,
        "trading_authority": False,
        "capital_authority": False,
    }
    identity_values = {k: v for k, v in values.items() if k not in {
        "producer_path_transport", "ap0_root_transport", "ap0_manifest_transport", "output_transport"
    }}
    digest = _digest({"contract": REAL_CAPABILITY_CONTRACT, "plan": identity_values})
    return _attest_real_plan(
        real_producer_execution_plan_id="QRPP-" + digest[:32],
        real_producer_execution_plan_digest=digest,
        **values,
    )


def build_ap1_runner_command(
    plan: QualifiedRealProducerExecutionPlan,
    invocation_profile: RealProducerInvocationProfile,
    *,
    python_executable: str,
    runner_path: str | Path,
    producer_path: str | Path,
) -> tuple[str, ...]:
    if not is_factory_attested_qualified_real_producer_execution_plan(plan):
        raise P112CBlocked("BLOCKED_UNATTESTED_PRODUCER_PLAN")
    if not is_factory_attested_real_producer_invocation_profile(invocation_profile):
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if plan.invocation_profile_digest != invocation_profile.invocation_profile_digest:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if invocation_profile.shell is not False:
        raise P112CBlocked("REJECT_SHELL_INVOCATION")
    runner = Path(runner_path)
    producer = Path(producer_path)
    if not runner.is_file() or git_blob_sha1(runner) != invocation_profile.sandbox_runner_blob:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if not producer.is_file() or git_blob_sha1(producer) != plan.producer_code_blob:
        raise P112CBlocked("BLOCKED_PRODUCER_CODE_IDENTITY_REQUIRED")
    if not python_executable:
        raise P112CBlocked("BLOCKED_PYTHON_BINARY_IDENTITY_REQUIRED")
    return (
        str(python_executable),
        "-I",
        str(runner),
        "--producer",
        str(producer),
        "--invocation-profile",
        AP1_INVOCATION_PROFILE_ID,
        "--ap0-root",
        plan.ap0_root_transport,
        "--ap0-manifest",
        plan.ap0_manifest_transport,
        "--output",
        plan.output_transport,
    )


def build_ap1_child_argv(
    invocation_profile: RealProducerInvocationProfile,
    *,
    producer_path: str,
    ap0_root_transport: str,
    ap0_manifest_transport: str,
    output_transport: str,
) -> tuple[str, ...]:
    if not is_factory_attested_real_producer_invocation_profile(invocation_profile):
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if invocation_profile.invocation_profile_id != AP1_INVOCATION_PROFILE_ID:
        raise P112CBlocked("BLOCKED_INVOCATION_PROFILE_MISMATCH")
    if not ap0_manifest_transport:
        raise P112CBlocked("BLOCKED_AP1_MANIFEST_ARGUMENT_REQUIRED")
    return (
        str(producer_path),
        "--ap0-root", str(ap0_root_transport),
        "--ap0-manifest", str(ap0_manifest_transport),
        "--output", str(output_transport),
    )
