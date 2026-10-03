from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-TD-03C-SOURCE-CONTINUITY-ASSURANCE-CONTRACT-V0.1.json"
_CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

CONTRACT = "ATDS_E1_TD_03C_SOURCE_CONTINUITY_ASSURANCE_V0_1"
WINDOW_START = "2026-10-01T00:00:00Z"
WINDOW_END = "2027-10-01T00:00:00Z"
SOURCE_B_DATASET_ID = "SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1"
INSURANCE_DATASET_ID = "DUKASCOPY_USATECH_PROSPECTIVE_INSURANCE_20261001_20271001_V0_1"

LANE_A_IDENTITY = {
    "lane_id": "LANE_A_SOURCE_B_TD01",
    "dataset_id": SOURCE_B_DATASET_ID,
    "publisher_dataset": "CarlosSilva1/ustech-ticks",
}
LANE_B_IDENTITY = {
    "lane_id": "LANE_B_DUKASCOPY_PROSPECTIVE_INSURANCE",
    "dataset_id": INSURANCE_DATASET_ID,
    "provider": "Dukascopy Bank SA",
    "instrument_id": "USATECH.IDX/USD",
}
FILE_FIELDS = {
    "lane_id",
    "dataset_id",
    "provider",
    "instrument_id",
    "relative_path",
    "sha256",
    "size_bytes",
    "rows",
    "first_timestamp_ms",
    "last_timestamp_ms",
    "schema_signature",
    "source_request_id",
}

EVENT_FIELDS = {
    "event_timestamp_utc",
    "event_type",
    "lane_id",
    "dataset_id",
    "provider",
    "instrument_id",
    "source_request_id",
    "requested_start_utc",
    "requested_end_utc",
    "object_relative_path",
    "object_sha256",
    "object_size_bytes",
    "parse_status",
    "row_count",
    "first_timestamp_ms",
    "last_timestamp_ms",
    "schema_signature",
    "event_status",
}
ALLOWED_EVENT_TYPES = {
    "ACQUISITION_REQUEST",
    "ACQUISITION_FAILURE",
    "OBJECT_RECEIVED",
    "OBJECT_ACCEPTED",
    "OBJECT_REJECTED",
    "SOURCE_REVISION_DETECTED",
    "FINAL_COVERAGE_CHECK",
}

FORBIDDEN_PERFORMANCE_FIELDS = {
    "signal",
    "position",
    "trade",
    "pnl",
    "expectancy",
    "drawdown",
    "win_rate",
    "largest_winner",
    "flip_fraction",
    "tail_dependence",
    "strategy_pnl",
    "strategy",
    "optimization",
}

MANIFEST_FIELDS = {
    "schema",
    "status",
    "lane_id",
    "dataset_id",
    "provider",
    "instrument_id",
    "source_equivalence_status",
    "logical_window_start_utc",
    "logical_window_end_utc",
    "file_count",
    "total_rows",
    "total_bytes",
    "first_observed_timestamp_ms",
    "last_observed_timestamp_ms",
    "files",
    "canonical_inventory_digest",
    "acquisition_ledger_final_digest",
    "runtime_environment",
    "created_at_utc",
}

class TD03CError(ValueError):
    pass


def canonical_json_bytes(payload: Any) -> bytes:
    return (
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
def validate_lane_b_binding(binding: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(binding, dict):
        return {"status": "BLOCKED_DATASET_IDENTITY"}
    if binding.get("dataset_id") == SOURCE_B_DATASET_ID:
        return {"status": "BLOCKED_DATASET_IDENTITY"}
    if binding.get("provider") != LANE_B_IDENTITY["provider"]:
        return {"status": "BLOCKED_PROVIDER_IDENTITY"}
    if binding.get("instrument_id") != LANE_B_IDENTITY["instrument_id"]:
        return {"status": "BLOCKED_INSTRUMENT_IDENTITY"}
    expected = {
        "lane_id": LANE_B_IDENTITY["lane_id"],
        "dataset_id": INSURANCE_DATASET_ID,
        "provider": LANE_B_IDENTITY["provider"],
        "instrument_id": LANE_B_IDENTITY["instrument_id"],
        "window_start_utc": WINDOW_START,
        "window_end_utc": WINDOW_END,
        "source_equivalence_status": "UNRESOLVED",
    }
    if binding != expected:
        return {"status": "BLOCKED_DATASET_IDENTITY"}
    return {"status": "PASS_LANE_B_BINDING"}


def _normalized_storage_path(value: str) -> str:
    normalized = os.path.normcase(os.path.normpath(str(value))).replace("\\", "/")
    return normalized.rstrip("/")
def validate_storage_separation(lane_a_path: str, lane_b_path: str) -> dict[str, Any]:
    a = _normalized_storage_path(lane_a_path)
    b = _normalized_storage_path(lane_b_path)
    if not a or not b:
        return {"status": "BLOCKED_CROSS_LANE_CONTAMINATION"}
    if a == b or b.startswith(a + "/") or a.startswith(b + "/"):
        return {"status": "BLOCKED_CROSS_LANE_CONTAMINATION"}
    return {"status": "PASS_STORAGE_SEPARATION"}


def validate_file_record(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict) or set(record) != FILE_FIELDS:
        return {"status": "BLOCKED_MANIFEST"}
    if record["lane_id"] != LANE_B_IDENTITY["lane_id"]:
        return {"status": "BLOCKED_CROSS_LANE_CONTAMINATION"}
    if record["dataset_id"] != INSURANCE_DATASET_ID:
        return {"status": "BLOCKED_CROSS_LANE_CONTAMINATION"}
    if record["provider"] != LANE_B_IDENTITY["provider"]:
        return {"status": "BLOCKED_PROVIDER_IDENTITY"}
    if record["instrument_id"] != LANE_B_IDENTITY["instrument_id"]:
        return {"status": "BLOCKED_INSTRUMENT_IDENTITY"}
    rel = record["relative_path"]
    sha = record["sha256"]
    if not isinstance(rel, str) or not rel or not isinstance(sha, str) or len(sha) != 64:
        return {"status": "BLOCKED_MANIFEST"}
    try:
        size = int(record["size_bytes"])
        rows = int(record["rows"])
        first = int(record["first_timestamp_ms"])
        last = int(record["last_timestamp_ms"])
    except (TypeError, ValueError, OverflowError):
        return {"status": "BLOCKED_MANIFEST"}
    if size < 0 or rows < 0 or first > last:
        return {"status": "BLOCKED_MANIFEST"}
    return {"status": "PASS_FILE_RECORD"}


def verify_raw_object(
    raw: bytes,
    *,
    expected_sha256: str,
    expected_size: int,
) -> dict[str, Any]:
    digest = hashlib.sha256(raw).hexdigest()
    size = len(raw)
    if digest != expected_sha256 or size != int(expected_size):
        return {
            "status": "BLOCKED_RAW_OBJECT_INTEGRITY",
            "sha256": digest,
            "size_bytes": size,
        }
    return {
        "status": "PASS_RAW_OBJECT_INTEGRITY",
        "sha256": digest,
        "size_bytes": size,
    }


def detect_source_revision(previous_sha256: str, observed_sha256: str) -> dict[str, Any]:
    if previous_sha256 != observed_sha256:
        return {"status": "BLOCKED_SOURCE_REVISION"}
    return {"status": "PASS_NO_SOURCE_REVISION"}


def inspect_interpreted_ticks(
    rows: Iterable[dict[str, Any]],
    semantics: dict[str, Any],
) -> dict[str, Any]:
    expected_semantics = {
        "timezone": "UTC",
        "timestamp_unit": "ms",
        "bid": "BID",
        "ask": "ASK",
    }
    if semantics != expected_semantics:
        return {"status": "BLOCKED_TIMESTAMP_SEMANTICS"}
    previous: int | None = None
    count = 0
    first: int | None = None
    last: int | None = None
    for row in rows:
        if not isinstance(row, dict):
            return {"status": "BLOCKED_BID_ASK_SEMANTICS"}
        if "bid_price" not in row or "ask_price" not in row:
            return {"status": "BLOCKED_BID_ASK_SEMANTICS"}
        if "timestamp" not in row:
            return {"status": "BLOCKED_TIMESTAMP_SEMANTICS"}
        try:
            ts = int(row["timestamp"])
            bid = float(row["bid_price"])
            ask = float(row["ask_price"])
        except (TypeError, ValueError, OverflowError):
            return {"status": "BLOCKED_BID_ASK_SEMANTICS"}
        if not math.isfinite(bid) or not math.isfinite(ask) or bid <= 0 or ask <= 0 or ask < bid:
            return {"status": "BLOCKED_BID_ASK_SEMANTICS"}
        if previous is not None and ts <= previous:
            return {"status": "BLOCKED_TIMESTAMP_INTEGRITY"}
        if first is None:
            first = ts
        previous = ts
        last = ts
        count += 1
    return {
        "status": "PASS_INTERPRETED_TICKS",
        "rows": count,
        "first_timestamp_ms": first,
        "last_timestamp_ms": last,
    }


def assess_bi5_decode_semantics(evidence: dict[str, Any]) -> dict[str, Any]:
    scale = evidence.get("raw_price_scale") if isinstance(evidence, dict) else None
    status = evidence.get("scale_evidence_status") if isinstance(evidence, dict) else None
    if scale is None or status == "UNRESOLVED":
        return {
            "status": "RAW_PRESERVATION_ONLY",
            "raw_preservation": "ALLOWED",
            "decoded_values": "BLOCKED_RAW_DECODE_SEMANTICS",
            "source_equivalence": "UNRESOLVED",
        }
    return {
        "status": "PASS_DECODE_SEMANTICS_WITHIN_DECLARED_EVIDENCE",
        "raw_preservation": "ALLOWED",
        "decoded_values": "ALLOWED_WITHIN_DECLARED_EVIDENCE",
        "source_equivalence": "UNRESOLVED",
    }


def _reject_performance_fields(payload: dict[str, Any]) -> None:
    for key in payload:
        if key.casefold() in FORBIDDEN_PERFORMANCE_FIELDS:
            raise TD03CError("BLOCKED_PERFORMANCE_PEEK")


def _validate_event_binding(event: dict[str, Any]) -> None:
    if event.get("lane_id") != LANE_B_IDENTITY["lane_id"]:
        raise TD03CError("BLOCKED_CROSS_LANE_CONTAMINATION")
    if event.get("dataset_id") != INSURANCE_DATASET_ID:
        raise TD03CError("BLOCKED_CROSS_LANE_CONTAMINATION")
    if event.get("provider") != LANE_B_IDENTITY["provider"]:
        raise TD03CError("BLOCKED_PROVIDER_IDENTITY")
    if event.get("instrument_id") != LANE_B_IDENTITY["instrument_id"]:
        raise TD03CError("BLOCKED_INSTRUMENT_IDENTITY")


def append_ledger_event(
    ledger: list[dict[str, Any]],
    event: dict[str, Any],
) -> list[dict[str, Any]]:
    if not isinstance(event, dict):
        raise TD03CError("BLOCKED_LEDGER")
    _reject_performance_fields(event)
    if set(event) != EVENT_FIELDS:
        raise TD03CError("BLOCKED_LEDGER")
    _validate_event_binding(event)
    if event["event_type"] not in ALLOWED_EVENT_TYPES:
        raise TD03CError("BLOCKED_LEDGER")
    out = [dict(x) for x in ledger]
    prior = out[-1]["event_digest"] if out else None
    body = {
        "event_sequence": len(out) + 1,
        "previous_event_digest": prior,
        **event,
    }
    body["event_digest"] = canonical_sha256(body)
    out.append(body)
    return out


def validate_ledger(ledger: list[dict[str, Any]]) -> dict[str, Any]:
    prior = None
    expected_keys = {
        "event_sequence",
        "previous_event_digest",
        "event_digest",
        *EVENT_FIELDS,
    }
    for index, event in enumerate(ledger, 1):
        if not isinstance(event, dict) or set(event) != expected_keys:
            return {"status": "BLOCKED_LEDGER"}
        try:
            _reject_performance_fields(event)
            _validate_event_binding(event)
        except TD03CError:
            return {"status": "BLOCKED_LEDGER"}
        if event["event_sequence"] != index:
            return {"status": "BLOCKED_LEDGER"}
        if event["previous_event_digest"] != prior:
            return {"status": "BLOCKED_LEDGER"}
        if event["event_type"] not in ALLOWED_EVENT_TYPES:
            return {"status": "BLOCKED_LEDGER"}
        body = {k: v for k, v in event.items() if k != "event_digest"}
        if canonical_sha256(body) != event["event_digest"]:
            return {"status": "BLOCKED_LEDGER"}
        prior = event["event_digest"]
    return {"status": "PASS_LEDGER", "events": len(ledger)}


def _validated_sorted_files(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in files:
        verdict = validate_file_record(record)
        if verdict["status"] != "PASS_FILE_RECORD":
            raise TD03CError(verdict["status"])
        rel = record["relative_path"]
        if rel in seen:
            raise TD03CError("BLOCKED_MANIFEST")
        seen.add(rel)
        out.append(dict(record))
    return sorted(out, key=lambda x: x["relative_path"])


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    ordered = _validated_sorted_files(files)
    payload = {
        "schema": "ATDS_E1_TD_03C_LANE_B_CANONICAL_INVENTORY_V0_1",
        "lane_id": LANE_B_IDENTITY["lane_id"],
        "dataset_id": INSURANCE_DATASET_ID,
        "logical_window": {
            "start_utc": WINDOW_START,
            "end_utc": WINDOW_END,
        },
        "files": ordered,
    }
    return canonical_sha256(payload)


def build_manifest(
    *,
    binding: dict[str, Any],
    files: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    runtime_environment: dict[str, Any],
    created_at_utc: str,
) -> dict[str, Any]:
    if validate_lane_b_binding(binding)["status"] != "PASS_LANE_B_BINDING":
        raise TD03CError("BLOCKED_DATASET_IDENTITY")
    if validate_ledger(ledger)["status"] != "PASS_LEDGER":
        raise TD03CError("BLOCKED_LEDGER")
    ordered = _validated_sorted_files(files)
    if not ordered:
        raise TD03CError("BLOCKED_MANIFEST")
    manifest = {
        "schema": "ATDS_E1_TD_03C_LANE_B_MANIFEST_V0_1",
        "status": "MANIFEST_CANDIDATE",
        "lane_id": LANE_B_IDENTITY["lane_id"],
        "dataset_id": INSURANCE_DATASET_ID,
        "provider": LANE_B_IDENTITY["provider"],
        "instrument_id": LANE_B_IDENTITY["instrument_id"],
        "source_equivalence_status": "UNRESOLVED",
        "logical_window_start_utc": WINDOW_START,
        "logical_window_end_utc": WINDOW_END,
        "file_count": len(ordered),
        "total_rows": sum(int(x["rows"]) for x in ordered),
        "total_bytes": sum(int(x["size_bytes"]) for x in ordered),
        "first_observed_timestamp_ms": min(int(x["first_timestamp_ms"]) for x in ordered),
        "last_observed_timestamp_ms": max(int(x["last_timestamp_ms"]) for x in ordered),
        "files": ordered,
        "canonical_inventory_digest": canonical_inventory_digest(ordered),
        "acquisition_ledger_final_digest": ledger[-1]["event_digest"] if ledger else None,
        "runtime_environment": dict(runtime_environment),
        "created_at_utc": created_at_utc,
    }
    return manifest
def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["lane_id"] != LANE_B_IDENTITY["lane_id"]:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["dataset_id"] != INSURANCE_DATASET_ID:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["provider"] != LANE_B_IDENTITY["provider"]:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["instrument_id"] != LANE_B_IDENTITY["instrument_id"]:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["source_equivalence_status"] != "UNRESOLVED":
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["logical_window_start_utc"] != WINDOW_START:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["logical_window_end_utc"] != WINDOW_END:
        return {"status": "BLOCKED_MANIFEST"}
    try:
        ordered = _validated_sorted_files(manifest["files"])
        inventory = canonical_inventory_digest(ordered)
    except (TD03CError, TypeError, ValueError):
        return {"status": "BLOCKED_MANIFEST"}
    if inventory != manifest["canonical_inventory_digest"]:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["file_count"] != len(ordered):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["total_rows"] != sum(int(x["rows"]) for x in ordered):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["total_bytes"] != sum(int(x["size_bytes"]) for x in ordered):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["first_observed_timestamp_ms"] != min(int(x["first_timestamp_ms"]) for x in ordered):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["last_observed_timestamp_ms"] != max(int(x["last_timestamp_ms"]) for x in ordered):
        return {"status": "BLOCKED_MANIFEST"}
    return {"status": "PASS_MANIFEST"}


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise TD03CError("UTC_TIMESTAMP_REQUIRED")
    return parsed.astimezone(timezone.utc)


def build_seal(
    *,
    manifest: dict[str, Any],
    sealed_at_utc: str,
    human_authority_reference: str,
) -> dict[str, Any]:
    if validate_manifest(manifest)["status"] != "PASS_MANIFEST":
        raise TD03CError("BLOCKED_MANIFEST")
    if _parse_utc(sealed_at_utc) < _parse_utc(WINDOW_END):
        raise TD03CError("BLOCKED_PREMATURE_SEAL")
    seal = {
        "schema": "ATDS_E1_TD_03C_LANE_B_SEAL_V0_1",
        "lane_id": LANE_B_IDENTITY["lane_id"],
        "dataset_id": INSURANCE_DATASET_ID,
        "manifest_sha256": canonical_sha256(manifest),
        "canonical_inventory_digest": manifest["canonical_inventory_digest"],
        "acquisition_ledger_final_digest": manifest["acquisition_ledger_final_digest"],
        "logical_window_start_utc": WINDOW_START,
        "logical_window_end_utc": WINDOW_END,
        "file_count": manifest["file_count"],
        "total_rows": manifest["total_rows"],
        "total_bytes": manifest["total_bytes"],
        "source_equivalence_status": "UNRESOLVED",
        "source_b_promotion": "NOT_AUTHORIZED",
        "performance_peek_before_seal": False,
        "h1_built_before_seal": False,
        "strategy_executed_before_seal": False,
        "pnl_observed_before_seal": False,
        "sealed_at_utc": sealed_at_utc,
        "human_authority_reference": human_authority_reference,
    }
    seal["canonical_digest"] = canonical_sha256(seal)
    return seal


def verify_seal(manifest: dict[str, Any], seal: dict[str, Any]) -> dict[str, Any]:
    if seal.get("manifest_sha256") != canonical_sha256(manifest):
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    body = {k: v for k, v in seal.items() if k != "canonical_digest"}
    if seal.get("canonical_digest") != canonical_sha256(body):
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    if seal.get("lane_id") != LANE_B_IDENTITY["lane_id"]:
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    if seal.get("dataset_id") != INSURANCE_DATASET_ID:
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    if seal.get("canonical_inventory_digest") != manifest.get("canonical_inventory_digest"):
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    if seal.get("acquisition_ledger_final_digest") != manifest.get("acquisition_ledger_final_digest"):
        return {"status": "BLOCKED_POST_SEAL_MUTATION"}
    return {"status": "PASS_SEAL"}


def assess_source_equivalence_claim(claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "BLOCKED_SOURCE_EQUIVALENCE",
        "source_equivalence_status": "UNRESOLVED",
        "required_future_frontier": "E1-TD-03D",
    }


def validate_source_b_promotion(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "BLOCKED_SOURCE_SUBSTITUTION",
        "source_b_promotion": "NOT_AUTHORIZED",
    }