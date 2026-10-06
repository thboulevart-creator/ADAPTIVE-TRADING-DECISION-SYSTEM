from __future__ import annotations

import hashlib
import json
import math

CONTRACT = "ATDS_AO_E0_B12_DATA01_TC01_COUNT_ONLY_V0_1"
EXPECTED_H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
REQUIRED_CLOSED_TRADES = 58927
FIRST_EVIDENCE_DECISION_TIME_MS = 1791284400000
HOUR_MS = 3_600_000

REQUIRED_H1_FIELDS = (
    "h1_start_ms_utc",
    "source_segment_id",
    "continuity_block_id",
    "continuity_ordinal",
    "mid_close",
)

ALLOWED_OUTPUT_KEYS = {
    "cumulative_closed_trade_count",
    "terminal_threshold_reached",
    "exact_terminal_decision_time_if_reached",
    "bound_input_identity_digest",
    "count_trace_digest",
}


class TC01Blocked(ValueError):
    pass


def _canonical_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(value) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _finite_number(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def _validate_h1_rows(h1_rows):
    if not isinstance(h1_rows, list):
        raise TC01Blocked("H1_ROWS_NOT_LIST")

    previous_ts = None
    previous_block = None
    previous_ordinal = None
    seen_blocks = set()

    for index, row in enumerate(h1_rows):
        if not isinstance(row, dict) or any(field not in row for field in REQUIRED_H1_FIELDS):
            raise TC01Blocked("MISSING_H1_FIELD")

        ts = row["h1_start_ms_utc"]
        close = row["mid_close"]
        if isinstance(ts, bool) or not isinstance(ts, int):
            raise TC01Blocked("INVALID_H1_TIMESTAMP")
        if not _finite_number(close):
            raise TC01Blocked("NONFINITE_MID_CLOSE")

        block = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]

        if previous_ts is not None:
            if ts == previous_ts:
                raise TC01Blocked("DUPLICATE_H1_TIMESTAMP")
            if ts < previous_ts:
                raise TC01Blocked("INVALID_H1_ORDER")

        if index == 0:
            if ordinal != 0:
                raise TC01Blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block)
        elif block == previous_block:
            if ordinal != previous_ordinal + 1 or ts != previous_ts + HOUR_MS:
                raise TC01Blocked("CONTINUITY_INCOHERENT")
        else:
            if block in seen_blocks or ordinal != 0:
                raise TC01Blocked("CONTINUITY_INCOHERENT")
            seen_blocks.add(block)

        previous_ts = ts
        previous_block = block
        previous_ordinal = ordinal


def _target_for_row(h1_rows, index, block_start_index):
    row = h1_rows[index]
    if row["continuity_ordinal"] < 20:
        return None

    lookback_index = index - 20
    if lookback_index < block_start_index:
        return None

    lookback = h1_rows[lookback_index]
    if lookback["continuity_block_id"] != row["continuity_block_id"]:
        return None

    momentum = float(row["mid_close"]) / float(lookback["mid_close"]) - 1.0
    if momentum > 0:
        return 1
    if momentum < 0:
        return -1
    return 0


def _required_side(current_position: int, target_position: int):
    if current_position not in (-1, 0, 1) or target_position not in (-1, 0, 1):
        raise TC01Blocked("PYRAMIDING_FORBIDDEN")
    if current_position == target_position:
        return None
    if current_position == -1 and target_position in (0, 1):
        return "ask"
    if current_position == 0 and target_position == 1:
        return "ask"
    if current_position == 1 and target_position in (0, -1):
        return "bid"
    if current_position == 0 and target_position == -1:
        return "bid"
    raise TC01Blocked("UNREACHABLE_TRANSITION")


def _structural_transition(current_position, target_position, decision_time_ms, raw_ticks):
    side = _required_side(current_position, target_position)
    if side is None:
        return "HOLD"

    for tick in raw_ticks:
        if not isinstance(tick, dict):
            raise TC01Blocked("MALFORMED_RAW_TICK")
        for field in ("timestamp_ms", "bid", "ask", "continuity_status"):
            if field not in tick:
                raise TC01Blocked("MALFORMED_RAW_TICK")

        try:
            timestamp_ms = int(tick["timestamp_ms"])
        except (TypeError, ValueError):
            raise TC01Blocked("MALFORMED_RAW_TICK") from None

        if timestamp_ms < int(decision_time_ms):
            continue

        if tick["continuity_status"] == "FORBIDDEN_BOUNDARY":
            return "NOT_EXECUTED"

        if _finite_number(tick[side]):
            return "EXECUTED"

    return "NOT_EXECUTED"


def _run_count_only_core(
    h1_rows,
    *,
    raw_ticks,
    first_evidence_decision_time_ms,
    initial_position,
    required_closed_trades,
):
    _validate_h1_rows(h1_rows)

    if initial_position not in (-1, 0, 1):
        raise TC01Blocked("INVALID_INITIAL_POSITION")
    if isinstance(required_closed_trades, bool) or not isinstance(required_closed_trades, int) or required_closed_trades <= 0:
        raise TC01Blocked("INVALID_REQUIRED_CLOSED_TRADES")
    if isinstance(first_evidence_decision_time_ms, bool) or not isinstance(first_evidence_decision_time_ms, int):
        raise TC01Blocked("INVALID_FIRST_EVIDENCE_TIME")

    current_position = initial_position
    cumulative = 0
    terminal_time = None
    block_start_index = 0
    previous_block = None
    trace = []

    for index, row in enumerate(h1_rows):
        block = row["continuity_block_id"]
        if previous_block is None or block != previous_block:
            block_start_index = index
        previous_block = block

        target = _target_for_row(h1_rows, index, block_start_index)
        decision_time = row["h1_start_ms_utc"] + HOUR_MS

        if target is None or decision_time < first_evidence_decision_time_ms:
            continue

        status = _structural_transition(
            current_position,
            target,
            decision_time,
            raw_ticks,
        )

        increment = 0
        if status == "EXECUTED":
            if current_position != 0 and target != current_position:
                increment = 1
            current_position = target

        cumulative += increment
        trace.append(
            {
                "decision_time_ms": decision_time,
                "transition_status": status,
                "closed_trade_increment": increment,
                "cumulative_closed_trade_count": cumulative,
            }
        )

        if cumulative >= required_closed_trades:
            terminal_time = decision_time
            break

    input_binding = {
        "h1_rows": h1_rows,
        "raw_ticks": raw_ticks,
        "first_evidence_decision_time_ms": first_evidence_decision_time_ms,
        "initial_position": initial_position,
        "required_closed_trades": required_closed_trades,
    }
    result = {
        "cumulative_closed_trade_count": cumulative,
        "terminal_threshold_reached": terminal_time is not None,
        "exact_terminal_decision_time_if_reached": terminal_time,
        "bound_input_identity_digest": _sha256(input_binding),
        "count_trace_digest": _sha256(trace),
    }
    if set(result) != ALLOWED_OUTPUT_KEYS:
        raise TC01Blocked("OUTPUT_SURFACE_VIOLATION")
    return result


def run_count_only(
    h1_rows,
    *,
    raw_ticks,
    e1_03_identity,
    initial_position=0,
    first_evidence_decision_time_ms=FIRST_EVIDENCE_DECISION_TIME_MS,
):
    if e1_03_identity != EXPECTED_H1_IDENTITY:
        raise TC01Blocked("E1_03_IDENTITY_MISMATCH")

    return _run_count_only_core(
        h1_rows,
        raw_ticks=raw_ticks,
        first_evidence_decision_time_ms=first_evidence_decision_time_ms,
        initial_position=initial_position,
        required_closed_trades=REQUIRED_CLOSED_TRADES,
    )
