# Trading Breaks Calendar Closure — Persisted-HEAD Re-break

## Verdict

**PASS — `TRADING_BREAKS_EXECUTION_WINDOW_CALENDAR_EVIDENCE_FULLY_CLOSED`**

This report closes the bounded Trading Breaks calendar-evidence work for the selected execution-window candidate. It does not freeze the execution window, authorize native tick acquisition, or authorize a real backtest.

## Authoritative integration

- integration workflow: `Trading Breaks Calendar Closure Integration`
- authoritative run/job: `35099003783 / 104803390287`
- trigger HEAD: `bc4439df64b689c658e5bbc543456da2f26a4897`
- atomic integration commit: `34c57567d6a564e0f1ca5970a23b12ee24c86c90`
- conclusion: `success`

The atomic integration changed exactly three governed state surfaces:

1. `tools/dukascopy_usatech_calendar.py`
2. `tools/dukascopy_usatech_calendar_coverage.py`
3. `reports/data-qualification/historical_trading_breaks_recovery_progression_runtime.json`

The attempt ledger and capability-change registry remained byte-identical.

## Integrated qualified decisions

### Nine Class-A positive overlap-V2 decisions

The integration bound the nine remaining Class-A dates to the already-qualified offline readjudication under:

`TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`

No broker recapture and no new broker attempt were created.

Integrated dates:

- `2023-12-25 — CHRISTMAS_OBSERVED` — record `63023` — hours `0..22` — source `batch07:2023-12-25`
- `2024-01-01 — NEW_YEARS_OBSERVED` — record `63024` — hours `0..22` — source `batch07:2024-01-01`
- `2024-03-29 — GOOD_FRIDAY` — record `66555` — hours `0..23` — source `batch08:2024-03-29`
- `2024-12-25 — CHRISTMAS_OBSERVED` — record `74339` — hours `0..22` — source `batch09:2024-12-25`
- `2025-01-01 — NEW_YEARS_OBSERVED` — record `75799` — hours `0..22` — source `batch10:2025-01-01`
- `2025-04-18 — GOOD_FRIDAY` — record `80057` — hours `0..23` — source `batch10:2025-04-18`
- `2025-12-25 — CHRISTMAS_OBSERVED` — record `91078` — hours `0..22` — source `batch12:2025-12-25`
- `2026-01-01 — NEW_YEARS_OBSERVED` — record `92491` — hours `0..22` — source `batch13:2026-01-01`
- `2026-04-03 — GOOD_FRIDAY` — record `98541` — hours `0..21` — source `batch13:2026-04-03`

Authoritative semantic source:

`reports/data-qualification/trading_breaks_target_day_overlap_readjudication.md`

### Three Class-B qualified negative-evidence decisions

The integration populated governed `NO_SPECIAL_CHANGE_EVIDENCE` only after the separate completeness contract had passed:

`TRADING_BREAKS_NEGATIVE_EVIDENCE_COMPLETENESS_V1`

The permitted date-level conclusion is:

`NO_BROKER_TRADING_BREAK_INTERVAL_OVERLAPS_TARGET_DAY`

Integrated dates and immutable historical sources:

- `2021-12-31 — NEW_YEARS_EVE_CANDIDATE+NEW_YEARS_OBSERVED`
  - `batch01:2021-12-31`
  - `batch02:2021-12-31`
- `2022-07-01 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
  - `batch03:2022-07-01`
- `2026-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
  - `batch14:2026-07-02`

Authoritative completeness source:

`reports/data-qualification/trading_breaks_negative_evidence_completeness_qualification.md`

## Exact post-integration state

### Global coverage envelope

- candidates: `111`
- resolved: `91`
- unresolved: `20`
- FAIL: `0`
- global verdict remains `BLOCKED`
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

The remaining 20 global unresolved dates are outside the selected execution-window candidate and remain visible; they were not deleted or reclassified.

### Execution-window candidate

Window:

`2021-08-14 → 2026-08-14`

State:

- candidates: `68`
- resolved: `68`
- unresolved: `0`
- FAIL: `0`
- date-coverage audit verdict: `PASS`

### Recovery state

- historical broker attempts: `73`
- registered material capability changes: `1`
- current capability: `TRADING_BREAKS_PRIMARY_WIDGET_TARGET_DAY_OVERLAP_V2`
- recovery queue: `0`
- progression decisions: `0`
- execution-eligible recovery queue: `0`
- deterministic progression regeneration: byte-stable

## Integration adversarial history

The first integration candidate execution failed before mutation because a test incorrectly prohibited `matching_records` anywhere in the integration tool, despite legitimate Class-A positive-source parsing. The scope was corrected to the Class-B path only.

A second pre-mutation execution exposed a test that searched for a contract's literal value although the production code imported it under `NEGATIVE_CONTRACT`. The assertion was corrected without changing production semantics.

No governed state mutation occurred in either failed run.

## Independent persisted-HEAD re-break

Workflow:

`Trading Breaks Calendar Closure Persisted HEAD Re-break`

Authoritative verifier:

- verifier HEAD: `87f1d6bc2c61c1fd489789bc3a9d3ca70ff8a791`
- run/job: `35099483420 / 104804978766`
- permissions: `contents: read`
- conclusion: `success`

The verifier independently proved:

- integration commit ancestry;
- exact three-file atomic integration delta;
- no governed-state delta after the integration commit;
- attempt ledger unchanged from the pre-integration parent;
- capability-change registry unchanged from the pre-integration parent;
- exact nine Class-A records, closed-hour sets and immutable source attempts;
- exact three Class-B negative-evidence records and provenance bindings;
- global state `111 / 91 / 20`;
- execution-window state `68 / 68 / 0`;
- empty recovery/progression/eligibility queues;
- `85 passed` durable semantic/calendar/boundary regressions;
- deterministic progression byte stability;
- read-only workflow permission and bounded external action surface;
- clean final worktree.

Three earlier verifier executions reached all substantive state/regression checks and failed only in self-referential workflow-source assertions. Those checks were replaced by structural permission/action-surface validation; no production state or acceptance criterion was weakened.

## Closure

Trading Breaks calendar evidence for the fixed execution-window candidate is **FULLY CLOSED**.

This PASS establishes calendar completeness inside the candidate window. It does **not** itself perform the separate `FREEZE_EXECUTION_WINDOW` governance decision.

It does **not** authorize `.bi5` acquisition.

It does **not** authorize a real backtest.

The next system-level priority must be selected by confronting this now-current repository state with the architecture snapshot and its outstanding dependencies, rather than blindly continuing the historical batch process.
