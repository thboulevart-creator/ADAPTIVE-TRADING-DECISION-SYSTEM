from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch04 import (
    BATCH_CONTRACT,
    CURRENT_CAPABILITY_ID,
    batch04_targets,
)


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch04_adjudication.json"
PROGRESSION_RUNTIME = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
PROGRESSION_TEST = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
BATCH02_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch02.py"
BATCH03_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03.py"
BATCH03_INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03_integration.py"
BATCH04_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch04.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2022_batch04.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch04_integration.py"

RUN_ID = 34895457466
JOB_ID = 104148201341
PROBE_COMMIT = "11a81294720898802e49dd1131a64e20e7e7ae3a"
ARTIFACT_ID = 10369230708
ARTIFACT_SHA256 = "3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2022-11-24": {
        "reason_token": "SPECIAL_THANKSGIVING_DAY_2022",
        "record_id": "45119",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1669248000000,
        "start_utc": "2022-11-24T17:59:00Z",
        "final_closed_minute_utc": "2022-11-24T22:59:00Z",
        "reopen_utc": "2022-11-24T23:00:00Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2022-11-25": {
        "reason_token": "SPECIAL_THANKSGIVING_FRIDAY_2022",
        "record_id": "45120",
        "broker_reason": "Thanksgiving Day",
        "request_epoch_ms": 1669334400000,
        "start_utc": "2022-11-25T18:14:00Z",
        "final_closed_minute_utc": "2022-11-27T22:59:00Z",
        "reopen_utc": "2022-11-27T23:00:00Z",
        "closed_hours": (19, 20, 21, 22, 23),
    },
    "2022-12-23": {
        "reason_token": "SPECIAL_CHRISTMAS_PRE_HOLIDAY_2022",
        "record_id": "46756",
        "broker_reason": "Christmas Day",
        "request_epoch_ms": 1671753600000,
        "start_utc": "2022-12-23T21:14:00Z",
        "final_closed_minute_utc": "2022-12-26T22:59:00Z",
        "reopen_utc": "2022-12-26T23:00:00Z",
        "closed_hours": (22, 23),
    },
}

BLOCKED_DATES = {
    "2022-12-26": "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
    "2023-01-02": "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
}

EXPECTED_VERDICTS = ["PASS", "PASS", "PASS", "BLOCKED", "BLOCKED"]
EXPECTED_PRE_ATTEMPTS = 15
EXPECTED_POST_ATTEMPTS = 20
EXPECTED_POST_GLOBAL = (111, 37, 74)
EXPECTED_POST_WINDOW = (68, 14, 54)
EXPECTED_POST_BLOCKED_INELIGIBLE = 6
EXPECTED_POST_ELIGIBLE = 48


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH04_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 3, 2, 0):
        raise RuntimeError("BATCH04_ADJUDICATION_ACCOUNTING_MISMATCH")

    provenance = report.get("provenance") or {}
    expected_provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "probe_commit": PROBE_COMMIT,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
    }
    for key, value in expected_provenance.items():
        if provenance.get(key) != value:
            raise RuntimeError(f"BATCH04_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH04_ADJUDICATION_CARDINALITY_MISMATCH")

    frozen = [(day.isoformat(), reason) for day, reason in batch04_targets()]
    observed_identity = [
        (item.get("target_date"), item.get("candidate_reason"))
        for item in adjudications
    ]
    if observed_identity != frozen:
        raise RuntimeError("BATCH04_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [item.get("verdict") for item in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH04_ADJUDICATION_VERDICT_ORDER_MISMATCH")

    by_day = {item["target_date"]: item for item in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_DATES):
        raise RuntimeError("BATCH04_ADJUDICATION_TARGET_SET_MISMATCH")

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
        }
        for key, value in checks.items():
            if item.get(key) != value:
                raise RuntimeError(f"BATCH04_PASS_RECORD_MISMATCH:{day}:{key}")
        if item.get("dom_witness_present") is not True:
            raise RuntimeError(f"BATCH04_PASS_DOM_WITNESS_MISSING:{day}")

    for day, blocking_reason in BLOCKED_DATES.items():
        item = by_day[day]
        if item.get("verdict") != "BLOCKED" or item.get("reason") != blocking_reason:
            raise RuntimeError(f"BATCH04_BLOCKED_REASON_MISMATCH:{day}")
        overlap_start = item.get("overlap_start_utc")
        if not isinstance(overlap_start, str) or overlap_start.startswith(day):
            raise RuntimeError(f"BATCH04_BLOCKED_CROSS_DATE_WITNESS_MISMATCH:{day}")

    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [item["reason_token"] for item in PASS_RECORDS.values()]
    present = [token in calendar_text for token in reason_tokens]
    if any(present):
        if all(present):
            raise RuntimeError("BATCH04_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH04_CALENDAR_INTEGRATION_DETECTED")
    for blocked in BLOCKED_DATES:
        year, month, dom = [int(x) for x in blocked.split("-")]
        if f"date({year}, {month}, {dom}):" in calendar_text:
            raise RuntimeError(f"BLOCKED_DATE_ALREADY_PROMOTED:{blocked}")

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")
    batch04 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch04:")]
    if batch04:
        if len(batch04) == 5:
            raise RuntimeError("BATCH04_ATTEMPTS_ALREADY_INTEGRATED")
        raise RuntimeError("PARTIAL_BATCH04_ATTEMPT_LEDGER_DETECTED")
    if len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError(f"PRE_BATCH04_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")

    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected_progression = {
        "verdict": "PASS",
        "calendar_unresolved_count": 57,
        "attempt_ledger_count": 15,
        "attempted_blocked_ineligible_count": 4,
        "eligible_initial_or_retry_count": 53,
    }
    for key, value in expected_progression.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH04_PROGRESSION_STATE_MISMATCH:{key}")


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
            "historical_trading_breaks_recovery_batch04_qualification.md"
        ),
    }},
'''
        )
    CALENDAR.write_text(
        replace_once(text, marker, "".join(entries) + marker, "calendar Batch 04 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH04_CAPABILITY_ID_MISMATCH")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch04_targets(), report["adjudications"], strict=True),
        start=16,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        attempts.append(
            {
                "attempt_sequence": sequence,
                "attempt_id": f"batch04:{target_day.isoformat()}",
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
        "test_queue_scope_sorted_and_has_57_unresolved_candidates_after_batch03",
        "test_queue_scope_sorted_and_has_54_unresolved_candidates_after_batch04",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 57", "assert len(queue) == 54", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        (
            "test_attempt_ledger_preserves_all_fifteen_historical_attempts_and_duplicate_history",
            "test_attempt_ledger_preserves_all_twenty_historical_attempts_and_duplicate_history",
            "progression ledger test name",
        ),
        ("assert len(attempts) == 15", "assert len(attempts) == 20", "progression attempt count"),
        ("list(range(1, 16))", "list(range(1, 21))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 15", "len({item.attempt_id for item in attempts}) == 20", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 57", "assert len(decisions) == len(queue) == 54", "progression unresolved count"),
        (
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1)):",
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2)):",
            "progression blocked replay set",
        ),
        (
            'assert eligible[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")',
            "assert eligible[0][0] > date(2023, 1, 2)",
            "progression non-starving first eligible",
        ),
        (
            "    assert date(2022, 11, 24) in eligible_days\n",
            "    assert date(2022, 12, 26) not in eligible_days\n    assert date(2023, 1, 2) not in eligible_days\n    assert all(day not in eligible_days for day, _ in ((date(2022, 11, 24), 'THANKSGIVING_DAY'), (date(2022, 11, 25), 'THANKSGIVING_FRIDAY'), (date(2022, 12, 23), 'CHRISTMAS_PRE_HOLIDAY_SESSION')))\n",
            "progression Batch04 eligible assertions",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    blocked_anchor = "    assert date(2022, 7, 1) in queue_days\n"
    text = replace_once(
        text,
        blocked_anchor,
        blocked_anchor + "    assert date(2022, 12, 26) in queue_days\n    assert date(2023, 1, 2) in queue_days\n",
        "progression blocked calendar set",
    )
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def update_batch02_test() -> None:
    text = BATCH02_TEST.read_text(encoding="utf-8")
    BATCH02_TEST.write_text(
        replace_once(text, "assert len(queue) == 57", "assert len(queue) == 54", "Batch02 current queue count"),
        encoding="utf-8",
    )


def update_batch03_test() -> None:
    text = BATCH03_TEST.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '    assert eligible_recovery_queue()[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")\n',
        "",
        "Batch03 stale next-eligible assertion",
    )
    BATCH03_TEST.write_text(text, encoding="utf-8")


def rewrite_batch03_integration_test() -> None:
    BATCH03_INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch03_integrated_evidence_remains_valid_in_post_batch04_state():
    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert global_report["candidate_dates"] == 111
    assert global_report["resolved_candidate_dates"] == 37
    assert global_report["unresolved_candidate_dates"] == 74
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []
    assert window_report["candidate_dates"] == 68
    assert window_report["resolved_candidate_dates"] == 14
    assert window_report["unresolved_candidate_dates"] == 54


def test_batch03_attempt_history_remains_preserved_post_batch04():
    _, _, attempts = load_attempt_ledger()
    batch03 = [item for item in attempts if item.attempt_id.startswith("batch03:")]
    assert len(attempts) == 20
    assert [item.attempt_sequence for item in batch03] == [11, 12, 13, 14, 15]
    assert [item.outcome for item in batch03] == ["PASS", "PASS", "BLOCKED", "PASS", "PASS"]
    assert load_material_capability_changes() == []


def test_batch03_blocked_date_remains_unresolved_but_not_retryable_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert date(2022, 7, 1) in raw_days
    assert date(2022, 7, 1) not in eligible_days
    assert decisions[date(2022, 7, 1)].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
''', encoding="utf-8")


def rewrite_batch04_test() -> None:
    BATCH04_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch04 as batch04_module
from tools.trading_breaks_recovery_batch04 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH04_TARGETS,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch04_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH04 = [
    (date(2022, 11, 24), "THANKSGIVING_DAY"),
    (date(2022, 11, 25), "THANKSGIVING_FRIDAY"),
    (date(2022, 12, 23), "CHRISTMAS_PRE_HOLIDAY_SESSION"),
    (date(2022, 12, 26), "CHRISTMAS_OBSERVED"),
    (date(2023, 1, 2), "NEW_YEARS_OBSERVED"),
]
PASS_DAYS = {date(2022, 11, 24), date(2022, 11, 25), date(2022, 12, 23)}
BLOCKED_DAYS = {date(2022, 12, 26), date(2023, 1, 2)}
ALL_ATTEMPTED_BLOCKED = {
    date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15),
    date(2022, 7, 1), date(2022, 12, 26), date(2023, 1, 2),
}


def test_batch04_contract_size_and_historical_membership_remain_frozen():
    assert BATCH_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_POLICY_V1"
    assert PARENT_PROGRESSION_CONTRACT == "HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1"
    assert BATCH_SIZE == 5
    assert isinstance(FROZEN_BATCH04_TARGETS, tuple)
    assert batch04_targets() == EXPECTED_BATCH04


def test_batch04_historical_membership_is_immutable_and_not_rederived_post_integration():
    first = batch04_targets()
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch04_targets() == EXPECTED_BATCH04
    assert {day for day, _ in EXPECTED_BATCH04}.isdisjoint({day for day, _ in eligible_recovery_queue()})


def test_post_integration_calendar_contains_only_batch04_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAYS <= raw_days


def test_post_integration_attempt_ledger_records_all_five_batch04_attempts():
    _, _, attempts = load_attempt_ledger()
    batch04 = [item for item in attempts if item.attempt_id.startswith("batch04:")]
    assert [item.attempt_sequence for item in batch04] == [16, 17, 18, 19, 20]
    assert [item.target_date for item in batch04] == [day for day, _ in EXPECTED_BATCH04]
    assert [item.outcome for item in batch04] == ["PASS", "PASS", "PASS", "BLOCKED", "BLOCKED"]
    assert [item.blocking_reason for item in batch04[-2:]] == [
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
        "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
    ]
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch04)


def test_all_six_attempted_blocked_dates_remain_unresolved_but_ineligible_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert ALL_ATTEMPTED_BLOCKED <= raw_days
    assert ALL_ATTEMPTED_BLOCKED.isdisjoint(eligible_days)
    for day in ALL_ATTEMPTED_BLOCKED:
        decision = decisions[day]
        assert decision.eligible is False
        assert decision.latest_attempt_outcome == "BLOCKED"
        assert decision.reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decision.contract_verdict == "PASS"


def test_freeze_provenance_remains_historical_truth_after_integration():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "4d3c5db74ec31215b74799f27cdfe476d513014b"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "d85d6102f8b9d9204521dacfbdcc3a0212f8de5e"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    assert load_material_capability_changes() == []


def test_batch04_accessor_and_freeze_module_expose_no_manual_or_browser_surface():
    assert inspect.signature(batch04_targets).parameters == {}
    source = inspect.getsource(batch04_module).lower()
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
    date(2022, 11, 24): ("SPECIAL_THANKSGIVING_DAY_2022", "45119", frozenset(range(18, 23))),
    date(2022, 11, 25): ("SPECIAL_THANKSGIVING_FRIDAY_2022", "45120", frozenset(range(19, 24))),
    date(2022, 12, 23): ("SPECIAL_CHRISTMAS_PRE_HOLIDAY_2022", "46756", frozenset({22, 23})),
}


def test_batch04_pass_dates_encode_exact_adjudicated_broker_records():
    for day, (reason, record_id, closed_hours) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["artifact_id"] == 10369230708
        assert record["artifact_sha256"] == "3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc"
        assert record["probe_commit"] == "11a81294720898802e49dd1131a64e20e7e7ae3a"
        assert record["fully_closed_hours_utc"] == closed_hours
        for hour in closed_hours:
            assert classify_slot(day, hour).status == EXPECTED_CLOSED


def test_batch04_partial_start_hours_are_not_rounded_closed():
    assert classify_slot(date(2022, 11, 24), 17).status == EXPECTED_OPEN
    assert classify_slot(date(2022, 11, 25), 18).status == EXPECTED_OPEN
    assert classify_slot(date(2022, 12, 23), 21).status == EXPECTED_OPEN


def test_batch04_cross_date_blocked_dates_are_not_promoted_to_special_evidence():
    assert date(2022, 12, 26) not in SPECIAL_SESSION_EVIDENCE
    assert date(2023, 1, 2) not in SPECIAL_SESSION_EVIDENCE
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


PASS_DAYS = {date(2022, 11, 24), date(2022, 11, 25), date(2022, 12, 23)}
BLOCKED_DAYS = {date(2022, 12, 26), date(2023, 1, 2)}


def test_batch04_atomic_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert (global_report["candidate_dates"], global_report["resolved_candidate_dates"], global_report["unresolved_candidate_dates"]) == (111, 37, 74)
    assert (window["candidate_dates"], window["resolved_candidate_dates"], window["unresolved_candidate_dates"]) == (68, 14, 54)
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []


def test_batch04_atomic_integration_records_exactly_five_factual_attempts():
    _, _, attempts = load_attempt_ledger()
    batch04 = [item for item in attempts if item.attempt_id.startswith("batch04:")]
    assert len(attempts) == 20
    assert [item.attempt_sequence for item in batch04] == [16, 17, 18, 19, 20]
    assert [item.outcome for item in batch04] == ["PASS", "PASS", "PASS", "BLOCKED", "BLOCKED"]
    assert load_material_capability_changes() == []


def test_batch04_passes_leave_unresolved_queue_and_blocked_remain_unresolved_but_ineligible():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    decisions = {d.target_date: d for d in progression_decisions()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert PASS_DAYS <= set(SPECIAL_SESSION_EVIDENCE)
    assert BLOCKED_DAYS <= raw_days
    assert BLOCKED_DAYS.isdisjoint(eligible_days)
    assert BLOCKED_DAYS.isdisjoint(set(SPECIAL_SESSION_EVIDENCE))
    for day in BLOCKED_DAYS:
        assert decisions[day].reason == "SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED"
        assert decisions[day].latest_attempt_outcome == "BLOCKED"
        assert decisions[day].contract_verdict == "PASS"


def test_batch04_progression_is_non_starving_after_integration():
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(recovery_queue()) == len(decisions) == 54
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 6
    assert len(eligible) == 48
    assert eligible == sorted(eligible, key=lambda item: item[0])
    assert eligible[0][0] > date(2023, 1, 2)
''', encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_attempt_ledger(report)
    update_protocol_test()
    update_progression_test()
    update_batch02_test()
    update_batch03_test()
    rewrite_batch03_integration_test()
    rewrite_batch04_test()
    create_calendar_test()
    create_integration_test()
    print(
        "Prepared atomic Batch 04 integration in worktree: 3 PASS calendar dates + "
        "5 factual attempts; 2022-12-26 and 2023-01-02 remain unresolved/BLOCKED."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
