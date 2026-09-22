#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"evidence"/"bpesem"/"registry"/"bpesem03r_berd02_lineage_registry_v0_1.json"
OUT=ROOT/"evidence"/"bpesem03r"
REPORT=Path(os.environ.get("BPESEM03R_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem03r_lineage_registration_adversarial_break_2026-09-22.md")))

RUNNER_PATH="tools/berd02_transport_runner.py"
RUNNER_BLOB="e10a0c47ec6e9b28f480c958baf18141287187cb"
HIST_SOURCE_HEAD="2eb8350fb24c3043017c91475d202b5e0d6bb501"
HIST_EXECUTION_ID="BERD02-GHA-35533153289-1"
OLD_FAIL_REPORT="reports/data-qualification/bpesem03_operational_semantic_adjudication_final_rebreak_2026-09-21.md"
OLD_FAIL_BLOB="cc2679fccee0470d40c5c2d6ace26797664d6e73"
OLD_ADJ_PATH="evidence/bpesem03/operational_semantic_rule_adjudication_v0_1.json"
OLD_ADJ_BLOB="3da0aebd8bcf3c10fa9545c4d091c4c047f99bd4"
TARGET_CLAIMS=["BPE-SEM-C01-OP","BPE-SEM-C02-OP","BPE-SEM-C03-OP","BPE-SEM-C07-OP"]
TARGET_DIMS=[
    "C01-D1-OP","C01-D2-OP","C01-D3-OP",
    "C02-D1-OP","C02-D2-OP","C02-D3-OP","C02-D4-OP",
    "C03-D1-OP","C03-D2-OP","C03-D4-OP","C07-D2-OP",
]
REF_RE=re.compile(r"(?:evidence|reports|04-REFERENCE|src|tools|breakers|[.]github)/[A-Za-z0-9_./-]+")

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=json.loads(json.dumps(o))
    x.pop(field,None)
    return digest(x)

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def blob(path:str)->str:
    return git("hash-object",path)

def readj(path:Path|str)->dict[str,Any]:
    p=ROOT/path if isinstance(path,str) else path
    return json.loads(p.read_text(encoding="utf-8"))

head=git("rev-parse","HEAD")
registry=readj(REG)
baseline=readj(OUT/"governed_semantic_evidence_baseline_v0_1.json")
horizon=readj(OUT/"semantic_evidence_horizon_v0_1.json")
adj=readj(OUT/"operational_semantic_rule_adjudication_v0_1.json")
delta=readj(OUT/"current_authority_evidence_delta_review_v0_1.json")
old=readj(OLD_ADJ_PATH)
hist=readj("evidence/bpesem03/historical_observation_eligibility_v0_1.json")
exec_result=readj("evidence/berd02/gha_run_35533153289/execution_result.json")

attacks=[]
defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond:
        defects.append(name)

items=registry.get("registered_items",[])
item=items[0] if len(items)==1 else {}

check("R01_EXACT_PATH_BLOB",
      len(items)==1 and item.get("artifact_path")==RUNNER_PATH and item.get("artifact_git_blob")==RUNNER_BLOB and blob(RUNNER_PATH)==RUNNER_BLOB,
      "registry binds exact current runner path/blob")

tree_has=subprocess.run(["git","cat-file","-e",HIST_SOURCE_HEAD+":"+RUNNER_PATH],cwd=ROOT,check=False).returncode==0
source_blob=git("rev-parse",HIST_SOURCE_HEAD+":"+RUNNER_PATH) if tree_has else ""
check("R02_GOVERNED_HEAD_AND_HISTORICAL_BLOB",
      source_blob==RUNNER_BLOB,
      "same runner blob exists at historical B-ERD-02 source HEAD")

check("R03_LINEAGE_ROLE_ONLY",
      item.get("artifact_role")=="LINEAGE_EVIDENCE" and item.get("positive_authority_eligible") is False and item.get("independent_semantic_source") is False,
      "LINEAGE_EVIDENCE cannot escalate to positive/independent authority")

check("R04_PROJECT_ORIGIN_FIREWALL",
      item.get("project_origin_status")=="PROJECT_ORIGIN_EXECUTION_MECHANISM",
      "runner remains project-origin execution mechanism")

check("R05_HISTORICAL_IDENTITY",
      item.get("historical_source_head")==HIST_SOURCE_HEAD and item.get("historical_execution_id")==HIST_EXECUTION_ID,
      "registry binds exact historical source HEAD and execution")

source_time=git("show","-s","--format=%cI",HIST_SOURCE_HEAD)
obs_time=exec_result["created_at_utc"]
source_dt=dt.datetime.fromisoformat(source_time.replace("Z","+00:00"))
obs_dt=dt.datetime.fromisoformat(obs_time.replace("Z","+00:00"))
check("R06_PREOBSERVATION_ORDER",
      source_dt < obs_dt and exec_result["source_head"]==HIST_SOURCE_HEAD,
      "runner identity/source commit predates observed execution")

check("R07_EXACT_DIMENSION_SCOPE",
      sorted(item.get("target_dimension_ids",[]))==sorted(TARGET_DIMS) and sorted(item.get("target_claim_ids",[]))==sorted(TARGET_CLAIMS),
      "registration limited to exact 11 dimensions / 4 claims")

hist_records=[r for r in hist["records"] if RUNNER_PATH in r["pre_observation_artifact_refs"]]
check("R08_NONDECISIVE_COMPATIBILITY",
      len(hist_records)==11 and all(r["eligibility_role"]=="NONDECISIVE_COMPATIBILITY" and r["decisive_discrimination_eligible"] is False for r in hist_records)
      and item.get("historical_observation_role")=="NONDECISIVE_COMPATIBILITY"
      and item.get("decisive_semantic_discrimination_eligible") is False,
      "historical reuse remains nondecisive compatibility")

check("R09_NO_POSTHOC_DISCRIMINATION",
      item.get("post_hoc_semantic_discrimination_eligible") is False
      and all(r["post_hoc_broadening_check"]=="EXACT_C01_C07_HYPOTHESIS_IDENTITY_NOT_PRECOMMITTED" for r in hist_records),
      "no post-hoc exact C01-C07 discrimination")

hmap={x["path"]:x["git_blob"] for x in horizon["discovered_semantic_artifact_refs"]}
registry_rel=str(REG.relative_to(ROOT))
check("R10_REGISTRY_AND_RUNNER_IN_HORIZON",
      hmap.get(RUNNER_PATH)==RUNNER_BLOB and hmap.get(registry_rel)==blob(registry_rel),
      "fresh horizon contains registry and exact runner")

runner_refs=set(REF_RE.findall((ROOT/RUNNER_PATH).read_text(encoding="utf-8")))
check("R11_REFERENCE_CLOSURE_CLOSED",
      all(r in hmap for r in runner_refs),
      "runner repository references are all included in fresh horizon")

check("R12_DELTA_CLOSED",
      delta["status"]=="PASS" and delta.get("unresolved_paths")==[],
      "successor exact delta review has no unresolved artifact")

check("R13_OLD_FAIL_IMMUTABLE",
      blob(OLD_FAIL_REPORT)==OLD_FAIL_BLOB and blob(OLD_ADJ_PATH)==OLD_ADJ_BLOB
      and adj["prior_bpesem03_final_verdict"]["overall"]=="FAIL"
      and adj["prior_bpesem03_final_verdict"]["preserved_unchanged"] is True,
      "B-PE-SEM-03 final FAIL remains unchanged historical authority")

old_dims={x["dimension_id"]:x["status"] for x in old["dimension_adjudications"]}
new_dims={x["dimension_id"]:x["status"] for x in adj["dimension_adjudications"]}
check("R14_NO_SEMANTIC_PROMOTION",
      old_dims==new_dims and old["claim_adjudications"]==adj["claim_adjudications"]
      and old["overall_operational_semantic_status"]==adj["overall_operational_semantic_status"]=="BLOCKED",
      "registration alone changes no semantic proposition status")

serialized=json.dumps(adj,sort_keys=True)
check("R15_NO_C08_LEAKAGE",
      "BPE-SEM-C08" not in serialized and adj["lineage_registration_resolution"]["artifact_role"]=="LINEAGE_EVIDENCE",
      "no C01-C07/C08 authority leakage")

check("R16_REGISTRY_SEAL",
      registry["registry_digest"]==seal(registry,"registry_digest"),
      "registry digest canonical and valid")

check("R17_HORIZON_AND_BASELINE_SEALS",
      baseline["baseline_digest"]==seal(baseline,"baseline_digest")
      and horizon["horizon_digest"]==seal(horizon,"horizon_digest"),
      "fresh baseline/horizon seals valid")

check("R18_ADJUDICATION_SEAL",
      adj["adjudication_seal"]==seal(adj,"adjudication_seal"),
      "successor adjudication seal valid")

check("R19_RUNNER_NOT_POSITIVE_AUTHORITY",
      RUNNER_PATH not in json.dumps(old.get("positive_authority_universe_ids",[]))
      and item.get("positive_authority_eligible") is False,
      "runner cannot become positive authority")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=[
    "# B-PE-SEM-03R — LINEAGE REGISTRATION / FRESH HORIZON — ADVERSARIAL BREAK",
    "",
    "Persisted candidate HEAD attacked: "+head,
    "",
    "Candidate adversarial verdict: "+verdict,
    "",
]
for name,status,detail in attacks:
    lines += ["## "+name,"",status+" — "+detail,""]
lines += [
    "## Result","",
    "~~~text",
    "attack count = "+str(len(attacks)),
    "demonstrated defects = "+str(len(defects)),
    *(defects or ["NONE"]),
    "~~~","",
    "No provider contact, BI5 GET, FULL_INTERVAL, D materialization or backtest occurred.","",
    "STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":head,"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))
