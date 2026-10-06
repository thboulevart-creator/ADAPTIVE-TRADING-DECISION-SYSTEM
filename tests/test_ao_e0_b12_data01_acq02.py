from __future__ import annotations
import copy,json
from pathlib import Path
import pytest
from tools.ao_e0_b12_data01_acq02 import *

BASE={
"provider":PROVIDER,"instrument":INSTRUMENT,"transport":TRANSPORT,"multiplier":MULTIPLIER,
"transformation_id":TRANSFORMATION_ID,"raw_forward_first_hour_start_ms":RAW_FORWARD_FIRST_HOUR_START_MS,
"forward_decision_start_ms":FORWARD_DECISION_START_MS,"warmup_is_evidence":False,
"object_hash_required":True,"interval_identity_required":True,"append_only":True,
"ledger_chain_required":True,"manifest_deterministic":True,"ap0_forward_fill":False,
"ap0_volume_used":False,"ap0_returns_calculated":False,"ap0_strategy_calculated":False,
"ap0_pnl_calculated":False,"h1_identity":H1_IDENTITY,"h1_strategy_calculated":False,
"human_forward_prices_visible":False,"human_performance_visible":False,"b12_open":False,
"pipe01_first_read_invoked":False,"owner02_real_plan_invoked":False,"owner02_real_result_invoked":False,
"final_digest_placeholder":False,"final_instance_complete_fields_only":True,
"terminal_count_from_performance":False,"optional_stop_pnl":False,"optional_stop_ci":False,
"old_e1_oos_inserted":False,"new_external_cost":False,"missing_intervals_allowed":False,
"duplicate_interval_conflict_allowed":False,"timestamps_strict":True,"ask_ge_bid":True,
"ap0_h1_bound_to_raw":True,"rolling_is_final":False,"data01_ready":False,
"strategy_qualified_claim":False,"trading_authority":False,"capital_authority":False,
"forward_start_shifted_to_acquisition_time":False,"source_semantic_drift":False
}

MUTATIONS=[
("provider","X"),("instrument","X"),("transport","X"),("multiplier","0.01"),
("source_semantic_drift",True),("raw_forward_first_hour_start_ms",RAW_FORWARD_FIRST_HOUR_START_MS+3600000),
("forward_start_shifted_to_acquisition_time",True),("warmup_is_evidence",True),
("object_hash_required",False),("interval_identity_required",False),("append_only",False),
("duplicate_interval_conflict_allowed",True),("ledger_chain_required",False),
("manifest_deterministic",False),("ap0_h1_bound_to_raw",False),("ap0_forward_fill",True),
("ap0_volume_used",True),("ap0_returns_calculated",True),("ap0_strategy_calculated",True),
("ap0_pnl_calculated",True),("h1_identity","X"),("h1_strategy_calculated",True),
("human_forward_prices_visible",True),("human_performance_visible",True),("b12_open",True),
("pipe01_first_read_invoked",True),("owner02_real_plan_invoked",True),("owner02_real_result_invoked",True),
("final_digest_placeholder",True),("final_instance_complete_fields_only",False),
("terminal_count_from_performance",True),("optional_stop_pnl",True),("optional_stop_ci",True),
("old_e1_oos_inserted",True),("new_external_cost",True),("missing_intervals_allowed",True),
("timestamps_strict",False),("ask_ge_bid",False),("rolling_is_final",True),("data01_ready",True),
("strategy_qualified_claim",True),("trading_authority",True),("capital_authority",True),
("transformation_id","OTHER"),("forward_decision_start_ms",FORWARD_DECISION_START_MS+3600000),
("capital_authority",True)
]

def raw(base=0,bad_ask=False,mult="0.001"):
    o={"timestamp":base,"multiplier":mult,"times":[1,1000,1000],"bid":100.000,"ask":100.010,
       "bids":[0,1,-1],"asks":[0,1,-1],"bidVolumes":[1,1,1],"askVolumes":[1,1,1]}
    if bad_ask:o["ask"]=99.0
    return (json.dumps(o,separators=(",",":"))+"\n").encode()

def test_01_policy_positive():
    validate_runtime_policy(BASE)

@pytest.mark.parametrize("k,v",MUTATIONS)
def test_02_policy_breakers(k,v):
    d=copy.deepcopy(BASE);d[k]=v
    with pytest.raises(ACQ02Blocked): validate_runtime_policy(d)

def test_03_named_breaker_count_contract():
    p=Path("GOVERNANCE/AO-E0-B12-DATA-01-ACQ-02-FROZEN-BREAKERS-V0.1.json")
    d=json.loads(p.read_text())
    assert d["count"]==46 and len(d["cases"])==46 and len(set(d["cases"]))==46

def test_04_valid_raw_sealed_duplicate_idempotent_conflict_blocked(tmp_path):
    a=seal_raw_object(tmp_path,interval_start_utc="2026-10-05T14:00:00Z",interval_end_utc="2026-10-05T15:00:00Z",
      raw=raw(1791208800000),acquisition_time_utc="2026-10-06T18:00:00Z",classification="WARMUP")
    assert a["status"]=="SEALED"
    b=seal_raw_object(tmp_path,interval_start_utc="2026-10-05T14:00:00Z",interval_end_utc="2026-10-05T15:00:00Z",
      raw=raw(1791208800000),acquisition_time_utc="2026-10-06T18:01:00Z",classification="WARMUP")
    assert b["status"]=="REPRODUCIBILITY_ONLY"
    changed=json.loads(raw(1791208800000).decode())
    changed["bid"]=100.001
    changed_raw=(json.dumps(changed,separators=(",",":"))+"\n").encode()
    with pytest.raises(ACQ02Blocked,match="SOURCE_OBJECT_MUTATION"):
      seal_raw_object(tmp_path,interval_start_utc="2026-10-05T14:00:00Z",interval_end_utc="2026-10-05T15:00:00Z",
       raw=changed_raw,acquisition_time_utc="2026-10-06T18:02:00Z",classification="WARMUP")

def test_05_wrong_classification_and_bad_tick_semantics(tmp_path):
    with pytest.raises(ACQ02Blocked):
      seal_raw_object(tmp_path,interval_start_utc="2026-10-06T10:00:00Z",interval_end_utc="2026-10-06T11:00:00Z",
       raw=raw(1791280800000),acquisition_time_utc="2026-10-06T18:00:00Z",classification="WARMUP")
    with pytest.raises(ACQ02Blocked):
      decode_jetta(raw(0,bad_ask=True))
    with pytest.raises(ACQ02Blocked):
      decode_jetta(raw(0,mult="0.01"))

def test_06_ledger_chain_tamper_blocks(tmp_path):
    seal_raw_object(tmp_path,interval_start_utc="2026-10-05T14:00:00Z",interval_end_utc="2026-10-05T15:00:00Z",
      raw=raw(1791208800000),acquisition_time_utc="2026-10-06T18:00:00Z",classification="WARMUP")
    p=tmp_path/"ledger"/"events.jsonl"; rows=p.read_text().splitlines(); o=json.loads(rows[0]);o["size_bytes"]+=1;p.write_text(json.dumps(o)+"\n")
    with pytest.raises(ACQ02Blocked): read_ledger(tmp_path)

def test_07_manifest_is_deterministic(tmp_path):
    seal_raw_object(tmp_path,interval_start_utc="2026-10-05T14:00:00Z",interval_end_utc="2026-10-05T15:00:00Z",
      raw=raw(1791208800000),acquisition_time_utc="2026-10-06T18:00:00Z",classification="WARMUP")
    assert rolling_raw_manifest(tmp_path)==rolling_raw_manifest(tmp_path)

def test_08_ap0_h1_structural_no_performance(tmp_path):
    # 60 synthetic minute objects in one complete hour; no strategy calculation.
    for m in range(60):
      start=1791280800000+m*60000
      s=datetime.fromtimestamp(start/1000,tz=timezone.utc).strftime("%Y-%m-%dT%H:00:00Z")
      # one ledger object per unique minute cannot share interval; simulate one hourly raw with 60 one-minute-separated ticks.
    times=[1]+[60000]*59
    o={"timestamp":1791280800000,"multiplier":"0.001","times":times,"bid":100.0,"ask":100.01,
       "bids":[0]+[0]*59,"asks":[0]+[0]*59,"bidVolumes":[1]*60,"askVolumes":[1]*60}
    rb=(json.dumps(o,separators=(",",":"))+"\n").encode()
    seal_raw_object(tmp_path,interval_start_utc="2026-10-06T10:00:00Z",interval_end_utc="2026-10-06T11:00:00Z",
      raw=rb,acquisition_time_utc="2026-10-06T18:00:00Z",classification="FORWARD_EVIDENCE")
    ap0=materialize_ap0_from_ledger(tmp_path)
    assert ap0["forward_fill"] is False and ap0["returns_calculated"] is False and ap0["strategy_calculated"] is False and ap0["pnl_calculated"] is False
    h1=materialize_h1_from_ap0(ap0,1791280800000,1791284400000)
    assert h1["identity"]==H1_IDENTITY and h1["strategy_calculated"] is False and h1["pnl_calculated"] is False

def test_09_readiness_waits_without_structural_count(tmp_path):
    o={"timestamp":1791280800000,"multiplier":"0.001","times":[1],"bid":100.0,"ask":100.01,"bids":[0],"asks":[0],"bidVolumes":[1],"askVolumes":[1]}
    seal_raw_object(tmp_path,interval_start_utc="2026-10-06T10:00:00Z",interval_end_utc="2026-10-06T11:00:00Z",
      raw=(json.dumps(o)+"\n").encode(),acquisition_time_utc="2026-10-06T18:00:00Z",classification="FORWARD_EVIDENCE")
    rm=rolling_raw_manifest(tmp_path); ap0=materialize_ap0_from_ledger(tmp_path)
    h1={"h1_forward_stream_sha256":"a"*64}
    r=rolling_readiness(raw_manifest=rm,ap0=ap0,h1=h1)
    assert r["state"]=="WAIT_TERMINAL_COUNT_AUTHORITY" and r["exact_forward_instance"]=="NOT_YET_AVAILABLE"

def test_10_performance_derived_count_blocks(tmp_path):
    with pytest.raises(ACQ02Blocked,match="TERMINAL_COUNT_FROM_PERFORMANCE"):
      rolling_readiness(raw_manifest={"raw_forward_manifest_sha256":"a","raw_forward_inventory_digest":"b"},
       ap0={"ap0_forward_manifest_sha256":"c"},h1={"h1_forward_stream_sha256":"d"},
       terminal_count_info={"derived_from_performance":True,"exact_closed_trade_count":58927,"exact_terminal_decision_time":"x"})
