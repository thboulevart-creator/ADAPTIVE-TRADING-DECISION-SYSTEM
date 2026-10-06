# SMF-AP1-M03-02-R1-SI-02 — FINAL HUMAN SCIENTIFIC ADJUDICATION CLOSURE

Status: HUMAN_SCIENTIFIC_ADJUDICATION_CLOSED

Closure parent:
- HEAD: `59b8c09c5623e6adeece5cd951238059ffb3d3af`
- TREE: `fec420083cfea7eac86b777a0e01d14ae0f00b84`

Protected package:
- SI01 candidate set: `8f85f301380d192e7a8bbc225e39d080d76d78ac`
- SI01 final receipt: `f5eeae8b3806bd2aff0fb16d30d1ea139f5c6d89`
- SI02 decision packet: `69344c38638361ef7e027d28c34b8c3ff0416949`
- SI02 opening receipt: `9576b43fef21734da1813e4de2ff2e17055545c6`

All concurrent drift since SI02 opening was classified NON_MATERIAL; no protected SI01/SI02/M03/AP1/DATA-02 surface changed.

## Human decisions

### SI01-C01 — ADOPT
GLOBAL_UPPER_QUANTILE_DISPERSION_DIFFERENCES

Within the admitted corpus, minute_range and tick_count show substantially larger upper-quantile separation from their medians than spread_mean.

### SI01-C02 — ADOPT
NEW_YORK_INTRADAY_DISTRIBUTIONAL_HETEROGENEITY

The admitted corpus exhibits large descriptive differences by New York local hour; the 09–10 buckets have high activity/range quantiles and much lower spread_mean quantiles than several evening/overnight buckets.

### SI01-C03 — ADOPT
NEW_YORK_WEEKDAY_DISTRIBUTIONAL_HETEROGENEITY

Within the admitted corpus, weekday buckets differ descriptively; Friday has higher tick_count and minute_range quantiles than Sunday, while Saturday has no admitted observations.

### SI01-C04 — AMEND AND ADOPT
Adopted name: UTC_YEAR_DISTRIBUTIONAL_VARIATION_CANDIDATE

Within the admitted 2021-05-25 through 2026-05-24 corpus, the predeclared UTC_YEAR bucket distributions differ descriptively across years for minute_range, tick_count, and spread_mean. The 2025-2026 spread_mean central quantiles differ sharply from earlier year buckets while p99 remains near prior-year levels. This is a retrospective descriptive variation candidate only; formal temporal instability, nonstationarity, structural break, cause, persistence, and generalization remain untested.

### SI01-C05 — ADOPT
PREDECLARED_TIME_SUPPORT_IS_INCOMPLETE

The admitted corpus has incomplete support across the full predeclared New York calendar grid; empty buckets are explicit rather than numerically imputed.

## Binding scope
RETROSPECTIVE / DESCRIPTIVE / EMPIRICAL / FRAME-BOUND.

No causality, statistical significance, generalization, predictive/economic edge, profitability, strategy validation, trading signal, trading authority, or capital authority is established.

No downstream method is authorized. M01 and M10 remain closed.

Next logical frontier only:
M01 — EXACT TEMPORAL / REGIME STABILITY CLAIM + ESTIMAND FREEZE

STOP SI-02 = REACHED.
