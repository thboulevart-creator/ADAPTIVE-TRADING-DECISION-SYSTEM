# SESSION BACKUP — 14 SEPTEMBRE 2026 — TRADING BREAKS RECOVERY PROGRESSION PASS

## 1. Scope completed

This session completed exactly the governed action that followed Trading Breaks Recovery Batch 02:

**formalize and adversarially qualify an attempt-aware recovery progression contract before defining Batch 03.**

No Batch 03 membership was frozen or observed in this session.

No `.bi5` acquisition occurred.

No real backtest occurred.

## 2. Starting authoritative state

Starting branch:

`feat/multi-year-dukascopy-acquisition`

Starting verified HEAD:

`7b6ecac38819312b58661ccf20311474e0fa9a0a`

Starting calendar state:

- global: `111 candidates / 30 resolved / 81 unresolved / 0 FAIL`
- execution-window candidate: `68 candidates / 7 resolved / 61 unresolved / 0 FAIL`
- execution window: `2021-08-14 → 2026-08-14`
- execution window frozen: NO

Batch 02 had left three dates unresolved after BLOCKED outcomes:

- `2021-12-24 — CHRISTMAS_OBSERVED`
- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-04-15 — GOOD_FRIDAY`

The progression defect was that raw `recovery_queue()[:5]` would continue to reselect already-attempted BLOCKED dates and could starve later unresolved candidates.

## 3. Contract created

Reference:

`04-REFERENCE/HISTORICAL-TRADING-BREAKS-RECOVERY-PROGRESSION-CONTRACT.md`

Contract:

`HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION_V1`

Final verdict:

**PASS — `ATTEMPT_AWARE_RECOVERY_PROGRESSION_REJECTS_RETRY_BYPASSES_AND_PREVENTS_STARVATION`**

The contract separates:

1. calendar evidence state;
2. factual attempt history;
3. execution eligibility.

`BLOCKED` remains unresolved calendar state and never becomes negative evidence merely because it was attempted.

## 4. Attempt ledger created

Authoritative ledger:

`reports/data-qualification/historical_trading_breaks_recovery_attempt_ledger.json`

Schema:

`HISTORICAL_TRADING_BREAKS_RECOVERY_ATTEMPT_LEDGER_V1`

Current semantic capability:

`TRADING_BREAKS_PRIMARY_WIDGET_V1`

Current capability fingerprint:

`82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

The ledger preserves all **10** factual Batch 01 / Batch 02 attempts, including duplicate historical attempts of `2021-12-24` and `2021-12-31` under the same semantic capability.

Batch 02 reuses:

`tools.trading_breaks_recovery_batch01.probe_candidate`

Therefore different workflow runs, artifacts, or probe commits between Batch 01 and Batch 02 do not constitute different semantic capabilities.

## 5. Material capability-change registry created

Registry:

`reports/data-qualification/historical_trading_breaks_recovery_capability_changes.json`

Schema:

`HISTORICAL_TRADING_BREAKS_RECOVERY_CAPABILITY_CHANGE_REGISTRY_V1`

Current qualified changes:

`0`

A future retry of an already-BLOCKED date requires a versioned registry entry proving a material semantic capability change.

## 6. Executable progression boundary

Implementation:

`tools/trading_breaks_recovery_progression.py`

Adversarial tests:

`tests/test_trading_breaks_recovery_progression.py`

Production interfaces:

- `progression_decisions()`
- `eligible_recovery_queue()`

Both derive their production state from governed repository files and accept no caller-provided retry authorization, attempt history, current capability, expected outcome, manual priority, or manual skip input.

## 7. First adversarial run — nominal PASS but not accepted as final

First workflow run:

- run: `34890138036`
- job: `104130467209`
- trigger commit: `fe09849451c868a9abb624d9d1525539e0b49d25`
- result: SUCCESS
- suite: `67 passed`

The initial runtime state was coherent, but a second adversarial design review exposed two untested real bypasses.

### Bypass 1 — declarative proof-capability token

The first implementation could add a blocker-relevant `proof_capability` token without changing the actual evidence route/protocol/capture implementation and treat that as material capability change.

This allowed declarative metadata to masquerade as executable capability.

### Bypass 2 — caller-injected retry authorization

The first production API accepted caller-provided attempts/current capability/material changes.

A future caller could therefore inject unversioned scheduling/retry state rather than use repository-governed state.

The first nominal PASS was therefore deliberately not accepted as final.

## 8. Minimal corrections

The corrected material-change predicate now requires:

- exact old/new semantic fingerprints;
- declared changed dimensions exactly equal actual changes;
- at least one real executable semantic change among `route_contract`, `protocol_contract`, `capture_implementation`;
- at least one newly added blocker-relevant proof capability;
- no removal of previously qualified proof capabilities;
- explicit coverage of the prior blocking reason;
- versioned qualification contract;
- exact 40-hex qualification commit.

A proof-capability-token-only change fails with:

`NO_ROUTE_PROTOCOL_OR_RUNTIME_CHANGE`

Production progression now loads the versioned attempt ledger and material-change registry itself.

## 9. Final corrected adversarial re-break

Authoritative final run:

- run: `34890560172`
- job: `104131879994`
- trigger commit: `c020a5132d053011f517007b9562b5257bbf9aaf`
- conclusion: SUCCESS
- adversarial/regression suite: `72 passed in 0.51s`
- corrected runtime persistence commit: `b7dcd82f7b6cc7f90773f28a78ac4d300b9adaa2`

Runtime verdict:

**PASS — `ATTEMPT_AWARE_PROGRESSION_STATE_IS_DETERMINISTIC_AND_NON_STARVING`**

Runtime state:

- calendar unresolved: `61`
- attempt ledger entries: `10`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `3`
- execution-eligible unresolved: `58`

The three already-attempted BLOCKED dates remain unresolved and are explicitly execution-ineligible under the unchanged capability:

- `2021-12-24` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2021-12-31` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`
- `2022-04-15` → `SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

Later never-attempted unresolved dates remain eligible, proving non-starvation.

## 10. Qualification report and workflow state

Qualification report:

`reports/data-qualification/historical_trading_breaks_recovery_progression_qualification.md`

The qualification workflow is archived to `workflow_dispatch` only after final PASS:

`.github/workflows/trading-breaks-recovery-progression.yml`

## 11. Calendar state unchanged by progression qualification

The progression PASS changes scheduling eligibility only. It changes no calendar evidence.

Current accounting remains:

- global: `111 / 30 resolved / 81 unresolved / 0 FAIL`
- execution-window candidate: `68 / 7 resolved / 61 unresolved / 0 FAIL`

Window remains:

`2021-08-14 → 2026-08-14`

Window frozen: NO.

## 12. Current boundary matrix

PASS:

- `GLOBAL_CROSS_YEAR_ACCOUNTING_AUDIT`
- `WINDOW_SELECTION_RULE`
- `WINDOW_CANDIDATE_DEFINED`
- `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROTOCOL`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH01`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_BATCH02`
- `HISTORICAL_TRADING_BREAKS_RECOVERY_PROGRESSION`
- `LOCAL_RUNTIME_EVIDENCE_ARCHIVE`

BLOCKED:

- `DECLARE_GLOBAL_COVERAGE_PASS`
- `FREEZE_EXECUTION_WINDOW — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`
- `AUTHORIZE_MASSIVE_ACQUISITION — EXECUTION_WINDOW_NOT_FROZEN`
- `REAL_BACKTEST — UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`

## 13. Exactly one next governed action

**Freeze and version Batch 03 with `BATCH_SIZE = 5` as exactly the first five entries of the governed `eligible_recovery_queue()`, before any Batch 03 historical observation.**

Batch 03 membership MUST be derived mechanically from `eligible_recovery_queue()`.

It MUST NOT be derived from raw `recovery_queue()[:5]`.

No candidate may be inserted, skipped, substituted, or reordered because of expected outcome, holiday type, apparent ease, manual preference, or convenience.

This backup does not freeze Batch 03.

No `.bi5`. No real backtest.
