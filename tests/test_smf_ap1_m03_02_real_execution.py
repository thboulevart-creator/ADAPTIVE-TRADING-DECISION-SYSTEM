from __future__ import annotations

from pathlib import Path

import numpy as np

from tools import smf_ap1_m03_02_real_execution as m


def test_contract_identities():
    assert m.CONTRACT == "ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
    assert m.AP1_SHA256 == "db8963bb1bd1fa5b76a9a435fcb9b2d24781f92df0c5e53b6664bafe6235076b"
    assert m.AP0_MANIFEST_SHA256 == "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert m.EXPECTED_FILES == 61
    assert m.PARITY_FACTOR == 8.0


def test_parity_tolerance_is_machine_epsilon_derived():
    a = 100.0
    b = 100.0
    assert m.parity_tolerance(a, b) == 8.0 * m.DOUBLE_EPSILON * 100.0


def test_ap1_field_mapping():
    assert m.ap1_field("tick_count", 0.5) == "tick_count_p50"
    assert m.ap1_field("minute_range", 0.95) == "minute_range_p95"
    assert m.ap1_field("spread_mean", 0.99) == "spread_mean_p99"


def test_empty_evidence_has_no_numerical_result():
    out = m.empty_evidence("tick_count", "UTC_HOUR:00")
    assert out["status"] == "EMPTY_NO_NUMERICAL_RESULT"
    assert out["n"] == 0
    assert all(value is None for value in out["quantiles"].values())
    assert all(value is False for value in out["authority"].values())


def test_derive_codes_matches_expected_bucket_shapes():
    minute = np.array(
        [
            1609459200000,
            1609462800000,
        ],
        dtype=np.int64,
    )
    codes = m.derive_codes(minute)
    assert set(codes) == {
        "UTC_HOUR",
        "NEW_YORK_HOUR",
        "NEW_YORK_WEEKDAY",
        "NEW_YORK_WEEKDAY_HOUR",
        "UTC_YEAR",
    }
    assert len(codes["UTC_HOUR"][1]) == 24
    assert len(codes["NEW_YORK_HOUR"][1]) == 24
    assert len(codes["NEW_YORK_WEEKDAY"][1]) == 7
    assert len(codes["NEW_YORK_WEEKDAY_HOUR"][1]) == 168
    assert codes["UTC_YEAR"][1] == list(range(2021, 2027))


def test_synthetic_m03_execution_uses_exact_binding():
    minute = np.array(
        [1609459200000, 1609459260000, 1609459320000],
        dtype=np.int64,
    )
    tick = np.array([1, 2, 3], dtype=np.int64)
    minute_range = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    spread_mean = np.array([0.5, 1.0, 1.5], dtype=np.float64)
    out = m.execute_real_m03(minute, tick, minute_range, spread_mean)
    global_tick = out["bucket_evidence"]["GLOBAL"]["tick_count"]
    assert global_tick["n"] == 3
    assert global_tick["quantiles"]["0.5"] == 2.0
    assert global_tick["procedure_ref"].endswith("#ecdf_quantiles")
    assert all(value is False for value in global_tick["authority"].values())


def test_parity_check_passes_exact_equal_synthetic_values():
    ap1 = {
        "global": {
            "tick_count_p50": 2.0,
            "tick_count_p90": 2.8,
            "tick_count_p99": 2.98,
            "minute_range_p50": 2.0,
            "minute_range_p90": 2.8,
            "minute_range_p95": 2.9,
            "minute_range_p99": 2.98,
            "spread_mean_p50": 1.0,
            "spread_mean_p90": 1.4,
            "spread_mean_p95": 1.45,
            "spread_mean_p99": 1.49,
        },
        "utc_hour": [],
        "new_york_hour": [],
        "new_york_weekday": [],
        "new_york_weekday_hour": [],
        "utc_year": [],
    }
    evidence = {
        "GLOBAL": {
            "tick_count": {"quantiles": {"0.5": 2.0, "0.9": 2.8, "0.99": 2.98}},
            "minute_range": {"quantiles": {"0.5": 2.0, "0.9": 2.8, "0.95": 2.9, "0.99": 2.98}},
            "spread_mean": {"quantiles": {"0.5": 1.0, "0.9": 1.4, "0.95": 1.45, "0.99": 1.49}},
        }
    }
    result = m.parity_check(ap1, evidence)
    assert result["overall"] == "PASS"
    assert result["fail_count"] == 0


def test_source_contains_no_ap1_main_invocation():
    source = Path(m.__file__).read_text(encoding="utf-8")
    assert "ap1_intraday_spread_census.py" not in source
    assert "subprocess.run" not in source
