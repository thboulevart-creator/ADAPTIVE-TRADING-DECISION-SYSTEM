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


def _compare(left: Mapping[str, Any], right: Mapping[str, Any]) -> Mapping[str, Any]:
    result = _o().compare_freeze_artifacts(
        copy.deepcopy(left),
        copy.deepcopy(right),
    )
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


def test_b3_anomaly_semantic_relation_difference_is_different() -> None:
    left = _frozen(_qualified_input())
    right = _frozen(_local_anomaly_variant())
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_b4_component_membership_difference_is_semantic_different() -> None:
    left = _frozen()
    right = _frozen(_qualified_two_component_input())
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_b5_physical_repartition_equivalence_is_not_invented() -> None:
    left = _frozen()
    right = _frozen(_repartitioned_same_payload_bag())
    assert (
        _semantic_projection_for_breaker(left)["payload_bag"]
        == _semantic_projection_for_breaker(right)["payload_bag"]
    )
    result = _compare(left, right)
    assert result["oracle_result"] == "SEMANTIC_DIFFERENT"


def test_c0_same_id_version_different_bound_content_is_integrity_conflict() -> None:
    left = _frozen()
    data = _qualified_input()
    d = next(item for item in data["reconstruction_tuple"] if item["stage"] == "D")
    d["integrity_digest"] = "e" * 64
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


@pytest.mark.parametrize(
    "outcome",
    ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"),
)
def test_c2_terminal_f_artifact_blocks_qualified_universe_comparison(outcome: str) -> None:
    terminal = _terminal(outcome)
    result = _compare(_frozen(), terminal)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "TERMINAL_INPUT"


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
def test_c4_malformed_or_nonfrozen_input_blocks(mutation: str) -> None:
    left = _frozen()
    right = copy.deepcopy(left)
    if mutation == "count":
        right["qualified_occurrence_count"] += 1
    elif mutation == "integrity":
        right["artifact_integrity_digest"] = "0" * 64
    elif mutation == "class":
        right["artifact_class"] = "QUALIFICATION_TERMINAL_EVIDENCE"
    else:
        right["freeze_state"] = "NOT_CREATED"

    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["qualified_universe_comparison"] == "BLOCKED"
    assert result["comparison_scope"] == "INVALID_F_INPUT"


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
    }
    assert forbidden.isdisjoint(result)


def test_e0_unqualified_version_mutation_is_not_mislabeled_legitimate_distinct_state() -> None:
    left = _frozen()
    right = copy.deepcopy(left)
    q = next(
        item
        for item in right["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "Q"
    )
    q["normative_version"] = "UNQUALIFIED_SYNTHETIC_Q_V2"
    result = _compare(left, right)
    assert result["oracle_result"] == "BLOCKED"
    assert result["comparison_scope"] == "INVALID_F_INPUT"


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
