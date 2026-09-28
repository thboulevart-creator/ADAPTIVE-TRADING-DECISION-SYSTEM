from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-05-MINIMAL-MOMENTUM-RUNNER-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(
    os.environ.get(
        "E1_05_RUNTIME_PATH",
        str(ROOT / "tools/e1_05_minimal_momentum_runner.py"),
    )
)
E1_04_RUNTIME_PATH = ROOT / "tools/e1_04_execution_cost_model.py"

RUNTIME_CONTRACT = "ATDS_E1_05_MINIMAL_MOMENTUM_RUNNER_V0_1"
H1_IDENTITY = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"
E1_04_CONTRACT = "ATDS_E1_04_EXECUTION_COST_MODEL_V0_1"
HOUR_MS = 3_600_000
OOS_START_MS = 1_748_131_200_000
BASE_MS = OOS_START_MS - 30 * HOUR_MS

PROHIBITED_FEATURES = {
    "PARAMETER_OPTIMIZATION",
    "REGIME_FILTER",
    "DISCRETIONARY_OVERRIDE",
    "PYRAMIDING",
    "STOP_LOSS",
    "TAKE_PROFIT",
    "TRAILING_STOP",
    "BREAK_EVEN",
    "POSITION_SIZING_OPTIMIZATION",
}
FORBIDDEN_CLAIMS = {
    "STRATEGY_QUALIFIED",
    "BROKER_NET_PNL",
    "ALL_IN_COST_PROFITABILITY",
    "LIVE_PROFITABILITY",
    "FULL_BROKER_EXECUTION_REALISM",
}

_CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert _CONTRACT["schema"] == "ATDS_E1_05_MINIMAL_MOMENTUM_RUNNER_CONTRACT_V0_1"
assert _CONTRACT["runtime_contract"] == RUNTIME_CONTRACT
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"M5-{i:02d}" for i in range(1, 34)]
assert len(_CONTRACT["test_cases"]) == 33


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"MODULE_UNLOADABLE:{name}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("E1_05_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    module = _load_module(RUNTIME_PATH, "e1_05_minimal_momentum_runner_under_test")
    for name in (
        "CONTRACT",
        "EXPECTED_H1_IDENTITY",
        "EXPECTED_E1_04_CONTRACT",
        "PROHIBITED_FEATURES",
        "FORBIDDEN_CLAIMS",
        "run_momentum_runner",
    ):
        assert hasattr(module, name), f"E1_05_RUNTIME_SURFACE_MISSING:{name}"
    assert module.CONTRACT == RUNTIME_CONTRACT
    assert module.EXPECTED_H1_IDENTITY == H1_IDENTITY
    assert module.EXPECTED_E1_04_CONTRACT == E1_04_CONTRACT
    return module


def _e104():
    assert E1_04_RUNTIME_PATH.is_file()
    module = _load_module(E1_04_RUNTIME_PATH, "e1_04_runtime_for_e1_05_tests")
    assert module.CONTRACT == E1_04_CONTRACT
    return module


def _rows(
    count,
    *,
    start=BASE_MS,
    block=7,
    source_segment=11,
    close_fn=None,
    ordinal_start=0,
):
    if close_fn is None:
        close_fn = lambda i: 100.0 + i
    return [
        {
            "h1_start_ms_utc": start + i * HOUR_MS,
            "source_segment_id": source_segment,
            "continuity_block_id": block,
            "continuity_ordinal": ordinal_start + i,
            "mid_close": float(close_fn(i)),
        }
        for i in range(count)
    ]


def _tick(ts, *, bid=100.0, ask=100.5, continuity="OK"):
    return {
        "timestamp_ms": int(ts),
        "bid": bid,
        "ask": ask,
        "continuity_status": continuity,
    }


def _run(
    module,
    h1_rows,
    *,
    raw_ticks=None,
    e1_03_identity=H1_IDENTITY,
    e1_04_runtime="DEFAULT",
    initial_position=0,
):
    if raw_ticks is None:
        raw_ticks = []
    if e1_04_runtime == "DEFAULT":
        e1_04_runtime = _e104()
    return module.run_momentum_runner(
        h1_rows,
        raw_ticks=raw_ticks,
        e1_03_identity=e1_03_identity,
        e1_04_runtime=e1_04_runtime,
        initial_position=initial_position,
    )


def _last_record(result):
    assert result["status"] == "PASS"
    assert result["records"]
    return result["records"][-1]


def _set_endpoint(rows, *, first=100.0, last=101.0):
    out = copy.deepcopy(rows)
    out[0]["mid_close"] = float(first)
    out[-1]["mid_close"] = float(last)
    return out


def _all_keys(value):
    keys = set()
    if isinstance(value, dict):
        keys.update(value.keys())
        for item in value.values():
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return keys


def test_m5_01_ordinal_19_is_undefined():
    m = _runtime()
    record = _last_record(_run(m, _rows(20)))
    assert record["signal"] == "UNDEFINED"
    assert record["target_position"] is None
    assert record["execution"] == {"status": "NOT_APPLICABLE", "events": []}


def test_m5_02_positive_exact_t_minus_20_is_long():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    record = _last_record(_run(m, rows))
    assert record["signal"] == "LONG"
    assert record["target_position"] == 1


def test_m5_03_negative_exact_t_minus_20_is_short():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=99.0)
    record = _last_record(_run(m, rows))
    assert record["signal"] == "SHORT"
    assert record["target_position"] == -1


def test_m5_04_zero_exact_t_minus_20_is_neutral():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=100.0)
    record = _last_record(_run(m, rows))
    assert record["signal"] == "NEUTRAL"
    assert record["target_position"] == 0


def test_m5_05_formula_uses_exact_t_minus_20_not_adjacent_bar():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[0]["mid_close"] = 100.0
    rows[19]["mid_close"] = 1000.0
    rows[20]["mid_close"] = 101.0
    record = _last_record(_run(m, rows))
    assert record["signal"] == "LONG"


def test_m5_06_block_change_resets_warmup_and_forbids_cross_block_lookback():
    m = _runtime()
    rows = _rows(20, block=7)
    rows += _rows(
        1,
        start=rows[-1]["h1_start_ms_utc"] + HOUR_MS,
        block=8,
        source_segment=12,
        ordinal_start=0,
        close_fn=lambda _: 200.0,
    )
    record = _last_record(_run(m, rows))
    assert record["signal"] == "UNDEFINED"
    assert record["trace"]["lookback_h1_start_ms_utc"] is None


def test_m5_07_ordinal_20_is_first_eligible_signal():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    result = _run(m, rows)
    assert result["records"][19]["signal"] == "UNDEFINED"
    assert result["records"][20]["signal"] == "LONG"


def test_m5_08_oos_boundary_does_not_reset_same_block_warmup():
    m = _runtime()
    start = OOS_START_MS - 20 * HOUR_MS
    rows = _rows(21, start=start, close_fn=lambda i: 100.0 + i)
    assert rows[-1]["h1_start_ms_utc"] == OOS_START_MS
    record = _last_record(_run(m, rows))
    assert record["signal"] == "LONG"
    assert record["trace"]["lookback_h1_start_ms_utc"] == start


def test_m5_09_future_mutation_cannot_change_prior_signal():
    m = _runtime()
    rows = _rows(22, close_fn=lambda i: 100.0 + i)
    baseline = _run(m, rows)
    mutated = copy.deepcopy(rows)
    mutated[21]["mid_close"] = 1_000_000.0
    after = _run(m, mutated)
    assert baseline["records"][20] == after["records"][20]


def test_m5_10_raw_tick_inside_signal_h1_cannot_execute():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    t = rows[-1]["h1_start_ms_utc"]
    raw_ticks = [
        _tick(t + HOUR_MS - 1, bid=90.0, ask=90.5),
        _tick(t + HOUR_MS, bid=101.0, ask=101.5),
    ]
    record = _last_record(_run(m, rows, raw_ticks=raw_ticks))
    assert record["execution"]["status"] == "EXECUTED"
    assert record["execution"]["events"][0]["timestamp_ms"] == t + HOUR_MS
    assert record["execution"]["events"][0]["price"] == 101.5


def test_m5_11_long_target_delegates_to_e104_ask_execution():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    ts = rows[-1]["h1_start_ms_utc"] + HOUR_MS
    record = _last_record(_run(m, rows, raw_ticks=[_tick(ts, bid=99.0, ask=100.0)]))
    event = record["execution"]["events"][0]
    assert event["action"] == "BUY"
    assert event["price_side"] == "ASK"
    assert event["price"] == 100.0


def test_m5_12_short_target_delegates_to_e104_bid_execution():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=99.0)
    ts = rows[-1]["h1_start_ms_utc"] + HOUR_MS
    record = _last_record(_run(m, rows, raw_ticks=[_tick(ts, bid=99.0, ask=100.0)]))
    event = record["execution"]["events"][0]
    assert event["action"] == "SELL"
    assert event["price_side"] == "BID"
    assert event["price"] == 99.0


def test_m5_13_neutral_target_delegates_to_e104_close_semantics():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=100.0)
    ts = rows[-1]["h1_start_ms_utc"] + HOUR_MS
    record = _last_record(
        _run(m, rows, raw_ticks=[_tick(ts, bid=99.0, ask=100.0)], initial_position=1)
    )
    assert record["target_position"] == 0
    assert record["execution"]["status"] == "EXECUTED"
    event = record["execution"]["events"][0]
    assert event["action"] == "SELL"
    assert event["price_side"] == "BID"


def test_m5_14_same_exposure_delegates_to_hold():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    record = _last_record(_run(m, rows, initial_position=1))
    assert record["signal"] == "LONG"
    assert record["execution"] == {"status": "HOLD", "events": []}


def test_m5_15_missing_admissible_tick_preserves_not_executed():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    record = _last_record(_run(m, rows, raw_ticks=[]))
    assert record["execution"] == {"status": "NOT_EXECUTED", "events": []}


def test_m5_16_target_exposure_is_bounded():
    m = _runtime()
    result = _run(m, _rows(21))
    assert {r["target_position"] for r in result["records"]} <= {None, -1, 0, 1}


def test_m5_17_identical_inputs_are_exactly_deterministic():
    m = _runtime()
    rows = _rows(21)
    ts = rows[-1]["h1_start_ms_utc"] + HOUR_MS
    ticks = [_tick(ts, bid=99.0, ask=100.0)]
    assert _run(m, rows, raw_ticks=ticks) == _run(m, rows, raw_ticks=ticks)


def test_m5_18_missing_e103_identity_fails_closed():
    m = _runtime()
    result = _run(m, _rows(21), e1_03_identity=None)
    assert result == {"status": "BLOCKED", "reason": "E1_03_IDENTITY_MISSING"}


def test_m5_19_wrong_e103_identity_fails_closed():
    m = _runtime()
    result = _run(m, _rows(21), e1_03_identity="WRONG")
    assert result == {"status": "BLOCKED", "reason": "E1_03_IDENTITY_MISMATCH"}


def test_m5_20_missing_e104_runtime_fails_closed():
    m = _runtime()
    result = _run(m, _rows(21), e1_04_runtime=None)
    assert result == {"status": "BLOCKED", "reason": "E1_04_RUNTIME_MISSING"}


def test_m5_21_wrong_e104_runtime_identity_fails_closed():
    m = _runtime()

    class WrongE104:
        CONTRACT = "WRONG"

        @staticmethod
        def execute_transition(**kwargs):
            return {"status": "HOLD", "events": []}

    result = _run(m, _rows(21), e1_04_runtime=WrongE104)
    assert result == {"status": "BLOCKED", "reason": "E1_04_IDENTITY_MISMATCH"}


def test_m5_22_missing_e104_execution_surface_fails_closed():
    m = _runtime()

    class MissingSurface:
        CONTRACT = E1_04_CONTRACT

    result = _run(m, _rows(21), e1_04_runtime=MissingSurface)
    assert result == {"status": "BLOCKED", "reason": "E1_04_RUNTIME_SURFACE_MISSING"}


def test_m5_23_duplicate_h1_timestamp_fails_closed():
    m = _runtime()
    rows = _rows(21)
    rows[1]["h1_start_ms_utc"] = rows[0]["h1_start_ms_utc"]
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "DUPLICATE_H1_TIMESTAMP"}


def test_m5_24_non_increasing_h1_order_fails_closed():
    m = _runtime()
    rows = _rows(21)
    rows[1], rows[2] = rows[2], rows[1]
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "INVALID_H1_ORDER"}


def test_m5_25_continuity_ordinal_inconsistency_fails_closed():
    m = _runtime()
    rows = _rows(21)
    rows[10]["continuity_ordinal"] = 99
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m5_26_continuity_block_inconsistency_fails_closed():
    m = _runtime()
    rows = _rows(21)
    rows[10]["continuity_block_id"] = 8
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m5_27_nonfinite_mid_close_fails_closed():
    m = _runtime()
    rows = _rows(21)
    rows[10]["mid_close"] = math.nan
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "NONFINITE_MID_CLOSE"}


def test_m5_28_missing_critical_h1_field_fails_closed():
    m = _runtime()
    rows = _rows(21)
    del rows[10]["mid_close"]
    result = _run(m, rows)
    assert result == {"status": "BLOCKED", "reason": "MISSING_H1_FIELD"}


def test_m5_29_prohibited_features_are_exactly_disabled():
    m = _runtime()
    assert set(m.PROHIBITED_FEATURES) == PROHIBITED_FEATURES


def test_m5_30_forbidden_claims_are_exactly_bounded():
    m = _runtime()
    assert set(m.FORBIDDEN_CLAIMS) == FORBIDDEN_CLAIMS


def test_m5_31_output_contains_no_pnl_or_performance_metrics():
    m = _runtime()
    result = _run(m, _rows(21))
    forbidden_keys = {
        "pnl",
        "profit",
        "return",
        "returns",
        "equity",
        "drawdown",
        "sharpe",
        "performance",
    }
    assert not ({k.lower() for k in _all_keys(result)} & forbidden_keys)


def test_m5_32_runner_does_not_extend_e104_cost_scope_in_execution_output():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    ts = rows[-1]["h1_start_ms_utc"] + HOUR_MS
    record = _last_record(_run(m, rows, raw_ticks=[_tick(ts, bid=99.0, ask=100.0)]))
    assert set(record["execution"].keys()) == {"status", "events"}


def test_m5_33_trace_is_minimal_and_deterministically_links_t_to_lookback():
    m = _runtime()
    rows = _set_endpoint(_rows(21), first=100.0, last=101.0)
    record = _last_record(_run(m, rows))
    assert set(record.keys()) == {
        "h1_start_ms_utc",
        "signal",
        "target_position",
        "execution",
        "trace",
    }
    assert set(record["trace"].keys()) == {
        "continuity_block_id",
        "continuity_ordinal",
        "lookback_h1_start_ms_utc",
    }
    assert record["trace"]["continuity_block_id"] == rows[-1]["continuity_block_id"]
    assert record["trace"]["continuity_ordinal"] == 20
    assert record["trace"]["lookback_h1_start_ms_utc"] == rows[0]["h1_start_ms_utc"]
