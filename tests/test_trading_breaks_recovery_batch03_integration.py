from datetime import date

from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch03_integrated_evidence_remains_valid_in_post_batch14_state():
    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert global_report["candidate_dates"] == 111
    assert global_report["resolved_candidate_dates"] == 74
    assert global_report["unresolved_candidate_dates"] == 37
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []
    assert window_report["candidate_dates"] == 68
    assert window_report["resolved_candidate_dates"] == 51
    assert window_report["unresolved_candidate_dates"] == 17


def test_batch03_attempt_history_remains_preserved_post_batch09():
    _, _, attempts = load_attempt_ledger()
    batch03 = [item for item in attempts if item.attempt_id.startswith("batch03:")]
    assert len(attempts) == 68
    assert [item.attempt_sequence for item in batch03] == [11, 12, 13, 14, 15]
    assert [item.outcome for item in batch03] == ["PASS", "PASS", "BLOCKED", "PASS", "PASS"]
    assert load_material_capability_changes() == []


def test_batch03_blocked_date_remains_unresolved_but_not_retryable_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert date(2022, 7, 1) in raw_days
    assert date(2022, 7, 1) not in eligible_days
    assert decisions[date(2022, 7, 1)].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
