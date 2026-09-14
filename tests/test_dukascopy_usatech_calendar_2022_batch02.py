from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


def test_mlk_day_2022_exact_broker_break_is_integrated():
    day = date(2022, 1, 17)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_MARTIN_LUTHER_KING_DAY_2022"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_presidents_day_2022_exact_broker_break_is_integrated():
    day = date(2022, 2, 21)
    assert SPECIAL_SESSION_EVIDENCE[day]["fully_closed_hours_utc"] == frozenset(range(18, 23))
    assert classify_slot(day, 17).status == EXPECTED_OPEN
    for hour in range(18, 23):
        slot = classify_slot(day, hour)
        assert slot.status == EXPECTED_CLOSED
        assert slot.reason == "SPECIAL_PRESIDENTS_DAY_2022"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_batch02_blocked_dates_are_not_silently_promoted():
    assert date(2021, 12, 24) not in SPECIAL_SESSION_EVIDENCE
    assert date(2021, 12, 31) not in SPECIAL_SESSION_EVIDENCE
    assert date(2022, 4, 15) not in SPECIAL_SESSION_EVIDENCE
