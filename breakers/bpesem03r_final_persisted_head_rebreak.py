#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem03r"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem03r_final_persisted_head_rebreak_2026-09-22.md"
FINAL_DELTA=OUT/"final_current_authority_evidence_delta_review_v0_1.json"

EXPECTED_BASELINE_BLOB="551968c682e3b7ff4b823fec0361ec6329ba8d8c"
EXPECTED_HORIZON_BLOB="147056a7bcd3c872f58bea7320c44350a2030f32"
EXPECTED_ADJ_BLOB="d26655e3806b36305252fda186ccf4d08e38084b"
EXPECTED_DELTA_BLOB="1fb6f703a715572f9ae749092464db592dc5b2ef"
EXPECTED_BREAK_BLOB="52fa677ddd1c8e0228ebf7223a174d1ccbd4dd76"
RUNNER_PATH="tools/berd02_transport_runner.py"
RUNNER_BLOB="e10a0c47ec6e9b28f480c958baf18141287187cb"
REG_PATH="evidence/bpesem/registry/bpesem03r_berd02_lineage_registry_v0_1.json"
OLD_FAIL_REPORT="reports/data-qualification/bpesem03_operational_semantic_adjudication_final_rebreak_2026-09-21.md"
OLD_FAIL_BLOB="cc2679fccee0470d40c5c2d6ace26797664d6e73"

DIRECT_PREFIXES=(
    "evidence/bpe",
    "reports/data-qualification/bpe",
    "evidence/berd",
    "reports/data-qualification/berd",
    "evidence/bfiq",
    "reports/data-qualification/bfiq",
)
REGISTRY_PREFIX="evidence/bpesem/registry/"
REF_RE=re.compile(rb"(?<![A-Za-z0-9_.-])(?:evidence|reports|04-REFERENCE|src|tools|breakers|[.]github)/[A-Za-z0-9_./-]+")

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

def readj(path:str|Path)->dict[str,Any]:
    p=ROOT/path if isinstance(path,str) else path
    return json.loads(p.read_text(encoding="utf-8"))

def ls_tree(head:str)->dict[str,dict[str,Any]]:
    raw=subprocess.check_output(["git","ls-tree","-r","-l",head],cwd=ROOT)
    out={}
    for line in raw.decode("utf-8").splitlines():
        left,path=line.split("\t",1)
        mode,typ,sha,size=left.split()
        if typ=="blob":
            out[path]={"git_blob":sha,"size":int(size)}
    return out

def refs_for(path:str,tree:dict[str,dict[str,Any]])->set[str]:
    raw=(ROOT/path).read_bytes()
    if bytes([0]) in raw[:8192]:
        return set()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return set()
    refs=set()
    for m in REF_RE.finditer(raw):
        p=m.group(0).decode("utf-8").rstrip(".,;:)]}'\"")
        if p in tree:
            refs.add(p)
    return refs

def relevance(path:str)->str:
    if path==RUNNER_PATH:
        return "LINEAGE_VISIBLE"
    if path.startswith("evidence/berd") or path.startswith("evidence/bpe"):
        return "MATERIAL_VISIBLE"
    if path.startswith("evidence/bfiq") and any(k in path for k in ("semantic_invariant","representation_regime","provider_delivery_identity","interval_inventory")):
        return "MATERIAL_VISIBLE"
    return "GOVERNANCE_VISIBLE"

def registries_at_head(head:str,tree:dict[str,dict[str,Any]])->list[dict[str,Any]]:
    regs=[]
    for p in sorted(tree):
        if p.startswith(REGISTRY_PREFIX) and p.endswith(".json"):
            try:
                r=readj(p)
            except Exception:
                continue
            if r.get("schema")=="B_PE_SEM_02_SEMANTIC_EVIDENCE_REGISTRY_V0_6":
                if r.get("registry_digest")!=seal(r,"registry_digest"):
                    raise RuntimeError("invalid registry digest: "+p)
                regs.append(r)
    return regs

def discover(head:str)->list[dict[str,Any]]:
    tree=ls_tree(head)
    direct=sorted(p for p in tree if any(p.startswith(x) for x in DIRECT_PREFIXES))
    regs=registries_at_head(head,tree)
    seed=set(direct)
    for r in regs:
        for it in r.get("registered_items",[]):
            p=it["artifact_path"]; b=it["artifact_git_blob"]
            if p not in tree or tree[p]["git_blob"]!=b:
                raise RuntimeError("registered path/blob absent at HEAD: "+p)
            seed.add(p)
    seen=set(seed); queue=sorted(seed)
    while queue:
        p=queue.pop(0)
        for q in refs_for(p,tree):
            if q not in seen:
                seen.add(q); queue.append(q)
    return [{"path":p,"git_blob":tree[p]["git_blob"],"relevance_disposition":relevance(p)} for p in sorted(seen)]

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")

# Exact persisted candidate identity.
assert blob("evidence/bpesem03r/governed_semantic_evidence_baseline_v0_1.json")==EXPECTED_BASELINE_BLOB
assert blob("evidence/bpesem03r/semantic_evidence_horizon_v0_1.json")==EXPECTED_HORIZON_BLOB
assert blob("evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json")==EXPECTED_ADJ_BLOB
assert blob("evidence/bpesem03r/current_authority_evidence_delta_review_v0_1.json")==EXPECTED_DELTA_BLOB
assert blob("reports/data-qualification/bpesem03r_lineage_registration_adversarial_break_2026-09-22.md")==EXPECTED_BREAK_BLOB
assert blob(RUNNER_PATH)==RUNNER_BLOB
assert blob(OLD_FAIL_REPORT)==OLD_FAIL_BLOB

# Full adversarial regression on exact persisted candidate.
env=dict(os.environ)
env["BPESEM03R_BREAK_REPORT"]="/tmp/bpesem03r-final-regression.md"
cp=subprocess.run(
    ["python3","breakers/bpesem03r_lineage_registration_breaker.py"],
    cwd=ROOT,text=True,capture_output=True,env=env,check=False
)
if cp.returncode!=0:
    raise RuntimeError("candidate breaker execution error: "+cp.stdout+"\n"+cp.stderr)
pre=json.loads(cp.stdout)
if pre.get("verdict")!="PASS" or pre.get("defects"):
    raise RuntimeError("candidate regression failed: "+repr(pre))

horizon=readj("evidence/bpesem03r/semantic_evidence_horizon_v0_1.json")
adj=readj("evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json")
candidate_delta=readj("evidence/bpesem03r/current_authority_evidence_delta_review_v0_1.json")
registry=readj(REG_PATH)

prior_head=horizon["cutoff_head"]
ancestry="DESCENDANT" if subprocess.run(["git","merge-base","--is-ancestor",prior_head,HEAD],cwd=ROOT,check=False).returncode==0 else "NON_DESCENDANT"
current_rows=discover(HEAD)
P={x["path"]:x["git_blob"] for x in horizon["discovered_semantic_artifact_refs"]}
C={x["path"]:x["git_blob"] for x in current_rows}
if len(P)!=len(horizon["discovered_semantic_artifact_refs"]) or len(C)!=len(current_rows):
    raise RuntimeError("duplicate path identity in horizon")

added=sorted(set(C)-set(P))
deleted=sorted(set(P)-set(C))
modified=sorted(p for p in set(P)&set(C) if P[p]!=C[p])

def self_governance(p:str)->bool:
    return p.startswith("evidence/bpesem03r/") or p.startswith("reports/data-qualification/bpesem03r_")

dispositions=[]
blockers=[]
for p in added:
    if self_governance(p):
        disp="CORROBORATING_SELF_GOVERNANCE"
        reasons=["BPESEM03R_SAME_SUCCESSOR_LINEAGE","NO_NEW_INDEPENDENT_SEMANTIC_AUTHORITY"]
    elif p==REG_PATH:
        disp="GOVERNANCE_CONSTRAINT"
        reasons=["V0_6_REGISTRY_ALREADY_BOUND"]
    elif p==RUNNER_PATH:
        disp="REGISTERED_LINEAGE_EVIDENCE"
        reasons=["EXACT_V0_6_LINEAGE_REGISTRATION","NONDECISIVE_COMPATIBILITY","NO_POSITIVE_AUTHORITY"]
    else:
        disp="BLOCKED_UNRESOLVED"; reasons=["NEW_DISCOVERED_ARTIFACT_REQUIRES_REVIEW"]; blockers.append(p)
    dispositions.append({"path":p,"change_type":"ADDED","prior_git_blob":None,"current_git_blob":C[p],"disposition":disp,"reason_codes":reasons})

for p in modified:
    if self_governance(p):
        disp="CORROBORATING_SELF_GOVERNANCE"
        reasons=["BPESEM03R_CANDIDATE_PERSISTENCE_OR_BREAK_OUTPUT","NO_NEW_INDEPENDENT_SEMANTIC_AUTHORITY"]
    else:
        disp="BLOCKED_UNRESOLVED"; reasons=["NON_SELF_GOVERNANCE_ARTIFACT_MODIFIED"]; blockers.append(p)
    dispositions.append({"path":p,"change_type":"MODIFIED","prior_git_blob":P[p],"current_git_blob":C[p],"disposition":disp,"reason_codes":reasons})

for p in deleted:
    blockers.append(p)
    dispositions.append({"path":p,"change_type":"DELETED","prior_git_blob":P[p],"current_git_blob":None,"disposition":"BLOCKED_UNRESOLVED","reason_codes":["PRIOR_HORIZON_ARTIFACT_DELETED"]})

final_status="PASS" if ancestry=="DESCENDANT" and not blockers else "BLOCKED"
final_delta={
    "schema":"B_PE_SEM_02_CURRENT_AUTHORITY_EVIDENCE_DELTA_REVIEW_V0_1",
    "delta_review_id":"BPESEM03R-FINAL-CURRENT-AUTHORITY-DELTA-V0_1",
    "adjudication_id":adj["adjudication_id"],
    "adjudication_seal":adj["adjudication_seal"],
    "prior_horizon_id":horizon["horizon_id"],
    "prior_horizon_digest":horizon["horizon_digest"],
    "prior_cutoff_head":prior_head,
    "reviewed_consumer_parent_head":HEAD,
    "reviewed_consumer_parent_tree_sha":TREE,
    "descendant_relation_status":ancestry,
    "added_items":[{"path":p,"current_git_blob":C[p]} for p in added],
    "deleted_items":[{"path":p,"prior_git_blob":P[p]} for p in deleted],
    "modified_items":[{"path":p,"prior_git_blob":P[p],"current_git_blob":C[p]} for p in modified],
    "per_delta_item_dispositions":dispositions,
    "unresolved_paths":sorted(set(blockers)),
    "status":final_status,
    "created_at_utc":"2026-09-22T10:15:00Z",
}
final_delta["delta_review_seal"]=seal(final_delta,"delta_review_seal")
FINAL_DELTA.write_text(json.dumps(final_delta,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

defects=[]
def chk(name:str,cond:bool):
    if not cond: defects.append(name)

item=registry["registered_items"][0]
chk("F01_CANDIDATE_REGRESSION",pre["verdict"]=="PASS" and not pre["defects"])
chk("F02_ANCESTRY",ancestry=="DESCENDANT")
chk("F03_FINAL_DELTA_CLOSED",final_status=="PASS" and not blockers)
chk("F04_CANDIDATE_DELTA_PASS",candidate_delta["status"]=="PASS" and candidate_delta.get("unresolved_paths")==[])
chk("F05_RUNNER_ROLE",item["artifact_role"]=="LINEAGE_EVIDENCE" and item["positive_authority_eligible"] is False)
chk("F06_NONDECISIVE",item["historical_observation_role"]=="NONDECISIVE_COMPATIBILITY" and item["decisive_semantic_discrimination_eligible"] is False)
chk("F07_SEMANTIC_STILL_BLOCKED",adj["overall_operational_semantic_status"]=="BLOCKED")
chk("F08_OLD_FAIL_PRESERVED",adj["prior_bpesem03_final_verdict"]["overall"]=="FAIL" and adj["prior_bpesem03_final_verdict"]["preserved_unchanged"] is True and blob(OLD_FAIL_REPORT)==OLD_FAIL_BLOB)
chk("F09_NO_C08","BPE-SEM-C08" not in json.dumps(adj))
chk("F10_EXACT_CANDIDATE_BLOBS",blob("evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json")==EXPECTED_ADJ_BLOB and blob("evidence/bpesem03r/semantic_evidence_horizon_v0_1.json")==EXPECTED_HORIZON_BLOB)

integrity="PASS" if not defects else "FAIL"
overall="PASS_WITH_BLOCKED_SEMANTIC_AUTHORITY" if integrity=="PASS" and adj["overall_operational_semantic_status"]=="BLOCKED" else "FAIL"

lines=[
    "# B-PE-SEM-03R — FINAL PERSISTED-HEAD RE-BREAK",
    "",
    "Persisted HEAD attacked: "+HEAD,
    "Persisted tree attacked: "+TREE,
    "",
    "## Exact candidate identity",
    "",
    "~~~text",
    "baseline blob = "+EXPECTED_BASELINE_BLOB,
    "horizon blob = "+EXPECTED_HORIZON_BLOB,
    "adjudication blob = "+EXPECTED_ADJ_BLOB,
    "candidate delta blob = "+EXPECTED_DELTA_BLOB,
    "adversarial break blob = "+EXPECTED_BREAK_BLOB,
    "~~~",
    "",
    "## Full adversarial regression",
    "",
    "~~~text",
    "candidate breaker verdict = "+pre["verdict"],
    "candidate breaker defects = "+str(len(pre["defects"])),
    "~~~",
    "",
    "## Final current-authority delta",
    "",
    "~~~text",
    "candidate horizon cutoff = "+prior_head,
    "reviewed persisted HEAD = "+HEAD,
    "ancestry = "+ancestry,
    "added = "+str(len(added)),
    "modified = "+str(len(modified)),
    "deleted = "+str(len(deleted)),
    "unresolved = "+str(len(blockers)),
    "final delta status = "+final_status,
    "final delta seal = "+final_delta["delta_review_seal"],
    "~~~",
    "",
    "## Final governed result",
    "",
    "~~~text",
    "B-PE-SEM-03R lineage-registration / horizon integrity = "+integrity,
    "C01-C07 operational semantic authority = "+adj["overall_operational_semantic_status"],
    "B-PE-SEM-03R final result = "+overall,
    "demonstrated final defects = "+str(len(defects)),
    *(defects or ["NONE"]),
    "~~~",
    "",
    "A PASS here qualifies only the lineage-registration and fresh-horizon repair. It does not promote any blocked semantic proposition and does not authorize B-FIQ-02R.",
    "",
    "No provider contact, BI5 GET, FULL_INTERVAL, D materialization or backtest occurred.",
    "",
    "STOP."
]
REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({
    "head":HEAD,
    "candidate_breaker_verdict":pre["verdict"],
    "final_delta_status":final_status,
    "added":len(added),
    "modified":len(modified),
    "deleted":len(deleted),
    "unresolved":blockers,
    "integrity":integrity,
    "semantic_authority":adj["overall_operational_semantic_status"],
    "overall":overall,
    "defects":defects,
},indent=2))
