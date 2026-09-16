from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timezone

from tools.trading_breaks_target_day_overlap_semantics import (
    CLASS_A_SOURCES,
    QUALIFIED_PROOF_CAPABILITY,
    load_class_a_evidence,
    qualify_class_a,
    validate_target_day_overlap_result,
)


def _fixture(target: date):
    for day, reason, raw, provenance, _ in load_class_a_evidence():
        if day == target:
            return reason, raw, provenance
    raise AssertionError(target)


def test_all_14_persisted_class_a_cases_pass_offline_semantics():
    result = qualify_class_a()
    assert result["verdict"] == "PASS"
    assert result["class_a_count"] == 14 == len(CLASS_A_SOURCES)
    assert result["qualified_proof_capability"] == QUALIFIED_PROOF_CAPABILITY
    assert all(item["cross_date"] is True for item in result["results"])


def test_missing_dom_is_not_promoted_by_itself_but_valid_primary_network_evidence_can_pass():
    reason, raw, provenance = _fixture(date(2024, 3, 29))
    assert raw["dom_witness_lines"] == []
    verdict = validate_target_day_overlap_result(raw, date(2024, 3, 29), reason, provenance)
    assert verdict["verdict"] == "PASS"
    assert verdict["dom_crosscheck"] == "UNAVAILABLE"
    attacked = deepcopy(raw)
    attacked["raw_payload_present"] = False
    assert validate_target_day_overlap_result(attacked, date(2024, 3, 29), reason, provenance)["verdict"] != "PASS"


def test_adjacent_non_overlapping_record_is_rejected():
    reason, raw, provenance = _fixture(date(2024, 12, 25))
    attacked = deepcopy(raw)
    record = attacked["matching_records"][0]
    record["start"] = "1735171200000"  # 2024-12-26T00:00:00Z
    record["end"] = "1735174799000"
    record["start_utc"] = "2024-12-26T00:00:00Z"
    record["end_last_closed_minute_utc"] = "2024-12-26T00:59:59Z"
    record["derived_reopen_utc"] = "2024-12-26T01:00:59Z"
    record["fully_closed_hours_utc"] = []
    assert validate_target_day_overlap_result(attacked, date(2024, 12, 25), reason, provenance) == {
        "verdict": "FAIL", "reason": "BROKER_INTERVAL_DOES_NOT_OVERLAP_TARGET_DAY"
    }


def test_wrong_requested_date_and_wrong_instrument_are_rejected():
    reason, raw, provenance = _fixture(date(2025, 1, 1))
    attacked = deepcopy(raw)
    attacked["requested_date"] = "2024-12-31"
    assert validate_target_day_overlap_result(attacked, date(2025, 1, 1), reason, provenance)["reason"] == "TARGET_OR_REQUESTED_DATE_MISMATCH"
    attacked = deepcopy(raw)
    attacked["instrument_id_observed"] = "9999"
    assert validate_target_day_overlap_result(attacked, date(2025, 1, 1), reason, provenance)["reason"] == "WRONG_INSTRUMENT_ID"


def test_reversed_interval_and_fabricated_reopen_are_rejected():
    reason, raw, provenance = _fixture(date(2026, 4, 3))
    attacked = deepcopy(raw)
    record = attacked["matching_records"][0]
    record["end"] = str(int(record["start"]) - 1)
    assert validate_target_day_overlap_result(attacked, date(2026, 4, 3), reason, provenance)["reason"] == "MALFORMED_NETWORK_INTERVAL"
    attacked = deepcopy(raw)
    attacked["matching_records"][0]["derived_reopen_utc"] = "2099-01-01T00:00:00Z"
    assert validate_target_day_overlap_result(attacked, date(2026, 4, 3), reason, provenance)["reason"] == "DERIVED_REOPEN_MISMATCH"


def test_missing_raw_payload_or_provenance_cannot_pass():
    reason, raw, provenance = _fixture(date(2023, 12, 25))
    attacked = deepcopy(raw)
    attacked["raw_payload_present"] = False
    assert validate_target_day_overlap_result(attacked, date(2023, 12, 25), reason, provenance)["verdict"] == "BLOCKED"
    bad_provenance = deepcopy(provenance)
    bad_provenance["artifact_sha256"] = "bad"
    assert validate_target_day_overlap_result(raw, date(2023, 12, 25), reason, bad_provenance)["verdict"] == "BLOCKED"


def test_multiple_records_and_dom_network_contradiction_are_rejected():
    reason, raw, provenance = _fixture(date(2024, 12, 25))
    attacked = deepcopy(raw)
    attacked["matching_records"].append(deepcopy(attacked["matching_records"][0]))
    assert validate_target_day_overlap_result(attacked, date(2024, 12, 25), reason, provenance)["reason"] == "MULTIPLE_MATCHING_RECORDS_AMBIGUOUS"
    attacked = deepcopy(raw)
    attacked["dom_witness_lines"][0] = attacked["dom_witness_lines"][0].replace("24-Dec-24 18:14:59", "24-Dec-24 18:15:00")
    assert validate_target_day_overlap_result(attacked, date(2024, 12, 25), reason, provenance)["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_partial_hour_rounding_attack_is_rejected():
    reason, raw, provenance = _fixture(date(2025, 4, 18))
    attacked = deepcopy(raw)
    attacked["matching_records"][0]["fully_closed_hours_utc"] = list(range(24)) + [24]
    assert validate_target_day_overlap_result(attacked, date(2025, 4, 18), reason, provenance)["reason"] == "TARGET_DAY_CLOSED_HOURS_MISMATCH"


def test_unrelated_year_record_borrowing_is_rejected():
    reason, raw, provenance = _fixture(date(2025, 12, 25))
    _, donor, _ = _fixture(date(2024, 12, 25))
    attacked = deepcopy(raw)
    attacked["matching_records"] = deepcopy(donor["matching_records"])
    attacked["dom_witness_lines"] = deepcopy(donor["dom_witness_lines"])
    assert validate_target_day_overlap_result(attacked, date(2025, 12, 25), reason, provenance)["reason"] == "BROKER_INTERVAL_DOES_NOT_OVERLAP_TARGET_DAY"


def test_captured_label_cannot_bypass_independent_semantic_validation():
    reason, raw, provenance = _fixture(date(2025, 1, 1))
    attacked = deepcopy(raw)
    attacked["capture_verdict"] = "CAPTURED"
    attacked["matching_records"][0]["fully_closed_hours_utc"] = [23]
    assert validate_target_day_overlap_result(attacked, date(2025, 1, 1), reason, provenance)["verdict"] == "FAIL"


def test_no_whole_hour_overlap_cannot_be_promoted():
    reason, raw, provenance = _fixture(date(2025, 1, 1))
    attacked = deepcopy(raw)
    record = attacked["matching_records"][0]
    # 00:10 -> 00:20 closed interval on target day: overlap exists, no complete UTC hour.
    start = datetime(2025, 1, 1, 0, 10, tzinfo=timezone.utc)
    end = datetime(2025, 1, 1, 0, 19, tzinfo=timezone.utc)
    record["start"] = str(int(start.timestamp() * 1000))
    record["end"] = str(int(end.timestamp() * 1000))
    record["start_utc"] = "2025-01-01T00:10:00Z"
    record["end_last_closed_minute_utc"] = "2025-01-01T00:19:00Z"
    record["derived_reopen_utc"] = "2025-01-01T00:20:00Z"
    record["fully_closed_hours_utc"] = []
    attacked["dom_witness_lines"] = []
    verdict = validate_target_day_overlap_result(attacked, date(2025, 1, 1), reason, provenance)
    assert verdict == {"verdict": "BLOCKED", "reason": "NO_WHOLE_TARGET_DAY_CLOSED_HOUR_PROVEN"}
