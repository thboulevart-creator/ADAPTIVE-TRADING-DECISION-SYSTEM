# P5-E V0.1 — FINAL PRE-ADOPTION EVIDENCE HYGIENE — SELF-CONTAINED DELTA REVIEW PACKET

Date: 2026-10-02

## Independent reviewer mandate

Review only the delta:

`P5-E V0.1 — FINAL PRE-ADOPTION EVIDENCE HYGIENE`

This delta follows an external:

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

on the BB1 normative-guard closure.

The authorized delta addresses only:
- N1 — explicit contract/test coverage for read completion before attempt start;
- N2 — provenance label of the newly introduced D2-file test;
- N3 — mutation-sweep interpretation correction;
- N6 — stale `built_against_head` metadata.

Do not reopen N4, N5, NB2, NB3, NB5 or NB9 except to detect accidental claim leakage.

Do not authorize real P5-E execution or human adoption.

## Base and delta identity

Base reviewed HEAD:
`148c68cb43e77ebff9fb98af91109668b949d62f`

Delta technical HEAD:
`51b581cdab96e32a2f3be1b8a2ed94982de4ceb7`

Current contract blob:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Current model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Important:
the model blob is unchanged from the externally reviewed BB1 candidate.

Current evidence-matrix blob:
`454889848803bdaeed70a6fdfd80033ff22b8e72`

Current adversarial-test blob:
`de4133706661c5d92cb2d7b93cf1f2573e1a916b`

Current BB1-closure-test blob:
`e019f67d04560313a8f98a6fac8b5073c1301f0e`

Final-hygiene RED test blob:
`7e2e71b289d5bbde9c08cea1170794318a662b38`

## Evidence claims to audit

RED:
```text
6 tests
3 failures
1 error
1 behavioral N1 pass
```

Final targeted surface:
```text
67 / 67 PASS
MODEL_DIFF_COUNT = 0
```

No full Obsidian suite was executed by this delta.

Real P5-D4 fingerprints remained:
```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Required delta questions

### N1

1. Is `read_completion_before_attempt_start_forbidden = true` now explicit in the contract?
2. Is that field strictly guarded by the canonical invariant checker?
3. Is there a dedicated behavioral test for `READ_COMPLETION_PRECEDES_ATTEMPT_START`?
4. Did the delta leave the model implementation byte-identical?
5. Does the test actually falsify the impossible record rather than merely checking a declarative field?

### N2

6. Do only the two entries using the newly introduced D2-file test change provenance to `DIRECT_P5E`?
7. Do queue-capacity proofs remain `REUSED_QUALIFIED_P5D2_P5D4`?
8. Does the semantic test path/method remain exact?

### N3

9. Does the addendum correctly distinguish:
   - semantic sweep without binding: 13 survivors, all non-normative;
   - full surface with object binding: 0 survivors?
10. Does it avoid claiming that the 0-survivor object-binding result independently proves semantic completeness?

### N6

11. Is stale `built_against_head` absent?
12. Was it correctly not replaced by a self-referential final HEAD?
13. Do `covered_contract_blob` and `covered_model_blob` remain exact and binding?

## Additional checks

14. Did the delta introduce any model/runtime behavior change beyond tests/contract/matrix/documentation?
15. Does any evidence label still overstate qualification provenance?
16. Did any deferred finding become silently claimed as solved?
17. Did any authority boundary change?
18. Are all current matrix-referenced blobs consistent with the current files?
19. Does the 67-test targeted surface reproduce cleanly?

## Required output

Return exactly one top-level verdict:

`VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL`

Then provide:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- N1_CHECK
- N2_CHECK
- N3_CHECK
- N6_CHECK
- OBJECT_BINDING_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_ACTION_BEFORE_HUMAN_ADJUDICATION

For each finding:
- cite the exact packet section;
- identify exact field/function/test/matrix entry;
- distinguish OBSERVED from INFERENCE;
- state BLOCKING or NON_BLOCKING.

This review does not authorize REAL P5-E.

This review does not constitute human normative adoption.

---

# EXACT TECHNICAL DIFF — BASE TO DELTA
~~~~diff
diff --git a/tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py b/tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py
index ed4a2c3..e019f67 100644
--- a/tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py
+++ b/tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py
@@ -189,8 +189,9 @@ class TestP5EBB1NormativeGuardClosureV01(unittest.TestCase):
             )
             self.assertEqual(
                 entry["evidence_kind"],
-                "REUSED_QUALIFIED_P5D2_P5D4",
+                "DIRECT_P5E",
             )
+
     def test_nb7_incomplete_window_is_explicit_non_pass(self):
         synthetic = self.contract["synthetic_timing_model"]
         self.assertIn(
diff --git a/tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py b/tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
index 16b6fdb..de41337 100644
--- a/tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
+++ b/tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
@@ -155,6 +155,7 @@ def assert_contract_invariants(contract):
     assert synthetic["attempt_overruns_next_required_slot_failure_code"] == "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
     assert synthetic["duplicate_fixed_rate_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
     assert synthetic["duplicate_fixed_rate_slot_failure_code"] == "DUPLICATE_FIXED_RATE_SLOT"
+    assert synthetic["read_completion_before_attempt_start_forbidden"] is True
     assert synthetic["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
     assert synthetic["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
     assert synthetic["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
diff --git a/tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py b/tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py
new file mode 100644
index 0000000..7e2e71b
--- /dev/null
+++ b/tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py
@@ -0,0 +1,100 @@
+import copy
+import importlib.util
+import json
+import unittest
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[2]
+CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
+MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
+MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"
+ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"
+
+TARGET = "a" * 40
+D2_METHOD = "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation"
+
+
+def load_json(path):
+    return json.loads(path.read_text(encoding="utf-8"))
+
+
+def load_module(path, name):
+    spec = importlib.util.spec_from_file_location(name, path)
+    if spec is None or spec.loader is None:
+        raise AssertionError(f"cannot load {path}")
+    module = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(module)
+    return module
+
+
+def obs(scheduled, completed, outcome, head=None):
+    return {
+        "scheduled_at_seconds": scheduled,
+        "completed_at_seconds": completed,
+        "outcome": outcome,
+        "observed_head": head,
+    }
+
+
+class TestP5EFinalPreAdoptionEvidenceHygieneV01(unittest.TestCase):
+    def test_n1_contract_explicitly_forbids_completion_before_attempt_start(self):
+        contract = load_json(CONTRACT)
+        synthetic = contract["synthetic_timing_model"]
+        self.assertTrue(
+            synthetic["read_completion_before_attempt_start_forbidden"]
+        )
+
+    def test_n1_behavior_blocks_completion_before_attempt_start(self):
+        model = load_module(MODEL, "p5e_final_hygiene_n1_model")
+        result = model.qualify_detection(
+            plan=model.make_timing_plan(),
+            source_release_at_seconds=1,
+            target_head=TARGET,
+            observations=[
+                obs(60, 40, "REMOTE_HEAD_OBSERVED", TARGET),
+            ],
+        )
+        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
+        self.assertEqual(
+            result["failure_code"],
+            "READ_COMPLETION_PRECEDES_ATTEMPT_START",
+        )
+
+    def test_n1_contract_field_is_strictly_guarded(self):
+        contract = load_json(CONTRACT)
+        candidate = copy.deepcopy(contract)
+        candidate["synthetic_timing_model"][
+            "read_completion_before_attempt_start_forbidden"
+        ] = False
+        adv = load_module(ADV, "p5e_final_hygiene_n1_adv")
+        with self.assertRaises(AssertionError):
+            adv.assert_contract_invariants(candidate)
+
+    def test_n2_new_d2_file_test_is_labelled_direct_p5e(self):
+        matrix = load_json(MATRIX)
+        entries = [
+            matrix["required_synthetic_cases"][
+                "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
+            ],
+            matrix["base_breakers"][
+                "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD"
+            ],
+        ]
+        for entry in entries:
+            self.assertEqual(entry["test_method"], D2_METHOD)
+            self.assertEqual(entry["evidence_kind"], "DIRECT_P5E")
+
+    def test_n6_stale_built_against_head_is_absent(self):
+        matrix = load_json(MATRIX)
+        self.assertNotIn("built_against_head", matrix)
+
+    def test_n6_object_blobs_remain_the_binding_authority(self):
+        matrix = load_json(MATRIX)
+        self.assertTrue(matrix["covered_object_drift_must_fail"])
+        self.assertRegex(matrix["covered_contract_blob"], r"^[0-9a-f]{40}$")
+        self.assertRegex(matrix["covered_model_blob"], r"^[0-9a-f]{40}$")
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json b/tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
index 7e3e18b..43d2e45 100644
--- a/tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
+++ b/tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
@@ -80,7 +80,8 @@
     "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
     "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
     "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
-    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT"
+    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
+    "read_completion_before_attempt_start_forbidden": true
   },
   "authority_boundary": {
     "observer_may_create_governance_authority": false,
diff --git a/tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json b/tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json
index 88e13a4..4548898 100644
--- a/tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json
+++ b/tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json
@@ -1,7 +1,6 @@
 {
   "schema": "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
   "qualification_scope": "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
-  "built_against_head": "95881afe5f03783de3c933d2c8ee65373220f3ed",
   "binding": "GIT_HASH_OBJECT_WITH_PATH_FILTERS",
   "real_p5e_execution_authorized": false,
   "real_60_second_sla_qualified": false,
@@ -77,7 +76,7 @@
       "path": "tests/obsidian_projection/test_observer_tick.py",
       "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
       "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
-      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
+      "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     }
   },
@@ -85,56 +84,56 @@
     "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "DETECTION_BOUND_ABOVE_60_ACCEPTED": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_previously_surviving_contract_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "SLEEP_USED_IN_SYNTHETIC_MODEL": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "NETWORK_USED_IN_SYNTHETIC_MODEL": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
@@ -198,62 +197,62 @@
       "path": "tests/obsidian_projection/test_observer_tick.py",
       "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
       "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
-      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
+      "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "EVALUATION_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "PROMOTION_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "PUBLICATION_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "REAL_POLLING_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "P6_AUTHORITY_BECOMES_TRUE": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     },
     "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS": {
       "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
       "test_method": "TestP5EAdversarialV01.test_claim_and_tip_mutations_are_rejected",
-      "blob": "16b6fdb9c0bb5be980e5db59eb6f87f93e160205",
+      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
       "evidence_kind": "DIRECT_P5E",
       "verdict": "PASS"
     }
@@ -324,7 +323,7 @@
     "unmapped": 0,
     "deferred": 0
   },
-  "covered_contract_blob": "7e3e18ba946246065b43bc5fbabdc35980140eb9",
+  "covered_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
   "covered_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
   "covered_object_drift_must_fail": true
 }
~~~~

# SOURCE: FINAL HYGIENE INTERNAL ADJUDICATION
Path: reports/program/2026-10-02-OBSIDIAN-P5E-FINAL-PRE-ADOPTION-EVIDENCE-HYGIENE-INTERNAL-ADJUDICATION.md
~~~~
# P5-E V0.1 â€” FINAL PRE-ADOPTION EVIDENCE HYGIENE â€” INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Branch:
`feat/obsidian-projection-p5e-v0.1-final-pre-adoption-evidence-hygiene`

Opening HEAD:
`148c68cb43e77ebff9fb98af91109668b949d62f`

Opening worktree:
`CLEAN`

Contract blob:
`7e3e18ba946246065b43bc5fbabdc35980140eb9`

Model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

Evidence matrix blob:
`88e13a447a96455d4ac1d9d0f96e11b29329616d`
## External re-review result

External verdict:
`PASS_WITH_NON_BLOCKING_NOTES`

Blocking findings:
`NONE`

The reviewer independently reconstructed the candidate identities and reported:
- P5-E surface: 61 / 61 PASS;
- D2: 55 / 55 PASS;
- the 22 distinct tests referenced by the evidence matrix passed;
- BB1 semantic sweep excluding object-binding tests: only the 13 preregistered non-normative leaves survived.

Therefore:
`BB1_EXTERNAL_CLOSURE = PASS`

This external review creates no execution or adoption authority.
## N1 â€” read completion before attempt start

Adjudication:
`VALID â€” CLOSE BEFORE HUMAN ADOPTION`

Current runtime behavior is correct:
`READ_COMPLETION_PRECEDES_ATTEMPT_START`

However the rule is not represented by a dedicated contract field plus dedicated behavioral test.

Authorized correction:
- add one explicit contract field;
- add one strict guard for that field;
- add one behavioral test demonstrating fail-closed behavior.

No model behavior change is required.

## N2 â€” provenance label for newly added D2-file test

Adjudication:
`VALID â€” CLOSE BEFORE HUMAN ADOPTION`

The two evidence-matrix entries using:
`ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation`

currently label it:
`REUSED_QUALIFIED_P5D2_P5D4`

That is provenance-overstated because the test was introduced by the BB1 closure.

Authorized correction:
`evidence_kind = DIRECT_P5E`
for those two entries only.
## N3 â€” mutation-sweep reporting

Adjudication:
`VALID â€” DOCUMENTARY CORRECTION`

The previous wording conflated two different measurements.

Correct reporting must distinguish:

```text
SEMANTIC SWEEP WITHOUT CONTRACT/MODEL BINDING TESTS
= 13 survivors
= all preregistered non-normative metadata

FULL SURFACE WITH CONTRACT/MODEL BINDING
= 0 survivors
```

The first measurement demonstrates semantic guard coverage.

The second demonstrates object-identity binding.

No claim that "0 survivors exceeds the semantic criterion" is permitted.

## N4 â€” added-key mutation coverage

Adjudication:
`VALID â€” DEFERRED`

Current object binding prevents silent drift of added keys.

Closed-schema / unexpected-key rejection is useful hardening but is not required to close the present candidate.

Record as a prerequisite before REAL P5-E.

No mutation authorized here.
## N5 â€” equality and boundary semantics

Adjudication:
`VALID â€” DEFERRED`

Examples include:
- `> / >=` at overrun and overlap boundaries;
- source release exactly on a slot;
- exact feasibility at the 60-second boundary;
- first-slot rounding for non-aligned releases;
- uppercase SHA acceptance.

Current behavior is coherent but not exhaustively frozen by dedicated tests.

These boundaries are mandatory hardening before REAL P5-E.

No mutation authorized here.

## N6 â€” stale matrix construction metadata

Adjudication:
`VALID â€” CLOSE BEFORE HUMAN ADOPTION`

Current:
`built_against_head = 95881afe5f03783de3c933d2c8ee65373220f3ed`

This is stale and conflicts with the newer object bindings.

Authorized correction:
remove the stale `built_against_head` field.

Do not replace it with the final branch HEAD, because that would make the matrix self-referential and mechanically unstable.

Object identity authority remains:
- `covered_contract_blob`;
- `covered_model_blob`.
## N7 â€” full re-break evidence scope

Adjudication:
`VALID LIMITATION â€” NO CURRENT CORRECTION`

The previous authorized full-suite budget is already consumed.

No new full-suite is authorized by this hygiene pass.

The reviewer limitation that 282/282 and 1486/1486 were not independently reproducible is preserved as a provenance note only.

## N8 â€” P5-A future-design-debt metadata classification

Adjudication:
`NON_MATERIAL_FOR_CURRENT_ADOPTION`

The field:
`queue_and_supersession.p5a_supersession_intent_preserved_as_future_design_debt`

does not grant current behavioral authority.

It remains non-normative metadata in this closure.

## Deferred earlier findings

NB2, NB3, NB5 and NB9 remain deferred exactly as previously recorded.

This hygiene pass does not reopen them.
## Real P5-D4 fingerprint before hygiene

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Authorized delta only

This pass may modify only:
- P5-E contract fields/tests needed for N1;
- evidence-matrix labels/metadata needed for N2/N6;
- documentary evidence needed for N3;
- mechanically necessary blob bindings;
- targeted tests/reports/delta-review packet.

It may not run another full Obsidian suite.

## Current boundary

```text
BB1_EXTERNAL_REREVIEW = PASS_WITH_NON_BLOCKING_NOTES
N1 = IN_SCOPE
N2 = IN_SCOPE
N3 = IN_SCOPE_DOCUMENTARY
N6 = IN_SCOPE
N4 = DEFERRED_BEFORE_REAL_P5E
N5 = DEFERRED_BEFORE_REAL_P5E
N7 = NO_ACTION
N8 = NO_ACTION

REAL_P5E = CLOSED
HUMAN_NORMATIVE_ADOPTION = CLOSED
```

~~~~

# SOURCE: FINAL HYGIENE RED EVIDENCE
Path: reports/program/2026-10-02-OBSIDIAN-P5E-FINAL-PRE-ADOPTION-EVIDENCE-HYGIENE-RED.md
~~~~
# P5-E V0.1 â€” FINAL PRE-ADOPTION EVIDENCE HYGIENE â€” RED

Date: 2026-10-02

## Scope

Targeted RED for the authorized delta-only hygiene pass N1 / N2 / N6.

Base adjudication HEAD:
`4f280938a0f1bbc569aabffe0dc92daa31f37ae1`

## RED test

`tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py`

Created before any contract or evidence-matrix correction.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_p5e_final_pre_adoption_evidence_hygiene_v0_1
```

## Observed result

```text
Ran 6 tests in 0.012s

FAILED (failures=3, errors=1)

RED_EXIT=1
```

Interpretation:

- N1 behavioral runtime case already passes:
  `READ_COMPLETION_PRECEDES_ATTEMPT_START`;
- N1 explicit contract field is absent;
- N1 strict invariant guard is absent;
- N2 still labels the two newly introduced D2-file tests as
  `REUSED_QUALIFIED_P5D2_P5D4`;
- N6 stale `built_against_head` remains present;
- covered contract/model blob authority remains present and valid.

## Authority

No runtime model behavior was changed by this RED.

No full Obsidian suite was executed.

No real P5-E operation was executed.

`REAL_P5E = CLOSED`

~~~~

# SOURCE: FINAL HYGIENE GREEN EVIDENCE
Path: reports/program/2026-10-02-OBSIDIAN-P5E-FINAL-PRE-ADOPTION-EVIDENCE-HYGIENE-GREEN.md
~~~~
# P5-E V0.1 â€” FINAL PRE-ADOPTION EVIDENCE HYGIENE â€” GREEN

Date: 2026-10-02

## Scope

Delta-only closure of N1, N2, N3 and N6 after external
`PASS_WITH_NON_BLOCKING_NOTES`.

No model behavior change was authorized or made.

No full Obsidian suite was executed.

## RED predecessor

RED HEAD:
`033e9fdc750c7bbf02ad604fc067f009ed66dbd2`

RED test blob:
`7e2e71b289d5bbde9c08cea1170794318a662b38`

RED evidence blob:
`f51f763b491060dba24179fd81e3a5f5eea6560f`

## N1 closure

The contract now explicitly declares:

`synthetic_timing_model.read_completion_before_attempt_start_forbidden = true`

The canonical P5-E invariant checker strictly guards this field.

A dedicated behavioral test verifies that an observation with:

```text
scheduled_at_seconds = 60
completed_at_seconds = 40
```

returns:

```text
BLOCKED_REQUIRES_ADJUDICATION
READ_COMPLETION_PRECEDES_ATTEMPT_START
```

The model implementation itself was not modified.

## N2 closure

The evidence entries:

- `SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD`
- `PENDING_HEAD_RETARGETED_TO_NEWER_HEAD`

still point to:

`ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation`

Their provenance label is now:

`DIRECT_P5E`

rather than:

`REUSED_QUALIFIED_P5D2_P5D4`

No D2 runtime or D2 behavioral implementation was modified.

## N6 closure

The stale matrix field:

`built_against_head = 95881afe5f03783de3c933d2c8ee65373220f3ed`

was removed.

It was not replaced by a final-HEAD field because such a value would be self-referential and mechanically unstable.

Binding authority remains the exact covered object identities:

- `covered_contract_blob`
- `covered_model_blob`

## Corrected prospective identities

Contract:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

P5-E adversarial test:
`de4133706661c5d92cb2d7b93cf1f2573e1a916b`

BB1 closure test:
`e019f67d04560313a8f98a6fac8b5073c1301f0e`

Evidence matrix:
`454889848803bdaeed70a6fdfd80033ff22b8e72`

## Targeted execution

Executed modules:

- P5-E contract tests;
- P5-E adversarial tests;
- prior external-review closure tests;
- evidence-matrix tests;
- BB1 normative-guard closure tests;
- final pre-adoption hygiene tests.

Observed:

```text
Ran 67 tests in 1.621s

OK

TARGETED_EXIT=0
MODEL_DIFF_COUNT=0
```

An intermediate recheck failed only because the previously qualified BB1 test still asserted the old N2 provenance label. That assertion was mechanically aligned to the newly authorized `DIRECT_P5E` semantics. Queue-capacity evidence remained `REUSED_QUALIFIED_P5D2_P5D4`.

## Deferred findings preserved

No correction was made for:
- N4;
- N5;
- NB2;
- NB3;
- NB5;
- NB9.

No new full-suite was executed.

## Current boundary

```text
FINAL_PRE_ADOPTION_EVIDENCE_HYGIENE = TARGETED_GREEN
DELTA_EXTERNAL_REVIEW = NEXT
HUMAN_NORMATIVE_ADOPTION = CLOSED
REAL_P5E = CLOSED
P6 = CLOSED
```

~~~~

# SOURCE: N3 MUTATION-SWEEP INTERPRETATION ADDENDUM
Path: reports/program/2026-10-02-OBSIDIAN-P5E-BB1-MUTATION-SWEEP-INTERPRETATION-ADDENDUM.md
~~~~
# P5-E V0.1 â€” BB1 MUTATION-SWEEP INTERPRETATION ADDENDUM

Date: 2026-10-02

## Purpose

This addendum corrects the interpretation of the BB1 mutation-sweep evidence without rewriting the historical reports.

## Correct distinction

Two different measurements exist and must not be conflated.

### Semantic guard measurement without contract/model binding tests

External re-review independently excluded the two object-binding tests and observed:

```text
CONTRACT LEAVES = 161
SURVIVORS = 13
```

All 13 survivors are the preregistered non-normative / historical metadata leaves.

Therefore the semantic conclusion is:

`NORMATIVE_SEMANTIC_SURVIVORS = 0`

### Full qualification surface with contract/model object binding

With the object-binding tests included, the prior BB1 qualification observed:

```text
CONTRACT LEAVES = 161
SURVIVORS = 0
```

This proves that any byte-level contract drift invalidates the covered-object binding.

It is not an independent measure of semantic invariant completeness.

## Corrected claim

Do not state that:

`FULL_SURFACE_SURVIVORS = 0`

"exceeds" the semantic mutation criterion.

Instead state:

```text
SEMANTIC SWEEP WITHOUT OBJECT-BINDING TESTS
= 13 survivors
= all non-normative metadata
= 0 normative survivors

FULL SURFACE WITH OBJECT BINDING
= 0 survivors
= object identity drift rejected
```

These two measurements answer different questions and are both retained.

## Authority

This addendum changes no runtime, contract authority, queue semantics or P5-E execution authority.

`REAL_P5E = CLOSED`

~~~~

# SOURCE: CURRENT P5-E CONTRACT
Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
  "qualification_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "objective": {
    "name": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "purpose": "Define the temporal and authority contract required before any real repeated observation experiment may claim bounded near-real-time behavior around the already-qualified P5-D4 bounded loop.",
    "this_stage_is_not_real_end_to_end_execution": true,
    "this_stage_may_not_claim_continuous_synchronization": true
  },
  "near_real_time_timing": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "instantaneous_realtime_claim_forbidden": true,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true,
    "detection_latency_definition": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "FIXED_RATE_30_SECOND_GRID",
    "single_transient_read_failure_may_still_meet_60_second_bound": false,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true,
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "remote_head_available_time_is_measurable_origin": false,
    "real_latency_metric": "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "attempt_start_and_read_completion_are_distinct": true,
    "read_duration_is_included_in_detection_latency": true,
    "eligible_detection_attempt_must_start_at_or_after_release": true,
    "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation.",
    "schedule_semantics": "FIXED_RATE",
    "schedule_origin_seconds": 0,
    "observation_record_fields": [
      "scheduled_at_seconds",
      "completed_at_seconds",
      "outcome",
      "observed_head"
    ],
    "head_identity_required_on_successful_remote_observation": true,
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "explicit_non_pass_statuses": [
      "INCOMPLETE_SYNTHETIC_WINDOW"
    ],
    "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
    "read_completion_before_attempt_start_forbidden": true
  },
  "authority_boundary": {
    "observer_may_create_governance_authority": false,
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "head_transition_policy": {
    "same_head_result": "NOOP",
    "same_head_queue_growth_forbidden": true,
    "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "non_fast_forward_auto_continue_forbidden": true,
    "unknown_ancestry_auto_continue_forbidden": true,
    "active_or_pending_candidate_retarget_forbidden": true
  },
  "queue_and_supersession": {
    "precedence_rule": "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT",
    "p5a_supersession_intent_preserved_as_future_design_debt": true,
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "coalescing_authorized": false,
    "new_coalescing_semantic_event_authorized": false,
    "pending_head_retarget_forbidden": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_mutate_p5d2_state": true,
    "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": true
  },
  "failure_and_freshness": {
    "fail_closed_default": true,
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved": true,
    "latency_bound_breach_result": "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED",
    "queue_capacity_exhaustion_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "timing_inconsistency_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION"
  },
  "end_to_end_definition": {
    "real_end_to_end_stages": [
      "SOURCE_HEAD_BECOMES_OBSERVABLE",
      "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
      "HEAD_TRANSITION_CLASSIFIED",
      "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
      "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
      "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
      "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
      "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
    ],
    "current_stage_may_qualify_only": [
      "TIMING_CONTRACT",
      "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
      "AUTHORITY_BOUNDARIES",
      "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true,
    "transient_tip_exact_detection_sla_not_qualified": true,
    "real_remote_availability_to_detection_sla_not_qualified": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED",
      "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
      "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
    ]
  },
  "real_context_evidence_only": {
    "live_projection_head_at_opening": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head_at_opening": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_observed_during_contract_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "must_not_be_used_as_real_experiment_execution": true,
    "must_not_be_mutated_by_contract_qualification": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
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
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "next_gate_after_candidate_qualification": {
    "external_adversarial_review_required_before_normative_adoption": true,
    "human_adjudication_required_after_external_review": true,
    "real_p5e_execution_requires_separate_human_authorization": true,
    "p6_remains_closed": true,
    "external_adversarial_rereview_required": true,
    "human_adjudication_before_external_rereview_forbidden": true
  },
  "tip_visibility_semantics": {
    "observed_remote_tip_definition": "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_queue_coalescing": false,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false,
    "future_ancestry_enumeration_requires_separate_qualification": true,
    "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "external_review_targeted_closure": {
    "findings": {
      "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
      "B2": "CONFIRMED_BLOCKING",
      "B3": "CONFIRMED_BLOCKING",
      "B4": "CONFIRMED_BLOCKING",
      "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
    },
    "required_breakers": [
      "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
      "CADENCE_GAP_ACCEPTED",
      "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
      "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
      "READ_COMPLETION_LATENCY_HIDDEN",
      "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
      "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
      "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
    ],
    "requirement_to_executable_evidence_matrix_required": true,
    "all_required_cases_must_be_mapped": true,
    "all_base_breakers_must_be_mapped": true,
    "all_targeted_closure_breakers_must_be_mapped": true,
    "unmapped_requirement_result": "BLOCKED",
    "external_rereview_required_before_human_normative_adoption": true
  }
}

~~~~

# SOURCE: UNCHANGED P5-E MODEL
Path: tools/obsidian_projection/p5e_near_real_time_model.py
~~~~
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1_AMENDED"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1_AMENDED"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_SCHEDULE_ORIGIN_SECONDS = 0
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "REMOTE_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def _valid_head(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(ch in "0123456789abcdef" for ch in value)


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
    schedule_origin_seconds: int = _SCHEDULE_ORIGIN_SECONDS,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    if schedule_origin_seconds != _SCHEDULE_ORIGIN_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 synthetic fixed-rate origin must remain exactly zero"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": _POLL_INTERVAL_SECONDS,
        "detection_latency_seconds_max": _DETECTION_LATENCY_SECONDS_MAX,
        "schedule_origin_seconds": _SCHEDULE_ORIGIN_SECONDS,
        "schedule_semantics": "FIXED_RATE",
        "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
        "measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
        schedule_origin_seconds=plan.get("schedule_origin_seconds"),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _blocked(failure_code: str) -> dict[str, Any]:
    return _result(
        status="BLOCKED_REQUIRES_ADJUDICATION",
        failure_code=failure_code,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )


def _result(
    *,
    status: str,
    failure_code: str | None,
    detection_latency_seconds: int | None,
    first_detection_scheduled_at_seconds: int | None,
    first_detection_completed_at_seconds: int | None,
    observed_head: str | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "failure_code": failure_code,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_scheduled_at_seconds": (
            first_detection_scheduled_at_seconds
        ),
        "first_detection_completed_at_seconds": (
            first_detection_completed_at_seconds
        ),
        "observed_head": observed_head,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def _first_fixed_rate_slot_at_or_after(
    *,
    instant_seconds: int,
    interval: int,
    origin: int,
) -> int:
    first_slot = origin + interval
    if instant_seconds <= first_slot:
        return first_slot
    delta = instant_seconds - origin
    quotient, remainder = divmod(delta, interval)
    return origin + (quotient + (1 if remainder else 0)) * interval


def _validate_observation_shapes(
    observations: list[dict[str, Any]],
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    required_fields = {
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    }
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != required_fields:
            raise P5ETimingModelError("observation fields mismatch")
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]
        outcome = observation["outcome"]
        observed_head = observation["observed_head"]
        if not _is_nonnegative_int(scheduled):
            raise P5ETimingModelError("scheduled time must be nonnegative")
        if not _is_nonnegative_int(completed):
            raise P5ETimingModelError("completion time must be nonnegative")
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        if outcome == "READ_FAILURE":
            if observed_head is not None:
                raise P5ETimingModelError(
                    "read failure may not carry a head identity"
                )
        elif not _valid_head(observed_head):
            raise P5ETimingModelError(
                "successful remote observation requires exact head identity"
            )


def classify_tip_visibility(
    *,
    target_head: str,
    observed_head: str,
    fast_forward_contains_target: bool,
) -> str:
    if not _valid_head(target_head) or not _valid_head(observed_head):
        raise P5ETimingModelError("tip identity must be a lowercase 40-hex SHA")
    if not isinstance(fast_forward_contains_target, bool):
        raise P5ETimingModelError("containment fact must be boolean")
    if observed_head == target_head:
        return "EXACT_TIP_OBSERVED"
    if fast_forward_contains_target:
        return "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED"
    return "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION"


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_release_at_seconds: int,
    target_head: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_release_at_seconds):
        raise P5ETimingModelError(
            "controlled source release time must be a nonnegative integer"
        )
    if not _valid_head(target_head):
        raise P5ETimingModelError(
            "target head must be a lowercase 40-hex SHA"
        )
    _validate_observation_shapes(observations)

    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    origin = plan["schedule_origin_seconds"]

    previous_scheduled: int | None = None
    previous_completed: int | None = None
    for observation in observations:
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if completed < scheduled:
            return _blocked("READ_COMPLETION_PRECEDES_ATTEMPT_START")
        if previous_scheduled is not None:
            if scheduled == previous_scheduled:
                return _blocked("DUPLICATE_FIXED_RATE_SLOT")
            if scheduled - previous_scheduled != interval:
                return _blocked("CADENCE_GAP")
            if previous_completed is not None and previous_completed > scheduled:
                return _blocked("ATTEMPT_OVERLAP")
        previous_scheduled = scheduled
        previous_completed = completed

        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
            and scheduled < source_release_at_seconds
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE"
            )

    last_observation = observations[-1]
    if (
        last_observation["completed_at_seconds"]
        > last_observation["scheduled_at_seconds"] + interval
    ):
        return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    first_required_slot = _first_fixed_rate_slot_at_or_after(
        instant_seconds=source_release_at_seconds,
        interval=interval,
        origin=origin,
    )
    scheduled_slots = {
        observation["scheduled_at_seconds"] for observation in observations
    }
    if (
        any(slot >= first_required_slot for slot in scheduled_slots)
        and first_required_slot not in scheduled_slots
    ):
        return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    first_detection: dict[str, Any] | None = None
    for observation in observations:
        if observation["scheduled_at_seconds"] < source_release_at_seconds:
            continue
        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
        ):
            first_detection = observation
            break

    if first_detection is not None:
        completed = first_detection["completed_at_seconds"]
        latency = completed - source_release_at_seconds
        if latency <= bound:
            status = "PASS_DETECTED_WITHIN_BOUND"
            failure_code = None
        else:
            status = "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            failure_code = "DETECTION_COMPLETION_EXCEEDED_BOUND"
        return _result(
            status=status,
            failure_code=failure_code,
            detection_latency_seconds=latency,
            first_detection_scheduled_at_seconds=(
                first_detection["scheduled_at_seconds"]
            ),
            first_detection_completed_at_seconds=completed,
            observed_head=first_detection["observed_head"],
        )

    last_scheduled = observations[-1]["scheduled_at_seconds"]
    next_required_slot = last_scheduled + interval
    if next_required_slot - source_release_at_seconds > bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            failure_code="NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            detection_latency_seconds=None,
            first_detection_scheduled_at_seconds=None,
            first_detection_completed_at_seconds=None,
            observed_head=None,
        )

    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        failure_code=None,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )

~~~~

# SOURCE: CURRENT EVIDENCE MATRIX
Path: tools/obsidian_projection/p5e_v0_1_requirement_evidence_matrix.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
  "qualification_scope": "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
  "binding": "GIT_HASH_OBJECT_WITH_PATH_FILTERS",
  "real_p5e_execution_authorized": false,
  "real_60_second_sla_qualified": false,
  "per_transient_tip_detection_sla_qualified": false,
  "automatic_evaluation_authorized": false,
  "automatic_promotion_authorized": false,
  "automatic_publication_authorized": false,
  "required_synthetic_cases": {
    "SAME_HEAD_NOOP": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_change_just_after_poll_is_detected_at_next_slot_completion",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_one_transient_failure_can_pass_only_by_completion_within_60",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DETECTION_AFTER_60_SECONDS_REJECTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_read_completion_after_60_is_rejected",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NO_DETECTION_BY_60_SECONDS_REJECTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NON_FAST_FORWARD_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_non_fast_forward_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "UNKNOWN_ANCESTRY_BLOCKED": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_unknown_ancestry_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "SAME_HEAD_DOES_NOT_GROW_QUEUE": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    }
  },
  "base_breakers": {
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DETECTION_BOUND_ABOVE_60_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_timing_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_previously_surviving_contract_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SLEEP_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NETWORK_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_synthetic_model_imports_are_ast_allowlisted",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_read_completion_after_60_is_rejected",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py",
      "test_method": "TestP5EContractV01.test_no_detection_fails_when_next_fixed_rate_slot_cannot_meet_bound",
      "blob": "a4fbd35987b4abb4fe185f8ceee3f75bd749e23d",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "SAME_HEAD_GROWS_QUEUE": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_same_head_is_strict_noop_for_queue",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "NON_FAST_FORWARD_AUTO_CONTINUES": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_non_fast_forward_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_unknown_ancestry_blocks_without_queueing",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_SILENTLY_DROPS_HEAD": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT": {
      "path": "tests/obsidian_projection/test_p5d4_bounded_observer_loop_runtime_v0_1.py",
      "test_method": "P5D4RuntimeV01Tests.test_07_queue_capacity_blocks_before_tick",
      "blob": "5bcc563487ca8c64a1afde9f022504b2b618af7b",
      "evidence_kind": "REUSED_QUALIFIED_P5D2_P5D4",
      "verdict": "PASS"
    },
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD": {
      "path": "tests/obsidian_projection/test_observer_tick.py",
      "test_method": "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation",
      "blob": "f5b4bca7524f74f221927d1ec389e23d607d1eee",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "EVALUATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PROMOTION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PUBLICATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "P6_AUTHORITY_BECOMES_TRUE": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_authority_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS": {
      "path": "tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py",
      "test_method": "TestP5EAdversarialV01.test_claim_and_tip_mutations_are_rejected",
      "blob": "de4133706661c5d92cb2d7b93cf1f2573e1a916b",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    }
  },
  "targeted_closure_breakers": {
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b2_skipped_first_required_slot_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "CADENCE_GAP_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b2_cadence_gap_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b3_pre_source_target_observation_blocks",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b4_contract_uses_falsifiable_local_monotonic_measurement",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "READ_COMPLETION_LATENCY_HIDDEN": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b4_read_completion_not_poll_start_controls_latency",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b5_observation_requires_head_identity",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED": {
      "path": "tests/obsidian_projection/test_p5e_external_review_targeted_closure_v0_1.py",
      "test_method": "TestP5EExternalReviewTargetedClosureV01.test_b5_exact_and_contained_tip_classifications_are_distinct",
      "blob": "15c3e44ab9c1c40873110d88ff42cebb13a2643e",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    },
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED": {
      "path": "tests/obsidian_projection/test_p5e_requirement_evidence_matrix_v0_1.py",
      "test_method": "TestP5ERequirementEvidenceMatrixV01.test_matrix_has_no_unmapped_or_deferred_requirements",
      "blob": "182a7b60b440ddb8d5c0c9fdc65f423309383244",
      "evidence_kind": "DIRECT_P5E",
      "verdict": "PASS"
    }
  },
  "coverage_summary": {
    "required_synthetic_cases_total": 10,
    "base_breakers_total": 25,
    "targeted_closure_breakers_total": 8,
    "mapped_total": 43,
    "unmapped": 0,
    "deferred": 0
  },
  "covered_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
  "covered_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
  "covered_object_drift_must_fail": true
}

~~~~

# SOURCE: CURRENT P5-E ADVERSARIAL TESTS
Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
~~~~
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
    assert contract["source_repository"] == "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"

    source = contract["monitored_source"]
    assert source["remote"] == "origin"
    assert source["branch"] == "integration/system-v1"
    assert source["canonical_authority"] == "GITHUB_REMOTE_BRANCH"
    assert source["local_working_tree_is_not_authority"] is True

    objective = contract["objective"]
    assert objective["this_stage_is_not_real_end_to_end_execution"] is True
    assert objective["this_stage_may_not_claim_continuous_synchronization"] is True

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True
    assert timing["delivery_semantics"] == "NEAR_REAL_TIME_BOUNDED_LATENCY"
    assert timing["detection_latency_definition"] == (
        "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    )
    assert timing["future_real_bound_clock"] == "MONOTONIC_ELAPSED_TIME"
    assert timing["future_real_wall_clock_may_be_recorded_as_evidence_only"] is True
    assert timing["latency_bound_breach_must_not_be_reported_as_near_real_time_pass"] is True
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
    assert synthetic["required"] is True
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
    assert synthetic["observation_record_fields"] == [
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    ]
    assert synthetic["head_identity_required_on_successful_remote_observation"] is True
    assert synthetic["explicit_non_pass_statuses"] == ["INCOMPLETE_SYNTHETIC_WINDOW"]
    assert synthetic["attempt_overruns_next_required_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["attempt_overruns_next_required_slot_failure_code"] == "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
    assert synthetic["duplicate_fixed_rate_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["duplicate_fixed_rate_slot_failure_code"] == "DUPLICATE_FIXED_RATE_SLOT"
    assert synthetic["read_completion_before_attempt_start_forbidden"] is True
    assert synthetic["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    transition = contract["head_transition_policy"]
    assert transition["same_head_result"] == "NOOP"
    assert transition["same_head_queue_growth_forbidden"] is True
    assert transition["initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
    assert transition["fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
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
    assert queue["burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification"] is True
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

    real_context = contract["real_context_evidence_only"]
    assert real_context["must_not_be_used_as_real_experiment_execution"] is True
    assert real_context["must_not_be_mutated_by_contract_qualification"] is True

    tips = contract["tip_visibility_semantics"]
    assert tips["observed_remote_tip_definition"] == "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ"
    assert tips["unobserved_intermediate_tip_may_be_claimed_observed"] is False
    assert tips["unobserved_intermediate_tip_may_be_queued"] is False
    assert tips["fast_forward_content_containment_is_queue_coalescing"] is False
    assert tips["already_observed_queued_head_replacement_forbidden"] is True
    assert tips["already_observed_queued_head_retarget_forbidden"] is True
    assert tips["per_transient_tip_detection_sla_authorized"] is False
    assert tips["future_ancestry_enumeration_requires_separate_qualification"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_future_adapter_rule"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property"] is False

    end_to_end = contract["end_to_end_definition"]
    assert end_to_end["real_end_to_end_stages"] == [
        "SOURCE_HEAD_BECOMES_OBSERVABLE",
        "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
        "HEAD_TRANSITION_CLASSIFIED",
        "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
        "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
        "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
        "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
        "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED",
    ]
    assert end_to_end["current_stage_may_qualify_only"] == [
        "TIMING_CONTRACT",
        "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
        "AUTHORITY_BOUNDARIES",
        "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR",
    ]
    assert end_to_end["real_end_to_end_pass_requires_all_authorized_applicable_stages"] is True
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
    assert closure["external_rereview_required_before_human_normative_adoption"] is True


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
        forbidden_calls = {
            "open", "eval", "exec", "__import__", "compile", "input"
        }
        forbidden_attributes = {
            "sleep", "wait", "system", "popen", "Popen", "run",
            "connect", "request", "urlopen", "FileIO", "environ"
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_calls)
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attributes)
            elif isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, forbidden_attributes)

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
                "DUPLICATE_FIXED_RATE_SLOT",
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

~~~~

# SOURCE: CURRENT BB1 CLOSURE TESTS
Path: tests/obsidian_projection/test_p5e_bb1_normative_guard_closure_v0_1.py
~~~~
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
                "DIRECT_P5E",
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

~~~~

# SOURCE: FINAL HYGIENE TESTS
Path: tests/obsidian_projection/test_p5e_final_pre_adoption_evidence_hygiene_v0_1.py
~~~~
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"
ADV = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"

TARGET = "a" * 40
D2_METHOD = "ObserverTickTests.test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
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


class TestP5EFinalPreAdoptionEvidenceHygieneV01(unittest.TestCase):
    def test_n1_contract_explicitly_forbids_completion_before_attempt_start(self):
        contract = load_json(CONTRACT)
        synthetic = contract["synthetic_timing_model"]
        self.assertTrue(
            synthetic["read_completion_before_attempt_start_forbidden"]
        )

    def test_n1_behavior_blocks_completion_before_attempt_start(self):
        model = load_module(MODEL, "p5e_final_hygiene_n1_model")
        result = model.qualify_detection(
            plan=model.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(60, 40, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "READ_COMPLETION_PRECEDES_ATTEMPT_START",
        )

    def test_n1_contract_field_is_strictly_guarded(self):
        contract = load_json(CONTRACT)
        candidate = copy.deepcopy(contract)
        candidate["synthetic_timing_model"][
            "read_completion_before_attempt_start_forbidden"
        ] = False
        adv = load_module(ADV, "p5e_final_hygiene_n1_adv")
        with self.assertRaises(AssertionError):
            adv.assert_contract_invariants(candidate)

    def test_n2_new_d2_file_test_is_labelled_direct_p5e(self):
        matrix = load_json(MATRIX)
        entries = [
            matrix["required_synthetic_cases"][
                "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
            ],
            matrix["base_breakers"][
                "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD"
            ],
        ]
        for entry in entries:
            self.assertEqual(entry["test_method"], D2_METHOD)
            self.assertEqual(entry["evidence_kind"], "DIRECT_P5E")

    def test_n6_stale_built_against_head_is_absent(self):
        matrix = load_json(MATRIX)
        self.assertNotIn("built_against_head", matrix)

    def test_n6_object_blobs_remain_the_binding_authority(self):
        matrix = load_json(MATRIX)
        self.assertTrue(matrix["covered_object_drift_must_fail"])
        self.assertRegex(matrix["covered_contract_blob"], r"^[0-9a-f]{40}$")
        self.assertRegex(matrix["covered_model_blob"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: EVIDENCE MATRIX TESTS
Path: tests/obsidian_projection/test_p5e_requirement_evidence_matrix_v0_1.py
~~~~
import subprocess
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"
MATRIX = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_requirement_evidence_matrix.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path, relative_path):
    return subprocess.check_output(
        [
            "git",
            "hash-object",
            f"--path={relative_path}",
            str(path),
        ],
        cwd=ROOT,
        text=True,
    ).strip()


class TestP5ERequirementEvidenceMatrixV01(unittest.TestCase):
    def test_matrix_exists_and_schema_is_exact(self):
        self.assertTrue(MATRIX.is_file())
        m = load_json(MATRIX)
        self.assertEqual(
            m["schema"],
            "ATDS_OBSIDIAN_P5E_REQUIREMENT_EVIDENCE_MATRIX_V0_1",
        )
        self.assertEqual(
            m["qualification_scope"],
            "P5E_V0_1_EXTERNAL_REVIEW_TARGETED_CLOSURE",
        )
        self.assertFalse(m["real_p5e_execution_authorized"])

    def test_matrix_binds_exact_covered_contract_and_model(self):
        m = load_json(MATRIX)
        self.assertTrue(m["covered_object_drift_must_fail"])
        self.assertEqual(
            m["covered_contract_blob"],
            git_blob_sha1(
                CONTRACT,
                "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
            ),
        )
        self.assertEqual(
            m["covered_model_blob"],
            git_blob_sha1(
                MODEL,
                "tools/obsidian_projection/p5e_near_real_time_model.py",
            ),
        )

    def test_every_required_case_and_breaker_is_mapped_exactly_once(self):
        c = load_json(CONTRACT)
        m = load_json(MATRIX)
        self.assertEqual(
            set(m["required_synthetic_cases"]),
            set(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            set(m["base_breakers"]),
            set(c["required_breakers"]),
        )
        self.assertEqual(
            set(m["targeted_closure_breakers"]),
            set(c["external_review_targeted_closure"]["required_breakers"]),
        )
        self.assertEqual(
            len(m["required_synthetic_cases"]),
            len(c["required_synthetic_cases"]),
        )
        self.assertEqual(
            len(m["base_breakers"]),
            len(c["required_breakers"]),
        )
        self.assertEqual(
            len(m["targeted_closure_breakers"]),
            len(c["external_review_targeted_closure"]["required_breakers"]),
        )

    def test_all_mappings_bind_to_current_file_blobs_and_real_test_methods(self):
        m = load_json(MATRIX)
        sections = (
            "required_synthetic_cases",
            "base_breakers",
            "targeted_closure_breakers",
        )
        for section in sections:
            for requirement, entry in m[section].items():
                with self.subTest(section=section, requirement=requirement):
                    self.assertEqual(entry["verdict"], "PASS")
                    self.assertIn(
                        entry["evidence_kind"],
                        {"DIRECT_P5E", "REUSED_QUALIFIED_P5D2_P5D4"},
                    )
                    path = ROOT / entry["path"]
                    self.assertTrue(path.is_file(), entry["path"])
                    self.assertEqual(
                        entry["blob"],
                        git_blob_sha1(path, entry["path"]),
                    )
                    method = entry["test_method"].split(".")[-1]
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(f"def {method}", text)

    def test_matrix_has_no_unmapped_or_deferred_requirements(self):
        m = load_json(MATRIX)
        summary = m["coverage_summary"]
        self.assertEqual(summary["unmapped"], 0)
        self.assertEqual(summary["deferred"], 0)
        self.assertEqual(summary["required_synthetic_cases_total"], 10)
        self.assertEqual(summary["base_breakers_total"], 25)
        self.assertEqual(summary["targeted_closure_breakers_total"], 8)
        self.assertEqual(summary["mapped_total"], 43)

    def test_matrix_does_not_claim_real_execution(self):
        m = load_json(MATRIX)
        self.assertFalse(m["real_p5e_execution_authorized"])
        self.assertFalse(m["real_60_second_sla_qualified"])
        self.assertFalse(m["per_transient_tip_detection_sla_qualified"])
        self.assertFalse(m["automatic_evaluation_authorized"])
        self.assertFalse(m["automatic_promotion_authorized"])
        self.assertFalse(m["automatic_publication_authorized"])


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: D2 OBSERVER TICK TESTS
Path: tests/obsidian_projection/test_observer_tick.py
~~~~
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tools.obsidian_projection.observer_tick import (
    DECISION_SCHEMA,
    EVENT_SCHEMA,
    INPUT_SCHEMA,
    RESULT_SCHEMA,
    STATE_SCHEMA,
    ObserverTickError,
    canonical_result_bytes,
    make_initial_state,
    one_shot_tick,
)


H1 = "1" * 40
H2 = "2" * 40
H3 = "3" * 40
H4 = "4" * 40


def event(
    sequence: int,
    event_type: str,
    *,
    observed_head: str | None = None,
    transition_class: str | None = None,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": sequence,
        "observed_head": observed_head,
        "transition_class": transition_class,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }


def tick(
    state: dict,
    event_type: str,
    **kwargs,
) -> dict:
    payload = event(
        state["last_event_sequence"] + 1,
        event_type,
        **kwargs,
    )
    return one_shot_tick(state, payload)


def bootstrap() -> dict:
    state = make_initial_state()
    return tick(
        state,
        "BOOTSTRAP",
    )["next_state"]


def observe_initial(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "REMOTE_HEAD_OBSERVED",
        observed_head=head,
        transition_class="INITIAL",
    )["next_state"]


def begin_evaluation(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_STARTED",
        candidate_head=head,
    )["next_state"]


def qualify(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_PASSED",
        candidate_head=head,
    )["next_state"]


def promote(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "PROMOTION_CONFIRMED",
        candidate_head=head,
    )["next_state"]


def make_current_state() -> dict:
    state = bootstrap()
    state = observe_initial(state, H1)
    state = begin_evaluation(state, H1)
    state = qualify(state, H1)
    state = promote(state, H1)
    return state


class ObserverTickTests(unittest.TestCase):
    def test_initial_state_is_canonical(self) -> None:
        state = make_initial_state()
        self.assertEqual(state["schema"], STATE_SCHEMA)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(
            state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            state["projection_state"],
            "MISSING",
        )
        self.assertEqual(state["pending_heads"], [])
        self.assertEqual(state["last_event_sequence"], 0)

    def test_bootstrap_changes_only_sequence(self) -> None:
        state = make_initial_state()
        result = tick(state, "BOOTSTRAP")
        next_state = result["next_state"]
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] = 1
        self.assertEqual(next_state, expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )
        self.assertEqual(
            result["decision"]["reason_code"],
            "BOOTSTRAP_ACCEPTED",
        )

    def test_bootstrap_rejects_noncanonical_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["remote_freshness"] = "KNOWN"
        with self.assertRaises(ObserverTickError):
            tick(state, "BOOTSTRAP")

    def test_initial_head_is_queued_exactly_once(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["latest_observed_head"],
            H1,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1],
        )
        self.assertEqual(
            next_state["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "MISSING",
        )
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )

    def test_initial_rejected_after_previous_observation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="INITIAL",
            )

    def test_same_head_is_strict_noop_for_queue(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        before_pending = copy.deepcopy(
            state["pending_heads"]
        )
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            before_pending,
        )
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_same_requires_previous_observed_equality(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_network_failure_from_current_becomes_stale(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            "NETWORK_UNAVAILABLE",
        )

    def test_same_head_restores_current_after_network_failure(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "CURRENT",
        )

    def test_same_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_new_remote_head_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        blocked_before = state["blocked_head"]
        failure_before = state["last_failure_code"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H3,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["blocked_head"],
            blocked_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            failure_before,
        )
        self.assertEqual(
            next_state["latest_observed_head"],
            H3,
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )

    def test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(state["pending_heads"], [H1])
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(next_state["observer_phase"], "IDLE")
        self.assertEqual(next_state["pending_heads"], [H1, H2])
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )
        self.assertEqual(result["decision"]["candidate_head"], H2)

    def test_fast_forward_queues_without_retargeting_active(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1, H2],
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )

    def test_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="NON_FAST_FORWARD",
            )

    def test_unknown_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="UNKNOWN",
            )

    def test_fast_forward_requires_previous_observed_head(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["blocked_head"],
            H2,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertNotIn(H2, next_state["pending_heads"])

    def test_unknown_ancestry_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="UNKNOWN",
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )
        self.assertNotIn(
            H2,
            result["next_state"]["pending_heads"],
        )

    def test_evaluation_start_binds_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        result = tick(
            state,
            "EVALUATION_STARTED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H1],
        )
        self.assertEqual(
            result["decision"]["candidate_head"],
            H1,
        )

    def test_evaluation_start_rejects_non_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H2,
            )

    def test_evaluation_start_requires_idle(self) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H1,
            )

    def test_evaluation_pass_advances_qualified_not_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["last_qualified_head"],
            H1,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [],
        )
        self.assertEqual(
            next_state["observer_phase"],
            "CANDIDATE_PENDING",
        )

    def test_evaluation_pass_preserves_newer_queued_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )
        self.assertEqual(
            result["next_state"]["last_qualified_head"],
            H1,
        )

    def test_evaluation_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_FAILED",
            candidate_head=H2,
            failure_code="CANDIDATE_INVALID",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["blocked_head"],
            H2,
        )

    def test_promotion_confirmation_is_logical_only(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["live_projection_head"],
            H1,
        )
        self.assertEqual(
            next_state["projection_state"],
            "CURRENT",
        )
        self.assertEqual(
            result["decision"][
                "production_write_authorized"
            ],
            False,
        )
        self.assertEqual(
            result["decision"][
                "automatic_promotion_authorized"
            ],
            False,
        )

    def test_promotion_confirmation_stays_stale_if_newer_remote(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            H1,
        )
        self.assertEqual(
            result["next_state"]["latest_observed_head"],
            H2,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "STALE",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )

    def test_promotion_rejects_nonqualified_candidate(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "PROMOTION_CONFIRMED",
                candidate_head=H2,
            )

    def test_promotion_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        state = qualify(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "PROMOTION_FAILED",
            candidate_head=H2,
            failure_code="POINTER_NOT_CONFIRMED",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_lock_contended_changes_only_sequence(
        self,
    ) -> None:
        state = make_current_state()
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] += 1
        result = tick(
            state,
            "LOCK_CONTENDED",
            failure_code="LOCK_CONTENDED",
        )
        self.assertEqual(result["next_state"], expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_shutdown_preserves_pending_and_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "STOPPED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )

    def test_stopped_state_accepts_no_further_event(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )["next_state"]
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_input_sequence_skip_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 2,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_input_sequence_replay_is_rejected(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"],
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_boolean_sequence_is_rejected(self) -> None:
        state = make_initial_state()
        payload = event(
            True,
            "BOOTSTRAP",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_extra_input_field_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["unexpected"] = "x"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_wrong_input_schema_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["schema"] = "WRONG"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_remote_observed_requires_head(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                transition_class="INITIAL",
            )

    def test_remote_observed_requires_transition_class(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
            )

    def test_invalid_repository_is_rejected(self) -> None:
        state = make_initial_state()
        state["repository"] = "wrong/repo"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_invalid_branch_is_rejected(self) -> None:
        state = make_initial_state()
        state["branch"] = "main"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_uppercase_head_is_rejected(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head="A" * 40,
                transition_class="INITIAL",
            )

    def test_duplicate_pending_heads_are_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["pending_heads"] = [H1, H1]
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_current_unknown_freshness_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["remote_freshness"] = "UNKNOWN"
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_current_head_mismatch_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["latest_observed_head"] = H2
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_evaluating_empty_queue_is_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "EVALUATING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_candidate_pending_requires_qualified_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "CANDIDATE_PENDING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_consistent_block_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "STALE"
        state["blocked_head"] = H1
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_blocked_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "BLOCKED"
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_caller_inputs_are_not_mutated(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        state_before = copy.deepcopy(state)
        payload_before = copy.deepcopy(payload)
        one_shot_tick(state, payload)
        self.assertEqual(state, state_before)
        self.assertEqual(payload, payload_before)

    def test_result_schemas_and_authority_flags(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        self.assertEqual(result["schema"], RESULT_SCHEMA)
        self.assertEqual(
            result["next_state"]["schema"],
            STATE_SCHEMA,
        )
        self.assertEqual(
            result["decision"]["schema"],
            DECISION_SCHEMA,
        )
        self.assertEqual(
            result["audit"]["schema"],
            EVENT_SCHEMA,
        )
        self.assertFalse(
            result["decision"][
                "automatic_promotion_authorized"
            ]
        )
        self.assertFalse(
            result["decision"][
                "production_write_authorized"
            ]
        )

    def test_same_inputs_are_byte_deterministic(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        first = one_shot_tick(state, payload)
        second = one_shot_tick(state, payload)
        self.assertEqual(first, second)
        self.assertEqual(
            canonical_result_bytes(first),
            canonical_result_bytes(second),
        )

    def test_canonical_result_is_compact_sorted_lf(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        raw = canonical_result_bytes(result)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertNotIn(b": ", raw)
        self.assertNotIn(b", ", raw)
        decoded = json.loads(raw.decode("utf-8"))
        self.assertEqual(decoded, result)

    def test_audit_digests_match_canonical_values(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        result = one_shot_tick(state, payload)

        def digest(value: dict) -> str:
            raw = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
            return hashlib.sha256(raw).hexdigest()

        audit = result["audit"]
        self.assertEqual(
            audit["previous_state_digest"],
            digest(state),
        )
        self.assertEqual(
            audit["input_digest"],
            digest(payload),
        )
        self.assertEqual(
            audit["decision_digest"],
            digest(result["decision"]),
        )
        self.assertEqual(
            audit["next_state_digest"],
            digest(result["next_state"]),
        )

    def test_audit_has_no_volatile_host_fields(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        audit = result["audit"]
        for forbidden in (
            "observed_at",
            "timestamp",
            "host_id",
            "process_id",
            "pid",
            "path",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, audit)


if __name__ == "__main__":
    unittest.main()

~~~~
