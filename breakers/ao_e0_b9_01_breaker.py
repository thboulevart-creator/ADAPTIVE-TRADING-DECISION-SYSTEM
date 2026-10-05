from pathlib import Path
import json, pytest
from tools.smf03_evidence_governance import exposure_transition, search_provenance_gate
R=Path(__file__).resolve().parents[1]
D=json.loads((R/"GOVERNANCE"/"AO-E0-B9-01-PRIOR-EXPOSURE-MULTIPLICITY-DECLARATION-V0.1.json").read_text())
def test_exact_classification():
    assert D["prior_exposure_state"]=="CONTAMINATED"
    s=D["search_provenance"]; assert s["status"]=="PARTIAL_SEARCH_UNIVERSE"; assert s["explicit_n_trials"] is None; assert s["provenance_complete"] is False
def test_exposure_progression():
    x=exposure_transition("PRISTINE","EXPLORATORY_INSPECTION"); assert x["after"]=="EXPOSED"
    y=exposure_transition(x["after"],"HYPOTHESIS_REDESIGN_USING_EVIDENCE"); assert y["after"]=="CONTAMINATED"
    assert exposure_transition("CONTAMINATED","EXPLORATORY_INSPECTION")["after"]=="CONTAMINATED"
    with pytest.raises(ValueError): exposure_transition("CONTAMINATED","RESET_TO_PRISTINE")
def test_m11_partial_universe():
    s=D["search_provenance"]
    g=search_provenance_gate(s["status"],registry_candidate_ids=s["registry_candidate_ids"],explicit_n_trials=None,provenance_complete=False)
    assert g["n_trials"] is None and g["registry_record_count"]==len(s["registry_candidate_ids"])
def test_partial_cannot_invent_n_trials():
    s=D["search_provenance"]
    with pytest.raises(ValueError): search_provenance_gate("PARTIAL_SEARCH_UNIVERSE",registry_candidate_ids=s["registry_candidate_ids"],explicit_n_trials=len(s["registry_candidate_ids"]),provenance_complete=False)
def test_known_requires_complete_provenance():
    with pytest.raises(ValueError): search_provenance_gate("KNOWN_SEARCH_UNIVERSE",registry_candidate_ids=["X"],explicit_n_trials=1,provenance_complete=False)
def test_false_pristine_forbidden():
    e=D["exposure_evidence"]; assert e["oos_exposed"] is True and e["oos_clean"] is False and e["independent_confirmation_eligible"] is False
def test_histories_present():
    h=D["histories"]; assert set(h)=={"parameter_selection_history","strategy_selection_history","claim_selection_history","dataset_window_exposure_history","oos_performance_exposure_history"}
def test_no_relevant_multiplicity_not_claimed():
    s=D["search_provenance"]; assert s["no_relevant_multiplicity_claimed"] is False and s["multiplicity_relevant_to_cc05"] is True
def test_no_authority():
    assert all(v is False for v in D["authority"].values()); assert D["closure_candidate"]["b8"]=="OPEN"; assert D["closure_candidate"]["b12"]=="CLOSED"
