from __future__ import annotations
from math import sqrt
from statistics import NormalDist

REFERENCE_PLANNING_N = 58927
SIGMA = 336.4106561689863
CONFIDENCE_LEVEL = 0.99
EFFECT_SIZE = 5.0
ALPHA = 0.01

def planning_metrics(n: int) -> dict:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("INVALID_N")
    if n == 0:
        half_width = None
        power = None
    else:
        z = NormalDist().inv_cdf((1.0 + CONFIDENCE_LEVEL) / 2.0)
        half_width = z * SIGMA / sqrt(n)
        z_alpha = NormalDist().inv_cdf(1.0 - ALPHA)
        power = 1.0 - NormalDist().cdf(z_alpha - EFFECT_SIZE * sqrt(n) / SIGMA)
    return {
        "actual_closed_trade_count": n,
        "reference_planning_n": REFERENCE_PLANNING_N,
        "reference_planning_n_reached": n >= REFERENCE_PLANNING_N,
        "planning_model_precision_half_width_at_actual_n": half_width,
        "planning_model_power_at_actual_n": power,
        "reference_planning_n_is_terminal_authority": False,
        "planning_shortfall_authorizes_extension": False,
    }
