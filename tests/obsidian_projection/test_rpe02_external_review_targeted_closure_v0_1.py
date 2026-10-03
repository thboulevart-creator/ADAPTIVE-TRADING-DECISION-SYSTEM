import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
A = "a" * 40


def load():
    spec = importlib.util.spec_from_file_location("rpe02_targeted", MODULE)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-02 module")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def obs(scheduled, started, remote_done, attempt_done, outcome="READ_FAILURE", head=None):
    return {
        "scheduled_at_ns": scheduled,
        "attempt_started_at_ns": started,
        "remote_observation_completed_at_ns": remote_done,
        "attempt_completed_at_ns": attempt_done,
        "outcome": outcome,
        "observed_head": head,
    }


class TestRPE02ExternalReviewTargetedClosureV01(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.plan = self.m.make_real_time_plan(schedule_origin_ns=0)

    def test_unknown_outcome_is_rejected_before_sla_verdict(self):
        with self.assertRaises(self.m.RPE02TimingError):
            self.m.qualify_detection_ns(
                plan=self.plan,
                controlled_source_release_started_at_ns=1_000_000_000,
                target_head=A,
                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"GARBAGE",A)],
            )

    def test_success_without_head_is_rejected_before_sla_verdict(self):
        with self.assertRaises(self.m.RPE02TimingError):
            self.m.qualify_detection_ns(
                plan=self.plan,
                controlled_source_release_started_at_ns=1_000_000_000,
                target_head=A,
                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"REMOTE_HEAD_OBSERVED",None)],
            )

    def test_failure_with_head_is_rejected_before_sla_verdict(self):
        with self.assertRaises(self.m.RPE02TimingError):
            self.m.qualify_detection_ns(
                plan=self.plan,
                controlled_source_release_started_at_ns=1_000_000_000,
                target_head=A,
                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"READ_FAILURE",A)],
            )

    def test_outcome_typo_with_target_head_is_rejected(self):
        with self.assertRaises(self.m.RPE02TimingError):
            self.m.qualify_detection_ns(
                plan=self.plan,
                controlled_source_release_started_at_ns=1_000_000_000,
                target_head=A,
                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"REMOTE_HEAD_OBSERVED ",A)],
            )

    def test_actual_start_after_release_is_eligible_even_if_slot_precedes_release(self):
        r = self.m.qualify_detection_ns(
            plan=self.plan,
            controlled_source_release_started_at_ns=30_500_000_000,
            target_head=A,
            observations=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)],
        )
        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(r["detection_latency_ns"], 1_500_000_000)

    def test_started_before_scheduled_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[obs(30_000_000_000,29_999_999_999,30_000_000_000,30_000_000_000)])
        self.assertEqual(r["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")

    def test_remote_completion_before_start_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,29_999_999_999,30_000_000_000)])
        self.assertEqual(r["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")

    def test_attempt_completion_before_remote_completion_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,30_999_999_999)])
        self.assertEqual(r["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")

    def test_duplicate_slot_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000)])
        self.assertEqual(r["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")

    def test_cadence_gap_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
                obs(90_000_000_000,90_000_000_000,90_000_000_000,90_000_000_000)])
        self.assertEqual(r["failure_code"],"CADENCE_GAP")

    def test_skipped_first_required_attempt_is_blocked(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
            observations=[obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000)])
        self.assertEqual(r["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")

    def test_supplied_out_of_order_observations_are_not_silently_sorted(self):
        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
            observations=[
                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)])
        self.assertEqual(r["status"],"BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(r["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

    def test_parity_infeasible_next_slot_fails_even_before_last_remote_reaches_bound(self):
        r=self.m.qualify_detection_ns(
            plan=self.plan,controlled_source_release_started_at_ns=1_000_000_000,target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000)])
        self.assertEqual(r["status"],"FAIL_NO_DETECTION_BY_BOUND")
        self.assertEqual(r["failure_code"],"NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND")

    def test_parity_next_slot_exactly_at_bound_is_incomplete_not_fail(self):
        r=self.m.qualify_detection_ns(
            plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
                obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000)])
        self.assertEqual(r["status"],"INCOMPLETE_REAL_TIME_WINDOW")
        self.assertIsNone(r["failure_code"])

    def test_nb4_scope_full_completion_does_not_replace_remote_latency_endpoint(self):
        r=self.m.qualify_detection_ns(
            plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_000,300_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["status"],"PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(r["detection_latency_ns"],30_000_000_000)


if __name__ == "__main__":
    unittest.main()
