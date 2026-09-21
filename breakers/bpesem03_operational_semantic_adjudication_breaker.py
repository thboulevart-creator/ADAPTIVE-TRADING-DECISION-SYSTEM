#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem03"
REPORT=Path(os.environ.get("BPESEM03_BREAK_REPORT", str(ROOT/"reports"/"data-qualification"/"bpesem03_operational_semantic_adjudication_adversarial_break_2026-09-21.md")))

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")

def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()

def seal(o:dict[str,Any],field:str)->str:
    x=dict(o); x.pop(field,None); return digest(x)

def read(name:str)->dict[str,Any]:
    return json.loads((E/name).read_text(encoding="utf-8"))

def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()

head=git("rev-parse","HEAD")
adj=read("operational_semantic_rule_adjudication_v0_1.json")
claim=read("claim_dimension_register_v0_1.json")
basis=read("dimension_authority_basis_register_v0_1.json")
scope=read("operational_semantic_scope_signature_v0_1.json")
obl=read("execution_obligation_set_v0_1.json")
baseline=read("governed_semantic_evidence_baseline_v0_1.json")
persist=read("baseline_persistence_record_v0_1.json")
ev=read("operational_evidence_records_and_admissibility_v0_1.json")
hist=read("historical_observation_eligibility_v0_1.json")
scopes=read("semantic_rule_scope_applicability_v0_1.json")
reviews=read("semantic_evidence_review_universes_v0_1.json")
vis=read("visibility_universes_v0_1.json")
pos=read("positive_authority_universes_v0_1.json")
alts=read("known_material_alternative_registries_v0_1.json")
hyps=read("semantic_hypothesis_sets_v0_1.json")
anchors=read("semantic_anchor_manifests_v0_1.json")
lineage=read("semantic_lineage_resolution_v0_1.json")
horizon=read("semantic_evidence_horizon_v0_1.json")
bpe02=json.loads((ROOT/"evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json").read_text(encoding="utf-8"))

defects=[]
attacks=[]

def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond:
        defects.append(name)

dims=[d["dimension_id"] for c in claim["claims"] for d in c["mandatory_dimensions"]]
check("A01_REGISTER_CARDINALITY",len(dims)==26 and len(set(dims))==26,"exact 26 unique operational dimensions")
basis_dims=[x["dimension_id"] for x in basis["dimension_bases"]]
check("A02_BASIS_BIJECTION",sorted(basis_dims)==sorted(dims) and len(basis_dims)==len(set(basis_dims)),"one exact authority basis per dimension")
adj_dims={d["dimension_id"]:d for d in adj["dimension_adjudications"]}
check("A03_ADJUDICATION_BIJECTION",set(adj_dims)==set(dims) and len(adj["dimension_adjudications"])==26,"no missing/extra dimension adjudication")

pass_dims=sorted(d for d,x in adj_dims.items() if x["status"]=="PASS")
expected_pass=["C03-D3-OP","C05-D2-OP"]
check("A04_NO_SEMANTIC_OVERPROMOTION",pass_dims==expected_pass,"only conditional mathematical signedness dimensions may PASS from current evidence")

scope_by={x["dimension_id"]:x for x in scopes["decisions"]}
scope_ok=True
for d in dims:
    if d in expected_pass:
        scope_ok &= scope_by[d]["status"]=="PASS"
    else:
        scope_ok &= scope_by[d]["status"]=="BLOCKED"
    scope_ok &= scope_by[d]["c08_authority_effect"]=="NONE"
    scope_ok &= scope_by[d]["representation_presence_authority"]=="NOT_ADJUDICATED_IN_B_PE_SEM_03"
check("A05_SCOPE_FIREWALL",scope_ok,"semantic-rule scope is separate from C08 representation presence")

# Exact signedness obligations and canonical union.
dim_obls=[]
for d in adj["dimension_adjudications"]:
    dim_obls.extend(d["execution_obligations"])
def sortcanon(xs):
    return sorted(xs,key=lambda x:canon(x))
check("A06_OBLIGATION_UNION",canon(sortcanon(dim_obls))==canon(sortcanon(adj["execution_obligation_set"]))==canon(sortcanon(obl["obligations"])),"global obligation set equals exact dimension union")
check("A07_OBLIGATION_DIGEST",adj["obligation_set_digest"]==obl["obligation_set_digest"]==digest(sortcanon(obl["obligations"])),"obligation digest exact")
check("A08_SIGNEDNESS_NONWAIVABLE",all(x["nonwaivable"] and x["on_fail"].startswith("BLOCKED") for x in obl["obligations"]) and {x["source_dimension_id"] for x in obl["obligations"]}==set(expected_pass),"signedness high-bit-zero obligations non-waivable")

# Evidence admissibility firewall.
dec={x["evidence_id"]:x for x in ev["admissibility_decisions"]}
check("A09_PROVIDER_LIVE_NOT_PROMOTED",dec["BPE02-E01"]["decision_status"]=="BLOCKED" and dec["BPE02-E02"]["decision_status"]=="BLOCKED","unversioned live provider pages retain zero positive authority")
check("A10_PROJECT_EVIDENCE_REJECTED",dec["BPE02-E11"]["decision_status"]=="REJECTED","project evidence cannot self-authorize")

# Positive universes must never contain inadmissible or scope-blocked sources.
positive_ok=True
for u in pos["universes"]:
    d=u["target_dimension_id"]
    for it in u["positive_authority_items"]:
        positive_ok &= dec[it["evidence_id"]]["decision_status"]=="ADMISSIBLE"
        positive_ok &= scope_by[d]["status"]=="PASS"
check("A11_POSITIVE_AUTHORITY_FILTER",positive_ok,"positive authority requires ADMISSIBLE source and PASS scope")

# Review -> visibility -> positive bindings are exact.
review_by={x["target_dimension_id"]:x for x in reviews["universes"]}
vis_by={x["target_dimension_id"]:x for x in vis["universes"]}
pos_by={x["target_dimension_id"]:x for x in pos["universes"]}
bind_ok=True
for d in dims:
    r=review_by[d]; v=vis_by[d]; p=pos_by[d]
    bind_ok &= v["semantic_evidence_review_universe_id"]==r["review_universe_id"]
    bind_ok &= v["semantic_evidence_review_universe_digest"]==r["review_universe_digest"]
    bind_ok &= p["visibility_universe_id"]==v["visibility_universe_id"]
    bind_ok &= p["visibility_universe_digest"]==v["visibility_universe_digest"]
check("A12_REVIEW_VISIBILITY_POSITIVE_CHAIN",bind_ok,"projection chain binds exact upstream digests")

# All original BPE02 assertions for C01-C07 remain visible in corresponding dimension.
expected={}
for a in bpe02["claim_evidence_assertions"]:
    if a["dimension_id"].startswith(("C01-","C02-","C03-","C04-","C05-","C06-","C07-")):
        expected.setdefault(a["dimension_id"]+"-OP",set()).add(a["assertion_id"])
visible_ok=True
for d,ids in expected.items():
    got={x["evidence_or_assertion_ref"] for x in vis_by[d]["visible_items"]}
    visible_ok &= ids.issubset(got)
check("A13_NO_INHERITED_ASSERTION_OMISSION",visible_ok,"all BPE02 C01-C07 assertions remain visible")

# BPE03 continuity limitation must be visible for every non-mathematical dimension.
continuity_ok=True
for d in dims:
    if d in expected_pass:
        continue
    continuity_ok &= any(x["evidence_or_assertion_ref"]=="BPE03-C08-D5-BLOCKED-CONTINUITY-LIMITATION" for x in vis_by[d]["visible_items"])
check("A14_BPE03_CONTINUITY_LIMIT_VISIBLE",continuity_ok,"target-epoch continuity limitation cannot be erased")

# B-ERD02 cannot be decisive for newly minted exact semantic hypotheses.
hist_ok=all(
    x["historical_execution_id"]=="BERD02-GHA-35533153289-1"
    and x["eligibility_role"]=="NONDECISIVE_COMPATIBILITY"
    and x["decisive_discrimination_eligible"] is False
    and x["status"]=="PASS"
    for x in hist["records"]
)
check("A15_BERD02_POSTHOC_FIREWALL",hist_ok,"bounded provider bytes are compatibility evidence only")

# Physical dimensions may not PASS without decisive historical eligibility.
physical={x["dimension_id"] for x in basis["dimension_bases"] if x["primary_authority_class"]=="PHYSICAL_HYPOTHESIS"}
check("A16_PHYSICAL_FAIL_CLOSED",all(adj_dims[d]["status"]=="BLOCKED" for d in physical),"physical hypotheses remain blocked")

# Semantic anchors are not current while scope is blocked.
anchor_ok=all(a["admissibility_status"]=="BLOCKED" and scope_by[a["target_dimension_id"]]["status"]=="BLOCKED" for a in anchors["anchors"])
check("A17_REFERENCE_IMPL_NOT_SOLE_SEMANTIC_AUTHORITY",anchor_ok,"reference implementation anchors remain non-current")

# Claims must be pure projection from registered mandatory dimensions.
claim_by={c["claim_id"]:c for c in adj["claim_adjudications"]}
projection_ok=True
for c in claim["claims"]:
    vals=[adj_dims[d["dimension_id"]]["status"] for d in c["mandatory_dimensions"]]
    expected_status="FAIL" if "FAIL" in vals else ("PASS" if all(x=="PASS" for x in vals) else "BLOCKED")
    projection_ok &= claim_by[c["claim_id"]]["status"]==expected_status
check("A18_CLAIM_PROJECTION",projection_ok,"claim status derived from immutable register")

check("A19_OVERALL_BLOCKED",adj["overall_operational_semantic_status"]=="BLOCKED" and adj["adjudication_status"]=="BLOCKED" and all(c["status"]=="BLOCKED" for c in adj["claim_adjudications"]),"all seven claims and overall authority remain BLOCKED")
check("A20_NO_FALSE_FAIL",not any(d["status"]=="FAIL" for d in adj["dimension_adjudications"]),"no exact target-scope authoritative contradiction warrants FAIL")

# Baseline and horizon integrity.
check("A21_BASELINE_PERSISTENCE",baseline["parent_relation_status"]=="PASS" and persist["parent_relation_status"]=="PASS" and baseline["baseline_digest"]==persist["baseline_digest"],"fresh baseline persistence relation exact")
check("A22_HORIZON_SEAL",horizon["horizon_digest"]==seal(horizon,"horizon_digest"),"candidate-parent evidence horizon seal exact")
check("A23_ADJUDICATION_SEAL",adj["adjudication_seal"]==seal(adj,"adjudication_seal"),"adjudication seal exact")

# Set digests recompute.
evdigest=digest(sorted([
    {"evidence_id":e["evidence_id"],"evidence_exact_content_sha256":e["exact_content_sha256"],"admissibility_decision_id":dec[e["evidence_id"]]["decision_id"],"admissibility_decision_seal":dec[e["evidence_id"]]["decision_seal"]}
    for e in ev["evidence_records"]
],key=lambda x:canon(x)))
check("A24_EVIDENCE_SET_DIGEST",adj["evidence_set_digest"]==evdigest,"evidence/admissibility binding exact")

# No C08 claim is present or modified.
check("A25_NO_C08_ADJUDICATION",all(not x["claim_id"].startswith("BPE-C08") for x in adj["claim_adjudications"]) and scope["c08_authority_effect"]=="NONE","B-PE-SEM-03 cannot promote C08")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=[
    "# B-PE-SEM-03 — OPERATIONAL SEMANTIC ADJUDICATION — ADVERSARIAL BREAK",
    "",
    f"Persisted candidate HEAD attacked: {head}",
    "",
    f"Candidate adversarial verdict: {verdict}",
    "",
    "## Attack matrix",
    "",
]
for name,status,detail in attacks:
    lines += [f"### {name}", "", f"{status} — {detail}", ""]
lines += [
    "## Result","",
    "~~~text",
    f"demonstrated candidate defects = {len(defects)}",
    *(defects or ["NONE"]),
    "~~~","",
    "No provider contact, BI5 GET, new semantic execution, FULL_INTERVAL, D materialization or backtest occurred.","",
    "STOP PART 2 BREAK.",
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"candidate_head":head,"verdict":verdict,"defects":defects,"attack_count":len(attacks)},indent=2))
