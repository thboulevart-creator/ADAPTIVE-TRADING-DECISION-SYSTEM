from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch08 as batch08_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch08 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH08_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PERSISTED_HEAD_REBREAK_COMMIT,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch08_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH08 = [
    (date(2024, 3, 29), "GOOD_FRIDAY"),
    (date(2024, 5, 27), "MEMORIAL_DAY"),
    (date(2024, 6, 19), "JUNETEENTH_OBSERVED"),
    (date(2024, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2024, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
]
ALL_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    date(2022, 7, 1),
    date(2022, 12, 26),
    date(2023, 1, 2),
    date(2023, 7, 4),
    date(2023, 12, 25),
    date(2024, 1, 1),
}
BATCH07_RESOLVED = {
    date(2023, 12, 22),
    date(2024, 1, 15),
    date(2024, 2, 19),
}


def _accepted_membership(candidate: list[tuple[date, str]]) -> bool:
    return candidate == batch08_targets() == eligible_recovery_queue()[:BATCH_SIZE]


def test_batch08_contract_size_and_membership_are_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert isinstance(FROZEN_BATCH08_TARGETS, tuple)
    assert batch08_targets() == EXPECTED_BATCH08


def test_batch08_is_exact_first_five_of_governed_eligible_queue():
    eligible = eligible_recovery_queue()
    assert len(eligible) == 33
    assert eligible[:BATCH_SIZE] == EXPECTED_BATCH08
    assert batch08_targets() == eligible[:BATCH_SIZE]


def test_batch08_raw_unresolved_queue_cannot_substitute_for_governed_queue():
    raw = recovery_queue()
    assert raw[:BATCH_SIZE] != EXPECTED_BATCH08
    assert any(day in ALL_BLOCKED for day, _ in raw[:BATCH_SIZE])
    assert ALL_BLOCKED <= {day for day, _ in raw}
    assert ALL_BLOCKED.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_batch08_members_are_unique_ordered_unresolved_initial_attempts():
    frozen = batch08_targets()
    dates = [day for day, _ in frozen]
    assert len(frozen) == BATCH_SIZE
    assert len(set(frozen)) == BATCH_SIZE
    assert dates == sorted(dates)

    raw_days = {day for day, _ in recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}

    for day, reason in frozen:
        assert day in raw_days
        assert day not in attempted_days
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.calendar_state == "UNRESOLVED"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.contract_verdict == "PASS"


def test_batch08_excludes_same_capability_blocked_and_resolved_batch07_passes():
    frozen_days = {day for day, _ in batch08_targets()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    raw_days = {day for day, _ in recovery_queue()}

    assert frozen_days.isdisjoint(ALL_BLOCKED)
    assert ALL_BLOCKED <= raw_days
    assert ALL_BLOCKED.isdisjoint(eligible_days)
    assert frozen_days.isdisjoint(BATCH07_RESOLVED)
    assert BATCH07_RESOLVED <= set(SPECIAL_SESSION_EVIDENCE)
    assert BATCH07_RESOLVED.isdisjoint(raw_days)


def test_batch08_adversarial_membership_bypasses_are_rejected():
    eligible = eligible_recovery_queue()
    governed = eligible[:BATCH_SIZE]
    later = eligible[BATCH_SIZE]

    attacks = [
        governed[1:] + [later],
        [governed[1], governed[0], *governed[2:]],
        [*governed[:-1], later],
        governed[:-1],
        [*governed, later],
        [(date(2024, 1, 1), "NEW_YEARS_OBSERVED"), *governed[1:]],
        [(date(2024, 2, 19), "PRESIDENTS_DAY"), *governed[1:]],
    ]
    assert _accepted_membership(governed)
    for candidate in attacks:
        assert not _accepted_membership(candidate)


def test_batch08_accessor_returns_copy_and_accepts_no_caller_selection():
    assert inspect.signature(batch08_targets).parameters == {}
    first = batch08_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch08_targets() == EXPECTED_BATCH08


def test_batch08_parent_state_is_exact_at_freeze():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, current_capability_id, attempts = load_attempt_ledger()

    assert len(recovery_queue()) == len(decisions) == 42
    assert len(attempts) == 35
    assert load_material_capability_changes() == []
    assert sum(
        not item.eligible and item.latest_attempt_outcome == "BLOCKED"
        for item in decisions
    ) == 9
    assert len(eligible) == 33
    assert current_capability_id == CURRENT_CAPABILITY_ID
    assert eligible == sorted(eligible, key=lambda item: item[0])


def test_batch08_freeze_provenance_is_exact():
    assert FREEZE_BASELINE_HEAD == "2e9e51cea8342c701eec14d8d86aca215c5b7b62"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "616643e2bfd0b8a8ae3f21352554dc32fdbb503d"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "b4a2f3400b0629e7b1d0a715320735f74293b15a"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch08_freeze_module_has_no_browser_live_selection_or_manual_priority_surface():
    source = inspect.getsource(batch08_module).lower()
    for forbidden in (
        "eligible_recovery_queue(",
        "recovery_queue(",
        "playwright",
        "chromium",
        "probe_candidate",
        "asyncio",
        "expected_outcome",
        "source_availability",
        "holiday_preference",
        "manual_skip",
        "priority=",
    ):
        assert forbidden not in source
