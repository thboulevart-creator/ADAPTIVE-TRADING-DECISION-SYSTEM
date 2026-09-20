from __future__ import annotations

import hashlib
import json
from dataclasses import fields, is_dataclass
from typing import Any, Mapping, Sequence

from src import native_bi5_freeze_persistence as freeze
from src import native_bi5_semantic_universe_comparator as oracle


HANDOFF_ID = "Q_RM_12_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_POSTSEAL_HANDOFF"
HANDOFF_VERSION = (
    "Q_RM_12_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_POSTSEAL_HANDOFF_V0_1_CANDIDATE"
)
RESULT_SCHEMA = "NATIVE_BI5_QRM12_HANDOFF_RESULT_V0_1_CANDIDATE"
IMPLEMENTATION_RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_2_CANDIDATE"
RECEIPT_SCHEMA = "NATIVE_BI5_QRM12_EXECUTION_RECEIPT_V0_1_CANDIDATE"

_STAGES = ("D", "R", "M", "B", "A", "Q", "F", "O")
_F_STAGES = ("D", "R", "M", "B", "A", "Q", "F")
_RESULT_FIELDS = (
    "schema",
    "implementation_id",
    "implementation_version",
    "implementation_manifest_digest",
    "input_determinant_bindings",
    "materialized_acquisition_id",
    "execution_status",
    "semantic_status",
    "freeze_status",
    "bound_f_artifact",
    "terminal_evidence",
    "isolation_evidence",
    "result_seal",
)
_PIN_FIELDS = {
    "implementation_id",
    "implementation_version",
    "implementation_manifest_digest",
    "implementation_source_digest",
}
_RECEIPT_FIELDS = {
    "schema",
    "run_id",
    "implementation_id",
    "implementation_version",
    "implementation_manifest_digest",
    "implementation_source_digest",
    "workspace_isolation_identity",
    "result_seal",
}
_BINDING_FIELDS = {
    "stage",
    "normative_id",
    "normative_version",
    "immutable_reference",
    "integrity_digest",
}
_ALLOWED_PRESEAL = frozenset(
    ("common_immutable_input_package", "own_implementation_runtime", "python_stdlib")
)
_ALLOWED_ENV = frozenset(("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL"))


class _Blocked(ValueError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _is_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _handoff_result(
    handoff_result: str,
    oracle_result: str,
    comparison_scope: str,
    reason: str,
) -> dict[str, str]:
    return {
        "schema": RESULT_SCHEMA,
        "handoff_id": HANDOFF_ID,
        "handoff_version": HANDOFF_VERSION,
        "handoff_result": handoff_result,
        "oracle_result": oracle_result,
        "comparison_scope": comparison_scope,
        "reason": reason,
    }


def _blocked(reason: str, scope: str = "POSTSEAL_VALIDATION") -> dict[str, str]:
    return _handoff_result("BLOCKED", "NOT_INVOKED", scope, reason)


def _result_payload(result: Any) -> dict[str, Any]:
    if not is_dataclass(result):
        raise _Blocked("RESULT_NOT_DATACLASS")
    names = tuple(field.name for field in fields(result))
    if names != _RESULT_FIELDS:
        raise _Blocked("RESULT_SCHEMA_FIELDS_MISMATCH")
    return {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }


def _result_seal(result: Any) -> str:
    try:
        return _sha256(_canonical_bytes(_result_payload(result)))
    except (TypeError, ValueError) as exc:
        raise _Blocked("RESULT_NOT_STRICT_CANONICAL_JSON") from exc


def _binding_tuple(value: Any) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _Blocked("RESULT_DETERMINANT_BINDINGS_MISSING")
    by_stage: dict[str, dict[str, Any]] = {}
    for raw in value:
        if not isinstance(raw, Mapping) or set(raw) != _BINDING_FIELDS:
            raise _Blocked("RESULT_DETERMINANT_BINDING_INVALID")
        item = dict(raw)
        stage = item.get("stage")
        if stage not in _STAGES or stage in by_stage:
            raise _Blocked("RESULT_DETERMINANT_STAGE_INVALID")
        if not all(
            _nonempty(item.get(key))
            for key in ("normative_id", "normative_version", "immutable_reference")
        ):
            raise _Blocked("RESULT_DETERMINANT_IDENTITY_INVALID")
        if not _is_digest(item.get("integrity_digest")):
            raise _Blocked("RESULT_DETERMINANT_DIGEST_INVALID")
        try:
            _canonical_bytes(item)
        except (TypeError, ValueError) as exc:
            raise _Blocked("RESULT_DETERMINANT_NOT_STRICT_JSON") from exc
        by_stage[stage] = item
    if set(by_stage) != set(_STAGES):
        raise _Blocked("RESULT_DETERMINANT_SET_NOT_EXACT")
    return tuple(by_stage[stage] for stage in _STAGES)


def _isolation_closed(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    expected_keys = {
        "workspace_isolation_identity",
        "preseal_input_allowlist",
        "network_policy",
        "ipc_policy",
        "environment_variable_allowlist",
        "cache_policy",
        "other_path_output_readable",
        "runtime_read_set",
    }
    if set(value) != expected_keys:
        return False
    workspace = value.get("workspace_isolation_identity")
    return (
        _nonempty(workspace)
        and frozenset(value.get("preseal_input_allowlist", ())) == _ALLOWED_PRESEAL
        and value.get("network_policy") == "DENY"
        and value.get("ipc_policy") == "DENY"
        and frozenset(value.get("environment_variable_allowlist", ())) == _ALLOWED_ENV
        and value.get("cache_policy") == "PRIVATE_ONLY"
        and value.get("other_path_output_readable") is False
        and frozenset(value.get("runtime_read_set", ())) == _ALLOWED_PRESEAL
    )


def _validate_pin(value: Any) -> Mapping[str, str]:
    if not isinstance(value, Mapping) or set(value) != _PIN_FIELDS:
        raise _Blocked("EXTERNAL_PIN_SCHEMA_INVALID")
    for key in _PIN_FIELDS:
        if not _nonempty(value.get(key)):
            raise _Blocked("EXTERNAL_PIN_FIELD_INVALID")
    if not _is_digest(value["implementation_manifest_digest"]):
        raise _Blocked("EXTERNAL_MANIFEST_PIN_INVALID")
    if not _is_digest(value["implementation_source_digest"]):
        raise _Blocked("EXTERNAL_SOURCE_PIN_INVALID")
    return value


def _validate_receipt(
    receipt: Any,
    pin: Mapping[str, str],
    result: Any,
) -> None:
    if not isinstance(receipt, Mapping) or set(receipt) != _RECEIPT_FIELDS:
        raise _Blocked("EXECUTION_RECEIPT_SCHEMA_INVALID")
    if receipt.get("schema") != RECEIPT_SCHEMA:
        raise _Blocked("EXECUTION_RECEIPT_SCHEMA_INVALID")
    if not _nonempty(receipt.get("run_id")):
        raise _Blocked("EXECUTION_RECEIPT_RUN_ID_INVALID")
    if not _nonempty(receipt.get("workspace_isolation_identity")):
        raise _Blocked("EXECUTION_RECEIPT_WORKSPACE_INVALID")
    if not _is_digest(receipt.get("result_seal")):
        raise _Blocked("EXECUTION_RECEIPT_RESULT_SEAL_INVALID")

    for key in _PIN_FIELDS:
        if receipt.get(key) != pin[key]:
            raise _Blocked("EXECUTION_RECEIPT_PRODUCER_PIN_MISMATCH")

    if receipt["result_seal"] != result.result_seal:
        raise _Blocked("EXECUTION_RECEIPT_RESULT_SEAL_MISMATCH")
    if receipt["workspace_isolation_identity"] != result.isolation_evidence.get(
        "workspace_isolation_identity"
    ):
        raise _Blocked("EXECUTION_RECEIPT_WORKSPACE_MISMATCH")


def _validate_result_against_pin(
    result: Any,
    pin: Mapping[str, str],
) -> tuple[tuple[dict[str, Any], ...], Mapping[str, Any]]:
    payload = _result_payload(result)
    if getattr(result, "schema", None) != IMPLEMENTATION_RESULT_SCHEMA:
        raise _Blocked("IMPLEMENTATION_RESULT_SCHEMA_INVALID")
    if getattr(result, "implementation_id", None) != pin["implementation_id"]:
        raise _Blocked("RESULT_IMPLEMENTATION_ID_PIN_MISMATCH")
    if getattr(result, "implementation_version", None) != pin["implementation_version"]:
        raise _Blocked("RESULT_IMPLEMENTATION_VERSION_PIN_MISMATCH")
    if (
        getattr(result, "implementation_manifest_digest", None)
        != pin["implementation_manifest_digest"]
    ):
        raise _Blocked("RESULT_MANIFEST_PIN_MISMATCH")

    actual_seal = getattr(result, "result_seal", None)
    if not _is_digest(actual_seal) or actual_seal != _sha256(_canonical_bytes(payload)):
        raise _Blocked("RESULT_SEAL_INVALID")

    if (
        getattr(result, "execution_status", None) != "COMPLETED"
        or getattr(result, "semantic_status", None) != "QUALIFIED"
        or getattr(result, "freeze_status", None) != "FROZEN"
        or getattr(result, "terminal_evidence", None) is not None
        or getattr(result, "bound_f_artifact", None) is None
    ):
        raise _Blocked("RESULT_NOT_COMPLETED_QUALIFIED_FROZEN")

    if not _isolation_closed(getattr(result, "isolation_evidence", None)):
        raise _Blocked("RESULT_ISOLATION_NOT_CLOSED")

    bindings = _binding_tuple(result.input_determinant_bindings)
    artifact = result.bound_f_artifact
    try:
        freeze.validate_freeze_artifact(artifact)
    except (TypeError, ValueError, KeyError) as exc:
        raise _Blocked("EMBEDDED_F_INVALID") from exc

    universe = artifact.get("qualified_universe")
    if not isinstance(universe, Mapping):
        raise _Blocked("EMBEDDED_F_UNIVERSE_MISSING")
    if result.materialized_acquisition_id != universe.get("acquisition_domain_id"):
        raise _Blocked("RESULT_F_ACQUISITION_MISMATCH")

    reconstruction = universe.get("reconstruction_tuple")
    if not isinstance(reconstruction, Sequence) or isinstance(
        reconstruction, (str, bytes, bytearray)
    ):
        raise _Blocked("EMBEDDED_F_RECONSTRUCTION_MISSING")
    f_by_stage: dict[str, Mapping[str, Any]] = {}
    for raw in reconstruction:
        if not isinstance(raw, Mapping):
            raise _Blocked("EMBEDDED_F_RECONSTRUCTION_INVALID")
        stage = raw.get("stage")
        if stage not in _F_STAGES or stage in f_by_stage:
            raise _Blocked("EMBEDDED_F_RECONSTRUCTION_INVALID")
        f_by_stage[stage] = raw
    if set(f_by_stage) != set(_F_STAGES):
        raise _Blocked("EMBEDDED_F_RECONSTRUCTION_NOT_EXACT")

    result_by_stage = {item["stage"]: item for item in bindings}
    for stage in _F_STAGES:
        if dict(result_by_stage[stage]) != dict(f_by_stage[stage]):
            raise _Blocked("RESULT_F_RECONSTRUCTION_MISMATCH")

    return bindings, artifact


def _pair_gate(
    left_bindings: tuple[dict[str, Any], ...],
    right_bindings: tuple[dict[str, Any], ...],
) -> dict[str, str] | None:
    left = {item["stage"]: item for item in left_bindings}
    right = {item["stage"]: item for item in right_bindings}

    for stage in _STAGES:
        l_item = left[stage]
        r_item = right[stage]
        same_identity_version = (
            l_item["normative_id"] == r_item["normative_id"]
            and l_item["normative_version"] == r_item["normative_version"]
        )
        if same_identity_version and (
            l_item["immutable_reference"] != r_item["immutable_reference"]
            or l_item["integrity_digest"] != r_item["integrity_digest"]
        ):
            return _blocked(
                "NORMATIVE_VERSION_INTEGRITY_CONFLICT",
                "DETERMINANT_CONSISTENCY",
            )

    for stage in _STAGES:
        l_item = left[stage]
        r_item = right[stage]
        if (
            l_item["normative_id"] != r_item["normative_id"]
            or l_item["normative_version"] != r_item["normative_version"]
        ):
            if stage == "O":
                return _blocked("O_DETERMINANT_MISMATCH", "O_DETERMINANT_GATE")
            return _blocked("DISTINCT_QUALIFICATION_STATE", "DETERMINANT_COMPATIBILITY")

    return None


def compare_sealed_results(
    left_result,
    left_receipt,
    right_result,
    right_receipt,
    *,
    expected_left,
    expected_right,
):
    try:
        left_pin = _validate_pin(expected_left)
        right_pin = _validate_pin(expected_right)

        left_bindings, left_f = _validate_result_against_pin(left_result, left_pin)
        right_bindings, right_f = _validate_result_against_pin(right_result, right_pin)

        _validate_receipt(left_receipt, left_pin, left_result)
        _validate_receipt(right_receipt, right_pin, right_result)

        gate = _pair_gate(left_bindings, right_bindings)
        if gate is not None:
            return gate

        oracle_value = oracle.compare_freeze_artifacts(left_f, right_f)
        if not isinstance(oracle_value, Mapping):
            return _blocked("ORACLE_OUTPUT_INVALID", "ORACLE")
        oracle_result = oracle_value.get("oracle_result")
        if oracle_result not in ("SEMANTIC_EQUAL", "SEMANTIC_DIFFERENT", "BLOCKED"):
            return _blocked("ORACLE_OUTPUT_INVALID", "ORACLE")
        if oracle_result == "BLOCKED":
            return _handoff_result(
                "BLOCKED",
                "BLOCKED",
                str(oracle_value.get("comparison_scope", "ORACLE")),
                str(oracle_value.get("reason", "ORACLE_BLOCKED")),
            )
        return _handoff_result(
            oracle_result,
            oracle_result,
            str(oracle_value.get("comparison_scope", "QUALIFIED_UNIVERSE")),
            str(oracle_value.get("reason", oracle_result)),
        )
    except (_Blocked, TypeError, ValueError, KeyError, AttributeError) as exc:
        reason = exc.reason if isinstance(exc, _Blocked) else "POSTSEAL_VALIDATION_ERROR"
        return _blocked(reason)
