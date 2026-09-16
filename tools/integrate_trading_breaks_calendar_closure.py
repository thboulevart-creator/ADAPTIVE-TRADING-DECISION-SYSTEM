from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import (
    NO_SPECIAL_CHANGE_EVIDENCE,
    audit_calendar_coverage,
)
from tools.trading_breaks_negative_evidence_completeness import (
    CONTRACT as NEGATIVE_CONTRACT,
    PASS_REASON as NEGATIVE_PASS_REASON,
    SOURCE_OBSERVATIONS,
)
from tools.trading_breaks_recovery_progression import (
    eligible_recovery_queue,
    load_attempt_ledger,
    load_material_capability_changes,
    progression_decisions,
)
from tools.trading_breaks_recovery_protocol import recovery_queue
from tools.trading_breaks_target_day_overlap_semantics import (
    load_class_a_evidence,
    qualify_class_a,
)

REPO = Path(__file__).resolve().parents[1]
CALENDAR = REPO / "tools" / "dukascopy_usatech_calendar.py"
COVERAGE = REPO / "tools" / "dukascopy_usatech_calendar_coverage.py"
READJUDICATION_REPORT = (
    REPO
    / "reports"
    / "data-qualification"
    / "trading_breaks_target_day_overlap_readjudication.md"
)
NEGATIVE_REPORT = (
    REPO
    / "reports"
    / "data-qualification"
    / "trading_breaks_negative_evidence_completeness_qualification.md"
)

CURRENT_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2"
BASE_CAPABILITY_ID = "TRADING_BREAKS_PRIMARY_WIDGET_V1"
BLOCKER_CLASS_B = "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"

CLASS_A_PENDING: tuple[tuple[date, str], ...] = (
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2024, 3, 29), "GOOD_FRIDAY"),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2025, 4, 18), "GOOD_FRIDAY"),
    (date(2025, 12, 25), "CHRISTMAS_OBSERVED"),
    (date(2026, 1, 1), "NEW_YEARS_OBSERVED"),
    (date(2026, 4, 3), "GOOD_FRIDAY"),
)

CLASS_B: tuple[tuple[date, str], ...] = (
    (date(2021, 12, 31), "NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED"),
    (date(2022, 7, 1), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
    (date(2026, 7, 2), "INDEPENDENCE_PRE_HOLIDAY_SESSION"),
)

EXPECTED_QUEUE: tuple[tuple[date, str], ...] = (
    CLASS_B[0],
    CLASS_B[1],
    *CLASS_A_PENDING,
    CLASS_B[2],
)

CLASS_A_REASON_TOKENS = {
    "2023-12-25": "SPECIAL_CHRISTMAS_OBSERVED_2023_OVERLAP_V2",
    "2024-01-01": "SPECIAL_NEW_YEARS_OBSERVED_2024_OVERLAP_V2",
    "2024-03-29": "SPECIAL_GOOD_FRIDAY_2024_OVERLAP_V2",
    "2024-12-25": "SPECIAL_CHRISTMAS_OBSERVED_2024_OVERLAP_V2",
    "2025-01-01": "SPECIAL_NEW_YEARS_OBSERVED_2025_OVERLAP_V2",
    "2025-04-18": "SPECIAL_GOOD_FRIDAY_2025_OVERLAP_V2",
    "2025-12-25": "SPECIAL_CHRISTMAS_OBSERVED_2025_OVERLAP_V2",
    "2026-01-01": "SPECIAL_NEW_YEARS_OBSERVED_2026_OVERLAP_V2",
    "2026-04-03": "SPECIAL_GOOD_FRIDAY_2026_OVERLAP_V2",
}

NO_CHANGE_REASON = "NO_SPECIAL_CHANGE_EVIDENCE_TRADING_BREAKS_NEGATIVE_COMPLETENESS_V1"
READJUDICATION_REPORT_SOURCE = (
    "reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md"
)
NEGATIVE_REPORT_SOURCE = (
    "reports/data-qualification/trading_breaks_negative_evidence_completeness_qualification.md"
)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def _require_report_tokens(path: Path, tokens: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        if token not in text:
            raise RuntimeError(f"{label}_REPORT_MISMATCH:{token}")


def authoritative_class_a() -> list[dict[str, Any]]:
    _require_report_tokens(
        READJUDICATION_REPORT,
        (
            "PASS — `ALL_14_CLASS_A_DATES_OFFLINE_READJUDICATED_UNDER_QUALIFIED_V2`",
            "35065038684` / `104693341828",
            "108a35d9d2101635ba2122be316f1f32207d62f1",
            "14 PASS / 0 BLOCKED / 0 FAIL",
        ),
        "CLASS_A_READJUDICATION",
    )

    qualification = qualify_class_a()
    if qualification.get("verdict") != "PASS" or qualification.get("class_a_count") != 14:
        raise RuntimeError("CLASS_A_QUALIFICATION_NOT_AUTHORITATIVE")
    qualified_by_day = {
        date.fromisoformat(str(item["target_date"])): item
        for item in qualification.get("results", [])
    }

    raw_by_day: dict[date, dict[str, Any]] = {}
    for target_day, reason, raw, provenance, source_batch in load_class_a_evidence():
        if target_day not in dict(CLASS_A_PENDING):
            continue
        if reason != dict(CLASS_A_PENDING)[target_day]:
            raise RuntimeError(f"CLASS_A_REASON_MISMATCH:{target_day}")
        records = raw.get("matching_records")
        if not isinstance(records, list) or len(records) != 1:
            raise RuntimeError(f"CLASS_A_RAW_RECORD_CARDINALITY:{target_day}")
        record = records[0]
        raw_by_day[target_day] = {
            "candidate_reason": reason,
            "source_batch": source_batch,
            "source_attempt_id": f"batch{source_batch:02d}:{target_day.isoformat()}",
            "target_epoch_ms": raw.get("target_epoch_ms"),
            "broker_reason": str(record.get("reason", "")).strip(),
            "record_id": str(record.get("id", "")),
            "provenance": provenance,
        }

    result: list[dict[str, Any]] = []
    for target_day, reason in CLASS_A_PENDING:
        qualified = qualified_by_day.get(target_day)
        raw = raw_by_day.get(target_day)
        if not qualified or not raw:
            raise RuntimeError(f"CLASS_A_SOURCE_MISSING:{target_day}")
        if qualified.get("verdict") != "PASS":
            raise RuntimeError(f"CLASS_A_NOT_PASS:{target_day}")
        if qualified.get("reason") != "TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED":
            raise RuntimeError(f"CLASS_A_REASON_NOT_QUALIFIED:{target_day}")
        if qualified.get("source_batch") != raw["source_batch"]:
            raise RuntimeError(f"CLASS_A_SOURCE_BATCH_MISMATCH:{target_day}")
        if str(qualified.get("record_id")) != raw["record_id"]:
            raise RuntimeError(f"CLASS_A_RECORD_ID_MISMATCH:{target_day}")
        if qualified.get("artifact_id") != raw["provenance"].get("artifact_id"):
            raise RuntimeError(f"CLASS_A_ARTIFACT_ID_MISMATCH:{target_day}")
        if qualified.get("artifact_sha256") != raw["provenance"].get("artifact_sha256"):
            raise RuntimeError(f"CLASS_A_ARTIFACT_SHA_MISMATCH:{target_day}")
        if qualified.get("probe_commit") != raw["provenance"].get("probe_commit"):
            raise RuntimeError(f"CLASS_A_PROBE_COMMIT_MISMATCH:{target_day}")
        if not raw["broker_reason"]:
            raise RuntimeError(f"CLASS_A_BROKER_REASON_MISSING:{target_day}")
        if raw["target_epoch_ms"] is None:
            raise RuntimeError(f"CLASS_A_TARGET_EPOCH_MISSING:{target_day}")
        item = dict(qualified)
        item.update(raw)
        item["target_date"] = target_day.isoformat()
        item["candidate_reason"] = reason
        result.append(item)

    if [(date.fromisoformat(x["target_date"]), x["candidate_reason"]) for x in result] != list(CLASS_A_PENDING):
        raise RuntimeError("CLASS_A_PENDING_IDENTITY_OR_ORDER_MISMATCH")
    return result


def authoritative_class_b() -> list[dict[str, Any]]:
    _require_report_tokens(
        NEGATIVE_REPORT,
        (
            "PASS — `ALL_THREE_CLASS_B_DATES_HAVE_COMPLETE_BROKER_NATIVE_NEGATIVE_EVIDENCE`",
            "35097034040 / 104796843502",
            "20 passed in 0.07s",
            NEGATIVE_PASS_REASON,
        ),
        "CLASS_B_NEGATIVE_COMPLETENESS",
    )

    _, current_id, attempts = load_attempt_ledger()
    if current_id != CURRENT_CAPABILITY_ID:
        raise RuntimeError("CLASS_B_CURRENT_CAPABILITY_MISMATCH")
    attempts_by_id = {item.attempt_id: item for item in attempts}
    if len(attempts_by_id) != len(attempts):
        raise RuntimeError("CLASS_B_DUPLICATE_ATTEMPT_ID")

    result: list[dict[str, Any]] = []
    for target_day, reason in CLASS_B:
        sources = [
            source
            for source in SOURCE_OBSERVATIONS
            if source["target_date"] == target_day.isoformat()
        ]
        expected_count = 2 if target_day == date(2021, 12, 31) else 1
        if len(sources) != expected_count:
            raise RuntimeError(f"CLASS_B_SOURCE_OBSERVATION_COUNT:{target_day}")

        source_attempt_ids: list[str] = []
        runtime_paths: list[str] = []
        artifact_ids: list[int] = []
        artifact_sha256s: list[str] = []
        probe_commits: list[str] = []
        workflow_runs: list[int] = []
        for source in sources:
            if source["candidate_reason"] != reason:
                raise RuntimeError(f"CLASS_B_SOURCE_REASON_MISMATCH:{target_day}")
            attempt_id = str(source["attempt_id"])
            attempt = attempts_by_id.get(attempt_id)
            if attempt is None:
                raise RuntimeError(f"CLASS_B_SOURCE_ATTEMPT_MISSING:{attempt_id}")
            if attempt.target_date != target_day or attempt.candidate_reason != reason:
                raise RuntimeError(f"CLASS_B_SOURCE_ATTEMPT_IDENTITY_MISMATCH:{attempt_id}")
            if attempt.outcome != "BLOCKED" or attempt.blocking_reason != BLOCKER_CLASS_B:
                raise RuntimeError(f"CLASS_B_SOURCE_ATTEMPT_BLOCKER_MISMATCH:{attempt_id}")
            if attempt.capability_id != BASE_CAPABILITY_ID:
                raise RuntimeError(f"CLASS_B_SOURCE_ATTEMPT_CAPABILITY_MISMATCH:{attempt_id}")
            source_attempt_ids.append(attempt_id)
            runtime_paths.append(str(source["runtime_path"]))
            artifact_ids.append(int(attempt.provenance["artifact_id"]))
            artifact_sha256s.append(str(attempt.provenance["artifact_sha256"]))
            probe_commits.append(str(attempt.provenance["probe_commit"]))
            workflow_runs.append(int(attempt.provenance["workflow_run"]))

        result.append(
            {
                "target_date": target_day.isoformat(),
                "candidate_reason": reason,
                "source_attempt_ids": tuple(source_attempt_ids),
                "runtime_paths": tuple(runtime_paths),
                "artifact_ids": tuple(artifact_ids),
                "artifact_sha256s": tuple(artifact_sha256s),
                "probe_commits": tuple(probe_commits),
                "workflow_runs": tuple(workflow_runs),
            }
        )

    if [(date.fromisoformat(x["target_date"]), x["candidate_reason"]) for x in result] != list(CLASS_B):
        raise RuntimeError("CLASS_B_IDENTITY_OR_ORDER_MISMATCH")
    return result


def guard_preintegration_state() -> None:
    global_audit = audit_calendar_coverage()
    window_audit = audit_calendar_coverage(date(2021, 8, 14), date(2026, 8, 14))
    global_counts = (
        global_audit["candidate_dates"],
        global_audit["resolved_candidate_dates"],
        global_audit["unresolved_candidate_dates"],
    )
    window_counts = (
        window_audit["candidate_dates"],
        window_audit["resolved_candidate_dates"],
        window_audit["unresolved_candidate_dates"],
    )
    if global_counts != (111, 79, 32):
        raise RuntimeError(f"PRE_CLOSURE_GLOBAL_COUNTS_MISMATCH:{global_counts}")
    if window_counts != (68, 56, 12):
        raise RuntimeError(f"PRE_CLOSURE_WINDOW_COUNTS_MISMATCH:{window_counts}")
    if global_audit["orphan_special_evidence"] or global_audit["contradictory_evidence_dates"] or global_audit["evidence_shape_errors"]:
        raise RuntimeError("PRE_CLOSURE_CALENDAR_INTEGRITY_FAILURE")

    queue = recovery_queue()
    if queue != list(EXPECTED_QUEUE):
        raise RuntimeError(f"PRE_CLOSURE_QUEUE_MISMATCH:{queue}")
    decisions = progression_decisions()
    if [(d.target_date, d.candidate_reason) for d in decisions] != queue:
        raise RuntimeError("PRE_CLOSURE_PROGRESSION_IDENTITY_MISMATCH")
    if eligible_recovery_queue() != list(CLASS_A_PENDING):
        raise RuntimeError("PRE_CLOSURE_ELIGIBLE_QUEUE_MISMATCH")

    capabilities, current_id, attempts = load_attempt_ledger()
    if current_id != CURRENT_CAPABILITY_ID or current_id not in capabilities:
        raise RuntimeError("PRE_CLOSURE_CURRENT_CAPABILITY_MISMATCH")
    if len(attempts) != 73:
        raise RuntimeError("PRE_CLOSURE_LEDGER_COUNT_MISMATCH")
    if [item.attempt_sequence for item in attempts] != list(range(1, 74)):
        raise RuntimeError("PRE_CLOSURE_LEDGER_SEQUENCE_MISMATCH")
    if len(load_material_capability_changes()) != 1:
        raise RuntimeError("PRE_CLOSURE_CAPABILITY_CHANGE_COUNT_MISMATCH")

    for target_day, _ in CLASS_A_PENDING:
        if target_day in SPECIAL_SESSION_EVIDENCE:
            raise RuntimeError(f"CLASS_A_ALREADY_IN_SPECIAL_EVIDENCE:{target_day}")
    for target_day, _ in CLASS_B:
        if target_day in SPECIAL_SESSION_EVIDENCE or target_day in NO_SPECIAL_CHANGE_EVIDENCE:
            raise RuntimeError(f"CLASS_B_ALREADY_RESOLVED:{target_day}")
    if NO_SPECIAL_CHANGE_EVIDENCE:
        raise RuntimeError("PRE_CLOSURE_NO_SPECIAL_CHANGE_EVIDENCE_NOT_EMPTY")


def _range_expr(hours: list[int]) -> str:
    if not hours:
        raise RuntimeError("CLASS_A_EMPTY_CLOSED_HOURS")
    if hours != list(range(hours[0], hours[-1] + 1)):
        raise RuntimeError(f"CLASS_A_NONCONTIGUOUS_CLOSED_HOURS:{hours}")
    return f"frozenset(range({hours[0]}, {hours[-1] + 1}))"


def render_class_a_entry(item: dict[str, Any]) -> str:
    target_day = date.fromisoformat(item["target_date"])
    reason_token = CLASS_A_REASON_TOKENS[item["target_date"]]
    epoch = int(item["target_epoch_ms"])
    hours = [int(x) for x in item["fully_closed_hours_utc"]]
    return f'''    date({target_day.year}, {target_day.month}, {target_day.day}): {{
        "reason": "{reason_token}",
        "fully_closed_hours_utc": {_range_expr(hours)},
        "broker_record_id": "{item['record_id']}",
        "broker_reason": {item['broker_reason']!r},
        "artifact_id": {item['artifact_id']},
        "artifact_sha256": "{item['artifact_sha256']}",
        "probe_commit": "{item['probe_commit']}",
        "target_day_overlap_capability": "{CURRENT_CAPABILITY_ID}",
        "source_attempt_id": "{item['source_attempt_id']}",
        "dukascopy_widget_source": (
            "https://freeserv.dukascopy.com/2.0/"
            "?path=trading_breaks%2Findex&currentDate=false&date={epoch}"
        ),
        "runtime_evidence_source": (
            "https://github.com/thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM/actions/runs/{item['workflow_run']}"
        ),
        "qualification_report_source": (
            "{READJUDICATION_REPORT_SOURCE}"
        ),
    }},
'''


def _tuple_literal(values: tuple[Any, ...]) -> str:
    if len(values) == 1:
        return f"({values[0]!r},)"
    return repr(values)


def render_class_b_entry(item: dict[str, Any]) -> str:
    target_day = date.fromisoformat(item["target_date"])
    return f'''    date({target_day.year}, {target_day.month}, {target_day.day}): {{
        "reason": "{NO_CHANGE_REASON}",
        "negative_evidence_contract": "{NEGATIVE_CONTRACT}",
        "negative_evidence_reason": "{NEGATIVE_PASS_REASON}",
        "instrument_name": "USATECH.IDX/USD",
        "instrument_id": "9016",
        "source_attempt_ids": {_tuple_literal(item['source_attempt_ids'])},
        "source_artifact_ids": {_tuple_literal(item['artifact_ids'])},
        "source_artifact_sha256s": {_tuple_literal(item['artifact_sha256s'])},
        "source_probe_commits": {_tuple_literal(item['probe_commits'])},
        "source_workflow_runs": {_tuple_literal(item['workflow_runs'])},
        "runtime_evidence_sources": {_tuple_literal(item['runtime_paths'])},
        "qualification_report_source": "{NEGATIVE_REPORT_SOURCE}",
    }},
'''


def integrate_calendar(class_a: list[dict[str, Any]]) -> None:
    text = CALENDAR.read_text(encoding="utf-8")
    block = "".join(render_class_a_entry(item) for item in class_a)
    marker = '}\n\nCALENDAR_CONTRACT = "DUKASCOPY_USATECH_SESSION_CALENDAR_V3"'
    text = replace_once(text, marker, block + marker, "calendar closure Class-A insertion")
    CALENDAR.write_text(text, encoding="utf-8")


def integrate_no_special_change(class_b: list[dict[str, Any]]) -> None:
    text = COVERAGE.read_text(encoding="utf-8")
    marker = "NO_SPECIAL_CHANGE_EVIDENCE: dict[date, dict] = {}"
    block = "NO_SPECIAL_CHANGE_EVIDENCE: dict[date, dict] = {\n" + "".join(
        render_class_b_entry(item) for item in class_b
    ) + "}"
    text = replace_once(text, marker, block, "calendar closure Class-B insertion")
    COVERAGE.write_text(text, encoding="utf-8")


def main() -> int:
    guard_preintegration_state()
    class_a = authoritative_class_a()
    class_b = authoritative_class_b()
    integrate_calendar(class_a)
    integrate_no_special_change(class_b)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
