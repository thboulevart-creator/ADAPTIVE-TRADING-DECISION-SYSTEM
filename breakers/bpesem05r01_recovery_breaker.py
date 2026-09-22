#!/usr/bin/env python3
from __future__ import annotations

import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05r01"
REPORT=Path(os.environ.get("BPESEM05R01_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem05r01_recovery_adversarial_break_2026-09-22.md")))

EXPECTED={
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_1.json":"e6e3c2a671ade38ec34f2dad03c02e2e20d06adc",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_1.json":"ff0e950eef72dee5497e6db480cd8ce9e16fc31a",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_1.json":"92e1d8a467682f530bde4c2e34bf718d638eddc3",
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_2.json":"130f767ea4a470edbd604b8896a62354589f25b7",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_2.json":"6869b00772048097d87afc40a8775baf61669f14",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_2.json":"59e3b004cca1fd909019723e119bc994b629830e",
"evidence/bpesem05r01/provider_artifact_acquisition_plan_v0_3.json":"93067b75ecd2d5167b2efe4ebe39042fd3ba7bd8",
"evidence/bpesem05r01/provider_artifact_identity_registry_v0_3.json":"95502f7a0600e34eda34ffa78665db7ee8b81046",
"evidence/bpesem05r01/relevant_class_resource_inventory_v0_3.json":"e77c87a54da46394dae457f36c8f70ccd1043b79",
"evidence/bpesem05r01/provider_artifact_semantic_extraction_plan_v0_1.json":"b5dd1bfc3cbd217b7294407adf74855b2127a486",
"evidence/bpesem05r01/semantic_extraction_identity_registry_v0_1.json":"aee550bd1b05abea92105ed66018918fb2f7b30b",
"evidence/bpesem05r01/pinned_greed_bytecode_extraction_v0_1.json":"6c7c601b1096eec83aac39a038275161d73e2303",
"evidence/bpesem05r01/msg_semantic_inventory_v0_1.json":"b2dd084446e9f4c379f5a59a9c502cfd0be3567f",
"evidence/bpesem05/lane_s_qualification_v0_1.json":"b5223228e02818a6d00b3e5d4d329af5abe74578",
"reports/data-qualification/post_bpesem05_lane_s_blocked_authority_recovery_route_selection_2026-09-22.md":"3a15319721970983fc49e5388f09ef97170108fe",
}

OUTFILES=[
"provider_artifact_inventory_v0_1.json",
"provider_artifact_identity_registry_composite_v0_1.json",
"relevant_class_resource_inventory_composite_v0_1.json",
"artifact_lineage_resolution_v0_1.json",
"legacy_hourly_semantic_artifact_finding_v0_1.json",
"usatech_raw_scale_artifact_finding_v0_1.json",
"cross_version_semantic_change_ledger_v0_1.json",
"jetta_change_impact_finding_v0_1.json",
"recovery_a_result_v0_1.json",
"recovery_b_result_v0_1.json",
"recovery_c_result_v0_1.json",
"documentary_evidence_horizon_v0_1.json",
"no_market_data_observation_attestation_v0_1.json",
"recovery_package_result_v0_1.json",
]

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
def read(name:str)->dict:
    return json.loads((E/name).read_text(encoding="utf-8"))

HEAD=git("rev-parse","HEAD")
attacks=[]; defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond: defects.append(name)

check("R01_GOVERNED_INPUT_IDENTITIES",
      all(blob(p)==b for p,b in EXPECTED.items()),
      "all governed recovery inputs remain byte-identical")

check("R02_REQUIRED_OUTPUT_SET",
      all((E/f).exists() for f in OUTFILES),
      "all required compact recovery artifacts exist")

inv=read("provider_artifact_inventory_v0_1.json")
ident=read("provider_artifact_identity_registry_composite_v0_1.json")
resinv=read("relevant_class_resource_inventory_composite_v0_1.json")
lineage=read("artifact_lineage_resolution_v0_1.json")
fa=read("legacy_hourly_semantic_artifact_finding_v0_1.json")
fb=read("usatech_raw_scale_artifact_finding_v0_1.json")
ledger=read("cross_version_semantic_change_ledger_v0_1.json")
jetta=read("jetta_change_impact_finding_v0_1.json")
ra=read("recovery_a_result_v0_1.json")
rb=read("recovery_b_result_v0_1.json")
rc=read("recovery_c_result_v0_1.json")
horizon=read("documentary_evidence_horizon_v0_1.json")
att=read("no_market_data_observation_attestation_v0_1.json")
overall=read("recovery_package_result_v0_1.json")

checks=[
(inv,"inventory_seal"),(ident,"identity_registry_seal"),(resinv,"resource_inventory_seal"),
(lineage,"lineage_resolution_seal"),(fa,"finding_seal"),(fb,"finding_seal"),
(ledger,"ledger_seal"),(jetta,"finding_seal"),(ra,"result_seal"),(rb,"result_seal"),
(rc,"result_seal"),(horizon,"horizon_seal"),(att,"attestation_seal"),(overall,"package_result_seal")
]
check("R03_ALL_SEALS_RECOMPUTE",
      all(o[f]==seal(o,f) for o,f in checks),
      "all compact recovery seals recompute")

check("R04_PROVIDER_ARTIFACT_COUNT_AND_IDENTITY",
      inv["unique_provider_artifact_count"]==19
      and inv["all_provider_sidecar_checks"]=="PASS"
      and all(r["sha1_verification"]=="PASS" for r in inv["records"]),
      "19 unique provider coordinates are bound to verified identities")

check("R05_SINGLE_PROVIDER_LINEAGE",
      lineage["all_acquired_artifacts_single_provider_lineage"] is True
      and lineage["independence_claim"]=="NONE_WITHIN_PROVIDER_CHAIN"
      and lineage["status"]=="RESOLVED",
      "provider dependency chain is not miscounted as independent evidence")

crit={x["entry"]:x for x in resinv["critical_provider_resources"] if "entry" in x}
check("R06_DATACACHE_CROSS_VERSION_IDENTITY",
      crit["com/dukascopy/charts/data/datacache/DataCacheUtils.class"]["sha256"]=="337761c442e7d129095f69bbc1ac6cd71c18dc1ecf2a271f3a9169cd1bed951a"
      and crit["com/dukascopy/charts/data/datacache/DataCacheUtils.class"]["stable_across_greed_versions"] is True,
      "DataCacheUtils is byte-identical across selected greed-common versions")

check("R07_TICK_BI5_FILTER_CROSS_VERSION_IDENTITY",
      crit["com/dukascopy/charts/data/datacache/DataCacheUtils$4.class"]["sha256"]=="013df7da4ef48abd90d6366953c309df1b6f589f9d035a734e7887b158f55d07"
      and crit["com/dukascopy/charts/data/datacache/DataCacheUtils$4.class"]["stable_across_greed_versions"] is True,
      "_ticks.bi5 file filter is byte-identical across selected provider versions")

check("R08_PROVIDER_BI5_IDENTITY_RECOVERED",
      any("VERSION_5" in x["finding"] and "bi5" in x["finding"] for x in fa["provider_evidence"])
      and any("_ticks.bi5" in x["finding"] for x in fa["provider_evidence"]),
      "provider-owned artifacts explicitly bind cache version 5 and tick cache naming to bi5")

check("R09_A_NOT_OVERPROMOTED",
      fa["exact_native_layout_semantics_found"] is False
      and fa["status"]=="AMBIGUOUS"
      and ra["result"]=="AMBIGUOUS"
      and ra["required_exact_semantics_recovered"] is False,
      "BI5 cache identity is not laundered into exact raw-payload semantic authority")

check("R10_A_MISSING_SEMANTICS_EXPLICIT",
      all(x in fa["not_recovered"] for x in [
        "compression/wrapper authority","20-byte record width authority",
        "five-field primitive layout authority","field role authority",
        "hour-relative timestamp authority for target K1",
        "native raw price divisor authority","volume encoding/role authority"]),
      "every material exact-native semantic gap remains explicit")

check("R11_NO_LAYOUT_SIGNATURE_LAUNDERING",
      fa["observed_exact_layout_markers"]==[],
      "no exact layout marker found in pinned provider bytecode extraction")

check("R12_USATECH_PROVIDER_IDENTITY_WITHOUT_RAW_SCALE",
      fb["usatech_static_native_bi5_raw_divisor_found"] is False
      and fb["raw_divisor_value"] is None
      and rb["required_native_raw_divisor_recovered"] is False,
      "provider USATECH/API structures do not contain static native BI5 raw divisor authority")

check("R13_INSTRUMENT_SETTINGS_SCHEMA_NE_VALUE_AUTHORITY",
      "priceScale" in " ".join(fb["provider_artifact_facts"])
      and "runtime InstrumentSettings.priceScale" in fb["forbidden_inference_preserved"],
      "runtime priceScale schema is not converted into native raw divisor authority")

check("R14_B_RESULT_NOT_FOUND",
      fb["status"]=="NOT_FOUND" and rb["result"]=="NOT_FOUND"
      and "NO_CIRCULAR_INFERENCE" in rb["reason_codes"],
      "Recovery B fails closed without /1000 plausibility inference")

stable=ledger["stable_provider_classes"]
check("R15_GREED_CRITICAL_CLASSES_STABLE",
      sum(1 for x in stable if x.get("versions")==5)>=3,
      "three critical provider classes are byte-identical across five sampled greed-common versions")

msg_stable=[x for x in stable if "versions" in x and isinstance(x["versions"],list)]
check("R16_MSG_HISTORY_TICK_SCHEMAS_STABLE",
      len(msg_stable)>=6
      and all(len(x["versions"])==2 for x in msg_stable),
      "selected history/tick/settings message classes are byte-identical across both msg versions")

check("R17_C_PARTIAL_STABILITY_ONLY",
      ledger["continuity_conclusion"]=="PARTIAL_CLIENT_ARTIFACT_STABILITY_ONLY"
      and ledger["full_target_semantic_continuity_proven"] is False,
      "client bytecode stability is not equated with full raw-object semantic continuity")

check("R18_TARGET_INTERVAL_EXACT",
      ledger["target_interval"]["start"]=="2021-08-13T01:00:00Z"
      and ledger["target_interval"]["end"]=="2026-08-14T20:00:00Z",
      "cross-version ledger preserves exact governed target interval")

check("R19_2026_COVERAGE_GAP_EXPLICIT",
      any("2025-10" in x for x in ledger["coverage_limitations"])
      and any("2026-08-14" in x for x in ledger["coverage_limitations"]),
      "public Maven lineage does not silently cover target end")

check("R20_JETTA_IMPACT_UNRESOLVED",
      jetta["event_time"]=="2026-03-03T00:00:00Z"
      and jetta["native_k1_wire_semantic_effect"]=="UNRESOLVED"
      and jetta["jetta_string_found_in_acquired_maven_artifacts"] is False
      and jetta["matching_2026_public_dds2_client_artifact_inspected"] is False,
      "JETTA change is retained as unresolved rather than inferred stable/changed")

check("R21_C_RESULT_INCOMPLETE_COVERAGE",
      rc["result"]=="INCOMPLETE_VERSION_COVERAGE"
      and rc["full_target_coverage_recovered"] is False
      and rc["partial_stability_recovered"] is True,
      "Recovery C distinguishes partial stability from exhaustive target coverage")

check("R22_GENERIC_DEPENDENCY_STOP_RULE",
      "system-msg" in horizon["not_followed_generic_dependency"]
      and "specific A/B/C semantic dependency" in horizon["not_followed_generic_dependency"],
      "dependency recursion stops unless evidence demonstrates relevance")

check("R23_RECOVERY_RESULTS_EXACT",
      horizon["recovery_results"]=={"A":"AMBIGUOUS","B":"NOT_FOUND","C":"INCOMPLETE_VERSION_COVERAGE"},
      "documentary horizon binds exact A/B/C outcomes")

check("R24_NO_LANE_S_READJUDICATION",
      horizon["lane_s_readjudication_sufficient_new_authority"] is False
      and overall["lane_s_readjudication_authorized_by_this_block"] is False,
      "recovery block does not self-promote Lane S")

check("R25_NO_LANE_P_AUTHORIZATION",
      horizon["lane_p_authorization_effect"]=="NONE"
      and overall["lane_p_authorized"] is False,
      "Lane P remains closed")

check("R26_NO_MARKET_DATA_OBSERVATION",
      att["provider_bi5_market_data_get_performed"] is False
      and att["historical_market_data_object_acquired"] is False
      and att["status"]=="PASS",
      "only provider software/documentary artifacts were acquired")

check("R27_NO_DISALLOWED_EXECUTION",
      att["lane_p_request_manifest_created"] is False
      and att["p_diag_implemented"] is False
      and att["physical_semantic_discrimination_executed"] is False
      and att["full_interval_executed"] is False
      and att["d_materialized"] is False
      and att["backtest_executed"] is False,
      "all downstream execution boundaries remain closed")

serialized=json.dumps([inv,ident,resinv,lineage,fa,fb,ledger,jetta,ra,rb,rc,horizon,att,overall],sort_keys=True)
check("R28_NO_C08_AUTHORITY_LEAKAGE",
      "C08-D" not in serialized and "BPE-SEM-C08" not in serialized,
      "recovery package does not create a C08 authority path")

tracked=git("ls-files","evidence/bpesem05r01","reports/data-qualification/bpesem05r01*","tools/bpesem05r01*","breakers/bpesem05r01*")
check("R29_NO_LANE_P_ARTIFACTS",
      "request_manifest" not in tracked.lower() and "p_diag" not in tracked.lower(),
      "no Lane P artifacts are created by provider documentary recovery")

check("R30_OVERALL_BLOCKED_FAIL_CLOSED",
      overall["any_full_recovery"] is False
      and overall["overall_substantive_result"]=="BLOCKED"
      and overall["package_integrity_candidate_status"]=="READY_FOR_ADVERSARIAL_BREAK",
      "partial positive provider findings do not overpromote overall recovery")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=[
"# B-PE-SEM-05R-01 — RECOVERY PACKAGE ADVERSARIAL BREAK","",
"Persisted candidate HEAD attacked: "+HEAD,"",
"Package breaker verdict: "+verdict,""
]
for n,s,d in attacks:
    lines += ["## "+n,"",s+" — "+d,""]
lines += [
"## Result","","~~~text",
"attack count = "+str(len(attacks)),
"demonstrated defects = "+str(len(defects)),
*(defects or ["NONE"]),
"~~~","",
"This breaker qualifies the recovery package integrity. It does not convert A/B/C into recovered authority.","",
"No provider BI5 market-data object, Lane P RequestManifest/P-DIAG, FULL_INTERVAL, D or backtest was authorized or executed.","","STOP."
]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":HEAD,"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))
