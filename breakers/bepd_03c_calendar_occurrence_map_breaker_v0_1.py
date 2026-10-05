from __future__ import annotations

import argparse, hashlib, json, subprocess, sys
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

AUTH=Path("GOVERNANCE/BEPD-03C-PREREGISTERED-CALENDAR-OCCURRENCE-MAP-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03C-CALENDAR-OCCURRENCE-MAP-IMPLEMENTATION-CONTRACT-V0.1.json")
CALC=Path("tools/bepd_03c_calendar_occurrence_map_v0_1.py")
BC=Path("GOVERNANCE/BEPD-03C-FROZEN-CALENDAR-OCCURRENCE-MAP-BREAKER-CONTRACT-V0.1.json")
DIMS=Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
BASE=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RESULT.json")
BASE_MAN=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RUN_MANIFEST.json")
OPP=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")

EXPECTED={
 AUTH:"6de519f3cfc885819e4147f08e4cc9f6f68d6fbf",
 IMPL:"fc6093a5d3d6fb0029b602657b0464df4cad3bd1",
 CALC:"376d5153181f6ee9bdb63cd4adb8c38724cd0b3d",
 BC:"5065d301d27e466d6cd4ca1ab9295150c224b67a",
 DIMS:"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
 MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
 M05:"53d33074038fa9d971b4672b1d981589da020a1e",
 ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
 BASE:"a2d083b67415b6cb8aa92395d702d1ab558dd4c1",
 BASE_MAN:"98abfece6796ecfb355714c31bcf0126a28729c9",
 OPP:"0e97fb3b45bf8510b8531bb733cc155467a2ce49",
 SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"

class BF(AssertionError): pass
def fail(x:str)->None: print(f"BEPD_03C_BREAKER_FAIL:{x}"); raise SystemExit(1)
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

def read_opp(p:Path)->list[dict[str,Any]]:
    rows=[]
    with p.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            r=json.loads(line)
            req(r["run_id"]==SOURCE_RUN_ID,f"RUN_ID:{n}")
            req(r["dependence_key"]==r["target_week_id"],f"DEP:{n}")
            req(isinstance(r["swept_this_week"],bool),f"BOOL:{n}")
            date.fromisoformat(r["target_week_id"])
            rows.append(r)
    return rows

def prop(e:int,n:int):
    if n==0:return None
    return format((Decimal(e)/Decimal(n)).quantize(Decimal("0.000000000000000001"),rounding=ROUND_HALF_EVEN),"f")

def cell(cat,rows):
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
        eq([x["id"] for x in bc["cases"]],[f"BEPD03C-B{i:02d}" for i in range(1,31)],"CASE_IDS")
        eq(bc["frozen_result_contract"]["m05_generalization_uncertainty"],"BLOCKED","BC_M05")

        eq({p.name for p in out.iterdir()},{"RESULT.json","RUN_MANIFEST.json"},"OUTPUT_SURFACE")
        result=json.loads((out/"RESULT.json").read_text(encoding="utf-8"))
        manifest=json.loads((out/"RUN_MANIFEST.json").read_text(encoding="utf-8"))
        eq(result["interpretation"],"HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_HETEROGENEITY","INTERPRETATION")
        eq(result["m05_generalization_uncertainty"],"BLOCKED","M05")
        eq(result["forbidden_analytics_executed"],False,"FORBIDDEN_FLAG")
        req("OPPORTUNITY ROW != IID OBSERVATION" in result["dependence_statement"],"DEP_STATEMENT")

        rows=read_opp(root/OPP)
        baseline=json.loads((root/BASE).read_text(encoding="utf-8"))
        g=baseline["views"][0]
        eq(result["baseline_reference"]["source_result_blob"],EXPECTED[BASE],"BASE_BLOB")
        for k in ("eligible_target_week_count","unique_level_count","opportunity_count","event_count","occurrence_fraction","occurrence_proportion_decimal"):
            eq(result["baseline_reference"][k],g[k],f"BASE_REF:{k}")

        months=list(range(1,13))
        month_cells=[cell(m,[r for r in rows if date.fromisoformat(r["target_week_id"]).month==m]) for m in months]
        pos_order=["EARLY_01_15","LATE_16_EOM"]
        def pos(r): return "EARLY_01_15" if date.fromisoformat(r["target_week_id"]).day<=15 else "LATE_16_EOM"
        pos_cells=[cell(p,[r for r in rows if pos(r)==p]) for p in pos_order]
        years=sorted({date.fromisoformat(r["target_week_id"]).year for r in rows})
        year_cells=[cell(y,[r for r in rows if date.fromisoformat(r["target_week_id"]).year==y]) for y in years]
        expected_dims=[
          {"dimension_id":"V02_TARGET_MONTH","category_order":months,"cells":month_cells},
          {"dimension_id":"V03_TARGET_MONTH_POSITION","category_order":pos_order,"cells":pos_cells},
          {"dimension_id":"V04_TARGET_YEAR","category_order":years,"cells":year_cells}
        ]
        eq(result["dimensions"],expected_dims,"DIRECT_RECOMPUTATION")
        eq([d["dimension_id"] for d in result["dimensions"]],["V02_TARGET_MONTH","V03_TARGET_MONTH_POSITION","V04_TARGET_YEAR"],"DIM_ORDER")

        for d in result["dimensions"]:
            eq(sum(c["opportunity_count"] for c in d["cells"]),g["opportunity_count"],f"OPP_RECON:{d['dimension_id']}")
            eq(sum(c["event_count"] for c in d["cells"]),g["event_count"],f"EVENT_RECON:{d['dimension_id']}")
            eq(sum(c["eligible_target_week_count"] for c in d["cells"]),g["eligible_target_week_count"],f"WEEK_RECON:{d['dimension_id']}")

        forbidden={"rank","best","worst","p_value","significance","confidence_interval","standard_error","bootstrap","level_age_band","take_day_ny","side_filter","cross_product"}
        def walk(x):
            if isinstance(x,dict):
                for k,v in x.items():
                    req(k.lower() not in forbidden,f"FORBIDDEN_KEY:{k}")
                    walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(result)

        eq(manifest["schema"],"ATDS_BEPD_03C_CALENDAR_OCCURRENCE_MAP_RUN_MANIFEST_V0_1","MAN_SCHEMA")
        eq(manifest["forbidden_analytics_executed"],False,"MAN_FLAG")
        eq(manifest["calculator_blob"],EXPECTED[CALC],"CALC_BLOB")
        eq(manifest["source_bepd02_run_id"],SOURCE_RUN_ID,"SOURCE_RUN")
        eq(manifest["input_git_blobs"],{
          "LEVEL_WEEK_OPPORTUNITY":EXPECTED[OPP],"BEPD03B_RESULT":EXPECTED[BASE],
          "BEPD03B_RUN_MANIFEST":EXPECTED[BASE_MAN],"BEPD02_RUN_MANIFEST":EXPECTED[SOURCE_RUN]},"INPUT_BLOBS")
        eq(manifest["policy_git_blobs"],{
          "BEPD03C_AUTHORIZATION":EXPECTED[AUTH],"BEPD03C_IMPLEMENTATION_CONTRACT":EXPECTED[IMPL],
          "BEPD03A_DIMENSIONS":EXPECTED[DIMS],"BEPD03A_MEASUREMENT_CONTRACT":EXPECTED[MEASURE],
          "BEPD03A_M05_ACTIVATION":EXPECTED[M05],"BEPD03A_ADJUDICATION":EXPECTED[ADJ]},"POLICY_BLOBS")
        payload={"repository":manifest["repository"],"branch":manifest["branch"],"head":manifest["head"],"tree":manifest["tree"],
          "source_bepd02_run_id":SOURCE_RUN_ID,"opportunity_blob":EXPECTED[OPP],"baseline_result_blob":EXPECTED[BASE],
          "authorization_blob":EXPECTED[AUTH],"implementation_contract_blob":EXPECTED[IMPL],"dimensions_blob":EXPECTED[DIMS],
          "measurement_contract_blob":EXPECTED[MEASURE],"m05_activation_blob":EXPECTED[M05],"calculator_blob":EXPECTED[CALC]}
        eq(canon_hash(payload),manifest["run_id"],"RUN_ID")
        eq(result["run_id"],manifest["run_id"],"RESULT_RUN_ID")
        eq(len(manifest["output_files"]),1,"OUTPUT_COUNT")
        info=manifest["output_files"][0]
        eq(info["relative_path"],"artifacts/bepd03c/preregistered-calendar-occurrence-map-v0.1/RESULT.json","REL_PATH")
        eq(info["sha256"],sha256_file(out/"RESULT.json"),"RESULT_SHA")
        eq(info["size_bytes"],(out/"RESULT.json").stat().st_size,"RESULT_SIZE")

        print("BEPD_03C_CALENDAR_OCCURRENCE_MAP_BREAKER_PASS"); return 0
    except (BF,KeyError,ValueError,json.JSONDecodeError) as exc:
        fail(str(exc))

if __name__=="__main__": sys.exit(main())
