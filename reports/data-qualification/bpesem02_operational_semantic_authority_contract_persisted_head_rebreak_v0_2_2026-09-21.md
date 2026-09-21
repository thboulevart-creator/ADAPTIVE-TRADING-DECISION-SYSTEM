# B-PE-SEM-02 — PERSISTED-HEAD RE-BREAK OF V0.2 CORRECTED COMPOSITE

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Persisted corrected HEAD attacked:** d6e35d6f5fb56c4a082e79d98f23c2afe356cc40

Persisted inputs re-read:

~~~text
candidate blob =
092aae41821afb69d7fb84da095d1c8c0bfacb3d

adversarial break =
reports/data-qualification/
bpesem02_operational_semantic_authority_contract_adversarial_break_2026-09-21.md

correction V0.2 blob =
09f13707a51b4957cf28e4ae48b2e52e90e96343
~~~

No conversational reconstruction is authority for this re-break.

## 1. Re-break of initial F01-F07

The V0.2 correction materially closes the direct exploits demonstrated in F01-F07:

~~~text
F01 dimension omission
  -> direct omission route closed by ClaimDimensionRegister

F02 evidence self-admissibility
  -> direct route closed by separate admissibility decision and authority basis

F03 current-daily -> historical-K1 direct scope leak
  -> direct route closed by per-dimension scope applicability decision

F04 retrospective B-ERD-02 decisive reuse
  -> direct route closed by HistoricalObservationEligibilityRecord

F05 omission inside an actually reviewed evidence set
  -> direct route closed by KnownMaterialAlternativeRegistry

F06 ambiguity for most named set digests
  -> materially improved by explicit projections

F07 dropped dimension obligation
  -> direct route closed by canonical obligation union/digest
~~~

However the extended attack demonstrates four residual/new defects.

## 2. Demonstrated residual/new defects

### BPESEM02-R01 — DIMENSION AUTHORITY BASIS IS NOT ITSELF CONTRACT-LOCKED

V0.2 requires a DimensionAuthorityBasis per dimension, but the adjudication can still materialize those basis records later.

The ClaimDimensionRegister does not bind an exact authority-basis-register digest.

The field future_execution_obligation_allowed is also not assigned exact values per dimension.

Exploit:

~~~text
future adjudication
-> create a weaker DimensionAuthorityBasis for a semantic dimension
or
-> permit a future conditional obligation where the missing item is semantic meaning
-> mark dimension PASS now
-> defer the missing meaning into execution
~~~

This reopens the exact failure mode the parent candidate intended to forbid.

Required correction:

~~~text
DimensionAuthorityBasisRegister
-> one exact basis per registered dimension
-> exact primary authority class
-> exact prerequisite IDs
-> exact allowed conditional-semantic rule IDs
-> exact obligation-mode policy
-> register digest bound by adjudication
~~~

Under this contract version:

~~~text
conditional semantic obligation
is permitted only for
C03-D3-OP and C05-D2-OP
through SIGNEDNESS_EQUIVALENCE_RULE_V0_1
~~~

Other runtime checks may test conformance to already-authorized meaning but may not supply missing meaning.

### BPESEM02-R02 — MACHINE-CLOSED SCOPE STILL DOES NOT IDENTIFY THE EXACT WARMUP DOMAIN

V0.2 binds the execution-window freeze blob and warmup_h1_bars = 20.

But the actual warmup H1 members depend on the qualified USATECH session calendar.

The scope signature does not bind:

~~~text
DUKASCOPY_USATECH_SESSION_CALENDAR_V3
tools/dukascopy_usatech_calendar.py
blob fab634aab7b8c299b0139c3c43bf5b89a2aa03d0
~~~

nor the already sealed full-domain IntervalInventory identity.

Current B-FIQ-02 proves:

~~~text
full_domain_first_h1 = 2021-08-13T01:00:00Z
full_domain_last_h1  = 2026-08-14T20:00:00Z
IntervalInventory root =
26d86a34a00e6697208a6481867f6338f21c1deae26e5be74b52cc8ba83eced8
IntervalInventory blob =
8c02972228941d8b6f1aacaf9ac6bf75fb0f2029
~~~

Exploit:

~~~text
same freeze file + same warmup count
but different calendar resolution
-> different warmup prefix
-> same semantic scope identity
~~~

Required correction:

Bind the exact session-calendar identity plus exact full-domain first/last H1 and current structural IntervalInventory root/blob.

This does not import the blocked B-FIQ semantic manifest; it only fixes the already-qualified structural domain identity.

### BPESEM02-R03 — KNOWN-ALTERNATIVE REVIEW UNIVERSE CAN BE SHRUNK

KnownMaterialAlternativeRegistry requires reviewed_evidence_ids[].

But an adjudicator may omit inconvenient already-known evidence from reviewed_evidence_ids and then truthfully claim that all alternatives in the chosen reviewed set were included.

Exploit:

~~~text
known contradictory/alternative evidence exists in prior governed artifacts
-> do not include it in reviewed_evidence_ids
-> registry contains one material candidate
-> one hypothesis survives
~~~

Required correction:

Create a sealed SemanticEvidenceReviewUniverse that must include at minimum:

~~~text
all evidence records contributing to the current adjudication
all evidence records referenced by prerequisite/reopen/contradiction state
all inherited BPE02 evidence/assertions relevant to C01-C07
all relevant B-PE-SEM-01 identified conflicts/limitations
B-ERD-02 evidence whenever reused
~~~

KnownMaterialAlternativeRegistry must bind the review-universe ID/digest.

Any known relevant governed evidence excluded without an explicit qualified irrelevance/inadmissibility decision => BLOCKED.

### BPESEM02-R04 — TWO INTEGRITY DIGEST DOMAINS REMAIN IMPLICIT

V0.2 names but does not give exact formulas for:

~~~text
scope_signature_digest
lineage_resolution_digest
~~~

They are then transitively relied upon by the adjudication seal and current-authority predicate.

Required correction:

~~~text
scope_signature_digest =
SHA256(canonical_json(scope_signature_payload_without_scope_signature_digest))

lineage_resolution_digest =
SHA256(canonical_json(lineage_resolution_payload_without_lineage_resolution_digest))
~~~

and the lineage-resolution set must bind exact evidence/semantic-source IDs covered by each record.

## 3. Extended attacks still held

No defect was demonstrated for:

~~~text
C08 -> C01-C07 leakage
I_A/I_B/F/O self-authority
CFD 0.01 -> /1000 inference
spread sign -> ask/bid meaning
offset range -> timestamp meaning
volume removal
signedness high-bit-one silent acceptance
B-FIQ-02 in-place reinterpretation
historical PASS reuse while an OPEN reopen event exists
~~~

## 4. V0.2 re-break verdict

~~~text
B-PE-SEM-02 V0.2 CORRECTED COMPOSITE = FAIL

residual/new material defects = 4
R01-R04
~~~

No semantic proposition is promoted.

Required next movement:

~~~text
minimal correction V0.3 for R01-R04 only
-> persist
-> persisted-head final re-break
-> PASS / FAIL / BLOCKED
~~~

STOP.
