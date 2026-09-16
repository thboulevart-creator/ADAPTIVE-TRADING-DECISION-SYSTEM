from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Sequence

from tools.dukascopy_usatech_calendar import SPECIAL_SESSION_EVIDENCE
from tools.dukascopy_usatech_calendar_coverage import (
    NO_SPECIAL_CHANGE_EVIDENCE,
    candidate_special_dates,
)


CONTRACT = "HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL_V1"
WINDOW_START = date(2021, 8, 14)
WINDOW_END = date(2026, 8, 14)
TARGET_INSTRUMENT_ID = "9016"
TARGET_INSTRUMENT_NAME = "USATECH.IDX/USD"
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")


@dataclass(frozen=True)
class RecoveryEvidence:
    target_date: date
    candidate_reason: str
    requested_date: date
    instrument_id: str
    instrument_name: str
    network_record: dict[str, Any] | None
    raw_payload_present: bool
    dom_available: bool
    dom_record: dict[str, Any] | None
    workflow_run: int | None
    artifact_id: int | None
    artifact_sha256: str | None
    probe_commit: str | None


def recovery_queue() -> list[tuple[date, str]]:
    """Return the governed unresolved in-window candidates in date order."""
    resolved = set(SPECIAL_SESSION_EVIDENCE) | set(NO_SPECIAL_CHANGE_EVIDENCE)
    return [
        (item.day, item.reason)
        for item in candidate_special_dates(WINDOW_START, WINDOW_END)
        if item.day not in resolved
    ]


def _epoch_ms(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("boolean is not an epoch")
    return int(value)


def _utc_from_ms(value: Any) -> datetime:
    return datetime.fromtimestamp(_epoch_ms(value) / 1000, tz=timezone.utc)


def derive_interval(record: dict[str, Any]) -> tuple[datetime, datetime, datetime]:
    """Return start, final closed minute, and calibrated reopen instant."""
    start = _utc_from_ms(record["start"])
    end = _utc_from_ms(record["end"])
    if end < start:
        raise ValueError("negative interval")
    reopen = end + timedelta(seconds=60)
    return start, end, reopen


def derive_fully_closed_hours_utc(
    target_date: date,
    start: datetime,
    reopen: datetime,
) -> frozenset[int]:
    """Emit only whole UTC hours fully contained in the closed interval."""
    closed: set[int] = set()
    for hour in range(24):
        hour_start = datetime(
            target_date.year,
            target_date.month,
            target_date.day,
            hour,
            tzinfo=timezone.utc,
        )
        hour_end = hour_start + timedelta(hours=1)
        if hour_start >= start and hour_end <= reopen:
            closed.add(hour)
    return frozenset(closed)


def _dom_matches_network(dom: dict[str, Any], network: dict[str, Any]) -> bool:
    required = ("instrument", "start", "end")
    if any(key not in dom for key in required):
        return False
    if str(dom["instrument"]) != str(network.get("instrument")):
        return False
    if _epoch_ms(dom["start"]) != _epoch_ms(network.get("start")):
        return False
    if _epoch_ms(dom["end"]) != _epoch_ms(network.get("end")):
        return False
    dom_reason = str(dom.get("reason", "")).strip()
    network_reason = str(network.get("reason", "")).strip()
    if dom_reason and network_reason and dom_reason != network_reason:
        return False
    return True


def _validate_positive_recovery_in_scope(
    evidence: RecoveryEvidence,
    allowed_targets: dict[date, str],
    *,
    missing_target_reason: str,
) -> dict[str, Any]:
    """Validate evidence against an already-qualified target scope.

    This function validates evidence semantics only. It does not mutate or widen the
    live recovery queue. Callers are responsible for supplying either the current
    unresolved queue or an immutable historical batch membership.
    """
    if not (WINDOW_START <= evidence.target_date <= WINDOW_END):
        return {"verdict": "FAIL", "reason": "TARGET_OUTSIDE_FROZEN_WINDOW"}
    if evidence.target_date not in allowed_targets:
        return {"verdict": "FAIL", "reason": missing_target_reason}
    if evidence.candidate_reason != allowed_targets[evidence.target_date]:
        return {"verdict": "FAIL", "reason": "CANDIDATE_REASON_MISMATCH"}
    if evidence.requested_date != evidence.target_date:
        return {"verdict": "FAIL", "reason": "REQUESTED_DATE_MISMATCH"}
    if evidence.instrument_id != TARGET_INSTRUMENT_ID:
        return {"verdict": "FAIL", "reason": "WRONG_INSTRUMENT_ID"}
    if evidence.instrument_name != TARGET_INSTRUMENT_NAME:
        return {"verdict": "FAIL", "reason": "WRONG_INSTRUMENT_NAME"}

    if evidence.network_record is None:
        return {"verdict": "BLOCKED", "reason": "NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED"}
    if not evidence.raw_payload_present:
        return {"verdict": "BLOCKED", "reason": "RAW_BROKER_PAYLOAD_NOT_RETAINED"}

    record = evidence.network_record
    if str(record.get("instrument")) != TARGET_INSTRUMENT_ID:
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_WRONG_INSTRUMENT"}
    if not str(record.get("reason", "")).strip():
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_REASON_MISSING"}

    try:
        start, end, reopen = derive_interval(record)
    except (KeyError, TypeError, ValueError, OverflowError):
        return {"verdict": "FAIL", "reason": "MALFORMED_NETWORK_INTERVAL"}

    if start.date() != evidence.target_date:
        return {"verdict": "FAIL", "reason": "NETWORK_RECORD_DATE_MISMATCH"}

    if evidence.dom_available:
        if evidence.dom_record is None:
            return {"verdict": "BLOCKED", "reason": "EXPECTED_DOM_CROSSCHECK_MISSING"}
        try:
            if not _dom_matches_network(evidence.dom_record, record):
                return {"verdict": "FAIL", "reason": "DOM_NETWORK_CONTRADICTION"}
        except (TypeError, ValueError, OverflowError):
            return {"verdict": "FAIL", "reason": "MALFORMED_DOM_RECORD"}

    if not evidence.workflow_run or evidence.workflow_run <= 0:
        return {"verdict": "BLOCKED", "reason": "WORKFLOW_PROVENANCE_MISSING"}
    if not evidence.artifact_id or evidence.artifact_id <= 0:
        return {"verdict": "BLOCKED", "reason": "ARTIFACT_ID_MISSING"}
    if not evidence.artifact_sha256 or not _SHA256_RE.fullmatch(evidence.artifact_sha256):
        return {"verdict": "BLOCKED", "reason": "ARTIFACT_SHA256_INVALID"}
    if not evidence.probe_commit or not _COMMIT_RE.fullmatch(evidence.probe_commit):
        return {"verdict": "BLOCKED", "reason": "PROBE_COMMIT_INVALID"}

    fully_closed = derive_fully_closed_hours_utc(evidence.target_date, start, reopen)

    return {
        "schema": CONTRACT,
        "verdict": "PASS",
        "reason": "EXACT_PRIMARY_BROKER_POSITIVE_BREAK_RECORD_VALIDATED",
        "target_date": evidence.target_date.isoformat(),
        "candidate_reason": evidence.candidate_reason,
        "instrument": TARGET_INSTRUMENT_NAME,
        "instrument_id": TARGET_INSTRUMENT_ID,
        "break_start_utc": start.isoformat().replace("+00:00", "Z"),
        "final_closed_minute_utc": end.isoformat().replace("+00:00", "Z"),
        "reopen_utc": reopen.isoformat().replace("+00:00", "Z"),
        "fully_closed_hours_utc": sorted(fully_closed),
        "workflow_run": evidence.workflow_run,
        "artifact_id": evidence.artifact_id,
        "artifact_sha256": evidence.artifact_sha256.lower(),
        "probe_commit": evidence.probe_commit.lower(),
    }


def validate_positive_recovery(evidence: RecoveryEvidence) -> dict[str, Any]:
    """Validate one currently-unresolved date. Resolved dates cannot re-enter."""
    return _validate_positive_recovery_in_scope(
        evidence,
        dict(recovery_queue()),
        missing_target_reason="TARGET_NOT_IN_GOVERNED_RECOVERY_QUEUE",
    )


def validate_positive_recovery_against_frozen_batch(
    evidence: RecoveryEvidence,
    frozen_targets: Sequence[tuple[date, str]],
) -> dict[str, Any]:
    """Replay evidence against immutable historical batch membership.

    This is an adjudication/reproducibility interface only. It never changes the
    current recovery queue and does not make a resolved date execution-eligible.
    """
    if not frozen_targets:
        return {"verdict": "FAIL", "reason": "FROZEN_SCOPE_EMPTY"}

    normalized: list[tuple[date, str]] = []
    for item in frozen_targets:
        if (
            not isinstance(item, tuple)
            or len(item) != 2
            or not isinstance(item[0], date)
            or not isinstance(item[1], str)
            or not item[1].strip()
        ):
            return {"verdict": "FAIL", "reason": "FROZEN_SCOPE_MALFORMED"}
        normalized.append((item[0], item[1]))

    days = [day for day, _ in normalized]
    if len(days) != len(set(days)):
        return {"verdict": "FAIL", "reason": "FROZEN_SCOPE_DUPLICATE_TARGET"}
    if days != sorted(days):
        return {"verdict": "FAIL", "reason": "FROZEN_SCOPE_NOT_CHRONOLOGICAL"}

    return _validate_positive_recovery_in_scope(
        evidence,
        dict(normalized),
        missing_target_reason="TARGET_NOT_IN_FROZEN_BATCH_SCOPE",
    )
