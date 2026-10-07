from __future__ import annotations
import ast
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"

PACKET=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-03A-ROUTE-B-APPLICATION-PACKET-V0.1.json"
BREAKERS=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-03A-FROZEN-BREAKER-CONTRACT-V0.1.json"
TRACE=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-03A-REQUIREMENTS-PROVENANCE-TRACEABILITY-V0.1.json"

EXPECTED={
    "dc01_receipt":"3538cc0af1067f8387c415db08a3b8ee8c5e3ccb",
    "dc01_closure":"08c196054f1937ee0a903928017995dc7aaa7798",
    "tcs01":"b9d79720b7e0e1732ddf0b5d1ca50f9b9e07f7d5",
    "runtime":"2b4b96b755293c47efa89522e5509bda4f0c9c73",
    "reference":"6567e3d7325bfa769e10bc5bf1497b6aa416e3ce",
    "pcg01_breaker":"82362c52e52da84d251faeaa12d943d3c236b8b5",
}

REQUIRED_RUNTIME_FIELDS={
    "case_id","claim_unit","downstream_claim_id","downstream_analysis_id",
    "requested_temporal_scope","pooling_requested","conditioning_requested",
    "preregistered_robust_method_requested","requested_routes",
    "pooling_justification_ref","pooling_justification_status",
    "pooling_justification_reason_code","temporal_conditioning_spec_ref",
    "temporal_conditioning_spec_status","robust_method_preregistration_ref",
    "robust_method_preregistration_status","robust_method_fields",
    "evidence_state_request","authority_requests",
    "real_data_dependency_requested","admissibility_basis_claim_unit",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(
        ["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],
        text=True
    ).strip()

def test_01_exact_dc01_bindings():
    p=load(PACKET)
    b=p["dc01_bindings"]
    assert b["final_readiness_receipt_blob"]==EXPECTED["dc01_receipt"]
    assert b["final_closure_blob"]==EXPECTED["dc01_closure"]
    assert b["year_strata_spec_blob"]==EXPECTED["tcs01"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-READINESS-RECEIPT-V0.1.json")==EXPECTED["dc01_receipt"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-CLOSURE.md")==EXPECTED["dc01_closure"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DC-01-YEAR-STRATA-TEMPORAL-CONDITIONING-SPEC-V0.1.json")==EXPECTED["tcs01"]

def test_02_exact_pcg01_bindings():
    p=load(PACKET)["pcg01_bindings"]
    assert p=={
        "runtime_blob":EXPECTED["runtime"],
        "reference_blob":EXPECTED["reference"],
        "breaker_blob":EXPECTED["pcg01_breaker"],
    }
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED["runtime"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED["reference"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json")==EXPECTED["pcg01_breaker"]

def test_03_application_identity_is_exact():
    p=load(PACKET)
    assert p["application_id"]=="POST_M10-PCG03A-APP01-TICKCOUNT-P50-YEAR-STRATA-2022-2025"
    assert p["control_id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-03A"

def test_04_runtime_packet_field_set_is_exact():
    rp=load(PACKET)["runtime_packet"]
    assert set(rp)==REQUIRED_RUNTIME_FIELDS

def test_05_exact_claim_scope():
    rp=load(PACKET)["runtime_packet"]
    assert rp["claim_unit"]=="tick_count p50"
    assert rp["downstream_claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert rp["downstream_analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert rp["requested_temporal_scope"]=="UTC_YEAR:2022|UTC_YEAR:2023|UTC_YEAR:2024|UTC_YEAR:2025"

def test_06_exact_route_b_request_only():
    rp=load(PACKET)["runtime_packet"]
    assert rp["pooling_requested"] is False
    assert rp["conditioning_requested"] is True
    assert rp["preregistered_robust_method_requested"] is False
    assert rp["requested_routes"]==["B"]

def test_07_route_a_fields_absent():
    rp=load(PACKET)["runtime_packet"]
    assert rp["pooling_justification_ref"] is None
    assert rp["pooling_justification_status"]=="JUSTIFICATION_ABSENT"
    assert rp["pooling_justification_reason_code"]=="NONE"

def test_08_route_b_spec_is_exactly_dc01_tcs01():
    p=load(PACKET)
    rp=p["runtime_packet"]
    assert p["temporal_conditioning_spec"]["id"]=="POST_M10-TCS01-TICKCOUNT-P50-UTC-YEAR-STRATA-2022-2025"
    assert p["temporal_conditioning_spec"]["git_blob"]==EXPECTED["tcs01"]
    assert p["temporal_conditioning_spec"]["conditioning_type"]=="YEAR_STRATA"
    assert p["temporal_conditioning_spec"]["status"]=="SPEC_QUALIFIED_AND_FROZEN"
    assert rp["temporal_conditioning_spec_ref"]=="GIT_BLOB:"+EXPECTED["tcs01"]
    assert rp["temporal_conditioning_spec_status"]=="SPEC_QUALIFIED_AND_FROZEN"

def test_09_route_c_fields_absent():
    rp=load(PACKET)["runtime_packet"]
    assert rp["robust_method_preregistration_ref"] is None
    assert rp["robust_method_preregistration_status"]=="METHOD_PREREG_ABSENT_OR_INCOMPLETE"
    assert rp["robust_method_fields"]=={}

def test_10_evidence_state_preserved():
    rp=load(PACKET)["runtime_packet"]
    assert rp["evidence_state_request"]=="PRESERVE_EXPOSED_NON_PRISTINE"

def test_11_no_authority_requests_or_real_data_dependency():
    rp=load(PACKET)["runtime_packet"]
    assert rp["authority_requests"]==[]
    assert rp["real_data_dependency_requested"] is False
    assert rp["admissibility_basis_claim_unit"]=="tick_count p50"

def test_12_old_pooled_claim_preserved_blocked():
    p=load(PACKET)["old_pooled_claim"]
    assert p["id"]=="POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert p["status"]=="PRESERVED_AS_BLOCKED"
    assert p["semantic_rewrite"]=="FORBIDDEN"

def test_13_expected_gate_result_not_preregistered():
    p=load(PACKET)
    assert p["expected_gate_result"]=="NOT_PREREGISTERED"
    assert p["route_b_admissible"]=="NOT_YET_ESTABLISHED"

def test_14_authority_ceiling_all_false():
    a=load(PACKET)["authority_ceiling"]
    assert all(v is False for v in a.values())

def test_15_breaker_surface_exactly_42():
    b=load(BREAKERS)
    assert b["minimum_required_breaker_count"]==42
    assert b["breaker_count"]==42
    ids=[x[0] for x in b["breakers"]]
    assert ids==[f"PCG03A-B{i:02d}" for i in range(1,43)]

def test_16_method_state_remains_closed():
    b=load(BREAKERS)
    assert b["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert b["route_b_admissible"]=="NOT_YET_ESTABLISHED"

def test_17_breaker_execution_authority_is_false():
    b=load(BREAKERS)
    for key in (
        "runtime_execution_authorized","reference_execution_authorized",
        "real_data_read_authorized","conditioning_execution_authorized",
        "year_stratified_estimation_authorized","statistical_method_activation_authorized",
        "statistical_method_execution_authorized","oos_consumption_authorized",
        "trading_authority","capital_authority",
    ):
        assert b[key] is False

def test_18_traceability_covers_all_breakers():
    all_breakers={x[0] for x in load(BREAKERS)["breakers"]}
    mapped={x for row in load(TRACE)["requirement_map"] for x in row["breakers"]}
    assert all_breakers==mapped

def test_19_material_fields_have_explicit_provenance():
    t=load(TRACE)
    allowed=set(t["provenance_labels"])
    for item in t["material_fields"].values():
        assert item["provenance"] in allowed

def test_20_no_pcg03a_runtime_or_result_artifact_surface():
    assert not list((ROOT/"tools").glob("*pcg_03a*"))
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*pcg_03a*"))
        assert not list(art.glob("*PCG-03A*"))

def test_21_test_cannot_execute_primary_or_reference_runtime():
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

def test_22_spec_is_not_mutated_by_packet():
    p=load(PACKET)
    assert p["temporal_conditioning_spec"]["git_blob"]==blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DC-01-YEAR-STRATA-TEMPORAL-CONDITIONING-SPEC-V0.1.json")

def test_23_runtime_packet_has_no_expected_result_field():
    rp=load(PACKET)["runtime_packet"]
    assert "expected_gate_result" not in rp

def test_24_runtime_packet_has_no_governance_metadata():
    rp=load(PACKET)["runtime_packet"]
    assert "application_id" not in rp
    assert "dc01_bindings" not in rp
    assert "pcg01_bindings" not in rp
    assert "authority_ceiling" not in rp


FREEZE=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-03A-PRE-EXECUTION-FREEZE-V0.1.json"

def test_25_pre_execution_freeze_binds_exact_packet_identity():
    f=load(FREEZE)
    p=f["packet_identity"]
    assert p["git_blob"]=="349e0ea3e98ad24a9d179f06ffeeaea11c36f425"
    assert p["sha256"]=="56d3a58c0e236590ebcb13caed0fe98d38fb2bde860b2024b084eceb2351f4b1"
    assert p["persisted_head"]=="0fe3a977e529577ceb5a4d8e4df1a44777d22984"
    assert p["persisted_tree"]=="c29fdc88edfe2b43fae6a061ca041d5bc3bf40fd"

def test_26_pre_execution_freeze_binds_exact_dc01_and_pcg01():
    f=load(FREEZE)
    assert f["dc01_bindings"]["final_readiness_receipt_blob"]==EXPECTED["dc01_receipt"]
    assert f["dc01_bindings"]["final_closure_blob"]==EXPECTED["dc01_closure"]
    assert f["dc01_bindings"]["temporal_conditioning_spec_blob"]==EXPECTED["tcs01"]
    assert f["pcg01_execution_bindings"]=={
      "runtime_blob":EXPECTED["runtime"],
      "reference_blob":EXPECTED["reference"],
      "breaker_blob":EXPECTED["pcg01_breaker"],
    }

def test_27_pre_execution_freeze_preserves_route_b_input_only():
    s=load(FREEZE)["frozen_application_summary"]
    assert s["pooling_requested"] is False
    assert s["conditioning_requested"] is True
    assert s["preregistered_robust_method_requested"] is False
    assert s["requested_routes"]==["B"]
    assert s["temporal_conditioning_spec_status"]=="SPEC_QUALIFIED_AND_FROZEN"

def test_28_pre_execution_freeze_has_no_expected_result_or_execution_authority():
    f=load(FREEZE)
    assert f["expected_gate_result"]=="NOT_PREREGISTERED"
    assert f["route_b_admissible"]=="NOT_YET_ESTABLISHED"
    assert all(v is False for v in f["authority_ceiling"].values())

def test_29_pcg03b_remains_closed():
    n=load(FREEZE)["next_frontier"]
    assert n["id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-03B"
    assert n["separate_human_authorization_required"] is True
    assert n["automatic_open"] is False
    assert n["automatic_execution"] is False
    assert n["opened"] is False
    assert n["executed"] is False
