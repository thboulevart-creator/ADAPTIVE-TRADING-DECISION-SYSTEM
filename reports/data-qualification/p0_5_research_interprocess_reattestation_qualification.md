# P0.5 — RESEARCH INTER-PROCESS RE-ATTESTATION QUALIFICATION

**Date:** 16 September 2026  
**Branch:** `integration/system-v1`  
**Base P0.4:** `aa9551addc0fe554af9cbb8ebdb26314d37e412e`  
**Contract:** `RESEARCH_INTERPROCESS_REATTESTATION_V1`  
**Tier:** A

## Verdict candidate

**PASS — `DURABLE_REPLAY_REATTESTATION_SURVIVES_INTERPROCESS_TIER_A_REBREAK`**, subject to the final documentary persisted-HEAD re-break containing this report, the JIT audit, checkpoint, backup and final P0.5 verifier.

## Problem closed

P0.4 intentionally kept `ResearchRunEvidence` attestation process-local. A serialized/reconstructed evidence object loses authority when moved to another process.

P0.5 adds the minimum durable bridge without inventing an ungoverned signing/key system:

`qualified RESEARCH execution → content-addressed persisted proof → fresh process → source-byte validation → deterministic replay → exact claim comparison → fresh P0.4 process-local attestation → ResearchFindings / DECISION`

The persisted JSON proof is explicitly **non-authorizing by itself**. Its checksum does not prove who wrote it. Authorization is re-established only after deterministic replay from independently supplied source paths and a separately trusted expected code version.

## Minimal implementation

New authorization-adjacent module:

`src/research_interprocess.py`

It provides:

- `persist_research_execution_proof(...)`;
- `reattest_persisted_research_execution(...)`;
- canonical sorted compact JSON plus newline;
- content-addressed filename `research-proof-<sha256>.json`;
- exact schema and duplicate-key rejection;
- immutable/idempotent proof write semantics;
- no producer filesystem path used as persisted identity;
- consumer-side source validation and deterministic replay;
- exact execution/Dataset/Context/ResearchRunEvidence claim comparison;
- fresh local P0.4 attestation only after replay.

No change was made to the raw P0.4 attestation minter. `_attest_factory_evidence` remains absent from module scope.

## Initial adversarial FAIL

Pre-correction HEAD:

`36f97ee715655f6b2470e7836f7c82e6285aa237`

Run/job:

`35143592655 / 104953910890` — **FAIL expected**.

Evidence:

- P0.4 C0–C15: `16 passed`;
- P0.5 provisional breaker: `1 failed / 1 passed`;
- exact failure: durable proof writer/re-attestation bridge did not yet exist;
- raw serialized `ResearchRunEvidence` already remained non-authorizing in a fresh process;
- read-only/no-acquisition checks: PASS;
- worktree: clean.

## Corrected D0–D14 re-break

Corrected attack-matrix HEAD:

`7f864b2da4e5590df26ca5a152e84cd67a362d98`

Run/job:

`35144130840 / 104955745568` — **SUCCESS**.

- P0.4 C0–C15: `16 passed`;
- P0.5 D0–D14: `15 passed`;
- read-only/no-acquisition checks: PASS;
- worktree: clean.

The attacks cover:

- fresh-process positive replay to DECISION;
- raw serialized evidence remaining unattested;
- evidence/execution/Dataset/Context tamper plus recomputed proof digest;
- foreign valid-shaped code version;
- corpus and contract source-byte substitution;
- proof rename/content-address mismatch;
- unknown/missing/duplicate/schema-substituted JSON;
- legacy V4.3 report-only evidence;
- copied/deep-copied/reconstructed/mutated evidence;
- byte-identical source relocation;
- distinction between non-authorizing serialized fields and the newly re-attested consumer object.

## Combined technical persisted-HEAD re-break

Technical qualification HEAD:

`05b9752fff9f25ad2301c6385feba14848b4bb27`

Run/job:

`35144258717 / 104956179724` — **SUCCESS**.

Exact results:

- complete repository: `207 passed`;
- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- global truth: `111 / 91 / 20` and global coverage still **BLOCKED**;
- selected window: `68 / 68 / 0`, freeze **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- persisted `massive_acquisition_authorized = false`;
- persisted `real_backtest_authorized = false`;
- replay-only/non-authorizing-proof model: PASS;
- raw evidence minter absent: PASS;
- workflow permissions: `contents: read`, `metadata: read`;
- worktree: clean.

## Covered by P0.5

P0.5 closes only:

- durable content-addressed persistence of a qualified research execution proof;
- deterministic replay re-attestation in a fresh consumer process;
- separately trusted expected code version;
- local source-path independence when source bytes/identities are unchanged;
- fail-closed rejection of tested proof/source/identity tampering;
- fresh P0.4 authority reconstruction before ResearchFindings/DECISION;
- preservation of P0.2/P0.3/P0.4 invariants.

## Explicitly not covered by P0.5

Still open / not authorized:

- non-replay cryptographic bearer attestation;
- signing-key generation, custody, rotation or revocation;
- repository-wide dependency/environment lock;
- remaining branch-coupled integration workflows beyond this bounded gate;
- native `.bi5` acquisition protocol/readiness/authorization;
- acquisition manifests, tick completeness/exhaustiveness/reconciliation;
- exact OOS split;
- real-data backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE` complete chain;
- complete transverse decision reconstruction;
- resilience/restoration beyond this replay proof path;
- promotion gate or live activation.

## Safety state preserved

P0.5 does not authorize data acquisition or execution. The multi-year state remains:

- global `111/91/20`: BLOCKED;
- selected `68/68/0`: PASS;
- persisted freeze: PASS;
- acquisition after freeze: BLOCKED;
- massive acquisition: false;
- real backtest: false.

## Closure rule

This report is a documentary closure candidate. P0.5 is durably CLOSED only when a final read-only P0.5 persisted-HEAD workflow succeeds on the exact HEAD containing:

- this report;
- `P0_5_RESEARCH_INTERPROCESS_REATTESTATION_JIT_AUDIT_V1` in the audit register;
- the P0.5 recovery checkpoint;
- the P0.5 session backup;
- the final P0.5 verifier.

No run identifier will be written after that final re-break, because doing so would move the persisted HEAD being qualified.
