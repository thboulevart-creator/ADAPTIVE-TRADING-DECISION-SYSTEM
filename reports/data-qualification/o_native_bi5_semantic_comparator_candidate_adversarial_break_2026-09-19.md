# O — NATIVE BI5 SEMANTIC-COMPARATOR IMPLEMENTATION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Initial implementation commit:** `049e13ab18348699e7b7982d00c825562438beb9`  
**Initial qualification-runner commit:** `39974a48ad569531dd43e318d77206946d5c775d`

Production source:

`src/native_bi5_semantic_universe_comparator.py`

Initial source blob:

`837ff71dd54e0068047604c327ab53db71e32fb1`

Frozen O breaker:

`breakers/native_bi5_o_semantic_comparator_breaker.py`

Frozen breaker blob:

`9e1d897329a15f8b26172558b6579d61d9ba3820`

F boundary remained byte-identical:

```text
src/native_bi5_freeze_persistence.py
= 199b07929fe8ec40d719b001b0321d1f26c8faab

breakers/native_bi5_f_freeze_persistence_breaker.py
= 3d9eb75c2f4e988c984da67af0af344d3dc24148

breakers/native_bi5_f_freeze_persistence_adversarial.py
= c4c499d5e76e15a8fdcaeb91dde80beadad6487a
```

No real BI5 input, acquisition or backtest was used.

---

## 1. Initial frozen-breaker qualification

Workflow:

`Native BI5 O Semantic Comparator Candidate`

Run:

```text
run = 35463859646
job = 105952401656
```

Result:

```text
frozen O breaker = 77 passed
```

All source/breaker/F/contract locks, qualification-environment checks and clean-worktree checks passed.

The initial green frozen breaker is not sufficient for implementation PASS.

---

## 2. O-F01 — DISTINCT_VERSION_CAN_MASK_SAME_VERSION_INTEGRITY_CONFLICT

The determinant gate returns immediately when it sees the first legitimate version difference.

Current stage order starts with D.

Therefore this combined state can be classified as merely:

```text
DISTINCT_QUALIFICATION_STATE
```

even when a later determinant simultaneously contains:

```text
same normative_id
same normative_version
different immutable reference or integrity digest
```

The latter is a normative-version integrity conflict and must never be hidden by an unrelated distinct version.

### Attack

Construct a right artifact with:

```text
D materialization version = legitimate synthetic V0.2
R id/version              = unchanged
R integrity digest        = changed
```

Both artifacts are individually valid F artifacts.

Expected O result:

```text
oracle_result = BLOCKED
qualified_universe_comparison = BLOCKED
comparison_scope = NORMATIVE_VERSION_INTEGRITY_CONFLICT
reason = NORMATIVE_VERSION_INTEGRITY_CONFLICT
```

### Verdict

```text
O-F01 = FAIL
```

### Minimal correction

Scan all same-id/same-version determinant pairs for binding conflicts first.

Only if no such conflict exists may any legitimate id/version difference produce `DISTINCT_QUALIFICATION_STATE`.

---

## 3. O-F02 — COMPONENT_DIAGNOSTIC_METADATA_IS_TREATED_AS_MATERIALIZED_IDENTITY

The current materialized-acquisition gate canonicalizes the entire component object.

F permits extra component metadata while O section 18 explicitly declares fields such as:

```text
worker id
worker partition
cache layout
temporary path
artifact filename
Git blob identity
```

non-semantic.

Therefore adding such metadata to an otherwise identical component changes the whole-object canonicalization and incorrectly blocks comparison.

### Expected behavior

Same exact materialized component semantics plus only diagnostic/execution metadata difference:

```text
SEMANTIC_EQUAL
```

### Verdict

```text
O-F02 = FAIL
```

### Minimal correction

Project components only onto the F/O semantic component fields:

```text
component_manifest_entry_id
declared_role
instrument_source_identity
declared_hour_bucket_utc
immutable_payload_reference
payload_integrity_reference
materialization_status
complete_slot_count
terminal_fragment semantic fields
```

Do not compare incidental execution/diagnostic metadata.

---

## 4. O-F03 — COMPLETENESS_DIAGNOSTIC_METADATA_IS_TREATED_AS_MATERIALIZED_IDENTITY

The current materialized-acquisition gate compares the complete `completeness_evidence` dictionary.

F requires and validates the semantic binding:

```text
immutable_reference
integrity_digest
```

but may preserve extra evidence diagnostics.

O section 18 makes worker/runtime/path metadata non-semantic.

Thus an added diagnostic field in completeness evidence can currently turn an otherwise same-state comparison into a blocked acquisition-state mismatch.

### Expected behavior

Only diagnostic/execution metadata difference in completeness evidence:

```text
SEMANTIC_EQUAL
```

### Verdict

```text
O-F03 = FAIL
```

### Minimal correction

Compare the exact semantic completeness binding only:

```text
immutable_reference
integrity_digest
```

while ignoring explicitly non-semantic execution/diagnostic extras.

---

## 5. Current implementation verdict

```text
frozen O breaker = PASS
adversarial implementation review = FAIL

O implementation candidate = FAIL
O global gate = BLOCKED
```

Exactly authorized next action:

```text
encode O-F01..O-F03 in a supplemental adversarial breaker
→ demonstrate persisted RED
→ correct O-F01..O-F03 only
→ frozen + supplemental persisted-head re-break
```

The frozen O breaker and all F assets must remain byte-identical.

No real BI5 data, acquisition, backtest, paper/broker/live action is authorized.


---

## 6. Executable supplemental break

Supplemental breaker:

`breakers/native_bi5_o_semantic_comparator_adversarial.py`

Initial supplemental breaker blob:

`89fb272b133800ecf4366c6b117a18c0acafcef2`

Workflow:

`Native BI5 O Semantic Comparator Adversarial`

Run:

```text
run = 35463977481
job = 105952715015
```

Results:

```text
frozen O breaker       = 77 passed
supplemental adversary = 3 failed
```

Observed failures map exactly to the demonstrated defects:

```text
O-F01
expected NORMATIVE_VERSION_INTEGRITY_CONFLICT
observed DISTINCT_QUALIFICATION_STATE

O-F02
expected SEMANTIC_EQUAL
observed BLOCKED

O-F03
expected SEMANTIC_EQUAL
observed BLOCKED
```

All exact O/F source and breaker locks, contract locks, qualification-environment checks and clean-worktree checks passed.

Current state:

```text
O frozen breaker = PASS
O supplemental breaker = FAIL
O implementation candidate = FAIL
O global gate = BLOCKED
```

Only O-F01..O-F03 are authorized for correction.


---

## 7. Residual re-break after O-F01..O-F03

Correction commit:

`03eb0a972775f9fba5982ac5525094e1b3bfe7ff`

Corrected source blob:

`482fdb3e609d2d7f8a4028754be04367b71a2c18`

Executable results:

```text
candidate run = 35464054174
job = 105952914637
frozen O breaker = 77 passed

adversarial run = 35464054185
job = 105952914640
frozen O breaker       = 77 passed
supplemental adversary = 3 passed
```

O-F01..O-F03 are materially corrected.

### O-R01 — PYTHON_NUMERIC_EQUALITY_COLLAPSES_DISTINCT_JSON_PARAMETER_TYPES

The same-state gate currently compares:

`qualification_parameters`

using Python mapping equality.

Python defines:

```text
True == 1
```

while JSON preserves these as different semantic types:

```json
true
1
```

F can persist both parameter values as strict JSON.

Thus two otherwise identical valid F artifacts can bind:

```text
left parameter  = true
right parameter = 1
```

and the current O candidate can treat the parameter sets as equal, then return `SEMANTIC_EQUAL`.

Qualification parameters are qualification-relevant state and must be compared with strict persisted JSON semantics, not Python numeric coercion semantics.

### Verdict

```text
O-R01 = FAIL
```

### Minimal correction

Compare qualification parameters through the same strict canonical JSON representation used for semantic projections.

This must preserve:

- object-key order non-authority;
- nested object-key order non-authority;
- JSON type distinctions such as boolean versus number.

Exactly authorized next action:

```text
encode O-R01 in supplemental breaker
→ demonstrate RED
→ correct O-R01 only
→ persisted-head frozen + supplemental re-break
```

F and the frozen O breaker remain unchanged.


---

## 8. Executable O-R01 break

Extended supplemental breaker blob:

`255ff9f02d206815638b5e63e92546e647e826e4`

Workflow run:

```text
run = 35464180340
job = 105953244422
```

Results:

```text
frozen O breaker       = 77 passed
supplemental adversary = 3 passed / 1 failed
```

The sole failure is:

`test_adv_json_parameter_type_distinction_is_qualification_state`

Observed:

```text
left typed_parameter  = true
right typed_parameter = 1
→ SEMANTIC_EQUAL
```

Required:

```text
DISTINCT_QUALIFICATION_STATE
→ BLOCKED
```

All O/F locks, environment checks and clean-worktree checks passed.

Only O-R01 is authorized for correction.
