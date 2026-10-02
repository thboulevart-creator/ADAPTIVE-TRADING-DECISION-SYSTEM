# MCEPR — ACTIVATION CONTRACT V0.2 — BOUNDED PILOT MACRO-AUTHORIZATION — DOCUMENTARY QUALIFICATION

**Date:** 2026-10-02  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Governed branch:** integration/system-v1  
**Qualification base HEAD:** 3ccf82bff7b6195bc1047f6316de4471bc0f8ffa  
**Qualification base TREE:** 1cceb66010cf44eedd171b8eeb4b5d664b86bc86

## 1. Qualified targeted amendment

Path: GOVERNANCE/MCEPR-ACTIVATION-CONTRACT-V0.2.json

Blob: 532da50bb1e72341d3b7126aa0d3f08568c01e78

Parent contract blob: cf235747fc5218a3f1b492159f82593a6ee51392

Status: DOCUMENTARY_AMENDMENT_QUALIFIED / FUTURE_PILOT_NOT_AUTHORIZED.

V0.2 is a targeted amendment, not a semantic rewrite. All V0.1 rules remain in force except the exact per-append approval clauses explicitly replaced by V0.2.

## 2. Purpose

V0.2 moves human authority from repeated candidate-by-candidate approvals to one future bounded macro authorization. Per-candidate human blob approval may be removed only inside that exact future envelope; deterministic construction, validation, force=false persistence, post-persistence verification, replay and evidence remain mandatory.

## 3. Material adversarial hardening

The documentary review identified the critical authority risk created by removing micro-approval: macro authorization could otherwise be misread as evidence that an event occurred. V0.2 therefore freezes MACRO_AUTHORIZATION_IS_NEVER_EVIDENCE_THAT_AN_EVENT_OCCURRED.

Every event still requires an occurrence/admission basis independent of the need to populate MCEPR. MCEPR administrative acts themselves are explicitly ineligible for pilot progression.

## 4. Preserved event-only pilot

Initial pilot remains one real event per segment, zero relations, minimum three consecutive successful appends, maximum five cycles. Genesis remains one real event strictly after the effective cutover and zero relations.

## 5. Cutover remains exact

Forward cutover blob: 2e2528e908ffefaa4451fe9b41ca639943d2415d.

Effective cutover: 2026-10-02T17:19:21Z.

Only occurred_at_utc strictly greater than that instant can enter this forward pilot. Historical/backfill material remains outside scope.

## 6. Macro execution boundary

A future separately authorized pilot may mechanically perform admission, candidate construction, validation, force=false persistence, exact post-persistence verification, full replay, cycle-evidence persistence and progression to the next eligible cycle without per-candidate human approval.

No background monitoring or waiting for future events is authorized. If insufficient real eligible events are available, the executor must not manufacture or wait for them.

## 7. Concurrency

Unrelated Git drift can be absorbed only after fresh proof that the entire MCEPR semantic state and decisive references remain exact. Any MCEPR-head change makes the current candidate stale and requires full-chain revalidation plus deterministic rebuild. A valid external append does not count as a cycle of this pilot unless it was executed under the same active macro authorization. Forks remain BLOCKED.

## 8. Adversarial review

Twenty-four targeted cases are frozen in the amendment. They cover self-manufactured events, administrative events, cutover bypass, ambiguous relevance, guessed references, unrelated Git drift, external MCEPR drift, false cycle counting, forks, prior-segment mutation, identity drift, relation/backfill escape, false completeness, insufficient real events, background monitoring, automatic N_budget/N_famille, automatic promotion/trading authority, skipped replay, and drift rebuild without decisive-reference revalidation.

Result: PASS_WITH_TARGETED_HARDENING.

## 9. Authority verdict

HUMAN_AUTHORITY = PRESERVED

HUMAN_INTERMEDIATION = REDUCED_FOR_MECHANICAL_STEPS

EVENT_SEMANTIC_SELF_AUTHORITY = NONE

SCIENTIFIC_AUTO_ADJUDICATION = NONE

RUNTIME_COUPLING = NONE

TRADING_AUTHORITY = NONE

## 10. No population performed

GENESIS = NOT_CREATED

REAL_EVENT = NOT_PERSISTED

REAL_RELATION = NOT_PERSISTED

SEGMENTS = 0

BACKFILL = NONE

AUTOMATED_PRODUCER = NONE

AUTOMATED_CONSUMER = NONE

## 11. Documentary verdict

MCEPR_ACTIVATION_CONTRACT_V0_2 = QUALIFIED

AMENDMENT_MODE = TARGETED

BOUNDED_PILOT_MACRO_AUTHORIZATION = DEFINED_NOT_AUTHORIZED

FAIL_CLOSED_GUARANTEES = UNCHANGED_OR_STRONGER

REAL_REGISTRY_POPULATION = NOT_AUTHORIZED

## 12. Next candidate frontier

MCEPR FORWARD PILOT MACRO-AUTHORIZATION V0.1.

It requires one separate explicit human authorization bound to the exact persisted V0.2 amendment blob. After that authorization, eligible event-only pilot cycles may execute without micro-approval until qualification or automatic STOP/BLOCKED.

## 13. STOP

DOCUMENTARY_AMENDMENT_QUALIFICATION = CLOSED

PILOT_EXECUTION = NOT_AUTHORIZED

GENESIS = NOT_AUTHORIZED

REAL_EVENT_PERSISTENCE = NOT_AUTHORIZED

STOP = TRUE
