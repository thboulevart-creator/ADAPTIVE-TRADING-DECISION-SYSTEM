from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SFE-02F-IMPLEMENTATION-EXECUTION-READINESS-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(
    os.environ.get(
        "SFE_02F_RUNTIME_PATH",
        str(ROOT / "tools/sfe_02f_structural_continuity.py"),
    )
)

RUNTIME_CONTRACT = "ATDS_SFE_02F_STRUCTURAL_CONTINUITY_RUNTIME_V0_1"
HOUR_MS = 3_600_000
WARMUP = 20
BASE_MS = 1_800_000_000_000

ALLOWED_FIELDS = {
    "h1_start_ms_utc",
    "source_segment_id",
    "continuity_block_id",
    "continuity_ordinal",
    "mid_close",
}
FORBIDDEN_OUTPUT_KEYS = {
    "signal",
    "strategy_signal",
    "strategy_event",
    "strategy_event_membership",
    "y",
    "theta",
    "ci",
    "pnl",
    "trade",
    "position",
    "execution",
    "return",
    "abs_return",
    "volatility",
    "zscore",
    "range",
    "atr",
    "optimization",
    "ranking",
    "router",
}

_CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert _CONTRACT["schema"] == "ATDS_SFE_02F_IMPLEMENTATION_EXECUTION_READINESS_CONTRACT_V0_1"
assert _CONTRACT["runtime_contract"] == RUNTIME_CONTRACT
assert [x[0] for x in _CONTRACT["test_cases"]] == [f"F2R-{i:02d}" for i in range(1, 32)]
assert len(_CONTRACT["test_cases"]) == 31


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"MODULE_UNLOADABLE:{name}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    if not RUNTIME_PATH.is_file():
        pytest.fail("SFE_02F_RUNTIME_ABSENT_EXPECTED_RED", pytrace=False)
    module = _load_module(RUNTIME_PATH, "sfe_02f_structural_continuity_under_test")
    for name in (
        "CONTRACT",
        "HOUR_MS",
        "WARMUP_H1",
        "ALLOWED_ROW_FIELDS",
        "ROW_LEVEL_UPSTREAM_CLASSIFICATION",
        "FROZEN_CALENDAR_IDENTITY",
        "CANONICAL_DATASET_IDENTITY",
        "FORBIDDEN_OUTPUT_KEYS",
        "verify_calendar_identity",
        "verify_canonical_dataset_identity",
        "profile_structural_geometry",
    ):
        assert hasattr(module, name), f"SFE_02F_RUNTIME_SURFACE_MISSING:{name}"
    assert module.CONTRACT == RUNTIME_CONTRACT
    return module


def _rows(length, *, block="A", source="S1", start=BASE_MS, close=100.0):
    return [
        {
            "h1_start_ms_utc": start + i * HOUR_MS,
            "source_segment_id": source,
            "continuity_block_id": block,
            "continuity_ordinal": i,
            "mid_close": float(close),
        }
        for i in range(length)
    ]


def _join(first, second, *, step_ms=HOUR_MS):
    second = copy.deepcopy(second)
    if first and second:
        shift = first[-1]["h1_start_ms_utc"] + step_ms - second[0]["h1_start_ms_utc"]
        for row in second:
            row["h1_start_ms_utc"] += shift
    return copy.deepcopy(first) + second


def _profile(module, rows):
    return module.profile_structural_geometry(rows)


def _pass_profile(module, rows):
    result = _profile(module, rows)
    assert result["status"] == "SYNTHETIC_PROFILE_PRODUCED"
    assert result["authority"] == "SYNTHETIC_ONLY"
    return result["profile"]


def _all_keys(value):
    keys = set()
    if isinstance(value, dict):
        keys.update(str(k).lower() for k in value.keys())
        for item in value.values():
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return keys


def _canonical_identity():
    return copy.deepcopy(_CONTRACT["canonical_dataset_identity"])


def test_f2r_01_contiguous_same_block_transition():
    m = _runtime()
    p = _pass_profile(m, _rows(3))
    assert p["N_ROWS"] == 3
    assert p["N_BLOCKS"] == 1
    assert p["N_INTERNAL_BOUNDARIES"] == 0


def test_f2r_02_source_change_only_classification():
    m = _runtime()
    rows = _join(_rows(2, block="A", source="S1"), _rows(2, block="B", source="S2"))
    p = _pass_profile(m, rows)
    assert p["BOUNDARY_MECHANISM_COUNTS"]["SOURCE_SEGMENT_CHANGE_ONLY"] == 1
    assert p["BOUNDARY_MECHANISM_COUNTS"]["SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP"] == 0


def test_f2r_03_source_change_plus_gap_classification():
    m = _runtime()
    rows = _join(_rows(2, block="A", source="S1"), _rows(2, block="B", source="S2"), step_ms=2 * HOUR_MS)
    p = _pass_profile(m, rows)
    assert p["BOUNDARY_MECHANISM_COUNTS"]["SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP"] == 1


def test_f2r_04_temporal_gap_within_source_stops():
    m = _runtime()
    rows = _join(_rows(2, block="A", source="S1"), _rows(2, block="B", source="S1"), step_ms=2 * HOUR_MS)
    assert _profile(m, rows) == {
        "status": "BLOCKED",
        "reason": "BLOCKED_UPSTREAM_SEMANTICS_DISCREPANCY",
    }


def test_f2r_05_block_id_reuse_a_b_a_fails_closed():
    m = _runtime()
    a1 = _rows(1, block="A", source="S1")
    b = _join(a1, _rows(1, block="B", source="S2"))[1:]
    ab = a1 + b
    a2 = _join(ab, _rows(1, block="A", source="S3"))[-1:]
    assert _profile(m, ab + a2) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_06_block_change_without_trigger_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["continuity_block_id"] = "B"
    rows[1]["continuity_ordinal"] = 0
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_07_trigger_without_block_change_fails_closed():
    m = _runtime()
    rows = _rows(2)
    rows[1]["source_segment_id"] = "S2"
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_08_first_row_ordinal_must_be_zero():
    m = _runtime()
    rows = _rows(2)
    rows[0]["continuity_ordinal"] = 1
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_09_dataset_truncation_markers_are_explicit():
    m = _runtime()
    p = _pass_profile(m, _rows(3))
    assert p["N_DATASET_START_TRUNCATED_BLOCKS"] == 1
    assert p["N_DATASET_END_TRUNCATED_BLOCKS"] == 1
    assert p["N_DATASET_END_TERMINALS"] == 1
    assert p["DATASET_START_TRUNCATION_BLOCK_ID"] == "A"
    assert p["DATASET_END_TRUNCATION_BLOCK_ID"] == "A"


@pytest.mark.parametrize(
    ("case_id", "length", "mature", "with_t1"),
    [
        ("F2R-10", 1, 0, 0),
        ("F2R-11", 20, 0, 0),
        ("F2R-12", 21, 1, 0),
        ("F2R-13", 22, 2, 1),
        ("F2R-14", 100, 80, 79),
    ],
)
def test_f2r_10_to_14_block_length_identities(case_id, length, mature, with_t1):
    del case_id
    m = _runtime()
    p = _pass_profile(m, _rows(length))
    assert p["N_WARMUP_MATURE_ROWS"] == mature
    assert p["N_WARMUP_MATURE_ROWS_WITH_SAME_BLOCK_T1"] == with_t1
    assert p["BLOCK_LENGTH_HISTOGRAM_EXACT"] == {str(length): 1}


def test_f2r_15_exact_calendar_identity_passes():
    m = _runtime()
    result = m.verify_calendar_identity()
    assert result["status"] == "PASS"
    assert result["identity"] == m.FROZEN_CALENDAR_IDENTITY


def test_f2r_16_calendar_identity_mismatch_blocks(monkeypatch):
    m = _runtime()
    original = m._observed_calendar_identity

    def bad_identity():
        value = original()
        value["iana_tzdb_release"] = "MISMATCH"
        return value

    monkeypatch.setattr(m, "_observed_calendar_identity", bad_identity)
    assert m.verify_calendar_identity() == {
        "status": "BLOCKED",
        "reason": "BLOCKED_CALENDAR_IDENTITY",
    }
    assert _profile(m, _rows(2)) == {
        "status": "BLOCKED",
        "reason": "BLOCKED_CALENDAR_IDENTITY",
    }


def test_f2r_17_dst_annotation_crosses_spring_transition():
    m = _runtime()
    boundary_ms = 1_772_953_200_000
    first = _rows(1, block="A", source="S1", start=boundary_ms - HOUR_MS)
    second = _rows(1, block="B", source="S2", start=boundary_ms)
    p = _pass_profile(m, first + second)
    rows = p["BOUNDARY_CALENDAR_ROWS"]
    assert len(rows) == 1
    assert rows[0]["B_T_MS_UTC"] == boundary_ms
    assert rows[0]["NY_UTC_OFFSET_SECONDS"] == -14_400
    assert rows[0]["NY_DST_STATE"] == "DST"
    assert rows[0]["NY_LOCAL_HOUR"] == 3


def test_f2r_18_row_level_source_b_label_attempt_is_rejected():
    m = _runtime()
    rows = _rows(2)
    rows[0]["source_b_classification"] = "HISTORICAL_UNKNOWN_GAP"
    result = _profile(m, rows)
    assert result == {"status": "BLOCKED", "reason": "BLOCKED_FORBIDDEN_INPUT_SURFACE"}
    assert m.ROW_LEVEL_UPSTREAM_CLASSIFICATION == "UNRESOLVED"


@pytest.mark.parametrize("field", ["signal", "Y", "PnL"])
def test_f2r_19_to_21_strategy_y_pnl_inputs_are_rejected(field):
    m = _runtime()
    rows = _rows(2)
    rows[0][field] = 1
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_FORBIDDEN_INPUT_SURFACE"}


def test_f2r_22_mid_close_is_domain_only_and_profile_invariant():
    m = _runtime()
    baseline = _profile(m, _rows(25, close=100.0))
    mutated_rows = _rows(25, close=100.0)
    for i, row in enumerate(mutated_rows):
        row["mid_close"] = float(1 + i * 1000)
    mutated = _profile(m, mutated_rows)
    assert baseline == mutated


@pytest.mark.parametrize("bad", [0.0, -1.0, math.nan, math.inf])
def test_f2r_23_bad_mid_close_blocks_dataset_identity(bad):
    m = _runtime()
    rows = _rows(2)
    rows[1]["mid_close"] = bad
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_DATASET_IDENTITY"}


def test_f2r_24_identical_input_replay_is_exact():
    m = _runtime()
    rows = _rows(30)
    assert _profile(m, rows) == _profile(m, copy.deepcopy(rows))


def test_f2r_25_output_has_no_forbidden_strategy_or_performance_surface():
    m = _runtime()
    result = _profile(m, _rows(30))
    keys = _all_keys(result)
    assert not (keys & FORBIDDEN_OUTPUT_KEYS)
    assert set(m.FORBIDDEN_OUTPUT_KEYS) == FORBIDDEN_OUTPUT_KEYS


def test_f2r_26_type7_quantiles_are_frozen():
    m = _runtime()
    lengths = [1, 2, 3, 4]
    rows = []
    for i, length in enumerate(lengths):
        block = chr(ord("A") + i)
        source = f"S{i}"
        part = _rows(length, block=block, source=source)
        rows = part if not rows else _join(rows, part)
    p = _pass_profile(m, rows)
    assert p["BLOCK_LENGTH_Q25"] == 1.75
    assert p["BLOCK_LENGTH_MEDIAN"] == 2.5
    assert p["BLOCK_LENGTH_Q75"] == 3.25


def test_f2r_27_exact_canonical_dataset_identity_metadata_passes():
    m = _runtime()
    identity = _canonical_identity()
    assert m.verify_canonical_dataset_identity(identity) == {"status": "PASS"}


def test_f2r_28_canonical_dataset_identity_metadata_mismatch_blocks():
    m = _runtime()
    identity = _canonical_identity()
    identity["rows"] += 1
    assert m.verify_canonical_dataset_identity(identity) == {
        "status": "BLOCKED",
        "reason": "BLOCKED_DATASET_IDENTITY",
    }


def test_f2r_29_ordinal_jump_within_block_fails_closed():
    m = _runtime()
    rows = _rows(3)
    rows[2]["continuity_ordinal"] = 9
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_30_new_block_ordinal_must_reset_zero():
    m = _runtime()
    rows = _join(_rows(2, block="A", source="S1"), _rows(2, block="B", source="S2"))
    rows[2]["continuity_ordinal"] = 1
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_CANONICAL_INTEGRITY"}


def test_f2r_31_row_schema_is_exact():
    m = _runtime()
    assert set(m.ALLOWED_ROW_FIELDS) == ALLOWED_FIELDS
    rows = _rows(2)
    del rows[0]["mid_close"]
    assert _profile(m, rows) == {"status": "BLOCKED", "reason": "BLOCKED_DATASET_IDENTITY"}
