# SESSION BACKUP — 2026-09-13 — 2020 CALENDAR QUALIFICATION

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint for 2020 continuation: `9ed768cdfb07bb099eb966244764d5aab1fac567`
- Checkpoint before MLK qualification: `92d9de87dc596277034f842bc50850916487f7eb`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Governing boundary: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`
- Governing historical-gap rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

## Governed permission

The qualified boundary allows chronological qualification to continue into later dates while preserving unresolved historical gaps.

It does NOT authorize:

- global coverage PASS;
- execution-window freeze;
- massive `.bi5` acquisition.

## Locked historical gaps

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Unchanged in the 2020 continuation.

### `2020-01-01 — NEW_YEARS_OBSERVED`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`

The initial false-PASS route was broken and fully revoked. Current calendar blob remains the authoritative pre-candidate blob `971999e86090267464b794b9427f379dddd89060`; no Jan-1 record or test remains.

### `2020-01-20 — MARTIN_LUTHER_KING_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Durable report:

`reports/data-qualification/dukascopy_usatech_2020_01_20_gap_application.md`

Report commit:

`5aba402419cd345247c92b695c14b9e8a0ffb260`

## `2020-01-20` evidence recovered

Official CME Group holiday advisory:

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-mlk-day-advisory.pdf`

The document explicitly identifies Dr. Martin Luther King, Jr. Day as Monday `2020-01-20` and points to CME holiday trading schedules.

Preserved CME Globex Control Center summary:

`https://www.ampfutures.com/news/holiday-trading-schedule-mlk-2020`

The preserved text records the key Monday 20 January 2020 change as:

`Market HALT - Noon Chicago (CST)`

For the strongest favorable application of the governance gate, the same-date exchange/reference side was treated as present and verified.

## `2020-01-20` missing broker link

Targeted Dukascopy retrieval covered:

- exact `2020-01-20`, `20 January 2020` and `20th January` formulations;
- Martin Luther King / MLK page-title variants;
- exact `USATECH.IDX/USD` queries;
- Europe and Swiss `about/ournews` trees;
- multilingual pages;
- external archive-index / mirror queries.

Historical official Dukascopy USATECH MLK schedules were recovered for other years, including 2016, 2017 and 2018. Later generic Dukascopy MLK closure announcements also exist.

None is admissible as a 2020 substitute.

Missing PASS-bearing evidence for `2020-01-20`:

- B0 exact primary Dukascopy USATECH witness: absent;
- B1 exact archived broker witness with verified provenance: absent;
- B2 exact-date broker event explicitly naming `USATECH.IDX/USD`: absent;
- B3 official special-session mapping contract from Dukascopy USATECH to CME: absent.

Cross-year broker examples remain corroborative-only. Exact CME timing cannot silently become broker truth.

## `2020-01-20` gate application

The qualified `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` gate was applied under the strongest favorable exchange assumption:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

This is an absence-of-proof verdict. It does not assert a specific Dukascopy close/reopen schedule for that day.

No `2020-01-20` calendar record was created and no test expectation changed.

## Current executable state

No executable calendar/test code changed during the MLK qualification.

Therefore the calendar suite and coverage were not rerun merely to generate a newer timestamp.

Latest observed current-state execution remains:

```text
..................................                                       [100%]
34 passed
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
- exit-code semantics: 2 for BLOCKED

First global unresolved remains `2019-07-03`.

## Already-qualified 2020 date — do not reopen

`2020-02-17 — PRESIDENTS_DAY` is already versioned in `SPECIAL_SESSION_EVIDENCE` as `SPECIAL_PRESIDENTS_DAY_2020` with exact Dukascopy evidence.

It remains locked and is not rerun merely to reconstruct chronological history.

## Auxiliary branch incident

The accidental auxiliary branch `__noop_should_not_exist__` remains a recorded tooling cleanup debt and MUST NOT be used. It was aligned to a corrected technical state. Delete it only when a supported branch-deletion route is available.

## Locked consequences

- `2019-07-03`: BLOCKED, unchanged.
- `2020-01-01`: BLOCKED, unchanged.
- `2020-01-20`: BLOCKED, irreducible broker-evidence gap.
- `2020-02-17`: previously qualified, locked; do not reopen.
- global coverage: BLOCKED.
- execution window: not frozen.
- massive `.bi5`: forbidden.
- no `.bi5` was downloaded.

## Exactly one next governed action

**Continue chronological 2020 qualification with `2020-04-10` — Good Friday — under the same date-specific broker evidence threshold. Preserve `2019-07-03`, `2020-01-01`, and `2020-01-20` as explicit BLOCKED global-envelope records; keep `2020-02-17` locked as already qualified. Do not freeze an execution window and do not download `.bi5`.**
