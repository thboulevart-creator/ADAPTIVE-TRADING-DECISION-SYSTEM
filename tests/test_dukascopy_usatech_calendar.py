from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    classify_slot,
)


def test_saturday_is_fully_closed() -> None:
    day = date(2025, 1, 18)
    assert all(
        classify_slot(day, hour).status == EXPECTED_CLOSED
        for hour in range(24)
    )


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


def test_jan_9_2025_special_equity_session_closes_only_full_hour_buckets() -> None:
    day = date(2025, 1, 9)

    # CME equity-index session closes at 14:30 UTC, so the 14h BI5 bucket
    # still contains an admissible 30-minute trading interval.
    assert classify_slot(day, 14).status == EXPECTED_OPEN

    # 15:00-23:00 UTC is fully closed at hourly BI5 granularity.
    for hour in range(15, 23):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_US_NATIONAL_DAY_OF_MOURNING_2025"

    # Normal reopening is 23:00 UTC for the next trade date.
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_jan_9_special_session_does_not_hide_other_open_hours() -> None:
    day = date(2025, 1, 9)
    for hour in (0, 2, 4, 7, 10, 13):
        assert classify_slot(day, hour).status == EXPECTED_OPEN
