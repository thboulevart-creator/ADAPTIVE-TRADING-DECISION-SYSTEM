# Q-RM-12 — POST-SEAL I_A/I_B → F/O DETERMINISM HANDOFF — FORMALIZATION CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `d4acb8d23c77e02c64662ea4fcefcc5e776a092c`  
**Scope:** formalization only — no Q-RM-12 runtime, no adapter, no shared semantic builder, no F/O/I_A/I_B code modification, no acquisition, no BI5 processing, no backtest, no paper/broker/live execution.

## 0. Status and strict separations

This document formalizes only the missing handoff between independently sealed implementation-path results and the already-qualified F/O surfaces.

Current scoped truths remain:

```text
I_A implementation candidate qualification = PASS
I_B implementation candidate qualification = PASS
F implementation candidate qualification   = PASS
O implementation candidate qualification   = PASS

I_A global executable gate = BLOCKED
I_B global executable gate = BLOCKED
F global executable gate   = BLOCKED
O global executable gate   = BLOCKED
Q-RM-12 executable run     = BLOCKED
```

Strict separations:

```text
ImplementationQualificationResult V0.1
≠ exact F artifact

result seal
≠ semantic oracle

F artifact integrity digest
≠ cross-path semantic equality

post-seal structural extraction
≠ post-seal semantic reconstruction

shared structural schema
≠ shared semantic builder

terminal semantic agreement
≠ qualified-universe equality PASS

candidate
≠ PASS
```

## 1. Observed incompatibility

The current I_A and I_B implementations emit sealed:

`NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_1_CANDIDATE`

with fields including:

- implementation identity/version;
- implementation manifest digest;
- determinant digests;
- materialized acquisition id;
- execution/semantic/freeze statuses;
- qualified occurrences;
- source accounting;
- anomaly outcomes;
- terminal evidence;
- isolation evidence;
- result seal.

The current qualified O surface is:

```text
compare_freeze_artifacts(left_artifact, right_artifact)
```

and each argument must be an exact valid F artifact:

`QUALIFICATION_FREEZE_ARTIFACT_V0_1_CANDIDATE`.

V0.1 implementation results do not contain the exact F object and do not contain enough explicit information to reconstruct it after sealing without introducing new semantic decisions. In particular, the current I_A/I_B input/result surface does not explicitly carry the complete F reconstruction tuple, the complete D acquisition snapshot/completeness evidence, or explicit Q qualification parameters in the exact F form.

Therefore the current V0.1 result schema is **insufficient for Q-RM-12 handoff**.

This does not invalidate the already-qualified I_A/I_B implementation layer. It means only that those candidates are not yet Q-RM-12-compatible.

## 2. Selected handoff model

The selected model is:

```text
common immutable input package V0.2
        ↓                         ↓
 isolated I_A                 isolated I_B
        ↓                         ↓
independent D/R/M/B/A/Q/F   independent D/R/M/B/A/Q/F
        ↓                         ↓
exact F_A built pre-seal     exact F_B built pre-seal
        ↓                         ↓
sealed result A V0.2         sealed result B V0.2
        \                         /
         \                       /
          Q-RM-12 structural ingress
                    ↓
       validate A seal + embedded F_A
       validate B seal + embedded F_B
                    ↓
             extract F_A, F_B
                    ↓
            existing O comparator
```

No post-seal semantic builder exists.

The Q-RM-12 ingress may validate and extract. It may not infer, normalize, repair, complete, or reconstruct missing F semantics.

## 3. Required version-forward result

A future Q-RM-12-compatible implementation path must emit a successor result schema:

`NATIVE_BI5_IMPLEMENTATION_QUALIFICATION_RESULT_V0_2_CANDIDATE`

Because emitting that schema requires changed implementation behavior, **both implementation identities must version-forward independently**. The already-qualified I_A/I_B V0.1 implementation versions may not emit V0.2 results.

A future executable candidate must therefore use new I_A and I_B implementation versions/manifests and requalify them at the Q-RM-12-compatibility scope. The existing V0.1 scoped PASS remains historical and is not reused as authority for changed code.

The exact future executable schema remains to be test-first qualified, but this formalization fixes the minimum semantic contract.

Minimum fields:

```text
schema
implementation_id
implementation_version
implementation_manifest_digest
input_determinant_bindings
materialized_acquisition_id
execution_status
semantic_status
freeze_status
bound_f_artifact
terminal_evidence
isolation_evidence
result_seal
```

### 3.1 Complete determinant bindings

`input_determinant_bindings` must be a closed exact stage set:

```text
D
R
M
B
A
Q
F
O
```

Each binding must contain exactly the qualification-relevant identity/integrity material required to attribute the run:

```text
stage
normative_id
normative_version
immutable_reference
integrity_digest
```

A digest-only map is insufficient for Q-RM-12 because it does not independently expose the normative identity/version/reference that must be checked against F and O.

No missing stage may be filled from implementation constants after sealing.

No post-seal code may invent an immutable reference.

## 4. Required common immutable input package extension

For a path to build its own exact F artifact before sealing, the common immutable input package used by both implementations must explicitly supply, without ambient defaults:

- acquisition-domain identity;
- acquisition declaration version;
- D-declared component membership;
- D completeness evidence binding;
- component identities/declared roles/source/hour bindings;
- immutable component payload references and payload integrity references;
- raw declared component payloads;
- explicit Q qualification parameters;
- complete D/R/M/B/A/Q/F/O determinant bindings;
- qualification-relevant evidence bindings.

The common package **must not supply B/A-derived semantic answers as trusted authority**, including precomputed complete-slot counts or terminal-fragment interpretation.

Each implementation must independently derive from the raw declared payload:

- decompressed physical length;
- complete 20-byte slot count;
- terminal-fragment presence/start/length;
- all B/A consequences later represented in its own F artifact.

The F artifact may contain those derived fields, but they must be populated independently by each path.

This extension is structural input availability, not a shared semantic derivation.

Neither path may obtain these values from:

- the other path;
- O;
- a post-seal bridge;
- filename inference;
- traversal order;
- cache residue;
- implementation defaults.

## 5. Exact timing of F construction

For both I_A and I_B, the branch is exact:

```text
Q = QUALIFIED
→ independent semantic derivation
→ path-private qualified F construction
→ path-private F semantic validation
→ result construction including exact F artifact
→ result seal

Q = QUALIFICATION_BLOCKED or ACQUISITION_REJECTED
→ no qualified F freeze construction
→ bound_f_artifact = null
→ path-local terminal evidence
→ result seal
```

For ENVIRONMENT_BLOCKED / IMPLEMENTATION_ERROR, F is NOT_REACHED and `bound_f_artifact = null`.

Qualified F construction must occur **before result sealing**.

Reason:

- before sealing, F is still part of that path's independently derived semantic output;
- the result seal can bind the exact F object actually produced by that path;
- after sealing, constructing F would require a new actor to interpret sealed fields plus external state, creating a new semantic authority and a mix-and-match surface.

Therefore:

```text
post-seal F construction = forbidden
post-seal F completion   = forbidden
post-seal F repair       = forbidden
```

## 6. Independent F construction requirement

The exact F schema and F contract are common normative specifications.

The semantic code that populates F_A and F_B must remain independently owned by each path.

The two paths may not both call the same project-owned semantic F builder **or the same project-owned semantic F validator/normalizer before sealing**.

Pre-seal F construction and pre-seal F semantic validation must both remain path-private and independently implemented.

The existing shared F validator is allowed only at the post-seal Q-RM-12 ingress, after both results are sealed, where it can validate already-produced artifacts but cannot feed semantic decisions back into either implementation path.

Allowed shared primitives remain non-semantic, for example:

```text
SHA-256
strict JSON library
generic byte/integer primitives
generic compression primitive
schema field-name constants with no defaults/builders
```

Forbidden shared pre-seal helpers include anything that:

- constructs the reconstruction tuple;
- fills acquisition snapshot fields;
- derives qualification parameters;
- converts source accounting into retained membership;
- constructs anomaly semantics;
- constructs retained occurrences;
- repairs/mutates an F candidate;
- creates a semantic projection expected by O.

A shared pure structural schema definition is permitted only if it has:

- no semantic defaults;
- no computed semantic fields;
- no normalization;
- no builder/factory;
- no repair behavior.

## 7. Status-to-F rules

### 7.1 Qualified path

Exact invariant:

```text
execution_status = COMPLETED
semantic_status  = QUALIFIED
freeze_status    = FROZEN
→ bound_f_artifact MUST exist
→ terminal_evidence = null
→ bound_f_artifact MUST validate as exact F
→ artifact_class = QUALIFIED_UNIVERSE_FREEZE
→ freeze_state = FROZEN
→ qualification_outcome = QUALIFIED
```

### 7.2 Qualification blocked

Exact invariant:

```text
execution_status = COMPLETED
semantic_status  = QUALIFICATION_BLOCKED
freeze_status    = NOT_CREATED
→ bound_f_artifact = null
→ terminal_evidence MUST exist
→ terminal_evidence MUST NOT contain a qualified universe
```

### 7.3 Acquisition rejected

Exact invariant:

```text
execution_status = COMPLETED
semantic_status  = ACQUISITION_REJECTED
freeze_status    = NOT_CREATED
→ bound_f_artifact = null
→ terminal_evidence MUST exist
→ terminal_evidence MUST NOT contain a qualified universe
```

### 7.4 Execution not completed

Exact invariant:

```text
execution_status = ENVIRONMENT_BLOCKED or IMPLEMENTATION_ERROR
semantic_status  = NOT_REACHED
freeze_status    = NOT_REACHED
→ bound_f_artifact = null
→ no qualified universe exists
```

Q-RM-12 must never synthesize an F artifact for 7.2–7.4.

## 8. Result/F integrity binding

For a qualified result, the exact F artifact is embedded in the sealed result payload as `bound_f_artifact`.

The result seal covers the complete result payload except the seal field itself, including:

- complete determinant bindings;
- materialized acquisition id;
- statuses;
- the complete embedded F artifact;
- isolation evidence.

The seal normal form is strict canonical JSON:

- UTF-8;
- object keys sorted;
- compact separators;
- non-finite numbers rejected;
- JSON type distinctions preserved;
- duplicate object keys rejected at serialized ingress;
- `result_seal` excluded from its own digest.

The embedded F artifact independently carries its own F `artifact_integrity_digest`.

Required checks are therefore two-layered:

```text
result payload integrity
AND
F artifact integrity/validity
```

Neither digest is used as semantic equality.

The result seal is a non-secret integrity checksum, **not producer authentication**. Producer identity must be established from separately pinned qualification/execution evidence.

For each path, the qualification harness must additionally produce external execution/sealing evidence binding the **exact emitted result** to that isolated run. At minimum that evidence binds:

```text
run identity
implementation id/version
qualified implementation manifest digest
qualified source/blob digest
workspace/isolation identity
exact emitted result_seal
```

Q-RM-12 must reject a presented result if its `result_seal` differs from the seal bound by that run evidence.

This external receipt is provenance evidence only. It does not define semantic equality.

No separate post-seal envelope hash is allowed to become a substitute root of authority.

## 9. Q-RM-12 post-seal ingress

Q-RM-12 may run only after both paths have independently sealed.

For each side separately, ingress must:

1. verify the expected **new** Q-RM-12-compatible implementation identity/version;
2. verify that `implementation_manifest_digest` equals an externally pinned qualified manifest digest for that side;
3. verify external execution evidence that the invoked source/blob digest matches the qualified source identity bound by that manifest;
4. verify that the same external run evidence binds the exact presented `result_seal`;
5. verify the complete result schema;
6. verify structural status invariants;
7. verify strict result-seal integrity;
8. verify the complete D/R/M/B/A/Q/F/O determinant-binding set;
9. verify isolation-evidence presence/closure required by the implementation boundary and consistency with the run receipt;
10. if qualified, validate `bound_f_artifact` with the existing shared F validator **only now, post-seal**;
11. if qualified, cross-bind result and F without reconstructing semantics.

The manifest digest written inside the result is not itself the external pin and cannot establish its own producer identity.

For a qualified side, cross-binding must at minimum prove:

```text
result.materialized_acquisition_id
= F.qualified_universe.acquisition_domain_id

result D/R/M/B/A/Q/F determinant bindings
= exact corresponding F reconstruction_tuple bindings

result semantic_status = QUALIFIED
= F qualification_outcome

result freeze_status = FROZEN
= F freeze_state
```

The O determinant remains outside F and must be validated from the sealed result binding before comparator invocation.

## 10. Same-state gate before O

Before calling O, Q-RM-12 must verify that both sealed results claim the same common qualification state for the handoff-relevant bindings.

At minimum:

- same intended materialized acquisition identity;
- both results are independently valid and sealed;
- complete D/R/M/B/A/Q/F/O bindings are present on both sides.

Conflict precedence is exact:

1. scan **all** D/R/M/B/A/Q/F/O stage pairs whose normative id/version are equal;
2. if any such pair has different immutable reference or integrity digest, block as an integrity conflict;
3. only after that full conflict scan is clean may any legitimate normative id/version difference classify the pair as a distinct/non-same-state run.

This prevents an early distinct-version observation from masking a later same-version integrity conflict.

This gate must not duplicate O semantic equality logic.

It only prevents calling O with an invalid or different contract state.

## 11. O invocation

Only this state reaches O:

```text
A = COMPLETED + QUALIFIED + FROZEN + valid bound F_A
B = COMPLETED + QUALIFIED + FROZEN + valid bound F_B
same-state handoff bindings valid
```

Q-RM-12 then passes exactly:

```text
compare_freeze_artifacts(F_A, F_B)
```

No wrapper-derived semantic projection is passed.

No result-level occurrence/accounting/anomaly fields are used to rebuild F.

O remains unchanged.

## 12. Terminal-state handling

If either path is not `COMPLETED + QUALIFIED + FROZEN`, qualified-universe comparison is unavailable.

Examples:

```text
A QUALIFIED / B QUALIFICATION_BLOCKED
→ no O qualified-universe comparison
→ path divergence remains visible

A QUALIFICATION_BLOCKED / B QUALIFICATION_BLOCKED
→ terminal states may be recorded independently
→ no qualified-universe equality PASS

A ACQUISITION_REJECTED / B ACQUISITION_REJECTED
→ terminal states may be recorded independently
→ no qualified-universe equality PASS

A ENVIRONMENT_BLOCKED / B ENVIRONMENT_BLOCKED
→ not semantic agreement
→ executable prerequisite remains unresolved
```

Q-RM-12 must preserve both side statuses and evidence separately.

It may not normalize them into one generic BLOCKED agreement.

## 13. Post-seal read policy

After both seals exist, the Q-RM-12 coordinator may read only:

- sealed result A;
- sealed result B;
- the exact embedded F artifact in each qualified result;
- fixed validators/contracts needed to verify structure/integrity;
- O comparator output.

It may not read either private workspace to fill missing fields.

It may not inspect the other path's pre-seal intermediate semantic state.

Cross-path debugging may begin only after both seals exist and must not mutate either result.

## 14. One-sided mutant observability

The model preserves one-sided fault detectability because:

- I_A constructs F_A independently before sealing;
- I_B constructs F_B independently before sealing;
- Q-RM-12 does not normalize them into a common semantic object;
- O compares the two exact F artifacts.

Therefore an I_A-only or I_B-only mutant can produce only one of:

- path-local validation failure;
- result/F binding failure;
- O `SEMANTIC_DIFFERENT`;
- O `BLOCKED` for a noncomparable/invalid F state.

A shared post-seal semantic builder is forbidden because it could homogenize both sides and mask such a mutant.

## 15. Non-authorities

The following remain explicitly non-authoritative for semantic equality:

```text
source witness
traversal order
array order
worker partition
cache layout
temporary path
serialized byte order
result_seal digest
F artifact byte/integrity hash
adapter output
shared helper output
```

Integrity digests may prove self-consistency/binding only.

They may not replace O semantic comparison.

## 16. Current V0.1 compatibility verdict

Current I_A/I_B V0.1 implementation results are not sufficient for this handoff because they do not contain the exact pre-seal F artifact or the complete explicit handoff bindings required above.

Therefore:

```text
I_A implementation candidate qualification = PASS at its existing scope
I_B implementation candidate qualification = PASS at its existing scope

I_A Q-RM-12 compatibility = BLOCKED
I_B Q-RM-12 compatibility = BLOCKED
```

No prior scoped PASS is revoked.

A future executable Q-RM-12 step must version forward the implementation-result/input boundary and requalify that new compatibility surface before any real Q-RM-12 execution.

## 17. Permission boundary

Nothing here authorizes:

```text
native BI5 download
real BI5 processing
real acquisition
real backtest
paper
broker
live
positive P1.1 authorization
```

## 18. Candidate verdict before adversarial break

```text
Q-RM-12 HANDOFF FORMALIZATION CANDIDATE
= PERSISTED CANDIDATE ONLY

Q-RM-12 formalization
= NOT YET QUALIFIED

Q-RM-12 executable run
= BLOCKED
```

## 19. Required adversarial break

Attack at minimum:

- post-seal F construction from V0.1 fields;
- stale F artifact substitution;
- F_A/F_B mix-and-match;
- recomputed result seal after F substitution;
- determinant digest-only ambiguity;
- same normative version with different immutable reference;
- legitimate different version hidden by later conflict;
- O determinant mismatch while F artifacts otherwise match;
- terminal status normalized into generic BLOCKED agreement;
- terminal result given a synthetic qualified F artifact;
- both paths sharing the same semantic F builder;
- shared schema containing semantic defaults;
- adapter reconstructing acquisition snapshot;
- adapter deriving Q parameters;
- result/F acquisition identity mismatch;
- result/F reconstruction-tuple mismatch;
- missing F artifact on QUALIFIED result;
- F artifact present on NOT_CREATED/NOT_REACHED result;
- one-sided mutant hidden by common bridge;
- artifact integrity hash used as semantic oracle;
- source witness/traversal/serialized order promoted to identity;
- pre-seal read of opposite path output;
- permission leakage.

No production code may be created during this break.
