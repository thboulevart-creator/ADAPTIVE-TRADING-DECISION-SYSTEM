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
    current_capability,
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
ATTEMPTED_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    date(2022, 7, 1),
}


def test_batch04_contract_size_and_exact_frozen_membership():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert len(FROZEN_BATCH04_TARGETS) == BATCH_SIZE
    assert batch04_targets() == EXPECTED_BATCH04


def test_batch04_is_exact_first_five_of_governed_eligible_queue_at_freeze():
    eligible = eligible_recovery_queue()
    assert len(eligible) == 53
    assert eligible[:BATCH_SIZE] == EXPECTED_BATCH04
    assert batch04_targets() == eligible[:BATCH_SIZE]


def test_raw_recovery_prefix_is_not_an_admissible_batch04_source():
    raw = recovery_queue()
    assert len(raw) == 57
    assert raw[:BATCH_SIZE] != EXPECTED_BATCH04
    assert [day for day, _ in raw[:4]] == [
        date(2021, 12, 24),
        date(2021, 12, 31),
        date(2022, 4, 15),
        date(2022, 7, 1),
    ]


def test_batch04_members_are_initial_attempts_unresolved_and_never_attempted():
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}
    decisions = {d.target_date: d for d in progression_decisions()}
    raw_days = {day for day, _ in recovery_queue()}

    for day, reason in EXPECTED_BATCH04:
        assert day in raw_days
        assert day not in attempted_days
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.calendar_state == "UNRESOLVED"
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert decision.contract_verdict == "PASS"


def test_attempted_blocked_dates_remain_unresolved_but_cannot_enter_batch04():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    batch_days = {day for day, _ in batch04_targets()}
    decisions = {d.target_date: d for d in progression_decisions()}

    assert ATTEMPTED_BLOCKED <= raw_days
    assert ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    assert ATTEMPTED_BLOCKED.isdisjoint(batch_days)
    for day in ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch04_membership_is_chronological_unique_and_return_value_is_mutation_safe():
    first = batch04_targets()
    days = [day for day, _ in first]
    assert days == sorted(days)
    assert len(days) == len(set(days))
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch04_targets() == EXPECTED_BATCH04


def test_batch04_accessor_exposes_no_manual_selection_surface():
    assert inspect.signature(batch04_targets).parameters == {}
    source = inspect.getsource(batch04_targets).lower()
    for forbidden in (
        "expected_outcome",
        "priority",
        "manual_skip",
        "holiday_type",
        "source_availability",
        "candidate_override",
    ):
        assert forbidden not in source


def test_freeze_provenance_and_semantic_capability_match_governed_state():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "4d3c5db74ec31215b74799f27cdfe476d513014b"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "d85d6102f8b9d9204521dacfbdcc3a0212f8de5e"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert current_capability().fingerprint() == CURRENT_CAPABILITY_FINGERPRINT
    assert CURRENT_CAPABILITY_FINGERPRINT == (
        "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    )
    assert load_material_capability_changes() == []


def test_parent_progression_state_is_exact_at_batch04_freeze():
    _, _, attempts = load_attempt_ledger()
    decisions = progression_decisions()
    assert len(attempts) == 15
    assert len(decisions) == len(recovery_queue()) == 57
    assert sum(
        (not d.eligible) and d.latest_attempt_outcome == "BLOCKED"
        for d in decisions
    ) == 4
    assert len(eligible_recovery_queue()) == 53


def test_batch04_freeze_module_has_no_browser_or_probe_execution_path():
    source = inspect.getsource(batch04_module).lower()
    assert "playwright" not in source
    assert "chromium" not in source
    assert "probe_candidate" not in source
    assert "asyncio" not in source


def test_frozen_membership_constant_is_tuple_not_mutable_list():
    assert isinstance(FROZEN_BATCH04_TARGETS, tuple)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in FROZEN_BATCH04_TARGETS)
