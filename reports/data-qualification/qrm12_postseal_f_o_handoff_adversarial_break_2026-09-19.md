# Q-RM-12 — POST-SEAL I_A/I_B → F/O HANDOFF — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Candidate commit:** `65bd16e20722c8bf9c9b342fb960d6449f8a6e27`  
**Candidate:** `reports/data-qualification/qrm12_postseal_f_o_handoff_formalization_candidate_2026-09-19.md`

Scope is documentary/formalization only. No Q-RM-12 runtime, adapter, shared semantic builder, F/O/I_A/I_B code change, acquisition, BI5 processing or backtest was used.

## 1. Pre-break verdict

The persisted candidate correctly selected the high-level model:

```text
independent path semantics
→ exact path-private F artifact before seal
→ sealed result
→ post-seal validation/extraction only
→ unchanged O comparator
```

However the persisted text is not yet sufficient for PASS.

```text
Q-RM-12 FORMALIZATION CANDIDATE = FAIL
Q-RM-12 EXECUTABLE RUN         = BLOCKED
```

## 2. QRM12-F01 — COMMON_INPUT_PRECOMPUTES_B_DERIVED_F_FIELDS

The candidate section 4 requires the common immutable input package to supply:

```text
complete-slot counts
terminal-fragment state
```

Those values are not neutral transport metadata in this boundary. They are consequences of physical framing/interpretation that each implementation is required to derive independently from the raw declared payload.

If both paths trust one shared precomputed slot count or terminal-fragment interpretation, a common upstream error can be injected into both F artifacts before O and remain invisible as a one-sided implementation defect.

### Attack

Provide one raw payload whose true decompressed byte length yields:

```text
N complete 20-byte slots
+
terminal fragment
```

but place a shared common-package field claiming:

```text
N+1 complete slots
no terminal fragment
```

If both implementations consume that shared derived value, the independence objective is bypassed.

### Verdict

```text
QRM12-F01 = FAIL
```

### Minimal correction

The common package may supply D-declared component membership, immutable payload bytes/references/integrity, declared role/source/hour and D completeness evidence.

Each path must independently derive and verify:

- decompressed physical length;
- complete 20-byte slot count;
- terminal-fragment presence/start/length;
- every B/A consequence used in its own F artifact.

The F artifact may contain those fields, but they may not be accepted as common precomputed semantic authority.

## 3. QRM12-F02 — IMPLEMENTATION_VERSION_CAN REMAIN V0.1 WHILE OUTPUT CONTRACT CHANGES

The candidate requires a V0.2 result schema but does not explicitly require the I_A and I_B implementation versions/manifests to version-forward.

That permits a changed executable implementation to continue identifying itself as the already-qualified V0.1 candidate while emitting materially different handoff semantics.

### Attack

Modify I_A to emit the new V0.2 result and embedded F artifact while keeping:

```text
implementation_version =
I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_V0_1_CANDIDATE
```

A label-only ingress check can then confuse the old scoped PASS with the new compatibility surface.

### Verdict

```text
QRM12-F02 = FAIL
```

### Minimal correction

Any implementation code/output-contract change required for Q-RM-12 compatibility must advance the implementation version and manifest identity separately for I_A and I_B.

The existing V0.1 implementation candidates remain qualified only at their already-recorded scope.

## 4. QRM12-F03 — RESULT PRODUCER IDENTITY IS SELF-ASSERTED

The candidate ingress says to verify implementation identity/version and result-seal integrity, but does not explicitly require the observed implementation manifest/source identity to equal an externally pinned qualified identity.

A self-labelled object can therefore claim the expected implementation id/version, claim an arbitrary manifest digest and recompute its non-secret result seal.

The seal is integrity, not producer authentication.

### Attack

Construct a result object outside the qualified I_A runtime with:

- expected I_A id/version strings;
- attacker-chosen manifest digest;
- structurally valid statuses;
- valid F artifact;
- recomputed result seal.

Without an external pinned manifest/source check, the object can pass a purely self-contained integrity check.

### Verdict

```text
QRM12-F03 = FAIL
```

### Minimal correction

Q-RM-12 ingress must require external qualification evidence that pins, per side:

- expected implementation id/version;
- exact qualified implementation manifest digest;
- exact qualified source digest/blob identity;
- execution evidence showing the invoked runtime matched those pins.

The result's own manifest field must equal the pinned value but cannot create the pin.

## 5. QRM12-F04 — SAME-STATE CONFLICT PRECEDENCE IS UNDERSPECIFIED

The candidate requires both:

- legitimate different-version state to be treated as non-same-state;
- same-id/same-version immutable-reference or integrity conflict to block.

It does not define precedence when both conditions exist in different stages.

This recreates the class of defect already demonstrated and corrected in O-F01.

### Attack

Construct result A/B bindings with:

```text
D = legitimate different normative version
R = same id/version but different immutable reference/integrity
```

A first-difference implementation could classify only `DISTINCT_QUALIFICATION_STATE` and hide the R integrity conflict.

### Verdict

```text
QRM12-F04 = FAIL
```

### Minimal correction

For D/R/M/B/A/Q/F/O:

1. first scan every same-id/same-version pair for immutable-reference/integrity conflicts;
2. any such conflict blocks immediately;
3. only after the full conflict scan is clean may legitimate id/version differences classify the run as distinct/non-same-state.

## 6. QRM12-F05 — RESULT SEAL NORMAL FORM IS NOT FIXED

The candidate states that the result seal covers the complete payload but does not define a strict normal form.

This leaves ambiguity around:

- non-finite numeric values;
- boolean versus number distinctions;
- object-key order;
- serialized representation differences.

The O implementation already demonstrated why Python-native equality is not sufficient for strict persisted semantics.

### Verdict

```text
QRM12-F05 = FAIL
```

### Minimal correction

Define result sealing over strict canonical JSON:

- UTF-8;
- object keys sorted;
- compact separators;
- non-finite values rejected;
- JSON type distinctions preserved;
- duplicate object keys rejected at any serialized ingress;
- seal field excluded from its own digest.

The seal remains integrity only and must never become semantic equality.

## 7. QRM12-F06 — QUALIFIED-FREEZE CONSTRUCTION AND TERMINAL HANDLING ARE TEXTUALLY AMBIGUOUS

Section 5 says both paths perform path-private F construction before sealing.

Section 7 simultaneously requires `bound_f_artifact = null` for QUALIFICATION_BLOCKED / ACQUISITION_REJECTED.

Without an explicit branch point, an implementation could either:

- construct a terminal F artifact and then discard it;
- treat that terminal artifact as the bound artifact;
- skip F entirely.

That ambiguity matters because O accepts the general F schema but qualified-universe comparison must never be invented for terminal states.

### Verdict

```text
QRM12-F06 = FAIL
```

### Minimal correction

Fix the branch explicitly:

```text
Q = QUALIFIED
→ path-private qualified F freeze construction
→ validate exact F
→ embed bound_f_artifact
→ seal

Q = QUALIFICATION_BLOCKED or ACQUISITION_REJECTED
→ no qualified F freeze is created
→ bound_f_artifact = null
→ path-local terminal evidence only
→ seal
```

Q-RM-12 never constructs or injects a terminal F object post-seal.

## 8. Attacks that the persisted candidate already survives conceptually

No additional correction is currently required for these candidate properties:

- post-seal semantic reconstruction is forbidden;
- shared semantic F builder is forbidden;
- shared structural schema with no defaults/builders is allowed;
- F artifact hash is not semantic equality;
- O remains unchanged and receives direct F_A/F_B only;
- terminal states cannot create qualified-universe PASS;
- cross-path reads are forbidden before both seals exist;
- result/F acquisition and reconstruction bindings are required;
- one-sided mutants are not normalized through a common semantic bridge;
- permission boundary remains closed.

## 9. Current verdict

```text
Q-RM-12 formalization candidate = FAIL
Q-RM-12 executable run         = BLOCKED
```

Exactly authorized next action:

```text
correct QRM12-F01..F06 only
→ persist corrected formalization
→ exact persisted-HEAD documentary re-break
→ PASS / FAIL / BLOCKED
```

No production code is authorized.


## 10. QRM12-F07 — SHARED PRE-SEAL F VALIDATOR CAN BECOME COMMON SEMANTIC AUTHORITY

The candidate requires each path to perform "path-private F validation" before sealing, but it does not explicitly forbid both paths from calling the same project-owned semantic F validator at that pre-seal stage.

A common pre-seal validator can itself encode the same F acceptance/rejection defect for both paths and therefore act as shared semantic authority before independent sealing.

### Attack

Let I_A and I_B independently construct different internal F candidates, but route both through one shared project-owned pre-seal F semantic validator/normalizer that silently accepts or rewrites the same defect.

The pair can then become artificially homogeneous before O.

### Verdict

```text
QRM12-F07 = FAIL
```

### Minimal correction

Pre-seal F construction **and pre-seal F semantic validation** must remain path-private/independently implemented.

The existing shared F validator is permitted only at the post-seal Q-RM-12 ingress, where it validates already-sealed artifacts and cannot feed semantic decisions back into either implementation path.

Updated authorized correction set:

```text
QRM12-F01..F07 only
```
