from __future__ import annotations
import copy, importlib.util, inspect, os
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
TARGET=Path(os.environ.get("E1_07_TARGET_PATH",ROOT/"tools/e1_07_preflight_trace.py"))
HEAD=os.environ.get("E1_07_EXPECTED_HEAD"); TREE=os.environ.get("E1_07_EXPECTED_TREE"); TOOL=os.environ.get("E1_07_EXPECTED_TOOL_BLOB")
ENV={"implementation":"cpython","version":"3.12.14","system":"Linux","machine":"x86_64","dependencies":{"pytest":"8.4.2","pluggy":"1.6.0"},"environment_variables":{"PYTHONHASHSEED":"0","TZ":"UTC"}}
RAW="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"; H1="15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f"; RUNNER="baad3bd7c2e810451737c89bf8f9bcabc17c5ba6"; QUAL="0793adc08416563125f57a55c0d272d24bb4b3df"
def sha40(x): return isinstance(x,str) and len(x)==40 and all(c in "0123456789abcdef" for c in x)
def load():
    if not TARGET.is_file(): pytest.fail("E1_07_TARGET_ABSENT_EXPECTED_RED",pytrace=False)
    if not sha40(HEAD) or not sha40(TREE): pytest.fail("E1_07_EXACT_HEAD_TREE_REQUIRED",pytrace=False)
    if not sha40(TOOL): pytest.fail("E1_07_EXACT_TOOL_BLOB_REQUIRED",pytrace=False)
    s=importlib.util.spec_from_file_location("e107",TARGET); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
    assert m.CONTRACT=="ATDS_E1_07_PREFLIGHT_REPRODUCIBILITY_TRACE_V0_1" and m.PREFLIGHT_SCHEMA_ID=="E1_PREFLIGHT_MANIFEST_V0" and m.RESULT_SCHEMA_ID=="E1_RESULT_ENVELOPE_SCHEMA_V0"; return m
def pf(env=None): return load().build_preflight(repository_full_name="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",branch="integration/system-v1",head=HEAD,tree=TREE,preflight_tool_blob=TOOL,environment_snapshot=copy.deepcopy(ENV if env is None else env))
def obs(m): return {"repository_full_name":m["repository"]["full_name"],"branch":m["repository"]["branch"],"head":m["repository"]["head"],"tree":m["repository"]["tree"],"preflight_tool_blob":m["repository"]["preflight_tool_blob"],"environment_identity":m["environment"]["identity_sha256"],"raw_dataset_identity":m["datasets"]["raw"]["identity"],"raw_manifest_sha256":m["datasets"]["raw"]["manifest_sha256"],"h1_dataset_identity":m["datasets"]["h1"]["identity"],"h1_stream_sha256":m["datasets"]["h1"]["canonical_stream_sha256"],"runner_blob":m["runner"]["runtime_blob"],"qualification_blob":m["qualification"]["qualifier_blob"],"result_schema_digest":m["result_schema"]["canonical_sha256"]}
def env(): m=pf(); return load().build_result_envelope(m,run_id="E1-07-QUALIFICATION-FIXTURE-001",timestamp_utc="2026-09-28T20:00:00Z",execution_status="QUALIFICATION_FIXTURE",metrics={"fixture_metric":1},result_payload={"fixture":True,"value":7}),m
def test_q7_01(): m=pf(); assert load().verify_preflight(m,observed=obs(m))["status"]=="PASS"
def test_q7_02(): assert pf()==pf()
def test_q7_03():
    e=copy.deepcopy(ENV); e["dependencies"]={"pluggy":"1.6.0","pytest":"8.4.2"}; assert pf(e)["canonical_digest"]==pf()["canonical_digest"]
def test_q7_04(): m=pf(); assert (m["repository"]["full_name"],m["repository"]["branch"])==("thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM","integration/system-v1")
def test_q7_05(): m=pf(); assert (m["repository"]["head"],m["repository"]["tree"])==(HEAD,TREE)
def test_q7_06(): m=pf(); assert m["strategy"]=={"strategy_id":"MOMENTUM_V1","mode":"OFFLINE","class":"EXPLORATORY","research_level":"N0","timeframe":"H1","lookback_completed_admissible_h1":20,"scope_freeze_blob":"6b1e0d6e76d9813cd50eb01eb4b6c06cbfa8260e"}
def test_q7_07(): assert pf()["window"]=={"raw_window_start":"2021-05-25T00:00:00.309Z","raw_window_end":"2026-05-24T23:59:59.963Z","pre_oos":"timestamp < 2025-05-25T00:00:00Z","oos_start":"2025-05-25T00:00:00Z","oos_end":"2026-05-24T23:59:59.963Z"}
def test_q7_08(): r=pf()["datasets"]["raw"]; assert (r["identity"],r["manifest_sha256"])==("SOURCE_B_USTECH_PRICE_CORE_V0_1",RAW)
def test_q7_09(): h=pf()["datasets"]["h1"]; assert (h["identity"],h["canonical_stream_sha256"],h["qualification_result_sha256"],h["jsonl_sha256"])==("USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1",H1,"3a96ac264f23b7c1f14de69dbe0444af5b25265b7a61d5e233479a4b581e6425","94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0")
def test_q7_10(): e=pf()["execution_model"]; assert (e["contract_blob"],e["runtime_blob"])==("cf07f1400af614fa53fe41afe8a40e412d28c87d","15e72b8743e7726fc8b8bedd933cf7defe56413b") and e["pnl_scope"]["spread"]=={"included":True,"mode":"RAW_BID_ASK_INTRINSIC"}
def test_q7_11(): assert pf()["runner"]["runtime_blob"]==RUNNER
def test_q7_12(): q=pf()["qualification"]; assert (q["contract_blob"],q["breaker_blob"],q["reference_blob"],q["qualifier_blob"],q["report_blob"])==("483552f2ea1def15f94a28f2e45b97dd65f786ff","dc4858559a2fda113c7290ad39a45d5291580773","25b01e6d31709f02f9c095262bfe78366e83003b",QUAL,"6f16f9367e932379a87b59599b59c7cc47127b1d")
def test_q7_13(): m=pf(); assert m["environment"]["descriptor"]==ENV and m["environment"]["identity_sha256"]==load().canonical_sha256(ENV)
def test_q7_14(): r=pf()["result_schema"]; assert (r["schema_id"],r["canonical_sha256"])==("E1_RESULT_ENVELOPE_SCHEMA_V0",load().RESULT_SCHEMA_CANONICAL_SHA256)
def test_q7_15(): assert not any(pf()["authority"].values())
@pytest.mark.parametrize(("k","bad"),[("head","0"*40),("tree","0"*40),("raw_manifest_sha256","0"*64),("h1_stream_sha256","0"*64),("runner_blob","0"*40),("qualification_blob","0"*40),("environment_identity","0"*64),("result_schema_digest","0"*64)],ids=["Q7-16","Q7-17","Q7-18","Q7-19","Q7-20","Q7-21","Q7-22","Q7-23"])
def test_substitution(k,bad): m=pf(); o=obs(m); o[k]=bad; assert load().verify_preflight(m,observed=o)["status"]=="BLOCKED"
def test_q7_24(): e,m=env(); assert load().verify_result_envelope(e,m)["status"]=="PASS"; assert {"experiment_id","preflight_digest","timestamp_utc","runner_identity","environment_identity","execution_status","result_payload","result_digest"}.issubset(e)
@pytest.mark.parametrize("kind",["payload","preflight","identity","trace"],ids=["Q7-25","Q7-26","Q7-27","Q7-28"])
def test_result_tamper(kind):
    e,m=env()
    if kind=="payload": e["result_payload"]["value"]=8
    elif kind=="preflight": e["preflight_digest"]="0"*64
    elif kind=="identity": e["datasets"]["raw"]["manifest_sha256"]="0"*64
    else: e["trace_digest"]="0"*64
    assert load().verify_result_envelope(e,m)["status"]=="BLOCKED"
def test_q7_29(): m=pf(); m["unexpected"]=True; assert load().verify_preflight(m,observed=obs(pf()))["status"]=="BLOCKED"
def test_q7_30():
    s=inspect.getsource(load()); forbidden=("run_momentum_runner(","qualify_fixture(","subprocess.","requests.","MetaTrader5","mt5.initialize","order_send("); assert not any(x in s for x in forbidden)
