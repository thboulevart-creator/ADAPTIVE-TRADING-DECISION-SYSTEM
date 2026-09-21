#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem03"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem03_operational_semantic_adjudication_candidate_2026-09-21.md"

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=dict(o); x.pop(field,None); return digest(x)

def rawsha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

def gitblob(data:bytes)->str:
    return hashlib.sha1(("blob %d\0"%len(data)).encode()+data).hexdigest()

def source_identity(rel:str)->dict[str,Any]:
    raw=(ROOT/rel).read_bytes()
    return {"path":rel,"git_blob":gitblob(raw),"sha256_raw_bytes":hashlib.sha256(raw).hexdigest(),"byte_length":len(raw)}

def write_json(name:str,obj:dict[str,Any])->dict[str,Any]:
    p=OUT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    return source_identity(str(p.relative_to(ROOT)))

def readj(rel:str)->dict[str,Any]:
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

REF_RE=re.compile(rb"(?<![A-Za-z0-9_.-])(?:evidence|reports|04-REFERENCE|src|tools|breakers|\\.github)/[A-Za-z0-9_.\\-/]+")

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
        p=m.group(0).decode("utf-8").rstrip(".,;:)]}'\\\"")
        if p in tree:
            out.add(p)
    return out

def current_discovery(head:str,direct_prefixes:list[str])->list[dict[str,Any]]:
    tree=ls_tree(head)
    direct=sorted(p for p in tree if any(p.startswith(x) for x in direct_prefixes))
    seen=set(direct); q=list(direct); origins={p:{"DIRECT_PREFIX"} for p in direct}
    while q:
        p=q.pop(0)
        for r in read_refs(p,tree):
            origins.setdefault(r,set()).add("REF:"+p)
            if r not in seen:
                seen.add(r); q.append(r)
    rows=[]
    for p in sorted(seen):
        if p.startswith("evidence/bpe") or p.startswith("evidence/berd"):
            rel="MATERIAL_VISIBLE"
        elif p.startswith("evidence/bfiq") and any(k in p for k in ("semantic_invariant","representation_regime","provider_delivery_identity","interval_inventory")):
            rel="MATERIAL_VISIBLE"
        else:
            rel="GOVERNANCE_VISIBLE"
        rows.append({"path":p,"git_blob":tree[p]["git_blob"],"relevance_disposition":rel,"discovery_origin":sorted(origins.get(p,{"REFERENCE_CLOSURE"}))})
    return rows

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")

baseline=readj("evidence/bpesem03/governed_semantic_evidence_baseline_v0_1.json")
persist=readj("evidence/bpesem03/baseline_persistence_record_v0_1.json")
claimreg=readj("evidence/bpesem03/claim_dimension_register_v0_1.json")
basisreg=readj("evidence/bpesem03/dimension_authority_basis_register_v0_1.json")
scope=readj("evidence/bpesem03/operational_semantic_scope_signature_v0_1.json")
rule=readj("evidence/bpesem03/signedness_equivalence_rule_v0_1.json")
oblig=readj("evidence/bpesem03/execution_obligation_set_v0_1.json")
bpe02=readj("evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json")
bpe03=readj("evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json")
berd_exec=readj("evidence/berd02/gha_run_35533153289/execution_result.json")
berd_prov=readj("evidence/berd02/gha_run_35533153289/PROVENANCE.json")

if baseline["parent_relation_status"]!="PASS":
    raise RuntimeError("baseline persistence relation not PASS")
if baseline["baseline_digest"]!=persist["baseline_digest"]:
    raise RuntimeError("baseline persistence digest mismatch")

all_dims=[]
dim_to_claim={}
for c in claimreg["claims"]:
    for d in c["mandatory_dimensions"]:
        all_dims.append(d["dimension_id"])
        dim_to_claim[d["dimension_id"]]=c["claim_id"]
if len(all_dims)!=26 or len(set(all_dims))!=26:
    raise RuntimeError("unexpected dimension register cardinality")

# Existing evidence records, preserved without upgrading their original truth.
evidence_records=[]
for s in bpe02["sources"]:
    cls={"EC-P1":"OS-E-P1","EC-P2":"OS-E-P2","EC-I1":"OS-E-I1","EC-I2":"OS-E-I2","EC-PROJECT":"OS-E-PROJECT"}.get(s["evidence_class"],s["evidence_class"])
    evidence_records.append({
        "evidence_id":s["evidence_id"],
        "evidence_class":cls,
        "publisher_or_origin_identity":s["publisher_identity"],
        "title_or_repository":s["source_title_or_repository"],
        "exact_locator":s["source_locator"],
        "source_version_or_commit":s["source_version_or_commit"],
        "exact_content_sha256":s["content_integrity_digest"],
        "declared_representation_scope":s["declared_representation_scope"],
        "declared_instrument_scope":s["declared_instrument_scope"],
        "declared_temporal_scope":s["declared_temporal_scope"],
        "project_origin_status":s["project_origin_check"],
        "semantic_source_lineage_id":s["evidence_lineage_candidate_id"],
        "origin_bundle":"BPE02",
    })

for s in bpe03["sources"]:
    if any(e["evidence_id"]==s["evidence_id"] for e in evidence_records):
        continue
    evidence_records.append({
        "evidence_id":s["evidence_id"],
        "evidence_class":"OS-E-P1" if s["evidence_class"]=="EC-P1" else "OS-E-I2",
        "publisher_or_origin_identity":s["publisher_identity"],
        "title_or_repository":s["source_title_or_repository"],
        "exact_locator":s["source_locator"],
        "source_version_or_commit":s["source_version_or_commit"],
        "exact_content_sha256":s["content_integrity_digest"],
        "declared_representation_scope":s["declared_representation_scope"],
        "declared_instrument_scope":s["declared_instrument_scope"],
        "declared_temporal_scope":s["declared_temporal_scope"],
        "project_origin_status":s["project_origin_check"],
        "semantic_source_lineage_id":s["evidence_lineage_candidate_id"],
        "origin_bundle":"BPE03",
    })

evidence_records.append({
    "evidence_id":"BPESEM03-E-BERD02-K1-BOUNDED",
    "evidence_class":"OS-E-P3",
    "publisher_or_origin_identity":"DUKASCOPY_PROVIDER_DIRECT_BYTES_CAPTURED_BY_PROJECT",
    "title_or_repository":"BERD02-GHA-35533153289-1 bounded K1 provider bytes",
    "exact_locator":"evidence/berd02/gha_run_35533153289/",
    "source_version_or_commit":berd_exec["source_head"],
    "exact_content_sha256":berd_prov["artifact_digest"].replace("sha256:",""),
    "declared_representation_scope":"BOUNDED_K1_PROVIDER_DIRECT_PHYSICAL_COMPATIBILITY",
    "declared_instrument_scope":"USATECHIDXUSD",
    "declared_temporal_scope":"PW_PLUS_P0_P7_ONLY",
    "project_origin_status":"PROVIDER_BYTES_PROJECT_CAPTURE_METADATA",
    "semantic_source_lineage_id":"LINEAGE-DUKASCOPY-PROVIDER-BYTES",
    "origin_bundle":"BERD02",
})

# Operational admissibility decisions.
bpe02_dec={d["evidence_id"]:d for d in bpe02["admissibility_decisions"]}
bpe03_dec={d["evidence_id"]:d for d in bpe03["admissibility_decisions"]}
op_decisions=[]
for e in evidence_records:
    eid=e["evidence_id"]
    if eid=="BPESEM03-E-BERD02-K1-BOUNDED":
        status="ADMISSIBLE"; reasons=["EXACT_PROVIDER_DIRECT_BOUNDED_BYTES_AND_RESULT_SEALED","BOUNDED_COMPATIBILITY_ONLY"]
        imm="EXACT_ARTIFACT_DIGEST_AND_RESULT_SEAL"; prov="PASS"; proj="PROJECT_CAPTURE_NOT_PROJECT_SEMANTIC_SOURCE"; lin="PROVIDER_DIRECT_BYTES"
    elif eid in bpe02_dec:
        d=bpe02_dec[eid]
        status=d["decision_status"]
        reasons=list(d["reason_codes"])
        imm=d["immutability_status"]; prov=d["provenance_status"]; proj=d["project_origin_status"]; lin=d["lineage_precheck_status"]
    elif eid in bpe03_dec:
        d=bpe03_dec[eid]
        status=d["decision_status"]
        reasons=list(d["reason_codes"])
        imm=d["immutability_status"]; prov=d["provenance_status"]; proj=d["project_origin_status"]; lin=d["lineage_precheck_status"]
    else:
        status="BLOCKED"; reasons=["NO_INHERITED_ADMISSIBILITY_DECISION"]
        imm="BLOCKED"; prov="BLOCKED"; proj="BLOCKED"; lin="BLOCKED"
    dec={
        "schema":"B_PE_SEM_02_EVIDENCE_ADMISSIBILITY_DECISION_V0_2",
        "decision_id":"BPESEM03-ADM-"+eid,
        "evidence_id":eid,
        "evidence_exact_content_sha256":e["exact_content_sha256"],
        "contract_id":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY",
        "contract_version":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_6_CORRECTED",
        "scope_signature_id":scope["scope_signature_id"],
        "evidence_class":e["evidence_class"],
        "immutability_status":imm,
        "provenance_status":prov,
        "project_origin_status":proj,
        "semantic_source_lineage_status":lin,
        "declared_scope_status":e["declared_representation_scope"],
        "decision_status":status,
        "reason_codes":reasons,
        "reviewer_identity":"B-PE-SEM-03_GOVERNED_ADJUDICATION",
        "created_at_utc":"2026-09-21T20:30:00Z",
    }
    dec["decision_seal"]=seal(dec,"decision_seal")
    op_decisions.append(dec)

dec_by_eid={d["evidence_id"]:d for d in op_decisions}
ev_by_id={e["evidence_id"]:e for e in evidence_records}

# Inherited lineage: preserve unresolved third-party pairwise semantic independence.
lineage={
    "lineage_resolution_id":"BPESEM03-SEMANTIC-LINEAGE-V0_1",
    "covered_evidence_ids":sorted(e["evidence_id"] for e in evidence_records),
    "covered_semantic_source_ids":sorted(set(e["semantic_source_lineage_id"] for e in evidence_records)),
    "lineage_groups":{
        "LINEAGE-DUKASCOPY":["BPE02-E01","BPE02-E02","BPE03-E01-DUKASCOPY-API-SUPPORT-2013","BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE","BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE","BPESEM03-E-BERD02-K1-BOUNDED"],
        "LINEAGE-DUKA-DATA":["BPE02-E03"],
        "LINEAGE-NINETY47":["BPE02-E04","BPE02-E05"],
        "LINEAGE-LEOCLC":["BPE02-E06","BPE02-E07","BPE02-E08","BPE02-E09","BPE02-E10"],
        "LINEAGE-PROJECT":["BPE02-E11"],
    },
    "pairwise_relationships":{
        "DUKASCOPY::DUKA-DATA":"INDEPENDENT",
        "DUKASCOPY::NINETY47":"INDEPENDENT",
        "DUKASCOPY::LEOCLC":"INDEPENDENT",
        "DUKA-DATA::NINETY47":"UNRESOLVED",
        "DUKA-DATA::LEOCLC":"UNRESOLVED",
        "NINETY47::LEOCLC":"UNRESOLVED",
        "PROJECT::*":"DISQUALIFIED",
    },
    "relationship_proof_refs":[
        "evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json",
        "evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json",
    ],
    "project_origin_checks":["BPE02-E11 rejected as project circular","E03-E10 non-project exact-revision sources"],
    "reviewer_identity":"B-PE-SEM-03_GOVERNED_ADJUDICATION",
    "created_at_utc":"2026-09-21T20:30:00Z",
}
lineage["lineage_resolution_digest"]=seal(lineage,"lineage_resolution_digest")

# B-ERD-02 historical evidence may remain visible but cannot decisively discriminate
# newly materialized exact C01-C07 semantic hypotheses.
physical_dims=[b["dimension_id"] for b in basisreg["dimension_bases"] if b["primary_authority_class"]=="PHYSICAL_HYPOTHESIS"]
hist_records=[]
for dim in physical_dims:
    rec={
        "schema":"B_PE_SEM_02_HISTORICAL_OBSERVATION_ELIGIBILITY_V0_2",
        "eligibility_id":"BPESEM03-HIST-BERD02-"+dim,
        "historical_execution_id":"BERD02-GHA-35533153289-1",
        "historical_source_head":berd_exec["source_head"],
        "historical_observed_at_utc":berd_exec["created_at_utc"],
        "historical_evidence_ids":["BPESEM03-E-BERD02-K1-BOUNDED"],
        "target_dimension_id":dim,
        "proposed_hypothesis_set_id":"BPESEM03-HYP-"+dim,
        "proposed_discriminator_ids":["BERD02-DIAGNOSTIC-A","BERD02-DIAGNOSTIC-B"],
        "pre_observation_artifact_refs":[
            "reports/data-qualification/berd01_bounded_empirical_representation_discrimination_contract_candidate_2026-09-20.md",
            "evidence/berd02/probe_plan_v0_1.json",
            "tools/berd02_transport_runner.py",
        ],
        "pre_observation_artifact_hashes":[
            "ac83ff40c080913de29ba74c3b7423a8f858c2fd",
            "4aae1736f0bb165dbcdd171b8ce8613f51295413",
            "e10a0c47ec6e9b28f480c958baf18141287187cb",
        ],
        "pre_observation_commit_or_time":berd_exec["source_head"],
        "equivalence_mapping_rationale":"B-ERD-01 precommitted K1 representation-family discrimination and diagnostics, but not the exact later B-PE-SEM-02 per-dimension semantic hypothesis set.",
        "post_hoc_broadening_check":"EXACT_C01_C07_HYPOTHESIS_IDENTITY_NOT_PRECOMMITTED",
        "eligibility_role":"NONDECISIVE_COMPATIBILITY",
        "decisive_discrimination_eligible":False,
        "status":"PASS",
        "reason_codes":["BOUNDED_COMPATIBILITY_REUSE_ALLOWED","DECISIVE_SEMANTIC_DISCRIMINATION_NOT_PRECOMMITTED"],
    }
    rec["eligibility_seal"]=seal(rec,"eligibility_seal")
    hist_records.append(rec)

# Scope applicability is conditional semantic-rule applicability only; it never proves C08 presence.
scope_decisions=[]
for dim in all_dims:
    if dim in {"C03-D3-OP","C05-D2-OP"}:
        st="PASS"; reasons=["UNIVERSAL_32BIT_MATHEMATICAL_EQUIVALENCE_RULE","REPRESENTATION_PRESENCE_NOT_REQUIRED_FOR_RULE_AUTHORITY"]
    else:
        st="BLOCKED"; reasons=["TARGET_K1_SEMANTIC_RULE_CONTINUITY_2021_2026_NOT_ESTABLISHED","BOUNDED_COMPATIBILITY_NE_FULL_SEMANTIC_SCOPE_AUTHORITY"]
    sd={
        "schema":"B_PE_SEM_02_SEMANTIC_RULE_SCOPE_APPLICABILITY_DECISION_V0_1",
        "scope_decision_id":"BPESEM03-SCOPE-"+dim,
        "dimension_id":dim,
        "target_scope_signature_id":scope["scope_signature_id"],
        "target_scope_signature_digest":scope["scope_signature_digest"],
        "source_representation_scope":"EXISTING_GOVERNED_EVIDENCE_ONLY",
        "source_instrument_scope":"USATECHIDXUSD_WHERE_AVAILABLE",
        "source_temporal_scope":"BOUNDED_OR_IMPLEMENTATION_EPOCHS; NO COMPLETE 2021_2026 SEMANTIC CONTINUITY PROOF",
        "continuity_or_equivalence_proof_refs":[],
        "uncovered_scope_segments":[] if st=="PASS" else ["UNPROVEN_COMPLETE_TARGET_EPOCH_SEMANTIC_RULE_CONTINUITY"],
        "contradictory_scope_evidence_ids":[],
        "representation_presence_authority":"NOT_ADJUDICATED_IN_B_PE_SEM_03",
        "c08_authority_effect":"NONE",
        "status":st,
        "reason_codes":reasons,
        "reviewer_identity":"B-PE-SEM-03_GOVERNED_ADJUDICATION",
        "created_at_utc":"2026-09-21T20:30:00Z",
    }
    sd["scope_decision_seal"]=seal(sd,"scope_decision_seal")
    scope_decisions.append(sd)
scope_by_dim={x["dimension_id"]:x for x in scope_decisions}

# Map inherited documentary assertions into visibility only.
assertions=bpe02["claim_evidence_assertions"]
vis=[]
pos=[]
anchors=[]
known_regs=[]
hyp_sets=[]
review_universes=[]

def old_dim(newdim:str)->str:
    return newdim.replace("-OP","")

for dim in all_dims:
    od=old_dim(dim)
    rel=[a for a in assertions if a["dimension_id"]==od]
    visible=[]
    for a in rel:
        dec=dec_by_eid.get(a["evidence_id"])
        if a["scope_mapping"] in {"CURRENT_DAILY_ONLY","CURRENT_CFD_ONLY"}:
            disp="WRONG_SCOPE_PROVEN"
        elif a["stance"]=="CONTRADICT":
            disp="MATERIAL_ALTERNATIVE"
        else:
            disp="SUPPORTING_SAME_PROPOSITION"
        visible.append({
            "visible_item_id":"VIS-"+a["assertion_id"],
            "evidence_or_assertion_ref":a["assertion_id"],
            "evidence_id":a["evidence_id"],
            "exact_content_identity":ev_by_id[a["evidence_id"]]["exact_content_sha256"],
            "normalized_interpretation_if_any":a["normalized_proposition"],
            "visibility_disposition":disp,
            "controlling_decision_refs":[dec["decision_id"]] if dec else [],
        })
    # preserve BPE03 temporal continuity limitation as governance-visible for every non-math rule.
    if dim not in {"C03-D3-OP","C05-D2-OP"}:
        visible.append({
            "visible_item_id":"VIS-BPE03-CONTINUITY-"+dim,
            "evidence_or_assertion_ref":"BPE03-C08-D5-BLOCKED-CONTINUITY-LIMITATION",
            "evidence_id":"BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE",
            "exact_content_identity":ev_by_id["BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE"]["exact_content_sha256"],
            "normalized_interpretation_if_any":"Provider client releases do not prove legacy-hourly BI5 semantic continuity through 2021-2026.",
            "visibility_disposition":"GOVERNANCE_CONSTRAINT",
            "controlling_decision_refs":["ADM-BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE"],
        })
    vu={
        "visibility_universe_id":"BPESEM03-VIS-"+dim,
        "baseline_id":baseline["baseline_id"],
        "baseline_digest":baseline["baseline_digest"],
        "target_dimension_id":dim,
        "visible_items":visible,
    }
    vu["visibility_universe_digest"]=seal(vu,"visibility_universe_digest")
    vis.append(vu)

    # Positive authority requires scope PASS. Non-math dimensions therefore have no positive items yet.
    items=[]
    if scope_by_dim[dim]["status"]=="PASS":
        items=[]
    pu={
        "positive_authority_universe_id":"BPESEM03-POS-"+dim,
        "target_dimension_id":dim,
        "visibility_universe_id":vu["visibility_universe_id"],
        "visibility_universe_digest":vu["visibility_universe_digest"],
        "positive_authority_items":items,
    }
    pu["positive_authority_universe_digest"]=seal(pu,"positive_authority_universe_digest")
    pos.append(pu)

    candidates=[]
    for it in visible:
        if it["visibility_disposition"]=="MATERIAL_ALTERNATIVE":
            candidates.append({
                "candidate_id":"ALT-"+it["visible_item_id"],
                "normalized_interpretation":it["normalized_interpretation_if_any"],
                "material_effect_if_true":"MATERIAL_UNDER_M01_M17_UNLESS_CONDITIONAL_RULE_RESOLVES_INSTANCE",
                "evidence_refs":[it["evidence_or_assertion_ref"]],
                "disposition":"INCLUDED_MATERIAL_HYPOTHESIS",
                "disposition_rationale":"Existing governed contradictory/alternative interpretation remains visible.",
            })
    if dim in {"C03-D3-OP","C05-D2-OP"}:
        candidates=[
            {"candidate_id":"SIGNED_INT32","normalized_interpretation":"Affected 32-bit field interpreted signed","material_effect_if_true":"DIFFERS_WHEN_HIGH_BIT_ONE","evidence_refs":["AST-BPE02-E03-C03-D3-CONTRADICT","AST-BPE02-E06-C03-D3-CONTRADICT"],"disposition":"INCLUDED_MATERIAL_HYPOTHESIS","disposition_rationale":"Existing independent references use signed integers."},
            {"candidate_id":"UNSIGNED_UINT32","normalized_interpretation":"Affected 32-bit field interpreted unsigned","material_effect_if_true":"DIFFERS_WHEN_HIGH_BIT_ONE","evidence_refs":["AST-BPE02-E04-C03-D3-SUPPORT"],"disposition":"INCLUDED_MATERIAL_HYPOTHESIS","disposition_rationale":"Existing independent reference uses unsigned integers."},
        ]
    reviewed_ids=sorted(set(it["evidence_id"] for it in visible if it.get("evidence_id")))
    contradiction_ids=sorted(set(it["evidence_id"] for it in visible if it.get("evidence_id") and it["visibility_disposition"] in {"MATERIAL_ALTERNATIVE","MATERIAL_CONTRADICTION"}))
    mandatory_refs=[
        "evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json",
        "evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json",
        "reports/data-qualification/bpe01r_empirical_evidence_sufficiency_final_rebreak_2026-09-21.md",
        "reports/data-qualification/bpesem01_semantic_authority_route_review_final_rebreak_2026-09-21.md",
        "evidence/bfiq02/semantic_invariant_manifest_v0_1.json",
    ]
    if basisreg and next(x for x in basisreg["dimension_bases"] if x["dimension_id"]==dim)["primary_authority_class"]=="PHYSICAL_HYPOTHESIS":
        mandatory_refs += [
            "evidence/berd02/gha_run_35533153289/PROVENANCE.json",
            "evidence/berd02/gha_run_35533153289/execution_result.json",
        ]
    ru={
        "schema":"B_PE_SEM_02_SEMANTIC_EVIDENCE_REVIEW_UNIVERSE_V0_3",
        "review_universe_id":"BPESEM03-REVIEW-"+dim,
        "target_dimension_id":dim,
        "cutoff_head":HEAD,
        "cutoff_time":"2026-09-21T20:30:00Z",
        "governed_semantic_evidence_baseline_id":baseline["baseline_id"],
        "governed_semantic_evidence_baseline_digest":baseline["baseline_digest"],
        "mandatory_inherited_evidence_refs":mandatory_refs,
        "current_adjudication_evidence_ids":reviewed_ids,
        "reopen_or_contradiction_evidence_ids":contradiction_ids,
        "exclusion_decisions":[],
        "effective_review_evidence_ids":reviewed_ids,
    }
    ru["review_universe_digest"]=seal(ru,"review_universe_digest")
    review_universes.append(ru)

    # Bind the visibility/positive projections to the exact review universe they derive from.
    vu["semantic_evidence_review_universe_id"]=ru["review_universe_id"]
    vu["semantic_evidence_review_universe_digest"]=ru["review_universe_digest"]
    vu["visibility_universe_digest"]=seal(vu,"visibility_universe_digest")
    pu["visibility_universe_digest"]=vu["visibility_universe_digest"]
    pu["positive_authority_universe_digest"]=seal(pu,"positive_authority_universe_digest")

    kr={
        "schema":"B_PE_SEM_02_KNOWN_MATERIAL_ALTERNATIVES_V0_2",
        "registry_id":"BPESEM03-KNOWN-ALT-"+dim,
        "target_dimension_id":dim,
        "semantic_evidence_review_universe_id":ru["review_universe_id"],
        "semantic_evidence_review_universe_digest":ru["review_universe_digest"],
        "evidence_review_cutoff_head":HEAD,
        "evidence_review_cutoff_time":"2026-09-21T20:30:00Z",
        "reviewed_evidence_ids":reviewed_ids,
        "candidate_interpretations":candidates,
        "included_hypothesis_ids":[x["candidate_id"] for x in candidates],
        "unresolved_candidate_ids":[],
    }
    kr["registry_digest"]=seal(kr,"registry_digest")
    known_regs.append(kr)

    basis=next(x for x in basisreg["dimension_bases"] if x["dimension_id"]==dim)
    if basis["primary_authority_class"]=="PHYSICAL_HYPOTHESIS":
        hypotheses=[{
            "hypothesis_id":"REGISTERED_PROPOSITION",
            "exact_interpretation":next(d["exact_dimension_proposition"] for c in claimreg["claims"] for d in c["mandatory_dimensions"] if d["dimension_id"]==dim),
            "material_effect_if_true":"GOVERNS_PHYSICAL_DECODING",
            "discriminator_ids":["EXISTING_REFERENCE_IMPLEMENTATIONS","BERD02_BOUNDED_NONDECISIVE_COMPATIBILITY"],
            "required_anchor_ids":[],
            "contradiction_condition":"ADMISSIBLE_TARGET_SCOPE_EVIDENCE_ESTABLISHES_DISTINCT_PHYSICAL_RULE",
        }]
        for c in candidates:
            hypotheses.append({
                "hypothesis_id":c["candidate_id"],
                "exact_interpretation":c["normalized_interpretation"],
                "material_effect_if_true":c["material_effect_if_true"],
                "discriminator_ids":["EXISTING_GOVERNED_EVIDENCE"],
                "required_anchor_ids":[],
                "contradiction_condition":"N/A",
            })
        hs={
            "schema":"B_PE_SEM_02_SEMANTIC_HYPOTHESIS_SET_V0_1",
            "hypothesis_set_id":"BPESEM03-HYP-"+dim,
            "contract_id":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY",
            "contract_version":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_6_CORRECTED",
            "scope_signature_id":scope["scope_signature_id"],
            "target_claim_id":dim_to_claim[dim],
            "target_dimension_id":dim,
            "known_material_alternative_registry_id":kr["registry_id"],
            "known_material_alternative_registry_digest":kr["registry_digest"],
            "hypothesis_records":hypotheses,
            "completeness_rationale":"All currently visible governed material alternatives are retained; open-world reopen remains active.",
            "open_world_rule":"NEW_MATERIAL_INTERPRETATION_OPENS_REOPEN_AND_BLOCKS_CURRENT_AUTHORITY",
            "decision_rule":"EXACTLY_ONE_SURVIVING_MATERIAL_HYPOTHESIS_REQUIRED_FOR_PASS",
            "current_discrimination_status":"BLOCKED_NO_DECISIVE_PREOBSERVATION_TARGET_HYPOTHESIS_DISCRIMINATION",
            "created_at_utc":"2026-09-21T20:30:00Z",
        }
        hs["hypothesis_set_seal"]=seal(hs,"hypothesis_set_seal")
        hyp_sets.append(hs)

# Semantic anchors from inherited explicit independent assertions remain visible,
# but are blocked as current semantic authority because full target semantic scope is unresolved.
semantic_dims=[b["dimension_id"] for b in basisreg["dimension_bases"] if b["primary_authority_class"] in {"SEMANTIC_ANCHOR","PREREQUISITE_CLOSURE"}]
for dim in semantic_dims:
    od=old_dim(dim)
    rel=[a for a in assertions if a["dimension_id"]==od and a["stance"]=="SUPPORT" and dec_by_eid.get(a["evidence_id"],{}).get("decision_status")=="ADMISSIBLE"]
    for i,a in enumerate(rel):
        an={
            "schema":"B_PE_SEM_02_SEMANTIC_ANCHOR_MANIFEST_V0_1",
            "anchor_manifest_id":"BPESEM03-ANCHOR-"+dim+"-"+str(i+1),
            "anchor_id":"ANCHOR-"+a["assertion_id"],
            "anchor_class":"INDEPENDENT_NONPROJECT_REFERENCE_IMPLEMENTATION",
            "evidence_id":a["evidence_id"],
            "evidence_exact_sha256":ev_by_id[a["evidence_id"]]["exact_content_sha256"],
            "source_version_or_commit":ev_by_id[a["evidence_id"]]["source_version_or_commit"],
            "immutable_materialization_ref":"evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json",
            "provenance_status":"PASS",
            "project_origin_status":"NON_PROJECT",
            "semantic_source_lineage_id":ev_by_id[a["evidence_id"]]["semantic_source_lineage_id"],
            "semantic_source_identity":"REFERENCE_IMPLEMENTATION_EXPLICIT_BEHAVIOR",
            "semantic_source_relationship_proof_refs":["BPE02-LINEAGE-V0_2"],
            "target_claim_id":dim_to_claim[dim],
            "target_dimension_id":dim,
            "normalized_semantic_proposition":a["normalized_proposition"],
            "hypothesis_set_id_if_applicable":None,
            "expected_discriminator":"EXPLICIT_IMPLEMENTATION_SEMANTICS",
            "contradiction_condition":"MATERIAL_TARGET_SCOPE_CONFLICT",
            "ambiguity_condition":"TARGET_EPOCH_SCOPE_OR_SEMANTIC_SOURCE_AUTHORITY_UNRESOLVED",
            "failure_disposition":"BLOCKED",
            "admissibility_status":"BLOCKED",
            "admissibility_reason_codes":["SEMANTIC_RULE_SCOPE_APPLICABILITY_BLOCKED","REFERENCE_IMPLEMENTATION_NOT_SUFFICIENT_AS_SOLE_CURRENT_SEMANTIC_AUTHORITY"],
            "created_at_utc":"2026-09-21T20:30:00Z",
        }
        an["anchor_manifest_seal"]=seal(an,"anchor_manifest_seal")
        anchors.append(an)

# Exact dimension adjudication.
dimension_adjudications=[]
for dim in all_dims:
    basis=next(x for x in basisreg["dimension_bases"] if x["dimension_id"]==dim)
    if dim in {"C03-D3-OP","C05-D2-OP"}:
        status="PASS"
        reasons=["SIGNEDNESS_EQUIVALENCE_RULE_V0_1_CURRENT","NONWAIVABLE_HIGH_BIT_ZERO_EXECUTION_OBLIGATION_BOUND","MATHEMATICAL_RULE_SCOPE_PASS"]
        rules=[rule["rule_id"]]
        obligations_for_dim=[o for o in oblig["obligations"] if o["source_dimension_id"]==dim]
    elif basis["primary_authority_class"]=="PREREQUISITE_CLOSURE":
        status="BLOCKED"
        reasons=["PREREQUISITE_AUTHORITY_NOT_ALL_PASS","SEMANTIC_RULE_SCOPE_APPLICABILITY_BLOCKED"]
        if dim=="C06-D3-OP":
            reasons.append("NONCIRCULAR_USATECH_SCALE_AUTHORITY_NOT_CURRENT")
        rules=[]; obligations_for_dim=[]
    elif basis["primary_authority_class"]=="SEMANTIC_ANCHOR":
        status="BLOCKED"
        reasons=["SEMANTIC_RULE_SCOPE_APPLICABILITY_BLOCKED"]
        if not any(a["target_dimension_id"]==dim for a in anchors):
            reasons.append("ADMISSIBLE_CURRENT_SEMANTIC_ANCHOR_ABSENT")
        else:
            reasons.append("REFERENCE_IMPLEMENTATION_ANCHORS_NONCURRENT_FOR_TARGET_EPOCH")
        rules=[]; obligations_for_dim=[]
    else:
        status="BLOCKED"
        reasons=["SEMANTIC_RULE_SCOPE_APPLICABILITY_BLOCKED","NO_DECISIVE_PREOBSERVATION_PHYSICAL_HYPOTHESIS_DISCRIMINATION"]
        rules=[]; obligations_for_dim=[]
    drec={
        "dimension_id":dim,
        "dimension_class":basis["primary_authority_class"],
        "proposition":next(d["exact_dimension_proposition"] for c in claimreg["claims"] for d in c["mandatory_dimensions"] if d["dimension_id"]==dim),
        "evidence_ids":sorted(set(it.get("evidence_id") for v in vis if v["target_dimension_id"]==dim for it in v["visible_items"] if it.get("evidence_id"))),
        "anchor_ids":[a["anchor_id"] for a in anchors if a["target_dimension_id"]==dim],
        "hypothesis_set_ids":[h["hypothesis_set_id"] for h in hyp_sets if h["target_dimension_id"]==dim],
        "rule_ids":rules,
        "scope_mapping":scope["scope_signature_id"],
        "scope_decision_id":scope_by_dim[dim]["scope_decision_id"],
        "contradiction_state":"SIGNEDNESS_CONDITIONALIZED" if dim in {"C03-D3-OP","C05-D2-OP"} else "NO_AUTHORITATIVE_FAIL_CONTRADICTION",
        "execution_obligations":obligations_for_dim,
        "status":status,
        "reason_codes":reasons,
    }
    dimension_adjudications.append(drec)

status_by_dim={d["dimension_id"]:d["status"] for d in dimension_adjudications}
claim_adjudications=[]
for c in claimreg["claims"]:
    dims=[d["dimension_id"] for d in c["mandatory_dimensions"]]
    vals=[status_by_dim[d] for d in dims]
    st="FAIL" if "FAIL" in vals else ("PASS" if all(x=="PASS" for x in vals) else "BLOCKED")
    reasons=[] if st=="PASS" else ["ONE_OR_MORE_MANDATORY_DIMENSIONS_NOT_PASS"]
    claim_adjudications.append({"claim_id":c["claim_id"],"mandatory_dimension_ids":dims,"status":st,"reason_codes":reasons})

# Integrity projections.
evidence_set_digest=digest(sorted([
    {"evidence_id":e["evidence_id"],"evidence_exact_content_sha256":e["exact_content_sha256"],"admissibility_decision_id":dec_by_eid[e["evidence_id"]]["decision_id"],"admissibility_decision_seal":dec_by_eid[e["evidence_id"]]["decision_seal"]}
    for e in evidence_records
],key=lambda x:canon(x)))
anchor_set_digest=digest(sorted([
    {"anchor_manifest_id":a["anchor_manifest_id"],"anchor_id":a["anchor_id"],"target_dimension_id":a["target_dimension_id"],"evidence_id":a["evidence_id"],"evidence_exact_sha256":a["evidence_exact_sha256"],"anchor_manifest_seal":a["anchor_manifest_seal"]}
    for a in anchors
],key=lambda x:canon(x)))
hypothesis_set_digest=digest(sorted([
    {"hypothesis_set_id":h["hypothesis_set_id"],"target_dimension_id":h["target_dimension_id"],"known_material_alternative_registry_id":h["known_material_alternative_registry_id"],"known_material_alternative_registry_digest":h["known_material_alternative_registry_digest"],"hypothesis_set_seal":h["hypothesis_set_seal"]}
    for h in hyp_sets
],key=lambda x:canon(x)))
rule_set_digest=digest([{"rule_id":rule["rule_id"],"rule_seal":rule["rule_seal"]}])
scope_set_digest=digest(sorted([
    {"scope_decision_id":s["scope_decision_id"],"dimension_id":s["dimension_id"],"target_scope_signature_id":s["target_scope_signature_id"],"scope_decision_seal":s["scope_decision_seal"]}
    for s in scope_decisions
],key=lambda x:canon(x)))
hist_set_digest=digest(sorted([
    {"eligibility_id":h["eligibility_id"],"historical_execution_id":h["historical_execution_id"],"target_dimension_id":h["target_dimension_id"],"eligibility_role":h["eligibility_role"],"eligibility_seal":h["eligibility_seal"]}
    for h in hist_records
],key=lambda x:canon(x)))
lineage_set_digest=digest([{"lineage_resolution_id":lineage["lineage_resolution_id"],"lineage_resolution_digest":lineage["lineage_resolution_digest"]}])

# Evidence horizon at candidate materialization parent: rescan the actual candidate parent HEAD.
current_horizon_rows=current_discovery(HEAD,[
    "evidence/bpe",
    "reports/data-qualification/bpe",
    "evidence/berd",
    "reports/data-qualification/berd",
    "evidence/bfiq",
    "reports/data-qualification/bfiq",
])
horizon={
    "schema":"B_PE_SEM_02_SEMANTIC_EVIDENCE_HORIZON_V0_1",
    "horizon_id":"BPESEM03-EVIDENCE-HORIZON-V0_1",
    "adjudication_id":"BPESEM03-OPERATIONAL-SEMANTIC-ADJUDICATION-V0_1",
    "cutoff_head":HEAD,
    "cutoff_tree_sha":TREE,
    "discovery_policy_id":baseline["discovery_policy_id"],
    "discovery_policy_digest":baseline["discovery_policy_digest"],
    "governed_baseline_id":baseline["baseline_id"],
    "governed_baseline_digest":baseline["baseline_digest"],
    "discovered_semantic_artifact_refs":[{"path":x["path"],"git_blob":x["git_blob"],"relevance_disposition":x["relevance_disposition"]} for x in current_horizon_rows],
}
horizon["horizon_digest"]=seal(horizon,"horizon_digest")

adjudication={
    "schema":"B_PE_SEM_02_OPERATIONAL_SEMANTIC_RULE_ADJUDICATION_V0_1",
    "adjudication_id":"BPESEM03-OPERATIONAL-SEMANTIC-ADJUDICATION-V0_1",
    "contract_id":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY",
    "contract_version":"B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_6_CORRECTED",
    "claim_dimension_register_id":claimreg["register_id"],
    "claim_dimension_register_digest":claimreg["register_digest"],
    "dimension_authority_basis_register_id":basisreg["basis_register_id"],
    "dimension_authority_basis_register_digest":basisreg["basis_register_digest"],
    "scope_signature_id":scope["scope_signature_id"],
    "scope_signature_digest":scope["scope_signature_digest"],
    "governed_semantic_evidence_baseline_id":baseline["baseline_id"],
    "governed_semantic_evidence_baseline_digest":baseline["baseline_digest"],
    "discovery_policy_id":baseline["discovery_policy_id"],
    "discovery_policy_digest":baseline["discovery_policy_digest"],
    "discovery_result_digest":baseline["discovery_result_digest"],
    "semantic_evidence_review_universe_ids":[x["review_universe_id"] for x in review_universes],
    "semantic_evidence_review_universe_digests":[x["review_universe_digest"] for x in review_universes],
    "visibility_universe_ids":[x["visibility_universe_id"] for x in vis],
    "visibility_universe_digests":[x["visibility_universe_digest"] for x in vis],
    "positive_authority_universe_ids":[x["positive_authority_universe_id"] for x in pos],
    "positive_authority_universe_digests":[x["positive_authority_universe_digest"] for x in pos],
    "evidence_records":evidence_records,
    "evidence_admissibility_decisions":op_decisions,
    "semantic_anchor_manifests":anchors,
    "semantic_hypothesis_sets":hyp_sets,
    "known_material_alternative_registries":known_regs,
    "semantic_scope_applicability_decisions":scope_decisions,
    "historical_observation_eligibility_records":hist_records,
    "lineage_resolution_records":[lineage],
    "rule_records":[rule],
    "dimension_adjudications":dimension_adjudications,
    "claim_adjudications":claim_adjudications,
    "overall_operational_semantic_status":"BLOCKED",
    "execution_obligation_set":oblig["obligations"],
    "evidence_set_digest":evidence_set_digest,
    "anchor_set_digest":anchor_set_digest,
    "hypothesis_set_digest":hypothesis_set_digest,
    "rule_set_digest":rule_set_digest,
    "scope_applicability_set_digest":scope_set_digest,
    "historical_eligibility_set_digest":hist_set_digest,
    "lineage_resolution_set_digest":lineage_set_digest,
    "obligation_set_digest":oblig["obligation_set_digest"],
    "semantic_evidence_horizon_id":horizon["horizon_id"],
    "semantic_evidence_horizon_digest":horizon["horizon_digest"],
    "supersedes_adjudication_id":None,
    "adjudication_status":"BLOCKED",
    "created_at_utc":"2026-09-21T20:30:00Z",
    "adjudicator_identity":"B-PE-SEM-03_GOVERNED_ADJUDICATION",
}
adjudication["adjudication_seal"]=seal(adjudication,"adjudication_seal")

# Persist component groups.
write_json("operational_evidence_records_and_admissibility_v0_1.json",{"evidence_records":evidence_records,"admissibility_decisions":op_decisions,"evidence_set_digest":evidence_set_digest})
write_json("semantic_lineage_resolution_v0_1.json",lineage)
write_json("historical_observation_eligibility_v0_1.json",{"records":hist_records,"historical_eligibility_set_digest":hist_set_digest})
write_json("semantic_rule_scope_applicability_v0_1.json",{"decisions":scope_decisions,"scope_applicability_set_digest":scope_set_digest})
write_json("semantic_evidence_review_universes_v0_1.json",{"universes":review_universes})
write_json("visibility_universes_v0_1.json",{"universes":vis})
write_json("positive_authority_universes_v0_1.json",{"universes":pos})
write_json("known_material_alternative_registries_v0_1.json",{"registries":known_regs})
write_json("semantic_hypothesis_sets_v0_1.json",{"hypothesis_sets":hyp_sets,"hypothesis_set_digest":hypothesis_set_digest})
write_json("semantic_anchor_manifests_v0_1.json",{"anchors":anchors,"anchor_set_digest":anchor_set_digest})
write_json("semantic_evidence_horizon_v0_1.json",horizon)
write_json("operational_semantic_rule_adjudication_v0_1.json",adjudication)

pass_dims=[d["dimension_id"] for d in dimension_adjudications if d["status"]=="PASS"]
blocked_dims=[d["dimension_id"] for d in dimension_adjudications if d["status"]=="BLOCKED"]
failed_dims=[d["dimension_id"] for d in dimension_adjudications if d["status"]=="FAIL"]

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(
    "# B-PE-SEM-03 — OPERATIONAL C01-C07 SEMANTIC AUTHORITY — CANDIDATE\\n\\n"
    f"Candidate parent HEAD: {HEAD}\\n\\n"
    "## Candidate result\\n\\n"
    "~~~text\\n"
    f"dimension PASS = {len(pass_dims)}: {', '.join(pass_dims)}\\n"
    f"dimension BLOCKED = {len(blocked_dims)}\\n"
    f"dimension FAIL = {len(failed_dims)}\\n"
    "all seven operational claims = BLOCKED\\n"
    "overall operational semantic status = BLOCKED\\n"
    "~~~\\n\\n"
    "The only PASS dimensions are the two conditional mathematical signedness dimensions. "
    "They create non-waivable future high-bit-zero obligations and do not assert that target data satisfy them.\\n\\n"
    "All physical/semantic meaning dimensions remain BLOCKED because the existing evidence does not establish complete target-epoch semantic-rule applicability, and B-ERD-02 is bounded compatibility evidence rather than a prospectively precommitted per-dimension semantic discriminator.\\n\\n"
    "No dimension is FAIL: no exact current-authority target-scope evidence positively establishes the registered proposition false.\\n\\n"
    "C08 authority effect remains NONE. No provider contact, BI5 GET, new semantic execution, FULL_INTERVAL, D or backtest occurred.\\n",
    encoding="utf-8",
)

print(json.dumps({
    "candidate_parent_head":HEAD,
    "adjudication_seal":adjudication["adjudication_seal"],
    "overall":adjudication["overall_operational_semantic_status"],
    "pass_dimensions":pass_dims,
    "blocked_dimension_count":len(blocked_dims),
    "failed_dimensions":failed_dims,
    "claim_statuses":{c["claim_id"]:c["status"] for c in claim_adjudications},
},indent=2,sort_keys=True))
