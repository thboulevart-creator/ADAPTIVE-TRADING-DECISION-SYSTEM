import copy
import importlib.util
import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"
PREREG = ROOT / "tools" / "obsidian_projection" / "p5e_bb1_normative_guard_closure_preregistration_v0_1.json"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_path(obj, dotted):
    cur = obj
    for key in dotted.split("."):
        cur = cur[key]
    return cur


def set_path(obj, dotted, value):
    parts = dotted.split(".")
    cur = obj
    for key in parts[:-1]:
        cur = cur[key]
    cur[parts[-1]] = value


def mutate(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return "MUTATED"
    if isinstance(value, list):
        return value[:-1] if value else ["MUTATED"]
    raise AssertionError(f"unsupported normative leaf type: {type(value)}")


def git_blob(path):
    relative = path.relative_to(ROOT).as_posix()
    return subprocess.check_output(
        ["git", "hash-object", f"--path={relative}", str(path)],
        cwd=ROOT,
        text=True,
    ).strip()


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


class TestP5EBB1NormativeGuardClosureV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_json(CONTRACT)
        self.prereg = load_json(PREREG)
        self.adv = load_module(ADV, "p5e_adv_bb1_closure")

    def test_preregistration_freezes_exact_leaf_sets(self):
        self.assertEqual(self.prereg["status"], "PREREGISTERED_BEFORE_RED")
        self.assertEqual(len(self.prereg["normative_leaf_set"]), 23)
        self.assertEqual(len(self.prereg["non_normative_metadata_set"]), 13)
        self.assertEqual(
            self.prereg["mutation_sweep_contract"]["exit_criterion"],
            "NORMATIVE_LEAF_MUTATIONS_SURVIVING_EQUALS_ZERO",
        )
        self.assertFalse(self.prereg["real_p5e_execution_authorized"])

    def test_all_preregistered_normative_leaf_mutations_are_rejected(self):
        survivors = []
        for dotted in self.prereg["normative_leaf_set"]:
            candidate = copy.deepcopy(self.contract)
            original = get_path(candidate, dotted)
            set_path(candidate, dotted, mutate(original))
            try:
                self.adv.assert_contract_invariants(candidate)
            except AssertionError:
                continue
            survivors.append(dotted)
        self.assertEqual(
            survivors,
            [],
            "normative mutations survived: " + ", ".join(survivors),
        )
    def test_combined_bb1_regression_is_rejected(self):
        candidate = copy.deepcopy(self.contract)
        changes = {
            "near_real_time_timing.detection_latency_definition":
                "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
            "near_real_time_timing.future_real_bound_clock": "WALL_CLOCK",
            "near_real_time_timing.future_real_wall_clock_may_be_recorded_as_evidence_only": False,
            "near_real_time_timing.latency_bound_breach_must_not_be_reported_as_near_real_time_pass": False,
            "monitored_source.branch": "main",
            "queue_and_supersession.burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": False,
        }
        for dotted, value in changes.items():
            set_path(candidate, dotted, value)
        with self.assertRaises(AssertionError):
            self.adv.assert_contract_invariants(candidate)

    def test_matrix_binds_exact_contract_and_model_blobs(self):
        matrix = load_json(MATRIX)
        self.assertEqual(matrix["covered_contract_blob"], git_blob(CONTRACT))
        self.assertEqual(matrix["covered_model_blob"], git_blob(MODEL))
        self.assertTrue(matrix["covered_object_drift_must_fail"])

    def test_nb1_read_overrun_of_next_required_slot_blocks(self):
        model = load_module(MODEL, "p5e_model_bb1_nb1")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 61, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
        )

    def test_nb4_contract_marks_non_injection_as_future_adapter_rule_only(self):
        tips = self.contract["tip_visibility_semantics"]
        self.assertTrue(
            tips["unobserved_intermediate_tip_non_injection_is_future_adapter_rule"]
        )
        self.assertFalse(
            tips["unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property"]
        )

    def test_nb6_matrix_uses_behavioral_queue_capacity_evidence(self):
        matrix = load_json(MATRIX)
        for key in (
            "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
            "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
        ):
            entry = matrix["base_breakers"][key]
            self.assertEqual(
                entry["path"],
                "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
            )
            self.assertEqual(
                entry["test_method"],
                "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
            )
            self.assertEqual(
                entry["evidence_kind"],
                "REUSED_QUALIFIED_P5D2_P5D4",
            )

    def test_nb6_pending_non_active_mapping_is_semantically_exact(self):
        matrix = load_json(MATRIX)
        for key in (
            "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
            "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
        ):
            section = (
                matrix["required_synthetic_cases"]
                if key in matrix["required_synthetic_cases"]
                else matrix["base_breakers"]
            )
            entry = section[key]
            self.assertEqual(
                entry["test_method"],
                "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
            )
            self.assertEqual(
                entry["evidence_kind"],
                "REUSED_QUALIFIED_P5D2_P5D4",
            )
    def test_nb7_incomplete_window_is_explicit_non_pass(self):
        synthetic = self.contract["synthetic_timing_model"]
        self.assertIn(
            "INCOMPLETE_SYNTHETIC_WINDOW",
            synthetic["explicit_non_pass_statuses"],
        )

    def test_nb7_duplicate_slot_has_distinct_failure_code(self):
        model = load_module(MODEL, "p5e_model_bb1_nb7")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 30, "READ_FAILURE"),
                obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "DUPLICATE_FIXED_RATE_SLOT")


if __name__ == "__main__":
    unittest.main()
