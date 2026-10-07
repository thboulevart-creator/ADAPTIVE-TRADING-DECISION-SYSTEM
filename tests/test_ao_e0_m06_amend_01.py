from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "tools/ao_e0_m06_amend_01_analysis.py"
CONTRACT_PATH = ROOT / "GOVERNANCE/AO-E0-M06-AMEND-01-PROSPECTIVE-ANALYSIS-CONTRACT-V0.1.json"
AUTH_PATH = ROOT / "GOVERNANCE/AO-E0-M06-AMEND-01-HUMAN-AUTHORIZATION-2026-10-07.md"


def load_runtime():
    spec = importlib.util.spec_from_file_location("m06_amend_01", RUNTIME_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


M = load_runtime()


def test_01_contract_identity():
    assert M.CONTRACT == "ATDS_AO_E0_M06_AMEND_01_ANALYSIS_V0_1"


def test_02_frozen_power_recomputes_exact_58927():
    assert M.required_power_n(
        sigma=M.SIGMA,
        effect=M.POWER_EFFECT_SIZE,
        alpha=M.ALPHA,
        power=M.TARGET_POWER,
    ) == 58927


def test_03_frozen_precision_recomputes_exact_30036():
    assert M.required_precision_n(
        sigma=M.SIGMA,
        half_width=M.DELTA_MIN,
        confidence=M.CONFIDENCE_LEVEL,
    ) == 30036


def test_04_final_n_is_power_dominated():
    out = M.analyze()["frozen_model_recomputation"]
    assert out["precision_required_n"] == 30036
    assert out["power_required_n"] == 58927
    assert out["final_required_n"] == 58927


def test_05_signal_to_noise_is_small_and_exactly_derived():
    ratio = M.analyze()["frozen_model_recomputation"]["signal_to_noise_effect_over_sigma"]
    assert abs(ratio - (5.0 / 336.4106561689863)) < 1e-15


def test_06_closed_trade_unit_matches_estimand():
    s = M.analyze()["sample_unit"]
    assert s["current_estimand_unit"] == "CLOSED_TRADE"
    assert s["closed_trade_unit_matches_estimand"] is True


def test_07_h1_substitution_does_not_preserve_estimand():
    assert M.analyze()["sample_unit"]["h1_substitution_preserves_estimand"] is False


def test_08_dependence_was_not_ignored():
    d = M.analyze()["dependence"]
    assert d["ignored"] is False
    assert d["m04_m05_dependence_route_exists"] is True


def test_09_58927_is_not_effective_independent_n_claim():
    assert M.analyze()["dependence"]["58927_is_effective_independent_n_claim"] is False


def test_10_absolute_lower_bound_is_58927_hours():
    assert M.analyze()["operational_feasibility"]["absolute_24x7_lower_bound_hours"] == 58927


def test_11_absolute_lower_bound_exceeds_6_7_years():
    years = M.analyze()["operational_feasibility"]["absolute_24x7_lower_bound_years_36525"]
    assert years > 6.7


def test_12_exposed_activity_proxy_uses_650_trades_only():
    p = M.exposed_activity_proxy()
    assert p["closed_trades"] == 650
    assert p["performance_values_used"] is False
    assert p["confirmatory_use"] is False


def test_13_exposed_activity_window_is_about_five_years():
    years = M.exposed_activity_proxy()["window_years_36525"]
    assert 4.99 < years < 5.01


def test_14_exposed_activity_rate_is_about_130_per_year():
    rate = M.exposed_activity_proxy()["closed_trades_per_year"]
    assert 129.0 < rate < 131.0


def test_15_same_activity_proxy_implies_over_450_years_for_58927():
    years = M.exposed_activity_proxy()["years_to_58927_at_same_activity_rate"]
    assert years > 450.0


def test_16_baseline_95_80_power_n_recomputes_27988():
    assert M.analyze()["operational_feasibility"]["baseline_95_80_power_required_n"] == 27988


def test_17_baseline_relaxation_still_exceeds_200_years_at_same_activity_proxy():
    years = M.analyze()["operational_feasibility"]["baseline_95_80_years_at_same_activity_proxy"]
    assert years > 200.0


def test_18_no_finite_completion_guarantee():
    assert M.analyze()["operational_feasibility"]["finite_completion_guaranteed_by_strategy_semantics"] is False


def test_19_root_cause_is_not_arithmetic():
    r = M.analyze()["root_cause"]
    assert r["arithmetic_error"] is False
    assert r["wrong_sample_unit_for_current_estimand"] is False
    assert r["dependence_omitted"] is False


def test_20_primary_root_cause_is_terminal_translation():
    assert M.analyze()["root_cause"]["primary"] == "NOMINAL_PLANNING_N_TRANSLATED_INTO_MANDATORY_TERMINAL_COUNT"


def test_21_keep_route_not_recommended():
    assert M.analyze()["routes"]["R0_KEEP_58927_AS_MANDATORY_TERMINAL_COUNT"] == "NOT_RECOMMENDED"


def test_22_parameter_relaxation_not_primary_remedy():
    assert M.analyze()["routes"]["R1_RELAX_ALPHA_POWER_OR_PRECISION_FOR_CONVENIENCE"] == "NOT_RECOMMENDED_AS_PRIMARY_REMEDY"


def test_23_h1_unit_route_rejected():
    assert M.analyze()["routes"]["R2_REPLACE_CLOSED_TRADE_UNIT_WITH_H1_DECISION_UNIT"] == "REJECT_FOR_CURRENT_ESTIMAND"


def test_24_r4_is_recommended():
    assert M.analyze()["routes"]["R4_DECOUPLE_PLANNING_N_FROM_FIXED_NONPERFORMANCE_CONFIRMATORY_HORIZON"] == "RECOMMENDED_FOR_NEXT_DESIGN_PHASE"


def test_25_next_phase_does_not_select_horizon_now():
    n = M.analyze()["recommended_next_phase"]
    assert n["control"] == "AO-E0-M06-AMEND-02"
    assert n["select_exact_horizon_now"] is False
    assert n["use_forward_performance_to_choose_horizon"] is False


def test_26_authority_firewall():
    a = M.analyze()["authority"]
    assert all(value is False for value in a.values())


def test_27_contract_preserves_frozen_m06():
    c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    assert c["frozen_inputs"]["final_required_n"] == 58927
    assert c["authority"]["m06_parameter_change"] is False
    assert c["authority"]["data01_terminal_rule_change"] is False
    assert c["authority"]["real_tc01_forward_read"] is False
    assert c["authority"]["b12_open"] is False


def test_28_human_authorization_is_analysis_only():
    text = AUTH_PATH.read_text(encoding="utf-8")
    assert "AUTHORIZE_PROSPECTIVE_M06_AMENDMENT_ANALYSIS_ONLY" in text
    assert "FINAL_REQUIRED_N = 58927" in text
    assert "B12 =" in text and "CLOSED" in text
