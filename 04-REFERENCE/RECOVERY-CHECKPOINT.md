# RECOVERY CHECKPOINT — 15 SEPTEMBRE 2026 — BATCH 14 INTEGRATED / CAPABILITY EXHAUSTED / CRITICAL PATH REEVALUATED

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `feat/multi-year-dukascopy-acquisition`

## Source-of-truth rule

GitHub code, executable tests, reports and qualified workflow evidence are authoritative. `Carte Architecturale Snapshots Claude/adts-carte-architecturale.md` remains a point-in-time diagnostic snapshot only.

The three immediate Claude priorities remain closed at their executable loci:

1. recovery/checkpoint drift: **FIXED**;
2. `RESEARCH → DECISION` provenance/forgeability: **FIXED AND INDEPENDENTLY RE-BROKEN** on `feat/decision-producer-contract`;
3. durable boundary CI branch-name coupling: **FIXED AND INDEPENDENTLY RE-BROKEN** on `feat/decision-producer-contract`.

## Batch 13

Batch 13 is **FULLY CLOSED**.

- integration commit: `52b1978feb0018c1eafc80108e4b411edf0ec982`
- persisted-HEAD verifier head: `bb8f6dbf7781accf7051c8e6bc9213757da1d6da`
- verifier run/job: `35023156320` / `104563657205`
- regression: `447 passed`
- byte-stable progression and clean worktree: PASS

## Batch 14 — terminal batch

Terminal membership was frozen before observation as the complete remaining eligible queue:

1. `2026-06-19 — JUNETEENTH_OBSERVED`
2. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
3. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Terminal freeze qualification:

- qualification head: `3c83e62a24ee6d638079edc0d79cd8bf843b6460`
- workflow run/job: `35023675791` / `104565373090`
- permissions: `contents: read`
- regression: `448 passed`
- exact complete eligible remainder: PASS
- omission/permutation/duplication/padding-with-BLOCKED attacks rejected
- no browser observation in freeze
- progression byte-stable

Independent persisted-membership re-break:

- verifier head: `6beb60438f0a1bdcfc38bbbb5c3b8b0ef146dd07`
- workflow run/job: `35023738920` / `104565583457`
- verdict: PASS
- verifier-only delta, exact membership, adversarial variants, byte-stability and clean worktree: PASS

Capture/adjudication provenance:

- workflow run/job: `35023845609` / `104565948108`
- probe commit: `4194108c6c9e2c0308209b31cfa64ba8fb3b9f2b`
- artifact: `10418961548`
- artifact SHA-256: `00dd2044a76d926417779d22c7ce08b67318a9d00933b9cac1bc980f2a7c9910`
- adjudication: **PASS — 2 PASS / 1 BLOCKED / 0 FAIL**

Individual verdicts:

- `2026-06-19` → PASS — broker record `101094`
- `2026-07-02` → BLOCKED — `NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`
- `2026-07-03` → PASS — broker record `101959`

Atomic integration:

- integration commit: `075b33b79c8de3b2f4f6201a7541c6555585a5e4`
- calendar: only the two PASS targets persisted
- ledger: all three attempts persisted as sequences `66..68`
- provenance preserved exactly

### Batch 14 closure status

**INTEGRATED — NOT YET FULLY CLOSED.**

An independent read-only persisted-HEAD re-break of the Batch 14 integration has not yet been completed. No later functional work may treat Batch 14 as fully closed until that proof passes.

## Deterministic progression after Batch 14 integration

- global calendar: `111 candidates / 74 resolved / 37 unresolved / 0 FAIL`
- execution-window candidate (`2021-08-14` → `2026-08-14`): `68 candidates / 51 resolved / 17 unresolved / 0 FAIL`
- recovery queue: `17`
- attempt ledger: `68`
- same-capability BLOCKED/ineligible: `17`
- eligible unresolved under `TRADING_BREAKS_PRIMARY_WIDGET_V1`: **0**
- material capability changes: `0`
- execution window frozen: **NO**
- `.bi5`: **FORBIDDEN**
- real backtest: **NOT AUTHORIZED**

The current capability is exhausted. A Batch 15 under the same capability is not a valid continuation path.

## Critical-path reevaluation

Decision record:

`reports/data-qualification/pre_backtest_critical_path_reevaluation_2026-09-15.md`

The 17 unresolved dates are not one homogeneous missing-data problem.

### Class A — 14 semantic-admissibility cases

Fourteen dates have a positive primary broker Trading Breaks record overlapping the addressed target day, but remain BLOCKED solely because the current adjudication requires `record.start.date() == target_date`.

The capture layer and `derive_fully_closed_hours_utc(target_date, start, reopen)` already support deriving target-day whole closed hours from a spanning broker-native interval. The exact-start-date condition is therefore an additional semantic constraint that must be independently justified or replaced, not blindly inherited.

Current blocking reason:

`NO_EXACT_TARGET_DATE_POSITIVE_RECORD_ADMISSIBLE`

### Class B — 3 genuine no-positive-record cases

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Current blocking reason:

`NO_POSITIVE_EXACT_BROKER_RECORD_RECOVERED`

These require a separate negative-evidence/completeness decision. Empty broker output remains BLOCKED unless completeness is independently proven.

## Governing decision

Rejected:

- repeating a Batch 15;
- searching for a new source for all 17 dates;
- bypassing calendar qualification and starting `.bi5` acquisition.

Selected path:

1. independently re-break the already-integrated Batch 14 HEAD in read-only mode;
2. if PASS, qualify offline/adversarially a target-day overlap semantic contract against existing Class-A evidence only;
3. if that contract passes, re-adjudicate the 14 Class-A dates without new browser observation and without rewriting historical attempts;
4. handle the remaining three Class-B dates through a separately qualified negative-evidence/completeness contract or a materially different primary source;
5. only when in-window unresolved = 0 and FAIL = 0, freeze the execution window, freeze OOS, authorize native tick acquisition, qualify the five-year dataset/cost model, then execute Momentum V1 baseline.

## Exactly one next governed action

**Perform an independent, read-only persisted-HEAD re-break of Batch 14 integration commit `075b33b79c8de3b2f4f6201a7541c6555585a5e4`. If and only if it passes, the next workstream is an offline adversarial qualification of target-day overlap semantics using already captured evidence — not Batch 15 and not a new browser capture.**

No new browser capture.  
No `.bi5`.  
No real backtest.
