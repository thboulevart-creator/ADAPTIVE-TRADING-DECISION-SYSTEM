from __future__ import annotations

import math

CONTRACT = "ATDS_E1_06_INDEPENDENT_REFERENCE_V0_1"
HOUR_MS = 3_600_000
H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"

PNL_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}

FORBIDDEN_CLAIMS = (
    "STRATEGY_QUALIFIED",
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
)


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def _transition(current, target):
    if current == target:
        return "HOLD", ()
    table = {
        (0, 1): (("BUY", "ASK", "OPEN"),),
        (0, -1): (("SELL", "BID", "OPEN"),),
        (1, 0): (("SELL", "BID", "CLOSE"),),
        (-1, 0): (("BUY", "ASK", "CLOSE"),),
        (1, -1): (("SELL", "BID", "CLOSE"), ("SELL", "BID", "OPEN")),
        (-1, 1): (("BUY", "ASK", "CLOSE"), ("BUY", "ASK", "OPEN")),
    }
    return "EXECUTE", table[(current, target)]


def _execute(current, target, signal_end, raw_ticks):
    mode, specs = _transition(current, target)
    if mode == "HOLD":
        return {"status": "HOLD", "events": []}
    for tick in raw_ticks:
        ts = int(tick["timestamp_ms"])
        if ts < int(signal_end):
            continue
        if tick.get("continuity_status") == "FORBIDDEN_BOUNDARY":
            return {"status": "NOT_EXECUTED", "events": []}
        needed = {side.lower() for _, side, _ in specs}
        if any(not _finite(tick.get(side)) for side in needed):
            continue
        events = []
        for action, side, role in specs:
            e = {
                "timestamp_ms": ts,
                "action": action,
                "quantity": 1,
                "price_side": side,
                "price": float(tick[side.lower()]),
            }
            if len(specs) == 2:
                e["role"] = role
            events.append(e)
        return {"status": "EXECUTED", "events": events}
    return {"status": "NOT_EXECUTED", "events": []}


def _derive_pnl(records, initial_position=0):
    position = initial_position
    entry = None
    components = []
    transitions = []
    for record in records:
        execution = record["execution"]
        events = execution.get("events", [])
        before = position
        if execution["status"] != "EXECUTED":
            transitions.append({
                "h1_start_ms_utc": record["h1_start_ms_utc"],
                "before": before,
                "after": position,
                "status": execution["status"],
            })
            continue
        for event in events:
            px = float(event["price"])
            action = event["action"]
            role = event.get("role")
            if position == 0:
                position = 1 if action == "BUY" else -1
                entry = px
            elif position == 1 and action == "SELL":
                components.append(round(px - entry, 12))
                position = 0
                entry = None
                if role == "CLOSE" and len(events) == 2:
                    continue
            elif position == -1 and action == "BUY":
                components.append(round(entry - px, 12))
                position = 0
                entry = None
                if role == "CLOSE" and len(events) == 2:
                    continue
            if role == "OPEN":
                position = 1 if action == "BUY" else -1
                entry = px
        transitions.append({
            "h1_start_ms_utc": record["h1_start_ms_utc"],
            "before": before,
            "after": position,
            "status": execution["status"],
        })
    return {
        "components": components,
        "aggregate": round(sum(components), 12),
        "trade_count": len(components),
        "transitions": transitions,
    }


def reference_run(h1_rows, *, raw_ticks, initial_position=0):
    records = []
    current = initial_position
    block_start = 0
    previous_block = None
    for i, row in enumerate(h1_rows):
        block = row["continuity_block_id"]
        if previous_block is None or block != previous_block:
            block_start = i
        previous_block = block
        if row["continuity_ordinal"] < 20 or i - 20 < block_start:
            signal, target, lb = "UNDEFINED", None, None
            execution = {"status": "NOT_APPLICABLE", "events": []}
        else:
            lookback = h1_rows[i - 20]
            if lookback["continuity_block_id"] != block:
                signal, target, lb = "UNDEFINED", None, None
                execution = {"status": "NOT_APPLICABLE", "events": []}
            else:
                m = float(row["mid_close"]) / float(lookback["mid_close"]) - 1.0
                if m > 0:
                    signal, target = "LONG", 1
                elif m < 0:
                    signal, target = "SHORT", -1
                else:
                    signal, target = "NEUTRAL", 0
                lb = lookback["h1_start_ms_utc"]
                execution = _execute(
                    current,
                    target,
                    row["h1_start_ms_utc"] + HOUR_MS,
                    raw_ticks,
                )
                if execution["status"] == "EXECUTED":
                    current = target
        records.append({
            "h1_start_ms_utc": row["h1_start_ms_utc"],
            "signal": signal,
            "target_position": target,
            "execution": execution,
            "trace": {
                "continuity_block_id": block,
                "continuity_ordinal": row["continuity_ordinal"],
                "lookback_h1_start_ms_utc": lb,
            },
        })
    pnl = _derive_pnl(records, initial_position=initial_position)
    return {
        "status": "PASS",
        "records": records,
        "pnl_components": pnl["components"],
        "aggregate_pnl": pnl["aggregate"],
        "trade_count": pnl["trade_count"],
        "transitions": pnl["transitions"],
        "pnl_scope": PNL_SCOPE,
    }
