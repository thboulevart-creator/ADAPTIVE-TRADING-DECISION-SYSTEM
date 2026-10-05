from pathlib import Path
import importlib.util, json, copy
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("b",R/"breakers"/"ao_e0_cell_01_identity_breaker.py")
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
def payload(): return json.loads((R/"GOVERNANCE"/"AO-E0-CELL-01-CANONICAL-SERIALIZATION-V0.1.json").read_text())
def contract(): return json.loads((R/"GOVERNANCE"/"AO-E0-CELL-01-EXACT-STRATEGY-QUALIFICATION-CELL-IDENTITY-CONTRACT-V0.1.json").read_text())
def test_full_breaker(): b.run()
def test_exact_identity(): assert b.digest(payload())==contract()["cell_identity"]
def test_determinism(): assert b.canon(payload())==b.canon(json.loads(b.canon(payload())))
def test_no_evidence_dimensions(): assert not (set(b.walk_keys(payload())) & b.FORBIDDEN_KEYS)
def test_source_feed_not_laundered(): assert payload()["cell_dimensions"]["asset_instrument_identity"]["source_b_feed_equivalence_to_vt_execution_feed"] is False
def test_not_auto_adopted(): assert contract()["human_adopted"] is False
def test_no_oos_authority(): assert contract()["authority"]["oos_consumption_authorized"] is False
def test_material_drift_changes_id():
    x=copy.deepcopy(payload()); x["cell_dimensions"]["strategy_version_identity"]["lookback_completed_admissible_h1_bars"]=21
    assert b.digest(x)!=contract()["cell_identity"]
