from __future__ import annotations

import math


CONTRACT = "ATDS_SFE_02B_MEAN_REVERSION_V1_RUNTIME_V0_1"
STRATEGY_ID = "MEAN_REVERSION_V1"
BAR_INTERVAL = "H1"
LOOKBACK = 20
Z_THRESHOLD = 1.0
SIGMA_DENOMINATOR = 20
HOUR_MS = 3_600_000

MEAN_ALGORITHM = "FSUM_DIVIDED_TERMS"
SIGMA_ALGORITHM = "SCALED_TWO_PASS_POPULATION"
ZERO_SIGMA_RULE = "EXACT_ZERO_UNDEFINED"

PROHIBITED_FEATURES = (
    "PARAMETER_OPTIMIZATION",
    "PERFORMANCE_OBSERVATION",
    "BEHAVIORAL_Y_CALCULATION",
    "PNL_CALCULATION",
    "EXECUTION",
    "POSITION_STATE",
    "REGIME_FILTER",
    "ROUTER",
    "DISCRETIONARY_OVERRIDE",
    "BREAKOUT_PERFORMANCE_CONSUMPTION",
    "E1_TD_DATA_CONSUMPTION",
)

FORBIDDEN_CLAIMS = (
    "MEAN_REVERSION_V1_SUPPORTED",
    "MEAN_REVERSION_V1_REFUTED",
    "MEAN_REVERSION_V1_PROFITABLE",
    "ECONOMIC_EDGE",
    "ROBUST",
    "SOURCE_INDEPENDENT",
    "PRODUCTION_READY",
    "PAPER_READY",
    "BROKER_READY",
    "LIVE_READY",
    "CAPITAL_READY",
)

REQUIRED_FIELDS = (
    "bar_start_ms_utc",
    "continuity_block_id",
    "continuity_ordinal",
    "close",
)


def _blocked(reason: str) -> dict:
    return {"status": "BLOCKED", "reason": reason}


def _normalize_rows(h1_rows):
    if not isinstance(h1_rows, list):
        return None, _blocked("INPUT_NOT_LIST")

    normalized = []
    for row in h1_rows:
        if not isinstance(row, dict):
            return None, _blocked("ROW_NOT_OBJECT")

        if any(field not in row for field in REQUIRED_FIELDS):
            return None, _blocked("MISSING_REQUIRED_FIELD")

        timestamp = row["bar_start_ms_utc"]
        block_id = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]
        close = row["close"]

        if isinstance(timestamp, bool) or not isinstance(timestamp, int):
            return None, _blocked("INVALID_TIMESTAMP_TYPE")

        if isinstance(close, bool) or not isinstance(close, (int, float)):
            return None, _blocked("INVALID_CLOSE_TYPE")

        try:
            close_f64 = float(close)
        except (OverflowError, ValueError):
            return None, _blocked("NONFINITE_CLOSE")

        if not math.isfinite(close_f64):
            return None, _blocked("NONFINITE_CLOSE")
        if close_f64 <= 0.0:
            return None, _blocked("NONPOSITIVE_CLOSE")

        if isinstance(block_id, bool) or not isinstance(block_id, (str, int)):
            return None, _blocked("INVALID_BLOCK_ID")

        if isinstance(ordinal, bool) or not isinstance(ordinal, int):
            return None, _blocked("INVALID_ORDINAL_TYPE")

        normalized.append(
            {
                "bar_start_ms_utc": timestamp,
                "continuity_block_id": block_id,
                "continuity_ordinal": ordinal,
                "close": close_f64,
            }
        )

    previous_timestamp = None
    for row in normalized:
        timestamp = row["bar_start_ms_utc"]
        if previous_timestamp is not None:
            if timestamp == previous_timestamp:
                return None, _blocked("DUPLICATE_TIMESTAMP")
            if timestamp < previous_timestamp:
                return None, _blocked("INVALID_TIMESTAMP_ORDER")
        previous_timestamp = timestamp

    previous_timestamp = None
    previous_block = None
    previous_ordinal = None
    seen_blocks = set()

    for index, row in enumerate(normalized):
        timestamp = row["bar_start_ms_utc"]
        block_id = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]

        if index == 0:
            if ordinal != 0:
                return None, _blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block_id)
        elif block_id == previous_block:
            if ordinal != previous_ordinal + 1:
                return None, _blocked("CONTINUITY_INCOHERENT")
            if timestamp != previous_timestamp + HOUR_MS:
                return None, _blocked("CONTINUITY_INCOHERENT")
        else:
            if block_id in seen_blocks:
                return None, _blocked("CONTINUITY_INCOHERENT")
            if ordinal != 0:
                return None, _blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block_id)

        previous_timestamp = timestamp
        previous_block = block_id
        previous_ordinal = ordinal

    return normalized, None


def _population_reference(window):
    mu = math.fsum(value / float(LOOKBACK) for value in window)
    deviations = [value - mu for value in window]
    scale = max(abs(value) for value in deviations)

    if scale == 0.0:
        return mu, 0.0

    scaled_population_second_moment = math.fsum(
        ((value / scale) ** 2) / float(SIGMA_DENOMINATOR)
        for value in deviations
    )
    sigma = scale * math.sqrt(scaled_population_second_moment)
    return mu, sigma


def _signal_at(rows, index: int, block_start_index: int):
    row = rows[index]
    ordinal = row["continuity_ordinal"]

    if ordinal < LOOKBACK or index - LOOKBACK < block_start_index:
        return "UNDEFINED", None, None

    lookback_start_index = index - LOOKBACK
    lookback_end_index = index - 1
    window = [item["close"] for item in rows[lookback_start_index:index]]

    mu, sigma = _population_reference(window)

    if sigma == 0.0:
        signal = "UNDEFINED"
    else:
        z_score = (row["close"] - mu) / sigma
        if z_score <= -Z_THRESHOLD:
            signal = "LONG"
        elif z_score >= Z_THRESHOLD:
            signal = "SHORT"
        else:
            signal = "NEUTRAL"

    return (
        signal,
        rows[lookback_start_index]["bar_start_ms_utc"],
        rows[lookback_end_index]["bar_start_ms_utc"],
    )


def run_mean_reversion_v1(h1_rows):
    rows, validation_error = _normalize_rows(h1_rows)
    if validation_error is not None:
        return validation_error

    records = []
    block_start_index = 0
    previous_block = None

    for index, row in enumerate(rows):
        block_id = row["continuity_block_id"]
        if previous_block is None or block_id != previous_block:
            block_start_index = index

        signal, lookback_start, lookback_end = _signal_at(
            rows,
            index,
            block_start_index,
        )

        records.append(
            {
                "bar_start_ms_utc": row["bar_start_ms_utc"],
                "signal": signal,
                "trace": {
                    "continuity_block_id": block_id,
                    "continuity_ordinal": row["continuity_ordinal"],
                    "lookback_start_ms_utc": lookback_start,
                    "lookback_end_ms_utc": lookback_end,
                },
            }
        )

        previous_block = block_id

    return {"status": "PASS", "records": records}
