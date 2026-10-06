from __future__ import annotations
import ast, hashlib, importlib.util, json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/"tests"/"fixtures"/"smf_ap1_m03_02_r1_post_m10_pcg_01_synthetic_cases_v0_1.json"
BREAKER=ROOT/"GOVERNANCE"/"SMF-AP1-M03-02-R1-POST-M10-PCG-01-FROZEN-SYNTHETIC-BREAKER-CONTRACT-V0.1.json"
RUNTIME=ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_pcg_01.py"
REFERENCE=ROOT/"tools"/"smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py"
EXPECTED_FIXTURE_SHA="12f8ec564b86a8db91df48b497a409871dbb719b31b8f96f949325ef31462b4c"

def load_json(p):
    return json.loads(p.read_text(encoding="ascii"))

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def mods():
    assert RUNTIME.exists(), "MISSING_IMPLEMENTATION:smf_ap1_m03_02_r1_post_m10_pcg_01.py"
    assert REFERENCE.exists(), "MISSING_REFERENCE:smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py"
    return load_module(RUNTIME,"pcg01_runtime"),load_module(REFERENCE,"pcg01_reference")

def fixtures():
    return load_json(FIX)["cases"]

def test_00_runtime_and_reference_exist():
    assert RUNTIME.exists(), "MISSING_IMPLEMENTATION:smf_ap1_m03_02_r1_post_m10_pcg_01.py"
    assert REFERENCE.exists(), "MISSING_REFERENCE:smf_ap1_m03_02_r1_post_m10_pcg_01_reference.py"

def test_01_fixture_identity_is_frozen_and_synthetic():
    raw=FIX.read_bytes()
    doc=load_json(FIX)
    assert hashlib.sha256(raw).hexdigest()==EXPECTED_FIXTURE_SHA
    assert doc["status"]=="FROZEN_BEFORE_RUNTIME_IMPLEMENTATION"
    assert doc["synthetic_only"] is True
    assert doc["contains_real_market_values"] is False
    assert doc["case_count"]==32
    b=load_json(BREAKER)
    assert b["fixture_sha256"]==EXPECTED_FIXTURE_SHA
    assert b["fixture_case_count"]==32
    assert b["breaker_count"]==46

def test_02_exact_pcg00_bindings_are_embedded():
    r,_=mods()
    assert r.PCG00_BINDINGS=={
      "contract_blob":"8e6e888f8330e40d792b43650c32b09a8dc6a281",
      "decision_table_blob":"da9bb3a7436072795fced2d171cae8df23591279",
      "breaker_contract_blob":"c52eca89c45fd68e83c506925626a3c389b5d4a2",
      "traceability_blob":"364baff4a603c9be69f29742ba2647477742974f",
      "final_receipt_blob":"769fcc81f4b365b4a54152042be31a2dd1ce9412",
      "final_closure_blob":"4433648fb71684695513eddb2c60c4eddae41b6a"
    }

def test_03_all_fixture_expectations_and_reference_parity():
    r,o=mods()
    for case in fixtures():
        p=case["packet"]
        e=case["expected"]
        if e["kind"]=="error":
            with pytest.raises(r.PCGFailClosedError) as rr:
                r.evaluate(p)
            with pytest.raises(o.PCGFailClosedError) as oo:
                o.reference_evaluate(p)
            assert rr.value.code==e["error_code"], case["id"]
            assert oo.value.code==e["error_code"], case["id"]
        else:
            actual=r.evaluate(p)
            ref=o.reference_evaluate(p)
            assert actual==ref, case["id"]
            assert actual["gate_state"]==e["gate_state"], case["id"]
            assert actual["overall_gate_admissibility"]==e["overall_gate_admissibility"], case["id"]
            assert actual["qualifying_routes"]==e["qualifying_routes"], case["id"]
            assert actual["block_reason"]==e["block_reason"], case["id"]
            assert actual["authority_created"]=="NONE", case["id"]

def test_04_full_result_contract_is_present_for_valid_cases():
    r,_=mods()
    required={
      "claim_unit","downstream_claim_id","downstream_analysis_id","requested_temporal_scope",
      "input_classification","selected_route","gate_state","route_states","decision_reason",
      "block_reason","binding_references","authority_created","qualifying_routes",
      "overall_gate_admissibility","method_state","real_data_read"
    }
    for case in fixtures():
        if case["expected"]["kind"]=="result":
            out=r.evaluate(case["packet"])
            assert required <= set(out), case["id"]

def test_05_only_frozen_gate_states_are_emitted():
    r,_=mods()
    allowed={
      "NOT_APPLICABLE","BLOCKED","ROUTE_A_PENDING","ROUTE_B_PENDING","ROUTE_C_PENDING",
      "ADMISSIBLE_BY_ROUTE_A","ADMISSIBLE_BY_ROUTE_B","ADMISSIBLE_BY_ROUTE_C",
      "NON_MATERIAL_POOLING_REVIEW_REQUIRED"
    }
    for case in fixtures():
        if case["expected"]["kind"]=="result":
            assert set(r.evaluate(case["packet"])["gate_state"]) <= allowed

def test_06_multiple_route_provenance_has_no_silent_priority():
    r,_=mods()
    by={x["id"]:x for x in fixtures()}
    a=r.evaluate(by["D17_MULTI_A_B_VALID"]["packet"])
    assert a["selected_route"]=="MULTIPLE"
    assert a["route_states"]=={"A":"ADMISSIBLE_BY_ROUTE_A","B":"ADMISSIBLE_BY_ROUTE_B"}
    assert a["qualifying_routes"]==["A","B"]
    assert a["overall_gate_admissibility"]=="ADMISSIBLE"
    b=r.evaluate(by["D18_MULTI_PENDING_AND_VALID"]["packet"])
    assert b["route_states"]=={"A":"ROUTE_A_PENDING","B":"ADMISSIBLE_BY_ROUTE_B"}
    assert b["qualifying_routes"]==["B"]
    assert b["overall_gate_admissibility"]=="ADMISSIBLE"

def test_07_hard_blocker_precedence():
    r,_=mods()
    by={x["id"]:x for x in fixtures()}
    for cid in ("D13_RESET_PRISTINE","D14_M05_AUTHORITY","D15_METHOD_EXECUTION","D16_REAL_DATA_DEPENDENCY","D20_CROSS_CLAIM","D21_CROSS_METRIC"):
        out=r.evaluate(by[cid]["packet"])
        assert out["gate_state"]==["BLOCKED"]
        assert out["overall_gate_admissibility"]=="BLOCKED"
        assert out["qualifying_routes"]==[]

def test_08_method_states_and_authority_never_expand():
    r,_=mods()
    expected={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    for case in fixtures():
        if case["expected"]["kind"]=="result":
            out=r.evaluate(case["packet"])
            assert out["method_state"]==expected
            assert out["authority_created"]=="NONE"
            assert out["real_data_read"] is False

def test_09_deterministic_replay_exact_bytes():
    r,_=mods()
    for case in fixtures():
        if case["expected"]["kind"]=="result":
            outputs=[r.canonical_json_bytes(r.evaluate(case["packet"])) for _ in range(5)]
            assert len(set(outputs))==1, case["id"]

def test_10_reference_is_independent_and_does_not_import_runtime():
    src=REFERENCE.read_text(encoding="utf-8")
    assert "smf_ap1_m03_02_r1_post_m10_pcg_01" not in src
    assert "pcg01_runtime" not in src

def test_11_runtime_and_reference_have_no_clock_random_network_or_filesystem_reads():
    forbidden_import_roots={"time","random","socket","requests","urllib","http","os","pathlib"}
    for path in (RUNTIME,REFERENCE):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        roots=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node,ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        assert not (roots & forbidden_import_roots), (path,roots & forbidden_import_roots)
        src=path.read_text(encoding="utf-8")
        assert "open(" not in src
        assert ".read_text(" not in src
        assert ".read_bytes(" not in src

def test_12_no_real_pcg_result_artifact_exists():
    art=ROOT/"artifacts"
    if art.exists():
        assert not list(art.glob("*pcg_01*"))
        assert not list(art.glob("*PCG-01*"))

def test_13_runtime_source_contains_no_real_data_identifiers():
    src=RUNTIME.read_text(encoding="utf-8").lower()
    forbidden=[
      "m03-r1-real","m10_real_result","ap0","broker data","market data path",
      "atds-control","oos data path"
    ]
    for x in forbidden:
        assert x not in src

def test_14_breaker_contract_keeps_real_application_closed():
    b=load_json(BREAKER)
    assert b["runtime_implementation_authorized"] is True
    assert b["real_gate_application_authorized"] is False
    assert b["real_data_read_authorized"] is False
    assert b["statistical_method_execution_authorized"] is False
    assert b["real_market_result_authorized"] is False

def test_15_canonical_serializer_is_stable_and_ascii():
    r,_=mods()
    by={x["id"]:x for x in fixtures()}
    raw=r.canonical_json_bytes(r.evaluate(by["D17_MULTI_A_B_VALID"]["packet"]))
    raw.decode("ascii")
    assert raw.endswith(b"\n")
