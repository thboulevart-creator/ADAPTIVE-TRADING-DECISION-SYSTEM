# RPE-01 ? NB-1 / NB-2 TARGETED CLOSURE ? EXTERNAL DELTA REVIEW PACKET

Date: 2026-10-03

## Independent reviewer mandate

Review only the targeted closure of the prior RPE-01 external review notes.

Prior external verdict: PASS_WITH_NON_BLOCKING_NOTES
Prior blockers: NONE

Targeted corrections under review:

- NB-1 ? public validation API must require raw schema input and remove the parsed-schema bypass;
- NB-2 ? parser/runtime failures ValueError and RecursionError must normalize to GovernedSchemaError;
- NB-6 ? mutation evidence must distinguish parsed-object mutations from raw-JSON breaker families and use strict raw schema input;
- NB-7 ? packet source/identity fidelity.

This review creates no adoption authority.

RPE-02 = CLOSED
REAL_P5E = CLOSED

## Candidate identity

First RPE-01 external-review packet HEAD:
ae75f3f1013bdf3e26a7d38e005340bf50c1abe1

Persisted review + adjudication HEAD:
c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b

Targeted RED HEAD:
0d680623b50a075024107443b14b638b1250e0d8

Targeted closure technical HEAD:
8924e0121c091887f461a727a284b5ad2a84f14f

Final guard:
82f4323316b95ea5895cdd0c6f0c68e801e595ca

P5-E governed schema unchanged:
87e45cc75753439879e2902d3cbdbd5d71d8a1b2

Final main RPE-01 test:
cd0e091233e5a4473ef280c7061db8cf880169e9

Final mutation sweep:
a8baceaf4a921765ae0fdcb182bef7dd0eba1246

Targeted RED/GREEN test:
1691d7f74e430d65f00fd4603f6da51c23e75a52

Targeted RED report:
425b8102389e134ef54f6ff95b03afa8a9d9ae8c

Targeted closure qualification JSON:
c20501938569de38de3190982d3dc97b49154904

Targeted closure qualification report:
b08d02c479631824261556ef23b2f04d29587daa

Persisted first external review:
51b168dd9973b748e8e592093dc16497d2a42301

Persisted internal adjudication:
b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a

## Historical evidence fidelity

Historical first RPE-01 RED is not embedded under a later source label.

Immutable references only:

- initial RED test blob:
  803709c26769fc9889b4ac1e47c0dd8df2782580
- initial RED report blob:
  b3a7df32198fd5a618f927c83d04d5f3a6491050

All authoritative source identities in this packet are Git blob SHAs.

Display copies are produced from those Git blobs and normalized only for readable packet formatting. They are explicitly NOT claimed byte-identical.

## Reproduced final evidence

NB-1 / NB-2 targeted = 6 / 6 PASS
RPE-01 main + sweep unittest surface = 22 / 22 PASS

Mutation evidence:
- parsed-object mutations = 433
- raw-JSON breakers = 7
- total attempted = 440
- survivors = 0

Final P5-E + RPE-01 targeted regression:
95 / 95 PASS

Protected predecessor diffs:
- P5-E contract diff = 0
- P5-E model diff = 0
- P5-D4 runtime diff = 0

## Delta questions

### NB-1
1. Does final validate_governed_json require raw str|bytes for both document and schema?
2. Is a pre-parsed schema dictionary rejected?
3. Has public validate_document(document, schema) been removed?
4. Do current RPE-01 callers, including sweep, use raw schema?
5. Can any public path still validate against permissively pre-parsed schema?

### NB-2
6. Are ValueError and RecursionError normalized to GovernedSchemaError?
7. Are 5000-digit integer and 5000-level nesting probes adequate for the observed failure classes?
8. Does normalization preserve fail-closed behavior?

### NB-6
9. Is 433 parsed + 7 raw = 440 accurate?
10. Are duplicate document members, escaped duplicates, NaN, Infinity, -Infinity and duplicate raw schema members exercised?
11. Does sweep itself consume raw schema through strict API?
12. Does any claim incorrectly imply old 433 count covered raw families?

### NB-7
13. Is historical RED now clearly an immutable reference rather than mislabeled current source?
14. Are authoritative identities explicit Git blob SHAs?
15. Are display copies correctly described as normalized/non-byte-identical?
16. Is any current announced blob inconsistent with its display copy semantically?

### Remaining notes
17. Is NB-3 correctly stated as structural/type/list scope, with adopted P5-E invariants carrying value semantics?
18. Is NB-4 correctly stated as a binding-evidence limitation rather than dynamic enforcement?
19. Do NB-5 items remain non-blocking for N4?

### Regression / authority
20. Is 95/95 targeted regression sufficient?
21. Is full Obsidian suite still unnecessary given zero diff to protected runtime artifacts?
22. Has any RPE-02 or REAL P5-E authority leaked?
23. Is RPE-01 ready for human adoption if this delta review has no blocker?

## Required adversarial probes

Attempt at least:
- pre-parsed schema dict to validate_governed_json;
- duplicate fields in raw schema;
- escaped duplicate raw schema member;
- pathological integer;
- pathological nesting;
- raw document duplicate;
- raw escaped duplicate;
- NaN / Infinity / -Infinity;
- schema widening by unknown field;
- remaining public parsed-schema bypass;
- mutation sweep with raw schema;
- change only an authority boolean and verify this remains outside structural N4 semantics.

## Required output

Return exactly one:
VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then provide:
- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- NB1_CHECK
- NB2_CHECK
- NB6_CHECK
- NB7_PACKET_FIDELITY_CHECK
- NB3_NB4_SCOPE_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_NEXT_ACTION

For every finding distinguish OBSERVED from INFERENCE, state BLOCKING or NON_BLOCKING, cite exact packet section/function/test, and give a minimal falsification case when possible.

This review creates no authority.

RPE-02 = CLOSED
REAL_P5E = CLOSED

---

# NORMALIZED DISPLAY OF EXACT GIT DIFF ? TARGETED RED TO CLOSURE
~~~~diff
diff --git a/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
new file mode 100644
index 0000000..b08d02c
--- /dev/null
+++ b/reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
@@ -0,0 +1,294 @@
+# RPE-01 — EXTERNAL REVIEW TARGETED CLOSURE — QUALIFICATION
+
+Date: 2026-10-03
+
+## Result
+
+```text
+RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
+= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW
+
+RPE01_HUMAN_ADOPTION
+= PENDING
+
+RPE-02
+= CLOSED
+
+REAL_P5E
+= CLOSED
+```
+
+## External-review origin
+
+The first independent RPE-01 review returned:
+
+`PASS_WITH_NON_BLOCKING_NOTES`
+
+with:
+
+`BLOCKING_FINDINGS = NONE`
+
+The reviewer reproduced:
+- 22/22 RPE-01 tests;
+- 89/89 targeted P5-E + RPE-01 regression;
+- 41 additional adversarial probes.
+
+Two notes were adjudicated as targeted corrections required before human adoption / before RPE-02 consumes the guard:
+
+- NB-1 — parsed-schema bypass;
+- NB-2 — non-normalized parser exceptions.
+
+NB-6 and NB-7 were accepted as evidence-hygiene corrections for this closure.
+
+## RED
+
+Opening HEAD:
+`c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b`
+
+Targeted RED commit:
+`0d680623b50a075024107443b14b638b1250e0d8`
+
+Targeted RED test blob:
+`1691d7f74e430d65f00fd4603f6da51c23e75a52`
+
+Targeted RED report blob:
+`425b8102389e134ef54f6ff95b03afa8a9d9ae8c`
+
+Observed before correction:
+
+```text
+Ran 6 tests
+
+FAILED
+failures = 2
+errors = 3
+1 test passed
+```
+
+RED demonstrated:
+- legitimate raw schema not accepted by public API;
+- pre-parsed schema object accepted by public API;
+- parsed document/schema bypass still publicly exposed;
+- pathological integer leaks ValueError;
+- pathological nesting leaks RecursionError.
+
+## NB-1 closure
+
+Final guard blob:
+`82f4323316b95ea5895cdd0c6f0c68e801e595ca`
+
+Public API is now:
+
+```text
+validate_governed_json(
+    raw_document: str | bytes,
+    raw_schema: str | bytes,
+)
+```
+
+The public API strictly parses the schema itself before parsing/validating the document.
+
+A pre-parsed schema dictionary is rejected.
+
+The former public:
+`validate_document(document, schema)`
+
+no longer exists.
+
+The internal parsed-document validator is private:
+
+`_validate_document(...)`
+
+and receives an already strictly validated schema only from the raw public path.
+
+Existing RPE-01 tests and the mutation sweep now send the concrete P5-E schema as raw JSON.
+
+## NB-2 closure
+
+`parse_json_strict` now normalizes:
+
+- `ValueError`;
+- `RecursionError`;
+- `json.JSONDecodeError`;
+
+into:
+
+`GovernedSchemaError`
+
+while preserving existing direct `GovernedSchemaError` failures.
+
+Dedicated RED→GREEN cases cover:
+- a 5000-digit integer;
+- 5000-level array nesting.
+
+The guard remains fail-closed with one public exception family for these parser failure modes.
+
+## GREEN
+
+Targeted NB-1/NB-2 tests:
+
+```text
+6 / 6 PASS
+```
+
+Current RPE-01 main + mutation-sweep unittest surface:
+
+```text
+22 / 22 PASS
+```
+
+## NB-6 — corrected sweep accounting
+
+The previous reported count `433` represented parsed-object mutations only.
+
+The final sweep now reports separately:
+
+```text
+PARSED-OBJECT MUTATIONS = 433
+RAW-JSON BREAKERS       = 7
+TOTAL                    = 440
+SURVIVORS                = 0
+```
+
+Raw breaker families now executed inside the sweep:
+
+- duplicate top-level member;
+- duplicate nested member;
+- escaped key duplicate that decodes to the same member;
+- NaN;
+- Infinity;
+- -Infinity;
+- duplicate member in raw schema JSON.
+
+The sweep itself uses the raw concrete schema through the strict public API.
+
+Therefore no claim is made that the original 433 count covered raw JSON operators.
+
+## Final targeted regression
+
+Current P5-E qualification surface + RPE-01 + targeted closure:
+
+```text
+95 / 95 PASS
+```
+
+Relative to the adopted readiness base:
+
+```text
+P5-E contract diff = 0
+P5-E model diff = 0
+P5-D4 runtime diff = 0
+```
+
+No full Obsidian suite was run.
+
+## NB-3 — explicit scope clarification
+
+The concrete P5-E governed schema is:
+
+`STRUCTURAL + STRICT-TYPE + CLOSED-NORMATIVE-LIST`
+
+It is not a replacement for the adopted P5-E semantic invariant layer.
+
+Therefore values such as existing authorization booleans, timing integers, and free descriptive strings are not all frozen to their current literal value by this schema.
+
+Existing P5-E value semantics remain guarded by the adopted P5-E invariants.
+
+For future REAL P5-E configuration schemas, an authority flag should normally be encoded as schema-level `const: false` when the schema itself is intended to carry that authority boundary.
+
+This requirement is carried forward to the preregistrations that define RPE-04/RPE-05/RPE-06 configuration surfaces.
+
+## NB-4 — explicit binding limitation
+
+The generic guard validates the structure of:
+- `artifact_role`;
+- `source_binding`.
+
+It does not currently receive an externally expected role or recompute the Git source blob as part of generic validation.
+
+For the current P5-E schema, source binding remains independently demonstrated by the dedicated Git blob test and qualification evidence.
+
+No claim is made that dynamic source-binding enforcement is already part of the generic RPE-01 guard.
+
+Later REAL P5-E preregistrations must decide explicitly whether expected-role/source-byte binding belongs in the guard API or at the governed caller boundary.
+
+## NB-5 — retained non-blocking hardening debt
+
+The following remain non-blocking future hardening:
+- proactively reject contradictory restrictive schema constraints;
+- require ASCII regex semantics where a future schema relies on character classes;
+- reject isolated Unicode surrogates where downstream UTF-8 evidence persistence requires it.
+
+These do not reopen N4.
+
+## NB-7 — packet-fidelity rule for the next delta packet
+
+The next packet must:
+- identify the historical RED only by its exact immutable Git identity/reference unless its exact historical bytes are deliberately extracted;
+- not label the current GREEN test as the historical RED source;
+- not claim transformed Markdown to be byte-identical to historical report blobs;
+- embed the persisted external review from its current canonical file;
+- bind exact current code/JSON blobs;
+- include an exact Git diff for the targeted closure.
+
+## Final candidate identities
+
+```text
+GUARD
+= 82f4323316b95ea5895cdd0c6f0c68e801e595ca
+
+P5-E GOVERNED SCHEMA
+= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2
+
+MAIN RPE-01 TEST
+= cd0e091233e5a4473ef280c7061db8cf880169e9
+
+MUTATION SWEEP TEST
+= a8baceaf4a921765ae0fdcb182bef7dd0eba1246
+
+TARGETED CLOSURE TEST
+= 1691d7f74e430d65f00fd4603f6da51c23e75a52
+```
+
+## Real-state integrity
+
+P5-D4 real state remains unchanged:
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
+## Maximum claim
+
+```text
+NB-1
+= CLOSED_CANDIDATE
+
+NB-2
+= CLOSED_CANDIDATE
+
+NB-6
+= EVIDENCE_ACCOUNTING_CORRECTED
+
+NB-7
+= DELTA_PACKET_FIDELITY_REQUIREMENT_ACTIVE
+
+RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
+= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW
+
+RPE01_HUMAN_ADOPTION
+= PENDING
+
+RPE-02
+= CLOSED
+
+REAL_P5E
+= CLOSED
+```
diff --git a/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
index bad4959..a8bacea 100644
--- a/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
+++ b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
@@ -58,21 +58,34 @@ def wrong_type(value):

 def run_sweep():
     guard = load_guard()
-    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
+    schema_raw = SCHEMA_PATH.read_text(encoding="utf-8")
     baseline = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
     raw_baseline = CONTRACT_PATH.read_text(encoding="utf-8")
-    guard.validate_governed_json(raw_baseline, schema)
+    guard.validate_governed_json(raw_baseline, schema_raw)

-    attempted = 0
+    parsed_object_attempted = 0
+    raw_json_attempted = 0
     survivors = []

     def expect_reject(label, mutated):
-        nonlocal attempted
-        attempted += 1
+        nonlocal parsed_object_attempted
+        parsed_object_attempted += 1
         try:
             guard.validate_governed_json(
                 json.dumps(mutated, ensure_ascii=False),
-                schema,
+                schema_raw,
+            )
+        except guard.GovernedSchemaError:
+            return
+        survivors.append(label)
+
+    def expect_raw_reject(label, raw_document, raw_schema=None):
+        nonlocal raw_json_attempted
+        raw_json_attempted += 1
+        try:
+            guard.validate_governed_json(
+                raw_document,
+                schema_raw if raw_schema is None else raw_schema,
             )
         except guard.GovernedSchemaError:
             return
@@ -133,8 +146,27 @@ def run_sweep():
     target[0], target[1] = target[1], target[0]
     expect_reject("ORDER_CHANGE:real_end_to_end_stages", mutated)

+    # Raw JSON breaker families preregistered separately from parsed-object mutations.
+    expect_raw_reject("RAW_DUPLICATE_TOP_LEVEL", '{"x":1,"x":2}')
+    expect_raw_reject("RAW_DUPLICATE_NESTED", '{"outer":{"x":1,"x":2}}')
+    expect_raw_reject(
+        "RAW_ESCAPED_DUPLICATE",
+        '{"evaluation_authorized":true,"\u0065valuation_authorized":false}',
+    )
+    expect_raw_reject("RAW_NAN", '{"x":NaN}')
+    expect_raw_reject("RAW_POSITIVE_INFINITY", '{"x":Infinity}')
+    expect_raw_reject("RAW_NEGATIVE_INFINITY", '{"x":-Infinity}')
+    duplicate_schema = (
+        '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
+        '"artifact_role":"A","artifact_role":"B",'
+        '"root":{"kind":"null"}}'
+    )
+    expect_raw_reject("RAW_SCHEMA_DUPLICATE_MEMBER", 'null', duplicate_schema)
+
     return {
-        "attempted": attempted,
+        "parsed_object_attempted": parsed_object_attempted,
+        "raw_json_attempted": raw_json_attempted,
+        "attempted": parsed_object_attempted + raw_json_attempted,
         "survivors": survivors,
         "survivor_count": len(survivors),
     }
@@ -143,7 +175,9 @@ def run_sweep():
 class RPE01MutationSweepTests(unittest.TestCase):
     def test_all_preregistered_contract_schema_mutations_are_rejected(self):
         result = run_sweep()
-        self.assertGreater(result["attempted"], 0)
+        self.assertEqual(result["parsed_object_attempted"], 433)
+        self.assertEqual(result["raw_json_attempted"], 7)
+        self.assertEqual(result["attempted"], 440)
         self.assertEqual(result["survivors"], [])


diff --git a/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py b/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
index 391663e..cd0e091 100644
--- a/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
+++ b/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
@@ -28,11 +28,14 @@ def load_guard():
     return load_module(GUARD_PATH, "rpe01_guard_under_test")


-def load_schema():
+def load_schema_raw():
     if not P5E_SCHEMA_PATH.exists():
         raise AssertionError(f"required governed schema missing: {P5E_SCHEMA_PATH}")
-    g = load_guard()
-    return g.parse_schema_json_strict(P5E_SCHEMA_PATH.read_text(encoding="utf-8"))
+    return P5E_SCHEMA_PATH.read_text(encoding="utf-8")
+
+
+def synthetic_schema_raw():
+    return json.dumps(synthetic_schema(), separators=(",", ":"))


 def current_contract_raw() -> str:
@@ -135,14 +138,14 @@ class StrictTypeAndListTests(unittest.TestCase):
     def assert_rejected(self, document):
         g = load_guard()
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(json.dumps(document), synthetic_schema())
+            g.validate_governed_json(json.dumps(document), synthetic_schema_raw())

     def test_float_and_scientific_float_where_integer_required_are_rejected(self):
         self.assert_rejected({"interval_ns": 30.0, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
         g = load_guard()
         raw = '{"interval_ns":1e2,"enabled":false,"mode":"FIXED_RATE","stages":["OBSERVE","STOP"]}'
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(raw, synthetic_schema())
+            g.validate_governed_json(raw, synthetic_schema_raw())

     def test_boolean_where_integer_required_is_rejected(self):
         self.assert_rejected({"interval_ns": True, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
@@ -171,13 +174,13 @@ class StrictTypeAndListTests(unittest.TestCase):
 class P5EConcreteSchemaTests(unittest.TestCase):
     def test_adopted_contract_is_accepted_without_byte_mutation(self):
         g = load_guard()
-        schema = load_schema()
-        doc = g.validate_governed_json(current_contract_raw(), schema)
+        schema_raw = load_schema_raw()
+        doc = g.validate_governed_json(current_contract_raw(), schema_raw)
         self.assertEqual(doc["schema"], "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1")

     def test_unknown_keys_at_representative_depths_are_rejected(self):
         g = load_guard()
-        schema = load_schema()
+        schema_raw = load_schema_raw()
         contract = json.loads(current_contract_raw())
         paths = [
             (),
@@ -194,43 +197,44 @@ class P5EConcreteSchemaTests(unittest.TestCase):
                     node = node[key]
                 node["rpe01_unknown_key"] = True
                 with self.assertRaises(g.GovernedSchemaError):
-                    g.validate_governed_json(json.dumps(mutated), schema)
+                    g.validate_governed_json(json.dumps(mutated), schema_raw)

     def test_missing_required_key_is_rejected(self):
         g = load_guard()
-        schema = load_schema()
+        schema_raw = load_schema_raw()
         contract = json.loads(current_contract_raw())
         del contract["authority_boundary"]["evaluation_authorized"]
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(json.dumps(contract), schema)
+            g.validate_governed_json(json.dumps(contract), schema_raw)

     def test_normative_list_duplicate_unknown_and_order_change_are_rejected(self):
         g = load_guard()
-        schema = load_schema()
+        schema_raw = load_schema_raw()
         contract = json.loads(current_contract_raw())

         duplicate = copy.deepcopy(contract)
         duplicate["claim_boundary"]["forbidden_current_claims"][1] = duplicate["claim_boundary"]["forbidden_current_claims"][0]
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(json.dumps(duplicate), schema)
+            g.validate_governed_json(json.dumps(duplicate), schema_raw)

         unknown = copy.deepcopy(contract)
         unknown["required_synthetic_cases"][0] = "RPE01_UNKNOWN_CASE"
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(json.dumps(unknown), schema)
+            g.validate_governed_json(json.dumps(unknown), schema_raw)

         reordered = copy.deepcopy(contract)
         stages = reordered["end_to_end_definition"]["real_end_to_end_stages"]
         stages[0], stages[1] = stages[1], stages[0]
         with self.assertRaises(g.GovernedSchemaError):
-            g.validate_governed_json(json.dumps(reordered), schema)
+            g.validate_governed_json(json.dumps(reordered), schema_raw)


 class SchemaBindingTests(unittest.TestCase):
     def test_p5e_schema_source_binding_matches_current_contract_blob(self):
         import subprocess

-        schema = load_schema()
+        g = load_guard()
+        schema = g.parse_schema_json_strict(load_schema_raw())
         binding = schema["source_binding"]
         self.assertEqual(
             binding["path"],
diff --git a/tools/obsidian_projection/rpe01_external_review_targeted_closure_qualification_v0_1.json b/tools/obsidian_projection/rpe01_external_review_targeted_closure_qualification_v0_1.json
new file mode 100644
index 0000000..c205019
--- /dev/null
+++ b/tools/obsidian_projection/rpe01_external_review_targeted_closure_qualification_v0_1.json
@@ -0,0 +1,96 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
+  "date": "2026-10-03",
+  "opening_head": "c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b",
+  "external_review_blob": "51b168dd9973b748e8e592093dc16497d2a42301",
+  "internal_adjudication_blob": "b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a",
+  "targeted_red_head": "0d680623b50a075024107443b14b638b1250e0d8",
+  "targeted_red_test_blob": "1691d7f74e430d65f00fd4603f6da51c23e75a52",
+  "targeted_red_report_blob": "425b8102389e134ef54f6ff95b03afa8a9d9ae8c",
+  "final_guard_blob": "82f4323316b95ea5895cdd0c6f0c68e801e595ca",
+  "p5e_schema_blob_unchanged": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
+  "final_main_test_blob": "cd0e091233e5a4473ef280c7061db8cf880169e9",
+  "final_mutation_sweep_test_blob": "a8baceaf4a921765ae0fdcb182bef7dd0eba1246",
+  "final_targeted_closure_test_blob": "1691d7f74e430d65f00fd4603f6da51c23e75a52",
+  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
+  "closure_results": {
+    "nb1_nb2_targeted_tests": "6/6 PASS",
+    "rpe01_main_plus_sweep_tests": "22/22 PASS",
+    "schema_mutation_sweep": {
+      "parsed_object_attempted": 433,
+      "raw_json_attempted": 7,
+      "attempted_total": 440,
+      "survivors": 0
+    },
+    "p5e_plus_rpe01_final_targeted_regression": "95/95 PASS",
+    "contract_diff_from_adopted_readiness_head": 0,
+    "model_diff_from_adopted_readiness_head": 0,
+    "p5d4_runtime_diff_from_adopted_readiness_head": 0
+  },
+  "nb1_closure": {
+    "status": "CLOSED_CANDIDATE",
+    "public_validation_api": "validate_governed_json(raw_document: str|bytes, raw_schema: str|bytes)",
+    "preparsed_schema_object_public_input_rejected": true,
+    "parsed_document_schema_validator_public_symbol_removed": true,
+    "all_current_rpe01_public_validation_tests_use_raw_schema": true,
+    "mutation_sweep_uses_raw_schema": true
+  },
+  "nb2_closure": {
+    "status": "CLOSED_CANDIDATE",
+    "value_error_normalized_to_governed_schema_error": true,
+    "recursion_error_normalized_to_governed_schema_error": true,
+    "pathological_integer_red_green_covered": true,
+    "pathological_nesting_red_green_covered": true
+  },
+  "nb6_evidence_hygiene": {
+    "status": "CLOSED_CANDIDATE",
+    "parsed_object_sweep_reported_separately": 433,
+    "raw_json_breakers_reported_separately": 7,
+    "raw_json_breaker_families": [
+      "duplicate top-level member",
+      "duplicate nested member",
+      "escaped duplicate decoded to same key",
+      "NaN",
+      "Infinity",
+      "-Infinity",
+      "duplicate raw schema member"
+    ],
+    "total_attempted": 440,
+    "survivors": 0
+  },
+  "nb7_packet_fidelity_policy": {
+    "status": "MUST_BE_VERIFIED_BY_DELTA_PACKET",
+    "historical_red_blob_is_reference_only_not_mislabeled_as_current_source": true,
+    "embedded_external_review_source_must_come_from_current_persisted_file": true,
+    "transformed_markdown_must_not_be_claimed_byte_identical": true,
+    "current_code_json_blob_identities_must_be_exact": true,
+    "exact_diff_required": true
+  },
+  "scope_clarifications": {
+    "nb3": "The concrete P5-E schema is structural/type/list governance. Existing P5-E value semantics remain guarded by adopted P5-E invariants. Future REAL P5-E authority flags should normally use schema-level const:false where the schema itself carries authority.",
+    "nb4": "Current source_binding and artifact_role are structurally validated but not dynamically enforced against expected role/source bytes by the generic guard. The current P5-E binding remains independently proven by Git blob evidence. Later RPE preregistrations must explicitly decide the binding enforcement boundary."
+  },
+  "remaining_nonblocking_debt": {
+    "nb5": [
+      "contradictory schema constraints may be rejected proactively in a future hardening",
+      "ASCII regex semantics may be enforced where required",
+      "isolated Unicode surrogates may be rejected where downstream UTF-8 persistence requires it"
+    ]
+  },
+  "real_state_fingerprints_unchanged": {
+    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
+    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
+    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
+  },
+  "claim_boundary": {
+    "rpe01_targeted_external_review_closure_qualified_for_delta_review": true,
+    "rpe01_human_adopted": false,
+    "rpe02_opened": false,
+    "real_p5e_authorized": false
+  },
+  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
+  "stop": true
+}
diff --git a/tools/obsidian_projection/rpe01_governed_closed_schema.py b/tools/obsidian_projection/rpe01_governed_closed_schema.py
index 3f61b91..82f4323 100644
--- a/tools/obsidian_projection/rpe01_governed_closed_schema.py
+++ b/tools/obsidian_projection/rpe01_governed_closed_schema.py
@@ -45,8 +45,10 @@ def parse_json_strict(raw: str | bytes) -> Any:
         )
     except GovernedSchemaError:
         raise
-    except json.JSONDecodeError as exc:
-        raise GovernedSchemaError(f"invalid governed JSON: {exc}") from exc
+    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
+        raise GovernedSchemaError(
+            f"invalid or unsupported governed JSON: {type(exc).__name__}: {exc}"
+        ) from exc


 def _exact_keys(label: str, value: object, allowed: set[str], required: set[str]) -> dict[str, Any]:
@@ -311,12 +313,15 @@ def parse_schema_json_strict(raw: str | bytes) -> dict[str, Any]:
     return validate_schema_definition(schema)


-def validate_document(document: object, schema: object) -> Any:
-    validated_schema = validate_schema_definition(schema)
+def _validate_document(document: object, validated_schema: dict[str, Any]) -> Any:
     _validate_document_node(document, validated_schema["root"], "$")
     return document


-def validate_governed_json(raw: str | bytes, schema: object) -> Any:
-    document = parse_json_strict(raw)
-    return validate_document(document, schema)
+def validate_governed_json(
+    raw_document: str | bytes,
+    raw_schema: str | bytes,
+) -> Any:
+    validated_schema = parse_schema_json_strict(raw_schema)
+    document = parse_json_strict(raw_document)
+    return _validate_document(document, validated_schema)

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: PERSISTED FIRST EXTERNAL REVIEW
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-CLAUDE-RETURN.md
Authoritative Git blob: 51b168dd9973b748e8e592093dc16497d2a42301
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
VERDICT = PASS_WITH_NON_BLOCKING_NOTES

J'ai reconstruit les artefacts code et JSON du paquet. Leurs identités correspondent toutes : garde `3f61b91…`, schéma P5-E `87e45cc…`, préregistration `406e67d…`, test GREEN `391663e…`, balayage `bad4959…`, qualification JSON `782e4ef…`, contrat adopté `43d2e45…`.

Ce que j'ai reproduit (OBSERVÉ) :

- 22/22 tests RPE-01 (21 dans le fichier GREEN + 1 balayage) ;
- 89/89 sur la régression ciblée P5-E + RPE-01, avec les tests P5-E du paquet précédent, dont les blobs sont inchangés ;
- 41 sondes adversariales sur le garde.

Rien ne contredit le critère de sortie N4 : toutes les clés ajoutées et tous les vecteurs de doublon ou de coercition sont rejetés sémantiquement, sans recours à la liaison de blob. Les notes ci-dessous sont des durcissements, dont un à faire avant que RPE-02 s'appuie sur le garde.

### BLOCKING_FINDINGS

Aucun.

### NON_BLOCKING_FINDINGS

**NB-1 — L'API accepte un schéma déjà parsé, ce qui laisse contourner la protection contre les doublons du schéma.** (OBSERVÉ ; à corriger avant que RPE-02 consomme le garde)

- Concerné : « RPE-01 GUARD IMPLEMENTATION », `validate_governed_json(raw, schema: object)` et `validate_document(document, schema: object)`.
- Le document est forcément parsé strictement, mais le schéma peut arriver sous forme d'objet déjà construit.
- Falsification : un schéma brut avec deux membres `"fields"`, où le dernier ajoute `"evaluation_override": {"kind": "boolean"}`. Chargé par `json.loads`, il donne un schéma élargi, et `validate_governed_json('{"a":1,"evaluation_override":true}', schema)` est ACCEPTÉ. Le même schéma passé par `parse_schema_json_strict` est rejeté.
- C'est l'usage naturel : le test de balayage lui-même charge le schéma avec `json.loads`.
- Correction minimale : n'accepter que des schémas bruts (`str | bytes`) dans l'API publique, ou n'accepter que des objets produits par le parseur strict (marqueur ou type dédié).

**NB-2 — Exceptions non normalisées.** (OBSERVÉ)

- Concerné : `parse_json_strict`.
- Un entier de 4500 chiffres lève `ValueError` (limite Python de conversion entier/chaîne). Une imbrication de 100 000 niveaux lève `RecursionError`.
- Le comportement reste fail-closed, mais ce ne sont pas des `GovernedSchemaError` : un appelant qui n'intercepte que `GovernedSchemaError` plantera au lieu de rejeter.
- Correction : intercepter `ValueError` et `RecursionError` et les convertir en `GovernedSchemaError`, éventuellement avec une borne explicite de profondeur et de taille.

**NB-3 — Le schéma P5-E est structurel, pas sémantique.** (OBSERVÉ)

- Concerné : « P5-E CONCRETE GOVERNED SCHEMA ».
- Contenu : 89 booléens sans `const`, 3 entiers sans bornes, 57 chaînes libres. Les sondes `evaluation_authorized: true` et `poll_interval_seconds: -5` sont ACCEPTÉES par le garde.
- C'est cohérent avec le périmètre N4 (clés, types, listes), puisque les valeurs restent gardées par `assert_contract_invariants`.
- La qualification devrait le dire explicitement, par exemple : « closed structure, values guarded by P5-E invariants ».
- Pour les futures configurations de runner, d'adaptateur et d'expérience, préregistrer que les drapeaux d'autorité utilisent `const: false` dans le schéma lui-même, pour que le garde porte l'autorité sans dépendre d'un second vérificateur.

**NB-4 — `source_binding` et `artifact_role` ne sont pas appliqués par le garde.** (OBSERVÉ)

- Le garde valide un contrat différent (`objective.purpose` modifié) contre un schéma lié à `43d2e45`. Le rôle n'est jamais comparé à un rôle attendu.
- La liaison n'est donc vérifiée que par `test_p5e_schema_source_binding_matches_current_contract_blob`.
- Recommandation : ajouter des paramètres `expected_role` et, si souhaité, une vérification de blob calculée de façon pure (`sha1("blob <n>\0" + octets)`). Attention à la normalisation des fins de ligne sous Windows (CRLF).

**NB-5 — Langage de schéma : contradictions et classes de caractères.** (OBSERVÉ)

- `const ∉ enum`, `ordered_const ∉ allowed_values` et `const` incompatible avec `pattern` sont acceptés à la définition du schéma. L'effet est restrictif : le schéma devient insatisfiable et tout document est rejeté. Fail-closed, mais détectable seulement par le test d'acceptation de référence.
- `pattern: "\\d"` accepte le chiffre arabe `٣`. Les 13 motifs actuels (`[0-9a-f]{40}\Z`) ne sont pas concernés. Recommandation : `re.ASCII`, ou interdire `\d`, `\w`, `\s`.
- Une surrogate isolée (`\ud800`) est acceptée dans une chaîne libre. Elle pourrait faire échouer plus tard l'écriture des preuves en UTF-8.

**NB-6 — Le balayage de 433 mutations ne couvre pas tous les opérateurs préregistrés.** (OBSERVÉ)

- Concerné : « RPE-01 MUTATION SWEEP TEST » face à `preregistration.mutation_sweep.operators`.
- Les opérateurs « duplicate selected raw JSON member names » et « inject NaN/Infinity constants » sont absents du balayage, qui ne mute que des objets parsés. Ils sont couverts seulement par des tests unitaires ponctuels (`test_duplicate_*`, `test_nan_and_infinities_are_rejected`).
- Le nombre 433 compte donc uniquement les opérateurs sur objets parsés.
- Le balayage charge aussi le schéma de façon permissive (voir NB-1).

**NB-7 — Fidélité du paquet.** (OBSERVÉ)

- La source « RPE-01 RED TEST » embarquée est en réalité le blob GREEN `391663e`. Le RED annoncé `803709c` n'est pas fourni.
- Les rapports Markdown ne correspondent pas à leurs blobs (RED `32e4335` contre `b3a7df3` annoncé ; qualification `1791df2` contre `83f17da`), probablement à cause de l'encodage mal converti (« â€” ») lors de la construction du paquet.
- Le code et les JSON correspondent tous.

### STRICT_JSON_CHECK

- **Question 1.** Les doublons sont rejetés avant construction du dictionnaire, à toutes les profondeurs, y compris l'orthographe échappée `\u0065valuation_authorized`, qui est décodée avant que le hook la voie. Rejeté (OBSERVÉ).
- **Question 2.** `NaN`, `Infinity` et `-Infinity` sont rejetés. `1e400` (lu comme `inf`) est rejeté aussi, parce qu'aucun type « nombre flottant » n'existe dans le langage de schéma.
- **Question 3.** Le décodage UTF-8 est strict : octets invalides et BOM sont rejetés.
- **Question 4.** Restent les exceptions non normalisées (NB-2) et les surrogates isolées (NB-5). Aucun blanchiment de type ou d'autorité.

### SCHEMA_LANGUAGE_CHECK

- **Question 5.** Le langage est fermé : une clé inconnue, un `kind` non supporté, un `min_items` de type `"1"` ou `True`, un `unique` à `"yes"` sont rejetés.
- **Question 6.** Entiers et booléens sont bien distingués via `type(x) is …` : `true` à la place d'un entier et `0` à la place d'un booléen sont rejetés, et `[True]` contre `ordered_const [1]` aussi.
- **Question 7.** Les flottants et la notation scientifique sont rejetés là où un entier est requis (`30.0` et `1e2` rejetés).
- **Question 8.** Unicité, `allowed_values` et `ordered_const` sont sains. L'ordre de validation (vocabulaire, puis ordre, puis type des éléments) n'ouvre aucune faille d'égalité `True == 1`.
- **Question 9.** Les contraintes contradictoires restreignent mais n'élargissent jamais (NB-5).
- **Question 10.** Le parsing strict du schéma brut suffit, à condition qu'il soit obligatoire, ce qu'il n'est pas aujourd'hui (NB-1).

### GUARD_AUTHORITY_CHECK

- **Question 11.** Le garde est pur : imports limités à `json`, `re` et `typing`, aucun accès à l'environnement, aux arguments CLI, au système de fichiers ou au réseau.
- **Question 12.** Aucun canal d'autorité. Seul risque : un déni de service par regex coûteuse, mais les motifs viennent d'un schéma gouverné.
- **Questions 13 et 29.** Un JSON brut explicite plus un schéma explicite constituent la bonne frontière. Garder le garde pur, sans aide de chargement de fichier, est plus sûr ; le chargement est la responsabilité de l'appelant gouverné.

### P5E_CONCRETE_SCHEMA_CHECK

- **Questions 14 et 15.** Les 17 objets sont fermés et toutes les clés sont requises : le balayage ajoute une clé inconnue à chaque objet et retire chaque clé requise.
- **Question 16.** Les types des feuilles sont figés. Les valeurs ne le sont pas, ce qui est voulu (NB-3).
- **Question 17.** Les 8 listes sont fermées : `allowed_values`, unicité, et `min_items == max_items` égal à la cardinalité actuelle.
- **Question 18.** L'ordre de `real_end_to_end_stages` est figé par `ordered_const`.
- **Question 19.** La liaison au blob `43d2e45` est correcte, mais elle n'est prouvée que par un test (NB-4).
- **Question 20.** Le schéma est rigide sur les listes (cardinalité exacte), donc tout amendement exige de modifier le schéma. C'est l'effet recherché, et ce n'est pas dangereux.

### MUTATION_SWEEP_CHECK

- **Questions 21 et 22.** Le balayage est suffisant pour N4. Il rejette par la sémantique du schéma (`validate_document`), sans aucune liaison de blob.
- **Question 23.** Opérateurs à ajouter :&#x20;
  - doublons bruts et constantes NaN/Infinity, intégrés au balayage plutôt qu'en tests unitaires isolés ;
  - remplacement d'une feuille par un objet ou un tableau ;
  - schéma élargi via un chargement permissif (NB-1).
- **Questions 24 et 25.** Aucune mutation ne survit du fait de travailler sur des objets parsés. Les familles « doublons bruts » et « NaN/Infinity » sont couvertes, mais de façon ponctuelle (NB-6).

### NF_D_ADJACENT_CONFIG_CHECK

- **Questions 26 et 27.** Le garde générique convient. Les clés d'autorité, d'override d'environnement et d'override CLI inconnues dans une configuration voisine sont rejetées (`test_unknown_adjacent_config_authority_keys_are_rejected`).
- **Question 28.** Empêcher que du code de runner ou d'adaptateur lise `os.environ` ou `argv` relève à juste titre d'une préregistration ultérieure (RPE-04, RPE-05). Un schéma ne peut pas l'imposer. Il faudra l'exiger par une analyse statique d'imports et d'usages dans ces étapes.

### BINDING_CHECK

- **Question 30.** Les identités du garde et du schéma sont liées dans la qualification JSON. Suffisant.
- **Question 31.** Les sémantiques du langage de schéma n'ont pas besoin d'un artefact séparé. Le blob du garde est leur identité, et la préregistration les décrit.
- **Question 32.** « Toute modification du garde ou du schéma exige une requalification » suffit à ce stade.
- **Question 33.** Aucune auto-référence : le schéma lie le contrat, la qualification lie le garde et le schéma.

### REGRESSION_CHECK

- **Question 34.** 89/89 est suffisant, et reproduit (OBSERVÉ).
- **Question 35.** Une suite Obsidian complète n'est pas nécessaire : le contrat, le modèle et le runtime D4 sont inchangés, et le garde n'a aucun consommateur runtime (INFÉRENCE).

### AUTHORITY_LEAKAGE_CHECK

- **Question 36.** Aucune fuite. Les drapeaux de la préregistration sont tous à false hors `implementation_authorized` (périmètre garde seulement). `rpe02_opened: false`, `real_p5e_authorized: false`.

### CLAIM_SCOPE_CHECK

- **Question 37.** La déclaration `QUALIFIED_FOR_EXTERNAL_REVIEW` est correctement bornée.
- Une imprécision : `qualified_properties` devrait préciser que le schéma P5-E est structurel (NB-3), et que la propriété « schema definition itself strictly parsed » n'est vraie que via `parse_schema_json_strict` (NB-1).

### RECOMMENDED_NEXT_ACTION

1. Une correction minimale ciblée, avant l'adjudication humaine ou au plus tard avant que RPE-02 consomme le garde :&#x20;
   - NB-1 : API acceptant uniquement un schéma brut, ou issu du parseur strict ;
   - NB-2 : normalisation des exceptions.
   &#x20;Ajouter les deux tests RED correspondants et faire une revue delta courte.
2. Intégrer NB-3 et NB-4 (`const` pour les drapeaux d'autorité, `expected_role`) comme exigences des préregistrations RPE-04, RPE-05 et RPE-06.
3. NB-5 à NB-7 : documentaire ou optionnel.

Cette revue ne vaut ni adoption humaine, ni ouverture de RPE-02, ni autorisation de P5-E réel.
~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: INTERNAL ADJUDICATION
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-INTERNAL-ADJUDICATION.md
Authoritative Git blob: b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
# RPE-01 — GOVERNED CLOSED SCHEMA — EXTERNAL REVIEW INTERNAL ADJUDICATION

Date: 2026-10-03

## External review result

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

`BLOCKING_FINDINGS = NONE`

The external reviewer reproduced:
- 22/22 RPE-01 tests;
- 89/89 targeted P5-E + RPE-01 regression;
- 41 additional adversarial probes.

The N4 exit criterion remains supported: added-key, duplicate-member, and coercion vectors are rejected semantically without relying on P5-E contract blob binding.

## Internal adjudication

```text
NB-1 = CONFIRMED / TARGETED CORRECTION REQUIRED BEFORE HUMAN ADOPTION
NB-2 = CONFIRMED / TARGETED CORRECTION REQUIRED BEFORE HUMAN ADOPTION
NB-3 = CONFIRMED / SCOPE CLARIFICATION + FUTURE RPE REQUIREMENT
NB-4 = CONFIRMED / NON-BLOCKING BINDING NOTE + FUTURE RPE REQUIREMENT
NB-5 = CONFIRMED / NON-BLOCKING HARDENING DEBT
NB-6 = CONFIRMED / EVIDENCE-HYGIENE CORRECTION IN TARGETED CLOSURE
NB-7 = CONFIRMED / PACKET-FIDELITY CORRECTION IN TARGETED CLOSURE
```

## NB-1 — parsed-schema bypass

Confirmed.

Current public API accepts:
`validate_governed_json(raw_document, schema_object)`

and:
`validate_document(document, schema_object)`

A caller may therefore parse raw schema JSON permissively before passing the resulting object to the guard, bypassing duplicate-member rejection in the schema source.

### Required targeted correction

The public validation surface must accept only raw schema bytes/text, or an unforgeable/explicitly validated schema handle produced by the strict parser.

Preferred minimal closure:

```text
validate_governed_json(raw_document, raw_schema)
`

where both inputs are `str | bytes`.

Internal parsed-object validation may remain private only.

All RPE-01 tests and the mutation sweep must consume the raw schema through this public path.

## NB-2 — exception normalization

Confirmed.

The strict parser may leak parser/runtime exceptions such as:
- `ValueError` for pathological integer conversion;
- `RecursionError` for pathological nesting.

These are fail-closed in effect but violate the API contract if callers catch only `GovernedSchemaError`.

### Required targeted correction

Normalize parser and recursive-validation failures into:
`GovernedSchemaError`

at the public boundary.

At minimum add RED coverage for:
- oversized integer conversion;
- pathological nesting.

## NB-3 — structural versus semantic scope

Confirmed and non-blocking.

The concrete P5-E governed schema is a structural/type/list guard, not a replacement for P5-E semantic invariants.

It intentionally does not freeze every existing boolean to `const`, every integer to its current value, or every free string to its exact current value.

The qualification must state explicitly:

`CLOSED STRUCTURE / STRICT TYPES / CLOSED NORMATIVE LISTS; P5-E VALUE SEMANTICS REMAIN GUARDED BY THE ADOPTED P5-E INVARIANTS.`

For future REAL P5-E configuration schemas, authority flags should normally be encoded as schema-level `const: false` where the schema itself is intended to carry the authority boundary.

This requirement is to be carried into RPE-04/RPE-05/RPE-06 preregistration.

## NB-4 — source binding and artifact role

Confirmed and non-blocking for RPE-01.

The current generic guard validates `source_binding` and `artifact_role` structurally but does not itself compare:
- artifact role against an externally expected role;
- source-binding blob against the bytes being validated.

Current P5-E binding is independently proven by the dedicated Git blob test and qualification identity.

For later governed runtime configuration artifacts, preregistration must decide whether pure expected-role/source-blob verification belongs in the generic guard API or in the governed caller boundary.

No silent claim is made that RPE-01 currently enforces source binding dynamically.

## NB-5 — schema-language hardening debt

Confirmed, non-blocking.

Contradictory constraints identified by the review are restrictive, not permissive; they fail closed.

Potential future hardening:
- reject contradictory `const/enum/pattern`;
- reject contradictory `ordered_const/allowed_values`;
- enforce ASCII regex semantics where required;
- reject isolated Unicode surrogates where downstream UTF-8 evidence persistence requires it.

These are not required to close N4.

## NB-6 — mutation-sweep evidence hygiene

Confirmed.

The 433-count sweep covers parsed-object mutation operators only.

Raw duplicate-member and NaN/Infinity families were covered by unit tests, not included in the sweep count.

The targeted closure must:
- route the mutation sweep through strict raw-schema parsing;
- add explicit raw duplicate-member and non-standard numeric-constant mutations to the reported sweep or clearly split the metrics into parsed-object sweep and raw-JSON breaker families.

The final evidence must not imply the 433 count covered operators it did not execute.

## NB-7 — packet fidelity

Confirmed.

The first external packet embedded:
- the current GREEN test under a RED-test source label rather than the historical RED blob;
- Markdown source text whose byte identity did not match the announced historical report blobs, likely due to encoding/newline transformation during packet assembly.

Code and JSON identities were correct.

The targeted delta packet must therefore:
- include the external review return exactly;
- include the historical RED evidence as immutable Git identity/reference rather than mislabeling a later file as the RED blob;
- distinguish verbatim embedded content from Git-identity references;
- avoid claiming byte identity for any transformed Markdown;
- include exact current code/JSON blobs and exact diff.

## Targeted closure authorization interpretation

The user's existing instruction was to execute the full RPE-01 block directly through test-first qualification and external review, stopping before human adoption.

NB-1/NB-2 are within the already-open RPE-01 scope and are required before human adoption/RPE-02 consumption.

Therefore the next technical step is a narrow RPE-01 external-review targeted closure:

1. RED for NB-1 and NB-2;
2. minimal guard/API correction;
3. update RPE-01 tests and sweep to use raw schema;
4. evidence-hygiene correction for NB-6/NB-7;
5. re-run RPE-01 targeted tests, mutation/raw-breaker sweep and targeted P5-E regression;
6. produce a short self-contained delta-review packet;
7. STOP before human adoption.

## Authority boundary

No authorization is created for:
- RPE-02;
- real timing model;
- ancestry classifier;
- remote adapter;
- timed runner;
- sandbox creation;
- real polling;
- real P5-E.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: TARGETED RED/GREEN TEST
Path: tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py
Authoritative Git blob: 1691d7f74e430d65f00fd4603f6da51c23e75a52
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
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
        depth = 5000
        pathological = ("[" * depth) + "0" + ("]" * depth)
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(pathological)


if __name__ == "__main__":
    unittest.main()

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: TARGETED RED REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-NB1-NB2-TARGETED-CLOSURE-RED.md
Authoritative Git blob: 425b8102389e134ef54f6ff95b03afa8a9d9ae8c
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
# RPE-01 — NB-1 / NB-2 TARGETED CLOSURE — RED EVIDENCE

Date: 2026-10-03

## Opening identity

Branch:
`feat/obsidian-projection-rpe01-governed-closed-schema-v0.1`

Opening HEAD:
`c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b`

External review:
`PASS_WITH_NON_BLOCKING_NOTES`

External review blob:
`51b168dd9973b748e8e592093dc16497d2a42301`

Internal adjudication blob:
`b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a`

Guard blob before targeted closure:
`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`

## RED test

`tests/obsidian_projection/test_rpe01_external_review_targeted_closure_v0_1.py`

The test was written before modifying the guard.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_external_review_targeted_closure_v0_1
```

## Observed result

```text
Ran 6 tests in 0.043s

FAILED (failures=2, errors=3)

TARGETED_RED_EXIT=1
```

One test passed; five produced the required RED signal.

## NB-1 reproduced

Observed before patch:

1. A legitimate raw schema passed directly to `validate_governed_json` fails because the API expects an already parsed object.
2. A permissively pre-parsed schema object is accepted by `validate_governed_json`.
3. The parsed-object helper `validate_document` remains publicly exposed.
4. The raw duplicate-schema-member attack is already rejected when strict raw parsing is actually used.

Therefore the defect is specifically the public API path allowing a parsed schema object.

## NB-2 reproduced

Observed before patch:

### Pathological integer

A JSON integer containing 5000 digits raises:

`ValueError`

from Python's integer-string conversion limit.

It is not normalized to:

`GovernedSchemaError`

### Pathological nesting

A JSON array nested 5000 levels deep raises:

`RecursionError`

from the JSON decoder.

It is not normalized to:

`GovernedSchemaError`

Both behaviors remain fail-closed in effect but violate the guard's intended single exception contract.

## Targeted correction boundary

The RED authorizes only the already-adjudicated minimal closure:

- public `validate_governed_json(document_raw, schema_raw)`;
- reject parsed schema objects at the public boundary;
- remove/privatize the parsed document/schema bypass;
- normalize `ValueError` and `RecursionError` into `GovernedSchemaError`;
- update existing RPE-01 tests/sweep to use raw schema input;
- correct NB-6/NB-7 evidence hygiene.

No semantic P5-E contract/model/runtime modification is authorized.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL GUARD
Path: tools/obsidian_projection/rpe01_governed_closed_schema.py
Authoritative Git blob: 82f4323316b95ea5895cdd0c6f0c68e801e595ca
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
from __future__ import annotations

import json
import re
from typing import Any


SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
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


def validate_schema_definition(schema: object) -> dict[str, Any]:
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
    validated_schema = parse_schema_json_strict(raw_schema)
    document = parse_json_strict(raw_document)
    return _validate_document(document, validated_schema)

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: UNCHANGED P5-E GOVERNED SCHEMA
Path: tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json
Authoritative Git blob: 87e45cc75753439879e2902d3cbdbd5d71d8a1b2
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
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

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL MAIN RPE-01 TEST
Path: tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
Authoritative Git blob: cd0e091233e5a4473ef280c7061db8cf880169e9
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
import ast
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
P5E_SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
P5E_CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
P5E_ADV_PATH = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"


def load_module(path: Path, name: str):
    if not path.exists():
        raise AssertionError(f"required implementation missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_guard():
    return load_module(GUARD_PATH, "rpe01_guard_under_test")


def load_schema_raw():
    if not P5E_SCHEMA_PATH.exists():
        raise AssertionError(f"required governed schema missing: {P5E_SCHEMA_PATH}")
    return P5E_SCHEMA_PATH.read_text(encoding="utf-8")


def synthetic_schema_raw():
    return json.dumps(synthetic_schema(), separators=(",", ":"))


def current_contract_raw() -> str:
    return P5E_CONTRACT_PATH.read_text(encoding="utf-8")


def synthetic_schema():
    return {
        "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
        "artifact_role": "RPE01_SYNTHETIC_ADJACENT_CONFIG",
        "root": {
            "kind": "object",
            "fields": {
                "interval_ns": {
                    "kind": "integer",
                    "minimum": 1,
                    "maximum": 60_000_000_000,
                },
                "enabled": {"kind": "boolean", "const": False},
                "mode": {
                    "kind": "string",
                    "enum": ["FIXED_RATE", "DISABLED"],
                },
                "stages": {
                    "kind": "array",
                    "items": {"kind": "string"},
                    "min_items": 2,
                    "max_items": 2,
                    "unique": True,
                    "ordered_const": ["OBSERVE", "STOP"],
                },
            },
        },
    }


class ExistingGapEvidenceTests(unittest.TestCase):
    def test_existing_p5e_invariants_do_not_close_unknown_keys(self):
        adv = load_module(P5E_ADV_PATH, "rpe01_gap_adv")
        contract = json.loads(current_contract_raw())
        mutated = copy.deepcopy(contract)
        mutated["authority_boundary"]["rpe01_probe_unknown_authority"] = True
        # This PASS demonstrates the pre-RPE01 structural gap.
        adv.assert_contract_invariants(mutated)


class StrictRawJsonTests(unittest.TestCase):
    def test_duplicate_authority_member_is_rejected_before_dict_construction(self):
        g = load_guard()
        raw = '{"evaluation_authorized":true,"evaluation_authorized":false}'
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(raw)

    def test_duplicate_nested_member_is_rejected(self):
        g = load_guard()
        raw = '{"outer":{"x":1,"x":2}}'
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(raw)

    def test_nan_and_infinities_are_rejected(self):
        g = load_guard()
        for raw in ('{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(raw=raw):
                with self.assertRaises(g.GovernedSchemaError):
                    g.parse_json_strict(raw)


class SchemaDefinitionTests(unittest.TestCase):
    def test_schema_definition_rejects_unknown_schema_language_key(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["surprise"] = True
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)

    def test_schema_definition_rejects_wrong_constraint_type(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["fields"]["interval_ns"]["minimum"] = "1"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)

    def test_schema_definition_rejects_unsupported_kind(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["fields"]["interval_ns"]["kind"] = "number"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)

    def test_raw_schema_duplicate_member_and_nan_are_rejected(self):
        g = load_guard()
        duplicate = '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1","artifact_role":"A","artifact_role":"B","root":{"kind":"null"}}'
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_schema_json_strict(duplicate)
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_schema_json_strict('{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1","artifact_role":"A","root":{"kind":"integer","minimum":NaN}}')


class StrictTypeAndListTests(unittest.TestCase):
    def assert_rejected(self, document):
        g = load_guard()
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(document), synthetic_schema_raw())

    def test_float_and_scientific_float_where_integer_required_are_rejected(self):
        self.assert_rejected({"interval_ns": 30.0, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
        g = load_guard()
        raw = '{"interval_ns":1e2,"enabled":false,"mode":"FIXED_RATE","stages":["OBSERVE","STOP"]}'
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(raw, synthetic_schema_raw())

    def test_boolean_where_integer_required_is_rejected(self):
        self.assert_rejected({"interval_ns": True, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})

    def test_integer_where_boolean_required_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": 0, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})

    def test_unknown_enum_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "COALESCE", "stages": ["OBSERVE", "STOP"]})

    def test_duplicate_list_member_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "OBSERVE"]})

    def test_normative_order_change_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["STOP", "OBSERVE"]})

    def test_unknown_adjacent_config_authority_keys_are_rejected(self):
        base = {"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]}
        for key in ("evaluation_authorized", "environment_override", "cli_override"):
            with self.subTest(key=key):
                mutated = dict(base)
                mutated[key] = True
                self.assert_rejected(mutated)


class P5EConcreteSchemaTests(unittest.TestCase):
    def test_adopted_contract_is_accepted_without_byte_mutation(self):
        g = load_guard()
        schema_raw = load_schema_raw()
        doc = g.validate_governed_json(current_contract_raw(), schema_raw)
        self.assertEqual(doc["schema"], "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1")

    def test_unknown_keys_at_representative_depths_are_rejected(self):
        g = load_guard()
        schema_raw = load_schema_raw()
        contract = json.loads(current_contract_raw())
        paths = [
            (),
            ("authority_boundary",),
            ("near_real_time_timing",),
            ("queue_and_supersession",),
            ("external_review_targeted_closure", "findings"),
        ]
        for path in paths:
            with self.subTest(path=path):
                mutated = copy.deepcopy(contract)
                node = mutated
                for key in path:
                    node = node[key]
                node["rpe01_unknown_key"] = True
                with self.assertRaises(g.GovernedSchemaError):
                    g.validate_governed_json(json.dumps(mutated), schema_raw)

    def test_missing_required_key_is_rejected(self):
        g = load_guard()
        schema_raw = load_schema_raw()
        contract = json.loads(current_contract_raw())
        del contract["authority_boundary"]["evaluation_authorized"]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(contract), schema_raw)

    def test_normative_list_duplicate_unknown_and_order_change_are_rejected(self):
        g = load_guard()
        schema_raw = load_schema_raw()
        contract = json.loads(current_contract_raw())

        duplicate = copy.deepcopy(contract)
        duplicate["claim_boundary"]["forbidden_current_claims"][1] = duplicate["claim_boundary"]["forbidden_current_claims"][0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(duplicate), schema_raw)

        unknown = copy.deepcopy(contract)
        unknown["required_synthetic_cases"][0] = "RPE01_UNKNOWN_CASE"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(unknown), schema_raw)

        reordered = copy.deepcopy(contract)
        stages = reordered["end_to_end_definition"]["real_end_to_end_stages"]
        stages[0], stages[1] = stages[1], stages[0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(reordered), schema_raw)


class SchemaBindingTests(unittest.TestCase):
    def test_p5e_schema_source_binding_matches_current_contract_blob(self):
        import subprocess

        g = load_guard()
        schema = g.parse_schema_json_strict(load_schema_raw())
        binding = schema["source_binding"]
        self.assertEqual(
            binding["path"],
            "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
        )
        actual = subprocess.check_output(
            [
                "git",
                "hash-object",
                "--path=" + binding["path"],
                binding["path"],
            ],
            cwd=ROOT,
            text=True,
        ).strip()
        self.assertEqual(actual, binding["git_blob"])


class GuardPurityTests(unittest.TestCase):
    def test_guard_source_has_no_implicit_authority_channels(self):
        if not GUARD_PATH.exists():
            self.fail(f"required implementation missing: {GUARD_PATH}")
        source = GUARD_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_import_roots = {
            "argparse", "os", "socket", "subprocess", "sys", "urllib",
            "requests", "httpx",
        }
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported.isdisjoint(forbidden_import_roots), imported & forbidden_import_roots)
        for forbidden_text in ("os.environ", "sys.argv", "input(", "open(", ".read_text(", ".read_bytes("):
            self.assertNotIn(forbidden_text, source)


if __name__ == "__main__":
    unittest.main()

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: FINAL MUTATION SWEEP
Path: tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
Authoritative Git blob: a8baceaf4a921765ae0fdcb182bef7dd0eba1246
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
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

    def expect_raw_reject(label, raw_document, raw_schema=None):
        nonlocal raw_json_attempted
        raw_json_attempted += 1
        try:
            guard.validate_governed_json(
                raw_document,
                schema_raw if raw_schema is None else raw_schema,
            )
        except guard.GovernedSchemaError:
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

    # Raw JSON breaker families preregistered separately from parsed-object mutations.
    expect_raw_reject("RAW_DUPLICATE_TOP_LEVEL", '{"x":1,"x":2}')
    expect_raw_reject("RAW_DUPLICATE_NESTED", '{"outer":{"x":1,"x":2}}')
    expect_raw_reject(
        "RAW_ESCAPED_DUPLICATE",
        '{"evaluation_authorized":true,"\u0065valuation_authorized":false}',
    )
    expect_raw_reject("RAW_NAN", '{"x":NaN}')
    expect_raw_reject("RAW_POSITIVE_INFINITY", '{"x":Infinity}')
    expect_raw_reject("RAW_NEGATIVE_INFINITY", '{"x":-Infinity}')
    duplicate_schema = (
        '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
        '"artifact_role":"A","artifact_role":"B",'
        '"root":{"kind":"null"}}'
    )
    expect_raw_reject("RAW_SCHEMA_DUPLICATE_MEMBER", 'null', duplicate_schema)

    return {
        "parsed_object_attempted": parsed_object_attempted,
        "raw_json_attempted": raw_json_attempted,
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


if __name__ == "__main__":
    result = run_sweep()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["survivor_count"] == 0 else 1)

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: TARGETED CLOSURE QUALIFICATION JSON
Path: tools/obsidian_projection/rpe01_external_review_targeted_closure_qualification_v0_1.json
Authoritative Git blob: c20501938569de38de3190982d3dc97b49154904
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW",
  "date": "2026-10-03",
  "opening_head": "c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b",
  "external_review_blob": "51b168dd9973b748e8e592093dc16497d2a42301",
  "internal_adjudication_blob": "b6bf8eabfeefff2e264ae0b0d957b1492d2a0c5a",
  "targeted_red_head": "0d680623b50a075024107443b14b638b1250e0d8",
  "targeted_red_test_blob": "1691d7f74e430d65f00fd4603f6da51c23e75a52",
  "targeted_red_report_blob": "425b8102389e134ef54f6ff95b03afa8a9d9ae8c",
  "final_guard_blob": "82f4323316b95ea5895cdd0c6f0c68e801e595ca",
  "p5e_schema_blob_unchanged": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
  "final_main_test_blob": "cd0e091233e5a4473ef280c7061db8cf880169e9",
  "final_mutation_sweep_test_blob": "a8baceaf4a921765ae0fdcb182bef7dd0eba1246",
  "final_targeted_closure_test_blob": "1691d7f74e430d65f00fd4603f6da51c23e75a52",
  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
  "closure_results": {
    "nb1_nb2_targeted_tests": "6/6 PASS",
    "rpe01_main_plus_sweep_tests": "22/22 PASS",
    "schema_mutation_sweep": {
      "parsed_object_attempted": 433,
      "raw_json_attempted": 7,
      "attempted_total": 440,
      "survivors": 0
    },
    "p5e_plus_rpe01_final_targeted_regression": "95/95 PASS",
    "contract_diff_from_adopted_readiness_head": 0,
    "model_diff_from_adopted_readiness_head": 0,
    "p5d4_runtime_diff_from_adopted_readiness_head": 0
  },
  "nb1_closure": {
    "status": "CLOSED_CANDIDATE",
    "public_validation_api": "validate_governed_json(raw_document: str|bytes, raw_schema: str|bytes)",
    "preparsed_schema_object_public_input_rejected": true,
    "parsed_document_schema_validator_public_symbol_removed": true,
    "all_current_rpe01_public_validation_tests_use_raw_schema": true,
    "mutation_sweep_uses_raw_schema": true
  },
  "nb2_closure": {
    "status": "CLOSED_CANDIDATE",
    "value_error_normalized_to_governed_schema_error": true,
    "recursion_error_normalized_to_governed_schema_error": true,
    "pathological_integer_red_green_covered": true,
    "pathological_nesting_red_green_covered": true
  },
  "nb6_evidence_hygiene": {
    "status": "CLOSED_CANDIDATE",
    "parsed_object_sweep_reported_separately": 433,
    "raw_json_breakers_reported_separately": 7,
    "raw_json_breaker_families": [
      "duplicate top-level member",
      "duplicate nested member",
      "escaped duplicate decoded to same key",
      "NaN",
      "Infinity",
      "-Infinity",
      "duplicate raw schema member"
    ],
    "total_attempted": 440,
    "survivors": 0
  },
  "nb7_packet_fidelity_policy": {
    "status": "MUST_BE_VERIFIED_BY_DELTA_PACKET",
    "historical_red_blob_is_reference_only_not_mislabeled_as_current_source": true,
    "embedded_external_review_source_must_come_from_current_persisted_file": true,
    "transformed_markdown_must_not_be_claimed_byte_identical": true,
    "current_code_json_blob_identities_must_be_exact": true,
    "exact_diff_required": true
  },
  "scope_clarifications": {
    "nb3": "The concrete P5-E schema is structural/type/list governance. Existing P5-E value semantics remain guarded by adopted P5-E invariants. Future REAL P5-E authority flags should normally use schema-level const:false where the schema itself carries authority.",
    "nb4": "Current source_binding and artifact_role are structurally validated but not dynamically enforced against expected role/source bytes by the generic guard. The current P5-E binding remains independently proven by Git blob evidence. Later RPE preregistrations must explicitly decide the binding enforcement boundary."
  },
  "remaining_nonblocking_debt": {
    "nb5": [
      "contradictory schema constraints may be rejected proactively in a future hardening",
      "ASCII regex semantics may be enforced where required",
      "isolated Unicode surrogates may be rejected where downstream UTF-8 persistence requires it"
    ]
  },
  "real_state_fingerprints_unchanged": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "claim_boundary": {
    "rpe01_targeted_external_review_closure_qualified_for_delta_review": true,
    "rpe01_human_adopted": false,
    "rpe02_opened": false,
    "real_p5e_authorized": false
  },
  "next_gate": "SHORT_EXTERNAL_DELTA_REVIEW_THEN_HUMAN_ADJUDICATION",
  "stop": true
}

~~~~

# GIT-BLOB-SOURCED DISPLAY COPY: TARGETED CLOSURE QUALIFICATION REPORT
Path: reports/program/2026-10-03-OBSIDIAN-REAL-P5E-RPE01-EXTERNAL-REVIEW-TARGETED-CLOSURE-QUALIFICATION.md
Authoritative Git blob: b08d02c479631824261556ef23b2f04d29587daa
Display copy below is normalized for line endings/trailing whitespace and is NOT claimed byte-identical.
~~~~
# RPE-01 — EXTERNAL REVIEW TARGETED CLOSURE — QUALIFICATION

Date: 2026-10-03

## Result

```text
RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

REAL_P5E
= CLOSED
```

## External-review origin

The first independent RPE-01 review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with:

`BLOCKING_FINDINGS = NONE`

The reviewer reproduced:
- 22/22 RPE-01 tests;
- 89/89 targeted P5-E + RPE-01 regression;
- 41 additional adversarial probes.

Two notes were adjudicated as targeted corrections required before human adoption / before RPE-02 consumes the guard:

- NB-1 — parsed-schema bypass;
- NB-2 — non-normalized parser exceptions.

NB-6 and NB-7 were accepted as evidence-hygiene corrections for this closure.

## RED

Opening HEAD:
`c9e8ad98aeee6b4ae9346dac554fc599abfe1a8b`

Targeted RED commit:
`0d680623b50a075024107443b14b638b1250e0d8`

Targeted RED test blob:
`1691d7f74e430d65f00fd4603f6da51c23e75a52`

Targeted RED report blob:
`425b8102389e134ef54f6ff95b03afa8a9d9ae8c`

Observed before correction:

```text
Ran 6 tests

FAILED
failures = 2
errors = 3
1 test passed
```

RED demonstrated:
- legitimate raw schema not accepted by public API;
- pre-parsed schema object accepted by public API;
- parsed document/schema bypass still publicly exposed;
- pathological integer leaks ValueError;
- pathological nesting leaks RecursionError.

## NB-1 closure

Final guard blob:
`82f4323316b95ea5895cdd0c6f0c68e801e595ca`

Public API is now:

```text
validate_governed_json(
    raw_document: str | bytes,
    raw_schema: str | bytes,
)
```

The public API strictly parses the schema itself before parsing/validating the document.

A pre-parsed schema dictionary is rejected.

The former public:
`validate_document(document, schema)`

no longer exists.

The internal parsed-document validator is private:

`_validate_document(...)`

and receives an already strictly validated schema only from the raw public path.

Existing RPE-01 tests and the mutation sweep now send the concrete P5-E schema as raw JSON.

## NB-2 closure

`parse_json_strict` now normalizes:

- `ValueError`;
- `RecursionError`;
- `json.JSONDecodeError`;

into:

`GovernedSchemaError`

while preserving existing direct `GovernedSchemaError` failures.

Dedicated RED→GREEN cases cover:
- a 5000-digit integer;
- 5000-level array nesting.

The guard remains fail-closed with one public exception family for these parser failure modes.

## GREEN

Targeted NB-1/NB-2 tests:

```text
6 / 6 PASS
```

Current RPE-01 main + mutation-sweep unittest surface:

```text
22 / 22 PASS
```

## NB-6 — corrected sweep accounting

The previous reported count `433` represented parsed-object mutations only.

The final sweep now reports separately:

```text
PARSED-OBJECT MUTATIONS = 433
RAW-JSON BREAKERS       = 7
TOTAL                    = 440
SURVIVORS                = 0
```

Raw breaker families now executed inside the sweep:

- duplicate top-level member;
- duplicate nested member;
- escaped key duplicate that decodes to the same member;
- NaN;
- Infinity;
- -Infinity;
- duplicate member in raw schema JSON.

The sweep itself uses the raw concrete schema through the strict public API.

Therefore no claim is made that the original 433 count covered raw JSON operators.

## Final targeted regression

Current P5-E qualification surface + RPE-01 + targeted closure:

```text
95 / 95 PASS
```

Relative to the adopted readiness base:

```text
P5-E contract diff = 0
P5-E model diff = 0
P5-D4 runtime diff = 0
```

No full Obsidian suite was run.

## NB-3 — explicit scope clarification

The concrete P5-E governed schema is:

`STRUCTURAL + STRICT-TYPE + CLOSED-NORMATIVE-LIST`

It is not a replacement for the adopted P5-E semantic invariant layer.

Therefore values such as existing authorization booleans, timing integers, and free descriptive strings are not all frozen to their current literal value by this schema.

Existing P5-E value semantics remain guarded by the adopted P5-E invariants.

For future REAL P5-E configuration schemas, an authority flag should normally be encoded as schema-level `const: false` when the schema itself is intended to carry that authority boundary.

This requirement is carried forward to the preregistrations that define RPE-04/RPE-05/RPE-06 configuration surfaces.

## NB-4 — explicit binding limitation

The generic guard validates the structure of:
- `artifact_role`;
- `source_binding`.

It does not currently receive an externally expected role or recompute the Git source blob as part of generic validation.

For the current P5-E schema, source binding remains independently demonstrated by the dedicated Git blob test and qualification evidence.

No claim is made that dynamic source-binding enforcement is already part of the generic RPE-01 guard.

Later REAL P5-E preregistrations must decide explicitly whether expected-role/source-byte binding belongs in the guard API or at the governed caller boundary.

## NB-5 — retained non-blocking hardening debt

The following remain non-blocking future hardening:
- proactively reject contradictory restrictive schema constraints;
- require ASCII regex semantics where a future schema relies on character classes;
- reject isolated Unicode surrogates where downstream UTF-8 evidence persistence requires it.

These do not reopen N4.

## NB-7 — packet-fidelity rule for the next delta packet

The next packet must:
- identify the historical RED only by its exact immutable Git identity/reference unless its exact historical bytes are deliberately extracted;
- not label the current GREEN test as the historical RED source;
- not claim transformed Markdown to be byte-identical to historical report blobs;
- embed the persisted external review from its current canonical file;
- bind exact current code/JSON blobs;
- include an exact Git diff for the targeted closure.

## Final candidate identities

```text
GUARD
= 82f4323316b95ea5895cdd0c6f0c68e801e595ca

P5-E GOVERNED SCHEMA
= 87e45cc75753439879e2902d3cbdbd5d71d8a1b2

MAIN RPE-01 TEST
= cd0e091233e5a4473ef280c7061db8cf880169e9

MUTATION SWEEP TEST
= a8baceaf4a921765ae0fdcb182bef7dd0eba1246

TARGETED CLOSURE TEST
= 1691d7f74e430d65f00fd4603f6da51c23e75a52
```

## Real-state integrity

P5-D4 real state remains unchanged:

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Maximum claim

```text
NB-1
= CLOSED_CANDIDATE

NB-2
= CLOSED_CANDIDATE

NB-6
= EVIDENCE_ACCOUNTING_CORRECTED

NB-7
= DELTA_PACKET_FIDELITY_REQUIREMENT_ACTIVE

RPE01_EXTERNAL_REVIEW_TARGETED_CLOSURE
= QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE-02
= CLOSED

REAL_P5E
= CLOSED
```

~~~~
