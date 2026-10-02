import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40
D2_METHOD = "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


class TestP5EFinalPreAdoptionEvidenceHygieneV01(unittest.TestCase):
    def test_n1_contract_explicitly_forbids_completion_before_attempt_start(self):
        contract = load_json(CONTRACT)
        synthetic = contract["synthetic_timing_model"]
        self.assertTrue(
            synthetic["read_completion_before_attempt_start_forbidden"]
        )

    def test_n1_behavior_blocks_completion_before_attempt_start(self):
        model = load_module(MODEL, "p5e_final_hygiene_n1_model")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(60, 40, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "READ_COMPLETION_PRECEDES_ATTEMPT_START",
        )

    def test_n1_contract_field_is_strictly_guarded(self):
        contract = load_json(CONTRACT)
        candidate = copy.deepcopy(contract)
        candidate["synthetic_timing_model"][
            "read_completion_before_attempt_start_forbidden"
        ] = False
        adv = load_module(ADV, "p5e_final_hygiene_n1_adv")
        with self.assertRaises(AssertionError):
            adv.assert_contract_invariants(candidate)

    def test_n2_new_d2_file_test_is_labelled_direct_p5e(self):
        matrix = load_json(MATRIX)
        entries = [
            matrix["required_synthetic_cases"][
                "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
            ],
            matrix["base_breakers"][
                "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD"
            ],
        ]
        for entry in entries:
            self.assertEqual(entry["test_method"], D2_METHOD)
            self.assertEqual(entry["evidence_kind"], "DIRECT_P5E")

    def test_n6_stale_built_against_head_is_absent(self):
        matrix = load_json(MATRIX)
        self.assertNotIn("built_against_head", matrix)

    def test_n6_object_blobs_remain_the_binding_authority(self):
        matrix = load_json(MATRIX)
        self.assertTrue(matrix["covered_object_drift_must_fail"])
        self.assertRegex(matrix["covered_contract_blob"], r"^[0-9a-f]{40}$")
        self.assertRegex(matrix["covered_model_blob"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
