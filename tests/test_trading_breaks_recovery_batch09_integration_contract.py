from __future__ import annotations

import ast
import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch09 as integration
from tools.trading_breaks_recovery_batch09 import batch09_targets

EXPECTED = [
    (date(2024, 9, 2), "LABOR_DAY"),
    (date(2024, 11, 28), "THANKSGIVING_DAY"),
    (date(2024, 11, 29), "THANKSGIVING_FRIDAY"),
    (date(2024, 12, 24), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
]


def test_integration_contract_consumes_exact_historical_batch09_identity():
    assert batch09_targets() == EXPECTED
    assert set(integration.PASS_RECORDS) == {
        "2024-09-02",
        "2024-11-28",
        "2024-11-29",
        "2024-12-24",
    }
    assert integration.BLOCKED_TARGETS == {
        "2024-12-25": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "74339")
    }
    assert integration.EXPECTED_VERDICTS == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]


def test_integration_contract_locks_authoritative_execution_provenance():
    assert integration.RUN_ID == 34993614373
    assert integration.JOB_ID == 104464228483
    assert integration.ARTIFACT_ID == 10406357435
    assert integration.ARTIFACT_SHA256 == "dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc"
    assert integration.PROBE_COMMIT == "0b5dedf6028add27040af112d0bceef76be25827"
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_integration_contract_locks_exact_pre_and_post_accounting():
    assert integration.EXPECTED_PRE_ATTEMPTS == 40
    assert integration.EXPECTED_POST_ATTEMPTS == 45
    assert integration.EXPECTED_POST_GLOBAL == (111, 57, 54)
    assert integration.EXPECTED_POST_WINDOW == (68, 34, 34)
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 11
    assert integration.EXPECTED_POST_ELIGIBLE == 23


def test_authoritative_adjudication_is_revalidated_before_any_mutation():
    report = integration.load_authoritative_adjudication()
    assert report["verdict"] == "PASS"
    assert (report["attempted"], report["pass"], report["blocked"], report["fail"]) == (5, 4, 1, 0)
    assert [item["verdict"] for item in report["adjudications"]] == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
    assert report["adjudications"][-1]["target_date"] == "2024-12-25"
    assert report["adjudications"][-1]["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_integration_surface_has_no_browser_capture_or_live_membership_recalculation():
    source = inspect.getsource(integration)
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
    assert not any("playwright" in name or "selenium" in name or "chromium" in name for name in imports)
    assert "probe_candidate" not in calls
    assert "eligible_recovery_queue" not in calls
    assert "recovery_queue" not in calls
    assert "progression_decisions" not in calls
    assert "derive_batch09_membership" not in calls
    assert "batch09_targets" in calls


def test_dec25_blocked_record_cannot_enter_calendar_pass_records():
    assert "2024-12-25" not in integration.PASS_RECORDS
    assert integration.BLOCKED_TARGETS["2024-12-25"][0] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    report = integration.load_authoritative_adjudication()
    blocked = report["adjudications"][-1]
    assert blocked["broker_record_id"] == "74339"
    assert blocked["capture_verdict"] == "CAPTURED"
    assert "fully_closed_hours_utc" not in blocked


def test_pass_record_hour_projection_preserves_partial_start_hours():
    assert integration.PASS_RECORDS["2024-09-02"]["closed_hours"] == (17, 18, 19, 20, 21)
    assert integration.PASS_RECORDS["2024-11-28"]["closed_hours"] == (18, 19, 20, 21, 22)
    assert integration.PASS_RECORDS["2024-11-29"]["closed_hours"] == (19, 20, 21, 22, 23)
    assert integration.PASS_RECORDS["2024-12-24"]["closed_hours"] == (19, 20, 21, 22, 23)
    assert 18 not in integration.PASS_RECORDS["2024-11-29"]["closed_hours"]
    assert 18 not in integration.PASS_RECORDS["2024-12-24"]["closed_hours"]
