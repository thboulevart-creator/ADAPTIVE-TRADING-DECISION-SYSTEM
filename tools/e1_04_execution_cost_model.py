from __future__ import annotations

import math


CONTRACT = "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1"

COST_SCOPE = {
    "spread": {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"},
    "commission": {"included": False, "assumed_zero": False},
    "slippage": {"included": False, "assumed_zero": False},
    "financing": {"included": False, "assumed_zero": False},
}

FORBIDDEN_CLAIMS = (
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
)


def _result(status: str, *, events=None, reason=None) -> dict:
    out = {"status": status, "events": [] if events is None else events}
    if reason is not None:
        out["reason"] = reason
    return out


def _valid_price(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(float(value))


def _transition_spec(current_position: int, target_position: int):
    transition = (current_position, target_position)

    if transition in ((1, 1), (-1, -1), (0, 0)):
        return "HOLD", ()

    specs = {
        (0, 1): (("BUY", "ASK", None),),
        (0, -1): (("SELL", "BID", None),),
        (1, 0): (("SELL", "BID", None),),
        (-1, 0): (("BUY", "ASK", None),),
        (1, -1): (
            ("SELL", "BID", "CLOSE"),
            ("SELL", "BID", "OPEN"),
        ),
        (-1, 1): (
            ("BUY", "ASK", "CLOSE"),
            ("BUY", "ASK", "OPEN"),
        ),
    }
    return "EXECUTE", specs[transition]


def execute_transition(
    *,
    current_position: int,
    target_position: int,
    signal_h1_end_ms: int,
    raw_ticks,
):
    if target_position not in (-1, 0, 1):
        return _result("BLOCKED", reason="PYRAMIDING_FORBIDDEN")

    mode, specs = _transition_spec(current_position, target_position)
    if mode == "HOLD":
        return _result("HOLD")

    for tick in raw_ticks:
        timestamp_ms = int(tick["timestamp_ms"])
        if timestamp_ms < int(signal_h1_end_ms):
            continue

        if tick["continuity_status"] == "FORBIDDEN_BOUNDARY":
            return _result("NOT_EXECUTED")

        required_sides = {price_side for _, price_side, _ in specs}
        if any(
            not _valid_price(tick[price_side.lower()])
            for price_side in required_sides
        ):
            continue

        events = []
        for action, price_side, role in specs:
            event = {
                "timestamp_ms": timestamp_ms,
                "action": action,
                "quantity": 1,
                "price_side": price_side,
                "price": float(tick[price_side.lower()]),
            }
            if role is not None:
                event["role"] = role
            events.append(event)

        return _result("EXECUTED", events=events)

    return _result("NOT_EXECUTED")
