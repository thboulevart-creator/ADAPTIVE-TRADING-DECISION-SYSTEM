from __future__ import annotations

from datetime import datetime, timezone
from math import ceil, sqrt
from statistics import NormalDist

CONTRACT = "ATDS_AO_E0_M06_AMEND_01_ANALYSIS_V0_1"

SIGMA = 336.4106561689863
DELTA_MIN = 5.0
POWER_EFFECT_SIZE = 5.0
ALPHA = 0.01
TARGET_POWER = 0.90
CONFIDENCE_LEVEL = 0.99
FINAL_REQUIRED_N = 58927

EXPOSED_STRUCTURAL_CLOSED_TRADES = 650
EXPOSED_WINDOW_START = datetime(2021, 5, 25, 0, 0, 0, 309000, tzinfo=timezone.utc)
EXPOSED_WINDOW_END = datetime(2026, 5, 24, 23, 59, 59, 963000, tzinfo=timezone.utc)

FIRST_FORWARD_DECISION = datetime(2026, 10, 6, 11, 0, 0, tzinfo=timezone.utc)

FORWARD_DATA_USED = False
FORWARD_PERFORMANCE_USED = False
M06_MODIFIED = False
DATA01_TERMINAL_RULE_MODIFIED = False
B12_OPENED = False


def required_power_n(*, sigma: float, effect: float, alpha: float, power: float) -> int:
    z_alpha = NormalDist().inv_cdf(1.0 - alpha)
    z_power = NormalDist().inv_cdf(power)
    return ceil(((z_alpha + z_power) * sigma / effect) ** 2)


def required_precision_n(*, sigma: float, half_width: float, confidence: float) -> int:
    z = NormalDist().inv_cdf((1.0 + confidence) / 2.0)
    return ceil((z * sigma / half_width) ** 2)


def exposed_activity_proxy():
    seconds = (EXPOSED_WINDOW_END - EXPOSED_WINDOW_START).total_seconds()
    years_36525 = seconds / (365.25 * 24.0 * 3600.0)
    trades_per_year = EXPOSED_STRUCTURAL_CLOSED_TRADES / years_36525
    return {
        "window_years_36525": years_36525,
        "closed_trades": EXPOSED_STRUCTURAL_CLOSED_TRADES,
        "closed_trades_per_year": trades_per_year,
        "years_to_58927_at_same_activity_rate": FINAL_REQUIRED_N / trades_per_year,
        "epistemic_class": "EXPOSED_STRUCTURAL_ACTIVITY_RATE_FEASIBILITY_PROXY_ONLY",
        "confirmatory_use": False,
        "performance_values_used": False,
    }


def analyze():
    power_n = required_power_n(
        sigma=SIGMA,
        effect=POWER_EFFECT_SIZE,
        alpha=ALPHA,
        power=TARGET_POWER,
    )
    precision_n = required_precision_n(
        sigma=SIGMA,
        half_width=DELTA_MIN,
        confidence=CONFIDENCE_LEVEL,
    )
    baseline_power_n = required_power_n(
        sigma=SIGMA,
        effect=POWER_EFFECT_SIZE,
        alpha=0.05,
        power=0.80,
    )
    proxy = exposed_activity_proxy()

    return {
        "frozen_model_recomputation": {
            "signal_to_noise_effect_over_sigma": POWER_EFFECT_SIZE / SIGMA,
            "precision_required_n": precision_n,
            "power_required_n": power_n,
            "final_required_n": max(precision_n, power_n),
            "arithmetic_matches_frozen_m06": power_n == FINAL_REQUIRED_N,
        },
        "sample_unit": {
            "current_estimand_unit": "CLOSED_TRADE",
            "closed_trade_unit_matches_estimand": True,
            "h1_substitution_preserves_estimand": False,
        },
        "dependence": {
            "ignored": False,
            "m06_explicitly_distinguishes_nominal_from_effective_independent_n": True,
            "m04_m05_dependence_route_exists": True,
            "58927_is_effective_independent_n_claim": False,
        },
        "operational_feasibility": {
            "absolute_24x7_lower_bound_hours": FINAL_REQUIRED_N,
            "absolute_24x7_lower_bound_years_36525": FINAL_REQUIRED_N / (24.0 * 365.25),
            "historical_exposed_activity_proxy": proxy,
            "baseline_95_80_power_required_n": baseline_power_n,
            "baseline_95_80_years_at_same_activity_proxy": baseline_power_n / proxy["closed_trades_per_year"],
            "finite_completion_guaranteed_by_strategy_semantics": False,
        },
        "root_cause": {
            "arithmetic_error": False,
            "wrong_sample_unit_for_current_estimand": False,
            "dependence_omitted": False,
            "primary": "NOMINAL_PLANNING_N_TRANSLATED_INTO_MANDATORY_TERMINAL_COUNT",
            "deeper": "LOW_EFFECT_TO_DISPERSION_INFORMATION_RATE_PLUS_LOW_CLOSED_TRADE_ARRIVAL_RATE",
        },
        "routes": {
            "R0_KEEP_58927_AS_MANDATORY_TERMINAL_COUNT": "NOT_RECOMMENDED",
            "R1_RELAX_ALPHA_POWER_OR_PRECISION_FOR_CONVENIENCE": "NOT_RECOMMENDED_AS_PRIMARY_REMEDY",
            "R2_REPLACE_CLOSED_TRADE_UNIT_WITH_H1_DECISION_UNIT": "REJECT_FOR_CURRENT_ESTIMAND",
            "R3_CHANGE_ESTIMAND_OR_STRATEGY_INFORMATION_UNIT": "MAJOR_REDESIGN_ONLY",
            "R4_DECOUPLE_PLANNING_N_FROM_FIXED_NONPERFORMANCE_CONFIRMATORY_HORIZON": "RECOMMENDED_FOR_NEXT_DESIGN_PHASE",
        },
        "recommended_next_phase": {
            "control": "AO-E0-M06-AMEND-02",
            "purpose": "DESIGN_FIXED_NONPERFORMANCE_HORIZON_AND_COHERENT_M06_DATA01_DR01_AMENDMENT",
            "select_exact_horizon_now": False,
            "use_forward_performance_to_choose_horizon": False,
            "preserve_58927_as_reference_planning_n_pending_human_amendment": True,
        },
        "authority": {
            "forward_data_used": FORWARD_DATA_USED,
            "forward_performance_used": FORWARD_PERFORMANCE_USED,
            "m06_modified": M06_MODIFIED,
            "data01_terminal_rule_modified": DATA01_TERMINAL_RULE_MODIFIED,
            "b12_opened": B12_OPENED,
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(analyze(), indent=2, sort_keys=True))
