import importlib.util, json, os, pathlib, tempfile
import numpy as np

MODULE_PATH=os.environ.get("C01_MODEL_MODULE_PATH","/mnt/data/c01_frozen_model_artifact.py")
spec=importlib.util.spec_from_file_location("c01_model_under_test",MODULE_PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def ck(x,msg):
    if not x: raise AssertionError(msg)

def valid_charter():
    return {
      "schema":"ATDS_C01_CONFIRMATORY_RESEARCH_CHARTER_V0_2","status":"FROZEN_BEFORE_CONFIRMATION_DATA_ACCESS",
      "candidate":{"id":"CR2-C01-ABS_VOL_X_TICK","cr2_status":"SUPPORTED_N0_SYNTHESIS"},
      "confirmation_data":{"eligible_start_utc":"2026-05-25T00:00:00Z","fixed_end_utc":"2027-05-24T23:59:59Z"},
      "development_freeze":{"already_registered_thresholds":{
        "abs_rv15_state":list(m.EXPECTED_VOL_THRESHOLDS),"tick5_hour_relative_state":list(m.EXPECTED_TICK_THRESHOLDS),
        "rv15_target_quintiles":list(m.EXPECTED_RV_QUINTILES),"tick15_target_quintiles":list(m.EXPECTED_TICK_QUINTILES)}}}

def valid_evidence():
    return {"schema":"ATDS_CR2_REGIME_CANDIDATE_SYNTHESIS_V0_1","status":"CR2_COMPLETE","research_class":"N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS",
      "candidates":[{"candidate_id":"CR2-C01-ABS_VOL_X_TICK","scientific_status":"SUPPORTED_N0_SYNTHESIS"},{"candidate_id":"CR2-C02-REL_VOL_X_TICK","scientific_status":"NOT_INTERPRETABLE"}],
      "scope":{k:False for k in ("direction_target_used","pnl_calculated","optimization","feature_search","interaction_search","winner_selection","semantic_regime_labels_instantiated","mt5_used")}}

def test_charter_accepts_exact(): m.validate_charter(valid_charter())
def test_charter_rejects_old_version():
    x=valid_charter(); x["schema"]="ATDS_C01_CONFIRMATORY_RESEARCH_CHARTER_V0_1"
    try: m.validate_charter(x); raise AssertionError("old charter accepted")
    except RuntimeError: pass

def test_charter_rejects_window_drift():
    x=valid_charter(); x["confirmation_data"]["eligible_start_utc"]="2026-05-26T00:00:00Z"
    try: m.validate_charter(x); raise AssertionError("window drift accepted")
    except RuntimeError: pass

def test_charter_rejects_threshold_drift():
    x=valid_charter(); x["development_freeze"]["already_registered_thresholds"]["abs_rv15_state"][0]+=0.01
    try: m.validate_charter(x); raise AssertionError("threshold drift accepted")
    except RuntimeError: pass

def test_evidence_accepts_exact_status_family(): m.validate_cr2_evidence(valid_evidence())
def test_evidence_rejects_c02_promotion():
    x=valid_evidence(); x["candidates"][1]["scientific_status"]="SUPPORTED_N0_SYNTHESIS"
    try: m.validate_cr2_evidence(x); raise AssertionError("C02 promotion accepted")
    except RuntimeError: pass

def test_evidence_rejects_scope_opening():
    x=valid_evidence(); x["scope"]["pnl_calculated"]=True
    try: m.validate_cr2_evidence(x); raise AssertionError("PnL scope accepted")
    except RuntimeError: pass

def test_pad_counts_fixed_shape():
    x=np.array([[1,2]+[0]*23],dtype=np.int64); y=m.pad_counts(x,3)
    ck(y.shape==(3,25) and y[0,1]==2 and np.all(y[1:]==0),"pad counts")
def test_pad_counts_rejects_oversize():
    try: m.pad_counts(np.zeros((4,25),dtype=np.int64),3); raise AssertionError("oversize accepted")
    except RuntimeError: pass

def test_probability_rows_sum_one():
    c=np.zeros((2,25),dtype=np.int64); c[1,0]=10; p=m.probabilities_from_counts(c)
    ck(np.allclose(p.sum(axis=1),1.0),"prob sum")
def test_probability_zero_row_uniform():
    p=m.probabilities_from_counts(np.zeros((1,25),dtype=np.int64))
    ck(np.allclose(p[0],np.ones(25)/25),"uniform")
def test_probability_laplace_nonzero():
    c=np.zeros((1,25),dtype=np.int64); c[0,0]=100; p=m.probabilities_from_counts(c)
    ck(np.all(p>0),"laplace omitted")
def test_digest_deterministic():
    args=[np.arange(24,dtype=float),[1,2],[3,4],[5,6,7,8],[9,10,11,12],np.zeros((2,25),int),np.ones((2,25),int),np.full((3,25),2,int)]
    ck(m.canonical_model_digest(*args)==m.canonical_model_digest(*args),"digest nondeterministic")
def test_digest_changes_counts():
    args=[np.arange(24,dtype=float),[1,2],[3,4],[5,6,7,8],[9,10,11,12],np.zeros((2,25),int),np.ones((2,25),int),np.full((3,25),2,int)]
    d1=m.canonical_model_digest(*args); args[-1]=args[-1].copy(); args[-1][0,0]+=1
    ck(d1!=m.canonical_model_digest(*args),"digest count blind")
def test_compare_tuple_accepts_exact(): m.compare_tuple([1,2],[1,2])
def test_compare_tuple_rejects_drift():
    try: m.compare_tuple([1,2.1],[1,2],atol=1e-12); raise AssertionError("drift accepted")
    except RuntimeError: pass

def test_extract_c01():
    x={"candidates":[{"candidate_id":"x"},{"candidate_id":"CR2-C01-ABS_VOL_X_TICK","v":1}]}
    ck(m.extract_c01_from_evidence(x)["v"]==1,"extract")
def test_d2026_reproduction_accepts_exact():
    ref={"primary_15m":{"D2026":{"comparisons":{"vs_vol":{"delta_log_loss":.1,"delta_brier":.2,"n":3},"vs_tick":{"delta_log_loss":.3,"delta_brier":.4,"n":3}},"joint_state_counts_test":{"0":1}}}}
    got={"comparisons":ref["primary_15m"]["D2026"]["comparisons"],"joint_state_counts_test":{"0":1}}
    m.validate_d2026_reproduction(ref,got)
def test_d2026_reproduction_rejects_score_drift():
    ref={"primary_15m":{"D2026":{"comparisons":{"vs_vol":{"delta_log_loss":.1,"delta_brier":.2,"n":3},"vs_tick":{"delta_log_loss":.3,"delta_brier":.4,"n":3}},"joint_state_counts_test":{"0":1}}}}
    got={"comparisons":json.loads(json.dumps(ref["primary_15m"]["D2026"]["comparisons"])),"joint_state_counts_test":{"0":1}}; got["comparisons"]["vs_vol"]["delta_log_loss"]+=.01
    try: m.validate_d2026_reproduction(ref,got); raise AssertionError("score drift accepted")
    except RuntimeError: pass

def test_d2026_reproduction_rejects_state_count_drift():
    ref={"primary_15m":{"D2026":{"comparisons":{"vs_vol":{"delta_log_loss":.1,"delta_brier":.2,"n":3},"vs_tick":{"delta_log_loss":.3,"delta_brier":.4,"n":3}},"joint_state_counts_test":{"0":1}}}}
    got={"comparisons":ref["primary_15m"]["D2026"]["comparisons"],"joint_state_counts_test":{"0":2}}
    try: m.validate_d2026_reproduction(ref,got); raise AssertionError("count drift accepted")
    except RuntimeError: pass

def test_scope_forbids_confirmation_access(): ck(m.SCOPE["confirmation_data_accessed"] is False,"confirmation access open")
def test_scope_forbids_pnl(): ck(m.SCOPE["pnl_calculated"] is False,"PnL open")
def test_scope_forbids_winner(): ck(m.SCOPE["winner_selection"] is False,"winner open")
def test_path_symlink_guard():
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td); real=root/"real"; real.mkdir(); (real/"x").write_text("x"); link=root/"link"
        try: link.symlink_to(real,target_is_directory=True)
        except OSError: return
        ck(m.path_chain_has_reparse_or_symlink(link/"x"),"symlink bypass")
def test_hour_median_serialization_marks_unavailable():
    vals=np.arange(24,dtype=float); vals[17]=np.nan
    serialized, unavailable=m.serialize_hour_medians(vals)
    ck(serialized[17] is None and unavailable==[17] and serialized[16]==16.0,"hour median serialization")

def test_unavailable_hour_guard_accepts_exact():
    m.validate_unavailable_hours([17])

def test_unavailable_hour_guard_rejects_drift():
    try: m.validate_unavailable_hours([]); raise AssertionError("missing unavailable hour accepted")
    except RuntimeError: pass
    try: m.validate_unavailable_hours([16]); raise AssertionError("wrong unavailable hour accepted")
    except RuntimeError: pass

def test_write_json_rejects_nonfinite():
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"bad.json"
        try: m.write_json_exclusive(p,{"x":float("nan")}); raise AssertionError("NaN JSON accepted")
        except ValueError: pass
        ck(not p.exists() or p.stat().st_size==0,"nonfinite JSON partially persisted")

def test_write_exclusive_refuses_overwrite():
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"x.json"; m.write_json_exclusive(p,{"a":1})
        try: m.write_json_exclusive(p,{"b":2}); raise AssertionError("overwrite accepted")
        except FileExistsError: pass

def main():
    ts=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts: t(); print("PASS",t.__name__)
    print(f"{len(ts)}/{len(ts)} PASS")
if __name__=="__main__": main()
