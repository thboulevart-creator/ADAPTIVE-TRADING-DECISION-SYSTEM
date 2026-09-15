from __future__ import annotations

import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch06 as integration
from tools.trading_breaks_recovery_batch06 import batch06_targets

EXPECTED_TARGETS = [
    (date(2023, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2023, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
    (date(2023, 9, 4), "LABOR_DAY"),
    (date(2023, 11, 23), "THANKSGIVING_DAY"),
    (date(2023, 11, 24), "THANKSGIVING_FRIDAY"),
]


def test_integration_contract_consumes_exact_historical_batch06_membership():
    assert batch06_targets() == EXPECTED_TARGETS
    report = integration.load_authoritative_adjudication()
    assert [x["target_date"] for x in report["adjudications"]] == [day.isoformat() for day, _ in EXPECTED_TARGETS]
    assert [x["verdict"] for x in report["adjudications"]] == ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]


def test_integration_authorizes_only_four_pass_calendar_records_and_never_july4():
    assert set(integration.PASS_RECORDS) == {"2023-07-03", "2023-09-04", "2023-11-23", "2023-11-24"}
    assert integration.BLOCKED_TARGETS == {"2023-07-04": "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"}
    assert "2023-07-04" not in integration.PASS_RECORDS


def test_integration_provenance_is_locked_to_authoritative_runtime():
    assert integration.RUN_ID == 34954308324
    assert integration.JOB_ID == 104332522379
    assert integration.ARTIFACT_ID == 10390926878
    assert integration.ARTIFACT_SHA256 == "1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052"
    assert integration.PROBE_COMMIT == "e968db2be1fbfd4d2c419f9dad717ca479b52edd"
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_expected_postintegration_accounting_is_locked_and_self_consistent():
    assert integration.EXPECTED_POST_GLOBAL == (111, 46, 65)
    assert integration.EXPECTED_POST_WINDOW == (68, 23, 45)
    assert integration.EXPECTED_POST_ATTEMPTS == 30
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 7
    assert integration.EXPECTED_POST_ELIGIBLE == 38
    assert integration.EXPECTED_POST_WINDOW[1] + integration.EXPECTED_POST_WINDOW[2] == 68
    assert integration.EXPECTED_POST_ELIGIBLE + integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 45


def test_preintegration_guard_rejects_partial_duplicate_or_stale_state_by_design():
    source = inspect.getsource(integration.guard_preintegration_state)
    for token in (
        "PARTIAL_BATCH06_CALENDAR_INTEGRATION_DETECTED",
        "BATCH06_ALREADY_INTEGRATED",
        "PARTIAL_BATCH06_ATTEMPT_LEDGER_DETECTED",
        "BATCH06_ATTEMPTS_ALREADY_INTEGRATED",
        "BATCH06_TARGET_ALREADY_PRESENT_IN_CALENDAR",
        "PRE_BATCH06_PROGRESSION_STATE_MISMATCH",
    ):
        assert token in source


def test_ledger_integrator_records_blocked_as_fact_without_resolving_it():
    ledger_source = inspect.getsource(integration.integrate_attempt_ledger)
    calendar_source = inspect.getsource(integration.integrate_calendar)
    assert '"blocking_reason": reason if outcome == "BLOCKED" else None' in ledger_source
    assert 'outcome not in {"PASS", "BLOCKED"}' in ledger_source
    assert "BLOCKED_TARGETS" not in calendar_source
    assert "2023-07-04" not in calendar_source


def test_integration_has_no_browser_capture_or_live_membership_selection_surface():
    runtime_surface = "\n".join(
        inspect.getsource(callable_obj)
        for callable_obj in (
            integration.load_authoritative_adjudication,
            integration.guard_preintegration_state,
            integration.integrate_calendar,
            integration.integrate_attempt_ledger,
            integration.main,
        )
    ).lower()
    for forbidden in (
        "playwright",
        "chromium",
        "probe_candidate",
        "eligible_recovery_queue()[:5]",
        "recovery_queue()[:5]",
    ):
        assert forbidden not in runtime_surface


def test_main_mutates_calendar_and_ledger_in_same_precommit_worktree_phase():
    source = inspect.getsource(integration.main)
    assert source.index("integrate_calendar()") < source.index("integrate_attempt_ledger(report)")
    assert "create_integration_test()" in source
