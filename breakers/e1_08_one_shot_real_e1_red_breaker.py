from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "GOVERNANCE/E1-08A-ONE-SHOT-REAL-E1-CONTRACT-V0.1.json"
TARGET_PATH = Path(os.environ.get("E1_08_RUNTIME_PATH", str(ROOT / "tools/e1_08_one_shot_real_e1.py")))

RUNTIME_CONTRACT = "ATDS_E1_08A_ONE_SHOT_REAL_E1_V0_1"
EXPECTED_PROTECTED = {
    "e1_01_e1_02_freeze_package_blob": "6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e",
    "e1_03_runtime_blob": "38d481755e00ce3c2ed9c66c4db710500ca0911a",
    "e1_04_runtime_blob": "15e72b8743e7726fc8b8bedd933cf7defe56413b",
    "e1_05_runtime_blob": "baad3bd7c2e810451737c89bf8f9bcabc17c5ba6",
    "e1_06_reference_blob": "25b01e6d31709f02f9c095262bfe78366e83003b",
    "e1_06_qualifier_blob": "0793adc08416563125f57a55c0d272d24bb4b3df",
    "e1_07_runtime_blob": "88ca1f1ae89d1a2cfac1ae35becb3ea6209755f5",
    "phase_21_decision_blob": "eecbfd4a7c214a2d09210f5b0490c06673619c24",
}
OOS = 1_748_131_200_000

CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
assert CONTRACT["schema"] == "ATDS_E1_08A_ONE_SHOT_REAL_E1_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT["test_cases"]] == [f"Q8-{i:02d}" for i in range(1, 21)]
assert len(CONTRACT["test_cases"]) == 20

def _target():
    if not TARGET_PATH.is_file():
        pytest.fail("E1_08_TARGET_ABSENT_EXPECTED_RED", pytrace=False)
    spec = importlib.util.spec_from_file_location("e1_08_under_test", TARGET_PATH)
    if spec is None or spec.loader is None:
        pytest.fail("E1_08_TARGET_UNLOADABLE_EXPECTED_RED", pytrace=False)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _deps():
    def load(name, path):
        spec=importlib.util.spec_from_file_location(name, ROOT / path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return (
        load("e103","tools/e1_03_h1_dataset_identity.py"),
        load("e104","tools/e1_04_execution_cost_model.py"),
        load("e105","tools/e1_05_minimal_momentum_runner.py"),
        load("e107","tools/e1_07_preflight_trace.py"),
    )

def _rows():
    H=3_600_000
    start=1_700_000_000_000
    rows=[]
    for i in range(23):
        close=100.0
        if i==20: close=110.0
        elif i==21: close=90.0
        elif i==22: close=100.0
        rows.append({
            "h1_start_ms_utc":start+i*H,
            "source_segment_id":1,
            "continuity_block_id":1,
            "continuity_ordinal":i,
            "mid_close":close,
        })
    return rows

def _raw_rows(rows):
    H=3_600_000
    return [
        {"timestamp":rows[20]["h1_start_ms_utc"]+H,"bid_price":100.0,"ask_price":101.0},
        {"timestamp":rows[21]["h1_start_ms_utc"]+H,"bid_price":104.0,"ask_price":105.0},
        {"timestamp":rows[22]["h1_start_ms_utc"]+H,"bid_price":99.0,"ask_price":100.0},
    ]

def _exposure(m, prior="NONE_DECLARED"):
    return m.build_exposure_declaration(
        declaration_timestamp_utc="2026-09-28T20:00:00Z",
        human_authority_reference="SYNTHETIC_FIXTURE_ONLY",
        prior_oos_performance_exposure=prior,
    )

def _authority(m):
    base={
        "schema":"E1_ONE_SHOT_RUN_AUTHORITY_V0",
        "experiment_id":m.EXPERIMENT_ID,
        "run_id":"SYNTHETIC-E1-08A-FIXTURE",
        "repository":m.REPOSITORY,
        "branch":m.BRANCH,
        "authorized_base_head":"1"*40,
        "authorized_base_tree":"2"*40,
        "executor_blob":"3"*40,
        "protected_bindings":dict(m.PROTECTED_BLOBS),
        "source_manifest_sha256":m.SOURCE_MANIFEST_SHA256,
        "h1_jsonl_sha256":m.H1_JSONL_SHA256,
        "oos_start":m.OOS_START,
        "oos_end":m.OOS_END,
        "max_runs":1,
        "real_e1_run_authorized":True,
        "authorized_at_utc":"2026-09-28T20:01:00Z",
        "human_decision_reference":"SYNTHETIC_FIXTURE_ONLY",
    }
    base["canonical_digest"]=m.canonical_sha256(base)
    return base

def test_q8_01_runtime_contract_and_surface():
    m=_target()
    assert m.CONTRACT==RUNTIME_CONTRACT
    required={
        "canonical_sha256","adapt_tick_rows","verify_file_bytes","verify_source_manifest",
        "load_h1_jsonl","build_exposure_declaration","verify_exposure_declaration",
        "verify_one_shot_authority","consume_authorization_once","derive_trade_ledger",
        "compute_metrics","build_result_payload","run_synthetic_qualification"
    }
    assert required.issubset(set(dir(m)))

def test_q8_02_protected_dependency_identities():
    m=_target()
    for k,v in EXPECTED_PROTECTED.items():
        assert m.PROTECTED_BLOBS[k]==v

def test_q8_03_gap_gt_60000_forbidden():
    m=_target()
    rows=[
        {"timestamp":1_000_000,"bid_price":10.0,"ask_price":11.0},
        {"timestamp":1_060_001,"bid_price":12.0,"ask_price":13.0},
    ]
    out=list(m.adapt_tick_rows(rows))
    assert out[1]["continuity_status"]=="FORBIDDEN_BOUNDARY"

def test_q8_04_gap_eq_60000_ok():
    m=_target()
    rows=[
        {"timestamp":1_000_000,"bid_price":10.0,"ask_price":11.0},
        {"timestamp":1_060_000,"bid_price":12.0,"ask_price":13.0},
    ]
    out=list(m.adapt_tick_rows(rows))
    assert out[1]["continuity_status"]=="OK"

def test_q8_05_adapter_preserves_order_mapping():
    m=_target()
    rows=[
        {"timestamp":5,"bid_price":1.0,"ask_price":2.0},
        {"timestamp":6,"bid_price":3.0,"ask_price":4.0},
    ]
    out=list(m.adapt_tick_rows(rows))
    assert [x["timestamp_ms"] for x in out]==[5,6]
    assert [(x["bid"],x["ask"]) for x in out]==[(1.0,2.0),(3.0,4.0)]

def test_q8_06_non_increasing_fails_no_repair():
    m=_target()
    rows=[
        {"timestamp":10,"bid_price":1.0,"ask_price":2.0},
        {"timestamp":9,"bid_price":3.0,"ask_price":4.0},
    ]
    with pytest.raises(m.E108Error, match="NON_INCREASING_SOURCE_TIMESTAMP"):
        list(m.adapt_tick_rows(rows))

def test_q8_07_file_hash_mismatch_detected(tmp_path):
    m=_target()
    p=tmp_path/"x.bin"
    p.write_bytes(b"abc")
    good=hashlib.sha256(b"abc").hexdigest()
    assert m.verify_file_bytes(p,good)["status"]=="PASS"
    assert m.verify_file_bytes(p,"0"*64)["status"]=="BLOCKED"

def test_q8_08_manifest_inventory_binding(tmp_path):
    m=_target()
    p=tmp_path/"manifest.json"
    files=[
        {"relative_path":"a.parquet","size_bytes":3,"mtime_ns":1,"sha256":"a"*64},
        {"relative_path":"b.parquet","size_bytes":4,"mtime_ns":2,"sha256":"b"*64},
    ]
    payload={
        "schema":"ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1",
        "status":"MANIFEST_COMPLETE",
        "inventory":{"parquet_files":2,"files":files}
    }
    raw=(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n").encode()
    p.write_bytes(raw)
    inv=m.canonical_inventory_digest(files)
    ok=m.verify_source_manifest(p,hashlib.sha256(raw).hexdigest(),inv,2)
    assert ok["status"]=="PASS"
    payload["inventory"]["files"][0]["sha256"]="c"*64
    p.write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    bad=m.verify_source_manifest(p,hashlib.sha256(p.read_bytes()).hexdigest(),inv,2)
    assert bad["status"]=="BLOCKED"

def test_q8_09_h1_jsonl_and_stream_identity(tmp_path):
    m=_target()
    e103,_,_,_=_deps()
    rows=_rows()
    p=tmp_path/"h1.jsonl"
    p.write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in rows),encoding="utf-8")
    file_sha=hashlib.sha256(p.read_bytes()).hexdigest()
    stream=e103.canonical_stream_sha256(rows)
    out=m.load_h1_jsonl(p,file_sha,stream,e103)
    assert out["status"]=="PASS" and out["rows"]==rows
    out2=m.load_h1_jsonl(p,file_sha,"0"*64,e103)
    assert out2["status"]=="BLOCKED"

def test_q8_10_exposure_missing_malformed_blocks():
    m=_target()
    assert m.verify_exposure_declaration(None)["status"]=="BLOCKED"
    x=_exposure(m)
    del x["human_authority_reference"]
    assert m.verify_exposure_declaration(x)["status"]=="BLOCKED"

def test_q8_11_prior_exposure_not_clean():
    m=_target()
    assert _exposure(m)["oos_clean"] is True
    assert _exposure(m,"PREVIOUSLY_OBSERVED")["oos_clean"] is False

def test_q8_12_authority_exact_max_one():
    m=_target()
    a=_authority(m)
    assert m.verify_one_shot_authority(a,executor_blob="3"*40)["status"]=="PASS"
    b=dict(a); b["max_runs"]=2; b["canonical_digest"]=m.canonical_sha256({k:v for k,v in b.items() if k!="canonical_digest"})
    assert m.verify_one_shot_authority(b,executor_blob="3"*40)["status"]=="BLOCKED"

def test_q8_13_marker_cannot_be_consumed_twice(tmp_path):
    m=_target()
    a=_authority(m)
    marker=tmp_path/"used.marker"
    assert m.consume_authorization_once(marker,a)["status"]=="PASS"
    assert m.consume_authorization_once(marker,a)["status"]=="BLOCKED"

def test_q8_14_authority_mismatch_blocks():
    m=_target()
    a=_authority(m)
    assert m.verify_one_shot_authority(a,executor_blob="4"*40)["status"]=="BLOCKED"
    b=dict(a); b["experiment_id"]="OTHER"; b["canonical_digest"]=m.canonical_sha256({k:v for k,v in b.items() if k!="canonical_digest"})
    assert m.verify_one_shot_authority(b,executor_blob="3"*40)["status"]=="BLOCKED"

def test_q8_15_partition_attribution_exact():
    m=_target()
    assert m.classify_trade(OOS-2,OOS-1)=="PRE_OOS"
    assert m.classify_trade(OOS,OOS+1)=="OOS"
    assert m.classify_trade(OOS-1,OOS)=="CROSS_BOUNDARY"

def test_q8_16_open_position_not_forced_closed():
    m=_target()
    records=[
        {"h1_start_ms_utc":OOS,"execution":{"status":"EXECUTED","events":[{"timestamp_ms":OOS,"action":"BUY","quantity":1,"price_side":"ASK","price":100.0}]}}
    ]
    out=m.derive_trade_ledger(records)
    assert out["closed_trades"]==[]
    assert out["open_position"]["status"]=="OPEN_UNREALIZED"
    assert out["open_position"]["direction"]=="LONG"

def test_q8_17_metrics_schema_and_drawdown():
    m=_target()
    trades=[
        {"direction":"LONG","entry_timestamp_ms":OOS,"entry_price":100.0,"exit_timestamp_ms":OOS+1,"exit_price":103.0,"realized_unit_pnl":3.0,"partition":"OOS","calendar_period":"2025"},
        {"direction":"SHORT","entry_timestamp_ms":OOS+2,"entry_price":100.0,"exit_timestamp_ms":OOS+3,"exit_price":104.0,"realized_unit_pnl":-4.0,"partition":"OOS","calendar_period":"2025"},
        {"direction":"LONG","entry_timestamp_ms":OOS+4,"entry_price":100.0,"exit_timestamp_ms":OOS+5,"exit_price":102.0,"realized_unit_pnl":2.0,"partition":"OOS","calendar_period":"2025"},
    ]
    records=[{"execution":{"status":"EXECUTED","events":[]}}]
    out=m.compute_metrics(trades,records)
    assert tuple(out["full_sample"].keys())==m.FULL_METRIC_KEYS
    assert out["full_sample"]["aggregate_realized_unit_pnl"]==1.0
    assert out["full_sample"]["realized_closed_trade_max_drawdown"]==4.0

def test_q8_18_synthetic_executor_deterministic(tmp_path):
    m=_target()
    _,e104,e105,e107=_deps()
    rows=_rows()
    raw=_raw_rows(rows)
    exposure=_exposure(m)
    authority=_authority(m)
    env={"implementation":"cpython","version":"3.12","system":"synthetic","machine":"x86_64","dependencies":{},"environment_variables":{}}
    pre=e107.build_preflight(repository_full_name=m.REPOSITORY,branch=m.BRANCH,head="1"*40,tree="2"*40,preflight_tool_blob="8"*40,environment_snapshot=env)
    out1=m.run_synthetic_qualification(rows,raw,e105,e104,e107,pre,exposure,authority,tmp_path/"a.marker")
    out2=m.run_synthetic_qualification(rows,raw,e105,e104,e107,pre,exposure,authority,tmp_path/"b.marker")
    assert out1["status"]=="PASS" and out1["result"]==out2["result"]
    assert out1["trace"]["execution_status"]=="QUALIFICATION_FIXTURE"

def test_q8_19_result_payload_bindings():
    m=_target()
    records=[]
    exposure=_exposure(m)
    authority=_authority(m)
    result=m.build_result_payload(records,exposure,authority,execution_status="QUALIFICATION_FIXTURE")
    assert result["records_digest"]==m.canonical_sha256(records)
    assert result["exposure_digest"]==exposure["canonical_digest"]
    assert result["authority_digest"]==authority["canonical_digest"]
    assert result["result_digest"]==m.canonical_sha256({k:v for k,v in result.items() if k!="result_digest"})

def test_q8_20_no_forbidden_automatic_or_live_surface():
    m=_target()
    source=TARGET_PATH.read_text(encoding="utf-8")
    forbidden=("MetaTrader5","requests.","urllib.request","subprocess.","optimize","automatic_retry","while True")
    assert all(x not in source for x in forbidden)
    assert not hasattr(m,"rerun")
    assert not hasattr(m,"optimize")
    assert set(m.FORBIDDEN_CLAIMS)==set(CONTRACT["forbidden_claims"])
