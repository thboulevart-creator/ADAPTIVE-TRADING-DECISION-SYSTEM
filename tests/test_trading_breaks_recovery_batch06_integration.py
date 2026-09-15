from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2023, 7, 3), date(2023, 9, 4), date(2023, 11, 23), date(2023, 11, 24)}
BLOCKED_DAY = date(2023, 7, 4)


def test_batch06_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 46, 65)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 23, 45)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch06_atomic_integration_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch06 = [item for item in attempts if item.attempt_id.startswith("batch06:")]
    assert len(attempts) == 30
    assert [item.attempt_sequence for item in batch06] == [26, 27, 28, 29, 30]
    assert [item.outcome for item in batch06] == ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]
    assert batch06[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch06_passes_resolve_only_pass_dates_and_blocked_remains_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decisions[BLOCKED_DAY].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decisions[BLOCKED_DAY].latest_attempt_outcome == "BLOCKED"
    assert decisions[BLOCKED_DAY].contract_verdict == "PASS"


def test_batch06_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 45
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 7
    assert len(eligible) == 38
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 11, 24)
