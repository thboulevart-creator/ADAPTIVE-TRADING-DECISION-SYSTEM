import importlib.util
import inspect
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
PREREG = ROOT / "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json"
SCHEMA = ROOT / "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json"
GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
SYNTH = ROOT / "tools/obsidian_projection/p5e_near_real_time_model.py"
A = "a" * 40


def load(path, name):
    if not path.exists():
        raise AssertionError(f"required module missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
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


class TestRPE02RealTimeRepresentationV01(unittest.TestCase):
    def test_preregistration_is_rpe01_guarded(self):
        g = load(GUARD, "rpe01_guard_for_rpe02")
        doc = g.validate_governed_json(
            PREREG.read_text(encoding="utf-8"),
            SCHEMA.read_text(encoding="utf-8"),
        )
        self.assertEqual(doc["architecture"]["selected"], "SEPARATE_REAL_TIME_MODEL_V0_2")

    def test_exact_nanosecond_plan(self):
        m = load(MODULE, "rpe02")
        plan = m.make_real_time_plan(schedule_origin_ns=0)
        self.assertEqual(plan["poll_interval_ns"], 30_000_000_000)
        self.assertEqual(plan["detection_latency_bound_ns"], 60_000_000_000)
        self.assertEqual(plan["normative_unit"], "INTEGER_MONOTONIC_NANOSECONDS")

    def test_strict_integer_timestamps(self):
        m = load(MODULE, "rpe02_int")
        for value in (0.0, True, "0", None):
            with self.subTest(value=value):
                with self.assertRaises(m.RPE02TimingError):
                    m.make_real_time_plan(schedule_origin_ns=value)

    def test_release_must_be_after_origin(self):
        m = load(MODULE, "rpe02_release")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        with self.assertRaises(m.RPE02TimingError):
            m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=0, target_head=A, observations=[obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)])

    def test_exact_60_second_latency_passes(self):
        m = load(MODULE, "rpe02_bound")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(
            plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
                obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000,"REMOTE_HEAD_OBSERVED",A),
            ])
        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(r["detection_latency_ns"], 60_000_000_000)

    def test_latency_one_nanosecond_over_bound_fails(self):
        m = load(MODULE, "rpe02_over")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(
            plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
                obs(90_000_000_000,90_000_000_000,90_000_000_001,90_000_000_001,"REMOTE_HEAD_OBSERVED",A),
            ])
        self.assertEqual(r["status"], "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED")
        self.assertEqual(r["detection_latency_ns"], 60_000_000_001)

    def test_late_actual_start_cannot_hide_behind_slot(self):
        m = load(MODULE, "rpe02_late")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[obs(30_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["failure_code"], "ACTUAL_START_MISSED_FIXED_RATE_SLOT")

    def test_remote_completion_equal_next_slot_allowed(self):
        m = load(MODULE, "rpe02_equal_slot")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_000,60_000_000_000)])
        self.assertEqual(r["status"], "INCOMPLETE_REAL_TIME_WINDOW")

    def test_remote_completion_after_next_slot_blocked(self):
        m = load(MODULE, "rpe02_after_slot")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_001,60_000_000_001)])
        self.assertEqual(r["failure_code"], "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    def test_previous_completion_equal_next_start_allowed(self):
        m = load(MODULE, "rpe02_equal_overlap")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,40_000_000_000,60_000_000_000),
                obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")

    def test_previous_completion_greater_next_start_blocked(self):
        m = load(MODULE, "rpe02_overlap")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[
                obs(30_000_000_000,30_000_000_000,40_000_000_000,60_000_000_001),
                obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["failure_code"], "ATTEMPT_OVERLAP")

    def test_pre_release_started_target_is_blocked(self):
        m = load(MODULE, "rpe02_pre")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=45_000_000_000, target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,45_000_000_000,45_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["failure_code"], "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT")

    def test_full_completion_does_not_replace_remote_latency_endpoint(self):
        m = load(MODULE, "rpe02_two_phase")
        p = m.make_real_time_plan(schedule_origin_ns=0)
        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
            observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,100_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(r["detection_latency_ns"], 1_000_000_000)
        self.assertEqual(r["first_detection_attempt_completed_at_ns"], 100_000_000_000)

    def test_release_ceiling_rule(self):
        m = load(MODULE, "rpe02_ceiling")
        self.assertEqual(m.first_fixed_rate_slot_at_or_after_ns(30_000_000_000,30_000_000_000,0),30_000_000_000)
        self.assertEqual(m.first_fixed_rate_slot_at_or_after_ns(30_000_000_001,30_000_000_000,0),60_000_000_000)

    def test_exact_grid_parity_with_synthetic_reference(self):
        m = load(MODULE, "rpe02_parity")
        s = load(SYNTH, "p5e_synthetic_reference")
        sp=s.make_timing_plan()
        sr=s.qualify_detection(plan=sp,source_release_at_seconds=30,target_head=A,observations=[
            {"scheduled_at_seconds":30,"completed_at_seconds":30,"outcome":"READ_FAILURE","observed_head":None},
            {"scheduled_at_seconds":60,"completed_at_seconds":90,"outcome":"REMOTE_HEAD_OBSERVED","observed_head":A}])
        rp=m.make_real_time_plan(schedule_origin_ns=0)
        rr=m.qualify_detection_ns(plan=rp,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,observations=[
            obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
            obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
        self.assertEqual(rr["status"],sr["status"])
        self.assertEqual(rr["detection_latency_ns"],sr["detection_latency_seconds"]*1_000_000_000)

    def test_clock_capability_evidence(self):
        m = load(MODULE, "rpe02_clock")
        e=m.capture_monotonic_clock_capability()
        self.assertTrue(e["monotonic"])
        self.assertIs(type(e["sample_1_ns"]),int)
        self.assertIs(type(e["sample_2_ns"]),int)
        self.assertGreaterEqual(e["sample_2_ns"],e["sample_1_ns"])
        self.assertTrue(e["same_process_host_domain"])

    def test_no_environment_or_cli_config_authority(self):
        source=MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""
        self.assertNotIn("argparse",source)
        self.assertNotIn("os.environ",source)
        self.assertNotIn("getenv(",source)
        self.assertNotIn("time.time(",source)


if __name__ == "__main__":
    unittest.main()
