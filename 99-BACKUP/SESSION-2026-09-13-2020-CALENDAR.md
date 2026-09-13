# SESSION BACKUP — 2026-09-13 — 2020 CALENDAR QUALIFICATION

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint for 2020 continuation: `9ed768cdfb07bb099eb966244764d5aab1fac567`
- Checkpoint before Good Friday qualification: `95f5954d581aba459d26f7e0721dce87d5586f66`
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

Report commit:

`77a6b38d9a4ac2c83022ce33b30d457a3ca411d9`

## `2020-04-10` evidence recovered

Official CME Group Good Friday advisory:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-good-friday-advisory.pdf`

The memorandum explicitly identifies `Good Friday, April 10th, 2020` and the associated CME holiday-processing/trading-calendar reference.

Official CME settlement notice:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/good-friday-holiday-settlement-times-2020.pdf`

It states there are no CME Group settlements on Friday `2020-04-10` due to Good Friday.

Preserved CME Globex Control Center summary:

`https://www.ampfutures.com/news/holiday-trading-schedule-good-friday-2020`

The preserved schedule image shows Good Friday `2020-04-10` fully closed across the listed product categories, including equity products.

The exact same-date exchange/reference side is therefore accepted for the strongest favorable gate application.

## `2020-04-10` missing broker link

Targeted Dukascopy retrieval covered:

- exact 10-Apr-2020 date variants;
- `Good Friday` / `Easter weekend market closures 2020`;
- exact `USATECH.IDX/USD` queries;
- Swiss/Europe `about/ournews` and `full-news` routes;
- multilingual Easter variants;
- archive/index-style web searches.

No qualifying 2020 Dukascopy USATECH witness was recovered.

Dukascopy Easter/USATECH material was recovered for other years, including 2017, 2019, 2021, 2025 and 2026. These are corroborative-only and cannot substitute for 2020.

Dukascopy's March 2020 daylight-saving announcement explicitly lists `USATECH.IDX/USD`, proving instrument/schedule context for 2020, but it is not a Good-Friday special-session witness and is not B0/B1/B2/B3 for the target fact.

Missing PASS-bearing evidence:

- B0 exact primary broker witness: absent;
- B1 exact archived broker witness with verified provenance: absent;
- B2 exact-date broker event explicitly naming target instrument: absent;
- B3 official broker special-session mapping contract to CME: absent.

## `2020-04-10` gate application

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

No `2020-04-10` calendar record was created and no test expectation changed.

## Already-qualified 2020 date — do not reopen

`2020-02-17 — PRESIDENTS_DAY` remains versioned as `SPECIAL_PRESIDENTS_DAY_2020` with exact Dukascopy evidence and stays locked.

## Current executable state

No executable calendar/test code changed during the Good Friday qualification.

Therefore the calendar suite and coverage were not rerun merely to create a newer timestamp.

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
- `2020-04-10`: BLOCKED, irreducible broker-evidence gap.
- global coverage: BLOCKED.
- execution window: not frozen.
- massive `.bi5`: forbidden.
- no `.bi5` was downloaded.

## Exactly one next governed action

**Continue chronological 2020 qualification with `2020-05-25` — Memorial Day — under the same date-specific broker evidence threshold. Preserve `2019-07-03`, `2020-01-01`, `2020-01-20`, and `2020-04-10` as explicit BLOCKED global-envelope records; keep `2020-02-17` locked as already qualified. Do not freeze an execution window and do not download `.bi5`.**
