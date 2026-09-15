from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2023, 7, 3): ("SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2023", "56233", frozenset(range(18, 24))),
    date(2023, 9, 4): ("SPECIAL_LABOR_DAY_2023", "57462", frozenset(range(17, 22))),
    date(2023, 11, 23): ("SPECIAL_THANKSGIVING_DAY_2023", "59358", frozenset(range(17, 23))),
    date(2023, 11, 24): ("SPECIAL_THANKSGIVING_FRIDAY_2023", "59359", frozenset(range(18, 24))),
}


def test_batch06_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10390926878
        assert record["artifact_sha256"] == "1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052"
        assert record["probe_commit"] == "e968db2be1fbfd4d2c419f9dad717ca479b52edd"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch06_blocked_july4_is_not_promoted_to_calendar_evidence():
    assert date(2023, 7, 4) not in SPECIAL_SESSION_EVIDENCE


def test_partial_start_hours_remain_open():
    assert classify_slot(date(2023, 7, 3), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 7, 3), 18).status == EXPECTED_CLOSED
    assert classify_slot(date(2023, 11, 24), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 11, 24), 18).status == EXPECTED_CLOSED


def test_multiday_records_project_only_target_day_whole_hours():
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 7, 3)]["fully_closed_hours_utc"] == frozenset(range(18, 24))
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 11, 24)]["fully_closed_hours_utc"] == frozenset(range(18, 24))
