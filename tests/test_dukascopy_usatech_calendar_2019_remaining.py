from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    classify_slot,
)


def test_2019_good_friday_is_fully_closed() -> None:
    day = date(2019, 4, 19)
    for hour in range(24):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_GOOD_FRIDAY_2019"


def test_2019_independence_day_closes_17_to_22() -> None:
    day = date(2019, 7, 4)
    assert classify_slot(day, 16).status == EXPECTED_OPEN
    for hour in range(17, 22):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_INDEPENDENCE_DAY_2019"
    assert classify_slot(day, 22).status == EXPECTED_OPEN


def test_2019_labor_day_closes_17_to_22() -> None:
    day = date(2019, 9, 2)
    assert classify_slot(day, 16).status == EXPECTED_OPEN
    for hour in range(17, 22):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_LABOR_DAY_2019"
    assert classify_slot(day, 22).status == EXPECTED_OPEN


def test_2019_christmas_eve_preserves_partial_18h_bucket() -> None:
    day = date(2019, 12, 24)
    assert classify_slot(day, 18).status == EXPECTED_OPEN
    for hour in range(19, 24):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_CHRISTMAS_EVE_2019"


def test_2019_christmas_day_closed_until_23_utc_reopen() -> None:
    day = date(2019, 12, 25)
    for hour in range(0, 23):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_CHRISTMAS_DAY_2019"
    assert classify_slot(day, 23).status == EXPECTED_OPEN


def test_2019_new_years_eve_suppresses_23_utc_reopen_only() -> None:
    day = date(2019, 12, 31)
    assert classify_slot(day, 21).status == EXPECTED_OPEN

    classification_22 = classify_slot(day, 22)
    assert classification_22.status == EXPECTED_CLOSED
    assert classification_22.reason == "DAILY_TRADING_BREAK"

    classification_23 = classify_slot(day, 23)
    assert classification_23.status == EXPECTED_CLOSED
    assert classification_23.reason == "SPECIAL_NEW_YEARS_EVE_2019"
