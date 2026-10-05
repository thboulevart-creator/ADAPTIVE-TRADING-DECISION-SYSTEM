from __future__ import annotations
import copy, importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,R/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
A=load("a",Path("tools/ao_e0_dt_01a_cc05_data_admission.py"))
B=load("b",Path("tools/ao_e0_dt_01b_e1_pit_admissibility.py"))
def good_data():
    return {"cell_identity":A.CELL_IDENTITY,"claim_class":"CC05_ECONOMIC_NET_PROFITABILITY","source_b_feed_equals_vt_execution_feed":False,"native_dukascopy_tick_equivalence_claimed":False,"data02_cc02_transferred_to_cc05":False,"family":copy.deepcopy(A.EXPECTED),"mid_as_execution_price":False,"temporal_pass_claimed":False,"scientific_support_claimed":False}
def good_trace():
    s=1_800_000_000_000
    return {"h1_start_ms":s,"lookback_h1_start_ms":s-20*B.HOUR_MS,"same_continuity_block":True,"execution_tick_ms":s+B.HOUR_MS,"future_h1_dependency":False,"future_aware_transformation":False,"same_bar_execution":False,"past_price_forward_fill":False,"future_bid_ask_used_for_signal":False,"essential_temporal_unknown":False,"research_freezes_pre_result":True,"source_b_equals_vt_feed_claim":False,"full_broker_realism_claim":False,"historical_vt_tradability_claim":False}
def expect_block_data(mut):
    x=good_data(); mut(x); assert A.qualify(x)["status"]=="BLOCKED"
def expect_block_trace(mut):
    x=good_trace(); mut(x); assert B.assess(x)["status"]=="BLOCKED"
def run():
    assert A.qualify(good_data())["status"]=="QUALIFIED_CANDIDATE"
    assert B.assess(good_trace())["status"]=="QUALIFIED_CANDIDATE"
    expect_block_data(lambda x:x.__setitem__("source_b_feed_equals_vt_execution_feed",True))
    expect_block_data(lambda x:x.__setitem__("native_dukascopy_tick_equivalence_claimed",True))
    expect_block_data(lambda x:x.__setitem__("data02_cc02_transferred_to_cc05",True))
    expect_block_data(lambda x:x.__setitem__("temporal_pass_claimed",True))
    expect_block_data(lambda x:x.__setitem__("scientific_support_claimed",True))
    expect_block_data(lambda x:x["family"]["h1"].__setitem__("canonical_stream_sha256","0"*64))
    expect_block_trace(lambda x:x.__setitem__("lookback_h1_start_ms",x["h1_start_ms"]+B.HOUR_MS))
    expect_block_trace(lambda x:x.__setitem__("execution_tick_ms",x["h1_start_ms"]+B.HOUR_MS-1))
    expect_block_trace(lambda x:x.__setitem__("same_bar_execution",True))
    expect_block_trace(lambda x:x.__setitem__("same_continuity_block",False))
    expect_block_trace(lambda x:x.__setitem__("future_aware_transformation",True))
    expect_block_trace(lambda x:x.__setitem__("past_price_forward_fill",True))
    expect_block_trace(lambda x:x.__setitem__("future_bid_ask_used_for_signal",True))
    expect_block_trace(lambda x:x.__setitem__("essential_temporal_unknown",True))
    expect_block_trace(lambda x:x.__setitem__("source_b_equals_vt_feed_claim",True))
    expect_block_trace(lambda x:x.__setitem__("research_freezes_pre_result",False))
    expect_block_trace(lambda x:x.__setitem__("full_broker_realism_claim",True))
    expect_block_trace(lambda x:x.__setitem__("historical_vt_tradability_claim",True))
    y=good_trace(); del y["future_h1_dependency"]; assert B.assess(y)["status"]=="BLOCKED"
    assert A.AUTHORITY["temporal"] is False
    assert B.AUTHORITY["rvo"] is False
    assert A.AUTHORITY["oos_consumption"] is False
    assert B.AUTHORITY["oos_consumption"] is False
    print("AO_E0_DT_01_BREAKER_PASS")
if __name__=="__main__": run()
