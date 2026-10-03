import types
import unittest
from pathlib import Path


ROOT=Path(__file__).resolve().parents[2]
MODULE=ROOT/"tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
A="a"*40


def load(name,replacements=()):
    source=MODULE.read_text(encoding="utf-8")
    for old,new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source=source.replace(old,new,1)
    m=types.ModuleType(name)
    m.__file__=str(MODULE)
    exec(compile(source,str(MODULE),"exec"),m.__dict__)
    return m


def obs(scheduled,started,remote_done,attempt_done,outcome="READ_FAILURE",head=None):
    return {"scheduled_at_ns":scheduled,"attempt_started_at_ns":started,
        "remote_observation_completed_at_ns":remote_done,"attempt_completed_at_ns":attempt_done,
        "outcome":outcome,"observed_head":head}


def result(m,release,observations):
    return m.qualify_detection_ns(
        plan=m.make_real_time_plan(schedule_origin_ns=0),
        controlled_source_release_started_at_ns=release,
        target_head=A,
        observations=observations,
    )


class TestRPE02ExternalReviewTargetedMutationV01(unittest.TestCase):
    def test_detection_eligibility_scheduled_substitution_is_killed(self):
        base=load("base_det")
        mut=load("mut_det",(('if item["attempt_started_at_ns"] < release:','if item["scheduled_at_ns"] < release:'),))
        data=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)]
        self.assertEqual(result(base,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")
        self.assertNotEqual(result(mut,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")

    def test_pre_release_target_scheduled_substitution_is_killed(self):
        base=load("base_pre")
        mut=load("mut_pre",(("            and started < release\n","            and scheduled < release\n"),))
        data=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)]
        self.assertEqual(result(base,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result(mut,30_500_000_000,data)["failure_code"],"TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT")

    def test_started_before_scheduled_guard_mutant_is_killed(self):
        base=load("base_started")
        mut=load("mut_started",(("        if started < scheduled:\n","        if False:\n"),))
        data=[obs(30_000_000_000,29_999_999_999,30_000_000_000,30_000_000_000)]
        self.assertEqual(result(base,1,data)["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")

    def test_remote_before_start_guard_mutant_is_killed(self):
        base=load("base_remote")
        mut=load("mut_remote",(("        if remote_done < started:\n","        if False:\n"),))
        data=[obs(30_000_000_000,30_000_000_000,29_999_999_999,30_000_000_000)]
        self.assertEqual(result(base,1,data)["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")

    def test_attempt_before_remote_guard_mutant_is_killed(self):
        base=load("base_completion")
        mut=load("mut_completion",(("        if attempt_done < remote_done:\n","        if False:\n"),))
        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,30_999_999_999)]
        self.assertEqual(result(base,1,data)["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")

    def test_duplicate_slot_guard_mutant_is_killed(self):
        base=load("base_dup")
        mut=load("mut_dup",(('        if scheduled in seen_slots:\n            return _blocked("DUPLICATE_FIXED_RATE_SLOT")\n','        if False:\n            return _blocked("DUPLICATE_FIXED_RATE_SLOT")\n'),))
        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
              obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000)]
        self.assertEqual(result(base,1,data)["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")

    def test_cadence_gap_guard_mutant_is_killed(self):
        base=load("base_gap")
        mut=load("mut_gap",(('        if previous_scheduled is not None and scheduled != previous_scheduled + interval:\n            return _blocked("CADENCE_GAP")\n','        if False:\n            return _blocked("CADENCE_GAP")\n'),))
        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
              obs(90_000_000_000,90_000_000_000,90_000_000_000,90_000_000_000)]
        self.assertEqual(result(base,1,data)["failure_code"],"CADENCE_GAP")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"CADENCE_GAP")

    def test_skipped_required_attempt_guard_mutant_is_killed(self):
        base=load("base_skip")
        mut=load("mut_skip",(('        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:\n            return _blocked("SKIPPED_REQUIRED_ATTEMPT")\n','        if False:\n            return _blocked("SKIPPED_REQUIRED_ATTEMPT")\n'),))
        data=[obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000)]
        self.assertEqual(result(base,30_000_000_000,data)["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")
        self.assertNotEqual(result(mut,30_000_000_000,data)["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")

    def test_no_detection_exact_bound_operator_mutant_is_killed(self):
        base=load("base_no_detect")
        mut=load("mut_no_detect",(("    if next_required_slot - release > bound:\n","    if next_required_slot - release >= bound:\n"),))
        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
              obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000)]
        self.assertEqual(result(base,30_000_000_000,data)["status"],"INCOMPLETE_REAL_TIME_WINDOW")
        self.assertEqual(result(mut,30_000_000_000,data)["status"],"FAIL_NO_DETECTION_BY_BOUND")

    def test_order_integrity_mutant_is_killed(self):
        base=load("base_order")
        mut=load("mut_order",(('        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:\n            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")\n','        if False:\n            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")\n'),))
        data=[obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
              obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)]
        self.assertEqual(result(base,1,data)["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")
        self.assertNotEqual(result(mut,1,data)["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

    def test_outcome_vocabulary_mutant_is_killed(self):
        base=load("base_outcome")
        mut=load("mut_outcome",(('    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:\n','    if type(out["outcome"]) is not str or not out["outcome"]:\n'),))
        bad=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"GARBAGE",A)]
        with self.assertRaises(base.RPE02TimingError):
            result(base,1,bad)
        result(mut,1,bad)

    def test_failure_head_coherence_mutant_is_killed(self):
        base=load("base_coherence")
        mut=load("mut_coherence",(('        if out["observed_head"] is not None:\n            raise RPE02TimingError(\n                f"observations[{index}] READ_FAILURE may not carry observed_head"\n            )\n','        if False:\n            raise RPE02TimingError(\n                f"observations[{index}] READ_FAILURE may not carry observed_head"\n            )\n'),))
        bad=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"READ_FAILURE",A)]
        with self.assertRaises(base.RPE02TimingError):
            result(base,1,bad)
        result(mut,1,bad)


if __name__=="__main__":
    unittest.main()
