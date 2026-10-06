from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"
CONTRACT=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-00-CONTRACT-V0.1.json"
TABLE=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-00-DECISION-TABLE-V0.1.json"
BREAKERS=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-00-FROZEN-BREAKER-CONTRACT-V0.1.json"
TRACE=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-00-REQUIREMENTS-TRACEABILITY-V0.1.json"

EXPECTED_ADJ="aeed65dd6853392168aa97432ebadb1f9ea48e46"
EXPECTED_REC="afe3fe2cc9dc36182f785620496a66bdab297370"

def load(p): return json.loads(p.read_text(encoding="utf-8"))

def test_01_design_only_no_implementation_or_execution():
    c=load(CONTRACT)
    assert c["design_only"] is True
    assert c["implementation"]=={
      "executable_gate_implemented":False,
      "executable_gate_executed":False,
      "real_data_read":False,
      "new_statistical_method_executed":False,
      "new_market_result":False,
      "oos_consumption":False
    }

def test_02_exact_binding_source_identities():
    c=load(CONTRACT)
    assert c["binding_sources"]["post_m10_human_adjudication_blob"]==EXPECTED_ADJ
    assert c["binding_sources"]["post_m10_human_adoption_receipt_blob"]==EXPECTED_REC

def test_03_exact_eight_material_claim_units():
    c=load(CONTRACT)
    assert c["claim_units"]["material_temporal_variation"]==[
      "tick_count p50","tick_count p90","tick_count p99",
      "minute_range p50","minute_range p90","minute_range p95","minute_range p99",
      "spread_mean p50"
    ]

def test_04_exact_three_no_material_detected_claim_units():
    c=load(CONTRACT)
    assert c["claim_units"]["no_material_temporal_variation_detected"]==[
      "spread_mean p90","spread_mean p95","spread_mean p99"
    ]

def test_05_material_pooling_defaults_not_allowed():
    c=load(CONTRACT)
    assert c["claim_units"]["material_default_pooling_rule"]=="NOT_ALLOWED_BY_DEFAULT"

def test_06_required_inputs_are_explicit():
    c=load(CONTRACT)
    assert c["required_inputs"]==[
      "CLAIM_UNIT","DOWNSTREAM_CLAIM_ID","DOWNSTREAM_ANALYSIS_ID","REQUESTED_TEMPORAL_SCOPE",
      "POOLING_REQUESTED","CONDITIONING_REQUESTED","PREREGISTERED_ROBUST_METHOD_REQUESTED"
    ]
    assert c["material_defaults_forbidden"] is True

def test_07_route_a_is_reference_bound_and_cannot_self_adopt():
    a=load(CONTRACT)["routes"]["A"]
    assert a["required_ref"]=="POOLING_JUSTIFICATION_REF"
    assert a["self_adoption_forbidden"] is True
    assert "JUSTIFICATION_HUMAN_ADOPTED" in a["ref_states"]

def test_08_route_b_is_design_only_and_requires_frozen_spec():
    b=load(CONTRACT)["routes"]["B"]
    assert b["required_ref"]=="TEMPORAL_CONDITIONING_SPEC_REF"
    assert b["spec_must_be_frozen_before_downstream_result"] is True
    assert b["executes_stratification"] is False

def test_09_route_c_cannot_select_activate_or_execute_method():
    c=load(CONTRACT)["routes"]["C"]
    assert c["selects_method"] is False
    assert c["activates_method"] is False
    assert c["executes_method"] is False
    assert c["required_method_fields"]==[
      "EXACT_METHOD_IDENTITY","EXACT_FAILURE_MODE","EXACT_ASSUMPTION_SET",
      "EXACT_VALIDITY_SCOPE","EXACT_MATERIAL_PARAMETERS"
    ]

def test_10_required_states_include_route_provenance():
    states=set(load(CONTRACT)["states"])
    assert {
      "NOT_APPLICABLE","BLOCKED","ROUTE_A_PENDING","ROUTE_B_PENDING","ROUTE_C_PENDING",
      "ADMISSIBLE_BY_ROUTE_A","ADMISSIBLE_BY_ROUTE_B","ADMISSIBLE_BY_ROUTE_C",
      "NON_MATERIAL_POOLING_REVIEW_REQUIRED"
    } <= states

def test_11_material_without_route_is_blocked_in_decision_table():
    rows={x["id"]:x for x in load(TABLE)["rows"]}
    assert rows["PCG-D02"]["state"]=="BLOCKED"
    assert rows["PCG-D02"]["reason"]=="MATERIAL_CLAIM_UNIT_DEFAULTS_TO_BLOCKED_WITHOUT_A_B_OR_C"

def test_12_nonmaterial_status_never_auto_approves_pooling():
    rows={x["id"]:x for x in load(TABLE)["rows"]}
    assert rows["PCG-D09"]["state"]=="NON_MATERIAL_POOLING_REVIEW_REQUIRED"
    assert rows["PCG-D09"]["reason"]=="NO_MATERIAL_VARIATION_DETECTED_DOES_NOT_AUTO_VALIDATE_POOLING"

def test_13_insufficient_route_a_reasons_are_blocked():
    rows={x["id"]:x for x in load(TABLE)["rows"]}
    for key in ("PCG-D12","PCG-D13","PCG-D14"):
        assert rows[key]["state"]=="BLOCKED"
        assert rows[key]["reason"]=="INSUFFICIENT_ROUTE_A_JUSTIFICATION"

def test_14_same_corpus_pristine_reset_is_blocked():
    rows={x["id"]:x for x in load(TABLE)["rows"]}
    assert rows["PCG-D15"]["state"]=="BLOCKED"
    assert load(CONTRACT)["evidence_state"]["reset_to_pristine"]=="FORBIDDEN"

def test_15_m04_m05_m08_m09_m11_remain_closed():
    assert load(CONTRACT)["method_guards"]=={
      "M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED",
      "global_m05_resampling_across_2022_2025":"BLOCKED_PENDING_TEMPORAL_JUSTIFICATION"
    }

def test_16_no_authority_expansion():
    a=load(CONTRACT)["authority"]
    assert all(value is False for value in a.values())

def test_17_all_required_b01_to_b32_are_frozen():
    b=load(BREAKERS)
    ids=[x[0] for x in b["breakers"]]
    assert ids[:32]==[f"PCG-B{i:02d}" for i in range(1,33)]
    assert b["minimum_required_breakers"]==32
    assert b["total_frozen_breakers"]>=32
    assert b["executable_breaker_runner_authorized"] is False

def test_18_traceability_covers_every_frozen_breaker():
    b_ids={x[0] for x in load(BREAKERS)["breakers"]}
    mapped={x for row in load(TRACE)["mappings"] for x in row["breakers"]}
    assert b_ids <= mapped

def test_19_no_runtime_or_real_result_artifact_created_for_pcg_00():
    assert not list((ROOT/"tools").glob("*pcg*"))
    assert not list((ROOT/"artifacts").glob("*pcg*"))
    assert not list((ROOT/"artifacts").glob("*PCG*"))

def test_20_no_pass_fail_only_or_forbidden_scientific_promotion():
    t=load(TABLE)
    assert t["semantics"]["pass_fail_only_forbidden"] is True
    forbidden=set(t["forbidden_output_labels"])
    assert {"PASS","FAIL","STABILITY_PROVEN","STATIONARITY_PROVEN","FORMAL_NONSTATIONARITY","REGIME_CHANGE"} <= forbidden

def test_21_claim_scope_is_exact_and_no_propagation():
    c=load(CONTRACT)
    assert c["scope_binding"]==[
      "CLAIM_UNIT","DOWNSTREAM_CLAIM_ID","DOWNSTREAM_ANALYSIS_ID","REQUESTED_TEMPORAL_SCOPE"
    ]
    t=load(TABLE)["semantics"]
    assert t["no_cross_claim_propagation"] is True
    assert t["no_cross_metric_route_propagation"] is True

def test_22_pcg01_requires_separate_human_authorization():
    n=load(CONTRACT)["next_frontier"]
    assert n["id"]=="POST_M10_PCG-01"
    assert n["separate_human_authorization_required"] is True
    assert n["automatically_opened"] is False


FINAL_RECEIPT=ROOT/"reports"/"program"/"2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-00-FINAL-READINESS-RECEIPT-V0.1.json"

def test_23_final_receipt_closes_pcg00_and_keeps_pcg01_closed():
    r=load(FINAL_RECEIPT)
    v=r["verdict"]
    assert v["POST_M10_PCG_DESIGN"]=="QUALIFIED"
    assert v["POST_M10_PCG_SEMANTICS"]=="FROZEN"
    assert v["POST_M10_PCG_BREAKER_CONTRACT"]=="FROZEN"
    assert v["POST_M10_PCG_DOCUMENTARY_QUALIFICATION"]=="PASS"
    assert v["POST_M10_PCG_IMPLEMENTATION_READINESS"]=="READY_FOR_SEPARATE_HUMAN_DECISION"
    assert v["POST_M10_PCG_IMPLEMENTED"] is False
    assert v["POST_M10_PCG_EXECUTED"] is False
    assert v["REAL_DATA_READ"] is False
    assert v["NEW_STATISTICAL_METHOD_EXECUTED"] is False
    assert v["NEW_MARKET_RESULT"] is False
    assert r["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert r["authority"]=={"oos_consumption":False,"trading":False,"capital":False}
    assert r["next_frontier"]["id"]=="POST_M10_PCG-01"
    assert r["next_frontier"]["separate_human_authorization_required"] is True
    assert r["next_frontier"]["opened"] is False
    assert r["next_frontier"]["executed"] is False
    assert r["stop"] is True
