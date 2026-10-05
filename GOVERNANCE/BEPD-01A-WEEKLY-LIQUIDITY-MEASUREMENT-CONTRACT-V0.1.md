# ATDS — BEPD-01A — WEEKLY LIQUIDITY MEASUREMENT CONTRACT V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Persistence parent HEAD:** `223703feaf070fb8165ca8dfe39a4b3e7464e374`  
**Persistence parent TREE:** `33ccab46c45a7565bf92ccb51efe64ab8ad12c25`  
**Status:** CANDIDATE_CANONICALLY_PERSISTED / CALIBRATION_SEMANTICS_FROZEN / HUMAN_ADOPTION_PENDING  
**Implementation authority:** NONE  
**Five-year historical execution authority:** NONE  
**Strategy / PnL / trading authority:** NONE

## 1. Purpose

Freeze a testable first semantic contract for the USTECH Weekly liquidity study before any five-year scan.

```text
USTECH
→ COMPLETED WEEKLY HIGH / LOW LEVELS
→ ACTIVE LEVEL LEDGER
→ H1-CLOSE LEVEL TAKE
→ H1-CLOSE REINTEGRATION
→ WEEKLY SWEEP CLUSTER
→ LEVEL-SPECIFIC WEEKLY-CLOSE DISPLACEMENT
```

This contract establishes no edge, strategy, probability claim or trading authority.

## 2. Bound data surface

```text
DATASET_IDENTITY =
USTECH_PROFILE_MINUTE_CORE_V0_1

AP0_MANIFEST_SHA256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce

PRICE_SURFACE =
mid

MID_IS_EXECUTION_PRICE =
false
```

Volume, order flow, market depth and execution-price realism remain out of scope.

## 3. Calibration Weekly boundary

For this V0.1 calibration fixture only:

```text
TIMEZONE =
Europe/Paris

WEEK_START =
Monday 00:00 local inclusive

WEEK_END_SELECTION_WINDOW =
Saturday 00:00 local exclusive

WEEKLY_CLOSE =
last observed AP0 mid_close within the window
```

Calibration window:

```text
2026-01-12T00:00:00+01:00
→
2026-02-21T00:00:00+01:00 exclusive
```

This is not yet a five-year DST/session policy. Five-year execution remains blocked until DST, holiday and gap semantics are separately frozen.

## 4. Weekly level creation

Once a Weekly window is complete it creates exactly:

```text
WEEKLY_HIGH_LEVEL
WEEKLY_LOW_LEVEL
```

Each level binds source week, side, price, causal availability, age in weeks and state.

A level cannot be used prospectively before its source Weekly is complete.

## 5. Active-level lifecycle

Initial state:

```text
ACTIVE
```

A HIGH level is taken at the first H1 satisfying:

```text
H1_CLOSE > ACTIVE_WEEKLY_HIGH
```

A LOW level is taken at the first H1 satisfying:

```text
H1_CLOSE < ACTIVE_WEEKLY_LOW
```

Equality is not a take.

At that first qualifying H1 close:

```text
ACTIVE → CONSUMED
```

Consumption is permanent. A consumed level never becomes active again.

```text
WICK TOUCH != LEVEL TAKE
LEVEL TAKE != REINTEGRATION
```

## 6. H1 semantics

H1 bars are derived from AP0 mid-minute data in `Europe/Paris`, aligned to local wall-clock hours.

The H1 close is the last observed AP0 `mid_close` in that H1 bucket.

For this calibration fixture, only observed H1 closes are used. General incomplete-hour/gap admissibility is not promoted by this contract.

## 7. Reintegration

For a consumed HIGH, reintegration is the first strictly later H1 with:

```text
H1_CLOSE < CONSUMED_HIGH_LEVEL
```

For a consumed LOW:

```text
H1_CLOSE > CONSUMED_LOW_LEVEL
```

Reintegration is recorded separately and does not reactivate the level.

No same-week reintegration is a valid observed outcome and may not be deleted.

## 8. Weekly sweep cluster

Every valid level consumed within the same target Weekly belongs to the same `SWEEP_CLUSTER_ID`.

```text
MULTIPLE LEVELS SWEPT IN ONE WEEK
!=
MULTIPLE INDEPENDENT WEEKS
```

Each level retains its own source week, age, price, take time, reintegration time and close displacement.

## 9. Multiple active levels

No result-dependent choice is permitted among:

```text
PREVIOUS-WEEK LEVEL
OLDER ACTIVE LEVEL
MOST-RECENT SWEPT LEVEL
OUTERMOST SWEPT LEVEL
```

If one Weekly consumes two valid active levels, both remain in the same cluster.

Derived labels such as `MOST_RECENT`, `OUTERMOST`, `AGE_IN_WEEKS` and `LEVELS_SWEPT_IN_CLUSTER` may be stored, but this contract does not promote one as the correct trading reference.

## 10. Level-specific outcome

Consumed HIGH:

```text
D = LEVEL_PRICE - TARGET_WEEKLY_CLOSE
```

Consumed LOW:

```text
D = TARGET_WEEKLY_CLOSE - LEVEL_PRICE
```

Interpretation:

```text
D > 0 = Weekly close in rejection direction
D = 0 = Weekly close exactly at level
D < 0 = Weekly close remains beyond the consumed level
```

Negative D remains evidence.

## 11. Failure-preserving rule

The empirical ledger must retain:

```text
TAKE + REINTEGRATION + POSITIVE D
TAKE + REINTEGRATION + NEGATIVE D
TAKE + NO SAME-WEEK REINTEGRATION
```

Selecting only sweeps that "worked" is allowed for visual explanation only, never for empirical estimation.

## 12. Frozen calibration fixture

Path:

`GOVERNANCE/BEPD-01A-WEEKLY-LIQUIDITY-CALIBRATION-FIXTURE-V0.1.json`

Git blob:

`89f2af87171002e75fa06d7fb704817e149968bc`

Canonical-text SHA-256:

`0365e0dfb1c5e3f78f4a3f01aca1f3bc91dc13147900c63831e4a51c1644434e`

The fixture binds six Weekly bars and expected stateful clusters for 2026-01-12 through 2026-02-20.

Seed limitation:

```text
Only levels created by fixture week 2026-01-12 are seeded.
No claim is made that pre-window active levels are exhaustively represented.
```

## 13. Mandatory breaker expectations

A future implementation must fail qualification if it:

1. uses a wick-only touch as a level take;
2. uses non-strict crossing where strict beyond is required;
3. consumes a level before its source Weekly is complete;
4. reactivates a consumed level;
5. counts the same consumed level again later;
6. deletes a negative D event;
7. deletes a take without same-week reintegration;
8. keeps only the most profitable level from a multi-level cluster;
9. treats several levels in one cluster as independent weeks;
10. expires an older active level merely because one week passed;
11. substitutes Pepperstone values for AP0 values inside the AP0 fixture;
12. treats AP0 mid as execution price;
13. claims the six-week fixture proves a probability;
14. expands directly to five years without separate authority.

## 14. TradingView visual calibration

Pepperstone TradingView values supplied by the human are diagnostic cross-feed anchors, not canonical AP0 values.

```text
2026-01-12 HIGH
TradingView = 25875.8
AP0 mid     = 25880.369
delta       = +4.569

2026-01-12 LOW
TradingView = 25253.8
AP0 mid     = 25262.8315
delta       = +9.0315

2026-01-19 HIGH
TradingView = 25705.7
AP0 mid     = 25709.83
delta       = +4.13

2026-01-19 LOW
TradingView = 24880.9
AP0 mid     = 24883.833
delta       = +2.933
```

Cross-feed agreement is diagnostic only. The AP0 research surface remains internally self-consistent.

## 15. Authority and stop boundary

```text
SEMANTIC CONTRACT CANDIDATE =
PERSISTENCE AUTHORIZED

SIX-WEEK CALIBRATION REPLAY =
AUTHORIZED / OBSERVED

HUMAN ADOPTION OF THIS EXACT CONTRACT =
PENDING

GENERAL IMPLEMENTATION =
NOT AUTHORIZED

FIVE-YEAR HISTORICAL EXECUTION =
NOT AUTHORIZED

OCCURRENCE / RESPONSE PROBABILITY CLAIMS =
NOT AUTHORIZED

STRATEGY / BACKTEST / PNL =
NOT AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT AUTHORIZED
```

STOP after candidate persistence and calibration replay evidence.
