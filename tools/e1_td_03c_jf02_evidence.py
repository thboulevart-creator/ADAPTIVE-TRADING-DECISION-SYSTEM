from __future__ import annotations

import csv
import hashlib
import io
import json
from dataclasses import dataclass
from typing import Any

from tools.ao_e0_b12_data01_fc01_jf01 import CSV_HEADER

CONTROL_ID = "E1-TD-03C-JF02"
PROVIDER = "DUKASCOPY_BANK_SA"
TRANSPORT = "JFOREX_SDK_IHISTORY_READTICKS"
ATDS_INSTRUMENT = "USATECH.IDX-USD"
JFOREX_INSTRUMENT = "USATECH.IDX/USD"
INTERVAL_START_UTC = "2025-10-01T14:00:00.000Z"
INTERVAL_END_EXCLUSIVE_UTC = "2025-10-01T15:00:00.000Z"
FROM_MS = 1759327200000
TO_MS_INCLUSIVE = 1759330799999
ENVIRONMENT = "DEMO"
CANONICAL_ADAPTER = "DUKASCOPY_JFOREX_CANONICAL_TICK_ADAPTER_V0_1"


class JF02Blocked(RuntimeError):
    pass


FROZEN_REQUEST: dict[str, Any] = {
    "schema": "ATDS_E1_TD_03C_JF02_FROZEN_REQUEST_V0_1",
    "control_id": CONTROL_ID,
    "provider": PROVIDER,
    "transport": TRANSPORT,
    "environment": ENVIRONMENT,
    "instrument_atds": ATDS_INSTRUMENT,
    "instrument_jforex": JFOREX_INSTRUMENT,
    "interval_semantics": "[START,END_EXCLUSIVE)",
    "interval_start_utc": INTERVAL_START_UTC,
    "interval_end_exclusive_utc": INTERVAL_END_EXCLUSIVE_UTC,
    "jforex_from_ms": FROM_MS,
    "jforex_to_ms_inclusive": TO_MS_INCLUSIVE,
    "automatic_request_retries": 0,
    "sorting": False,
    "deduplication": False,
    "repair": False,
    "canonical_adapter": CANONICAL_ADAPTER,
}


def request_manifest_bytes() -> bytes:
    return (json.dumps(FROZEN_REQUEST, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def payload_sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def evidence_identity_sha256(payload: bytes) -> str:
    h = hashlib.sha256()
    h.update(request_manifest_bytes())
    h.update(b"\x00")
    h.update(payload)
    return h.hexdigest()


@dataclass(frozen=True)
class PayloadSummary:
    tick_count: int
    first_timestamp: str
    last_timestamp: str
    payload_sha256: str
    evidence_identity_sha256: str


def summarize_payload(payload: bytes) -> PayloadSummary:
    if payload.startswith(b"\xef\xbb\xbf"):
        raise JF02Blocked("BLOCKED_JF02_BOM")
    if b"\r\n" in payload or b"\r" in payload:
        raise JF02Blocked("BLOCKED_JF02_LINE_ENDING")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise JF02Blocked("BLOCKED_JF02_ENCODING") from exc
    if not text.startswith(CSV_HEADER):
        raise JF02Blocked("BLOCKED_JF02_SCHEMA_DRIFT")

    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise JF02Blocked("BLOCKED_JF02_EMPTY_RESPONSE")
    required = ["timestamp", "askPrice", "bidPrice", "askVolume", "bidVolume"]
    if list(rows[0].keys()) != required:
        raise JF02Blocked("BLOCKED_JF02_SCHEMA_DRIFT")

    timestamps = [r["timestamp"] for r in rows]
    if any(not t for t in timestamps):
        raise JF02Blocked("BLOCKED_JF02_SCHEMA_DRIFT")
    if timestamps != sorted(timestamps):
        raise JF02Blocked("BLOCKED_JF02_SOURCE_ORDERING")

    return PayloadSummary(
        tick_count=len(rows),
        first_timestamp=timestamps[0],
        last_timestamp=timestamps[-1],
        payload_sha256=payload_sha256(payload),
        evidence_identity_sha256=evidence_identity_sha256(payload),
    )


def compare_repeat_reads(payload_a: bytes, payload_b: bytes) -> dict[str, Any]:
    a = summarize_payload(payload_a)
    b = summarize_payload(payload_b)
    byte_identical = payload_a == payload_b
    result = {
        "payload_sha256_a": a.payload_sha256,
        "payload_sha256_b": b.payload_sha256,
        "evidence_identity_sha256_a": a.evidence_identity_sha256,
        "evidence_identity_sha256_b": b.evidence_identity_sha256,
        "tick_count_a": a.tick_count,
        "tick_count_b": b.tick_count,
        "first_timestamp_a": a.first_timestamp,
        "first_timestamp_b": b.first_timestamp,
        "last_timestamp_a": a.last_timestamp,
        "last_timestamp_b": b.last_timestamp,
        "byte_identical": byte_identical,
    }
    if not byte_identical:
        raise JF02Blocked("BLOCKED_JF02_REPEAT_RESPONSE_MISMATCH")
    return result


def build_receipt(payload: bytes, *, api_version: str, run_label: str, acquisition_started_utc: str, acquisition_finished_utc: str) -> dict[str, Any]:
    if not api_version.strip():
        raise JF02Blocked("BLOCKED_JF02_API_VERSION_UNBOUND")
    if run_label not in {"READ_A", "READ_B"}:
        raise JF02Blocked("BLOCKED_JF02_RUN_LABEL")
    summary = summarize_payload(payload)
    return {
        "schema": "ATDS_E1_TD_03C_JF02_JFOREX_HISTORY_RECEIPT_V0_1",
        "control_id": CONTROL_ID,
        "run_label": run_label,
        "provider": PROVIDER,
        "transport": TRANSPORT,
        "environment": ENVIRONMENT,
        "api_version": api_version,
        "request": FROZEN_REQUEST,
        "tick_count": summary.tick_count,
        "first_timestamp": summary.first_timestamp,
        "last_timestamp": summary.last_timestamp,
        "payload_sha256": summary.payload_sha256,
        "evidence_identity_sha256": summary.evidence_identity_sha256,
        "acquisition_started_utc": acquisition_started_utc,
        "acquisition_finished_utc": acquisition_finished_utc,
        "raw_provider_object_claim": False,
        "source_b_equivalence_claim": False,
    }
