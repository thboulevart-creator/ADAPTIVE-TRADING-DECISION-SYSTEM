#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "bpesem03"
REPORT = ROOT / "reports" / "data-qualification" / "bpesem03_part1_foundation_materialization_2026-09-21.md"

CONTRACT_ID = "B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY"
CONTRACT_VERSION = "B_PE_SEM_02_OPERATIONAL_NATIVE_BI5_SEMANTIC_AUTHORITY_V0_6_CORRECTED"
DISCOVERY_POLICY_ID = "BPESEM02-GOVERNED-SEMANTIC-DISCOVERY-V0_6"
BRANCH = "integration/system-v1"

DIRECT_PREFIXES = (
    "evidence/bpe",
    "reports/data-qualification/bpe",
    "evidence/berd",
    "reports/data-qualification/berd",
    "evidence/bfiq",
    "reports/data-qualification/bfiq",
)
REF_RE = re.compile(
    rb"(?<![A-Za-z0-9_.-])"
    rb"(?:evidence|reports|04-REFERENCE|src|tools|breakers|\.github)"
    rb"/[A-Za-z0-9_.\-/]+"
)

def canon(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def digest(v: Any) -> str:
    return sha256_bytes(canon(v))

def seal(obj: dict[str, Any], field: str) -> str:
    x = dict(obj)
    x.pop(field, None)
    return digest(x)

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def git_blob_sha1(data: bytes) -> str:
    hdr = ("blob %d\\0" % len(data)).encode()
    return hashlib.sha1(hdr + data).hexdigest()

def source_identity(rel: str) -> dict[str, Any]:
    raw = (ROOT / rel).read_bytes()
    return {"path": rel, "git_blob": git_blob_sha1(raw), "sha256_raw_bytes": sha256_bytes(raw), "byte_length": len(raw)}

def write_json(name: str, obj: dict[str, Any]) -> dict[str, Any]:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / name
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\\n", encoding="utf-8")
    return source_identity(str(p.relative_to(ROOT)))

def ls_tree(head: str) -> dict[str, dict[str, Any]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", "-l", head], cwd=ROOT)
    out = {}
    for line in raw.decode("utf-8").splitlines():
        left, path = line.split("\\t", 1)
        mode, typ, blob, size = left.split()
        if typ == "blob":
            out[path] = {"mode": mode, "git_blob": blob, "size": int(size)}
    return out

def is_direct(path: str) -> bool:
    return any(path.startswith(pfx) for pfx in DIRECT_PREFIXES)

def read_refs(path: str, tree: dict[str, dict[str, Any]]) -> set[str]:
    raw = (ROOT / path).read_bytes()
    if bytes([0]) in raw[:8192]:
        return set()
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError:
        return set()
    refs = set()
    for m in REF_RE.finditer(raw):
        candidate = m.group(0).decode("utf-8").rstrip(".,;:)]}'\\\"")
        if candidate in tree:
            refs.add(candidate)
    return refs

def relevance(path: str) -> str:
    if path.startswith("evidence/bpe") or path.startswith("evidence/berd"):
        return "MATERIAL_VISIBLE"
    if path.startswith("evidence/bfiq") and any(k in path for k in ("semantic_invariant","representation_regime","provider_delivery_identity","interval_inventory")):
        return "MATERIAL_VISIBLE"
    return "GOVERNANCE_VISIBLE"

def mk_dimension(dim, proposition, cls, prereq=None, conditional_allowed=False):
    return {
        "dimension_id": dim,
        "exact_dimension_proposition": proposition,
        "dimension_class": cls,
        "prerequisite_dimension_ids": prereq or [],
        "future_execution_obligation_allowed": conditional_allowed,
    }

HEAD = git("rev-parse", "HEAD")
TREE = git("rev-parse", HEAD + "^{tree}")
CURRENT_BRANCH = git("rev-parse", "--abbrev-ref", "HEAD")
if CURRENT_BRANCH != BRANCH:
    raise RuntimeError("wrong branch " + CURRENT_BRANCH)

tree = ls_tree(HEAD)
direct = sorted(p for p in tree if is_direct(p))
discovered = set(direct)
queue = list(direct)
origins = {p: {"DIRECT_PREFIX"} for p in direct}

while queue:
    p = queue.pop(0)
    for r in read_refs(p, tree):
        origins.setdefault(r, set()).add("REF:" + p)
        if r not in discovered:
            discovered.add(r)
            queue.append(r)

mandatory = {
    "evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json",
    "evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json",
    "reports/data-qualification/bpe01r_empirical_evidence_sufficiency_final_rebreak_2026-09-21.md",
    "reports/data-qualification/bpesem01_semantic_authority_route_review_final_rebreak_2026-09-21.md",
    "reports/data-qualification/bpesem02_operational_semantic_authority_contract_final_rebreak_2026-09-21.md",
    "reports/data-qualification/bpesem02_operational_semantic_authority_contract_final_closeout_2026-09-21.md",
    "evidence/bfiq02/semantic_invariant_manifest_v0_1.json",
    "evidence/bfiq02/representation_regime_manifest_v0_1.json",
    "evidence/bfiq02/provider_delivery_identity_policy_v0_1.json",
    "evidence/bfiq02/interval_inventory_v0_1.json",
    "evidence/berd02/gha_run_35533153289/PROVENANCE.json",
    "evidence/berd02/gha_run_35533153289/execution_result.json",
}
missing = sorted(p for p in mandatory if p not in tree)
if missing:
    raise RuntimeError("mandatory baseline artifacts absent: " + repr(missing))
discovered |= mandatory
for p in mandatory:
    origins.setdefault(p, set()).add("MANDATORY_LINEAGE")

records = []
for p in sorted(discovered):
    meta = tree[p]
    records.append({
        "path": p,
        "git_blob": meta["git_blob"],
        "size": meta["size"],
        "discovery_origin": sorted(origins.get(p, {"MANDATORY_LINEAGE"})),
        "relevance_disposition": relevance(p),
        "controlling_decision_refs": [],
    })

policy_payload = {
    "policy_id": DISCOVERY_POLICY_ID,
    "case_sensitive": True,
    "git_tree_recursive_enumeration": True,
    "direct_prefixes": list(DIRECT_PREFIXES),
    "registry_path_prefix": "evidence/bpesem/registry/",
    "reference_closure": "TRANSITIVE_FIXED_POINT",
    "visited_identity": "{path,git_blob}",
    "unresolved_required_reference_disposition": "BLOCKED",
}
policy_digest = digest(policy_payload)
discovery_result_digest = digest([
    {
        "path": r["path"],
        "git_blob": r["git_blob"],
        "discovery_origin": r["discovery_origin"],
        "relevance_disposition": r["relevance_disposition"],
        "controlling_decision_refs": r["controlling_decision_refs"],
    }
    for r in records
])

baseline = {
    "schema": "B_PE_SEM_02_GOVERNED_SEMANTIC_EVIDENCE_BASELINE_V0_4",
    "baseline_id": "BPESEM03-GOVERNED-EVIDENCE-BASELINE-V0_1",
    "contract_id": CONTRACT_ID,
    "contract_version": CONTRACT_VERSION,
    "governed_branch": BRANCH,
    "fresh_live_head": HEAD,
    "fresh_live_tree_sha": TREE,
    "fresh_head_observed_at_utc": "2026-09-21T20:00:00Z",
    "baseline_head": HEAD,
    "baseline_tree_sha": TREE,
    "baseline_materialization_parent_head": HEAD,
    "baseline_materialization_commit_binding": "EXTERNAL_BASELINE_PERSISTENCE_RECORD_REQUIRED",
    "parent_relation_status": "PENDING_PERSISTENCE_BINDING",
    "discovery_policy_id": DISCOVERY_POLICY_ID,
    "discovery_policy_digest": policy_digest,
    "discovery_result_digest": discovery_result_digest,
    "mandatory_lineages": sorted(mandatory),
    "direct_discovered_count": len(direct),
    "reference_closure_member_count": len(discovered - set(direct)),
    "baseline_member_count": len(records),
    "discovered_repository_artifacts": records,
    "baseline_member_refs": [
        {"path": r["path"], "git_blob": r["git_blob"], "relevance_disposition": r["relevance_disposition"]}
        for r in records
    ],
}
baseline["baseline_digest"] = seal(baseline, "baseline_digest")
baseline_ident = write_json("governed_semantic_evidence_baseline_v0_1.json", baseline)

claims = [
    {"claim_id":"BPE-SEM-C01-OP","exact_claim_proposition":"Target K1 bytes use the authorized LZMA-family envelope and successful decoding yields the physical slot byte stream.","mandatory_dimensions":[
        mk_dimension("C01-D1-OP","compression family = LZMA","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C01-D2-OP","exact envelope/container mode for target K1","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C01-D3-OP","exact stream/wrapper admission rule","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C01-D4-OP","decompressed output role = physical slot byte stream","SEMANTIC_ANCHOR")]},
    {"claim_id":"BPE-SEM-C02-OP","exact_claim_proposition":"Decompressed bytes are framed from byte zero into fixed complete records under exact residual/header rules.","mandatory_dimensions":[
        mk_dimension("C02-D1-OP","complete record width = 20 bytes","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C02-D2-OP","frame origin = byte zero","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C02-D3-OP","terminal residual/trailing-byte disposition","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C02-D4-OP","per-record header/delimiter presence and semantics","PHYSICAL_HYPOTHESIS")]},
    {"claim_id":"BPE-SEM-C03-OP","exact_claim_proposition":"Each complete record has the authorized five-field big-endian integer/float physical layout.","mandatory_dimensions":[
        mk_dimension("C03-D1-OP","byte order = big-endian","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C03-D2-OP","exact five-field physical order","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C03-D3-OP","first three fields obey SIGNEDNESS_EQUIVALENCE_RULE_V0_1 or exact signedness authority","CONDITIONAL_RULE",conditional_allowed=True),
        mk_dimension("C03-D4-OP","final two fields = IEEE-754 binary32","PHYSICAL_HYPOTHESIS")]},
    {"claim_id":"BPE-SEM-C04-OP","exact_claim_proposition":"First physical integer field denotes a millisecond offset from the represented UTC H1 origin.","mandatory_dimensions":[
        mk_dimension("C04-D1-OP","timestamp offset unit = millisecond","SEMANTIC_ANCHOR"),
        mk_dimension("C04-D2-OP","reference origin = represented provider H1 object hour","SEMANTIC_ANCHOR"),
        mk_dimension("C04-D3-OP","hour/time basis = UTC or exact provider-equivalent mapping","SEMANTIC_ANCHOR"),
        mk_dimension("C04-D4-OP","valid offset domain = exact authorized domain for one H1","SEMANTIC_ANCHOR")]},
    {"claim_id":"BPE-SEM-C05-OP","exact_claim_proposition":"Second and third integer fields are raw ask then raw bid and price-conversion prerequisites are closed.","mandatory_dimensions":[
        mk_dimension("C05-D1-OP","field roles/order = ask_raw then bid_raw","SEMANTIC_ANCHOR"),
        mk_dimension("C05-D2-OP","raw price integers obey SIGNEDNESS_EQUIVALENCE_RULE_V0_1 or exact signedness authority","CONDITIONAL_RULE",conditional_allowed=True),
        mk_dimension("C05-D3-OP","no unresolved prerequisite semantic state between raw ask/bid and logical price conversion","PREREQUISITE_CLOSURE",["C05-D1-OP","C05-D2-OP","C06-D1-OP","C06-D2-OP","C06-D3-OP","C06-D4-OP"])]},
    {"claim_id":"BPE-SEM-C06-OP","exact_claim_proposition":"For USATECHIDXUSD target K1, logical ask/bid price = raw integer / 1000.","mandatory_dimensions":[
        mk_dimension("C06-D1-OP","exact applicability to USATECHIDXUSD and target K1 representation","SEMANTIC_ANCHOR"),
        mk_dimension("C06-D2-OP","numeric divisor = 1000","SEMANTIC_ANCHOR"),
        mk_dimension("C06-D3-OP","scale authority is non-circular, identity-bound, scope-bound and contradiction-sensitive","PREREQUISITE_CLOSURE"),
        mk_dimension("C06-D4-OP","temporal/version applicability covers intended semantic epoch conditionally on K1 classification","SEMANTIC_ANCHOR")]},
    {"claim_id":"BPE-SEM-C07-OP","exact_claim_proposition":"Fourth and fifth fields are provider-native ask-volume then bid-volume binary32 values with exact authorized transform.","mandatory_dimensions":[
        mk_dimension("C07-D1-OP","field roles/order = ask_volume_raw then bid_volume_raw","SEMANTIC_ANCHOR"),
        mk_dimension("C07-D2-OP","primitive encoding = IEEE-754 binary32","PHYSICAL_HYPOTHESIS"),
        mk_dimension("C07-D3-OP","exact representation-level transform/scale including explicit no-additional-scale when applicable","SEMANTIC_ANCHOR")]},
]
claim_reg={"schema":"B_PE_SEM_02_CLAIM_DIMENSION_REGISTER_V0_2","register_id":"BPESEM03-C01-C07-CLAIM-DIMENSION-REGISTER-V0_1","contract_id":CONTRACT_ID,"contract_version":CONTRACT_VERSION,"claims":claims,"created_at_utc":"2026-09-21T20:00:00Z"}
claim_reg["register_digest"]=seal(claim_reg,"register_digest")
claim_ident=write_json("claim_dimension_register_v0_1.json",claim_reg)

primary={}
for c in claims:
    for d in c["mandatory_dimensions"]:
        primary[d["dimension_id"]]=d
basis_rows=[]
for dim,d in sorted(primary.items()):
    cls=d["dimension_class"]
    allowed=["SIGNEDNESS_EQUIVALENCE_RULE_V0_1"] if dim in {"C03-D3-OP","C05-D2-OP"} else []
    modes=["CONFORMANCE_ONLY"]+(["CONDITIONAL_SEMANTIC_SIGNEDNESS"] if allowed else [])
    if cls=="PHYSICAL_HYPOTHESIS":
        roles=["ADMISSIBLE_EXACT_PHYSICAL_EVIDENCE","SEALED_HYPOTHESIS_SET","KNOWN_MATERIAL_ALTERNATIVES_CLOSED","SCOPE_APPLICABILITY_PASS"]
    elif cls=="SEMANTIC_ANCHOR":
        roles=["ADMISSIBLE_SEMANTIC_ANCHOR","SEMANTIC_SOURCE_LINEAGE_RESOLVED","SCOPE_APPLICABILITY_PASS"]
    elif cls=="CONDITIONAL_RULE":
        roles=["SEALED_RULE_RECORD","EXACT_AFFECTED_FIELD_SET","NONWAIVABLE_EXECUTION_OBLIGATION","SCOPE_APPLICABILITY_PASS"]
    else:
        roles=["EXACT_PREREQUISITE_CLOSURE","SCOPE_APPLICABILITY_PASS"]
    if dim=="C06-D3-OP":
        roles=["ADMISSIBLE_EXACT_SEMANTIC_EVIDENCE","SEALED_SEMANTIC_ANCHOR","SEMANTIC_SOURCE_LINEAGE_RESOLVED","SCOPE_APPLICABILITY_PASS","NO_UNRESOLVED_MATERIAL_CONTRADICTION"]
    basis_rows.append({"dimension_id":dim,"primary_authority_class":cls,"required_scope_applicability":True,"exact_prerequisite_dimension_ids":d["prerequisite_dimension_ids"],"allowed_conditional_semantic_rule_ids":allowed,"allowed_obligation_modes":modes,"required_authority_roles":roles})
basis_reg={"schema":"B_PE_SEM_02_DIMENSION_AUTHORITY_BASIS_REGISTER_V0_3","basis_register_id":"BPESEM03-DIMENSION-AUTHORITY-BASIS-REGISTER-V0_1","claim_dimension_register_id":claim_reg["register_id"],"claim_dimension_register_digest":claim_reg["register_digest"],"dimension_bases":basis_rows,"created_at_utc":"2026-09-21T20:00:00Z"}
basis_reg["basis_register_digest"]=seal(basis_reg,"basis_register_digest")
basis_ident=write_json("dimension_authority_basis_register_v0_1.json",basis_reg)

scope={"schema":"B_PE_SEM_02_OPERATIONAL_SCOPE_SIGNATURE_V0_3","scope_signature_id":"BPESEM03-USATECH-K1-SEMANTIC-SCOPE-V0_1","provider_identity":"DUKASCOPY","instrument_id":"USATECHIDXUSD","representation_identity":"DUKASCOPY_NATIVE_BI5_HOURLY_TICKS","representation_regime_id":"K1_LEGACY_HOURLY_TICK_BI5","native_object_family":"HOURLY_HH_TICKS_BI5","canonical_delivery_host":"datafeed.dukascopy.com","provider_delivery_identity_policy_id":"BFIQ02-DUKASCOPY-PROVIDER-DELIVERY-V0_1","provider_delivery_identity_policy_seal":"302b3abe97a495cf173ae3561077fe59bbd8b71c3517220c115edcc82bf8387a","representation_regime_manifest_id":"BFIQ02-USATECH-K1-REGIME-MANIFEST-V0_1","representation_regime_manifest_seal":"368659c30c480673fea57030e63389d1d3950bb544de684d41120794389c90d5","execution_window_freeze_path":"04-REFERENCE/EXECUTION-WINDOW-FREEZE.json","execution_window_freeze_blob":"bf7c43e9d90d952dfa3715c28575fdf6cf379a89","evaluation_first_open_slot_utc":"2021-08-15T22:00:00+00:00","evaluation_last_open_slot_utc":"2026-08-14T20:00:00+00:00","mandatory_warmup_h1_bars":20,"session_calendar_contract":"DUKASCOPY_USATECH_SESSION_CALENDAR_V3","session_calendar_path":"tools/dukascopy_usatech_calendar.py","session_calendar_git_blob":"fab634aab7b8c299b0139c3c43bf5b89a2aa03d0","full_domain_first_h1":"2021-08-13T01:00:00Z","full_domain_last_h1":"2026-08-14T20:00:00Z","wall_clock_interval_count":43868,"expected_open_interval_count":29543,"expected_closed_interval_count":14325,"warmup_open_interval_count":20,"evaluation_open_interval_count":29523,"interval_inventory_path":"evidence/bfiq02/interval_inventory_v0_1.json","interval_inventory_git_blob":"8c02972228941d8b6f1aacaf9ac6bf75fb0f2029","interval_inventory_sha256_raw_bytes":"7f55d600d9bfcab804283d668a9f74b555e55cc6c98a99919e0012c08f038f5d","interval_inventory_root":"26d86a34a00e6697208a6481867f6338f21c1deae26e5be74b52cc8ba83eced8","semantic_scope_predicate":"SEMANTIC_RULE_SCOPE_APPLICABILITY_ONLY","representation_presence_authority":"NOT_ADJUDICATED_IN_B_PE_SEM_03","c08_authority_effect":"NONE","contract_id":CONTRACT_ID,"contract_version":CONTRACT_VERSION}
scope["scope_signature_digest"]=seal(scope,"scope_signature_digest")
scope_ident=write_json("operational_semantic_scope_signature_v0_1.json",scope)

rule={"schema":"B_PE_SEM_02_RULE_RECORD_V0_1","rule_id":"SIGNEDNESS_EQUIVALENCE_RULE_V0_1","rule_type":"CONDITIONAL_MATHEMATICAL_EQUIVALENCE","target_dimension_ids":["C03-D3-OP","C05-D2-OP"],"exact_proposition":"For an exact 32-bit bit pattern, signed_int32 equals unsigned_uint32 iff high_bit == 0; if high_bit == 1 their numeric interpretations differ.","exact_condition":"high_bit == 0","affected_field_set":["timestamp_offset_raw","ask_price_raw","bid_price_raw"],"violation_disposition":"BLOCKED_UNLESS_EXACT_SIGNEDNESS_HAS_SEPARATE_CURRENT_AUTHORITY","created_at_utc":"2026-09-21T20:00:00Z"}
rule["rule_seal"]=seal(rule,"rule_seal")
rule_ident=write_json("signedness_equivalence_rule_v0_1.json",rule)

obligations=[]
for dim,fields,claim in [
    ("C03-D3-OP",["timestamp_offset_raw","ask_price_raw","bid_price_raw"],"BPE-SEM-C03-OP"),
    ("C05-D2-OP",["ask_price_raw","bid_price_raw"],"BPE-SEM-C05-OP")]:
    obligations.append({"obligation_id":"SIGNEDNESS_HIGH_BIT_ZERO_REQUIRED::"+dim,"source_claim_id":claim,"source_dimension_id":dim,"rule_id":rule["rule_id"],"exact_predicate":"high_bit == 0 for every affected target-domain field instance unless exact signedness authority is separately current PASS","affected_field_set":fields,"evaluation_scope":"EVERY_ACCEPTED_TARGET_DOMAIN_RECORD","evaluation_cardinality":"EVERY_ACCEPTED_AFFECTED_FIELD_INSTANCE","on_pass":"CONDITIONAL_SIGNEDNESS_EQUIVALENCE_SATISFIED","on_fail":"BLOCKED — SIGNEDNESS_SEMANTIC_AMBIGUITY","on_blocked":"BLOCKED","nonwaivable":True})
obligation_digest=digest(sorted(obligations,key=lambda x:canon(x)))
obl={"schema":"B_PE_SEM_03_EXECUTION_OBLIGATION_SET_V0_1","obligations":obligations,"obligation_set_digest":obligation_digest}
obl_ident=write_json("execution_obligation_set_v0_1.json",obl)

package={"schema":"B_PE_SEM_03_FOUNDATION_PACKAGE_V0_1","package_id":"BPESEM03-FOUNDATION-PACKAGE-V0_1","starting_head":HEAD,"starting_tree":TREE,"contract_id":CONTRACT_ID,"contract_version":CONTRACT_VERSION,"artifacts":{"baseline":baseline_ident,"claim_dimension_register":claim_ident,"dimension_authority_basis_register":basis_ident,"scope_signature":scope_ident,"signedness_rule":rule_ident,"execution_obligations":obl_ident},"baseline_digest":baseline["baseline_digest"],"claim_dimension_register_digest":claim_reg["register_digest"],"dimension_authority_basis_register_digest":basis_reg["basis_register_digest"],"scope_signature_digest":scope["scope_signature_digest"],"rule_set_digest":digest([{"rule_id":rule["rule_id"],"rule_seal":rule["rule_seal"]}]),"obligation_set_digest":obligation_digest,"provider_network_requests_performed":False,"semantic_adjudication_performed":False,"created_at_utc":"2026-09-21T20:00:00Z"}
package["package_seal"]=seal(package,"package_seal")
write_json("foundation_package_v0_1.json",package)

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text("# B-PE-SEM-03 — PART 1/3 FOUNDATION MATERIALIZATION\\n\\n"
                  f"Starting HEAD: {HEAD}\\n\\nStarting tree: {TREE}\\n\\n"
                  "Materialized baseline, claim/dimension register, authority-basis register, exact scope, signedness rule and execution obligations.\\n\\n"
                  f"Direct discovered blobs: {len(direct)}\\n\\n"
                  f"Reference-closure members: {len(discovered)}\\n\\n"
                  f"Baseline digest: {baseline['baseline_digest']}\\n\\n"
                  f"Claim register digest: {claim_reg['register_digest']}\\n\\n"
                  f"Basis register digest: {basis_reg['basis_register_digest']}\\n\\n"
                  f"Scope digest: {scope['scope_signature_digest']}\\n\\n"
                  f"Obligation digest: {obligation_digest}\\n\\n"
                  f"Foundation package seal: {package['package_seal']}\\n\\n"
                  "No provider contact, BI5 GET, semantic execution, FULL_INTERVAL, D or backtest occurred.\\n\\nSTOP PART 1.\\n",
                  encoding="utf-8")

print(json.dumps({"starting_head":HEAD,"starting_tree":TREE,"direct_discovered_count":len(direct),"baseline_member_count":len(records),"baseline_digest":baseline["baseline_digest"],"claim_register_digest":claim_reg["register_digest"],"basis_register_digest":basis_reg["basis_register_digest"],"scope_signature_digest":scope["scope_signature_digest"],"obligation_set_digest":obligation_digest,"package_seal":package["package_seal"]},indent=2,sort_keys=True))
