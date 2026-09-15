from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch10 import BATCH_CONTRACT, CURRENT_CAPABILITY_ID, batch10_targets

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch10_adjudication.json"
PROGRESSION_RUNTIME = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_progression_runtime.json"

RUN_ID = 35004172846
JOB_ID = 104499660140
PROBE_COMMIT = "443b3696e4e2740a54354787de231c886f90b26e"
ARTIFACT_ID = 10411022092
ARTIFACT_SHA256 = "1572cc5a1c38998f59d32e107b1bcb006a74b288fe32c70ffe019726b3ad5f14"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2024-12-31": {
        "reason_token": "SPECIAL_NEW_YEARS_EVE_CANDIDATE_2024",
        "record_id": "75799",
        "broker_reason": "New Year's Day",
        "request_epoch_ms": 1735603200000,
        "start_utc": "2024-12-31T21:14:59Z",
        "final_closed_minute_utc": "2025-01-01T22:59:59Z",
        "reopen_utc": "2025-01-01T23:00:59Z",
        "closed_hours": (22, 23),
    },
    "2025-01-20": {
        "reason_token": "SPECIAL_MARTIN_LUTHER_KING_DAY_2025",
        "record_id": "76806",
        "broker_reason": "Martin Luther King Jr. Day",
        "request_epoch_ms": 1737331200000,
        "start_utc": "2025-01-20T17:59:59Z",
        "final_closed_minute_utc": "2025-01-20T22:59:59Z",
        "reopen_utc": "2025-01-20T23:00:59Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
    "2025-02-17": {
        "reason_token": "SPECIAL_PRESIDENTS_DAY_2025",
        "record_id": "78513",
        "broker_reason": "Presidents's Day",
        "request_epoch_ms": 1739750400000,
        "start_utc": "2025-02-17T17:59:59Z",
        "final_closed_minute_utc": "2025-02-17T22:59:59Z",
        "reopen_utc": "2025-02-17T23:00:59Z",
        "closed_hours": (18, 19, 20, 21, 22),
    },
}
BLOCKED_TARGETS = {
    "2025-01-01": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "75799"),
    "2025-04-18": ("NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE", "80057"),
}
EXPECTED_VERDICTS = ["PASS", "BLOCKED", "PASS", "PASS", "BLOCKED"]
EXPECTED_PRE_ATTEMPTS = 45
EXPECTED_POST_ATTEMPTS = 50
EXPECTED_POST_GLOBAL = (111, 60, 51)
EXPECTED_POST_WINDOW = (68, 37, 31)
EXPECTED_POST_BLOCKED_INELIGIBLE = 13
EXPECTED_POST_ELIGIBLE = 18


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("schema") != "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH10_ADJUDICATION_V1":
        raise RuntimeError("BATCH10_ADJUDICATION_SCHEMA_MISMATCH")
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH10_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 3, 2, 0):
        raise RuntimeError("BATCH10_ADJUDICATION_ACCOUNTING_MISMATCH")
    provenance = report.get("provenance") or {}
    expected = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "probe_commit": PROBE_COMMIT,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
    }
    for key, value in expected.items():
        if provenance.get(key) != value:
            raise RuntimeError(f"BATCH10_ADJUDICATION_PROVENANCE_MISMATCH:{key}")
    adjudications = report.get("adjudications")
    if not isinstance(adjudications, list) or len(adjudications) != 5:
        raise RuntimeError("BATCH10_ADJUDICATION_CARDINALITY_MISMATCH")
    frozen = [(day.isoformat(), reason) for day, reason in batch10_targets()]
    observed = [(x.get("target_date"), x.get("candidate_reason")) for x in adjudications]
    if observed != frozen:
        raise RuntimeError("BATCH10_ADJUDICATION_FROZEN_IDENTITY_MISMATCH")
    if [x.get("verdict") for x in adjudications] != EXPECTED_VERDICTS:
        raise RuntimeError("BATCH10_ADJUDICATION_VERDICT_ORDER_MISMATCH")
    by_day = {x["target_date"]: x for x in adjudications}
    if set(by_day) != set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        raise RuntimeError("BATCH10_ADJUDICATION_TARGET_SET_MISMATCH")
    for day, expected_record in PASS_RECORDS.items():
        item = by_day[day]
        checks = {
            "reason": "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED",
            "broker_record_id": expected_record["record_id"],
            "broker_reason": expected_record["broker_reason"],
            "break_start_utc": expected_record["start_utc"],
            "final_closed_minute_utc": expected_record["final_closed_minute_utc"],
            "reopen_utc": expected_record["reopen_utc"],
            "fully_closed_hours_utc": list(expected_record["closed_hours"]),
            "workflow_run": RUN_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_sha256": ARTIFACT_SHA256,
            "probe_commit": PROBE_COMMIT,
            "dom_witness_present": True,
        }
        for key, value in checks.items():
            if item.get(key) != value:
                raise RuntimeError(f"BATCH10_PASS_RECORD_MISMATCH:{day}:{key}")
    for day, (reason, overlap_id) in BLOCKED_TARGETS.items():
        item = by_day[day]
        if item.get("verdict") != "BLOCKED" or item.get("reason") != reason:
            raise RuntimeError(f"BATCH10_BLOCKED_VERDICT_MISMATCH:{day}")
        if item.get("overlap_record_id") != overlap_id:
            raise RuntimeError(f"BATCH10_BLOCKED_OVERLAP_MISMATCH:{day}")
        if "break_start_utc" in item or "fully_closed_hours_utc" in item:
            raise RuntimeError(f"BATCH10_BLOCKED_TARGET_WAS_PROMOTED:{day}")
    return report


def guard_preintegration_state() -> None:
    calendar_text = CALENDAR.read_text(encoding="utf-8")
    for token in [x["reason_token"] for x in PASS_RECORDS.values()]:
        if token in calendar_text:
            raise RuntimeError("BATCH10_ALREADY_OR_PARTIALLY_INTEGRATED")
    for day in set(PASS_RECORDS) | set(BLOCKED_TARGETS):
        y, m, d = map(int, day.split("-"))
        if f"date({y}, {m}, {d}):" in calendar_text:
            raise RuntimeError(f"BATCH10_TARGET_ALREADY_PRESENT_IN_CALENDAR:{day}")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("PRE_BATCH10_ATTEMPT_COUNT_MISMATCH")
    if any(str(x.get("attempt_id", "")).startswith("batch10:") for x in attempts):
        raise RuntimeError("BATCH10_ATTEMPTS_ALREADY_OR_PARTIALLY_INTEGRATED")
    if [x.get("attempt_sequence") for x in attempts[-5:]] != [41, 42, 43, 44, 45]:
        raise RuntimeError("PRE_BATCH10_LEDGER_TAIL_MISMATCH")
    progression = json.loads(PROGRESSION_RUNTIME.read_text(encoding="utf-8"))
    expected = {
        "verdict": "PASS",
        "calendar_unresolved_count": 34,
        "attempt_ledger_count": 45,
        "attempted_blocked_ineligible_count": 11,
        "eligible_initial_or_retry_count": 23,
    }
    for key, value in expected.items():
        if progression.get(key) != value:
            raise RuntimeError(f"PRE_BATCH10_PROGRESSION_STATE_MISMATCH:{key}")


def _render_calendar_entry(day: str, record: dict) -> str:
    y, m, d = map(int, day.split("-"))
    hours = tuple(record["closed_hours"])
    if hours != tuple(range(hours[0], hours[-1] + 1)):
        raise RuntimeError(f"BATCH10_NONCONTIGUOUS_CLOSED_HOURS:{day}")
    return f'''    date({y}, {m}, {d}): {{
        "reason": "{record['reason_token']}",
        # Exact broker-native Trading Breaks record {record['record_id']}.
        # Start {record['start_utc']}; final closed instant {record['final_closed_minute_utc']};
        # protocol-derived reopen {record['reopen_utc']}. Only whole target-day UTC
        # buckets proven closed by the independently adjudicated interval are encoded here.
        "fully_closed_hours_utc": frozenset(range({hours[0]}, {hours[-1] + 1})),
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
            "historical_trading_breaks_recovery_batch10_qualification.md"
        ),
    }},
'''


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    dec31 = _render_calendar_entry("2024-12-31", PASS_RECORDS["2024-12-31"])
    marker = "    date(2025, 1, 9): {\n"
    text = replace_once(text, marker, dec31 + marker, "Batch10 Dec31 insertion")
    later = _render_calendar_entry("2025-01-20", PASS_RECORDS["2025-01-20"]) + _render_calendar_entry("2025-02-17", PASS_RECORDS["2025-02-17"])
    end_marker = "}\n\nCALENDAR_CONTRACT = \"DUKASCOPY_USATECH_SESSION_CALENDAR_V3\""
    text = replace_once(text, end_marker, later + end_marker, "Batch10 2025 insertion")
    if "date(2025, 1, 1):" in text or "date(2025, 4, 18):" in text:
        raise RuntimeError("BATCH10_BLOCKED_TARGET_CALENDAR_PROMOTION_ATTEMPT")
    CALENDAR.write_text(text, encoding="utf-8")


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list) or len(attempts) != EXPECTED_PRE_ATTEMPTS:
        raise RuntimeError("ATTEMPT_LEDGER_PRECONDITION_CHANGED")
    if ledger.get("current_capability_id") != CURRENT_CAPABILITY_ID or CURRENT_CAPABILITY_ID != CAPABILITY_ID:
        raise RuntimeError("BATCH10_CAPABILITY_ID_MISMATCH")
    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    for sequence, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch10_targets(), report["adjudications"], strict=True), start=46
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        if outcome not in {"PASS", "BLOCKED"}:
            raise RuntimeError(f"BATCH10_UNINTEGRABLE_OUTCOME:{target_day}:{outcome}")
        attempts.append({
            "attempt_sequence": sequence,
            "attempt_id": f"batch10:{target_day.isoformat()}",
            "batch_contract": BATCH_CONTRACT,
            "target_date": target_day.isoformat(),
            "candidate_reason": candidate_reason,
            "outcome": outcome,
            "adjudication_reason": reason,
            "blocking_reason": reason if outcome == "BLOCKED" else None,
            "capability_id": CAPABILITY_ID,
            "provenance": dict(provenance),
        })
    if len(attempts) != EXPECTED_POST_ATTEMPTS:
        raise RuntimeError("BATCH10_POST_LEDGER_COUNT_MISMATCH")
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")


def rewrite_current_state_tests() -> None:
    replacements = {
        "assert len(attempts) == 45": "assert len(attempts) == 50",
        "list(range(1, 46))": "list(range(1, 51))",
        "len({item.attempt_id for item in attempts}) == 45": "len({item.attempt_id for item in attempts}) == 50",
        "assert len(queue) == 34": "assert len(queue) == 31",
        "assert len(decisions) == len(queue) == 34": "assert len(decisions) == len(queue) == 31",
        "assert len(recovery_queue()) == len(decisions) == 34": "assert len(recovery_queue()) == len(decisions) == 31",
        "assert len(eligible) == 23": "assert len(eligible) == 18",
        "(111, 57, 54)": "(111, 60, 51)",
        "(68, 34, 34)": "(68, 37, 31)",
        'global_report["resolved_candidate_dates"] == 57': 'global_report["resolved_candidate_dates"] == 60',
        'global_report["unresolved_candidate_dates"] == 54': 'global_report["unresolved_candidate_dates"] == 51',
        'window_report["resolved_candidate_dates"] == 34': 'window_report["resolved_candidate_dates"] == 37',
        'window_report["unresolved_candidate_dates"] == 34': 'window_report["unresolved_candidate_dates"] == 31',
        'eligible[0] == (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE")': 'eligible[0] == (date(2025, 5, 26), "MEMORIAL_DAY")',
        "post_batch09_state": "post_batch10_state",
        "post_batch09_progression_state": "post_batch10_progression_state",
    }
    for path in sorted((REPO / "tests").glob("test_*.py")):
        if path.name in {
            "test_trading_breaks_recovery_batch10_adjudication.py",
            "test_trading_breaks_recovery_batch10_execute.py",
            "test_trading_breaks_recovery_batch10_integration_contract.py",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")

    progression = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
    text = progression.read_text(encoding="utf-8")
    text = text.replace(
        "date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25)):",
        "date(2024, 1, 1), date(2024, 3, 29), date(2024, 12, 25), date(2025, 1, 1), date(2025, 4, 18)):",
    )
    for day in ("2025, 1, 1", "2025, 4, 18"):
        queue_anchor = "    assert date(2024, 12, 25) in queue_days\n"
        line = f"    assert date({day}) in queue_days\n"
        if line not in text:
            text = text.replace(queue_anchor, queue_anchor + line)
        eligible_anchor = "    assert date(2024, 12, 25) not in eligible_days\n"
        line2 = f"    assert date({day}) not in eligible_days\n"
        if line2 not in text:
            text = text.replace(eligible_anchor, eligible_anchor + line2)
    batch09_line = "    assert all(day not in eligible_days for day, _ in ((date(2024, 9, 2), 'LABOR_DAY'), (date(2024, 11, 28), 'THANKSGIVING_DAY'), (date(2024, 11, 29), 'THANKSGIVING_FRIDAY'), (date(2024, 12, 24), 'CHRISTMAS_PRE_HOLIDAY_SESSION'), (date(2024, 12, 25), 'CHRISTMAS_OBSERVED')))\n"
    batch10_line = "    assert all(day not in eligible_days for day, _ in ((date(2024, 12, 31), 'NEW_YEARS_EVE_CANDIDATE'), (date(2025, 1, 1), 'NEW_YEARS_OBSERVED'), (date(2025, 1, 20), 'MARTIN_LUTHER_KING_DAY'), (date(2025, 2, 17), 'PRESIDENTS_DAY'), (date(2025, 4, 18), 'GOOD_FRIDAY')))\n"
    if batch10_line not in text:
        text = text.replace(batch09_line, batch09_line + batch10_line)
    progression.write_text(text, encoding="utf-8")


def rewrite_batch10_freeze_tests_as_historical() -> None:
    frozen = '''from __future__ import annotations

import inspect
from datetime import date

import tools.trading_breaks_recovery_batch10 as batch10_module
from tools.trading_breaks_recovery_batch10 import batch10_targets

EXPECTED_BATCH10 = [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2025, 1, 20), "MARTIN_LUTHER_KING_DAY"),
    (date(2025, 2, 17), "PRESIDENTS_DAY"),
    (date(2025, 4, 18), "GOOD_FRIDAY"),
]


def test_batch10_historical_frozen_identity_is_immutable_after_integration():
    assert batch10_targets() == EXPECTED_BATCH10


def test_batch10_accessor_remains_immutable_to_caller():
    altered = batch10_targets()
    altered.pop()
    assert batch10_targets() == EXPECTED_BATCH10


def test_batch10_frozen_module_remains_free_of_live_selection():
    source = inspect.getsource(batch10_module).lower()
    assert "eligible_recovery_queue(" not in source
    assert "recovery_queue(" not in source
    assert "probe_candidate" not in source
'''
    (REPO / "tests" / "test_trading_breaks_recovery_batch10.py").write_text(frozen, encoding="utf-8")

    contract = '''from __future__ import annotations

from datetime import date

import tools.freeze_trading_breaks_recovery_batch10 as freeze

HISTORICAL_FROZEN = [
    (date(2024, 12, 31), "NEW_YEARS_EVE_CANDIDATE"),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2025, 1, 20), "MARTIN_LUTHER_KING_DAY"),
    (date(2025, 2, 17), "PRESIDENTS_DAY"),
    (date(2025, 4, 18), "GOOD_FRIDAY"),
]
HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT = HISTORICAL_FROZEN + [
    (date(2025, 5, 26), "MEMORIAL_DAY"),
]


def test_batch10_freeze_historical_identity_preserved_without_live_rederivation():
    assert freeze.BATCH_SIZE == 5
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN, HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT) == {
        "verdict": "PASS", "reason": "EXACT_GOVERNED_ELIGIBLE_PREFIX"
    }


def test_batch10_historical_attacks_remain_rejected():
    eligible = HISTORICAL_ELIGIBLE_PREFIX_PLUS_NEXT
    reordered = [HISTORICAL_FROZEN[1], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(reordered, eligible)["verdict"] == "FAIL"
    assert freeze.validate_freeze_candidate(eligible[1:6], eligible)["reason"] == "FIRST_ELIGIBLE_MEMBER_SKIPPED"
    assert freeze.validate_freeze_candidate([*HISTORICAL_FROZEN[:-1], eligible[5]], eligible)["reason"] == "NON_PREFIX_MEMBER_SUBSTITUTED"
    assert freeze.validate_freeze_candidate(HISTORICAL_FROZEN[:-1], eligible)["reason"] == "BATCH_CARDINALITY_CHANGED"
    duplicate = [HISTORICAL_FROZEN[0], HISTORICAL_FROZEN[0], *HISTORICAL_FROZEN[2:]]
    assert freeze.validate_freeze_candidate(duplicate, eligible)["reason"] == "BATCH_DUPLICATE_DATE"
'''
    (REPO / "tests" / "test_trading_breaks_recovery_batch10_freeze_contract.py").write_text(contract, encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    guard_preintegration_state()
    integrate_calendar()
    integrate_attempt_ledger(report)
    rewrite_current_state_tests()
    rewrite_batch10_freeze_tests_as_historical()
    print("PASS: prepared Batch 10 atomic worktree integration")
    print("calendar PASS dates:", ", ".join(PASS_RECORDS))
    print("ledger attempts: 46..50")
    print("blocked unresolved:", ", ".join(BLOCKED_TARGETS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
