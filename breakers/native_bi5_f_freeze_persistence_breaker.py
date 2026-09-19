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
        "anomaly_outcomes": [],
        "retained_occurrences": occurrences,
        "rejection_diagnostics": [],
    }


def _qualified_with_local_reject() -> dict[str, Any]:
    data = _qualified_input()
    data["retained_occurrences"] = data["retained_occurrences"][:2]
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


def _terminal_input(outcome: str) -> dict[str, Any]:
    data = _qualified_input()
    data["qualification_outcome"] = outcome
    data["retained_occurrences"] = []
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


def test_a1_qualified_q_creates_only_qualified_frozen_artifact() -> None:
    artifact = _build(_qualified_input())
    assert artifact["schema"] == ARTIFACT_SCHEMA
    assert artifact["freeze_contract_id"] == F_ID
    assert artifact["freeze_contract_version"] == F_VERSION
    assert artifact["artifact_class"] == "QUALIFIED_UNIVERSE_FREEZE"
    assert artifact["freeze_state"] == "FROZEN"
    assert artifact["qualification_outcome"] == "QUALIFIED"
    assert artifact["qualified_universe"] is not None
    assert artifact["qualified_occurrence_count"] == 3
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
    data = _qualified_with_local_reject()
    data["source_accounting"][2]["anomaly_class_id"] = "BI5-A08"
    data["anomaly_outcomes"][0] = {
        "anomaly_class_id": "BI5-A08",
        "anomaly_matrix_version": "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE",
        "target": {
            "target_scope": "TERMINAL_FRAGMENT",
            "component_manifest_entry_id": "SYNTH-F-COMP-001",
            "terminal_fragment_start_offset": 60,
            "terminal_fragment_length": 7,
        },
        "mandatory_outcome": "REJECT_RECORD",
        "acquisition_fatal": False,
        "qualification_evidence_bindings": [],
    }
    artifact = _build(data)
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None


def test_c0_every_retained_occurrence_persisted_exactly_once() -> None:
    artifact = _build(_qualified_input())
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
    artifact = _build(_qualified_input())
    corrupted = copy.deepcopy(artifact)
    occurrences = corrupted["qualified_universe"]["retained_occurrences"]
    occurrences[0]["source_witness"], occurrences[1]["source_witness"] = (
        occurrences[1]["source_witness"],
        occurrences[0]["source_witness"],
    )
    with pytest.raises((TypeError, ValueError)):
        _f().validate_freeze_artifact(corrupted)


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


def test_d0_array_order_is_nonsemantic_for_validation() -> None:
    artifact = _build(_qualified_with_local_reject())
    reordered = copy.deepcopy(artifact)
    universe = reordered["qualified_universe"]
    universe["components"].reverse()
    universe["source_accounting"].reverse()
    universe["anomaly_outcomes"].reverse()
    universe["retained_occurrences"].reverse()
    _f().validate_freeze_artifact(reordered)


def test_d1_json_whitespace_and_key_order_do_not_define_semantic_identity() -> None:
    artifact = _build(_qualified_input())
    compact = _f().serialize_freeze_artifact(artifact, pretty=False)
    pretty = _f().serialize_freeze_artifact(artifact, pretty=True)
    assert isinstance(compact, bytes)
    assert isinstance(pretty, bytes)
    assert compact != pretty
    assert hashlib.sha256(compact).hexdigest() != hashlib.sha256(pretty).hexdigest()
    decoded_compact = _f().deserialize_freeze_artifact(compact)
    decoded_pretty = _f().deserialize_freeze_artifact(pretty)
    _f().validate_freeze_artifact(decoded_compact)
    _f().validate_freeze_artifact(decoded_pretty)
    assert decoded_compact == decoded_pretty == artifact


def test_d2_timestamp_regression_does_not_create_temporal_authority() -> None:
    artifact = _build(_qualified_input())
    assert artifact["freeze_state"] == "FROZEN"
    timestamps = [
        item["logical_payload"]["market_timestamp_utc"]
        for item in artifact["qualified_universe"]["retained_occurrences"]
    ]
    assert timestamps[0] > timestamps[1]
    for item in artifact["qualified_universe"]["retained_occurrences"]:
        assert "temporal_rank" not in item
        assert "sequence_position" not in item


def test_d3_byte_hash_is_integrity_only_not_semantic_identity() -> None:
    artifact = _build(_qualified_input())
    compact = _f().serialize_freeze_artifact(artifact, pretty=False)
    pretty = _f().serialize_freeze_artifact(artifact, pretty=True)
    assert hashlib.sha256(compact).digest() != hashlib.sha256(pretty).digest()
    assert _f().deserialize_freeze_artifact(compact) == _f().deserialize_freeze_artifact(pretty)


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
