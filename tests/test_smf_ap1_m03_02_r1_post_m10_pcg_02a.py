from __future__ import annotations
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"
PACKET=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-02A-FIRST-REAL-APPLICATION-PACKET-V0.1.json"
BREAKERS=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-02A-FROZEN-BREAKER-CONTRACT-V0.1.json"
DC00_RECEIPT=ROOT/"reports"/"program"/"2026-10-06-SMF-AP1-M03-02-R1-POST-M10-DC-00-FINAL-READINESS-RECEIPT-V0.1.json"
RUNTIME=ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_pcg_01.py"
REFERENCE=ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py"

EXPECTED_RUNTIME="2b4b96b755293c47efa89522e5509bda4f0c9c73"
EXPECTED_REFERENCE="6567e3d7325bfa769e10bc5bf1497b6aa416e3ce"
EXPECTED_PCG01_BREAKER="82362c52e52da84d251faeaa12d943d3c236b8b5"
EXPECTED_DC00_RECEIPT="7c1d9474fc35e08e07c1b4481113e35d354715bc"
EXPECTED_DC00_CLOSURE="a17c4863c464357744beaeeba2f5ee156e2f2d2d"

REQUIRED_RUNTIME_FIELDS={
    "case_id","claim_unit","downstream_claim_id","downstream_analysis_id",
    "requested_temporal_scope","pooling_requested","conditioning_requested",
    "preregistered_robust_method_requested","requested_routes",
    "pooling_justification_ref","pooling_justification_status",
    "pooling_justification_reason_code","temporal_conditioning_spec_ref",
    "temporal_conditioning_spec_status","robust_method_preregistration_ref",
    "robust_method_preregistration_status","robust_method_fields",
    "evidence_state_request","authority_requests",
    "real_data_dependency_requested","admissibility_basis_claim_unit"
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def blob(path):
    return subprocess.check_output(
        ["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],
        text=True
    ).strip()

def test_01_exact_binding_identities():
    p=load(PACKET)
    assert p["source_dc00"]["final_receipt_blob"]==EXPECTED_DC00_RECEIPT
    assert p["source_dc00"]["final_closure_blob"]==EXPECTED_DC00_CLOSURE
    assert p["pcg01_bindings"]["runtime_blob"]==EXPECTED_RUNTIME
    assert p["pcg01_bindings"]["reference_blob"]==EXPECTED_REFERENCE
    assert p["pcg01_bindings"]["breaker_blob"]==EXPECTED_PCG01_BREAKER

def test_02_repository_objects_match_bindings():
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED_RUNTIME
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED_REFERENCE
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json")==EXPECTED_PCG01_BREAKER
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-DC-00-FINAL-READINESS-RECEIPT-V0.1.json")==EXPECTED_DC00_RECEIPT
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-DC-00-FINAL-CLOSURE.md")==EXPECTED_DC00_CLOSURE

def test_03_dc00_is_qualified_and_frozen():
    r=load(DC00_RECEIPT)
    assert r["verdict"]["POST_M10_DC_00"]=="QUALIFIED"
    assert r["verdict"]["FIRST_DOWNSTREAM_CLAIM"]=="FROZEN"
    assert r["verdict"]["FIRST_DOWNSTREAM_ESTIMAND"]=="FROZEN"
    assert r["verdict"]["FIRST_DOWNSTREAM_ANALYSIS_INTENT"]=="FROZEN"

def test_04_application_identity_is_exact():
    p=load(PACKET)
    assert p["application_id"]=="POST_M10-PCG02A-APP01-TICKCOUNT-P50-POOLED-2022-2025"
    assert p["m10_context"]=={
        "claim_unit":"tick_count p50",
        "claim_unit_status":"MATERIAL_TEMPORAL_VARIATION",
    }

def test_05_runtime_packet_has_exact_frozen_input_surface():
    rp=load(PACKET)["runtime_packet"]
    assert set(rp)==REQUIRED_RUNTIME_FIELDS

def test_06_downstream_identity_matches_dc00():
    rp=load(PACKET)["runtime_packet"]
    target=load(DC00_RECEIPT)["frozen_target"]
    assert rp["claim_unit"]==target["claim_unit"]
    assert rp["downstream_claim_id"]==target["downstream_claim_id"]
    assert rp["downstream_analysis_id"]==target["downstream_analysis_id"]

def test_07_temporal_scope_is_exact_complete_year_scope():
    rp=load(PACKET)["runtime_packet"]
    assert rp["requested_temporal_scope"]=="UTC_YEAR:2022|UTC_YEAR:2023|UTC_YEAR:2024|UTC_YEAR:2025"

def test_08_pooling_is_requested_but_not_executed():
    p=load(PACKET)
    rp=p["runtime_packet"]
    assert rp["pooling_requested"] is True
    assert p["authority_ceiling"]["pcg_runtime_execution"] is False
    assert p["authority_ceiling"]["pcg_result_creation"] is False

def test_09_no_route_is_manufactured():
    rp=load(PACKET)["runtime_packet"]
    assert rp["requested_routes"]==[]
    assert rp["conditioning_requested"] is False
    assert rp["preregistered_robust_method_requested"] is False

def test_10_route_a_basis_is_absent_exactly():
    rp=load(PACKET)["runtime_packet"]
    assert rp["pooling_justification_ref"] is None
    assert rp["pooling_justification_status"]=="JUSTIFICATION_ABSENT"
    assert rp["pooling_justification_reason_code"]=="NONE"

def test_11_route_b_basis_is_absent_exactly():
    rp=load(PACKET)["runtime_packet"]
    assert rp["temporal_conditioning_spec_ref"] is None
    assert rp["temporal_conditioning_spec_status"]=="SPEC_ABSENT"

def test_12_route_c_basis_is_absent_exactly():
    rp=load(PACKET)["runtime_packet"]
    assert rp["robust_method_preregistration_ref"] is None
    assert rp["robust_method_preregistration_status"]=="METHOD_PREREG_ABSENT_OR_INCOMPLETE"
    assert rp["robust_method_fields"]=={}

def test_13_evidence_state_is_preserved():
    rp=load(PACKET)["runtime_packet"]
    assert rp["evidence_state_request"]=="PRESERVE_EXPOSED_NON_PRISTINE"

def test_14_no_authority_or_real_data_dependency_is_requested():
    rp=load(PACKET)["runtime_packet"]
    assert rp["authority_requests"]==[]
    assert rp["real_data_dependency_requested"] is False

def test_15_admissibility_basis_is_claim_scoped():
    rp=load(PACKET)["runtime_packet"]
    assert rp["admissibility_basis_claim_unit"]=="tick_count p50"
    assert rp["admissibility_basis_claim_unit"]==rp["claim_unit"]

def test_16_authority_ceiling_is_all_false():
    a=load(PACKET)["authority_ceiling"]
    assert all(v is False for v in a.values())

def test_17_breaker_surface_is_complete():
    b=load(BREAKERS)
    ids=[x[0] for x in b["breakers"]]
    assert ids[:24]==[f"PCG02A-B{i:02d}" for i in range(1,25)]
    assert b["minimum_required_breaker_count"]==24
    assert b["breaker_count"]==32
    assert b["runtime_execution_authorized"] is False
    assert b["reference_execution_authorized"] is False
    assert b["real_data_read_authorized"] is False
    assert b["statistical_method_activation_authorized"] is False
    assert b["statistical_method_execution_authorized"] is False
    assert b["pcg_result_authorized"] is False

def test_18_packet_serialization_is_deterministic_json():
    doc=load(PACKET)
    canonical=(json.dumps(doc,ensure_ascii=True,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n").encode("ascii")
    assert canonical==(
        json.dumps(load(PACKET),ensure_ascii=True,sort_keys=True,separators=(",",":"),allow_nan=False)+"\n"
    ).encode("ascii")
    assert hashlib.sha256(canonical).hexdigest()

def test_19_no_pcg_runtime_or_reference_is_imported_or_called():
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

def test_20_no_real_pcg_result_or_real_data_artifact_exists():
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*pcg_02a*"))
        assert not list(art.glob("*PCG-02A*"))
        assert not list(art.glob("*PCG02A*"))

def test_21_runtime_source_is_not_modified_by_pcg02a():
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED_RUNTIME
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED_REFERENCE

def test_22_expected_gate_result_is_not_preregistered():
    b=load(BREAKERS)
    names=dict(b["breakers"])
    assert names["PCG02A-B30"]=="EXPECTED_GATE_RESULT_NOT_PREREGISTERED"


FREEZE=GOV/"SMF-AP1-M03-02-R1-POST-M10-PCG-02A-PRE-EXECUTION-FREEZE-V0.1.json"

def test_23_pre_execution_freeze_binds_exact_packet_identity():
    f=load(FREEZE)
    p=f["packet_identity"]
    assert p["git_blob"]=="bcf5258247b9ef08f732d42abe88ca7e0a9b9c55"
    assert p["sha256"]=="d0a4dde068a7fb460413120041f521597509b80736299af7dd21d7ad90531a99"
    assert p["persisted_head"]=="f5ea7d92960e7952a809ae71a97fd01e988b9908"
    assert p["persisted_tree"]=="fcc6715c166cc9d81c893ebe809f44f237d61e25"

def test_24_pre_execution_freeze_binds_exact_pcg01_identity():
    f=load(FREEZE)["pcg01_execution_bindings"]
    assert f=={
        "runtime_blob":EXPECTED_RUNTIME,
        "reference_blob":EXPECTED_REFERENCE,
        "breaker_blob":EXPECTED_PCG01_BREAKER,
    }

def test_25_expected_gate_result_is_explicitly_not_preregistered():
    f=load(FREEZE)
    assert f["expected_gate_result"]=="NOT_PREREGISTERED"
    assert f["next_frontier"]["id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-02B"
    assert f["next_frontier"]["separate_human_authorization_required"] is True
    assert f["next_frontier"]["opened"] is False
    assert f["next_frontier"]["executed"] is False

def test_26_pre_execution_freeze_authority_ceiling_is_all_false():
    assert all(v is False for v in load(FREEZE)["authority_ceiling"].values())

def test_27_freeze_preserves_explicit_empty_route_set():
    s=load(FREEZE)["frozen_application_summary"]
    assert s["pooling_requested"] is True
    assert s["requested_routes"]==[]
    assert s["authority_requests"]==[]
    assert s["real_data_dependency_requested"] is False
