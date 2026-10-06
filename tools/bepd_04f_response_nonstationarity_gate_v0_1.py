from __future__ import annotations
from decimal import Decimal, InvalidOperation

EXPECTED_UPSTREAM = {
    "bepd04e_human_adjudication_blob":"a92da70e6efec49729b275d806a76f0244e79bdd",
    "bepd04e_qualification_report_blob":"a4d8aefe4b49efaddadc857bbe11d81415c2a6ad",
    "bepd04e_qualification_receipt_blob":"10cc28e4c042f2af4ff5adfa995dcb64a228f3e8",
    "bepd04e_material_parameter_packet_blob":"e88900779eab989e5bfa3265d217485023dab4bb",
    "bepd04e_m05_candidate_blob":"b740312275bff3d6910c2e0fd1a69a24d96df1cb",
    "bepd04e_complete_week_calendar_blob":"26385eb2547892df4b87206ad59fc2ba07721354",
    "bepd04e_runtime_blob":"61a996562fe18e0e2efd6f16db27a48738e60421",
    "bepd04e_breaker_blob":"eda63bf26230a2b48eb75bb655e64e766b66c1a3",
    "bepd04d_old_gate_blob":"fedb12d532f1e68ee9405d05931a2a0d22672983",
    "bepd04d_claim_blob":"1f3e2cd2366315ed4198249864abcc84db35a9db",
    "bepd04d_m09_blob":"726b1f93a75fb4a1fbccab4668a509d18c3f9d8e",
    "bepd04c_human_adjudication_blob":"6008e441d241dc185087208c6d9977501df52813",
}
EXPECTED_STRATA = [
    {"id":"T1","start":"2021-06-07","end":"2022-05-30"},
    {"id":"T2","start":"2022-06-06","end":"2023-05-29"},
    {"id":"T3","start":"2023-06-05","end":"2024-05-27"},
    {"id":"T4","start":"2024-06-03","end":"2025-05-26"},
    {"id":"T5","start":"2025-06-02","end":"2026-05-18"},
]
CALENDAR_BLOB="26385eb2547892df4b87206ad59fc2ba07721354"
M04_STATUS="NOT_APPLICABLE_BY_REPRESENTATION"
MIN_N=30
MAX_SPREAD=Decimal("0.10")

def assert_upstream_bindings(bindings):
    if not isinstance(bindings,dict):
        raise ValueError("UPSTREAM_BINDINGS_REQUIRED")
    for k,v in EXPECTED_UPSTREAM.items():
        if bindings.get(k)!=v:
            if k=="bepd04e_human_adjudication_blob":
                raise ValueError("HUMAN_ADJUDICATION_IDENTITY_MISMATCH")
            if k=="bepd04d_old_gate_blob":
                raise ValueError("OLD_GATE_IDENTITY_MISMATCH")
            raise ValueError("UPSTREAM_IDENTITY_MISMATCH")
    return True

def _forbid_scope(req):
    if req.get("execution_scope")!="SYNTHETIC_QUALIFICATION" or req.get("real_response_input") is not False:
        raise ValueError("REAL_EXECUTION_NOT_AUTHORIZED")
    if req.get("m05_activation_state")!="NOT_ACTIVATED":
        raise ValueError("M05_ACTIVATION_NOT_AUTHORIZED")
    if req.get("real_bootstrap") is not False:
        raise ValueError("REAL_BOOTSTRAP_NOT_AUTHORIZED")
    if req.get("real_confidence_interval") is not False:
        raise ValueError("REAL_INTERVAL_NOT_AUTHORIZED")
    if req.get("response_subgroup") is not None:
        raise ValueError("RESPONSE_SUBGROUP_NOT_AUTHORIZED")
    if req.get("alternative_response") is not False:
        raise ValueError("ALTERNATIVE_RESPONSE_NOT_AUTHORIZED")
    if req.get("alternative_horizon") is not False:
        raise ValueError("ALTERNATIVE_HORIZON_NOT_AUTHORIZED")
    if req.get("occurrence_x_response") is not False:
        raise ValueError("OCCURRENCE_X_RESPONSE_NOT_AUTHORIZED")
    if req.get("time_to_reintegration") is not False:
        raise ValueError("TIME_TO_REINTEGRATION_NOT_AUTHORIZED")
    if req.get("prediction_claim") is not False:
        raise ValueError("PREDICTION_NOT_AUTHORIZED")
    if req.get("edge_claim") is not False:
        raise ValueError("EDGE_NOT_AUTHORIZED")
    if req.get("trading_authority")!="NONE":
        raise ValueError("TRADING_AUTHORITY_FORBIDDEN")
    if req.get("post_result_parameter_selection") is True:
        raise ValueError("POST_RESULT_PARAMETER_SELECTION_FORBIDDEN")
    if req.get("m04_workaround") not in (None,False):
        raise ValueError("M04_WORKAROUND_FORBIDDEN")

def _validate_structure(req):
    if req.get("calendar_binding_blob")!=CALENDAR_BLOB:
        raise ValueError("CALENDAR_IDENTITY_MISMATCH")
    if req.get("complete_target_week_count")!=259:
        raise ValueError("TARGET_WEEK_COUNT_MISMATCH")
    if req.get("first_target_week_id")!="2021-06-07" or req.get("last_target_week_id")!="2026-05-18":
        raise ValueError("CALENDAR_BOUNDARY_MISMATCH")
    if req.get("zero_event_week_count")!=29:
        raise ValueError("ZERO_EVENT_WEEK_COUNT_MISMATCH")
    if req.get("calendar_spacing_days")!=7:
        raise ValueError("CALENDAR_SPACING_MISMATCH")
    if req.get("calendar_order")!="STRICT_ASCENDING_WEEKLY":
        raise ValueError("CALENDAR_ORDER_INVALID")
    if req.get("target_week_cluster_integrity") is not True:
        raise ValueError("TARGET_WEEK_CLUSTER_INTEGRITY_FAIL")
    if req.get("sweep_cluster_integrity") is not True:
        raise ValueError("SWEEP_CLUSTER_INTEGRITY_FAIL")
    if req.get("moving_block_axis")!="COMPLETE_TARGET_WEEK_CALENDAR":
        raise ValueError("MOVING_BLOCK_AXIS_INVALID")
    if req.get("individual_event_iid_resampling") is not False:
        raise ValueError("IID_RESAMPLING_FORBIDDEN")
    if "m04_status" not in req:
        raise ValueError("M04_STATUS_REQUIRED")
    if req.get("m04_status")!=M04_STATUS:
        raise ValueError("M04_STATUS_INVALID")
    if req.get("m10_minimum_n")!=MIN_N:
        raise ValueError("M10_MINIMUM_N_MISMATCH")
    if str(req.get("m10_maximum_spread"))!="0.10":
        raise ValueError("M10_THRESHOLD_MISMATCH")
    if req.get("declared_strata")!=EXPECTED_STRATA:
        raise ValueError("DECLARED_STRATA_MISMATCH")

def _validate_stats(req):
    stats=req.get("stratum_stats")
    if not isinstance(stats,list):
        raise ValueError("STRATUM_STATS_REQUIRED")
    expected_ids=[x["id"] for x in EXPECTED_STRATA]
    ids=[x.get("id") for x in stats if isinstance(x,dict)]
    if ids!=expected_ids:
        raise ValueError("STRATUM_STATS_MISMATCH")
    parsed=[]
    for x in stats:
        n=x.get("n")
        if isinstance(n,bool) or not isinstance(n,int) or n<0:
            raise ValueError("STRATUM_N_INVALID")
        try:
            m=Decimal(str(x.get("response_mean")))
        except (InvalidOperation,TypeError):
            raise ValueError("RESPONSE_MEAN_INVALID")
        if m<0 or m>1:
            raise ValueError("RESPONSE_MEAN_INVALID")
        parsed.append((x["id"],n,m))
    return parsed

def evaluate_gate(req):
    if not isinstance(req,dict):
        raise ValueError("REQUEST_INVALID")
    _forbid_scope(req)
    _validate_structure(req)
    parsed=_validate_stats(req)
    ns={sid:n for sid,n,_ in parsed}
    means=[m for _,_,m in parsed]
    insufficient=[sid for sid,n,_ in parsed if n<MIN_N]
    spread=max(means)-min(means)
    if insufficient:
        state="NONSTATIONARITY_UNRESOLVED"
        reason="M10_INSUFFICIENT_SAMPLE"
        sample="INSUFFICIENT"
        spread_class="NOT_DECISION_CONTROLLING"
    elif spread>MAX_SPREAD:
        state="NONSTATIONARITY_MATERIALLY_DETECTED"
        reason="M10_SPREAD_EXCEEDS_ADOPTED_THRESHOLD"
        sample="PASS"
        spread_class="ABOVE_ADOPTED_TOLERANCE"
    else:
        state="NONSTATIONARITY_NOT_MATERIALLY_DETECTED"
        reason="M10_WITHIN_ADOPTED_TOLERANCE"
        sample="PASS"
        spread_class="WITHIN_ADOPTED_TOLERANCE"
    return {
        "state":state,
        "reason_code":reason,
        "structural_validation_status":"PASS",
        "sample_adequacy":sample,
        "stratum_n":ns,
        "insufficient_strata":insufficient,
        "maximum_spread":format(spread,"f"),
        "spread_classification":spread_class,
        "m04_status":M04_STATUS,
        "m04_executed":False,
        "stationarity_proven":False,
        "iid_proven":False,
        "generalization_proven":False,
        "m05_activation_state":"NOT_ACTIVATED",
    }
