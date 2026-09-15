from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch07 as batch07_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch07 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH07_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch07_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH07 = [
    (date(2023, 12, 22), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2024, 1, 15), "MARTIN_LUTHER_KING_DAY"),
    (date(2024, 2, 19), "PRESIDENTS_DAY"),
]
PASS_DAYS = {date(2023, 12, 22), date(2024, 1, 15), date(2024, 2, 19)}
BLOCKED_DAYS = {date(2023, 12, 25), date(2024, 1, 1)}
ALL_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),
    date(2023, 12, 25), date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25),
}


def test_batch07_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH07_TARGETS, tuple)
    assert batch07_targets() == EXPECTED_BATCH07


def test_batch07_historical_membership_is_not_rederived_post_integration():
    first = batch07_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch07_targets() == EXPECTED_BATCH07
    current_eligible = {day for day, _ in eligible_recovery_queue()}
    assert PASS_DAYS.isdisjoint(current_eligible)
    assert BLOCKED_DAYS.isdisjoint(current_eligible)


def test_batch07_calendar_integrates_only_three_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    assert BLOCKED_DAYS <= raw_days


def test_batch07_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch07 = [item for item in attempts if item.attempt_id.startswith("batch07:")]
    assert len(attempts) == 45
    assert [item.attempt_sequence for item in batch07] == [31, 32, 33, 34, 35]
    assert [item.target_date for item in batch07] == [day for day, _ in EXPECTED_BATCH07]
    assert [item.outcome for item in batch07] == ["PASS", "BLOCKED", "BLOCKED", "PASS", "PASS"]
    assert batch07[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert batch07[2].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch07)


def test_batch07_blocked_dates_remain_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ALL_BLOCKED <= raw_days
    assert ALL_BLOCKED.isdisjoint(eligible_days)
    for day in BLOCKED_DAYS:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch07_remains_valid_in_post_batch09_progression_state():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 34
    assert len(attempts) == 45
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 11
    assert len(eligible) == 23
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")


def test_batch07_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "16c6288158985bb3ad68360401b6bdae60687e15"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "a2a59baefd7986f65efb4d625acd2c47c085ae31"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "3feb9f937bf74202f68642992ca3fe8b363398d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch07_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch07_targets).parameters == {}
    source = inspect.getsource(batch07_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source
