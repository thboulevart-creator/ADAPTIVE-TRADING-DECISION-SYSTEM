from __future__ import annotations
import hashlib, importlib.util, inspect, json, math, os, platform, re, subprocess, traceback
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import scipy
from scipy.optimize import minimize, root
import scipy.optimize._optimize as scipy_optimize_internal

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-cr1-f2-precision-loss"
OUT.mkdir(parents=True,exist_ok=True)

LEDGER=ROOT/"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PART=ROOT/"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
R2PATH=ROOT/"tools/bepd09d_r2_runtime.py"

EXPECTED_LEDGER_SHA256="301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"
MAX_ITER=5000
XTOL=1e-10
FIT_TOL=1e-10
EPS=np.finfo(np.float64).eps
FD_STEP_POWER=1.0/5.0
GRAD_ERR_THRESHOLD=5e-7
HESS_ERR_THRESHOLD=5e-7
PRACTICAL_STATIONARY=1e-10
NEAR_STATIONARY=1e-7
VECTOR_REPLAY_ATOL=1e-12
OBJECTIVE_REPLAY_ATOL=1e-12
SCORE_REPLAY_ATOL=1e-12

EXPECTED={
"GOVERNANCE/BEPD-09D-R2-CR1-F1-FINAL-HUMAN-ADJUDICATION-CLOSURE-2026-10-08.md":"a7360bb1db335861db8c15c1d09278bac6eb62aa",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-FAILED-FIT-IDENTIFICATION-RECEIPT-V0.1.json":"f6bbfa7ef5d4b37ccb489df34e728714872393ee",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-NEWTON-CG-STATE-RECEIPT-V0.1.json":"1aabe9794024d4a34a4bff71a20e01c350241209",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-DESIGN-MATRIX-CONDITIONING-RECEIPT-V0.1.json":"097f346938ac27bb314a22656f9eb72a2db74e2b",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-REFERENCE-SOLVER-FORENSIC-RECEIPT-V0.1.json":"b30d01babf36a1b23cfc0892e50ecf8985ddbe48",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-ROOT-CAUSE-CLASSIFICATION-PACKAGE-V0.1.json":"6b65a9a8c0cf547d2dc9916b4bd585e9eb6f085f",
"reports/program/2026-10-08-BEPD-09D-R2-CR1-F1-PERSISTED-HEAD-VERIFICATION-RECEIPT-V0.1.json":"3f5262e764c2976d46dd90d91c91a38e0f5f24c0",
"tools/bepd09d_r2_runtime.py":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
"tools/bepd09c_runtime.py":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
"tools/bepd09c_reference.py":"2c8a82405082ce3f820b580017a96af77e74b0e4",
"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json":"7d950d957611cf209d811c788ff10abded30d011",
"GOVERNANCE/BEPD-09D-R2-CR1-F2-HUMAN-AUTHORIZATION-2026-10-08.json":"ae91e0ad5f47b6268beea165d673a85d8a30e66c",
"GOVERNANCE/BEPD-09D-R2-CR1-F2-PRECISION-LOSS-DIAGNOSTIC-CONTRACT-V0.1.json":"071c95455a452fdf40cda447b1ea38f1b133e0ca",
"GOVERNANCE/BEPD-09D-R2-CR1-F2-FORENSIC-BREAKER-CONTRACT-V0.1.json":"290344292e72203ef32cbe101961394ba992b6c8"
}

def wr(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")

def git_blob(path):
    line=subprocess.check_output(["git","ls-tree","HEAD","--",path],cwd=ROOT,text=True).strip()
    if not line:
        raise RuntimeError("MISSING_TRACKED_PATH:"+path)
    return line.split()[2]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILURE:"+name)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def sig(z):
    z=np.asarray(z,float)
    return np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))

def make_problem(r2,rows,cal):
    rs=r2.validate_rows(rows,cal)
    blocks=r2.partition_calendar(cal)
    train_weeks={w for b in blocks[:3] for w in b}
    train=[x for x in rs if x["target_week_id"] in train_weeks]
    if len(train)!=237:
        raise RuntimeError("WRONG_FOLD3_TRAIN_COUNT")
    stats=r2._stats(train)
    xb,_=r2._mats(train,stats)
    y=np.array([x["y"] for x in train],float)
    if xb.shape!=(237,5):
        raise RuntimeError("WRONG_FOLD3_BASELINE_SHAPE")
    if int(np.sum(y==0))!=51 or int(np.sum(y==1))!=186:
        raise RuntimeError("WRONG_FOLD3_RESPONSE_COUNTS")
    return xb,y

def fun_factory(X,y):
    def fun(b):
        z=X@b
        return float(np.sum(np.logaddexp(0,z)-y*z))
    def jac(b):
        z=X@b
        p=sig(z)
        return X.T@(p-y)
    def hess(b):
        z=X@b
        p=sig(z)
        w=p*(1-p)
        return X.T@(X*w[:,None])
    return fun,jac,hess

def state(X,fun,jac,hess,x,prev=None,index=None):
    x=np.asarray(x,float)
    g=np.asarray(jac(x),float)
    H=np.asarray(hess(x),float)
    ev=np.linalg.eigvalsh((H+H.T)/2)
    z=X@x
    p=sig(z)
    try:
        d=np.linalg.solve(H,-g)
        dnorm=float(np.linalg.norm(d))
        directional=float(g@d)
    except Exception:
        dnorm=float("nan")
        directional=float("nan")
    return {
        "iteration_index":index,
        "parameter_vector_norm":float(np.linalg.norm(x)),
        "objective_value":float(fun(x)),
        "gradient_l2_norm":float(np.linalg.norm(g)),
        "gradient_inf_norm":float(np.max(np.abs(g))),
        "step_norm":None if prev is None else float(np.linalg.norm(x-np.asarray(prev,float))),
        "linear_predictor_min":float(np.min(z)),
        "linear_predictor_max":float(np.max(z)),
        "probability_min":float(np.min(p)),
        "probability_max":float(np.max(p)),
        "hessian_min_eigenvalue":float(np.min(ev)),
        "hessian_max_eigenvalue":float(np.max(ev)),
        "hessian_condition_number":float(np.linalg.cond(H)),
        "newton_direction_norm":dnorm,
        "gradient_dot_newton_direction":directional
    }

def run_newton(X,y,instrument=False):
    fun,jac,hess=fun_factory(X,y)
    trace=[]
    prev=[np.zeros(X.shape[1],float)]
    if instrument:
        trace.append(state(X,fun,jac,hess,prev[0],None,0))
        def callback(xk):
            xcopy=np.array(xk,float,copy=True)
            trace.append(state(X,fun,jac,hess,xcopy,prev[0],len(trace)))
            prev[0]=xcopy
    else:
        callback=None
    res=minimize(
        fun,np.zeros(X.shape[1],float),jac=jac,hess=hess,method="Newton-CG",
        callback=callback,
        options={"xtol":XTOL,"maxiter":MAX_ITER,"disp":False}
    )
    x=np.asarray(res.x,float)
    final={
        "success":bool(res.success),
        "status":int(res.status),
        "message":str(res.message),
        "iteration_count":int(getattr(res,"nit",-1)),
        "function_evaluation_count":int(getattr(res,"nfev",-1)),
        "gradient_evaluation_count":int(getattr(res,"njev",-1)),
        "hessian_evaluation_count":int(getattr(res,"nhev",-1)),
        "x":[float(v) for v in x],
        "objective_value":float(fun(x)),
        "score_inf_norm":float(np.max(np.abs(jac(x))))
    }
    return final,trace,fun,jac,hess

def run_root(jac,hess,n):
    rr=root(jac,np.zeros(n,float),jac=hess,method="hybr",options={"xtol":1e-10,"maxfev":5000})
    x=np.asarray(rr.x,float)
    return {
        "success":bool(rr.success),
        "message":str(rr.message),
        "function_evaluation_count":int(getattr(rr,"nfev",-1)),
        "jacobian_evaluation_count":int(getattr(rr,"njev",-1)),
        "x":[float(v) for v in x],
        "score_inf_norm":float(np.max(np.abs(jac(x)))),
        "finite_solution":bool(np.all(np.isfinite(x)))
    }

def five_point_scalar_gradient(fun,x):
    x=np.asarray(x,float)
    out=np.zeros_like(x)
    for j in range(len(x)):
        h=(EPS**FD_STEP_POWER)*max(1.0,abs(float(x[j])))
        e=np.zeros_like(x); e[j]=h
        out[j]=(-fun(x+2*e)+8*fun(x+e)-8*fun(x-e)+fun(x-2*e))/(12*h)
    return out

def five_point_gradient_jacobian(jac,x):
    x=np.asarray(x,float)
    n=len(x)
    H=np.zeros((n,n),float)
    for j in range(n):
        h=(EPS**FD_STEP_POWER)*max(1.0,abs(float(x[j])))
        e=np.zeros_like(x); e[j]=h
        H[:,j]=(-jac(x+2*e)+8*jac(x+e)-8*jac(x-e)+jac(x-2*e))/(12*h)
    return H

def derivative_check(fun,jac,hess,x,label):
    x=np.asarray(x,float)
    ag=np.asarray(jac(x),float)
    ah=np.asarray(hess(x),float)
    fg=five_point_scalar_gradient(fun,x)
    fh=five_point_gradient_jacobian(jac,x)
    g_abs=float(np.max(np.abs(ag-fg)))
    h_abs=float(np.max(np.abs(ah-fh)))
    g_norm=float(g_abs/max(1.0,float(np.max(np.abs(ag)))))
    h_norm=float(h_abs/max(1.0,float(np.max(np.abs(ah)))))
    return {
        "point":label,
        "gradient_max_abs_error":g_abs,
        "gradient_normalized_error":g_norm,
        "gradient_consistent":bool(g_norm<=GRAD_ERR_THRESHOLD),
        "hessian_max_abs_error":h_abs,
        "hessian_normalized_error":h_norm,
        "hessian_consistent":bool(h_norm<=HESS_ERR_THRESHOLD)
    }

def geometry(hess,x,label):
    H=np.asarray(hess(np.asarray(x,float)),float)
    ev=np.linalg.eigvalsh((H+H.T)/2)
    mx=float(np.max(ev)); mn=float(np.min(ev))
    rel=float(mn/mx) if mx!=0 else 0.0
    return {
        "point":label,
        "min_eigenvalue":mn,
        "max_eigenvalue":mx,
        "condition_number":float(np.linalg.cond(H)),
        "relative_min_to_max_eigenvalue":rel,
        "positive_definite":bool(mn>0),
        "near_singular_by_frozen_rule":bool(abs(rel)<=1e-8),
        "large_condition_number_by_frozen_rule":bool(np.linalg.cond(H)>=1e7)
    }

def stationarity(score):
    if score<=PRACTICAL_STATIONARY:
        return "PRACTICALLY_STATIONARY"
    if score<=NEAR_STATIONARY:
        return "NEAR_STATIONARY"
    return "MATERIALLY_NON_STATIONARY"

def scipy_source_diagnostic():
    src=inspect.getsource(scipy_optimize_internal._minimize_newtoncg)
    compact=re.sub(r"\s+"," ",src)
    warn2_count=len(re.findall(r"warnflag\s*=\s*2",src))
    line_search_to_warn2=bool(re.search(r"except\s+_LineSearchError\s*:[\s\S]{0,500}?warnflag\s*=\s*2",src))
    pr_loss_present=("_status_message['pr_loss']" in src or '_status_message["pr_loss"]' in src)
    return {
        "scipy_version":scipy.__version__,
        "source_sha256":hashlib.sha256(src.encode()).hexdigest(),
        "warnflag_2_assignment_count":warn2_count,
        "line_search_error_branch_sets_warnflag_2":line_search_to_warn2,
        "precision_loss_status_message_present":pr_loss_present,
        "status_2_uniquely_mapped_to_detected_line_search_branch":bool(warn2_count==1 and line_search_to_warn2 and pr_loss_present),
        "source_length":len(src),
        "compact_source_sha256":hashlib.sha256(compact.encode()).hexdigest()
    }

def scale_diag(X):
    X=np.asarray(X,float)
    norms=np.linalg.norm(X,axis=0)
    stds=np.std(X,axis=0,ddof=1)
    ranges=np.max(X,axis=0)-np.min(X,axis=0)
    nonzero_norms=norms[norms>0]
    nonzero_stds=stds[stds>0]
    nonzero_ranges=ranges[ranges>0]
    return {
        "column_norms":[float(v) for v in norms],
        "column_sample_stds":[float(v) for v in stds],
        "column_ranges":[float(v) for v in ranges],
        "column_norm_ratio_max_to_min_nonzero":float(np.max(nonzero_norms)/np.min(nonzero_norms)),
        "column_std_ratio_max_to_min_nonzero":float(np.max(nonzero_stds)/np.min(nonzero_stds)),
        "column_range_ratio_max_to_min_nonzero":float(np.max(nonzero_ranges)/np.min(nonzero_ranges))
    }

try:
    if os.environ.get("GITHUB_REPOSITORY")!="thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM":
        raise RuntimeError("WRONG_REPOSITORY")
    if os.environ.get("GITHUB_REF_NAME")!="integration/system-v1":
        raise RuntimeError("WRONG_BRANCH")
    if not (platform.python_version().startswith("3.12.") and np.__version__=="2.3.5" and scipy.__version__=="1.17.0" and ZoneInfo("America/New_York").key=="America/New_York"):
        raise RuntimeError("WRONG_ENVIRONMENT")

    observed={k:git_blob(k) for k in EXPECTED}
    if observed!=EXPECTED:
        raise RuntimeError("IDENTITY_MISMATCH")

    r2=load("bepd09d_r2_cr1_f2_runtime",R2PATH)
    if r2.MAX_ITER!=5000 or r2.FIT_TOL!=1e-10:
        raise RuntimeError("FROZEN_SOLVER_STATE_MISMATCH")

    raw=LEDGER.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_LEDGER_SHA256:
        raise RuntimeError("WRONG_EVENT_LEDGER")
    rows=[json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]
    cal=[w for b in json.loads(PART.read_text(encoding="utf-8"))["blocks"] for w in b["weeks"]]

    X,y=make_problem(r2,rows,cal)
    problem_identity=hashlib.sha256(X.tobytes(order="C")+y.tobytes(order="C")).hexdigest()

    u1,_,fun,jac,hess=run_newton(X,y,False)
    u2,_,_,_,_=run_newton(X,y,False)
    inst,trace,_,_,_=run_newton(X,y,True)

    def message_class(m):
        return "PRECISION_LOSS" if "precision loss" in m.lower() else "OTHER"

    replay={
        "run_1":u1,"run_2":u2,"instrumented_run":inst,
        "message_class_run_1":message_class(u1["message"]),
        "message_class_run_2":message_class(u2["message"]),
        "message_class_instrumented":message_class(inst["message"]),
        "run1_run2_vector_max_abs_diff":float(np.max(np.abs(np.array(u1["x"])-np.array(u2["x"])))),
        "run1_instrumented_vector_max_abs_diff":float(np.max(np.abs(np.array(u1["x"])-np.array(inst["x"])))),
        "run1_run2_objective_abs_diff":abs(u1["objective_value"]-u2["objective_value"]),
        "run1_instrumented_objective_abs_diff":abs(u1["objective_value"]-inst["objective_value"]),
        "run1_run2_score_abs_diff":abs(u1["score_inf_norm"]-u2["score_inf_norm"]),
        "run1_instrumented_score_abs_diff":abs(u1["score_inf_norm"]-inst["score_inf_norm"])
    }
    replay_pass=(
        u1["status"]==2 and u2["status"]==2 and inst["status"]==2 and
        message_class(u1["message"])=="PRECISION_LOSS" and
        message_class(u2["message"])=="PRECISION_LOSS" and
        message_class(inst["message"])=="PRECISION_LOSS" and
        u1["iteration_count"]==u2["iteration_count"]==inst["iteration_count"] and
        replay["run1_run2_vector_max_abs_diff"]<=VECTOR_REPLAY_ATOL and
        replay["run1_instrumented_vector_max_abs_diff"]<=VECTOR_REPLAY_ATOL and
        replay["run1_run2_objective_abs_diff"]<=OBJECTIVE_REPLAY_ATOL and
        replay["run1_instrumented_objective_abs_diff"]<=OBJECTIVE_REPLAY_ATOL and
        replay["run1_run2_score_abs_diff"]<=SCORE_REPLAY_ATOL and
        replay["run1_instrumented_score_abs_diff"]<=SCORE_REPLAY_ATOL
    )
    if not replay_pass:
        raise RuntimeError("NONREPRODUCIBLE_PRECISION_LOSS_OR_CALLBACK_INTERFERENCE")

    rootdiag=run_root(jac,hess,X.shape[1])
    if not (rootdiag["success"] and rootdiag["finite_solution"]):
        raise RuntimeError("REFERENCE_STATIONARITY_DIAGNOSTIC_FAILED")

    x0=np.zeros(X.shape[1],float)
    xn=np.array(u1["x"],float)
    xr=np.array(rootdiag["x"],float)

    deriv=[
        derivative_check(fun,jac,hess,x0,"ZERO_INITIALIZATION"),
        derivative_check(fun,jac,hess,xn,"NEWTON_CG_FINAL"),
        derivative_check(fun,jac,hess,xr,"ROOT_HYBR_SOLUTION")
    ]
    gradient_consistent=all(d["gradient_consistent"] for d in deriv)
    hessian_consistent=all(d["hessian_consistent"] for d in deriv)

    newton_score=u1["score_inf_norm"]
    root_score=rootdiag["score_inf_norm"]
    newton_obj=u1["objective_value"]
    root_obj=float(fun(xr))
    obj_abs=abs(newton_obj-root_obj)
    obj_rel=obj_abs/max(1.0,abs(root_obj))
    param_max=float(np.max(np.abs(xn-xr)))
    param_l2=float(np.linalg.norm(xn-xr))

    geom_newton=geometry(hess,xn,"NEWTON_CG_FINAL")
    geom_root=geometry(hess,xr,"ROOT_HYBR_SOLUTION")
    scales=scale_diag(X)

    srcdiag=scipy_source_diagnostic()

    objective_roundoff_scale=EPS*max(1.0,abs(newton_obj))
    machine={
        "float64_epsilon":float(EPS),
        "objective_roundoff_scale_eps_times_objective":float(objective_roundoff_scale),
        "newton_final_score_inf_norm":float(newton_score),
        "root_score_inf_norm":float(root_score),
        "newton_score_to_float64_epsilon_ratio":float(newton_score/EPS),
        "newton_score_to_objective_roundoff_scale_ratio":float(newton_score/objective_roundoff_scale),
        "newton_objective_to_root_objective_abs_gap":float(obj_abs),
        "newton_objective_to_root_objective_relative_gap":float(obj_rel)
    }

    hypotheses={
        "PL-A_DERIVATIVE_IMPLEMENTATION_DEFECT":"RULED_OUT" if gradient_consistent and hessian_consistent else "CONSISTENT_WITH",
        "PL-B_ILL_CONDITIONED_CURVATURE_NUMERICAL_GEOMETRY":"OBSERVED" if (geom_newton["large_condition_number_by_frozen_rule"] or geom_newton["near_singular_by_frozen_rule"]) else "CONSISTENT_WITH",
        "PL-C_FLOAT64_TERMINATION_ROUNDOFF_LIMITATION":"CONSISTENT_WITH",
        "PL-D_SCIPY_NEWTON_CG_TERMINATION_CRITERION_INTERACTION":"PROVEN" if (
            srcdiag["status_2_uniquely_mapped_to_detected_line_search_branch"] and
            stationarity(newton_score) in ("PRACTICALLY_STATIONARY","NEAR_STATIONARY") and
            rootdiag["success"] and gradient_consistent and hessian_consistent
        ) else "NOT_PROVEN",
        "PL-E_OBJECTIVE_GRADIENT_INCONSISTENCY":"RULED_OUT" if gradient_consistent else "NOT_PROVEN"
    }

    if hypotheses["PL-D_SCIPY_NEWTON_CG_TERMINATION_CRITERION_INTERACTION"]=="PROVEN":
        mechanism="PL-D"
        mechanism_label="SCIPY_NEWTON_CG_LINE_SEARCH_TERMINATION_INTERACTION_NEAR_STATIONARY_POINT"
        evidence_grade="PROVEN"
        root_cause="PROVEN"
        repair_class="R2"
        repair_feasibility="POTENTIALLY_ADMISSIBLE"
    else:
        mechanism="PL-G"
        mechanism_label="PRECISION_LOSS_MECHANISM_NOT_PROVEN"
        evidence_grade="NOT_PROVEN"
        root_cause="NOT_PROVEN"
        repair_class="NOT_DETERMINED"
        repair_feasibility="NOT_DETERMINED"

    wr("05_REPRODUCIBILITY_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_REPRODUCIBILITY_RECEIPT_V0_1",
        "status":"PASS",
        "problem_identity_sha256":problem_identity,
        "replay":replay,
        "frozen_tolerances":{
            "vector_max_abs":VECTOR_REPLAY_ATOL,
            "objective_abs":OBJECTIVE_REPLAY_ATOL,
            "score_inf_abs":SCORE_REPLAY_ATOL
        },
        "callback_non_interference":"PASS"
    })
    wr("06_NEWTON_CG_TRACE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_NEWTON_CG_TRACE_RECEIPT_V0_1",
        "status":"PASS",
        "fold":3,"model":"BASELINE",
        "solver":"Newton-CG","max_iter":5000,"xtol":1e-10,
        "instrumented_termination":inst,
        "trace":trace,
        "instrumentation":"OBSERVATIONAL_ONLY"
    })
    wr("07_DERIVATIVE_CONSISTENCY_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_DERIVATIVE_CONSISTENCY_RECEIPT_V0_1",
        "status":"PASS",
        "method":{
            "gradient":"FIVE_POINT_CENTRAL_FINITE_DIFFERENCE_OF_OBJECTIVE",
            "hessian":"FIVE_POINT_CENTRAL_FINITE_DIFFERENCE_OF_ANALYTIC_GRADIENT",
            "step_rule":"EPSILON_POW_1_5_TIMES_MAX_1_ABS_XJ",
            "gradient_normalized_error_threshold":GRAD_ERR_THRESHOLD,
            "hessian_normalized_error_threshold":HESS_ERR_THRESHOLD
        },
        "checks":deriv,
        "gradient_implementation_consistent":"YES" if gradient_consistent else "NO",
        "hessian_implementation_consistent":"YES" if hessian_consistent else "NO"
    })
    wr("08_STATIONARITY_OBJECTIVE_GAP_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_STATIONARITY_OBJECTIVE_GAP_RECEIPT_V0_1",
        "status":"PASS",
        "stationarity_thresholds":{
            "practically_stationary_lte":PRACTICAL_STATIONARY,
            "near_stationary_lte":NEAR_STATIONARY
        },
        "newton_cg_final_score_inf_norm":newton_score,
        "newton_cg_stationarity_class":stationarity(newton_score),
        "root_hybr_score_inf_norm":root_score,
        "root_hybr_success":rootdiag["success"],
        "objective_newton_cg":newton_obj,
        "objective_root_hybr":root_obj,
        "objective_abs_difference":obj_abs,
        "objective_relative_difference":obj_rel,
        "parameter_max_abs_difference":param_max,
        "parameter_l2_difference":param_l2
    })
    wr("09_HESSIAN_GEOMETRY_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_HESSIAN_GEOMETRY_RECEIPT_V0_1",
        "status":"PASS",
        "newton_cg_final":geom_newton,
        "root_hybr_solution":geom_root
    })
    wr("10_SCALE_MACHINE_PRECISION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_SCALE_MACHINE_PRECISION_RECEIPT_V0_1",
        "status":"PASS",
        "scale":scales,
        "machine_precision":machine,
        "scipy_newton_cg_source_diagnostic":srcdiag
    })
    wr("11_ROOT_CAUSE_CLASSIFICATION_PACKAGE.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_ROOT_CAUSE_CLASSIFICATION_PACKAGE_V0_1",
        "status":"QUALIFIED_FOR_HUMAN_ADJUDICATION",
        "precision_loss_mechanism":mechanism,
        "precision_loss_mechanism_label":mechanism_label,
        "evidence_grade":evidence_grade,
        "root_cause":root_cause,
        "hypothesis_grades":hypotheses,
        "candidate_repair_class":repair_class,
        "repair_feasibility":repair_feasibility,
        "repair_authority":"NONE",
        "scientific_result":"NONE",
        "c1_retry_authorized":False
    })
    wr("12_FORENSIC_QUALIFICATION_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_FORENSIC_QUALIFICATION_RECEIPT_V0_1",
        "status":"PASS",
        "verdict":"FORENSICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION",
        "precision_loss_mechanism":mechanism,
        "precision_loss_mechanism_label":mechanism_label,
        "evidence_grade":evidence_grade,
        "root_cause":root_cause,
        "candidate_repair_class":repair_class,
        "repair_feasibility":repair_feasibility,
        "repair_authority":"NONE",
        "bepd_09d_r2_pre_retry_ready":"NO_AUTOMATIC_PROMOTION",
        "test_predictions_computed":False,
        "test_scoring_computed":False,
        "logloss_computed":False,
        "brier_computed":False,
        "scientific_result":"NONE",
        "c1_retry_authorized":False,
        "fresh_oos":"CLOSED",
        "trading_authority":"NONE",
        "next":"HUMAN_ADJUDICATION_OF_BEPD_09D_R2_CR1_F2",
        "stop":True
    })
    print("BEPD-09D-R2-CR1-F2 FORENSIC QUALIFICATION COMPLETED; STOP FOR HUMAN ADJUDICATION")
except Exception as exc:
    wr("99_F2_FAILURE_RECEIPT.json",{
        "schema":"ATDS_BEPD_09D_R2_CR1_F2_FAILURE_RECEIPT_V0_1",
        "status":"BLOCKED_FAIL_CLOSED",
        "error_type":type(exc).__name__,
        "error":str(exc),
        "traceback":traceback.format_exc(),
        "repair_applied":False,
        "rerun_performed":False,
        "c1_retry_authorized":False,
        "scientific_result":"NONE",
        "trading_authority":"NONE",
        "stop":True
    })
    raise
