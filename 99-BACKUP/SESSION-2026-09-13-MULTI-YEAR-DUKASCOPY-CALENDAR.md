# SESSION BACKUP — 2026-09-13 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Prior authoritative checkpoint: `3a39e86d457095ca99d782b4eb48cc206cbefa2f`
- Late-2019 calendar evidence commit: `6dbe69cc3a4d7a1fe023e7274945bfe147b6aeeb`
- Late-2019 supplementary-test commit: `82ede6465f9fa006cc49868b663d0fd67c9824fc`
- Dedicated 2019-07-03 witness-search report commit: `f0289238eb89cb634fb8c78c520bb2e540deda75`
- Dedicated witness-search report: `reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`
- Active objective: qualify the complete Dukascopy USATECH special-session calendar before native `.bi5` acquisition.
- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`.
- Coverage envelope: `2018-05-01` through `2026-08-14`.
- Execution/backtest window: NOT frozen yet.

## Source-of-truth verification

At the start of the dedicated `2019-07-03` continuation, GitHub comparison proved `feat/multi-year-dukascopy-acquisition` was exactly identical to checkpoint `3a39e86d457095ca99d782b4eb48cc206cbefa2f` (`ahead_by=0`, `behind_by=0`). The search therefore began from the governed checkpoint, not conversational reconstruction.

## Locked upstream state preserved

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- Actual 3.1.2 execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution-cost environment exist.
- No partial/synthetic/fabricated backtest is authorized.
- Massive `.bi5` acquisition remains forbidden until calendar coverage reaches zero unresolved dates and verdict PASS.

## 2019 qualification state before dedicated witness search

Twelve 2019 candidate dates were already resolved:

- `2019-01-01` New Year's Day
- `2019-01-21` Martin Luther King Jr. Day
- `2019-02-18` Presidents Day
- `2019-04-19` Good Friday
- `2019-05-27` Memorial Day
- `2019-07-04` Independence Day
- `2019-09-02` Labor Day
- `2019-11-28` Thanksgiving Day
- `2019-11-29` Thanksgiving Friday
- `2019-12-24` Christmas Eve
- `2019-12-25` Christmas Day
- `2019-12-31` New Year's Eve

The sole unresolved 2019 candidate was and remains:

- `2019-07-03` — `INDEPENDENCE_PRE_HOLIDAY_SESSION`

## Dedicated 2019-07-03 witness search

The next governed action was executed directly: search for a materially new, date-specific Dukascopy/USATECH broker witness for `2019-07-03`, without reusing 2018 and without promoting CME-only evidence.

Search dimensions included:

- `site:dukascopy.com` + 2019 July 3 + US Independence Day + USATECH;
- exact `USATECH.IDX/USD` + `3 July 2019` / `July 3, 2019`;
- exact `17:15` + Dukascopy + USATECH + 2019;
- Dukascopy company-news pages around 1-5 July 2019;
- exact publication timestamps around 1-3 July 2019;
- multilingual Dukascopy pages;
- external indexed/archive references and RSS/news-digest style mirrors;
- official/social-web searches for Dukascopy Independence-Day trading-hours material.

The search found genuine Dukascopy content published on `2019-07-03`, demonstrating that the historical date is represented in the searchable corpus. None of those pages contained a qualifying USATECH holiday-break witness.

### Historical Dukascopy witnesses recovered but rejected as substitutes

1. **2018 official Dukascopy**
   - `USATECH.IDX/USD` trading stops at 17:15 GMT on Tuesday 3 July 2018 and reopens at 22:00 GMT;
   - exact broker-specific witness, but wrong year;
   - cannot be extrapolated to 2019.

2. **2017 official Dukascopy**
   - July-3 pre-holiday USATECH closure exists with a different time;
   - demonstrates that the treatment can differ by year;
   - cannot qualify 2019.

3. **2015 official Dukascopy**
   - July-3 USATECH closure exists for that year's observed holiday configuration;
   - cannot qualify 2019.

4. **2026 official Dukascopy**
   - Dukascopy applies special breaks on Friday 3 July 2026 ahead of Independence Day;
   - confirms broker behavior is year-specific and can include July 3;
   - cannot qualify 2019.

5. **Current regular schedule**
   - Dukascopy identifies regular summer USATECH hours as Sun-Fri 22:00-20:15 GMT with daily 20:15-22:00 break;
   - regular-session context only, not special-session proof for 2019-07-03.

### Existing 2019 exchange evidence

Exact 2019 CME-derived evidence remains available for ES/NQ/YM early close at 12:15 Chicago time on Wednesday 3 July 2019. That would imply a partially tradable 17 UTC hour and fully closed exchange buckets `18-21 UTC`.

This exchange timing remains **insufficient alone** because the missing fact is whether Dukascopy applied that exact special break to `USATECH.IDX/USD` in 2019.

### Archive-path limitation

A direct Wayback/CDX query for Dukascopy `about/ournews` captures around 1-5 July 2019 was attempted from the local execution environment. It failed because that environment has no DNS/network route to `web.archive.org`.

This is recorded as an access limitation, **not evidence of absence**. Web-index searches for archived/Wayback copies also returned no qualifying date-specific 2019-07-03 Dukascopy/USATECH witness.

## Dedicated search verdict

**BLOCKED**

Reason: `DATE_SPECIFIC_DUKASCOPY_USATECH_2019_07_03_WITNESS_NOT_FOUND`

The detailed durable report is versioned at:

`reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`

No calendar record was added for `2019-07-03`.
No test expectation changed.
No coverage PASS was claimed.

## Latest executable evidence remains unchanged

The last observed calendar tests remain:

```text
............................                                             [100%]
28 passed in 0.04s
```

and the six late-2019 targeted tests remain:

```text
......                                                                   [100%]
6 passed in 0.02s
```

Combined last observed execution: `34 passed in 0.04s`.

They were not rerun during the witness-only search because no executable calendar/test code changed. Do not fabricate a newer execution claim.

## Latest coverage state remains unchanged

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

The first unresolved date remains `2019-07-03`.

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
- Exchange-only evidence is not silently promoted to broker truth where broker treatment remains uncertain.
- The historical Trading Breaks widget route remains CLOSED unless materially new evidence appears.
- Do not repeat the generic `2019-07-03` searches merely to reconstruct this state; read the witness-search report first.
- Massive acquisition remains forbidden until coverage reaches zero unresolved dates and verdict PASS.

## Exactly one next governed action

**Formalize an `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` governance rule for historical dates where exhaustive retrieval cannot recover a date-specific broker witness. Define an explicit evidence hierarchy and PASS / FAIL / BLOCKED conditions, adversarially break the proposed rule, and qualify it before applying anything to `2019-07-03`. Do not change `2019-07-03`, do not begin 2020 qualification, and do not begin massive `.bi5` acquisition until that governance rule itself is qualified.**
