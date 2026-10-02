from __future__ import annotations

import math

CONTRACT = "ATDS_SMF03_EVIDENCE_GOVERNANCE_REFERENCE_V0_1"


def _num(value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(float(value))
    ):
        raise ValueError("NONFINITE_REFERENCE_INPUT")
    return float(value)


def _avg(values):
    return math.fsum(values) / len(values)


def reference_influence_analysis(values, *, unit_ids, materiality_abs_delta):
    sample = [_num(x) for x in values]
    if not sample:
        raise ValueError("EMPTY_SAMPLE")
    if len(unit_ids) != len(sample):
        raise ValueError("UNIT_ID_LENGTH_MISMATCH")
    threshold = _num(materiality_abs_delta)
    if threshold < 0.0:
        raise ValueError("INVALID_MATERIALITY_THRESHOLD")

    order = []
    clean_ids = []
    for raw in unit_ids:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("INVALID_UNIT_ID")
        value = raw.strip()
        clean_ids.append(value)
        if value not in order:
            order.append(value)
    if len(order) < 2:
        raise ValueError("INSUFFICIENT_DEPENDENCE_UNITS")

    baseline = _avg(sample)
    rows = []
    deltas = []
    reversal_any = False
    for omitted in order:
        remaining = []
        for value, unit in zip(sample, clean_ids):
            if unit != omitted:
                remaining.append(value)
        remaining_mean = _avg(remaining)
        delta = remaining_mean - baseline
        deltas.append(abs(delta))
        baseline_sign = 1 if baseline > 0 else (-1 if baseline < 0 else 0)
        remaining_sign = 1 if remaining_mean > 0 else (-1 if remaining_mean < 0 else 0)
        reversal = (
            baseline_sign != 0
            and remaining_sign != 0
            and baseline_sign != remaining_sign
        )
        reversal_any = reversal_any or reversal
        rows.append({
            "unit_id": omitted,
            "remaining_n": len(remaining),
            "remaining_mean": remaining_mean,
            "delta_from_baseline": delta,
            "sign_reversal": reversal,
        })

    maximum = max(deltas)
    return {
        "n": len(sample),
        "unique_unit_count": len(order),
        "baseline_mean": baseline,
        "materiality_abs_delta": threshold,
        "leave_one_unit_out": rows,
        "max_abs_delta": maximum,
        "material_influence": maximum >= threshold,
        "sign_reversal_detected": reversal_any,
    }


def reference_attrition_analysis(
    *,
    included,
    reasons,
    strata,
    max_inclusion_rate_gap,
):
    if not included:
        raise ValueError("EMPTY_SAMPLE")
    if len(reasons) != len(included):
        raise ValueError("REASON_LENGTH_MISMATCH")
    if len(strata) != len(included):
        raise ValueError("STRATUM_LENGTH_MISMATCH")
    threshold = _num(max_inclusion_rate_gap)
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("INVALID_INCLUSION_RATE_GAP_THRESHOLD")

    reason_counts = {}
    clean_strata = []
    included_count = 0
    for i in range(len(included)):
        flag = included[i]
        if not isinstance(flag, bool):
            raise ValueError("INCLUSION_INDICATOR_NOT_BOOLEAN")
        label = strata[i]
        if not isinstance(label, str) or not label.strip():
            raise ValueError("INVALID_STRATUM")
        label = label.strip()
        clean_strata.append(label)
        if flag:
            included_count += 1
        else:
            reason = reasons[i]
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("EXCLUSION_REASON_REQUIRED")
            reason = reason.strip()
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    details = {}
    rates = []
    for label in sorted(set(clean_strata)):
        total = 0
        kept = 0
        for i, observed_label in enumerate(clean_strata):
            if observed_label == label:
                total += 1
                if included[i]:
                    kept += 1
        rate = kept / total
        rates.append(rate)
        details[label] = {
            "total": total,
            "included": kept,
            "excluded": total - kept,
            "inclusion_rate": rate,
        }

    gap = max(rates) - min(rates)
    return {
        "n": len(included),
        "included_count": included_count,
        "excluded_count": len(included) - included_count,
        "overall_inclusion_rate": included_count / len(included),
        "excluded_reason_counts": dict(sorted(reason_counts.items())),
        "strata": details,
        "max_inclusion_rate_gap": threshold,
        "observed_inclusion_rate_gap": gap,
        "material_selection_asymmetry": gap >= threshold,
    }


def reference_temporal_stability(
    values,
    *,
    strata,
    declared_strata,
    strata_predeclared,
    minimum_n_per_stratum,
    max_mean_spread,
):
    sample = [_num(x) for x in values]
    if not sample:
        raise ValueError("EMPTY_SAMPLE")
    if strata_predeclared is not True:
        raise ValueError("POST_HOC_CONFIRMATORY_STRATA_FORBIDDEN")
    if len(strata) != len(sample):
        raise ValueError("STRATUM_LENGTH_MISMATCH")
    if not declared_strata:
        raise ValueError("DECLARED_STRATA_REQUIRED")
    if (
        isinstance(minimum_n_per_stratum, bool)
        or not isinstance(minimum_n_per_stratum, int)
        or minimum_n_per_stratum <= 0
    ):
        raise ValueError("INVALID_MINIMUM_N_PER_STRATUM")
    threshold = _num(max_mean_spread)
    if threshold < 0.0:
        raise ValueError("INVALID_MAX_MEAN_SPREAD")

    declared = []
    for raw in declared_strata:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("INVALID_DECLARED_STRATUM")
        label = raw.strip()
        if label in declared:
            raise ValueError("DUPLICATE_DECLARED_STRATUM")
        declared.append(label)

    observed = []
    for raw in strata:
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("INVALID_STRATUM")
        label = raw.strip()
        if label not in declared:
            raise ValueError("UNDECLARED_STRATUM")
        observed.append(label)

    details = {}
    insufficient = []
    means = []
    for declared_label in declared:
        group = []
        for value, observed_label in zip(sample, observed):
            if observed_label == declared_label:
                group.append(value)
        if len(group) < minimum_n_per_stratum:
            insufficient.append(declared_label)
        mean = _avg(group) if group else None
        if mean is not None:
            means.append(mean)
        details[declared_label] = {"n": len(group), "mean": mean}

    if insufficient:
        status = "INSUFFICIENT_CONDITIONAL_SAMPLE"
        spread = None if len(means) < 2 else max(means) - min(means)
    else:
        spread = max(means) - min(means) if len(means) > 1 else 0.0
        status = (
            "STABLE_WITHIN_DECLARED_TOLERANCE"
            if spread <= threshold
            else "INSTABILITY_DETECTED"
        )

    return {
        "n": len(sample),
        "declared_strata": declared,
        "minimum_n_per_stratum": minimum_n_per_stratum,
        "max_mean_spread": threshold,
        "strata": details,
        "insufficient_strata": insufficient,
        "observed_mean_spread": spread,
        "status": status,
    }
