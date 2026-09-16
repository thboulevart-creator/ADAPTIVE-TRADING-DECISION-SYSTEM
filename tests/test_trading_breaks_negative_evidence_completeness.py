from __future__ import annotations

from copy import deepcopy

from tools.trading_breaks_negative_evidence_completeness import (
    PASS_REASON,
    evaluate_observation,
    evaluate_repeated_consistency,
)


def baseline() -> dict:
    return {
        "provenance_match": True,
        "runtime_artifact_match": True,
        "borrowed_adjacent_or_other_year": False,
        "requested_date_exact": True,
        "date_honored": True,
        "instrument_identity_exact": True,
        "runtime_errors_present": False,
        "artifact_runtime_errors_present": False,
        "http_success": True,
        "raw_payload_present": True,
        "target_scope_full_day": True,
        "single_target_range_request_response": True,
        "pagination_present": False,
        "body_capture_complete": True,
        "jsonp_list_complete": True,
        "internal_target_instrument_raw_control": True,
        "internal_target_instrument_dom_control": True,
        "raw_target_day_overlap_count": 0,
        "normalized_matching_count": 0,
        "raw_target_instrument_records": [
            {
                "id": "control",
                "instrument": "9016",
                "start": "1656953940000",
                "end": "1656971940000",
                "reason": "Internal control outside target day",
            }
        ],
        "target_scope_start_ms": 1656633600000,
        "target_scope_end_ms": 1659311999999,
    }


def test_complete_raw_negative_evidence_passes() -> None:
    result = evaluate_observation(baseline())
    assert result.verdict == "PASS"
    assert result.reason == PASS_REASON


def test_http_200_does_not_rescue_missing_raw_payload() -> None:
    item = baseline()
    item["raw_payload_present"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RAW_PAYLOAD_MISSING"


def test_date_fallback_is_rejected() -> None:
    item = baseline()
    item["date_honored"] = False
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "TARGET_DATE_NOT_EXACTLY_HONORED"


def test_wrong_instrument_identity_is_rejected() -> None:
    item = baseline()
    item["instrument_identity_exact"] = False
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "TARGET_INSTRUMENT_IDENTITY_MISMATCH"


def test_raw_overlap_hidden_by_normalized_filter_is_rejected() -> None:
    item = baseline()
    item["raw_target_day_overlap_count"] = 1
    item["normalized_matching_count"] = 0
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "NORMALIZED_FILTER_HIDES_OR_INVENTS_RAW_TARGET_RECORD"


def test_positive_raw_overlap_cannot_be_promoted_as_negative() -> None:
    item = baseline()
    item["raw_target_day_overlap_count"] = 1
    item["normalized_matching_count"] = 1
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "POSITIVE_TARGET_DAY_INTERVAL_EXISTS_NOT_NEGATIVE_EVIDENCE"


def test_capture_truncation_is_blocked() -> None:
    item = baseline()
    item["body_capture_complete"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RAW_BODY_CAPTURE_COMPLETENESS_NOT_PROVEN"


def test_pagination_or_continuation_is_blocked() -> None:
    item = baseline()
    item["pagination_present"] = True
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "PAGINATION_OR_CONTINUATION_PRESENT"


def test_partial_target_day_scope_is_blocked() -> None:
    item = baseline()
    item["target_scope_full_day"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "TARGET_DAY_NOT_FULLY_REPRESENTED_BY_RESPONSE_SCOPE"


def test_multiple_or_missing_target_range_responses_are_blocked() -> None:
    item = baseline()
    item["single_target_range_request_response"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "SINGLE_FULL_RANGE_RESPONSE_NOT_PROVEN"


def test_adjacent_or_other_year_borrowing_is_rejected() -> None:
    item = baseline()
    item["borrowed_adjacent_or_other_year"] = True
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "BORROWED_NON_TARGET_EVIDENCE"


def test_runtime_errors_cannot_be_presented_as_negative_evidence() -> None:
    item = baseline()
    item["runtime_errors_present"] = True
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RUNTIME_OR_NETWORK_ERRORS_PRESENT"


def test_artifact_runtime_errors_cannot_be_hidden() -> None:
    item = baseline()
    item["artifact_runtime_errors_present"] = True
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RUNTIME_OR_NETWORK_ERRORS_PRESENT"


def test_provenance_mismatch_is_rejected() -> None:
    item = baseline()
    item["provenance_match"] = False
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "PROVENANCE_MISMATCH"


def test_runtime_artifact_contradiction_is_rejected() -> None:
    item = baseline()
    item["runtime_artifact_match"] = False
    result = evaluate_observation(item)
    assert result.verdict == "FAIL"
    assert result.reason == "RUNTIME_ARTIFACT_CONTRADICTION"


def test_empty_normalized_result_without_complete_jsonp_is_blocked() -> None:
    item = baseline()
    item["jsonp_list_complete"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RAW_BROKER_LIST_NOT_SYNTACTICALLY_COMPLETE"


def test_empty_normalized_result_without_raw_instrument_control_is_blocked() -> None:
    item = baseline()
    item["internal_target_instrument_raw_control"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "RAW_TARGET_INSTRUMENT_SCOPE_CONTROL_MISSING"


def test_empty_normalized_result_without_dom_instrument_control_is_blocked() -> None:
    item = baseline()
    item["internal_target_instrument_dom_control"] = False
    result = evaluate_observation(item)
    assert result.verdict == "BLOCKED"
    assert result.reason == "DOM_TARGET_INSTRUMENT_SCOPE_CONTROL_MISSING"


def test_repeated_observations_must_be_consistent() -> None:
    first = baseline()
    second = deepcopy(first)
    second["raw_target_instrument_records"] = [
        {
            "id": "different",
            "instrument": "9016",
            "start": "1657000000000",
            "end": "1657003600000",
            "reason": "Different observation",
        }
    ]
    result = evaluate_repeated_consistency([first, second])
    assert result.verdict == "FAIL"
    assert result.reason == "INCONSISTENT_REPEATED_OBSERVATIONS"


def test_repeated_identical_observations_are_only_consistency_support() -> None:
    first = baseline()
    second = deepcopy(first)
    result = evaluate_repeated_consistency([first, second])
    assert result.verdict == "PASS"
    assert result.reason == "REPEATED_OBSERVATIONS_CONSISTENT"
