from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
from typing import Any, Mapping

import pytest

from breakers.native_bi5_f_freeze_persistence_breaker import (
    _logical_payload,
    _occurrence,
    _qualified_input,
    _qualified_two_component_input,
    _qualified_with_local_reject,
    _qualified_with_two_local_rejects,
    _terminal_input,
)
from src import native_bi5_freeze_persistence as freeze


O_MODULE = "src.native_bi5_semantic_universe_comparator"

ORACLE_ID = "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR"
ORACLE_VERSION = (
    "O_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_SEMANTIC_UNIVERSE_COMPARATOR_V0_1_CANDIDATE"
)
RESULT_SCHEMA = "NATIVE_BI5_SEMANTIC_COMPARISON_RESULT_V0_1_CANDIDATE"


def _o():
    try:
        module = importlib.import_module(O_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            "O runtime absent — expected pre-implementation RED: "
            "src.native_bi5_semantic_universe_comparator does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    assert getattr(module, "ORACLE_ID", None) == ORACLE_ID
    assert getattr(module, "ORACLE_VERSION", None) == ORACLE_VERSION
    assert getattr(module, "RESULT_SCHEMA", None) == RESULT_SCHEMA
    assert hasattr(module, "compare_freeze_artifacts")
    return module


@pytest.fixture(autouse=True)
def _runtime_must_exist():
    _o()


def _assert_result_shape(result: Any) -> Mapping[str, Any]:
    assert isinstance(result, Mapping)
    assert result["schema"] == RESULT_SCHEMA
    assert result["oracle_id"] == ORACLE_ID
    assert result["oracle_version"] == ORACLE_VERSION
    assert result["oracle_result"] in {
        "SEMANTIC_EQUAL",
        "SEMANTIC_DIFFERENT",
        "BLOCKED",
    }
    assert result["qualified_universe_comparison"] in {
        "SEMANTIC_EQUAL",
        "SEMANTIC_DIFFERENT",
        "BLOCKED",
    }
    assert isinstance(result["comparison_scope"], str)
    assert isinstance(result["reason"], str)
    return result


def _compare(left: Any, right: Any) -> Mapping[str, Any]:
    result = _o().compare_freeze_artifacts(
        copy.deepcopy(left),
        copy.deepcopy(right),
    )
    return _assert_result_shape(result)


def _frozen(data=None):
    artifact = freeze.build_freeze_artifact(
        copy.deepcopy(_qualified_input() if data is None else data)
    )
    freeze.validate_freeze_artifact(artifact)
    assert artifact["freeze_state"] == "FROZEN"
    return artifact


def _terminal(outcome: str):
    artifact = freeze.build_freeze_artifact(_terminal_input(outcome))
    freeze.validate_freeze_artifact(artifact)
    assert artifact["freeze_state"] == "NOT_CREATED"
    return artifact


def _set_payload_field(data, slot: int, field: str, value: Any) -> None:
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        data[relation_name][slot]["logical_payload"][field] = copy.deepcopy(value)


def _same_semantics_permuted_input():
    data = _qualified_two_component_input()
    data["acquisition_snapshot"]["components"].reverse()
    data["source_accounting"].reverse()
    data["b_candidate_occurrences"].reverse()
    data["retained_occurrences"].reverse()
    data["reconstruction_tuple"].reverse()
    return data


def _same_semantics_diagnostic_permutation():
    left = _qualified_with_two_local_rejects()
    right = copy.deepcopy(left)
    right["anomaly_outcomes"].reverse()
    for index, item in enumerate(right["anomaly_outcomes"]):
        item["diagnostic_path"] = f"synthetic://other-worker/path/{index}"
        item["worker_id"] = f"worker-{index}"
    return left, right


def _swap_source_to_payload_relation():
    data = _qualified_input()
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        relation = data[relation_name]
        relation[0]["logical_payload"], relation[1]["logical_payload"] = (
            copy.deepcopy(relation[1]["logical_payload"]),
            copy.deepcopy(relation[0]["logical_payload"]),
        )
    return data


def _different_duplicate_multiplicity():
    data = _qualified_input()
    payload_b = _logical_payload(
        "2026-01-02T10:00:03.000Z",
        100_200,
        100_100,
        (1, 0),
        (1, 0),
    )
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        relation = data[relation_name]
        relation[2]["logical_payload"] = copy.deepcopy(payload_b)
    return data


def _local_anomaly_variant():
    data = _qualified_input()
    data["retained_occurrences"] = data["retained_occurrences"][:2]
    data["b_candidate_occurrences"] = copy.deepcopy(data["retained_occurrences"])
    data["source_accounting"][2] = {
        "component_manifest_entry_id": "SYNTH-F-COMP-001",
        "component_local_slot_index": 2,
        "disposition": "REJECT_RECORD",
        "anomaly_class_id": "BI5-A10",
    }
    data["anomaly_outcomes"] = [
        {
            "anomaly_class_id": "BI5-A10",
            "anomaly_matrix_version": (
                "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
            ),
            "target": {
                "target_scope": "COMPLETE_SLOT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
                "component_local_slot_index": 2,
            },
            "mandatory_outcome": "REJECT_RECORD",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
        }
    ]
    return data


def _repartitioned_same_payload_bag():
    data = _qualified_input()
    first_component = data["acquisition_snapshot"]["components"][0]
    first_component["complete_slot_count"] = 2

    second_component = {
        "component_manifest_entry_id": "SYNTH-F-COMP-002",
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
        "instrument_source_identity": "DUKASCOPY/USATECHIDXUSD",
        "declared_hour_bucket_utc": "2026-01-02T10:00:00Z",
        "immutable_payload_reference": "synthetic://payload/repartition-002",
        "payload_integrity_reference": "c" * 64,
        "materialization_status": "MATERIALIZED",
        "complete_slot_count": 1,
        "terminal_fragment": None,
    }
    data["acquisition_snapshot"]["components"].append(second_component)

    third_payload = copy.deepcopy(data["retained_occurrences"][2]["logical_payload"])
    moved = {
        "logical_payload": third_payload,
        "source_witness": {
            "component_manifest_entry_id": "SYNTH-F-COMP-002",
            "component_local_slot_index": 0,
        },
        "source_provenance": copy.deepcopy(
            data["retained_occurrences"][2].get("source_provenance", {})
        ),
    }
    data["source_accounting"] = data["source_accounting"][:2] + [
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-002",
            "component_local_slot_index": 0,
            "disposition": "CANDIDATE_RETAINED",
            "anomaly_class_id": None,
        }
    ]
    data["b_candidate_occurrences"] = (
        data["b_candidate_occurrences"][:2] + [copy.deepcopy(moved)]
    )
    data["retained_occurrences"] = data["retained_occurrences"][:2] + [moved]
    return data


def _reseal_for_breaker(artifact: Mapping[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(dict(artifact))
    unsigned = {
        key: child
        for key, child in value.items()
        if key != "artifact_integrity_digest"
    }
    payload = json.dumps(
        unsigned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    value["artifact_integrity_digest"] = hashlib.sha256(payload).hexdigest()
    return value


def _recursive_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            keys.add(str(key))
            keys.update(_recursive_keys(child))
    elif isinstance(value, (list, tuple)):
        for child in value:
            keys.update(_recursive_keys(child))
    return keys


def _semantic_verdict_tuple(result: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        result["oracle_result"],
        result["qualified_universe_comparison"],
        result["comparison_scope"],
    )


def _semantic_projection_for_breaker(artifact: Mapping[str, Any]) -> Mapping[str, Any]:
    universe = artifact["qualified_universe"]
    payload_bag = sorted(
        json.dumps(
            item["logical_payload"],
            sort_keys=True,
            separators=(",", ":"),
        )
        for item in universe["retained_occurrences"]
    )
    retained_relation = sorted(
        (
            item["source_witness"]["component_manifest_entry_id"],
            item["source_witness"]["component_local_slot_index"],
            json.dumps(
                item["logical_payload"],
                sort_keys=True,
                separators=(",", ":"),
            ),
        )
        for item in universe["retained_occurrences"]
    )
    return {
        "payload_bag": payload_bag,
        "retained_relation": retained_relation,
    }


def test_a0_surface_is_pure_comparator_only() -> None:
    module = _o()
    sig = inspect.signature(module.compare_freeze_artifacts)
    assert tuple(sig.parameters) == ("left_artifact", "right_artifact")
    forbidden = (
        "download_bi5",
        "run_backtest",
        "persist_freeze",
        "build_freeze_artifact",
        "order_send",
        "activate_live",
    )
    assert all(not hasattr(module, name) for name in forbidden)


def test_a1_same_valid_freeze_is_semantic_equal() -> None:
    artifact = _frozen()
    result = _compare(artifact, artifact)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert result["qualified_universe_comparison"] == "SEMANTIC_EQUAL"
    assert result["comparison_scope"] == "SAME_QUALIFICATION_STATE"


def test_a2_independently_built_equal_freezes_are_equal() -> None:
    left = _frozen(_qualified_two_component_input())
    right = _frozen(_same_semantics_permuted_input())
    assert left["artifact_integrity_digest"] != right["artifact_integrity_digest"]
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_b0_logical_payload_difference_is_semantic_different() -> None:
    left = _frozen()
    data = _qualified_input()
    _set_payload_field(
        data,
        0,
        "ask_price",
        {"numerator": 100_001, "denominator": 1000},
    )
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"
    assert result["qualified_universe_comparison"] == "SEMANTIC_DIFFERENT"


def test_b1_duplicate_multiplicity_difference_is_semantic_different() -> None:
    left = _frozen()
    right = _frozen(_different_duplicate_multiplicity())
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_b2_source_to_logical_relation_change_with_equal_payload_bag_is_different() -> None:
    left = _frozen()
    right = _frozen(_swap_source_to_payload_relation())
    assert (
        _semantic_projection_for_breaker(left)["payload_bag"]
        == _semantic_projection_for_breaker(right)["payload_bag"]
    )
    assert (
        _semantic_projection_for_breaker(left)["retained_relation"]
        != _semantic_projection_for_breaker(right)["retained_relation"]
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_b3_rejected_source_semantic_relation_difference_is_different() -> None:
    left = _frozen(_qualified_with_local_reject())
    right = _frozen(_local_anomaly_variant())

    left_u = left["qualified_universe"]
    right_u = right["qualified_universe"]
    assert left["qualified_occurrence_count"] == right["qualified_occurrence_count"] == 2

    left_rejected = [
        item
        for item in left_u["source_accounting"]
        if item["disposition"] == "REJECT_RECORD"
    ]
    right_rejected = [
        item
        for item in right_u["source_accounting"]
        if item["disposition"] == "REJECT_RECORD"
    ]
    assert [
        (item["component_manifest_entry_id"], item["component_local_slot_index"])
        for item in left_rejected
    ] == [
        (item["component_manifest_entry_id"], item["component_local_slot_index"])
        for item in right_rejected
    ]
    assert left_rejected[0]["anomaly_class_id"] == "BI5-A09"
    assert right_rejected[0]["anomaly_class_id"] == "BI5-A10"

    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_b3b_anomaly_only_mutation_is_invalid_f_input_not_comparable_semantics() -> None:
    left = _frozen(_qualified_with_local_reject())
    right = copy.deepcopy(left)
    right["qualified_universe"]["anomaly_outcomes"][0]["anomaly_class_id"] = "BI5-A10"
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_b4_component_membership_contradiction_is_not_same_state_semantic_diff() -> None:
    left = _frozen()
    right = _frozen(_qualified_two_component_input())
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_b5_physical_repartition_equivalence_is_not_invented() -> None:
    left = _frozen()
    right = _frozen(_repartitioned_same_payload_bag())
    assert (
        _semantic_projection_for_breaker(left)["payload_bag"]
        == _semantic_projection_for_breaker(right)["payload_bag"]
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


@pytest.mark.parametrize("stage", ("D", "R", "M", "B", "A", "Q", "F"))
def test_c0_same_id_version_different_bound_content_is_integrity_conflict(stage: str) -> None:
    left = _frozen()
    data = _qualified_input()
    binding = next(
        item for item in data["reconstruction_tuple"] if item["stage"] == stage
    )
    binding["integrity_digest"] = "e" * 64
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"
    assert result["reason"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"


@pytest.mark.parametrize("stage", ("D", "R", "M", "B", "A", "Q", "F"))
def test_c0b_same_id_version_different_immutable_reference_is_integrity_conflict(
    stage: str,
) -> None:
    left = _frozen()
    data = _qualified_input()
    binding = next(
        item for item in data["reconstruction_tuple"] if item["stage"] == stage
    )
    binding["immutable_reference"] = f"synthetic://{stage.lower()}/other-content-binding"
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"
    assert result["reason"] == "NORMATIVE_VERSION_INTEGRITY_CONFLICT"


def test_c1_different_qualification_parameters_are_distinct_state() -> None:
    left = _frozen()
    data = _qualified_input()
    data["qualification_parameters"]["semantic_profile"] = "ALTERNATE_LEGITIMATE_PROFILE"
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "DISTINCT_QUALIFICATION_STATE"


def test_c1b_different_valid_d_materialization_version_is_distinct_state() -> None:
    left = _frozen()
    data = _qualified_input()
    data["acquisition_declaration_version"] = "D_MATERIALIZATION_V0_2_SYNTHETIC"
    d = next(item for item in data["reconstruction_tuple"] if item["stage"] == "D")
    d["normative_version"] = "D_MATERIALIZATION_V0_2_SYNTHETIC"
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "DISTINCT_QUALIFICATION_STATE"


@pytest.mark.parametrize(
    "outcome",
    ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"),
)
@pytest.mark.parametrize("side", ("left", "right"))
def test_c2_terminal_f_artifact_blocks_qualified_universe_comparison(
    outcome: str,
    side: str,
) -> None:
    terminal = _terminal(outcome)
    qualified = _frozen()
    left, right = (
        (terminal, qualified)
        if side == "left"
        else (qualified, terminal)
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_c2b_different_acquisition_domain_identity_is_noncomparable() -> None:
    left = _frozen()
    data = _qualified_input()
    data["acquisition_domain_id"] = "SYNTH-F-ACQ-002"
    data["acquisition_snapshot"]["acquisition_domain_id"] = "SYNTH-F-ACQ-002"
    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


@pytest.mark.parametrize(
    "field",
    (
        "completeness_reference",
        "completeness_digest",
        "component_payload_reference",
        "component_payload_digest",
    ),
)
def test_c2c_materialized_acquisition_binding_difference_is_noncomparable(
    field: str,
) -> None:
    left = _frozen()
    data = _qualified_input()

    if field == "completeness_reference":
        data["acquisition_snapshot"]["completeness_evidence"][
            "immutable_reference"
        ] = "synthetic://d/completeness-other"
    elif field == "completeness_digest":
        data["acquisition_snapshot"]["completeness_evidence"][
            "integrity_digest"
        ] = "9" * 64
    elif field == "component_payload_reference":
        data["acquisition_snapshot"]["components"][0][
            "immutable_payload_reference"
        ] = "synthetic://payload/component-001-other"
    else:
        data["acquisition_snapshot"]["components"][0][
            "payload_integrity_reference"
        ] = "8" * 64

    right = _frozen(data)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_c3_equal_terminal_outcomes_still_do_not_create_qualified_comparison() -> None:
    left = _terminal("QUALIFICATION_BLOCKED")
    right = _terminal("QUALIFICATION_BLOCKED")
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"


@pytest.mark.parametrize(
    "mutation",
    (
        "count",
        "integrity",
        "class",
        "freeze_state",
    ),
)
@pytest.mark.parametrize("side", ("left", "right"))
def test_c4_malformed_or_nonfrozen_input_blocks(mutation: str, side: str) -> None:
    valid = _frozen()
    malformed = copy.deepcopy(valid)
    if mutation == "count":
        malformed["qualified_occurrence_count"] += 1
    elif mutation == "integrity":
        malformed["artifact_integrity_digest"] = "0" * 64
    elif mutation == "class":
        malformed["artifact_class"] = "QUALIFICATION_TERMINAL_EVIDENCE"
    else:
        malformed["freeze_state"] = "NOT_CREATED"

    left, right = (
        (malformed, valid)
        if side == "left"
        else (valid, malformed)
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


@pytest.mark.parametrize(
    "mutation",
    (
        "count",
        "missing_determinant",
        "anomaly_accounting",
        "terminal_partial_universe",
    ),
)
@pytest.mark.parametrize("side", ("left", "right"))
def test_c5_resealed_structurally_invalid_f_input_blocks(
    mutation: str,
    side: str,
) -> None:
    valid = _frozen()
    malformed = copy.deepcopy(valid)

    if mutation == "count":
        malformed["qualified_occurrence_count"] += 1
    elif mutation == "missing_determinant":
        malformed["qualified_universe"]["reconstruction_tuple"] = [
            item
            for item in malformed["qualified_universe"]["reconstruction_tuple"]
            if item["stage"] != "Q"
        ]
    elif mutation == "anomaly_accounting":
        data = _qualified_with_local_reject()
        malformed = _frozen(data)
        malformed["qualified_universe"]["anomaly_outcomes"][0][
            "anomaly_class_id"
        ] = "BI5-A10"
    else:
        malformed = _terminal("QUALIFICATION_BLOCKED")
        malformed["qualified_universe"] = {
            "retained_occurrences": [
                copy.deepcopy(valid["qualified_universe"]["retained_occurrences"][0])
            ]
        }
        malformed["qualified_occurrence_count"] = 1

    malformed = _reseal_for_breaker(malformed)
    left, right = (
        (malformed, valid)
        if side == "left"
        else (valid, malformed)
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


@pytest.mark.parametrize("side", ("left", "right"))
@pytest.mark.parametrize("bad_value", (None, [], 7, "not-an-artifact"))
def test_c6_nonmapping_input_blocks(side: str, bad_value: Any) -> None:
    valid = _frozen()
    left, right = (
        (bad_value, valid)
        if side == "left"
        else (valid, bad_value)
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


@pytest.mark.parametrize("reverse", (False, True))
def test_c7_different_terminal_outcomes_never_create_qualified_comparison(
    reverse: bool,
) -> None:
    blocked = _terminal("QUALIFICATION_BLOCKED")
    rejected = _terminal("ACQUISITION_REJECTED")
    left, right = (rejected, blocked) if reverse else (blocked, rejected)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_d0_component_occurrence_accounting_array_order_is_nonsemantic() -> None:
    left = _frozen(_qualified_two_component_input())
    right = _frozen(_same_semantics_permuted_input())
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_d1_anomaly_diagnostic_order_path_and_worker_are_nonsemantic() -> None:
    left_data, right_data = _same_semantics_diagnostic_permutation()
    left = _frozen(left_data)
    right = _frozen(right_data)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_d1b_raw_source_provenance_difference_is_nonsemantic() -> None:
    left_data = _qualified_input()
    right_data = copy.deepcopy(left_data)
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        right_data[relation_name][1]["source_provenance"] = {
            "ask_volume_raw_bits": "80000000"
        }

    left = _frozen(left_data)
    right = _frozen(right_data)
    assert (
        left["qualified_universe"]["retained_occurrences"][1]["logical_payload"]
        == right["qualified_universe"]["retained_occurrences"][1]["logical_payload"]
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert result["qualified_universe_comparison"] == "SEMANTIC_EQUAL"


def test_d2_pretty_compact_byte_hash_difference_is_nonsemantic() -> None:
    artifact = _frozen()
    compact = freeze.serialize_freeze_artifact(artifact, pretty=False)
    pretty = freeze.serialize_freeze_artifact(artifact, pretty=True)
    assert hashlib.sha256(compact).digest() != hashlib.sha256(pretty).digest()
    left = freeze.deserialize_freeze_artifact(compact)
    right = freeze.deserialize_freeze_artifact(pretty)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_d3_object_key_order_is_nonsemantic() -> None:
    data = _qualified_input()
    reversed_data = {
        key: copy.deepcopy(data[key])
        for key in reversed(tuple(data))
    }
    left = _frozen(data)
    right = _frozen(reversed_data)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"


def test_d3b_nested_qualification_parameter_key_order_is_nonsemantic() -> None:
    left_data = _qualified_input()
    right_data = copy.deepcopy(left_data)
    right_data["qualification_parameters"] = {
        key: copy.deepcopy(right_data["qualification_parameters"][key])
        for key in reversed(tuple(right_data["qualification_parameters"]))
    }

    left = _frozen(left_data)
    right = _frozen(right_data)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert result["qualified_universe_comparison"] == "SEMANTIC_EQUAL"


def test_d4_timestamp_array_order_never_creates_temporal_precedence() -> None:
    data = _qualified_input()
    ordered = copy.deepcopy(data)
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        ordered[relation_name].sort(
            key=lambda item: item["logical_payload"]["market_timestamp_utc"]
        )
    left = _frozen(data)
    right = _frozen(ordered)
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_EQUAL"
    assert "temporal_order" not in result
    assert "canonical_sequence" not in result


def test_d5_source_witness_is_not_reported_as_canonical_identity() -> None:
    result = _compare(_frozen(), _frozen())
    forbidden = {
        "canonical_occurrence_id",
        "canonical_record_position",
        "global_row_id",
        "temporal_rank",
        "canonical_sequence",
        "temporal_order",
        "source_witness_identity",
        "ordered_occurrences",
        "sorted_occurrences",
        "sequence_position",
        "source_sequence",
        "chronological_rank",
    }
    assert forbidden.isdisjoint(_recursive_keys(result))


@pytest.mark.parametrize(
    "case",
    ("equal", "different", "conflict"),
)
def test_d6_comparison_semantic_verdict_is_symmetric(case: str) -> None:
    if case == "equal":
        left = _frozen(_qualified_two_component_input())
        right = _frozen(_same_semantics_permuted_input())
    elif case == "different":
        left = _frozen()
        data = _qualified_input()
        _set_payload_field(
            data,
            0,
            "ask_price",
            {"numerator": 100_001, "denominator": 1000},
        )
        right = _frozen(data)
    else:
        left = _frozen()
        data = _qualified_input()
        d = next(item for item in data["reconstruction_tuple"] if item["stage"] == "D")
        d["integrity_digest"] = "e" * 64
        right = _frozen(data)

    forward = _compare(left, right)
    reverse = _compare(right, left)
    assert _semantic_verdict_tuple(forward) == _semantic_verdict_tuple(reverse)


def test_d7_comparator_does_not_mutate_inputs() -> None:
    left = _frozen(_qualified_two_component_input())
    right = _frozen(_same_semantics_permuted_input())
    before_left = copy.deepcopy(left)
    before_right = copy.deepcopy(right)

    result = _o().compare_freeze_artifacts(left, right)
    _assert_result_shape(result)

    assert left == before_left
    assert right == before_right


def test_e0_unqualified_version_mutation_is_not_mislabeled_legitimate_distinct_state() -> None:
    left = _frozen()
    right = copy.deepcopy(left)
    q = next(
        item
        for item in right["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "Q"
    )
    q["normative_version"] = "UNQUALIFIED_SYNTHETIC_Q_V2"
    right = _reseal_for_breaker(right)
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] != "SAME_QUALIFICATION_STATE"
    assert result["reason"]


def test_e1_byte_hash_is_never_the_semantic_oracle() -> None:
    left = _frozen(_qualified_two_component_input())
    right = _frozen(_same_semantics_permuted_input())
    assert left["artifact_integrity_digest"] != right["artifact_integrity_digest"]
    assert _compare(left, right)["oracle_result"] == "SEMANTIC_EQUAL"


def test_e2_permission_closure_and_no_execution_surface() -> None:
    module = _o()
    source = inspect.getsource(module)
    forbidden_tokens = (
        "requests.",
        "httpx.",
        "urllib.request",
        "socket.",
        "MetaTrader5",
        "order_send",
        "run_backtest",
        "download_bi5",
        "build_freeze_artifact(",
    )
    assert all(token not in source for token in forbidden_tokens)
