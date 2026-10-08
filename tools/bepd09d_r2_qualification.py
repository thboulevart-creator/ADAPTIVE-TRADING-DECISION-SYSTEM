from __future__ import annotations
import hashlib, importlib.util, io, json, math, os, platform, subprocess, unittest
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import scipy
from scipy.optimize import minimize, root, linprog

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-pre-retry"
OUT.mkdir(parents=True,exist_ok=True)
LEDGER=ROOT/"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PART=ROOT/"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
TESTFILE=ROOT/"tests/test_bepd09c_runtime.py"
EXPECTED_SHA="301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"
NUM_ATOL=2e-5
STRUCT_ATOL=1e-12

def wr(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")

def git_blob(path):
    line=subprocess.check_output(["git","ls-tree","HEAD","--",path],cwd=ROOT,text=True).strip()
    if not line: raise RuntimeError("MISSING:"+path)
    return line.split()[2]

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    if s is None or s.loader is None: raise RuntimeError("LOAD:"+name)
    m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def score_inf(X,y,b):
    z=X@b
    p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
    return float(np.max(np.abs(X.T@(p-y))))

def objective(X,y,b):
    z=X@b
    return float(np.sum(np.logaddexp(0,z)-y*z))

def primary_capture(X,y):
    signs=np.where(y>.5,1.,-1.)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method="highs")
    def f(b): return objective(X,y,b)
    def g(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return X.T@(p-y)
    def H(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); w=p*(1-p); return X.T@(X*w[:,None])
    r=minimize(f,np.zeros(X.shape[1]),jac=g,hess=H,method="Newton-CG",options={"xtol":1e-10,"maxiter":5000,"disp":False})
    return r,sep

def reference_capture(X,y):
    signs=np.where(y>.5,1.,-1.)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method="highs")
    def g(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return X.T@(p-y)
    def H(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); w=p*(1-p); return X.T@(X*w[:,None])
    r=root(g,np.zeros(X.shape[1]),jac=H,method="hybr",options={"xtol":1e-10,"maxfev":5000})
    return r,sep

def synthetic_once(r2):
    tm=load("r2_test_module",TESTFILE)
    tm.P=r2
    tm.ATOL=r2.NUMERIC_PARITY_ATOL
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(tm.T)
    stream=io.StringIO()
    res=unittest.TextTestRunner(stream=stream,verbosity=0).run(suite)
    fx=tm.FX
    p1=r2.run_protocol(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    p2=r2.run_protocol(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    r1=tm.R.run_reference(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    r2id=tm.R.run_reference(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    return {"tests_run":res.testsRun,"failures":len(res.failures),"errors":len(res.errors),"successful":res.wasSuccessful(),
            "primary_replay_1":p1,"primary_replay_2":p2,"reference_replay_1":r1,"reference_replay_2":r2id}

def audit_once(r2,ref,rows,cal):
    rp=r2.validate_rows(rows,cal)
    rr=ref._prep(rows,cal)
    blocks=r2.partition_calendar(cal)
    primary=[]; reference=[]; consistency=[]
    for i in range(1,6):
        trw={w for b in blocks[:i] for w in b}
        tp=[x for x in rp if x["target_week_id"] in trw]
        tr=[x for x in rr if x["target_week_id"] in trw]
        stats=r2._stats(tp)
        xb,xc=r2._mats(tp,stats)
        y=np.array([x["y"] for x in tp],float)
        rstats={}
        for k in ("age","active","overshoot"):
            v=np.array([x[k] for x in tr],float); rstats[k]=(float(v.mean()),float(v.std(ddof=1)))
        rb=[]; rc=[]
        for x in tr:
            base=[1.0]+list(x["basis"])
            rb.append(base); rc.append(base+[x["side"]]+[(x[k]-rstats[k][0])/rstats[k][1] for k in ("age","active","overshoot")])
        rb=np.array(rb,float); rc=np.array(rc,float)
        structural=max(float(np.max(np.abs(xb-rb))),float(np.max(np.abs(xc-rc))))
        if structural>STRUCT_ATOL: raise RuntimeError("PRIMARY_REFERENCE_STRUCTURAL_INCONSISTENCY")
        for model,X,RX in (("BASELINE",xb,rb),("CONTEXT",xc,rc)):
            # Authoritative frozen-path calls.
            bp=r2.fit_logistic(X,y)
            br=ref._fit(RX,y)
            # Diagnostic captures of the exact frozen algorithms.
            pc,psep=primary_capture(X,y)
            rcpt,rsep=reference_capture(RX,y)
            if not pc.success: raise RuntimeError("ANY_REAL_TRAINING_FIT_NONCONVERGENCE")
            if not (rcpt.success or score_inf(RX,y,rcpt.x)<=1e-8): raise RuntimeError("REFERENCE_TRAINING_FIT_FAILURE")
            if psep.success or rsep.success: raise RuntimeError("PERFECT_SEPARATION")
            pobj=objective(X,y,bp); robj=objective(RX,y,br)
            od=abs(pobj-robj)
            if od>NUM_ATOL: raise RuntimeError("PRIMARY_REFERENCE_SOLUTION_INCONSISTENCY")
            base_rec={"fold":i,"model":model,"train_event_count":len(tp),
                      "train_response_class_counts":{"0":int(np.sum(y==0)),"1":int(np.sum(y==1))},
                      "design_matrix_rank":int(np.linalg.matrix_rank(X)),"design_condition_number":float(np.linalg.cond(X)),
                      "perfect_separation":False,"finite":bool(np.all(np.isfinite(bp)))}
            primary.append({**base_rec,"solver_success":True,"termination_status":str(pc.message),
                            "iteration_count":int(pc.nit),"function_evaluation_count":int(pc.nfev),
                            "gradient_inf_norm":score_inf(X,y,bp)})
            reference.append({**base_rec,"solver_success":True,"termination_status":str(rcpt.message),
                              "function_evaluation_count":int(rcpt.nfev),"score_inf_norm":score_inf(RX,y,br)})
            consistency.append({"fold":i,"model":model,"structural_max_abs_difference":structural,
                                "objective_abs_difference":od,
                                "parameter_max_abs_difference":float(np.max(np.abs(np.asarray(bp)-np.asarray(br)))),
                                "primary_score_inf_norm":score_inf(X,y,bp),
                                "reference_score_inf_norm":score_inf(RX,y,br),"status":"PASS"})
    core={"primary":primary,"reference":reference,"consistency":consistency,
          "test_predictions_computed":False,"test_scoring_computed":False,"logloss_computed":False,"brier_computed":False}
    ident=hashlib.sha256(json.dumps(core,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    return core,ident

try:
    if os.environ.get("GITHUB_REPOSITORY")!="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM": raise RuntimeError("WRONG_REPOSITORY")
    if os.environ.get("GITHUB_REF_NAME")!="integration/system-v1": raise RuntimeError("WRONG_BRANCH")
    if not (platform.python_version().startswith("3.12.") and np.__version__=="2.3.5" and scipy.__version__=="1.17.0" and ZoneInfo("America/New_York").key=="America/New_York"):
        raise RuntimeError("ENVIRONMENT_DRIFT")
    ids={
      "f1_closure":git_blob("GOVERNANCE/BEPD-09D-F1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-08.md"),
      "source_runtime":git_blob("tools/bepd09c_runtime.py"),
      "r2_runtime":git_blob("tools/bepd09d_r2_runtime.py"),
      "reference_runtime":git_blob("tools/bepd09c_reference.py"),
      "partition":git_blob("GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json")
    }
    expected={"f1_closure":"67133fc7b978dbef68f021066ffb3970fea51543","source_runtime":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
              "r2_runtime":"58a68c6ad8ecb7db2a1294ad90d26f4f01c9de85","reference_runtime":"2c8a82405082ce3f820b580017a96af77e74b0e4",
              "partition":"7d950d957611cf209d811c788ff10abded30d011"}
    if ids!=expected: raise RuntimeError("IDENTITY_MISMATCH")
    r2=load("bepd09d_r2_runtime",ROOT/"tools/bepd09d_r2_runtime.py")
    ref=load("bepd09d_r2_reference",ROOT/"tools/bepd09c_reference.py")
    if r2.MAX_ITER!=5000 or r2.FIT_TOL!=1e-10: raise RuntimeError("R2_BEHAVIOR_MISMATCH")
    syn1=synthetic_once(r2); syn2=synthetic_once(r2)
    if not (syn1["successful"] and syn2["successful"] and syn1["tests_run"]==44 and syn2["tests_run"]==44): raise RuntimeError("SYNTHETIC_REGRESSION_FAILURE")
    if syn1["primary_replay_1"]!=syn1["primary_replay_2"] or syn2["primary_replay_1"]!=syn2["primary_replay_2"]: raise RuntimeError("NONDETERMINISTIC_SYNTHETIC_PRIMARY")
    if syn1["reference_replay_1"]!=syn1["reference_replay_2"] or syn2["reference_replay_1"]!=syn2["reference_replay_2"]: raise RuntimeError("NONDETERMINISTIC_SYNTHETIC_REFERENCE")
    wr("07_SYNTHETIC_REQUALIFICATION_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_SYNTHETIC_REQUALIFICATION_RECEIPT_V0_1","status":"PASS","run_1":syn1,"run_2":syn2,"expected_tests":44})
    raw=LEDGER.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA: raise RuntimeError("WRONG_EVENT_LEDGER")
    rows=[json.loads(x) for x in raw.decode().splitlines() if x.strip()]
    if len(rows)!=472: raise RuntimeError("WRONG_EVENT_LEDGER_ROW_COUNT")
    cal=[w for b in json.loads(PART.read_text())["blocks"] for w in b["weeks"]]
    if len(cal)!=259: raise RuntimeError("WRONG_CALENDAR")
    a1,id1=audit_once(r2,ref,rows,cal); a2,id2=audit_once(r2,ref,rows,cal)
    if id1!=id2: raise RuntimeError("NONDETERMINISTIC_REPLAY")
    if len(a1["primary"])!=10 or len(a1["reference"])!=10: raise RuntimeError("FIT_COUNT_MISMATCH")
    wr("08_REAL_TRAINING_PRIMARY_CONVERGENCE_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_PRIMARY_TRAINING_CONVERGENCE_V0_1","status":"PASS","fit_count":10,"fits":a1["primary"],"replay_identity":id1})
    wr("09_REAL_TRAINING_REFERENCE_CONVERGENCE_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_REFERENCE_TRAINING_CONVERGENCE_V0_1","status":"PASS","fit_count":10,"fits":a1["reference"],"replay_identity":id1})
    wr("10_PRIMARY_REFERENCE_TRAINING_CONSISTENCY_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_TRAINING_CONSISTENCY_V0_1","status":"PASS","numeric_atol":NUM_ATOL,"structural_atol":STRUCT_ATOL,"fits":a1["consistency"],"replay_identity_1":id1,"replay_identity_2":id2})
    wr("11_PRE_RETRY_QUALIFICATION_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_PRE_RETRY_QUALIFICATION_V0_1","status":"PASS","verdict":"SOLVER_TERMINATION_BEHAVIOR_AMENDMENT_QUALIFIED_AND_PRE_RETRY_READY_FOR_HUMAN_ADJUDICATION","synthetic":"44 / 44 PASS TWICE","primary_training_fits":"10 / 10 CONVERGED","reference_training_fits":"10 / 10 CONVERGED","training_consistency":"PASS","deterministic_replay":"PASS","test_predictions_computed":False,"test_scoring_computed":False,"logloss_computed":False,"brier_computed":False,"c1_retry_authorized":False,"scientific_result":"NONE","fresh_oos":False,"trading_authority":"NONE","stop":True})
    print("BEPD-09D-R2 PRE-RETRY QUALIFICATION PASS; STOP FOR HUMAN ADJUDICATION")
except Exception as e:
    wr("99_R2_FAILURE_RECEIPT.json",{"schema":"ATDS_BEPD_09D_R2_FAILURE_RECEIPT_V0_1","status":"BLOCKED_FAIL_CLOSED","error_type":type(e).__name__,"error":str(e),"test_predictions_computed":False,"scientific_result":"NONE","c1_retry_authorized":False,"trading_authority":"NONE"})
    raise
