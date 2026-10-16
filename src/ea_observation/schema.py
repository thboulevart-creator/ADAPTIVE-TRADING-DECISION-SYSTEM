"""Static V0.1 synthetic observation schema; standard library only."""
from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Mapping

SCHEMA_VERSION = "ATDS_EA_OBSERVATION_V0_1"
COLLECTIONS = (
    "ea_registry", "run_manifest", "source_manifest", "trade_events",
    "position_snapshots", "account_snapshots", "market_context_refs",
)
REQUIRED = {
    "ea_registry": ("ea_id", "binary_sha256", "config_sha256", "ownership"),
    "run_manifest": ("run_id", "ea_id", "source_id", "mode", "account_scope",
                     "position_mode", "account_currency", "market_symbol",
                     "ea_isolated", "attested_binding", "equity_coverage"),
    "source_manifest": ("source_id", "kind", "synthetic", "sha256",
                        "record_count", "raw_records", "completeness"),
    "trade_events": ("event_id", "run_id", "source_id", "source_record_ref",
                     "source_seq", "event_type", "timestamp_raw",
                     "timestamp_utc", "time_precision", "timezone_status",
                     "observation_class", "ea_attribution"),
    "position_snapshots": ("snapshot_id", "run_id", "source_id", "source_record_ref",
                           "timestamp_raw", "timestamp_utc", "time_precision",
                           "timezone_status", "native_position_id", "symbol",
                           "side", "volume", "floating_pnl", "attribution"),
    "account_snapshots": ("snapshot_id", "run_id", "source_id", "source_record_ref",
                          "timestamp_raw", "timestamp_utc", "time_precision",
                          "timezone_status", "balance", "equity",
                          "margin_used", "margin_free", "account_currency"),
    "market_context_refs": ("context_id", "run_id", "source_id",
                            "source_record_ref", "available_at_utc",
                            "decision_at_utc", "use_for_decision"),
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
OBS_CLASSES = {"OBSERVED_DIRECT", "DERIVED_DETERMINISTIC", "INFERRED_HYPOTHESIS", "UNKNOWN"}
ATTR = {"EXACT", "AMBIGUOUS", "UNASSIGNED"}
SOURCE_KINDS = {"SYNTHETIC"}
CLAIMS = {"DESCRIPTIVE", "EA_NET_PNL", "PORTFOLIO_NET_PNL", "EXACT_DRAWDOWN", "TRADING_AUTHORIZATION", "EXACT_EA_RISK"}
MONEY_FIELDS = {"volume", "price", "profit", "commission", "swap", "fee",
                "balance", "equity", "margin_used", "margin_free", "floating_pnl",
                "conversion_rate", "margin_level", "contract_size", "tick_size",
                "tick_value", "volume_step"}
TIME_PRECISION = {"SECONDS", "MILLISECONDS", "MICROSECONDS", "UNKNOWN"}
TIMEZONE_STATUS = {"KNOWN_OFFSET", "UNKNOWN"}
SOURCE_COMPLETENESS = {"COMPLETE", "PARTIAL", "UNKNOWN"}


def exact_decimal(value: object) -> bool:
    """Reject binary floats, NaN/Infinity and implicit zero conversions."""
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        number = Decimal(value)
    except (InvalidOperation, ValueError):
        return False
    return number.is_finite()


def is_sha256(value: object) -> bool:
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def validate_shape(batch: object) -> list[str]:
    issues: list[str] = []
    if not isinstance(batch, dict):
        return ["INVALID_TOP_LEVEL"]
    allowed = {"schema_version", "batch_id", "synthetic", "authority", "requested_claim", *COLLECTIONS}
    if set(batch) - allowed:
        issues.append("UNKNOWN_TOP_LEVEL_FIELD")
    if batch.get("schema_version") != SCHEMA_VERSION:
        issues.append("INVALID_SCHEMA_VERSION")
    if not isinstance(batch.get("batch_id"), str) or not batch["batch_id"]:
        issues.append("INVALID_BATCH_ID")
    if batch.get("synthetic") is not True:
        issues.append("NON_SYNTHETIC_BATCH_FORBIDDEN")
    authority = batch.get("authority")
    if authority != {"trading": False, "capital": False, "real_data": False}:
        issues.append("AUTHORITY_NOT_FAIL_CLOSED")
    if batch.get("requested_claim", "DESCRIPTIVE") not in CLAIMS:
        issues.append("UNKNOWN_CLAIM")
    for collection in COLLECTIONS:
        records = batch.get(collection)
        if not isinstance(records, list):
            issues.append("MISSING_COLLECTION:" + collection)
            continue
        for row in records:
            if not isinstance(row, dict):
                issues.append("NON_OBJECT_RECORD:" + collection)
                continue
            for key in REQUIRED[collection]:
                if key not in row:
                    issues.append("MISSING_FIELD:" + collection + "." + key)
    return issues
