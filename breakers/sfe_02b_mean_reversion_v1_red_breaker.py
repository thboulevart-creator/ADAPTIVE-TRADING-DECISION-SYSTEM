from __future__ import annotations

import copy
from decimal import Decimal, getcontext
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SFE-02B-MEAN-REVERSION-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(
    os.environ.get(
        "SFE_02B_RUNTIME_PATH",
        str(ROOT / "tools/sfe_02b_mean_reversion_v1.py"),
    )
)

RUNTIME_CONTRACT = "ATDS_SFE_02B_MEAN_REVERSION_V1_RUNTIME_V0_1"
BAR_INTERVAL = "H1"
LOOKBACK = 20
Z_THRESHOLD = 1.0
SIGMA_DENOMINATOR = 20
HOUR_MS = 3_600_000
BASE_MS = 1_810_000_000_000

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
    "BREAKOUT_PERFORMANCE_CONSUMPTION",
    "E1_TD_DATA_CONSUMPTION",
}

FORBIDDEN_CLAIMS = {
    "MEAN_REVERSION_V1_SUPPORTED",
    "MEAN_REVERSION_V1_REFUTED",
    "MEAN_REVERSION_V1_PROFITABLE",
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
assert _CONTRACT["schema"] == "ATDS_SFE_02B_MEAN_REVERSION_V1_MINIMAL_IMPLEMENTATION_CONTRACT_V0_1"
assert _CONTRACT["runtime_contract"] == RUNTIME_CONTRACT
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"M2B-{i:02d}" for i in range(1, 43)]
assert len(_CONTRACT["test_cases"]) == 42


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"MODULE_UNLOADABLE:{name}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("SFE_02B_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    module = _load_module(RUNTIME_PATH, "sfe_02b_mean_reversion_v1_under_test")
    for name in (
        "CONTRACT",
        "STRATEGY_ID",
        "BAR_INTERVAL",
        "LOOKBACK",
        "Z_THRESHOLD",
        "SIGMA_DENOMINATOR",
        "MEAN_ALGORITHM",
        "SIGMA_ALGORITHM",
        "ZERO_SIGMA_RULE",
        "PROHIBITED_FEATURES",
        "FORBIDDEN_CLAIMS",
        "run_mean_reversion_v1",
    ):
        assert hasattr(module, name), f"SFE_02B_RUNTIME_SURFACE_MISSING:{name}"
    assert module.CONTRACT == RUNTIME_CONTRACT
    assert module.STRATEGY_ID == "MEAN_REVERSION_V1"
    return module


def _rows(
    count,
    *,
    start=BASE_MS,
    block=7,
    close_fn=None,
    ordinal_start=0,
    as_float=True,
):
    if close_fn is None:
        close_fn = lambda i: 100.0
    out = []
    for i in range(count):
        value = close_fn(i)
        if as_float:
            value = float(value)
        out.append(
            {
                "bar_start_ms_utc": start + i * HOUR_MS,
                "continuity_block_id": block,
                "continuity_ordinal": ordinal_start + i,
                "close": value,
            }
        )
    return out


def _balanced_window():
    return [99.0] * 10 + [101.0] * 10


def _rows_from_window(window, current, *, start=BASE_MS, block=7):
    rows = _rows(len(window) + 1, start=start, block=block)
    for i, value in enumerate(window):
        rows[i]["close"] = value
    rows[-1]["close"] = current
    return rows


def _run(module, rows):
    return module.run_mean_reversion_v1(rows)


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


def _decimal_signal(window, current):
    getcontext().prec = 80
    values = [Decimal(str(float(x))) for x in window]
    c = Decimal(str(float(current)))
    n = Decimal(20)
    mu = sum(values, Decimal(0)) / n
    variance = sum(((x - mu) * (x - mu) for x in values), Decimal(0)) / n
    if variance == 0:
        return "UNDEFINED"
    sigma = variance.sqrt()
    z = (c - mu) / sigma
    if z <= Decimal("-1"):
        return "LONG"
    if z >= Decimal("1"):
        return "SHORT"
    return "NEUTRAL"


def test_m2b_01_ordinal_19_is_undefined():
    m = _runtime()
    assert _last(_run(m, _rows(20)))["signal"] == "UNDEFINED"


def test_m2b_02_exact_upper_z_threshold_is_short():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 101.0)
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_m2b_03_exact_lower_z_threshold_is_long():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 99.0)
    assert _last(_run(m, rows))["signal"] == "LONG"


def test_m2b_04_immediately_below_upper_threshold_is_neutral():
    m = _runtime()
    current = math.nextafter(101.0, 100.0)
    rows = _rows_from_window(_balanced_window(), current)
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_m2b_05_immediately_above_lower_threshold_is_neutral():
    m = _runtime()
    current = math.nextafter(99.0, 100.0)
    rows = _rows_from_window(_balanced_window(), current)
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_m2b_06_inside_z_band_is_neutral():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 100.25)
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_m2b_07_exact_zero_sigma_is_undefined():
    m = _runtime()
    rows = _rows_from_window([100.0] * 20, 101.0)
    assert _last(_run(m, rows))["signal"] == "UNDEFINED"


def test_m2b_08_current_close_is_excluded_from_reference_statistics():
    m = _runtime()
    window = [99.0] * 10 + [101.0] * 10
    rows = _rows_from_window(window, 101.0)
    assert rows[0]["close"] == 99.0
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_m2b_09_oldest_exact_lookback_element_is_included():
    m = _runtime()
    window = [90.0] + [100.0] * 19
    rows = _rows_from_window(window, 100.5)
    assert _last(_run(m, rows))["signal"] == "NEUTRAL"


def test_m2b_10_bar_older_than_exact_lookback_is_excluded():
    m = _runtime()
    rows = _rows(22)
    rows[0]["close"] = 1.0
    for i, value in enumerate(_balanced_window(), start=1):
        rows[i]["close"] = value
    rows[-1]["close"] = 101.0
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_m2b_11_population_denominator_20_not_sample_19():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 101.01)
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_m2b_12_continuity_change_resets_warmup():
    m = _runtime()
    rows = _rows(20, block=7, close_fn=lambda i: 99.0 if i % 2 == 0 else 101.0)
    rows += _rows(
        1,
        start=rows[-1]["bar_start_ms_utc"] + HOUR_MS,
        block=8,
        ordinal_start=0,
        close_fn=lambda _: 200.0,
    )
    record = _last(_run(m, rows))
    assert record["signal"] == "UNDEFINED"
    assert record["trace"]["lookback_start_ms_utc"] is None


def test_m2b_13_new_block_ordinal_20_is_first_eligible():
    m = _runtime()
    first = _rows(3, block=7)
    start = first[-1]["bar_start_ms_utc"] + HOUR_MS
    second = _rows_from_window(_balanced_window(), 101.0, start=start, block=8)
    result = _run(m, first + second)
    assert result["records"][-2]["signal"] == "UNDEFINED"
    assert result["records"][-1]["signal"] == "SHORT"


def test_m2b_14_future_mutation_cannot_change_prior_signal():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 101.0)
    rows.append(
        {
            "bar_start_ms_utc": rows[-1]["bar_start_ms_utc"] + HOUR_MS,
            "continuity_block_id": 7,
            "continuity_ordinal": 21,
            "close": 100.0,
        }
    )
    baseline = _run(m, rows)
    mutated = copy.deepcopy(rows)
    mutated[-1]["close"] = 1_000_000.0
    after = _run(m, mutated)
    assert baseline["records"][20] == after["records"][20]


def test_m2b_15_identical_input_is_exactly_deterministic():
    m = _runtime()
    rows = _rows(30, close_fn=lambda i: 100.0 + ((i * 7) % 13))
    assert _run(m, rows) == _run(m, rows)


def test_m2b_16_missing_required_field_fails_closed():
    m = _runtime()
    rows = _rows(2)
    del rows[1]["close"]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "MISSING_REQUIRED_FIELD"}


def test_m2b_17_non_object_row_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1] = "bad"
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "ROW_NOT_OBJECT"}


def test_m2b_18_non_list_top_level_input_fails_closed():
    m = _runtime()
    assert _run(m, tuple()) == {"status": "BLOCKED", "reason": "INPUT_NOT_LIST"}


def test_m2b_19_non_numeric_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = "100"
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_CLOSE_TYPE"}


def test_m2b_20_boolean_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_CLOSE_TYPE"}


def test_m2b_21_nan_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = math.nan
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}


def test_m2b_22_infinite_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = math.inf
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}


def test_m2b_23_binary64_conversion_overflow_fails_closed():
    m = _runtime()
    rows = _rows(2, as_float=False)
    rows[1]["close"] = 10 ** 400
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONFINITE_CLOSE"}


def test_m2b_24_zero_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = 0.0
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONPOSITIVE_CLOSE"}


def test_m2b_25_negative_close_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["close"] = -1.0
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "NONPOSITIVE_CLOSE"}


def test_m2b_26_invalid_timestamp_type_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["bar_start_ms_utc"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_TYPE"}


def test_m2b_27_duplicate_timestamp_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["bar_start_ms_utc"] = rows[0]["bar_start_ms_utc"]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "DUPLICATE_TIMESTAMP"}


def test_m2b_28_decreasing_timestamp_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1], rows[2] = rows[2], rows[1]
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_TIMESTAMP_ORDER"}


def test_m2b_29_non_h1_step_inside_block_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1]["bar_start_ms_utc"] += 1
    rows[2]["bar_start_ms_utc"] += 1
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m2b_30_invalid_ordinal_type_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["continuity_ordinal"] = True
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_ORDINAL_TYPE"}


def test_m2b_31_ordinal_jump_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[1]["continuity_ordinal"] = 9
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m2b_32_new_block_must_start_at_zero():
    m = _runtime()
    rows = _rows(2, block=7)
    rows += _rows(
        1,
        start=rows[-1]["bar_start_ms_utc"] + HOUR_MS,
        block=8,
        ordinal_start=1,
    )
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m2b_33_continuity_block_cannot_reappear():
    m = _runtime()
    rows = _rows(1, block=7)
    rows += _rows(1, start=rows[-1]["bar_start_ms_utc"] + HOUR_MS, block=8)
    rows += _rows(1, start=rows[-1]["bar_start_ms_utc"] + HOUR_MS, block=7)
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "CONTINUITY_INCOHERENT"}


def test_m2b_34_invalid_continuity_block_id_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["continuity_block_id"] = []
    assert _run(m, rows) == {"status": "BLOCKED", "reason": "INVALID_BLOCK_ID"}


def test_m2b_35_integer_and_equivalent_float_closes_normalize_identically():
    m = _runtime()
    ints = _rows_from_window([99] * 10 + [101] * 10, 101)
    floats = _rows_from_window([99.0] * 10 + [101.0] * 10, 101.0)
    for row in ints:
        row["close"] = int(row["close"])
    assert _run(m, ints) == _run(m, floats)


def test_m2b_36_runtime_constants_numerical_semantics_and_prohibitions_are_exact():
    m = _runtime()
    assert m.BAR_INTERVAL == BAR_INTERVAL
    assert m.LOOKBACK == LOOKBACK
    assert m.Z_THRESHOLD == Z_THRESHOLD
    assert m.SIGMA_DENOMINATOR == SIGMA_DENOMINATOR
    assert m.MEAN_ALGORITHM == "FSUM_DIVIDED_TERMS"
    assert m.SIGMA_ALGORITHM == "SCALED_TWO_PASS_POPULATION"
    assert m.ZERO_SIGMA_RULE == "EXACT_ZERO_UNDEFINED"
    assert set(m.PROHIBITED_FEATURES) == PROHIBITED_FEATURES
    assert set(m.FORBIDDEN_CLAIMS) == FORBIDDEN_CLAIMS


def test_m2b_37_output_contains_no_numeric_reference_performance_execution_or_position_surface():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 101.0)
    result = _run(m, rows)
    forbidden = {
        "mean",
        "mu",
        "sigma",
        "variance",
        "z",
        "z_score",
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


def test_m2b_38_trace_binds_exact_previous_20_window():
    m = _runtime()
    rows = _rows_from_window(_balanced_window(), 101.0)
    record = _last(_run(m, rows))
    assert record["trace"] == {
        "continuity_block_id": 7,
        "continuity_ordinal": 20,
        "lookback_start_ms_utc": rows[0]["bar_start_ms_utc"],
        "lookback_end_ms_utc": rows[19]["bar_start_ms_utc"],
    }


def test_m2b_39_independent_decimal_reference_parity_on_safe_synthetic_corpus():
    m = _runtime()
    corpora = [
        ([99.0] * 10 + [101.0] * 10, 103.0),
        ([99.0] * 10 + [101.0] * 10, 97.0),
        ([90.0, 95.0, 100.0, 105.0, 110.0] * 4, 100.0),
        ([100.0 + (i % 7) for i in range(20)], 115.0),
        ([200.0 - (i % 9) for i in range(20)], 180.0),
    ]
    for window, current in corpora:
        expected = _decimal_signal(window, current)
        observed = _last(_run(m, _rows_from_window(window, current)))["signal"]
        assert observed == expected


def test_m2b_40_very_large_finite_positive_closes_are_interpretable():
    m = _runtime()
    window = [9.0e307] * 10 + [1.1e308] * 10
    rows = _rows_from_window(window, 1.1e308)
    assert _last(_run(m, rows))["signal"] == "SHORT"


def test_m2b_41_near_zero_nonzero_sigma_uses_no_hidden_epsilon():
    m = _runtime()
    hi = math.nextafter(1.0, 2.0)
    current = math.nextafter(hi, 2.0)
    window = [1.0] * 10 + [hi] * 10
    rows = _rows_from_window(window, current)
    signal = _last(_run(m, rows))["signal"]
    assert signal != "UNDEFINED"
    assert signal == "SHORT"


def test_m2b_42_steady_trend_displacement_can_be_directional():
    m = _runtime()
    window = [float(i) for i in range(101, 121)]
    rows = _rows_from_window(window, 121.0)
    assert _last(_run(m, rows))["signal"] == "SHORT"
