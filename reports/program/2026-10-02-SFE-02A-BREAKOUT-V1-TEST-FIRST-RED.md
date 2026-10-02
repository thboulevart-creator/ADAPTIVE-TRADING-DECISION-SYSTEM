# SFE-02A — BREAKOUT_V1 — TEST-FIRST RED

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Authority and scope

Human authorization opened only:

```text
SFE-02A — BREAKOUT_V1
CONTRACT
→ TEST-FIRST RED
→ MINIMAL IMPLEMENTATION
→ ADVERSARIAL BREAK
→ SYNTHETIC QUALIFICATION
→ STOP
```

No real market data, `Y`, performance, PnL, backtest, execution, ranking, router, regime filter, SFE-02B, E1-TD, TD03B, MT5, paper, broker, live or capital authority is opened.

## 2. Persisted preregistration identity

Observed persisted HEAD before RED execution:

```text
HEAD =
fd35afb19f64439778e8ed7750e0dd7f41e75f30

TREE =
b1088b36077492e2e2123540c45004a980e8c624
```

Contract:

```text
GOVERNANCE/SFE-02A-BREAKOUT-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json

BLOB =
0b99adfd76f2756e1d58319093fded50d751cf32
```

Breaker:

```text
breakers/sfe_02a_breakout_v1_red_breaker.py

BLOB =
c2189c8b28f62ccffda58b02ff537dd53ba343f9
```

Runtime target:

```text
tools/sfe_02a_breakout_v1.py
```

Observed before RED:

```text
RUNTIME_EXISTS = FALSE
```

## 3. Frozen synthetic test surface

Exactly 36 cases are preregistered:

```text
B2A-01 → B2A-36
```

They cover:

- exact 20 completed H1 close lookback;
- current close excluded from the channel;
- strict upper/lower breach;
- ties neutral;
- warmup and first eligible ordinal 20;
- no cross-continuity history;
- future mutation cannot affect an already computed signal;
- deterministic replay;
- validation precedence and fail-closed input handling;
- strictly positive finite binary64 close semantics;
- strict H1 continuity inside a block;
- exact runtime constants and forbidden surfaces;
- no performance, `Y`, execution or position output;
- structural implication from Breakout directional signals to same-direction 20-bar Momentum sign;
- exact trace binding to the previous-20 window;
- independent synthetic reference parity.

## 4. Observed RED

Execution environment:

```text
Python = 3.14.7
pytest = 8.4.2
```

Breaker compile:

```text
PY_COMPILE = PASS
```

Observed pytest result:

```text
TOTAL = 36
PASS = 0
FAIL = 36
```

Every failure had exactly the same preregistered cause:

```text
SFE_02A_RUNTIME_ABSENT_EXPECTED_RED
```

No alternate failure family was observed.

## 5. RED adjudication

```text
SFE_02A_TEST_FIRST_SURFACE =
PERSISTED

SFE_02A_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

RUNTIME =
ABSENT

SIGNAL_IMPLEMENTATION =
NOT_YET_OBSERVED

PERFORMANCE_OBSERVATION =
NONE

REAL_MARKET_DATA =
NONE
```

The RED proves that the contract and breaker existed and failed before the runtime existed.

It does not establish correctness of any future runtime.

## 6. Next authorized boundary

The already-authorized next boundary is:

```text
SFE-02A — MINIMAL BREAKOUT_V1 IMPLEMENTATION CANDIDATE
```

The implementation may only satisfy the frozen synthetic contract and breaker.

No performance surface may be added.

