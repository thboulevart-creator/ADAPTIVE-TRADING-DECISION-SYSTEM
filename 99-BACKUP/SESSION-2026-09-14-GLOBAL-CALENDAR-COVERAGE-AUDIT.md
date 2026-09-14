# SESSION BACKUP — 2026-09-14 — GLOBAL CROSS-YEAR CALENDAR COVERAGE AUDIT

## 0. Purpose

Authoritative durable recovery snapshot after completion of chronological Dukascopy USATECH calendar qualification through the governed envelope end and completion of the global cross-year consolidation/audit.

Do not reconstruct this state from conversation history.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `feat/multi-year-dukascopy-acquisition`
- Starting verified checkpoint/HEAD: `3e1324199b4e8ab8c2c2534d264d3dea6b859193`
- Global envelope: `2018-05-01` → `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Chronological annual/segment research: COMPLETE TO ENVELOPE END
- Execution window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: BLOCKED

## 2. Global audit artifact

`reports/data-qualification/dukascopy_usatech_global_calendar_coverage_audit.md`

Creation commit:

`ce7d0869efeddcf27e496f3bb9410aa08534c957`

Global audit verdict:

**PASS**

Reason:

`ALL_111_CANDIDATES_RECONCILED_WITH_24_RESOLVED_87_UNRESOLVED_AND_NO_INTEGRITY_DEFECT`

This PASS means only that global accounting and integrity are complete/correct. It does not mean global calendar coverage is complete.

## 3. Global candidate reconciliation

Bounded annual/segment matrix:

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

Arithmetic:

- candidate total = `10+13+13+13+12+13+14+15+8 = 111`;
- resolved = `10+12+1+0+0+0+0+1+0 = 24`;
- unresolved = `0+1+12+13+12+13+14+14+8 = 87`;
- `24+87=111`.

No candidate was lost or silently reclassified during annual progression.

## 4. Executable evidence integrity

Current `SPECIAL_SESSION_EVIDENCE` contains exactly 24 records:

- 2018: 10;
- 2019: 12;
- 2020: 1 (`2020-02-17`);
- 2021: 0;
- 2022: 0;
- 2023: 0;
- 2024: 0;
- 2025: 1 (`2025-01-09`);
- 2026 bounded: 0.

`NO_SPECIAL_CHANGE_EVIDENCE` remains empty.

Static integrity checks:

- orphan special evidence: 0;
- contradictory overlap: 0;
- malformed evidence records: 0;
- hidden/reclassified prior gaps: 0;
- prior gaps preserved: yes.

First unresolved remains:

`2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**.

## 5. Boundary application

Updated current application:

`reports/data-qualification/current_coverage_execution_window_boundary_application.md`

Update commit:

`a8a64c3c15e7fbf4699f5c496fa3a0d9d2392d4c`

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

### Global coverage

**BLOCKED — `GLOBAL_COVERAGE_STILL_HAS_UNRESOLVED_DATES`**

Reason: unresolved = 87, while Action B requires unresolved = 0.

### Execution-window freeze

Executable current decision:

**BLOCKED — `EXECUTION_WINDOW_NOT_DEFINED`**

### Execution-window feasibility under current evidence

**BLOCKED — `NO_ADMISSIBLE_FIVE_YEAR_ZERO_UNRESOLVED_WINDOW_UNDER_CURRENT_EVIDENCE`**

Proof:

- first unresolved is `2019-07-03`;
- only ~14 months of the envelope precede it, far below five years;
- every later annual/segment block contains unresolved dates;
- therefore every contiguous >=5-year subset inside the current envelope intersects unresolved evidence.

This is BLOCKED, not FAIL: evidence can in principle be completed later.

### Massive `.bi5` acquisition

**BLOCKED — `EXECUTION_WINDOW_NOT_FROZEN`**

Massive native `.bi5` acquisition remains forbidden.

### Real backtest

**BLOCKED — `UPSTREAM_WINDOW_ACQUISITION_AND_DATA_QUALIFICATION_NOT_PASS`**

No real backtest may begin.

## 6. Final current matrix

- global cross-year accounting audit: **PASS**;
- global calendar coverage: **BLOCKED**;
- execution-window feasibility: **BLOCKED**;
- execution-window freeze: **BLOCKED**;
- massive native `.bi5` acquisition: **BLOCKED**;
- real backtest: **BLOCKED**.

Latest observed executable calendar tests remain **34 PASS**. They were not rerun because no executable calendar code/evidence changed during the global audit.

## 7. Important interpretation

The annual/segment qualification campaign succeeded at its purpose: it exposed and preserved the truth state of the envelope.

It did **not** produce complete historical broker-session evidence for a five-year window.

The fact that 87 dates are BLOCKED is not an audit failure. Hiding them would have been a failure. The global audit PASS means the gaps are correctly accounted for and visible.

## 8. Anti-cherry-pick rule remains active

Do not now choose a convenient five-year period by inspecting which gaps are easiest or hardest.

Before an execution window can even become a governed candidate, its selection rationale must be:

- explicit;
- versioned;
- independent of known unresolved/FAIL dates;
- at least five calendar years;
- contiguous.

Only after that rationale is frozen may the resulting in-window candidate list and exact unresolved set be used as a targeted evidence-recovery frontier.

## 9. Exactly one next governed action

**Define and version an execution-window selection rationale independent of known gaps, without freezing a window or acquiring data.**

This next action must formalize the selection policy first. It must not inspect the unresolved matrix in order to choose boundaries.

After the policy selects an exact >=5-year contiguous candidate window, enumerate its candidate dates and unresolved set. Because current evidence contains no zero-gap >=5-year window, the candidate will remain BLOCKED until its in-window gaps are genuinely resolved.

Do not download `.bi5`. Do not start a real backtest. Do not redefine the global envelope merely to obtain PASS.