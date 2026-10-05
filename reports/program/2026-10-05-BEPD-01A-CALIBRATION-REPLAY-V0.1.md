# BEPD-01A — SIX-WEEK CALIBRATION REPLAY V0.1

**Date:** 2026-10-05  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Replay persistence parent HEAD:** `b8041df7e1e6885051af15fe164fdbd585df3a7f`  
**Replay persistence parent TREE:** `7615cf9d78bcc04c39faa576130229022687fe39`  
**Contract blob:** `341f6267f7f1add350759d6d95dfebfb5b9e46f7`  
**Fixture blob:** `89f2af87171002e75fa06d7fb704817e149968bc`  
**Fixture canonical-text SHA-256:** `0365e0dfb1c5e3f78f4a3f01aca1f3bc91dc13147900c63831e4a51c1644434e`  
**Dataset:** `USTECH_PROFILE_MINUTE_CORE_V0_1`  
**AP0 manifest SHA-256:** `62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce`  
**Price surface:** descriptive `mid`  
**Status:** OBSERVED_READ_ONLY_CALIBRATION_REPLAY / NOT_GENERAL_QUALIFICATION

## 1. Purpose

Replay the human-annotated 2026-01-12 → 2026-02-20 Weekly example against real AP0 minute data and freeze exact expected outputs for a future implementation breaker.

## 2. Observed Weekly anchors

```text
2026-01-12
H = 25880.369 @ 2026-01-13 14:32 +01
L = 25262.8315 @ 2026-01-14 19:38 +01
C = 25522.4835

2026-01-19
H = 25709.83
L = 24883.833
C = 25570.013

2026-01-26
H = 26219.597
L = 25267.864
C = 25532.501

2026-02-02
H = 25917.352
L = 24150.3635
C = 25040.6875

2026-02-09
H = 25382.97
L = 24507.2445
C = 24728.0505

2026-02-16
H = 25079.9755
L = 24382.217
C = 25018.969
```

## 3. Stateful expected clusters

### Target week 2026-01-19

```text
LOW from 2026-01-12 = 25262.8315
age = 1 week
take H1 = 2026-01-19 02:00 +01
take close = 25242.3845
reintegration H1 = 2026-01-20 02:00 +01
reintegration close = 25267.261
target Weekly close = 25570.013
D = +307.1815
```

### Target week 2026-01-26

```text
HIGH from 2026-01-19 = 25709.83
age = 1 week
take H1 = 2026-01-26 16:00 +01
reintegration H1 = 2026-01-29 16:00 +01
D = +177.329

HIGH from 2026-01-12 = 25880.369
age = 2 weeks
take H1 = 2026-01-27 12:00 +01
reintegration H1 = 2026-01-27 13:00 +01
D = +347.868
```

One target Weekly therefore contains two consumed active HIGH levels. They remain two level-specific observations inside one shared Weekly cluster.

### Target week 2026-02-02

```text
LOW from 2026-01-26 = 25267.864
age = 1 week
take H1 = 2026-02-02 03:00 +01
reintegration H1 = 2026-02-02 09:00 +01
D = -227.1765

LOW from 2026-01-19 = 24883.833
age = 2 weeks
take H1 = 2026-02-04 18:00 +01
reintegration H1 = 2026-02-04 20:00 +01
D = +156.8545
```

This is the anti-selection case: the same Weekly contains one negative and one positive level-specific outcome. Neither may be discarded.

### Target week 2026-02-09

```text
No seeded active level consumed.
```

### Target week 2026-02-16

```text
LOW from 2026-02-09 = 24507.2445
age = 1 week
take H1 = 2026-02-17 15:00 +01
reintegration H1 = 2026-02-17 16:00 +01
D = +511.7245
```

## 4. TradingView / AP0 diagnostic

Human Pepperstone anchors and AP0 mid values are close on the manually checked Weekly High/Low geometry:

```text
2026-01-12 H delta = +4.569
2026-01-12 L delta = +9.0315
2026-01-19 H delta = +4.13
2026-01-19 L delta = +2.933
```

Weekly closes show larger cross-feed differences. Pepperstone prices are not substituted into the AP0 fixture.

## 5. Replay verdict

```text
CALIBRATION_MECHANISM =
OBSERVED

H1-CLOSE TAKE SEMANTICS =
OBSERVED

ACTIVE-LEVEL PERSISTENCE =
OBSERVED

PERMANENT CONSUMPTION =
OBSERVED

MULTI-LEVEL SAME-WEEK CLUSTER =
OBSERVED

NEGATIVE RESULT PRESERVATION =
OBSERVED

NO-EVENT WEEK =
OBSERVED

FIVE-YEAR GENERALIZATION =
NOT TESTED / NOT AUTHORIZED

STATISTICAL PROBABILITY CLAIM =
NOT MADE
```

## 6. Scope limitation

The fixture is seeded only from the 2026-01-12 Weekly. It is not evidence that levels created before the fixture window are absent.

The replay validates the calibration semantics over this bounded surface only.

## 7. Stop boundary

No general implementation, five-year execution, occurrence/response map, strategy research, PnL, paper, broker, live or capital authority is created by this report.
