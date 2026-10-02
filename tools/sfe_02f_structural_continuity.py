from __future__ import annotations

import hashlib
import importlib.resources as resources
import math
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from zoneinfo import TZPATH, ZoneInfo

import tzdata


CONTRACT = "ATDS_SFE_02F_STRUCTURAL_CONTINUITY_RUNTIME_V0_1"
HOUR_MS = 3_600_000
WARMUP_H1 = 20

ALLOWED_ROW_FIELDS = (
    "h1_start_ms_utc",
    "source_segment_id",
    "continuity_block_id",
    "continuity_ordinal",
    "mid_close",
)

ROW_LEVEL_UPSTREAM_CLASSIFICATION = "UNRESOLVED"

FROZEN_CALENDAR_IDENTITY = {
    "timezone_key": "America/New_York",
    "python_implementation": "cpython",
    "python_version": "3.13.14",
    "timezone_library": "stdlib.zoneinfo",
    "zoneinfo_tzpath_exact": [],
    "tzdata_package_version": "2026.3",
    "iana_tzdb_release": "2026c",
    "america_new_york_tzif_sha256": "d7f2206b3a45989fc9ad63d558922532fa7352280d5f87176bf1db79cb1d1fa9",
}

CANONICAL_DATASET_IDENTITY = {
    "dataset": "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",
    "canonical_stream_sha256": "15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f",
    "recorded_jsonl_sha256": "94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0",
    "rows": 27677,
    "continuity_blocks": 1436,
    "first_h1_start_ms_utc": 1621904400000,
    "last_h1_start_ms_utc": 1779660000000,
    "row_fields_exact": list(ALLOWED_ROW_FIELDS),
    "mismatch_status": "BLOCKED_DATASET_IDENTITY",
}

SOURCE_B_AGGREGATE_CONTEXT = {
    "SOURCE_B_GAPS_GT_60S": 1605,
    "REGULAR_SESSION_BOUNDARIES": 1290,
    "IN_REGULAR_SESSION_PRE_HOLIDAY_OVERLAY": 315,
    "DEMONSTRATED_HISTORICAL_ACQUISITION_LOSSES": 13,
    "HISTORICAL_UNKNOWN_GAPS": 9,
}

FORBIDDEN_OUTPUT_KEYS = {
    "signal",
    "strategy_signal",
    "strategy_event",
    "strategy_event_membership",
    "y",
    "theta",
    "ci",
    "pnl",
    "trade",
    "position",
    "execution",
    "return",
    "abs_return",
    "volatility",
    "zscore",
    "range",
    "atr",
    "optimization",
    "ranking",
    "router",
}

_FORBIDDEN_INPUT_KEYS = {
    "strategy",
    "signal",
    "strategy_signal",
    "strategy_event",
    "strategy_event_membership",
    "y",
    "Y",
    "theta",
    "ci",
    "CI",
    "pnl",
    "PnL",
    "trade",
    "position",
    "execution",
    "return",
    "abs_return",
    "volatility",
    "zscore",
    "range",
    "atr",
    "optimization",
    "ranking",
    "router",
    "source_b_classification",
    "source_b_label",
    "upstream_classification",
}


def _blocked(reason: str):
    return {"status": "BLOCKED", "reason": reason}


def _observed_calendar_identity():
    zone_path = resources.files("tzdata.zoneinfo").joinpath("America").joinpath("New_York")
    zone_bytes = zone_path.read_bytes()
    return {
        "timezone_key": "America/New_York",
        "python_implementation": sys.implementation.name,
        "python_version": ".".join(str(x) for x in sys.version_info[:3]),
        "timezone_library": "stdlib.zoneinfo",
        "zoneinfo_tzpath_exact": list(TZPATH),
        "tzdata_package_version": tzdata.__version__,
        "iana_tzdb_release": tzdata.IANA_VERSION,
        "america_new_york_tzif_sha256": hashlib.sha256(zone_bytes).hexdigest(),
    }


def verify_calendar_identity():
    try:
        observed = _observed_calendar_identity()
    except Exception:
        return _blocked("BLOCKED_CALENDAR_IDENTITY")
    if observed != FROZEN_CALENDAR_IDENTITY:
        return _blocked("BLOCKED_CALENDAR_IDENTITY")
    return {"status": "PASS", "identity": observed}


def verify_canonical_dataset_identity(identity):
    if not isinstance(identity, dict):
        return _blocked("BLOCKED_DATASET_IDENTITY")
    if identity != CANONICAL_DATASET_IDENTITY:
        return _blocked("BLOCKED_DATASET_IDENTITY")
    return {"status": "PASS"}


def _quantile_type7(values, p):
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    h = (len(ordered) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return float(ordered[lo])
    weight = h - lo
    return float(ordered[lo] + (ordered[hi] - ordered[lo]) * weight)


def _histogram(values):
    counts = Counter(values)
    return {str(k): counts[k] for k in sorted(counts)}


def _fraction(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


def _validate_row_schema_and_domain(rows):
    if not isinstance(rows, list) or not rows:
        return _blocked("BLOCKED_DATASET_IDENTITY")

    normalized = []
    allowed = set(ALLOWED_ROW_FIELDS)

    for row in rows:
        if not isinstance(row, dict):
            return _blocked("BLOCKED_DATASET_IDENTITY")

        keys = set(row)
        if keys & _FORBIDDEN_INPUT_KEYS:
            return _blocked("BLOCKED_FORBIDDEN_INPUT_SURFACE")
        if keys != allowed:
            return _blocked("BLOCKED_DATASET_IDENTITY")

        ts = row["h1_start_ms_utc"]
        source = row["source_segment_id"]
        block = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]
        mid_close = row["mid_close"]

        if isinstance(ts, bool) or not isinstance(ts, int):
            return _blocked("BLOCKED_DATASET_IDENTITY")
        if isinstance(source, bool) or not isinstance(source, (str, int)):
            return _blocked("BLOCKED_DATASET_IDENTITY")
        if isinstance(block, bool) or not isinstance(block, (str, int)):
            return _blocked("BLOCKED_DATASET_IDENTITY")
        if isinstance(ordinal, bool) or not isinstance(ordinal, int) or ordinal < 0:
            return _blocked("BLOCKED_CANONICAL_INTEGRITY")
        if isinstance(mid_close, bool) or not isinstance(mid_close, (int, float)):
            return _blocked("BLOCKED_DATASET_IDENTITY")
        mid = float(mid_close)
        if not math.isfinite(mid) or mid <= 0:
            return _blocked("BLOCKED_DATASET_IDENTITY")

        normalized.append(
            {
                "h1_start_ms_utc": ts,
                "source_segment_id": source,
                "continuity_block_id": block,
                "continuity_ordinal": ordinal,
            }
        )

    for previous, current in zip(normalized, normalized[1:]):
        if current["h1_start_ms_utc"] <= previous["h1_start_ms_utc"]:
            return _blocked("BLOCKED_DATASET_IDENTITY")

    return {"status": "PASS", "rows": normalized}


def _validate_continuity(rows):
    if rows[0]["continuity_ordinal"] != 0:
        return _blocked("BLOCKED_CANONICAL_INTEGRITY")

    seen_blocks = {rows[0]["continuity_block_id"]}
    boundaries = []

    for i, (previous, current) in enumerate(zip(rows, rows[1:])):
        source_change = current["source_segment_id"] != previous["source_segment_id"]
        time_gap = current["h1_start_ms_utc"] != previous["h1_start_ms_utc"] + HOUR_MS
        block_change = current["continuity_block_id"] != previous["continuity_block_id"]

        if not source_change and not time_gap:
            if block_change:
                return _blocked("BLOCKED_CANONICAL_INTEGRITY")
            if current["continuity_ordinal"] != previous["continuity_ordinal"] + 1:
                return _blocked("BLOCKED_CANONICAL_INTEGRITY")
            continue

        if not block_change:
            return _blocked("BLOCKED_CANONICAL_INTEGRITY")
        if current["continuity_ordinal"] != 0:
            return _blocked("BLOCKED_CANONICAL_INTEGRITY")
        if current["continuity_block_id"] in seen_blocks:
            return _blocked("BLOCKED_CANONICAL_INTEGRITY")

        seen_blocks.add(current["continuity_block_id"])

        if source_change and time_gap:
            mechanism = "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP"
        elif source_change:
            mechanism = "SOURCE_SEGMENT_CHANGE_ONLY"
        else:
            return _blocked("BLOCKED_UPSTREAM_SEMANTICS_DISCREPANCY")

        boundaries.append(
            {
                "row_index_t": i,
                "B_T_MS_UTC": previous["h1_start_ms_utc"] + HOUR_MS,
                "ending_ordinal": previous["continuity_ordinal"],
                "mechanism": mechanism,
            }
        )

    if len(seen_blocks) != len(boundaries) + 1:
        return _blocked("BLOCKED_CANONICAL_INTEGRITY")

    return {
        "status": "PASS",
        "boundaries": boundaries,
        "n_blocks": len(seen_blocks),
    }


def _block_lengths(rows):
    lengths = []
    ids = []
    current_id = rows[0]["continuity_block_id"]
    count = 0
    for row in rows:
        if row["continuity_block_id"] != current_id:
            ids.append(current_id)
            lengths.append(count)
            current_id = row["continuity_block_id"]
            count = 0
        count += 1
    ids.append(current_id)
    lengths.append(count)
    return ids, lengths


def _length_summary(lengths, prefix=""):
    if not lengths:
        return {
            f"{prefix}BLOCK_LENGTH_MIN": None,
            f"{prefix}BLOCK_LENGTH_MAX": None,
            f"{prefix}BLOCK_LENGTH_MEDIAN": None,
            f"{prefix}BLOCK_LENGTH_Q25": None,
            f"{prefix}BLOCK_LENGTH_Q75": None,
            f"{prefix}BLOCK_LENGTH_HISTOGRAM_EXACT": {},
        }
    return {
        f"{prefix}BLOCK_LENGTH_MIN": min(lengths),
        f"{prefix}BLOCK_LENGTH_MAX": max(lengths),
        f"{prefix}BLOCK_LENGTH_MEDIAN": _quantile_type7(lengths, 0.5),
        f"{prefix}BLOCK_LENGTH_Q25": _quantile_type7(lengths, 0.25),
        f"{prefix}BLOCK_LENGTH_Q75": _quantile_type7(lengths, 0.75),
        f"{prefix}BLOCK_LENGTH_HISTOGRAM_EXACT": _histogram(lengths),
    }


def _calendar_annotation(boundary):
    dt_utc = datetime.fromtimestamp(boundary["B_T_MS_UTC"] / 1000, tz=timezone.utc)
    ny = dt_utc.astimezone(ZoneInfo("America/New_York"))
    offset = ny.utcoffset()
    dst = ny.dst()
    return {
        "B_T_MS_UTC": boundary["B_T_MS_UTC"],
        "BOUNDARY_REASON": boundary["mechanism"],
        "UTC_WEEKDAY": dt_utc.isoweekday(),
        "UTC_HOUR": dt_utc.hour,
        "UTC_CALENDAR_MONTH": dt_utc.month,
        "UTC_CALENDAR_YEAR": dt_utc.year,
        "NY_UTC_OFFSET_SECONDS": int(offset.total_seconds()) if offset is not None else None,
        "NY_DST_STATE": "DST" if dst not in (None, timedelta(0)) else "STANDARD",
        "NY_LOCAL_WEEKDAY": ny.isoweekday(),
        "NY_LOCAL_HOUR": ny.hour,
    }


def _counter_dict(values):
    counts = Counter(values)
    return {str(k): counts[k] for k in sorted(counts, key=lambda x: str(x))}


def profile_structural_geometry(rows):
    calendar = verify_calendar_identity()
    if calendar["status"] != "PASS":
        return _blocked("BLOCKED_CALENDAR_IDENTITY")

    validated = _validate_row_schema_and_domain(rows)
    if validated["status"] != "PASS":
        return validated
    normalized = validated["rows"]

    continuity = _validate_continuity(normalized)
    if continuity["status"] != "PASS":
        return continuity

    boundaries = continuity["boundaries"]
    block_ids, lengths = _block_lengths(normalized)
    n_rows = len(normalized)
    n_blocks = len(block_ids)
    n_internal = len(boundaries)

    if n_blocks != n_internal + 1:
        return _blocked("BLOCKED_CANONICAL_INTEGRITY")

    interior_ids = set(block_ids)
    interior_ids.discard(block_ids[0])
    interior_ids.discard(block_ids[-1])
    interior_lengths = [
        length
        for block_id, length in zip(block_ids, lengths)
        if block_id in interior_ids
    ]

    mature_rows = sum(max(length - WARMUP_H1, 0) for length in lengths)
    mature_with_t1 = sum(max(length - WARMUP_H1 - 1, 0) for length in lengths)
    mature_internal_ends = sum(
        1 for length in lengths[:-1] if length >= WARMUP_H1 + 1
    )
    mature_dataset_end = 1 if lengths[-1] >= WARMUP_H1 + 1 else 0

    mechanism_counts = {
        "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP": 0,
        "SOURCE_SEGMENT_CHANGE_ONLY": 0,
        "TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT": 0,
    }
    for boundary in boundaries:
        mechanism_counts[boundary["mechanism"]] += 1

    if mechanism_counts["TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT"] != 0:
        return _blocked("BLOCKED_UPSTREAM_SEMANTICS_DISCREPANCY")

    annotations = [_calendar_annotation(boundary) for boundary in boundaries]

    profile = {
        "N_ROWS": n_rows,
        "N_BLOCKS": n_blocks,
        "N_INTERNAL_BOUNDARIES": n_internal,
        "N_DATASET_START_TRUNCATED_BLOCKS": 1,
        "N_DATASET_END_TRUNCATED_BLOCKS": 1,
        "N_DATASET_END_TERMINALS": 1,
        "DATASET_START_TRUNCATION_BLOCK_ID": block_ids[0],
        "DATASET_END_TRUNCATION_BLOCK_ID": block_ids[-1],
    }
    profile.update(_length_summary(lengths))
    profile.update(
        {
            "N_BLOCKS_LENGTH_1": sum(length == 1 for length in lengths),
            "N_BLOCKS_LENGTH_2_TO_20": sum(2 <= length <= 20 for length in lengths),
            "N_BLOCKS_LENGTH_21": sum(length == 21 for length in lengths),
            "N_BLOCKS_LENGTH_GE_22": sum(length >= 22 for length in lengths),
            "FRACTION_BLOCKS_LENGTH_LE_20": _fraction(sum(length <= 20 for length in lengths), n_blocks),
            "FRACTION_BLOCKS_LENGTH_GE_21": _fraction(sum(length >= 21 for length in lengths), n_blocks),
        }
    )
    profile.update(_length_summary(interior_lengths, prefix="INTERIOR_"))

    ending_ordinals = [boundary["ending_ordinal"] for boundary in boundaries]
    profile.update(
        {
            "BLOCK_END_ORDINAL_HISTOGRAM_EXACT": _histogram(ending_ordinals),
            "BLOCK_END_ORDINAL_MIN": min(ending_ordinals) if ending_ordinals else None,
            "BLOCK_END_ORDINAL_MAX": max(ending_ordinals) if ending_ordinals else None,
            "BLOCK_END_ORDINAL_MEDIAN": _quantile_type7(ending_ordinals, 0.5),
            "N_WARMUP_MATURE_ROWS": mature_rows,
            "N_WARMUP_MATURE_ROWS_WITH_SAME_BLOCK_T1": mature_with_t1,
            "N_WARMUP_MATURE_INTERNAL_BLOCK_END_ROWS": mature_internal_ends,
            "N_WARMUP_MATURE_DATASET_END_ROWS": mature_dataset_end,
            "FRACTION_WARMUP_MATURE_WITH_SAME_BLOCK_T1": _fraction(mature_with_t1, mature_rows),
            "FRACTION_WARMUP_MATURE_AT_INTERNAL_BLOCK_END": _fraction(mature_internal_ends, mature_rows),
            "BOUNDARY_MECHANISM_COUNTS": mechanism_counts,
            "BOUNDARY_CALENDAR_ROWS": annotations,
            "UTC_WEEKDAY_COUNTS": _counter_dict(row["UTC_WEEKDAY"] for row in annotations),
            "UTC_HOUR_COUNTS": _counter_dict(row["UTC_HOUR"] for row in annotations),
            "UTC_WEEKDAY_X_HOUR_COUNTS": _counter_dict(
                f'{row["UTC_WEEKDAY"]}|{row["UTC_HOUR"]:02d}' for row in annotations
            ),
            "UTC_CALENDAR_MONTH_COUNTS": _counter_dict(row["UTC_CALENDAR_MONTH"] for row in annotations),
            "UTC_CALENDAR_YEAR_COUNTS": _counter_dict(row["UTC_CALENDAR_YEAR"] for row in annotations),
            "NY_DST_STATE_X_UTC_WEEKDAY_X_HOUR_COUNTS": _counter_dict(
                f'{row["NY_DST_STATE"]}|{row["UTC_WEEKDAY"]}|{row["UTC_HOUR"]:02d}'
                for row in annotations
            ),
            "NY_UTC_OFFSET_X_UTC_WEEKDAY_X_HOUR_COUNTS": _counter_dict(
                f'{row["NY_UTC_OFFSET_SECONDS"]}|{row["UTC_WEEKDAY"]}|{row["UTC_HOUR"]:02d}'
                for row in annotations
            ),
            "BOUNDARY_REASON_X_UTC_WEEKDAY_X_HOUR_COUNTS": _counter_dict(
                f'{row["BOUNDARY_REASON"]}|{row["UTC_WEEKDAY"]}|{row["UTC_HOUR"]:02d}'
                for row in annotations
            ),
            "BOUNDARY_REASON_X_NY_DST_STATE_COUNTS": _counter_dict(
                f'{row["BOUNDARY_REASON"]}|{row["NY_DST_STATE"]}' for row in annotations
            ),
            "ROW_LEVEL_UPSTREAM_CLASSIFICATION": ROW_LEVEL_UPSTREAM_CLASSIFICATION,
            "SOURCE_B_AGGREGATE_CONTEXT": dict(SOURCE_B_AGGREGATE_CONTEXT),
        }
    )

    return {
        "status": "SYNTHETIC_PROFILE_PRODUCED",
        "authority": "SYNTHETIC_ONLY",
        "profile": profile,
    }
