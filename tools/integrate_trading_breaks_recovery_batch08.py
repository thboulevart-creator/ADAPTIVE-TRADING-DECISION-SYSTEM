from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch08 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch08_targets,
)


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch08_adjudication.json"
PROGRESSION_RUNTIME = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
PROGRESSION_TEST = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
BATCH02_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch02.py"
BATCH03_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03_integration.py"
BATCH04_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch04_integration.py"
BATCH05_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05.py"
BATCH05_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05_integration.py"
BATCH06_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch06.py"
BATCH06_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch06_integration.py"
BATCH07_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch07.py"
BATCH07_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch07_integration.py"
BATCH08_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch08.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2024_batch08.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch08_integration.py"

RUN_ID = 34984538763
JOB_ID = 104433139005
PROBE_COMMIT = "5cc4834af2c75de99f6e3427f31ab07b38b42611"
ARTIFACT_ID = 10402433119
ARTIFACT_SHA256 = "644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2024-05-27": {
        "reason_token": "SPECIAL_MEMORIAL_DAY_2024",
        "record_id": "68242",
        "broker_reason": "Memorial Day",
        "request_epoch_ms": 1716768000000,
        "start_utc": "2024-05-27T16:59:59Z",
        "final_closed_minute_utc": "2024-05-27T21:59:59Z",
        "reopen_utc": "2024-05-27T22:00:59Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
    "2024-06-19": {
        "reason_token": "SPECIAL_JUNETEENTH_OBSERVED_2024",
        "record_id": "69037",
        "broker_reason": "Juneteenth Holiday",
        "request_epoch_ms": 1718755200000,
        "start_utc": "2024-06-19T17:00:00Z",
        "final_closed_minute_utc": "2024-06-19T21:59:59Z",
        "reopen_utc": "2024-06-19T22:00:59Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
    "2024-07-03": {
        "reason_token": "SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2024",
        "record_id": "69819",
        "broker_reason": "Independence Day",
        "request_epoch_ms": 1719964800000,
        "start_utc": "2024-07-03T17:14:59Z",
        "final_closed_minute_utc": "2024-07-03T21:59:59Z",
        "reopen_utc": "2024-07-03T22:00:59Z",
        "closed_hours": (18, 19, 20, 21),
    },
    "2024-07-04": {
        "reason_token": "SPECIAL_INDEPENDENCE_DAY_OBSERVED_2024",
        "record_id": "69820",
        "broker_reason": "Independence Day",
        "request_epoch_ms": 1720051200000,
        "start_utc": "2024-07-04T16:59:59Z",
        "final_closed_minute_utc": "2024-07-04T21:59:59Z",
        "reopen_utc": "2024-07-04T22:00:59Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
}
BLOCKED_TARGETS = {
    "2024-03-29": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "66555"),
}
EXPECTED_VERDICTS = ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]
EXPECTED_PRE_ATTEMPTS = 35
EXPECTED_POST_ATTEMPTS = 40
EXPECTED_POST_GLOBAL = (111, 53, 58)
EXPECTED_POST_WINDOW = (68, 30, 38)
EXPECTED_POST_BLOCKED_INELIGIBLE = 10
EXPECTED_POST_ELIGIBLE = 28


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def replace_all_expected(text: str, old: str, new: str, expected_count: int, label: str) -> str:
    count = text.count(old)
    if count != expected_count:
        raise RuntimeError(f"{label}: expected exactly {expected_count} matches, found {count}")
    return text.replace(old, new)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("schema") != "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_ADJUDICATION_V1":
        raise RuntimeError("BATCH08_ADJUDICATION_SCHEMA_MISMATCH")
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH08_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 4, 1, 0):
        raise RuntimeError("BATCH08_ADJUDICATION_ACCOUNTING_MISMATCH")

    expected_provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "probe_commit": PROBE_COMMIT,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
    }
    provenance = report.get("provenance") or {}
    for key, value in expected_provenance.items():
        if provenance.get(key) != value:
            raise RuntimeError(f"BATCH08_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH08_ADJUDICATION_CARDINALITY_MISMATCH")
    frozen = [(day.isoformat(), reason) for day, reason in batch08_targets()]
    observed_identity = [(item.get("target_date"), item.get("candidate_reason")) for item in adjudications]
    if observed_identity != frozen:
        raise RuntimeError("BATCH08_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH08_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        raise RuntimeError("BATCH08_ADJUDICATION_TARGET_SET_MISMATCH")

    for day, expected in PASS_RECORDS.items():
        item = by_day[day]
        checks = {
            "reason": "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED",
            "broker_record_id": expected["record_id"],
            "broker_reason": expected["broker_reason"],
            "break_start_utc": expected["start_utc"],
            "final_closed_minute_utc": expected["final_closed_minute_utc"],
            "reopen_utc": expected["reopen_utc"],
            "fully_closed_hours_utc": list(expected["closed_hours"]),
            "workflow_run": RUN_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_sha256": ARTIFACT_SHA256,
            "probe_commit": PROBE_COMMIT,
        }
        for key, value in checks.items():
            if item.get(key) != value:
                raise RuntimeError(f"BATCH08_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH08_PASS_DOM_WITNESS_MISSING:{day}")

    blocked = by_day["2024-03-29"]
    reason, overlap_id = BLOCKED_TARGETS["2024-03-29"]
    if blocked.get("reason") != reason or blocked.get("overlap_record_id") != overlap_id:
        raise RuntimeError("BATCH08_BLOCKED_GOOD_FRIDAY_EVIDENCE_MISMATCH")
    if "break_start_utc" in blocked or "fully_closed_hours_utc" in blocked:
        raise RuntimeError("BATCH08_BLOCKED_GOOD_FRIDAY_WAS_PROMOTED")
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH08_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH08_CALENDAR_INTEGRATION_DETECTED")
    for day in set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        year, month, dom = [int(x) for x in day.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BATCH08_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch08 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch08:")]
    if batch08:
        if len(batch08) == 5:
            raise RuntimeError("BATCH08_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH08_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH08_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")
    if [x.get("attempt_sequence") for x in attempts[-5:]] != [31, 32, 33, 34, 35]:
        raise RuntimeError("PRE_BATCH08_LEDGER_TAIL_MISMATCH")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 42,
        "attempt_ledger_count": 35,
        "attempted_blocked_ineligible_count": 9,
        "eligible_initial_or_retry_count": 33,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH08_PROGRESSION_STATE_MISMATCH:{key}")


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, record in PASS_RECORDS.items():
        year, month, dom = [int(x) for x in day.split("-")]
        closed_hours = tuple(record["closed_hours"])
        if closed_hours != tuple(range(closed_hours[0], closed_hours[-1] + 1)):
            raise RuntimeError(f"BATCH08_NONCONTIGUOUS_CLOSED_HOURS_REQUIRE_EXPLICIT_ENCODING:{day}")
        closed_expr = f"frozenset(range({closed_hours[0]}, {closed_hours[-1] + 1}))"
        entries.append(
            f'''    date({year}, {month}, {dom}): {{
        "reason": "{record['reason_token']}",
        # Exact broker-native Trading Breaks record {record['record_id']}.
        # Start {record['start_utc']}; final closed instant {record['final_closed_minute_utc']};
        # protocol-derived reopen {record['reopen_utc']}. Only whole target-day UTC
        # buckets proven closed by the independently adjudicated interval are encoded here.
        "fully_closed_hours_utc": {closed_expr},
        "broker_record_id": "{record['record_id']}",
        "broker_reason": "{record['broker_reason']}",
        "artifact_id": {ARTIFACT_ID},
        "artifact_sha256": "{ARTIFACT_SHA256}",
        "probe_commit": "{PROBE_COMMIT}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={record['request_epoch_ms']}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch08_qualification.md"
        ),
    }},
'''
        )
    CALENDAR.write_text(
        replace_once(text, marker, "".join(entries) + marker, "calendar Batch 08 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH08_CAPABILITY_ID_MISMATCH")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    start_sequence = len(attempts) + 1
    if start_sequence != 36:
        raise RuntimeError(f"BATCH08_UNEXPECTED_START_SEQUENCE:{start_sequence}")
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch08_targets(), report["adjudications"], strict=True),
        start=start_sequence,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        if outcome not in {"PASS", "BLOCKED"}:
            raise RuntimeError(f"BATCH08_UNINTEGRABLE_ATTEMPT_OUTCOME:{target_day.isoformat()}:{outcome}")
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch08:{target_day.isoformat()}",
                "batch_contract": BATCH_CONTRACT,
                "target_date": target_day.isoformat(),
                "candidate_reason": candidate_reason,
                "outcome": outcome,
                "adjudication_reason": reason,
                "blocking_reason": reason if outcome == "BLOCKED" else None,
                "capability_id": CAPABILITY_ID,
                "provenance": dict(provenance),
            }
        )
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def update_protocol_test() -> None:
    text = PROTOCOL_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "test_queue_scope_sorted_and_has_42_unresolved_candidates_after_batch07",
        "test_queue_scope_sorted_and_has_38_unresolved_candidates_after_batch08",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 42", "assert len(queue) == 38", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("test_attempt_ledger_preserves_all_thirty_five_historical_attempts_and_duplicate_history", "test_attempt_ledger_preserves_all_forty_historical_attempts_and_duplicate_history", "progression ledger test name"),
        ("assert len(attempts) == 35", "assert len(attempts) == 40", "progression attempt count"),
        ("list(range(1, 36))", "list(range(1, 41))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 35", "len({item.attempt_id for item in attempts}) == 40", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 42", "assert len(decisions) == len(queue) == 38", "progression unresolved count"),
        ("for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4), date(2023, 12, 25), date(2024, 1, 1)):", "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4), date(2023, 12, 25), date(2024, 1, 1), date(2024, 3, 29)):", "progression blocked replay set"),
        ("assert eligible[0][0] > date(2024, 2, 19)", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "progression first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    queue_anchor = "    assert date(2024, 1, 1) in queue_days\n"
    text = replace_once(text, queue_anchor, queue_anchor + "    assert date(2024, 3, 29) in queue_days\n", "progression blocked calendar addition")
    eligible_anchor = "    assert date(2024, 1, 1) not in eligible_days\n"
    text = replace_once(text, eligible_anchor, eligible_anchor + "    assert date(2024, 3, 29) not in eligible_days\n", "progression blocked eligible addition")
    batch07_anchor = "    assert all(day not in eligible_days for day, _ in ((date(2023, 12, 22), 'CHRISTMAS_PRE_HOLIDAY_SESSION'), (date(2023, 12, 25), 'CHRISTMAS_OBSERVED'), (date(2024, 1, 1), 'NEW_YEARS_OBSERVED'), (date(2024, 1, 15), 'MARTIN_LUTHER_KING_DAY'), (date(2024, 2, 19), 'PRESIDENTS_DAY')))\n"
    batch08_exclusion = "    assert all(day not in eligible_days for day, _ in ((date(2024, 3, 29), 'GOOD_FRIDAY'), (date(2024, 5, 27), 'MEMORIAL_DAY'), (date(2024, 6, 19), 'JUNETEENTH_OBSERVED'), (date(2024, 7, 3), 'INDEPENDENCE_PRE_HOLIDAY_SESSION'), (date(2024, 7, 4), 'INDEPENDENCE_DAY_OBSERVED')))\n"
    text = replace_once(text, batch07_anchor, batch07_anchor + batch08_exclusion, "progression Batch08 exclusion")
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_simple_state_tests() -> None:
    text = BATCH02_TEST.read_text(encoding="utf-8")
    BATCH02_TEST.write_text(replace_once(text, "assert len(queue) == 42", "assert len(queue) == 38", "Batch02 current queue count"), encoding="utf-8")

    text = BATCH03_INTEGRATION_TEST.read_text(encoding="utf-8")
    for old, new, label in [
        ("post_batch07_state", "post_batch08_state", "Batch03 state name"),
        ("post_batch07", "post_batch08", "Batch03 history name"),
        ('assert global_report["resolved_candidate_dates"] == 49', 'assert global_report["resolved_candidate_dates"] == 53', "Batch03 global resolved"),
        ('assert global_report["unresolved_candidate_dates"] == 62', 'assert global_report["unresolved_candidate_dates"] == 58', "Batch03 global unresolved"),
        ('assert window_report["resolved_candidate_dates"] == 26', 'assert window_report["resolved_candidate_dates"] == 30', "Batch03 window resolved"),
        ('assert window_report["unresolved_candidate_dates"] == 42', 'assert window_report["unresolved_candidate_dates"] == 38', "Batch03 window unresolved"),
        ("assert len(attempts) == 35", "assert len(attempts) == 40", "Batch03 ledger total"),
    ]:
        text = replace_once(text, old, new, label)
    BATCH03_INTEGRATION_TEST.write_text(text, encoding="utf-8")

    state_files = [
        (BATCH04_INTEGRATION_TEST, "Batch04"),
        (BATCH05_INTEGRATION_TEST, "Batch05 integration"),
        (BATCH06_INTEGRATION_TEST, "Batch06 integration"),
    ]
    for path, prefix in state_files:
        text = path.read_text(encoding="utf-8")
        for old, new, label in [
            ("(111, 49, 62)", "(111, 53, 58)", f"{prefix} global accounting"),
            ("(68, 26, 42)", "(68, 30, 38)", f"{prefix} window accounting"),
            ("assert len(attempts) == 35", "assert len(attempts) == 40", f"{prefix} ledger total"),
            ("assert len(recovery_queue()) == len(decisions) == 42", "assert len(recovery_queue()) == len(decisions) == 38", f"{prefix} queue"),
            ("== 9", "== 10", f"{prefix} blocked count"),
            ("assert len(eligible) == 33", "assert len(eligible) == 28", f"{prefix} eligible count"),
            ("assert eligible[0][0] > date(2024, 2, 19)", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", f"{prefix} first eligible"),
        ]:
            text = replace_once(text, old, new, label)
        path.write_text(text, encoding="utf-8")


def update_batch05_test() -> None:
    text = BATCH05_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "    date(2023, 12, 25), date(2024, 1, 1),\n",
        "    date(2023, 12, 25), date(2024, 1, 1), date(2024, 3, 29),\n",
        "Batch05 blocked set",
    )
    text = replace_all_expected(text, "assert len(attempts) == 35", "assert len(attempts) == 40", 2, "Batch05 ledger total")
    for old, new, label in [
        ("test_all_nine_historical_blocked_dates_remain_unresolved_but_ineligible", "test_all_ten_historical_blocked_dates_remain_unresolved_but_ineligible", "Batch05 blocked test name"),
        ("assert len(recovery_queue()) == len(decisions) == 42", "assert len(recovery_queue()) == len(decisions) == 38", "Batch05 queue"),
        ("== 9", "== 10", "Batch05 blocked count"),
        ("assert len(eligible) == 33", "assert len(eligible) == 28", "Batch05 eligible count"),
        ("assert eligible[0][0] > date(2024, 2, 19)", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "Batch05 first eligible"),
    ]:
        text = replace_once(text, old, new, label)
    BATCH05_TEST.write_text(text, encoding="utf-8")


def update_batch06_test() -> None:
    text = BATCH06_TEST.read_text(encoding="utf-8")
    text = replace_all_expected(text, "assert len(attempts) == 35", "assert len(attempts) == 40", 2, "Batch06 total attempts")
    for old, new, label in [
        ("test_batch06_remains_valid_in_post_batch07_progression_state", "test_batch06_remains_valid_in_post_batch08_progression_state", "Batch06 state test name"),
        ("assert len(recovery_queue()) == len(decisions) == 42", "assert len(recovery_queue()) == len(decisions) == 38", "Batch06 queue"),
        ("== 9", "== 10", "Batch06 blocked count"),
        ("assert len(eligible) == 33", "assert len(eligible) == 28", "Batch06 eligible count"),
        ("assert eligible[0][0] > date(2024, 2, 19)", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "Batch06 first eligible"),
    ]:
        text = replace_once(text, old, new, label)
    BATCH06_TEST.write_text(text, encoding="utf-8")


def update_batch07_tests() -> None:
    text = BATCH07_TEST.read_text(encoding="utf-8")
    text = replace_once(text, "    date(2023, 12, 25), date(2024, 1, 1),\n", "    date(2023, 12, 25), date(2024, 1, 1), date(2024, 3, 29),\n", "Batch07 blocked set")
    text = replace_all_expected(text, "assert len(attempts) == 35", "assert len(attempts) == 40", 2, "Batch07 total attempts")
    for old, new, label in [
        ("test_batch07_postintegration_progression_state_is_exact_and_non_starving", "test_batch07_remains_valid_in_post_batch08_progression_state", "Batch07 state test name"),
        ("assert len(recovery_queue()) == len(decisions) == 42", "assert len(recovery_queue()) == len(decisions) == 38", "Batch07 queue"),
        ("== 9", "== 10", "Batch07 blocked count"),
        ("assert len(eligible) == 33", "assert len(eligible) == 28", "Batch07 eligible count"),
        ("assert eligible[0] == (date(2024, 3, 29), \"GOOD_FRIDAY\")", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "Batch07 first eligible"),
    ]:
        text = replace_once(text, old, new, label)
    BATCH07_TEST.write_text(text, encoding="utf-8")

    text = BATCH07_INTEGRATION_TEST.read_text(encoding="utf-8")
    for old, new, label in [
        ("(111, 49, 62)", "(111, 53, 58)", "Batch07 integration global accounting"),
        ("(68, 26, 42)", "(68, 30, 38)", "Batch07 integration window accounting"),
        ("assert len(attempts) == 35", "assert len(attempts) == 40", "Batch07 integration ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 42", "assert len(recovery_queue()) == len(decisions) == 38", "Batch07 integration queue"),
        ("== 9", "== 10", "Batch07 integration blocked count"),
        ("assert len(eligible) == 33", "assert len(eligible) == 28", "Batch07 integration eligible count"),
        ("assert eligible[0] == (date(2024, 3, 29), \"GOOD_FRIDAY\")", "assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "Batch07 integration first eligible"),
    ]:
        text = replace_once(text, old, new, label)
    BATCH07_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def rewrite_batch08_test() -> None:
    BATCH08_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch08 as batch08_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_batch08 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH08_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch08_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH08 = [
    (date(2024, 3, 29), "GOOD_FRIDAY"),
    (date(2024, 5, 27), "MEMORIAL_DAY"),
    (date(2024, 6, 19), "JUNETEENTH_OBSERVED"),
    (date(2024, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2024, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
]
PASS_DAYS = {date(2024, 5, 27), date(2024, 6, 19), date(2024, 7, 3), date(2024, 7, 4)}
BLOCKED_DAYS = {date(2024, 3, 29)}
ALL_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1),
    date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4), date(2023, 12, 25),
    date(2024, 1, 1), date(2024, 3, 29),
}


def test_batch08_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH08_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert isinstance(FROZEN_BATCH08_TARGETS, tuple)
    assert batch08_targets() == EXPECTED_BATCH08


def test_batch08_historical_membership_is_not_rederived_post_integration():
    first = batch08_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch08_targets() == EXPECTED_BATCH08
    current_eligible = {day for day, _ in eligible_recovery_queue()}
    assert {day for day, _ in EXPECTED_BATCH08}.isdisjoint(current_eligible)


def test_batch08_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    assert BLOCKED_DAYS.isdisjoint(set(NO_SPECIAL_CHANGE_EVIDENCE))
    assert BLOCKED_DAYS <= raw_days


def test_batch08_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch08 = [item for item in attempts if item.attempt_id.startswith("batch08:")]
    assert len(attempts) == 40
    assert [item.attempt_sequence for item in batch08] == [36, 37, 38, 39, 40]
    assert [item.target_date for item in batch08] == [day for day, _ in EXPECTED_BATCH08]
    assert [item.outcome for item in batch08] == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]
    assert batch08[0].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch08)


def test_batch08_blocked_good_friday_remains_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ALL_BLOCKED <= raw_days
    assert ALL_BLOCKED.isdisjoint(eligible_days)
    decision = decisions[date(2024, 3, 29)]
    assert decision.eligible is False
    assert decision.latest_attempt_id == "batch08:2024-03-29"
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch08_postintegration_progression_state_is_exact_and_non_starving():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 38
    assert len(attempts) == 40
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 10
    assert len(eligible) == 28
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")


def test_batch08_freeze_provenance_remains_historical_truth_after_integration():
    assert FREEZE_BASELINE_HEAD == "2e9e51cea8342c701eec14d8d86aca215c5b7b62"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "616643e2bfd0b8a8ae3f21352554dc32fdbb503d"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "b4a2f3400b0629e7b1d0a715320735f74293b15a"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch08_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch08_targets).parameters == {}
    source = inspect.getsource(batch08_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "source_availability", "holiday_preference", "manual_skip", "priority="):
        assert forbidden not in source
''', encoding="utf-8")


def create_calendar_test() -> None:
    CALENDAR_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2024, 5, 27): ("SPECIAL_MEMORIAL_DAY_2024", "68242", frozenset(range(17, 22))),
    date(2024, 6, 19): ("SPECIAL_JUNETEENTH_OBSERVED_2024", "69037", frozenset(range(17, 22))),
    date(2024, 7, 3): ("SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2024", "69819", frozenset(range(18, 22))),
    date(2024, 7, 4): ("SPECIAL_INDEPENDENCE_DAY_OBSERVED_2024", "69820", frozenset(range(17, 22))),
}


def test_batch08_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10402433119
        assert record["artifact_sha256"] == "644e6d6776792dac03e7cb87a3bd63af0be603c6efe951f44c8911ecd9defadd"
        assert record["probe_commit"] == "5cc4834af2c75de99f6e3427f31ab07b38b42611"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch08_blocked_good_friday_is_not_promoted_to_calendar_evidence():
    assert date(2024, 3, 29) not in SPECIAL_SESSION_EVIDENCE


def test_batch08_partial_start_hours_remain_open_and_only_whole_hours_close():
    assert classify_slot(date(2024, 5, 27), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 5, 27), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 5, 27), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 5, 27), 22).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 7, 3), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 7, 3), 18).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 7, 3), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 7, 3), 22).status == EXPECTED_OPEN


def test_batch08_exact_hour_start_closes_that_whole_hour():
    assert classify_slot(date(2024, 6, 19), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 6, 19), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 6, 19), 21).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 6, 19), 22).status == EXPECTED_OPEN
''', encoding="utf-8")


def create_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2024, 5, 27), date(2024, 6, 19), date(2024, 7, 3), date(2024, 7, 4)}
BLOCKED_DAY = date(2024, 3, 29)


def test_batch08_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 53, 58)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 30, 38)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch08_atomic_integration_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch08 = [item for item in attempts if item.attempt_id.startswith("batch08:")]
    assert len(attempts) == 40
    assert [item.attempt_sequence for item in batch08] == [36, 37, 38, 39, 40]
    assert [item.outcome for item in batch08] == ["BLOCKED", "PASS", "PASS", "PASS", "PASS"]
    assert batch08[0].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch08_passes_resolve_only_pass_dates_and_good_friday_stays_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY not in NO_SPECIAL_CHANGE_EVIDENCE
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decisions[BLOCKED_DAY].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decisions[BLOCKED_DAY].latest_attempt_id == "batch08:2024-03-29"
    assert decisions[BLOCKED_DAY].latest_attempt_outcome == "BLOCKED"
    assert decisions[BLOCKED_DAY].contract_verdict == "PASS"


def test_batch08_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 38
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 10
    assert len(eligible) == 28
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")
''', encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_attempt_ledger(report)
    update_protocol_test()
    update_progression_test()
    update_simple_state_tests()
    update_batch05_test()
    update_batch06_test()
    update_batch07_tests()
    rewrite_batch08_test()
    create_calendar_test()
    create_integration_test()
    print("Prepared atomic Batch 08 integration in worktree: 4 PASS calendar dates + 5 factual attempts; 2024-03-29 remains unresolved BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
