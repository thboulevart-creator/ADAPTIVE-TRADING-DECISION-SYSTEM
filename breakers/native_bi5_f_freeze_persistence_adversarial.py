from __future__ import annotations

import copy

import pytest

from breakers.native_bi5_f_freeze_persistence_breaker import (
    _a08_without_evidence_input,
    _qualified_input,
    _qualified_with_local_reject,
)
from src import native_bi5_freeze_persistence as f


def _assert_not_frozen(data) -> None:
    artifact = f.build_freeze_artifact(copy.deepcopy(data))
    assert artifact["artifact_class"] == "QUALIFICATION_TERMINAL_EVIDENCE"
    assert artifact["freeze_state"] == "NOT_CREATED"
    assert artifact["qualified_universe"] is None
    assert artifact["qualified_occurrence_count"] is None


def _set_slot0_field(data, field, value) -> None:
    for relation_name in ("b_candidate_occurrences", "retained_occurrences"):
        data[relation_name][0]["logical_payload"][field] = copy.deepcopy(value)


def test_adv_a08_shape_only_binding_cannot_promote_unqualified_proof() -> None:
    data = _a08_without_evidence_input()
    target = copy.deepcopy(data["anomaly_outcomes"][0]["target"])
    data["anomaly_outcomes"][0]["qualification_evidence_bindings"] = [
        {
            "evidence_role": "CONSTRUCTIVE_COMPLETENESS_PROOF",
            "immutable_reference": "synthetic://self-described-proof",
            "integrity_digest_or_reference": "synthetic://self-described-digest",
            "exact_anomaly_target_binding": target,
        }
    ]
    _assert_not_frozen(data)


def test_adv_qualified_state_cannot_contain_blocking_anomaly() -> None:
    data = _qualified_input()
    data["anomaly_outcomes"].append(
        {
            "anomaly_class_id": "BI5-A06",
            "anomaly_matrix_version": (
                "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
            ),
            "target": {
                "target_scope": "COMPONENT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
            },
            "mandatory_outcome": "QUALIFICATION_BLOCKED",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
        }
    )
    _assert_not_frozen(data)


def test_adv_a13_cannot_be_recast_as_local_record_rejection() -> None:
    data = _qualified_with_local_reject()
    data["source_accounting"][2]["anomaly_class_id"] = "BI5-A13"
    data["anomaly_outcomes"][0]["anomaly_class_id"] = "BI5-A13"
    data["anomaly_outcomes"][0]["mandatory_outcome"] = "REJECT_RECORD"
    _assert_not_frozen(data)


@pytest.mark.parametrize("stage", ("D", "R", "M", "B", "A", "Q"))
def test_adv_concrete_determinant_identity_is_not_free_text(stage: str) -> None:
    data = _qualified_input()
    binding = next(
        item for item in data["reconstruction_tuple"] if item["stage"] == stage
    )
    binding["normative_id"] = f"WRONG_{stage}_IDENTITY"
    _assert_not_frozen(data)


@pytest.mark.parametrize("stage", ("R", "M", "B", "A", "Q"))
def test_adv_concrete_determinant_version_is_exact(stage: str) -> None:
    data = _qualified_input()
    binding = next(
        item for item in data["reconstruction_tuple"] if item["stage"] == stage
    )
    binding["normative_version"] = f"WRONG_{stage}_VERSION"
    _assert_not_frozen(data)


def test_adv_d_binding_version_matches_acquisition_declaration_version() -> None:
    data = _qualified_input()
    d_binding = next(
        item for item in data["reconstruction_tuple"] if item["stage"] == "D"
    )
    d_binding["normative_version"] = "DIFFERENT_D_MATERIALIZATION_VERSION"
    _assert_not_frozen(data)


def test_adv_anomaly_matrix_version_must_match_a_determinant() -> None:
    data = _qualified_with_local_reject()
    data["anomaly_outcomes"][0]["anomaly_matrix_version"] = "WRONG_A_VERSION"
    _assert_not_frozen(data)


def test_adv_rfc3339_shape_is_not_enough_for_calendar_validity() -> None:
    data = _qualified_input()
    _set_slot0_field(data, "market_timestamp_utc", "2026-99-99T99:99:99.999Z")
    _assert_not_frozen(data)


@pytest.mark.parametrize(
    "volume",
    (
        {"integer_coefficient": 16_777_217, "exponent2": 0},
        {"integer_coefficient": 1, "exponent2": 128},
        {"integer_coefficient": 1, "exponent2": -150},
    ),
)
def test_adv_binary32_normal_form_must_be_representable(volume) -> None:
    data = _qualified_input()
    _set_slot0_field(data, "ask_volume", volume)
    _assert_not_frozen(data)


@pytest.mark.parametrize("numerator", (-1, 4_294_967_296))
def test_adv_price_numerator_must_remain_uint32(numerator: int) -> None:
    data = _qualified_input()
    _set_slot0_field(
        data,
        "ask_price",
        {"numerator": numerator, "denominator": 1000},
    )
    _assert_not_frozen(data)


def test_adv_extra_local_anomaly_cannot_target_retained_slot() -> None:
    data = _qualified_input()
    data["anomaly_outcomes"].append(
        {
            "anomaly_class_id": "BI5-A09",
            "anomaly_matrix_version": (
                "A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE"
            ),
            "target": {
                "target_scope": "COMPLETE_SLOT",
                "component_manifest_entry_id": "SYNTH-F-COMP-001",
                "component_local_slot_index": 0,
            },
            "mandatory_outcome": "REJECT_RECORD",
            "acquisition_fatal": False,
            "qualification_evidence_bindings": [],
        }
    )
    _assert_not_frozen(data)


def test_adv_duplicate_local_anomaly_relation_is_rejected() -> None:
    data = _qualified_with_local_reject()
    data["anomaly_outcomes"].append(copy.deepcopy(data["anomaly_outcomes"][0]))
    _assert_not_frozen(data)


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("declared_role", "WRONG_ROLE"),
        ("instrument_source_identity", "OTHER/INSTRUMENT"),
        ("declared_hour_bucket_utc", "2026-99-99T99:00:00Z"),
    ),
)
def test_adv_component_snapshot_is_concrete_domain_bound(field, value) -> None:
    data = _qualified_input()
    data["acquisition_snapshot"]["components"][0][field] = value
    _assert_not_frozen(data)


def test_adv_zero_complete_slots_without_fragment_is_a06_not_qualified_zero() -> None:
    data = _qualified_input()
    data["acquisition_snapshot"]["components"][0]["complete_slot_count"] = 0
    data["acquisition_snapshot"]["components"][0]["terminal_fragment"] = None
    data["source_accounting"] = []
    data["b_candidate_occurrences"] = []
    data["retained_occurrences"] = []
    data["anomaly_outcomes"] = []
    _assert_not_frozen(data)


def test_adv_duplicate_json_object_key_is_rejected() -> None:
    artifact = f.build_freeze_artifact(_qualified_input())
    payload = f.serialize_freeze_artifact(artifact, pretty=False)
    text = payload.decode("utf-8")
    duplicate = ('{"schema":"WRONG_DUPLICATE",' + text[1:]).encode("utf-8")
    with pytest.raises(ValueError):
        f.deserialize_freeze_artifact(duplicate)


def test_adv_nan_cannot_enter_strict_json_freeze() -> None:
    data = _qualified_input()
    data["qualification_parameters"]["nonstandard_number"] = float("nan")
    _assert_not_frozen(data)
