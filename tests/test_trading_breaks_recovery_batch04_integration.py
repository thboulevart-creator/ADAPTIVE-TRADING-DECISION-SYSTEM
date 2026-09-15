from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


PASS_DAYS = {date(2022, 11, 24), date(2022, 11, 25), date(2022, 12, 23)}
BLOCKED_DAYS = {date(2022, 12, 26), date(2023, 1, 2)}


def test_batch04_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 53, 58)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 30, 38)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch04_atomic_integration_records_exactly_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch04 = [item for item in attempts if item.attempt_id.startswith("batch04:")]
    assert len(attempts) == 40
    assert [item.attempt_sequence for item in batch04] == [16, 17, 18, 19, 20]
    assert [item.outcome for item in batch04] == ["PASS", "PASS", "PASS", "BLOCKED", "BLOCKED"]
    assert load_material_capability_changes() == []


def test_batch04_passes_leave_unresolved_queue_and_blocked_remain_unresolved_but_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert BLOCKED_DAYS <= raw_days
    assert BLOCKED_DAYS.isdisjoint(eligible_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    for day in BLOCKED_DAYS:
        assert decisions[day].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decisions[day].latest_attempt_outcome == "BLOCKED"
        assert decisions[day].contract_verdict == "PASS"


def test_batch04_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 38
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 10
    assert len(eligible) == 28
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")
