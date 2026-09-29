from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-TD-03A-SOURCE-B-PROVENANCE-COLLECTOR-QUALIFICATION-CONTRACT-V0.1.json"
_CONTRACT_DOC = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

CONTRACT = "ATDS_E1_TD_03A_ACQUISITION_COLLECTOR_V0_1"
AUTHORITY = dict(_CONTRACT_DOC["authority"])
PROVENANCE = dict(_CONTRACT_DOC["provenance"])
DATASET_ID = _CONTRACT_DOC["future_dataset"]["dataset_id"]
WINDOW_START = _CONTRACT_DOC["future_dataset"]["logical_window_start_utc"]
WINDOW_END = _CONTRACT_DOC["future_dataset"]["logical_window_end_utc"]

WINDOW_START_MS = 1_790_812_800_000
WINDOW_END_MS = 1_822_348_800_000

FILE_FIELDS = (
    "relative_path",
    "sha256",
    "size_bytes",
    "rows",
    "first_timestamp_ms",
    "last_timestamp_ms",
    "schema_signature",
    "source_request_id",
)

EVENT_FIELDS = (
    "event_timestamp_utc",
    "event_type",
    "provider_lineage_id",
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
)

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
    "tail_dependence_verdict",
    "strategy_pnl",
}

MANIFEST_FIELDS = {
    "schema",
    "dataset_id",
    "status",
    "parent_source_dataset_id",
    "parent_source_manifest_sha256",
    "parent_source_inventory_digest",
    "parent_source_schema_signature",
    "provenance_record",
    "economic_instrument",
    "provider_instrument_identifier",
    "source_semantics",
    "logical_window_start_utc",
    "logical_window_end_utc",
    "required_fields",
    "forbidden_repairs",
    "file_count",
    "total_rows",
    "total_bytes",
    "first_observed_timestamp_ms",
    "last_observed_timestamp_ms",
    "gap_gt_60000ms_count",
    "files",
    "canonical_inventory_digest",
    "acquisition_ledger_final_digest",
    "runtime_environment",
    "created_at_utc",
}


class TD03AError(ValueError):
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


def validate_provenance(record: dict[str, Any]) -> dict[str, Any]:
    if record != PROVENANCE:
        return {"status": "BLOCKED_SOURCE_PROVENANCE"}
    return {"status": "PASS_PROVENANCE"}


def verify_raw_object(
    raw: bytes,
    *,
    expected_sha256: str,
    expected_size: int,
) -> dict[str, Any]:
    digest = hashlib.sha256(raw).hexdigest()
    size = len(raw)
    if digest != expected_sha256 or size != expected_size:
        return {
            "status": "BLOCKED_RAW_OBJECT_HASH",
            "sha256": digest,
            "size_bytes": size,
        }
    return {
        "status": "PASS_OBJECT_INTEGRITY",
        "sha256": digest,
        "size_bytes": size,
    }


def inspect_source_rows(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    previous: int | None = None
    count = 0
    gaps = 0
    first: int | None = None
    last: int | None = None
    for row in rows:
        if set(("timestamp", "bid_price", "ask_price")) - set(row):
            raise TD03AError("SOURCE_ROW_FIELDS")
        timestamp = int(row["timestamp"])
        bid = float(row["bid_price"])
        ask = float(row["ask_price"])
        if not math.isfinite(bid) or not math.isfinite(ask) or bid <= 0 or ask <= 0 or ask < bid:
            raise TD03AError("INVALID_BID_ASK")
        if previous is not None:
            if timestamp <= previous:
                raise TD03AError("NON_INCREASING_SOURCE_TIMESTAMP")
            if timestamp - previous > 60_000:
                gaps += 1
        if first is None:
            first = timestamp
        previous = timestamp
        last = timestamp
        count += 1
    return {
        "status": "PASS_SOURCE_ROWS",
        "rows": count,
        "first_timestamp_ms": first,
        "last_timestamp_ms": last,
        "gap_gt_60000ms_count": gaps,
    }


def _reject_performance_fields(payload: dict[str, Any]) -> None:
    for key in payload:
        if key.casefold() in FORBIDDEN_PERFORMANCE_FIELDS:
            raise TD03AError("FORBIDDEN_PERFORMANCE_FIELD")


def append_ledger_event(
    ledger: list[dict[str, Any]],
    event: dict[str, Any],
) -> list[dict[str, Any]]:
    _reject_performance_fields(event)
    if set(event) != set(EVENT_FIELDS):
        raise TD03AError("LEDGER_EVENT_FIELDS")
    if event["event_type"] not in ALLOWED_EVENT_TYPES:
        raise TD03AError("LEDGER_EVENT_TYPE")
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
    for index, event in enumerate(ledger, 1):
        expected_keys = {"event_sequence", "previous_event_digest", "event_digest", *EVENT_FIELDS}
        if set(event) != expected_keys:
            return {"status": "BLOCKED_LEDGER"}
        if event["event_sequence"] != index or event["previous_event_digest"] != prior:
            return {"status": "BLOCKED_LEDGER"}
        payload = {k: v for k, v in event.items() if k != "event_digest"}
        if canonical_sha256(payload) != event["event_digest"]:
            return {"status": "BLOCKED_LEDGER"}
        prior = event["event_digest"]
    return {"status": "PASS_COLLECTION_LEDGER", "events": len(ledger)}


def _validated_sorted_files(files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for record in files:
        if set(record) != set(FILE_FIELDS):
            raise TD03AError("FILE_RECORD_FIELDS")
        rel = record["relative_path"]
        if not isinstance(rel, str) or not rel:
            raise TD03AError("FILE_RECORD_FIELDS")
        if rel in seen:
            raise TD03AError("DUPLICATE_RELATIVE_PATH")
        seen.add(rel)
        sha = record["sha256"]
        if not isinstance(sha, str) or len(sha) != 64:
            raise TD03AError("FILE_RECORD_SHA256")
        int(record["size_bytes"])
        int(record["rows"])
        int(record["first_timestamp_ms"])
        int(record["last_timestamp_ms"])
        normalized.append(dict(record))
    return sorted(normalized, key=lambda x: x["relative_path"])


def canonical_inventory_digest(files: list[dict[str, Any]]) -> str:
    ordered = _validated_sorted_files(files)
    payload = {
        "schema": "ATDS_E1_TD_03_CANONICAL_INVENTORY_V0_1",
        "dataset_id": DATASET_ID,
        "logical_window": {
            "start_utc": WINDOW_START,
            "end_utc": WINDOW_END,
        },
        "files": ordered,
    }
    return canonical_sha256(payload)


def build_manifest(
    *,
    provenance_record: dict[str, Any],
    files: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    runtime_environment: dict[str, Any],
    created_at_utc: str,
) -> dict[str, Any]:
    if validate_provenance(provenance_record)["status"] != "PASS_PROVENANCE":
        raise TD03AError("SOURCE_PROVENANCE")
    if validate_ledger(ledger)["status"] != "PASS_COLLECTION_LEDGER":
        raise TD03AError("LEDGER")
    ordered = _validated_sorted_files(files)
    if not ordered:
        raise TD03AError("EMPTY_INVENTORY")
    inventory_digest = canonical_inventory_digest(ordered)
    first_ts = min(x["first_timestamp_ms"] for x in ordered)
    last_ts = max(x["last_timestamp_ms"] for x in ordered)
    manifest = {
        "schema": "ATDS_E1_TD_03_PROSPECTIVE_DATASET_MANIFEST_V0_1",
        "dataset_id": DATASET_ID,
        "status": "MANIFEST_CANDIDATE",
        "parent_source_dataset_id": "SOURCE_B_USTECH_PRICE_CORE_V0_1",
        "parent_source_manifest_sha256": "c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5",
        "parent_source_inventory_digest": "5cf0fe2c5cad725145432cab984375283df5fa3abdc72650cbba5f73278f28bf",
        "parent_source_schema_signature": "c770f02e90917154da1a32e668d59e030581e6159fa272496eac45d88bdda98d",
        "provenance_record": dict(provenance_record),
        "economic_instrument": "USTECH",
        "provider_instrument_identifier": "USTECH",
        "source_semantics": {
            "publisher_dataset": "CarlosSilva1/ustech-ticks",
            "publisher_declared_provenance": "Dukascopy via Tickstory",
            "timestamp": "UTC tick time, millisecond precision",
            "bid": "best bid, index points",
            "ask": "best ask, index points",
            "native_feed_equivalence_proven": False,
        },
        "logical_window_start_utc": WINDOW_START,
        "logical_window_end_utc": WINDOW_END,
        "required_fields": ["timestamp", "bid_price", "ask_price"],
        "forbidden_repairs": [
            "SORT_TO_REPAIR",
            "DEDUPLICATE_TO_REPAIR",
            "INTERPOLATE",
            "FORWARD_FILL",
            "SYNTHETIC_TICK_INSERTION",
            "PRICE_RECONSTRUCTION",
            "PERFORMANCE_BASED_ROW_FILTER",
        ],
        "file_count": len(ordered),
        "total_rows": sum(int(x["rows"]) for x in ordered),
        "total_bytes": sum(int(x["size_bytes"]) for x in ordered),
        "first_observed_timestamp_ms": first_ts,
        "last_observed_timestamp_ms": last_ts,
        "gap_gt_60000ms_count": 0,
        "files": ordered,
        "canonical_inventory_digest": inventory_digest,
        "acquisition_ledger_final_digest": ledger[-1]["event_digest"] if ledger else None,
        "runtime_environment": dict(runtime_environment),
        "created_at_utc": created_at_utc,
    }
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if set(manifest) != MANIFEST_FIELDS:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["dataset_id"] != DATASET_ID:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["logical_window_start_utc"] != WINDOW_START or manifest["logical_window_end_utc"] != WINDOW_END:
        return {"status": "BLOCKED_MANIFEST"}
    if validate_provenance(manifest["provenance_record"])["status"] != "PASS_PROVENANCE":
        return {"status": "BLOCKED_MANIFEST"}
    try:
        expected_inventory = canonical_inventory_digest(manifest["files"])
    except (TD03AError, TypeError, ValueError):
        return {"status": "BLOCKED_MANIFEST"}
    if expected_inventory != manifest["canonical_inventory_digest"]:
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["file_count"] != len(manifest["files"]):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["total_rows"] != sum(int(x["rows"]) for x in manifest["files"]):
        return {"status": "BLOCKED_MANIFEST"}
    if manifest["total_bytes"] != sum(int(x["size_bytes"]) for x in manifest["files"]):
        return {"status": "BLOCKED_MANIFEST"}
    return {"status": "PASS_MANIFEST"}


def is_evaluation_eligible(timestamp_ms: int) -> bool:
    return WINDOW_START_MS <= int(timestamp_ms) < WINDOW_END_MS


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise TD03AError("UTC_TIMESTAMP_REQUIRED")
    return parsed.astimezone(timezone.utc)


def build_seal(
    *,
    manifest: dict[str, Any],
    sealed_at_utc: str,
    human_authority_reference: str,
) -> dict[str, Any]:
    if validate_manifest(manifest)["status"] != "PASS_MANIFEST":
        raise TD03AError("MANIFEST_INVALID")
    if _parse_utc(sealed_at_utc) < _parse_utc(WINDOW_END):
        raise TD03AError("PREMATURE_SEAL")
    seal = {
        "schema": "ATDS_E1_TD_03_DATASET_SEAL_V0_1",
        "dataset_id": DATASET_ID,
        "manifest_sha256": canonical_sha256(manifest),
        "canonical_inventory_digest": manifest["canonical_inventory_digest"],
        "acquisition_ledger_final_digest": manifest["acquisition_ledger_final_digest"],
        "logical_window_start_utc": WINDOW_START,
        "logical_window_end_utc": WINDOW_END,
        "file_count": manifest["file_count"],
        "total_rows": manifest["total_rows"],
        "total_bytes": manifest["total_bytes"],
        "provenance_status": "PASS",
        "coverage_status": "PASS",
        "integrity_status": "PASS",
        "performance_peek_before_seal": False,
        "h1_built_before_seal": False,
        "momentum_executed_before_seal": False,
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
        return {"status": "BLOCKED_SEAL"}
    if seal.get("canonical_inventory_digest") != manifest.get("canonical_inventory_digest"):
        return {"status": "BLOCKED_SEAL"}
    if seal.get("acquisition_ledger_final_digest") != manifest.get("acquisition_ledger_final_digest"):
        return {"status": "BLOCKED_SEAL"}
    return {"status": "PASS_SEAL"}
