# SFE-02B — MEAN_REVERSION_V1 — TEST-FIRST RED

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Authority and scope

Human authorization opened only:

```text
SFE-02B — MEAN_REVERSION_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ NUMERICAL + ADVERSARIAL BREAK
→ SYNTHETIC QUALIFICATION
→ FINAL PERSISTED-STATE REBREAK
→ STOP
```

No real market data, behavioral `Y`, performance, PnL, backtest, execution, optimization, ranking, router, regime filter, E1/E1-TD/TD03B, MT5, paper, broker, live or capital authority is opened.

## 2. Persisted preregistration identity

Observed persisted HEAD before RED execution:

```text
HEAD =
8319fada3edea692d5c6e50889d447035e6c0ea6

TREE =
fa1d9ecee2bfbb9494c4fb3e9fff99f93413576a
```

Contract:

```text
GOVERNANCE/SFE-02B-MEAN-REVERSION-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json

BLOB =
ba4b98296c8d4f1e37793f3cb5f1dbdfb0fe7d9d
```

Breaker:

```text
breakers/sfe_02b_mean_reversion_v1_red_breaker.py

BLOB =
a3406991cb534f3590dbe02aafbb995f66b01d84
```

Runtime target:

```text
tools/sfe_02b_mean_reversion_v1.py
```

Observed before RED:

```text
RUNTIME_EXISTS = FALSE
```

## 3. Frozen numerical semantics

Before implementation, the contract froze:

```text
PRICE REPRESENTATION =
Python float / IEEE-754 binary64

MEAN =
math.fsum(x / 20.0 for x in window)

SIGMA =
scaled two-pass population standard deviation
with denominator 20

SQRT =
math.sqrt

ZERO SIGMA =
exact SIGMA == 0.0
→ UNDEFINED

HIDDEN EPSILON =
NONE

Z =
(current_close - MU) / SIGMA

LONG =
Z <= -1.0

SHORT =
Z >= +1.0

NEUTRAL =
-1.0 < Z < +1.0
```

## 4. Frozen synthetic test surface

Exactly 42 cases were preregistered:

```text
M2B-01 → M2B-42
```

The surface includes:

- exact H1/lookback-20 semantics;
- current-close exclusion;
- population rather than sample dispersion;
- exact threshold inclusivity;
- immediately-inside-threshold binary64 cases;
- exact sigma zero;
- near-zero but nonzero sigma with no hidden epsilon;
- large finite positive closes;
- continuity and warmup;
- deterministic replay;
- validation precedence and fail-closed handling;
- binary64 conversion overflow;
- independent `Decimal` reference parity on safe synthetic corpora;
- no mean/sigma/z/performance/execution/position output;
- steady-trend directional triggering as an explicitly allowed construct limitation.

## 5. Observed RED

Execution environment:

```text
Python = 3.14.7
pytest = 8.4.2
```

Breaker compile:

```text
PY_COMPILE = PASS
```

Observed pytest:

```text
TOTAL = 42
PASS = 0
FAIL = 42
```

Every failure had exactly one preregistered cause:

```text
SFE_02B_RUNTIME_ABSENT_EXPECTED_RED
```

No alternate failure family was observed.

## 6. RED adjudication

```text
SFE_02B_TEST_FIRST_SURFACE =
PERSISTED

SFE_02B_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

RUNTIME =
ABSENT

NUMERICAL_IMPLEMENTATION =
NOT_YET_OBSERVED

PERFORMANCE_OBSERVATION =
NONE

BREAKOUT_PERFORMANCE_OBSERVATION =
NONE

REAL_MARKET_DATA =
NONE
```

The RED proves the contract and breaker existed and failed before implementation.

## 7. Next authorized boundary

The already-authorized next boundary is:

```text
SFE-02B — MINIMAL MEAN_REVERSION_V1 IMPLEMENTATION CANDIDATE
```

Only the frozen synthetic signal/numerical surface may be implemented.

