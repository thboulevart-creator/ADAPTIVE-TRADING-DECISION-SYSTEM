import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_CASES = [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
]

EXPECTED_BASE_BREAKERS = [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
]

EXPECTED_CLOSURE_BREAKERS = [
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
    "CADENCE_GAP_ACCEPTED",
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
    "READ_COMPLETION_LATENCY_HIDDEN",
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED",
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def observation(scheduled, completed, outcome, observed_head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": observed_head,
    }


class TestP5EExternalReviewTargetedClosureV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_json(CONTRACT)

    def test_b1_required_lists_are_exactly_frozen(self):
        self.assertEqual(self.contract["required_synthetic_cases"], EXPECTED_CASES)
        self.assertEqual(self.contract["required_breakers"], EXPECTED_BASE_BREAKERS)
        self.assertEqual(
            self.contract["external_review_targeted_closure"]["required_breakers"],
            EXPECTED_CLOSURE_BREAKERS,
        )

    def test_b1_adversarial_invariants_reject_previously_surviving_mutations(self):
        adv = load_module(ADV, "p5e_adv_for_closure")
        mutations = [
            lambda c: c["head_transition_policy"].__setitem__(
                "non_fast_forward_result", "AUTO_CONTINUE"
            ),
            lambda c: c["head_transition_policy"].__setitem__(
                "unknown_ancestry_auto_continue_forbidden", False
            ),
            lambda c: c["head_transition_policy"].__setitem__(
                "same_head_queue_growth_forbidden", False
            ),
            lambda c: c["queue_and_supersession"].__setitem__(
                "capacity_exhausted_must_not_mutate_p5d2_state", False
            ),
            lambda c: c["synthetic_timing_model"].__setitem__(
                "clock_source", "WALL_CLOCK"
            ),
            lambda c: c["authority_boundary"].__setitem__(
                "observer_may_create_governance_authority", True
            ),
            lambda c: c["next_gate_after_candidate_qualification"].__setitem__(
                "p6_remains_closed", False
            ),
            lambda c: c.__setitem__(
                "required_breakers", [f"FAKE_{i}" for i in range(25)]
            ),
        ]
        for mutator in mutations:
            candidate = copy.deepcopy(self.contract)
            mutator(candidate)
            with self.assertRaises(AssertionError):
                adv.assert_contract_invariants(candidate)

    def test_b4_contract_uses_falsifiable_local_monotonic_measurement(self):
        timing = self.contract["near_real_time_timing"]
        self.assertEqual(
            timing["real_measurement_origin"],
            "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )
        self.assertEqual(
            timing["measurement_endpoint"],
            "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        )
        self.assertEqual(timing["schedule_semantics"], "FIXED_RATE")
        self.assertFalse(
            timing["remote_head_available_time_is_measurable_origin"]
        )
        self.assertEqual(
            timing["real_latency_metric"],
            "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )

    def test_b5_contract_distinguishes_observed_tip_from_intermediate_commit(self):
        tip = self.contract["tip_visibility_semantics"]
        self.assertEqual(
            tip["observed_remote_tip_definition"],
            "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
        )
        self.assertEqual(
            tip["intermediate_fast_forward_commit_definition"],
            "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
        )
        self.assertFalse(tip["unobserved_intermediate_tip_may_be_claimed_observed"])
        self.assertFalse(tip["unobserved_intermediate_tip_may_be_queued"])
        self.assertFalse(tip["per_transient_tip_detection_sla_authorized"])
        self.assertTrue(tip["already_observed_queued_head_retarget_forbidden"])

    def test_b2_skipped_first_required_slot_blocks(self):
        m = load_module(MODEL, "p5e_model_b2_first")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "SKIPPED_REQUIRED_ATTEMPT")

    def test_b2_cadence_gap_blocks(self):
        m = load_module(MODEL, "p5e_model_b2_gap")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(90, 91, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "CADENCE_GAP")

    def test_b3_pre_source_target_observation_blocks(self):
        m = load_module(MODEL, "p5e_model_b3")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=45,
            target_head=TARGET,
            observations=[
                observation(30, 31, "REMOTE_HEAD_OBSERVED", TARGET),
                observation(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE",
        )

    def test_b4_read_completion_not_poll_start_controls_latency(self):
        m = load_module(MODEL, "p5e_model_b4_duration")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )
        self.assertEqual(result["detection_latency_seconds"], 61)
        self.assertEqual(result["first_detection_completed_at_seconds"], 62)

    def test_non_aligned_source_failure_window_becomes_fail_when_future_slot_cannot_meet_bound(self):
        m = load_module(MODEL, "p5e_model_no_future")
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                observation(30, 31, "READ_FAILURE"),
                observation(60, 60, "READ_FAILURE"),
            ],
        )
        self.assertEqual(result["status"], "FAIL_NO_DETECTION_BY_BOUND")
        self.assertEqual(result["failure_code"], "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND")

    def test_b5_observation_requires_head_identity(self):
        m = load_module(MODEL, "p5e_model_b5_identity")
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=[
                    observation(30, 31, "REMOTE_HEAD_OBSERVED", None),
                ],
            )

    def test_b5_exact_and_contained_tip_classifications_are_distinct(self):
        m = load_module(MODEL, "p5e_model_b5_visibility")
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=TARGET,
                fast_forward_contains_target=False,
            ),
            "EXACT_TIP_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=True,
            ),
            "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=False,
            ),
            "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION",
        )

    def test_synthetic_model_imports_are_ast_allowlisted(self):
        import ast

        tree = ast.parse(MODEL.read_text(encoding="utf-8"))
        allowed = {"__future__", "typing"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)


if __name__ == "__main__":
    unittest.main()
