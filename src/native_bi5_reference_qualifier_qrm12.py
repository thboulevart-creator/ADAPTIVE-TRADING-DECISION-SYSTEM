from __future__ import annotations

import copy
import hashlib
import json
import lzma
import struct
import sys
from dataclasses import dataclass, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


IMPLEMENTATION_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_QRM12"
IMPLEMENTATION_VERSION = (
    "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_QRM12_V0_2_CANDIDATE"
)
INPUT_SCHEMA = "NATIVE_BI5_QRM12_COMMON_INPUT_PACKAGE_V0_2_CANDIDATE"
RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_2_CANDIDATE"

D_ID = "D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1"
R_ID = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS"
R_VERSION = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE"
M_ID = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL"
M_VERSION = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE"
B_ID = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
B_VERSION = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
A_ID = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
A_VERSION = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
Q_ID = "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP"
Q_VERSION = (
    "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE"
)
F_ID = "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE"
F_VERSION = (
    "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE"
)
F_ARTIFACT_SCHEMA = "QUALIFICATION_FREEZE_ARTIFACT_V0_1_CANDIDATE"
O_ID = "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR"
O_VERSION = (
    "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE"
)

_SOURCE_PATH = "src/native_bi5_reference_qualifier_qrm12.py"
_STAGES = ("D", "R", "M", "B", "A", "Q", "F", "O")
_F_STAGES = ("D", "R", "M", "B", "A", "Q", "F")
_BINDING_FIELDS = {
    "stage",
    "normative_id",
    "normative_version",
    "immutable_reference",
    "integrity_digest",
}
_REQUIRED_PRESEAL_INPUTS = frozenset(
    ("common_immutable_input_package", "own_implementation_runtime", "python_stdlib")
)
_REQUIRED_ENVIRONMENT_VARIABLES = frozenset(
    ("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL")
)
_EXECUTION_STATUSES = frozenset(
    ("COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR")
)
_SEMANTIC_STATUSES = frozenset(
    ("QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED", "NOT_REACHED")
)
_FREEZE_STATUSES = frozenset(("FROZEN", "NOT_CREATED", "NOT_REACHED"))
_SLOT = struct.Struct(">IIIff")
_SLOT_WIDTH = 20
_HOUR_MILLISECONDS = 3_600_000


@dataclass(frozen=True)
class ImplementationQualificationResultV2:
    schema: str
    implementation_id: str
    implementation_version: str
    implementation_manifest_digest: str
    input_determinant_bindings: tuple[Mapping[str, Any], ...]
    materialized_acquisition_id: str
    execution_status: str
    semantic_status: str
    freeze_status: str
    bound_f_artifact: Mapping[str, Any] | None
    terminal_evidence: Mapping[str, Any] | None
    isolation_evidence: Mapping[str, Any]
    result_seal: str


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _source_digest() -> str:
    return _sha256(Path(__file__).read_bytes())


def build_implementation_manifest() -> dict[str, Any]:
    return {
        "implementation_id": IMPLEMENTATION_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "entrypoint": "qualify_native_bi5_v2",
        "source_files": [_SOURCE_PATH],
        "source_digests": {_SOURCE_PATH: _source_digest()},
        "project_dependency_imports": [],
        "external_dependencies": {
            "python": ".".join(str(part) for part in sys.version_info[:3]),
            "compression_primitive": "python-stdlib-lzma",
            "binary_primitive": "python-stdlib-struct",
            "integrity_primitive": "python-stdlib-hashlib-sha256",
            "serialization_primitive": "python-stdlib-json-strict",
        },
        "semantic_stage_ownership": {
            "D_PREFLIGHT": "ia_qrm12_validate_common_input",
            "R_COMPATIBILITY": "ia_qrm12_validate_determinant_bindings",
            "B_ENVELOPE": "ia_qrm12_decompress_exact_single_stream",
            "B_FRAMING": "ia_qrm12_interpret_component",
            "B_BINARY_DECODE": "ia_qrm12_interpret_complete_slot",
            "B_TIMESTAMP": "ia_qrm12_market_timestamp",
            "B_PRICE": "ia_qrm12_interpret_complete_slot",
            "B_VOLUME": "ia_qrm12_binary32_normal_form",
            "A_CLASSIFICATION": "ia_qrm12_anomaly",
            "M_OCCURRENCE": "ia_qrm12_occurrence",
            "Q_MEMBERSHIP": "ia_qrm12_qualify_components",
            "F_FREEZE": "IA_QRM12_PRIVATE_F_BUILDER_VALIDATOR",
        },
        "build_runtime_environment_identity": {
            "runtime": "CPython",
            "major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
    }


def _manifest_digest() -> str:
    return _sha256(_canonical_bytes(build_implementation_manifest()))


def _result_payload(result: ImplementationQualificationResultV2) -> dict[str, Any]:
    return {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }


def _result_seal(result: ImplementationQualificationResultV2) -> str:
    return _sha256(_canonical_bytes(_result_payload(result)))


def _seal_result(
    result: ImplementationQualificationResultV2,
) -> ImplementationQualificationResultV2:
    return replace(result, result_seal=_result_seal(result))


def _safe_acquisition_id(input_package: Any) -> str:
    if not isinstance(input_package, Mapping):
        return ""
    value = input_package.get("acquisition_domain_id")
    return value if isinstance(value, str) else ""


def _safe_bindings(input_package: Any) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(input_package, Mapping):
        return ()
    value = input_package.get("determinant_bindings")
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return ()
    result: list[Mapping[str, Any]] = []
    for raw in value:
        if isinstance(raw, Mapping):
            candidate = copy.deepcopy(dict(raw))
            try:
                _canonical_bytes(candidate)
            except (TypeError, ValueError):
                continue
            result.append(candidate)
    return tuple(result)


def _isolation_evidence(execution_context: Any) -> dict[str, Any]:
    if not isinstance(execution_context, Mapping):
        return {
            "workspace_isolation_identity": None,
            "preseal_input_allowlist": (),
            "network_policy": None,
            "ipc_policy": None,
            "environment_variable_allowlist": (),
            "cache_policy": None,
            "other_path_output_readable": None,
            "runtime_read_set": (),
        }

    allowlist = tuple(execution_context.get("preseal_input_allowlist", ()))
    runtime_read_set = tuple(
        item
        for item in (
            "common_immutable_input_package",
            "own_implementation_runtime",
            "python_stdlib",
        )
        if item in allowlist
    )
    return {
        "workspace_isolation_identity": execution_context.get(
            "workspace_isolation_identity"
        ),
        "preseal_input_allowlist": allowlist,
        "network_policy": execution_context.get("network_policy"),
        "ipc_policy": execution_context.get("ipc_policy"),
        "environment_variable_allowlist": tuple(
            execution_context.get("environment_variable_allowlist", ())
        ),
        "cache_policy": execution_context.get("cache_policy"),
        "other_path_output_readable": execution_context.get(
            "other_path_output_readable"
        ),
        "runtime_read_set": runtime_read_set,
    }


def _isolation_closed(evidence: Mapping[str, Any]) -> bool:
    workspace = evidence.get("workspace_isolation_identity")
    return (
        isinstance(workspace, str)
        and bool(workspace.strip())
        and frozenset(evidence.get("preseal_input_allowlist", ()))
        == _REQUIRED_PRESEAL_INPUTS
        and evidence.get("network_policy") == "DENY"
        and evidence.get("ipc_policy") == "DENY"
        and frozenset(evidence.get("environment_variable_allowlist", ()))
        == _REQUIRED_ENVIRONMENT_VARIABLES
        and evidence.get("cache_policy") == "PRIVATE_ONLY"
        and evidence.get("other_path_output_readable") is False
        and frozenset(evidence.get("runtime_read_set", ()))
        == _REQUIRED_PRESEAL_INPUTS
    )


def _new_result(
    input_package: Any,
    execution_context: Any,
    *,
    execution_status: str,
    semantic_status: str,
    freeze_status: str,
    bound_f_artifact: Mapping[str, Any] | None,
    terminal_evidence: Mapping[str, Any] | None,
    bindings: tuple[Mapping[str, Any], ...] | None = None,
) -> ImplementationQualificationResultV2:
    result = ImplementationQualificationResultV2(
        schema=RESULT_SCHEMA,
        implementation_id=IMPLEMENTATION_ID,
        implementation_version=IMPLEMENTATION_VERSION,
        implementation_manifest_digest=_manifest_digest(),
        input_determinant_bindings=(
            copy.deepcopy(bindings)
            if bindings is not None
            else _safe_bindings(input_package)
        ),
        materialized_acquisition_id=_safe_acquisition_id(input_package),
        execution_status=execution_status,
        semantic_status=semantic_status,
        freeze_status=freeze_status,
        bound_f_artifact=copy.deepcopy(bound_f_artifact),
        terminal_evidence=copy.deepcopy(terminal_evidence),
        isolation_evidence=_isolation_evidence(execution_context),
        result_seal="",
    )
    return _seal_result(result)


def _validate_result_structure(result: ImplementationQualificationResultV2) -> None:
    if not isinstance(result, ImplementationQualificationResultV2):
        raise TypeError("result must be ImplementationQualificationResultV2")
    if result.schema != RESULT_SCHEMA:
        raise ValueError("unexpected result schema")
    if result.implementation_id != IMPLEMENTATION_ID:
        raise ValueError("unexpected implementation identity")
    if result.implementation_version != IMPLEMENTATION_VERSION:
        raise ValueError("unexpected implementation version")
    if result.implementation_manifest_digest != _manifest_digest():
        raise ValueError("implementation manifest digest mismatch")
    if result.execution_status not in _EXECUTION_STATUSES:
        raise ValueError("invalid execution status")
    if result.semantic_status not in _SEMANTIC_STATUSES:
        raise ValueError("invalid semantic status")
    if result.freeze_status not in _FREEZE_STATUSES:
        raise ValueError("invalid freeze status")

    if result.execution_status != "COMPLETED":
        if (
            result.semantic_status != "NOT_REACHED"
            or result.freeze_status != "NOT_REACHED"
            or result.bound_f_artifact is not None
            or result.terminal_evidence is None
        ):
            raise ValueError("non-completed execution state contradiction")
        return

    if result.semantic_status == "QUALIFIED":
        if (
            result.freeze_status != "FROZEN"
            or result.bound_f_artifact is None
            or result.terminal_evidence is not None
        ):
            raise ValueError("qualified result state contradiction")
        artifact = _ia_validate_freeze_artifact(result.bound_f_artifact)
        universe = artifact["qualified_universe"]
        if result.materialized_acquisition_id != universe["acquisition_domain_id"]:
            raise ValueError("result/F acquisition identity mismatch")

        result_bindings = _validate_determinant_bindings(
            result.input_determinant_bindings,
            universe["acquisition_declaration_version"],
        )
        result_by_stage = {
            item["stage"]: item
            for item in result_bindings
        }
        freeze_by_stage = {
            item["stage"]: item
            for item in universe["reconstruction_tuple"]
        }
        if set(freeze_by_stage) != set(_F_STAGES):
            raise ValueError("result/F reconstruction stage mismatch")
        for stage in _F_STAGES:
            if result_by_stage[stage] != freeze_by_stage[stage]:
                raise ValueError("result/F reconstruction binding mismatch")
        return

    if result.semantic_status in ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"):
        if (
            result.freeze_status != "NOT_CREATED"
            or result.bound_f_artifact is not None
            or result.terminal_evidence is None
        ):
            raise ValueError("terminal semantic result state contradiction")
        return

    raise ValueError("completed execution must reach a terminal semantic state")


def is_sealed_implementation_result_v2(value: object) -> bool:
    if not isinstance(value, ImplementationQualificationResultV2):
        return False
    try:
        _validate_result_structure(value)
        return bool(value.result_seal) and value.result_seal == _result_seal(value)
    except (TypeError, ValueError):
        return False


def validate_implementation_result_v2(
    result: ImplementationQualificationResultV2,
) -> ImplementationQualificationResultV2:
    _validate_result_structure(result)
    if not result.result_seal or result.result_seal != _result_seal(result):
        raise ValueError("result seal mismatch")
    return result


def _expected_binding_identity(
    stage: str,
    acquisition_declaration_version: str,
) -> tuple[str, str]:
    expected = {
        "D": (D_ID, acquisition_declaration_version),
        "R": (R_ID, R_VERSION),
        "M": (M_ID, M_VERSION),
        "B": (B_ID, B_VERSION),
        "A": (A_ID, A_VERSION),
        "Q": (Q_ID, Q_VERSION),
        "F": (F_ID, F_VERSION),
        "O": (O_ID, O_VERSION),
    }
    return expected[stage]


def _validate_determinant_bindings(
    value: Any,
    acquisition_declaration_version: str,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("determinant bindings missing")

    by_stage: dict[str, dict[str, Any]] = {}
    for raw in value:
        if not isinstance(raw, Mapping) or set(raw) != _BINDING_FIELDS:
            raise ValueError("determinant binding incomplete")
        binding = copy.deepcopy(dict(raw))
        stage = binding.get("stage")
        if stage not in _STAGES or stage in by_stage:
            raise ValueError("determinant binding stage invalid or repeated")
        for key in ("normative_id", "normative_version", "immutable_reference"):
            if not _is_nonempty_string(binding.get(key)):
                raise ValueError("determinant binding identity invalid")
        if not _is_digest(binding.get("integrity_digest")):
            raise ValueError("determinant binding digest invalid")
        expected_id, expected_version = _expected_binding_identity(
            stage,
            acquisition_declaration_version,
        )
        if (
            binding["normative_id"] != expected_id
            or binding["normative_version"] != expected_version
        ):
            raise ValueError(f"{stage} determinant identity/version mismatch")
        by_stage[stage] = binding

    if set(by_stage) != set(_STAGES):
        raise ValueError("determinant binding set is not exact")
    return tuple(by_stage[stage] for stage in _STAGES)


def _validate_common_input(
    input_package: Any,
) -> tuple[tuple[dict[str, Any], ...], dict[str, Any], tuple[Mapping[str, Any], ...]]:
    if not isinstance(input_package, Mapping):
        raise ValueError("input package must be mapping")
    if input_package.get("schema") != INPUT_SCHEMA:
        raise ValueError("input package schema mismatch")

    acquisition_id = input_package.get("acquisition_domain_id")
    declaration_version = input_package.get("acquisition_declaration_version")
    if not _is_nonempty_string(acquisition_id):
        raise ValueError("acquisition domain identity missing")
    if not _is_nonempty_string(declaration_version):
        raise ValueError("acquisition declaration version missing")

    bindings = _validate_determinant_bindings(
        input_package.get("determinant_bindings"),
        declaration_version,
    )

    parameters = input_package.get("qualification_parameters")
    if not isinstance(parameters, Mapping) or not parameters:
        raise ValueError("qualification parameters missing")
    try:
        _canonical_bytes(dict(parameters))
    except (TypeError, ValueError) as exc:
        raise ValueError("qualification parameters are not strict JSON") from exc

    completeness = input_package.get("d_completeness_evidence")
    if (
        not isinstance(completeness, Mapping)
        or not _is_nonempty_string(completeness.get("immutable_reference"))
        or not _is_digest(completeness.get("integrity_digest"))
    ):
        raise ValueError("D completeness evidence invalid")

    components = input_package.get("components")
    if not isinstance(components, Sequence) or isinstance(
        components, (str, bytes, bytearray)
    ) or not components:
        raise ValueError("component manifest missing")

    evidence = input_package.get("qualification_evidence_bindings", ())
    if not isinstance(evidence, Sequence) or isinstance(evidence, (str, bytes, bytearray)):
        raise ValueError("qualification evidence bindings invalid")

    return (
        bindings,
        copy.deepcopy(dict(parameters)),
        tuple(copy.deepcopy(list(components))),
    )


def _parse_hour(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    parsed = parsed.astimezone(timezone.utc)
    if parsed.minute or parsed.second or parsed.microsecond:
        return None
    return parsed


def _format_timestamp(value: datetime) -> str:
    utc = value.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


def _binary32_normal_form(raw: bytes) -> dict[str, int] | None:
    bits = int.from_bytes(raw, "big")
    sign = -1 if (bits >> 31) else 1
    exponent_bits = (bits >> 23) & 0xFF
    fraction = bits & 0x7FFFFF
    if exponent_bits == 0xFF:
        return None
    if exponent_bits == 0 and fraction == 0:
        return {"integer_coefficient": 0, "exponent2": 0}
    if exponent_bits == 0:
        coefficient = fraction
        exponent2 = -149
    else:
        coefficient = (1 << 23) | fraction
        exponent2 = exponent_bits - 127 - 23
    while coefficient % 2 == 0:
        coefficient //= 2
        exponent2 += 1
    return {"integer_coefficient": sign * coefficient, "exponent2": exponent2}


def _decompress_exact_single_stream(payload: bytes) -> bytes | None:
    try:
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        output = decoder.decompress(payload)
    except lzma.LZMAError:
        return None
    if not decoder.eof or decoder.unused_data:
        return None
    return output


def _anomaly(
    class_id: str,
    outcome: str,
    target_scope: str,
    *,
    acquisition_id: str | None = None,
    component_id: str | None = None,
    slot_index: int | None = None,
    fragment_start: int | None = None,
    fragment_length: int | None = None,
) -> dict[str, Any]:
    target: dict[str, Any] = {"target_scope": target_scope}
    if acquisition_id is not None:
        target["acquisition_domain_id"] = acquisition_id
    if component_id is not None:
        target["component_manifest_entry_id"] = component_id
    if slot_index is not None:
        target["component_local_slot_index"] = slot_index
    if fragment_start is not None:
        target["terminal_fragment_start_offset"] = fragment_start
    if fragment_length is not None:
        target["terminal_fragment_length"] = fragment_length
    return {
        "anomaly_class_id": class_id,
        "anomaly_matrix_version": A_VERSION,
        "target": target,
        "mandatory_outcome": outcome,
        "acquisition_fatal": False,
        "qualification_evidence_bindings": [],
    }


def _occurrence(
    component_id: str,
    slot_index: int,
    raw: bytes,
    hour: datetime,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    millisecond_offset, ask_raw, bid_raw, _ask_float, _bid_float = _SLOT.unpack(raw)
    if millisecond_offset >= _HOUR_MILLISECONDS:
        return None, _anomaly(
            "BI5-A09",
            "REJECT_RECORD",
            "COMPLETE_SLOT",
            component_id=component_id,
            slot_index=slot_index,
        )

    ask_volume = _binary32_normal_form(raw[12:16])
    bid_volume = _binary32_normal_form(raw[16:20])
    if ask_volume is None or bid_volume is None:
        return None, _anomaly(
            "BI5-A10",
            "REJECT_RECORD",
            "COMPLETE_SLOT",
            component_id=component_id,
            slot_index=slot_index,
        )

    return {
        "logical_payload": {
            "market_timestamp_utc": _format_timestamp(
                hour + timedelta(milliseconds=millisecond_offset)
            ),
            "ask_price": {"numerator": ask_raw, "denominator": 1000},
            "bid_price": {"numerator": bid_raw, "denominator": 1000},
            "ask_volume": ask_volume,
            "bid_volume": bid_volume,
        },
        "source_witness": {
            "component_manifest_entry_id": component_id,
            "component_local_slot_index": slot_index,
        },
    }, None


def _interpret_component(
    component: Any,
    acquisition_id: str,
) -> tuple[
    bool,
    dict[str, Any] | None,
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    occurrences: list[dict[str, Any]] = []
    accounting: list[dict[str, Any]] = []
    anomalies: list[dict[str, Any]] = []

    if not isinstance(component, Mapping):
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A11", "QUALIFICATION_BLOCKED", "ACQUISITION", acquisition_id=acquisition_id)
        ]

    component_id = component.get("component_manifest_entry_id")
    if not _is_nonempty_string(component_id):
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A11", "QUALIFICATION_BLOCKED", "ACQUISITION", acquisition_id=acquisition_id)
        ]

    if "complete_slot_count" in component or "terminal_fragment" in component:
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A12", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]

    if (
        component.get("instrument_id") != "USATECHIDXUSD"
        or component.get("instrument_source_identity") != "DUKASCOPY/USATECHIDXUSD"
        or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
        or not _is_nonempty_string(component.get("immutable_payload_reference"))
        or not _is_digest(component.get("payload_integrity_reference"))
    ):
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A12", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]

    hour = _parse_hour(component.get("declared_hour_bucket_utc"))
    if hour is None:
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A04", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]

    payload = component.get("compressed_payload_bytes")
    declared_payload_sha = component.get("payload_sha256")
    if (
        not isinstance(payload, bytes)
        or not _is_digest(declared_payload_sha)
        or declared_payload_sha != component["payload_integrity_reference"]
        or _sha256(payload) != declared_payload_sha
    ):
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A11", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]

    decompressed = _decompress_exact_single_stream(payload)
    if decompressed is None:
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A05", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]
    if not decompressed:
        return False, None, occurrences, accounting, [
            _anomaly("BI5-A06", "QUALIFICATION_BLOCKED", "COMPONENT", component_id=component_id)
        ]

    complete_slot_count, remainder = divmod(len(decompressed), _SLOT_WIDTH)
    snapshot = {
        "component_manifest_entry_id": component_id,
        "declared_role": component["declared_role"],
        "instrument_source_identity": component["instrument_source_identity"],
        "declared_hour_bucket_utc": component["declared_hour_bucket_utc"],
        "immutable_payload_reference": component["immutable_payload_reference"],
        "payload_integrity_reference": component["payload_integrity_reference"],
        "materialization_status": "MATERIALIZED",
        "complete_slot_count": complete_slot_count,
        "terminal_fragment": (
            None
            if remainder == 0
            else {
                "terminal_fragment_start_offset": complete_slot_count * _SLOT_WIDTH,
                "terminal_fragment_length": remainder,
            }
        ),
    }

    for slot_index in range(complete_slot_count):
        start = slot_index * _SLOT_WIDTH
        occurrence, anomaly = _occurrence(
            component_id,
            slot_index,
            decompressed[start : start + _SLOT_WIDTH],
            hour,
        )
        if anomaly is None:
            occurrences.append(occurrence)
            accounting.append(
                {
                    "component_manifest_entry_id": component_id,
                    "component_local_slot_index": slot_index,
                    "disposition": "CANDIDATE_RETAINED",
                    "anomaly_class_id": None,
                }
            )
        else:
            anomalies.append(anomaly)
            accounting.append(
                {
                    "component_manifest_entry_id": component_id,
                    "component_local_slot_index": slot_index,
                    "disposition": "REJECT_RECORD",
                    "anomaly_class_id": anomaly["anomaly_class_id"],
                }
            )

    if remainder:
        anomalies.append(
            _anomaly(
                "BI5-A07",
                "QUALIFICATION_BLOCKED",
                "TERMINAL_FRAGMENT",
                component_id=component_id,
                fragment_start=complete_slot_count * _SLOT_WIDTH,
                fragment_length=remainder,
            )
        )
        return False, snapshot, occurrences, accounting, anomalies

    return True, snapshot, occurrences, accounting, anomalies


def _artifact_digest(artifact: Mapping[str, Any]) -> str:
    unsigned = {
        key: value
        for key, value in artifact.items()
        if key != "artifact_integrity_digest"
    }
    return _sha256(_canonical_bytes(unsigned))


def _ia_build_freeze_artifact(
    *,
    acquisition_id: str,
    declaration_version: str,
    bindings: tuple[Mapping[str, Any], ...],
    parameters: Mapping[str, Any],
    completeness: Mapping[str, Any],
    component_snapshots: Sequence[Mapping[str, Any]],
    accounting: Sequence[Mapping[str, Any]],
    anomalies: Sequence[Mapping[str, Any]],
    occurrences: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    by_stage = {item["stage"]: item for item in bindings}
    universe = {
        "acquisition_domain_id": acquisition_id,
        "acquisition_declaration_version": declaration_version,
        "qualification_parameters": copy.deepcopy(dict(parameters)),
        "completeness_evidence": copy.deepcopy(dict(completeness)),
        "reconstruction_tuple": [
            copy.deepcopy(by_stage[stage]) for stage in _F_STAGES
        ],
        "components": copy.deepcopy(list(component_snapshots)),
        "source_accounting": copy.deepcopy(list(accounting)),
        "anomaly_outcomes": copy.deepcopy(list(anomalies)),
        "retained_occurrences": copy.deepcopy(list(occurrences)),
        "b_candidate_occurrences": copy.deepcopy(list(occurrences)),
    }
    artifact = {
        "schema": F_ARTIFACT_SCHEMA,
        "freeze_contract_id": F_ID,
        "freeze_contract_version": F_VERSION,
        "artifact_class": "QUALIFIED_UNIVERSE_FREEZE",
        "freeze_state": "FROZEN",
        "qualification_outcome": "QUALIFIED",
        "qualified_universe": universe,
        "qualified_occurrence_count": len(occurrences),
        "terminal_evidence": None,
    }
    artifact["artifact_integrity_digest"] = _artifact_digest(artifact)
    return artifact


def _validate_payload(payload: Any) -> None:
    if not isinstance(payload, Mapping) or set(payload) != {
        "market_timestamp_utc",
        "ask_price",
        "bid_price",
        "ask_volume",
        "bid_volume",
    }:
        raise ValueError("logical payload shape invalid")
    timestamp = payload["market_timestamp_utc"]
    if not isinstance(timestamp, str):
        raise ValueError("timestamp invalid")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise ValueError("timestamp invalid") from exc
    for key in ("ask_price", "bid_price"):
        price = payload[key]
        if (
            not isinstance(price, Mapping)
            or set(price) != {"numerator", "denominator"}
            or isinstance(price["numerator"], bool)
            or not isinstance(price["numerator"], int)
            or not 0 <= price["numerator"] <= 0xFFFFFFFF
            or price["denominator"] != 1000
        ):
            raise ValueError("price invalid")
    for key in ("ask_volume", "bid_volume"):
        volume = payload[key]
        if (
            not isinstance(volume, Mapping)
            or set(volume) != {"integer_coefficient", "exponent2"}
            or isinstance(volume["integer_coefficient"], bool)
            or not isinstance(volume["integer_coefficient"], int)
            or isinstance(volume["exponent2"], bool)
            or not isinstance(volume["exponent2"], int)
        ):
            raise ValueError("volume invalid")
        coefficient = volume["integer_coefficient"]
        exponent = volume["exponent2"]
        if coefficient == 0:
            if exponent != 0:
                raise ValueError("zero volume normal form invalid")
        else:
            if coefficient % 2 == 0:
                raise ValueError("volume coefficient not normalized")
            bits = abs(coefficient).bit_length()
            if bits > 24 or exponent < -149 or exponent + bits - 1 > 127:
                raise ValueError("volume outside binary32 domain")


def _ia_validate_freeze_artifact(artifact: Any) -> Mapping[str, Any]:
    if not isinstance(artifact, Mapping):
        raise TypeError("freeze artifact must be mapping")
    if (
        artifact.get("schema") != F_ARTIFACT_SCHEMA
        or artifact.get("freeze_contract_id") != F_ID
        or artifact.get("freeze_contract_version") != F_VERSION
        or artifact.get("artifact_class") != "QUALIFIED_UNIVERSE_FREEZE"
        or artifact.get("freeze_state") != "FROZEN"
        or artifact.get("qualification_outcome") != "QUALIFIED"
        or artifact.get("terminal_evidence") is not None
    ):
        raise ValueError("freeze artifact identity/state invalid")
    if (
        not _is_digest(artifact.get("artifact_integrity_digest"))
        or artifact["artifact_integrity_digest"] != _artifact_digest(artifact)
    ):
        raise ValueError("freeze artifact digest invalid")

    universe = artifact.get("qualified_universe")
    if not isinstance(universe, Mapping):
        raise ValueError("qualified universe missing")
    acquisition_id = universe.get("acquisition_domain_id")
    declaration_version = universe.get("acquisition_declaration_version")
    if not _is_nonempty_string(acquisition_id) or not _is_nonempty_string(declaration_version):
        raise ValueError("qualified universe identity invalid")

    reconstruction = universe.get("reconstruction_tuple")
    validated_bindings = _validate_determinant_bindings(
        list(reconstruction or ()) + [
            {
                "stage": "O",
                "normative_id": O_ID,
                "normative_version": O_VERSION,
                "immutable_reference": "private-validation://o-placeholder",
                "integrity_digest": "0" * 64,
            }
        ],
        declaration_version,
    )
    if tuple(item["stage"] for item in validated_bindings[:7]) != _F_STAGES:
        raise ValueError("freeze reconstruction tuple invalid")

    parameters = universe.get("qualification_parameters")
    completeness = universe.get("completeness_evidence")
    components = universe.get("components")
    accounting = universe.get("source_accounting")
    anomalies = universe.get("anomaly_outcomes")
    retained = universe.get("retained_occurrences")
    b_candidates = universe.get("b_candidate_occurrences")
    if not isinstance(parameters, Mapping) or not parameters:
        raise ValueError("freeze qualification parameters missing")
    if (
        not isinstance(completeness, Mapping)
        or not _is_nonempty_string(completeness.get("immutable_reference"))
        or not _is_digest(completeness.get("integrity_digest"))
    ):
        raise ValueError("freeze completeness evidence invalid")
    if not all(
        isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))
        for value in (components, accounting, anomalies, retained, b_candidates)
    ):
        raise ValueError("freeze relations invalid")
    if not components:
        raise ValueError("qualified freeze component universe empty")

    component_counts: dict[str, int] = {}
    component_hours: dict[str, datetime] = {}
    for component in components:
        if not isinstance(component, Mapping):
            raise ValueError("freeze component invalid")
        component_id = component.get("component_manifest_entry_id")
        count = component.get("complete_slot_count")
        if (
            not _is_nonempty_string(component_id)
            or component_id in component_counts
            or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
            or component.get("instrument_source_identity") != "DUKASCOPY/USATECHIDXUSD"
            or not _is_nonempty_string(component.get("immutable_payload_reference"))
            or not _is_digest(component.get("payload_integrity_reference"))
            or component.get("materialization_status") != "MATERIALIZED"
            or isinstance(count, bool)
            or not isinstance(count, int)
            or count <= 0
            or component.get("terminal_fragment") is not None
        ):
            raise ValueError("freeze component invalid")
        hour = _parse_hour(component.get("declared_hour_bucket_utc"))
        if hour is None:
            raise ValueError("freeze component hour invalid")
        component_counts[component_id] = count
        component_hours[component_id] = hour

    expected_sources = {
        (component_id, slot)
        for component_id, count in component_counts.items()
        for slot in range(count)
    }
    accounting_map: dict[tuple[str, int], Mapping[str, Any]] = {}
    for item in accounting:
        if not isinstance(item, Mapping) or set(item) != {
            "component_manifest_entry_id",
            "component_local_slot_index",
            "disposition",
            "anomaly_class_id",
        }:
            raise ValueError("freeze accounting invalid")
        source = (
            item.get("component_manifest_entry_id"),
            item.get("component_local_slot_index"),
        )
        if (
            source not in expected_sources
            or source in accounting_map
            or item.get("disposition") not in ("CANDIDATE_RETAINED", "REJECT_RECORD")
        ):
            raise ValueError("freeze accounting relation invalid")
        if item["disposition"] == "CANDIDATE_RETAINED":
            if item.get("anomaly_class_id") is not None:
                raise ValueError("retained accounting carries anomaly")
        elif item.get("anomaly_class_id") not in ("BI5-A09", "BI5-A10"):
            raise ValueError("rejected accounting anomaly invalid")
        accounting_map[source] = item
    if set(accounting_map) != expected_sources:
        raise ValueError("freeze accounting incomplete")

    def occurrence_relation(rows: Sequence[Any]) -> dict[tuple[str, int], Any]:
        relation: dict[tuple[str, int], Any] = {}
        for occurrence in rows:
            if (
                not isinstance(occurrence, Mapping)
                or not set(occurrence).issubset(
                    {"logical_payload", "source_witness", "source_provenance"}
                )
            ):
                raise ValueError("freeze occurrence invalid")
            witness = occurrence.get("source_witness")
            if not isinstance(witness, Mapping) or set(witness) != {
                "component_manifest_entry_id",
                "component_local_slot_index",
            }:
                raise ValueError("freeze witness invalid")
            source = (
                witness.get("component_manifest_entry_id"),
                witness.get("component_local_slot_index"),
            )
            if source not in expected_sources or source in relation:
                raise ValueError("freeze occurrence witness invalid")
            _validate_payload(occurrence.get("logical_payload"))
            timestamp = datetime.strptime(
                occurrence["logical_payload"]["market_timestamp_utc"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            declared_hour = component_hours[source[0]].replace(tzinfo=None)
            if not (declared_hour <= timestamp < declared_hour + timedelta(hours=1)):
                raise ValueError("freeze occurrence timestamp outside declared hour")
            relation[source] = copy.deepcopy(occurrence["logical_payload"])
        return relation

    retained_relation = occurrence_relation(retained)
    b_relation = occurrence_relation(b_candidates)
    if retained_relation != b_relation:
        raise ValueError("B/Q occurrence relation mismatch")

    retained_sources = {
        source
        for source, item in accounting_map.items()
        if item["disposition"] == "CANDIDATE_RETAINED"
    }
    rejected_sources = expected_sources - retained_sources
    if set(retained_relation) != retained_sources:
        raise ValueError("retained occurrence/accounting mismatch")

    anomaly_relation: set[tuple[str, int, str]] = set()
    for anomaly in anomalies:
        if (
            not isinstance(anomaly, Mapping)
            or anomaly.get("anomaly_matrix_version") != A_VERSION
            or anomaly.get("mandatory_outcome") != "REJECT_RECORD"
            or anomaly.get("acquisition_fatal") is not False
            or anomaly.get("qualification_evidence_bindings") not in ([], ())
            or anomaly.get("anomaly_class_id") not in ("BI5-A09", "BI5-A10")
        ):
            raise ValueError("freeze local anomaly invalid")
        target = anomaly.get("target")
        if not isinstance(target, Mapping) or set(target) != {
            "target_scope",
            "component_manifest_entry_id",
            "component_local_slot_index",
        } or target.get("target_scope") != "COMPLETE_SLOT":
            raise ValueError("freeze anomaly target invalid")
        relation = (
            target.get("component_manifest_entry_id"),
            target.get("component_local_slot_index"),
            anomaly["anomaly_class_id"],
        )
        if relation in anomaly_relation:
            raise ValueError("freeze anomaly repeated")
        anomaly_relation.add(relation)

    expected_anomalies = {
        (source[0], source[1], accounting_map[source]["anomaly_class_id"])
        for source in rejected_sources
    }
    if anomaly_relation != expected_anomalies:
        raise ValueError("freeze anomaly/accounting mismatch")

    count = artifact.get("qualified_occurrence_count")
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count != len(retained)
    ):
        raise ValueError("freeze qualified occurrence count mismatch")
    return artifact


def _blocked(
    input_package: Any,
    execution_context: Any,
    reason: str,
    *,
    bindings: tuple[Mapping[str, Any], ...] | None = None,
    anomalies: Sequence[Mapping[str, Any]] = (),
) -> ImplementationQualificationResultV2:
    return _new_result(
        input_package,
        execution_context,
        execution_status="COMPLETED",
        semantic_status="QUALIFICATION_BLOCKED",
        freeze_status="NOT_CREATED",
        bound_f_artifact=None,
        terminal_evidence={
            "reason": reason,
            "anomaly_outcomes": copy.deepcopy(list(anomalies)),
        },
        bindings=bindings,
    )


def _environment_blocked(
    input_package: Any,
    execution_context: Any,
) -> ImplementationQualificationResultV2:
    return _new_result(
        input_package,
        execution_context,
        execution_status="ENVIRONMENT_BLOCKED",
        semantic_status="NOT_REACHED",
        freeze_status="NOT_REACHED",
        bound_f_artifact=None,
        terminal_evidence={"reason": "PRESEAL_EXECUTION_ENVIRONMENT_NOT_CLOSED"},
    )


def _implementation_error(
    input_package: Any,
    execution_context: Any,
    reason: str,
) -> ImplementationQualificationResultV2:
    return _new_result(
        input_package,
        execution_context,
        execution_status="IMPLEMENTATION_ERROR",
        semantic_status="NOT_REACHED",
        freeze_status="NOT_REACHED",
        bound_f_artifact=None,
        terminal_evidence={"reason": reason},
    )


def _qualify_components(
    input_package: Mapping[str, Any],
    execution_context: Mapping[str, Any],
    bindings: tuple[Mapping[str, Any], ...],
    parameters: Mapping[str, Any],
    components: tuple[Mapping[str, Any], ...],
) -> ImplementationQualificationResultV2:
    acquisition_id = str(input_package["acquisition_domain_id"])
    declaration_version = str(input_package["acquisition_declaration_version"])
    completeness = copy.deepcopy(dict(input_package["d_completeness_evidence"]))

    ids: dict[str, int] = {}
    for component in components:
        if isinstance(component, Mapping):
            component_id = component.get("component_manifest_entry_id")
            if _is_nonempty_string(component_id):
                ids[component_id] = ids.get(component_id, 0) + 1
    duplicates = {key for key, count in ids.items() if count > 1}
    if duplicates:
        anomalies = [
            _anomaly(
                "BI5-A03",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
            for component_id in sorted(duplicates)
        ]
        return _blocked(
            input_package,
            execution_context,
            "DUPLICATED_COMPONENT_IDENTITY",
            bindings=bindings,
            anomalies=anomalies,
        )

    snapshots: list[Mapping[str, Any]] = []
    occurrences: list[Mapping[str, Any]] = []
    accounting: list[Mapping[str, Any]] = []
    anomalies: list[Mapping[str, Any]] = []
    blocked = False

    for component in components:
        ok, snapshot, local_occurrences, local_accounting, local_anomalies = (
            _interpret_component(component, acquisition_id)
        )
        if snapshot is not None:
            snapshots.append(snapshot)
        occurrences.extend(local_occurrences)
        accounting.extend(local_accounting)
        anomalies.extend(local_anomalies)
        if not ok:
            blocked = True

    if blocked:
        return _blocked(
            input_package,
            execution_context,
            "QUALIFICATION_BLOCKED_ANOMALY",
            bindings=bindings,
            anomalies=anomalies,
        )

    source_keys = [
        (
            item["source_witness"]["component_manifest_entry_id"],
            item["source_witness"]["component_local_slot_index"],
        )
        for item in occurrences
    ]
    if len(set(source_keys)) != len(source_keys):
        return _blocked(
            input_package,
            execution_context,
            "DUPLICATED_SOURCE_SLOT_CANDIDATE",
            bindings=bindings,
            anomalies=anomalies,
        )

    artifact = _ia_build_freeze_artifact(
        acquisition_id=acquisition_id,
        declaration_version=declaration_version,
        bindings=bindings,
        parameters=parameters,
        completeness=completeness,
        component_snapshots=snapshots,
        accounting=accounting,
        anomalies=anomalies,
        occurrences=occurrences,
    )
    _ia_validate_freeze_artifact(artifact)

    result = _new_result(
        input_package,
        execution_context,
        execution_status="COMPLETED",
        semantic_status="QUALIFIED",
        freeze_status="FROZEN",
        bound_f_artifact=artifact,
        terminal_evidence=None,
        bindings=bindings,
    )
    return validate_implementation_result_v2(result)


def qualify_native_bi5_v2(
    input_package: Mapping[str, Any],
    *,
    execution_context: Mapping[str, Any],
) -> ImplementationQualificationResultV2:
    isolation = _isolation_evidence(execution_context)
    if not _isolation_closed(isolation):
        return _environment_blocked(input_package, execution_context)

    try:
        bindings, parameters, components = _validate_common_input(input_package)
    except (TypeError, ValueError) as exc:
        return _blocked(
            input_package,
            execution_context,
            f"COMMON_INPUT_INVALID:{exc}",
        )

    try:
        return _qualify_components(
            input_package,
            execution_context,
            bindings,
            parameters,
            components,
        )
    except (TypeError, ValueError, lzma.LZMAError, struct.error, OverflowError) as exc:
        return _implementation_error(
            input_package,
            execution_context,
            f"REFERENCE_PATH_IMPLEMENTATION_ERROR:{type(exc).__name__}",
        )
