from __future__ import annotations

import hashlib
import json
from tools import ao_e0_b12_data01_tc01_count_only as V1

REFERENCE_PLANNING_N = 58927
EVIDENCE_START_MS = 1791284400000
EVIDENCE_END_EXCLUSIVE_MS = 1822820400000
NO_TERMINAL_THRESHOLD = 10**18
HOUR_MS = V1.HOUR_MS
EXPECTED_H1_IDENTITY = V1.EXPECTED_H1_IDENTITY
TC01Blocked = V1.TC01Blocked

ALLOWED_OUTPUT_KEYS = {
    "cumulative_closed_trade_count",
    "reference_planning_n_reached",
    "bound_input_identity_digest",
    "count_trace_digest",
}

def _sha(value) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(data).hexdigest()

def _bounded_rows(rows):
    if not isinstance(rows, list):
        raise TC01Blocked("H1_ROWS_NOT_LIST")
    kept = []
    for row in rows:
        if not isinstance(row, dict) or "h1_start_ms_utc" not in row:
            raise TC01Blocked("MISSING_H1_FIELD")
        decision = row["h1_start_ms_utc"] + HOUR_MS
        if decision < EVIDENCE_END_EXCLUSIVE_MS:
            kept.append(row)
    return kept

def _bounded_ticks(ticks):
    if not isinstance(ticks, list):
        raise TC01Blocked("RAW_TICKS_NOT_LIST")
    kept = []
    for tick in ticks:
        if not isinstance(tick, dict) or "timestamp_ms" not in tick:
            raise TC01Blocked("MALFORMED_RAW_TICK")
        ts = int(tick["timestamp_ms"])
        if EVIDENCE_START_MS <= ts < EVIDENCE_END_EXCLUSIVE_MS:
            kept.append(tick)
    return kept

def run_count_only(h1_rows, *, raw_ticks, e1_03_identity, initial_position=0):
    if e1_03_identity != EXPECTED_H1_IDENTITY:
        raise TC01Blocked("E1_03_IDENTITY_MISMATCH")

    rows = _bounded_rows(h1_rows)
    ticks = _bounded_ticks(raw_ticks)
    inner = V1._run_count_only_core(
        rows,
        raw_ticks=ticks,
        first_evidence_decision_time_ms=EVIDENCE_START_MS,
        initial_position=initial_position,
        required_closed_trades=NO_TERMINAL_THRESHOLD,
    )
    count = inner["cumulative_closed_trade_count"]
    result = {
        "cumulative_closed_trade_count": count,
        "reference_planning_n_reached": count >= REFERENCE_PLANNING_N,
        "bound_input_identity_digest": _sha({
            "rows": rows,
            "ticks": ticks,
            "start": EVIDENCE_START_MS,
            "end": EVIDENCE_END_EXCLUSIVE_MS,
            "initial_position": initial_position,
            "reference_planning_n": REFERENCE_PLANNING_N,
        }),
        "count_trace_digest": inner["count_trace_digest"],
    }
    if set(result) != ALLOWED_OUTPUT_KEYS:
        raise TC01Blocked("OUTPUT_SURFACE_VIOLATION")
    return result
