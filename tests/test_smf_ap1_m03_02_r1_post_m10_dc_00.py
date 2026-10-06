from __future__ import annotations
import ast
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"
CLAIM=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-00-DOWNSTREAM-CLAIM-CONTRACT-V0.1.json"
EST=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-00-ESTIMAND-CONTRACT-V0.1.json"
INTENT=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-00-ANALYSIS-INTENT-CONTRACT-V0.1.json"
BREAK=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-00-FROZEN-BREAKER-CONTRACT-V0.1.json"
TRACE=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-00-REQUIREMENTS-PROVENANCE-TRACEABILITY-V0.1.json"

EXPECTED={
 "m01":"2293c665a2d30c520056c7814aec6a9dc79d68d1",
 "m10_receipt":"899d0e6d27920dccfc260de0c30646d9e5ee8c53",
 "m10_closure":"1664e786e65a68cf77370afc7cc933b34958133a",
 "post_m10":"aeed65dd6853392168aa97432ebadb1f9ea48e46",
 "pcg00":"8e6e888f8330e40d792b43650c32b09a8dc6a281",
 "pcg01_runtime":"2b4b96b755293c47efa89522e5509bda4f0c9c73",
 "pcg01_reference":"6567e3d7325bfa769e10bc5bf1497b6aa416e3ce",
 "pcg01_breaker":"82362c52e52da84d251faeaa12d943d3c236b8b5",
 "pcg01_fixture":"4695450cbeb13b695de649e84b853967b07334c7",
 "pcg01_receipt":"c0987d858d30ba05587e94f0287982270d9b5cc2",
 "pcg01_closure":"ab207ff4b2c36aeb5b315e3260855be1f7a54030",
}

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def test_01_exact_canonical_bindings():
    c=load(CLAIM)["binding_sources"]
    assert c["m01_temporal_stability_contract_blob"]==EXPECTED["m01"]
    assert c["m10_01_final_receipt_blob"]==EXPECTED["m10_receipt"]
    assert c["m10_01_final_closure_blob"]==EXPECTED["m10_closure"]
    assert c["post_m10_method_necessity_adjudication_blob"]==EXPECTED["post_m10"]
    assert c["pcg00_contract_blob"]==EXPECTED["pcg00"]
    assert c["pcg01_runtime_blob"]==EXPECTED["pcg01_runtime"]
    assert c["pcg01_reference_blob"]==EXPECTED["pcg01_reference"]
    assert c["pcg01_breaker_blob"]==EXPECTED["pcg01_breaker"]
    assert c["pcg01_fixture_blob"]==EXPECTED["pcg01_fixture"]
    assert c["pcg01_final_receipt_blob"]==EXPECTED["pcg01_receipt"]
    assert c["pcg01_final_closure_blob"]==EXPECTED["pcg01_closure"]

def test_02_current_repository_objects_match_bindings():
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.2.json")==EXPECTED["m01"]
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-M10-01-FINAL-EXECUTION-RECEIPT-V0.1.json")==EXPECTED["m10_receipt"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-METHOD-NECESSITY-HUMAN-ADJUDICATION-2026-10-06.md")==EXPECTED["post_m10"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-00-CONTRACT-V0.1.json")==EXPECTED["pcg00"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED["pcg01_runtime"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED["pcg01_reference"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json")==EXPECTED["pcg01_breaker"]

def test_03_claim_selection_is_exact_and_non_posthoc():
    s=load(CLAIM)["selection"]
    assert s["claim_unit"]=="tick_count p50"
    assert s["m10_status"]=="MATERIAL_TEMPORAL_VARIATION"
    assert s["basis"]=="FIRST_MATERIAL_CLAIM_UNIT_IN_FROZEN_CANONICAL_M10_ORDER"
    assert all(s[k] is False for k in ("by_effect_magnitude","by_profitability","by_predictive_interest","by_extremeness","by_convenience"))

def test_04_downstream_claim_is_frozen_but_unresolved():
    d=load(CLAIM)["downstream_claim"]
    assert d["id"]=="POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert d["claim_class"]=="DESCRIPTIVE_GOVERNANCE_DEPENDENT"
    assert d["claim_origin"]=="POST_M10_DOWNSTREAM_DESIGN"
    assert d["admissibility"]=="UNRESOLVED_PENDING_PCG"

def test_05_estimand_semantics_only_no_numeric_estimation():
    e=load(EST)
    assert e["estimand_id"]=="POST_M10-E01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert e["metric"]=="tick_count"
    assert e["probability"]=="p50"
    assert e["observational_unit"]=="ONE_ADMITTED_AP0_MINUTE"
    assert e["requested_temporal_scope"]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert e["excluded_partial_years"]==["UTC_YEAR:2021","UTC_YEAR:2026"]
    assert e["estimand_semantics"]=="FROZEN"
    assert e["numerical_estimation"] is False
    assert e["real_data_read"] is False

def test_06_pooling_intent_does_not_create_admissibility_or_execution():
    i=load(INTENT)
    assert i["pooling_intent"] is True
    assert i["pooling_admissibility"]=="UNRESOLVED_PENDING_PCG"
    assert i["pooling_execution"] is False
    assert i["conditioning_execution"] is False

def test_07_no_route_is_selected():
    i=load(INTENT)
    assert i["route_selection"]=="NONE"
    assert i["route_a_selected"] is False
    assert i["route_b_selected"] is False
    assert i["route_c_selected"] is False
    assert i["requested_route_for_pcg"]=="NOT_YET_FROZEN"

def test_08_no_existing_route_basis_is_promoted():
    k=load(INTENT)["known_route_state"]
    assert k["human_adopted_pooling_justification"]=="NONE_IDENTIFIED"
    assert k["frozen_temporal_conditioning_spec"]=="NONE_IDENTIFIED"
    assert k["qualified_robust_method_preregistration"]=="NONE_IDENTIFIED"

def test_09_evidence_state_and_epistemic_limits_are_preserved():
    e=load(CLAIM)["epistemic_status"]
    assert e["evidence_state"]=="EXPOSED"
    assert e["claim_provenance"]=="RESULT_AWARE"
    assert e["same_corpus_confirmatory_status"]=="NON_PRISTINE"
    assert e["reset_to_pristine"]=="FORBIDDEN"

def test_10_m10_relation_is_exact_and_non_promotional():
    r=load(CLAIM)["m10_relation"]
    assert r["finding"]=="MATERIAL_TEMPORAL_VARIATION"
    assert r["implication"]=="UNCONDITIONAL_TEMPORAL_POOLING_CANNOT_BE_ASSUMED_HARMLESS"
    assert set(r["does_not_imply"])=={"POOLING_IMPOSSIBLE","CONDITIONING_REQUIRED","ROBUST_METHOD_REQUIRED"}

def test_11_methods_and_authority_remain_closed():
    c=load(CLAIM)
    assert c["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert c["global_m05_resampling_across_2022_2025"]=="BLOCKED_PENDING_TEMPORAL_JUSTIFICATION"
    assert all(v is False for v in c["authority"].values())

def test_12_breaker_contract_has_required_surface():
    b=load(BREAK)
    ids=[x[0] for x in b["breakers"]]
    assert ids[:34]==[f"DC00-B{i:02d}" for i in range(1,35)]
    assert b["minimum_required_breaker_count"]==34
    assert b["breaker_count"]==36
    assert b["runtime_authorized"] is False
    assert b["real_data_read_authorized"] is False
    assert b["pcg_execution_authorized"] is False
    assert b["method_execution_authorized"] is False

def test_13_traceability_covers_every_breaker():
    breakers={x[0] for x in load(BREAK)["breakers"]}
    mapped={x for row in load(TRACE)["requirement_map"] for x in row["breakers"]}
    assert breakers <= mapped

def test_14_provenance_labels_are_explicit():
    t=load(TRACE)
    assert set(t["provenance_labels"])=={"CANONICAL_FACT","HUMAN_DECISION","DERIVED_GOVERNANCE_INPUT"}
    for item in t["material_fields"].values():
        assert item["provenance"] in t["provenance_labels"]

def test_15_dc00_has_no_runtime_or_artifact_surface():
    assert not list((ROOT/"tools").glob("*post_m10_dc_00*"))
    assert not list((ROOT/"artifacts").glob("*dc_00*"))
    assert not list((ROOT/"artifacts").glob("*DC-00*"))

def test_16_dc00_tests_do_not_import_or_call_pcg_runtime():
    src=Path(__file__).read_text(encoding="utf-8")
    tree=ast.parse(src)
    imports=[]
    call_names=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            imports += [a.name for a in n.names]
        if isinstance(n,ast.ImportFrom) and n.module:
            imports.append(n.module)
        if isinstance(n,ast.Call):
            f=n.func
            if isinstance(f,ast.Name):
                call_names.append(f.id)
            elif isinstance(f,ast.Attribute):
                call_names.append(f.attr)
    assert not any("pcg_01" in x for x in imports)
    assert not ({"evaluate","reference_evaluate","load_module"} & set(call_names))

def test_17_pcg02a_remains_closed():
    i=load(INTENT)["relation_to_pcg"]
    assert i["next_packet_phase"]=="PCG-02A"
    assert i["create_pcg_application_packet"] is False
    assert i["call_pcg_runtime"] is False
    assert i["call_pcg_reference"] is False
    assert i["compute_pcg_state"] is False
