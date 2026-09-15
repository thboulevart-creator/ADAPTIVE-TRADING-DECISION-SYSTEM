from __future__ import annotations

import ast
import inspect
from datetime import date

import tools.freeze_trading_breaks_recovery_batch09 as freeze
from tools.trading_breaks_recovery_batch09 import batch09_targets

HISTORICAL_FROZEN = [
    (date(2024, 9, 2), "LABOR_DAY"),
    (date(2024, 11, 28), "THANKSGIVING_DAY"),
    (date(2024, 11, 29), "THANKSGIVING_FRIDAY"),
    (date(2024, 12, 24), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
]
HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT = HISTORICAL_FROZEN + [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
]


def test_batch09_freeze_historical_identity_is_preserved_without_live_rederivation():
    assert freeze.BATCH_SIZE == 5
    assert batch09_targets() == HISTORICAL_FROZEN
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch09_historical_reorder_attack_is_rejected():
    attacked = [HISTORICAL_FROZEN[1], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    result = freeze.validate_freeze_candidate(attacked, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT)
    assert result["verdict"] == "FAIL"
    assert result["reason"] in {"BATCH_NOT_CHRONOLOGICAL", "BATCH_MEMBERSHIP_REORDERED"}


def test_batch09_historical_skip_substitution_cardinality_and_duplicate_attacks_are_rejected():
    eligible = HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT
    assert freeze.validate_freeze_candidate(eligible[1:6], eligible)["reason"] == "FIRST_ELIGIBLE_MEMBER_SKIPPED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN[:-1], eligible[5]], eligible)["reason"] == "NON_PREFIX_MEMBER_SUBSTITUTED"
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN, eligible[5]], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    duplicated = [HISTORICAL_FROZEN[0], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(duplicated, eligible)["reason"] == "BATCH_DUPLICATE_DATE"


def test_batch09_generator_has_no_executable_browser_probe_surface():
    tree = ast.parse(inspect.getsource(freeze))
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
    assert not any("playwright" in name or "selenium" in name for name in imports)
    assert "probe_candidate" not in calls
    assert "sync_playwright" not in calls
    assert "async_playwright" not in calls
    assert "goto" not in calls
    assert "launch" not in calls


def test_rendered_frozen_module_has_no_live_queue_or_observation_surface():
    source = freeze.render_frozen_module(HISTORICAL_FROZEN).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source
    assert "batch09_targets" in source
    assert "frozen_batch09_targets" in source
