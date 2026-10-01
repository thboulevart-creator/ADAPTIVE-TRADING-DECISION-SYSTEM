import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
PREREG = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_preregistration_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_PREDECESSORS = {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model", MODEL)
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


class TestP5EContractV01(unittest.TestCase):
    def test_preregistration_is_present_and_frozen_before_contract(self):
        p = load_json(PREREG)
        self.assertEqual(p["status"], "PREREGISTERED_BEFORE_RED")
        self.assertFalse(p["real_p5e_execution_authorized"])

    def test_contract_schema_stage_and_status_are_exact(self):
        c = load_json(CONTRACT)
        self.assertEqual(
            c["schema"],
            "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
        )
        self.assertEqual(
            c["qualification_stage"],
            "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
        )
        self.assertEqual(
            c["status"],
            "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
        )
        self.assertFalse(c["real_p5e_execution_authorized"])

    def test_all_predecessor_blobs_are_exact(self):
        c = load_json(CONTRACT)
        self.assertEqual(c["predecessors"], EXPECTED_PREDECESSORS)

    def test_timing_inheritance_remains_exact_30_and_60(self):
        t = load_json(CONTRACT)["near_real_time_timing"]
        self.assertEqual(t["poll_interval_seconds"], 30)
        self.assertEqual(t["detection_latency_seconds_max"], 60)
        self.assertTrue(t["instantaneous_realtime_claim_forbidden"])
        self.assertTrue(t["silent_interval_widening_forbidden"])
        self.assertTrue(t["silent_latency_bound_widening_forbidden"])

    def test_real_latency_metric_is_falsifiable_and_local_monotonic(self):
        t = load_json(CONTRACT)["near_real_time_timing"]
        self.assertEqual(
            t["real_measurement_origin"],
            "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        )
        self.assertEqual(
            t["measurement_endpoint"],
            "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        )
        self.assertEqual(t["schedule_semantics"], "FIXED_RATE")
        self.assertFalse(t["remote_head_available_time_is_measurable_origin"])
        self.assertTrue(t["attempt_start_and_read_completion_are_distinct"])
        self.assertTrue(t["read_duration_is_included_in_detection_latency"])
        self.assertTrue(
            t["eligible_detection_attempt_must_start_at_or_after_release"]
        )

    def test_contract_forbids_authority_expansion(self):
        a = load_json(CONTRACT)["authority_boundary"]
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
            self.assertFalse(a[field], field)

    def test_queue_conflict_resolves_in_favor_of_p5d4(self):
        q = load_json(CONTRACT)["queue_and_supersession"]
        self.assertTrue(q["fifo_required"])
        self.assertTrue(q["silent_drop_forbidden"])
        self.assertTrue(q["silent_reorder_forbidden"])
        self.assertTrue(q["latest_only_replacement_forbidden"])
        self.assertFalse(q["coalescing_authorized"])
        self.assertFalse(q["new_coalescing_semantic_event_authorized"])
        self.assertTrue(q["pending_head_retarget_forbidden"])
        self.assertTrue(q["capacity_exhausted_must_not_mutate_p5d2_state"])
        self.assertEqual(
            q["capacity_exhausted_result"],
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
        )

    def test_tip_visibility_does_not_claim_unobserved_tip_detection(self):
        t = load_json(CONTRACT)["tip_visibility_semantics"]
        self.assertFalse(t["unobserved_intermediate_tip_may_be_claimed_observed"])
        self.assertFalse(t["unobserved_intermediate_tip_may_be_queued"])
        self.assertFalse(t["fast_forward_content_containment_is_queue_coalescing"])
        self.assertTrue(t["already_observed_queued_head_replacement_forbidden"])
        self.assertTrue(t["already_observed_queued_head_retarget_forbidden"])
        self.assertFalse(t["per_transient_tip_detection_sla_authorized"])

    def test_claim_boundary_is_narrowed_pending_external_rereview(self):
        claims = load_json(CONTRACT)["claim_boundary"]
        self.assertEqual(
            claims["maximum_current_claim"],
            "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
        )
        self.assertTrue(
            claims["real_end_to_end_qualification_requires_separate_authorization"]
        )
        forbidden = set(claims["forbidden_current_claims"])
        for claim in (
            "P5E_REAL_END_TO_END_QUALIFIED",
            "REAL_60_SECOND_SLA_QUALIFIED",
            "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
            "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
            "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED",
        ):
            self.assertIn(claim, forbidden)

    def test_model_freezes_exact_plan(self):
        m = load_model()
        plan = m.make_timing_plan()
        self.assertEqual(plan["poll_interval_seconds"], 30)
        self.assertEqual(plan["detection_latency_seconds_max"], 60)
        self.assertEqual(plan["schedule_semantics"], "FIXED_RATE")
        self.assertEqual(plan["schedule_origin_seconds"], 0)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(poll_interval_seconds=31)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(detection_latency_seconds_max=61)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(schedule_origin_seconds=1)

    def test_change_just_after_poll_is_detected_at_next_slot_completion(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 31, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 30)
        self.assertEqual(result["first_detection_scheduled_at_seconds"], 30)
        self.assertEqual(result["first_detection_completed_at_seconds"], 31)
        self.assertFalse(result["real_end_to_end_qualified"])

    def test_one_transient_failure_can_pass_only_by_completion_within_60(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_read_completion_after_60_is_rejected(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(
            result["status"], "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
        )
        self.assertEqual(result["detection_latency_seconds"], 61)

    def test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 31, "READ_FAILURE"),
                obs(60, 60, "READ_FAILURE"),
            ],
        )
        self.assertEqual(result["status"], "FAIL_NO_DETECTION_BY_BOUND")
        self.assertEqual(
            result["failure_code"],
            "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
        )

    def test_off_grid_schedule_is_fail_closed(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(31, 32, "REMOTE_HEAD_OBSERVED", TARGET)],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OFF_FIXED_RATE_GRID")

    def test_tip_visibility_classification_is_explicit(self):
        m = load_model()
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


if __name__ == "__main__":
    unittest.main()
