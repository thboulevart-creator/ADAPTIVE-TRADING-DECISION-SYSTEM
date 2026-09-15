from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2024, 9, 2): ("SPECIAL_LABOR_DAY_2024", "70878", frozenset(range(17, 22))),
    date(2024, 11, 28): ("SPECIAL_THANKSGIVING_DAY_2024", "72887", frozenset(range(18, 23))),
    date(2024, 11, 29): ("SPECIAL_THANKSGIVING_FRIDAY_2024", "72888", frozenset(range(19, 24))),
    date(2024, 12, 24): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_SESSION_2024", "74339", frozenset(range(19, 24))),
}


def test_batch09_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10406357435
        assert record["artifact_sha256"] == "dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc"
        assert record["probe_commit"] == "0b5dedf6028add27040af112d0bceef76be25827"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch09_blocked_dec25_is_not_promoted_to_calendar_evidence():
    assert date(2024, 12, 25) not in SPECIAL_SESSION_EVIDENCE


def test_batch09_partial_start_hours_remain_open_and_only_whole_hours_close():
    assert classify_slot(date(2024, 11, 29), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 11, 29), 19).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 12, 24), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 12, 24), 19).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 12, 24), 23).status == EXPECTED_CLOSED


def test_batch09_exact_or_pre_hour_boundary_behavior_is_preserved():
    assert classify_slot(date(2024, 9, 2), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 9, 2), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 11, 28), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 11, 28), 18).status == EXPECTED_CLOSED
