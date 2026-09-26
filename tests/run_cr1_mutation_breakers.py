import os, pathlib, subprocess, sys, tempfile
SOURCE=pathlib.Path("/mnt/data/cr1_context_informativeness.py").read_text()
TEST="/mnt/data/test_cr1_context_informativeness.py"
MUTANTS=[
("CONTEXT_ID_BYPASS",'if stable_context_id(context) != context.get("context_id") or context.get("context_id") != EXPECTED_CONTEXT_ID:','if False and (stable_context_id(context) != context.get("context_id") or context.get("context_id") != EXPECTED_CONTEXT_ID):'),
("RETURN_CROSS_GAP",'((minute[1:]-minute[:-1])==60_000)','((minute[1:]-minute[:-1])>=60_000)'),
("FORWARD_INCLUDES_T",'sums=cs[end+1]-cs[t+1]','sums=cs[end+1]-cs[t]'),
("FORWARD_GAP_BYPASS",'((minute[end]-minute[t])==h*60_000)','((minute[end]-minute[t])>=h*60_000)'),
("TRAILING_FUTURE_LEAK",'out[end[boundary]]=vals[boundary]','out[np.maximum(end[boundary]-1,0)]=vals[boundary]'),
("FOLD_TEST_LEAK",'if fold_id=="F2": return y<=2023, y==2024','if fold_id=="F2": return y<=2024, y==2024'),
("GAP_STATE_THRESHOLD_SEARCH",'out[(x>=16)&(x<=60)]=2','out[(x>=31)&(x<=60)]=2'),
("TEST_QUANTILE_RECALIBRATION",'thresholds=quantile_thresholds(target[train_valid],(20,40,60,80))','thresholds=quantile_thresholds(target[~train_valid & np.isfinite(target)],(20,40,60,80))'),
("UNSEEN_NO_LAPLACE",'out=np.full((len(keys),k),1.0/k,dtype=np.float64)','out=np.zeros((len(keys),k),dtype=np.float64)'),
("STATUS_ALLOW_TWO_FOLDS",'if all(v>0 for v in vals) and pooled_delta_brier>0:','if sum(v>0 for v in vals)>=2 and pooled_delta_brier>0:'),
("SPARSE_BYPASS",'if not critical_controls_pass or sparse_any:','if not critical_controls_pass:'),
("D2026_PRIMARY",'PRIMARY_FOLDS = ("F1", "F2", "F3")','PRIMARY_FOLDS = ("F1", "F2", "F3", "D2026")'),
("STATE_BASELINE_B0",'if hid=="CR-H03-ABS-VOL": return ("RV15","B2","rv_abs",True)','if hid=="CR-H03-ABS-VOL": return ("RV15","B0","rv_abs",True)'),
("SPREAD_TARGET_DRIFT",'if hid=="CR-H05-SPREAD": return ("SPREAD15","B2","spread_rel",True)','if hid=="CR-H05-SPREAD": return ("RV15","B2","spread_rel",True)'),
("DIRECTION_SCOPE_TRUE",'"direction_target_used": False,','"direction_target_used": True,'),
("PNL_SCOPE_TRUE",'"pnl_calculated": False,','"pnl_calculated": True,'),
("REGIME_LABELS_TRUE",'"regime_labels_instantiated": False,','"regime_labels_instantiated": True,'),
("REGISTRY_OMISSION_BYPASS",'if ids != EXPECTED_HYPOTHESES:','if False and ids != EXPECTED_HYPOTHESES:'),
("H07_DIAGNOSTIC_OMIT",'return ("SPREAD15",) if hid=="CR-H07-GAP-REOPEN" else ()','return ()'),
("B2_DROP_WEEKDAY",'return (h.astype(np.int32)*7+w.astype(np.int32))','return h.astype(np.int32)'),
]
killed=[]; survived=[]
for name,old,new in MUTANTS:
    if old not in SOURCE:
        print("SETUP_FAIL",name); sys.exit(2)
    mutated=SOURCE.replace(old,new,1)
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"cr1_mutant.py"; p.write_text(mutated)
        env=os.environ.copy(); env["CR1_MODULE_PATH"]=str(p)
        r=subprocess.run([sys.executable,TEST],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode!=0:
            killed.append(name); print("KILLED",name)
        else:
            survived.append(name); print("SURVIVED",name); print(r.stdout)
print(f"{len(killed)}/{len(MUTANTS)} KILLED")
if survived:
    print("SURVIVORS",",".join(survived)); sys.exit(1)
