# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.2 DECISION BLOCK INTEGRATION PASS / MULTI-YEAR IMPORT NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, tests, workflow evidence and this checkpoint are authoritative. Do not reconstruct project state from conversation memory.

Construction rule remains:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts remain `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Integration branch identity

`integration/system-v1` was created exactly from:

`main@43ec28f3e09856fe508874af3aaf32079761d2d5`

No merge, rebase, reset, force-push or blind history replay was used.

Qualified decision source:

`feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

Current-governance source used during controlled import:

`feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

P0.2 technical integration candidate:

`fa43c44739e75c8d927626a2b3df8eefb185e00f`

## P0.2 — controlled decision-block integration CLOSED

Verdict:

**PASS — `QUALIFIED_DECISION_BLOCK_CONTROLLED_IMPORT_SURVIVES_INTEGRATION_REBREAK`**

Durable qualification report:

`reports/data-qualification/p0_2_decision_block_integration_qualification.md`

JIT governance audit:

`GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`

Integration-specific persisted-HEAD verifier:

`.github/workflows/p0-2-decision-block-integration-rebreak.yml`

### Controlled source-identical import

The integrated decision block contains exactly the bounded qualified surface required for:

`DATA → CONTEXT → RESEARCH FINDINGS / EVIDENCE → DECISION`

The imported block includes:

- four durable branch-neutral boundary workflows;
- six STEP/manifest governance documents from the qualified decision workstream;
- `docs/RESEARCH-FINDINGS-CONTRACT.md`;
- six executable source modules;
- seven executable/adversarial test files.

These 24 source files are verified byte-identical to the qualified decision source HEAD.

The historical source-only verifier `.github/workflows/research-to-decision-persisted-head.yml` was intentionally not imported because its ancestry/delta assertions are specific to the feature branch history. P0.2 uses a new integration verifier instead.

### Governance preservation

All governance files already present on base `main` are preserved.

Current governed versions were explicitly carried forward for:

- `04-REFERENCE/AI-OPERATING-MEMORY.md`;
- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md`;
- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`.

The audit register preserves the prior governed content and appends the P0.2 JIT audit only.

No governance deletion from feature-branch history was replayed.

## P0.2 execution evidence

### Historical source proof

At source HEAD `c0116d195063c464d602fb699654ac61adc7290c`:

- workflow: `Research to Decision Persisted HEAD Re-break`;
- run/job: `35019876682 / 104552615501`;
- executable source-boundary suite: `50 passed`;
- reconstruction/copy/identity/self-attestation bypasses rejected;
- durable CI branch-neutral and read-only.

### Integration candidate proof

P0.2 persisted-HEAD re-break:

- run/job: `35130280160 / 104909282190`;
- HEAD: `fa43c44739e75c8d927626a2b3df8eefb185e00f`;
- exact persisted HEAD checkout: PASS;
- exact `main` ancestry: PASS;
- bounded allowlist import: PASS;
- 24 source-identical file identities: PASS;
- governance deletion check: PASS;
- repository suite: **`96 passed`**;
- targeted Tier-A suite: **`83 passed`**;
- provenance/forgeability attacks: PASS;
- durable CI branch-neutral/PR-covered/path-scoped/read-only: PASS;
- no multi-year acquisition/data/backtest surface: PASS;
- worktree: clean;
- permissions: `contents: read`, `metadata: read`.

Durable boundary workflows on the same integration candidate:

- DATA → CONTEXT: `35130279937 / 104909281059` — SUCCESS;
- CONTEXT → RESEARCH: `35130279821 / 104909280516` — SUCCESS;
- RESEARCH FINDINGS: `35130280001 / 104909281671` — SUCCESS;
- RESEARCH → DECISION: `35130279993 / 104909281053` — SUCCESS.

## Covered by P0.2

P0.2 closes only the integration validity of the already-qualified decision block on the authoritative integration work branch, including:

- branch creation from exact `main`;
- bounded source-identical transplant;
- preservation of current governance;
- re-break of the imported Tier-A boundaries;
- rejection of tested ResearchRunEvidence reconstruction/identity bypasses;
- branch-neutral durable CI;
- absence of accidental multi-year/acquisition/backtest import.

## Explicitly NOT covered by P0.2

P0.2 does not close or authorize:

- real producer junction `src/research/` → `ResearchRunEvidence`;
- inter-process attestation;
- complete `DECISION → RISK → ACTION → RESULT → TRACE` chain;
- complete transverse decision reconstruction through RESULT;
- resilience/restoration;
- multi-year Dukascopy / Trading Breaks / frozen execution-window technical import onto this integration branch;
- exact OOS split;
- native `.bi5` acquisition protocol/readiness/authorization;
- market-data acquisition;
- real backtest;
- promotion or live activation.

Historical global governance verdicts therefore remain:

- Decision Traceability: **FAIL** at the complete transverse-system level;
- Resilience / Continuity: **FAIL**;
- Change / Validity: **BLOCKED** where execution proof remains absent;
- Governance Effectiveness: **BLOCKED** globally despite bounded JIT PASSes.

## Freeze / multi-year truth remains external to integration branch for now

On the qualified multi-year branch, the outer execution window is already durably frozen at:

`2021-08-14 → 2026-08-14`

with:

- selected window: `68 / 68 / 0`, FAIL `0`;
- global envelope: `111 / 91 / 20`, global coverage still BLOCKED;
- freeze verdict: PASS;
- `.bi5` acquisition: NOT AUTHORIZED;
- real backtest: NOT AUTHORIZED.

Those facts are not yet imported as a technical block into `integration/system-v1`; P0.3 must import them explicitly and re-break them on the combined HEAD.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-P0.2-INTEGRATION-DECISION-BLOCK-PASS.md`
4. `reports/data-qualification/p0_2_decision_block_integration_qualification.md`
5. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
6. `.github/workflows/p0-2-decision-block-integration-rebreak.yml`
7. the four durable imported boundary workflows
8. `src/context.py`, `src/context_identity.py`, `src/research_run_evidence.py`, `src/research_findings.py`, `src/decision.py`, `src/decision_trace.py`
9. the seven imported adversarial/boundary tests
10. inspect `feat/multi-year-dukascopy-acquisition` current checkpoint/report before designing P0.3
11. compare active branch HEAD against this checkpoint before any mutation.

## Exactly one next governed action

**P0.3 — determine the minimal already-qualified multi-year import surface from `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`, import that surface into `integration/system-v1` by explicit allowlist only, then re-break both the already-integrated decision Tier-A boundaries and the imported data/calendar/freeze Tier-A boundaries on the combined integration HEAD.**

Rules for P0.3:

- no blind merge;
- no replay of feature-branch deletions;
- preserve all P0.2 decision-block identities unless an observed compatibility defect requires an explicit governed correction;
- import the smallest proven multi-year surface rather than branch history;
- preserve the 20 unresolved global Trading Breaks candidates outside the frozen window;
- do not acquire `.bi5`;
- do not issue new broker probes merely to repeat already-qualified evidence;
- do not run a real backtest;
- any critical compatibility correction must be adversarially re-broken before PASS.
