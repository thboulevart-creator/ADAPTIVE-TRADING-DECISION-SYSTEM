from __future__ import annotations
CONTRACT="ATDS_AO_E0_DT_01B_E1_SCOPED_MINIMAL_PIT_ADMISSIBILITY_V0_1"
HOUR_MS=3_600_000
AUTHORITY={"generic_temporal":False,"rvo":False,"oos_consumption":False,"performance_observation":False}
def assess(trace:dict)->dict:
    required=("h1_start_ms","lookback_h1_start_ms","same_continuity_block","execution_tick_ms","future_h1_dependency","future_aware_transformation","same_bar_execution","past_price_forward_fill","future_bid_ask_used_for_signal","essential_temporal_unknown","research_freezes_pre_result","source_b_equals_vt_feed_claim","full_broker_realism_claim","historical_vt_tradability_claim")
    if any(k not in trace for k in required): return {"status":"BLOCKED","reason":"UNKNOWN_ESSENTIAL_TEMPORAL_PREDICATE"}
    if trace["essential_temporal_unknown"]: return {"status":"BLOCKED","reason":"UNKNOWN_ESSENTIAL_TEMPORAL_PREDICATE"}
    start=int(trace["h1_start_ms"]); decision=start+HOUR_MS; lookback=int(trace["lookback_h1_start_ms"]); tick=int(trace["execution_tick_ms"])
    if lookback>start: return {"status":"BLOCKED","reason":"FUTURE_H1_LEAKAGE"}
    if lookback!=start-20*HOUR_MS: return {"status":"BLOCKED","reason":"LOOKBACK_NOT_T_MINUS_20_H1"}
    if trace["same_continuity_block"] is not True: return {"status":"BLOCKED","reason":"CROSS_CONTINUITY_LOOKBACK"}
    if trace["future_h1_dependency"] is not False: return {"status":"BLOCKED","reason":"FUTURE_H1_LEAKAGE"}
    if trace["future_aware_transformation"] is not False: return {"status":"BLOCKED","reason":"FUTURE_AWARE_TRANSFORMATION"}
    if tick<decision: return {"status":"BLOCKED","reason":"FUTURE_TICK_OR_SAME_BAR_BOUNDARY_VIOLATION"}
    if trace["same_bar_execution"] is not False: return {"status":"BLOCKED","reason":"SAME_BAR_EXECUTION"}
    if trace["past_price_forward_fill"] is not False: return {"status":"BLOCKED","reason":"PAST_PRICE_FORWARD_FILL"}
    if trace["future_bid_ask_used_for_signal"] is not False: return {"status":"BLOCKED","reason":"FUTURE_BID_ASK_SIGNAL_LEAKAGE"}
    if trace["research_freezes_pre_result"] is not True: return {"status":"BLOCKED","reason":"POST_RESULT_RESEARCH_SELECTION"}
    if trace["source_b_equals_vt_feed_claim"] is not False: return {"status":"BLOCKED","reason":"SOURCE_B_VT_FEED_LAUNDERING"}
    if trace["full_broker_realism_claim"] is not False: return {"status":"BLOCKED","reason":"FULL_BROKER_REALISM_LAUNDERING"}
    if trace["historical_vt_tradability_claim"] is not False: return {"status":"BLOCKED","reason":"HISTORICAL_VT_TRADABILITY_LAUNDERING"}
    return {"status":"QUALIFIED_CANDIDATE","b6":"CANDIDATE_PASS","decision_time_ms":decision,"temporal_mode":"E1_REPLAY_POINT_IN_TIME"}
