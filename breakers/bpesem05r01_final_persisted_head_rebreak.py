#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05r01"
QUAL=E/"recovery_qualification_v0_1.json"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r01_final_persisted_head_rebreak_2026-09-22.md"

CANDIDATE_COMMIT="b98a011e21f539c10d3064b30513efc9817bedf4"
PROTECTED={
"evidence/bpesem05r01/provider_artifact_inventory_v0_1.json":"a022e1c16b363477cec4de71a830dd1255992471",
"evidence/bpesem05r01/provider_artifact_identity_registry_composite_v0_1.json":"aacc0b10e9f06d18119e318d4048a59caa53f77e",
"evidence/bpesem05r01/relevant_class_resource_inventory_composite_v0_1.json":"c8916f5fd3dfcc0a33f2ab6313d9119d85a47076",
"evidence/bpesem05r01/artifact_lineage_resolution_v0_1.json":"6c6285c2c37f643b2078a4e592e4603651fe829c",
"evidence/bpesem05r01/legacy_hourly_semantic_artifact_finding_v0_1.json":"43f6b95945b71e7beb70b2cd86a242e8a2e5a0cd",
"evidence/bpesem05r01/usatech_raw_scale_artifact_finding_v0_1.json":"fff29d789223dca2690d01b0918ee1527156e253",
"evidence/bpesem05r01/cross_version_semantic_change_ledger_v0_1.json":"9d1638b8391e259796e798c7fcfbfde4292ebc81",
"evidence/bpesem05r01/jetta_change_impact_finding_v0_1.json":"b83bb700ba9a4381dbc3d9b0a9253135d3f59ca7",
"evidence/bpesem05r01/recovery_a_result_v0_1.json":"945873c2d0f7504eb866ad524d4dc03995b41c84",
"evidence/bpesem05r01/recovery_b_result_v0_1.json":"d5e4d05090ca684775457b363ed0b0de5fbed48d",
"evidence/bpesem05r01/recovery_c_result_v0_1.json":"c1db014e9f7e4fafa80a9db3142d6e02c7659357",
"evidence/bpesem05r01/documentary_evidence_horizon_v0_1.json":"b9fb63bb9ecb729223fe4c40789d01ba321d62b1",
"evidence/bpesem05r01/no_market_data_observation_attestation_v0_1.json":"49430b7ae0994068988b842ac2583ab949e53321",
"evidence/bpesem05r01/recovery_package_result_v0_1.json":"ab3ccfb4bdd7da1d93511b0d0523b70f974f2908",
"reports/data-qualification/bpesem05r01_recovery_candidate_2026-09-22.md":"4567f710b7af4b116e35e76569c01a4fb1c7ca08",
"reports/data-qualification/bpesem05r01_recovery_adversarial_break_2026-09-22.md":"dce384f248153f4a7407bc1a3239f5e0f5d4e442",
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
    if blob(p)!=b:
        defects.append("PROTECTED_BLOB::"+p)

ancestry=subprocess.run(["git","merge-base","--is-ancestor",CANDIDATE_COMMIT,HEAD],cwd=ROOT,check=False).returncode==0
if not ancestry:
    defects.append("CANDIDATE_NOT_ANCESTOR")

env=dict(os.environ)
env["BPESEM05R01_BREAK_REPORT"]="/tmp/bpesem05r01-final-regression.md"
cp=subprocess.run(["python3","breakers/bpesem05r01_recovery_breaker.py"],cwd=ROOT,text=True,capture_output=True,env=env,check=False)
if cp.returncode!=0:
    raise RuntimeError(cp.stdout+"\n"+cp.stderr)
reg=json.loads(cp.stdout)
if not (reg.get("verdict")=="PASS" and reg.get("attack_count")==30 and reg.get("defects")==[]):
    defects.append("FULL_BREAKER_REGRESSION")

raw=git("diff","--name-status",CANDIDATE_COMMIT+".."+HEAD)
changes=[]; unresolved=[]
for line in raw.splitlines():
    if not line.strip(): continue
    parts=line.split("\t")
    status=parts[0]; path=parts[-1]
    if path in PROTECTED:
        disposition="PROTECTED_EXPECTED_IDENTITY"
    elif path=="breakers/bpesem05r01_final_persisted_head_rebreak.py":
        disposition="FINAL_REBREAK_GOVERNANCE"
    elif path==".github/workflows/bpesem05r01-final-rebreak.yml":
        disposition="FINAL_REBREAK_WORKFLOW"
    elif path.startswith("breakers/bpesem05r01_"):
        disposition="RECOVERY_BREAKER_GOVERNANCE"
    elif path.startswith(".github/workflows/bpesem05r01-"):
        disposition="RECOVERY_WORKFLOW_GOVERNANCE"
    elif path.startswith("reports/data-qualification/bpesem05r01_"):
        disposition="RECOVERY_GOVERNANCE_REPORT"
    else:
        disposition="BLOCKED_UNRESOLVED_CHANGE"
        unresolved.append(path)
    changes.append({"status":status,"path":path,"disposition":disposition})
if unresolved:
    defects.append("POST_CANDIDATE_CHANGESET_UNRESOLVED")

overall=readj("evidence/bpesem05r01/recovery_package_result_v0_1.json")
ra=readj("evidence/bpesem05r01/recovery_a_result_v0_1.json")
rb=readj("evidence/bpesem05r01/recovery_b_result_v0_1.json")
rc=readj("evidence/bpesem05r01/recovery_c_result_v0_1.json")
horizon=readj("evidence/bpesem05r01/documentary_evidence_horizon_v0_1.json")
att=readj("evidence/bpesem05r01/no_market_data_observation_attestation_v0_1.json")

if ra["result"]!="AMBIGUOUS": defects.append("RECOVERY_A_DRIFT")
if rb["result"]!="NOT_FOUND": defects.append("RECOVERY_B_DRIFT")
if rc["result"]!="INCOMPLETE_VERSION_COVERAGE": defects.append("RECOVERY_C_DRIFT")
if overall["overall_substantive_result"]!="BLOCKED" or overall["any_full_recovery"] is not False:
    defects.append("OVERALL_RECOVERY_DRIFT")
if horizon["lane_s_readjudication_sufficient_new_authority"] is not False:
    defects.append("UNAUTHORIZED_LANE_S_READJUDICATION")
if overall["lane_p_authorized"] is not False or horizon["lane_p_authorization_effect"]!="NONE":
    defects.append("UNAUTHORIZED_LANE_P")
if not (att["provider_bi5_market_data_get_performed"] is False
        and att["historical_market_data_object_acquired"] is False
        and att["physical_semantic_discrimination_executed"] is False):
    defects.append("MARKET_DATA_BOUNDARY_VIOLATION")

package_integrity="PASS" if not defects else "FAIL"
governed_result="BLOCKED" if package_integrity=="PASS" else "FAIL"

qualification={
 "schema":"BPESEM05R01_RECOVERY_QUALIFICATION_V0_1",
 "candidate_commit":CANDIDATE_COMMIT,
 "reviewed_persisted_head":HEAD,
 "reviewed_persisted_tree":TREE,
 "protected_candidate_blobs":PROTECTED,
 "candidate_ancestry":"PASS" if ancestry else "FAIL",
 "full_adversarial_break":reg,
 "post_candidate_changes":changes,
 "unresolved_post_candidate_paths":unresolved,
 "package_integrity_status":package_integrity,
 "recovery_a_result":ra["result"],
 "recovery_b_result":rb["result"],
 "recovery_c_result":rc["result"],
 "any_full_recovery":overall["any_full_recovery"],
 "lane_s_readjudication_sufficient_new_authority":horizon["lane_s_readjudication_sufficient_new_authority"],
 "lane_p_authorized":overall["lane_p_authorized"],
 "provider_market_data_observation_performed":False,
 "overall_governed_result":governed_result,
 "demonstrated_final_defects":defects,
 "created_at_utc":"2026-09-22T17:20:00Z"
}
qualification["qualification_seal"]=seal(qualification,"qualification_seal")
QUAL.write_text(json.dumps(qualification,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

lines=[
"# B-PE-SEM-05R-01 — FINAL PERSISTED-HEAD RE-BREAK","",
"Persisted HEAD attacked: "+HEAD,
"Persisted tree attacked: "+TREE,"",
"## Candidate / breaker","",
"~~~text",
"candidate commit = "+CANDIDATE_COMMIT,
"candidate ancestor = "+("PASS" if ancestry else "FAIL"),
"breaker verdict = "+str(reg.get("verdict")),
"breaker attacks = "+str(reg.get("attack_count")),
"breaker defects = "+str(len(reg.get("defects",[]))),
"post-candidate changed paths = "+str(len(changes)),
"unresolved changed paths = "+str(len(unresolved)),
"~~~","",
"## Recovery result","",
"~~~text",
"package integrity = "+package_integrity,
"Recovery A = "+ra["result"],
"Recovery B = "+rb["result"],
"Recovery C = "+rc["result"],
"any full recovery = "+("YES" if overall["any_full_recovery"] else "NO"),
"Lane S re-adjudication sufficient new authority = NO",
"Lane P authorized = NO",
"B-PE-SEM-05R-01 = "+governed_result,
"demonstrated final defects = "+str(len(defects)),
*(defects or ["NONE"]),
"qualification seal = "+qualification["qualification_seal"],
"~~~","",
"BLOCKED is substantive: provider-versioned artifacts recovered exact BI5 cache identity and partial client/history stability, but did not recover the complete provider-primary A/B/C authority required by the qualified semantic contract.","",
"No provider BI5 market-data object was requested or observed. No Lane P RequestManifest/P-DIAG, FULL_INTERVAL, D or backtest was authorized or executed.","","STOP."
]
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

print(json.dumps({
 "head":HEAD,
 "package_integrity_status":package_integrity,
 "recovery_a":ra["result"],"recovery_b":rb["result"],"recovery_c":rc["result"],
 "overall_governed_result":governed_result,
 "attack_count":reg.get("attack_count"),
 "unresolved_changes":unresolved,
 "defects":defects,
 "qualification_seal":qualification["qualification_seal"]
},indent=2))
