# SMF-AP1-M03-02-R1-SI-01 — Bounded Scientific Interpretation

Status candidate: QUALIFIED_FOR_HUMAN_SCIENTIFIC_ADJUDICATION

## Scope
This report interprets only the existing qualified M03 output within RETROSPECTIVE / DESCRIPTIVE / EMPIRICAL / FRAME-BOUND scope. It does not execute M03, AP1, another SMF method, a backtest, OOS, paper/live trading, or capital.

## A. Direct execution facts
- Qualified M03 output SHA-256: 7d4369cdfab545f0edb94b93ad9d1d1070e6afa35a1000376af55d9c10943a9e
- 1,709,180 admitted minutes
- 230 predeclared buckets
- M03 procedure: ECDF + empirical quantiles
- AP1↔M03 parity: PASS; 1925 PASS; 0 FAIL; 165 NOT_COMPARABLE; max abs diff 0.0
- 165 NOT_COMPARABLE entries are exactly explained by 55 empty time buckets x 3 metrics.

## B. Descriptive empirical observations
Global quantiles:
- tick_count: p50 184; p90 443; p99 621
- minute_range: p50 4.7400; p90 14.2490; p95 19.2340; p99 33.31121
- spread_mean: p50 3.34246; p90 3.43136; p95 3.43800; p99 3.45010

Exploratory scans over predeclared buckets show:
- New York hour: large activity/range contrasts, with 09–10 among the highest observed activity/range buckets and materially lower spread_mean quantiles than several evening/overnight buckets.
- Weekday: Friday (Python weekday 4) has higher observed tick_count/minute_range quantiles than Sunday (6); Saturday (5) is empty.
- UTC year: distributions vary strongly across years. The spread_mean center changes sharply in 2025–2026 while its p99 remains near earlier levels; minute_range and tick_count also vary across years.
- Temporal support is incomplete in the New York calendar grid: hour 17 is empty, Saturday is empty, and 53 weekday-hour cells are empty.

## C. Scientific interpretation candidates
Five candidates are recorded in the canonical candidate-set JSON. Four are explicitly exploratory because extrema/large contrasts were selected after observing all predeclared buckets.

The highest-priority next scientific question is the temporal-stability candidate. If human-adopted as a question worth testing, the directly relevant method is M10 — PREDECLARED TEMPORAL / REGIME STABILITY, preceded by an exact M01 claim/estimand freeze. M10 is not opened by SI-01.

## D. Claims not supported / still unknown
SI-01 does not establish causality, statistical significance, formal nonstationarity, predictive power, generalization, economic edge, profitability, strategy validity, trading signal, trading authority, or capital authority.

No candidate in this report is automatically adopted as a scientific finding.
