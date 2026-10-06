# SMF-AP1-M03-02-R1-M01-01 — FINAL CLOSURE

Status: M01_TEMPORAL_STABILITY_CLAIM_ESTIMAND_FROZEN

The previously unresolved materiality boundary is now human-adopted and frozen:

- effect scale: SYMMETRIC_RELATIVE_CHANGE
- threshold scope: COMMON_TO_ALL_11_CLAIM_UNITS
- threshold: 0.20
- claim-unit rule: ANY_ADJACENT_MATERIAL_SHIFT
- zero denominator: UNDEFINED / BLOCKED
- global cross-metric pass/fail: FORBIDDEN

Decision precedence:
1. if any required adjacent contrast is undefined/blocked, the claim unit is BLOCKED;
2. otherwise, if at least one adjacent contrast has R >= 0.20, the claim unit is MATERIAL_TEMPORAL_VARIATION;
3. otherwise, it is NO_MATERIAL_TEMPORAL_VARIATION_DETECTED.

The primary frame remains complete UTC years 2022-2025 only, with 2021 and 2026 retained as sensitivity/descriptive context. There are 11 metric×quantile claim units and 33 preregistered adjacent-year contrasts.

Claim origin remains EXPLORATORY_RESULT_DERIVED. Any future M10 use on the already exposed corpus has at most EXPLORATORY_DIAGNOSTIC_TEMPORAL_STABILITY_EVIDENCE semantics.

M01 is frozen. M10 is not authorized or executed. No other SMF method, new M03/AP1, backtest, OOS, paper/live trading, or capital use is authorized by this closure.

STOP M01-01 = REACHED.
