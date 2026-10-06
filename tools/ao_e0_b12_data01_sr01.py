from __future__ import annotations

A_PASS="A_QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION"
A_REJECT="REJECTED_NOT_RECONCILABLE"
B_PASS="A_REJECTED__B_QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION"
B_BLOCK="A_REJECTED__B_BLOCKED"

def adjudicate_a(*, frozen, validation_detail_prefreeze, deterministic, time_invariant,
                 strategy_independent, performance_independent, row_specific_lookup,
                 post_hoc_tolerance, dropped_quotes, interpolation, future_data_used,
                 validation_ts, validation_bid, validation_ask,
                 full_ts, full_bid, full_ask, full_ref_rows, full_candidate_rows,
                 provenance_sufficient):
    gates=[
        frozen, not validation_detail_prefreeze, deterministic, time_invariant,
        strategy_independent, performance_independent, not row_specific_lookup,
        not post_hoc_tolerance, not dropped_quotes, not interpolation, not future_data_used,
        validation_ts==0, validation_bid==0, validation_ask==0,
        full_ts==0, full_bid==0, full_ask==0,
        full_ref_rows==2058942, full_candidate_rows==2058942,
        provenance_sufficient,
    ]
    return A_PASS if all(gates) else A_REJECT

def select_after_a(a):
    if a==A_PASS:
        return {"selected_path":"A","b_open":False}
    if a==A_REJECT:
        return {"selected_path":"B","b_open":True}
    raise ValueError("INVALID_A_STATE")

def adjudicate_b(*, provider_ok, instrument_ok, utc_ok, bid_ask_ok, ask_ge_bid,
                 scale_ok, schema_ok, decoder_deterministic, object_hash_ok,
                 interval_ok, append_only_ok, duplicate_semantics_ok,
                 conflicting_bytes_fail_closed, ordering_ok, no_forward_fill,
                 no_interpolation, no_volume, ap0_ok, h1_ok, warmup_ok,
                 forward_boundary_ok, no_performance_output, october_forward_used,
                 b12_opened, pipe01_first_read, source_b_continuation_claim,
                 auto_adopt):
    gates=[
        provider_ok,instrument_ok,utc_ok,bid_ask_ok,ask_ge_bid,scale_ok,schema_ok,
        decoder_deterministic,object_hash_ok,interval_ok,append_only_ok,
        duplicate_semantics_ok,conflicting_bytes_fail_closed,ordering_ok,
        no_forward_fill,no_interpolation,no_volume,ap0_ok,h1_ok,warmup_ok,
        forward_boundary_ok,no_performance_output,not october_forward_used,
        not b12_opened,not pipe01_first_read,not source_b_continuation_claim,
        not auto_adopt,
    ]
    return B_PASS if all(gates) else B_BLOCK
