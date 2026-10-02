from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SFE-02A-BREAKOUT-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(
    os.environ.get(
        "SFE_02A_RUNTIME_PATH",
        str(ROOT / "tools/sfe_02a_breakout_v1.py"),
    )
)

RUNTIME_CONTRACT = "ATDS_SFE_02A_BREAKOUT_V1_RUNTIME_V0_1"
BAR_INTERVAL = "H1"
LOOKBACK = 20
HOUR_MS = 3_600_000
BASE_MS = 1_800_000_000_000

PROHIBITED_FEATURES = {
    "PARAMETER_OPTIMIZATION",
    "PERFORMANCE_OBSERVATION",
    "BEHAVIORAL_Y_CALCULATION",
    "PNL_CALCULATION",
    "EXECUTION",
    "POSITION_STATE",
    "REGIME_FILTER",
    "ROUTER",
    "DISCRETIONARY_OVERRIDE",
    "E1_TD_DATA_CONSUMPTION",
}

FORBIDDEN_CLAIMS = {
    "BREAKOUT_V1_SUPPORTED",
    "BREAKOUT_V1_REFUTED",
    "BREAKOUT_V1_PROFITABLE",
    "ECONOMIC_EDGE",
    "ROBUST",
    "SOURCE_INDEPENDENT",
    "PRODUCTION_READY",
    "PAPER_READY",
    "BROKER_READY",
    "LIVE_READY",
    "CAPITAL_READY",
}

_CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert _CONTRACT["schema"] == "ATDS_SFE_02A_BREAKOUT_V1_MINIMAL_IMPLEMENTATION_CONTRACT_V0_1"
assert _CONTRACT["runtime_contract"] == RUNTIME_CONTRACT
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"B2A-{i:02d}" for i in range(1, 37)]
assert len(_CONTRACT["test_cases"]) == 36


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"MODULE_UNLOADABLE:{name}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("SFE_02A_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    module = _load_module(RUNTIME_PATH, "sfe_02a_breakout_v1_under_test")
    for name in (
        "CONTRACT",
        "STRATEGY_ID",
        "BAR_INTERVAL",
        "LOOKBACK",
        "PROHIBITED_FEATURES",
        "FORBIDDEN_CLAIMS",
        "run_breakout_v1",
    ):
        assert hasattr(module, name), f"SFE_02A_RUNTIME_SURFACE_MISSING:{name}"
    assert module.CONTRACT == RUNTIME_CONTRACT
    assert module.STRATEGY_ID == "BREAKOUT_V1"
    return module


def _rows(
    count,
    *,
    start=BASE_MS,
    block=7,
    close_fn=None,
    ordinal_start=0,
):
    if close_fn is None:
        close_fn = lambda i: 100.0
    return [
        {
            "bar_start_ms_utc": start + i * HOUR_MS,
            "continuity_block_id": block,
            "continuity_ordinal": ordinal_start + i,
            "close": float(close_fn(i)),
        }
        for i in range(count)
    ]


def _run(module, rows):
    return module.run_breakout_v1(rows)


def _last(result):
    assert result["status"] == "PASS"
    assert result["records"]
    return result["records"][-1]


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


def _reference(rows):
    if not isinstance(rows, list):
        return {"status": "BLOCKED", "reason": "INPUT_NOT_LIST"}

    required = ("bar_start_ms_utc", "continuity_block_id", "continuity_ordinal", "close")
    normalized = []
    for row in rows:
        if not isinstance(row, dict):
            return {"status": "BLOCKED", "reason": "ROW_NOT_OBJECT"}
        if any(k not in row for k in required):
            return {"status": "BLOCKED", "reason": "MISSING_REQUIRED_FIELD"}

        ts = row["bar_start_ms_utc"]
        close = row["close"]
        block = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]

        if isinstance(ts, bool) or not isinstance(ts, int):
            return {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_TYPE"}
        if isinstance(close, bool) or not isinstance(close, (int, float)):
            return {"status": "BLOCKED", "reason": "INVALID_CLOSE_TYPE"}
        f = float(close)
        if not math.isfinite(f):
            return {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}
        if f <= 0:
            return {"status": "BLOCKED", "reason": "NONPOSITIVE_CLOSE"}
        if isinstance(block, bool) or not isinstance(block, (str, int)):
            return {"status": "BLOCKED", "reason": "INVALID_BLOCK_ID"}
        if isinstance(ordinal, bool) or not isinstance(ordinal, int):
            return {"status": "BLOCKED", "reason": "INVALID_ORDINAL_TYPE"}

        normalized.append(
            {
                "bar_start_ms_utc": ts,
                "continuity_block_id": block,
                "continuity_ordinal": ordinal,
                "close": f,
            }
        )

    previous_ts = None
    for row in normalized:
        ts = row["bar_start_ms_utc"]
        if previous_ts is not None:
            if ts == previous_ts:
                return {"status": "BLOCKED", "reason": "DUPLICATE_TIMESTAMP"}
            if ts < previous_ts:
                return {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_ORDER"}
        previous_ts = ts

    previous_ts = None
    previous_block = None
    previous_ordinal = None
    seen = set()
    block_start = 0
    records = []

    for i, row in enumerate(normalized):
        ts = row["bar_start_ms_utc"]
        block = row["continuity_block_id"]
        ordinal = row["continuity_ordinal"]

        if i == 0:
            if ordinal != 0:
                return {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}
            seen.add(block)
            block_start = 0
        elif block == previous_block:
            if ordinal != previous_ordinal + 1:
                return {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}
            if ts != previous_ts + HOUR_MS:
                return {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}
        else:
            if block in seen or ordinal != 0:
                return {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}
            seen.add(block)
            block_start = i

        if ordinal < LOOKBACK or i - LOOKBACK < block_start:
            signal = "UNDEFINED"
            lb_start = None
            lb_end = None
        else:
            window = [x["close"] for x in normalized[i - LOOKBACK:i]]
            upper = max(window)
            lower = min(window)
            c = row["close"]
            if c > upper:
                signal = "LONG"
            elif c < lower:
                signal = "SHORT"
            else:
                signal = "NEUTRAL"
            lb_start = normalized[i - LOOKBACK]["bar_start_ms_utc"]
            lb_end = normalized[i - 1]["bar_start_ms_utc"]

        records.append(
            {
                "bar_start_ms_utc": ts,
                "signal": signal,
                "trace": {
                    "continuity_block_id": block,
                    "continuity_ordinal": ordinal,
                    "lookback_start_ms_utc": lb_start,
                    "lookback_end_ms_utc": lb_end,
                },
            }
        )

        previous_ts = ts
        previous_block = block
        previous_ordinal = ordinal

    return {"status": "PASS", "records": records}


def test_b2a_01_ordinal_19_is_undefined():
    m = _runtime()
    record = _last(_run(m, _rows(20)))
    assert record["signal"] == "UNDEFINED"


def test_b2a_02_ordinal_20_strict_upper_breach_is_long():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[-1]["close"] = 101.0
    assert _last(_run(m, rows))["signal"] == "LONG"


def test_b2a_03_ordinal_20_strict_lower_breach_is_short():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[-1]["close"] = 99.0
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_b2a_04_upper_tie_is_neutral():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0 + (i % 3))
    rows[-1]["close"] = max(r["close"] for r in rows[:20])
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_b2a_05_lower_tie_is_neutral():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0 + (i % 3))
    rows[-1]["close"] = min(r["close"] for r in rows[:20])
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_b2a_06_inside_channel_is_neutral():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0 + (i % 5))
    rows[-1]["close"] = 102.0
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_b2a_07_current_close_is_excluded_from_channel():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[-1]["close"] = 500.0
    assert _last(_run(m, rows))["signal"] == "LONG"


def test_b2a_08_oldest_exact_lookback_element_is_included():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[0]["close"] = 200.0
    rows[-1]["close"] = 150.0
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_b2a_09_bar_older_than_exact_lookback_is_excluded():
    m = _runtime()
    rows = _rows(22, close_fn=lambda i: 100.0)
    rows[0]["close"] = 1000.0
    rows[-1]["close"] = 150.0
    assert _last(_run(m, rows))["signal"] == "LONG"


def test_b2a_10_continuity_change_resets_warmup():
    m = _runtime()
    rows = _rows(20, block=7)
    rows += _rows(
        1,
        start=rows[-1]["bar_start_ms_utc"] + HOUR_MS,
        block=8,
        ordinal_start=0,
        close_fn=lambda _: 500.0,
    )
    record = _last(_run(m, rows))
    assert record["signal"] == "UNDEFINED"
    assert record["trace"]["lookback_start_ms_utc"] is None


def test_b2a_11_new_block_ordinal_20_is_first_eligible():
    m = _runtime()
    first = _rows(3, block=7)
    start = first[-1]["bar_start_ms_utc"] + HOUR_MS
    second = _rows(21, start=start, block=8, close_fn=lambda i: 100.0)
    second[-1]["close"] = 101.0
    result = _run(m, first + second)
    assert result["records"][-2]["signal"] == "UNDEFINED"
    assert result["records"][-1]["signal"] == "LONG"


def test_b2a_12_future_mutation_cannot_change_prior_signal():
    m = _runtime()
    rows = _rows(22, close_fn=lambda i: 100.0)
    rows[20]["close"] = 101.0
    baseline = _run(m, rows)
    mutated = copy.deepcopy(rows)
    mutated[21]["close"] = 1_000_000.0
    after = _run(m, mutated)
    assert baseline["records"][20] == after["records"][20]


def test_b2a_13_identical_input_is_exactly_deterministic():
    m = _runtime()
    rows = _rows(25, close_fn=lambda i: 100.0 + i)
    assert _run(m, rows) == _run(m, rows)


def test_b2a_14_missing_required_field_fails_closed():
    m = _runtime()
    rows = _rows(2)
    del rows[1]["close"]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "MISSING_REQUIRED_FIELD"}


def test_b2a_15_non_object_row_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1] = "bad"
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "ROW_NOT_OBJECT"}


def test_b2a_16_non_list_top_level_input_fails_closed():
    m = _runtime()
    assert _run(m, tuple()) == {"status": "BLOCKED", "reason": "INPUT_NOT_LIST"}


def test_b2a_17_non_numeric_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = "100"
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_CLOSE_TYPE"}


def test_b2a_18_boolean_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_CLOSE_TYPE"}


def test_b2a_19_nan_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = math.nan
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}


def test_b2a_20_infinite_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = math.inf
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}


def test_b2a_21_zero_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = 0.0
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONPOSITIVE_CLOSE"}


def test_b2a_22_negative_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = -1.0
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONPOSITIVE_CLOSE"}


def test_b2a_23_invalid_timestamp_type_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["bar_start_ms_utc"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_TYPE"}


def test_b2a_24_duplicate_timestamp_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["bar_start_ms_utc"] = rows[0]["bar_start_ms_utc"]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "DUPLICATE_TIMESTAMP"}


def test_b2a_25_decreasing_timestamp_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1], rows[2] = rows[2], rows[1]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_ORDER"}


def test_b2a_26_non_h1_step_inside_block_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1]["bar_start_ms_utc"] += 1
    rows[2]["bar_start_ms_utc"] += 1
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_b2a_27_invalid_ordinal_type_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["continuity_ordinal"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_ORDINAL_TYPE"}


def test_b2a_28_ordinal_jump_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1]["continuity_ordinal"] = 9
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_b2a_29_new_block_must_start_at_zero():
    m = _runtime()
    rows = _rows(2, block=7)
    rows += _rows(
        1,
        start=rows[-1]["bar_start_ms_utc"] + HOUR_MS,
        block=8,
        ordinal_start=1,
    )
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_b2a_30_continuity_block_cannot_reappear():
    m = _runtime()
    rows = _rows(1, block=7)
    rows += _rows(1, start=rows[-1]["bar_start_ms_utc"] + HOUR_MS, block=8)
    rows += _rows(1, start=rows[-1]["bar_start_ms_utc"] + HOUR_MS, block=7)
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_b2a_31_invalid_continuity_block_id_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["continuity_block_id"] = []
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_BLOCK_ID"}


def test_b2a_32_runtime_constants_and_prohibitions_are_exact():
    m = _runtime()
    assert m.BAR_INTERVAL == BAR_INTERVAL
    assert m.LOOKBACK == LOOKBACK
    assert set(m.PROHIBITED_FEATURES) == PROHIBITED_FEATURES
    assert set(m.FORBIDDEN_CLAIMS) == FORBIDDEN_CLAIMS


def test_b2a_33_output_contains_no_performance_execution_or_position_surface():
    m = _runtime()
    rows = _rows(25, close_fn=lambda i: 100.0 + i)
    result = _run(m, rows)
    forbidden = {
        "return",
        "returns",
        "y",
        "pnl",
        "profit",
        "performance",
        "execution",
        "order",
        "position",
        "target_position",
        "equity",
        "drawdown",
    }
    assert not ({str(k).lower() for k in _all_keys(result)} & forbidden)
    for record in result["records"]:
        assert set(record.keys()) == {"bar_start_ms_utc", "signal", "trace"}


def test_b2a_34_breakout_direction_implies_same_direction_20bar_momentum_sign():
    m = _runtime()
    corpora = []
    for direction in ("LONG", "SHORT"):
        for base in (10.0, 100.0, 1000.0):
            rows = _rows(21, close_fn=lambda i, b=base: b + (i % 4))
            if direction == "LONG":
                rows[-1]["close"] = max(r["close"] for r in rows[:20]) + 1.0
            else:
                rows[-1]["close"] = min(r["close"] for r in rows[:20]) - 1.0
            corpora.append((direction, rows))

    for direction, rows in corpora:
        record = _last(_run(m, rows))
        assert record["signal"] == direction
        momentum = float(rows[-1]["close"]) / float(rows[0]["close"]) - 1.0
        if direction == "LONG":
            assert momentum > 0
        else:
            assert momentum < 0


def test_b2a_35_trace_binds_exact_previous_20_window():
    m = _runtime()
    rows = _rows(21, close_fn=lambda i: 100.0)
    rows[-1]["close"] = 101.0
    record = _last(_run(m, rows))
    assert record["trace"] == {
        "continuity_block_id": 7,
        "continuity_ordinal": 20,
        "lookback_start_ms_utc": rows[0]["bar_start_ms_utc"],
        "lookback_end_ms_utc": rows[19]["bar_start_ms_utc"],
    }


def test_b2a_36_independent_reference_parity_on_synthetic_corpus():
    m = _runtime()
    corpora = []

    flat = _rows(25, close_fn=lambda i: 100.0)
    corpora.append(flat)

    up = _rows(25, close_fn=lambda i: 100.0 + i)
    corpora.append(up)

    down = _rows(25, close_fn=lambda i: 200.0 - i)
    corpora.append(down)

    mixed = _rows(30, close_fn=lambda i: 100.0 + ((i * 7) % 11))
    corpora.append(mixed)

    first = _rows(7, block="A", close_fn=lambda i: 50.0 + i)
    second = _rows(
        25,
        start=first[-1]["bar_start_ms_utc"] + HOUR_MS,
        block="B",
        close_fn=lambda i: 100.0 + ((i * 3) % 8),
    )
    corpora.append(first + second)

    for rows in corpora:
        assert _run(m, copy.deepcopy(rows)) == _reference(copy.deepcopy(rows))
