from __future__ import annotations

import math

CONTRACT = "ATDS_SMF03_EVIDENCE_GOVERNANCE_V0_1"

EXPOSURE_STATES = ("PRISTINE", "EXPOSED", "CONTAMINATED")
EXPOSURE_EVENTS = (
    "CONFIRMATORY_EVALUATION",
    "EXPLORATORY_INSPECTION",
    "HYPOTHESIS_REDESIGN_USING_EVIDENCE",
)
SEARCH_STATUSES = (
    "NO_RELEVANT_MULTIPLICITY",
    "KNOWN_SEARCH_UNIVERSE",
    "PARTIAL_SEARCH_UNIVERSE",
    "UNKNOWN_SEARCH_UNIVERSE",
)


def _finite_number(value) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _finite_sample(values):
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


def _clean_label(value, error):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(error)
    return value.strip()


def _sign(value):
    if value > 0.0:
        return 1
    if value < 0.0:
        return -1
    return 0


def influence_analysis(values, *, unit_ids, materiality_abs_delta):
    sample = _finite_sample(values)
    if not isinstance(unit_ids, (list, tuple)) or len(unit_ids) != len(sample):
        raise ValueError("UNIT_ID_LENGTH_MISMATCH")
    if not _finite_number(materiality_abs_delta) or float(materiality_abs_delta) < 0.0:
        raise ValueError("INVALID_MATERIALITY_THRESHOLD")

    clean_units = [_clean_label(x, "INVALID_UNIT_ID") for x in unit_ids]
    unique_units = []
    for unit in clean_units:
        if unit not in unique_units:
            unique_units.append(unit)
    if len(unique_units) < 2:
        raise ValueError("INSUFFICIENT_DEPENDENCE_UNITS")

    baseline = _mean(sample)
    analyses = []
    max_abs_delta = 0.0
    sign_reversal = False

    for unit in unique_units:
        remaining = [
            value
            for value, observed_unit in zip(sample, clean_units)
            if observed_unit != unit
        ]
        if not remaining:
            raise ValueError("INSUFFICIENT_DEPENDENCE_UNITS")
        remaining_mean = _mean(remaining)
        delta = remaining_mean - baseline
        reversal = (
            _sign(baseline) != 0
            and _sign(remaining_mean) != 0
            and _sign(baseline) != _sign(remaining_mean)
        )
        max_abs_delta = max(max_abs_delta, abs(delta))
        sign_reversal = sign_reversal or reversal
        analyses.append(
            {
                "unit_id": unit,
                "remaining_n": len(remaining),
                "remaining_mean": remaining_mean,
                "delta_from_baseline": delta,
                "sign_reversal": reversal,
            }
        )

    threshold = float(materiality_abs_delta)
    return {
        "n": len(sample),
        "unique_unit_count": len(unique_units),
        "baseline_mean": baseline,
        "materiality_abs_delta": threshold,
        "leave_one_unit_out": analyses,
        "max_abs_delta": max_abs_delta,
        "material_influence": max_abs_delta >= threshold,
        "sign_reversal_detected": sign_reversal,
    }


def attrition_analysis(
    *,
    included,
    reasons,
    strata,
    max_inclusion_rate_gap,
):
    if not isinstance(included, (list, tuple)) or not included:
        raise ValueError("EMPTY_SAMPLE")
    n = len(included)
    if not isinstance(reasons, (list, tuple)) or len(reasons) != n:
        raise ValueError("REASON_LENGTH_MISMATCH")
    if not isinstance(strata, (list, tuple)) or len(strata) != n:
        raise ValueError("STRATUM_LENGTH_MISMATCH")
    if not _finite_number(max_inclusion_rate_gap) or not (0.0 <= float(max_inclusion_rate_gap) <= 1.0):
        raise ValueError("INVALID_INCLUSION_RATE_GAP_THRESHOLD")

    clean_included = []
    clean_strata = []
    reason_counts = {}
    for index, flag in enumerate(included):
        if not isinstance(flag, bool):
            raise ValueError("INCLUSION_INDICATOR_NOT_BOOLEAN")
        clean_included.append(flag)
        clean_strata.append(_clean_label(strata[index], "INVALID_STRATUM"))
        if not flag:
            reason = _clean_label(reasons[index], "EXCLUSION_REASON_REQUIRED")
            reason_counts[reason] = reason_counts.get(reason, 0) + 1

    stratum_names = sorted(set(clean_strata))
    stats = {}
    rates = []
    for name in stratum_names:
        positions = [i for i, value in enumerate(clean_strata) if value == name]
        included_count = sum(1 for i in positions if clean_included[i])
        total = len(positions)
        rate = included_count / total
        rates.append(rate)
        stats[name] = {
            "total": total,
            "included": included_count,
            "excluded": total - included_count,
            "inclusion_rate": rate,
        }

    gap = max(rates) - min(rates) if rates else 0.0
    threshold = float(max_inclusion_rate_gap)
    return {
        "n": n,
        "included_count": sum(clean_included),
        "excluded_count": n - sum(clean_included),
        "overall_inclusion_rate": sum(clean_included) / n,
        "excluded_reason_counts": dict(sorted(reason_counts.items())),
        "strata": stats,
        "max_inclusion_rate_gap": threshold,
        "observed_inclusion_rate_gap": gap,
        "material_selection_asymmetry": gap >= threshold,
    }


def exposure_transition(current_state, event):
    if current_state not in EXPOSURE_STATES:
        raise ValueError("INVALID_EXPOSURE_STATE")
    if event == "RESET_TO_PRISTINE":
        if current_state != "PRISTINE":
            raise ValueError("PRISTINE_RESET_FORBIDDEN")
        return {"before": current_state, "event": event, "after": "PRISTINE"}
    if event not in EXPOSURE_EVENTS:
        raise ValueError("INVALID_EXPOSURE_EVENT")

    if current_state == "CONTAMINATED":
        after = "CONTAMINATED"
    elif event == "HYPOTHESIS_REDESIGN_USING_EVIDENCE":
        after = "CONTAMINATED"
    elif current_state == "PRISTINE":
        after = "EXPOSED"
    else:
        after = "EXPOSED"

    return {
        "before": current_state,
        "event": event,
        "after": after,
    }


def temporal_stability(
    values,
    *,
    strata,
    declared_strata,
    strata_predeclared,
    minimum_n_per_stratum,
    max_mean_spread,
):
    sample = _finite_sample(values)
    if strata_predeclared is not True:
        raise ValueError("POST_HOC_CONFIRMATORY_STRATA_FORBIDDEN")
    if not isinstance(strata, (list, tuple)) or len(strata) != len(sample):
        raise ValueError("STRATUM_LENGTH_MISMATCH")
    if not isinstance(declared_strata, (list, tuple)) or not declared_strata:
        raise ValueError("DECLARED_STRATA_REQUIRED")
    if (
        isinstance(minimum_n_per_stratum, bool)
        or not isinstance(minimum_n_per_stratum, int)
        or minimum_n_per_stratum <= 0
    ):
        raise ValueError("INVALID_MINIMUM_N_PER_STRATUM")
    if not _finite_number(max_mean_spread) or float(max_mean_spread) < 0.0:
        raise ValueError("INVALID_MAX_MEAN_SPREAD")

    declared = [_clean_label(x, "INVALID_DECLARED_STRATUM") for x in declared_strata]
    if len(set(declared)) != len(declared):
        raise ValueError("DUPLICATE_DECLARED_STRATUM")
    observed = [_clean_label(x, "INVALID_STRATUM") for x in strata]
    if any(label not in declared for label in observed):
        raise ValueError("UNDECLARED_STRATUM")

    details = {}
    insufficient = []
    means = []
    for label in declared:
        group = [x for x, group_label in zip(sample, observed) if group_label == label]
        if len(group) < minimum_n_per_stratum:
            insufficient.append(label)
        group_mean = _mean(group) if group else None
        if group_mean is not None:
            means.append(group_mean)
        details[label] = {
            "n": len(group),
            "mean": group_mean,
        }

    threshold = float(max_mean_spread)
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


def search_provenance_gate(
    status,
    *,
    registry_candidate_ids,
    explicit_n_trials,
    provenance_complete,
):
    if status not in SEARCH_STATUSES:
        raise ValueError("INVALID_SEARCH_UNIVERSE_STATUS")
    if not isinstance(registry_candidate_ids, (list, tuple)):
        raise ValueError("REGISTRY_CANDIDATE_IDS_INVALID")
    clean_ids = [_clean_label(x, "INVALID_REGISTRY_CANDIDATE_ID") for x in registry_candidate_ids]
    if len(set(clean_ids)) != len(clean_ids):
        raise ValueError("DUPLICATE_REGISTRY_CANDIDATE_ID")
    if not isinstance(provenance_complete, bool):
        raise ValueError("PROVENANCE_COMPLETENESS_NOT_BOOLEAN")

    if status == "KNOWN_SEARCH_UNIVERSE":
        if (
            isinstance(explicit_n_trials, bool)
            or not isinstance(explicit_n_trials, int)
            or explicit_n_trials <= 0
        ):
            raise ValueError("EXPLICIT_N_TRIALS_REQUIRED")
        if provenance_complete is not True:
            raise ValueError("KNOWN_UNIVERSE_PROVENANCE_INCOMPLETE")
        n_trials = explicit_n_trials
    elif status in ("PARTIAL_SEARCH_UNIVERSE", "UNKNOWN_SEARCH_UNIVERSE"):
        if explicit_n_trials is not None:
            raise ValueError("N_TRIALS_NOT_DEFENSIBLE_FOR_UNRESOLVED_UNIVERSE")
        n_trials = None
    else:
        if explicit_n_trials is not None:
            raise ValueError("N_TRIALS_NOT_APPLICABLE")
        n_trials = None

    return {
        "status": status,
        "registry_candidate_ids": clean_ids,
        "registry_record_count": len(clean_ids),
        "provenance_complete": provenance_complete,
        "n_trials": n_trials,
        "n_trials_source": "EXPLICIT_GOVERNED_INPUT" if n_trials is not None else None,
    }
