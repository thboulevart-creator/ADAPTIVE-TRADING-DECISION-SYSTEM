from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_batch04 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch04_targets,
)
from tools.trading_breaks_recovery_protocol import (
    CONTRACT as RECOVERY_PROTOCOL,
    RecoveryEvidence,
    validate_positive_recovery_against_frozen_batch,
)


REPO = Path(__file__).resolve().parents[1]
RUNTIME_PATH = (
    REPO
    / "reports"
    / "data-qualification"
    / "historical_trading_breaks_recovery_batch04_runtime.json"
)
ADJUDICATION_JSON = (
    REPO
    / "reports"
    / "data-qualification"
    / "historical_trading_breaks_recovery_batch04_adjudication.json"
)
QUALIFICATION_MD = (
    REPO
    / "reports"
    / "data-qualification"
    / "historical_trading_breaks_recovery_batch04_qualification.md"
)

EXPECTED_RUN = 34895457466
EXPECTED_JOB = 104148201341
EXPECTED_ARTIFACT = 10369230708
EXPECTED_ARTIFACT_SHA256 = (
    "3e6d259f24fce540d39560cdc2714963cdd887f67f362aa9bc90eafa3d4176dc"
)
EXPECTED_PROBE_COMMIT = "11a81294720898802e49dd1131a64e20e7e7ae3a"
TARGET_INSTRUMENT_NAME = "USATECH.IDX/USD"
TARGET_INSTRUMENT_ID = "9016"


def _epoch_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _utc_from_ms(value: Any) -> datetime:
    if isinstance(value, bool):
        raise ValueError("BOOLEAN_IS_NOT_EPOCH")
    return datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc)


def _parse_dom_line(line: str) -> dict[str, Any]:
    parts = [part.strip() for part in line.split("\t")]
    if len(parts) != 4:
        raise ValueError("DOM_WITNESS_SHAPE_INVALID")
    instrument_name, start_raw, end_raw, reason = parts
    if instrument_name != TARGET_INSTRUMENT_NAME:
        raise ValueError("DOM_WITNESS_INSTRUMENT_NAME_MISMATCH")
    start = datetime.strptime(start_raw, "%d-%b-%y %H:%M:%S").replace(
        tzinfo=timezone.utc
    )
    end = datetime.strptime(end_raw, "%d-%b-%y %H:%M:%S").replace(
        tzinfo=timezone.utc
    )
    return {
        "instrument": TARGET_INSTRUMENT_ID,
        "start": _epoch_ms(start),
        "end": _epoch_ms(end),
        "reason": reason,
    }


def _dom_matches_network(dom: dict[str, Any], network: dict[str, Any]) -> bool:
    try:
        return (
            str(dom["instrument"]) == str(network["instrument"])
            and int(dom["start"]) == int(network["start"])
            and int(dom["end"]) == int(network["end"])
            and str(dom.get("reason", "")).strip()
            == str(network.get("reason", "")).strip()
        )
    except (KeyError, TypeError, ValueError):
        return False


def _validate_runtime_identity(runtime: dict[str, Any]) -> dict[str, Any]:
    if runtime.get("schema") != BATCH_CONTRACT:
        raise ValueError("RUNTIME_SCHEMA_MISMATCH")
    if runtime.get("parent_protocol") != RECOVERY_PROTOCOL:
        raise ValueError("PARENT_PROTOCOL_MISMATCH")
    if runtime.get("parent_progression_contract") != PARENT_PROGRESSION_CONTRACT:
        raise ValueError("PARENT_PROGRESSION_MISMATCH")
    if runtime.get("batch_number") != 4 or runtime.get("batch_size") != BATCH_SIZE:
        raise ValueError("BATCH_IDENTITY_MISMATCH")
    if runtime.get("selection_rule") != SELECTION_RULE:
        raise ValueError("SELECTION_RULE_MISMATCH")
    if runtime.get("capability_id") != CURRENT_CAPABILITY_ID:
        raise ValueError("CAPABILITY_ID_MISMATCH")
    if runtime.get("capability_fingerprint") != CURRENT_CAPABILITY_FINGERPRINT:
        raise ValueError("CAPABILITY_FINGERPRINT_MISMATCH")

    expected_targets = [
        {"date": day.isoformat(), "reason": reason}
        for day, reason in batch04_targets()
    ]
    if runtime.get("targets") != expected_targets:
        raise ValueError("FROZEN_MEMBERSHIP_MISMATCH")
    if runtime.get("read_only") is not True or runtime.get("market_data_written") is not False:
        raise ValueError("RUNTIME_READ_ONLY_BOUNDARY_MISMATCH")
    if runtime.get("workflow_run") != str(EXPECTED_RUN):
        raise ValueError("RUNTIME_RUN_ID_MISMATCH")
    if runtime.get("probe_commit") != EXPECTED_PROBE_COMMIT:
        raise ValueError("RUNTIME_PROBE_COMMIT_MISMATCH")

    provenance = runtime.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("PROVENANCE_MISSING")
    expected = {
        "workflow_run": EXPECTED_RUN,
        "job_id": EXPECTED_JOB,
        "probe_commit": EXPECTED_PROBE_COMMIT,
        "artifact_id": EXPECTED_ARTIFACT,
        "artifact_sha256": EXPECTED_ARTIFACT_SHA256,
    }
    for key, value in expected.items():
        if provenance.get(key) != value:
            raise ValueError(f"PROVENANCE_MISMATCH:{key}")
    return provenance


def _validate_result_envelope(
    raw: dict[str, Any],
    target_day: date,
    candidate_reason: str,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    if raw.get("target_date") != target_day.isoformat():
        raise ValueError("RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH")
    if raw.get("candidate_reason") != candidate_reason:
        raise ValueError("RESULT_REASON_MISMATCH")
    if raw.get("requested_date") != target_day.isoformat():
        raise ValueError("RESULT_REQUESTED_DATE_MISMATCH")
    if raw.get("instrument_id_observed") != TARGET_INSTRUMENT_ID:
        raise ValueError("RESULT_OBSERVED_INSTRUMENT_MISMATCH")
    if raw.get("instrument_name") != TARGET_INSTRUMENT_NAME:
        raise ValueError("RESULT_INSTRUMENT_NAME_MISMATCH")
    if raw.get("date_honored") is not True:
        raise ValueError("RESULT_DATE_NOT_HONORED")
    if raw.get("raw_payload_present") is not True:
        raise ValueError("RESULT_RAW_PAYLOAD_MISSING")
    if raw.get("runtime_errors"):
        raise ValueError("RESULT_RUNTIME_ERRORS_PRESENT")

    records = raw.get("matching_records")
    if not isinstance(records, list):
        raise ValueError("MATCHING_RECORDS_NOT_LIST")
    if len(records) > 1:
        raise ValueError("MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION")

    dom_lines = raw.get("dom_witness_lines")
    if not isinstance(dom_lines, list):
        raise ValueError("DOM_WITNESS_LINES_NOT_LIST")
    if len(dom_lines) > 1:
        raise ValueError("MULTIPLE_DOM_WITNESSES_REQUIRE_SEPARATE_ADJUDICATION")
    dom_record = _parse_dom_line(dom_lines[0]) if dom_lines else None
    return records, dom_record


def _overlap_blocked_verdict(
    *,
    target_day: date,
    candidate_reason: str,
    network_record: dict[str, Any],
    dom_record: dict[str, Any] | None,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    if str(network_record.get("instrument")) != TARGET_INSTRUMENT_ID:
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_WRONG_INSTRUMENT"}
    if not str(network_record.get("reason", "")).strip():
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_REASON_MISSING"}
    try:
        start = _utc_from_ms(network_record["start"])
        end = _utc_from_ms(network_record["end"])
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"verdict": "FAIL", "reason": "MALFORMED_NETWORK_INTERVAL"}
    if end < start:
        return {"verdict": "FAIL", "reason": "MALFORMED_NETWORK_INTERVAL"}
    if start.date() == target_day:
        return {"verdict": "FAIL", "reason": "OVERLAP_PATH_USED_FOR_EXACT_TARGET_RECORD"}

    reopen = end + timedelta(seconds=60)
    target_start = datetime(
        target_day.year, target_day.month, target_day.day, tzinfo=timezone.utc
    )
    target_end = target_start + timedelta(days=1)
    if not (start < target_end and reopen > target_start):
        return {"verdict": "FAIL", "reason": "NON_TARGET_RECORD_DOES_NOT_OVERLAP_TARGET_DAY"}

    if dom_record is not None and not _dom_matches_network(dom_record, network_record):
        return {"verdict": "FAIL", "reason": "DOM_NETWORK_CONTRADICTION"}

    return {
        "schema": RECOVERY_PROTOCOL,
        "verdict": "BLOCKED",
        "reason": "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE",
        "target_date": target_day.isoformat(),
        "candidate_reason": candidate_reason,
        "instrument": TARGET_INSTRUMENT_NAME,
        "instrument_id": TARGET_INSTRUMENT_ID,
        "overlap_record_id": str(network_record.get("id")),
        "overlap_record_reason": str(network_record.get("reason")),
        "overlap_start_utc": start.isoformat().replace("+00:00", "Z"),
        "overlap_final_closed_minute_utc": end.isoformat().replace("+00:00", "Z"),
        "overlap_reopen_utc": reopen.isoformat().replace("+00:00", "Z"),
        "dom_witness_present": dom_record is not None,
        "workflow_run": provenance["workflow_run"],
        "artifact_id": provenance["artifact_id"],
        "artifact_sha256": provenance["artifact_sha256"],
        "probe_commit": provenance["probe_commit"],
    }


def adjudicate_runtime(runtime: dict[str, Any]) -> dict[str, Any]:
    provenance = _validate_runtime_identity(runtime)
    results = runtime.get("results")
    if not isinstance(results, list) or len(results) != BATCH_SIZE:
        raise ValueError("RESULT_COUNT_MISMATCH")

    expected_targets = batch04_targets()
    adjudications: list[dict[str, Any]] = []

    for raw, (target_day, candidate_reason) in zip(
        results, expected_targets, strict=True
    ):
        if not isinstance(raw, dict):
            raise ValueError("RESULT_NOT_OBJECT")
        records, dom_record = _validate_result_envelope(
            raw, target_day, candidate_reason
        )
        network_record = records[0] if records else None

        if network_record is not None:
            try:
                record_start = _utc_from_ms(network_record["start"])
            except (KeyError, TypeError, ValueError, OverflowError):
                record_start = None
            if record_start is not None and record_start.date() != target_day:
                verdict = _overlap_blocked_verdict(
                    target_day=target_day,
                    candidate_reason=candidate_reason,
                    network_record=network_record,
                    dom_record=dom_record,
                    provenance=provenance,
                )
            else:
                evidence = RecoveryEvidence(
                    target_date=target_day,
                    candidate_reason=candidate_reason,
                    requested_date=target_day,
                    instrument_id=str(raw["instrument_id_observed"]),
                    instrument_name=str(raw["instrument_name"]),
                    network_record=network_record,
                    raw_payload_present=True,
                    dom_available=dom_record is not None,
                    dom_record=dom_record,
                    workflow_run=provenance["workflow_run"],
                    artifact_id=provenance["artifact_id"],
                    artifact_sha256=provenance["artifact_sha256"],
                    probe_commit=provenance["probe_commit"],
                )
                verdict = validate_positive_recovery_against_frozen_batch(
                    evidence, expected_targets
                )
        else:
            evidence = RecoveryEvidence(
                target_date=target_day,
                candidate_reason=candidate_reason,
                requested_date=target_day,
                instrument_id=str(raw["instrument_id_observed"]),
                instrument_name=str(raw["instrument_name"]),
                network_record=None,
                raw_payload_present=True,
                dom_available=dom_record is not None,
                dom_record=dom_record,
                workflow_run=provenance["workflow_run"],
                artifact_id=provenance["artifact_id"],
                artifact_sha256=provenance["artifact_sha256"],
                probe_commit=provenance["probe_commit"],
            )
            verdict = validate_positive_recovery_against_frozen_batch(
                evidence, expected_targets
            )

        verdict["capture_verdict"] = raw.get("capture_verdict")
        verdict["broker_record_id"] = (
            network_record.get("id") if network_record else None
        )
        verdict["broker_reason"] = (
            network_record.get("reason") if network_record else None
        )
        if "dom_witness_present" not in verdict:
            verdict["dom_witness_present"] = dom_record is not None
        adjudications.append(verdict)

    pass_count = sum(item.get("verdict") == "PASS" for item in adjudications)
    blocked_count = sum(item.get("verdict") == "BLOCKED" for item in adjudications)
    fail_count = sum(item.get("verdict") == "FAIL" for item in adjudications)
    overall = "PASS" if fail_count == 0 else "FAIL"
    return {
        "schema": "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH04_ADJUDICATION_V1",
        "batch_contract": BATCH_CONTRACT,
        "parent_protocol": RECOVERY_PROTOCOL,
        "verdict": overall,
        "reason": (
            "BATCH04_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_CROSS_DATE_PROMOTION"
            if overall == "PASS"
            else "BATCH04_ADJUDICATION_CONTAINS_FAIL"
        ),
        "attempted": BATCH_SIZE,
        "pass": pass_count,
        "blocked": blocked_count,
        "fail": fail_count,
        "provenance": provenance,
        "adjudications": adjudications,
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# HISTORICAL TRADING BREAKS RECOVERY — BATCH 04 QUALIFICATION",
        "",
        f"**{report['verdict']} — `{report['reason']}`**",
        "",
        "## Authoritative runtime provenance",
        "",
        f"- workflow run: `{EXPECTED_RUN}`",
        f"- job: `{EXPECTED_JOB}`",
        f"- probe commit: `{EXPECTED_PROBE_COMMIT}`",
        f"- artifact: `{EXPECTED_ARTIFACT}`",
        f"- artifact SHA-256: `{EXPECTED_ARTIFACT_SHA256}`",
        "- instrument: `USATECH.IDX/USD` / `9016`",
        "- replay scope: immutable frozen Batch 04 membership",
        "",
        "## Independent date-level adjudication",
        "",
    ]
    for item, (day, candidate_reason) in zip(
        report["adjudications"], batch04_targets(), strict=True
    ):
        lines += [
            f"### {day.isoformat()} — {candidate_reason}",
            "",
            f"**{item['verdict']} — `{item['reason']}`**",
            "",
        ]
        if item["verdict"] == "PASS":
            lines += [
                f"- broker record: `{item['broker_record_id']}`",
                f"- broker reason: `{item['broker_reason']}`",
                f"- start: `{item['break_start_utc']}`",
                f"- final closed minute: `{item['final_closed_minute_utc']}`",
                f"- calibrated reopen: `{item['reopen_utc']}`",
                f"- fully closed UTC hours: `{','.join(map(str, item['fully_closed_hours_utc']))}`",
                f"- exact DOM witness present: `{item['dom_witness_present']}`",
                "",
            ]
        elif item["reason"] == "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE":
            lines += [
                f"- overlapping broker record: `{item['overlap_record_id']}`",
                f"- broker reason: `{item['overlap_record_reason']}`",
                f"- overlap starts: `{item['overlap_start_utc']}`",
                f"- overlap final closed minute: `{item['overlap_final_closed_minute_utc']}`",
                "- the record starts on another date and cannot be promoted as exact-target evidence",
                "- this remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`",
                "",
            ]
        else:
            lines += [
                "No admissible exact positive broker record was recovered for this target date.",
                "This remains unresolved/BLOCKED and MUST NOT populate `NO_SPECIAL_CHANGE_EVIDENCE`.",
                "",
            ]

    lines += [
        "## Batch accounting",
        "",
        f"- attempted: `{report['attempted']}`",
        f"- PASS: `{report['pass']}`",
        f"- BLOCKED: `{report['blocked']}`",
        f"- FAIL: `{report['fail']}`",
        "",
        "Only genuine exact-target PASS dates are eligible for later executable calendar integration.",
        "Cross-date overlaps remain BLOCKED and unresolved.",
        "No absence or overlap is negative evidence.",
        "",
        "No `.bi5` acquisition and no real backtest are authorized by this qualification.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    report = adjudicate_runtime(runtime)
    ADJUDICATION_JSON.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    QUALIFICATION_MD.write_text(_render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if report["verdict"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
