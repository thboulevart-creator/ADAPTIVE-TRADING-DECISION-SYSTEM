# ASSET BEHAVIORAL PROFILE CORE V0.1 — USTECH

Date : 2026-09-26  
Status : **CORE_COMPLETE / PASS**  
DatasetIdentity : `USTECH_PROFILE_MINUTE_CORE_V0_1`

## 1. Scope

This CORE describes what has been empirically qualified about USTECH price-core behavior before any strategy or performance research.

It is not:
- a strategy;
- an edge claim;
- a signal catalogue;
- a backtest;
- a causal model;
- an execution-price model.

Source period: 2021-05-25 → 2026-05-24, discontinuous.

Coverage:
- 1,709,180 canonical minutes;
- 376,003,618 source ticks;
- 1,606 segments;
- 61 AP0 files.

Qualified chain:
AP0 → AP1 → AP2 → AP3 → AP4 → AP5 → AP6.

Machine-readable CORE:
`reports/program/evidence/2026-09-26-ASSET-BEHAVIORAL-PROFILE-CORE-V0.1.json`.

## 2. Data truth constraints

The price-core is based on timestamp/bid/ask-derived descriptive mid prices and spread.

Not qualified:
- traded volume;
- market depth;
- order flow;
- sub-minute microstructure;
- execution-price realism.

Gaps are never silently bridged.

There are 1,605 reopen boundaries.

## 3. Core property — intraday structure is relative and persistent

The strongest temporally persistent organization found is **New York time-of-day**.

Across complete years 2022–2025, minimum pairwise Spearman of hourly mean profiles:
- minute range: **0.9674**
- RV15: **0.9634**
- RV60: **0.9650**
- tick density: **0.9812**

Full-sample examples:
- 10:00 NY: minute range ≈ 8.884 bps, RV60 ≈ 49.79 bps, tick density ≈ 439/min;
- 00:00 NY: minute range ≈ 1.725 bps, RV60 ≈ 9.74 bps, tick density ≈ 95/min.

This supports a **persistent relative intraday shape**.

It does **not** support one timeless absolute volatility scale.

## 4. Core property — absolute volatility level is nonstationary

Across 2022–2025:
- minute-range mean CV ≈ **27.34 %**
- RV15 mean CV ≈ **27.13 %**
- RV60 mean CV ≈ **27.25 %**
- tick-density mean CV ≈ **27.88 %**

AP2/AP6 yearly examples show large level changes, with 2022 materially above 2023–2025 for absolute volatility.

Therefore:

**absolute volatility thresholds derived from the full sample must not be treated as permanent asset constants.**

This confirms the AP3 observation that normalizing only by hour does not remove inter-year distribution changes.

## 5. Core property — weekday structure persists; month structure does not

For range/RV/tick, complete-year weekday-profile minimum Spearman is **0.942857**.

Full-sample weekday ordering shows Friday higher in range/volatility/activity than earlier weekdays, while Sunday/reopen observations are lower-activity.

By contrast, month-profile minimum Spearman is negative:
- range: **-0.6503**
- RV15: **-0.6643**
- RV60: **-0.6713**
- tick density: **-0.6294**

Therefore:
- weekday may be retained as a candidate context dimension;
- calendar month is **not promoted as a stable behavioral dimension**.

## 6. Core property — no dominant 1m directional persistence

Global close-to-close 1m sign behavior:
- persistence: **49.33797 %**
- reversal: **50.66203 %**

Complete years:
- 2022: 49.4529 %
- 2023: 49.1011 %
- 2024: 49.4030 %
- 2025: 49.4969 %

The registered metric remains close to 50/50.

This does not establish directional persistence, and it also does not establish a contrarian edge.

## 7. Core property — path efficiency is low and level-stable

Efficiency:
- 15m mean: **0.2574**, median: **0.2237**
- 60m mean: **0.1308**, median: **0.1115**

Complete-year stability:
- efficiency15 mean CV ≈ **0.87 %**
- efficiency60 mean CV ≈ **1.11 %**
- max complete-year decile-CDF distance ≈ **0.0080** / **0.0110**

Thus the distribution level of path efficiency is far more stable than the absolute volatility level.

This means only that net displacement is small relative to travelled path under this metric.

It does **not** prove mean reversion, predictability, or profitability.

## 8. Core property — spread/activity structure exists but spread level drifts

AP5 full-sample observations:
- spread tick-weighted mean: **2.1395**
- tick density mean: **219.99/min**
- spread ↔ minute range Pearson: **-0.3408**
- spread ↔ tick density Pearson: **-0.5911**

Higher-activity/range minutes coexist descriptively with narrower spreads.

Intraday spread ranking has temporal persistence:
- NY-hour minimum Spearman: **0.7757**

But the spread distribution itself shifts materially across years and especially in late-2025/2026 observations.

No provider/exchange cause is inferred.

Downstream work must therefore treat spread/cost context as **time-varying and provider-specific**, not constant.

## 9. Core property — discontinuities are material

AP4 identified 1,605 reopen boundaries.

Absolute discontinuous log move:
- median ≈ **5.99 bps**
- p90 ≈ **32.00 bps**
- p99 ≈ **118.19 bps**
- max ≈ **517.61 bps**

Any downstream context/research procedure must preserve segment/gap boundaries.

The temporal stability of reopen magnitude itself is not qualified by AP6 V0.1.

## 10. Core property — distributions have heavy tails, but tail level is not invariant

Full-sample RV60:
- mean ≈ **21.63 bps**
- median ≈ **16.20 bps**
- p99 ≈ **89.01 bps**
- max ≈ **479.92 bps**

Large tails are clearly present in the historical sample.

Because absolute volatility level drifts materially through time, these exact tail magnitudes are not promoted as timeless constants.

## 11. AP3 expansion/compression interpretation

AP3 absolute RV15 thresholds:
- compression ≤ 4.0381 bps
- expansion ≥ 15.0183 bps

Hour-normalized thresholds:
- compression ≤ 0.6304
- expansion ≥ 1.6570

The 20/60/20 shares are created by the quantile construction.

After hour normalization, annual expansion share still changed strongly across years.

Therefore:
- hour normalization is useful descriptively;
- it does not make the volatility distribution invariant;
- AP3 thresholds are not live/deployable regime rules.

## 12. Historical observation retained but not stability-promoted

AP4 breakout/reentry findings remain useful historical description:
- many 15m/60m boundary breaks re-entered;
- for re-entered events, median delay ≈ 2 minutes and p90 ≈ 9 minutes.

However AP4 uses future observations to label reentry.

AP6 V0.1 deliberately did not stability-test these future labels.

Therefore this behavior remains **historical / hypothesis-generating**, not a stable CORE rule.

## 13. Stable vs variable vs unresolved

### Promoted with temporal evidence
- relative New York intraday volatility/activity shape;
- weekday volatility/activity ordering;
- near-balanced 1m persistence/reversal;
- efficiency15/60 distribution level.

### Promoted as time-varying properties
- absolute volatility level;
- absolute tick-density level;
- spread level/distribution.

### Not promoted
- calendar-month seasonality;
- breakout/reentry stability;
- causal relationships;
- full-sample thresholds as live constants;
- volume/depth/order-flow;
- sub-minute microstructure;
- strategy/edge/PnL.

## 14. Candidate context axes for the next research gate

The CORE permits investigation — not adoption — of:
1. New York time-of-day;
2. weekday;
3. absolute/relative volatility state;
4. time-varying spread and tick-density state;
5. gap/reopen state;
6. efficiency state.

Each remains a **research variable** until tested under the CONTEXT / REGIME RESEARCH contract.

No performance-oriented selection is authorized by this CORE.

## 15. CORE promotion gate

Protocol gate:

- AP0 transformation identified/reproducible: PASS
- gaps not masked: PASS
- metrics documented: PASS
- no strategy calculations: PASS
- temporal stability measured: PASS
- limits/non-qualified data explicit: PASS

## Verdict

**PASS — ASSET BEHAVIORAL PROFILE CORE V0.1.**

The price-core understanding phase is now complete under the registered scope.

The next permissible program frontier is **CONTEXT / REGIME RESEARCH**, beginning with a preflight/research contract — not strategy optimization.
