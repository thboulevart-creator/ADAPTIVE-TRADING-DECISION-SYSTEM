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
CONTRACT_PATH=ROOT/"evidence"/"bpesem04"/"prospective_semantic_authority_closure_contract_v0_1.json"
REPORT=Path(os.environ.get("BPESEM04_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem04_prospective_semantic_authority_contract_adversarial_break_2026-09-22.md")))

ROUTE_PATH="reports/data-qualification/post_bpesem03r_semantic_authority_closure_route_selection_2026-09-22.md"
ROUTE_BLOB="ba8687735cd48f81bb654d33117d957447707783"
PRIOR_ADJ_PATH="evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json"
PRIOR_ADJ_BLOB="d26655e3806b36305252fda186ccf4d08e38084b"
PRIOR_CLOSEOUT_PATH="reports/data-qualification/bpesem03r_final_closeout_2026-09-22.md"
PRIOR_CLOSEOUT_BLOB="acd90221fc97d816bec8d30e5c421aa89947e994"
INTERVAL_PATH="evidence/bfiq02/interval_inventory_v0_1.json"
INTERVAL_BLOB="8c02972228941d8b6f1aacaf9ac6bf75fb0f2029"
INTERVAL_ROOT="26d86a34a00e6697208a6481867f6338f21c1deae26e5be74b52cc8ba83eced8"

PHYSICAL=[
"C01-D1-OP","C01-D2-OP","C01-D3-OP",
"C02-D1-OP","C02-D2-OP","C02-D3-OP","C02-D4-OP",
"C03-D1-OP","C03-D2-OP","C03-D4-OP","C07-D2-OP"]
SEMANTIC=[
"C01-D4-OP",
"C04-D1-OP","C04-D2-OP","C04-D3-OP","C04-D4-OP",
"C05-D1-OP",
"C06-D1-OP","C06-D2-OP","C06-D4-OP",
"C07-D1-OP","C07-D3-OP"]
PREREQ=["C05-D3-OP","C06-D3-OP"]
PASS=["C03-D3-OP","C05-D2-OP"]
BLOCKED=PHYSICAL+SEMANTIC+PREREQ

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

head=git("rev-parse","HEAD")
contract=readj(CONTRACT_PATH)
prior=readj(PRIOR_ADJ_PATH)

attacks=[]
defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond:
        defects.append(name)

check("A01_INPUT_HISTORY_IMMUTABLE",
      blob(ROUTE_PATH)==ROUTE_BLOB and blob(PRIOR_ADJ_PATH)==PRIOR_ADJ_BLOB and blob(PRIOR_CLOSEOUT_PATH)==PRIOR_CLOSEOUT_BLOB,
      "route selection and B-PE-SEM-03R historical artifacts remain byte-identical")

check("A02_CONTRACT_SEAL",
      contract.get("contract_seal")==seal(contract,"contract_seal"),
      "canonical contract seal recomputes exactly")

pop=contract["dimension_population"]
check("A03_DIMENSION_POPULATION_EXACT",
      sorted(pop["already_pass"])==sorted(PASS)
      and sorted(pop["blocked_physical_hypothesis"])==sorted(PHYSICAL)
      and sorted(pop["blocked_semantic_anchor"])==sorted(SEMANTIC)
      and sorted(pop["blocked_prerequisite_closure"])==sorted(PREREQ),
      "exact 2 PASS + 24 BLOCKED population is frozen")

pres=contract["preserved_existing_authority"]
check("A04_EXISTING_SIGNEDNESS_AUTHORITY_PRESERVED",
      sorted(pres["dimension_ids"])==sorted(PASS)
      and pres["conditional_rule_ids"]==["SIGNEDNESS_EQUIVALENCE_RULE_V0_1"]
      and pres["obligation_set_digest"]==prior["obligation_set_digest"]
      and pres["execution_obligation_set"]==prior["execution_obligation_set"],
      "existing conditional signedness PASS and nonwaivable obligations are preserved exactly")

lane_s=contract["lane_s"]
slots=lane_s["evidence_slots"]
slot_ids=[x["evidence_slot_id"] for x in slots]
check("A05_SEMANTIC_SLOT_IDENTITIES_PREALLOCATED",
      len(slots)==6 and len(set(slot_ids))==6 and all(x["status_before_observation"]=="UNFILLED_PRE_REGISTERED_SLOT" for x in slots),
      "semantic evidence namespaces are frozen before observation")

provider_primary=[x for x in slots if x["authority_role"] in {"PRIMARY_SEMANTIC_AUTHORITY","PRIMARY_SCALE_AND_INSTRUMENT_AUTHORITY","TARGET_EPOCH_SCOPE_AUTHORITY"}]
check("A06_PROVIDER_PRIMARY_AUTHORITY_REQUIRED",
      len(provider_primary)==3
      and all("PROVIDER" in x["required_source_class"] for x in provider_primary),
      "provider-authored immutable/versioned authority is required for meaning/scale/epoch")

check("A07_REFERENCE_IMPLEMENTATION_NOT_SOLE_AUTHORITY",
      all(x.get("sole_positive_authority_allowed") is False for x in slots if x["authority_role"]=="CORROBORATION_ONLY")
      and all(x.get("sole_reference_implementation_allowed") is False for x in slots if x["authority_role"]=="PRIMARY_SEMANTIC_AUTHORITY"),
      "non-project reference implementations are corroboration only")

epoch=lane_s["epoch_coverage_policy"]
scope=contract["scope_signature"]
check("A08_TARGET_EPOCH_EXACT_AND_FAIL_CLOSED",
      epoch["target_interval_start"]==scope["target_start"]
      and epoch["target_interval_end"]==scope["target_end"]
      and epoch["partial_coverage_disposition"]=="BLOCKED"
      and epoch["forward_or_backward_extrapolation_without_explicit_continuity_proof"]=="FORBIDDEN"
      and epoch["representation_presence_is_semantic_continuity"]=="FALSE",
      "full target epoch is required with no silent extrapolation or representation/semantic conflation")

lineage=lane_s["source_lineage_rules"]
check("A09_LINEAGE_INDEPENDENCE_FAIL_CLOSED",
      lineage["project_origin_never_independent_semantic_authority"] is True
      and lineage["fork_copy_or_shared_upstream_counts_as_same_lineage"] is True
      and lineage["duplicate_lineage_cannot_satisfy_multi_source_requirement"] is True
      and lineage["unresolved_lineage_disposition"]=="BLOCKED",
      "project/fork/copy lineages cannot manufacture independence")

scale=lane_s["scale_noncircularity"]
check("A10_SCALE_NONCIRCULARITY",
      scale["dimension_id"]=="C06-D3-OP"
      and "expected market price" in scale["prohibited_authority_inputs"]
      and "agreement with /1000 reference implementation" in scale["prohibited_authority_inputs"]
      and "provider-authored" in scale["required_primary_source"],
      "/1000 authority cannot be inferred from plausibility or project/reference agreement")

lane_p=contract["lane_p"]
hyp=lane_p["hypothesis_sets"]
check("A11_PHYSICAL_HYPOTHESIS_SET_BIJECTION",
      sorted(hyp.keys())==sorted(PHYSICAL) and len(hyp)==11,
      "exactly 11 physical dimensions have prospectively frozen hypothesis sets")

hyp_ok=True
for d in PHYSICAL:
    x=hyp[d]
    hyp_ok &= isinstance(x.get("registered_proposition"),str) and len(x["registered_proposition"])>0
    hyp_ok &= len(x.get("alternatives",[]))>=3
    hyp_ok &= len(set(x.get("alternatives",[])))==len(x.get("alternatives",[]))
    hyp_ok &= len(x.get("discriminators",[]))>=1
check("A12_MATERIAL_ALTERNATIVES_AND_DISCRIMINATORS",
      hyp_ok,
      "each physical dimension has explicit material alternatives and predeclared discriminators")

alt=lane_p["known_material_alternative_policy"]
check("A13_UNKNOWN_ALTERNATIVE_REOPENS",
      alt["enumerated_sets_are_preobservation_closed"] is True
      and "BLOCKED" in alt["other_category_is_not_a_winner"]
      and alt["silent_alternative_collapse_forbidden"] is True,
      "OTHER/UNKNOWN cannot silently become a winning interpretation")

disc=lane_p["discriminators"]
disc_ids=[x["discriminator_id"] for x in disc]
referenced=set(z for x in hyp.values() for z in x["discriminators"])
check("A14_DISCRIMINATOR_CLOSURE",
      len(disc)==16 and len(set(disc_ids))==16 and referenced.issubset(set(disc_ids))
      and "P-D15-SIGNEDNESS-OBLIGATION-CHECK" in disc_ids
      and "P-D16-SEMANTIC-CROSSCHECK-REQUIRED" in disc_ids,
      "all hypothesis discriminators resolve to predeclared definitions and signedness/semantic firewalls exist")

disc_text=json.dumps(disc,sort_keys=True)
check("A15_NO_PLAUSIBILITY_LAUNDERING",
      "spread sign or market plausibility alone cannot select a winner" in disc_text
      and "realistic-looking values are not authority" in disc_text
      and "raw plausibility cannot replace semantic authority" in disc_text,
      "ask/bid, volume and mixed physical-semantic decisions cannot use plausibility as authority")

sampling=lane_p["sampling_policy"]
check("A16_SAMPLING_BINDS_SEALED_INVENTORY",
      sampling["source_interval_inventory_path"]==INTERVAL_PATH
      and sampling["source_interval_inventory_git_blob"]==INTERVAL_BLOB
      and sampling["source_interval_inventory_root"]==INTERVAL_ROOT
      and blob(INTERVAL_PATH)==INTERVAL_BLOB,
      "sampling derives only from exact sealed interval inventory")

seq=" ".join(sampling["selection_sequence"])
check("A17_PRE_GET_SAMPLE_FREEZE",
      "SemanticEpochManifest before any Lane P provider-object GET" in seq
      and "RequestManifest containing every selected H1 before the first provider-object GET" in seq
      and sampling["selection_mutability_after_first_provider_object_get"]=="FORBIDDEN"
      and "NO_SILENT_SUBSTITUTION" in sampling["unexpected_closed_or_missing_selected_slot_disposition"],
      "semantic epochs and exact request sample are frozen before first BI5 observation")

check("A18_DETERMINISTIC_TEMPORAL_SAMPLING",
      "floor((n-1)*0.10)" in seq and "floor((n-1)*0.50)" in seq and "floor((n-1)*0.90)" in seq
      and "nearest open slot strictly before" in seq
      and "nearest open slot at-or-after" in seq,
      "quarter stratification and change-boundary sampling are deterministic")

diag=lane_p["diagnostic_independence"]
check("A19_DIAGNOSTIC_INDEPENDENCE",
      diag["required_diagnostics"]==["P-DIAG-A","P-DIAG-B"]
      and "BLOCKED"==diag["fake_independence_disposition"]
      and any("no function/code copy" in x for x in diag["requirements"])
      and any("outputs compared only after each diagnostic result is sealed" in x for x in diag["requirements"]),
      "two genuinely independent diagnostic paths are mandatory")

check("A20_BERD02_NONDECISIVE_PRESERVED",
      lane_p["known_prior_observation_role"]=="B-ERD-02 remains NONDECISIVE_COMPATIBILITY only"
      and lane_p["pre_observation_freeze_required"] is True,
      "historical B-ERD-02 cannot be promoted post hoc")

lane_c=contract["lane_c"]
rules={x["dimension_id"]:x for x in lane_c["rules"]}
check("A21_C05_D3_DERIVED_ONLY",
      lane_c["derived_closure_only"] is True
      and rules["C05-D3-OP"]["exact_prerequisites"]==["C05-D1-OP","C05-D2-OP","C06-D1-OP","C06-D2-OP","C06-D3-OP","C06-D4-OP"]
      and rules["C05-D3-OP"]["independent_evidence_acquisition_allowed"] is False,
      "C05-D3 can only derive from its exact prerequisites")

check("A22_C06_D3_NONCIRCULAR_DERIVED_RULE",
      rules["C06-D3-OP"]["independent_provider_object_acquisition_allowed"] is False
      and "market price" in rules["C06-D3-OP"]["noncircularity_rule"]
      and "provider-authored scale semantics" in rules["C06-D3-OP"]["pass_rule"],
      "C06-D3 cannot be manufactured from object plausibility")

eid=contract["evidence_identity_policy"]
check("A23_EVIDENCE_IDS_FROZEN_BEFORE_OBSERVATION",
      eid["semantic_slot_ids"]==slot_ids
      and eid["lane_p_request_manifest_id"]=="BPESEM04-P-REQUEST-MANIFEST-V0_1"
      and "{UTC_H1_ISO}" in eid["lane_p_object_evidence_id_template"]
      and "no ad-hoc IDs after observation" in eid["allocation_rule"],
      "semantic slots and deterministic physical evidence namespace are preallocated")

sealpol=contract["sealing_policy"]
check("A24_SEALING_PRE_POST_OBSERVATION",
      sealpol["hash"]=="SHA-256"
      and "contract_seal" in sealpol["lane_p_pre_observation_seals"]
      and "request_manifest_seal" in sealpol["lane_p_pre_observation_seals"]
      and "raw_response_sha256" in sealpol["lane_p_post_observation_seals"]
      and sealpol["mutation_after_seal"]=="FORBIDDEN; NEW_VERSION_REQUIRED",
      "pre/post observation identities cannot mutate silently")

reopens=contract["reopen_rules"]
reopen_text=json.dumps(reopens,sort_keys=True)
check("A25_REOPEN_COVERAGE",
      all(k in reopen_text for k in ["new material semantic interpretation","new provider semantic change point","source bytes/version/provenance mutation","diagnostic code changes after pre-observation seal","sample manifest changes after first GET","unexpected response wrapper/residual/layout"]),
      "material evidence/code/sample changes force governed reopen")

out=contract["outcome_rules"]
check("A26_PASS_FAIL_BLOCKED_FAIL_CLOSED",
      "All authority roles" in out["dimension_pass"]
      and "positively establishes the registered proposition false" in out["dimension_fail"]
      and "Evidence absent" in out["dimension_blocked"]
      and "PASS only if all mandatory dimensions PASS" in out["claim_projection"]
      and "Contract PASS does not imply any C01-C07 evidence PASS" in out["contract_qualification_pass"],
      "contract and evidence verdict semantics are separated and fail closed")

sg=contract["mandatory_safeguards"]
expected=[f"S{i:02d}_" for i in range(1,21)]
check("A27_ALL_20_SAFEGUARDS_PRESENT",
      len(sg)==20 and all(any(x.startswith(p) for x in sg) for p in expected),
      "route-selected S01-S20 safeguard set is complete")

boundary=contract["execution_boundary"]
check("A28_NO_EXECUTION_AUTHORIZATION",
      all(v is False for k,v in boundary.items() if k.startswith("this_contract_authorizes_"))
      and "no network execution is self-authorized" in boundary["post_contract_consumer_if_qualified"],
      "contract qualification cannot self-authorize provider/network/FULL_INTERVAL/D/backtest/live")

target_ids=[]
target_ids += contract["dimension_population"]["already_pass"]
target_ids += contract["dimension_population"]["blocked_physical_hypothesis"]
target_ids += contract["dimension_population"]["blocked_semantic_anchor"]
target_ids += contract["dimension_population"]["blocked_prerequisite_closure"]
for s in contract["lane_s"]["evidence_slots"]:
    target_ids += s.get("target_dimension_ids",[])
for r in contract["lane_s"]["semantic_authority_rules"]:
    target_ids.append(r["dimension_id"])
target_ids += contract["lane_p"]["target_dimension_ids"]
target_ids += list(contract["lane_p"]["hypothesis_sets"].keys())
target_ids += [r["dimension_id"] for r in contract["lane_c"]["rules"]]
check("A29_C08_FIREWALL",
      all("C08" not in x for x in target_ids)
      and any("C08" in x for x in contract["mandatory_safeguards"]),
      "C08 may appear only as an explicit anti-circularity safeguard, never as an authority target")

check("A30_DIGESTS_RECOMPUTE",
      contract["semantic_slot_set_digest"]==digest(sorted(slots,key=lambda x:x["evidence_slot_id"]))
      and contract["physical_hypothesis_set_digest"]==digest({k:hyp[k] for k in sorted(hyp)})
      and contract["discriminator_set_digest"]==digest(sorted(disc,key=lambda x:x["discriminator_id"]))
      and contract["sampling_policy_digest"]==digest(sampling)
      and contract["lane_c_digest"]==digest(lane_c)
      and contract["safeguard_set_digest"]==digest(sorted(sg)),
      "all component digests recompute exactly")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=[
"# B-PE-SEM-04 — PROSPECTIVE CLOSURE CONTRACT — ADVERSARIAL BREAK",
"",
"Persisted candidate HEAD attacked: "+head,
"",
"Candidate adversarial verdict: "+verdict,
"",
]
for n,s,d in attacks:
    lines += ["## "+n,"",s+" — "+d,""]
lines += [
"## Result","",
"~~~text",
"attack count = "+str(len(attacks)),
"demonstrated defects = "+str(len(defects)),
*(defects or ["NONE"]),
"~~~","",
"No provider contact, BI5 GET, new provider-object acquisition, semantic-discrimination execution, FULL_INTERVAL, D materialization or backtest occurred.","",
"STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":head,"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))
