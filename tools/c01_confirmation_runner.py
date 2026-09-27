from __future__ import annotations

import math
from typing import Any


RUNNER_CONTRACT = "ATDS_C01_CONFIRMATION_RUNNER_V0_1"
RESULT_SCHEMA = "ATDS_C01_CONFIRMATION_RUNNER_RESULT_V0_1"


EXPECTED_BINDINGS = {
    "charter_git_blob":
        "ada0ebf41ecd7ab406d2656ac745ed7003d5b5c1",
    "sealed_model_git_blob":
        "68ee4795462c5dbd5747a7bfdef81716dc84227f",
    "seal_candidate_git_blob":
        "3a6897a63ef2f07a26429342b45977767090651e",
    "final_seal_git_blob":
        "d54ec7840a7bf4eecd94a72f753a02418ea8f543",
    "model_digest_sha256":
        "a8b8b823336fb0f7cd5a6b2bbae80d858603b6ff7567fe5e67e4b20c46726c7f",
}

EXPECTED_INSTRUMENT = "USTECH"
EXPECTED_PRICE_CORE = "USTECH_PROFILE_MINUTE_CORE_V0_1"
EXPECTED_SOURCE_LINEAGE = "SAME_AS_DEVELOPMENT_SOURCE_LINEAGE"

REQUIRED_COMPARISONS = (
    "B2+ABS_VOL",
    "B2+TICK",
)

SPARSE_FLOOR = 500


def _result() -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "execution_status": "PASS",
        "data_class": "SYNTHETIC_ONLY",
        "confirmatory_claim_status": "SYNTHETIC_ONLY",
        "primary_decision_status": "NOT_INTERPRETABLE",
        "primary_confirmation_score_computed": False,
        "real_confirmation_execution": False,
        "scientific_confirmation": "NOT_YET_PERFORMED",
        "comparisons": {},
        "guard_failures": [],
    }


def _block(
    result: dict[str, Any],
    reason: str,
    *,
    not_confirmatory: bool = False,
) -> dict[str, Any]:
    result["execution_status"] = "BLOCKED"
    result["primary_decision_status"] = "NOT_INTERPRETABLE"
    result["guard_failures"].append(reason)

    if not_confirmatory:
        result["confirmatory_claim_status"] = "NOT_CONFIRMATORY"

    return result


def _strict_metric(
    raw: dict[str, Any],
    key: str,
) -> float:
    value = raw[key]

    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
    ):
        raise ValueError(
            f"invalid primary metric type:{key}"
        )

    try:
        numeric = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(
            f"invalid primary metric:{key}"
        ) from exc

    if (
        not math.isfinite(numeric)
        or numeric < 0.0
    ):
        raise ValueError(
            f"invalid primary metric value:{key}"
        )

    return numeric


def _comparison(
    raw: dict[str, Any],
) -> dict[str, float | int]:
    if not isinstance(raw, dict):
        raise ValueError(
            "invalid comparison payload"
        )

    n_raw = raw["n"]

    if (
        type(n_raw) is not int
        or n_raw <= 0
    ):
        raise ValueError(
            "invalid comparison sample count"
        )

    baseline_ll = _strict_metric(
        raw,
        "baseline_log_loss",
    )

    candidate_ll = _strict_metric(
        raw,
        "candidate_log_loss",
    )

    baseline_brier = _strict_metric(
        raw,
        "baseline_brier",
    )

    candidate_brier = _strict_metric(
        raw,
        "candidate_brier",
    )

    return {
        "n": n_raw,
        "baseline_log_loss": baseline_ll,
        "candidate_log_loss": candidate_ll,
        "baseline_brier": baseline_brier,
        "candidate_brier": candidate_brier,
        "delta_log_loss": baseline_ll - candidate_ll,
        "delta_brier": baseline_brier - candidate_brier,
    }


def evaluate_confirmation_case(
    case: dict[str, Any],
) -> dict[str, Any]:
    """
    Pure synthetic evaluator for the qualified C01 test-first harness.

    This function does not read confirmation data, does not access MT5,
    does not refit thresholds/probabilities, and cannot execute a real
    confirmation run.
    """

    result = _result()

    if not isinstance(case, dict):
        return _block(
            result,
            "INVALID_CASE_PAYLOAD",
        )

    if (
        case.get("schema")
        != "ATDS_C01_CONFIRMATION_SYNTHETIC_CASE_V0_1"
    ):
        return _block(
            result,
            "INVALID_CASE_SCHEMA",
        )

    # ------------------------------------------------------------
    # Synthetic-only execution boundary
    # ------------------------------------------------------------

    mode = case.get("mode")
    window = case.get("window")

    if not isinstance(window, dict):
        return _block(
            result,
            "INVALID_WINDOW_CONTROL_BLOCK",
        )

    required_window_bools = (
        "real_execution_requested",
        "partial_window_primary_scoring",
        "early_primary_score_exposed",
    )

    if any(
        key not in window
        or type(window[key]) is not bool
        for key in required_window_bools
    ):
        return _block(
            result,
            "INCOMPLETE_WINDOW_CONTROLS",
        )

    real_requested = window[
        "real_execution_requested"
    ]

    if mode != "SYNTHETIC_ONLY" or real_requested:
        as_of = case.get("as_of_utc")
        fixed_end = window.get("fixed_end_utc")

        if (
            isinstance(as_of, str)
            and isinstance(fixed_end, str)
            and as_of < fixed_end
        ):
            reason = "REAL_EXECUTION_BEFORE_FIXED_WINDOW_CLOSE"
        else:
            reason = "REAL_EXECUTION_NOT_AUTHORIZED"

        return _block(result, reason)

    # ------------------------------------------------------------
    # Frozen object identity
    # ------------------------------------------------------------

    bindings = case.get("bindings")

    if not isinstance(bindings, dict):
        return _block(
            result,
            "INVALID_BINDINGS_BLOCK",
        )

    for key, expected in EXPECTED_BINDINGS.items():
        if bindings.get(key) != expected:
            return _block(
                result,
                f"BINDING_MISMATCH:{key}",
            )

    # ------------------------------------------------------------
    # No confirmation-data access / no early scoring
    # ------------------------------------------------------------

    data = case.get("data")

    if not isinstance(data, dict):
        return _block(
            result,
            "INVALID_DATA_CONTROL_BLOCK",
        )

    if (
        "confirmation_data_accessed_during_development"
        not in data
        or type(
            data[
                "confirmation_data_accessed_during_development"
            ]
        ) is not bool
    ):
        return _block(
            result,
            "CONFIRMATION_DATA_ACCESS_CONTROL_MISSING",
        )

    if data[
        "confirmation_data_accessed_during_development"
    ]:
        return _block(
            result,
            "CONFIRMATION_DATA_ACCESS_DURING_DEVELOPMENT",
        )

    if window.get(
        "partial_window_primary_scoring",
        False,
    ):
        return _block(
            result,
            "PARTIAL_WINDOW_PRIMARY_SCORING",
        )

    if window.get(
        "early_primary_score_exposed",
        False,
    ):
        return _block(
            result,
            "EARLY_PRIMARY_SCORE_EXPOSURE",
        )

    # ------------------------------------------------------------
    # Dataset identity / provenance
    # ------------------------------------------------------------

    if data.get("instrument") != EXPECTED_INSTRUMENT:
        return _block(
            result,
            "WRONG_INSTRUMENT",
        )

    if data.get(
        "price_core_semantics"
    ) != EXPECTED_PRICE_CORE:
        return _block(
            result,
            "WRONG_PRICE_CORE_SEMANTICS",
        )

    if data.get(
        "source_lineage"
    ) != EXPECTED_SOURCE_LINEAGE:
        return _block(
            result,
            "WRONG_SOURCE_LINEAGE",
        )

    pristine = data.get("pristine_status")

    if pristine != "PROVEN_SYNTHETIC":
        return _block(
            result,
            "PRISTINE_NEW_DATA_ELIGIBILITY_UNPROVEN",
            not_confirmatory=True,
        )

    if data.get("dataset_identity_pass") is not True:
        return _block(
            result,
            "DATASET_IDENTITY_FAILURE",
        )

    if data.get("provenance_pass") is not True:
        return _block(
            result,
            "PROVENANCE_FAILURE",
        )

    # ------------------------------------------------------------
    # Frozen model / no refit / no redesign
    # ------------------------------------------------------------

    freeze = case.get("freeze_integrity")

    if not isinstance(freeze, dict):
        return _block(
            result,
            "INVALID_FREEZE_INTEGRITY_BLOCK",
        )

    forbidden_freeze_flags = (
        "confirmation_anchors_entered_fitting",
        "threshold_refit",
        "probability_refit",
        "feature_modified",
        "interaction_modified",
        "post_hoc_charter_modification",
    )

    for key in forbidden_freeze_flags:
        if (
            key not in freeze
            or type(freeze[key]) is not bool
        ):
            return _block(
                result,
                f"FREEZE_CONTROL_MISSING:{key}",
            )

        if freeze[key]:
            return _block(
                result,
                f"FROZEN_MODEL_VIOLATION:{key}",
            )

    # ------------------------------------------------------------
    # Causality / continuity
    # ------------------------------------------------------------

    causality = case.get("causality")

    if not isinstance(causality, dict):
        return _block(
            result,
            "INVALID_CAUSALITY_BLOCK",
        )

    required_causality_bools = (
        "gap_crossing",
        "segment_crossing",
        "exact_minute_continuity",
        "same_segment_continuity",
    )

    if any(
        key not in causality
        or type(causality[key]) is not bool
        for key in required_causality_bools
    ):
        return _block(
            result,
            "INCOMPLETE_CAUSALITY_CONTROLS",
        )

    target_start_offset = causality.get(
        "target_start_offset_minutes"
    )

    if (
        type(target_start_offset) is not int
        or target_start_offset != 1
    ):
        return _block(
            result,
            "TARGET_DOES_NOT_START_AT_T_PLUS_1",
        )

    if causality.get("gap_crossing", False):
        return _block(
            result,
            "GAP_CROSSING",
        )

    if causality.get("segment_crossing", False):
        return _block(
            result,
            "SEGMENT_CROSSING",
        )

    if causality.get(
        "exact_minute_continuity"
    ) is not True:
        return _block(
            result,
            "EXACT_MINUTE_CONTINUITY_FAILURE",
        )

    if causality.get(
        "same_segment_continuity"
    ) is not True:
        return _block(
            result,
            "SAME_SEGMENT_CONTINUITY_FAILURE",
        )

    # ------------------------------------------------------------
    # Forbidden scope expansion
    # ------------------------------------------------------------

    scope = case.get("scope")

    if not isinstance(scope, dict):
        return _block(
            result,
            "INVALID_SCOPE_CONTROL_BLOCK",
        )

    forbidden_scope_flags = (
        "semantic_regime_labels_instantiated",
        "strategy",
        "direction_target",
        "pnl",
        "signals",
        "trades",
        "c02_redesign",
        "winner_selection",
    )

    for key in forbidden_scope_flags:
        if (
            key not in scope
            or type(scope[key]) is not bool
        ):
            return _block(
                result,
                f"SCOPE_CONTROL_MISSING:{key}",
            )

        if scope[key]:
            return _block(
                result,
                f"FORBIDDEN_SCOPE:{key}",
            )

    # ------------------------------------------------------------
    # Required baselines
    # ------------------------------------------------------------

    raw_comparisons = case.get(
        "comparisons"
    )

    if not isinstance(raw_comparisons, dict):
        return _block(
            result,
            "INVALID_COMPARISONS_BLOCK",
        )

    for name in REQUIRED_COMPARISONS:
        if name not in raw_comparisons:
            return _block(
                result,
                f"MISSING_COMPARISON:{name}",
            )

    # ------------------------------------------------------------
    # Guard-first sparse adjudication
    # ------------------------------------------------------------

    counts = case.get(
        "joint_state_counts",
        [],
    )

    if (
        not isinstance(counts, list)
        or len(counts) != 9
        or any(
            isinstance(value, bool)
            or not isinstance(value, int)
            for value in counts
        )
    ):
        return _block(
            result,
            "INVALID_JOINT_STATE_COUNT_VECTOR",
        )

    if any(
        value < SPARSE_FLOOR
        for value in counts
    ):
        return _block(
            result,
            "SPARSE_PRIMARY_JOINT_STATE",
        )

    # ------------------------------------------------------------
    # Primary synthetic metric adjudication
    # delta = baseline - candidate
    # ------------------------------------------------------------

    try:
        comparisons = {
            name: _comparison(
                raw_comparisons[name]
            )
            for name in REQUIRED_COMPARISONS
        }
    except (
        KeyError,
        TypeError,
        ValueError,
    ):
        return _block(
            result,
            "INVALID_PRIMARY_COMPARISON_PAYLOAD",
        )

    expected_primary_n = sum(counts)

    if any(
        comparison["n"] != expected_primary_n
        for comparison in comparisons.values()
    ):
        return _block(
            result,
            "PRIMARY_SAMPLE_COUNT_MISMATCH",
        )

    result["comparisons"] = comparisons

    refuted = any(
        comparison["delta_log_loss"] <= 0
        or comparison["delta_brier"] <= 0
        for comparison in comparisons.values()
    )

    result["execution_status"] = "PASS"

    if refuted:
        result["primary_decision_status"] = "REFUTED"
    else:
        result["primary_decision_status"] = "CONFIRMED"

    return result