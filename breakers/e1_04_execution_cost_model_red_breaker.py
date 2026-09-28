from __future__ import annotations

import importlib.util
import json
import math
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-04-EXECUTION-COST-MODEL-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(
    os.environ.get(
        "E1_04_RUNTIME_PATH",
        str(ROOT / "tools/e1_04_execution_cost_model.py"),
    )
)

RUNTIME_CONTRACT = "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1"
SIGNAL_END = 1_800_000_000_000
FORBIDDEN_CLAIMS = {
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
}


_CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert _CONTRACT["schema"] == "ATDS_E1_04_EXECUTION_COST_MODEL_CONTRACT_V0_1"
assert _CONTRACT["runtime_contract"] == RUNTIME_CONTRACT
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"E4-{i:02d}" for i in range(1, 23)]
assert len(_CONTRACT["test_cases"]) == 22


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("E1_04_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)

    spec = importlib.util.spec_from_file_location(
        "e1_04_execution_cost_model_under_test",
        RUNTIME_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail("E1_04_RUNTIME_UNLOADABLE_EXPECTED_RED", pytrace=False)

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name in ("CONTRACT", "COST_SCOPE", "FORBIDDEN_CLAIMS", "execute_transition"):
        assert hasattr(module, name), f"E1_04_RUNTIME_SURFACE_MISSING:{name}"
    assert module.CONTRACT == RUNTIME_CONTRACT
    return module


def _tick(ts, *, bid=100.0, ask=100.5, continuity="OK", mid=None):
    row = {
        "timestamp_ms": int(ts),
        "bid": bid,
        "ask": ask,
        "continuity_status": continuity,
    }
    if mid is not None:
        row["mid"] = mid
    return row


def _run(module, current, target, ticks):
    return module.execute_transition(
        current_position=current,
        target_position=target,
        signal_h1_end_ms=SIGNAL_END,
        raw_ticks=ticks,
    )


def _events(result):
    return result.get("events", [])


def _single_event(result):
    assert result["status"] == "EXECUTED"
    events = _events(result)
    assert len(events) == 1
    return events[0]


def test_e4_01_mid_only_raw_value_cannot_be_execution_price():
    m = _runtime()
    result = _run(m, 0, 1, [_tick(SIGNAL_END, bid=None, ask=None, mid=100.25)])
    assert result["status"] == "NOT_EXECUTED"
    assert _events(result) == []


def test_e4_02_same_bar_event_is_forbidden():
    m = _runtime()
    ticks = [
        _tick(SIGNAL_END - 1, bid=90.0, ask=90.5),
        _tick(SIGNAL_END, bid=101.0, ask=101.5),
    ]
    event = _single_event(_run(m, 0, 1, ticks))
    assert event["timestamp_ms"] == SIGNAL_END
    assert event["price"] == 101.5


def test_e4_03_first_admissible_t_plus_1_raw_tick_is_selected():
    m = _runtime()
    ticks = [
        _tick(SIGNAL_END, bid=100.0, ask=None),
        _tick(SIGNAL_END + 1, bid=101.0, ask=101.5),
        _tick(SIGNAL_END + 2, bid=102.0, ask=102.5),
    ]
    event = _single_event(_run(m, 0, 1, ticks))
    assert event["timestamp_ms"] == SIGNAL_END + 1
    assert event["price"] == 101.5


def test_e4_04_flat_to_long_uses_ask():
    m = _runtime()
    event = _single_event(_run(m, 0, 1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    assert event["action"] == "BUY"
    assert event["price_side"] == "ASK"
    assert event["price"] == 100.0


def test_e4_05_flat_to_short_uses_bid():
    m = _runtime()
    event = _single_event(_run(m, 0, -1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    assert event["action"] == "SELL"
    assert event["price_side"] == "BID"
    assert event["price"] == 99.0


def test_e4_06_long_to_neutral_closes_at_bid():
    m = _runtime()
    event = _single_event(_run(m, 1, 0, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    assert event["action"] == "SELL"
    assert event["price_side"] == "BID"
    assert event["price"] == 99.0


def test_e4_07_short_to_neutral_closes_at_ask():
    m = _runtime()
    event = _single_event(_run(m, -1, 0, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    assert event["action"] == "BUY"
    assert event["price_side"] == "ASK"
    assert event["price"] == 100.0


def test_e4_08_long_to_short_uses_same_bid_tick_for_close_and_open():
    m = _runtime()
    result = _run(m, 1, -1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)])
    assert result["status"] == "EXECUTED"
    events = _events(result)
    assert len(events) == 2
    assert [e["action"] for e in events] == ["SELL", "SELL"]
    assert [e["price_side"] for e in events] == ["BID", "BID"]
    assert [e["price"] for e in events] == [99.0, 99.0]
    assert len({e["timestamp_ms"] for e in events}) == 1


def test_e4_09_short_to_long_uses_same_ask_tick_for_close_and_open():
    m = _runtime()
    result = _run(m, -1, 1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)])
    assert result["status"] == "EXECUTED"
    events = _events(result)
    assert len(events) == 2
    assert [e["action"] for e in events] == ["BUY", "BUY"]
    assert [e["price_side"] for e in events] == ["ASK", "ASK"]
    assert [e["price"] for e in events] == [100.0, 100.0]
    assert len({e["timestamp_ms"] for e in events}) == 1


def test_e4_10_long_to_long_is_hold():
    m = _runtime()
    result = _run(m, 1, 1, [_tick(SIGNAL_END)])
    assert result["status"] == "HOLD"
    assert _events(result) == []


def test_e4_11_short_to_short_is_hold():
    m = _runtime()
    result = _run(m, -1, -1, [_tick(SIGNAL_END)])
    assert result["status"] == "HOLD"
    assert _events(result) == []


def test_e4_12_flat_to_neutral_is_hold():
    m = _runtime()
    result = _run(m, 0, 0, [_tick(SIGNAL_END)])
    assert result["status"] == "HOLD"
    assert _events(result) == []


def test_e4_13_pyramiding_target_is_blocked():
    m = _runtime()
    result = _run(m, 1, 2, [_tick(SIGNAL_END)])
    assert result["status"] == "BLOCKED"
    assert result["reason"] == "PYRAMIDING_FORBIDDEN"


def test_e4_14_missing_post_t_ask_is_not_forward_filled():
    m = _runtime()
    ticks = [
        _tick(SIGNAL_END - 1, bid=90.0, ask=90.5),
        _tick(SIGNAL_END, bid=100.0, ask=None),
        _tick(SIGNAL_END + 1, bid=101.0, ask=101.5),
    ]
    event = _single_event(_run(m, 0, 1, ticks))
    assert event["timestamp_ms"] == SIGNAL_END + 1
    assert event["price"] == 101.5


def test_e4_15_missing_required_side_is_not_last_price_carried():
    m = _runtime()
    ticks = [
        _tick(SIGNAL_END - 1, bid=90.0, ask=90.5),
        _tick(SIGNAL_END, bid=None, ask=100.5),
    ]
    result = _run(m, 1, 0, ticks)
    assert result["status"] == "NOT_EXECUTED"
    assert _events(result) == []


def test_e4_16_mid_is_not_substituted_for_bid_or_ask():
    m = _runtime()
    result = _run(
        m,
        -1,
        0,
        [_tick(SIGNAL_END, bid=None, ask=None, mid=100.25)],
    )
    assert result["status"] == "NOT_EXECUTED"
    assert _events(result) == []


def test_e4_17_forbidden_continuity_boundary_is_not_crossed():
    m = _runtime()
    ticks = [
        _tick(SIGNAL_END, bid=99.0, ask=100.0, continuity="FORBIDDEN_BOUNDARY"),
        _tick(SIGNAL_END + 1, bid=101.0, ask=101.5, continuity="OK"),
    ]
    result = _run(m, 0, 1, ticks)
    assert result["status"] == "NOT_EXECUTED"
    assert _events(result) == []


def test_e4_18_no_admissible_raw_tick_means_not_executed():
    m = _runtime()
    result = _run(m, 0, -1, [_tick(SIGNAL_END - 1, bid=99.0, ask=100.0)])
    assert result["status"] == "NOT_EXECUTED"
    assert _events(result) == []


def test_e4_19_spread_is_intrinsic_raw_bid_ask_cost():
    m = _runtime()
    scope = m.COST_SCOPE
    assert scope["spread"] == {"included": True, "mode": "RAW_BID_ASK_INTRINSIC"}
    long_event = _single_event(_run(m, 0, 1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    short_event = _single_event(_run(m, 0, -1, [_tick(SIGNAL_END, bid=99.0, ask=100.0)]))
    assert long_event["price"] == 100.0
    assert short_event["price"] == 99.0


def test_e4_20_commission_is_excluded_but_not_assumed_zero():
    m = _runtime()
    assert m.COST_SCOPE["commission"] == {"included": False, "assumed_zero": False}


def test_e4_21_slippage_and_financing_are_excluded_but_not_assumed_zero():
    m = _runtime()
    assert m.COST_SCOPE["slippage"] == {"included": False, "assumed_zero": False}
    assert m.COST_SCOPE["financing"] == {"included": False, "assumed_zero": False}


def test_e4_22_forbidden_claims_are_exactly_bounded():
    m = _runtime()
    assert set(m.FORBIDDEN_CLAIMS) == FORBIDDEN_CLAIMS
