from __future__ import annotations

import math
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from src.smf_ap1_m03_binding import (
    BindingBlocked,
    COMPANION_ID,
    execute_m03_observations,
    validate_activation,
)

CONTRACT = "ATDS_SMF_AP1_M03_COMPANION_V0_1"
NY = ZoneInfo("America/New_York")

REQUIRED_FIELDS = (
    "minute_start_ms_utc",
    "tick_count",
    "mid_high",
    "mid_low",
    "spread_mean",
)

def _finite(value) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise BindingBlocked("NONFINITE_COMPANION_RECORD")
    return float(value)

def record_to_observations(record):
    if not isinstance(record, dict):
        raise BindingBlocked("COMPANION_RECORD_INVALID")
    for key in REQUIRED_FIELDS:
        if key not in record:
            raise BindingBlocked("COMPANION_RECORD_FIELD_MISSING:" + key)
    minute_ms = record["minute_start_ms_utc"]
    tick_count = record["tick_count"]
    if isinstance(minute_ms, bool) or not isinstance(minute_ms, int):
        raise BindingBlocked("MINUTE_START_INVALID")
    if isinstance(tick_count, bool) or not isinstance(tick_count, int) or tick_count <= 0:
        raise BindingBlocked("TICK_COUNT_INVALID")
    high = _finite(record["mid_high"])
    low = _finite(record["mid_low"])
    spread = _finite(record["spread_mean"])
    if high < low:
        raise BindingBlocked("MID_RANGE_INVALID")
    return {
        "minute_start_ms_utc": minute_ms,
        "tick_count": float(tick_count),
        "minute_range": high - low,
        "spread_mean": spread,
    }

def bucket_keys_for_minute(minute_start_ms_utc: int):
    if isinstance(minute_start_ms_utc, bool) or not isinstance(minute_start_ms_utc, int):
        raise BindingBlocked("MINUTE_START_INVALID")
    utc_dt = datetime.fromtimestamp(minute_start_ms_utc / 1000, tz=timezone.utc)
    ny_dt = utc_dt.astimezone(NY)
    return (
        "GLOBAL",
        f"UTC_HOUR:{utc_dt.hour:02d}",
        f"NEW_YORK_HOUR:{ny_dt.hour:02d}",
        f"NEW_YORK_WEEKDAY:{ny_dt.weekday()}",
        f"NEW_YORK_WEEKDAY_HOUR:{ny_dt.weekday()}:{ny_dt.hour:02d}",
        f"UTC_YEAR:{utc_dt.year}",
    )

def build_companion_evidence(records, *, activation):
    validate_activation(activation)
    if not isinstance(records, (list, tuple)) or not records:
        raise BindingBlocked("EMPTY_COMPANION_RECORD_SET")
    buckets = {}
    for raw in records:
        obs = record_to_observations(raw)
        for bucket_id in bucket_keys_for_minute(obs["minute_start_ms_utc"]):
            bucket = buckets.setdefault(bucket_id, {"tick_count": [], "minute_range": [], "spread_mean": []})
            bucket["tick_count"].append(obs["tick_count"])
            bucket["minute_range"].append(obs["minute_range"])
            bucket["spread_mean"].append(obs["spread_mean"])
    evidence = {}
    for bucket_id in sorted(buckets):
        evidence[bucket_id] = {}
        for metric in ("tick_count", "minute_range", "spread_mean"):
            evidence[bucket_id][metric] = execute_m03_observations(
                buckets[bucket_id][metric],
                metric=metric,
                bucket_id=bucket_id,
                activation=activation,
            )
    return {
        "schema": CONTRACT,
        "status": "SYNTHETIC_OR_FUTURE_ADMITTED_RECORD_EVIDENCE_COMPLETE",
        "companion_id": COMPANION_ID,
        "bucket_evidence": evidence,
        "real_workspace_materialized": False,
        "authority": {"scientific": False, "operational": False, "trading": False, "capital": False},
    }

def main() -> int:
    print("BLOCKED_REAL_EXECUTION_WORKSPACE_NOT_MATERIALIZED")
    print("This companion exposes only in-memory binding capability. G05 remains separately governed.")
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
