from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATHS={
 "auth":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-HUMAN-AUTHORIZATION-RECEIPT-V0.1.json",
 "binding":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-DATA-PAYLOAD-BINDING-V0.1.json",
 "contract":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-EXECUTION-CONTRACT-V0.1.json",
 "schema_v1":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-OUTPUT-SCHEMA-V0.1.json",
 "cr1":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-CR1-CORRECTION-RECORD-V0.1.json",
 "schema":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-OUTPUT-SCHEMA-V0.2.json",
 "breakers":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-FROZEN-BREAKER-CONTRACT-V0.1.json",
 "trace":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-REQUIREMENTS-PROVENANCE-TRACEABILITY-V0.1.json",
 "freeze_v1":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-PRE-EXECUTION-FREEZE-V0.1.json",
 "freeze":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-PRE-EXECUTION-FREEZE-V0.2.json",
}
EXPECTED={
 "auth":"cb7b39ba9cdfd08b366368fa33cc4d2d28eb2e02",
 "binding":"efd7ba2e1f822a0bc1e4b444bb1cac33117ae12f",
 "contract":"26889ea08b1bb4e4aebac953ed37e4c4425446bf",
 "schema_v1":"3a58e3a41a8cf9f68994bd165edd4a98f0cec161",
 "cr1":"3f44dd44002c9e12abb490a260e861c228468ed4",
 "schema":"8f3224b7aff804b1e9ce3776e552f8b2d60ae40d",
 "breakers":"ba80d33d36fef04a556d9c4e596d46eb9cfdf90e",
 "trace":"442e810db71ebe6a174ca100c96ee730cdf109d9",
 "freeze_v1":"19d5d5fd01baf577853cc7086d426da1448387dc",
}
def load(k): return json.loads((ROOT/PATHS[k]).read_text(encoding="utf-8"))
def blob(p): return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{p}"],text=True).strip()

def test_01_exact_frozen_source_artifacts():
    for k in ("auth","binding","contract","schema_v1","cr1","schema","breakers","trace","freeze_v1"):
        assert blob(PATHS[k])==EXPECTED[k]

def test_02_cr1_is_identity_only():
    c=load("cr1")
    assert c["classification"]=="IDENTITY_ENCODING_CORRECTION_ONLY"
    assert c["semantic_effect"]=="NONE"
    assert c["algorithm_effect"]=="NONE"
    assert c["source_binding_effect"]=="NONE"
    assert c["breaker_weakening"] is False

def test_03_schema_v2_has_exact_canonical_estimand_id():
    s=load("schema")
    assert s["success_object"]["fixed_values"]["estimand_id"]=="POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert s["supersedes"]["blob"]==EXPECTED["schema_v1"]

def test_04_design_only_authority():
    a=load("auth")
    assert a["authorization_scope"]=="DESIGN_FREEZE_ONLY"
    assert a["separate_execution_authorization_required"] is True
    assert a["automatic_execution"] is False

def test_05_source_payload_exact():
    b=load("binding")["frozen_real_source_payload"]
    assert b["required_sha256"]=="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
    assert b["expected_schema"]=="ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
    assert b["expected_status"]=="M03_REAL_EXECUTION_COMPLETE"
    assert b["read_authorized_under_dre01_design_freeze"] is False

def test_06_dataset_lineage_exact():
    s=load("binding")["source_lineage"]
    assert s["dataset_identity"]=="USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert s["ap0_manifest_sha256"]=="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert s["expected_ap0_files"]==61
    assert s["expected_ap0_minutes"]==1709180
    assert s["raw_ap0_read_in_future_dre_execution"] is False

def test_07_p50_is_extraction_not_recomputation():
    p=load("contract")["p50_procedure"]
    assert p["future_dre_operation"]=="EXTRACT_EXISTING_P50_ONLY"
    assert p["source_quantile_key"]=="0.5"
    assert p["recompute_quantile_from_observations"] is False
    assert p["interpolate_again"] is False
    assert p["round_value"] is False
    assert p["integer_cast"] is False
    assert p["normalize_value"] is False
    assert p["transform_value"] is False

def test_08_exact_year_strata():
    s=load("contract")["strata_implementation"]
    assert s["implementation_mode"]=="EXACT_FROZEN_M03_BUCKET_ID_SELECTION"
    assert s["dre01_recomputes_timestamp_membership"] is False
    assert [x["id"] for x in s["ordered_strata"]]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert all(x["interval"]=="[START,END)" for x in s["ordered_strata"])
    assert s["excluded_partial_years"]==["UTC_YEAR:2021","UTC_YEAR:2026"]

def test_09_fail_closed_atomic_vector():
    f=load("contract")["fail_closed_behavior"]
    assert f["any_required_component_invalid"]=="BLOCK_WHOLE_EXECUTION"
    assert f["partial_vector_output"]=="FORBIDDEN"
    assert f["imputation"]=="FORBIDDEN"
    assert f["adjacent_year_borrowing"]=="FORBIDDEN"
    assert f["alternate_source_fallback"]=="FORBIDDEN"

def test_10_determinism():
    d=load("contract")["determinism"]
    assert d["fixed_component_order"]==["R_2022","R_2023","R_2024","R_2025"]
    assert d["random_state"]=="NONE"
    assert d["wall_clock_in_scientific_result"] is False
    assert d["locale_dependency"] is False
    assert d["timezone_conversion_during_dre"] is False
    assert d["filesystem_iteration_dependency"] is False
    assert d["primary_reference_object_parity"]=="EXACT_REQUIRED"
    assert d["primary_reference_canonical_byte_parity"]=="EXACT_REQUIRED"

def test_11_future_budget():
    assert load("contract")["future_execution_budget"]=={
      "primary_execution_count":1,
      "independent_reference_execution_count":1,
      "retry_count":0,
      "automatic_retry":False,
    }

def test_12_output_schema_exact():
    s=load("schema")["success_object"]
    assert s["fixed_values"]["claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert s["fixed_values"]["estimand_id"]=="POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert s["fixed_values"]["analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert s["vector_order"]==["R_2022","R_2023","R_2024","R_2025"]
    assert s["fixed_values"]["aggregation"]=="NONE"
    assert s["scientific_result_timestamp"] is False

def test_13_blocked_output_contains_no_partial_numbers():
    b=load("schema")["blocked_object"]
    assert b["numerical_components"]=="FORBIDDEN"
    assert b["partial_values"]=="FORBIDDEN"

def test_14_breaker_contract_complete():
    b=load("breakers")
    assert b["breaker_count"]==69
    ids=[x[0] for x in b["breakers"]]
    assert ids==[f"DRE01-B{i:02d}" for i in range(1,70)]

def test_15_traceability_covers_all_breakers():
    covered={bid for row in load("trace")["requirement_map"] for bid in row["breakers"]}
    assert covered=={f"DRE01-B{i:02d}" for i in range(1,70)}

def test_16_freeze_v2_supersedes_v1_and_binds_schema_v2():
    f=load("freeze")
    assert f["supersedes"]["blob"]==EXPECTED["freeze_v1"]
    assert f["correction_record_blob"]==EXPECTED["cr1"]
    assert f["frozen_design_blobs"]["output_schema"]==EXPECTED["schema"]
    assert f["frozen_output"]["output_schema_blob"]==EXPECTED["schema"]

def test_17_freeze_v2_exact_scientific_ids():
    o=load("freeze")["frozen_output"]
    assert o["claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert o["estimand_id"]=="POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert o["analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"

def test_18_freeze_v2_exact_source_and_operation():
    f=load("freeze")
    assert f["frozen_source"]["sha256"]=="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
    assert f["frozen_source"]["dataset_identity"]=="USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert f["frozen_extraction"]["operation"]=="EXTRACT_EXISTING_M03_P50_WITHOUT_RECOMPUTATION"
    assert f["frozen_extraction"]["whole_vector_atomic"] is True
    assert f["frozen_extraction"]["partial_vector"] is False

def test_19_freeze_v2_stops_before_execution():
    f=load("freeze")
    assert f["execution_authorized"] is False
    assert f["separate_human_execution_authorization_required"] is True
    assert f["automatic_open"] is False
    assert f["automatic_execution"] is False
    assert f["stop"] is True
    assert f["force"] is False

def test_20_epistemic_and_methods_preserved():
    f=load("freeze")
    assert f["epistemic_state"]=={
      "evidence_state":"EXPOSED","claim_provenance":"RESULT_AWARE",
      "same_corpus_confirmatory_status":"NON_PRISTINE","reset_to_pristine":"FORBIDDEN"}
    assert f["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}

def test_21_no_execution_surface_created():
    assert not list((ROOT/"tools").glob("*dre_01*"))
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*dre_01*"))
        assert not list(art.glob("*DRE-01*"))
