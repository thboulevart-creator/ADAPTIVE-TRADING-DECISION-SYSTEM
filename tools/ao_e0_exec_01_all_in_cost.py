from __future__ import annotations
import math
from datetime import datetime, timezone

CONTRACT="ATDS_AO_E0_EXEC_01_E1_SCOPED_ALL_IN_COST_V0_1"
BASE_EXECUTION_CONTRACT="ATDS_E1_04_EXECUTION_COST_MODEL_V0_1"
UNIT="PRICE_UNITS_PER_UNIT_POSITION"
REQUIRED_COMPONENTS=("commission","slippage","financing")
NONNEGATIVE_COMPONENTS=("commission","slippage")
OOS_START=datetime.fromisoformat("2025-05-25T00:00:00+00:00")
OOS_END=datetime.fromisoformat("2026-05-24T23:59:59.963+00:00")
AUTHORITY={"oos_consumption_authorized":False,"real_performance_observation_authorized":False,"strategy_qualification_authorized":False,"paper_broker_live_capital_authorized":False}
_REQUIRED_SCOPE=("strategy_id","instrument","timeframe","base_execution_contract","execution_venue_identity","account_cost_profile_identity","symbol_contract_identity","cost_schedule_effective_from_utc","cost_schedule_effective_to_utc","cost_profile_source_ref","unit_conversion_identity_or_NOT_REQUIRED_WITH_BASIS")
_ALLOWED_STATES={"EXACT","BOUNDED","NOT_APPLICABLE_WITH_EVIDENCE","UNKNOWN"}
_ALLOWED_PROVENANCE={"OBSERVED","CONTRACTUAL","ESTIMATED_WITH_BOUND","POLICY_BOUND","NOT_APPLICABLE_EVIDENCE"}

def _d(status,reason=None,**extra):
    out={"status":status}
    if reason is not None: out["reason"]=reason
    out.update(extra); return out
def _finite(x): return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(float(x))
def _utc(v):
    if not isinstance(v,str) or not v.strip(): return None
    try: dt=datetime.fromisoformat(v.replace("Z","+00:00"))
    except ValueError: return None
    if dt.tzinfo is None: return None
    return dt.astimezone(timezone.utc)
def _scope(s):
    if not isinstance(s,dict): return _d("BLOCKED","MISSING_SCOPE_BINDING")
    for k in _REQUIRED_SCOPE:
        if not isinstance(s.get(k),str) or not s[k].strip(): return _d("BLOCKED","MISSING_SCOPE_BINDING",field=k)
    if s["strategy_id"]!="MOMENTUM_V1": return _d("BLOCKED","STRATEGY_SCOPE_MISMATCH")
    if s["instrument"]!="USTECH" or s["timeframe"]!="H1": return _d("BLOCKED","MARKET_SCOPE_MISMATCH")
    if s["base_execution_contract"]!=BASE_EXECUTION_CONTRACT: return _d("BLOCKED","BASE_EXECUTION_CONTRACT_MISMATCH")
    a,b=_utc(s["cost_schedule_effective_from_utc"]),_utc(s["cost_schedule_effective_to_utc"])
    if a is None or b is None or a>OOS_START or b<OOS_END: return _d("BLOCKED","COST_SCHEDULE_DOES_NOT_COVER_OOS")
    return _d("PASS")
def _component(name,c):
    if not isinstance(c,dict): return _d("BLOCKED","MISSING_REQUIRED_COST_COMPONENT",component=name)
    state,prov,ref,unit=c.get("state"),c.get("provenance_kind"),c.get("source_ref"),c.get("unit")
    if state not in _ALLOWED_STATES: return _d("BLOCKED","INVALID_COST_STATE",component=name)
    if state=="UNKNOWN": return _d("BLOCKED","UNKNOWN_COST_COMPONENT",component=name)
    if prov not in _ALLOWED_PROVENANCE: return _d("BLOCKED","INVALID_COST_PROVENANCE",component=name)
    if not isinstance(ref,str) or not ref.strip(): return _d("BLOCKED","MISSING_COST_PROVENANCE",component=name)
    if unit!=UNIT: return _d("BLOCKED","COST_UNIT_MISMATCH",component=name)
    lo,hi=c.get("lower_cost"),c.get("upper_cost")
    if not _finite(lo) or not _finite(hi): return _d("BLOCKED","INVALID_COST_BOUND",component=name)
    lo,hi=float(lo),float(hi)
    if lo>hi: return _d("BLOCKED","INVALID_COST_BOUND",component=name)
    if name in NONNEGATIVE_COMPONENTS and (lo<0 or hi<0): return _d("BLOCKED","NEGATIVE_NONNEGATIVE_COST_COMPONENT",component=name)
    if state=="EXACT" and lo!=hi: return _d("BLOCKED","EXACT_COST_NOT_EXACT",component=name)
    if state=="NOT_APPLICABLE_WITH_EVIDENCE":
        if prov!="NOT_APPLICABLE_EVIDENCE": return _d("BLOCKED","NOT_APPLICABLE_PROVENANCE_MISMATCH",component=name)
        if lo!=0 or hi!=0: return _d("BLOCKED","NOT_APPLICABLE_NONZERO_COST",component=name)
    if prov=="ESTIMATED_WITH_BOUND" and state!="BOUNDED": return _d("BLOCKED","ESTIMATE_REQUIRES_BOUND",component=name)
    return _d("PASS",component=name,conservative_cost=hi)
def validate_cost_profile(p):
    if not isinstance(p,dict): return _d("BLOCKED","INVALID_COST_PROFILE")
    r=_scope(p.get("scope"))
    if r["status"]!="PASS": return r
    if p.get("material_cost_inventory_complete") is not True: return _d("BLOCKED","INCOMPLETE_MATERIAL_COST_INVENTORY")
    cs=p.get("components")
    if not isinstance(cs,dict): return _d("BLOCKED","MISSING_REQUIRED_COST_COMPONENT")
    if "spread" in cs: return _d("BLOCKED","SPREAD_DOUBLE_COUNT_FORBIDDEN")
    res={}
    for n in REQUIRED_COMPONENTS:
        if n not in cs: return _d("BLOCKED","MISSING_REQUIRED_COST_COMPONENT",component=n)
        rr=_component(n,cs[n])
        if rr["status"]!="PASS": return rr
        res[n]=rr
    for i,item in enumerate(p.get("other_material_components",[])):
        if not isinstance(item,dict) or not isinstance(item.get("name"),str) or not item["name"].strip(): return _d("BLOCKED","INVALID_OTHER_COMPONENT",index=i)
        n=item["name"]
        if n.strip().lower()=="spread": return _d("BLOCKED","SPREAD_DOUBLE_COUNT_FORBIDDEN")
        rr=_component(n,item)
        if rr["status"]!="PASS": return rr
        res[n]=rr
    return _d("READY_FOR_CC05_COST_APPLICATION",conservative_component_costs={k:v["conservative_cost"] for k,v in res.items()},claim_scope="MOMENTUM_V1/USTECH/H1/CC05")
def apply_conservative_all_in_cost(*,raw_bid_ask_realized_unit_pnl,profile):
    if not _finite(raw_bid_ask_realized_unit_pnl): return _d("BLOCKED","INVALID_RAW_REALIZED_UNIT_PNL")
    v=validate_cost_profile(profile)
    if v["status"]!="READY_FOR_CC05_COST_APPLICATION": return v
    total=sum(v["conservative_component_costs"].values())
    return _d("COST_APPLIED",raw_bid_ask_realized_unit_pnl=float(raw_bid_ask_realized_unit_pnl),conservative_total_cost=total,conservative_all_in_net_realized_unit_pnl=float(raw_bid_ask_realized_unit_pnl)-total,unit=UNIT,authority=dict(AUTHORITY))
