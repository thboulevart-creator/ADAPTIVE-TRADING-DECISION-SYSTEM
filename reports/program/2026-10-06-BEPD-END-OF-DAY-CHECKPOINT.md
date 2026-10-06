# ATDS / BEPD — END-OF-DAY RECOVERY CHECKPOINT — 2026-10-06

## Scope

Canonical recovery checkpoint for today's BEPD Weekly Liquidity Sweeps work.
No scientific claim, OOS authority, strategy authority or trading authority is created by this checkpoint.

## Session start

```text
BEPD-08D =
QUALIFIED_FOR_HUMAN_ADJUDICATION

RESULT HUMAN_ADOPTED =
NO
```

First real dual descriptive result already exposed:

```text
TOTAL N = 472
INTERNAL N = 207
EXTERNAL N = 265
EXACT_LEVEL N = 0
OVERLAPPING MEMBERSHIP = 0
UNCLASSIFIED EVENTS = 0

D_CLOSE = abs(close_displacement)
D_INTERNAL = D_CLOSE | close_displacement > 0
D_EXTERNAL = D_CLOSE | close_displacement < 0
```

Historical corpus already exposed. Comparative, threshold, OOS, TP/SL and trading frontiers were closed.

## BEPD-08D closure completed today

```text
BEPD-08D =
QUALIFIED / HUMAN_ADOPTED / CLOSED

FINAL HUMAN ADJUDICATION BLOB =
227ee01f330fc5c10ad29422cab69ac8a6461de4

CLOSURE HEAD =
5f137f800e6c21791bf6ea57416085afb7e6fc0c

CLOSURE TREE =
51b7cb33086a0a1b0738d95ba5ab44abfd59ea57

EVIDENCE STATUS =
EXPOSED_EXPLORATORY_ONLY

GENERALIZATION =
NOT_ESTABLISHED

TRADING AUTHORITY =
NONE
```

No INTERNAL-vs-EXTERNAL comparative claim was created.

## BEPD-09A opened as design-only frontier

`BEPD-09A — EX-ANTE DECISION-TIME INFORMATION + CANDIDATE CLAIM SELECTION GATE V0.1`

Purpose: define what information is truly available at decision time before any future predictive claim is selected.

No real EVENT_LEDGER row was read.

### Design identities

```text
DESIGN PACKAGE HEAD =
374ab2c04401eecb2b8f3319022df924ca889a8e

DESIGN PACKAGE TREE =
df4937f4934edec87a34449b27454d07453b44fb

HUMAN AUTHORIZATION =
7324ceafdc66c9fa9e21d2f6d8e455ab85c07e14

DESIGN CONTRACT =
a3a3dd9fae1548de2b5ee6bf76536e68820ba932

DOCUMENTARY BREAKER =
d5cc742bb4cd256dde6f9a9988caece3a687b54e

DESIGN REPORT =
a5dead3f42e2ce0521a168bfa9905f9a0a83c18d
```

### Decision-time boundary frozen

```text
T0 =
take_h1_close_utc

INFORMATION AVAILABLE <= T0
=
POTENTIALLY PREDICTOR-ELIGIBLE

INFORMATION AVAILABLE > T0
=
FORBIDDEN AS EX-ANTE PREDICTOR

FIELD PRESENT IN HISTORICAL LEDGER
!=
FIELD AVAILABLE EX-ANTE
```

### T0-eligible candidate surface

```text
source_week_id
target_week_id AS CALENDAR CONTEXT ONLY
side
level_price_mid
level_age_weeks
active_level_count_at_target_week_start
take_h1_bucket_start_utc
take_h1_close_utc
take_h1_close_mid
```

Eligibility does not imply predictive usefulness.

### Explicitly forbidden as predictors

```text
cluster_consumed_level_count
reintegration_h1_*
same_week_reintegration
target_week_close_mid
close_displacement
CLOSE_SIDE
D_CLOSE
D_INTERNAL
D_EXTERNAL
target-week terminal gap diagnostics
```

`holiday_tag` remains ineligible until a separately bound ex-ante calendar source exists.

Derived features require all inputs available <= T0 and a formula frozen before response/outcome read.

### Dependence boundary

```text
EVENT IS IID =
FALSE

DEPENDENCE KEYS =
target_week_id
sweep_cluster_id
```

### Candidate claims ranked, none selected

```text
C1 — RANK 1 / PREFERRED
T0 CONTEXT → SAME-WEEK REINTEGRATION

C2 — RANK 2
T0 CONTEXT → TARGET-WEEK CLOSE_SIDE

C3 — RANK 3
T0 CONTEXT → D_CLOSE

C4 — RANK 4 / DEFER
T0 CONTEXT → TIME-TO-FIRST-REINTEGRATION / SURVIVAL
```

C1 caveat:

```text
REMAINING OBSERVATION TIME
FROM T0 TO TARGET-WEEK END
VARIES ACROSS EVENTS
```

Any future C1 design must explicitly represent or otherwise control this unequal exposure time.

## BEPD-09A qualification completed today

```text
QUALIFICATION HEAD =
d65c48e4c6bd727567f800146684b3901543ff08

QUALIFICATION TREE =
72dbcb9e02fe844ed417689f1ff5f1ab2810c444

QUALIFICATION RECEIPT =
cff9cdc47e59be1e6c77a05bbcd3661bba99a810

QUALIFICATION REPORT =
59609d27a6c1943dfef71cd1631a236c364e9c15

PERSISTED-HEAD VERIFICATION RECEIPT =
823b9d0557d73b13e33af1d807c057f192a69782

PROGRAMMATIC CHECKS =
33 / 33 PASS

DOCUMENTARY HARD-FAIL CASES =
28 / 28 PRESENT

REAL EVENT_LEDGER ROWS READ =
NO

REAL RESULT RECOMPUTATION =
NO

STATISTICAL TEST =
NO

MODEL FIT =
NO

OOS READ =
NO
```

## BEPD-09A closure completed today

```text
BEPD-09A =
QUALIFIED / HUMAN_ADOPTED / CLOSED

FINAL ADJUDICATION BLOB =
5ed041e76e72ec1f334379945396c44ec00e4e7a

FINAL CLOSURE HEAD =
247b74977c5e6b1d907865ea501d900c7c8cc0b7

FINAL CLOSURE TREE =
d545bc072c40029ddbf927bfd4d1f91dc7083a71
```

## Current terminal state

```text
FINAL CLAIM SELECTED =
NO

C1 SELECTED =
NO

C2 SELECTED =
NO

C3 SELECTED =
NO

C4 SELECTED =
NO

HISTORICAL CLAIM TESTING =
CLOSED

COMPARATIVE TESTING =
CLOSED

THRESHOLD SEARCH =
CLOSED

MODEL TRAINING =
CLOSED

OOS CONSUMPTION =
CLOSED

TP / SL =
CLOSED

BACKTEST / PNL / PAPER / BROKER / LIVE =
CLOSED

TRADING AUTHORITY =
NONE
```

## Exact resume frontier

Next human decision only:

```text
SELECT OR REJECT C1 AS THE NEXT CLAIM TO PREREGISTER

C1 =
T0-AVAILABLE CONTEXT
→
SAME-WEEK REINTEGRATION
```

If C1 is selected later, the next phase must be pre-result design only and must freeze:
- exact C1 estimand;
- exact T0-available predictor surface or claim-scoped subset;
- treatment of unequal remaining observation time to target-week end;
- target_week_id / sweep_cluster_id dependence;
- method eligibility without implicit IID;
- anti-leakage / no post-outcome feature selection;
- exploratory historical vs future confirmatory OOS boundary.

Until separate human authorization:

```text
STOP
```
