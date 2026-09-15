from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch09 as batch09_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_batch09 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH09_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_INTEGRATION_COMMIT,
    batch09_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH09 = [
    (date(2024, 9, 2), "LABOR_DAY"),
    (date(2024, 11, 28), "THANKSGIVING_DAY"),
    (date(2024, 11, 29), "THANKSGIVING_FRIDAY"),
    (date(2024, 12, 24), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
]
PASS_DAYS = {date(2024, 9, 2), date(2024, 11, 28), date(2024, 11, 29), date(2024, 12, 24)}
BLOCKED_DAY = date(2024, 12, 25)


def test_batch09_contract_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert isinstance(FROZEN_BATCH09_TARGETS, tuple)
    assert batch09_targets() == EXPECTED_BATCH09


def test_batch09_historical_membership_is_not_rederived_post_integration():
    altered = batch09_targets()
    altered.pop()
    altered.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch09_targets() == EXPECTED_BATCH09
    assert {day for day, _ in EXPECTED_BATCH09}.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_batch09_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY not in NO_SPECIAL_CHANGE_EVIDENCE
    assert BLOCKED_DAY in raw_days


def test_batch09_attempt_ledger_records_all_five_factual_attempts_in_frozen_order():
    _, _, attempts = load_attempt_ledger()
    batch09 = [item for item in attempts if item.attempt_id.startswith("batch09:")]
    assert len(attempts) == 55
    assert [item.attempt_sequence for item in batch09] == [41, 42, 43, 44, 45]
    assert [item.target_date for item in batch09] == [day for day, _ in EXPECTED_BATCH09]
    assert [item.outcome for item in batch09] == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
    assert batch09[-1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch09)


def test_batch09_blocked_dec25_remains_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decision = {item.target_date: item for item in progression_decisions()}[BLOCKED_DAY]
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decision.eligible is False
    assert decision.latest_attempt_id == "batch09:2024-12-25"
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch09_postintegration_progression_state_is_exact_and_non_starving():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 26
    assert len(attempts) == 55
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 13
    assert len(eligible) == 13
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2025, 11, 27), "THANKSGIVING_DAY")


def test_batch09_freeze_provenance_remains_historical_truth_after_integration():
    assert FREEZE_BASELINE_HEAD == "2e94b8bfa1459d300ee315d0754f84973be2dd1e"
    assert SOURCE_PROGRESSION_INTEGRATION_COMMIT == "aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "d996d1e3573bfc36437710cc95510ca73b519650"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch09_frozen_module_has_no_live_queue_or_browser_surface():
    assert inspect.signature(batch09_targets).parameters == {}
    source = inspect.getsource(batch09_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "manual_skip", "priority="):
        assert forbidden not in source
