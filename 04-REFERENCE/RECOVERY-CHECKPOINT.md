# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `0e0111cc544adae2791da9cb82bb48a0d08fe785`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Execution/backtest window frozen:** no
- **Massive native `.bi5` acquisition:** forbidden
- **Global coverage verdict:** BLOCKED
- **Global unresolved candidates:** 87
- **First unresolved:** `2019-07-03`

Latest boundary artifacts:

- rule: `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
  - commit `39b1647c8f0458a436cfcf2f41f058b05d2927b9`
- executable gate: `tools/coverage_execution_window_boundary.py`
  - commit `e0cc3264745809bb455936b297f1974e0471fee1`
- adversarial tests: `tests/test_coverage_execution_window_boundary.py`
  - commit `c028f2caa123ef0e2bcae2d0b7eaa40e5ae902e9`
- qualification report: `reports/data-qualification/coverage_execution_window_boundary_qualification.md`
  - commit `9b3ada180ff7d84e35cee888a5b0424fd070c63e`
- current-state application: `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
  - commit `3b9cf340240ebec6ebc2905462857dd6a1eaa068`
- durable backup: `99-BACKUP/SESSION-2026-09-13-COVERAGE-EXECUTION-WINDOW-BOUNDARY.md`
  - commit `f790cd5df363d84281efbf4fa97e8c477e62d157`

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-COVERAGE-EXECUTION-WINDOW-BOUNDARY.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2019_07_03_gap_application.md`
8. `reports/data-qualification/coverage_execution_window_boundary_qualification.md`
9. `reports/data-qualification/current_coverage_execution_window_boundary_application.md`
10. `tools/dukascopy_usatech_calendar.py`
11. `tools/dukascopy_usatech_calendar_coverage.py`
12. boundary/calendar tests and actual GitHub state

## 3. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.
- No OHLC M1, interpolation, synthetic ticks, or substituted ticks are authorized.

## 4. CALENDAR STATE

The calendar contains **24** date-specific special-session evidence records inside the global coverage envelope.

Latest observed calendar test state remains:

- 28 historical/current tests PASS;
- 6 late-2019 targeted tests PASS;
- combined prior observed execution: **34 passed**.

No calendar/test classification changed in the boundary block, so calendar tests/coverage were not rerun merely to generate a newer timestamp.

Latest observed coverage remains:

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **24**
- `special_session_evidence_dates`: **24**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **87**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

## 5. 2019-07-03 LOCKED STATE

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION` remains:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

The irreducible-gap governance rule itself remains PASS, but the date remains BLOCKED. Do not conflate method qualification with date qualification.

Do not repeat generic witness searches unless materially new evidence appears.

## 6. COVERAGE / EXECUTION-WINDOW BOUNDARY RULE

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

The rule separates four independent actions:

1. `CONTINUE_LATER_QUALIFICATION`
2. `DECLARE_GLOBAL_COVERAGE_PASS`
3. `FREEZE_EXECUTION_WINDOW`
4. `AUTHORIZE_MASSIVE_ACQUISITION`

PASS for one action does not imply PASS for another.

### Global coverage envelope

The global envelope is a research/qualification superset. Historical BLOCKED dates remain visible and unchanged until resolved. Later research cannot silently delete or reclassify them.

### Future execution window

A future execution window may be narrower than the global envelope, but to be admissible it must:

- be exact and versioned;
- be contiguous;
- span at least five calendar years;
- have a versioned selection rationale independent of known gaps;
- not be shifted/shortened merely to avoid a known BLOCKED/FAIL date;
- have every calendar candidate inside it enumerated;
- have zero unresolved and zero FAIL candidates inside it;
- preserve outside gaps in global reports.

A window selected as `2020+` **because** `2019-07-03` is BLOCKED is FAIL.

## 7. ADVERSARIAL QUALIFICATION OF BOUNDARY

Observed local execution of the versioned gate and attacks:

```text
..................                                                       [100%]
18 passed in 0.05s
```

Attacks covered:

- false global PASS;
- hidden/reclassified prior gaps;
- cherry-picked window boundaries;
- manual date deletion;
- sub-five-year windows;
- unresolved/FAIL inside a proposed window;
- unversioned/non-independent window rationale;
- acquisition before freeze;
- misuse of qualification-continuation PASS as acquisition authorization;
- eventual acquisition path requiring separate explicit gates.

### Boundary-rule verdict

**PASS**

Reason:

`BOUNDARY_ACTIONS_SEPARATED_AND_ADVERSARIAL_BYPASSES_REJECTED`

This PASS certifies only the governance boundary.

## 8. APPLICATION TO CURRENT STATE

Current action verdicts are:

### `CONTINUE_LATER_QUALIFICATION`

**PASS**

Reason:

`LATER_QUALIFICATION_MAY_CONTINUE_WITH_PRIOR_GAPS_PRESERVED`

Therefore chronological qualification may advance into **2020+** while `2019-07-03` remains explicitly BLOCKED.

### `DECLARE_GLOBAL_COVERAGE_PASS`

**BLOCKED**

Reason:

`GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`

The global envelope remains BLOCKED with 87 unresolved candidates.

### `FREEZE_EXECUTION_WINDOW`

**BLOCKED**

Reason:

`EXECUTION_WINDOW_NOT_DEFINED`

No exact future execution window or independent versioned selection rationale exists yet. Do not invent `2020+` as a frozen window merely because it excludes the 2019 gap.

### `AUTHORIZE_MASSIVE_ACQUISITION`

**BLOCKED**

Reason:

`EXECUTION_WINDOW_NOT_FROZEN`

Massive `.bi5` acquisition remains forbidden.

## 9. LOCKED DISTINCTION

The current truth is simultaneously:

- **boundary governance rule: PASS**;
- **permission to continue 2020+ qualification: PASS**;
- **2019-07-03: BLOCKED**;
- **global coverage: BLOCKED**;
- **execution-window freeze: BLOCKED**;
- **massive acquisition: BLOCKED**.

No one of these verdicts may be substituted for another.

## 10. ANTI-BYPASS INVARIANTS

Do not:

- mark `2019-07-03` resolved without new qualifying evidence;
- call global coverage PASS while any candidate is unresolved;
- choose or move a future window merely to avoid a known gap;
- manually delete dates inside a contiguous window;
- redefine the global envelope to obtain PASS;
- infer acquisition permission from permission to continue qualification;
- begin massive acquisition before a separate future window is frozen and all its mandatory gates are PASS.

## 11. EXACTLY ONE NEXT GOVERNED ACTION

**Continue chronological calendar qualification into 2020, beginning with `2020-01-01`, while preserving `2019-07-03` as an explicit BLOCKED global-envelope record. Do not freeze an execution window and do not begin massive `.bi5` acquisition.**
