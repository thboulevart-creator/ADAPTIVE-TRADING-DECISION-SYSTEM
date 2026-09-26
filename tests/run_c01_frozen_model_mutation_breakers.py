import os, pathlib, subprocess, sys, tempfile
SOURCE=pathlib.Path("/mnt/data/c01_frozen_model_artifact.py").read_text()
TEST="/mnt/data/test_c01_frozen_model_artifact.py"
MUTANTS=[
 ("OLD_CHARTER_ACCEPTED",'if ch.get("schema") != "ATDS_C01_CONFIRMATORY_RESEARCH_CHARTER_V0_2":','if False and ch.get("schema") != "ATDS_C01_CONFIRMATORY_RESEARCH_CHARTER_V0_2":'),
 ("WINDOW_DRIFT_ACCEPTED",'if conf.get("eligible_start_utc") != "2026-05-25T00:00:00Z" or conf.get("fixed_end_utc") != "2027-05-24T23:59:59Z":','if False and (conf.get("eligible_start_utc") != "2026-05-25T00:00:00Z" or conf.get("fixed_end_utc") != "2027-05-24T23:59:59Z"):'),
 ("THRESHOLD_DRIFT_ACCEPTED",'if ev != exact:','if False and ev != exact:'),
 ("C02_PROMOTION_ACCEPTED",'if got != expected:','if False and got != expected:'),
 ("PNL_SCOPE_ACCEPTED",'if any(scope.get(k) is not False for k in forbidden):','if False and any(scope.get(k) is not False for k in forbidden):'),
 ("PAD_OVERSIZE_ACCEPTED",'if a.ndim != 2 or a.shape[1] != k or a.shape[0] > nkeys:','if a.ndim != 2 or a.shape[1] != k:'),
 ("NO_LAPLACE",'return (c + alpha) / (c.sum(axis=1, keepdims=True) + alpha * c.shape[1])','return c / np.maximum(c.sum(axis=1, keepdims=True),1.0)'),
 ("DIGEST_BLIND_COUNTS",'(cand_counts, "<i8"),',''),
 ("COMPARE_TOLERANCE_WEAK",'if g.shape != e.shape or not np.allclose(g, e, rtol=0.0, atol=atol, equal_nan=False):','if g.shape != e.shape or not np.allclose(g, e, rtol=1.0, atol=1.0, equal_nan=False):'),
 ("D2026_SCORE_BYPASS",'if abs(float(rr[key]) - float(gg[key])) > atol:','if False and abs(float(rr[key]) - float(gg[key])) > atol:'),
 ("D2026_COUNT_BYPASS",'if ref.get("joint_state_counts_test") != result.get("joint_state_counts_test"):','if False and ref.get("joint_state_counts_test") != result.get("joint_state_counts_test"):'),
 ("CONFIRM_ACCESS_TRUE",'"confirmation_data_accessed": False,','"confirmation_data_accessed": True,'),
 ("PNL_TRUE",'"pnl_calculated": False,','"pnl_calculated": True,'),
 ("WINNER_TRUE",'"winner_selection": False,','"winner_selection": True,'),
 ("SYMLINK_BYPASS",'if stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):','if False and (stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):'),
]
killed=[]; survived=[]
for name,old,new in MUTANTS:
    if old not in SOURCE:
        print("SETUP_FAIL",name); sys.exit(2)
    mutated=SOURCE.replace(old,new,1)
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/"mutant.py"; p.write_text(mutated)
        env=os.environ.copy(); env["C01_MODEL_MODULE_PATH"]=str(p)
        r=subprocess.run([sys.executable,TEST],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode!=0:
            killed.append(name); print("KILLED",name)
        else:
            survived.append(name); print("SURVIVED",name); print(r.stdout)
print(f"{len(killed)}/{len(MUTANTS)} KILLED")
if survived:
    print("SURVIVORS",",".join(survived)); sys.exit(1)
