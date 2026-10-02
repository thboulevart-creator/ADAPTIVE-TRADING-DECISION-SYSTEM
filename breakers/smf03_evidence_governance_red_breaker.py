from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SMF-03-EVIDENCE-GOVERNANCE-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(os.environ.get(
    "SMF03_EG_RUNTIME_PATH",
    str(ROOT / "tools/smf03_evidence_governance.py"),
))
REFERENCE_PATH = ROOT / "tools/smf03_evidence_governance_reference.py"

RUNTIME_CONTRACT = "ATDS_SMF03_EVIDENCE_GOVERNANCE_V0_1"
REFERENCE_CONTRACT = "ATDS_SMF03_EVIDENCE_GOVERNANCE_REFERENCE_V0_1"
FORBIDDEN = {
    "OUTLIERS_INVALID",
    "MISSINGNESS_IGNORABLE",
    "PRISTINE_RESET",
    "POST_HOC_REGIME_CONFIRMED",
    "AUTOMATIC_N_TRIALS",
    "STRATEGY_QUALIFIED",
    "EDGE_GENERALIZABLE",
    "LIVE_PROFITABILITY",
}

CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert CONTRACT["schema"] == "ATDS_SMF03_EVIDENCE_GOVERNANCE_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT["test_cases"]] == [f"EG-{i:02d}" for i in range(1, 30)]


def _load(path: Path, name: str):
    if not path.is_file():
        pytest.fail(f"MODULE_ABSENT_EXPECTED_RED:{name}", pytrace=False)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        pytest.fail(f"MODULE_UNLOADABLE:{name}", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _runtime():
    m = _load(RUNTIME_PATH, "smf03_evidence_governance_under_test")
    for name in (
        "CONTRACT",
        "influence_analysis",
        "attrition_analysis",
        "exposure_transition",
        "temporal_stability",
        "search_provenance_gate",
    ):
        assert hasattr(m, name), f"RUNTIME_SURFACE_MISSING:{name}"
    assert m.CONTRACT == RUNTIME_CONTRACT
    return m


def _reference():
    m = _load(REFERENCE_PATH, "smf03_evidence_governance_reference")
    assert m.CONTRACT == REFERENCE_CONTRACT
    return m


def _all_keys(value):
    keys = set()
    if isinstance(value, dict):
        keys.update(str(x).upper() for x in value.keys())
        for item in value.values():
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return keys


def test_eg_01_runtime_contract_and_exact_surface():
    assert _runtime().CONTRACT == RUNTIME_CONTRACT


def test_eg_02_m07_requires_dependence_unit_ids():
    m = _runtime()
    with pytest.raises(ValueError, match="UNIT_ID_LENGTH_MISMATCH"):
        m.influence_analysis(
            [1.0, 2.0, 3.0],
            unit_ids=["A", "B"],
            materiality_abs_delta=0.1,
        )


def test_eg_03_m07_groups_repeated_observations_by_unit():
    m = _runtime()
    out = m.influence_analysis(
        [1.0, 1.0, -1.0, -1.0],
        unit_ids=["A", "A", "B", "B"],
        materiality_abs_delta=0.5,
    )
    assert out["unique_unit_count"] == 2
    by_unit = {x["unit_id"]: x for x in out["leave_one_unit_out"]}
    assert by_unit["A"]["remaining_mean"] == -1.0
    assert by_unit["B"]["remaining_mean"] == 1.0


def test_eg_04_m07_detects_sign_reversal_without_deletion_claim():
    m = _runtime()
    out = m.influence_analysis(
        [10.0, -1.0, -1.0],
        unit_ids=["A", "B", "C"],
        materiality_abs_delta=1.0,
    )
    assert out["sign_reversal_detected"] is True
    assert "OUTLIERS_INVALID" not in _all_keys(out)


def test_eg_05_m07_materiality_threshold_is_exact():
    m = _runtime()
    out = m.influence_analysis(
        [1.0, 1.0, -1.0, -1.0],
        unit_ids=["A", "A", "B", "B"],
        materiality_abs_delta=1.0,
    )
    assert out["max_abs_delta"] == pytest.approx(1.0)
    assert out["material_influence"] is True


def test_eg_06_m07_independent_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        unit_ids=["A", "A", "B", "C", "C"],
        materiality_abs_delta=0.3,
    )
    values = [0.5, 0.2, -0.1, 0.4, -0.2]
    assert m.influence_analysis(values, **kwargs) == r.reference_influence_analysis(values, **kwargs)


def test_eg_07_m08_excluded_requires_reason():
    m = _runtime()
    with pytest.raises(ValueError, match="EXCLUSION_REASON_REQUIRED"):
        m.attrition_analysis(
            included=[True, False],
            reasons=[None, ""],
            strata=["A", "A"],
            max_inclusion_rate_gap=0.2,
        )


def test_eg_08_m08_exact_reason_counts():
    m = _runtime()
    out = m.attrition_analysis(
        included=[True, False, False, True, False],
        reasons=[None, "GAP", "GAP", None, "END_BLOCK"],
        strata=["A", "A", "B", "B", "B"],
        max_inclusion_rate_gap=0.5,
    )
    assert out["excluded_reason_counts"] == {"END_BLOCK": 1, "GAP": 2}


def test_eg_09_m08_exact_stratum_inclusion_rates():
    m = _runtime()
    out = m.attrition_analysis(
        included=[True, False, True, True],
        reasons=[None, "GAP", None, None],
        strata=["A", "A", "B", "B"],
        max_inclusion_rate_gap=0.6,
    )
    assert out["strata"]["A"]["inclusion_rate"] == 0.5
    assert out["strata"]["B"]["inclusion_rate"] == 1.0
    assert out["max_inclusion_rate_gap"] == 0.5


def test_eg_10_m08_material_asymmetry_uses_explicit_threshold():
    m = _runtime()
    out = m.attrition_analysis(
        included=[True, False, True, True],
        reasons=[None, "GAP", None, None],
        strata=["A", "A", "B", "B"],
        max_inclusion_rate_gap=0.5,
    )
    assert out["observed_inclusion_rate_gap"] == 0.5
    assert out["material_selection_asymmetry"] is True


def test_eg_11_m08_independent_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        included=[True, False, True, False, True, True],
        reasons=[None, "GAP", None, "END_BLOCK", None, None],
        strata=["A", "A", "A", "B", "B", "B"],
        max_inclusion_rate_gap=0.2,
    )
    assert m.attrition_analysis(**kwargs) == r.reference_attrition_analysis(**kwargs)


def test_eg_12_m09_pristine_confirmatory_becomes_exposed():
    m = _runtime()
    out = m.exposure_transition("PRISTINE", "CONFIRMATORY_EVALUATION")
    assert out["before"] == "PRISTINE"
    assert out["after"] == "EXPOSED"


def test_eg_13_m09_exploratory_inspection_becomes_exposed():
    m = _runtime()
    assert m.exposure_transition("PRISTINE", "EXPLORATORY_INSPECTION")["after"] == "EXPOSED"


def test_eg_14_m09_redesign_contaminates():
    m = _runtime()
    assert m.exposure_transition(
        "EXPOSED", "HYPOTHESIS_REDESIGN_USING_EVIDENCE"
    )["after"] == "CONTAMINATED"


@pytest.mark.parametrize("state", ["EXPOSED", "CONTAMINATED"])
def test_eg_15_m09_reset_to_pristine_is_forbidden(state):
    m = _runtime()
    with pytest.raises(ValueError, match="PRISTINE_RESET_FORBIDDEN"):
        m.exposure_transition(state, "RESET_TO_PRISTINE")


def test_eg_16_m09_progression_is_monotonic_and_deterministic():
    m = _runtime()
    first = m.exposure_transition("PRISTINE", "EXPLORATORY_INSPECTION")
    second = m.exposure_transition(first["after"], "HYPOTHESIS_REDESIGN_USING_EVIDENCE")
    third = m.exposure_transition(second["after"], "CONFIRMATORY_EVALUATION")
    assert [first["after"], second["after"], third["after"]] == [
        "EXPOSED", "CONTAMINATED", "CONTAMINATED"
    ]
    assert m.exposure_transition("PRISTINE", "EXPLORATORY_INSPECTION") == first


def test_eg_17_m10_rejects_post_hoc_confirmatory_strata():
    m = _runtime()
    with pytest.raises(ValueError, match="POST_HOC_CONFIRMATORY_STRATA_FORBIDDEN"):
        m.temporal_stability(
            [1.0, 2.0],
            strata=["A", "B"],
            declared_strata=["A", "B"],
            strata_predeclared=False,
            minimum_n_per_stratum=1,
            max_mean_spread=2.0,
        )


def test_eg_18_m10_rejects_undeclared_labels():
    m = _runtime()
    with pytest.raises(ValueError, match="UNDECLARED_STRATUM"):
        m.temporal_stability(
            [1.0, 2.0],
            strata=["A", "C"],
            declared_strata=["A", "B"],
            strata_predeclared=True,
            minimum_n_per_stratum=1,
            max_mean_spread=2.0,
        )


def test_eg_19_m10_blocks_insufficient_conditional_sample():
    m = _runtime()
    out = m.temporal_stability(
        [1.0, 2.0, 3.0],
        strata=["A", "A", "B"],
        declared_strata=["A", "B"],
        strata_predeclared=True,
        minimum_n_per_stratum=2,
        max_mean_spread=10.0,
    )
    assert out["status"] == "INSUFFICIENT_CONDITIONAL_SAMPLE"
    assert out["insufficient_strata"] == ["B"]


def test_eg_20_m10_detects_mean_spread_instability():
    m = _runtime()
    out = m.temporal_stability(
        [0.0, 0.0, 2.0, 2.0],
        strata=["A", "A", "B", "B"],
        declared_strata=["A", "B"],
        strata_predeclared=True,
        minimum_n_per_stratum=2,
        max_mean_spread=1.0,
    )
    assert out["observed_mean_spread"] == 2.0
    assert out["status"] == "INSTABILITY_DETECTED"


def test_eg_21_m10_passes_only_within_explicit_tolerance():
    m = _runtime()
    out = m.temporal_stability(
        [0.0, 0.0, 1.0, 1.0],
        strata=["A", "A", "B", "B"],
        declared_strata=["A", "B"],
        strata_predeclared=True,
        minimum_n_per_stratum=2,
        max_mean_spread=1.0,
    )
    assert out["observed_mean_spread"] == 1.0
    assert out["status"] == "STABLE_WITHIN_DECLARED_TOLERANCE"


def test_eg_22_m10_independent_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        strata=["PRE", "PRE", "OOS", "OOS"],
        declared_strata=["PRE", "OOS"],
        strata_predeclared=True,
        minimum_n_per_stratum=2,
        max_mean_spread=0.2,
    )
    values = [0.1, 0.2, 0.15, 0.25]
    assert m.temporal_stability(values, **kwargs) == r.reference_temporal_stability(values, **kwargs)


def test_eg_23_m11_known_universe_requires_explicit_n_trials():
    m = _runtime()
    with pytest.raises(ValueError, match="EXPLICIT_N_TRIALS_REQUIRED"):
        m.search_provenance_gate(
            "KNOWN_SEARCH_UNIVERSE",
            registry_candidate_ids=["A", "B"],
            explicit_n_trials=None,
            provenance_complete=True,
        )


def test_eg_24_m11_registry_count_never_becomes_n_trials():
    m = _runtime()
    out = m.search_provenance_gate(
        "PARTIAL_SEARCH_UNIVERSE",
        registry_candidate_ids=["A", "B", "C", "D", "E"],
        explicit_n_trials=None,
        provenance_complete=False,
    )
    assert out["registry_record_count"] == 5
    assert out["n_trials"] is None


@pytest.mark.parametrize("status", ["PARTIAL_SEARCH_UNIVERSE", "UNKNOWN_SEARCH_UNIVERSE"])
def test_eg_25_m11_unresolved_universe_has_null_n_trials(status):
    m = _runtime()
    out = m.search_provenance_gate(
        status,
        registry_candidate_ids=["A", "B"],
        explicit_n_trials=None,
        provenance_complete=False,
    )
    assert out["n_trials"] is None


def test_eg_26_m11_no_multiplicity_distinct_from_known_one_trial():
    m = _runtime()
    none = m.search_provenance_gate(
        "NO_RELEVANT_MULTIPLICITY",
        registry_candidate_ids=[],
        explicit_n_trials=None,
        provenance_complete=True,
    )
    one = m.search_provenance_gate(
        "KNOWN_SEARCH_UNIVERSE",
        registry_candidate_ids=["A"],
        explicit_n_trials=1,
        provenance_complete=True,
    )
    assert none["n_trials"] is None
    assert one["n_trials"] == 1
    assert none["status"] != one["status"]


@pytest.mark.parametrize("n_trials,complete", [(0, True), (1.5, True), (3, False)])
def test_eg_27_m11_known_requires_positive_integer_and_complete(n_trials, complete):
    m = _runtime()
    with pytest.raises(ValueError):
        m.search_provenance_gate(
            "KNOWN_SEARCH_UNIVERSE",
            registry_candidate_ids=["A"],
            explicit_n_trials=n_trials,
            provenance_complete=complete,
        )


def test_eg_28_outputs_contain_no_forbidden_claims():
    m = _runtime()
    outputs = [
        m.influence_analysis([1.0, -1.0], unit_ids=["A", "B"], materiality_abs_delta=1.0),
        m.attrition_analysis(
            included=[True, False],
            reasons=[None, "GAP"],
            strata=["A", "A"],
            max_inclusion_rate_gap=1.0,
        ),
        m.exposure_transition("PRISTINE", "EXPLORATORY_INSPECTION"),
        m.temporal_stability(
            [0.0, 0.0],
            strata=["A", "A"],
            declared_strata=["A"],
            strata_predeclared=True,
            minimum_n_per_stratum=2,
            max_mean_spread=0.0,
        ),
        m.search_provenance_gate(
            "UNKNOWN_SEARCH_UNIVERSE",
            registry_candidate_ids=[],
            explicit_n_trials=None,
            provenance_complete=False,
        ),
    ]
    keys = set()
    for output in outputs:
        keys.update(_all_keys(output))
    assert not (keys & FORBIDDEN)


def test_eg_29_identical_inputs_are_deterministic():
    m = _runtime()
    kwargs = dict(
        included=[True, False, True],
        reasons=[None, "GAP", None],
        strata=["A", "A", "B"],
        max_inclusion_rate_gap=0.6,
    )
    assert m.attrition_analysis(**kwargs) == m.attrition_analysis(**kwargs)
