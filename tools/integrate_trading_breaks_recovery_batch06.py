from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch06 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch06_targets,
)


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch06_adjudication.json"
PROGRESSION_RUNTIME = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
PROGRESSION_TEST = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
BATCH02_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch02.py"
BATCH03_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03_integration.py"
BATCH04_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch04_integration.py"
BATCH05_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05.py"
BATCH05_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05_integration.py"
BATCH06_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch06.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2023_batch06.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch06_integration.py"

RUN_ID = 34954308324
JOB_ID = 104332522379
PROBE_COMMIT = "e968db2be1fbfd4d2c419f9dad717ca479b52edd"
ARTIFACT_ID = 10390926878
ARTIFACT_SHA256 = "1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2023-07-03": {
        "reason_token": "SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2023",
        "record_id": "56233",
        "broker_reason": "Independence Day",
        "request_epoch_ms": 1688342400000,
        "start_utc": "2023-07-03T17:14:00Z",
        "final_closed_minute_utc": "2023-07-04T21:59:00Z",
        "reopen_utc": "2023-07-04T22:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22, 23),
    },
    "2023-09-04": {
        "reason_token": "SPECIAL_LABOR_DAY_2023",
        "record_id": "57462",
        "broker_reason": "Labor Day",
        "request_epoch_ms": 1693785600000,
        "start_utc": "2023-09-04T16:59:00Z",
        "final_closed_minute_utc": "2023-09-04T21:59:00Z",
        "reopen_utc": "2023-09-04T22:00:00Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
    "2023-11-23": {
        "reason_token": "SPECIAL_THANKSGIVING_DAY_2023",
        "record_id": "59358",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1700697600000,
        "start_utc": "2023-11-23T16:59:00Z",
        "final_closed_minute_utc": "2023-11-23T22:59:00Z",
        "reopen_utc": "2023-11-23T23:00:00Z",
        "closed_hours": (17, 18, 19, 20, 21, 22),
    },
    "2023-11-24": {
        "reason_token": "SPECIAL_THANKSGIVING_FRIDAY_2023",
        "record_id": "59359",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1700784000000,
        "start_utc": "2023-11-24T17:14:00Z",
        "final_closed_minute_utc": "2023-11-26T22:59:00Z",
        "reopen_utc": "2023-11-26T23:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22, 23),
    },
}
BLOCKED_TARGETS = {
    "2023-07-04": "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
}
EXPECTED_VERDICTS = ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]
EXPECTED_PRE_ATTEMPTS = 25
EXPECTED_POST_ATTEMPTS = 30
EXPECTED_POST_GLOBAL = (111, 46, 65)
EXPECTED_POST_WINDOW = (68, 23, 45)
EXPECTED_POST_BLOCKED_INELIGIBLE = 7
EXPECTED_POST_ELIGIBLE = 38


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH06_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 4, 1, 0):
        raise RuntimeError("BATCH06_ADJUDICATION_ACCOUNTING_MISMATCH")

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
            raise RuntimeError(f"BATCH06_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH06_ADJUDICATION_CARDINALITY_MISMATCH")

    frozen = [(day.isoformat(), reason) for day, reason in batch06_targets()]
    observed_identity = [(item.get("target_date"), item.get("candidate_reason")) for item in adjudications]
    if observed_identity != frozen:
        raise RuntimeError("BATCH06_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH06_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        raise RuntimeError("BATCH06_ADJUDICATION_TARGET_SET_MISMATCH")

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
                raise RuntimeError(f"BATCH06_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH06_PASS_DOM_WITNESS_MISSING:{day}")

    blocked = by_day["2023-07-04"]
    if blocked.get("reason") != BLOCKED_TARGETS["2023-07-04"]:
        raise RuntimeError("BATCH06_BLOCKED_REASON_MISMATCH")
    if blocked.get("overlap_record_id") != "56233":
        raise RuntimeError("BATCH06_BLOCKED_OVERLAP_WITNESS_MISMATCH")
    if blocked.get("dom_witness_present") is not True:
        raise RuntimeError("BATCH06_BLOCKED_DOM_WITNESS_MISSING")
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH06_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH06_CALENDAR_INTEGRATION_DETECTED")
    for day in set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        year, month, dom = [int(x) for x in day.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BATCH06_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch06 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch06:")]
    if batch06:
        if len(batch06) == 5:
            raise RuntimeError("BATCH06_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH06_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH06_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 49,
        "attempt_ledger_count": 25,
        "attempted_blocked_ineligible_count": 6,
        "eligible_initial_or_retry_count": 43,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH06_PROGRESSION_STATE_MISMATCH:{key}")


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, record in PASS_RECORDS.items():
        year, month, dom = [int(x) for x in day.split("-")]
        closed_hours = tuple(record["closed_hours"])
        closed_expr = f"frozenset(range({closed_hours[0]}, {closed_hours[-1] + 1}))"
        entries.append(
            f'''    date({year}, {month}, {dom}): {{
        "reason": "{record['reason_token']}",
        # Exact broker-native Trading Breaks record {record['record_id']}.
        # Start {record['start_utc']}; final closed minute {record['final_closed_minute_utc']};
        # calibrated reopen {record['reopen_utc']}. Only whole target-day UTC
        # buckets proven closed by the adjudicated interval are encoded here.
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
            "historical_trading_breaks_recovery_batch06_qualification.md"
        ),
    }},
'''
        )
    CALENDAR.write_text(
        replace_once(text, marker, "".join(entries) + marker, "calendar Batch 06 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH06_CAPABILITY_ID_MISMATCH")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch06_targets(), report["adjudications"], strict=True),
        start=26,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        if outcome not in {"PASS", "BLOCKED"}:
            raise RuntimeError(f"BATCH06_UNINTEGRABLE_ATTEMPT_OUTCOME:{target_day.isoformat()}:{outcome}")
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch06:{target_day.isoformat()}",
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
        "test_queue_scope_sorted_and_has_49_unresolved_candidates_after_batch05",
        "test_queue_scope_sorted_and_has_45_unresolved_candidates_after_batch06",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 49", "assert len(queue) == 45", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        (
            "test_attempt_ledger_preserves_all_twenty_five_historical_attempts_and_duplicate_history",
            "test_attempt_ledger_preserves_all_thirty_historical_attempts_and_duplicate_history",
            "progression ledger test name",
        ),
        ("assert len(attempts) == 25", "assert len(attempts) == 30", "progression attempt count"),
        ("list(range(1, 26))", "list(range(1, 31))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 25", "len({item.attempt_id for item in attempts}) == 30", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 49", "assert len(decisions) == len(queue) == 45", "progression unresolved count"),
        (
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2)):",
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4)):",
            "progression blocked replay set",
        ),
        ("assert eligible[0][0] > date(2023, 6, 19)", "assert eligible[0][0] > date(2023, 11, 24)", "progression non-starving first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    anchor = "    assert date(2023, 1, 2) in queue_days\n"
    text = replace_once(text, anchor, anchor + "    assert date(2023, 7, 4) in queue_days\n", "progression blocked calendar set")
    eligible_anchor = "    assert date(2023, 1, 2) not in eligible_days\n"
    text = replace_once(text, eligible_anchor, eligible_anchor + "    assert date(2023, 7, 4) not in eligible_days\n", "progression blocked eligible set")
    batch05_anchor = "    assert all(day not in eligible_days for day, _ in ((date(2023, 1, 16), 'MARTIN_LUTHER_KING_DAY'), (date(2023, 2, 20), 'PRESIDENTS_DAY'), (date(2023, 4, 7), 'GOOD_FRIDAY'), (date(2023, 5, 29), 'MEMORIAL_DAY'), (date(2023, 6, 19), 'JUNETEENTH_OBSERVED')))\n"
    batch06_exclusion = "    assert all(day not in eligible_days for day, _ in ((date(2023, 7, 3), 'INDEPENDENCE_PRE_HOLIDAY_SESSION'), (date(2023, 7, 4), 'INDEPENDENCE_DAY_OBSERVED'), (date(2023, 9, 4), 'LABOR_DAY'), (date(2023, 11, 23), 'THANKSGIVING_DAY'), (date(2023, 11, 24), 'THANKSGIVING_FRIDAY')))\n"
    text = replace_once(text, batch05_anchor, batch05_anchor + batch06_exclusion, "progression Batch06 exclusion")
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_batch02_test() -> None:
    text = BATCH02_TEST.read_text(encoding="utf-8")
    BATCH02_TEST.write_text(replace_once(text, "assert len(queue) == 49", "assert len(queue) == 45", "Batch02 current queue count"), encoding="utf-8")


def update_batch03_integration_test() -> None:
    text = BATCH03_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("post_batch05_state", "post_batch06_state", "Batch03 state name"),
        ("post_batch05", "post_batch06", "Batch03 history name"),
        ('assert global_report["resolved_candidate_dates"] == 42', 'assert global_report["resolved_candidate_dates"] == 46', "Batch03 global resolved"),
        ('assert global_report["unresolved_candidate_dates"] == 69', 'assert global_report["unresolved_candidate_dates"] == 65', "Batch03 global unresolved"),
        ('assert window_report["resolved_candidate_dates"] == 19', 'assert window_report["resolved_candidate_dates"] == 23', "Batch03 window resolved"),
        ('assert window_report["unresolved_candidate_dates"] == 49', 'assert window_report["unresolved_candidate_dates"] == 45', "Batch03 window unresolved"),
        ("assert len(attempts) == 25", "assert len(attempts) == 30", "Batch03 ledger total"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH03_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch04_integration_test() -> None:
    text = BATCH04_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("(111, 42, 69)", "(111, 46, 65)", "Batch04 global accounting"),
        ("(68, 19, 49)", "(68, 23, 45)", "Batch04 window accounting"),
        ("assert len(attempts) == 25", "assert len(attempts) == 30", "Batch04 ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 49", "assert len(recovery_queue()) == len(decisions) == 45", "Batch04 progression queue"),
        ("== 6", "== 7", "Batch04 blocked count"),
        ("assert len(eligible) == 43", "assert len(eligible) == 38", "Batch04 progression eligible"),
        ("assert eligible[0][0] > date(2023, 6, 19)", "assert eligible[0][0] > date(2023, 11, 24)", "Batch04 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH04_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch05_test() -> None:
    text = BATCH05_TEST.read_text(encoding="utf-8")
    text = replace_once(text, "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),\n", "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n", "Batch05 blocked set")
    attempt_count = "assert len(attempts) == 25"
    if text.count(attempt_count) != 2:
        raise RuntimeError(f"Batch05 total attempts: expected exactly two matches, found {text.count(attempt_count)}")
    text = text.replace(attempt_count, "assert len(attempts) == 30")
    replacements = [
        ("test_all_six_historical_blocked_dates_remain_unresolved_but_ineligible", "test_all_seven_historical_blocked_dates_remain_unresolved_but_ineligible", "Batch05 blocked test name"),
        ("assert len(recovery_queue()) == len(decisions) == 49", "assert len(recovery_queue()) == len(decisions) == 45", "Batch05 queue"),
        ("== 6", "== 7", "Batch05 blocked count"),
        ("assert len(eligible) == 43", "assert len(eligible) == 38", "Batch05 eligible count"),
        ("assert eligible[0][0] > date(2023, 6, 19)", "assert eligible[0][0] > date(2023, 11, 24)", "Batch05 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH05_TEST.write_text(text, encoding="utf-8")


def update_batch05_integration_test() -> None:
    text = BATCH05_INTEGRATION_TEST.read_text(encoding="utf-8")
    text = replace_once(text, "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),\n", "    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2), date(2023, 7, 4),\n", "Batch05 integration blocked set")
    replacements = [
        ("(111, 42, 69)", "(111, 46, 65)", "Batch05 global accounting"),
        ("(68, 19, 49)", "(68, 23, 45)", "Batch05 window accounting"),
        ("assert len(attempts) == 25", "assert len(attempts) == 30", "Batch05 ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 49", "assert len(recovery_queue()) == len(decisions) == 45", "Batch05 queue"),
        ("== 6", "== 7", "Batch05 blocked count"),
        ("assert len(eligible) == 43", "assert len(eligible) == 38", "Batch05 eligible count"),
        ("assert eligible[0][0] > date(2023, 6, 19)", "assert eligible[0][0] > date(2023, 11, 24)", "Batch05 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH05_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def rewrite_batch06_test() -> None:
    BATCH06_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch06 as batch06_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch06 import (
    BATCH_CONTRACT, BATCH_SIZE, CURRENT_CAPABILITY_FINGERPRINT, CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD, FROZEN_BATCH06_TARGETS, PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE, SOURCE_PERSISTED_HEAD_REBREAK_COMMIT, SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch06_targets,
)
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

EXPECTED_BATCH06 = [
    (date(2023, 7, 3), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2023, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
    (date(2023, 9, 4), "LABOR_DAY"),
    (date(2023, 11, 23), "THANKSGIVING_DAY"),
    (date(2023, 11, 24), "THANKSGIVING_FRIDAY"),
]
PASS_DAYS = {date(2023, 7, 3), date(2023, 9, 4), date(2023, 11, 23), date(2023, 11, 24)}
BLOCKED_DAY = date(2023, 7, 4)


def test_batch06_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH06_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH06_TARGETS, tuple)
    assert batch06_targets() == EXPECTED_BATCH06


def test_batch06_historical_membership_is_not_rederived_post_integration():
    first = batch06_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch06_targets() == EXPECTED_BATCH06
    assert PASS_DAYS.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_batch06_calendar_integrates_only_four_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY in raw_days


def test_batch06_attempt_ledger_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch06 = [item for item in attempts if item.attempt_id.startswith("batch06:")]
    assert len(attempts) == 30
    assert [item.attempt_sequence for item in batch06] == [26, 27, 28, 29, 30]
    assert [item.target_date for item in batch06] == [day for day, _ in EXPECTED_BATCH06]
    assert [item.outcome for item in batch06] == ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]
    assert batch06[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch06)


def test_batch06_blocked_july4_remains_unresolved_and_same_capability_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decision = {item.target_date: item for item in progression_decisions()}[BLOCKED_DAY]
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decision.eligible is False
    assert decision.latest_attempt_outcome == "BLOCKED"
    assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decision.contract_verdict == "PASS"


def test_batch06_postintegration_progression_state_is_exact():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 45
    assert len(attempts) == 30
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 7
    assert len(eligible) == 38
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 11, 24)


def test_batch06_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "289d7f4432efba4ad2bc1e97d5b23f14f587019e"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "99c2f38842a0c4ea66ba6ff90496380986d02e52"
    assert SOURCE_PERSISTED_HEAD_REBREAK_COMMIT == "70428e536689793a74420d35c84744b8ad0f2f3d"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch06_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch06_targets).parameters == {}
    source = inspect.getsource(batch06_module).lower()
    for forbidden in ("eligible_recovery_queue(", "recovery_queue(", "playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source
''', encoding="utf-8")


def create_calendar_test() -> None:
    CALENDAR_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import EXPECTED_CLOSED, EXPECTED_OPEN, SPECIAL_SESSION_EVIDENCE, classify_slot

EXPECTED = {
    date(2023, 7, 3): ("SPECIAL_INDEPENDENCE_PRE_HOLIDAY_SESSION_2023", "56233", frozenset(range(18, 24))),
    date(2023, 9, 4): ("SPECIAL_LABOR_DAY_2023", "57462", frozenset(range(17, 22))),
    date(2023, 11, 23): ("SPECIAL_THANKSGIVING_DAY_2023", "59358", frozenset(range(17, 23))),
    date(2023, 11, 24): ("SPECIAL_THANKSGIVING_FRIDAY_2023", "59359", frozenset(range(18, 24))),
}


def test_batch06_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10390926878
        assert record["artifact_sha256"] == "1e21a4fac890059f436c1488407b5f8ca92809dda18aa220e6af41ee6dfa1052"
        assert record["probe_commit"] == "e968db2be1fbfd4d2c419f9dad717ca479b52edd"
        assert record["fully_closed_hours_utc"] == closed_hours


def test_batch06_blocked_july4_is_not_promoted_to_calendar_evidence():
    assert date(2023, 7, 4) not in SPECIAL_SESSION_EVIDENCE


def test_partial_start_hours_remain_open():
    assert classify_slot(date(2023, 7, 3), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 7, 3), 18).status == EXPECTED_CLOSED
    assert classify_slot(date(2023, 11, 24), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 11, 24), 18).status == EXPECTED_CLOSED


def test_multiday_records_project_only_target_day_whole_hours():
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 7, 3)]["fully_closed_hours_utc"] == frozenset(range(18, 24))
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 11, 24)]["fully_closed_hours_utc"] == frozenset(range(18, 24))
''', encoding="utf-8")


def create_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import eligible_recovery_queue, load_attempt_ledger, load_material_capability_changes, progression_decisions
from tools.trading_breaks_recovery_protocol import recovery_queue

PASS_DAYS = {date(2023, 7, 3), date(2023, 9, 4), date(2023, 11, 23), date(2023, 11, 24)}
BLOCKED_DAY = date(2023, 7, 4)


def test_batch06_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 46, 65)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 23, 45)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch06_atomic_integration_records_all_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch06 = [item for item in attempts if item.attempt_id.startswith("batch06:")]
    assert len(attempts) == 30
    assert [item.attempt_sequence for item in batch06] == [26, 27, 28, 29, 30]
    assert [item.outcome for item in batch06] == ["PASS", "BLOCKED", "PASS", "PASS", "PASS"]
    assert batch06[1].blocking_reason == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
    assert load_material_capability_changes() == []


def test_batch06_passes_resolve_only_pass_dates_and_blocked_remains_unresolved_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY not in SPECIAL_SESSION_EVIDENCE
    assert BLOCKED_DAY in raw_days
    assert BLOCKED_DAY not in eligible_days
    assert decisions[BLOCKED_DAY].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
    assert decisions[BLOCKED_DAY].latest_attempt_outcome == "BLOCKED"
    assert decisions[BLOCKED_DAY].contract_verdict == "PASS"


def test_batch06_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 45
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 7
    assert len(eligible) == 38
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 11, 24)
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
    rewrite_batch06_test()
    create_calendar_test()
    create_integration_test()
    print("Prepared atomic Batch 06 integration in worktree: 4 PASS calendar dates + 5 factual attempts; 2023-07-04 remains unresolved BLOCKED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
