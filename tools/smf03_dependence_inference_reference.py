from __future__ import annotations

import math
import random
from statistics import NormalDist

CONTRACT = "ATDS_SMF03_DEPENDENCE_INFERENCE_REFERENCE_V0_1"
NORMAL_MEAN_MODEL = "NORMAL_MEAN_KNOWN_SIGMA"


def _num(value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(float(value))
    ):
        raise ValueError("NONFINITE_REFERENCE_INPUT")
    return float(value)


def _vals(values):
    out = [_num(x) for x in values]
    if not out:
        raise ValueError("EMPTY_SAMPLE")
    return out


def _avg(values):
    total = 0.0
    for value in values:
        total = math.fsum((total, value))
    return total / len(values)


def _q(ordered, p):
    if len(ordered) == 1:
        return ordered[0]
    loc = (len(ordered) - 1) * p
    left = int(math.floor(loc))
    right = int(math.ceil(loc))
    if left == right:
        return ordered[left]
    frac = loc - left
    return ordered[left] * (1.0 - frac) + ordered[right] * frac


def reference_dependence_diagnostics(
    values,
    *,
    lags,
    estimator,
    abs_threshold,
    structural_flags,
):
    sample = _vals(values)
    n = len(sample)
    if not lags:
        raise ValueError("LAGS_REQUIRED")
    if estimator not in ("BIASED", "ADJUSTED"):
        raise ValueError("ACF_ESTIMATOR_UNSUPPORTED")
    threshold = _num(abs_threshold)
    if threshold <= 0.0:
        raise ValueError("INVALID_ACF_THRESHOLD")
    center = _avg(sample)
    denom_terms = [(x - center) * (x - center) for x in sample]
    denom = math.fsum(denom_terms)
    if denom == 0.0:
        raise ValueError("ZERO_VARIANCE_ACF_UNDEFINED")
    acf = {}
    clean = []
    for lag in lags:
        if isinstance(lag, bool) or not isinstance(lag, int) or lag <= 0 or lag >= n:
            raise ValueError("LAG_OUT_OF_RANGE")
        if lag in clean:
            raise ValueError("DUPLICATE_LAG")
        clean.append(lag)
        pieces = []
        for index in range(lag, n):
            pieces.append((sample[index] - center) * (sample[index - lag] - center))
        numerator = math.fsum(pieces)
        if estimator == "BIASED":
            rho = numerator / denom
        else:
            rho = (numerator / (n - lag)) / (denom / n)
        acf[str(lag)] = rho
    flags = [str(flag).strip() for flag in structural_flags]
    if flags:
        status = "STRUCTURALLY_PRESENT"
    else:
        found = False
        for value in acf.values():
            if abs(value) >= threshold:
                found = True
        status = (
            "DETECTED_WITHIN_TESTED_LAGS"
            if found
            else "NO_MATERIAL_DEPENDENCE_FOUND_WITHIN_TESTED_LAGS"
        )
    return {
        "n": n,
        "estimator": estimator,
        "lags": clean,
        "acf": acf,
        "abs_threshold": threshold,
        "structural_flags": flags,
        "status": status,
    }


def _replicate(sample, *, scheme, rng, block_length):
    n = len(sample)
    generated = []
    if scheme == "IID":
        for _ in range(n):
            generated.append(sample[rng.randrange(n)])
    else:
        last_start = n - block_length
        while len(generated) < n:
            start = rng.randrange(last_start + 1)
            for offset in range(block_length):
                generated.append(sample[start + offset])
                if len(generated) == n:
                    break
    return _avg(generated)


def reference_bootstrap_mean_ci(
    values,
    *,
    scheme,
    interval_method,
    confidence_level,
    replications,
    seed,
    stationarity_status,
    iid_justified=None,
    block_length=None,
):
    sample = _vals(values)
    if stationarity_status == "UNRESOLVED_NONSTATIONARY":
        raise ValueError("UNRESOLVED_NONSTATIONARITY")
    if scheme not in ("IID", "MOVING_BLOCK"):
        raise ValueError("BOOTSTRAP_SCHEME_UNSUPPORTED")
    if interval_method not in ("PERCENTILE", "BASIC"):
        raise ValueError("INTERVAL_METHOD_UNSUPPORTED")
    confidence = _num(confidence_level)
    if not 0.0 < confidence < 1.0:
        raise ValueError("INVALID_CONFIDENCE_LEVEL")
    if isinstance(replications, bool) or not isinstance(replications, int) or replications <= 0:
        raise ValueError("INVALID_REPLICATIONS")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("SEED_REQUIRED")
    if scheme == "IID":
        if iid_justified is not True:
            raise ValueError("IID_NOT_JUSTIFIED")
        block = None
    else:
        if (
            isinstance(block_length, bool)
            or not isinstance(block_length, int)
            or block_length <= 0
            or block_length > len(sample)
        ):
            raise ValueError("BLOCK_LENGTH_REQUIRED")
        block = block_length
    rng = random.Random(seed)
    means = []
    for _ in range(replications):
        means.append(_replicate(sample, scheme=scheme, rng=rng, block_length=block))
    means.sort()
    alpha = (1.0 - confidence) / 2.0
    lo_q = _q(means, alpha)
    hi_q = _q(means, 1.0 - alpha)
    point = _avg(sample)
    if interval_method == "PERCENTILE":
        lower = lo_q
        upper = hi_q
    else:
        lower = 2.0 * point - hi_q
        upper = 2.0 * point - lo_q
    return {
        "n": len(sample),
        "scheme": scheme,
        "interval_method": interval_method,
        "confidence_level": confidence,
        "replications": replications,
        "seed": seed,
        "stationarity_status": stationarity_status,
        "iid_justified": iid_justified if scheme == "IID" else None,
        "block_length": block,
        "point_estimate": point,
        "lower": lower,
        "upper": upper,
    }


def reference_required_n_for_mean_precision(
    *,
    model_ref,
    stddev,
    half_width,
    confidence_level,
):
    if model_ref != NORMAL_MEAN_MODEL:
        raise ValueError("PRECISION_MODEL_UNSUPPORTED")
    sigma = _num(stddev)
    width = _num(half_width)
    confidence = _num(confidence_level)
    if sigma <= 0.0 or width <= 0.0 or not 0.0 < confidence < 1.0:
        raise ValueError("INVALID_PRECISION_INPUT")
    critical = NormalDist().inv_cdf((1.0 + confidence) / 2.0)
    needed = math.ceil((critical * sigma / width) ** 2)
    return {
        "model_ref": model_ref,
        "stddev": sigma,
        "half_width": width,
        "confidence_level": confidence,
        "required_n": max(1, needed),
    }


def _power(n, effect, sigma, alpha, alternative):
    normal = NormalDist()
    shift = effect * math.sqrt(n) / sigma
    if alternative == "GREATER":
        boundary = normal.inv_cdf(1.0 - alpha)
        return 1.0 - normal.cdf(boundary - shift)
    if alternative == "LESS":
        boundary = normal.inv_cdf(alpha)
        return normal.cdf(boundary - shift)
    boundary = normal.inv_cdf(1.0 - alpha / 2.0)
    return 1.0 - normal.cdf(boundary - shift) + normal.cdf(-boundary - shift)


def reference_required_n_for_mean_power(
    *,
    model_ref,
    effect_size,
    stddev,
    alpha,
    target_power,
    alternative,
    effect_source,
    max_n,
):
    if model_ref != NORMAL_MEAN_MODEL:
        raise ValueError("POWER_MODEL_UNSUPPORTED")
    if effect_source != "PREDECLARED":
        raise ValueError("POST_HOC_POWER_FORBIDDEN")
    effect = _num(effect_size)
    sigma = _num(stddev)
    level = _num(alpha)
    target = _num(target_power)
    if sigma <= 0.0 or effect == 0.0:
        raise ValueError("INVALID_POWER_INPUT")
    if alternative == "GREATER" and effect <= 0.0:
        raise ValueError("EFFECT_DIRECTION_MISMATCH")
    if alternative == "LESS" and effect >= 0.0:
        raise ValueError("EFFECT_DIRECTION_MISMATCH")
    if alternative not in ("GREATER", "LESS", "TWO_SIDED"):
        raise ValueError("ALTERNATIVE_UNSUPPORTED")
    if not 0.0 < level < 1.0 or not 0.0 < target < 1.0:
        raise ValueError("INVALID_POWER_INPUT")
    if isinstance(max_n, bool) or not isinstance(max_n, int) or max_n <= 0:
        raise ValueError("INVALID_MAX_N")
    for n in range(1, max_n + 1):
        achieved = _power(n, effect, sigma, level, alternative)
        if achieved >= target:
            return {
                "model_ref": model_ref,
                "effect_size": effect,
                "stddev": sigma,
                "alpha": level,
                "target_power": target,
                "alternative": alternative,
                "effect_source": effect_source,
                "required_n": n,
                "achieved_power": achieved,
                "max_n": max_n,
            }
    raise ValueError("TARGET_POWER_UNREACHABLE_WITHIN_MAX_N")
