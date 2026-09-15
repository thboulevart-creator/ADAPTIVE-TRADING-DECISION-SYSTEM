from __future__ import annotations

import ast
import asyncio
import inspect

import pytest

import tools.trading_breaks_recovery_batch09_execute as execution
from tools.trading_breaks_recovery_batch09 import BATCH_SIZE, batch09_targets


def _called_function_names(source: str) -> set[str]:
    tree = ast.parse(source)
    calls: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            calls.add(node.func.id.lower())
        elif isinstance(node.func, ast.Attribute):
            calls.add(node.func.attr.lower())
    return calls


def test_execution_surface_consumes_only_frozen_batch09_membership():
    source = inspect.getsource(execution)
    calls = _called_function_names(source)
    assert "batch09_targets" in calls
    assert "eligible_recovery_queue" not in calls
    assert "recovery_queue" not in calls
    assert "progression_decisions" not in calls
    assert "derive_batch09_membership" not in calls
    assert "validate_freeze_candidate" not in calls
    assert "probe_candidate" in calls


def test_execution_has_no_caller_injected_target_or_selection_surface():
    assert list(inspect.signature(execution.execute_frozen_batch).parameters) == ["browser"]
    source = inspect.getsource(execution.execute_frozen_batch).lower()
    for forbidden in (
        "expected_outcome",
        "manual_skip",
        "priority",
        "source_availability",
        "holiday_preference",
    ):
        assert forbidden not in source


def test_qualified_capture_probe_itself_does_not_recalculate_membership():
    calls = _called_function_names(inspect.getsource(execution.capture.probe_candidate))
    assert "eligible_recovery_queue" not in calls
    assert "recovery_queue" not in calls
    assert "progression_decisions" not in calls


def test_execution_attempts_every_frozen_member_once_in_exact_order(monkeypatch):
    expected = batch09_targets()
    observed: list[tuple[object, str]] = []

    async def fake_probe(browser, target_day, candidate_reason):
        observed.append((target_day, candidate_reason))
        return {
            "target_date": target_day.isoformat(),
            "candidate_reason": candidate_reason,
            "capture_verdict": "CAPTURED",
        }

    monkeypatch.setattr(execution.capture, "probe_candidate", fake_probe)
    targets, results = asyncio.run(execution.execute_frozen_batch(object()))

    assert targets == expected
    assert observed == expected
    assert len(results) == BATCH_SIZE
    assert [item["target_date"] for item in results] == [day.isoformat() for day, _ in expected]


def test_one_probe_exception_cannot_skip_remaining_frozen_members(monkeypatch):
    expected = batch09_targets()
    observed: list[tuple[object, str]] = []

    async def fake_probe(browser, target_day, candidate_reason):
        observed.append((target_day, candidate_reason))
        if len(observed) == 2:
            raise RuntimeError("synthetic probe failure")
        return {
            "target_date": target_day.isoformat(),
            "candidate_reason": candidate_reason,
            "capture_verdict": "CAPTURED",
        }

    monkeypatch.setattr(execution.capture, "probe_candidate", fake_probe)
    targets, results = asyncio.run(execution.execute_frozen_batch(object()))

    assert targets == expected
    assert observed == expected
    assert len(results) == BATCH_SIZE
    assert results[1]["capture_verdict"] == "BLOCKED"
    assert results[1]["capture_reason"] == "PROBE_EXECUTION_EXCEPTION"


def test_shortened_membership_fails_before_any_probe(monkeypatch):
    expected = batch09_targets()
    calls = 0

    async def fake_probe(browser, target_day, candidate_reason):
        nonlocal calls
        calls += 1
        return {}

    monkeypatch.setattr(execution, "batch09_targets", lambda: expected[:-1])
    monkeypatch.setattr(execution.capture, "probe_candidate", fake_probe)
    with pytest.raises(RuntimeError, match="FROZEN_BATCH09_SIZE_DRIFT"):
        asyncio.run(execution.execute_frozen_batch(object()))
    assert calls == 0


def test_reordered_membership_fails_before_any_probe(monkeypatch):
    expected = batch09_targets()
    attacked = [expected[1], expected[0], *expected[2:]]
    calls = 0

    async def fake_probe(browser, target_day, candidate_reason):
        nonlocal calls
        calls += 1
        return {}

    monkeypatch.setattr(execution, "batch09_targets", lambda: attacked)
    monkeypatch.setattr(execution.capture, "probe_candidate", fake_probe)
    with pytest.raises(RuntimeError, match="FROZEN_BATCH09_ORDER_DRIFT"):
        asyncio.run(execution.execute_frozen_batch(object()))
    assert calls == 0


def test_duplicate_membership_fails_before_any_probe(monkeypatch):
    expected = batch09_targets()
    attacked = [expected[0], expected[0], *expected[2:]]
    calls = 0

    async def fake_probe(browser, target_day, candidate_reason):
        nonlocal calls
        calls += 1
        return {}

    monkeypatch.setattr(execution, "batch09_targets", lambda: attacked)
    monkeypatch.setattr(execution.capture, "probe_candidate", fake_probe)
    with pytest.raises(RuntimeError, match="FROZEN_BATCH09_DUPLICATE_TARGET"):
        asyncio.run(execution.execute_frozen_batch(object()))
    assert calls == 0
