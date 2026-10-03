# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — EXTERNAL REVIEW PACKET

Date: 2026-10-03

## Reviewer mandate

Independently review RPE-02 only.

Candidate status:
RPE-02 = QUALIFIED_FOR_EXTERNAL_REVIEW

This review creates no authority.

RPE-03 is a separate branch and is outside this packet.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

## Lineage

RPE-01 human-adoption base:
8ed3ec4079f3f996a5159b78fc40d0f32a917b25

RPE-01 adoption blob:
49203ebc2fb208c5dd23ded140295ac00c0afab6

RPE-02 preregistration HEAD:
c42a0f3df48807b3681db782f0a6fd58bd5c7aea

RPE-02 RED HEAD:
03394a8a85680ca24a2593d14466c192fd208e8e

RPE-02 implementation HEAD:
c17d68b04de9dca13f9d9ed655e034b13436484d

RPE-02 qualification HEAD:
a01ac84d8610a6644192bcb3d88c7b16f0d981dd

## Candidate identities

Preregistration:
614d3724c5c36bbdb6afbf9b49a31f88da465719

Preregistration schema:
923671b1539585b5c32c8e2d284598b521fc0bba

RED test:
089a72c736302abd08ea1267c149e2ef771240db

RED report:
0c5f30c7cce63e5d149111bae4d5b3309367f4af

Implementation:
db5dcfe8ad3b7ce93099368b459bb09ac25f933b

Final main test:
23618a9317c554099670e84482641a8014f8682d

Mutation test:
77cdadb376320c4e8f591a3a80105feac250b716

Qualification JSON:
81d225d932a985d65a627d727b0b164950a32865

Qualification report:
e2550e5629f5a505718e867b805be232f5fe345b

Protected parent identities:
RPE-01 guard = 26f977961d72a062199d71ffd628d5a5cc047887
P5-E contract = 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9
P5-E synthetic model = c0f16baa151c1466e30ba5778f1fca8184cd4aac
P5-D4 runtime = 1825e53d195ba2a63b5b646a5b78eb77939b94b5

## Reproduced local evidence

Dedicated RPE-02 surface:
22 / 22 PASS

P5-E + RPE-01 + RPE-02 targeted regression:
135 / 135 PASS

Targeted mutants:
4 / 4 KILLED

Protected diffs from RPE-01 adoption base:
P5-E contract = 0
P5-E synthetic model = 0
P5-D4 runtime = 0

Host clock evidence:
- time.monotonic_ns
- monotonic = true
- adjustable = false
- resolution = 1e-7 seconds
- implementation = QueryPerformanceCounter()
- integer non-decreasing samples
- CPython 3.13.14 / Windows 11

## Required review questions

### Representation and boundary semantics
1. Is every normative real-time verdict nanosecond-native with strict Python int values excluding bool/float coercion?
2. Are all six required timestamps represented?
3. Is actual attempt start distinct from scheduled slot and used for release eligibility?
4. Is the 30-second fixed-rate grid exact?
5. Is release exactly on a slot mapped to that slot and release just after a slot mapped to the next slot?
6. Is actual start equal to the next slot correctly blocked as a missed fixed-rate slot?
7. Is remote completion equal to the next slot allowed and +1 ns blocked?
8. Is previous full completion equal to next start allowed and greater-than blocked as overlap?
9. Is pre-release-started target observation blocked rather than credited?
10. Is detection latency measured from controlled release to remote-observation completion, not full-attempt completion?
11. Does exactly 60 s pass and 60 s + 1 ns fail?
12. Is no-detection-by-bound distinguished from an incomplete window?

### Synthetic reference and provenance
13. Is the adopted synthetic model unchanged and used only as semantic/exact-grid parity reference?
14. Does the exact-grid parity test compare a legitimate common domain without making seconds conversion normative?
15. Do implementation constants match the governed RPE-02 preregistration?
16. Is any normative timing authority silently obtained from environment variables, CLI, or an unlisted file?
17. Does any float-second quantity feed a real verdict?

### Clock capability
18. Is time.monotonic_ns appropriate for the intended same-host/same-process comparison domain?
19. Is the recorded clock evidence sufficient for RPE-02, while suspend semantics remain a later real-experiment concern?
20. Is any cross-host or wall-clock interpretation accidentally implied?

### Mutation/regression
21. Do the four mutation checks discriminate the exact boundary and endpoint rules they claim?
22. Is the 135/135 targeted regression sufficient for this isolated component?
23. Is a full Obsidian suite unnecessary given zero protected-runtime diff and no real runtime activation?

### Authority
24. Did RPE-02 open any network, RPE-04/05/06, P5-D4 real-state, Vault/CURRENT or REAL P5-E authority?
25. Is RPE-02 ready for human adoption if no blocker is found?

## Required adversarial probes

At minimum attempt:
- bool/float/string timestamps;
- release <= origin;
- off-grid/duplicate/gapped slots;
- actual start before slot;
- actual start exactly next slot;
- remote completion before actual start;
- remote completion exactly next slot and +1 ns;
- full completion before remote completion;
- overlap equality and +1 ns;
- target observed from pre-release-started attempt;
- 60-second exact latency and +1 ns;
- mutate scheduled-vs-actual eligibility;
- mutate remote-completion latency endpoint to full completion;
- mutate exact comparison operators;
- attempt environment/CLI authority;
- compare exact-grid behavior to adopted synthetic model.

## Required output

Return exactly one:

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then provide:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- REPRESENTATION_CHECK
- BOUNDARY_SEMANTICS_CHECK
- CLOCK_CAPABILITY_CHECK
- SYNTHETIC_PARITY_CHECK
- CONFIG_PROVENANCE_CHECK
- MUTATION_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RPE02_ADOPTION_READINESS
- RECOMMENDED_NEXT_ACTION

Distinguish OBSERVED from INFERENCE. Give minimal falsification cases for findings where possible.

This review creates no authority.
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED

---

# NORMALIZED DISPLAY OF EXACT GIT DIFF — RPE-01 ADOPTION TO RPE-02 QUALIFICATION
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-PREDRAFT.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-PREDRAFT.md
new file mode 100644
index 0000000..a5d559e
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-PREDRAFT.md
@@ -0,0 +1,11 @@
+﻿# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — PRE-DRAFT
+
+Base: RPE-01 adoption commit 8ed3ec4079f3f996a5159b78fc40d0f32a917b25.
+
+Architecture selected before RED: SEPARATE_REAL_TIME_MODEL_V0_2.
+
+The real verdict component is integer-nanosecond-native. The adopted synthetic model is immutable and remains only a semantic and exact-grid parity reference. No float-second or lossy integer-second conversion may decide a real pass/fail.
+
+The preregistration freezes the six required time fields, exact 30-second interval and 60-second bound in nanoseconds, actual-start eligibility, remote-completion latency endpoint, full-attempt-completion separation, equality boundaries, overlap semantics, first-required-slot ceiling semantics, exact-grid parity, and host monotonic-clock capability evidence.
+
+No network, RPE-04/05/06, REAL P5-E, P5-D4 real-state mutation, Vault or CURRENT mutation is authorized.
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-QUALIFICATION.md
new file mode 100644
index 0000000..e2550e5
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-QUALIFICATION.md
@@ -0,0 +1,155 @@
+# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — QUALIFICATION
+
+Date: 2026-10-03
+
+## Verdict
+
+`RPE-02 = QUALIFIED_FOR_EXTERNAL_REVIEW`
+
+Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.
+
+## Canonical base
+
+RPE-01 adoption commit:
+`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`
+
+RPE-01 adoption blob:
+`49203ebc2fb208c5dd23ded140295ac00c0afab6`
+
+The adopted P5-E contract, synthetic timing model and P5-D4 runtime remain byte-identical to the RPE-01 base.
+
+## Preregistration and RED
+
+Preregistration HEAD:
+`c42a0f3df48807b3681db782f0a6fd58bd5c7aea`
+
+Preregistration blob:
+`614d3724c5c36bbdb6afbf9b49a31f88da465719`
+
+Closed-schema blob:
+`923671b1539585b5c32c8e2d284598b521fc0bba`
+
+The preregistration validates through the adopted RPE-01 public entrypoint.
+
+RED HEAD:
+`03394a8a85680ca24a2593d14466c192fd208e8e`
+
+Observed RED:
+`17 tests / 15 failures / 2 passes`.
+
+The failures were caused by the preregistered real-time module not yet existing.
+
+## Final implementation
+
+Implementation HEAD:
+`c17d68b04de9dca13f9d9ed655e034b13436484d`
+
+Module:
+`db5dcfe8ad3b7ce93099368b459bb09ac25f933b`
+
+Main tests:
+`23618a9317c554099670e84482641a8014f8682d`
+
+Mutation tests:
+`77cdadb376320c4e8f591a3a80105feac250b716`
+
+The implementation is a separate nanosecond-native real timing component. The adopted synthetic model is unchanged and is used only as semantic/exact-grid parity reference.
+
+## Qualified timing semantics
+
+Normative representation:
+`INTEGER_MONOTONIC_NANOSECONDS`
+
+Preregistered exact constants:
+- poll interval = 30,000,000,000 ns;
+- detection bound = 60,000,000,000 ns.
+
+Required evidence fields include:
+- schedule_origin_ns;
+- scheduled_at_ns;
+- attempt_started_at_ns;
+- remote_observation_completed_at_ns;
+- attempt_completed_at_ns;
+- controlled_source_release_started_at_ns.
+
+The qualified component distinguishes scheduled slot from actual attempt start. A scheduled-on-time attempt cannot hide an actual start at or after the next fixed-rate slot.
+
+Detection eligibility uses actual attempt start. A target observation produced by an attempt started before controlled source release is blocked for adjudication.
+
+Detection latency is:
+`remote_observation_completed_at_ns - controlled_source_release_started_at_ns`.
+
+Full attempt completion is retained for timeline/overlap validity but does not replace the remote-observation completion endpoint.
+
+Equality boundaries are frozen:
+- exactly 60 seconds = PASS;
+- 60 seconds + 1 ns = FAIL;
+- remote completion exactly at the next slot = allowed;
+- remote completion after the next slot = blocked;
+- previous attempt completion exactly at next attempt start = allowed;
+- previous completion greater than next start = overlap blocked.
+
+## Governed configuration provenance
+
+RPE-02's preregistration and schema are governed RPE-01 artifacts.
+
+A dedicated parity test proves the implementation constants equal the governed preregistration values.
+
+No environment variable, CLI argument or unlisted file supplies normative timing authority.
+
+## Mutation/discrimination
+
+Four targeted mutants were killed:
+
+1. exact latency bound `<=` changed to `<`;
+2. actual-start next-slot `>=` changed to `>`;
+3. remote-completion next-slot `>` changed to `>=`;
+4. latency endpoint changed from remote completion to full attempt completion.
+
+Result:
+`4 / 4 KILLED`.
+
+## Test result
+
+Dedicated RPE-02 surface:
+`22 / 22 PASS`
+
+P5-E + RPE-01 + RPE-02 targeted regression:
+`135 / 135 PASS`
+
+Protected diffs:
+```text
+P5-E CONTRACT = 0
+P5-E SYNTHETIC MODEL = 0
+P5-D4 RUNTIME = 0
+```
+
+## Host monotonic-clock capability evidence
+
+Observed on the qualification host:
+- API: `time.monotonic_ns`;
+- monotonic: true;
+- adjustable: false;
+- resolution: 1e-7 seconds;
+- implementation: `QueryPerformanceCounter()`;
+- samples were integer nanoseconds and non-decreasing;
+- same-process host domain: true.
+
+Environment:
+`CPython 3.13.14 / Windows-11-10.0.22631-SP0`.
+
+This host evidence is non-normative context; the verdict semantics remain integer-nanosecond based.
+
+## Authority boundary
+
+This qualification does not authorize:
+- RPE-04/05/06;
+- network observation;
+- GitHub polling;
+- P5-D4 real-state mutation;
+- Vault/CURRENT mutation;
+- REAL P5-E;
+- human adoption of RPE-02.
+
+Maximum claim:
+`RPE02_REAL_TIME_REPRESENTATION = QUALIFIED_FOR_EXTERNAL_REVIEW`.
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-RED.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-RED.md
new file mode 100644
index 0000000..0c5f30c
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-RED.md
@@ -0,0 +1,43 @@
+﻿# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — RED EVIDENCE
+
+Date: 2026-10-03
+
+## Preregistered predecessor
+
+Preregistration HEAD:
+c42a0f3df48807b3681db782f0a6fd58bd5c7aea
+
+Preregistration blob:
+614d3724c5c36bbdb6afbf9b49a31f88da465719
+
+Preregistration schema blob:
+923671b1539585b5c32c8e2d284598b521fc0bba
+
+## RED command
+
+python -B -m unittest tests.obsidian_projection.test_rpe02_real_time_representation_v0_1
+
+## Observed result
+
+Ran 17 tests.
+
+FAILED (failures=15).
+
+RPE02_RED_EXIT=1.
+
+Two tests passed:
+- governed preregistration validates through RPE-01;
+- the absent implementation source contains no environment/CLI authority by construction.
+
+The fifteen RED failures all arise because the preregistered module
+tools/obsidian_projection/rpe02_real_time_model_v0_1.py
+does not yet exist.
+
+The frozen test surface already covers integer-nanosecond representation, exact 60-second and +1 ns boundaries, actual-start semantics, next-slot completion equality, overlap equality, pre-release target handling, remote-completion versus full-completion separation, release ceiling, synthetic parity and host monotonic-clock evidence.
+
+No network or protected predecessor mutation occurred.
+
+RPE-04 = CLOSED.
+RPE-05 = CLOSED.
+RPE-06 = CLOSED.
+REAL P5-E = CLOSED.
diff --git a/tests/obsidian_projection/test_rpe02_real_time_representation_mutation_v0_1.py b/tests/obsidian_projection/test_rpe02_real_time_representation_mutation_v0_1.py
new file mode 100644
index 0000000..77cdadb
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe02_real_time_representation_mutation_v0_1.py
@@ -0,0 +1,155 @@
+import json
+import types
+import unittest
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools" / "obsidian_projection" / "rpe02_real_time_model_v0_1.py"
+A = "a" * 40
+
+
+def load_source_module(name, replacements=()):
+    source = MODULE.read_text(encoding="utf-8")
+    for old, new in replacements:
+        if source.count(old) != 1:
+            raise AssertionError(f"mutation anchor count != 1: {old!r}")
+        source = source.replace(old, new, 1)
+    module = types.ModuleType(name)
+    module.__file__ = str(MODULE)
+    exec(compile(source, str(MODULE), "exec"), module.__dict__)
+    return module
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
+class TestRPE02MutationDiscriminationV01(unittest.TestCase):
+    def test_exact_bound_operator_mutant_is_killed(self):
+        base = load_source_module("rpe02_base_bound")
+        mutant = load_source_module(
+            "rpe02_mut_bound",
+            (("if latency <= bound", "if latency < bound"),),
+        )
+        observations = [
+            obs(30_000_000_000, 30_000_000_000, 30_000_000_000, 30_000_000_000),
+            obs(
+                60_000_000_000,
+                60_000_000_000,
+                90_000_000_000,
+                90_000_000_000,
+                "REMOTE_HEAD_OBSERVED",
+                A,
+            ),
+        ]
+        kwargs = dict(
+            controlled_source_release_started_at_ns=30_000_000_000,
+            target_head=A,
+            observations=observations,
+        )
+        self.assertEqual(
+            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
+            "PASS_DETECTED_WITHIN_BOUND",
+        )
+        self.assertEqual(
+            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
+            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+        )
+
+    def test_actual_start_next_slot_operator_mutant_is_killed(self):
+        base = load_source_module("rpe02_base_start")
+        mutant = load_source_module(
+            "rpe02_mut_start",
+            (("if started >= scheduled + interval:", "if started > scheduled + interval:"),),
+        )
+        observations = [
+            obs(
+                30_000_000_000,
+                60_000_000_000,
+                60_000_000_000,
+                60_000_000_000,
+                "REMOTE_HEAD_OBSERVED",
+                A,
+            )
+        ]
+        kwargs = dict(
+            controlled_source_release_started_at_ns=30_000_000_000,
+            target_head=A,
+            observations=observations,
+        )
+        self.assertEqual(
+            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
+            "ACTUAL_START_MISSED_FIXED_RATE_SLOT",
+        )
+        self.assertNotEqual(
+            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
+            "ACTUAL_START_MISSED_FIXED_RATE_SLOT",
+        )
+
+    def test_remote_completion_next_slot_operator_mutant_is_killed(self):
+        base = load_source_module("rpe02_base_remote")
+        mutant = load_source_module(
+            "rpe02_mut_remote",
+            (("if remote_done > scheduled + interval:", "if remote_done >= scheduled + interval:"),),
+        )
+        observations = [
+            obs(30_000_000_000, 30_000_000_000, 60_000_000_000, 60_000_000_000)
+        ]
+        kwargs = dict(
+            controlled_source_release_started_at_ns=30_000_000_000,
+            target_head=A,
+            observations=observations,
+        )
+        self.assertEqual(
+            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
+            "INCOMPLETE_REAL_TIME_WINDOW",
+        )
+        self.assertEqual(
+            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["failure_code"],
+            "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
+        )
+
+    def test_latency_endpoint_mutant_is_killed(self):
+        base = load_source_module("rpe02_base_endpoint")
+        mutant = load_source_module(
+            "rpe02_mut_endpoint",
+            ((
+                'latency = item["remote_observation_completed_at_ns"] - release',
+                'latency = item["attempt_completed_at_ns"] - release',
+            ),),
+        )
+        observations = [
+            obs(
+                30_000_000_000,
+                30_000_000_000,
+                31_000_000_000,
+                100_000_000_000,
+                "REMOTE_HEAD_OBSERVED",
+                A,
+            )
+        ]
+        kwargs = dict(
+            controlled_source_release_started_at_ns=30_000_000_000,
+            target_head=A,
+            observations=observations,
+        )
+        self.assertEqual(
+            base.qualify_detection_ns(plan=base.make_real_time_plan(schedule_origin_ns=0), **kwargs)["detection_latency_ns"],
+            1_000_000_000,
+        )
+        self.assertEqual(
+            mutant.qualify_detection_ns(plan=mutant.make_real_time_plan(schedule_origin_ns=0), **kwargs)["status"],
+            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+        )
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py b/tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py
new file mode 100644
index 0000000..23618a9
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py
@@ -0,0 +1,204 @@
+﻿import importlib.util
+import inspect
+import json
+import unittest
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[2]
+MODULE = ROOT / "tools/obsidian_projection/rpe02_real_time_model_v0_1.py"
+PREREG = ROOT / "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json"
+SCHEMA = ROOT / "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json"
+GUARD = ROOT / "tools/obsidian_projection/rpe01_governed_closed_schema.py"
+SYNTH = ROOT / "tools/obsidian_projection/p5e_near_real_time_model.py"
+A = "a" * 40
+
+
+def load(path, name):
+    if not path.exists():
+        raise AssertionError(f"required module missing: {path}")
+    spec = importlib.util.spec_from_file_location(name, path)
+    if spec is None or spec.loader is None:
+        raise AssertionError(f"cannot load {path}")
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
+class TestRPE02RealTimeRepresentationV01(unittest.TestCase):
+    def test_preregistration_is_rpe01_guarded(self):
+        g = load(GUARD, "rpe01_guard_for_rpe02")
+        doc = g.validate_governed_json(
+            PREREG.read_text(encoding="utf-8"),
+            SCHEMA.read_text(encoding="utf-8"),
+        )
+        self.assertEqual(doc["architecture"]["selected"], "SEPARATE_REAL_TIME_MODEL_V0_2")
+
+    def test_implementation_constants_match_governed_preregistration(self):
+        g = load(GUARD, "rpe01_guard_for_rpe02_parity")
+        doc = g.validate_governed_json(
+            PREREG.read_text(encoding="utf-8"),
+            SCHEMA.read_text(encoding="utf-8"),
+        )
+        m = load(MODULE, "rpe02_governed_config_parity")
+        self.assertEqual(
+            m.NANOSECONDS_PER_SECOND,
+            doc["representation"]["nanoseconds_per_second"],
+        )
+        self.assertEqual(
+            m.POLL_INTERVAL_NS,
+            doc["representation"]["poll_interval_ns"],
+        )
+        self.assertEqual(
+            m.DETECTION_LATENCY_BOUND_NS,
+            doc["representation"]["detection_latency_bound_ns"],
+        )
+
+    def test_exact_nanosecond_plan(self):
+        m = load(MODULE, "rpe02")
+        plan = m.make_real_time_plan(schedule_origin_ns=0)
+        self.assertEqual(plan["poll_interval_ns"], 30_000_000_000)
+        self.assertEqual(plan["detection_latency_bound_ns"], 60_000_000_000)
+        self.assertEqual(plan["normative_unit"], "INTEGER_MONOTONIC_NANOSECONDS")
+
+    def test_strict_integer_timestamps(self):
+        m = load(MODULE, "rpe02_int")
+        for value in (0.0, True, "0", None):
+            with self.subTest(value=value):
+                with self.assertRaises(m.RPE02TimingError):
+                    m.make_real_time_plan(schedule_origin_ns=value)
+
+    def test_release_must_be_after_origin(self):
+        m = load(MODULE, "rpe02_release")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        with self.assertRaises(m.RPE02TimingError):
+            m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=0, target_head=A, observations=[obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000)])
+
+    def test_exact_60_second_latency_passes(self):
+        m = load(MODULE, "rpe02_bound")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(
+            plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
+                obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000,"REMOTE_HEAD_OBSERVED",A),
+            ])
+        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
+        self.assertEqual(r["detection_latency_ns"], 60_000_000_000)
+
+    def test_latency_one_nanosecond_over_bound_fails(self):
+        m = load(MODULE, "rpe02_over")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(
+            plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
+                obs(60_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000),
+                obs(90_000_000_000,90_000_000_000,90_000_000_001,90_000_000_001,"REMOTE_HEAD_OBSERVED",A),
+            ])
+        self.assertEqual(r["status"], "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED")
+        self.assertEqual(r["detection_latency_ns"], 60_000_000_001)
+
+    def test_late_actual_start_cannot_hide_behind_slot(self):
+        m = load(MODULE, "rpe02_late")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[obs(30_000_000_000,60_000_000_000,60_000_000_000,60_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["failure_code"], "ACTUAL_START_MISSED_FIXED_RATE_SLOT")
+
+    def test_remote_completion_equal_next_slot_allowed(self):
+        m = load(MODULE, "rpe02_equal_slot")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_000,60_000_000_000)])
+        self.assertEqual(r["status"], "INCOMPLETE_REAL_TIME_WINDOW")
+
+    def test_remote_completion_after_next_slot_blocked(self):
+        m = load(MODULE, "rpe02_after_slot")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,60_000_000_001,60_000_000_001)])
+        self.assertEqual(r["failure_code"], "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
+
+    def test_previous_completion_equal_next_start_allowed(self):
+        m = load(MODULE, "rpe02_equal_overlap")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,40_000_000_000,60_000_000_000),
+                obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
+
+    def test_previous_completion_greater_next_start_blocked(self):
+        m = load(MODULE, "rpe02_overlap")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[
+                obs(30_000_000_000,30_000_000_000,40_000_000_000,60_000_000_001),
+                obs(60_000_000_000,60_000_000_000,61_000_000_000,61_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["failure_code"], "ATTEMPT_OVERLAP")
+
+    def test_pre_release_started_target_is_blocked(self):
+        m = load(MODULE, "rpe02_pre")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=45_000_000_000, target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,45_000_000_000,45_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["failure_code"], "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT")
+
+    def test_full_completion_does_not_replace_remote_latency_endpoint(self):
+        m = load(MODULE, "rpe02_two_phase")
+        p = m.make_real_time_plan(schedule_origin_ns=0)
+        r = m.qualify_detection_ns(plan=p, controlled_source_release_started_at_ns=30_000_000_000, target_head=A,
+            observations=[obs(30_000_000_000,30_000_000_000,31_000_000_000,100_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(r["status"], "PASS_DETECTED_WITHIN_BOUND")
+        self.assertEqual(r["detection_latency_ns"], 1_000_000_000)
+        self.assertEqual(r["first_detection_attempt_completed_at_ns"], 100_000_000_000)
+
+    def test_release_ceiling_rule(self):
+        m = load(MODULE, "rpe02_ceiling")
+        self.assertEqual(m.first_fixed_rate_slot_at_or_after_ns(30_000_000_000,30_000_000_000,0),30_000_000_000)
+        self.assertEqual(m.first_fixed_rate_slot_at_or_after_ns(30_000_000_001,30_000_000_000,0),60_000_000_000)
+
+    def test_exact_grid_parity_with_synthetic_reference(self):
+        m = load(MODULE, "rpe02_parity")
+        s = load(SYNTH, "p5e_synthetic_reference")
+        sp=s.make_timing_plan()
+        sr=s.qualify_detection(plan=sp,source_release_at_seconds=30,target_head=A,observations=[
+            {"scheduled_at_seconds":30,"completed_at_seconds":30,"outcome":"READ_FAILURE","observed_head":None},
+            {"scheduled_at_seconds":60,"completed_at_seconds":90,"outcome":"REMOTE_HEAD_OBSERVED","observed_head":A}])
+        rp=m.make_real_time_plan(schedule_origin_ns=0)
+        rr=m.qualify_detection_ns(plan=rp,controlled_source_release_started_at_ns=30_000_000_000,target_head=A,observations=[
+            obs(30_000_000_000,30_000_000_000,30_000_000_000,30_000_000_000),
+            obs(60_000_000_000,60_000_000_000,90_000_000_000,90_000_000_000,"REMOTE_HEAD_OBSERVED",A)])
+        self.assertEqual(rr["status"],sr["status"])
+        self.assertEqual(rr["detection_latency_ns"],sr["detection_latency_seconds"]*1_000_000_000)
+
+    def test_clock_capability_evidence(self):
+        m = load(MODULE, "rpe02_clock")
+        e=m.capture_monotonic_clock_capability()
+        self.assertTrue(e["monotonic"])
+        self.assertIs(type(e["sample_1_ns"]),int)
+        self.assertIs(type(e["sample_2_ns"]),int)
+        self.assertGreaterEqual(e["sample_2_ns"],e["sample_1_ns"])
+        self.assertTrue(e["same_process_host_domain"])
+
+    def test_no_environment_or_cli_config_authority(self):
+        source=MODULE.read_text(encoding="utf-8") if MODULE.exists() else ""
+        self.assertNotIn("argparse",source)
+        self.assertNotIn("os.environ",source)
+        self.assertNotIn("getenv(",source)
+        self.assertNotIn("time.time(",source)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/rpe02_real_time_model_v0_1.py b/tools/obsidian_projection/rpe02_real_time_model_v0_1.py
new file mode 100644
index 0000000..db5dcfe
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_real_time_model_v0_1.py
@@ -0,0 +1,276 @@
+"""RPE-02 V0.1: nanosecond-native real-time representation.
+
+Pure timing qualification except capture_monotonic_clock_capability(), which records
+host clock capability/evidence. No network, CLI, environment, filesystem config, or
+P5-D4/Vault mutation authority exists in this module.
+"""
+
+from __future__ import annotations
+
+import platform
+import re
+import sys
+import time
+from typing import Any, Mapping, Sequence
+
+
+NANOSECONDS_PER_SECOND = 1_000_000_000
+POLL_INTERVAL_NS = 30 * NANOSECONDS_PER_SECOND
+DETECTION_LATENCY_BOUND_NS = 60 * NANOSECONDS_PER_SECOND
+_SHA40_RE = re.compile(r"[0-9a-f]{40}\Z")
+
+
+class RPE02TimingError(ValueError):
+    """Invalid RPE-02 timing evidence or plan."""
+
+
+def _strict_int(name: str, value: object) -> int:
+    if type(value) is not int:
+        raise RPE02TimingError(f"{name} must be an integer nanosecond value")
+    return value
+
+
+def _strict_sha40(name: str, value: object) -> str:
+    if type(value) is not str or _SHA40_RE.fullmatch(value) is None:
+        raise RPE02TimingError(f"{name} must be lowercase 40-hex")
+    return value
+
+
+def make_real_time_plan(*, schedule_origin_ns: int) -> dict[str, Any]:
+    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
+    return {
+        "schema": "ATDS_RPE02_REAL_TIME_PLAN_V0_1",
+        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
+        "schedule_origin_ns": origin,
+        "poll_interval_ns": POLL_INTERVAL_NS,
+        "detection_latency_bound_ns": DETECTION_LATENCY_BOUND_NS,
+        "synthetic_reference_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE",
+    }
+
+
+def first_fixed_rate_slot_at_or_after_ns(
+    timestamp_ns: int,
+    poll_interval_ns: int,
+    schedule_origin_ns: int,
+) -> int:
+    timestamp = _strict_int("timestamp_ns", timestamp_ns)
+    interval = _strict_int("poll_interval_ns", poll_interval_ns)
+    origin = _strict_int("schedule_origin_ns", schedule_origin_ns)
+    if interval <= 0:
+        raise RPE02TimingError("poll_interval_ns must be positive")
+    if timestamp <= origin:
+        return origin + interval
+    delta = timestamp - origin
+    q, r = divmod(delta, interval)
+    return origin + (q if r == 0 else q + 1) * interval
+
+
+def _blocked(code: str, **extra: Any) -> dict[str, Any]:
+    out: dict[str, Any] = {
+        "status": "BLOCKED_REQUIRES_ADJUDICATION",
+        "failure_code": code,
+        "detection_latency_ns": None,
+    }
+    out.update(extra)
+    return out
+
+
+def _validate_plan(plan: Mapping[str, Any]) -> tuple[int, int, int]:
+    if not isinstance(plan, Mapping):
+        raise RPE02TimingError("plan must be a mapping")
+    if plan.get("normative_unit") != "INTEGER_MONOTONIC_NANOSECONDS":
+        raise RPE02TimingError("plan normative unit mismatch")
+    origin = _strict_int("plan.schedule_origin_ns", plan.get("schedule_origin_ns"))
+    interval = _strict_int("plan.poll_interval_ns", plan.get("poll_interval_ns"))
+    bound = _strict_int(
+        "plan.detection_latency_bound_ns",
+        plan.get("detection_latency_bound_ns"),
+    )
+    if interval != POLL_INTERVAL_NS:
+        raise RPE02TimingError("poll interval is not the preregistered 30 seconds")
+    if bound != DETECTION_LATENCY_BOUND_NS:
+        raise RPE02TimingError("latency bound is not the preregistered 60 seconds")
+    return origin, interval, bound
+
+
+def _normalize_observation(raw: Mapping[str, Any], index: int) -> dict[str, Any]:
+    if not isinstance(raw, Mapping):
+        raise RPE02TimingError(f"observations[{index}] must be a mapping")
+    required = {
+        "scheduled_at_ns",
+        "attempt_started_at_ns",
+        "remote_observation_completed_at_ns",
+        "attempt_completed_at_ns",
+        "outcome",
+        "observed_head",
+    }
+    if set(raw) != required:
+        raise RPE02TimingError(
+            f"observations[{index}] keys mismatch: "
+            f"missing={sorted(required - set(raw))}, "
+            f"unknown={sorted(set(raw) - required)}"
+        )
+    out = dict(raw)
+    for key in (
+        "scheduled_at_ns",
+        "attempt_started_at_ns",
+        "remote_observation_completed_at_ns",
+        "attempt_completed_at_ns",
+    ):
+        out[key] = _strict_int(f"observations[{index}].{key}", out[key])
+    if type(out["outcome"]) is not str or not out["outcome"]:
+        raise RPE02TimingError(f"observations[{index}].outcome must be non-empty string")
+    if out["observed_head"] is not None:
+        out["observed_head"] = _strict_sha40(
+            f"observations[{index}].observed_head",
+            out["observed_head"],
+        )
+    return out
+
+
+def qualify_detection_ns(
+    *,
+    plan: Mapping[str, Any],
+    controlled_source_release_started_at_ns: int,
+    target_head: str,
+    observations: Sequence[Mapping[str, Any]],
+) -> dict[str, Any]:
+    origin, interval, bound = _validate_plan(plan)
+    release = _strict_int(
+        "controlled_source_release_started_at_ns",
+        controlled_source_release_started_at_ns,
+    )
+    target = _strict_sha40("target_head", target_head)
+    if release <= origin:
+        raise RPE02TimingError(
+            "controlled_source_release_started_at_ns must be greater than schedule_origin_ns"
+        )
+    if not isinstance(observations, Sequence) or isinstance(
+        observations, (str, bytes, bytearray)
+    ):
+        raise RPE02TimingError("observations must be a sequence")
+
+    normalized = [_normalize_observation(raw, i) for i, raw in enumerate(observations)]
+    normalized.sort(key=lambda item: item["scheduled_at_ns"])
+
+    previous_scheduled: int | None = None
+    previous_completion: int | None = None
+    seen_slots: set[int] = set()
+
+    for item in normalized:
+        scheduled = item["scheduled_at_ns"]
+        started = item["attempt_started_at_ns"]
+        remote_done = item["remote_observation_completed_at_ns"]
+        attempt_done = item["attempt_completed_at_ns"]
+
+        if scheduled <= origin or (scheduled - origin) % interval != 0:
+            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
+        if scheduled in seen_slots:
+            return _blocked("DUPLICATE_FIXED_RATE_SLOT")
+        seen_slots.add(scheduled)
+
+        if previous_scheduled is not None and scheduled != previous_scheduled + interval:
+            return _blocked("CADENCE_GAP")
+        if started < scheduled:
+            return _blocked("ACTUAL_START_PRECEDES_SCHEDULED_SLOT")
+        if started >= scheduled + interval:
+            return _blocked("ACTUAL_START_MISSED_FIXED_RATE_SLOT")
+        if remote_done < started:
+            return _blocked("REMOTE_COMPLETION_PRECEDES_ATTEMPT_START")
+        if remote_done > scheduled + interval:
+            return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")
+        if attempt_done < remote_done:
+            return _blocked("ATTEMPT_COMPLETION_PRECEDES_REMOTE_COMPLETION")
+        if previous_completion is not None and previous_completion > started:
+            return _blocked("ATTEMPT_OVERLAP")
+
+        if (
+            item["outcome"] == "REMOTE_HEAD_OBSERVED"
+            and item["observed_head"] == target
+            and started < release
+        ):
+            return _blocked(
+                "TARGET_HEAD_OBSERVED_BY_PRE_RELEASE_ATTEMPT",
+                first_detection_scheduled_at_ns=scheduled,
+                first_detection_attempt_started_at_ns=started,
+                first_detection_remote_observation_completed_at_ns=remote_done,
+                first_detection_attempt_completed_at_ns=attempt_done,
+            )
+
+        previous_scheduled = scheduled
+        previous_completion = attempt_done
+
+    first_required = first_fixed_rate_slot_at_or_after_ns(release, interval, origin)
+    if normalized:
+        slots_at_or_after_release = [
+            item["scheduled_at_ns"]
+            for item in normalized
+            if item["scheduled_at_ns"] >= first_required
+        ]
+        if slots_at_or_after_release and slots_at_or_after_release[0] != first_required:
+            return _blocked("SKIPPED_REQUIRED_ATTEMPT")
+
+    for item in normalized:
+        if item["attempt_started_at_ns"] < release:
+            continue
+        if (
+            item["outcome"] == "REMOTE_HEAD_OBSERVED"
+            and item["observed_head"] == target
+        ):
+            latency = item["remote_observation_completed_at_ns"] - release
+            status = (
+                "PASS_DETECTED_WITHIN_BOUND"
+                if latency <= bound
+                else "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
+            )
+            return {
+                "status": status,
+                "failure_code": None,
+                "detection_latency_ns": latency,
+                "first_detection_scheduled_at_ns": item["scheduled_at_ns"],
+                "first_detection_attempt_started_at_ns": item["attempt_started_at_ns"],
+                "first_detection_remote_observation_completed_at_ns": item[
+                    "remote_observation_completed_at_ns"
+                ],
+                "first_detection_attempt_completed_at_ns": item["attempt_completed_at_ns"],
+            }
+
+    window_end = max(
+        (item["remote_observation_completed_at_ns"] for item in normalized),
+        default=origin,
+    )
+    if window_end >= release + bound:
+        return {
+            "status": "FAIL_NO_DETECTION_BY_BOUND",
+            "failure_code": None,
+            "detection_latency_ns": None,
+        }
+    return {
+        "status": "INCOMPLETE_REAL_TIME_WINDOW",
+        "failure_code": None,
+        "detection_latency_ns": None,
+    }
+
+
+def capture_monotonic_clock_capability() -> dict[str, Any]:
+    info = time.get_clock_info("monotonic")
+    sample_1 = time.monotonic_ns()
+    sample_2 = time.monotonic_ns()
+    if not info.monotonic:
+        raise RPE02TimingError("host monotonic clock does not report monotonic capability")
+    return {
+        "schema": "ATDS_RPE02_MONOTONIC_CLOCK_CAPABILITY_V0_1",
+        "api": "time.monotonic_ns",
+        "metadata_api": "time.get_clock_info('monotonic')",
+        "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
+        "monotonic": bool(info.monotonic),
+        "adjustable": bool(info.adjustable),
+        "resolution_seconds": info.resolution,
+        "implementation": info.implementation,
+        "sample_1_ns": sample_1,
+        "sample_2_ns": sample_2,
+        "same_process_host_domain": True,
+        "python_version": sys.version.replace("\n", " "),
+        "python_implementation": platform.python_implementation(),
+        "platform": platform.platform(),
+    }
diff --git a/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json b/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json
new file mode 100644
index 0000000..614d372
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json
@@ -0,0 +1,105 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION_V0_1",
+  "status": "PREREGISTERED_BEFORE_RED",
+  "base": {
+    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
+    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
+    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
+    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
+  },
+  "authority": {
+    "stage": "RPE-02",
+    "rpe02_implementation_authorized": true,
+    "rpe04_authorized": false,
+    "rpe05_authorized": false,
+    "rpe06_authorized": false,
+    "real_p5e_authorized": false,
+    "network_authorized": false,
+    "real_p5d4_state_mutation_authorized": false,
+    "vault_or_current_mutation_authorized": false
+  },
+  "architecture": {
+    "selected": "SEPARATE_REAL_TIME_MODEL_V0_2",
+    "synthetic_model_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE"
+  },
+  "governed_config": {
+    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
+    "private_guard_functions_forbidden": true,
+    "validate_schema_definition_not_document_entrypoint": true,
+    "runtime_preregistration_path": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json",
+    "runtime_schema_path": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json",
+    "environment_authority_forbidden": true,
+    "cli_authority_forbidden": true,
+    "unlisted_file_authority_forbidden": true
+  },
+  "representation": {
+    "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
+    "nanoseconds_per_second": 1000000000,
+    "poll_interval_ns": 30000000000,
+    "detection_latency_bound_ns": 60000000000,
+    "floating_point_seconds_normative_forbidden": true,
+    "lossy_integer_seconds_real_verdict_forbidden": true,
+    "required_fields": [
+      "schedule_origin_ns",
+      "scheduled_at_ns",
+      "attempt_started_at_ns",
+      "remote_observation_completed_at_ns",
+      "attempt_completed_at_ns",
+      "controlled_source_release_started_at_ns"
+    ]
+  },
+  "boundaries": {
+    "origin_release": "schedule_origin_ns < controlled_source_release_started_at_ns",
+    "first_slot": "schedule_origin_ns + poll_interval_ns",
+    "slot_grid": "scheduled_at_ns > schedule_origin_ns AND exact poll grid",
+    "release_on_slot": "THAT_SLOT_IS_FIRST_REQUIRED",
+    "release_after_slot": "NEXT_SLOT_IS_FIRST_REQUIRED",
+    "actual_start_min": "attempt_started_at_ns >= scheduled_at_ns",
+    "actual_start_max": "attempt_started_at_ns < scheduled_at_ns + poll_interval_ns",
+    "actual_start_equal_next_slot": "BLOCKED_ACTUAL_START_MISSED_FIXED_RATE_SLOT",
+    "remote_completion_min": "remote_observation_completed_at_ns >= attempt_started_at_ns",
+    "remote_completion_equal_next_slot": "ALLOWED",
+    "remote_completion_after_next_slot": "BLOCKED_ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
+    "attempt_completion_min": "attempt_completed_at_ns >= remote_observation_completed_at_ns",
+    "previous_completion_equal_next_start": "ALLOWED",
+    "previous_completion_gt_next_start": "BLOCKED_ATTEMPT_OVERLAP",
+    "eligible_detection": "attempt_started_at_ns >= controlled_source_release_started_at_ns",
+    "pre_release_target": "BLOCKED_REQUIRES_ADJUDICATION",
+    "latency_metric": "remote_observation_completed_at_ns - controlled_source_release_started_at_ns",
+    "latency_equal_bound": "PASS_DETECTED_WITHIN_BOUND",
+    "latency_gt_bound": "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+    "full_completion_role": "TIMELINE_AND_OVERLAP_ONLY_NOT_LATENCY"
+  },
+  "statuses": [
+    "BLOCKED_REQUIRES_ADJUDICATION",
+    "PASS_DETECTED_WITHIN_BOUND",
+    "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+    "FAIL_NO_DETECTION_BY_BOUND",
+    "INCOMPLETE_REAL_TIME_WINDOW"
+  ],
+  "mandatory_red_cases": [
+    "non-integer timestamps rejected",
+    "latency exactly 60 seconds passes",
+    "latency 60 seconds plus 1 nanosecond fails",
+    "late actual start cannot hide behind on-time slot",
+    "remote completion exactly next slot allowed",
+    "remote completion one nanosecond after next slot blocked",
+    "previous completion equal next start allowed",
+    "previous completion greater next start blocked",
+    "pre-release-started target observation blocked",
+    "full attempt completion does not replace remote completion latency endpoint",
+    "exact-grid parity with adopted synthetic model"
+  ],
+  "clock_capability": {
+    "required_api": "time.monotonic_ns",
+    "metadata_api": "time.get_clock_info('monotonic')",
+    "monotonic_true_required": true,
+    "adjustable_recorded": true,
+    "resolution_recorded": true,
+    "implementation_recorded": true,
+    "python_platform_recorded": true,
+    "same_process_host_domain_required": true
+  },
+  "stop": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+}
diff --git a/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json b/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json
new file mode 100644
index 0000000..923671b
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json
@@ -0,0 +1,371 @@
+{
+  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
+  "artifact_role": "RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION",
+  "root": {
+    "kind": "object",
+    "fields": {
+      "schema": {
+        "kind": "string",
+        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION_V0_1"
+      },
+      "status": {
+        "kind": "string",
+        "const": "PREREGISTERED_BEFORE_RED"
+      },
+      "base": {
+        "kind": "object",
+        "fields": {
+          "rpe01_adoption_commit": {
+            "kind": "string",
+            "const": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25"
+          },
+          "rpe01_adoption_blob": {
+            "kind": "string",
+            "const": "49203ebc2fb208c5dd23ded140295ac00c0afab6"
+          },
+          "rpe01_guard_blob": {
+            "kind": "string",
+            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
+          },
+          "p5e_contract_blob": {
+            "kind": "string",
+            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
+          },
+          "p5e_synthetic_model_blob": {
+            "kind": "string",
+            "const": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
+          }
+        }
+      },
+      "authority": {
+        "kind": "object",
+        "fields": {
+          "stage": {
+            "kind": "string",
+            "const": "RPE-02"
+          },
+          "rpe02_implementation_authorized": {
+            "kind": "boolean",
+            "const": true
+          },
+          "rpe04_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "rpe05_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "rpe06_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "real_p5e_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "network_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "real_p5d4_state_mutation_authorized": {
+            "kind": "boolean",
+            "const": false
+          },
+          "vault_or_current_mutation_authorized": {
+            "kind": "boolean",
+            "const": false
+          }
+        }
+      },
+      "architecture": {
+        "kind": "object",
+        "fields": {
+          "selected": {
+            "kind": "string",
+            "const": "SEPARATE_REAL_TIME_MODEL_V0_2"
+          },
+          "synthetic_model_role": {
+            "kind": "string",
+            "const": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE"
+          }
+        }
+      },
+      "governed_config": {
+        "kind": "object",
+        "fields": {
+          "authorized_entrypoint": {
+            "kind": "string",
+            "const": "validate_governed_json(raw_document, raw_schema)"
+          },
+          "private_guard_functions_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "validate_schema_definition_not_document_entrypoint": {
+            "kind": "boolean",
+            "const": true
+          },
+          "runtime_preregistration_path": {
+            "kind": "string",
+            "const": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json"
+          },
+          "runtime_schema_path": {
+            "kind": "string",
+            "const": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json"
+          },
+          "environment_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "cli_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "unlisted_file_authority_forbidden": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "representation": {
+        "kind": "object",
+        "fields": {
+          "normative_unit": {
+            "kind": "string",
+            "const": "INTEGER_MONOTONIC_NANOSECONDS"
+          },
+          "nanoseconds_per_second": {
+            "kind": "integer",
+            "const": 1000000000
+          },
+          "poll_interval_ns": {
+            "kind": "integer",
+            "const": 30000000000
+          },
+          "detection_latency_bound_ns": {
+            "kind": "integer",
+            "const": 60000000000
+          },
+          "floating_point_seconds_normative_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "lossy_integer_seconds_real_verdict_forbidden": {
+            "kind": "boolean",
+            "const": true
+          },
+          "required_fields": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 6,
+            "max_items": 6,
+            "unique": true,
+            "ordered_const": [
+              "schedule_origin_ns",
+              "scheduled_at_ns",
+              "attempt_started_at_ns",
+              "remote_observation_completed_at_ns",
+              "attempt_completed_at_ns",
+              "controlled_source_release_started_at_ns"
+            ],
+            "allowed_values": [
+              "schedule_origin_ns",
+              "scheduled_at_ns",
+              "attempt_started_at_ns",
+              "remote_observation_completed_at_ns",
+              "attempt_completed_at_ns",
+              "controlled_source_release_started_at_ns"
+            ]
+          }
+        }
+      },
+      "boundaries": {
+        "kind": "object",
+        "fields": {
+          "origin_release": {
+            "kind": "string",
+            "const": "schedule_origin_ns < controlled_source_release_started_at_ns"
+          },
+          "first_slot": {
+            "kind": "string",
+            "const": "schedule_origin_ns + poll_interval_ns"
+          },
+          "slot_grid": {
+            "kind": "string",
+            "const": "scheduled_at_ns > schedule_origin_ns AND exact poll grid"
+          },
+          "release_on_slot": {
+            "kind": "string",
+            "const": "THAT_SLOT_IS_FIRST_REQUIRED"
+          },
+          "release_after_slot": {
+            "kind": "string",
+            "const": "NEXT_SLOT_IS_FIRST_REQUIRED"
+          },
+          "actual_start_min": {
+            "kind": "string",
+            "const": "attempt_started_at_ns >= scheduled_at_ns"
+          },
+          "actual_start_max": {
+            "kind": "string",
+            "const": "attempt_started_at_ns < scheduled_at_ns + poll_interval_ns"
+          },
+          "actual_start_equal_next_slot": {
+            "kind": "string",
+            "const": "BLOCKED_ACTUAL_START_MISSED_FIXED_RATE_SLOT"
+          },
+          "remote_completion_min": {
+            "kind": "string",
+            "const": "remote_observation_completed_at_ns >= attempt_started_at_ns"
+          },
+          "remote_completion_equal_next_slot": {
+            "kind": "string",
+            "const": "ALLOWED"
+          },
+          "remote_completion_after_next_slot": {
+            "kind": "string",
+            "const": "BLOCKED_ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
+          },
+          "attempt_completion_min": {
+            "kind": "string",
+            "const": "attempt_completed_at_ns >= remote_observation_completed_at_ns"
+          },
+          "previous_completion_equal_next_start": {
+            "kind": "string",
+            "const": "ALLOWED"
+          },
+          "previous_completion_gt_next_start": {
+            "kind": "string",
+            "const": "BLOCKED_ATTEMPT_OVERLAP"
+          },
+          "eligible_detection": {
+            "kind": "string",
+            "const": "attempt_started_at_ns >= controlled_source_release_started_at_ns"
+          },
+          "pre_release_target": {
+            "kind": "string",
+            "const": "BLOCKED_REQUIRES_ADJUDICATION"
+          },
+          "latency_metric": {
+            "kind": "string",
+            "const": "remote_observation_completed_at_ns - controlled_source_release_started_at_ns"
+          },
+          "latency_equal_bound": {
+            "kind": "string",
+            "const": "PASS_DETECTED_WITHIN_BOUND"
+          },
+          "latency_gt_bound": {
+            "kind": "string",
+            "const": "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
+          },
+          "full_completion_role": {
+            "kind": "string",
+            "const": "TIMELINE_AND_OVERLAP_ONLY_NOT_LATENCY"
+          }
+        }
+      },
+      "statuses": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 5,
+        "max_items": 5,
+        "unique": true,
+        "ordered_const": [
+          "BLOCKED_REQUIRES_ADJUDICATION",
+          "PASS_DETECTED_WITHIN_BOUND",
+          "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+          "FAIL_NO_DETECTION_BY_BOUND",
+          "INCOMPLETE_REAL_TIME_WINDOW"
+        ],
+        "allowed_values": [
+          "BLOCKED_REQUIRES_ADJUDICATION",
+          "PASS_DETECTED_WITHIN_BOUND",
+          "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
+          "FAIL_NO_DETECTION_BY_BOUND",
+          "INCOMPLETE_REAL_TIME_WINDOW"
+        ]
+      },
+      "mandatory_red_cases": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 11,
+        "max_items": 11,
+        "unique": true,
+        "ordered_const": [
+          "non-integer timestamps rejected",
+          "latency exactly 60 seconds passes",
+          "latency 60 seconds plus 1 nanosecond fails",
+          "late actual start cannot hide behind on-time slot",
+          "remote completion exactly next slot allowed",
+          "remote completion one nanosecond after next slot blocked",
+          "previous completion equal next start allowed",
+          "previous completion greater next start blocked",
+          "pre-release-started target observation blocked",
+          "full attempt completion does not replace remote completion latency endpoint",
+          "exact-grid parity with adopted synthetic model"
+        ],
+        "allowed_values": [
+          "non-integer timestamps rejected",
+          "latency exactly 60 seconds passes",
+          "latency 60 seconds plus 1 nanosecond fails",
+          "late actual start cannot hide behind on-time slot",
+          "remote completion exactly next slot allowed",
+          "remote completion one nanosecond after next slot blocked",
+          "previous completion equal next start allowed",
+          "previous completion greater next start blocked",
+          "pre-release-started target observation blocked",
+          "full attempt completion does not replace remote completion latency endpoint",
+          "exact-grid parity with adopted synthetic model"
+        ]
+      },
+      "clock_capability": {
+        "kind": "object",
+        "fields": {
+          "required_api": {
+            "kind": "string",
+            "const": "time.monotonic_ns"
+          },
+          "metadata_api": {
+            "kind": "string",
+            "const": "time.get_clock_info('monotonic')"
+          },
+          "monotonic_true_required": {
+            "kind": "boolean",
+            "const": true
+          },
+          "adjustable_recorded": {
+            "kind": "boolean",
+            "const": true
+          },
+          "resolution_recorded": {
+            "kind": "boolean",
+            "const": true
+          },
+          "implementation_recorded": {
+            "kind": "boolean",
+            "const": true
+          },
+          "python_platform_recorded": {
+            "kind": "boolean",
+            "const": true
+          },
+          "same_process_host_domain_required": {
+            "kind": "boolean",
+            "const": true
+          }
+        }
+      },
+      "stop": {
+        "kind": "string",
+        "const": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
+      }
+    }
+  }
+}
diff --git a/tools/obsidian_projection/rpe02_real_time_representation_qualification_v0_1.json b/tools/obsidian_projection/rpe02_real_time_representation_qualification_v0_1.json
new file mode 100644
index 0000000..81d225d
--- /dev/null
+++ b/tools/obsidian_projection/rpe02_real_time_representation_qualification_v0_1.json
@@ -0,0 +1,108 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
+  "date": "2026-10-03",
+  "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
+  "base": {
+    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
+    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
+    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
+    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
+  },
+  "preregistration": {
+    "head": "c42a0f3df48807b3681db782f0a6fd58bd5c7aea",
+    "blob": "614d3724c5c36bbdb6afbf9b49a31f88da465719",
+    "schema_blob": "923671b1539585b5c32c8e2d284598b521fc0bba",
+    "predraft_blob": "a5d559ebb854c029dbdeb5834562864c7c035f02"
+  },
+  "red": {
+    "head": "03394a8a85680ca24a2593d14466c192fd208e8e",
+    "test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
+    "report_blob": "0c5f30c7cce63e5d149111bae4d5b3309367f4af",
+    "result": "17 tests; 15 failures; 2 passes; implementation absent"
+  },
+  "implementation": {
+    "head": "c17d68b04de9dca13f9d9ed655e034b13436484d",
+    "module_blob": "db5dcfe8ad3b7ce93099368b459bb09ac25f933b",
+    "main_test_blob": "23618a9317c554099670e84482641a8014f8682d",
+    "mutation_test_blob": "77cdadb376320c4e8f591a3a80105feac250b716"
+  },
+  "qualified_properties": {
+    "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
+    "schedule_origin_ns": true,
+    "scheduled_at_ns": true,
+    "attempt_started_at_ns": true,
+    "remote_observation_completed_at_ns": true,
+    "attempt_completed_at_ns": true,
+    "controlled_source_release_started_at_ns": true,
+    "poll_interval_ns": 30000000000,
+    "detection_latency_bound_ns": 60000000000,
+    "actual_start_drives_attempt_eligibility": true,
+    "pre_release_started_target_observation_blocks": true,
+    "remote_completion_is_latency_endpoint": true,
+    "full_attempt_completion_is_not_latency_endpoint": true,
+    "remote_completion_equal_next_slot_allowed": true,
+    "remote_completion_after_next_slot_blocked": true,
+    "previous_completion_equal_next_start_allowed": true,
+    "overlap_blocked": true,
+    "exact_bound_passes": true,
+    "bound_plus_one_nanosecond_fails": true,
+    "exact_grid_parity_with_synthetic_reference": true,
+    "float_or_bool_timestamp_authority_rejected": true,
+    "environment_or_cli_normative_authority_absent": true,
+    "implementation_constants_match_governed_preregistration": true
+  },
+  "mutation_discrimination": {
+    "checks": 4,
+    "kills": 4,
+    "survivors": 0,
+    "families": [
+      "exact latency-bound comparison operator",
+      "actual-start next-slot comparison operator",
+      "remote-completion next-slot comparison operator",
+      "remote-completion versus full-attempt-completion latency endpoint"
+    ]
+  },
+  "test_results": {
+    "dedicated_surface": "22/22 PASS",
+    "full_targeted_regression": "135/135 PASS",
+    "p5e_contract_diff": 0,
+    "p5e_synthetic_model_diff": 0,
+    "p5d4_runtime_diff": 0
+  },
+  "host_clock_capability_non_normative": {
+    "api": "time.monotonic_ns",
+    "metadata_api": "time.get_clock_info('monotonic')",
+    "monotonic": true,
+    "adjustable": false,
+    "resolution_seconds": 1e-7,
+    "implementation": "QueryPerformanceCounter()",
+    "sample_1_ns": 4845925967277900,
+    "sample_2_ns": 4845925967278100,
+    "same_process_host_domain": true,
+    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
+    "python_implementation": "CPython",
+    "platform": "Windows-11-10.0.22631-SP0"
+  },
+  "real_p5d4_state_unchanged": {
+    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
+    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
+    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
+  },
+  "claim_boundary": {
+    "rpe02_qualified_for_external_review": true,
+    "rpe02_human_adopted": false,
+    "rpe03_status_untouched_by_this_branch": true,
+    "rpe04_opened": false,
+    "rpe05_opened": false,
+    "rpe06_opened": false,
+    "real_p5e_authorized": false,
+    "network_used": false,
+    "p5d4_real_state_mutated": false,
+    "vault_or_current_mutated": false
+  },
+  "next_gate": "INDEPENDENT_EXTERNAL_REVIEW_THEN_HUMAN_ADJUDICATION",
+  "stop": true
+}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-01 HUMAN ADOPTION
Path: GOVERNANCE/RPE-01-N4-GOVERNED-CLOSED-SCHEMA-HUMAN-ADJUDICATION-2026-10-03.md
Authoritative Git blob: 49203ebc2fb208c5dd23ded140295ac00c0afab6
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-01 — N4 GOVERNED CLOSED SCHEMA — HUMAN ADJUDICATION

Date: 2026-10-03

## Human decision

The human authority adopts:

`RPE-01 — N4 GOVERNED CLOSED SCHEMA`

in its final qualified state after:
- initial RPE-01 qualification;
- external review `PASS_WITH_NON_BLOCKING_NOTES` with no blocker;
- NB-1 / NB-2 targeted closure;
- portability and raw-breaker discrimination hardening;
- final external delta-review `PASS_WITH_NON_BLOCKING_NOTES` with `BLOCKING_FINDINGS = NONE`;
- NB-α scanner string/escape test-only closure.

The adopted normative state is:

`RPE01_GOVERNED_CLOSED_SCHEMA = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-01 = CLOSED`

This adoption does not automatically open RPE-02 or RPE-03.

## Binding pre-adoption identity

This human adoption is bound to the exact pre-adoption repository state:

```text
PRE-ADOPTION HEAD
= 686e9266f84e1a9ae05938bf3260728492a17c92

FINAL GUARD
= 26f977961d72a062199d71ffd628d5a5cc047887

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

FINAL HARDENING QUALIFICATION
= f514af4bf01a62b3f751e14cfffaaf20bfe66885

FINAL HARDENING QUALIFICATION REPORT
= 92e45cf8fa279c0b9643a9ad77d4c1f19d6a7cdf

NB-α TEST
= a170019180579f82e9f9ea0918f4fed445cab1ba

NB-α CLOSURE PROOF
= 76e8b5c2f85fc1088df0a25ef3df194f63904b75
```

Branch at adoption:

`feat/obsidian-projection-rpe01-governed-closed-schema-v0.1`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.

## Adopted governed-artifact consumer contract

The following constraints are adopted for every future consumer of RPE-01:

```text
AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)

UNDERSCORE-PREFIXED GUARD FUNCTIONS
= FORBIDDEN FOR EXTERNAL CONSUMERS

validate_schema_definition
= NOT AN AUTHORIZED GOVERNED-DOCUMENT VALIDATION ENTRYPOINT
```

RPE-02, RPE-03 and later consumers must carry this contract explicitly into their preregistration and implementation boundaries.

No future consumer may use a private `_*` guard function as a normative validation path.

## Adopted deterministic JSON depth rule

The final qualified guard contains the preregistered rule:

```text
MAX_GOVERNED_JSON_DEPTH = 64
```

Normative interpretation:

- JSON container nesting is counted lexically outside strings;
- a root object or array has depth 1;
- document and schema raw JSON are both checked before `json.loads`;
- depth `<= 64` is permitted by the depth guard subject to all other validation;
- depth `> 64` is rejected with `GovernedSchemaError`;
- interpreter recursion limits are not normative.

Residual validation recursion is normalized to `GovernedSchemaError` at the qualified boundary.

## Final scanner string/escape proof

NB-α is accepted as test-locked by the final test-only closure.

The qualified guard itself was not modified during NB-α closure.

The final proof establishes:

```text
container characters inside governed JSON strings
→ do not consume JSON depth budget

escaped quote/backslash handling
→ cannot hide later real container depth

in_string mutant
→ KILLED

escaped-state mutant
→ KILLED
```

Final local evidence before adoption:

```text
NB-α dedicated tests
= 4 / 4 PASS

current RPE-01 surface
= 46 / 46 PASS

P5-E + RPE-01 targeted regression
= 113 / 113 PASS
```

## Retained scope boundaries

### NB-3 — structural scope

RPE-01 protects:

- closed object structure;
- strict JSON/member handling;
- strict types;
- closed normative lists and list order where specified;
- governed schema-language structure;
- deterministic JSON depth;
- fail-closed parser/validation behavior covered by the qualified guard.

RPE-01 does not replace the adopted P5-E value-semantic invariant layer.

Existing P5-E invariants continue to carry value semantics.

Future schemas that themselves carry authority flags should normally encode those flags with explicit constraints such as `const: false` where preregistered.

### NB-4 — binding scope

`source_binding` and `artifact_role` are structurally represented and validated.

The generic RPE-01 guard does not claim dynamic verification of expected artifact role or recomputation/enforcement of source Git blob identity.

Where such dynamic binding is required, the future consumer/caller boundary must preregister and enforce it explicitly.

### NB-5 — non-blocking future hardening

The following remain non-blocking future hardening only where a distinct future failure mode requires them:

- proactive rejection of contradictory restrictive schema constraints;
- explicit ASCII regex semantics where relevant;
- isolated Unicode-surrogate handling where downstream UTF-8 persistence requires it.

These notes do not reopen RPE-01.

## NB-β / NB-c consumer-state interpretation

Static repository checks before adoption found no runtime Python consumer under `tools/` using:

- `validate_schema_definition`;
- `_validate_document`;
- `_validate_document_node`;
- `_validate_schema_node`.

No runtime Python consumer currently invokes `validate_governed_json`, which is expected because RPE-02/RPE-03 remain unopened.

Tests may exercise schema utilities directly for qualification purposes; this does not constitute a runtime governed-document consumer.

The consumer contract above is mandatory for future stages.

## Protected predecessor integrity

At adoption, the protected identities remain:

```text
P5-E ADOPTED CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E ADOPTED SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac

P5-D4 RUNTIME
= 1825e53d195ba2a63b5b646a5b78eb77939b94b5
```

No mutation of those artifacts is part of this adoption.

## Real P5-D4 state integrity before adoption

```text
observer-events.jsonl SHA256
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json SHA256
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json SHA256
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

No real P5-D4 control-state mutation is authorized by this persistence step.

## Stage state after verified persistence

The human decision closes RPE-01 only.

```text
RPE-01
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-02
= CLOSED

RPE-03
= CLOSED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

Under the already adopted readiness DAG, RPE-02 and RPE-03 become eligible to be separately opened after RPE-01 closure, but this record does not itself open or authorize either stage.

## Explicitly not authorized

This adoption does not authorize:

- implementation or execution of RPE-02;
- implementation or execution of RPE-03;
- implementation or execution of RPE-04;
- implementation or execution of RPE-05;
- implementation or execution of RPE-06;
- real GitHub polling;
- sandbox repository or ref creation;
- experimental push;
- real HEAD evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- real P5-D4 control-state mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.

`REAL_P5E = CLOSED`

## Persistence authority

The only operations authorized by the human adoption statement are:

- persist this adjudication record;
- commit and push it;
- verify final repository consistency;
- STOP.

No guard, schema, qualification, test, P5-E contract/model, P5-D4 runtime, control state, Vault, CURRENT or future RPE artifact may be modified by this persistence step.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 PREREGISTRATION
Path: tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json
Authoritative Git blob: 614d3724c5c36bbdb6afbf9b49a31f88da465719
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "base": {
    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
  },
  "authority": {
    "stage": "RPE-02",
    "rpe02_implementation_authorized": true,
    "rpe04_authorized": false,
    "rpe05_authorized": false,
    "rpe06_authorized": false,
    "real_p5e_authorized": false,
    "network_authorized": false,
    "real_p5d4_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false
  },
  "architecture": {
    "selected": "SEPARATE_REAL_TIME_MODEL_V0_2",
    "synthetic_model_role": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE"
  },
  "governed_config": {
    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "private_guard_functions_forbidden": true,
    "validate_schema_definition_not_document_entrypoint": true,
    "runtime_preregistration_path": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json",
    "runtime_schema_path": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json",
    "environment_authority_forbidden": true,
    "cli_authority_forbidden": true,
    "unlisted_file_authority_forbidden": true
  },
  "representation": {
    "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
    "nanoseconds_per_second": 1000000000,
    "poll_interval_ns": 30000000000,
    "detection_latency_bound_ns": 60000000000,
    "floating_point_seconds_normative_forbidden": true,
    "lossy_integer_seconds_real_verdict_forbidden": true,
    "required_fields": [
      "schedule_origin_ns",
      "scheduled_at_ns",
      "attempt_started_at_ns",
      "remote_observation_completed_at_ns",
      "attempt_completed_at_ns",
      "controlled_source_release_started_at_ns"
    ]
  },
  "boundaries": {
    "origin_release": "schedule_origin_ns < controlled_source_release_started_at_ns",
    "first_slot": "schedule_origin_ns + poll_interval_ns",
    "slot_grid": "scheduled_at_ns > schedule_origin_ns AND exact poll grid",
    "release_on_slot": "THAT_SLOT_IS_FIRST_REQUIRED",
    "release_after_slot": "NEXT_SLOT_IS_FIRST_REQUIRED",
    "actual_start_min": "attempt_started_at_ns >= scheduled_at_ns",
    "actual_start_max": "attempt_started_at_ns < scheduled_at_ns + poll_interval_ns",
    "actual_start_equal_next_slot": "BLOCKED_ACTUAL_START_MISSED_FIXED_RATE_SLOT",
    "remote_completion_min": "remote_observation_completed_at_ns >= attempt_started_at_ns",
    "remote_completion_equal_next_slot": "ALLOWED",
    "remote_completion_after_next_slot": "BLOCKED_ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "attempt_completion_min": "attempt_completed_at_ns >= remote_observation_completed_at_ns",
    "previous_completion_equal_next_start": "ALLOWED",
    "previous_completion_gt_next_start": "BLOCKED_ATTEMPT_OVERLAP",
    "eligible_detection": "attempt_started_at_ns >= controlled_source_release_started_at_ns",
    "pre_release_target": "BLOCKED_REQUIRES_ADJUDICATION",
    "latency_metric": "remote_observation_completed_at_ns - controlled_source_release_started_at_ns",
    "latency_equal_bound": "PASS_DETECTED_WITHIN_BOUND",
    "latency_gt_bound": "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
    "full_completion_role": "TIMELINE_AND_OVERLAP_ONLY_NOT_LATENCY"
  },
  "statuses": [
    "BLOCKED_REQUIRES_ADJUDICATION",
    "PASS_DETECTED_WITHIN_BOUND",
    "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
    "FAIL_NO_DETECTION_BY_BOUND",
    "INCOMPLETE_REAL_TIME_WINDOW"
  ],
  "mandatory_red_cases": [
    "non-integer timestamps rejected",
    "latency exactly 60 seconds passes",
    "latency 60 seconds plus 1 nanosecond fails",
    "late actual start cannot hide behind on-time slot",
    "remote completion exactly next slot allowed",
    "remote completion one nanosecond after next slot blocked",
    "previous completion equal next start allowed",
    "previous completion greater next start blocked",
    "pre-release-started target observation blocked",
    "full attempt completion does not replace remote completion latency endpoint",
    "exact-grid parity with adopted synthetic model"
  ],
  "clock_capability": {
    "required_api": "time.monotonic_ns",
    "metadata_api": "time.get_clock_info('monotonic')",
    "monotonic_true_required": true,
    "adjustable_recorded": true,
    "resolution_recorded": true,
    "implementation_recorded": true,
    "python_platform_recorded": true,
    "same_process_host_domain_required": true
  },
  "stop": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 PREREGISTRATION SCHEMA
Path: tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json
Authoritative Git blob: 923671b1539585b5c32c8e2d284598b521fc0bba
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION",
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string",
        "const": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_PREREGISTRATION_V0_1"
      },
      "status": {
        "kind": "string",
        "const": "PREREGISTERED_BEFORE_RED"
      },
      "base": {
        "kind": "object",
        "fields": {
          "rpe01_adoption_commit": {
            "kind": "string",
            "const": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25"
          },
          "rpe01_adoption_blob": {
            "kind": "string",
            "const": "49203ebc2fb208c5dd23ded140295ac00c0afab6"
          },
          "rpe01_guard_blob": {
            "kind": "string",
            "const": "26f977961d72a062199d71ffd628d5a5cc047887"
          },
          "p5e_contract_blob": {
            "kind": "string",
            "const": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
          },
          "p5e_synthetic_model_blob": {
            "kind": "string",
            "const": "c0f16baa151c1466e30ba5778f1fca8184cd4aac"
          }
        }
      },
      "authority": {
        "kind": "object",
        "fields": {
          "stage": {
            "kind": "string",
            "const": "RPE-02"
          },
          "rpe02_implementation_authorized": {
            "kind": "boolean",
            "const": true
          },
          "rpe04_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe05_authorized": {
            "kind": "boolean",
            "const": false
          },
          "rpe06_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5e_authorized": {
            "kind": "boolean",
            "const": false
          },
          "network_authorized": {
            "kind": "boolean",
            "const": false
          },
          "real_p5d4_state_mutation_authorized": {
            "kind": "boolean",
            "const": false
          },
          "vault_or_current_mutation_authorized": {
            "kind": "boolean",
            "const": false
          }
        }
      },
      "architecture": {
        "kind": "object",
        "fields": {
          "selected": {
            "kind": "string",
            "const": "SEPARATE_REAL_TIME_MODEL_V0_2"
          },
          "synthetic_model_role": {
            "kind": "string",
            "const": "IMMUTABLE_SEMANTIC_AND_EXACT_GRID_PARITY_REFERENCE"
          }
        }
      },
      "governed_config": {
        "kind": "object",
        "fields": {
          "authorized_entrypoint": {
            "kind": "string",
            "const": "validate_governed_json(raw_document, raw_schema)"
          },
          "private_guard_functions_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "validate_schema_definition_not_document_entrypoint": {
            "kind": "boolean",
            "const": true
          },
          "runtime_preregistration_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1.json"
          },
          "runtime_schema_path": {
            "kind": "string",
            "const": "tools/obsidian_projection/rpe02_real_time_representation_preregistration_v0_1_schema_v0_1.json"
          },
          "environment_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "cli_authority_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "unlisted_file_authority_forbidden": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "representation": {
        "kind": "object",
        "fields": {
          "normative_unit": {
            "kind": "string",
            "const": "INTEGER_MONOTONIC_NANOSECONDS"
          },
          "nanoseconds_per_second": {
            "kind": "integer",
            "const": 1000000000
          },
          "poll_interval_ns": {
            "kind": "integer",
            "const": 30000000000
          },
          "detection_latency_bound_ns": {
            "kind": "integer",
            "const": 60000000000
          },
          "floating_point_seconds_normative_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "lossy_integer_seconds_real_verdict_forbidden": {
            "kind": "boolean",
            "const": true
          },
          "required_fields": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 6,
            "max_items": 6,
            "unique": true,
            "ordered_const": [
              "schedule_origin_ns",
              "scheduled_at_ns",
              "attempt_started_at_ns",
              "remote_observation_completed_at_ns",
              "attempt_completed_at_ns",
              "controlled_source_release_started_at_ns"
            ],
            "allowed_values": [
              "schedule_origin_ns",
              "scheduled_at_ns",
              "attempt_started_at_ns",
              "remote_observation_completed_at_ns",
              "attempt_completed_at_ns",
              "controlled_source_release_started_at_ns"
            ]
          }
        }
      },
      "boundaries": {
        "kind": "object",
        "fields": {
          "origin_release": {
            "kind": "string",
            "const": "schedule_origin_ns < controlled_source_release_started_at_ns"
          },
          "first_slot": {
            "kind": "string",
            "const": "schedule_origin_ns + poll_interval_ns"
          },
          "slot_grid": {
            "kind": "string",
            "const": "scheduled_at_ns > schedule_origin_ns AND exact poll grid"
          },
          "release_on_slot": {
            "kind": "string",
            "const": "THAT_SLOT_IS_FIRST_REQUIRED"
          },
          "release_after_slot": {
            "kind": "string",
            "const": "NEXT_SLOT_IS_FIRST_REQUIRED"
          },
          "actual_start_min": {
            "kind": "string",
            "const": "attempt_started_at_ns >= scheduled_at_ns"
          },
          "actual_start_max": {
            "kind": "string",
            "const": "attempt_started_at_ns < scheduled_at_ns + poll_interval_ns"
          },
          "actual_start_equal_next_slot": {
            "kind": "string",
            "const": "BLOCKED_ACTUAL_START_MISSED_FIXED_RATE_SLOT"
          },
          "remote_completion_min": {
            "kind": "string",
            "const": "remote_observation_completed_at_ns >= attempt_started_at_ns"
          },
          "remote_completion_equal_next_slot": {
            "kind": "string",
            "const": "ALLOWED"
          },
          "remote_completion_after_next_slot": {
            "kind": "string",
            "const": "BLOCKED_ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
          },
          "attempt_completion_min": {
            "kind": "string",
            "const": "attempt_completed_at_ns >= remote_observation_completed_at_ns"
          },
          "previous_completion_equal_next_start": {
            "kind": "string",
            "const": "ALLOWED"
          },
          "previous_completion_gt_next_start": {
            "kind": "string",
            "const": "BLOCKED_ATTEMPT_OVERLAP"
          },
          "eligible_detection": {
            "kind": "string",
            "const": "attempt_started_at_ns >= controlled_source_release_started_at_ns"
          },
          "pre_release_target": {
            "kind": "string",
            "const": "BLOCKED_REQUIRES_ADJUDICATION"
          },
          "latency_metric": {
            "kind": "string",
            "const": "remote_observation_completed_at_ns - controlled_source_release_started_at_ns"
          },
          "latency_equal_bound": {
            "kind": "string",
            "const": "PASS_DETECTED_WITHIN_BOUND"
          },
          "latency_gt_bound": {
            "kind": "string",
            "const": "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
          },
          "full_completion_role": {
            "kind": "string",
            "const": "TIMELINE_AND_OVERLAP_ONLY_NOT_LATENCY"
          }
        }
      },
      "statuses": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 5,
        "max_items": 5,
        "unique": true,
        "ordered_const": [
          "BLOCKED_REQUIRES_ADJUDICATION",
          "PASS_DETECTED_WITHIN_BOUND",
          "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
          "FAIL_NO_DETECTION_BY_BOUND",
          "INCOMPLETE_REAL_TIME_WINDOW"
        ],
        "allowed_values": [
          "BLOCKED_REQUIRES_ADJUDICATION",
          "PASS_DETECTED_WITHIN_BOUND",
          "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
          "FAIL_NO_DETECTION_BY_BOUND",
          "INCOMPLETE_REAL_TIME_WINDOW"
        ]
      },
      "mandatory_red_cases": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 11,
        "max_items": 11,
        "unique": true,
        "ordered_const": [
          "non-integer timestamps rejected",
          "latency exactly 60 seconds passes",
          "latency 60 seconds plus 1 nanosecond fails",
          "late actual start cannot hide behind on-time slot",
          "remote completion exactly next slot allowed",
          "remote completion one nanosecond after next slot blocked",
          "previous completion equal next start allowed",
          "previous completion greater next start blocked",
          "pre-release-started target observation blocked",
          "full attempt completion does not replace remote completion latency endpoint",
          "exact-grid parity with adopted synthetic model"
        ],
        "allowed_values": [
          "non-integer timestamps rejected",
          "latency exactly 60 seconds passes",
          "latency 60 seconds plus 1 nanosecond fails",
          "late actual start cannot hide behind on-time slot",
          "remote completion exactly next slot allowed",
          "remote completion one nanosecond after next slot blocked",
          "previous completion equal next start allowed",
          "previous completion greater next start blocked",
          "pre-release-started target observation blocked",
          "full attempt completion does not replace remote completion latency endpoint",
          "exact-grid parity with adopted synthetic model"
        ]
      },
      "clock_capability": {
        "kind": "object",
        "fields": {
          "required_api": {
            "kind": "string",
            "const": "time.monotonic_ns"
          },
          "metadata_api": {
            "kind": "string",
            "const": "time.get_clock_info('monotonic')"
          },
          "monotonic_true_required": {
            "kind": "boolean",
            "const": true
          },
          "adjustable_recorded": {
            "kind": "boolean",
            "const": true
          },
          "resolution_recorded": {
            "kind": "boolean",
            "const": true
          },
          "implementation_recorded": {
            "kind": "boolean",
            "const": true
          },
          "python_platform_recorded": {
            "kind": "boolean",
            "const": true
          },
          "same_process_host_domain_required": {
            "kind": "boolean",
            "const": true
          }
        }
      },
      "stop": {
        "kind": "string",
        "const": "EXTERNAL_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
      }
    }
  }
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 RED TEST
Path: tests/obsidian_projection/test_rpe02_real_time_representation_v0_1.py
Authoritative Git blob: 23618a9317c554099670e84482641a8014f8682d
Display copy is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 RED REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-RED.md
Authoritative Git blob: 0c5f30c7cce63e5d149111bae4d5b3309367f4af
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
﻿# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

Preregistration HEAD:
c42a0f3df48807b3681db782f0a6fd58bd5c7aea

Preregistration blob:
614d3724c5c36bbdb6afbf9b49a31f88da465719

Preregistration schema blob:
923671b1539585b5c32c8e2d284598b521fc0bba

## RED command

python -B -m unittest tests.obsidian_projection.test_rpe02_real_time_representation_v0_1

## Observed result

Ran 17 tests.

FAILED (failures=15).

RPE02_RED_EXIT=1.

Two tests passed:
- governed preregistration validates through RPE-01;
- the absent implementation source contains no environment/CLI authority by construction.

The fifteen RED failures all arise because the preregistered module
tools/obsidian_projection/rpe02_real_time_model_v0_1.py
does not yet exist.

The frozen test surface already covers integer-nanosecond representation, exact 60-second and +1 ns boundaries, actual-start semantics, next-slot completion equality, overlap equality, pre-release target handling, remote-completion versus full-completion separation, release ceiling, synthetic parity and host monotonic-clock evidence.

No network or protected predecessor mutation occurred.

RPE-04 = CLOSED.
RPE-05 = CLOSED.
RPE-06 = CLOSED.
REAL P5-E = CLOSED.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 IMPLEMENTATION
Path: tools/obsidian_projection/rpe02_real_time_model_v0_1.py
Authoritative Git blob: db5dcfe8ad3b7ce93099368b459bb09ac25f933b
Display copy is normalized for packet formatting and is not claimed byte-identical.
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
    if type(out["outcome"]) is not str or not out["outcome"]:
        raise RPE02TimingError(f"observations[{index}].outcome must be non-empty string")
    if out["observed_head"] is not None:
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
    normalized.sort(key=lambda item: item["scheduled_at_ns"])

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

    window_end = max(
        (item["remote_observation_completed_at_ns"] for item in normalized),
        default=origin,
    )
    if window_end >= release + bound:
        return {
            "status": "FAIL_NO_DETECTION_BY_BOUND",
            "failure_code": None,
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

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 MUTATION TEST
Path: tests/obsidian_projection/test_rpe02_real_time_representation_mutation_v0_1.py
Authoritative Git blob: 77cdadb376320c4e8f591a3a80105feac250b716
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
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
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 QUALIFICATION JSON
Path: tools/obsidian_projection/rpe02_real_time_representation_qualification_v0_1.json
Authoritative Git blob: 81d225d932a985d65a627d727b0b164950a32865
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE02_REAL_TIME_REPRESENTATION_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
  "date": "2026-10-03",
  "branch": "feat/obsidian-projection-rpe02-real-time-representation-v0.1",
  "base": {
    "rpe01_adoption_commit": "8ed3ec4079f3f996a5159b78fc40d0f32a917b25",
    "rpe01_adoption_blob": "49203ebc2fb208c5dd23ded140295ac00c0afab6",
    "rpe01_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
    "p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "p5e_synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5"
  },
  "preregistration": {
    "head": "c42a0f3df48807b3681db782f0a6fd58bd5c7aea",
    "blob": "614d3724c5c36bbdb6afbf9b49a31f88da465719",
    "schema_blob": "923671b1539585b5c32c8e2d284598b521fc0bba",
    "predraft_blob": "a5d559ebb854c029dbdeb5834562864c7c035f02"
  },
  "red": {
    "head": "03394a8a85680ca24a2593d14466c192fd208e8e",
    "test_blob": "089a72c736302abd08ea1267c149e2ef771240db",
    "report_blob": "0c5f30c7cce63e5d149111bae4d5b3309367f4af",
    "result": "17 tests; 15 failures; 2 passes; implementation absent"
  },
  "implementation": {
    "head": "c17d68b04de9dca13f9d9ed655e034b13436484d",
    "module_blob": "db5dcfe8ad3b7ce93099368b459bb09ac25f933b",
    "main_test_blob": "23618a9317c554099670e84482641a8014f8682d",
    "mutation_test_blob": "77cdadb376320c4e8f591a3a80105feac250b716"
  },
  "qualified_properties": {
    "normative_unit": "INTEGER_MONOTONIC_NANOSECONDS",
    "schedule_origin_ns": true,
    "scheduled_at_ns": true,
    "attempt_started_at_ns": true,
    "remote_observation_completed_at_ns": true,
    "attempt_completed_at_ns": true,
    "controlled_source_release_started_at_ns": true,
    "poll_interval_ns": 30000000000,
    "detection_latency_bound_ns": 60000000000,
    "actual_start_drives_attempt_eligibility": true,
    "pre_release_started_target_observation_blocks": true,
    "remote_completion_is_latency_endpoint": true,
    "full_attempt_completion_is_not_latency_endpoint": true,
    "remote_completion_equal_next_slot_allowed": true,
    "remote_completion_after_next_slot_blocked": true,
    "previous_completion_equal_next_start_allowed": true,
    "overlap_blocked": true,
    "exact_bound_passes": true,
    "bound_plus_one_nanosecond_fails": true,
    "exact_grid_parity_with_synthetic_reference": true,
    "float_or_bool_timestamp_authority_rejected": true,
    "environment_or_cli_normative_authority_absent": true,
    "implementation_constants_match_governed_preregistration": true
  },
  "mutation_discrimination": {
    "checks": 4,
    "kills": 4,
    "survivors": 0,
    "families": [
      "exact latency-bound comparison operator",
      "actual-start next-slot comparison operator",
      "remote-completion next-slot comparison operator",
      "remote-completion versus full-attempt-completion latency endpoint"
    ]
  },
  "test_results": {
    "dedicated_surface": "22/22 PASS",
    "full_targeted_regression": "135/135 PASS",
    "p5e_contract_diff": 0,
    "p5e_synthetic_model_diff": 0,
    "p5d4_runtime_diff": 0
  },
  "host_clock_capability_non_normative": {
    "api": "time.monotonic_ns",
    "metadata_api": "time.get_clock_info('monotonic')",
    "monotonic": true,
    "adjustable": false,
    "resolution_seconds": 1e-7,
    "implementation": "QueryPerformanceCounter()",
    "sample_1_ns": 4845925967277900,
    "sample_2_ns": 4845925967278100,
    "same_process_host_domain": true,
    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
    "python_implementation": "CPython",
    "platform": "Windows-11-10.0.22631-SP0"
  },
  "real_p5d4_state_unchanged": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "claim_boundary": {
    "rpe02_qualified_for_external_review": true,
    "rpe02_human_adopted": false,
    "rpe03_status_untouched_by_this_branch": true,
    "rpe04_opened": false,
    "rpe05_opened": false,
    "rpe06_opened": false,
    "real_p5e_authorized": false,
    "network_used": false,
    "p5d4_real_state_mutated": false,
    "vault_or_current_mutated": false
  },
  "next_gate": "INDEPENDENT_EXTERNAL_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: RPE-02 QUALIFICATION REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE02-REAL-TIME-REPRESENTATION-QUALIFICATION.md
Authoritative Git blob: e2550e5629f5a505718e867b805be232f5fe345b
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — QUALIFICATION

Date: 2026-10-03

## Verdict

`RPE-02 = QUALIFIED_FOR_EXTERNAL_REVIEW`

Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.

## Canonical base

RPE-01 adoption commit:
`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`

RPE-01 adoption blob:
`49203ebc2fb208c5dd23ded140295ac00c0afab6`

The adopted P5-E contract, synthetic timing model and P5-D4 runtime remain byte-identical to the RPE-01 base.

## Preregistration and RED

Preregistration HEAD:
`c42a0f3df48807b3681db782f0a6fd58bd5c7aea`

Preregistration blob:
`614d3724c5c36bbdb6afbf9b49a31f88da465719`

Closed-schema blob:
`923671b1539585b5c32c8e2d284598b521fc0bba`

The preregistration validates through the adopted RPE-01 public entrypoint.

RED HEAD:
`03394a8a85680ca24a2593d14466c192fd208e8e`

Observed RED:
`17 tests / 15 failures / 2 passes`.

The failures were caused by the preregistered real-time module not yet existing.

## Final implementation

Implementation HEAD:
`c17d68b04de9dca13f9d9ed655e034b13436484d`

Module:
`db5dcfe8ad3b7ce93099368b459bb09ac25f933b`

Main tests:
`23618a9317c554099670e84482641a8014f8682d`

Mutation tests:
`77cdadb376320c4e8f591a3a80105feac250b716`

The implementation is a separate nanosecond-native real timing component. The adopted synthetic model is unchanged and is used only as semantic/exact-grid parity reference.

## Qualified timing semantics

Normative representation:
`INTEGER_MONOTONIC_NANOSECONDS`

Preregistered exact constants:
- poll interval = 30,000,000,000 ns;
- detection bound = 60,000,000,000 ns.

Required evidence fields include:
- schedule_origin_ns;
- scheduled_at_ns;
- attempt_started_at_ns;
- remote_observation_completed_at_ns;
- attempt_completed_at_ns;
- controlled_source_release_started_at_ns.

The qualified component distinguishes scheduled slot from actual attempt start. A scheduled-on-time attempt cannot hide an actual start at or after the next fixed-rate slot.

Detection eligibility uses actual attempt start. A target observation produced by an attempt started before controlled source release is blocked for adjudication.

Detection latency is:
`remote_observation_completed_at_ns - controlled_source_release_started_at_ns`.

Full attempt completion is retained for timeline/overlap validity but does not replace the remote-observation completion endpoint.

Equality boundaries are frozen:
- exactly 60 seconds = PASS;
- 60 seconds + 1 ns = FAIL;
- remote completion exactly at the next slot = allowed;
- remote completion after the next slot = blocked;
- previous attempt completion exactly at next attempt start = allowed;
- previous completion greater than next start = overlap blocked.

## Governed configuration provenance

RPE-02's preregistration and schema are governed RPE-01 artifacts.

A dedicated parity test proves the implementation constants equal the governed preregistration values.

No environment variable, CLI argument or unlisted file supplies normative timing authority.

## Mutation/discrimination

Four targeted mutants were killed:

1. exact latency bound `<=` changed to `<`;
2. actual-start next-slot `>=` changed to `>`;
3. remote-completion next-slot `>` changed to `>=`;
4. latency endpoint changed from remote completion to full attempt completion.

Result:
`4 / 4 KILLED`.

## Test result

Dedicated RPE-02 surface:
`22 / 22 PASS`

P5-E + RPE-01 + RPE-02 targeted regression:
`135 / 135 PASS`

Protected diffs:
```text
P5-E CONTRACT = 0
P5-E SYNTHETIC MODEL = 0
P5-D4 RUNTIME = 0
```

## Host monotonic-clock capability evidence

Observed on the qualification host:
- API: `time.monotonic_ns`;
- monotonic: true;
- adjustable: false;
- resolution: 1e-7 seconds;
- implementation: `QueryPerformanceCounter()`;
- samples were integer nanoseconds and non-decreasing;
- same-process host domain: true.

Environment:
`CPython 3.13.14 / Windows-11-10.0.22631-SP0`.

This host evidence is non-normative context; the verdict semantics remain integer-nanosecond based.

## Authority boundary

This qualification does not authorize:
- RPE-04/05/06;
- network observation;
- GitHub polling;
- P5-D4 real-state mutation;
- Vault/CURRENT mutation;
- REAL P5-E;
- human adoption of RPE-02.

Maximum claim:
`RPE02_REAL_TIME_REPRESENTATION = QUALIFIED_FOR_EXTERNAL_REVIEW`.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: ADOPTED P5-E CONTRACT
Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
Authoritative Git blob: 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9
Display copy is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: ADOPTED P5-E SYNTHETIC MODEL
Path: tools/obsidian_projection/p5e_near_real_time_model.py
Authoritative Git blob: c0f16baa151c1466e30ba5778f1fca8184cd4aac
Display copy is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: ADOPTED RPE-01 GUARD
Path: tools/obsidian_projection/rpe01_governed_closed_schema.py
Authoritative Git blob: 26f977961d72a062199d71ffd628d5a5cc047887
Display copy is normalized for packet formatting and is not claimed byte-identical.
~~~~
from __future__ import annotations

import json
import re
from typing import Any


SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
MAX_GOVERNED_JSON_DEPTH = 64
_ALLOWED_KINDS = {"object", "array", "string", "integer", "boolean", "null"}
_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")


class GovernedSchemaError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise GovernedSchemaError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise GovernedSchemaError(f"non-standard JSON numeric constant forbidden: {value}")


def _enforce_max_json_depth(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char in "[{":
            depth += 1
            if depth > MAX_GOVERNED_JSON_DEPTH:
                raise GovernedSchemaError(
                    "maximum governed JSON depth exceeded: "
                    f"{depth} > {MAX_GOVERNED_JSON_DEPTH}"
                )
        elif char in "]}":
            depth -= 1


def parse_json_strict(raw: str | bytes) -> Any:
    if isinstance(raw, bytes):
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise GovernedSchemaError(f"governed JSON must be valid UTF-8: {exc}") from exc
    elif isinstance(raw, str):
        text = raw
    else:
        raise GovernedSchemaError("raw governed JSON must be str or bytes")
    _enforce_max_json_depth(text)
    try:
        return json.loads(
            text,
            object_pairs_hook=_strict_object,
            parse_constant=_reject_constant,
        )
    except GovernedSchemaError:
        raise
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise GovernedSchemaError(
            f"invalid or unsupported governed JSON: {type(exc).__name__}: {exc}"
        ) from exc


def _exact_keys(label: str, value: object, allowed: set[str], required: set[str]) -> dict[str, Any]:
    if type(value) is not dict:
        raise GovernedSchemaError(f"{label} must be an object")
    actual = set(value)
    unknown = actual - allowed
    missing = required - actual
    if unknown or missing:
        raise GovernedSchemaError(
            f"{label} schema mismatch: missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    return value


def _strict_int(label: str, value: object, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise GovernedSchemaError(f"{label} must be an integer")
    if minimum is not None and value < minimum:
        raise GovernedSchemaError(f"{label} must be >= {minimum}")
    return value


def _strict_bool(label: str, value: object) -> bool:
    if type(value) is not bool:
        raise GovernedSchemaError(f"{label} must be a boolean")
    return value


def _strict_string(label: str, value: object, *, nonempty: bool = True) -> str:
    if type(value) is not str:
        raise GovernedSchemaError(f"{label} must be a string")
    if nonempty and not value:
        raise GovernedSchemaError(f"{label} must be non-empty")
    return value


def _unique_json_values(values: list[Any]) -> bool:
    encoded = [
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        for value in values
    ]
    return len(encoded) == len(set(encoded))


def _value_matches_kind(value: object, kind: str) -> bool:
    if kind == "object":
        return type(value) is dict
    if kind == "array":
        return type(value) is list
    if kind == "string":
        return type(value) is str
    if kind == "integer":
        return type(value) is int
    if kind == "boolean":
        return type(value) is bool
    if kind == "null":
        return value is None
    return False


def _validate_constraint_value(label: str, value: object, kind: str) -> None:
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{label} does not match node kind {kind}")


def _validate_schema_node(node: object, path: str) -> None:
    if type(node) is not dict:
        raise GovernedSchemaError(f"{path} schema node must be an object")
    kind = node.get("kind")
    if type(kind) is not str or kind not in _ALLOWED_KINDS:
        raise GovernedSchemaError(f"{path}.kind unsupported")

    if kind == "object":
        allowed = {"kind", "fields"}
        _exact_keys(path, node, allowed, allowed)
        fields = node["fields"]
        if type(fields) is not dict or not fields:
            raise GovernedSchemaError(f"{path}.fields must be a non-empty object")
        for name, child in fields.items():
            _strict_string(f"{path}.fields key", name)
            _validate_schema_node(child, f"{path}.fields.{name}")
        return

    if kind == "array":
        allowed = {
            "kind", "items", "min_items", "max_items", "unique",
            "ordered_const", "allowed_values",
        }
        _exact_keys(path, node, allowed, {"kind", "items"})
        _validate_schema_node(node["items"], f"{path}.items")
        item_kind = node["items"]["kind"]

        minimum = None
        maximum = None
        if "min_items" in node:
            minimum = _strict_int(f"{path}.min_items", node["min_items"], minimum=0)
        if "max_items" in node:
            maximum = _strict_int(f"{path}.max_items", node["max_items"], minimum=0)
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} min_items exceeds max_items")
        if "unique" in node:
            _strict_bool(f"{path}.unique", node["unique"])
        for constraint in ("ordered_const", "allowed_values"):
            if constraint not in node:
                continue
            values = node[constraint]
            if type(values) is not list:
                raise GovernedSchemaError(f"{path}.{constraint} must be an array")
            for index, value in enumerate(values):
                _validate_constraint_value(
                    f"{path}.{constraint}[{index}]",
                    value,
                    item_kind,
                )
            if not _unique_json_values(values):
                raise GovernedSchemaError(f"{path}.{constraint} must not contain duplicates")
        if "ordered_const" in node:
            ordered = node["ordered_const"]
            if minimum is not None and len(ordered) < minimum:
                raise GovernedSchemaError(f"{path}.ordered_const shorter than min_items")
            if maximum is not None and len(ordered) > maximum:
                raise GovernedSchemaError(f"{path}.ordered_const longer than max_items")
        return

    if kind == "string":
        allowed = {"kind", "const", "enum", "pattern"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        if "pattern" in node:
            pattern = _strict_string(f"{path}.pattern", node["pattern"])
            try:
                re.compile(pattern)
            except re.error as exc:
                raise GovernedSchemaError(f"{path}.pattern invalid: {exc}") from exc
        return

    if kind == "integer":
        allowed = {"kind", "const", "enum", "minimum", "maximum"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        if "enum" in node:
            enum = node["enum"]
            if type(enum) is not list or not enum:
                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
            for index, value in enumerate(enum):
                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
            if not _unique_json_values(enum):
                raise GovernedSchemaError(f"{path}.enum must be unique")
        minimum = None
        maximum = None
        if "minimum" in node:
            minimum = _strict_int(f"{path}.minimum", node["minimum"])
        if "maximum" in node:
            maximum = _strict_int(f"{path}.maximum", node["maximum"])
        if minimum is not None and maximum is not None and minimum > maximum:
            raise GovernedSchemaError(f"{path} minimum exceeds maximum")
        return

    if kind == "boolean":
        allowed = {"kind", "const"}
        _exact_keys(path, node, allowed, {"kind"})
        if "const" in node:
            _validate_constraint_value(f"{path}.const", node["const"], kind)
        return

    if kind == "null":
        _exact_keys(path, node, {"kind"}, {"kind"})
        return

    raise GovernedSchemaError(f"{path}.kind unsupported")


def _validate_schema_definition(schema: object) -> dict[str, Any]:
    top = _exact_keys(
        "schema",
        schema,
        {"schema", "artifact_role", "source_binding", "root"},
        {"schema", "artifact_role", "root"},
    )
    if top["schema"] != SCHEMA_ID:
        raise GovernedSchemaError("unsupported governed schema version")
    _strict_string("schema.artifact_role", top["artifact_role"])
    if "source_binding" in top:
        binding = _exact_keys(
            "schema.source_binding",
            top["source_binding"],
            {"path", "git_blob"},
            {"path", "git_blob"},
        )
        _strict_string("schema.source_binding.path", binding["path"])
        blob = _strict_string("schema.source_binding.git_blob", binding["git_blob"])
        if _SHA1_RE.fullmatch(blob) is None:
            raise GovernedSchemaError("schema.source_binding.git_blob must be lowercase 40-hex")
    _validate_schema_node(top["root"], "schema.root")
    return top


def validate_schema_definition(schema: object) -> dict[str, Any]:
    try:
        return _validate_schema_definition(schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed schema validation exceeded recursion safety boundary"
        ) from exc


def _validate_document_node(value: object, node: dict[str, Any], path: str) -> None:
    kind = node["kind"]
    if not _value_matches_kind(value, kind):
        raise GovernedSchemaError(f"{path} must be {kind}")

    if kind == "object":
        fields = node["fields"]
        actual = set(value)
        expected = set(fields)
        if actual != expected:
            raise GovernedSchemaError(
                f"{path} closed-schema mismatch: "
                f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
            )
        for key, child in fields.items():
            _validate_document_node(value[key], child, f"{path}.{key}")
        return

    if kind == "array":
        length = len(value)
        if "min_items" in node and length < node["min_items"]:
            raise GovernedSchemaError(f"{path} shorter than min_items")
        if "max_items" in node and length > node["max_items"]:
            raise GovernedSchemaError(f"{path} longer than max_items")
        if node.get("unique") is True and not _unique_json_values(value):
            raise GovernedSchemaError(f"{path} contains duplicate items")
        if "allowed_values" in node:
            allowed = node["allowed_values"]
            for item in value:
                if item not in allowed:
                    raise GovernedSchemaError(f"{path} contains item outside closed vocabulary")
        if "ordered_const" in node and value != node["ordered_const"]:
            raise GovernedSchemaError(f"{path} violates normative array order/content")
        for index, item in enumerate(value):
            _validate_document_node(item, node["items"], f"{path}[{index}]")
        return

    if "const" in node and value != node["const"]:
        raise GovernedSchemaError(f"{path} const mismatch")
    if "enum" in node and value not in node["enum"]:
        raise GovernedSchemaError(f"{path} outside closed enum")
    if kind == "string" and "pattern" in node:
        if re.fullmatch(node["pattern"], value) is None:
            raise GovernedSchemaError(f"{path} pattern mismatch")
    if kind == "integer":
        if "minimum" in node and value < node["minimum"]:
            raise GovernedSchemaError(f"{path} below minimum")
        if "maximum" in node and value > node["maximum"]:
            raise GovernedSchemaError(f"{path} above maximum")


def parse_schema_json_strict(raw: str | bytes) -> dict[str, Any]:
    schema = parse_json_strict(raw)
    return validate_schema_definition(schema)


def _validate_document(document: object, validated_schema: dict[str, Any]) -> Any:
    _validate_document_node(document, validated_schema["root"], "$")
    return document


def validate_governed_json(
    raw_document: str | bytes,
    raw_schema: str | bytes,
) -> Any:
    try:
        validated_schema = parse_schema_json_strict(raw_schema)
        document = parse_json_strict(raw_document)
        return _validate_document(document, validated_schema)
    except GovernedSchemaError:
        raise
    except RecursionError as exc:
        raise GovernedSchemaError(
            "governed document validation exceeded recursion safety boundary"
        ) from exc
~~~~
