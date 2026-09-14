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

ATTEMPTED_BLOCKED_INELIGIBLE = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
}


def test_batch03_size_is_frozen_at_five():
    assert BATCH_SIZE == 5
    assert len(FROZEN_BATCH03_TARGETS) == BATCH_SIZE


def test_batch03_membership_is_exactly_frozen_expected_membership():
    assert batch03_targets() == EXPECTED_BATCH03


def test_batch03_was_derived_from_attempt_aware_eligible_prefix_at_freeze_state():
    assert eligible_recovery_queue()[:BATCH_SIZE] == EXPECTED_BATCH03


def test_raw_unresolved_prefix_is_not_batch03_selection_source():
    raw_prefix = recovery_queue()[:BATCH_SIZE]
    assert raw_prefix != EXPECTED_BATCH03
    assert {day for day, _ in raw_prefix} & ATTEMPTED_BLOCKED_INELIGIBLE
    assert not ({day for day, _ in EXPECTED_BATCH03} & ATTEMPTED_BLOCKED_INELIGIBLE)


def test_batch03_members_are_chronological_unique_and_execution_eligible():
    targets = batch03_targets()
    days = [day for day, _ in targets]
    eligible = set(eligible_recovery_queue())
    assert days == sorted(days)
    assert len(days) == len(set(days))
    assert all(item in eligible for item in targets)


def test_every_batch03_member_is_an_initial_attempt_with_no_attempt_history():
    decisions = {d.target_date: d for d in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}

    for target_day, target_reason in EXPECTED_BATCH03:
        decision = decisions[target_day]
        assert decision.candidate_reason == target_reason
        assert decision.calendar_state == "UNRESOLVED"
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert target_day not in attempted_days


def test_attempted_blocked_dates_remain_unresolved_but_are_not_batch03_members():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    batch_days = {day for day, _ in batch03_targets()}

    assert ATTEMPTED_BLOCKED_INELIGIBLE <= raw_days
    assert ATTEMPTED_BLOCKED_INELIGIBLE.isdisjoint(eligible_days)
    assert ATTEMPTED_BLOCKED_INELIGIBLE.isdisjoint(batch_days)


def test_batch03_target_accessor_cannot_accept_manual_selection_inputs():
    params = inspect.signature(batch03_targets).parameters
    assert not params


def test_batch03_return_value_cannot_mutate_frozen_membership():
    first = batch03_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch03_targets() == EXPECTED_BATCH03


def test_selection_rule_explicitly_requires_governed_eligible_queue():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert "ELIGIBLE_RECOVERY_QUEUE" in SELECTION_RULE


def test_freeze_provenance_matches_qualified_progression_boundary():
    assert FREEZE_BASELINE_HEAD == "d4dab0a10ba6bc782186159899f7b8225e7aab59"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == (
        "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    )


def test_batch03_membership_contains_no_expected_outcome_or_priority_surface():
    source = inspect.getsource(batch03_targets)
    lowered = source.lower()
    assert "expected_outcome" not in lowered
    assert "priority" not in lowered
    assert "manual_skip" not in lowered
    assert "holiday_type" not in lowered
