# HISTORICAL TRADING BREAKS RECOVERY — BATCH 06 PERSISTED-HEAD REBREAK

**PASS — `BATCH06_PERSISTED_HEAD_INTEGRATION_STATE_REBROKEN_READ_ONLY`**

## Scope

Independent read-only verification of the already-persisted Batch 06 atomic integration before any Batch 07 membership freeze.

The authoritative atomic integration commit is:

`a2a59baefd7986f65efb4d625acd2c47c085ae31`

The re-break workflow commit is:

`3feb9f937bf74202f68642992ca3fe8b363398d9`

The only file changed between the atomic integration commit and the re-break trigger commit was:

`.github/workflows/trading-breaks-recovery-batch06-persisted-head.yml`

No executable calendar, attempt-ledger, progression, protocol or capability state changed before the re-break.

## Authoritative re-break

- workflow run: `34956317590`
- job: `104339111722`
- trigger commit: `3feb9f937bf74202f68642992ca3fe8b363398d9`
- workflow permissions: `contents: read`
- adversarial/regression suite: `206 passed in 0.83s`
- exact persisted-state assertion: PASS
- no-browser/no-capture dependency guard: PASS
- deterministic progression regeneration + `git diff --exit-code`: PASS

## Persisted state proven

- global calendar: `111 candidates / 46 resolved / 65 unresolved / 0 FAIL`
- execution-window candidate: `68 candidates / 23 resolved / 45 unresolved / 0 FAIL`
- attempt ledger: `30`
- attempt sequences: exact `1..30`
- unique attempt IDs: `30`
- registered material capability changes: `0`
- attempted BLOCKED / execution-ineligible: `7`
- execution-eligible unresolved: `38`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_V1`
- capability fingerprint: `82238de6e862e2b31e7a8f4e5faa3f822545ba46251703b06180087a957aaf8f`

## Batch 06 persisted attempt facts

Sequences `26..30` are exactly:

1. `2023-07-03 — PASS`
2. `2023-07-04 — BLOCKED`
3. `2023-09-04 — PASS`
4. `2023-11-23 — PASS`
5. `2023-11-24 — PASS`

The `2023-07-04` attempt retains blocking reason:

`NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

Its post-integration progression state is exactly:

`UNRESOLVED + INELIGIBLE — SAME_CAPABILITY_BLOCKED_ALREADY_ATTEMPTED`

It is absent from executable `SPECIAL_SESSION_EVIDENCE` and no `NO_SPECIAL_CHANGE_EVIDENCE` was created for it.

The other four Batch 06 PASS dates are present in executable special-session evidence and absent from the unresolved recovery queue.

## Progression boundary

The persisted eligible recovery queue is chronological and contains `38` candidates.

Its first current eligible candidate is:

`2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`

This observation is a persisted-state fact only. It **does not freeze Batch 07**.

## Failure/correction history during integration qualification

Two pre-persistence failures occurred and were fail-closed; neither wrote a partial calendar/ledger/progression mutation:

1. run `34955611637` / job `104336823027`: the integration preparer incorrectly expected one Batch 05 attempt-count assertion but found two legitimate assertions. The rewrite guard was minimally corrected.
2. run `34956027482` / job `104338171283`: the simulated mutation and `206` post-mutation tests passed, but a whole-file lexical browser guard falsely matched browser tokens contained only inside generated test source. The guard was minimally scoped to executable integration functions.

The corrected authoritative integration then passed on run `34956127849` / job `104338497611` and persisted exactly one atomic state commit.

## Workflow closure

The completed Batch 06 persisted-head workflow is archived to `workflow_dispatch` only at commit:

`6caa402c21a78faccb7ac3897c5b280f4dbdca6a`

The completed Batch 06 atomic integration workflow is archived to `workflow_dispatch` only at commit:

`da6cff32eae7c8c863753aaff0875aeb0fe42774`

No normal push may silently repeat historical Batch 06 integration or persisted-head re-break.

## Downstream boundary

Batch 06 integration + persisted-head re-break are closed PASS.

Still forbidden:

- massive native `.bi5` acquisition;
- execution-window freeze while unresolved dates remain;
- real backtest.

Batch 07 is **not frozen** by this report.
