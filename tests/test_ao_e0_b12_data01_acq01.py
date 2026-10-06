from pathlib import Path
import pytest
from tools.ao_e0_b12_data01_acq01 import *

GOOD={"candidate_id":"DUKASCOPY_USATECH_FORWARD_CANDIDATE_V0_1","provider":"DUKASCOPY","instrument":"USATECH.IDX/USD","symbol":"USATECHIDXUSD"}

def test_01_source_binding_exact(): assert validate_source_binding(GOOD)["status"]=="PASS_SOURCE_BINDING"
def test_02_source_substitution_blocked(): assert validate_source_binding({**GOOD,"provider":"OTHER"})["status"]=="BLOCKED_SOURCE_SUBSTITUTION"
def test_03_requester_pays_blocked(): assert validate_cost_gate(requester_pays=True,human_spend_authorized=False)["status"]=="BLOCKED_REQUESTER_PAYS_HUMAN_AUTHORIZATION_REQUIRED"
def test_04_free_transport_allowed(): assert validate_cost_gate(requester_pays=False,human_spend_authorized=False)["status"]=="PASS_COST_GATE"
def test_05_exact_forward_boundary(): assert validate_forward_boundary(first_evidence_ms=FORWARD_START_MS,warmup_h1_bars=20,warmup_in_evidence=False)["status"]=="PASS_FORWARD_BOUNDARY"
def test_06_wrong_forward_boundary(): assert validate_forward_boundary(first_evidence_ms=FORWARD_START_MS+1,warmup_h1_bars=20,warmup_in_evidence=False)["status"]=="BLOCKED_WRONG_FORWARD_START"
def test_07_warmup_scope(): assert validate_forward_boundary(first_evidence_ms=FORWARD_START_MS,warmup_h1_bars=21,warmup_in_evidence=False)["status"]=="BLOCKED_WARMUP_SCOPE"
def test_08_warmup_evidence_forbidden(): assert validate_forward_boundary(first_evidence_ms=FORWARD_START_MS,warmup_h1_bars=20,warmup_in_evidence=True)["status"]=="BLOCKED_WARMUP_INCLUDED_AS_EVIDENCE"
def test_09_new_raw_object(): assert seal_raw_object(b"abc")["status"]=="PASS_NEW_RAW_OBJECT"
def test_10_duplicate_is_reproducibility():
    x=seal_raw_object(b"abc"); assert seal_raw_object(b"abc",x)["status"]=="PASS_REPRODUCIBILITY_DUPLICATE"
def test_11_conflicting_bytes_blocked():
    x=seal_raw_object(b"abc"); assert seal_raw_object(b"abd",x)["status"]=="BLOCKED_SOURCE_OBJECT_MUTATION"
def test_12_exact_overlap_scaled_candidate():
    r=[{"timestamp":1,"bid_price":"20.001","ask_price":"20.003"}]
    c=[{"timestamp":1,"raw_bid":20001,"raw_ask":20003}]
    assert assess_exact_overlap(r,c)["status"]=="PASS_EXACT_SOURCE_CONTINUATION"
def test_13_overlap_timestamp_mismatch_blocks():
    r=[{"timestamp":1,"bid_price":"20.001","ask_price":"20.003"}]
    c=[{"timestamp":2,"raw_bid":20001,"raw_ask":20003}]
    assert assess_exact_overlap(r,c)["status"]=="BLOCKED_SOURCE_CONTINUATION_NOT_EXACT"
def test_14_overlap_bid_mismatch_blocks():
    r=[{"timestamp":1,"bid_price":"20.001","ask_price":"20.003"}]
    c=[{"timestamp":1,"raw_bid":20002,"raw_ask":20003}]
    assert assess_exact_overlap(r,c)["status"]=="BLOCKED_SOURCE_CONTINUATION_NOT_EXACT"
def test_15_overlap_ask_mismatch_blocks():
    r=[{"timestamp":1,"bid_price":"20.001","ask_price":"20.003"}]
    c=[{"timestamp":1,"raw_bid":20001,"raw_ask":20004}]
    assert assess_exact_overlap(r,c)["status"]=="BLOCKED_SOURCE_CONTINUATION_NOT_EXACT"
def test_16_performance_peek_rejected():
    with pytest.raises(ACQ01Error,match="BLOCKED_PERFORMANCE_PEEK"): validate_rolling_state({"b12":"CLOSED","pnl":1})
def test_17_b12_open_rejected(): assert validate_rolling_state({"b12":"OPEN","exact_closed_trade_count":0})["status"]=="BLOCKED_AUTHORITY_BOUNDARY"
def test_18_wait_not_ready_below_n(): assert validate_rolling_state({"b12":"CLOSED","exact_closed_trade_count":58926,"data01_state":"WAIT_NOT_READY"})["status"]=="WAIT_NOT_READY_NO_PERFORMANCE_OBSERVATION"
def test_19_premature_ready_blocked(): assert validate_rolling_state({"b12":"CLOSED","exact_closed_trade_count":1,"data01_state":"READY"})["status"]=="BLOCKED_PREMATURE_READY"
def test_20_final_digest_out_of_scope():
    with pytest.raises(ACQ01Error,match="BLOCKED_FINAL_INSTANCE_OUT_OF_SCOPE"): build_final_instance_digest({})
def test_21_required_n_still_requires_count_contract(): assert validate_rolling_state({"b12":"CLOSED","exact_closed_trade_count":58927,"data01_state":"WAIT_NOT_READY"})["status"]=="BLOCKED_FINAL_INSTANCE_REQUIRES_SEPARATE_COUNT_ONLY_READINESS_CONTRACT"
def test_22_store_layout(tmp_path):
    for x in ("raw","manifests","evidence","ap0","h1"): (tmp_path/x).mkdir()
    assert validate_local_store_paths(tmp_path)["status"]=="PASS_STORE_LAYOUT"
