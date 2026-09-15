from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch05 as batch05_module
from tools.trading_breaks_recovery_batch05 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH05_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch05_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH05 = [
    (date(2023, 1, 16), "MARTIN_LUTHER_KING_DAY"),
    (date(2023, 2, 20), "PRESIDENTS_DAY"),
    (date(2023, 4, 7), "GOOD_FRIDAY"),
    (date(2023, 5, 29), "MEMORIAL_DAY"),
    (date(2023, 6, 19), "JUNETEENTH_OBSERVED"),
]
ATTEMPTED_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    date(2022, 7, 1),
    date(2022, 12, 26),
    date(2023, 1, 2),
}


def test_batch05_contract_size_and_exact_frozen_membership():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH05_TARGETS, tuple)
    assert batch05_targets() == EXPECTED_BATCH05


def test_batch05_membership_equals_governed_eligible_prefix_at_freeze():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert batch05_targets() == eligible_recovery_queue()[:BATCH_SIZE]
    assert eligible_recovery_queue()[:5] == EXPECTED_BATCH05


def test_raw_recovery_queue_prefix_is_not_an_admissible_batch05_selection_source():
    raw_prefix = recovery_queue()[:BATCH_SIZE]
    assert raw_prefix != EXPECTED_BATCH05
    assert any(day in ATTEMPTED_BLOCKED for day, _ in raw_prefix)


def test_all_frozen_batch05_members_are_unresolved_initial_attempts_with_no_prior_ledger_entry():
    raw_days = {day for day, _ in recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}

    for day, reason in EXPECTED_BATCH05:
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


def test_all_six_attempted_blocked_dates_remain_unresolved_but_excluded_from_batch05():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    frozen_days = {day for day, _ in EXPECTED_BATCH05}

    assert ATTEMPTED_BLOCKED <= raw_days
    assert ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    assert ATTEMPTED_BLOCKED.isdisjoint(frozen_days)
    for day in ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch05_parent_state_is_exactly_post_batch04_persisted_state():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()

    assert len(recovery_queue()) == len(decisions) == 54
    assert len(attempts) == 20
    assert load_material_capability_changes() == []
    assert sum(
        not item.eligible and item.latest_attempt_outcome == "BLOCKED"
        for item in decisions
    ) == 6
    assert len(eligible) == 48
    assert eligible == sorted(eligible, key=lambda item: item[0])


def test_batch05_freeze_provenance_and_semantic_capability_are_locked():
    assert FREEZE_BASELINE_HEAD == "601310a55b64233ada9e481d3cb2f11dc20a30d5"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "6cafa5337f28c5424cbcc25280c690de702061d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch05_membership_is_chronological_unique_and_accessor_mutation_safe():
    targets = batch05_targets()
    assert len({day for day, _ in targets}) == BATCH_SIZE
    assert targets == sorted(targets, key=lambda item: item[0])

    targets.pop()
    targets.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch05_targets() == EXPECTED_BATCH05


def test_batch05_accessor_has_no_caller_selection_arguments():
    assert inspect.signature(batch05_targets).parameters == {}


def test_batch05_freeze_module_exposes_no_manual_outcome_or_browser_surface():
    source = inspect.getsource(batch05_module).lower()
    for forbidden in (
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
