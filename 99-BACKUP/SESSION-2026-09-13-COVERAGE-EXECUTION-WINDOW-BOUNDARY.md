# SESSION BACKUP — 2026-09-13 — COVERAGE / EXECUTION WINDOW BOUNDARY

## Repository state

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint: `0e0111cc544adae2791da9cb82bb48a0d08fe785`
- Starting branch comparison: identical, ahead 0 / behind 0.

## Prior locked state

- Global coverage envelope: `2018-05-01` → `2026-08-14`.
- Global unresolved candidates: 87.
- `2019-07-03` remains `BLOCKED — IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`.
- Governance rule for irreducible broker gaps remains PASS.
- Calendar executable evidence remains 34 prior PASS tests; no calendar code changed in this boundary block.
- Massive `.bi5` acquisition was and remains forbidden.

## Boundary formalized

New rule:

`04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

The rule separates four actions:

1. continuing later qualification;
2. declaring global coverage PASS;
3. freezing a >=5-year execution window;
4. authorizing massive acquisition.

PASS for one action does not transfer to another.

## Core rule

Later qualification may continue despite earlier BLOCKED dates if those dates remain durably preserved and unchanged.

A future execution window may eventually be admissible with outside global gaps only if:

- it is contiguous;
- spans >=5 calendar years;
- its rationale is versioned and independent of known gaps;
- it was not shifted to avoid a known gap;
- every candidate date inside it is enumerated;
- unresolved inside = 0;
- FAIL inside = 0;
- outside gaps remain visible globally.

A window selected because `2019-07-03` is difficult is explicitly FAIL.

Acquisition remains a separate gate.

## Executable gate and adversarial break

Gate:

`tools/coverage_execution_window_boundary.py`

Tests:

`tests/test_coverage_execution_window_boundary.py`

Observed execution:

```text
..................                                                       [100%]
18 passed in 0.05s
```

Qualification report:

`reports/data-qualification/coverage_execution_window_boundary_qualification.md`

Governance-rule verdict:

**PASS**

Reason:

`BOUNDARY_ACTIONS_SEPARATED_AND_ADVERSARIAL_BYPASSES_REJECTED`

## Application to current state

Application report:

`reports/data-qualification/current_coverage_execution_window_boundary_application.md`

Current decisions:

- `CONTINUE_LATER_QUALIFICATION` → **PASS**
  - `LATER_QUALIFICATION_MAY_CONTINUE_WITH_PRIOR_GAPS_PRESERVED`
- `DECLARE_GLOBAL_COVERAGE_PASS` → **BLOCKED**
  - `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`
- `FREEZE_EXECUTION_WINDOW` → **BLOCKED**
  - `EXECUTION_WINDOW_NOT_DEFINED`
- `AUTHORIZE_MASSIVE_ACQUISITION` → **BLOCKED**
  - `EXECUTION_WINDOW_NOT_FROZEN`

Therefore qualification may proceed into 2020+ without resolving or hiding `2019-07-03`, while all stronger claims remain blocked.

## Anti-bypass conclusion

Do not:

- call global coverage PASS;
- choose `2020+` as an execution window merely to dodge the 2019 gap;
- delete individual dates from a contiguous window;
- infer acquisition permission from qualification continuation;
- rewrite the global unresolved count to match only a preferred subset.

## Exactly one next governed action

Proceed with chronological **2020 candidate-date qualification**, starting with `2020-01-01`, while preserving `2019-07-03` as an explicit outside-frontier BLOCKED record. Do not freeze an execution window and do not begin massive `.bi5` acquisition.
