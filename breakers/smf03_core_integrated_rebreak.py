from __future__ import annotations

import ast
import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION_PATH = ROOT / "tools/smf03_core_foundation.py"
DI_PATH = ROOT / "tools/smf03_dependence_inference.py"
EG_PATH = ROOT / "tools/smf03_evidence_governance.py"
FOUNDATION_REF_PATH = ROOT / "tools/smf03_core_foundation_reference.py"
DI_REF_PATH = ROOT / "tools/smf03_dependence_inference_reference.py"
EG_REF_PATH = ROOT / "tools/smf03_evidence_governance_reference.py"

FORBIDDEN_CLAIMS = {
    "STRATEGY_QUALIFIED",
    "EDGE_GENERALIZABLE",
    "LIVE_PROFITABILITY",
    "DEPLOYMENT_AUTHORIZED",
    "INDEPENDENCE_PROVEN",
    "MODEL_VALID",
    "OUTLIERS_INVALID",
    "MISSINGNESS_IGNORABLE",
    "PRISTINE_RESET",
    "POST_HOC_REGIME_CONFIRMED",
    "AUTOMATIC_N_TRIALS",
}


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _modules():
    return (
        _load(FOUNDATION_PATH, "smf03_core_foundation_integrated"),
        _load(DI_PATH, "smf03_dependence_inference_integrated"),
        _load(EG_PATH, "smf03_evidence_governance_integrated"),
    )


def _references():
    return (
        _load(FOUNDATION_REF_PATH, "smf03_core_foundation_reference_integrated"),
        _load(DI_REF_PATH, "smf03_dependence_inference_reference_integrated"),
        _load(EG_REF_PATH, "smf03_evidence_governance_reference_integrated"),
    )


def _activation_kwargs(method="M02", state="ACTIVATED"):
    return {
        "claim_definition_ref": "sha256:claim-core-integrated",
        "failure_mode_ref": "FM-INTEGRATED",
        "method_family_ref": method,
        "validity_scope_ref": "sha256:scope-core-integrated",
        "assumption_set_ref": "sha256:assumptions-core-integrated",
        "activation_reason": "Synthetic integrated qualification",
        "activation_rule": "SYNTHETIC_INTEGRATED_RULE",
        "parameter_selection_policy": {"selector": "PREDECLARED_SYNTHETIC"},
        "dependency_refs": ["sha256:m01-integrated"],
        "activation_state": state,
    }


def _all_strings(value):
    found = set()
    if isinstance(value, dict):
        for key, item in value.items():
            found.add(str(key).upper())
            found.update(_all_strings(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_all_strings(item))
    elif isinstance(value, str):
        found.add(value.upper())
    return found


def test_core_01_exact_runtime_contracts_load_together():
    foundation, di, eg = _modules()
    assert foundation.CONTRACT == "ATDS_SMF03_CORE_FOUNDATION_V0_1"
    assert di.CONTRACT == "ATDS_SMF03_DEPENDENCE_INFERENCE_V0_1"
    assert eg.CONTRACT == "ATDS_SMF03_EVIDENCE_GOVERNANCE_V0_1"


def test_core_02_adopted_core_families_are_addressable():
    foundation, _, _ = _modules()
    required = {f"M{i:02d}" for i in range(1, 12)}
    assert required <= set(foundation.ALLOWED_METHOD_FAMILIES)


def test_core_03_activation_identity_changes_with_method_or_state():
    foundation, _, _ = _modules()
    m02 = foundation.create_activation_record(**_activation_kwargs("M02", "ACTIVATED"))
    m03 = foundation.create_activation_record(**_activation_kwargs("M03", "ACTIVATED"))
    blocked = foundation.create_activation_record(**_activation_kwargs("M02", "BLOCKED"))
    assert len({m02["activation_digest"], m03["activation_digest"], blocked["activation_digest"]}) == 3


def test_core_04_post_result_activation_is_forbidden_across_core():
    foundation, _, _ = _modules()
    kwargs = _activation_kwargs("M07", "ACTIVATED")
    with pytest.raises(ValueError, match="METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE"):
        foundation.create_activation_record(**kwargs, result_exposed=True)


def test_core_05_positive_gross_cannot_hide_negative_net_effect():
    foundation, _, _ = _modules()
    result = foundation.net_economic_effect(
        [0.20, 0.20],
        costs=[0.25, 0.30],
        minimum_effect=0.0,
    )
    assert result["gross_mean"] > 0.0
    assert result["net_mean"] < 0.0
    assert result["threshold_relation"] == "BELOW"


def test_core_06_low_tested_acf_does_not_auto_authorize_iid():
    _, di, _ = _modules()
    diagnostic = di.dependence_diagnostics(
        [1.0, -1.0, -1.0, 1.0],
        lags=[1],
        estimator="BIASED",
        abs_threshold=0.9,
        structural_flags=[],
    )
    assert diagnostic["status"] == "NO_MATERIAL_DEPENDENCE_FOUND_WITHIN_TESTED_LAGS"
    with pytest.raises(ValueError, match="IID_NOT_JUSTIFIED"):
        di.bootstrap_mean_ci(
            [1.0, -1.0, -1.0, 1.0],
            scheme="IID",
            interval_method="PERCENTILE",
            confidence_level=0.8,
            replications=51,
            seed=5,
            stationarity_status="STATIONARY",
            iid_justified=False,
        )


def test_core_07_structural_dependence_and_influence_units_remain_visible():
    _, di, eg = _modules()
    diagnostic = di.dependence_diagnostics(
        [1.0, 1.0, -1.0, -1.0],
        lags=[1],
        estimator="BIASED",
        abs_threshold=2.0,
        structural_flags=["SHARED_EVENT"],
    )
    influence = eg.influence_analysis(
        [1.0, 1.0, -1.0, -1.0],
        unit_ids=["A", "A", "B", "B"],
        materiality_abs_delta=1.0,
    )
    assert diagnostic["status"] == "STRUCTURALLY_PRESENT"
    assert influence["unique_unit_count"] == 2
    assert influence["material_influence"] is True


def test_core_08_attrition_and_stability_do_not_compensate_each_other():
    _, _, eg = _modules()
    attrition = eg.attrition_analysis(
        included=[True, False, True, True],
        reasons=[None, "GAP", None, None],
        strata=["A", "A", "B", "B"],
        max_inclusion_rate_gap=0.4,
    )
    stability = eg.temporal_stability(
        [1.0, 1.0, 1.0, 1.0],
        strata=["A", "A", "B", "B"],
        declared_strata=["A", "B"],
        strata_predeclared=True,
        minimum_n_per_stratum=2,
        max_mean_spread=0.0,
    )
    assert attrition["material_selection_asymmetry"] is True
    assert stability["status"] == "STABLE_WITHIN_DECLARED_TOLERANCE"


def test_core_09_oos_exposure_is_irreversible():
    _, _, eg = _modules()
    exposed = eg.exposure_transition("PRISTINE", "CONFIRMATORY_EVALUATION")
    assert exposed["after"] == "EXPOSED"
    with pytest.raises(ValueError, match="PRISTINE_RESET_FORBIDDEN"):
        eg.exposure_transition(exposed["after"], "RESET_TO_PRISTINE")


def test_core_10_unknown_search_universe_never_infers_trials():
    _, _, eg = _modules()
    gate = eg.search_provenance_gate(
        "UNKNOWN_SEARCH_UNIVERSE",
        registry_candidate_ids=["A", "B", "C"],
        explicit_n_trials=None,
        provenance_complete=False,
    )
    assert gate["registry_record_count"] == 3
    assert gate["n_trials"] is None
    assert gate["n_trials_source"] is None


def test_core_11_post_hoc_regime_cannot_rescue_claim():
    _, _, eg = _modules()
    with pytest.raises(ValueError, match="POST_HOC_CONFIRMATORY_STRATA_FORBIDDEN"):
        eg.temporal_stability(
            [0.0, 1.0, 0.0, 1.0],
            strata=["A", "A", "B", "B"],
            declared_strata=["A", "B"],
            strata_predeclared=False,
            minimum_n_per_stratum=2,
            max_mean_spread=1.0,
        )


def test_core_12_independent_reference_paths_still_match():
    foundation, di, eg = _modules()
    fref, diref, egref = _references()

    economic_args = ([0.11, -0.04, 0.08, 0.03],)
    economic_kwargs = {"costs": [0.01, 0.02, 0.01, 0.01], "minimum_effect": 0.02}
    assert foundation.net_economic_effect(*economic_args, **economic_kwargs) == (
        fref.reference_net_economic_effect(*economic_args, **economic_kwargs)
    )

    diag_kwargs = {
        "lags": [1, 2],
        "estimator": "BIASED",
        "abs_threshold": 0.5,
        "structural_flags": [],
    }
    actual = di.dependence_diagnostics([0.1, -0.2, 0.4, 0.3, -0.1], **diag_kwargs)
    expected = diref.reference_dependence_diagnostics([0.1, -0.2, 0.4, 0.3, -0.1], **diag_kwargs)
    actual_acf = actual.pop("acf")
    expected_acf = expected.pop("acf")
    assert actual == expected
    assert actual_acf == pytest.approx(expected_acf, rel=1e-12, abs=1e-15)

    influence_kwargs = {
        "unit_ids": ["A", "A", "B", "C"],
        "materiality_abs_delta": 0.2,
    }
    assert eg.influence_analysis([0.2, 0.1, -0.1, 0.4], **influence_kwargs) == (
        egref.reference_influence_analysis([0.2, 0.1, -0.1, 0.4], **influence_kwargs)
    )


def test_core_13_all_outputs_remain_non_authoritative():
    foundation, di, eg = _modules()
    packet = {
        "activation": foundation.create_activation_record(**_activation_kwargs()),
        "economic": foundation.net_economic_effect([0.1, -0.1], costs=0.01, minimum_effect=0.0),
        "distribution": foundation.ecdf_quantiles([0.1, -0.1], probabilities=[0.1, 0.5, 0.9]),
        "dependence": di.dependence_diagnostics(
            [1.0, -1.0, -1.0, 1.0],
            lags=[1],
            estimator="BIASED",
            abs_threshold=0.9,
            structural_flags=[],
        ),
        "influence": eg.influence_analysis(
            [1.0, -1.0],
            unit_ids=["A", "B"],
            materiality_abs_delta=1.0,
        ),
        "search": eg.search_provenance_gate(
            "UNKNOWN_SEARCH_UNIVERSE",
            registry_candidate_ids=[],
            explicit_n_trials=None,
            provenance_complete=False,
        ),
    }
    assert not (_all_strings(packet) & FORBIDDEN_CLAIMS)


def test_core_14_runtime_modules_remain_stdlib_only():
    allowed = {
        "__future__",
        "hashlib",
        "json",
        "math",
        "random",
        "statistics",
    }
    for path in (FOUNDATION_PATH, DI_PATH, EG_PATH):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split(".")[0])
        assert imports <= allowed


def test_core_15_integrated_packet_is_exactly_deterministic():
    foundation, di, eg = _modules()

    def build():
        return {
            "activation": foundation.create_activation_record(**_activation_kwargs("M02")),
            "economic": foundation.net_economic_effect(
                [0.2, 0.0, -0.1],
                costs=[0.01, 0.02, 0.03],
                minimum_effect=0.0,
            ),
            "ci": di.bootstrap_mean_ci(
                [0.2, 0.0, -0.1],
                scheme="IID",
                interval_method="PERCENTILE",
                confidence_level=0.8,
                replications=101,
                seed=23,
                stationarity_status="STATIONARY",
                iid_justified=True,
            ),
            "exposure": eg.exposure_transition("PRISTINE", "CONFIRMATORY_EVALUATION"),
        }

    assert build() == build()
