from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

CFG = load_module("ao_e0_b8_smf_01", ROOT / "tools" / "ao_e0_b8_smf_01_preregistration.py")
DI = load_module("smf03_dependence_inference", ROOT / "tools" / "smf03_dependence_inference.py")
EG = load_module("smf03_evidence_governance", ROOT / "tools" / "smf03_evidence_governance.py")
CONTRACT = json.loads((ROOT / "GOVERNANCE" / "AO-E0-B8-SMF-01-MATERIAL-CONFIGURATION-CANDIDATE-V0.1.json").read_text())

class TestAOE0B8SMF01(unittest.TestCase):
    def test_candidate_projection_at_required_n(self):
        c = CFG.candidate_for_n(58927)
        self.assertEqual(c["m04"]["estimator"], "ADJUSTED")
        self.assertEqual(c["m04"]["lags"][0], 1)
        self.assertEqual(c["m04"]["lags"][-1], 39)
        self.assertEqual(len(c["m04"]["lags"]), 39)
        self.assertEqual(c["m05"]["block_length"], 40)
        self.assertEqual(c["m05"]["scheme"], "MOVING_BLOCK")
        self.assertEqual(c["m05"]["replications"], 50000)

    def test_lag_rule_is_deterministic_and_bounded(self):
        self.assertEqual(CFG.m04_lags(8), [1, 2])
        self.assertEqual(CFG.m05_block_length(8), 3)
        with self.assertRaisesRegex(ValueError, "INSUFFICIENT_N_FOR_M04"):
            CFG.m04_lags(1)

    def test_m04_detects_material_dependence(self):
        values = [1.0, -1.0] * 20
        out = DI.dependence_diagnostics(values, lags=CFG.m04_lags(len(values)), estimator="ADJUSTED", abs_threshold=0.05, structural_flags=[])
        self.assertEqual(out["status"], "DETECTED_WITHIN_TESTED_LAGS")

    def test_m04_structural_flags_cannot_be_erased(self):
        values = [1.0, 2.0, 4.0, 8.0, 3.0, 7.0, 5.0, 9.0]
        out = DI.dependence_diagnostics(values, lags=[1], estimator="ADJUSTED", abs_threshold=0.99, structural_flags=["OVERLAP"])
        self.assertEqual(out["status"], "STRUCTURALLY_PRESENT")

    def test_m04_low_acf_ne_independence_claim(self):
        values = [3.0, -2.0, 5.0, 1.0, -4.0, 6.0, 0.5, -1.0, 2.5, -3.0]
        out = DI.dependence_diagnostics(values, lags=[1], estimator="ADJUSTED", abs_threshold=0.99, structural_flags=[])
        self.assertNotEqual(out["status"], "INDEPENDENCE_PROVEN")

    def test_m04_invalid_surface_blocks(self):
        vals = [1.0,2.0,3.0,4.0]
        with self.assertRaisesRegex(ValueError, "ACF_ESTIMATOR_UNSUPPORTED"):
            DI.dependence_diagnostics(vals,lags=[1],estimator="AUTO",abs_threshold=.05,structural_flags=[])
        with self.assertRaisesRegex(ValueError, "LAGS_REQUIRED"):
            DI.dependence_diagnostics(vals,lags=[],estimator="ADJUSTED",abs_threshold=.05,structural_flags=[])
        with self.assertRaisesRegex(ValueError, "DUPLICATE_LAG"):
            DI.dependence_diagnostics(vals,lags=[1,1],estimator="ADJUSTED",abs_threshold=.05,structural_flags=[])
        with self.assertRaisesRegex(ValueError, "LAG_OUT_OF_RANGE"):
            DI.dependence_diagnostics(vals,lags=[0],estimator="ADJUSTED",abs_threshold=.05,structural_flags=[])
        with self.assertRaisesRegex(ValueError, "LAG_OUT_OF_RANGE"):
            DI.dependence_diagnostics(vals,lags=[4],estimator="ADJUSTED",abs_threshold=.05,structural_flags=[])
        with self.assertRaisesRegex(ValueError, "INVALID_ACF_THRESHOLD"):
            DI.dependence_diagnostics(vals,lags=[1],estimator="ADJUSTED",abs_threshold=0,structural_flags=[])

    def test_m05_candidate_exact_and_deterministic(self):
        values = [1.0,2.0,4.0,3.0,6.0,5.0,8.0,7.0]
        kwargs = dict(
            scheme="MOVING_BLOCK", interval_method="PERCENTILE",
            confidence_level=0.99, replications=50000, seed=21449402,
            stationarity_status="RESOLVED_FOR_RESAMPLING",
            block_length=CFG.m05_block_length(len(values)))
        a = DI.bootstrap_mean_ci(values, **kwargs)
        b = DI.bootstrap_mean_ci(values, **kwargs)
        self.assertEqual(a, b)
        self.assertEqual(a["scheme"], "MOVING_BLOCK")
        self.assertEqual(a["interval_method"], "PERCENTILE")
        self.assertEqual(a["confidence_level"], 0.99)
        self.assertEqual(a["replications"], 50000)
        self.assertEqual(a["seed"], 21449402)

    def test_m05_unresolved_nonstationarity_blocks(self):
        with self.assertRaisesRegex(ValueError, "UNRESOLVED_NONSTATIONARITY"):
            DI.bootstrap_mean_ci([1,2,3,4], scheme="MOVING_BLOCK", interval_method="PERCENTILE", confidence_level=.99, replications=10, seed=1, stationarity_status="UNRESOLVED_NONSTATIONARY", block_length=2)

    def test_m05_iid_not_candidate_and_unjustified_iid_blocks(self):
        self.assertEqual(CONTRACT["m05"]["scheme_policy"], "MOVING_BLOCK_ONLY_FOR_AO_E0_WHEN_M05_EXECUTES")
        with self.assertRaisesRegex(ValueError, "IID_NOT_JUSTIFIED"):
            DI.bootstrap_mean_ci([1,2,3,4], scheme="IID", interval_method="PERCENTILE", confidence_level=.99, replications=10, seed=1, stationarity_status="RESOLVED", iid_justified=False)

    def test_m05_invalid_surface_blocks(self):
        vals=[1,2,3,4]
        with self.assertRaisesRegex(ValueError, "BOOTSTRAP_SCHEME_UNSUPPORTED"):
            DI.bootstrap_mean_ci(vals,scheme="AUTO",interval_method="PERCENTILE",confidence_level=.99,replications=10,seed=1,stationarity_status="RESOLVED")
        with self.assertRaisesRegex(ValueError, "INTERVAL_METHOD_UNSUPPORTED"):
            DI.bootstrap_mean_ci(vals,scheme="MOVING_BLOCK",interval_method="AUTO",confidence_level=.99,replications=10,seed=1,stationarity_status="RESOLVED",block_length=2)
        with self.assertRaisesRegex(ValueError, "INVALID_CONFIDENCE_LEVEL"):
            DI.bootstrap_mean_ci(vals,scheme="MOVING_BLOCK",interval_method="PERCENTILE",confidence_level=1.0,replications=10,seed=1,stationarity_status="RESOLVED",block_length=2)
        with self.assertRaisesRegex(ValueError, "INVALID_REPLICATIONS"):
            DI.bootstrap_mean_ci(vals,scheme="MOVING_BLOCK",interval_method="PERCENTILE",confidence_level=.99,replications=0,seed=1,stationarity_status="RESOLVED",block_length=2)
        with self.assertRaisesRegex(ValueError, "SEED_REQUIRED"):
            DI.bootstrap_mean_ci(vals,scheme="MOVING_BLOCK",interval_method="PERCENTILE",confidence_level=.99,replications=10,seed=None,stationarity_status="RESOLVED",block_length=2)
        with self.assertRaisesRegex(ValueError, "BLOCK_LENGTH_REQUIRED"):
            DI.bootstrap_mean_ci(vals,scheme="MOVING_BLOCK",interval_method="PERCENTILE",confidence_level=.99,replications=10,seed=1,stationarity_status="RESOLVED",block_length=None)

    def test_m07_materiality_threshold_exact(self):
        out = EG.influence_analysis([20.0,20.0,0.0,0.0], unit_ids=["A","A","B","B"], materiality_abs_delta=5.0)
        self.assertTrue(out["material_influence"])
        self.assertEqual(out["materiality_abs_delta"], 5.0)
        self.assertGreaterEqual(out["max_abs_delta"], 5.0)

    def test_m07_invalid_surface_blocks(self):
        with self.assertRaisesRegex(ValueError, "UNIT_ID_LENGTH_MISMATCH"):
            EG.influence_analysis([1.0,2.0], unit_ids=["A"], materiality_abs_delta=5.0)
        with self.assertRaisesRegex(ValueError, "INVALID_MATERIALITY_THRESHOLD"):
            EG.influence_analysis([1.0,2.0], unit_ids=["A","B"], materiality_abs_delta=-1.0)

    def test_m08_gap_threshold_exact(self):
        included = [True]*10 + [True]*9 + [False]
        reasons = [""]*19 + ["EXCLUDED"]
        strata = ["A"]*10 + ["B"]*10
        out = EG.attrition_analysis(included=included, reasons=reasons, strata=strata, max_inclusion_rate_gap=0.05)
        self.assertAlmostEqual(out["observed_inclusion_rate_gap"], 0.10)
        self.assertTrue(out["material_selection_asymmetry"])
        self.assertEqual(out["max_inclusion_rate_gap"], 0.05)

    def test_m08_invalid_surface_blocks(self):
        with self.assertRaisesRegex(ValueError, "INCLUSION_INDICATOR_NOT_BOOLEAN"):
            EG.attrition_analysis(included=[True,1],reasons=["",""],strata=["A","B"],max_inclusion_rate_gap=.05)
        with self.assertRaisesRegex(ValueError, "EXCLUSION_REASON_REQUIRED"):
            EG.attrition_analysis(included=[True,False],reasons=["",""],strata=["A","B"],max_inclusion_rate_gap=.05)
        with self.assertRaisesRegex(ValueError, "STRATUM_LENGTH_MISMATCH"):
            EG.attrition_analysis(included=[True,False],reasons=["","X"],strata=["A"],max_inclusion_rate_gap=.05)
        with self.assertRaisesRegex(ValueError, "INVALID_INCLUSION_RATE_GAP_THRESHOLD"):
            EG.attrition_analysis(included=[True,False],reasons=["","X"],strata=["A","B"],max_inclusion_rate_gap=1.1)

    def test_no_silent_parameter_inheritance(self):
        self.assertFalse(CONTRACT["m05"]["confidence_silent_inheritance_from_m06"])
        self.assertIn("separate M07 policy decision", CONTRACT["m07"]["rationale"])
        self.assertTrue(CONTRACT["cross_method"]["same_numeric_value_ne_same_semantic_role"])

    def test_no_free_material_parameter(self):
        m04=CONTRACT["m04"]; m05=CONTRACT["m05"]; m07=CONTRACT["m07"]; m08=CONTRACT["m08"]
        self.assertIn(m04["acf_estimator"], ["BIASED","ADJUSTED"])
        self.assertEqual(m04["lags_policy"]["type"], "FULLY_DETERMINISTIC_PREDECLARED_SELECTION_RULE")
        self.assertGreater(m04["absolute_threshold"], 0)
        self.assertEqual(m05["scheme_policy"], "MOVING_BLOCK_ONLY_FOR_AO_E0_WHEN_M05_EXECUTES")
        self.assertIn(m05["interval_method"], ["PERCENTILE","BASIC"])
        self.assertTrue(0 < m05["confidence_level"] < 1)
        self.assertGreater(m05["replications"], 0)
        self.assertIsInstance(m05["seed"], int)
        self.assertEqual(m05["moving_block_length_policy"]["type"], "FULLY_DETERMINISTIC_PREDECLARED_SELECTION_RULE")
        self.assertGreaterEqual(m07["materiality_abs_delta"], 0)
        self.assertTrue(0 <= m08["max_inclusion_rate_gap"] <= 1)

    def test_m06_unchanged_and_authority_absent(self):
        m06=CONTRACT["m06_non_modification"]
        self.assertEqual(m06["final_required_n"], 58927)
        self.assertEqual(m06["confidence_level"], .99)
        self.assertEqual(m06["alpha"], .01)
        self.assertFalse(m06["modified_by_smf_01"])
        self.assertTrue(all(v is False for v in CONTRACT["authority"].values()))
        self.assertEqual(CONTRACT["state"]["b8"], "BLOCKED")
        self.assertEqual(CONTRACT["state"]["b12"], "CLOSED")

if __name__ == "__main__":
    unittest.main()
