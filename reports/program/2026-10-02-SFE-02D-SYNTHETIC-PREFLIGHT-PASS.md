# SFE-02D — SYNTHETIC PREFLIGHT PASS

**Date:** 2026-10-02  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Purpose

This artifact closes the synthetic preflight for the governed dual result-run runner before any real SFE performance calculation.

## 2. Persisted identities

```text
HEAD =
ace38c721d4db4d2671ba79384e2a2cf1ff6b9ff

TREE =
8d17dd11bda121fd6fea584a194a4204562f93da

RUN CONTRACT BLOB =
4fd8b1adb2bb8e6d2ca11870bdee88fd232c757f

DUAL RUNNER BLOB =
539d9fa0198a92cc1424a06ebb5606c708a71472

ORIGINAL BREAKER V0.1 BLOB =
e82fee01d8414603440db2d680c859c1d900fe6b

CORRECTED BREAKER V0.2 BLOB =
696730bfee380b4ee22d50e0b7714126dfd52196

PREFLIGHT FAIL REPORT BLOB =
3d6269339eebb2cbfab5737736086cef63f4c143
```

## 3. V0.1 break

Original synthetic preflight:

```text
TOTAL = 10
PASS = 8
FAIL = 2
```

Both failures were demonstrated breaker defects:

1. impossible directional signal during a reset warmup;
2. explicit `PNL` non-claim metadata incorrectly treated as a PnL result field.

No runner defect was established.

No real data run had started.

## 4. Targeted breaker correction

V0.2 changed only the synthetic breaker:

- new-block warmup rows are now `UNDEFINED`;
- PnL/result-field absence is checked separately from explicit governance `non_claims`.

The runner and experiment contracts remained unchanged.

## 5. V0.2 re-break

```text
PY_COMPILE = PASS

TOTAL = 10
PASS = 10
FAIL = 0

SYNTHETIC_PREFLIGHT =
PASS
```

Covered surfaces include:

- evidence-sufficiency gates;
- supported/refuted synthetic mappings;
- insufficient-evidence mapping;
- t+1 continuity exclusion;
- neutral-vs-undefined co-firing categories;
- atomic deterministic JSON output;
- Git blob hash primitive;
- exact t+1 continuity conditions;
- absence of PnL/execution result fields;
- primary `ALL_VALID_DIRECTIONAL_EVENTS` / `RAW_ZERO` surface.

## 6. Real-data authority after preflight

The user has authorized SFE-02D dual result-run qualification.

The real run remains subject to:

```text
BOTH ENVELOPES
MUST BE PRODUCED TOGETHER

BOTH ENVELOPES
MUST BE PERSISTED IN ONE GIT COMMIT

BEFORE HUMAN OR MODEL INSPECTION
OF EITHER RESULT
```

Allowed pre-persistence output is restricted to validation state, file existence, cryptographic hashes, and commit/push status.

## 7. State

```text
SFE_02D_SYNTHETIC_PREFLIGHT =
PASS

REAL_DUAL_RESULT_RUN =
AUTHORIZED_NEXT

REAL_PERFORMANCE_OBSERVED =
NO

STOP_BEFORE_NO_PEEK_RUN =
FALSE
```
