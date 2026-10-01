import ast
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"

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


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model_adv", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
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


def assert_contract_invariants(contract):
    assert contract["schema"] == "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1"
    assert contract["status"] == "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW"
    assert contract["qualification_stage"] == "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY"
    assert contract["real_p5e_execution_authorized"] is False

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True
    assert timing["real_measurement_origin"] == "CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    assert timing["measurement_endpoint"] == "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC"
    assert timing["schedule_semantics"] == "FIXED_RATE"
    assert timing["future_real_poll_schedule_semantics"] == "FIXED_RATE_30_SECOND_GRID"
    assert timing["remote_head_available_time_is_measurable_origin"] is False
    assert timing["attempt_start_and_read_completion_are_distinct"] is True
    assert timing["read_duration_is_included_in_detection_latency"] is True
    assert timing["eligible_detection_attempt_must_start_at_or_after_release"] is True
    assert timing["single_transient_read_failure_may_still_meet_60_second_bound"] is False
    assert timing[
        "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds"
    ] is True

    synthetic = contract["synthetic_timing_model"]
    assert synthetic["clock_source"] == "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY"
    assert synthetic["schedule_semantics"] == "FIXED_RATE"
    assert synthetic["schedule_origin_seconds"] == 0
    assert synthetic["sleep_forbidden"] is True
    assert synthetic["network_forbidden"] is True
    assert synthetic["filesystem_state_forbidden"] is True
    assert synthetic["process_launch_forbidden"] is True
    assert synthetic["environment_read_forbidden"] is True
    assert synthetic["real_p5d4_control_state_access_forbidden"] is True
    assert synthetic["real_vault_access_forbidden"] is True
    assert synthetic["head_identity_required_on_successful_remote_observation"] is True
    assert synthetic["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    transition = contract["head_transition_policy"]
    assert transition["same_head_result"] == "NOOP"
    assert transition["same_head_queue_growth_forbidden"] is True
    assert transition["non_fast_forward_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["non_fast_forward_auto_continue_forbidden"] is True
    assert transition["unknown_ancestry_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["unknown_ancestry_auto_continue_forbidden"] is True
    assert transition["active_or_pending_candidate_retarget_forbidden"] is True

    queue = contract["queue_and_supersession"]
    assert queue["fifo_required"] is True
    assert queue["unique_heads_required"] is True
    assert queue["silent_drop_forbidden"] is True
    assert queue["silent_reorder_forbidden"] is True
    assert queue["latest_only_replacement_forbidden"] is True
    assert queue["coalescing_authorized"] is False
    assert queue["new_coalescing_semantic_event_authorized"] is False
    assert queue["pending_head_retarget_forbidden"] is True
    assert queue["capacity_exhausted_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert queue["capacity_exhausted_must_not_mutate_p5d2_state"] is True
    assert queue["precedence_rule"] == (
        "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_"
        "EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT"
    )

    failure = contract["failure_and_freshness"]
    assert failure["fail_closed_default"] is True
    assert failure["network_failure_must_not_create_current_claim"] is True
    assert failure["last_known_good_live_projection_preserved"] is True
    assert failure["latency_bound_breach_result"] == "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED"
    assert failure["queue_capacity_exhaustion_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert failure["non_fast_forward_or_unknown_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["unexpected_state_or_timing_ambiguity_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["timing_inconsistency_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    authority = contract["authority_boundary"]
    for field in (
        "observer_may_create_governance_authority",
        "pending_head_evaluation_authorized",
        "evaluation_authorized",
        "stage_a_authorized",
        "stage_b_authorized",
        "promotion_authorized",
        "publication_authorized",
        "real_vault_mutation_authorized",
        "current_mutation_authorized",
        "current_tmp_mutation_authorized",
        "real_polling_loop_authorized",
        "daemon_authorized",
        "startup_registration_authorized",
        "scheduled_task_authorized",
        "windows_service_authorized",
        "p6_authorized",
    ):
        assert authority[field] is False

    tips = contract["tip_visibility_semantics"]
    assert tips["observed_remote_tip_definition"] == "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ"
    assert tips["unobserved_intermediate_tip_may_be_claimed_observed"] is False
    assert tips["unobserved_intermediate_tip_may_be_queued"] is False
    assert tips["fast_forward_content_containment_is_queue_coalescing"] is False
    assert tips["already_observed_queued_head_replacement_forbidden"] is True
    assert tips["already_observed_queued_head_retarget_forbidden"] is True
    assert tips["per_transient_tip_detection_sla_authorized"] is False

    end_to_end = contract["end_to_end_definition"]
    assert end_to_end["current_stage_may_qualify_only"] == [
        "TIMING_CONTRACT",
        "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
        "AUTHORITY_BOUNDARIES",
        "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR",
    ]
    assert end_to_end["omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass"] is True
    assert end_to_end["transient_tip_exact_detection_sla_not_qualified"] is True
    assert end_to_end["real_remote_availability_to_detection_sla_not_qualified"] is True

    claims = contract["claim_boundary"]
    assert claims["maximum_current_claim"] == (
        "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW"
    )
    assert claims["real_end_to_end_qualification_requires_separate_authorization"] is True
    forbidden = set(claims["forbidden_current_claims"])
    for claim in (
        "P5E_REAL_END_TO_END_QUALIFIED",
        "REAL_60_SECOND_SLA_QUALIFIED",
        "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
        "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
        "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED",
    ):
        assert claim in forbidden

    gate = contract["next_gate_after_candidate_qualification"]
    assert gate["external_adversarial_review_required_before_normative_adoption"] is True
    assert gate["human_adjudication_required_after_external_review"] is True
    assert gate["p6_remains_closed"] is True
    assert gate["real_p5e_execution_requires_separate_human_authorization"] is True
    assert gate["external_adversarial_rereview_required"] is True
    assert gate["human_adjudication_before_external_rereview_forbidden"] is True

    assert contract["required_synthetic_cases"] == EXPECTED_CASES
    assert contract["required_breakers"] == EXPECTED_BASE_BREAKERS
    closure = contract["external_review_targeted_closure"]
    assert closure["required_breakers"] == EXPECTED_CLOSURE_BREAKERS
    assert closure["requirement_to_executable_evidence_matrix_required"] is True
    assert closure["all_required_cases_must_be_mapped"] is True
    assert closure["all_base_breakers_must_be_mapped"] is True
    assert closure["all_targeted_closure_breakers_must_be_mapped"] is True
    assert closure["unmapped_requirement_result"] == "BLOCKED"


class TestP5EAdversarialV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        assert_contract_invariants(self.contract)

    def assert_mutation_rejected(self, mutator):
        candidate = copy.deepcopy(self.contract)
        mutator(candidate)
        with self.assertRaises(AssertionError):
            assert_contract_invariants(candidate)

    def test_timing_mutations_are_rejected(self):
        mutations = [
            lambda c: c["near_real_time_timing"].__setitem__("poll_interval_seconds", 31),
            lambda c: c["near_real_time_timing"].__setitem__("detection_latency_seconds_max", 61),
            lambda c: c["near_real_time_timing"].__setitem__("instantaneous_realtime_claim_forbidden", False),
            lambda c: c["near_real_time_timing"].__setitem__("schedule_semantics", "FIXED_DELAY"),
            lambda c: c["near_real_time_timing"].__setitem__("remote_head_available_time_is_measurable_origin", True),
            lambda c: c["near_real_time_timing"].__setitem__("read_duration_is_included_in_detection_latency", False),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_previously_surviving_contract_mutations_are_rejected(self):
        mutations = [
            lambda c: c["head_transition_policy"].__setitem__("non_fast_forward_result", "AUTO_CONTINUE"),
            lambda c: c["head_transition_policy"].__setitem__("unknown_ancestry_auto_continue_forbidden", False),
            lambda c: c["head_transition_policy"].__setitem__("same_head_queue_growth_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_must_not_mutate_p5d2_state", False),
            lambda c: c["synthetic_timing_model"].__setitem__("clock_source", "WALL_CLOCK"),
            lambda c: c["authority_boundary"].__setitem__("observer_may_create_governance_authority", True),
            lambda c: c["next_gate_after_candidate_qualification"].__setitem__("p6_remains_closed", False),
            lambda c: c.__setitem__("required_breakers", [f"FAKE_{i}" for i in range(25)]),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_authority_mutations_are_rejected(self):
        for field in (
            "evaluation_authorized",
            "promotion_authorized",
            "publication_authorized",
            "real_vault_mutation_authorized",
            "real_polling_loop_authorized",
            "daemon_authorized",
            "startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p6_authorized",
        ):
            self.assert_mutation_rejected(
                lambda c, field=field: c["authority_boundary"].__setitem__(field, True)
            )

    def test_queue_mutations_are_rejected(self):
        mutations = [
            lambda c: c["queue_and_supersession"].__setitem__("coalescing_authorized", True),
            lambda c: c["queue_and_supersession"].__setitem__("latest_only_replacement_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("pending_head_retarget_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_result", "CONTINUE"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_claim_and_tip_mutations_are_rejected(self):
        mutations = [
            lambda c: c["claim_boundary"].__setitem__("maximum_current_claim", "P5E_REAL_END_TO_END_QUALIFIED"),
            lambda c: c["tip_visibility_semantics"].__setitem__("unobserved_intermediate_tip_may_be_claimed_observed", True),
            lambda c: c["tip_visibility_semantics"].__setitem__("per_transient_tip_detection_sla_authorized", True),
            lambda c: c["end_to_end_definition"]["current_stage_may_qualify_only"].append("REAL_END_TO_END"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_required_lists_cannot_be_reduced_or_replaced(self):
        self.assert_mutation_rejected(
            lambda c: c.__setitem__("required_synthetic_cases", ["SAME_HEAD_NOOP"])
        )
        self.assert_mutation_rejected(
            lambda c: c["external_review_targeted_closure"].__setitem__(
                "required_breakers", ["FAKE"]
            )
        )

    def test_synthetic_model_imports_are_ast_allowlisted(self):
        tree = ast.parse(MODEL.read_text(encoding="utf-8"))
        allowed = {"__future__", "typing"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)

    def test_exact_60_second_completion_boundary_passes(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=0,
            target_head=TARGET,
            observations=[
                obs(30, 30, "READ_FAILURE"),
                obs(60, 60, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_pre_source_target_observation_blocks(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=45,
            target_head=TARGET,
            observations=[
                obs(30, 31, "REMOTE_HEAD_OBSERVED", TARGET),
                obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE",
        )

    def test_invalid_source_release_values_are_rejected(self):
        m = load_model()
        for value in (-1, True):
            with self.assertRaises(m.P5ETimingModelError):
                m.qualify_detection(
                    plan=m.make_timing_plan(),
                    source_release_at_seconds=value,
                    target_head=TARGET,
                    observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
                )

    def test_empty_observation_list_is_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[],
            )

    def test_invalid_observation_shape_and_head_are_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", None)],
            )
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "PROMOTE", None)],
            )

    def test_cadence_duplicate_and_gap_are_blocked(self):
        m = load_model()
        for observations, code in (
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "CADENCE_GAP",
            ),
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(90, 90, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "CADENCE_GAP",
            ),
        ):
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(result["failure_code"], code)

    def test_attempt_overlap_is_blocked(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 61, "READ_FAILURE"),
                obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OVERLAP")

    def test_incomplete_window_does_not_claim_pass(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 31, "READ_FAILURE")],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertFalse(result["real_end_to_end_qualified"])
        self.assertFalse(result["continuous_synchronization_qualified"])

    def test_all_result_paths_keep_downstream_authority_false(self):
        m = load_model()
        cases = [
            [obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(30, 31, "READ_FAILURE"), obs(60, 60, "READ_FAILURE")],
            [obs(30, 31, "READ_FAILURE"), obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET)],
        ]
        for observations in cases:
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertFalse(result["automatic_evaluation_authorized"])
            self.assertFalse(result["automatic_promotion_authorized"])
            self.assertFalse(result["automatic_publication_authorized"])

    def test_tip_visibility_does_not_launder_containment_into_exact_observation(self):
        m = load_model()
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


if __name__ == "__main__":
    unittest.main()
