# DUKASCOPY USATECH — 2021 ANNUAL CALENDAR AUDIT

## 1. Audit verdict

**PASS**

Reason:

`ALL_2021_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

Important separation:

- `2021_ANNUAL_AUDIT = PASS`
- `2021_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

This audit PASS certifies annual accounting and evidence discipline only. It does not certify that 2021 broker-session coverage is complete.

## 2. Audited artifacts and identities

Repository:

`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:

`feat/multi-year-dukascopy-acquisition`

Starting governed checkpoint:

`f4938f2823412aef3df65d6fd30408f2036d2b88`

Candidate generator:

`tools/dukascopy_usatech_calendar_coverage.py`

Generator blob:

`dceedb8b2b9d27c121b816e5ce0bd36ef572b1bb`

2021 qualification report:

`reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`

Candidate freeze commit:

`d8083da25951d1f506179c39bfba1691ef53c60c`

Completed qualification commit:

`2f6531a72e85a91382564305193d67985fe544ac`

Evidence-gap gate:

`tools/irreducible_historical_broker_evidence_gap.py`

Gate blob:

`1b152b9d1d3ac4c3da135db1528cfb1f687d3a05`

## 3. Completeness audit

Frozen candidate count: **13**.

Qualification-report candidate count: **13**.

Every frozen candidate has exactly one final verdict.

Final matrix:

- PASS: **0**
- FAIL: **0**
- BLOCKED: **13**

No candidate was omitted after the evidence campaign.

No candidate was added after research to manufacture a desired result.

## 4. Candidate-by-candidate accounting

1. `2021-01-01 — NEW_YEARS_OBSERVED` → BLOCKED
2. `2021-01-18 — MARTIN_LUTHER_KING_DAY` → BLOCKED
3. `2021-02-15 — PRESIDENTS_DAY` → BLOCKED
4. `2021-04-02 — GOOD_FRIDAY` → BLOCKED
5. `2021-05-31 — MEMORIAL_DAY` → BLOCKED
6. `2021-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION` → BLOCKED
7. `2021-07-05 — INDEPENDENCE_DAY_OBSERVED` → BLOCKED
8. `2021-09-06 — LABOR_DAY` → BLOCKED
9. `2021-11-25 — THANKSGIVING_DAY` → BLOCKED
10. `2021-11-26 — THANKSGIVING_FRIDAY` → BLOCKED
11. `2021-12-23 — CHRISTMAS_PRE_HOLIDAY_SESSION` → BLOCKED
12. `2021-12-24 — CHRISTMAS_OBSERVED` → BLOCKED
13. `2021-12-31 — NEW_YEARS_EVE_CANDIDATE` → BLOCKED

## 5. Adversarial anti-bypass audit

### Cross-year substitution

PASS-bearing exact USATECH schedules from other years were not reused as 2021 broker truth.

**PASS**

### Adjacent-date substitution

No pre-holiday, holiday, Thanksgiving pair, Christmas pair, or New-Year date was allowed to validate another date automatically.

**PASS**

### Exchange-only promotion

CME/Nasdaq/reference evidence was not promoted into Dukascopy broker truth.

**PASS**

### Generic broker notice promotion

Exact-date/period Dukascopy notices that only state special CFD/Bullion closures and delegate detailed hours to the Trading Breaks Calendar were not promoted into exact `USATECH.IDX/USD` schedule witnesses.

**PASS**

### Annual-majority shortcut

No annual PASS was declared merely because holiday context or external exchange evidence exists for most dates.

**PASS**

### Hidden-gap check

All 13 unresolved 2021 candidates remain explicitly visible as BLOCKED.

**PASS**

### Executable-evidence check

No 2021 `SPECIAL_SESSION_EVIDENCE` record was added without a date-level PASS.

**PASS**

### Window/acquisition bypass

No execution window was frozen and no `.bi5` acquisition or real backtest was authorized by completion of the annual batch.

**PASS**

## 6. Evidence-governance audit

The governing `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` threshold was preserved:

- PASS-A requires exact primary broker date + instrument + hours;
- PASS-B requires exact archived broker witness with verified provenance;
- PASS-C requires exact-date broker event + target instrument explicit + explicit broker special-session mapping contract + exact verified exchange/reference schedule.

The 2021 campaign recovered some exact-date Dukascopy event notices, but no candidate satisfied one of the complete PASS routes.

Under a strongest-favorable adversarial check, granting the external exchange side does not create PASS-C because the required broker target-instrument/mapping chain remains absent.

The 13 BLOCKED verdicts are therefore compatible with the qualified gate and do not represent false FAILs or false PASSes.

## 7. Executable-state audit

No 2021 candidate earned PASS.

Therefore no executable calendar evidence change was warranted.

Observed governed state remains:

- `tools/dukascopy_usatech_calendar.py`: unchanged by 2021 batch;
- global `SPECIAL_SESSION_EVIDENCE`: **24** records in latest observed state;
- calendar tests: latest observed **34 PASS**;
- global candidate dates: **111**;
- globally resolved: **24**;
- globally unresolved: **87**;
- global coverage verdict: **BLOCKED**;
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`.

Because executable calendar/test code did not change, the test suite was intentionally not rerun merely to generate a newer timestamp.

## 8. Historical preservation audit

The following locked historical state remains unchanged:

- `2019-07-03` remains BLOCKED;
- all 2020 BLOCKED dates remain BLOCKED;
- `2020-02-17 — PRESIDENTS_DAY` remains the locked 2020 PASS;
- the 2020 annual audit remains PASS;
- the 2020 annual calendar coverage remains BLOCKED.

No prior verdict was reopened merely to conduct the 2021 batch.

## 9. Final annual distinction

2021 research/accounting is complete.

Therefore:

**2021 ANNUAL AUDIT: PASS**

But because all 13 date-level broker-session facts remain unresolved:

**2021 CALENDAR COVERAGE: BLOCKED — `2021_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

This does not authorize global coverage PASS, execution-window freeze, `.bi5` acquisition, or real backtest execution.
