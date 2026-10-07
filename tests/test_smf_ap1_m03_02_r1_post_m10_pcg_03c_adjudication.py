from __future__ import annotations
import ast
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"
REPORTS=ROOT/"reports"/"program"
ART=ROOT/"artifacts"/"smf_ap1_m03_02_r1_post_m10_pcg_03b"

ADJ=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-03C-HUMAN-ADJUDICATION-2026-10-07.json"
PRIMARY=ART/"REAL_PCG_RESULT.json"
REFERENCE=ART/"REAL_PCG_REFERENCE_RESULT.json"
PARITY=ART/"REAL_REFERENCE_PARITY.json"

EXPECTED={
    "pcg03b_receipt":"e8b8af3253d1a4b8ca8f9de12daeb2bafdf6535c",
    "pcg03b_closure":"a35f6044da104bc9b5dd27b96e22e85aa655b120",
    "primary":"b3a9ee10f6c0289e54391a368447a1f80d73ca48",
    "reference":"b3a9ee10f6c0289e54391a368447a1f80d73ca48",
    "parity":"881791e3a4b33c2fee9e252ab7736595de688ec4",
    "tcs01":"b9d79720b7e0e1732ddf0b5d1ca50f9b9e07f7d5",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def test_01_source_blobs_exact():
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03B-FINAL-EXECUTION-RECEIPT-V0.1.json")==EXPECTED["pcg03b_receipt"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03B-FINAL-TECHNICAL-CLOSURE.md")==EXPECTED["pcg03b_closure"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_03b/REAL_PCG_RESULT.json")==EXPECTED["primary"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_03b/REAL_PCG_REFERENCE_RESULT.json")==EXPECTED["reference"]
    assert blob("artifacts/smf_ap1_m03_02_r1_post_m10_pcg_03b/REAL_REFERENCE_PARITY.json")==EXPECTED["parity"]

def test_02_source_results_remain_identical():
    assert PRIMARY.read_bytes()==REFERENCE.read_bytes()
    assert load(PRIMARY)==load(REFERENCE)

def test_03_adjudication_source_bindings_exact():
    a=load(ADJ)["source_bindings"]
    assert a["pcg03b_final_execution_receipt_blob"]==EXPECTED["pcg03b_receipt"]
    assert a["pcg03b_final_technical_closure_blob"]==EXPECTED["pcg03b_closure"]
    assert a["primary_result_blob"]==EXPECTED["primary"]
    assert a["reference_result_blob"]==EXPECTED["reference"]
    assert a["parity_blob"]==EXPECTED["parity"]

def test_04_technical_evidence_human_adopted():
    t=load(ADJ)["technical_evidence_adoption"]
    assert t["POST_M10_PCG_03B_EXECUTION"]=="HUMAN_ACCEPTED_AS_TECHNICALLY_QUALIFIED"
    assert t["POST_M10_PCG_03B_PRIMARY_EXECUTION"]=="PASS"
    assert t["POST_M10_PCG_03B_REFERENCE_EXECUTION"]=="PASS"
    assert t["POST_M10_PCG_03B_REFERENCE_PARITY"]=="PASS"
    assert t["POST_M10_PCG_03B_RESULT_INTEGRITY"]=="QUALIFIED"
    assert t["primary_real_gate_execution_count"]==1
    assert t["independent_reference_execution_count"]==1
    assert t["retry_count"]==0
    assert t["primary_reference_semantic_parity"]=="EXACT"
    assert t["primary_reference_canonical_byte_parity"]=="EXACT"

def test_05_exact_gate_result_human_adopted():
    r=load(ADJ)["adopted_gate_result"]
    assert r["claim_unit"]=="tick_count p50"
    assert r["input_classification"]=="MATERIAL_TEMPORAL_VARIATION"
    assert r["selected_route"]=="B"
    assert r["gate_state"]==["ADMISSIBLE_BY_ROUTE_B"]
    assert r["route_states"]=={"B":"ADMISSIBLE_BY_ROUTE_B"}
    assert r["decision_reason"]=="ADMISSIBLE_BY_ONE_OR_MORE_QUALIFIED_ROUTES"
    assert r["block_reason"] is None
    assert r["qualifying_routes"]==["B"]
    assert r["overall_gate_admissibility"]=="ADMISSIBLE"
    assert r["authority_created"]=="NONE"
    assert r["PCG_03B_GATE_RESULT"]=="HUMAN_ADOPTED"

def test_06_route_b_adoption_is_exactly_claim_scoped():
    r=load(ADJ)["route_b_adjudication"]
    s=r["exact_scope"]
    assert r["ROUTE_B_ADMISSIBILITY"]=="HUMAN_ADOPTED"
    assert s["claim_unit"]=="tick_count p50"
    assert s["downstream_claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert s["downstream_analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert s["temporal_conditioning_spec_id"]=="POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
    assert s["conditioning_type"]=="YEAR_STRATA"
    assert s["strata"]==["UTC_YEAR:2022","UTC_YEAR:2023","UTC_YEAR:2024","UTC_YEAR:2025"]
    assert r["automatic_cross_scope_propagation"] is False

def test_07_tcs01_identity_unchanged():
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DC-01-YEAR-STRATA-TEMPORAL-CONDITIONING-SPEC-V0.1.json")==EXPECTED["tcs01"]
    s=load(ADJ)["conditioning_spec"]
    assert s["id"]=="POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
    assert s["status"]=="QUALIFIED_AND_FROZEN"
    assert s["route_b_admissibility"]=="HUMAN_ADOPTED"
    assert s["mutation_authorized"] is False

def test_08_admissibility_semantics_exact():
    s=load(ADJ)["admissibility_semantics"]
    assert s["exclusive_meaning"]=="THE EXACT CLAIM-SCOPED YEAR_STRATA CONDITIONING DESIGN SATISFIES THE FROZEN PCG ROUTE-B GOVERNANCE ADMISSIBILITY CONDITIONS"
    assert s["result_class"]=="CLAIM_SCOPED_GOVERNANCE_GATE_RESULT"

def test_09_no_scientific_promotion():
    p=set(load(ADJ)["admissibility_semantics"]["prohibited_promotions"])
    required={"YEAR_SPECIFIC_REFERENCE_VALUES","TEMPORAL_STABILITY","TEMPORAL_INSTABILITY","FORMAL_NONSTATIONARITY","STATIONARITY","CHANGE_POINT","STRUCTURAL_BREAK","MARKET_REGIME","REGIME_CAUSATION","PREDICTIVE_VALUE","GENERALIZATION","ECONOMIC_EDGE","PROFITABILITY","STRATEGY_VALIDITY","TRADING_EDGE"}
    assert required<=p

def test_10_old_pooled_claim_remains_blocked():
    o=load(ADJ)["original_pooled_claim"]
    assert o["id"]=="POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert o["status"]=="PRESERVED_AS_BLOCKED"
    assert o["semantic_rewrite"]=="FORBIDDEN"
    assert o["route_a"]=="NOT_SELECTED"
    assert o["unconditional_2022_2025_pooling"]=="NOT_AUTHORIZED"

def test_11_conditioned_claim_is_governance_admissible_not_executed():
    c=load(ADJ)["conditioned_claim"]
    assert c["governance_admissibility"]=="ADMISSIBLE_BY_ROUTE_B"
    assert c["claim_governance_admissible"] is True
    assert c["scientific_execution"]=="NOT_EXECUTED"
    assert c["numerical_result"]=="NONE"
    assert c["claim_empirically_estimated"] is False

def test_12_estimands_remain_not_estimated():
    e=load(ADJ)["estimands"]
    for y in ("2022","2023","2024","2025"):
        assert e[f"R_{y}"]["value"]=="NOT_ESTIMATED"

def test_13_no_cross_year_aggregation():
    e=load(ADJ)["estimands"]
    assert e["relation"]=="A_CONDITIONED_REFERENCE_VECTOR"
    assert set(e["forbidden_aggregations"])=={
        "MEAN_OF_YEAR_REFERENCES","WEIGHTED_MEAN_OF_YEAR_REFERENCES",
        "MEDIAN_OF_YEAR_MEDIANS","POOLED_RECOMPOSITION","GLOBAL_2022_2025_REFERENCE"
    }

def test_14_epistemic_state_preserved():
    e=load(ADJ)["epistemic_state"]
    assert e=={
        "evidence_state":"EXPOSED",
        "claim_provenance":"RESULT_AWARE",
        "same_corpus_confirmatory_status":"NON_PRISTINE",
        "reset_to_pristine":"FORBIDDEN",
    }

def test_15_methods_remain_closed():
    assert load(ADJ)["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}

def test_16_authority_only_adds_route_b_governance_admissibility():
    a=load(ADJ)["authority"]
    assert a["ROUTE_B_GOVERNANCE_ADMISSIBILITY"]=="HUMAN_ADOPTED"
    assert all(v is False for k,v in a.items() if k!="ROUTE_B_GOVERNANCE_ADMISSIBILITY")

def test_17_execution_state_all_false():
    assert all(v is False for v in load(ADJ)["execution_state"].values())

def test_18_human_closure_exact():
    h=load(ADJ)["human_closure"]
    assert h["POST_M10_PCG_03C"]=="HUMAN_ADOPTED"
    assert h["PCG_03B_TECHNICAL_RESULT"]=="HUMAN_ADOPTED"
    assert h["PCG_03B_GATE_RESULT"]=="HUMAN_ADOPTED"
    assert h["ROUTE_B_ADMISSIBILITY"]=="HUMAN_ADOPTED"
    assert h["CONDITIONED_DOWNSTREAM_CLAIM"]=="GOVERNANCE_ADMISSIBLE"
    assert h["YEAR_STRATA_CONDITIONING_SPEC"]=="QUALIFIED_AND_FROZEN"
    assert h["SELECTED_ROUTE"]=="B"
    assert h["OLD_POOLED_CLAIM"]=="PRESERVED_AS_BLOCKED"
    assert h["AUTOMATIC_DOWNSTREAM_ACTION"] is False

def test_19_next_real_estimation_remains_closed():
    n=load(ADJ)["next_frontier"]
    assert n["exact_id"]=="NOT_YET_ASSIGNED"
    assert n["next_real_estimation_execution"]=="CLOSED"
    assert n["real_data_read"] is False
    assert n["year_stratified_estimation"] is False
    assert n["separate_human_authorization_required"] is True
    assert n["automatic_open"] is False
    assert n["automatic_execution"] is False

def test_20_no_pcg03c_runtime_surface():
    assert not list((ROOT/"tools").glob("*pcg_03c*"))
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*pcg_03c*"))
        assert not list(art.glob("*PCG-03C*"))

def test_21_test_cannot_replay_pcg03b_or_call_estimator():
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
    assert not ({"evaluate","reference_evaluate","load_module","quantile","median"} & set(calls))

def test_22_primary_reference_budget_remains_consumed_exactly_once():
    t=load(ADJ)["technical_evidence_adoption"]
    assert t["primary_real_gate_execution_count"]==1
    assert t["independent_reference_execution_count"]==1
    assert t["retry_count"]==0

def test_23_authority_created_by_gate_remains_none():
    assert load(ADJ)["adopted_gate_result"]["authority_created"]=="NONE"

def test_24_force_false():
    assert load(ADJ)["force"] is False

def test_25_no_automatic_downstream_action():
    assert load(ADJ)["human_closure"]["AUTOMATIC_DOWNSTREAM_ACTION"] is False