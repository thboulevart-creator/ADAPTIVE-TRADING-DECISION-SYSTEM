from __future__ import annotations

import math

CONTRACT = "ATDS_SMF03_CORE_FOUNDATION_REFERENCE_V0_1"

def _number(value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(float(value))
    ):
        raise ValueError("NONFINITE_REFERENCE_INPUT")
    return float(value)

def reference_net_economic_effect(gross_outcomes, *, costs, minimum_effect):
    gross = [_number(x) for x in gross_outcomes]
    if not gross:
        raise ValueError("EMPTY_SAMPLE")
    if isinstance(costs, (int, float)) and not isinstance(costs, bool):
        one = _number(costs)
        cost_values = [one for _ in gross]
    else:
        if len(costs) != len(gross):
            raise ValueError("COST_LENGTH_MISMATCH")
        cost_values = [_number(x) for x in costs]
    threshold = _number(minimum_effect)
    net = []
    for index in range(len(gross)):
        net.append(gross[index] - cost_values[index])
    n = len(gross)
    gross_mean = math.fsum(gross) / n
    cost_mean = math.fsum(cost_values) / n
    net_mean = math.fsum(net) / n
    return {
        "n": n,
        "gross_mean": gross_mean,
        "cost_mean": cost_mean,
        "net_mean": net_mean,
        "minimum_effect": threshold,
        "margin_to_minimum": net_mean - threshold,
        "threshold_relation": "ABOVE_OR_EQUAL" if net_mean >= threshold else "BELOW",
        "net_outcomes": net,
    }

def _reference_quantile(ordered, probability):
    n = len(ordered)
    if n == 1:
        return ordered[0]
    location = (n - 1) * probability
    left = int(math.floor(location))
    right = int(math.ceil(location))
    if left == right:
        return ordered[left]
    fraction = location - left
    return (1.0 - fraction) * ordered[left] + fraction * ordered[right]

def reference_ecdf_quantiles(values, *, probabilities):
    sample = [_number(x) for x in values]
    if not sample:
        raise ValueError("EMPTY_SAMPLE")
    probs = [_number(x) for x in probabilities]
    for p in probs:
        if p < 0.0 or p > 1.0:
            raise ValueError("PROBABILITY_OUT_OF_RANGE")
    ordered = sorted(sample)
    total = len(ordered)
    points = []
    rank = 0
    for item in ordered:
        rank += 1
        points.append({"x": item, "p": rank / total})
    q = {}
    for p in probs:
        q[str(p)] = _reference_quantile(ordered, p)
    return {
        "n": total,
        "sorted_values": ordered,
        "ecdf": points,
        "quantiles": q,
        "tail_extrapolation": "FORBIDDEN",
    }
