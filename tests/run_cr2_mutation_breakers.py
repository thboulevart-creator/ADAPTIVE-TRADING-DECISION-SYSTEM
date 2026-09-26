import os, pathlib, subprocess, tempfile, sys
from concurrent.futures import ThreadPoolExecutor

HERE=pathlib.Path(__file__).resolve()
ROOT=HERE.parents[1] if HERE.parent.name=="tests" else HERE.parent
SOURCE_PATH=pathlib.Path(os.environ.get("CR2_SOURCE_PATH",str(ROOT/"tools"/"cr2_regime_candidate_synthesis.py")))
TEST=os.environ.get("CR2_TEST_PATH",str(ROOT/"tests"/"test_cr2_regime_candidate_synthesis.py"))
SOURCE=SOURCE_PATH.read_text()
MUTANTS=[
("CONTEXT_ID_BYPASS",'if ctx.get("schema")!="ATDS_CR1_CONTEXT_V0_1" or ctx.get("context_id")!=EXPECTED_CONTEXT_ID:','if False and (ctx.get("schema")!="ATDS_CR1_CONTEXT_V0_1" or ctx.get("context_id")!=EXPECTED_CONTEXT_ID):'),
("CR1_STATUS_DRIFT_ACCEPT",'if got!=EXPECTED_CR1_STATUSES: raise RuntimeError("CR1 status family mismatch")','if False and got!=EXPECTED_CR1_STATUSES: raise RuntimeError("CR1 status family mismatch")'),
("REGISTRY_EXTRA_FAMILY_ACCEPT",'if fam!=EXPECTED_FAMILIES: raise RuntimeError("CR2 candidate family mismatch")','if False and fam!=EXPECTED_FAMILIES: raise RuntimeError("CR2 candidate family mismatch")'),
("JOINT_STATE_WRONG_BASE",'out[ok]=(v[ok]*3+t[ok]).astype(np.int16)','out[ok]=(v[ok]*2+t[ok]).astype(np.int16)'),
("TARGET_TEST_RECALIBRATION",'rv_th=np.percentile(rv[train_valid],(20,40,60,80),method="linear")','rv_th=np.percentile(rv[np.isfinite(rv)],(20,40,60,80),method="linear")'),
("TERTILE_TEST_LEAK",'valid=train_mask & np.isfinite(x)','valid=np.isfinite(x)'),
("B2_DROP_WEEKDAY",'return h.astype(np.int32)*7+w.astype(np.int32)','return h.astype(np.int32)'),
("SPARSE_FLOOR_ZERO_ONLY",'if n<SPARSE_MIN_TEST: out.append({"state":v,"count":n})','if 0<n<SPARSE_MIN_TEST: out.append({"state":v,"count":n})'),
("D2026_PRIMARY_LEAK",'PRIMARY_FOLDS = ("F1","F2","F3")','PRIMARY_FOLDS = ("F1","F2","F3","D2026")'),
("SUPPORT_ONE_BASELINE_ONLY",'for c in comp_names:','for c in comp_names[:1]:'),
("REFUTE_REQUIRES_BOTH_FAIL",'if pooled[c]["delta_log_loss"]<=0 or sum(v<=0 for v in vals)>=2:','if pooled[c]["delta_log_loss"]<=0 and sum(v<=0 for v in vals)>=2:'),
("SPARSE_SUPPORT_BYPASS",'if sparse_any: return "NOT_INTERPRETABLE"','if False and sparse_any: return "NOT_INTERPRETABLE"'),
("C01_USES_REL",'vol_raw=np.asarray(rv_context["abs"],dtype=np.float64)','vol_raw=np.asarray(rv_context["rel_by_fold"][fold_id],dtype=np.float64)'),
("C02_USES_ABS",'vol_raw=np.asarray(rv_context["rel_by_fold"][fold_id],dtype=np.float64)','vol_raw=np.asarray(rv_context["abs"],dtype=np.float64)'),
("WINNER_SELECTION_TRUE",'"winner_selection":False,','"winner_selection":True,'),
("SEMANTIC_LABEL_TRUE",'"semantic_regime_labels_instantiated":False,','"semantic_regime_labels_instantiated":True,'),
("PNL_TRUE",'"pnl_calculated":False,','"pnl_calculated":True,'),
("DIRECTION_TRUE",'"direction_target_used":False,','"direction_target_used":True,'),
("COLUMN_SPREAD_INJECT",'READ_COLUMNS = ["minute_start_ms_utc","tick_count","segment_id","mid_close"]','READ_COLUMNS = ["minute_start_ms_utc","tick_count","segment_id","mid_close","spread_mean"]'),
("SPARSE_100_INSTEAD_500",'SPARSE_MIN_TEST = 500','SPARSE_MIN_TEST = 100'),
]

def run_one(item):
    name,old,new=item
    if old not in SOURCE:
        return name,"SETUP_FAIL","replacement not found"
    mutated=SOURCE.replace(old,new,1)
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"cr2_mutant.py"; p.write_text(mutated)
        env=os.environ.copy(); env["CR2_MODULE_PATH"]=str(p)
        r=subprocess.run([sys.executable,TEST],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        return name,("KILLED" if r.returncode!=0 else "SURVIVED"),r.stdout

with ThreadPoolExecutor(max_workers=5) as ex:
    results=list(ex.map(run_one,MUTANTS))
killed=[]; survived=[]
for name,status,out in results:
    print(status,name)
    if status=="KILLED": killed.append(name)
    elif status=="SURVIVED":
        survived.append(name); print(out)
    else:
        print(out); sys.exit(2)
print(f"{len(killed)}/{len(MUTANTS)} KILLED")
if survived:
    print("SURVIVORS",",".join(survived)); sys.exit(1)
