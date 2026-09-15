from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch09 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch09_targets,
)

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch09_adjudication.json"
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
BATCH08_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch08_integration.py"
BATCH09_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch09.py"
BATCH09_FREEZE_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch09_freeze_contract.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2024_batch09.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch09_integration.py"

RUN_ID = 34993614373
JOB_ID = 104464228483
PROBE_COMMIT = "0b5dedf6028add27040af112d0bceef76be25827"
ARTIFACT_ID = 10406357435
ARTIFACT_SHA256 = "dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2024-09-02": {
        "reason_token": "SPECIAL_LABOR_DAY_2024",
        "record_id": "70878",
        "broker_reason": "Labor Day",
        "request_epoch_ms": 1725235200000,
        "start_utc": "2024-09-02T16:59:59Z",
        "final_closed_minute_utc": "2024-09-02T21:59:59Z",
        "reopen_utc": "2024-09-02T22:00:59Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
    "2024-11-28": {
        "reason_token": "SPECIAL_THANKSGIVING_DAY_2024",
        "record_id": "72887",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1732752000000,
        "start_utc": "2024-11-28T17:59:59Z",
        "final_closed_minute_utc": "2024-11-28T22:59:59Z",
        "reopen_utc": "2024-11-28T23:00:59Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2024-11-29": {
        "reason_token": "SPECIAL_THANKSGIVING_FRIDAY_2024",
        "record_id": "72888",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1732838400000,
        "start_utc": "2024-11-29T18:14:59Z",
        "final_closed_minute_utc": "2024-12-01T22:59:59Z",
        "reopen_utc": "2024-12-01T23:00:59Z",
        "closed_hours": (19, 20, 21, 22, 23),
    },
    "2024-12-24": {
        "reason_token": "SPECIAL_CHRISTMAS_PRE_HOLIDAY_SESSION_2024",
        "record_id": "74339",
        "broker_reason": "Christmas",
        "request_epoch_ms": 1734998400000,
        "start_utc": "2024-12-24T18:14:59Z",
        "final_closed_minute_utc": "2024-12-25T22:59:59Z",
        "reopen_utc": "2024-12-25T23:00:59Z",
        "closed_hours": (19, 20, 21, 22, 23),
    },
}
BLOCKED_TARGETS = {
    "2024-12-25": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "74339"),
}
EXPECTED_VERDICTS = ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
EXPECTED_PRE_ATTEMPTS = 40
EXPECTED_POST_ATTEMPTS = 45
EXPECTED_POST_GLOBAL = (111, 57, 54)
EXPECTED_POST_WINDOW = (68, 34, 34)
EXPECTED_POST_BLOCKED_INELIGIBLE = 11
EXPECTED_POST_ELIGIBLE = 23


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def replace_all(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count < 1:
        raise RuntimeError(f"{label}: expected at least one match")
    return text.replace(old, new)


def update_file(path: Path, replacements: list[tuple[str, str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new, label in replacements:
        text = replace_once(text, old, new, f"{path.name}:{label}")
    path.write_text(text, encoding="utf-8")


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("schema") != "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_ADJUDICATION_V1":
        raise RuntimeError("BATCH09_ADJUDICATION_SCHEMA_MISMATCH")
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH09_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 4, 1, 0):
        raise RuntimeError("BATCH09_ADJUDICATION_ACCOUNTING_MISMATCH")

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
            raise RuntimeError(f"BATCH09_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH09_ADJUDICATION_CARDINALITY_MISMATCH")
    frozen = [(day.isoformat(), reason) for day, reason in batch09_targets()]
    observed_identity = [(item.get("target_date"), item.get("candidate_reason")) for item in adjudications]
    if observed_identity != frozen:
        raise RuntimeError("BATCH09_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH09_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        raise RuntimeError("BATCH09_ADJUDICATION_TARGET_SET_MISMATCH")

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
                raise RuntimeError(f"BATCH09_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH09_PASS_DOM_WITNESS_MISSING:{day}")

    blocked = by_day["2024-12-25"]
    reason, overlap_id = BLOCKED_TARGETS["2024-12-25"]
    if blocked.get("reason") != reason or blocked.get("overlap_record_id") != overlap_id:
        raise RuntimeError("BATCH09_BLOCKED_DEC25_EVIDENCE_MISMATCH")
    if blocked.get("capture_verdict") != "CAPTURED":
        raise RuntimeError("BATCH09_BLOCKED_DEC25_CAPTURE_IDENTITY_MISMATCH")
    if "break_start_utc" in blocked or "fully_closed_hours_utc" in blocked:
        raise RuntimeError("BATCH09_BLOCKED_DEC25_WAS_PROMOTED")
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH09_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH09_CALENDAR_INTEGRATION_DETECTED")
    for day in set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        year, month, dom = [int(x) for x in day.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BATCH09_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch09 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch09:")]
    if batch09:
        if len(batch09) == 5:
            raise RuntimeError("BATCH09_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH09_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH09_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")
    if [x.get("attempt_sequence") for x in attempts[-5:]] != [36, 37, 38, 39, 40]:
        raise RuntimeError("PRE_BATCH09_LEDGER_TAIL_MISMATCH")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 38,
        "attempt_ledger_count": 40,
        "attempted_blocked_ineligible_count": 10,
        "eligible_initial_or_retry_count": 28,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH09_PROGRESSION_STATE_MISMATCH:{key}")


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, record in PASS_RECORDS.items():
        closed_hours = tuple(record["closed_hours"])
        if closed_hours != tuple(range(closed_hours[0], closed_hours[-1] + 1)):
            raise RuntimeError(f"BATCH09_NONCONTIGUOUS_CLOSED_HOURS_REQUIRE_EXPLICIT_ENCODING:{day}")
        year, month, dom = [int(x) for x in day.split("-")]
        entries.append(
            f'''    date({year}, {month}, {dom}): {{
        "reason": "{record['reason_token']}",
        # Exact broker-native Trading Breaks record {record['record_id']}.
        # Start {record['start_utc']}; final closed instant {record['final_closed_minute_utc']};
        # protocol-derived reopen {record['reopen_utc']}. Only whole target-day UTC
        # buckets proven closed by the independently adjudicated interval are encoded here.
        "fully_closed_hours_utc": frozenset(range({closed_hours[0]}, {closed_hours[-1] + 1})),
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
            "historical_trading_breaks_recovery_batch09_qualification.md"
        ),
    }},
'''
        )
    new_text = replace_once(text, marker, "".join(entries) + marker, "calendar Batch09 insertion")
    if "date(2024, 12, 25):" in new_text:
        raise RuntimeError("BATCH09_BLOCKED_DEC25_CALENDAR_PROMOTION_ATTEMPT")
    CALENDAR.write_text(new_text, encoding="utf-8")


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH09_CAPABILITY_ID_MISMATCH")
    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    start_sequence = len(attempts) + 1
    if start_sequence != 41:
        raise RuntimeError(f"BATCH09_UNEXPECTED_START_SEQUENCE:{start_sequence}")
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch09_targets(), report["adjudications"], strict=True),
        start=start_sequence,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        if outcome not in {"PASS", "BLOCKED"}:
            raise RuntimeError(f"BATCH09_UNINTEGRABLE_ATTEMPT_OUTCOME:{target_day.isoformat()}:{outcome}")
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch09:{target_day.isoformat()}",
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


def update_protocol_and_progression_tests() -> None:
    update_file(PROTOCOL_TEST, [
        ("test_queue_scope_sorted_and_has_38_unresolved_candidates_after_batch08", "test_queue_scope_sorted_and_has_34_unresolved_candidates_after_batch09", "test name"),
        ("assert len(queue) == 38", "assert len(queue) == 34", "queue count"),
    ])

    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("test_attempt_ledger_preserves_all_forty_historical_attempts_and_duplicate_history", "test_attempt_ledger_preserves_all_forty_five_historical_attempts_and_duplicate_history", "ledger name"),
        ("assert len(attempts) == 40", "assert len(attempts) == 45", "ledger count"),
        ("list(range(1, 41))", "list(range(1, 46))", "ledger sequences"),
        ("len({item.attempt_id for item in attempts}) == 40", "len({item.attempt_id for item in attempts}) == 45", "ledger ids"),
        ("assert len(decisions) == len(queue) == 38", "assert len(decisions) == len(queue) == 34", "unresolved count"),
        ("date(2024, 1, 1), date(2024, 3, 29)):", "date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25)):", "blocked replay set"),
        ("assert eligible[0] == (date(2024, 9, 2), \"LABOR_DAY\")", "assert eligible[0] == (date(2024, 12, 31), \"NEW_YEARS_EVE_CANDIDATE\")", "first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, f"progression:{label}")
    anchor = "    assert date(2024, 3, 29) in queue_days\n"
    text = replace_once(text, anchor, anchor + "    assert date(2024, 12, 25) in queue_days\n", "progression blocked queue addition")
    anchor = "    assert date(2024, 3, 29) not in eligible_days\n"
    text = replace_once(text, anchor, anchor + "    assert date(2024, 12, 25) not in eligible_days\n", "progression blocked eligible addition")
    batch08_line = "    assert all(day not in eligible_days for day, _ in ((date(2024, 3, 29), 'GOOD_FRIDAY'), (date(2024, 5, 27), 'MEMORIAL_DAY'), (date(2024, 6, 19), 'JUNETEENTH_OBSERVED'), (date(2024, 7, 3), 'INDEPENDENCE_PRE_HOLIDAY_SESSION'), (date(2024, 7, 4), 'INDEPENDENCE_DAY_OBSERVED')))\n"
    batch09_line = "    assert all(day not in eligible_days for day, _ in ((date(2024, 9, 2), 'LABOR_DAY'), (date(2024, 11, 28), 'THANKSGIVING_DAY'), (date(2024, 11, 29), 'THANKSGIVING_FRIDAY'), (date(2024, 12, 24), 'CHRISTMAS_PRE_HOLIDAY_SESSION'), (date(2024, 12, 25), 'CHRISTMAS_OBSERVED')))\n"
    text = replace_once(text, batch08_line, batch08_line + batch09_line, "progression Batch09 exclusion")
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_historical_current_state_tests() -> None:
    update_file(BATCH02_TEST, [("assert len(queue) == 38", "assert len(queue) == 34", "queue count")])
    update_file(BATCH03_INTEGRATION_TEST, [
        ("post_batch08_state", "post_batch09_state", "state name"),
        ("post_batch08", "post_batch09", "history name"),
        ('assert global_report["resolved_candidate_dates"] == 53', 'assert global_report["resolved_candidate_dates"] == 57', "global resolved"),
        ('assert global_report["unresolved_candidate_dates"] == 58', 'assert global_report["unresolved_candidate_dates"] == 54', "global unresolved"),
        ('assert window_report["resolved_candidate_dates"] == 30', 'assert window_report["resolved_candidate_dates"] == 34', "window resolved"),
        ('assert window_report["unresolved_candidate_dates"] == 38', 'assert window_report["unresolved_candidate_dates"] == 34', "window unresolved"),
        ("assert len(attempts) == 40", "assert len(attempts) == 45", "attempt total"),
    ])

    state_paths = [BATCH04_INTEGRATION_TEST, BATCH05_INTEGRATION_TEST, BATCH06_INTEGRATION_TEST, BATCH07_INTEGRATION_TEST, BATCH08_INTEGRATION_TEST]
    for path in state_paths:
        text = path.read_text(encoding="utf-8")
        text = replace_all(text, "(111, 53, 58)", "(111, 57, 54)", f"{path.name}:global")
        text = replace_all(text, "(68, 30, 38)", "(68, 34, 34)", f"{path.name}:window")
        text = text.replace("assert len(attempts) == 40", "assert len(attempts) == 45")
        text = text.replace("assert len(recovery_queue()) == len(decisions) == 38", "assert len(recovery_queue()) == len(decisions) == 34")
        text = text.replace("== 10", "== 11")
        text = text.replace("assert len(eligible) == 28", "assert len(eligible) == 23")
        text = text.replace('assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")', 'assert eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")')
        path.write_text(text, encoding="utf-8")

    for path in [BATCH05_TEST, BATCH06_TEST, BATCH07_TEST, BATCH08_TEST]:
        text = path.read_text(encoding="utf-8")
        text = text.replace("assert len(attempts) == 40", "assert len(attempts) == 45")
        text = text.replace("assert len(recovery_queue()) == len(decisions) == 38", "assert len(recovery_queue()) == len(decisions) == 34")
        text = text.replace("== 10", "== 11")
        text = text.replace("assert len(eligible) == 28", "assert len(eligible) == 23")
        text = text.replace('assert eligible[0] == (date(2024, 9, 2), "LABOR_DAY")', 'assert eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")')
        text = text.replace("post_batch08_progression_state", "post_batch09_progression_state")
        path.write_text(text, encoding="utf-8")

    text = BATCH05_TEST.read_text(encoding="utf-8")
    text = replace_once(text, "date(2024, 1, 1), date(2024, 3, 29),\n", "date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25),\n", "Batch05 blocked set")
    text = text.replace("test_all_ten_historical_blocked_dates_remain_unresolved_but_ineligible", "test_all_eleven_historical_blocked_dates_remain_unresolved_but_ineligible")
    BATCH05_TEST.write_text(text, encoding="utf-8")

    for path in [BATCH07_TEST, BATCH08_TEST]:
        text = path.read_text(encoding="utf-8")
        text = replace_once(text, "date(2024, 1, 1), date(2024, 3, 29),\n", "date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25),\n", f"{path.name} blocked set")
        path.write_text(text, encoding="utf-8")


def rewrite_batch09_tests() -> None:
    BATCH09_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch09 as batch09_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE
from tools.trading_breaks_recovery_batch09 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH09_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_INTEGRATION_COMMIT,
    batch09_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH09 = [
    (date(2024, 9, 2), "LABOR_DAY"),
    (date(2024, 11, 28), "THANKSGIVING_DAY"),
    (date(2024, 11, 29), "THANKSGIVING_FRIDAY"),
    (date(2024, 12, 24), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
]
PASS_DAYS = {date(2024, 9, 2), date(2024, 11, 28), date(2024, 11, 29), date(2024, 12, 24)}
BLOCKED_DAY = date(2024, 12, 25)


def test_batch09_contract_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH09_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert isinstance(FROZEN_BATCH09_TARGETS, tuple)
    assert batch09_targets() == EXPECTED_BATCH09


def test_batch09_historical_membership_is_not_rederived_post_integration():
    altered = batch09_targets()
    altered.pop()
    altered.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch09_targets() == EXPECTED_BATCH09
    assert {day for day, _ in EXPECTED_BATCH09}.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_batch09_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY not in NO_SPECIAL_CHANGE_EVIDENCE
    assert BLOCKED_DAY in raw_days


def test_batch09_attempt_ledger_records_all_five_factual_attempts_in_frozen_order():
    _, _, attempts = load_attempt_ledger()
    batch09 = [item for item in attempts if item.attempt_id.startswith("batch09:")]
    assert len(attempts) == 45
    assert [item.attempt_sequence for item in batch09] == [41, 42, 43, 44, 45]
    assert [item.target_date for item in batch09] == [day for day, _ in EXPECTED_BATCH09]
    assert [item.outcome for item in batch09] == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
    assert batch09[-1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch09)


def test_batch09_blocked_dec25_remains_unresolved_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decision = {item.target_date: item for item in progression_decisions()}[BLOCKED_DAY]
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decision.eligible is False
    assert decision.latest_attempt_id == "batch09:2024-12-25"
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch09_postintegration_progression_state_is_exact_and_non_starving():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 34
    assert len(attempts) == 45
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 11
    assert len(eligible) == 23
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")


def test_batch09_freeze_provenance_remains_historical_truth_after_integration():
    assert FREEZE_BASELINE_HEAD == "2e94b8bfa1459d300ee315d0754f84973be2dd1e"
    assert SOURCE_PROGRESSION_INTEGRATION_COMMIT == "aa85a2ade1fe9d9b1ade78f77b9b56c5310a6e74"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "d996d1e3573bfc36437710cc95510ca73b519650"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch09_frozen_module_has_no_live_queue_or_browser_surface():
    assert inspect.signature(batch09_targets).parameters == {}
    source = inspect.getsource(batch09_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "manual_skip", "priority="):
        assert forbidden not in source
''', encoding="utf-8")

    BATCH09_FREEZE_TEST.write_text('''from __future__ import annotations

import ast
import inspect
from datetime import date

import tools.freeze_trading_breaks_recovery_batch09 as freeze
from tools.trading_breaks_recovery_batch09 import batch09_targets

HISTORICAL_FROZEN = [
    (date(2024, 9, 2), "LABOR_DAY"),
    (date(2024, 11, 28), "THANKSGIVING_DAY"),
    (date(2024, 11, 29), "THANKSGIVING_FRIDAY"),
    (date(2024, 12, 24), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
]
HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT = HISTORICAL_FROZEN + [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
]


def test_batch09_freeze_historical_identity_is_preserved_without_live_rederivation():
    assert freeze.BATCH_SIZE == 5
    assert batch09_targets() == HISTORICAL_FROZEN
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT) == {
        "verdict": "PASS",
        "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX",
    }


def test_batch09_historical_reorder_attack_is_rejected():
    attacked = [HISTORICAL_FROZEN[1], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    result = freeze.validate_freeze_candidate(attacked, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT)
    assert result["verdict"] == "FAIL"
    assert result["reason"] in {"BATCH_NOT_CHRONOLOGICAL", "BATCH_MEMBERSHIP_REORDERED"}


def test_batch09_historical_skip_substitution_cardinality_and_duplicate_attacks_are_rejected():
    eligible = HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT
    assert freeze.validate_freeze_candidate(eligible[1:6], eligible)["reason"] == "FIRST_ELIGIBLE_MEMBER_SKIPPED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN[:-1], eligible[5]], eligible)["reason"] == "NON_PREFIX_MEMBER_SUBSTITUTED"
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN, eligible[5]], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    duplicated = [HISTORICAL_FROZEN[0], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(duplicated, eligible)["reason"] == "BATCH_DUPLICATE_DATE"


def test_batch09_generator_has_no_executable_browser_probe_surface():
    tree = ast.parse(inspect.getsource(freeze))
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
    assert not any("playwright" in name or "selenium" in name for name in imports)
    assert "probe_candidate" not in calls
    assert "sync_playwright" not in calls
    assert "async_playwright" not in calls
    assert "goto" not in calls
    assert "launch" not in calls


def test_rendered_frozen_module_has_no_live_queue_or_observation_surface():
    source = freeze.render_frozen_module(HISTORICAL_FROZEN).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source
    assert "batch09_targets" in source
    assert "frozen_batch09_targets" in source
''', encoding="utf-8")


def create_batch09_calendar_test() -> None:
    CALENDAR_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2024, 9, 2): ("SPECIAL_LABOR_DAY_2024", "70878", frozenset(range(17, 22))),
    date(2024, 11, 28): ("SPECIAL_THANKSGIVING_DAY_2024", "72887", frozenset(range(18, 23))),
    date(2024, 11, 29): ("SPECIAL_THANKSGIVING_FRIDAY_2024", "72888", frozenset(range(19, 24))),
    date(2024, 12, 24): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_SESSION_2024", "74339", frozenset(range(19, 24))),
}


def test_batch09_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10406357435
        assert record["artifact_sha256"] == "dc241bac2c214ad562b9efc5ce8f3ad16705d967c82d0bfbd51e5084323220cc"
        assert record["probe_commit"] == "0b5dedf6028add27040af112d0bceef76be25827"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch09_blocked_dec25_is_not_promoted_to_calendar_evidence():
    assert date(2024, 12, 25) not in SPECIAL_SESSION_EVIDENCE


def test_batch09_partial_start_hours_remain_open_and_only_whole_hours_close():
    assert classify_slot(date(2024, 11, 29), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 11, 29), 19).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 12, 24), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 12, 24), 19).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 12, 24), 23).status == EXPECTED_CLOSED


def test_batch09_exact_or_pre_hour_boundary_behavior_is_preserved():
    assert classify_slot(date(2024, 9, 2), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 9, 2), 17).status == EXPECTED_CLOSED
    assert classify_slot(date(2024, 11, 28), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2024, 11, 28), 18).status == EXPECTED_CLOSED
''', encoding="utf-8")


def create_batch09_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import NO_SPECIAL_CHANGE_EVIDENCE, audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2024, 9, 2), date(2024, 11, 28), date(2024, 11, 29), date(2024, 12, 24)}
BLOCKED_DAY = date(2024, 12, 25)


def test_batch09_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 57, 54)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 34, 34)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch09_atomic_integration_records_all_five_factual_attempts_in_frozen_order():
    _, _, attempts = load_attempt_ledger()
    batch09 = [item for item in attempts if item.attempt_id.startswith("batch09:")]
    assert len(attempts) == 45
    assert [item.attempt_sequence for item in batch09] == [41, 42, 43, 44, 45]
    assert [item.outcome for item in batch09] == ["PASS", "PASS", "PASS", "PASS", "BLOCKED"]
    assert batch09[-1].target_date == BLOCKED_DAY
    assert batch09[-1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch09_passes_resolve_only_pass_dates_and_dec25_stays_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY not in NO_SPECIAL_CHANGE_EVIDENCE
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decisions[BLOCKED_DAY].latest_attempt_id == "batch09:2024-12-25"
    assert decisions[BLOCKED_DAY].latest_attempt_outcome == "BLOCKED"
    assert decisions[BLOCKED_DAY].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decisions[BLOCKED_DAY].contract_verdict == "PASS"


def test_batch09_progression_is_exact_non_starving_and_chronological():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 34
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 11
    assert len(eligible) == 23
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")
''', encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_attempt_ledger(report)
    update_protocol_and_progression_tests()
    update_historical_current_state_tests()
    rewrite_batch09_tests()
    create_batch09_calendar_test()
    create_batch09_integration_test()
    print("Prepared atomic Batch 09 integration in worktree: 4 PASS calendar dates + 5 factual attempts; 2024-12-25 remains unresolved BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
