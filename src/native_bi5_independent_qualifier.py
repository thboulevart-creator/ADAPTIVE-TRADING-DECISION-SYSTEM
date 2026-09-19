from __future__ import annotations

import hashlib
import json
import lzma
import struct
import sys
from dataclasses import dataclass, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping


IMPLEMENTATION_ID = "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER"
IMPLEMENTATION_VERSION = (
    "I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_V0_1_CANDIDATE"
)
RESULT_SCHEMA = "NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_1_CANDIDATE"

_SOURCE_PATH = "src/native_bi5_independent_qualifier.py"

_R_ID = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS"
_R_VERSION = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE"
_M_VERSION = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE"
_B_ID = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
_B_VERSION = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
_A_ID = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
_A_VERSION = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
_Q_ID = "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP"
_Q_VERSION = (
    "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE"
)
_F_ID = "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE"
_F_VERSION = (
    "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE"
)
_O_ID = "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR"
_O_VERSION = (
    "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE"
)

_EVIDENCE_REFS = {
    "semantic_source_provenance_ref":
        "reports/data-qualification/iab/ib_semantic_source_provenance.json",
    "no_copy_declaration_ref":
        "reports/data-qualification/iab/ib_no_copy_declaration.json",
    "independent_stage_test_inventory_ref":
        "reports/data-qualification/iab/ib_independent_stage_test_inventory.json",
}

_REQUIRED_DETERMINANTS = frozenset(("D", "R", "M", "B", "A", "Q", "F", "O"))
_ALLOWED_PRESEAL = frozenset(
    ("common_immutable_input_package", "own_implementation_runtime", "python_stdlib")
)
_ALLOWED_ENV = frozenset(("PYTHONHASHSEED", "TZ", "LANG", "LC_ALL"))

_VALID_EXECUTION = frozenset(
    ("COMPLETED", "ENVIRONMENT_BLOCKED", "IMPLEMENTATION_ERROR")
)
_VALID_SEMANTIC = frozenset(
    ("QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED", "NOT_REACHED")
)
_VALID_FREEZE = frozenset(("FROZEN", "NOT_CREATED", "NOT_REACHED"))

_RECORD_WIDTH = 20
_SLOT_STRUCT = struct.Struct(">IIIff")
_HOUR_MS = 3_600_000


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


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _source_sha256() -> str:
    return _sha256_bytes(Path(__file__).read_bytes())


def build_implementation_manifest() -> dict[str, Any]:
    return {
        "implementation_id": IMPLEMENTATION_ID,
        "implementation_version": IMPLEMENTATION_VERSION,
        "entrypoint": "qualify_native_bi5",
        "source_files": [_SOURCE_PATH],
        "source_digests": {_SOURCE_PATH: _source_sha256()},
        "project_dependencies": [],
        "external_dependencies": {
            "python": ".".join(str(part) for part in sys.version_info[:3]),
            "lzma": "python-stdlib",
            "struct": "python-stdlib",
            "hashlib": "python-stdlib",
        },
        "semantic_stage_ownership": {
            "D_PREFLIGHT": "IndependentQualificationEngine.check_normative_package",
            "R_COMPATIBILITY": "IndependentQualificationEngine.check_normative_package",
            "B_ENVELOPE": "IndependentQualificationEngine.decode_component_envelope",
            "B_FRAMING": "IndependentQualificationEngine.scan_component_slots",
            "B_BINARY_DECODE": "IndependentQualificationEngine.decode_slot",
            "B_TIMESTAMP": "IndependentQualificationEngine.decode_slot",
            "B_PRICE": "IndependentQualificationEngine.decode_slot",
            "B_VOLUME": "IndependentQualificationEngine.binary32_value",
            "A_CLASSIFICATION": "IndependentQualificationEngine.classify_component",
            "M_OCCURRENCE": "IndependentQualificationEngine.decode_slot",
            "Q_MEMBERSHIP": "IndependentQualificationEngine.finalize_membership",
            "F_FREEZE": "IndependentQualificationEngine.make_terminal_result",
        },
        "independent_derivation_evidence_refs": dict(_EVIDENCE_REFS),
        "build_runtime_environment_identity": {
            "runtime": "CPython",
            "major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
    }


def _manifest_sha256() -> str:
    return _sha256_bytes(_json_bytes(build_implementation_manifest()))


def _canonical_result_payload(result: ImplementationQualificationResult) -> dict[str, Any]:
    return {
        item.name: getattr(result, item.name)
        for item in fields(result)
        if item.name != "result_seal"
    }


def _seal_digest(result: ImplementationQualificationResult) -> str:
    return _sha256_bytes(_json_bytes(_canonical_result_payload(result)))


def _with_seal(result: ImplementationQualificationResult) -> ImplementationQualificationResult:
    return replace(result, result_seal=_seal_digest(result))


def _validate_shape(result: ImplementationQualificationResult) -> None:
    if not isinstance(result, ImplementationQualificationResult):
        raise TypeError("unexpected result type")
    if result.schema != RESULT_SCHEMA:
        raise ValueError("unexpected result schema")
    if result.implementation_id != IMPLEMENTATION_ID:
        raise ValueError("unexpected implementation id")
    if result.implementation_version != IMPLEMENTATION_VERSION:
        raise ValueError("unexpected implementation version")
    if result.implementation_manifest_digest != _manifest_sha256():
        raise ValueError("implementation manifest digest mismatch")
    if not isinstance(result.input_determinant_digests, Mapping):
        raise ValueError("input determinant bindings must be a mapping")
    determinant_keys = set(result.input_determinant_digests)
    if not determinant_keys.issubset(_REQUIRED_DETERMINANTS):
        raise ValueError("unknown input determinant binding")
    for digest in result.input_determinant_digests.values():
        if not isinstance(digest, str) or len(digest) != 64:
            raise ValueError("invalid input determinant digest")
        try:
            int(digest, 16)
        except ValueError as exc:
            raise ValueError("invalid input determinant digest") from exc
    if result.execution_status not in _VALID_EXECUTION:
        raise ValueError("invalid execution status")
    if result.semantic_status not in _VALID_SEMANTIC:
        raise ValueError("invalid semantic status")
    if result.freeze_status not in _VALID_FREEZE:
        raise ValueError("invalid freeze status")

    qualified = (
        result.execution_status == "COMPLETED"
        and result.semantic_status == "QUALIFIED"
        and result.freeze_status == "FROZEN"
    )
    if qualified and determinant_keys != _REQUIRED_DETERMINANTS:
        raise ValueError("qualified result requires complete determinant bindings")

    if result.execution_status != "COMPLETED":
        if result.semantic_status != "NOT_REACHED":
            raise ValueError("non-completed execution reached semantic state")
        if result.freeze_status != "NOT_REACHED":
            raise ValueError("non-completed execution reached freeze state")
    elif result.semantic_status == "QUALIFIED":
        if result.freeze_status != "FROZEN":
            raise ValueError("qualified result is not frozen")
    elif result.semantic_status in ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"):
        if result.freeze_status != "NOT_CREATED":
            raise ValueError("blocked/rejected result created freeze")
    else:
        raise ValueError("completed execution cannot be NOT_REACHED")

    if result.freeze_status == "FROZEN" and result.semantic_status != "QUALIFIED":
        raise ValueError("freeze requires qualification")

    if qualified:
        if result.qualified_occurrences is None or result.source_accounting is None:
            raise ValueError("qualified result lacks complete semantic universe")
    else:
        if result.qualified_occurrences is not None:
            raise ValueError("non-qualified result exposes qualified occurrences")
        if result.source_accounting is not None:
            raise ValueError("non-qualified result exposes normative source accounting")


def is_sealed_implementation_result(value: object) -> bool:
    if not isinstance(value, ImplementationQualificationResult):
        return False
    try:
        _validate_shape(value)
        return bool(value.result_seal) and value.result_seal == _seal_digest(value)
    except (TypeError, ValueError):
        return False


def validate_implementation_result(
    result: ImplementationQualificationResult,
) -> ImplementationQualificationResult:
    _validate_shape(result)
    if not result.result_seal or result.result_seal != _seal_digest(result):
        raise ValueError("invalid result seal")
    return result


class IndependentQualificationEngine:
    def __init__(
        self,
        input_package: Mapping[str, Any],
        execution_context: Mapping[str, Any],
    ) -> None:
        self.package = input_package
        self.context = execution_context if isinstance(execution_context, Mapping) else {}
        self.acquisition_id = ""
        self.determinants: dict[str, str] = {}
        self.occurrences: list[Mapping[str, Any]] = []
        self.accounting: list[Mapping[str, Any]] = []
        self.anomalies: list[Mapping[str, Any]] = []
        self.blocked = False

    @staticmethod
    def digest_like(value: Any) -> bool:
        if not isinstance(value, str) or len(value) != 64:
            return False
        try:
            int(value, 16)
        except ValueError:
            return False
        return True

    @staticmethod
    def binary32_value(raw: bytes) -> tuple[int, int] | None:
        bits = int.from_bytes(raw, "big")
        exponent_field = (bits >> 23) & 0xFF
        fraction = bits & 0x7FFFFF
        negative = bool(bits >> 31)

        if exponent_field == 0xFF:
            return None
        if exponent_field == 0 and fraction == 0:
            return (0, 0)

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
        return (coefficient, exponent2)

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
            "anomaly_matrix_version": _A_VERSION,
            "target": target,
            "mandatory_outcome": outcome,
            "acquisition_fatal": False,
            "qualification_evidence_bindings": (),
        }

    def isolation_snapshot(self) -> dict[str, Any]:
        allow = tuple(self.context.get("preseal_input_allowlist", ()))
        reads = tuple(item for item in _ALLOWED_PRESEAL if item in allow)
        return {
            "workspace_isolation_identity": self.context.get("workspace_isolation_identity"),
            "preseal_input_allowlist": allow,
            "network_policy": self.context.get("network_policy"),
            "ipc_policy": self.context.get("ipc_policy"),
            "environment_variable_allowlist": tuple(
                self.context.get("environment_variable_allowlist", ())
            ),
            "cache_policy": self.context.get("cache_policy"),
            "other_path_output_readable": self.context.get(
                "other_path_output_readable"
            ),
            "runtime_read_set": reads,
        }

    def environment_is_closed(self) -> bool:
        isolation = self.isolation_snapshot()
        workspace = isolation["workspace_isolation_identity"]
        return (
            isinstance(workspace, str)
            and bool(workspace.strip())
            and frozenset(isolation["preseal_input_allowlist"]) == _ALLOWED_PRESEAL
            and frozenset(isolation["environment_variable_allowlist"]) == _ALLOWED_ENV
            and isolation["network_policy"] == "DENY"
            and isolation["ipc_policy"] == "DENY"
            and isolation["cache_policy"] == "PRIVATE_ONLY"
            and isolation["other_path_output_readable"] is False
            and frozenset(isolation["runtime_read_set"]) == _ALLOWED_PRESEAL
        )

    def check_normative_package(self) -> tuple[bool, str]:
        if not isinstance(self.package, Mapping):
            return False, "INPUT_PACKAGE_NOT_MAPPING"

        expected = {
            "representation_id": _R_ID,
            "representation_version": _R_VERSION,
            "record_model_version": _M_VERSION,
            "format_binding_id": _B_ID,
            "format_binding_version": _B_VERSION,
            "anomaly_matrix_id": _A_ID,
            "anomaly_matrix_version": _A_VERSION,
            "qualification_contract_id": _Q_ID,
            "qualification_contract_version": _Q_VERSION,
            "freeze_contract_id": _F_ID,
            "freeze_contract_version": _F_VERSION,
            "oracle_id": _O_ID,
            "oracle_version": _O_VERSION,
        }
        for key, required in expected.items():
            if self.package.get(key) != required:
                return False, f"NORMATIVE_IDENTITY_MISMATCH:{key}"

        acquisition = self.package.get("acquisition_domain_id")
        if not isinstance(acquisition, str) or not acquisition:
            return False, "MISSING_ACQUISITION_DOMAIN_ID"
        self.acquisition_id = acquisition

        determinants = self.package.get("determinant_digests")
        if not isinstance(determinants, Mapping):
            return False, "MISSING_DETERMINANT_DIGESTS"

        self.determinants = {
            str(key): str(value)
            for key, value in determinants.items()
            if str(key) in _REQUIRED_DETERMINANTS and self.digest_like(value)
        }

        if set(determinants) != _REQUIRED_DETERMINANTS:
            return False, "INCOMPLETE_DETERMINANT_SET"
        if any(not self.digest_like(value) for value in determinants.values()):
            return False, "INVALID_DETERMINANT_DIGEST"

        components = self.package.get("components")
        if not isinstance(components, (tuple, list)) or not components:
            return False, "MISSING_COMPONENT_MATERIALIZATION"
        return True, "OK"

    def decode_component_envelope(
        self,
        payload: bytes,
    ) -> bytes | None:
        try:
            decoder = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)
            decoded = decoder.decompress(payload)
        except lzma.LZMAError:
            return None
        if not decoder.eof or decoder.unused_data:
            return None
        return decoded

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
                    "BI5-A09",
                    "COMPLETE_SLOT",
                    "REJECT_RECORD",
                    component_id=component_id,
                    slot_index=slot_index,
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
                    "BI5-A10",
                    "COMPLETE_SLOT",
                    "REJECT_RECORD",
                    component_id=component_id,
                    slot_index=slot_index,
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
                "market_timestamp_utc": self.format_timestamp(hour, offset_ms),
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
        )
        self.accounting.append(
            {
                "component_manifest_entry_id": component_id,
                "component_local_slot_index": slot_index,
                "disposition": "CANDIDATE_RETAINED",
                "anomaly_class_id": None,
            }
        )

    def scan_component_slots(
        self,
        component_id: str,
        decoded: bytes,
        hour: datetime,
    ) -> None:
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
            self.anomalies.append(
                self.anomaly(
                    "BI5-A07",
                    "TERMINAL_FRAGMENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                    fragment_start=complete * _RECORD_WIDTH,
                    fragment_length=remainder,
                )
            )
            self.blocked = True

    def classify_component(self, component: Any) -> None:
        if not isinstance(component, Mapping):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11",
                    "ACQUISITION",
                    "QUALIFICATION_BLOCKED",
                    acquisition_id=self.acquisition_id,
                )
            )
            self.blocked = True
            return

        component_id = component.get("component_manifest_entry_id")
        if not isinstance(component_id, str) or not component_id:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11",
                    "ACQUISITION",
                    "QUALIFICATION_BLOCKED",
                    acquisition_id=self.acquisition_id,
                )
            )
            self.blocked = True
            return

        if (
            component.get("instrument_id") != "USATECHIDXUSD"
            or component.get("declared_role") != "HOURLY_NATIVE_BI5_TICKS"
        ):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A12",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        hour = self.parse_hour(component.get("declared_hour_bucket_utc"))
        if hour is None:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A04",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        payload = component.get("compressed_payload_bytes")
        expected_hash = component.get("payload_sha256")
        if (
            not isinstance(payload, bytes)
            or not self.digest_like(expected_hash)
            or _sha256_bytes(payload) != expected_hash
        ):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A11",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        decoded = self.decode_component_envelope(payload)
        if decoded is None:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A05",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return
        if not decoded:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A06",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True
            return

        self.scan_component_slots(component_id, decoded, hour)

    def finalize_membership(self) -> tuple[bool, str]:
        if self.blocked:
            return False, "QUALIFICATION_BLOCKED_ANOMALY"

        occurrence_sources = [
            (
                item["component_manifest_entry_id"],
                item["component_local_slot_index"],
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

    def blocked_result(self, reason: str) -> ImplementationQualificationResult:
        diagnostics = tuple(self.accounting)
        result = ImplementationQualificationResult(
            schema=RESULT_SCHEMA,
            implementation_id=IMPLEMENTATION_ID,
            implementation_version=IMPLEMENTATION_VERSION,
            implementation_manifest_digest=_manifest_sha256(),
            input_determinant_digests=dict(self.determinants),
            materialized_acquisition_id=self.acquisition_id,
            execution_status="COMPLETED",
            semantic_status="QUALIFICATION_BLOCKED",
            freeze_status="NOT_CREATED",
            qualified_occurrences=None,
            source_accounting=None,
            anomaly_outcomes=tuple(self.anomalies),
            terminal_evidence={
                "artifact_class": "QUALIFICATION_TERMINAL_EVIDENCE",
                "freeze_state": "NOT_CREATED",
                "qualified_universe": None,
                "qualified_occurrence_count": None,
                "reason": reason,
                "execution_diagnostics": {
                    "non_normative_source_accounting": diagnostics,
                },
            },
            isolation_evidence=self.isolation_snapshot(),
            result_seal="",
        )
        return _with_seal(result)

    def environment_blocked_result(self) -> ImplementationQualificationResult:
        result = ImplementationQualificationResult(
            schema=RESULT_SCHEMA,
            implementation_id=IMPLEMENTATION_ID,
            implementation_version=IMPLEMENTATION_VERSION,
            implementation_manifest_digest=_manifest_sha256(),
            input_determinant_digests=dict(self.determinants),
            materialized_acquisition_id=self.acquisition_id,
            execution_status="ENVIRONMENT_BLOCKED",
            semantic_status="NOT_REACHED",
            freeze_status="NOT_REACHED",
            qualified_occurrences=None,
            source_accounting=None,
            anomaly_outcomes=None,
            terminal_evidence={
                "reason": "PRESEAL_EXECUTION_ENVIRONMENT_NOT_CLOSED",
            },
            isolation_evidence=self.isolation_snapshot(),
            result_seal="",
        )
        return _with_seal(result)

    def make_terminal_result(self) -> ImplementationQualificationResult:
        result = ImplementationQualificationResult(
            schema=RESULT_SCHEMA,
            implementation_id=IMPLEMENTATION_ID,
            implementation_version=IMPLEMENTATION_VERSION,
            implementation_manifest_digest=_manifest_sha256(),
            input_determinant_digests=dict(self.determinants),
            materialized_acquisition_id=self.acquisition_id,
            execution_status="COMPLETED",
            semantic_status="QUALIFIED",
            freeze_status="FROZEN",
            qualified_occurrences=tuple(self.occurrences),
            source_accounting=tuple(self.accounting),
            anomaly_outcomes=tuple(self.anomalies),
            terminal_evidence=None,
            isolation_evidence=self.isolation_snapshot(),
            result_seal="",
        )
        sealed = _with_seal(result)
        return validate_implementation_result(sealed)

    def run(self) -> ImplementationQualificationResult:
        valid, reason = self.check_normative_package()
        if not valid:
            self.anomalies.append(
                self.anomaly(
                    "BI5-A12",
                    "ACQUISITION",
                    "QUALIFICATION_BLOCKED",
                    acquisition_id=self.acquisition_id,
                )
            )
            return self.blocked_result(reason)

        if not self.environment_is_closed():
            return self.environment_blocked_result()

        components = self.package["components"]
        counts: dict[str, int] = {}
        for component in components:
            if isinstance(component, Mapping):
                component_id = component.get("component_manifest_entry_id")
                if isinstance(component_id, str) and component_id:
                    counts[component_id] = counts.get(component_id, 0) + 1

        duplicates = {key for key, count in counts.items() if count > 1}
        for component_id in sorted(duplicates):
            self.anomalies.append(
                self.anomaly(
                    "BI5-A03",
                    "COMPONENT",
                    "QUALIFICATION_BLOCKED",
                    component_id=component_id,
                )
            )
            self.blocked = True

        for component in components:
            component_id = (
                component.get("component_manifest_entry_id")
                if isinstance(component, Mapping)
                else None
            )
            if isinstance(component_id, str) and component_id in duplicates:
                continue
            self.classify_component(component)

        qualified, reason = self.finalize_membership()
        if not qualified:
            return self.blocked_result(reason)
        return self.make_terminal_result()


def qualify_native_bi5(
    input_package: Mapping[str, Any],
    *,
    execution_context: Mapping[str, Any],
) -> ImplementationQualificationResult:
    engine = IndependentQualificationEngine(input_package, execution_context)
    return engine.run()
