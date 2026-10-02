# SFE-02A — BREAKOUT_V1 — MINIMAL IMPLEMENTATION QUALIFICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Qualification boundary

This qualification is restricted to the adopted BREAKOUT_V1 **synthetic signal kernel**.

It does not use or authorize:

```text
REAL MARKET DATA
BEHAVIORAL Y
PERFORMANCE OBSERVATION
PNL
BACKTEST
EXECUTION
POSITION STATE
RANKING
ROUTER
REGIME FILTER
SFE-02B
E1-TD / TD03B
MT5 / PAPER / BROKER / LIVE / CAPITAL
```

A PASS here means only:

> no failure was found within the preregistered synthetic implementation surface actually executed.

## 2. Persisted identities under qualification

Candidate HEAD:

```text
HEAD =
d342bf6414efd30547984b0acbf73a624b74dd71

TREE =
622eb512fb4aa92862c60e9b7141d9c231b6908f
```

Contract:

```text
GOVERNANCE/SFE-02A-BREAKOUT-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json

BLOB =
0b99adfd76f2756e1d58319093fded50d751cf32
```

Frozen breaker:

```text
breakers/sfe_02a_breakout_v1_red_breaker.py

BLOB =
c2189c8b28f62ccffda58b02ff537dd53ba343f9
```

Runtime:

```text
tools/sfe_02a_breakout_v1.py

BLOB =
60f32b2d054390c2b5dbb975b015d7e09a5a1a96
```

Prior RED evidence:

```text
reports/program/2026-10-02-SFE-02A-BREAKOUT-V1-TEST-FIRST-RED.md

BLOB =
18c7f04c52f88c36dd9001d44641194521178c19
```

Adopted SFE-01 authority:

```text
GOVERNANCE/SFE-01-V0.2-HUMAN-ADJUDICATION-2026-10-02.md

BLOB =
66aa556e4e161e49550451062273bc8d6422593c
```

## 3. Test-first evidence

The frozen surface existed and failed before implementation:

```text
RED =
36 FAIL / 0 PASS

UNIQUE CAUSE =
SFE_02A_RUNTIME_ABSENT_EXPECTED_RED
```

The runtime did not exist at the RED checkpoint.

## 4. Minimal implementation result

Execution environment:

```text
Python =
3.14.7

pytest =
8.4.2
```

Compile:

```text
RUNTIME_PY_COMPILE = PASS
BREAKER_PY_COMPILE = PASS
```

Frozen breaker replay:

```text
B2A-01 → B2A-36

TOTAL = 36
PASS = 36
FAIL = 0
```

The passing surface includes:

- strict previous-20 channel semantics;
- current bar exclusion;
- strict upper/lower breach;
- tie neutrality;
- exact warmup and continuity reset;
- deterministic replay;
- fail-closed validation and validation precedence;
- binary64 close semantics;
- no cross-block lookback;
- no performance/execution/position output;
- Breakout → same-direction 20-bar Momentum implication;
- exact lookback trace binding;
- independent synthetic reference parity.

## 5. Adversarial mutation sweep

Eight deliberate implementation defects were injected one at a time into temporary, non-persisted runtime copies:

```text
M01_LOOKBACK_19
M02_UPPER_TIE_LONG
M03_LOWER_TIE_SHORT
M04_INCLUDE_CURRENT_IN_CHANNEL
M05_DROP_OLDEST_LOOKBACK_BAR
M06_DISABLE_H1_STEP_GUARD
M07_ALLOW_NONPOSITIVE_CLOSE
M08_INVERT_LONG_SIGNAL
```

Observed:

```text
MUTATIONS_TOTAL = 8
MUTATIONS_KILLED = 8
MUTATIONS_SURVIVED = 0

MUTATION_SWEEP = PASS
```

No mutated runtime was persisted.

## 6. Repository-wide regression attempt

A broader repository-wide pytest run was attempted as an additional, non-preregistered regression check.

It did **not** reach test execution because collection encountered an existing environment dependency:

```text
tests/test_ap4_price_structure.py
→ import numpy as np
→ ModuleNotFoundError: No module named 'numpy'
```

The available ATDS pytest environment contains:

```text
pytest = 8.4.2
numpy = ABSENT
```

No package was installed and no environment mutation was authorized or performed.

Therefore:

```text
REPOSITORY_WIDE_REGRESSION =
BLOCKED_ENVIRONMENT_MISSING_NUMPY

REPOSITORY_WIDE_REGRESSION_PASS =
NOT_CLAIMED
```

This environment blocker is not evidence of an SFE-02A runtime defect.

## 7. Qualification verdict

```text
SFE_02A_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

SFE_02A_FROZEN_BREAKER =
PASS_36_OF_36

SFE_02A_MUTATION_SWEEP =
PASS_8_OF_8_KILLED

SFE_02A_SYNTHETIC_SIGNAL_KERNEL =
QUALIFIED

SFE_02A_MINIMAL_IMPLEMENTATION =
PASS_WITHIN_DECLARED_SYNTHETIC_SURFACE

REPOSITORY_WIDE_REGRESSION =
BLOCKED_ENVIRONMENT_MISSING_NUMPY

REAL_DATA =
NONE

PERFORMANCE_OBSERVATION =
NONE

BEHAVIORAL_Y =
NONE

PNL =
NONE

BACKTEST =
NONE
```

## 8. Preserved scientific meaning

This qualification establishes only that the persisted runtime implements the adopted BREAKOUT_V1 signal definition on the preregistered synthetic adversarial surface.

It does **not** establish:

```text
BREAKOUT_V1_SUPPORTED
BREAKOUT_V1_REFUTED
BREAKOUT_V1_PROFITABLE
ECONOMIC_EDGE
ROBUSTNESS
SOURCE_INDEPENDENCE
PRODUCTION_READINESS
```

## 9. Next boundary

The approved sequence requires:

```text
SFE-02A QUALIFICATION
→ STOP
→ SFE-02B — MEAN_REVERSION_V1
```

However SFE-02B remains a separate control surface and no SFE-02B repository mutation is performed by this report.

No performance observation is permitted before both family implementations are qualified and both experiment contracts are frozen under the adopted SFE-01 contamination rules.

