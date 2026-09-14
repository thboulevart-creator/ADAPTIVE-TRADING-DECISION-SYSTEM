from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


EXPECTED = {
    date(2022, 5, 30): ("SPECIAL_MEMORIAL_DAY_2022", "37019"),
    date(2022, 6, 20): ("SPECIAL_JUNETEENTH_OBSERVED_2022", "38945"),
    date(2022, 7, 4): ("SPECIAL_INDEPENDENCE_DAY_2022", "41225"),
    date(2022, 9, 5): ("SPECIAL_LABOR_DAY_2022", "42569"),
}


def test_batch03_pass_dates_use_exact_broker_1659_2159_break_semantics():
    for day, (reason, record_id) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["fully_closed_hours_utc"] == frozenset(range(17, 22))
        assert classify_slot(day, 16).status == EXPECTED_OPEN
        for hour in range(17, 22):
            slot = classify_slot(day, hour)
            assert slot.status == EXPECTED_CLOSED
            assert slot.reason == reason
        assert classify_slot(day, 22).status == EXPECTED_OPEN


def test_batch03_blocked_july_1_is_not_promoted_to_special_or_normal_evidence():
    assert date(2022, 7, 1) not in SPECIAL_SESSION_EVIDENCE
