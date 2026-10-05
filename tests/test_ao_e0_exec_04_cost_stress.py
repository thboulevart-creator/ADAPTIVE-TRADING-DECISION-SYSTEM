from __future__ import annotations
import importlib.util
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("m",R/"tools"/"ao_e0_exec_04_cost_stress.py")
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_grid_size(): assert len(m.policy_surface())==28
def test_no_authority(): assert m.AUTHORITY["oos_consumption_authorized"] is False
def test_slippage_zero(): assert m.adverse_slippage_cost(reference_price=10000,bps=0)==0
def test_slippage_one_bp(): assert m.adverse_slippage_cost(reference_price=10000,bps=1)==1
def test_financing_friday_triple(): assert abs(m.rollover_policy_cost(direction="SHORT",weekday="friday",stress_multiplier=2)-38.199)<1e-12
def test_direction_neutral_financing(): assert m.rollover_policy_cost(direction="LONG",weekday="monday",stress_multiplier=1)==m.rollover_policy_cost(direction="SHORT",weekday="monday",stress_multiplier=1)
def test_reversal_two_events(): assert m.execution_event_slippage_cost(reference_prices=[10000,10000],bps=1)==2
def test_epistemic_label(): assert all(n["epistemic_class"]=="POLICY_STRESS_NOT_OBSERVED_HISTORICAL_COST" for n in m.policy_surface())
