from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    assert s and s.loader
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

P = load("primary", ROOT / "tools/ao_e0_m06_amend_02_fixed_horizon.py")
R = load("reference", ROOT / "tools/ao_e0_m06_amend_02_reference.py")
CONTRACT = json.loads((ROOT / "GOVERNANCE/AO-E0-M06-AMEND-02-FIXED-HORIZON-CONTRACT-CANDIDATE-V0.1.json").read_text(encoding="utf-8"))
DIFFS = json.loads((ROOT / "GOVERNANCE/AO-E0-M06-AMEND-02-EXACT-SEMANTIC-DIFFS-CANDIDATE-V0.1.json").read_text(encoding="utf-8"))
BREAKERS = json.loads((ROOT / "GOVERNANCE/AO-E0-M06-AMEND-02-FROZEN-BREAKERS-V0.1.json").read_text(encoding="utf-8"))
AUTH = json.loads((ROOT / "GOVERNANCE/AO-E0-M06-AMEND-02-HUMAN-AUTHORIZATION-RECEIPT-2026-10-07.json").read_text(encoding="utf-8"))

def test_01_identity():
    assert P.CONTRACT == "ATDS_AO_E0_M06_AMEND_02_FIXED_HORIZON_V0_1"

def test_02_exact_start():
    assert P.START_MS == 1791284400000

def test_03_exact_end():
    assert P.END_MS == 1822820400000

def test_04_exact_365d_duration():
    assert P.END_MS - P.START_MS == P.DURATION_MS == 365 * 24 * 3600 * 1000

def test_05_start_inclusive():
    assert P.included(P.START_MS)

def test_06_end_exclusive():
    assert not P.included(P.END_MS)

def test_07_before_start_excluded():
    assert not P.included(P.START_MS - 1)

def test_08_last_millisecond_included():
    assert P.included(P.END_MS - 1)

def test_09_horizon_not_reached_before_end():
    assert not P.horizon_reached(P.END_MS - 1)

def test_10_horizon_reached_exact_end():
    assert P.horizon_reached(P.END_MS)

def test_11_reference_n_preserved():
    assert P.REFERENCE_N == 58927
    assert CONTRACT["bindings"]["reference_planning_n"] == 58927

def test_12_annual_cycle_contains_standard_and_dst_new_york():
    ny = ZoneInfo("America/New_York")
    jan = datetime(2027, 1, 15, 12, tzinfo=timezone.utc).astimezone(ny).utcoffset().total_seconds()
    jul = datetime(2027, 7, 15, 12, tzinfo=timezone.utc).astimezone(ny).utcoffset().total_seconds()
    assert jan == -18000
    assert jul == -14400

def test_13_contract_is_365d_calendar():
    h = CONTRACT["horizon"]
    assert h["type"] == "FIXED_365D_UTC_CALENDAR_HORIZON"
    assert h["duration_days"] == 365

def test_14_no_performance_end_authority():
    h = CONTRACT["horizon"]
    assert h["performance_values_may_determine_end"] is False
    assert h["closed_trade_count_may_determine_end"] is False
    assert h["reference_planning_n_may_determine_end"] is False

def test_15_no_result_extension():
    h = CONTRACT["horizon"]
    assert h["result_driven_extension"] is False
    assert h["precision_driven_extension"] is False
    assert h["power_driven_extension"] is False
    assert h["near_significance_extension"] is False

def test_16_zero_n_metrics():
    x = P.planning_metrics(0)
    assert x["planning_model_precision_half_width_at_actual_n"] is None
    assert x["planning_model_power_at_actual_n"] is None
    assert x["reference_planning_n_reached"] is False

def test_17_one_trade_not_analyzable_by_existing_m04_minimum():
    assert P.planning_metrics(1)["inference_analyzable_by_existing_m04_minimum"] is False

def test_18_two_trades_meet_existing_m04_minimum():
    assert P.planning_metrics(2)["inference_analyzable_by_existing_m04_minimum"] is True

def test_19_reference_n_reach_boundary():
    assert not P.planning_metrics(58926)["reference_planning_n_reached"]
    assert P.planning_metrics(58927)["reference_planning_n_reached"]

def test_20_invalid_n_fails():
    import pytest
    for n in (-1, True, 1.5):
        with pytest.raises(ValueError):
            P.planning_metrics(n)

def test_21_wait_before_horizon_irrespective_of_n():
    assert P.terminal_state(now_ms=P.END_MS - 1, n=58927, data_complete=True, existing_validity_blocked=False)["state"] == "WAIT_NOT_READY"

def test_22_data_incomplete_no_extension():
    x = P.terminal_state(now_ms=P.END_MS, n=100, data_complete=False, existing_validity_blocked=False)
    assert x["state"] == "INCONCLUSIVE_DATA_INCOMPLETE"
    assert x["extension_authorized"] is False

def test_23_unanalyzable_no_extension():
    x = P.terminal_state(now_ms=P.END_MS, n=1, data_complete=True, existing_validity_blocked=False)
    assert x["state"] == "INCONCLUSIVE_INFERENCE_NOT_ANALYZABLE"
    assert x["extension_authorized"] is False

def test_24_validity_block_no_extension():
    x = P.terminal_state(now_ms=P.END_MS, n=100, data_complete=True, existing_validity_blocked=True)
    assert x["state"] == "INCONCLUSIVE_VALIDITY_BLOCKED"
    assert x["extension_authorized"] is False

def test_25_ready_even_when_reference_n_not_reached():
    x = P.terminal_state(now_ms=P.END_MS, n=100, data_complete=True, existing_validity_blocked=False)
    assert x["state"] == "READY_FOR_EXISTING_DR01_INFERENCE_PATHS"
    assert x["reference_planning_n_reached"] is False

def test_26_reference_n_does_not_auto_support():
    assert DIFFS["dr01"]["candidate_new"]["n_ge_58927"] == "PLANNING_TARGET_REACHED_LIMITATION_CLEARED_ONLY"

def test_27_n_below_reference_is_limitation_only():
    assert DIFFS["dr01"]["candidate_new"]["n_lt_58927"] == "PLANNING_TARGET_NOT_REACHED_LIMITATION_ONLY"

def test_28_existing_support_refute_paths_preserved():
    assert DIFFS["dr01"]["candidate_new"]["valid_support_refute_paths"] == "PRESERVED"

def test_29_tc01_loses_terminal_authority_in_candidate():
    assert DIFFS["tc01"]["candidate_new"]["terminal_authority"] is False
    assert DIFFS["tc01"]["candidate_new"]["purpose"] == "DESCRIPTIVE_COUNT_TRACKER_ONLY"

def test_30_actual_application_not_authorized():
    assert DIFFS["application_status"] == "NOT_AUTHORIZED"
    assert CONTRACT["authority"]["actual_amendment_application"] is False

def test_31_real_forward_read_not_authorized():
    assert CONTRACT["authority"]["real_tc01_forward_read"] is False
    assert AUTH["not_authorized"]["real_tc01_forward_read"] is True

def test_32_b12_closed_authority():
    assert CONTRACT["authority"]["b12_open"] is False
    assert AUTH["frozen_state"]["b12"] == "CLOSED"

def test_33_exact_breaker_count_and_fail_closed():
    assert len(BREAKERS["breakers"]) == 30
    assert BREAKERS["required_behavior"] == "FAIL_CLOSED"

def test_34_primary_reference_parity_boundaries():
    for t in [P.START_MS - 1, P.START_MS, P.END_MS - 1, P.END_MS, P.END_MS + 1]:
        assert P.included(t) == R.is_in_window(t)
        assert P.horizon_reached(t) == R.done(t)

def test_35_primary_reference_metrics_parity():
    for n in [0, 1, 2, 100, 58926, 58927, 60000]:
        assert P.planning_metrics(n) == R.reference_metrics(n)

def test_36_primary_reference_terminal_parity():
    cases = [
        (P.END_MS - 1, 100, True, False),
        (P.END_MS, 0, True, False),
        (P.END_MS, 1, True, False),
        (P.END_MS, 100, False, False),
        (P.END_MS, 100, True, True),
        (P.END_MS, 100, True, False),
        (P.END_MS, 58927, True, False),
    ]
    for args in cases:
        assert P.terminal_state(now_ms=args[0], n=args[1], data_complete=args[2], existing_validity_blocked=args[3]) == R.reference_terminal(*args)

def test_37_horizon_selection_is_nonperformance():
    r = CONTRACT["selection_rationale"]
    assert r["exposed_structural_activity_proxy_is_performance"] is False
    assert r["expected_closed_trades_at_proxy_rate_is_forecast"] is False

def test_38_365d_is_selected_as_minimum_full_annual_cycle():
    r = CONTRACT["selection_rationale"]
    assert r["primary"] == "MINIMUM_FIXED_HORIZON_SPANNING_ONE_COMPLETE_ANNUAL_CALENDAR_CYCLE"
    assert "REJECTED" in r["shorter_90d_180d"]
    assert "NOT_SELECTED" in r["longer_730d"]

def test_39_no_new_numeric_analyzability_threshold():
    assert CONTRACT["dr01_semantics_candidate"]["minimum_analyzability"] == "EXISTING_M04_M05_RUNTIME_PRECONDITIONS_ONLY_NO_NEW_NUMERIC_THRESHOLD"

def test_40_force_false_everywhere():
    assert CONTRACT["force"] is False
    assert DIFFS["force"] is False
    assert BREAKERS["force"] is False
    assert AUTH["force"] is False
