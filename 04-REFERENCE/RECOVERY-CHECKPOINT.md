# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — END OF DAY — ANNUAL DUKASCOPY CALENDAR QUALIFICATION

## 1. CURRENT AUTHORITATIVE STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Checkpoint before end-of-day persistence:** `9e07a2cbbf79607dc5f74e52cf459ad1eca56295`
- **Authoritative end-of-day backup:** `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
  - commit `d9121c64ceac1ff15e0fcde0a7ed425007e44022`
- **Annual protocol:** `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
  - commit `4dec1dcd83259f219c2f6e1aadb0a2216a7315af`
- **2020 annual qualification:** `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
  - commit `04a51fb509d73ed3ed3748fff539d78e9e54cc95`
- **2020 annual audit:** `reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`
  - commit `a5495e234d45263d98c9b15c6d004bf24b62537d`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Execution/backtest window frozen:** NO
- **Massive native `.bi5` acquisition:** FORBIDDEN
- **Real backtest:** NOT authorized
- **Global coverage:** BLOCKED
- **Latest observed coverage counts:** `111 candidates / 24 resolved / 87 unresolved`
- **Latest observed calendar tests:** `34 PASS`

## 2. TOMORROW MORNING — READ ONLY THESE FIRST

Before any substantive action:

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`
9. compare the active branch against this checkpoint's final HEAD before writing anything.

The end-of-day backup contains the detailed history, failures, corrections, commits and evidence logic. Do not reconstruct today's state by searching conversations.

## 3. LOCKED OPERATING METHOD

Project methodology remains governed by `AI-OPERATING-MEMORY.md`.

Calendar research now follows:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Permanent operating unit:

- **research batch = one calendar year**;
- **evidence verdict = one candidate date**;
- **audit = one calendar year**.

Annual batching never weakens date-specific proof.

Every candidate date stays independent.

## 4. LOCKED EVIDENCE GOVERNANCE

### `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict: **PASS**.

Date-level PASS is allowed only through:

- PASS-A exact primary broker witness;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event explicitly covering target instrument + explicit broker special-session mapping contract + exact same-date verified exchange/reference timing.

Exchange-only timing, another year, adjacent dates, generic broker holiday context, missing data, HTTP failure or source majority do not create PASS.

### `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict: **PASS**.

Current action matrix:

- continue annual qualification: **PASS**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive `.bi5` acquisition: **BLOCKED**.

## 5. LOCKED HISTORICAL STATE

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Still the first global unresolved candidate.

### 2020

Complete candidate set: **13**.

Final date-level matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**

Sole PASS:

- `2020-02-17 — PRESIDENTS_DAY` → locked exact Dukascopy evidence.

BLOCKED:

- `2020-01-01`
- `2020-01-20`
- `2020-04-10`
- `2020-05-25`
- `2020-07-02`
- `2020-07-03`
- `2020-09-07`
- `2020-11-26`
- `2020-11-27`
- `2020-12-24`
- `2020-12-25`
- `2020-12-31`

2020 annual audit:

**PASS — `ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`**

2020 calendar coverage:

**BLOCKED — `2020_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

Do not confuse annual-audit PASS with calendar-coverage PASS.

## 6. IMPORTANT CORRECTIONS / DO NOT REPEAT

- The transient false-PASS route for `2020-01-01` was adversarially broken and fully revoked.
- Never use `generic broker context + exact exchange timing + same holiday event` as a PASS route.
- The accidental branch `__noop_should_not_exist__` is cleanup debt only and MUST NOT be used.
- Wayback/archive access failures and HTTP failures are not evidence of broker session behavior or witness absence.
- Do not reopen 2019/2020 locked verdicts unless materially new evidence appears.
- Do not rerun unchanged tests or annual audits only for timestamp freshness.

## 7. EXECUTABLE STATE

No new 2020 annual-batch date earned PASS, therefore no executable calendar update was justified.

Latest observed state remains:

- calendar tests: `34 PASS`;
- `SPECIAL_SESSION_EVIDENCE`: `24` global records;
- candidate dates: `111`;
- resolved: `24`;
- unresolved: `87`;
- contradictions: none in latest observed coverage;
- evidence-shape errors: none in latest observed coverage;
- global verdict: **BLOCKED**;
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`.

## 8. LOCKED UPSTREAM / BACKTEST STATE

- B02–B09 historical qualification: locked;
- B09 final: historical PASS;
- 3.1.1 Momentum V1 definition: PASS;
- 3.1.2 baseline protocol: PASS;
- 3.1.2 actual execution: BLOCKED until verified >=5-year native ticks + realistic execution environment;
- no OHLC M1, interpolation, synthetic ticks or substituted ticks;
- no real backtest yet.

## 9. EXACTLY ONE NEXT GOVERNED ACTION

**Begin and complete the 2021 annual calendar qualification batch.**

Required sequence:

1. verify branch == checkpoint HEAD;
2. enumerate complete 2021 candidates from `candidate_special_dates()`;
3. freeze the exact 2021 candidate list before outcome research;
4. preserve already-qualified 2021 candidates without reopening unless materially new evidence requires it;
5. research all remaining 2021 candidates together;
6. apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently date by date;
7. assign one PASS / FAIL / BLOCKED verdict per date;
8. modify executable calendar evidence only for admissible PASS dates;
9. rerun calendar tests/coverage only if executable evidence changes;
10. create `reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`;
11. perform and record `reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`;
12. preserve all 2019/2020 locked gaps and verdicts;
13. update backup + checkpoint at the end of the 2021 batch.

During this action, do NOT freeze an execution window, download massive `.bi5`, begin a real backtest, or infer broker truth from exchange-only/other-year/adjacent-date evidence.
