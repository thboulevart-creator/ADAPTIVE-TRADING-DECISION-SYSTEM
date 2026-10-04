from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/"tools"/"ao_e0_exec_01_all_in_cost.py"
CONTRACT=ROOT/"GOVERNANCE"/"AO-E0-EXEC-01-E1-SCOPED-ALL-IN-COST-CONTRACT-V0.1.json"
def load():
    if not TARGET.exists(): raise AssertionError("EXPECTED_TARGET_MISSING")
    s=importlib.util.spec_from_file_location("ao",TARGET); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
def exact(): return {"state":"EXACT","provenance_kind":"CONTRACTUAL","source_ref":"ref://c","lower_cost":0.2,"upper_cost":0.2,"unit":"PRICE_UNITS_PER_UNIT_POSITION"}
def p():
    return {"scope":{"strategy_id":"MOMENTUM_V1","instrument":"USTECH","timeframe":"H1","base_execution_contract":"ATDS_E1_04_EXECUTION_COST_MODEL_V0_1","execution_venue_identity":"V","account_cost_profile_identity":"A","symbol_contract_identity":"S","cost_schedule_effective_from_utc":"2025-05-25T00:00:00Z","cost_schedule_effective_to_utc":"2026-05-24T23:59:59.963Z","cost_profile_source_ref":"ref://p","unit_conversion_identity_or_NOT_REQUIRED_WITH_BASIS":"NOT_REQUIRED_SAME_UNIT"},"material_cost_inventory_complete":True,"components":{"commission":exact(),"slippage":{"state":"BOUNDED","provenance_kind":"ESTIMATED_WITH_BOUND","source_ref":"ref://s","lower_cost":0.0,"upper_cost":0.4,"unit":"PRICE_UNITS_PER_UNIT_POSITION"},"financing":{"state":"NOT_APPLICABLE_WITH_EVIDENCE","provenance_kind":"NOT_APPLICABLE_EVIDENCE","source_ref":"ref://f","lower_cost":0.0,"upper_cost":0.0,"unit":"PRICE_UNITS_PER_UNIT_POSITION"}},"other_material_components":[]}
def block(m,q,reason):
    r=m.validate_cost_profile(q); assert r["status"]=="BLOCKED" and r["reason"]==reason,r
def run():
    c=json.loads(CONTRACT.read_text(encoding="utf-8")); assert c["authority"]["oos_consumption_authorized"] is False
    m=load(); q=p(); assert m.validate_cost_profile(q)["status"]=="READY_FOR_CC05_COST_APPLICATION"
    x=p(); x["components"].pop("commission"); block(m,x,"MISSING_REQUIRED_COST_COMPONENT")
    x=p(); x["components"]["slippage"]["state"]="UNKNOWN"; block(m,x,"UNKNOWN_COST_COMPONENT")
    x=p(); x["components"]["slippage"]["upper_cost"]=None; block(m,x,"INVALID_COST_BOUND")
    x=p(); x["components"]["commission"]["source_ref"]=""; block(m,x,"MISSING_COST_PROVENANCE")
    x=p(); x["components"]["commission"]["lower_cost"]=-.1; block(m,x,"NEGATIVE_NONNEGATIVE_COST_COMPONENT")
    x=p(); x["scope"]["account_cost_profile_identity"]=""; block(m,x,"MISSING_SCOPE_BINDING")
    x=p(); x["material_cost_inventory_complete"]=False; block(m,x,"INCOMPLETE_MATERIAL_COST_INVENTORY")
    x=p(); x["components"]["commission"]["unit"]="USD"; block(m,x,"COST_UNIT_MISMATCH")
    x=p(); x["scope"]["cost_schedule_effective_from_utc"]="2025-06-01T00:00:00Z"; block(m,x,"COST_SCHEDULE_DOES_NOT_COVER_OOS")
    x=p(); x["components"]["spread"]=exact(); block(m,x,"SPREAD_DOUBLE_COUNT_FORBIDDEN")
    r=m.apply_conservative_all_in_cost(raw_bid_ask_realized_unit_pnl=3.0,profile=q); assert math.isclose(r["conservative_all_in_net_realized_unit_pnl"],2.4)
    x=p(); x["components"]["financing"]={"state":"BOUNDED","provenance_kind":"CONTRACTUAL","source_ref":"ref://credit","lower_cost":-.2,"upper_cost":-.1,"unit":"PRICE_UNITS_PER_UNIT_POSITION"}
    r=m.apply_conservative_all_in_cost(raw_bid_ask_realized_unit_pnl=3.0,profile=x); assert math.isclose(r["conservative_total_cost"],.5)
    assert m.AUTHORITY["oos_consumption_authorized"] is False and m.AUTHORITY["strategy_qualification_authorized"] is False
    print("AO_E0_EXEC_01_BREAKER_PASS")
if __name__=="__main__": run()
