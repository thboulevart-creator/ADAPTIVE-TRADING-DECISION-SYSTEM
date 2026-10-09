"""BEPD-09D-R2-RD5 frozen test-first synthetic regression and adversarial matrix."""
from __future__ import annotations
import copy
import hashlib
import json
import math
import unittest
from unittest.mock import patch
from pathlib import Path

import numpy as np
import bepd09d_r2_rd5_synthetic_fixture as fixture
import bepd09d_r2_rd5_training_only_adapter as adapter
import bepd09d_r2_rd3_candidate_b_runtime as candidate

class TrainingOnlyRD5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = fixture.training_rows(1)

    def run_precheck(self, rows=None, fold=1, **opts):
        return adapter.execute_synthetic_fold(
            fold_id=fold, rows=copy.deepcopy(self.rows if rows is None else rows),
            provenance=fixture.PROVENANCE, perform_fit=False, **opts)

    def must_stop(self, rows=None, fold=1, **opts):
        with self.assertRaises(adapter.TrainingOnlyBreaker):
            self.run_precheck(rows, fold, **opts)

    def test_01_calendar_259_frozen(self):
        self.assertEqual(len(fixture.WEEKS),259)
        self.assertEqual(tuple(map(len,fixture.BLOCKS.values())),(44,43,43,43,43,43))
        self.assertEqual(fixture.WEEKS[0],"2021-06-07")
        self.assertEqual(fixture.WEEKS[-1],"2026-05-18")

    def test_02_all_folds_exact(self):
        self.assertEqual([len(fixture.FOLDS[i][0]) for i in range(1,6)],[44,87,130,173,216])
        for i in range(1,6):
            self.assertFalse(set(fixture.FOLDS[i][0]) & set(fixture.FOLDS[i][1]))

    def test_03_valid_training_precheck_no_fit(self):
        a=self.run_precheck()
        self.assertEqual(a["fold_id"],1)
        self.assertEqual(a["model_role"],"PRECHECK_ONLY")
        self.assertEqual(a["training_row_count"],len(self.rows))
        self.assertEqual(a["verdict"],"STATIC_SYNTHETIC_PRECHECK_PASS")

    def test_04_later_fold_includes_former_test(self):
        rows=fixture.training_rows(2, per_week=2)
        a=self.run_precheck(rows,2)
        self.assertEqual(a["training_row_count"],len(rows))
        self.assertIn("B2",a["train_block_ids"])

    def test_05_fold_zero(self):
        self.must_stop(fold=0)

    def test_06_fold_six(self):
        self.must_stop(fold=6)

    def test_07_injected_current_test_week(self):
        rows=copy.deepcopy(self.rows)+[fixture.synthetic_row(fixture.BLOCKS["B2"][0],0)]
        self.must_stop(rows)

    def test_08_injected_future_week(self):
        rows=copy.deepcopy(self.rows)+[fixture.synthetic_row(fixture.BLOCKS["B3"][0],0)]
        self.must_stop(rows)

    def test_09_duplicate_event(self):
        self.must_stop(copy.deepcopy(self.rows)+[copy.deepcopy(self.rows[0])])

    def test_10_cluster_reused_across_weeks(self):
        rows=copy.deepcopy(self.rows)
        rows[6]["sweep_cluster_id"]=rows[0]["sweep_cluster_id"]
        self.must_stop(rows)

    def test_11_extra_test_label_key(self):
        rows=copy.deepcopy(self.rows)
        rows[0]["test_response"]=True
        self.must_stop(rows)

    def test_12_missing_source_key(self):
        rows=copy.deepcopy(self.rows)
        del rows[0]["same_week_reintegration"]
        self.must_stop(rows)

    def test_13_bad_side(self):
        rows=copy.deepcopy(self.rows)
        rows[0]["side"]="OTHER"
        self.must_stop(rows)

    def test_14_response_not_bool(self):
        rows=copy.deepcopy(self.rows)
        rows[0]["same_week_reintegration"]=1
        self.must_stop(rows)

    def test_15_nonfinite_input(self):
        rows=copy.deepcopy(self.rows)
        rows[0]["level_price_mid"]=float("nan")
        self.must_stop(rows)

    def test_16_zero_price(self):
        rows=copy.deepcopy(self.rows)
        rows[0]["level_price_mid"]=0
        self.must_stop(rows)

    def test_17_one_class_sample(self):
        rows=copy.deepcopy(self.rows)
        for r in rows:r["same_week_reintegration"]=True
        self.must_stop(rows)

    def test_18_rank_deficient_context(self):
        rows=copy.deepcopy(self.rows)
        for r in rows:r["level_age_weeks"]=3
        self.must_stop(rows)

    def test_19_bad_provenance(self):
        with self.assertRaises(adapter.TrainingOnlyBreaker):
            adapter.execute_synthetic_fold(fold_id=1,rows=copy.deepcopy(self.rows),provenance="REAL_LEDGER",perform_fit=False)

    def test_20_wrong_contract_identity(self):
        self.must_stop(contract_identity="FORGED_IDENTITY")

    def test_21_no_raw_or_coefficients_in_receipt(self):
        obj=self.run_precheck()
        self.assertEqual(set(obj),adapter.ALLOWLIST)
        self.assertNotIn("parameters",json.dumps(obj))
        self.assertNotIn("matrix",json.dumps(obj))

    def test_22_serializer_rejects_extra_key(self):
        with self.assertRaises(adapter.TrainingOnlyBreaker):
            adapter.safe_receipt({"fold_id":1,"parameters":[1.]})

    def test_23_outside_reader_forbidden(self):
        self.assertFalse(hasattr(adapter,"read_real_ledger"))
        source=Path(adapter.__file__).read_text(encoding="utf-8")
        self.assertNotIn("EVENT_LEDGER.jsonl",source)
        self.assertNotIn("run_protocol(",source)

    def test_24_unknown_preflight_lp(self):
        with patch.object(adapter, "_linprog", side_effect=RuntimeError("LP_UNAVAILABLE")):
            self.must_stop()

    def test_25_positive_synthetic_fit_two_models(self):
        out=adapter.execute_synthetic_fold(fold_id=1,rows=copy.deepcopy(self.rows),provenance=fixture.PROVENANCE,perform_fit=True)
        self.assertEqual(len(out),2)
        for q in out:
            self.assertEqual(set(q),adapter.ALLOWLIST)
            self.assertEqual(q["verdict"],"ACCEPT")
            self.assertNotIn("parameters",json.dumps(q))
            self.assertTrue(q["mathematical_gate_statuses"]["SCORE_INF_NORM_LTE_TAU_SCORE"])

    def test_26_deterministic_receipt(self):
        a=adapter.execute_synthetic_fold(fold_id=1,rows=copy.deepcopy(self.rows),provenance=fixture.PROVENANCE,perform_fit=True)
        b=adapter.execute_synthetic_fold(fold_id=1,rows=copy.deepcopy(self.rows),provenance=fixture.PROVENANCE,perform_fit=True)
        self.assertEqual(a,b)

    def test_27_unknown_internal_second_LP_fail_closed(self):
        orig=candidate.linprog
        calls=[0]
        def injected(*args,**kwargs):
            calls[0]+=1
            if calls[0]==2:raise RuntimeError("SYNTHETIC_INTERNAL_LP_EXCEPTION")
            return orig(*args,**kwargs)
        with patch.object(candidate,"linprog",side_effect=injected):
            with self.assertRaises(adapter.TrainingOnlyBreaker):
                adapter.execute_synthetic_fold(fold_id=1,rows=copy.deepcopy(self.rows),provenance=fixture.PROVENANCE,perform_fit=True)
        self.assertGreaterEqual(calls[0],2)

    def test_28_reference_only_diagnostic(self):
        self.assertEqual(adapter.REFERENCE_ROLE,"INDEPENDENT_NUMERICAL_CONSISTENCY_CHECK_ONLY")
        self.assertFalse(adapter.REAL_EXECUTION_PATH_ACTIVATION)
        self.assertIsNone(candidate.run_protocol)
        self.assertFalse(candidate.REAL_EXECUTION_PATH_ACTIVATION)

    def test_29_reference_synthetic_stationarity_not_parity(self):
        info=adapter.synthetic_reference_probe()
        self.assertEqual(info["reference_role"],adapter.REFERENCE_ROLE)
        self.assertTrue(info["stationarity_gate"])
        self.assertEqual(info["comparison_parity"],"UNADJUDICATED_NOT_EXECUTED")

if __name__=="__main__":
    unittest.main()
