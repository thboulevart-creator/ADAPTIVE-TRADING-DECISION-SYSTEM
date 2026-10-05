from __future__ import annotations

import argparse, hashlib, json, subprocess, sys
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

AUTH=Path("GOVERNANCE/BEPD-03D-LEVEL-AGE-OCCURRENCE-MAP-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03D-LEVEL-AGE-OCCURRENCE-MAP-IMPLEMENTATION-CONTRACT-V0.1.json")
CALC=Path("tools/bepd_03d_level_age_occurrence_map_v0_1.py")
BC=Path("GOVERNANCE/BEPD-03D-FROZEN-LEVEL-AGE-OCCURRENCE-MAP-BREAKER-CONTRACT-V0.1.json")
DIMS=Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
BASE=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RESULT.json")
BASE_MAN=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RUN_MANIFEST.json")
CALENDAR=Path("artifacts/bepd03c/preregistered-calendar-occurrence-map-v0.1/RESULT.json")
CALENDAR_MAN=Path("artifacts/bepd03c/preregistered-calendar-occurrence-map-v0.1/RUN_MANIFEST.json")
OPP=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")

EXPECTED={
 AUTH:"4bbcc78cf8e74bcb5fcd96bc51b60921ed82e2b0",
 IMPL:"ee9464c167954367591654514c7cb0596be7340b",
 CALC:"d3cbad6e744fd9a6029561824a9618c2751de4a7",
 BC:"b24f70dceec8fe51cc8ef2c46b2178dcd56b46cd",
 DIMS:"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
 MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
 M05:"53d33074038fa9d971b4672b1d981589da020a1e",
 ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
 BASE:"a2d083b67415b6cb8aa92395d702d1ab558dd4c1",
 BASE_MAN:"98abfece6796ecfb355714c31bcf0126a28729c9",
 CALENDAR:"809fa76f82bbbe0311a6c538378eed2a22c77fe0",
 CALENDAR_MAN:"02acd5a81808119c9bb3896f4be34ca977eb3839",
 OPP:"0e97fb3b45bf8510b8531bb733cc155467a2ce49",
 SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
AGE_ORDER=["AGE_1","AGE_2","AGE_3_4","AGE_5_8","AGE_9_16","AGE_17_32","AGE_33_64","AGE_65_PLUS"]

class BF(AssertionError): pass
def fail(x:str)->None: print(f"BEPD_03D_BREAKER_FAIL:{x}"); raise SystemExit(1)
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

def age_band(age:Any)->str:
    if isinstance(age,bool) or not isinstance(age,int): raise BF(f"INVALID_AGE_TYPE:{age!r}")
    if age<=0: raise BF(f"NON_POSITIVE_AGE:{age}")
    if age==1:return "AGE_1"
    if age==2:return "AGE_2"
    if age<=4:return "AGE_3_4"
    if age<=8:return "AGE_5_8"
    if age<=16:return "AGE_9_16"
    if age<=32:return "AGE_17_32"
    if age<=64:return "AGE_33_64"
    return "AGE_65_PLUS"

def read_opp(p:Path)->list[dict[str,Any]]:
    rows=[]
    required={"run_id","level_id","target_week_id","dependence_key","side","level_age_weeks","swept_this_week","event_id","active_level_count_at_target_week_start"}
    with p.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            r=json.loads(line)
            eq(set(r),required,f"SCHEMA:{n}")
            eq(r["run_id"],SOURCE_RUN_ID,f"RUN_ID:{n}")
            eq(r["dependence_key"],r["target_week_id"],f"DEP:{n}")
            req(isinstance(r["swept_this_week"],bool),f"BOOL:{n}")
            eq(r["swept_this_week"],r["event_id"] is not None,f"EVENT_FLAG:{n}")
            age_band(r["level_age_weeks"])
            rows.append(r)
    req(bool(rows),"EMPTY_OPPORTUNITY_LEDGER")
    return rows

def prop(e:int,n:int):
    if n==0:return None
    return format((Decimal(e)/Decimal(n)).quantize(Decimal("0.000000000000000001"),rounding=ROUND_HALF_EVEN),"f")

def cell(cat:str,rows:list[dict[str,Any]])->dict[str,Any]:
    e=sum(1 for r in rows if r["swept_this_week"])
    n=len(rows)
    return {"category":cat,"eligible_target_week_count":len({r["target_week_id"] for r in rows}),
            "unique_level_count":len({r["level_id"] for r in rows}),"opportunity_count":n,"event_count":e,
            "occurrence_fraction":f"{e}/{n}" if n else "0/0","occurrence_proportion_decimal":prop(e,n)}

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--root",type=Path,required=True); ap.add_argument("--result-dir",type=Path,required=True); a=ap.parse_args()
    root=a.root.resolve(); out=a.result_dir.resolve()
    try:
        for p,s in EXPECTED.items(): eq(git_blob(root,p),s,f"BLOB:{p}")
        bc=json.loads((root/BC).read_text(encoding="utf-8"))
        impl=json.loads((root/IMPL).read_text(encoding="utf-8"))
        eq([x["id"] for x in bc["cases"]],[f"BEPD03D-B{i:02d}" for i in range(1,31)],"CASE_IDS")
        eq(bc["frozen_result_contract"]["age_order"],AGE_ORDER,"BC_AGE_ORDER")
        eq(bc["frozen_result_contract"]["m05_generalization_uncertainty"],"BLOCKED","BC_M05")
        eq(impl["baseline_reconciliation"]["target_week_counts_are_not_additive"],True,"WEEK_NONADDITIVE")
        eq(impl["baseline_reconciliation"]["unique_level_counts_are_not_additive"],True,"LEVEL_NONADDITIVE")

        # Synthetic boundary checks, independent of market values.
        boundary_expect={
          1:"AGE_1",2:"AGE_2",3:"AGE_3_4",4:"AGE_3_4",5:"AGE_5_8",8:"AGE_5_8",
          9:"AGE_9_16",16:"AGE_9_16",17:"AGE_17_32",32:"AGE_17_32",
          33:"AGE_33_64",64:"AGE_33_64",65:"AGE_65_PLUS",130:"AGE_65_PLUS"
        }
        for age,expected in boundary_expect.items(): eq(age_band(age),expected,f"BOUNDARY:{age}")
        for bad in (0,-1):
            try: age_band(bad); raise BF(f"NON_POSITIVE_ACCEPTED:{bad}")
            except BF as exc:
                if str(exc).startswith("NON_POSITIVE_ACCEPTED"): raise
        try: age_band(1.5); raise BF("NON_INTEGER_ACCEPTED")
        except BF as exc:
            if str(exc)=="NON_INTEGER_ACCEPTED": raise

        eq({p.name for p in out.iterdir()},{"RESULT.json","RUN_MANIFEST.json"},"OUTPUT_SURFACE")
        result=json.loads((out/"RESULT.json").read_text(encoding="utf-8"))
        manifest=json.loads((out/"RUN_MANIFEST.json").read_text(encoding="utf-8"))

        result_fields={"schema","interpretation","run_id","source_bepd02_run_id","baseline_reference","calendar_reference_identity","dependence_statement","m05_generalization_uncertainty","dimension","forbidden_analytics_executed"}
        eq(set(result),result_fields,"RESULT_FIELDS")
        eq(result["schema"],"ATDS_BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_RESULT_V0_1","RESULT_SCHEMA")
        eq(result["interpretation"],"HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_AGE_HETEROGENEITY","INTERPRETATION")
        eq(result["m05_generalization_uncertainty"],"BLOCKED","M05")
        eq(result["forbidden_analytics_executed"],False,"FORBIDDEN_FLAG")
        req("OPPORTUNITY ROW != IID OBSERVATION" in result["dependence_statement"],"DEP_STATEMENT")
        req("temporal repeated measure" in result["dependence_statement"],"REPEATED_MEASURE_STATEMENT")

        baseline=json.loads((root/BASE).read_text(encoding="utf-8"))
        g=baseline["views"][0]
        eq(result["baseline_reference"]["source_result_blob"],EXPECTED[BASE],"BASE_BLOB")
        for k in ("eligible_target_week_count","unique_level_count","opportunity_count","event_count","occurrence_fraction","occurrence_proportion_decimal"):
            eq(result["baseline_reference"][k],g[k],f"BASE_REF:{k}")
        eq(result["calendar_reference_identity"],{"source_result_blob":EXPECTED[CALENDAR],"use":"IDENTITY_ONLY_NOT_CROSSED_WITH_AGE"},"CALENDAR_IDENTITY")

        rows=read_opp(root/OPP)
        expected_cells=[cell(label,[r for r in rows if age_band(r["level_age_weeks"])==label]) for label in AGE_ORDER]
        dim=result["dimension"]
        eq(set(dim),{"dimension_id","category_order","cells"},"DIM_FIELDS")
        eq(dim["dimension_id"],"V05_LEVEL_AGE_BAND","DIM_ID")
        eq(dim["category_order"],AGE_ORDER,"AGE_ORDER")
        eq(dim["cells"],expected_cells,"DIRECT_RECOMPUTATION")

        eq(sum(c["opportunity_count"] for c in expected_cells),g["opportunity_count"],"OPP_RECON")
        eq(sum(c["event_count"] for c in expected_cells),g["event_count"],"EVENT_RECON")
        source_weeks={r["target_week_id"] for r in rows}
        source_levels={r["level_id"] for r in rows}
        union_weeks=set(); union_levels=set()
        for label in AGE_ORDER:
            xs=[r for r in rows if age_band(r["level_age_weeks"])==label]
            union_weeks|={r["target_week_id"] for r in xs}
            union_levels|={r["level_id"] for r in xs}
        eq(union_weeks,source_weeks,"TARGET_WEEK_UNION")
        eq(union_levels,source_levels,"LEVEL_UNION")

        cell_fields={"category","eligible_target_week_count","unique_level_count","opportunity_count","event_count","occurrence_fraction","occurrence_proportion_decimal"}
        for c in dim["cells"]: eq(set(c),cell_fields,f"CELL_FIELDS:{c.get('category')}")

        forbidden={"rank","best","worst","p_value","significance","confidence_interval","standard_error","bootstrap","target_month","target_year","target_month_position","take_day_ny","side_filter","cross_product"}
        def walk(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    req(k.lower() not in forbidden,f"FORBIDDEN_KEY:{k}")
                    walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(result)

        manifest_fields={"schema","repository","branch","head","tree","run_id","source_bepd02_run_id","input_git_blobs","policy_git_blobs","calculator_blob","output_files","forbidden_analytics_executed"}
        eq(set(manifest),manifest_fields,"MANIFEST_FIELDS")
        eq(manifest["schema"],"ATDS_BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_RUN_MANIFEST_V0_1","MANIFEST_SCHEMA")
        eq(manifest["forbidden_analytics_executed"],False,"MAN_FLAG")
        eq(manifest["calculator_blob"],EXPECTED[CALC],"CALC_BLOB")
        eq(manifest["source_bepd02_run_id"],SOURCE_RUN_ID,"SOURCE_RUN")
        eq(manifest["input_git_blobs"],{
          "LEVEL_WEEK_OPPORTUNITY":EXPECTED[OPP],"BEPD03B_RESULT":EXPECTED[BASE],
          "BEPD03B_RUN_MANIFEST":EXPECTED[BASE_MAN],"BEPD03C_RESULT":EXPECTED[CALENDAR],
          "BEPD03C_RUN_MANIFEST":EXPECTED[CALENDAR_MAN],"BEPD02_RUN_MANIFEST":EXPECTED[SOURCE_RUN]},"INPUT_BLOBS")
        eq(manifest["policy_git_blobs"],{
          "BEPD03D_AUTHORIZATION":EXPECTED[AUTH],"BEPD03D_IMPLEMENTATION_CONTRACT":EXPECTED[IMPL],
          "BEPD03A_DIMENSIONS":EXPECTED[DIMS],"BEPD03A_MEASUREMENT_CONTRACT":EXPECTED[MEASURE],
          "BEPD03A_M05_ACTIVATION":EXPECTED[M05],"BEPD03A_ADJUDICATION":EXPECTED[ADJ]},"POLICY_BLOBS")
        payload={"repository":manifest["repository"],"branch":manifest["branch"],"head":manifest["head"],"tree":manifest["tree"],
          "source_bepd02_run_id":SOURCE_RUN_ID,"opportunity_blob":EXPECTED[OPP],"baseline_result_blob":EXPECTED[BASE],
          "calendar_result_blob":EXPECTED[CALENDAR],"authorization_blob":EXPECTED[AUTH],
          "implementation_contract_blob":EXPECTED[IMPL],"dimensions_blob":EXPECTED[DIMS],
          "measurement_contract_blob":EXPECTED[MEASURE],"m05_activation_blob":EXPECTED[M05],"calculator_blob":EXPECTED[CALC]}
        eq(canon_hash(payload),manifest["run_id"],"RUN_ID")
        eq(result["run_id"],manifest["run_id"],"RESULT_RUN_ID")
        eq(len(manifest["output_files"]),1,"OUTPUT_COUNT")
        info=manifest["output_files"][0]
        eq(info["relative_path"],"artifacts/bepd03d/level-age-occurrence-map-v0.1/RESULT.json","REL_PATH")
        eq(info["sha256"],sha256_file(out/"RESULT.json"),"RESULT_SHA")
        eq(info["size_bytes"],(out/"RESULT.json").stat().st_size,"RESULT_SIZE")

        print("BEPD_03D_LEVEL_AGE_OCCURRENCE_MAP_BREAKER_PASS"); return 0
    except (BF,KeyError,ValueError,json.JSONDecodeError) as exc:
        fail(str(exc))

if __name__=="__main__": sys.exit(main())
