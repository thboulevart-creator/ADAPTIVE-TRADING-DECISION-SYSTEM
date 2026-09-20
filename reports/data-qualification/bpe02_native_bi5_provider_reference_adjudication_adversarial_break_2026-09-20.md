# B-PE-02 — PROVIDER / REFERENCE ADJUDICATION — ADVERSARIAL BREAK

**Date:** 2026-09-20
**Candidate HEAD:** `428ac771e238ea1988c8fe2d8cad2d7e7b83adf9`
**Evidence bundle blob:** `8445b235ab5d203fcf4352245dc79f3745905d71`
**Scope:** adjudication integrity only; no BI5/project data.

## Demonstrated defects

### BPE02-F01 — NONRECURSIVE_CANONICAL_SEAL_GENERATION

Recomputation using the B-PE-01 recursive canonical JSON rules produced:

```text
admissibility decisions mismatching = 6 / 6
lineage digest mismatching          = yes
adjudication seal mismatching       = yes
```

Example:

```text
persisted decision seal
299c3e1b59c704dc2479a984d113d0645b09f58e56b2d2cb1707bd39204c3bc7

B-PE-01 canonical recomputation
e42d571e1a270a525b205ed4f812850796c0494e80dbaab352a4a4b712984e5b
```

Adjudication:

```text
persisted
4c387c4a0b2bdf0525fa67ae2fc9e908124d59615f874d593aa3a2515c410c7d

canonical recomputation
815890de46b8803cf48d134a859c2669fa2d2c731c07647a0ef1943a3ecffbe6
```

Verdict: demonstrated defect.

Correction required: recompute every structured seal/digest using recursive sorted-key canonical JSON exactly as B-PE-01 specifies.

### BPE02-F02 — LIVE_PROVIDER_PAGE_SNAPSHOT_NOT_DURABLY MATERIALIZED

E01/E02 are provider-primary live pages. The candidate stores URL/line anchors and digests of captured extracts, but not the exact captured source bytes/snapshot itself.

Therefore a future persisted-HEAD auditor cannot independently reconstruct those source digests if the live page changes.

Under B-PE-01:

```text
source digest alone
≠ persisted immutable evidence snapshot
```

Verdict: demonstrated defect.

Correction required in the current no-copy/no-provider-archive situation:

```text
E01 = BLOCKED source admissibility
E02 = BLOCKED source admissibility
```

until an immutable provider snapshot/version can be pinned and persisted/retrieved.

Their observations may remain contextual diagnostics but contribute zero PASS/FAIL evidentiary weight.

Consequences:

- previous C08-D1/D2 PASS cannot stand because they depended on E01;
- all C01-C08 mandatory claims remain BLOCKED;
- no FAIL is created;
- overall provider evidence remains BLOCKED.

## Attacks that did not demonstrate an adjudication defect

- current-daily provider docs were not silently transplanted to legacy hourly;
- "raw LZMA" was not treated as proof of LZMA-Alone;
- current CFD point value was not treated as raw /1000 proof;
- signedness disagreement was preserved instead of majority-voted;
- third-party pairwise lineage remained UNRESOLVED;
- project V4.3 was explicitly rejected;
- generic facts did not bypass C08 temporal/version scope.

## Verdict

```text
B-PE-02 INITIAL ADJUDICATION CANDIDATE = FAIL
```

Only BPE02-F01 and BPE02-F02 are authorized for correction.


---

## Residual adversarial findings before correction

### BPE02-F03 — CLAIM_ASSERTION_SCHEMA_NOT_CLOSED

The candidate bundle stores claim anchors as multi-dimension objects:

```text
{id, evidence_id, anchor, proposition, dims:[...]}
```

B-PE-01 requires one closed assertion containing:

```text
assertion_id
evidence_id
claim_id
dimension_id
stance
anchor_type
anchor_locator
anchor_integrity_digest
normalized_proposition
scope_mapping
scope_mapping_rationale
adjudicator_identity
assertion_created_at_utc
```

A multi-dimension shortcut can silently assign one proposition to dimensions it does not actually entail and makes the required assertion-set digest projection impossible to reproduce.

Verdict: demonstrated defect.

Correction: one exact assertion per source × dimension × stance, using the closed B-PE-01 schema.

### BPE02-F04 — MULTI_FILE_SOURCE_DIGEST_PROJECTION_NOT SELF-DESCRIBING

E03/E04/E05 use one `content_integrity_digest` representing a hand-built bundle of several GitHub files.

The EvidenceSourceRecord does not persist the exact bundle-member projection/algorithm, so a future auditor cannot reconstruct that digest from the record alone.

Verdict: demonstrated defect.

Correction: persist each GitHub file used as evidence as its own EvidenceSourceRecord with its own exact SHA-256 bytes digest and exact commit/path locator; group them only through lineage resolution, never through an undocumented bundle digest.

## Updated authorized correction scope

Correct only:

```text
BPE02-F01 — canonical seal generation
BPE02-F02 — live provider snapshot immutability/admissibility
BPE02-F03 — assertion schema closure
BPE02-F04 — self-describing source digest projection
```
