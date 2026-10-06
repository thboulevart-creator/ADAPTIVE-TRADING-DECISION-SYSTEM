#!/usr/bin/env python3
"""BEPD-08D deterministic dual close-side distance distributions.

Consumes only persisted BEPD-02 EVENT_LEDGER.close_displacement.
Classifies each event exactly once:
  > 0 INTERNAL
  < 0 EXTERNAL
  = 0 EXACT_LEVEL
Computes separate descriptive distributions for D_INTERNAL and D_EXTERNAL.
No market reconstruction, comparative metric, threshold search, inference,
prediction, strategy, PnL or trading analysis.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from decimal import Decimal, ROUND_HALF_EVEN, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec=80
Q18=Decimal("0.000000000000000001")
PROBS=[("P01",Decimal("0.01")),("P05",Decimal("0.05")),("P10",Decimal("0.10")),("P25",Decimal("0.25")),("P50",Decimal("0.50")),("P75",Decimal("0.75")),("P90",Decimal("0.90")),("P95",Decimal("0.95")),("P99",Decimal("0.99"))]

EXPECTED_BINDINGS={
 "event_ledger_blob":"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
 "bepd08c_final_adjudication_blob":"0cc7d4f812525bd3c4dab29490613b70f8600514",
 "bepd08c_contract_blob":"dc767d77b8f0c8cf89f6d87e9a4cd2401dd0b42e",
 "bepd08c_breaker_blob":"13ad7dba0d4e83036ea1f40b47f1a0a8d1f40bb8",
 "bepd08c_freeze_blob":"e4d6ebb35147f8cb884dbe569197236ed34251da",
 "bepd08b_final_adjudication_blob":"73ff0141c2e879ae0b3c51444d5a0af95359ba6f",
 "bepd08b_result_blob":"ed6e9088e06e80c21fcb6314add93268c9bc307a",
 "bepd05a_contract_blob":"0a580920ce47885d2bd3277b879b2b888b8d4354",
 "bepd05b_result_blob":"1280156ca949fc48f00e50240aa09cdae11ba4d7",
 "bepd08a_contract_blob":"4cfcb983ad64f31b443534d70991f8ddcb11ff8f",
}

POLICY={
 "classification_source":"close_displacement",
 "internal_rule":"close_displacement > 0",
 "external_rule":"close_displacement < 0",
 "exact_level_rule":"close_displacement == 0",
 "distance":"abs(close_displacement)",
 "same_week_reintegration_used":False,
 "reintegration_h1_close_utc_used":False,
 "high_low_used":False,
 "market_reconstruction":False,
 "ap0_read":False,
 "h1_read":False,
 "weekly_reconstruction":False,
 "comparative_metrics":False,
 "difference_of_means":False,
 "difference_of_medians":False,
 "ratios":False,
 "effect_size":False,
 "significance_test":False,
 "confidence_interval":False,
 "threshold_search":False,
 "tp_sl":False,
 "pnl":False,
 "prediction":False,
 "edge":False,
 "strategy_validation":False,
 "trading_authority":"NONE",
}

ALLOWED_CORE={"N","MINIMUM","MAXIMUM","MEAN","MEDIAN","P01","P05","P10","P25","P50","P75","P90","P95","P99","ZERO_COUNT","ZERO_FRACTION","EMPIRICAL_CDF"}

def q18(v:Decimal)->str:
    return format(v.quantize(Q18,rounding=ROUND_HALF_EVEN),"f")

def frac(n:int,d:int)->str:
    f=Fraction(n,d)
    return str(f.numerator) if f.denominator==1 else f"{f.numerator}/{f.denominator}"

def type7(xs:list[Decimal],p:Decimal)->Decimal:
    if not xs: raise ValueError("empty distribution")
    n=len(xs)
    if n==1: return xs[0]
    h=Decimal(1)+Decimal(n-1)*p
    j=int(h); g=h-Decimal(j)
    if j>=n:return xs[-1]
    return xs[j-1]+g*(xs[j]-xs[j-1])

def validate_bindings(b:dict)->None:
    for k,v in EXPECTED_BINDINGS.items():
        if b.get(k)!=v: raise ValueError(f"binding mismatch: {k}")

def validate_policy(p:dict)->None:
    if set(p) != set(POLICY): raise ValueError("policy key-set mismatch")
    for k,v in POLICY.items():
        if p.get(k)!=v: raise ValueError(f"policy mismatch: {k}")

def classify(v:Decimal)->str:
    if not v.is_finite(): raise ValueError("non-finite close_displacement")
    if v>0:return "INTERNAL"
    if v<0:return "EXTERNAL"
    return "EXACT_LEVEL"

def load_rows(path:Path)->list[dict]:
    rows=[]
    with path.open("r",encoding="utf-8") as fh:
        for no,line in enumerate(fh,1):
            if not line.strip():continue
            try: rows.append(json.loads(line,parse_float=Decimal))
            except Exception as e: raise ValueError(f"invalid JSONL line {no}: {e}") from e
    return rows

def partition_rows(rows:list[dict],expected_total:int,expected_internal:int,expected_external:int,expected_exact:int)->dict:
    if len(rows)!=expected_total: raise ValueError("total population mismatch")
    ids=[]; groups={"INTERNAL":[],"EXTERNAL":[],"EXACT_LEVEL":[]}
    for i,r in enumerate(rows):
        eid=r.get("event_id")
        if not isinstance(eid,str) or not eid: raise ValueError(f"invalid event_id row {i}")
        ids.append(eid)
        if "close_displacement" not in r: raise ValueError(f"missing close_displacement row {i}")
        raw=r["close_displacement"]; v=raw if isinstance(raw,Decimal) else Decimal(str(raw))
        side=classify(v)
        groups[side].append(abs(v))
    if len(set(ids))!=expected_total: raise ValueError("duplicate event_id")
    obs=(len(groups["INTERNAL"]),len(groups["EXTERNAL"]),len(groups["EXACT_LEVEL"]))
    exp=(expected_internal,expected_external,expected_exact)
    if obs!=exp: raise ValueError(f"partition population mismatch: observed={obs} expected={exp}")
    if sum(obs)!=expected_total: raise ValueError("non-exhaustive partition")
    if any(v<0 for g in groups.values() for v in g): raise ValueError("negative conditional distance")
    return groups

def aggregate(xs:list[Decimal])->dict:
    if any(v < 0 for v in xs): raise ValueError("negative conditional distance")
    xs=sorted(xs); n=len(xs)
    if n==0:raise ValueError("empty distribution")
    qs={k:q18(type7(xs,p)) for k,p in PROBS}
    zeros=sum(v==0 for v in xs)
    counts=Counter(xs); cum=0; ecdf=[]
    for s in sorted(counts):
        c=counts[s];cum+=c
        ecdf.append({"support_value":format(s,"f"),"support_count":c,"cumulative_count":cum,"cumulative_fraction":frac(cum,n),"cumulative_decimal":q18(Decimal(cum)/Decimal(n))})
    core={"N":n,"MINIMUM":q18(xs[0]),"MAXIMUM":q18(xs[-1]),"MEAN":q18(sum(xs,Decimal(0))/Decimal(n)),"MEDIAN":qs["P50"],**qs,"ZERO_COUNT":zeros,"ZERO_FRACTION":{"fraction":frac(zeros,n),"decimal":q18(Decimal(zeros)/Decimal(n))},"EMPIRICAL_CDF":ecdf}
    if set(core)!=ALLOWED_CORE:raise ValueError("unauthorized output surface")
    if core["P50"]!=core["MEDIAN"]:raise ValueError("P50 != median")
    if ecdf[-1]["cumulative_count"]!=n or ecdf[-1]["cumulative_fraction"]!="1":raise ValueError("ECDF terminal mismatch")
    return core

def run(rows:list[dict])->dict:
    validate_policy(POLICY)
    groups=partition_rows(rows,472,207,265,0)
    return {"INTERNAL":aggregate(groups["INTERNAL"]),"EXTERNAL":aggregate(groups["EXTERNAL"]),"EXACT_LEVEL_COUNT":len(groups["EXACT_LEVEL"])}

def sha256_file(p:Path)->str:
    h=hashlib.sha256();h.update(p.read_bytes());return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    for x in ["input","output","manifest","source-blob","bepd08c-final-blob","contract-blob","breaker-blob","freeze-blob","runner-blob"]: ap.add_argument("--"+x,required=True)
    args=ap.parse_args()
    bindings={"event_ledger_blob":args.source_blob,"bepd08c_final_adjudication_blob":args.bepd08c_final_blob,"bepd08c_contract_blob":args.contract_blob,"bepd08c_breaker_blob":args.breaker_blob,"bepd08c_freeze_blob":args.freeze_blob,"bepd08b_final_adjudication_blob":EXPECTED_BINDINGS["bepd08b_final_adjudication_blob"],"bepd08b_result_blob":EXPECTED_BINDINGS["bepd08b_result_blob"],"bepd05a_contract_blob":EXPECTED_BINDINGS["bepd05a_contract_blob"],"bepd05b_result_blob":EXPECTED_BINDINGS["bepd05b_result_blob"],"bepd08a_contract_blob":EXPECTED_BINDINGS["bepd08a_contract_blob"]}
    validate_bindings(bindings)
    inp=Path(args.input); rows=load_rows(inp); dual=run(rows)
    run_bindings={**bindings,"runner_blob":args.runner_blob,"total_n":472,"internal_n":207,"external_n":265,"exact_level_n":0,"quantile_method":"HYNDMAN_FAN_TYPE_7","ecdf":"EXACT_UNSMOOTHED_UNBINNED","scalar_output":"18_DECIMAL_ROUND_HALF_EVEN"}
    run_id=hashlib.sha256(json.dumps(run_bindings,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    result={"schema":"ATDS_BEPD_08D_FIRST_REAL_INTERNAL_EXTERNAL_DISTANCE_DISTRIBUTIONS_V0_1","control_id":"BEPD-08D","run_id":run_id,"scope":"DUAL_CONDITIONAL_CLOSE_SIDE_DISTRIBUTIONS","partition":{"TOTAL_N":472,"INTERNAL_N":dual["INTERNAL"]["N"],"EXTERNAL_N":dual["EXTERNAL"]["N"],"EXACT_LEVEL_N":dual["EXACT_LEVEL_COUNT"],"OVERLAPPING_MEMBERSHIP":0,"UNCLASSIFIED_EVENTS":0},"classification":{"INTERNAL":"close_displacement > 0","EXTERNAL":"close_displacement < 0","EXACT_LEVEL":"close_displacement == 0","same_week_reintegration_used":False,"high_low_used":False},"distance":{"formula":"abs(close_displacement)","source_policy":"PERSISTED_FIELD_ONLY","unit":"USTECH_PRICE_UNITS_AS_PERSISTED"},"numerical_contract":{"quantile_method":"HYNDMAN_FAN_TYPE_7","p50_equals_median":True,"ecdf":"EXACT_UNSMOOTHED_UNBINNED","scalar_output":"18_DECIMAL_ROUND_HALF_EVEN"},"INTERNAL":dual["INTERNAL"],"EXTERNAL":dual["EXTERNAL"],"comparative_metrics":[],"subgroups":[],"threshold_search_executed":False,"tp_sl_executed":False,"pnl_executed":False,"prediction":False,"edge":False,"strategy_validation":False,"trading_authority":"NONE","evidence_status":"EXPOSED_EXPLORATORY_ONLY","generalization":"NOT_ESTABLISHED","bindings":run_bindings}
    out=Path(args.output);man=Path(args.manifest);out.parent.mkdir(parents=True,exist_ok=True);man.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    manifest={"schema":"ATDS_BEPD_08D_RUN_MANIFEST_V0_1","run_id":run_id,"input_path":str(inp),"input_git_blob":args.source_blob,"input_sha256":sha256_file(inp),"output_path":str(out),"output_sha256":sha256_file(out),"runner_blob":args.runner_blob,"partition":{"TOTAL":472,"INTERNAL":207,"EXTERNAL":265,"EXACT_LEVEL":0},"result_exposure":"FIRST_REAL_DUAL_CONDITIONAL_DISTRIBUTIONS"}
    man.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":main()
