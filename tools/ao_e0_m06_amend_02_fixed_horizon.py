from __future__ import annotations

from datetime import datetime, timezone
from math import sqrt
from statistics import NormalDist

CONTRACT = "ATDS_AO_E0_M06_AMEND_02_FIXED_HORIZON_V0_1"
START_MS = 1791284400000
END_MS = 1822820400000
DURATION_MS = 365 * 24 * 3600 * 1000
REFERENCE_N = 58927
SIGMA = 336.4106561689863
EFFECT = 5.0
ALPHA = 0.01
CONFIDENCE = 0.99

def included(decision_time_ms: int) -> bool:
    return START_MS <= int(decision_time_ms) < END_MS

def horizon_reached(now_ms: int) -> bool:
    return int(now_ms) >= END_MS

def planning_metrics(n: int) -> dict:
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("INVALID_N")
    z = NormalDist().inv_cdf((1.0 + CONFIDENCE) / 2.0)
    z_alpha = NormalDist().inv_cdf(1.0 - ALPHA)
    if n == 0:
        half_width = None
        power = None
    else:
        half_width = z * SIGMA / sqrt(n)
        shift = EFFECT * sqrt(n) / SIGMA
        power = 1.0 - NormalDist().cdf(z_alpha - shift)
    return {
        "actual_closed_trade_count": n,
        "reference_planning_n": REFERENCE_N,
        "reference_planning_n_reached": n >= REFERENCE_N,
        "planning_model_precision_half_width_at_actual_n": half_width,
        "planning_model_power_at_actual_n": power,
        "inference_analyzable_by_existing_m04_minimum": n >= 2,
    }

def terminal_state(*, now_ms: int, n: int, data_complete: bool, existing_validity_blocked: bool) -> dict:
    if not horizon_reached(now_ms):
        return {"state": "WAIT_NOT_READY", "extension_authorized": False}
    metrics = planning_metrics(n)
    if not data_complete:
        return {"state": "INCONCLUSIVE_DATA_INCOMPLETE", "extension_authorized": False, **metrics}
    if not metrics["inference_analyzable_by_existing_m04_minimum"]:
        return {"state": "INCONCLUSIVE_INFERENCE_NOT_ANALYZABLE", "extension_authorized": False, **metrics}
    if existing_validity_blocked:
        return {"state": "INCONCLUSIVE_VALIDITY_BLOCKED", "extension_authorized": False, **metrics}
    return {"state": "READY_FOR_EXISTING_DR01_INFERENCE_PATHS", "extension_authorized": False, **metrics}

def identity() -> dict:
    return {
        "start_utc": datetime.fromtimestamp(START_MS / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "end_exclusive_utc": datetime.fromtimestamp(END_MS / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        "duration_ms": DURATION_MS,
        "reference_planning_n": REFERENCE_N,
        "terminal_authority": "FIXED_CALENDAR_END_ONLY",
        "performance_based_extension": False,
    }
