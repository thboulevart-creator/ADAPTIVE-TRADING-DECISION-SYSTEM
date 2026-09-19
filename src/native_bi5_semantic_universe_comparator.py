from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping
from typing import Any

from src.native_bi5_freeze_persistence import validate_freeze_artifact


ORACLE_ID = "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR"
ORACLE_VERSION = (
    "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE"
)
RESULT_SCHEMA = "NATIVE_BI5_SEMANTIC_COMPARISON_RESULT_V0_1_CANDIDATE"


def _result(
    oracle_result: str,
    qualified_universe_comparison: str,
    comparison_scope: str,
    reason: str,
) -> dict[str, str]:
    return {
        "schema": RESULT_SCHEMA,
        "oracle_id": ORACLE_ID,
        "oracle_version": ORACLE_VERSION,
        "oracle_result": oracle_result,
        "qualified_universe_comparison": qualified_universe_comparison,
        "comparison_scope": comparison_scope,
        "reason": reason,
    }


def _blocked(scope: str, reason: str) -> dict[str, str]:
    return _result("BLOCKED", "BLOCKED", scope, reason)


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _validated_artifact(value: Any) -> Mapping[str, Any] | None:
    if not isinstance(value, Mapping):
        return None
    try:
        validate_freeze_artifact(value)
    except (TypeError, ValueError, KeyError):
        return None
    return value


def _bindings(universe: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        item["stage"]: item
        for item in universe["reconstruction_tuple"]
    }


def _determinant_gate(
    left_u: Mapping[str, Any],
    right_u: Mapping[str, Any],
) -> dict[str, str] | None:
    left = _bindings(left_u)
    right = _bindings(right_u)
    stages = ("D", "R", "M", "B", "A", "Q", "F")

    for stage in stages:
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
                "NORMATIVE_VERSION_INTEGRITY_CONFLICT",
            )

    for stage in stages:
        l_item = left[stage]
        r_item = right[stage]
        if (
            l_item["normative_id"] != r_item["normative_id"]
            or l_item["normative_version"] != r_item["normative_version"]
        ):
            return _blocked(
                "DISTINCT_QUALIFICATION_STATE",
                "DISTINCT_QUALIFICATION_STATE",
            )

    if left_u["qualification_parameters"] != right_u["qualification_parameters"]:
        return _blocked(
            "DISTINCT_QUALIFICATION_STATE",
            "DISTINCT_QUALIFICATION_STATE",
        )

    return None


def _component_semantics(item: Mapping[str, Any]) -> dict[str, Any]:
    fragment = item.get("terminal_fragment")
    fragment_semantics = None
    if isinstance(fragment, Mapping):
        fragment_semantics = {
            key: fragment[key]
            for key in (
                "terminal_fragment_start_offset",
                "terminal_fragment_length",
                "remainder_reference",
            )
            if key in fragment
        }

    return {
        "component_manifest_entry_id": item["component_manifest_entry_id"],
        "declared_role": item["declared_role"],
        "instrument_source_identity": item["instrument_source_identity"],
        "declared_hour_bucket_utc": item["declared_hour_bucket_utc"],
        "immutable_payload_reference": item["immutable_payload_reference"],
        "payload_integrity_reference": item["payload_integrity_reference"],
        "materialization_status": item["materialization_status"],
        "complete_slot_count": item["complete_slot_count"],
        "terminal_fragment": fragment_semantics,
    }


def _component_relation(universe: Mapping[str, Any]) -> Counter[str]:
    return Counter(
        _canonical(_component_semantics(item))
        for item in universe["components"]
    )


def _completeness_binding(universe: Mapping[str, Any]) -> dict[str, Any]:
    evidence = universe["completeness_evidence"]
    return {
        "immutable_reference": evidence["immutable_reference"],
        "integrity_digest": evidence["integrity_digest"],
    }


def _materialized_acquisition_equal(
    left_u: Mapping[str, Any],
    right_u: Mapping[str, Any],
) -> bool:
    if left_u["acquisition_domain_id"] != right_u["acquisition_domain_id"]:
        return False
    if (
        left_u["acquisition_declaration_version"]
        != right_u["acquisition_declaration_version"]
    ):
        return False
    if _completeness_binding(left_u) != _completeness_binding(right_u):
        return False
    if _component_relation(left_u) != _component_relation(right_u):
        return False
    return True


def _accounting_relation(universe: Mapping[str, Any]) -> Counter[str]:
    rows = []
    for item in universe["source_accounting"]:
        rows.append(
            {
                "component_manifest_entry_id": item["component_manifest_entry_id"],
                "component_local_slot_index": item["component_local_slot_index"],
                "disposition": item["disposition"],
                "anomaly_class_id": item.get("anomaly_class_id"),
            }
        )
    return Counter(_canonical(item) for item in rows)


def _anomaly_relation(universe: Mapping[str, Any]) -> Counter[str]:
    rows = []
    for item in universe["anomaly_outcomes"]:
        rows.append(
            {
                "anomaly_class_id": item["anomaly_class_id"],
                "target": item["target"],
                "mandatory_outcome": item["mandatory_outcome"],
                "acquisition_fatal": item["acquisition_fatal"],
            }
        )
    return Counter(_canonical(item) for item in rows)


def _logical_payload_bag(universe: Mapping[str, Any]) -> Counter[str]:
    return Counter(
        _canonical(item["logical_payload"])
        for item in universe["retained_occurrences"]
    )


def _retained_relation(universe: Mapping[str, Any]) -> Counter[str]:
    rows = []
    for item in universe["retained_occurrences"]:
        witness = item["source_witness"]
        rows.append(
            {
                "component_manifest_entry_id": witness[
                    "component_manifest_entry_id"
                ],
                "component_local_slot_index": witness[
                    "component_local_slot_index"
                ],
                "logical_payload": item["logical_payload"],
            }
        )
    return Counter(_canonical(item) for item in rows)


def _semantic_projection(
    artifact: Mapping[str, Any],
) -> tuple[Any, ...]:
    universe = artifact["qualified_universe"]
    return (
        _accounting_relation(universe),
        _anomaly_relation(universe),
        _logical_payload_bag(universe),
        _retained_relation(universe),
        artifact["qualified_occurrence_count"],
    )


def compare_freeze_artifacts(left_artifact, right_artifact):
    left = _validated_artifact(left_artifact)
    right = _validated_artifact(right_artifact)

    if left is None or right is None:
        return _blocked("INVALID_F_INPUT", "INVALID_F_INPUT")

    if (
        left["freeze_state"] != "FROZEN"
        or right["freeze_state"] != "FROZEN"
        or left["qualification_outcome"] != "QUALIFIED"
        or right["qualification_outcome"] != "QUALIFIED"
    ):
        return _blocked("TERMINAL_INPUT", "QUALIFIED_UNIVERSE_UNAVAILABLE")

    left_u = left["qualified_universe"]
    right_u = right["qualified_universe"]

    gate = _determinant_gate(left_u, right_u)
    if gate is not None:
        return gate

    if not _materialized_acquisition_equal(left_u, right_u):
        return _blocked(
            "NONCOMPARABLE_ACQUISITION_STATE",
            "MATERIALIZED_ACQUISITION_STATE_DIFFERS",
        )

    if _semantic_projection(left) == _semantic_projection(right):
        return _result(
            "SEMANTIC_EQUAL",
            "SEMANTIC_EQUAL",
            "SAME_QUALIFICATION_STATE",
            "SEMANTIC_PROJECTIONS_EQUAL",
        )

    return _result(
        "SEMANTIC_DIFFERENT",
        "SEMANTIC_DIFFERENT",
        "SAME_QUALIFICATION_STATE",
        "SEMANTIC_PROJECTIONS_DIFFER",
    )
