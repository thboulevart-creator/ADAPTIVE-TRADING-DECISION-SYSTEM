from __future__ import annotations
import copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.bepd_04i_real_m05_bootstrap_v0_1 import guard_bindings,guard_config,EXPECTED_BINDINGS
results=[]
def hard(cid,fn):
    try: fn()
    except Exception:
        results.append((cid,"HARD_FAIL")); return
    raise AssertionError(f"{cid}:EXPECTED_HARD_FAIL")
base={
 "method":"M05","scheme":"MOVING_BLOCK","statistic":"RATIO_OF_SUMS",
 "replications":200000,"block_length":13,"seed":40420261006,
 "confidence_level":0.99,"interval_method":"PERCENTILE","execution_scope":"EXPLORATORY_ONLY",
 "response_subgroup":None,"sensitivity_analysis":False,"alternative_response":False,
 "alternative_horizon":False,"occurrence_x_response":False,"time_to_reintegration":False,
 "prediction_claim":False,"edge_claim":False,"strategy_claim":False,"trading_authority":"NONE",
 "post_result_parameter_selection":False,"competing_canonical_execution":False,
}
for i,k in enumerate(EXPECTED_BINDINGS,1):
    bad=dict(EXPECTED_BINDINGS); bad[k]="wrong"
    hard(f"B{i:02d}_WRONG_BINDING_{k}",lambda bad=bad:guard_bindings(bad))
start=len(EXPECTED_BINDINGS)+1
mods=[
 ("BLOCK_LENGTH",{"block_length":12}),("CONFIDENCE",{"confidence_level":0.95}),
 ("INTERVAL",{"interval_method":"BASIC"}),("REPLICATIONS",{"replications":1000}),
 ("SEED",{"seed":1}),("METHOD",{"method":"IID"}),("SCHEME",{"scheme":"IID_EVENT"}),
 ("STATISTIC",{"statistic":"MEAN_OF_WEEKLY_MEANS"}),("SCOPE",{"execution_scope":"CONFIRMATORY"}),
 ("SUBGROUP",{"response_subgroup":"HIGH"}),("SENSITIVITY",{"sensitivity_analysis":True}),
 ("ALT_RESPONSE",{"alternative_response":True}),("ALT_HORIZON",{"alternative_horizon":True}),
 ("OCC_X_RESP",{"occurrence_x_response":True}),("TIME_TO_REINT",{"time_to_reintegration":True}),
 ("PREDICTION",{"prediction_claim":True}),("EDGE",{"edge_claim":True}),
 ("STRATEGY",{"strategy_claim":True}),("TRADING",{"trading_authority":"LIVE"}),
 ("POST_RESULT",{"post_result_parameter_selection":True}),("SECOND_CANONICAL",{"competing_canonical_execution":True}),
]
for j,(name,patch) in enumerate(mods,start):
    x=copy.deepcopy(base); x.update(patch)
    hard(f"B{j:02d}_{name}",lambda x=x:guard_config(x))
guard_bindings(EXPECTED_BINDINGS); guard_config(base)
print(f"BEPD04I_BREAKER_PASS:{len(results)}/{len(results)} HARD_FAIL")
