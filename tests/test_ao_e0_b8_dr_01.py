from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

DR = load_module("ao_e0_b8_dr_01", ROOT / "tools" / "ao_e0_b8_dr_01_decision_rule.py")

def base():
    return {
        "sample_n": 58927,
        "m05_interval_available": True,
        "m05_ci_lower": 6.0,
        "m05_ci_upper": 8.0,
        "stationarity_status": "RESOLVED_FOR_RESAMPLING",
        "f2_s4_status": "COST_ROBUSTNESS_PASS",
        "m07_material_influence": False,
        "m07_sign_reversal": False,
        "m08_material_selection_asymmetry": False,
        "prior_exposure_state": "CONTAMINATED",
        "search_universe_status": "PARTIAL_SEARCH_UNIVERSE",
        "n_trials": None,
        "confirmatory_route": "NEW_FORWARD_DATA_ONLY",
    }

class TestAOE0B8DR01(unittest.TestCase):
    def test_support_requires_all_clean_gates(self):
        out = DR.evaluate(base())
        self.assertEqual(out["evidence_verdict"], "SUPPORT")
        self.assertEqual(out["qualification_status"], "QUALIFIED")
        self.assertIn("PRIOR_SEARCH_UNIVERSE_PARTIAL", out["qualification_limitations"])

    def test_support_creates_no_authority(self):
        out = DR.evaluate(base())
        self.assertEqual(out["decision"], "PENDING_HUMAN_PROMOTION")
        self.assertEqual(out["decision_authority"], "NONE")
        self.assertFalse(out["b8_closure"])
        self.assertFalse(out["b12_open"])
        self.assertFalse(out["ao_e0_execution_authorized"])

    def test_direct_refute_requires_ci_and_f2_fail(self):
        x = base(); x.update(m05_ci_lower=1.0, m05_ci_upper=5.0, f2_s4_status="COST_ROBUSTNESS_FAIL")
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "REFUTE")
        self.assertEqual(out["qualification_status"], "NOT_QUALIFIED")

    def test_ci_overlap_is_inconclusive(self):
        x = base(); x.update(m05_ci_lower=4.0, m05_ci_upper=6.0)
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("CI_OVERLAPS_MATERIALITY_BOUNDARY", out["all_qualification_reasons"])

    def test_lower_equal_boundary_is_not_support(self):
        self.assertEqual(DR.classify_m05_ci(5.0, 7.0), "INCONCLUSIVE")

    def test_upper_equal_boundary_is_refute_signal(self):
        self.assertEqual(DR.classify_m05_ci(1.0, 5.0), "REFUTE")

    def test_above_boundary_is_support_signal(self):
        self.assertEqual(DR.classify_m05_ci(5.000001, 6.0), "SUPPORT")

    def test_insufficient_sample_is_inconclusive_not_refute(self):
        x = base(); x["sample_n"] = 58926
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertEqual(out["qualification_reason"], "INSUFFICIENT_SAMPLE")

    def test_required_n_does_not_auto_support(self):
        x = base(); x.update(m05_ci_lower=4.0, m05_ci_upper=6.0)
        out = DR.evaluate(x)
        self.assertNotEqual(out["evidence_verdict"], "SUPPORT")

    def test_unresolved_nonstationarity_is_inconclusive(self):
        x = base(); x.update(stationarity_status="UNRESOLVED_NONSTATIONARY", m05_interval_available=False, m05_ci_lower=None, m05_ci_upper=None)
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("NONSTATIONARITY_UNRESOLVED", out["all_qualification_reasons"])

    def test_m07_material_influence_vetoes_support(self):
        x = base(); x["m07_material_influence"] = True
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("MATERIAL_INFLUENCE", out["all_qualification_reasons"])

    def test_m07_sign_reversal_vetoes_support(self):
        x = base(); x["m07_sign_reversal"] = True
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("SIGN_REVERSAL", out["all_qualification_reasons"])

    def test_m08_asymmetry_vetoes_support(self):
        x = base(); x["m08_material_selection_asymmetry"] = True
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("MATERIAL_SELECTION_ASYMMETRY", out["all_qualification_reasons"])

    def test_cost_inconclusive_is_inconclusive(self):
        x = base(); x["f2_s4_status"] = "COST_ROBUSTNESS_INCONCLUSIVE"
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")

    def test_support_vs_cost_fail_is_conflict_not_refute(self):
        x = base(); x["f2_s4_status"] = "COST_ROBUSTNESS_FAIL"
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("EVIDENCE_CONFLICT_M05_SUPPORT_VS_COST_ROBUSTNESS_FAIL", out["all_qualification_reasons"])

    def test_refute_vs_cost_pass_is_conflict_not_refute(self):
        x = base(); x.update(m05_ci_lower=1.0, m05_ci_upper=5.0)
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("EVIDENCE_CONFLICT_M05_REFUTE_VS_COST_ROBUSTNESS_PASS", out["all_qualification_reasons"])

    def test_old_oos_route_is_blocked(self):
        x = base(); x["confirmatory_route"] = "OLD_E1_OOS"
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("PROVENANCE_ROUTE_INVALID", out["all_qualification_reasons"])

    def test_invented_n_trials_is_blocked(self):
        x = base(); x["n_trials"] = 1
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("PROVENANCE_BINDING_MISMATCH", out["all_qualification_reasons"])

    def test_search_universe_cannot_be_relabelled(self):
        x = base(); x["search_universe_status"] = "KNOWN_SEARCH_UNIVERSE"
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")

    def test_partial_search_is_preserved_as_limitation(self):
        out = DR.evaluate(base())
        self.assertIn("N_TRIALS_UNKNOWN", out["qualification_limitations"])
        self.assertIn("ALPHA_NOT_MULTIPLICITY_CORRECTED", out["qualification_limitations"])
        self.assertIn("HYPOTHESIS_ORIGIN_NOT_PRISTINE", out["qualification_limitations"])

    def test_multiple_failures_are_all_preserved(self):
        x = base()
        x.update(sample_n=58926, m07_material_influence=True, m08_material_selection_asymmetry=True)
        out = DR.evaluate(x)
        reasons = set(out["all_qualification_reasons"])
        self.assertTrue({"INSUFFICIENT_SAMPLE", "MATERIAL_INFLUENCE", "MATERIAL_SELECTION_ASYMMETRY"}.issubset(reasons))

    def test_invalid_interval_blocks_inference(self):
        x = base(); x.update(m05_ci_lower=8.0, m05_ci_upper=6.0)
        out = DR.evaluate(x)
        self.assertEqual(out["evidence_verdict"], "INCONCLUSIVE")
        self.assertIn("INFERENCE_BLOCKED", out["all_qualification_reasons"])

if __name__ == "__main__":
    unittest.main()
