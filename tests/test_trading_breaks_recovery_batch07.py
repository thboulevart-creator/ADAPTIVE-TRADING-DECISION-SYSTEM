from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch07 as batch07_module
from tools.trading_breaks_recovery_batch07 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH07_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PERSISTED_HEAD_REBREAK_COMMIT,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch07_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH07 = [
    (date(2023, 12, 22), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2024, 1, 15), "MARTIN_LUTHER_KING_DAY"),
    (date(2024, 2, 19), "PRESIDENTS_DAY"),
]
ATTEMPTED_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    date(2022, 7, 1),
    date(2022, 12, 26),
    date(2023, 1, 2),
    date(2023, 7, 4),
}
BATCH06_PASS_DAYS = {
    date(2023, 7, 3),
    date(2023, 9, 4),
    date(2023, 11, 23),
    date(2023, 11, 24),
}


def test_batch07_contract_size_and_exact_frozen_membership():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH07_TARGETS, tuple)
    assert batch07_targets() == EXPECTED_BATCH07


def test_batch07_membership_equals_governed_post_batch06_eligible_prefix_at_freeze():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    eligible = eligible_recovery_queue()
    assert eligible[:BATCH_SIZE] == EXPECTED_BATCH07
    assert batch07_targets() == eligible[:BATCH_SIZE]


def test_raw_recovery_queue_prefix_cannot_substitute_for_attempt_aware_batch07_membership():
    raw_prefix = recovery_queue()[:BATCH_SIZE]
    assert raw_prefix != EXPECTED_BATCH07
    assert any(day in ATTEMPTED_BLOCKED for day, _ in raw_prefix)
    assert ATTEMPTED_BLOCKED.isdisjoint({day for day, _ in EXPECTED_BATCH07})


def test_batch07_rejects_skip_reorder_substitution_and_cardinality_drift_against_governed_prefix():
    eligible = eligible_recovery_queue()
    governed = eligible[:BATCH_SIZE]
    skipped = governed[1:] + [eligible[BATCH_SIZE]]
    reordered = [governed[1], governed[0], *governed[2:]]
    substituted = [eligible[BATCH_SIZE], *governed[1:]]
    shortened = governed[:-1]
    expanded = governed + [eligible[BATCH_SIZE]]

    assert skipped != EXPECTED_BATCH07
    assert reordered != EXPECTED_BATCH07
    assert substituted != EXPECTED_BATCH07
    assert shortened != EXPECTED_BATCH07
    assert expanded != EXPECTED_BATCH07
    assert batch07_targets() == governed == EXPECTED_BATCH07


def test_all_frozen_batch07_members_are_unresolved_initial_attempts_with_no_prior_attempt():
    raw_days = {day for day, _ in recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}

    for day, reason in EXPECTED_BATCH07:
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


def test_same_capability_blocked_dates_remain_unresolved_ineligible_and_excluded():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    frozen_days = {day for day, _ in EXPECTED_BATCH07}

    assert ATTEMPTED_BLOCKED <= raw_days
    assert ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    assert ATTEMPTED_BLOCKED.isdisjoint(frozen_days)
    for day in ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch06_passes_cannot_reenter_batch07_membership():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    frozen_days = {day for day, _ in EXPECTED_BATCH07}
    assert BATCH06_PASS_DAYS.isdisjoint(raw_days)
    assert BATCH06_PASS_DAYS.isdisjoint(eligible_days)
    assert BATCH06_PASS_DAYS.isdisjoint(frozen_days)


def test_batch07_parent_state_is_exactly_persisted_post_batch06_state():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()

    assert len(recovery_queue()) == len(decisions) == 45
    assert len(attempts) == 30
    assert load_material_capability_changes() == []
    assert sum(
        not item.eligible and item.latest_attempt_outcome == "BLOCKED"
        for item in decisions
    ) == 7
    assert len(eligible) == 38
    assert eligible == sorted(eligible, key=lambda item: item[0])


def test_batch07_freeze_provenance_and_capability_identity_are_locked():
    assert FREEZE_BASELINE_HEAD == "16c6288158985bb3ad68360401b6bdae60687e15"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "a2a59baefd7986f65efb4d625acd2c47c085ae31"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "3feb9f937bf74202f68642992ca3fe8b363398d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch07_membership_is_chronological_unique_and_accessor_mutation_safe():
    targets = batch07_targets()
    assert len(targets) == BATCH_SIZE
    assert len({day for day, _ in targets}) == BATCH_SIZE
    assert targets == sorted(targets, key=lambda item: item[0])

    targets.pop()
    targets.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch07_targets() == EXPECTED_BATCH07


def test_batch07_accessor_has_no_caller_selection_arguments():
    assert inspect.signature(batch07_targets).parameters == {}


def test_batch07_freeze_module_exposes_no_live_selection_manual_outcome_or_browser_surface():
    source = inspect.getsource(batch07_module).lower()
    for forbidden in (
        "eligible_recovery_queue(",
        "recovery_queue(",
        "playwright",
        "chromium",
        "probe_candidate",
        "asyncio",
        "expected_outcome",
        "priority",
        "manual_skip",
        "holiday_type",
        "source_availability",
        "candidate_override",
    ):
        assert forbidden not in source
