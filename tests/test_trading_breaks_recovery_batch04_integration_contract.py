from __future__ import annotations

import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch04 as integration
from tools.trading_breaks_recovery_batch04 import batch04_targets


EXPECTED_TARGETS = [
    (date(2022, 11, 24), "THANKSGIVING_DAY"),
    (date(2022, 11, 25), "THANKSGIVING_FRIDAY"),
    (date(2022, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2022, 12, 26), "CHRISTMAS_OBSERVED"),
    (date(2023, 1, 2), "NEW_YEARS_OBSERVED"),
]


def test_integration_contract_consumes_exact_historical_batch04_membership():
    assert batch04_targets() == EXPECTED_TARGETS
    report = integration.load_authoritative_adjudication()
    assert [x["target_date"] for x in report["adjudications"]] == [
        day.isoformat() for day, _ in EXPECTED_TARGETS
    ]


def test_integration_authorizes_exactly_three_pass_calendar_records():
    assert set(integration.PASS_RECORDS) == {
        "2022-11-24",
        "2022-11-25",
        "2022-12-23",
    }
    assert set(integration.BLOCKED_DATES) == {"2022-12-26", "2023-01-02"}
    assert set(integration.PASS_RECORDS).isdisjoint(integration.BLOCKED_DATES)


def test_blocked_dates_cannot_be_silently_promoted_by_calendar_integrator():
    source = inspect.getsource(integration.integrate_calendar)
    for day in integration.BLOCKED_DATES:
        assert day not in integration.PASS_RECORDS
    assert "PASS_RECORDS" in source
    assert "BLOCKED_DATES" not in source


def test_integration_provenance_is_locked_to_authoritative_runtime():
    assert integration.RUN_ID == 34895457466
    assert integration.JOB_ID == 104148201341
    assert integration.ARTIFACT_ID == 10369230708
    assert integration.ARTIFACT_SHA256 == "3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc"
    assert integration.PROBE_COMMIT == "11a81294720898802e49dd1131a64e20e7e7ae3a"
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_expected_postintegration_accounting_is_locked_and_nonnegative():
    assert integration.EXPECTED_POST_GLOBAL == (111, 37, 74)
    assert integration.EXPECTED_POST_WINDOW == (68, 14, 54)
    assert integration.EXPECTED_POST_ATTEMPTS == 20
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 6
    assert integration.EXPECTED_POST_ELIGIBLE == 48
    assert integration.EXPECTED_POST_WINDOW[1] + integration.EXPECTED_POST_WINDOW[2] == 68
    assert integration.EXPECTED_POST_ELIGIBLE + integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 54


def test_preintegration_guard_rejects_partial_or_duplicate_state_by_design():
    source = inspect.getsource(integration.guard_preintegration_state)
    assert "PARTIAL_BATCH04_CALENDAR_INTEGRATION_DETECTED" in source
    assert "BATCH04_ALREADY_INTEGRATED" in source
    assert "PARTIAL_BATCH04_ATTEMPT_LEDGER_DETECTED" in source
    assert "BATCH04_ATTEMPTS_ALREADY_INTEGRATED" in source
    assert "BLOCKED_DATE_ALREADY_PROMOTED" in source


def test_integration_has_no_browser_capture_or_live_membership_selection_surface():
    source = inspect.getsource(integration).lower()
    for forbidden in ("playwright", "chromium", "probe_candidate", "eligible_recovery_queue()[:5]", "recovery_queue()[:5]"):
        assert forbidden not in source
