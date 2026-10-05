from __future__ import annotations

import copy
from datetime import datetime, timezone

import pytest

import src.smf_ap1_m03_binding as m
import tools.smf_ap1_m03_companion as c
from tools.smf03_core_foundation_reference import reference_ecdf_quantiles

def activation():
    return m.create_m03_activation(result_exposed=False)

def plan(**overrides):
    args=dict(
        activation=activation(),
        ap1_producer_blob=m.AP1_PRODUCER_BLOB,
        data02_receipt_blob=m.DATA02_RECEIPT_BLOB,
        p121_receipt_blob=m.P121_RECEIPT_BLOB,
        smf_core_blob=m.SMF_CORE_BLOB,
        ap0_manifest_sha256=m.AP0_MANIFEST_SHA256,
        dataset_identity=m.DATASET_IDENTITY,
    )
    args.update(overrides)
    return m.build_execution_plan(**args)

def test_01_applicability_is_exact_m03_activation():
    a=activation()
    assert a["method_family_ref"]=="M03"
    assert a["activation_state"]=="ACTIVATED"
    assert m.POPULATION_SEMANTICS["iid_claim"] is False

def test_02_activation_is_deterministic():
    assert activation()==activation()

def test_03_post_result_activation_fails_closed():
    with pytest.raises(m.BindingBlocked, match="METHOD_ACTIVATION_AFTER_RESULT_EXPOSURE"):
        m.create_m03_activation(result_exposed=True)

@pytest.mark.parametrize("field,value,code",[
    ("ap1_producer_blob","bad","AP1_PRODUCER_IDENTITY_MISMATCH"),
    ("data02_receipt_blob","bad","DATA02_RECEIPT_IDENTITY_MISMATCH"),
    ("p121_receipt_blob","bad","P121_RECEIPT_IDENTITY_MISMATCH"),
    ("smf_core_blob","bad","SMF_CORE_IDENTITY_MISMATCH"),
    ("ap0_manifest_sha256","bad","AP0_MANIFEST_IDENTITY_MISMATCH"),
    ("dataset_identity","bad","DATASET_IDENTITY_MISMATCH"),
])
def test_04_exact_identity_gates(field,value,code):
    with pytest.raises(m.BindingBlocked, match=code):
        plan(**{field:value})

def test_05_plan_is_non_authoritative_and_path_free():
    p=plan()
    assert p["status"]=="M03_BINDING_PLAN_READY"
    assert p["result_minted"] is False
    assert p["g05_materialized"] is False
    assert p["authority"]["execution"] is False
    assert "ap0_root" not in p and "output" not in p

@pytest.mark.parametrize("metric,values",[
    ("tick_count",[5,1,9,4,8]),
    ("minute_range",[1.5,0.5,4.0,3.0,2.0]),
    ("spread_mean",[2.0,1.0,3.0,1.5,2.5]),
])
def test_06_exact_m03_matches_independent_reference(metric,values):
    got=m.execute_m03_observations(values,metric=metric,bucket_id="GLOBAL",activation=activation())
    ref=reference_ecdf_quantiles(values,probabilities=m.METRIC_PROBABILITIES[metric])
    assert got["n"]==ref["n"]
    assert got["quantiles"]==ref["quantiles"]
    assert got["procedure_ref"]==m.METHOD_PROCEDURE_REF

def test_07_compact_result_excludes_raw_vectors_and_ecdf():
    r=m.execute_m03_observations([3,1,2],metric="tick_count",bucket_id="GLOBAL",activation=activation())
    assert "ecdf" not in r and "sorted_values" not in r and "raw_values" not in r
    assert r["ecdf_digest"].startswith("sha256:")
    assert r["sorted_values_digest"].startswith("sha256:")

def test_08_result_digest_is_deterministic():
    a=m.execute_m03_observations([3,1,2],metric="tick_count",bucket_id="GLOBAL",activation=activation())
    b=m.execute_m03_observations([3,1,2],metric="tick_count",bucket_id="GLOBAL",activation=activation())
    assert a["result_digest"]==b["result_digest"]

def test_09_activation_tampering_fails_closed():
    a=copy.deepcopy(activation())
    a["activation_digest"]="sha256:"+"0"*64
    with pytest.raises(m.BindingBlocked,match="ACTIVATION_DIGEST_MISMATCH"):
        m.execute_m03_observations([1,2],metric="tick_count",bucket_id="GLOBAL",activation=a)

def test_10_empty_and_nonfinite_fail_closed():
    with pytest.raises(m.BindingBlocked,match="EMPTY_SAMPLE"):
        m.execute_m03_observations([],metric="tick_count",bucket_id="GLOBAL",activation=activation())
    with pytest.raises(m.BindingBlocked,match="NONFINITE_OBSERVATION"):
        m.execute_m03_observations([1,float("inf")],metric="tick_count",bucket_id="GLOBAL",activation=activation())

def test_11_companion_record_semantics_match_ap1_metrics():
    obs=c.record_to_observations({
        "minute_start_ms_utc": 1704204000000,
        "tick_count": 10,
        "mid_high": 102.5,
        "mid_low": 100.0,
        "spread_mean": 1.25,
    })
    assert obs["tick_count"]==10.0
    assert obs["minute_range"]==2.5
    assert obs["spread_mean"]==1.25

def test_12_companion_buckets_cover_exact_dimensions_standard_time():
    ms=int(datetime(2024,1,2,14,0,tzinfo=timezone.utc).timestamp()*1000)
    keys=set(c.bucket_keys_for_minute(ms))
    assert {"GLOBAL","UTC_HOUR:14","NEW_YORK_HOUR:09","NEW_YORK_WEEKDAY:1","NEW_YORK_WEEKDAY_HOUR:1:09","UTC_YEAR:2024"} <= keys

def test_13_companion_buckets_respect_new_york_dst():
    ms=int(datetime(2024,7,2,14,0,tzinfo=timezone.utc).timestamp()*1000)
    keys=set(c.bucket_keys_for_minute(ms))
    assert "NEW_YORK_HOUR:10" in keys

def test_14_companion_builds_exact_method_evidence_synthetically():
    rows=[
        {"minute_start_ms_utc":int(datetime(2024,1,2,14,0,tzinfo=timezone.utc).timestamp()*1000),"tick_count":10,"mid_high":102.0,"mid_low":100.0,"spread_mean":1.0},
        {"minute_start_ms_utc":int(datetime(2024,1,2,14,1,tzinfo=timezone.utc).timestamp()*1000),"tick_count":20,"mid_high":103.0,"mid_low":100.0,"spread_mean":2.0},
    ]
    out=c.build_companion_evidence(rows,activation=activation())
    assert out["real_workspace_materialized"] is False
    assert out["bucket_evidence"]["GLOBAL"]["tick_count"]["quantiles"]["0.5"]==15.0
    assert out["bucket_evidence"]["GLOBAL"]["minute_range"]["quantiles"]["0.5"]==2.5
    assert out["authority"]["scientific"] is False

def test_15_companion_identity_is_not_ap1_identity():
    assert m.COMPANION_ID != "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"

def test_16_bucket_identity_required():
    with pytest.raises(m.BindingBlocked,match="BUCKET_ID_REQUIRED"):
        m.execute_m03_observations([1,2],metric="tick_count",bucket_id="",activation=activation())

def test_17_unknown_metric_fails_closed():
    with pytest.raises(m.BindingBlocked,match="UNSUPPORTED_M03_METRIC"):
        m.execute_m03_observations([1,2],metric="unknown",bucket_id="GLOBAL",activation=activation())

def test_18_no_authority_is_minted_by_method_evidence():
    r=m.execute_m03_observations([1,2],metric="spread_mean",bucket_id="GLOBAL",activation=activation())
    assert r["authority"]=={"scientific":False,"operational":False,"trading":False,"capital":False}
