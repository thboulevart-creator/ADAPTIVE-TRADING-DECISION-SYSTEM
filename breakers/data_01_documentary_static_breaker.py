"""DATA-01 documentary/static qualification breaker.

This breaker validates only frozen design semantics and exact repository identities.
It does not read real market datasets, execute a backtest, consume OOS, or modify
any Data/Temporal/owner runtime.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQ_PATH = ROOT / "GOVERNANCE/DATA-01-FIRST-USE-DATA-REQUIREMENTS-MAP-V0.1.json"
CONTRACT_PATH = ROOT / "GOVERNANCE/DATA-01-CLAIM-SCOPED-DATA-ADMISSIBILITY-PROVENANCE-CONTRACT-V0.1.json"
BOUNDARY_PATH = ROOT / "GOVERNANCE/DATA-01-DATA-TEMPORAL-OWNERSHIP-BOUNDARY-V0.1.md"
BREAKER_PATH = ROOT / "GOVERNANCE/DATA-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json"

EXPECTED = {
    "GOVERNANCE/DATA-01-FIRST-USE-DATA-REQUIREMENTS-MAP-V0.1.json": "2d6d43d783281ee3dfd4028bc9b84c4dce495b87",
    "GOVERNANCE/DATA-01-CLAIM-SCOPED-DATA-ADMISSIBILITY-PROVENANCE-CONTRACT-V0.1.json": "ec013c8db53b482770a62016db50b113b19ecd7f",
    "GOVERNANCE/DATA-01-DATA-TEMPORAL-OWNERSHIP-BOUNDARY-V0.1.md": "4bdb9d6c7448759c0349048fd4f48abba296c0cf",
    "GOVERNANCE/DATA-01-FROZEN-ADVERSARIAL-BREAKER-CONTRACT-V0.1.json": "d9cafc53c863341ca827097014411702c26633f2",
    "tools/ap0_ustech_profile_minute_core.py": "42fcb38809a1cc0365cd4027fae5154e1d6d3b4f",
    "tools/ap1_intraday_spread_census.py": "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a",
    "reports/program/2026-09-25-AP0-USTECH-PROFILE-MINUTE-CORE-ADJUDICATION.md": "94bba3315e3569993623b8cd2a2bf4264f4ab6f8",
    "reports/data-qualification/source_b_price_core_data_truth_closure_2026-09-25.md": "62e9bd1e0892dab7273eed35c8704a9e05611112",
    "reports/program/2026-09-28-E1-03-REAL-H1-QUALIFICATION.md": "534233d63a01c42c6b4de8979cca8dcb2feb7bc7",
    "tools/e1_03_h1_dataset_identity.py": "38d481755e00ce3c2ed9c66c4db710500ca0911a",
    "src/data/dataset_admissibility.py": "63f629a8cf39c79b5334015e038b70771c39f78b",
    "src/data/tick_reader.py": "ee80355504e14e1ac7f70b7481b3e9a980d7dc30",
    "docs/05-DATA-CONTRACT.md": "e7426c6c5ee4a122aecc8c8719f9cdd9173841e7",
    "docs/09-DATASET-PROVENANCE-REGISTRY.md": "89763a279e957afd0e9a1e3933a2d582df58dda3",
    "docs/10-TEMPORAL-POINT-IN-TIME-CONTRACT.md": "861362264a3602aa875bb16487d12558f700c250",
}

def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

REQ = _json(REQ_PATH)
CONTRACT = _json(CONTRACT_PATH)
BREAKER = _json(BREAKER_PATH)
BOUNDARY = BOUNDARY_PATH.read_text(encoding="utf-8")

def _git_blob(path: str) -> str:
    return subprocess.check_output(["git", "hash-object", path], cwd=ROOT, text=True).strip()

def test_data01_01_exact_bound_blobs():
    for path, expected in EXPECTED.items():
        assert _git_blob(path) == expected, path

def test_data01_02_first_use_selection_is_exact_ap0():
    assert REQ["selection"]["result"] == "SELECTED"
    assert REQ["selection"]["dataset_identity"] == "USTECH_PROFILE_MINUTE_CORE_V0_1"
    assert REQ["selection"]["dataset_family"] == "AP0_GAP_AWARE_1_MINUTE_MONTHLY_PARQUET"
    assert REQ["selection"]["manifest_sha256"] == "62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce"

def test_data01_03_first_consumer_is_canonical_ap1():
    target = REQ["target"]
    assert target["rvo_claim_class"] == "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
    assert target["semantic_limit"] == "RETROSPECTIVE_DESCRIPTIVE_ONLY"
    assert target["first_canonical_consumer"]["id"] == "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    assert target["first_canonical_consumer"]["runtime_blob"] == "9f613063fb8a190a1ff6f2f8b12c97c4ed97712a"

def test_data01_04_exact_full_schema_is_material():
    exact = REQ["consumer_schema_requirement"]
    assert exact["full_schema_exact_match_required"] is True
    assert len(exact["exact_schema"]) == 14
    assert exact["rule"] == "UNREAD_COLUMNS_REMAIN_SCHEMA_MATERIAL_BECAUSE_THE_FIRST_CONSUMER_REQUIRES_EXACT_FULL_SCHEMA"
    assert CONTRACT["selected_dataset"]["schema_requirement"] == "EXACT_FULL_SCHEMA_REQUIRED_BY_FIRST_USE_CONSUMER"

def test_data01_05_raw_source_is_parent_not_forced_first_consumer():
    raw = REQ["inspected_surfaces"]["source_b_price_core"]
    assert raw["identity"] == "SOURCE_B_USTECH_PRICE_CORE_V0_1"
    assert raw["selection_status"] == "PARENT_NOT_FIRST_USE_CONSUMER"

def test_data01_06_h1_is_not_selected_for_convenience():
    h1 = REQ["inspected_surfaces"]["e1_h1"]
    assert h1["state"] == "QUALIFIED_E1_SPECIFIC_DERIVATION"
    assert h1["selection_status"] == "NOT_SELECTED"

def test_data01_07_tick_csv_available_is_not_selection_authority():
    tick = REQ["inspected_surfaces"]["generic_tick_csv_runtime"]
    assert tick["state"] == "AVAILABLE_RUNTIME_NOT_SELECTED_FIRST_USE_CORPUS"
    assert tick["selection_status"] == "NOT_SELECTED"

def test_data01_08_identity_is_not_filename():
    assert CONTRACT["identity_semantics"]["rule"] == "FILENAME != DATASET_IDENTITY"
    assert CONTRACT["identity_semantics"]["same_dataset_id_different_bytes"] == "FORBIDDEN"
    assert CONTRACT["result_to_dataset_binding"]["filename_only_binding"] == "FORBIDDEN"

def test_data01_09_parent_pass_does_not_flow_to_child():
    assert CONTRACT["provenance_semantics"]["parent_pass_inheritance"] == "FORBIDDEN"
    assert CONTRACT["admissibility_semantics"]["parent_pass_implies_child_pass"] is False

def test_data01_10_missing_lineage_is_unknown_not_no_parent():
    assert CONTRACT["provenance_semantics"]["missing_lineage_rule"] == "LINEAGE_UNKNOWN_NOT_NO_PARENT"

def test_data01_11_missing_provenance_cannot_pass():
    assert CONTRACT["provenance_semantics"]["missing_provenance_rule"] == "UNVERIFIED_OR_BLOCKED_NEVER_PASS"
    assert CONTRACT["admissibility_semantics"]["absence_of_check"] == "NOT_PASS"

def test_data01_12_usage_scope_is_exact_cc02():
    usage = CONTRACT["usage_envelope"]
    assert usage["permitted_claim_class"] == "CC02_DESCRIPTIVE_MARKET_BEHAVIOR"
    assert usage["permitted_first_use"] == "ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1"
    assert usage["cross_claim_reuse_rule"] == "REQUIRES_NEW_APPLICABILITY_AND_USAGE_EVALUATION"

def test_data01_13_subminute_claim_not_laundered_through_ap0():
    assert CONTRACT["usage_envelope"]["subminute_claim_rule"].startswith("AP0_IS_NOT_UNIVERSALLY_SUFFICIENT")

def test_data01_14_mid_and_tick_count_semantics_are_bounded():
    meta = CONTRACT["selected_dataset"]["metadata_semantics"]
    assert meta["mid_semantics"] == "descriptive_only_not_execution_price"
    assert meta["volumes_used"] is False
    assert "execution price" in CONTRACT["usage_envelope"]["prohibited_semantics"]
    assert "traded volume" in CONTRACT["usage_envelope"]["prohibited_semantics"]

def test_data01_15_result_binding_is_content_addressed():
    fields = set(CONTRACT["result_to_dataset_binding"]["minimum_fields"])
    assert {"dataset_identity","ap0_manifest_sha256","dataset_file_set_digest_or_exact_61_file_hash_set","schema_identity","source_identity","transformer_blob","result_identity"} <= fields
    assert CONTRACT["result_to_dataset_binding"]["required"] is True

def test_data01_16_temporal_firewall_is_explicit():
    assert CONTRACT["temporal_firewall"]["current_first_use_state"] == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
    assert "known_from" in CONTRACT["temporal_firewall"]["temporal_owner_only"]
    assert "historical point-in-time availability" in CONTRACT["temporal_firewall"]["temporal_owner_only"]
    assert "TEMPORAL_OWNER_REQUIRED" in CONTRACT["temporal_firewall"]["expansion_rule"]

def test_data01_17_temporal_not_applicable_is_not_pass():
    assert "NOT_APPLICABLE != PASS" in BREAKER["invariants"]
    assert "NOT_APPLICABLE != PASS" in BOUNDARY

def test_data01_18_status_preservation_is_frozen():
    inv = set(BREAKER["invariants"])
    assert {"UNKNOWN != PASS","UNVERIFIED != PASS","BLOCKED != FAIL","AVAILABLE != QUALIFIED"} <= inv

def test_data01_19_breaker_inventory_is_complete_and_unique():
    ids = [x["id"] for x in BREAKER["cases"]]
    assert ids == [f"DATA01-B{i:02d}" for i in range(1, 33)]
    assert len(ids) == len(set(ids)) == 32
    assert set(BREAKER["classes"]) == {x["class"] for x in BREAKER["cases"]}

def test_data01_20_required_attack_families_are_present():
    attacks = " ".join(x["attack"] for x in BREAKER["cases"]).lower()
    for phrase in (
        "same filename",
        "same declared dataset id",
        "silently substituted",
        "inherits source_b parent pass",
        "missing provenance",
        "missing parent/lineage",
        "schema drifts",
        "row/domain corruption",
        "minute ordering",
        "transformation ambiguity",
        "unverified source",
        "usage envelope",
        "historically available",
        "result lacks binding",
        "mutable commentary",
        "unknown or unverified",
        "rvo description",
        "scientific/trading authority",
    ):
        assert phrase in attacks, phrase

def test_data01_21_breaker_is_design_only():
    auth = BREAKER["authority"]
    assert auth["executable_data_implementation_authorized"] is False
    assert auth["data_runtime_modification_authorized"] is False
    assert auth["real_data_consumption_authorized"] is False
    assert auth["real_experiment_authorized"] is False
    assert auth["oos_consumption_authorized"] is False
    assert BREAKER["stop_boundary"] == "STOP_BEFORE_DATA02_OR_ANY_DATA_RUNTIME_IMPLEMENTATION"

def test_data01_22_data_contract_has_no_temporal_authority():
    auth = CONTRACT["authority"]
    assert auth["temporal_authority"] is False
    assert auth["scientific_authority"] is False
    assert auth["trading_authority"] is False
    assert auth["implementation_authority"] is False
    assert auth["rvo_authority"] == "NONE"

def test_data01_23_current_temporal_na_has_explicit_basis_only_for_current_claim():
    temporal = REQ["current_claim_temporal_requirement"]
    assert temporal["state"] == "NOT_APPLICABLE_WITH_EXPLICIT_BASIS"
    assert "retrospective descriptive only" in temporal["basis"]
    assert "historical tradability" in temporal["firewall"]

def test_data01_24_no_universal_data_abstraction_claim():
    assert "not a universal assertion" in REQ["selection"]["selection_scope_only"]
    assert CONTRACT["admissibility_semantics"]["admissible_for_this_claim_implies_all_claims"] is False

def test_data01_25_next_boundaries_remain_closed():
    assert CONTRACT["next_boundary"]["status"] == "NOT_AUTHORIZED"
    assert "DATA RUNTIME MODIFICATION =\nNOT AUTHORIZED" in BOUNDARY
    assert "REAL EMPIRICAL EXPERIMENT =\nNOT AUTHORIZED" in BOUNDARY
