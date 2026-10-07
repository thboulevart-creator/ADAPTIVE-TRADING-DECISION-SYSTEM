# BEPD-09C — SYNTHETIC QUALIFICATION V0.1

## Verdict

```text
BEPD-09C =
SYNTHETICALLY_QUALIFIED
FOR HUMAN ADJUDICATION

AUTOMATED TESTS =
44 / 44 PASS
```

This qualification applies to immutable implementation commit:

```text
IMPLEMENTATION HEAD =
bb716dad71a8e73f4ec75b4238c1254586c36488

IMPLEMENTATION TREE =
60606a844c8012560dd28435ec25bbb41564a2b2
```

## Canonical package identity

All eight implementation artifacts were read back from the immutable GitHub commit and matched their expected blob identities exactly.

```text
CANONICAL BLOB READBACK =
8 / 8 PASS
```

## Synthetic-only execution

The deterministic qualification fixture contains:

```text
CALENDAR WEEKS =
120

SYNTHETIC EVENT ROWS =
466

EMPTY CALENDAR WEEKS =
7

DST DURATIONS COVERED =
167 / 168 / 169 HOURS

FORWARD FOLDS COVERED =
5

REAL DATA USED =
NO
```

No line from the real EVENT_LEDGER was read or ingested.

## Primary / independent reference parity

Frozen before canonical persistence:

```text
FLOATING ABSOLUTE TOLERANCE =
2e-5

STRUCTURAL / DESIGN-MATRIX TOLERANCE =
1e-12
```

Observed synthetic maximum absolute differences:

```text
PREDICTED PROBABILITIES =
9.252156032868442e-06

PER-WEEK METRICS =
1.5179080629867947e-05

AGGREGATE METRICS =
6.393542788529771e-07

DESIGN MATRICES =
0

STANDARDIZATION PARAMETERS =
0

EXPOSURE FRACTION =
0

SPLINE BASIS =
0
```

```text
PRIMARY / REFERENCE PARITY =
PASS
```

## Deterministic replay

```text
PRIMARY REPLAY ID =
17bf889af41aad3d60bb15b017b2b0bb038468f4c3b2e8b6f3c98818a5f3d7bb

REFERENCE REPLAY ID =
0dac5f5f569a8494221b051de7fff39d699c83fa2f13da7450a19b1ff7e5a1e9

PRIMARY REPEAT =
IDENTICAL

REFERENCE REPEAT =
IDENTICAL
```

The two replay IDs are not required to equal each other because the primary and reference implementations are deliberately independent numerical paths. Required structural and numerical surfaces are compared directly under the frozen tolerances.

## Negative breaker execution

The automated suite exercised fail-closed paths including missing values, invalid side, nonfinite numeric input, invalid exposure, zero level price, duplicate event identity, week/cluster mismatch, one-class training fold, zero-variance training feature, perfect separation, forced nonconvergence, target-week split, cluster split and post-T0 unauthorized feature attempt.

No adaptive fallback is authorized.

## Numerical implementation note

During pre-persistence synthetic engineering, an initial primary solver path correctly failed closed on convergence.

Before canonical persistence, with no real-data access and without modifying the frozen scientific protocol, the numerical implementation was revised to the preregistered unregularized logistic target using a Newton-CG path with exact score/Hessian and explicit complete-separation fail-closed detection.

The independent reference uses a separate root-solving path.

This is implementation qualification, not scientific result tuning.

## Scientific boundary

```text
REAL EVENT_LEDGER READ =
NO

REAL C1 ROW INGESTION =
NO

REAL C1 MODEL FIT =
NO

REAL LOGLOSS RESULT =
NONE

REAL BRIER RESULT =
NONE

REAL FOLD RESULT =
NONE

REAL RESPONSE DISTRIBUTION =
NONE

FRESH OOS READ =
NO

C1 SCIENTIFICALLY VALIDATED =
NO

C1 HISTORICALLY VALIDATED =
NO

PREDICTION VALIDATED =
NO

GENERALIZATION ESTABLISHED =
NO

EDGE ESTABLISHED =
NO

STRATEGY VALIDATED =
NO

TRADING AUTHORITY =
NONE
```

## Next

Persisted-head verification only.

Then:

```text
STOP

NEXT =
HUMAN ADJUDICATION
OF BEPD-09C PACKAGE ONLY
```

No real historical C1 execution is opened automatically.
