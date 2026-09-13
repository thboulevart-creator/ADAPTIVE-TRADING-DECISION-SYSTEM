from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    classify_slot,
)


def test_2020_new_years_day_closed_until_23_utc_reopen() -> None:
    day = date(2020, 1, 1)

    for hour in range(0, 23):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_NEW_YEARS_DAY_2020"

    assert classify_slot(day, 23).status == EXPECTED_OPEN
