from __future__ import annotations
import importlib.util
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = json.loads((ROOT / "GOVERNANCE" / "AO-E0-B8-M06-02-SAMPLE-ADEQUACY-PREREGISTRATION-CANDIDATE-V0.1.json").read_text())
SPEC = importlib.util.spec_from_file_location("m06_runtime", ROOT / "tools" / "smf03_dependence_inference.py")
M06 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M06)

class TestM0602(unittest.TestCase):
    def test_candidate_exact_values(self):
        p = CONTRACT["precision"]; w = CONTRACT["power"]
        self.assertEqual(CONTRACT["sample_adequacy_rule"]["mode"], "PRECISION_AND_POWER")
        self.assertEqual(p["required_n"], 30036)
        self.assertEqual(w["required_n"], 58927)
        self.assertEqual(CONTRACT["final_required_n"], 58927)
        self.assertEqual(w["alternative"], "GREATER")
        self.assertEqual(w["effect_source"], "PREDECLARED")

    def test_runtime_exact_candidate(self):
        p = M06.required_n_for_mean_precision(
            model_ref="NORMAL_MEAN_KNOWN_SIGMA", stddev=336.4106561689863,
            half_width=5.0, confidence_level=0.99)
        w = M06.required_n_for_mean_power(
            model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=5.0,
            stddev=336.4106561689863, alpha=0.01, target_power=0.90,
            alternative="GREATER", effect_source="PREDECLARED", max_n=58927)
        self.assertEqual(p["required_n"], 30036)
        self.assertEqual(w["required_n"], 58927)
        self.assertTrue(w["achieved_power"] >= 0.90)

    def test_unsupported_model_substitution(self):
        with self.assertRaisesRegex(ValueError, "PRECISION_MODEL_UNSUPPORTED"):
            M06.required_n_for_mean_precision(model_ref="AUTO", stddev=1, half_width=1, confidence_level=.95)

    def test_missing_confidence_rejected(self):
        with self.assertRaises((TypeError, ValueError)):
            M06.required_n_for_mean_precision(model_ref="NORMAL_MEAN_KNOWN_SIGMA", stddev=1, half_width=1, confidence_level=None)

    def test_invalid_half_width_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_HALF_WIDTH"):
            M06.required_n_for_mean_precision(model_ref="NORMAL_MEAN_KNOWN_SIGMA", stddev=1, half_width=0, confidence_level=.95)

    def test_invalid_alpha_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_ALPHA"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=1, stddev=1, alpha=1, target_power=.9, alternative="GREATER", effect_source="PREDECLARED", max_n=10)

    def test_invalid_target_power_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_TARGET_POWER"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=1, stddev=1, alpha=.01, target_power=1, alternative="GREATER", effect_source="PREDECLARED", max_n=10)

    def test_zero_effect_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_EFFECT_SIZE"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=0, stddev=1, alpha=.01, target_power=.9, alternative="GREATER", effect_source="PREDECLARED", max_n=10)

    def test_effect_direction_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError, "EFFECT_DIRECTION_MISMATCH"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=-1, stddev=1, alpha=.01, target_power=.9, alternative="GREATER", effect_source="PREDECLARED", max_n=10)

    def test_non_predeclared_effect_source_rejected(self):
        with self.assertRaisesRegex(ValueError, "POST_HOC_POWER_FORBIDDEN"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=1, stddev=1, alpha=.01, target_power=.9, alternative="GREATER", effect_source="OBSERVED", max_n=10)

    def test_invalid_max_n_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_MAX_N"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=1, stddev=1, alpha=.01, target_power=.9, alternative="GREATER", effect_source="PREDECLARED", max_n=0)

    def test_n_minus_one_is_unreachable(self):
        with self.assertRaisesRegex(ValueError, "TARGET_POWER_UNREACHABLE_WITHIN_MAX_N"):
            M06.required_n_for_mean_power(model_ref="NORMAL_MEAN_KNOWN_SIGMA", effect_size=5.0, stddev=336.4106561689863, alpha=.01, target_power=.90, alternative="GREATER", effect_source="PREDECLARED", max_n=58926)

    def test_no_exposed_result_tuning(self):
        c = CONTRACT["parameter_source_controls"]
        self.assertFalse(c["new_real_result_used"])
        self.assertFalse(c["exposed_e1_performance_used_for_parameter_selection"])
        self.assertTrue(c["exposed_e1_use_limited_to_adopted_planning_sigma"])

    def test_epistemic_firewalls(self):
        self.assertTrue(all(CONTRACT["epistemic_firewalls"].values()))
        self.assertEqual(CONTRACT["dependence_routing"]["m06_required_n_interpretation"], "NOMINAL_MODEL_BASED_PLANNING_COUNT_ONLY")

    def test_combination_rule_is_explicit(self):
        self.assertEqual(CONTRACT["sample_adequacy_rule"]["combination_rule"], "FINAL_REQUIRED_N = MAX(PRECISION_REQUIRED_N, POWER_REQUIRED_N)")

    def test_no_parameter_optimization_or_execution_authority(self):
        self.assertFalse(CONTRACT["parameter_source_controls"]["post_hoc_parameter_tuning"])
        self.assertTrue(all(v is False for v in CONTRACT["authority"].values()))

    def test_b8_and_b12_stay_closed_to_execution(self):
        self.assertEqual(CONTRACT["state"]["b8"], "BLOCKED_PENDING_DISTINCT_HUMAN_ADOPTION")
        self.assertEqual(CONTRACT["state"]["b12"], "CLOSED")

if __name__ == "__main__":
    unittest.main()
