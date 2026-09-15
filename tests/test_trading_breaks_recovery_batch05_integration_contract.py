from __future__ import annotations

import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch05 as integration
from tools.trading_breaks_recovery_batch05 import batch05_targets


EXPECTED_TARGETS = [
    (date(2023, 1, 16), "MARTIN_LUTHER_KING_DAY"),
    (date(2023, 2, 20), "PRESIDENTS_DAY"),
    (date(2023, 4, 7), "GOOD_FRIDAY"),
    (date(2023, 5, 29), "MEMORIAL_DAY"),
    (date(2023, 6, 19), "JUNETEENTH_OBSERVED"),
]


def test_integration_contract_consumes_exact_historical_batch05_membership():
    assert batch05_targets() == EXPECTED_TARGETS
    report = integration.load_authoritative_adjudication()
    assert [x["target_date"] for x in report["adjudications"]] == [
        day.isoformat() for day, _ in EXPECTED_TARGETS
    ]


def test_integration_authorizes_exactly_five_pass_calendar_records():
    assert set(integration.PASS_RECORDS) == {
        "2023-01-16",
        "2023-02-20",
        "2023-04-07",
        "2023-05-29",
        "2023-06-19",
    }
    assert integration.EXPECTED_VERDICTS == ["PASS"] * 5


def test_integration_provenance_is_locked_to_authoritative_runtime():
    assert integration.RUN_ID == 34947146056
    assert integration.JOB_ID == 104309150262
    assert integration.ARTIFACT_ID == 10386998786
    assert integration.ARTIFACT_SHA256 == "ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c"
    assert integration.PROBE_COMMIT == "33ae476c48372bce64421a411066db2ddea6125c"
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_expected_postintegration_accounting_is_locked_and_self_consistent():
    assert integration.EXPECTED_POST_GLOBAL == (111, 42, 69)
    assert integration.EXPECTED_POST_WINDOW == (68, 19, 49)
    assert integration.EXPECTED_POST_ATTEMPTS == 25
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 6
    assert integration.EXPECTED_POST_ELIGIBLE == 43
    assert integration.EXPECTED_POST_WINDOW[1] + integration.EXPECTED_POST_WINDOW[2] == 68
    assert integration.EXPECTED_POST_ELIGIBLE + integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 49


def test_preintegration_guard_rejects_partial_or_duplicate_state_by_design():
    source = inspect.getsource(integration.guard_preintegration_state)
    assert "PARTIAL_BATCH05_CALENDAR_INTEGRATION_DETECTED" in source
    assert "BATCH05_ALREADY_INTEGRATED" in source
    assert "PARTIAL_BATCH05_ATTEMPT_LEDGER_DETECTED" in source
    assert "BATCH05_ATTEMPTS_ALREADY_INTEGRATED" in source
    assert "BATCH05_TARGET_ALREADY_PRESENT_IN_CALENDAR" in source


def test_ledger_integrator_cannot_record_non_pass_as_batch05_pass():
    source = inspect.getsource(integration.integrate_attempt_ledger)
    assert "BATCH05_NON_PASS_ATTEMPT_REFUSED" in source
    assert '"outcome": "PASS"' in source
    assert '"blocking_reason": None' in source


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
