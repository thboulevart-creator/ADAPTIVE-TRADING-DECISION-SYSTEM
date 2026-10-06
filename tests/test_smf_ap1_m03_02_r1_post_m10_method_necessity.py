from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
GOV=ROOT/"GOVERNANCE"/"SMF-AP1-M03-02-R1-POST-M10-METHOD-NECESSITY-HUMAN-ADJUDICATION-2026-10-06.md"
REC=ROOT/"reports"/"program"/"2026-10-06-SMF-AP1-M03-02-R1-POST-M10-METHOD-NECESSITY-HUMAN-ADOPTION-RECEIPT-V0.1.json"

def load():
    return json.loads(REC.read_text(encoding="ascii"))

def test_decision_is_human_adopted_and_closed():
    r=load()
    assert r["status"]=="HUMAN_ADOPTED_BINDING_CLOSED"
    assert r["decision"]["post_m10_method_necessity"]=="RESOLVED"
    assert r["decision"]["immediate_additional_statistical_method"]=="NONE"
    assert r["stop"] is True

def test_no_method_auto_activation():
    r=load()
    assert r["method_state"]=={"M04":"CLOSED","M05":"CLOSED","M08":"CLOSED","M09":"CLOSED","M11":"CLOSED"}
    assert r["authority"]["new_statistical_method_execution"] is False

def test_temporal_pooling_gate_is_required_but_not_opened():
    r=load()
    assert r["decision"]["minimum_required_next_control"]=="POST_M10_TEMPORAL_POOLING_AND_CONDITIONING_GATE"
    assert r["next_frontier"]["scope"]=="DESIGN_FREEZE_ONLY"
    assert r["next_frontier"]["separate_human_authorization_required"] is True
    assert r["next_frontier"]["automatic_execution"] is False

def test_material_claim_unit_pooling_rule_exact():
    r=load()
    p=r["pooling_rule"]
    assert p["material_claim_units"]==8
    assert p["unconditional_pooling_across_2022_2025"]=="NOT_ALLOWED_BY_DEFAULT"
    assert p["admissible_routes"]==[
      "EXPLICITLY_JUSTIFY_TEMPORAL_POOLING",
      "CONDITION_OR_STRATIFY_BY_TIME",
      "PREREGISTER_A_METHOD_EXPLICITLY_ROBUST_TO_THE_OBSERVED_TEMPORAL_VARIATION"
    ]
    assert p["otherwise"]=="BLOCKED"

def test_nonmaterial_claim_units_not_promoted():
    r=load()
    x=r["non_material_claim_units"]
    assert x["claim_units"]==["spread_mean p90","spread_mean p95","spread_mean p99"]
    assert x["status"]=="NO_MATERIAL_TEMPORAL_VARIATION_DETECTED"
    assert set(x["forbidden_promotions"])=={"STABILITY_PROVEN","STATIONARITY_PROVEN","UNCONDITIONAL_POOLING_VALIDATED"}

def test_same_corpus_not_pristine():
    s=load()["scientific_boundaries"]
    assert s["evidence_state"]=="EXPOSED"
    assert s["same_corpus_confirmatory_status"]=="CONTAMINATED_OR_NON_PRISTINE"
    assert s["pristine_reset"]=="FORBIDDEN"

def test_global_m05_remains_blocked():
    assert load()["m05"]["global_resampling_across_2022_2025"]=="BLOCKED_PENDING_TEMPORAL_JUSTIFICATION"

def test_no_data_market_oos_trading_or_capital_authority():
    assert load()["authority"]=={
      "new_statistical_method_execution":False,
      "real_data_read":False,
      "new_market_result":False,
      "oos_consumption":False,
      "trading":False,
      "capital":False
    }

def test_governance_record_contains_binding_stop_and_frontier():
    s=GOV.read_text(encoding="utf-8")
    assert "POST_M10_METHOD_NECESSITY =\nRESOLVED" in s
    assert "NEW_STATISTICAL_METHOD =\nNONE" in s
    assert "TEMPORAL_POOLING_GATE =\nREQUIRED" in s
    assert "DESIGN / FREEZE ONLY" in s
    assert s.rstrip().endswith("STOP.")
