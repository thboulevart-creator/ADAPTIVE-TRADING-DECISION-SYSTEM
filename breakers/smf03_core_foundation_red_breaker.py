from __future__ import annotations

import copy
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/SMF-03-CORE-FOUNDATION-CONTRACT-V0.1.json"
RUNTIME_PATH = Path(os.environ.get(
    "SMF03_CORE_RUNTIME_PATH",
    str(ROOT / "tools/smf03_core_foundation.py"),
))
REFERENCE_PATH = ROOT / "tools/smf03_core_foundation_reference.py"

RUNTIME_CONTRACT = "ATDS_SMF03_CORE_FOUNDATION_V0_1"
REFERENCE_CONTRACT = "ATDS_SMF03_CORE_FOUNDATION_REFERENCE_V0_1"
FORBIDDEN = {
    "STRATEGY_QUALIFIED",
    "EDGE_GENERALIZABLE",
    "LIVE_PROFITABILITY",
    "DEPLOYMENT_AUTHORIZED",
    "UNOBSERVED_TAIL_IMPOSSIBLE",
}

CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert CONTRACT["schema"] == "ATDS_SMF03_CORE_FOUNDATION_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT["test_cases"]] == [f"CF-{i:02d}" for i in range(1, 19)]


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
    m = _load(RUNTIME_PATH, "smf03_core_foundation_under_test")
    for name in (
        "CONTRACT",
        "ALLOWED_METHOD_FAMILIES",
        "ACTIVATION_STATES",
        "create_activation_record",
        "net_economic_effect",
        "ecdf_quantiles",
    ):
        assert hasattr(m, name), f"RUNTIME_SURFACE_MISSING:{name}"
    assert m.CONTRACT == RUNTIME_CONTRACT
    return m


def _reference():
    m = _load(REFERENCE_PATH, "smf03_core_foundation_reference")
    assert m.CONTRACT == REFERENCE_CONTRACT
    return m


def _activation_kwargs():
    return {
        "claim_definition_ref": "sha256:claim-001",
        "failure_mode_ref": "FM-01",
        "method_family_ref": "M02",
        "validity_scope_ref": "sha256:scope-001",
        "assumption_set_ref": "sha256:assumptions-001",
        "activation_reason": "Net economic effect claim requires M02",
        "activation_rule": "ECONOMIC_VIABILITY_CLAIM",
        "parameter_selection_policy": {"minimum_effect": 0.05},
        "dependency_refs": ["sha256:m01-001"],
        "activation_state": "ACTIVATED",
    }


def _all_keys(value):
    keys = set()
    if isinstance(value, dict):
        keys.update(value.keys())
        for item in value.values():
            keys.update(_all_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(_all_keys(item))
    return {str(x) for x in keys}


def test_cf_01_runtime_contract_and_surface_are_exact():
    m = _runtime()
    assert set(m.ACTIVATION_STATES) == {"ACTIVATED", "NOT_APPLICABLE", "BLOCKED"}
    assert set(CONTRACT["allowed_method_families"]) == set(m.ALLOWED_METHOD_FAMILIES)


def test_cf_02_activation_rejects_post_result_selection():
    m = _runtime()
    with pytest.raises(ValueError, match="METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE"):
        m.create_activation_record(**_activation_kwargs(), result_exposed=True)


def test_cf_03_activation_rejects_empty_material_identity():
    m = _runtime()
    kwargs = _activation_kwargs()
    kwargs["claim_definition_ref"] = " "
    with pytest.raises(ValueError, match="EMPTY_MATERIAL_IDENTITY"):
        m.create_activation_record(**kwargs)


def test_cf_04_activation_rejects_non_adopted_method_family():
    m = _runtime()
    kwargs = _activation_kwargs()
    kwargs["method_family_ref"] = "M99"
    with pytest.raises(ValueError, match="METHOD_FAMILY_NOT_ADOPTED"):
        m.create_activation_record(**kwargs)


def test_cf_05_activation_states_remain_distinct():
    m = _runtime()
    records = []
    for state in ("ACTIVATED", "NOT_APPLICABLE", "BLOCKED"):
        kwargs = _activation_kwargs()
        kwargs["activation_state"] = state
        records.append(m.create_activation_record(**kwargs))
    assert [x["activation_state"] for x in records] == [
        "ACTIVATED", "NOT_APPLICABLE", "BLOCKED"
    ]


def test_cf_06_activation_digest_is_deterministic():
    m = _runtime()
    kwargs = _activation_kwargs()
    a = m.create_activation_record(**kwargs)
    b = m.create_activation_record(**copy.deepcopy(kwargs))
    assert a == b
    assert a["activation_digest"].startswith("sha256:")
    assert len(a["activation_digest"]) == 71


def test_cf_07_m02_scalar_cost_before_average():
    m = _runtime()
    out = m.net_economic_effect([0.20, -0.10, 0.30], costs=0.05, minimum_effect=0.05)
    assert out["gross_mean"] == pytest.approx(0.13333333333333333)
    assert out["cost_mean"] == pytest.approx(0.05)
    assert out["net_mean"] == pytest.approx(0.08333333333333333)


def test_cf_08_m02_per_observation_costs():
    m = _runtime()
    out = m.net_economic_effect([0.2, 0.0, -0.1], costs=[0.01, 0.02, 0.03], minimum_effect=0.0)
    assert out["net_outcomes"] == pytest.approx([0.19, -0.02, -0.13])
    assert out["net_mean"] == pytest.approx(0.013333333333333334)


def test_cf_09_m02_threshold_relation_is_exact():
    m = _runtime()
    equal = m.net_economic_effect([0.1, 0.1], costs=0.0, minimum_effect=0.1)
    below = m.net_economic_effect([0.1, 0.09], costs=0.0, minimum_effect=0.1)
    assert equal["threshold_relation"] == "ABOVE_OR_EQUAL"
    assert below["threshold_relation"] == "BELOW"


@pytest.mark.parametrize("values,costs", [
    ([1.0, math.nan], 0.0),
    ([1.0, math.inf], 0.0),
    ([1.0, 2.0], math.nan),
    ([1.0, 2.0], [0.0, math.inf]),
])
def test_cf_10_m02_rejects_nonfinite(values, costs):
    m = _runtime()
    with pytest.raises(ValueError, match="NONFINITE"):
        m.net_economic_effect(values, costs=costs, minimum_effect=0.0)


def test_cf_11_m03_ecdf_exact_ranks():
    m = _runtime()
    out = m.ecdf_quantiles([3.0, 1.0, 2.0], probabilities=[0.5])
    assert out["sorted_values"] == [1.0, 2.0, 3.0]
    assert out["ecdf"] == [
        {"x": 1.0, "p": pytest.approx(1 / 3)},
        {"x": 2.0, "p": pytest.approx(2 / 3)},
        {"x": 3.0, "p": pytest.approx(1.0)},
    ]


def test_cf_12_m03_linear_quantile_definition():
    m = _runtime()
    out = m.ecdf_quantiles([0.0, 10.0, 20.0, 30.0], probabilities=[0.25, 0.5, 0.75])
    assert out["quantiles"] == pytest.approx({"0.25": 7.5, "0.5": 15.0, "0.75": 22.5})


def test_cf_13_m03_endpoints_are_exact():
    m = _runtime()
    out = m.ecdf_quantiles([-2.0, 5.0, 9.0], probabilities=[0.0, 1.0])
    assert out["quantiles"] == {"0.0": -2.0, "1.0": 9.0}


def test_cf_14_m03_blocks_empty_sample():
    m = _runtime()
    with pytest.raises(ValueError, match="EMPTY_SAMPLE"):
        m.ecdf_quantiles([], probabilities=[0.5])


def test_cf_15_m02_independent_reference_parity():
    m = _runtime()
    r = _reference()
    values = [0.11, -0.04, 0.08, 0.03, -0.01]
    costs = [0.01, 0.02, 0.01, 0.01, 0.02]
    assert m.net_economic_effect(values, costs=costs, minimum_effect=0.025) ==         r.reference_net_economic_effect(values, costs=costs, minimum_effect=0.025)


def test_cf_16_m03_independent_reference_parity():
    m = _runtime()
    r = _reference()
    values = [9.0, 1.0, 4.0, 4.0, -2.0, 7.0]
    probs = [0.0, 0.1, 0.5, 0.9, 1.0]
    assert m.ecdf_quantiles(values, probabilities=probs) ==         r.reference_ecdf_quantiles(values, probabilities=probs)


def test_cf_17_outputs_contain_no_forbidden_claims():
    m = _runtime()
    a = m.create_activation_record(**_activation_kwargs())
    e = m.net_economic_effect([0.2, -0.1], costs=0.01, minimum_effect=0.0)
    d = m.ecdf_quantiles([0.2, -0.1], probabilities=[0.05, 0.5, 0.95])
    keys = {x.upper() for x in (_all_keys(a) | _all_keys(e) | _all_keys(d))}
    assert not (keys & FORBIDDEN)


def test_cf_18_identical_inputs_are_deterministic():
    m = _runtime()
    args = ([0.12, -0.03, 0.07, -0.01],)
    kwargs = {"costs": [0.01, 0.02, 0.01, 0.01], "minimum_effect": 0.02}
    assert m.net_economic_effect(*args, **kwargs) == m.net_economic_effect(*args, **kwargs)
    assert m.ecdf_quantiles(args[0], probabilities=[0.1, 0.5, 0.9]) ==         m.ecdf_quantiles(args[0], probabilities=[0.1, 0.5, 0.9])
