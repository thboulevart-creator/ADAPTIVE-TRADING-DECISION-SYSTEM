from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


def test_thanksgiving_2021_exact_broker_break_is_integrated():
    day = date(2021, 11, 25)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_THANKSGIVING_DAY_2021"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_thanksgiving_friday_2021_preserves_regular_weekly_close_boundary():
    day = date(2021, 11, 26)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset({19, 20, 21})
    assert classify_slot(day, 18).status == EXPECTED_OPEN
    for hour in (19, 20, 21):
        assert classify_slot(day, hour).reason == "SPECIAL_THANKSGIVING_FRIDAY_2021"
    assert classify_slot(day, 22).reason == "WEEKLY_POST_CLOSE"
    assert classify_slot(day, 23).reason == "WEEKLY_POST_CLOSE"


def test_christmas_pre_holiday_2021_exact_start_date_is_integrated():
    day = date(2021, 12, 23)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset({22, 23})
    assert classify_slot(day, 21).status == EXPECTED_OPEN
    for hour in (22, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2021"


def test_blocked_batch01_dates_are_not_silently_promoted():
    assert date(2021, 12, 24) not in SPECIAL_SESSION_EVIDENCE
    assert date(2021, 12, 31) not in SPECIAL_SESSION_EVIDENCE
