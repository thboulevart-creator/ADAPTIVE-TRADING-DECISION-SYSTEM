# Q-RM-12 — TEST-FIRST COMPATIBILITY HARNESS — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Initial breaker blob:** `9a2a11cab31aad52aa9ba48280b43299a56dcf88`  
**Initial workflow blob:** `b00a977d42bb52ae123a7d210eb78ff83142f534`  
**RED baseline run:** `35496588495`  
**RED baseline job:** `106040566517`

Scope: adversarial review of the test-first breaker/harness only.

No Q-RM-12-compatible production runtime or I_A/I_B V0.2 production implementation exists or is authorized.

## 1. Starting verdict

The initial RED baseline is valid:

```text
44 tests collected
44 errors
sole controlled cause = all three future production surfaces absent
```

However a valid RED baseline does not prove that the harness is sufficiently adversarial.

Initial harness verdict:

```text
Q-RM-12 TEST-FIRST HARNESS = FAIL
```

because the following harness defects were demonstrated.

---

## 2. QTF-F01 — GLOBAL AUTOUSE SURFACE GATE MASKS PARTIAL IMPLEMENTATION DEFECTS

The initial breaker uses one autouse fixture that requires all three future modules before any test body can execute.

Consequently, after only one or two future surfaces exist, every test still stops at the remaining missing module(s).

This masks defects in a newly created I_A V0.2 or I_B V0.2 path until the entire three-module stack exists.

### Minimal correction

Remove the global all-surface autouse gate.

Use separate lazy loaders:

```text
_ia2()
_ib2()
_handoff()
```

Each test must require only the surface(s) it actually exercises.

The initial all-absent RED remains valid, but future partial implementation becomes diagnostically observable.

---

## 3. QTF-F02 — STALE-F ATTACK CAN BE A NO-OP WHEN F_A == F_B

The stale-F attack substitutes the opposite path's F artifact.

For a correct equal pair, independently produced F_A and F_B may be byte-identical, including equal artifact integrity digests.

In that case substitution changes nothing and cannot prove run-bound stale-F rejection.

### Minimal correction

Construct a **distinct but individually valid** stale F artifact, for example by a non-semantic ordering mutation that changes the artifact digest/result seal while preserving F validity.

Present that modified result with the original run receipt.

The rejection must then be attributable to exact emitted-result binding.

---

## 4. QTF-F03 — MIX-AND-MATCH ATTACK CAN BE SEMANTICALLY/IDENTICALLY EQUIVALENT

The initial mix-and-match attack replaces F_A with F_B and then recomputes both result seal and receipt.

If F_A and F_B are valid and same-state equal, there is no governed reason for the handoff to reject the newly self-consistent object solely because its bytes originated from the other fixture.

This attack conflates provenance substitution with semantic equality.

### Minimal correction

Split the concerns:

1. **post-run mix-and-match substitution**: swap a distinct F artifact while retaining the original run receipt → must reject;
2. **result/F cross-binding**: use a valid F from a different acquisition/binding state with a recomputed receipt → must reject through acquisition/reconstruction cross-binding.

Do not require rejection merely because two equal F objects were produced by different synthetic fixture helpers.

---

## 5. QTF-F04 — PRE-SEAL INDEPENDENCE CHECK FALSE-POSITIVELY FORBIDS LOCAL FUNCTION NAMES

The initial source scan forbids textual occurrences:

```text
build_freeze_artifact(
validate_freeze_artifact(
```

This would reject an independently authored local function that happens to use the same descriptive name.

The contract forbids **shared project semantic implementation**, not names.

### Minimal correction

Remove name-based prohibition.

Instead prove:

- I_A V0.2 does not import/call the existing shared F production module;
- I_B V0.2 does not import/call it;
- neither imports the other path or Q-RM-12 handoff pre-seal;
- semantic-stage ownership identifies distinct path-owned F units;
- manifest project dependency/import inventory does not contain forbidden shared semantic modules.

---

## 6. QTF-F05 — POST-SEAL HANDOFF SOURCE SCAN USES OVERBROAD "repair" TOKEN

The initial test forbids the substring `repair` anywhere in handoff source.

A harmless reason constant such as `POSTSEAL_REPAIR_FORBIDDEN` would fail even though no repair behavior exists.

Conversely, reconstruction could be hidden behind a differently named helper.

### Minimal correction

Verify the actual surface instead:

- exact closed function signature accepts only two sealed results, two receipts and two external pin objects;
- no common/raw input package argument exists;
- no `build_freeze_artifact` callable is exposed or referenced;
- existing F validation and O comparison are present;
- handoff result construction does not expose semantic-builder entrypoints.

Avoid generic English-token bans.

---

## 7. QTF-F06 — EXECUTION RECEIPT / ISOLATION CROSS-BINDING IS NOT ATTACKED

The formalization requires the run receipt to bind workspace/isolation identity and Q-RM-12 ingress to verify consistency with result isolation evidence.

The initial breaker attacks only `result_seal` mismatch.

A receipt naming a different workspace could pass unnoticed.

### Minimal correction

Add attacks for:

- receipt workspace identity ≠ sealed result isolation identity;
- result isolation evidence claims `other_path_output_readable = true`;
- invalid receipt schema.

All must block before O.

---

## 8. QTF-F07 — PRODUCER PIN ATTACK DOES NOT COVER SOURCE/IDENTITY FIELDS COMPLETELY

The initial self-asserted-manifest attack covers manifest digest but not independently:

- implementation id;
- implementation version;
- source digest;
- receipt schema.

A handoff that ignores one of those externally pinned fields could pass the original harness.

### Minimal correction

Parametrize external provenance attacks over all pinned producer fields and require BLOCKED independently.

---

## 9. QTF-F08 — TERMINAL/NON-REACHED COVERAGE IS INCOMPLETE

The initial breaker tests a QUALIFICATION_BLOCKED path carrying synthetic F.

The formalization separately governs:

```text
QUALIFICATION_BLOCKED
ACQUISITION_REJECTED
ENVIRONMENT_BLOCKED + NOT_REACHED
IMPLEMENTATION_ERROR + NOT_REACHED
```

The harness does not prove the no-qualified-F invariant across all terminal/non-reached status axes.

### Minimal correction

Add structural forged-result attacks covering all terminal/non-reached combinations.

Every such result carrying `bound_f_artifact != null` must be rejected.

Also exercise a real ENVIRONMENT_BLOCKED synthetic context where practical.

---

## 10. QTF-F09 — HANDOFF OUTPUT SCHEMA / O-NOT-INVOKED STATE IS UNDERSPECIFIED

The initial helper only requires:

```text
schema
handoff_id
handoff_version
handoff_result
reason
```

but later tests assume `oracle_result`.

The blocked-before-O state is therefore ambiguous.

### Minimal correction

Freeze an exact handoff result shape:

```text
schema
handoff_id
handoff_version
handoff_result
oracle_result
comparison_scope
reason
```

Allowed:

```text
handoff_result =
SEMANTIC_EQUAL
SEMANTIC_DIFFERENT
BLOCKED

oracle_result =
SEMANTIC_EQUAL
SEMANTIC_DIFFERENT
BLOCKED
NOT_INVOKED
```

Any pre-O ingress rejection must use `oracle_result = NOT_INVOKED`.

---

## 11. QTF-F10 — PRE-SEAL CROSS-PATH CHECK IS TOO TEXTUAL

The initial test scans a few source strings.

Dynamic import/dependency indirection or a manifest-declared shared semantic dependency could evade those strings.

### Minimal correction

Require each implementation manifest to expose a project dependency/import inventory and attack it explicitly.

At minimum forbid, pre-seal:

- opposite Q-RM-12 implementation module;
- Q-RM-12 handoff;
- current shared F production module;
- current O comparator module;
- current opposite V0.1 semantic implementation.

Source-token scan may remain supplemental, but not sole evidence.

---

## 12. QTF-F11 — MUTABILITY TEST COVERS ONLY RESULTS

The handoff could mutate receipts or expected pin objects while leaving result objects unchanged.

### Minimal correction

Deep-copy and verify immutability of:

- left result;
- right result;
- left receipt;
- right receipt;
- left expected pin;
- right expected pin.

---

## 13. Corrective scope

Only the Q-RM-12 test-first breaker and its exact workflow hash lock may change.

Must remain byte-identical:

- I_A V0.1 source/breaker;
- I_B V0.1 source/breaker;
- F source and both qualified breakers;
- O source and both qualified breakers;
- Q-RM-12 qualified formalization artifacts.

Exactly authorized next action:

```text
correct QTF-F01..QTF-F11 only
→ atomically persist corrected breaker + workflow hash lock
→ execute RED re-break
→ require collection PASS
→ require RED solely from absent future surfaces
→ adversarially re-review corrected persisted breaker
→ final persisted-HEAD RED re-break
→ PASS / FAIL / BLOCKED
```

No production code is authorized.
