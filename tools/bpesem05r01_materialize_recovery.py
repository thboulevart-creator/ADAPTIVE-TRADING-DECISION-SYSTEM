#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05r01"
REPORT=ROOT/"reports"/"data-qualification"/"bpesem05r01_recovery_candidate_2026-09-22.md"

INPUTS={
"04-REFERENCE/AI-OPERATING-MEMORY.md":"0ec6687b288bdd76284fe05e2e437d3bd2b89518",
"evidence/bpesem05/lane_s_qualification_v0_1.json":"b5223228e02818a6d00b3e5d4d329af5abe74578",
"reports/data-qualification/bpesem05_final_closeout_2026-09-22.md":"adff96d9497e4be491ff9fa26a63cc2d40a9dcb2",
"99-BACKUP/SESSION-2026-09-22-BPESEM05-FINAL-CLOSEOUT.md":"ebd7f5eee3f135d5d4f8253516266292d5265f34",
"reports/data-qualification/post_bpesem05_lane_s_blocked_authority_recovery_route_selection_2026-09-22.md":"3a15319721970983fc49e5388f09ef97170108fe",
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_1.json":"e6e3c2a671ade38ec34f2dad03c02e2e20d06adc",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_1.json":"ff0e950eef72dee5497e6db480cd8ce9e16fc31a",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_1.json":"92e1d8a467682f530bde4c2e34bf718d638eddc3",
"evidence/bpesem05r01/provider_pom_snapshot_set_v0_1.json":"f8d45a07d739f1916cf741fe686c539454a43350",
"evidence/bpesem05r01/provider_artifact_inventory_analysis_v0_1.json":"ad451efdaf6ff0a190f198357a9faac9de75cbf1",
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_2.json":"130f767ea4a470edbd604b8896a62354589f25b7",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_2.json":"6869b00772048097d87afc40a8775baf61669f14",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_2.json":"59e3b004cca1fd909019723e119bc994b629830e",
"evidence/bpesem05r01/provider_pom_snapshot_set_v0_2.json":"8e9137aa4a25878852aaae5b73bae51f1c6e8665",
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_3.json":"93067b75ecd2d5167b2efe4ebe39042fd3ba7bd8",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_3.json":"95502f7a0600e34eda34ffa78665db7ee8b81046",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_3.json":"e77c87a54da46394dae457f36c8f70ccd1043b79",
"evidence/bpesem05r01/provider_pom_snapshot_set_v0_3.json":"2aefd99332d254539ad9fe972e4427cdc42c6d6c",
"evidence/bpesem05r01/provider_artifact_semantic_extraction_plan_v0_1.json":"b5dd1bfc3cbd217b7294407adf74855b2127a486",
"evidence/bpesem05r01/semantic_extraction_identity_registry_v0_1.json":"aee550bd1b05abea92105ed66018918fb2f7b30b",
"evidence/bpesem05r01/pinned_greed_bytecode_extraction_v0_1.json":"6c7c601b1096eec83aac39a038275161d73e2303",
"evidence/bpesem05r01/msg_semantic_inventory_v0_1.json":"b2dd084446e9f4c379f5a59a9c502cfd0be3567f",
"evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json":"f934df8ea93018ee0c22b2d69575f15fc8f2c72f",
}

TARGET_START="2021-08-13T01:00:00Z"
TARGET_END="2026-08-14T20:00:00Z"

def canon(v:Any)->bytes:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def digest(v:Any)->str:
    return hashlib.sha256(canon(v)).hexdigest()
def seal(o:dict,field:str)->str:
    x=copy.deepcopy(o); x.pop(field,None); return digest(x)
def git(*args:str)->str:
    return subprocess.check_output(["git",*args],cwd=ROOT,text=True).strip()
def blob(path:str)->str:
    return git("hash-object",path)
def readj(path:str)->dict:
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def writej(name:str,obj:dict):
    p=E/name
    p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")

HEAD=git("rev-parse","HEAD")
TREE=git("rev-parse",HEAD+"^{tree}")
for p,b in INPUTS.items():
    if blob(p)!=b:
        raise RuntimeError("governed input drift: "+p+" expected="+b+" got="+blob(p))

q=readj("evidence/bpesem05/lane_s_qualification_v0_1.json")
if q["overall_governed_result"]!="BLOCKED" or q["package_integrity_status"]!="PASS":
    raise RuntimeError("unexpected B-PE-SEM-05 starting state")

id1=readj("evidence/bpesem05r01/provider_artifact_identity_registry_v0_1.json")
id2=readj("evidence/bpesem05r01/provider_artifact_identity_registry_v0_2.json")
id3=readj("evidence/bpesem05r01/provider_artifact_identity_registry_v0_3.json")
inv3=readj("evidence/bpesem05r01/relevant_class_resource_inventory_v0_3.json")
bytecode=readj("evidence/bpesem05r01/pinned_greed_bytecode_extraction_v0_1.json")
msg=readj("evidence/bpesem05r01/msg_semantic_inventory_v0_1.json")
bpe03=readj("evidence/bpe03/legacy_hourly_scope_version_evidence_bundle_v0_1.json")

for reg in (id1,id2,id3):
    if reg["all_official_sha1_checks"]!="PASS" or not reg["no_market_data_object_acquired"]:
        raise RuntimeError("artifact identity registry not qualified")

semid=readj("evidence/bpesem05r01/semantic_extraction_identity_registry_v0_1.json")
if not semid["no_market_data_object_acquired"]:
    raise RuntimeError("semantic extraction boundary violation")
for r in semid["records"]:
    if r.get("sha1_verification") not in (None,"PASS"):
        raise RuntimeError("semantic extraction SHA1 failure")
    if r.get("expected_sha256_verification") not in (None,"PASS"):
        raise RuntimeError("semantic extraction SHA256 failure")

# Exact provider-artifact observations used in final findings.
data_cache_records=[r for r in inv3["records"] if r["entry_path"]=="com/dukascopy/charts/data/datacache/DataCacheUtils.class"]
filter_records=[r for r in inv3["records"] if r["entry_path"]=="com/dukascopy/charts/data/datacache/DataCacheUtils$4.class"]
conv_records=[r for r in inv3["records"] if r["entry_path"]=="com/dukascopy/dds2/greed/util/AbstractCurrencyConverter.class"]
if len(data_cache_records)!=5 or len(filter_records)!=5 or len(conv_records)!=5:
    raise RuntimeError("expected five greed-common observations per critical class")
if len({r["entry_sha256"] for r in data_cache_records})!=1:
    raise RuntimeError("DataCacheUtils cross-version identity unexpectedly changed")
if len({r["entry_sha256"] for r in filter_records})!=1:
    raise RuntimeError("DataCacheUtils$4 cross-version identity unexpectedly changed")
if len({r["entry_sha256"] for r in conv_records})!=1:
    raise RuntimeError("AbstractCurrencyConverter cross-version identity unexpectedly changed")
if not all(any("_ticks.bi5" in s for s in r["matched_strings"]) for r in filter_records):
    raise RuntimeError("expected provider _ticks.bi5 evidence missing")

bc_by={(r["artifact_id"],r["class_name"]):r for r in bytecode["records"]}
for aid in ["GREED-COMMON-318.4.115-REINSPECTION","GREED-COMMON-318.4.128-REINSPECTION"]:
    dc=bc_by[(aid,"com.dukascopy.charts.data.datacache.DataCacheUtils")]
    if 'VERSION_5_CACHE_FILE_EXTENSION = "bi5"' not in dc["javap_text"]:
        raise RuntimeError("provider V5 bi5 constant missing")
    f=bc_by[(aid,"com.dukascopy.charts.data.datacache.DataCacheUtils$4")]
    if "_ticks.bi5" not in f["javap_text"]:
        raise RuntimeError("provider tick bi5 filter missing")

# No extracted provider artifact binds native format fields or static USATECH raw divisor.
all_javap="\n".join(r["javap_text"] for r in bytecode["records"]).lower()
exact_layout_markers=[">iiiff",">iiiff",">3i2f","20 bytes","20-byte","lzma"]
observed_layout_markers=[m for m in exact_layout_markers if m in all_javap]

msg_text="\n".join(r["entry_path"]+"\n"+"\n".join(r["matched_strings"]) for r in msg["records"]).lower()
msg_bi5="bi5" in msg_text
msg_jetta="jetta" in msg_text
msg_usatech="usatech" in msg_text

instrument_settings=[r for r in msg["records"] if r["entry_path"]=="com/dukascopy/dds3/transport/msg/settings/InstrumentSettings.class"]
if len(instrument_settings)!=2:
    raise RuntimeError("expected InstrumentSettings in both msg versions")
if len({r["entry_sha256"] for r in instrument_settings})!=1:
    raise RuntimeError("InstrumentSettings cross-version identity changed unexpectedly")
if not all(any("priceScale" in s for s in r["matched_strings"]) for r in instrument_settings):
    raise RuntimeError("priceScale schema missing")

stable_msg_paths=[
"com/dukascopy/dds3/transport/msg/dfs/CandleHistoryGroupMessage.class",
"com/dukascopy/dds3/transport/msg/dfs/DFHistoryStartRequestMessage.class",
"com/dukascopy/dds3/transport/msg/dfw/TickCacheDataRequestMessage.class",
"com/dukascopy/dds3/transport/msg/dfw/TickCacheDataResponseMessage.class",
"com/dukascopy/dds3/transport/msg/dfw/TickMessage.class",
"com/dukascopy/dds3/transport/msg/settings/InstrumentSettings.class",
]
stable_msg=[]
for p in stable_msg_paths:
    rs=[r for r in msg["records"] if r["entry_path"]==p]
    if len(rs)!=2 or len({r["entry_sha256"] for r in rs})!=1:
        raise RuntimeError("expected cross-version stability for "+p)
    stable_msg.append({"entry_path":p,"sha256":rs[0]["entry_sha256"],"versions":[r["artifact_id"] for r in rs]})

# Provider release evidence for JETTA.
jetta=[x for x in bpe03["sources"] if x["evidence_id"]=="BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE"]
if len(jetta)!=1 or jetta[0]["publication_or_commit_time"]!="2026-03-03T00:00:00Z":
    raise RuntimeError("JETTA governed source missing")

all_unique={}
for family,reg in [("DDS2_JCLIENT_AND_API",id1),("DDS2_CHARTS",id2),("GREED_COMMON",id3)]:
    for r in reg["records"]:
        all_unique[r["coordinate"]]={
            "family":family,
            "artifact_id":r["artifact_id"],
            "coordinate":r["coordinate"],
            "artifact_sha256":r["computed_sha256"],
            "official_sha1":r["official_sha1"],
            "sha1_verification":r["sha1_verification"],
            "pom_sha256":r["pom_computed_sha256"],
        }
for r in semid["records"]:
    if r["artifact_id"].startswith("MSG-"):
        coord=("com.dukascopy.dds2:msg:1.1.98.2-JForex3" if "98.2" in r["artifact_id"]
               else "com.dukascopy.dds2:msg:1.1.98.4-JForex3")
        all_unique[coord]={
            "family":"MSG","artifact_id":r["artifact_id"],"coordinate":coord,
            "artifact_sha256":r["computed_sha256"],"official_sha1":r["official_sha1"],
            "sha1_verification":r["sha1_verification"],"pom_sha256":r["pom_sha256"],
        }

artifact_inventory={
 "schema":"BPESEM05R01_PROVIDER_ARTIFACT_INVENTORY_V0_1",
 "candidate_parent_head":HEAD,
 "provider":"Dukascopy Bank SA",
 "target_interval":{"start":TARGET_START,"end":TARGET_END},
 "unique_provider_artifact_count":len(all_unique),
 "artifact_families":["DDS2-jClient-JForex","JForex-API sources","DDS2-Charts","greed-common","msg"],
 "records":[all_unique[k] for k in sorted(all_unique)],
 "acquisition_plan_blobs":[
     INPUTS["evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_1.json"],
     INPUTS["evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_2.json"],
     INPUTS["evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_3.json"],
     INPUTS["evidence/bpesem05r01/provider_artifact_semantic_extraction_plan_v0_1.json"],
 ],
 "all_provider_sidecar_checks":"PASS",
 "no_market_data_object_acquired":True
}
artifact_inventory["inventory_seal"]=seal(artifact_inventory,"inventory_seal")

identity_registry={
 "schema":"BPESEM05R01_PROVIDER_ARTIFACT_IDENTITY_REGISTRY_COMPOSITE_V0_1",
 "source_registries":[
   {"path":"evidence/bpesem05r01/provider_artifact_identity_registry_v0_1.json","blob":INPUTS["evidence/bpesem05r01/provider_artifact_identity_registry_v0_1.json"]},
   {"path":"evidence/bpesem05r01/provider_artifact_identity_registry_v0_2.json","blob":INPUTS["evidence/bpesem05r01/provider_artifact_identity_registry_v0_2.json"]},
   {"path":"evidence/bpesem05r01/provider_artifact_identity_registry_v0_3.json","blob":INPUTS["evidence/bpesem05r01/provider_artifact_identity_registry_v0_3.json"]},
   {"path":"evidence/bpesem05r01/semantic_extraction_identity_registry_v0_1.json","blob":INPUTS["evidence/bpesem05r01/semantic_extraction_identity_registry_v0_1.json"]},
 ],
 "all_exact_identity_checks":"PASS",
 "duplicate_reinspection_rule":"Pinned greed-common reinspections are identity verification, not additional independent evidence.",
 "no_market_data_object_acquired":True
}
identity_registry["identity_registry_seal"]=seal(identity_registry,"identity_registry_seal")

resource_inventory={
 "schema":"BPESEM05R01_RELEVANT_CLASS_RESOURCE_INVENTORY_COMPOSITE_V0_1",
 "source_inventories":[
   {"path":"evidence/bpesem05r01/relevant_class_resource_inventory_v0_1.json","blob":INPUTS["evidence/bpesem05r01/relevant_class_resource_inventory_v0_1.json"]},
   {"path":"evidence/bpesem05r01/relevant_class_resource_inventory_v0_2.json","blob":INPUTS["evidence/bpesem05r01/relevant_class_resource_inventory_v0_2.json"]},
   {"path":"evidence/bpesem05r01/relevant_class_resource_inventory_v0_3.json","blob":INPUTS["evidence/bpesem05r01/relevant_class_resource_inventory_v0_3.json"]},
   {"path":"evidence/bpesem05r01/pinned_greed_bytecode_extraction_v0_1.json","blob":INPUTS["evidence/bpesem05r01/pinned_greed_bytecode_extraction_v0_1.json"]},
   {"path":"evidence/bpesem05r01/msg_semantic_inventory_v0_1.json","blob":INPUTS["evidence/bpesem05r01/msg_semantic_inventory_v0_1.json"]},
 ],
 "critical_provider_resources":[
   {"entry":"com/dukascopy/charts/data/datacache/DataCacheUtils.class","sha256":data_cache_records[0]["entry_sha256"],"stable_across_greed_versions":True},
   {"entry":"com/dukascopy/charts/data/datacache/DataCacheUtils$4.class","sha256":filter_records[0]["entry_sha256"],"stable_across_greed_versions":True},
   {"entry":"com/dukascopy/dds2/greed/util/AbstractCurrencyConverter.class","sha256":conv_records[0]["entry_sha256"],"stable_across_greed_versions":True},
   *stable_msg,
 ],
}
resource_inventory["resource_inventory_seal"]=seal(resource_inventory,"resource_inventory_seal")

lineage={
 "schema":"BPESEM05R01_ARTIFACT_LINEAGE_RESOLUTION_V0_1",
 "provider_lineage_id":"LINEAGE-DUKASCOPY-OFFICIAL-MAVEN-DISTRIBUTION",
 "all_acquired_artifacts_single_provider_lineage":True,
 "dependency_chain":[
   "DDS2-jClient-JForex -> DDS2-Charts",
   "DDS2-Charts -> greed-common",
   "greed-common -> msg",
 ],
 "independence_claim":"NONE_WITHIN_PROVIDER_CHAIN",
 "reinspection_deduplicated":True,
 "status":"RESOLVED"
}
lineage["lineage_resolution_seal"]=seal(lineage,"lineage_resolution_seal")

finding_a={
 "schema":"BPESEM05R01_LEGACY_HOURLY_SEMANTIC_ARTIFACT_FINDING_V0_1",
 "recovery_target":"A",
 "provider_evidence":[
   {"class":"com.dukascopy.charts.data.datacache.DataCacheUtils","class_sha256":data_cache_records[0]["entry_sha256"],"finding":"Provider client code defines VERSION_5_CACHE_FILE_EXTENSION = bi5."},
   {"class":"com.dukascopy.charts.data.datacache.DataCacheUtils$4","class_sha256":filter_records[0]["entry_sha256"],"finding":"Provider client code explicitly recognizes _ticks.bi5 and _ticks.bin intra-period tick files."},
 ],
 "cross_version_fact":"Both critical classes are byte-identical across greed-common 318.4.115, 318.4.118, 318.4.125, 318.4.127 and 318.4.128.",
 "exact_native_layout_semantics_found":False,
 "observed_exact_layout_markers":observed_layout_markers,
 "not_recovered":["compression/wrapper authority","20-byte record width authority","five-field primitive layout authority","field role authority","hour-relative timestamp authority for target K1","native raw price divisor authority","volume encoding/role authority"],
 "interpretation":"Provider-versioned artifacts recover an exact BI5 cache-format identity/usage trace, but do not bind the exact legacy-hourly native payload semantics required by Recovery A.",
 "status":"AMBIGUOUS"
}
finding_a["finding_seal"]=seal(finding_a,"finding_seal")

finding_b={
 "schema":"BPESEM05R01_USATECH_RAW_SCALE_ARTIFACT_FINDING_V0_1",
 "recovery_target":"B",
 "provider_artifact_facts":[
   "Provider DDS2 distributions expose Instrument.USATECHIDXUSD and API pip/tick scale interfaces.",
   "Provider msg InstrumentSettings schema exposes priceScale and pricePipValue fields.",
   "AbstractCurrencyConverter is byte-identical across all five inspected greed-common versions and references USATECHIDXUSD as an instrument conversion dependency.",
 ],
 "msg_instrument_settings_sha256":instrument_settings[0]["entry_sha256"],
 "usatech_static_native_bi5_raw_divisor_found":False,
 "raw_divisor_value":None,
 "forbidden_inference_preserved":"API pip/tick scale or runtime InstrumentSettings.priceScale is not treated as native BI5 raw integer divisor without an exact provider binding.",
 "third_party_1000_not_used_as_provider_primary":True,
 "status":"NOT_FOUND"
}
finding_b["finding_seal"]=seal(finding_b,"finding_seal")

ledger={
 "schema":"BPESEM05R01_CROSS_VERSION_SEMANTIC_CHANGE_LEDGER_V0_1",
 "target_interval":{"start":TARGET_START,"end":TARGET_END},
 "provider_release_samples":[
   {"client":"3.6.34","relation":"PRE_TARGET_NEAR_BOUNDARY","greed_common":"318.4.115","msg":"1.1.98.2-JForex3"},
   {"client":"3.6.37","relation":"POST_TARGET_START","greed_common":"318.4.118","msg":"1.1.98.2-JForex3"},
   {"client":"3.6.48","relation":"TARGET_2023","greed_common":"318.4.125","msg":"1.1.98.4-JForex3"},
   {"client":"3.6.49","relation":"TARGET_2024","greed_common":"318.4.127","msg":"1.1.98.4-JForex3"},
   {"client":"3.6.51","relation":"TARGET_2025","greed_common":"318.4.128","msg":"1.1.98.4-JForex3"},
 ],
 "stable_provider_classes":[
   {"entry":"DataCacheUtils.class","sha256":data_cache_records[0]["entry_sha256"],"versions":5},
   {"entry":"DataCacheUtils$4.class","sha256":filter_records[0]["entry_sha256"],"versions":5},
   {"entry":"AbstractCurrencyConverter.class","sha256":conv_records[0]["entry_sha256"],"versions":5},
   *stable_msg,
 ],
 "observed_msg_version_transition":{"from":"1.1.98.2-JForex3","to":"1.1.98.4-JForex3","selected_critical_history_tick_classes_changed":False},
 "coverage_limitations":[
   "Selected public Maven client lineage ends at DDS2-jClient-JForex 3.6.51 / 2025-10 in the governed inventory.",
   "Target interval continues through 2026-08-14.",
   "2026-03-03 JETTA release-note change has no matching inspected public Maven client artifact in this recovery package.",
   "Byte-identical client/cache/message classes do not prove server-side or public raw-object semantic continuity.",
 ],
 "continuity_conclusion":"PARTIAL_CLIENT_ARTIFACT_STABILITY_ONLY",
 "full_target_semantic_continuity_proven":False
}
ledger["ledger_seal"]=seal(ledger,"ledger_seal")

jetta_finding={
 "schema":"BPESEM05R01_JETTA_CHANGE_IMPACT_FINDING_V0_1",
 "event_time":"2026-03-03T00:00:00Z",
 "provider_evidence_id":"BPE03-E03-DUKASCOPY-JFOREX-4-8-0-RELEASE",
 "governed_source_bundle_blob":"f934df8ea93018ee0c22b2d69575f15fc8f2c72f",
 "provider_statement_scope":"JForex 4.8.0 historical price data retrieval from JETTA.",
 "jetta_string_found_in_acquired_maven_artifacts":False,
 "matching_2026_public_dds2_client_artifact_inspected":False,
 "native_k1_wire_semantic_effect":"UNRESOLVED",
 "cannot_infer":["NO_CHANGE_TO_K1","CHANGE_TO_K1","LEGACY_HOURLY_TO_DAILY_TRANSITION_DATE"],
 "status":"BLOCKED_UNRESOLVED_IMPACT"
}
if msg_jetta:
    raise RuntimeError("unexpected JETTA string discovered; finding must be re-adjudicated")
jetta_finding["finding_seal"]=seal(jetta_finding,"finding_seal")

recovery_a={
 "schema":"BPESEM05R01_RECOVERY_A_RESULT_V0_1",
 "target":"exact immutable/provider-versioned legacy-hourly K1 semantic authority",
 "evidence_recovered":["provider V5 cache extension = bi5","provider _ticks.bi5 recognition","cross-version byte identity of DataCacheUtils/DataCacheUtils$4"],
 "required_exact_semantics_recovered":False,
 "result":"AMBIGUOUS",
 "reason_codes":["PROVIDER_BI5_USAGE_IDENTITY_RECOVERED","EXACT_NATIVE_PAYLOAD_SEMANTICS_NOT_EXPOSED","CACHE_FILE_SEMANTICS_NE_PUBLIC_RAW_OBJECT_SEMANTICS"]
}
recovery_a["result_seal"]=seal(recovery_a,"result_seal")

recovery_b={
 "schema":"BPESEM05R01_RECOVERY_B_RESULT_V0_1",
 "target":"exact provider-primary native BI5 USATECH raw scale/divisor authority",
 "evidence_recovered":["USATECH provider API identity","Instrument pip/tick scale interfaces","InstrumentSettings priceScale schema"],
 "required_native_raw_divisor_recovered":False,
 "result":"NOT_FOUND",
 "reason_codes":["NO_STATIC_USATECH_NATIVE_BI5_RAW_DIVISOR_IN_INSPECTED_PROVIDER_ARTIFACTS","RUNTIME_PRICE_SCALE_SCHEMA_NE_RAW_BI5_DIVISOR","NO_CIRCULAR_INFERENCE"]
}
recovery_b["result_seal"]=seal(recovery_b,"result_seal")

recovery_c={
 "schema":"BPESEM05R01_RECOVERY_C_RESULT_V0_1",
 "target":"exhaustive target-epoch semantic change-point / continuity authority",
 "partial_stability_recovered":True,
 "full_target_coverage_recovered":False,
 "result":"INCOMPLETE_VERSION_COVERAGE",
 "reason_codes":["CLIENT_CACHE_CLASSES_STABLE_ACROSS_SELECTED_2021_2025_ARTIFACTS","SELECTED_MSG_HISTORY_TICK_SCHEMAS_STABLE_ACROSS_MSG_VERSIONS","NO_INSPECTED_2026_PUBLIC_MAVEN_CLIENT_ARTIFACT","JETTA_2026_K1_IMPACT_UNRESOLVED","CLIENT_STABILITY_NE_SERVER_RAW_OBJECT_SEMANTIC_CONTINUITY"]
}
recovery_c["result_seal"]=seal(recovery_c,"result_seal")

horizon={
 "schema":"BPESEM05R01_DOCUMENTARY_EVIDENCE_HORIZON_V0_1",
 "candidate_parent_head":HEAD,
 "provider_artifact_channel":"Dukascopy official Maven/public distribution chain",
 "families_exhausted_in_this_block":["DDS2-jClient-JForex","JForex-API sources","DDS2-Charts","greed-common","msg"],
 "specific_dependency_following_rule":"Only dependencies directly demonstrated by persisted provider POMs were followed.",
 "not_followed_generic_dependency":"system-msg 1.0.32 was not followed because msg inspection exposed no specific A/B/C semantic dependency requiring it.",
 "recovery_results":{"A":"AMBIGUOUS","B":"NOT_FOUND","C":"INCOMPLETE_VERSION_COVERAGE"},
 "remaining_authority_gaps":[
   "Exact provider binding of legacy-hourly K1 raw payload semantics.",
   "Exact provider binding of USATECH native BI5 raw integer divisor.",
   "2026/JETTA and server-side/public-object semantic continuity through target end."
 ],
 "lane_s_readjudication_sufficient_new_authority":False,
 "lane_p_authorization_effect":"NONE",
 "overall_status":"BLOCKED"
}
horizon["horizon_seal"]=seal(horizon,"horizon_seal")

attestation={
 "schema":"BPESEM05R01_NO_MARKET_DATA_OBSERVATION_ATTESTATION_V0_1",
 "provider_software_documentary_artifact_acquisition_performed":True,
 "provider_bi5_market_data_get_performed":False,
 "historical_market_data_object_acquired":False,
 "lane_p_request_manifest_created":False,
 "p_diag_implemented":False,
 "physical_semantic_discrimination_executed":False,
 "full_interval_executed":False,
 "d_materialized":False,
 "backtest_executed":False,
 "evidence":["All acquisition plans reject .bi5/datafeed market-data URLs.","All persisted provider artifact registries attest no market-data object acquired."],
 "status":"PASS"
}
attestation["attestation_seal"]=seal(attestation,"attestation_seal")

overall={
 "schema":"BPESEM05R01_RECOVERY_PACKAGE_RESULT_V0_1",
 "block":"B-PE-SEM-05R-01",
 "candidate_parent_head":HEAD,
 "candidate_parent_tree":TREE,
 "package_integrity_candidate_status":"READY_FOR_ADVERSARIAL_BREAK",
 "recovery_a":"AMBIGUOUS",
 "recovery_b":"NOT_FOUND",
 "recovery_c":"INCOMPLETE_VERSION_COVERAGE",
 "any_full_recovery":False,
 "lane_s_readjudication_authorized_by_this_block":False,
 "lane_p_authorized":False,
 "overall_substantive_result":"BLOCKED",
 "reason":"Provider-versioned Maven archaeology recovered material BI5/cache/history evidence and partial cross-version stability, but did not recover all provider-primary authority required by A/B/C."
}
overall["package_result_seal"]=seal(overall,"package_result_seal")

for fn,obj in [
 ("provider_artifact_inventory_v0_1.json",artifact_inventory),
 ("provider_artifact_identity_registry_composite_v0_1.json",identity_registry),
 ("relevant_class_resource_inventory_composite_v0_1.json",resource_inventory),
 ("artifact_lineage_resolution_v0_1.json",lineage),
 ("legacy_hourly_semantic_artifact_finding_v0_1.json",finding_a),
 ("usatech_raw_scale_artifact_finding_v0_1.json",finding_b),
 ("cross_version_semantic_change_ledger_v0_1.json",ledger),
 ("jetta_change_impact_finding_v0_1.json",jetta_finding),
 ("recovery_a_result_v0_1.json",recovery_a),
 ("recovery_b_result_v0_1.json",recovery_b),
 ("recovery_c_result_v0_1.json",recovery_c),
 ("documentary_evidence_horizon_v0_1.json",horizon),
 ("no_market_data_observation_attestation_v0_1.json",attestation),
 ("recovery_package_result_v0_1.json",overall),
]:
    writej(fn,obj)

REPORT.parent.mkdir(parents=True,exist_ok=True)
REPORT.write_text(f"""# B-PE-SEM-05R-01 — PROVIDER-VERSIONED ARTIFACT DOCUMENTARY RECOVERY — CANDIDATE

Candidate parent HEAD: {HEAD}

## Recovery outcomes

~~~text
Recovery A = AMBIGUOUS
Recovery B = NOT_FOUND
Recovery C = INCOMPLETE_VERSION_COVERAGE

any full recovery = NO
Lane S re-adjudication authority effect = NONE
Lane P authority effect = NONE

overall substantive result = BLOCKED
~~~

Provider Maven archaeology recovered exact SHA-verified artifacts across DDS2 client, API sources, DDS2-Charts, greed-common and msg.

Material positive findings include provider-owned VERSION_5 cache extension "bi5", provider recognition of "_ticks.bi5", stable DataCacheUtils/DataCacheUtils$4 across all five selected greed-common versions, stable selected history/tick message schemas across msg 1.1.98.2 and 1.1.98.4, and provider USATECH/API priceScale structures.

However the inspected artifacts do not expose an exact provider-primary binding for the legacy-hourly native payload layout or USATECH raw BI5 divisor. Public Maven coverage in the selected lineage ends in 2025 while the governed target continues through 2026-08-14, and the 2026-03-03 JETTA effect on K1 remains unresolved.

No provider BI5 market-data object was requested or observed. No Lane P RequestManifest/P-DIAG/FULL_INTERVAL/D/backtest was created or executed.
""",encoding="utf-8")

print(json.dumps({
 "candidate_parent_head":HEAD,
 "unique_provider_artifacts":len(all_unique),
 "data_cache_sha256":data_cache_records[0]["entry_sha256"],
 "data_cache_filter_sha256":filter_records[0]["entry_sha256"],
 "abstract_currency_converter_sha256":conv_records[0]["entry_sha256"],
 "observed_exact_layout_markers":observed_layout_markers,
 "msg_bi5":msg_bi5,"msg_usatech":msg_usatech,"msg_jetta":msg_jetta,
 "RecoveryA":recovery_a["result"],"RecoveryB":recovery_b["result"],"RecoveryC":recovery_c["result"],
 "overall":overall["overall_substantive_result"]
},indent=2))
