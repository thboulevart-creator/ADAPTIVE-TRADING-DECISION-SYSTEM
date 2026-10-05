from pathlib import Path
import json
D=json.loads((Path(__file__).resolve().parents[1]/"GOVERNANCE"/"AO-E0-B9-01-PRIOR-EXPOSURE-MULTIPLICITY-DECLARATION-V0.1.json").read_text())
def test_cell(): assert D["cell_identity"]=="sha256:38610ff2afd70998a7fa3e522575faf697ec3159e00829c2b2bbd5da45c52054"
def test_claim(): assert D["claim_class"]=="CC05_ECONOMIC_NET_PROFITABILITY"
def test_candidate(): assert D["closure_candidate"]["b9"]=="CLOSED_IF_GREEN"
def test_n_trials_null(): assert D["search_provenance"]["explicit_n_trials"] is None
def test_contaminated(): assert D["prior_exposure_state"]=="CONTAMINATED"
