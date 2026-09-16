# EXECUTION WINDOW SELECTION RULE — V1

Contract: `EXECUTION_WINDOW_SELECTION_RULE_V1`

## 1. Purpose

Define the primary execution/backtest-window candidate **before** using calendar gaps, data holes, strategy performance, or any other outcome to choose boundaries.

This rule selects a candidate window only. It does **not** freeze the window, authorize `.bi5` acquisition, or authorize a real backtest.

## 2. Upstream constraints already locked

The rule is derived from existing project requirements, not from the observed gap map:

1. `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md` requires at least five years before a real backtest is accepted as a qualification result.
2. The baseline performs no development/calibration and no parameter optimization.
3. The execution window must be fixed before results are observed.
4. OOS remains a separate untouched evaluation segment whose split is fixed before execution.
5. `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` requires a contiguous window of at least five calendar years with a versioned rationale independent of known unresolved/FAIL dates.

## 3. Selection principle

Primary rule:

**Use the most recent contiguous five-calendar-year span ending at the already-governed coverage end.**

Rationale:

- five calendar years is the pre-existing minimum qualification horizon;
- the primary baseline has no calibration/optimization reason to require a longer initial execution span;
- anchoring at the latest already-governed date maximizes temporal relevance to intended future deployment;
- using the minimum qualifying horizon limits the first irreversible native-tick acquisition to the amount required by the frozen baseline gate;
- older history remains available as a later robustness / historical-extension challenge rather than being silently discarded;
- none of these reasons depends on where calendar gaps, missing data, or favorable/unfavorable strategy results happen to fall.

## 4. Deterministic formula

Inputs allowed:

- `coverage_start`
- `coverage_end`
- fixed minimum horizon = `5 calendar years`

Inputs forbidden:

- unresolved calendar dates;
- FAIL dates;
- distribution of holiday gaps;
- tick availability by sub-period;
- download convenience by sub-period;
- strategy PnL / drawdown / win rate / regime results;
- spread/cost results;
- any knowledge of which dates are easier to prove.

Selection:

1. `candidate_end = coverage_end`
2. `candidate_start = candidate_end shifted backward by exactly 5 calendar years`
3. the interval is contiguous; no date may be manually removed;
4. if the calculated start precedes `coverage_start`, verdict is `BLOCKED — INSUFFICIENT_GOVERNED_HISTORY_FOR_PRIMARY_WINDOW`;
5. leap-day handling follows calendar-year subtraction semantics: if a Feb-29 anchor must be mapped into a non-leap target year, use Feb-28.

## 5. Why the rule uses exactly five years

The project requirement is `at least five years`, not `all available history`.

For the first baseline experiment, exactly five years is chosen because:

- it satisfies the locked minimum research horizon;
- the baseline itself has no parameter-calibration phase requiring extra development history;
- the primary purpose is first reproducible qualification, not maximal historical stress coverage;
- any extension beyond the primary five-year window is a separate robustness experiment and must not be mixed into the baseline after results are seen.

This choice MUST NOT be justified by calendar completeness. A five-year candidate remains the candidate even if it contains many unresolved dates.

## 6. OOS separation

This rule selects only the outer execution-window candidate.

It does not choose the OOS split.

The exact OOS split must be frozen separately before execution and may not be moved after results are observed. OOS design MUST NOT be used to delete unresolved calendar dates from the outer execution window.

## 7. Anti-cherry-pick invariants

After this rule is versioned, the following are forbidden without a separately governed rule-version change whose rationale is independent of observed outcomes:

- moving the start date because an unresolved holiday lies near the boundary;
- snapping boundaries to January 1 / December 31 merely for convenience;
- shifting the end date to avoid a recent unresolved date;
- extending or shortening the window because one version has fewer calendar gaps;
- removing individual dates from inside the window;
- changing the window after seeing backtest performance;
- changing the window after seeing tick-download availability;
- treating an outside-window gap as resolved.

## 8. Application sequence

Only after this rule has been versioned:

1. apply it mechanically to the governed envelope;
2. persist the resulting exact candidate dates;
3. enumerate every generated calendar candidate inside that interval;
4. count in-window PASS / FAIL / BLOCKED states;
5. apply `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`;
6. freeze only if the freeze action itself returns PASS.

No `.bi5` acquisition or real backtest is authorized by rule selection alone.

## 9. Rule verdict semantics

The rule itself may receive PASS only if adversarial review confirms that its boundaries are deterministic from allowed upstream inputs and cannot be influenced by gap/performance outcomes.

A PASS for this selection rule means only:

`WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`

It does not mean the resulting candidate window is admissible for freeze.
