# SESSION BACKUP — 2026-09-13 — 2020 CALENDAR QUALIFICATION

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint for 2020 continuation: `9ed768cdfb07bb099eb966244764d5aab1fac567`
- Checkpoint before Memorial-Day qualification: `c14c84a3e85ebee9ac3de31a3a8bda29676618c2`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Governing boundary: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`
- Governing historical-gap rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

## Governed permission

Chronological qualification may continue while unresolved historical gaps remain durably preserved.

This does NOT authorize:

- global coverage PASS;
- execution-window freeze;
- massive `.bi5` acquisition.

## Locked historical gaps

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Unchanged.

### `2020-01-01 — NEW_YEARS_OBSERVED`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`

The initial false-PASS route was broken and fully revoked. No Jan-1 record/test remains.

### `2020-01-20 — MARTIN_LUTHER_KING_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_01_20_gap_application.md`

Exact same-date CME/Globex evidence exists, but no B0/B1/B2/B3 Dukascopy link was recovered.

### `2020-04-10 — GOOD_FRIDAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_04_10_gap_application.md`

Exact same-date CME/Globex evidence exists, but no qualifying 2020 Dukascopy USATECH link was recovered.

### `2020-05-25 — MEMORIAL_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_05_25_gap_application.md`

Report commit:

`807f24d11dc4c9702523791c1d719124b30aabc9`

## `2020-05-25` evidence recovered

Official CME Group Memorial Day 2020 advisory:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-memorial-day-advisory.pdf`

The CME memorandum explicitly identifies `Memorial Day May 25, 2020` and the related holiday-processing/trading-calendar context.

Preserved CME Globex Control Center summary:

`https://www.ampfutures.com/news/holiday-trading-schedule-memorial-day-2020`

It records:

- Monday `2020-05-25`;
- early market HALT at noon Chicago;
- normal reopening thereafter.

The exact same-date exchange/reference side is accepted for the strongest favorable gate application.

## `2020-05-25` missing broker link

Targeted Dukascopy retrieval covered:

- exact May-25-2020 date variants;
- Memorial Day / market-closure title variants;
- exact `USATECH.IDX/USD` searches;
- Swiss/Europe company-news routes;
- multilingual variants;
- publication dates immediately preceding the holiday;
- external indexed/archive-style searches.

No qualifying 2020 Dukascopy USATECH witness was recovered.

Dukascopy material recovered for other Memorial-Day years includes:

- 2017 exact USATECH schedule;
- 2018 exact USATECH schedule;
- 2021/2022 Memorial-Day notices;
- 2024/2025/2026 later Memorial-Day notices.

These remain corroborative only and cannot substitute for 2020.

A currently indexed Dukascopy page titled `MARKET CLOSURES on Monday 25 May` is dated 2026 and therefore cannot be relabelled as a 2020 witness.

Missing PASS-bearing evidence:

- B0 exact primary broker witness: absent;
- B1 exact archived broker witness with verified provenance: absent;
- B2 exact-date broker event explicitly naming `USATECH.IDX/USD`: absent;
- B3 official broker special-session mapping contract to CME: absent.

## `2020-05-25` gate application

Under the strongest favorable exchange assumption:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

This is an absence-of-proof verdict, not a claim about the actual Dukascopy close/reopen time.

No `2020-05-25` calendar record was created and no test expectation changed.

## Already-qualified 2020 date — do not reopen

`2020-02-17 — PRESIDENTS_DAY` remains versioned as `SPECIAL_PRESIDENTS_DAY_2020` with exact Dukascopy evidence and stays locked.

## Current executable state

No executable calendar/test code changed during the Memorial-Day qualification.

Therefore the calendar suite and coverage were not rerun merely to generate a newer timestamp.

Latest locked executable state remains:

```text
34 calendar tests PASS
```

Current global coverage remains:

- candidate dates: 111
- resolved candidate dates: 24
- special-session evidence dates: 24
- no-special-change evidence dates: 0
- unresolved candidate dates: 87
- contradictions: none
- evidence-shape errors: none
- orphan special evidence: none
- verdict: BLOCKED
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`

First global unresolved remains `2019-07-03`.

## Auxiliary branch incident

The accidental auxiliary branch `__noop_should_not_exist__` remains a recorded tooling cleanup debt and MUST NOT be used. Delete it only when a supported branch-deletion route is available.

## Locked consequences

- `2019-07-03`: BLOCKED, unchanged.
- `2020-01-01`: BLOCKED, unchanged.
- `2020-01-20`: BLOCKED, unchanged.
- `2020-02-17`: previously qualified, locked.
- `2020-04-10`: BLOCKED, unchanged.
- `2020-05-25`: BLOCKED, irreducible broker-evidence gap.
- global coverage: BLOCKED.
- execution window: not frozen.
- massive `.bi5`: forbidden.
- no `.bi5` was downloaded.

## Exactly one next governed action

**Continue chronological 2020 qualification with `2020-07-02` — `INDEPENDENCE_PRE_HOLIDAY_SESSION` — under the same date-specific broker evidence threshold. Preserve all earlier BLOCKED dates explicitly, keep `2020-02-17` locked as already qualified, do not merge `2020-07-02` with `2020-07-03`, do not freeze an execution window, and do not download `.bi5`.**
