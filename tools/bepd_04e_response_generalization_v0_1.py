from __future__ import annotations
import math, random
from datetime import date

CONTRACT="ATDS_BEPD_04E_RESPONSE_GENERALIZATION_RUNTIME_V0_1"
INTERVAL_METHODS=("PERCENTILE","BASIC")

def _iso_week_date(value):
    if not isinstance(value,str):
        raise ValueError("INVALID_TARGET_WEEK")
    try:
        d=date.fromisoformat(value)
    except Exception as exc:
        raise ValueError("INVALID_TARGET_WEEK") from exc
    if d.weekday()!=0:
        raise ValueError("TARGET_WEEK_NOT_MONDAY")
    return d

def _validate_calendar(calendar):
    if not isinstance(calendar,(list,tuple)) or not calendar:
        raise ValueError("EMPTY_CALENDAR")
    seen=set(); out=[]; prev=None
    for w in calendar:
        d=_iso_week_date(w)
        if w in seen: raise ValueError("DUPLICATE_TARGET_WEEK")
        if prev is not None:
            delta=(d-prev).days
            if delta<0: raise ValueError("UNSORTED_TARGET_WEEK")
            if delta!=7: raise ValueError("CALENDAR_GAP")
        seen.add(w); out.append(w); prev=d
    return out

def _validate_events(events, calendar):
    if not isinstance(events,(list,tuple)):
        raise ValueError("EVENTS_INVALID")
    cal=set(calendar); ids=set(); cluster_week={}; week_cluster={}
    clean=[]
    for row in events:
        if not isinstance(row,dict): raise ValueError("EVENT_INVALID")
        for k in ("event_id","target_week_id","sweep_cluster_id","same_week_reintegration"):
            if k not in row: raise ValueError("EVENT_FIELD_MISSING")
        eid=row["event_id"]; w=row["target_week_id"]; cluster=row["sweep_cluster_id"]; y=row["same_week_reintegration"]
        if not isinstance(eid,str) or not eid: raise ValueError("EVENT_ID_INVALID")
        if eid in ids: raise ValueError("DUPLICATE_EVENT_ID")
        ids.add(eid)
        if w not in cal: raise ValueError("EVENT_WEEK_OUTSIDE_CALENDAR")
        if not isinstance(cluster,str) or not cluster: raise ValueError("SWEEP_CLUSTER_INVALID")
        if type(y) is not bool: raise ValueError("RESPONSE_NOT_BOOLEAN")
        if cluster in cluster_week and cluster_week[cluster]!=w: raise ValueError("SWEEP_CLUSTER_SPLIT")
        cluster_week[cluster]=w
        if w in week_cluster and week_cluster[w]!=cluster: raise ValueError("TARGET_WEEK_CLUSTER_SPLIT")
        week_cluster[w]=cluster
        clean.append({"event_id":eid,"target_week_id":w,"sweep_cluster_id":cluster,"same_week_reintegration":y})
    return clean

def aggregate_week_counts(calendar, events):
    cal=_validate_calendar(calendar)
    clean=_validate_events(events,cal)
    out={w:{"target_week_id":w,"success_count":0,"event_count":0} for w in cal}
    for e in clean:
        x=out[e["target_week_id"]]
        x["event_count"]+=1
        x["success_count"]+=int(e["same_week_reintegration"])
    return [out[w] for w in cal]

def ratio_of_sums(week_counts):
    s=sum(int(x["success_count"]) for x in week_counts)
    n=sum(int(x["event_count"]) for x in week_counts)
    if n<=0: raise ValueError("ZERO_TOTAL_EVENT_DENOMINATOR")
    return s/n

def _q(ordered,p):
    if not ordered: raise ValueError("EMPTY_BOOTSTRAP_DISTRIBUTION")
    if len(ordered)==1: return ordered[0]
    h=(len(ordered)-1)*p
    lo=math.floor(h); hi=math.ceil(h)
    if lo==hi: return ordered[lo]
    w=h-lo
    return ordered[lo]+w*(ordered[hi]-ordered[lo])

def moving_block_ratio_ci(calendar, events, *, execution_scope, block_length, replications, seed, confidence_level, interval_method, real_execution_authorized=False):
    if execution_scope not in ("SYNTHETIC_QUALIFICATION","REAL_AUTHORIZED"):
        raise ValueError("EXECUTION_SCOPE_INVALID")
    if execution_scope=="REAL_AUTHORIZED" and real_execution_authorized is not True:
        raise ValueError("REAL_EXECUTION_NOT_AUTHORIZED")
    cal=_validate_calendar(calendar)
    agg=aggregate_week_counts(cal,events)
    n=len(agg)
    if isinstance(block_length,bool) or not isinstance(block_length,int) or block_length<=0 or block_length>n:
        raise ValueError("BLOCK_LENGTH_REQUIRED")
    if isinstance(replications,bool) or not isinstance(replications,int) or replications<=0:
        raise ValueError("INVALID_REPLICATIONS")
    if isinstance(seed,bool) or not isinstance(seed,int):
        raise ValueError("SEED_REQUIRED")
    if isinstance(confidence_level,bool) or not isinstance(confidence_level,(int,float)) or not (0<float(confidence_level)<1):
        raise ValueError("INVALID_CONFIDENCE_LEVEL")
    if interval_method not in INTERVAL_METHODS:
        raise ValueError("INTERVAL_METHOD_UNSUPPORTED")
    point=ratio_of_sums(agg)
    rng=random.Random(seed)
    reps=[]
    max_start=n-block_length
    for _ in range(replications):
        sampled=[]
        while len(sampled)<n:
            start=rng.randrange(max_start+1)
            sampled.extend(agg[start:start+block_length])
        sampled=sampled[:n]
        denom=sum(x["event_count"] for x in sampled)
        if denom<=0: raise ValueError("ZERO_DENOMINATOR_REPLICATE")
        reps.append(sum(x["success_count"] for x in sampled)/denom)
    reps.sort()
    alpha=(1-float(confidence_level))/2
    qlo=_q(reps,alpha); qhi=_q(reps,1-alpha)
    if interval_method=="PERCENTILE":
        lo,hi=qlo,qhi
    else:
        lo,hi=2*point-qhi,2*point-qlo
    return {"contract":CONTRACT,"execution_scope":execution_scope,"calendar_week_count":n,"statistic":"RATIO_OF_SUMS","block_length":block_length,"replications":replications,"seed":seed,"confidence_level":float(confidence_level),"interval_method":interval_method,"point_estimate":point,"lower":lo,"upper":hi,"individual_event_iid_resampling":False}

def temporal_stability_synthetic(values, *, strata, declared_strata, minimum_n_per_stratum, max_mean_spread):
    if not isinstance(values,(list,tuple)) or not values: raise ValueError("EMPTY_SAMPLE")
    if len(strata)!=len(values): raise ValueError("STRATUM_LENGTH_MISMATCH")
    if not declared_strata: raise ValueError("DECLARED_STRATA_REQUIRED")
    if len(set(declared_strata))!=len(declared_strata): raise ValueError("DUPLICATE_DECLARED_STRATUM")
    if any(s not in declared_strata for s in strata): raise ValueError("UNDECLARED_STRATUM")
    if isinstance(minimum_n_per_stratum,bool) or not isinstance(minimum_n_per_stratum,int) or minimum_n_per_stratum<=0: raise ValueError("INVALID_MINIMUM_N_PER_STRATUM")
    if isinstance(max_mean_spread,bool) or not isinstance(max_mean_spread,(int,float)) or max_mean_spread<0: raise ValueError("INVALID_MAX_MEAN_SPREAD")
    details={}; means=[]; insufficient=[]
    for label in declared_strata:
        vals=[float(v) for v,s in zip(values,strata) if s==label]
        if len(vals)<minimum_n_per_stratum: insufficient.append(label)
        mean=sum(vals)/len(vals) if vals else None
        if mean is not None: means.append(mean)
        details[label]={"n":len(vals),"mean":mean}
    spread=(max(means)-min(means)) if len(means)>1 else 0.0
    if insufficient: status="INSUFFICIENT_CONDITIONAL_SAMPLE"
    else: status="STABLE_WITHIN_DECLARED_TOLERANCE" if spread<=max_mean_spread else "INSTABILITY_DETECTED"
    return {"status":status,"strata":details,"observed_mean_spread":spread,"insufficient_strata":insufficient}

def nonstationarity_gate_support(*, m04_status, m10_status, conflicting_policy):
    if conflicting_policy!="ANY_BLOCK_OR_CONFLICT_UNRESOLVED": raise ValueError("CONFLICT_POLICY_UNSUPPORTED")
    if m04_status=="BLOCKED_BY_REPRESENTATION_CONSTRAINT": return {"state":"NONSTATIONARITY_UNRESOLVED","reason":"M04_RESPONSE_REPRESENTATION_BLOCKED"}
    if m10_status=="INSTABILITY_DETECTED": return {"state":"NONSTATIONARITY_MATERIALLY_DETECTED","reason":"M10_INSTABILITY"}
    if m10_status=="INSUFFICIENT_CONDITIONAL_SAMPLE": return {"state":"NONSTATIONARITY_UNRESOLVED","reason":"M10_INSUFFICIENT"}
    if m04_status=="NO_MATERIAL_DEPENDENCE_FOUND_WITHIN_TESTED_LAGS" and m10_status=="STABLE_WITHIN_DECLARED_TOLERANCE": return {"state":"NONSTATIONARITY_NOT_MATERIALLY_DETECTED","reason":"ALL_PREDECLARED_DIAGNOSTICS_CLEAR"}
    return {"state":"NONSTATIONARITY_UNRESOLVED","reason":"DIAGNOSTIC_CONFLICT_OR_UNKNOWN"}

def assert_calendar_binding(actual_blob, expected_blob):
    if not isinstance(actual_blob,str) or not isinstance(expected_blob,str) or not actual_blob or not expected_blob: raise ValueError("CALENDAR_IDENTITY_REQUIRED")
    if actual_blob!=expected_blob: raise ValueError("CALENDAR_IDENTITY_MISMATCH")
    return True

def guard_request(request):
    if not isinstance(request,dict): raise ValueError("REQUEST_INVALID")
    if request.get("analysis_surface")!="GLOBAL_RESPONSE_GENERALIZATION_ONLY": raise ValueError("UNAUTHORIZED_ANALYSIS_SURFACE")
    if request.get("method")!="MOVING_BLOCK_RATIO_OF_SUMS": raise ValueError("UNAUTHORIZED_METHOD")
    if request.get("response_subgroup") is not None: raise ValueError("RESPONSE_SUBGROUP_NOT_AUTHORIZED")
    if request.get("occurrence_x_response") is not False: raise ValueError("OCCURRENCE_X_RESPONSE_NOT_AUTHORIZED")
    if request.get("time_to_reintegration") is not False: raise ValueError("TIME_TO_REINTEGRATION_NOT_AUTHORIZED")
    if request.get("occurrence_m05_reused") is not False: raise ValueError("OCCURRENCE_M05_REUSE_FORBIDDEN")
    if request.get("response_m05_activation_state")!="NOT_ACTIVATED": raise ValueError("RESPONSE_M05_ACTIVATION_NOT_AUTHORIZED")
    if request.get("trading_authority")!="NONE": raise ValueError("TRADING_AUTHORITY_FORBIDDEN")
    return True
