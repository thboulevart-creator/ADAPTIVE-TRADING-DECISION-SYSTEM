# BEPD-09A — DOCUMENTARY / PROGRAMMATIC QUALIFICATION V0.1

## Verdict

```text
BEPD-09A DESIGN PACKAGE =
QUALIFIED_FOR_HUMAN_ADJUDICATION

CHECKS =
33 / 33 PASS

DOCUMENTARY BREAKER HARD-FAIL CASES =
28 / 28 PRESENT

REAL EVENT_LEDGER ROWS READ =
NO

REAL RESULT RECOMPUTATION =
NO

STATISTICAL TEST =
NO

MODEL FIT =
NO

OOS READ =
NO
```

## Exact qualified state

```text
IMMUTABLE DESIGN COMMIT =
374ab2c04401eecb2b8f3319022df924ca889a8e

DESIGN TREE =
df4937f4934edec87a34449b27454d07453b44fb

HUMAN AUTHORIZATION =
7324ceafdc66c9fa9e21d2f6d8e455ab85c07e14

DESIGN CONTRACT =
a3a3dd9fae1548de2b5ee6bf76536e68820ba932

DOCUMENTARY BREAKER =
d5cc742bb4cd256dde6f9a9988caece3a687b54e

DESIGN REPORT =
a5dead3f42e2ce0521a168bfa9905f9a0a83c18d
```

## Qualified boundary

```text
T0 =
take_h1_close_utc

POST_T0 INFORMATION AS PREDICTOR =
FORBIDDEN

ROW PRESENCE =
NOT PROOF OF EX-ANTE AVAILABILITY

DERIVED FEATURE =
ALL INPUTS MUST BE AVAILABLE <= T0
AND FORMULA MUST BE FROZEN BEFORE RESPONSE READ
```

The readback qualification confirms that the known response/outcome fields are not predictor-eligible, including `same_week_reintegration`, reintegration timestamps/prices, `target_week_close_mid`, `close_displacement`, `CLOSE_SIDE`, `D_CLOSE`, `D_INTERNAL`, `D_EXTERNAL`, and final cluster-consumption count.

## Candidate gate

```text
C1 =
RANK 1 / PREFERRED FIRST CANDIDATE
same_week_reintegration as RESPONSE

C2 =
RANK 2
CLOSE_SIDE as RESPONSE

C3 =
RANK 3
D_CLOSE as RESPONSE

C4 =
RANK 4 / DEFER
TIME-TO-EVENT / SURVIVAL
```

C1 remains only a ranked candidate. Its variable remaining observation window to target-week end is explicitly material and must be handled in any later claim-specific design.

```text
FINAL CLAIM SELECTED =
NO

CLAIM TESTING AUTHORIZED =
NO
```

## Scientific boundary

```text
HISTORICAL CORPUS =
ALREADY EXPOSED

GENERALIZATION =
NOT_ESTABLISHED

PREDICTION =
NO

CAUSATION =
NOT_ESTABLISHED

EDGE =
NO

STRATEGY VALIDATION =
NO

TRADING AUTHORITY =
NONE
```

## Next

Persisted-head verification only, then human adjudication of the BEPD-09A design package.

No candidate claim may be preregistered or tested before that separate human decision.

```text
STOP AFTER PERSISTED-HEAD VERIFICATION
```
