import importlib.util, os, pathlib, tempfile, json
import numpy as np

MODULE_PATH=os.environ.get("CR1_MODULE_PATH","/mnt/data/cr1_context_informativeness.py")
spec=importlib.util.spec_from_file_location("cr1_under_test",MODULE_PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def ck(x,msg):
    if not x: raise AssertionError(msg)

def valid_context():
    return {
      "schema":"ATDS_CR1_CONTEXT_V0_1",
      "context_id":m.EXPECTED_CONTEXT_ID,
      "dataset_id":"USTECH_PROFILE_MINUTE_CORE_V0_1","dataset_version":"V0.1",
      "content_hash":m.EXPECTED_AP0_MANIFEST_SHA256,"instrument":"USTECH","granularity":"1-minute","timezone_storage":"UTC",
      "configuration_version":"CR1-CONTEXT-INFORMATIVENESS-V0.1",
      "bindings":{"core_commit":m.EXPECTED_CORE_COMMIT,"hypothesis_registry_git_blob":m.EXPECTED_REGISTRY_BLOB},
    }

def test_context_identity_accept_and_forgery():
    c=valid_context(); m.validate_context_payload(c)
    c=dict(c); c["instrument"]="FOREIGN"
    try: m.validate_context_payload(c); raise AssertionError("foreign context accepted")
    except RuntimeError: pass

def test_context_id_determinism():
    c=valid_context(); ck(m.stable_context_id(c)==m.EXPECTED_CONTEXT_ID,"context id drift")
    forged=dict(c); forged["context_id"]="CTX-forged"
    try: m.validate_context_payload(forged); raise AssertionError("forged context_id accepted")
    except RuntimeError: pass

def test_return_gap():
    minute=np.array([0,60000,180000]); seg=np.array([0,0,0]); close=np.array([100.,101.,102.])
    r,v=m.signed_return_1m_bps(minute,seg,close); ck(v.tolist()==[False,True,False],"return crossed gap")

def test_forward_starts_after_t():
    minute=np.arange(5)*60000; seg=np.zeros(5,dtype=int); x=np.array([10.,20.,30.,40.,50.])
    f=m.forward_mean(x,minute,seg,2)
    ck(abs(f[0]-25.0)<1e-12,"forward target included t")
    ck(abs(f[1]-35.0)<1e-12,"forward target alignment")

def test_forward_rejects_gap_and_segment():
    minute=np.array([0,60000,180000,240000]); seg=np.array([0,0,1,1]); x=np.arange(4,dtype=float)
    f=m.forward_mean(x,minute,seg,2); ck(not np.isfinite(f[0]) and not np.isfinite(f[1]),"forward crossed gap/segment")
    minute2=np.array([0,60000,180000,240000]); seg2=np.zeros(4,dtype=int)
    f2=m.forward_mean(x,minute2,seg2,2); ck(not np.isfinite(f2[0]),"forward accepted same-segment time gap")

def test_trailing_mean_causal():
    minute=np.arange(5)*60000; seg=np.zeros(5,dtype=int); x=np.array([1.,2.,3.,4.,100.])
    t=m.trailing_mean(x,minute,seg,3)
    ck(abs(t[3]-3.0)<1e-12,"trailing mean leaked future")

def test_forward_endpoint_shift():
    minute=np.arange(6)*60000; seg=np.zeros(6,dtype=int); b=np.array([np.nan,1,2,3,4,5],float)
    f=m.forward_from_endpoint(b,minute,seg,2)
    ck(f[0]==2 and f[2]==4,"endpoint target shift wrong")

def test_fold_masks_utc_years():
    y=np.array([2022,2023,2024,2025,2026])
    tr,te=m.fold_masks(y,"F2")
    ck(tr.tolist()==[True,True,False,False,False] and te.tolist()==[False,False,True,False,False],"fold leak")

def test_gap_state_fixed():
    x=np.array([0,1,15,16,60,61,100])
    ck(m.gap_state(x).tolist()==[0,1,1,2,2,3,3],"gap states changed")

def test_quantile_freeze():
    target=np.array([0.,1.,2.,3.,4.,5.,100.,200.])
    train_valid=np.array([True,True,True,True,True,True,False,False])
    classes,th=m.classify_target_train_frozen(target,train_valid)
    ck(classes[-2:].tolist()==[4,4],"test recalibration occurred")
    ck(np.allclose(th,m.quantile_thresholds(target[train_valid],(20,40,60,80))),"thresholds not train-frozen")

def test_hour_relative_uses_supplied_training_medians():
    vals=np.array([10.,20.]); hour=np.array([1,1]); med=np.full(24,np.nan); med[1]=10
    rel=m.relative_by_hour(vals,hour,med); ck(np.allclose(rel,[1,2]),"hour normalization wrong")

def test_unseen_key_laplace_is_uniform():
    model=m.fit_categorical_model(np.array([0,0]),np.array([1,2]))
    p=m.probability_for(model,999)
    ck(np.allclose(p,np.ones(5)/5),"unseen key not uniform Laplace")

def test_candidate_can_improve_logscore():
    y=np.array([0,0,4,4],dtype=int); base=np.zeros(4,dtype=int); cand=np.array([0,0,1,1])
    bm=m.fit_categorical_model(base,y); cm=m.fit_categorical_model(cand,y)
    bs=m.score_model(bm,base,y); cs=m.score_model(cm,cand,y)
    ck(bs["log_loss"]>cs["log_loss"],"informativeness score inverted")

def test_status_supported_requires_all_three():
    folds={f:{"delta_log_loss":0.01} for f in m.PRIMARY_FOLDS}
    ck(m.adjudicate_status(folds,0.01,0.01,False)=="SUPPORTED_N0","support rule wrong")
    folds["F2"]["delta_log_loss"]=-0.001
    ck(m.adjudicate_status(folds,0.01,0.01,False)=="NOT_INTERPRETABLE","mixed fold promoted")

def test_status_refuted_two_folds():
    folds={"F1":{"delta_log_loss":0.01},"F2":{"delta_log_loss":-0.01},"F3":{"delta_log_loss":0.0}}
    ck(m.adjudicate_status(folds,-0.001,0.01,False)=="REFUTED_N0","refute rule wrong")

def test_sparse_blocks_support():
    folds={f:{"delta_log_loss":0.01} for f in m.PRIMARY_FOLDS}
    ck(m.adjudicate_status(folds,0.01,0.01,True)=="NOT_INTERPRETABLE","sparse support allowed")

def test_d2026_not_part_of_status():
    folds={f:{"delta_log_loss":0.01} for f in m.PRIMARY_FOLDS}
    folds["D2026"]={"delta_log_loss":-999}
    ck(m.adjudicate_status(folds,0.01,0.01,False)=="SUPPORTED_N0","D2026 changed status")

def test_hypothesis_baselines_frozen():
    ck(m.hypothesis_spec("CR-H01-NY-HOUR")[1]=="B0","H01 baseline")
    ck(m.hypothesis_spec("CR-H02-WEEKDAY")[1]=="B1","H02 baseline")
    for hid in m.EXPECTED_HYPOTHESES[2:]:
        ck(m.hypothesis_spec(hid)[1]=="B2","state baseline not B2")

def test_b2_candidate_keys_include_hour_weekday_state():
    h=np.array([10,10]); w=np.array([1,2]); state=np.array([0,0])
    base=m.baseline_key_codes("B2",h,w); cand=m.candidate_key_codes("B2",h,w,state)
    ck(base[0]!=base[1] and cand[0]!=cand[1],"B2 conditioning dropped")

def test_h07_spread_diagnostic_frozen():
    ck(m.diagnostic_targets_for("CR-H07-GAP-REOPEN")==("SPREAD15",),"H07 diagnostic omitted")
    ck(m.diagnostic_targets_for("CR-H03-ABS-VOL")==(),"unexpected diagnostic injected")

def test_primary_targets_frozen():
    expected={"CR-H01-NY-HOUR":"RV15","CR-H02-WEEKDAY":"RV15","CR-H03-ABS-VOL":"RV15","CR-H04-REL-VOL":"RV15","CR-H05-SPREAD":"SPREAD15","CR-H06-TICK-DENSITY":"TICK15","CR-H07-GAP-REOPEN":"RV15","CR-H08-EFFICIENCY":"EFF15"}
    for h,t in expected.items(): ck(m.hypothesis_spec(h)[0]==t,f"primary target drift {h}")

def test_no_direction_pnl_regime_scope():
    ck(m.SCOPE["direction_target_used"] is False,"direction target opened")
    ck(m.SCOPE["pnl_calculated"] is False,"PnL opened")
    ck(m.SCOPE["regime_labels_instantiated"] is False,"regime labels opened")
    ck(m.SCOPE["winner_selection"] is False,"winner selection opened")

def test_ny_dst():
    ts=np.array([1741501800000,1741505400000],dtype=np.int64)
    h,w,y=m.time_dimensions(ts); ck(h.tolist()==[1,3],"NY DST broken")

def test_efficiency_gap_invalid():
    r=np.array([np.nan,1,1,np.nan,1,1,1],float); v=np.isfinite(r)
    e=m.efficiency_array(r,v,3); ck(not np.isfinite(e[4]),"efficiency crossed invalid return")

def test_symlink_chain_guard():
    with tempfile.TemporaryDirectory() as td:
        root=pathlib.Path(td); real=root/"real"; real.mkdir(); (real/"x").write_text("x"); link=root/"link"
        try: link.symlink_to(real,target_is_directory=True)
        except OSError: return
        ck(m.path_chain_has_reparse_or_symlink(link/"x"),"symlink chain bypass")

def test_registry_family_exact():
    fake={"schema":"ATDS_CONTEXT_REGIME_HYPOTHESIS_REGISTRY_V0_1","status":"PREFLIGHT_ONLY_NO_RESEARCH_EXECUTED","epistemic_class":"N0_EXPLORATORY",
          "hypotheses":[{"id":x} for x in m.EXPECTED_HYPOTHESES],
          "scoring":{"ranking_or_winner_selection":False},
          "target_contract":{"pnl_target":False,"directional_return_target":False}}
    m.validate_registry(fake)
    fake["hypotheses"]=fake["hypotheses"][:-1]
    try: m.validate_registry(fake); raise AssertionError("omitted hypothesis accepted")
    except RuntimeError: pass

def main():
    ts=[v for k,v in globals().items() if k.startswith("test_") and callable(v)]
    for t in ts:
        t(); print("PASS",t.__name__)
    print(f"{len(ts)}/{len(ts)} PASS")
if __name__=="__main__": main()
