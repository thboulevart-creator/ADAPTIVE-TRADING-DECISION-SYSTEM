from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.bepd_04e_response_generalization_v0_1 import aggregate_week_counts,moving_block_ratio_ci,assert_calendar_binding,guard_request
results=[]
def case(cid,fn):
    try: fn()
    except Exception:
        results.append((cid,"HARD_FAIL")); return
    raise AssertionError(f"{cid}:EXPECTED_HARD_FAIL")
cal=["2026-01-05","2026-01-12","2026-01-19"]
events=[{"event_id":"e1","target_week_id":"2026-01-05","sweep_cluster_id":"c1","same_week_reintegration":True},{"event_id":"e2","target_week_id":"2026-01-19","sweep_cluster_id":"c3","same_week_reintegration":False}]
base={"analysis_surface":"GLOBAL_RESPONSE_GENERALIZATION_ONLY","method":"MOVING_BLOCK_RATIO_OF_SUMS","response_subgroup":None,"occurrence_x_response":False,"time_to_reintegration":False,"occurrence_m05_reused":False,"response_m05_activation_state":"NOT_ACTIVATED","trading_authority":"NONE"}
case("B01_WRONG_CALENDAR_IDENTITY",lambda:assert_calendar_binding("wrong","expected"))
case("B02_UNSORTED_CALENDAR",lambda:aggregate_week_counts(["2026-01-12","2026-01-05"],events))
case("B03_DUPLICATE_TARGET_WEEK",lambda:aggregate_week_counts(["2026-01-05","2026-01-05"],events[:1]))
case("B04_CALENDAR_GAP_REMOVED",lambda:aggregate_week_counts(["2026-01-05","2026-01-19"],events))
case("B05_ZERO_EVENT_WEEK_REMOVED",lambda:aggregate_week_counts(["2026-01-05","2026-01-19"],events))
case("B06_EVENT_OUTSIDE_CALENDAR",lambda:aggregate_week_counts(["2026-01-05"],[events[1]]))
case("B07_TARGET_WEEK_CLUSTER_SPLIT",lambda:aggregate_week_counts(["2026-01-05"],[{"event_id":"a","target_week_id":"2026-01-05","sweep_cluster_id":"x","same_week_reintegration":True},{"event_id":"b","target_week_id":"2026-01-05","sweep_cluster_id":"y","same_week_reintegration":False}]))
case("B08_SWEEP_CLUSTER_SPLIT",lambda:aggregate_week_counts(["2026-01-05","2026-01-12"],[{"event_id":"a","target_week_id":"2026-01-05","sweep_cluster_id":"x","same_week_reintegration":True},{"event_id":"b","target_week_id":"2026-01-12","sweep_cluster_id":"x","same_week_reintegration":False}]))
case("B09_INDIVIDUAL_EVENT_IID_BOOTSTRAP",lambda:guard_request({**base,"method":"IID_EVENT_BOOTSTRAP"}))
case("B10_NAIVE_BINOMIAL_CI",lambda:guard_request({**base,"method":"NAIVE_BINOMIAL_CI"}))
case("B11_IMPLICIT_BLOCK_LENGTH",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",replications=20,seed=1,confidence_level=.95,interval_method="PERCENTILE"))
case("B12_IMPLICIT_CONFIDENCE_LEVEL",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",block_length=1,replications=20,seed=1,interval_method="PERCENTILE"))
case("B13_IMPLICIT_INTERVAL_METHOD",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",block_length=1,replications=20,seed=1,confidence_level=.95))
case("B14_IMPLICIT_REPLICATION_COUNT",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",block_length=1,seed=1,confidence_level=.95,interval_method="PERCENTILE"))
case("B15_IMPLICIT_SEED",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",block_length=1,replications=20,confidence_level=.95,interval_method="PERCENTILE"))
case("B16_UNSUPPORTED_INTERVAL",lambda:moving_block_ratio_ci(cal,events,execution_scope="SYNTHETIC_QUALIFICATION",block_length=1,replications=20,seed=1,confidence_level=.95,interval_method="BCA"))
case("B17_POST_RESULT_PARAMETER_SELECTION",lambda:guard_request({**base,"analysis_surface":"POST_RESULT_PARAMETER_SELECTION"}))
case("B18_REAL_RESPONSE_UNDER_SYNTHETIC_QUALIFICATION",lambda:moving_block_ratio_ci(cal,events,execution_scope="REAL_AUTHORIZED",block_length=1,replications=20,seed=1,confidence_level=.95,interval_method="PERCENTILE"))
case("B19_REAL_GATE_WITHOUT_AUTHORITY",lambda:guard_request({**base,"analysis_surface":"REAL_NONSTATIONARITY_GATE"}))
case("B20_REAL_BOOTSTRAP_WITHOUT_AUTHORITY",lambda:moving_block_ratio_ci(cal,events,execution_scope="REAL_AUTHORIZED",block_length=1,replications=20,seed=1,confidence_level=.95,interval_method="PERCENTILE",real_execution_authorized=False))
case("B21_RESPONSE_SUBGROUP",lambda:guard_request({**base,"response_subgroup":"HIGH"}))
case("B22_OCCURRENCE_X_RESPONSE",lambda:guard_request({**base,"occurrence_x_response":True}))
case("B23_TIME_TO_REINTEGRATION",lambda:guard_request({**base,"time_to_reintegration":True}))
case("B24_OCCURRENCE_M05_REUSE",lambda:guard_request({**base,"occurrence_m05_reused":True}))
case("B25_RESPONSE_M05_ACTIVATED",lambda:guard_request({**base,"response_m05_activation_state":"ACTIVATED"}))
case("B26_TRADING_AUTHORITY",lambda:guard_request({**base,"trading_authority":"LIVE"}))
if len(results)!=26: raise AssertionError(f"BREAKER_COUNT:{len(results)}")
for cid,status in results: print(f"{cid}={status}")
print("BEPD04E_EXECUTABLE_BREAKER_PASS")
