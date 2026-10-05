from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"GOVERNANCE"/"AO-E0-CELL-01-EXACT-STRATEGY-QUALIFICATION-CELL-IDENTITY-CONTRACT-V0.1.json"
SER=ROOT/"GOVERNANCE"/"AO-E0-CELL-01-CANONICAL-SERIALIZATION-V0.1.json"
DIMENSIONS=("strategy_version_identity","qualification_claim_identity","asset_instrument_identity","timeframe_horizon_identity","execution_model_identity","cost_scope_identity","context_domain_identity")
FORBIDDEN_KEYS={"dataset_instance","dataset_hash","sample_window","exact_sample_window","oos_partition","individual_test_run","result","p_value","performance_metric","evidence_package","qualification_decision_timestamp"}
def canon(o): return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def digest(o): return "sha256:"+hashlib.sha256(canon(o).encode("utf-8")).hexdigest()
def walk_keys(o):
    if isinstance(o,dict):
        for k,v in o.items():
            yield k; yield from walk_keys(v)
    elif isinstance(o,list):
        for v in o: yield from walk_keys(v)
def validate_payload(payload):
    assert payload["schema"]=="ATDS_AO_E0_STRATEGY_QUALIFICATION_CELL_IDENTITY_V0_1"
    dims=payload["cell_dimensions"]; assert tuple(sorted(dims))==tuple(sorted(DIMENSIONS)); assert not (set(walk_keys(payload)) & FORBIDDEN_KEYS)
    assert dims["asset_instrument_identity"]["source_b_feed_equivalence_to_vt_execution_feed"] is False
    assert dims["execution_model_identity"]["full_broker_execution_realism_claimed"] is False
    assert dims["execution_model_identity"]["mid_is_execution_price"] is False
    assert dims["execution_model_identity"]["same_bar_execution"]=="FORBIDDEN"; assert dims["execution_model_identity"]["no_pyramiding"] is True
    assert dims["cost_scope_identity"]["policy_stress_is_observed_historical_cost"] is False
    assert dims["context_domain_identity"]["context_routing"]=="NONE"; assert dims["context_domain_identity"]["context_scope_mode"]=="FIXED_BY_EVIDENCE"; assert dims["context_domain_identity"]["unknown_context_transportability"]=="UNKNOWN"
    return True
def run():
    c=json.loads(CONTRACT.read_text(encoding="utf-8")); raw=SER.read_bytes(); assert not raw.endswith(b"\n"); payload=json.loads(raw.decode("utf-8")); assert raw.decode("utf-8")==canon(payload); validate_payload(payload); assert digest(payload)==c["cell_identity"]
    assert c["cell_identity_status"]=="QUALIFIED_CANDIDATE_FOR_HUMAN_ADOPTION"; assert c["human_adopted"] is False; assert c["authority"]["oos_consumption_authorized"] is False; assert c["authority"]["real_performance_observation_authorized"] is False; assert c["authority"]["b12"]=="CLOSED"
    mutations=[]
    def mut(path,value):
        x=copy.deepcopy(payload); cur=x
        for key in path[:-1]: cur=cur[key]
        cur[path[-1]]=value; mutations.append(x)
    mut(("cell_dimensions","strategy_version_identity","strategy_runtime_blob"),"0"*40); mut(("cell_dimensions","strategy_version_identity","lookback_completed_admissible_h1_bars"),21); mut(("cell_dimensions","execution_model_identity","e1_04_runtime_blob"),"1"*40); mut(("cell_dimensions","cost_scope_identity","exec_04_policy_blob"),"2"*40); mut(("cell_dimensions","qualification_claim_identity","h1"),"theta_AO_E0 > 6.0"); mut(("cell_dimensions","context_domain_identity","context_routing"),"REGIME_ROUTED")
    assert all(digest(x)!=c["cell_identity"] for x in mutations)
    x=copy.deepcopy(payload); del x["cell_dimensions"]["cost_scope_identity"]
    try: validate_payload(x)
    except AssertionError: pass
    else: raise AssertionError("OMITTED_DIMENSION_MUST_FAIL")
    for key in ("dataset_hash","oos_partition","result","p_value","performance_metric","evidence_package"):
        x=copy.deepcopy(payload); x["cell_dimensions"]["qualification_claim_identity"][key]="FORBIDDEN"
        try: validate_payload(x)
        except AssertionError: pass
        else: raise AssertionError(f"{key}_MUST_FAIL")
    x=copy.deepcopy(payload); x["cell_dimensions"]["asset_instrument_identity"]["source_b_feed_equivalence_to_vt_execution_feed"]=True
    try: validate_payload(x)
    except AssertionError: pass
    else: raise AssertionError("FEED_EQUIVALENCE_LAUNDERING_MUST_FAIL")
    x=copy.deepcopy(payload); x["cell_dimensions"]["cost_scope_identity"]["slippage_bps_per_execution_event"]=8; assert digest(x)!=c["cell_identity"]; assert c["material_change_rule"]=="NEW_QUALIFICATION_CELL_IDENTITY_NO_AUTOMATIC_TRANSFER"
    print("AO_E0_CELL_01_BREAKER_PASS")
if __name__=="__main__": run()
