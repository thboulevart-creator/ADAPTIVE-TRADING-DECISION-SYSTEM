#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import lzma
import _lzma
import _struct
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.dukascopy_usatech_calendar import (
    CALENDAR_CONTRACT,
    EXPECTED_OPEN,
    EXPECTED_CLOSED,
    classify_slot,
)

OUT = ROOT / "evidence" / "bfiq02"
REPORT = ROOT / "reports" / "data-qualification" / "bfiq02_preexecution_package_candidate_2026-09-21.md"

CONTRACT_ID = "B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION"
CONTRACT_VERSION = "B_FIQ_01_USATECH_FULL_INTERVAL_EMPIRICAL_REPRESENTATION_QUALIFICATION_V0_2_CORRECTED"

START_OPEN = datetime(2021, 8, 15, 22, tzinfo=timezone.utc)
LAST_OPEN = datetime(2026, 8, 14, 20, tzinfo=timezone.utc)
INSTRUMENT = "USATECHIDXUSD"
FREEZE_BLOB = "bf7c43e9d90d952dfa3715c28575fdf6cf379a89"
CALENDAR_BLOB = "fab634aab7b8c299b0139c3c43bf5b89a2aa03d0"
IA_BLOB = "cab85272bc5a2e229f56f1e02e624d68dc84ce29"
IB_BLOB = "6d14704548861c13dfc809adad6ae7a21e31c2ca"
IA_REPORT_BLOB = "d9c51d7455092a90621dc76564c337d57c7c9c0b"
IB_REPORT_BLOB = "d1b248cb98251f84a48619a63e34ef1e39395e3f"
IB_PROVENANCE_BLOB = "a6f3a2c1c8e6e1c1aeb496be87e17330516925e8"  # checked by package audit if stale
BPE02_PATH = ROOT / "evidence" / "bpe02" / "native_bi5_provider_reference_evidence_bundle_v0_1.json"

def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def sha(v):
    if isinstance(v, bytes):
        raw = v
    else:
        raw = canon(v)
    return hashlib.sha256(raw).hexdigest()

def seal(obj, field):
    x=dict(obj)
    x.pop(field, None)
    return sha(x)

def iso_hour(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def git_blob_sha1(data: bytes) -> str:
    header=f"blob {len(data)}\0".encode()
    return hashlib.sha1(header+data).hexdigest()

def source_identity(rel):
    p=ROOT/rel
    data=p.read_bytes()
    return {
        "path": rel,
        "git_blob_sha1": git_blob_sha1(data),
        "sha256_raw_bytes": hashlib.sha256(data).hexdigest(),
        "byte_length": len(data),
    }

def runtime_binary_identity(path):
    p=Path(path)
    data=p.read_bytes()
    return {
        "path": str(p),
        "sha256_raw_bytes": hashlib.sha256(data).hexdigest(),
        "byte_length": len(data),
    }

def write_json(name, obj):
    path=OUT/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return source_identity(str(path.relative_to(ROOT)))

def derive_warmup():
    opens=[]
    t=START_OPEN-timedelta(hours=1)
    while len(opens)<20:
        c=classify_slot(t.date(), t.hour)
        if c.status==EXPECTED_OPEN:
            opens.append(t)
        t-=timedelta(hours=1)
    opens.reverse()
    return opens

warmup=derive_warmup()
full_first=warmup[0]

intervals=[]
t=full_first
ordinal=0
warmup_set={iso_hour(x) for x in warmup}
evaluation_open=[]
while t<=LAST_OPEN:
    c=classify_slot(t.date(), t.hour)
    if c.status not in (EXPECTED_OPEN, EXPECTED_CLOSED):
        raise RuntimeError(f"unclosed calendar status {c.status} at {t}")
    end=t+timedelta(hours=1)
    start_s=iso_hour(t)
    end_s=iso_hour(end)
    rec={
        "interval_ordinal": ordinal,
        "interval_start_utc": start_s,
        "interval_end_utc": end_s,
        "expected_market_status": c.status,
        "calendar_reason": c.reason,
        "calendar_schedule": c.schedule,
        "provider_component_requirement": "REQUIRED" if c.status==EXPECTED_OPEN else "NOT_REQUIRED_CALENDAR_CLOSED",
        "is_warmup_open_member": start_s in warmup_set,
        "is_evaluation_open_member": bool(c.status==EXPECTED_OPEN and START_OPEN<=t<=LAST_OPEN),
    }
    rec["interval_id"]=sha({
        "instrument_identity":INSTRUMENT,
        "interval_start_utc":start_s,
        "interval_end_utc":end_s,
        "execution_window_freeze_identity":FREEZE_BLOB,
        "session_calendar_identity":{"contract":CALENDAR_CONTRACT,"git_blob":CALENDAR_BLOB},
        "expected_market_status":c.status,
    })
    intervals.append(rec)
    if rec["is_evaluation_open_member"]:
        evaluation_open.append(start_s)
    ordinal+=1
    t=end

if len(warmup)!=20:
    raise RuntimeError("warmup cardinality")
if evaluation_open[0]!=iso_hour(START_OPEN) or evaluation_open[-1]!=iso_hour(LAST_OPEN):
    raise RuntimeError("evaluation boundaries mismatch")
if sum(1 for x in intervals if x["is_warmup_open_member"])!=20:
    raise RuntimeError("warmup inventory cardinality mismatch")

inventory={
    "schema":"B_FIQ_01_INTERVAL_INVENTORY_V0_1",
    "inventory_id":"BFIQ02-USATECH-INTERVAL-INVENTORY-V0_1",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "provider_identity":"DUKASCOPY",
    "instrument_identity":INSTRUMENT,
    "execution_window_freeze_identity":{
        "path":"04-REFERENCE/EXECUTION-WINDOW-FREEZE.json",
        "git_blob":FREEZE_BLOB,
        "first_included_open_slot_utc":iso_hour(START_OPEN),
        "last_included_open_slot_utc":iso_hour(LAST_OPEN),
        "warmup_h1_bars":20,
    },
    "warmup_rule_identity":"FINAL_20_EXPECTED_OPEN_H1_STRICTLY_BEFORE_FIRST_INCLUDED_OPEN_V0_1",
    "session_calendar_identity":{
        "contract":CALENDAR_CONTRACT,
        "path":"tools/dukascopy_usatech_calendar.py",
        "git_blob":CALENDAR_BLOB,
    },
    "full_domain_first_h1":iso_hour(full_first),
    "full_domain_last_h1":iso_hour(LAST_OPEN),
    "wall_clock_interval_count":len(intervals),
    "expected_open_interval_count":sum(x["expected_market_status"]==EXPECTED_OPEN for x in intervals),
    "expected_closed_interval_count":sum(x["expected_market_status"]==EXPECTED_CLOSED for x in intervals),
    "warmup_open_interval_count":20,
    "evaluation_open_interval_count":len(evaluation_open),
    "intervals":intervals,
    "created_at_utc":"2026-09-21T15:00:00Z",
}
inventory["interval_inventory_root"]=sha(intervals)
inventory["inventory_seal"]=seal(inventory,"inventory_seal")

provider_policy={
    "schema":"B_FIQ_01_PROVIDER_DELIVERY_IDENTITY_POLICY_V0_1",
    "policy_id":"BFIQ02-DUKASCOPY-PROVIDER-DELIVERY-V0_1",
    "provider_identity":"DUKASCOPY",
    "allowed_delivery_endpoints":[
        {"scheme":"https","hostname":"datafeed.dukascopy.com","port":443,"endpoint_role":"K1_LEGACY_HOURLY_TICK_OBJECT_CANONICAL"}
    ],
    "allowed_redirect_edges":[],
    "tls_policy":"SYSTEM_TRUST_STORE_FAIL_CLOSED",
    "http_version_policy":"HTTP_1_1",
    "provider_identity_evidence_refs":[
        "evidence/bpe03/provider_snapshots/dukascopy_api_support_2013_hourly_history.json",
        "evidence/berd02/gha_run_35533153289/PROVENANCE.json",
    ],
    "created_at_utc":"2026-09-21T15:00:00Z",
}
provider_policy["policy_seal"]=seal(provider_policy,"policy_seal")

regime_manifest={
    "schema":"B_FIQ_01_REPRESENTATION_REGIME_MANIFEST_V0_1",
    "manifest_id":"BFIQ02-USATECH-K1-REGIME-MANIFEST-V0_1",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "provider_delivery_identity_policy_id":provider_policy["policy_id"],
    "provider_delivery_identity_policy_seal":provider_policy["policy_seal"],
    "regimes":[{
        "regime_id":"K1_LEGACY_HOURLY_TICK_BI5",
        "representation_identity":"DUKASCOPY_NATIVE_BI5_HOURLY_TICKS",
        "applicability_rule":"ALL_INTERVALS_WITH_EXPECTED_MARKET_STATUS_EXPECTED_OPEN_IN_SEALED_INVENTORY",
        "interval_domain_rule":"ONE_PROVIDER_OBJECT_PER_EXPECTED_OPEN_UTC_H1",
        "locator_rendering_rule":"https://datafeed.dukascopy.com/datafeed/{INSTRUMENT}/{YYYY}/{MONTH_ZERO_INDEXED_2D}/{DD}/{HH}h_ticks.bi5",
        "locator_source_evidence_refs":[
            "evidence/berd02/locator_manifest_v0_1.json",
            "evidence/berd02/gha_run_35533153289/PROVENANCE.json",
        ],
        "representation_semantic_authority_refs":[
            "evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json"
        ],
        "transition_boundary_evidence_refs_if_any":[],
    }],
    "open_world_rule":"POSITIVE_MATERIAL_UNKNOWN_OR_COMPETING_REPRESENTATION_EVIDENCE_BLOCKS_CURRENT_LINEAGE",
    "created_at_utc":"2026-09-21T15:00:00Z",
}
regime_manifest["manifest_seal"]=seal(regime_manifest,"manifest_seal")

rows=[]
for x in intervals:
    if x["provider_component_requirement"]=="REQUIRED":
        t=datetime.strptime(x["interval_start_utc"],"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        url=f"https://datafeed.dukascopy.com/datafeed/{INSTRUMENT}/{t.year}/{t.month-1:02d}/{t.day:02d}/{t.hour:02d}h_ticks.bi5"
        row={
            "interval_ordinal":x["interval_ordinal"],
            "interval_id":x["interval_id"],
            "expected_market_status":x["expected_market_status"],
            "provider_component_requirement":"REQUIRED",
            "regime_id_or_null":"K1_LEGACY_HOURLY_TICK_BI5",
            "exact_request_locator_or_null":url,
            "provider_delivery_endpoint_identity_or_null":"https://datafeed.dukascopy.com:443",
            "request_expected":True,
        }
    else:
        row={
            "interval_ordinal":x["interval_ordinal"],
            "interval_id":x["interval_id"],
            "expected_market_status":x["expected_market_status"],
            "provider_component_requirement":"NOT_REQUIRED_CALENDAR_CLOSED",
            "regime_id_or_null":None,
            "exact_request_locator_or_null":None,
            "provider_delivery_endpoint_identity_or_null":None,
            "request_expected":False,
        }
    rows.append(row)

request_manifest={
    "schema":"B_FIQ_01_REQUEST_MANIFEST_V0_2",
    "request_manifest_id":"BFIQ02-USATECH-REQUEST-MANIFEST-V0_1",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "interval_inventory_id":inventory["inventory_id"],
    "interval_inventory_root":inventory["interval_inventory_root"],
    "representation_regime_manifest_id":regime_manifest["manifest_id"],
    "representation_regime_manifest_seal":regime_manifest["manifest_seal"],
    "provider_delivery_identity_policy_id":provider_policy["policy_id"],
    "provider_delivery_identity_policy_seal":provider_policy["policy_seal"],
    "rows":rows,
    "required_request_count":sum(r["request_expected"] for r in rows),
    "closed_no_request_count":sum(not r["request_expected"] for r in rows),
    "created_at_utc":"2026-09-21T15:00:00Z",
}
request_manifest["request_manifest_root"]=sha(rows)
request_manifest["request_manifest_seal"]=seal(request_manifest,"request_manifest_seal")

transport_policy={
    "schema":"B_FIQ_02_TRANSPORT_POLICY_V0_1",
    "transport_policy_id":"BFIQ02-K1-CURL-IPV4-HTTPS-V0_1",
    "implementation":"curl",
    "force_ipv4":True,
    "http_version":"1.1",
    "method":"GET",
    "automatic_retry_count":0,
    "automatic_content_decoding":False,
    "request_headers":{"Accept":"*/*","Accept-Encoding":"identity","User-Agent":"ATDS-BFIQ/1.0"},
    "automatic_redirect_follow":False,
    "max_redirects":0,
    "connect_timeout_seconds":10,
    "per_request_total_timeout_seconds":30,
    "max_response_body_bytes":52428800,
    "max_parallel_requests":4,
    "aggregate_request_start_rate_per_second":2,
    "preserve_exact_response_body":True,
    "preserve_request_header_trace":True,
    "preserve_response_headers":True,
    "source_demonstration":{"workflow_run_id":35533153289,"execution_id":"BERD02-GHA-35533153289-1"},
    "created_at_utc":"2026-09-21T15:00:00Z",
}
transport_policy["transport_policy_seal"]=seal(transport_policy,"transport_policy_seal")

request_budget={
    "schema":"B_FIQ_02_REQUEST_BUDGET_V0_1",
    "request_budget_id":"BFIQ02-USATECH-REQUEST-BUDGET-V0_1",
    "planned_request_count":request_manifest["required_request_count"],
    "maximum_actual_request_count":request_manifest["required_request_count"],
    "max_parallel_requests":transport_policy["max_parallel_requests"],
    "aggregate_request_start_rate_per_second":transport_policy["aggregate_request_start_rate_per_second"],
    "transport_policy_id":transport_policy["transport_policy_id"],
    "transport_policy_seal":transport_policy["transport_policy_seal"],
    "interval_inventory_root":inventory["interval_inventory_root"],
    "request_manifest_root":request_manifest["request_manifest_root"],
    "regime_manifest_seal":regime_manifest["manifest_seal"],
    "created_at_utc":"2026-09-21T15:00:00Z",
}
request_budget["budget_seal"]=seal(request_budget,"budget_seal")

required_rows=[r for r in rows if r["request_expected"]]
SHARD_REQ=512
shards=[]
for idx in range(0,len(required_rows),SHARD_REQ):
    chunk=required_rows[idx:idx+SHARD_REQ]
    shards.append({
        "shard_id":f"BFIQ02-SHARD-{len(shards):03d}",
        "first_interval_ordinal":chunk[0]["interval_ordinal"],
        "last_interval_ordinal":chunk[-1]["interval_ordinal"],
        "required_request_count":len(chunk),
        "required_interval_ids":[r["interval_id"] for r in chunk],
        "worker_identity_rule":"ONE_GOVERNED_WORKER_PER_SHARD_ID",
    })
shard_plan={
    "schema":"B_FIQ_01_EXECUTION_SHARD_PLAN_V0_1",
    "shard_plan_id":"BFIQ02-USATECH-SHARD-PLAN-V0_1",
    "interval_inventory_root":inventory["interval_inventory_root"],
    "request_manifest_root":request_manifest["request_manifest_root"],
    "request_budget_id":request_budget["request_budget_id"],
    "request_budget_seal":request_budget["budget_seal"],
    "shards":shards,
    "shard_order_policy":"ASCENDING_SHARD_ID_FOR_ORCHESTRATION_ONLY",
    "cross_shard_overlap_policy":"FORBIDDEN",
    "created_at_utc":"2026-09-21T15:00:00Z",
}
shard_plan["shard_plan_seal"]=seal(shard_plan,"shard_plan_seal")

ia_src=source_identity("src/native_bi5_reference_qualifier_qrm12.py")
ib_src=source_identity("src/native_bi5_independent_qualifier_qrm12.py")
lzma_bin=runtime_binary_identity(_lzma.__file__)
struct_bin=runtime_binary_identity(_struct.__file__)
python_runtime_version=".".join(str(x) for x in sys.version_info[:3])

independence={
    "schema":"B_FIQ_01_DIAGNOSTIC_INDEPENDENCE_MANIFEST_V0_2",
    "manifest_id":"BFIQ02-DIAGNOSTIC-INDEPENDENCE-V0_2",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "raw_input_interface_identity":"EXACT_COMPRESSED_PROVIDER_BODY_SHA256",
    "diagnostic_A":{
        "implementation_id":"I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_QRM12",
        "source_identity":ia_src,
        "decompressor_identity":"CPYTHON_STDLIB_LZMA_EXTENSION",
        "decompressor_version":python_runtime_version,
        "decompressor_binary_or_source_sha256":lzma_bin["sha256_raw_bytes"],
        "parser_identity":"I_A_PRIVATE_BINARY_DECODER",
        "parser_source_blob_sha256":ia_src["sha256_raw_bytes"],
        "projection_identity":"I_A_PRIVATE_SEMANTIC_PROJECTION",
        "projection_source_blob_sha256":ia_src["sha256_raw_bytes"],
        "invariant_evaluator_identity":"I_A_PRIVATE_QUALIFICATION_LOGIC",
        "invariant_evaluator_source_blob_sha256":ia_src["sha256_raw_bytes"],
    },
    "diagnostic_B":{
        "implementation_id":"I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_QRM12",
        "source_identity":ib_src,
        "decompressor_identity":"CPYTHON_STDLIB_LZMA_EXTENSION",
        "decompressor_version":python_runtime_version,
        "decompressor_binary_or_source_sha256":lzma_bin["sha256_raw_bytes"],
        "parser_identity":"I_B_PRIVATE_BINARY_DECODER",
        "parser_source_blob_sha256":ib_src["sha256_raw_bytes"],
        "projection_identity":"I_B_PRIVATE_SEMANTIC_PROJECTION",
        "projection_source_blob_sha256":ib_src["sha256_raw_bytes"],
        "invariant_evaluator_identity":"I_B_PRIVATE_QUALIFICATION_LOGIC",
        "invariant_evaluator_source_blob_sha256":ib_src["sha256_raw_bytes"],
    },
    "shared_generic_runtime_primitives":{
        "python_runtime_version":python_runtime_version,
        "lzma_extension":lzma_bin,
        "struct_extension":struct_bin,
        "shared_stage_rule":"DECOMPRESSION_PRIMITIVE_SHARED_GENERIC_NON_PROJECT_SEMANTIC_EXCEPTION",
        "execution_runtime_match_required":True,
    },
    "allowed_shared_artifacts":[
        {
            "artifact_identity":"exact_raw_body_bytes",
            "artifact_hash":None,
            "justification":"common immutable input",
            "source_semantic_adjudication_id_or_null":None,
        },
        {
            "artifact_identity":"qualified normative contracts",
            "artifact_hash":None,
            "justification":"shared authority, not shared implementation",
            "source_semantic_adjudication_id_or_null":"QRM12_QUALIFIED_INDEPENDENCE_BOUNDARY",
        },
        {
            "artifact_identity":"CPython stdlib lzma/_lzma generic primitive",
            "artifact_hash":lzma_bin["sha256_raw_bytes"],
            "justification":"shared generic non-project semantic primitive already tolerated by qualified Q-RM-12 I_B independence boundary; decompression-stage independence is explicitly not claimed",
            "source_semantic_adjudication_id_or_null":"QRM12_IB_V0_2_INDEPENDENT_COMPATIBILITY_PASS",
        },
        {
            "artifact_identity":"CPython stdlib struct/_struct generic primitive",
            "artifact_hash":struct_bin["sha256_raw_bytes"],
            "justification":"shared generic binary primitive; project parser/projection/invariant code lineages remain distinct",
            "source_semantic_adjudication_id_or_null":"QRM12_IB_V0_2_INDEPENDENT_COMPATIBILITY_PASS",
        },
    ],
    "forbidden_shared_semantic_helpers":[
        "shared project parser helper","shared project projection helper","shared project invariant evaluator",
        "I_A output as I_B input","O-normalized expected answer as pre-seal input"
    ],
    "relationship_analysis":{
        "ia_final_rebreak_report_blob":IA_REPORT_BLOB,
        "ib_final_rebreak_report_blob":IB_REPORT_BLOB,
        "ib_semantic_source_provenance_blob":"f78025f5e8ad9bf9a66f8ceef3995eddecdc0cf3",
        "ib_no_copy_declaration_blob":"b62df24e695c925ab440b826b5100c84e9072468",
        "ib_independent_stage_test_inventory_blob":"b822f48bbdca3c9580374a7170b493f7f684e1b0",
        "shared_decompression_exception_authority":"qualified Q-RM-12 I_B independence boundary permits generic non-semantic standard-library primitives; B-FIQ decompression stage is excluded from independent-stage claim and runtime primitive identity is exact-pinned",
        "ib_qualified_properties":[
            "independent raw-payload decoding and anomaly/membership derivation",
            "independent path-private F construction and validation",
            "no pre-seal dependency on I_A/shared F/O/handoff",
        ],
    },
    "stage_independence_verdicts":{
        "decompression":"SHARED_GENERIC_PRIMITIVE_EXEMPTED_NOT_CLAIMED_INDEPENDENT",
        "physical_framing":"PASS_DISTINCT_PROJECT_IMPLEMENTATION_LINEAGE",
        "primitive_parsing":"PASS_DISTINCT_PROJECT_IMPLEMENTATION_LINEAGE",
        "semantic_projection":"PASS_DISTINCT_PROJECT_IMPLEMENTATION_LINEAGE",
        "decisive_invariant_evaluation":"PASS_DISTINCT_PROJECT_IMPLEMENTATION_LINEAGE_BUT_SEMANTIC_AUTHORITY_CURRENTLY_BLOCKED",
    },
    "overall_independence_verdict":"PASS",
    "created_at_utc":"2026-09-21T15:25:00Z",
}
independence["manifest_seal"]=seal(independence,"manifest_seal")

bpe02=json.loads(BPE02_PATH.read_text(encoding="utf-8"))
adj=bpe02["adjudication"]
dims=[d for d in adj["dimension_adjudications"] if d["dimension_id"].startswith(tuple(f"C0{i}" for i in range(1,8)))]
blocked=[{"dimension_id":d["dimension_id"],"status":d["status"],"reason_codes":d.get("reason_codes",[])} for d in dims if d["status"]!="PASS"]
semantic_manifest={
    "schema":"B_FIQ_02_SEMANTIC_INVARIANT_MANIFEST_V0_1",
    "manifest_id":"BFIQ02-SEMANTIC-INVARIANTS-V0_1",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "provider_semantic_adjudication_id":adj["adjudication_id"],
    "provider_semantic_adjudication_seal":adj["adjudication_seal"],
    "provider_semantic_evidence_set_digest":adj["evidence_set_digest"],
    "applicable_claim_scope":["C01","C02","C03","C04","C05","C06","C07"],
    "dimension_statuses":blocked,
    "decisive_invariants":[],
    "candidate_non_decisive_checks":[
        "decompression succeeds under candidate LZMA-Alone premise",
        "decompressed byte length divisible by candidate 20-byte framing",
        "candidate timestamp offset in [0,3600000)",
        "candidate ask/bid raw values nonzero",
        "candidate ask_raw >= bid_raw",
        "candidate volumes finite",
    ],
    "overall_semantic_authority_status":"BLOCKED",
    "execution_eligibility":"BLOCKED",
    "reason_codes":["C01_C07_CURRENT_AUTHORITY_NOT_PASS","DECISIVE_INVARIANTS_CANNOT_BE_AUTHORIZED"],
    "created_at_utc":"2026-09-21T15:00:00Z",
}
semantic_manifest["manifest_seal"]=seal(semantic_manifest,"manifest_seal")

durable={
    "schema":"B_FIQ_01_DURABLE_EVIDENCE_POLICY_V0_2",
    "policy_id":"BFIQ02-DURABLE-EVIDENCE-V0_2",
    "policy_version":"V0_2",
    "allowed_storage_classes":[
        "GITHUB_RELEASE_ASSET_ID_PLUS_SHA256_MUTATION_DETECTABLE"
    ],
    "intrinsic_immutability_guarantee":False,
    "content_addressing_rule":"LOGICAL_CONTENT_IDENTITY_IS_SHA256_EXACT_BODY_BYTES; physical release asset is only a retrieval locator",
    "immutable_versioning_rule":"NO_INTRINSIC_IMMUTABILITY_CLAIM; authoritative evidence identity is release_id + asset_id + exact SHA256 + byte_length; any deletion/replacement/mismatch is integrity failure",
    "retention_requirement":"retain through all dependent qualification/backtest audit lifetimes; deletion or inaccessibility opens CAPTURE_INTEGRITY_FAILURE",
    "retrieval_verification_method":"download exact asset bytes by persisted release_id/asset_id and require byte_length + SHA256 equality",
    "repository_binding_requirement":"repository persists release_id, asset_id, asset_name, byte_length, sha256, upload timestamp and evidence-object seal",
    "asset_naming_rule":"sha256-{digest}.bi5",
    "access_control_requirement":"governed repository credentials; no body authority from inaccessible object",
    "audit_recovery_requirement":"every PASS-bound body must remain retrievable and rehashable",
    "object_reference_encoding_rule":"github-release://{repository}/release/{release_id}/asset/{asset_id}/{asset_name}#sha256={digest}",
    "credential_non_persistence_rule":"never persist tokens, signed authorization headers or secret query parameters",
    "body_persistence_deadline_rule":"before QualificationExecutionResult may close PASS-candidate",
    "temporary_staging_policy":"GitHub Actions artifacts are temporary staging only and have zero final authority",
    "failure_if_persistence_deadline_missed":"BLOCKED_INTEGRITY",
    "created_at_utc":"2026-09-21T15:25:00Z",
}
durable["policy_seal"]=seal(durable,"policy_seal")

scope={
    "schema":"B_FIQ_02_PROVISIONAL_AUTHORITY_SCOPE_TUPLE_V0_1",
    "status":"PROVISIONAL_PRE_EXECUTION_BLOCKED",
    "provider_identity":"DUKASCOPY",
    "instrument_identity":INSTRUMENT,
    "representation_rule_identity":"K1_LEGACY_HOURLY_TICK_BI5",
    "full_d_representation_domain_identity":{
        "first_h1":inventory["full_domain_first_h1"],
        "last_h1":inventory["full_domain_last_h1"],
        "interval_inventory_root":inventory["interval_inventory_root"],
    },
    "execution_window_freeze_identity":FREEZE_BLOB,
    "warmup_rule_identity":inventory["warmup_rule_identity"],
    "session_calendar_identity":{"contract":CALENDAR_CONTRACT,"git_blob":CALENDAR_BLOB},
    "interval_inventory_root":inventory["interval_inventory_root"],
    "provider_delivery_identity_policy_id":provider_policy["policy_id"],
    "provider_delivery_identity_policy_seal":provider_policy["policy_seal"],
    "locator_regime_manifest_id":regime_manifest["manifest_id"],
    "locator_regime_manifest_seal":regime_manifest["manifest_seal"],
    "request_manifest_id":request_manifest["request_manifest_id"],
    "request_manifest_root":request_manifest["request_manifest_root"],
    "request_manifest_seal":request_manifest["request_manifest_seal"],
    "transport_policy_id":transport_policy["transport_policy_id"],
    "transport_policy_seal":transport_policy["transport_policy_seal"],
    "request_budget_id":request_budget["request_budget_id"],
    "request_budget_seal":request_budget["budget_seal"],
    "execution_shard_plan_id":shard_plan["shard_plan_id"],
    "execution_shard_plan_seal":shard_plan["shard_plan_seal"],
    "diagnostic_independence_manifest_id":independence["manifest_id"],
    "diagnostic_independence_manifest_seal":independence["manifest_seal"],
    "semantic_invariant_manifest_id":semantic_manifest["manifest_id"],
    "semantic_invariant_manifest_seal":semantic_manifest["manifest_seal"],
    "applicable_C01_C07_adjudications":[{
        "adjudication_id":adj["adjudication_id"],
        "adjudication_seal":adj["adjudication_seal"],
        "current_authority_required":True,
        "current_authority_status":"BLOCKED",
    }],
    "qualified_empty_rule_id":None,
    "qualified_empty_rule_seal":None,
    "durable_evidence_policy_id":durable["policy_id"],
    "durable_evidence_policy_seal":durable["policy_seal"],
    "qualification_execution_result_id":None,
    "qualification_execution_result_seal":None,
    "evidence_set_digest":None,
    "qualification_capture_set_root_sha256":None,
    "successor_contract_id":"BPE-C08-OP-V0.2",
    "successor_contract_version":"B_PE_01R_OPERATIONAL_EMPIRICAL_SUPERSESSION_V0_2_CORRECTED",
    "pre_execution_eligibility":"BLOCKED",
    "blocking_reason_codes":["C01_C07_CURRENT_AUTHORITY_NOT_PASS","QUALIFIED_EMPTY_RULE_ABSENT_IF_ANY_OPEN_OBJECT_IS_NONQUALIFIABLE"],
    "authority_scope_tuple_digest_domain":{
        "canonicalization":"STRICT_SORTED_JSON_UTF8",
        "excluded_fields":["authority_scope_tuple_digest","scope_seal"],
    },
}
scope_digest_payload=dict(scope)
scope_digest_payload.pop("authority_scope_tuple_digest",None)
scope_digest_payload.pop("scope_seal",None)
scope["authority_scope_tuple_digest"]=sha(scope_digest_payload)
scope["scope_seal"]=seal(scope,"scope_seal")

OUT.mkdir(parents=True, exist_ok=True)
identities={}
for name,obj in [
    ("interval_inventory_v0_1.json",inventory),
    ("provider_delivery_identity_policy_v0_1.json",provider_policy),
    ("representation_regime_manifest_v0_1.json",regime_manifest),
    ("request_manifest_v0_1.json",request_manifest),
    ("transport_policy_v0_1.json",transport_policy),
    ("request_budget_v0_1.json",request_budget),
    ("execution_shard_plan_v0_1.json",shard_plan),
    ("diagnostic_independence_manifest_v0_1.json",independence),
    ("semantic_invariant_manifest_v0_1.json",semantic_manifest),
    ("durable_evidence_policy_v0_1.json",durable),
    ("provisional_authority_scope_tuple_v0_1.json",scope),
]:
    identities[name]=write_json(name,obj)

package={
    "schema":"B_FIQ_02_PREEXECUTION_PACKAGE_V0_2",
    "package_id":"BFIQ02-USATECH-PREEXECUTION-PACKAGE-V0_2",
    "contract_id":CONTRACT_ID,
    "contract_version":CONTRACT_VERSION,
    "artifacts":identities,
    "interval_inventory_root":inventory["interval_inventory_root"],
    "request_manifest_root":request_manifest["request_manifest_root"],
    "planned_request_count":request_manifest["required_request_count"],
    "shard_count":len(shards),
    "diagnostic_independence_status":independence["overall_independence_verdict"],
    "semantic_authority_status":semantic_manifest["overall_semantic_authority_status"],
    "pre_execution_eligibility":"BLOCKED",
    "blocking_reason_codes":["C01_C07_CURRENT_AUTHORITY_NOT_PASS"],
    "provider_network_requests_performed":False,
    "created_at_utc":"2026-09-21T15:25:00Z",
}
package["package_seal"]=seal(package,"package_seal")
identities["preexecution_package_v0_1.json"]=write_json("preexecution_package_v0_1.json",package)

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text(f"""# B-FIQ-02 — PRE-EXECUTION PACKAGE — MATERIALIZED CANDIDATE

Date: 2026-09-21

No provider request was performed.

## Domain

- full first H1: {inventory['full_domain_first_h1']}
- frozen last H1: {inventory['full_domain_last_h1']}
- wall-clock intervals: {inventory['wall_clock_interval_count']}
- expected-open intervals: {inventory['expected_open_interval_count']}
- expected-closed intervals: {inventory['expected_closed_interval_count']}
- warmup open intervals: {inventory['warmup_open_interval_count']}
- evaluation open intervals: {inventory['evaluation_open_interval_count']}

IntervalInventory root:

\`{inventory['interval_inventory_root']}\`

## Request package

Required requests:

\`{request_manifest['required_request_count']}\`

RequestManifest root:

\`{request_manifest['request_manifest_root']}\`

Shard count:

\`{len(shards)}\`

Transport:

\`curl / IPv4 / HTTPS / HTTP1.1 / retry=0 / max_parallel=4 / <=2 starts/sec\`

## Diagnostic independence

\`{independence['overall_independence_verdict']}\`

Bound implementations:

- I_A blob {ia_src['git_blob_sha1']}
- I_B blob {ib_src['git_blob_sha1']}

## Semantic authority

\`{semantic_manifest['overall_semantic_authority_status']}\`

The current B-PE-02 provider-semantic adjudication still has non-PASS C01-C07 dimensions.

Therefore decisive representation invariants cannot be authorized for an exhaustive execution.

## Candidate package state

\`\`\`text
B-FIQ-02 MATERIALIZATION = COMPLETE CANDIDATE
PRE-EXECUTION ELIGIBILITY = BLOCKED
reason = C01_C07_CURRENT_AUTHORITY_NOT_PASS
\`\`\`

No GET BI5, FULL_INTERVAL execution, D materialization or backtest occurred.
""", encoding="utf-8")

print(json.dumps({
    "full_domain_first_h1":inventory["full_domain_first_h1"],
    "full_domain_last_h1":inventory["full_domain_last_h1"],
    "wall_clock_interval_count":inventory["wall_clock_interval_count"],
    "expected_open_interval_count":inventory["expected_open_interval_count"],
    "expected_closed_interval_count":inventory["expected_closed_interval_count"],
    "planned_request_count":request_manifest["required_request_count"],
    "shard_count":len(shards),
    "interval_inventory_root":inventory["interval_inventory_root"],
    "request_manifest_root":request_manifest["request_manifest_root"],
    "diagnostic_independence_status":independence["overall_independence_verdict"],
    "semantic_authority_status":semantic_manifest["overall_semantic_authority_status"],
    "pre_execution_eligibility":"BLOCKED",
}, sort_keys=True))
