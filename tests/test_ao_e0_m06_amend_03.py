from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

def load(name, rel):
    p = ROOT / rel
    s = importlib.util.spec_from_file_location(name, p)
    assert s and s.loader
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def j(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

M06 = load("m06v02", "tools/ao_e0_b8_m06_02_reference_planning_v0_2.py")
DATA = load("data01v02", "tools/ao_e0_b12_data01_formation_v0_2.py")
DR = load("dr01v02", "tools/ao_e0_b8_dr_01_decision_rule_v0_2.py")
TC = load("tc01v02", "tools/ao_e0_b12_data01_tc01_count_only_v0_2.py")
REF = load("tc01refv02", "tools/ao_e0_b12_data01_tc01_reference_v0_2.py")

M06C = j("GOVERNANCE/AO-E0-B8-M06-02-SAMPLE-ADEQUACY-PREREGISTRATION-V0.2.json")
DATAC = j("GOVERNANCE/AO-E0-B12-DATA-01-PROSPECTIVE-FORWARD-INSTANCE-FORMATION-CONTRACT-V0.2.json")
DRC = j("GOVERNANCE/AO-E0-B8-DR-01-FINAL-QUALIFICATION-DECISION-RULE-V0.2.json")
TCC = j("GOVERNANCE/AO-E0-B12-DATA-01-TC-01-COUNT-ONLY-CONTRACT-V0.2.json")
APP = j("GOVERNANCE/AO-E0-M06-AMEND-03-PROSPECTIVE-APPLICATION-MANIFEST-V0.1.json")
AUTH = j("GOVERNANCE/AO-E0-M06-AMEND-03-HUMAN-AUTHORIZATION-RECEIPT-2026-10-07.json")

HOUR = 3_600_000
START = 1_791_284_400_000
END = 1_822_820_400_000
BASE = START - 21 * HOUR
H1_ID = "USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1"

def rows(n=24):
    return [{
        "h1_start_ms_utc": BASE + i * HOUR,
        "source_segment_id": 1,
        "continuity_block_id": 1,
        "continuity_ordinal": i,
        "mid_close": 100.0,
    } for i in range(n)]

def tick(ts):
    return {"timestamp_ms": ts, "bid": 99.0, "ask": 101.0, "continuity_status": "OK"}

def tc_fixture():
    h = rows(24)
    h[20]["mid_close"] = 101.0
    h[21]["mid_close"] = 99.0
    h[22]["mid_close"] = 101.0
    h[23]["mid_close"] = 99.0
    return h, [tick(h[i]["h1_start_ms_utc"] + HOUR) for i in range(20, 24)]

def dr_base(n=100):
    return {
        "fixed_horizon_reached": True,
        "sample_n": n,
        "m05_interval_available": True,
        "m05_ci_lower": 6.0,
        "m05_ci_upper": 8.0,
        "stationarity_status": "RESOLVED_FOR_RESAMPLING",
        "f2_s4_status": "COST_ROBUSTNESS_PASS",
        "m07_material_influence": False,
        "m07_sign_reversal": False,
        "m08_material_selection_asymmetry": False,
        "prior_exposure_state": "CONTAMINATED",
        "search_universe_status": "PARTIAL_SEARCH_UNIVERSE",
        "n_trials": None,
        "confirmatory_route": "NEW_FORWARD_DATA_ONLY",
    }

def test_01_authority_binding():
    assert AUTH["application_parent_head"] == "cd2ea9d40f7fcf14c3547384a03e00820ed5982c"
    assert AUTH["real_tc01_forward_read"] is False
    assert AUTH["b12"] == "CLOSED"

def test_02_exact_horizon():
    assert DATA.EVIDENCE_START_MS == START
    assert DATA.EVIDENCE_END_EXCLUSIVE_MS == END
    assert END - START == 365 * 24 * HOUR

def test_03_half_open_window():
    assert DATA.in_evidence_window(START)
    assert DATA.in_evidence_window(END - 1)
    assert not DATA.in_evidence_window(START - 1)
    assert not DATA.in_evidence_window(END)

def test_04_collection_state():
    assert DATA.collection_state(START) == "COLLECTING_WAIT_NOT_READY"
    assert DATA.collection_state(END) == "FIXED_HORIZON_REACHED"

def test_05_m06_reference_preserved():
    assert M06.REFERENCE_PLANNING_N == 58927
    assert M06C["reference_planning_n"] == 58927

def test_06_m06_no_terminal_authority():
    assert M06.planning_metrics(58927)["reference_planning_n_is_terminal_authority"] is False
    assert M06C["reference_planning_n_is_terminal_authority"] is False

def test_07_m06_boundary_is_descriptive():
    assert not M06.planning_metrics(58926)["reference_planning_n_reached"]
    assert M06.planning_metrics(58927)["reference_planning_n_reached"]

def test_08_m06_zero_n_reportable():
    out = M06.planning_metrics(0)
    assert out["planning_model_precision_half_width_at_actual_n"] is None
    assert out["planning_model_power_at_actual_n"] is None

def test_09_data01_count_cannot_end_experiment():
    assert DATAC["closed_trade_count_may_determine_end"] is False
    assert DATAC["reference_planning_n_may_determine_end"] is False

def test_10_no_optional_extension():
    assert DATAC["result_driven_extension"] is False
    assert DATAC["data_gap_extension"] is False

def test_11_dr_waits_before_horizon():
    out = DR.evaluate({"fixed_horizon_reached": False})
    assert out["collection_state"] == "WAIT_NOT_READY"
    assert out["evidence_verdict"] is None

def test_12_dr_support_below_reference_n():
    out = DR.evaluate(dr_base(100))
    assert out["evidence_verdict"] == "SUPPORT"
    assert out["qualification_status"] == "QUALIFIED"
    assert out["planning_target_status"] == "PLANNING_TARGET_NOT_REACHED"

def test_13_dr_no_insufficient_sample_blocker():
    out = DR.evaluate(dr_base(100))
    assert "INSUFFICIENT_SAMPLE" not in out["all_qualification_reasons"]
    assert "PLANNING_TARGET_NOT_REACHED" in out["qualification_limitations"]

def test_14_dr_zero_n_not_analyzable():
    out = DR.evaluate(dr_base(0))
    assert out["evidence_verdict"] == "INCONCLUSIVE"
    assert out["qualification_reason"] == "INFERENCE_NOT_ANALYZABLE"

def test_15_dr_reference_n_does_not_auto_support():
    x = dr_base(58927)
    x.update(m05_ci_lower=4.0, m05_ci_upper=6.0)
    assert DR.evaluate(x)["evidence_verdict"] == "INCONCLUSIVE"

def test_16_dr_refute_preserved():
    x = dr_base(100)
    x.update(m05_ci_lower=1.0, m05_ci_upper=5.0, f2_s4_status="COST_ROBUSTNESS_FAIL")
    assert DR.evaluate(x)["evidence_verdict"] == "REFUTE"

def test_17_dr_nonstationarity_preserved():
    x = dr_base(100)
    x["stationarity_status"] = "UNRESOLVED_NONSTATIONARY"
    assert "NONSTATIONARITY_UNRESOLVED" in DR.evaluate(x)["all_qualification_reasons"]

def test_18_no_new_minimum_n():
    assert DRC["new_arbitrary_minimum_n"] is None
    assert DRC["analyzability_source"] == "EXISTING_M04_M05_RUNTIME_PRECONDITIONS"

def test_19_inconclusive_terminal_preserved():
    assert DRC["inconclusive_is_valid_terminal_outcome"] is True

def test_20_tc_descriptive_only():
    assert TCC["role"] == "DESCRIPTIVE_COUNT_TRACKER_ONLY"
    assert TCC["terminal_authority"] is False

def test_21_tc_output_surface():
    h, ticks = tc_fixture()
    out = TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)
    assert set(out) == set(TCC["allowed_output"])

def test_22_tc_no_terminal_fields():
    h, ticks = tc_fixture()
    out = TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)
    assert "terminal_threshold_reached" not in out
    assert "exact_terminal_decision_time_if_reached" not in out

def test_23_tc_count_is_three():
    h, ticks = tc_fixture()
    assert TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)["cumulative_closed_trade_count"] == 3

def test_24_tc_reference_parity():
    h, ticks = tc_fixture()
    p = TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)
    r = REF.reference_count(h, ticks, H1_ID)
    assert p["cumulative_closed_trade_count"] == r["cumulative_closed_trade_count"]
    assert p["reference_planning_n_reached"] == r["reference_planning_n_reached"]

def test_25_post_end_tick_ignored():
    h, ticks = tc_fixture()
    a = TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)
    b = TC.run_count_only(
        h,
        raw_ticks=ticks + [{"timestamp_ms": END, "ignored": True}],
        e1_03_identity=H1_ID,
    )
    assert a == b

def test_26_post_end_row_ignored():
    h, ticks = tc_fixture()
    extra = {
        "h1_start_ms_utc": END,
        "source_segment_id": 9,
        "continuity_block_id": 9,
        "continuity_ordinal": 0,
        "mid_close": 999999.0,
    }
    a = TC.run_count_only(h, raw_ticks=ticks, e1_03_identity=H1_ID)
    b = TC.run_count_only(h + [extra], raw_ticks=ticks, e1_03_identity=H1_ID)
    assert a == b

def test_27_manifest_points_to_four_v02_surfaces():
    assert set(APP["future_forward_surface_after_qualification"]) == {"m06", "data01", "dr01", "tc01"}
    assert all(v.endswith("V0.2.json") for v in APP["future_forward_surface_after_qualification"].values())

def test_28_activation_requires_qualification_and_rebreak():
    assert APP["activation_condition"] == "M06_AMEND_03_TECHNICAL_QUALIFICATION_PASS_PLUS_PERSISTED_HEAD_REBREAK"

def test_29_manifest_firewall():
    assert APP["real_forward_read_authorized"] is False
    assert APP["b12"] == "CLOSED"

def test_30_force_false():
    assert AUTH["force"] is False
    assert APP["force"] is False
    assert M06C["force"] is False
    assert DATAC["force"] is False
    assert DRC["force"] is False
    assert TCC["force"] is False
