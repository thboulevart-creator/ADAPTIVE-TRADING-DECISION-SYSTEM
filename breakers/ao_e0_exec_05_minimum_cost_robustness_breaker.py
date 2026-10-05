from __future__ import annotations
import json, importlib.util
from pathlib import Path

R=Path(__file__).resolve().parents[1]
P=R/"GOVERNANCE"/"AO-E0-EXEC-05-PRE-OOS-MINIMUM-COST-ROBUSTNESS-REQUIREMENT-V0.1.json"
T=R/"tools"/"ao_e0_exec_05_minimum_cost_robustness.py"

def load():
    s=importlib.util.spec_from_file_location("m",T)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def run():
    p=json.loads(P.read_text())
    assert p["status"]=="CANDIDATE_NOT_HUMAN_ADOPTED"
    assert p["minimum_required_node"]["node_id"]=="F2_S4"
    assert p["minimum_required_node"]["financing_multiplier"]==2
    assert p["minimum_required_node"]["slippage_bps_per_execution_event"]==4
    assert p["gate_semantics"]["all_28_nodes_reported"] is True
    assert p["gate_semantics"]["post_result_threshold_change"]=="FORBIDDEN"
    assert p["pending"]["b4_numeric_delta_min"].startswith("PENDING")
    assert p["authority"]["oos_consumption_authorized"] is False
    assert p["authority"]["real_performance_observation_authorized"] is False
    m=load()
    assert m.required_node()==("F2_S4",2.0,4.0)
    assert m.evaluate("SUPPORTED")=="PASS"
    assert m.evaluate("REFUTED")=="FAIL"
    assert m.evaluate("INCONCLUSIVE")=="INCONCLUSIVE"
    try:
        m.evaluate("UNKNOWN")
    except ValueError:
        pass
    else:
        raise AssertionError("UNKNOWN_MUST_NOT_AUTO_MAP")
    print("AO_E0_EXEC_05_BREAKER_PASS")

if __name__=="__main__":
    run()
