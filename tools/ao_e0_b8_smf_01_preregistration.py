from __future__ import annotations
import math

M04_ESTIMATOR = "ADJUSTED"
M04_ABS_THRESHOLD = 0.05
M05_SCHEME = "MOVING_BLOCK"
M05_INTERVAL_METHOD = "PERCENTILE"
M05_CONFIDENCE_LEVEL = 0.99
M05_REPLICATIONS = 50000
M05_SEED = 21449402
M07_MATERIALITY_ABS_DELTA = 5.0
M08_MAX_INCLUSION_RATE_GAP = 0.05

def m04_lags(n: int) -> list[int]:
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("INSUFFICIENT_N_FOR_M04")
    max_lag = min(n - 1, math.ceil(n ** (1.0 / 3.0)))
    return list(range(1, max_lag + 1))

def m05_block_length(n: int) -> int:
    lags = m04_lags(n)
    return min(n, 1 + max(lags))

def candidate_for_n(n: int) -> dict:
    return {
        "m04": {
            "estimator": M04_ESTIMATOR,
            "lags": m04_lags(n),
            "abs_threshold": M04_ABS_THRESHOLD,
        },
        "m05": {
            "scheme": M05_SCHEME,
            "interval_method": M05_INTERVAL_METHOD,
            "confidence_level": M05_CONFIDENCE_LEVEL,
            "replications": M05_REPLICATIONS,
            "seed": M05_SEED,
            "block_length": m05_block_length(n),
        },
        "m07": {"materiality_abs_delta": M07_MATERIALITY_ABS_DELTA},
        "m08": {"max_inclusion_rate_gap": M08_MAX_INCLUSION_RATE_GAP},
    }

if __name__ == "__main__":
    import json
    print(json.dumps(candidate_for_n(58927), sort_keys=True, indent=2))
