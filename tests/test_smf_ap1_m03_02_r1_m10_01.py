from __future__ import annotations
import hashlib, json, pathlib, subprocess

ROOT=pathlib.Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"/"smf_ap1_m03_02_r1_m10_01"
RESULT=ART/"REAL_M10_RESULT.json"
REFERENCE=ART/"REAL_M10_REFERENCE_RESULT.json"
PARITY=ART/"REAL_REFERENCE_PARITY.json"
MANIFEST=ART/"RUN_MANIFEST.json"
EXPECTED_INPUT_SHA="7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e"
EXPECTED_OUTPUT_SHA="af136e218e31066d9eac756bae9b5a683d01948ed92aaa58b8a9c1101f1946c9"
EXPECTED_RUNTIME_BLOB="c1765a56d6c861522db02af6200b7072ce621799"
EXPECTED_REFERENCE_BLOB="2ddc0f69425d0a8349eb43b26f956f4159b76d93"
EXPECTED_M01_BLOB="2293c665a2d30c520056c7814aec6a9dc79d68d1"

def load(p): return json.loads(p.read_text(encoding="ascii"))
def git_sha(p):
    rel=p.relative_to(ROOT).as_posix()
    b=subprocess.check_output(["git","-C",str(ROOT),"show",f"HEAD:{rel}"])
    return hashlib.sha256(b).hexdigest()
def claim_map(r): return {(x["metric"],x["probability"]):x for x in r["claim_units"]}

def test_01_exact_input_and_output_identities():
    m=load(MANIFEST)
    assert m["input"]["sha256"]==EXPECTED_INPUT_SHA
    assert m["execution"]["real_result_sha256"]==EXPECTED_OUTPUT_SHA
    assert git_sha(RESULT)==EXPECTED_OUTPUT_SHA

def test_02_exact_procedure_identities():
    m=load(MANIFEST)
    ids=m["identities"]
    assert ids["m10_runtime_blob"]==EXPECTED_RUNTIME_BLOB
    assert ids["m10_reference_blob"]==EXPECTED_REFERENCE_BLOB
    assert ids["m01_contract_blob"]==EXPECTED_M01_BLOB

def test_03_exact_11_claim_units_and_33_contrasts():
    r=load(RESULT)
    assert len(r["claim_units"])==11
    assert sum(len(x["contrasts"]) for x in r["claim_units"])==33

def test_04_exact_primary_transitions():
    r=load(RESULT)
    assert r["transitions"]==["2022->2023","2023->2024","2024->2025"]
    for u in r["claim_units"]:
        assert [c["transition"] for c in u["contrasts"]]==r["transitions"]

def test_05_exact_claim_unit_statuses():
    r=claim_map(load(RESULT))
    material={
      ("tick_count",0.5),("tick_count",0.9),("tick_count",0.99),
      ("minute_range",0.5),("minute_range",0.9),("minute_range",0.95),("minute_range",0.99),
      ("spread_mean",0.5),
    }
    no_material={
      ("spread_mean",0.9),("spread_mean",0.95),("spread_mean",0.99),
    }
    assert set(r)==material|no_material
    assert all(r[k]["status"]=="MATERIAL_TEMPORAL_VARIATION" for k in material)
    assert all(r[k]["status"]=="NO_MATERIAL_TEMPORAL_VARIATION_DETECTED" for k in no_material)

def test_06_no_blocked_claim_units_or_contrasts():
    r=load(RESULT)
    assert all(u["status"]!="BLOCKED" for u in r["claim_units"])
    assert all(c["status"]!="BLOCKED" for u in r["claim_units"] for c in u["contrasts"])

def test_07_materiality_rule_is_respected_in_persisted_result():
    r=load(RESULT)
    for u in r["claim_units"]:
        for c in u["contrasts"]:
            assert c["r"] is not None
            assert (c["status"]=="MATERIAL") == (c["r"]>=0.20)

def test_08_claim_unit_any_material_rule_is_respected():
    r=load(RESULT)
    for u in r["claim_units"]:
        has_material=any(c["status"]=="MATERIAL" for c in u["contrasts"])
        expected="MATERIAL_TEMPORAL_VARIATION" if has_material else "NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
        assert u["status"]==expected

def test_09_summary_counts_exact():
    m=load(MANIFEST)["summary"]
    assert m=={
      "blocked_claim_units":0,
      "blocked_contrasts":0,
      "claim_units":11,
      "contrasts":33,
      "material_claim_units":8,
      "material_contrasts":20,
      "no_material_variation_claim_units":3,
      "non_material_contrasts":13,
    }

def test_10_reference_parity_exact():
    p=load(PARITY)
    assert p["status"]=="PASS"
    assert p["exact_object_equality"] is True
    assert p["exact_canonical_byte_equality"] is True
    assert p["runtime_result_sha256"]==EXPECTED_OUTPUT_SHA
    assert p["reference_result_sha256"]==EXPECTED_OUTPUT_SHA
    assert RESULT.read_bytes()==REFERENCE.read_bytes()
    assert git_sha(REFERENCE)==EXPECTED_OUTPUT_SHA

def test_11_no_global_verdict():
    r=load(RESULT)
    forbidden={"global_verdict","global_pass","global_fail","overall_stable","overall_unstable","strategy_valid","strategy_invalid"}
    assert forbidden.isdisjoint(r.keys())

def test_12_epistemic_ceiling_and_authority():
    r=load(RESULT)
    m=load(MANIFEST)
    assert r["epistemic_limit"]=="EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"
    assert m["epistemic_limit"]=="EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"
    assert r["authority"]=={"scientific_execution":False,"trading":False,"capital":False}
    assert m["authority"]=={"trading":False,"capital":False}
    assert m["scientific_adjudication"]=="PENDING_HUMAN_DECISION"

def test_13_single_runtime_and_reference_execution_recorded():
    e=load(MANIFEST)["execution"]
    assert e["runtime_execution_count"]==1
    assert e["independent_reference_execution_count"]==1
    assert e["reference_parity"]=="PASS"

def test_14_result_exposure_and_closed_next_authority():
    m=load(MANIFEST)
    assert m["m10_result_exposed"] is True
    assert m["global_cross_metric_verdict"]=="FORBIDDEN"

def test_15_no_unauthorized_artifact_surface():
    names={p.name for p in ART.iterdir()}
    assert names=={"REAL_M10_RESULT.json","REAL_M10_REFERENCE_RESULT.json","REAL_REFERENCE_PARITY.json","RUN_MANIFEST.json"}
