from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


EXPECTED = {
    date(2023, 1, 16): ("SPECIAL_MARTIN_LUTHER_KING_DAY_2023", "49338", frozenset(range(18, 23))),
    date(2023, 2, 20): ("SPECIAL_PRESIDENTS_DAY_2023", "50456", frozenset(range(18, 23))),
    date(2023, 4, 7): ("SPECIAL_GOOD_FRIDAY_2023", "52290", frozenset(range(15, 24))),
    date(2023, 5, 29): ("SPECIAL_MEMORIAL_DAY_2023", "54373", frozenset(range(17, 22))),
    date(2023, 6, 19): ("SPECIAL_JUNETEENTH_OBSERVED_2023", "55281", frozenset(range(17, 22))),
}


def test_batch05_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10386998786
        assert record["artifact_sha256"] == "ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c"
        assert record["probe_commit"] == "33ae476c48372bce64421a411066db2ddea6125c"
        assert record["fully_closed_hours_utc"] == closed_hours
        for hour in closed_hours:
            assert classify_slot(day, hour).status == EXPECTED_CLOSED


def test_batch05_partial_start_hours_are_not_rounded_closed():
    assert classify_slot(date(2023, 1, 16), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 2, 20), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 4, 7), 14).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 5, 29), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 6, 19), 16).status == EXPECTED_OPEN


def test_good_friday_weekend_span_projects_only_target_day_whole_hours():
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 4, 7)]["fully_closed_hours_utc"] == frozenset(range(15, 24))
