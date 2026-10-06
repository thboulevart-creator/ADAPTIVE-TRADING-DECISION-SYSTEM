from __future__ import annotations
import math

DELTA_MIN = 5.0
M06_FINAL_REQUIRED_N = 58927

BOUND_PRIOR_EXPOSURE_STATE = "CONTAMINATED"
BOUND_SEARCH_UNIVERSE_STATUS = "PARTIAL_SEARCH_UNIVERSE"
BOUND_CONFIRMATORY_ROUTE = "NEW_FORWARD_DATA_ONLY"

F2_ALLOWED = {
    "COST_ROBUSTNESS_PASS",
    "COST_ROBUSTNESS_FAIL",
    "COST_ROBUSTNESS_INCONCLUSIVE",
}

REASON_PRIORITY = [
    "PROVENANCE_ROUTE_INVALID",
    "PROVENANCE_BINDING_MISMATCH",
    "INSUFFICIENT_SAMPLE",
    "NONSTATIONARITY_UNRESOLVED",
    "INFERENCE_BLOCKED",
    "SIGN_REVERSAL",
    "MATERIAL_INFLUENCE",
    "MATERIAL_SELECTION_ASYMMETRY",
    "COST_ROBUSTNESS_INCONCLUSIVE",
    "CI_OVERLAPS_MATERIALITY_BOUNDARY",
    "COST_ROBUSTNESS_NOT_SUPPORTED",
    "EVIDENCE_CONFLICT_M05_SUPPORT_VS_COST_ROBUSTNESS_FAIL",
    "EVIDENCE_CONFLICT_M05_REFUTE_VS_COST_ROBUSTNESS_PASS",
]

PROVENANCE_LIMITATIONS = [
    "PRIOR_SEARCH_UNIVERSE_PARTIAL",
    "N_TRIALS_UNKNOWN",
    "ALPHA_NOT_MULTIPLICITY_CORRECTED",
    "HYPOTHESIS_ORIGIN_NOT_PRISTINE",
]

def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))

def _ordered_unique(values):
    seen = set()
    out = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out

def _primary_reason(reasons):
    for preferred in REASON_PRIORITY:
        if preferred in reasons:
            return preferred
    return reasons[0] if reasons else None

def classify_m05_ci(lower, upper):
    if not _finite(lower) or not _finite(upper) or float(lower) > float(upper):
        raise ValueError("INVALID_M05_INTERVAL")
    lower = float(lower)
    upper = float(upper)
    if lower > DELTA_MIN:
        return "SUPPORT"
    if upper <= DELTA_MIN:
        return "REFUTE"
    return "INCONCLUSIVE"

def evaluate(inputs: dict) -> dict:
    if not isinstance(inputs, dict):
        raise ValueError("INPUT_OBJECT_REQUIRED")

    n = inputs.get("sample_n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("INVALID_SAMPLE_N")

    prior = inputs.get("prior_exposure_state")
    search = inputs.get("search_universe_status")
    n_trials = inputs.get("n_trials")
    route = inputs.get("confirmatory_route")
    stationarity = inputs.get("stationarity_status")
    f2 = inputs.get("f2_s4_status")
    m07_material = inputs.get("m07_material_influence")
    m07_sign = inputs.get("m07_sign_reversal")
    m08_asym = inputs.get("m08_material_selection_asymmetry")
    m05_available = inputs.get("m05_interval_available")

    for name, value in {
        "m07_material_influence": m07_material,
        "m07_sign_reversal": m07_sign,
        "m08_material_selection_asymmetry": m08_asym,
        "m05_interval_available": m05_available,
    }.items():
        if not isinstance(value, bool):
            raise ValueError(f"{name.upper()}_BOOLEAN_REQUIRED")

    reasons = []
    limitations = []
    signals = []

    if route != BOUND_CONFIRMATORY_ROUTE:
        reasons.append("PROVENANCE_ROUTE_INVALID")

    if prior != BOUND_PRIOR_EXPOSURE_STATE or search != BOUND_SEARCH_UNIVERSE_STATUS or n_trials is not None:
        reasons.append("PROVENANCE_BINDING_MISMATCH")
    else:
        limitations.extend(PROVENANCE_LIMITATIONS)

    if n < M06_FINAL_REQUIRED_N:
        reasons.append("INSUFFICIENT_SAMPLE")

    if stationarity != "RESOLVED_FOR_RESAMPLING":
        reasons.append("NONSTATIONARITY_UNRESOLVED")

    if m07_sign:
        reasons.append("SIGN_REVERSAL")
    if m07_material:
        reasons.append("MATERIAL_INFLUENCE")
    if m08_asym:
        reasons.append("MATERIAL_SELECTION_ASYMMETRY")

    if f2 not in F2_ALLOWED:
        raise ValueError("INVALID_F2_S4_STATUS")
    if f2 == "COST_ROBUSTNESS_INCONCLUSIVE":
        reasons.append("COST_ROBUSTNESS_INCONCLUSIVE")

    m05_state = "UNAVAILABLE"
    if not m05_available:
        reasons.append("INFERENCE_BLOCKED")
    else:
        try:
            m05_state = classify_m05_ci(inputs.get("m05_ci_lower"), inputs.get("m05_ci_upper"))
        except ValueError:
            reasons.append("INFERENCE_BLOCKED")
            m05_state = "INVALID"
        else:
            signals.append(f"M05_{m05_state}")
            if m05_state == "INCONCLUSIVE":
                reasons.append("CI_OVERLAPS_MATERIALITY_BOUNDARY")

    reasons = _ordered_unique(reasons)

    if reasons:
        verdict = "INCONCLUSIVE"
    else:
        if m05_state == "SUPPORT":
            if f2 == "COST_ROBUSTNESS_PASS":
                verdict = "SUPPORT"
            else:
                verdict = "INCONCLUSIVE"
                reasons.append("EVIDENCE_CONFLICT_M05_SUPPORT_VS_COST_ROBUSTNESS_FAIL")
        elif m05_state == "REFUTE":
            if f2 == "COST_ROBUSTNESS_FAIL":
                verdict = "REFUTE"
            else:
                verdict = "INCONCLUSIVE"
                reasons.append("EVIDENCE_CONFLICT_M05_REFUTE_VS_COST_ROBUSTNESS_PASS")
        else:
            verdict = "INCONCLUSIVE"
            reasons.append("INFERENCE_BLOCKED")

    if verdict == "INCONCLUSIVE" and f2 == "COST_ROBUSTNESS_FAIL" and m05_state == "INCONCLUSIVE":
        reasons.append("COST_ROBUSTNESS_NOT_SUPPORTED")

    reasons = _ordered_unique(reasons)

    if verdict == "SUPPORT":
        qualification_status = "QUALIFIED"
        qualification_reason = "SUPPORTED_NEW_FORWARD_CC05_WITH_PARTIAL_PRIOR_SEARCH_UNIVERSE"
    elif verdict == "REFUTE":
        qualification_status = "NOT_QUALIFIED"
        qualification_reason = "REFUTED_BY_VALID_FORWARD_CI_AND_COST_ROBUSTNESS_FAIL"
    else:
        qualification_status = "NOT_QUALIFIED"
        qualification_reason = _primary_reason(reasons) or "INCONCLUSIVE"

    return {
        "evidence_verdict": verdict,
        "m05_evidence_state": m05_state,
        "qualification_status": qualification_status,
        "qualification_reason": qualification_reason,
        "all_qualification_reasons": reasons,
        "qualification_limitations": limitations,
        "signals": signals,
        "decision": "PENDING_HUMAN_PROMOTION",
        "decision_authority": "NONE",
        "b8_closure": False,
        "b12_open": False,
        "ao_e0_execution_authorized": False,
        "forward_data_observation_authorized": False,
        "real_performance_observation_authorized": False,
    }
