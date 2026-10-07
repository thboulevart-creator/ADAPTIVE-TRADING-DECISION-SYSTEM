from __future__ import annotations

from tools import ao_e0_b8_dr_01_decision_rule as V1
from tools import ao_e0_b8_smf_01_preregistration as SMF

REFERENCE_PLANNING_N = 58927

def _ordered_unique(values):
    seen = set()
    out = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out

def evaluate(inputs: dict) -> dict:
    if not isinstance(inputs, dict):
        raise ValueError("INPUT_OBJECT_REQUIRED")

    reached = inputs.get("fixed_horizon_reached")
    if not isinstance(reached, bool):
        raise ValueError("FIXED_HORIZON_REACHED_BOOLEAN_REQUIRED")

    if not reached:
        return {
            "collection_state": "WAIT_NOT_READY",
            "evidence_verdict": None,
            "qualification_status": None,
            "qualification_reason": "FIXED_HORIZON_NOT_REACHED",
            "planning_target_status": None,
            "reference_planning_n": REFERENCE_PLANNING_N,
            "same_experiment_extension": "FORBIDDEN",
            "b12_open": False,
        }

    n = inputs.get("sample_n")
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("INVALID_SAMPLE_N")

    planning_status = (
        "PLANNING_TARGET_REACHED"
        if n >= REFERENCE_PLANNING_N
        else "PLANNING_TARGET_NOT_REACHED"
    )

    limitations = []
    if n < REFERENCE_PLANNING_N:
        limitations.append("PLANNING_TARGET_NOT_REACHED")

    try:
        SMF.m04_lags(n)
        SMF.m05_block_length(n)
    except ValueError as exc:
        if str(exc) != "INSUFFICIENT_N_FOR_M04":
            raise
        return {
            "collection_state": "FIXED_HORIZON_REACHED",
            "evidence_verdict": "INCONCLUSIVE",
            "qualification_status": "NOT_QUALIFIED",
            "qualification_reason": "INFERENCE_NOT_ANALYZABLE",
            "all_qualification_reasons": ["INFERENCE_NOT_ANALYZABLE"],
            "qualification_limitations": limitations,
            "signals": [],
            "planning_target_status": planning_status,
            "reference_planning_n": REFERENCE_PLANNING_N,
            "same_experiment_extension": "FORBIDDEN",
            "decision": "PENDING_HUMAN_PROMOTION",
            "decision_authority": "NONE",
            "b12_open": False,
        }

    v1_inputs = dict(inputs)
    v1_inputs.pop("fixed_horizon_reached", None)
    v1_inputs["sample_n"] = max(n, V1.M06_FINAL_REQUIRED_N)
    out = V1.evaluate(v1_inputs)

    reasons = [
        reason for reason in out["all_qualification_reasons"]
        if reason != "INSUFFICIENT_SAMPLE"
    ]
    merged_limitations = _ordered_unique(
        list(out["qualification_limitations"]) + limitations
    )

    verdict = out["evidence_verdict"]
    qualification_status = out["qualification_status"]
    qualification_reason = out["qualification_reason"]
    if qualification_reason == "INSUFFICIENT_SAMPLE":
        qualification_reason = reasons[0] if reasons else "INCONCLUSIVE"

    return {
        **out,
        "collection_state": "FIXED_HORIZON_REACHED",
        "all_qualification_reasons": reasons,
        "qualification_limitations": merged_limitations,
        "qualification_reason": qualification_reason,
        "planning_target_status": planning_status,
        "reference_planning_n": REFERENCE_PLANNING_N,
        "same_experiment_extension": "FORBIDDEN",
        "evidence_verdict": verdict,
        "qualification_status": qualification_status,
        "b12_open": False,
    }
