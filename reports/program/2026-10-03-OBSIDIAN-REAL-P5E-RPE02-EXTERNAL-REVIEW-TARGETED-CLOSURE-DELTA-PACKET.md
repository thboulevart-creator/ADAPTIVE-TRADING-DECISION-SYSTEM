# RPE-02 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — DELTA REVIEW PACKET

Date: 2026-10-03

## Mandate

Review only the closure of findings from the prior RPE-02 external review.

Prior verdict:
VERDICT = FAIL

Prior blocker:
BF-1 = malformed observation integrity

Candidate status:
RPE-02 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

This packet creates no authority.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## Lineage

Prior externally reviewed packet HEAD:
4742ba3f717f7f9773e311d3c0f9470cfd6680f9

Review/adjudication HEAD:
fcf628a80c4db84f516a99863d1c80ec7501a381

Targeted preregistration HEAD:
b8b2698252be7f630e435d17313cd1058bec2a51

Targeted RED HEAD:
afaafb9f3b9fb3a4d90cfa912b7eb176abc19161

Targeted patch HEAD:
4a28540eafa82fd136dd4a402ef552f22f817f36

Targeted qualification HEAD:
5f0d19aa82f1c448354c8789a28118842d890c32

## Candidate identities

External review return = 45766b0ad21a62447b9233ec1563eb85825f221d
Internal adjudication = 836450b88ae69254dda77f548ede19bfaae1cb86
Targeted preregistration = cafee7194155944eb059ead466fd6bc517edde58
Targeted schema = d67da710e63643c26c0a004cc38109ff4e301b25
Targeted historical RED test = 0756598131911168a7cb5944c0ed465c7ebbd2a0
Targeted RED report = b558fceaf0b214715ef65cd710ebb391464778d0
Final implementation = 31db5d944a25e54db81bd901a087cdc2039925ad
Targeted mutation test = c00bb49ffa930aefcdce794c5b7a7c68211e586f
Qualification JSON = 97fac2708f24610fe3c4ebefa094f8ec1ba312bf
Qualification report = 1159b65345b15b5a6ee32c3bd320ee3ab3a0ef46

## Packet fidelity identities — deliberately distinct

ORIGINAL HISTORICAL RED TEST BLOB
= 089a72c736302abd08ea1267c149e2ef771240db

ORIGINAL FINAL PRE-CLOSURE MAIN TEST BLOB
= 23618a9317c554099670e84482641a8014f8682d

TARGETED HISTORICAL RED TEST BLOB
= 0756598131911168a7cb5944c0ed465c7ebbd2a0

The targeted RED test was not rewritten after RED; it became GREEN because the implementation changed. It is therefore both the historical targeted test identity and the current targeted test identity. This is stated explicitly and is not a mislabeled final-copy-as-RED substitution.

## Observed evidence

Targeted RED:
15 tests / 7 failures / 8 passes.

Targeted GREEN:
15 / 15 PASS.

Targeted mutation discrimination:
12 / 12 PASS; 12 / 12 mutants killed.

Full targeted regression:
162 / 162 PASS.

Protected diffs:
P5-E contract = 0
P5-E synthetic model = 0
P5-D4 runtime = 0

## Closure claims to review

BF-1:
- outcome vocabulary is exactly READ_FAILURE | REMOTE_HEAD_OBSERVED;
- success requires lowercase 40-hex observed_head;
- READ_FAILURE requires observed_head=None;
- malformed evidence raises RPE02TimingError before SLA verdicting.

NB-1:
- attempt_started_at_ns is test-locked for both detection eligibility and pre-release target handling;
- structural guards are mutation-locked.

NB-2:
- no-detection decision uses next fixed-rate slot feasibility;
- next_required_slot - release > bound => FAIL_NO_DETECTION_BY_BOUND;
- equality remains INCOMPLETE because an exact-bound future attempt can still pass;
- both reviewer counterexamples now converge with the synthetic reference.

NB-3:
- observations are no longer sorted;
- decreasing supplied scheduled_at_ns blocks as OBSERVATION_ORDER_NOT_STRICTLY_INCREASING;
- duplicate slots retain their dedicated failure code.

NB-4 adjudication:
- SLA endpoint remains remote_observation_completed_at_ns;
- full attempt completion remains timeline/overlap evidence;
- NO REAL ATTEMPT OVERLAP execution guarantee is explicitly carried to RPE-05.

NB-5:
- historical RED and final test identities are separated above and below.

## Required review

Return:
VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- BF1_INTEGRITY_CHECK
- NB1_TEST_LOCK_CHECK
- NB2_PARITY_CHECK
- NB3_ORDER_CHECK
- NB4_SCOPE_CHECK
- NB5_PACKET_FIDELITY_CHECK
- MUTATION_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RPE02_ADOPTION_READINESS
- RECOMMENDED_NEXT_ACTION

Attempt falsification of malformed outcome/head pairs, scheduled-vs-actual-start substitution, removed structural guards, both exact-grid counterexamples, exact-bound no-detection operator, and silent reorder.

This review creates no authority.
RPE-04 = CLOSED.
REAL P5-E = CLOSED.

---

# NORMALIZED DELTA — PRIOR REVIEWED HEAD TO TARGETED QUALIFICATION
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
new file mode 100644
index 0000000..1159b65
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
@@ -0,0 +1,128 @@
+# RPE-02 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION
+
+Date: 2026-10-03
+
+## Result
+
+`RPE-02 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`
+
+The prior external verdict was `FAIL`. No human adoption is created by this qualification.
+
+## Closure identities
+
+External review blob:
+`45766b0ad21a62447b9233ec1563eb85825f221d`
+
+Internal adjudication:
+`836450b88ae69254dda77f548ede19bfaae1cb86`
+
+Targeted preregistration:
+`cafee7194155944eb059ead466fd6bc517edde58`
+
+Targeted preregistration schema:
+`d67da710e63643c26c0a004cc38109ff4e301b25`
+
+Targeted RED HEAD:
+`afaafb9f3b9fb3a4d90cfa912b7eb176abc19161`
+
+Targeted RED test:
+`0756598131911168a7cb5944c0ed465c7ebbd2a0`
+
+Targeted RED report:
+`b558fceaf0b214715ef65cd710ebb391464778d0`
+
+Final candidate HEAD:
+`4a28540eafa82fd136dd4a402ef552f22f817f36`
+
+Final implementation:
+`31db5d944a25e54db81bd901a087cdc2039925ad`
+
+Targeted mutation tests:
+`c00bb49ffa930aefcdce794c5b7a7c68211e586f`
+
+## BF-1
+
+Observation integrity is now closed before business verdicting.
+
+Allowed outcome vocabulary is exactly:
+- READ_FAILURE;
+- REMOTE_HEAD_OBSERVED.
+
+REMOTE_HEAD_OBSERVED requires a lowercase 40-hex head.
+READ_FAILURE requires observed_head = null.
+Unknown outcomes and incoherent outcome/head combinations raise RPE02TimingError before any SLA status can be produced.
+
+## NB-1
+
+The actual attempt start is test-locked as the release-eligibility field in both:
+- first-detection eligibility;
+- pre-release target handling.
+
+Mutation tests also lock:
+- actual start before scheduled;
+- remote completion before actual start;
+- attempt completion before remote completion;
+- duplicate slot;
+- cadence gap;
+- skipped required attempt.
+
+## NB-2
+
+No-detection semantics now follow fixed-rate feasibility:
+
+`next_required_slot_ns - release_ns > bound_ns`
+→ `FAIL_NO_DETECTION_BY_BOUND`
+with `NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND`.
+
+At exact equality, the result remains INCOMPLETE because a future attempt can still meet the bound exactly.
+
+Both external-review counterexamples now converge with the adopted synthetic reference.
+
+## NB-3
+
+Observations are no longer silently sorted.
+
+A supplied scheduled timestamp lower than the preceding supplied timestamp returns:
+`BLOCKED_REQUIRES_ADJUDICATION / OBSERVATION_ORDER_NOT_STRICTLY_INCREASING`.
+
+Duplicate slots retain their dedicated failure code.
+
+## NB-4 adjudication
+
+The SLA endpoint remains:
+`remote_observation_completed_at_ns`.
+
+`attempt_completed_at_ns` remains timeline/overlap evidence only.
+
+The runtime execution guarantee `NO REAL ATTEMPT OVERLAP` is explicitly carried to RPE-05.
+
+## Evidence
+
+Targeted closure:
+`15 / 15 PASS`
+
+Targeted mutation discrimination:
+`12 / 12 PASS; 12 / 12 mutants killed`
+
+P5-E + RPE-01 + RPE-02 regression:
+`162 / 162 PASS`
+
+Protected diffs:
+- P5-E contract = 0;
+- P5-E synthetic model = 0;
+- P5-D4 runtime = 0.
+
+## Packet-fidelity rule
+
+The rebuilt delta-review packet must distinguish:
+- original historical RED test blob `089a72c736302abd08ea1267c149e2ef771240db`;
+- original final test blob `23618a9317c554099670e84482641a8014f8682d`;
+- targeted historical RED test blob `0756598131911168a7cb5944c0ed465c7ebbd2a0`.
+
+No final test may be labeled as a historical RED copy.
+
+## Authority
+
+RPE-02 human adoption = pending.
+RPE-04/05/06 = closed.
+REAL P5-E = closed.
diff --git a/tests/obsidian_projection/test_rpe02_external_review_targeted_closure_v0_1.py b/tests/obsidian_projection/test_rpe02_external_review_targeted_closure_v0_1.py
new file mode 100644
index 0000000..0756598
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe02_external_review_targeted_closure_v0_1.py
@@ -0,0 +1,151 @@
+import importlib.util
+import unittest
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
+A = "a" * 40
+
+
+def load():
+    spec = importlib.util.spec_from_file_location("rpe02_targeted", MODULE)
+    if spec is None or spec.loader is None:
+        raise AssertionError("cannot load RPE-02 module")
+    m = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(m)
+    return m
+
+
+def obs(scheduled, started, remote_done, attempt_done, outcome="READ_FAILURE", head=None):
+    return {
+        "scheduled_at_ns": scheduled,
+        "attempt_started_at_ns": started,
+        "remote_observation_completed_at_ns": remote_done,
+        "attempt_completed_at_ns": attempt_done,
+        "outcome": outcome,
+        "observed_head": head,
+    }
+
+
+class TestRPE02ExternalReviewTargetedClosureV01(unittest.TestCase):
+    def setUp(self):
+        self.m = load()
+        self.plan = self.m.make_real_time_plan(schedule_origin_ns=0)
+
+    def test_unknown_outcome_is_rejected_before_sla_verdict(self):
+        with self.assertRaises(self.m.RPE02TimingError):
+            self.m.qualify_detection_ns(
+                plan=self.plan,
+                controlled_source_release_started_at_ns=1_000_000_000,
+                target_head=A,
+                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"GARBAGE",A)],
+            )
+
+    def test_success_without_head_is_rejected_before_sla_verdict(self):
+        with self.assertRaises(self.m.RPE02TimingError):
+            self.m.qualify_detection_ns(
+                plan=self.plan,
+                controlled_source_release_started_at_ns=1_000_000_000,
+                target_head=A,
+                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"REMOTE_HEAD_OBSERVED",None)],
+            )
+
+    def test_failure_with_head_is_rejected_before_sla_verdict(self):
+        with self.assertRaises(self.m.RPE02TimingError):
+            self.m.qualify_detection_ns(
+                plan=self.plan,
+                controlled_source_release_started_at_ns=1_000_000_000,
+                target_head=A,
+                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"READ_FAILURE",A)],
+            )
+
+    def test_outcome_typo_with_target_head_is_rejected(self):
+        with self.assertRaises(self.m.RPE02TimingError):
+            self.m.qualify_detection_ns(
+                plan=self.plan,
+                controlled_source_release_started_at_ns=1_000_000_000,
+                target_head=A,
+                observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"REMOTE_HEAD_OBSERVED ",A)],
+            )
+
+    def test_actual_start_after_release_is_eligible_even_if_slot_precedes_release(self):
+        r = self.m.qualify_detection_ns(
+            plan=self.plan,
+            controlled_source_release_started_at_ns=30_500_000_000,
+            target_head=A,
+            observations=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)],
+        )
+        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
+        self.assertEqual(r["detection_latency_ns"], 1_500_000_000)
+
+    def test_started_before_scheduled_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[obs(30_000_000_000,29_999_999_999,30_000_000_000,30_000_000_000)])
+        self.assertEqual(r["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
+
+    def test_remote_completion_before_start_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,29_999_999_999,30_000_000_000)])
+        self.assertEqual(r["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
+
+    def test_attempt_completion_before_remote_completion_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,30_999_999_999)])
+        self.assertEqual(r["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
+
+    def test_duplicate_slot_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000)])
+        self.assertEqual(r["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")
+
+    def test_cadence_gap_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+                obs(90_000_000_000,90_000_000_000,90_000_000_000,90_000_000_000)])
+        self.assertEqual(r["failure_code"],"CADENCE_GAP")
+
+    def test_skipped_first_required_attempt_is_blocked(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
+            observations=[obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000)])
+        self.assertEqual(r["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")
+
+    def test_supplied_out_of_order_observations_are_not_silently_sorted(self):
+        r=self.m.qualify_detection_ns(plan=self.plan,controlled_source_release_started_at_ns=1,target_head=A,
+            observations=[
+                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
+                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)])
+        self.assertEqual(r["status"],"BLOCKED_REQUIRES_ADJUDICATION")
+        self.assertEqual(r["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")
+
+    def test_parity_infeasible_next_slot_fails_even_before_last_remote_reaches_bound(self):
+        r=self.m.qualify_detection_ns(
+            plan=self.plan,controlled_source_release_started_at_ns=1_000_000_000,target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
+                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000)])
+        self.assertEqual(r["status"],"FAIL_NO_DETECTION_BY_BOUND")
+        self.assertEqual(r["failure_code"],"NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND")
+
+    def test_parity_next_slot_exactly_at_bound_is_incomplete_not_fail(self):
+        r=self.m.qualify_detection_ns(
+            plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+                obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000)])
+        self.assertEqual(r["status"],"INCOMPLETE_REAL_TIME_WINDOW")
+        self.assertIsNone(r["failure_code"])
+
+    def test_nb4_scope_full_completion_does_not_replace_remote_latency_endpoint(self):
+        r=self.m.qualify_detection_ns(
+            plan=self.plan,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_000,300_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["status"],"PASS_DETECTED_WITHIN_BOUND")
+        self.assertEqual(r["detection_latency_ns"],30_000_000_000)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/obsidian_projection/test_rpe02_external_review_targeted_mutation_v0_1.py b/tests/obsidian_projection/test_rpe02_external_review_targeted_mutation_v0_1.py
new file mode 100644
index 0000000..c00bb49
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe02_external_review_targeted_mutation_v0_1.py
@@ -0,0 +1,131 @@
+import types
+import unittest
+from pathlib import Path
+
+
+ROOT=Path(__file__).resolve().parents[2]
+MODULE=ROOT/"tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
+A="a"*40
+
+
+def load(name,replacements=()):
+    source=MODULE.read_text(encoding="utf-8")
+    for old,new in replacements:
+        if source.count(old) != 1:
+            raise AssertionError(f"mutation anchor count != 1: {old!r}")
+        source=source.replace(old,new,1)
+    m=types.ModuleType(name)
+    m.__file__=str(MODULE)
+    exec(compile(source,str(MODULE),"exec"),m.__dict__)
+    return m
+
+
+def obs(scheduled,started,remote_done,attempt_done,outcome="READ_FAILURE",head=None):
+    return {"scheduled_at_ns":scheduled,"attempt_started_at_ns":started,
+        "remote_observation_completed_at_ns":remote_done,"attempt_completed_at_ns":attempt_done,
+        "outcome":outcome,"observed_head":head}
+
+
+def result(m,release,observations):
+    return m.qualify_detection_ns(
+        plan=m.make_real_time_plan(schedule_origin_ns=0),
+        controlled_source_release_started_at_ns=release,
+        target_head=A,
+        observations=observations,
+    )
+
+
+class TestRPE02ExternalReviewTargetedMutationV01(unittest.TestCase):
+    def test_detection_eligibility_scheduled_substitution_is_killed(self):
+        base=load("base_det")
+        mut=load("mut_det",(('if item["attempt_started_at_ns"] < release:','if item["scheduled_at_ns"] < release:'),))
+        data=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)]
+        self.assertEqual(result(base,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")
+        self.assertNotEqual(result(mut,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")
+
+    def test_pre_release_target_scheduled_substitution_is_killed(self):
+        base=load("base_pre")
+        mut=load("mut_pre",(("            and started < release\n","            and scheduled < release\n"),))
+        data=[obs(30_000_000_000,31_000_000_000,32_000_000_000,32_000_000_000,"REMOTE_HEAD_OBSERVED",A)]
+        self.assertEqual(result(base,30_500_000_000,data)["status"],"PASS_DETECTED_WITHIN_BOUND")
+        self.assertEqual(result(mut,30_500_000_000,data)["failure_code"],"TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT")
+
+    def test_started_before_scheduled_guard_mutant_is_killed(self):
+        base=load("base_started")
+        mut=load("mut_started",(("        if started < scheduled:\n","        if False:\n"),))
+        data=[obs(30_000_000_000,29_999_999_999,30_000_000_000,30_000_000_000)]
+        self.assertEqual(result(base,1,data)["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
+
+    def test_remote_before_start_guard_mutant_is_killed(self):
+        base=load("base_remote")
+        mut=load("mut_remote",(("        if remote_done < started:\n","        if False:\n"),))
+        data=[obs(30_000_000_000,30_000_000_000,29_999_999_999,30_000_000_000)]
+        self.assertEqual(result(base,1,data)["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
+
+    def test_attempt_before_remote_guard_mutant_is_killed(self):
+        base=load("base_completion")
+        mut=load("mut_completion",(("        if attempt_done < remote_done:\n","        if False:\n"),))
+        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,30_999_999_999)]
+        self.assertEqual(result(base,1,data)["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
+
+    def test_duplicate_slot_guard_mutant_is_killed(self):
+        base=load("base_dup")
+        mut=load("mut_dup",(('        if scheduled in seen_slots:\n            return _blocked("DUPLICATE_FIXED_RATE_SLOT")\n','        if False:\n            return _blocked("DUPLICATE_FIXED_RATE_SLOT")\n'),))
+        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+              obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000)]
+        self.assertEqual(result(base,1,data)["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"DUPLICATE_FIXED_RATE_SLOT")
+
+    def test_cadence_gap_guard_mutant_is_killed(self):
+        base=load("base_gap")
+        mut=load("mut_gap",(('        if previous_scheduled is not None and scheduled != previous_scheduled + interval:\n            return _blocked("CADENCE_GAP")\n','        if False:\n            return _blocked("CADENCE_GAP")\n'),))
+        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+              obs(90_000_000_000,90_000_000_000,90_000_000_000,90_000_000_000)]
+        self.assertEqual(result(base,1,data)["failure_code"],"CADENCE_GAP")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"CADENCE_GAP")
+
+    def test_skipped_required_attempt_guard_mutant_is_killed(self):
+        base=load("base_skip")
+        mut=load("mut_skip",(('        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:\n            return _blocked("SKIPPED_REQUIRED_ATTEMPT")\n','        if False:\n            return _blocked("SKIPPED_REQUIRED_ATTEMPT")\n'),))
+        data=[obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000)]
+        self.assertEqual(result(base,30_000_000_000,data)["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")
+        self.assertNotEqual(result(mut,30_000_000_000,data)["failure_code"],"SKIPPED_REQUIRED_ATTEMPT")
+
+    def test_no_detection_exact_bound_operator_mutant_is_killed(self):
+        base=load("base_no_detect")
+        mut=load("mut_no_detect",(("    if next_required_slot - release > bound:\n","    if next_required_slot - release >= bound:\n"),))
+        data=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000),
+              obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000)]
+        self.assertEqual(result(base,30_000_000_000,data)["status"],"INCOMPLETE_REAL_TIME_WINDOW")
+        self.assertEqual(result(mut,30_000_000_000,data)["status"],"FAIL_NO_DETECTION_BY_BOUND")
+
+    def test_order_integrity_mutant_is_killed(self):
+        base=load("base_order")
+        mut=load("mut_order",(('        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:\n            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")\n','        if False:\n            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")\n'),))
+        data=[obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
+              obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)]
+        self.assertEqual(result(base,1,data)["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")
+        self.assertNotEqual(result(mut,1,data)["failure_code"],"OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")
+
+    def test_outcome_vocabulary_mutant_is_killed(self):
+        base=load("base_outcome")
+        mut=load("mut_outcome",(('    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:\n','    if type(out["outcome"]) is not str or not out["outcome"]:\n'),))
+        bad=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"GARBAGE",A)]
+        with self.assertRaises(base.RPE02TimingError):
+            result(base,1,bad)
+        result(mut,1,bad)
+
+    def test_failure_head_coherence_mutant_is_killed(self):
+        base=load("base_coherence")
+        mut=load("mut_coherence",(('        if out["observed_head"] is not None:\n            raise RPE02TimingError(\n                f"observations[{index}] READ_FAILURE may not carry observed_head"\n            )\n','        if False:\n            raise RPE02TimingError(\n                f"observations[{index}] READ_FAILURE may not carry observed_head"\n            )\n'),))
+        bad=[obs(30_000_000_000,30_000_000_000,31_000_000_000,31_000_000_000,"READ_FAILURE",A)]
+        with self.assertRaises(base.RPE02TimingError):
+            result(base,1,bad)
+        result(mut,1,bad)
+
+
+if __name__=="__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/rpe02_external_review_targeted_closure_preregistration_v0_1.json b/tools/obsidian_projection/rpe02_external_review_targeted_closure_preregistration_v0_1.json
new file mode 100644
index 0000000..cafee71
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_external_review_targeted_closure_preregistration_v0_1.json
@@ -0,0 +1,95 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_EXTERNAL_REVIEW_TARGETED_CLOSURE_PREREGISTRATION_V0_1",
+  "status": "PREREGISTERED_BEFORE_TARGETED_RED",
+  "base": {
+    "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
+    "review_adjudication_head": "fcf628a80c4db84f516a99863d1c80ec7501a381",
+    "external_review_verdict": "FAIL",
+    "blocking_finding": "BF-1",
+    "qualified_impl_blob": "db5dcfe8ad3b7ce93099368b459bb09ac25f933b",
+    "qualified_main_test_blob": "23618a9317c554099670e84482641a8014f8682d",
+    "qualified_mutation_test_blob": "77cdadb376320c4e8f591a3a80105feac250b716"
+  },
+  "authority": {
+    "targeted_closure_authorized": true,
+    "rpe04_authorized": false,
+    "rpe05_authorized": false,
+    "rpe06_authorized": false,
+    "real_p5e_authorized": false,
+    "network_authorized": false
+  },
+  "closure_scope": [
+    "BF-1",
+    "NB-1",
+    "NB-2",
+    "NB-3",
+    "NB-5"
+  ],
+  "observation_integrity": {
+    "allowed_outcomes": [
+      "READ_FAILURE",
+      "REMOTE_HEAD_OBSERVED"
+    ],
+    "remote_head_observed_requires_lowercase_40hex": true,
+    "read_failure_requires_observed_head_null": true,
+    "malformed_record_policy": "RAISE_RPE02_TIMING_ERROR_BEFORE_ANY_SLA_VERDICT",
+    "input_order_field": "scheduled_at_ns",
+    "input_order_requirement": "STRICTLY_INCREASING_AS_SUPPLIED",
+    "silent_sorting_forbidden": true
+  },
+  "eligibility_test_lock": {
+    "detection_eligibility_field": "attempt_started_at_ns",
+    "pre_release_target_field": "attempt_started_at_ns",
+    "scheduled_at_ns_substitution_forbidden": true,
+    "structural_breakers": [
+      "ACTUAL_START_PRECEDES_SCHEDULED_SLOT",
+      "REMOTE_COMPLETION_PRECEDES_ATTEMPT_START",
+      "ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION",
+      "DUPLICATE_FIXED_RATE_SLOT",
+      "CADENCE_GAP",
+      "SKIPPED_REQUIRED_ATTEMPT",
+      "OBSERVATION_ORDER_NOT_STRICTLY_INCREASING"
+    ]
+  },
+  "no_detection_semantics": {
+    "rule": "NEXT_REQUIRED_FIXED_RATE_SLOT_FEASIBILITY",
+    "last_scheduled_source": "LAST_SUPPLIED_AND_VALIDATED_SCHEDULED_SLOT",
+    "next_required_slot_formula": "last_scheduled_at_ns + poll_interval_ns",
+    "fail_condition": "next_required_slot_ns - controlled_source_release_started_at_ns > detection_latency_bound_ns",
+    "fail_status": "FAIL_NO_DETECTION_BY_BOUND",
+    "fail_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
+    "otherwise_status": "INCOMPLETE_REAL_TIME_WINDOW",
+    "last_remote_completion_alone_may_not_decide_no_detection": true,
+    "exact_grid_parity_claim_may_remain_only_if_counterexamples_converge": true
+  },
+  "nb4_scope_adjudication": {
+    "sla_endpoint": "remote_observation_completed_at_ns",
+    "full_attempt_completion_role": "TIMELINE_AND_OVERLAP_EVIDENCE_ONLY",
+    "last_attempt_full_completion_beyond_future_slot_alone_changes_sla": false,
+    "no_real_attempt_overlap_execution_guarantee_stage": "RPE-05"
+  },
+  "packet_fidelity": {
+    "historical_red_test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
+    "final_preclosure_test_blob": "23618a9317c554099670e84482641a8014f8682d",
+    "historical_red_must_be_sourced_from_historical_blob": true,
+    "final_test_must_be_labeled_separately": true
+  },
+  "mandatory_red_cases": [
+    "unknown outcome",
+    "REMOTE_HEAD_OBSERVED without head",
+    "READ_FAILURE with head",
+    "outcome typo with target head",
+    "actual-start eligibility differs from scheduled slot",
+    "pre-release target handling differs from scheduled slot",
+    "started before scheduled",
+    "remote completion before started",
+    "attempt completion before remote completion",
+    "duplicate slot",
+    "cadence gap",
+    "skipped required attempt",
+    "out-of-order supplied observations",
+    "parity counterexample release 1 with slots 30 and 60",
+    "parity counterexample release 30 with completions 31 and 90"
+  ],
+  "stop": "TARGETED_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+}
diff --git a/tools/obsidian_projection/rpe02_external_review_targeted_closure_qualification_v0_1.json b/tools/obsidian_projection/rpe02_external_review_targeted_closure_qualification_v0_1.json
new file mode 100644
index 0000000..97fac27
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_external_review_targeted_closure_qualification_v0_1.json
@@ -0,0 +1,78 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
+  "date": "2026-10-03",
+  "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
+  "external_review": {
+    "verdict": "FAIL",
+    "review_blob": "45766b0ad21a62447b9233ec1563eb85825f221d",
+    "adjudication_blob": "836450b88ae69254dda77f548ede19bfaae1cb86"
+  },
+  "preregistration": {
+    "head": "b8b2698252be7f630e435d17313cd1058bec2a51",
+    "blob": "cafee7194155944eb059ead466fd6bc517edde58",
+    "schema_blob": "d67da710e63643c26c0a004cc38109ff4e301b25"
+  },
+  "targeted_red": {
+    "head": "afaafb9f3b9fb3a4d90cfa912b7eb176abc19161",
+    "test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
+    "report_blob": "b558fceaf0b214715ef65cd710ebb391464778d0",
+    "result": "15 tests; 7 failures; 8 passes"
+  },
+  "final_candidate": {
+    "head": "4a28540eafa82fd136dd4a402ef552f22f817f36",
+    "implementation_blob": "31db5d944a25e54db81bd901a087cdc2039925ad",
+    "targeted_test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
+    "targeted_mutation_blob": "c00bb49ffa930aefcdce794c5b7a7c68211e586f"
+  },
+  "closures": {
+    "bf1": "CLOSED_CANDIDATE",
+    "nb1": "CLOSED_CANDIDATE",
+    "nb2": "CLOSED_CANDIDATE",
+    "nb3": "CLOSED_CANDIDATE",
+    "nb4": "SCOPE_ADJUDICATED_RPE05_EXECUTION_GUARANTEE",
+    "nb5": "PACKET_REBUILD_REQUIRED_AND_AUTHORIZED"
+  },
+  "final_semantics": {
+    "outcomes": [
+      "READ_FAILURE",
+      "REMOTE_HEAD_OBSERVED"
+    ],
+    "successful_remote_observation_requires_lowercase_40hex": true,
+    "read_failure_requires_null_head": true,
+    "malformed_observation": "RPE02TimingError before SLA verdict",
+    "observation_order": "supplied scheduled_at_ns may not decrease; duplicates retain DUPLICATE_FIXED_RATE_SLOT",
+    "release_eligibility": "attempt_started_at_ns",
+    "no_detection_rule": "next_required_slot_ns - release_ns > bound_ns",
+    "no_detection_failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
+    "exact_bound_without_detection": "INCOMPLETE_REAL_TIME_WINDOW",
+    "sla_endpoint": "remote_observation_completed_at_ns",
+    "full_attempt_completion_role": "TIMELINE_AND_OVERLAP_EVIDENCE_ONLY",
+    "no_real_attempt_overlap_execution_guarantee_stage": "RPE-05"
+  },
+  "tests": {
+    "targeted_green": "15/15 PASS",
+    "targeted_mutation": "12/12 PASS / 12 mutants killed",
+    "full_targeted_regression": "162/162 PASS"
+  },
+  "protected_diffs": {
+    "p5e_contract": 0,
+    "p5e_synthetic_model": 0,
+    "p5d4_runtime": 0
+  },
+  "packet_fidelity": {
+    "original_historical_red_test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
+    "original_final_test_blob": "23618a9317c554099670e84482641a8014f8682d",
+    "targeted_historical_red_test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
+    "labels_must_remain_distinct": true
+  },
+  "claim_boundary": {
+    "rpe02_human_adopted": false,
+    "rpe04_opened": false,
+    "rpe05_opened": false,
+    "rpe06_opened": false,
+    "real_p5e_authorized": false
+  },
+  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
+  "stop": true
+}
diff --git a/tools/obsidian_projection/rpe02_real_time_model_v0_1.py b/tools/obsidian_projection/rpe02_real_time_model_v0_1.py
index db5dcfe..31db5d9 100644
--- a/tools/obsidian_projection/rpe02_real_time_model_v0_1.py
+++ b/tools/obsidian_projection/rpe02_real_time_model_v0_1.py
@@ -18,6 +18,7 @@ NANOSECONDS_PER_SECOND = 1_000_000_000
 POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
 DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
 _SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
+_ALLOWED_OUTCOMES = {"READ_FAILURE", "REMOTE_HEAD_OBSERVED"}


 class RPE02TimingError(ValueError):
@@ -118,9 +119,17 @@ def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]
         "attempt_completed_at_ns",
     ):
         out[key] = _strict_int(f"observations[{index}].{key}", out[key])
-    if type(out["outcome"]) is not str or not out["outcome"]:
-        raise RPE02TimingError(f"observations[{index}].outcome must be non-empty string")
-    if out["observed_head"] is not None:
+    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:
+        raise RPE02TimingError(
+            f"observations[{index}].outcome must be one of "
+            f"{sorted(_ALLOWED_OUTCOMES)}"
+        )
+    if out["outcome"] == "READ_FAILURE":
+        if out["observed_head"] is not None:
+            raise RPE02TimingError(
+                f"observations[{index}] READ_FAILURE may not carry observed_head"
+            )
+    else:
         out["observed_head"] = _strict_sha40(
             f"observations[{index}].observed_head",
             out["observed_head"],
@@ -151,7 +160,9 @@ def qualify_detection_ns(
         raise RPE02TimingError("observations must be a sequence")

     normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
-    normalized.sort(key=lambda item: item["scheduled_at_ns"])
+    for index in range(1, len(normalized)):
+        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:
+            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

     previous_scheduled: int | None = None
     previous_completion: int | None = None
@@ -235,14 +246,15 @@ def qualify_detection_ns(
                 "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
             }

-    window_end = max(
-        (item["remote_observation_completed_at_ns"] for item in normalized),
-        default=origin,
+    next_required_slot = (
+        normalized[-1]["scheduled_at_ns"] + interval
+        if normalized
+        else first_required
     )
-    if window_end >= release + bound:
+    if next_required_slot - release > bound:
         return {
             "status": "FAIL_NO_DETECTION_BY_BOUND",
-            "failure_code": None,
+            "failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
             "detection_latency_ns": None,
         }
     return {
~~~~

# GIT-BLOB-SOURCED COPY: PRIOR EXTERNAL REVIEW RETURN
Path: reports/program/...RPE02-EXTERNAL-REVIEW-CLAUDE-RETURN.md
Authoritative Git blob: 45766b0ad21a62447b9233ec1563eb85825f221d
~~~~
# RPE-02 — EXTERNAL REVIEW RETURN — CLAUDE

Date: 2026-10-03

## Verdict

`VERDICT = FAIL`

## Blocking finding

### BF-1 — malformed observation integrity

Observed behavior:
- arbitrary non-empty strings are accepted as `outcome`;
- `REMOTE_HEAD_OBSERVED` does not require a head;
- `READ_FAILURE` may carry a head;
- malformed records can become `FAIL_NO_DETECTION_BY_BOUND` instead of being rejected or blocked.

Required closure:
- vocabulary exactly `READ_FAILURE | REMOTE_HEAD_OBSERVED`;
- `REMOTE_HEAD_OBSERVED -> observed_head = lowercase 40-hex`;
- `READ_FAILURE -> observed_head = null`;
- malformed evidence must fail closed before any SLA business verdict.

## Non-blocking findings carried into targeted closure

### NB-1 — insufficient test lock

Additional discrimination required for:
- actual-start versus scheduled-slot release eligibility;
- started < scheduled;
- remote completion < actual start;
- attempt completion < remote completion;
- duplicate slot;
- cadence gap;
- skipped required attempt;
- no-detection exact boundary.

### NB-2 — exact-grid parity divergence

Two observed counterexamples distinguish:
- `FAIL_NO_DETECTION_BY_BOUND`;
- `INCOMPLETE_REAL_TIME_WINDOW`.

The current implementation uses last remote completion rather than feasibility of the next required fixed-rate slot. Exact-grid parity is therefore overclaimed until corrected.

### NB-3 — silent sorting

Input observations are sorted internally. Input order should instead be treated as evidence integrity.

### NB-4 — final full-attempt completion

The reviewer noted that the last attempt's full completion may extend far beyond the next slot. Human adjudication for targeted closure keeps:
- remote completion = SLA endpoint;
- full attempt completion = timeline/overlap evidence;
- real no-overlap execution guarantee deferred to RPE-05.

### NB-5 — packet fidelity

The previous packet labeled the final test as the RED test. The replacement packet must distinguish historical RED blob from final test blob.

## Adoption readiness

`RPE-02 = NOT_READY_FOR_HUMAN_ADOPTION`

This review creates no authority.

`RPE-04 = CLOSED`
`REAL_P5E = CLOSED`
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED PREREGISTRATION
Path: tools/obsidian_projection/rpe02_external_review_targeted_closure_preregistration_v0_1.json
Authoritative Git blob: cafee7194155944eb059ead466fd6bc517edde58
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_EXTERNAL_REVIEW_TARGETED_CLOSURE_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_TARGETED_RED",
  "base": {
    "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
    "review_adjudication_head": "fcf628a80c4db84f516a99863d1c80ec7501a381",
    "external_review_verdict": "FAIL",
    "blocking_finding": "BF-1",
    "qualified_impl_blob": "db5dcfe8ad3b7ce93099368b459bb09ac25f933b",
    "qualified_main_test_blob": "23618a9317c554099670e84482641a8014f8682d",
    "qualified_mutation_test_blob": "77cdadb376320c4e8f591a3a80105feac250b716"
  },
  "authority": {
    "targeted_closure_authorized": true,
    "rpe04_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false,
    "network_authorized": false
  },
  "closure_scope": [
    "BF-1",
    "NB-1",
    "NB-2",
    "NB-3",
    "NB-5"
  ],
  "observation_integrity": {
    "allowed_outcomes": [
      "READ_FAILURE",
      "REMOTE_HEAD_OBSERVED"
    ],
    "remote_head_observed_requires_lowercase_40hex": true,
    "read_failure_requires_observed_head_null": true,
    "malformed_record_policy": "RAISE_RPE02_TIMING_ERROR_BEFORE_ANY_SLA_VERDICT",
    "input_order_field": "scheduled_at_ns",
    "input_order_requirement": "STRICTLY_INCREASING_AS_SUPPLIED",
    "silent_sorting_forbidden": true
  },
  "eligibility_test_lock": {
    "detection_eligibility_field": "attempt_started_at_ns",
    "pre_release_target_field": "attempt_started_at_ns",
    "scheduled_at_ns_substitution_forbidden": true,
    "structural_breakers": [
      "ACTUAL_START_PRECEDES_SCHEDULED_SLOT",
      "REMOTE_COMPLETION_PRECEDES_ATTEMPT_START",
      "ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION",
      "DUPLICATE_FIXED_RATE_SLOT",
      "CADENCE_GAP",
      "SKIPPED_REQUIRED_ATTEMPT",
      "OBSERVATION_ORDER_NOT_STRICTLY_INCREASING"
    ]
  },
  "no_detection_semantics": {
    "rule": "NEXT_REQUIRED_FIXED_RATE_SLOT_FEASIBILITY",
    "last_scheduled_source": "LAST_SUPPLIED_AND_VALIDATED_SCHEDULED_SLOT",
    "next_required_slot_formula": "last_scheduled_at_ns + poll_interval_ns",
    "fail_condition": "next_required_slot_ns - controlled_source_release_started_at_ns > detection_latency_bound_ns",
    "fail_status": "FAIL_NO_DETECTION_BY_BOUND",
    "fail_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
    "otherwise_status": "INCOMPLETE_REAL_TIME_WINDOW",
    "last_remote_completion_alone_may_not_decide_no_detection": true,
    "exact_grid_parity_claim_may_remain_only_if_counterexamples_converge": true
  },
  "nb4_scope_adjudication": {
    "sla_endpoint": "remote_observation_completed_at_ns",
    "full_attempt_completion_role": "TIMELINE_AND_OVERLAP_EVIDENCE_ONLY",
    "last_attempt_full_completion_beyond_future_slot_alone_changes_sla": false,
    "no_real_attempt_overlap_execution_guarantee_stage": "RPE-05"
  },
  "packet_fidelity": {
    "historical_red_test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
    "final_preclosure_test_blob": "23618a9317c554099670e84482641a8014f8682d",
    "historical_red_must_be_sourced_from_historical_blob": true,
    "final_test_must_be_labeled_separately": true
  },
  "mandatory_red_cases": [
    "unknown outcome",
    "REMOTE_HEAD_OBSERVED without head",
    "READ_FAILURE with head",
    "outcome typo with target head",
    "actual-start eligibility differs from scheduled slot",
    "pre-release target handling differs from scheduled slot",
    "started before scheduled",
    "remote completion before started",
    "attempt completion before remote completion",
    "duplicate slot",
    "cadence gap",
    "skipped required attempt",
    "out-of-order supplied observations",
    "parity counterexample release 1 with slots 30 and 60",
    "parity counterexample release 30 with completions 31 and 90"
  ],
  "stop": "TARGETED_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}
~~~~

# GIT-BLOB-SOURCED COPY: ORIGINAL HISTORICAL RED TEST
Path: historical tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py
Authoritative Git blob: 089a72c736302abd08ea1267c149e2ef771240db
~~~~
﻿import importlib.util
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
~~~~

# GIT-BLOB-SOURCED COPY: ORIGINAL FINAL PRE-CLOSURE MAIN TEST
Path: tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py
Authoritative Git blob: 23618a9317c554099670e84482641a8014f8682d
~~~~
﻿import importlib.util
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

    def test_implementation_constants_match_governed_preregistration(self):
        g = load(GUARD, "rpe01_guard_for_rpe02_parity")
        doc = g.validate_governed_json(
            PREREG.read_text(encoding="utf-8"),
            SCHEMA.read_text(encoding="utf-8"),
        )
        m = load(MODULE, "rpe02_governed_config_parity")
        self.assertEqual(
            m.NANOSECONDS_PER_SECOND,
            doc["representation"]["nanoseconds_per_second"],
        )
        self.assertEqual(
            m.POLL_INTERVAL_NS,
            doc["representation"]["poll_interval_ns"],
        )
        self.assertEqual(
            m.DETECTION_LATENCY_BOUND_NS,
            doc["representation"]["detection_latency_bound_ns"],
        )

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
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED HISTORICAL RED TEST
Path: tests/obsidian_projection/test_rpe02_external_review_targeted_closure_v0_1.py
Authoritative Git blob: 0756598131911168a7cb5944c0ed465c7ebbd2a0
~~~~
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
~~~~

# GIT-BLOB-SOURCED COPY: FINAL IMPLEMENTATION
Path: tools/obsidian_projection/rpe02_real_time_model_v0_1.py
Authoritative Git blob: 31db5d944a25e54db81bd901a087cdc2039925ad
~~~~
"""RPE-02 V0.1: nanosecond-native real-time representation.

Pure timing qualification except capture_monotonic_clock_capability(), which records
host clock capability/evidence. No network, CLI, environment, filesystem config, or
P5-D4/Vault mutation authority exists in this module.
"""

from __future__ import annotations

import platform
import re
import sys
import time
from typing import Any, Mapping, Sequence


NANOSECONDS_PER_SECOND = 1_000_000_000
POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
_ALLOWED_OUTCOMES = {"READ_FAILURE", "REMOTE_HEAD_OBSERVED"}


class RPE02TimingError(ValueError):
    """Invalid RPE-02 timing evidence or plan."""


def _strict_int(name: str, value: object) -> int:
    if type(value) is not int:
        raise RPE02TimingError(f"{name} must be an integer nanosecond value")
    return value


def _strict_sha40(name: str, value: object) -> str:
    if type(value) is not str or _SHA40_RE.fullmatch(value) is None:
        raise RPE02TimingError(f"{name} must be lowercase 40-hex")
    return value


def make_real_time_plan(*, schedule_origin_ns: int) -> dict[str, Any]:
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    return {
        "schema": "ATDS_RPE02_REAL_TIME_PLAN_V0_1",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "schedule_origin_ns": origin,
        "poll_interval_ns": POLL_INTERVAL_NS,
        "detection_latency_bound_ns": DETECTION_LATENCY_BOUND_NS,
        "synthetic_reference_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE",
    }


def first_fixed_rate_slot_at_or_after_ns(
    timestamp_ns: int,
    poll_interval_ns: int,
    schedule_origin_ns: int,
) -> int:
    timestamp = _strict_int("timestamp_ns", timestamp_ns)
    interval = _strict_int("poll_interval_ns", poll_interval_ns)
    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
    if interval <= 0:
        raise RPE02TimingError("poll_interval_ns must be positive")
    if timestamp <= origin:
        return origin + interval
    delta = timestamp - origin
    q, r = divmod(delta, interval)
    return origin + (q if r == 0 else q + 1) * interval


def _blocked(code: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {
        "status": "BLOCKED_REQUIRES_ADJUDICATION",
        "failure_code": code,
        "detection_latency_ns": None,
    }
    out.update(extra)
    return out


def _validate_plan(plan: Mapping[str, Any]) -> tuple[int, int, int]:
    if not isinstance(plan, Mapping):
        raise RPE02TimingError("plan must be a mapping")
    if plan.get("normative_unit") != "INTEGER_MONOTONIC_NANOSECONDS":
        raise RPE02TimingError("plan normative unit mismatch")
    origin = _strict_int("plan.schedule_origin_ns", plan.get("schedule_origin_ns"))
    interval = _strict_int("plan.poll_interval_ns", plan.get("poll_interval_ns"))
    bound = _strict_int(
        "plan.detection_latency_bound_ns",
        plan.get("detection_latency_bound_ns"),
    )
    if interval != POLL_INTERVAL_NS:
        raise RPE02TimingError("poll interval is not the preregistered 30 seconds")
    if bound != DETECTION_LATENCY_BOUND_NS:
        raise RPE02TimingError("latency bound is not the preregistered 60 seconds")
    return origin, interval, bound


def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise RPE02TimingError(f"observations[{index}] must be a mapping")
    required = {
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
        "outcome",
        "observed_head",
    }
    if set(raw) != required:
        raise RPE02TimingError(
            f"observations[{index}] keys mismatch: "
            f"missing={sorted(required - set(raw))}, "
            f"unknown={sorted(set(raw) - required)}"
        )
    out = dict(raw)
    for key in (
        "scheduled_at_ns",
        "attempt_started_at_ns",
        "remote_observation_completed_at_ns",
        "attempt_completed_at_ns",
    ):
        out[key] = _strict_int(f"observations[{index}].{key}", out[key])
    if type(out["outcome"]) is not str or out["outcome"] not in _ALLOWED_OUTCOMES:
        raise RPE02TimingError(
            f"observations[{index}].outcome must be one of "
            f"{sorted(_ALLOWED_OUTCOMES)}"
        )
    if out["outcome"] == "READ_FAILURE":
        if out["observed_head"] is not None:
            raise RPE02TimingError(
                f"observations[{index}] READ_FAILURE may not carry observed_head"
            )
    else:
        out["observed_head"] = _strict_sha40(
            f"observations[{index}].observed_head",
            out["observed_head"],
        )
    return out


def qualify_detection_ns(
    *,
    plan: Mapping[str, Any],
    controlled_source_release_started_at_ns: int,
    target_head: str,
    observations: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    origin, interval, bound = _validate_plan(plan)
    release = _strict_int(
        "controlled_source_release_started_at_ns",
        controlled_source_release_started_at_ns,
    )
    target = _strict_sha40("target_head", target_head)
    if release <= origin:
        raise RPE02TimingError(
            "controlled_source_release_started_at_ns must be greater than schedule_origin_ns"
        )
    if not isinstance(observations, Sequence) or isinstance(
        observations, (str, bytes, bytearray)
    ):
        raise RPE02TimingError("observations must be a sequence")

    normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
    for index in range(1, len(normalized)):
        if normalized[index]["scheduled_at_ns"] < normalized[index - 1]["scheduled_at_ns"]:
            return _blocked("OBSERVATION_ORDER_NOT_STRICTLY_INCREASING")

    previous_scheduled: int | None = None
    previous_completion: int | None = None
    seen_slots: set[int] = set()

    for item in normalized:
        scheduled = item["scheduled_at_ns"]
        started = item["attempt_started_at_ns"]
        remote_done = item["remote_observation_completed_at_ns"]
        attempt_done = item["attempt_completed_at_ns"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if scheduled in seen_slots:
            return _blocked("DUPLICATE_FIXED_RATE_SLOT")
        seen_slots.add(scheduled)

        if previous_scheduled is not None and scheduled != previous_scheduled + interval:
            return _blocked("CADENCE_GAP")
        if started < scheduled:
            return _blocked("ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
        if started >= scheduled + interval:
            return _blocked("ACTUAL_START_MISSED_FIXED_RATE_SLOT")
        if remote_done < started:
            return _blocked("REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
        if remote_done > scheduled + interval:
            return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
        if attempt_done < remote_done:
            return _blocked("ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
        if previous_completion is not None and previous_completion > started:
            return _blocked("ATTEMPT_OVERLAP")

        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
            and started < release
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT",
                first_detection_scheduled_at_ns=scheduled,
                first_detection_attempt_started_at_ns=started,
                first_detection_remote_observation_completed_at_ns=remote_done,
                first_detection_attempt_completed_at_ns=attempt_done,
            )

        previous_scheduled = scheduled
        previous_completion = attempt_done

    first_required = first_fixed_rate_slot_at_or_after_ns(release, interval, origin)
    if normalized:
        slots_at_or_after_release = [
            item["scheduled_at_ns"]
            for item in normalized
            if item["scheduled_at_ns"] >= first_required
        ]
        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:
            return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    for item in normalized:
        if item["attempt_started_at_ns"] < release:
            continue
        if (
            item["outcome"] == "REMOTE_HEAD_OBSERVED"
            and item["observed_head"] == target
        ):
            latency = item["remote_observation_completed_at_ns"] - release
            status = (
                "PASS_DETECTED_WITHIN_BOUND"
                if latency <= bound
                else "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            )
            return {
                "status": status,
                "failure_code": None,
                "detection_latency_ns": latency,
                "first_detection_scheduled_at_ns": item["scheduled_at_ns"],
                "first_detection_attempt_started_at_ns": item["attempt_started_at_ns"],
                "first_detection_remote_observation_completed_at_ns": item[
                    "remote_observation_completed_at_ns"
                ],
                "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
            }

    next_required_slot = (
        normalized[-1]["scheduled_at_ns"] + interval
        if normalized
        else first_required
    )
    if next_required_slot - release > bound:
        return {
            "status": "FAIL_NO_DETECTION_BY_BOUND",
            "failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            "detection_latency_ns": None,
        }
    return {
        "status": "INCOMPLETE_REAL_TIME_WINDOW",
        "failure_code": None,
        "detection_latency_ns": None,
    }


def capture_monotonic_clock_capability() -> dict[str, Any]:
    info = time.get_clock_info("monotonic")
    sample_1 = time.monotonic_ns()
    sample_2 = time.monotonic_ns()
    if not info.monotonic:
        raise RPE02TimingError("host monotonic clock does not report monotonic capability")
    return {
        "schema": "ATDS_RPE02_MONOTONIC_CLOCK_CAPABILITY_V0_1",
        "api": "time.monotonic_ns",
        "metadata_api": "time.get_clock_info('monotonic')",
        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
        "monotonic": bool(info.monotonic),
        "adjustable": bool(info.adjustable),
        "resolution_seconds": info.resolution,
        "implementation": info.implementation,
        "sample_1_ns": sample_1,
        "sample_2_ns": sample_2,
        "same_process_host_domain": True,
        "python_version": sys.version.replace("\n", " "),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED MUTATION TEST
Path: tests/obsidian_projection/test_rpe02_external_review_targeted_mutation_v0_1.py
Authoritative Git blob: c00bb49ffa930aefcdce794c5b7a7c68211e586f
~~~~
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
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED QUALIFICATION JSON
Path: tools/obsidian_projection/rpe02_external_review_targeted_closure_qualification_v0_1.json
Authoritative Git blob: 97fac2708f24610fe3c4ebefa094f8ec1ba312bf
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-03",
  "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
  "external_review": {
    "verdict": "FAIL",
    "review_blob": "45766b0ad21a62447b9233ec1563eb85825f221d",
    "adjudication_blob": "836450b88ae69254dda77f548ede19bfaae1cb86"
  },
  "preregistration": {
    "head": "b8b2698252be7f630e435d17313cd1058bec2a51",
    "blob": "cafee7194155944eb059ead466fd6bc517edde58",
    "schema_blob": "d67da710e63643c26c0a004cc38109ff4e301b25"
  },
  "targeted_red": {
    "head": "afaafb9f3b9fb3a4d90cfa912b7eb176abc19161",
    "test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
    "report_blob": "b558fceaf0b214715ef65cd710ebb391464778d0",
    "result": "15 tests; 7 failures; 8 passes"
  },
  "final_candidate": {
    "head": "4a28540eafa82fd136dd4a402ef552f22f817f36",
    "implementation_blob": "31db5d944a25e54db81bd901a087cdc2039925ad",
    "targeted_test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
    "targeted_mutation_blob": "c00bb49ffa930aefcdce794c5b7a7c68211e586f"
  },
  "closures": {
    "bf1": "CLOSED_CANDIDATE",
    "nb1": "CLOSED_CANDIDATE",
    "nb2": "CLOSED_CANDIDATE",
    "nb3": "CLOSED_CANDIDATE",
    "nb4": "SCOPE_ADJUDICATED_RPE05_EXECUTION_GUARANTEE",
    "nb5": "PACKET_REBUILD_REQUIRED_AND_AUTHORIZED"
  },
  "final_semantics": {
    "outcomes": [
      "READ_FAILURE",
      "REMOTE_HEAD_OBSERVED"
    ],
    "successful_remote_observation_requires_lowercase_40hex": true,
    "read_failure_requires_null_head": true,
    "malformed_observation": "RPE02TimingError before SLA verdict",
    "observation_order": "supplied scheduled_at_ns may not decrease; duplicates retain DUPLICATE_FIXED_RATE_SLOT",
    "release_eligibility": "attempt_started_at_ns",
    "no_detection_rule": "next_required_slot_ns - release_ns > bound_ns",
    "no_detection_failure_code": "NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
    "exact_bound_without_detection": "INCOMPLETE_REAL_TIME_WINDOW",
    "sla_endpoint": "remote_observation_completed_at_ns",
    "full_attempt_completion_role": "TIMELINE_AND_OVERLAP_EVIDENCE_ONLY",
    "no_real_attempt_overlap_execution_guarantee_stage": "RPE-05"
  },
  "tests": {
    "targeted_green": "15/15 PASS",
    "targeted_mutation": "12/12 PASS / 12 mutants killed",
    "full_targeted_regression": "162/162 PASS"
  },
  "protected_diffs": {
    "p5e_contract": 0,
    "p5e_synthetic_model": 0,
    "p5d4_runtime": 0
  },
  "packet_fidelity": {
    "original_historical_red_test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
    "original_final_test_blob": "23618a9317c554099670e84482641a8014f8682d",
    "targeted_historical_red_test_blob": "0756598131911168a7cb5944c0ed465c7ebbd2a0",
    "labels_must_remain_distinct": true
  },
  "claim_boundary": {
    "rpe02_human_adopted": false,
    "rpe04_opened": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_authorized": false
  },
  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}
~~~~

# GIT-BLOB-SOURCED COPY: TARGETED QUALIFICATION REPORT
Path: reports/program/...RPE02-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
Authoritative Git blob: 1159b65345b15b5a6ee32c3bd320ee3ab3a0ef46
~~~~
# RPE-02 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION

Date: 2026-10-03

## Result

`RPE-02 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`

The prior external verdict was `FAIL`. No human adoption is created by this qualification.

## Closure identities

External review blob:
`45766b0ad21a62447b9233ec1563eb85825f221d`

Internal adjudication:
`836450b88ae69254dda77f548ede19bfaae1cb86`

Targeted preregistration:
`cafee7194155944eb059ead466fd6bc517edde58`

Targeted preregistration schema:
`d67da710e63643c26c0a004cc38109ff4e301b25`

Targeted RED HEAD:
`afaafb9f3b9fb3a4d90cfa912b7eb176abc19161`

Targeted RED test:
`0756598131911168a7cb5944c0ed465c7ebbd2a0`

Targeted RED report:
`b558fceaf0b214715ef65cd710ebb391464778d0`

Final candidate HEAD:
`4a28540eafa82fd136dd4a402ef552f22f817f36`

Final implementation:
`31db5d944a25e54db81bd901a087cdc2039925ad`

Targeted mutation tests:
`c00bb49ffa930aefcdce794c5b7a7c68211e586f`

## BF-1

Observation integrity is now closed before business verdicting.

Allowed outcome vocabulary is exactly:
- READ_FAILURE;
- REMOTE_HEAD_OBSERVED.

REMOTE_HEAD_OBSERVED requires a lowercase 40-hex head.
READ_FAILURE requires observed_head = null.
Unknown outcomes and incoherent outcome/head combinations raise RPE02TimingError before any SLA status can be produced.

## NB-1

The actual attempt start is test-locked as the release-eligibility field in both:
- first-detection eligibility;
- pre-release target handling.

Mutation tests also lock:
- actual start before scheduled;
- remote completion before actual start;
- attempt completion before remote completion;
- duplicate slot;
- cadence gap;
- skipped required attempt.

## NB-2

No-detection semantics now follow fixed-rate feasibility:

`next_required_slot_ns - release_ns > bound_ns`
→ `FAIL_NO_DETECTION_BY_BOUND`
with `NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND`.

At exact equality, the result remains INCOMPLETE because a future attempt can still meet the bound exactly.

Both external-review counterexamples now converge with the adopted synthetic reference.

## NB-3

Observations are no longer silently sorted.

A supplied scheduled timestamp lower than the preceding supplied timestamp returns:
`BLOCKED_REQUIRES_ADJUDICATION / OBSERVATION_ORDER_NOT_STRICTLY_INCREASING`.

Duplicate slots retain their dedicated failure code.

## NB-4 adjudication

The SLA endpoint remains:
`remote_observation_completed_at_ns`.

`attempt_completed_at_ns` remains timeline/overlap evidence only.

The runtime execution guarantee `NO REAL ATTEMPT OVERLAP` is explicitly carried to RPE-05.

## Evidence

Targeted closure:
`15 / 15 PASS`

Targeted mutation discrimination:
`12 / 12 PASS; 12 / 12 mutants killed`

P5-E + RPE-01 + RPE-02 regression:
`162 / 162 PASS`

Protected diffs:
- P5-E contract = 0;
- P5-E synthetic model = 0;
- P5-D4 runtime = 0.

## Packet-fidelity rule

The rebuilt delta-review packet must distinguish:
- original historical RED test blob `089a72c736302abd08ea1267c149e2ef771240db`;
- original final test blob `23618a9317c554099670e84482641a8014f8682d`;
- targeted historical RED test blob `0756598131911168a7cb5944c0ed465c7ebbd2a0`.

No final test may be labeled as a historical RED copy.

## Authority

RPE-02 human adoption = pending.
RPE-04/05/06 = closed.
REAL P5-E = closed.
~~~~
