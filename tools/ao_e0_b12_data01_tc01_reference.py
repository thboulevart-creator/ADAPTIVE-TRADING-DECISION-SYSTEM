from __future__ import annotations

import hashlib
import json
import math

CONTRACT = "ATDS_AO_E0_B12_DATA01_TC01_REFERENCE_V0_1"
EXPECTED_H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
REQUIRED_CLOSED_TRADES = 58927
FIRST_EVIDENCE_DECISION_TIME_MS = 1791284400000
HOUR_MS = 3_600_000


class TC01ReferenceBlocked(ValueError):
    pass


def _enc(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _digest(value):
    return hashlib.sha256(_enc(value)).hexdigest()


def _ok_num(value):
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(float(value))
    )


def _check_rows(rows):
    needed = {
        "h1_start_ms_utc",
        "source_segment_id",
        "continuity_block_id",
        "continuity_ordinal",
        "mid_close",
    }
    seen = set()
    previous = None
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or not needed.issubset(row):
            raise TC01ReferenceBlocked("MISSING_H1_FIELD")
        if not isinstance(row["h1_start_ms_utc"], int) or isinstance(row["h1_start_ms_utc"], bool):
            raise TC01ReferenceBlocked("INVALID_H1_TIMESTAMP")
        if not _ok_num(row["mid_close"]):
            raise TC01ReferenceBlocked("NONFINITE_MID_CLOSE")
        if previous is not None:
            if row["h1_start_ms_utc"] == previous["h1_start_ms_utc"]:
                raise TC01ReferenceBlocked("DUPLICATE_H1_TIMESTAMP")
            if row["h1_start_ms_utc"] < previous["h1_start_ms_utc"]:
                raise TC01ReferenceBlocked("INVALID_H1_ORDER")
        if i == 0:
            if row["continuity_ordinal"] != 0:
                raise TC01ReferenceBlocked("CONTINUITY_INCOHERENT")
            seen.add(row["continuity_block_id"])
        elif row["continuity_block_id"] == previous["continuity_block_id"]:
            if row["continuity_ordinal"] != previous["continuity_ordinal"] + 1:
                raise TC01ReferenceBlocked("CONTINUITY_INCOHERENT")
            if row["h1_start_ms_utc"] != previous["h1_start_ms_utc"] + HOUR_MS:
                raise TC01ReferenceBlocked("CONTINUITY_INCOHERENT")
        else:
            if row["continuity_block_id"] in seen or row["continuity_ordinal"] != 0:
                raise TC01ReferenceBlocked("CONTINUITY_INCOHERENT")
            seen.add(row["continuity_block_id"])
        previous = row


def _target(rows, i):
    row = rows[i]
    if row["continuity_ordinal"] < 20 or i < 20:
        return None
    prior = rows[i - 20]
    if prior["continuity_block_id"] != row["continuity_block_id"]:
        return None
    ratio = float(row["mid_close"]) / float(prior["mid_close"]) - 1.0
    return 1 if ratio > 0 else (-1 if ratio < 0 else 0)


def _side(current, target):
    if current not in (-1, 0, 1) or target not in (-1, 0, 1):
        raise TC01ReferenceBlocked("PYRAMIDING_FORBIDDEN")
    if current == target:
        return None
    table = {
        (0, 1): "ask",
        (0, -1): "bid",
        (1, 0): "bid",
        (-1, 0): "ask",
        (1, -1): "bid",
        (-1, 1): "ask",
    }
    if (current, target) not in table:
        raise TC01ReferenceBlocked("UNREACHABLE_TRANSITION")
    return table[(current, target)]


def _eligible(current, target, boundary, ticks):
    needed_side = _side(current, target)
    if needed_side is None:
        return "HOLD"

    for tick in ticks:
        if not isinstance(tick, dict) or not {"timestamp_ms", "bid", "ask", "continuity_status"}.issubset(tick):
            raise TC01ReferenceBlocked("MALFORMED_RAW_TICK")
        try:
            ts = int(tick["timestamp_ms"])
        except (TypeError, ValueError):
            raise TC01ReferenceBlocked("MALFORMED_RAW_TICK") from None
        if ts < boundary:
            continue
        if tick["continuity_status"] == "FORBIDDEN_BOUNDARY":
            return "NOT_EXECUTED"
        if _ok_num(tick[needed_side]):
            return "EXECUTED"
    return "NOT_EXECUTED"


def reference_count_only(
    h1_rows,
    *,
    raw_ticks,
    e1_03_identity,
    initial_position=0,
    first_evidence_decision_time_ms=FIRST_EVIDENCE_DECISION_TIME_MS,
    required_closed_trades=REQUIRED_CLOSED_TRADES,
):
    if e1_03_identity != EXPECTED_H1_IDENTITY:
        raise TC01ReferenceBlocked("E1_03_IDENTITY_MISMATCH")
    if initial_position not in (-1, 0, 1):
        raise TC01ReferenceBlocked("INVALID_INITIAL_POSITION")
    if not isinstance(required_closed_trades, int) or isinstance(required_closed_trades, bool) or required_closed_trades <= 0:
        raise TC01ReferenceBlocked("INVALID_REQUIRED_CLOSED_TRADES")
    _check_rows(h1_rows)

    current = initial_position
    total = 0
    terminal = None
    trace = []

    for i, row in enumerate(h1_rows):
        decision = row["h1_start_ms_utc"] + HOUR_MS
        target = _target(h1_rows, i)
        if target is None or decision < first_evidence_decision_time_ms:
            continue

        state = _eligible(current, target, decision, raw_ticks)
        inc = 0
        if state == "EXECUTED":
            if current != 0 and target != current:
                inc = 1
            current = target

        total += inc
        trace.append(
            {
                "decision_time_ms": decision,
                "transition_status": state,
                "closed_trade_increment": inc,
                "cumulative_closed_trade_count": total,
            }
        )
        if total >= required_closed_trades:
            terminal = decision
            break

    binding = {
        "h1_rows": h1_rows,
        "raw_ticks": raw_ticks,
        "first_evidence_decision_time_ms": first_evidence_decision_time_ms,
        "initial_position": initial_position,
        "required_closed_trades": required_closed_trades,
    }
    return {
        "cumulative_closed_trade_count": total,
        "terminal_threshold_reached": terminal is not None,
        "exact_terminal_decision_time_if_reached": terminal,
        "bound_input_identity_digest": _digest(binding),
        "count_trace_digest": _digest(trace),
    }
