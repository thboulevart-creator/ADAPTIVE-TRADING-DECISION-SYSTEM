from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch05 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch05_targets,
)


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch05_adjudication.json"
PROGRESSION_RUNTIME = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
PROGRESSION_TEST = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
BATCH02_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch02.py"
BATCH03_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03_integration.py"
BATCH04_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch04_integration.py"
BATCH05_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2023_batch05.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch05_integration.py"

RUN_ID = 34947146056
JOB_ID = 104309150262
PROBE_COMMIT = "33ae476c48372bce64421a411066db2ddea6125c"
ARTIFACT_ID = 10386998786
ARTIFACT_SHA256 = "ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2023-01-16": {
        "reason_token": "SPECIAL_MARTIN_LUTHER_KING_DAY_2023",
        "record_id": "49338",
        "broker_reason": "Martin Luther King Jr. Day",
        "request_epoch_ms": 1673827200000,
        "start_utc": "2023-01-16T17:59:00Z",
        "final_closed_minute_utc": "2023-01-16T22:59:00Z",
        "reopen_utc": "2023-01-16T23:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2023-02-20": {
        "reason_token": "SPECIAL_PRESIDENTS_DAY_2023",
        "record_id": "50456",
        "broker_reason": "Washington's Birthday",
        "request_epoch_ms": 1676851200000,
        "start_utc": "2023-02-20T17:59:00Z",
        "final_closed_minute_utc": "2023-02-20T22:59:00Z",
        "reopen_utc": "2023-02-20T23:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2023-04-07": {
        "reason_token": "SPECIAL_GOOD_FRIDAY_2023",
        "record_id": "52290",
        "broker_reason": "Easter",
        "request_epoch_ms": 1680825600000,
        "start_utc": "2023-04-07T14:14:00Z",
        "final_closed_minute_utc": "2023-04-09T21:59:00Z",
        "reopen_utc": "2023-04-09T22:00:00Z",
        "closed_hours": (15, 16, 17, 18, 19, 20, 21, 22, 23),
    },
    "2023-05-29": {
        "reason_token": "SPECIAL_MEMORIAL_DAY_2023",
        "record_id": "54373",
        "broker_reason": "Memorial Day",
        "request_epoch_ms": 1685318400000,
        "start_utc": "2023-05-29T16:59:00Z",
        "final_closed_minute_utc": "2023-05-29T21:59:00Z",
        "reopen_utc": "2023-05-29T22:00:00Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
    "2023-06-19": {
        "reason_token": "SPECIAL_JUNETEENTH_OBSERVED_2023",
        "record_id": "55281",
        "broker_reason": "Juneteenth Holiday",
        "request_epoch_ms": 1687132800000,
        "start_utc": "2023-06-19T16:59:00Z",
        "final_closed_minute_utc": "2023-06-19T21:59:00Z",
        "reopen_utc": "2023-06-19T22:00:00Z",
        "closed_hours": (17, 18, 19, 20, 21),
    },
}

EXPECTED_VERDICTS = ["PASS"] * 5
EXPECTED_PRE_ATTEMPTS = 20
EXPECTED_POST_ATTEMPTS = 25
EXPECTED_POST_GLOBAL = (111, 42, 69)
EXPECTED_POST_WINDOW = (68, 19, 49)
EXPECTED_POST_BLOCKED_INELIGIBLE = 6
EXPECTED_POST_ELIGIBLE = 43


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH05_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 5, 0, 0):
        raise RuntimeError("BATCH05_ADJUDICATION_ACCOUNTING_MISMATCH")

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
            raise RuntimeError(f"BATCH05_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH05_ADJUDICATION_CARDINALITY_MISMATCH")

    frozen = [(day.isoformat(), reason) for day, reason in batch05_targets()]
    observed_identity = [
        (item.get("target_date"), item.get("candidate_reason"))
        for item in adjudications
    ]
    if observed_identity != frozen:
        raise RuntimeError("BATCH05_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH05_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS):
        raise RuntimeError("BATCH05_ADJUDICATION_TARGET_SET_MISMATCH")

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
                raise RuntimeError(f"BATCH05_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH05_PASS_DOM_WITNESS_MISSING:{day}")

    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH05_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH05_CALENDAR_INTEGRATION_DETECTED")
    for day in PASS_RECORDS:
        year, month, dom = [int(x) for x in day.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BATCH05_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch05 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch05:")]
    if batch05:
        if len(batch05) == 5:
            raise RuntimeError("BATCH05_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH05_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH05_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 54,
        "attempt_ledger_count": 20,
        "attempted_blocked_ineligible_count": 6,
        "eligible_initial_or_retry_count": 48,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH05_PROGRESSION_STATE_MISMATCH:{key}")


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, record in PASS_RECORDS.items():
        year, month, dom = [int(x) for x in day.split("-")]
        closed_hours = tuple(record["closed_hours"])
        if closed_hours == tuple(range(closed_hours[0], closed_hours[-1] + 1)):
            closed_expr = f"frozenset(range({closed_hours[0]}, {closed_hours[-1] + 1}))"
        else:
            closed_expr = "frozenset({" + ", ".join(str(x) for x in closed_hours) + "})"
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
            "historical_trading_breaks_recovery_batch05_qualification.md"
        ),
    }},
'''
        )
    CALENDAR.write_text(
        replace_once(text, marker, "".join(entries) + marker, "calendar Batch 05 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH05_CAPABILITY_ID_MISMATCH")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch05_targets(), report["adjudications"], strict=True),
        start=21,
    ):
        if adjudication["verdict"] != "PASS":
            raise RuntimeError(f"BATCH05_NON_PASS_ATTEMPT_REFUSED:{target_day.isoformat()}")
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch05:{target_day.isoformat()}",
                "batch_contract": BATCH_CONTRACT,
                "target_date": target_day.isoformat(),
                "candidate_reason": candidate_reason,
                "outcome": "PASS",
                "adjudication_reason": adjudication["reason"],
                "blocking_reason": None,
                "capability_id": CAPABILITY_ID,
                "provenance": dict(provenance),
            }
        )
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def update_protocol_test() -> None:
    text = PROTOCOL_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "test_queue_scope_sorted_and_has_54_unresolved_candidates_after_batch04",
        "test_queue_scope_sorted_and_has_49_unresolved_candidates_after_batch05",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 54", "assert len(queue) == 49", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        (
            "test_attempt_ledger_preserves_all_twenty_historical_attempts_and_duplicate_history",
            "test_attempt_ledger_preserves_all_twenty_five_historical_attempts_and_duplicate_history",
            "progression ledger test name",
        ),
        ("assert len(attempts) == 20", "assert len(attempts) == 25", "progression attempt count"),
        ("list(range(1, 21))", "list(range(1, 26))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 20", "len({item.attempt_id for item in attempts}) == 25", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 54", "assert len(decisions) == len(queue) == 49", "progression unresolved count"),
        (
            "assert eligible[0][0] > date(2023, 1, 2)",
            "assert eligible[0][0] > date(2023, 6, 19)",
            "progression non-starving first eligible",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    anchor = "    assert all(day not in eligible_days for day, _ in ((date(2022, 11, 24), 'THANKSGIVING_DAY'), (date(2022, 11, 25), 'THANKSGIVING_FRIDAY'), (date(2022, 12, 23), 'CHRISTMAS_PRE_HOLIDAY_SESSION')))\n"
    replacement = anchor + "    assert all(day not in eligible_days for day, _ in ((date(2023, 1, 16), 'MARTIN_LUTHER_KING_DAY'), (date(2023, 2, 20), 'PRESIDENTS_DAY'), (date(2023, 4, 7), 'GOOD_FRIDAY'), (date(2023, 5, 29), 'MEMORIAL_DAY'), (date(2023, 6, 19), 'JUNETEENTH_OBSERVED')))\n"
    text = replace_once(text, anchor, replacement, "progression Batch05 pass exclusion")
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_batch02_test() -> None:
    text = BATCH02_TEST.read_text(encoding="utf-8")
    BATCH02_TEST.write_text(
        replace_once(text, "assert len(queue) == 54", "assert len(queue) == 49", "Batch02 current queue count"),
        encoding="utf-8",
    )


def update_batch03_integration_test() -> None:
    text = BATCH03_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("post_batch04_state", "post_batch05_state", "Batch03 integration state name"),
        ("post_batch04", "post_batch05", "Batch03 integration history name"),
        ('assert global_report["resolved_candidate_dates"] == 37', 'assert global_report["resolved_candidate_dates"] == 42', "Batch03 global resolved"),
        ('assert global_report["unresolved_candidate_dates"] == 74', 'assert global_report["unresolved_candidate_dates"] == 69', "Batch03 global unresolved"),
        ('assert window_report["resolved_candidate_dates"] == 14', 'assert window_report["resolved_candidate_dates"] == 19', "Batch03 window resolved"),
        ('assert window_report["unresolved_candidate_dates"] == 54', 'assert window_report["unresolved_candidate_dates"] == 49', "Batch03 window unresolved"),
        ("assert len(attempts) == 20", "assert len(attempts) == 25", "Batch03 ledger total"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH03_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def update_batch04_integration_test() -> None:
    text = BATCH04_INTEGRATION_TEST.read_text(encoding="utf-8")
    replacements = [
        ("(111, 37, 74)", "(111, 42, 69)", "Batch04 global accounting"),
        ("(68, 14, 54)", "(68, 19, 49)", "Batch04 window accounting"),
        ("assert len(attempts) == 20", "assert len(attempts) == 25", "Batch04 ledger total"),
        ("assert len(recovery_queue()) == len(decisions) == 54", "assert len(recovery_queue()) == len(decisions) == 49", "Batch04 progression queue"),
        ("assert len(eligible) == 48", "assert len(eligible) == 43", "Batch04 progression eligible"),
        ("assert eligible[0][0] > date(2023, 1, 2)", "assert eligible[0][0] > date(2023, 6, 19)", "Batch04 first eligible"),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    BATCH04_INTEGRATION_TEST.write_text(text, encoding="utf-8")


def rewrite_batch05_test() -> None:
    BATCH05_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch05 as batch05_module
from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.trading_breaks_recovery_batch05 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH05_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch05_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH05 = [
    (date(2023, 1, 16), "MARTIN_LUTHER_KING_DAY"),
    (date(2023, 2, 20), "PRESIDENTS_DAY"),
    (date(2023, 4, 7), "GOOD_FRIDAY"),
    (date(2023, 5, 29), "MEMORIAL_DAY"),
    (date(2023, 6, 19), "JUNETEENTH_OBSERVED"),
]
PASS_DAYS = {day for day, _ in EXPECTED_BATCH05}
ATTEMPTED_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),
}


def test_batch05_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH05_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH05_TARGETS, tuple)
    assert batch05_targets() == EXPECTED_BATCH05


def test_batch05_historical_membership_is_immutable_and_not_rederived_post_integration():
    first = batch05_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch05_targets() == EXPECTED_BATCH05
    assert PASS_DAYS.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_post_integration_calendar_contains_all_five_batch05_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)


def test_post_integration_attempt_ledger_records_exactly_five_batch05_pass_attempts():
    _, _, attempts = load_attempt_ledger()
    batch05 = [item for item in attempts if item.attempt_id.startswith("batch05:")]
    assert len(attempts) == 25
    assert [item.attempt_sequence for item in batch05] == [21, 22, 23, 24, 25]
    assert [item.target_date for item in batch05] == [day for day, _ in EXPECTED_BATCH05]
    assert [item.outcome for item in batch05] == ["PASS"] * 5
    assert all(item.blocking_reason is None for item in batch05)
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch05)


def test_all_six_historical_blocked_dates_remain_unresolved_but_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {item.target_date: item for item in progression_decisions()}
    assert ATTEMPTED_BLOCKED <= raw_days
    assert ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    for day in ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_batch05_postintegration_progression_state_is_exact():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    _, _, attempts = load_attempt_ledger()
    assert len(recovery_queue()) == len(decisions) == 49
    assert len(attempts) == 25
    assert load_material_capability_changes() == []
    assert sum(not item.eligible and item.latest_attempt_outcome == "BLOCKED" for item in decisions) == 6
    assert len(eligible) == 43
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 6, 19)


def test_batch05_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "601310a55b64233ada9e481d3cb2f11dc20a30d5"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "6cafa5337f28c5424cbcc25280c690de702061d9"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"


def test_batch05_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch05_targets).parameters == {}
    source = inspect.getsource(batch05_module).lower()
    for forbidden in ("playwright", "chromium", "probe_candidate", "asyncio", "expected_outcome", "priority", "manual_skip"):
        assert forbidden not in source
''', encoding="utf-8")


def create_calendar_test() -> None:
    CALENDAR_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import (
    EXPECTED_CLOSED,
    EXPECTED_OPEN,
    SPECIAL_SESSION_EVIDENCE,
    classify_slot,
)


EXPECTED = {
    date(2023, 1, 16): ("SPECIAL_MARTIN_LUTHER_KING_DAY_2023", "49338", frozenset(range(18, 23))),
    date(2023, 2, 20): ("SPECIAL_PRESIDENTS_DAY_2023", "50456", frozenset(range(18, 23))),
    date(2023, 4, 7): ("SPECIAL_GOOD_FRIDAY_2023", "52290", frozenset(range(15, 24))),
    date(2023, 5, 29): ("SPECIAL_MEMORIAL_DAY_2023", "54373", frozenset(range(17, 22))),
    date(2023, 6, 19): ("SPECIAL_JUNETEENTH_OBSERVED_2023", "55281", frozenset(range(17, 22))),
}


def test_batch05_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10386998786
        assert record["artifact_sha256"] == "ad96e1850ca53910c092abd444f02a04e2a84ea192fa6c0b5189a7e349ea800c"
        assert record["probe_commit"] == "33ae476c48372bce64421a411066db2ddea6125c"
        assert record["fully_closed_hours_utc"] == closed_hours
        for hour in closed_hours:
            assert classify_slot(day, hour).status == EXPECTED_CLOSED


def test_batch05_partial_start_hours_are_not_rounded_closed():
    assert classify_slot(date(2023, 1, 16), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 2, 20), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 4, 7), 14).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 5, 29), 16).status == EXPECTED_OPEN
    assert classify_slot(date(2023, 6, 19), 16).status == EXPECTED_OPEN


def test_good_friday_weekend_span_projects_only_target_day_whole_hours():
    assert SPECIAL_SESSION_EVIDENCE[date(2023, 4, 7)]["fully_closed_hours_utc"] == frozenset(range(15, 24))
''', encoding="utf-8")


def create_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


PASS_DAYS = {
    date(2023, 1, 16), date(2023, 2, 20), date(2023, 4, 7),
    date(2023, 5, 29), date(2023, 6, 19),
}
BLOCKED_DAYS = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),
}


def test_batch05_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 42, 69)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 19, 49)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch05_atomic_integration_records_exactly_five_factual_pass_attempts():
    _, _, attempts = load_attempt_ledger()
    batch05 = [item for item in attempts if item.attempt_id.startswith("batch05:")]
    assert len(attempts) == 25
    assert [item.attempt_sequence for item in batch05] == [21, 22, 23, 24, 25]
    assert [item.outcome for item in batch05] == ["PASS"] * 5
    assert all(item.blocking_reason is None for item in batch05)
    assert load_material_capability_changes() == []


def test_batch05_passes_leave_unresolved_queue_without_disturbing_blocked_semantics():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert BLOCKED_DAYS <= raw_days
    assert BLOCKED_DAYS.isdisjoint(eligible_days)
    for day in BLOCKED_DAYS:
        assert decisions[day].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decisions[day].latest_attempt_outcome == "BLOCKED"
        assert decisions[day].contract_verdict == "PASS"


def test_batch05_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 49
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 6
    assert len(eligible) == 43
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 6, 19)
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
    rewrite_batch05_test()
    create_calendar_test()
    create_integration_test()
    print(
        "Prepared atomic Batch 05 integration in worktree: 5 PASS calendar dates + "
        "5 factual PASS attempts; historical BLOCKED dates remain unresolved."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
