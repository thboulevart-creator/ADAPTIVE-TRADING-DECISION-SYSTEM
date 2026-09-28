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
