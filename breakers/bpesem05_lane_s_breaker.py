#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, json, os, subprocess
from pathlib import Path
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"evidence"/"bpesem05"
REPORT=Path(os.environ.get("BPESEM05_BREAK_REPORT",str(ROOT/"reports"/"data-qualification"/"bpesem05_lane_s_adversarial_break_2026-09-22.md")))

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

EXPECTED_SLOTS=[
"BPESEM04-S-E01-PROVIDER-FORMAT-SEMANTICS",
"BPESEM04-S-E02-PROVIDER-INSTRUMENT-SCALE",
"BPESEM04-S-E03-PROVIDER-EPOCH-CONTINUITY",
"BPESEM04-S-E04-INDEPENDENT-CORROBORATION-A",
"BPESEM04-S-E05-INDEPENDENT-CORROBORATION-B",
"BPESEM04-S-E06-CONTRADICTION-SWEEP"]

FILES=[
"lane_s_evidence_registry_v0_1.json",
"source_lineage_resolution_v0_1.json",
"provider_primary_semantic_anchor_set_v0_1.json",
"provider_instrument_scale_authority_v0_1.json",
"provider_semantic_change_point_inventory_v0_1.json",
"semantic_epoch_manifest_v0_1.json",
"independent_corroboration_register_v0_1.json",
"contradiction_sweep_result_v0_1.json",
"lane_s_scope_applicability_decision_v0_1.json",
"lane_s_semantic_authority_result_v0_1.json",
"current_evidence_horizon_v0_1.json"]

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
def read(name:str)->dict:
    return json.loads((E/name).read_text(encoding="utf-8"))

head=git("rev-parse","HEAD")
contract=json.loads((ROOT/CONTRACT_PATH).read_text(encoding="utf-8"))
registry=read("lane_s_evidence_registry_v0_1.json")
lineage=read("source_lineage_resolution_v0_1.json")
anchors=read("provider_primary_semantic_anchor_set_v0_1.json")
scale=read("provider_instrument_scale_authority_v0_1.json")
cp=read("provider_semantic_change_point_inventory_v0_1.json")
epoch=read("semantic_epoch_manifest_v0_1.json")
corr=read("independent_corroboration_register_v0_1.json")
sweep=read("contradiction_sweep_result_v0_1.json")
scope=read("lane_s_scope_applicability_decision_v0_1.json")
result=read("lane_s_semantic_authority_result_v0_1.json")
horizon=read("current_evidence_horizon_v0_1.json")

attacks=[]; defects=[]
def check(name:str,cond:bool,detail:str):
    attacks.append((name,"PASS" if cond else "FAIL",detail))
    if not cond: defects.append(name)

check("S01_GOVERNED_INPUT_BLOBS",
 all(blob(p)==b for p,b in [(CONTRACT_PATH,CONTRACT_BLOB),(QUAL_PATH,QUAL_BLOB),(ROUTE_PATH,ROUTE_BLOB),(BPE02_PATH,BPE02_BLOB),(BPE03_PATH,BPE03_BLOB)]),
 "B-PE-SEM-04 and inherited evidence inputs remain byte-identical")

check("S02_ALL_REQUIRED_ARTIFACTS",
 all((E/f).exists() for f in FILES),
 "all eleven Lane S outputs exist")

check("S03_SEALS_RECOMPUTE",
 registry["registry_seal"]==seal(registry,"registry_seal")
 and lineage["lineage_resolution_seal"]==seal(lineage,"lineage_resolution_seal")
 and anchors["anchor_set_seal"]==seal(anchors,"anchor_set_seal")
 and scale["scale_authority_seal"]==seal(scale,"scale_authority_seal")
 and cp["change_point_inventory_seal"]==seal(cp,"change_point_inventory_seal")
 and epoch["semantic_epoch_manifest_seal"]==seal(epoch,"semantic_epoch_manifest_seal")
 and corr["corroboration_register_seal"]==seal(corr,"corroboration_register_seal")
 and sweep["contradiction_sweep_seal"]==seal(sweep,"contradiction_sweep_seal")
 and scope["scope_decision_seal"]==seal(scope,"scope_decision_seal")
 and result["lane_s_result_seal"]==seal(result,"lane_s_result_seal")
 and horizon["evidence_horizon_seal"]==seal(horizon,"evidence_horizon_seal"),
 "all Lane S seals recompute")

slots={x["slot_id"]:x for x in result["slot_results"]}
check("S04_SIX_SLOT_BIJECTION",
 list(slots.keys())==EXPECTED_SLOTS and len(slots)==6,
 "exact six pre-registered Lane S slots are adjudicated once")

obs={x["evidence_id"]:x for x in registry["observations"]}
check("S05_LIVE_PROVIDER_NO_FAKE_IMMUTABILITY",
 obs["BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT"]["raw_provider_bytes_sha256"] is None
 and obs["BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT"]["admissibility"]=="BLOCKED_FOR_PRIMARY_AUTHORITY"
 and obs["BPESEM05-E02-DUKASCOPY-USATECH-CFD-CURRENT"]["raw_provider_bytes_sha256"] is None,
 "live provider observations are not laundered into immutable primary evidence")

check("S06_CURRENT_DAILY_NE_TARGET_K1",
 "CURRENT_DAILY_SCOPE_NE_TARGET_LEGACY_HOURLY_K1" in obs["BPESEM05-E01-DUKASCOPY-HISTORICAL-PRICE-DATA-CURRENT"]["reason_codes"]
 and slots[EXPECTED_SLOTS[0]]["status"]=="BLOCKED",
 "current daily BI5 documentation is not promoted to target legacy-hourly K1 authority")

check("S07_LEGACY_WARNING_NOT_EXACT_AUTHORITY",
 "LEGACY_HOURLY_WARNING_NONEXACT" in " ".join(slots[EXPECTED_SLOTS[0]]["reason_codes"])
 and anchors["qualified_target_primary_anchor_ids"]==[],
 "provider 'may use hour base' warning cannot become exact legacy K1 authority")

check("S08_MARKET_POINT_VALUE_NOT_RAW_DIVISOR",
 scale["forbidden_inference_applied"]=="0.01_USD_MARKET_POINT_VALUE_NOT_CONVERTED_INTO_RAW_BI5_DIVISOR"
 and scale["provider_native_bi5_raw_divisor_authority"] is None
 and scale["overall_status"]=="BLOCKED",
 "current CFD point value is not converted into native BI5 /1000 authority")

check("S09_THIRDPARTY_1000_CORROBORATION_ONLY",
 scale["third_party_corroborated_decimal_factor"]==1000
 and len(scale["third_party_evidence"])>=2
 and slots[EXPECTED_SLOTS[1]]["status"]=="BLOCKED",
 "third-party decimalFactor 1000 corroboration cannot replace provider-primary scale authority")

check("S10_PROVIDER_LINEAGE_SINGLE",
 [x for x in lineage["lineages"] if x["lineage_id"]=="LINEAGE-DUKASCOPY-OFFICIAL"][0]["independence_role"]=="ONE_PROVIDER_LINEAGE"
 and lineage["duplicate_provider_pages_count_as_multiple_independent_sources"] is False,
 "multiple provider pages are one provider lineage")

check("S11_CORROBORATION_LINEAGES_INDEPENDENT",
 corr["pair_independence_status"]=="PASS"
 and corr["entries"][0]["lineage_id"]=="LINEAGE-DUKA-DATA"
 and corr["entries"][1]["lineage_id"]=="LINEAGE-LEOCLC"
 and corr["provider_primary_substitution_allowed"] is False,
 "A/B corroboration uses distinct non-project lineages and cannot substitute for provider primary")

check("S12_NO_PROJECT_SELF_AUTHORITY",
 lineage["project_origin_used_as_independent_authority"] is False,
 "project-origin evidence is not independent semantic authority")

check("S13_JETTA_CHANGEPOINT_UNRESOLVED",
 any(x["event_id"]=="CP-2026-03-03-JETTA" and x["semantic_effect"]=="UNRESOLVED_FOR_NATIVE_K1" for x in cp["events"])
 and "CP-2026-03-03-JETTA" in epoch["unresolved_change_points"],
 "2026 JETTA backend event is retained as unresolved change point, not silently ignored")

check("S14_UNKNOWN_DAILY_HOURLY_TRANSITION",
 any(x["event_id"]=="CP-UNKNOWN-LEGACY-HOURLY-TO-DAILY" and x["time"] is None for x in cp["events"])
 and "CP-UNKNOWN-LEGACY-HOURLY-TO-DAILY" in epoch["unresolved_change_points"],
 "unknown legacy-hourly to current-daily transition remains explicit")

check("S15_RELEASE_TIMELINE_NOT_EXHAUSTIVE_CHANGELOG",
 cp["exhaustive_wire_semantic_changelog_proven"] is False
 and cp["overall_status"]=="BLOCKED",
 "provider client release timeline is not treated as exhaustive native K1 semantic changelog")

check("S16_FULL_TARGET_EPOCH_REQUIRED",
 epoch["target_start"]=="2021-08-13T01:00:00Z"
 and epoch["target_end"]=="2026-08-14T20:00:00Z"
 and epoch["full_authoritative_coverage"] is False
 and epoch["overall_status"]=="BLOCKED_UNRESOLVED_TARGET_EPOCH",
 "target epoch is exact and incomplete authority remains blocked")

check("S17_NO_TEMPORAL_EXTRAPOLATION",
 len(epoch["uncovered_authoritative_intervals"])>=1
 and scope["overall_status"]=="BLOCKED",
 "uncovered authority is not filled by forward/backward extrapolation")

check("S18_SCOPE_BLOCKS_ALL_24",
 scope["pass_count"]==0 and scope["blocked_count"]==24 and scope["fail_count"]==0
 and len(scope["decisions"])==24,
 "all 24 blocked target dimensions remain scope-blocked")

check("S19_NO_DIMENSION_PROMOTION",
 result["dimension_promotions_to_pass"]==[]
 and result["registered_target_proposition_failures"]==[]
 and result["lane_s_overall_status"]=="BLOCKED",
 "partial documentary evidence neither promotes PASS nor invents FAIL")

check("S20_CONTRADICTION_SWEEP_MATERIAL_FINDINGS",
 sweep["sweep_completeness_status"]=="PASS_FOR_DISCOVERED_MATERIAL_SOURCES"
 and sweep["substantive_authority_status"]=="BLOCKED"
 and len(sweep["material_findings"])>=3
 and sweep["positive_exact_target_scope_contradictions"]==[],
 "contradiction sweep is complete for discovered material sources but substantive authority remains blocked")

check("S21_DAILY_VS_HOURLY_FIREWALL_IN_SWEEP",
 any(x["type"]=="REGIME_SCOPE_DIFFERENCE" for x in sweep["material_findings"]),
 "daily/current versus legacy-hourly regime difference is explicitly reviewed")

check("S22_SCALE_GAP_IN_SWEEP",
 any(x["type"]=="SCALE_AUTHORITY_GAP" for x in sweep["material_findings"]),
 "provider-primary raw scale authority gap is explicit")

check("S23_REQUEST_MANIFEST_FORBIDDEN",
 result["lane_p_request_manifest_authorized"] is False
 and epoch["request_manifest_derivation_authorized"] is False,
 "Lane P RequestManifest remains unauthorized")

tracked=git("ls-files","evidence/bpesem05","reports/data-qualification/bpesem05*","tools/bpesem05*","breakers/bpesem05*")
check("S24_NO_LANE_P_OR_PROVIDER_OBJECT_ARTIFACT",
 "request_manifest" not in tracked.lower()
 and "p_diag" not in tracked.lower()
 and "provider_object" not in tracked.lower(),
 "B-PE-SEM-05 creates no Lane P RequestManifest, diagnostic or provider-object artifact")

serialized=json.dumps([registry,lineage,anchors,scale,cp,epoch,corr,sweep,scope,result,horizon],sort_keys=True)
check("S25_NO_C08_AUTHORITY_LEAKAGE",
 "C08-D" not in serialized and "BPE-SEM-C08" not in serialized,
 "Lane S package contains no C08 authority target")

check("S26_NO_PHYSICAL_HYPOTHESIS_ADJUDICATION",
 sorted(result["physical_hypothesis_dimensions_not_adjudicated_here"])==sorted(contract["dimension_population"]["blocked_physical_hypothesis"]),
 "all 11 physical hypotheses remain explicitly unadjudicated in Lane S")

check("S27_EXISTING_SIGNEDNESS_PASS_PRESERVED",
 sorted(result["existing_pass_dimensions_preserved"])==sorted(["C03-D3-OP","C05-D2-OP"]),
 "existing conditional signedness PASS dimensions are preserved, not redecided")

check("S28_EVIDENCE_HORIZON_FAIL_CLOSED",
 horizon["overall_status"]=="BLOCKED"
 and len(horizon["unresolved_required_authority"])==3,
 "current horizon enumerates the three unresolved authority classes")

check("S29_NO_BI5_OBJECT_OBSERVATION",
 registry["no_provider_object_bytes_observed"] is True and registry["no_bi5_get_performed"] is True,
 "documentary acquisition did not observe provider BI5 objects")

check("S30_GOVERNED_RESULT_BLOCKED",
 result["lane_s_overall_status"]=="BLOCKED"
 and not result["lane_p_request_manifest_authorized"],
 "B-PE-SEM-05 substantive result remains fail-closed BLOCKED")

verdict="PASS" if not defects else "FAIL"
REPORT.parent.mkdir(parents=True,exist_ok=True)
lines=["# B-PE-SEM-05 — Lane S adversarial break","",
       "Persisted candidate HEAD attacked: "+head,"",
       "Package breaker verdict: "+verdict,""]
for n,s,d in attacks:
    lines += ["## "+n,"",s+" — "+d,""]
lines += ["## Result","","~~~text",
          "attack count = "+str(len(attacks)),
          "demonstrated defects = "+str(len(defects)),
          *(defects or ["NONE"]),
          "~~~","",
          "This breaker qualifies package integrity only. It does not convert Lane S BLOCKED semantic authority into PASS.","",
          "No provider BI5 object, Lane P RequestManifest, P-DIAG, FULL_INTERVAL, D or backtest was authorized or executed.","","STOP."]
REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(json.dumps({"head":head,"verdict":verdict,"attack_count":len(attacks),"defects":defects},indent=2))
