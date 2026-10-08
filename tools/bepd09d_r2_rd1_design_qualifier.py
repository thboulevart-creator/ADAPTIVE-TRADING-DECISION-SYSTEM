from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-r2-rd1-design"
OUT.mkdir(parents=True,exist_ok=True)

contract=json.loads((ROOT/"GOVERNANCE/BEPD-09D-R2-RD1-REPAIR-DESIGN-CONTRACT-V0.1.json").read_text())
matrix=json.loads((ROOT/"reports/program/2026-10-08-BEPD-09D-R2-RD1-CANDIDATE-DECISION-MATRIX-V0.1.json").read_text())

candidates=["A","B","C","D","E","F"]
dims=[f"D{i}" for i in range(1,13)]
if list(matrix["candidates"].keys()) != candidates:
    raise RuntimeError("CANDIDATE_SET_MISMATCH")
if set(contract["dimensions"].keys()) != set(dims):
    raise RuntimeError("DIMENSION_SET_MISMATCH")

g=contract["mandatory_gates"]
scores={}
eligible={}
for k in candidates:
    s=matrix["candidates"][k]["scores"]
    if set(s.keys()) != set(dims):
        raise RuntimeError("SCORE_DIMENSION_MISMATCH:"+k)
    if any((not isinstance(v,int)) or v<0 or v>3 for v in s.values()):
        raise RuntimeError("INVALID_SCORE:"+k)
    scores[k]=sum(s.values())
    eligible[k]=(
        s["D1"]>=g["D1_min"] and
        s["D3"]>=g["D3_min"] and
        s["D4"]>=g["D4_min"] and
        s["D5"]>=g["D5_min"] and
        s["D8"]>=g["D8_min"] and
        s["D12"]>=g["D12_min"]
    )

ranked=sorted([k for k in candidates if eligible[k]], key=lambda k:scores[k], reverse=True)
if len(ranked) < 2:
    recommendation="NOT_DETERMINED"
    margin=None
else:
    margin=scores[ranked[0]]-scores[ranked[1]]
    recommendation=ranked[0] if margin>=contract["recommendation_rule"]["minimum_margin_over_second_place"] else "NOT_DETERMINED"

def accept_b(finite_solution,finite_objective,finite_score,no_separation,full_rank,score,tau,optimizer_success):
    return finite_solution and finite_objective and finite_score and no_separation and full_rank and score<=tau

tau=1.0
fixtures=[
    ("SUCCESS_TRUE_VALID",(True,True,True,True,True,0.5*tau,tau,True),True),
    ("SUCCESS_FALSE_BUT_VALID",(True,True,True,True,True,0.5*tau,tau,False),True),
    ("RESIDUAL_ABOVE_TAU",(True,True,True,True,True,2.0*tau,tau,True),False),
    ("NONFINITE",(False,True,True,True,True,0.1*tau,tau,True),False),
    ("SEPARATION",(True,True,True,False,True,0.1*tau,tau,True),False),
    ("RANK_DEFICIENT",(True,True,True,True,False,0.1*tau,tau,True),False),
]
fixture_results=[]
for name,args,expected in fixtures:
    observed=accept_b(*args)
    fixture_results.append({"name":name,"expected":expected,"observed":observed,"status":"PASS" if observed==expected else "FAIL"})
if any(x["status"]!="PASS" for x in fixture_results):
    raise RuntimeError("CANDIDATE_B_SEMANTIC_FIXTURE_FAILURE")

if contract["candidate_B_threshold"]!="NOT_DETERMINED":
    raise RuntimeError("RD1_IMPROPERLY_SELECTED_THRESHOLD")
if contract["new_real_fits"] is not False or contract["repair_implementation"] is not False:
    raise RuntimeError("RD1_BOUNDARY_VIOLATION")

def write(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

write("09_MACHINE_RECOMMENDATION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD1_MACHINE_RECOMMENDATION_RECEIPT_V0_1",
    "status":"PASS",
    "scores":scores,
    "eligible":eligible,
    "eligible_ranked":ranked,
    "top_margin":margin,
    "recommended_candidate":recommendation,
    "candidate_B_semantic_fixtures":fixture_results,
    "candidate_B_tau_score":"NOT_DETERMINED",
    "repair_adopted":False,
    "repair_implemented":False
})
write("10_REPAIR_DESIGN_QUALIFICATION_RECEIPT.json",{
    "schema":"ATDS_BEPD_09D_R2_RD1_REPAIR_DESIGN_QUALIFICATION_RECEIPT_V0_1",
    "status":"PASS",
    "verdict":"REPAIR_DESIGN_QUALIFIED_FOR_HUMAN_SELECTION",
    "recommended_candidate":recommendation,
    "recommendation_is_not_adoption":True,
    "new_real_training_fits":False,
    "new_reference_fits":False,
    "new_test_fits":False,
    "scientific_result":"NONE",
    "repair_selection":"NONE",
    "repair_implementation":False,
    "bepd_09d_r2":"NOT_PRE_RETRY_READY",
    "c1_retry":"NOT_AUTHORIZED",
    "fresh_oos":"CLOSED",
    "trading_authority":"NONE",
    "next":"HUMAN_SELECTION_OR_REJECTION_OF_REPAIR_CANDIDATE",
    "stop":True
})
print(json.dumps({"scores":scores,"eligible":eligible,"recommended_candidate":recommendation,"margin":margin},sort_keys=True))
