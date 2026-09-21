#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem03"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem03_operational_semantic_adjudication_final_rebreak_2026-09-21.md"
DELTA=E/"current_authority_evidence_delta_review_v0_1.json"

DIRECT_PREFIXES=(
    "evidence/bpe",
    "reports/data-qualification/bpe",
    "evidence/berd",
    "reports/data-qualification/berd",
    "evidence/bfiq",
    "reports/data-qualification/bfiq",
)
REF_RE=re.compile(rb"(?<![A-Za-z0-9_.-])(?:evidence|reports|04-REFERENCE|src|tools|breakers|[.]github)/[A-Za-z0-9_./-]+")

EXPECTED_ADJ_BLOB="3da0aebd8bcf3c10fa9545c4d091c4c047f99bd4"
EXPECTED_CANDIDATE_REPORT_BLOB="ce0159029b100c4e766eae44ae805fb1c5977915"
EXPECTED_INITIAL_BREAK_BLOB="507ad73018d963b5bd43ab276c95f53f1924fc18"
EXPECTED_HORIZON_BLOB="52cbc43f2a08f2c992ee978c368696127cbdc210"

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=dict(o); x.pop(field,None); return digest(x)

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def readj(p:Path)->dict[str,Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def git_blob(path:str)->str:
    return git("hash-object",path)

def ls_tree(head:str)->dict[str,dict[str,Any]]:
    raw=subprocess.check_output(["git","ls-tree","-r","-l",head],cwd=ROOT)
    out={}
    for line in raw.decode("utf-8").splitlines():
        left,path=line.split("\t",1)
        mode,typ,blob,size=left.split()
        if typ=="blob":
            out[path]={"git_blob":blob,"size":int(size)}
    return out

def read_refs(path:str,tree:dict[str,dict[str,Any]])->set[str]:
    raw=(ROOT/path).read_bytes()
    if bytes([0]) in raw[:8192]:
        return set()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return set()
    out=set()
    for m in REF_RE.finditer(raw):
        p=m.group(0).decode("utf-8").rstrip(".,;:)]}'\"")
        if p in tree:
            out.add(p)
    return out

def relevance(path:str)->str:
    if path.startswith("evidence/bpe") or path.startswith("evidence/berd"):
        return "MATERIAL_VISIBLE"
    if path.startswith("evidence/bfiq") and any(k in path for k in ("semantic_invariant","representation_regime","provider_delivery_identity","interval_inventory")):
        return "MATERIAL_VISIBLE"
    return "GOVERNANCE_VISIBLE"

def discover(head:str)->list[dict[str,Any]]:
    tree=ls_tree(head)
    direct=sorted(p for p in tree if any(p.startswith(x) for x in DIRECT_PREFIXES))
    seen=set(direct)
    queue=list(direct)
    while queue:
        p=queue.pop(0)
        for r in read_refs(p,tree):
            if r not in seen:
                seen.add(r)
                queue.append(r)
    return [
        {"path":p,"git_blob":tree[p]["git_blob"],"relevance_disposition":relevance(p)}
        for p in sorted(seen)
    ]

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")

assert git_blob("evidence/bpesem03/operational_semantic_rule_adjudication_v0_1.json")==EXPECTED_ADJ_BLOB
assert git_blob("reports/data-qualification/bpesem03_operational_semantic_adjudication_candidate_2026-09-21.md")==EXPECTED_CANDIDATE_REPORT_BLOB
assert git_blob("reports/data-qualification/bpesem03_operational_semantic_adjudication_adversarial_break_2026-09-21.md")==EXPECTED_INITIAL_BREAK_BLOB
assert git_blob("evidence/bpesem03/semantic_evidence_horizon_v0_1.json")==EXPECTED_HORIZON_BLOB

env=dict(os.environ)
env["BPESEM03_BREAK_REPORT"]="/tmp/bpesem03-final-rebreak-precheck.md"
cp=subprocess.run(
    ["python3","breakers/bpesem03_operational_semantic_adjudication_breaker.py"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    env=env,
    check=False,
)
if cp.returncode!=0:
    raise RuntimeError("Part-2 breaker execution failed: "+cp.stdout+"\n"+cp.stderr)
pre=json.loads(cp.stdout)
if pre.get("verdict")!="PASS" or pre.get("defects"):
    raise RuntimeError("Persisted candidate no longer survives Part-2 breaker: "+repr(pre))

adj=readj(E/"operational_semantic_rule_adjudication_v0_1.json")
horizon=readj(E/"semantic_evidence_horizon_v0_1.json")

prior_head=horizon["cutoff_head"]
ancestry="DESCENDANT" if subprocess.run(["git","merge-base","--is-ancestor",prior_head,HEAD],cwd=ROOT).returncode==0 else "NON_DESCENDANT"

prior_rows=horizon["discovered_semantic_artifact_refs"]
current_rows=discover(HEAD)
P={x["path"]:x["git_blob"] for x in prior_rows}
C={x["path"]:x["git_blob"] for x in current_rows}
if len(P)!=len(prior_rows) or len(C)!=len(current_rows):
    raise RuntimeError("duplicate artifact keys in horizon")

added=sorted(set(C)-set(P))
deleted=sorted(set(P)-set(C))
modified=sorted(p for p in set(P)&set(C) if P[p]!=C[p])

def is_self_governance(path:str)->bool:
    return path.startswith("evidence/bpesem03/") or path.startswith("reports/data-qualification/bpesem03_")

dispositions=[]
delta_blockers=[]
for p in added:
    if is_self_governance(p):
        disp="CORROBORATING_NO_AUTHORITY_CHANGE"
        reasons=["SELF_MATERIALIZED_BPESEM03_SAME_ADJUDICATION_LINEAGE","NO_NEW_EXTERNAL_OR_INDEPENDENT_SEMANTIC_SOURCE"]
    else:
        disp="BLOCKED_UNRESOLVED"
        reasons=["NEW_DISCOVERED_GOVERNED_SEMANTIC_ARTIFACT_OUTSIDE_CURRENT_LINEAGE"]
        delta_blockers.append(p)
    dispositions.append({"path":p,"change_type":"ADDED","prior_git_blob":None,"current_git_blob":C[p],"disposition":disp,"reason_codes":reasons})

for p in deleted:
    dispositions.append({"path":p,"change_type":"DELETED","prior_git_blob":P[p],"current_git_blob":None,"disposition":"BLOCKED_UNRESOLVED","reason_codes":["PRIOR_HORIZON_ARTIFACT_DELETED"]})
    delta_blockers.append(p)

for p in modified:
    dispositions.append({"path":p,"change_type":"MODIFIED","prior_git_blob":P[p],"current_git_blob":C[p],"disposition":"BLOCKED_UNRESOLVED","reason_codes":["PRIOR_HORIZON_ARTIFACT_BYTES_CHANGED"]})
    delta_blockers.append(p)

delta_status="PASS" if ancestry=="DESCENDANT" and not delta_blockers else "BLOCKED"
delta={
    "schema":"B_PE_SEM_02_CURRENT_AUTHORITY_EVIDENCE_DELTA_REVIEW_V0_1",
    "delta_review_id":"BPESEM03-CURRENT-AUTHORITY-DELTA-V0_1",
    "adjudication_id":adj["adjudication_id"],
    "adjudication_seal":adj["adjudication_seal"],
    "prior_horizon_id":horizon["horizon_id"],
    "prior_horizon_digest":horizon["horizon_digest"],
    "prior_cutoff_head":prior_head,
    "reviewed_consumer_parent_head":HEAD,
    "reviewed_consumer_parent_tree_sha":TREE,
    "descendant_relation_status":ancestry,
    "current_discovery_policy_id":horizon["discovery_policy_id"],
    "current_discovery_policy_digest":horizon["discovery_policy_digest"],
    "current_discovered_semantic_artifact_refs":current_rows,
    "added_items":[{"path":p,"current_git_blob":C[p]} for p in added],
    "deleted_items":[{"path":p,"prior_git_blob":P[p]} for p in deleted],
    "modified_items":[{"path":p,"prior_git_blob":P[p],"current_git_blob":C[p]} for p in modified],
    "per_delta_item_dispositions":dispositions,
    "created_reopen_event_ids":[],
    "status":delta_status,
    "reviewer_identity":"B-PE-SEM-03_FINAL_REBREAK",
    "created_at_utc":"2026-09-21T20:45:00Z",
}
delta["delta_review_seal"]=seal(delta,"delta_review_seal")
DELTA.write_text(json.dumps(delta,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

defects=[]
def chk(name:str,condition:bool):
    if not condition:
        defects.append(name)

dims=adj["dimension_adjudications"]
pass_dims=sorted(x["dimension_id"] for x in dims if x["status"]=="PASS")
blocked_dims=sorted(x["dimension_id"] for x in dims if x["status"]=="BLOCKED")
fail_dims=sorted(x["dimension_id"] for x in dims if x["status"]=="FAIL")

chk("F01_PART2_BREAKER_REGRESSION",pre["verdict"]=="PASS" and not pre["defects"])
chk("F02_ADJUDICATION_SEAL",adj["adjudication_seal"]==seal(adj,"adjudication_seal"))
chk("F03_EXACT_PASS_DIMENSIONS",pass_dims==["C03-D3-OP","C05-D2-OP"])
chk("F04_EXACT_BLOCKED_DIMENSION_COUNT",len(blocked_dims)==24)
chk("F05_NO_FAIL_DIMENSIONS",fail_dims==[])
chk("F06_ALL_CLAIMS_BLOCKED",len(adj["claim_adjudications"])==7 and all(x["status"]=="BLOCKED" for x in adj["claim_adjudications"]))
chk("F07_OVERALL_SEMANTIC_BLOCKED",adj["overall_operational_semantic_status"]=="BLOCKED" and adj["adjudication_status"]=="BLOCKED")
chk("F08_ZERO_C08_EFFECT",all(not x.get("claim_id","").startswith("BPE-SEM-C08") for x in adj["claim_adjudications"]))
chk("F09_DELTA_ANCESTRY",ancestry=="DESCENDANT")
chk("F10_DELTA_SET_EXACT",len(dispositions)==len(added)+len(deleted)+len(modified))
chk("F11_DELTA_NO_UNRESOLVED",not delta_blockers)
chk("F12_DELTA_PASS",delta_status=="PASS")
chk("F13_NO_REOPEN_REQUIRED",delta["created_reopen_event_ids"]==[])
chk("F14_PERSISTED_CANDIDATE_IDENTITY",git_blob("evidence/bpesem03/operational_semantic_rule_adjudication_v0_1.json")==EXPECTED_ADJ_BLOB)

integrity_verdict="PASS" if not defects else "FAIL"
overall="BLOCKED" if integrity_verdict=="PASS" and adj["overall_operational_semantic_status"]=="BLOCKED" else "FAIL"

lines=[
    "# B-PE-SEM-03 — OPERATIONAL C01-C07 SEMANTIC AUTHORITY — FINAL PERSISTED-HEAD RE-BREAK",
    "",
    "Persisted HEAD attacked: "+HEAD,
    "Persisted tree attacked: "+TREE,
    "",
    "## 1. Candidate identity",
    "",
    "The exact persisted Part-2 candidate bytes were reverified before re-break.",
    "",
    "~~~text",
    "OperationalSemanticRuleAdjudication blob = "+EXPECTED_ADJ_BLOB,
    "candidate report blob = "+EXPECTED_CANDIDATE_REPORT_BLOB,
    "initial adversarial-break blob = "+EXPECTED_INITIAL_BREAK_BLOB,
    "semantic evidence horizon blob = "+EXPECTED_HORIZON_BLOB,
    "~~~",
    "",
    "## 2. Full adversarial regression",
    "",
    "~~~text",
    "Part-2 breaker verdict = "+pre["verdict"],
    "Part-2 demonstrated defects = "+str(len(pre["defects"])),
    "~~~",
    "",
    "## 3. Current-authority evidence delta",
    "",
    "~~~text",
    "prior horizon HEAD = "+prior_head,
    "reviewed current parent HEAD = "+HEAD,
    "ancestry = "+ancestry,
    "added discovered artifacts = "+str(len(added)),
    "deleted discovered artifacts = "+str(len(deleted)),
    "modified discovered artifacts = "+str(len(modified)),
    "unresolved/material authority-changing delta items = "+str(len(delta_blockers)),
    "CurrentAuthorityEvidenceDeltaReview = "+delta_status,
    "delta review seal = "+delta["delta_review_seal"],
    "~~~",
    "",
    "All accepted added items are self-materialized B-PE-SEM-03 governance/adjudication outputs from the same evidence lineage. They add no independent external semantic authority and create no reopen trigger.",
    "",
    "## 4. Final semantic result",
    "",
    "~~~text",
    "dimension PASS = "+str(len(pass_dims)),
    "PASS dimensions = "+", ".join(pass_dims),
    "dimension BLOCKED = "+str(len(blocked_dims)),
    "dimension FAIL = "+str(len(fail_dims)),
    "",
    "BPE-SEM-C01-OP = BLOCKED",
    "BPE-SEM-C02-OP = BLOCKED",
    "BPE-SEM-C03-OP = BLOCKED",
    "BPE-SEM-C04-OP = BLOCKED",
    "BPE-SEM-C05-OP = BLOCKED",
    "BPE-SEM-C06-OP = BLOCKED",
    "BPE-SEM-C07-OP = BLOCKED",
    "",
    "overall operational semantic authority = BLOCKED",
    "~~~",
    "",
    "The two PASS dimensions are only the pre-authorized conditional mathematical signedness rule. Their future high-bit-zero obligations remain non-waivable; no target data satisfaction is asserted.",
    "",
    "## 5. Final governed verdict",
    "",
    "~~~text",
    "B-PE-SEM-03 PACKAGE MATERIALIZATION / ADJUDICATION INTEGRITY = "+integrity_verdict,
    "B-PE-SEM-03 OPERATIONAL C01-C07 SEMANTIC AUTHORITY = BLOCKED",
    "B-PE-SEM-03 OVERALL GOVERNED VERDICT = "+overall,
    "",
    "demonstrated final re-break defects = "+str(len(defects)),
    *(defects or ["NONE"]),
    "~~~",
    "",
    "This BLOCKED verdict is a successful fail-closed adjudication of the existing governed evidence. It is not a failure of B-PE-SEM-02.",
    "",
    "No provider contact, provider BI5 GET, new provider-object acquisition, new semantic-discrimination execution, FULL_INTERVAL execution, D materialization or backtest occurred.",
    "",
    "## 6. Consequence",
    "",
    "B-FIQ-02R is NOT authorized because current operational C01-C07 semantic authority is not overall PASS.",
    "",
    "The next governed block must formalize the minimum admissible closure route for the 24 BLOCKED dimensions before any new evidence acquisition/execution is authorized.",
    "",
    "STOP.",
]
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")

print(json.dumps({
    "persisted_head":HEAD,
    "part2_breaker_verdict":pre["verdict"],
    "delta_status":delta_status,
    "added":len(added),
    "deleted":len(deleted),
    "modified":len(modified),
    "integrity_verdict":integrity_verdict,
    "semantic_authority":"BLOCKED",
    "overall":overall,
    "defects":defects,
},indent=2,sort_keys=True))
