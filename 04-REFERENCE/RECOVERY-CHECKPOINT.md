# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.3 MULTI-YEAR INTEGRATION PASS / RESEARCH PRODUCER JUNCTION NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, tests, workflow evidence and this checkpoint are authoritative. Do not reconstruct project state from conversation memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Integration lineage

`integration/system-v1` was created from:

`main@43ec28f3e09856fe508874af3aaf32079761d2d5`

P0.2 qualified decision source:

`feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

P0.2 closed integration HEAD before P0.3:

`45d9bc8c4bf133eced67ccede7c5f439253869b7`

P0.3 qualified multi-year source:

`feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

P0.3 technical integration candidate:

`36e207abf779c02ea99f2d2e66ddf4b6bc7103d2`

No blind merge, rebase, reset, force-push or branch-history replay was used.

## P0.2 — decision-block integration remains CLOSED

Verdict remains:

**PASS — `QUALIFIED_DECISION_BLOCK_CONTROLLED_IMPORT_SURVIVES_INTEGRATION_REBREAK`**

The 24 controlled decision-block artifacts remain byte-identical to their qualified source. The P0.3 verifier re-checks those identities and re-breaks the critical `RESEARCH → DECISION` anti-forgery boundary.

## P0.3 — controlled multi-year freeze-surface integration CLOSED

Verdict:

**PASS — `QUALIFIED_MULTI_YEAR_FREEZE_SURFACE_SURVIVES_COMBINED_INTEGRATION_REBREAK`**

Durable qualification report:

`reports/data-qualification/p0_3_multi_year_integration_qualification.md`

JIT governance audit:

`GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md` — `P0_3_MULTI_YEAR_INTEGRATION_JIT_AUDIT_V1`

Combined persisted-HEAD verifier:

`.github/workflows/p0-3-multi-year-integration-rebreak.yml`

### Exact minimal source-identical surface

P0.3 imports exactly 19 source-identical multi-year files required to reproduce current calendar/freeze truth:

- 4 versioned rule/protocol/freeze artifacts;
- 7 proof/runtime derivation tools;
- 2 terminal state registries;
- 6 current-state / Tier-A tests.

The exact list is recorded in the P0.3 qualification report and enforced executablely by the verifier.

### Deliberately excluded from current integration truth

Not imported:

- `.bi5` files;
- `data/` or `LOCAL-EVIDENCE/`;
- Dukascopy downloader/probe/qualification tooling;
- capability activation / historical recovery integration scripts;
- `src/research/`;
- historical pre-closure current-state tests that assert attempt count 68 or non-empty recovery queues;
- any real backtest execution surface.

## P0.3 candidate execution evidence

Workflow:

`P0.3 Combined Decision and Multi-Year Persisted HEAD Re-break`

Run/job:

`35132710182 / 104917355632`

HEAD:

`36e207abf779c02ea99f2d2e66ddf4b6bc7103d2`

Conclusion: **SUCCESS**.

Evidence:

- exact persisted HEAD and P0.2 ancestry: PASS;
- multi-year allowlist/source identity: PASS;
- all 24 P0.2 decision identities preserved: PASS;
- governance deletion check: PASS;
- combined repository suite: **176 passed**;
- decision Tier-A suite: **83 passed**;
- calendar/freeze Tier-A suite: **80 passed**;
- decision provenance/forgeability attacks: PASS;
- durable decision CI branch-neutral/read-only: PASS;
- no acquisition/probe/recovery-history/backtest execution surface imported: PASS;
- worktree: clean;
- workflow permissions: `contents: read`, `metadata: read`.

## Current multi-year truth on integration branch

The combined integration state re-derives:

- coverage envelope: `2018-05-01 → 2026-08-14`;
- global candidates/resolved/unresolved: `111 / 91 / 20`;
- global coverage verdict: **BLOCKED**;
- all 20 unresolved global dates are before selected-window start;
- selected window: `2021-08-14 → 2026-08-14`;
- selected-window candidates/resolved/unresolved: `68 / 68 / 0`;
- selected-window FAIL count: `0`;
- recovery ledger attempts: `73`;
- material capability changes: `1`;
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`;
- capability fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`;
- recovery queue: `0`;
- progression decisions: `0`;
- eligible recovery queue: `0`;
- current freeze eligibility: **PASS**;
- persisted execution-window freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED — `MANDATORY_WINDOW_GATES_NOT_PASS`**;
- persisted `massive_acquisition_authorized`: `false`;
- persisted `real_backtest_authorized`: `false`.

## Covered by P0.3

P0.3 closes only:

- controlled source-identical import of the minimal final multi-year proof surface;
- coexistence of that surface with the P0.2 decision block;
- current calendar truth and outside-gap visibility;
- proof-derived execution-window boundary state;
- persisted freeze validity;
- continued rejection of tested decision provenance forgeries;
- continued absence of acquisition/backtest authorization.

## Explicitly NOT covered by P0.3

Still open / not authorized:

- `src/research/` → `ResearchRunEvidence` real producer junction;
- inter-process attestation;
- native `.bi5` acquisition protocol/readiness/authorization;
- tick completeness, manifests and reconciliation;
- exact OOS split;
- `DECISION → RISK → ACTION → RESULT → TRACE`;
- complete transverse decision reconstruction;
- resilience/restoration;
- real backtest;
- promotion or live activation.

Historical global governance verdicts therefore remain unchanged where not directly closed by this bounded audit:

- Decision Traceability: **FAIL** globally;
- Resilience / Continuity: **FAIL**;
- Governance Effectiveness: **BLOCKED** globally despite bounded JIT PASSes.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-P0.3-INTEGRATION-MULTI-YEAR-PASS.md`
4. `reports/data-qualification/p0_3_multi_year_integration_qualification.md`
5. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
6. `.github/workflows/p0-3-multi-year-integration-rebreak.yml`
7. the four durable P0.2 decision-boundary workflows
8. the 24 P0.2 controlled decision artifacts
9. the 19 P0.3 source-identical multi-year artifacts listed in the qualification report
10. inspect `src/research/` and its relevant tests on verified source revisions before designing P0.4
11. compare active branch HEAD against this checkpoint before any mutation.

## Exactly one next governed action

**P0.4 — map the existing `src/research/` runtime producer surface against the integrated `ResearchRunEvidence` contract, formalize the minimal producer-junction boundary, then adversarially qualify that junction before importing or wiring any research runtime into `integration/system-v1`.**

Rules for P0.4:

- no blind merge;
- do not import all of `src/research/` merely because it exists;
- preserve all P0.2 and P0.3 qualified identities unless an observed compatibility defect requires a governed correction;
- treat `src/research/ → ResearchRunEvidence` as a Tier-A boundary if it can authorize downstream decision use;
- no `.bi5` acquisition;
- no redundant broker/network probe;
- no real backtest;
- any compatibility correction must be adversarially re-broken before PASS.
