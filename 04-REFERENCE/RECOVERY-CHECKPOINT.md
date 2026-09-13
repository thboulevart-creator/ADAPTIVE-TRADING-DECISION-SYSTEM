# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `3a39e86d457095ca99d782b4eb48cc206cbefa2f`
- **Late-2019 calendar evidence commit:** `6dbe69cc3a4d7a1fe023e7274945bfe147b6aeeb`
- **Late-2019 supplementary-test commit:** `82ede6465f9fa006cc49868b663d0fd67c9824fc`
- **2019-07-03 witness-search report commit:** `f0289238eb89cb634fb8c78c520bb2e540deda75`
- **Witness-search report:** `reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`
- **Durable session backup:** `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
- **Active block:** complete special-session/calendar qualification for Dukascopy `USATECHIDXUSD` before multi-year native `.bi5` acquisition.
- **Coverage envelope:** `2018-05-01` → `2026-08-14`.
- **Execution/backtest window frozen:** no.

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-MULTI-YEAR-DUKASCOPY-CALENDAR.md`
5. `reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`
6. `tools/dukascopy_usatech_calendar.py`
7. `tools/dukascopy_usatech_calendar_coverage.py`
8. `tests/test_dukascopy_usatech_calendar.py`
9. `tests/test_dukascopy_usatech_calendar_2019_remaining.py`
10. actual GitHub/worktree state and current execution evidence

## 3. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked; do not rerun merely to reconstruct history.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.

## 4. ACTIVE CALENDAR CONTRACTS

- `tools/dukascopy_usatech_calendar.py`
  - `DUKASCOPY_USATECH_SESSION_CALENDAR_V3`
  - contains **24** date-specific special-session evidence records inside the coverage envelope.
- `tools/dukascopy_usatech_calendar_coverage.py`
  - `DUKASCOPY_USATECH_SPECIAL_SESSION_COVERAGE_V1`
- `tests/test_dukascopy_usatech_calendar.py`
  - **28** historical/current calendar tests.
- `tests/test_dukascopy_usatech_calendar_2019_remaining.py`
  - **6** targeted tests for the newly-qualified late-2019 sessions.

No calendar or test code changed during the dedicated `2019-07-03` witness-search continuation.

## 5. LATEST OBSERVED TEST EXECUTION

The latest observed executable state remains:

```text
............................                                             [100%]
28 passed in 0.04s
```

and:

```text
......                                                                   [100%]
6 passed in 0.02s
```

Combined observed execution: **34 passed in 0.04s**.

These tests were not rerun during the witness-only search because no calendar classification or test expectation changed. Do not represent a new run where none occurred.

Execution caveat: the container has no direct network route to GitHub. GitHub state/writes/blob verification were handled through the GitHub connector; Python execution used a local materialisation of the versioned calendar classification/evidence logic and tests. This is not a GitHub Actions run or network checkout.

## 6. LATEST OBSERVED COVERAGE VERDICT

Because no calendar record changed, the latest observed coverage state remains:

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
- coverage script exit code: `2`

This is a clean BLOCKED, not FAIL.

## 7. 2019 RESOLUTION STATE

Resolved 2019 candidate dates:

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

The **only unresolved 2019 candidate** remains:

- `2019-07-03` — `INDEPENDENCE_PRE_HOLIDAY_SESSION`

The first unresolved coverage date therefore remains `2019-07-03`.

## 8. 2019-07-03 — DEDICATED WITNESS SEARCH RESULT

A dedicated adversarial search was executed specifically to close the missing broker side of the `2019-07-03` proof.

The search covered:

- indexed Dukascopy company-news pages around 1-5 July 2019;
- exact `USATECH.IDX/USD` + `3 July 2019` / `July 3, 2019`;
- exact `17:15` + Dukascopy + USATECH + 2019;
- multilingual Dukascopy pages;
- exact 2019 publication timestamps;
- external indexed/archive references and RSS/news-digest style mirrors;
- official/social-web searches for Dukascopy Independence-Day trading-hours material.

The search also verified that Dukascopy content genuinely dated `2019-07-03` is indexed, so the failure is not simply explained by the date being absent from the searchable Dukascopy corpus.

Relevant historical witnesses found:

- **2018 official Dukascopy:** exact USATECH July-3 close `17:15 GMT`, reopen `22:00 GMT` — valid for 2018 only.
- **2017 official Dukascopy:** a July-3 USATECH pre-holiday closure exists, but with a different historical time — valid for 2017 only.
- **2015 official Dukascopy:** a July-3 USATECH closure exists for that year's observed holiday — valid for 2015 only.
- **2026 official Dukascopy:** confirms Dukascopy can apply special breaks on a July-3 pre-holiday session in some years — valid for 2026 only.
- **Current Dukascopy range-of-markets:** establishes regular USATECH summer hours, not the 2019 special session.

No materially new, date-specific Dukascopy/USATECH witness for `2019-07-03` was found.

A direct Wayback/CDX request was attempted from the local execution environment but could not execute because that environment has no DNS/network route to `web.archive.org`. That network failure is **not evidence of absence**. Web-index searches for archived copies also produced no qualifying witness.

Full durable research trace:

`reports/data-qualification/dukascopy_usatech_2019_07_03_witness_search.md`

### Verdict for the dedicated search

**BLOCKED**

Reason: `DATE_SPECIFIC_DUKASCOPY_USATECH_2019_07_03_WITNESS_NOT_FOUND`

No special calendar record was created. No test expectation was changed. The exact 2018 July-3 rule remains forbidden as a 2019 substitute. CME-only timing remains insufficient under the locked threshold.

## 9. EVIDENCE DISCIPLINE

- Only complete UTC hourly BI5 buckets proven closed enter `fully_closed_hours_utc`.
- A partially tradable hour remains EXPECTED_OPEN.
- Holiday name alone is not closure evidence.
- HTTP 403/404/503 or missing BI5 data is not closure evidence.
- Do not extrapolate one year's special hours to another year.
- Dukascopy establishes broker special-event context; precise equity-index timing may be supplied by CME evidence when necessary.
- Preserved third-party historical CME schedules remain explicitly labelled mirror evidence.
- Exchange-only evidence does not silently become Dukascopy broker truth where broker treatment is materially uncertain.
- Do not repeat the same `2019-07-03` generic web searches merely to reconstruct this result; consult the versioned witness-search report first.

## 10. HISTORICAL WIDGET ROUTE — CLOSED

Do not restart the historical Trading Breaks widget path unless materially new evidence appears.

The prior route reached the exact historical frame but returned an empty DOM/table after the stale-frame false PASS was detected and corrected. The chosen path remains date-specific archived/primary evidence.

## 11. MULTI-YEAR ACQUISITION GATE

Massive acquisition is still forbidden.

Before acquisition:

1. calendar coverage must reach zero unresolved candidate dates;
2. verdict must be PASS;
3. then freeze the exact >=5-year execution window;
4. only then download native Dukascopy `.bi5` real ticks with manifest/hash/reconciliation;
5. no OHLC M1, interpolation, synthetic or substituted ticks.

## 12. EXACTLY ONE NEXT GOVERNED ACTION

**Formalize an `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP` governance rule for cases where exhaustive retrieval fails to recover a date-specific broker witness. Define the admissible evidence hierarchy and explicit conditions for PASS / FAIL / BLOCKED, then adversarially break that rule before applying it to `2019-07-03`. Do not change the `2019-07-03` calendar classification, do not begin 2020 qualification, and do not begin massive `.bi5` acquisition until this governance rule itself has been qualified.**
