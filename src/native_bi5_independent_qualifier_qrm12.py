from __future__ import annotations

import copy
import hashlib
import json
import lzma
import re
import struct
import sys
from dataclasses import dataclass, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


IMPLEMENTATION_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_QRM12"
IMPLEMENTATION_VERSION = (
    "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_QRM12_V0_2_CANDIDATE"
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

_SOURCE_PATH = "src/native_bi5_independent_qualifier_qrm12.py"
_STAGES = ("D", "R", "M", "B", "A", "Q", "F", "O")
_F_STAGES = ("D", "R", "M", "B", "A", "Q", "F")
_BINDING_FIELDS = frozenset(
    ("stage", "normative_id", "normative_version", "immutable_reference", "integrity_digest")
)
_ALLOWED_PRESEAL = frozenset(
    ("common_immutable_input_package", "own_implementation_runtime", "python_stdlib")
)
_ALLOWED_ENV = frozenset(("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL"))
_EXECUTION = frozenset(("COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR"))
_SEMANTIC = frozenset(
    ("QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED", "NOT_REACHED")
)
_FREEZE = frozenset(("FROZEN", "NOT_CREATED", "NOT_REACHED"))
_RECORD_WIDTH = 20
_SLOT_STRUCT = struct.Struct(">IIIff")
_HOUR_MS = 3_600_000
_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$")
_CROSS_READ_KEY = "other_" + "path_output_readable"

_EVIDENCE_REFS = {
    "semantic_source_provenance_ref":
        "reports/data-qualification/iab/ib_semantic_source_provenance.json",
    "no_copy_declaration_ref":
        "reports/data-qualification/iab/ib_no_copy_declaration.json",
    "independent_stage_test_inventory_ref":
        "reports/data-qualification/iab/ib_independent_stage_test_inventory.json",
}


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


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _strict_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest_like(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _source_sha256() -> str:
    return _sha256_bytes(Path(__file__).read_bytes())


def build_implementation_manifest() -> dict[str, Any]:
    return {
        "implementation_id": IMPLEMENTATION_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "entrypoint": "qualify_native_bi5_v2",
        "source_files": [_SOURCE_PATH],
        "source_digests": {_SOURCE_PATH: _source_sha256()},
        "project_dependency_imports": [],
        "external_dependencies": {
            "python": ".".join(str(part) for part in sys.version_info[:3]),
            "compression_primitive": "python-stdlib-lzma",
            "binary_primitive": "python-stdlib-struct",
            "integrity_primitive": "python-stdlib-hashlib-sha256",
            "serialization_primitive": "python-stdlib-json-strict",
        },
        "semantic_stage_ownership": {
            "D_PREFLIGHT": "IndependentQualificationEngineV2.validate_common_package",
            "R_COMPATIBILITY": "IndependentQualificationEngineV2.validate_bindings",
            "B_ENVELOPE": "IndependentQualificationEngineV2.decode_component_envelope",
            "B_FRAMING": "IndependentQualificationEngineV2.scan_slots",
            "B_BINARY_DECODE": "IndependentQualificationEngineV2.decode_slot",
            "B_TIMESTAMP": "IndependentQualificationEngineV2.decode_slot",
            "B_PRICE": "IndependentQualificationEngineV2.decode_slot",
            "B_VOLUME": "IndependentQualificationEngineV2.binary32_value",
            "A_CLASSIFICATION": "IndependentQualificationEngineV2.classify_component",
            "M_OCCURRENCE": "IndependentQualificationEngineV2.decode_slot",
            "Q_MEMBERSHIP": "IndependentQualificationEngineV2.finalize_membership",
            "F_FREEZE": "IndependentQualificationEngineV2.private_freeze_builder_validator",
        },
        "independent_derivation_evidence_refs": dict(_EVIDENCE_REFS),
        "build_runtime_environment_identity": {
            "runtime": "CPython",
            "major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
    }


def _manifest_sha256() -> str:
    return _sha256_bytes(_strict_json_bytes(build_implementation_manifest()))


def _result_payload(result: ImplementationQualificationResultV2) -> dict[str, Any]:
    return {
        field.name: getattr(result, field.name)
        for field in fields(result)
        if field.name != "result_seal"
    }


def _seal_digest(result: ImplementationQualificationResultV2) -> str:
    return _sha256_bytes(_strict_json_bytes(_result_payload(result)))


def _seal_result(result: ImplementationQualificationResultV2) -> ImplementationQualificationResultV2:
    return replace(result, result_seal=_seal_digest(result))


def _safe_bindings(package: Any) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(package, Mapping):
        return ()
    raw = package.get("determinant_bindings")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes, bytearray)):
        return ()
    kept: list[Mapping[str, Any]] = []
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        candidate = copy.deepcopy(dict(item))
        try:
            _strict_json_bytes(candidate)
        except (TypeError, ValueError):
            continue
        kept.append(candidate)
    return tuple(kept)


def _safe_sequence(value: Any) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return ()
    return tuple(
        item if isinstance(item, str) else "__INVALID_NONSTRING__"
        for item in value
    )


def _isolation_snapshot(context: Any) -> dict[str, Any]:
    if not isinstance(context, Mapping):
        return {
            "workspace_isolation_identity": None,
            "preseal_input_allowlist": (),
            "network_policy": None,
            "ipc_policy": None,
            "environment_variable_allowlist": (),
            "cache_policy": None,
            _CROSS_READ_KEY: None,
            "runtime_read_set": (),
        }

    allow = _safe_sequence(context.get("preseal_input_allowlist", ()))
    env = _safe_sequence(context.get("environment_variable_allowlist", ()))
    workspace = context.get("workspace_isolation_identity")
    network = context.get("network_policy")
    ipc = context.get("ipc_policy")
    cache = context.get("cache_policy")
    cross_read = context.get(_CROSS_READ_KEY)
    reads = tuple(
        item
        for item in (
            "common_immutable_input_package",
            "own_implementation_runtime",
            "python_stdlib",
        )
        if item in allow
    )
    return {
        "workspace_isolation_identity": workspace if isinstance(workspace, str) else None,
        "preseal_input_allowlist": allow,
        "network_policy": network if isinstance(network, str) else None,
        "ipc_policy": ipc if isinstance(ipc, str) else None,
        "environment_variable_allowlist": env,
        "cache_policy": cache if isinstance(cache, str) else None,
        _CROSS_READ_KEY: cross_read if isinstance(cross_read, bool) else None,
        "runtime_read_set": reads,
    }


def _isolation_closed(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    workspace = value.get("workspace_isolation_identity")
    return (
        isinstance(workspace, str)
        and bool(workspace.strip())
        and frozenset(value.get("preseal_input_allowlist", ())) == _ALLOWED_PRESEAL
        and value.get("network_policy") == "DENY"
        and value.get("ipc_policy") == "DENY"
        and frozenset(value.get("environment_variable_allowlist", ())) == _ALLOWED_ENV
        and value.get("cache_policy") == "PRIVATE_ONLY"
        and value.get(_CROSS_READ_KEY) is False
        and frozenset(value.get("runtime_read_set", ())) == _ALLOWED_PRESEAL
    )


def _expected_binding(stage: str, declaration_version: str) -> tuple[str, str]:
    values = {
        "D": (D_ID, declaration_version),
        "R": (R_ID, R_VERSION),
        "M": (M_ID, M_VERSION),
        "B": (B_ID, B_VERSION),
        "A": (A_ID, A_VERSION),
        "Q": (Q_ID, Q_VERSION),
        "F": (F_ID, F_VERSION),
        "O": (O_ID, O_VERSION),
    }
    return values[stage]


def _validate_bindings(
    value: Any,
    declaration_version: str,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("determinant bindings missing")

    by_stage: dict[str, dict[str, Any]] = {}
    for raw in value:
        if not isinstance(raw, Mapping) or set(raw) != _BINDING_FIELDS:
            raise ValueError("determinant binding incomplete")
        item = copy.deepcopy(dict(raw))
        stage = item.get("stage")
        if stage not in _STAGES or stage in by_stage:
            raise ValueError("determinant stage invalid or repeated")
        if not all(
            _nonempty(item.get(key))
            for key in ("normative_id", "normative_version", "immutable_reference")
        ):
            raise ValueError("determinant identity invalid")
        if not _digest_like(item.get("integrity_digest")):
            raise ValueError("determinant digest invalid")
        expected_id, expected_version = _expected_binding(stage, declaration_version)
        if item["normative_id"] != expected_id or item["normative_version"] != expected_version:
            raise ValueError(f"{stage} determinant identity/version mismatch")
        _strict_json_bytes(item)
        by_stage[stage] = item

    if set(by_stage) != set(_STAGES):
        raise ValueError("determinant set is not exact")
    return tuple(by_stage[stage] for stage in _STAGES)


def _validate_freeze_bindings(
    value: Any,
    declaration_version: str,
) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError("freeze reconstruction bindings missing")
    by_stage: dict[str, dict[str, Any]] = {}
    for raw in value:
        if not isinstance(raw, Mapping) or set(raw) != _BINDING_FIELDS:
            raise ValueError("freeze reconstruction binding incomplete")
        item = copy.deepcopy(dict(raw))
        stage = item.get("stage")
        if stage not in _F_STAGES or stage in by_stage:
            raise ValueError("freeze reconstruction stage invalid or repeated")
        if not all(
            _nonempty(item.get(key))
            for key in ("normative_id", "normative_version", "immutable_reference")
        ):
            raise ValueError("freeze reconstruction identity invalid")
        if not _digest_like(item.get("integrity_digest")):
            raise ValueError("freeze reconstruction digest invalid")
        expected_id, expected_version = _expected_binding(stage, declaration_version)
        if item["normative_id"] != expected_id or item["normative_version"] != expected_version:
            raise ValueError(f"{stage} freeze determinant identity/version mismatch")
        _strict_json_bytes(item)
        by_stage[stage] = item
    if set(by_stage) != set(_F_STAGES):
        raise ValueError("freeze reconstruction set is not exact")
    return tuple(by_stage[stage] for stage in _F_STAGES)


def _validate_price(value: Any) -> None:
    if (
        not isinstance(value, Mapping)
        or set(value) != {"numerator", "denominator"}
        or isinstance(value.get("numerator"), bool)
        or not isinstance(value.get("numerator"), int)
        or not 0 <= value["numerator"] <= 0xFFFFFFFF
        or value.get("denominator") != 1000
    ):
        raise ValueError("price rational invalid")


def _validate_volume(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {"integer_coefficient", "exponent2"}:
        raise ValueError("binary32 normal form invalid")
    coefficient = value["integer_coefficient"]
    exponent = value["exponent2"]
    if (
        isinstance(coefficient, bool)
        or not isinstance(coefficient, int)
        or isinstance(exponent, bool)
        or not isinstance(exponent, int)
    ):
        raise ValueError("binary32 type invalid")
    if coefficient == 0:
        if exponent != 0:
            raise ValueError("binary32 zero normal form invalid")
        return
    if coefficient % 2 == 0:
        raise ValueError("binary32 coefficient not normalized")
    bits = abs(coefficient).bit_length()
    if bits > 24 or exponent < -149 or exponent + bits - 1 > 127:
        raise ValueError("binary32 value outside finite domain")


def _validate_payload(value: Any) -> None:
    if not isinstance(value, Mapping) or set(value) != {
        "market_timestamp_utc", "ask_price", "bid_price", "ask_volume", "bid_volume"
    }:
        raise ValueError("logical payload shape invalid")
    timestamp = value["market_timestamp_utc"]
    if not isinstance(timestamp, str) or _TIMESTAMP.fullmatch(timestamp) is None:
        raise ValueError("timestamp normal form invalid")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise ValueError("timestamp value invalid") from exc
    _validate_price(value["ask_price"])
    _validate_price(value["bid_price"])
    _validate_volume(value["ask_volume"])
    _validate_volume(value["bid_volume"])


def _artifact_digest(artifact: Mapping[str, Any]) -> str:
    unsigned = {
        key: value
        for key, value in artifact.items()
        if key != "artifact_integrity_digest"
    }
    return _sha256_bytes(_strict_json_bytes(unsigned))


def _validate_private_freeze(artifact: Any) -> Mapping[str, Any]:
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
        not _digest_like(artifact.get("artifact_integrity_digest"))
        or artifact["artifact_integrity_digest"] != _artifact_digest(artifact)
    ):
        raise ValueError("freeze artifact digest invalid")

    universe = artifact.get("qualified_universe")
    if not isinstance(universe, Mapping):
        raise ValueError("qualified universe missing")
    acquisition_id = universe.get("acquisition_domain_id")
    declaration_version = universe.get("acquisition_declaration_version")
    if not _nonempty(acquisition_id) or not _nonempty(declaration_version):
        raise ValueError("qualified universe identity invalid")

    _validate_freeze_bindings(universe.get("reconstruction_tuple"), declaration_version)

    parameters = universe.get("qualification_parameters")
    completeness = universe.get("completeness_evidence")
    components = universe.get("components")
    accounting = universe.get("source_accounting")
    anomalies = universe.get("anomaly_outcomes")
    retained = universe.get("retained_occurrences")
    candidates = universe.get("b_candidate_occurrences")

    if not isinstance(parameters, Mapping) or not parameters:
        raise ValueError("qualification parameters missing")
    _strict_json_bytes(dict(parameters))
    if (
        not isinstance(completeness, Mapping)
        or not _nonempty(completeness.get("immutable_reference"))
        or not _digest_like(completeness.get("integrity_digest"))
    ):
        raise ValueError("completeness evidence invalid")
    _strict_json_bytes(dict(completeness))
    if not all(
        isinstance(rows, Sequence) and not isinstance(rows, (str, bytes, bytearray))
        for rows in (components, accounting, anomalies, retained, candidates)
    ):
        raise ValueError("freeze relation malformed")
    if not components:
        raise ValueError("qualified component universe empty")

    component_counts: dict[str, int] = {}
    component_hours: dict[str, datetime] = {}
    for component in components:
        if not isinstance(component, Mapping):
            raise ValueError("freeze component malformed")
        component_id = component.get("component_manifest_entry_id")
        count = component.get("complete_slot_count")
        if (
            not _nonempty(component_id)
            or component_id in component_counts
            or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
            or component.get("instrument_source_identity") != "DUKASCOPY/USATECHIDXUSD"
            or not _nonempty(component.get("immutable_payload_reference"))
            or not _digest_like(component.get("payload_integrity_reference"))
            or component.get("materialization_status") != "MATERIALIZED"
            or isinstance(count, bool)
            or not isinstance(count, int)
            or count <= 0
            or component.get("terminal_fragment") is not None
        ):
            raise ValueError("freeze component invalid")
        try:
            hour = datetime.strptime(component["declared_hour_bucket_utc"], "%Y-%m-%dT%H:%M:%SZ")
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("freeze component hour invalid") from exc
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
            raise ValueError("source accounting shape invalid")
        component_id = item.get("component_manifest_entry_id")
        slot = item.get("component_local_slot_index")
        if (
            not _nonempty(component_id)
            or isinstance(slot, bool)
            or not isinstance(slot, int)
            or slot < 0
        ):
            raise ValueError("source accounting source invalid")
        source = (component_id, slot)
        if source not in expected_sources or source in accounting_map:
            raise ValueError("source accounting relation invalid")
        disposition = item.get("disposition")
        if disposition == "CANDIDATE_RETAINED":
            if item.get("anomaly_class_id") is not None:
                raise ValueError("retained source carries anomaly")
        elif disposition == "REJECT_RECORD":
            if item.get("anomaly_class_id") not in ("BI5-A09", "BI5-A10"):
                raise ValueError("rejected source anomaly invalid")
        else:
            raise ValueError("source accounting disposition invalid")
        accounting_map[source] = item

    if set(accounting_map) != expected_sources:
        raise ValueError("source accounting incomplete")

    def occurrence_relation(rows: Sequence[Any]) -> dict[tuple[str, int], Any]:
        relation: dict[tuple[str, int], Any] = {}
        for occurrence in rows:
            if (
                not isinstance(occurrence, Mapping)
                or not set(occurrence).issubset(
                    {"logical_payload", "source_witness", "source_provenance"}
                )
            ):
                raise ValueError("occurrence malformed")
            witness = occurrence.get("source_witness")
            if not isinstance(witness, Mapping) or set(witness) != {
                "component_manifest_entry_id", "component_local_slot_index"
            }:
                raise ValueError("source witness malformed")
            component_id = witness.get("component_manifest_entry_id")
            slot = witness.get("component_local_slot_index")
            if (
                not _nonempty(component_id)
                or isinstance(slot, bool)
                or not isinstance(slot, int)
                or slot < 0
            ):
                raise ValueError("source witness invalid")
            source = (component_id, slot)
            if source not in expected_sources or source in relation:
                raise ValueError("occurrence source relation invalid")
            _validate_payload(occurrence.get("logical_payload"))
            timestamp = datetime.strptime(
                occurrence["logical_payload"]["market_timestamp_utc"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )
            hour = component_hours[component_id]
            if not (hour <= timestamp < hour + timedelta(hours=1)):
                raise ValueError("occurrence timestamp outside declared hour")
            relation[source] = copy.deepcopy(occurrence["logical_payload"])
        return relation

    retained_relation = occurrence_relation(retained)
    candidate_relation = occurrence_relation(candidates)
    if retained_relation != candidate_relation:
        raise ValueError("B/Q occurrence relation mismatch")

    retained_sources = {
        source
        for source, item in accounting_map.items()
        if item["disposition"] == "CANDIDATE_RETAINED"
    }
    rejected_sources = expected_sources - retained_sources
    if set(retained_relation) != retained_sources:
        raise ValueError("retained relation/accounting mismatch")

    anomaly_relation: set[tuple[str, int, str]] = set()
    for anomaly in anomalies:
        if (
            not isinstance(anomaly, Mapping)
            or anomaly.get("anomaly_matrix_version") != A_VERSION
            or anomaly.get("mandatory_outcome") != "REJECT_RECORD"
            or anomaly.get("acquisition_fatal") is not False
            or anomaly.get("anomaly_class_id") not in ("BI5-A09", "BI5-A10")
        ):
            raise ValueError("local anomaly invalid")
        bindings = anomaly.get("qualification_evidence_bindings")
        if not isinstance(bindings, Sequence) or isinstance(bindings, (str, bytes, bytearray)) or len(bindings):
            raise ValueError("local anomaly evidence invalid")
        target = anomaly.get("target")
        if not isinstance(target, Mapping) or set(target) != {
            "target_scope", "component_manifest_entry_id", "component_local_slot_index"
        } or target.get("target_scope") != "COMPLETE_SLOT":
            raise ValueError("local anomaly target invalid")
        component_id = target.get("component_manifest_entry_id")
        slot = target.get("component_local_slot_index")
        if (
            not _nonempty(component_id)
            or isinstance(slot, bool)
            or not isinstance(slot, int)
            or slot < 0
        ):
            raise ValueError("local anomaly source invalid")
        row = (component_id, slot, anomaly["anomaly_class_id"])
        if row in anomaly_relation:
            raise ValueError("duplicate local anomaly")
        anomaly_relation.add(row)

    expected_anomalies = {
        (source[0], source[1], accounting_map[source]["anomaly_class_id"])
        for source in rejected_sources
    }
    if anomaly_relation != expected_anomalies:
        raise ValueError("anomaly/accounting mismatch")

    count = artifact.get("qualified_occurrence_count")
    if isinstance(count, bool) or not isinstance(count, int) or count != len(retained):
        raise ValueError("qualified occurrence count mismatch")
    return artifact


def _validate_result_shape(result: ImplementationQualificationResultV2) -> None:
    if not isinstance(result, ImplementationQualificationResultV2):
        raise TypeError("unexpected result type")
    if result.schema != RESULT_SCHEMA:
        raise ValueError("unexpected result schema")
    if result.implementation_id != IMPLEMENTATION_ID:
        raise ValueError("unexpected implementation id")
    if result.implementation_version != IMPLEMENTATION_VERSION:
        raise ValueError("unexpected implementation version")
    if result.implementation_manifest_digest != _manifest_sha256():
        raise ValueError("manifest digest mismatch")
    if result.execution_status not in _EXECUTION:
        raise ValueError("execution status invalid")
    if result.semantic_status not in _SEMANTIC:
        raise ValueError("semantic status invalid")
    if result.freeze_status not in _FREEZE:
        raise ValueError("freeze status invalid")

    isolation_closed = _isolation_closed(result.isolation_evidence)
    if result.execution_status != "COMPLETED":
        if (
            result.semantic_status != "NOT_REACHED"
            or result.freeze_status != "NOT_REACHED"
            or result.bound_f_artifact is not None
            or result.terminal_evidence is None
        ):
            raise ValueError("non-completed execution contradiction")
        if result.execution_status == "ENVIRONMENT_BLOCKED":
            if isolation_closed:
                raise ValueError("environment-blocked result claims closed environment")
        elif not isolation_closed:
            raise ValueError("implementation error lacks closed isolation evidence")
        return

    if not isolation_closed:
        raise ValueError("completed result lacks closed isolation evidence")

    if result.semantic_status == "QUALIFIED":
        if (
            result.freeze_status != "FROZEN"
            or result.bound_f_artifact is None
            or result.terminal_evidence is not None
        ):
            raise ValueError("qualified result contradiction")
        artifact = _validate_private_freeze(result.bound_f_artifact)
        universe = artifact["qualified_universe"]
        if result.materialized_acquisition_id != universe["acquisition_domain_id"]:
            raise ValueError("result/F acquisition mismatch")
        result_bindings = _validate_bindings(
            result.input_determinant_bindings,
            universe["acquisition_declaration_version"],
        )
        by_result = {item["stage"]: item for item in result_bindings}
        by_freeze = {
            item["stage"]: item
            for item in _validate_freeze_bindings(
                universe["reconstruction_tuple"],
                universe["acquisition_declaration_version"],
            )
        }
        for stage in _F_STAGES:
            if by_result[stage] != by_freeze[stage]:
                raise ValueError("result/F determinant mismatch")
        return

    if result.semantic_status in ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"):
        if (
            result.freeze_status != "NOT_CREATED"
            or result.bound_f_artifact is not None
            or result.terminal_evidence is None
        ):
            raise ValueError("non-qualified semantic result contradiction")
        return

    raise ValueError("completed execution cannot be NOT_REACHED")


def is_sealed_implementation_result_v2(value: object) -> bool:
    if not isinstance(value, ImplementationQualificationResultV2):
        return False
    try:
        _validate_result_shape(value)
        return bool(value.result_seal) and value.result_seal == _seal_digest(value)
    except (TypeError, ValueError):
        return False


def validate_implementation_result_v2(
    result: ImplementationQualificationResultV2,
) -> ImplementationQualificationResultV2:
    _validate_result_shape(result)
    if not result.result_seal or result.result_seal != _seal_digest(result):
        raise ValueError("result seal mismatch")
    return result


class IndependentQualificationEngineV2:
    def __init__(self, package: Any, context: Any) -> None:
        self.package = package
        self.context = context
        self.acquisition_id = ""
        self.declaration_version = ""
        self.bindings: tuple[Mapping[str, Any], ...] = ()
        self.parameters: Mapping[str, Any] = {}
        self.completeness: Mapping[str, Any] = {}
        self.components: tuple[Any, ...] = ()
        self.snapshots: list[Mapping[str, Any]] = []
        self.occurrences: list[Mapping[str, Any]] = []
        self.accounting: list[Mapping[str, Any]] = []
        self.anomalies: list[Mapping[str, Any]] = []
        self.blocked = False

    @staticmethod
    def binary32_value(raw: bytes) -> dict[str, int] | None:
        bits = int.from_bytes(raw, "big")
        exponent_field = (bits >> 23) & 0xFF
        fraction = bits & 0x7FFFFF
        negative = bool(bits >> 31)

        if exponent_field == 0xFF:
            return None
        if exponent_field == 0 and fraction == 0:
            return {"integer_coefficient": 0, "exponent2": 0}
        if exponent_field == 0:
            coefficient = fraction
            exponent2 = -149
        else:
            coefficient = (1 << 23) | fraction
            exponent2 = exponent_field - 150
        while coefficient and coefficient % 2 == 0:
            coefficient //= 2
            exponent2 += 1
        if negative:
            coefficient = -coefficient
        return {"integer_coefficient": coefficient, "exponent2": exponent2}

    @staticmethod
    def parse_hour(value: Any) -> datetime | None:
        if not isinstance(value, str):
            return None
        try:
            parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            return None
        return parsed.replace(tzinfo=timezone.utc)

    @staticmethod
    def format_timestamp(hour: datetime, offset_ms: int) -> str:
        value = hour + timedelta(milliseconds=offset_ms)
        return value.strftime("%Y-%m-%dT%H:%M:%S.") + f"{value.microsecond // 1000:03d}Z"

    @staticmethod
    def decode_component_envelope(payload: bytes) -> bytes | None:
        try:
            decoder = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
            decoded = decoder.decompress(payload)
        except lzma.LZMAError:
            return None
        if not decoder.eof or decoder.unused_data:
            return None
        return decoded

    @staticmethod
    def anomaly(
        class_id: str,
        target_scope: str,
        outcome: str,
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

    def isolation_snapshot(self) -> dict[str, Any]:
        return _isolation_snapshot(self.context)

    def environment_is_closed(self) -> bool:
        return _isolation_closed(self.isolation_snapshot())

    def validate_common_package(self) -> tuple[bool, str]:
        if not isinstance(self.package, Mapping):
            return False, "INPUT_PACKAGE_NOT_MAPPING"
        if self.package.get("schema") != INPUT_SCHEMA:
            return False, "INPUT_SCHEMA_MISMATCH"

        acquisition = self.package.get("acquisition_domain_id")
        declaration = self.package.get("acquisition_declaration_version")
        if not _nonempty(acquisition):
            return False, "MISSING_ACQUISITION_DOMAIN_ID"
        if not _nonempty(declaration):
            return False, "MISSING_ACQUISITION_DECLARATION_VERSION"
        self.acquisition_id = acquisition
        self.declaration_version = declaration

        try:
            self.bindings = _validate_bindings(
                self.package.get("determinant_bindings"),
                declaration,
            )
        except (TypeError, ValueError) as exc:
            return False, f"INVALID_DETERMINANT_BINDINGS:{exc}"

        parameters = self.package.get("qualification_parameters")
        if not isinstance(parameters, Mapping) or not parameters:
            return False, "QUALIFICATION_PARAMETERS_MISSING"
        try:
            _strict_json_bytes(dict(parameters))
        except (TypeError, ValueError):
            return False, "QUALIFICATION_PARAMETERS_NOT_STRICT_JSON"
        self.parameters = copy.deepcopy(dict(parameters))

        completeness = self.package.get("d_completeness_evidence")
        if (
            not isinstance(completeness, Mapping)
            or not _nonempty(completeness.get("immutable_reference"))
            or not _digest_like(completeness.get("integrity_digest"))
        ):
            return False, "D_COMPLETENESS_EVIDENCE_INVALID"
        try:
            _strict_json_bytes(dict(completeness))
        except (TypeError, ValueError):
            return False, "D_COMPLETENESS_EVIDENCE_NOT_STRICT_JSON"
        self.completeness = copy.deepcopy(dict(completeness))

        components = self.package.get("components")
        if not isinstance(components, Sequence) or isinstance(
            components, (str, bytes, bytearray)
        ) or not components:
            return False, "COMPONENT_MANIFEST_MISSING"
        self.components = tuple(copy.deepcopy(list(components)))

        evidence = self.package.get("qualification_evidence_bindings", ())
        if not isinstance(evidence, Sequence) or isinstance(evidence, (str, bytes, bytearray)):
            return False, "QUALIFICATION_EVIDENCE_BINDINGS_INVALID"
        return True, "OK"

    def decode_slot(
        self,
        component_id: str,
        slot_index: int,
        raw: bytes,
        hour: datetime,
    ) -> None:
        offset_ms, ask_raw, bid_raw, _ask_float, _bid_float = _SLOT_STRUCT.unpack(raw)

        if offset_ms >= _HOUR_MS:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A09", "COMPLETE_SLOT", "REJECT_RECORD",
                    component_id=component_id, slot_index=slot_index,
                )
            )
            self.accounting.append(
                {
                    "component_manifest_entry_id": component_id,
                    "component_local_slot_index": slot_index,
                    "disposition": "REJECT_RECORD",
                    "anomaly_class_id": "BI5-A09",
                }
            )
            return

        ask_volume = self.binary32_value(raw[12:16])
        bid_volume = self.binary32_value(raw[16:20])
        if ask_volume is None or bid_volume is None:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A10", "COMPLETE_SLOT", "REJECT_RECORD",
                    component_id=component_id, slot_index=slot_index,
                )
            )
            self.accounting.append(
                {
                    "component_manifest_entry_id": component_id,
                    "component_local_slot_index": slot_index,
                    "disposition": "REJECT_RECORD",
                    "anomaly_class_id": "BI5-A10",
                }
            )
            return

        self.occurrences.append(
            {
                "logical_payload": {
                    "market_timestamp_utc": self.format_timestamp(hour, offset_ms),
                    "ask_price": {"numerator": ask_raw, "denominator": 1000},
                    "bid_price": {"numerator": bid_raw, "denominator": 1000},
                    "ask_volume": ask_volume,
                    "bid_volume": bid_volume,
                },
                "source_witness": {
                    "component_manifest_entry_id": component_id,
                    "component_local_slot_index": slot_index,
                },
            }
        )
        self.accounting.append(
            {
                "component_manifest_entry_id": component_id,
                "component_local_slot_index": slot_index,
                "disposition": "CANDIDATE_RETAINED",
                "anomaly_class_id": None,
            }
        )

    def scan_slots(
        self,
        component_id: str,
        decoded: bytes,
        hour: datetime,
    ) -> tuple[int, dict[str, int] | None]:
        complete, remainder = divmod(len(decoded), _RECORD_WIDTH)
        for slot_index in range(complete):
            start = slot_index * _RECORD_WIDTH
            self.decode_slot(
                component_id,
                slot_index,
                decoded[start : start + _RECORD_WIDTH],
                hour,
            )
        if remainder:
            fragment = {
                "terminal_fragment_start_offset": complete * _RECORD_WIDTH,
                "terminal_fragment_length": remainder,
            }
            self.anomalies.append(
                self.anomaly(
                    "BI5-A07", "TERMINAL_FRAGMENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                    fragment_start=fragment["terminal_fragment_start_offset"],
                    fragment_length=fragment["terminal_fragment_length"],
                )
            )
            self.blocked = True
            return complete, fragment
        return complete, None

    def classify_component(self, component: Any) -> None:
        if not isinstance(component, Mapping):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11", "ACQUISITION", "QUALIFICATION_BLOCKED",
                    acquisition_id=self.acquisition_id,
                )
            )
            self.blocked = True
            return

        component_id = component.get("component_manifest_entry_id")
        if not _nonempty(component_id):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11", "ACQUISITION", "QUALIFICATION_BLOCKED",
                    acquisition_id=self.acquisition_id,
                )
            )
            self.blocked = True
            return

        if "complete_slot_count" in component or "terminal_fragment" in component:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A12", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        if (
            component.get("instrument_id") != "USATECHIDXUSD"
            or component.get("instrument_source_identity") != "DUKASCOPY/USATECHIDXUSD"
            or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
            or not _nonempty(component.get("immutable_payload_reference"))
            or not _digest_like(component.get("payload_integrity_reference"))
        ):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A12", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        hour = self.parse_hour(component.get("declared_hour_bucket_utc"))
        if hour is None:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A04", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        payload = component.get("compressed_payload_bytes")
        declared_sha = component.get("payload_sha256")
        if (
            not isinstance(payload, bytes)
            or not _digest_like(declared_sha)
            or declared_sha != component["payload_integrity_reference"]
            or _sha256_bytes(payload) != declared_sha
        ):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        decoded = self.decode_component_envelope(payload)
        if decoded is None:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A05", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return
        if not decoded:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A06", "COMPONENT", "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        complete, fragment = self.scan_slots(component_id, decoded, hour)
        self.snapshots.append(
            {
                "component_manifest_entry_id": component_id,
                "declared_role": component["declared_role"],
                "instrument_source_identity": component["instrument_source_identity"],
                "declared_hour_bucket_utc": component["declared_hour_bucket_utc"],
                "immutable_payload_reference": component["immutable_payload_reference"],
                "payload_integrity_reference": component["payload_integrity_reference"],
                "materialization_status": "MATERIALIZED",
                "complete_slot_count": complete,
                "terminal_fragment": copy.deepcopy(fragment),
            }
        )

    def finalize_membership(self) -> tuple[bool, str]:
        if self.blocked:
            return False, "QUALIFICATION_BLOCKED_ANOMALY"

        occurrence_sources = [
            (
                item["source_witness"]["component_manifest_entry_id"],
                item["source_witness"]["component_local_slot_index"],
            )
            for item in self.occurrences
        ]
        accounting_sources = [
            (
                item["component_manifest_entry_id"],
                item["component_local_slot_index"],
            )
            for item in self.accounting
        ]
        if len(set(occurrence_sources)) != len(occurrence_sources):
            return False, "DUPLICATED_CANDIDATE_SOURCE"
        if len(set(accounting_sources)) != len(accounting_sources):
            return False, "DUPLICATED_ACCOUNTING_SOURCE"

        retained = {
            (
                item["component_manifest_entry_id"],
                item["component_local_slot_index"],
            )
            for item in self.accounting
            if item["disposition"] == "CANDIDATE_RETAINED"
        }
        if retained != set(occurrence_sources):
            return False, "SOURCE_TO_LOGICAL_RELATION_MISMATCH"
        return True, "QUALIFIED"

    def private_freeze_builder_validator(self) -> Mapping[str, Any]:
        by_stage = {item["stage"]: item for item in self.bindings}
        universe = {
            "acquisition_domain_id": self.acquisition_id,
            "acquisition_declaration_version": self.declaration_version,
            "qualification_parameters": copy.deepcopy(dict(self.parameters)),
            "completeness_evidence": copy.deepcopy(dict(self.completeness)),
            "reconstruction_tuple": [
                copy.deepcopy(by_stage[stage]) for stage in _F_STAGES
            ],
            "components": copy.deepcopy(self.snapshots),
            "source_accounting": copy.deepcopy(self.accounting),
            "anomaly_outcomes": copy.deepcopy(self.anomalies),
            "retained_occurrences": copy.deepcopy(self.occurrences),
            "b_candidate_occurrences": copy.deepcopy(self.occurrences),
        }
        artifact: dict[str, Any] = {
            "schema": F_ARTIFACT_SCHEMA,
            "freeze_contract_id": F_ID,
            "freeze_contract_version": F_VERSION,
            "artifact_class": "QUALIFIED_UNIVERSE_FREEZE",
            "freeze_state": "FROZEN",
            "qualification_outcome": "QUALIFIED",
            "qualified_universe": universe,
            "qualified_occurrence_count": len(self.occurrences),
            "terminal_evidence": None,
        }
        artifact["artifact_integrity_digest"] = _artifact_digest(artifact)
        return _validate_private_freeze(artifact)

    def make_result(
        self,
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
            implementation_manifest_digest=_manifest_sha256(),
            input_determinant_bindings=(
                copy.deepcopy(bindings)
                if bindings is not None
                else _safe_bindings(self.package)
            ),
            materialized_acquisition_id=self.acquisition_id,
            execution_status=execution_status,
            semantic_status=semantic_status,
            freeze_status=freeze_status,
            bound_f_artifact=copy.deepcopy(bound_f_artifact),
            terminal_evidence=copy.deepcopy(terminal_evidence),
            isolation_evidence=self.isolation_snapshot(),
            result_seal="",
        )
        return _seal_result(result)

    def blocked_result(self, reason: str) -> ImplementationQualificationResultV2:
        return self.make_result(
            execution_status="COMPLETED",
            semantic_status="QUALIFICATION_BLOCKED",
            freeze_status="NOT_CREATED",
            bound_f_artifact=None,
            terminal_evidence={
                "reason": reason,
                "anomaly_outcomes": copy.deepcopy(self.anomalies),
            },
            bindings=self.bindings if self.bindings else None,
        )

    def environment_blocked_result(self) -> ImplementationQualificationResultV2:
        return self.make_result(
            execution_status="ENVIRONMENT_BLOCKED",
            semantic_status="NOT_REACHED",
            freeze_status="NOT_REACHED",
            bound_f_artifact=None,
            terminal_evidence={"reason": "PRESEAL_EXECUTION_ENVIRONMENT_NOT_CLOSED"},
            bindings=self.bindings if self.bindings else None,
        )

    def implementation_error_result(self, exc: BaseException) -> ImplementationQualificationResultV2:
        return self.make_result(
            execution_status="IMPLEMENTATION_ERROR",
            semantic_status="NOT_REACHED",
            freeze_status="NOT_REACHED",
            bound_f_artifact=None,
            terminal_evidence={
                "reason": f"INDEPENDENT_PATH_IMPLEMENTATION_ERROR:{type(exc).__name__}"
            },
            bindings=self.bindings if self.bindings else None,
        )

    def run(self) -> ImplementationQualificationResultV2:
        if not self.environment_is_closed():
            return self.environment_blocked_result()

        valid, reason = self.validate_common_package()
        if not valid:
            return self.blocked_result(reason)

        counts: dict[str, int] = {}
        for component in self.components:
            if isinstance(component, Mapping):
                component_id = component.get("component_manifest_entry_id")
                if _nonempty(component_id):
                    counts[component_id] = counts.get(component_id, 0) + 1
        duplicates = {key for key, count in counts.items() if count > 1}
        if duplicates:
            for component_id in sorted(duplicates):
                self.anomalies.append(
                    self.anomaly(
                        "BI5-A03", "COMPONENT", "QUALIFICATION_BLOCKED",
                        component_id=component_id,
                    )
                )
            return self.blocked_result("DUPLICATED_COMPONENT_IDENTITY")

        for component in self.components:
            self.classify_component(component)

        qualified, reason = self.finalize_membership()
        if not qualified:
            return self.blocked_result(reason)

        try:
            artifact = self.private_freeze_builder_validator()
            result = self.make_result(
                execution_status="COMPLETED",
                semantic_status="QUALIFIED",
                freeze_status="FROZEN",
                bound_f_artifact=artifact,
                terminal_evidence=None,
                bindings=self.bindings,
            )
            return validate_implementation_result_v2(result)
        except (TypeError, ValueError, OverflowError, struct.error, lzma.LZMAError) as exc:
            return self.implementation_error_result(exc)


def qualify_native_bi5_v2(
    input_package: Mapping[str, Any],
    *,
    execution_context: Mapping[str, Any],
) -> ImplementationQualificationResultV2:
    engine = IndependentQualificationEngineV2(input_package, execution_context)
    return engine.run()
