from datetime import date

from tools.dukascopy_usatech_calendar_coverage import (
    COVERAGE_END,
    COVERAGE_START,
    audit_calendar_coverage,
    candidate_special_dates,
)


def _candidate_days() -> set[date]:
    return {item.day for item in candidate_special_dates()}


def test_coverage_envelope_is_broader_than_five_year_requirement() -> None:
    assert COVERAGE_START == date(2018, 5, 1)
    assert COVERAGE_END == date(2026, 8, 14)
    assert (COVERAGE_END - COVERAGE_START).days > 5 * 365


def test_candidate_generator_contains_known_special_sessions() -> None:
    days = _candidate_days()
    for day in (
        date(2018, 5, 28),
        date(2018, 7, 3),
        date(2018, 7, 4),
        date(2018, 12, 5),
        date(2020, 2, 17),
        date(2025, 1, 9),
    ):
        assert day in days


def test_candidate_generator_handles_observed_holidays_and_adjacent_sessions() -> None:
    days = _candidate_days()

    # 2021 Independence Day was Sunday -> Monday 5 July observed, with Friday
    # 2 July retained as the preceding-session candidate.
    assert date(2021, 7, 5) in days
    assert date(2021, 7, 2) in days

    # Juneteenth enters CME holiday treatment from 2022 onward.
    assert date(2022, 6, 20) in days

    # 2026 Independence Day is Saturday -> Friday 3 July observed; Thursday 2
    # July is the preceding-session candidate.
    assert date(2026, 7, 3) in days
    assert date(2026, 7, 2) in days


def test_coverage_audit_cannot_pass_while_evidence_is_incomplete() -> None:
    report = audit_calendar_coverage()
    assert report["execution_window_frozen"] is False
    assert report["verdict"] == "BLOCKED"
    assert report["reason"] == "SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE"
    assert report["unresolved_candidate_dates"] > 0


def test_current_special_evidence_is_well_formed_and_not_orphaned() -> None:
    report = audit_calendar_coverage()
    assert report["evidence_shape_errors"] == []
    assert report["contradictory_evidence_dates"] == []
    assert report["orphan_special_evidence"] == []
    assert report["special_session_evidence_dates"] >= 5
