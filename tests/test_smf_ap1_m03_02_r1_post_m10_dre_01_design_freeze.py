from __future__ import annotations
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"

PATHS={
 "auth":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-HUMAN-AUTHORIZATION-RECEIPT-V0.1.json",
 "binding":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-DATA-PAYLOAD-BINDING-V0.1.json",
 "contract":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-EXECUTION-CONTRACT-V0.1.json",
 "schema":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-OUTPUT-SCHEMA-V0.1.json",
 "breakers":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-FROZEN-BREAKER-CONTRACT-V0.1.json",
 "trace":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-REQUIREMENTS-PROVENANCE-TRACEABILITY-V0.1.json",
 "freeze":"GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DRE-01-PRE-EXECUTION-FREEZE-V0.1.json",
}
EXPECTED={
 "auth":"cb7b39ba9cdfd08b366368fa33cc4d2d28eb2e02",
 "binding":"efd7ba2e1f822a0bc1e4b444bb1cac33117ae12f",
 "contract":"26889ea08b1bb4e4aebac953ed37e4c4425446bf",
 "schema":"3a58e3a41a8cf9f68994bd165edd4a98f0cec161",
 "breakers":"ba80d33d36fef04a556d9c4e596d46eb9cfdf90e",
 "trace":"442e810db71ebe6a174ca100c96ee730cdf109d9",
 "freeze":"19d5d5fd01baf577853cc7086d426da1448387dc",
}

def load(key):
    return json.loads((ROOT/PATHS[key]).read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def test_01_exact_design_blobs():
    for key,path in PATHS.items():
        assert blob(path)==EXPECTED[key]

def test_02_control_id_consistent():
    for key in PATHS:
        assert load(key)["control_id"]=="SMF-AP1-M03-02-R1-POST-M10-DRE-01"

def test_03_design_only_not_execution_authority():
    a=load("auth")
    assert a["authorization_scope"]=="DESIGN_FREEZE_ONLY"
    assert a["separate_execution_authorization_required"] is True
    assert a["automatic_execution"] is False

def test_04_exact_source_payload_binding():
    b=load("binding")["frozen_real_source_payload"]
    assert b["required_sha256"]=="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
    assert b["expected_schema"]=="ATDS_SMF_AP1_M03_02_REAL_EXECUTION_V0_1"
    assert b["expected_status"]=="M03_REAL_EXECUTION_COMPLETE"
    assert b["read_authorized_under_dre01_design_freeze"] is False

def test_05_exact_dataset_lineage():
    s=load("binding")["source_lineage"]
    assert s["dataset_identity"]=="USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert s["ap0_manifest_sha256"]=="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"
    assert s["expected_ap0_files"]==61
    assert s["expected_ap0_minutes"]==1709180
    assert s["raw_ap0_read_in_future_dre_execution"] is False

def test_06_exact_m03_procedure_binding():
    m=load("binding")["m03_procedure_bindings"]
    assert m["procedure_ref"]=="gitblob:b67d63bbbc4f93be3fe1e7327c1f1f1cc440ebeb#ecdf_quantiles"
    assert m["quantile_definition"]=="linear interpolation with h=(n-1)*p"
    assert m["tail_extrapolation"]=="FORBIDDEN"
    assert m["metric"]=="tick_count"
    assert m["required_probability"]==0.5

def test_07_exact_four_ordered_buckets():
    e=load("binding")["extraction_bindings"]
    assert e["ordered_bucket_ids"]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert e["metric_key"]=="tick_count"
    assert e["p50_key"]=="0.5"

def test_08_contract_is_extraction_not_recomputation():
    p=load("contract")["p50_procedure"]
    assert p["future_dre_operation"]=="EXTRACT_EXISTING_P50_ONLY"
    assert p["recompute_quantile_from_observations"] is False
    assert p["interpolate_again"] is False
    assert p["round_value"] is False
    assert p["integer_cast"] is False
    assert p["transform_value"] is False

def test_09_strata_are_half_open_and_fixed():
    s=load("contract")["strata_implementation"]
    assert s["implementation_mode"]=="EXACT_FROZEN_M03_BUCKET_ID_SELECTION"
    assert s["dre01_recomputes_timestamp_membership"] is False
    assert [x["id"] for x in s["ordered_strata"]]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert all(x["interval"]=="[START,END)" for x in s["ordered_strata"])

def test_10_validation_fail_closed():
    c=load("contract")
    assert c["fail_closed_behavior"]["any_required_component_invalid"]=="BLOCK_WHOLE_EXECUTION"
    assert c["fail_closed_behavior"]["partial_vector_output"]=="FORBIDDEN"
    assert c["fail_closed_behavior"]["imputation"]=="FORBIDDEN"
    assert c["fail_closed_behavior"]["alternate_source_fallback"]=="FORBIDDEN"

def test_11_determinism_exact():
    d=load("contract")["determinism"]
    assert d["fixed_component_order"]==["R_2022","R_2023","R_2024","R_2025"]
    assert d["random_state"]=="NONE"
    assert d["wall_clock_in_scientific_result"] is False
    assert d["locale_dependency"] is False
    assert d["timezone_conversion_during_dre"] is False
    assert d["primary_reference_object_parity"]=="EXACT_REQUIRED"
    assert d["primary_reference_canonical_byte_parity"]=="EXACT_REQUIRED"

def test_12_future_execution_budget_frozen():
    b=load("contract")["future_execution_budget"]
    assert b=={
      "primary_execution_count":1,
      "independent_reference_execution_count":1,
      "retry_count":0,
      "automatic_retry":False,
    }

def test_13_output_has_exact_vector_semantics():
    s=load("schema")
    assert s["success_object"]["vector_order"]==["R_2022","R_2023","R_2024","R_2025"]
    assert s["success_object"]["fixed_values"]["aggregation"]=="NONE"
    assert s["success_object"]["components"]["type"]=="ARRAY_EXACT_LENGTH_4"
    assert s["success_object"]["scientific_result_timestamp"] is False

def test_14_blocked_output_has_no_numbers():
    b=load("schema")["blocked_object"]
    assert b["status"]=="DRE01_BLOCKED"
    assert b["numerical_components"]=="FORBIDDEN"
    assert b["partial_values"]=="FORBIDDEN"

def test_15_breaker_count_and_uniqueness():
    b=load("breakers")
    assert b["breaker_count"]==69
    assert len(b["breakers"])==69
    ids=[x[0] for x in b["breakers"]]
    assert len(ids)==len(set(ids))

def test_16_breakers_preserve_authority_ceiling():
    a=load("breakers")["authority_ceiling"]
    assert a["design_freeze"] is True
    assert all(v is False for k,v in a.items() if k!="design_freeze")

def test_17_freeze_binds_all_design_blobs():
    f=load("freeze")["frozen_design_blobs"]
    assert f["human_authorization_receipt"]==EXPECTED["auth"]
    assert f["data_payload_binding"]==EXPECTED["binding"]
    assert f["execution_contract"]==EXPECTED["contract"]
    assert f["output_schema"]==EXPECTED["schema"]
    assert f["breaker_contract"]==EXPECTED["breakers"]
    assert f["requirements_provenance_traceability"]==EXPECTED["trace"]

def test_18_freeze_exact_source():
    s=load("freeze")["frozen_source"]
    assert s["sha256"]=="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
    assert s["dataset_identity"]=="USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert s["ap0_manifest_sha256"]=="62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"

def test_19_freeze_exact_extraction():
    e=load("freeze")["frozen_extraction"]
    assert [x["id"] for x in e["ordered_components"]]==["R_2022","R_2023","R_2024","R_2025"]
    assert all(x["metric"]=="tick_count" and x["probability_key"]=="0.5" for x in e["ordered_components"])
    assert e["operation"]=="EXTRACT_EXISTING_M03_P50_WITHOUT_RECOMPUTATION"
    assert e["whole_vector_atomic"] is True
    assert e["partial_vector"] is False

def test_20_freeze_stops_execution():
    f=load("freeze")
    assert f["execution_authorized"] is False
    assert f["separate_human_execution_authorization_required"] is True
    assert f["automatic_open"] is False
    assert f["automatic_execution"] is False
    assert f["stop"] is True
    assert f["force"] is False

def test_21_epistemic_state_preserved():
    e=load("freeze")["epistemic_state"]
    assert e=={
      "evidence_state":"EXPOSED",
      "claim_provenance":"RESULT_AWARE",
      "same_corpus_confirmatory_status":"NON_PRISTINE",
      "reset_to_pristine":"FORBIDDEN",
    }

def test_22_methods_remain_closed():
    assert load("freeze")["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}

def test_23_traceability_covers_all_breakers():
    t=load("trace")["requirement_map"]
    covered={bid for row in t for bid in row["breakers"]}
    expected={f"DRE01-B{i:02d}" for i in range(1,70)}
    assert covered==expected

def test_24_no_runtime_or_result_artifact_is_created_by_design():
    assert not list((ROOT/"tools").glob("*dre_01*"))
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*dre_01*"))
        assert not list(art.glob("*DRE-01*"))
