from __future__ import annotations

import copy
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any


FREEZE_CONTRACT_ID = "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE"
FREEZE_CONTRACT_VERSION = (
    "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE"
)
ARTIFACT_SCHEMA = "QUALIFICATION_FREEZE_ARTIFACT_V0_1_CANDIDATE"

_D_ID = "D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1"
_R_ID = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS"
_R_VERSION = "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE"
_M_ID = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL"
_M_VERSION = "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE"
_B_ID = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
_B_VERSION = "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
_A_ID = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD"
_A_VERSION = "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
_Q_ID = "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP"
_Q_VERSION = "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE"
_EXPECTED_COMPONENT_ROLE = "HOURLY_NATIVE_BI5_TICKS"
_EXPECTED_COMPONENT_SOURCE = "DUKASCOPY/USATECHIDXUSD"

_REQUIRED_STAGES = frozenset(("D", "R", "M", "B", "A", "Q", "F"))
_ALLOWED_Q_OUTCOMES = frozenset(
    ("QUALIFIED", "QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED")
)
_ALLOWED_DISPOSITIONS = frozenset(("CANDIDATE_RETAINED", "REJECT_RECORD"))
_TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$"
)


class _ConstructionError(ValueError):
    pass


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _is_digest(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _artifact_digest(artifact: Mapping[str, Any]) -> str:
    unsigned = {
        key: value
        for key, value in artifact.items()
        if key != "artifact_integrity_digest"
    }
    return hashlib.sha256(_canonical_bytes(unsigned)).hexdigest()


def _seal_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    artifact["artifact_integrity_digest"] = _artifact_digest(artifact)
    return artifact


def _terminal_artifact(
    qualification_outcome: str,
    reason: str,
    *,
    anomaly_outcomes: Sequence[Any] | None = None,
    upstream_terminal_evidence: Any = None,
) -> dict[str, Any]:
    terminal_evidence: dict[str, Any] = {
        "qualification_outcome": qualification_outcome,
        "freeze_construction_outcome": "NOT_CREATED",
        "reason": reason,
        "anomaly_outcomes": copy.deepcopy(list(anomaly_outcomes or ())),
    }
    if upstream_terminal_evidence is not None:
        terminal_evidence["upstream_terminal_evidence"] = copy.deepcopy(
            upstream_terminal_evidence
        )

    return _seal_artifact(
        {
            "schema": ARTIFACT_SCHEMA,
            "freeze_contract_id": FREEZE_CONTRACT_ID,
            "freeze_contract_version": FREEZE_CONTRACT_VERSION,
            "artifact_class": "QUALIFICATION_TERMINAL_EVIDENCE",
            "freeze_state": "NOT_CREATED",
            "qualification_outcome": qualification_outcome,
            "qualified_universe": None,
            "qualified_occurrence_count": None,
            "terminal_evidence": terminal_evidence,
        }
    )


def _validate_binding(binding: Any) -> dict[str, Any]:
    if not isinstance(binding, Mapping):
        raise _ConstructionError("reconstruction binding must be an object")
    required = (
        "stage",
        "normative_id",
        "normative_version",
        "immutable_reference",
        "integrity_digest",
    )
    if any(key not in binding for key in required):
        raise _ConstructionError("reconstruction binding incomplete")
    if not all(_is_nonempty_string(binding[key]) for key in required[:-1]):
        raise _ConstructionError("reconstruction binding contains empty identity")
    if not _is_digest(binding["integrity_digest"]):
        raise _ConstructionError("reconstruction binding digest invalid")
    return copy.deepcopy(dict(binding))


def _validate_reconstruction_tuple(
    value: Any,
    acquisition_declaration_version: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _ConstructionError("reconstruction tuple missing")

    bindings = [_validate_binding(item) for item in value]
    stages = [item["stage"] for item in bindings]
    if set(stages) != _REQUIRED_STAGES or len(stages) != len(_REQUIRED_STAGES):
        raise _ConstructionError("reconstruction tuple is not exact")

    by_stage = {item["stage"]: item for item in bindings}
    expected = {
        "D": (_D_ID, acquisition_declaration_version),
        "R": (_R_ID, _R_VERSION),
        "M": (_M_ID, _M_VERSION),
        "B": (_B_ID, _B_VERSION),
        "A": (_A_ID, _A_VERSION),
        "Q": (_Q_ID, _Q_VERSION),
        "F": (FREEZE_CONTRACT_ID, FREEZE_CONTRACT_VERSION),
    }
    for stage, (expected_id, expected_version) in expected.items():
        binding = by_stage[stage]
        if (
            binding["normative_id"] != expected_id
            or binding["normative_version"] != expected_version
        ):
            raise _ConstructionError(
                f"{stage} determinant identity/version mismatch"
            )

    return bindings


def _validate_completeness_evidence(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise _ConstructionError("D completeness evidence missing")
    if not _is_nonempty_string(value.get("immutable_reference")):
        raise _ConstructionError("D completeness reference missing")
    if not _is_digest(value.get("integrity_digest")):
        raise _ConstructionError("D completeness digest invalid")
    return copy.deepcopy(dict(value))


def _validate_terminal_fragment(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise _ConstructionError("terminal fragment malformed")
    start = value.get("terminal_fragment_start_offset")
    length = value.get("terminal_fragment_length")
    if isinstance(start, bool) or not isinstance(start, int) or start < 0:
        raise _ConstructionError("terminal fragment start invalid")
    if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
        raise _ConstructionError("terminal fragment length invalid")
    return copy.deepcopy(dict(value))


def _validate_components(value: Any) -> tuple[list[dict[str, Any]], dict[str, int]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _ConstructionError("component snapshot missing")
    if not value:
        raise _ConstructionError("component snapshot empty")

    result: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    seen: set[str] = set()

    for raw in value:
        if not isinstance(raw, Mapping):
            raise _ConstructionError("component snapshot malformed")
        component = copy.deepcopy(dict(raw))
        component_id = component.get("component_manifest_entry_id")
        if not _is_nonempty_string(component_id) or component_id in seen:
            raise _ConstructionError("component identity invalid or repeated")
        seen.add(component_id)

        required_strings = (
            "declared_role",
            "instrument_source_identity",
            "declared_hour_bucket_utc",
            "immutable_payload_reference",
        )
        if any(not _is_nonempty_string(component.get(key)) for key in required_strings):
            raise _ConstructionError("component reconstruction field missing")
        if component["declared_role"] != _EXPECTED_COMPONENT_ROLE:
            raise _ConstructionError("component role outside concrete F domain")
        if component["instrument_source_identity"] != _EXPECTED_COMPONENT_SOURCE:
            raise _ConstructionError("component source identity outside concrete F domain")
        try:
            hour = datetime.strptime(
                component["declared_hour_bucket_utc"],
                "%Y-%m-%dT%H:%M:%SZ",
            )
        except ValueError as exc:
            raise _ConstructionError("declared hour bucket invalid") from exc
        if hour.minute != 0 or hour.second != 0 or hour.microsecond != 0:
            raise _ConstructionError("declared hour bucket is not hour aligned")
        if not _is_digest(component.get("payload_integrity_reference")):
            raise _ConstructionError("component payload integrity invalid")
        if component.get("materialization_status") != "MATERIALIZED":
            raise _ConstructionError("component is not materialized")

        count = component.get("complete_slot_count")
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise _ConstructionError("complete slot count invalid")
        component["terminal_fragment"] = _validate_terminal_fragment(
            component.get("terminal_fragment")
        )
        if count == 0 and component["terminal_fragment"] is None:
            raise _ConstructionError("zero-byte component cannot be qualified")

        result.append(component)
        counts[component_id] = count

    return result, counts


def _witness(value: Any) -> tuple[str, int]:
    if not isinstance(value, Mapping):
        raise _ConstructionError("source witness malformed")
    if set(value) != {
        "component_manifest_entry_id",
        "component_local_slot_index",
    }:
        raise _ConstructionError("source witness shape invalid")
    component_id = value.get("component_manifest_entry_id")
    slot = value.get("component_local_slot_index")
    if not _is_nonempty_string(component_id):
        raise _ConstructionError("source witness component missing")
    if isinstance(slot, bool) or not isinstance(slot, int) or slot < 0:
        raise _ConstructionError("source witness slot invalid")
    return component_id, slot


def _validate_volume(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise _ConstructionError("binary32 value malformed")
    if set(value) != {"integer_coefficient", "exponent2"}:
        raise _ConstructionError("binary32 normal form shape invalid")
    coefficient = value["integer_coefficient"]
    exponent = value["exponent2"]
    if (
        isinstance(coefficient, bool)
        or not isinstance(coefficient, int)
        or isinstance(exponent, bool)
        or not isinstance(exponent, int)
    ):
        raise _ConstructionError("binary32 normal form type invalid")
    if coefficient == 0:
        if exponent != 0:
            raise _ConstructionError("zero binary32 normal form not unique")
        return

    if coefficient % 2 == 0:
        raise _ConstructionError("binary32 coefficient must be odd")

    magnitude_bits = abs(coefficient).bit_length()
    if magnitude_bits > 24:
        raise _ConstructionError("binary32 coefficient exceeds significand domain")
    if exponent < -149:
        raise _ConstructionError("binary32 exponent below representable domain")
    if exponent + magnitude_bits - 1 > 127:
        raise _ConstructionError("binary32 value exceeds finite representable domain")


def _validate_price(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise _ConstructionError("price rational malformed")
    if set(value) != {"numerator", "denominator"}:
        raise _ConstructionError("price rational shape invalid")
    numerator = value["numerator"]
    denominator = value["denominator"]
    if isinstance(numerator, bool) or not isinstance(numerator, int):
        raise _ConstructionError("price numerator invalid")
    if numerator < 0 or numerator > 0xFFFFFFFF:
        raise _ConstructionError("price numerator outside uint32 domain")
    if denominator != 1000:
        raise _ConstructionError("price denominator invalid")


def _validate_logical_payload(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise _ConstructionError("logical payload malformed")
    required = {
        "market_timestamp_utc",
        "ask_price",
        "bid_price",
        "ask_volume",
        "bid_volume",
    }
    if set(value) != required:
        raise _ConstructionError("logical payload shape invalid")
    timestamp = value["market_timestamp_utc"]
    if not isinstance(timestamp, str) or _TIMESTAMP.fullmatch(timestamp) is None:
        raise _ConstructionError("timestamp normal form invalid")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError as exc:
        raise _ConstructionError("timestamp is not a valid UTC instant") from exc
    _validate_price(value["ask_price"])
    _validate_price(value["bid_price"])
    _validate_volume(value["ask_volume"])
    _validate_volume(value["bid_volume"])


def _validate_occurrences(
    value: Any,
    component_counts: Mapping[str, int],
) -> tuple[list[dict[str, Any]], dict[tuple[str, int], Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _ConstructionError("occurrence relation missing")

    result: list[dict[str, Any]] = []
    relation: dict[tuple[str, int], Any] = {}
    allowed_occurrence_keys = {
        "logical_payload",
        "source_witness",
        "source_provenance",
    }

    for raw in value:
        if not isinstance(raw, Mapping):
            raise _ConstructionError("occurrence malformed")
        occurrence = copy.deepcopy(dict(raw))
        if not set(occurrence).issubset(allowed_occurrence_keys):
            raise _ConstructionError("occurrence carries canonical identity leakage")
        if "logical_payload" not in occurrence or "source_witness" not in occurrence:
            raise _ConstructionError("occurrence incomplete")

        source = _witness(occurrence["source_witness"])
        count = component_counts.get(source[0])
        if count is None or source[1] >= count:
            raise _ConstructionError("occurrence witness outside complete slots")
        if source in relation:
            raise _ConstructionError("occurrence witness repeated")

        _validate_logical_payload(occurrence["logical_payload"])
        if "source_provenance" in occurrence and not isinstance(
            occurrence["source_provenance"], Mapping
        ):
            raise _ConstructionError("source provenance malformed")

        relation[source] = copy.deepcopy(occurrence["logical_payload"])
        result.append(occurrence)

    return result, relation


def _validate_accounting(
    value: Any,
    component_counts: Mapping[str, int],
) -> tuple[list[dict[str, Any]], dict[tuple[str, int], dict[str, Any]]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _ConstructionError("source accounting missing")

    expected = {
        (component_id, slot)
        for component_id, count in component_counts.items()
        for slot in range(count)
    }
    relation: dict[tuple[str, int], dict[str, Any]] = {}
    result: list[dict[str, Any]] = []

    for raw in value:
        if not isinstance(raw, Mapping):
            raise _ConstructionError("source accounting malformed")
        item = copy.deepcopy(dict(raw))
        allowed_keys = {
            "component_manifest_entry_id",
            "component_local_slot_index",
            "disposition",
            "anomaly_class_id",
        }
        if set(item) != allowed_keys:
            raise _ConstructionError("source accounting shape invalid")
        component_id = item.get("component_manifest_entry_id")
        slot = item.get("component_local_slot_index")
        if not _is_nonempty_string(component_id):
            raise _ConstructionError("source accounting component invalid")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot < 0:
            raise _ConstructionError("source accounting slot invalid")
        source = (component_id, slot)
        if source not in expected or source in relation:
            raise _ConstructionError("source accounting witness invalid")
        disposition = item.get("disposition")
        if disposition not in _ALLOWED_DISPOSITIONS:
            raise _ConstructionError("source accounting disposition invalid")
        anomaly_class = item.get("anomaly_class_id")
        if disposition == "CANDIDATE_RETAINED":
            if anomaly_class is not None:
                raise _ConstructionError("retained source carries rejection anomaly")
        elif not _is_nonempty_string(anomaly_class):
            raise _ConstructionError("rejected source lacks anomaly class")

        relation[source] = item
        result.append(item)

    if set(relation) != expected:
        raise _ConstructionError("source accounting is incomplete")

    return result, relation


def _semantic_anomaly_target(target: Any) -> tuple[str, tuple[Any, ...]]:
    if not isinstance(target, Mapping):
        raise _ConstructionError("anomaly target malformed")
    scope = target.get("target_scope")

    if scope == "COMPLETE_SLOT":
        if set(target) != {
            "target_scope",
            "component_manifest_entry_id",
            "component_local_slot_index",
        }:
            raise _ConstructionError("complete-slot anomaly target shape invalid")
        component_id = target.get("component_manifest_entry_id")
        slot = target.get("component_local_slot_index")
        if not _is_nonempty_string(component_id):
            raise _ConstructionError("complete-slot anomaly component invalid")
        if isinstance(slot, bool) or not isinstance(slot, int) or slot < 0:
            raise _ConstructionError("complete-slot anomaly slot invalid")
        return scope, (component_id, slot)

    if scope == "TERMINAL_FRAGMENT":
        if set(target) != {
            "target_scope",
            "component_manifest_entry_id",
            "terminal_fragment_start_offset",
            "terminal_fragment_length",
        }:
            raise _ConstructionError("terminal-fragment anomaly target shape invalid")
        component_id = target.get("component_manifest_entry_id")
        start = target.get("terminal_fragment_start_offset")
        length = target.get("terminal_fragment_length")
        if not _is_nonempty_string(component_id):
            raise _ConstructionError("terminal-fragment component invalid")
        if isinstance(start, bool) or not isinstance(start, int) or start < 0:
            raise _ConstructionError("terminal-fragment start invalid")
        if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
            raise _ConstructionError("terminal-fragment length invalid")
        return scope, (component_id, start, length)

    if scope == "COMPONENT":
        if set(target) != {"target_scope", "component_manifest_entry_id"}:
            raise _ConstructionError("component anomaly target shape invalid")
        component_id = target.get("component_manifest_entry_id")
        if not _is_nonempty_string(component_id):
            raise _ConstructionError("component anomaly target invalid")
        return scope, (component_id,)

    if scope == "ACQUISITION":
        if set(target) != {"target_scope", "acquisition_domain_id"}:
            raise _ConstructionError("acquisition anomaly target shape invalid")
        acquisition_id = target.get("acquisition_domain_id")
        if not _is_nonempty_string(acquisition_id):
            raise _ConstructionError("acquisition anomaly target invalid")
        return scope, (acquisition_id,)

    raise _ConstructionError("unknown anomaly target scope")


def _validate_a08_evidence(
    bindings: Any,
    target: Mapping[str, Any],
) -> None:
    if not isinstance(bindings, Sequence) or isinstance(
        bindings, (str, bytes, bytearray)
    ) or not bindings:
        raise _ConstructionError("A08 constructive proof binding missing")

    for raw in bindings:
        if not isinstance(raw, Mapping):
            raise _ConstructionError("A08 proof binding malformed")
        required = {
            "evidence_role",
            "immutable_reference",
            "integrity_digest_or_reference",
            "exact_anomaly_target_binding",
        }
        if set(raw) != required:
            raise _ConstructionError("A08 proof binding incomplete")
        if not all(
            _is_nonempty_string(raw[key])
            for key in (
                "evidence_role",
                "immutable_reference",
                "integrity_digest_or_reference",
            )
        ):
            raise _ConstructionError("A08 proof binding identity invalid")
        if raw["exact_anomaly_target_binding"] != target:
            raise _ConstructionError("A08 proof binding target mismatch")


def _validate_anomalies(
    value: Any,
    component_map: Mapping[str, Mapping[str, Any]],
    acquisition_domain_id: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise _ConstructionError("anomaly relation missing")

    result: list[dict[str, Any]] = []
    for raw in value:
        if not isinstance(raw, Mapping):
            raise _ConstructionError("anomaly relation malformed")
        item = copy.deepcopy(dict(raw))
        for key in (
            "anomaly_class_id",
            "anomaly_matrix_version",
            "target",
            "mandatory_outcome",
            "acquisition_fatal",
        ):
            if key not in item:
                raise _ConstructionError("anomaly relation incomplete")
        if not _is_nonempty_string(item["anomaly_class_id"]):
            raise _ConstructionError("anomaly class invalid")
        if item["anomaly_matrix_version"] != _A_VERSION:
            raise _ConstructionError("anomaly matrix version mismatch")
        if not _is_nonempty_string(item["mandatory_outcome"]):
            raise _ConstructionError("anomaly outcome invalid")
        if not isinstance(item["acquisition_fatal"], bool):
            raise _ConstructionError("anomaly fatal flag invalid")

        scope, locator = _semantic_anomaly_target(item["target"])
        if scope == "ACQUISITION" and locator[0] != acquisition_domain_id:
            raise _ConstructionError("acquisition anomaly target mismatch")
        if scope in ("COMPLETE_SLOT", "COMPONENT", "TERMINAL_FRAGMENT"):
            if locator[0] not in component_map:
                raise _ConstructionError("anomaly targets unknown component")

        bindings = item.get("qualification_evidence_bindings", [])
        if not isinstance(bindings, Sequence) or isinstance(
            bindings, (str, bytes, bytearray)
        ):
            raise _ConstructionError("qualification evidence bindings malformed")

        class_id = item["anomaly_class_id"]
        if class_id == "BI5-A08":
            raise _ConstructionError(
                "A08 constructive-completeness verifier is not qualified"
            )
        if class_id not in {"BI5-A09", "BI5-A10"}:
            raise _ConstructionError(
                "qualified state contains non-local anomaly class"
            )
        if scope != "COMPLETE_SLOT":
            raise _ConstructionError("local reject anomaly target must be complete slot")
        if item["mandatory_outcome"] != "REJECT_RECORD":
            raise _ConstructionError("local reject anomaly outcome mismatch")
        if item["acquisition_fatal"] is not False:
            raise _ConstructionError("local reject cannot be acquisition fatal")
        if len(bindings) != 0:
            raise _ConstructionError("A09/A10 must not invent evidence authority")

        result.append(item)

    return result


def _validate_qualified_input(
    freeze_input: Mapping[str, Any],
) -> dict[str, Any]:
    acquisition_domain_id = freeze_input.get("acquisition_domain_id")
    acquisition_declaration_version = freeze_input.get(
        "acquisition_declaration_version"
    )
    if not _is_nonempty_string(acquisition_domain_id):
        raise _ConstructionError("acquisition domain identity missing")
    if not _is_nonempty_string(acquisition_declaration_version):
        raise _ConstructionError("acquisition declaration version missing")

    reconstruction = _validate_reconstruction_tuple(
        freeze_input.get("reconstruction_tuple"),
        acquisition_declaration_version,
    )

    parameters = freeze_input.get("qualification_parameters")
    if not isinstance(parameters, Mapping) or not parameters:
        raise _ConstructionError("qualification parameters missing")
    parameters_copy = copy.deepcopy(dict(parameters))

    snapshot = freeze_input.get("acquisition_snapshot")
    if not isinstance(snapshot, Mapping):
        raise _ConstructionError("acquisition snapshot missing")
    if snapshot.get("acquisition_domain_id") != acquisition_domain_id:
        raise _ConstructionError("acquisition snapshot identity mismatch")

    completeness = _validate_completeness_evidence(
        snapshot.get("completeness_evidence")
    )
    components, component_counts = _validate_components(snapshot.get("components"))
    component_map = {
        item["component_manifest_entry_id"]: item
        for item in components
    }

    accounting, accounting_map = _validate_accounting(
        freeze_input.get("source_accounting"),
        component_counts,
    )
    b_occurrences, b_relation = _validate_occurrences(
        freeze_input.get("b_candidate_occurrences"),
        component_counts,
    )
    retained_occurrences, retained_relation = _validate_occurrences(
        freeze_input.get("retained_occurrences"),
        component_counts,
    )

    if b_relation != retained_relation:
        raise _ConstructionError("B candidate relation and Q retained relation disagree")

    retained_sources = {
        source
        for source, item in accounting_map.items()
        if item["disposition"] == "CANDIDATE_RETAINED"
    }
    rejected_sources = {
        source
        for source, item in accounting_map.items()
        if item["disposition"] == "REJECT_RECORD"
    }
    if retained_sources & rejected_sources:
        raise _ConstructionError("candidate/reject overlap")
    if set(retained_relation) != retained_sources:
        raise _ConstructionError("retained relation does not match slot accounting")

    anomalies = _validate_anomalies(
        freeze_input.get("anomaly_outcomes"),
        component_map,
        acquisition_domain_id,
    )

    anomaly_complete_slot_relation: set[tuple[str, int, str]] = set()
    terminal_a08: set[tuple[str, int, int]] = set()
    for anomaly in anomalies:
        scope, locator = _semantic_anomaly_target(anomaly["target"])
        if scope == "COMPLETE_SLOT":
            anomaly_complete_slot_relation.add(
                (locator[0], locator[1], anomaly["anomaly_class_id"])
            )
        elif anomaly["anomaly_class_id"] == "BI5-A08":
            terminal_a08.add((locator[0], locator[1], locator[2]))

    expected_local_anomalies = {
        (source[0], source[1], accounting_map[source]["anomaly_class_id"])
        for source in rejected_sources
    }
    local_anomaly_rows = [
        (item["target"]["component_manifest_entry_id"],
         item["target"]["component_local_slot_index"],
         item["anomaly_class_id"])
        for item in anomalies
    ]
    if len(local_anomaly_rows) != len(set(local_anomaly_rows)):
        raise _ConstructionError("duplicate local anomaly relation")
    if set(local_anomaly_rows) != expected_local_anomalies:
        raise _ConstructionError("local anomaly relation does not equal reject accounting")

    for source in rejected_sources:
        if source in b_relation:
            raise _ConstructionError("rejected source also appears as B candidate")

    for component in components:
        fragment = component.get("terminal_fragment")
        if fragment is not None:
            relation = (
                component["component_manifest_entry_id"],
                fragment["terminal_fragment_start_offset"],
                fragment["terminal_fragment_length"],
            )
            if relation not in terminal_a08:
                raise _ConstructionError(
                    "terminal fragment lacks exact qualified A08 relation"
                )

    return {
        "acquisition_domain_id": acquisition_domain_id,
        "acquisition_declaration_version": acquisition_declaration_version,
        "qualification_parameters": parameters_copy,
        "completeness_evidence": completeness,
        "reconstruction_tuple": reconstruction,
        "components": components,
        "source_accounting": accounting,
        "anomaly_outcomes": anomalies,
        "retained_occurrences": retained_occurrences,
        "b_candidate_occurrences": b_occurrences,
    }


def build_freeze_artifact(freeze_input):
    if not isinstance(freeze_input, Mapping):
        return _terminal_artifact(
            "QUALIFICATION_BLOCKED",
            "F_INPUT_NOT_MAPPING",
        )

    qualification_outcome = freeze_input.get("qualification_outcome")
    if qualification_outcome not in _ALLOWED_Q_OUTCOMES:
        return _terminal_artifact(
            "QUALIFICATION_BLOCKED",
            "Q_OUTCOME_INVALID_OR_MISSING",
        )

    if qualification_outcome != "QUALIFIED":
        return _terminal_artifact(
            qualification_outcome,
            "UPSTREAM_Q_NONQUALIFIED",
            anomaly_outcomes=freeze_input.get("anomaly_outcomes"),
            upstream_terminal_evidence=freeze_input.get(
                "qualification_terminal_evidence"
            ),
        )

    try:
        qualified = _validate_qualified_input(freeze_input)
    except _ConstructionError as exc:
        return _terminal_artifact(
            "QUALIFIED",
            f"F_CONSTRUCTION_BLOCKED:{exc}",
            anomaly_outcomes=freeze_input.get("anomaly_outcomes"),
        )

    artifact = {
        "schema": ARTIFACT_SCHEMA,
        "freeze_contract_id": FREEZE_CONTRACT_ID,
        "freeze_contract_version": FREEZE_CONTRACT_VERSION,
        "artifact_class": "QUALIFIED_UNIVERSE_FREEZE",
        "freeze_state": "FROZEN",
        "qualification_outcome": "QUALIFIED",
        "qualified_universe": qualified,
        "qualified_occurrence_count": len(qualified["retained_occurrences"]),
        "terminal_evidence": None,
    }
    try:
        return _seal_artifact(artifact)
    except (TypeError, ValueError):
        return _terminal_artifact(
            "QUALIFIED",
            "F_CONSTRUCTION_BLOCKED:STRICT_JSON_PERSISTENCE_FAILURE",
        )


def _validate_integrity(artifact: Mapping[str, Any]) -> None:
    digest = artifact.get("artifact_integrity_digest")
    if not _is_digest(digest) or digest != _artifact_digest(artifact):
        raise ValueError("artifact integrity digest mismatch")


def _validate_terminal_artifact(artifact: Mapping[str, Any]) -> None:
    if artifact.get("artifact_class") != "QUALIFICATION_TERMINAL_EVIDENCE":
        raise ValueError("terminal artifact class invalid")
    if artifact.get("freeze_state") != "NOT_CREATED":
        raise ValueError("terminal artifact cannot be frozen")
    if artifact.get("qualified_universe") is not None:
        raise ValueError("terminal artifact exposes qualified universe")
    if artifact.get("qualified_occurrence_count") is not None:
        raise ValueError("terminal artifact exposes qualified count")
    if artifact.get("freeze_id"):
        raise ValueError("terminal artifact claims freeze identity")
    terminal = artifact.get("terminal_evidence")
    if not isinstance(terminal, Mapping):
        raise ValueError("terminal evidence missing")
    if terminal.get("qualification_outcome") != artifact.get(
        "qualification_outcome"
    ):
        raise ValueError("terminal qualification outcome mismatch")
    if terminal.get("freeze_construction_outcome") != "NOT_CREATED":
        raise ValueError("terminal construction state invalid")


def _artifact_to_qualified_input(
    artifact: Mapping[str, Any],
) -> dict[str, Any]:
    universe = artifact.get("qualified_universe")
    if not isinstance(universe, Mapping):
        raise ValueError("qualified universe missing")

    return {
        "qualification_outcome": "QUALIFIED",
        "acquisition_domain_id": universe.get("acquisition_domain_id"),
        "acquisition_declaration_version": universe.get(
            "acquisition_declaration_version"
        ),
        "reconstruction_tuple": universe.get("reconstruction_tuple"),
        "qualification_parameters": universe.get("qualification_parameters"),
        "acquisition_snapshot": {
            "acquisition_domain_id": universe.get("acquisition_domain_id"),
            "completeness_evidence": universe.get("completeness_evidence"),
            "components": universe.get("components"),
        },
        "source_accounting": universe.get("source_accounting"),
        "b_candidate_occurrences": universe.get("b_candidate_occurrences"),
        "anomaly_outcomes": universe.get("anomaly_outcomes"),
        "retained_occurrences": universe.get("retained_occurrences"),
    }


def _validate_qualified_artifact(artifact: Mapping[str, Any]) -> None:
    if artifact.get("artifact_class") != "QUALIFIED_UNIVERSE_FREEZE":
        raise ValueError("qualified artifact class invalid")
    if artifact.get("freeze_state") != "FROZEN":
        raise ValueError("qualified artifact not frozen")
    if artifact.get("qualification_outcome") != "QUALIFIED":
        raise ValueError("qualified artifact Q outcome invalid")
    if artifact.get("terminal_evidence") is not None:
        raise ValueError("qualified artifact carries terminal evidence")

    try:
        qualified = _validate_qualified_input(
            _artifact_to_qualified_input(artifact)
        )
    except _ConstructionError as exc:
        raise ValueError(str(exc)) from exc

    count = artifact.get("qualified_occurrence_count")
    if (
        isinstance(count, bool)
        or not isinstance(count, int)
        or count != len(qualified["retained_occurrences"])
    ):
        raise ValueError("qualified occurrence count mismatch")


def validate_freeze_artifact(artifact):
    if not isinstance(artifact, Mapping):
        raise TypeError("freeze artifact must be an object")
    if artifact.get("schema") != ARTIFACT_SCHEMA:
        raise ValueError("freeze artifact schema invalid")
    if artifact.get("freeze_contract_id") != FREEZE_CONTRACT_ID:
        raise ValueError("freeze contract id invalid")
    if artifact.get("freeze_contract_version") != FREEZE_CONTRACT_VERSION:
        raise ValueError("freeze contract version invalid")
    if artifact.get("qualification_outcome") not in _ALLOWED_Q_OUTCOMES:
        raise ValueError("qualification outcome invalid")

    _validate_integrity(artifact)

    if artifact.get("freeze_state") == "FROZEN":
        _validate_qualified_artifact(artifact)
    elif artifact.get("freeze_state") == "NOT_CREATED":
        _validate_terminal_artifact(artifact)
    else:
        raise ValueError("freeze state invalid")

    return artifact


def serialize_freeze_artifact(artifact, *, pretty=False):
    validate_freeze_artifact(artifact)
    if not isinstance(pretty, bool):
        raise TypeError("pretty must be bool")
    if pretty:
        text = json.dumps(
            artifact,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            indent=2,
        )
    else:
        text = json.dumps(
            artifact,
            sort_keys=True,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
        )
    return (text + "\n").encode("utf-8")


def _strict_object_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_nonfinite_json_constant(value):
    raise ValueError(f"non-standard JSON numeric constant: {value}")


def deserialize_freeze_artifact(payload):
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError("freeze payload must be bytes")
    try:
        value = json.loads(
            bytes(payload).decode("utf-8"),
            object_pairs_hook=_strict_object_pairs,
            parse_constant=_reject_nonfinite_json_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("freeze payload is not strict UTF-8 JSON") from exc
    validate_freeze_artifact(value)
    return value
