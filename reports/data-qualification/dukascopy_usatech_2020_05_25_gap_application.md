# DUKASCOPY USATECH — 2020-05-25 MEMORIAL DAY GAP APPLICATION

## Target

- Date: `2020-05-25`
- Candidate reason: `MEMORIAL_DAY`
- Broker instrument: `USATECH.IDX/USD`
- Required fact: exact special-session treatment at hourly UTC BI5 granularity.
- Governing rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

## Starting state

- `2019-07-03`: BLOCKED, preserved.
- `2020-01-01`: BLOCKED, preserved.
- `2020-01-20`: BLOCKED, preserved.
- `2020-02-17`: previously qualified PASS, locked.
- `2020-04-10`: BLOCKED, preserved.
- Global calendar coverage before this application: 24 resolved / 87 unresolved / BLOCKED.
- Execution window: undefined and unfrozen.
- Massive `.bi5` acquisition: forbidden.

## Same-date exchange/reference evidence recovered

### CME Group official Memorial Day 2020 advisory

`https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-memorial-day-advisory.pdf`

The CME Group memorandum explicitly identifies `Memorial Day May 25, 2020` and the associated holiday processing/trading-calendar context.

### Preserved CME Globex Control Center summary

`https://www.ampfutures.com/news/holiday-trading-schedule-memorial-day-2020`

The preserved summary records:

- Monday `2020-05-25`;
- early market `HALT` at noon Chicago;
- normal reopening thereafter.

For the strongest favorable application of the governance rule, the exact same-date exchange/reference side is treated as present and verified.

## Targeted Dukascopy retrieval

Searches covered:

- exact `2020-05-25`, `25 May 2020`, and `Monday 25 May 2020` formulations;
- `Memorial Day` / `market closures` title variants;
- exact `USATECH.IDX/USD` + Memorial Day + 2020 queries;
- Swiss and Europe `about/ournews` / `full-news` routes;
- multilingual Dukascopy variants;
- searches around publication dates immediately preceding `2020-05-25`;
- external indexed/archive-style references.

The searchable Dukascopy corpus clearly contains pages and market-research material dated `2020-05-22` and `2020-05-25`, so the target period itself is represented in the indexed historical corpus.

However, no qualifying Dukascopy 2020 Memorial-Day witness was recovered that explicitly names `USATECH.IDX/USD` and establishes the target special-session hours.

Historical/future Dukascopy Memorial-Day pages were recovered for other years, including:

- 2017: exact USATECH schedule;
- 2018: exact USATECH schedule;
- 2021/2022: Memorial-Day closure notices;
- 2024/2025/2026: later Memorial-Day closure notices.

These remain corroborative-only and cannot substitute for the exact 2020 broker witness.

A currently indexed Dukascopy page titled `MARKET CLOSURES on Monday 25 May` is dated 2026, not 2020, and is not admissible as a 2020 witness despite the matching calendar date/title pattern.

## Evidence classification under V1

- B0 exact primary broker witness: **absent**.
- B1 exact archived broker witness with verified provenance: **absent**.
- B2 exact-date broker event explicitly naming `USATECH.IDX/USD`: **absent**.
- B3 official Dukascopy special-session mapping contract to CME/reference product: **absent**.
- Exact same-date exchange/reference evidence: **present**.
- Exchange provenance: **accepted for strongest favorable application**.
- Strong broker contradiction: **none found**.
- Retrieval materially exhausted for the currently available routes: **yes**.

## Adversarial checks

The following false-PASS routes are explicitly rejected:

1. **CME timing only -> PASS**: forbidden; exchange timing is not broker truth.
2. **2017/2018 exact Dukascopy USATECH Memorial schedules -> infer 2020**: forbidden cross-year extrapolation.
3. **2021/2022/2024/2025/2026 Dukascopy Memorial notices -> infer 2020**: forbidden cross-year substitution.
4. **Same calendar date/title in 2026 (`Monday 25 May`) -> infer historical identity**: forbidden; publication year and target event differ.
5. **Absence of a retrievable 2020 page -> closure proof**: forbidden.
6. **Market-data absence or future `.bi5` behavior -> closure proof**: forbidden and no `.bi5` was downloaded.

No FAIL-producing contradiction or falsified witness was identified. The case is missing required broker evidence rather than proving conflicting broker facts.

## Gate application

Under the strongest favorable exchange assumption:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## Verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

This is an absence-of-proof verdict. It does not assert that Dukascopy USATECH was open or closed at any particular hour on `2020-05-25`.

## Repository consequences

- No `2020-05-25` special-session calendar record is added.
- No test expectation is changed.
- Existing resolved-count remains 24.
- Existing unresolved-count remains 87.
- Global calendar coverage remains BLOCKED.
- `2019-07-03`, `2020-01-01`, `2020-01-20`, and `2020-04-10` remain BLOCKED.
- `2020-02-17` remains locked as already qualified.
- No execution window is frozen.
- No `.bi5` acquisition is authorized or performed.

## Next chronological unresolved candidate

`2020-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

This next date must be qualified independently under the same evidence threshold. `2020-07-03 — INDEPENDENCE_DAY_OBSERVED` follows after it and must not be collapsed into the pre-holiday qualification.