# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.5 INTER-PROCESS RE-ATTESTATION PASS / DOCUMENTARY REBREAK PENDING

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, tests, workflow evidence and this checkpoint are authoritative. Do not reconstruct project state from conversation memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Integration lineage

Integration base:

`main@43ec28f3e09856fe508874af3aaf32079761d2d5`

P0.2 qualified decision source:

`feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

P0.3 qualified multi-year source:

`feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

P0.4 final closed base:

`aa9551addc0fe554af9cbb8ebdb26314d37e412e`

No blind merge, rebase, reset, force-push or branch-history replay is authorized by this checkpoint.

## P0.2 / P0.3 / P0.4 remain CLOSED

P0.5 combined qualification re-casses the protected predecessors:

- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- P0.4 producer junction C0–C15: `16 passed`.

No P0.5 operation widens acquisition, backtest or live permissions.

## P0.5 — RESEARCH inter-process replay re-attestation

Contract:

`04-REFERENCE/RESEARCH-INTERPROCESS-REATTESTATION-CONTRACT.md`

Contract ID:

`RESEARCH_INTERPROCESS_REATTESTATION_V1`

Implementation:

`src/research_interprocess.py`

Qualification report:

`reports/data-qualification/p0_5_research_interprocess_reattestation_qualification.md`

JIT audit marker:

`P0_5_RESEARCH_INTERPROCESS_REATTESTATION_JIT_AUDIT_V1`

Session backup:

`99-BACKUP/SESSION-2026-09-16-P0.5-RESEARCH-INTERPROCESS-REATTESTATION-PASS.md`

### Selected trust model

P0.5 does not promote a JSON checksum into a bearer credential. The durable proof is non-authorizing until a fresh consumer process independently replays the qualified research execution.

Admissible path:

`qualified RESEARCH execution → content-addressed persisted proof → fresh process → source-byte validation → deterministic replay → exact claim comparison → fresh P0.4 process-local ResearchRunEvidence attestation → ResearchFindings / DECISION`

The consumer receives the expected code version separately from the proof and supplies local corpus/contract paths independently. A byte-identical source may move filesystem location without changing its governed identity.

## Initial Tier-A FAIL

Pre-correction HEAD:

`36f97ee715655f6b2470e7836f7c82e6285aa237`

Run/job:

`35143592655 / 104953910890` — **FAIL expected**.

Evidence:

- P0.4 C0–C15: `16 passed`;
- P0.5 provisional breaker: `1 failed / 1 passed`;
- failure was exactly the absent durable writer/re-attestation bridge;
- raw serialized evidence was already non-authorizing in a fresh process;
- no acquisition/backtest side effect;
- worktree clean.

## Corrected D0–D14 attack matrix

HEAD:

`7f864b2da4e5590df26ca5a152e84cd67a362d98`

Run/job:

`35144130840 / 104955745568` — **SUCCESS**.

- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- read-only/no-acquisition checks: PASS;
- worktree clean.

Attacks cover fresh-process positive replay, raw serialized non-authority, claim tampering plus recomputed digest, trusted code-version mismatch, corpus/contract substitution, content-address rename, strict schema/duplicate keys, report-only evidence, copied/reconstructed/mutated evidence and filesystem relocation of byte-identical sources.

## Combined technical persisted-HEAD qualification

HEAD:

`05b9752fff9f25ad2301c6385feba14848b4bb27`

Run/job:

`35144258717 / 104956179724` — **SUCCESS**.

Exact results:

- complete repository: `207 passed`;
- P0.5 D0–D14: `15 passed`;
- P0.4 C0–C15: `16 passed`;
- P0.2 decision Tier-A: `83 passed`;
- P0.3 calendar/freeze Tier-A: `80 passed`;
- proof is non-authorizing without replay: PASS;
- raw evidence minter absent: PASS;
- permissions read-only;
- worktree clean.

## Current multi-year safety truth

Still re-derived unchanged:

- global candidates/resolved/unresolved: `111 / 91 / 20`;
- global coverage: **BLOCKED**;
- selected window: `2021-08-14 → 2026-08-14`;
- selected-window candidates/resolved/unresolved: `68 / 68 / 0`;
- persisted freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- persisted `massive_acquisition_authorized = false`;
- persisted `real_backtest_authorized = false`.

## Covered by P0.5

P0.5 closes only:

- durable content-addressed persistence of qualified research execution proof;
- consumer-side deterministic replay across a process boundary;
- exact source/execution/Dataset/Context/evidence revalidation;
- separately trusted expected code version;
- fresh local P0.4 attestation before downstream authorization;
- tested tamper/reconstruction/substitution/schema/content-address attacks;
- preservation of P0.2/P0.3/P0.4 qualified boundaries.

## Explicitly NOT covered by P0.5

Still open / not authorized:

- non-replay cryptographic bearer attestation;
- signing-key trust root/lifecycle;
- repository-wide dependency/environment lock and reproducibility envelope;
- remaining integration workflow branch coupling where still present;
- native `.bi5` acquisition/readiness/authorization;
- acquisition manifests and tick completeness/reconciliation;
- exact OOS split;
- real-data backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE`;
- complete transverse decision reconstruction;
- general resilience/restoration;
- promotion gate or live activation.

Historical global governance verdicts therefore remain unchanged outside this bounded scope:

- Decision Traceability: **FAIL globally** until the downstream chain is proven;
- Resilience / Continuity: **FAIL**;
- Governance Effectiveness: **BLOCKED globally**, despite bounded JIT PASSes.

## Documentary closure status

The P0.5 code boundary is technically qualified PASS.

This checkpoint is part of the documentary closure candidate. P0.5 becomes durably CLOSED only after a final read-only persisted-HEAD P0.5 re-break succeeds on the exact HEAD containing:

- this checkpoint;
- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md` with `P0_5_RESEARCH_INTERPROCESS_REATTESTATION_JIT_AUDIT_V1`;
- `reports/data-qualification/p0_5_research_interprocess_reattestation_qualification.md`;
- `99-BACKUP/SESSION-2026-09-16-P0.5-RESEARCH-INTERPROCESS-REATTESTATION-PASS.md`;
- the final P0.5 persisted-HEAD workflow.

No substantive write may follow that successful final re-break without reopening qualification.

## Mandatory recovery order before next substantive block

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-P0.5-RESEARCH-INTERPROCESS-REATTESTATION-PASS.md`
4. `reports/data-qualification/p0_5_research_interprocess_reattestation_qualification.md`
5. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
6. `04-REFERENCE/RESEARCH-INTERPROCESS-REATTESTATION-CONTRACT.md`
7. `.github/workflows/p0-5-research-interprocess-reattestation.yml`
8. `src/research_interprocess.py`
9. `tests/test_research_interprocess_reattestation_tier_a.py`
10. P0.4 contract/workflow/runtime/evidence source and C0–C15 tests
11. P0.2 and P0.3 regression guards
12. verify branch HEAD and latest successful final P0.5 persisted-HEAD re-break before mutation.

## Exactly one next governed action after final P0.5 documentary re-break

**P0.6 — close the repository reproducibility envelope before adding new capability: inventory the actual Python/runtime dependencies and workflow assumptions, select the smallest authoritative dependency/environment lock, make qualification workflows reproducible/transportable where required, adversarially break version drift/missing dependency/environment mismatch, and re-break P0.2–P0.5 without authorizing acquisition or backtest.**

The promotion gate remains the following P1 gate; P0.6 must not silently implement or authorize capability promotion.
