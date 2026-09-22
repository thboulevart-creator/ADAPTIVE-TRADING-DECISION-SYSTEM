#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"evidence"/"bpesem05"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05_lane_s_candidate_2026-09-22.md"

CONTRACT_PATH="evidence/bpesem04/prospective_semantic_authority_closure_contract_v0_1.json"
CONTRACT_BLOB="fe0ca12e12624371be28ea8c09340691466a37ce"
QUAL_PATH="evidence/bpesem04/contract_qualification_v0_1.json"
QUAL_BLOB="680194efc3968c2c44c36dd731762d70ef270f55"
ROUTE_PATH="reports/data-qualification/post_bpesem04_qualified_contract_consumer_route_selection_2026-09-22.md"
ROUTE_BLOB="a37f84337c45387ff363b9c7bf8f17cb2d98b0fb"
BPE02_PATH="evidence/bpe02/native_bi5_provider_reference_evidence_bundle_v0_1.json"
BPE02_BLOB="df22332709377591d73571a4940c1fda39565867"
BPE03_PATH="evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json"
BPE03_BLOB="f934df8ea93018ee0c22b2d69575f15fc8f2c72f"

TARGET_START="2021-08-13T01:00:00Z"
TARGET_END="2026-08-14T20:00:00Z"

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def sha(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None); return sha(x)
def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def blob(path:str)->str:
    return git("hash-object",path)
def readj(path:str)->dict:
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def writej(name:str,obj:dict):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")
for p,b in [(CONTRACT_PATH,CONTRACT_BLOB),(QUAL_PATH,QUAL_BLOB),(ROUTE_PATH,ROUTE_BLOB),(BPE02_PATH,BPE02_BLOB),(BPE03_PATH,BPE03_BLOB)]:
    if blob(p)!=b: raise RuntimeError("governed input blob mismatch: "+p)

contract=readj(CONTRACT_PATH)
qual=readj(QUAL_PATH)
bpe02=readj(BPE02_PATH)
bpe03=readj(BPE03_PATH)
if qual["qualification_status"]!="PASS": raise RuntimeError("B-PE-SEM-04 contract not qualified")
slots=contract["lane_s"]["evidence_slots"]
slot_ids=[x["evidence_slot_id"] for x in slots]
expected_slots=[
"BPESEM04-S-E01-PROVIDER-FORMAT-SEMANTICS",
"BPESEM04-S-E02-PROVIDER-INSTRUMENT-SCALE",
"BPESEM04-S-E03-PROVIDER-EPOCH-CONTINUITY",
"BPESEM04-S-E04-INDEPENDENT-CORROBORATION-A",
"BPESEM04-S-E05-INDEPENDENT-CORROBORATION-B",
"BPESEM04-S-E06-CONTRADICTION-SWEEP"]
if slot_ids!=expected_slots: raise RuntimeError("Lane S slot drift")

# Documentary observations acquired under B-PE-SEM-05. No provider-object/tick bytes.
observations=[
{
 "evidence_id":"BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT",
 "publisher_identity":"Dukascopy Bank SA",
 "source_class":"PROVIDER_AUTHORED_LIVE_DOCUMENTATION",
 "locator":"https://www.dukascopy.com/wiki/en/development/data-export/",
 "retrieved_at_utc":"2026-09-22T15:20:00Z",
 "raw_provider_bytes_sha256":None,
 "immutable_version_identity":None,
 "immutability_status":"LIVE_OBSERVATION_NO_RAW_IMMUTABLE_PROVIDER_SNAPSHOT",
 "claims":[
   "Current documented BI5 tick file is one full day per file.",
   "Current documented tick record is fixed 20 bytes, big-endian: uint32 time, uint32 ask, uint32 bid, float32 ask volume, float32 bid volume.",
   "Current documented time field is milliseconds since start of day UTC.",
   "Provider warns that older legacy hourly files may use milliseconds since start of hour instead.",
   "Provider states index/commodity price scaling varies by instrument and should be verified per instrument."
 ],
 "target_role":"PRIMARY_SEMANTIC_AUTHORITY_CANDIDATE",
 "scope_relation":"CURRENT_DAILY_BI5_PLUS_LEGACY_HOURLY_WARNING; NOT_EXACT_TARGET_K1_CONTINUITY",
 "admissibility":"BLOCKED_FOR_PRIMARY_AUTHORITY",
 "reason_codes":["LIVE_SOURCE_NOT_IMMUTABLY_SNAPSHOTTED","CURRENT_DAILY_SCOPE_NE_TARGET_LEGACY_HOURLY_K1","LEGACY_HOURLY_WORDING_NONEXACT_MAY_USE_HOUR_BASE"]
},
{
 "evidence_id":"BPESEM05-E02-DUKASCOPY-USATECH-CFD-CURRENT",
 "publisher_identity":"Dukascopy Bank SA",
 "source_class":"PROVIDER_AUTHORED_LIVE_INSTRUMENT_PAGE",
 "locator":"https://www.dukascopy.com/europe/french/cfd/range-of-markets/",
 "retrieved_at_utc":"2026-09-22T15:20:00Z",
 "raw_provider_bytes_sha256":None,
 "immutable_version_identity":None,
 "immutability_status":"LIVE_OBSERVATION_NO_RAW_IMMUTABLE_PROVIDER_SNAPSHOT",
 "claims":[
   "USATECH.IDX/USD is listed by provider as US 100 Tech Index.",
   "Current CFD market table quotes point value 0.01 USD."
 ],
 "target_role":"PRIMARY_SCALE_AND_INSTRUMENT_AUTHORITY_CANDIDATE",
 "scope_relation":"CURRENT_MARKET_METADATA_ONLY; DOES_NOT_BIND_NATIVE_BI5_RAW_INTEGER_DIVISOR",
 "admissibility":"BLOCKED_FOR_RAW_SCALE_AUTHORITY",
 "reason_codes":["LIVE_SOURCE_NOT_IMMUTABLY_SNAPSHOTTED","CFD_MARKET_POINT_VALUE_NE_NATIVE_BI5_RAW_DIVISOR_AUTHORITY"]
},
{
 "evidence_id":"BPESEM05-E03-DUKASCOPY-ITICK-CURRENT",
 "publisher_identity":"Dukascopy Bank SA",
 "source_class":"PROVIDER_AUTHORED_LIVE_JAVADOC",
 "locator":"https://www.dukascopy.com/client/javadoc3/com/dukascopy/api/ITick.html",
 "retrieved_at_utc":"2026-09-22T15:20:00Z",
 "raw_provider_bytes_sha256":None,
 "immutable_version_identity":"JAVADOC3_CURRENT_COPYRIGHT_2025_OBSERVED",
 "immutability_status":"LIVE_OBSERVATION_WITHOUT_EXACT_ARTIFACT_HASH",
 "claims":["ITick exposes best ask, best bid, ask volume and bid volume semantic roles."],
 "target_role":"LOGICAL_TICK_SEMANTIC_CORROBORATION",
 "scope_relation":"API_LOGICAL_TICK_SEMANTICS; NOT_NATIVE_BI5_FIELD_BINDING",
 "admissibility":"CORROBORATION_ONLY",
 "reason_codes":["NO_EXACT_JAVADOC_ARTIFACT_HASH","LOGICAL_API_NE_NATIVE_WIRE_BINDING"]
},
# Reuse exact governed provider evidence.
{
 "evidence_id":"BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE",
 "publisher_identity":"Dukascopy Bank SA",
 "source_class":"PROVIDER_AUTHORED_VERSIONED_CHANGE_HISTORY",
 "locator":"https://www.dukascopy.com/client/jforexlib/publicrepo/com/dukascopy/dds2/DDS2-jClient-JForex/",
 "immutable_version_identity":"VERSIONED_PROVIDER_MAVEN_INDEX_CAPTURE",
 "content_integrity_digest":"ff2547ca714a34a8c30780ee4dcf345451f1fa211c225326391e69445576abc4",
 "immutability_status":"GOVERNED_EXISTING_VERSIONED_PROVIDER_EVIDENCE",
 "claims":["Provider client release timeline spans multiple versions across target-era years."],
 "target_role":"EPOCH_CHANGE_HISTORY_CONTEXT",
 "scope_relation":"CLIENT_RELEASE_TIMELINE_NOT_EXHAUSTIVE_K1_WIRE_SEMANTIC_CHANGELOG",
 "admissibility":"ADMISSIBLE_CONTEXT_ONLY",
 "reason_codes":["VERSIONED_PROVIDER_SOURCE","NO_EXACT_K1_SEMANTIC_CONTINUITY_STATEMENT"]
},
{
 "evidence_id":"BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE",
 "publisher_identity":"Dukascopy Bank SA",
 "source_class":"PROVIDER_AUTHORED_VERSIONED_CHANGE_HISTORY",
 "locator":"https://www.dukascopy.com/wiki/en/manuals/jforex4-desktop/release-notes/",
 "immutable_version_identity":"JFOREX_4.8.0",
 "publication_time":"2026-03-03T00:00:00Z",
 "content_integrity_digest":"aaa26415a11f8582b0897ca5c051cfda0cbab4933618cf03880681a79b69be8e",
 "immutability_status":"GOVERNED_EXISTING_VERSIONED_PROVIDER_EVIDENCE",
 "claims":["JForex 4.8.0 release notes include historical price data retrieval from JETTA."],
 "target_role":"MATERIAL_CHANGE_POINT_CANDIDATE",
 "scope_relation":"HISTORICAL_DATA_BACKEND_CHANGE; NO_PROOF_OF_NATIVE_BI5_WIRE_CHANGE_OR_NONCHANGE",
 "admissibility":"ADMISSIBLE_CHANGE_POINT_CONTEXT",
 "reason_codes":["VERSIONED_PROVIDER_RELEASE_NOTE","SEMANTIC_EFFECT_ON_K1_UNRESOLVED"]
},
{
 "evidence_id":"BPE03-E01-DUKASCOPY-API-SUPPORT-2013",
 "publisher_identity":"Dukascopy Bank SA / API Support",
 "source_class":"PROVIDER_AUTHORED_DATED_SUPPORT",
 "locator":"https://www.dukascopy.com/swiss/english/forex/jforex/forum/viewtopic.php?f=65&t=50326",
 "immutable_version_identity":"DATED_PROVIDER_SUPPORT_POST_2013-11-07",
 "publication_time":"2013-11-07T14:08:00Z",
 "content_integrity_digest":"ac92a240fd3f961269dbaf3b7375c14213fb2a2b544358aff486dea90016edc7",
 "immutability_status":"GOVERNED_EXISTING_DATED_PROVIDER_EVIDENCE",
 "claims":["Provider historical service used legacy hourly tick file family."],
 "target_role":"HISTORICAL_LEGACY_HOURLY_EXISTENCE",
 "scope_relation":"PRE_TARGET_HISTORICAL_EXISTENCE_ONLY",
 "admissibility":"ADMISSIBLE_CONTEXT_ONLY",
 "reason_codes":["DATED_PROVIDER_SOURCE","NO_TARGET_EPOCH_CONTINUITY_PROOF"]
},
# Existing independent corroborations.
{
 "evidence_id":"BPE02-E03",
 "publisher_identity":"saleem-latif/duka-data",
 "source_class":"VERSIONED_NONPROJECT_REFERENCE_IMPLEMENTATION_OR_SPEC",
 "locator":"https://github.com/saleem-latif/duka-data/blob/2220708e7d0be9d2b6feaf6efe4d3f89c6bb040c/download.py",
 "immutable_version_identity":"2220708e7d0be9d2b6feaf6efe4d3f89c6bb040c",
 "content_integrity_digest":"42e7ada6a7c841ab2a92387954e30e0dfeb21ddc50b8b31ddef8b9851506a24b",
 "lineage_id":"LINEAGE-DUKA-DATA",
 "immutability_status":"EXACT_GITHUB_COMMIT_AND_FILE_HASH",
 "claims":["Legacy hourly BI5 reference implementation corroborates LZMA/20-byte/big-endian/hour+ms/ask-bid//1000/volume interpretation."],
 "target_role":"CORROBORATION_A_ONLY",
 "admissibility":"ADMISSIBLE_CORROBORATION_ONLY"
},
{
 "evidence_id":"BPE02-E08+BPE02-E10",
 "publisher_identity":"leoclc/dukascopy-tick",
 "source_class":"VERSIONED_NONPROJECT_REFERENCE_IMPLEMENTATION_OR_SPEC",
 "locator":"https://github.com/leoclc/dukascopy-tick/tree/989987db0808e215962e136ce043797992d1a1a2",
 "immutable_version_identity":"989987db0808e215962e136ce043797992d1a1a2",
 "lineage_id":"LINEAGE-LEOCLC",
 "immutability_status":"EXACT_GITHUB_COMMIT_AND_COMPONENT_HASHES",
 "claims":["Independent legacy-hourly normalizer corroborates startTs+ms and ask/bid/askVolume/bidVolume roles; instrument metadata corroborates USATECH decimalFactor 1000."],
 "target_role":"CORROBORATION_B_ONLY",
 "admissibility":"ADMISSIBLE_CORROBORATION_ONLY"
},
{
 "evidence_id":"BPESEM05-E09-HISTORICAL-MARKET-DATA-USATECH",
 "publisher_identity":"theninthsky/historical-market-data",
 "source_class":"VERSIONED_NONPROJECT_REFERENCE_IMPLEMENTATION_OR_SPEC",
 "locator":"https://github.com/theninthsky/historical-market-data/blob/be4db659bda379b8c3d78fc7ef225e3566925376/src/instruments.js",
 "immutable_version_identity":"be4db659bda379b8c3d78fc7ef225e3566925376",
 "git_blob":"2ba6f322346f0dd9110646a673f6f3c4b23db756",
 "lineage_id":"LINEAGE-THENINTHSKY-HISTORICAL-MARKET-DATA",
 "immutability_status":"EXACT_GITHUB_COMMIT_AND_BLOB",
 "claims":["USATECH.IDX/USD metadata sets decimalFactor 1000."],
 "target_role":"ADDITIONAL_SCALE_CORROBORATION_ONLY",
 "admissibility":"ADMISSIBLE_CORROBORATION_ONLY"
}]

lineage={
 "schema":"BPESEM05_SOURCE_LINEAGE_RESOLUTION_V0_1",
 "contract_seal":contract["contract_seal"],
 "lineages":[
   {"lineage_id":"LINEAGE-DUKASCOPY-OFFICIAL","members":["BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT","BPESEM05-E02-DUKASCOPY-USATECH-CFD-CURRENT","BPESEM05-E03-DUKASCOPY-ITICK-CURRENT","BPE03-E01-DUKASCOPY-API-SUPPORT-2013","BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE","BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE"],"independence_role":"ONE_PROVIDER_LINEAGE"},
   {"lineage_id":"LINEAGE-DUKA-DATA","members":["BPE02-E03"],"independence_role":"NONPROJECT_CORROBORATION_A"},
   {"lineage_id":"LINEAGE-LEOCLC","members":["BPE02-E08+BPE02-E10"],"independence_role":"NONPROJECT_CORROBORATION_B"},
   {"lineage_id":"LINEAGE-THENINTHSKY-HISTORICAL-MARKET-DATA","members":["BPESEM05-E09-HISTORICAL-MARKET-DATA-USATECH"],"independence_role":"ADDITIONAL_NONPROJECT_CORROBORATION"}
 ],
 "project_origin_used_as_independent_authority":False,
 "duplicate_provider_pages_count_as_multiple_independent_sources":False,
 "unresolved_lineage_ids":[],
}
lineage["lineage_resolution_seal"]=seal(lineage,"lineage_resolution_seal")

registry={
 "schema":"BPESEM05_LANE_S_EVIDENCE_REGISTRY_V0_1",
 "contract_id":contract["contract_id"],
 "contract_seal":contract["contract_seal"],
 "candidate_parent_head":HEAD,
 "slot_population":expected_slots,
 "observations":observations,
 "no_provider_object_bytes_observed":True,
 "no_bi5_get_performed":True,
}
registry["registry_seal"]=seal(registry,"registry_seal")

slot_results=[
 {"slot_id":expected_slots[0],"status":"BLOCKED","evidence_ids":["BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT","BPESEM05-E03-DUKASCOPY-ITICK-CURRENT","BPE03-E01-DUKASCOPY-API-SUPPORT-2013"],"reason_codes":["CURRENT_PROVIDER_FORMAT_DOC_IS_DAILY_NOT_EXACT_TARGET_K1","LIVE_CURRENT_PROVIDER_DOC_NOT_DURABLY_IMMUTABLE","LEGACY_HOURLY_WARNING_NONEXACT","NO_PROVIDER_PRIMARY_EXACT_TARGET_K1_SEMANTIC_BINDING"]},
 {"slot_id":expected_slots[1],"status":"BLOCKED","evidence_ids":["BPESEM05-E02-DUKASCOPY-USATECH-CFD-CURRENT","BPE02-E08+BPE02-E10","BPESEM05-E09-HISTORICAL-MARKET-DATA-USATECH"],"reason_codes":["CURRENT_PROVIDER_INSTRUMENT_IDENTITY_OBSERVED","PROVIDER_CFD_POINT_VALUE_NE_NATIVE_BI5_RAW_DIVISOR_AUTHORITY","NO_IMMUTABLE_PROVIDER_PRIMARY_RAW_SCALE_AUTHORITY","THIRD_PARTY_DECIMAL_FACTOR_1000_CORROBORATION_ONLY"]},
 {"slot_id":expected_slots[2],"status":"BLOCKED","evidence_ids":["BPE03-E01-DUKASCOPY-API-SUPPORT-2013","BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE","BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE","BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT"],"reason_codes":["TARGET_EPOCH_CHANGE_HISTORY_NOT_EXHAUSTIVE","LEGACY_HOURLY_TO_CURRENT_DAILY_TRANSITION_DATE_UNRESOLVED","JETTA_2026_CHANGE_POINT_SEMANTIC_EFFECT_UNRESOLVED","FULL_2021_2026_CONTINUITY_NOT_ESTABLISHED"]},
 {"slot_id":expected_slots[3],"status":"FILLED_CORROBORATION_ONLY","evidence_ids":["BPE02-E03"],"reason_codes":["EXACT_VERSIONED_NONPROJECT_LINEAGE","NOT_PROVIDER_PRIMARY_AUTHORITY"]},
 {"slot_id":expected_slots[4],"status":"FILLED_CORROBORATION_ONLY","evidence_ids":["BPE02-E08+BPE02-E10"],"reason_codes":["EXACT_VERSIONED_NONPROJECT_LINEAGE","INDEPENDENT_FROM_DUKA_DATA","NOT_PROVIDER_PRIMARY_AUTHORITY"]},
 {"slot_id":expected_slots[5],"status":"PASS_AS_CONTROL_WITH_BLOCKING_FINDINGS","evidence_ids":[x["evidence_id"] for x in observations],"reason_codes":["MATERIAL_SOURCES_REVIEWED","CURRENT_DAILY_VS_LEGACY_HOURLY_SCOPE_DIFFERENCE_FOUND","RAW_SCALE_PRIMARY_AUTHORITY_ABSENT","TARGET_EPOCH_CONTINUITY_UNRESOLVED","NO_POSITIVE_CONTRADICTION_ESTABLISHING_REGISTERED_TARGET_PROPOSITION_FALSE"]}
]

anchors={
 "schema":"BPESEM05_PROVIDER_PRIMARY_SEMANTIC_ANCHOR_SET_V0_1",
 "target_scope":{"provider":"DUKASCOPY","instrument":"USATECHIDXUSD","representation":"K1_LEGACY_HOURLY_TICK_BI5","start":TARGET_START,"end":TARGET_END},
 "candidate_anchors":[
   {"evidence_id":"BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT","status":"REJECTED_AS_TARGET_PRIMARY","reason":"CURRENT_DAILY_FORMAT_WITH_ONLY_NONEXACT_LEGACY_WARNING"},
   {"evidence_id":"BPESEM05-E03-DUKASCOPY-ITICK-CURRENT","status":"CORROBORATION_ONLY","reason":"LOGICAL_API_SEMANTICS_NOT_NATIVE_WIRE_BINDING"},
 ],
 "qualified_target_primary_anchor_ids":[],
 "overall_status":"BLOCKED",
 "reason_codes":["NO_EXACT_IMMUTABLE_PROVIDER_PRIMARY_ANCHOR_FOR_LEGACY_HOURLY_K1_ACROSS_TARGET_EPOCH"]
}
anchors["anchor_set_seal"]=seal(anchors,"anchor_set_seal")

scale={
 "schema":"BPESEM05_PROVIDER_INSTRUMENT_SCALE_AUTHORITY_V0_1",
 "instrument":"USATECHIDXUSD",
 "provider_current_identity_observation":"USATECH.IDX/USD / US 100 Tech Index",
 "provider_current_market_point_value_observation":"0.01 USD",
 "provider_native_bi5_raw_divisor_authority":None,
 "third_party_corroborated_decimal_factor":1000,
 "third_party_evidence":["BPE02-E08+BPE02-E10","BPESEM05-E09-HISTORICAL-MARKET-DATA-USATECH"],
 "noncircularity_check":"PASS",
 "forbidden_inference_applied":"0.01_USD_MARKET_POINT_VALUE_NOT_CONVERTED_INTO_RAW_BI5_DIVISOR",
 "overall_status":"BLOCKED",
 "reason_codes":["NO_IMMUTABLE_PROVIDER_PRIMARY_NATIVE_BI5_RAW_SCALE_AUTHORITY"]
}
scale["scale_authority_seal"]=seal(scale,"scale_authority_seal")

change_points={
 "schema":"BPESEM05_PROVIDER_SEMANTIC_CHANGE_POINT_INVENTORY_V0_1",
 "target_start":TARGET_START,"target_end":TARGET_END,
 "events":[
   {"event_id":"CP-HIST-2013-LEGACY-HOURLY","time":"2013-11-07T14:08:00Z","relation":"BEFORE_TARGET","evidence_id":"BPE03-E01-DUKASCOPY-API-SUPPORT-2013","meaning":"legacy hourly provider file family existed","semantic_effect":"CONTEXT_ONLY"},
   {"event_id":"CP-2026-03-03-JETTA","time":"2026-03-03T00:00:00Z","relation":"INSIDE_TARGET","evidence_id":"BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE","meaning":"historical price data retrieval moved/added to JETTA","semantic_effect":"UNRESOLVED_FOR_NATIVE_K1"},
   {"event_id":"CP-UNKNOWN-LEGACY-HOURLY-TO-DAILY","time":None,"relation":"UNKNOWN_WITH_RESPECT_TO_TARGET","evidence_id":"BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT","meaning":"current provider documentation describes daily files and warns legacy hourly files may use hour-relative time","semantic_effect":"MATERIAL_TRANSITION_EXISTS_OR_MAY_EXIST_BUT_DATE_AND_EXACT_RULES_UNRESOLVED"}
 ],
 "provider_release_timeline_evidence":"BPE03-E02-DUKASCOPY-MAVEN-DDS2-TIMELINE",
 "exhaustive_wire_semantic_changelog_proven":False,
 "overall_status":"BLOCKED",
 "reason_codes":["CHANGE_POINT_COVERAGE_NOT_EXHAUSTIVE","UNKNOWN_LEGACY_HOURLY_TO_DAILY_TRANSITION_BOUNDARY","JETTA_K1_SEMANTIC_EFFECT_UNRESOLVED"]
}
change_points["change_point_inventory_seal"]=seal(change_points,"change_point_inventory_seal")

epoch={
 "schema":"BPESEM05_SEMANTIC_EPOCH_MANIFEST_V0_1",
 "policy_id":contract["lane_s"]["epoch_coverage_policy"]["policy_id"],
 "target_start":TARGET_START,"target_end":TARGET_END,
 "epochs":[
   {"epoch_id":"TARGET-PRE-JETTA","start":TARGET_START,"end":"2026-03-03T00:00:00Z","authority_status":"BLOCKED","reason":"NO_EXACT_PROVIDER_PRIMARY_LEGACY_HOURLY_K1_SEMANTIC_CONTINUITY_PROOF"},
   {"epoch_id":"TARGET-POST-JETTA","start":"2026-03-03T00:00:00Z","end":TARGET_END,"authority_status":"BLOCKED","reason":"JETTA_HISTORICAL_BACKEND_SEMANTIC_EFFECT_ON_TARGET_K1_UNRESOLVED"}
 ],
 "unresolved_change_points":["CP-2026-03-03-JETTA","CP-UNKNOWN-LEGACY-HOURLY-TO-DAILY"],
 "uncovered_authoritative_intervals":[[TARGET_START,TARGET_END]],
 "full_authoritative_coverage":False,
 "overall_status":"BLOCKED_UNRESOLVED_TARGET_EPOCH",
 "request_manifest_derivation_authorized":False
}
epoch["semantic_epoch_manifest_seal"]=seal(epoch,"semantic_epoch_manifest_seal")

corroboration={
 "schema":"BPESEM05_INDEPENDENT_CORROBORATION_REGISTER_V0_1",
 "entries":[
   {"slot_id":expected_slots[3],"lineage_id":"LINEAGE-DUKA-DATA","evidence_ids":["BPE02-E03"],"status":"PASS_CORROBORATION_ONLY"},
   {"slot_id":expected_slots[4],"lineage_id":"LINEAGE-LEOCLC","evidence_ids":["BPE02-E08+BPE02-E10"],"status":"PASS_CORROBORATION_ONLY"},
   {"slot_id":"ADDITIONAL","lineage_id":"LINEAGE-THENINTHSKY-HISTORICAL-MARKET-DATA","evidence_ids":["BPESEM05-E09-HISTORICAL-MARKET-DATA-USATECH"],"status":"PASS_ADDITIONAL_CORROBORATION_ONLY"}
 ],
 "required_pair_independent":True,
 "pair_independence_status":"PASS",
 "provider_primary_substitution_allowed":False
}
corroboration["corroboration_register_seal"]=seal(corroboration,"corroboration_register_seal")

contradiction={
 "schema":"BPESEM05_CONTRADICTION_SWEEP_RESULT_V0_1",
 "reviewed_evidence_ids":[x["evidence_id"] for x in observations],
 "material_findings":[
   {"finding_id":"F01","type":"REGIME_SCOPE_DIFFERENCE","finding":"Current provider documentation is daily-object/day-relative while target is legacy-hourly K1; provider itself warns old hourly files may use hour-relative timestamps.","disposition":"BLOCK_TARGET_SCOPE_PROMOTION"},
   {"finding_id":"F02","type":"SCALE_AUTHORITY_GAP","finding":"Independent sources corroborate decimalFactor 1000, but no immutable provider-primary native BI5 raw divisor authority was obtained.","disposition":"BLOCK_C06_SCALE_AUTHORITY"},
   {"finding_id":"F03","type":"CHANGE_POINT_UNCERTAINTY","finding":"2026-03-03 JETTA historical-data backend change is versioned provider evidence but its K1 wire-semantic effect is unresolved.","disposition":"BLOCK_TARGET_EPOCH_CONTINUITY"},
 ],
 "positive_exact_target_scope_contradictions":[],
 "registered_proposition_failures_established":[],
 "sweep_completeness_status":"PASS_FOR_DISCOVERED_MATERIAL_SOURCES",
 "substantive_authority_status":"BLOCKED",
}
contradiction["contradiction_sweep_seal"]=seal(contradiction,"contradiction_sweep_seal")

scope_decisions=[]
for d in contract["dimension_population"]["blocked_physical_hypothesis"]+contract["dimension_population"]["blocked_semantic_anchor"]+contract["dimension_population"]["blocked_prerequisite_closure"]:
    scope_decisions.append({"dimension_id":d,"status":"BLOCKED","reason_codes":["TARGET_EPOCH_PROVIDER_PRIMARY_SEMANTIC_COVERAGE_INCOMPLETE","UNRESOLVED_SEMANTIC_CHANGE_POINT","NO_FORWARD_OR_BACKWARD_EXTRAPOLATION_ALLOWED"]})
scope_result={
 "schema":"BPESEM05_LANE_S_SCOPE_APPLICABILITY_DECISION_V0_1",
 "target_start":TARGET_START,"target_end":TARGET_END,
 "decisions":scope_decisions,
 "pass_count":0,"blocked_count":len(scope_decisions),"fail_count":0,
 "overall_status":"BLOCKED"
}
scope_result["scope_decision_seal"]=seal(scope_result,"scope_decision_seal")

semantic_dimensions=[]
for d in contract["dimension_population"]["blocked_semantic_anchor"]:
    semantic_dimensions.append({"dimension_id":d,"status":"BLOCKED","reason_codes":["LANE_S_SCOPE_APPLICABILITY_BLOCKED","PROVIDER_PRIMARY_TARGET_K1_AUTHORITY_INSUFFICIENT"]})
# C06-D3 is Lane-C later, but Lane S scale authority prerequisite is blocked.
semantic_result={
 "schema":"BPESEM05_LANE_S_SEMANTIC_AUTHORITY_RESULT_V0_1",
 "slot_results":slot_results,
 "semantic_anchor_dimension_results":semantic_dimensions,
 "c06_d3_lane_s_prerequisite_status":"BLOCKED",
 "existing_pass_dimensions_preserved":contract["dimension_population"]["already_pass"],
 "physical_hypothesis_dimensions_not_adjudicated_here":contract["dimension_population"]["blocked_physical_hypothesis"],
 "lane_s_overall_status":"BLOCKED",
 "registered_target_proposition_failures":[],
 "dimension_promotions_to_pass":[],
 "lane_p_request_manifest_authorized":False,
 "reason_codes":["NO_EXACT_PROVIDER_PRIMARY_LEGACY_HOURLY_K1_AUTHORITY","TARGET_EPOCH_CONTINUITY_UNRESOLVED","NATIVE_USATECH_RAW_SCALE_AUTHORITY_UNRESOLVED"]
}
semantic_result["lane_s_result_seal"]=seal(semantic_result,"lane_s_result_seal")

horizon={
 "schema":"BPESEM05_CURRENT_EVIDENCE_HORIZON_V0_1",
 "cutoff_head":HEAD,
 "governed_inputs":[
   {"path":CONTRACT_PATH,"blob":CONTRACT_BLOB},
   {"path":QUAL_PATH,"blob":QUAL_BLOB},
   {"path":ROUTE_PATH,"blob":ROUTE_BLOB},
   {"path":BPE02_PATH,"blob":BPE02_BLOB},
   {"path":BPE03_PATH,"blob":BPE03_BLOB}
 ],
 "lane_s_evidence_ids":[x["evidence_id"] for x in observations],
 "unresolved_required_authority":[
   "immutable/provider-versioned exact legacy-hourly K1 semantic format authority across target epoch",
   "provider-primary exact native BI5 USATECH raw scale/divisor authority",
   "exhaustive target-epoch semantic change-point/continuity authority"
 ],
 "overall_status":"BLOCKED"
}
horizon["evidence_horizon_seal"]=seal(horizon,"evidence_horizon_seal")

for name,obj in [
("lane_s_evidence_registry_v0_1.json",registry),
("source_lineage_resolution_v0_1.json",lineage),
("provider_primary_semantic_anchor_set_v0_1.json",anchors),
("provider_instrument_scale_authority_v0_1.json",scale),
("provider_semantic_change_point_inventory_v0_1.json",change_points),
("semantic_epoch_manifest_v0_1.json",epoch),
("independent_corroboration_register_v0_1.json",corroboration),
("contradiction_sweep_result_v0_1.json",contradiction),
("lane_s_scope_applicability_decision_v0_1.json",scope_result),
("lane_s_semantic_authority_result_v0_1.json",semantic_result),
("current_evidence_horizon_v0_1.json",horizon),
]: writej(name,obj)

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(
f"""# B-PE-SEM-05 — Lane S candidate

Candidate parent HEAD: {HEAD}

## Result

~~~text
package materialization = COMPLETE
six Lane S slots = REVIEWED
Lane S semantic authority = BLOCKED
target epoch scope = BLOCKED
SemanticEpochManifest = BLOCKED_UNRESOLVED_TARGET_EPOCH
dimension promotions = 0
registered target proposition failures = 0
Lane P RequestManifest authorized = NO
~~~

The block fails closed because current provider documentation describes a daily BI5 regime while only warning non-exactly about older hourly files; the exact legacy-hourly K1 semantic authority and transition/continuity over 2021-08-13 through 2026-08-14 were not established. Current provider USATECH market metadata also does not establish the native BI5 raw integer divisor.

Two independent existing governed non-project lineages fill the two corroboration slots, but corroboration cannot replace provider-primary authority.

No provider BI5 object was requested or observed. No Lane P RequestManifest or diagnostic implementation was created. No FULL_INTERVAL, D, backtest, paper, broker or live execution occurred.
""",encoding="utf-8")

print(json.dumps({
 "candidate_parent_head":HEAD,
 "lane_s_status":semantic_result["lane_s_overall_status"],
 "semantic_epoch_status":epoch["overall_status"],
 "slot_statuses":{x["slot_id"]:x["status"] for x in slot_results},
 "dimension_promotions":semantic_result["dimension_promotions_to_pass"],
 "failures":semantic_result["registered_target_proposition_failures"],
 "request_manifest_authorized":semantic_result["lane_p_request_manifest_authorized"]
},indent=2))
