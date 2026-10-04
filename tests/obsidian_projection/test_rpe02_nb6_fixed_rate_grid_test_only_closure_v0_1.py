import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
TARGET = "a" * 40


def load_module(name, replacements=()):
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


def shifted_grid_case(m):
    second = m.NANOSECONDS_PER_SECOND
    return m.qualify_detection_ns(
        plan=m.make_real_time_plan(schedule_origin_ns=0),
        controlled_source_release_started_at_ns=100 * second,
        target_head=TARGET,
        observations=[
            obs(15 * second, 15 * second, 16 * second, 16 * second),
            obs(45 * second, 45 * second, 46 * second, 46 * second),
            obs(75 * second, 75 * second, 76 * second, 76 * second),
            obs(
                105 * second,
                105 * second,
                106 * second,
                106 * second,
                "REMOTE_HEAD_OBSERVED",
                TARGET,
            ),
        ],
    )


class TestRPE02NB6FixedRateGridTestOnlyClosureV01(unittest.TestCase):
    def test_shifted_grid_is_blocked(self):
        m = load_module("rpe02_nb6_base")
        result = shifted_grid_case(m)
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OFF_FIXED_RATE_GRID")

    def test_off_grid_guard_mutant_is_killed(self):
        base = load_module("rpe02_nb6_base_mut")
        mutant = load_module(
            "rpe02_nb6_mutant",
            ((
                '        if scheduled <= origin or (scheduled - origin) % interval != 0:\n'
                '            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")\n',
                '        if False:\n'
                '            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")\n',
            ),),
        )

        base_result = shifted_grid_case(base)
        mutant_result = shifted_grid_case(mutant)

        self.assertEqual(base_result["failure_code"], "ATTEMPT_OFF_FIXED_RATE_GRID")
        self.assertEqual(mutant_result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(
            mutant_result["detection_latency_ns"],
            6 * mutant.NANOSECONDS_PER_SECOND,
        )


if __name__ == "__main__":
    unittest.main()
