from __future__ import annotations

import inspect
from datetime import date

from tools.trading_breaks_recovery_batch03 import (
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH03_TARGETS,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch03_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH03 = [
    (date(2022, 5, 30), "MEMORIAL_DAY"),
    (date(2022, 6, 20), "JUNETEENTH_OBSERVED"),
    (date(2022, 7, 1), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2022, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
    (date(2022, 9, 5), "LABOR_DAY"),
]
PASS_DAYS = {
    date(2022, 5, 30),
    date(2022, 6, 20),
    date(2022, 7, 4),
    date(2022, 9, 5),
}
BLOCKED_DAY = date(2022, 7, 1)
ALL_ATTEMPTED_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    BLOCKED_DAY,
}


def test_batch03_size_and_historical_membership_remain_frozen():
    assert BATCH_SIZE == 5
    assert len(FROZEN_BATCH03_TARGETS) == BATCH_SIZE
    assert batch03_targets() == EXPECTED_BATCH03


def test_batch03_historical_membership_is_chronological_unique_and_immutable():
    first = batch03_targets()
    days = [day for day, _ in first]
    assert days == sorted(days)
    assert len(days) == len(set(days))
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch03_targets() == EXPECTED_BATCH03


def test_post_adjudication_calendar_integrates_only_batch03_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY in raw_days


def test_post_adjudication_attempt_ledger_records_all_five_batch03_attempts():
    _, _, attempts = load_attempt_ledger()
    batch03 = [item for item in attempts if item.attempt_id.startswith("batch03:")]
    assert [item.attempt_sequence for item in batch03] == [11, 12, 13, 14, 15]
    assert [item.target_date for item in batch03] == [day for day, _ in EXPECTED_BATCH03]
    assert [item.outcome for item in batch03] == ["PASS", "PASS", "BLOCKED", "PASS", "PASS"]
    assert batch03[2].blocking_reason == "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch03)


def test_all_attempted_blocked_dates_remain_unresolved_but_ineligible_same_capability():
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


def test_batch03_dates_cannot_reenter_execution_projection_after_attempt():
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    assert {day for day, _ in EXPECTED_BATCH03}.isdisjoint(eligible_days)


def test_batch03_target_accessor_cannot_accept_manual_selection_inputs():
    assert inspect.signature(batch03_targets).parameters == {}


def test_selection_rule_and_freeze_provenance_remain_historical_truth():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "d4dab0a10ba6bc782186159899f7b8225e7aab59"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == (
        "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    )


def test_batch03_membership_contains_no_expected_outcome_or_priority_surface():
    source = inspect.getsource(batch03_targets).lower()
    assert "expected_outcome" not in source
    assert "priority" not in source
    assert "manual_skip" not in source
    assert "holiday_type" not in source
