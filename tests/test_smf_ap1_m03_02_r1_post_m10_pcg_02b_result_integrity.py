from __future__ import annotations
import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"/"smf_ap1_m03_02_r1_post_m10_pcg_02b"
PRIMARY=ART/"REAL_PCG_RESULT.json"
REFERENCE=ART/"REAL_PCG_REFERENCE_RESULT.json"
PARITY=ART/"REAL_REFERENCE_PARITY.json"
MANIFEST=ART/"RUN_MANIFEST.json"
RECORD=ROOT/"reports"/"program"/"2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02B-REAL-EXECUTION-RECORD-V0.1.json"

EXPECTED={
 "pcg02a_receipt":"9762fc6e85c9feb9a62a4e3a4fe9f4f0c1bad8bf",
 "pcg02a_closure":"8ff1a970245790173dab079c74cc445c1c5be571",
 "packet_blob":"bcf5258247b9ef08f732d42abe88ca7e0a9b9c55",
 "packet_sha256":"d0a4dde068a7fb460413120041f521597509b80736299af7dd21d7ad90531a99",
 "freeze_blob":"12dcbd725c7f436025938b694ed1b8f4fafbc7be",
 "freeze_sha256":"941ea0464b980a81db73813b51287c28dc6fc992fafe4cb3563be3634aed3e22",
 "runtime_blob":"2b4b96b755293c47efa89522e5509bda4f0c9c73",
 "reference_blob":"6567e3d7325bfa769e10bc5bf1497b6aa416e3ce",
 "breaker_blob":"82362c52e52da84d251faeaa12d943d3c236b8b5",
 "primary_sha256":"2e31a9f728417c3a7f599573b15555efb8cd33037a4c9e900e68238d1cbe6464",
 "reference_sha256":"2e31a9f728417c3a7f599573b15555efb8cd33037a4c9e900e68238d1cbe6464",
 "parity_sha256":"0babdae9a72c433ea4eb67f27f73110f758ed17880a4086dc606417185e2c06e",
 "manifest_sha256":"0fc38e9dfa8524959dd44523db9d9d5148367398a869a1d7c7db79659a4a2caf",
}

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def blob(path):
    return subprocess.check_output(["git","-C",str(ROOT),"rev-parse",f"HEAD:{path}"],text=True).strip()

def test_01_exact_existing_binding_objects():
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02A-FINAL-READINESS-RECEIPT-V0.1.json")==EXPECTED["pcg02a_receipt"]
    assert blob("reports/program/2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02A-FINAL-CLOSURE.md")==EXPECTED["pcg02a_closure"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-02A-FIRST-REAL-APPLICATION-PACKET-V0.1.json")==EXPECTED["packet_blob"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-02A-PRE-EXECUTION-FREEZE-V0.1.json")==EXPECTED["freeze_blob"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01.py")==EXPECTED["runtime_blob"]
    assert blob("tools/smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py")==EXPECTED["reference_blob"]
    assert blob("GOVERNANCE/SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json")==EXPECTED["breaker_blob"]

def test_02_result_artifact_hashes_are_exact():
    assert sha(PRIMARY)==EXPECTED["primary_sha256"]
    assert sha(REFERENCE)==EXPECTED["reference_sha256"]
    assert sha(PARITY)==EXPECTED["parity_sha256"]
    assert sha(MANIFEST)==EXPECTED["manifest_sha256"]

def test_03_primary_and_reference_are_semantically_identical():
    assert load(PRIMARY)==load(REFERENCE)

def test_04_primary_and_reference_are_byte_identical():
    assert PRIMARY.read_bytes()==REFERENCE.read_bytes()

def test_05_execution_counts_are_exactly_one_each_and_no_retry():
    m=load(MANIFEST)
    r=load(RECORD)
    assert m["primary_execution_count"]==1
    assert m["reference_execution_count"]==1
    assert r["execution_counts"]=={
        "primary_real_gate_execution":1,
        "independent_reference_execution":1,
        "retry_count":0,
    }

def test_06_result_is_exact_claim_scoped_input():
    r=load(PRIMARY)
    assert r["claim_unit"]=="tick_count p50"
    assert r["downstream_claim_id"]=="POST_M10-DC01-TICKCOUNT-P50-POOLED-HISTORICAL-REFERENCE"
    assert r["downstream_analysis_id"]=="POST_M10-DA01-POOLED-TICKCOUNT-P50-REFERENCE-CONSTRUCTION"
    assert r["requested_temporal_scope"]=="UTC_YEAR:2022|UTC_YEAR:2023|UTC_YEAR:2024|UTC_YEAR:2025"

def test_07_input_classification_is_exact():
    assert load(PRIMARY)["input_classification"]=="MATERIAL_TEMPORAL_VARIATION"

def test_08_selected_route_is_none():
    assert load(PRIMARY)["selected_route"]=="NONE"

def test_09_gate_state_is_blocked():
    assert load(PRIMARY)["gate_state"]==["BLOCKED"]
    assert load(PRIMARY)["overall_gate_admissibility"]=="BLOCKED"

def test_10_block_reason_is_exactly_no_admissibility_route():
    r=load(PRIMARY)
    assert r["decision_reason"]=="MATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE"
    assert r["block_reason"]=="MATERIAL_CLAIM_UNIT_NO_ADMISSIBILITY_ROUTE"

def test_11_no_route_state_or_qualifying_route_exists():
    r=load(PRIMARY)
    assert r["route_states"]=={}
    assert r["qualifying_routes"]==[]

def test_12_no_authority_is_created():
    assert load(PRIMARY)["authority_created"]=="NONE"

def test_13_methods_remain_closed():
    assert load(PRIMARY)["method_state"]=={
        "M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"
    }

def test_14_no_real_data_read():
    assert load(PRIMARY)["real_data_read"] is False
    assert load(MANIFEST)["real_market_data_read"] is False

def test_15_parity_is_exact():
    p=load(PARITY)
    assert p["primary_reference_semantic_parity"]=="EXACT"
    assert p["primary_reference_canonical_byte_parity"]=="EXACT"
    assert p["primary_result_sha256"]==EXPECTED["primary_sha256"]
    assert p["reference_result_sha256"]==EXPECTED["reference_sha256"]

def test_16_manifest_binds_exact_inputs_and_code():
    m=load(MANIFEST)
    assert m["packet_blob"]==EXPECTED["packet_blob"]
    assert m["packet_sha256"]==EXPECTED["packet_sha256"]
    assert m["pre_execution_freeze_blob"]==EXPECTED["freeze_blob"]
    assert m["pre_execution_freeze_sha256"]==EXPECTED["freeze_sha256"]
    assert m["runtime_blob"]==EXPECTED["runtime_blob"]
    assert m["reference_blob"]==EXPECTED["reference_blob"]
    assert m["breaker_blob"]==EXPECTED["breaker_blob"]

def test_17_no_downstream_execution_or_authority():
    m=load(MANIFEST)
    assert m["numerical_estimation"] is False
    assert m["pooling_execution"] is False
    assert m["conditioning_execution"] is False
    assert m["statistical_method_activation"] is False
    assert m["statistical_method_execution"] is False
    assert m["oos_consumption"] is False
    assert m["trading_authority"] is False
    assert m["capital_authority"] is False

def test_18_record_classifies_result_as_governance_only():
    r=load(RECORD)
    assert r["semantic_classification"]=="CLAIM_SCOPED_GOVERNANCE_GATE_RESULT"
    assert "SCIENTIFIC_FINDING" in r["prohibited_interpretations"]
    assert "NONSTATIONARITY_FINDING" in r["prohibited_interpretations"]
    assert "STRATEGY_VALIDATION" in r["prohibited_interpretations"]

def test_19_human_adjudication_is_pending():
    assert load(RECORD)["human_adjudication"]=="PENDING"

def test_20_test_file_cannot_execute_primary_or_reference_runtime():
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
    assert not any("pcg_01" in name for name in imports)
    assert not ({"evaluate","reference_evaluate","load_module"} & set(calls))

def test_21_result_binding_references_have_no_route_refs():
    b=load(PRIMARY)["binding_references"]
    assert b["pooling_justification_ref"] is None
    assert b["temporal_conditioning_spec_ref"] is None
    assert b["robust_method_preregistration_ref"] is None

def test_22_record_preserves_hard_authority_ceiling():
    d=load(RECORD)["downstream_state"]
    assert all(v is False for v in d.values())


FINAL_RECEIPT=ROOT/"reports"/"program"/"2026-10-06-SMF-AP1-M03-02-R1-POST-M10-PCG-02B-FINAL-EXECUTION-RECEIPT-V0.1.json"

def test_23_final_receipt_preserves_pending_human_adjudication_and_closed_pcg02c():
    r=load(FINAL_RECEIPT)
    v=r["verdict"]
    assert v["POST_M10_PCG_02B_EXECUTION"]=="QUALIFIED"
    assert v["POST_M10_PCG_02B_PRIMARY_EXECUTION"]=="PASS"
    assert v["POST_M10_PCG_02B_REFERENCE_EXECUTION"]=="PASS"
    assert v["POST_M10_PCG_02B_REFERENCE_PARITY"]=="PASS"
    assert v["POST_M10_PCG_02B_RESULT_INTEGRITY"]=="QUALIFIED"
    assert v["POST_M10_PCG_02B_GATE_RESULT"]=="PERSISTED"
    assert v["PCG_02B_HUMAN_ADJUDICATION"]=="PENDING"
    assert v["POOLING_EXECUTION"] is False
    assert v["CONDITIONING_EXECUTION"] is False
    assert v["REAL_DATA_READ"] is False
    assert v["NUMERICAL_ESTIMATION"] is False
    assert v["NEW_STATISTICAL_METHOD_ACTIVATED"] is False
    assert v["NEW_STATISTICAL_METHOD_EXECUTED"] is False
    assert v["NEW_MARKET_RESULT"] is False
    assert v["OOS_CONSUMPTION"] is False
    assert r["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert r["authority"]=={"trading":False,"capital":False}
    assert r["next_frontier"]["id"]=="SMF-AP1-M03-02-R1-POST-M10-PCG-02C"
    assert r["next_frontier"]["separate_human_decision_required"] is True
    assert r["next_frontier"]["automatic_adoption"] is False
    assert r["next_frontier"]["automatic_downstream_action"] is False
    assert r["next_frontier"]["opened"] is False
    assert r["stop"] is True
