from __future__ import annotations
import hashlib, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"/"smf_ap1_m03_02_r1_post_m10_dre_03"
REPORTS=ROOT/"reports"/"program"
PRIMARY=ART/"REAL_PRIMARY_RESULT.json"; REFERENCE=ART/"REAL_REFERENCE_RESULT.json"
PARITY=ART/"REAL_REFERENCE_PARITY.json"; SOURCE=ART/"REAL_SOURCE_IDENTITY_RECEIPT.json"
EXEC=REPORTS/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DRE-03-REAL-EXECUTION-RECEIPT-V0.1.json"
ENV=REPORTS/"2026-10-07-SMF-AP1-M03-02-R1-POST-M10-DRE-03-REAL-EXECUTION-ENVIRONMENT-MANIFEST-V0.1.json"
BREAKERS=ROOT/"GOVERNANCE"/"SMF-AP1-M03-02-R1-POST-M10-DRE-01-FROZEN-BREAKER-CONTRACT-V0.1.json"
EXPECTED_RESULT_SHA="d965cec1a01c7d130a49974b481abf43b874835be999460df93becbb452d556f"
EXPECTED_SOURCE_SHA="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def test_01_primary_reference_bytes_exact():
 assert PRIMARY.read_bytes()==REFERENCE.read_bytes()
 assert hashlib.sha256(PRIMARY.read_bytes()).hexdigest()==EXPECTED_RESULT_SHA
def test_02_result_schema_and_vector_shape():
 r=load(PRIMARY); assert r["status"]=="DRE01_COMPLETE"; assert r["schema"]=="ATDS_SMF_AP1_M03_02_R1_POST_M10_DRE_01_YEAR_STRATIFIED_REFERENCE_VECTOR_V0_1"; assert r["vector_order"]==["R_2022","R_2023","R_2024","R_2025"]; assert r["relation_between_components"]=="A_CONDITIONED_REFERENCE_VECTOR"; assert r["aggregation"]=="NONE"; assert [x["id"] for x in r["components"]]==r["vector_order"]; assert len(r["components"])==4; assert all(isinstance(x["n"],int) and not isinstance(x["n"],bool) and x["n"]>0 for x in r["components"]); assert all(isinstance(x["value"],(int,float)) and not isinstance(x["value"],bool) and math.isfinite(float(x["value"])) for x in r["components"])
def test_03_source_identity_exact_and_single_read():
 s=load(SOURCE); assert s["exact_match"] is True; assert s["expected_sha256"]==EXPECTED_SOURCE_SHA; assert s["observed_sha256"]==EXPECTED_SOURCE_SHA; assert s["source_read_count"]==1; assert s["source_copy_count"]==0; assert s["alternate_source_read_count"]==0; assert s["raw_ap0_read_count"]==0; assert s["m03_reexecution_count"]==0; assert s["real_source_has_been_exposed"] is True
def test_04_execution_counts_and_authority_ceiling():
 e=load(EXEC); assert e["status"]=="REAL_EXECUTION_TECHNICALLY_QUALIFIED"; assert e["primary_real_execution_count"]==1; assert e["reference_real_execution_count"]==1; assert e["retry_count"]==0; assert e["retry_authorized"] is False; assert e["primary_reference_semantic_parity"]=="EXACT"; assert e["primary_reference_canonical_byte_parity"]=="EXACT"; assert e["primary_result_sha256"]==EXPECTED_RESULT_SHA; assert e["reference_result_sha256"]==EXPECTED_RESULT_SHA; assert e["human_scientific_adoption"]=="NOT_YET_PRONOUNCED"; assert e["method_authority"] is False; assert e["method_execution_authority"] is False; assert e["oos_authority"] is False; assert e["trading_authority"] is False; assert e["capital_authority"] is False; assert e["automatic_downstream_action"] is False
def test_05_parity_receipt_exact():
 p=load(PARITY); assert p["semantic_object_parity"]=="EXACT"; assert p["canonical_byte_parity"]=="EXACT"; assert p["sha256_parity"]=="EXACT"; assert p["primary_result_sha256"]==EXPECTED_RESULT_SHA; assert p["reference_result_sha256"]==EXPECTED_RESULT_SHA
def test_06_environment_frozen_before_read():
 e=load(ENV); assert e["status"]=="PRE_REAL_READ_FROZEN"; assert e["bindings"]["primary_runtime_blob"]=="adf8b5bd885c4e8fc2b06c5d33e1df8638e8c28f"; assert e["bindings"]["reference_runtime_blob"]=="cb9fc6e54d40f1d59257f345cfae2648423883a7"; assert e["real_source"]["expected_sha256"]==EXPECTED_SOURCE_SHA; assert e["real_source"]["read_budget"]==1; assert e["execution_budget"]=={"primary_real_execution":1,"independent_reference_real_execution":1,"retry":0}
def test_07_all_69_breakers_still_normative():
 b=load(BREAKERS); assert b["breaker_count"]==69; assert len(b["breakers"])==69
def test_08_no_raw_real_source_committed():
 forbidden="M03-R1-REAL-e73a24ca.json"; assert [p for p in ROOT.rglob("*") if p.is_file() and p.name==forbidden]==[]
def test_09_epistemic_state_preserved():
 r=load(PRIMARY); assert r["epistemic_state"]=={"claim_provenance":"RESULT_AWARE","evidence_state":"EXPOSED","reset_to_pristine":"FORBIDDEN","same_corpus_confirmatory_status":"NON_PRISTINE"}
def test_10_no_result_authority_promotion():
 r=load(PRIMARY); assert r["authority"]=={"authority_created":"NONE","capital":False,"method":False,"method_execution":False,"oos":False,"trading":False}
