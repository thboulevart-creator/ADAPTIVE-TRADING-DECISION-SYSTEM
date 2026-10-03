"""RTMA-01 V0.2 minimal synthetic change laboratory.

Synthetic generation, truth separation, view construction, matching and
mechanical scoring only. No detector selection, scientific authority, trading,
production, causal, decision or adaptation authority is exposed.
"""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Iterable
import numpy as np

CONTRACT = "RTMA_01_SYNTHETIC_CHANGE_LAB_V0_2"
GENERATOR_IDENTITY = "RTMA_01_SYNTHETIC_CHANGE_GENERATOR_V0_2"

TASK_CLASSES = (
    "DISTRIBUTIONAL_CHANGE_DETECTION",
    "PERSISTENT_MARKET_TRANSITION_DETECTION",
    "GRADUAL_DRIFT_DETECTION",
    "TRANSIENT_SHOCK_DETECTION",
    "DATA_INTEGRITY_CHANGE_DETECTION",
    "STATE_NOVELTY_RECOGNITION",
    "TRANSITION_NOVELTY_RECOGNITION",
    "RESPONSE_NOVELTY_DETECTION",
    "WITHIN_CONTEXT_RESPONSE_DEGRADATION",
    "EXECUTION_DEGRADATION",
)
LANES = (
    ("LANE_O","ONLINE_SEQUENTIAL","PREFIX_ONLY"),
    ("LANE_R","RETROSPECTIVE","FULL_FROZEN_SEQUENCE"),
    ("LANE_M","MEMORY_RECOGNITION","TIME_CAUSAL_REFERENCE_MEMORY"),
    ("LANE_E","EDGE_RESPONSE","FROZEN_CONTEXT_PLUS_SYNTHETIC_RESPONSE"),
)
CASE_FAMILIES = (
    ("SYN-00","NO_STRUCTURAL_CHANGE"),
    ("SYN-01","ABRUPT_LOCATION_CHANGE"),
    ("SYN-02","ABRUPT_SCALE_VARIANCE_CHANGE"),
    ("SYN-03","DEPENDENCY_CHANGE"),
    ("SYN-04","GRADUAL_DRIFT"),
    ("SYN-05","TRANSIENT_SHOCK"),
    ("SYN-06","A_TO_B_TO_A_RECURRENCE"),
    ("SYN-07","KNOWN_ENDPOINTS_MEMORY_NOVEL_TRANSITION"),
    ("SYN-08","MEMORY_NOVEL_STATE"),
    ("SYN-09","FAMILIAR_STATE_RESPONSE_NOVELTY"),
    ("SYN-10","OBSERVATION_PROVIDER_ARTIFACT"),
    ("SYN-11","CONTEXT_MIX_CHANGE_WITHOUT_CONDITIONAL_RESPONSE_CHANGE"),
    ("SYN-12","WITHIN_CONTEXT_RESPONSE_CHANGE"),
    ("SYN-13","EXECUTION_DEGRADATION"),
    ("SYN-14","MULTIPLE_CLOSE_STRUCTURAL_CHANGES"),
    ("SYN-15","WEAK_CHANGE_NEAR_DETECTION_LIMIT"),
    ("SYN-16","EXPECTED_PERIODIC_VARIATION"),
    ("SYN-17","CONTINUITY_BREAK_WITHOUT_LATENT_MARKET_CHANGE"),
    ("SYN-18","HEAVY_TAILED_AUTOCORRELATED_NO_CHANGE"),
    ("SYN-19","ASYNCHRONOUS_MULTIDIMENSIONAL_CHANGE"),
    ("SYN-20","SCALE_LOCAL_CHANGE"),
    ("SYN-21","STOCHASTIC_VOLATILITY_WITHOUT_STRUCTURAL_BREAK"),
    ("SYN-22","WANDERING_LEVEL_WITHOUT_DISCRETE_BREAK"),
)
_CASE_IDS = frozenset(x[0] for x in CASE_FAMILIES)
_LANE_IDS = frozenset(x[0] for x in LANES)
_INPUT_VIEWS = frozenset({
    "MARKET_OBSERVATIONS_ONLY",
    "MARKET_PLUS_ADMISSIBLE_CONTINUITY_STATUS",
    "INTEGRITY_STREAM_ONLY",
    "RESPONSE_PLUS_CONTEXT",
})

def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()

def _str(value: object, label: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{label} must be exact str")
    if not value.strip():
        raise ValueError(f"{label} must be nonempty")
    return value

def _int(value: object, label: str, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise TypeError(f"{label} must be exact int")
    if minimum is not None and value < minimum:
        raise ValueError(f"{label} below minimum")
    return value

def validate_case_spec(spec: object) -> bool:
    if type(spec) is not dict:
        raise TypeError("case spec must be exact dict")
    required=("case_id","seed","generator_version","prng_identity","runtime_identity","scope_id","sample_count","task_id","input_view_id")
    missing=[k for k in required if k not in spec]
    if missing:
        raise ValueError(f"case spec missing fields: {missing}")
    if _str(spec["case_id"],"case_id") not in _CASE_IDS:
        raise ValueError("unknown case_id")
    _int(spec["seed"],"seed",0)
    if spec["generator_version"] != "V0.2":
        raise ValueError("generator_version mismatch")
    if spec["prng_identity"] != "PCG64":
        raise ValueError("prng_identity must be PCG64")
    _str(spec["runtime_identity"],"runtime_identity")
    _str(spec["scope_id"],"scope_id")
    _int(spec["sample_count"],"sample_count",32)
    if spec["task_id"] not in TASK_CLASSES:
        raise ValueError("unknown task_id")
    if spec["input_view_id"] not in _INPUT_VIEWS:
        raise ValueError("unknown input_view_id")
    if spec.get("surface") not in (None,"DEVELOPMENT","HOLDOUT"):
        raise ValueError("unknown surface")
    if spec.get("surface")=="HOLDOUT" and spec.get("consumed_for_model_modification") is True and spec.get("untouched") is True:
        raise ValueError("consumed holdout cannot remain untouched")
    return True

def build_opaque_run_identity(spec: object) -> str:
    validate_case_spec(spec)
    return "RUN-" + canonical_sha256({"contract":CONTRACT,"generator":GENERATOR_IDENTITY,"case_spec":spec})[:32]

def _schedule(case_id: str, n: int) -> dict[str,object]:
    m=n//2; t=n//3
    return {
        "SYN-00":{"kind":"NO_CHANGE"},
        "SYN-01":{"kind":"LOCATION_STEP","onset":m,"delta":2.0,"dimension":"X"},
        "SYN-02":{"kind":"SCALE_STEP","onset":m,"factor":2.0,"dimension":"X"},
        "SYN-03":{"kind":"DEPENDENCY_STEP","onset":m,"rho_before":0.0,"rho_after":0.8},
        "SYN-04":{"kind":"DRIFT","start":t,"end":2*t,"delta":2.0},
        "SYN-05":{"kind":"TRANSIENT_SHOCK","start":m,"end":min(n,m+8),"delta":5.0},
        "SYN-06":{"kind":"RECURRENCE","events":[t,2*t],"states":["A","B","A"]},
        "SYN-07":{"kind":"KNOWN_ENDPOINTS_NOVEL_PATH","start":t,"end":2*t},
        "SYN-08":{"kind":"MEMORY_NOVEL_STATE","onset":m,"state":"C"},
        "SYN-09":{"kind":"RESPONSE_NOVELTY","onset":m},
        "SYN-10":{"kind":"OBSERVATION_SCALE_ARTIFACT","onset":m,"factor":10.0},
        "SYN-11":{"kind":"CONTEXT_MIX_SHIFT","onset":m,"mix_before":[0.8,0.2],"mix_after":[0.2,0.8]},
        "SYN-12":{"kind":"WITHIN_CONTEXT_RESPONSE_SHIFT","onset":m},
        "SYN-13":{"kind":"EXECUTION_DEGRADATION","onset":m},
        "SYN-14":{"kind":"CLOSE_MULTIPLE_CHANGES","events":[max(1,m-8),min(n-1,m+4)]},
        "SYN-15":{"kind":"WEAK_LOCATION_STEP","onset":m,"delta":0.2},
        "SYN-16":{"kind":"FIXED_PERIODIC","period":16},
        "SYN-17":{"kind":"CONTINUITY_BREAK","start":max(1,m-4),"end":min(n,m+4)},
        "SYN-18":{"kind":"HEAVY_TAIL_AR1","phi":0.6,"df":4},
        "SYN-19":{"kind":"ASYNC_DIMENSION_CHANGES","x_onset":max(1,m-12),"y_onset":min(n-1,m+12)},
        "SYN-20":{"kind":"SCALE_LOCAL_PULSE","start":max(1,m-3),"end":min(n,m+3)},
        "SYN-21":{"kind":"STATIONARY_STOCHASTIC_VOLATILITY","alpha":0.15,"beta":0.8},
        "SYN-22":{"kind":"RANDOM_WALK_NO_DISCRETE_BREAK"},
    }[case_id]

def _truth(case_id: str, schedule: dict[str,object]) -> dict[str,object]:
    no_break={"SYN-00","SYN-16","SYN-17","SYN-18","SYN-21","SYN-22"}
    gt={"case_id":case_id,"semantic_schedule":schedule,"structural_change":case_id not in no_break,"events":[]}
    if case_id=="SYN-05": gt.update(transient_shock=True,durable_transition=False)
    if case_id=="SYN-10": gt.update(latent_market_change=False,observation_process_change=True)
    if case_id=="SYN-11": gt.update(context_mix_change=True,within_context_response_change=False)
    if case_id=="SYN-12": gt.update(market_law_change=False,within_context_response_change=True)
    if case_id=="SYN-13": gt.update(gross_response_change=False,execution_degradation=True)
    if case_id in {"SYN-07","SYN-08"}: gt["reference_memory_required"]=True
    if case_id=="SYN-20": gt["scale_truths_derived_from_one_base_process"]=True
    return gt

def _obs(x: np.ndarray, y: np.ndarray) -> list[list[float]]:
    return [[float(a),float(b)] for a,b in zip(x,y,strict=True)]

def generate_case(spec: object) -> dict[str,object]:
    validate_case_spec(spec)
    cid=spec["case_id"]; n=spec["sample_count"]; m=n//2; t=n//3
    rng=np.random.Generator(np.random.PCG64(spec["seed"]))
    schedule=_schedule(cid,n); gt=_truth(cid,schedule)
    x=rng.normal(0,1,n); y=rng.normal(0,1,n)
    response=[0.0]*n; integrity=[]
    if cid=="SYN-01":
        x[m:]+=2; gt["events"]=[{"event_id":"E1","onset":m,"dimensions":["X"]}]
    elif cid=="SYN-02":
        x[m:]*=2; gt["events"]=[{"event_id":"E1","onset":m,"dimensions":["X"]}]
    elif cid=="SYN-03":
        z=rng.normal(0,1,n-m); y[m:]=0.8*x[m:]+0.6*z
        gt["events"]=[{"event_id":"E1","onset":m,"dimensions":["DEPENDENCY"]}]
    elif cid=="SYN-04":
        end=2*t; x[t:end]+=np.linspace(0,2,max(0,end-t),endpoint=False); x[end:]+=2
        gt.update(geometry="ONSET_INTERVAL",interval=[t,end],events=[{"event_id":"D1","interval":[t,end],"dimensions":["X"]}])
    elif cid=="SYN-05":
        end=min(n,m+8); x[m:end]+=5; gt["events"]=[{"event_id":"S1","interval":[m,end],"dimensions":["X"]}]
    elif cid=="SYN-06":
        x[t:2*t]+=2; gt["events"]=[{"event_id":"E1","onset":t,"dimensions":["X"]},{"event_id":"E2","onset":2*t,"dimensions":["X"]}]
    elif cid=="SYN-07":
        end=2*t; phase=np.linspace(0,np.pi,max(1,end-t),endpoint=False); x[t:end]+=1-np.cos(phase); x[end:]+=2
        gt["events"]=[{"event_id":"E1","interval":[t,end],"dimensions":["X"]}]
    elif cid=="SYN-08":
        x[m:]+=3; gt["events"]=[{"event_id":"E1","onset":m,"dimensions":["X"]}]
    elif cid=="SYN-09":
        response=[float(v) for v in rng.normal(0,1,n)]
        for i in range(m,n): response[i]+=1.5
        gt["events"]=[{"event_id":"R1","onset":m,"dimensions":["RESPONSE"]}]
    elif cid=="SYN-10":
        x[m:]*=10; y[m:]*=10; integrity=[{"at":m,"kind":"OBSERVATION_SCALE_CHANGE"}]
        gt["events"]=[{"event_id":"A1","onset":m,"dimensions":["OBSERVATION_PROCESS"]}]
    elif cid=="SYN-11":
        state=rng.random(n); x[:m]+=np.where(state[:m]<0.8,0,2); x[m:]+=np.where(state[m:]<0.2,0,2)
        gt["events"]=[{"event_id":"M1","onset":m,"dimensions":["CONTEXT_MIX"]}]
    elif cid=="SYN-12":
        response=[float(v) for v in rng.normal(0,1,n)]
        for i in range(m,n): response[i]+=1
        gt["events"]=[{"event_id":"R1","onset":m,"dimensions":["WITHIN_CONTEXT_RESPONSE"]}]
    elif cid=="SYN-13":
        response=[float(v) for v in rng.normal(0,1,n)]
        for i in range(m,n): response[i]-=0.75
        gt["events"]=[{"event_id":"X1","onset":m,"dimensions":["EXECUTION"]}]
    elif cid=="SYN-14":
        a,b=max(1,m-8),min(n-1,m+4); x[a:]+=1.5; x[b:]-=2.5
        gt["events"]=[{"event_id":"E1","onset":a,"dimensions":["X"]},{"event_id":"E2","onset":b,"dimensions":["X"]}]
    elif cid=="SYN-15":
        x[m:]+=0.2; gt["events"]=[{"event_id":"E1","onset":m,"dimensions":["X"],"difficulty":"WEAK"}]
    elif cid=="SYN-16":
        x+=np.sin(2*np.pi*np.arange(n)/16)
    elif cid=="SYN-17":
        a,b=max(1,m-4),min(n,m+4); integrity=[{"start":a,"end":b,"kind":"CONTINUITY_BREAK"}]
    elif cid=="SYN-18":
        e=rng.standard_t(4,n); x=np.zeros(n)
        for i in range(1,n): x[i]=0.6*x[i-1]+e[i]
    elif cid=="SYN-19":
        a,b=max(1,m-12),min(n-1,m+12); x[a:]+=1.5; y[b:]*=1.8
        gt["events"]=[{"event_id":"E1","onset":a,"dimensions":["X"]},{"event_id":"E2","onset":b,"dimensions":["Y"]}]
    elif cid=="SYN-20":
        a,b=max(1,m-3),min(n,m+3); x[a:b]+=3; gt["events"]=[{"event_id":"F1","interval":[a,b],"dimensions":["FAST_SCOPE"]}]
    elif cid=="SYN-21":
        e=rng.normal(0,1,n); var=np.ones(n); x=np.zeros(n)
        for i in range(1,n):
            var[i]=0.05+0.15*x[i-1]**2+0.8*var[i-1]; x[i]=float(np.sqrt(max(var[i],1e-12))*e[i])
    elif cid=="SYN-22":
        x=np.cumsum(rng.normal(0,0.25,n))
    return {
        "run_id":build_opaque_run_identity(spec),
        "observations":_obs(x,y),
        "ground_truth":gt,
        "integrity_stream":integrity,
        "response_stream":response,
        "scope_id":spec["scope_id"],
        "task_id":spec["task_id"],
        "input_view_id":spec["input_view_id"],
    }

def seal_case(case: object) -> dict[str,str]:
    if type(case) is not dict or "observations" not in case or "ground_truth" not in case:
        raise TypeError("invalid case")
    return {
        "contract":CONTRACT,
        "observations_sha256":canonical_sha256(case["observations"]),
        "ground_truth_sha256":canonical_sha256(case["ground_truth"]),
        "case_sha256":canonical_sha256(case),
    }

def verify_case(case: object, seal: object) -> bool:
    if type(case) is not dict or type(seal) is not dict: return False
    try:
        return (
            seal.get("contract")==CONTRACT and
            seal.get("observations_sha256")==canonical_sha256(case["observations"]) and
            seal.get("ground_truth_sha256")==canonical_sha256(case["ground_truth"]) and
            seal.get("case_sha256")==canonical_sha256(case)
        )
    except Exception:
        return False

def iter_online_prefixes(observations: Iterable[object]):
    seen=[]
    for item in observations:
        seen.append(deepcopy(item)); yield deepcopy(seen)

def build_retrospective_view(observations: Iterable[object]) -> dict[str,object]:
    return {"evaluation_mode":"RETROSPECTIVE","observations":deepcopy(list(observations))}

def validate_reference_memory(memory: object, *, query_time: int, query_episode_id: str) -> bool:
    if type(memory) is not dict: raise TypeError("memory must be exact dict")
    _str(memory.get("version"),"memory.version"); _int(query_time,"query_time"); _str(query_episode_id,"query_episode_id")
    episodes=memory.get("episodes")
    if type(episodes) is not list: raise TypeError("memory.episodes must be exact list")
    for ep in episodes:
        if type(ep) is not dict: raise TypeError("episode must be exact dict")
        eid=_str(ep.get("episode_id"),"episode_id"); available=_int(ep.get("available_from"),"available_from")
        if eid==query_episode_id: raise ValueError("reference memory self-match forbidden")
        if available>=query_time: raise ValueError("future reference episode forbidden")
    return True

def validate_detector_output(output: object) -> bool:
    if type(output) is not dict: raise TypeError("detector output must be exact dict")
    required=("detector_id","detector_version","task_id","lane_id","scope_id","output_id","emitted_at","knowledge_cutoff_at","output_type")
    missing=[k for k in required if k not in output]
    if missing: raise ValueError(f"detector output missing fields: {missing}")
    for key in ("detector_id","detector_version","scope_id","output_id"): _str(output[key],key)
    if output["task_id"] not in TASK_CLASSES: raise ValueError("unknown task_id")
    if output["lane_id"] not in _LANE_IDS: raise ValueError("unknown lane_id")
    _int(output["emitted_at"],"emitted_at"); _int(output["knowledge_cutoff_at"],"knowledge_cutoff_at")
    if output["lane_id"]=="LANE_R" and "first_alert_at" in output: raise ValueError("retrospective cannot claim FIRST_ALERT_AT")
    if output["output_type"] not in {"RAW_SCORE","ALERT"}: raise ValueError("unknown output_type")
    if output["output_type"]=="RAW_SCORE" and "scalar_score" not in output: raise ValueError("RAW_SCORE requires scalar_score")
    if output["output_type"]=="ALERT" and "scalar_score" in output:
        if type(output.get("decision_adapter_id")) is not str or not output["decision_adapter_id"].strip():
            raise ValueError("score-derived ALERT requires decision_adapter_id")
    return True

def _anchor(event: dict[str,object]) -> tuple[int,int]:
    if "onset" in event:
        t=int(event["onset"]); return t,t
    interval=event.get("interval")
    if type(interval) is list and len(interval)==2: return int(interval[0]),int(interval[1])
    raise ValueError("truth event lacks onset/interval")

def match_outputs_to_truth(outputs: object, truth: object, policy: object) -> dict[str,object]:
    if type(outputs) is not list or type(truth) is not dict or type(policy) is not dict: raise TypeError("matching inputs")
    events=truth.get("events",[])
    if type(events) is not list: raise TypeError("truth.events")
    window=policy.get("match_window")
    if type(window) is not list or len(window)!=2: raise ValueError("match_window required")
    low,high=int(window[0]),int(window[1])
    outs=[deepcopy(o) for o in outputs]
    for o in outs: validate_detector_output(o)
    event_by_id={}; output_by_id={o["output_id"]:o for o in outs}; candidates=[]
    for event in events:
        eid=_str(event.get("event_id"),"event_id"); start,end=_anchor(event); event_by_id[eid]=event
        for o in outs:
            tt=o["emitted_at"]
            if start+low<=tt<=end+high:
                dist=start-tt if tt<start else tt-end if tt>end else 0
                candidates.append((dist,eid,o["output_id"],start,end))
    candidates.sort(key=lambda x:(x[0],x[1],x[2]))
    used_e=set(); used_o=set(); primary=[]
    for dist,eid,oid,start,end in candidates:
        if eid in used_e or oid in used_o: continue
        o=output_by_id[oid]; tt=o["emitted_at"]
        delay=0 if start<=tt<=end else (tt-start if tt<start else tt-end)
        pred=set(o.get("affected_dimensions",[])); actual=set(event_by_id[eid].get("dimensions",[]))
        primary.append({"event_id":eid,"output_id":oid,"delay":delay,"distance":dist,"dimension_correct":pred==actual if pred or actual else True})
        used_e.add(eid); used_o.add(oid)
    duplicates=[]; false_alerts=[]
    for o in outs:
        if o["output_id"] in used_o: continue
        if any(c[2]==o["output_id"] and c[1] in used_e for c in candidates): duplicates.append(o)
        else: false_alerts.append(o)
    misses=[deepcopy(e) for e in events if e["event_id"] not in used_e]
    return {"geometry":truth.get("geometry","POINT_EVENT"),"primary_matches":primary,"duplicates":duplicates,"false_alerts":false_alerts,"misses":misses}

def calculate_mechanical_metrics(match_result: object, truth: object, outputs: object) -> dict[str,int|float]:
    if type(match_result) is not dict or type(truth) is not dict or type(outputs) is not list: raise TypeError("metric inputs")
    p=match_result.get("primary_matches",[]); f=match_result.get("false_alerts",[]); d=match_result.get("duplicates",[]); m=match_result.get("misses",[])
    return {
        "true_event_count":len(truth.get("events",[])),
        "matched_event_count":len(p),
        "miss_count":len(m),
        "false_alert_count":len(f),
        "duplicate_alert_count":len(d),
        "dimension_true_positive_count":sum(1 for x in p if x.get("dimension_correct",True) is True),
        "delay_sum":float(sum(float(x.get("delay",0.0)) for x in p)),
    }
