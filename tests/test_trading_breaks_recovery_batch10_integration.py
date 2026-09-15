from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2024, 12, 31), date(2025, 1, 20), date(2025, 2, 17)}
BLOCKED_DAYS = {date(2025, 1, 1), date(2025, 4, 18)}


def test_batch10_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 65, 46)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 42, 26)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch10_atomic_integration_records_all_five_factual_attempts_in_frozen_order():
    _, _, attempts = load_attempt_ledger()
    batch10 = [item for item in attempts if item.attempt_id.startswith("batch10:")]
    assert len(attempts) == 55
    assert [item.attempt_sequence for item in batch10] == [46, 47, 48, 49, 50]
    assert [item.outcome for item in batch10] == ["PASS", "BLOCKED", "PASS", "PASS", "BLOCKED"]
    assert [item.target_date for item in batch10] == [date(2024, 12, 31), date(2025, 1, 1), date(2025, 1, 20), date(2025, 2, 17), date(2025, 4, 18)]
    assert batch10[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert batch10[4].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch10_only_pass_dates_resolve_and_both_blocked_dates_stay_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    for day in BLOCKED_DAYS:
        assert day not in SPECIAL_SESSION_EVIDENCE
        assert day not in NO_SPECIAL_CHANGE_EVIDENCE
        assert day in raw_days
        assert day not in eligible_days
        assert decisions[day].latest_attempt_outcome == "BLOCKED"
        assert decisions[day].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decisions[day].contract_verdict == "PASS"


def test_batch10_progression_is_exact_non_starving_and_chronological():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 26
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 13
    assert len(eligible) == 13
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2025, 11, 27), "THANKSGIVING_DAY")
