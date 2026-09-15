from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2023, 12, 22): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_2023", "63023", frozenset(range(22, 24))),
    date(2024, 1, 15): ("SPECIAL_MARTIN_LUTHER_KING_DAY_2024", "63883", frozenset(range(18, 23))),
    date(2024, 2, 19): ("SPECIAL_PRESIDENTS_DAY_2024", "65120", frozenset(range(18, 23))),
}


def test_batch07_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10392510730
        assert record["artifact_sha256"] == "0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a"
        assert record["probe_commit"] == "3d434dda9bd293d48cbe2f35df3d464abd5938a4"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch07_blocked_dates_are_not_promoted_to_calendar_evidence():
    assert date(2023, 12, 25) not in SPECIAL_SESSION_EVIDENCE
    assert date(2024, 1, 1) not in SPECIAL_SESSION_EVIDENCE


def test_christmas_preholiday_partial_start_hour_remains_open():
    assert classify_slot(date(2023, 12, 22), 21).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 12, 22), 22).status == EXPECTED_CLOSED
    assert classify_slot(date(2023, 12, 22), 23).status == EXPECTED_CLOSED


def test_2024_exact_target_records_encode_only_proven_whole_hours():
    for day in (date(2024, 1, 15), date(2024, 2, 19)):
        assert classify_slot(day, 18).status == EXPECTED_CLOSED
        assert classify_slot(day, 22).status == EXPECTED_CLOSED
        assert classify_slot(day, 23).status == EXPECTED_OPEN
