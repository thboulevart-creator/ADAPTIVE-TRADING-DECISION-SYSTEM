#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
CONTRACT="evidence/bpesem05r02/provider_primary_authority_inquiry_contract_v0_1.json"
CANDIDATE_REPORT="reports/data-qualification/bpesem05r02_inquiry_contract_candidate_2026-09-22.md"
BREAK_REPORT="reports/data-qualification/bpesem05r02_inquiry_contract_adversarial_break_2026-09-22.md"
QUAL=ROOT/"evidence"/"bpesem05r02"/"inquiry_contract_qualification_v0_1.json"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r02_final_persisted_head_rebreak_2026-09-22.md"

CANDIDATE_COMMIT="c5c39707c07ca60b0fb6a7475ab3d0426d6e45a7"
PROTECTED={
 CONTRACT:"3eeb079b834102a2c8983563bd21088ad50796ed",
 CANDIDATE_REPORT:"4c4115556bdf513f87d2d7c4633841ac51c472b5",
 BREAK_REPORT:"94d190231d46f5849a106efdae908ed4f7d1c471",
}

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None)
    return hashlib.sha256(canon(x)).hexdigest()
def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def blob(path:str)->str:
    return git("hash-object",path)

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")
defects=[]

for p,b in PROTECTED.items():
    if blob(p)!=b:
        defects.append("PROTECTED_BLOB::"+p)

ancestor=subprocess.run(["git","merge-base","--is-ancestor",CANDIDATE_COMMIT,HEAD],cwd=ROOT,check=False).returncode==0
if not ancestor:
    defects.append("CANDIDATE_NOT_ANCESTOR")

env=dict(os.environ)
env["BPESEM05R02_BREAK_REPORT"]="/tmp/bpesem05r02-final-regression.md"
cp=subprocess.run(["python3","breakers/bpesem05r02_inquiry_contract_breaker.py"],cwd=ROOT,text=True,capture_output=True,env=env,check=False)
if cp.returncode!=0:
    raise RuntimeError(cp.stdout+"\n"+cp.stderr)
reg=json.loads(cp.stdout)
if not (reg.get("verdict")=="PASS" and reg.get("attack_count")==36 and reg.get("defects")==[]):
    defects.append("FULL_BREAKER_REGRESSION")

raw=git("diff","--name-status",CANDIDATE_COMMIT+".."+HEAD)
changes=[]; unresolved=[]
for line in raw.splitlines():
    if not line.strip(): continue
    parts=line.split("\t")
    status=parts[0]; path=parts[-1]
    if path in PROTECTED:
        disposition="PROTECTED_EXPECTED_IDENTITY"
    elif path=="breakers/bpesem05r02_final_persisted_head_rebreak.py":
        disposition="FINAL_REBREAK_GOVERNANCE"
    elif path==".github/workflows/bpesem05r02-final-rebreak.yml":
        disposition="FINAL_REBREAK_WORKFLOW"
    elif path.startswith("reports/data-qualification/bpesem05r02_"):
        disposition="BPESEM05R02_GOVERNANCE_REPORT"
    elif path.startswith("breakers/bpesem05r02_"):
        disposition="BPESEM05R02_BREAKER_GOVERNANCE"
    elif path.startswith(".github/workflows/bpesem05r02-"):
        disposition="BPESEM05R02_WORKFLOW_GOVERNANCE"
    else:
        disposition="BLOCKED_UNRESOLVED_CHANGE"
        unresolved.append(path)
    changes.append({"status":status,"path":path,"disposition":disposition})
if unresolved:
    defects.append("POST_CANDIDATE_CHANGESET_UNRESOLVED")

c=json.loads((ROOT/CONTRACT).read_text(encoding="utf-8"))
if c["contract_seal"]!=seal(c,"contract_seal"):
    defects.append("CONTRACT_SEAL_DRIFT")
if c["preserved_recovery_state"]!={"A":"AMBIGUOUS","B":"NOT_FOUND","C":"INCOMPLETE_VERSION_COVERAGE"}:
    defects.append("RECOVERY_STATE_DRIFT")
if c["contact_channel_policy"]["contact_authorized_by_this_contract"] is not False:
    defects.append("CONTACT_AUTHORIZATION_DRIFT")
if not all(v is False for v in c["execution_boundary"].values()):
    defects.append("EXECUTION_BOUNDARY_VIOLATION")
qe=c["qualification_effect"]
if not (qe["contract_pass_does_not_recover_A_B_C"] is True
        and qe["contract_pass_does_not_authorize_contact"] is True
        and qe["contact_requires_separate_governed_consumer_block"] is True
        and qe["lane_s_authority_effect"]=="NONE"
        and qe["lane_p_authority_effect"]=="NONE"):
    defects.append("QUALIFICATION_EFFECT_DRIFT")

package_integrity="PASS" if not defects else "FAIL"
contract_qualification="PASS" if package_integrity=="PASS" else "FAIL"

qualification={
 "schema":"BPESEM05R02_INQUIRY_CONTRACT_QUALIFICATION_V0_1",
 "candidate_commit":CANDIDATE_COMMIT,
 "reviewed_persisted_head":HEAD,
 "reviewed_persisted_tree":TREE,
 "protected_candidate_blobs":PROTECTED,
 "candidate_ancestry":"PASS" if ancestor else "FAIL",
 "full_adversarial_break":reg,
 "post_candidate_changes":changes,
 "unresolved_post_candidate_paths":unresolved,
 "package_integrity_status":package_integrity,
 "contract_qualification_status":contract_qualification,
 "preserved_recovery_state":c["preserved_recovery_state"],
 "provider_contact_authorized":False,
 "provider_contact_performed":False,
 "provider_inquiry_sent":False,
 "lane_s_authority_effect":"NONE",
 "lane_p_authority_effect":"NONE",
 "demonstrated_final_defects":defects,
 "created_at_utc":"2026-09-22T17:54:00Z"
}
qualification["qualification_seal"]=seal(qualification,"qualification_seal")
QUAL.write_text(json.dumps(qualification,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

lines=[
"# B-PE-SEM-05R-02 — FINAL PERSISTED-HEAD RE-BREAK","",
"Persisted HEAD attacked: "+HEAD,
"Persisted tree attacked: "+TREE,"",
"## Candidate / breaker","",
"~~~text",
"candidate commit = "+CANDIDATE_COMMIT,
"candidate ancestor = "+("PASS" if ancestor else "FAIL"),
"breaker verdict = "+str(reg.get("verdict")),
"breaker attacks = "+str(reg.get("attack_count")),
"breaker defects = "+str(len(reg.get("defects",[]))),
"post-candidate changed paths = "+str(len(changes)),
"unresolved changed paths = "+str(len(unresolved)),
"~~~","",
"## Contract qualification","",
"~~~text",
"package integrity = "+package_integrity,
"inquiry contract qualification = "+contract_qualification,
"A preserved = AMBIGUOUS",
"B preserved = NOT_FOUND",
"C preserved = INCOMPLETE_VERSION_COVERAGE",
"provider contact authorized = NO",
"provider contact performed = NO",
"provider inquiry sent = NO",
"Lane S authority effect = NONE",
"Lane P authority effect = NONE",
"demonstrated final defects = "+str(len(defects)),
*(defects or ["NONE"]),
"qualification seal = "+qualification["qualification_seal"],
"~~~","",
"A PASS here qualifies only the pre-contact inquiry contract. It does not recover A/B/C and does not authorize sending the inquiry.","",
"No provider contact, new documentary acquisition, provider BI5 object, Lane S re-adjudication, Lane P artifact, FULL_INTERVAL, D or backtest occurred.","","STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({
 "head":HEAD,
 "package_integrity_status":package_integrity,
 "contract_qualification_status":contract_qualification,
 "attack_count":reg.get("attack_count"),
 "unresolved_changes":unresolved,
 "defects":defects,
 "qualification_seal":qualification["qualification_seal"]
},indent=2))
