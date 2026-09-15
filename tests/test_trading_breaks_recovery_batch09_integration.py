from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2024, 9, 2), date(2024, 11, 28), date(2024, 11, 29), date(2024, 12, 24)}
BLOCKED_DAY = date(2024, 12, 25)


def test_batch09_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 74, 37)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 51, 17)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch09_atomic_integration_records_all_five_factual_attempts_in_frozen_order():
    _, _, attempts = load_attempt_ledger()
    batch09 = [item for item in attempts if item.attempt_id.startswith("batch09:")]
    assert len(attempts) == 68
    assert [item.attempt_sequence for item in batch09] == [41, 42, 43, 44, 45]
    assert [item.outcome for item in batch09] == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
    assert batch09[-1].target_date == BLOCKED_DAY
    assert batch09[-1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch09_passes_resolve_only_pass_dates_and_dec25_stays_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY not in NO_SPECIAL_CHANGE_EVIDENCE
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decisions[BLOCKED_DAY].latest_attempt_id == "batch09:2024-12-25"
    assert decisions[BLOCKED_DAY].latest_attempt_outcome == "BLOCKED"
    assert decisions[BLOCKED_DAY].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decisions[BLOCKED_DAY].contract_verdict == "PASS"


def test_batch09_progression_is_exact_non_starving_and_chronological():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 17
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 17
    assert len(eligible) == 0
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible == []
