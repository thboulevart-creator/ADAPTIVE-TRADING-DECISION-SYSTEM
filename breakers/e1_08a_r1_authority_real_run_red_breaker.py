from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
TARGET=Path(os.environ.get("E1_08A_R1_TARGET_PATH",ROOT/"tools/e1_08a_r1_real_run.py"))
CONTRACT_PATH=ROOT/"GOVERNANCE/E1-08A-R1-AUTHORITY-REAL-RUN-CLOSURE-CONTRACT-V0.1.json"
CONTRACT=json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
EXPECTED_HEAD=os.environ.get("E1_R1_EXPECTED_HEAD")
EXPECTED_TREE=os.environ.get("E1_R1_EXPECTED_TREE")
HUMAN_REF="HUMAN_DECISION_SHA256:"+"a"*64

assert CONTRACT["schema"]=="ATDS_E1_08A_R1_AUTHORITY_REAL_RUN_CLOSURE_CONTRACT_V0_1"
assert [x[0] for x in CONTRACT["tests"]]==[f"R1-{i:02d}" for i in range(1,23)]

def _target():
    if not TARGET.is_file():
        pytest.fail("E1_08A_R1_TARGET_ABSENT_EXPECTED_RED",pytrace=False)
    spec=importlib.util.spec_from_file_location("e108r1",TARGET)
    if spec is None or spec.loader is None:
        pytest.fail("E1_08A_R1_TARGET_UNLOADABLE_EXPECTED_RED",pytrace=False)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def _load(path,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def _base():
    return _load("tools/e1_08_one_shot_real_e1.py","e108base")

def _e103():
    return _load("tools/e1_03_h1_dataset_identity.py","e103")

def _auth(m,*,head=None,tree=None,executor_blob=None,human_ref=HUMAN_REF,authorized_at="2026-09-29T07:30:00Z"):
    head=head or EXPECTED_HEAD or "1"*40
    tree=tree or EXPECTED_TREE or "2"*40
    executor_blob=executor_blob or m.git_blob_sha1_file(TARGET)
    out={
        "schema":"E1_ONE_SHOT_RUN_AUTHORITY_V0",
        "experiment_id":m.EXPERIMENT_ID,
        "run_id":"E1-R1-SYNTHETIC-FIXTURE",
        "repository":m.REPOSITORY,
        "branch":m.BRANCH,
        "authorized_base_head":head,
        "authorized_base_tree":tree,
        "executor_blob":executor_blob,
        "protected_bindings":dict(m.BASE_PROTECTED_BLOBS),
        "source_manifest_sha256":m.SOURCE_MANIFEST_SHA256,
        "h1_jsonl_sha256":m.H1_JSONL_SHA256,
        "oos_start":m.OOS_START,
        "oos_end":m.OOS_END,
        "max_runs":1,
        "real_e1_run_authorized":True,
        "authorized_at_utc":authorized_at,
        "human_decision_reference":human_ref,
    }
    out["canonical_digest"]=m.canonical_sha256(out)
    return out

def _h1_rows():
    H=3_600_000; start=1_700_000_000_000; rows=[]
    for i in range(23):
        close=100.0
        if i==20: close=110.0
        elif i==21: close=90.0
        elif i==22: close=100.0
        rows.append({"h1_start_ms_utc":start+i*H,"source_segment_id":1,"continuity_block_id":1,"continuity_ordinal":i,"mid_close":close})
    return rows

def _write_h1(path,rows):
    path.write_text("".join(json.dumps(x,sort_keys=True,separators=(",",":"))+"\n" for x in rows),encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest(),_e103().canonical_stream_sha256(rows)

def _write_parquet(path,timestamps,bids,asks,*,unit="ms"):
    import pyarrow as pa
    import pyarrow.parquet as pq
    table=pa.table({
        "timestamp":pa.array(timestamps,type=pa.timestamp(unit)),
        "bid_price":pa.array(bids,type=pa.float64()),
        "ask_price":pa.array(asks,type=pa.float64()),
    })
    pq.write_table(table,path)

def _manifest(path,corpus,files):
    rows=[]
    for p in files:
        raw=p.read_bytes()
        rows.append({"relative_path":p.relative_to(corpus).as_posix(),"size_bytes":len(raw),"mtime_ns":p.stat().st_mtime_ns,
                     "sha256":hashlib.sha256(raw).hexdigest(),"sha256_status":"PASS","parquet_magic_status":"PASS"})
    payload={"schema":"ATDS_E0_SOURCE_B_ACCESS_MANIFEST_V0_1","status":"MANIFEST_COMPLETE",
             "inventory":{"parquet_files":len(rows),"files":rows}}
    path.write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n",encoding="utf-8")
    return payload,hashlib.sha256(path.read_bytes()).hexdigest()

def test_r1_01_surface():
    m=_target()
    assert m.CONTRACT=="ATDS_E1_08A_R1_REAL_RUN_V0_1"
    required={"canonical_sha256","git_blob_sha1_file","verify_runtime_environment","read_git_identity",
              "verify_real_one_shot_authority","ParquetTickCursor","build_provenance_bridge","run_real_one_shot"}
    assert required.issubset(set(dir(m)))

def test_r1_02_frozen_parent_bindings():
    m=_target()
    assert m.BASE_EXECUTOR_BLOB=="a4a04a7f63546e09d43f8c043d41872ec973a900"
    assert m.BASE_PROTECTED_BLOBS==_base().PROTECTED_BLOBS
    assert m.E1_08A_CONTRACT_BLOB=="4d868b34c42fe6765ece8007a0bf173d22199ab1"
    assert m.E1_08A_BREAKER_BLOB=="20297ca64c12bf9cd1eb9f6bef73598692959342"

def test_r1_03_strict_authority_pass():
    m=_target(); a=_auth(m)
    out=m.verify_real_one_shot_authority(a,executor_blob=a["executor_blob"],expected_head=a["authorized_base_head"],
                                         expected_tree=a["authorized_base_tree"],expected_human_decision_reference=HUMAN_REF)
    assert out["status"]=="PASS"

def test_r1_04_head_substitution_blocks():
    m=_target(); a=_auth(m)
    assert m.verify_real_one_shot_authority(a,executor_blob=a["executor_blob"],expected_head="f"*40,
        expected_tree=a["authorized_base_tree"],expected_human_decision_reference=HUMAN_REF)["status"]=="BLOCKED"

def test_r1_05_tree_substitution_blocks():
    m=_target(); a=_auth(m)
    assert m.verify_real_one_shot_authority(a,executor_blob=a["executor_blob"],expected_head=a["authorized_base_head"],
        expected_tree="f"*40,expected_human_decision_reference=HUMAN_REF)["status"]=="BLOCKED"

@pytest.mark.parametrize("ref",["","HUMAN_DECISION_SHA256:xyz","a"*64],ids=["missing","malformed","untyped"])
def test_r1_06_human_reference_blocks(ref):
    m=_target(); a=_auth(m,human_ref=ref)
    assert m.verify_real_one_shot_authority(a,executor_blob=a["executor_blob"],expected_head=a["authorized_base_head"],
        expected_tree=a["authorized_base_tree"],expected_human_decision_reference=HUMAN_REF)["status"]=="BLOCKED"

@pytest.mark.parametrize("ts",["2026-09-29","2026-09-29T07:30:00","not-a-time"],ids=["date","naive","invalid"])
def test_r1_07_bad_authorized_at_blocks(ts):
    m=_target(); a=_auth(m,authorized_at=ts)
    assert m.verify_real_one_shot_authority(a,executor_blob=a["executor_blob"],expected_head=a["authorized_base_head"],
        expected_tree=a["authorized_base_tree"],expected_human_decision_reference=HUMAN_REF)["status"]=="BLOCKED"

def test_r1_08_executor_substitution_blocks():
    m=_target(); a=_auth(m)
    assert m.verify_real_one_shot_authority(a,executor_blob="f"*40,expected_head=a["authorized_base_head"],
        expected_tree=a["authorized_base_tree"],expected_human_decision_reference=HUMAN_REF)["status"]=="BLOCKED"

def test_r1_09_runtime_environment_exact():
    m=_target(); out=m.verify_runtime_environment()
    assert out["status"]=="PASS"
    assert out["python"]=="3.12.14" and out["pyarrow"]=="25.0.1"

def test_r1_10_git_identity_observed():
    m=_target()
    if not EXPECTED_HEAD or not EXPECTED_TREE: pytest.fail("E1_R1_EXACT_HEAD_TREE_REQUIRED",pytrace=False)
    assert m.read_git_identity(ROOT)=={"head":EXPECTED_HEAD,"tree":EXPECTED_TREE}
    assert m.verify_git_identity(ROOT,EXPECTED_HEAD,EXPECTED_TREE)["status"]=="PASS"
    assert m.verify_git_identity(ROOT,"f"*40,EXPECTED_TREE)["status"]=="BLOCKED"

def test_r1_11_git_blob_identity():
    m=_target()
    assert m.git_blob_sha1_file(ROOT/"tools/e1_08_one_shot_real_e1.py")==m.BASE_EXECUTOR_BLOB
    p=ROOT/"tools/e1_08_one_shot_real_e1.py"
    assert m.verify_git_blob_file(p,m.BASE_EXECUTOR_BLOB)["status"]=="PASS"

def test_r1_12_parquet_cursor_mapping_and_gap(tmp_path):
    m=_target(); p=tmp_path/"x.parquet"
    _write_parquet(p,[1_000_000,1_060_000,1_120_001],[10,11,12],[11,12,13])
    row={"relative_path":"x.parquet","size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    c=m.ParquetTickCursor(tmp_path,[row])
    out=[next(c),next(c),next(c)]
    assert [x["timestamp_ms"] for x in out]==[1_000_000,1_060_000,1_120_001]
    assert [x["continuity_status"] for x in out]==["OK","OK","FORBIDDEN_BOUNDARY"]
    assert [(x["bid"],x["ask"]) for x in out]==[(10.0,11.0),(11.0,12.0),(12.0,13.0)]

def test_r1_13_hash_mismatch_before_yield(tmp_path):
    m=_target(); p=tmp_path/"x.parquet"; _write_parquet(p,[1_000],[10],[11])
    row={"relative_path":"x.parquet","size_bytes":p.stat().st_size,"sha256":"0"*64}
    c=m.ParquetTickCursor(tmp_path,[row])
    with pytest.raises(m.R1Error,match="PARQUET_SHA256_MISMATCH"): next(c)
    assert c.rows_yielded==0

def test_r1_14_schema_or_timestamp_unit_blocks(tmp_path):
    m=_target(); p=tmp_path/"x.parquet"; _write_parquet(p,[1_000],[10],[11],unit="s")
    row={"relative_path":"x.parquet","size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    with pytest.raises(m.R1Error,match="PARQUET_TIMESTAMP_TYPE_MISMATCH"): next(m.ParquetTickCursor(tmp_path,[row]))

def test_r1_15_non_increasing_across_files_blocks(tmp_path):
    m=_target(); a=tmp_path/"a.parquet"; b=tmp_path/"b.parquet"
    _write_parquet(a,[2_000],[10],[11]); _write_parquet(b,[1_000],[12],[13])
    rows=[{"relative_path":p.name,"size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in (a,b)]
    c=m.ParquetTickCursor(tmp_path,rows); next(c)
    with pytest.raises(m.R1Error,match="NON_INCREASING_SOURCE_TIMESTAMP"): next(c)

def test_r1_16_cursor_single_pass(tmp_path):
    m=_target(); p=tmp_path/"x.parquet"; _write_parquet(p,[1_000,2_000],[10,11],[11,12])
    row={"relative_path":"x.parquet","size_bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    c=m.ParquetTickCursor(tmp_path,[row]); assert iter(c) is c
    assert next(iter(c))["timestamp_ms"]==1_000
    assert next(iter(c))["timestamp_ms"]==2_000
    with pytest.raises(StopIteration): next(iter(c))

def test_r1_17_provenance_bridge():
    m=_target(); p=m.build_provenance_bridge()
    assert p["execution_raw_source"]["manifest_sha256"]=="c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
    assert p["signal_intermediate_source"]["manifest_sha256"]=="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert p["h1_source"]["canonical_stream_sha256"]=="15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"

def test_r1_18_real_orchestration_synthetic_parquet(tmp_path,monkeypatch):
    m=_target(); e103=_e103()
    corpus=tmp_path/"corpus"; corpus.mkdir(); pq=corpus/"x.parquet"
    rows=_h1_rows(); H=3_600_000
    _write_parquet(pq,[rows[20]["h1_start_ms_utc"]+H,rows[21]["h1_start_ms_utc"]+H,rows[22]["h1_start_ms_utc"]+H],
                   [100,104,99],[101,105,100])
    manifest=tmp_path/"manifest.json"; payload,manifest_sha=_manifest(manifest,corpus,[pq])
    inventory=m.canonical_inventory_digest(payload["inventory"]["files"])
    h1=tmp_path/"h1.jsonl"; h1_sha,h1_stream=_write_h1(h1,rows)
    monkeypatch.setattr(m,"SOURCE_MANIFEST_SHA256",manifest_sha); monkeypatch.setattr(m,"SOURCE_INVENTORY_DIGEST",inventory)
    monkeypatch.setattr(m,"SOURCE_PARQUET_FILES",1); monkeypatch.setattr(m,"H1_JSONL_SHA256",h1_sha); monkeypatch.setattr(m,"H1_CANONICAL_STREAM_SHA256",h1_stream)
    executor=m.git_blob_sha1_file(TARGET); a=_auth(m,executor_blob=executor)
    exposure=tmp_path/"exposure.json"; result=tmp_path/"result.json"; trace=tmp_path/"trace.json"; marker=tmp_path/"used.marker"
    out=m.run_real_one_shot(repo_root=ROOT,source_manifest_path=manifest,source_corpus_root=corpus,h1_jsonl_path=h1,
        authority=a,expected_human_decision_reference=HUMAN_REF,prior_oos_performance_exposure="NONE_DECLARED",
        exposure_output_path=exposure,result_output_path=result,trace_output_path=trace,marker_path=marker)
    assert out["status"]=="PASS"
    assert all(p.exists() for p in (exposure,result,trace,marker))
    stored=json.loads(result.read_text(encoding="utf-8"))
    assert stored["provenance"]["execution_raw_source"]["manifest_sha256"]==manifest_sha
    assert stored["base_result"]["execution_status"]=="REAL_E1_ONE_SHOT"

def test_r1_19_outputs_exclusive_create(tmp_path,monkeypatch):
    m=_target()
    result=tmp_path/"result.json"; result.write_text("occupied",encoding="utf-8")
    out=m.preflight_output_paths(tmp_path/"corpus",tmp_path/"exposure.json",result,tmp_path/"trace.json",tmp_path/"marker")
    assert out["status"]=="BLOCKED" and out["reason"]=="OUTPUT_ALREADY_EXISTS"

def test_r1_20_consumed_marker_blocks_second_execution(tmp_path):
    m=_target(); a=_auth(m); marker=tmp_path/"used.marker"
    base=_base()
    assert base.consume_authorization_once(marker,a)["status"]=="PASS"
    assert m.verify_unused_marker(marker)["status"]=="BLOCKED"

def test_r1_21_no_forbidden_surface():
    _target(); src=TARGET.read_text(encoding="utf-8")
    forbidden=("MetaTrader5","requests.","urllib.request","socket.","broker_order","live_order","automatic_retry","optimize_strategy")
    assert all(x not in src for x in forbidden)

def test_r1_22_legacy_mismatch_disclosed():
    m=_target(); p=m.build_provenance_bridge()
    notice=p["legacy_e1_07_binding_notice"]
    assert notice["legacy_identity"]=="SOURCE_B_USTECH_PRICE_CORE_V0_1"
    assert notice["legacy_manifest_sha256"]=="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert notice["correct_physical_source_manifest_sha256"]=="c341fb5eef9f013c602abfc9e3ca58afcdbab1b71af21b0429d46df37dd5b4a5"
    assert notice["status"]=="LEGACY_BINDING_MISMATCH_DISCLOSED"
