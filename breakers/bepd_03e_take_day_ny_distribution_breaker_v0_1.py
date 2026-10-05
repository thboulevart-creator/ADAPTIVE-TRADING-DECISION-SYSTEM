from __future__ import annotations

import argparse, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

AUTH=Path("GOVERNANCE/BEPD-03E-EVENT-CONDITIONAL-TAKE-DAY-NY-DISTRIBUTION-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03E-TAKE-DAY-NY-DISTRIBUTION-IMPLEMENTATION-CONTRACT-V0.1.json")
CALC=Path("tools/bepd_03e_take_day_ny_distribution_v0_1.py")
BC=Path("GOVERNANCE/BEPD-03E-FROZEN-TAKE-DAY-NY-DISTRIBUTION-BREAKER-CONTRACT-V0.1.json")
DIMS=Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
Q03B=Path("reports/program/2026-10-05-BEPD-03B-GLOBAL-WEEKLY-LIQUIDITY-OCCURRENCE-BASELINE-QUALIFICATION-V0.1.md")
Q03C=Path("reports/program/2026-10-05-BEPD-03C-PREREGISTERED-CALENDAR-OCCURRENCE-MAP-QUALIFICATION-V0.1.md")
Q03D=Path("reports/program/2026-10-05-BEPD-03D-LEVEL-AGE-OCCURRENCE-MAP-QUALIFICATION-V0.1.md")
EVENT=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")

EXPECTED={
 AUTH:"e6e91abc1449ecc55f2241446e80da657148ca8f",
 IMPL:"5a4aa7f22abd68e47fe67b888314a33d0128530a",
 CALC:"98e025b430a051fa0b6eb7c55dd72dbfddd276eb",
 BC:"abb40d40299452fd6104690d640689c716973fd9",
 DIMS:"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
 MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
 M05:"53d33074038fa9d971b4672b1d981589da020a1e",
 ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
 Q03B:"e88bcce2d3256a9e374e76cfb5e9ebc641316d56",
 Q03C:"fd3b0caa97361e61e81510a2e69f0fbeb25cbe12",
 Q03D:"c7151af0bd7acce71f5d7f0e1e059c6f141c57d1",
 EVENT:"0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2",
 SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
CATS=["SUNDAY_OPEN","MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY"]
NY=ZoneInfo("America/New_York")
Q=Decimal("0.000000000000000001")
TOL=Decimal("0.000000000000000003")

class BF(AssertionError): pass
def fail(x:str)->None: print(f"BEPD_03E_BREAKER_FAIL:{x}"); raise SystemExit(1)
def eq(a,b,c):
    if a!=b: raise BF(f"{c}:expected={b!r}:actual={a!r}")
def req(x,c):
    if not x: raise BF(c)

def git_blob(root:Path,rel:Path)->str:
    cp=subprocess.run(["git","-C",str(root),"rev-parse",f"HEAD:{rel.as_posix()}"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
    if cp.returncode!=0: raise BF(f"MISSING:{rel}")
    return cp.stdout.strip()

def canon_hash(payload:dict[str,Any])->str:
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def parse_utc(v:Any,n:int)->datetime:
    req(isinstance(v,str) and bool(v),f"MISSING_TS:{n}")
    try: dt=datetime.fromisoformat(v)
    except ValueError as exc: raise BF(f"INVALID_TS:{n}:{exc}")
    req(dt.tzinfo is not None and dt.utcoffset() is not None,f"NAIVE_TS:{n}")
    eq(dt.utcoffset().total_seconds(),0.0,f"NON_UTC_TS:{n}")
    return dt.astimezone(timezone.utc)

def cat(dt:datetime)->str:
    local=dt.astimezone(NY)
    wd=local.weekday()
    if wd==5: raise BF(f"SATURDAY_LOCAL:{local.isoformat()}")
    m={6:"SUNDAY_OPEN",0:"MONDAY",1:"TUESDAY",2:"WEDNESDAY",3:"THURSDAY",4:"FRIDAY"}
    req(wd in m,f"UNMAPPED_WEEKDAY:{wd}")
    return m[wd]

def share(e:int,n:int)->str:
    return format((Decimal(e)/Decimal(n)).quantize(Q,rounding=ROUND_HALF_EVEN),"f")

def read_events(p:Path)->list[dict[str,Any]]:
    out=[]
    with p.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            r=json.loads(line)
            for k in ("run_id","event_id","sweep_cluster_id","target_week_id","take_h1_close_utc"):
                req(k in r,f"MISSING_FIELD:{n}:{k}")
            eq(r["run_id"],SOURCE_RUN_ID,f"RUN_ID:{n}")
            req(isinstance(r["event_id"],str) and r["event_id"],f"EVENT_ID:{n}")
            req(isinstance(r["sweep_cluster_id"],str) and r["sweep_cluster_id"],f"CLUSTER_ID:{n}")
            req(isinstance(r["target_week_id"],str) and r["target_week_id"],f"TARGET_WEEK:{n}")
            dt=parse_utc(r["take_h1_close_utc"],n)
            out.append({"event_id":r["event_id"],"cluster":r["sweep_cluster_id"],"week":r["target_week_id"],"category":cat(dt)})
    req(bool(out),"EMPTY_EVENT_LEDGER")
    eq(len({x["event_id"] for x in out}),len(out),"DUPLICATE_EVENT_ID")
    return out

def validate_synthetic_time()->None:
    eq(getattr(NY,"key",None),"America/New_York","TZ_KEY")
    probes=[
      ("2024-03-10T06:59:00+00:00","2024-03-10T01:59:00-05:00"),
      ("2024-03-10T07:00:00+00:00","2024-03-10T03:00:00-04:00"),
      ("2024-11-03T05:59:00+00:00","2024-11-03T01:59:00-04:00"),
      ("2024-11-03T06:00:00+00:00","2024-11-03T01:00:00-05:00"),
    ]
    for raw,expected in probes: eq(datetime.fromisoformat(raw).astimezone(NY).isoformat(),expected,f"DST:{raw}")
    synthetic=[
      ("2024-01-07T23:00:00+00:00","SUNDAY_OPEN"),
      ("2024-01-08T17:00:00+00:00","MONDAY"),
      ("2024-01-09T17:00:00+00:00","TUESDAY"),
      ("2024-01-10T17:00:00+00:00","WEDNESDAY"),
      ("2024-01-11T17:00:00+00:00","THURSDAY"),
      ("2024-01-12T17:00:00+00:00","FRIDAY"),
    ]
    for raw,expected in synthetic: eq(cat(datetime.fromisoformat(raw)),expected,f"DAYMAP:{expected}")
    try:
        cat(datetime.fromisoformat("2024-01-13T17:00:00+00:00"))
        raise BF("SATURDAY_ACCEPTED")
    except BF as exc:
        if str(exc)=="SATURDAY_ACCEPTED": raise

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); ap.add_argument("--result-dir",type=Path,required=True); a=ap.parse_args()
    root=a.root.resolve(); out=a.result_dir.resolve()
    try:
        for p,s in EXPECTED.items(): eq(git_blob(root,p),s,f"BLOB:{p}")
        validate_synthetic_time()
        bc=json.loads((root/BC).read_text(encoding="utf-8"))
        eq([x["id"] for x in bc["cases"]],[f"BEPD03E-B{i:02d}" for i in range(1,31)],"CASE_IDS")
        eq(bc["frozen_result_contract"]["category_order"],CATS,"CATEGORY_ORDER")
        eq(bc["frozen_result_contract"]["denominator_source"],"EVENT_LEDGER","DENOM_SOURCE")
        eq(bc["frozen_result_contract"]["m05_generalization_uncertainty"],"BLOCKED","BC_M05")

        eq({p.name for p in out.iterdir()},{"RESULT.json","RUN_MANIFEST.json"},"OUTPUT_SURFACE")
        result=json.loads((out/"RESULT.json").read_text(encoding="utf-8"))
        manifest=json.loads((out/"RUN_MANIFEST.json").read_text(encoding="utf-8"))

        eq(result["schema"],"ATDS_BEPD_03E_EVENT_CONDITIONAL_TAKE_DAY_NY_DISTRIBUTION_RESULT_V0_1","RESULT_SCHEMA")
        eq(result["interpretation"],"EVENT_CONDITIONAL_HISTORICAL_FIXED_CORPUS_TAKE_TIMING_DISTRIBUTION","INTERPRETATION")
        eq(result["population"]["denominator_source"],"EVENT_LEDGER","RESULT_DENOM_SOURCE")
        eq(result["m05_generalization_uncertainty"],"BLOCKED","M05")
        eq(result["forbidden_analytics_executed"],False,"FORBIDDEN_FLAG")
        req("EVENT != IID OBSERVATION" in result["dependence_statement"],"DEPENDENCE")
        req("sweep_cluster_id" in result["dependence_statement"] and "target_week_id" in result["dependence_statement"],"DEPENDENCE_KEYS")

        events=read_events(root/EVENT)
        total=len(events)
        eq(result["population"]["total_sweep_event_count"],total,"TOTAL_EVENTS")
        dim=result["dimension"]
        eq(dim["dimension_id"],"V06_TAKE_DAY_NY","DIM_ID")
        eq(dim["timezone"],"America/New_York","TZ")
        eq(dim["timestamp_source"],"take_h1_close_utc","TS_SOURCE")
        eq(dim["category_order"],CATS,"RESULT_CAT_ORDER")

        expected_cells=[]
        exact=Fraction(0,1); decsum=Decimal("0")
        for category in CATS:
            n=sum(1 for x in events if x["category"]==category)
            d=share(n,total)
            exact+=Fraction(n,total); decsum+=Decimal(d)
            expected_cells.append({"category":category,"event_count":n,"conditional_event_fraction":f"{n}/{total}","conditional_event_share_decimal":d})
        eq(dim["cells"],expected_cells,"DIRECT_RECOMPUTATION")
        eq(sum(x["event_count"] for x in expected_cells),total,"EVENT_RECON")
        eq(exact,Fraction(1,1),"EXACT_SHARE_RECON")
        err=abs(decsum-Decimal("1"))
        req(err<=TOL,f"DECIMAL_RECON:{decsum}:{err}")
        eq(result["decimal_reconciliation"],{
          "sum_of_cell_decimal_shares":format(decsum,"f"),
          "absolute_error_from_one":format(err,"f"),
          "tolerance":"0.000000000000000003",
          "within_tolerance":True
        },"DECIMAL_RECON_OBJ")

        forbidden={"occurrence_rate","opportunity_count","rank","best","worst","p_value","significance","confidence_interval","standard_error","bootstrap","side_filter","target_month","target_year","level_age_band","cross_product"}
        def walk(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    req(k.lower() not in forbidden,f"FORBIDDEN_KEY:{k}"); walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(result)

        eq(manifest["schema"],"ATDS_BEPD_03E_TAKE_DAY_NY_DISTRIBUTION_RUN_MANIFEST_V0_1","MAN_SCHEMA")
        eq(manifest["source_bepd02_run_id"],SOURCE_RUN_ID,"SOURCE_RUN")
        eq(manifest["forbidden_analytics_executed"],False,"MAN_FLAG")
        eq(manifest["calculator_blob"],EXPECTED[CALC],"CALC_BLOB")
        eq(manifest["input_git_blobs"],{"EVENT_LEDGER":EXPECTED[EVENT],"BEPD02_RUN_MANIFEST":EXPECTED[SOURCE_RUN]},"INPUT_BLOBS")
        req("LEVEL_WEEK_OPPORTUNITY" not in manifest["input_git_blobs"],"OPPORTUNITY_INPUT_PRESENT")
        eq(manifest["policy_git_blobs"],{
          "BEPD03E_AUTHORIZATION":EXPECTED[AUTH],"BEPD03E_IMPLEMENTATION_CONTRACT":EXPECTED[IMPL],
          "BEPD03A_DIMENSIONS":EXPECTED[DIMS],"BEPD03A_MEASUREMENT_CONTRACT":EXPECTED[MEASURE],
          "BEPD03A_M05_ACTIVATION":EXPECTED[M05],"BEPD03A_ADJUDICATION":EXPECTED[ADJ],
          "BEPD03B_QUALIFICATION":EXPECTED[Q03B],"BEPD03C_QUALIFICATION":EXPECTED[Q03C],"BEPD03D_QUALIFICATION":EXPECTED[Q03D]
        },"POLICY_BLOBS")
        eq(manifest["timezone_runtime"],{"zoneinfo_key":"America/New_York","dst_probes_passed":True},"TZ_RUNTIME")

        payload={"repository":manifest["repository"],"branch":manifest["branch"],"head":manifest["head"],"tree":manifest["tree"],
          "source_bepd02_run_id":SOURCE_RUN_ID,"event_ledger_blob":EXPECTED[EVENT],"authorization_blob":EXPECTED[AUTH],
          "implementation_contract_blob":EXPECTED[IMPL],"dimensions_blob":EXPECTED[DIMS],"measurement_contract_blob":EXPECTED[MEASURE],
          "m05_activation_blob":EXPECTED[M05],"calculator_blob":EXPECTED[CALC]}
        eq(canon_hash(payload),manifest["run_id"],"RUN_ID")
        eq(result["run_id"],manifest["run_id"],"RESULT_RUN_ID")
        eq(len(manifest["output_files"]),1,"OUTPUT_COUNT")
        info=manifest["output_files"][0]
        eq(info["relative_path"],"artifacts/bepd03e/event-conditional-take-day-ny-distribution-v0.1/RESULT.json","REL_PATH")
        eq(info["sha256"],sha256_file(out/"RESULT.json"),"RESULT_SHA")
        eq(info["size_bytes"],(out/"RESULT.json").stat().st_size,"RESULT_SIZE")

        print("BEPD_03E_TAKE_DAY_NY_DISTRIBUTION_BREAKER_PASS"); return 0
    except (BF,KeyError,ValueError,json.JSONDecodeError) as exc:
        fail(str(exc))

if __name__=="__main__": sys.exit(main())
