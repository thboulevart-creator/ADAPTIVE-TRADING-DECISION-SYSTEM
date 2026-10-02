from __future__ import annotations

import importlib.util
import json
import math
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SMF-03-DEPENDENCE-INFERENCE-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(os.environ.get(
    "SMF03_DI_RUNTIME_PATH",
    str(ROOT / "tools/smf03_dependence_inference.py"),
))
REFERENCE_PATH = ROOT / "tools/smf03_dependence_inference_reference.py"

RUNTIME_CONTRACT = "ATDS_SMF03_DEPENDENCE_INFERENCE_V0_1"
REFERENCE_CONTRACT = "ATDS_SMF03_DEPENDENCE_INFERENCE_REFERENCE_V0_1"
FORBIDDEN = {
    "INDEPENDENCE_PROVEN",
    "MODEL_VALID",
    "STRATEGY_QUALIFIED",
    "EDGE_GENERALIZABLE",
    "LIVE_PROFITABILITY",
}

CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert CONTRACT["schema"] == "ATDS_SMF03_DEPENDENCE_INFERENCE_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT["test_cases"]] == [f"DI-{i:02d}" for i in range(1, 25)]


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
    m = _load(RUNTIME_PATH, "smf03_dependence_inference_under_test")
    for name in (
        "CONTRACT",
        "dependence_diagnostics",
        "bootstrap_mean_ci",
        "required_n_for_mean_precision",
        "required_n_for_mean_power",
    ):
        assert hasattr(m, name), f"RUNTIME_SURFACE_MISSING:{name}"
    assert m.CONTRACT == RUNTIME_CONTRACT
    return m


def _reference():
    m = _load(REFERENCE_PATH, "smf03_dependence_inference_reference")
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


def test_di_01_runtime_contract_and_exact_surface():
    m = _runtime()
    assert m.CONTRACT == RUNTIME_CONTRACT


def test_di_02_m04_requires_explicit_nonempty_lags():
    m = _runtime()
    with pytest.raises(ValueError, match="LAGS_REQUIRED"):
        m.dependence_diagnostics(
            [1.0, 2.0, 3.0],
            lags=[],
            estimator="BIASED",
            abs_threshold=0.2,
            structural_flags=[],
        )


def test_di_03_m04_biased_acf_frozen_case():
    m = _runtime()
    out = m.dependence_diagnostics(
        [1.0, 2.0, 3.0, 4.0],
        lags=[1],
        estimator="BIASED",
        abs_threshold=0.9,
        structural_flags=[],
    )
    assert out["acf"]["1"] == pytest.approx(0.25)


def test_di_04_m04_adjusted_acf_frozen_case():
    m = _runtime()
    out = m.dependence_diagnostics(
        [1.0, 2.0, 3.0, 4.0],
        lags=[1],
        estimator="ADJUSTED",
        abs_threshold=0.9,
        structural_flags=[],
    )
    assert out["acf"]["1"] == pytest.approx(1.0 / 3.0)


def test_di_05_structural_dependence_cannot_be_erased():
    m = _runtime()
    out = m.dependence_diagnostics(
        [1.0, -1.0, 1.0, -1.0],
        lags=[1],
        estimator="BIASED",
        abs_threshold=2.0,
        structural_flags=["OVERLAPPING_OUTCOMES"],
    )
    assert out["status"] == "STRUCTURALLY_PRESENT"


def test_di_06_low_acf_never_claims_independence():
    m = _runtime()
    out = m.dependence_diagnostics(
        [1.0, -1.0, -1.0, 1.0],
        lags=[1],
        estimator="BIASED",
        abs_threshold=0.9,
        structural_flags=[],
    )
    assert out["status"] == "NO_MATERIAL_DEPENDENCE_FOUND_WITHIN_TESTED_LAGS"
    assert "INDEPENDENCE_PROVEN" not in _all_keys(out)


@pytest.mark.parametrize("values,threshold", [
    ([1.0, math.nan, 2.0], 0.2),
    ([1.0, 2.0, 3.0], math.nan),
    ([1.0, 2.0, 3.0], 0.0),
])
def test_di_07_m04_rejects_invalid_inputs(values, threshold):
    m = _runtime()
    with pytest.raises(ValueError):
        m.dependence_diagnostics(
            values,
            lags=[1],
            estimator="BIASED",
            abs_threshold=threshold,
            structural_flags=[],
        )


def test_di_08_m04_independent_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        lags=[1, 2],
        estimator="ADJUSTED",
        abs_threshold=0.35,
        structural_flags=[],
    )
    values = [0.1, -0.2, 0.4, 0.3, -0.1, 0.2]
    actual = m.dependence_diagnostics(values, **kwargs)
    expected = r.reference_dependence_diagnostics(values, **kwargs)
    actual_acf = actual.pop("acf")
    expected_acf = expected.pop("acf")
    assert actual == expected
    assert actual_acf == pytest.approx(expected_acf, rel=1e-12, abs=1e-15)


def test_di_09_iid_bootstrap_requires_justification():
    m = _runtime()
    with pytest.raises(ValueError, match="IID_NOT_JUSTIFIED"):
        m.bootstrap_mean_ci(
            [1.0, 2.0, 3.0],
            scheme="IID",
            interval_method="PERCENTILE",
            confidence_level=0.95,
            replications=100,
            seed=7,
            stationarity_status="STATIONARY",
            iid_justified=False,
        )


def test_di_10_unresolved_nonstationarity_blocks_resampling():
    m = _runtime()
    with pytest.raises(ValueError, match="UNRESOLVED_NONSTATIONARITY"):
        m.bootstrap_mean_ci(
            [1.0, 2.0, 3.0, 4.0],
            scheme="MOVING_BLOCK",
            interval_method="PERCENTILE",
            confidence_level=0.95,
            replications=100,
            seed=7,
            stationarity_status="UNRESOLVED_NONSTATIONARY",
            block_length=2,
        )


def test_di_11_moving_block_requires_valid_block_length():
    m = _runtime()
    with pytest.raises(ValueError, match="BLOCK_LENGTH_REQUIRED"):
        m.bootstrap_mean_ci(
            [1.0, 2.0, 3.0, 4.0],
            scheme="MOVING_BLOCK",
            interval_method="PERCENTILE",
            confidence_level=0.95,
            replications=100,
            seed=7,
            stationarity_status="STATIONARY",
        )


def test_di_12_interval_method_must_be_explicit_and_supported():
    m = _runtime()
    with pytest.raises(ValueError, match="INTERVAL_METHOD_UNSUPPORTED"):
        m.bootstrap_mean_ci(
            [1.0, 2.0, 3.0],
            scheme="IID",
            interval_method="AUTO",
            confidence_level=0.95,
            replications=100,
            seed=7,
            stationarity_status="STATIONARY",
            iid_justified=True,
        )


def test_di_13_bootstrap_seed_is_exactly_deterministic():
    m = _runtime()
    kwargs = dict(
        scheme="IID",
        interval_method="PERCENTILE",
        confidence_level=0.9,
        replications=121,
        seed=17,
        stationarity_status="STATIONARY",
        iid_justified=True,
    )
    assert m.bootstrap_mean_ci([0.0, 1.0, 4.0, 9.0], **kwargs) == m.bootstrap_mean_ci([0.0, 1.0, 4.0, 9.0], **kwargs)


@pytest.mark.parametrize("scheme,extra", [
    ("IID", {"iid_justified": True}),
    ("MOVING_BLOCK", {"block_length": 2}),
])
def test_di_14_constant_sample_ci_collapses(scheme, extra):
    m = _runtime()
    out = m.bootstrap_mean_ci(
        [5.0, 5.0, 5.0, 5.0],
        scheme=scheme,
        interval_method="PERCENTILE",
        confidence_level=0.95,
        replications=75,
        seed=3,
        stationarity_status="STATIONARY",
        **extra,
    )
    assert out["point_estimate"] == 5.0
    assert out["lower"] == 5.0
    assert out["upper"] == 5.0


def test_di_15_percentile_and_basic_are_distinct_selectable_contracts():
    m = _runtime()
    common = dict(
        scheme="IID",
        confidence_level=0.8,
        replications=301,
        seed=11,
        stationarity_status="STATIONARY",
        iid_justified=True,
    )
    values = [0.0, 1.0, 1.0, 10.0, 30.0]
    a = m.bootstrap_mean_ci(values, interval_method="PERCENTILE", **common)
    b = m.bootstrap_mean_ci(values, interval_method="BASIC", **common)
    assert (a["lower"], a["upper"]) != (b["lower"], b["upper"])


def test_di_16_m05_independent_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        scheme="MOVING_BLOCK",
        interval_method="BASIC",
        confidence_level=0.8,
        replications=101,
        seed=19,
        stationarity_status="STATIONARY",
        block_length=2,
    )
    values = [0.0, 1.0, 2.0, 5.0, -1.0]
    assert m.bootstrap_mean_ci(values, **kwargs) == r.reference_bootstrap_mean_ci(values, **kwargs)


def test_di_17_m06_precision_requires_supported_model():
    m = _runtime()
    with pytest.raises(ValueError, match="PRECISION_MODEL_UNSUPPORTED"):
        m.required_n_for_mean_precision(
            model_ref="AUTO",
            stddev=1.0,
            half_width=0.1,
            confidence_level=0.95,
        )


def test_di_18_m06_precision_reference_parity():
    m = _runtime()
    r = _reference()
    kwargs = dict(
        model_ref="NORMAL_MEAN_KNOWN_SIGMA",
        stddev=1.7,
        half_width=0.2,
        confidence_level=0.95,
    )
    assert m.required_n_for_mean_precision(**kwargs) == r.reference_required_n_for_mean_precision(**kwargs)


def test_di_19_m06_power_requires_predeclared_effect():
    m = _runtime()
    with pytest.raises(ValueError, match="POST_HOC_POWER_FORBIDDEN"):
        m.required_n_for_mean_power(
            model_ref="NORMAL_MEAN_KNOWN_SIGMA",
            effect_size=0.3,
            stddev=1.0,
            alpha=0.05,
            target_power=0.8,
            alternative="GREATER",
            effect_source="OBSERVED",
            max_n=10000,
        )


def test_di_20_m06_unsupported_model_blocks():
    m = _runtime()
    with pytest.raises(ValueError, match="POWER_MODEL_UNSUPPORTED"):
        m.required_n_for_mean_power(
            model_ref="AUTO",
            effect_size=0.3,
            stddev=1.0,
            alpha=0.05,
            target_power=0.8,
            alternative="GREATER",
            effect_source="PREDECLARED",
            max_n=10000,
        )


def test_di_21_m06_power_is_deterministic_and_bounded():
    m = _runtime()
    out = m.required_n_for_mean_power(
        model_ref="NORMAL_MEAN_KNOWN_SIGMA",
        effect_size=0.4,
        stddev=1.0,
        alpha=0.05,
        target_power=0.8,
        alternative="GREATER",
        effect_source="PREDECLARED",
        max_n=1000,
    )
    assert isinstance(out["required_n"], int)
    assert 1 <= out["required_n"] <= 1000
    assert out["achieved_power"] >= 0.8


def test_di_22_m06_unreachable_target_blocks():
    m = _runtime()
    with pytest.raises(ValueError, match="TARGET_POWER_UNREACHABLE_WITHIN_MAX_N"):
        m.required_n_for_mean_power(
            model_ref="NORMAL_MEAN_KNOWN_SIGMA",
            effect_size=0.001,
            stddev=10.0,
            alpha=0.05,
            target_power=0.999,
            alternative="TWO_SIDED",
            effect_source="PREDECLARED",
            max_n=3,
        )


def test_di_23_outputs_contain_no_forbidden_claims():
    m = _runtime()
    outputs = [
        m.dependence_diagnostics(
            [1.0, 2.0, 3.0, 4.0],
            lags=[1],
            estimator="BIASED",
            abs_threshold=0.9,
            structural_flags=[],
        ),
        m.bootstrap_mean_ci(
            [1.0, 2.0, 3.0],
            scheme="IID",
            interval_method="PERCENTILE",
            confidence_level=0.8,
            replications=51,
            seed=2,
            stationarity_status="STATIONARY",
            iid_justified=True,
        ),
        m.required_n_for_mean_precision(
            model_ref="NORMAL_MEAN_KNOWN_SIGMA",
            stddev=1.0,
            half_width=0.2,
            confidence_level=0.95,
        ),
    ]
    keys = set()
    for output in outputs:
        keys.update(_all_keys(output))
    assert not (keys & FORBIDDEN)


def test_di_24_identical_inputs_are_deterministic():
    m = _runtime()
    kwargs = dict(
        scheme="MOVING_BLOCK",
        interval_method="PERCENTILE",
        confidence_level=0.9,
        replications=99,
        seed=123,
        stationarity_status="STATIONARY",
        block_length=2,
    )
    values = [0.0, 1.0, 2.0, 3.0]
    assert m.bootstrap_mean_ci(values, **kwargs) == m.bootstrap_mean_ci(values, **kwargs)