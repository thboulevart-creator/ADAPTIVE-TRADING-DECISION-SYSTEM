from __future__ import annotations

from copy import deepcopy
from datetime import date

from tools.trading_breaks_target_day_overlap_readjudication import readjudicate_class_a
from tools.trading_breaks_target_day_overlap_semantics import (
    load_class_a_evidence,
    validate_target_day_overlap_result,
)


def _fixture(target: date):
    for day, reason, raw, provenance, _ in load_class_a_evidence():
        if day == target:
            return reason, raw, provenance
    raise AssertionError(target)


def test_all_14_class_a_dates_readjudicate_pass_under_persisted_v2():
    result = readjudicate_class_a()
    assert result["verdict"] == "PASS"
    assert result["historical_attempt_count"] == 68
    assert result["material_capability_change_count"] == 1
    assert result["readjudicated_count"] == 14
    assert (result["pass_count"], result["blocked_count"], result["fail_count"]) == (14, 0, 0)
    assert len(result["results"]) == 14
    assert all(item["verdict"] == "PASS" for item in result["results"])
    assert all(item["cross_date"] is True for item in result["results"])
    assert all(item["proposed_retry_attempt_id"].startswith("overlap-v2:") for item in result["results"])


def test_readjudication_does_not_confuse_source_blocked_attempt_with_new_pass():
    result = readjudicate_class_a()
    for item in result["results"]:
        assert item["source_attempt_id"] != item["proposed_retry_attempt_id"]
        assert item["source_capability_id"] == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
        assert item["readjudication_capability_id"] == "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"


def test_cross_date_promotion_still_requires_independent_semantic_validation():
    reason, raw, provenance = _fixture(date(2025, 1, 1))
    attacked = deepcopy(raw)
    attacked["capture_verdict"] = "CAPTURED"
    attacked["matching_records"][0]["derived_reopen_utc"] = "2099-01-01T00:00:00Z"
    verdict = validate_target_day_overlap_result(attacked, date(2025, 1, 1), reason, provenance)
    assert verdict["verdict"] == "FAIL"
    assert verdict["reason"] == "DERIVED_REOPEN_MISMATCH"


def test_missing_dom_case_cannot_pass_if_primary_network_payload_is_removed():
    reason, raw, provenance = _fixture(date(2025, 4, 18))
    assert raw["dom_witness_lines"] == []
    attacked = deepcopy(raw)
    attacked["raw_payload_present"] = False
    verdict = validate_target_day_overlap_result(attacked, date(2025, 4, 18), reason, provenance)
    assert verdict == {"verdict": "BLOCKED", "reason": "RAW_BROKER_PAYLOAD_NOT_RETAINED"}


def test_dom_network_contradiction_blocks_even_with_v2_enabled():
    reason, raw, provenance = _fixture(date(2024, 12, 25))
    attacked = deepcopy(raw)
    attacked["dom_witness_lines"][0] = attacked["dom_witness_lines"][0].replace("24-Dec-24 18:14:59", "24-Dec-24 18:15:00")
    verdict = validate_target_day_overlap_result(attacked, date(2024, 12, 25), reason, provenance)
    assert verdict == {"verdict": "FAIL", "reason": "DOM_NETWORK_CONTRADICTION"}


def test_multiple_record_or_wrong_target_attacks_remain_rejected():
    reason, raw, provenance = _fixture(date(2026, 1, 1))
    attacked = deepcopy(raw)
    attacked["matching_records"].append(deepcopy(attacked["matching_records"][0]))
    assert validate_target_day_overlap_result(attacked, date(2026, 1, 1), reason, provenance)["reason"] == "MULTIPLE_MATCHING_RECORDS_AMBIGUOUS"
    attacked = deepcopy(raw)
    attacked["target_date"] = "2025-12-31"
    assert validate_target_day_overlap_result(attacked, date(2026, 1, 1), reason, provenance)["reason"] == "TARGET_OR_REQUESTED_DATE_MISMATCH"
