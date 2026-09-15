from __future__ import annotations

import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch07 as integration
from tools.trading_breaks_recovery_batch07 import batch07_targets


EXPECTED_TARGETS = [
    (date(2023, 12, 22), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2024, 1, 15), "MARTIN_LUTHER_KING_DAY"),
    (date(2024, 2, 19), "PRESIDENTS_DAY"),
]


def test_integration_contract_consumes_exact_historical_batch07_membership():
    assert batch07_targets() == EXPECTED_TARGETS
    report = integration.load_authoritative_adjudication()
    assert [x["target_date"] for x in report["adjudications"]] == [
        day.isoformat() for day, _ in EXPECTED_TARGETS
    ]
    assert [x["verdict"] for x in report["adjudications"]] == [
        "PASS", "BLOCKED", "BLOCKED", "PASS", "PASS"
    ]


def test_integration_authorizes_only_three_pass_calendar_records():
    assert set(integration.PASS_RECORDS) == {
        "2023-12-22", "2024-01-15", "2024-02-19"
    }
    assert integration.BLOCKED_TARGETS == {
        "2023-12-25": (
            "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "63023"
        ),
        "2024-01-01": (
            "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "63024"
        ),
    }
    assert set(integration.PASS_RECORDS).isdisjoint(integration.BLOCKED_TARGETS)


def test_integration_provenance_is_locked_to_authoritative_runtime():
    assert integration.RUN_ID == 34958083459
    assert integration.JOB_ID == 104344855871
    assert integration.ARTIFACT_ID == 10392510730
    assert integration.ARTIFACT_SHA256 == (
        "0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a"
    )
    assert integration.PROBE_COMMIT == (
        "3d434dda9bd293d48cbe2f35df3d464abd5938a4"
    )
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_expected_postintegration_accounting_is_locked_and_self_consistent():
    assert integration.EXPECTED_POST_GLOBAL == (111, 49, 62)
    assert integration.EXPECTED_POST_WINDOW == (68, 26, 42)
    assert integration.EXPECTED_POST_ATTEMPTS == 35
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 9
    assert integration.EXPECTED_POST_ELIGIBLE == 33
    assert integration.EXPECTED_POST_WINDOW[1] + integration.EXPECTED_POST_WINDOW[2] == 68
    assert (
        integration.EXPECTED_POST_ELIGIBLE
        + integration.EXPECTED_POST_BLOCKED_INELIGIBLE
        == integration.EXPECTED_POST_WINDOW[2]
    )


def test_preintegration_guard_rejects_partial_duplicate_or_stale_state_by_design():
    source = inspect.getsource(integration.guard_preintegration_state)
    for token in (
        "PARTIAL_BATCH07_CALENDAR_INTEGRATION_DETECTED",
        "BATCH07_ALREADY_INTEGRATED",
        "PARTIAL_BATCH07_ATTEMPT_LEDGER_DETECTED",
        "BATCH07_ATTEMPTS_ALREADY_INTEGRATED",
        "BATCH07_TARGET_ALREADY_PRESENT_IN_CALENDAR",
        "PRE_BATCH07_PROGRESSION_STATE_MISMATCH",
    ):
        assert token in source


def test_authoritative_adjudication_guard_rejects_blocked_promotion():
    source = inspect.getsource(integration.load_authoritative_adjudication)
    assert "BATCH07_BLOCKED_WAS_PROMOTED_TO_EXECUTABLE_INTERVAL" in source
    assert '"break_start_utc" in item' in source
    assert '"fully_closed_hours_utc" in item' in source


def test_ledger_integrator_records_blocked_as_fact_without_resolving_it():
    ledger_source = inspect.getsource(integration.integrate_attempt_ledger)
    calendar_source = inspect.getsource(integration.integrate_calendar)
    assert '"blocking_reason": reason if outcome == "BLOCKED" else None' in ledger_source
    assert 'outcome not in {"PASS", "BLOCKED"}' in ledger_source
    assert "BLOCKED_TARGETS" not in calendar_source
    assert "2023-12-25" not in calendar_source
    assert "2024-01-01" not in calendar_source


def test_integration_has_no_negative_evidence_browser_capture_or_live_selection_surface():
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
        "no_special_change_evidence",
        "playwright",
        "chromium",
        "probe_candidate",
        "eligible_recovery_queue()[:5]",
        "recovery_queue()[:5]",
    ):
        assert forbidden not in runtime_surface


def test_generated_integration_test_checks_negative_evidence_from_coverage_module_only():
    source = inspect.getsource(integration.create_integration_test)
    assert (
        "from tools.dukascopy_usatech_calendar_coverage import "
        "NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage"
    ) in source
    assert (
        "from tools.dukascopy_usatech_calendar import "
        "NO_SPECIAL_CHANGE_EVIDENCE"
    ) not in source
    assert "BLOCKED_DAYS.isdisjoint(set(NO_SPECIAL_CHANGE_EVIDENCE))" in source


def test_main_mutates_calendar_and_ledger_in_same_precommit_worktree_phase():
    source = inspect.getsource(integration.main)
    assert source.index("integrate_calendar()") < source.index(
        "integrate_attempt_ledger(report)"
    )
    assert "create_calendar_test()" in source
    assert "create_integration_test()" in source
