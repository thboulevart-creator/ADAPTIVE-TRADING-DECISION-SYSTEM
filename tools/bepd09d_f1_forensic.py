from __future__ import annotations
import hashlib,json,importlib.util
from pathlib import Path
import numpy as np
from scipy.optimize import minimize,linprog,root

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"/"bepd09d-f1-forensics"; OUT.mkdir(parents=True,exist_ok=True)
LEDGER=ROOT/"artifacts/bepd02/real-historical-weekly-liquidity-ledger-v0.1/EVENT_LEDGER.jsonl"
PART=ROOT/"GOVERNANCE/BEPD-09D0-FROZEN-CALENDAR-PARTITION-MANIFEST-V0.1.json"
RUNTIME=ROOT/"tools/bepd09c_runtime.py"
SHA="301a621b97fea14a72540d4c2c6da78eb742cc44c5009e44ad98e9f678ca4731"

def wr(n,o):(OUT/n).write_text(json.dumps(o,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
def load():
 s=importlib.util.spec_from_file_location("rt",RUNTIME);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def solve(X,y,it):
 signs=np.where(y>.5,1.,-1.);sep=linprog(np.zeros(X.shape[1]),A_ub=-(signs[:,None]*X),b_ub=-np.ones(len(y)),bounds=[(None,None)]*X.shape[1],method="highs")
 def f(b):
  z=X@b;return float(np.sum(np.logaddexp(0,z)-y*z))
 def g(b):
  z=X@b;p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)));return X.T@(p-y)
 def H(b):
  z=X@b;p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)));w=p*(1-p);return X.T@(X*w[:,None])
 r=minimize(f,np.zeros(X.shape[1]),jac=g,hess=H,method="Newton-CG",options={"xtol":1e-10,"maxiter":it,"disp":False})
 b=np.asarray(r.x);hh=H(b);sv=np.linalg.svd(X,compute_uv=False);ev=np.linalg.eigvalsh((hh+hh.T)/2);z=X@b;p=np.where(z>=0,1/(1+np.exp(-z)),np.exp(z)/(1+np.exp(z)))
 d={"success":bool(r.success),"status":int(r.status),"message":str(r.message),"nit":int(getattr(r,"nit",-1)),"nfev":int(getattr(r,"nfev",-1)),"gradient_inf":float(np.max(np.abs(g(b)))),"coefficients":[float(x) for x in b],"shape":list(X.shape),"rank":int(np.linalg.matrix_rank(X)),"condition_number":float(np.linalg.cond(X)),"singular_values":[float(x) for x in sv],"hessian_min_eigenvalue":float(np.min(ev)),"hessian_max_eigenvalue":float(np.max(ev)),"hessian_condition_number":float(np.linalg.cond(hh)),"linear_predictor_min":float(np.min(z)),"linear_predictor_max":float(np.max(z)),"probability_min":float(np.min(p)),"probability_max":float(np.max(p)),"saturated_probability_count_1e12":int(np.sum((p<1e-12)|(p>1-1e-12))),"perfect_separation":bool(sep.success),"finite":bool(np.all(np.isfinite(b)) and np.all(np.isfinite(hh)))}
 return d,f,g,H
raw=LEDGER.read_bytes()
assert hashlib.sha256(raw).hexdigest()==SHA
rows=[json.loads(x) for x in raw.decode().splitlines() if x.strip()];assert len(rows)==472
cal=[w for b in json.loads(PART.read_text())["blocks"] for w in b["weeks"]]
rt=load();rs=rt.validate_rows(rows,cal);bs=rt.partition_calendar(cal)
seq=[];bad=None
for i in range(1,6):
 trw={w for b in bs[:i] for w in b};tew=set(bs[i]);tr=[r for r in rs if r["target_week_id"] in trw];te=[r for r in rs if r["target_week_id"] in tew]
 rt.validate_fold_integrity(tr,te);s=rt._stats(tr);xb,xc=rt._mats(tr,s);y=np.array([r["y"] for r in tr])
 for name,X in (("BASELINE",xb),("CONTEXT",xc)):
  d,f,g,H=solve(X,y,100);seq.append({"fold":i,"model":name,"success":d["success"]})
  if not d["success"]:
   ext,_,_,_=solve(X,y,5000)
   rr=root(g,np.zeros(X.shape[1]),jac=H,method="hybr",options={"xtol":1e-10,"maxfev":5000})
   cf={"newton_cg_5000":{"success":ext["success"],"message":ext["message"],"nit":ext["nit"],"gradient_inf":ext["gradient_inf"]},"root_hybr":{"success":bool(rr.success),"message":str(rr.message),"nfev":int(rr.nfev),"score_inf":float(np.max(np.abs(g(rr.x))))}}
   bad={"fold":i,"model":name,"train_event_count":len(tr),"test_event_count_not_scored":len(te),"class_counts":{"0":int(np.sum(y==0)),"1":int(np.sum(y==1))},"standardization":{k:{"mean":float(v[0]),"sample_sd":float(v[1])} for k,v in s.items()},"original_solver":d,"counterfactuals":cf};break
 if bad:break
assert bad is not None
wr("03_FAILED_FOLD_IDENTIFICATION_RECEIPT.json",{"status":"PASS","failed_fold":bad["fold"],"failed_model":bad["model"],"fit_sequence":seq,"test_predictions_computed":False,"scientific_metrics_computed":False})
wr("04_NUMERICAL_STATE_DIAGNOSTIC_RECEIPT.json",{"status":"PASS",**bad})
wr("05_DESIGN_MATRIX_CONDITIONING_RECEIPT.json",{"status":"PASS","fold":bad["fold"],"model":bad["model"],**{k:bad["original_solver"][k] for k in ["shape","rank","condition_number","singular_values","hessian_min_eigenvalue","hessian_max_eigenvalue","hessian_condition_number","perfect_separation","finite"]}})
wr("06_SOLVER_TERMINATION_FORENSIC_RECEIPT.json",{"status":"PASS","fold":bad["fold"],"model":bad["model"],"original":bad["original_solver"],"counterfactuals":bad["counterfactuals"],"forensic_only":True,"non_scientific":True,"non_admissible_as_c1_result":True})
wr("07_FORENSIC_RAW_PACKAGE.json",{"status":"FORENSIC_EXECUTION_COMPLETED","failed_fit":bad,"fit_sequence":seq,"event_ledger_rows_re_read":472,"scientific_result":"NONE","c1_rerun":False,"repair_applied":False,"trading_authority":"NONE"})
print("BEPD-09D-F1 FORENSIC EXECUTION COMPLETED")
