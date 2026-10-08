from __future__ import annotations

import copy, hashlib, json, math, subprocess
from pathlib import Path
from types import SimpleNamespace

import numpy as np
from scipy.optimize import linprog

import bepd09d_r2_runtime as legacy
import bepd09c_runtime as source
import bepd09d_r2_rd2_candidate_b_contract as adopted
import bepd09d_r2_rd3_candidate_b_runtime as controlled

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-rd3-green"
OUT.mkdir(parents=True,exist_ok=True)

EXPECTED_BLOBS={
    "tools/bepd09c_runtime.py":"72645c3201d3d454d4d5402a0e2191e1195c68a6",
    "tools/bepd09d_r2_runtime.py":"209b3b5b804da4da9ee6751f2a15a32df0e3e4b1",
    "tools/bepd09c_reference.py":"2c8a82405082ce3f820b580017a96af77e74b0e4",
    "tools/bepd09d_r2_rd2_candidate_b_contract.py":"0e87aa62433218b44f8ddaf64351ed0beccd93a3",
}
def git_blob(path):
    line=subprocess.check_output(["git","ls-tree","HEAD","--",path],cwd=ROOT,text=True).strip()
    if not line: raise RuntimeError("MISSING_TRACKED_PATH:"+path)
    return line.split()[2]
observed_blobs={p:git_blob(p) for p in EXPECTED_BLOBS}
if observed_blobs!=EXPECTED_BLOBS:
    raise RuntimeError("LEGACY_OR_CONTRACT_BLOB_DRIFT")

if controlled.REAL_EXECUTION_PATH_ACTIVATION is not False:
    raise RuntimeError("REAL_EXECUTION_PATH_ACTIVATED")
if callable(getattr(controlled,"run_protocol",None)):
    raise RuntimeError("CONTROLLED_RUNTIME_EXPOSES_ACTIVE_RUN_PROTOCOL")
if controlled.SOLVER!="Newton-CG" or controlled.MAX_ITER!=5000 or controlled.XTOL!=1e-10 or controlled.INITIALIZATION!="ZERO_VECTOR":
    raise RuntimeError("FROZEN_NUMERICS_DRIFT")

def wr(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")

X=[[1.0,-1.0],[1.0,0.0],[1.0,1.0],[1.0,2.0]]
y=[0.0,1.0,0.0,1.0]
tau=adopted.tau_score(X)
below=math.nextafter(tau,0.0)
above=math.nextafter(tau,math.inf)

base_packet={
    "X":copy.deepcopy(X),
    "parameters":[0.1,-0.2],
    "objective":2.0,
    "score_inf_norm":0.5*tau,
    "derivatives_finite":True,
    "full_required_design_rank":True,
    "perfect_separation":False,
    "one_class_sample":False,
    "solver":adopted.EXPECTED_SOLVER,
    "model_id":adopted.EXPECTED_MODEL_ID,
    "feature_contract_id":adopted.EXPECTED_FEATURE_CONTRACT_ID,
    "bindings":copy.deepcopy(adopted.EXPECTED_BINDINGS),
    "tau_contract_blob":adopted.TAU_DERIVATION_CONTRACT_BLOB,
    "optimizer_success":True,
    "optimizer_status":0,
    "optimizer_message":"SYNTHETIC",
    "registered_state":True,
    "reference_metadata":{"role":"DIAGNOSTIC_ONLY","variant":"A"},
}
def packet(**changes):
    p=copy.deepcopy(base_packet)
    p.update(changes)
    return p

cases=[
 ("VALID_STATIONARY_FIT",packet(),"ACCEPT"),
 ("SUCCESS_TRUE_CONTRACT_PASS",packet(optimizer_success=True),"ACCEPT"),
 ("SUCCESS_FALSE_CONTRACT_PASS",packet(optimizer_success=False,optimizer_status=2,optimizer_message="PRECISION_LOSS"),"ACCEPT"),
 ("SUCCESS_TRUE_SCORE_ABOVE_TAU",packet(optimizer_success=True,score_inf_norm=2*tau),"REJECT"),
 ("SUCCESS_FALSE_SCORE_ABOVE_TAU",packet(optimizer_success=False,score_inf_norm=2*tau),"REJECT"),
 ("NONFINITE_INPUT",packet(X=[[1.0,float("nan")]]),"REJECT"),
 ("NONFINITE_PARAMETERS",packet(parameters=[float("nan"),0.0]),"REJECT"),
 ("NONFINITE_OBJECTIVE",packet(objective=float("inf")),"REJECT"),
 ("NONFINITE_SCORE",packet(score_inf_norm=float("inf")),"REJECT"),
 ("NONFINITE_DERIVATIVES",packet(derivatives_finite=False),"REJECT"),
 ("RANK_DEFICIENCY",packet(full_required_design_rank=False),"REJECT"),
 ("PERFECT_SEPARATION",packet(perfect_separation=True),"REJECT"),
 ("ONE_CLASS",packet(one_class_sample=True),"REJECT"),
 ("SCORE_JUST_BELOW_TAU",packet(score_inf_norm=below),"ACCEPT"),
 ("SCORE_EXACTLY_AT_TAU",packet(score_inf_norm=tau),"ACCEPT"),
 ("SCORE_JUST_ABOVE_TAU",packet(score_inf_norm=above),"REJECT"),
 ("TAU_IDENTITY_FAILURE",packet(tau_contract_blob="WRONG"),"REJECT"),
 ("MISSING_TAU_IDENTITY",packet(tau_contract_blob=None),"REJECT"),
 ("UNKNOWN_STATE",packet(registered_state=False),"FAIL_CLOSED"),
 ("UNEXPECTED_SOLVER",packet(solver="OTHER"),"REJECT"),
 ("UNEXPECTED_MODEL",packet(model_id="OTHER"),"REJECT"),
 ("UNEXPECTED_FEATURE_SET",packet(feature_contract_id="OTHER"),"REJECT"),
 ("UNEXPECTED_DATA_BINDING",packet(bindings={}),"REJECT"),
]

green=[]
parity=[]
breaker_names={
 "NONFINITE_INPUT":"FINITE_INPUT",
 "NONFINITE_PARAMETERS":"FINITE_PARAMETERS",
 "NONFINITE_OBJECTIVE":"FINITE_OBJECTIVE",
 "NONFINITE_SCORE":"FINITE_SCORE",
 "NONFINITE_DERIVATIVES":"FINITE_DERIVATIVES",
 "RANK_DEFICIENCY":"FULL_REQUIRED_DESIGN_RANK",
 "PERFECT_SEPARATION":"NO_PERFECT_SEPARATION",
 "ONE_CLASS":"NOT_ONE_CLASS",
 "SUCCESS_TRUE_SCORE_ABOVE_TAU":"SCORE_INF_NORM_LTE_TAU_SCORE",
 "MISSING_TAU_IDENTITY":"EXPECTED_TAU_DERIVATION_CONTRACT",
 "TAU_IDENTITY_FAILURE":"EXPECTED_TAU_DERIVATION_CONTRACT",
 "UNEXPECTED_SOLVER":"EXPECTED_SOLVER",
 "UNEXPECTED_MODEL":"EXPECTED_MODEL",
 "UNEXPECTED_FEATURE_SET":"EXPECTED_FEATURE_SET",
 "UNEXPECTED_DATA_BINDING":"EXPECTED_DATA_BINDING",
}
breaker_results=[]
for name,p,want in cases:
    got=controlled.evaluate_fit_state(p)
    ref=adopted.evaluate(p)
    same=(got==ref)
    green.append({
        "name":name,"expected":want,"observed":got["verdict"],
        "receipt_identity":got["receipt_identity"],
        "status":"PASS" if got["verdict"]==want else "FAIL"
    })
    parity.append({
        "name":name,
        "same_tau_score":got["tau_score"]==ref["tau_score"],
        "same_gates":got["gates"]==ref["gates"],
        "same_verdict":got["verdict"]==ref["verdict"],
        "exact_receipt_parity":same,
        "status":"PASS" if same else "FAIL"
    })
    if name in breaker_names:
        gate=breaker_names[name]
        breaker_results.append({
            "name":name,"gate":gate,
            "gate_observed":got["gates"][gate],
            "verdict":got["verdict"],
            "status":"PASS" if got["gates"][gate] is False and got["verdict"]!="ACCEPT" else "FAIL"
        })
    if name=="UNKNOWN_STATE":
        breaker_results.append({
            "name":"UNKNOWN_STATE","gate":"REGISTERED_STATE",
            "gate_observed":False,"verdict":got["verdict"],
            "status":"PASS" if got["verdict"]=="FAIL_CLOSED" else "FAIL"
        })

if any(x["status"]!="PASS" for x in green):
    raise RuntimeError("GREEN_REGRESSION_FAILURE")
if any(x["status"]!="PASS" for x in parity):
    raise RuntimeError("CONTRACT_PARITY_FAILURE")
if any(x["status"]!="PASS" for x in breaker_results):
    raise RuntimeError("BREAKER_REGRESSION_FAILURE")

# Actual controlled Newton-CG fit on synthetic data only.
actual1=controlled.fit_logistic_candidate_b(np.asarray(X,float),np.asarray(y,float))
actual2=controlled.fit_logistic_candidate_b(np.asarray(X,float),np.asarray(y,float))
if actual1["final_acceptance_verdict"]!="ACCEPT" or actual2["final_acceptance_verdict"]!="ACCEPT":
    raise RuntimeError("ACTUAL_SYNTHETIC_CONTROLLED_FIT_NOT_ACCEPTED")
if actual1["receipt_identity"]!=actual2["receipt_identity"]:
    raise RuntimeError("ACTUAL_SYNTHETIC_FIT_NONDETERMINISTIC")
if actual1["parameters"]!=actual2["parameters"]:
    raise RuntimeError("ACTUAL_SYNTHETIC_PARAMETERS_NONDETERMINISTIC")

def full_replay():
    return [
        {
          "name":name,
          "receipt":controlled.evaluate_fit_state(p)["receipt_identity"],
          "verdict":controlled.evaluate_fit_state(p)["verdict"],
          "tau":controlled.evaluate_fit_state(p)["tau_score"]
        }
        for name,p,_ in cases
    ] + [{
        "name":"ACTUAL_CONTROLLED_NEWTON_CG_SYNTHETIC_FIT",
        "receipt":controlled.fit_logistic_candidate_b(np.asarray(X,float),np.asarray(y,float))["receipt_identity"],
        "verdict":controlled.fit_logistic_candidate_b(np.asarray(X,float),np.asarray(y,float))["final_acceptance_verdict"],
        "tau":controlled.fit_logistic_candidate_b(np.asarray(X,float),np.asarray(y,float))["tau_score"],
    }]
r1=full_replay()
r2=full_replay()
if r1!=r2:
    raise RuntimeError("FULL_SYNTHETIC_REPLAY_NONDETERMINISTIC")

# Legacy non-regression: helper identity plus numerical formula checks.
alias_checks={
 "validate_rows":controlled.validate_rows is legacy.validate_rows,
 "validate_fold_integrity":controlled.validate_fold_integrity is legacy.validate_fold_integrity,
 "partition_calendar":controlled.partition_calendar is legacy.partition_calendar,
 "exposure_values":controlled.exposure_values is legacy.exposure_values,
 "spline_basis":controlled.spline_basis is legacy.spline_basis,
 "_stats":controlled._stats is legacy._stats,
 "_mats":controlled._mats is legacy._mats,
 "_sig":controlled._sig is source._sig,
 "_score":controlled._score is source._score,
}
if not all(alias_checks.values()):
    raise RuntimeError("LEGACY_HELPER_IDENTITY_DRIFT")

Xa=np.asarray(X,float); ya=np.asarray(y,float); b=np.array([0.2,-0.1])
objective_parity=abs(controlled.objective(Xa,ya,b) - (-source._ll(Xa,ya,b))) <= 1e-12

h=1e-6
fdg=np.zeros_like(b)
for j in range(len(b)):
    e=np.zeros_like(b); e[j]=h
    fdg[j]=((-source._ll(Xa,ya,b+e))-(-source._ll(Xa,ya,b-e)))/(2*h)
gradient_parity=bool(np.max(np.abs(fdg-controlled.gradient(Xa,ya,b)))<=1e-7)

fdH=np.zeros((len(b),len(b)))
for j in range(len(b)):
    e=np.zeros_like(b); e[j]=h
    fdH[:,j]=(controlled.gradient(Xa,ya,b+e)-controlled.gradient(Xa,ya,b-e))/(2*h)
hessian_parity=bool(np.max(np.abs(fdH-controlled.hessian(Xa,ya,b)))<=1e-7)

signs=np.where(ya>0.5,1.0,-1.0)
sep_ref=linprog(np.zeros(Xa.shape[1]),A_ub=-(signs[:,None]*Xa),b_ub=-np.ones(len(ya)),bounds=[(None,None)]*Xa.shape[1],method="highs")
separation_parity=(controlled.perfect_separation(Xa,ya)==bool(sep_ref.success))

legacy_nonreg=(
    all(alias_checks.values()) and objective_parity and gradient_parity and hessian_parity and
    separation_parity and observed_blobs==EXPECTED_BLOBS and controlled.run_protocol is None
)
if not legacy_nonreg:
    raise RuntimeError("LEGACY_NON_REGRESSION_FAILURE")

# Reference role invariance.
pa=packet(reference_metadata={"role":"DIAGNOSTIC_ONLY","success":True,"score":0.0})
pb=packet(reference_metadata={"role":"DIAGNOSTIC_ONLY","success":False,"score":"UNAVAILABLE"})
ra=controlled.evaluate_fit_state(pa)
rb=controlled.evaluate_fit_state(pb)
reference_role_pass=(
    ra["verdict"]==rb["verdict"]=="ACCEPT" and
    ra["gates"]==rb["gates"] and
    ra["tau_score"]==rb["tau_score"] and
    ra["receipt_identity"]!=rb["receipt_identity"]
)
if not reference_role_pass:
    raise RuntimeError("REFERENCE_ROLE_INVARIANCE_FAILURE")

wr("07_GREEN_SYNTHETIC_REGRESSION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_GREEN_SYNTHETIC_REGRESSION_RECEIPT_V0_1",
    "status":"PASS",
    "registered_case_count":len(green),
    "registered_cases":green,
    "actual_controlled_newton_cg_synthetic_fit":{
        "verdict":actual1["final_acceptance_verdict"],
        "optimizer_success":actual1["optimizer_success"],
        "optimizer_status":actual1["optimizer_status"],
        "optimizer_message":actual1["optimizer_message"],
        "score_inf_norm":actual1["score_inf_norm"],
        "score_scale":actual1["score_scale"],
        "tau_relative":actual1["tau_relative"],
        "tau_score":actual1["tau_score"],
        "receipt_identity":actual1["receipt_identity"]
    },
    "real_data_used":False,
    "fold3_replay":False
})
wr("08_CONTRACT_PARITY_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_CONTRACT_PARITY_RECEIPT_V0_1",
    "status":"PASS",
    "candidate_b_adopted_contract_blob":"0e87aa62433218b44f8ddaf64351ed0beccd93a3",
    "fixture_count":len(parity),
    "fixtures":parity,
    "all_exact_receipt_parity":True
})
wr("09_BREAKER_REGRESSION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_BREAKER_REGRESSION_RECEIPT_V0_1",
    "status":"PASS",
    "breaker_case_count":len(breaker_results),
    "breakers":breaker_results,
    "all_fail_closed":True
})
replay_hash=hashlib.sha256(json.dumps(r1,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
wr("10_DETERMINISM_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_DETERMINISM_RECEIPT_V0_1",
    "status":"PASS",
    "replay_1_identity":replay_hash,
    "replay_2_identity":replay_hash,
    "same_tau_score":True,
    "same_diagnostics":True,
    "same_individual_gates":True,
    "same_final_verdict":True,
    "same_receipt_identity":True,
    "actual_fit_parameters_exact_replay":True
})
wr("11_LEGACY_NON_REGRESSION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_LEGACY_NON_REGRESSION_RECEIPT_V0_1",
    "status":"PASS",
    "observed_frozen_blobs":observed_blobs,
    "alias_identity_checks":alias_checks,
    "objective_parity":objective_parity,
    "gradient_parity":gradient_parity,
    "hessian_parity":hessian_parity,
    "separation_detector_parity":separation_parity,
    "reference_role_not_activated":controlled.run_protocol is None,
    "only_functional_delta":"FIT_ACCEPTANCE_SEMANTICS",
    "real_data_used":False
})
wr("12_REFERENCE_ROLE_INVARIANCE_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_REFERENCE_ROLE_INVARIANCE_RECEIPT_V0_1",
    "status":"PASS",
    "role":"INDEPENDENT_NUMERICAL_CONSISTENCY_CHECK_ONLY_NOT_FALLBACK_NOT_RESULT_PRODUCER",
    "acceptance_gates_identical":ra["gates"]==rb["gates"],
    "tau_score_identical":ra["tau_score"]==rb["tau_score"],
    "verdict_identical":ra["verdict"]==rb["verdict"],
    "audit_identity_changes_with_reference_metadata":ra["receipt_identity"]!=rb["receipt_identity"],
    "real_reference_fit_executed":False
})
wr("13_IMPLEMENTATION_QUALIFICATION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD3_IMPLEMENTATION_QUALIFICATION_RECEIPT_V0_1",
    "status":"PASS",
    "verdict":"CANDIDATE_B_IMPLEMENTATION_SYNTHETICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION",
    "controlled_runtime_activation":False,
    "green_synthetic_regression":"PASS",
    "contract_parity":"PASS",
    "breaker_regression":"PASS",
    "determinism":"PASS",
    "legacy_non_regression":"PASS",
    "reference_role_invariance":"PASS",
    "real_data_model_execution":False,
    "real_training_fit":False,
    "real_fold3_replay":False,
    "real_reference_fit":False,
    "real_training_requalification":False,
    "c1_retry":False,
    "scientific_result":"NONE",
    "fresh_oos":"CLOSED",
    "trading_authority":"NONE",
    "next":"HUMAN_ADJUDICATION_OF_CANDIDATE_B_CONTROLLED_IMPLEMENTATION",
    "stop":True
})
print(json.dumps({
    "green":"PASS","cases":len(green),
    "actual_fit":actual1["final_acceptance_verdict"],
    "parity":"PASS","breakers":"PASS","determinism":"PASS",
    "legacy_non_regression":"PASS","reference_role":"PASS",
    "verdict":"CANDIDATE_B_IMPLEMENTATION_SYNTHETICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION"
},sort_keys=True))
