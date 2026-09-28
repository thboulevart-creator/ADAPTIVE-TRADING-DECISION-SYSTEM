# E1-06 — ADVERSARIAL RUNNER QUALIFICATION + INDEPENDENT REFERENCE PARITY

Date: 2026-09-28

Base HEAD:
`b2edbb83c71699a502827b64d9486ec4467d1d8e`

Base TREE:
`a8be442caf92340dac7f3af3c13bb0c21f8738b3`

## 1. Accelerated governed authority

E1-06 is authorized as one complete accelerated governed control cycle.

Synthetic/reference PnL is authorized only for parity qualification.

Real E1 backtest, real-data performance use, profitability interpretation, E1-07, E1-08, MT5, paper, broker, live and capital remain closed.

## 2. Frozen preregistration

Contract:
`GOVERNANCE/E1-06-ADVERSARIAL-RUNNER-REFERENCE-PARITY-CONTRACT-V0.1.json`

Breaker:
`breakers/e1_06_adversarial_reference_parity_red_breaker.py`

Independent reference:
`tools/e1_06_independent_reference.py`

Future qualifier target:
`tools/e1_06_adversarial_parity.py`

Tests:
`Q6-01 → Q6-22`

Adversarial families:
look-ahead; same-bar execution; incorrect t+1; BID/ASK inversion; reversal accounting; gap crossing; warmup leakage; OOS leakage; double count; missing execution price; cost omission; nondeterminism.

Parity dimensions include signal direction/timestamps, execution timestamps/sides/prices, position transitions, closed-trade count, realized PnL components and aggregate realized PnL.

## 3. Reference independence

The reference is a separate implementation and is forbidden from importing or delegating to E1-04 or E1-05.

Its PnL scope is realized unit PnL only, spread intrinsic via raw BID/ASK, with commission/slippage/financing excluded but not assumed zero.

## 4. Expected test-first state

Before qualifier implementation:

```text
E1_06_TARGET = ABSENT
Q6_01_TO_Q6_22 = EXPECTED_RED
EXPECTED_REASON = E1_06_TARGET_ABSENT_EXPECTED_RED
```

No real-data execution or strategy-performance result is authorized.

## 5. Observed test-first RED

Persisted HEAD under test:

`79b98fe6fea3c6bf0015c049850b0d0654d0cd4f`

Persisted TREE under test:

`9a002b870dd682f8b8e7ebd499e51eab41c93144`

Protected E1-06 preregistration identities:

```text
contract =
483552f2ea1def15f94a28f2e45b97dd65f786ff

breaker =
dc4858559a2fda113c7290ad39a45d5291580773

independent reference =
25b01e6d31709f02f9c095262bfe78366e83003b
```

Protected qualified runtime identities used by the fixture:

```text
E1-05 runtime =
baad3bd7c2e810451737c89bf8f9bcabc17c5ba6

E1-04 runtime =
15e72b8743e7726fc8b8bedd933cf7defe56413b
```

Exact local materialization was verified against the Git blob identities above before execution.

Observed breaker result:

```text
PY_COMPILE = PASS

Q6-01 → Q6-22
TOTAL = 22
PASS = 1
FAIL = 21

PASS =
Q6-20 — independent reference has no E1-04/E1-05 import or delegation

ALL 21 FAILURES =
E1_06_TARGET_ABSENT_EXPECTED_RED
```

Interpretation:

Q6-20 is a static independence control over the already-persisted reference and does not require the absent qualifier target.

Every test that requires the E1-06 qualifier target failed for the single preregistered reason:

`E1_06_TARGET_ABSENT_EXPECTED_RED`

Adjudication:

```text
E1_06_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_06_REFERENCE_INDEPENDENCE_PRECHECK = PASS
E1_06_TARGET = ABSENT
E1_06_IMPLEMENTATION = NOT_YET
```

This RED does not establish parity qualification. It establishes the frozen test surface before qualifier implementation.

## 6. Final exact persisted-head qualification

Qualified persisted HEAD:

`992a2c9b62ca825481efad36ea5f5d511269500f`

Qualified persisted TREE:

`61a5e1a7b8575bbe52f70116a6456180abe45b8a`

Exact protected identities executed:

```text
E1-06 contract =
483552f2ea1def15f94a28f2e45b97dd65f786ff

E1-06 breaker =
dc4858559a2fda113c7290ad39a45d5291580773

E1-06 qualifier =
0793adc08416563125f57a55c0d272d24bb4b3df

E1-06 independent reference =
25b01e6d31709f02f9c095262bfe78366e83003b

E1-05 runner =
baad3bd7c2e810451737c89bf8f9bcabc17c5ba6

E1-04 execution runtime =
15e72b8743e7726fc8b8bedd933cf7defe56413b
```

Before execution, every materialized file listed above was verified with `git hash-object` and matched the persisted GitHub blob identity exactly.

Observed compile result:

```text
PY_COMPILE = PASS
```

Observed exact breaker replay:

```text
Q6-01 → Q6-22
TOTAL = 22
PASS = 22
FAIL = 0
```

The passing qualification includes:

- full runner/reference signal parity;
- exact signal timestamps;
- exact execution timestamps;
- exact BID/ASK sides and prices;
- exact position transitions including reversal;
- exact closed-trade count;
- exact realized PnL components;
- exact aggregate realized PnL;
- intrinsic spread handling;
- no look-ahead;
- no same-bar execution;
- exact first admissible post-H1 tick selection;
- forbidden gap-boundary protection;
- warmup isolation across continuity blocks;
- no artificial OOS warmup reset;
- reversal close counted once;
- no fabricated PnL when execution price is absent;
- deterministic replay;
- exact E1-04 cost-scope parity;
- independent-reference static independence;
- tampered aggregate detection;
- forbidden profitability/live claims absent.

Baseline synthetic realized PnL parity fixture:

```text
runner components = [3.0, 4.0]
reference components = [3.0, 4.0]

runner aggregate = 7.0
reference aggregate = 7.0
```

This PnL is synthetic qualification evidence only.

It is not a strategy-performance result.

## 7. E1-06 adjudication

```text
E1_06_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_06_REFERENCE_INDEPENDENCE_PRECHECK = PASS
E1_06_EXACT_PERSISTED_HEAD_REBREAK = PASS_22_OF_22
E1_06_SYNTHETIC_REFERENCE_PARITY = PASS
E1_06 = PASS
```

No real E1 backtest was executed.

No real E1-03 dataset was used to compute performance.

No claim of strategy profitability, broker-net PnL, all-in profitability or live profitability is authorized.

E1-07 and E1-08 remain closed.

## 8. End-of-control STOP

Accelerated-governed E1-06 control cycle is complete.

```text
E1-06 = PASS
CONTROL_CYCLE = CLOSED
NEXT_E1_CONTROL = NOT_OPENED
```

