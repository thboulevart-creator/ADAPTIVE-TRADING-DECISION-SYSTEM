# E1-08A — ONE-SHOT REAL E1 — TEST-FIRST RED

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Persisted HEAD under test:

`ff26ae07817b91227430bd401fab6ac405b1e67b`

Persisted TREE under test:

`6ab5132cc57ad39d6b27a0f4e885c4f30ef5b482`

## 1. Frozen preregistration identities

```text
contract =
4d868b34c42fe6765ece8007a0bf173d22199ab1

breaker =
20297ca64c12bf9cd1eb9f6bef73598692959342

future target =
tools/e1_08_one_shot_real_e1.py
```

The contract and breaker were materialized byte-exactly and locally re-hashed with Git blob framing before execution.

Observed local Git blob identities:

```text
contract = 4d868b34c42fe6765ece8007a0bf173d22199ab1
breaker  = 20297ca64c12bf9cd1eb9f6bef73598692959342
```

Both matched the persisted GitHub blobs.

## 2. Expected RED state

The preregistered target is absent.

Expected unique failure:

`E1_08_TARGET_ABSENT_EXPECTED_RED`

Expected surface:

`Q8-01 → Q8-20`

## 3. Observed execution

The exact persisted breaker was executed locally against the exact persisted contract.

Observed:

```text
TOTAL = 20
PASS = 0
FAIL = 20

UNIQUE FAILURE =
E1_08_TARGET_ABSENT_EXPECTED_RED
```

No collection error or alternative failure class was observed.

Adjudication:

```text
E1_08A_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_08A_EXECUTOR = ABSENT
E1_08A_IMPLEMENTATION = NOT_YET
```

## 4. Authority boundary

This RED did not access or calculate real Momentum OOS performance.

```text
REAL_E1_RUN = NOT_AUTHORIZED
REAL_OOS_PERFORMANCE = NOT_AUTHORIZED
E1_08B = NOT_AUTHORIZED
AUTOMATIC_RERUN = NOT_AUTHORIZED
MT5/PAPER/BROKER/LIVE/CAPITAL = CLOSED
PHASE_22_PLUS = CLOSED
```

The next permitted action inside the already-authorized E1-08A boundary is the minimal executor candidate.