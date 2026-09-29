# E1-08A-R2 — WINDOWS RUNTIME CORRECTION — QUALIFICATION

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Qualified runtime HEAD:

`5e1ceb171c57f2c4804f923d47e6388f8f75f648`

Qualified runtime TREE:

`6ba93c5dfbcdc9aea706682be9a13ce087135d60`

Qualified R2 executor blob:

`5a91f7b072fb37e8653027c387096ced6da9c053`

## 1. Scope

R2 was explicitly human-authorized for one minimal correction:

```text
Windows real-run Python:
3.12.14 → 3.12.10
```

Unchanged:

```text
Linux qualification Python = 3.12.14
pyarrow = 25.0.1
strategy = unchanged
dataset = unchanged
OOS = unchanged
runner = unchanged
execution model = unchanged
```

No real Source-B Momentum performance was computed or observed.

## 2. Frozen R2 preregistration

```text
R2 contract =
78b38f62365f154c7b151eab3d03d50423adcb82

R2 breaker =
ef4ecda3b6641cffa8a1932c490365fecfe7847c

R2 Windows workflow =
a90904006afe5157f41328111061a7e877711899
```

R1 requirements remain byte-identical:

`8a047b50d76c12784c9b0bee7b6f2a629df60fd5`

## 3. Test-first RED

RED persisted HEAD:

`a4d62d02d4c7e19769d4e372a02152d3b5b86760`

Windows run/job:

`36545058034 / 109329335988`

Observed environment before RED:

```text
Windows runner = windows-2025
Python = 3.12.10
pyarrow = 25.0.1
R2_WINDOWS_ENVIRONMENT = PASS
```

Observed breaker:

```text
5 executable cases
1 PASS
4 FAIL
```

The passing case was the non-environment invariance check.

The four failures were exactly attributable to the old global Python 3.12.14 binding.

Adjudication:

`E1_08A_R2_TEST_FIRST_RED = PASS_EXPECTED_FAILURE`

## 4. Minimal implementation

Only:

`tools/e1_08a_r1_real_run.py`

was technically modified.

Environment binding changed from one global Python version to:

```text
Windows → Python 3.12.10
Linux   → Python 3.12.14
```

`pyarrow 25.0.1` remains exact on both.

No strategy, dataset, H1, OOS, runner, execution-model, authority-schema, Parquet-cursor or result semantic was modified.

## 5. Windows qualification

GitHub Actions:

```text
run = 36545309207
job = 109330156782
runner = windows-2025
Python = 3.12.10
pyarrow = 25.0.1
```

Observed:

```text
R2_WINDOWS_ENVIRONMENT = PASS
R2 frozen breaker = 5/5 PASS
clean worktree = PASS
```

## 6. Linux/R1 non-regression qualification

GitHub Actions:

```text
run = 36545309230
job = 109330157037
runner = ubuntu-24.04
Python = 3.12.14
pyarrow = 25.0.1
```

Observed:

```text
R1 frozen breaker = 26/26 PASS
existing Q8 frozen breaker = 20/20 PASS
clean worktree = PASS
```

Therefore the Windows correction did not break the previously qualified Linux/R1 path.

## 7. Protected invariance

At the qualified runtime HEAD, exact blob verification confirmed unchanged identities for all protected E1-01→E1-08A artifacts and all frozen R1 contract/breaker/requirements/workflow artifacts.

R2 changed only the environment binding in the R1 real-run target, plus additive R2 governance/test/workflow evidence.

## 8. Adjudication

```text
E1_08A_R2_PREREGISTRATION = PASS
E1_08A_R2_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_08A_R2_WINDOWS_31210 = PASS
E1_08A_R2_LINUX_31214_NON_REGRESSION = PASS
E1_08A_R2_PYARROW_2501 = PASS
E1_08A_R2 = PASS
```

## 9. Authority state

The earlier E1-08B authorization referenced:

```text
HEAD =
94a8b35022babc01ab81e0157885474a1c159e20

TREE =
946af1ca21809df4a0a6ac8413262523205039aa

executor blob =
d3e9c848f5585346048e1a911d82cdf865b06e85
```

R2 necessarily changed all three governed execution bindings.

Therefore:

```text
PREVIOUS_E1_08B_AUTHORIZATION = SUPERSEDED / NOT VALID FOR R2 STATE

REAL_E1_RUN = NOT_EXECUTED
OOS_EXPOSED = FALSE
AUTOMATIC_RERUN = NOT_AUTHORIZED
```

A new exact E1-08B human authorization is required against the final post-R2 HEAD/TREE/executor blob.

## 10. Hard stop

```text
E1-08A-R2 = PASS
HARD_STOP = TRUE
```

Next candidate boundary:

```text
E1-08B
—
RE-AUTHORIZE EXACT ONE-SHOT REAL E1
AGAINST POST-R2 STATE
```
