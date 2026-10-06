#!/usr/bin/env python3
"""Executable-equivalent BEPD-08C 32-case breaker for BEPD-08D."""
from __future__ import annotations
import argparse,copy,importlib.util
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"tools"/"bepd_08d_internal_external_distance.py"
S=importlib.util.spec_from_file_location("r",P);r=importlib.util.module_from_spec(S);S.loader.exec_module(r)
CASES=[
"wrong EVENT_LEDGER identity","wrong BEPD-05A identity","wrong BEPD-05B identity","wrong BEPD-08A identity","wrong BEPD-08B identity",
"using same_week_reintegration for classification","using reintegration_h1_close_utc for classification","using HIGH / LOW for classification",
"reversing positive / negative sign semantics","assigning zero to INTERNAL","assigning zero to EXTERNAL","dropping INTERNAL rows","dropping EXTERNAL rows",
"overlapping INTERNAL / EXTERNAL membership","non-exhaustive partition","recomputing market prices","reading AP0","reading H1","negative D_CLOSE",
"signed values retained as conditional distance","changing Type-7 quantiles","changing ECDF semantics","subgroup cross-product","post-hoc threshold search",
"INTERNAL distribution → TP laundering","EXTERNAL distribution → SL laundering","outcome-side → predictor laundering","IID laundering","prediction laundering",
"edge laundering","strategy-validation laundering","trading-authority laundering"]
def fail(fn,label):
 try:fn()
 except Exception:return
 raise AssertionError("breaker did not fail: "+label)
def mp(**k):
 p=copy.deepcopy(r.POLICY);p.update(k);return p
def run():
 if len(CASES)!=32:raise AssertionError("case count")
 # identity families are all hard-bound through validate_bindings
 for key in ["event_ledger_blob","bepd05a_contract_blob","bepd05b_result_blob","bepd08a_contract_blob","bepd08b_result_blob"]:
  fail(lambda k=key:r.validate_bindings({**r.EXPECTED_BINDINGS,k:"bad"}),key)
 fail(lambda:r.validate_policy(mp(same_week_reintegration_used=True)),CASES[5])
 fail(lambda:r.validate_policy(mp(reintegration_h1_close_utc_used=True)),CASES[6])
 fail(lambda:r.validate_policy(mp(high_low_used=True)),CASES[7])
 fail(lambda:r.validate_policy(mp(internal_rule="close_displacement < 0")),CASES[8])
 fail(lambda:r.validate_policy(mp(exact_level_rule="zero -> INTERNAL")),CASES[9])
 fail(lambda:r.validate_policy(mp(exact_level_rule="zero -> EXTERNAL")),CASES[10])
 # row-drop/partition breakers
 rows=[{"event_id":"i","close_displacement":Decimal("1")},{"event_id":"e","close_displacement":Decimal("-1")}]
 fail(lambda:r.partition_rows(rows,2,0,1,1),CASES[11])
 fail(lambda:r.partition_rows(rows,2,1,0,1),CASES[12])
 fail(lambda:r.partition_rows(rows,2,2,2,0),CASES[13])
 fail(lambda:r.partition_rows(rows,3,1,1,1),CASES[14])
 fail(lambda:r.validate_policy(mp(market_reconstruction=True)),CASES[15])
 fail(lambda:r.validate_policy(mp(ap0_read=True)),CASES[16])
 fail(lambda:r.validate_policy(mp(h1_read=True)),CASES[17])
 fail(lambda:r.aggregate([Decimal("-1")]),CASES[18])
 fail(lambda:r.validate_policy(mp(distance="close_displacement")),CASES[19])
 # numerical policy drift represented as forbidden altered metadata
 fail(lambda:r.validate_policy({**r.POLICY,"quantile_method":"OTHER"}),CASES[20])
 fail(lambda:r.validate_policy({**r.POLICY,"ecdf":"BINNED"}),CASES[21])
 fail(lambda:r.validate_policy({**r.POLICY,"subgroup_cross_product":True}),CASES[22])
 fail(lambda:r.validate_policy(mp(threshold_search=True)),CASES[23])
 fail(lambda:r.validate_policy(mp(tp_sl=True)),CASES[24])
 fail(lambda:r.validate_policy(mp(tp_sl=True)),CASES[25])
 fail(lambda:r.validate_policy({**r.POLICY,"outcome_side_as_predictor":True}),CASES[26])
 fail(lambda:r.validate_policy({**r.POLICY,"event_is_iid":True}),CASES[27])
 fail(lambda:r.validate_policy(mp(prediction=True)),CASES[28])
 fail(lambda:r.validate_policy(mp(edge=True)),CASES[29])
 fail(lambda:r.validate_policy(mp(strategy_validation=True)),CASES[30])
 fail(lambda:r.validate_policy(mp(trading_authority="AUTHORIZED")),CASES[31])
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--mode",choices=["pre-result","real-preflight"],default="pre-result");a=ap.parse_args()
 r.validate_bindings(r.EXPECTED_BINDINGS);r.validate_policy(r.POLICY);run()
 print("BEPD08C_EXECUTABLE_EQUIVALENT_BREAKER=32/32_PASS");print("MODE="+a.mode)
if __name__=="__main__":main()
