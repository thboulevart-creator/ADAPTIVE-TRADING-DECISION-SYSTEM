from __future__ import annotations
import ast
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"

CLAIM=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-CONDITIONED-DOWNSTREAM-CLAIM-CONTRACT-V0.1.json"
EST=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-CONDITIONED-ESTIMAND-CONTRACT-V0.1.json"
SPEC=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-YEAR-STRATA-TEMPORAL-CONDITIONING-SPEC-V0.1.json"
INTENT=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-ANALYSIS-INTENT-CONTRACT-V0.1.json"
BREAKERS=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-FROZEN-BREAKER-CONTRACT-V0.1.json"
TRACE=GOV/"SMF-AP1-M03-02-R1-POST-M10-DC-01-REQUIREMENTS-PROVENANCE-TRACEABILITY-V0.1.json"

EXPECTED_PCG02C={
 "adj":"2534e5d710e0242060c98d4e3f32beabbc01d16b",
 "receipt":"9efe330d11f09671e71a79978026e33f105794bf",
 "closure":"09a8c552b6613de1d1c9849e487bba75a3580498",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def dt(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def test_01_exact_pcg02c_bindings():
    c=load(CLAIM)["pcg02c_bindings"]
    assert c["human_adjudication_blob"]==EXPECTED_PCG02C["adj"]
    assert c["human_adoption_receipt_blob"]==EXPECTED_PCG02C["receipt"]
    assert c["final_closure_blob"]==EXPECTED_PCG02C["closure"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-02C-HUMAN-ADJUDICATION-2026-10-06.md")==EXPECTED_PCG02C["adj"]
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02C-HUMAN-ADOPTION-RECEIPT-V0.1.json")==EXPECTED_PCG02C["receipt"]
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02C-FINAL-CLOSURE.md")==EXPECTED_PCG02C["closure"]

def test_02_old_pooled_claim_is_preserved_blocked():
    p=load(CLAIM)["prior_pooled_claim"]
    assert p["downstream_claim_id"]=="POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert p["status"]=="PRESERVED_AS_BLOCKED"
    assert p["semantic_rewrite"]=="FORBIDDEN"

def test_03_new_claim_identity_is_distinct_and_exact():
    c=load(CLAIM)
    assert c["claim_unit"]=="tick_count p50"
    assert c["m10_status"]=="MATERIAL_TEMPORAL_VARIATION"
    assert c["downstream_claim"]["id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert c["downstream_claim"]["claim_class"]=="DESCRIPTIVE_TEMPORALLY_CONDITIONED"
    assert c["downstream_claim"]["claim_origin"]=="POST_M10_RESULT_AWARE_DOWNSTREAM_DESIGN"

def test_04_claim_has_no_scientific_promotion():
    c=load(CLAIM)
    assert c["downstream_claim"]["answer_at_dc01"]=="NOT_ESTABLISHED"
    assert set(c["excluded_claim_classes"])=={"CONFIRMATORY","PREDICTIVE","CAUSAL","PROFITABILITY","STRATEGY_VALIDATION","TRADING_SIGNAL"}

def test_05_estimand_is_four_component_vector():
    e=load(EST)
    assert e["estimand_id"]=="POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert e["metric"]=="tick_count"
    assert e["probability"]=="p50"
    assert e["observational_unit"]=="ONE_ADMITTED_AP0_MINUTE"
    assert [x["id"] for x in e["components"]]==["R_2022","R_2023","R_2024","R_2025"]
    assert all(x["value"]=="NOT_ESTIMATED" for x in e["components"])

def test_06_symbolic_estimands_are_exact():
    e=load(EST)
    defs=[x["symbolic_definition"] for x in e["components"]]
    assert defs==[
      "p50(tick_count | UTC_YEAR = 2022)",
      "p50(tick_count | UTC_YEAR = 2023)",
      "p50(tick_count | UTC_YEAR = 2024)",
      "p50(tick_count | UTC_YEAR = 2025)",
    ]

def test_07_cross_year_aggregation_is_forbidden():
    e=load(EST)
    assert e["relation_between_components"]=="A_CONDITIONED_REFERENCE_VECTOR"
    assert set(e["forbidden_aggregations"])=={
      "MEAN_OF_YEAR_REFERENCES","WEIGHTED_MEAN_OF_YEAR_REFERENCES",
      "MEDIAN_OF_YEAR_MEDIANS","POOLED_RECOMPOSITION","GLOBAL_2022_2025_REFERENCE"
    }

def test_08_conditioning_spec_identity_and_route_are_exact():
    s=load(SPEC)
    assert s["temporal_conditioning_spec_id"]=="POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
    assert s["spec_type"]=="YEAR_STRATA"
    assert s["route_mapping"]=={"pcg_route":"B","semantics":"CONDITION_OR_STRATIFY_BY_TIME"}

def test_09_exactly_four_year_strata():
    s=load(SPEC)
    assert [x["id"] for x in s["strata"]]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert len(s["strata"])==4

def test_10_half_open_utc_boundaries_are_exact_and_contiguous():
    strata=load(SPEC)["strata"]
    expected=[
      ("2022-01-01T00:00:00Z","2023-01-01T00:00:00Z"),
      ("2023-01-01T00:00:00Z","2024-01-01T00:00:00Z"),
      ("2024-01-01T00:00:00Z","2025-01-01T00:00:00Z"),
      ("2025-01-01T00:00:00Z","2026-01-01T00:00:00Z"),
    ]
    for x,(start,end) in zip(strata,expected):
        assert x["start_utc"]==start and x["end_utc"]==end
        assert x["start_inclusive"] is True and x["end_exclusive"] is True
        assert dt(x["start_utc"]).tzinfo==timezone.utc
        assert dt(x["end_utc"]).tzinfo==timezone.utc
    for a,b in zip(strata,strata[1:]):
        assert a["end_utc"]==b["start_utc"]

def test_11_membership_rules_are_fail_closed():
    s=load(SPEC)
    assert s["timezone"]=="UTC"
    assert s["membership_source"]=="ADMITTED_AP0_MINUTE_UTC_TIMESTAMP"
    assert s["membership_rule"]=="EACH_ADMITTED_MINUTE_MUST_BELONG_TO_EXACTLY_ONE_YEAR_STRATUM_OR_TO_NONE"
    assert all(v is False for v in s["constraints"].values())

def test_12_partial_years_are_excluded():
    s=load(SPEC)
    assert s["outside_scope"]=={
      "UTC_YEAR:2021":"EXCLUDED_PARTIAL_YEAR",
      "UTC_YEAR:2026":"EXCLUDED_PARTIAL_YEAR",
    }
    assert s["real_completeness_recomputation"] is False

def test_13_missing_data_policy_has_no_imputation():
    s=load(SPEC)
    assert s["missing_observation_policy"]=="NO_IMPUTATION_BY_DC_01"
    assert set(s["forbidden_missing_data_operations"])=={
      "FORWARD_FILL","BACKWARD_FILL","CROSS_YEAR_IMPUTATION",
      "SYNTHETIC_MINUTE_CREATION","YEAR_LEVEL_VALUE_SUBSTITUTION"
    }

def test_14_route_b_is_not_yet_admissible():
    s=load(SPEC)
    i=load(INTENT)
    assert s["route_b_admissible"]=="NOT_YET_ESTABLISHED"
    assert i["route_b_status"]["route_b_admissible"]=="NOT_YET_ESTABLISHED"
    assert s["conditioning_execution"] is False
    assert s["year_stratified_estimation"] is False

def test_15_analysis_identity_is_exact():
    i=load(INTENT)
    assert i["downstream_analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert i["downstream_claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert i["estimand_id"]=="POST_M10-E02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert i["temporal_conditioning_spec_id"]=="POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"

def test_16_no_real_execution_or_estimation_authority():
    c=load(CLAIM)["authority"]
    i=load(INTENT)["execution_state"]
    assert c["conditioning_spec_design"] is True
    assert all(v is False for k,v in c.items() if k!="conditioning_spec_design")
    assert all(v is False for v in i.values())

def test_17_epistemic_state_is_preserved():
    e=load(CLAIM)["epistemic_status"]
    assert e=={
      "evidence_state":"EXPOSED",
      "claim_provenance":"RESULT_AWARE",
      "same_corpus_confirmatory_status":"NON_PRISTINE",
      "reset_to_pristine":"FORBIDDEN"
    }

def test_18_breaker_contract_contains_exact_required_surface():
    b=load(BREAKERS)
    ids=[x[0] for x in b["breakers"]]
    assert b["minimum_required_breaker_count"]==42
    assert b["breaker_count"]==42
    assert ids==[f"DC01-B{i:02d}" for i in range(1,43)]

def test_19_method_state_remains_closed():
    b=load(BREAKERS)
    assert b["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert b["global_m05_resampling_across_2022_2025"]=="BLOCKED_PENDING_TEMPORAL_JUSTIFICATION"

def test_20_breaker_authority_ceiling_is_exact():
    a=load(BREAKERS)["authority_ceiling"]
    assert a["conditioning_spec_design"] is True
    assert all(v is False for k,v in a.items() if k!="conditioning_spec_design")
    assert load(BREAKERS)["runtime_authorized"] is False
    assert load(BREAKERS)["real_data_read_authorized"] is False
    assert load(BREAKERS)["pcg_real_execution_authorized"] is False

def test_21_traceability_covers_all_breakers():
    b={x[0] for x in load(BREAKERS)["breakers"]}
    mapped={x for row in load(TRACE)["requirement_map"] for x in row["breakers"]}
    assert b==mapped

def test_22_material_fields_have_explicit_provenance():
    t=load(TRACE)
    allowed=set(t["provenance_labels"])|{"CANONICAL_FACT/HUMAN_ADOPTED_GOVERNANCE_RESULT"}
    for field in t["material_fields"].values():
        assert field["provenance"] in allowed

def test_23_no_dc01_runtime_or_data_artifact_surface():
    assert not list((ROOT/"tools").glob("*post_m10_dc_01*"))
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*dc_01*"))
        assert not list(art.glob("*DC-01*"))

def test_24_test_does_not_import_or_call_real_execution_surfaces():
    src=Path(__file__).read_text(encoding="utf-8")
    tree=ast.parse(src)
    imports=[]
    calls=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):
            imports.extend(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom) and node.module:
            imports.append(node.module)
        elif isinstance(node,ast.Call):
            if isinstance(node.func,ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func,ast.Attribute):
                calls.append(node.func.attr)
    assert not any("pcg_01" in x for x in imports)
    assert not ({"evaluate","reference_evaluate","load_module"} & set(calls))

def test_25_next_pcg_route_b_application_remains_closed():
    i=load(INTENT)["next_gate_application"]
    assert i["separate_human_authorization_required"] is True
    assert i["open"] is False


FINAL_RECEIPT=ROOT/"reports"/"program"/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-READINESS-RECEIPT-V0.1.json"
FINAL_CLOSURE=ROOT/"reports"/"program"/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-CLOSURE.md"

def test_26_final_receipt_preserves_dc01_authority_ceiling():
    r=load(FINAL_RECEIPT)
    v=r["verdict"]
    assert r["status"]=="QUALIFIED_AND_FROZEN_READY_FOR_SEPARATE_ROUTE_B_PCG_APPLICATION_DECISION"
    assert v["POST_M10_DC_01"]=="QUALIFIED"
    assert v["CONDITIONED_DOWNSTREAM_CLAIM"]=="FROZEN"
    assert v["CONDITIONED_ESTIMAND"]=="FROZEN"
    assert v["YEAR_STRATA_CONDITIONING_SPEC"]=="QUALIFIED_AND_FROZEN"
    assert v["ROUTE_B_ADMISSIBLE"]=="NOT_YET_ESTABLISHED"
    assert v["CONDITIONING_EXECUTION"] is False
    assert v["YEAR_STRATIFIED_ESTIMATION"] is False
    assert v["REAL_DATA_READ"] is False
    assert v["NUMERICAL_ESTIMATION"] is False
    assert v["PCG_REAL_EXECUTION"] is False
    assert v["NEW_STATISTICAL_METHOD_ACTIVATED"] is False
    assert v["NEW_STATISTICAL_METHOD_EXECUTED"] is False
    assert v["NEW_MARKET_RESULT"] is False
    assert v["OOS_CONSUMPTION"] is False
    assert r["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert r["authority"]["conditioning_spec_design"] is True
    assert all(val is False for key,val in r["authority"].items() if key!="conditioning_spec_design")
    assert r["next_frontier"]["id"]=="NOT_YET_ASSIGNED"
    assert r["next_frontier"]["separate_human_authorization_required"] is True
    assert r["next_frontier"]["automatic_open"] is False
    assert r["next_frontier"]["automatic_execution"] is False
    assert r["next_frontier"]["opened"] is False
    assert r["stop"] is True

def test_27_final_closure_stops_before_route_b_gate_or_estimation():
    t=FINAL_CLOSURE.read_text(encoding="utf-8")
    assert "YEAR_STRATA_CONDITIONING_SPEC =\nQUALIFIED_AND_FROZEN" in t
    assert "ROUTE_B_ADMISSIBLE =\nNOT_YET_ESTABLISHED" in t
    assert "NEXT_PCG_ROUTE_B_APPLICATION =\nCLOSED" in t
    assert "SEPARATE_HUMAN_AUTHORIZATION =\nREQUIRED" in t
    assert "REAL_DATA_READ =\nFALSE" in t
    assert "NUMERICAL_ESTIMATION =\nFALSE" in t
    assert "PCG_REAL_EXECUTION =\nFALSE" in t
    assert t.rstrip().endswith("STOP.")
