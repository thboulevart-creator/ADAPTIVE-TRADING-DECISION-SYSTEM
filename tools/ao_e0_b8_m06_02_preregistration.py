from __future__ import annotations
import math
from statistics import NormalDist
from tools import smf03_dependence_inference as m06

SIGMA = 336.4106561689863
DELTA_MIN = 5.0
HALF_WIDTH = 5.0
CONFIDENCE_LEVEL = 0.99
ALPHA = 0.01
TARGET_POWER = 0.90
EFFECT_SIZE = 5.0
ALTERNATIVE = "GREATER"
EFFECT_SOURCE = "PREDECLARED"
POWER_MAX_N = 58927
MODEL_REF = "NORMAL_MEAN_KNOWN_SIGMA"

def independent_precision_n(*, sigma, half_width, confidence_level):
    z = NormalDist().inv_cdf(0.5 + confidence_level / 2.0)
    return math.ceil((z * sigma / half_width) ** 2)

def independent_one_sided_power(n, *, effect_size, sigma, alpha):
    z_alpha = NormalDist().inv_cdf(1.0 - alpha)
    shift = effect_size * math.sqrt(n) / sigma
    return 1.0 - NormalDist().cdf(z_alpha - shift)

def build_candidate():
    precision = m06.required_n_for_mean_precision(
        model_ref=MODEL_REF,
        stddev=SIGMA,
        half_width=HALF_WIDTH,
        confidence_level=CONFIDENCE_LEVEL,
    )
    power = m06.required_n_for_mean_power(
        model_ref=MODEL_REF,
        effect_size=EFFECT_SIZE,
        stddev=SIGMA,
        alpha=ALPHA,
        target_power=TARGET_POWER,
        alternative=ALTERNATIVE,
        effect_source=EFFECT_SOURCE,
        max_n=POWER_MAX_N,
    )
    ref_precision = independent_precision_n(
        sigma=SIGMA,
        half_width=HALF_WIDTH,
        confidence_level=CONFIDENCE_LEVEL,
    )
    assert precision["required_n"] == ref_precision == 30036
    assert power["required_n"] == POWER_MAX_N == 58927
    assert independent_one_sided_power(
        POWER_MAX_N - 1,
        effect_size=EFFECT_SIZE,
        sigma=SIGMA,
        alpha=ALPHA,
    ) < TARGET_POWER
    assert independent_one_sided_power(
        POWER_MAX_N,
        effect_size=EFFECT_SIZE,
        sigma=SIGMA,
        alpha=ALPHA,
    ) >= TARGET_POWER
    return {
        "precision": precision,
        "power": power,
        "combination_rule": "MAX_PRECISION_POWER",
        "final_required_n": max(precision["required_n"], power["required_n"]),
        "design_alternative_theta": DELTA_MIN + EFFECT_SIZE,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(build_candidate(), sort_keys=True, indent=2))
