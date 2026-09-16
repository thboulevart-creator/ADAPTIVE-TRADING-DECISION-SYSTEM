# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0.4 RESEARCH PRODUCER JUNCTION PASS / DOCUMENTARY REBREAK PENDING

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Active branch: `integration/system-v1`

## Source of truth

GitHub code, persisted qualification reports, tests, workflow evidence and this checkpoint are authoritative. Do not reconstruct project state from conversation memory.

Construction rule:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

Allowed verdicts: `PASS / FAIL / BLOCKED`. `BLOCKED` is never `PASS`.

## Integration lineage

Base integration branch:

`main@43ec28f3e09856fe508874af3aaf32079761d2d5`

P0.2 qualified decision source:

`feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`

P0.3 qualified multi-year source:

`feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`

No blind merge, rebase, reset, force-push or branch-history replay is authorized by this checkpoint.

## P0.2 — decision block remains CLOSED

Current regression verdict:

**PASS — qualified P0.2 decision invariants survive the governed P0.4 evolution.**

On combined HEAD:

`3b09bd9f6e06fd8833f7bd93d98e839e335000b5`

P0.2 run/job:

`35140401689 / 104943189786` — **SUCCESS**

Evidence:

- 21 protected P0.2 artifacts remain source-identical;
- 3 authorization-bearing artifacts are explicitly handed to P0.4:
  - `src/research_run_evidence.py`
  - `tests/test_context_research_alternative_paths.py`
  - `tests/test_research_to_decision_boundary.py`
- decision Tier-A suite: `83 passed`;
- raw research-evidence minter absent;
- copy/reconstruction/mutation anti-forgery properties survive;
- durable decision workflows remain branch-neutral and read-only;
- worktree clean.

The P0.2 guard is a composable regression guard, not a freeze preventing later governed evolution.

## P0.3 — multi-year freeze surface remains CLOSED

Current verdict:

**PASS — qualified multi-year calendar/freeze truth survives the governed P0.4 integration.**

P0.3 run/job on the same combined HEAD:

`35140401667 / 104943190208` — **SUCCESS**

Evidence:

- 19 protected P0.3 artifacts remain source-identical to the qualified multi-year source;
- P0.4 downstream handoff is explicit;
- shared upstream boundary suite: `72 passed`;
- calendar/freeze Tier-A suite: `80 passed`;
- current global truth: `111 / 91 / 20`;
- global coverage verdict: **BLOCKED**;
- all 20 unresolved dates remain outside and before the frozen selected window;
- selected window: `2021-08-14 → 2026-08-14`;
- selected-window truth: `68 / 68 / 0`, FAIL `0`;
- persisted execution-window freeze: **PASS**;
- acquisition after persisted freeze: **BLOCKED**;
- persisted `massive_acquisition_authorized = false`;
- persisted `real_backtest_authorized = false`;
- worktree clean.

P0.4 does not widen any P0.3 acquisition or backtest permission.

## P0.4 — real research producer junction qualified

Contract:

`04-REFERENCE/RESEARCH-PRODUCER-JUNCTION-CONTRACT.md`

Marker:

`RESEARCH_PRODUCER_JUNCTION_V1`

Durable qualification report:

`reports/data-qualification/p0_4_research_producer_junction_qualification.md`

JIT governance audit marker:

`P0_4_RESEARCH_PRODUCER_JUNCTION_JIT_AUDIT_V1`

Session backup:

`99-BACKUP/SESSION-2026-09-16-P0.4-RESEARCH-PRODUCER-JUNCTION-PASS.md`

### Exact runtime surface

Exactly five `src/research/` files are integrated:

1. `src/research/__init__.py`
2. `src/research/bi5_reader.py`
3. `src/research/input_binding.py`
4. `src/research/engine.py`
5. `src/research/execution.py`

`__init__.py` and `bi5_reader.py` remain source-identical to the qualified multi-year source. The authorization-bearing input/execution path was minimally hardened for P0.4.

No `.bi5` corpus, `data/`, `LOCAL-EVIDENCE/`, acquisition downloader, network probe, historical recovery script or real backtest execution surface was imported.

### Admissible producer chain

`QualifiedResearchInput → BoundResearchInput → deterministic runtime execution → ResearchExecutionResult → ResearchRunEvidence → ResearchFindings / DECISION`

Required properties:

- only factory-bound input reaches the engine;
- bound input is process-locally identity/content attested;
- execution result is process-locally identity/content attested and bound to its exact input;
- empty execution is non-authorizing;
- Dataset and full Context identities must match;
- corpus and contract hashes must match;
- observation bounds and code version must match;
- only `from_research_execution(...)` can produce downstream-attested `ResearchRunEvidence`;
- legacy `from_v43_report(...)` remains compatibility-only and non-authorizing;
- raw `_attest_factory_evidence` is absent from module scope.

### Initial Tier-A FAIL

Pre-integration breaker HEAD:

`5619f6d3ae608bf9a3f0871345815b7906a6caba`

Run/job:

`35136475040 / 104929994347`

Observed failures:

1. report-only V4.3 evidence could authorize downstream use without real runtime execution;
2. raw evidence-attestation minter was module-visible;
3. manual evidence could reach that minter.

This state was correctly classified **FAIL**.

### Corrected full C0–C15 qualification

Corrected code qualification HEAD:

`edb2501a2b09bd142f037a82f6971696c08c1213`

Run/job:

`35137560719 / 104933628790` — **SUCCESS**

Results:

- complete repository: `192 passed`;
- P0.4 C0 + C1–C15: `16 passed`;
- upstream decision boundary: `73 passed`;
- calendar/freeze boundary: `80 passed`;
- exact five-file runtime surface: PASS;
- raw minter absent: PASS;
- no acquisition/probe/data/backtest surface: PASS;
- worktree clean;
- read-only workflow permissions.

No further P0.4 defect was observed.

## Same-SHA combined proof

All three dedicated P0.2/P0.3/P0.4 regression guards are green on the same persisted SHA:

`3b09bd9f6e06fd8833f7bd93d98e839e335000b5`

- P0.2: `35140401689 / 104943189786` — SUCCESS — `83 passed` Tier-A decision suite;
- P0.3: `35140401667 / 104943190208` — SUCCESS — `72 passed` shared upstream + `80 passed` calendar/freeze;
- P0.4: `35140401707 / 104943190275` — SUCCESS — `192 passed` repository + `16 passed` C0–C15 + `73 passed` decision + `80 passed` calendar/freeze.

All are read-only and clean-worktree qualified.

## Covered by P0.4

P0.4 closes only:

- the in-process real `src/research/ → ResearchRunEvidence` producer junction;
- exact five-file runtime integration;
- factory-bound input/result provenance;
- tested report-only/manual/copy/reconstruction/mutation/rebinding rejection;
- downstream use of only runtime-attested research evidence;
- preservation/composability of P0.2 and P0.3;
- deterministic synthetic local BI5 qualification.

## Explicitly NOT covered by P0.4

Still open / not authorized:

- inter-process or persisted attestation;
- native `.bi5` acquisition protocol/readiness/authorization;
- acquisition manifests, tick completeness/exhaustiveness and reconciliation;
- exact OOS split;
- real-data backtest;
- `DECISION → RISK → ACTION → RESULT → TRACE` complete chain;
- complete transverse decision reconstruction;
- resilience/restoration;
- promotion gate or live activation.

Historical global governance verdicts remain unchanged outside the bounded P0.4 scope:

- Decision Traceability: **FAIL globally** until the downstream transverse chain is proven;
- Resilience / Continuity: **FAIL**;
- Governance Effectiveness: **BLOCKED globally**, despite bounded JIT PASSes.

## Documentary closure status

The P0.4 code boundary and the same-SHA P0.2/P0.3/P0.4 regression state are qualified **PASS**.

This checkpoint is part of the documentary closure candidate. P0.4 becomes durably closed only after a final read-only persisted-HEAD P0.4 re-break succeeds on the exact HEAD containing:

- this checkpoint;
- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md` with `P0_4_RESEARCH_PRODUCER_JUNCTION_JIT_AUDIT_V1`;
- `reports/data-qualification/p0_4_research_producer_junction_qualification.md`;
- `99-BACKUP/SESSION-2026-09-16-P0.4-RESEARCH-PRODUCER-JUNCTION-PASS.md`;
- the final P0.4 persisted-HEAD workflow.

No substantive write may follow that successful final re-break without reopening qualification.

## Mandatory recovery order before next substantive block

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-P0.4-RESEARCH-PRODUCER-JUNCTION-PASS.md`
4. `reports/data-qualification/p0_4_research_producer_junction_qualification.md`
5. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
6. `04-REFERENCE/RESEARCH-PRODUCER-JUNCTION-CONTRACT.md`
7. `.github/workflows/p0-4-research-producer-junction.yml`
8. `.github/workflows/p0-2-decision-block-integration-rebreak.yml`
9. `.github/workflows/p0-3-multi-year-integration-rebreak.yml`
10. `src/research_run_evidence.py`
11. the five `src/research/` runtime files
12. `tests/test_research_producer_junction_tier_a.py`
13. `tests/research_runtime_fixture.py`
14. verify branch HEAD and the latest successful final P0.4 persisted-HEAD re-break before any mutation.

## Next governed action after final documentary re-break

Do not start it until P0.4 documentary closure is proven.

The next block must be selected from the remaining explicitly open architecture, not inferred as authorization for acquisition or real backtest. In particular, native acquisition, exact OOS split, inter-process attestation and downstream execution/risk remain separate gates.
