import importlib.util, os, pathlib, tempfile, json
import numpy as np

HERE=pathlib.Path(__file__).resolve()
ROOT=HERE.parents[1] if HERE.parent.name=="tests" else HERE.parent
MODULE_PATH=os.environ.get("CR2_MODULE_PATH",str(ROOT/"tools"/"cr2_regime_candidate_synthesis.py"))
spec=importlib.util.spec_from_file_location("cr2_under_test",MODULE_PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def ck(x,msg):
    if not x: raise AssertionError(msg)

def valid_context():
    return {"schema":"ATDS_CR1_CONTEXT_V0_1","context_id":m.EXPECTED_CONTEXT_ID,
            "dataset_id":m.EXPECTED_AP0_IDENTITY,"content_hash":m.EXPECTED_AP0_MANIFEST_SHA256}

def valid_cr1_evidence():
    return {"schema":"ATDS_CR1_CONTEXT_INFORMATIVENESS_V0_1","status":"CR1_COMPLETE",
            "research_class":"N0_EXPLORATORY_PREVIOUSLY_EXPOSED_CORPUS","context_id":m.EXPECTED_CONTEXT_ID,
            "fold_contract":{"pristine_oos":False},
            "hypotheses":[{"hypothesis_id":k,"scientific_status":v} for k,v in m.EXPECTED_CR1_STATUSES.items()],
            "scope":{"pnl_calculated":False,"direction_target_used":False,"optimization":False,"feature_search":False,
                     "interaction_search":False,"winner_selection":False,"regime_labels_instantiated":False,"mt5_used":False}}

def valid_registry():
    return {"schema":"ATDS_CR2_REGIME_CANDIDATE_REGISTRY_V0_1","status":"PREFLIGHT_ONLY_NO_SYNTHESIS_EXECUTED",
            "candidate_families":[{"id":x} for x in m.EXPECTED_FAMILIES],
            "admitted_axes":["NY_HOUR","NY_WEEKDAY","BACKWARD_RV15_ABSOLUTE_STATE",
                             "BACKWARD_RV15_HOUR_RELATIVE_STATE","BACKWARD_TICK5_HOUR_RELATIVE_STATE"],
            "scoring":{"sparse_min_test_per_joint_state":500}}

def test_context_exact():
    m.validate_context(valid_context())
    x=valid_context(); x["context_id"]="CTX-bad"
    try: m.validate_context(x); raise AssertionError("forged context accepted")
    except RuntimeError: pass

def test_cr1_status_family_exact():
    m.validate_cr1_evidence(valid_cr1_evidence())
    x=valid_cr1_evidence(); x["hypotheses"][0]["scientific_status"]="REFUTED_N0"
    try: m.validate_cr1_evidence(x); raise AssertionError("CR1 status drift accepted")
    except RuntimeError: pass

def test_cr1_forbidden_scope():
    x=valid_cr1_evidence(); x["scope"]["pnl_calculated"]=True
    try: m.validate_cr1_evidence(x); raise AssertionError("PnL scope accepted")
    except RuntimeError: pass

def test_registry_exact_two_families():
    m.validate_cr2_registry(valid_registry())
    x=valid_registry(); x["candidate_families"].append({"id":"EXTRA"})
    try: m.validate_cr2_registry(x); raise AssertionError("extra family accepted")
    except RuntimeError: pass

def test_registry_rejects_forbidden_axis():
    x=valid_registry(); x["admitted_axes"].append("BACKWARD_SPREAD5_HOUR_RELATIVE_STATE")
    try: m.validate_cr2_registry(x); raise AssertionError("forbidden axis accepted")
    except RuntimeError: pass

def test_joint_state_3x3():
    v=np.array([0,0,1,1,2,2]); t=np.array([0,2,0,2,0,2])
    ck(m.joint_state(v,t).tolist()==[0,2,3,5,6,8],"joint coding wrong")

def test_joint_target_25_classes_train_frozen():
    rv=np.array([0,1,2,3,4,3.5,3.6],float)
    tk=np.array([0,1,2,3,4,100,200],float)
    tr=np.array([1,1,1,1,1,0,0],bool)
    cls,rq,tq=m.joint_target_classes(rv,tk,tr)
    ck(cls[-2:].tolist()==[24,24],"test thresholds recalibrated")
    ck(len(rq)==4 and len(tq)==4,"quintiles wrong")

def test_tertiles_train_only():
    x=np.array([0,1,2,3,4,1.5,2.5],float); tr=np.array([1,1,1,1,1,0,0],bool)
    st,th=m.tertile_states(x,tr)
    ck(st[-2:].tolist()==[1,1],"test tertiles leaked")
    ck(len(th)==2,"tertile count")

def test_b2_codes_keeps_weekday():
    h=np.array([10,10]); w=np.array([1,2])
    b=m.b2_codes(h,w); ck(b[0]!=b[1],"weekday dropped from B2")

def test_conditional_codes_not_cartesian_hour_state_identity():
    base=np.array([71,72]); state=np.array([0,0])
    c=m.conditional_codes(base,state,3); ck(c[0]!=c[1],"B2 conditioning dropped")

def test_sparse_guard_checks_all_nine_including_zero():
    s=np.array([0]*500+[1]*499+[2]*500+[3]*500+[4]*500+[5]*500+[6]*500+[7]*500+[8]*500)
    sparse=m.sparse_joint_states(s,np.ones(len(s),bool))
    ck(sparse==[{"state":1,"count":499}],"sparse floor wrong")
    s2=np.array([0]*500+[1]*500)
    sp=m.sparse_joint_states(s2,np.ones(len(s2),bool))
    ck(any(x["state"]==8 and x["count"]==0 for x in sp),"missing state not sparse")

def test_fold_masks_d2026_separate():
    y=np.array([2022,2023,2024,2025,2026])
    tr,te=m._fold_masks(y,"F3")
    ck(te.tolist()==[False,False,False,True,False],"F3 leaked 2026")

def test_adjudicate_supported_requires_both_comparisons():
    folds={}
    for f in m.PRIMARY_FOLDS:
        folds[f]={"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":0.2}}}
    pooled={"vs_vol":{"delta_log_loss":0.1,"delta_brier":0.1},"vs_tick":{"delta_log_loss":0.2,"delta_brier":0.1}}
    ck(m.adjudicate_candidate(folds,pooled,False)=="SUPPORTED_N0_SYNTHESIS","support rule")

def test_adjudicate_refutes_if_one_comparison_fails():
    folds={}
    for f in m.PRIMARY_FOLDS:
        folds[f]={"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":-0.1}}}
    pooled={"vs_vol":{"delta_log_loss":0.1,"delta_brier":0.1},"vs_tick":{"delta_log_loss":-0.1,"delta_brier":-0.1}}
    ck(m.adjudicate_candidate(folds,pooled,False)=="REFUTED_N0_SYNTHESIS","one failed baseline didn't refute")


def test_adjudicate_refutes_on_pooled_failure_even_one_bad_fold():
    folds={
      "F1":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":0.1}}},
      "F2":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":0.1}}},
      "F3":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":-0.5}}},
    }
    pooled={"vs_vol":{"delta_log_loss":0.1,"delta_brier":0.1},"vs_tick":{"delta_log_loss":-0.1,"delta_brier":0.1}}
    ck(m.adjudicate_candidate(folds,pooled,False)=="REFUTED_N0_SYNTHESIS","pooled failure did not refute")

def test_adjudicate_mixed_not_interpretable():
    folds={
      "F1":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":0.1}}},
      "F2":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":-0.1}}},
      "F3":{"comparisons":{"vs_vol":{"delta_log_loss":0.1},"vs_tick":{"delta_log_loss":0.1}}},
    }
    pooled={"vs_vol":{"delta_log_loss":0.1,"delta_brier":0.1},"vs_tick":{"delta_log_loss":0.01,"delta_brier":0.1}}
    ck(m.adjudicate_candidate(folds,pooled,False)=="NOT_INTERPRETABLE","mixed promoted")

def test_sparse_forces_not_interpretable():
    folds={f:{"comparisons":{"vs_vol":{"delta_log_loss":1},"vs_tick":{"delta_log_loss":1}}} for f in m.PRIMARY_FOLDS}
    pooled={"vs_vol":{"delta_log_loss":1,"delta_brier":1},"vs_tick":{"delta_log_loss":1,"delta_brier":1}}
    ck(m.adjudicate_candidate(folds,pooled,True)=="NOT_INTERPRETABLE","sparse support allowed")

def test_probability_unseen_uniform():
    c=m.fit_model(np.array([0,0]),np.array([0,1]),k=25)
    p=m.probabilities(c,np.array([999]),k=25)[0]
    ck(np.allclose(p,np.ones(25)/25),"unseen key not uniform")

def test_score_candidate_can_improve():
    y=np.array([0,0,24,24],dtype=np.int16)
    base=np.zeros(4,dtype=np.int64); cand=np.array([0,0,1,1],dtype=np.int64)
    bm=m.fit_model(base,y); cm=m.fit_model(cand,y)
    r=m.comparison_result(bm,cm,base,cand,y)
    ck(r["delta_log_loss"]>0,"comparison sign inverted")

def test_family_abs_uses_abs_not_rel():
    src=pathlib.Path(MODULE_PATH).read_text()
    ck('if family_id=="CR2-C01-ABS_VOL_X_TICK":\n        vol_raw=np.asarray(rv_context["abs"]' in src,"C01 not bound to abs")

def test_family_rel_uses_rel_not_abs():
    src=pathlib.Path(MODULE_PATH).read_text()
    ck('elif family_id=="CR2-C02-REL_VOL_X_TICK":\n        vol_raw=np.asarray(rv_context["rel_by_fold"][fold_id]' in src,"C02 not bound to rel")

def test_scope_forbids_winner_and_labels():
    ck(m.SCOPE["winner_selection"] is False,"winner opened")
    ck(m.SCOPE["semantic_regime_labels_instantiated"] is False,"regime labels opened")
    ck(m.SCOPE["pnl_calculated"] is False and m.SCOPE["direction_target_used"] is False,"economic scope opened")

def test_only_four_ap0_columns():
    ck(m.READ_COLUMNS==["minute_start_ms_utc","tick_count","segment_id","mid_close"],"column scope drift")

def test_primary_folds_exact():
    ck(m.PRIMARY_FOLDS==("F1","F2","F3"),"primary folds drift")

def test_sparse_floor_exact():
    ck(m.SPARSE_MIN_TEST==500,"sparse floor drift")

def test_no_forbidden_semantic_names_in_families():
    joined=" ".join(m.EXPECTED_FAMILIES).lower()
    for x in ("trend","range","breakout","stress"):
        ck(x not in joined,"semantic regime label introduced")

def main():
    ts=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts:
        t(); print("PASS",t.__name__)
    print(f"{len(ts)}/{len(ts)} PASS")

if __name__=="__main__": main()
