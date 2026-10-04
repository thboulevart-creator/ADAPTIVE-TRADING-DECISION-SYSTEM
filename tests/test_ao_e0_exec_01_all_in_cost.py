from __future__ import annotations
import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]; s=importlib.util.spec_from_file_location("ao",R/"tools"/"ao_e0_exec_01_all_in_cost.py"); ao=importlib.util.module_from_spec(s); s.loader.exec_module(ao)
def c(state="EXACT",kind="CONTRACTUAL",lo=.1,hi=.1): return {"state":state,"provenance_kind":kind,"source_ref":"ref://x","lower_cost":lo,"upper_cost":hi,"unit":"PRICE_UNITS_PER_UNIT_POSITION"}
def p(): return {"scope":{"strategy_id":"MOMENTUM_V1","instrument":"USTECH","timeframe":"H1","base_execution_contract":"ATDS_E1_04_EXECUTION_COST_MODEL_V0_1","execution_venue_identity":"V","account_cost_profile_identity":"A","symbol_contract_identity":"S","cost_schedule_effective_from_utc":"2025-05-25T00:00:00Z","cost_schedule_effective_to_utc":"2026-05-24T23:59:59.963Z","cost_profile_source_ref":"ref://p","unit_conversion_identity_or_NOT_REQUIRED_WITH_BASIS":"NOT_REQUIRED_SAME_UNIT"},"material_cost_inventory_complete":True,"components":{"commission":c(),"slippage":c("BOUNDED","ESTIMATED_WITH_BOUND",0,.3),"financing":{"state":"NOT_APPLICABLE_WITH_EVIDENCE","provenance_kind":"NOT_APPLICABLE_EVIDENCE","source_ref":"ref://na","lower_cost":0.0,"upper_cost":0.0,"unit":"PRICE_UNITS_PER_UNIT_POSITION"}},"other_material_components":[]}
def test_valid(): assert ao.validate_cost_profile(p())["status"]=="READY_FOR_CC05_COST_APPLICATION"
def test_unknown(): q=p();q["components"]["slippage"]["state"]="UNKNOWN";assert ao.validate_cost_profile(q)["status"]=="BLOCKED"
def test_scope(): q=p();q["scope"]["symbol_contract_identity"]="";assert ao.validate_cost_profile(q)["status"]=="BLOCKED"
def test_inventory(): q=p();q["material_cost_inventory_complete"]=False;assert ao.validate_cost_profile(q)["status"]=="BLOCKED"
def test_upper(): assert abs(ao.apply_conservative_all_in_cost(raw_bid_ask_realized_unit_pnl=2,profile=p())["conservative_all_in_net_realized_unit_pnl"]-1.6)<1e-12
def test_authority(): assert ao.AUTHORITY["oos_consumption_authorized"] is False
def test_window(): q=p();q["scope"]["cost_schedule_effective_to_utc"]="2026-01-01T00:00:00Z";assert ao.validate_cost_profile(q)["reason"]=="COST_SCHEDULE_DOES_NOT_COVER_OOS"
def test_spread(): q=p();q["components"]["spread"]=c();assert ao.validate_cost_profile(q)["reason"]=="SPREAD_DOUBLE_COUNT_FORBIDDEN"
