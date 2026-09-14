from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch04 as batch04_module
from tools.trading_breaks_recovery_batch04 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH04_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch04_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH04 = [
    (date(2022, 11, 24), "THANKSGIVING_DAY"),
    (date(2022, 11, 25), "THANKSGIVING_FRIDAY"),
    (date(2022, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2022, 12, 26), "CHRISTMAS_OBSERVED"),
    (date(2023, 1, 2), "NEW_YEARS_OBSERVED"),
]
PASS_DAYS = {date(2022, 11, 24), date(2022, 11, 25), date(2022, 12, 23)}
BLOCKED_DAYS = {date(2022, 12, 26), date(2023, 1, 2)}
ALL_ATTEMPTED_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),
}


def test_batch04_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH04_TARGETS, tuple)
    assert batch04_targets() == EXPECTED_BATCH04


def test_batch04_historical_membership_is_immutable_and_not_rederived_post_integration():
    first = batch04_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch04_targets() == EXPECTED_BATCH04
    assert {day for day, _ in EXPECTED_BATCH04}.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_post_integration_calendar_contains_only_batch04_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS <= raw_days


def test_post_integration_attempt_ledger_records_all_five_batch04_attempts():
    _, _, attempts = load_attempt_ledger()
    batch04 = [item for item in attempts if item.attempt_id.startswith("batch04:")]
    assert [item.attempt_sequence for item in batch04] == [16, 17, 18, 19, 20]
    assert [item.target_date for item in batch04] == [day for day, _ in EXPECTED_BATCH04]
    assert [item.outcome for item in batch04] == ["PASS", "PASS", "PASS", "BLOCKED", "BLOCKED"]
    assert [item.blocking_reason for item in batch04[-2:]] == [
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
    ]
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch04)


def test_all_six_attempted_blocked_dates_remain_unresolved_but_ineligible_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert ALL_ATTEMPTED_BLOCKED <= raw_days
    assert ALL_ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    for day in ALL_ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "4d3c5db74ec31215b74799f27cdfe476d513014b"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "d85d6102f8b9d9204521dacfbdcc3a0212f8de5e"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    assert load_material_capability_changes() == []


def test_batch04_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch04_targets).parameters == {}
    source = inspect.getsource(batch04_module).lower()
    for forbidden in ("playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source
