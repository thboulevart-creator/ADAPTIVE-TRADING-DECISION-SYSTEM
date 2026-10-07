from __future__ import annotations
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"/"smf_ap1_m03_02_r1_post_m10_pcg_03b"
PRIMARY=ART/"REAL_PCG_RESULT.json"
REFERENCE=ART/"REAL_PCG_REFERENCE_RESULT.json"
PARITY=ART/"REAL_REFERENCE_PARITY.json"
MANIFEST=ART/"RUN_MANIFEST.json"
RECORD=ROOT/"reports"/"program"/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03B-REAL-EXECUTION-RECORD-V0.1.json"

EXPECTED={
 "pcg03a_receipt":"ac8610c8c89eb2ea7598fee59cc27cf8d1fca947",
 "pcg03a_closure":"e22557226ce2922ce0031fa685846cf09bf1d3fc",
 "packet_blob":"349e0ea3e98ad24a9d179f06ffeeaea11c36f425",
 "packet_sha256":"56d3a58c0e236590ebcb13caed0fe98d38fb2bde860b2024b084eceb2351f4b1",
 "freeze_blob":"5fd6e7937674990d718d328ee4b823b86a09e62e",
 "freeze_sha256":"c07f9dd77042e9bdbf989333203c99ba4898a4ddb316e1c5d332a80ecd7cf92e",
 "dc01_receipt":"3538cc0af1067f8387c415db08a3b8ee8c5e3ccb",
 "dc01_closure":"08c196054f1937ee0a903928017995dc7aaa7798",
 "tcs01":"b9d79720b7e0e1732ddf0b5d1ca50f9b9e07f7d5",
 "runtime":"2b4b96b755293c47efa89522e5509bda4f0c9c73",
 "reference":"6567e3d7325bfa769e10bc5bf1497b6aa416e3ce",
 "breaker":"82362c52e52da84d251faeaa12d943d3c236b8b5",
 "primary_sha256":"687e721aceead052f186df735284005a2dd4e692ba111007f00774dafa3f0f2f",
 "reference_sha256":"687e721aceead052f186df735284005a2dd4e692ba111007f00774dafa3f0f2f",
 "parity_sha256":"5c56332fdee66a2879418f9ca023690983bbb974d9d84b8d21e546da00b1a96a",
 "manifest_sha256":"0084d4b338e0967cffd605860f4f725319783ad0dcd7bf74e907ecc1d4279803",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def test_01_exact_pcg03a_and_dc01_bindings():
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03A-FINAL-READINESS-RECEIPT-V0.1.json")==EXPECTED["pcg03a_receipt"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03A-FINAL-CLOSURE.md")==EXPECTED["pcg03a_closure"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-03A-ROUTE-B-APPLICATION-PACKET-V0.1.json")==EXPECTED["packet_blob"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-03A-PRE-EXECUTION-FREEZE-V0.1.json")==EXPECTED["freeze_blob"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-READINESS-RECEIPT-V0.1.json")==EXPECTED["dc01_receipt"]
    assert blob("reports/program/2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DC-01-FINAL-CLOSURE.md")==EXPECTED["dc01_closure"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-DC-01-YEAR-STRATA-TEMPORAL-CONDITIONING-SPEC-V0.1.json")==EXPECTED["tcs01"]

def test_02_exact_pcg01_code_bindings():
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED["runtime"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED["reference"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json")==EXPECTED["breaker"]

def test_03_result_artifact_hashes_are_exact():
    assert sha(PRIMARY)==EXPECTED["primary_sha256"]
    assert sha(REFERENCE)==EXPECTED["reference_sha256"]
    assert sha(PARITY)==EXPECTED["parity_sha256"]
    assert sha(MANIFEST)==EXPECTED["manifest_sha256"]

def test_04_primary_and_reference_semantic_parity_exact():
    assert load(PRIMARY)==load(REFERENCE)

def test_05_primary_and_reference_byte_parity_exact():
    assert PRIMARY.read_bytes()==REFERENCE.read_bytes()

def test_06_execution_counts_are_exactly_one_each_and_no_retry():
    m=load(MANIFEST)
    r=load(RECORD)
    assert m["primary_real_gate_execution_count"]==1
    assert m["independent_reference_execution_count"]==1
    assert m["retry_count"]==0
    assert r["execution_counts"]=={
        "primary_real_gate_execution":1,
        "independent_reference_execution":1,
        "retry_count":0,
    }

def test_07_result_is_exact_claim_scoped_input():
    r=load(PRIMARY)
    assert r["claim_unit"]=="tick_count p50"
    assert r["downstream_claim_id"]=="POST_M10-DC02-TICKCOUNT-P50-YEAR-STRATIFIED-HISTORICAL-REFERENCES"
    assert r["downstream_analysis_id"]=="POST_M10-DA02-TICKCOUNT-P50-YEAR-STRATIFIED-REFERENCE-CONSTRUCTION"
    assert r["requested_temporal_scope"]=="UTC_YEAR:2022|UTC_YEAR:2023|UTC_YEAR:2024|UTC_YEAR:2025"

def test_08_input_classification_is_exact():
    assert load(PRIMARY)["input_classification"]=="MATERIAL_TEMPORAL_VARIATION"

def test_09_selected_route_is_b():
    assert load(PRIMARY)["selected_route"]=="B"

def test_10_gate_state_is_admissible_by_route_b():
    r=load(PRIMARY)
    assert r["gate_state"]==["ADMISSIBLE_BY_ROUTE_B"]
    assert r["route_states"]=={"B":"ADMISSIBLE_BY_ROUTE_B"}
    assert r["overall_gate_admissibility"]=="ADMISSIBLE"

def test_11_decision_reason_and_block_reason_are_exact():
    r=load(PRIMARY)
    assert r["decision_reason"]=="ADMISSIBLE_BY_ONE_OR_MORE_QUALIFIED_ROUTES"
    assert r["block_reason"] is None

def test_12_only_route_b_qualifies():
    assert load(PRIMARY)["qualifying_routes"]==["B"]

def test_13_no_authority_is_created():
    assert load(PRIMARY)["authority_created"]=="NONE"

def test_14_methods_remain_closed():
    assert load(PRIMARY)["method_state"]=={
        "M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"
    }

def test_15_no_real_data_read():
    assert load(PRIMARY)["real_data_read"] is False
    assert load(MANIFEST)["real_data_read"] is False

def test_16_binding_reference_is_exact_tcs01_and_no_route_a_c_ref():
    b=load(PRIMARY)["binding_references"]
    assert b["pooling_justification_ref"] is None
    assert b["temporal_conditioning_spec_ref"]=="GIT_BLOB:"+EXPECTED["tcs01"]
    assert b["robust_method_preregistration_ref"] is None

def test_17_parity_artifact_is_exact():
    p=load(PARITY)
    assert p["primary_reference_semantic_parity"]=="EXACT"
    assert p["primary_reference_canonical_byte_parity"]=="EXACT"
    assert p["primary_result_sha256"]==EXPECTED["primary_sha256"]
    assert p["reference_result_sha256"]==EXPECTED["reference_sha256"]

def test_18_manifest_binds_exact_packet_freeze_spec_and_code():
    m=load(MANIFEST)
    assert m["packet_blob"]==EXPECTED["packet_blob"]
    assert m["packet_sha256"]==EXPECTED["packet_sha256"]
    assert m["pre_execution_freeze_blob"]==EXPECTED["freeze_blob"]
    assert m["pre_execution_freeze_sha256"]==EXPECTED["freeze_sha256"]
    assert m["tcs01_spec_blob"]==EXPECTED["tcs01"]
    assert m["pcg01_runtime_blob"]==EXPECTED["runtime"]
    assert m["pcg01_reference_blob"]==EXPECTED["reference"]
    assert m["pcg01_breaker_blob"]==EXPECTED["breaker"]

def test_19_record_classifies_result_as_governance_only():
    r=load(RECORD)
    assert r["semantic_classification"]=="CLAIM_SCOPED_GOVERNANCE_GATE_RESULT"
    assert r["permitted_interpretation"]=="THE EXACT CLAIM-SCOPED YEAR_STRATA CONDITIONING DESIGN SATISFIES THE FROZEN PCG ROUTE-B GOVERNANCE ADMISSIBILITY CONDITIONS"
    for x in ("SCIENTIFIC_FINDING","NONSTATIONARITY_FINDING","YEAR_STRATIFIED_ESTIMATE","STRATEGY_VALIDATION"):
        assert x in r["prohibited_interpretations"]

def test_20_epistemic_state_remains_exposed_non_pristine():
    e=load(RECORD)["epistemic_state"]
    assert e=={
        "evidence_state":"EXPOSED",
        "claim_provenance":"RESULT_AWARE",
        "same_corpus_confirmatory_status":"NON_PRISTINE",
        "reset_to_pristine":"FORBIDDEN",
    }

def test_21_no_downstream_execution_or_authority():
    d=load(RECORD)["downstream_state"]
    assert all(v is False for v in d.values())

def test_22_human_adjudication_is_pending():
    assert load(RECORD)["human_adjudication"]=="PENDING"

def test_23_next_frontier_is_pcg03c_closed():
    n=load(RECORD)["next_frontier"]
    assert n["id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-03C"
    assert n["separate_human_decision_required"] is True
    assert n["automatic_adoption"] is False
    assert n["automatic_downstream_action"] is False
    assert n["opened"] is False

def test_24_result_integrity_test_cannot_execute_gate():
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

def test_25_record_stop_is_true():
    assert load(RECORD)["stop"] is True


FINAL_RECEIPT=ROOT/"reports"/"program"/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03B-FINAL-EXECUTION-RECEIPT-V0.1.json"
FINAL_CLOSURE=ROOT/"reports"/"program"/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-PCG-03B-FINAL-TECHNICAL-CLOSURE.md"

def test_26_final_receipt_preserves_pending_human_adjudication_and_closed_pcg03c():
    r=load(FINAL_RECEIPT)
    v=r["verdict"]
    assert r["status"]=="TECHNICALLY_QUALIFIED_RESULT_PERSISTED_HUMAN_ADJUDICATION_PENDING"
    assert v["POST_M10_PCG_03B_EXECUTION"]=="QUALIFIED"
    assert v["POST_M10_PCG_03B_PRIMARY_EXECUTION"]=="PASS"
    assert v["POST_M10_PCG_03B_REFERENCE_EXECUTION"]=="PASS"
    assert v["POST_M10_PCG_03B_REFERENCE_PARITY"]=="PASS"
    assert v["POST_M10_PCG_03B_RESULT_INTEGRITY"]=="QUALIFIED"
    assert v["POST_M10_PCG_03B_GATE_RESULT"]=="PERSISTED"
    assert v["PCG_03B_HUMAN_ADJUDICATION"]=="PENDING"
    assert v["REAL_DATA_READ"] is False
    assert v["NUMERICAL_ESTIMATION"] is False
    assert v["CONDITIONING_EXECUTION"] is False
    assert v["YEAR_STRATIFIED_ESTIMATION"] is False
    assert v["NEW_STATISTICAL_METHOD_ACTIVATED"] is False
    assert v["NEW_STATISTICAL_METHOD_EXECUTED"] is False
    assert v["NEW_MARKET_RESULT"] is False
    assert v["OOS_CONSUMPTION"] is False
    assert r["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert all(x is False for x in r["authority"].values())
    assert r["next_frontier"]["id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-03C"
    assert r["next_frontier"]["separate_human_decision_required"] is True
    assert r["next_frontier"]["automatic_adoption"] is False
    assert r["next_frontier"]["automatic_downstream_action"] is False
    assert r["next_frontier"]["opened"] is False
    assert r["stop"] is True

def test_27_final_closure_stops_before_human_adjudication_or_estimation():
    t=FINAL_CLOSURE.read_text(encoding="utf-8")
    assert "PCG_03B_HUMAN_ADJUDICATION =\nPENDING" in t
    assert "SMF-AP1-M03-02-R1-POST-M10-PCG-03C =\nCLOSED" in t
    assert "SEPARATE_HUMAN_DECISION_REQUIRED =\nTRUE" in t
    assert "AUTOMATIC_ADOPTION =\nFALSE" in t
    assert "AUTOMATIC_DOWNSTREAM_ACTION =\nFALSE" in t
    assert "CONDITIONING_EXECUTION =\nFALSE" in t
    assert "YEAR_STRATIFIED_ESTIMATION =\nFALSE" in t
    assert t.rstrip().endswith("STOP.")
