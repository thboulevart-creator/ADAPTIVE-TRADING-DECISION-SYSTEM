"""RVO-04 static/adversarial breaker for claim routing and readiness design.

No real experiment, market-performance result, OOS data, broker state, or owner
mutation is performed here.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TAXONOMY_PATH = ROOT / "GOVERNANCE/RVO-04-CLAIM-CLASS-TAXONOMY-V0.1.json"
GRAPH_PATH = ROOT / "GOVERNANCE/RVO-04-CLAIM-CAPABILITY-GRAPH-V0.1.json"
GAPS_PATH = ROOT / "GOVERNANCE/RVO-04-OWNER-GAP-PRIORITIZATION-V0.1.json"
READINESS_PATH = ROOT / "GOVERNANCE/RVO-04-REAL-EXPERIMENT-READINESS-DESIGN-V0.1.md"
RVO03_MATRIX_PATH = ROOT / "GOVERNANCE/RVO-03-CANONICAL-OWNER-CAPABILITY-MATRIX-V0.1.json"
MCEPR_ACTIVATION_PATH = ROOT / "GOVERNANCE/MCEPR-ACTIVATION-CONTRACT-V0.2.json"

EXPECTED_CLAIMS = [
    "CC01_STRUCTURAL_PROTOCOL",
    "CC02_DESCRIPTIVE_MARKET_BEHAVIOR",
    "CC03_STATISTICAL_EFFECT",
    "CC04_PREDICTIVE",
    "CC05_ECONOMIC_NET_PROFITABILITY",
    "CC06_ROBUSTNESS_STABILITY",
    "CC07_MULTIPLICITY_MODEL_SELECTION",
    "CC08_HISTORICAL_POINT_IN_TIME",
    "CC09_PATH_RISK_RUIN",
    "CC10_OOS_CONFIRMATION",
]

def _json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

TAXONOMY = _json(TAXONOMY_PATH)
GRAPH = _json(GRAPH_PATH)
GAPS = _json(GAPS_PATH)
RVO03 = _json(RVO03_MATRIX_PATH)
MCEPR = _json(MCEPR_ACTIVATION_PATH)
READINESS = READINESS_PATH.read_text(encoding="utf-8")

def _route(claim_id):
    return next(x for x in GRAPH["routes"] if x["claim_class"] == claim_id)

def _req(claim_id):
    return {row[0]: row[1] for row in _route(claim_id)["requirements"]}

def _gap(gap_id):
    return next(x for x in GAPS["gaps"] if x["id"] == gap_id)

def test_rvo04_01_exact_claim_taxonomy():
    assert TAXONOMY["schema"] == "ATDS_RVO_04_CLAIM_CLASS_TAXONOMY_V0_1"
    ids = [x["id"] for x in TAXONOMY["claim_classes"]]
    assert ids == EXPECTED_CLAIMS
    assert len(ids) == len(set(ids)) == 10

def test_rvo04_02_graph_covers_taxonomy_once():
    ids = [x["claim_class"] for x in GRAPH["routes"]]
    assert ids == EXPECTED_CLAIMS
    assert len(ids) == len(set(ids))

def test_rvo04_03_requirement_vocabulary_is_closed():
    allowed = {"REQUIRED", "CONDITIONAL", "NOT_APPLICABLE"}
    for route in GRAPH["routes"]:
        assert all(row[1] in allowed for row in route["requirements"])

def test_rvo04_04_structural_claim_does_not_inherit_global_data_temporal_execution():
    req = _req("CC01_STRUCTURAL_PROTOCOL")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "NOT_APPLICABLE"
    assert req["TEMPORAL_PIT"] == "NOT_APPLICABLE"
    assert req["EXECUTION_GENERIC"] == "NOT_APPLICABLE"
    assert req["PCP_IDENTITY"] == "REQUIRED"
    assert req["PCP_EVIDENCE"] == "REQUIRED"

def test_rvo04_05_descriptive_claim_requires_data_but_not_execution():
    req = _req("CC02_DESCRIPTIVE_MARKET_BEHAVIOR")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "REQUIRED"
    assert req["EXECUTION_GENERIC"] == "NOT_APPLICABLE"
    assert req["TEMPORAL_PIT"] == "CONDITIONAL"

def test_rvo04_06_statistical_effect_requires_data_and_smf_core():
    req = _req("CC03_STATISTICAL_EFFECT")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "REQUIRED"
    assert req["SMF_CORE"] == "REQUIRED"
    assert req["P1_DOWNSTREAM_FINDING_CHAIN"] == "REQUIRED"

def test_rvo04_07_predictive_claim_cannot_bypass_temporal():
    req = _req("CC04_PREDICTIVE")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "REQUIRED"
    assert req["TEMPORAL_PIT"] == "REQUIRED"
    assert req["SMF_CORE"] == "REQUIRED"

def test_rvo04_08_economic_claim_cannot_use_effect_as_profitability():
    req = _req("CC05_ECONOMIC_NET_PROFITABILITY")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "REQUIRED"
    assert req["TEMPORAL_PIT"] == "REQUIRED"
    assert req["EXECUTION_GENERIC"] == "REQUIRED"
    assert req["SMF_CORE"] == "REQUIRED"

def test_rvo04_09_e1_specific_execution_is_not_generic_substitute():
    node = GRAPH["capability_nodes"]["EXECUTION_E1_SPECIFIC"]
    assert node["state"] == "QUALIFIED"
    assert node["generic_for_rvo"] is False
    assert GRAPH["capability_nodes"]["EXECUTION_GENERIC"]["state"] == "UNAVAILABLE"

def test_rvo04_10_robustness_inherits_base_claim_requirements():
    route = _route("CC06_ROBUSTNESS_STABILITY")
    assert route["inherits_base_claim_requirements"] is True
    assert _req("CC06_ROBUSTNESS_STABILITY")["SMF_CORE"] == "REQUIRED"

def test_rvo04_11_multiplicity_requires_mcepr_and_smf_m11_surface():
    req = _req("CC07_MULTIPLICITY_MODEL_SELECTION")
    assert req["MCEPR_REGISTRY"] == "REQUIRED"
    assert req["SMF_CORE"] == "REQUIRED"

def test_rvo04_12_historical_pit_requires_temporal_owner():
    req = _req("CC08_HISTORICAL_POINT_IN_TIME")
    assert req["TEMPORAL_PIT"] == "REQUIRED"
    assert GRAPH["capability_nodes"]["TEMPORAL_PIT"]["state"] == "UNAVAILABLE"

def test_rvo04_13_path_risk_requires_execution_and_conditional_smf():
    req = _req("CC09_PATH_RISK_RUIN")
    assert req["EXECUTION_GENERIC"] == "REQUIRED"
    assert req["SMF_CONDITIONAL"] == "REQUIRED"
    assert "C09" in req.__repr__() or "C09" in json.dumps(_route("CC09_PATH_RISK_RUIN"))

def test_rvo04_14_oos_requires_data_temporal_mcepr_and_separate_authority():
    route = _route("CC10_OOS_CONFIRMATION")
    req = _req("CC10_OOS_CONFIRMATION")
    assert req["DATA_EXACT_CLAIM_SURFACE"] == "REQUIRED"
    assert req["TEMPORAL_PIT"] == "REQUIRED"
    assert req["MCEPR_REGISTRY"] == "REQUIRED"
    assert req["SMF_CORE"] == "REQUIRED"
    assert route["authority_gate"] == "OOS_CONSUMPTION_REQUIRES_SEPARATE_EXPLICIT_HUMAN_AUTHORIZATION"

def test_rvo04_15_current_data_state_is_available_not_qualified():
    assert GRAPH["capability_nodes"]["DATA_EXACT_CLAIM_SURFACE"]["state"] == "AVAILABLE"
    rvo03 = {x["capability_id"]: x for x in RVO03["capabilities"]}
    assert rvo03["DATASET_ADMISSIBILITY_TICK_CSV"]["state"] == "AVAILABLE"

def test_rvo04_16_missing_generic_capabilities_are_not_laundered_to_na():
    assert GRAPH["capability_nodes"]["TEMPORAL_PIT"]["state"] == "UNAVAILABLE"
    assert GRAPH["capability_nodes"]["EXECUTION_GENERIC"]["state"] == "UNAVAILABLE"
    assert _req("CC04_PREDICTIVE")["TEMPORAL_PIT"] == "REQUIRED"
    assert _req("CC05_ECONOMIC_NET_PROFITABILITY")["EXECUTION_GENERIC"] == "REQUIRED"

def test_rvo04_17_conditional_smf_is_not_blanket_implemented():
    assert GRAPH["capability_nodes"]["SMF_CONDITIONAL"]["state"] == "BLOCKED"
    assert _gap("GAP-RVO04-07")["priority"] == "ON_DEMAND_ONLY"
    assert "Do not implement C01-C12 as a catalogue" in _gap("GAP-RVO04-07")["decision"]

def test_rvo04_18_mcepr_runtime_qualification_is_separate_from_real_persistence_authority():
    node = GRAPH["capability_nodes"]["MCEPR_REGISTRY"]
    assert node["state"] == "QUALIFIED"
    assert node["real_persistence_authority"] == "BLOCKED"
    assert MCEPR["authority"]["real_event_persistence_authorized"] is False
    assert MCEPR["authority"]["runtime_integration_authorized"] is False
    assert MCEPR["bounded_macro_envelope"]["status"] == "DEFINED_NOT_AUTHORIZED"

def test_rvo04_19_p1_and_smf_binding_gaps_are_rvo_gaps_not_owner_failures():
    assert _gap("GAP-RVO04-01")["type"] == "RVO_INTEGRATION_GAP"
    assert _gap("GAP-RVO04-01")["does_not_require_owner_modification"] is True
    assert _gap("GAP-RVO04-02")["type"] == "RVO_INTEGRATION_GAP"
    assert _gap("GAP-RVO04-02")["does_not_require_owner_modification"] is True

def test_rvo04_20_data_is_first_owner_frontier_for_meaningful_empirical_claim():
    rec = GAPS["global_recommendation"]
    assert rec["first_owner_frontier"] == "GAP-RVO04-03 / DATA-01"
    assert _gap("GAP-RVO04-03")["type"] == "OWNER_QUALIFICATION_GAP"

def test_rvo04_21_global_generic_data_is_not_required_before_first_use():
    decision = _gap("GAP-RVO04-03")["decision"]
    assert "universal generic Data abstraction is not required" in decision
    assert "exact dataset family/schema" in decision

def test_rvo04_22_protocol_only_readiness_does_not_grant_real_use_authority():
    assert "FIRST REAL RVO PROTOCOL-ONLY APPLICATION =" in READINESS
    assert "CAPABILITY_CONDITIONALLY_READY" in READINESS
    assert "REAL_USE_AUTHORITY_NOT_GRANTED" in READINESS

def test_rvo04_23_empirical_predictive_economic_and_oos_claims_remain_blocked():
    for marker in (
        "FIRST REAL EMPIRICAL DESCRIPTIVE CLAIM =\nBLOCKED_BY_DATA_QUALIFICATION",
        "FIRST REAL PREDICTIVE CLAIM =\nBLOCKED_BY_DATA",
        "FIRST REAL ECONOMIC CLAIM =\nBLOCKED_BY_DATA",
        "FIRST REAL OOS CONFIRMATION =\nBLOCKED_BY_DATA",
    ):
        assert marker in READINESS

def test_rvo04_24_authority_and_owner_boundaries_are_explicit():
    assert TAXONOMY["semantics"]["rvo_authority"] == "NONE"
    assert GAPS["principles"][0] == "OWNER_GAP != RVO_INTEGRATION_GAP"
    assert "RVO_AUTHORITY =\nNONE" in READINESS
    assert "OWNER_MODIFICATION =\nNONE" in READINESS
    assert "REAL_EXPERIMENT =\nNONE" in READINESS
    assert "OOS_CONSUMPTION =\nNONE" in READINESS

def test_rvo04_25_rvo05_is_closed():
    assert "RVO-05 =\nNOT_AUTHORIZED" in READINESS
