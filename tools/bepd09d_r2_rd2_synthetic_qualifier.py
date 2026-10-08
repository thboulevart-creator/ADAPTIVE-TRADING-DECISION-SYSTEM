from __future__ import annotations
import copy, hashlib, importlib.util, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-rd2-candidate-b"
OUT.mkdir(parents=True,exist_ok=True)

CONTRACT_PATH=ROOT/"tools/bepd09d_r2_rd2_candidate_b_contract.py"
TAU_PATH=ROOT/"GOVERNANCE/BEPD-09D-R2-RD2-TAU-SCORE-DERIVATION-CONTRACT-V0.1.json"
ACCEPT_PATH=ROOT/"GOVERNANCE/BEPD-09D-R2-RD2-NUMERICAL-ACCEPTANCE-CONTRACT-V0.1.json"
PLAN_PATH=ROOT/"GOVERNANCE/BEPD-09D-R2-RD2-SYNTHETIC-TEST-PLAN-V0.1.json"

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILURE")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def wr(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()

c=load_module("candidate_b",CONTRACT_PATH)
tau_contract=json.loads(TAU_PATH.read_text(encoding="utf-8"))
accept_contract=json.loads(ACCEPT_PATH.read_text(encoding="utf-8"))
plan=json.loads(PLAN_PATH.read_text(encoding="utf-8"))

if tau_contract["numeric_basis"]["epsilon"] != c.FLOAT64_EPSILON:
    raise RuntimeError("EPSILON_MISMATCH")
if tau_contract["numeric_basis"]["tau_relative"] != c.TAU_RELATIVE:
    raise RuntimeError("TAU_RELATIVE_MISMATCH")
if tau_contract["tau_score"]["formula"] != "TAU_RELATIVE * SCORE_SCALE":
    raise RuntimeError("TAU_FORMULA_MISMATCH")
if accept_contract["expected_bindings"]["tau_derivation_contract_blob"] != c.TAU_DERIVATION_CONTRACT_BLOB:
    raise RuntimeError("TAU_IDENTITY_MISMATCH")
if plan["real_data"] is not False or plan["real_fold3_replay"] is not False:
    raise RuntimeError("REAL_DATA_BOUNDARY_VIOLATION")

X=[[1.0,0.25],[1.0,-0.5],[1.0,0.75],[1.0,-1.0]]
tau=c.tau_score(X)
expected_scale=4.0
expected_tau=c.TAU_RELATIVE*expected_scale
if tau != expected_tau:
    raise RuntimeError("SYNTHETIC_TAU_DERIVATION_FAILURE")

base={
    "X":X,
    "parameters":[0.1,-0.2],
    "objective":2.0,
    "score_inf_norm":0.5*tau,
    "derivatives_finite":True,
    "full_required_design_rank":True,
    "perfect_separation":False,
    "one_class_sample":False,
    "solver":c.EXPECTED_SOLVER,
    "model_id":c.EXPECTED_MODEL_ID,
    "feature_contract_id":c.EXPECTED_FEATURE_CONTRACT_ID,
    "bindings":copy.deepcopy(c.EXPECTED_BINDINGS),
    "tau_contract_blob":c.TAU_DERIVATION_CONTRACT_BLOB,
    "optimizer_success":True,
    "optimizer_status":0,
    "optimizer_message":"SYNTHETIC",
    "registered_state":True,
    "reference_metadata":{"role":"DIAGNOSTIC_ONLY","success":True}
}

def packet(**changes):
    p=copy.deepcopy(base)
    p.update(changes)
    return p

below=math.nextafter(tau,0.0)
above=math.nextafter(tau,math.inf)

cases=[
    ("VALID_STATIONARY_FIT",packet(),"ACCEPT"),
    ("OPTIMIZER_SUCCESS_TRUE_CONTRACT_PASS",packet(optimizer_success=True),"ACCEPT"),
    ("OPTIMIZER_SUCCESS_FALSE_CONTRACT_PASS",packet(optimizer_success=False,optimizer_status=2,optimizer_message="PRECISION_LOSS"),"ACCEPT"),
    ("OPTIMIZER_SUCCESS_TRUE_SCORE_ABOVE_TAU",packet(optimizer_success=True,score_inf_norm=2*tau),"REJECT"),
    ("OPTIMIZER_SUCCESS_FALSE_SCORE_ABOVE_TAU",packet(optimizer_success=False,score_inf_norm=2*tau),"REJECT"),
    ("NONFINITE_SOLUTION",packet(parameters=[float("nan"),0.0]),"REJECT"),
    ("NONFINITE_OBJECTIVE",packet(objective=float("inf")),"REJECT"),
    ("NONFINITE_SCORE",packet(score_inf_norm=float("inf")),"REJECT"),
    ("NONFINITE_DERIVATIVES",packet(derivatives_finite=False),"REJECT"),
    ("RANK_DEFICIENCY",packet(full_required_design_rank=False),"REJECT"),
    ("PERFECT_SEPARATION",packet(perfect_separation=True),"REJECT"),
    ("ONE_CLASS_FAILURE",packet(one_class_sample=True),"REJECT"),
    ("BOUNDARY_SCORE_JUST_BELOW_TAU",packet(score_inf_norm=below),"ACCEPT"),
    ("BOUNDARY_SCORE_EXACTLY_AT_TAU",packet(score_inf_norm=tau),"ACCEPT"),
    ("BOUNDARY_SCORE_JUST_ABOVE_TAU",packet(score_inf_norm=above),"REJECT"),
    ("MISSING_TAU_SCORE_IDENTITY",packet(tau_contract_blob=None),"REJECT"),
    ("TAU_SCORE_IDENTITY_MISMATCH",packet(tau_contract_blob="WRONG"),"REJECT"),
    ("UNKNOWN_STATE",packet(registered_state=False),"FAIL_CLOSED"),
    ("UNEXPECTED_SOLVER",packet(solver="OTHER"),"REJECT"),
    ("UNEXPECTED_MODEL",packet(model_id="OTHER"),"REJECT"),
    ("UNEXPECTED_FEATURE_SET",packet(feature_contract_id="OTHER"),"REJECT"),
    ("UNEXPECTED_DATA_BINDING",packet(bindings={}),"REJECT"),
    ("NONFINITE_INPUT",packet(X=[[1.0,float("nan")]]),"REJECT"),
]

green=[]
for name,p,want in cases:
    got=c.evaluate(p)
    green.append({
        "name":name,
        "expected":want,
        "observed":got["verdict"],
        "tau_score":got["tau_score"],
        "score_inf_norm":got["score_inf_norm"],
        "receipt_identity":got["receipt_identity"],
        "status":"PASS" if got["verdict"]==want else "FAIL"
    })
if any(x["status"]!="PASS" for x in green):
    raise RuntimeError("GREEN_SYNTHETIC_QUALIFICATION_FAILURE")

def legacy_accept(p):
    return "ACCEPT" if p.get("optimizer_success") is True else "REJECT"

red_cases=[
    ("LEGACY_REJECTS_VALID_SUCCESS_FALSE",packet(optimizer_success=False,score_inf_norm=0.5*tau),"ACCEPT"),
    ("LEGACY_ACCEPTS_INVALID_SUCCESS_TRUE_ABOVE_TAU",packet(optimizer_success=True,score_inf_norm=2*tau),"REJECT"),
]
red=[]
for name,p,new_spec in red_cases:
    legacy=legacy_accept(p)
    demonstrated=legacy != new_spec
    red.append({"name":name,"legacy_observed":legacy,"new_spec_expected":new_spec,"red_demonstrated":demonstrated,"status":"PASS" if demonstrated else "FAIL"})
if any(x["status"]!="PASS" for x in red):
    raise RuntimeError("RED_TEST_FAILURE")

def replay():
    return [c.evaluate(p)["receipt_identity"] for _,p,_ in cases]
r1=replay()
r2=replay()
if r1 != r2:
    raise RuntimeError("NONDETERMINISTIC_RECEIPT_IDENTITY")
determinism={
    "schema":"ATDS_BEPD_09D_R2_RD2_DETERMINISM_RECEIPT_V0_1",
    "status":"PASS",
    "replay_1_identity":canonical_hash(r1),
    "replay_2_identity":canonical_hash(r2),
    "same_receipt_identities":True,
    "same_fit_candidate_input":True,
    "same_numerical_diagnostics":True,
    "same_accept_reject_verdicts":True
}

ref_a=packet(reference_metadata={"role":"DIAGNOSTIC_ONLY","success":True,"score":0.0})
ref_b=packet(reference_metadata={"role":"DIAGNOSTIC_ONLY","success":False,"score":"UNAVAILABLE"})
ea=c.evaluate(ref_a)
eb=c.evaluate(ref_b)
reference_role_pass=(
    ea["verdict"]==eb["verdict"]=="ACCEPT" and
    ea["gates"]==eb["gates"] and
    ea["tau_score"]==eb["tau_score"]
)
if not reference_role_pass:
    raise RuntimeError("REFERENCE_ROLE_INVARIANCE_FAILURE")

wr("07_RED_TEST_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD2_RED_TEST_RECEIPT_V0_1",
    "status":"PASS",
    "legacy_contract":"OPTIMIZER_SUCCESS_ONLY",
    "cases":red,
    "real_data_used":False
})
wr("08_GREEN_SYNTHETIC_QUALIFICATION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD2_GREEN_SYNTHETIC_QUALIFICATION_RECEIPT_V0_1",
    "status":"PASS",
    "case_count":len(green),
    "cases":green,
    "tau_derivation":{
        "float64_epsilon":c.FLOAT64_EPSILON,
        "tau_relative":c.TAU_RELATIVE,
        "synthetic_score_scale":expected_scale,
        "synthetic_tau_score":tau,
        "formula":"sqrt(epsilon) * max(1, max_j sum_i abs(X[i,j]))"
    },
    "optimizer_success_binding":"NON_BINDING_DIAGNOSTIC",
    "real_data_used":False
})
wr("09_DETERMINISM_RECEIPT.json",determinism)
wr("10_REFERENCE_ROLE_INVARIANCE_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD2_REFERENCE_ROLE_INVARIANCE_RECEIPT_V0_1",
    "status":"PASS",
    "reference_solver_role":"INDEPENDENT_NUMERICAL_CONSISTENCY_CHECK_ONLY_NOT_FALLBACK_NOT_RESULT_PRODUCER",
    "reference_metadata_variant_a":ref_a["reference_metadata"],
    "reference_metadata_variant_b":ref_b["reference_metadata"],
    "verdict_a":ea["verdict"],
    "verdict_b":eb["verdict"],
    "acceptance_gates_identical":ea["gates"]==eb["gates"],
    "tau_score_identical":ea["tau_score"]==eb["tau_score"],
    "reference_metadata_can_change_receipt_audit_identity_without_changing_acceptance":ea["receipt_identity"]!=eb["receipt_identity"],
    "real_reference_fit_executed":False
})
wr("11_CANDIDATE_B_QUALIFICATION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD2_CANDIDATE_B_QUALIFICATION_RECEIPT_V0_1",
    "status":"PASS",
    "verdict":"PREREGISTERED_AND_SYNTHETICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION",
    "candidate":"B",
    "tau_score_derivation":"PREREGISTERED_INDEPENDENT_OF_F2_OBSERVED_RESIDUAL",
    "tau_relative":c.TAU_RELATIVE,
    "tau_formula":"TAU_RELATIVE * max(1, max_j sum_i abs(X[i,j]))",
    "red_tests":"PASS",
    "green_synthetic_cases":len(green),
    "green_synthetic_qualification":"PASS",
    "determinism":"PASS",
    "reference_role_invariance":"PASS",
    "implementation_authorized":False,
    "real_training_requalification_authorized":False,
    "c1_retry_authorized":False,
    "scientific_result":"NONE",
    "fresh_oos":"CLOSED",
    "trading_authority":"NONE",
    "next":"HUMAN_ADJUDICATION_OF_PREREGISTERED_AND_SYNTHETICALLY_QUALIFIED_CANDIDATE_B_CONTRACT",
    "stop":True
})
print(json.dumps({
    "candidate":"B",
    "tau_relative":c.TAU_RELATIVE,
    "synthetic_tau":tau,
    "red":"PASS",
    "green_cases":len(green),
    "determinism":"PASS",
    "reference_role":"PASS",
    "verdict":"PREREGISTERED_AND_SYNTHETICALLY_QUALIFIED_FOR_HUMAN_ADJUDICATION"
},sort_keys=True))
