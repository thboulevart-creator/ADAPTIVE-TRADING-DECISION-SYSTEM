#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
CONTRACT_PATH="evidence/bpesem04/prospective_semantic_authority_closure_contract_v0_1.json"
CANDIDATE_REPORT="reports/data-qualification/bpesem04_prospective_semantic_authority_closure_contract_candidate_2026-09-22.md"
BREAK_REPORT="reports/data-qualification/bpesem04_prospective_semantic_authority_contract_adversarial_break_2026-09-22.md"
QUAL_PATH=ROOT/"evidence"/"bpesem04"/"contract_qualification_v0_1.json"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem04_final_persisted_head_rebreak_2026-09-22.md"

CANDIDATE_COMMIT="7507e6603c711e8a8b33ec361fa871e7d0428a6b"
EXPECTED_CONTRACT_BLOB="fe0ca12e12624371be28ea8c09340691466a37ce"
EXPECTED_CANDIDATE_REPORT_BLOB="75f8a00e2d98882e99e9e905432913759a967bfa"
EXPECTED_BREAK_REPORT_BLOB="da5da7309a440393de2a66205774e4374beb7475"
EXPECTED_ROUTE_BLOB="ba8687735cd48f81bb654d33117d957447707783"
EXPECTED_PRIOR_ADJ_BLOB="d26655e3806b36305252fda186ccf4d08e38084b"
EXPECTED_PRIOR_CLOSEOUT_BLOB="acd90221fc97d816bec8d30e5c421aa89947e994"
EXPECTED_SCOPE_BLOB="80c47551707b8d36c04fd8b3f4003e93dfecaf37"
EXPECTED_BASIS_BLOB="b67abaf9468689855b7f362264a1fd801f9f12a8"
EXPECTED_INTERVAL_BLOB="8c02972228941d8b6f1aacaf9ac6bf75fb0f2029"

PROTECTED={
    CONTRACT_PATH:EXPECTED_CONTRACT_BLOB,
    CANDIDATE_REPORT:EXPECTED_CANDIDATE_REPORT_BLOB,
    "reports/data-qualification/post_bpesem03r_semantic_authority_closure_route_selection_2026-09-22.md":EXPECTED_ROUTE_BLOB,
    "evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json":EXPECTED_PRIOR_ADJ_BLOB,
    "reports/data-qualification/bpesem03r_final_closeout_2026-09-22.md":EXPECTED_PRIOR_CLOSEOUT_BLOB,
    "evidence/bpesem03/operational_semantic_scope_signature_v0_1.json":EXPECTED_SCOPE_BLOB,
    "evidence/bpesem03/dimension_authority_basis_register_v0_1.json":EXPECTED_BASIS_BLOB,
    "evidence/bfiq02/interval_inventory_v0_1.json":EXPECTED_INTERVAL_BLOB,
}

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None); return digest(x)

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def blob(path:str)->str:
    return git("hash-object",path)

def readj(path:str)->dict[str,Any]:
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")

defects=[]
def chk(name:str,cond:bool):
    if not cond:
        defects.append(name)

# Exact candidate and governed-input identity.
for p,b in PROTECTED.items():
    chk("PROTECTED_BLOB::"+p,blob(p)==b)
chk("BREAK_REPORT_BLOB",blob(BREAK_REPORT)==EXPECTED_BREAK_REPORT_BLOB)

# Candidate commit must remain an ancestor.
ancestry=subprocess.run(["git","merge-base","--is-ancestor",CANDIDATE_COMMIT,HEAD],cwd=ROOT,check=False).returncode==0
chk("CANDIDATE_ANCESTRY",ancestry)

# Full corrected breaker regression on unchanged candidate.
env=dict(os.environ)
env["BPESEM04_BREAK_REPORT"]="/tmp/bpesem04-final-break-regression.md"
cp=subprocess.run(["python3","breakers/bpesem04_contract_breaker.py"],cwd=ROOT,text=True,capture_output=True,env=env,check=False)
if cp.returncode!=0:
    raise RuntimeError("contract breaker execution error: "+cp.stdout+"\n"+cp.stderr)
pre=json.loads(cp.stdout)
chk("FULL_BREAKER_PASS",pre.get("verdict")=="PASS" and pre.get("attack_count")==30 and pre.get("defects")==[])

# Review every Git path changed since candidate persistence.
raw=subprocess.check_output(["git","diff","--name-status",CANDIDATE_COMMIT+".."+HEAD],cwd=ROOT,text=True)
changes=[]
unresolved=[]
for line in raw.splitlines():
    if not line.strip():
        continue
    parts=line.split("\t")
    status=parts[0]
    path=parts[-1]
    if path in PROTECTED:
        disp="PROTECTED_UNCHANGED"
    elif path==BREAK_REPORT:
        disp="ADVERSARIAL_REPORT_ONLY"
    elif path.startswith("breakers/bpesem04_"):
        disp="BPESEM04_BREAKER_GOVERNANCE"
    elif path.startswith(".github/workflows/bpesem04-"):
        disp="BPESEM04_WORKFLOW_GOVERNANCE"
    elif path.startswith("reports/data-qualification/bpesem04_"):
        disp="BPESEM04_GOVERNANCE_REPORT"
    else:
        disp="BLOCKED_UNRESOLVED_CHANGE"
        unresolved.append(path)
    changes.append({"status":status,"path":path,"disposition":disp})

chk("POST_CANDIDATE_CHANGESET_CLOSED",not unresolved)

contract=readj(CONTRACT_PATH)
chk("CONTRACT_SEAL_CURRENT",contract["contract_seal"]==seal(contract,"contract_seal"))
chk("CONTRACT_NO_NETWORK_AUTHORIZATION",all(v is False for k,v in contract["execution_boundary"].items() if k.startswith("this_contract_authorizes_")))
chk("SEMANTIC_AUTHORITY_NOT_PROMOTED",contract["prior_bpesem03r"]["semantic_authority"]=="BLOCKED")
chk("C08_NOT_TARGETED",all("C08" not in x for x in (
    contract["dimension_population"]["already_pass"]
    +contract["dimension_population"]["blocked_physical_hypothesis"]
    +contract["dimension_population"]["blocked_semantic_anchor"]
    +contract["dimension_population"]["blocked_prerequisite_closure"]
)))

qualification_status="PASS" if not defects else "FAIL"
qualification={
    "schema":"B_PE_SEM_04_CONTRACT_QUALIFICATION_V0_1",
    "contract_id":contract["contract_id"],
    "contract_version":contract["contract_version"],
    "contract_path":CONTRACT_PATH,
    "contract_git_blob":EXPECTED_CONTRACT_BLOB,
    "contract_seal":contract["contract_seal"],
    "candidate_commit":CANDIDATE_COMMIT,
    "reviewed_persisted_head":HEAD,
    "reviewed_persisted_tree":TREE,
    "candidate_ancestor_status":"PASS" if ancestry else "FAIL",
    "full_adversarial_break":{"verdict":pre.get("verdict"),"attack_count":pre.get("attack_count"),"defects":pre.get("defects")},
    "post_candidate_changes":changes,
    "unresolved_post_candidate_paths":unresolved,
    "semantic_authority_effect":"NONE; C01-C07 remains BLOCKED pending future qualified evidence",
    "execution_authorization_effect":"NONE",
    "qualification_status":qualification_status,
    "demonstrated_final_defects":defects,
    "created_at_utc":"2026-09-22T11:45:00Z",
}
qualification["qualification_seal"]=seal(qualification,"qualification_seal")
QUAL_PATH.parent.mkdir(parents=True,exist_ok=True)
QUAL_PATH.write_text(json.dumps(qualification,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

lines=[
"# B-PE-SEM-04 — FINAL PERSISTED-HEAD RE-BREAK",
"",
"Persisted HEAD attacked: "+HEAD,
"Persisted tree attacked: "+TREE,
"",
"## Candidate identity",
"",
"~~~text",
"candidate commit = "+CANDIDATE_COMMIT,
"contract blob = "+EXPECTED_CONTRACT_BLOB,
"candidate report blob = "+EXPECTED_CANDIDATE_REPORT_BLOB,
"corrected adversarial report blob = "+EXPECTED_BREAK_REPORT_BLOB,
"contract seal = "+contract["contract_seal"],
"~~~",
"",
"## Full adversarial regression",
"",
"~~~text",
"verdict = "+str(pre.get("verdict")),
"attack count = "+str(pre.get("attack_count")),
"defects = "+str(len(pre.get("defects",[]))),
"~~~",
"",
"## Post-candidate persisted change review",
"",
"~~~text",
"candidate ancestor = "+("PASS" if ancestry else "FAIL"),
"changed paths reviewed = "+str(len(changes)),
"unresolved changed paths = "+str(len(unresolved)),
"~~~",
"",
"## Final result",
"",
"~~~text",
"B-PE-SEM-04 contract qualification = "+qualification_status,
"C01-C07 semantic authority effect = NONE / remains BLOCKED",
"provider/network acquisition authorization = NONE",
"demonstrated final defects = "+str(len(defects)),
*(defects or ["NONE"]),
"qualification seal = "+qualification["qualification_seal"],
"~~~",
"",
"A contract PASS means only that the prospective evidence rules are qualified before observation. It is not evidence that any blocked C01-C07 proposition is true.",
"",
"No provider contact, provider BI5 GET, new provider-object acquisition, semantic-discrimination execution, FULL_INTERVAL, D materialization or backtest occurred.",
"",
"STOP."
]
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

print(json.dumps({
    "head":HEAD,
    "breaker_verdict":pre.get("verdict"),
    "attack_count":pre.get("attack_count"),
    "post_candidate_changes":len(changes),
    "unresolved_changes":unresolved,
    "qualification_status":qualification_status,
    "defects":defects,
    "qualification_seal":qualification["qualification_seal"],
},indent=2))
