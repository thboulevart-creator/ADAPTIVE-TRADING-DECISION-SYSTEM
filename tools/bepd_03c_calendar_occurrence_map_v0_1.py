from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path
from typing import Any

REPOSITORY="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
BRANCH="integration/system-v1"

AUTH=Path("GOVERNANCE/BEPD-03C-PREREGISTERED-CALENDAR-OCCURRENCE-MAP-HUMAN-AUTHORIZATION-2026-10-05.md")
IMPL=Path("GOVERNANCE/BEPD-03C-CALENDAR-OCCURRENCE-MAP-IMPLEMENTATION-CONTRACT-V0.1.json")
DIMS=Path("GOVERNANCE/BEPD-03A-PREREGISTERED-OCCURRENCE-DIMENSIONS-V0.1.json")
MEASURE=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-CONTRACT-V0.1.json")
M05=Path("GOVERNANCE/BEPD-03A-SMF-M05-OCCURRENCE-UNCERTAINTY-ACTIVATION-RECORD-V0.1.json")
ADJ=Path("GOVERNANCE/BEPD-03A-WEEKLY-LIQUIDITY-OCCURRENCE-MEASUREMENT-HUMAN-ADJUDICATION-2026-10-05.md")
BASELINE_RESULT=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RESULT.json")
BASELINE_MANIFEST=Path("artifacts/bepd03b/global-weekly-liquidity-occurrence-baseline-v0.1/RUN_MANIFEST.json")
OPP=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/LEVEL_WEEK_OPPORTUNITY.jsonl")
SOURCE_RUN=Path("artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/RUN_MANIFEST.json")
SELF=Path("tools/bepd_03c_calendar_occurrence_map_v0_1.py")

EXPECTED_BLOBS={
 AUTH:"6de519f3cfc885819e4147f08e4cc9f6f68d6fbf",
 IMPL:"fc6093a5d3d6fb0029b602657b0464df4cad3bd1",
 DIMS:"b7ec6a00e3d2281217c30e11d21527b5ce72aef6",
 MEASURE:"e117ddea324dd1b6906bc9eadcf8a5806b8b591a",
 M05:"53d33074038fa9d971b4672b1d981589da020a1e",
 ADJ:"b796fd69a9b40c0397cc89db5be755d59974b1fe",
 BASELINE_RESULT:"a2d083b67415b6cb8aa92395d702d1ab558dd4c1",
 BASELINE_MANIFEST:"98abfece6796ecfb355714c31bcf0126a28729c9",
 OPP:"0e97fb3b45bf8510b8531bb733cc155467a2ce49",
 SOURCE_RUN:"ccd5e31e1aeeadb4cceee24a8b8cd5eb0f8cf6d5",
}
SOURCE_RUN_ID="68d858ffcb6cde1941cd16b73ad0590ef4ae9a9528fb3a2c82099fca5a33a821"
OUTPUT_SUBDIR=Path("artifacts/bepd03c/preregistered-calendar-occurrence-map-v0.1")


class CalendarFailure(RuntimeError):
    pass


def fail(code:str)->None:
    raise CalendarFailure(code)


def git_text(root:Path,*args:str)->str:
    cp=subprocess.run(["git","-C",str(root),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=False)
    if cp.returncode!=0:
        fail(f"GIT_COMMAND_FAILED:{' '.join(args)}:{cp.stderr.strip()}")
    return cp.stdout.strip()


def git_blob(root:Path,rel:Path)->str:
    return git_text(root,"rev-parse",f"HEAD:{rel.as_posix()}")


def canonical_hash(payload:dict[str,Any])->str:
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def verify_bindings(root:Path)->None:
    for rel,expected in EXPECTED_BLOBS.items():
        actual=git_blob(root,rel)
        if actual!=expected:
            fail(f"GIT_BINDING_MISMATCH:{rel.as_posix()}:{actual}:{expected}")


def read_opportunities(path:Path)->list[dict[str,Any]]:
    required={"run_id","level_id","target_week_id","dependence_key","side","level_age_weeks","swept_this_week","event_id","active_level_count_at_target_week_start"}
    rows=[]
    with path.open("r",encoding="utf-8") as f:
        for n,line in enumerate(f,1):
            row=json.loads(line)
            if set(row)!=required:
                fail(f"OPPORTUNITY_SCHEMA_DRIFT:{n}")
            if row["run_id"]!=SOURCE_RUN_ID:
                fail(f"SOURCE_RUN_ID_DRIFT:{n}")
            if row["dependence_key"]!=row["target_week_id"]:
                fail(f"DEPENDENCE_KEY_DRIFT:{n}")
            if not isinstance(row["swept_this_week"],bool):
                fail(f"SWEEP_NOT_BOOL:{n}")
            if row["swept_this_week"]!=(row["event_id"] is not None):
                fail(f"EVENT_FLAG_DRIFT:{n}")
            date.fromisoformat(row["target_week_id"])
            rows.append(row)
    if not rows:
        fail("EMPTY_OPPORTUNITY_LEDGER")
    return rows


def prop(events:int,opportunities:int)->str|None:
    if opportunities==0:
        return None
    v=(Decimal(events)/Decimal(opportunities)).quantize(Decimal("0.000000000000000001"),rounding=ROUND_HALF_EVEN)
    return format(v,"f")


def make_cell(category:Any,rows:list[dict[str,Any]])->dict[str,Any]:
    events=sum(1 for r in rows if r["swept_this_week"])
    n=len(rows)
    return {
      "category":category,
      "eligible_target_week_count":len({r["target_week_id"] for r in rows}),
      "unique_level_count":len({r["level_id"] for r in rows}),
      "opportunity_count":n,
      "event_count":events,
      "occurrence_fraction":f"{events}/{n}" if n else "0/0",
      "occurrence_proportion_decimal":prop(events,n),
    }


def global_baseline(baseline:dict[str,Any])->dict[str,Any]:
    views=baseline.get("views",[])
    if [v.get("view_id") for v in views] != ["GLOBAL_ALL_SIDES","HIGH","LOW"]:
        fail("BASELINE_VIEW_ORDER_DRIFT")
    g=views[0]
    return {
      "eligible_target_week_count":g["eligible_target_week_count"],
      "unique_level_count":g["unique_level_count"],
      "opportunity_count":g["opportunity_count"],
      "event_count":g["event_count"],
      "occurrence_fraction":g["occurrence_fraction"],
      "occurrence_proportion_decimal":g["occurrence_proportion_decimal"],
    }


def reconcile(cells:list[dict[str,Any]],rows:list[dict[str,Any]],baseline:dict[str,Any],label:str)->None:
    if sum(c["opportunity_count"] for c in cells)!=baseline["opportunity_count"]:
        fail(f"{label}_OPPORTUNITY_RECONCILIATION")
    if sum(c["event_count"] for c in cells)!=baseline["event_count"]:
        fail(f"{label}_EVENT_RECONCILIATION")
    weeks=set()
    for r in rows:
        weeks.add(r["target_week_id"])
    if sum(c["eligible_target_week_count"] for c in cells)!=len(weeks):
        fail(f"{label}_TARGET_WEEK_RECONCILIATION")


def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,required=True)
    parser.add_argument("--output-dir",type=Path,default=None)
    args=parser.parse_args()
    root=args.root.resolve()
    out=(args.output_dir or (root/OUTPUT_SUBDIR)).resolve()

    try:
        verify_bindings(root)
        calculator_blob=git_blob(root,SELF)
        head=git_text(root,"rev-parse","HEAD")
        tree=git_text(root,"rev-parse","HEAD^{tree}")

        baseline=json.loads((root/BASELINE_RESULT).read_text(encoding="utf-8"))
        if baseline.get("interpretation")!="HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_PROPORTION":
            fail("BASELINE_INTERPRETATION_DRIFT")
        if baseline.get("m05_generalization_uncertainty")!="BLOCKED":
            fail("BASELINE_M05_DRIFT")
        base=global_baseline(baseline)

        rows=read_opportunities(root/OPP)
        if len(rows)!=base["opportunity_count"]:
            fail("BASELINE_SOURCE_ROW_COUNT_DRIFT")
        if sum(1 for r in rows if r["swept_this_week"])!=base["event_count"]:
            fail("BASELINE_SOURCE_EVENT_COUNT_DRIFT")

        if out.exists():
            if any(out.iterdir()):
                fail(f"OUTPUT_DIR_NOT_EMPTY:{out}")
        else:
            out.mkdir(parents=True,exist_ok=False)

        months=list(range(1,13))
        month_cells=[make_cell(m,[r for r in rows if date.fromisoformat(r["target_week_id"]).month==m]) for m in months]

        pos_order=["EARLY_01_15","LATE_16_EOM"]
        def pos(r:dict[str,Any])->str:
            return "EARLY_01_15" if date.fromisoformat(r["target_week_id"]).day<=15 else "LATE_16_EOM"
        pos_cells=[make_cell(p,[r for r in rows if pos(r)==p]) for p in pos_order]

        years=sorted({date.fromisoformat(r["target_week_id"]).year for r in rows})
        year_cells=[make_cell(y,[r for r in rows if date.fromisoformat(r["target_week_id"]).year==y]) for y in years]

        reconcile(month_cells,rows,base,"MONTH")
        reconcile(pos_cells,rows,base,"MONTH_POSITION")
        reconcile(year_cells,rows,base,"YEAR")

        run_payload={
          "repository":REPOSITORY,
          "branch":BRANCH,
          "head":head,
          "tree":tree,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "opportunity_blob":EXPECTED_BLOBS[OPP],
          "baseline_result_blob":EXPECTED_BLOBS[BASELINE_RESULT],
          "authorization_blob":EXPECTED_BLOBS[AUTH],
          "implementation_contract_blob":EXPECTED_BLOBS[IMPL],
          "dimensions_blob":EXPECTED_BLOBS[DIMS],
          "measurement_contract_blob":EXPECTED_BLOBS[MEASURE],
          "m05_activation_blob":EXPECTED_BLOBS[M05],
          "calculator_blob":calculator_blob,
        }
        run_id=canonical_hash(run_payload)

        result={
          "schema":"ATDS_BEPD_03C_PREREGISTERED_CALENDAR_OCCURRENCE_MAP_RESULT_V0_1",
          "interpretation":"HISTORICAL_FIXED_CORPUS_DESCRIPTIVE_HETEROGENEITY",
          "run_id":run_id,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "baseline_reference":{
            "source_result_blob":EXPECTED_BLOBS[BASELINE_RESULT],
            **base
          },
          "dependence_statement":"OPPORTUNITY ROW != IID OBSERVATION; dependence_key=target_week_id; multiple active levels in one target week are structurally dependent",
          "m05_generalization_uncertainty":"BLOCKED",
          "dimensions":[
            {"dimension_id":"V02_TARGET_MONTH","category_order":months,"cells":month_cells},
            {"dimension_id":"V03_TARGET_MONTH_POSITION","category_order":pos_order,"cells":pos_cells},
            {"dimension_id":"V04_TARGET_YEAR","category_order":years,"cells":year_cells},
          ],
          "forbidden_analytics_executed":False,
        }

        result_path=out/"RESULT.json"
        result_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        manifest={
          "schema":"ATDS_BEPD_03C_CALENDAR_OCCURRENCE_MAP_RUN_MANIFEST_V0_1",
          "repository":REPOSITORY,
          "branch":BRANCH,
          "head":head,
          "tree":tree,
          "run_id":run_id,
          "source_bepd02_run_id":SOURCE_RUN_ID,
          "input_git_blobs":{
            "LEVEL_WEEK_OPPORTUNITY":EXPECTED_BLOBS[OPP],
            "BEPD03B_RESULT":EXPECTED_BLOBS[BASELINE_RESULT],
            "BEPD03B_RUN_MANIFEST":EXPECTED_BLOBS[BASELINE_MANIFEST],
            "BEPD02_RUN_MANIFEST":EXPECTED_BLOBS[SOURCE_RUN],
          },
          "policy_git_blobs":{
            "BEPD03C_AUTHORIZATION":EXPECTED_BLOBS[AUTH],
            "BEPD03C_IMPLEMENTATION_CONTRACT":EXPECTED_BLOBS[IMPL],
            "BEPD03A_DIMENSIONS":EXPECTED_BLOBS[DIMS],
            "BEPD03A_MEASUREMENT_CONTRACT":EXPECTED_BLOBS[MEASURE],
            "BEPD03A_M05_ACTIVATION":EXPECTED_BLOBS[M05],
            "BEPD03A_ADJUDICATION":EXPECTED_BLOBS[ADJ],
          },
          "calculator_blob":calculator_blob,
          "output_files":[{
            "relative_path":result_path.relative_to(root).as_posix(),
            "sha256":sha256_file(result_path),
            "size_bytes":result_path.stat().st_size,
          }],
          "forbidden_analytics_executed":False,
        }
        manifest_path=out/"RUN_MANIFEST.json"
        manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")

        print(json.dumps({
          "status":"BEPD03C_CALENDAR_OCCURRENCE_MAP_COMPLETE",
          "run_id":run_id,
          "result_sha256":sha256_file(result_path),
          "manifest_sha256":sha256_file(manifest_path),
          "month_cell_count":len(month_cells),
          "month_position_cell_count":len(pos_cells),
          "year_cell_count":len(year_cells)
        },sort_keys=True))
        return 0
    except CalendarFailure as exc:
        print(f"BEPD03C_CALENDAR_FAIL:{exc}")
        return 1


if __name__=="__main__":
    raise SystemExit(main())
