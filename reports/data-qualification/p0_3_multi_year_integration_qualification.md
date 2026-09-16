# P0.3 — Controlled Multi-Year Freeze-Surface Integration Qualification

**Date:** 16 septembre 2026  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Integration branch:** `integration/system-v1`  
**P0.2 base:** `45d9bc8c4bf133eced67ccede7c5f439253869b7`  
**Qualified multi-year source:** `feat/multi-year-dukascopy-acquisition@b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`  
**Technical integration candidate:** `36e207abf779c02ea99f2d2e66ddf4b6bc7103d2`  
**Verdict:** **PASS — `QUALIFIED_MULTI_YEAR_FREEZE_SURFACE_SURVIVES_COMBINED_INTEGRATION_REBREAK`**

## 1. Objective

Import into `integration/system-v1` only the already-qualified multi-year surface required to reproduce and adversarially verify current calendar coverage, terminal Trading Breaks state, execution-window derivation and persisted freeze, while preserving the complete P0.2 decision block.

P0.3 explicitly prohibited blind merge, `.bi5` acquisition, new broker/network probes, replay of recovery history and real backtesting.

## 2. Why the branch history was not merged

The multi-year branch contains a long recovery/acquisition history, historical-state tests and probe/downloader tooling that are not required to reproduce the final qualified state. Importing branch history would enlarge the trusted computing surface and could reintroduce historical regression worlds as current truth.

P0.3 therefore used a strict file allowlist from the exact qualified source HEAD.

## 3. Minimal source-identical multi-year surface

Exactly **19 source files** are imported byte-for-byte from `b7d13bb3492fb6e1f0d4dcab64079bf1a8f55698`.

### Versioned policy/freeze evidence

1. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
2. `04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`
3. `04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`
4. `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md`

### Proof/runtime derivation surface

5. `tools/coverage_execution_window_boundary.py`
6. `tools/current_execution_window_boundary_state.py`
7. `tools/dukascopy_usatech_calendar.py`
8. `tools/dukascopy_usatech_calendar_coverage.py`
9. `tools/frozen_execution_window.py`
10. `tools/trading_breaks_recovery_progression.py`
11. `tools/trading_breaks_recovery_protocol.py`

### Persisted terminal state

12. `reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`
13. `reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

### Current-state / Tier-A tests

14. `tests/test_coverage_execution_window_boundary.py`
15. `tests/test_current_execution_window_boundary_state.py`
16. `tests/test_dukascopy_usatech_calendar.py`
17. `tests/test_dukascopy_usatech_calendar_coverage.py`
18. `tests/test_frozen_execution_window.py`
19. `tests/test_trading_breaks_post_closure_current_state.py`

The integration-specific verifier is new and is not claimed to be source-identical:

`.github/workflows/p0-3-multi-year-integration-rebreak.yml`

## 4. Deliberate exclusions

P0.3 does **not** import historical transition mechanisms merely because they exist on the source branch. In particular it excludes:

- `tools/activate_trading_breaks_target_day_overlap_capability.py`;
- `tools/trading_breaks_target_day_overlap_semantics.py`;
- `tools/integrate_trading_breaks_calendar_closure.py`;
- Dukascopy download/probe/qualification acquisition tooling;
- `data/` and `LOCAL-EVIDENCE/`;
- `.bi5` files;
- `src/research/`;
- historical current-state tests such as `test_trading_breaks_calendar_closure_integration_contract.py`, `test_trading_breaks_target_day_overlap_v2_state.py` and `test_trading_breaks_recovery_progression.py`.

Those historical tests encode pre-closure states such as attempt count 68 and non-empty recovery queues. Importing them as current regression truth would recreate the P0.0 defect that was already corrected on the source workstream.

## 5. P0.2 preservation

The combined verifier re-checks all 24 source-identical P0.2 decision-block artifacts against `feat/decision-producer-contract@c0116d195063c464d602fb699654ac61adc7290c`.

No P0.2 functional artifact was modified by the candidate commit. The diff from P0.2 base contains exactly 19 multi-year additions plus the P0.3 verifier.

## 6. Candidate persisted-HEAD re-break

Candidate:

`36e207abf779c02ea99f2d2e66ddf4b6bc7103d2`

Workflow:

`P0.3 Combined Decision and Multi-Year Persisted HEAD Re-break`

Run/job:

`35132710182 / 104917355632`

Conclusion: **SUCCESS**.

### Executable regression results

- complete combined repository suite: **`176 passed`**;
- P0.2 decision Tier-A suite: **`83 passed`**;
- multi-year calendar/freeze Tier-A suite: **`80 passed`**.

### Re-derived current truth

The verifier independently derives and checks:

- global calendar: `111 candidates / 91 resolved / 20 unresolved`;
- selected execution window: `68 candidates / 68 resolved / 0 unresolved`;
- all 20 unresolved global dates are outside the selected window and earlier than `2021-08-14`;
- window: `2021-08-14 → 2026-08-14`;
- terminal recovery state: 73 attempts, 1 material capability change, recovery/progression/eligible queues empty;
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`;
- capability fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`;
- `FREEZE_EXECUTION_WINDOW`: PASS;
- persisted freeze: PASS;
- `DECLARE_GLOBAL_COVERAGE_PASS`: BLOCKED;
- acquisition after persisted freeze: BLOCKED with `MANDATORY_WINDOW_GATES_NOT_PASS`;
- persisted freeze explicitly records `massive_acquisition_authorized=false` and `real_backtest_authorized=false`.

### Cross-block adversarial re-break

The decision provenance/forgeability boundary was re-attacked with the multi-year surface present. Reconstructed evidence, shallow/deep copies, legacy self-attestation, identity-field mutation, direct `__dict__` mutation and unattested ResearchFindings seeding remain rejected.

The four durable decision workflows remain branch-neutral, PR-covered, path-scoped and read-only.

Worktree after the verifier: clean. GitHub token permissions: `contents: read`, `metadata: read`.

## 7. What P0.3 proves

P0.3 proves that the already-qualified multi-year **final proof state** can coexist with the already-qualified decision block on `integration/system-v1` without mutating either block's critical identities and without importing recovery/acquisition history that is unnecessary for the final proof.

The combined branch now reproduces both:

`DATA → CONTEXT → RESEARCH FINDINGS / EVIDENCE → DECISION`

and the governed calendar/freeze truth:

`GLOBAL COVERAGE → SELECTED EXECUTION WINDOW → PROOF-DERIVED BOUNDARY STATE → DURABLE FREEZE`.

## 8. What P0.3 does NOT prove or authorize

P0.3 does not close:

- the real runtime producer junction `src/research/` → `ResearchRunEvidence`;
- inter-process attestation;
- native `.bi5` acquisition protocol/readiness/authorization;
- tick completeness/manifests/reconciliation;
- exact OOS split;
- `DECISION → RISK → ACTION → RESULT → TRACE`;
- complete transverse decision reconstruction;
- resilience/restoration;
- real backtesting;
- promotion or live activation.

Global coverage therefore remains BLOCKED and acquisition/backtest remain unauthorized.

## 9. Verdict

**PASS — `QUALIFIED_MULTI_YEAR_FREEZE_SURFACE_SURVIVES_COMBINED_INTEGRATION_REBREAK`**

This verdict is bounded to the imported surface and must survive the persisted-HEAD re-break of the closure commit before P0.3 is considered durably closed.

## 10. Next governed action

**P0.4 — map the existing `src/research/` runtime producer surface against the integrated `ResearchRunEvidence` contract, formalize the minimal producer-junction boundary, then adversarially qualify that junction before importing or wiring any research runtime into the integration branch.**

P0.4 must remain fail-closed and must not trigger `.bi5` acquisition or real backtesting.
