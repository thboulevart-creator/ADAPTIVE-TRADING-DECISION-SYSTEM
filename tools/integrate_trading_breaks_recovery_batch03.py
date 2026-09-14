from __future__ import annotations

import json
from pathlib import Path

from tools.trading_breaks_recovery_batch03 import BATCH_CONTRACT, batch03_targets


REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
LEDGER = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_attempt_ledger.json"
ADJUDICATION = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch03_adjudication.json"
PROTOCOL_TEST = REPO / "tests" / "test_trading_breaks_recovery_protocol.py"
PROGRESSION_TEST = REPO / "tests" / "test_trading_breaks_recovery_progression.py"
BATCH03_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03.py"
CALENDAR_TEST = REPO / "tests" / "test_dukascopy_usatech_calendar_2022_batch03.py"
INTEGRATION_TEST = REPO / "tests" / "test_trading_breaks_recovery_batch03_integration.py"

RUN_ID = 34892253133
JOB_ID = 104137558818
PROBE_COMMIT = "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4"
ARTIFACT_ID = 10367930592
ARTIFACT_SHA256 = "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41"
CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"

PASS_RECORDS = {
    "2022-05-30": ("SPECIAL_MEMORIAL_DAY_2022", "37019", "Memorial Day", 1653868800000),
    "2022-06-20": ("SPECIAL_JUNETEENTH_OBSERVED_2022", "38945", "Juneteenth Holiday", 1655683200000),
    "2022-07-04": ("SPECIAL_INDEPENDENCE_DAY_2022", "41225", "Independence Day", 1656892800000),
    "2022-09-05": ("SPECIAL_LABOR_DAY_2022", "42569", "Labor Day", 1662336000000),
}
BLOCKED_DATE = "2022-07-01"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def load_authoritative_adjudication() -> dict:
    report = json.loads(ADJUDICATION.read_text(encoding="utf-8"))
    if report.get("verdict") != "PASS":
        raise RuntimeError("BATCH03_ADJUDICATION_NOT_PASS")
    if (report.get("attempted"), report.get("pass"), report.get("blocked"), report.get("fail")) != (5, 4, 1, 0):
        raise RuntimeError("BATCH03_ADJUDICATION_ACCOUNTING_MISMATCH")
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
            raise RuntimeError(f"BATCH03_ADJUDICATION_PROVENANCE_MISMATCH:{key}")

    expected_verdicts = ["PASS", "PASS", "BLOCKED", "PASS", "PASS"]
    observed = [item.get("verdict") for item in report.get("adjudications", [])]
    if observed != expected_verdicts:
        raise RuntimeError("BATCH03_ADJUDICATION_DATE_ORDER_OR_VERDICT_MISMATCH")
    if report["adjudications"][2].get("reason") != "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED":
        raise RuntimeError("BATCH03_BLOCKED_REASON_MISMATCH")
    return report


def integrate_calendar() -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    reason_tokens = [record[0] for record in PASS_RECORDS.values()]
    present = [token in text for token in reason_tokens]
    if all(present):
        if "date(2022, 7, 1):" in text:
            raise RuntimeError("BLOCKED_DATE_WAS_SILENTLY_PROMOTED")
        return
    if any(present):
        raise RuntimeError("PARTIAL_BATCH03_CALENDAR_INTEGRATION_DETECTED")
    if "date(2022, 7, 1):" in text:
        raise RuntimeError("BLOCKED_DATE_ALREADY_PRESENT_IN_SPECIAL_EVIDENCE")

    marker = "    date(2025, 1, 9): {\n"
    entries: list[str] = []
    for day, (reason, record_id, broker_reason, request_epoch_ms) in PASS_RECORDS.items():
        year, month, dom = [int(x) for x in day.split("-")]
        entries.append(
            f'''    date({year}, {month}, {dom}): {{
        "reason": "{reason}",
        # Broker-native Trading Breaks record {record_id}: 16:59-21:59 UTC.
        # Calibrated reopen is 22:00 UTC; hour 16 is partially tradable, so
        # only whole UTC hours 17-21 are proven fully closed.
        "fully_closed_hours_utc": frozenset(range(17, 22)),
        "broker_record_id": "{record_id}",
        "broker_reason": "{broker_reason}",
        "artifact_id": {ARTIFACT_ID},
        "artifact_sha256": "{ARTIFACT_SHA256}",
        "probe_commit": "{PROBE_COMMIT}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={request_epoch_ms}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{RUN_ID}"
        ),
        "qualification_report_source": (
            "reports/data-qualification/"
            "historical_trading_breaks_recovery_batch03_qualification.md"
        ),
    }},
'''
        )
    block = "".join(entries)
    CALENDAR.write_text(
        replace_once(text, marker, block + marker, "calendar Batch 03 insertion"),
        encoding="utf-8",
    )


def integrate_attempt_ledger(report: dict) -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    attempts = ledger.get("attempts")
    if not isinstance(attempts, list):
        raise RuntimeError("ATTEMPT_LEDGER_MALFORMED")

    existing_batch03 = [x for x in attempts if str(x.get("attempt_id", "")).startswith("batch03:")]
    if existing_batch03:
        if len(existing_batch03) != 5:
            raise RuntimeError("PARTIAL_BATCH03_ATTEMPT_LEDGER_DETECTED")
        return
    if len(attempts) != 10:
        raise RuntimeError(f"PRE_BATCH03_ATTEMPT_COUNT_MISMATCH:{len(attempts)}")

    provenance = {
        "workflow_run": RUN_ID,
        "job_id": JOB_ID,
        "artifact_id": ARTIFACT_ID,
        "artifact_sha256": ARTIFACT_SHA256,
        "probe_commit": PROBE_COMMIT,
    }
    adjudications = report["adjudications"]
    for offset, ((target_day, candidate_reason), adjudication) in enumerate(
        zip(batch03_targets(), adjudications, strict=True),
        start=11,
    ):
        outcome = adjudication["verdict"]
        reason = adjudication["reason"]
        attempts.append(
            {
                "attempt_sequence": offset,
                "attempt_id": f"batch03:{target_day.isoformat()}",
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
        "test_queue_scope_sorted_and_has_61_unresolved_candidates_after_batch02",
        "test_queue_scope_sorted_and_has_57_unresolved_candidates_after_batch03",
        "protocol test name",
    )
    text = replace_once(text, "assert len(queue) == 61", "assert len(queue) == 57", "protocol queue count")
    PROTOCOL_TEST.write_text(text, encoding="utf-8")


def update_progression_test() -> None:
    text = PROGRESSION_TEST.read_text(encoding="utf-8")
    replacements = [
        (
            "test_attempt_ledger_preserves_all_ten_historical_attempts_and_duplicate_history",
            "test_attempt_ledger_preserves_all_fifteen_historical_attempts_and_duplicate_history",
            "progression ledger test name",
        ),
        ("assert len(attempts) == 10", "assert len(attempts) == 15", "progression attempt count"),
        ("list(range(1, 11))", "list(range(1, 16))", "progression sequences"),
        ("len({item.attempt_id for item in attempts}) == 10", "len({item.attempt_id for item in attempts}) == 15", "progression attempt ids"),
        ("assert len(decisions) == len(queue) == 61", "assert len(decisions) == len(queue) == 57", "progression unresolved count"),
        (
            "test_unchanged_capability_forbids_third_retry_of_historical_blocked_dates",
            "test_unchanged_capability_forbids_replay_of_historical_blocked_dates",
            "progression blocked replay name",
        ),
        (
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15)):",
            "for target in (date(2021, 12, 24), date(2021, 12, 31), date(2022, 4, 15), date(2022, 7, 1)):",
            "progression blocked loop",
        ),
        (
            'assert eligible[0] == (date(2022, 5, 30), "MEMORIAL_DAY")',
            'assert eligible[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")',
            "progression first eligible",
        ),
        (
            "    assert date(2022, 5, 30) in eligible_days\n",
            "    assert date(2022, 7, 1) not in eligible_days\n    assert date(2022, 11, 24) in eligible_days\n",
            "progression post Batch03 eligible assertions",
        ),
    ]
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)

    blocked_anchor = "    assert date(2022, 4, 15) in queue_days\n"
    text = replace_once(
        text,
        blocked_anchor,
        blocked_anchor + "    assert date(2022, 7, 1) in queue_days\n",
        "progression blocked calendar set",
    )
    PROGRESSION_TEST.write_text(text, encoding="utf-8")


def rewrite_batch03_test() -> None:
    BATCH03_TEST.write_text('''from __future__ import annotations

import inspect
from datetime import date

from tools.trading_breaks_recovery_batch03 import (
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    FREEZE_BASELINE_HEAD,
    FROZEN_BATCH03_TARGETS,
    SELECTION_RULE,
    SOURCE_PROGRESSION_RUNTIME_COMMIT,
    batch03_targets,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


EXPECTED_BATCH03 = [
    (date(2022, 5, 30), "MEMORIAL_DAY"),
    (date(2022, 6, 20), "JUNETEENTH_OBSERVED"),
    (date(2022, 7, 1), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2022, 7, 4), "INDEPENDENCE_DAY_OBSERVED"),
    (date(2022, 9, 5), "LABOR_DAY"),
]
PASS_DAYS = {
    date(2022, 5, 30),
    date(2022, 6, 20),
    date(2022, 7, 4),
    date(2022, 9, 5),
}
BLOCKED_DAY = date(2022, 7, 1)
ALL_ATTEMPTED_BLOCKED = {
    date(2021, 12, 24),
    date(2021, 12, 31),
    date(2022, 4, 15),
    BLOCKED_DAY,
}


def test_batch03_size_and_historical_membership_remain_frozen():
    assert BATCH_SIZE == 5
    assert len(FROZEN_BATCH03_TARGETS) == BATCH_SIZE
    assert batch03_targets() == EXPECTED_BATCH03


def test_batch03_historical_membership_is_chronological_unique_and_immutable():
    first = batch03_targets()
    days = [day for day, _ in first]
    assert days == sorted(days)
    assert len(days) == len(set(days))
    first.pop()
    first.insert(0, (date(2099, 1, 1), "MANUAL_INJECTION"))
    assert batch03_targets() == EXPECTED_BATCH03


def test_post_adjudication_calendar_integrates_only_batch03_pass_dates():
    raw_days = {day for day, _ in recovery_queue()}
    assert PASS_DAYS.isdisjoint(raw_days)
    assert BLOCKED_DAY in raw_days


def test_post_adjudication_attempt_ledger_records_all_five_batch03_attempts():
    _, _, attempts = load_attempt_ledger()
    batch03 = [item for item in attempts if item.attempt_id.startswith("batch03:")]
    assert [item.attempt_sequence for item in batch03] == [11, 12, 13, 14, 15]
    assert [item.target_date for item in batch03] == [day for day, _ in EXPECTED_BATCH03]
    assert [item.outcome for item in batch03] == ["PASS", "PASS", "BLOCKED", "PASS", "PASS"]
    assert batch03[2].blocking_reason == "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"
    assert all(item.capability_id == CURRENT_CAPABILITY_ID for item in batch03)


def test_all_attempted_blocked_dates_remain_unresolved_but_ineligible_same_capability():
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


def test_batch03_dates_cannot_reenter_execution_projection_after_attempt():
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    assert {day for day, _ in EXPECTED_BATCH03}.isdisjoint(eligible_days)
    assert eligible_recovery_queue()[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")


def test_batch03_target_accessor_cannot_accept_manual_selection_inputs():
    assert inspect.signature(batch03_targets).parameters == {}


def test_selection_rule_and_freeze_provenance_remain_historical_truth():
    assert SELECTION_RULE == "FIRST_N_OF_GOVERNED_ELIGIBLE_RECOVERY_QUEUE_AT_FREEZE"
    assert FREEZE_BASELINE_HEAD == "d4dab0a10ba6bc782186159899f7b8225e7aab59"
    assert SOURCE_PROGRESSION_RUNTIME_COMMIT == "b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2"
    assert CURRENT_CAPABILITY_ID == "TRADING_BREAKS_PRIMARY_WIDGET_V1"
    assert CURRENT_CAPABILITY_FINGERPRINT == (
        "82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f"
    )


def test_batch03_membership_contains_no_expected_outcome_or_priority_surface():
    source = inspect.getsource(batch03_targets).lower()
    assert "expected_outcome" not in source
    assert "priority" not in source
    assert "manual_skip" not in source
    assert "holiday_type" not in source
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
    date(2022, 5, 30): ("SPECIAL_MEMORIAL_DAY_2022", "37019"),
    date(2022, 6, 20): ("SPECIAL_JUNETEENTH_OBSERVED_2022", "38945"),
    date(2022, 7, 4): ("SPECIAL_INDEPENDENCE_DAY_2022", "41225"),
    date(2022, 9, 5): ("SPECIAL_LABOR_DAY_2022", "42569"),
}


def test_batch03_pass_dates_use_exact_broker_1659_2159_break_semantics():
    for day, (reason, record_id) in EXPECTED.items():
        record = SPECIAL_SESSION_EVIDENCE[day]
        assert record["reason"] == reason
        assert record["broker_record_id"] == record_id
        assert record["fully_closed_hours_utc"] == frozenset(range(17, 22))
        assert classify_slot(day, 16).status == EXPECTED_OPEN
        for hour in range(17, 22):
            slot = classify_slot(day, hour)
            assert slot.status == EXPECTED_CLOSED
            assert slot.reason == reason
        assert classify_slot(day, 22).status == EXPECTED_OPEN


def test_batch03_blocked_july_1_is_not_promoted_to_special_or_normal_evidence():
    assert date(2022, 7, 1) not in SPECIAL_SESSION_EVIDENCE
''', encoding="utf-8")


def create_integration_test() -> None:
    INTEGRATION_TEST.write_text('''from datetime import date

from tools.dukascopy_usatech_calendar_coverage import audit_calendar_coverage
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue


def test_batch03_integration_global_and_window_accounting_is_exact():
    global_report = audit_calendar_coverage()
    window_report = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    assert global_report["candidate_dates"] == 111
    assert global_report["resolved_candidate_dates"] == 34
    assert global_report["unresolved_candidate_dates"] == 77
    assert global_report["evidence_shape_errors"] == []
    assert global_report["orphan_special_evidence"] == []
    assert global_report["contradictory_evidence_dates"] == []
    assert window_report["candidate_dates"] == 68
    assert window_report["resolved_candidate_dates"] == 11
    assert window_report["unresolved_candidate_dates"] == 57


def test_batch03_integration_progression_accounting_is_exact_and_non_starving():
    _, _, attempts = load_attempt_ledger()
    decisions = progression_decisions()
    eligible = eligible_recovery_queue()
    assert len(attempts) == 15
    assert len(recovery_queue()) == len(decisions) == 57
    assert sum(not d.eligible and d.latest_attempt_outcome == "BLOCKED" for d in decisions) == 4
    assert len(eligible) == 53
    assert eligible[0] == (date(2022, 11, 24), "THANKSGIVING_DAY")
    assert load_material_capability_changes() == []


def test_batch03_blocked_date_remains_unresolved_but_not_retryable_same_capability():
    raw_days = {day for day, _ in recovery_queue()}
    eligible_days = {day for day, _ in eligible_recovery_queue()}
    assert date(2022, 7, 1) in raw_days
    assert date(2022, 7, 1) not in eligible_days
''', encoding="utf-8")


def main() -> int:
    report = load_authoritative_adjudication()
    integrate_calendar()
    integrate_attempt_ledger(report)
    update_protocol_test()
    update_progression_test()
    rewrite_batch03_test()
    create_calendar_test()
    create_integration_test()
    print(
        "Prepared atomic Batch 03 integration: 4 PASS calendar dates + 5 immutable attempts; "
        "2022-07-01 remains unresolved/BLOCKED; no negative-evidence promotion."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
