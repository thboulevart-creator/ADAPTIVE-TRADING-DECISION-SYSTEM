# SESSION BACKUP — 2026-09-13 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint HEAD: `501a090afd09da1bcd30e9111c53147d682c5317`
- Calendar evidence commit: `2f0a088bc8f6aaafed9db9c1ed6966301271ac75`
- Calendar test commit: `df668b89b219cee8e72e20a10d5c307439a8046d`
- Active objective: qualify the complete Dukascopy USATECH special-session calendar before native `.bi5` acquisition.
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`.
- Coverage envelope: `2018-05-01` through `2026-08-14`.
- Execution/backtest window: NOT frozen yet.

## Recovery and source-of-truth verification

The session started by reading, in governed order:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. `99-BACKUP/README.md`
4. this session snapshot
5. `tools/dukascopy_usatech_calendar.py`
6. `tools/dukascopy_usatech_calendar_coverage.py`
7. `tests/test_dukascopy_usatech_calendar.py`

GitHub comparison proved the branch was exactly identical to checkpoint commit `501a090afd09da1bcd30e9111c53147d682c5317` before writes (`ahead_by=0`, `behind_by=0`). No conversational reconstruction was used as technical source of truth.

## Locked upstream state preserved

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- Actual 3.1.2 execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution-cost environment exist.
- No partial/synthetic/fabricated backtest is authorized.

## 2019 evidence consolidation performed

Thirteen unresolved 2019 candidate dates were investigated using the same evidence discipline as 2018. Only six crossed the threshold sufficiently to be versioned:

1. `2019-01-01` — New Year's Day
   - same exact Dec 31 2018–Jan 1 2019 evidenced holiday window already used for the 2018 New Year's Eve qualification;
   - whole-hour closure: `00-22 UTC`; reopening `23 UTC`.
2. `2019-01-21` — Martin Luther King Jr. Day
   - date-specific Dukascopy special-CFD-break announcement;
   - preserved CME Globex Control Center summary via AMP mirror: noon CST halt, then normal reopening;
   - whole-hour closure: `18-22 UTC`.
3. `2019-02-18` — Presidents Day
   - date-specific Dukascopy special-CFD-break announcement;
   - preserved CME Globex Control Center summary via AMP mirror: noon CST halt, then normal reopening;
   - whole-hour closure: `18-22 UTC`.
4. `2019-05-27` — Memorial Day
   - date-specific Dukascopy market-closure context;
   - preserved CME Globex Control Center summary via AMP mirror: noon Chicago halt, then normal reopening;
   - Chicago is on CDT, so whole-hour closure: `17-21 UTC`.
5. `2019-11-28` — Thanksgiving Day
   - Dukascopy explicitly identifies special closures on Thursday and Friday;
   - preserved CME Globex Control Center summary via AMP mirror: noon CST halt, then normal reopening;
   - whole-hour closure: `18-22 UTC`.
6. `2019-11-29` — Thanksgiving Friday
   - same Dukascopy date-specific Thanksgiving context;
   - CME mirror gives 12:15 CST early close;
   - hour `18 UTC` remains partially tradable;
   - special whole-hour closures: `19-21 UTC`; `22-23 UTC` remain regular Friday weekly closure.

These dates were added to `SPECIAL_SESSION_EVIDENCE` in commit `2f0a088bc8f6aaafed9db9c1ed6966301271ac75`.

## 2019 dates deliberately NOT promoted

The following seven dates remain unresolved because available evidence did not meet the same broker/date-specific timing threshold without extrapolation:

- `2019-04-19` — GOOD_FRIDAY
- `2019-07-03` — INDEPENDENCE_PRE_HOLIDAY_SESSION
- `2019-07-04` — INDEPENDENCE_DAY_OBSERVED
- `2019-09-02` — LABOR_DAY
- `2019-12-24` — CHRISTMAS_PRE_HOLIDAY_SESSION
- `2019-12-25` — CHRISTMAS_OBSERVED
- `2019-12-31` — NEW_YEARS_EVE_CANDIDATE

Relevant exchange/mirror evidence exists for several of these dates, but absent sufficiently precise Dukascopy-specific date evidence or complete closure/reopening proof, it was not converted into calendar truth. This is intentional BLOCKED discipline, not missing work disguised as PASS.

## Tests

Six new targeted tests were added in commit `df668b89b219cee8e72e20a10d5c307439a8046d`, bringing the versioned calendar suite from 22 to 28 tests.

Observed local execution after materializing the current GitHub test blob and the current calendar classification/evidence logic:

```text
............................                                             [100%]
28 passed in 0.08s
```

This is an observed test execution, not an inferred `28/28` claim. There is no repository GitHub Actions workflow available on this branch, and the local container has no direct network route to GitHub; GitHub writes and blob verification were therefore performed through the GitHub connector, while Python execution was performed locally from the versioned logic.

## Coverage execution

Observed execution of `tools/dukascopy_usatech_calendar_coverage.py` after the six evidence additions:

- `candidate_dates`: **111**
- `resolved_candidate_dates`: **18**
- `special_session_evidence_dates`: **18**
- `no_special_change_evidence_dates`: **0**
- `unresolved_candidate_dates`: **93**
- `contradictory_evidence_dates`: `[]`
- `evidence_shape_errors`: `[]`
- `orphan_special_evidence`: `[]`
- `verdict`: **BLOCKED**
- `reason`: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`
- process exit code: `2` (expected for BLOCKED under this script contract)

The first unresolved date is now `2019-04-19`.

## Evidence discipline preserved

- Verdicts only PASS / FAIL / BLOCKED.
- Never promote missing evidence to PASS.
- Never infer a closure merely from a holiday name.
- Never infer closure from HTTP/BI5 absence.
- Never extrapolate one year's hours to another year.
- Partial tradable hour remains EXPECTED_OPEN.
- Only complete UTC hourly buckets proven closed enter `fully_closed_hours_utc`.
- Historical CME copies remain explicitly mirror evidence.
- The Dukascopy Trading Breaks historical widget route remains CLOSED unless materially new evidence appears.
- Massive acquisition remains forbidden until calendar coverage reaches zero unresolved dates and verdict PASS.

## Exactly one next governed action

**Resolve the remaining seven 2019 candidate dates (`2019-04-19`, `2019-07-03`, `2019-07-04`, `2019-09-02`, `2019-12-24`, `2019-12-25`, `2019-12-31`) using date-specific evidence at the same threshold; commit only dates that actually cross the threshold; then rerun the 28-test calendar suite and coverage audit.**
