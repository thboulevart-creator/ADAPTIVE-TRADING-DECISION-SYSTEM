# E1-08A — ONE-SHOT REAL E1 — SYNTHETIC QUALIFICATION

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Qualified persisted HEAD:

`ef4de80cc8a09df1599331f99a6d81651f461666`

Qualified persisted TREE:

`1764f531c2c6f77b9a87433f182842a65517d17f`

GitHub Actions qualification run:

`36482003414`

GitHub Actions job:

`109129659217`

## 1. Scope

This artifact closes:

```text
E1-08A
—
PREREGISTRATION
+ FROZEN BREAKER
+ MINIMAL ONE-SHOT EXECUTOR
+ SYNTHETIC QUALIFICATION
```

It does **not** authorize or execute E1-08B.

It does not compute real Source-B Momentum performance and does not expose the frozen OOS to a strategy-performance result.

## 2. Frozen preregistration identities

```text
E1-08A contract =
4d868b34c42fe6765ece8007a0bf173d22199ab1

E1-08A breaker =
20297ca64c12bf9cd1eb9f6bef73598692959342
```

The contract and breaker remained byte-identical from preregistration through qualification.

## 3. Test-first RED

Persisted RED HEAD:

`7aafbfc52900961912b0059784e391e8edfed72e`

Persisted RED TREE:

`137ee12fdb8f80ca242091451625ca8ae5aada30`

Observed exact persisted-byte RED:

```text
Q8-01 → Q8-20

TOTAL = 20
PASS = 0
FAIL = 20

UNIQUE FAILURE =
E1_08_TARGET_ABSENT_EXPECTED_RED
```

Adjudication:

`E1_08A_TEST_FIRST_RED = PASS_EXPECTED_FAILURE`

## 4. Minimal executor candidate

Runtime:

`tools/e1_08_one_shot_real_e1.py`

Runtime blob:

`a4a04a7f63546e09d43f8c043d41872ec973a900`

The candidate is limited to:

- deterministic canonical hashing;
- raw Source-B tick adaptation;
- source-file and source-manifest identity verification;
- H1 JSONL + canonical stream identity verification;
- OOS exposure declaration and verification;
- one-shot authority verification and exclusive consumption;
- PRE_OOS / OOS / CROSS_BOUNDARY trade attribution;
- closed-trade ledger;
- frozen realized-unit-PnL metrics;
- no forced liquidation of an open final position;
- synthetic delegation to the already-qualified E1-05 runner and E1-04 execution runtime;
- E1-07 result-envelope construction.

It adds no optimizer, no regime filter, no MT5/broker/live/capital path and no automatic rerun path.

## 5. Raw-tick adapter semantics

The adapter preserves source order and maps:

```text
timestamp  → timestamp_ms
bid_price  → bid
ask_price  → ask
```

Continuity mapping:

```text
first tick = OK

delta <= 60,000 ms
= OK

delta > 60,000 ms
= FORBIDDEN_BOUNDARY
```

Non-increasing timestamps fail closed.

No sorting, deduplication, interpolation, forward filling or repair is performed.

## 6. OOS exposure semantics

Before a future real run, the executor requires an exposure declaration bound to:

```text
experiment =
ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0

hypothesis family =
MOMENTUM_V1

dataset =
SOURCE_B_USTECH_PRICE_CORE_V0_1

OOS =
2025-05-25T00:00:00Z
→
2026-05-24T23:59:59.963Z
```

`NONE_DECLARED` is the only prior-exposure value that yields `oos_clean=true`.

A prior performance exposure does not block the record itself; it prevents the result from being represented as untouched clean OOS.

## 7. One-shot authority semantics

The frozen authority schema requires:

```text
max_runs = 1
real_e1_run_authorized = true
exact experiment binding
exact repository/branch binding
exact executor blob binding
exact protected dependency bindings
exact source manifest identity
exact H1 identity
exact OOS window
unique run_id
human decision reference
canonical digest
```

The authorization-consumption marker uses exclusive creation.

A second consumption attempt returns BLOCKED.

E1-08A itself contains no valid E1-08B authority artifact and therefore grants no real-run permission.

## 8. Result semantics

Trade partitions are frozen as:

```text
PRE_OOS:
entry < OOS_START and exit < OOS_START

OOS:
entry >= OOS_START

CROSS_BOUNDARY:
entry < OOS_START and exit >= OOS_START
```

A final open position remains:

`OPEN_UNREALIZED`

It is not forcibly liquidated to manufacture realized PnL.

The maximum-drawdown metric is explicitly:

`realized_closed_trade_max_drawdown`

It is not represented as intratrade, broker-equity or capital drawdown.

## 9. Exact persisted-head qualification

Dedicated read-only workflow:

`.github/workflows/e1-08a-synthetic-qualification.yml`

Qualified workflow blob:

`52dd15df4f46f7477028344c03443361f2201369`

Environment:

```text
ubuntu-24.04
CPython 3.12.14
PYTHONHASHSEED = 0
TZ = UTC
locked qualification requirements
```

The workflow checked out the exact persisted HEAD and dynamically bound the E1-07 frozen breaker to:

- current persisted HEAD;
- current persisted TREE;
- exact E1-07 runtime blob.

Observed E1-08A frozen breaker:

```text
Q8-01 → Q8-20

20 passed in 0.09s
```

Observed complete protected executable E1 chain:

```text
E1-03 breaker
E1-04 breaker
E1-05 breaker
E1-06 breaker
E1-07 breaker
E1-08A breaker

TOTAL = 148
PASS = 148
FAIL = 0

148 passed in 0.81s
```

Clean worktree:

`PASS`

## 10. Qualification-path diagnostics

Two earlier CI attempts were intentionally not treated as E1-08A qualification:

1. Legacy P0.4/P0.5/P0.6 workflows failed on historical workflow assertions before reaching current executable regression. Their failure did not demonstrate an E1-08A defect.
2. The first dedicated E1-08A workflow successfully passed Q8 20/20, but an attempted whole-repository regression failed during collection because the locked P0.6 qualification environment intentionally excludes NumPy while unrelated AP4/AP5/AP6/C01/CR1/CR2 tests require it.
3. A subsequent E1-chain replay passed E1-03/04/05/06/08 but E1-07 correctly refused to run without its explicit current HEAD/TREE/tool bindings.

The final workflow corrected only the qualification harness configuration. No frozen breaker and no E1-08A executor behavior was changed.

## 11. Protected dependency invariance

At qualified HEAD, exact checks confirmed the expected blobs remained unchanged for:

- E1-01/E1-02 freeze package;
- E1-03 runtime;
- E1-04 runtime;
- E1-05 runner;
- E1-06 independent reference;
- E1-06 qualifier;
- E1-07 runtime;
- E1-08A contract;
- E1-08A breaker;
- E1-08A executor;
- dedicated E1-08A qualification workflow.

No E1-01→E1-07 runtime, contract or frozen breaker was modified by the final E1-08A qualification correction.

## 12. Adjudication

```text
E1_08A_PREREGISTRATION = PASS
E1_08A_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_08A_MINIMAL_EXECUTOR = PRESENT
E1_08A_FROZEN_BREAKER = PASS_20_OF_20
E1_03_TO_E1_08A_EXECUTABLE_CHAIN = PASS_148_OF_148
E1_08A_SYNTHETIC_QUALIFICATION = PASS
E1_08A = PASS
```

Authority remains:

```text
E1_08B = NOT_OPENED
E1_08B = NOT_AUTHORIZED

REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_AUTHORIZED
AUTOMATIC_RERUN = NOT_AUTHORIZED

MT5 = CLOSED
PAPER = CLOSED
BROKER = CLOSED
LIVE = CLOSED
CAPITAL = CLOSED

PHASE_22_PLUS = CLOSED
```

## 13. Hard stop

E1-08A is complete.

```text
CONTROL_CYCLE = CLOSED
HARD_STOP = TRUE
```

The next candidate boundary is:

```text
E1-08B
—
EXPLICIT HUMAN ONE-SHOT REAL E1 RUN AUTHORIZATION
```

That boundary requires a separate explicit human decision.

No real E1 execution is authorized by this qualification artifact.
