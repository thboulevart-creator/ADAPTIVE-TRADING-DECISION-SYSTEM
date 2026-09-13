# DUKASCOPY USATECH — 2020 ANNUAL CALENDAR AUDIT

## Audit identity

- Protocol: `ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`
- Instrument: `USATECH.IDX/USD`
- Year: `2020`
- Qualification report: `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
- Evidence gate: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- Audit objective: verify annual accounting, evidence discipline, locked-state preservation, and anti-bypass invariants.

## Candidate-set completeness

Expected candidates from `candidate_special_dates()` for 2020: **13**.

Qualification-report candidates: **13**.

Expected dates:

- 2020-01-01
- 2020-01-20
- 2020-02-17
- 2020-04-10
- 2020-05-25
- 2020-07-02
- 2020-07-03
- 2020-09-07
- 2020-11-26
- 2020-11-27
- 2020-12-24
- 2020-12-25
- 2020-12-31

Qualification report contains exactly the same date set.

**Check: PASS — no candidate omitted or added.**

## Verdict-domain check

Every candidate has exactly one allowed verdict: PASS / FAIL / BLOCKED.

Observed:

- PASS: 1
- FAIL: 0
- BLOCKED: 12

Total: 13.

**Check: PASS.**

## Locked-state preservation

Previously qualified/blocked dates were not silently rewritten:

- `2020-01-01`: BLOCKED preserved.
- `2020-01-20`: BLOCKED preserved.
- `2020-02-17`: PASS preserved; existing `SPECIAL_PRESIDENTS_DAY_2020` not reopened.
- `2020-04-10`: BLOCKED preserved.
- `2020-05-25`: BLOCKED preserved.

**Check: PASS.**

## Remaining-date evidence threshold

For the eight remaining candidates, the annual research batch did not identify a new admissible broker route under `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`.

For each BLOCKED date:

- exact primary Dukascopy USATECH witness was not recovered;
- exact archived Dukascopy USATECH witness with verified provenance was not recovered;
- PASS-C was not complete because the target-instrument broker link and/or explicit broker special-session mapping contract was absent.

Exchange/reference evidence was retained as corroborative where available and was not promoted to broker truth.

**Check: PASS — no false PASS path accepted.**

## Cross-date inference attack

Attacks considered:

1. Use `2020-07-03` Independence-Day evidence to resolve `2020-07-02`.
   - Rejected.
2. Use Thanksgiving Thursday evidence to resolve Friday.
   - Rejected.
3. Use Christmas-period generic Dukascopy notice to resolve Dec 24, Dec 25 and Dec 31 as a single broker fact.
   - Rejected.
4. Use Dec 31 CME normal closing time as proof of Dukascopy regular USATECH schedule.
   - Rejected.
5. Use another year's exact Dukascopy holiday schedule for the same named holiday.
   - Rejected.

**Check: PASS.**

## Source-role attack

The audit verifies the following distinctions were preserved:

- CME/Globex evidence = exchange/reference evidence, not broker truth.
- generic Dukascopy holiday-period notices = broker context, not exact USATECH hours when the instrument is absent.
- weekend leverage notices = risk/leverage controls, not market-session proof.
- other-year Dukascopy USATECH schedules = corroborative only.

**Check: PASS.**

## Executable calendar consistency

Only `2020-02-17` has a current 2020 special-session record in executable calendar evidence.

No new 2020 PASS was earned by the annual batch, therefore no new calendar record or test expectation was created.

The latest observed calendar suite remains 34 tests PASS from the unchanged executable state.

No rerun was required solely to refresh a timestamp.

**Check: PASS.**

## Coverage-state integrity

The annual batch did not claim that research completion equals coverage completion.

2020 qualification coverage remains:

**BLOCKED**

because 12 candidate dates remain unresolved at the broker-evidence level.

Global 2018–2026 coverage also remains BLOCKED.

**Check: PASS.**

## Boundary integrity

The annual batch did not:

- freeze an execution/backtest window;
- redefine the global coverage envelope;
- authorize massive `.bi5` acquisition;
- begin a backtest;
- use annual completeness to evade earlier historical gaps.

**Check: PASS.**

## Annual audit verdict

**PASS**

Reason:

`ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

This PASS certifies the **annual qualification process and accounting for 2020**.

It does **not** certify 2020 calendar coverage as PASS.

The simultaneously valid state is:

- `2020_ANNUAL_AUDIT`: **PASS**
- `2020_CALENDAR_COVERAGE`: **BLOCKED**
- `GLOBAL_2018_2026_COVERAGE`: **BLOCKED**
- `EXECUTION_WINDOW_FREEZE`: **BLOCKED**
- `MASSIVE_BI5_ACQUISITION`: **BLOCKED**

## Next annual action

Move to **2021 as one annual research batch**.

Before writing any 2021 executable calendar evidence:

1. enumerate and freeze the complete 2021 candidate set from `candidate_special_dates()`;
2. preserve all 2020 verdicts as locked historical state;
3. research all 2021 candidates as a batch;
4. issue independent date-level verdicts;
5. finish with a 2021 annual audit.
