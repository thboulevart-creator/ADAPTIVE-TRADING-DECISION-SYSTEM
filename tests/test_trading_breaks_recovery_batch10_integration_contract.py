from __future__ import annotations

import ast
import inspect

import tools.integrate_trading_breaks_recovery_batch10 as integration
from tools.trading_breaks_recovery_batch10 import batch10_targets


def test_batch10_integration_contract_accepts_only_persisted_adjudication():
    report = integration.load_authoritative_adjudication()
    assert report["verdict"] == "PASS"
    assert (report["attempted"], report["pass"], report["blocked"], report["fail"]) == (5, 3, 2, 0)
    assert [(x["target_date"], x["candidate_reason"]) for x in report["adjudications"]] == [
        (day.isoformat(), reason) for day, reason in batch10_targets()
    ]


def test_batch10_integration_promotable_and_blocked_sets_are_exact():
    assert list(integration.PASS_RECORDS) == ["2024-12-31", "2025-01-20", "2025-02-17"]
    assert integration.BLOCKED_TARGETS == {
        "2025-01-01": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "75799"),
        "2025-04-18": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "80057"),
    }
    assert integration.EXPECTED_VERDICTS == ["PASS", "BLOCKED", "PASS", "PASS", "BLOCKED"]


def test_batch10_integration_expected_accounting_is_locked():
    assert integration.EXPECTED_PRE_ATTEMPTS == 45
    assert integration.EXPECTED_POST_ATTEMPTS == 50
    assert integration.EXPECTED_POST_GLOBAL == (111, 60, 51)
    assert integration.EXPECTED_POST_WINDOW == (68, 37, 31)
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 13
    assert integration.EXPECTED_POST_ELIGIBLE == 18


def test_batch10_integration_has_no_browser_probe_or_live_membership_selection_path():
    tree = ast.parse(inspect.getsource(integration))
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
    assert not any(token in module for module in imports for token in ("playwright", "selenium", "requests", "httpx"))
    for forbidden in ("probe_candidate", "eligible_recovery_queue", "recovery_queue", "goto", "launch"):
        assert forbidden not in calls
