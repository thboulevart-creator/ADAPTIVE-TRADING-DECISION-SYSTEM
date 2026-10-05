from __future__ import annotations
import importlib.util, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/"GOVERNANCE"/"AO-E0-EXEC-04-PRE-RESULT-CONSERVATIVE-COST-STRESS-POLICY-V0.1.json"
TARGET=ROOT/"tools"/"ao_e0_exec_04_cost_stress.py"

def load():
    spec=importlib.util.spec_from_file_location("stress",TARGET)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def run():
    p=json.loads(POLICY.read_text(encoding="utf-8"))
    assert p["status"]=="CANDIDATE_NOT_HUMAN_ADOPTED"
    assert p["authority"]["oos_consumption_authorized"] is False
    assert p["authority"]["performance_observation_authorized"] is False
    assert p["authority"]["policy_human_adopted"] is False
    assert p["epistemic_firewall"]["POLICY_BOUND_NE_OBSERVED_COST"] is True
    assert p["stress_surface"]["all_nodes_must_be_reported"] is True
    assert p["stress_surface"]["post_result_node_selection_forbidden"] is True
    assert p["decision_semantics"]["final_minimum_robustness_requirement"].startswith("PENDING")
    assert p["financing_policy"]["stress_multiplier_grid"]==[0.0,1.0,2.0,4.0]
    assert p["slippage_policy"]["stress_bps_grid"]==[0.0,0.5,1.0,2.0,4.0,8.0,16.0]
    m=load()
    assert len(m.STRESS_NODES)==28
    assert m.FINANCING_MULTIPLIERS==sorted(m.FINANCING_MULTIPLIERS)
    assert m.SLIPPAGE_BPS==sorted(m.SLIPPAGE_BPS)
    vals=[m.adverse_slippage_cost(reference_price=20000.0,bps=x) for x in m.SLIPPAGE_BPS]
    assert vals==sorted(vals)
    assert vals[0]==0.0 and math.isclose(vals[-1],32.0)
    for mult in m.FINANCING_MULTIPLIERS:
        a=m.rollover_policy_cost(direction="LONG",weekday="monday",stress_multiplier=mult)
        b=m.rollover_policy_cost(direction="SHORT",weekday="monday",stress_multiplier=mult)
        assert math.isclose(a,b) and a>=0
    assert math.isclose(m.rollover_policy_cost(direction="LONG",weekday="friday",stress_multiplier=1.0),19.0995)
    assert math.isclose(m.execution_event_slippage_cost(reference_prices=[20000.0,20000.0],bps=1.0),4.0)
    s=m.policy_surface()
    assert len(s)==28
    assert all("selected" not in n for n in s)
    assert m.AUTHORITY["oos_consumption_authorized"] is False
    assert m.AUTHORITY["performance_observation_authorized"] is False
    print("AO_E0_EXEC_04_BREAKER_PASS")
if __name__=="__main__":
    run()
