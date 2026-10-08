from __future__ import annotations
import hashlib, importlib.util, io, json, os, platform, subprocess, unittest
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import scipy
from scipy.optimize import minimize, root, linprog

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-cr1-pre-retry"
OUT.mkdir(parents=True,exist_ok=True)
LEDGER=ROOT/"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PART=ROOT/"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
TESTFILE=ROOT/"tests/test_bepd09c_runtime.py"
R2PATH=ROOT/"tools/bepd09d_r2_runtime.py"
REFPATH=ROOT/"tools/bepd09c_reference.py"
EXPECTED_LEDGER_SHA="301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"
NUM_ATOL=2e-5
STRUCT_ATOL=1e-12

EXPECTED_BLOBS={
"GOVERNANCE/BEPD-09D-F1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-08.md":"67133fc7b978dbef68f021066ffb3970fea51543",
"reports/program/2026-10-08-BEPD-09D-R2-FAILURE-RECEIPT-V0.1.json":"349d81a29c0f40577c46ce0348ec0e65a9a022ca",
"reports/program/2026-10-08-BEPD-09D-R2-PERSISTED-HEAD-VERIFICATION-RECEIPT-V0.1.json":"a70196dc028af891779f65aac418c2af14731683",
"tools/bepd09c_runtime.py":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
"tools/bepd09c_reference.py":"2c8a82405082ce3f820b580017a96af77e74b0e4",
"tools/bepd09d_r2_runtime.py":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json":"7d950d957611cf209d811c788ff10abded30d011",
"GOVERNANCE/BEPD-09D-R2-CR1-HUMAN-AUTHORIZATION-2026-10-08.json":"b13fa7881a903b01717987cacedb3dc3ca6ba99c",
"GOVERNANCE/BEPD-09D-R2-CR1-INTERFACE-CORRECTION-CONTRACT-V0.1.json":"bccf58b8ec3edd08c405a8ed341b09c92cc418fc",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-SOURCE-DIFF-RECEIPT-V0.1.json":"d861041b6c61083933d4259686dbe9e2e6cc4fc7",
"GOVERNANCE/BEPD-09D-R2-CR1-BREAKER-CONTRACT-V0.1.json":"3e2885bc12d7a1e30ec8d05019fd2a75b68010be"
}

def wr(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")

def git_blob(path):
    line=subprocess.check_output(["git","ls-tree","HEAD","--",path],cwd=ROOT,text=True).strip()
    if not line: raise RuntimeError("MISSING_TRACKED_PATH:"+path)
    return line.split()[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError("MODULE_LOAD_FAILURE:"+name)
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

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
    res=minimize(f,np.zeros(X.shape[1]),jac=g,hess=H,method="Newton-CG",options={"xtol":1e-10,"maxiter":5000,"disp":False})
    return res,sep

def reference_capture(X,y):
    signs=np.where(y>.5,1.,-1.)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method="highs")
    def g(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); return X.T@(p-y)
    def H(b):
        z=X@b; p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z))); w=p*(1-p); return X.T@(X*w[:,None])
    res=root(g,np.zeros(X.shape[1]),jac=H,method="hybr",options={"xtol":1e-10,"maxfev":5000})
    return res,sep

def synthetic_once(r2):
    tm=load("cr1_test_module",TESTFILE)
    tm.P=r2
    tm.ATOL=r2.NUMERIC_PARITY_ATOL
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(tm.T)
    stream=io.StringIO()
    res=unittest.TextTestRunner(stream=stream,verbosity=0).run(suite)
    fx=tm.FX
    p1=r2.run_protocol(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    p2=r2.run_protocol(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    q1=tm.R.run_reference(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    q2=tm.R.run_reference(fx["rows"],fx["calendar"])["deterministic_replay_identity"]
    return {"tests_run":res.testsRun,"failures":len(res.failures),"errors":len(res.errors),"successful":res.wasSuccessful(),
            "primary_replay_1":p1,"primary_replay_2":p2,"reference_replay_1":q1,"reference_replay_2":q2}

def audit_once(r2,ref,rows,cal):
    primary_rows=r2.validate_rows(rows,cal)
    reference_rows=ref._prep(rows,cal)
    blocks=r2.partition_calendar(cal)
    primary=[]; reference=[]; consistency=[]
    for i in range(1,6):
        train_weeks={w for b in blocks[:i] for w in b}
        tp=[x for x in primary_rows if x["target_week_id"] in train_weeks]
        tr=[x for x in reference_rows if x["target_week_id"] in train_weeks]
        stats=r2._stats(tp)
        xb,xc=r2._mats(tp,stats)
        y=np.array([x["y"] for x in tp],float)

        ref_stats={}
        for k in ("age","active","overshoot"):
            vals=np.array([x[k] for x in tr],float)
            ref_stats[k]=(float(vals.mean()),float(vals.std(ddof=1)))
        rb=[]; rc=[]
        for x in tr:
            base=[1.0]+list(x["basis"])
            rb.append(base)
            rc.append(base+[x["side"]]+[(x[k]-ref_stats[k][0])/ref_stats[k][1] for k in ("age","active","overshoot")])
        rb=np.array(rb,float); rc=np.array(rc,float)

        structural=max(float(np.max(np.abs(xb-rb))),float(np.max(np.abs(xc-rc))))
        if structural>STRUCT_ATOL: raise RuntimeError("PRIMARY_REFERENCE_STRUCTURAL_INCONSISTENCY")

        for model,X,RX in (("BASELINE",xb,rb),("CONTEXT",xc,rc)):
            bp=r2.fit_logistic(X,y)
            br=ref._fit(RX,y)
            pc,psep=primary_capture(X,y)
            rcpt,rsep=reference_capture(RX,y)
            if not pc.success: raise RuntimeError("PRIMARY_TRAINING_NONCONVERGENCE")
            if not (rcpt.success or score_inf(RX,y,rcpt.x)<=1e-8): raise RuntimeError("REFERENCE_TRAINING_NONCONVERGENCE")
            if psep.success or rsep.success: raise RuntimeError("PERFECT_SEPARATION")
            if not (np.all(np.isfinite(bp)) and np.all(np.isfinite(br))): raise RuntimeError("NONFINITE_STATE")
            objdiff=abs(objective(X,y,bp)-objective(RX,y,br))
            if objdiff>NUM_ATOL: raise RuntimeError("PRIMARY_REFERENCE_CONSISTENCY_FAILURE")

            common={"fold":i,"model":model,"train_event_count":len(tp),
                    "train_response_class_counts":{"0":int(np.sum(y==0)),"1":int(np.sum(y==1))},
                    "design_matrix_rank":int(np.linalg.matrix_rank(X)),
                    "design_condition_number":float(np.linalg.cond(X)),
                    "perfect_separation":False,"finite":True}
            primary.append({**common,"solver_success":True,"termination_status":str(pc.message),
                            "iteration_count":int(pc.nit),"function_evaluation_count":int(pc.nfev),
                            "gradient_inf_norm":score_inf(X,y,bp)})
            reference.append({**common,"solver_success":True,"termination_status":str(rcpt.message),
                              "function_evaluation_count":int(rcpt.nfev),
                              "score_inf_norm":score_inf(RX,y,br)})
            consistency.append({"fold":i,"model":model,"structural_max_abs_difference":structural,
                                "objective_abs_difference":objdiff,
                                "parameter_max_abs_difference":float(np.max(np.abs(np.asarray(bp)-np.asarray(br)))),
                                "primary_score_inf_norm":score_inf(X,y,bp),
                                "reference_score_inf_norm":score_inf(RX,y,br),
                                "status":"PASS"})

    core={"primary":primary,"reference":reference,"consistency":consistency,
          "test_predictions_computed":False,"test_scoring_computed":False,
          "logloss_computed":False,"brier_computed":False}
    replay=hashlib.sha256(json.dumps(core,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
    return core,replay

try:
    if os.environ.get("GITHUB_REPOSITORY")!="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM": raise RuntimeError("WRONG_REPOSITORY")
    if os.environ.get("GITHUB_REF_NAME")!="integration/system-v1": raise RuntimeError("WRONG_BRANCH")
    if not (platform.python_version().startswith("3.12.") and np.__version__=="2.3.5" and scipy.__version__=="1.17.0" and ZoneInfo("America/New_York").key=="America/New_York"):
        raise RuntimeError("ENVIRONMENT_DRIFT")

    observed={k:git_blob(k) for k in EXPECTED_BLOBS}
    if observed!=EXPECTED_BLOBS: raise RuntimeError("IDENTITY_MISMATCH")

    r2=load("bepd09d_r2_cr1_runtime",R2PATH)
    ref=load("bepd09d_r2_cr1_reference",REFPATH)

    if r2._stats is not r2._base._stats: raise RuntimeError("_stats_NOT_IDENTICAL_TO_base._stats")
    if r2._mats is not r2._base._mats: raise RuntimeError("_mats_NOT_IDENTICAL_TO_base._mats")
    if r2.MAX_ITER!=5000: raise RuntimeError("MAX_ITER_NOT_5000")
    if r2.FIT_TOL!=1e-10: raise RuntimeError("XTOL_NOT_1E_MINUS_10")

    wr("07_CR1_INTERFACE_IDENTITY_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_INTERFACE_IDENTITY_RECEIPT_V0_1",
        "status":"PASS",
        "stats_identity":True,
        "mats_identity":True,
        "max_iter":r2.MAX_ITER,
        "fit_tol":r2.FIT_TOL,
        "corrected_overlay_blob":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1"
    })

    s1=synthetic_once(r2); s2=synthetic_once(r2)
    if not (s1["successful"] and s2["successful"] and s1["tests_run"]==44 and s2["tests_run"]==44):
        raise RuntimeError("SYNTHETIC_FAILURE")
    if s1["primary_replay_1"]!=s1["primary_replay_2"] or s2["primary_replay_1"]!=s2["primary_replay_2"]:
        raise RuntimeError("NONDETERMINISTIC_SYNTHETIC_PRIMARY")
    if s1["reference_replay_1"]!=s1["reference_replay_2"] or s2["reference_replay_1"]!=s2["reference_replay_2"]:
        raise RuntimeError("NONDETERMINISTIC_SYNTHETIC_REFERENCE")
    wr("08_CR1_SYNTHETIC_REQUALIFICATION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_SYNTHETIC_REQUALIFICATION_RECEIPT_V0_1",
        "status":"PASS","expected_tests":44,"run_1":s1,"run_2":s2,
        "deterministic_replay":"PASS","scientific_result":"NONE"
    })

    raw=LEDGER.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_LEDGER_SHA: raise RuntimeError("WRONG_EVENT_LEDGER")
    rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
    if len(rows)!=472: raise RuntimeError("WRONG_EVENT_LEDGER")
    cal=[w for b in json.loads(PART.read_text(encoding="utf-8"))["blocks"] for w in b["weeks"]]
    if len(cal)!=259: raise RuntimeError("WRONG_CALENDAR")

    a1,id1=audit_once(r2,ref,rows,cal)
    a2,id2=audit_once(r2,ref,rows,cal)
    if id1!=id2: raise RuntimeError("NONDETERMINISTIC_REPLAY")
    if len(a1["primary"])!=10: raise RuntimeError("PRIMARY_FIT_COUNT_MISMATCH")
    if len(a1["reference"])!=10: raise RuntimeError("REFERENCE_FIT_COUNT_MISMATCH")

    wr("09_CR1_REAL_TRAINING_PRIMARY_CONVERGENCE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_PRIMARY_TRAINING_CONVERGENCE_V0_1",
        "status":"PASS","fit_count":10,"fits":a1["primary"],"replay_identity":id1
    })
    wr("10_CR1_REAL_TRAINING_REFERENCE_CONVERGENCE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_REFERENCE_TRAINING_CONVERGENCE_V0_1",
        "status":"PASS","fit_count":10,"fits":a1["reference"],"replay_identity":id1
    })
    wr("11_CR1_PRIMARY_REFERENCE_TRAINING_CONSISTENCY_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_TRAINING_CONSISTENCY_V0_1",
        "status":"PASS","numeric_atol":NUM_ATOL,"structural_atol":STRUCT_ATOL,
        "fits":a1["consistency"],"replay_identity_1":id1,"replay_identity_2":id2
    })
    wr("12_CR1_R2_PRE_RETRY_QUALIFICATION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_PRE_RETRY_QUALIFICATION_V0_1",
        "status":"PASS",
        "verdict":"BEPD_09D_R2_CR1_QUALIFIED_AND_BEPD_09D_R2_SOLVER_TERMINATION_BEHAVIOR_AMENDMENT_QUALIFIED_PRE_RETRY_READY_FOR_HUMAN_ADJUDICATION",
        "interface_identity":"PASS",
        "synthetic":"44 / 44 PASS TWICE",
        "primary_training_fits":"10 / 10 CONVERGED",
        "reference_training_fits":"10 / 10 CONVERGED",
        "training_consistency":"PASS",
        "deterministic_replay":"PASS",
        "test_predictions_computed":False,
        "test_scoring_computed":False,
        "logloss_computed":False,
        "brier_computed":False,
        "scientific_result":"NONE",
        "c1_retry_authorized":False,
        "fresh_oos":"CLOSED",
        "trading_authority":"NONE",
        "stop":True
    })
    print("BEPD-09D-R2-CR1 QUALIFIED; BEPD-09D-R2 PRE-RETRY READY FOR HUMAN ADJUDICATION; STOP")
except Exception as e:
    wr("99_CR1_FAILURE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_FAILURE_RECEIPT_V0_1",
        "status":"BLOCKED_FAIL_CLOSED",
        "error_type":type(e).__name__,
        "error":str(e),
        "test_predictions_computed":False,
        "test_scoring_computed":False,
        "logloss_computed":False,
        "brier_computed":False,
        "scientific_result":"NONE",
        "c1_retry_authorized":False,
        "repair_beyond_authority_occurred":False,
        "trading_authority":"NONE",
        "stop":True
    })
    raise
