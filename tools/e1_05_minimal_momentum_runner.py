from __future__ import annotations

import math


CONTRACT = "ATDS_E1_05_MINIMAL_MOMENTUM_RUNNER_V0_1"
EXPECTED_H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
EXPECTED_E1_04_CONTRACT = "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1"

PROHIBITED_FEATURES = (
    "PARAMETER_OPTIMIZATION",
    "REGIME_FILTER",
    "DISCRETIONARY_OVERRIDE",
    "PYRAMIDING",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP",
    "BREAK_EVEN",
    "POSITION_SIZING_OPTIMIZATION",
)

FORBIDDEN_CLAIMS = (
    "STRATEGY_QUALIFIED",
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
)

HOUR_MS = 3_600_000
REQUIRED_H1_FIELDS = (
    "h1_start_ms_utc",
    "source_segment_id",
    "continuity_block_id",
    "continuity_ordinal",
    "mid_close",
)


def _blocked(reason: str) -> dict:
    return {"status": "BLOCKED", "reason": reason}


def _finite_number(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def _validate_dependencies(*, e1_03_identity, e1_04_runtime):
    if e1_03_identity is None:
        return _blocked("E1_03_IDENTITY_MISSING")
    if e1_03_identity != EXPECTED_H1_IDENTITY:
        return _blocked("E1_03_IDENTITY_MISMATCH")

    if e1_04_runtime is None:
        return _blocked("E1_04_RUNTIME_MISSING")
    if getattr(e1_04_runtime, "CONTRACT", None) != EXPECTED_E1_04_CONTRACT:
        return _blocked("E1_04_IDENTITY_MISMATCH")
    if not callable(getattr(e1_04_runtime, "execute_transition", None)):
        return _blocked("E1_04_RUNTIME_SURFACE_MISSING")

    return None


def _validate_h1_rows(h1_rows):
    previous_ts = None

    for row in h1_rows:
        if not isinstance(row, dict):
            return _blocked("MISSING_H1_FIELD")

        if any(field not in row for field in REQUIRED_H1_FIELDS):
            return _blocked("MISSING_H1_FIELD")

        ts = row["h1_start_ms_utc"]
        close = row["mid_close"]

        if not _finite_number(close):
            return _blocked("NONFINITE_MID_CLOSE")

        if previous_ts is not None:
            if ts == previous_ts:
                return _blocked("DUPLICATE_H1_TIMESTAMP")
            if ts < previous_ts:
                return _blocked("INVALID_H1_ORDER")

        previous_ts = ts

    previous_ts = None
    previous_block = None
    previous_ordinal = None
    seen_blocks = set()

    for index, row in enumerate(h1_rows):
        ts = row["h1_start_ms_utc"]
        block = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]

        if index == 0:
            if ordinal != 0:
                return _blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block)
        elif block == previous_block:
            if ordinal != previous_ordinal + 1:
                return _blocked("CONTINUITY_INCOHERENT")
            if ts != previous_ts + HOUR_MS:
                return _blocked("CONTINUITY_INCOHERENT")
        else:
            if block in seen_blocks:
                return _blocked("CONTINUITY_INCOHERENT")
            if ordinal != 0:
                return _blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block)

        previous_ts = ts
        previous_block = block
        previous_ordinal = ordinal

    return None

def _signal_for_row(h1_rows, index, block_start_index):
    row = h1_rows[index]

    if row["continuity_ordinal"] < 20:
        return "UNDEFINED", None, None

    lookback_index = index - 20
    if lookback_index < block_start_index:
        return "UNDEFINED", None, None

    lookback = h1_rows[lookback_index]
    if lookback["continuity_block_id"] != row["continuity_block_id"]:
        return "UNDEFINED", None, None

    momentum = float(row["mid_close"]) / float(lookback["mid_close"]) - 1.0

    if momentum > 0:
        return "LONG", 1, lookback["h1_start_ms_utc"]
    if momentum < 0:
        return "SHORT", -1, lookback["h1_start_ms_utc"]
    return "NEUTRAL", 0, lookback["h1_start_ms_utc"]


def run_momentum_runner(
    h1_rows,
    *,
    raw_ticks,
    e1_03_identity,
    e1_04_runtime,
    initial_position=0,
):
    dependency_error = _validate_dependencies(
        e1_03_identity=e1_03_identity,
        e1_04_runtime=e1_04_runtime,
    )
    if dependency_error is not None:
        return dependency_error

    validation_error = _validate_h1_rows(h1_rows)
    if validation_error is not None:
        return validation_error

    current_position = initial_position
    records = []
    block_start_index = 0
    previous_block = None

    for index, row in enumerate(h1_rows):
        block = row["continuity_block_id"]
        if previous_block is None or block != previous_block:
            block_start_index = index
        previous_block = block

        signal, target_position, lookback_h1_start_ms_utc = _signal_for_row(
            h1_rows,
            index,
            block_start_index,
        )

        trace = {
            "continuity_block_id": block,
            "continuity_ordinal": row["continuity_ordinal"],
            "lookback_h1_start_ms_utc": lookback_h1_start_ms_utc,
        }

        if signal == "UNDEFINED":
            execution = {"status": "NOT_APPLICABLE", "events": []}
        else:
            execution = e1_04_runtime.execute_transition(
                current_position=current_position,
                target_position=target_position,
                signal_h1_end_ms=row["h1_start_ms_utc"] + HOUR_MS,
                raw_ticks=raw_ticks,
            )
            if execution.get("status") == "EXECUTED":
                current_position = target_position

        records.append(
            {
                "h1_start_ms_utc": row["h1_start_ms_utc"],
                "signal": signal,
                "target_position": target_position,
                "execution": execution,
                "trace": trace,
            }
        )

    return {"status": "PASS", "records": records}
