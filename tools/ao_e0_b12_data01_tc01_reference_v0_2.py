from __future__ import annotations
from tools import ao_e0_b12_data01_tc01_reference as V1R

REFERENCE_PLANNING_N = 58927
START_MS = 1791284400000
END_MS = 1822820400000
NO_TERMINAL_THRESHOLD = 10**18
HOUR_MS = V1R.HOUR_MS

def reference_count(h1_rows, raw_ticks, e1_03_identity, initial_position=0):
    rows = [
        row for row in h1_rows
        if row["h1_start_ms_utc"] + HOUR_MS < END_MS
    ]
    ticks = [
        tick for tick in raw_ticks
        if START_MS <= int(tick["timestamp_ms"]) < END_MS
    ]
    out = V1R.reference_count_only(
        rows,
        raw_ticks=ticks,
        e1_03_identity=e1_03_identity,
        initial_position=initial_position,
        first_evidence_decision_time_ms=START_MS,
        required_closed_trades=NO_TERMINAL_THRESHOLD,
    )
    count = out["cumulative_closed_trade_count"]
    return {
        "cumulative_closed_trade_count": count,
        "reference_planning_n_reached": count >= REFERENCE_PLANNING_N,
    }
