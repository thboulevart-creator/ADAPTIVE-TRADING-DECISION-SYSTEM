from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


def test_2021_labor_day_record_is_exact_broker_native_evidence() -> None:
    day = date(2021, 9, 6)
    record = SPECIAL_SESSION_EVIDENCE[day]

    assert record["reason"] == "SPECIAL_LABOR_DAY_2021"
    assert record["fully_closed_hours_utc"] == frozenset(range(17, 22))
    assert "dukascopy.com" in record["dukascopy_widget_source"]
    assert "date=1630886400000" in record["dukascopy_widget_source"]


def test_2021_labor_day_closes_exactly_17_to_21_utc() -> None:
    day = date(2021, 9, 6)

    assert classify_slot(day, 16).status == EXPECTED_OPEN

    for hour in range(17, 22):
        classification = classify_slot(day, hour)
        assert classification.status == EXPECTED_CLOSED
        assert classification.reason == "SPECIAL_LABOR_DAY_2021"

    assert classify_slot(day, 22).status == EXPECTED_OPEN
