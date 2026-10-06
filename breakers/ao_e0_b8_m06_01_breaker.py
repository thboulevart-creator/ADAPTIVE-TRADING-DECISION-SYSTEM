from pathlib import Path
import json, math, statistics, pytest

R=Path(__file__).resolve().parents[1]
C=json.loads((R/"GOVERNANCE"/"AO-E0-B8-M06-01-EXPOSED-E1-PLANNING-DISPERSION-CONTRACT-V0.1.json").read_text())

def test_exact_source_identities():
    s=C["source"]
    assert s["zip_sha256"]=="a6588ef94d6cf15447ee8f7d2be0b7d3642ae857f2d64fcf86c77070ced0ca84"
    assert s["result_canonical_digest"]=="56eaf2626629bff2ff7b6dcd13e2ca178edddf06aade81f9480c4e3d142cf738"
    assert s["records_digest"]=="f890dd32f3e14b20430cb5898a05946a5d71231a9103b755fa0eb683f8834fc4"

def test_counts_and_aggregates():
    v=C["verification"]
    assert v["closed_trade_count"]==650
    assert v["pre_oos_closed_trade_count"]==535
    assert v["exposed_oos_closed_trade_count"]==114
    assert v["cross_boundary_closed_trade_count"]==1
    assert math.isclose(v["full_sample_aggregate_realized_unit_pnl"],-3653.772000000031,abs_tol=1e-9)
    assert math.isclose(v["exposed_oos_aggregate_realized_unit_pnl"],2856.667999999994,abs_tol=1e-9)

def test_sample_not_population_stddev():
    d=C["dispersion"]
    assert d["estimator"]=="SAMPLE_STANDARD_DEVIATION"
    assert d["denominator"]=="n-1"
    assert not math.isclose(d["full_sample_sample_stddev"],d["full_sample_population_stddev"],abs_tol=1e-12)
    assert math.isclose(d["selected_planning_stddev_candidate"],336.4106561689863,abs_tol=1e-12)

def test_no_oos_only_sigma_substitution():
    d=C["dispersion"]
    assert d["selection_rule"]=="FULL_SAMPLE_ONLY_PREDECLARED_TO_AVOID_OOS_ONLY_SELECTION"
    assert d["selected_planning_stddev_candidate"]==d["full_sample_sample_stddev"]
    assert d["selected_planning_stddev_candidate"]!=d["exposed_oos_sample_stddev"]

def test_epistemic_firewalls():
    assert all(C["separations"].values())
    assert C["dispersion"]["epistemic_class"]=="EXPOSED_E1_PLANNING_PROXY_ONLY"

def test_no_authority():
    assert all(v is False for v in C["authority"].values())
    assert C["status"]=="QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION"

def test_mutated_row_changes_sample_stddev():
    xs=[-1.0,0.0,1.0]
    a=statistics.stdev(xs)
    xs[0]=-2.0
    b=statistics.stdev(xs)
    assert a!=b

def test_population_substitution_rejected():
    d=C["dispersion"]
    with pytest.raises(AssertionError):
        assert d["selected_planning_stddev_candidate"]==d["full_sample_population_stddev"]
