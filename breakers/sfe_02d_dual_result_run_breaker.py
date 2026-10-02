from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "tools/sfe_02d_dual_result_run.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("sfe02d_runner_under_test", RUNNER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _synthetic_surface(blocks=30, events_per_block=20):
    r = _load_runner()
    total_events = blocks * events_per_block
    total_rows = 20 + total_events + 1

    closes = [100.0]
    for i in range(total_rows - 1):
        if i < 20:
            ret = 0.0002
        else:
            block = (i - 20) // 20
            magnitude = 0.001 + block * 0.00001
            ret = magnitude if i % 2 == 0 else -magnitude
        closes.append(closes[-1] * (1.0 + ret))

    h1 = []
    for i, close in enumerate(closes):
        h1.append(
            {
                "h1_start_ms_utc": 2_000_000_000_000 + i * r.HOUR_MS,
                "source_segment_id": 1,
                "continuity_block_id": 1,
                "continuity_ordinal": i,
                "mid_close": close,
            }
        )

    supported_records = []
    refuted_records = []
    neutral_records = []
    for i, row in enumerate(h1):
        if i < 20 or i == len(h1) - 1:
            supported_signal = "UNDEFINED"
            refuted_signal = "UNDEFINED"
        else:
            up = h1[i + 1]["mid_close"] > row["mid_close"]
            supported_signal = "LONG" if up else "SHORT"
            refuted_signal = "SHORT" if up else "LONG"

        supported_records.append(
            {
                "bar_start_ms_utc": row["h1_start_ms_utc"],
                "signal": supported_signal,
                "trace": {},
            }
        )
        refuted_records.append(
            {
                "bar_start_ms_utc": row["h1_start_ms_utc"],
                "signal": refuted_signal,
                "trace": {},
            }
        )
        neutral_records.append(
            {
                "bar_start_ms_utc": row["h1_start_ms_utc"],
                "signal": "NEUTRAL",
                "trace": {},
            }
        )

    return r, h1, supported_records, refuted_records, neutral_records


def test_sfe02d_01_cluster_jackknife_supported_surface():
    r, h1, supported, _, _ = _synthetic_surface()
    env = r._build_family_envelope(
        "TEST",
        "TEST_SUPPORTED",
        "blob",
        {"status": "PASS", "records": supported},
        h1,
        r._unconditional_drift(h1),
    )
    assert env["evidence"]["valid_directional_events"] == 600
    assert env["evidence"]["valid_LONG"] == 300
    assert env["evidence"]["valid_SHORT"] == 300
    assert env["evidence"]["event_bearing_inference_blocks"] == 30
    assert all(env["evidence"]["gates"].values())
    assert env["primary"]["theta"] > 0
    assert env["primary"]["se_cluster_jackknife"] > 0
    assert env["primary"]["status"] == "SUPPORTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE"


def test_sfe02d_02_cluster_jackknife_refuted_surface():
    r, h1, _, refuted, _ = _synthetic_surface()
    env = r._build_family_envelope(
        "TEST",
        "TEST_REFUTED",
        "blob",
        {"status": "PASS", "records": refuted},
        h1,
        r._unconditional_drift(h1),
    )
    assert env["primary"]["theta"] < 0
    assert env["primary"]["ci_upper"] <= 0
    assert env["primary"]["status"] == "REFUTED_ON_THIS_EXPLORATORY_E1_EXPOSED_SURFACE"


def test_sfe02d_03_insufficient_evidence_is_not_interpretable():
    r, h1, supported, _, _ = _synthetic_surface(blocks=2)
    env = r._build_family_envelope(
        "TEST",
        "TEST_SMALL",
        "blob",
        {"status": "PASS", "records": supported},
        h1,
        r._unconditional_drift(h1),
    )
    assert not all(env["evidence"]["gates"].values())
    assert env["primary"]["status"] == "NOT_INTERPRETABLE / INSUFFICIENT_EVIDENCE"


def test_sfe02d_04_t1_end_of_continuity_is_excluded():
    r, h1, supported, _, _ = _synthetic_surface()
    split = 200
    for i in range(split, len(h1)):
        h1[i]["continuity_block_id"] = 2
        h1[i]["continuity_ordinal"] = i - split
    supported[split - 1]["signal"] = "LONG"
    env = r._build_family_envelope(
        "TEST",
        "TEST_EXCLUSION",
        "blob",
        {"status": "PASS", "records": supported},
        h1,
        r._unconditional_drift(h1),
    )
    assert env["diagnostics"]["t1_exclusions"]["by_reason"]["END_OF_CONTINUITY_BLOCK"] >= 1


def test_sfe02d_05_cofiring_categories_distinguish_neutral_and_undefined():
    r = _load_runner()
    def rec(signal):
        return {"bar_start_ms_utc": 1, "signal": signal, "trace": {}}
    b = [rec("LONG"), rec("SHORT"), rec("NEUTRAL"), rec("UNDEFINED"), rec("LONG")]
    m = [rec("SHORT"), rec("NEUTRAL"), rec("LONG"), rec("SHORT"), rec("UNDEFINED")]
    c = r._cofiring(b, m)
    assert c == {
        "N_BREAKOUT_DIRECTIONAL": 3,
        "N_MEAN_REVERSION_DIRECTIONAL": 3,
        "N_CO_FIRING": 1,
        "N_BREAKOUT_EXCLUSIVE_OTHER_NEUTRAL": 1,
        "N_BREAKOUT_EXCLUSIVE_OTHER_UNDEFINED": 1,
        "N_MEAN_REVERSION_EXCLUSIVE_OTHER_NEUTRAL": 1,
        "N_MEAN_REVERSION_EXCLUSIVE_OTHER_UNDEFINED": 1,
    }


def test_sfe02d_06_atomic_json_is_deterministic_and_no_nan(tmp_path):
    r = _load_runner()
    path = tmp_path / "x.json"
    h1 = r._atomic_json(path, {"b": 2, "a": 1})
    raw = path.read_bytes()
    assert raw == b'{\n  "a": 1,\n  "b": 2\n}\n'
    assert h1 == r._sha256(raw)
    with pytest.raises(ValueError):
        r._atomic_json(tmp_path / "bad.json", {"x": math.nan})


def test_sfe02d_07_git_blob_hash_matches_known_vector():
    r = _load_runner()
    assert r._git_blob_sha1(b"test\n") == "9daeafb9864cf43055ae93beb0afd6c7d144bfa4"


def test_sfe02d_08_same_next_requires_all_three_continuity_conditions():
    r = _load_runner()
    row = {
        "h1_start_ms_utc": 1000,
        "continuity_block_id": 1,
        "continuity_ordinal": 5,
        "mid_close": 100.0,
    }
    nxt = {
        "h1_start_ms_utc": 1000 + r.HOUR_MS,
        "continuity_block_id": 1,
        "continuity_ordinal": 6,
        "mid_close": 101.0,
    }
    assert r._same_next(row, nxt)
    bad = dict(nxt)
    bad["continuity_ordinal"] = 7
    assert not r._same_next(row, bad)


def test_sfe02d_09_output_has_no_pnl_or_execution_claims():
    r, h1, supported, _, _ = _synthetic_surface()
    env = r._build_family_envelope(
        "TEST",
        "TEST_NO_PNL",
        "blob",
        {"status": "PASS", "records": supported},
        h1,
        r._unconditional_drift(h1),
    )
    text = json.dumps(env).lower()
    assert '"pnl"' not in text
    assert '"profitability"' in text
    assert "execution_price" not in text


def test_sfe02d_10_primary_surface_is_all_valid_directional_events():
    r, h1, supported, _, _ = _synthetic_surface()
    env = r._build_family_envelope(
        "TEST",
        "TEST_PRIMARY",
        "blob",
        {"status": "PASS", "records": supported},
        h1,
        r._unconditional_drift(h1),
    )
    assert env["primary"]["surface"] == "ALL_VALID_DIRECTIONAL_EVENTS"
    assert env["primary"]["reference"] == "RAW_ZERO"
