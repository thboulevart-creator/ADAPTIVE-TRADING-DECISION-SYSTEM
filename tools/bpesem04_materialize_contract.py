#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem04"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem04_prospective_semantic_authority_closure_contract_candidate_2026-09-22.md"

ROUTE_PATH="reports/data-qualification/post_bpesem03r_semantic_authority_closure_route_selection_2026-09-22.md"
ROUTE_BLOB="ba8687735cd48f81bb654d33117d957447707783"
PRIOR_ADJ_PATH="evidence/bpesem03r/operational_semantic_rule_adjudication_v0_1.json"
PRIOR_ADJ_BLOB="d26655e3806b36305252fda186ccf4d08e38084b"
PRIOR_CLOSEOUT_PATH="reports/data-qualification/bpesem03r_final_closeout_2026-09-22.md"
PRIOR_CLOSEOUT_BLOB="acd90221fc97d816bec8d30e5c421aa89947e994"
SCOPE_PATH="evidence/bpesem03/operational_semantic_scope_signature_v0_1.json"
SCOPE_BLOB="eacbda1fffc0c452e5efae6e0d97dd47fb28791c"
BASIS_PATH="evidence/bpesem03/dimension_authority_basis_register_v0_1.json"
BASIS_BLOB="b67abaf9468689855b7f362264a1fd801f9f12a8"
INTERVAL_INVENTORY_PATH="evidence/bfiq02/interval_inventory_v0_1.json"
INTERVAL_INVENTORY_BLOB="8c02972228941d8b6f1aacaf9ac6bf75fb0f2029"
INTERVAL_INVENTORY_ROOT="26d86a34a00e6697208a6481867f6338f21c1deae26e5be74b52cc8ba83eced8"

CONTRACT_ID="B_PE_SEM_04_PROSPECTIVE_C01_C07_SEMANTIC_AUTHORITY_CLOSURE_EVIDENCE_CONTRACT"
CONTRACT_VERSION="B_PE_SEM_04_V0_1_CANDIDATE"

PHYSICAL_DIMS=[
    "C01-D1-OP","C01-D2-OP","C01-D3-OP",
    "C02-D1-OP","C02-D2-OP","C02-D3-OP","C02-D4-OP",
    "C03-D1-OP","C03-D2-OP","C03-D4-OP",
    "C07-D2-OP",
]
SEMANTIC_DIMS=[
    "C01-D4-OP",
    "C04-D1-OP","C04-D2-OP","C04-D3-OP","C04-D4-OP",
    "C05-D1-OP",
    "C06-D1-OP","C06-D2-OP","C06-D4-OP",
    "C07-D1-OP","C07-D3-OP",
]
PREREQ_DIMS=["C05-D3-OP","C06-D3-OP"]
PASS_DIMS=["C03-D3-OP","C05-D2-OP"]
BLOCKED_DIMS=PHYSICAL_DIMS+SEMANTIC_DIMS+PREREQ_DIMS

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

def readj(path:str)->dict[str,Any]:
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def writej(path:Path,obj:dict[str,Any]):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")

for p,b in [
    (ROUTE_PATH,ROUTE_BLOB),
    (PRIOR_ADJ_PATH,PRIOR_ADJ_BLOB),
    (PRIOR_CLOSEOUT_PATH,PRIOR_CLOSEOUT_BLOB),
    (SCOPE_PATH,SCOPE_BLOB),
    (BASIS_PATH,BASIS_BLOB),
    (INTERVAL_INVENTORY_PATH,INTERVAL_INVENTORY_BLOB),
]:
    if blob(p)!=b:
        raise RuntimeError("governed input blob mismatch: "+p)

prior=readj(PRIOR_ADJ_PATH)
scope=readj(SCOPE_PATH)
basis=readj(BASIS_PATH)
blocked=sorted(x["dimension_id"] for x in prior["dimension_adjudications"] if x["status"]=="BLOCKED")
passed=sorted(x["dimension_id"] for x in prior["dimension_adjudications"] if x["status"]=="PASS")
if blocked!=sorted(BLOCKED_DIMS) or passed!=sorted(PASS_DIMS):
    raise RuntimeError("prior adjudication dimension population changed")
if prior["overall_operational_semantic_status"]!="BLOCKED":
    raise RuntimeError("prior semantic authority no longer BLOCKED")

basis_by={x["dimension_id"]:x for x in basis["dimension_bases"]}
if sorted(d for d in BLOCKED_DIMS if basis_by[d]["primary_authority_class"]=="PHYSICAL_HYPOTHESIS")!=sorted(PHYSICAL_DIMS):
    raise RuntimeError("physical dimension class drift")
if sorted(d for d in BLOCKED_DIMS if basis_by[d]["primary_authority_class"]=="SEMANTIC_ANCHOR")!=sorted(SEMANTIC_DIMS):
    raise RuntimeError("semantic dimension class drift")
if sorted(d for d in BLOCKED_DIMS if basis_by[d]["primary_authority_class"]=="PREREQUISITE_CLOSURE")!=sorted(PREREQ_DIMS):
    raise RuntimeError("prerequisite dimension class drift")

semantic_slots=[
    {
        "evidence_slot_id":"BPESEM04-S-E01-PROVIDER-FORMAT-SEMANTICS",
        "lane":"S",
        "required_source_class":"PROVIDER_AUTHORED_IMMUTABLE_OR_VERSIONED",
        "purpose":"Exact native hourly BI5 semantic format meanings: decompressed payload role, timestamp offset semantics, ask/bid roles, volume roles/transform where provider-authoritative.",
        "target_dimension_ids":["C01-D4-OP","C04-D1-OP","C04-D2-OP","C04-D3-OP","C04-D4-OP","C05-D1-OP","C07-D1-OP","C07-D3-OP"],
        "authority_role":"PRIMARY_SEMANTIC_AUTHORITY",
        "minimum_materialization_requirements":["immutable_snapshot_or_exact_version","publisher_identity","exact_locator","raw_sha256","semantic_extract_sha256","retrieval_time","scope_statement"],
        "sole_reference_implementation_allowed":False,
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
    {
        "evidence_slot_id":"BPESEM04-S-E02-PROVIDER-INSTRUMENT-SCALE",
        "lane":"S",
        "required_source_class":"PROVIDER_AUTHORED_IMMUTABLE_OR_VERSIONED",
        "purpose":"USATECHIDXUSD identity, K1 applicability, decimal/price scale authority, and exact noncircular /1000 or alternative mapping.",
        "target_dimension_ids":["C06-D1-OP","C06-D2-OP","C06-D3-OP","C06-D4-OP"],
        "authority_role":"PRIMARY_SCALE_AND_INSTRUMENT_AUTHORITY",
        "minimum_materialization_requirements":["immutable_snapshot_or_exact_version","publisher_identity","exact_instrument_identity","exact_scale_statement","raw_sha256","retrieval_time","scope_statement"],
        "price_plausibility_inference_allowed":False,
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
    {
        "evidence_slot_id":"BPESEM04-S-E03-PROVIDER-EPOCH-CONTINUITY",
        "lane":"S",
        "required_source_class":"PROVIDER_AUTHORED_VERSIONED_CHANGE_HISTORY",
        "purpose":"Provider semantic change-point inventory and continuity/epoch coverage across the exact target interval.",
        "target_dimension_ids":BLOCKED_DIMS,
        "authority_role":"TARGET_EPOCH_SCOPE_AUTHORITY",
        "minimum_materialization_requirements":["version_or_date_boundaries","immutable_snapshot_or_exact_version","raw_sha256","complete_change_point_review","coverage_ledger"],
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
    {
        "evidence_slot_id":"BPESEM04-S-E04-INDEPENDENT-CORROBORATION-A",
        "lane":"S",
        "required_source_class":"VERSIONED_NONPROJECT_REFERENCE_IMPLEMENTATION_OR_SPEC",
        "purpose":"Independent corroboration for candidate semantic meanings; never sole provider authority.",
        "target_dimension_ids":SEMANTIC_DIMS,
        "authority_role":"CORROBORATION_ONLY",
        "lineage_independence_required":True,
        "sole_positive_authority_allowed":False,
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
    {
        "evidence_slot_id":"BPESEM04-S-E05-INDEPENDENT-CORROBORATION-B",
        "lane":"S",
        "required_source_class":"VERSIONED_NONPROJECT_REFERENCE_IMPLEMENTATION_OR_SPEC",
        "purpose":"Second independent corroboration lineage where available; cannot substitute for missing provider primary authority.",
        "target_dimension_ids":SEMANTIC_DIMS,
        "authority_role":"CORROBORATION_ONLY",
        "lineage_independence_required":True,
        "must_be_independent_from_slot":"BPESEM04-S-E04-INDEPENDENT-CORROBORATION-A",
        "sole_positive_authority_allowed":False,
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
    {
        "evidence_slot_id":"BPESEM04-S-E06-CONTRADICTION-SWEEP",
        "lane":"S",
        "required_source_class":"GOVERNED_MULTI_SOURCE_REVIEW",
        "purpose":"Explicit contradiction and alternative interpretation sweep before any semantic PASS.",
        "target_dimension_ids":SEMANTIC_DIMS+["C06-D3-OP"],
        "authority_role":"CONTRADICTION_CONTROL",
        "must_cover_all_registered_and_newly_discovered_material_sources":True,
        "status_before_observation":"UNFILLED_PRE_REGISTERED_SLOT",
    },
]

semantic_authority_rules=[]
for d in SEMANTIC_DIMS:
    semantic_authority_rules.append({
        "dimension_id":d,
        "pass_requires":[
            "EXACT_PROVIDER_PRIMARY_SEMANTIC_ANCHOR",
            "SEMANTIC_SOURCE_LINEAGE_RESOLVED",
            "TARGET_EPOCH_SCOPE_APPLICABILITY_PASS",
            "NO_UNRESOLVED_MATERIAL_CONTRADICTION",
        ],
        "corroboration_requirement":"AT_LEAST_ONE_INDEPENDENT_NONPROJECT_CORROBORATION_WHERE_MATERIAL_SOURCE_EXISTS; ABSENCE_DOES_NOT_REPLACE_PROVIDER_PRIMARY",
        "fail_condition":"ADMISSIBLE_EXACT_TARGET_SCOPE_PRIMARY_AUTHORITY_ESTABLISHES_REGISTERED_PROPOSITION_FALSE",
        "blocked_conditions":[
            "PROVIDER_PRIMARY_ABSENT",
            "SOURCE_NOT_IMMUTABLE_OR_VERSIONED",
            "LINEAGE_UNRESOLVED",
            "TARGET_EPOCH_GAP",
            "MATERIAL_CONTRADICTION_UNRESOLVED",
        ],
    })

physical_hypotheses={
    "C01-D1-OP":{
        "registered_proposition":"compression family = LZMA",
        "alternatives":["LZMA_FAMILY","NON_LZMA_COMPRESSED","UNCOMPRESSED_OR_OTHER"],
        "discriminators":["P-D01-CODEC-FAMILY-MATRIX","P-D02-DECOMPRESSED-BYTE-IDENTITY"],
    },
    "C01-D2-OP":{
        "registered_proposition":"exact envelope/container mode for target K1",
        "alternatives":["LZMA_ALONE","RAW_LZMA1","XZ_CONTAINER","OTHER_CONTAINER_OR_WRAPPER"],
        "discriminators":["P-D03-ENVELOPE-PARSER-MATRIX","P-D04-WHOLE-OBJECT-STREAM-CONSUMPTION"],
    },
    "C01-D3-OP":{
        "registered_proposition":"exact stream/wrapper admission rule",
        "alternatives":["SINGLE_WHOLE_OBJECT_STREAM","CONCATENATED_STREAMS","PREFIX_SUFFIX_WRAPPER","OTHER_ADMISSION_RULE"],
        "discriminators":["P-D04-WHOLE-OBJECT-STREAM-CONSUMPTION","P-D05-PREFIX-SUFFIX-AND-CONCATENATION-SWEEP"],
    },
    "C02-D1-OP":{
        "registered_proposition":"complete record width = 20 bytes",
        "alternatives":["FIXED_20_BYTES","OTHER_FIXED_WIDTH","VARIABLE_WIDTH"],
        "discriminators":["P-D06-DECOMPRESSED-LENGTH-MODULUS","P-D07-CANDIDATE-WIDTH-CONSISTENCY"],
    },
    "C02-D2-OP":{
        "registered_proposition":"frame origin = byte zero",
        "alternatives":["ORIGIN_BYTE_ZERO","NONZERO_FIXED_ORIGIN","VARIABLE_ORIGIN"],
        "discriminators":["P-D08-FRAME-OFFSET-SWEEP"],
    },
    "C02-D3-OP":{
        "registered_proposition":"terminal residual/trailing-byte disposition",
        "alternatives":["NO_TRAILING_RESIDUAL","FIXED_TRAILER","VARIABLE_RESIDUAL_OR_TRAILER"],
        "discriminators":["P-D09-TERMINAL-RESIDUAL-EXACTNESS"],
    },
    "C02-D4-OP":{
        "registered_proposition":"per-record header/delimiter presence and semantics",
        "alternatives":["NO_PER_RECORD_HEADER_OR_DELIMITER","FIXED_PER_RECORD_HEADER","DELIMITER_BASED_OR_VARIABLE_HEADER"],
        "discriminators":["P-D10-PER-RECORD-STRUCTURAL-SWEEP"],
    },
    "C03-D1-OP":{
        "registered_proposition":"byte order = big-endian",
        "alternatives":["BIG_ENDIAN","LITTLE_ENDIAN","MIXED_ENDIAN_OR_OTHER"],
        "discriminators":["P-D11-ENDIAN-DUAL-DECODE","P-D16-SEMANTIC-CROSSCHECK-REQUIRED"],
    },
    "C03-D2-OP":{
        "registered_proposition":"exact five-field physical order",
        "alternatives":["TARGET_ORDER_MS_ASK_BID_ASKVOL_BIDVOL","MATERIAL_PERMUTATION","MIXED_OR_OTHER_LAYOUT"],
        "discriminators":["P-D12-FIELD-ORDER-CANDIDATE-MATRIX","P-D16-SEMANTIC-CROSSCHECK-REQUIRED"],
    },
    "C03-D4-OP":{
        "registered_proposition":"final two fields = IEEE-754 binary32",
        "alternatives":["IEEE754_BINARY32","INTEGER32","BINARY64_OR_OTHER_ENCODING"],
        "discriminators":["P-D13-PRIMITIVE-BIT-INTERPRETATION-MATRIX","P-D16-SEMANTIC-CROSSCHECK-REQUIRED"],
    },
    "C07-D2-OP":{
        "registered_proposition":"primitive encoding = IEEE-754 binary32",
        "alternatives":["IEEE754_BINARY32","INTEGER32_OR_FIXED_POINT","BINARY64_OR_OTHER_ENCODING"],
        "discriminators":["P-D14-VOLUME-PRIMITIVE-MATRIX","P-D16-SEMANTIC-CROSSCHECK-REQUIRED"],
    },
}

discriminators=[
    {"discriminator_id":"P-D01-CODEC-FAMILY-MATRIX","type":"PHYSICAL","rule":"Attempt only predeclared codec families against raw response bytes; exact raw input hash fixed first. Record success/failure and decoded bytes hash for every codec."},
    {"discriminator_id":"P-D02-DECOMPRESSED-BYTE-IDENTITY","type":"PHYSICAL","rule":"Independent diagnostics must yield byte-identical decompressed output for any surviving codec hypothesis."},
    {"discriminator_id":"P-D03-ENVELOPE-PARSER-MATRIX","type":"PHYSICAL","rule":"Test exact LZMA-Alone/raw-LZMA1/XZ/other predeclared envelope parsers without auto-detection fallback."},
    {"discriminator_id":"P-D04-WHOLE-OBJECT-STREAM-CONSUMPTION","type":"PHYSICAL","rule":"Record exact consumed byte count, unused bytes, concatenated stream count and terminal state."},
    {"discriminator_id":"P-D05-PREFIX-SUFFIX-AND-CONCATENATION-SWEEP","type":"PHYSICAL","rule":"Detect non-stream prefix/suffix and concatenated stream requirements without stripping bytes silently."},
    {"discriminator_id":"P-D06-DECOMPRESSED-LENGTH-MODULUS","type":"PHYSICAL","rule":"Evaluate exact decompressed length against 20 and all registered fixed-width alternatives; no row dropping."},
    {"discriminator_id":"P-D07-CANDIDATE-WIDTH-CONSISTENCY","type":"PHYSICAL","rule":"For each registered width hypothesis, require consistent complete framing across every acquired object in applicable segment."},
    {"discriminator_id":"P-D08-FRAME-OFFSET-SWEEP","type":"PHYSICAL","rule":"Evaluate byte-zero and every registered nonzero origin candidate; no preferred origin chosen from semantic plausibility alone."},
    {"discriminator_id":"P-D09-TERMINAL-RESIDUAL-EXACTNESS","type":"PHYSICAL","rule":"Preserve and hash all residual bytes; any undeclared residual blocks PASS until adjudicated."},
    {"discriminator_id":"P-D10-PER-RECORD-STRUCTURAL-SWEEP","type":"PHYSICAL","rule":"Test registered header/delimiter layouts without deleting candidate bytes; unknown recurring structure is a reopen trigger."},
    {"discriminator_id":"P-D11-ENDIAN-DUAL-DECODE","type":"PHYSICAL_PLUS_SEMANTIC_CROSSCHECK","rule":"Execute big/little/mixed registered decodes independently; physical survival alone is insufficient without Lane S semantic crosscheck where meanings are required."},
    {"discriminator_id":"P-D12-FIELD-ORDER-CANDIDATE-MATRIX","type":"PHYSICAL_PLUS_SEMANTIC_CROSSCHECK","rule":"Evaluate target order and all registered material order classes; spread sign or market plausibility alone cannot select a winner."},
    {"discriminator_id":"P-D13-PRIMITIVE-BIT-INTERPRETATION-MATRIX","type":"PHYSICAL_PLUS_SEMANTIC_CROSSCHECK","rule":"Compare exact 4-byte bit interpretations under registered primitive encodings; decodability alone cannot establish semantic meaning."},
    {"discriminator_id":"P-D14-VOLUME-PRIMITIVE-MATRIX","type":"PHYSICAL_PLUS_SEMANTIC_CROSSCHECK","rule":"Evaluate volume primitive hypotheses on unchanged bits; realistic-looking values are not authority."},
    {"discriminator_id":"P-D15-SIGNEDNESS-OBLIGATION-CHECK","type":"EXECUTION_OBLIGATION","rule":"For affected first-three fields, evaluate high_bit == 0 on every accepted target-domain instance unless separate exact signedness authority is current PASS."},
    {"discriminator_id":"P-D16-SEMANTIC-CROSSCHECK-REQUIRED","type":"FIREWALL","rule":"Any physical discriminator needing field meaning must consume Lane S qualified semantic anchors; raw plausibility cannot replace semantic authority."},
]

sampling_policy={
    "policy_id":"BPESEM04-P-SAMPLING-V0_1",
    "source_interval_inventory_path":INTERVAL_INVENTORY_PATH,
    "source_interval_inventory_git_blob":INTERVAL_INVENTORY_BLOB,
    "source_interval_inventory_root":INTERVAL_INVENTORY_ROOT,
    "source_scope_signature_id":scope["scope_signature_id"],
    "target_full_domain_first_h1":scope["full_domain_first_h1"],
    "target_full_domain_last_h1":scope["full_domain_last_h1"],
    "evaluation_first_open_slot_utc":scope["evaluation_first_open_slot_utc"],
    "evaluation_last_open_slot_utc":scope["evaluation_last_open_slot_utc"],
    "selection_sequence":[
        "Lane S evidence acquisition and immutable sealing occurs first.",
        "Lane S semantic change-point inventory is sealed as SemanticEpochManifest before any Lane P provider-object GET.",
        "Use canonical open-slot sequence from sealed interval inventory only.",
        "Partition evaluation open slots by UTC calendar quarter.",
        "For every non-empty quarter select deterministic ranks floor((n-1)*0.10), floor((n-1)*0.50), floor((n-1)*0.90).",
        "Add first and last open slot of full governed domain.",
        "For every sealed semantic change point inside target domain add nearest open slot strictly before and nearest open slot at-or-after the change point.",
        "Deduplicate exact H1 timestamps and sort ascending.",
        "Materialize and seal RequestManifest containing every selected H1 before the first provider-object GET.",
    ],
    "selection_mutability_after_first_provider_object_get":"FORBIDDEN",
    "unexpected_closed_or_missing_selected_slot_disposition":"BLOCKED_AND_REOPEN_SAMPLE_MANIFEST; NO_SILENT_SUBSTITUTION",
    "anti_extrapolation":"PHYSICAL_PASS_APPLIES_ONLY_TO_SEMANTIC_EPOCHS_WITH_REQUIRED_SAMPLE_COVERAGE_AND_LANE_S_SCOPE_PASS",
}

diagnostic_independence={
    "required_diagnostics":["P-DIAG-A","P-DIAG-B"],
    "requirements":[
        "separate implementation files and code hashes sealed before observation",
        "no function/code copy across diagnostics beyond primitive standard-library calls",
        "independent decode path for envelope/framing/primitive interpretation",
        "raw response bytes shared only as immutable input identity",
        "outputs compared only after each diagnostic result is sealed",
    ],
    "fake_independence_disposition":"BLOCKED",
}

lane_c={
    "lane_id":"C",
    "derived_closure_only":True,
    "rules":[
        {
            "dimension_id":"C05-D3-OP",
            "exact_prerequisites":["C05-D1-OP","C05-D2-OP","C06-D1-OP","C06-D2-OP","C06-D3-OP","C06-D4-OP"],
            "pass_rule":"PASS iff every exact prerequisite is current PASS under same scope signature and no newer reopen event exists.",
            "independent_evidence_acquisition_allowed":False,
        },
        {
            "dimension_id":"C06-D3-OP",
            "exact_prerequisites":["C06-D1-OP","C06-D2-OP","C06-D4-OP"],
            "additional_requirements":["PROVIDER_PRIMARY_SCALE_AUTHORITY","NONCIRCULAR_SCALE_PROOF","SEMANTIC_SOURCE_LINEAGE_RESOLVED","TARGET_EPOCH_SCOPE_APPLICABILITY_PASS","NO_UNRESOLVED_MATERIAL_CONTRADICTION"],
            "noncircularity_rule":"Neither expected market price, spread plausibility, project decoder output, nor agreement with /1000 implementation may serve as the authority that establishes the divisor.",
            "pass_rule":"PASS only when exact provider-authored scale semantics and target K1 applicability are independently bound and contradiction sweep is clear.",
            "independent_provider_object_acquisition_allowed":False,
        },
    ],
}

lineage_rules={
    "project_origin_never_independent_semantic_authority":True,
    "fork_copy_or_shared_upstream_counts_as_same_lineage":True,
    "same_publisher_multiple_pages_not_automatically_independent":True,
    "independence_requires":["distinct semantic source origin","no fork/copy derivation","documented provenance relationship","exact version/commit identity where applicable"],
    "unresolved_lineage_disposition":"BLOCKED",
    "duplicate_lineage_cannot_satisfy_multi_source_requirement":True,
}

epoch_policy={
    "policy_id":"BPESEM04-S-EPOCH-COVERAGE-V0_1",
    "target_interval_start":scope["full_domain_first_h1"],
    "target_interval_end":scope["full_domain_last_h1"],
    "change_point_discovery_rule":"Review all admissible provider-authored version/release/source-change evidence material to K1 semantic meaning. Every material change point splits the semantic epoch.",
    "coverage_rule":"Union of qualified semantic-authority intervals must cover the entire target interval with no uncovered time and no unresolved semantic change point.",
    "partial_coverage_disposition":"BLOCKED",
    "forward_or_backward_extrapolation_without_explicit_continuity_proof":"FORBIDDEN",
    "representation_presence_is_semantic_continuity":"FALSE",
    "new_change_point_after_seal":"REOPEN",
}

outcome_rules={
    "dimension_pass":"All authority roles required by DimensionAuthorityBasis are satisfied under the same exact scope; all mandatory lane-specific conditions PASS; no unresolved material contradiction/reopen event.",
    "dimension_fail":"Admissible exact target-scope authority positively establishes the registered proposition false, or a prospectively registered competing physical hypothesis uniquely survives and registered proposition is eliminated.",
    "dimension_blocked":"Evidence absent, inadmissible, non-immutable, scope-incomplete, lineage-unresolved, multiple material hypotheses survive, contradiction unresolved, sampling/diagnostic obligation violated, or required prerequisite not PASS.",
    "claim_projection":"FAIL if any mandatory dimension FAIL; PASS only if all mandatory dimensions PASS; otherwise BLOCKED.",
    "overall_c01_c07_pass":"All seven claims PASS under one current evidence horizon and scope authority.",
    "contract_qualification_pass":"This B-PE-SEM-04 contract passes only if its formalization, breaker and persisted-head final re-break pass. Contract PASS does not imply any C01-C07 evidence PASS.",
}

evidence_identity_policy={
    "semantic_slot_ids":[x["evidence_slot_id"] for x in semantic_slots],
    "lane_p_request_manifest_id":"BPESEM04-P-REQUEST-MANIFEST-V0_1",
    "lane_p_object_evidence_id_template":"BPESEM04-P-OBJ::{UTC_H1_ISO}::{RAW_RESPONSE_SHA256}",
    "semantic_epoch_manifest_id":"BPESEM04-S-SEMANTIC-EPOCH-MANIFEST-V0_1",
    "lane_p_result_manifest_id":"BPESEM04-P-PHYSICAL-DISCRIMINATION-RESULT-V0_1",
    "lane_s_result_manifest_id":"BPESEM04-S-SEMANTIC-AUTHORITY-RESULT-V0_1",
    "lane_c_result_manifest_id":"BPESEM04-C-DERIVED-CLOSURE-RESULT-V0_1",
    "allocation_rule":"All fixed slot IDs are frozen by this contract. Object IDs are deterministically allocated from the sealed pre-GET RequestManifest and raw response hash; no ad-hoc IDs after observation.",
}

sealing_policy={
    "canonical_json":"UTF-8, sorted keys, compact separators, allow_nan=false",
    "hash":"SHA-256",
    "semantic_source_seal_requires":["raw_bytes_sha256","exact_locator","publisher_identity","version_or_snapshot_identity","retrieval_time","scope_statement"],
    "lane_p_pre_observation_seals":["contract_seal","semantic_epoch_manifest_seal","request_manifest_seal","diagnostic_code_hashes","hypothesis_set_digest","sampling_policy_digest"],
    "lane_p_post_observation_seals":["raw_response_sha256","transport_metadata_digest","decompressed_bytes_sha256_if_any","diagnostic_result_seals","object_adjudication_seal"],
    "mutation_after_seal":"FORBIDDEN; NEW_VERSION_REQUIRED",
}

reopen_rules=[
    {"trigger":"new material semantic interpretation or physical hypothesis","effect":"REOPEN_AFFECTED_DIMENSIONS_AND_DEPENDENTS"},
    {"trigger":"new provider semantic change point","effect":"REOPEN_SCOPE_APPLICABILITY_AND_RESAMPLE_BOUNDARY_OBJECTS_BEFORE_NEW_GET"},
    {"trigger":"source bytes/version/provenance mutation","effect":"INVALIDATE_DEPENDENT_AUTHORITY"},
    {"trigger":"new contradiction","effect":"BLOCK_AFFECTED_PASS_UNTIL_RESOLVED"},
    {"trigger":"diagnostic code changes after pre-observation seal","effect":"INVALIDATE_PROSPECTIVE_DISCRIMINATION_AND_REQUIRE_NEW_PREOBSERVATION_FREEZE"},
    {"trigger":"sample manifest changes after first GET","effect":"INVALIDATE_LANE_P_EXECUTION"},
    {"trigger":"unexpected response wrapper/residual/layout","effect":"BLOCK_AND_ADD_MATERIAL_ALTERNATIVE_BEFORE_ANY_CONTINUATION"},
]

safeguards=[
    "S01_NO_SEMANTIC_AUTHORITY_FROM_RAW_PHYSICAL_COMPATIBILITY",
    "S02_NO_PHYSICAL_PASS_FROM_DOCUMENTATION_ALONE",
    "S03_NO_POST_HOC_HYPOTHESES_AFTER_NEW_BI5_OBSERVATION",
    "S04_NO_LIVE_UNVERSIONED_PROVIDER_PAGE_AS_DURABLE_AUTHORITY",
    "S05_NO_REFERENCE_IMPLEMENTATION_AS_SOLE_PROVIDER_AUTHORITY",
    "S06_NO_2026_SEMANTICS_BACKWARD_EXTRAPOLATION_WITHOUT_PROOF",
    "S07_NO_HISTORICAL_SEMANTICS_FORWARD_EXTRAPOLATION_WITHOUT_PROOF",
    "S08_NO_REPRESENTATION_PRESENCE_SEMANTIC_CONTINUITY_CONFLATION",
    "S09_NO_C08_TO_C01_C07_SELF_AUTHORIZATION",
    "S10_NO_C01_C07_TO_C08_PREAUTHORIZATION",
    "S11_NO_CIRCULAR_PRICE_SCALE_PLAUSIBILITY_AUTHORITY",
    "S12_NO_ASK_BID_ROLE_FROM_SPREAD_SIGN_ONLY",
    "S13_NO_TIMESTAMP_SEMANTICS_FROM_PLAUSIBLE_RANGE_ONLY",
    "S14_NO_VOLUME_SEMANTICS_FROM_BINARY32_DECODABILITY_ONLY",
    "S15_NO_PROJECT_IMPLEMENTATION_AS_INDEPENDENT_AUTHORITY",
    "S16_NO_BERD02_PROMOTION_BEYOND_NONDECISIVE_COMPATIBILITY",
    "S17_NO_PARTIAL_EPOCH_COVERAGE_AS_FULL_CONTINUITY",
    "S18_NO_DUPLICATE_LINEAGE_COUNTED_AS_INDEPENDENCE",
    "S19_NO_C05_D3_INDEPENDENT_EVIDENCE_LAUNDERING",
    "S20_NO_PROVIDER_OR_NETWORK_ACQUISITION_BEFORE_CONTRACT_QUALIFICATION",
]

execution_boundary={
    "this_contract_authorizes_provider_contact":False,
    "this_contract_authorizes_provider_bi5_get":False,
    "this_contract_authorizes_new_provider_object_acquisition":False,
    "this_contract_authorizes_new_semantic_discrimination_execution":False,
    "this_contract_authorizes_bfiq02r":False,
    "this_contract_authorizes_full_interval":False,
    "this_contract_authorizes_d_materialization":False,
    "this_contract_authorizes_backtest":False,
    "this_contract_authorizes_paper_broker_live":False,
    "post_contract_consumer_if_qualified":"A later explicitly opened acquisition/execution block may consume this contract; no network execution is self-authorized by contract PASS.",
}

contract={
    "schema":"B_PE_SEM_04_PROSPECTIVE_CLOSURE_EVIDENCE_CONTRACT_V0_1",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "governed_branch":"integration/system-v1",
    "candidate_parent_head":HEAD,
    "candidate_parent_tree":TREE,
    "selected_route_record":{"path":ROUTE_PATH,"git_blob":ROUTE_BLOB},
    "prior_bpesem03r":{"adjudication_path":PRIOR_ADJ_PATH,"adjudication_blob":PRIOR_ADJ_BLOB,"closeout_path":PRIOR_CLOSEOUT_PATH,"closeout_blob":PRIOR_CLOSEOUT_BLOB,"semantic_authority":"BLOCKED"},
    "scope_signature":{"path":SCOPE_PATH,"git_blob":SCOPE_BLOB,"scope_signature_id":scope["scope_signature_id"],"scope_signature_digest":scope["scope_signature_digest"],"provider_identity":scope["provider_identity"],"instrument_id":scope["instrument_id"],"representation_regime_id":scope["representation_regime_id"],"target_start":scope["full_domain_first_h1"],"target_end":scope["full_domain_last_h1"]},
    "dimension_authority_basis":{"path":BASIS_PATH,"git_blob":BASIS_BLOB,"basis_register_id":basis["basis_register_id"],"basis_register_digest":basis["basis_register_digest"]},
    "dimension_population":{"already_pass":PASS_DIMS,"blocked_physical_hypothesis":PHYSICAL_DIMS,"blocked_semantic_anchor":SEMANTIC_DIMS,"blocked_prerequisite_closure":PREREQ_DIMS},
    "lane_s":{
        "lane_id":"S",
        "purpose":"Prospective semantic authority and target-epoch scope closure.",
        "evidence_slots":semantic_slots,
        "semantic_authority_rules":semantic_authority_rules,
        "epoch_coverage_policy":epoch_policy,
        "source_lineage_rules":lineage_rules,
        "scale_noncircularity":{"dimension_id":"C06-D3-OP","prohibited_authority_inputs":["expected market price","spread plausibility","project decoder result","agreement with /1000 reference implementation"],"required_primary_source":"provider-authored exact scale/instrument semantic authority"},
    },
    "lane_p":{
        "lane_id":"P",
        "purpose":"Prospective decisive discrimination for exact 11 physical hypotheses.",
        "target_dimension_ids":PHYSICAL_DIMS,
        "hypothesis_sets":physical_hypotheses,
        "discriminators":discriminators,
        "sampling_policy":sampling_policy,
        "diagnostic_independence":diagnostic_independence,
        "known_prior_observation_role":"B-ERD-02 remains NONDECISIVE_COMPATIBILITY only",
        "pre_observation_freeze_required":True,
    },
    "lane_c":lane_c,
    "evidence_identity_policy":evidence_identity_policy,
    "sealing_policy":sealing_policy,
    "outcome_rules":outcome_rules,
    "reopen_rules":reopen_rules,
    "consumer_handoff":{
        "required_outputs_before_any_evidence_consumer_can_adjudicate":["Lane S result manifest","Lane P result manifest","Lane C derived closure manifest","current evidence horizon","scope applicability decisions","contradiction sweep result"],
        "handoff_does_not_imply_authorization":True,
    },
    "mandatory_safeguards":safeguards,
    "execution_boundary":execution_boundary,
    "created_at_utc":"2026-09-22T11:25:00Z",
}
contract["semantic_slot_set_digest"]=digest(sorted(semantic_slots,key=lambda x:x["evidence_slot_id"]))
contract["physical_hypothesis_set_digest"]=digest({k:physical_hypotheses[k] for k in sorted(physical_hypotheses)})
contract["discriminator_set_digest"]=digest(sorted(discriminators,key=lambda x:x["discriminator_id"]))
contract["sampling_policy_digest"]=digest(sampling_policy)
contract["lane_c_digest"]=digest(lane_c)
contract["safeguard_set_digest"]=digest(sorted(safeguards))
contract["contract_seal"]=seal(contract,"contract_seal")

OUT.mkdir(parents=True,exist_ok=True)
writej(OUT/"prospective_semantic_authority_closure_contract_v0_1.json",contract)

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(
    "# B-PE-SEM-04 — PROSPECTIVE C01-C07 SEMANTIC-AUTHORITY CLOSURE EVIDENCE CONTRACT — CANDIDATE\n\n"
    "Candidate parent HEAD: "+HEAD+"\n\n"
    "## Frozen structure\n\n"
    "~~~text\n"
    "Lane S semantic evidence slots = "+str(len(semantic_slots))+"\n"
    "Lane P physical hypothesis dimensions = "+str(len(PHYSICAL_DIMS))+"\n"
    "Lane P discriminators = "+str(len(discriminators))+"\n"
    "Lane C prerequisite dimensions = "+str(len(PREREQ_DIMS))+"\n"
    "Mandatory safeguards = "+str(len(safeguards))+"\n"
    "Target interval = "+scope["full_domain_first_h1"]+" -> "+scope["full_domain_last_h1"]+"\n"
    "Contract seal = "+contract["contract_seal"]+"\n"
    "~~~\n\n"
    "The contract freezes evidence namespaces, semantic-source admissibility, lineage rules, epoch coverage, all 11 physical hypothesis sets, prospective discriminators, deterministic sampling policy, diagnostic independence, sealing, PASS/FAIL/BLOCKED rules, reopen rules and consumer handoff before any new observation.\n\n"
    "Contract qualification does not imply C01-C07 semantic PASS and authorizes no provider/network acquisition.\n\n"
    "No provider contact, BI5 GET, new provider object, FULL_INTERVAL, D or backtest occurred.\n",
    encoding="utf-8"
)

print(json.dumps({
    "candidate_parent_head":HEAD,
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "semantic_slots":len(semantic_slots),
    "physical_dimensions":len(PHYSICAL_DIMS),
    "discriminators":len(discriminators),
    "safeguards":len(safeguards),
    "contract_seal":contract["contract_seal"],
},indent=2))
