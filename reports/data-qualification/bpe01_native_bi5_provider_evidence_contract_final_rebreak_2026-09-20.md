# B-PE-01 — NATIVE BI5 PROVIDER EVIDENCE CONTRACT — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Persisted corrected candidate HEAD:** `2dc7c9fff14efc9597797775cf8ed92878ed6456`  
**Final candidate blob:** `278a691b17cdd4b37e9c0e739f0fe9b56f014b29`  
**Scope:** documentary contract re-break only. No provider evidence gathered. No BI5 downloaded or processed.

## 1. Defect closure

Initial adversarial defects closed:

```text
BPE-F01 — SINGLE_PROVIDER_ESCAPE_UNDERCUTS_INDEPENDENCE_REQUIREMENT
BPE-F02 — CLAIM_SUPPORT_CAN_BE_SELF_ASSERTED_WITHOUT_EXACT_SOURCE_ANCHOR
BPE-F03 — LINEAGE_INDEPENDENCE_IS_SELF_ASSERTED
BPE-F04 — TARGET_PROVIDER_SCOPE_VERSION_BINDING_NOT_CONCRETE_ENOUGH
BPE-F05 — C07_MIXES_PROVIDER_FACT_WITH_PROJECT_DECODER_BEHAVIOR
BPE-F06 — BROAD_CLAIM_CAN_PASS_WITH_UNPROVEN_REQUIRED_DIMENSION
BPE-F07 — NO_CLOSED_PERSISTED_ADJUDICATION_OUTPUT_EVIDENCE_SET_BINDING
BPE-F08 — POST_PASS_CONFLICT_SUPERSESSION_SEMANTICS_INCOMPLETE
```

Residual persisted-head defects closed:

```text
BPE-R01 — INTEGRITY_DIGEST_AND_SEAL_CANONICALIZATION_DEFERRED
BPE-R02 — SOURCE_ADMISSIBILITY_IS_NOT_A_PERSISTED_DECISION
BPE-R03 — REOPEN_REQUIRED_EVENT_HAS_NO_CLOSED_SCHEMA_CURRENT_AUTHORITY_RULE
```

## 2. Final adversarial matrix

### A01 — one provider source only

Expected:

`BLOCKED — INSUFFICIENT_INDEPENDENT_CORROBORATION`

Observed contract behavior:

PASS cannot be emitted.

### A02 — provider source + V4.3/I_A/I_B corroboration

Expected:

project source has zero independent evidentiary weight.

Observed:

PASS cannot be emitted because EC-PROJECT is inadmissible as independent support.

### A03 — two independent-looking mirrors from one upstream parser

Expected:

one lineage.

Observed:

lineage resolution collapses them to COMMON_LINEAGE or leaves them UNRESOLVED; neither satisfies the second-lineage requirement.

### A04 — unproven lineage independence

Expected:

BLOCKED.

Observed:

UNRESOLVED pair cannot be counted as independent.

### A05 — large provider document/repository with no exact claim anchor

Expected:

no dimension support.

Observed:

source digest alone cannot satisfy a dimension; ClaimEvidenceAssertion requires exact anchor + normalized proposition.

### A06 — C02 sources prove only 20-byte width

Expected:

C02 remains BLOCKED because byte-zero origin/residual/header dimensions remain unresolved.

Observed:

claim PASS is impossible unless every mandatory dimension PASS.

### A07 — generic Dukascopy/FX price rule used for USATECHIDXUSD C06

Expected:

BLOCKED on scope.

Observed:

target signature + C06/C08 dimension requirements prevent silent symbol-family transplantation.

### A08 — external source proves binary32 volume but project decoder behavior is used to prove "no scaling"

Expected:

project behavior cannot complete provider claim.

Observed:

C07 is now representation-level only; project decoder conformance is downstream.

### A09 — REJECTED/BLOCKED source inserted in an evidence set

Expected:

zero positive weight.

Observed:

EvidenceAdmissibilityDecision is mandatory and only ADMISSIBLE sources may contribute to dimension PASS/FAIL.

### A10 — logical adjudication serialized with different JSON key order/whitespace

Expected:

same logical canonical projection / same seal.

Observed:

canonical JSON rule fixes UTF-8, sorted keys, compact separators, exact JSON types and set projections.

### A11 — duplicate JSON keys / nonfinite JSON values

Expected:

invalid serialized ingress.

Observed:

duplicate keys and nonfinite values are explicitly rejected from canonical structured integrity objects.

### A12 — current PASS receives new admissible exact-scope contradictory evidence

Expected:

current authority becomes BLOCKED before new promotion.

Observed:

OPEN ProviderEvidenceReopenEvent makes historical PASS non-authoritative for new promotion.

### A13 — downstream B pins historical PASS after supersession/open event

Expected:

rejected as current authority.

Observed:

current-authority predicate requires valid PASS, no superseding adjudication and no OPEN reopen event.

### A14 — evidence-set membership changes after PASS

Expected:

new adjudication identity/seal required.

Observed:

evidence_set_digest binds exact evidence IDs, content digests and admissibility decision IDs/seals.

### A15 — provider docs prove framing but not temporal/version continuity

Expected:

BLOCKED.

Observed:

C08-D5 and target temporal applicability prevent silent epoch inheritance.

### A16 — representation-wide evidence presented as proof of real acquisition completeness

Expected:

rejected.

Observed:

Section 14 explicitly defers component existence/count/hash/completeness/anomaly incidence and real Q/F/I_A/I_B results to later bounded acquisition evidence.

## 3. Final re-break result

No additional defect was demonstrated.

The contract now fixes:

- exact C01-C08 claim register;
- mandatory per-claim dimensions;
- closed target representation scope;
- source/evidence classes;
- source-level ADMISSIBLE/REJECTED/BLOCKED;
- exact claim anchors;
- lineage proof and independence;
- mandatory provider-primary + distinct corroborating lineage;
- strict claim PASS/FAIL/BLOCKED;
- conflict and staleness semantics;
- SHA-256 and canonical JSON integrity rules;
- exact evidence/adjudication binding;
- sealed reopen/supersession semantics;
- current-authority predicate;
- hard boundary between representation-wide evidence and real-acquisition evidence.

## 4. Verdict

```text
B-PE-01 NATIVE BI5 PROVIDER-SENSITIVE PHYSICAL SEMANTICS
EVIDENCE CONTRACT = PASS
```

This PASS applies only to the evidence-adjudication contract.

It does **not** adjudicate provider truth:

```text
BPE-C01 = NOT ADJUDICATED
BPE-C02 = NOT ADJUDICATED
BPE-C03 = NOT ADJUDICATED
BPE-C04 = NOT ADJUDICATED
BPE-C05 = NOT ADJUDICATED
BPE-C06 = NOT ADJUDICATED
BPE-C07 = NOT ADJUDICATED
BPE-C08 = NOT ADJUDICATED
```

Therefore:

```text
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
```

No provider evidence was gathered and no real data was touched.
