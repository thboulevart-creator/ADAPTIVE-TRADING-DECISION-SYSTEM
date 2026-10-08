from __future__ import annotations
import json, math
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.optimize import minimize as scipy_minimize

import bepd09c_runtime as base
import bepd09d_r2_runtime as legacy
import bepd09d_r2_rd2_candidate_b_contract as contract

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-rd3-red"
OUT.mkdir(parents=True,exist_ok=True)

X=np.array([[1.0,-1.0],[1.0,0.0],[1.0,1.0],[1.0,2.0]],float)
y=np.array([0.0,1.0,0.0,1.0],float)

def sigmoid(z):
    return np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))

def fun(b):
    z=X@b
    return float(np.sum(np.logaddexp(0,z)-y*z))

def jac(b):
    p=sigmoid(X@b)
    return X.T@(p-y)

def hess(b):
    p=sigmoid(X@b)
    w=p*(1-p)
    return X.T@(X*w[:,None])

opt=scipy_minimize(
    fun,np.zeros(X.shape[1]),jac=jac,hess=hess,method="Newton-CG",
    options={"xtol":1e-12,"maxiter":5000,"disp":False}
)
if not np.all(np.isfinite(opt.x)):
    raise RuntimeError("SYNTHETIC_OPTIMUM_NONFINITE")

bindings=dict(contract.EXPECTED_BINDINGS)

def packet(x,success,status,message):
    score=float(np.max(np.abs(jac(np.asarray(x,float)))))
    return {
        "X":X.tolist(),
        "parameters":np.asarray(x,float).tolist(),
        "objective":fun(np.asarray(x,float)),
        "score_inf_norm":score,
        "derivatives_finite":bool(np.all(np.isfinite(jac(x))) and np.all(np.isfinite(hess(x)))),
        "full_required_design_rank":bool(np.linalg.matrix_rank(X)==X.shape[1]),
        "perfect_separation":False,
        "one_class_sample":False,
        "solver":contract.EXPECTED_SOLVER,
        "model_id":contract.EXPECTED_MODEL_ID,
        "feature_contract_id":contract.EXPECTED_FEATURE_CONTRACT_ID,
        "bindings":bindings,
        "tau_contract_blob":contract.TAU_DERIVATION_CONTRACT_BLOB,
        "optimizer_success":success,
        "optimizer_status":status,
        "optimizer_message":message,
        "registered_state":True,
        "reference_metadata":{"role":"DIAGNOSTIC_ONLY"}
    }

def run_legacy_with_fake(fake):
    original=base.minimize
    try:
        base.minimize=lambda *a,**k: fake
        try:
            out=legacy.fit_logistic(X,y,max_iter=5000,tol=1e-10)
            return {"kind":"RETURN","parameters":np.asarray(out,float).tolist()}
        except Exception as exc:
            return {"kind":"RAISE","type":type(exc).__name__,"message":str(exc)}
    finally:
        base.minimize=original

case1_packet=packet(opt.x,False,2,"SYNTHETIC_PRECISION_LOSS")
case1_contract=contract.evaluate(case1_packet)
if case1_contract["verdict"]!="ACCEPT":
    raise RuntimeError("RED_FIXTURE_1_NOT_VALID_UNDER_ADOPTED_CONTRACT")
legacy1=run_legacy_with_fake(SimpleNamespace(success=False,x=np.asarray(opt.x,float)))
red1=(legacy1["kind"]=="RAISE" and legacy1["message"]=="MODEL_NONCONVERGENCE")

zero=np.zeros(X.shape[1],float)
case2_packet=packet(zero,True,0,"SYNTHETIC_SUCCESS")
case2_contract=contract.evaluate(case2_packet)
if case2_contract["verdict"]!="REJECT":
    raise RuntimeError("RED_FIXTURE_2_NOT_INVALID_UNDER_ADOPTED_CONTRACT")
legacy2=run_legacy_with_fake(SimpleNamespace(success=True,x=zero))
red2=(legacy2["kind"]=="RETURN")

receipt={
    "schema":"ATDS_BEPD_09D_R2_RD3_RED_TEST_RECEIPT_V0_1",
    "status":"PASS" if red1 and red2 else "FAIL",
    "surface":"CURRENT_R2_RUNTIME_SYNTHETIC_ONLY",
    "current_runtime_blob":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
    "source_runtime_blob":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
    "candidate_contract_blob":"0e87aa62433218b44f8ddaf64351ed0beccd93a3",
    "cases":[
      {
        "name":"LEGACY_REJECTS_MATHEMATICALLY_VALID_SUCCESS_FALSE",
        "candidate_b_expected":"ACCEPT",
        "candidate_b_observed":case1_contract["verdict"],
        "legacy_observed":legacy1,
        "red_demonstrated":red1,
        "score_inf_norm":case1_packet["score_inf_norm"],
        "tau_score":case1_contract["tau_score"]
      },
      {
        "name":"LEGACY_ACCEPTS_SUCCESS_TRUE_THAT_FAILS_MATHEMATICAL_CONTRACT",
        "candidate_b_expected":"REJECT",
        "candidate_b_observed":case2_contract["verdict"],
        "legacy_observed":legacy2,
        "red_demonstrated":red2,
        "score_inf_norm":case2_packet["score_inf_norm"],
        "tau_score":case2_contract["tau_score"]
      }
    ],
    "real_data_used":False,
    "fold3_replay":False,
    "implementation_present":False,
    "stop_after_red":True
}
if receipt["status"]!="PASS":
    raise RuntimeError("RED_TEST_DID_NOT_DEMONSTRATE_REQUIRED_LEGACY_MISMATCH")
(OUT/"05_RED_TEST_RECEIPT.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps({"red":"PASS","case1":legacy1["kind"],"case2":legacy2["kind"]},sort_keys=True))
