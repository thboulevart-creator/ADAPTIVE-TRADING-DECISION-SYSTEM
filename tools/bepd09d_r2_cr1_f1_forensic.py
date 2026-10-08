from __future__ import annotations
import hashlib, importlib.util, json, math, os, platform, subprocess, traceback
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import scipy
from scipy.optimize import minimize, linprog, root

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-cr1-f1-forensics"
OUT.mkdir(parents=True,exist_ok=True)
LEDGER=ROOT/"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PART=ROOT/"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
R2PATH=ROOT/"tools/bepd09d_r2_runtime.py"
REFPATH=ROOT/"tools/bepd09c_reference.py"
EXPECTED_LEDGER_SHA="301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"
MAX_ITER=5000
XTOL=1e-10

EXPECTED={
"GOVERNANCE/BEPD-09D-F1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-08.md":"67133fc7b978dbef68f021066ffb3970fea51543",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-FAILURE-RECEIPT-V0.1.json":"3a08cf99c95ac2a4afcbae5a877ed0d13aeaebc0",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-TECHNICAL-STATUS-RECEIPT-V0.1.json":"e7479ecc038a7879572d6dfe67d4e03471703721",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-PERSISTED-HEAD-VERIFICATION-RECEIPT-V0.1.json":"60df007666327772209f320818b3228485f3d548",
"tools/bepd09d_r2_runtime.py":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
"tools/bepd09c_runtime.py":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
"tools/bepd09c_reference.py":"2c8a82405082ce3f820b580017a96af77e74b0e4",
"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json":"7d950d957611cf209d811c788ff10abded30d011",
"GOVERNANCE/BEPD-09D-R2-CR1-F1-HUMAN-AUTHORIZATION-2026-10-08.json":"84d6866d20bd554547196d511331daa79b0fd8f9",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-FRESH-FORENSIC-PREFLIGHT-RECEIPT-V0.1.json":"c0e5b2ef6ee56270c57cae764e186a0ebfd6538c",
"GOVERNANCE/BEPD-09D-R2-CR1-F1-FAILURE-SEQUENCE-INSTRUMENTATION-CONTRACT-V0.1.json":"5bcaebd21d1bd84a1bc79d1a81817cb9fc3d3030",
"GOVERNANCE/BEPD-09D-R2-CR1-F1-FORENSIC-BREAKER-CONTRACT-V0.1.json":"900fb047d7f8b1413b0370261ced631c272d820d"
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

def exact_solver_capture(X,y):
    X=np.asarray(X,float); y=np.asarray(y,float)
    signs=np.where(y>0.5,1.0,-1.0)
    sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method="highs")
    def fun(b):
        z=X@b
        return float(np.sum(np.logaddexp(0,z)-y*z))
    def jac(b):
        z=X@b
        p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
        return X.T@(p-y)
    def hess(b):
        z=X@b
        p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
        w=p*(1-p)
        return X.T@(X*w[:,None])
    x0=np.zeros(X.shape[1])
    res=minimize(fun,x0,jac=jac,hess=hess,method="Newton-CG",options={"xtol":XTOL,"maxiter":MAX_ITER,"disp":False})
    b=np.asarray(res.x,float); g=np.asarray(jac(b),float); H=np.asarray(hess(b),float)
    z=X@b
    p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
    sv=np.linalg.svd(X,compute_uv=False)
    ev=np.linalg.eigvalsh((H+H.T)/2)
    finite={
        "design_matrix":bool(np.all(np.isfinite(X))),
        "response":bool(np.all(np.isfinite(y))),
        "initial_vector":bool(np.all(np.isfinite(x0))),
        "final_vector":bool(np.all(np.isfinite(b))),
        "objective":bool(math.isfinite(fun(b))),
        "gradient":bool(np.all(np.isfinite(g))),
        "hessian":bool(np.all(np.isfinite(H)))
    }
    state={
        "success":bool(res.success),
        "status":int(res.status),
        "message":str(res.message),
        "iteration_count":int(getattr(res,"nit",-1)),
        "function_evaluation_count":int(getattr(res,"nfev",-1)),
        "gradient_evaluation_count":int(getattr(res,"njev",-1)),
        "score_inf_norm":float(np.max(np.abs(g))),
        "objective_value":float(fun(b)),
        "coefficient_finiteness":finite["final_vector"],
        "linear_predictor_min":float(np.min(z)),
        "linear_predictor_max":float(np.max(z)),
        "probability_min":float(np.min(p)),
        "probability_max":float(np.max(p)),
        "saturation_count_1e_12":int(np.sum((p<1e-12)|(p>1-1e-12))),
        "design_matrix_shape":[int(X.shape[0]),int(X.shape[1])],
        "matrix_rank":int(np.linalg.matrix_rank(X)),
        "full_column_rank":bool(np.linalg.matrix_rank(X)==X.shape[1]),
        "singular_values":[float(v) for v in sv],
        "condition_number":float(np.linalg.cond(X)),
        "hessian_min_eigenvalue":float(np.min(ev)),
        "hessian_max_eigenvalue":float(np.max(ev)),
        "hessian_condition_number":float(np.linalg.cond(H)),
        "perfect_separation":bool(sep.success),
        "finiteness":finite
    }
    return state,jac,hess

def reference_diagnostic(X,y,jac,hess):
    rr=root(jac,np.zeros(X.shape[1]),jac=hess,method="hybr",options={"xtol":1e-10,"maxfev":5000})
    score=np.asarray(jac(rr.x),float)
    return {
        "solver":"ROOT_HYBR_SCORE_EQUATION",
        "forensic_only":True,
        "non_scientific":True,
        "non_admissible_as_c1_result":True,
        "success":bool(rr.success),
        "message":str(rr.message),
        "function_evaluation_count":int(getattr(rr,"nfev",-1)),
        "score_inf_norm":float(np.max(np.abs(score))),
        "finite_solution":bool(np.all(np.isfinite(rr.x)))
    }

def classify(state,refdiag,classes):
    if classes["0"]==0 or classes["1"]==0:
        return {"classification":"G","label":"ONE_CLASS_TRAINING_CONDITION","evidence_grade":"PROVEN","same_root_cause_as_original_f1":"NO","future_repair_class":"NOT_DETERMINED"}
    if state["perfect_separation"]:
        return {"classification":"A","label":"PERFECT_SEPARATION","evidence_grade":"PROVEN","same_root_cause_as_original_f1":"NO","future_repair_class":"NOT_DETERMINED"}
    if not state["full_column_rank"]:
        return {"classification":"B","label":"RANK_DEFICIENCY","evidence_grade":"PROVEN","same_root_cause_as_original_f1":"NO","future_repair_class":"NOT_DETERMINED"}
    if not all(state["finiteness"].values()):
        return {"classification":"C","label":"NONFINITE_NUMERICAL_STATE","evidence_grade":"PROVEN","same_root_cause_as_original_f1":"NO","future_repair_class":"NOT_DETERMINED"}
    msg=state["message"].lower()
    if (not state["success"]) and ("maximum number of iterations" in msg or state["status"]==1) and refdiag["success"] and refdiag["finite_solution"] and refdiag["score_inf_norm"]<=1e-8:
        return {
            "classification":"D",
            "label":"SOLVER_TERMINATION_OPTIMIZER_LIMITATION",
            "evidence_grade":"PROVEN",
            "same_root_cause_as_original_f1":"YES",
            "future_repair_class":"R2_POTENTIAL_NOT_AUTHORIZED",
            "conditioning_observed":{
                "design_condition_number":state["condition_number"],
                "hessian_condition_number":state["hessian_condition_number"],
                "interpretation":"CONTRIBUTORY_CONDITION_NOT_SEPARATELY_REQUIRED_FOR_D_CLASSIFICATION"
            }
        }
    if state["condition_number"]>=1e6 or state["hessian_condition_number"]>=1e10:
        return {"classification":"E","label":"SEVERE_NUMERICAL_CONDITIONING","evidence_grade":"CONSISTENT_WITH_NOT_PROVEN_AS_SOLE_CAUSE","same_root_cause_as_original_f1":"NOT_PROVEN","future_repair_class":"NOT_DETERMINED"}
    return {"classification":"H","label":"ROOT_CAUSE_NOT_PROVEN","evidence_grade":"NOT_PROVEN","same_root_cause_as_original_f1":"NOT_PROVEN","future_repair_class":"NOT_DETERMINED"}

try:
    if os.environ.get("GITHUB_REPOSITORY")!="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM": raise RuntimeError("WRONG_REPOSITORY")
    if os.environ.get("GITHUB_REF_NAME")!="integration/system-v1": raise RuntimeError("WRONG_BRANCH")
    if not (platform.python_version().startswith("3.12.") and np.__version__=="2.3.5" and scipy.__version__=="1.17.0" and ZoneInfo("America/New_York").key=="America/New_York"):
        raise RuntimeError("WRONG_ENVIRONMENT")
    observed={k:git_blob(k) for k in EXPECTED}
    if observed!=EXPECTED: raise RuntimeError("IDENTITY_MISMATCH")

    r2=load("bepd09d_r2_cr1_f1_runtime",R2PATH)
    if r2.MAX_ITER!=5000 or r2.FIT_TOL!=1e-10: raise RuntimeError("FROZEN_SOLVER_STATE_MISMATCH")

    raw=LEDGER.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_LEDGER_SHA: raise RuntimeError("WRONG_EVENT_LEDGER")
    rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
    if len(rows)!=472: raise RuntimeError("WRONG_EVENT_LEDGER_ROW_COUNT")
    cal=[w for b in json.loads(PART.read_text(encoding="utf-8"))["blocks"] for w in b["weeks"]]
    if len(cal)!=259: raise RuntimeError("WRONG_CALENDAR")

    rs=r2.validate_rows(rows,cal)
    blocks=r2.partition_calendar(cal)
    sequence=[]
    failed=None
    idx=0

    for fold in range(1,6):
        train_weeks={w for b in blocks[:fold] for w in b}
        train=[x for x in rs if x["target_week_id"] in train_weeks]
        stats=r2._stats(train)
        xb,xc=r2._mats(train,stats)
        y=np.array([x["y"] for x in train],float)
        classes={"0":int(np.sum(y==0)),"1":int(np.sum(y==1))}
        for model,X in (("BASELINE",xb),("CONTEXT",xc)):
            idx+=1
            pre={
                "fit_sequence_index":idx,
                "fold":fold,
                "model":model,
                "train_event_count":len(train),
                "train_response_class_counts":classes,
                "design_matrix_shape":[int(X.shape[0]),int(X.shape[1])],
                "design_matrix_rank":int(np.linalg.matrix_rank(X))
            }
            try:
                r2.fit_logistic(X,y)
                sequence.append({**pre,"status":"CONVERGED"})
            except Exception as exc:
                if str(exc)!="MODEL_NONCONVERGENCE":
                    raise
                state,jac,hess=exact_solver_capture(X,y)
                refdiag=reference_diagnostic(X,y,jac,hess)
                cause=classify(state,refdiag,classes)
                failed={**pre,"status":"MODEL_NONCONVERGENCE","newton_cg_state":state,"reference_solver_diagnostic":refdiag,"root_cause":cause}
                sequence.append({**pre,"status":"MODEL_NONCONVERGENCE"})
                break
        if failed:
            break

    if failed is None:
        raise RuntimeError("FORENSIC_REPRODUCTION_MISMATCH_NO_MODEL_NONCONVERGENCE")

    wr("05_FAILED_FIT_IDENTIFICATION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_FAILED_FIT_IDENTIFICATION_RECEIPT_V0_1",
        "status":"PASS",
        "fit_sequence":sequence,
        "failed_fit_sequence_index":failed["fit_sequence_index"],
        "failed_fold":failed["fold"],
        "failed_model":failed["model"],
        "train_event_count":failed["train_event_count"],
        "train_response_class_counts":failed["train_response_class_counts"],
        "test_predictions_computed":False,
        "test_scoring_computed":False
    })
    wr("06_ORIGINAL_NEWTON_CG_STATE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_NEWTON_CG_STATE_RECEIPT_V0_1",
        "status":"PASS",
        "fold":failed["fold"],
        "model":failed["model"],
        "solver":"Newton-CG",
        "max_iter":5000,
        "xtol":1e-10,
        "initialization":"ZERO_VECTOR",
        **failed["newton_cg_state"]
    })
    wr("07_DESIGN_MATRIX_CONDITIONING_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_DESIGN_MATRIX_CONDITIONING_RECEIPT_V0_1",
        "status":"PASS",
        "fold":failed["fold"],
        "model":failed["model"],
        **{k:failed["newton_cg_state"][k] for k in [
            "design_matrix_shape","matrix_rank","full_column_rank","singular_values",
            "condition_number","hessian_min_eigenvalue","hessian_max_eigenvalue",
            "hessian_condition_number","finiteness"
        ]}
    })
    wr("08_SEPARATION_RESPONSE_STRUCTURE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_SEPARATION_RESPONSE_STRUCTURE_RECEIPT_V0_1",
        "status":"PASS",
        "fold":failed["fold"],
        "model":failed["model"],
        "class_0_count":failed["train_response_class_counts"]["0"],
        "class_1_count":failed["train_response_class_counts"]["1"],
        "one_class_failure":failed["train_response_class_counts"]["0"]==0 or failed["train_response_class_counts"]["1"]==0,
        "perfect_separation":failed["newton_cg_state"]["perfect_separation"]
    })
    wr("09_REFERENCE_SOLVER_FORENSIC_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_REFERENCE_SOLVER_FORENSIC_RECEIPT_V0_1",
        "status":"PASS",
        "fold":failed["fold"],
        "model":failed["model"],
        **failed["reference_solver_diagnostic"]
    })
    wr("10_ROOT_CAUSE_CLASSIFICATION_PACKAGE.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_ROOT_CAUSE_CLASSIFICATION_PACKAGE_V0_1",
        "status":"QUALIFIED_FOR_HUMAN_ADJUDICATION",
        "failed_fold":failed["fold"],
        "failed_model":failed["model"],
        "root_cause":failed["root_cause"],
        "repair_applied":False,
        "c1_retry_authorized":False,
        "scientific_result":"NONE",
        "trading_authority":"NONE"
    })
    wr("11_FORENSIC_QUALIFICATION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_FORENSIC_QUALIFICATION_RECEIPT_V0_1",
        "status":"PASS",
        "verdict":"FORENSICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION",
        "failed_fit_identified_exactly":True,
        "failed_fold":failed["fold"],
        "failed_model":failed["model"],
        "root_cause_classification":failed["root_cause"]["classification"],
        "root_cause_evidence_grade":failed["root_cause"]["evidence_grade"],
        "same_root_cause_as_original_f1":failed["root_cause"]["same_root_cause_as_original_f1"],
        "test_predictions_computed":False,
        "test_scoring_computed":False,
        "logloss_computed":False,
        "brier_computed":False,
        "scientific_result":"NONE",
        "repair_applied":False,
        "c1_retry_authorized":False,
        "fresh_oos":"CLOSED",
        "trading_authority":"NONE",
        "next":"HUMAN_ADJUDICATION_OF_BEPD_09D_R2_CR1_F1",
        "stop":True
    })
    print("BEPD-09D-R2-CR1-F1 FORENSIC QUALIFICATION COMPLETED; STOP FOR HUMAN ADJUDICATION")
except Exception as exc:
    wr("99_FORENSIC_FAILURE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F1_FAILURE_RECEIPT_V0_1",
        "status":"BLOCKED_FAIL_CLOSED",
        "error_type":type(exc).__name__,
        "error":str(exc),
        "traceback":traceback.format_exc(),
        "repair_applied":False,
        "c1_retry_authorized":False,
        "scientific_result":"NONE",
        "trading_authority":"NONE",
        "stop":True
    })
    raise
