from __future__ import annotations

import inspect
from datetime import date

import tools.freeze_trading_breaks_recovery_batch09 as freeze
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def _baseline() -> list[tuple[date, str]]:
    return list(eligible_recovery_queue()[: freeze.BATCH_SIZE])


def test_batch09_freeze_derives_exact_current_governed_prefix_without_manual_members():
    eligible = eligible_recovery_queue()
    frozen = list(freeze.derive_batch09_membership())
    assert freeze.BATCH_SIZE == 5
    assert len(eligible) == 28
    assert frozen == eligible[: freeze.BATCH_SIZE]
    assert freeze.validate_freeze_candidate(frozen, eligible) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch09_freeze_prestate_is_exact_and_all_members_are_initial_attempts():
    raw = recovery_queue()
    eligible = eligible_recovery_queue()
    decisions = {item.target_date: item for item in progression_decisions()}
    _, current_id, attempts = load_attempt_ledger()
    frozen = freeze.derive_batch09_membership()

    assert len(raw) == 38
    assert len(eligible) == 28
    assert len(attempts) == 40
    assert current_id == freeze.CURRENT_CAPABILITY_ID
    assert load_material_capability_changes() == []
    assert sum(
        not item.eligible and item.latest_attempt_outcome == "BLOCKED"
        for item in decisions.values()
    ) == 10

    attempted_days = {item.target_date for item in attempts}
    for day, reason in frozen:
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert day not in attempted_days


def test_batch09_reorder_attack_is_rejected():
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    attacked = [baseline[1], baseline[0], *baseline[2:]]
    result = freeze.validate_freeze_candidate(attacked, eligible)
    assert result["verdict"] == "FAIL"
    assert result["reason"] in {"BATCH_NOT_CHRONOLOGICAL", "BATCH_MEMBERSHIP_REORDERED"}


def test_batch09_skip_first_attack_is_rejected():
    eligible = eligible_recovery_queue()
    attacked = list(eligible[1 : freeze.BATCH_SIZE + 1])
    assert freeze.validate_freeze_candidate(attacked, eligible) == {
        "verdict": "FAIL",
        "reason": "FIRST_ELIGIBLE_MEMBER_SKIPPED",
    }


def test_batch09_later_eligible_substitution_attack_is_rejected():
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    attacked = [*baseline[:-1], eligible[freeze.BATCH_SIZE]]
    result = freeze.validate_freeze_candidate(attacked, eligible)
    assert result == {"verdict": "FAIL", "reason": "NON_PREFIX_MEMBER_SUBSTITUTED"}


def test_batch09_shortening_and_expansion_attacks_are_rejected():
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    assert freeze.validate_freeze_candidate(baseline[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    assert freeze.validate_freeze_candidate([*baseline, eligible[freeze.BATCH_SIZE]], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"


def test_batch09_duplicate_attack_is_rejected():
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    attacked = [baseline[0], baseline[0], *baseline[2:]]
    assert freeze.validate_freeze_candidate(attacked, eligible) == {
        "verdict": "FAIL",
        "reason": "BATCH_DUPLICATE_DATE",
    }


def test_batch09_same_capability_blocked_reinsertion_attack_is_rejected():
    raw = recovery_queue()
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    blocked = [item for item in raw if item not in eligible]
    assert len(blocked) == 10
    attacked = [blocked[0], *baseline[1:]]
    assert freeze.validate_freeze_candidate(attacked, eligible)["verdict"] == "FAIL"


def test_batch09_resolved_date_reinsertion_is_not_a_governed_prefix():
    eligible = eligible_recovery_queue()
    baseline = _baseline()
    resolved = sorted(set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE))
    attacked = [(resolved[-1], "MANUAL_RESOLVED_REINSERTION"), *baseline[1:]]
    assert freeze.validate_freeze_candidate(attacked, eligible)["verdict"] == "FAIL"


def test_batch09_generator_has_no_browser_probe_or_outcome_priority_surface():
    source = inspect.getsource(freeze).lower()
    for forbidden in (
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


def test_rendered_frozen_module_has_no_live_queue_or_observation_surface():
    source = freeze.render_frozen_module(freeze.derive_batch09_membership()).lower()
    for forbidden in (
        "eligible_recovery_queue(",
        "recovery_queue(",
        "playwright",
        "chromium",
        "probe_candidate",
        "asyncio",
        "expected_outcome",
        "manual_skip",
    ):
        assert forbidden not in source
    assert "frozen_batch09_targets" in source
    assert "batch09_targets" in source
