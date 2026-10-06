from tools.ao_e0_b12_data01_sr01 import *

BASE_A=dict(
 frozen=True,validation_detail_prefreeze=False,deterministic=True,time_invariant=True,
 strategy_independent=True,performance_independent=True,row_specific_lookup=False,
 post_hoc_tolerance=False,dropped_quotes=False,interpolation=False,future_data_used=False,
 validation_ts=0,validation_bid=0,validation_ask=0,full_ts=0,full_bid=0,full_ask=0,
 full_ref_rows=2058942,full_candidate_rows=2058942,provenance_sufficient=True)
BASE_B=dict(
 provider_ok=True,instrument_ok=True,utc_ok=True,bid_ask_ok=True,ask_ge_bid=True,
 scale_ok=True,schema_ok=True,decoder_deterministic=True,object_hash_ok=True,
 interval_ok=True,append_only_ok=True,duplicate_semantics_ok=True,
 conflicting_bytes_fail_closed=True,ordering_ok=True,no_forward_fill=True,
 no_interpolation=True,no_volume=True,ap0_ok=True,h1_ok=True,warmup_ok=True,
 forward_boundary_ok=True,no_performance_output=True,october_forward_used=False,
 b12_opened=False,pipe01_first_read=False,source_b_continuation_claim=False,
 auto_adopt=False)

A_MUTATIONS=[
 ("validation_detail_prefreeze",True),("frozen",False),("row_specific_lookup",True),
 ("post_hoc_tolerance",True),("dropped_quotes",True),("interpolation",True),
 ("performance_independent",False),("strategy_independent",False),
 ("validation_ts",1),("validation_bid",1),("validation_ask",1),
 ("full_ts",1),("full_bid",1),("full_ask",1),("provenance_sufficient",False)]
B_MUTATIONS=[
 ("source_b_continuation_claim",True),("october_forward_used",True),
 ("no_forward_fill",False),("no_interpolation",False),("no_volume",False),
 ("ap0_ok",False),("h1_ok",False),("no_performance_output",False),
 ("b12_opened",True),("pipe01_first_read",True),("provider_ok",False),
 ("decoder_deterministic",False),("conflicting_bytes_fail_closed",False),
 ("auto_adopt",True),("instrument_ok",False)]

def test_a_positive():
    assert adjudicate_a(**BASE_A)==A_PASS

def test_a_breakers():
    for k,v in A_MUTATIONS:
        d=BASE_A.copy(); d[k]=v
        assert adjudicate_a(**d)==A_REJECT

def test_a_to_b_transition():
    assert select_after_a(A_REJECT)=={"selected_path":"B","b_open":True}
    assert select_after_a(A_PASS)=={"selected_path":"A","b_open":False}

def test_b_positive():
    assert adjudicate_b(**BASE_B)==B_PASS

def test_b_breakers():
    for k,v in B_MUTATIONS:
        d=BASE_B.copy(); d[k]=v
        assert adjudicate_b(**d)==B_BLOCK

def test_total_named_breakers_is_30():
    assert len(A_MUTATIONS)+len(B_MUTATIONS)==30
