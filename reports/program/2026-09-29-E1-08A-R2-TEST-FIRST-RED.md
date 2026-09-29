# E1-08A-R2 — TEST-FIRST RED

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Persisted RED HEAD:

`a4d62d02d4c7e19769d4e372a02152d3b5b86760`

Persisted RED TREE:

`e9b028e66122c157139a5ee605c59f6086bb8c6e`

GitHub Actions Windows run/job:

`36545058034 / 109329335988`

## Environment

Observed on `windows-2025` before the breaker:

```text
Python = 3.12.10
pyarrow = 25.0.1
R2_WINDOWS_ENVIRONMENT = PASS
```

## Expected RED

The old R1 runtime still required Python 3.12.14 on every platform.

Observed R2 breaker:

```text
R2 executable cases = 5
PASS = 1
FAIL = 4
```

The passing case was the non-environment invariance check.

The four failures are exactly attributable to the old global Python binding:

- real Windows 3.12.10 incorrectly BLOCKED;
- simulated Windows 3.12.14 incorrectly PASS;
- Linux 3.12.14 response lacks the new `system` field;
- pyarrow mismatch test is pre-empted by the old Python mismatch.

No strategy, dataset, OOS, runner or execution-model defect was observed.

Adjudication:

```text
E1_08A_R2_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
REAL_E1_RUN = NOT_AUTHORIZED_BY_R2
REAL_OOS_PERFORMANCE = NOT_OBSERVED
```
