from __future__ import annotations

import ast
import inspect

import tools.freeze_trading_breaks_recovery_batch10 as freeze
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def _eligible() -> list[tuple]:
    return list(eligible_recovery_queue())


def _baseline() -> list[tuple]:
    return _eligible()[: freeze.BATCH_SIZE]


def test_batch10_freeze_derives_exact_current_governed_prefix_without_manual_members():
    eligible = _eligible()
    frozen = list(freeze.derive_batch10_membership())
    assert freeze.BATCH_SIZE == 5
    assert len(recovery_queue()) == freeze.EXPECTED_RECOVERY_QUEUE_COUNT == 34
    assert len(eligible) == freeze.EXPECTED_ELIGIBLE_QUEUE_COUNT == 23
    _, _, attempts = load_attempt_ledger()
    assert len(attempts) == freeze.EXPECTED_ATTEMPT_COUNT == 45
    assert load_material_capability_changes() == []
    assert frozen == eligible[: freeze.BATCH_SIZE]
    assert freeze.validate_freeze_candidate(frozen, eligible) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch10_members_are_exactly_unresolved_eligible_initial_attempts():
    frozen = list(freeze.derive_batch10_membership())
    raw = set(recovery_queue())
    eligible = set(eligible_recovery_queue())
    decisions = {item.target_date: item for item in progression_decisions()}
    _, _, attempts = load_attempt_ledger()
    attempted_days = {item.target_date for item in attempts}
    resolved_days = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)

    assert set(frozen) <= raw
    assert set(frozen) <= eligible
    assert {day for day, _ in frozen}.isdisjoint(attempted_days)
    assert {day for day, _ in frozen}.isdisjoint(resolved_days)
    assert [day for day, _ in frozen] == sorted(day for day, _ in frozen)
    for day, reason in frozen:
        decision = decisions[day]
        assert decision.candidate_reason == reason
        assert decision.eligible is True
        assert decision.reason == "INITIAL_ATTEMPT"
        assert decision.latest_attempt_id is None
        assert decision.latest_attempt_outcome is None
        assert decision.contract_verdict == "PASS"


def test_batch10_reorder_attack_is_rejected():
    eligible = _eligible()
    baseline = _baseline()
    attacked = [baseline[1], baseline[0], *baseline[2:]]
    result = freeze.validate_freeze_candidate(attacked, eligible)
    assert result["verdict"] == "FAIL"
    assert result["reason"] in {"BATCH_NOT_CHRONOLOGICAL", "BATCH_MEMBERSHIP_REORDERED"}


def test_batch10_skip_first_attack_is_rejected():
    eligible = _eligible()
    attacked = eligible[1 : freeze.BATCH_SIZE + 1]
    assert freeze.validate_freeze_candidate(attacked, eligible) == {
        "verdict": "FAIL",
        "reason": "FIRST_ELIGIBLE_MEMBER_SKIPPED",
    }


def test_batch10_later_eligible_substitution_attack_is_rejected():
    eligible = _eligible()
    baseline = _baseline()
    attacked = [*baseline[:-1], eligible[freeze.BATCH_SIZE]]
    assert freeze.validate_freeze_candidate(attacked, eligible) == {
        "verdict": "FAIL",
        "reason": "NON_PREFIX_MEMBER_SUBSTITUTED",
    }


def test_batch10_cardinality_change_attacks_are_rejected():
    eligible = _eligible()
    baseline = _baseline()
    assert freeze.validate_freeze_candidate(baseline[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    assert freeze.validate_freeze_candidate([*baseline, eligible[freeze.BATCH_SIZE]], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"


def test_batch10_duplicate_attack_is_rejected():
    eligible = _eligible()
    baseline = _baseline()
    attacked = [baseline[0], baseline[0], *baseline[2:]]
    assert freeze.validate_freeze_candidate(attacked, eligible) == {
        "verdict": "FAIL",
        "reason": "BATCH_DUPLICATE_DATE",
    }


def test_batch10_raw_queue_bypass_and_same_capability_blocked_reinsertion_are_rejected():
    raw = list(recovery_queue())
    eligible = _eligible()
    baseline = _baseline()
    blocked = [item for item in raw if item not in eligible]
    assert len(blocked) == freeze.EXPECTED_BLOCKED_INELIGIBLE_COUNT == 11
    assert freeze.validate_freeze_candidate(raw[: freeze.BATCH_SIZE], eligible)["verdict"] == "FAIL"
    attacked = [blocked[0], *baseline[1:]]
    assert freeze.validate_freeze_candidate(attacked, eligible)["verdict"] == "FAIL"


def test_batch10_resolved_date_reinsertion_is_rejected():
    eligible = _eligible()
    baseline = _baseline()
    resolved = sorted(set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE))
    attacked = [(resolved[-1], "MANUAL_RESOLVED_REINSERTION"), *baseline[1:]]
    assert freeze.validate_freeze_candidate(attacked, eligible)["verdict"] == "FAIL"


def test_batch10_generator_selection_is_mechanical_and_has_no_observation_or_outcome_surface():
    source = inspect.getsource(freeze)
    tree = ast.parse(source)
    imports: set[str] = set()
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.lower() for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add((node.module or "").lower())
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id.lower())
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr.lower())

    assert "eligible_recovery_queue" in calls
    assert "recovery_queue" in calls
    assert "progression_decisions" in calls
    assert not any(
        token in module
        for module in imports
        for token in ("playwright", "selenium", "requests", "httpx", "batch10_adjudication", "batch10_execute")
    )
    for forbidden in (
        "probe_candidate",
        "sync_playwright",
        "async_playwright",
        "goto",
        "launch",
        "adjudicate_runtime",
    ):
        assert forbidden not in calls

    derive_tree = ast.parse(inspect.getsource(freeze.derive_batch10_membership))
    assert not any(
        isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "date"
        for node in ast.walk(derive_tree)
    )


def test_batch10_rendered_snapshot_has_no_live_queue_or_observation_surface():
    source = freeze.render_frozen_module(freeze.derive_batch10_membership()).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source
    assert "playwright" not in source
    assert "batch10_targets" in source
    assert "frozen_batch10_targets" in source
