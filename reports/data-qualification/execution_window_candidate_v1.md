# EXECUTION WINDOW CANDIDATE V1 — RULE APPLICATION

## Status

Candidate window: **DEFINED / NOT FROZEN**

Selection contract:

`EXECUTION_WINDOW_SELECTION_RULE_V1`

Selection-rule source:

`04-REFERENCE/EXECUTION-WINDOW-SELECTION-RULE.md`

Rule creation commit — before application:

`65adaa6bb22843c15d48e813326c80e7001c8c4a`

Adversarial qualification commit — before application:

`491ab7b9e3bd8aac4d5dab01d5650ec638ebdd60`

Rule qualification verdict:

**PASS — `WINDOW_SELECTION_RATIONALE_IS_VERSIONED_AND_GAP_INDEPENDENT`**

## 1. Allowed upstream inputs

Governed coverage envelope:

- `coverage_start = 2018-05-01`
- `coverage_end = 2026-08-14`

Fixed primary horizon:

- `5 calendar years`

No gap count, unresolved date, performance result, or sub-period data-availability result is an input to the rule.

## 2. Mechanical boundary derivation

Rule:

1. `candidate_end = coverage_end`
2. `candidate_start = candidate_end - 5 calendar years`

Therefore:

- **candidate start:** `2021-08-14`
- **candidate end:** `2026-08-14`
- **contiguous:** YES
- **manual date exclusion:** NO
- **duration:** exactly 5 calendar years
- **selection rationale versioned:** YES
- **selection independent of known gaps:** YES
- **shifted to avoid a known gap:** NO
- **execution window frozen:** NO

This is now the primary candidate produced by the rule. It MUST NOT be moved because of the evidence counts below.

## 3. Candidate calendar enumeration

Calendar generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob used by the global audit:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

Candidate call conceptually equivalent to:

`candidate_special_dates(start=date(2021,8,14), end=date(2026,8,14))`

Exactly **68** candidate dates lie inside the mechanically selected window.

### 2021 partial window — 6

1. `2021-09-06 — LABOR_DAY`
2. `2021-11-25 — THANKSGIVING_DAY`
3. `2021-11-26 — THANKSGIVING_FRIDAY`
4. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
5. `2021-12-24 — CHRISTMAS_OBSERVED`
6. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`

### 2022 — 12

7. `2022-01-17 — MARTIN_LUTHER_KING_DAY`
8. `2022-02-21 — PRESIDENTS_DAY`
9. `2022-04-15 — GOOD_FRIDAY`
10. `2022-05-30 — MEMORIAL_DAY`
11. `2022-06-20 — JUNETEENTH_OBSERVED`
12. `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
13. `2022-07-04 — INDEPENDENCE_DAY_OBSERVED`
14. `2022-09-05 — LABOR_DAY`
15. `2022-11-24 — THANKSGIVING_DAY`
16. `2022-11-25 — THANKSGIVING_FRIDAY`
17. `2022-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION`
18. `2022-12-26 — CHRISTMAS_OBSERVED`

### 2023 — 13

19. `2023-01-02 — NEW_YEARS_OBSERVED`
20. `2023-01-16 — MARTIN_LUTHER_KING_DAY`
21. `2023-02-20 — PRESIDENTS_DAY`
22. `2023-04-07 — GOOD_FRIDAY`
23. `2023-05-29 — MEMORIAL_DAY`
24. `2023-06-19 — JUNETEENTH_OBSERVED`
25. `2023-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
26. `2023-07-04 — INDEPENDENCE_DAY_OBSERVED`
27. `2023-09-04 — LABOR_DAY`
28. `2023-11-23 — THANKSGIVING_DAY`
29. `2023-11-24 — THANKSGIVING_FRIDAY`
30. `2023-12-22 — CHRISTMAS_PRE_HOLIDAY_SESSION`
31. `2023-12-25 — CHRISTMAS_OBSERVED`

### 2024 — 14

32. `2024-01-01 — NEW_YEARS_OBSERVED`
33. `2024-01-15 — MARTIN_LUTHER_KING_DAY`
34. `2024-02-19 — PRESIDENTS_DAY`
35. `2024-03-29 — GOOD_FRIDAY`
36. `2024-05-27 — MEMORIAL_DAY`
37. `2024-06-19 — JUNETEENTH_OBSERVED`
38. `2024-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
39. `2024-07-04 — INDEPENDENCE_DAY_OBSERVED`
40. `2024-09-02 — LABOR_DAY`
41. `2024-11-28 — THANKSGIVING_DAY`
42. `2024-11-29 — THANKSGIVING_FRIDAY`
43. `2024-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
44. `2024-12-25 — CHRISTMAS_OBSERVED`
45. `2024-12-31 — NEW_YEARS_EVE_CANDIDATE`

### 2025 — 15

46. `2025-01-01 — NEW_YEARS_OBSERVED`
47. `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`
48. `2025-01-20 — MARTIN_LUTHER_KING_DAY`
49. `2025-02-17 — PRESIDENTS_DAY`
50. `2025-04-18 — GOOD_FRIDAY`
51. `2025-05-26 — MEMORIAL_DAY`
52. `2025-06-19 — JUNETEENTH_OBSERVED`
53. `2025-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
54. `2025-07-04 — INDEPENDENCE_DAY_OBSERVED`
55. `2025-09-01 — LABOR_DAY`
56. `2025-11-27 — THANKSGIVING_DAY`
57. `2025-11-28 — THANKSGIVING_FRIDAY`
58. `2025-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
59. `2025-12-25 — CHRISTMAS_OBSERVED`
60. `2025-12-31 — NEW_YEARS_EVE_CANDIDATE`

### 2026 bounded to Aug 14 — 8

61. `2026-01-01 — NEW_YEARS_OBSERVED`
62. `2026-01-19 — MARTIN_LUTHER_KING_DAY`
63. `2026-02-16 — PRESIDENTS_DAY`
64. `2026-04-03 — GOOD_FRIDAY`
65. `2026-05-25 — MEMORIAL_DAY`
66. `2026-06-19 — JUNETEENTH_OBSERVED`
67. `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
68. `2026-07-03 — INDEPENDENCE_DAY_OBSERVED`

Candidate-count reconciliation:

`6 + 12 + 13 + 14 + 15 + 8 = 68`

## 4. In-window evidence state

Current executable `SPECIAL_SESSION_EVIDENCE` contains only one resolved candidate inside this selected interval:

- `2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025` — PASS / locked.

No other 2021-08-14 → 2026-08-14 candidate is currently resolved by `SPECIAL_SESSION_EVIDENCE` or `NO_SPECIAL_CHANGE_EVIDENCE`.

Therefore:

- candidate dates: **68**
- resolved: **1**
- unresolved: **67**
- FAIL: **0**

`1 + 67 = 68`

All 67 unresolved dates retain their previously qualified BLOCKED state. No date has been reclassified to make the candidate window look cleaner.

## 5. Boundary-rule application

State for `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`:

- `window_start = 2021-08-14`
- `window_end = 2026-08-14`
- `window_contiguous = True`
- `manual_date_exclusion_inside_window = False`
- `window_selection_rationale_versioned = True`
- `window_selection_independent_of_known_gaps = True`
- `window_shifted_to_avoid_known_gap = False`
- `window_candidates_enumerated = True`
- `window_unresolved_count = 67`
- `window_fail_count = 0`
- `execution_window_frozen = False`

Freeze decision:

**BLOCKED — `EXECUTION_WINDOW_CONTAINS_UNRESOLVED_DATES`**

This is the expected governed result. The rule was not changed after seeing the 67 gaps.

## 6. Acquisition / backtest state

The candidate is not frozen.

Therefore:

- massive `.bi5` acquisition: **BLOCKED**;
- real backtest: **BLOCKED**;
- no data acquisition is authorized by this application.

## 7. Important distinction

We now possess a **scientifically selected candidate window**, not an executable/frozen window.

The correct next work is no longer to search the entire 2018–2026 envelope indiscriminately. It is to deal with the **67 in-window unresolved calendar candidates** under the already-qualified evidence gate, while preserving all 20 global gaps outside the candidate window as global historical BLOCKED state.

No boundary may be moved to reduce that number.
