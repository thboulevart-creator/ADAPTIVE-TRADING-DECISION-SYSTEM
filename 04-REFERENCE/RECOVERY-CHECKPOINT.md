# RECOVERY CHECKPOINT — 16 SEPTEMBRE 2026 — P0 FULL-SUITE REBASELINE PASS / BOUNDARYSTATE NEXT

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source of truth

GitHub code, persisted reports, tests and qualified workflow evidence are authoritative. Do not reconstruct state from conversation memory.

Construction rule remains:

**UNDERSTAND → COMPARE → BREAK → DECIDE.**

A prior PASS does not authorize the next gate automatically. `BLOCKED` is never `PASS`.

## Calendar Trading Breaks — closure evidence complete inside the candidate window

The executable post-closure state is now directly asserted by the current regression corpus.

### Global calendar

- candidates: `111`
- resolved: `91`
- unresolved: `20`
- special-session evidence dates: `88`
- no-special-change evidence dates: `3`
- FAIL: `0`
- global coverage verdict: **BLOCKED**

All `20` unresolved global candidates are before the candidate execution-window start.

### Candidate execution window `2021-08-14 → 2026-08-14`

- candidates: `68`
- resolved: `68`
- unresolved: `0`
- FAIL: `0`
- coverage verdict: **PASS**

This is a coverage fact only. The execution window is **not yet formally frozen**.

### Recovery / progression state

- attempt ledger: `73`
- registered material capability changes: `1`
- current positive capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- current fingerprint: `e1e0f9402df2da900f34a721a355210a802533823f8d2750a296a1a759e29f31`
- recovery queue: empty
- progression decisions: empty
- eligible recovery queue: empty

### Qualified negative-evidence dates integrated as `NO_SPECIAL_CHANGE_EVIDENCE`

1. `2021-12-31`
2. `2022-07-01`
3. `2026-07-02`

Each is bound to `TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1` and the factual verdict `NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`.

Calendar-closure evidence was previously closed by commit:

`ae875d767b12555b6b904d0bd8e8371d864364c7`

## P0.0 — Full-suite historical/current rebaseline CLOSED

Durable qualification report:

`reports/data-qualification/trading_breaks_p0_full_suite_rebaseline_qualification.md`

### Problem corrected

After calendar closure, `115` tests describing historical pre-integration states were still evaluated as current-state assertions, producing `115 failed / 537 passed`.

The correction does not delete, skip or weaken those tests.

### Historical regression contract

- schema: `HISTORICAL_REGRESSION_BASELINES_V1`
- historical node IDs: `115`
- historical files: `42`
- manifest: `tests/historical_regression_baselines.json`
- fail-closed replay hook: `tests/conftest.py`
- manifest commit: `e1f0b16b79297b9ab1b4d3c872a9452a897ad003`
- replay/current-truth integration commit: `5c9ab2c82d9793f8029d18f2a8cd395624e9a972`

Fail-closed properties:

- missing historical node ID → failure;
- malformed/unavailable baseline SHA → failure;
- failed historical file replay → failure;
- no `skip` / `xfail` / test deletion used to produce green;
- post-closure truth is asserted separately on current HEAD.

## Governance finalization — CLOSED

Finalizer parent:

`965c031020883d0c6517183b073dddf0e7c2e7dc`

Finalizer output commit:

`102835db477c92d161fb7a4004b287d28dd54010`

It changed exactly three files:

- `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
- `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md`
- `tests/test_governance_relaxation_cooling_off_contract.py`

The persisted governance contract is:

`GOVERNANCE_RELAXATION_COOLING_OFF_V1`

Key rule: permissive governance relaxation causally linked to an incident/loss/missed opportunity/constraint is subject to a minimum `30-day` cooling-off period; same-cause recurrence resets the period. The system may become more restrictive autonomously, but never more permissive autonomously.

### Temporary workflow cleanup

- P0 re-break restored read-only: `5a1dcd4b9030396ff46db6c1e660d0c20a342214`
- disposable finalizer removed: `77e02094de76a4c02c9face507c4875dec382b12`

The qualified cleaned HEAD is:

`77e02094de76a4c02c9face507c4875dec382b12`

## Authoritative P0.0 final executions

### Full Suite Regression

- run/job: `35120428859 / 104876523965`
- HEAD: `77e02094de76a4c02c9face507c4875dec382b12`
- result: **`659 passed in 17.65s`**
- conclusion: success
- worktree: clean
- permissions: `contents: read`, `metadata: read`

### Persisted-HEAD re-break

- run/job: `35120428855 / 104876523450`
- HEAD: `77e02094de76a4c02c9face507c4875dec382b12`
- exact persisted-HEAD checkout: PASS
- baseline manifest `115 / 42`: PASS
- result: **`659 passed in 14.47s`**
- conclusion: success
- worktree: clean
- permissions: `contents: read`, `metadata: read`

P0.0 verdict:

**PASS — `P0_FULL_SUITE_REBASELINE_PERSISTED_HEAD_REBREAK_CONFIRMS_CURRENT_AND_HISTORICAL_REGRESSION_CORPUS`**

## Explicit current prohibitions / non-verdicts

- `DECLARE_GLOBAL_COVERAGE_PASS`: **BLOCKED** (`111 / 91 / 20` globally)
- execution-window formally frozen: **NO**
- evidence-derived `BoundaryState` qualified: **NO**
- `.bi5` acquisition: **NOT AUTHORIZED**
- real backtest: **NOT AUTHORIZED**
- `src/research/ ↔ research_run_evidence` junction: **NOT QUALIFIED BY P0.0**
- inter-process attestation: **NOT QUALIFIED BY P0.0**

The fact that the candidate window is `68 / 68 / 0` does not itself satisfy `FREEZE_EXECUTION_WINDOW`.

## Mandatory recovery order before next substantive write

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-16-TRADING-BREAKS-P0-FULL-SUITE-REBASELINE-PASS.md`
4. `reports/data-qualification/trading_breaks_p0_full_suite_rebaseline_qualification.md`
5. `tests/historical_regression_baselines.json`
6. `tests/conftest.py`
7. `GOVERNANCE/GOVERNANCE-EVOLUTION-AND-AUDIT-PROTOCOL.md`
8. `GOVERNANCE/GOVERNANCE-AUDIT-REGISTER.md`
9. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
10. current calendar/coverage/recovery/progression tests and reports
11. compare active branch HEAD against the commit containing this checkpoint before any governed-state mutation.

## Exactly one next governed action

**P0.1 — derive `BoundaryState` exclusively from versioned evidence, adversarially break that derivation, correct and re-break if necessary, then and only then evaluate `FREEZE_EXECUTION_WINDOW`.**

Required attacks must include at minimum:

- moved or widened window without matching evidence;
- omitted in-window candidate;
- unresolved candidate hidden by derivation;
- external/global gaps incorrectly promoted into an in-window PASS or silently erased;
- stale coverage report accepted as current;
- self-declared boolean replacing evidence derivation;
- mismatch between calendar, coverage and recovery/progression state;
- provenance or evidence identity mismatch.

Do not freeze by declaration.  
Do not declare global coverage PASS.  
Do not acquire `.bi5`.  
Do not run a real backtest.
