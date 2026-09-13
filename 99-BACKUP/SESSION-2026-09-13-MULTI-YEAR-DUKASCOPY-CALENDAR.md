# SESSION BACKUP — 2026-09-13 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Prior authoritative checkpoint: `25545ced686e06188c2e860d9355da478889ab82`
- Late-2019 calendar evidence commit: `6dbe69cc3a4d7a1fe023e7274945bfe147b6aeeb`
- Late-2019 supplementary-test commit: `82ede6465f9fa006cc49868b663d0fd67c9824fc`
- Active objective: qualify the complete Dukascopy USATECH special-session calendar before native `.bi5` acquisition.
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`.
- Coverage envelope: `2018-05-01` through `2026-08-14`.
- Execution/backtest window: NOT frozen yet.

## Source-of-truth verification

At the start of this continuation, GitHub comparison proved `feat/multi-year-dukascopy-acquisition` was exactly identical to checkpoint `25545ced686e06188c2e860d9355da478889ab82` (`ahead_by=0`, `behind_by=0`). Work proceeded from the versioned calendar/checkpoint state, not conversational reconstruction.

## Locked upstream state preserved

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- Actual 3.1.2 execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution-cost environment exist.
- No partial/synthetic/fabricated backtest is authorized.
- Massive `.bi5` acquisition remains forbidden until calendar coverage reaches zero unresolved dates and verdict PASS.

## Late-2019 qualification performed

The seven unresolved 2019 dates from the prior checkpoint were investigated under the same evidence threshold used for 2018 and the already-qualified 2019 dates.

Six dates crossed the threshold and were versioned in `SPECIAL_SESSION_EVIDENCE`:

1. `2019-04-19` — Good Friday
   - date-specific Dukascopy Easter-weekend CFD closure context;
   - preserved CME Globex 2019 schedule mirror identifies Good Friday as fully closed;
   - whole UTC day `00-23` classified closed.
2. `2019-07-04` — Independence Day
   - date-specific Dukascopy 4 July 2019 special-CFD-break announcement;
   - preserved 2019 CME-derived ES/NQ/YM schedule gives 12:00 Chicago halt;
   - Chicago was on CDT, giving fully closed UTC hours `17-21`, reopening `22`.
3. `2019-09-02` — Labor Day
   - date-specific Dukascopy announcement states several markets subject to early or total closure Monday 2 September 2019;
   - preserved CME Globex Equity schedule gives 12:00 CT halt and 17:00 CT resume;
   - fully closed UTC hours `17-21`.
4. `2019-12-24` — Christmas Eve
   - Dukascopy 2019 Christmas/New-Year CFD closure context;
   - exact 2019 CME Globex schedule mirror gives Equity close at 12:15 CT = 18:15 UTC;
   - hour `18` remains partially tradable; fully closed whole-hour buckets `19-23`.
5. `2019-12-25` — Christmas Day
   - same exact 2019 holiday context and CME schedule;
   - closed until 17:00 CT = 23:00 UTC reopening;
   - fully closed UTC hours `00-22`.
6. `2019-12-31` — New Year's Eve
   - Dukascopy 2019 Christmas/New-Year CFD closure context;
   - exact 2019/2020 CME Globex schedule mirror shows normal 16:00 CT = 22:00 UTC close followed by Jan 1 closure;
   - `21` UTC remains partially tradable; `22` UTC is already the regular Dukascopy daily break; only `23` UTC is an additional special whole-hour closure.

The calendar commit `6dbe69cc3a4d7a1fe023e7274945bfe147b6aeeb` was adversarially compared against checkpoint `25545ced...`: GitHub reported **98 additions, 0 deletions** in `tools/dukascopy_usatech_calendar.py`, proving no prior evidence record was overwritten by the update.

## 2019-07-03 remains BLOCKED

`2019-07-03` — `INDEPENDENCE_PRE_HOLIDAY_SESSION` did **not** cross the evidence threshold.

What is proven:

- a preserved exact 2019 CME-derived schedule shows ES/NQ/YM early close at 12:15 Chicago time on Wednesday 3 July 2019;
- this would correspond to a partially tradable 17 UTC hour and fully closed `18-21 UTC` for the CME equity-index session.

What is NOT proven:

- no sufficiently precise 2019 Dukascopy/USATECH broker-specific witness was found establishing that Dukascopy applied that July 3 early close to `USATECH.IDX/USD`;
- the Dukascopy 2019 Independence announcement found explicitly refers to special CFD breaks on **4 July 2019**, not 3 July;
- targeted searches for `USATECH.IDX/USD`, `3 July 2019`, `17:15`, and Dukascopy Trading Breaks produced no qualifying witness.

Therefore the 2018 July-3 rule was NOT extrapolated to 2019 and CME-only evidence was NOT silently promoted to broker truth. `2019-07-03` remains unresolved/BLOCKED.

## Tests

The pre-existing 28-test calendar suite was rerun after the calendar update:

```text
............................                                             [100%]
28 passed in 0.04s
```

Six additional targeted tests for the newly-qualified dates were versioned in `tests/test_dukascopy_usatech_calendar_2019_remaining.py` and executed:

```text
......                                                                   [100%]
6 passed in 0.02s
```

Combined execution was also observed as `34 passed in 0.04s`.

Execution note: the container cannot directly reach GitHub. GitHub state/writes and blob verification were performed through the GitHub connector; Python execution used a local materialisation of the versioned calendar classification/evidence logic and versioned tests. Do not misrepresent this as a network checkout or GitHub Actions run.

## Coverage execution

Observed execution of `tools/dukascopy_usatech_calendar_coverage.py` after the six late-2019 evidence additions:

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
- process exit code: `2`

The first unresolved date is now **`2019-07-03`**. If and only if that date is later resolved, the frontier moves to `2020-01-01` (notwithstanding the already-qualified isolated `2020-02-17` Presidents Day record).

## Evidence discipline preserved

- Verdicts only PASS / FAIL / BLOCKED.
- Never promote missing evidence to PASS.
- Never infer a closure merely from a holiday name.
- Never infer closure from HTTP/BI5 absence.
- Never extrapolate one year's hours to another year.
- Partial tradable hour remains EXPECTED_OPEN.
- Only complete UTC hourly buckets proven closed enter `fully_closed_hours_utc`.
- Historical CME copies remain explicitly mirror evidence.
- Dukascopy establishes broker/event context when exchange timing is used to derive exact buckets.
- The historical Trading Breaks widget route remains CLOSED unless materially new evidence appears.
- Massive acquisition remains forbidden until coverage reaches zero unresolved dates and verdict PASS.

## Exactly one next governed action

**Resolve `2019-07-03` only if a new date-specific Dukascopy/USATECH broker witness materially closes the current proof gap; do not extrapolate the 2018 rule. If the witness is found, version the exact whole-hour classification and rerun the 28 historical tests, the 6 late-2019 tests, and coverage. If no such witness exists, retain the explicit BLOCKED and do not begin 2020 or massive `.bi5` acquisition until governance decides how an irreducible historical broker-evidence gap may be handled without weakening the threshold.**
