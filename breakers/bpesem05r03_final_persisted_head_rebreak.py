#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
QUAL=ROOT/"evidence"/"bpesem05r03"/"channel_resolution_qualification_v0_1.json"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r03_final_persisted_head_rebreak_2026-09-22.md"

CANDIDATE_COMMIT="8c048e1317190827e4275852c9f35da73193b2e2"

PROTECTED={
"evidence/bpesem05r03/provider_contact_channel_inventory_v0_1.json":"d74a27b21bce53cb03e3013f53232da6932bea0f",
"evidence/bpesem05r03/provider_channel_ownership_evidence_v0_1.json":"31a14ba369bd2997612ebf2c633fa88a90f8ede4",
"evidence/bpesem05r03/provider_channel_identity_binding_v0_1.json":"cb8156fb5ec979e8e70a6176cd17f3a5c58e8145",
"evidence/bpesem05r03/channel_constraint_manifest_v0_1.json":"990efdac538c73401385df11d30c29c47b4b36d7",
"evidence/bpesem05r03/channel_authentication_requirement_v0_1.json":"68ece14c16817e47b82d144b34fff2708811a78a",
"evidence/bpesem05r03/outbound_capability_constraints_v0_1.json":"6e357c11d99bfe0ef1142a7bf6211e40e7237803",
"evidence/bpesem05r03/channel_resolution_decision_v0_1.json":"cb8156fb5ec979e8e70a6176cd17f3a5c58e8145",
"evidence/bpesem05r03/current_channel_evidence_horizon_v0_1.json":"1dbaaa2306240e36b58eaecce5fe0d80e8fa6b90",
"evidence/bpesem05r03/no_contact_execution_attestation_v0_1.json":"2724e1bf69feb921024a8c185785ee30d4b84548",
"reports/data-qualification/bpesem05r03_channel_resolution_candidate_2026-09-22.md":"2ba43ad3bd08df83592eead72be61aff15719d93",
"reports/data-qualification/bpesem05r03_channel_resolution_adversarial_break_2026-09-22.md":"e6f7c3af33b2c80fa32706f3366f13fbf7672337",
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
def readj(path:str)->dict:
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

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
env["BPESEM05R03_BREAK_REPORT"]="/tmp/bpesem05r03-final-regression.md"
cp=subprocess.run(["python3","breakers/bpesem05r03_channel_resolution_breaker.py"],cwd=ROOT,text=True,capture_output=True,env=env,check=False)
if cp.returncode!=0:
    raise RuntimeError(cp.stdout+"\n"+cp.stderr)
reg=json.loads(cp.stdout)
if not (reg.get("verdict")=="PASS" and reg.get("attack_count")==34 and reg.get("defects")==[]):
    defects.append("FULL_BREAKER_REGRESSION")

raw=git("diff","--name-status",CANDIDATE_COMMIT+".."+HEAD)
changes=[]; unresolved=[]
for line in raw.splitlines():
    if not line.strip():
        continue
    parts=line.split("\t")
    status=parts[0]; path=parts[-1]
    if path in PROTECTED:
        disposition="PROTECTED_EXPECTED_IDENTITY"
    elif path=="breakers/bpesem05r03_final_persisted_head_rebreak.py":
        disposition="FINAL_REBREAK_GOVERNANCE"
    elif path==".github/workflows/bpesem05r03-final-rebreak.yml":
        disposition="FINAL_REBREAK_WORKFLOW"
    elif path.startswith("reports/data-qualification/bpesem05r03_"):
        disposition="BPESEM05R03_GOVERNANCE_REPORT"
    elif path.startswith("breakers/bpesem05r03_"):
        disposition="BPESEM05R03_BREAKER_GOVERNANCE"
    elif path.startswith(".github/workflows/bpesem05r03-"):
        disposition="BPESEM05R03_WORKFLOW_GOVERNANCE"
    else:
        disposition="BLOCKED_UNRESOLVED_CHANGE"
        unresolved.append(path)
    changes.append({"status":status,"path":path,"disposition":disposition})
if unresolved:
    defects.append("POST_CANDIDATE_CHANGESET_UNRESOLVED")

decision=readj("evidence/bpesem05r03/channel_resolution_decision_v0_1.json")
constraints=readj("evidence/bpesem05r03/channel_constraint_manifest_v0_1.json")
horizon=readj("evidence/bpesem05r03/current_channel_evidence_horizon_v0_1.json")
attest=readj("evidence/bpesem05r03/no_contact_execution_attestation_v0_1.json")

if decision["result"]!="OFFICIAL_PROVIDER_CHANNEL_BOUND":
    defects.append("CHANNEL_RESULT_DRIFT")
if decision["selected_channel"]["endpoint"]!="https://www.dukascopy.com/plugins/contactForm/?b=swiss&id=contact&lang=en&mob=0":
    defects.append("ENDPOINT_DRIFT")
if decision["selected_channel"]["topic_value"]!="3":
    defects.append("TOPIC_DRIFT")
if decision["contact_authorized"] is not False or decision["contact_performed"] is not False or decision["send_authorized"] is not False:
    defects.append("CONTACT_BOUNDARY_DRIFT")
if decision["outbound_package_materialization_authorized_next"] is not True:
    defects.append("STAGE_P_EFFECT_DRIFT")
if constraints["required_fields"]["clear_details"]["required"] is not True:
    defects.append("BODY_FIELD_DRIFT")
if horizon["overall_status"]!="OFFICIAL_PROVIDER_CHANNEL_BOUND":
    defects.append("HORIZON_STATUS_DRIFT")
if not all(v is False for v in attest.values() if isinstance(v,bool)):
    defects.append("NO_CONTACT_ATTESTATION_VIOLATION")

package_integrity="PASS" if not defects else "FAIL"
qualification_status="PASS" if package_integrity=="PASS" else "FAIL"

qualification={
 "schema":"BPESEM05R03_CHANNEL_RESOLUTION_QUALIFICATION_V0_1",
 "candidate_commit":CANDIDATE_COMMIT,
 "reviewed_persisted_head":HEAD,
 "reviewed_persisted_tree":TREE,
 "protected_candidate_blobs":PROTECTED,
 "candidate_ancestry":"PASS" if ancestor else "FAIL",
 "full_adversarial_break":reg,
 "post_candidate_changes":changes,
 "unresolved_post_candidate_paths":unresolved,
 "package_integrity_status":package_integrity,
 "channel_resolution_status":qualification_status,
 "selected_channel":decision["selected_channel"],
 "provider_contact_authorized":False,
 "provider_contact_performed":False,
 "provider_inquiry_sent":False,
 "outbound_package_materialization_authorized_next":decision["outbound_package_materialization_authorized_next"],
 "lane_s_authority_effect":"NONE",
 "lane_p_authority_effect":"NONE",
 "demonstrated_final_defects":defects,
 "created_at_utc":"2026-09-22T19:24:00Z"
}
qualification["qualification_seal"]=seal(qualification,"qualification_seal")
QUAL.write_text(json.dumps(qualification,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

lines=[
"# B-PE-SEM-05R-03 — FINAL PERSISTED-HEAD RE-BREAK","",
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
"## Channel qualification","",
"~~~text",
"package integrity = "+package_integrity,
"channel resolution qualification = "+qualification_status,
"selected channel = GENERAL_CONTACT_FORM",
"endpoint = https://www.dukascopy.com/plugins/contactForm/?b=swiss&id=contact&lang=en&mob=0",
"topic = 3 / Live trading support. Technical support",
"provider contact authorized = NO",
"provider contact performed = NO",
"provider inquiry sent = NO",
"outbound package materialization authorized next = YES",
"Lane S authority effect = NONE",
"Lane P authority effect = NONE",
"demonstrated final defects = "+str(len(defects)),
*(defects or ["NONE"]),
"qualification seal = "+qualification["qualification_seal"],
"~~~","",
"A PASS here qualifies only official provider channel resolution. It does not authorize contact or send.","",
"No form submission, email, support ticket, inquiry, provider BI5 object, Lane S re-adjudication or Lane P work occurred.","","STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

print(json.dumps({
 "head":HEAD,
 "package_integrity_status":package_integrity,
 "channel_resolution_status":qualification_status,
 "attack_count":reg.get("attack_count"),
 "unresolved_changes":unresolved,
 "defects":defects,
 "qualification_seal":qualification["qualification_seal"]
},indent=2))
