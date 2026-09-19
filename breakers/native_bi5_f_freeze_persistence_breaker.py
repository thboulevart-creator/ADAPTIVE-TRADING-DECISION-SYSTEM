from __future__ import annotations

import copy
import hashlib
import importlib
import inspect
import json
from collections import Counter
from typing import Any

import pytest


F_MODULE = "src.native_bi5_freeze_persistence"

F_ID = "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE"
F_VERSION = "F_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_QUALIFIED_UNIVERSE_FREEZE_V0_1_CANDIDATE"
ARTIFACT_SCHEMA = "QUALIFICATION_FREEZE_ARTIFACT_V0_1_CANDIDATE"

REQUIRED_DETERMINANTS = {"D", "R", "M", "B", "A", "Q", "F"}


def _f():
    try:
        module = importlib.import_module(F_MODULE)
    except ModuleNotFoundError as exc:
        pytest.fail(
            "F runtime absent — expected pre-implementation RED: "
            "src.native_bi5_freeze_persistence does not exist",
            pytrace=False,
        )
        raise AssertionError from exc

    required = (
        "build_freeze_artifact",
        "validate_freeze_artifact",
        "serialize_freeze_artifact",
        "deserialize_freeze_artifact",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"F runtime surface incomplete: {missing}", pytrace=False)

    assert getattr(module, "FREEZE_CONTRACT_ID", None) == F_ID
    assert getattr(module, "FREEZE_CONTRACT_VERSION", None) == F_VERSION
    assert getattr(module, "ARTIFACT_SCHEMA", None) == ARTIFACT_SCHEMA
    return module


@pytest.fixture(autouse=True)
def _runtime_must_exist():
    _f()


def _digest(char: str) -> str:
    return char * 64


def _binding(
    stage: str,
    normative_id: str,
    normative_version: str,
    char: str,
) -> dict[str, Any]:
    return {
        "stage": stage,
        "normative_id": normative_id,
        "normative_version": normative_version,
        "immutable_reference": f"synthetic://{stage.lower()}/v1",
        "integrity_digest": _digest(char),
    }


def _reconstruction_tuple() -> list[dict[str, Any]]:
    return [
        _binding(
            "D",
            "D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1",
            "D_MATERIALIZATION_V0_1_SYNTHETIC",
            "d",
        ),
        _binding(
            "R",
            "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS",
            "DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE",
            "1",
        ),
        _binding(
            "M",
            "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL",
            "PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE",
            "2",
        ),
        _binding(
            "B",
            "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
            "B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "3",
        ),
        _binding(
            "A",
            "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD",
            "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "4",
        ),
        _binding(
            "Q",
            "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP",
            "Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE",
            "5",
        ),
        _binding("F", F_ID, F_VERSION, "6"),
    ]


def _component_snapshot(complete_slot_count: int = 3) -> dict[str, Any]:
    return {
        "component_manifest_entry_id": "SYNTH-F-COMP-001",
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
        "instrument_source_identity": "DUKASCOPY/USATECHIDXUSD",
        "declared_hour_bucket_utc": "2026-01-02T10:00:00Z",
        "immutable_payload_reference": "synthetic://payload/component-001",
        "payload_integrity_reference": _digest("a"),
        "materialization_status": "MATERIALIZED",
        "complete_slot_count": complete_slot_count,
        "terminal_fragment": None,
    }


def _logical_payload(
    timestamp: str,
    ask: int,
    bid: int,
    ask_volume: tuple[int, int],
    bid_volume: tuple[int, int],
) -> dict[str, Any]:
    return {
        "market_timestamp_utc": timestamp,
        "ask_price": {"numerator": ask, "denominator": 1000},
        "bid_price": {"numerator": bid, "denominator": 1000},
        "ask_volume": {
            "integer_coefficient": ask_volume[0],
            "exponent2": ask_volume[1],
        },
        "bid_volume": {
            "integer_coefficient": bid_volume[0],
            "exponent2": bid_volume[1],
        },
    }


def _occurrence(
    slot: int,
    payload: dict[str, Any],
    *,
    raw_volume_bits: str | None = None,
) -> dict[str, Any]:
    result = {
        "logical_payload": copy.deepcopy(payload),
        "source_witness": {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": slot,
        },
    }
    if raw_volume_bits is not None:
        result["source_provenance"] = {
            "ask_volume_raw_bits": raw_volume_bits,
        }
    return result


def _qualified_input() -> dict[str, Any]:
    p0 = _logical_payload(
        "2026-01-02T10:00:02.000Z",
        100_000,
        100_100,
        (-3, -1),
        (1, 1),
    )
    duplicated = _logical_payload(
        "2026-01-02T10:00:01.000Z",
        0,
        99_999,
        (0, 0),
        (0, 0),
    )
    occurrences = [
        _occurrence(0, p0),
        _occurrence(1, duplicated, raw_volume_bits="00000000"),
        _occurrence(2, duplicated, raw_volume_bits="80000000"),
    ]
    accounting = [
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": i,
            "disposition": "CANDIDATE_RETAINED",
            "anomaly_class_id": None,
        }
        for i in range(3)
    ]
    return {
        "schema": "SYNTHETIC_F_CONSTRUCTION_INPUT_V0_1",
        "qualification_outcome": "QUALIFIED",
        "acquisition_domain_id": "SYNTH-F-ACQ-001",
        "acquisition_declaration_version": "D_MATERIALIZATION_V0_1_SYNTHETIC",
        "reconstruction_tuple": _reconstruction_tuple(),
        "qualification_parameters": {
            "market_value_filter": "NONE",
            "temporal_order_authority": "NONE",
        },
        "acquisition_snapshot": {
            "acquisition_domain_id": "SYNTH-F-ACQ-001",
            "completeness_evidence": {
                "immutable_reference": "synthetic://d/completeness",
                "integrity_digest": _digest("b"),
            },
            "components": [_component_snapshot()],
        },
        "source_accounting": accounting,
        "b_candidate_occurrences": copy.deepcopy(occurrences),
        "anomaly_outcomes": [],
        "retained_occurrences": occurrences,
        "rejection_diagnostics": [],
    }


def _qualified_with_local_reject() -> dict[str, Any]:
    data = _qualified_input()
    data["retained_occurrences"] = data["retained_occurrences"][:2]
    data["b_candidate_occurrences"] = copy.deepcopy(data["retained_occurrences"])
    data["source_accounting"][2] = {
        "component_manifest_entry_id": "SYNTH-F-COMP-001",
        "component_local_slot_index": 2,
        "disposition": "REJECT_RECORD",
        "anomaly_class_id": "BI5-A09",
    }
    data["anomaly_outcomes"] = [
        {
            "anomaly_class_id": "BI5-A09",
            "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
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


def _qualified_two_component_input() -> dict[str, Any]:
    data = _qualified_input()
    second_component = {
        "component_manifest_entry_id": "SYNTH-F-COMP-002",
        "declared_role": "HOURLY_NATIVE_BI5_TICKS",
        "instrument_source_identity": "DUKASCOPY/USATECHIDXUSD",
        "declared_hour_bucket_utc": "2026-01-02T11:00:00Z",
        "immutable_payload_reference": "synthetic://payload/component-002",
        "payload_integrity_reference": _digest("c"),
        "materialization_status": "MATERIALIZED",
        "complete_slot_count": 1,
        "terminal_fragment": None,
    }
    payload = _logical_payload(
        "2026-01-02T11:00:00.500Z",
        100_500,
        100_400,
        (1, 0),
        (3, -1),
    )
    occurrence = {
        "logical_payload": payload,
        "source_witness": {
            "component_manifest_entry_id": "SYNTH-F-COMP-002",
            "component_local_slot_index": 0,
        },
    }
    data["acquisition_snapshot"]["components"].append(second_component)
    data["source_accounting"].append(
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-002",
            "component_local_slot_index": 0,
            "disposition": "CANDIDATE_RETAINED",
            "anomaly_class_id": None,
        }
    )
    data["b_candidate_occurrences"].append(copy.deepcopy(occurrence))
    data["retained_occurrences"].append(occurrence)
    return data


def _qualified_with_two_local_rejects() -> dict[str, Any]:
    data = _qualified_input()
    component = data["acquisition_snapshot"]["components"][0]
    component["complete_slot_count"] = 4

    retained0 = copy.deepcopy(data["retained_occurrences"][0])
    retained3 = _occurrence(
        3,
        _logical_payload(
            "2026-01-02T10:00:03.000Z",
            100_300,
            100_200,
            (1, 0),
            (1, 0),
        ),
    )
    data["retained_occurrences"] = [retained0, retained3]
    data["b_candidate_occurrences"] = copy.deepcopy(data["retained_occurrences"])
    data["source_accounting"] = [
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": 0,
            "disposition": "CANDIDATE_RETAINED",
            "anomaly_class_id": None,
        },
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": 1,
            "disposition": "REJECT_RECORD",
            "anomaly_class_id": "BI5-A09",
        },
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": 2,
            "disposition": "REJECT_RECORD",
            "anomaly_class_id": "BI5-A10",
        },
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": 3,
            "disposition": "CANDIDATE_RETAINED",
            "anomaly_class_id": None,
        },
    ]
    data["anomaly_outcomes"] = [
        {
            "anomaly_class_id": "BI5-A09",
            "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "target": {
                "target_scope": "COMPLETE_SLOT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
                "component_local_slot_index": 1,
            },
            "mandatory_outcome": "REJECT_RECORD",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
            "diagnostic_path": "synthetic://diagnostic/a09",
        },
        {
            "anomaly_class_id": "BI5-A10",
            "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "target": {
                "target_scope": "COMPLETE_SLOT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
                "component_local_slot_index": 2,
            },
            "mandatory_outcome": "REJECT_RECORD",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
            "diagnostic_path": "synthetic://diagnostic/a10",
        },
    ]
    return data


def _a08_without_evidence_input() -> dict[str, Any]:
    data = _qualified_input()
    component = data["acquisition_snapshot"]["components"][0]
    component["complete_slot_count"] = 2
    component["terminal_fragment"] = {
        "terminal_fragment_start_offset": 40,
        "terminal_fragment_length": 7,
        "remainder_reference": "synthetic://fragment/a08",
    }
    data["retained_occurrences"] = data["retained_occurrences"][:2]
    data["b_candidate_occurrences"] = copy.deepcopy(data["retained_occurrences"])
    data["source_accounting"] = data["source_accounting"][:2]
    data["anomaly_outcomes"] = [
        {
            "anomaly_class_id": "BI5-A08",
            "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "target": {
                "target_scope": "TERMINAL_FRAGMENT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
                "terminal_fragment_start_offset": 40,
                "terminal_fragment_length": 7,
            },
            "mandatory_outcome": "REJECT_RECORD",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
        }
    ]
    return data


def _terminal_input(outcome: str) -> dict[str, Any]:
    data = _qualified_input()
    data["qualification_outcome"] = outcome
    data["retained_occurrences"] = []
    data["b_candidate_occurrences"] = []
    data["source_accounting"] = []
    data["anomaly_outcomes"] = [
        {
            "anomaly_class_id": "BI5-A06",
            "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
            "target": {
                "target_scope": "COMPONENT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
            },
            "mandatory_outcome": (
                "QUALIFICATION_BLOCKED"
                if outcome == "QUALIFICATION_BLOCKED"
                else "REJECT_ACQUISITION"
            ),
            "acquisition_fatal": outcome == "ACQUISITION_REJECTED",
            "qualification_evidence_bindings": [],
        }
    ]
    return data


def _build(data: dict[str, Any]):
    return _f().build_freeze_artifact(copy.deepcopy(data))


def _payload_counter(artifact: Mapping[str, Any]) -> Counter:
    universe = artifact["qualified_universe"]
    return Counter(
        json.dumps(
            item["logical_payload"],
            sort_keys=True,
            separators=(",", ":"),
        )
        for item in universe["retained_occurrences"]
    )


def _witness_map(artifact: Mapping[str, Any]) -> dict[tuple[str, int], str]:
    universe = artifact["qualified_universe"]
    return {
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
        ): item["disposition"]
        for item in universe["source_accounting"]
    }


def _semantic_anomaly(item: Mapping[str, Any]) -> str:
    semantic = {
        "anomaly_class_id": item["anomaly_class_id"],
        "anomaly_matrix_version": item["anomaly_matrix_version"],
        "target": item["target"],
        "mandatory_outcome": item["mandatory_outcome"],
        "acquisition_fatal": item["acquisition_fatal"],
        "qualification_evidence_bindings": item.get(
            "qualification_evidence_bindings", []
        ),
    }
    return json.dumps(semantic, sort_keys=True, separators=(",", ":"))


def _artifact_semantic_projection(artifact: Mapping[str, Any]) -> dict[str, Any]:
    assert artifact["artifact_class"] == "QUALIFIED_UNIVERSE_FREEZE"
    universe = artifact["qualified_universe"]

    reconstruction = sorted(
        (
            item["stage"],
            item["normative_id"],
            item["normative_version"],
            item["immutable_reference"],
            item["integrity_digest"],
        )
        for item in universe["reconstruction_tuple"]
    )
    components = sorted(
        json.dumps(item, sort_keys=True, separators=(",", ":"))
        for item in universe["components"]
    )
    accounting = sorted(
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
            item["disposition"],
            item.get("anomaly_class_id"),
        )
        for item in universe["source_accounting"]
    )
    anomalies = sorted(
        _semantic_anomaly(item)
        for item in universe["anomaly_outcomes"]
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
    payload_bag = sorted(_payload_counter(artifact).items())

    return {
        "freeze_contract_id": artifact["freeze_contract_id"],
        "freeze_contract_version": artifact["freeze_contract_version"],
        "qualification_outcome": artifact["qualification_outcome"],
        "qualified_occurrence_count": artifact["qualified_occurrence_count"],
        "acquisition_domain_id": universe["acquisition_domain_id"],
        "acquisition_declaration_version": universe["acquisition_declaration_version"],
        "qualification_parameters": universe["qualification_parameters"],
        "completeness_evidence": universe["completeness_evidence"],
        "reconstruction_tuple": reconstruction,
        "components": components,
        "source_accounting": accounting,
        "anomaly_outcomes": anomalies,
        "retained_relation": retained_relation,
        "payload_bag": payload_bag,
    }


def _reverse_object_keys(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _reverse_object_keys(value[key])
            for key in reversed(tuple(value))
        }
    if isinstance(value, list):
        return [_reverse_object_keys(item) for item in value]
    return value


def test_a0_surface_is_f_only_and_no_oracle_api() -> None:
    module = _f()
    assert inspect.signature(module.build_freeze_artifact).parameters.keys() == {
        "freeze_input"
    }
    sig = inspect.signature(module.serialize_freeze_artifact)
    assert tuple(sig.parameters) == ("artifact", "pretty")
    assert sig.parameters["pretty"].kind is inspect.Parameter.KEYWORD_ONLY
    forbidden = (
        "compare_freezes",
        "semantic_equal",
        "oracle_compare",
        "compare_semantic_universes",
    )
    assert all(not hasattr(module, name) for name in forbidden)


def test_a1_qualified_q_creates_complete_reconstructible_frozen_artifact() -> None:
    source = _qualified_input()
    artifact = _build(source)
    assert artifact["schema"] == ARTIFACT_SCHEMA
    assert artifact["freeze_contract_id"] == F_ID
    assert artifact["freeze_contract_version"] == F_VERSION
    assert artifact["artifact_class"] == "QUALIFIED_UNIVERSE_FREEZE"
    assert artifact["freeze_state"] == "FROZEN"
    assert artifact["qualification_outcome"] == "QUALIFIED"
    assert artifact["qualified_universe"] is not None
    assert artifact["qualified_occurrence_count"] == 3

    universe = artifact["qualified_universe"]
    assert universe["acquisition_domain_id"] == source["acquisition_domain_id"]
    assert (
        universe["acquisition_declaration_version"]
        == source["acquisition_declaration_version"]
    )
    assert universe["qualification_parameters"] == source["qualification_parameters"]
    assert (
        universe["completeness_evidence"]
        == source["acquisition_snapshot"]["completeness_evidence"]
    )
    assert {
        item["stage"] for item in universe["reconstruction_tuple"]
    } == REQUIRED_DETERMINANTS
    assert sorted(
        item["component_manifest_entry_id"] for item in universe["components"]
    ) == sorted(
        item["component_manifest_entry_id"]
        for item in source["acquisition_snapshot"]["components"]
    )
    assert _witness_map(artifact) == {
        (
            item["component_manifest_entry_id"],
            item["component_local_slot_index"],
        ): item["disposition"]
        for item in source["source_accounting"]
    }
    assert sorted(
        _semantic_anomaly(item) for item in universe["anomaly_outcomes"]
    ) == sorted(
        _semantic_anomaly(item) for item in source["anomaly_outcomes"]
    )
    _f().validate_freeze_artifact(artifact)


@pytest.mark.parametrize(
    "outcome",
    ("QUALIFICATION_BLOCKED", "ACQUISITION_REJECTED"),
)
def test_a2_nonqualified_q_emits_terminal_nonfreeze_only(outcome: str) -> None:
    artifact = _build(_terminal_input(outcome))
    assert artifact["artifact_class"] == "QUALIFICATION_TERMINAL_EVIDENCE"
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualification_outcome"] == outcome
    assert artifact["qualified_universe"] is None
    assert artifact["qualified_occurrence_count"] is None
    assert not artifact.get("freeze_id")
    assert artifact.get("terminal_evidence") is not None
    assert artifact["terminal_evidence"]["qualification_outcome"] == outcome
    _f().validate_freeze_artifact(artifact)


def test_a3_nonqualified_prefix_cannot_escape_as_normative_universe() -> None:
    data = _terminal_input("QUALIFICATION_BLOCKED")
    data["retained_occurrences"] = _qualified_input()["retained_occurrences"][:1]
    data["source_accounting"] = _qualified_input()["source_accounting"][:1]
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None
    assert artifact["qualified_occurrence_count"] is None


@pytest.mark.parametrize("stage", sorted(REQUIRED_DETERMINANTS))
def test_b0_missing_reconstruction_determinant_prevents_freeze(stage: str) -> None:
    data = _qualified_input()
    data["reconstruction_tuple"] = [
        item for item in data["reconstruction_tuple"] if item["stage"] != stage
    ]
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["artifact_class"] == "QUALIFICATION_TERMINAL_EVIDENCE"
    assert artifact["qualified_universe"] is None


def test_b0b_missing_b_candidate_relation_prevents_freeze() -> None:
    data = _qualified_input()
    del data["b_candidate_occurrences"]
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_b1_same_id_version_conflicting_content_prevents_freeze() -> None:
    data = _qualified_input()
    b = next(item for item in data["reconstruction_tuple"] if item["stage"] == "B")
    conflict = copy.deepcopy(b)
    conflict["integrity_digest"] = _digest("c")
    data["reconstruction_tuple"].append(conflict)
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_b2_accounting_gap_prevents_freeze() -> None:
    data = _qualified_input()
    data["source_accounting"].pop()
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_b3_candidate_reject_overlap_prevents_freeze() -> None:
    data = _qualified_with_local_reject()
    data["retained_occurrences"].append(
        _occurrence(
            2,
            _logical_payload(
                "2026-01-02T10:00:03.000Z",
                100_200,
                100_100,
                (1, 0),
                (1, 0),
            ),
        )
    )
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"


def test_b4_terminal_fragment_never_enters_complete_slot_accounting() -> None:
    data = _qualified_input()
    data["acquisition_snapshot"]["components"][0]["terminal_fragment"] = {
        "terminal_fragment_start_offset": 60,
        "terminal_fragment_length": 7,
        "disposition": "REJECT_RECORD",
    }
    data["source_accounting"].append(
        {
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "component_local_slot_index": 3,
            "disposition": "REJECT_RECORD",
            "anomaly_class_id": "BI5-A08",
        }
    )
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"


def test_b5_anomaly_relation_cannot_be_dropped() -> None:
    data = _qualified_with_local_reject()
    artifact = _build(data)
    assert artifact["freeze_state"] == "FROZEN"
    assert artifact["qualified_universe"]["anomaly_outcomes"] == data["anomaly_outcomes"]

    corrupted = copy.deepcopy(artifact)
    corrupted["qualified_universe"]["anomaly_outcomes"] = []
    with pytest.raises((TypeError, ValueError)):
        _f().validate_freeze_artifact(corrupted)


def test_b6_a08_without_exact_evidence_binding_cannot_freeze() -> None:
    data = _a08_without_evidence_input()
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_c0_every_retained_occurrence_persisted_exactly_once() -> None:
    source = _qualified_input()
    artifact = _build(source)
    universe = artifact["qualified_universe"]
    assert len(universe["retained_occurrences"]) == 3
    witnesses = [
        (
            item["source_witness"]["component_manifest_entry_id"],
            item["source_witness"]["component_local_slot_index"],
        )
        for item in universe["retained_occurrences"]
    ]
    assert len(witnesses) == len(set(witnesses)) == 3
    expected = {
        (
            item["source_witness"]["component_manifest_entry_id"],
            item["source_witness"]["component_local_slot_index"],
        ): item["logical_payload"]
        for item in source["b_candidate_occurrences"]
    }
    frozen = {
        (
            item["source_witness"]["component_manifest_entry_id"],
            item["source_witness"]["component_local_slot_index"],
        ): item["logical_payload"]
        for item in universe["retained_occurrences"]
    }
    assert frozen == expected


def test_c1_strict_duplicate_multiplicity_survives_freeze() -> None:
    artifact = _build(_qualified_input())
    payloads = _payload_counter(artifact)
    assert max(payloads.values()) == 2
    assert artifact["qualified_occurrence_count"] == 3


def test_c2_nonunique_binary32_normal_form_prevents_freeze() -> None:
    data = _qualified_input()
    volume = data["retained_occurrences"][0]["logical_payload"]["ask_volume"]
    volume["integer_coefficient"] = -6
    volume["exponent2"] = -2
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"


def test_c3_signed_zero_source_bits_do_not_create_distinct_logical_zero() -> None:
    artifact = _build(_qualified_input())
    occurrences = artifact["qualified_universe"]["retained_occurrences"]
    by_slot = {
        item["source_witness"]["component_local_slot_index"]: item
        for item in occurrences
    }
    assert by_slot[1]["logical_payload"] == by_slot[2]["logical_payload"]
    assert by_slot[1]["source_witness"] != by_slot[2]["source_witness"]


def test_c4_source_to_logical_corruption_cannot_hide_behind_equal_payload_bag() -> None:
    data = _qualified_input()
    data["retained_occurrences"][0]["source_witness"], data["retained_occurrences"][1]["source_witness"] = (
        data["retained_occurrences"][1]["source_witness"],
        data["retained_occurrences"][0]["source_witness"],
    )
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_c5_source_witness_is_not_promoted_to_canonical_occurrence_identity() -> None:
    artifact = _build(_qualified_input())
    forbidden = {
        "occurrence_id",
        "canonical_occurrence_id",
        "global_row_id",
        "canonical_position",
        "temporal_rank",
    }
    for occurrence in artifact["qualified_universe"]["retained_occurrences"]:
        assert forbidden.isdisjoint(occurrence)
        assert set(occurrence).issubset(
            {"logical_payload", "source_witness", "source_provenance"}
        )


def test_d0_component_accounting_and_occurrence_array_order_is_nonsemantic() -> None:
    original_input = _qualified_two_component_input()
    permuted_input = copy.deepcopy(original_input)
    permuted_input["acquisition_snapshot"]["components"].reverse()
    permuted_input["source_accounting"].reverse()
    permuted_input["b_candidate_occurrences"].reverse()
    permuted_input["retained_occurrences"].reverse()

    first = _build(original_input)
    second = _build(permuted_input)
    assert first["freeze_state"] == second["freeze_state"] == "FROZEN"
    assert _artifact_semantic_projection(first) == _artifact_semantic_projection(second)


def test_d0b_anomaly_array_order_and_diagnostic_path_are_nonsemantic() -> None:
    original_input = _qualified_with_two_local_rejects()
    permuted_input = copy.deepcopy(original_input)
    permuted_input["anomaly_outcomes"].reverse()
    for index, item in enumerate(permuted_input["anomaly_outcomes"]):
        item["diagnostic_path"] = f"synthetic://different-path/{index}"

    first = _build(original_input)
    second = _build(permuted_input)
    assert first["freeze_state"] == second["freeze_state"] == "FROZEN"
    assert _artifact_semantic_projection(first) == _artifact_semantic_projection(second)


def test_d1_json_whitespace_and_key_order_do_not_define_semantic_identity() -> None:
    artifact = _build(_qualified_input())
    compact = _f().serialize_freeze_artifact(artifact, pretty=False)
    pretty = _f().serialize_freeze_artifact(artifact, pretty=True)
    reversed_keys = json.dumps(
        _reverse_object_keys(artifact),
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    assert isinstance(compact, bytes)
    assert isinstance(pretty, bytes)
    assert compact != pretty
    assert hashlib.sha256(compact).hexdigest() != hashlib.sha256(pretty).hexdigest()

    decoded_compact = _f().deserialize_freeze_artifact(compact)
    decoded_pretty = _f().deserialize_freeze_artifact(pretty)
    decoded_reversed = _f().deserialize_freeze_artifact(reversed_keys)
    for decoded in (decoded_compact, decoded_pretty, decoded_reversed):
        _f().validate_freeze_artifact(decoded)
        assert _artifact_semantic_projection(decoded) == _artifact_semantic_projection(
            artifact
        )


def test_d2_timestamp_array_order_does_not_create_temporal_authority() -> None:
    original_input = _qualified_input()
    permuted_input = copy.deepcopy(original_input)
    permuted_input["retained_occurrences"].sort(
        key=lambda item: item["logical_payload"]["market_timestamp_utc"],
    )
    permuted_input["b_candidate_occurrences"].sort(
        key=lambda item: item["logical_payload"]["market_timestamp_utc"],
    )

    first = _build(original_input)
    second = _build(permuted_input)
    assert first["freeze_state"] == second["freeze_state"] == "FROZEN"
    assert _artifact_semantic_projection(first) == _artifact_semantic_projection(second)
    for artifact in (first, second):
        for item in artifact["qualified_universe"]["retained_occurrences"]:
            assert "temporal_rank" not in item
            assert "sequence_position" not in item


def test_d3_byte_hash_is_integrity_only_not_semantic_identity() -> None:
    artifact = _build(_qualified_input())
    compact = _f().serialize_freeze_artifact(artifact, pretty=False)
    pretty = _f().serialize_freeze_artifact(artifact, pretty=True)
    assert hashlib.sha256(compact).digest() != hashlib.sha256(pretty).digest()
    assert _f().deserialize_freeze_artifact(compact) == _f().deserialize_freeze_artifact(pretty)


def test_d4_missing_d_completeness_evidence_prevents_freeze() -> None:
    data = _qualified_input()
    del data["acquisition_snapshot"]["completeness_evidence"]
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_d5_nonmaterialized_declared_component_prevents_freeze() -> None:
    data = _qualified_input()
    data["acquisition_snapshot"]["components"][0]["materialization_status"] = "MISSING"
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_d6_missing_qualification_parameters_prevents_freeze() -> None:
    data = _qualified_input()
    del data["qualification_parameters"]
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_e0_changed_determinant_content_cannot_reuse_old_reconstruction_binding() -> None:
    first = _build(_qualified_input())
    changed_input = _qualified_input()
    d = next(
        item for item in changed_input["reconstruction_tuple"] if item["stage"] == "D"
    )
    d["integrity_digest"] = _digest("e")
    second = _build(changed_input)
    first_d = next(
        item for item in first["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "D"
    )
    second_d = next(
        item for item in second["qualified_universe"]["reconstruction_tuple"]
        if item["stage"] == "D"
    )
    assert first_d["integrity_digest"] != second_d["integrity_digest"]


def test_e1_malformed_f_construction_never_validates_as_frozen() -> None:
    artifact = _build(_qualified_input())
    malformed = copy.deepcopy(artifact)
    malformed["qualified_occurrence_count"] += 1
    with pytest.raises((TypeError, ValueError)):
        _f().validate_freeze_artifact(malformed)


def test_e2_permission_closure_and_no_external_execution_surface() -> None:
    module = _f()
    source = inspect.getsource(module)
    forbidden_attrs = (
        "download_bi5",
        "run_backtest",
        "authorize",
        "activate_live",
        "order_send",
        "compare_semantic_universes",
    )
    assert all(not hasattr(module, name) for name in forbidden_attrs)
    forbidden_tokens = (
        "requests.",
        "httpx.",
        "urllib.request",
        "socket.",
        "MetaTrader5",
        "order_send",
        "run_backtest",
        "download_bi5",
    )
    assert all(token not in source for token in forbidden_tokens)
