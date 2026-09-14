from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_batch03 import (
    BATCH_CONTRACT,
    BATCH_SIZE,
    CURRENT_CAPABILITY_FINGERPRINT,
    CURRENT_CAPABILITY_ID,
    PARENT_PROGRESSION_CONTRACT,
    SELECTION_RULE,
    batch03_targets,
)
from tools.trading_breaks_recovery_protocol import (
    CONTRACT as RECOVERY_PROTOCOL,
    RecoveryEvidence,
    validate_positive_recovery,
)


REPO = Path(__file__).resolve().parents[1]
RUNTIME_PATH = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch03_runtime.json"
ADJUDICATION_JSON = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch03_adjudication.json"
QUALIFICATION_MD = REPO / "reports" / "data-qualification" / "historical_trading_breaks_recovery_batch03_qualification.md"

EXPECTED_RUN = 34892253133
EXPECTED_JOB = 104137558818
EXPECTED_ARTIFACT = 10367930592
EXPECTED_ARTIFACT_SHA256 = "994d0f4832400c05bd8fc46e07637e9b68590af1c4b37816ae0cbf650c04bd41"
EXPECTED_PROBE_COMMIT = "9b8b6342aea83d3ffbafa2ec6aebfe9abfaf4db4"


def _epoch_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _parse_dom_line(
    line: str,
    *,
    expected_instrument_name: str,
    expected_instrument_id: str,
) -> dict[str, Any]:
    parts = [part.strip() for part in line.split("\t")]
    if len(parts) != 4:
        raise ValueError("DOM_WITNESS_SHAPE_INVALID")
    instrument_name, start_raw, end_raw, reason = parts
    if instrument_name != expected_instrument_name:
        raise ValueError("DOM_WITNESS_INSTRUMENT_NAME_MISMATCH")
    start = datetime.strptime(start_raw, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    end = datetime.strptime(end_raw, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    return {
        "instrument": expected_instrument_id,
        "start": _epoch_ms(start),
        "end": _epoch_ms(end),
        "reason": reason,
    }


def _validate_runtime_identity(runtime: dict[str, Any]) -> dict[str, Any]:
    if runtime.get("schema") != BATCH_CONTRACT:
        raise ValueError("RUNTIME_SCHEMA_MISMATCH")
    if runtime.get("parent_protocol") != RECOVERY_PROTOCOL:
        raise ValueError("PARENT_PROTOCOL_MISMATCH")
    if runtime.get("parent_progression_contract") != PARENT_PROGRESSION_CONTRACT:
        raise ValueError("PARENT_PROGRESSION_MISMATCH")
    if runtime.get("batch_number") != 3 or runtime.get("batch_size") != BATCH_SIZE:
        raise ValueError("BATCH_IDENTITY_MISMATCH")
    if runtime.get("selection_rule") != SELECTION_RULE:
        raise ValueError("SELECTION_RULE_MISMATCH")
    if runtime.get("capability_id") != CURRENT_CAPABILITY_ID:
        raise ValueError("CAPABILITY_ID_MISMATCH")
    if runtime.get("capability_fingerprint") != CURRENT_CAPABILITY_FINGERPRINT:
        raise ValueError("CAPABILITY_FINGERPRINT_MISMATCH")
    expected_targets = [
        {"date": day.isoformat(), "reason": reason}
        for day, reason in batch03_targets()
    ]
    if runtime.get("targets") != expected_targets:
        raise ValueError("FROZEN_MEMBERSHIP_MISMATCH")
    if runtime.get("read_only") is not True or runtime.get("market_data_written") is not False:
        raise ValueError("RUNTIME_READ_ONLY_BOUNDARY_MISMATCH")

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
    if runtime.get("workflow_run") != str(EXPECTED_RUN):
        raise ValueError("RUNTIME_RUN_ID_MISMATCH")
    if runtime.get("probe_commit") != EXPECTED_PROBE_COMMIT:
        raise ValueError("RUNTIME_PROBE_COMMIT_MISMATCH")
    return provenance


def adjudicate_runtime(runtime: dict[str, Any]) -> dict[str, Any]:
    provenance = _validate_runtime_identity(runtime)
    results = runtime.get("results")
    if not isinstance(results, list) or len(results) != BATCH_SIZE:
        raise ValueError("RESULT_COUNT_MISMATCH")

    expected_targets = batch03_targets()
    adjudications: list[dict[str, Any]] = []
    for raw, (target_day, candidate_reason) in zip(results, expected_targets, strict=True):
        if raw.get("target_date") != target_day.isoformat():
            raise ValueError("RESULT_TARGET_ORDER_OR_IDENTITY_MISMATCH")
        if raw.get("candidate_reason") != candidate_reason:
            raise ValueError("RESULT_REASON_MISMATCH")
        if raw.get("requested_date") != target_day.isoformat():
            raise ValueError("RESULT_REQUESTED_DATE_MISMATCH")
        if raw.get("instrument_id_observed") != "9016":
            raise ValueError("RESULT_OBSERVED_INSTRUMENT_MISMATCH")
        if raw.get("instrument_name") != "USATECH.IDX/USD":
            raise ValueError("RESULT_INSTRUMENT_NAME_MISMATCH")
        if raw.get("runtime_errors"):
            raise ValueError("RESULT_RUNTIME_ERRORS_PRESENT")

        records = raw.get("matching_records")
        if not isinstance(records, list):
            raise ValueError("MATCHING_RECORDS_NOT_LIST")
        if len(records) > 1:
            raise ValueError("MULTIPLE_MATCHING_RECORDS_REQUIRE_SEPARATE_ADJUDICATION")
        network_record = records[0] if records else None

        dom_lines = raw.get("dom_witness_lines")
        if not isinstance(dom_lines, list):
            raise ValueError("DOM_WITNESS_LINES_NOT_LIST")
        if len(dom_lines) > 1:
            raise ValueError("MULTIPLE_DOM_WITNESSES_REQUIRE_SEPARATE_ADJUDICATION")
        dom_record = (
            _parse_dom_line(
                dom_lines[0],
                expected_instrument_name=str(raw["instrument_name"]),
                expected_instrument_id=str(raw["instrument_id_observed"]),
            )
            if dom_lines
            else None
        )

        evidence = RecoveryEvidence(
            target_date=target_day,
            candidate_reason=candidate_reason,
            requested_date=date.fromisoformat(raw["requested_date"]),
            instrument_id=str(raw.get("instrument_id_observed")),
            instrument_name=str(raw.get("instrument_name")),
            network_record=network_record,
            raw_payload_present=raw.get("raw_payload_present") is True,
            dom_available=dom_record is not None,
            dom_record=dom_record,
            workflow_run=provenance["workflow_run"],
            artifact_id=provenance["artifact_id"],
            artifact_sha256=provenance["artifact_sha256"],
            probe_commit=provenance["probe_commit"],
        )
        verdict = validate_positive_recovery(evidence)
        verdict["capture_verdict"] = raw.get("capture_verdict")
        verdict["broker_record_id"] = network_record.get("id") if network_record else None
        verdict["broker_reason"] = network_record.get("reason") if network_record else None
        verdict["dom_witness_present"] = dom_record is not None
        adjudications.append(verdict)

    pass_count = sum(item.get("verdict") == "PASS" for item in adjudications)
    blocked_count = sum(item.get("verdict") == "BLOCKED" for item in adjudications)
    fail_count = sum(item.get("verdict") == "FAIL" for item in adjudications)
    overall = "PASS" if fail_count == 0 else "FAIL"
    return {
        "schema": "HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH03_ADJUDICATION_V1",
        "batch_contract": BATCH_CONTRACT,
        "parent_protocol": RECOVERY_PROTOCOL,
        "verdict": overall,
        "reason": (
            "BATCH03_POSITIVE_RECORDS_INDEPENDENTLY_ADJUDICATED_WITH_NO_NEGATIVE_EVIDENCE_PROMOTION"
            if overall == "PASS"
            else "BATCH03_ADJUDICATION_CONTAINS_FAIL"
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
        "# HISTORICAL TRADING BREAKS RECOVERY — BATCH 03 QUALIFICATION",
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
        "",
        "## Independent date-level adjudication",
        "",
    ]
    for item, (day, candidate_reason) in zip(report["adjudications"], batch03_targets(), strict=True):
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
                "- exact DOM witness: present and protocol-matched",
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
        "Only PASS dates are authorized for executable calendar integration.",
        "BLOCKED dates remain unresolved; absence is not negative evidence.",
        "",
        "No `.bi5` acquisition and no real backtest are authorized by this qualification.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    runtime = json.loads(RUNTIME_PATH.read_text(encoding="utf-8"))
    report = adjudicate_runtime(runtime)
    ADJUDICATION_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    QUALIFICATION_MD.write_text(_render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if report["verdict"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
