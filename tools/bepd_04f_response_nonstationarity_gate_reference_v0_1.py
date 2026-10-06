from __future__ import annotations
from decimal import Decimal

STRATA=[
 {"id":"T1","start":"2021-06-07","end":"2022-05-30"},
 {"id":"T2","start":"2022-06-06","end":"2023-05-29"},
 {"id":"T3","start":"2023-06-05","end":"2024-05-27"},
 {"id":"T4","start":"2024-06-03","end":"2025-05-26"},
 {"id":"T5","start":"2025-06-02","end":"2026-05-18"},
]

def reference_evaluate_gate(req):
    if req["calendar_binding_blob"]!="26385eb2547892df4b87206ad59fc2ba07721354": raise ValueError("CALENDAR_IDENTITY_MISMATCH")
    if req["complete_target_week_count"]!=259: raise ValueError("TARGET_WEEK_COUNT_MISMATCH")
    if req["first_target_week_id"]!="2021-06-07" or req["last_target_week_id"]!="2026-05-18": raise ValueError("CALENDAR_BOUNDARY_MISMATCH")
    if req["zero_event_week_count"]!=29: raise ValueError("ZERO_EVENT_WEEK_COUNT_MISMATCH")
    if req["calendar_spacing_days"]!=7: raise ValueError("CALENDAR_SPACING_MISMATCH")
    if req["calendar_order"]!="STRICT_ASCENDING_WEEKLY": raise ValueError("CALENDAR_ORDER_INVALID")
    if req["target_week_cluster_integrity"] is not True: raise ValueError("TARGET_WEEK_CLUSTER_INTEGRITY_FAIL")
    if req["sweep_cluster_integrity"] is not True: raise ValueError("SWEEP_CLUSTER_INTEGRITY_FAIL")
    if req["m04_status"]!="NOT_APPLICABLE_BY_REPRESENTATION": raise ValueError("M04_STATUS_INVALID")
    if req["m10_minimum_n"]!=30: raise ValueError("M10_MINIMUM_N_MISMATCH")
    if str(req["m10_maximum_spread"])!="0.10": raise ValueError("M10_THRESHOLD_MISMATCH")
    if req["declared_strata"]!=STRATA: raise ValueError("DECLARED_STRATA_MISMATCH")
    if req["execution_scope"]!="SYNTHETIC_QUALIFICATION" or req["real_response_input"] is not False: raise ValueError("REAL_EXECUTION_NOT_AUTHORIZED")
    if req["m05_activation_state"]!="NOT_ACTIVATED": raise ValueError("M05_ACTIVATION_NOT_AUTHORIZED")
    stats=req["stratum_stats"]
    ids=[x["id"] for x in stats]
    if ids!=[x["id"] for x in STRATA]: raise ValueError("STRATUM_STATS_MISMATCH")
    ns={x["id"]:x["n"] for x in stats}
    means=[Decimal(str(x["response_mean"])) for x in stats]
    insufficient=[x["id"] for x in stats if x["n"]<30]
    spread=max(means)-min(means)
    if insufficient:
        return {"state":"NONSTATIONARITY_UNRESOLVED","reason_code":"M10_INSUFFICIENT_SAMPLE","structural_validation_status":"PASS","sample_adequacy":"INSUFFICIENT","stratum_n":ns,"insufficient_strata":insufficient,"maximum_spread":format(spread,"f"),"spread_classification":"NOT_DECISION_CONTROLLING","m04_status":"NOT_APPLICABLE_BY_REPRESENTATION","m04_executed":False}
    if spread>Decimal("0.10"):
        return {"state":"NONSTATIONARITY_MATERIALLY_DETECTED","reason_code":"M10_SPREAD_EXCEEDS_ADOPTED_THRESHOLD","structural_validation_status":"PASS","sample_adequacy":"PASS","stratum_n":ns,"insufficient_strata":[],"maximum_spread":format(spread,"f"),"spread_classification":"ABOVE_ADOPTED_TOLERANCE","m04_status":"NOT_APPLICABLE_BY_REPRESENTATION","m04_executed":False}
    return {"state":"NONSTATIONARITY_NOT_MATERIALLY_DETECTED","reason_code":"M10_WITHIN_ADOPTED_TOLERANCE","structural_validation_status":"PASS","sample_adequacy":"PASS","stratum_n":ns,"insufficient_strata":[],"maximum_spread":format(spread,"f"),"spread_classification":"WITHIN_ADOPTED_TOLERANCE","m04_status":"NOT_APPLICABLE_BY_REPRESENTATION","m04_executed":False}
