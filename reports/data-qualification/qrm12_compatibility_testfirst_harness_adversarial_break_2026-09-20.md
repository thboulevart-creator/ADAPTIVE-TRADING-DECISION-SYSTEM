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


---

## 14. Persisted corrected-harness re-break — residual defects

Corrected breaker/workflow atomic commit:

`11e3cbdebea84588c56a3892d0c7210681548a48`

Corrected breaker blob:

`0879576a4dfad6aa76da295fc8f040a602752a08`

Corrected workflow blob:

`d47ef244386bf8ac3c1eb82cdeb18c791cf25e07`

RED re-break:

```text
run = 35496936912
job = 106041529157
collection = 57 tests / PASS
locks = PASS
future surfaces absent = PASS
environment = PASS
breaker = RED
clean worktree = PASS
```

The RED failures are now surface-specific rather than one autouse gate.

The corrected persisted harness materially closes QTF-F01..QTF-F11, but a residual adversarial review demonstrates the following additional weaknesses.

### QTF-R01 — TWO SIDE-SPECIFIC RESULT TESTS STILL REQUIRE BOTH PATHS

`test_a2_qualified_result_shape_and_strict_seal[IB]` and
`test_a3_manifest_and_source_are_externally_pinnable[IB]`
still call `_qualify_pair()`.

Therefore an absent/broken I_A can still mask an otherwise independently testable I_B result/manifest defect.

#### Minimal correction

For those side-parametrized tests, load and execute only the selected side.

### QTF-R02 — ISOLATION CLOSURE ATTACKS ONLY WORKSPACE / OTHER-PATH FLAG

The corrected harness checks:

- workspace mismatch;
- `other_path_output_readable = true`.

It does not independently attack:

- `network_policy != DENY`;
- `ipc_policy != DENY`;
- `cache_policy != PRIVATE_ONLY`;
- runtime read set escaping the pre-seal allowlist.

A handoff that validates only part of isolation evidence could pass.

#### Minimal correction

Parametrize forged sealed isolation evidence over each closure field and require pre-O BLOCKED.

### QTF-R03 — SOURCE + MANIFEST CHECK CAN BOTH MISS DYNAMIC RUNTIME IMPORT

The corrected harness checks source strings and manifest dependency inventory.

A malicious/defective implementation can still:

- omit a dynamic dependency from the manifest;
- construct/import its module name dynamically so the forbidden literal does not appear in source;
- consume the forbidden module at import or execution time.

#### Minimal correction

Add breaker-owned cold-import/runtime audit evidence that records import/open/network/subprocess events and rejects any observed opposite-path, handoff, current shared F/O semantic module or external channel before sealing.

### QTF-R04 — RUN ID PRESENCE IS BOUND BUT NOT VALIDATED

The receipt model contains `run_id`, but no attack proves it must be present and non-empty.

A receipt can therefore satisfy all currently tested fields while failing to bind an actual run identity.

#### Minimal correction

Reject missing/empty/non-string run identity in receipt validation.

## 15. Updated corrective scope

Correct only:

```text
QTF-R01
QTF-R02
QTF-R03
QTF-R04
```

Then atomically persist breaker + workflow lock and execute the final persisted-HEAD RED re-break.

No production code is authorized.


### QTF-R05 — BREAKER-OWNED RUNTIME AUDIT EMITS UNGOVERNED MODULE-NOT-FOUND RED

Final candidate RED run on commit `a0a01d40699b95ff098aaca564b9e161c08b2c44`:

```text
run = 35497084675
job = 106041941665
collection = 70 tests / PASS
70 failed
```

68 failures used the governed expected-RED message for the missing future surface.

Two failures:

```text
test_e4_breaker_owned_runtime_audit_closes_dynamic_preseal_channels[IA]
test_e4_breaker_owned_runtime_audit_closes_dynamic_preseal_channels[IB]
```

escaped as raw `ModuleNotFoundError`.

This is still caused by future surface absence, but it violates the requirement that the final RED be attributable through the breaker-controlled expected-absence boundary rather than an uncontrolled import exception.

#### Minimal correction

In `_audited_fresh_qualify`, detect absent selected future surface before the fresh-import audit and fail with the same governed preimplementation RED classification used by `_ia2()` / `_ib2()`.

Do not weaken the runtime audit once the future surface exists.

## 16. Updated final corrective scope

Correct only:

```text
QTF-R05
```

Then repeat persisted-HEAD RED re-break and require **zero unexpected failure causes**.


---

## 17. Final persisted-head RED re-break

Final corrected breaker/workflow HEAD:

`5733f7d3c213eb73056c8b8b8f3addd95a25a584`

Final breaker:

`breakers/native_bi5_qrm12_compatibility_breaker.py`

Final breaker blob:

`967ab86d517cc8736344bb27154641eb9bac7996`

Final workflow:

`.github/workflows/native-bi5-qrm12-compatibility-preimplementation.yml`

Final workflow blob:

`76bfe3ccaf7cf2fbb359e33d9b5a737709ea22da`

Workflow run:

`35497152042`

Job:

`106042122886`

Results:

```text
exact persisted HEAD / governed blob locks = PASS
future Q-RM-12 production surfaces absent  = PASS
qualification environment                  = PASS
pytest collection                           = 70 tests / PASS
Q-RM-12 breaker execution                   = 70 expected RED
unexpected RED causes                       = 0
clean worktree                              = PASS
```

Every executed failure is explicitly classified as one of:

```text
Q-RM-12 I_A V0.2 surface absent — expected pre-implementation RED
Q-RM-12 I_B V0.2 surface absent — expected pre-implementation RED
Q-RM-12 handoff surface absent — expected pre-implementation RED
```

No raw `ModuleNotFoundError`, collection defect, environment defect, hash-lock defect, syntax defect or unrelated test-body failure remains.

## 18. Final corrected harness properties

The final persisted breaker proves/attacks:

- lazy independent loading of I_A V0.2, I_B V0.2 and handoff surfaces;
- V0.1 implementation identities cannot silently become V0.2 compatibility authority;
- complete unique D/R/M/B/A/Q/F/O identity/reference/integrity bindings;
- no digest-only determinant attribution;
- no common precomputed B slot-count / terminal-fragment authority;
- independent pre-seal F construction and semantic validation ownership;
- no shared pre-seal F/O semantic module dependency;
- closed V0.2 result shape and strict canonical result seal;
- exact embedded F only on QUALIFIED/FROZEN;
- no qualified F on blocked/rejected/not-reached axes;
- externally pinned producer id/version/manifest/source;
- closed execution-receipt schema;
- non-empty run identity;
- run receipt ↔ exact emitted result seal binding;
- receipt workspace ↔ sealed isolation evidence binding;
- network / IPC / cache / runtime-read-set isolation closure;
- breaker-owned fresh-import/runtime audit against dynamic forbidden channels;
- stale-F substitution with a materially distinct valid F artifact;
- foreign/mix-and-match F rejection through exact result/F binding;
- acquisition and reconstruction-tuple cross-binding;
- same-version integrity-conflict precedence over distinct-version classification;
- O determinant gate before O invocation;
- exact handoff result schema with `NOT_INVOKED` for pre-O blocks;
- no post-seal semantic reconstruction surface;
- I_A-only and I_B-only mutant observability;
- F artifact hash/order non-authority;
- no new canonical occurrence/temporal identity;
- input, receipt and expected-pin immutability;
- permission closure.

The static persisted-breaker re-review also confirms:

```text
global autouse all-surface gate = ABSENT
separate _ia2/_ib2/_handoff loaders = PRESENT
breaker-owned runtime audit = PRESENT
stale-F distinct mutation = PRESENT
foreign acquisition F attack = PRESENT
all isolation fields attacked = PRESENT
receipt run-id attack = PRESENT
permission closure = PRESENT
```

No additional internal harness defect was demonstrated after QTF-R05 correction.

## 19. Final test-first verdict

```text
Q-RM-12 TEST-FIRST EXECUTABLE COMPATIBILITY BREAKER / HARNESS = PASS
```

This is a test-first/harness-layer PASS only.

It means:

- the executable contract is persisted;
- its RED state is qualified;
- it is adversarially hardened;
- the RED is caused only by the intentional absence of the future production surfaces.

It does **not** mean any Q-RM-12-compatible production implementation exists or passes.

Current executable state remains:

```text
I_A Q-RM-12 V0.2 production surface = ABSENT
I_B Q-RM-12 V0.2 production surface = ABSENT
Q-RM-12 post-seal handoff runtime    = ABSENT
Q-RM-12 executable run               = BLOCKED
```

No real BI5 acquisition, processing, backtest, paper/broker/live execution or positive P1.1 authorization was created.
