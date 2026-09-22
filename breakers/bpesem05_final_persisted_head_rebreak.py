#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05"
QUAL=E/"lane_s_qualification_v0_1.json"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05_final_persisted_head_rebreak_2026-09-22.md"

CANDIDATE_COMMIT="b98ce80cd1a19940e24880dd3a8836bfb5ea83d8"

PROTECTED={
"evidence/bpesem05/lane_s_evidence_registry_v0_1.json":"8251c744cd9f0c3758be8f49979bd2ba42b69ca1",
"evidence/bpesem05/source_lineage_resolution_v0_1.json":"e19a76fe02e7546dcf15857b1a50bccdaa4efa44",
"evidence/bpesem05/provider_primary_semantic_anchor_set_v0_1.json":"bac24b40519c16f050e01e619fed60dff261ccfd",
"evidence/bpesem05/provider_instrument_scale_authority_v0_1.json":"14c02cd77503915d70e4090735e733dbe2c14e7e",
"evidence/bpesem05/provider_semantic_change_point_inventory_v0_1.json":"0cb9b2ddd6911dd09920fb66ec1d5d91a9f51327",
"evidence/bpesem05/semantic_epoch_manifest_v0_1.json":"e463a44e1bd142fb0a0ba0ca5dfab98b47a2ff77",
"evidence/bpesem05/independent_corroboration_register_v0_1.json":"cb8c4cf17f5c74e37876a1da648b98db05666164",
"evidence/bpesem05/contradiction_sweep_result_v0_1.json":"02d1bcd3ee56e5057db07e2b66d69f9445385ff7",
"evidence/bpesem05/lane_s_scope_applicability_decision_v0_1.json":"7251a267620b3e66edc950832dfa5b728d27bfb5",
"evidence/bpesem05/lane_s_semantic_authority_result_v0_1.json":"2d4d73a929310615f0860486d8a4e0095abc536d",
"evidence/bpesem05/current_evidence_horizon_v0_1.json":"961868bfacfef6891af07e56b83ce54d953574a7",
"reports/data-qualification/bpesem05_lane_s_candidate_2026-09-22.md":"2e80980ddad60d9c35b7cc8cc42bcf9e0badf60d",
"reports/data-qualification/bpesem05_lane_s_adversarial_break_2026-09-22.md":"2f1968cfb4a3832c746d4b553c7c3ccf9bfa2d6d",
}

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None); return digest(x)
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
    if blob(p)!=b: defects.append("PROTECTED_BLOB::"+p)

ancestry=subprocess.run(["git","merge-base","--is-ancestor",CANDIDATE_COMMIT,HEAD],cwd=ROOT,check=False).returncode==0
if not ancestry: defects.append("CANDIDATE_NOT_ANCESTOR")

env=dict(os.environ)
env["BPESEM05_BREAK_REPORT"]="/tmp/bpesem05-final-regression.md"
cp=subprocess.run(["python3","breakers/bpesem05_lane_s_breaker.py"],cwd=ROOT,text=True,capture_output=True,env=env,check=False)
if cp.returncode!=0:
    raise RuntimeError(cp.stdout+"\n"+cp.stderr)
regression=json.loads(cp.stdout)
if not (regression.get("verdict")=="PASS" and regression.get("attack_count")==30 and regression.get("defects")==[]):
    defects.append("FULL_BREAKER_REGRESSION")

raw=git("diff","--name-status",CANDIDATE_COMMIT+".."+HEAD)
changes=[]; unresolved=[]
for line in raw.splitlines():
    if not line.strip(): continue
    parts=line.split("\t")
    status=parts[0]; path=parts[-1]
    if path in PROTECTED:
        disposition="PROTECTED_EXPECTED_IDENTITY"
    elif path=="breakers/bpesem05_final_persisted_head_rebreak.py":
        disposition="FINAL_REBREAK_GOVERNANCE"
    elif path==".github/workflows/bpesem05-final-rebreak.yml":
        disposition="FINAL_REBREAK_WORKFLOW"
    elif path.startswith("reports/data-qualification/bpesem05_"):
        disposition="BPESEM05_GOVERNANCE_REPORT"
    elif path.startswith("breakers/bpesem05_"):
        disposition="BPESEM05_BREAKER_GOVERNANCE"
    elif path.startswith(".github/workflows/bpesem05-"):
        disposition="BPESEM05_WORKFLOW_GOVERNANCE"
    else:
        disposition="BLOCKED_UNRESOLVED_CHANGE"
        unresolved.append(path)
    changes.append({"status":status,"path":path,"disposition":disposition})
if unresolved: defects.append("POST_CANDIDATE_CHANGESET_UNRESOLVED")

result=readj("evidence/bpesem05/lane_s_semantic_authority_result_v0_1.json")
epoch=readj("evidence/bpesem05/semantic_epoch_manifest_v0_1.json")
scope=readj("evidence/bpesem05/lane_s_scope_applicability_decision_v0_1.json")
registry=readj("evidence/bpesem05/lane_s_evidence_registry_v0_1.json")

if result["lane_s_overall_status"]!="BLOCKED": defects.append("LANE_S_NOT_BLOCKED")
if result["dimension_promotions_to_pass"]!=[]: defects.append("UNAUTHORIZED_DIMENSION_PROMOTION")
if result["registered_target_proposition_failures"]!=[]: defects.append("UNSUPPORTED_FAIL")
if result["lane_p_request_manifest_authorized"] is not False: defects.append("REQUEST_MANIFEST_UNAUTHORIZED_STATE")
if epoch["full_authoritative_coverage"] is not False or epoch["request_manifest_derivation_authorized"] is not False:
    defects.append("EPOCH_FAIL_CLOSED_VIOLATION")
if scope["blocked_count"]!=24 or scope["pass_count"]!=0 or scope["fail_count"]!=0:
    defects.append("SCOPE_POPULATION_DRIFT")
if not (registry["no_provider_object_bytes_observed"] is True and registry["no_bi5_get_performed"] is True):
    defects.append("PROVIDER_OBJECT_BOUNDARY_VIOLATION")

package_integrity="PASS" if not defects else "FAIL"
governed_result="BLOCKED" if package_integrity=="PASS" and result["lane_s_overall_status"]=="BLOCKED" else "FAIL"

qualification={
 "schema":"BPESEM05_LANE_S_QUALIFICATION_V0_1",
 "candidate_commit":CANDIDATE_COMMIT,
 "reviewed_persisted_head":HEAD,
 "reviewed_persisted_tree":TREE,
 "protected_artifact_blobs":PROTECTED,
 "candidate_ancestry":"PASS" if ancestry else "FAIL",
 "full_breaker_regression":regression,
 "post_candidate_changes":changes,
 "unresolved_post_candidate_paths":unresolved,
 "package_integrity_status":package_integrity,
 "lane_s_semantic_authority_status":result["lane_s_overall_status"],
 "target_epoch_status":epoch["overall_status"],
 "scope_status":scope["overall_status"],
 "dimension_promotions":result["dimension_promotions_to_pass"],
 "registered_target_proposition_failures":result["registered_target_proposition_failures"],
 "lane_p_request_manifest_authorized":result["lane_p_request_manifest_authorized"],
 "provider_object_observation_performed":False,
 "overall_governed_result":governed_result,
 "demonstrated_final_defects":defects,
 "created_at_utc":"2026-09-22T15:45:00Z"
}
qualification["qualification_seal"]=seal(qualification,"qualification_seal")
QUAL.write_text(json.dumps(qualification,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

lines=[
"# B-PE-SEM-05 — FINAL PERSISTED-HEAD RE-BREAK","",
"Persisted HEAD attacked: "+HEAD,
"Persisted tree attacked: "+TREE,"",
"## Regression","",
"~~~text",
"candidate ancestor = "+("PASS" if ancestry else "FAIL"),
"breaker verdict = "+str(regression.get("verdict")),
"breaker attacks = "+str(regression.get("attack_count")),
"breaker defects = "+str(len(regression.get("defects",[]))),
"post-candidate changed paths = "+str(len(changes)),
"unresolved changed paths = "+str(len(unresolved)),
"~~~","",
"## Final governed result","",
"~~~text",
"package materialization/adjudication integrity = "+package_integrity,
"Lane S semantic authority = "+result["lane_s_overall_status"],
"target epoch = "+epoch["overall_status"],
"scope = "+scope["overall_status"],
"dimension promotions = "+str(len(result["dimension_promotions_to_pass"])),
"registered target proposition failures = "+str(len(result["registered_target_proposition_failures"])),
"Lane P RequestManifest authorized = NO",
"B-PE-SEM-05 = "+governed_result,
"demonstrated final defects = "+str(len(defects)),
*(defects or ["NONE"]),
"qualification seal = "+qualification["qualification_seal"],
"~~~","",
"BLOCKED is substantive and intentional: the package is sound, but provider-primary exact legacy-hourly K1 semantics, native USATECH raw scale authority, and exhaustive target-epoch continuity remain unproven.","",
"No provider BI5 object was requested or observed. No Lane P RequestManifest/P-DIAG, FULL_INTERVAL, D or backtest was authorized or executed.","","STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

print(json.dumps({
 "head":HEAD,
 "package_integrity_status":package_integrity,
 "lane_s_status":result["lane_s_overall_status"],
 "overall_governed_result":governed_result,
 "attack_count":regression.get("attack_count"),
 "unresolved_changes":unresolved,
 "defects":defects,
 "qualification_seal":qualification["qualification_seal"]
},indent=2))
