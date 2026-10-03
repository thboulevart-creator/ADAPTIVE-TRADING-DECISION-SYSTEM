import json
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools" / "obsidian_projection" / "rpe02_real_time_model_v0_1.py"
A = "a" * 40


def load_source_module(name, replacements=()):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


def obs(scheduled, started, remote_done, attempt_done, outcome="READ_FAILURE", head=None):
    return {
        "scheduled_at_ns": scheduled,
        "attempt_started_at_ns": started,
        "remote_observation_completed_at_ns": remote_done,
        "attempt_completed_at_ns": attempt_done,
        "outcome": outcome,
        "observed_head": head,
    }


class TestRPE02MutationDiscriminationV01(unittest.TestCase):
    def test_exact_bound_operator_mutant_is_killed(self):
        base = load_source_module("rpe02_base_bound")
        mutant = load_source_module(
            "rpe02_mut_bound",
            (("if latency <= bound", "if latency < bound"),),
        )
        observations = [
            obs(30_000_000_000, 30_000_000_000, 30_000_000_000, 30_000_000_000),
            obs(
                60_000_000_000,
                60_000_000_000,
                90_000_000_000,
                90_000_000_000,
                "REMOTE_HEAD_OBSERVED",
                A,
            ),
        ]
        kwargs = dict(
            controlled_source_release_started_at_ns=30_000_000_000,
            target_head=A,
            observations=observations,
        )
        self.assertEqual(
            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
            "PASS_DETECTED_WITHIN_BOUND",
        )
        self.assertEqual(
            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )

    def test_actual_start_next_slot_operator_mutant_is_killed(self):
        base = load_source_module("rpe02_base_start")
        mutant = load_source_module(
            "rpe02_mut_start",
            (("if started >= scheduled + interval:", "if started > scheduled + interval:"),),
        )
        observations = [
            obs(
                30_000_000_000,
                60_000_000_000,
                60_000_000_000,
                60_000_000_000,
                "REMOTE_HEAD_OBSERVED",
                A,
            )
        ]
        kwargs = dict(
            controlled_source_release_started_at_ns=30_000_000_000,
            target_head=A,
            observations=observations,
        )
        self.assertEqual(
            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
            "ACTUAL_START_MISSED_FIXED_RATE_SLOT",
        )
        self.assertNotEqual(
            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
            "ACTUAL_START_MISSED_FIXED_RATE_SLOT",
        )

    def test_remote_completion_next_slot_operator_mutant_is_killed(self):
        base = load_source_module("rpe02_base_remote")
        mutant = load_source_module(
            "rpe02_mut_remote",
            (("if remote_done > scheduled + interval:", "if remote_done >= scheduled + interval:"),),
        )
        observations = [
            obs(30_000_000_000, 30_000_000_000, 60_000_000_000, 60_000_000_000)
        ]
        kwargs = dict(
            controlled_source_release_started_at_ns=30_000_000_000,
            target_head=A,
            observations=observations,
        )
        self.assertEqual(
            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
            "INCOMPLETE_REAL_TIME_WINDOW",
        )
        self.assertEqual(
            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
            "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
        )

    def test_latency_endpoint_mutant_is_killed(self):
        base = load_source_module("rpe02_base_endpoint")
        mutant = load_source_module(
            "rpe02_mut_endpoint",
            ((
                'latency = item["remote_observation_completed_at_ns"] - release',
                'latency = item["attempt_completed_at_ns"] - release',
            ),),
        )
        observations = [
            obs(
                30_000_000_000,
                30_000_000_000,
                31_000_000_000,
                100_000_000_000,
                "REMOTE_HEAD_OBSERVED",
                A,
            )
        ]
        kwargs = dict(
            controlled_source_release_started_at_ns=30_000_000_000,
            target_head=A,
            observations=observations,
        )
        self.assertEqual(
            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["detection_latency_ns"],
            1_000_000_000,
        )
        self.assertEqual(
            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )


if __name__ == "__main__":
    unittest.main()
