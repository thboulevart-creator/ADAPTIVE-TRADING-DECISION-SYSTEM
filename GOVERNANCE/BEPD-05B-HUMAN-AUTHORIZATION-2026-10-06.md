# BEPD-05B — HUMAN AUTHORIZATION — 2026-10-06

## Governed target

```text
REPOSITORY =
thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

BRANCH =
integration/system-v1

CONTROL =
BEPD-05B — FIRST REAL GLOBAL CLOSE-DISPLACEMENT AGGREGATION + TECHNICAL QUALIFICATION V0.1

HUMAN AUTHORIZATION =
AUTHORIZED
```

## Binding prior authority

```text
BEPD-05A FINAL HUMAN ADJUDICATION =
024c7d23210b9c62604b3c6d2379746c1ac736a4

BEPD-05A SEMANTICS + AGGREGATION CONTRACT =
0a580920ce47885d2bd3277b879b2b888b8d4354

BEPD-05A FROZEN ADVERSARIAL BREAKER =
c39802f70d83dc249d23fe240b61169bf20ac757

BEPD-05A PRE-AGGREGATION FREEZE =
30d438ef1daad9acaad170c002d7d5d8426acec4

BEPD-02 EVENT_LEDGER =
0d15e3bc8dc9393e53923bb91d7c74d30d1cf0b2
```

## Authorized execution

One and only one first real GLOBAL_ALL_SIDES aggregation of the already-persisted `close_displacement` field over all 472 qualified BEPD-02 EVENT_LEDGER rows, with no filtering and equal event weighting.

Authorized result surface:

```text
N
MINIMUM
MAXIMUM
MEAN
MEDIAN
P01 P05 P10 P25 P50 P75 P90 P95 P99
POSITIVE_COUNT ZERO_COUNT NEGATIVE_COUNT
POSITIVE_FRACTION ZERO_FRACTION NEGATIVE_FRACTION
EMPIRICAL_CDF
```

Binding numerical rules:

```text
QUANTILE METHOD = HYNDMAN-FAN TYPE 7
P50 = MEDIAN
ECDF = EXACT / UNSMOOTHED / UNBINNED
CANONICAL SCALAR OUTPUT = 18-DECIMAL ROUND_HALF_EVEN
```

Implementation and the BEPD-05A breaker must be technically qualified before first real aggregation.

Strict identical replays are reproducibility evidence only and are not new independent evidence.

## Explicit prohibitions

No subgroups; no time-to-reintegration; no MFE/MAE; no fixed-horizon returns; no Occurrence × Response; no parameter or threshold search; no OOS consumption; no prediction, causation, edge, strategy, PnL, trading or capital authority.

Evidence status of the real result must remain:

```text
EXPOSED_EXPLORATORY_ONLY
GENERALIZATION = NOT_ESTABLISHED
CONFIRMATORY GENERALIZATION = FRESH_OOS_EVIDENCE_REQUIRED
```

After technical qualification of the real result, STOP for human adjudication of that result.
