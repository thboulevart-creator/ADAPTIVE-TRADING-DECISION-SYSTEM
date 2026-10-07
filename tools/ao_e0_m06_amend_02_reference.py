from __future__ import annotations

import math
from statistics import NormalDist

S = 1791284400000
E = 1822820400000
N_REF = 58927
SIG = 336.4106561689863

def is_in_window(t):
    t = int(t)
    return t >= S and t < E

def done(t):
    return int(t) >= E

def reference_metrics(n):
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("INVALID_N")
    if n == 0:
        hw = None
        p = None
    else:
        z = NormalDist().inv_cdf(0.995)
        hw = z * SIG / math.sqrt(n)
        za = NormalDist().inv_cdf(0.99)
        p = 1.0 - NormalDist().cdf(za - 5.0 * math.sqrt(n) / SIG)
    return {
        "actual_closed_trade_count": n,
        "reference_planning_n": N_REF,
        "reference_planning_n_reached": n >= N_REF,
        "planning_model_precision_half_width_at_actual_n": hw,
        "planning_model_power_at_actual_n": p,
        "inference_analyzable_by_existing_m04_minimum": n >= 2,
    }

def reference_terminal(now_ms, n, complete, blocked):
    if not done(now_ms):
        return {"state": "WAIT_NOT_READY", "extension_authorized": False}
    m = reference_metrics(n)
    if not complete:
        return {"state": "INCONCLUSIVE_DATA_INCOMPLETE", "extension_authorized": False, **m}
    if not m["inference_analyzable_by_existing_m04_minimum"]:
        return {"state": "INCONCLUSIVE_INFERENCE_NOT_ANALYZABLE", "extension_authorized": False, **m}
    if blocked:
        return {"state": "INCONCLUSIVE_VALIDITY_BLOCKED", "extension_authorized": False, **m}
    return {"state": "READY_FOR_EXISTING_DR01_INFERENCE_PATHS", "extension_authorized": False, **m}
