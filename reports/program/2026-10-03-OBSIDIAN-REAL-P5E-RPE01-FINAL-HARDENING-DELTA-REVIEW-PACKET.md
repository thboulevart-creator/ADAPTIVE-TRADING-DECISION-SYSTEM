# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — FINAL DELTA REVIEW PACKET

Date: 2026-10-03

## Reviewer mandate

Review only the final RPE-01 hardening delta.

Previous external verdict:
PASS_WITH_NON_BLOCKING_NOTES

Previous blocking findings:
NONE

This final delta addresses only:
- NB-a — deterministic JSON depth / recursion normalization;
- NB-b — discriminating raw JSON breakers;
- NB-c — governed consumer usage rule.

The requested decision is whether RPE-01 is ready for HUMAN ADOPTION.

This review creates no authority.

RPE-02 = CLOSED
RPE-03 = CLOSED
REAL_P5E = CLOSED

## Exact lineage

Pre-final-hardening HEAD:
cbe8b2534e3a4f65edbe1732a5b322e018756713

Preregistration HEAD:
cee9f7e4c46a9cef28891561c63e112d81cc3744

Final-hardening RED HEAD:
6327333ba27b551ac7c1fcda20fafe3eb488749f

Final-hardening candidate HEAD:
2ffae9c99c30749c13205a7ee5a772600d2271b6

Preregistration blob:
3fbd871ac3faeaab8d40c730ac539677ac272c33

Final review-return summary blob:
d5ce7aa73a070610a2a56c04647c426cff7d1249

RED test blob:
449898e62f244a275af290559b7441af1798ee09

RED report blob:
33f6f1bea040bddcb452657319e87f90bca9ed54

Final guard blob:
26f977961d72a062199d71ffd628d5a5cc047887

P5-E governed schema blob, unchanged:
87e45cc75753439879e2902d3cbdbd5d71d8a1b2

Adopted P5-E contract blob, unchanged:
43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

Main RPE-01 test blob, unchanged:
cd0e091233e5a4473ef280c7061db8cf880169e9

Final mutation sweep blob:
b37ca3e31aecde1beccf08eafe04696e6a7dc4c9

Portable prior NB1/NB2 test blob:
f52b88a9d56ea12a515e35ad8e915d0a1bc28b91

Final hardening test blob:
449898e62f244a275af290559b7441af1798ee09

Final qualification JSON:
f514af4bf01a62b3f751e14cfffaaf20bfe66885

Final qualification report:
92e45cf8fa279c0b9643a9ad77d4c1f19d6a7cdf

## Preregistered deterministic rule

MAX_GOVERNED_JSON_DEPTH = 64

Definition:
maximum syntactic nesting of JSON containers outside JSON strings.
A root object or array has depth 1.

This value was committed before RED.

Observed protected-artifact depths:
- adopted P5-E contract = 3;
- P5-E governed schema = 8.

These observations are non-normative.

## RED

Before the patch:

Ran 14 tests.

FAILED:
- 2 failures;
- 4 errors;
- 8 passes.

RED demonstrated:
- no MAX_GOVERNED_JSON_DEPTH constant;
- depth-65 document accepted;
- depth-65 valid governed schema accepted;
- forced schema-validation RecursionError escaped;
- forced document-validation RecursionError escaped;
- no deterministic depth guard existed to kill the depth mutant.

## Final reproduced evidence

Final hardening:
14 / 14 PASS

Current RPE-01 surface:
42 / 42 PASS

Final P5-E + RPE-01 targeted regression:
109 / 109 PASS

Mutation evidence:
- parsed-object mutations = 433;
- raw JSON breakers = 7;
- raw survivors = 0;
- mutation-kill checks = 3;
- mutants killed = 3;
- mutation survivors = 0.

Protected diffs from adopted readiness base:
- P5-E contract = 0;
- P5-E synthetic model = 0;
- P5-D4 runtime = 0.

Qualification environment, evidence context only:
- CPython 3.13.14;
- Windows-11-10.0.22631-SP0.

The previous reviewer observed Python 3.12.3 on Linux. The final normative depth property no longer depends on interpreter recursion behavior.

## NB-a questions

1. Is the lexical depth rule deterministic and correctly applied before json.loads for both document and schema?
2. Is depth 64 permitted and depth 65 rejected independently of Python recursion limits?
3. Does the scanner correctly ignore container characters inside strings and respect backslash escapes?
4. Is a limit of 64 reasonable given current governed artifacts at depths 3 and 8?
5. Are residual RecursionError failures from schema validation normalized to GovernedSchemaError?
6. Are residual RecursionError failures from document validation normalized at the public boundary?
7. Is the previous interpreter-dependent 5000-level test correctly replaced by MAX+1?
8. Can you construct a valid input at or below depth 64 that still leaks RecursionError through an authorized public governed-validation path?

## NB-b questions

9. Are the seven raw breakers now constructed from otherwise-valid governed artifacts?
10. Does contradictory duplicate evaluation_authorized isolate duplicate-key protection?
11. Does escaped duplicate evaluation_authorized exercise decoded-key equality?
12. Does duplicate poll_interval_seconds isolate duplicate-key protection on a real numeric field?
13. Do NaN / Infinity / -Infinity probes now require the parser-specific non-standard-constant rejection reason?
14. Does duplicate artifact_role exercise duplicate-member rejection on an otherwise-valid raw governed schema?
15. Is checking the targeted rejection reason sufficient to make the constant breakers discriminating even though later type validation would remain fail-closed?
16. Do the three explicit mutants demonstrate distinct protection value:
    - duplicate-member detection removed;
    - parse_constant rejection removed;
    - deterministic depth guard removed?
17. Is any important raw breaker still non-discriminating in a way that changes the RPE-01 claim?

## NB-c questions

18. Is validate_governed_json(raw_document, raw_schema) an adequate sole authorized governed-artifact entrypoint?
19. Is it acceptable that validate_schema_definition remains callable as a utility provided later RPE consumers are forbidden to use it for governed document validation?
20. Does the repository evidence support that no current runtime tool consumes private guard functions?
21. Should NB-c be carried as an explicit consumer contract into RPE-02/RPE-03 preregistration rather than requiring more RPE-01 code?

## Regression and claims

22. Is 109/109 targeted regression sufficient for this final structural hardening?
23. Is a full Obsidian suite unnecessary given zero modifications to the adopted P5-E contract/model/P5-D4 runtime and no runtime guard consumer?
24. Are NB-3, NB-4 and NB-5 still correctly non-blocking scope notes?
25. Has any RPE-02/RPE-03/REAL-P5E authority leaked?
26. Is RPE-01 ready for human adoption if no new blocking finding is found?

## Required adversarial probes

Attempt at least:
- JSON containing many braces/brackets inside strings must not consume depth budget;
- strings with escaped quotes/backslashes adjacent to bracket characters;
- valid document depth 64 and depth 65;
- valid governed schema depth 64 and depth 65;
- forced RecursionError in schema validator;
- forced RecursionError in document validator;
- duplicate real evaluation_authorized;
- escaped duplicate real evaluation_authorized;
- duplicate real poll_interval_seconds;
- NaN/Infinity/-Infinity in the stated real numeric fields;
- duplicate artifact_role in otherwise-valid raw schema;
- duplicate-detection mutant;
- parse-constant mutant;
- depth-guard mutant;
- attempt to use a pre-parsed schema dict through validate_governed_json.

## Required output

Return exactly one:

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then provide:

- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- NB_A_DEPTH_PORTABILITY_CHECK
- NB_B_DISCRIMINATION_CHECK
- NB_C_USAGE_RULE_CHECK
- MUTATION_KILL_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RPE01_ADOPTION_READINESS
- RECOMMENDED_NEXT_ACTION

For each finding:
- distinguish OBSERVED from INFERENCE;
- identify exact packet function/test/path;
- state BLOCKING or NON_BLOCKING;
- provide a minimal falsification case when possible.

This review creates no authority.

RPE-02 = CLOSED
RPE-03 = CLOSED
REAL_P5E = CLOSED

---

# NORMALIZED DISPLAY OF EXACT GIT DIFF — RED HEAD TO FINAL HARDENING HEAD
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-HARDENING-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-HARDENING-QUALIFICATION.md
new file mode 100644
index 0000000..92e45cf
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-HARDENING-QUALIFICATION.md
@@ -0,0 +1,380 @@
+# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — QUALIFICATION
+
+Date: 2026-10-03
+
+## Result
+
+```text
+RPE01_FINAL_HARDENING
+= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW
+
+RPE01_HUMAN_ADOPTION
+= PENDING
+
+RPE-02
+= CLOSED
+
+RPE-03
+= CLOSED
+
+REAL_P5E
+= CLOSED
+```
+
+## Purpose
+
+This is the final technical hardening pass requested after the independent review returned:
+
+`PASS_WITH_NON_BLOCKING_NOTES`
+
+with no blocker.
+
+It closes only:
+- NB-a — deterministic depth / recursion portability;
+- NB-b — discriminating raw breakers;
+- NB-c — consumer usage rule clarification.
+
+No adopted P5-E contract, synthetic model or P5-D4 runtime was changed.
+
+## Preregistration
+
+Opening HEAD:
+`cbe8b2534e3a4f65edbe1732a5b322e018756713`
+
+Preregistration HEAD:
+`cee9f7e4c46a9cef28891561c63e112d81cc3744`
+
+Preregistration blob:
+`3fbd871ac3faeaab8d40c730ac539677ac272c33`
+
+The deterministic bound was frozen before RED:
+
+```text
+MAX_GOVERNED_JSON_DEPTH = 64
+```
+
+Definition:
+
+maximum syntactic nesting of JSON containers outside JSON strings, with the root object/array at depth 1.
+
+Current protected artifacts are far below the bound:
+
+```text
+P5-E adopted contract max depth = 3
+P5-E governed schema max depth = 8
+```
+
+These current-depth observations are non-normative.
+
+## RED
+
+RED HEAD:
+`6327333ba27b551ac7c1fcda20fafe3eb488749f`
+
+RED test:
+`449898e62f244a275af290559b7441af1798ee09`
+
+RED report:
+`33f6f1bea040bddcb452657319e87f90bca9ed54`
+
+Observed before patch:
+
+```text
+Ran 14 tests
+
+FAILED
+failures = 2
+errors = 4
+
+8 tests already passed
+6 tests produced the required RED signal
+```
+
+The RED did not use an interpreter recursion threshold as evidence.
+
+## NB-a closure
+
+Final guard:
+
+`26f977961d72a062199d71ffd628d5a5cc047887`
+
+The guard now pre-scans raw JSON before `json.loads`.
+
+It tracks container nesting while ignoring braces/brackets inside JSON strings and honoring backslash escapes.
+
+Policy:
+
+```text
+depth <= 64
+→ depth guard permits parsing
+
+depth > 64
+→ GovernedSchemaError
+```
+
+The same parser boundary is used for:
+- governed documents;
+- governed schemas.
+
+Portable exact-boundary tests demonstrate:
+
+```text
+document depth 64 → allowed by depth guard
+document depth 65 → GovernedSchemaError
+
+schema depth 64 → valid / accepted
+schema depth 65 → GovernedSchemaError
+```
+
+Residual recursion is also normalized:
+- `validate_schema_definition` converts residual `RecursionError`;
+- public `validate_governed_json` converts residual document-validation `RecursionError`.
+
+Dedicated tests force recursion failures inside:
+- `_validate_schema_node`;
+- `_validate_document_node`.
+
+Both emerge as `GovernedSchemaError`.
+
+Therefore the normative property no longer depends on whether a particular Python JSON decoder accepts 5000 nested containers.
+
+The old 5000-level test was replaced by:
+
+`MAX_GOVERNED_JSON_DEPTH + 1`.
+
+## Qualification environment
+
+The final local qualification ran under:
+
+```text
+Python
+= 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]
+
+Implementation
+= CPython
+
+Platform
+= Windows-11-10.0.22631-SP0
+```
+
+This environment is evidence context only.
+
+It is not part of the depth semantics.
+
+## NB-b closure — discriminating raw breakers
+
+The parsed-object sweep remains:
+
+```text
+433 attempted
+0 survivors
+```
+
+The seven raw breakers are now built from otherwise-valid governed artifacts and require the intended parser rejection reason.
+
+They are:
+
+1. contradictory duplicate `evaluation_authorized`;
+2. escaped duplicate spelling of `evaluation_authorized`;
+3. duplicate real numeric `poll_interval_seconds`;
+4. NaN injected into real `poll_interval_seconds`;
+5. Infinity injected into real `detection_latency_seconds_max`;
+6. -Infinity injected into real `detection_latency_seconds_max`;
+7. duplicate `artifact_role` in the otherwise-valid raw P5-E schema.
+
+Observed:
+
+```text
+RAW BREAKERS = 7
+SURVIVORS = 0
+```
+
+The breaker no longer passes merely because a dummy key such as `x` is structurally unknown.
+
+## Mutation-kill evidence
+
+Three targeted mutants were exercised:
+
+### Duplicate-member mutant
+
+Protection:
+`object_pairs_hook=_strict_object`
+
+Mutant:
+duplicate detection replaced by normal dictionary construction.
+
+Result:
+the contradictory real `evaluation_authorized` document becomes structurally accepted.
+
+`MUTANT = KILLED`
+
+### Non-standard-constant mutant
+
+Protection:
+`parse_constant=_reject_constant`
+
+Mutant:
+NaN is allowed through JSON parsing.
+
+Result:
+the later schema still fails closed on integer type, but the required parser-specific NaN rejection disappears.
+
+`MUTANT = KILLED`
+
+### Deterministic-depth mutant
+
+Protection:
+`_enforce_max_json_depth`
+
+Mutant:
+depth guard replaced by no-op.
+
+Result:
+depth-65 JSON parses.
+
+`MUTANT = KILLED`
+
+Summary:
+
+```text
+MUTATION-KILL CHECKS = 3
+KILLS = 3
+SURVIVORS = 0
+```
+
+## NB-c usage rule
+
+The governed consumer rule is:
+
+```text
+AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
+= validate_governed_json(raw_document, raw_schema)
+```
+
+For future RPE consumers:
+- underscore-prefixed guard functions are forbidden;
+- `validate_schema_definition` is not a governed-document validation entrypoint;
+- callers must not use it as a document-validation bypass.
+
+A repository search over `tools/`, excluding the guard module itself, found no runtime consumer of:
+- `validate_schema_definition`;
+- `_validate_document`;
+- `_validate_document_node`;
+- `_validate_schema_node`.
+
+RPE-02/RPE-03 remain unopened, so no future runtime consumer exists yet.
+
+## GREEN
+
+Final hardening tests:
+
+```text
+14 / 14 PASS
+```
+
+Current RPE-01 surface:
+
+```text
+42 / 42 PASS
+```
+
+Final evidence partition:
+
+```text
+PARSED-OBJECT MUTATIONS = 433
+RAW-JSON BREAKERS       = 7
+RAW SURVIVORS           = 0
+
+MUTATION-KILL CHECKS    = 3
+MUTATION KILLS          = 3
+MUTATION SURVIVORS      = 0
+```
+
+## Final targeted regression
+
+P5-E qualification surface + all RPE-01 tests:
+
+```text
+109 / 109 PASS
+```
+
+Protected artifact deltas from the adopted readiness base:
+
+```text
+P5-E CONTRACT = 0
+P5-E MODEL = 0
+P5-D4 RUNTIME = 0
+```
+
+## Remaining non-blocking scope
+
+Unchanged:
+
+- NB-3: RPE-01 is structural/type/list governance; adopted P5-E invariants retain value semantics.
+- NB-4: generic source binding is structurally represented but not dynamically enforced by the generic guard.
+- NB-5: contradictory restrictive constraints, ASCII-regex policy and isolated-surrogate handling remain future hardening where relevant.
+
+None of these is claimed closed by this final hardening.
+
+## Real-state integrity
+
+```text
+observer-events.jsonl
+= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af
+
+observer-checkpoint.json
+= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4
+
+last-run.json
+= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
+```
+
+## Final candidate identities
+
+```text
+GUARD
+= 26f977961d72a062199d71ffd628d5a5cc047887
+
+P5-E GOVERNED SCHEMA
+= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2
+
+MAIN RPE-01 TEST
+= cd0e091233e5a4473ef280c7061db8cf880169e9
+
+MUTATION SWEEP
+= b37ca3e31aecde1beccf08eafe04696e6a7dc4c9
+
+PORTABLE NB1/NB2 TEST
+= f52b88a9d56ea12a515e35ad8e915d0a1bc28b91
+
+FINAL HARDENING TEST
+= 449898e62f244a275af290559b7441af1798ee09
+```
+
+## Maximum claim
+
+```text
+NB-a
+= CLOSED_CANDIDATE
+
+NB-b
+= CLOSED_CANDIDATE
+
+NB-c
+= USAGE_RULE_DEFINED
+
+RPE01_FINAL_HARDENING
+= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW
+
+RPE01_HUMAN_ADOPTION
+= PENDING
+
+RPE-02
+= CLOSED
+
+RPE-03
+= CLOSED
+
+REAL_P5E
+= CLOSED
+```
diff --git a/tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py b/tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py
index 1691d7f..f52b88a 100644
--- a/tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py
+++ b/tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py
@@ -78,9 +78,12 @@ class NB2NormalizedExceptionTests(unittest.TestCase):

     def test_pathological_nesting_is_normalized(self):
         g = load_guard()
-        depth = 5000
+        depth = g.MAX_GOVERNED_JSON_DEPTH + 1
         pathological = ("[" * depth) + "0" + ("]" * depth)
-        with self.assertRaises(g.GovernedSchemaError):
+        with self.assertRaisesRegex(
+            g.GovernedSchemaError,
+            "maximum governed JSON depth",
+        ):
             g.parse_json_strict(pathological)


diff --git a/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
index a8bacea..b37ca3e 100644
--- a/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
+++ b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
@@ -79,7 +79,7 @@ def run_sweep():
             return
         survivors.append(label)

-    def expect_raw_reject(label, raw_document, raw_schema=None):
+    def expect_raw_reject(label, raw_document, expected_reason, raw_schema=None):
         nonlocal raw_json_attempted
         raw_json_attempted += 1
         try:
@@ -87,7 +87,10 @@ def run_sweep():
                 raw_document,
                 schema_raw if raw_schema is None else raw_schema,
             )
-        except guard.GovernedSchemaError:
+        except guard.GovernedSchemaError as exc:
+            if expected_reason in str(exc):
+                return
+            survivors.append(f"{label}:WRONG_REASON:{exc}")
             return
         survivors.append(label)

@@ -146,26 +149,163 @@ def run_sweep():
     target[0], target[1] = target[1], target[0]
     expect_reject("ORDER_CHANGE:real_end_to_end_stages", mutated)

-    # Raw JSON breaker families preregistered separately from parsed-object mutations.
-    expect_raw_reject("RAW_DUPLICATE_TOP_LEVEL", '{"x":1,"x":2}')
-    expect_raw_reject("RAW_DUPLICATE_NESTED", '{"outer":{"x":1,"x":2}}')
+    # Raw JSON breaker families constructed from otherwise-valid governed artifacts.
+    def replace_once(raw, old, replacement):
+        if raw.count(old) != 1:
+            raise AssertionError(f"expected one raw anchor: {old!r}")
+        return raw.replace(old, replacement, 1)
+
+    authority_anchor = '    "evaluation_authorized": false,'
+    duplicate_authority = replace_once(
+        raw_baseline,
+        authority_anchor,
+        authority_anchor + '\n    "evaluation_authorized": true,',
+    )
+    expect_raw_reject(
+        "RAW_REAL_AUTHORITY_DUPLICATE",
+        duplicate_authority,
+        "duplicate JSON member: evaluation_authorized",
+    )
+
+    escaped_duplicate_authority = replace_once(
+        raw_baseline,
+        authority_anchor,
+        authority_anchor + '\n    "\\u0065valuation_authorized": true,',
+    )
+    expect_raw_reject(
+        "RAW_REAL_AUTHORITY_ESCAPED_DUPLICATE",
+        escaped_duplicate_authority,
+        "duplicate JSON member: evaluation_authorized",
+    )
+
+    poll_anchor = '    "poll_interval_seconds": 30,'
+    duplicate_poll = replace_once(
+        raw_baseline,
+        poll_anchor,
+        poll_anchor + '\n    "poll_interval_seconds": 31,',
+    )
+    expect_raw_reject(
+        "RAW_REAL_NUMERIC_DUPLICATE",
+        duplicate_poll,
+        "duplicate JSON member: poll_interval_seconds",
+    )
+
     expect_raw_reject(
-        "RAW_ESCAPED_DUPLICATE",
-        '{"evaluation_authorized":true,"\u0065valuation_authorized":false}',
+        "RAW_REAL_NAN",
+        replace_once(
+            raw_baseline,
+            poll_anchor,
+            '    "poll_interval_seconds": NaN,',
+        ),
+        "non-standard JSON numeric constant forbidden: NaN",
     )
-    expect_raw_reject("RAW_NAN", '{"x":NaN}')
-    expect_raw_reject("RAW_POSITIVE_INFINITY", '{"x":Infinity}')
-    expect_raw_reject("RAW_NEGATIVE_INFINITY", '{"x":-Infinity}')
-    duplicate_schema = (
-        '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
-        '"artifact_role":"A","artifact_role":"B",'
-        '"root":{"kind":"null"}}'
+
+    latency_anchor = '    "detection_latency_seconds_max": 60,'
+    expect_raw_reject(
+        "RAW_REAL_POSITIVE_INFINITY",
+        replace_once(
+            raw_baseline,
+            latency_anchor,
+            '    "detection_latency_seconds_max": Infinity,',
+        ),
+        "non-standard JSON numeric constant forbidden: Infinity",
+    )
+    expect_raw_reject(
+        "RAW_REAL_NEGATIVE_INFINITY",
+        replace_once(
+            raw_baseline,
+            latency_anchor,
+            '    "detection_latency_seconds_max": -Infinity,',
+        ),
+        "non-standard JSON numeric constant forbidden: -Infinity",
     )
-    expect_raw_reject("RAW_SCHEMA_DUPLICATE_MEMBER", 'null', duplicate_schema)
+
+    schema_role_anchor = (
+        '  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",'
+    )
+    duplicate_schema = replace_once(
+        schema_raw,
+        schema_role_anchor,
+        schema_role_anchor + "\n" + schema_role_anchor,
+    )
+    expect_raw_reject(
+        "RAW_VALID_SCHEMA_DUPLICATE_MEMBER",
+        raw_baseline,
+        "duplicate JSON member: artifact_role",
+        duplicate_schema,
+    )
+
+    mutation_checks = 0
+    mutation_kills = 0
+    mutation_survivors = []
+
+    # Mutant 1: remove duplicate-member protection. The real authority duplicate
+    # becomes structurally valid because N4 intentionally does not freeze its bool value.
+    mutation_checks += 1
+    original_strict_object = guard._strict_object
+    guard._strict_object = dict
+    try:
+        try:
+            guard.validate_governed_json(duplicate_authority, schema_raw)
+        except guard.GovernedSchemaError as exc:
+            mutation_survivors.append(
+                f"DUPLICATE_DETECTION_MUTANT_SURVIVED:{exc}"
+            )
+        else:
+            mutation_kills += 1
+    finally:
+        guard._strict_object = original_strict_object
+
+    # Mutant 2: remove non-standard constant parser rejection. The document
+    # remains fail-closed later on type, but the parser-specific breaker is killed.
+    mutation_checks += 1
+    original_reject_constant = guard._reject_constant
+    guard._reject_constant = lambda value: float(value)
+    try:
+        try:
+            guard.validate_governed_json(
+                replace_once(
+                    raw_baseline,
+                    poll_anchor,
+                    '    "poll_interval_seconds": NaN,',
+                ),
+                schema_raw,
+            )
+        except guard.GovernedSchemaError as exc:
+            if "non-standard JSON numeric constant forbidden: NaN" not in str(exc):
+                mutation_kills += 1
+            else:
+                mutation_survivors.append(
+                    "NONSTANDARD_CONSTANT_MUTANT_SURVIVED"
+                )
+        else:
+            mutation_kills += 1
+    finally:
+        guard._reject_constant = original_reject_constant
+
+    # Mutant 3: remove deterministic depth protection. Depth 65 must then parse.
+    mutation_checks += 1
+    original_depth_guard = guard._enforce_max_json_depth
+    guard._enforce_max_json_depth = lambda text: None
+    try:
+        depth_65 = ("[" * 65) + "0" + ("]" * 65)
+        try:
+            guard.parse_json_strict(depth_65)
+        except guard.GovernedSchemaError as exc:
+            mutation_survivors.append(
+                f"DEPTH_GUARD_MUTANT_SURVIVED:{exc}"
+            )
+        else:
+            mutation_kills += 1
+    finally:
+        guard._enforce_max_json_depth = original_depth_guard

     return {
         "parsed_object_attempted": parsed_object_attempted,
         "raw_json_attempted": raw_json_attempted,
+        "mutation_kill_checks": mutation_checks,
+        "mutation_kills": mutation_kills,
+        "mutation_survivors": mutation_survivors,
         "attempted": parsed_object_attempted + raw_json_attempted,
         "survivors": survivors,
         "survivor_count": len(survivors),
@@ -179,6 +319,9 @@ class RPE01MutationSweepTests(unittest.TestCase):
         self.assertEqual(result["raw_json_attempted"], 7)
         self.assertEqual(result["attempted"], 440)
         self.assertEqual(result["survivors"], [])
+        self.assertEqual(result["mutation_kill_checks"], 3)
+        self.assertEqual(result["mutation_kills"], 3)
+        self.assertEqual(result["mutation_survivors"], [])


 if __name__ == "__main__":
diff --git a/tools/obsidian_projection/rpe01_final_hardening_qualification_v0_1.json b/tools/obsidian_projection/rpe01_final_hardening_qualification_v0_1.json
new file mode 100644
index 0000000..f514af4
--- /dev/null
+++ b/tools/obsidian_projection/rpe01_final_hardening_qualification_v0_1.json
@@ -0,0 +1,109 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_FINAL_HARDENING_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW",
+  "date": "2026-10-03",
+  "opening_head": "cbe8b2534e3a4f65edbe1732a5b322e018756713",
+  "preregistration_head": "cee9f7e4c46a9cef28891561c63e112d81cc3744",
+  "preregistration_blob": "3fbd871ac3faeaab8d40c730ac539677ac272c33",
+  "final_delta_review_return_blob": "d5ce7aa73a070610a2a56c04647c426cff7d1249",
+  "red_head": "6327333ba27b551ac7c1fcda20fafe3eb488749f",
+  "red_test_blob": "449898e62f244a275af290559b7441af1798ee09",
+  "red_report_blob": "33f6f1bea040bddcb452657319e87f90bca9ed54",
+  "final_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
+  "p5e_schema_blob_unchanged": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
+  "main_rpe01_test_blob_unchanged": "cd0e091233e5a4473ef280c7061db8cf880169e9",
+  "final_mutation_sweep_blob": "b37ca3e31aecde1beccf08eafe04696e6a7dc4c9",
+  "portable_nb1_nb2_test_blob": "f52b88a9d56ea12a515e35ad8e915d0a1bc28b91",
+  "final_hardening_test_blob": "449898e62f244a275af290559b7441af1798ee09",
+  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
+  "nb_a": {
+    "status": "CLOSED_CANDIDATE",
+    "max_governed_json_depth": 64,
+    "depth_definition": "Maximum syntactic nesting of JSON containers outside strings, root container depth 1.",
+    "document_boundary_64": "PASS",
+    "document_boundary_65": "REJECT_GOVERNED_SCHEMA_ERROR",
+    "schema_boundary_64": "PASS",
+    "schema_boundary_65": "REJECT_GOVERNED_SCHEMA_ERROR",
+    "interpreter_recursion_limit_normative": false,
+    "schema_validation_recursion_normalized": true,
+    "document_validation_recursion_normalized_at_public_boundary": true
+  },
+  "nb_b": {
+    "status": "CLOSED_CANDIDATE",
+    "parsed_object_mutations": 433,
+    "raw_json_breakers": 7,
+    "raw_json_breaker_survivors": 0,
+    "mutation_kill_checks": 3,
+    "mutation_kills": 3,
+    "mutation_survivors": 0,
+    "raw_breakers_are_built_from": [
+      "otherwise-valid adopted P5-E contract",
+      "otherwise-valid P5-E governed schema"
+    ],
+    "raw_breaker_families": [
+      "contradictory duplicate real authority key evaluation_authorized",
+      "escaped duplicate real authority key evaluation_authorized",
+      "duplicate real numeric key poll_interval_seconds",
+      "NaN in real numeric field poll_interval_seconds",
+      "Infinity in real numeric field detection_latency_seconds_max",
+      "-Infinity in real numeric field detection_latency_seconds_max",
+      "duplicate artifact_role in otherwise-valid raw governed schema"
+    ],
+    "raw_breakers_require_targeted_parser_reason": true
+  },
+  "nb_c": {
+    "status": "ADOPTED_USAGE_RULE_CANDIDATE",
+    "authorized_governed_artifact_validation_entrypoint": "validate_governed_json(raw_document, raw_schema)",
+    "underscore_prefixed_guard_functions_external_consumer_use_forbidden": true,
+    "validate_schema_definition_is_not_authorized_for_governed_document_validation": true,
+    "runtime_tools_external_private_guard_consumers_observed": 0
+  },
+  "test_results": {
+    "final_hardening_red": "14 tests; 2 failures + 4 errors before patch; 8 passes",
+    "final_hardening_green": "14/14 PASS",
+    "current_rpe01_surface": "42/42 PASS",
+    "final_targeted_regression": "109/109 PASS",
+    "final_sweep": {
+      "parsed_object_attempted": 433,
+      "raw_json_attempted": 7,
+      "attempted_total": 440,
+      "survivors": 0,
+      "mutation_kill_checks": 3,
+      "mutation_kills": 3,
+      "mutation_survivors": 0
+    },
+    "contract_diff_from_adopted_readiness_head": 0,
+    "model_diff_from_adopted_readiness_head": 0,
+    "p5d4_runtime_diff_from_adopted_readiness_head": 0
+  },
+  "qualification_environment_non_normative": {
+    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
+    "python_implementation": "CPython",
+    "platform": "Windows-11-10.0.22631-SP0"
+  },
+  "current_artifact_depth_observations_non_normative": {
+    "adopted_p5e_contract": 3,
+    "p5e_governed_schema": 8
+  },
+  "remaining_nonblocking_scope_notes": {
+    "nb3": "The P5-E schema remains structural/type/list governance; adopted P5-E invariants retain value semantics.",
+    "nb4": "Generic source_binding/artifact_role remain structurally validated but not dynamically bound by the generic guard.",
+    "nb5": "Contradictory restrictive schema constraints, ASCII regex semantics, and isolated-surrogate handling remain non-blocking future hardening."
+  },
+  "real_state_fingerprints_unchanged": {
+    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
+    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
+    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
+  },
+  "claim_boundary": {
+    "rpe01_final_hardening_qualified_for_external_delta_review": true,
+    "rpe01_human_adopted": false,
+    "rpe02_opened": false,
+    "rpe03_opened": false,
+    "real_p5e_authorized": false
+  },
+  "next_gate": "FINAL_SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION",
+  "stop": true
+}
diff --git a/tools/obsidian_projection/rpe01_governed_closed_schema.py b/tools/obsidian_projection/rpe01_governed_closed_schema.py
index 82f4323..26f9779 100644
--- a/tools/obsidian_projection/rpe01_governed_closed_schema.py
+++ b/tools/obsidian_projection/rpe01_governed_closed_schema.py
@@ -6,6 +6,7 @@ from typing import Any


 SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
+MAX_GOVERNED_JSON_DEPTH = 64
 _ALLOWED_KINDS = {"object", "array", "string", "integer", "boolean", "null"}
 _SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")

@@ -27,6 +28,35 @@ def _reject_constant(value: str) -> None:
     raise GovernedSchemaError(f"non-standard JSON numeric constant forbidden: {value}")


+def _enforce_max_json_depth(text: str) -> None:
+    depth = 0
+    in_string = False
+    escaped = False
+    for char in text:
+        if in_string:
+            if escaped:
+                escaped = False
+            elif char == "\\":
+                escaped = True
+            elif char == '"':
+                in_string = False
+            continue
+
+        if char == '"':
+            in_string = True
+            continue
+
+        if char in "[{":
+            depth += 1
+            if depth > MAX_GOVERNED_JSON_DEPTH:
+                raise GovernedSchemaError(
+                    "maximum governed JSON depth exceeded: "
+                    f"{depth} > {MAX_GOVERNED_JSON_DEPTH}"
+                )
+        elif char in "]}":
+            depth -= 1
+
+
 def parse_json_strict(raw: str | bytes) -> Any:
     if isinstance(raw, bytes):
         try:
@@ -37,6 +67,7 @@ def parse_json_strict(raw: str | bytes) -> Any:
         text = raw
     else:
         raise GovernedSchemaError("raw governed JSON must be str or bytes")
+    _enforce_max_json_depth(text)
     try:
         return json.loads(
             text,
@@ -232,7 +263,7 @@ def _validate_schema_node(node: object, path: str) -> None:
     raise GovernedSchemaError(f"{path}.kind unsupported")


-def validate_schema_definition(schema: object) -> dict[str, Any]:
+def _validate_schema_definition(schema: object) -> dict[str, Any]:
     top = _exact_keys(
         "schema",
         schema,
@@ -257,6 +288,17 @@ def validate_schema_definition(schema: object) -> dict[str, Any]:
     return top


+def validate_schema_definition(schema: object) -> dict[str, Any]:
+    try:
+        return _validate_schema_definition(schema)
+    except GovernedSchemaError:
+        raise
+    except RecursionError as exc:
+        raise GovernedSchemaError(
+            "governed schema validation exceeded recursion safety boundary"
+        ) from exc
+
+
 def _validate_document_node(value: object, node: dict[str, Any], path: str) -> None:
     kind = node["kind"]
     if not _value_matches_kind(value, kind):
@@ -322,6 +364,13 @@ def validate_governed_json(
     raw_document: str | bytes,
     raw_schema: str | bytes,
 ) -> Any:
-    validated_schema = parse_schema_json_strict(raw_schema)
-    document = parse_json_strict(raw_document)
-    return _validate_document(document, validated_schema)
+    try:
+        validated_schema = parse_schema_json_strict(raw_schema)
+        document = parse_json_strict(raw_document)
+        return _validate_document(document, validated_schema)
+    except GovernedSchemaError:
+        raise
+    except RecursionError as exc:
+        raise GovernedSchemaError(
+            "governed document validation exceeded recursion safety boundary"
+        ) from exc
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL REVIEW RETURN SUMMARY
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-DELTA-REVIEW-CLAUDE-RETURN.md
Authoritative Git blob: d5ce7aa73a070610a2a56c04647c426cff7d1249
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-01 — FINAL DELTA REVIEW — CLAUDE RETURN

Date persisted: 2026-10-03

## Verdict

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

The reviewer reconstructed the packet copies and reported that the announced code, JSON, test, qualification, RED, and adjudication identities matched, except that the display copy of the persisted external review differed in bytes consistently with the packet's declared normalization.

The reviewer executed the candidate under Python 3.12.3 on Linux and observed:
- 94/95 tests passing;
- the only failure was `test_pathological_nesting_is_normalized`;
- the mutation sweep reproduced 433 parsed-object mutations + 7 raw breakers = 440 attempts, 0 survivors.

## NB-a — deterministic depth / recursion normalization

Status from reviewer:
`NON_BLOCKING`

Observed:
- `parse_json_strict` normalizes parser recursion only if the interpreter/parser itself raises there;
- recursive schema/document validation is not explicitly depth-bounded;
- a sufficiently deeply nested schema can reach `_validate_schema_node` and raise an unnormalized `RecursionError`;
- the existing 5000-level array test is interpreter-dependent: Python 3.12.3 on the reviewer environment parsed the input rather than raising during JSON parsing.

Reviewer correction recommendation:
- define an explicit deterministic maximum governed JSON depth for both documents and schemas;
- test exact boundary and boundary+1 rather than interpreter recursion limits;
- normalize residual validation `RecursionError` to `GovernedSchemaError`;
- record Python version/context in qualification.

## NB-b — raw breakers not all discriminating

Status from reviewer:
`NON_BLOCKING`

Observed:
- the count 433 + 7 = 440 is arithmetically correct;
- some raw probes such as `{"x":NaN}` are rejected by the concrete P5-E schema even if `parse_constant=_reject_constant` is removed, because `x` is itself an unknown key;
- therefore those raw probes do not independently demonstrate the parser protection.

Reviewer correction recommendation:
- construct raw breakers from the otherwise-valid adopted P5-E contract;
- duplicate a real normative key such as `evaluation_authorized`;
- inject NaN/Infinity into real numeric fields;
- use targeted mutation checks to demonstrate that removing the intended protection changes the targeted breaker outcome.

## NB-c — usage rule

Status from reviewer:
`ACCEPTABLE NON_BLOCKING NOTE`

`validate_schema_definition` remains public on a dictionary, but it does not provide a public document-validation bypass.

Adopted usage rule for subsequent RPE stages:
- `validate_governed_json(raw_document, raw_schema)` is the only authorized governed-artifact validation entrypoint;
- underscore-prefixed functions are forbidden to external consumers;
- `validate_schema_definition` must not be used as a bypass for governed document validation.

## Scope / authority

The reviewer found:
- NB-1 closed;
- NB-2 partially closed because of NB-a;
- NB-3/NB-4 correctly bounded;
- NB-5 non-blocking;
- no RPE-02 or REAL P5-E authority leakage.

Reviewer recommended one final technical pass for NB-a + NB-b before RPE-02 consumes the guard, followed by a short delta review.

This persisted review creates no authority.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL HARDENING PREREGISTRATION
Path: tools/obsidian_projection/rpe01_final_portability_raw_breaker_hardening_preregistration_v0_1.json
Authoritative Git blob: 3fbd871ac3faeaab8d40c730ac539677ac272c33
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_FINAL_PORTABILITY_RAW_BREAKER_HARDENING_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "date": "2026-10-03",
  "opening_head": "cbe8b2534e3a4f65edbe1732a5b322e018756713",
  "stage": "RPE-01",
  "scope": [
    "NB-a deterministic depth and residual recursion normalization",
    "NB-b discriminating raw-JSON breaker families",
    "NB-c governed consumer usage rule"
  ],
  "authority": {
    "rpe01_hardening_implementation_authorized": true,
    "p5e_contract_mutation_authorized": false,
    "p5e_model_mutation_authorized": false,
    "p5d4_runtime_mutation_authorized": false,
    "rpe02_authorized": false,
    "rpe03_authorized": false,
    "real_remote_io_authorized": false,
    "real_p5e_authorized": false
  },
  "deterministic_depth_contract": {
    "constant_name": "MAX_GOVERNED_JSON_DEPTH",
    "value": 64,
    "definition": "Maximum syntactic nesting of JSON containers outside strings. A root object or array has depth 1.",
    "application": [
      "raw governed document before json.loads",
      "raw governed schema before json.loads"
    ],
    "exact_boundary_policy": {
      "depth_64": "ALLOWED_BY_DEPTH_GUARD_SUBJECT_TO_NORMAL_JSON_AND_SCHEMA_VALIDATION",
      "depth_65": "REJECT_GOVERNED_SCHEMA_ERROR"
    },
    "current_artifact_observations_non_normative": {
      "adopted_p5e_contract_max_json_container_depth": 3,
      "p5e_governed_schema_max_json_container_depth": 8
    },
    "interpreter_recursion_limit_is_not_normative": true,
    "residual_recursion_policy": "Any RecursionError escaping schema/document validation through the public governed validation boundary is normalized to GovernedSchemaError."
  },
  "portable_red_families": [
    "DOCUMENT_DEPTH_64_ACCEPTED_BY_DEPTH_GUARD",
    "DOCUMENT_DEPTH_65_REJECTED_BY_DEPTH_GUARD",
    "SCHEMA_DEPTH_64_ACCEPTED_BY_DEPTH_GUARD",
    "SCHEMA_DEPTH_65_REJECTED_BY_DEPTH_GUARD",
    "VALIDATION_RECURSION_NORMALIZED_IF_FORCED"
  ],
  "discriminating_raw_breakers": {
    "source": "otherwise-valid adopted P5-E contract and otherwise-valid governed schema",
    "families": [
      "duplicate real authority key evaluation_authorized with contradictory values",
      "escaped duplicate spelling of real authority key evaluation_authorized",
      "NaN in real numeric field poll_interval_seconds",
      "Infinity in real numeric field target_max_detection_latency_seconds",
      "-Infinity in real numeric field target_max_detection_latency_seconds",
      "duplicate raw schema member on an otherwise-valid schema"
    ],
    "proof_requirement": "Each breaker must assert the intended strict-parser rejection reason, and targeted mutant checks must demonstrate that removing the relevant parser protection changes that targeted outcome."
  },
  "mutation_kill_requirements": [
    "duplicate-member-protection mutant is killed by a real-contract duplicate-key breaker",
    "non-standard-numeric-constant-protection mutant is killed by real-contract NaN/Infinity breakers",
    "depth-guard mutant is killed by depth_65 breaker"
  ],
  "nb_c_usage_rule": {
    "authorized_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "underscore_prefixed_functions_external_use_forbidden": true,
    "validate_schema_definition_is_not_an_authorized_governed_document_validation_entrypoint": true
  },
  "qualification_environment_context_required": [
    "python_version",
    "python_implementation",
    "platform"
  ],
  "evidence_partition_required": [
    "parsed_object_mutations",
    "raw_json_breakers",
    "mutation_kill_checks"
  ],
  "stop": "FINAL_EXTERNAL_DELTA_REVIEW_PACKET_THEN_HUMAN_ADOPTION_GATE"
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL HARDENING RED TEST
Path: tests/obsidian_projection/test_rpe01_final_portability_raw_breaker_hardening_v0_1.py
Authoritative Git blob: 449898e62f244a275af290559b7441af1798ee09
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_final_hardening", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_raw():
    return CONTRACT_PATH.read_text(encoding="utf-8")


def schema_raw():
    return SCHEMA_PATH.read_text(encoding="utf-8")


def replace_once(raw: str, old: str, new: str) -> str:
    if raw.count(old) != 1:
        raise AssertionError(f"expected exactly one raw anchor: {old!r}")
    return raw.replace(old, new, 1)


def duplicate_real_authority_raw(*, escaped: bool = False) -> str:
    raw = contract_raw()
    anchor = '    "evaluation_authorized": false,'
    if escaped:
        duplicate = '    "\\u0065valuation_authorized": true,'
    else:
        duplicate = '    "evaluation_authorized": true,'
    return replace_once(raw, anchor, anchor + "\n" + duplicate)


def nonstandard_numeric_real_contract(token: str, field: str, original: int) -> str:
    raw = contract_raw()
    anchor = f'    "{field}": {original},'
    replacement = f'    "{field}": {token},'
    return replace_once(raw, anchor, replacement)


def duplicate_valid_schema_member_raw() -> str:
    raw = schema_raw()
    anchor = '  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",'
    return replace_once(raw, anchor, anchor + "\n" + anchor)


def nested_array_raw(depth: int) -> str:
    return ("[" * depth) + "0" + ("]" * depth)


def nested_array_schema_raw(array_levels: int) -> str:
    node = {"kind": "null"}
    for _ in range(array_levels):
        node = {"kind": "array", "items": node}
    return json.dumps(
        {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_DEPTH_BOUNDARY",
            "root": node,
        },
        separators=(",", ":"),
    )


def syntactic_container_depth(raw: str) -> int:
    depth = 0
    maximum = 0
    in_string = False
    escaped = False
    for char in raw:
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
        elif char in "[{":
            depth += 1
            maximum = max(maximum, depth)
        elif char in "]}":
            depth -= 1
    if depth != 0:
        raise AssertionError("test fixture is not container-balanced")
    return maximum


def rejection_message(guard, raw_document: str, raw_schema: str | None = None):
    try:
        if raw_schema is None:
            guard.parse_json_strict(raw_document)
        else:
            guard.validate_governed_json(raw_document, raw_schema)
    except guard.GovernedSchemaError as exc:
        return str(exc)
    return None


class NBA_DeterministicDepthTests(unittest.TestCase):
    def test_preregistered_depth_constant_exists_and_is_exact(self):
        g = load_guard()
        self.assertEqual(g.MAX_GOVERNED_JSON_DEPTH, 64)

    def test_document_depth_64_allowed_and_65_rejected_by_depth_guard(self):
        g = load_guard()
        at_limit = nested_array_raw(64)
        above_limit = nested_array_raw(65)
        self.assertEqual(syntactic_container_depth(at_limit), 64)
        self.assertEqual(syntactic_container_depth(above_limit), 65)
        g.parse_json_strict(at_limit)
        with self.assertRaisesRegex(
            g.GovernedSchemaError,
            "maximum governed JSON depth",
        ):
            g.parse_json_strict(above_limit)

    def test_schema_depth_64_allowed_and_65_rejected_by_depth_guard(self):
        g = load_guard()
        at_limit = nested_array_schema_raw(62)
        above_limit = nested_array_schema_raw(63)
        self.assertEqual(syntactic_container_depth(at_limit), 64)
        self.assertEqual(syntactic_container_depth(above_limit), 65)
        g.parse_schema_json_strict(at_limit)
        with self.assertRaisesRegex(
            g.GovernedSchemaError,
            "maximum governed JSON depth",
        ):
            g.parse_schema_json_strict(above_limit)

    def test_validate_schema_definition_normalizes_residual_recursion(self):
        g = load_guard()
        schema = {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_FORCED_RECURSION",
            "root": {"kind": "null"},
        }
        original = g._validate_schema_node

        def forced(*args, **kwargs):
            raise RecursionError("forced schema recursion")

        g._validate_schema_node = forced
        try:
            with self.assertRaises(g.GovernedSchemaError):
                g.validate_schema_definition(schema)
        finally:
            g._validate_schema_node = original

    def test_public_document_validation_normalizes_residual_recursion(self):
        g = load_guard()
        raw_schema = json.dumps(
            {
                "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
                "artifact_role": "RPE01_FORCED_RECURSION",
                "root": {"kind": "null"},
            },
            separators=(",", ":"),
        )
        original = g._validate_document_node

        def forced(*args, **kwargs):
            raise RecursionError("forced document recursion")

        g._validate_document_node = forced
        try:
            with self.assertRaises(g.GovernedSchemaError):
                g.validate_governed_json("null", raw_schema)
        finally:
            g._validate_document_node = original


class NBB_DiscriminatingRawBreakerTests(unittest.TestCase):
    def assert_parser_reason(self, raw_document, expected, raw_schema=None):
        g = load_guard()
        message = rejection_message(
            g,
            raw_document,
            schema_raw() if raw_schema is None else raw_schema,
        )
        self.assertIsNotNone(message)
        self.assertIn(expected, message)

    def test_real_authority_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            duplicate_real_authority_raw(),
            "duplicate JSON member: evaluation_authorized",
        )

    def test_real_authority_escaped_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            duplicate_real_authority_raw(escaped=True),
            "duplicate JSON member: evaluation_authorized",
        )

    def test_real_numeric_nan_is_rejected_by_nonstandard_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "NaN",
                "poll_interval_seconds",
                30,
            ),
            "non-standard JSON numeric constant forbidden: NaN",
        )

    def test_real_numeric_positive_infinity_is_rejected_by_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "Infinity",
                "detection_latency_seconds_max",
                60,
            ),
            "non-standard JSON numeric constant forbidden: Infinity",
        )

    def test_real_numeric_negative_infinity_is_rejected_by_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "-Infinity",
                "detection_latency_seconds_max",
                60,
            ),
            "non-standard JSON numeric constant forbidden: -Infinity",
        )

    def test_otherwise_valid_raw_schema_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            contract_raw(),
            "duplicate JSON member: artifact_role",
            duplicate_valid_schema_member_raw(),
        )


class TargetedMutationKillTests(unittest.TestCase):
    def test_duplicate_member_breaker_kills_duplicate_detection_mutant(self):
        g = load_guard()
        raw = duplicate_real_authority_raw()
        baseline = rejection_message(g, raw, schema_raw())
        self.assertIn("duplicate JSON member: evaluation_authorized", baseline)

        original = g._strict_object
        g._strict_object = dict
        try:
            mutant_message = rejection_message(g, raw, schema_raw())
        finally:
            g._strict_object = original

        self.assertIsNone(
            mutant_message,
            "without duplicate detection this structural breaker must survive",
        )

    def test_constant_breaker_kills_parse_constant_mutant(self):
        g = load_guard()
        raw = nonstandard_numeric_real_contract(
            "NaN",
            "poll_interval_seconds",
            30,
        )
        expected = "non-standard JSON numeric constant forbidden: NaN"
        baseline = rejection_message(g, raw, schema_raw())
        self.assertIn(expected, baseline)

        original = g._reject_constant
        g._reject_constant = lambda value: float(value)
        try:
            mutant_message = rejection_message(g, raw, schema_raw())
        finally:
            g._reject_constant = original

        self.assertIsNotNone(mutant_message)
        self.assertNotIn(
            expected,
            mutant_message,
            "removing parse_constant protection must kill the parser-specific breaker",
        )

    def test_depth_65_breaker_kills_depth_guard_mutant(self):
        g = load_guard()
        raw = nested_array_raw(65)
        baseline = rejection_message(g, raw)
        self.assertIn("maximum governed JSON depth", baseline)

        original = g._enforce_max_json_depth
        g._enforce_max_json_depth = lambda text: None
        try:
            mutant_message = rejection_message(g, raw)
        finally:
            g._enforce_max_json_depth = original

        self.assertIsNone(
            mutant_message,
            "without the deterministic depth guard depth 65 must survive parsing",
        )


if __name__ == "__main__":
    unittest.main()
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL HARDENING RED REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-HARDENING-RED.md
Authoritative Git blob: 33f6f1bea040bddcb452657319e87f90bca9ed54
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — RED EVIDENCE

Date: 2026-10-03

## Preregistered predecessor

HEAD:
`cee9f7e4c46a9cef28891561c63e112d81cc3744`

Preregistration blob:
`3fbd871ac3faeaab8d40c730ac539677ac272c33`

Final delta-review return blob:
`d5ce7aa73a070610a2a56c04647c426cff7d1249`

Normative depth bound preregistered before RED:

`MAX_GOVERNED_JSON_DEPTH = 64`

Definition:
maximum syntactic nesting of JSON containers outside strings, with a root object or array at depth 1.

## RED test

`tests/obsidian_projection/test_rpe01_final_portability_raw_breaker_hardening_v0_1.py`

Written before any guard modification.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_final_portability_raw_breaker_hardening_v0_1
```

## Observed result

```text
Ran 14 tests in 0.064s

FAILED
failures = 2
errors = 4

FINAL_HARDENING_RED_EXIT = 1
```

Eight tests passed and six produced the required RED signal.

## NB-a RED signals

Observed before patch:

1. `MAX_GOVERNED_JSON_DEPTH` does not exist.
2. Document JSON at syntactic depth 65 is accepted by `parse_json_strict`.
3. Valid governed schema JSON at syntactic depth 65 is accepted by `parse_schema_json_strict`.
4. Forced `RecursionError` from `_validate_schema_node` escapes `validate_schema_definition`.
5. Forced `RecursionError` from `_validate_document_node` escapes the public `validate_governed_json` boundary.
6. The depth-65 breaker cannot kill a depth-guard mutant because no deterministic depth guard exists yet.

The exact boundary fixtures self-check:
- document depth 64;
- document depth 65;
- schema depth 64;
- schema depth 65.

No interpreter recursion threshold is used as normative evidence.

## NB-b baseline signals

The following real-contract/raw-schema breakers already reject for the intended strict-parser reason:

- contradictory duplicate real key `evaluation_authorized`;
- escaped duplicate of `evaluation_authorized`;
- `NaN` at real field `poll_interval_seconds`;
- `Infinity` at real field `detection_latency_seconds_max`;
- `-Infinity` at real field `detection_latency_seconds_max`;
- duplicate `artifact_role` in the otherwise-valid governed schema.

Targeted mutant checks already demonstrate:
- disabling duplicate-member detection allows the real-contract duplicate authority breaker to survive;
- disabling the non-standard constant parser hook removes the parser-specific NaN rejection signal.

These passing RED-baseline tests are expected; NB-b hardening focuses on incorporating these discriminating families into the final sweep/evidence partition.

## Authority boundary

No adopted contract/model/runtime was modified during RED.

`RPE-02 = CLOSED`

`RPE-03 = CLOSED`

`REAL_P5E = CLOSED`
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL GUARD
Path: tools/obsidian_projection/rpe01_governed_closed_schema.py
Authoritative Git blob: 26f977961d72a062199d71ffd628d5a5cc047887
Display copy below is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: ADOPTED P5-E CONTRACT
Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
Authoritative Git blob: 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9
Display copy below is normalized for packet formatting and is not claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: UNCHANGED P5-E GOVERNED SCHEMA
Path: tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json
Authoritative Git blob: 87e45cc75753439879e2902d3cbdbd5d71d8a1b2
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",
  "source_binding": {
    "path": "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
    "git_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
  },
  "root": {
    "kind": "object",
    "fields": {
      "schema": {
        "kind": "string"
      },
      "status": {
        "kind": "string"
      },
      "qualification_stage": {
        "kind": "string"
      },
      "real_p5e_execution_authorized": {
        "kind": "boolean"
      },
      "source_repository": {
        "kind": "string"
      },
      "monitored_source": {
        "kind": "object",
        "fields": {
          "remote": {
            "kind": "string"
          },
          "branch": {
            "kind": "string"
          },
          "canonical_authority": {
            "kind": "string"
          },
          "local_working_tree_is_not_authority": {
            "kind": "boolean"
          }
        }
      },
      "predecessors": {
        "kind": "object",
        "fields": {
          "p5a_continuous_projection_contract_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5a_qualification_report_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d1_observer_contract_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d1_static_review_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d2_one_shot_contract_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d2_static_review_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d4_loop_contract_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d4_runtime_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d4_real_v0_2_qualification_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "p5d4_human_adjudication_blob": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          }
        }
      },
      "objective": {
        "kind": "object",
        "fields": {
          "name": {
            "kind": "string"
          },
          "purpose": {
            "kind": "string"
          },
          "this_stage_is_not_real_end_to_end_execution": {
            "kind": "boolean"
          },
          "this_stage_may_not_claim_continuous_synchronization": {
            "kind": "boolean"
          }
        }
      },
      "near_real_time_timing": {
        "kind": "object",
        "fields": {
          "delivery_semantics": {
            "kind": "string"
          },
          "poll_interval_seconds": {
            "kind": "integer"
          },
          "detection_latency_seconds_max": {
            "kind": "integer"
          },
          "instantaneous_realtime_claim_forbidden": {
            "kind": "boolean"
          },
          "silent_interval_widening_forbidden": {
            "kind": "boolean"
          },
          "silent_latency_bound_widening_forbidden": {
            "kind": "boolean"
          },
          "detection_latency_definition": {
            "kind": "string"
          },
          "future_real_bound_clock": {
            "kind": "string"
          },
          "future_real_wall_clock_may_be_recorded_as_evidence_only": {
            "kind": "boolean"
          },
          "future_real_poll_schedule_semantics": {
            "kind": "string"
          },
          "single_transient_read_failure_may_still_meet_60_second_bound": {
            "kind": "boolean"
          },
          "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": {
            "kind": "boolean"
          },
          "real_measurement_origin": {
            "kind": "string"
          },
          "measurement_endpoint": {
            "kind": "string"
          },
          "schedule_semantics": {
            "kind": "string"
          },
          "remote_head_available_time_is_measurable_origin": {
            "kind": "boolean"
          },
          "real_latency_metric": {
            "kind": "string"
          },
          "attempt_start_and_read_completion_are_distinct": {
            "kind": "boolean"
          },
          "read_duration_is_included_in_detection_latency": {
            "kind": "boolean"
          },
          "eligible_detection_attempt_must_start_at_or_after_release": {
            "kind": "boolean"
          },
          "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": {
            "kind": "boolean"
          }
        }
      },
      "synthetic_timing_model": {
        "kind": "object",
        "fields": {
          "required": {
            "kind": "boolean"
          },
          "clock_source": {
            "kind": "string"
          },
          "sleep_forbidden": {
            "kind": "boolean"
          },
          "network_forbidden": {
            "kind": "boolean"
          },
          "filesystem_state_forbidden": {
            "kind": "boolean"
          },
          "process_launch_forbidden": {
            "kind": "boolean"
          },
          "environment_read_forbidden": {
            "kind": "boolean"
          },
          "real_p5d4_control_state_access_forbidden": {
            "kind": "boolean"
          },
          "real_vault_access_forbidden": {
            "kind": "boolean"
          },
          "purpose": {
            "kind": "string"
          },
          "schedule_semantics": {
            "kind": "string"
          },
          "schedule_origin_seconds": {
            "kind": "integer"
          },
          "observation_record_fields": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "allowed_values": [
              "scheduled_at_seconds",
              "completed_at_seconds",
              "outcome",
              "observed_head"
            ]
          },
          "head_identity_required_on_successful_remote_observation": {
            "kind": "boolean"
          },
          "skipped_required_attempt_result": {
            "kind": "string"
          },
          "cadence_gap_result": {
            "kind": "string"
          },
          "pre_source_target_observation_result": {
            "kind": "string"
          },
          "explicit_non_pass_statuses": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 1,
            "max_items": 1,
            "unique": true,
            "allowed_values": [
              "INCOMPLETE_SYNTHETIC_WINDOW"
            ]
          },
          "attempt_overruns_next_required_slot_result": {
            "kind": "string"
          },
          "attempt_overruns_next_required_slot_failure_code": {
            "kind": "string"
          },
          "duplicate_fixed_rate_slot_result": {
            "kind": "string"
          },
          "duplicate_fixed_rate_slot_failure_code": {
            "kind": "string"
          },
          "read_completion_before_attempt_start_forbidden": {
            "kind": "boolean"
          }
        }
      },
      "authority_boundary": {
        "kind": "object",
        "fields": {
          "observer_may_create_governance_authority": {
            "kind": "boolean"
          },
          "pending_head_evaluation_authorized": {
            "kind": "boolean"
          },
          "evaluation_authorized": {
            "kind": "boolean"
          },
          "stage_a_authorized": {
            "kind": "boolean"
          },
          "stage_b_authorized": {
            "kind": "boolean"
          },
          "promotion_authorized": {
            "kind": "boolean"
          },
          "publication_authorized": {
            "kind": "boolean"
          },
          "real_vault_mutation_authorized": {
            "kind": "boolean"
          },
          "current_mutation_authorized": {
            "kind": "boolean"
          },
          "current_tmp_mutation_authorized": {
            "kind": "boolean"
          },
          "real_polling_loop_authorized": {
            "kind": "boolean"
          },
          "daemon_authorized": {
            "kind": "boolean"
          },
          "startup_registration_authorized": {
            "kind": "boolean"
          },
          "scheduled_task_authorized": {
            "kind": "boolean"
          },
          "windows_service_authorized": {
            "kind": "boolean"
          },
          "p6_authorized": {
            "kind": "boolean"
          }
        }
      },
      "head_transition_policy": {
        "kind": "object",
        "fields": {
          "same_head_result": {
            "kind": "string"
          },
          "same_head_queue_growth_forbidden": {
            "kind": "boolean"
          },
          "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": {
            "kind": "boolean"
          },
          "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": {
            "kind": "boolean"
          },
          "non_fast_forward_result": {
            "kind": "string"
          },
          "unknown_ancestry_result": {
            "kind": "string"
          },
          "non_fast_forward_auto_continue_forbidden": {
            "kind": "boolean"
          },
          "unknown_ancestry_auto_continue_forbidden": {
            "kind": "boolean"
          },
          "active_or_pending_candidate_retarget_forbidden": {
            "kind": "boolean"
          }
        }
      },
      "queue_and_supersession": {
        "kind": "object",
        "fields": {
          "precedence_rule": {
            "kind": "string"
          },
          "p5a_supersession_intent_preserved_as_future_design_debt": {
            "kind": "boolean"
          },
          "fifo_required": {
            "kind": "boolean"
          },
          "unique_heads_required": {
            "kind": "boolean"
          },
          "silent_drop_forbidden": {
            "kind": "boolean"
          },
          "silent_reorder_forbidden": {
            "kind": "boolean"
          },
          "latest_only_replacement_forbidden": {
            "kind": "boolean"
          },
          "coalescing_authorized": {
            "kind": "boolean"
          },
          "new_coalescing_semantic_event_authorized": {
            "kind": "boolean"
          },
          "pending_head_retarget_forbidden": {
            "kind": "boolean"
          },
          "capacity_exhausted_result": {
            "kind": "string"
          },
          "capacity_exhausted_must_not_mutate_p5d2_state": {
            "kind": "boolean"
          },
          "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": {
            "kind": "boolean"
          }
        }
      },
      "failure_and_freshness": {
        "kind": "object",
        "fields": {
          "fail_closed_default": {
            "kind": "boolean"
          },
          "network_failure_must_not_create_current_claim": {
            "kind": "boolean"
          },
          "last_known_good_live_projection_preserved": {
            "kind": "boolean"
          },
          "latency_bound_breach_result": {
            "kind": "string"
          },
          "queue_capacity_exhaustion_result": {
            "kind": "string"
          },
          "non_fast_forward_or_unknown_result": {
            "kind": "string"
          },
          "unexpected_state_or_timing_ambiguity_result": {
            "kind": "string"
          },
          "timing_inconsistency_result": {
            "kind": "string"
          },
          "skipped_required_attempt_result": {
            "kind": "string"
          },
          "cadence_gap_result": {
            "kind": "string"
          },
          "pre_source_target_observation_result": {
            "kind": "string"
          }
        }
      },
      "end_to_end_definition": {
        "kind": "object",
        "fields": {
          "real_end_to_end_stages": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 8,
            "max_items": 8,
            "unique": true,
            "allowed_values": [
              "SOURCE_HEAD_BECOMES_OBSERVABLE",
              "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
              "HEAD_TRANSITION_CLASSIFIED",
              "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
              "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
              "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
              "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
              "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
            ],
            "ordered_const": [
              "SOURCE_HEAD_BECOMES_OBSERVABLE",
              "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
              "HEAD_TRANSITION_CLASSIFIED",
              "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
              "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
              "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
              "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
              "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
            ]
          },
          "current_stage_may_qualify_only": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 4,
            "max_items": 4,
            "unique": true,
            "allowed_values": [
              "TIMING_CONTRACT",
              "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
              "AUTHORITY_BOUNDARIES",
              "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
            ]
          },
          "real_end_to_end_pass_requires_all_authorized_applicable_stages": {
            "kind": "boolean"
          },
          "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": {
            "kind": "boolean"
          },
          "transient_tip_exact_detection_sla_not_qualified": {
            "kind": "boolean"
          },
          "real_remote_availability_to_detection_sla_not_qualified": {
            "kind": "boolean"
          }
        }
      },
      "claim_boundary": {
        "kind": "object",
        "fields": {
          "maximum_current_claim": {
            "kind": "string"
          },
          "real_end_to_end_qualification_requires_separate_authorization": {
            "kind": "boolean"
          },
          "forbidden_current_claims": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 8,
            "max_items": 8,
            "unique": true,
            "allowed_values": [
              "P5E_REAL_END_TO_END_QUALIFIED",
              "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
              "REAL_60_SECOND_SLA_QUALIFIED",
              "AUTOMATIC_EVALUATION_QUALIFIED",
              "AUTOMATIC_PROMOTION_QUALIFIED",
              "AUTOMATIC_PUBLICATION_QUALIFIED",
              "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
              "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
            ]
          }
        }
      },
      "real_context_evidence_only": {
        "kind": "object",
        "fields": {
          "live_projection_head_at_opening": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "queued_unevaluated_head_at_opening": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "remote_head_observed_during_contract_opening": {
            "kind": "string",
            "pattern": "[0-9a-f]{40}\\Z"
          },
          "queued_head_is_ancestor_of_remote_head": {
            "kind": "boolean"
          },
          "must_not_be_used_as_real_experiment_execution": {
            "kind": "boolean"
          },
          "must_not_be_mutated_by_contract_qualification": {
            "kind": "boolean"
          }
        }
      },
      "required_synthetic_cases": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 10,
        "max_items": 10,
        "unique": true,
        "allowed_values": [
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
        ]
      },
      "required_breakers": {
        "kind": "array",
        "items": {
          "kind": "string"
        },
        "min_items": 25,
        "max_items": 25,
        "unique": true,
        "allowed_values": [
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
        ]
      },
      "next_gate_after_candidate_qualification": {
        "kind": "object",
        "fields": {
          "external_adversarial_review_required_before_normative_adoption": {
            "kind": "boolean"
          },
          "human_adjudication_required_after_external_review": {
            "kind": "boolean"
          },
          "real_p5e_execution_requires_separate_human_authorization": {
            "kind": "boolean"
          },
          "p6_remains_closed": {
            "kind": "boolean"
          },
          "external_adversarial_rereview_required": {
            "kind": "boolean"
          },
          "human_adjudication_before_external_rereview_forbidden": {
            "kind": "boolean"
          }
        }
      },
      "tip_visibility_semantics": {
        "kind": "object",
        "fields": {
          "observed_remote_tip_definition": {
            "kind": "string"
          },
          "intermediate_fast_forward_commit_definition": {
            "kind": "string"
          },
          "unobserved_intermediate_tip_may_be_claimed_observed": {
            "kind": "boolean"
          },
          "unobserved_intermediate_tip_may_be_queued": {
            "kind": "boolean"
          },
          "fast_forward_content_containment_is_queue_coalescing": {
            "kind": "boolean"
          },
          "already_observed_queued_head_replacement_forbidden": {
            "kind": "boolean"
          },
          "already_observed_queued_head_retarget_forbidden": {
            "kind": "boolean"
          },
          "per_transient_tip_detection_sla_authorized": {
            "kind": "boolean"
          },
          "future_ancestry_enumeration_requires_separate_qualification": {
            "kind": "boolean"
          },
          "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": {
            "kind": "boolean"
          },
          "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": {
            "kind": "boolean"
          }
        }
      },
      "external_review_targeted_closure": {
        "kind": "object",
        "fields": {
          "findings": {
            "kind": "object",
            "fields": {
              "B1": {
                "kind": "string"
              },
              "B2": {
                "kind": "string"
              },
              "B3": {
                "kind": "string"
              },
              "B4": {
                "kind": "string"
              },
              "B5": {
                "kind": "string"
              }
            }
          },
          "required_breakers": {
            "kind": "array",
            "items": {
              "kind": "string"
            },
            "min_items": 8,
            "max_items": 8,
            "unique": true,
            "allowed_values": [
              "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
              "CADENCE_GAP_ACCEPTED",
              "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
              "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
              "READ_COMPLETION_LATENCY_HIDDEN",
              "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
              "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
              "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
            ]
          },
          "requirement_to_executable_evidence_matrix_required": {
            "kind": "boolean"
          },
          "all_required_cases_must_be_mapped": {
            "kind": "boolean"
          },
          "all_base_breakers_must_be_mapped": {
            "kind": "boolean"
          },
          "all_targeted_closure_breakers_must_be_mapped": {
            "kind": "boolean"
          },
          "unmapped_requirement_result": {
            "kind": "string"
          },
          "external_rereview_required_before_human_normative_adoption": {
            "kind": "boolean"
          }
        }
      }
    }
  }
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL MUTATION SWEEP
Path: tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
Authoritative Git blob: b37ca3e31aecde1beccf08eafe04696e6a7dc4c9
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_sweep", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_nodes(value, path=()):
    yield path, value
    if type(value) is dict:
        for key, child in value.items():
            yield from iter_nodes(child, path + (key,))
    elif type(value) is list:
        for index, child in enumerate(value):
            yield from iter_nodes(child, path + (index,))


def get_node(root, path):
    node = root
    for part in path:
        node = node[part]
    return node


def set_node(root, path, value):
    if not path:
        raise AssertionError("root replacement not used by this sweep")
    parent = get_node(root, path[:-1])
    parent[path[-1]] = value


def wrong_type(value):
    if type(value) is bool:
        return 0
    if type(value) is int:
        return float(value)
    if type(value) is str:
        return False
    if value is None:
        return "NOT_NULL"
    raise AssertionError(f"unsupported leaf type: {type(value).__name__}")


def run_sweep():
    guard = load_guard()
    schema_raw = SCHEMA_PATH.read_text(encoding="utf-8")
    baseline = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_baseline = CONTRACT_PATH.read_text(encoding="utf-8")
    guard.validate_governed_json(raw_baseline, schema_raw)

    parsed_object_attempted = 0
    raw_json_attempted = 0
    survivors = []

    def expect_reject(label, mutated):
        nonlocal parsed_object_attempted
        parsed_object_attempted += 1
        try:
            guard.validate_governed_json(
                json.dumps(mutated, ensure_ascii=False),
                schema_raw,
            )
        except guard.GovernedSchemaError:
            return
        survivors.append(label)

    def expect_raw_reject(label, raw_document, expected_reason, raw_schema=None):
        nonlocal raw_json_attempted
        raw_json_attempted += 1
        try:
            guard.validate_governed_json(
                raw_document,
                schema_raw if raw_schema is None else raw_schema,
            )
        except guard.GovernedSchemaError as exc:
            if expected_reason in str(exc):
                return
            survivors.append(f"{label}:WRONG_REASON:{exc}")
            return
        survivors.append(label)

    nodes = list(iter_nodes(baseline))

    # Unknown key at every object node.
    for path, value in nodes:
        if type(value) is not dict:
            continue
        mutated = copy.deepcopy(baseline)
        target = get_node(mutated, path)
        probe = "__rpe01_unknown_key__"
        if probe in target:
            raise AssertionError("unexpected probe collision")
        target[probe] = True
        expect_reject(f"ADD_UNKNOWN:{path}", mutated)

    # Remove every required key from every object node.
    for path, value in nodes:
        if type(value) is not dict:
            continue
        for key in value:
            mutated = copy.deepcopy(baseline)
            target = get_node(mutated, path)
            del target[key]
            expect_reject(f"REMOVE_REQUIRED:{path + (key,)}", mutated)

    # Change every scalar leaf to a different JSON type.
    for path, value in nodes:
        if type(value) in (dict, list):
            continue
        mutated = copy.deepcopy(baseline)
        set_node(mutated, path, wrong_type(value))
        expect_reject(f"WRONG_TYPE:{path}", mutated)

    # Every concrete contract list is preregistered as unique and closed vocabulary.
    for path, value in nodes:
        if type(value) is not list or not value:
            continue

        if len(value) >= 2:
            mutated = copy.deepcopy(baseline)
            target = get_node(mutated, path)
            target[1] = target[0]
            expect_reject(f"DUPLICATE_LIST_MEMBER:{path}", mutated)

        mutated = copy.deepcopy(baseline)
        target = get_node(mutated, path)
        target[0] = "__RPE01_UNKNOWN_LIST_MEMBER__"
        expect_reject(f"UNKNOWN_LIST_MEMBER:{path}", mutated)

    # Exact order is normative for the real end-to-end stage pipeline.
    path = ("end_to_end_definition", "real_end_to_end_stages")
    mutated = copy.deepcopy(baseline)
    target = get_node(mutated, path)
    target[0], target[1] = target[1], target[0]
    expect_reject("ORDER_CHANGE:real_end_to_end_stages", mutated)

    # Raw JSON breaker families constructed from otherwise-valid governed artifacts.
    def replace_once(raw, old, replacement):
        if raw.count(old) != 1:
            raise AssertionError(f"expected one raw anchor: {old!r}")
        return raw.replace(old, replacement, 1)

    authority_anchor = '    "evaluation_authorized": false,'
    duplicate_authority = replace_once(
        raw_baseline,
        authority_anchor,
        authority_anchor + '\n    "evaluation_authorized": true,',
    )
    expect_raw_reject(
        "RAW_REAL_AUTHORITY_DUPLICATE",
        duplicate_authority,
        "duplicate JSON member: evaluation_authorized",
    )

    escaped_duplicate_authority = replace_once(
        raw_baseline,
        authority_anchor,
        authority_anchor + '\n    "\\u0065valuation_authorized": true,',
    )
    expect_raw_reject(
        "RAW_REAL_AUTHORITY_ESCAPED_DUPLICATE",
        escaped_duplicate_authority,
        "duplicate JSON member: evaluation_authorized",
    )

    poll_anchor = '    "poll_interval_seconds": 30,'
    duplicate_poll = replace_once(
        raw_baseline,
        poll_anchor,
        poll_anchor + '\n    "poll_interval_seconds": 31,',
    )
    expect_raw_reject(
        "RAW_REAL_NUMERIC_DUPLICATE",
        duplicate_poll,
        "duplicate JSON member: poll_interval_seconds",
    )

    expect_raw_reject(
        "RAW_REAL_NAN",
        replace_once(
            raw_baseline,
            poll_anchor,
            '    "poll_interval_seconds": NaN,',
        ),
        "non-standard JSON numeric constant forbidden: NaN",
    )

    latency_anchor = '    "detection_latency_seconds_max": 60,'
    expect_raw_reject(
        "RAW_REAL_POSITIVE_INFINITY",
        replace_once(
            raw_baseline,
            latency_anchor,
            '    "detection_latency_seconds_max": Infinity,',
        ),
        "non-standard JSON numeric constant forbidden: Infinity",
    )
    expect_raw_reject(
        "RAW_REAL_NEGATIVE_INFINITY",
        replace_once(
            raw_baseline,
            latency_anchor,
            '    "detection_latency_seconds_max": -Infinity,',
        ),
        "non-standard JSON numeric constant forbidden: -Infinity",
    )

    schema_role_anchor = (
        '  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",'
    )
    duplicate_schema = replace_once(
        schema_raw,
        schema_role_anchor,
        schema_role_anchor + "\n" + schema_role_anchor,
    )
    expect_raw_reject(
        "RAW_VALID_SCHEMA_DUPLICATE_MEMBER",
        raw_baseline,
        "duplicate JSON member: artifact_role",
        duplicate_schema,
    )

    mutation_checks = 0
    mutation_kills = 0
    mutation_survivors = []

    # Mutant 1: remove duplicate-member protection. The real authority duplicate
    # becomes structurally valid because N4 intentionally does not freeze its bool value.
    mutation_checks += 1
    original_strict_object = guard._strict_object
    guard._strict_object = dict
    try:
        try:
            guard.validate_governed_json(duplicate_authority, schema_raw)
        except guard.GovernedSchemaError as exc:
            mutation_survivors.append(
                f"DUPLICATE_DETECTION_MUTANT_SURVIVED:{exc}"
            )
        else:
            mutation_kills += 1
    finally:
        guard._strict_object = original_strict_object

    # Mutant 2: remove non-standard constant parser rejection. The document
    # remains fail-closed later on type, but the parser-specific breaker is killed.
    mutation_checks += 1
    original_reject_constant = guard._reject_constant
    guard._reject_constant = lambda value: float(value)
    try:
        try:
            guard.validate_governed_json(
                replace_once(
                    raw_baseline,
                    poll_anchor,
                    '    "poll_interval_seconds": NaN,',
                ),
                schema_raw,
            )
        except guard.GovernedSchemaError as exc:
            if "non-standard JSON numeric constant forbidden: NaN" not in str(exc):
                mutation_kills += 1
            else:
                mutation_survivors.append(
                    "NONSTANDARD_CONSTANT_MUTANT_SURVIVED"
                )
        else:
            mutation_kills += 1
    finally:
        guard._reject_constant = original_reject_constant

    # Mutant 3: remove deterministic depth protection. Depth 65 must then parse.
    mutation_checks += 1
    original_depth_guard = guard._enforce_max_json_depth
    guard._enforce_max_json_depth = lambda text: None
    try:
        depth_65 = ("[" * 65) + "0" + ("]" * 65)
        try:
            guard.parse_json_strict(depth_65)
        except guard.GovernedSchemaError as exc:
            mutation_survivors.append(
                f"DEPTH_GUARD_MUTANT_SURVIVED:{exc}"
            )
        else:
            mutation_kills += 1
    finally:
        guard._enforce_max_json_depth = original_depth_guard

    return {
        "parsed_object_attempted": parsed_object_attempted,
        "raw_json_attempted": raw_json_attempted,
        "mutation_kill_checks": mutation_checks,
        "mutation_kills": mutation_kills,
        "mutation_survivors": mutation_survivors,
        "attempted": parsed_object_attempted + raw_json_attempted,
        "survivors": survivors,
        "survivor_count": len(survivors),
    }


class RPE01MutationSweepTests(unittest.TestCase):
    def test_all_preregistered_contract_schema_mutations_are_rejected(self):
        result = run_sweep()
        self.assertEqual(result["parsed_object_attempted"], 433)
        self.assertEqual(result["raw_json_attempted"], 7)
        self.assertEqual(result["attempted"], 440)
        self.assertEqual(result["survivors"], [])
        self.assertEqual(result["mutation_kill_checks"], 3)
        self.assertEqual(result["mutation_kills"], 3)
        self.assertEqual(result["mutation_survivors"], [])


if __name__ == "__main__":
    result = run_sweep()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["survivor_count"] == 0 else 1)
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: PORTABLE PRIOR NB1/NB2 TEST
Path: tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py
Authoritative Git blob: f52b88a9d56ea12a515e35ad8e915d0a1bc28b91
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_targeted_closure", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def schema_raw() -> str:
    return json.dumps(
        {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_TARGETED_CLOSURE_SYNTHETIC",
            "root": {
                "kind": "object",
                "fields": {
                    "a": {"kind": "integer"},
                },
            },
        },
        separators=(",", ":"),
    )


class NB1RawSchemaOnlyPublicApiTests(unittest.TestCase):
    def test_validate_governed_json_accepts_legitimate_raw_schema(self):
        g = load_guard()
        result = g.validate_governed_json('{"a":1}', schema_raw())
        self.assertEqual(result, {"a": 1})

    def test_validate_governed_json_rejects_preparsed_schema_object(self):
        g = load_guard()
        parsed_schema = json.loads(schema_raw())
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json('{"a":1}', parsed_schema)

    def test_public_validation_rejects_duplicate_schema_member_before_widening(self):
        g = load_guard()
        widened_duplicate_schema = (
            '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
            '"artifact_role":"RPE01_TARGETED_CLOSURE_SYNTHETIC",'
            '"root":{"kind":"object",'
            '"fields":{"a":{"kind":"integer"}},'
            '"fields":{"a":{"kind":"integer"},'
            '"evaluation_override":{"kind":"boolean"}}}}'
        )
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(
                '{"a":1,"evaluation_override":true}',
                widened_duplicate_schema,
            )

    def test_parsed_document_schema_validator_is_not_public(self):
        g = load_guard()
        self.assertFalse(
            hasattr(g, "validate_document"),
            "parsed-document/schema public bypass must not remain exposed",
        )


class NB2NormalizedExceptionTests(unittest.TestCase):
    def test_pathological_integer_conversion_is_normalized(self):
        g = load_guard()
        pathological = '{"a":' + ("9" * 5000) + "}"
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(pathological)

    def test_pathological_nesting_is_normalized(self):
        g = load_guard()
        depth = g.MAX_GOVERNED_JSON_DEPTH + 1
        pathological = ("[" * depth) + "0" + ("]" * depth)
        with self.assertRaisesRegex(
            g.GovernedSchemaError,
            "maximum governed JSON depth",
        ):
            g.parse_json_strict(pathological)


if __name__ == "__main__":
    unittest.main()
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL QUALIFICATION JSON
Path: tools/obsidian_projection/rpe01_final_hardening_qualification_v0_1.json
Authoritative Git blob: f514af4bf01a62b3f751e14cfffaaf20bfe66885
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_FINAL_HARDENING_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-03",
  "opening_head": "cbe8b2534e3a4f65edbe1732a5b322e018756713",
  "preregistration_head": "cee9f7e4c46a9cef28891561c63e112d81cc3744",
  "preregistration_blob": "3fbd871ac3faeaab8d40c730ac539677ac272c33",
  "final_delta_review_return_blob": "d5ce7aa73a070610a2a56c04647c426cff7d1249",
  "red_head": "6327333ba27b551ac7c1fcda20fafe3eb488749f",
  "red_test_blob": "449898e62f244a275af290559b7441af1798ee09",
  "red_report_blob": "33f6f1bea040bddcb452657319e87f90bca9ed54",
  "final_guard_blob": "26f977961d72a062199d71ffd628d5a5cc047887",
  "p5e_schema_blob_unchanged": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
  "main_rpe01_test_blob_unchanged": "cd0e091233e5a4473ef280c7061db8cf880169e9",
  "final_mutation_sweep_blob": "b37ca3e31aecde1beccf08eafe04696e6a7dc4c9",
  "portable_nb1_nb2_test_blob": "f52b88a9d56ea12a515e35ad8e915d0a1bc28b91",
  "final_hardening_test_blob": "449898e62f244a275af290559b7441af1798ee09",
  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
  "nb_a": {
    "status": "CLOSED_CANDIDATE",
    "max_governed_json_depth": 64,
    "depth_definition": "Maximum syntactic nesting of JSON containers outside strings, root container depth 1.",
    "document_boundary_64": "PASS",
    "document_boundary_65": "REJECT_GOVERNED_SCHEMA_ERROR",
    "schema_boundary_64": "PASS",
    "schema_boundary_65": "REJECT_GOVERNED_SCHEMA_ERROR",
    "interpreter_recursion_limit_normative": false,
    "schema_validation_recursion_normalized": true,
    "document_validation_recursion_normalized_at_public_boundary": true
  },
  "nb_b": {
    "status": "CLOSED_CANDIDATE",
    "parsed_object_mutations": 433,
    "raw_json_breakers": 7,
    "raw_json_breaker_survivors": 0,
    "mutation_kill_checks": 3,
    "mutation_kills": 3,
    "mutation_survivors": 0,
    "raw_breakers_are_built_from": [
      "otherwise-valid adopted P5-E contract",
      "otherwise-valid P5-E governed schema"
    ],
    "raw_breaker_families": [
      "contradictory duplicate real authority key evaluation_authorized",
      "escaped duplicate real authority key evaluation_authorized",
      "duplicate real numeric key poll_interval_seconds",
      "NaN in real numeric field poll_interval_seconds",
      "Infinity in real numeric field detection_latency_seconds_max",
      "-Infinity in real numeric field detection_latency_seconds_max",
      "duplicate artifact_role in otherwise-valid raw governed schema"
    ],
    "raw_breakers_require_targeted_parser_reason": true
  },
  "nb_c": {
    "status": "ADOPTED_USAGE_RULE_CANDIDATE",
    "authorized_governed_artifact_validation_entrypoint": "validate_governed_json(raw_document, raw_schema)",
    "underscore_prefixed_guard_functions_external_consumer_use_forbidden": true,
    "validate_schema_definition_is_not_authorized_for_governed_document_validation": true,
    "runtime_tools_external_private_guard_consumers_observed": 0
  },
  "test_results": {
    "final_hardening_red": "14 tests; 2 failures + 4 errors before patch; 8 passes",
    "final_hardening_green": "14/14 PASS",
    "current_rpe01_surface": "42/42 PASS",
    "final_targeted_regression": "109/109 PASS",
    "final_sweep": {
      "parsed_object_attempted": 433,
      "raw_json_attempted": 7,
      "attempted_total": 440,
      "survivors": 0,
      "mutation_kill_checks": 3,
      "mutation_kills": 3,
      "mutation_survivors": 0
    },
    "contract_diff_from_adopted_readiness_head": 0,
    "model_diff_from_adopted_readiness_head": 0,
    "p5d4_runtime_diff_from_adopted_readiness_head": 0
  },
  "qualification_environment_non_normative": {
    "python_version": "3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]",
    "python_implementation": "CPython",
    "platform": "Windows-11-10.0.22631-SP0"
  },
  "current_artifact_depth_observations_non_normative": {
    "adopted_p5e_contract": 3,
    "p5e_governed_schema": 8
  },
  "remaining_nonblocking_scope_notes": {
    "nb3": "The P5-E schema remains structural/type/list governance; adopted P5-E invariants retain value semantics.",
    "nb4": "Generic source_binding/artifact_role remain structurally validated but not dynamically bound by the generic guard.",
    "nb5": "Contradictory restrictive schema constraints, ASCII regex semantics, and isolated-surrogate handling remain non-blocking future hardening."
  },
  "real_state_fingerprints_unchanged": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "claim_boundary": {
    "rpe01_final_hardening_qualified_for_external_delta_review": true,
    "rpe01_human_adopted": false,
    "rpe02_opened": false,
    "rpe03_opened": false,
    "real_p5e_authorized": false
  },
  "next_gate": "FINAL_SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADOPTION",
  "stop": true
}
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL QUALIFICATION REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-FINAL-HARDENING-QUALIFICATION.md
Authoritative Git blob: 92e45cf8fa279c0b9643a9ad77d4c1f19d6a7cdf
Display copy below is normalized for packet formatting and is not claimed byte-identical.
~~~~
# RPE-01 — FINAL PORTABILITY + RAW-BREAKER DISCRIMINATION — QUALIFICATION

Date: 2026-10-03

## Result

```text
RPE01_FINAL_HARDENING
= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```

## Purpose

This is the final technical hardening pass requested after the independent review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with no blocker.

It closes only:
- NB-a — deterministic depth / recursion portability;
- NB-b — discriminating raw breakers;
- NB-c — consumer usage rule clarification.

No adopted P5-E contract, synthetic model or P5-D4 runtime was changed.

## Preregistration

Opening HEAD:
`cbe8b2534e3a4f65edbe1732a5b322e018756713`

Preregistration HEAD:
`cee9f7e4c46a9cef28891561c63e112d81cc3744`

Preregistration blob:
`3fbd871ac3faeaab8d40c730ac539677ac272c33`

The deterministic bound was frozen before RED:

```text
MAX_GOVERNED_JSON_DEPTH = 64
```

Definition:

maximum syntactic nesting of JSON containers outside JSON strings, with the root object/array at depth 1.

Current protected artifacts are far below the bound:

```text
P5-E adopted contract max depth = 3
P5-E governed schema max depth = 8
```

These current-depth observations are non-normative.

## RED

RED HEAD:
`6327333ba27b551ac7c1fcda20fafe3eb488749f`

RED test:
`449898e62f244a275af290559b7441af1798ee09`

RED report:
`33f6f1bea040bddcb452657319e87f90bca9ed54`

Observed before patch:

```text
Ran 14 tests

FAILED
failures = 2
errors = 4

8 tests already passed
6 tests produced the required RED signal
```

The RED did not use an interpreter recursion threshold as evidence.

## NB-a closure

Final guard:

`26f977961d72a062199d71ffd628d5a5cc047887`

The guard now pre-scans raw JSON before `json.loads`.

It tracks container nesting while ignoring braces/brackets inside JSON strings and honoring backslash escapes.

Policy:

```text
depth <= 64
→ depth guard permits parsing

depth > 64
→ GovernedSchemaError
```

The same parser boundary is used for:
- governed documents;
- governed schemas.

Portable exact-boundary tests demonstrate:

```text
document depth 64 → allowed by depth guard
document depth 65 → GovernedSchemaError

schema depth 64 → valid / accepted
schema depth 65 → GovernedSchemaError
```

Residual recursion is also normalized:
- `validate_schema_definition` converts residual `RecursionError`;
- public `validate_governed_json` converts residual document-validation `RecursionError`.

Dedicated tests force recursion failures inside:
- `_validate_schema_node`;
- `_validate_document_node`.

Both emerge as `GovernedSchemaError`.

Therefore the normative property no longer depends on whether a particular Python JSON decoder accepts 5000 nested containers.

The old 5000-level test was replaced by:

`MAX_GOVERNED_JSON_DEPTH + 1`.

## Qualification environment

The final local qualification ran under:

```text
Python
= 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)]

Implementation
= CPython

Platform
= Windows-11-10.0.22631-SP0
```

This environment is evidence context only.

It is not part of the depth semantics.

## NB-b closure — discriminating raw breakers

The parsed-object sweep remains:

```text
433 attempted
0 survivors
```

The seven raw breakers are now built from otherwise-valid governed artifacts and require the intended parser rejection reason.

They are:

1. contradictory duplicate `evaluation_authorized`;
2. escaped duplicate spelling of `evaluation_authorized`;
3. duplicate real numeric `poll_interval_seconds`;
4. NaN injected into real `poll_interval_seconds`;
5. Infinity injected into real `detection_latency_seconds_max`;
6. -Infinity injected into real `detection_latency_seconds_max`;
7. duplicate `artifact_role` in the otherwise-valid raw P5-E schema.

Observed:

```text
RAW BREAKERS = 7
SURVIVORS = 0
```

The breaker no longer passes merely because a dummy key such as `x` is structurally unknown.

## Mutation-kill evidence

Three targeted mutants were exercised:

### Duplicate-member mutant

Protection:
`object_pairs_hook=_strict_object`

Mutant:
duplicate detection replaced by normal dictionary construction.

Result:
the contradictory real `evaluation_authorized` document becomes structurally accepted.

`MUTANT = KILLED`

### Non-standard-constant mutant

Protection:
`parse_constant=_reject_constant`

Mutant:
NaN is allowed through JSON parsing.

Result:
the later schema still fails closed on integer type, but the required parser-specific NaN rejection disappears.

`MUTANT = KILLED`

### Deterministic-depth mutant

Protection:
`_enforce_max_json_depth`

Mutant:
depth guard replaced by no-op.

Result:
depth-65 JSON parses.

`MUTANT = KILLED`

Summary:

```text
MUTATION-KILL CHECKS = 3
KILLS = 3
SURVIVORS = 0
```

## NB-c usage rule

The governed consumer rule is:

```text
AUTHORIZED GOVERNED-ARTIFACT VALIDATION ENTRYPOINT
= validate_governed_json(raw_document, raw_schema)
```

For future RPE consumers:
- underscore-prefixed guard functions are forbidden;
- `validate_schema_definition` is not a governed-document validation entrypoint;
- callers must not use it as a document-validation bypass.

A repository search over `tools/`, excluding the guard module itself, found no runtime consumer of:
- `validate_schema_definition`;
- `_validate_document`;
- `_validate_document_node`;
- `_validate_schema_node`.

RPE-02/RPE-03 remain unopened, so no future runtime consumer exists yet.

## GREEN

Final hardening tests:

```text
14 / 14 PASS
```

Current RPE-01 surface:

```text
42 / 42 PASS
```

Final evidence partition:

```text
PARSED-OBJECT MUTATIONS = 433
RAW-JSON BREAKERS       = 7
RAW SURVIVORS           = 0

MUTATION-KILL CHECKS    = 3
MUTATION KILLS          = 3
MUTATION SURVIVORS      = 0
```

## Final targeted regression

P5-E qualification surface + all RPE-01 tests:

```text
109 / 109 PASS
```

Protected artifact deltas from the adopted readiness base:

```text
P5-E CONTRACT = 0
P5-E MODEL = 0
P5-D4 RUNTIME = 0
```

## Remaining non-blocking scope

Unchanged:

- NB-3: RPE-01 is structural/type/list governance; adopted P5-E invariants retain value semantics.
- NB-4: generic source binding is structurally represented but not dynamically enforced by the generic guard.
- NB-5: contradictory restrictive constraints, ASCII-regex policy and isolated-surrogate handling remain future hardening where relevant.

None of these is claimed closed by this final hardening.

## Real-state integrity

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Final candidate identities

```text
GUARD
= 26f977961d72a062199d71ffd628d5a5cc047887

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

MAIN RPE-01 TEST
= cd0e091233e5a4473ef280c7061db8cf880169e9

MUTATION SWEEP
= b37ca3e31aecde1beccf08eafe04696e6a7dc4c9

PORTABLE NB1/NB2 TEST
= f52b88a9d56ea12a515e35ad8e915d0a1bc28b91

FINAL HARDENING TEST
= 449898e62f244a275af290559b7441af1798ee09
```

## Maximum claim

```text
NB-a
= CLOSED_CANDIDATE

NB-b
= CLOSED_CANDIDATE

NB-c
= USAGE_RULE_DEFINED

RPE01_FINAL_HARDENING
= QUALIFIED_FOR_FINAL_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

RPE-03
= CLOSED

REAL_P5E
= CLOSED
```
~~~~
