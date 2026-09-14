# RECOVERY CHECKPOINT — 14 SEPTEMBRE 2026 — EXECUTION-WINDOW CANDIDATE DEFINED, NOT FROZEN

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Previous checkpoint / selection-rule session start HEAD:** `0f9a56e0fb8914f562d85eaa5ac32c107213a61a`
- **Global research envelope:** `2018-05-01` → `2026-08-14`
- **Chronological calendar qualification:** COMPLETE TO ENVELOPE END
- **Global calendar accounting:** `111 candidates / 24 resolved / 87 unresolved / 0 FAIL`
- **Global cross-year accounting audit:** PASS
- **Primary execution-window candidate:** `2021-08-14` → `2026-08-14`
- **Candidate window frozen:** NO
- **Candidate window state:** `68 candidates / 1 resolved / 67 unresolved / 0 FAIL`
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized
- **Latest observed executable calendar tests:** `34 PASS`

## 2. DURABLE ARTIFACTS CREATED IN THIS STEP

### Gap-independent window-selection rule

`04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`

Contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Creation commit:

`65adaa6bb22843c15d48e813326c80e7001c8c4a`

### Adversarial qualification of the selection rule

`reports/data-qualification/execution_window_selection_rule_qualification.md`

Commit:

`491ab7b9e3bd8aac4d5dab01d5650ec638ebdd60`

Verdict:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

### Mechanical candidate-window application

`reports/data-qualification/execution_window_candidate_v1.md`

Commit:

`ae83ea08c256d2fdc3b852afd51a4cb2ed7dabe0`

### Current boundary application

`reports/data-qualification/current_coverage_execution_window_boundary_application.md`

Update commit:

`e6f859bb1d43aab37fd51e62efc91824b07d011e`

### Durable session backup

`99-BACKUP/SESSION-2026-09-14-EXECUTION-WINDOW-SELECTION.md`

Commit:

`3a63bff65f5141828179fc22aede752e483f5e55`

## 3. MANDATORY RECOVERY ORDER

Before substantive continuation:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-14-EXECUTION-WINDOW-SELECTION.md`
4. `04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`
5. `reports/data-qualification/execution_window_selection_rule_qualification.md`
6. `reports/data-qualification/execution_window_candidate_v1.md`
7. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
8. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
9. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
10. compare active branch against this checkpoint final HEAD before writing anything.

Do not reconstruct annual 2019–2026 research from conversation history.

## 4. LOCKED GLOBAL STATE

Global cross-year audit report:

`reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`

Verdict:

**PASS — `ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT`**

This is accounting-integrity PASS only.

Global state remains:

- candidates: **111**
- resolved: **24**
- unresolved: **87**
- FAIL: **0**
- orphan special evidence: **0**
- contradictory overlap: **0**
- evidence-shape errors: **0**
- hidden/reclassified prior gaps: **0**
- prior gaps preserved: **YES**

Global coverage declaration remains:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

First global unresolved remains:

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

## 5. LOCKED WINDOW-SELECTION RULE

Primary rule:

**Use the most recent contiguous five-calendar-year span ending at the already-governed coverage end.**

Scientific/methodological basis:

- existing baseline protocol requires at least five years;
- baseline performs no parameter calibration/optimization;
- execution window must be fixed before results are observed;
- anchoring to the governed terminal date maximizes temporal relevance;
- exactly five years satisfies the primary qualification horizon without silently turning the first baseline into a larger robustness-extension experiment;
- older history remains available for later robustness/historical-extension challenges.

Allowed rule inputs:

- `coverage_start`;
- `coverage_end`;
- fixed minimum horizon = 5 calendar years.

Forbidden rule inputs:

- unresolved/FAIL dates;
- gap counts or distribution;
- strategy results;
- tick availability by sub-period;
- acquisition/download convenience;
- ease or difficulty of proving specific dates.

The rule MUST NOT be rewritten because its mechanically selected window contains many gaps.

## 6. RULE ADVERSARIAL QUALIFICATION

The following bypasses were explicitly rejected:

- start after a known gap;
- select the five-year span with the fewest gaps;
- snap to complete calendar years for convenience;
- shorten below five years to reduce acquisition cost;
- extend because additional years happen to contain fewer gaps;
- shift end backward to avoid recent gaps;
- remove individual dates inside the interval;
- move boundaries after observing PnL/drawdown;
- move boundaries after observing tick availability;
- manipulate OOS to remove outer-window dates.

Rule verdict remains:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

This PASS does not freeze the resulting window.

## 7. MECHANICALLY SELECTED PRIMARY CANDIDATE

Applying the qualified rule only after it was versioned gives:

- **start:** `2021-08-14`
- **end:** `2026-08-14`
- **duration:** exactly 5 calendar years
- **contiguous:** YES
- **manual exclusions:** NO
- **selection rationale versioned:** YES
- **selection independent of known gaps:** YES
- **shifted to avoid known gap:** NO
- **window frozen:** NO

This candidate MUST NOT be moved merely to reduce evidence gaps.

## 8. IN-WINDOW CALENDAR ACCOUNTING

The candidate contains exactly **68** generated special-session candidates:

- 2021 partial (`2021-08-14` onward): 6
- 2022: 12
- 2023: 13
- 2024: 14
- 2025: 15
- 2026 through `2026-08-14`: 8

Arithmetic:

`6 + 12 + 13 + 14 + 15 + 8 = 68`

Resolved inside candidate:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`

In-window state:

- candidates: **68**
- resolved: **1**
- unresolved/BLOCKED: **67**
- FAIL: **0**

Global unresolved outside candidate:

`87 - 67 = 20`

Those 20 remain globally visible and BLOCKED. They are not resolved by being outside the primary candidate.

## 9. CURRENT BOUNDARY DECISIONS

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

### Global coverage

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

### Window-selection rationale

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

### Window candidate defined

**PASS**

The exact candidate exists and is independently justified.

### Freeze execution window

**BLOCKED — `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`**

The prior temporary reason `EXECUTION_WINDOW_NOT_DEFINED` is obsolete.

The candidate is now defined, but it contains **67 unresolved dates**.

### Massive native `.bi5` acquisition

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

### Real backtest

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

No `.bi5` acquisition or real backtest may begin.

## 10. OOS BOUNDARY

The window-selection rule selects the outer five-year candidate only.

The OOS split remains a separate downstream freeze required by `docs/03.1.2-MOMENTUM-V1-BASELINE-PROTOCOL.md`.

OOS MUST NOT be used to remove unresolved dates from the outer candidate.

No OOS dates have been frozen in this step.

## 11. CRITICAL ANTI-LOOP / ANTI-CHERRY-PICK RULES

The 67 in-window BLOCKED dates were already investigated during the annual/segment campaigns under the currently known evidence routes.

Therefore:

- do NOT repeat the same generic date-by-date holiday searches;
- do NOT reopen a BLOCKED date without materially new evidence or a materially new admissible evidence route;
- do NOT shift, shorten, extend, or otherwise manipulate `2021-08-14 → 2026-08-14` because 67 gaps remain;
- do NOT redefine the global envelope to manufacture PASS;
- do NOT download `.bi5`;
- do NOT start a real backtest.

Previously locked anti-false-PASS lessons remain in force, including:

- generic broker context + exchange timing is insufficient without the explicit PASS-C chain;
- exchange evidence alone never becomes Dukascopy truth;
- current Trading Breaks route limitations are absence of proof, not session evidence;
- other-year or adjacent-date schedules never substitute for target-date proof.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Determine whether a materially new admissible broker-origin historical-session evidence route exists that can resolve the 67 in-window BLOCKED candidates without changing the selected boundaries.**

This next investigation must target a genuinely new evidence class/route, not repeat the exhausted annual searches.

Candidate route classes include, if actually demonstrable:

- official historical Dukascopy Trading Breaks dataset;
- historical Trading Breaks widget/API/backend payload;
- broker-origin historical export/archive with verified provenance;
- another official Dukascopy historical session record capable of binding target date + `USATECH.IDX/USD` + special hours.

Required decision:

- if a materially new admissible route exists: formalize and adversarially qualify that route before using it to reopen dates;
- if no materially new admissible route can be established: keep **`FREEZE_EXECUTION_WINDOW = BLOCKED — EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`** and do not alter the selection rule to escape the result.

Do not download `.bi5`. Do not start a real backtest.
