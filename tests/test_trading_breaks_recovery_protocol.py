from __future__ import annotations

from dataclasses import replace
from datetime import date

from tools.trading_breaks_recovery_protocol import (
    RecoveryEvidence,
    derive_fully_closed_hours_utc,
    derive_interval,
    recovery_queue,
    validate_positive_recovery,
    validate_positive_recovery_against_frozen_batch,
)


TARGET = date(2021, 12, 24)
GOOD_RECORD = {
    "id": "synthetic-test-record",
    "instrument": "9016",
    "start": "1640368800000",  # 2021-12-24 18:00:00Z
    "end": "1640386740000",    # 2021-12-24 22:59:00Z
    "reason": "Thanksgiving Day",
}
GOOD_DOM = {
    "instrument": "9016",
    "start": "1640368800000",
    "end": "1640386740000",
    "reason": "Thanksgiving Day",
}
FROZEN_SCOPE = [(TARGET, "CHRISTMAS_OBSERVED")]


def good_evidence() -> RecoveryEvidence:
    return RecoveryEvidence(
        target_date=TARGET,
        candidate_reason="CHRISTMAS_OBSERVED",
        requested_date=TARGET,
        instrument_id="9016",
        instrument_name="USATECH.IDX/USD",
        network_record=dict(GOOD_RECORD),
        raw_payload_present=True,
        dom_available=True,
        dom_record=dict(GOOD_DOM),
        workflow_run=123456,
        artifact_id=654321,
        artifact_sha256="a" * 64,
        probe_commit="b" * 40,
    )


def test_queue_scope_sorted_and_has_34_unresolved_candidates_after_batch09():
    queue = recovery_queue()
    days = [day for day, _ in queue]
    assert len(queue) == 34
    assert days == sorted(days)
    assert days[0] == date(2021, 12, 24)
    assert days[-1] == date(2026, 7, 3)
    assert date(2021, 9, 6) not in days
    assert date(2025, 1, 9) not in days


def test_valid_positive_record_passes_and_uses_calibrated_end_semantics():
    result = validate_positive_recovery(good_evidence())
    assert result["verdict"] == "PASS"
    assert result["reopen_utc"] == "2021-12-24T23:00:00Z"
    assert result["fully_closed_hours_utc"] == [18, 19, 20, 21, 22]


def test_out_of_window_target_fails():
    e = replace(good_evidence(), target_date=date(2020, 2, 17), requested_date=date(2020, 2, 17))
    assert validate_positive_recovery(e) == {
        "verdict": "FAIL",
        "reason": "TARGET_OUTSIDE_FROZEN_WINDOW",
    }


def test_already_resolved_date_cannot_reenter_recovery_queue():
    e = replace(good_evidence(), target_date=date(2021, 9, 6), requested_date=date(2021, 9, 6))
    assert validate_positive_recovery(e)["reason"] == "TARGET_NOT_IN_GOVERNED_RECOVERY_QUEUE"


def test_requested_date_mismatch_fails():
    e = replace(good_evidence(), requested_date=date(2021, 11, 26))
    assert validate_positive_recovery(e)["reason"] == "REQUESTED_DATE_MISMATCH"


def test_wrong_instrument_id_fails():
    e = replace(good_evidence(), instrument_id="9999")
    assert validate_positive_recovery(e)["reason"] == "WRONG_INSTRUMENT_ID"


def test_wrong_instrument_name_fails():
    e = replace(good_evidence(), instrument_name="USA500.IDX/USD")
    assert validate_positive_recovery(e)["reason"] == "WRONG_INSTRUMENT_NAME"


def test_empty_response_is_blocked_not_pass():
    e = replace(good_evidence(), network_record=None, dom_available=False, dom_record=None)
    result = validate_positive_recovery(e)
    assert result == {
        "verdict": "BLOCKED",
        "reason": "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED",
    }


def test_missing_raw_payload_is_blocked():
    e = replace(good_evidence(), raw_payload_present=False)
    assert validate_positive_recovery(e)["reason"] == "RAW_BROKER_PAYLOAD_NOT_RETAINED"


def test_network_record_wrong_instrument_fails():
    record = dict(GOOD_RECORD)
    record["instrument"] = "42"
    e = replace(good_evidence(), network_record=record)
    assert validate_positive_recovery(e)["reason"] == "NETWORK_RECORD_WRONG_INSTRUMENT"


def test_malformed_timestamp_fails():
    record = dict(GOOD_RECORD)
    record["start"] = "not-an-epoch"
    e = replace(good_evidence(), network_record=record)
    assert validate_positive_recovery(e)["reason"] == "MALFORMED_NETWORK_INTERVAL"


def test_negative_interval_fails():
    record = dict(GOOD_RECORD)
    record["start"], record["end"] = record["end"], record["start"]
    e = replace(good_evidence(), network_record=record)
    assert validate_positive_recovery(e)["reason"] == "MALFORMED_NETWORK_INTERVAL"


def test_adjacent_date_record_fails():
    record = dict(GOOD_RECORD)
    record["start"] = "1637776800000"  # 2021-11-24 18:00Z
    e = replace(good_evidence(), network_record=record)
    assert validate_positive_recovery(e)["reason"] == "NETWORK_RECORD_DATE_MISMATCH"


def test_dom_network_contradiction_fails():
    dom = dict(GOOD_DOM)
    dom["end"] = "1637881080000"
    e = replace(good_evidence(), dom_record=dom)
    assert validate_positive_recovery(e)["reason"] == "DOM_NETWORK_CONTRADICTION"


def test_expected_dom_missing_is_blocked():
    e = replace(good_evidence(), dom_record=None)
    assert validate_positive_recovery(e)["reason"] == "EXPECTED_DOM_CROSSCHECK_MISSING"


def test_missing_workflow_provenance_is_blocked():
    e = replace(good_evidence(), workflow_run=None)
    assert validate_positive_recovery(e)["reason"] == "WORKFLOW_PROVENANCE_MISSING"


def test_missing_artifact_id_is_blocked():
    e = replace(good_evidence(), artifact_id=None)
    assert validate_positive_recovery(e)["reason"] == "ARTIFACT_ID_MISSING"


def test_bad_artifact_hash_is_blocked():
    e = replace(good_evidence(), artifact_sha256="bad")
    assert validate_positive_recovery(e)["reason"] == "ARTIFACT_SHA256_INVALID"


def test_bad_probe_commit_is_blocked():
    e = replace(good_evidence(), probe_commit="bad")
    assert validate_positive_recovery(e)["reason"] == "PROBE_COMMIT_INVALID"


def test_partial_hour_is_not_rounded_to_closed():
    record = dict(GOOD_RECORD)
    record["start"] = "1640369700000"  # 18:15Z
    record["end"] = "1640386740000"    # 22:59Z -> reopen 23:00Z
    start, _, reopen = derive_interval(record)
    closed = derive_fully_closed_hours_utc(TARGET, start, reopen)
    assert 18 not in closed
    assert closed == frozenset({19, 20, 21, 22})


def test_frozen_batch_replay_accepts_exact_immutable_membership():
    before = recovery_queue()
    result = validate_positive_recovery_against_frozen_batch(good_evidence(), FROZEN_SCOPE)
    assert result["verdict"] == "PASS"
    assert result["reason"] == "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED"
    assert recovery_queue() == before


def test_frozen_batch_replay_rejects_target_absent_from_scope():
    scope = [(date(2022, 1, 17), "MARTIN_LUTHER_KING_DAY")]
    result = validate_positive_recovery_against_frozen_batch(good_evidence(), scope)
    assert result == {"verdict": "FAIL", "reason": "TARGET_NOT_IN_FROZEN_BATCH_SCOPE"}


def test_frozen_batch_replay_rejects_candidate_reason_substitution():
    e = replace(good_evidence(), candidate_reason="MANUAL_SUBSTITUTION")
    result = validate_positive_recovery_against_frozen_batch(e, FROZEN_SCOPE)
    assert result == {"verdict": "FAIL", "reason": "CANDIDATE_REASON_MISMATCH"}


def test_frozen_batch_replay_rejects_duplicate_target_identity():
    scope = [
        (TARGET, "CHRISTMAS_OBSERVED"),
        (TARGET, "MANUAL_DUPLICATE"),
    ]
    result = validate_positive_recovery_against_frozen_batch(good_evidence(), scope)
    assert result == {"verdict": "FAIL", "reason": "FROZEN_SCOPE_DUPLICATE_TARGET"}


def test_frozen_batch_replay_rejects_non_chronological_scope():
    scope = [
        (date(2022, 1, 17), "MARTIN_LUTHER_KING_DAY"),
        (TARGET, "CHRISTMAS_OBSERVED"),
    ]
    result = validate_positive_recovery_against_frozen_batch(good_evidence(), scope)
    assert result == {"verdict": "FAIL", "reason": "FROZEN_SCOPE_NOT_CHRONOLOGICAL"}


def test_frozen_batch_replay_rejects_empty_or_malformed_scope():
    assert validate_positive_recovery_against_frozen_batch(good_evidence(), []) == {
        "verdict": "FAIL",
        "reason": "FROZEN_SCOPE_EMPTY",
    }
    assert validate_positive_recovery_against_frozen_batch(
        good_evidence(),
        [[TARGET, "CHRISTMAS_OBSERVED"]],  # type: ignore[list-item]
    ) == {"verdict": "FAIL", "reason": "FROZEN_SCOPE_MALFORMED"}
