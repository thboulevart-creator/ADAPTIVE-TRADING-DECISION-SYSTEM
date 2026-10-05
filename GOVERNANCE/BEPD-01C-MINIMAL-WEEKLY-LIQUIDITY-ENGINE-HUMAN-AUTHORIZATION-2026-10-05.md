# BEPD-01C — MINIMAL WEEKLY LIQUIDITY ENGINE — HUMAN AUTHORIZATION — 2026-10-05

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Governed branch:** `integration/system-v1`  
**Authorization parent HEAD:** `434e369b64a285c7da1aa1d0be8ea5d0fd0540f3`  
**Authorization parent TREE:** `6d2d206a239f6245937ead6eb23dd75e660926de`

## 1. Human authorization

```text
BEPD-01C — MINIMAL WEEKLY LIQUIDITY ENGINE IMPLEMENTATION
+ FROZEN BREAKER GREEN QUALIFICATION V0.1

STATUS =
HUMAN_AUTHORIZED
```

Authorized target:

```text
tools/bepd_01_weekly_liquidity_engine.py
```

Authorized interfaces only:

```text
evaluate_level_event
advance_week
replay_calibration
```

## 2. Frozen bindings

```text
BEPD-01A CONTRACT BLOB =
341f6267f7f1add350759d6d95dfebfb5b9e46f7

BEPD-01A FIXTURE R1 BLOB =
d2e663eaef865507c1cb92f5baa0074dcfc11032

BEPD-01B CONTRACT BLOB =
d602a0666ab92662f2355ce0f44893934a7943a1

BEPD-01B EXECUTABLE BREAKER BLOB =
8433b725bb47423eac5879074557202993a664c2

BEPD-01B EXPECTED RED EVIDENCE BLOB =
1daeb46a74748fc0870f6543872e013930a0af61
```

The 20 BEPD-01B semantic cases are frozen and may not be changed or relaxed to obtain GREEN.

## 3. Required semantics

```text
WEEKLY HIGH/LOW only after source Weekly completion
ACTIVE level lifecycle
H1 close strictly beyond for take
permanent consumption
reintegration only on a strictly later H1 close
older untaken levels persist
multiple consumed levels in one target Weekly share one cluster
positive, negative and no-reintegration outcomes remain observable
```

## 4. Allowed implementation loop

```text
CREATE MINIMAL ENGINE
→ REPLAY UNCHANGED BREAKER
→ IF RED: CHANGE ENGINE ONLY
→ REPLAY UNCHANGED BREAKER
→ GREEN ONLY IF ALL BREAKER CONTROLS PASS
→ PERSIST EXACT GREEN EVIDENCE
→ STOP
```

## 5. Explicit prohibitions

```text
BEPD-01A CONTRACT CHANGE = FORBIDDEN
BEPD-01B CASE CHANGE = FORBIDDEN
BREAKER RELAXATION = FORBIDDEN
FIVE-YEAR SCAN = NOT AUTHORIZED
OCCURRENCE MAP = NOT AUTHORIZED
RESPONSE MAP = NOT AUTHORIZED
STRATEGY RESEARCH = NOT AUTHORIZED
BACKTEST / PNL = NOT AUTHORIZED
PAPER / BROKER / LIVE / CAPITAL = NOT AUTHORIZED
```

The calibration replay may read only the bounded AP0 data needed by the adopted six-week fixture.
