#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
REG_DIR=ROOT/"evidence"/"bpesem"/"registry"
OUT=ROOT/"evidence"/"bpesem03r"
REPORT_DIR=ROOT/"reports"/"data-qualification"

RUNNER_PATH="tools/berd02_transport_runner.py"
RUNNER_BLOB="e10a0c47ec6e9b28f480c958baf18141287187cb"
HIST_SOURCE_HEAD="2eb8350fb24c3043017c91475d202b5e0d6bb501"
HIST_EXECUTION_ID="BERD02-GHA-35533153289-1"
OLD_FAIL_REPORT="reports/data-qualification/bpesem03_operational_semantic_adjudication_final_rebreak_2026-09-21.md"
OLD_FAIL_REPORT_BLOB="cc2679fccee0470d40c5c2d6ace26797664d6e73"
OLD_ADJ="evidence/bpesem03/operational_semantic_rule_adjudication_v0_1.json"
OLD_ADJ_BLOB="3da0aebd8bcf3c10fa9545c4d091c4c047f99bd4"
OLD_HORIZON="evidence/bpesem03/semantic_evidence_horizon_v0_1.json"
OLD_HORIZON_BLOB="52cbc43f2a08f2c992ee978c368696127cbdc210"
POLICY_ID="BPESEM02-GOVERNED-SEMANTIC-DISCOVERY-V0_6"
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

TARGET_CLAIMS=["BPE-SEM-C01-OP","BPE-SEM-C02-OP","BPE-SEM-C03-OP","BPE-SEM-C07-OP"]
TARGET_DIMS=[
    "C01-D1-OP","C01-D2-OP","C01-D3-OP",
    "C02-D1-OP","C02-D2-OP","C02-D3-OP","C02-D4-OP",
    "C03-D1-OP","C03-D2-OP","C03-D4-OP",
    "C07-D2-OP",
]

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=copy.deepcopy(o)
    x.pop(field,None)
    return digest(x)

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def readj(path:str|Path)->dict[str,Any]:
    p=ROOT/path if isinstance(path,str) else path
    return json.loads(p.read_text(encoding="utf-8"))

def blob(path:str)->str:
    return git("hash-object",path)

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
                if r.get("governed_branch")!="integration/system-v1":
                    raise RuntimeError("registry branch mismatch: "+p)
                if r.get("registry_digest")!=seal(r,"registry_digest"):
                    raise RuntimeError("registry digest mismatch: "+p)
                regs.append(r)
    return regs

def discover(head:str)->tuple[list[dict[str,Any]],list[dict[str,Any]]]:
    tree=ls_tree(head)
    direct=sorted(p for p in tree if any(p.startswith(x) for x in DIRECT_PREFIXES))
    regs=registries_at_head(head,tree)
    seed=set(direct)
    registered_items=[]
    for r in regs:
        for it in r.get("registered_items",[]):
            p=it["artifact_path"]; b=it["artifact_git_blob"]
            if p not in tree or tree[p]["git_blob"]!=b:
                raise RuntimeError("registered path/blob absent at governed HEAD: "+p)
            seed.add(p)
            registered_items.append({
                "registry_id":r["registry_id"],
                "registry_digest":r["registry_digest"],
                **it,
            })
    seen=set(seed)
    queue=sorted(seed)
    origins={p:set(["DIRECT_PREFIX" if p in direct else "REGISTRY"]) for p in seed}
    while queue:
        p=queue.pop(0)
        for q in refs_for(p,tree):
            origins.setdefault(q,set()).add("REF:"+p)
            if q not in seen:
                seen.add(q); queue.append(q)
    rows=[]
    for p in sorted(seen):
        rows.append({
            "path":p,
            "git_blob":tree[p]["git_blob"],
            "size":tree[p]["size"],
            "relevance_disposition":relevance(p),
            "discovery_origin":sorted(origins.get(p,set())),
        })
    return rows,registered_items

def policy_payload()->dict[str,Any]:
    return {
        "policy_id":POLICY_ID,
        "case_sensitive":True,
        "git_tree_recursive_enumeration":True,
        "direct_prefixes":list(DIRECT_PREFIXES),
        "registry_path_prefix":REGISTRY_PREFIX,
        "reference_closure":"TRANSITIVE_FIXED_POINT",
        "visited_identity":"{path,git_blob}",
        "unresolved_required_reference_disposition":"BLOCKED",
    }

def writej(path:Path,obj:dict[str,Any]):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

def materialize_registry():
    head=git("rev-parse","HEAD")
    if blob(OLD_FAIL_REPORT)!=OLD_FAIL_REPORT_BLOB:
        raise RuntimeError("old B-PE-SEM-03 final FAIL report changed")
    if blob(OLD_ADJ)!=OLD_ADJ_BLOB:
        raise RuntimeError("old B-PE-SEM-03 adjudication changed")
    if blob(RUNNER_PATH)!=RUNNER_BLOB:
        raise RuntimeError("runner current blob mismatch")
    source_blob=subprocess.check_output(["git","rev-parse",HIST_SOURCE_HEAD+":"+RUNNER_PATH],cwd=ROOT,text=True).strip()
    if source_blob!=RUNNER_BLOB:
        raise RuntimeError("runner historical source blob mismatch")

    hist=readj("evidence/bpesem03/historical_observation_eligibility_v0_1.json")
    recs=[r for r in hist["records"] if RUNNER_PATH in r["pre_observation_artifact_refs"]]
    dims=sorted(r["target_dimension_id"] for r in recs)
    if dims!=sorted(TARGET_DIMS):
        raise RuntimeError("historical target dimension set mismatch")
    if any(r["historical_source_head"]!=HIST_SOURCE_HEAD or r["historical_execution_id"]!=HIST_EXECUTION_ID for r in recs):
        raise RuntimeError("historical identity mismatch")
    if any(r["eligibility_role"]!="NONDECISIVE_COMPATIBILITY" or r["decisive_discrimination_eligible"] is not False for r in recs):
        raise RuntimeError("historical compatibility firewall mismatch")

    registry={
        "schema":"B_PE_SEM_02_SEMANTIC_EVIDENCE_REGISTRY_V0_6",
        "registry_id":"BPESEM03R-BERD02-LINEAGE-REGISTRY-V0_1",
        "governed_branch":"integration/system-v1",
        "registry_parent_id":None,
        "registered_items":[{
            "registry_item_id":"BPESEM03R-LINEAGE-BERD02-TRANSPORT-RUNNER",
            "artifact_path":RUNNER_PATH,
            "artifact_git_blob":RUNNER_BLOB,
            "artifact_role":"LINEAGE_EVIDENCE",
            "target_claim_ids":TARGET_CLAIMS,
            "target_dimension_ids":TARGET_DIMS,
            "registration_reason":"Exact project-origin pre-observation execution mechanism for BERD02-GHA-35533153289-1; required for historical provenance/lineage closure only. It is not independent semantic authority and remains NONDECISIVE_COMPATIBILITY.",
            "historical_source_head":HIST_SOURCE_HEAD,
            "historical_execution_id":HIST_EXECUTION_ID,
            "project_origin_status":"PROJECT_ORIGIN_EXECUTION_MECHANISM",
            "positive_authority_eligible":False,
            "independent_semantic_source":False,
            "historical_observation_role":"NONDECISIVE_COMPATIBILITY",
            "decisive_semantic_discrimination_eligible":False,
            "post_hoc_semantic_discrimination_eligible":False,
        }],
        "created_at_utc":"2026-09-22T09:20:00Z",
    }
    registry["registry_digest"]=seal(registry,"registry_digest")
    p=REG_DIR/"bpesem03r_berd02_lineage_registry_v0_1.json"
    writej(p,registry)

    report=REPORT_DIR/"bpesem03r_lineage_registry_candidate_2026-09-22.md"
    report.write_text(
        "# B-PE-SEM-03R — BERD02 LINEAGE REGISTRY CANDIDATE\n\n"
        "Starting HEAD: "+head+"\n\n"
        "Registered exact artifact identity:\n\n"
        "~~~text\n"
        "path = "+RUNNER_PATH+"\n"
        "blob = "+RUNNER_BLOB+"\n"
        "role = LINEAGE_EVIDENCE\n"
        "project origin = PROJECT_ORIGIN_EXECUTION_MECHANISM\n"
        "positive authority eligible = false\n"
        "independent semantic source = false\n"
        "historical role = NONDECISIVE_COMPATIBILITY\n"
        "decisive semantic discrimination eligible = false\n"
        "~~~\n\n"
        "Old B-PE-SEM-03 final FAIL remains unchanged.\n\n"
        "No provider/network execution occurred.\n",
        encoding="utf-8"
    )
    print(json.dumps({"mode":"registry","head":head,"registry_digest":registry["registry_digest"],"target_dimensions":dims},indent=2))

def materialize_candidate():
    head=git("rev-parse","HEAD")
    tree=git("rev-parse",head+"^{tree}")
    if blob(OLD_FAIL_REPORT)!=OLD_FAIL_REPORT_BLOB or blob(OLD_ADJ)!=OLD_ADJ_BLOB or blob(OLD_HORIZON)!=OLD_HORIZON_BLOB:
        raise RuntimeError("B-PE-SEM-03 historical artifacts changed")
    rows,registered_items=discover(head)
    regitems=[x for x in registered_items if x["artifact_path"]==RUNNER_PATH and x["artifact_git_blob"]==RUNNER_BLOB]
    if len(regitems)!=1 or regitems[0]["artifact_role"]!="LINEAGE_EVIDENCE":
        raise RuntimeError("exact runner lineage registration missing")
    if regitems[0]["positive_authority_eligible"] is not False or regitems[0]["decisive_semantic_discrimination_eligible"] is not False:
        raise RuntimeError("runner authority firewall violated")

    policy=policy_payload()
    pdig=digest(policy)
    baseline={
        "schema":"B_PE_SEM_02_GOVERNED_SEMANTIC_EVIDENCE_BASELINE_V0_4",
        "baseline_id":"BPESEM03R-GOVERNED-EVIDENCE-BASELINE-V0_1",
        "governed_branch":"integration/system-v1",
        "baseline_head":head,
        "baseline_tree_sha":tree,
        "discovery_policy_id":POLICY_ID,
        "discovery_policy_digest":pdig,
        "registry_item_refs":[{
            "registry_id":x["registry_id"],
            "registry_digest":x["registry_digest"],
            "registry_item_id":x["registry_item_id"],
            "artifact_path":x["artifact_path"],
            "artifact_git_blob":x["artifact_git_blob"],
            "artifact_role":x["artifact_role"],
        } for x in registered_items],
        "baseline_member_count":len(rows),
        "baseline_member_refs":[{"path":x["path"],"git_blob":x["git_blob"],"relevance_disposition":x["relevance_disposition"]} for x in rows],
        "created_at_utc":"2026-09-22T09:25:00Z",
    }
    baseline["baseline_digest"]=seal(baseline,"baseline_digest")

    horizon={
        "schema":"B_PE_SEM_02_SEMANTIC_EVIDENCE_HORIZON_V0_1",
        "horizon_id":"BPESEM03R-EVIDENCE-HORIZON-V0_1",
        "adjudication_id":"BPESEM03R-OPERATIONAL-SEMANTIC-ADJUDICATION-V0_1",
        "cutoff_head":head,
        "cutoff_tree_sha":tree,
        "discovery_policy_id":POLICY_ID,
        "discovery_policy_digest":pdig,
        "governed_baseline_id":baseline["baseline_id"],
        "governed_baseline_digest":baseline["baseline_digest"],
        "registered_lineage_evidence":[{
            "artifact_path":RUNNER_PATH,
            "artifact_git_blob":RUNNER_BLOB,
            "artifact_role":"LINEAGE_EVIDENCE",
            "positive_authority_eligible":False,
            "historical_observation_role":"NONDECISIVE_COMPATIBILITY",
            "decisive_semantic_discrimination_eligible":False,
        }],
        "discovered_semantic_artifact_refs":[{"path":x["path"],"git_blob":x["git_blob"],"relevance_disposition":x["relevance_disposition"]} for x in rows],
    }
    horizon["horizon_digest"]=seal(horizon,"horizon_digest")

    old=readj(OLD_ADJ)
    adj=copy.deepcopy(old)
    adj["adjudication_id"]="BPESEM03R-OPERATIONAL-SEMANTIC-ADJUDICATION-V0_1"
    adj["supersedes_adjudication_id"]=old["adjudication_id"]
    adj["adjudicator_identity"]="B-PE-SEM-03R_GOVERNED_READJUDICATION"
    adj["governed_semantic_evidence_baseline_id"]=baseline["baseline_id"]
    adj["governed_semantic_evidence_baseline_digest"]=baseline["baseline_digest"]
    adj["semantic_evidence_horizon_id"]=horizon["horizon_id"]
    adj["semantic_evidence_horizon_digest"]=horizon["horizon_digest"]
    adj["discovery_policy_id"]=POLICY_ID
    adj["discovery_policy_digest"]=pdig
    adj["lineage_registration_resolution"]={
        "registry_id":regitems[0]["registry_id"],
        "registry_digest":regitems[0]["registry_digest"],
        "registry_item_id":regitems[0]["registry_item_id"],
        "artifact_path":RUNNER_PATH,
        "artifact_git_blob":RUNNER_BLOB,
        "artifact_role":"LINEAGE_EVIDENCE",
        "historical_source_head":HIST_SOURCE_HEAD,
        "historical_execution_id":HIST_EXECUTION_ID,
        "project_origin_status":"PROJECT_ORIGIN_EXECUTION_MECHANISM",
        "positive_authority_eligible":False,
        "independent_semantic_source":False,
        "historical_observation_role":"NONDECISIVE_COMPATIBILITY",
        "decisive_semantic_discrimination_eligible":False,
        "post_hoc_semantic_discrimination_eligible":False,
        "target_claim_ids":TARGET_CLAIMS,
        "target_dimension_ids":TARGET_DIMS,
        "status":"PASS",
    }
    adj["prior_bpesem03_final_verdict"]={
        "overall":"FAIL",
        "integrity":"FAIL",
        "semantic_authority":"BLOCKED",
        "final_report_path":OLD_FAIL_REPORT,
        "final_report_blob":OLD_FAIL_REPORT_BLOB,
        "preserved_unchanged":True,
    }
    adj["created_at_utc"]="2026-09-22T09:25:00Z"
    # Registration is lineage-only; semantic proposition statuses must remain byte-for-byte equivalent projections.
    old_dim={x["dimension_id"]:(x["status"],x["reason_codes"]) for x in old["dimension_adjudications"]}
    new_dim={x["dimension_id"]:(x["status"],x["reason_codes"]) for x in adj["dimension_adjudications"]}
    if old_dim!=new_dim:
        raise RuntimeError("semantic dimension status changed solely due to registration")
    if old["claim_adjudications"]!=adj["claim_adjudications"] or old["overall_operational_semantic_status"]!=adj["overall_operational_semantic_status"]:
        raise RuntimeError("semantic claim status changed solely due to registration")
    adj["adjudication_seal"]=seal(adj,"adjudication_seal")

    oldh=readj(OLD_HORIZON)
    P={x["path"]:x["git_blob"] for x in oldh["discovered_semantic_artifact_refs"]}
    C={x["path"]:x["git_blob"] for x in horizon["discovered_semantic_artifact_refs"]}
    added=sorted(set(C)-set(P))
    deleted=sorted(set(P)-set(C))
    modified=sorted(p for p in set(P)&set(C) if P[p]!=C[p])
    dispositions=[]
    blockers=[]
    for p in added:
        if p==RUNNER_PATH:
            disp="REGISTERED_LINEAGE_EVIDENCE"
            reasons=["V0_6_REGISTRY_EXACT_PATH_BLOB","PROJECT_ORIGIN_NONDECISIVE_COMPATIBILITY","NO_POSITIVE_AUTHORITY"]
        elif p.startswith("evidence/bpesem03/") or p.startswith("reports/data-qualification/bpesem03_"):
            disp="CORROBORATING_NO_AUTHORITY_CHANGE"
            reasons=["CLOSED_BPESEM03_SAME_HISTORICAL_LINEAGE"]
        elif p.startswith("evidence/bpesem/registry/"):
            disp="GOVERNANCE_CONSTRAINT"
            reasons=["V0_6_SEMANTIC_EVIDENCE_REGISTRY"]
        else:
            disp="BLOCKED_UNRESOLVED"
            reasons=["NEW_DISCOVERED_ARTIFACT_REQUIRES_REVIEW"]
            blockers.append(p)
        dispositions.append({"path":p,"change_type":"ADDED","prior_git_blob":None,"current_git_blob":C[p],"disposition":disp,"reason_codes":reasons})
    for p in deleted:
        blockers.append(p)
        dispositions.append({"path":p,"change_type":"DELETED","prior_git_blob":P[p],"current_git_blob":None,"disposition":"BLOCKED_UNRESOLVED","reason_codes":["PRIOR_HORIZON_ARTIFACT_DELETED"]})
    for p in modified:
        blockers.append(p)
        dispositions.append({"path":p,"change_type":"MODIFIED","prior_git_blob":P[p],"current_git_blob":C[p],"disposition":"BLOCKED_UNRESOLVED","reason_codes":["PRIOR_HORIZON_ARTIFACT_MODIFIED"]})

    delta={
        "schema":"B_PE_SEM_02_CURRENT_AUTHORITY_EVIDENCE_DELTA_REVIEW_V0_1",
        "delta_review_id":"BPESEM03R-CURRENT-AUTHORITY-DELTA-V0_1",
        "prior_horizon_id":oldh["horizon_id"],
        "prior_horizon_digest":oldh["horizon_digest"],
        "prior_cutoff_head":oldh["cutoff_head"],
        "current_horizon_id":horizon["horizon_id"],
        "current_horizon_digest":horizon["horizon_digest"],
        "reviewed_consumer_parent_head":head,
        "reviewed_consumer_parent_tree_sha":tree,
        "descendant_relation_status":"DESCENDANT" if subprocess.run(["git","merge-base","--is-ancestor",oldh["cutoff_head"],head],cwd=ROOT).returncode==0 else "NON_DESCENDANT",
        "added_items":[{"path":p,"current_git_blob":C[p]} for p in added],
        "deleted_items":[{"path":p,"prior_git_blob":P[p]} for p in deleted],
        "modified_items":[{"path":p,"prior_git_blob":P[p],"current_git_blob":C[p]} for p in modified],
        "per_delta_item_dispositions":dispositions,
        "unresolved_paths":sorted(set(blockers)),
        "status":"PASS" if not blockers else "BLOCKED",
        "created_at_utc":"2026-09-22T09:25:00Z",
    }
    delta["delta_review_seal"]=seal(delta,"delta_review_seal")

    OUT.mkdir(parents=True,exist_ok=True)
    writej(OUT/"governed_semantic_evidence_baseline_v0_1.json",baseline)
    writej(OUT/"semantic_evidence_horizon_v0_1.json",horizon)
    writej(OUT/"operational_semantic_rule_adjudication_v0_1.json",adj)
    writej(OUT/"current_authority_evidence_delta_review_v0_1.json",delta)

    report=REPORT_DIR/"bpesem03r_fresh_horizon_readjudication_candidate_2026-09-22.md"
    report.write_text(
        "# B-PE-SEM-03R — FRESH HORIZON RE-ADJUDICATION CANDIDATE\n\n"
        "Candidate parent HEAD: "+head+"\n\n"
        "~~~text\n"
        "registry role = LINEAGE_EVIDENCE\n"
        "runner positive authority = false\n"
        "runner historical role = NONDECISIVE_COMPATIBILITY\n"
        "runner decisive semantic discrimination = false\n"
        "baseline members = "+str(len(rows))+"\n"
        "delta added = "+str(len(added))+"\n"
        "delta deleted = "+str(len(deleted))+"\n"
        "delta modified = "+str(len(modified))+"\n"
        "delta unresolved = "+str(len(blockers))+"\n"
        "delta status = "+delta["status"]+"\n"
        "semantic dimension statuses changed = NO\n"
        "semantic claim statuses changed = NO\n"
        "overall semantic authority = "+adj["overall_operational_semantic_status"]+"\n"
        "~~~\n\n"
        "B-PE-SEM-03 final FAIL remains immutable historical authority.\n\n"
        "No provider contact, BI5 GET, FULL_INTERVAL, D or backtest occurred.\n",
        encoding="utf-8"
    )
    print(json.dumps({
        "mode":"candidate",
        "head":head,
        "baseline_members":len(rows),
        "runner_registered":True,
        "delta_added":len(added),
        "delta_deleted":len(deleted),
        "delta_modified":len(modified),
        "delta_unresolved":blockers,
        "delta_status":delta["status"],
        "semantic_status":adj["overall_operational_semantic_status"],
        "adjudication_seal":adj["adjudication_seal"],
        "horizon_digest":horizon["horizon_digest"],
    },indent=2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode",choices=["registry","candidate"],required=True)
    args=ap.parse_args()
    if args.mode=="registry":
        materialize_registry()
    else:
        materialize_candidate()

if __name__=="__main__":
    main()
