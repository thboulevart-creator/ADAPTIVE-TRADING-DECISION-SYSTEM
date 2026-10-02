from __future__ import annotations

import math
import random
from statistics import NormalDist

CONTRACT = "ATDS_SMF03_DEPENDENCE_INFERENCE_V0_1"

ACF_ESTIMATORS = ("BIASED", "ADJUSTED")
BOOTSTRAP_SCHEMES = ("IID", "MOVING_BLOCK")
INTERVAL_METHODS = ("PERCENTILE", "BASIC")
NORMAL_MEAN_MODEL = "NORMAL_MEAN_KNOWN_SIGMA"


def _finite_number(value) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _sample(values):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("EMPTY_SAMPLE")
    out = []
    for value in values:
        if not _finite_number(value):
            raise ValueError("NONFINITE_OBSERVATION")
        out.append(float(value))
    return out


def _mean(values):
    return math.fsum(values) / len(values)


def _linear_quantile(ordered, p):
    if len(ordered) == 1:
        return ordered[0]
    h = (len(ordered) - 1) * p
    lo = math.floor(h)
    hi = math.ceil(h)
    if lo == hi:
        return ordered[lo]
    w = h - lo
    return ordered[lo] + w * (ordered[hi] - ordered[lo])


def dependence_diagnostics(
    values,
    *,
    lags,
    estimator,
    abs_threshold,
    structural_flags,
):
    sample = _sample(values)
    n = len(sample)
    if not isinstance(lags, (list, tuple)) or not lags:
        raise ValueError("LAGS_REQUIRED")
    clean_lags = []
    for lag in lags:
        if isinstance(lag, bool) or not isinstance(lag, int) or lag <= 0 or lag >= n:
            raise ValueError("LAG_OUT_OF_RANGE")
        if lag in clean_lags:
            raise ValueError("DUPLICATE_LAG")
        clean_lags.append(lag)
    if estimator not in ACF_ESTIMATORS:
        raise ValueError("ACF_ESTIMATOR_UNSUPPORTED")
    if not _finite_number(abs_threshold) or float(abs_threshold) <= 0.0:
        raise ValueError("INVALID_ACF_THRESHOLD")
    if not isinstance(structural_flags, (list, tuple)):
        raise ValueError("STRUCTURAL_FLAGS_INVALID")
    flags = []
    for flag in structural_flags:
        if not isinstance(flag, str) or not flag.strip():
            raise ValueError("STRUCTURAL_FLAG_INVALID")
        flags.append(flag.strip())

    mean = _mean(sample)
    denominator = math.fsum((x - mean) ** 2 for x in sample)
    if denominator == 0.0:
        raise ValueError("ZERO_VARIANCE_ACF_UNDEFINED")

    acf = {}
    for lag in clean_lags:
        numerator = math.fsum(
            (sample[index] - mean) * (sample[index - lag] - mean)
            for index in range(lag, n)
        )
        if estimator == "BIASED":
            rho = numerator / denominator
        else:
            rho = (numerator * n) / ((n - lag) * denominator)
        acf[str(lag)] = rho

    threshold = float(abs_threshold)
    if flags:
        status = "STRUCTURALLY_PRESENT"
    elif any(abs(value) >= threshold for value in acf.values()):
        status = "DETECTED_WITHIN_TESTED_LAGS"
    else:
        status = "NO_MATERIAL_DEPENDENCE_FOUND_WITHIN_TESTED_LAGS"

    return {
        "n": n,
        "estimator": estimator,
        "lags": clean_lags,
        "acf": acf,
        "abs_threshold": threshold,
        "structural_flags": flags,
        "status": status,
    }


def _bootstrap_replicate_mean(sample, *, scheme, rng, block_length):
    n = len(sample)
    if scheme == "IID":
        replicate = [sample[rng.randrange(n)] for _ in range(n)]
        return _mean(replicate)

    replicate = []
    max_start = n - block_length
    while len(replicate) < n:
        start = rng.randrange(max_start + 1)
        replicate.extend(sample[start : start + block_length])
    return _mean(replicate[:n])


def bootstrap_mean_ci(
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
    sample = _sample(values)
    if not isinstance(stationarity_status, str) or not stationarity_status.strip():
        raise ValueError("STATIONARITY_STATUS_REQUIRED")
    if stationarity_status == "UNRESOLVED_NONSTATIONARY":
        raise ValueError("UNRESOLVED_NONSTATIONARITY")
    if scheme not in BOOTSTRAP_SCHEMES:
        raise ValueError("BOOTSTRAP_SCHEME_UNSUPPORTED")
    if interval_method not in INTERVAL_METHODS:
        raise ValueError("INTERVAL_METHOD_UNSUPPORTED")
    if not _finite_number(confidence_level) or not (0.0 < float(confidence_level) < 1.0):
        raise ValueError("INVALID_CONFIDENCE_LEVEL")
    if isinstance(replications, bool) or not isinstance(replications, int) or replications <= 0:
        raise ValueError("INVALID_REPLICATIONS")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("SEED_REQUIRED")

    if scheme == "IID":
        if iid_justified is not True:
            raise ValueError("IID_NOT_JUSTIFIED")
        effective_block_length = None
    else:
        if (
            isinstance(block_length, bool)
            or not isinstance(block_length, int)
            or block_length <= 0
            or block_length > len(sample)
        ):
            raise ValueError("BLOCK_LENGTH_REQUIRED")
        effective_block_length = block_length

    rng = random.Random(seed)
    replicate_means = [
        _bootstrap_replicate_mean(
            sample,
            scheme=scheme,
            rng=rng,
            block_length=effective_block_length,
        )
        for _ in range(replications)
    ]
    ordered = sorted(replicate_means)
    alpha = (1.0 - float(confidence_level)) / 2.0
    q_low = _linear_quantile(ordered, alpha)
    q_high = _linear_quantile(ordered, 1.0 - alpha)
    point = _mean(sample)

    if interval_method == "PERCENTILE":
        lower, upper = q_low, q_high
    else:
        lower, upper = 2.0 * point - q_high, 2.0 * point - q_low

    return {
        "n": len(sample),
        "scheme": scheme,
        "interval_method": interval_method,
        "confidence_level": float(confidence_level),
        "replications": replications,
        "seed": seed,
        "stationarity_status": stationarity_status,
        "iid_justified": iid_justified if scheme == "IID" else None,
        "block_length": effective_block_length,
        "point_estimate": point,
        "lower": lower,
        "upper": upper,
    }


def required_n_for_mean_precision(
    *,
    model_ref,
    stddev,
    half_width,
    confidence_level,
):
    if model_ref != NORMAL_MEAN_MODEL:
        raise ValueError("PRECISION_MODEL_UNSUPPORTED")
    if not _finite_number(stddev) or float(stddev) <= 0.0:
        raise ValueError("INVALID_STANDARD_DEVIATION")
    if not _finite_number(half_width) or float(half_width) <= 0.0:
        raise ValueError("INVALID_HALF_WIDTH")
    if not _finite_number(confidence_level) or not (0.0 < float(confidence_level) < 1.0):
        raise ValueError("INVALID_CONFIDENCE_LEVEL")

    z = NormalDist().inv_cdf(0.5 + float(confidence_level) / 2.0)
    raw_n = (z * float(stddev) / float(half_width)) ** 2
    return {
        "model_ref": model_ref,
        "stddev": float(stddev),
        "half_width": float(half_width),
        "confidence_level": float(confidence_level),
        "required_n": max(1, math.ceil(raw_n)),
    }


def _normal_mean_power(n, *, effect_size, stddev, alpha, alternative):
    distribution = NormalDist()
    delta = float(effect_size) * math.sqrt(n) / float(stddev)

    if alternative == "GREATER":
        critical = distribution.inv_cdf(1.0 - float(alpha))
        return 1.0 - distribution.cdf(critical - delta)
    if alternative == "LESS":
        critical = distribution.inv_cdf(float(alpha))
        return distribution.cdf(critical - delta)
    if alternative == "TWO_SIDED":
        critical = distribution.inv_cdf(1.0 - float(alpha) / 2.0)
        return (
            1.0
            - distribution.cdf(critical - delta)
            + distribution.cdf(-critical - delta)
        )
    raise ValueError("ALTERNATIVE_UNSUPPORTED")


def required_n_for_mean_power(
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
    if not _finite_number(effect_size) or float(effect_size) == 0.0:
        raise ValueError("INVALID_EFFECT_SIZE")
    if not _finite_number(stddev) or float(stddev) <= 0.0:
        raise ValueError("INVALID_STANDARD_DEVIATION")
    if not _finite_number(alpha) or not (0.0 < float(alpha) < 1.0):
        raise ValueError("INVALID_ALPHA")
    if not _finite_number(target_power) or not (0.0 < float(target_power) < 1.0):
        raise ValueError("INVALID_TARGET_POWER")
    if isinstance(max_n, bool) or not isinstance(max_n, int) or max_n <= 0:
        raise ValueError("INVALID_MAX_N")
    if alternative == "GREATER" and float(effect_size) <= 0.0:
        raise ValueError("EFFECT_DIRECTION_MISMATCH")
    if alternative == "LESS" and float(effect_size) >= 0.0:
        raise ValueError("EFFECT_DIRECTION_MISMATCH")
    if alternative not in ("GREATER", "LESS", "TWO_SIDED"):
        raise ValueError("ALTERNATIVE_UNSUPPORTED")

    for n in range(1, max_n + 1):
        power = _normal_mean_power(
            n,
            effect_size=float(effect_size),
            stddev=float(stddev),
            alpha=float(alpha),
            alternative=alternative,
        )
        if power >= float(target_power):
            return {
                "model_ref": model_ref,
                "effect_size": float(effect_size),
                "stddev": float(stddev),
                "alpha": float(alpha),
                "target_power": float(target_power),
                "alternative": alternative,
                "effect_source": effect_source,
                "required_n": n,
                "achieved_power": power,
                "max_n": max_n,
            }

    raise ValueError("TARGET_POWER_UNREACHABLE_WITHIN_MAX_N")
