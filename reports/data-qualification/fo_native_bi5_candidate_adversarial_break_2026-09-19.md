# F + O — ADVERSARIAL BREAK OF FIRST NATIVE-BI5 FREEZE / ORACLE CANDIDATE

**Date:** 2026-09-19  
**Candidate commit under attack:** `3424aefb491f502cade6dd703d9b93a380ca7039`  
**Candidate blob:** `dad8850746f21eb69010c5cfbe8ed9fbd46e2054`  
**Candidate artifact:** `reports/data-qualification/fo_native_bi5_freeze_oracle_candidate_2026-09-19.md`

No acquisition, BI5 download, real-data read, persistence implementation or backtest occurred.

## 1. Attack basis

The persisted candidate was attacked against:

- corrected/re-broken D/R/M;
- corrected/re-broken B/A;
- corrected/re-broken Q;
- Q-RM-07 qualification freeze;
- Q-RM-11 freeze artifact contract;
- Q-RM-12 reconstruction/determinism oracle;
- strict duplicate preservation;
- no physical locator as canonical identity;
- no temporal authority from traversal/serialization order;
- no silent repair;
- no partial qualified universe on blocked/rejected qualification.

The candidate is judged only on whether its own contract permits incompatible conforming interpretations or loses information required by the governed reconstruction/oracle semantics.

---

# 2. Freeze-state attacks that survive

## FO-A01 — blocked Q emits partial qualified universe

Attack:

A run produces 80 apparently valid retained occurrences, then a late A outcome forces Q to `QUALIFICATION_BLOCKED`.

Candidate result:

**SURVIVES.**

The candidate requires:

```text
artifact_class = QUALIFICATION_TERMINAL_EVIDENCE
freeze_state = NOT_CREATED
qualified_universe = null
qualified_occurrence_count = null
```

and forbids presenting the valid prefix as a normative universe.

## FO-A02 — rejected acquisition emits freeze

Attack:

A future explicitly acquisition-fatal anomaly produces `ACQUISITION_REJECTED`.

Candidate result:

**SURVIVES.**

No `QUALIFIED_UNIVERSE_FREEZE` may exist.

## FO-A03 — F self-check fails after Q=QUALIFIED

Attack:

Q claims `QUALIFIED`, but F discovers incomplete accounting or missing reconstruction state.

Candidate result:

**SURVIVES.**

F does not repair or emit a partial freeze; it fails closed with `freeze_state = NOT_CREATED`.

---

# 3. Ordering / identity attacks that survive

## FO-A04 — occurrence array reordered

Same retained semantic occurrences are serialized in a different JSON list order.

**SURVIVES.**

Array position is non-normative.

## FO-A05 — component/anomaly list reordered

**SURVIVES.**

Membership and anomaly relations are explicitly unordered.

## FO-A06 — strict duplicate payloads

Two distinct complete source slots decode to identical logical payload.

**SURVIVES.**

The candidate keeps two occurrences and forbids content deduplication.

## FO-A07 — same payload bag but different multiplicity

```text
[A, A, B]
vs
[A, B]
```

**SURVIVES.**

The unordered occurrence bag compares multiplicity.

## FO-A08 — source witness promoted to canonical identity

Attack:

Implementation exposes `(component_manifest_entry_id, slot_index)` as the final global occurrence ID.

**SURVIVES.**

Candidate explicitly limits it to physical provenance/conformance.

## FO-A09 — JSON index promoted to occurrence identity

**SURVIVES.**

Array index is explicitly non-normative.

## FO-A10 — hidden timestamp sorting

**SURVIVES.**

Neither F nor O grants sorting semantic or temporal authority.

---

# 4. Demonstrated defect FO-F01 — BINARY32_NUMERIC_NORMAL_FORM_UNDERSPECIFIED

Candidate says finite source volumes are persisted as:

```text
integer_coefficient * 2^exponent2
```

and gives a unique rule only for zero:

```text
0 → coefficient=0, exponent2=0
```

Attack:

The exact same finite logical value `1.0` may be emitted by two otherwise conforming implementations as:

```text
implementation A:
coefficient = 1
exponent2 = 0

implementation B:
coefficient = 2
exponent2 = -1
```

Both expressions are mathematically exact.

The current candidate calls the representation "normalized" but does not define the normalization invariant for non-zero values.

O §16 compares normalized logical payloads. Therefore two implementations can represent the same logical binary32 numeric value differently and produce a false `SEMANTIC_DIFFERENT`.

Result:

```text
BREAK — FO-F01
BINARY32_NUMERIC_NORMAL_FORM_UNDERSPECIFIED
```

Required minimal correction:

Define one unique finite binary32 semantic normal form.

For non-zero finite values:

```text
value = coefficient * 2^exponent2

coefficient = signed odd integer
exponent2 = integer
```

All powers of two are factored out of the coefficient.

For zero:

```text
coefficient = 0
exponent2 = 0
```

Thus each finite binary32 numeric value has exactly one semantic pair.

Raw source bits may still be retained separately as provenance.

---

# 5. Demonstrated defect FO-F02 — QUALIFICATION_RELEVANT_ANOMALY_EVIDENCE_NOT_FROZEN

Candidate §7 requires the anomaly semantic entry to contain at minimum:

```text
anomaly_class_id
anomaly_matrix_version
exact normative target
mandatory outcome
acquisition_fatal flag
```

and says diagnostic/provenance material *may* be persisted.

Attack:

Consider:

```text
BI5-A08
TERMINAL_PARTIAL_SLOT_WITH_CONSTRUCTIVE_COMPLETENESS_PROOF
→ REJECT RECORD
```

The difference between A08 and A07 is not the remainder itself.

It is the existence of constructive completeness/locality proof establishing that the terminal fragment cannot imply unseen missing membership.

If F stores only:

```text
class=A08
target=<fragment>
outcome=REJECT RECORD
```

while omitting the exact qualification-relevant proof binding, an independent reconstruction from F cannot determine whether A08 was legitimately applicable or whether the run should have been A07 → `QUALIFICATION_BLOCKED`.

The same issue can arise for other evidence-dependent anomaly decisions, such as exact provenance conflict/completeness facts.

Therefore the current freeze can preserve the *decision label* while losing the evidence necessary to reconstruct and validate that decision.

Result:

```text
BREAK — FO-F02
QUALIFICATION_RELEVANT_ANOMALY_EVIDENCE_NOT_FROZEN
```

Required minimal correction:

For every anomaly whose classification/localisability/outcome depends on evidence, F MUST persist an immutable qualification-evidence binding sufficient to revalidate the decision.

At minimum:

```text
qualification_evidence_refs[]
evidence_role
immutable reference
integrity digest/reference
binding to exact anomaly target
```

For A08 specifically, the exact completeness-proof reference must be frozen.

These proof references are reconstruction evidence.

They do not become occurrence identity.

O must validate their sufficiency before semantic comparison.

Alternative valid proof artifacts need not become semantic occurrence keys merely because their byte hashes differ.

---

# 6. Demonstrated defect FO-F03 — NORMATIVE_VERSION_COLLISION_DIGEST_CONFLICT_UNRESOLVED

Candidate F stores for each determinant:

```text
normative_id
normative_version
immutable artifact reference
integrity digest/reference
```

But O same-state comparability is stated primarily in terms of:

```text
same D/R/M/B/A/Q/F semantic versions + parameters
```

and O §16.1 says semantic identities/versions/parameters must match.

Attack:

Artifact A and artifact B both claim:

```text
format_binding_id =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD

format_binding_version =
..._V0_1_CANDIDATE
```

but the bound normative B artifact digests differ.

Example:

```text
A B-digest = X
B B-digest = Y
X != Y
```

The same declared ID/version now names two different immutable contents.

This is not an ordinary "different version" case.

It is a version-integrity collision / mutation conflict.

Under the current text O can still regard the inputs as same-state comparable because the IDs/versions match, then potentially return `SEMANTIC_EQUAL` over outputs generated from different normative contracts.

That would hide a governance-integrity failure.

Result:

```text
BREAK — FO-F03
NORMATIVE_VERSION_COLLISION_DIGEST_CONFLICT_UNRESOLVED
```

Required minimal correction:

The same-state comparability gate must require exact agreement of the immutable determinant-content binding, not just names/versions.

Rule:

```text
same normative_id + same normative_version
+
different bound integrity digest/content
→ BLOCKED
→ NORMATIVE_VERSION_INTEGRITY_CONFLICT
```

Do not classify this as a valid distinct qualification state under the same version.

A legitimate semantic change requires a new version.

Also distinguish:

```text
normative-input artifact digest
= part of determinant integrity

freeze-output byte digest
= physical artifact integrity only
= not semantic universe equality
```

---

# 7. Source→logical mapping attack

## FO-A11 — same logical payload bag, swapped source mappings

Attack:

Two complete slots contain logical payloads A and B.

Implementation 1 freezes:

```text
slot 1 → A
slot 2 → B
```

Implementation 2 freezes:

```text
slot 1 → B
slot 2 → A
```

The unordered payload bag is equal in both cases.

Candidate result:

**SURVIVES.**

O additionally compares the exact source→logical conformance relation for the current B version.

This catches the mapping defect without declaring slot witness to be final occurrence identity.

---

# 8. Hash / serialization attacks that survive

## FO-A12 — same semantics, different JSON whitespace

**SURVIVES.**

Freeze-output byte hash may differ; O ignores it as semantic equality evidence.

## FO-A13 — byte-identical file used as sole semantic oracle

**SURVIVES.**

Candidate explicitly forbids file/hash equality as the semantic oracle.

## FO-A14 — same semantic inputs, different Git blob SHA due serialization

**SURVIVES.**

Blob SHA is physical artifact integrity only.

---

# 9. Signed-zero attack

Attack:

Two source binary32 volume encodings are +0 and -0.

Under B candidate semantics, logical volume is the exact numeric value represented by the source finite binary32 field.

Both are numeric zero.

Candidate result:

**SURVIVES conceptually.**

The candidate intentionally canonicalizes logical zero while allowing raw source bits to remain provenance.

However FO-F01 must still be corrected so all non-zero finite values also have unique normal form.

---

# 10. Terminal fragment / accounting attacks that survive

## FO-A15 — terminal fragment inserted into complete-slot set

**SURVIVES.**

Candidate keeps terminal fragments outside complete-slot accounting.

## FO-A16 — candidate/reject overlap

**SURVIVES.**

Disjointness is preserved from Q and rechecked by F.

## FO-A17 — silent complete-slot omission

**SURVIVES.**

F requires complete source accounting.

---

# 11. Late correction / history attacks that survive

## FO-A18 — late upstream non-conformance rewrites old freeze

**SURVIVES.**

Q-RM-07 semantics are preserved: old freeze remains historical, affected status is invalidated as applicable, corrected inputs produce a new qualification/freeze.

## FO-A19 — new B/Q version compared as same state

**SURVIVES.**

Different qualification-relevant versions are not same-state comparable.

FO-F03 concerns the different problem of *same* ID/version with different bound content.

---

# 12. Physical repartitioning attack

Attack:

Implementation claims two different physical partitions are semantically equivalent even though current B V0.1 defines no such equivalence transform.

Candidate result:

**SURVIVES.**

O refuses to invent T06 equivalence.

---

# 13. Permission attack

Any inference:

```text
F/O candidate exists
→ download BI5
→ process real BI5
→ run real backtest
```

is forbidden.

**SURVIVES.**

---

# 14. Verdict

The first persisted F/O candidate is not promoted.

```text
F/O FIRST NATIVE-BI5 FREEZE / ORACLE CANDIDATE
FAIL
```

Demonstrated defects:

1. `FO-F01 — BINARY32_NUMERIC_NORMAL_FORM_UNDERSPECIFIED`
2. `FO-F02 — QUALIFICATION_RELEVANT_ANOMALY_EVIDENCE_NOT_FROZEN`
3. `FO-F03 — NORMATIVE_VERSION_COLLISION_DIGEST_CONFLICT_UNRESOLVED`

No D/R/M/B/A/Q mutation is authorized.

No runtime implementation is authorized.

No acquisition is authorized.

---

# 15. Authorized minimal correction

Correct only the F/O candidate:

1. uniquely normalize every finite binary32 logical numeric value;
2. freeze exact qualification-relevant evidence bindings for evidence-dependent anomaly decisions;
3. make determinant content-integrity agreement mandatory for same-state O comparability;
4. classify same ID/version with different determinant content as `BLOCKED / NORMATIVE_VERSION_INTEGRITY_CONFLICT`;
5. preserve the distinction between determinant-integrity digests and freeze-output byte digests.

Do not change:

- D/R/M/B/A/Q semantics;
- strict duplicate policy;
- source witness non-identity rule;
- no temporal authority;
- no partial universe rule;
- acquisition/backtest permissions.

After correction, persist the candidate and re-break the complete attack set from a freshly verified HEAD.


---

# 16. Persisted-head re-break after minimal correction

**Corrected candidate HEAD:** `d79f9008cb71f5b1fface9e87320c77bb8be253d`  
**Corrected candidate blob:** `fe62da06e63a51c336f9a447e7f1e0f3d89cad3b`

The branch was freshly verified identical to that HEAD before re-break.

The candidate blob was also re-read from GitHub and matched the expected corrected blob before the attack set was reapplied.

No candidate mutation occurred during this re-break.

## 16.1 Re-break FO-F01

Original defect:

`BINARY32_NUMERIC_NORMAL_FORM_UNDERSPECIFIED`

Corrected rule now requires:

```text
non-zero finite value
=
signed odd integer_coefficient * 2^exponent2

zero
=
0 * 2^0
```

Attack:

```text
1 * 2^0
vs
2 * 2^-1
```

Result:

The second representation is non-conforming because coefficient 2 is even and still contains a removable factor of two.

Attack:

negative/subnormal finite binary32 values.

Result:

Every non-zero dyadic rational still has one unique signed-odd-coefficient / integer-exponent representation.

Raw source bits remain separately admissible as provenance and do not replace the logical numeric normal form.

**RE-BREAK RESULT: SURVIVES.**

## 16.2 Re-break FO-F02

Original defect:

`QUALIFICATION_RELEVANT_ANOMALY_EVIDENCE_NOT_FROZEN`

Corrected F now requires immutable `qualification_evidence_bindings` whenever anomaly classification/localisability/outcome depends on evidence.

Attack:

A terminal remainder is labelled A08 / `REJECT RECORD` but no constructive completeness-proof binding is present.

Result:

The F artifact cannot validate the anomaly decision and therefore cannot reach `FROZEN`.

Attack:

A complete A08 proof is bound to the exact terminal-fragment target.

Result:

F may preserve the decision and proof binding.

Alternative valid proof bytes/locations do not become occurrence identity merely because their physical digests differ; O validates sufficiency before universe comparison.

**RE-BREAK RESULT: SURVIVES.**

## 16.3 Re-break FO-F03

Original defect:

`NORMATIVE_VERSION_COLLISION_DIGEST_CONFLICT_UNRESOLVED`

Corrected same-state gate requires the same immutable determinant-content binding.

Attack:

```text
same B id
same B version
digest X != digest Y
```

Result:

```text
oracle_result = BLOCKED
reason = NORMATIVE_VERSION_INTEGRITY_CONFLICT
```

No universe equality verdict is emitted.

Attack:

legitimate new B version.

Result:

```text
comparison_scope = DISTINCT_QUALIFICATION_STATE
qualified_universe_comparison = BLOCKED
```

Attack:

same determinant content but different freeze-output JSON whitespace/order causing a different freeze-output artifact digest.

Result:

This does not change semantic equality. Freeze-output byte digest remains physical artifact integrity only.

**RE-BREAK RESULT: SURVIVES.**

## 16.4 Full attack-set re-break

```text
late Q BLOCKED after valid prefix                     NO FREEZE / SURVIVES
Q ACQUISITION_REJECTED                               NO FREEZE / SURVIVES
F self-check incomplete                              NO FREEZE / SURVIVES
partial/prefix U presented as normative              FORBIDDEN / SURVIVES
blocked/rejected count represented as valid zero U   FORBIDDEN / SURVIVES

missing reconstruction determinant                   BLOCKED / SURVIVES
determinant version changed                          DISTINCT STATE / SURVIVES
same id+version, different determinant content       INTEGRITY CONFLICT BLOCKED / SURVIVES
freeze-output byte hash differs                      NON-SEMANTIC / SURVIVES
byte hash used as semantic oracle                    FORBIDDEN / SURVIVES

strict duplicate payloads                            MULTIPLICITY PRESERVED / SURVIVES
same payload, different multiplicity                 DIFFERENT / SURVIVES
content-hash deduplication                           FORBIDDEN / SURVIVES
occurrence array reorder                             EQUAL / SURVIVES
component array reorder                              EQUAL / SURVIVES
anomaly diagnostic reorder/path change               NON-SEMANTIC IF VALID / SURVIVES

source slot→payload swap with same payload bag       DIFFERENT RELATION / SURVIVES
source witness promoted to canonical identity        FORBIDDEN / SURVIVES
array index promoted to occurrence identity          FORBIDDEN / SURVIVES
physical slot order promoted to temporal authority   FORBIDDEN / SURVIVES
hidden timestamp sort                                FORBIDDEN / SURVIVES

binary32 equivalent non-unique expression            NON-CONFORMING / SURVIVES
finite binary32 negative/subnormal values            UNIQUE NORMAL FORM / SURVIVES
+0 vs -0 source representation                       SAME LOGICAL ZERO / SURVIVES
raw source bits substituted for logical value        FORBIDDEN / SURVIVES

A08 without completeness proof                       F BLOCKED / SURVIVES
evidence-dependent A decision without evidence bind  F BLOCKED / SURVIVES
alternative valid evidence provenance                NOT OCCURRENCE ID / SURVIVES

terminal fragment inserted as complete slot          BLOCKED / SURVIVES
candidate/reject overlap                             BLOCKED / SURVIVES
silent complete-slot omission                        BLOCKED / SURVIVES
unknown anomaly                                      BLOCKED UPSTREAM / SURVIVES

late upstream non-conformance rewrites old freeze    FORBIDDEN / SURVIVES
old freeze silently updated after contract change    FORBIDDEN / SURVIVES
physical repartition equivalence invented            FORBIDDEN / SURVIVES
different B/Q version compared as same state         BLOCKED / SURVIVES

acquisition permission inferred                      FORBIDDEN / SURVIVES
real BI5 processing inferred                         FORBIDDEN / SURVIVES
real backtest permission inferred                    FORBIDDEN / SURVIVES
```

No additional internal F/O candidate defect was demonstrated.

## 16.5 Final F/O candidate state

```text
F/O candidate formalization
= PERSISTED
= ADVERSARIALLY BROKEN
= FAIL ON FO-F01..FO-F03
= MINIMALLY CORRECTED
= PERSISTED-HEAD RE-BROKEN
= NO NEW INTERNAL DEFECT DEMONSTRATED
```

Official gates remain:

```text
F = BLOCKED
O = BLOCKED
```

because:

1. no materialized D acquisition/manifest/completeness evidence exists;
2. B/A provider-sensitive facts remain officially BLOCKED;
3. no executable Q implementation has been qualified;
4. no concrete qualified run exists from which a real F artifact can be emitted;
5. no executable F persistence implementation has been qualified;
6. no executable O semantic comparator has been qualified;
7. no independent I_A / I_B determinism run exists.

The corrected F/O contract is internally stable enough to become candidate input to the next concrete implementation-boundary block.

No acquisition or real backtest authorization is created.

## 16.6 Boundary for next work

Do not implement or acquire data merely because F/O survived formalization.

Before any next block:

1. persist this re-break;
2. update the global pre-backtest reconciliation audit;
3. create a durable session backup;
4. update the Recovery Checkpoint.

Only after those durable steps may the repository advance to the next governed concrete gate.
