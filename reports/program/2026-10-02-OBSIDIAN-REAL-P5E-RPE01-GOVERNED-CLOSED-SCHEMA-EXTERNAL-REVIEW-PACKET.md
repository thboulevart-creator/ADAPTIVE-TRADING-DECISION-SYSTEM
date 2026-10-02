# RPE-01 — N4 GOVERNED CLOSED SCHEMA — SELF-CONTAINED EXTERNAL REVIEW PACKET

Date: 2026-10-02

## Independent reviewer mandate

Review the RPE-01 candidate only.

Current adopted predecessor:

`REAL_P5E_PRE_EXECUTION_READINESS_V0_2 = QUALIFIED_AND_HUMAN_ADOPTED`

Current candidate claim:

`RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE = QUALIFIED_FOR_EXTERNAL_REVIEW`

This review does not authorize human adoption, RPE-02, or REAL P5-E.

## Identity

Adopted readiness base HEAD:
`d904eb61d9b704dc8ac38da445eb1cd491a58b33`

RPE-01 candidate HEAD:
`c9ab17b4c0004abace4c02b560e052559dbe14a6`

Preregistration blob:
`406e67da3ab197c5a9ae4b3e971368549af6e1da`

RED test blob:
`803709c26769fc9889b4ac1e47c0dd8df2782580`

RED report blob:
`b3a7df32198fd5a618f927c83d04d5f3a6491050`

Guard blob:
`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`

Concrete P5-E schema blob:
`87e45cc75753439879e2902d3cbdbd5d71d8a1b2`

Green test blob:
`391663ee2b8634c0221b5352c8d1242bfdb3c04e`

Mutation sweep test blob:
`bad495950ddce5c171cac4c667e40654c6673724`

Qualification JSON blob:
`782e4efb6986de13da2b001c49eb2b98273c51a2`

Qualification report blob:
`83f17dac6db42156ecaad2b8ea9ab3bfcb920662`

Adopted P5-E contract:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted P5-E synthetic model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

## Claimed evidence

```text
RED:
19 tests, failed as expected;
1 intentional PASS demonstrated the existing unknown-key gap.

GREEN:
22 / 22 PASS

SCHEMA MUTATION SWEEP:
433 attempted
0 survivors

P5-E + RPE-01 TARGETED REGRESSION:
89 / 89 PASS

P5-E CONTRACT DIFF:
0

P5-E MODEL DIFF:
0

P5-D4 RUNTIME DIFF:
0
```

## Review questions

### Strict raw JSON parser

1. Does duplicate-member rejection occur before dictionary construction at every object depth?
2. Are NaN, Infinity and -Infinity fail-closed?
3. Is UTF-8 decoding strict?
4. Is any permissive JSON behavior left that could launder type/authority semantics?

### Schema language

5. Is the schema language itself strictly closed against unknown schema-language keys?
6. Are integer and boolean types distinguished correctly despite Python bool subclassing int?
7. Are floats/scientific notation rejected where integer is required?
8. Are array uniqueness, closed allowed-values and ordered-const semantics sound?
9. Can malformed or contradictory schema constraints widen validation?
10. Is strict parsing of raw schema JSON sufficient to close duplicate-member attacks on the schema itself?

### Guard authority surface

11. Is the implementation genuinely pure with respect to environment, CLI, filesystem discovery, network and runtime state?
12. Does any imported module or built-in allow an unintended authority channel?
13. Is explicit raw JSON + explicit schema an appropriate authority boundary for later REAL P5-E configurations?

### Concrete P5-E schema

14. Does it close every current object depth of the adopted P5-E contract?
15. Are all current keys required?
16. Are current leaf JSON types frozen correctly?
17. Are normative lists closed and unique?
18. Is `real_end_to_end_stages` order correctly frozen?
19. Is the source binding to the adopted contract blob correct and sufficient as evidence?
20. Is the concrete schema over-constrained or under-constrained in a way that would make future governed amendments unsafe or impractical?

### Mutation sweep

21. Is the 433-mutation sweep broad enough to support the N4 exit criterion?
22. Does it genuinely reject mutations by schema semantics rather than P5-E contract blob binding?
23. Which additional mutation operators would materially test a distinct failure mode?
24. Could any mutation survive because the sweep mutates parsed objects rather than raw JSON bytes?
25. Are duplicate raw-member and NaN/Infinity families sufficiently covered outside the parsed-object sweep?

### NF-D / adjacent configurations

26. Does the generic guard capability adequately support future guarded adapter/runner/experiment/evidence JSON?
27. Is rejection of unknown adjacent-config authority/environment/CLI override keys demonstrated?
28. Is more needed in RPE-01 itself to ensure future runner/adapter code cannot consume environment/CLI authority outside guarded artifacts, or is that correctly a later-stage preregistration requirement?
29. Should the guard expose any path/file-loading helper, or is keeping it pure/raw-input-only safer?

### Binding and governance

30. Does the qualification bind the exact guard and P5-E schema identities strongly enough?
31. Must the guard's own schema-language semantics be represented in a separate governed artifact rather than code?
32. Is "any guard or schema change requires requalification" sufficient for this stage?
33. Is any hidden self-reference or circular binding present?

### Regression / claims

34. Is 89/89 targeted regression sufficient for this isolated structural guard stage?
35. Is a full Obsidian suite unnecessary here?
36. Does the candidate accidentally open RPE-02 or any REAL P5-E authority?
37. Is the maximum claim correctly limited to RPE-01 qualified-for-review?

## Required adversarial mandate

Try to falsify at least:

- duplicate top-level member;
- duplicate nested authority member;
- escaped duplicate key spelling that normalizes to same decoded key;
- NaN / Infinity / -Infinity;
- 30.0 and 1e2 where integer is required;
- true where integer is required;
- 0 where boolean is required;
- unknown object key at every depth;
- missing required object key;
- unknown enum;
- duplicate list member;
- unknown list member;
- normative list reorder;
- schema-language unknown key;
- schema-language duplicate raw key;
- schema-language wrong constraint type;
- invalid regex;
- min/max contradiction;
- min_items/max_items contradiction;
- ordered_const violating min/max;
- adjacent config carrying evaluation/promotion/environment/CLI authority;
- contract/schema binding drift;
- schema mutation that attempts to widen allowed keys;
- any use of object binding as a substitute for semantic schema rejection.

## Required output

Return exactly one:

`VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL`

Then provide:

- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- STRICT_JSON_CHECK
- SCHEMA_LANGUAGE_CHECK
- GUARD_AUTHORITY_CHECK
- P5E_CONCRETE_SCHEMA_CHECK
- MUTATION_SWEEP_CHECK
- NF_D_ADJACENT_CONFIG_CHECK
- BINDING_CHECK
- REGRESSION_CHECK
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_NEXT_ACTION

For every finding:
- distinguish OBSERVED from INFERENCE;
- cite exact packet section / function / schema path / test;
- state BLOCKING or NON_BLOCKING;
- give a minimal falsification case where possible.

This review creates no authority.

`RPE-02 = CLOSED`

`REAL_P5E = CLOSED`

---

# EXACT DIFF — ADOPTED READINESS BASE TO RPE-01 CANDIDATE
~~~~diff
diff --git a/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-PREDRAFT.md b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-PREDRAFT.md
new file mode 100644
index 0000000..e74b8dd
--- /dev/null
+++ b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-PREDRAFT.md
@@ -0,0 +1,152 @@
+# RPE-01 ÔÇö N4 GOVERNED CLOSED SCHEMA ÔÇö PRE-DRAFT
+
+Date: 2026-10-02
+
+## Objective
+
+Qualify a reusable, fail-closed JSON schema guard before any later REAL P5-E stage introduces adapter, runner, experiment, or evidence configuration.
+
+RPE-01 closes the structural failure mode identified by N4/NF-D:
+
+> authority must not enter through an unknown key, duplicate key, permissive numeric parsing, list laundering, or an adjacent ungoverned configuration source.
+
+## Starting authority
+
+Base HEAD:
+`d904eb61d9b704dc8ac38da445eb1cd491a58b33`
+
+Readiness V0.2:
+`QUALIFIED_AND_HUMAN_ADOPTED`
+
+RPE-01 is the only implementation stage opened by the current user instruction.
+
+All later RPE stages remain closed.
+
+## Architecture
+
+The guard is a pure boundary:
+
+```text
+explicit raw JSON bytes/text
+        +
+explicit governed schema
+        Ôåô
+strict parser
+        Ôåô
+closed recursive schema validator
+        Ôåô
+VALIDATED DOCUMENT
+or
+FAIL-CLOSED
+```
+
+The guard does not discover configuration.
+
+It must not read:
+- environment variables;
+- CLI arguments;
+- Git configuration;
+- network state;
+- P5-D4 control state;
+- Vault/CURRENT state.
+
+This makes configuration provenance the caller's explicit responsibility and prevents the guard itself from becoming an alternate authority channel.
+
+## Strict parser requirements
+
+Before dictionary construction:
+- reject duplicate object member names;
+- reject `NaN`;
+- reject `Infinity`;
+- reject `-Infinity`;
+- require UTF-8 JSON.
+
+Standard JSON floats may parse as floats, but a schema node of type `integer` must reject every float, including `30.0` and `1e2`.
+
+A boolean must never satisfy an integer schema merely because Python `bool` subclasses `int`.
+
+## Schema language V0.1
+
+Supported node kinds:
+- object;
+- array;
+- string;
+- integer;
+- boolean;
+- null.
+
+Object nodes are closed: the exact key set is normative.
+
+Array nodes can freeze:
+- item schema;
+- minimum/maximum length;
+- uniqueness;
+- allowed scalar vocabulary;
+- exact ordered content when order itself is normative.
+
+Scalar nodes can freeze:
+- type;
+- const;
+- enum;
+- regex pattern;
+- integer min/max.
+
+The schema definition itself must be strictly validated so an unknown schema-language key cannot silently widen the guard.
+
+## P5-E adopted-contract schema
+
+RPE-01 will create a governed schema for the already adopted P5-E V0.1 contract without modifying the contract bytes.
+
+The schema closes every object depth.
+
+Normative lists will be unique and use a closed vocabulary.
+
+`real_end_to_end_stages` will additionally freeze exact order.
+
+The guard is not a replacement for semantic invariants or object binding.
+
+It provides an independent structural defense against intentionally re-bound future amendments.
+
+## Future REAL P5-E artifacts
+
+The same guard API is intended for later governed JSON artifacts:
+- RPE-02 real-time contract/config;
+- RPE-04 adapter configuration;
+- RPE-05 runner configuration;
+- RPE-06 experiment preregistration;
+- execution evidence envelopes.
+
+Those future schemas are not created in RPE-01.
+
+RPE-01 only qualifies the guard capability and one concrete schema for the adopted P5-E contract.
+
+## Test-first plan
+
+1. Persist preregistration.
+2. Create RED tests while implementation/schema are absent.
+3. Persist RED.
+4. Implement the minimum pure guard.
+5. Generate/review the concrete P5-E schema.
+6. Run mandatory adversarial breakers.
+7. Run a programmatic mutation sweep over every object node/key and selected typed/list mutations.
+8. Re-run targeted existing P5-E tests.
+9. Persist qualification evidence with exact blobs.
+10. Produce external-review packet.
+11. STOP before human adoption/RPE-02.
+
+## Maximum claim
+
+If successful:
+
+`RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE = QUALIFIED_FOR_EXTERNAL_REVIEW`
+
+Not claimed:
+- RPE-02 readiness or implementation;
+- real-time timing qualification;
+- ancestry classification;
+- remote adapter;
+- timed runner;
+- real experiment;
+- REAL P5-E.
+
+`REAL_P5E = CLOSED`
diff --git a/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-QUALIFICATION.md b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-QUALIFICATION.md
new file mode 100644
index 0000000..83f17da
--- /dev/null
+++ b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-QUALIFICATION.md
@@ -0,0 +1,207 @@
+# RPE-01 ÔÇö N4 GOVERNED CLOSED SCHEMA ÔÇö QUALIFICATION
+
+Date: 2026-10-02
+
+## Result
+
+```text
+RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
+= QUALIFIED_FOR_EXTERNAL_REVIEW
+```
+
+RPE-01 is not yet human-adopted.
+
+RPE-02 and later stages remain closed.
+
+## Lineage
+
+Adopted readiness base:
+`d904eb61d9b704dc8ac38da445eb1cd491a58b33`
+
+Preregistration:
+`406e67da3ab197c5a9ae4b3e971368549af6e1da`
+
+RED test:
+`803709c26769fc9889b4ac1e47c0dd8df2782580`
+
+RED report:
+`b3a7df32198fd5a618f927c83d04d5f3a6491050`
+
+## Qualified implementation identities
+
+Guard:
+`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`
+
+Concrete P5-E governed schema:
+`87e45cc75753439879e2902d3cbdbd5d71d8a1b2`
+
+Green test:
+`391663ee2b8634c0221b5352c8d1242bfdb3c04e`
+
+Mutation sweep test:
+`bad495950ddce5c171cac4c667e40654c6673724`
+
+Adopted P5-E contract covered by the concrete schema:
+`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`
+
+## Test-first evidence
+
+Initial RED:
+
+```text
+Ran 19 tests
+FAILED
+1 intentional PASS demonstrated the pre-RPE01 gap:
+unknown authority key survived the old semantic invariant checker.
+```
+
+After implementation:
+
+```text
+RPE-01 targeted
+= 22 / 22 PASS
+```
+
+## Mutation sweep
+
+The programmatic sweep did not use P5-E contract blob binding as a rejection mechanism.
+
+It mutated:
+- every object node with an unknown key;
+- every required object key by deletion;
+- every scalar leaf to a different JSON type;
+- every concrete normative list with duplicate and unknown members;
+- the normative order of `real_end_to_end_stages`.
+
+Observed:
+
+```text
+attempted = 433
+survivors = 0
+```
+
+Therefore the preregistered exit criterion is satisfied:
+
+`ALL_PREREGISTERED_SCHEMA_MUTATIONS_REJECTED_WITHOUT_USING_P5E_CONTRACT_BLOB_BINDING`
+
+## Parser and schema-language properties
+
+The qualified guard rejects before dictionary construction:
+- duplicate raw JSON object members;
+- nested duplicates;
+- `NaN`;
+- `Infinity`;
+- `-Infinity`.
+
+The validator enforces:
+- exact closed object key sets;
+- strict JSON type identity;
+- bool is not accepted as integer;
+- float/scientific-float is not accepted as integer;
+- enums;
+- regex patterns;
+- integer bounds;
+- list length;
+- list uniqueness;
+- closed list vocabulary;
+- exact normative order where configured.
+
+The schema definition itself is also parsed through the strict parser and strictly validated.
+
+## Authority-channel property
+
+The guard implementation is pure with respect to configuration authority.
+
+Its source imports none of:
+- `os`;
+- `sys`;
+- `argparse`;
+- `socket`;
+- `subprocess`;
+- HTTP client modules.
+
+It does not use:
+- environment variables;
+- CLI arguments;
+- interactive input;
+- implicit file reads;
+- network state.
+
+Inputs are only:
+- explicit raw JSON;
+- explicit schema object/raw schema.
+
+This prevents the guard itself from becoming a hidden adjacent configuration authority.
+
+## Concrete P5-E schema
+
+The concrete P5-E schema:
+- closes every current object depth;
+- requires every current key;
+- enforces strict leaf types;
+- freezes the vocabulary and cardinality of current normative lists;
+- requires normative list uniqueness;
+- freezes exact order for `real_end_to_end_stages`;
+- includes source binding to the adopted P5-E contract blob.
+
+The source-binding test recomputes the Git object identity and matches:
+
+`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`
+
+The adopted contract bytes were not modified.
+
+## Targeted regression
+
+Executed the current P5-E qualification surface plus RPE-01:
+
+```text
+Ran 89 tests
+OK
+```
+
+Repository deltas relative to the adopted readiness base:
+
+```text
+P5-E contract diff = 0
+P5-E model diff = 0
+P5-D4 runtime diff = 0
+```
+
+No full Obsidian suite was required or executed.
+
+## Real state
+
+P5-D4 real-state fingerprints remained:
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
+## Binding
+
+The qualification binds the exact guard blob and P5-E schema blob.
+
+Any modification of either requires a new qualification before the modified artifact may be treated as RPE-01-qualified.
+
+## Maximum claim
+
+```text
+RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
+= QUALIFIED_FOR_EXTERNAL_REVIEW
+
+RPE01_HUMAN_ADOPTION
+= PENDING
+
+RPE02
+= CLOSED
+
+REAL_P5E
+= CLOSED
+```
diff --git a/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-RED.md b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-RED.md
new file mode 100644
index 0000000..b3a7df3
--- /dev/null
+++ b/reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-RED.md
@@ -0,0 +1,82 @@
+# RPE-01 ÔÇö N4 GOVERNED CLOSED SCHEMA ÔÇö RED EVIDENCE
+
+Date: 2026-10-02
+
+## Preregistered predecessor
+
+HEAD:
+`0c6089b56a438a3faad23af20216f9666685ba0f`
+
+Preregistration blob:
+`406e67da3ab197c5a9ae4b3e971368549af6e1da`
+
+## RED test
+
+`tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py`
+
+Created before:
+- `tools/obsidian_projection/rpe01_governed_closed_schema.py`;
+- `tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json`.
+
+## Command
+
+```text
+python -B -m unittest tests.obsidian_projection.test_rpe01_governed_closed_schema_v0_1
+```
+
+## Observed result
+
+```text
+Ran 19 tests in 0.016s
+
+FAILED (failures=20)
+
+RED_EXIT=1
+```
+
+The failure count exceeds the test count because one test contains multiple failing subtests.
+
+## Important RED signal
+
+One test intentionally PASSED:
+
+`ExistingGapEvidenceTests.test_existing_p5e_invariants_do_not_close_unknown_keys`
+
+It inserted:
+
+`authority_boundary.rpe01_probe_unknown_authority = true`
+
+into an in-memory copy of the adopted P5-E contract.
+
+The existing semantic invariant checker accepted that mutated object.
+
+This demonstrates the exact N4 gap independently of P5-E contract blob binding.
+
+## RED failures
+
+All new RPE-01 guard capabilities failed because the guard module and concrete governed schema did not yet exist.
+
+The RED covers:
+
+- duplicate raw JSON members;
+- nested duplicates;
+- NaN / ┬▒Infinity;
+- strict integer/boolean distinction;
+- float/scientific-float rejection where integer is required;
+- enum closure;
+- list uniqueness;
+- normative list order;
+- adjacent config unknown authority/environment/CLI override keys;
+- schema-language unknown keys;
+- schema-language wrong types;
+- unsupported schema node kinds;
+- P5-E contract exact object-depth closure;
+- missing required keys;
+- concrete normative-list closure;
+- guard purity / no implicit authority channels.
+
+## Authority boundary
+
+No runtime, adopted contract, adopted synthetic model, P5-D4 state, Vault or CURRENT artifact was modified.
+
+`REAL_P5E = CLOSED`
diff --git a/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
new file mode 100644
index 0000000..bad4959
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
@@ -0,0 +1,153 @@
+import copy
+import importlib.util
+import json
+import unittest
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[2]
+GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
+SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
+CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
+
+
+def load_guard():
+    spec = importlib.util.spec_from_file_location("rpe01_guard_sweep", GUARD_PATH)
+    if spec is None or spec.loader is None:
+        raise AssertionError("cannot load RPE-01 guard")
+    module = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(module)
+    return module
+
+
+def iter_nodes(value, path=()):
+    yield path, value
+    if type(value) is dict:
+        for key, child in value.items():
+            yield from iter_nodes(child, path + (key,))
+    elif type(value) is list:
+        for index, child in enumerate(value):
+            yield from iter_nodes(child, path + (index,))
+
+
+def get_node(root, path):
+    node = root
+    for part in path:
+        node = node[part]
+    return node
+
+
+def set_node(root, path, value):
+    if not path:
+        raise AssertionError("root replacement not used by this sweep")
+    parent = get_node(root, path[:-1])
+    parent[path[-1]] = value
+
+
+def wrong_type(value):
+    if type(value) is bool:
+        return 0
+    if type(value) is int:
+        return float(value)
+    if type(value) is str:
+        return False
+    if value is None:
+        return "NOT_NULL"
+    raise AssertionError(f"unsupported leaf type: {type(value).__name__}")
+
+
+def run_sweep():
+    guard = load_guard()
+    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
+    baseline = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
+    raw_baseline = CONTRACT_PATH.read_text(encoding="utf-8")
+    guard.validate_governed_json(raw_baseline, schema)
+
+    attempted = 0
+    survivors = []
+
+    def expect_reject(label, mutated):
+        nonlocal attempted
+        attempted += 1
+        try:
+            guard.validate_governed_json(
+                json.dumps(mutated, ensure_ascii=False),
+                schema,
+            )
+        except guard.GovernedSchemaError:
+            return
+        survivors.append(label)
+
+    nodes = list(iter_nodes(baseline))
+
+    # Unknown key at every object node.
+    for path, value in nodes:
+        if type(value) is not dict:
+            continue
+        mutated = copy.deepcopy(baseline)
+        target = get_node(mutated, path)
+        probe = "__rpe01_unknown_key__"
+        if probe in target:
+            raise AssertionError("unexpected probe collision")
+        target[probe] = True
+        expect_reject(f"ADD_UNKNOWN:{path}", mutated)
+
+    # Remove every required key from every object node.
+    for path, value in nodes:
+        if type(value) is not dict:
+            continue
+        for key in value:
+            mutated = copy.deepcopy(baseline)
+            target = get_node(mutated, path)
+            del target[key]
+            expect_reject(f"REMOVE_REQUIRED:{path + (key,)}", mutated)
+
+    # Change every scalar leaf to a different JSON type.
+    for path, value in nodes:
+        if type(value) in (dict, list):
+            continue
+        mutated = copy.deepcopy(baseline)
+        set_node(mutated, path, wrong_type(value))
+        expect_reject(f"WRONG_TYPE:{path}", mutated)
+
+    # Every concrete contract list is preregistered as unique and closed vocabulary.
+    for path, value in nodes:
+        if type(value) is not list or not value:
+            continue
+
+        if len(value) >= 2:
+            mutated = copy.deepcopy(baseline)
+            target = get_node(mutated, path)
+            target[1] = target[0]
+            expect_reject(f"DUPLICATE_LIST_MEMBER:{path}", mutated)
+
+        mutated = copy.deepcopy(baseline)
+        target = get_node(mutated, path)
+        target[0] = "__RPE01_UNKNOWN_LIST_MEMBER__"
+        expect_reject(f"UNKNOWN_LIST_MEMBER:{path}", mutated)
+
+    # Exact order is normative for the real end-to-end stage pipeline.
+    path = ("end_to_end_definition", "real_end_to_end_stages")
+    mutated = copy.deepcopy(baseline)
+    target = get_node(mutated, path)
+    target[0], target[1] = target[1], target[0]
+    expect_reject("ORDER_CHANGE:real_end_to_end_stages", mutated)
+
+    return {
+        "attempted": attempted,
+        "survivors": survivors,
+        "survivor_count": len(survivors),
+    }
+
+
+class RPE01MutationSweepTests(unittest.TestCase):
+    def test_all_preregistered_contract_schema_mutations_are_rejected(self):
+        result = run_sweep()
+        self.assertGreater(result["attempted"], 0)
+        self.assertEqual(result["survivors"], [])
+
+
+if __name__ == "__main__":
+    result = run_sweep()
+    print(json.dumps(result, indent=2))
+    raise SystemExit(0 if result["survivor_count"] == 0 else 1)
diff --git a/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py b/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
new file mode 100644
index 0000000..391663e
--- /dev/null
+++ b/tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
@@ -0,0 +1,274 @@
+import ast
+import copy
+import importlib.util
+import json
+import unittest
+from pathlib import Path
+
+
+ROOT = Path(__file__).resolve().parents[2]
+GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
+P5E_SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
+P5E_CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
+P5E_ADV_PATH = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"
+
+
+def load_module(path: Path, name: str):
+    if not path.exists():
+        raise AssertionError(f"required implementation missing: {path}")
+    spec = importlib.util.spec_from_file_location(name, path)
+    if spec is None or spec.loader is None:
+        raise AssertionError(f"cannot load module: {path}")
+    module = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(module)
+    return module
+
+
+def load_guard():
+    return load_module(GUARD_PATH, "rpe01_guard_under_test")
+
+
+def load_schema():
+    if not P5E_SCHEMA_PATH.exists():
+        raise AssertionError(f"required governed schema missing: {P5E_SCHEMA_PATH}")
+    g = load_guard()
+    return g.parse_schema_json_strict(P5E_SCHEMA_PATH.read_text(encoding="utf-8"))
+
+
+def current_contract_raw() -> str:
+    return P5E_CONTRACT_PATH.read_text(encoding="utf-8")
+
+
+def synthetic_schema():
+    return {
+        "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
+        "artifact_role": "RPE01_SYNTHETIC_ADJACENT_CONFIG",
+        "root": {
+            "kind": "object",
+            "fields": {
+                "interval_ns": {
+                    "kind": "integer",
+                    "minimum": 1,
+                    "maximum": 60_000_000_000,
+                },
+                "enabled": {"kind": "boolean", "const": False},
+                "mode": {
+                    "kind": "string",
+                    "enum": ["FIXED_RATE", "DISABLED"],
+                },
+                "stages": {
+                    "kind": "array",
+                    "items": {"kind": "string"},
+                    "min_items": 2,
+                    "max_items": 2,
+                    "unique": True,
+                    "ordered_const": ["OBSERVE", "STOP"],
+                },
+            },
+        },
+    }
+
+
+class ExistingGapEvidenceTests(unittest.TestCase):
+    def test_existing_p5e_invariants_do_not_close_unknown_keys(self):
+        adv = load_module(P5E_ADV_PATH, "rpe01_gap_adv")
+        contract = json.loads(current_contract_raw())
+        mutated = copy.deepcopy(contract)
+        mutated["authority_boundary"]["rpe01_probe_unknown_authority"] = True
+        # This PASS demonstrates the pre-RPE01 structural gap.
+        adv.assert_contract_invariants(mutated)
+
+
+class StrictRawJsonTests(unittest.TestCase):
+    def test_duplicate_authority_member_is_rejected_before_dict_construction(self):
+        g = load_guard()
+        raw = '{"evaluation_authorized":true,"evaluation_authorized":false}'
+        with self.assertRaises(g.GovernedSchemaError):
+            g.parse_json_strict(raw)
+
+    def test_duplicate_nested_member_is_rejected(self):
+        g = load_guard()
+        raw = '{"outer":{"x":1,"x":2}}'
+        with self.assertRaises(g.GovernedSchemaError):
+            g.parse_json_strict(raw)
+
+    def test_nan_and_infinities_are_rejected(self):
+        g = load_guard()
+        for raw in ('{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
+            with self.subTest(raw=raw):
+                with self.assertRaises(g.GovernedSchemaError):
+                    g.parse_json_strict(raw)
+
+
+class SchemaDefinitionTests(unittest.TestCase):
+    def test_schema_definition_rejects_unknown_schema_language_key(self):
+        g = load_guard()
+        schema = synthetic_schema()
+        schema["root"]["surprise"] = True
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_schema_definition(schema)
+
+    def test_schema_definition_rejects_wrong_constraint_type(self):
+        g = load_guard()
+        schema = synthetic_schema()
+        schema["root"]["fields"]["interval_ns"]["minimum"] = "1"
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_schema_definition(schema)
+
+    def test_schema_definition_rejects_unsupported_kind(self):
+        g = load_guard()
+        schema = synthetic_schema()
+        schema["root"]["fields"]["interval_ns"]["kind"] = "number"
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_schema_definition(schema)
+
+    def test_raw_schema_duplicate_member_and_nan_are_rejected(self):
+        g = load_guard()
+        duplicate = '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1","artifact_role":"A","artifact_role":"B","root":{"kind":"null"}}'
+        with self.assertRaises(g.GovernedSchemaError):
+            g.parse_schema_json_strict(duplicate)
+        with self.assertRaises(g.GovernedSchemaError):
+            g.parse_schema_json_strict('{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1","artifact_role":"A","root":{"kind":"integer","minimum":NaN}}')
+
+
+class StrictTypeAndListTests(unittest.TestCase):
+    def assert_rejected(self, document):
+        g = load_guard()
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(json.dumps(document), synthetic_schema())
+
+    def test_float_and_scientific_float_where_integer_required_are_rejected(self):
+        self.assert_rejected({"interval_ns": 30.0, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
+        g = load_guard()
+        raw = '{"interval_ns":1e2,"enabled":false,"mode":"FIXED_RATE","stages":["OBSERVE","STOP"]}'
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(raw, synthetic_schema())
+
+    def test_boolean_where_integer_required_is_rejected(self):
+        self.assert_rejected({"interval_ns": True, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
+
+    def test_integer_where_boolean_required_is_rejected(self):
+        self.assert_rejected({"interval_ns": 30, "enabled": 0, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
+
+    def test_unknown_enum_is_rejected(self):
+        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "COALESCE", "stages": ["OBSERVE", "STOP"]})
+
+    def test_duplicate_list_member_is_rejected(self):
+        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "OBSERVE"]})
+
+    def test_normative_order_change_is_rejected(self):
+        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["STOP", "OBSERVE"]})
+
+    def test_unknown_adjacent_config_authority_keys_are_rejected(self):
+        base = {"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]}
+        for key in ("evaluation_authorized", "environment_override", "cli_override"):
+            with self.subTest(key=key):
+                mutated = dict(base)
+                mutated[key] = True
+                self.assert_rejected(mutated)
+
+
+class P5EConcreteSchemaTests(unittest.TestCase):
+    def test_adopted_contract_is_accepted_without_byte_mutation(self):
+        g = load_guard()
+        schema = load_schema()
+        doc = g.validate_governed_json(current_contract_raw(), schema)
+        self.assertEqual(doc["schema"], "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1")
+
+    def test_unknown_keys_at_representative_depths_are_rejected(self):
+        g = load_guard()
+        schema = load_schema()
+        contract = json.loads(current_contract_raw())
+        paths = [
+            (),
+            ("authority_boundary",),
+            ("near_real_time_timing",),
+            ("queue_and_supersession",),
+            ("external_review_targeted_closure", "findings"),
+        ]
+        for path in paths:
+            with self.subTest(path=path):
+                mutated = copy.deepcopy(contract)
+                node = mutated
+                for key in path:
+                    node = node[key]
+                node["rpe01_unknown_key"] = True
+                with self.assertRaises(g.GovernedSchemaError):
+                    g.validate_governed_json(json.dumps(mutated), schema)
+
+    def test_missing_required_key_is_rejected(self):
+        g = load_guard()
+        schema = load_schema()
+        contract = json.loads(current_contract_raw())
+        del contract["authority_boundary"]["evaluation_authorized"]
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(json.dumps(contract), schema)
+
+    def test_normative_list_duplicate_unknown_and_order_change_are_rejected(self):
+        g = load_guard()
+        schema = load_schema()
+        contract = json.loads(current_contract_raw())
+
+        duplicate = copy.deepcopy(contract)
+        duplicate["claim_boundary"]["forbidden_current_claims"][1] = duplicate["claim_boundary"]["forbidden_current_claims"][0]
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(json.dumps(duplicate), schema)
+
+        unknown = copy.deepcopy(contract)
+        unknown["required_synthetic_cases"][0] = "RPE01_UNKNOWN_CASE"
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(json.dumps(unknown), schema)
+
+        reordered = copy.deepcopy(contract)
+        stages = reordered["end_to_end_definition"]["real_end_to_end_stages"]
+        stages[0], stages[1] = stages[1], stages[0]
+        with self.assertRaises(g.GovernedSchemaError):
+            g.validate_governed_json(json.dumps(reordered), schema)
+
+
+class SchemaBindingTests(unittest.TestCase):
+    def test_p5e_schema_source_binding_matches_current_contract_blob(self):
+        import subprocess
+
+        schema = load_schema()
+        binding = schema["source_binding"]
+        self.assertEqual(
+            binding["path"],
+            "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
+        )
+        actual = subprocess.check_output(
+            [
+                "git",
+                "hash-object",
+                "--path=" + binding["path"],
+                binding["path"],
+            ],
+            cwd=ROOT,
+            text=True,
+        ).strip()
+        self.assertEqual(actual, binding["git_blob"])
+
+
+class GuardPurityTests(unittest.TestCase):
+    def test_guard_source_has_no_implicit_authority_channels(self):
+        if not GUARD_PATH.exists():
+            self.fail(f"required implementation missing: {GUARD_PATH}")
+        source = GUARD_PATH.read_text(encoding="utf-8")
+        tree = ast.parse(source)
+        forbidden_import_roots = {
+            "argparse", "os", "socket", "subprocess", "sys", "urllib",
+            "requests", "httpx",
+        }
+        imported = set()
+        for node in ast.walk(tree):
+            if isinstance(node, ast.Import):
+                imported.update(alias.name.split(".")[0] for alias in node.names)
+            elif isinstance(node, ast.ImportFrom) and node.module:
+                imported.add(node.module.split(".")[0])
+        self.assertTrue(imported.isdisjoint(forbidden_import_roots), imported & forbidden_import_roots)
+        for forbidden_text in ("os.environ", "sys.argv", "input(", "open(", ".read_text(", ".read_bytes("):
+            self.assertNotIn(forbidden_text, source)
+
+
+if __name__ == "__main__":
+    unittest.main()
diff --git a/tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json b/tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json
new file mode 100644
index 0000000..87e45cc
--- /dev/null
+++ b/tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json
@@ -0,0 +1,734 @@
+{
+  "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
+  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",
+  "source_binding": {
+    "path": "tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json",
+    "git_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9"
+  },
+  "root": {
+    "kind": "object",
+    "fields": {
+      "schema": {
+        "kind": "string"
+      },
+      "status": {
+        "kind": "string"
+      },
+      "qualification_stage": {
+        "kind": "string"
+      },
+      "real_p5e_execution_authorized": {
+        "kind": "boolean"
+      },
+      "source_repository": {
+        "kind": "string"
+      },
+      "monitored_source": {
+        "kind": "object",
+        "fields": {
+          "remote": {
+            "kind": "string"
+          },
+          "branch": {
+            "kind": "string"
+          },
+          "canonical_authority": {
+            "kind": "string"
+          },
+          "local_working_tree_is_not_authority": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "predecessors": {
+        "kind": "object",
+        "fields": {
+          "p5a_continuous_projection_contract_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5a_qualification_report_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d1_observer_contract_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d1_static_review_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d2_one_shot_contract_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d2_static_review_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d4_loop_contract_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d4_runtime_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d4_real_v0_2_qualification_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "p5d4_human_adjudication_blob": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          }
+        }
+      },
+      "objective": {
+        "kind": "object",
+        "fields": {
+          "name": {
+            "kind": "string"
+          },
+          "purpose": {
+            "kind": "string"
+          },
+          "this_stage_is_not_real_end_to_end_execution": {
+            "kind": "boolean"
+          },
+          "this_stage_may_not_claim_continuous_synchronization": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "near_real_time_timing": {
+        "kind": "object",
+        "fields": {
+          "delivery_semantics": {
+            "kind": "string"
+          },
+          "poll_interval_seconds": {
+            "kind": "integer"
+          },
+          "detection_latency_seconds_max": {
+            "kind": "integer"
+          },
+          "instantaneous_realtime_claim_forbidden": {
+            "kind": "boolean"
+          },
+          "silent_interval_widening_forbidden": {
+            "kind": "boolean"
+          },
+          "silent_latency_bound_widening_forbidden": {
+            "kind": "boolean"
+          },
+          "detection_latency_definition": {
+            "kind": "string"
+          },
+          "future_real_bound_clock": {
+            "kind": "string"
+          },
+          "future_real_wall_clock_may_be_recorded_as_evidence_only": {
+            "kind": "boolean"
+          },
+          "future_real_poll_schedule_semantics": {
+            "kind": "string"
+          },
+          "single_transient_read_failure_may_still_meet_60_second_bound": {
+            "kind": "boolean"
+          },
+          "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": {
+            "kind": "boolean"
+          },
+          "real_measurement_origin": {
+            "kind": "string"
+          },
+          "measurement_endpoint": {
+            "kind": "string"
+          },
+          "schedule_semantics": {
+            "kind": "string"
+          },
+          "remote_head_available_time_is_measurable_origin": {
+            "kind": "boolean"
+          },
+          "real_latency_metric": {
+            "kind": "string"
+          },
+          "attempt_start_and_read_completion_are_distinct": {
+            "kind": "boolean"
+          },
+          "read_duration_is_included_in_detection_latency": {
+            "kind": "boolean"
+          },
+          "eligible_detection_attempt_must_start_at_or_after_release": {
+            "kind": "boolean"
+          },
+          "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "synthetic_timing_model": {
+        "kind": "object",
+        "fields": {
+          "required": {
+            "kind": "boolean"
+          },
+          "clock_source": {
+            "kind": "string"
+          },
+          "sleep_forbidden": {
+            "kind": "boolean"
+          },
+          "network_forbidden": {
+            "kind": "boolean"
+          },
+          "filesystem_state_forbidden": {
+            "kind": "boolean"
+          },
+          "process_launch_forbidden": {
+            "kind": "boolean"
+          },
+          "environment_read_forbidden": {
+            "kind": "boolean"
+          },
+          "real_p5d4_control_state_access_forbidden": {
+            "kind": "boolean"
+          },
+          "real_vault_access_forbidden": {
+            "kind": "boolean"
+          },
+          "purpose": {
+            "kind": "string"
+          },
+          "schedule_semantics": {
+            "kind": "string"
+          },
+          "schedule_origin_seconds": {
+            "kind": "integer"
+          },
+          "observation_record_fields": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 4,
+            "max_items": 4,
+            "unique": true,
+            "allowed_values": [
+              "scheduled_at_seconds",
+              "completed_at_seconds",
+              "outcome",
+              "observed_head"
+            ]
+          },
+          "head_identity_required_on_successful_remote_observation": {
+            "kind": "boolean"
+          },
+          "skipped_required_attempt_result": {
+            "kind": "string"
+          },
+          "cadence_gap_result": {
+            "kind": "string"
+          },
+          "pre_source_target_observation_result": {
+            "kind": "string"
+          },
+          "explicit_non_pass_statuses": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 1,
+            "max_items": 1,
+            "unique": true,
+            "allowed_values": [
+              "INCOMPLETE_SYNTHETIC_WINDOW"
+            ]
+          },
+          "attempt_overruns_next_required_slot_result": {
+            "kind": "string"
+          },
+          "attempt_overruns_next_required_slot_failure_code": {
+            "kind": "string"
+          },
+          "duplicate_fixed_rate_slot_result": {
+            "kind": "string"
+          },
+          "duplicate_fixed_rate_slot_failure_code": {
+            "kind": "string"
+          },
+          "read_completion_before_attempt_start_forbidden": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "authority_boundary": {
+        "kind": "object",
+        "fields": {
+          "observer_may_create_governance_authority": {
+            "kind": "boolean"
+          },
+          "pending_head_evaluation_authorized": {
+            "kind": "boolean"
+          },
+          "evaluation_authorized": {
+            "kind": "boolean"
+          },
+          "stage_a_authorized": {
+            "kind": "boolean"
+          },
+          "stage_b_authorized": {
+            "kind": "boolean"
+          },
+          "promotion_authorized": {
+            "kind": "boolean"
+          },
+          "publication_authorized": {
+            "kind": "boolean"
+          },
+          "real_vault_mutation_authorized": {
+            "kind": "boolean"
+          },
+          "current_mutation_authorized": {
+            "kind": "boolean"
+          },
+          "current_tmp_mutation_authorized": {
+            "kind": "boolean"
+          },
+          "real_polling_loop_authorized": {
+            "kind": "boolean"
+          },
+          "daemon_authorized": {
+            "kind": "boolean"
+          },
+          "startup_registration_authorized": {
+            "kind": "boolean"
+          },
+          "scheduled_task_authorized": {
+            "kind": "boolean"
+          },
+          "windows_service_authorized": {
+            "kind": "boolean"
+          },
+          "p6_authorized": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "head_transition_policy": {
+        "kind": "object",
+        "fields": {
+          "same_head_result": {
+            "kind": "string"
+          },
+          "same_head_queue_growth_forbidden": {
+            "kind": "boolean"
+          },
+          "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": {
+            "kind": "boolean"
+          },
+          "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": {
+            "kind": "boolean"
+          },
+          "non_fast_forward_result": {
+            "kind": "string"
+          },
+          "unknown_ancestry_result": {
+            "kind": "string"
+          },
+          "non_fast_forward_auto_continue_forbidden": {
+            "kind": "boolean"
+          },
+          "unknown_ancestry_auto_continue_forbidden": {
+            "kind": "boolean"
+          },
+          "active_or_pending_candidate_retarget_forbidden": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "queue_and_supersession": {
+        "kind": "object",
+        "fields": {
+          "precedence_rule": {
+            "kind": "string"
+          },
+          "p5a_supersession_intent_preserved_as_future_design_debt": {
+            "kind": "boolean"
+          },
+          "fifo_required": {
+            "kind": "boolean"
+          },
+          "unique_heads_required": {
+            "kind": "boolean"
+          },
+          "silent_drop_forbidden": {
+            "kind": "boolean"
+          },
+          "silent_reorder_forbidden": {
+            "kind": "boolean"
+          },
+          "latest_only_replacement_forbidden": {
+            "kind": "boolean"
+          },
+          "coalescing_authorized": {
+            "kind": "boolean"
+          },
+          "new_coalescing_semantic_event_authorized": {
+            "kind": "boolean"
+          },
+          "pending_head_retarget_forbidden": {
+            "kind": "boolean"
+          },
+          "capacity_exhausted_result": {
+            "kind": "string"
+          },
+          "capacity_exhausted_must_not_mutate_p5d2_state": {
+            "kind": "boolean"
+          },
+          "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "failure_and_freshness": {
+        "kind": "object",
+        "fields": {
+          "fail_closed_default": {
+            "kind": "boolean"
+          },
+          "network_failure_must_not_create_current_claim": {
+            "kind": "boolean"
+          },
+          "last_known_good_live_projection_preserved": {
+            "kind": "boolean"
+          },
+          "latency_bound_breach_result": {
+            "kind": "string"
+          },
+          "queue_capacity_exhaustion_result": {
+            "kind": "string"
+          },
+          "non_fast_forward_or_unknown_result": {
+            "kind": "string"
+          },
+          "unexpected_state_or_timing_ambiguity_result": {
+            "kind": "string"
+          },
+          "timing_inconsistency_result": {
+            "kind": "string"
+          },
+          "skipped_required_attempt_result": {
+            "kind": "string"
+          },
+          "cadence_gap_result": {
+            "kind": "string"
+          },
+          "pre_source_target_observation_result": {
+            "kind": "string"
+          }
+        }
+      },
+      "end_to_end_definition": {
+        "kind": "object",
+        "fields": {
+          "real_end_to_end_stages": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 8,
+            "max_items": 8,
+            "unique": true,
+            "allowed_values": [
+              "SOURCE_HEAD_BECOMES_OBSERVABLE",
+              "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
+              "HEAD_TRANSITION_CLASSIFIED",
+              "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
+              "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
+              "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
+              "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
+              "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
+            ],
+            "ordered_const": [
+              "SOURCE_HEAD_BECOMES_OBSERVABLE",
+              "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
+              "HEAD_TRANSITION_CLASSIFIED",
+              "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
+              "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
+              "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
+              "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
+              "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
+            ]
+          },
+          "current_stage_may_qualify_only": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 4,
+            "max_items": 4,
+            "unique": true,
+            "allowed_values": [
+              "TIMING_CONTRACT",
+              "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
+              "AUTHORITY_BOUNDARIES",
+              "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
+            ]
+          },
+          "real_end_to_end_pass_requires_all_authorized_applicable_stages": {
+            "kind": "boolean"
+          },
+          "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": {
+            "kind": "boolean"
+          },
+          "transient_tip_exact_detection_sla_not_qualified": {
+            "kind": "boolean"
+          },
+          "real_remote_availability_to_detection_sla_not_qualified": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "claim_boundary": {
+        "kind": "object",
+        "fields": {
+          "maximum_current_claim": {
+            "kind": "string"
+          },
+          "real_end_to_end_qualification_requires_separate_authorization": {
+            "kind": "boolean"
+          },
+          "forbidden_current_claims": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 8,
+            "max_items": 8,
+            "unique": true,
+            "allowed_values": [
+              "P5E_REAL_END_TO_END_QUALIFIED",
+              "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
+              "REAL_60_SECOND_SLA_QUALIFIED",
+              "AUTOMATIC_EVALUATION_QUALIFIED",
+              "AUTOMATIC_PROMOTION_QUALIFIED",
+              "AUTOMATIC_PUBLICATION_QUALIFIED",
+              "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
+              "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
+            ]
+          }
+        }
+      },
+      "real_context_evidence_only": {
+        "kind": "object",
+        "fields": {
+          "live_projection_head_at_opening": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "queued_unevaluated_head_at_opening": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "remote_head_observed_during_contract_opening": {
+            "kind": "string",
+            "pattern": "[0-9a-f]{40}\\Z"
+          },
+          "queued_head_is_ancestor_of_remote_head": {
+            "kind": "boolean"
+          },
+          "must_not_be_used_as_real_experiment_execution": {
+            "kind": "boolean"
+          },
+          "must_not_be_mutated_by_contract_qualification": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "required_synthetic_cases": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 10,
+        "max_items": 10,
+        "unique": true,
+        "allowed_values": [
+          "SAME_HEAD_NOOP",
+          "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
+          "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
+          "DETECTION_AFTER_60_SECONDS_REJECTED",
+          "NO_DETECTION_BY_60_SECONDS_REJECTED",
+          "NON_FAST_FORWARD_BLOCKED",
+          "UNKNOWN_ANCESTRY_BLOCKED",
+          "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
+          "SAME_HEAD_DOES_NOT_GROW_QUEUE",
+          "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
+        ]
+      },
+      "required_breakers": {
+        "kind": "array",
+        "items": {
+          "kind": "string"
+        },
+        "min_items": 25,
+        "max_items": 25,
+        "unique": true,
+        "allowed_values": [
+          "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
+          "DETECTION_BOUND_ABOVE_60_ACCEPTED",
+          "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
+          "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
+          "SLEEP_USED_IN_SYNTHETIC_MODEL",
+          "NETWORK_USED_IN_SYNTHETIC_MODEL",
+          "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
+          "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
+          "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
+          "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
+          "SAME_HEAD_GROWS_QUEUE",
+          "NON_FAST_FORWARD_AUTO_CONTINUES",
+          "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
+          "QUEUE_FULL_SILENTLY_DROPS_HEAD",
+          "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
+          "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
+          "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
+          "EVALUATION_AUTHORITY_BECOMES_TRUE",
+          "PROMOTION_AUTHORITY_BECOMES_TRUE",
+          "PUBLICATION_AUTHORITY_BECOMES_TRUE",
+          "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
+          "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
+          "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
+          "P6_AUTHORITY_BECOMES_TRUE",
+          "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
+        ]
+      },
+      "next_gate_after_candidate_qualification": {
+        "kind": "object",
+        "fields": {
+          "external_adversarial_review_required_before_normative_adoption": {
+            "kind": "boolean"
+          },
+          "human_adjudication_required_after_external_review": {
+            "kind": "boolean"
+          },
+          "real_p5e_execution_requires_separate_human_authorization": {
+            "kind": "boolean"
+          },
+          "p6_remains_closed": {
+            "kind": "boolean"
+          },
+          "external_adversarial_rereview_required": {
+            "kind": "boolean"
+          },
+          "human_adjudication_before_external_rereview_forbidden": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "tip_visibility_semantics": {
+        "kind": "object",
+        "fields": {
+          "observed_remote_tip_definition": {
+            "kind": "string"
+          },
+          "intermediate_fast_forward_commit_definition": {
+            "kind": "string"
+          },
+          "unobserved_intermediate_tip_may_be_claimed_observed": {
+            "kind": "boolean"
+          },
+          "unobserved_intermediate_tip_may_be_queued": {
+            "kind": "boolean"
+          },
+          "fast_forward_content_containment_is_queue_coalescing": {
+            "kind": "boolean"
+          },
+          "already_observed_queued_head_replacement_forbidden": {
+            "kind": "boolean"
+          },
+          "already_observed_queued_head_retarget_forbidden": {
+            "kind": "boolean"
+          },
+          "per_transient_tip_detection_sla_authorized": {
+            "kind": "boolean"
+          },
+          "future_ancestry_enumeration_requires_separate_qualification": {
+            "kind": "boolean"
+          },
+          "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": {
+            "kind": "boolean"
+          },
+          "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": {
+            "kind": "boolean"
+          }
+        }
+      },
+      "external_review_targeted_closure": {
+        "kind": "object",
+        "fields": {
+          "findings": {
+            "kind": "object",
+            "fields": {
+              "B1": {
+                "kind": "string"
+              },
+              "B2": {
+                "kind": "string"
+              },
+              "B3": {
+                "kind": "string"
+              },
+              "B4": {
+                "kind": "string"
+              },
+              "B5": {
+                "kind": "string"
+              }
+            }
+          },
+          "required_breakers": {
+            "kind": "array",
+            "items": {
+              "kind": "string"
+            },
+            "min_items": 8,
+            "max_items": 8,
+            "unique": true,
+            "allowed_values": [
+              "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
+              "CADENCE_GAP_ACCEPTED",
+              "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
+              "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
+              "READ_COMPLETION_LATENCY_HIDDEN",
+              "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
+              "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
+              "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
+            ]
+          },
+          "requirement_to_executable_evidence_matrix_required": {
+            "kind": "boolean"
+          },
+          "all_required_cases_must_be_mapped": {
+            "kind": "boolean"
+          },
+          "all_base_breakers_must_be_mapped": {
+            "kind": "boolean"
+          },
+          "all_targeted_closure_breakers_must_be_mapped": {
+            "kind": "boolean"
+          },
+          "unmapped_requirement_result": {
+            "kind": "string"
+          },
+          "external_rereview_required_before_human_normative_adoption": {
+            "kind": "boolean"
+          }
+        }
+      }
+    }
+  }
+}
diff --git a/tools/obsidian_projection/rpe01_governed_closed_schema.py b/tools/obsidian_projection/rpe01_governed_closed_schema.py
new file mode 100644
index 0000000..3f61b91
--- /dev/null
+++ b/tools/obsidian_projection/rpe01_governed_closed_schema.py
@@ -0,0 +1,322 @@
+from __future__ import annotations
+
+import json
+import re
+from typing import Any
+
+
+SCHEMA_ID = "ATDS_GOVERNED_JSON_SCHEMA_V0_1"
+_ALLOWED_KINDS = {"object", "array", "string", "integer", "boolean", "null"}
+_SHA1_RE = re.compile(r"[0-9a-f]{40}\Z")
+
+
+class GovernedSchemaError(ValueError):
+    pass
+
+
+def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
+    result: dict[str, Any] = {}
+    for key, value in pairs:
+        if key in result:
+            raise GovernedSchemaError(f"duplicate JSON member: {key}")
+        result[key] = value
+    return result
+
+
+def _reject_constant(value: str) -> None:
+    raise GovernedSchemaError(f"non-standard JSON numeric constant forbidden: {value}")
+
+
+def parse_json_strict(raw: str | bytes) -> Any:
+    if isinstance(raw, bytes):
+        try:
+            text = raw.decode("utf-8", errors="strict")
+        except UnicodeDecodeError as exc:
+            raise GovernedSchemaError(f"governed JSON must be valid UTF-8: {exc}") from exc
+    elif isinstance(raw, str):
+        text = raw
+    else:
+        raise GovernedSchemaError("raw governed JSON must be str or bytes")
+    try:
+        return json.loads(
+            text,
+            object_pairs_hook=_strict_object,
+            parse_constant=_reject_constant,
+        )
+    except GovernedSchemaError:
+        raise
+    except json.JSONDecodeError as exc:
+        raise GovernedSchemaError(f"invalid governed JSON: {exc}") from exc
+
+
+def _exact_keys(label: str, value: object, allowed: set[str], required: set[str]) -> dict[str, Any]:
+    if type(value) is not dict:
+        raise GovernedSchemaError(f"{label} must be an object")
+    actual = set(value)
+    unknown = actual - allowed
+    missing = required - actual
+    if unknown or missing:
+        raise GovernedSchemaError(
+            f"{label} schema mismatch: missing={sorted(missing)} unknown={sorted(unknown)}"
+        )
+    return value
+
+
+def _strict_int(label: str, value: object, *, minimum: int | None = None) -> int:
+    if type(value) is not int:
+        raise GovernedSchemaError(f"{label} must be an integer")
+    if minimum is not None and value < minimum:
+        raise GovernedSchemaError(f"{label} must be >= {minimum}")
+    return value
+
+
+def _strict_bool(label: str, value: object) -> bool:
+    if type(value) is not bool:
+        raise GovernedSchemaError(f"{label} must be a boolean")
+    return value
+
+
+def _strict_string(label: str, value: object, *, nonempty: bool = True) -> str:
+    if type(value) is not str:
+        raise GovernedSchemaError(f"{label} must be a string")
+    if nonempty and not value:
+        raise GovernedSchemaError(f"{label} must be non-empty")
+    return value
+
+
+def _unique_json_values(values: list[Any]) -> bool:
+    encoded = [
+        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
+        for value in values
+    ]
+    return len(encoded) == len(set(encoded))
+
+
+def _value_matches_kind(value: object, kind: str) -> bool:
+    if kind == "object":
+        return type(value) is dict
+    if kind == "array":
+        return type(value) is list
+    if kind == "string":
+        return type(value) is str
+    if kind == "integer":
+        return type(value) is int
+    if kind == "boolean":
+        return type(value) is bool
+    if kind == "null":
+        return value is None
+    return False
+
+
+def _validate_constraint_value(label: str, value: object, kind: str) -> None:
+    if not _value_matches_kind(value, kind):
+        raise GovernedSchemaError(f"{label} does not match node kind {kind}")
+
+
+def _validate_schema_node(node: object, path: str) -> None:
+    if type(node) is not dict:
+        raise GovernedSchemaError(f"{path} schema node must be an object")
+    kind = node.get("kind")
+    if type(kind) is not str or kind not in _ALLOWED_KINDS:
+        raise GovernedSchemaError(f"{path}.kind unsupported")
+
+    if kind == "object":
+        allowed = {"kind", "fields"}
+        _exact_keys(path, node, allowed, allowed)
+        fields = node["fields"]
+        if type(fields) is not dict or not fields:
+            raise GovernedSchemaError(f"{path}.fields must be a non-empty object")
+        for name, child in fields.items():
+            _strict_string(f"{path}.fields key", name)
+            _validate_schema_node(child, f"{path}.fields.{name}")
+        return
+
+    if kind == "array":
+        allowed = {
+            "kind", "items", "min_items", "max_items", "unique",
+            "ordered_const", "allowed_values",
+        }
+        _exact_keys(path, node, allowed, {"kind", "items"})
+        _validate_schema_node(node["items"], f"{path}.items")
+        item_kind = node["items"]["kind"]
+
+        minimum = None
+        maximum = None
+        if "min_items" in node:
+            minimum = _strict_int(f"{path}.min_items", node["min_items"], minimum=0)
+        if "max_items" in node:
+            maximum = _strict_int(f"{path}.max_items", node["max_items"], minimum=0)
+        if minimum is not None and maximum is not None and minimum > maximum:
+            raise GovernedSchemaError(f"{path} min_items exceeds max_items")
+        if "unique" in node:
+            _strict_bool(f"{path}.unique", node["unique"])
+        for constraint in ("ordered_const", "allowed_values"):
+            if constraint not in node:
+                continue
+            values = node[constraint]
+            if type(values) is not list:
+                raise GovernedSchemaError(f"{path}.{constraint} must be an array")
+            for index, value in enumerate(values):
+                _validate_constraint_value(
+                    f"{path}.{constraint}[{index}]",
+                    value,
+                    item_kind,
+                )
+            if not _unique_json_values(values):
+                raise GovernedSchemaError(f"{path}.{constraint} must not contain duplicates")
+        if "ordered_const" in node:
+            ordered = node["ordered_const"]
+            if minimum is not None and len(ordered) < minimum:
+                raise GovernedSchemaError(f"{path}.ordered_const shorter than min_items")
+            if maximum is not None and len(ordered) > maximum:
+                raise GovernedSchemaError(f"{path}.ordered_const longer than max_items")
+        return
+
+    if kind == "string":
+        allowed = {"kind", "const", "enum", "pattern"}
+        _exact_keys(path, node, allowed, {"kind"})
+        if "const" in node:
+            _validate_constraint_value(f"{path}.const", node["const"], kind)
+        if "enum" in node:
+            enum = node["enum"]
+            if type(enum) is not list or not enum:
+                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
+            for index, value in enumerate(enum):
+                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
+            if not _unique_json_values(enum):
+                raise GovernedSchemaError(f"{path}.enum must be unique")
+        if "pattern" in node:
+            pattern = _strict_string(f"{path}.pattern", node["pattern"])
+            try:
+                re.compile(pattern)
+            except re.error as exc:
+                raise GovernedSchemaError(f"{path}.pattern invalid: {exc}") from exc
+        return
+
+    if kind == "integer":
+        allowed = {"kind", "const", "enum", "minimum", "maximum"}
+        _exact_keys(path, node, allowed, {"kind"})
+        if "const" in node:
+            _validate_constraint_value(f"{path}.const", node["const"], kind)
+        if "enum" in node:
+            enum = node["enum"]
+            if type(enum) is not list or not enum:
+                raise GovernedSchemaError(f"{path}.enum must be a non-empty array")
+            for index, value in enumerate(enum):
+                _validate_constraint_value(f"{path}.enum[{index}]", value, kind)
+            if not _unique_json_values(enum):
+                raise GovernedSchemaError(f"{path}.enum must be unique")
+        minimum = None
+        maximum = None
+        if "minimum" in node:
+            minimum = _strict_int(f"{path}.minimum", node["minimum"])
+        if "maximum" in node:
+            maximum = _strict_int(f"{path}.maximum", node["maximum"])
+        if minimum is not None and maximum is not None and minimum > maximum:
+            raise GovernedSchemaError(f"{path} minimum exceeds maximum")
+        return
+
+    if kind == "boolean":
+        allowed = {"kind", "const"}
+        _exact_keys(path, node, allowed, {"kind"})
+        if "const" in node:
+            _validate_constraint_value(f"{path}.const", node["const"], kind)
+        return
+
+    if kind == "null":
+        _exact_keys(path, node, {"kind"}, {"kind"})
+        return
+
+    raise GovernedSchemaError(f"{path}.kind unsupported")
+
+
+def validate_schema_definition(schema: object) -> dict[str, Any]:
+    top = _exact_keys(
+        "schema",
+        schema,
+        {"schema", "artifact_role", "source_binding", "root"},
+        {"schema", "artifact_role", "root"},
+    )
+    if top["schema"] != SCHEMA_ID:
+        raise GovernedSchemaError("unsupported governed schema version")
+    _strict_string("schema.artifact_role", top["artifact_role"])
+    if "source_binding" in top:
+        binding = _exact_keys(
+            "schema.source_binding",
+            top["source_binding"],
+            {"path", "git_blob"},
+            {"path", "git_blob"},
+        )
+        _strict_string("schema.source_binding.path", binding["path"])
+        blob = _strict_string("schema.source_binding.git_blob", binding["git_blob"])
+        if _SHA1_RE.fullmatch(blob) is None:
+            raise GovernedSchemaError("schema.source_binding.git_blob must be lowercase 40-hex")
+    _validate_schema_node(top["root"], "schema.root")
+    return top
+
+
+def _validate_document_node(value: object, node: dict[str, Any], path: str) -> None:
+    kind = node["kind"]
+    if not _value_matches_kind(value, kind):
+        raise GovernedSchemaError(f"{path} must be {kind}")
+
+    if kind == "object":
+        fields = node["fields"]
+        actual = set(value)
+        expected = set(fields)
+        if actual != expected:
+            raise GovernedSchemaError(
+                f"{path} closed-schema mismatch: "
+                f"missing={sorted(expected - actual)} unknown={sorted(actual - expected)}"
+            )
+        for key, child in fields.items():
+            _validate_document_node(value[key], child, f"{path}.{key}")
+        return
+
+    if kind == "array":
+        length = len(value)
+        if "min_items" in node and length < node["min_items"]:
+            raise GovernedSchemaError(f"{path} shorter than min_items")
+        if "max_items" in node and length > node["max_items"]:
+            raise GovernedSchemaError(f"{path} longer than max_items")
+        if node.get("unique") is True and not _unique_json_values(value):
+            raise GovernedSchemaError(f"{path} contains duplicate items")
+        if "allowed_values" in node:
+            allowed = node["allowed_values"]
+            for item in value:
+                if item not in allowed:
+                    raise GovernedSchemaError(f"{path} contains item outside closed vocabulary")
+        if "ordered_const" in node and value != node["ordered_const"]:
+            raise GovernedSchemaError(f"{path} violates normative array order/content")
+        for index, item in enumerate(value):
+            _validate_document_node(item, node["items"], f"{path}[{index}]")
+        return
+
+    if "const" in node and value != node["const"]:
+        raise GovernedSchemaError(f"{path} const mismatch")
+    if "enum" in node and value not in node["enum"]:
+        raise GovernedSchemaError(f"{path} outside closed enum")
+    if kind == "string" and "pattern" in node:
+        if re.fullmatch(node["pattern"], value) is None:
+            raise GovernedSchemaError(f"{path} pattern mismatch")
+    if kind == "integer":
+        if "minimum" in node and value < node["minimum"]:
+            raise GovernedSchemaError(f"{path} below minimum")
+        if "maximum" in node and value > node["maximum"]:
+            raise GovernedSchemaError(f"{path} above maximum")
+
+
+def parse_schema_json_strict(raw: str | bytes) -> dict[str, Any]:
+    schema = parse_json_strict(raw)
+    return validate_schema_definition(schema)
+
+
+def validate_document(document: object, schema: object) -> Any:
+    validated_schema = validate_schema_definition(schema)
+    _validate_document_node(document, validated_schema["root"], "$")
+    return document
+
+
+def validate_governed_json(raw: str | bytes, schema: object) -> Any:
+    document = parse_json_strict(raw)
+    return validate_document(document, schema)
diff --git a/tools/obsidian_projection/rpe01_governed_closed_schema_preregistration_v0_1.json b/tools/obsidian_projection/rpe01_governed_closed_schema_preregistration_v0_1.json
new file mode 100644
index 0000000..406e67d
--- /dev/null
+++ b/tools/obsidian_projection/rpe01_governed_closed_schema_preregistration_v0_1.json
@@ -0,0 +1,99 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_GOVERNED_CLOSED_SCHEMA_PREREGISTRATION_V0_1",
+  "status": "PREREGISTERED_BEFORE_RED",
+  "date": "2026-10-02",
+  "base_head": "d904eb61d9b704dc8ac38da445eb1cd491a58b33",
+  "readiness_adoption_blob": "aeba19575671a37fbdde2bbb994bbe947fed88d8",
+  "readiness_v0_2_json_blob": "7708709840f2f3b4317a7968987b1a280f143b70",
+  "stage": "RPE-01",
+  "closes": ["N4", "NF-D"],
+  "authority": {
+    "implementation_authorized": true,
+    "scope": "GOVERNED_JSON_SCHEMA_GUARD_ONLY",
+    "adopted_p5e_contract_mutation_authorized": false,
+    "adopted_p5e_model_mutation_authorized": false,
+    "p5d4_runtime_mutation_authorized": false,
+    "real_remote_io_authorized": false,
+    "real_p5d4_state_mutation_authorized": false,
+    "vault_or_current_mutation_authorized": false,
+    "rpe02_or_later_implementation_authorized": false,
+    "real_p5e_authorized": false
+  },
+  "guard_api": {
+    "input_authority": "EXPLICIT_RAW_JSON_PLUS_EXPLICIT_GOVERNED_SCHEMA",
+    "environment_authority_forbidden": true,
+    "cli_authority_forbidden": true,
+    "implicit_file_discovery_forbidden": true,
+    "network_forbidden": true,
+    "runtime_state_forbidden": true
+  },
+  "schema_language_v0_1": {
+    "node_kinds": ["object", "array", "string", "integer", "boolean", "null"],
+    "object_closed_by_default_and_required": true,
+    "supported_scalar_constraints": ["const", "enum", "pattern", "minimum", "maximum"],
+    "supported_array_constraints": ["items", "min_items", "max_items", "unique", "ordered_const", "allowed_values"],
+    "schema_definition_itself_strictly_validated": true
+  },
+  "mandatory_breakers": [
+    "DUPLICATE_OBJECT_MEMBER_CONTRADICTORY_AUTHORITY",
+    "DUPLICATE_NESTED_MEMBER",
+    "UNKNOWN_TOP_LEVEL_KEY",
+    "UNKNOWN_NESTED_AUTHORITY_KEY",
+    "UNKNOWN_NESTED_TIMING_KEY",
+    "UNKNOWN_NESTED_QUEUE_KEY",
+    "NAN_CONSTANT",
+    "POSITIVE_INFINITY_CONSTANT",
+    "NEGATIVE_INFINITY_CONSTANT",
+    "FLOAT_WHERE_INTEGER_REQUIRED",
+    "SCIENTIFIC_FLOAT_WHERE_INTEGER_REQUIRED",
+    "BOOLEAN_WHERE_INTEGER_REQUIRED",
+    "INTEGER_WHERE_BOOLEAN_REQUIRED",
+    "UNKNOWN_ENUM_VALUE",
+    "DUPLICATE_NORMATIVE_LIST_MEMBER",
+    "UNKNOWN_NORMATIVE_LIST_MEMBER",
+    "NORMATIVE_ORDER_CHANGE",
+    "MISSING_REQUIRED_KEY",
+    "ADJACENT_CONFIG_UNKNOWN_AUTHORITY_KEY",
+    "ADJACENT_CONFIG_UNGOVERNED_ENVIRONMENT_OVERRIDE_KEY",
+    "ADJACENT_CONFIG_UNGOVERNED_CLI_OVERRIDE_KEY",
+    "SCHEMA_DEFINITION_UNKNOWN_KEY",
+    "SCHEMA_DEFINITION_WRONG_TYPE",
+    "SCHEMA_DEFINITION_UNSUPPORTED_KIND"
+  ],
+  "p5e_contract_schema_policy": {
+    "all_object_levels_closed": true,
+    "all_required_keys_exact": true,
+    "strict_json_types": true,
+    "normative_lists_unique": true,
+    "real_end_to_end_stages_order_frozen": true,
+    "known_normative_lists_use_closed_allowed_values": true,
+    "unknown_authority_claim_timing_queue_members_fail": true,
+    "contract_bytes_remain_unchanged": true
+  },
+  "mutation_sweep": {
+    "required": true,
+    "operators": [
+      "add unknown key at every object node",
+      "remove required key at every object node",
+      "change one leaf to a different JSON type",
+      "duplicate selected raw JSON member names",
+      "inject NaN/Infinity constants",
+      "duplicate each normative list member",
+      "replace one allowed normative list member",
+      "reorder real_end_to_end_stages"
+    ],
+    "exit_criterion": "ALL_PREREGISTERED_SCHEMA_MUTATIONS_REJECTED_WITHOUT_USING_P5E_CONTRACT_BLOB_BINDING"
+  },
+  "qualification_requirements": [
+    "RED persisted before implementation",
+    "guard module has no os.environ/sys.argv/argparse/network/runtime-state authority",
+    "schema definition validator is fail-closed",
+    "P5-E adopted contract passes through the governed schema",
+    "P5-E adopted contract blob is unchanged",
+    "all mandatory breakers pass",
+    "mutation sweep has zero survivors",
+    "targeted existing P5-E contract/adversarial tests remain green",
+    "guard implementation blob and P5-E schema blob are persisted in qualification evidence"
+  ],
+  "stop": "EXTERNAL_REVIEW_AND_HUMAN_ADOPTION_REQUIRED_BEFORE_RPE02"
+}
diff --git a/tools/obsidian_projection/rpe01_governed_closed_schema_qualification_v0_1.json b/tools/obsidian_projection/rpe01_governed_closed_schema_qualification_v0_1.json
new file mode 100644
index 0000000..782e4ef
--- /dev/null
+++ b/tools/obsidian_projection/rpe01_governed_closed_schema_qualification_v0_1.json
@@ -0,0 +1,62 @@
+{
+  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_GOVERNED_CLOSED_SCHEMA_QUALIFICATION_V0_1",
+  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
+  "date": "2026-10-02",
+  "base_adopted_readiness_head": "d904eb61d9b704dc8ac38da445eb1cd491a58b33",
+  "preregistration_blob": "406e67da3ab197c5a9ae4b3e971368549af6e1da",
+  "red_test_blob": "803709c26769fc9889b4ac1e47c0dd8df2782580",
+  "red_report_blob": "b3a7df32198fd5a618f927c83d04d5f3a6491050",
+  "guard_blob": "3f61b9191e0ee7fb8c18fdecf60f45c586c74629",
+  "p5e_schema_blob": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
+  "green_test_blob": "391663ee2b8634c0221b5352c8d1242bfdb3c04e",
+  "mutation_sweep_test_blob": "bad495950ddce5c171cac4c667e40654c6673724",
+  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
+  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
+  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
+  "results": {
+    "rpe01_targeted_tests": "22/22 PASS",
+    "schema_mutation_sweep": {
+      "attempted": 433,
+      "survivors": 0
+    },
+    "p5e_plus_rpe01_targeted_regression": "89/89 PASS",
+    "contract_diff_from_adopted_readiness_head": 0,
+    "model_diff_from_adopted_readiness_head": 0,
+    "p5d4_runtime_diff_from_adopted_readiness_head": 0
+  },
+  "qualified_properties": [
+    "duplicate JSON members rejected before dictionary construction",
+    "NaN and +/-Infinity rejected",
+    "closed object key sets at every covered P5-E contract object depth",
+    "strict integer/boolean/string/null typing",
+    "float/scientific-float values rejected where integer is required",
+    "closed enum capability",
+    "normative list uniqueness",
+    "closed normative list vocabulary",
+    "real_end_to_end_stages exact order",
+    "schema definition itself strictly parsed and strictly validated",
+    "guard source contains no environment/CLI/network/filesystem-discovery authority",
+    "P5-E schema source binding matches adopted P5-E contract Git blob",
+    "adjacent configuration unknown authority/environment/CLI override keys rejected by closed schema"
+  ],
+  "guard_binding_policy": {
+    "this_guard_blob_is_the_qualified_guard_identity": "3f61b9191e0ee7fb8c18fdecf60f45c586c74629",
+    "this_p5e_schema_blob_is_the_qualified_schema_identity": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
+    "any_guard_or_schema_change_requires_requalification": true
+  },
+  "real_state_fingerprints_unchanged": {
+    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
+    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
+    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
+  },
+  "claim_boundary": {
+    "rpe01_implemented": true,
+    "rpe01_qualified_for_external_review": true,
+    "rpe01_human_adopted": false,
+    "rpe02_opened": false,
+    "real_p5e_qualified": false,
+    "real_p5e_authorized": false
+  },
+  "next_gate": "EXTERNAL_REVIEW_THEN_HUMAN_ADOPTION",
+  "stop": true
+}
~~~~

# SOURCE: READINESS V0.2 HUMAN ADOPTION
Path: GOVERNANCE/REAL-P5E-PRE-EXECUTION-READINESS-V0.2-HUMAN-ADJUDICATION-2026-10-02.md
~~~~
# REAL P5-E â€” PRE-EXECUTION READINESS V0.2 â€” HUMAN ADJUDICATION

Date: 2026-10-02

## Human decision

The human authority adopts:

`REAL P5-E â€” PRE-EXECUTION READINESS V0.2`

after external delta-review:

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

with no blocking finding.

The adopted normative state is:

`REAL_P5E_PRE_EXECUTION_READINESS_V0_2 = QUALIFIED_AND_HUMAN_ADOPTED`

This adoption does not open or qualify REAL P5-E execution.
## Binding pre-adoption identity

This adoption is bound to:

```text
PRE-ADOPTION HEAD
= 878a0a6f0fbf65914dfa04b21ec0c6bdb9992d2b

READINESS V0.2 JSON
= 7708709840f2f3b4317a7968987b1a280f143b70

READINESS V0.2 REPORT
= 0ba9af17f0d62045fec4c5923cc876aedd772fb7

P5-E ADOPTED CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E ADOPTED SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac
```

Branch at adoption:

`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.
## Adopted dependency DAG

```text
RPE-01 â€” N4 GOVERNED CLOSED SCHEMA
       â”œâ†’ RPE-02 â€” N5 + REAL-TIME REPRESENTATION
       â””â†’ RPE-03 â€” NB5 ANCESTRY CLASSIFIER

RPE-02 + RPE-03
       â†’ RPE-04 â€” NB2 + NB3 REAL OBSERVATION ADAPTER
       â†’ RPE-05 â€” FINITE FIXED-RATE TIMED RUNNER
       â†’ RPE-06 â€” NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
       â†’ separate human execution authorization
```

The DAG is adopted as the normative readiness ordering.

RPE-02 and RPE-03 may progress independently only after RPE-01.

RPE-04 requires both RPE-02 and RPE-03.

RPE-05 follows RPE-04.

RPE-06 remains the final preregistration gate before any separately authorized real experiment.
## Mandatory preregistration requirements from final external review

The non-blocking findings NF-A through NF-K are adopted as mandatory preregistration requirements.

### NF-A â€” local integrated rehearsal before network experiment

RPE-05 must end with a local no-network integrated rehearsal using:
- the real qualified runner;
- the real qualified adapter;
- the real qualified ancestry classifier;
- a local bare Git repository;
- the host's real clock;
- the host's real sleep/wait mechanism;
- an isolated control root.

The integrated rehearsal must exercise the production-oriented orchestration path through P5-D4 on an isolated control root.

Direct P5-D2 calls remain acceptable for unit tests, but are insufficient as the final integrated-path proof.

### NF-B â€” schedule origin, release phase, and sample-size claim

RPE-06 must:
- freeze `schedule_origin_ns` before source release;
- make the schedule origin independent of the release event;
- preregister the release phase relative to the polling grid;
- include a worst-case or otherwise explicitly selected phase;
- state that one real execution is a demonstration, not a general SLA qualification.

No single favorable-phase execution may be presented as proof of a worst-case 60-second SLA.
### NF-C â€” temporal eligibility based on actual start

RPE-02 must define attempt eligibility using:

`attempt_started_at_ns`

not merely the planned `scheduled_at_ns`.

Any rule forbidding observation before source release must also be evaluated against actual attempt start / actual evidence timing, not only against the nominal schedule.

### NF-D â€” remaining closed-schema vectors

RPE-01 must additionally:
- reject non-standard JSON constants such as `NaN` and `Infinity`;
- reject non-integer numeric values where integers are required, including scientific-notation values that parse as floats;
- prohibit normative authority/configuration from ungoverned environment variables;
- prohibit normative authority/configuration from ungoverned CLI arguments;
- prohibit normative authority/configuration from unlisted/unprotected files.

Runner and adapter configuration authority must come only from schema-guarded governed artifacts.

The schema guard itself remains versioned and blob-bound.
### NF-E â€” ancestry-classifier environment isolation

RPE-03 must additionally neutralize or fail closed on:
- `objects/info/alternates`;
- `GIT_ALTERNATE_OBJECT_DIRECTORIES`;
- inherited `GIT_DIR`;
- inherited `GIT_OBJECT_DIRECTORY`;
- other inherited `GIT_*` variables capable of changing the Git object domain or repository context;
- unverified commit-graph influence.

The classifier must disable commit-graph use, for example with `core.commitGraph=false`, unless commit-graph integrity is explicitly qualified.

The rule:

`merge-base --is-ancestor exit 1 â†’ NON_FAST_FORWARD`

applies only after both objects and the verified domain have passed all preregistered checks.

### NF-F â€” remote fetch transaction details

RPE-04 must preregister:
- explicit repository URL;
- explicit refspec;
- no inherited remote fetch rules;
- `--no-tags`;
- `--no-recurse-submodules`;
- `--no-write-fetch-head`;
- `gc.auto=0`;
- exact source of the observed SHA evidence;
- initialization of the object domain before `schedule_origin_ns`;
- isolated namespace update semantics sufficient to observe NON_FAST_FORWARD transitions.

Any local refspec `+` used to update an isolated observation namespace is distinct from and does not authorize force-push to the remote.
### NF-G â€” runner / P5-D4 integration

The integrated RPE-05 qualification must orchestrate the P5-D4 path against an isolated control root.

This requirement exists to validate:
- persistence discipline;
- single-writer behavior;
- normalized-event handoff;
- production-path state-machine integration.

A runner that calls P5-D2 directly may be used for lower-level tests, but that alone does not qualify the integrated production-oriented path.

### NF-H â€” experiment contract inherits adopted semantics

RPE-06 must not create an unconstrained modified copy of the adopted P5-E contract.

The experiment contract must:
- bind by exact blob to the adopted timing/metric semantics;
- explicitly identify what is inherited unchanged;
- substitute only the experiment-specific source identity and explicitly preregistered experiment fields;
- fail closed if the inherited adopted contract identity drifts.

### NF-I â€” expanded push-outcome matrix

RPE-06 must also preregister:

```text
push outcome unknown because of timeout/process termination
+ target later observed
â†’ INCONCLUSIVE

push outcome unknown
+ target not observed
â†’ INVALID_EXPERIMENT

foreign/unexpected head observed on experiment ref
â†’ INVALID_EXPERIMENT

creation-only guard fails
â†’ STOP_BEFORE_RELEASE
```

Exact terminal labels may differ only if separately preregistered before execution.
### NF-J â€” sandbox technical safety and authority

Sandbox repository creation is not implicitly authorized.

Until separately authorized:

`sandbox_repository_creation_authorized = false`

Where technically possible, credentials used by the pilot must be scoped so that they cannot write to the canonical ATDS repository.

Before any real sandbox push, the side-effect audit must cover:
- workflow files and exact blobs;
- workflow `on:` triggers and ref filters;
- repository webhooks;
- organization webhooks relevant to the repository;
- installed GitHub Apps;
- repository/organization rulesets applicable to the experiment ref;
- any other automation capable of side effects.

### NF-K â€” real verdict component

RPE-02 must explicitly recognize that the real timing verdict will be produced by a new nanosecond-native component.

The adopted synthetic model remains immutable and serves as:
- semantic reference;
- parity reference on the common exact-grid domain.

No real pass/fail classification may depend on lossy conversion into the adopted integer-second synthetic model.
## Readiness interpretation after adoption

The final external review established:

```text
BLOCKING_FINDINGS = NONE

BF1
= CLOSED_AT_REQUIREMENT_LEVEL

BF2
= CLOSED_AT_REQUIREMENT_LEVEL
```

This adoption accepts the V0.2 decomposition and the NF-Aâ†’NF-K requirements.

It does not assert that any RPE stage is implemented or qualified.

Current stage state remains:

```text
RPE-01 = NOT_OPENED
RPE-02 = NOT_OPENED
RPE-03 = NOT_OPENED
RPE-04 = NOT_OPENED
RPE-05 = NOT_OPENED
RPE-06 = NOT_OPENED
```
## Explicitly not authorized

This adoption does not authorize:

- implementation of RPE-01;
- implementation of RPE-02;
- implementation of RPE-03;
- implementation of RPE-04;
- implementation of RPE-05;
- implementation of RPE-06;
- real GitHub P5-E polling;
- sandbox repository creation;
- sandbox ref creation;
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

The only operation authorized by the human adoption statement is:

- persist this adjudication record;
- commit and push it;
- verify repository consistency;
- STOP.

No readiness JSON/report, adopted P5-E contract/model, runtime, control state, Vault, or CURRENT artifact may be mutated by the persistence step.

~~~~

# SOURCE: RPE-01 PREDRAFT
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-PREDRAFT.md
~~~~
# RPE-01 â€” N4 GOVERNED CLOSED SCHEMA â€” PRE-DRAFT

Date: 2026-10-02

## Objective

Qualify a reusable, fail-closed JSON schema guard before any later REAL P5-E stage introduces adapter, runner, experiment, or evidence configuration.

RPE-01 closes the structural failure mode identified by N4/NF-D:

> authority must not enter through an unknown key, duplicate key, permissive numeric parsing, list laundering, or an adjacent ungoverned configuration source.

## Starting authority

Base HEAD:
`d904eb61d9b704dc8ac38da445eb1cd491a58b33`

Readiness V0.2:
`QUALIFIED_AND_HUMAN_ADOPTED`

RPE-01 is the only implementation stage opened by the current user instruction.

All later RPE stages remain closed.

## Architecture

The guard is a pure boundary:

```text
explicit raw JSON bytes/text
        +
explicit governed schema
        â†“
strict parser
        â†“
closed recursive schema validator
        â†“
VALIDATED DOCUMENT
or
FAIL-CLOSED
```

The guard does not discover configuration.

It must not read:
- environment variables;
- CLI arguments;
- Git configuration;
- network state;
- P5-D4 control state;
- Vault/CURRENT state.

This makes configuration provenance the caller's explicit responsibility and prevents the guard itself from becoming an alternate authority channel.

## Strict parser requirements

Before dictionary construction:
- reject duplicate object member names;
- reject `NaN`;
- reject `Infinity`;
- reject `-Infinity`;
- require UTF-8 JSON.

Standard JSON floats may parse as floats, but a schema node of type `integer` must reject every float, including `30.0` and `1e2`.

A boolean must never satisfy an integer schema merely because Python `bool` subclasses `int`.

## Schema language V0.1

Supported node kinds:
- object;
- array;
- string;
- integer;
- boolean;
- null.

Object nodes are closed: the exact key set is normative.

Array nodes can freeze:
- item schema;
- minimum/maximum length;
- uniqueness;
- allowed scalar vocabulary;
- exact ordered content when order itself is normative.

Scalar nodes can freeze:
- type;
- const;
- enum;
- regex pattern;
- integer min/max.

The schema definition itself must be strictly validated so an unknown schema-language key cannot silently widen the guard.

## P5-E adopted-contract schema

RPE-01 will create a governed schema for the already adopted P5-E V0.1 contract without modifying the contract bytes.

The schema closes every object depth.

Normative lists will be unique and use a closed vocabulary.

`real_end_to_end_stages` will additionally freeze exact order.

The guard is not a replacement for semantic invariants or object binding.

It provides an independent structural defense against intentionally re-bound future amendments.

## Future REAL P5-E artifacts

The same guard API is intended for later governed JSON artifacts:
- RPE-02 real-time contract/config;
- RPE-04 adapter configuration;
- RPE-05 runner configuration;
- RPE-06 experiment preregistration;
- execution evidence envelopes.

Those future schemas are not created in RPE-01.

RPE-01 only qualifies the guard capability and one concrete schema for the adopted P5-E contract.

## Test-first plan

1. Persist preregistration.
2. Create RED tests while implementation/schema are absent.
3. Persist RED.
4. Implement the minimum pure guard.
5. Generate/review the concrete P5-E schema.
6. Run mandatory adversarial breakers.
7. Run a programmatic mutation sweep over every object node/key and selected typed/list mutations.
8. Re-run targeted existing P5-E tests.
9. Persist qualification evidence with exact blobs.
10. Produce external-review packet.
11. STOP before human adoption/RPE-02.

## Maximum claim

If successful:

`RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE = QUALIFIED_FOR_EXTERNAL_REVIEW`

Not claimed:
- RPE-02 readiness or implementation;
- real-time timing qualification;
- ancestry classification;
- remote adapter;
- timed runner;
- real experiment;
- REAL P5-E.

`REAL_P5E = CLOSED`

~~~~

# SOURCE: RPE-01 PREREGISTRATION
Path: tools/obsidian_projection/rpe01_governed_closed_schema_preregistration_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_GOVERNED_CLOSED_SCHEMA_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "date": "2026-10-02",
  "base_head": "d904eb61d9b704dc8ac38da445eb1cd491a58b33",
  "readiness_adoption_blob": "aeba19575671a37fbdde2bbb994bbe947fed88d8",
  "readiness_v0_2_json_blob": "7708709840f2f3b4317a7968987b1a280f143b70",
  "stage": "RPE-01",
  "closes": ["N4", "NF-D"],
  "authority": {
    "implementation_authorized": true,
    "scope": "GOVERNED_JSON_SCHEMA_GUARD_ONLY",
    "adopted_p5e_contract_mutation_authorized": false,
    "adopted_p5e_model_mutation_authorized": false,
    "p5d4_runtime_mutation_authorized": false,
    "real_remote_io_authorized": false,
    "real_p5d4_state_mutation_authorized": false,
    "vault_or_current_mutation_authorized": false,
    "rpe02_or_later_implementation_authorized": false,
    "real_p5e_authorized": false
  },
  "guard_api": {
    "input_authority": "EXPLICIT_RAW_JSON_PLUS_EXPLICIT_GOVERNED_SCHEMA",
    "environment_authority_forbidden": true,
    "cli_authority_forbidden": true,
    "implicit_file_discovery_forbidden": true,
    "network_forbidden": true,
    "runtime_state_forbidden": true
  },
  "schema_language_v0_1": {
    "node_kinds": ["object", "array", "string", "integer", "boolean", "null"],
    "object_closed_by_default_and_required": true,
    "supported_scalar_constraints": ["const", "enum", "pattern", "minimum", "maximum"],
    "supported_array_constraints": ["items", "min_items", "max_items", "unique", "ordered_const", "allowed_values"],
    "schema_definition_itself_strictly_validated": true
  },
  "mandatory_breakers": [
    "DUPLICATE_OBJECT_MEMBER_CONTRADICTORY_AUTHORITY",
    "DUPLICATE_NESTED_MEMBER",
    "UNKNOWN_TOP_LEVEL_KEY",
    "UNKNOWN_NESTED_AUTHORITY_KEY",
    "UNKNOWN_NESTED_TIMING_KEY",
    "UNKNOWN_NESTED_QUEUE_KEY",
    "NAN_CONSTANT",
    "POSITIVE_INFINITY_CONSTANT",
    "NEGATIVE_INFINITY_CONSTANT",
    "FLOAT_WHERE_INTEGER_REQUIRED",
    "SCIENTIFIC_FLOAT_WHERE_INTEGER_REQUIRED",
    "BOOLEAN_WHERE_INTEGER_REQUIRED",
    "INTEGER_WHERE_BOOLEAN_REQUIRED",
    "UNKNOWN_ENUM_VALUE",
    "DUPLICATE_NORMATIVE_LIST_MEMBER",
    "UNKNOWN_NORMATIVE_LIST_MEMBER",
    "NORMATIVE_ORDER_CHANGE",
    "MISSING_REQUIRED_KEY",
    "ADJACENT_CONFIG_UNKNOWN_AUTHORITY_KEY",
    "ADJACENT_CONFIG_UNGOVERNED_ENVIRONMENT_OVERRIDE_KEY",
    "ADJACENT_CONFIG_UNGOVERNED_CLI_OVERRIDE_KEY",
    "SCHEMA_DEFINITION_UNKNOWN_KEY",
    "SCHEMA_DEFINITION_WRONG_TYPE",
    "SCHEMA_DEFINITION_UNSUPPORTED_KIND"
  ],
  "p5e_contract_schema_policy": {
    "all_object_levels_closed": true,
    "all_required_keys_exact": true,
    "strict_json_types": true,
    "normative_lists_unique": true,
    "real_end_to_end_stages_order_frozen": true,
    "known_normative_lists_use_closed_allowed_values": true,
    "unknown_authority_claim_timing_queue_members_fail": true,
    "contract_bytes_remain_unchanged": true
  },
  "mutation_sweep": {
    "required": true,
    "operators": [
      "add unknown key at every object node",
      "remove required key at every object node",
      "change one leaf to a different JSON type",
      "duplicate selected raw JSON member names",
      "inject NaN/Infinity constants",
      "duplicate each normative list member",
      "replace one allowed normative list member",
      "reorder real_end_to_end_stages"
    ],
    "exit_criterion": "ALL_PREREGISTERED_SCHEMA_MUTATIONS_REJECTED_WITHOUT_USING_P5E_CONTRACT_BLOB_BINDING"
  },
  "qualification_requirements": [
    "RED persisted before implementation",
    "guard module has no os.environ/sys.argv/argparse/network/runtime-state authority",
    "schema definition validator is fail-closed",
    "P5-E adopted contract passes through the governed schema",
    "P5-E adopted contract blob is unchanged",
    "all mandatory breakers pass",
    "mutation sweep has zero survivors",
    "targeted existing P5-E contract/adversarial tests remain green",
    "guard implementation blob and P5-E schema blob are persisted in qualification evidence"
  ],
  "stop": "EXTERNAL_REVIEW_AND_HUMAN_ADOPTION_REQUIRED_BEFORE_RPE02"
}

~~~~

# SOURCE: RPE-01 RED TEST
Path: tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py
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


def load_schema():
    if not P5E_SCHEMA_PATH.exists():
        raise AssertionError(f"required governed schema missing: {P5E_SCHEMA_PATH}")
    g = load_guard()
    return g.parse_schema_json_strict(P5E_SCHEMA_PATH.read_text(encoding="utf-8"))


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
            g.validate_governed_json(json.dumps(document), synthetic_schema())

    def test_float_and_scientific_float_where_integer_required_are_rejected(self):
        self.assert_rejected({"interval_ns": 30.0, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
        g = load_guard()
        raw = '{"interval_ns":1e2,"enabled":false,"mode":"FIXED_RATE","stages":["OBSERVE","STOP"]}'
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(raw, synthetic_schema())

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
        schema = load_schema()
        doc = g.validate_governed_json(current_contract_raw(), schema)
        self.assertEqual(doc["schema"], "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1")

    def test_unknown_keys_at_representative_depths_are_rejected(self):
        g = load_guard()
        schema = load_schema()
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
                    g.validate_governed_json(json.dumps(mutated), schema)

    def test_missing_required_key_is_rejected(self):
        g = load_guard()
        schema = load_schema()
        contract = json.loads(current_contract_raw())
        del contract["authority_boundary"]["evaluation_authorized"]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(contract), schema)

    def test_normative_list_duplicate_unknown_and_order_change_are_rejected(self):
        g = load_guard()
        schema = load_schema()
        contract = json.loads(current_contract_raw())

        duplicate = copy.deepcopy(contract)
        duplicate["claim_boundary"]["forbidden_current_claims"][1] = duplicate["claim_boundary"]["forbidden_current_claims"][0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(duplicate), schema)

        unknown = copy.deepcopy(contract)
        unknown["required_synthetic_cases"][0] = "RPE01_UNKNOWN_CASE"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(unknown), schema)

        reordered = copy.deepcopy(contract)
        stages = reordered["end_to_end_definition"]["real_end_to_end_stages"]
        stages[0], stages[1] = stages[1], stages[0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(reordered), schema)


class SchemaBindingTests(unittest.TestCase):
    def test_p5e_schema_source_binding_matches_current_contract_blob(self):
        import subprocess

        schema = load_schema()
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

# SOURCE: RPE-01 RED EVIDENCE
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-RED.md
~~~~
# RPE-01 â€” N4 GOVERNED CLOSED SCHEMA â€” RED EVIDENCE

Date: 2026-10-02

## Preregistered predecessor

HEAD:
`0c6089b56a438a3faad23af20216f9666685ba0f`

Preregistration blob:
`406e67da3ab197c5a9ae4b3e971368549af6e1da`

## RED test

`tests/obsidian_projection/test_rpe01_governed_closed_schema_v0_1.py`

Created before:
- `tools/obsidian_projection/rpe01_governed_closed_schema.py`;
- `tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json`.

## Command

```text
python -B -m unittest tests.obsidian_projection.test_rpe01_governed_closed_schema_v0_1
```

## Observed result

```text
Ran 19 tests in 0.016s

FAILED (failures=20)

RED_EXIT=1
```

The failure count exceeds the test count because one test contains multiple failing subtests.

## Important RED signal

One test intentionally PASSED:

`ExistingGapEvidenceTests.test_existing_p5e_invariants_do_not_close_unknown_keys`

It inserted:

`authority_boundary.rpe01_probe_unknown_authority = true`

into an in-memory copy of the adopted P5-E contract.

The existing semantic invariant checker accepted that mutated object.

This demonstrates the exact N4 gap independently of P5-E contract blob binding.

## RED failures

All new RPE-01 guard capabilities failed because the guard module and concrete governed schema did not yet exist.

The RED covers:

- duplicate raw JSON members;
- nested duplicates;
- NaN / Â±Infinity;
- strict integer/boolean distinction;
- float/scientific-float rejection where integer is required;
- enum closure;
- list uniqueness;
- normative list order;
- adjacent config unknown authority/environment/CLI override keys;
- schema-language unknown keys;
- schema-language wrong types;
- unsupported schema node kinds;
- P5-E contract exact object-depth closure;
- missing required keys;
- concrete normative-list closure;
- guard purity / no implicit authority channels.

## Authority boundary

No runtime, adopted contract, adopted synthetic model, P5-D4 state, Vault or CURRENT artifact was modified.

`REAL_P5E = CLOSED`

~~~~

# SOURCE: RPE-01 GUARD IMPLEMENTATION
Path: tools/obsidian_projection/rpe01_governed_closed_schema.py
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
    except json.JSONDecodeError as exc:
        raise GovernedSchemaError(f"invalid governed JSON: {exc}") from exc


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


def validate_document(document: object, schema: object) -> Any:
    validated_schema = validate_schema_definition(schema)
    _validate_document_node(document, validated_schema["root"], "$")
    return document


def validate_governed_json(raw: str | bytes, schema: object) -> Any:
    document = parse_json_strict(raw)
    return validate_document(document, schema)

~~~~

# SOURCE: P5-E CONCRETE GOVERNED SCHEMA
Path: tools/obsidian_projection/p5e_v0_1_governed_schema_v0_1.json
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

# SOURCE: RPE-01 MUTATION SWEEP TEST
Path: tests/obsidian_projection/test_rpe01_governed_closed_schema_mutation_sweep_v0_1.py
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
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_baseline = CONTRACT_PATH.read_text(encoding="utf-8")
    guard.validate_governed_json(raw_baseline, schema)

    attempted = 0
    survivors = []

    def expect_reject(label, mutated):
        nonlocal attempted
        attempted += 1
        try:
            guard.validate_governed_json(
                json.dumps(mutated, ensure_ascii=False),
                schema,
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

    return {
        "attempted": attempted,
        "survivors": survivors,
        "survivor_count": len(survivors),
    }


class RPE01MutationSweepTests(unittest.TestCase):
    def test_all_preregistered_contract_schema_mutations_are_rejected(self):
        result = run_sweep()
        self.assertGreater(result["attempted"], 0)
        self.assertEqual(result["survivors"], [])


if __name__ == "__main__":
    result = run_sweep()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["survivor_count"] == 0 else 1)

~~~~

# SOURCE: RPE-01 QUALIFICATION JSON
Path: tools/obsidian_projection/rpe01_governed_closed_schema_qualification_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_RPE01_GOVERNED_CLOSED_SCHEMA_QUALIFICATION_V0_1",
  "status": "QUALIFIED_FOR_EXTERNAL_REVIEW",
  "date": "2026-10-02",
  "base_adopted_readiness_head": "d904eb61d9b704dc8ac38da445eb1cd491a58b33",
  "preregistration_blob": "406e67da3ab197c5a9ae4b3e971368549af6e1da",
  "red_test_blob": "803709c26769fc9889b4ac1e47c0dd8df2782580",
  "red_report_blob": "b3a7df32198fd5a618f927c83d04d5f3a6491050",
  "guard_blob": "3f61b9191e0ee7fb8c18fdecf60f45c586c74629",
  "p5e_schema_blob": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
  "green_test_blob": "391663ee2b8634c0221b5352c8d1242bfdb3c04e",
  "mutation_sweep_test_blob": "bad495950ddce5c171cac4c667e40654c6673724",
  "covered_adopted_p5e_contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
  "covered_adopted_p5e_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
  "covered_p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
  "results": {
    "rpe01_targeted_tests": "22/22 PASS",
    "schema_mutation_sweep": {
      "attempted": 433,
      "survivors": 0
    },
    "p5e_plus_rpe01_targeted_regression": "89/89 PASS",
    "contract_diff_from_adopted_readiness_head": 0,
    "model_diff_from_adopted_readiness_head": 0,
    "p5d4_runtime_diff_from_adopted_readiness_head": 0
  },
  "qualified_properties": [
    "duplicate JSON members rejected before dictionary construction",
    "NaN and +/-Infinity rejected",
    "closed object key sets at every covered P5-E contract object depth",
    "strict integer/boolean/string/null typing",
    "float/scientific-float values rejected where integer is required",
    "closed enum capability",
    "normative list uniqueness",
    "closed normative list vocabulary",
    "real_end_to_end_stages exact order",
    "schema definition itself strictly parsed and strictly validated",
    "guard source contains no environment/CLI/network/filesystem-discovery authority",
    "P5-E schema source binding matches adopted P5-E contract Git blob",
    "adjacent configuration unknown authority/environment/CLI override keys rejected by closed schema"
  ],
  "guard_binding_policy": {
    "this_guard_blob_is_the_qualified_guard_identity": "3f61b9191e0ee7fb8c18fdecf60f45c586c74629",
    "this_p5e_schema_blob_is_the_qualified_schema_identity": "87e45cc75753439879e2902d3cbdbd5d71d8a1b2",
    "any_guard_or_schema_change_requires_requalification": true
  },
  "real_state_fingerprints_unchanged": {
    "observer_events_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "observer_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259"
  },
  "claim_boundary": {
    "rpe01_implemented": true,
    "rpe01_qualified_for_external_review": true,
    "rpe01_human_adopted": false,
    "rpe02_opened": false,
    "real_p5e_qualified": false,
    "real_p5e_authorized": false
  },
  "next_gate": "EXTERNAL_REVIEW_THEN_HUMAN_ADOPTION",
  "stop": true
}

~~~~

# SOURCE: RPE-01 QUALIFICATION REPORT
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-RPE01-GOVERNED-CLOSED-SCHEMA-QUALIFICATION.md
~~~~
# RPE-01 â€” N4 GOVERNED CLOSED SCHEMA â€” QUALIFICATION

Date: 2026-10-02

## Result

```text
RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REVIEW
```

RPE-01 is not yet human-adopted.

RPE-02 and later stages remain closed.

## Lineage

Adopted readiness base:
`d904eb61d9b704dc8ac38da445eb1cd491a58b33`

Preregistration:
`406e67da3ab197c5a9ae4b3e971368549af6e1da`

RED test:
`803709c26769fc9889b4ac1e47c0dd8df2782580`

RED report:
`b3a7df32198fd5a618f927c83d04d5f3a6491050`

## Qualified implementation identities

Guard:
`3f61b9191e0ee7fb8c18fdecf60f45c586c74629`

Concrete P5-E governed schema:
`87e45cc75753439879e2902d3cbdbd5d71d8a1b2`

Green test:
`391663ee2b8634c0221b5352c8d1242bfdb3c04e`

Mutation sweep test:
`bad495950ddce5c171cac4c667e40654c6673724`

Adopted P5-E contract covered by the concrete schema:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

## Test-first evidence

Initial RED:

```text
Ran 19 tests
FAILED
1 intentional PASS demonstrated the pre-RPE01 gap:
unknown authority key survived the old semantic invariant checker.
```

After implementation:

```text
RPE-01 targeted
= 22 / 22 PASS
```

## Mutation sweep

The programmatic sweep did not use P5-E contract blob binding as a rejection mechanism.

It mutated:
- every object node with an unknown key;
- every required object key by deletion;
- every scalar leaf to a different JSON type;
- every concrete normative list with duplicate and unknown members;
- the normative order of `real_end_to_end_stages`.

Observed:

```text
attempted = 433
survivors = 0
```

Therefore the preregistered exit criterion is satisfied:

`ALL_PREREGISTERED_SCHEMA_MUTATIONS_REJECTED_WITHOUT_USING_P5E_CONTRACT_BLOB_BINDING`

## Parser and schema-language properties

The qualified guard rejects before dictionary construction:
- duplicate raw JSON object members;
- nested duplicates;
- `NaN`;
- `Infinity`;
- `-Infinity`.

The validator enforces:
- exact closed object key sets;
- strict JSON type identity;
- bool is not accepted as integer;
- float/scientific-float is not accepted as integer;
- enums;
- regex patterns;
- integer bounds;
- list length;
- list uniqueness;
- closed list vocabulary;
- exact normative order where configured.

The schema definition itself is also parsed through the strict parser and strictly validated.

## Authority-channel property

The guard implementation is pure with respect to configuration authority.

Its source imports none of:
- `os`;
- `sys`;
- `argparse`;
- `socket`;
- `subprocess`;
- HTTP client modules.

It does not use:
- environment variables;
- CLI arguments;
- interactive input;
- implicit file reads;
- network state.

Inputs are only:
- explicit raw JSON;
- explicit schema object/raw schema.

This prevents the guard itself from becoming a hidden adjacent configuration authority.

## Concrete P5-E schema

The concrete P5-E schema:
- closes every current object depth;
- requires every current key;
- enforces strict leaf types;
- freezes the vocabulary and cardinality of current normative lists;
- requires normative list uniqueness;
- freezes exact order for `real_end_to_end_stages`;
- includes source binding to the adopted P5-E contract blob.

The source-binding test recomputes the Git object identity and matches:

`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

The adopted contract bytes were not modified.

## Targeted regression

Executed the current P5-E qualification surface plus RPE-01:

```text
Ran 89 tests
OK
```

Repository deltas relative to the adopted readiness base:

```text
P5-E contract diff = 0
P5-E model diff = 0
P5-D4 runtime diff = 0
```

No full Obsidian suite was required or executed.

## Real state

P5-D4 real-state fingerprints remained:

```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

## Binding

The qualification binds the exact guard blob and P5-E schema blob.

Any modification of either requires a new qualification before the modified artifact may be treated as RPE-01-qualified.

## Maximum claim

```text
RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REVIEW

RPE01_HUMAN_ADOPTION
= PENDING

RPE02
= CLOSED

REAL_P5E
= CLOSED
```

~~~~

# SOURCE: ADOPTED P5-E CONTRACT
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

# SOURCE: P5-E ADVERSARIAL INVARIANT TESTS
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
