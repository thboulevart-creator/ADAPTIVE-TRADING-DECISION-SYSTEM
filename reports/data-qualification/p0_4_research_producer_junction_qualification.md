# P0.4 — Research Producer Junction Qualification

Date: 16 September 2026  
Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`  
Contract: `RESEARCH_PRODUCER_JUNCTION_V1`

## Question

Can the existing `src/research/` runtime produce the only downstream-admissible `ResearchRunEvidence` without allowing report-only, reconstructed, copied, mutated or manually attested evidence to bypass the real research execution boundary?

## Construction rule

`UNDERSTAND → COMPARE → BREAK → DECIDE`

P0.4 is a Tier-A boundary because acceptance of forged or unexecuted research evidence can authorize downstream research findings and decisions.

## Cartography

The source runtime surface required for the junction is exactly five files:

1. `src/research/__init__.py`
2. `src/research/bi5_reader.py`
3. `src/research/input_binding.py`
4. `src/research/engine.py`
5. `src/research/execution.py`

`src/research/__init__.py` and `src/research/bi5_reader.py` remain source-identical to `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`. The other three runtime files are the minimal authorization-bearing surface that required hardening for the integrated junction.

No `.bi5` corpus, acquisition downloader, Dukascopy network probe, data directory, recovery script or real backtest surface was imported.

## Minimal junction

The admissible path is:

`QualifiedResearchInput → BoundResearchInput → deterministic runtime execution → ResearchExecutionResult → ResearchRunEvidence → ResearchFindings / DECISION`

The junction requires:

- input binding before execution;
- process-local identity/content attestation of `BoundResearchInput`;
- process-local identity/content attestation of `ResearchExecutionResult`;
- a non-empty execution result;
- coherence between execution result and the exact bound input;
- coherence with Dataset identity and full Context identity;
- source/corpus and instrument-contract hashes;
- observation-bound coherence;
- explicit non-empty code version;
- downstream attestation minted only by the runtime-evidence factory.

The legacy V4.3 report path remains readable for compatibility, but it is non-authorizing: report-only evidence is not factory-attested for downstream decision use.

The raw `_attest_factory_evidence` escape is absent from module scope.

## Initial adversarial break

Pre-integration breaker HEAD:

`5619f6d3ae608bf9a3f0871345815b7906a6caba`

Run/job:

`35136475040 / 104929994347`

Inherited upstream boundary suite before the new attacks:

`56 passed`

The new Tier-A breaker then failed exactly as intended on all three initially mapped bypasses:

1. V4.3 report-only evidence was downstream-attested without real runtime execution;
2. the raw evidence-attestation minter was reachable at module scope;
3. a manually built `ResearchRunEvidence` could reach that raw minter.

Initial verdict: **FAIL**, proving that an integration without correction was not admissible.

## Correction

The correction retained the exact five-file runtime surface and changed only the authorization-bearing path necessary to close the observed bypasses:

- `BoundResearchInput` is factory-bound and attested;
- runtime execution returns an attested `ResearchExecutionResult` bound to that input;
- empty execution cannot authorize evidence;
- `ResearchRunEvidence` downstream attestation is available only through the real execution factory;
- report-only V4.3 compatibility evidence is non-authorizing;
- raw module-level evidence minter is absent;
- downstream decision/findings fixtures now use deterministic local synthetic BI5 execution rather than report-only evidence.

Synthetic BI5 fixtures are created only inside tests. They are not acquisition evidence and do not authorize any real-data acquisition or backtest.

## Full Tier-A attack matrix

`tests/test_research_producer_junction_tier_a.py` covers the positive path C0 and attacks C1–C15, including:

- report-only bypass;
- raw minter/module escape;
- manual evidence promotion;
- copy and exact reconstruction;
- post-binding mutation;
- post-execution mutation;
- source-byte mutation after binding;
- result/input rebinding;
- empty execution;
- Dataset forgery;
- Context forgery;
- code-version forgery;
- downstream `ResearchFindings` / `DECISION` bypass attempts.

Corrected code qualification HEAD:

`edb2501a2b09bd142f037a82f6971696c08c1213`

P0.4 run/job:

`35137560719 / 104933628790`

Results:

- complete repository regression: `192 passed`;
- P0.4 C0–C15: `16 passed`;
- upstream decision Tier-A regression: `73 passed`;
- P0.3 calendar/freeze Tier-A regression: `80 passed`;
- exact five-file runtime surface: PASS;
- no raw minter: PASS;
- no acquisition/probe/data/backtest surface: PASS;
- worktree: clean;
- workflow permissions: read-only.

No further P0.4 defect was observed.

## Same-SHA combined regression proof

After making P0.2 and P0.3 regression guards composable with the governed P0.4 handoff, all three dedicated gates were executed against the same persisted SHA:

`3b09bd9f6e06fd8833f7bd93d98e839e335000b5`

### P0.2

Run/job: `35140401689 / 104943189786` — **SUCCESS**

- 21 P0.2 artifacts remain source-identical;
- 3 authorization-bearing P0.2 artifacts are explicitly handed to qualified P0.4;
- decision Tier-A suite: `83 passed`;
- anti-forgery properties survive P0.4;
- durable decision CI remains branch-neutral/read-only;
- worktree clean.

### P0.3

Run/job: `35140401667 / 104943190208` — **SUCCESS**

- 19 P0.3 artifacts remain source-identical;
- governed P0.4 downstream handoff is explicit;
- shared upstream boundary regression: `72 passed`;
- calendar/freeze Tier-A suite: `80 passed`;
- current `111/91/20` global and `68/68/0` selected-window truth survives;
- global coverage remains BLOCKED;
- persisted freeze remains PASS;
- acquisition remains BLOCKED;
- worktree clean.

### P0.4

Run/job: `35140401707 / 104943190275` — **SUCCESS**

- complete repository regression: `192 passed`;
- C0–C15 producer-junction suite: `16 passed`;
- upstream decision boundary: `73 passed`;
- calendar/freeze boundary: `80 passed`;
- exact five-file runtime surface: PASS;
- raw minter absent: PASS;
- no acquisition/probe/data/backtest surface: PASS;
- worktree clean;
- permissions read-only.

## Covered by P0.4

P0.4 closes, for this bounded scope:

- the real in-process `src/research/ → ResearchRunEvidence` producer junction;
- the five-file research runtime integration surface;
- binding of accepted evidence to actual deterministic runtime execution;
- rejection of the tested report-only/manual/copy/reconstruction/mutation/rebinding bypasses;
- preservation of qualified P0.2 decision and P0.3 calendar/freeze boundaries;
- deterministic synthetic-test qualification without acquisition or real backtest.

## Explicitly not covered by P0.4

P0.4 does **not** qualify or authorize:

- inter-process or persisted attestation;
- native `.bi5` acquisition readiness/authorization;
- acquisition manifests, tick exhaustiveness or reconciliation;
- exact OOS split;
- real-data backtest execution;
- `DECISION → RISK → ACTION → RESULT → TRACE`;
- complete transverse reconstruction from decision through result;
- resilience/restoration;
- promotion gate or live activation.

The historical global governance verdicts therefore remain unchanged where this bounded work does not close them.

## Verdict

**PASS — `RESEARCH_PRODUCER_JUNCTION_V1` is qualified for the covered in-process Tier-A boundary.**

This report is a documentary closure candidate. Final P0.4 closure additionally requires a read-only persisted-HEAD re-break of the exact HEAD containing this report, the JIT audit entry, recovery checkpoint and session backup. No substantive artifact may change after that successful final re-break without reopening qualification.
