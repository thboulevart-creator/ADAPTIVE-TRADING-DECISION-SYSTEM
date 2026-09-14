# DUKASCOPY USATECH — GLOBAL CROSS-YEAR CALENDAR COVERAGE AUDIT

## Status

Global cross-year audit: **PASS**

Reason:

`ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT`

This PASS certifies the integrity and completeness of the global accounting exercise. It does **not** mean calendar coverage is complete and does **not** authorize acquisition or backtesting.

## 1. Governed scope

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch: `feat/multi-year-dukascopy-acquisition`

Starting checkpoint / verified HEAD:

`3e1324199b4e8ab8c2c2534d264d3dea6b859193`

Global research envelope:

`2018-05-01` → `2026-08-14`

Instrument:

- Dukascopy: `USATECH.IDX/USD`
- internal: `USATECHIDXUSD`

Governed by:

- `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Executable sources:

- `tools/dukascopy_usatech_calendar.py`
- `tools/dukascopy_usatech_calendar_coverage.py`
- `tools/coverage_execution_window_boundary.py`

## 2. Global candidate reconciliation

The versioned candidate generator yields the following bounded annual/segment counts:

| Period | Candidates | Resolved | Unresolved |
|---|---:|---:|---:|
| 2018-05-01 → 2018-12-31 | 10 | 10 | 0 |
| 2019 | 13 | 12 | 1 |
| 2020 | 13 | 1 | 12 |
| 2021 | 13 | 0 | 13 |
| 2022 | 12 | 0 | 12 |
| 2023 | 13 | 0 | 13 |
| 2024 | 14 | 0 | 14 |
| 2025 | 15 | 1 | 14 |
| 2026-01-01 → 2026-08-14 | 8 | 0 | 8 |
| **TOTAL** | **111** | **24** | **87** |

Arithmetic reconciliation:

`10 + 13 + 13 + 13 + 12 + 13 + 14 + 15 + 8 = 111`

`10 + 12 + 1 + 0 + 0 + 0 + 0 + 1 + 0 = 24`

`0 + 1 + 12 + 13 + 12 + 13 + 14 + 14 + 8 = 87`

`24 + 87 = 111`

No candidate disappears between the annual/segment accounting and the global accounting.

## 3. Executable resolution state

Current `SPECIAL_SESSION_EVIDENCE` contains exactly **24** date records:

- 2018: **10**
- 2019: **12**
- 2020: **1** (`2020-02-17 — PRESIDENTS_DAY`)
- 2021: **0**
- 2022: **0**
- 2023: **0**
- 2024: **0**
- 2025: **1** (`2025-01-09 — NATIONAL_DAY_OF_MOURNING_CARTER_2025`)
- 2026 in-envelope: **0**

`NO_SPECIAL_CHANGE_EVIDENCE` remains empty.

Therefore:

- special-session evidence dates = **24**;
- no-special-change evidence dates = **0**;
- resolved candidate dates = **24**;
- unresolved candidate dates = **87**.

The first unresolved candidate remains:

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

with verdict:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**.

## 4. Integrity checks

### Candidate/orphan integrity

Every current `SPECIAL_SESSION_EVIDENCE` date corresponds to a generated candidate inside the governed envelope.

Result:

- orphan special evidence: **0**.

### Contradiction integrity

`NO_SPECIAL_CHANGE_EVIDENCE` is empty, therefore there is no date simultaneously classified as special-session evidence and no-special-change evidence.

Result:

- contradictory overlap dates: **0**.

### Evidence-shape integrity

Current special-session records provide:

- non-empty `reason`;
- `fully_closed_hours_utc` as `frozenset`;
- at least one source field ending in `_source`;
- UTC whole-hour values within `0..23`.

Result:

- evidence-shape errors: **0**.

### Historical-gap visibility

All annual/segment reports preserve their BLOCKED dates. No prior gap was silently deleted, converted to PASS, or excluded from the global count.

Result:

- hidden/reclassified prior gap: **NO**;
- prior gaps preserved: **YES**.

## 5. Cross-year annual/segment audit reconciliation

Locked qualification state remains:

- 2019 first known unresolved: `2019-07-03` BLOCKED;
- 2020: `1 PASS / 12 BLOCKED`, annual audit PASS;
- 2021: `0 PASS / 13 BLOCKED`, annual audit PASS;
- 2022: `0 PASS / 12 BLOCKED`, annual audit PASS;
- 2023: `0 PASS / 13 BLOCKED`, annual audit PASS;
- 2024: `0 PASS / 14 BLOCKED`, annual audit PASS;
- 2025: `1 PASS / 14 BLOCKED`, annual audit PASS;
- bounded 2026: `0 PASS / 8 BLOCKED`, bounded audit PASS.

The 2018 executable records plus the 2019 resolved records account for the remaining pre-2020 resolved candidates.

Annual/segment audit PASS means candidate accounting and evidence discipline passed. It never means the corresponding calendar coverage is complete.

## 6. Global coverage decision

Boundary action:

`DECLARE_GLOBAL_COVERAGE_PASS`

Current state:

- global unresolved = **87**;
- global FAIL = **0**;
- orphan evidence = **0**;
- contradictions = **0**;
- malformed evidence = **0**.

Decision:

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Rationale:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1` requires unresolved count = 0 before global coverage can PASS. Eighty-seven unresolved dates remain.

## 7. Execution-window feasibility and freeze decision

### 7.1 Current freeze action

No exact future execution window has been versioned/frozen.

Executable boundary decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_DEFINED`**

### 7.2 Feasibility under current evidence

A future execution window must be contiguous and span at least five calendar years with:

- zero in-window unresolved candidates;
- zero in-window FAIL candidates;
- an independently justified and versioned selection rationale.

Current evidence proves there is **no** contiguous >=5-calendar-year subset of `2018-05-01 → 2026-08-14` with zero unresolved candidates:

1. the first unresolved date is `2019-07-03`;
2. the interval from envelope start `2018-05-01` to that first gap is far shorter than five years;
3. unresolved candidates continue in every later annual/segment block through the envelope end.

Therefore any possible >=5-year contiguous window inside the current envelope intersects at least one unresolved candidate.

Feasibility conclusion:

**BLOCKED — `NO_ADMISSIBLE_FIVE_YEAR_ZERO_UNRESOLVED_WINDOW_UNDER_CURRENT_EVIDENCE`**

This is an evidence incompleteness BLOCKED, not a hard-invariant FAIL. A later window may become feasible if its in-window evidence gaps are genuinely resolved.

No window may be shifted or shortened merely to evade known gaps.

## 8. Massive `.bi5` acquisition decision

Boundary action:

`AUTHORIZE_MASSIVE_ACQUISITION`

Current state:

- execution window frozen: **NO**;
- freeze action PASS: **NO**;
- mandatory window gates PASS: **NO**;
- explicit acquisition authorization: **NO**.

Decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

Massive native `.bi5` acquisition remains forbidden.

No OHLC M1, synthetic ticks, interpolation, substituted ticks, or partial acquisition may be used to bypass this gate.

## 9. Real backtest decision

A real backtest remains downstream of a valid frozen execution window, qualified native tick data, calendar qualification, acquisition/reconciliation evidence, and the existing backtest gates.

Current upstream state contains:

- global calendar coverage BLOCKED;
- no admissible five-year zero-unresolved window under current evidence;
- no frozen execution window;
- no massive native `.bi5` acquisition authorization;
- no qualified acquired corpus for such a window.

Decision:

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

No real backtest may begin.

## 10. Final action matrix

| Action / claim | Verdict | Reason |
|---|---|---|
| Global cross-year accounting audit | **PASS** | `ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT` |
| Declare global coverage PASS | **BLOCKED** | `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES` |
| Execution-window feasibility | **BLOCKED** | `NO_ADMISSIBLE_FIVE_YEAR_ZERO_UNRESOLVED_WINDOW_UNDER_CURRENT_EVIDENCE` |
| Freeze execution window | **BLOCKED** | `EXECUTION_WINDOW_NOT_DEFINED` |
| Authorize massive `.bi5` acquisition | **BLOCKED** | `EXECUTION_WINDOW_NOT_FROZEN` |
| Start real backtest | **BLOCKED** | `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS` |

## 11. Executable state preservation

This global audit does not change executable calendar evidence.

Therefore:

- `tools/dukascopy_usatech_calendar.py` remains unchanged;
- `tools/dukascopy_usatech_calendar_coverage.py` remains unchanged;
- special-session evidence remains **24 records**;
- unresolved remains **87**;
- latest observed calendar test suite remains **34 PASS** and is not rerun merely for timestamp freshness;
- no `.bi5` is downloaded;
- no execution window is frozen;
- no real backtest is started;
- global envelope remains `2018-05-01 → 2026-08-14`.

## 12. Exactly one next governed action

**Define and version an execution-window selection rationale that is independent of known gaps, without freezing or acquiring data yet.**

The rationale must exist independently of gap avoidance (for example, a research-driven recency/horizon rule), then the resulting exact >=5-year contiguous candidate window must be enumerated and its unresolved set measured.

Because no current >=5-year window has zero unresolved dates, this next step is a candidate-window formalisation / gap-targeting step only. It cannot produce window-freeze PASS unless all in-window unresolved evidence is subsequently resolved.

Do not choose boundaries by inspecting which dates are easiest to prove. Do not download `.bi5`. Do not start a real backtest.