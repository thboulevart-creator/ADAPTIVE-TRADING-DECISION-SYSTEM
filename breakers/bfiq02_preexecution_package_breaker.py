#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bfiq02"
R=ROOT/"reports"/"data-qualification"/"bfiq02_preexecution_package_adversarial_break_2026-09-21.md"

def canon(v):
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

def sha(v):
    return hashlib.sha256(canon(v) if not isinstance(v,bytes) else v).hexdigest()

def load(n):
    return json.loads((E/n).read_text())

def seal_ok(o,field):
    x=copy.deepcopy(o)
    recorded=x.pop(field,None)
    return recorded==sha(x)

inv=load("interval_inventory_v0_1.json")
req=load("request_manifest_v0_1.json")
budget=load("request_budget_v0_1.json")
shards=load("execution_shard_plan_v0_1.json")
diag=load("diagnostic_independence_manifest_v0_1.json")
sem=load("semantic_invariant_manifest_v0_1.json")
dur=load("durable_evidence_policy_v0_1.json")
scope=load("provisional_authority_scope_tuple_v0_1.json")
pkg=load("preexecution_package_v0_1.json")
provider=load("provider_delivery_identity_policy_v0_1.json")
regime=load("representation_regime_manifest_v0_1.json")
transport=load("transport_policy_v0_1.json")

errors=[]
def check(cond,code):
    if not cond:
        errors.append(code)

for obj,field,name in [
    (inv,"inventory_seal","INVENTORY_SEAL"),
    (req,"request_manifest_seal","REQUEST_MANIFEST_SEAL"),
    (budget,"budget_seal","REQUEST_BUDGET_SEAL"),
    (shards,"shard_plan_seal","SHARD_PLAN_SEAL"),
    (diag,"manifest_seal","DIAG_INDEPENDENCE_SEAL"),
    (sem,"manifest_seal","SEMANTIC_MANIFEST_SEAL"),
    (dur,"policy_seal","DURABLE_POLICY_SEAL"),
    (scope,"scope_seal","SCOPE_SEAL"),
    (pkg,"package_seal","PACKAGE_SEAL"),
    (provider,"policy_seal","PROVIDER_POLICY_SEAL"),
    (regime,"manifest_seal","REGIME_MANIFEST_SEAL"),
    (transport,"transport_policy_seal","TRANSPORT_POLICY_SEAL"),
]:
    check(seal_ok(obj,field),f"{name}_MISMATCH")

ints=inv["intervals"]
rows=req["rows"]
check(len(ints)==43868,"INVENTORY_COUNT")
check(inv["expected_open_interval_count"]==29543,"OPEN_COUNT")
check(inv["expected_closed_interval_count"]==14325,"CLOSED_COUNT")
check(inv["warmup_open_interval_count"]==20,"WARMUP_COUNT")
check(inv["interval_inventory_root"]==sha(ints),"INVENTORY_ROOT")
check(len(rows)==len(ints),"REQUEST_ROW_COUNT")

for i,(a,b) in enumerate(zip(ints,rows)):
    check(a["interval_ordinal"]==i,f"ORDINAL_{i}")
    check(b["interval_ordinal"]==i and b["interval_id"]==a["interval_id"],f"REQ_JOIN_{i}")
    if i:
        p=datetime.strptime(ints[i-1]["interval_start_utc"],"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        q=datetime.strptime(a["interval_start_utc"],"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        check(q-p==timedelta(hours=1),f"CONTIGUITY_{i}")
    if a["provider_component_requirement"]=="REQUIRED":
        check(b["request_expected"] is True,f"OPEN_REQUEST_{i}")
        t=datetime.strptime(a["interval_start_utc"],"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        expected=f"https://datafeed.dukascopy.com/datafeed/USATECHIDXUSD/{t.year}/{t.month-1:02d}/{t.day:02d}/{t.hour:02d}h_ticks.bi5"
        check(b["exact_request_locator_or_null"]==expected,f"URL_RENDER_{i}")
    else:
        check(b["request_expected"] is False and b["exact_request_locator_or_null"] is None,f"CLOSED_NO_REQUEST_{i}")

check(req["request_manifest_root"]==sha(rows),"REQUEST_ROOT")
required=[r for r in rows if r["request_expected"]]
check(len(required)==budget["planned_request_count"]==budget["maximum_actual_request_count"],"REQUEST_BUDGET_COUNT")

all_ids=[x for s in shards["shards"] for x in s["required_interval_ids"]]
check(len(all_ids)==len(required),"SHARD_CARDINALITY")
check(len(set(all_ids))==len(required),"SHARD_DUPLICATE")
check(set(all_ids)=={r["interval_id"] for r in required},"SHARD_MEMBERSHIP")
check(sum(s["required_request_count"] for s in shards["shards"])==len(required),"SHARD_COUNTS")

m=copy.deepcopy(rows)
m[0]["exact_request_locator_or_null"]="https://invalid.example/"
check(sha(m)!=req["request_manifest_root"],"MUTANT_LOCATOR_NOT_DETECTED")
m=copy.deepcopy(ints)
m.pop()
check(sha(m)!=inv["interval_inventory_root"],"MUTANT_INTERVAL_DROP_NOT_DETECTED")

check(sem["overall_semantic_authority_status"]=="BLOCKED","SEMANTIC_STATUS_NOT_BLOCKED")
check(not sem["decisive_invariants"],"DECISIVE_INVARIANTS_PRESENT_WHILE_BLOCKED")
check(pkg["pre_execution_eligibility"]=="BLOCKED","PACKAGE_NOT_BLOCKED")
check(scope["pre_execution_eligibility"]=="BLOCKED","SCOPE_NOT_BLOCKED")

demonstrated=[]

required_diag_fields={
    "decompressor_identity",
    "decompressor_version",
    "decompressor_binary_or_source_sha256",
    "parser_identity",
    "parser_source_blob_sha256",
    "projection_identity",
    "projection_source_blob_sha256",
    "invariant_evaluator_identity",
    "invariant_evaluator_source_blob_sha256",
}
for path in ("diagnostic_A","diagnostic_B"):
    missing=sorted(required_diag_fields-set(diag[path]))
    if missing:
        demonstrated.append({
            "id":"BFIQ02-F01-DIAGNOSTIC_MANIFEST_SCHEMA_UNDERSPECIFIED",
            "path":path,
            "missing":missing,
        })

if diag["stage_independence_verdicts"].get("decompression")=="PASS":
    demonstrated.append({
        "id":"BFIQ02-F02-SHARED_GENERIC_DECOMPRESSOR_OVERCLAIMED_AS_INDEPENDENT",
        "detail":"Both qualified I_A/I_B sources use Python stdlib lzma. Generic primitive sharing can be allowed, but the decompression stage must be explicitly classified as shared-generic-exempted rather than independently implemented PASS.",
    })

if any("IMMUTABLE" in x for x in dur.get("allowed_storage_classes",[])):
    demonstrated.append({
        "id":"BFIQ02-F03-DURABLE_STORAGE_CLASS_OVERCLAIMS_IMMUTABILITY",
        "detail":"GitHub release assets can be deleted. Asset-id plus exact SHA-256 can make mutation detectable, but the storage class itself is not intrinsically immutable.",
    })

if "authority_scope_tuple_digest_domain" not in scope:
    demonstrated.append({
        "id":"BFIQ02-F04-AUTHORITY_SCOPE_DIGEST_DOMAIN_IMPLICIT",
        "detail":"The provisional scope contains both authority_scope_tuple_digest and scope_seal but does not state the exact excluded fields for the digest domain.",
    })

check(pkg["diagnostic_independence_status"]=="PASS","PACKAGE_DIAG_STATUS")
check("C01_C07_CURRENT_AUTHORITY_NOT_PASS" in pkg["blocking_reason_codes"],"PACKAGE_BLOCK_REASON")

verdict="FAIL" if demonstrated or errors else ("BLOCKED" if pkg["pre_execution_eligibility"]=="BLOCKED" else "PASS")

lines=[
    "# B-FIQ-02 — PRE-EXECUTION PACKAGE — ADVERSARIAL BREAK",
    "",
    f"Structural verification errors: {len(errors)}",
    "",
    f"Demonstrated contract/package defects: {len(demonstrated)}",
    "",
    "## Structural checks",
    "",
    json.dumps(errors,indent=2),
    "",
    "## Demonstrated defects",
    "",
    json.dumps(demonstrated,indent=2),
    "",
    "## Break verdict",
    "",
    f"B-FIQ-02 MATERIALIZED CANDIDATE = {verdict}",
    "",
    "The upstream C01-C07 semantic-authority blocker is preserved and is not counted as a package-construction defect.",
    "",
    "No provider GET, FULL_INTERVAL execution, D materialization or backtest occurred.",
    "",
]
R.write_text("\n".join(lines),encoding="utf-8")
print(json.dumps({"structural_errors":errors,"demonstrated":demonstrated,"verdict":verdict},sort_keys=True))
