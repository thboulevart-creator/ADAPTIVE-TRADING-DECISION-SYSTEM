from datetime import date

from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch03_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert global_report["candidate_dates"] == 111
    assert global_report["resolved_candidate_dates"] == 34
    assert global_report["unresolved_candidate_dates"] == 77
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []
    assert window_report["candidate_dates"] == 68
    assert window_report["resolved_candidate_dates"] == 11
    assert window_report["unresolved_candidate_dates"] == 57


def test_batch03_integration_progression_accounting_is_exact_and_non_starving():
    _, _, attempts = load_attempt_ledger()
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(attempts) == 15
    assert len(recovery_queue()) == len(decisions) == 57
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 4
    assert len(eligible) == 53
    assert eligible[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")
    assert load_material_capability_changes() == []


def test_batch03_blocked_date_remains_unresolved_but_not_retryable_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    assert date(2022, 7, 1) in raw_days
    assert date(2022, 7, 1) not in eligible_days
