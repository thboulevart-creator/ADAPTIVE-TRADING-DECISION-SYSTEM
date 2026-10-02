from __future__ import annotations

import hashlib
import json
import math

CONTRACT = "ATDS_SMF03_CORE_FOUNDATION_V0_1"

ALLOWED_METHOD_FAMILIES = (
    "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11",
    "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12",
)
ACTIVATION_STATES = ("ACTIVATED", "NOT_APPLICABLE", "BLOCKED")

def _finite_number(value) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )

def _required_text(name: str, value) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"EMPTY_MATERIAL_IDENTITY:{name}")
    return value.strip()

def _canonical_json(value) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("NON_CANONICAL_ACTIVATION_VALUE") from exc

def _sha256_ref(value) -> str:
    return "sha256:" + hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()

def create_activation_record(
    *,
    claim_definition_ref,
    failure_mode_ref,
    method_family_ref,
    validity_scope_ref,
    assumption_set_ref,
    activation_reason,
    activation_rule,
    parameter_selection_policy,
    dependency_refs,
    activation_state,
    result_exposed=False,
):
    if result_exposed:
        raise ValueError("METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE")
    claim_definition_ref = _required_text("claim_definition_ref", claim_definition_ref)
    failure_mode_ref = _required_text("failure_mode_ref", failure_mode_ref)
    method_family_ref = _required_text("method_family_ref", method_family_ref)
    validity_scope_ref = _required_text("validity_scope_ref", validity_scope_ref)
    assumption_set_ref = _required_text("assumption_set_ref", assumption_set_ref)
    activation_reason = _required_text("activation_reason", activation_reason)
    activation_rule = _required_text("activation_rule", activation_rule)
    if method_family_ref not in ALLOWED_METHOD_FAMILIES:
        raise ValueError("METHOD_FAMILY_NOT_ADOPTED")
    if activation_state not in ACTIVATION_STATES:
        raise ValueError("INVALID_ACTIVATION_STATE")
    if parameter_selection_policy is None:
        raise ValueError("PARAMETER_SELECTION_POLICY_MISSING")
    _canonical_json(parameter_selection_policy)
    if not isinstance(dependency_refs, (list, tuple)):
        raise ValueError("DEPENDENCY_REFS_INVALID")
    dependencies = [_required_text("dependency_ref", value) for value in dependency_refs]
    record = {
        "claim_definition_ref": claim_definition_ref,
        "failure_mode_ref": failure_mode_ref,
        "method_family_ref": method_family_ref,
        "validity_scope_ref": validity_scope_ref,
        "assumption_set_ref": assumption_set_ref,
        "activation_reason": activation_reason,
        "activation_rule": activation_rule,
        "parameter_selection_policy": parameter_selection_policy,
        "dependency_refs": dependencies,
        "activation_state": activation_state,
    }
    record["activation_digest"] = _sha256_ref(record)
    return record

def _validated_sample(values, *, name: str):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("EMPTY_SAMPLE")
    out = []
    for value in values:
        if not _finite_number(value):
            raise ValueError(f"NONFINITE_{name}")
        out.append(float(value))
    return out

def _validated_costs(costs, n: int):
    if _finite_number(costs):
        return [float(costs)] * n
    if not isinstance(costs, (list, tuple)) or len(costs) != n:
        raise ValueError("COST_LENGTH_MISMATCH")
    out = []
    for value in costs:
        if not _finite_number(value):
            raise ValueError("NONFINITE_COST")
        out.append(float(value))
    return out

def net_economic_effect(gross_outcomes, *, costs, minimum_effect):
    gross = _validated_sample(gross_outcomes, name="OUTCOME")
    cost_values = _validated_costs(costs, len(gross))
    if not _finite_number(minimum_effect):
        raise ValueError("NONFINITE_MINIMUM_EFFECT")
    net = [g - c for g, c in zip(gross, cost_values)]
    n = len(gross)
    gross_mean = math.fsum(gross) / n
    cost_mean = math.fsum(cost_values) / n
    net_mean = math.fsum(net) / n
    threshold = float(minimum_effect)
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

def _quantile_linear(sorted_values, p: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    h = (len(sorted_values) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return sorted_values[lo]
    weight = h - lo
    return sorted_values[lo] + weight * (sorted_values[hi] - sorted_values[lo])

def ecdf_quantiles(values, *, probabilities):
    sample = _validated_sample(values, name="OBSERVATION")
    if not isinstance(probabilities, (list, tuple)):
        raise ValueError("PROBABILITIES_INVALID")
    probs = []
    for value in probabilities:
        if not _finite_number(value):
            raise ValueError("NONFINITE_PROBABILITY")
        p = float(value)
        if p < 0.0 or p > 1.0:
            raise ValueError("PROBABILITY_OUT_OF_RANGE")
        probs.append(p)
    ordered = sorted(sample)
    n = len(ordered)
    return {
        "n": n,
        "sorted_values": ordered,
        "ecdf": [{"x": value, "p": (i + 1) / n} for i, value in enumerate(ordered)],
        "quantiles": {str(p): _quantile_linear(ordered, p) for p in probs},
        "tail_extrapolation": "FORBIDDEN",
    }
