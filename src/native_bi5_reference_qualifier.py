from __future__ import annotations

import hashlib
import json
import lzma
import math
import struct
import sys
from dataclasses import dataclass, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


IMPLEMENTATION_ID = "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER"
IMPLEMENTATION_VERSION = (
    "I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_V0_1_CANDIDATE"
)
RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_1_CANDIDATE"

REPRESENTATION_ID = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS"
REPRESENTATION_VERSION = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE"
RECORD_MODEL_VERSION = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE"
FORMAT_BINDING_ID = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
FORMAT_BINDING_VERSION = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
ANOMALY_MATRIX_ID = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
ANOMALY_MATRIX_VERSION = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
QUALIFICATION_CONTRACT_ID = (
    "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP"
)
QUALIFICATION_CONTRACT_VERSION = (
    "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE"
)
FREEZE_CONTRACT_ID = (
    "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE"
)
FREEZE_CONTRACT_VERSION = (
    "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE"
)
ORACLE_ID = "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR"
ORACLE_VERSION = (
    "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE"
)

_REQUIRED_DETERMINANTS = frozenset(("D", "R", "M", "B", "A", "Q", "F", "O"))
_EXECUTION_STATUSES = frozenset(
    ("COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR")
)
_SEMANTIC_STATUSES = frozenset(
    ("QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED", "NOT_REACHED")
)
_FREEZE_STATUSES = frozenset(("FROZEN", "NOT_CREATED", "NOT_REACHED"))
_REQUIRED_PRESEAL_INPUTS = frozenset(
    ("common_immutable_input_package", "own_implementation_runtime", "python_stdlib")
)
_REQUIRED_ENVIRONMENT_VARIABLES = frozenset(
    ("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL")
)
_SLOT = struct.Struct(">IIIff")
_SLOT_WIDTH = 20
_HOUR_MILLISECONDS = 3_600_000
_SOURCE_PATH = "src/native_bi5_reference_qualifier.py"


@dataclass(frozen=True)
class ImplementationQualificationResult:
    schema: str
    implementation_id: str
    implementation_version: str
    implementation_manifest_digest: str
    input_determinant_digests: Mapping[str, str]
    materialized_acquisition_id: str
    execution_status: str
    semantic_status: str
    freeze_status: str
    qualified_occurrences: tuple[Mapping[str, Any], ...] | None
    source_accounting: tuple[Mapping[str, Any], ...] | None
    anomaly_outcomes: tuple[Mapping[str, Any], ...] | None
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
    ).encode("utf-8")


def _source_digest() -> str:
    return _sha256(Path(__file__).read_bytes())


def build_implementation_manifest() -> dict[str, Any]:
    return {
        "implementation_id": IMPLEMENTATION_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "entrypoint": "qualify_native_bi5",
        "source_files": [_SOURCE_PATH],
        "source_digests": {_SOURCE_PATH: _source_digest()},
        "project_dependencies": [],
        "external_dependencies": {
            "python": ".".join(str(part) for part in sys.version_info[:3]),
            "compression_primitive": "python-stdlib-lzma",
            "binary_primitive": "python-stdlib-struct",
        },
        "semantic_stage_ownership": {
            "D_PREFLIGHT": "_validate_package_identity",
            "R_COMPATIBILITY": "_validate_package_identity",
            "B_ENVELOPE": "_decompress_exact_single_stream",
            "B_FRAMING": "_interpret_component",
            "B_BINARY_DECODE": "_interpret_complete_slot",
            "B_TIMESTAMP": "_market_timestamp",
            "B_PRICE": "_interpret_complete_slot",
            "B_VOLUME": "_binary32_normal_form",
            "A_CLASSIFICATION": "_anomaly",
            "M_OCCURRENCE": "_interpret_complete_slot",
            "Q_MEMBERSHIP": "_qualify_components",
            "F_FREEZE": "_build_terminal_result",
        },
        "build_runtime_environment_identity": {
            "runtime": "CPython",
            "major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
    }


def _manifest_digest() -> str:
    return _sha256(_canonical_bytes(build_implementation_manifest()))


def _is_hex_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _copy_digests(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}


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


def _result_payload(result: ImplementationQualificationResult) -> dict[str, Any]:
    return {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }


def _compute_result_seal(result: ImplementationQualificationResult) -> str:
    return _sha256(_canonical_bytes(_result_payload(result)))


def _seal(result: ImplementationQualificationResult) -> ImplementationQualificationResult:
    return replace(result, result_seal=_compute_result_seal(result))


def _validate_result_structure(result: ImplementationQualificationResult) -> None:
    if not isinstance(result, ImplementationQualificationResult):
        raise TypeError("result must be ImplementationQualificationResult")
    if result.schema != RESULT_SCHEMA:
        raise ValueError("unexpected result schema")
    if result.implementation_id != IMPLEMENTATION_ID:
        raise ValueError("unexpected implementation identity")
    if result.implementation_version != IMPLEMENTATION_VERSION:
        raise ValueError("unexpected implementation version")
    if result.execution_status not in _EXECUTION_STATUSES:
        raise ValueError("invalid execution status")
    if result.semantic_status not in _SEMANTIC_STATUSES:
        raise ValueError("invalid semantic status")
    if result.freeze_status not in _FREEZE_STATUSES:
        raise ValueError("invalid freeze status")

    qualified_state = (
        result.execution_status == "COMPLETED"
        and result.semantic_status == "QUALIFIED"
        and result.freeze_status == "FROZEN"
    )

    if not qualified_state:
        if result.qualified_occurrences is not None:
            raise ValueError("non-qualified state cannot expose a qualified universe")
        if result.source_accounting is not None:
            raise ValueError("non-qualified state cannot expose normative source accounting")

    if result.execution_status != "COMPLETED":
        if result.semantic_status != "NOT_REACHED" or result.freeze_status != "NOT_REACHED":
            raise ValueError("non-completed execution cannot claim semantic terminal state")
    elif result.semantic_status == "QUALIFIED":
        if result.freeze_status != "FROZEN":
            raise ValueError("qualified result must be frozen")
        if result.qualified_occurrences is None or result.source_accounting is None:
            raise ValueError("qualified result requires complete universe and accounting")
    elif result.semantic_status in ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"):
        if result.freeze_status != "NOT_CREATED":
            raise ValueError("non-qualified semantic result cannot create freeze")
    elif result.semantic_status == "NOT_REACHED":
        raise ValueError("completed execution must reach a semantic terminal state")

    if result.freeze_status == "FROZEN" and result.semantic_status != "QUALIFIED":
        raise ValueError("frozen result must be qualified")


def is_sealed_implementation_result(value: object) -> bool:
    if not isinstance(value, ImplementationQualificationResult):
        return False
    try:
        _validate_result_structure(value)
        return bool(value.result_seal) and value.result_seal == _compute_result_seal(value)
    except (TypeError, ValueError):
        return False


def validate_implementation_result(
    result: ImplementationQualificationResult,
) -> ImplementationQualificationResult:
    _validate_result_structure(result)
    if not result.result_seal or result.result_seal != _compute_result_seal(result):
        raise ValueError("result seal mismatch")
    return result


def _anomaly(
    class_id: str,
    outcome: str,
    target_scope: str,
    *,
    acquisition_domain_id: str | None = None,
    component_id: str | None = None,
    slot_index: int | None = None,
    fragment_start: int | None = None,
    fragment_length: int | None = None,
    evidence_bindings: tuple[Mapping[str, Any], ...] = (),
) -> dict[str, Any]:
    target: dict[str, Any] = {"target_scope": target_scope}
    if acquisition_domain_id is not None:
        target["acquisition_domain_id"] = acquisition_domain_id
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
        "anomaly_matrix_version": ANOMALY_MATRIX_VERSION,
        "target": target,
        "mandatory_outcome": outcome,
        "acquisition_fatal": False,
        "qualification_evidence_bindings": tuple(evidence_bindings),
    }


def _parse_hour(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    parsed = parsed.astimezone(timezone.utc)
    if (
        parsed.minute != 0
        or parsed.second != 0
        or parsed.microsecond != 0
        or not value.endswith("Z")
    ):
        return None
    return parsed


def _format_timestamp(value: datetime) -> str:
    utc = value.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.") + f"{utc.microsecond // 1000:03d}Z"


def _binary32_normal_form(raw: bytes) -> tuple[int, int] | None:
    bits = int.from_bytes(raw, "big")
    sign = -1 if (bits >> 31) else 1
    exponent_bits = (bits >> 23) & 0xFF
    fraction = bits & 0x7FFFFF

    if exponent_bits == 0xFF:
        return None
    if exponent_bits == 0 and fraction == 0:
        return (0, 0)

    if exponent_bits == 0:
        coefficient = fraction
        exponent2 = -149
    else:
        coefficient = (1 << 23) | fraction
        exponent2 = exponent_bits - 127 - 23

    while coefficient % 2 == 0:
        coefficient //= 2
        exponent2 += 1
    return (sign * coefficient, exponent2)


def _market_timestamp(hour: datetime, millisecond_offset: int) -> str:
    return _format_timestamp(hour + timedelta(milliseconds=millisecond_offset))


def _decompress_exact_single_stream(payload: bytes) -> bytes | None:
    try:
        decoder = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
        output = decoder.decompress(payload)
    except lzma.LZMAError:
        return None
    if not decoder.eof:
        return None
    if decoder.unused_data:
        return None
    return output


def _validate_package_identity(input_package: Any) -> tuple[bool, str]:
    if not isinstance(input_package, Mapping):
        return False, "INPUT_PACKAGE_NOT_MAPPING"

    exact = {
        "representation_id": REPRESENTATION_ID,
        "representation_version": REPRESENTATION_VERSION,
        "record_model_version": RECORD_MODEL_VERSION,
        "format_binding_id": FORMAT_BINDING_ID,
        "format_binding_version": FORMAT_BINDING_VERSION,
        "anomaly_matrix_id": ANOMALY_MATRIX_ID,
        "anomaly_matrix_version": ANOMALY_MATRIX_VERSION,
        "qualification_contract_id": QUALIFICATION_CONTRACT_ID,
        "qualification_contract_version": QUALIFICATION_CONTRACT_VERSION,
        "freeze_contract_id": FREEZE_CONTRACT_ID,
        "freeze_contract_version": FREEZE_CONTRACT_VERSION,
        "oracle_id": ORACLE_ID,
        "oracle_version": ORACLE_VERSION,
    }
    for key, expected in exact.items():
        if input_package.get(key) != expected:
            return False, f"IDENTITY_MISMATCH:{key}"

    acquisition_id = input_package.get("acquisition_domain_id")
    if not isinstance(acquisition_id, str) or not acquisition_id:
        return False, "MISSING_ACQUISITION_DOMAIN_ID"

    digests = input_package.get("determinant_digests")
    if not isinstance(digests, Mapping):
        return False, "MISSING_DETERMINANT_DIGESTS"
    if set(digests) != _REQUIRED_DETERMINANTS:
        return False, "INCOMPLETE_DETERMINANT_SET"
    if any(not _is_hex_digest(value) for value in digests.values()):
        return False, "INVALID_DETERMINANT_DIGEST"

    components = input_package.get("components")
    if not isinstance(components, (tuple, list)) or not components:
        return False, "MISSING_COMPONENT_MANIFEST"
    return True, "OK"


def _interpret_complete_slot(
    component_id: str,
    slot_index: int,
    raw: bytes,
    hour: datetime,
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
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

    occurrence = {
        "market_timestamp_utc": _market_timestamp(hour, millisecond_offset),
        "ask_price_numerator": ask_raw,
        "ask_price_denominator": 1000,
        "bid_price_numerator": bid_raw,
        "bid_price_denominator": 1000,
        "ask_volume": ask_volume,
        "bid_volume": bid_volume,
        "source_volume_unit": "DUKASCOPY_SOURCE_VOLUME_UNIT_V1_CANDIDATE",
        "component_manifest_entry_id": component_id,
        "component_local_slot_index": slot_index,
    }
    return occurrence, None


def _interpret_component(
    component: Any,
    acquisition_domain_id: str,
    qualification_evidence_bindings: Any,
) -> tuple[
    bool,
    list[Mapping[str, Any]],
    list[Mapping[str, Any]],
    list[Mapping[str, Any]],
]:
    occurrences: list[Mapping[str, Any]] = []
    accounting: list[Mapping[str, Any]] = []
    anomalies: list[Mapping[str, Any]] = []

    if not isinstance(component, Mapping):
        anomalies.append(
            _anomaly(
                "BI5-A11",
                "QUALIFICATION_BLOCKED",
                "ACQUISITION",
                acquisition_domain_id=acquisition_domain_id,
            )
        )
        return False, occurrences, accounting, anomalies

    component_id = component.get("component_manifest_entry_id")
    if not isinstance(component_id, str) or not component_id:
        anomalies.append(
            _anomaly(
                "BI5-A11",
                "QUALIFICATION_BLOCKED",
                "ACQUISITION",
                acquisition_domain_id=acquisition_domain_id,
            )
        )
        return False, occurrences, accounting, anomalies

    if (
        component.get("instrument_id") != "USATECHIDXUSD"
        or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
    ):
        anomalies.append(
            _anomaly(
                "BI5-A12",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies

    hour = _parse_hour(component.get("declared_hour_bucket_utc"))
    if hour is None:
        anomalies.append(
            _anomaly(
                "BI5-A04",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies

    payload = component.get("compressed_payload_bytes")
    expected_hash = component.get("payload_sha256")
    if not isinstance(payload, bytes) or not _is_hex_digest(expected_hash):
        anomalies.append(
            _anomaly(
                "BI5-A11",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies
    if _sha256(payload) != expected_hash:
        anomalies.append(
            _anomaly(
                "BI5-A11",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies

    decompressed = _decompress_exact_single_stream(payload)
    if decompressed is None:
        anomalies.append(
            _anomaly(
                "BI5-A05",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies
    if len(decompressed) == 0:
        anomalies.append(
            _anomaly(
                "BI5-A06",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        return False, occurrences, accounting, anomalies

    complete_slot_count, remainder = divmod(len(decompressed), _SLOT_WIDTH)
    for slot_index in range(complete_slot_count):
        start = slot_index * _SLOT_WIDTH
        occurrence, anomaly = _interpret_complete_slot(
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
        start = complete_slot_count * _SLOT_WIDTH
        anomalies.append(
            _anomaly(
                "BI5-A07",
                "QUALIFICATION_BLOCKED",
                "TERMINAL_FRAGMENT",
                component_id=component_id,
                fragment_start=start,
                fragment_length=remainder,
            )
        )
        return False, occurrences, accounting, anomalies

    return True, occurrences, accounting, anomalies


def _blocked_result(
    input_package: Any,
    execution_context: Any,
    reason: str,
    anomalies: tuple[Mapping[str, Any], ...] = (),
    source_accounting: tuple[Mapping[str, Any], ...] = (),
) -> ImplementationQualificationResult:
    acquisition_id = (
        str(input_package.get("acquisition_domain_id", ""))
        if isinstance(input_package, Mapping)
        else ""
    )
    result = ImplementationQualificationResult(
        schema=RESULT_SCHEMA,
        implementation_id=IMPLEMENTATION_ID,
        implementation_version=IMPLEMENTATION_VERSION,
        implementation_manifest_digest=_manifest_digest(),
        input_determinant_digests=_copy_digests(
            input_package.get("determinant_digests", {})
            if isinstance(input_package, Mapping)
            else {}
        ),
        materialized_acquisition_id=acquisition_id,
        execution_status="COMPLETED",
        semantic_status="QUALIFICATION_BLOCKED",
        freeze_status="NOT_CREATED",
        qualified_occurrences=None,
        source_accounting=None,
        anomaly_outcomes=anomalies,
        terminal_evidence={
            "artifact_class": "QUALIFICATION_TERMINAL_EVIDENCE",
            "freeze_state": "NOT_CREATED",
            "qualified_universe": None,
            "qualified_occurrence_count": None,
            "reason": reason,
            "execution_diagnostics": {
                "non_normative_source_accounting": source_accounting,
            },
        },
        isolation_evidence=_isolation_evidence(execution_context),
        result_seal="",
    )
    return _seal(result)


def _build_terminal_result(
    input_package: Mapping[str, Any],
    execution_context: Any,
    occurrences: tuple[Mapping[str, Any], ...],
    accounting: tuple[Mapping[str, Any], ...],
    anomalies: tuple[Mapping[str, Any], ...],
) -> ImplementationQualificationResult:
    result = ImplementationQualificationResult(
        schema=RESULT_SCHEMA,
        implementation_id=IMPLEMENTATION_ID,
        implementation_version=IMPLEMENTATION_VERSION,
        implementation_manifest_digest=_manifest_digest(),
        input_determinant_digests=_copy_digests(input_package["determinant_digests"]),
        materialized_acquisition_id=str(input_package["acquisition_domain_id"]),
        execution_status="COMPLETED",
        semantic_status="QUALIFIED",
        freeze_status="FROZEN",
        qualified_occurrences=occurrences,
        source_accounting=accounting,
        anomaly_outcomes=anomalies,
        terminal_evidence=None,
        isolation_evidence=_isolation_evidence(execution_context),
        result_seal="",
    )
    sealed = _seal(result)
    return validate_implementation_result(sealed)


def _qualify_components(
    input_package: Mapping[str, Any],
    execution_context: Any,
) -> ImplementationQualificationResult:
    components = input_package["components"]
    acquisition_id = str(input_package["acquisition_domain_id"])
    evidence_bindings = input_package.get("qualification_evidence_bindings", ())

    id_counts: dict[str, int] = {}
    for component in components:
        if isinstance(component, Mapping):
            component_id = component.get("component_manifest_entry_id")
            if isinstance(component_id, str) and component_id:
                id_counts[component_id] = id_counts.get(component_id, 0) + 1

    duplicate_ids = {
        component_id
        for component_id, count in id_counts.items()
        if count > 1
    }

    all_occurrences: list[Mapping[str, Any]] = []
    all_accounting: list[Mapping[str, Any]] = []
    all_anomalies: list[Mapping[str, Any]] = []
    blocked = False

    for component_id in sorted(duplicate_ids):
        all_anomalies.append(
            _anomaly(
                "BI5-A03",
                "QUALIFICATION_BLOCKED",
                "COMPONENT",
                component_id=component_id,
            )
        )
        blocked = True

    for component in components:
        component_id = (
            component.get("component_manifest_entry_id")
            if isinstance(component, Mapping)
            else None
        )
        if isinstance(component_id, str) and component_id in duplicate_ids:
            continue

        component_ok, occurrences, accounting, anomalies = _interpret_component(
            component,
            acquisition_id,
            evidence_bindings,
        )
        all_occurrences.extend(occurrences)
        all_accounting.extend(accounting)
        all_anomalies.extend(anomalies)

        if not component_ok or any(
            item["mandatory_outcome"] == "QUALIFICATION_BLOCKED"
            for item in anomalies
        ):
            blocked = True

    if blocked:
        return _blocked_result(
            input_package,
            execution_context,
            "QUALIFICATION_BLOCKED_ANOMALY",
            tuple(all_anomalies),
            tuple(all_accounting),
        )

    candidate_sources = {
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
        )
        for item in all_occurrences
    }
    if len(candidate_sources) != len(all_occurrences):
        return _blocked_result(
            input_package,
            execution_context,
            "DUPLICATED_SOURCE_SLOT_CANDIDATE",
            tuple(all_anomalies),
            tuple(all_accounting),
        )

    accounting_sources = [
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
        )
        for item in all_accounting
    ]
    if len(set(accounting_sources)) != len(accounting_sources):
        return _blocked_result(
            input_package,
            execution_context,
            "DUPLICATED_SOURCE_ACCOUNTING",
            tuple(all_anomalies),
            tuple(all_accounting),
        )

    retained_sources = {
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
        )
        for item in all_accounting
        if item["disposition"] == "CANDIDATE_RETAINED"
    }
    if retained_sources != candidate_sources:
        return _blocked_result(
            input_package,
            execution_context,
            "SOURCE_TO_LOGICAL_ACCOUNTING_CONTRADICTION",
            tuple(all_anomalies),
            tuple(all_accounting),
        )

    return _build_terminal_result(
        input_package,
        execution_context,
        tuple(all_occurrences),
        tuple(all_accounting),
        tuple(all_anomalies),
    )


def qualify_native_bi5(
    input_package: Mapping[str, Any],
    *,
    execution_context: Mapping[str, Any],
) -> ImplementationQualificationResult:
    valid, reason = _validate_package_identity(input_package)
    if not valid:
        anomaly = _anomaly(
            "BI5-A12",
            "QUALIFICATION_BLOCKED",
            "ACQUISITION",
            acquisition_domain_id=(
                str(input_package.get("acquisition_domain_id", ""))
                if isinstance(input_package, Mapping)
                else ""
            ),
        )
        return _blocked_result(
            input_package,
            execution_context,
            reason,
            (anomaly,),
            (),
        )

    isolation = _isolation_evidence(execution_context)
    workspace_identity = isolation["workspace_isolation_identity"]
    if (
        not isinstance(workspace_identity, str)
        or not workspace_identity.strip()
        or frozenset(isolation["preseal_input_allowlist"]) != _REQUIRED_PRESEAL_INPUTS
        or frozenset(isolation["environment_variable_allowlist"])
        != _REQUIRED_ENVIRONMENT_VARIABLES
        or isolation["other_path_output_readable"] is not False
        or isolation["network_policy"] != "DENY"
        or isolation["ipc_policy"] != "DENY"
        or isolation["cache_policy"] != "PRIVATE_ONLY"
        or frozenset(isolation["runtime_read_set"]) != _REQUIRED_PRESEAL_INPUTS
    ):
        result = ImplementationQualificationResult(
            schema=RESULT_SCHEMA,
            implementation_id=IMPLEMENTATION_ID,
            implementation_version=IMPLEMENTATION_VERSION,
            implementation_manifest_digest=_manifest_digest(),
            input_determinant_digests=_copy_digests(
                input_package["determinant_digests"]
            ),
            materialized_acquisition_id=str(input_package["acquisition_domain_id"]),
            execution_status="ENVIRONMENT_BLOCKED",
            semantic_status="NOT_REACHED",
            freeze_status="NOT_REACHED",
            qualified_occurrences=None,
            source_accounting=None,
            anomaly_outcomes=None,
            terminal_evidence={
                "reason": "PRESEAL_EXECUTION_ENVIRONMENT_NOT_CLOSED",
            },
            isolation_evidence=isolation,
            result_seal="",
        )
        return _seal(result)

    return _qualify_components(input_package, execution_context)
