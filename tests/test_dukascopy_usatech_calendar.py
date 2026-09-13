from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    classify_slot,
)


def test_saturday_is_fully_closed() -> None:
    day = date(2025, 1, 18)
    assert all(classify_slot(day, hour).status == EXPECTED_CLOSED for hour in range(24))


def test_winter_regular_day_keeps_partial_close_hour_open() -> None:
    day = date(2025, 1, 22)
    assert classify_slot(day, 21).status == EXPECTED_OPEN
    assert classify_slot(day, 22).status == EXPECTED_CLOSED
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_winter_sunday_opens_only_at_23_utc() -> None:
    day = date(2025, 1, 19)
    assert classify_slot(day, 22).status == EXPECTED_CLOSED
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_winter_friday_does_not_reopen_after_weekly_close() -> None:
    day = date(2025, 1, 24)
    assert classify_slot(day, 21).status == EXPECTED_OPEN
    assert classify_slot(day, 22).status == EXPECTED_CLOSED
    assert classify_slot(day, 23).status == EXPECTED_CLOSED


def test_summer_daily_break_is_hour_21_utc() -> None:
    day = date(2025, 7, 2)
    assert classify_slot(day, 20).status == EXPECTED_OPEN
    assert classify_slot(day, 21).status == EXPECTED_CLOSED
    assert classify_slot(day, 22).status == EXPECTED_OPEN
