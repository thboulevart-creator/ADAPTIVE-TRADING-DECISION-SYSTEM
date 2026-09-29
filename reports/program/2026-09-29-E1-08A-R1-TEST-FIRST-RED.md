# E1-08A-R1 — TEST-FIRST RED

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Persisted HEAD under RED:

`18b320214c47d5a93d61d795920489fee1a2374c`

Persisted TREE:

`eb37b167c78e87b5d3a452dae8d0a0bf4545f211`

GitHub Actions run:

`36536996640`

GitHub Actions job:

`109303214432`

## Frozen preregistration

```text
contract =
d4155af3fa5e1db2abfd3902469b9ae332434464

breaker =
eaf8dc6846f30a068c3a6cbebb3286e188e419d9

real-run requirements =
8a047b50d76c12784c9b0bee7b6f2a629df60fd5

workflow =
30e7c9146c169a872d6871b8e7796985b5eb6516
```

## Environment precondition

Observed before RED:

```text
Python = 3.12.14
pyarrow = 25.0.1
R1_ENVIRONMENT = PASS
```

No real Source-B data and no Momentum OOS performance were accessed.

## Expected RED

Target:

`tools/e1_08a_r1_real_run.py`

Expected state:

`ABSENT`

Expected unique failure:

`E1_08A_R1_TARGET_ABSENT_EXPECTED_RED`

## Observed RED

The frozen breaker executed 22 preregistered families. Parameterized attacks expanded the executable surface to 26 cases.

```text
EXECUTED = 26
PASS = 0
FAIL = 26

UNIQUE FAILURE =
E1_08A_R1_TARGET_ABSENT_EXPECTED_RED
```

No alternative defect class was observed.

Adjudication:

```text
E1_08A_R1_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
TARGET = ABSENT
IMPLEMENTATION = NOT_YET
```

Authority remains:

```text
REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_AUTHORIZED
E1_08B = NOT_AUTHORIZED
AUTOMATIC_RERUN = NOT_AUTHORIZED
MT5/PAPER/BROKER/LIVE/CAPITAL = CLOSED
```

Next action inside the authorized R1 cycle:

`MINIMAL IMPLEMENTATION CANDIDATE`
