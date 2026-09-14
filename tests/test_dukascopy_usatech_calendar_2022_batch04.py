from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


EXPECTED = {
    date(2022, 11, 24): ("SPECIAL_THANKSGIVING_DAY_2022", "45119", frozenset(range(18, 23))),
    date(2022, 11, 25): ("SPECIAL_THANKSGIVING_FRIDAY_2022", "45120", frozenset(range(19, 24))),
    date(2022, 12, 23): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_2022", "46756", frozenset({22, 23})),
}


def test_batch04_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10369230708
        assert record["artifact_sha256"] == "3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc"
        assert record["probe_commit"] == "11a81294720898802e49dd1131a64e20e7e7ae3a"
        assert record["fully_closed_hours_utc"] == closed_hours
        for hour in closed_hours:
            assert classify_slot(day, hour).status == EXPECTED_CLOSED


def test_batch04_partial_start_hours_are_not_rounded_closed():
    assert classify_slot(date(2022, 11, 24), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2022, 11, 25), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2022, 12, 23), 21).status == EXPECTED_OPEN


def test_batch04_cross_date_blocked_dates_are_not_promoted_to_special_evidence():
    assert date(2022, 12, 26) not in SPECIAL_SESSION_EVIDENCE
    assert date(2023, 1, 2) not in SPECIAL_SESSION_EVIDENCE
