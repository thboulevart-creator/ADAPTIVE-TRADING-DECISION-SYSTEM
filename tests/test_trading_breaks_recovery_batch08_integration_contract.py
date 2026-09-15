from __future__ import annotations

import inspect
from datetime import date

import tools.integrate_trading_breaks_recovery_batch08 as integration
from tools.trading_breaks_recovery_batch08 import batch08_targets


EXPECTED = [
    (date(2024, 3, 29), "GOOD_FRIDAY"),
    (date(2024, 5, 27), "MEMORIAL_DAY"),
    (date(2024, 6, 19), "JUNETEENTH_OBSERVED"),
    (date(2024, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2024, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
]


def test_integration_contract_consumes_exact_historical_batch08_identity():
    assert batch08_targets() == EXPECTED
    assert set(integration.PASS_RECORDS) == {
        "2024-05-27",
        "2024-06-19",
        "2024-07-03",
        "2024-07-04",
    }
    assert integration.BLOCKED_TARGETS == {
        "2024-03-29": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "66555")
    }
    assert integration.EXPECTED_VERDICTS == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]


def test_integration_contract_locks_authoritative_execution_provenance():
    assert integration.RUN_ID == 34984538763
    assert integration.JOB_ID == 104433139005
    assert integration.ARTIFACT_ID == 10402433119
    assert integration.ARTIFACT_SHA256 == "644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd"
    assert integration.PROBE_COMMIT == "5cc4834af2c75de99f6e3427f31ab07b38b42611"
    assert integration.CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"


def test_integration_contract_locks_exact_pre_and_post_accounting():
    assert integration.EXPECTED_PRE_ATTEMPTS == 35
    assert integration.EXPECTED_POST_ATTEMPTS == 40
    assert integration.EXPECTED_POST_GLOBAL == (111, 53, 58)
    assert integration.EXPECTED_POST_WINDOW == (68, 30, 38)
    assert integration.EXPECTED_POST_BLOCKED_INELIGIBLE == 10
    assert integration.EXPECTED_POST_ELIGIBLE == 28


def test_authoritative_adjudication_is_revalidated_before_any_mutation():
    report = integration.load_authoritative_adjudication()
    assert report["verdict"] == "PASS"
    assert (report["attempted"], report["pass"], report["blocked"], report["fail"]) == (5, 4, 1, 0)
    assert [item["verdict"] for item in report["adjudications"]] == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]


def test_integration_surface_has_no_browser_capture_or_live_membership_recalculation():
    source = inspect.getsource(integration).lower()
    for forbidden in (
        "playwright",
        "chromium",
        "probe_candidate",
        "eligible_recovery_queue(",
        "recovery_queue(",
        "expected_outcome",
        "manual_skip",
        "source_availability",
    ):
        assert forbidden not in source
    assert "batch08_targets()" in source


def test_good_friday_cannot_be_added_to_pass_records_even_if_overlap_exists():
    assert "2024-03-29" not in integration.PASS_RECORDS
    assert integration.BLOCKED_TARGETS["2024-03-29"][0] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"


def test_pass_record_hour_projection_preserves_partial_start_hours():
    assert integration.PASS_RECORDS["2024-05-27"]["closed_hours"] == (17, 18, 19, 20, 21)
    assert integration.PASS_RECORDS["2024-06-19"]["closed_hours"] == (17, 18, 19, 20, 21)
    assert integration.PASS_RECORDS["2024-07-03"]["closed_hours"] == (18, 19, 20, 21)
    assert integration.PASS_RECORDS["2024-07-04"]["closed_hours"] == (17, 18, 19, 20, 21)
