# SFE-02B — MEAN_REVERSION_V1 — FINAL PERSISTED-STATE CLOSURE

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Closure boundary

This closes only the synthetic implementation and numerical-qualification surface authorized for `SFE-02B — MEAN_REVERSION_V1`.

It does not authorize or establish any real-data, behavioral-performance, PnL, execution, ranking, routing or production claim.

## 2. Persisted state re-broken

Final persisted state before this closure artifact:

```text
HEAD =
b45d46e75cfe1d593851abf4140ecedf4f7882d0

TREE =
db36da116edac37944e7fe7f56cedf3c6f527237
```

Protected upstream identities:

```text
SFE-01 ADJUDICATION =
66aa556e4e161e49550451062273bc8d6422593c

SFE-02A CLOSURE =
b88d7468394913606b5931b1c3cc070631e19912

REPOSITORY SAFETY RULES =
b69f3cfab5318b950d70d4310bb763f08ef9d374
```

Protected SFE-02B identities:

```text
CONTRACT =
GOVERNANCE/SFE-02B-MEAN-REVERSION-V1-MINIMAL-IMPLEMENTATION-CONTRACT-V0.1.json

CONTRACT_BLOB =
ba4b98296c8d4f1e37793f3cb5f1dbdfb0fe7d9d


BREAKER =
breakers/sfe_02b_mean_reversion_v1_red_breaker.py

BREAKER_BLOB =
a3406991cb534f3590dbe02aafbb995f66b01d84


RUNTIME =
tools/sfe_02b_mean_reversion_v1.py

RUNTIME_BLOB =
273e184093e4cc98f0eb6569cd6f1007366cce40


TEST_FIRST_RED_REPORT =
reports/program/2026-10-02-SFE-02B-MEAN-REVERSION-V1-TEST-FIRST-RED.md

RED_REPORT_BLOB =
84ad8a57eb76928f535cf945901aee5b4b84484b


QUALIFICATION_REPORT =
reports/program/2026-10-02-SFE-02B-MEAN-REVERSION-V1-MINIMAL-IMPLEMENTATION-QUALIFICATION.md

QUALIFICATION_REPORT_BLOB =
104831403fe18d447ed5b9dec66b33525dc65a4c
```

## 3. Frozen numerical semantics closed

The qualified runtime preserves:

```text
PRICE REPRESENTATION =
IEEE-754 binary64 / Python float

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

ZERO SIGMA =
SIGMA == 0.0 exactly
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

No parameter or signal-rule change was introduced.

## 4. Final persisted-head execution

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

Frozen breaker:

```text
M2B-01 → M2B-42

TOTAL = 42
PASS = 42
FAIL = 0
```

Workspace state before execution:

```text
GIT_STATUS = CLEAN
```

Workspace state after removal of generated `__pycache__`:

```text
GIT_STATUS = CLEAN
```

## 5. Adversarial evidence

The persisted runtime passed the frozen breaker and the separately executed numerical/adversarial mutation sweep:

```text
MUTATIONS_TOTAL = 12
MUTATIONS_KILLED = 12
MUTATIONS_SURVIVED = 0
```

Mutations covered:

- wrong lookback;
- strict threshold mistakes;
- sample denominator 19;
- current-bar contamination;
- zero-sigma misclassification;
- hidden epsilon;
- H1 continuity bypass;
- nonpositive-close acceptance;
- direction inversion;
- naive mean;
- missing square root.

No mutant was persisted.

## 6. Independent reference

The preregistered breaker included an independently written `Decimal` implementation on safe synthetic corpora.

```text
INDEPENDENT_DECIMAL_REFERENCE_PARITY =
PASS
```

This is synthetic implementation evidence only, not external market validation.

## 7. Repository-wide regression status

A repository-wide pytest attempt remained blocked at collection because the available ATDS pytest environment lacks `numpy`, required by existing AP4 tests.

```text
REPOSITORY_WIDE_REGRESSION =
BLOCKED_ENVIRONMENT_MISSING_NUMPY

REPOSITORY_WIDE_REGRESSION_PASS =
NOT_CLAIMED
```

No dependency was installed and no environment mutation was performed.

This blocker is not evidence of an SFE-02B runtime defect.

## 8. Final SFE-02B verdict

```text
SFE_02B_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

SFE_02B_FROZEN_BREAKER =
PASS_42_OF_42

SFE_02B_INDEPENDENT_DECIMAL_REFERENCE =
PASS_ON_DECLARED_SYNTHETIC_CORPUS

SFE_02B_NUMERICAL_MUTATION_SWEEP =
PASS_12_OF_12_KILLED

SFE_02B_FINAL_PERSISTED_STATE_REBREAK =
PASS_42_OF_42

SFE_02B_SYNTHETIC_SIGNAL_KERNEL =
QUALIFIED

SFE_02B_MINIMAL_IMPLEMENTATION =
PASS_WITHIN_DECLARED_SYNTHETIC_SURFACE

SFE_02B =
CLOSED_AT_SYNTHETIC_IMPLEMENTATION_BOUNDARY
```

## 9. Scientific state after SFE-02A + SFE-02B

```text
BREAKOUT_V1_DEFINITION =
HUMAN_ADOPTED

BREAKOUT_V1_IMPLEMENTATION =
SYNTHETIC_KERNEL_QUALIFIED

BREAKOUT_V1_PERFORMANCE =
NOT_OBSERVED


MEAN_REVERSION_V1_DEFINITION =
HUMAN_ADOPTED

MEAN_REVERSION_V1_IMPLEMENTATION =
SYNTHETIC_NUMERICAL_KERNEL_QUALIFIED

MEAN_REVERSION_V1_PERFORMANCE =
NOT_OBSERVED
```

No real market evidence has been consumed for either family.

## 10. Explicit non-claims

This closure does not establish:

```text
MEAN_REVERSION_V1_SUPPORTED
MEAN_REVERSION_V1_REFUTED
MEAN_REVERSION_V1_PROFITABLE
BREAKOUT_V1_SUPPORTED
BREAKOUT_V1_REFUTED
BREAKOUT_V1_PROFITABLE
ECONOMIC_EDGE
ROBUSTNESS
SOURCE_INDEPENDENCE
COMPARATIVE_SUPERIORITY
PRODUCTION_READY
```

## 11. Authority after closure

```text
REAL_MARKET_DATA = NOT_AUTHORIZED
PERFORMANCE_OBSERVATION = NOT_AUTHORIZED
BEHAVIORAL_Y = NOT_AUTHORIZED
PNL = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED
EXECUTION = NOT_AUTHORIZED
OPTIMIZATION = NOT_AUTHORIZED
RANKING = NOT_AUTHORIZED
ROUTER = NOT_AUTHORIZED
REGIME_FILTER = NOT_AUTHORIZED
```

No experiment contract is automatically opened.

The previously selected scientific sequence now reaches the point where both family implementations are qualified and the next future boundary would be to preregister the **experiment designs for both families before observing either family’s performance**.

That future boundary requires separate explicit human authorization.

## 12. STOP

```text
SFE-02A =
CLOSED

SFE-02B =
CLOSED

BREAKOUT_PERFORMANCE =
NOT_OBSERVED

MEAN_REVERSION_PERFORMANCE =
NOT_OBSERVED

NEXT_CANDIDATE_FRONTIER =
DUAL EXPERIMENT PREREGISTRATION BEFORE ANY PERFORMANCE OBSERVATION

STOP =
TRUE
```
