from __future__ import annotations

import json
import re
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from tools.trading_breaks_recovery_progression import load_attempt_ledger, latest_attempt_for_date
from tools.trading_breaks_recovery_protocol import derive_fully_closed_hours_utc, derive_interval

CONTRACT = "TRADING_BREAKS_TARGET_DAY_OVERLAP_ATTRIBUTION_V1"
QUALIFIED_PROOF_CAPABILITY = "QUALIFIED_CROSS_DATE_INTERVAL_ATTRIBUTION"
ADDRESSES_BLOCKER = "NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE"
TARGET_INSTRUMENT_NAME = "USATECH.IDX/USD"
TARGET_INSTRUMENT_ID = "9016"
ROOT = Path(__file__).resolve().parents[1]
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")

CLASS_A_SOURCES: tuple[tuple[date, str, int], ...] = (
    (date(2021, 12, 24), "CHRISTMAS_OBSERVED", 2),
    (date(2022, 4, 15), "GOOD_FRIDAY", 2),
    (date(2022, 12, 26), "CHRISTMAS_OBSERVED", 4),
    (date(2023, 1, 2), "NEW_YEARS_OBSERVED", 4),
    (date(2023, 7, 4), "INDEPENDENCE_DAY_OBSERVED", 6),
    (date(2023, 12, 25), "CHRISTMAS_OBSERVED", 7),
    (date(2024, 1, 1), "NEW_YEARS_OBSERVED", 7),
    (date(2024, 3, 29), "GOOD_FRIDAY", 8),
    (date(2024, 12, 25), "CHRISTMAS_OBSERVED", 9),
    (date(2025, 1, 1), "NEW_YEARS_OBSERVED", 10),
    (date(2025, 4, 18), "GOOD_FRIDAY", 10),
    (date(2025, 12, 25), "CHRISTMAS_OBSERVED", 12),
    (date(2026, 1, 1), "NEW_YEARS_OBSERVED", 13),
    (date(2026, 4, 3), "GOOD_FRIDAY", 13),
)


def runtime_path(batch: int) -> Path:
    return ROOT / "reports" / "data-qualification" / f"historical_trading_breaks_recovery_batch{batch:02d}_runtime.json"


def _epoch_ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def _iso_z(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def _parse_dom_line(line: str) -> dict[str, Any]:
    parts = [part.strip() for part in line.split("\t")]
    if len(parts) != 4:
        raise ValueError("DOM_WITNESS_SHAPE_INVALID")
    instrument_name, start_raw, end_raw, reason = parts
    if instrument_name != TARGET_INSTRUMENT_NAME:
        raise ValueError("DOM_WITNESS_INSTRUMENT_NAME_MISMATCH")
    start = datetime.strptime(start_raw, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    end = datetime.strptime(end_raw, "%d-%b-%y %H:%M:%S").replace(tzinfo=timezone.utc)
    return {"instrument": TARGET_INSTRUMENT_ID, "start": _epoch_ms(start), "end": _epoch_ms(end), "reason": reason}


def _dom_matches(dom: dict[str, Any], record: dict[str, Any]) -> bool:
    try:
        return (
            str(dom["instrument"]) == str(record["instrument"])
            and int(dom["start"]) == int(record["start"])
            and int(dom["end"]) == int(record["end"])
            and str(dom.get("reason", "")).strip() == str(record.get("reason", "")).strip()
        )
    except (KeyError, TypeError, ValueError):
        return False


def validate_target_day_overlap_result(
    raw: dict[str, Any],
    target_day: date,
    candidate_reason: str,
    provenance: dict[str, Any],
) -> dict[str, Any]:
    """Validate target-day facts from one broker-native interval, without exact-start-date bias."""
    if raw.get("target_date") != target_day.isoformat() or raw.get("requested_date") != target_day.isoformat():
        return {"verdict": "FAIL", "reason": "TARGET_OR_REQUESTED_DATE_MISMATCH"}
    if raw.get("candidate_reason") != candidate_reason:
        return {"verdict": "FAIL", "reason": "CANDIDATE_REASON_MISMATCH"}
    target_start = datetime(target_day.year, target_day.month, target_day.day, tzinfo=timezone.utc)
    target_end = target_start + timedelta(days=1)
    if raw.get("target_epoch_ms") != _epoch_ms(target_start):
        return {"verdict": "FAIL", "reason": "TARGET_EPOCH_MISMATCH"}
    if raw.get("instrument_name") != TARGET_INSTRUMENT_NAME:
        return {"verdict": "FAIL", "reason": "WRONG_INSTRUMENT_NAME"}
    if raw.get("instrument_id_expected") != TARGET_INSTRUMENT_ID or raw.get("instrument_id_observed") != TARGET_INSTRUMENT_ID:
        return {"verdict": "FAIL", "reason": "WRONG_INSTRUMENT_ID"}
    if raw.get("date_honored") is not True:
        return {"verdict": "FAIL", "reason": "REQUESTED_DATE_NOT_HONORED"}
    if raw.get("raw_payload_present") is not True:
        return {"verdict": "BLOCKED", "reason": "RAW_BROKER_PAYLOAD_NOT_RETAINED"}
    if raw.get("runtime_errors"):
        return {"verdict": "FAIL", "reason": "RUNTIME_ERRORS_PRESENT"}
    if raw.get("capture_verdict") == "FAIL":
        return {"verdict": "FAIL", "reason": "CAPTURE_LAYER_FAIL_REQUIRES_REMEDIATION"}

    records = raw.get("matching_records")
    if not isinstance(records, list):
        return {"verdict": "FAIL", "reason": "MATCHING_RECORDS_NOT_LIST"}
    if not records:
        return {"verdict": "BLOCKED", "reason": "NO_POSITIVE_BROKER_RECORD_RECOVERED"}
    if len(records) != 1:
        return {"verdict": "FAIL", "reason": "MULTIPLE_MATCHING_RECORDS_AMBIGUOUS"}
    record = records[0]
    if str(record.get("instrument")) != TARGET_INSTRUMENT_ID:
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_WRONG_INSTRUMENT"}
    if not str(record.get("reason", "")).strip():
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_REASON_MISSING"}

    try:
        start, end, reopen = derive_interval(record)
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"verdict": "FAIL", "reason": "MALFORMED_NETWORK_INTERVAL"}
    if not (start < target_end and reopen > target_start):
        return {"verdict": "FAIL", "reason": "BROKER_INTERVAL_DOES_NOT_OVERLAP_TARGET_DAY"}

    expected_hours = sorted(derive_fully_closed_hours_utc(target_day, start, reopen))
    if not expected_hours:
        return {"verdict": "BLOCKED", "reason": "NO_WHOLE_TARGET_DAY_CLOSED_HOUR_PROVEN"}
    if record.get("start_utc") != _iso_z(start):
        return {"verdict": "FAIL", "reason": "DERIVED_START_MISMATCH"}
    if record.get("end_last_closed_minute_utc") != _iso_z(end):
        return {"verdict": "FAIL", "reason": "DERIVED_END_MISMATCH"}
    if record.get("derived_reopen_utc") != _iso_z(reopen):
        return {"verdict": "FAIL", "reason": "DERIVED_REOPEN_MISMATCH"}
    if record.get("fully_closed_hours_utc") != expected_hours:
        return {"verdict": "FAIL", "reason": "TARGET_DAY_CLOSED_HOURS_MISMATCH"}

    dom_lines = raw.get("dom_witness_lines")
    if not isinstance(dom_lines, list):
        return {"verdict": "FAIL", "reason": "DOM_WITNESS_LINES_NOT_LIST"}
    if len(dom_lines) > 1:
        return {"verdict": "FAIL", "reason": "MULTIPLE_DOM_WITNESSES_AMBIGUOUS"}
    dom_status = "UNAVAILABLE"
    if dom_lines:
        try:
            dom = _parse_dom_line(dom_lines[0])
        except (ValueError, TypeError):
            return {"verdict": "FAIL", "reason": "MALFORMED_DOM_WITNESS"}
        if not _dom_matches(dom, record):
            return {"verdict": "FAIL", "reason": "DOM_NETWORK_CONTRADICTION"}
        dom_status = "CONCORDANT"

    for key in ("workflow_run", "job_id", "artifact_id"):
        value = provenance.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            return {"verdict": "BLOCKED", "reason": f"PROVENANCE_{key.upper()}_INVALID"}
    artifact_hash = provenance.get("artifact_sha256")
    probe_commit = provenance.get("probe_commit")
    if not isinstance(artifact_hash, str) or not _SHA256_RE.fullmatch(artifact_hash):
        return {"verdict": "BLOCKED", "reason": "ARTIFACT_SHA256_INVALID"}
    if not isinstance(probe_commit, str) or not _COMMIT_RE.fullmatch(probe_commit):
        return {"verdict": "BLOCKED", "reason": "PROBE_COMMIT_INVALID"}

    return {
        "schema": CONTRACT,
        "verdict": "PASS",
        "reason": "TARGET_DAY_OVERLAP_PRIMARY_BROKER_INTERVAL_VALIDATED",
        "target_date": target_day.isoformat(),
        "candidate_reason": candidate_reason,
        "record_id": str(record.get("id")),
        "record_start_utc": _iso_z(start),
        "record_end_last_closed_minute_utc": _iso_z(end),
        "reopen_utc": _iso_z(reopen),
        "fully_closed_hours_utc": expected_hours,
        "cross_date": start.date() != target_day,
        "dom_crosscheck": dom_status,
        "workflow_run": provenance["workflow_run"],
        "job_id": provenance["job_id"],
        "artifact_id": provenance["artifact_id"],
        "artifact_sha256": artifact_hash,
        "probe_commit": probe_commit,
    }


def load_class_a_evidence() -> list[tuple[date, str, dict[str, Any], dict[str, Any], int]]:
    loaded: list[tuple[date, str, dict[str, Any], dict[str, Any], int]] = []
    cache: dict[int, dict[str, Any]] = {}
    _, _, attempts = load_attempt_ledger()
    for target_day, reason, batch in CLASS_A_SOURCES:
        runtime = cache.setdefault(batch, json.loads(runtime_path(batch).read_text(encoding="utf-8")))
        matches = [item for item in runtime.get("results", []) if item.get("target_date") == target_day.isoformat()]
        if len(matches) != 1:
            raise ValueError(f"CLASS_A_RUNTIME_RESULT_CARDINALITY:{target_day}")
        provenance = runtime.get("provenance")
        if not isinstance(provenance, dict):
            raise ValueError(f"CLASS_A_RUNTIME_PROVENANCE_MISSING:{target_day}")
        latest = latest_attempt_for_date(target_day, attempts)
        if latest is None or latest.blocking_reason != ADDRESSES_BLOCKER:
            raise ValueError(f"CLASS_A_LEDGER_BLOCKER_MISMATCH:{target_day}")
        expected_provenance = {
            "workflow_run": latest.provenance["workflow_run"],
            "job_id": latest.provenance["job_id"],
            "artifact_id": latest.provenance["artifact_id"],
            "artifact_sha256": latest.provenance["artifact_sha256"],
            "probe_commit": latest.provenance["probe_commit"],
        }
        if any(provenance.get(key) != value for key, value in expected_provenance.items()):
            raise ValueError(f"CLASS_A_RUNTIME_LEDGER_PROVENANCE_MISMATCH:{target_day}")
        loaded.append((target_day, reason, deepcopy(matches[0]), deepcopy(provenance), batch))
    return loaded


def qualify_class_a() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for target_day, reason, raw, provenance, batch in load_class_a_evidence():
        verdict = validate_target_day_overlap_result(raw, target_day, reason, provenance)
        if verdict.get("verdict") != "PASS":
            raise ValueError(f"CLASS_A_SEMANTIC_QUALIFICATION_FAILED:{target_day}:{verdict}")
        if verdict.get("cross_date") is not True:
            raise ValueError(f"CLASS_A_NOT_CROSS_DATE:{target_day}")
        verdict["source_batch"] = batch
        results.append(verdict)
    return {
        "schema": CONTRACT,
        "verdict": "PASS",
        "reason": "ALL_CLASS_A_CROSS_DATE_INTERVALS_SUPPORT_TARGET_DAY_FACTS",
        "qualified_proof_capability": QUALIFIED_PROOF_CAPABILITY,
        "addresses_blocking_reason": ADDRESSES_BLOCKER,
        "class_a_count": len(results),
        "results": results,
    }


def main() -> int:
    print(json.dumps(qualify_class_a(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
