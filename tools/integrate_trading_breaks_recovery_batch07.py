from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch07 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch07_targets,
)


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch07_adjudication.json"
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
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2023_2024_batch07.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch07_integration.py"

RUN_ID = 34958083459
JOB_ID = 104344855871
PROBE_COMMIT = "3d434dda9bd293d48cbe2f35df3d464abd5938a4"
ARTIFACT_ID = 10392510730
ARTIFACT_SHA256 = "0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2023-12-22": {
        "reason_token": "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2023",
        "record_id": "63023",
        "broker_reason": "Christmas Day",
        "request_epoch_ms": 1703203200000,
        "start_utc": "2023-12-22T21:14:00Z",
        "final_closed_minute_utc": "2023-12-25T22:59:00Z",
        "reopen_utc": "2023-12-25T23:00:00Z",
        "closed_hours": (22, 23),
    },
    "2024-01-15": {
        "reason_token": "SPECIAL_MARTIN_LUTHER_KING_DAY_2024",
        "record_id": "63883",
        "broker_reason": "Martin Luther King Jr. Day",
        "request_epoch_ms": 1705276800000,
        "start_utc": "2024-01-15T18:00:00Z",
        "final_closed_minute_utc": "2024-01-15T22:59:00Z",
        "reopen_utc": "2024-01-15T23:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2024-02-19": {
        "reason_token": "SPECIAL_PRESIDENTS_DAY_2024",
        "record_id": "65120",
        "broker_reason": "Presidents's Day",
        "request_epoch_ms": 1708300800000,
        "start_utc": "2024-02-19T18:00:00Z",
        "final_closed_minute_utc": "2024-02-19T22:59:59Z",
        "reopen_utc": "2024-02-19T23:00:59Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
}
BLOCKED_TARGETS = {
    "2023-12-25": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "63023"),
    "2024-01-01": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "63024"),
}
EXPECTED_VERDICTS = ["PASS", "BLOCKED", "BLOCKED", "PASS", "PASS"]
EXPECTED_PRE_ATTEMPTS = 30
EXPECTED_POST_ATTEMPTS = 35
EXPECTED_POST_GLOBAL = (111, 49, 62)
EXPECTED_POST_WINDOW = (68, 26, 42)
EXPECTED_POST_BLOCKED_INELIGIBLE = 9
EXPECTED_POST_ELIGIBLE = 33


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
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH07_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 3, 2, 0):
        raise RuntimeError("BATCH07_ADJUDICATION_ACCOUNTING_MISMATCH")

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
            raise RuntimeError(f"BATCH07_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH07_ADJUDICATION_CARDINALITY_MISMATCH")

    frozen = [(day.isoformat(), reason) for day, reason in batch07_targets()]
    observed_identity = [(item.get("target_date"), item.get("candidate_reason")) for item in adjudications]
    if observed_identity != frozen:
        raise RuntimeError("BATCH07_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH07_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        raise RuntimeError("BATCH07_ADJUDICATION_TARGET_SET_MISMATCH")

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
                raise RuntimeError(f"BATCH07_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH07_PASS_DOM_WITNESS_MISSING:{day}")

    for day, (reason, overlap_id) in BLOCKED_TARGETS.items():
        item = by_day[day]
        if item.get("reason") != reason:
            raise RuntimeError(f"BATCH07_BLOCKED_REASON_MISMATCH:{day}")
        if item.get("overlap_record_id") != overlap_id:
            raise RuntimeError(f"BATCH07_BLOCKED_OVERLAP_WITNESS_MISMATCH:{day}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH07_BLOCKED_DOM_WITNESS_MISSING:{day}")
        if "break_start_utc" in item or "fully_closed_hours_utc" in item:
            raise RuntimeError(f"BATCH07_BLOCKED_WAS_PROMOTED_TO_EXECUTABLE_INTERVAL:{day}")
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH07_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH07_CALENDAR_INTEGRATION_DETECTED")
    for day in set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        year, month, dom = [int(x) for x in day.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BATCH07_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch07 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch07:")]
    if batch07:
        if len(batch07) == 5:
            raise RuntimeError("BATCH07_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH07_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH07_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 45,
        "attempt_ledger_count": 30,
        "attempted_blocked_ineligible_count": 7,
        "eligible_initial_or_retry_count": 38,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH07_PROGRESSION_STATE_MISMATCH:{key}")


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, record in PASS_RECORDS.items():
        year, month, dom = [int(x) for x in day.split("-")]
        closed_hours = tuple(record["closed_hours"])
        if closed_hours != tuple(range(closed_hours[0], closed_hours[-1] + 1)):
            raise RuntimeError(f"BATCH07_NONCONTIGUOUS_CLOSED_HOURS_REQUIRE_EXPLICIT_ENCODING:{day}")
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
            "historical_trading_breaks_recovery_batch07_qualification.md"
        ),
    }},
'''
        )
    CALENDAR.write_text(
        replace_once(text, marker, "".join(entries) + marker, "calendar Batch 07 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH07_CAPABILITY_ID_MISMATCH")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch07_targets(), report["adjudications"], strict=True),
        start=31,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        if outcome not in {"PASS", "BLOCKED"}:
            raise RuntimeError(f"BATCH07_UNINTEGRABLE_ATTEMPT_OUTCOME:{target_day.isoformat()}:{outcome}")
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch07:{target_day.isoformat()}",
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
        "test_queue_scope_sorted_and_has_45_unresolved_candidates_after_batch06",
        "test_queue_scope_sorted_and_has_42_unresolved_candidates_after_batch07",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 45", "assert len(queue) == 42", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        (
            "test_attempt_ledger_preserves_all_thirty_historical_attempts_and_duplicate_history",
            "test_attempt_ledger_preserves_all_thirty_five_historical_attempts_and_duplicate_history",
            "progression ledger test name",
        ),
        ("assert len(attempts) == 30", "assert len(attempts) == 35", "progression attempt count"),
        ("list(range(1, 31))", "list(range(1, 36))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 30", "len({item.attempt_id for item in attempts}) == 35", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 45", "assert len(decisions) == len(queue) == 42", "progression unresolved count"),
        (
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4)):",
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4), date(2023, 12, 25), date(2024, 1, 1)):",
            "progression blocked replay set",
        ),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "progression non-starving first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    queue_anchor = "    assert date(2023, 7, 4) in queue_days\n"
    text = replace_once(
        text,
        queue_anchor,
        queue_anchor + "    assert date(2023, 12, 25) in queue_days\n    assert date(2024, 1, 1) in queue_days\n",
        "progression blocked calendar additions",
    )
    eligible_anchor = "    assert date(2023, 7, 4) not in eligible_days\n"
    text = replace_once(
        text,
        eligible_anchor,
        eligible_anchor + "    assert date(2023, 12, 25) not in eligible_days\n    assert date(2024, 1, 1) not in eligible_days\n",
        "progression blocked eligible additions",
    )
    batch06_anchor = "    assert all(day not in eligible_days for day, _ in ((date(2023, 7, 3), 'INDEPENDENCE_PRE_HOLIDAY_SESSION'), (date(2023, 7, 4), 'INDEPENDENCE_DAY_OBSERVED'), (date(2023, 9, 4), 'LABOR_DAY'), (date(2023, 11, 23), 'THANKSGIVING_DAY'), (date(2023, 11, 24), 'THANKSGIVING_FRIDAY')))\n"
    batch07_exclusion = "    assert all(day not in eligible_days for day, _ in ((date(2023, 12, 22), 'CHRISTMAS_PRE_HOLIDAY_SESSION'), (date(2023, 12, 25), 'CHRISTMAS_OBSERVED'), (date(2024, 1, 1), 'NEW_YEARS_OBSERVED'), (date(2024, 1, 15), 'MARTIN_LUTHER_KING_DAY'), (date(2024, 2, 19), 'PRESIDENTS_DAY')))\n"
    text = replace_once(text, batch06_anchor, batch06_anchor + batch07_exclusion, "progression Batch07 exclusion")
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_batch02_test() -> None:
    text = BATCH02_TEST.read_text(encoding="utf-8")
    BATCH02_TEST.write_text(replace_once(text, "assert len(queue) == 45", "assert len(queue) == 42", "Batch02 current queue count"), encoding="utf-8")


def update_batch03_integration_test() -> None:
    text = BATCH03_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("post_batch06_state", "post_batch07_state", "Batch03 state name"),
        ("post_batch06", "post_batch07", "Batch03 history name"),
        ('assert global_report["resolved_candidate_dates"] == 46', 'assert global_report["resolved_candidate_dates"] == 49', "Batch03 global resolved"),
        ('assert global_report["unresolved_candidate_dates"] == 65', 'assert global_report["unresolved_candidate_dates"] == 62', "Batch03 global unresolved"),
        ('assert window_report["resolved_candidate_dates"] == 23', 'assert window_report["resolved_candidate_dates"] == 26', "Batch03 window resolved"),
        ('assert window_report["unresolved_candidate_dates"] == 45', 'assert window_report["unresolved_candidate_dates"] == 42', "Batch03 window unresolved"),
        ("assert len(attempts) == 30", "assert len(attempts) == 35", "Batch03 ledger total"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH03_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch04_integration_test() -> None:
    text = BATCH04_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("(111, 46, 65)", "(111, 49, 62)", "Batch04 global accounting"),
        ("(68, 23, 45)", "(68, 26, 42)", "Batch04 window accounting"),
        ("assert len(attempts) == 30", "assert len(attempts) == 35", "Batch04 ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 45", "assert len(recovery_queue()) == len(decisions) == 42", "Batch04 progression queue"),
        ("== 7", "== 9", "Batch04 blocked count"),
        ("assert len(eligible) == 38", "assert len(eligible) == 33", "Batch04 progression eligible"),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "Batch04 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH04_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch05_test() -> None:
    text = BATCH05_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n",
        "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n    date(2023, 12, 25), date(2024, 1, 1),\n",
        "Batch05 blocked set",
    )
    text = replace_all_expected(
        text,
        "assert len(attempts) == 30",
        "assert len(attempts) == 35",
        2,
        "Batch05 ledger total",
    )
    replacements = [
        ("test_all_seven_historical_blocked_dates_remain_unresolved_but_ineligible", "test_all_nine_historical_blocked_dates_remain_unresolved_but_ineligible", "Batch05 blocked test name"),
        ("assert len(recovery_queue()) == len(decisions) == 45", "assert len(recovery_queue()) == len(decisions) == 42", "Batch05 queue"),
        ("== 7", "== 9", "Batch05 blocked count"),
        ("assert len(eligible) == 38", "assert len(eligible) == 33", "Batch05 eligible count"),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "Batch05 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH05_TEST.write_text(text, encoding="utf-8")


def update_batch05_integration_test() -> None:
    text = BATCH05_INTEGRATION_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n",
        "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n    date(2023, 12, 25), date(2024, 1, 1),\n",
        "Batch05 integration blocked set",
    )
    replacements = [
        ("(111, 46, 65)", "(111, 49, 62)", "Batch05 global accounting"),
        ("(68, 23, 45)", "(68, 26, 42)", "Batch05 window accounting"),
        ("assert len(recovery_queue()) == len(decisions) == 45", "assert len(recovery_queue()) == len(decisions) == 42", "Batch05 queue"),
        ("== 7", "== 9", "Batch05 blocked count"),
        ("assert len(eligible) == 38", "assert len(eligible) == 33", "Batch05 eligible count"),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "Batch05 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH05_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch06_test() -> None:
    text = BATCH06_TEST.read_text(encoding="utf-8")
    text = replace_all_expected(text, "assert len(attempts) == 30", "assert len(attempts) == 35", 2, "Batch06 total attempts")
    replacements = [
        ("test_batch06_postintegration_progression_state_is_exact", "test_batch06_remains_valid_in_post_batch07_progression_state", "Batch06 state test name"),
        ("assert len(recovery_queue()) == len(decisions) == 45", "assert len(recovery_queue()) == len(decisions) == 42", "Batch06 queue"),
        ("== 7", "== 9", "Batch06 blocked count"),
        ("assert len(eligible) == 38", "assert len(eligible) == 33", "Batch06 eligible count"),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "Batch06 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH06_TEST.write_text(text, encoding="utf-8")


def update_batch06_integration_test() -> None:
    text = BATCH06_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("(111, 46, 65)", "(111, 49, 62)", "Batch06 integration global accounting"),
        ("(68, 23, 45)", "(68, 26, 42)", "Batch06 integration window accounting"),
        ("assert len(attempts) == 30", "assert len(attempts) == 35", "Batch06 integration ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 45", "assert len(recovery_queue()) == len(decisions) == 42", "Batch06 integration queue"),
        ("== 7", "== 9", "Batch06 integration blocked count"),
        ("assert len(eligible) == 38", "assert len(eligible) == 33", "Batch06 integration eligible count"),
        ("assert eligible[0][0] > date(2023, 11, 24)", "assert eligible[0][0] > date(2024, 2, 19)", "Batch06 integration first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH06_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def rewrite_batch07_test() -> None:
    BATCH07_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch07 as batch07_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch07 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH07_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch07_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH07 = [
    (date(2023, 12, 22), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2024, 1, 15), "MARTIN_LUTHER_KING_DAY"),
    (date(2024, 2, 19), "PRESIDENTS_DAY"),
]
PASS_DAYS = {date(2023, 12, 22), date(2024, 1, 15), date(2024, 2, 19)}
BLOCKED_DAYS = {date(2023, 12, 25), date(2024, 1, 1)}
ALL_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),
    date(2023, 12, 25), date(2024, 1, 1),
}


def test_batch07_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH07_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH07_TARGETS, tuple)
    assert batch07_targets() == EXPECTED_BATCH07


def test_batch07_historical_membership_is_not_rederived_post_integration():
    first = batch07_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch07_targets() == EXPECTED_BATCH07
    current_eligible = {day for day, _ in eligible_recovery_queue()}
    assert PASS_DAYS.isdisjoint(current_eligible)
    assert BLOCKED_DAYS.isdisjoint(current_eligible)


def test_batch07_calendar_integrates_only_three_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    assert BLOCKED_DAYS <= raw_days


def test_batch07_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch07 = [item for item in attempts if item.attempt_id.startswith("batch07:")]
    assert len(attempts) == 35
    assert [item.attempt_sequence for item in batch07] == [31, 32, 33, 34, 35]
    assert [item.target_date for item in batch07] == [day for day, _ in EXPECTED_BATCH07]
    assert [item.outcome for item in batch07] == ["PASS", "BLOCKED", "BLOCKED", "PASS", "PASS"]
    assert batch07[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert batch07[2].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch07)


def test_batch07_blocked_dates_remain_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ALL_BLOCKED <= raw_days
    assert ALL_BLOCKED.isdisjoint(eligible_days)
    for day in BLOCKED_DAYS:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch07_postintegration_progression_state_is_exact_and_non_starving():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 42
    assert len(attempts) == 35
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 9
    assert len(eligible) == 33
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 3, 29), "GOOD_FRIDAY")


def test_batch07_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "16c6288158985bb3ad68360401b6bdae60687e15"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "a2a59baefd7986f65efb4d625acd2c47c085ae31"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "3feb9f937bf74202f68642992ca3fe8b363398d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch07_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch07_targets).parameters == {}
    source = inspect.getsource(batch07_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source
''', encoding="utf-8")


def create_calendar_test() -> None:
    CALENDAR_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2023, 12, 22): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_2023", "63023", frozenset(range(22, 24))),
    date(2024, 1, 15): ("SPECIAL_MARTIN_LUTHER_KING_DAY_2024", "63883", frozenset(range(18, 23))),
    date(2024, 2, 19): ("SPECIAL_PRESIDENTS_DAY_2024", "65120", frozenset(range(18, 23))),
}


def test_batch07_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10392510730
        assert record["artifact_sha256"] == "0df18b4bfcae04c0bf5e3670e789fc1253fde7317a50d108b35e10dd1cc2676a"
        assert record["probe_commit"] == "3d434dda9bd293d48cbe2f35df3d464abd5938a4"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch07_blocked_dates_are_not_promoted_to_calendar_evidence():
    assert date(2023, 12, 25) not in SPECIAL_SESSION_EVIDENCE
    assert date(2024, 1, 1) not in SPECIAL_SESSION_EVIDENCE


def test_christmas_preholiday_partial_start_hour_remains_open():
    assert classify_slot(date(2023, 12, 22), 21).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 12, 22), 22).status == EXPECTED_CLOSED
    assert classify_slot(date(2023, 12, 22), 23).status == EXPECTED_CLOSED


def test_2024_exact_target_records_encode_only_proven_whole_hours():
    for day in (date(2024, 1, 15), date(2024, 2, 19)):
        assert classify_slot(day, 18).status == EXPECTED_CLOSED
        assert classify_slot(day, 22).status == EXPECTED_CLOSED
        assert classify_slot(day, 23).status == EXPECTED_OPEN
''', encoding="utf-8")


def create_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2023, 12, 22), date(2024, 1, 15), date(2024, 2, 19)}
BLOCKED_DAYS = {date(2023, 12, 25), date(2024, 1, 1)}


def test_batch07_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 49, 62)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 26, 42)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch07_atomic_integration_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch07 = [item for item in attempts if item.attempt_id.startswith("batch07:")]
    assert len(attempts) == 35
    assert [item.attempt_sequence for item in batch07] == [31, 32, 33, 34, 35]
    assert [item.outcome for item in batch07] == ["PASS", "BLOCKED", "BLOCKED", "PASS", "PASS"]
    assert batch07[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert batch07[2].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch07_passes_resolve_only_pass_dates_and_blocked_remain_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    assert BLOCKED_DAYS.isdisjoint(set(NO_SPECIAL_CHANGE_EVIDENCE))
    assert BLOCKED_DAYS <= raw_days
    assert BLOCKED_DAYS.isdisjoint(eligible_days)
    for day in BLOCKED_DAYS:
        assert decisions[day].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decisions[day].latest_attempt_outcome == "BLOCKED"
        assert decisions[day].contract_verdict == "PASS"


def test_batch07_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 42
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 9
    assert len(eligible) == 33
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 3, 29), "GOOD_FRIDAY")
''', encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_attempt_ledger(report)
    update_protocol_test()
    update_progression_test()
    update_batch02_test()
    update_batch03_integration_test()
    update_batch04_integration_test()
    update_batch05_test()
    update_batch05_integration_test()
    update_batch06_test()
    update_batch06_integration_test()
    rewrite_batch07_test()
    create_calendar_test()
    create_integration_test()
    print("Prepared atomic Batch 07 integration in worktree: 3 PASS calendar dates + 5 factual attempts; 2023-12-25 and 2024-01-01 remain unresolved BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
