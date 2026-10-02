# SFE-02B — MEAN_REVERSION_V1 — MINIMAL IMPLEMENTATION QUALIFICATION

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Qualification boundary

This qualification is restricted to the adopted MEAN_REVERSION_V1 **synthetic signal and numerical kernel**.

It does not use or authorize:

```text
REAL MARKET DATA
BEHAVIORAL Y
PERFORMANCE OBSERVATION
PNL
BACKTEST
EXECUTION
POSITION STATE
OPTIMIZATION
RANKING
ROUTER
REGIME FILTER
E1 / E1-TD / TD03B
MT5 / PAPER / BROKER / LIVE / CAPITAL
```

A PASS means only that no failure was found within the preregistered synthetic implementation surface actually executed.

## 2. Persisted identities under qualification

Candidate HEAD:

```text
HEAD =
5afe41cf725d43e6c39f9f474233f8e304b3d31d

TREE =
75b9658aea6d46a43d1035144bf5f4520381de9d
```

Contract:

```text
GOVERNANCE/SFE-02B-MEAN-REVERSION-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json

BLOB =
ba4b98296c8d4f1e37793f3cb5f1dbdfb0fe7d9d
```

Frozen breaker:

```text
breakers/sfe_02b_mean_reversion_v1_red_breaker.py

BLOB =
a3406991cb534f3590dbe02aafbb995f66b01d84
```

Runtime:

```text
tools/sfe_02b_mean_reversion_v1.py

BLOB =
273e184093e4cc98f0eb6569cd6f1007366cce40
```

Prior RED evidence:

```text
reports/program/2026-10-02-SFE-02B-MEAN-REVERSION-V1-TEST-FIRST-RED.md

BLOB =
84ad8a57eb76928f535cf945901aee5b4b84484b
```

Upstream SFE-01 adjudication:

```text
GOVERNANCE/SFE-01-V0.2-HUMAN-ADJUDICATION-2026-10-02.md

BLOB =
66aa556e4e161e49550451062273bc8d6422593c
```

SFE-02A closure remains:

```text
reports/program/2026-10-02-SFE-02A-BREAKOUT-V1-FINAL-PERSISTED-STATE-CLOSURE.md

BLOB =
b88d7468394913606b5931b1c3cc070631e19912
```

## 3. Test-first evidence

The frozen SFE-02B test surface existed and failed before the runtime existed:

```text
RED =
42 FAIL / 0 PASS

UNIQUE CAUSE =
SFE_02B_RUNTIME_ABSENT_EXPECTED_RED
```

Therefore the implementation did not precede the preregistered breaker.

## 4. Frozen numerical semantics actually qualified

```text
PRICE REPRESENTATION =
Python float / IEEE-754 binary64

LOOKBACK =
20 completed admissible H1 closes

CURRENT CLOSE IN REFERENCE =
EXCLUDED

MEAN =
math.fsum(x / 20.0 for x in window)

SIGMA =
scaled two-pass population standard deviation

POPULATION DENOMINATOR =
20

SQRT =
math.sqrt

SIGMA ZERO =
exact binary64 SIGMA == 0.0

SIGMA EPSILON =
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

The scaled population-sigma implementation is mathematically equivalent to the adopted population standard deviation definition while avoiding avoidable overflow in the sum of squared deviations.

## 5. Frozen breaker result

Execution environment:

```text
Python = 3.14.7
pytest = 8.4.2
```

Compile:

```text
RUNTIME_PY_COMPILE = PASS
BREAKER_PY_COMPILE = PASS
```

Frozen breaker replay:

```text
M2B-01 → M2B-42

TOTAL = 42
PASS = 42
FAIL = 0
```

The passing surface includes:

- exact 20-H1 warmup;
- current-close exclusion;
- exact upper/lower threshold inclusivity;
- immediately-inside-threshold binary64 cases;
- exact sigma-zero UNDEFINED;
- no hidden near-zero epsilon;
- population denominator 20 rather than sample denominator 19;
- continuity reset and no cross-block reference;
- deterministic replay;
- validation precedence;
- nonfinite, nonpositive and binary64-conversion failure handling;
- integer/float normalization parity;
- large finite positive close handling;
- exact previous-20 trace binding;
- steady-trend directional triggering;
- no mean/sigma/z/performance/execution/position output.

## 6. Independent synthetic reference

The frozen breaker includes an independently written `Decimal` reference for safe synthetic corpora away from numerical decision boundaries.

Observed:

```text
INDEPENDENT_DECIMAL_REFERENCE_PARITY =
PASS
```

The reference does not reuse the runtime mean/sigma implementation.

It is not a claim of independent real-market validation.

## 7. Numerical and adversarial mutation sweep

Twelve temporary implementation mutations were created one at a time and never persisted:

```text
M01_LOOKBACK_19
M02_LOWER_THRESHOLD_STRICT
M03_UPPER_THRESHOLD_STRICT
M04_SAMPLE_DENOMINATOR_19
M05_INCLUDE_CURRENT_IN_REFERENCE
M06_ZERO_SIGMA_NEUTRAL
M07_HIDDEN_SIGMA_EPSILON
M08_DISABLE_H1_STEP_GUARD
M09_ALLOW_NONPOSITIVE_CLOSE
M10_INVERT_SHORT_SIGNAL
M11_NAIVE_MEAN
M12_REMOVE_SQRT
```

A separate synthetic numerical boundary probe was also used for the mean-algorithm mutation without altering the persisted breaker.

Observed:

```text
BASELINE_NUMERIC_PROBE =
NEUTRAL

MUTATIONS_TOTAL =
12

MUTATIONS_KILLED =
12

MUTATIONS_SURVIVED =
0

MUTATION_SWEEP =
PASS
```

## 8. Repository-wide regression attempt

A broader repository-wide pytest run was attempted as an additional non-preregistered regression check.

Collection stopped in the existing AP4 test surface:

```text
tests/test_ap4_price_structure.py
→ import numpy
→ ModuleNotFoundError: No module named 'numpy'
```

Direct environment check confirmed:

```text
NUMPY =
ABSENT
```

No dependency was installed and no environment mutation was performed.

Therefore:

```text
REPOSITORY_WIDE_REGRESSION =
BLOCKED_ENVIRONMENT_MISSING_NUMPY

REPOSITORY_WIDE_REGRESSION_PASS =
NOT_CLAIMED
```

This environment blocker is not evidence of an SFE-02B runtime defect.

## 9. Qualification verdict

```text
SFE_02B_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

SFE_02B_FROZEN_BREAKER =
PASS_42_OF_42

SFE_02B_INDEPENDENT_DECIMAL_REFERENCE =
PASS_ON_DECLARED_SYNTHETIC_CORPUS

SFE_02B_NUMERICAL_MUTATION_SWEEP =
PASS_12_OF_12_KILLED

SFE_02B_SYNTHETIC_SIGNAL_KERNEL =
QUALIFIED

SFE_02B_MINIMAL_IMPLEMENTATION =
PASS_WITHIN_DECLARED_SYNTHETIC_SURFACE

REPOSITORY_WIDE_REGRESSION =
BLOCKED_ENVIRONMENT_MISSING_NUMPY

REAL_MARKET_DATA =
NONE

BREAKOUT_PERFORMANCE_OBSERVATION =
NONE

MEAN_REVERSION_PERFORMANCE_OBSERVATION =
NONE

BEHAVIORAL_Y =
NONE

PNL =
NONE

BACKTEST =
NONE
```

## 10. Preserved scientific meaning

This qualification establishes only that the persisted runtime implements the adopted MEAN_REVERSION_V1 signal definition and the frozen numerical semantics on the preregistered synthetic adversarial surface.

It does not establish:

```text
MEAN_REVERSION_V1_SUPPORTED
MEAN_REVERSION_V1_REFUTED
MEAN_REVERSION_V1_PROFITABLE
ECONOMIC_EDGE
ROBUSTNESS
SOURCE_INDEPENDENCE
PRODUCTION_READINESS
```

## 11. Next authorized operation

The remaining operation inside the current human authorization is:

```text
FINAL PERSISTED-STATE REBREAK
→ PERSIST CLOSURE
→ STOP
```

No experiment contract or performance observation is opened by this qualification report.
