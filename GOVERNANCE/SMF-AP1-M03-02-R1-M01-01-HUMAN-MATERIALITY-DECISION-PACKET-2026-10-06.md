# M01-01 — HUMAN MATERIALITY PARAMETER ADJUDICATION REQUIRED

Status: M01_BLOCKED_PENDING_HUMAN_PARAMETER_ADJUDICATION

The M01 claim, population, complete/partial-year policy, 11 quantile-series estimands, 33 adjacent-year contrasts, strict H0/H1 semantics, failure-mode map, multiplicity classification, and dependency map are determined.

The only material blocker is the materiality boundary required to distinguish a merely detectable/numerical difference from materially relevant temporal variation.

## Why this cannot be chosen automatically

The M03 corpus has already been exposed. Choosing a threshold by looking for a value that classifies the observed year differences favorably would be post-hoc threshold optimization.

No upstream human-adopted threshold exists.

Therefore no M01 freeze and no M10 execution readiness are permitted yet.

## Human decisions required

### Decision M01-MAT-01 — Effect scale

Choose exactly one:

A — ABSOLUTE_METRIC_UNITS

Materiality is evaluated on:
|q[m,p,b] - q[m,p,a]|

This requires metric/quantile-specific thresholds because tick_count, minute_range and spread_mean have different units/scales.

B — SYMMETRIC_RELATIVE_CHANGE

Materiality is evaluated on:
R[m,p,a,b] =
2 * |q[m,p,b] - q[m,p,a]|
/
(|q[m,p,b]| + |q[m,p,a]|)

If both denominator terms are zero:
R is undefined and that contrast is BLOCKED, not imputed.

This scale is dimensionless and symmetric in adjacent years, but adopting it is itself a human methodological choice.

C — DUAL_BOUND

Use both an absolute and a symmetric-relative bound under an explicitly chosen boolean rule:
BOTH_REQUIRED
or
EITHER_SUFFICIENT.

This is more complex and must be justified as protecting a distinct failure mode.

### Decision M01-MAT-02 — Thresholds

After MAT-01 is selected, provide the exact threshold value(s).

No default threshold is authorized.

For ABSOLUTE_METRIC_UNITS:
provide exact thresholds at least by metric, and state whether one threshold applies to all quantiles of that metric or whether each (metric,p) gets its own threshold.

For SYMMETRIC_RELATIVE_CHANGE:
provide either:
- one common dimensionless threshold for all 11 claim units; or
- exact metric-specific / metric×quantile thresholds.

For DUAL_BOUND:
provide both sets.

### Decision M01-MAT-03 — Claim-unit decision rule

The preregistered scientific unit is each (metric, quantile) series across 2022-2025.

Choose exactly one:

A — ANY_ADJACENT_MATERIAL_SHIFT
A claim unit is materially temporally varying if at least one of its three adjacent-year contrasts exceeds the adopted bound.

B — ALL_ADJACENT_MATERIAL_SHIFT
A claim unit is materially temporally varying only if all three adjacent-year contrasts exceed the adopted bound.

C — PREDECLARED_COUNT_K
Provide exact K ∈ {1,2,3}; a claim unit is materially temporally varying if at least K of the three adjacent-year contrasts exceed the bound.

No global cross-metric pass/fail is authorized. Eleven claim units remain separate.

## Not being decided here

This adjudication does not authorize M10, M04, M05, M08, M09, M11, any new M03/AP1 execution, backtest, OOS, trading or capital.

After these three parameter decisions, M01-01 may resume solely to incorporate the human materiality boundary, freeze the exact M01 contract, qualify/persist it, and STOP.
