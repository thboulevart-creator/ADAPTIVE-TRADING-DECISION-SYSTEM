from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2024, 5, 27): ("SPECIAL_MEMORIAL_DAY_2024", "68242", frozenset(range(17, 22))),
    date(2024, 6, 19): ("SPECIAL_JUNETEENTH_OBSERVED_2024", "69037", frozenset(range(17, 22))),
    date(2024, 7, 3): ("SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2024", "69819", frozenset(range(18, 22))),
    date(2024, 7, 4): ("SPECIAL_INDEPENDENCE_DAY_OBSERVED_2024", "69820", frozenset(range(17, 22))),
}


def test_batch08_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10402433119
        assert record["artifact_sha256"] == "644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd"
        assert record["probe_commit"] == "5cc4834af2c75de99f6e3427f31ab07b38b42611"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch08_blocked_good_friday_is_not_promoted_to_calendar_evidence():
    assert date(2024, 3, 29) not in SPECIAL_SESSION_EVIDENCE


def test_batch08_partial_start_hours_remain_open_and_only_whole_hours_close():
    assert classify_slot(date(2024, 5, 27), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 5, 27), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 5, 27), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 5, 27), 22).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 7, 3), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 7, 3), 18).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 7, 3), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 7, 3), 22).status == EXPECTED_OPEN


def test_batch08_exact_hour_start_closes_that_whole_hour():
    assert classify_slot(date(2024, 6, 19), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 6, 19), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 6, 19), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 6, 19), 22).status == EXPECTED_OPEN
