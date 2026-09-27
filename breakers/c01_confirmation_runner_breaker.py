from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]

RUNTIME_PATH = Path(
    os.environ.get(
        "C01_CONFIRMATION_RUNNER_MODULE_PATH",
        str(ROOT / "tools/c01_confirmation_runner.py"),
    )
)

CONTRACT_PATH = (
    ROOT
    / "reports/program/evidence/"
      "2026-09-26-C01-CONFIRMATION-EXECUTION-CONTRACT-V0.1.json"
)

EXPECTED_CONTRACT_BLOB = (
    "f6823cfa7b3c582524b3d512d45b16fdc0450ee8"
)

RUNNER_CONTRACT = "ATDS_C01_CONFIRMATION_RUNNER_V0_1"
RESULT_SCHEMA = "ATDS_C01_CONFIRMATION_RUNNER_RESULT_V0_1"


def git_blob_sha1(raw: bytes) -> str:
    h = hashlib.sha1()
    h.update(
        f"blob {len(raw)}\0".encode("ascii")
    )
    h.update(raw)
    return h.hexdigest()


_contract_raw = CONTRACT_PATH.read_bytes()

assert (
    git_blob_sha1(_contract_raw)
    == EXPECTED_CONTRACT_BLOB
)

_contract = json.loads(
    _contract_raw.decode("utf-8")
)

_breakers = _contract["minimum_runner_breakers"]

assert len(_breakers) == 32

CASES = tuple(
    (
        f"B{i:02d}",
        description,
    )
    for i, description in enumerate(
        _breakers,
        start=1,
    )
)


def _runner():
    if not RUNTIME_PATH.is_file():
        pytest.fail(
            "C01_CONFIRMATION_RUNNER_ABSENT_EXPECTED_RED",
            pytrace=False,
        )

    spec = importlib.util.spec_from_file_location(
        "c01_confirmation_runner_under_test",
        RUNTIME_PATH,
    )

    if spec is None or spec.loader is None:
        pytest.fail(
            "candidate module cannot be loaded",
            pytrace=False,
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    required = (
        "RUNNER_CONTRACT",
        "RESULT_SCHEMA",
        "evaluate_confirmation_case",
    )

    missing = [
        name
        for name in required
        if not hasattr(module, name)
    ]

    if missing:
        pytest.fail(
            f"runner surface incomplete: {missing}",
            pytrace=False,
        )

    assert module.RUNNER_CONTRACT == RUNNER_CONTRACT
    assert module.RESULT_SCHEMA == RESULT_SCHEMA

    return module


def _base_case():
    return {
        "schema": "ATDS_C01_CONFIRMATION_SYNTHETIC_CASE_V0_1",
        "mode": "SYNTHETIC_ONLY",
        "as_of_utc": "2026-09-27T00:00:00Z",

        "bindings": {
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
        },

        "window": {
            "eligible_start_utc":
                "2026-05-25T00:00:00Z",
            "fixed_end_utc":
                "2027-05-24T23:59:59Z",
            "earliest_primary_evaluation_utc":
                "2027-05-25T00:00:00Z",
            "real_execution_requested": False,
            "partial_window_primary_scoring": False,
            "early_primary_score_exposed": False,
        },

        "data": {
            "confirmation_data_accessed_during_development":
                False,
            "instrument":
                "USTECH",
            "price_core_semantics":
                "USTECH_PROFILE_MINUTE_CORE_V0_1",
            "source_lineage":
                "SAME_AS_DEVELOPMENT_SOURCE_LINEAGE",
            "pristine_status":
                "PROVEN_SYNTHETIC",
            "dataset_identity_pass":
                True,
            "provenance_pass":
                True,
        },

        "freeze_integrity": {
            "confirmation_anchors_entered_fitting":
                False,
            "threshold_refit":
                False,
            "probability_refit":
                False,
            "feature_modified":
                False,
            "interaction_modified":
                False,
            "post_hoc_charter_modification":
                False,
        },

        "causality": {
            "target_start_offset_minutes":
                1,
            "gap_crossing":
                False,
            "segment_crossing":
                False,
            "exact_minute_continuity":
                True,
            "same_segment_continuity":
                True,
        },

        "joint_state_counts": [
            600, 600, 600,
            600, 600, 600,
            600, 600, 600,
        ],

        "comparisons": {
            "B2+ABS_VOL": {
                "n": 5400,
                "baseline_log_loss": 1.20,
                "candidate_log_loss": 1.00,
                "baseline_brier": 0.80,
                "candidate_brier": 0.70,
            },

            "B2+TICK": {
                "n": 5400,
                "baseline_log_loss": 1.15,
                "candidate_log_loss": 1.00,
                "baseline_brier": 0.76,
                "candidate_brier": 0.70,
            },
        },

        "diagnostic_60m": {
            "B2+ABS_VOL": {
                "delta_log_loss": 0.40,
                "delta_brier": 0.10,
            },

            "B2+TICK": {
                "delta_log_loss": 0.30,
                "delta_brier": 0.08,
            },
        },

        "scope": {
            "semantic_regime_labels_instantiated":
                False,
            "strategy":
                False,
            "direction_target":
                False,
            "pnl":
                False,
            "signals":
                False,
            "trades":
                False,
            "c02_redesign":
                False,
            "winner_selection":
                False,
        },
    }


def _evaluate(module, case):
    result = module.evaluate_confirmation_case(
        copy.deepcopy(case)
    )

    assert isinstance(result, dict)
    assert result["schema"] == RESULT_SCHEMA

    assert (
        result["primary_confirmation_score_computed"]
        is False
    )

    assert (
        result["real_confirmation_execution"]
        is False
    )

    assert (
        result["scientific_confirmation"]
        == "NOT_YET_PERFORMED"
    )

    return result


def _assert_blocked(result):
    assert result["execution_status"] == "BLOCKED"

    assert (
        result["primary_decision_status"]
        == "NOT_INTERPRETABLE"
    )


def _assert_ni(result):
    assert (
        result["primary_decision_status"]
        == "NOT_INTERPRETABLE"
    )

    assert (
        result["primary_decision_status"]
        not in ("CONFIRMED", "REFUTED")
    )


def _negative_primary(case):
    for name in (
        "B2+ABS_VOL",
        "B2+TICK",
    ):
        comp = case["comparisons"][name]

        comp["baseline_log_loss"] = 1.00
        comp["candidate_log_loss"] = 1.10

        comp["baseline_brier"] = 0.70
        comp["candidate_brier"] = 0.80


def test_a0_positive_synthetic_control():
    m = _runner()

    result = _evaluate(
        m,
        _base_case(),
    )

    assert result["execution_status"] == "PASS"
    assert result["data_class"] == "SYNTHETIC_ONLY"

    assert (
        result["confirmatory_claim_status"]
        == "SYNTHETIC_ONLY"
    )

    assert (
        result["primary_decision_status"]
        == "CONFIRMED"
    )


@pytest.mark.parametrize(
    "breaker_id,description",
    CASES,
    ids=[x[0] for x in CASES],
)
def test_breaker_contract(
    breaker_id,
    description,
):
    m = _runner()

    case = _base_case()

    assert (
        description
        == dict(CASES)[breaker_id]
    )

    if breaker_id == "B01":
        case["bindings"]["charter_git_blob"] = "0" * 40
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B02":
        case["bindings"]["sealed_model_git_blob"] = "0" * 40
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B03":
        case["bindings"]["seal_candidate_git_blob"] = "0" * 40
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B04":
        case["bindings"]["model_digest_sha256"] = "0" * 64
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B05":
        assert (
            case["as_of_utc"]
            < case["window"]["fixed_end_utc"]
        )

        case["mode"] = "REAL_CONFIRMATION"

        case["window"][
            "real_execution_requested"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B06":
        case["data"][
            "confirmation_data_accessed_during_development"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B07":
        case["window"][
            "partial_window_primary_scoring"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B08":
        case["window"][
            "early_primary_score_exposed"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B09":
        case["data"]["instrument"] = "NOT_USTECH"
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B10":
        case["data"]["price_core_semantics"] = "DRIFTED"
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B11":
        case["data"]["source_lineage"] = "DRIFTED"
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B12":
        case["data"]["pristine_status"] = "UNPROVEN"

        result = _evaluate(m, case)

        assert (
            result["confirmatory_claim_status"]
            == "NOT_CONFIRMATORY"
        )

    elif breaker_id == "B13":
        case["data"]["pristine_status"] = "UNPROVEN"

        _assert_ni(
            _evaluate(m, case)
        )

    elif breaker_id == "B14":
        case["freeze_integrity"][
            "confirmation_anchors_entered_fitting"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B15":
        case["freeze_integrity"][
            "threshold_refit"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B16":
        case["freeze_integrity"][
            "probability_refit"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B17":
        case["causality"][
            "target_start_offset_minutes"
        ] = 0

        _assert_ni(_evaluate(m, case))

    elif breaker_id == "B18":
        case["causality"]["gap_crossing"] = True
        _assert_ni(_evaluate(m, case))

    elif breaker_id == "B19":
        case["causality"]["segment_crossing"] = True
        _assert_ni(_evaluate(m, case))

    elif breaker_id == "B20":
        del case["comparisons"]["B2+ABS_VOL"]
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B21":
        del case["comparisons"]["B2+TICK"]
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B22":
        c = case["comparisons"]["B2+ABS_VOL"]

        c["baseline_log_loss"] = 1.00
        c["candidate_log_loss"] = 1.10

        c["baseline_brier"] = 0.70
        c["candidate_brier"] = 0.80

        result = _evaluate(m, case)

        assert (
            result["comparisons"][
                "B2+ABS_VOL"
            ]["delta_log_loss"]
            < 0
        )

        assert (
            result["comparisons"][
                "B2+ABS_VOL"
            ]["delta_brier"]
            < 0
        )

        assert (
            result["primary_decision_status"]
            == "REFUTED"
        )

    elif breaker_id == "B23":
        case["joint_state_counts"][0] = 499

        _assert_ni(
            _evaluate(m, case)
        )

    elif breaker_id == "B24":
        _negative_primary(case)

        for diagnostic in (
            case["diagnostic_60m"].values()
        ):
            diagnostic["delta_log_loss"] = 10.0
            diagnostic["delta_brier"] = 10.0

        result = _evaluate(m, case)

        assert (
            result["primary_decision_status"]
            == "REFUTED"
        )

    elif breaker_id == "B25":
        case["scope"][
            "semantic_regime_labels_instantiated"
        ] = True

        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B26":
        for key in (
            "strategy",
            "direction_target",
            "pnl",
            "signals",
            "trades",
        ):
            mutated = copy.deepcopy(case)
            mutated["scope"][key] = True

            _assert_blocked(
                _evaluate(m, mutated)
            )

    elif breaker_id == "B27":
        case["scope"]["c02_redesign"] = True
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B28":
        case["scope"]["winner_selection"] = True
        _assert_blocked(_evaluate(m, case))

    elif breaker_id == "B29":
        for key in (
            "post_hoc_charter_modification",
            "feature_modified",
            "interaction_modified",
        ):
            mutated = copy.deepcopy(case)

            mutated[
                "freeze_integrity"
            ][key] = True

            _assert_blocked(
                _evaluate(m, mutated)
            )

    elif breaker_id == "B30":
        case["joint_state_counts"][0] = 499

        _negative_primary(case)

        _assert_ni(
            _evaluate(m, case)
        )

    elif breaker_id == "B31":
        attacks = (
            ("data", "dataset_identity_pass"),
            ("data", "provenance_pass"),
            ("causality", "exact_minute_continuity"),
            ("causality", "same_segment_continuity"),
        )

        for group, key in attacks:
            mutated = copy.deepcopy(case)

            mutated[group][key] = False

            _negative_primary(mutated)

            _assert_ni(
                _evaluate(m, mutated)
            )

    elif breaker_id == "B32":
        case["data"]["pristine_status"] = "UNPROVEN"

        _negative_primary(case)

        result = _evaluate(m, case)

        assert (
            result["confirmatory_claim_status"]
            == "NOT_CONFIRMATORY"
        )

        _assert_ni(result)

    else:
        raise AssertionError(
            f"unhandled breaker {breaker_id}"
        )
