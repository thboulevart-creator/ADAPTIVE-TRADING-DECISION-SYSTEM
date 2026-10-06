from __future__ import annotations
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.bepd_04f_response_nonstationarity_gate_v0_1 import evaluate_gate,assert_upstream_bindings,EXPECTED_UPSTREAM
FIX=json.loads((ROOT/"tests/fixtures/bepd_04f_response_nonstationarity_gate_synthetic_v0_1.json").read_text())
BASE=FIX["base_request"]
results=[]

def hard(cid,fn):
    try: fn()
    except Exception:
        results.append((cid,"HARD_FAIL")); return
    raise AssertionError(f"{cid}:EXPECTED_HARD_FAIL")

def patch(**kwargs):
    x=copy.deepcopy(BASE); x.update(kwargs); return x

bad_up=dict(EXPECTED_UPSTREAM); bad_up["bepd04d_claim_blob"]="wrong"
hard("B01_WRONG_UPSTREAM_IDENTITY",lambda:assert_upstream_bindings(bad_up))
bad_h=dict(EXPECTED_UPSTREAM); bad_h["bepd04e_human_adjudication_blob"]="wrong"
hard("B02_WRONG_HUMAN_ADJUDICATION",lambda:assert_upstream_bindings(bad_h))
bad_g=dict(EXPECTED_UPSTREAM); bad_g["bepd04d_old_gate_blob"]="mutated"
hard("B03_OLD_GATE_MUTATION",lambda:assert_upstream_bindings(bad_g))
hard("B04_CALENDAR_IDENTITY",lambda:evaluate_gate(patch(calendar_binding_blob="wrong")))
hard("B05_WEEK_COUNT",lambda:evaluate_gate(patch(complete_target_week_count=258)))
hard("B06_ZERO_WEEK_REMOVAL",lambda:evaluate_gate(patch(zero_event_week_count=28)))
hard("B07_CALENDAR_COMPRESSION",lambda:evaluate_gate(patch(calendar_spacing_days=14)))
hard("B08_M04_WORKAROUND",lambda:evaluate_gate(patch(m04_workaround="DROP_ZERO_EVENT_WEEKS")))
hard("B09_M04_PASS_LAUNDERING",lambda:evaluate_gate(patch(m04_status="PASS")))
hard("B10_M04_FAIL_LAUNDERING",lambda:evaluate_gate(patch(m04_status="FAIL")))
hard("B11_M04_UNKNOWN",lambda:evaluate_gate(patch(m04_status="UNKNOWN")))
x=copy.deepcopy(BASE); x.pop("m04_status")
hard("B12_M04_MISSING",lambda:evaluate_gate(x))
hard("B13_M10_THRESHOLD_CHANGED",lambda:evaluate_gate(patch(m10_maximum_spread="0.11")))
hard("B14_MINIMUM_N_CHANGED",lambda:evaluate_gate(patch(m10_minimum_n=29)))
hard("B15_TEMPORAL_STRATA_CHANGED",lambda:evaluate_gate(patch(declared_strata=BASE["declared_strata"][:-1])))
hard("B16_POST_RESULT_THRESHOLD_SELECTION",lambda:evaluate_gate(patch(post_result_parameter_selection=True)))
hard("B17_REAL_RESPONSE_DIAGNOSTIC",lambda:evaluate_gate(patch(execution_scope="REAL_AUTHORIZED",real_response_input=True)))
hard("B18_REAL_M10_WITHOUT_AUTHORITY",lambda:evaluate_gate(patch(execution_scope="REAL_AUTHORIZED")))
hard("B19_REAL_GATE_WITHOUT_AUTHORITY",lambda:evaluate_gate(patch(execution_scope="REAL_GATE")))
hard("B20_M05_ACTIVATION",lambda:evaluate_gate(patch(m05_activation_state="ACTIVATED")))
hard("B21_REAL_BOOTSTRAP",lambda:evaluate_gate(patch(real_bootstrap=True)))
hard("B22_REAL_CONFIDENCE_INTERVAL",lambda:evaluate_gate(patch(real_confidence_interval=True)))
hard("B23_SUBGROUP",lambda:evaluate_gate(patch(response_subgroup="HIGH")))
hard("B24_ALTERNATIVE_RESPONSE",lambda:evaluate_gate(patch(alternative_response=True)))
hard("B25_ALTERNATIVE_HORIZON",lambda:evaluate_gate(patch(alternative_horizon=True)))
hard("B26_OCCURRENCE_X_RESPONSE",lambda:evaluate_gate(patch(occurrence_x_response=True)))
hard("B27_TIME_TO_REINTEGRATION",lambda:evaluate_gate(patch(time_to_reintegration=True)))
hard("B28_PREDICTION",lambda:evaluate_gate(patch(prediction_claim=True)))
hard("B29_EDGE",lambda:evaluate_gate(patch(edge_claim=True)))
hard("B30_TRADING_AUTHORITY",lambda:evaluate_gate(patch(trading_authority="LIVE")))
hard("B31_TARGET_WEEK_CLUSTER",lambda:evaluate_gate(patch(target_week_cluster_integrity=False)))
hard("B32_SWEEP_CLUSTER",lambda:evaluate_gate(patch(sweep_cluster_integrity=False)))
if len(results)!=32: raise AssertionError(f"BREAKER_COUNT:{len(results)}")
for cid,status in results: print(f"{cid}={status}")
print("BEPD04F_EXECUTABLE_BREAKER_PASS")
