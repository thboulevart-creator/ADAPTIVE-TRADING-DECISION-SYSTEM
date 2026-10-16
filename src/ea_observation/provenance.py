"""Synthetic source/observation identity binding; no assertion of real authenticity."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from .schema import is_sha256

# Only observations whose raw synthetic records expose these source values may
# be described as OBSERVED_DIRECT. All fields listed for a tag are mandatory.
SOURCE_VALUE_FIELDS = {
    "ORDER": ("native_order_id", "order_state", "source_seq",
              "timestamp_raw", "timestamp_utc"),
    "DEAL": ("native_deal_id", "native_order_id", "native_position_id", "symbol",
             "side", "entry_type", "volume", "price", "profit", "commission",
             "swap", "fee", "source_seq", "timestamp_raw", "timestamp_utc"),
    "CASH_FLOW": ("cash_flow_kind", "amount", "source_seq",
                  "timestamp_raw", "timestamp_utc"),
    "POSITION_SNAPSHOT": ("native_position_id", "symbol", "side", "volume",
                          "floating_pnl", "timestamp_raw", "timestamp_utc"),
    "ACCOUNT_SNAPSHOT": ("balance", "equity", "margin_used", "margin_free",
                         "account_currency", "timestamp_raw", "timestamp_utc"),
    "CONTEXT": ("available_at_utc", "decision_at_utc", "use_for_decision"),
}
ALL_BOUND_FIELDS = frozenset(
    field for fields in SOURCE_VALUE_FIELDS.values() for field in fields
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def sha256_records(raw_records: list[dict]) -> str:
    return hashlib.sha256(canonical_bytes(raw_records)).hexdigest()


def time_utc(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt if dt.tzinfo is not None else None
    except (ValueError, OverflowError):
        return None


def source_index(batch: dict) -> tuple[dict, list[str]]:
    """Index immutable synthetic values against their canonical manifest hash."""
    indexed: dict[str, dict] = {}
    issues: list[str] = []
    for source in batch.get("source_manifest", []):
        if not isinstance(source, dict):
            issues.append("INVALID_RAW_SOURCE")
            continue
        sid = source.get("source_id")
        if not isinstance(sid, str) or not sid or sid in indexed:
            issues.append("DUPLICATE_OR_INVALID_SOURCE_ID")
            continue
        if source.get("kind") != "SYNTHETIC" or source.get("synthetic") is not True:
            issues.append("REAL_SOURCE_IN_SYNTHETIC_SCOPE")
        raw = source.get("raw_records")
        if not isinstance(raw, list) or not all(isinstance(x, dict) for x in raw):
            issues.append("INVALID_RAW_RECORDS")
            continue
        if type(source.get("record_count")) is not int or source["record_count"] != len(raw):
            issues.append("RAW_RECORD_COUNT_MISMATCH")
        if not is_sha256(source.get("sha256")) or source["sha256"] != sha256_records(raw):
            issues.append("RAW_SOURCE_HASH_MISMATCH")
        raw_map: dict[str, dict] = {}
        for item in raw:
            ref = item.get("ref")
            if not isinstance(ref, str) or not ref or ref in raw_map:
                issues.append("INVALID_RAW_REFERENCE_UNIQUENESS")
            else:
                raw_map[ref] = item
        completeness = source.get("completeness")
        needed = ("orders", "deals", "positions", "account", "market")
        if (not isinstance(completeness, dict)
                or any(completeness.get(k) not in {"COMPLETE", "PARTIAL", "UNKNOWN"}
                       for k in needed)):
            issues.append("INVALID_SOURCE_COMPLETENESS")
        indexed[sid] = {"row": source, "raw_refs": set(raw_map), "raw_map": raw_map}
    return indexed, issues


def record_tag(row: dict) -> str:
    """Only known D1 observation classes can consume raw source records."""
    event_type = row.get("event_type")
    if event_type is not None:
        return event_type if isinstance(event_type, str) else ""
    if "native_position_id" in row:
        return "POSITION_SNAPSHOT"
    if "balance" in row:
        return "ACCOUNT_SNAPSHOT"
    if "context_id" in row:
        return "CONTEXT"
    return ""


def provenance_check(row: dict, sources: dict) -> list[str]:
    issues: list[str] = []
    sid, ref = row.get("source_id"), row.get("source_record_ref")
    if not isinstance(sid, str) or not isinstance(ref, str):
        return ["INVALID_INPUT"]
    src = sources.get(sid)
    if src is None:
        return ["UNKNOWN_EVENT_SOURCE"]
    raw = src["raw_map"].get(ref)
    if raw is None:
        return ["UNBOUND_SOURCE_RECORD"]
    tag = record_tag(row)
    if raw.get("tag") != tag or tag not in SOURCE_VALUE_FIELDS:
        issues.append("SOURCE_RECORD_TYPE_MISMATCH")
    if row.get("observation_class", "OBSERVED_DIRECT") == "OBSERVED_DIRECT":
        values = raw.get("values")
        required = SOURCE_VALUE_FIELDS.get(tag, ())
        if not isinstance(values, dict) or any(k not in values for k in required):
            issues.append("SOURCE_VALUES_MISSING")
        else:
            keys_to_check = (set(row) & ALL_BOUND_FIELDS) | set(required)
            if any(k not in values or row.get(k) != values[k] for k in keys_to_check):
                issues.append("SOURCE_VALUE_MISMATCH")
    elif row.get("observation_class") == "DERIVED_DETERMINISTIC":
        # The declared rule is not an executable, independently qualified rule.
        derivation = row.get("derivation")
        if not isinstance(derivation, dict) or not all(
            isinstance(derivation.get(k), str) and derivation[k]
            for k in ("rule_id", "source_record_ref", "output_field")
        ) or derivation.get("source_record_ref") != ref:
            issues.append("UNBOUND_DERIVATION_RULE")
        issues.append("DERIVATION_RULE_UNQUALIFIED")
    return issues
