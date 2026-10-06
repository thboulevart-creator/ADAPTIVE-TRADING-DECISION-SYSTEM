from __future__ import annotations
import json, subprocess
from pathlib import Path
from tools.ao_e0_b12_data01_sr01 import adjudicate_a, select_after_a, A_PASS
ROOT=Path(__file__).resolve().parents[1]

def load(p): return json.loads((ROOT/p).read_text())
def blob(p): return subprocess.check_output(["git","hash-object",str(ROOT/p)],text=True).strip()

def test_acq01_historical_blocker_preserved():
    assert blob("GOVERNANCE/AO-E0-B12-DATA-01-ACQ-01-BLOCKER-V0.1.json")=="297e9d6ebbd44cf3a8dd3fabfce942ec5a418bee"

def test_sr01_decision_rule_and_holdout_split_frozen():
    c=load("GOVERNANCE/AO-E0-B12-DATA-01-SR-01-CONTRACT-V0.1.json")
    assert c["decision_rule"]=="A_FIRST_THEN_B_IF_A_FAILS"
    assert c["a"]["validation_window"]==["2026-05-22T00:00:00Z","2026-05-24T23:59:59.963Z"]
    assert c["firewall"]["october_forward_acquisition"] is False

def test_discovery_exact():
    d=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-DISCOVERY-V0.1.json")
    assert d["rows"]==1698188
    assert (d["timestamp_mismatch_count"],d["bid_mismatch_count"],d["ask_mismatch_count"])==(0,0,0)

def test_transform_frozen_before_validation():
    t=load("GOVERNANCE/AO-E0-B12-DATA-01-SR-01-A-TRANSFORMATION-FREEZE-V0.1.json")
    assert t["transformation_id"]=="DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1"
    assert t["validation_detail_observed_before_freeze"] is False
    assert t["epsilon"]==0 and t["row_removal"]==0 and t["rounding_mode"] is None
    assert t["code_blob"]=="e60fd260642f1a3dfb88b7cce4b6c4f5defc3131"
    assert t["test_blob"]=="54837800f16f60b56328ddc818d0f9e2b2b01c1d"

def test_validation_exact():
    d=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-VALIDATION-V0.1.json")
    assert d["reference_rows"]==d["candidate_rows"]==360754
    assert (d["timestamp_mismatch_count"],d["bid_mismatch_count"],d["ask_mismatch_count"])==(0,0,0)
    assert d["epsilon"]==0 and d["row_removal"]==0
    assert d["status"]=="PASS_EXACT"

def test_full_rebreak_exact():
    d=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-FULL-REBREAK-V0.1.json")
    assert d["reference_rows"]==d["candidate_rows"]==2058942
    assert (d["timestamp_mismatch_count"],d["bid_mismatch_count"],d["ask_mismatch_count"])==(0,0,0)
    assert d["candidate_multiplier_values"]==["0.001"]
    assert d["reference_float_to_milli_max_abs_residual_milli"]==0.0
    assert d["status"]=="PASS_EXACT_DETERMINISTIC_RECONCILIATION"

def test_provenance_exact_and_sufficient():
    p=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-PROVENANCE-RECONCILIATION-V0.1.json")
    assert p["reference"]["documented_publisher_provenance"]=="Dukascopy via Tickstory"
    assert p["reference"]["bid_type"]==p["reference"]["ask_type"]=="double"
    assert p["candidate"]["canonical_multiplier"]=="0.001"
    assert p["reconciliation"]["provenance_sufficient"] is True
    assert p["reconciliation"]["semantic_relation"]=="EXACT_DETERMINISTIC_RECONCILIATION"
    assert p["reconciliation"]["raw_dukascopy_equals_historical_source_b_bytes"] is False
    assert p["reconciliation"]["transformed_dukascopy_semantics_equals_source_b_price_core_semantics"] is True

def test_operational_float64_equivalence_exact():
    p=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-PROVENANCE-RECONCILIATION-V0.1.json")
    e=p["additional_operational_equivalence"]
    assert e["candidate_milli_div_1000_float64_bid_mismatch_count"]==0
    assert e["candidate_milli_div_1000_float64_ask_mismatch_count"]==0
    assert e["max_abs_float64_bid_difference"]==0.0
    assert e["max_abs_float64_ask_difference"]==0.0

def test_actual_a_adjudication_passes_and_b_stays_closed():
    a=adjudicate_a(
      frozen=True,validation_detail_prefreeze=False,deterministic=True,time_invariant=True,
      strategy_independent=True,performance_independent=True,row_specific_lookup=False,
      post_hoc_tolerance=False,dropped_quotes=False,interpolation=False,future_data_used=False,
      validation_ts=0,validation_bid=0,validation_ask=0,full_ts=0,full_bid=0,full_ask=0,
      full_ref_rows=2058942,full_candidate_rows=2058942,provenance_sufficient=True)
    assert a==A_PASS
    assert select_after_a(a)=={"selected_path":"A","b_open":False}

def test_b12_and_october_forward_remain_closed():
    p=load("reports/program/2026-10-06-AO-E0-B12-DATA-01-SR-01-A-PROVENANCE-RECONCILIATION-V0.1.json")
    assert p["selected_path"]=="A" and p["b_phase"]=="NOT_OPENED"
    assert p["firewall"]["b12"]=="CLOSED"
    assert p["firewall"]["october_forward_acquisition"] is False
    assert p["firewall"]["performance_bearing_read"] is False
    assert p["firewall"]["performance_observed"] is False
