from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
G = ROOT / "GOVERNANCE"

def load(name: str):
    return json.loads((G / name).read_text(encoding="utf-8-sig"))

def test_human_materiality_adjudication_exact():
    h = load("SMF-AP1-M03-02-R1-M01-01-HUMAN-MATERIALITY-ADJUDICATION-V0.1.json")
    assert h["status"] == "HUMAN_ADOPTED"
    assert h["effect_scale"]["selected_option"] == "B"
    assert h["effect_scale"]["name"] == "SYMMETRIC_RELATIVE_CHANGE"
    assert h["effect_scale"]["zero_denominator"] == "UNDEFINED_BLOCKED"
    assert h["threshold"]["scope"] == "COMMON_TO_ALL_11_CLAIM_UNITS"
    assert h["threshold"]["value"] == 0.20
    assert h["claim_unit_rule"]["selected_rule"] == "A"
    assert h["claim_unit_rule"]["name"] == "ANY_ADJACENT_MATERIAL_SHIFT"
    assert h["claim_unit_rule"]["global_cross_metric_pass_fail"] == "FORBIDDEN"
    assert all(v is False for v in h["downstream_authority"].values())

def test_final_m01_contract_frozen_and_complete():
    c = load("SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.1.json")
    assert c["status"] == "M01_TEMPORAL_STABILITY_CLAIM_ESTIMAND_FROZEN"
    assert c["freeze_status"] == "FROZEN"
    assert c["materiality_adjudication_status"] == "HUMAN_ADOPTED_AND_FROZEN"
    assert c["m01_readiness"] == "COMPLETE"
    assert c["unresolved_material_parameters"] == []
    assert c["primary_estimands"]["claim_units"] == 11
    assert c["primary_contrasts"]["total_contrasts"] == 33
    assert c["primary_estimands"]["global_pass_forbidden"] is True
    assert c["m10_authorized"] is False
    assert c["m10_executed"] is False
    assert c["authority"]["scientific_method_execution"] is False

def test_materiality_boundary_semantics_exact():
    c = load("SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.1.json")
    m = c["materiality_boundary"]
    assert m["status"] == "HUMAN_ADOPTED_AND_FROZEN"
    assert m["effect_scale"] == "SYMMETRIC_RELATIVE_CHANGE"
    assert m["zero_denominator"] == "UNDEFINED_BLOCKED"
    assert m["threshold_scope"] == "COMMON_TO_ALL_11_CLAIM_UNITS"
    assert m["threshold"] == 0.20
    assert m["contrast_material_rule"] == "R >= 0.20"
    assert m["contrast_below_materiality_rule"] == "R < 0.20"
    assert m["claim_unit_rule"] == "ANY_ADJACENT_MATERIAL_SHIFT"
    assert m["decision_precedence"] == [
        "IF_ANY_REQUIRED_CONTRAST_UNDEFINED_OR_BLOCKED => BLOCKED",
        "ELSE_IF_ANY_ADJACENT_R_GTE_0_20 => MATERIAL_TEMPORAL_VARIATION",
        "ELSE => NO_MATERIAL_TEMPORAL_VARIATION_DETECTED",
    ]
    assert m["global_cross_metric_pass_fail"] == "FORBIDDEN"

def test_epistemic_and_dependency_boundaries_preserved():
    c = load("SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.1.json")
    assert c["provenance"]["claim_origin"] == "EXPLORATORY_RESULT_DERIVED"
    assert c["epistemic_limits"]["retroactive_confirmatory_preregistration"] is False
    assert c["epistemic_limits"]["same_corpus_m10_maximum_semantics"] == "EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE"
    assert c["population"]["primary_analysis"] == "COMPLETE_YEARS_ONLY"
    assert c["population"]["partial_year_role"] == "SENSITIVITY_DESCRIPTIVE_CONTEXT_ONLY"
    assert c["multiplicity"]["exists"] is True
    assert c["multiplicity"]["claim_units"] == 11
    assert c["multiplicity"]["adjacent_contrasts"] == 33
    for method in ("M04","M05","M08","M09","M10","M11"):
        assert c["dependency_map"][method]["authorized"] is False

def test_fm10_closed_by_human_boundary_without_method_execution():
    c = load("SMF-AP1-M03-02-R1-M01-01-TEMPORAL-STABILITY-CONTRACT-V0.1.json")
    fm10 = [x for x in c["failure_modes"] if x["id"] == "FM-10"][0]
    assert "HUMAN_ADOPTED_SYMMETRIC_RELATIVE_CHANGE" in fm10["disposition"]
    assert c["m10_authorized"] is False
    assert c["m10_executed"] is False
