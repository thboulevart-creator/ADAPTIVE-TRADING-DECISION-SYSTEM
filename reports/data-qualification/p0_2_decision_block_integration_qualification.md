# P0.2 — Controlled Decision-Block Integration Qualification

**Date:** 16 septembre 2026  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Integration branch:** `integration/system-v1`  
**Base main:** `43ec28f3e09856fe508874af3aaf32079761d2d5`  
**Qualified source block:** `feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`  
**Technical integration candidate:** `fa43c44739e75c8d927626a2b3df8eefb185e00f`  
**Verdict:** **PASS — `QUALIFIED_DECISION_BLOCK_CONTROLLED_IMPORT_SURVIVES_INTEGRATION_REBREAK`**

## 1. Objective

Create the authoritative controlled integration work branch from `main`, import the already-qualified decision-producer block without a blind merge, preserve the governance corpus, and independently re-break the imported Tier-A boundaries before any multi-year import.

No `.bi5` acquisition, broker probe, market-data download, Strategy Tester execution, real backtest, or multi-year Trading Breaks technical import occurred.

## 2. Why no branch merge was used

At the start of P0.2:

- `main` HEAD: `43ec28f3e09856fe508874af3aaf32079761d2d5`;
- `feat/decision-producer-contract` HEAD: `c0116d195063c464d602fb699654ac61adc7290c`;
- compare state: diverged;
- feature branch ahead of current `main`: `56` commits;
- feature branch behind current `main`: `6` commits.

Therefore a merge/cherry-pick history replay would have mixed unrelated branch history and risked replaying stale governance state. P0.2 used a file-level controlled transplant instead.

## 3. Imported source-identical block

Exactly 24 files are required to remain byte-identical to the qualified decision source HEAD:

- 4 durable boundary workflows:
  - `data-to-context.yml`;
  - `context-to-research-boundary.yml`;
  - `research-findings-contract.yml`;
  - `research-to-decision-boundary.yml`;
- 6 STEP/manifest governance documents from the decision workstream;
- `docs/RESEARCH-FINDINGS-CONTRACT.md`;
- 6 executable source modules:
  - `src/context.py`;
  - `src/context_identity.py`;
  - `src/decision.py`;
  - `src/decision_trace.py`;
  - `src/research_findings.py`;
  - `src/research_run_evidence.py`;
- 7 executable/adversarial test files.

The old source-only verifier `.github/workflows/research-to-decision-persisted-head.yml` was deliberately **not** transplanted because it encodes ancestry and verifier-only-delta assertions specific to the source feature history. Copying it unchanged would have asserted a false integration ancestry.

## 4. Governance preservation

The integration branch was created exactly from current `main`, so all pre-existing `main` governance files were inherited first.

Three global governance artifacts were then brought to the current qualified governance state from `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`:

- `04-REFERENCE/AI-OPERATING-MEMORY.md`;
- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md`;
- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`.

The integration verifier proves:

- every governance path that existed on the base `main` still exists;
- only the audit register and evolution/audit protocol are changed among pre-existing `GOVERNANCE/` files;
- the evolution/audit protocol remains byte-identical to the current governed source;
- the audit register preserves the prior governed content and only extends it with the P0.2 JIT audit;
- no feature-branch governance deletion is replayed.

## 5. Original source qualification retained as historical evidence

At source HEAD `c0116d195063c464d602fb699654ac61adc7290c`:

- workflow: `Research to Decision Persisted HEAD Re-break`;
- run/job: `35019876682 / 104552615501`;
- executable boundary suite: `50 passed`;
- exact reconstruction, `copy.copy`, `copy.deepcopy`, legacy `_factory_validated`, all seven identity-field mutations, direct `__dict__` mutation and unattested `ResearchFindings` seeding were rejected;
- durable boundary workflows were proven branch-neutral, PR-covered, path-scoped and read-only.

P0.2 did not merely trust this historical PASS; it re-broke the imported boundaries on the integration branch.

## 6. Integration candidate proof

Candidate commit:

`fa43c44739e75c8d927626a2b3df8eefb185e00f`

The diff from base `main` is one bounded commit containing only the controlled decision block, current governance preservation updates, and the P0.2 verifier.

### P0.2 persisted-HEAD re-break

- workflow: `P0.2 Decision Block Integration Persisted HEAD Re-break`;
- run/job: `35130280160 / 104909282190`;
- conclusion: **SUCCESS**;
- exact persisted HEAD checkout: PASS;
- exact base-main ancestry: PASS;
- all 24 controlled-import file identities vs source decision HEAD: PASS;
- governance preservation/no deletion: PASS;
- complete integration-branch repository suite: **`96 passed`**;
- imported Tier-A focused suite: **`83 passed`**;
- provenance/reconstruction/identity bypass attacks: PASS;
- durable boundary CI branch-neutral/read-only: PASS;
- no multi-year acquisition/data/backtest surface imported: PASS;
- worktree: clean;
- permissions: `contents: read`, `metadata: read`.

### Durable boundary workflows on the same SHA

All four imported durable workflows executed successfully on `integration/system-v1`:

- DATA → CONTEXT: run/job `35130279937 / 104909281059` — SUCCESS (`16 passed` + downstream CONTEXT→RESEARCH `17 passed`);
- CONTEXT → RESEARCH: run/job `35130279821 / 104909280516` — SUCCESS;
- RESEARCH FINDINGS: run/job `35130280001 / 104909281671` — SUCCESS;
- RESEARCH → DECISION: run/job `35130279993 / 104909281053` — SUCCESS.

## 7. What P0.2 proves

P0.2 proves, on the controlled integration branch, that the imported block preserves and revalidates:

`DATA → CONTEXT → RESEARCH FINDINGS / EVIDENCE → DECISION`

for the executable contracts actually present in the imported block, including the critical anti-forgery/provenance boundary around `ResearchRunEvidence`.

It also proves that this import did not require a blind merge and did not delete the current governance corpus.

## 8. What P0.2 does NOT prove

P0.2 does not close:

- the real runtime producer junction `src/research/` → `ResearchRunEvidence`;
- inter-process attestation;
- the complete `DECISION → RISK → ACTION → RESULT → TRACE` chain;
- complete transverse reconstruction of an operational decision through its result;
- resilience/restoration;
- the multi-year Dukascopy / Trading Breaks / frozen-window technical block on the integration branch;
- exact OOS split;
- native `.bi5` acquisition readiness or authorization;
- real backtesting;
- promotion/live activation.

Therefore the historical governance verdicts for full Decision Traceability and Resilience/Continuity are not promoted to PASS by this block.

## 9. Verdict

**PASS — `QUALIFIED_DECISION_BLOCK_CONTROLLED_IMPORT_SURVIVES_INTEGRATION_REBREAK`**

The first authoritative controlled import is valid on `integration/system-v1`. The decision-producer block survives independent Tier-A re-breaks on top of current `main` while preserving governance. No multi-year technical block has yet been imported.

## 10. Next governed action

**P0.3 — determine the minimal already-qualified multi-year import surface from `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`, import that surface into `integration/system-v1` by explicit allowlist only, then re-break both the existing decision boundaries and the imported data/calendar/freeze Tier-A boundaries on the combined integration HEAD.**

Still prohibited during P0.3:

- blind merge;
- `.bi5` acquisition;
- broker probes performed only to repeat already-qualified evidence;
- real backtest.
