# EXECUTION WINDOW SELECTION RULE V1 — ADVERSARIAL QUALIFICATION

Contract under test:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Rule source:

`04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`

Rule creation commit preceding this qualification/application:

`65adaa6bb22843c15d48e813326c80e7001c8c4a`

## Verdict

**PASS**

Reason:

`SELECTION_RULE_IS_DETERMINISTIC_GAP_BLIND_RESULT_BLIND_AND_BOUNDARY_INDEPENDENT`

This PASS qualifies the selection rationale only. It does not freeze any resulting candidate window.

## Adversarial attacks

### Attack 1 — use the gap map to choose the start

Attempt: move the start to the first date after a troublesome unresolved holiday.

Expected rejection: the rule accepts only `coverage_start`, `coverage_end`, and the fixed five-calendar-year horizon. Gap dates are forbidden inputs.

Result: **REJECTED**.

### Attack 2 — choose the five-year span with the fewest unresolved dates

Attempt: enumerate many five-year spans, count unresolved dates, select the minimum-gap span.

Expected rejection: this makes the outcome map a selection input and is explicitly forbidden.

Result: **REJECTED**.

### Attack 3 — snap to complete calendar years

Attempt: change mechanically produced dates to Jan-1 / Dec-31 for reporting convenience.

Expected rejection: the rule anchors to the governed `coverage_end` and subtracts exactly five calendar years. Convenience cannot alter the dates.

Result: **REJECTED**.

### Attack 4 — shorten below five years because acquisition is expensive

Attempt: choose 3 or 4 years to reduce download time.

Expected rejection: conflicts with the pre-existing minimum five-year research gate.

Result: **REJECTED**.

### Attack 5 — extend only because extra years have fewer gaps

Attempt: change to six/seven years after seeing the calendar gap distribution.

Expected rejection: outcome-driven duration change is forbidden. A robustness extension is a separate experiment, not a replacement primary window selected post-outcome.

Result: **REJECTED**.

### Attack 6 — shift the end backward to avoid recent gaps

Attempt: stop at a prior complete year/month.

Expected rejection: `candidate_end = coverage_end`; the already-governed terminal date is the anchor.

Result: **REJECTED**.

### Attack 7 — delete individual holidays inside the candidate interval

Attempt: preserve outer dates but omit troublesome days.

Expected rejection: the interval must be contiguous and manual exclusions are forbidden by both this rule and `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`.

Result: **REJECTED**.

### Attack 8 — move the window after seeing PnL/drawdown

Attempt: backtest several windows and retain the best.

Expected rejection: strategy performance is a forbidden selection input and the baseline protocol requires the execution window fixed before results are observed.

Result: **REJECTED**.

### Attack 9 — move the window after seeing native-tick availability

Attempt: shift boundaries toward periods that download more easily.

Expected rejection: sub-period tick availability is a forbidden selection input. Missing required data blocks qualification; it does not move the scientific window.

Result: **REJECTED**.

### Attack 10 — manipulate OOS to remove unresolved dates

Attempt: move problematic calendar dates into/out of an OOS segment or use the OOS split to exclude them from the outer window.

Expected rejection: OOS is a separate inner split and cannot alter outer-window membership.

Result: **REJECTED**.

### Attack 11 — insufficient governed history

Attempt: apply the rule where `coverage_end - 5 calendar years < coverage_start`.

Expected behavior: do not invent or extend history; return BLOCKED.

Result: **SAFE BY CONTRACT** — `INSUFFICIENT_GOVERNED_HISTORY_FOR_PRIMARY_WINDOW`.

### Attack 12 — leap-day ambiguity

Attempt: make calendar-year subtraction non-deterministic when the anchor is Feb 29.

Expected behavior: map to Feb 28 in the non-leap target year.

Result: **DETERMINISTIC BY CONTRACT**.

## Independence assessment

The rule was versioned before applying it to the current envelope in the next artifact.

Its formula does not require and must not inspect:

- the 87 global unresolved dates;
- annual gap counts;
- the first unresolved date;
- strategy results;
- tick availability distribution;
- download speed or convenience by period.

The reason for five years is inherited from the already-PASS baseline protocol, and the reason for anchoring at the end is recency relative to the already-governed coverage envelope.

Therefore the selection rationale satisfies the independence requirement of `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`.

## Qualified rule verdict

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

Next governed step after this PASS: apply the rule mechanically to the current envelope and measure the resulting candidate window without freezing it.
