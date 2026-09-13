# SESSION BACKUP — 2026-09-13 — END OF DAY — DUKASCOPY CALENDAR QUALIFICATION

## 0. Purpose

This is the authoritative end-of-day recovery snapshot for the Dukascopy USATECH calendar-qualification workstream.

Tomorrow, do not reconstruct today's state from chat history or search the repository blindly. Read the recovery files in the order below, verify the governed branch/head, then resume from the single next action in section 15.

## 1. Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- End-of-day state before this backup update: `9e07a2cbbf79607dc5f74e52cf459ad1eca56295`
- Coverage envelope: `2018-05-01` through `2026-08-14`
- Instrument: Dukascopy `USATECH.IDX/USD` / internal `USATECHIDXUSD`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Real backtest: NOT authorized
- Global calendar coverage: BLOCKED
- Latest observed coverage: `111 candidates / 24 resolved / 87 unresolved`
- Latest observed executable calendar suite: `34 tests PASS`
- No `.bi5` was downloaded today.

## 2. Mandatory recovery order tomorrow

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. `04-REFERENCE/RECOVERY-CHECKPOINT.md`
3. this file: `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
4. `04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`
8. `reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`
9. compare `feat/multi-year-dukascopy-acquisition` against the checkpoint HEAD recorded in `RECOVERY-CHECKPOINT.md`
10. if identical, begin the 2021 annual batch in section 15.

Repository/versioned artifacts override conversational recollection.

## 3. Durable working method that must be preserved

Project-wide rules from `AI-OPERATING-MEMORY.md` remain mandatory:

- verdicts only `PASS / FAIL / BLOCKED`;
- never turn missing/non-executable evidence into PASS;
- distinguish current violation, architectural exposure, absence of proof, historical evidence and reproducible current evidence;
- qualification flow: `formalisation → candidate → adversarial break → correction → re-break → verdict`;
- verify actual repository/branch state before modifying anything;
- diagnose failures before retrying;
- preserve important work through `Script → Report → Verdict → Conclusion → Recovery Checkpoint` where applicable;
- do not create parasite artifacts merely to make tests pass;
- do not rerun unchanged tests only to manufacture a newer timestamp.

Backtest/data methodology remains locked:

- minimum five years when real backtesting begins;
- real/native ticks only, not OHLC M1 or synthetic/interpolated ticks;
- realistic spread and transaction costs;
- out-of-sample validation;
- robustness testing;
- MT5 `Every tick based on real ticks` when MT5 is used;
- no partial/synthetic/fabricated substitute.

## 4. New annual calendar operating model adopted today

Contract:

`ANNUAL_CALENDAR_QUALIFICATION_PROTOCOL_V1`

Artifact:

`04-REFERENCE/ANNUAL-CALENDAR-QUALIFICATION-PROTOCOL.md`

Commit:

`4dec1dcd83259f219c2f6e1aadb0a2216a7315af`

Permanent rule from now on:

> **Research batch = one complete calendar year.**
>
> **Evidence verdict = one candidate date.**
>
> **Audit = one complete calendar year.**

Annual batching is only an efficiency improvement. It does not weaken the date-specific evidence threshold.

Forbidden shortcuts:

- infer one holiday date from an adjacent date;
- infer a broker schedule from the same holiday in another year;
- promote exchange/CME timing into broker truth;
- promote generic broker holiday context into exact USATECH evidence;
- declare annual coverage PASS because most dates are resolved;
- hide BLOCKED dates;
- confuse annual-audit PASS with annual-calendar-coverage PASS.

Preferred annual artifacts:

- `reports/data-qualification/dukascopy_usatech_<YEAR>_calendar_qualification.md`
- `reports/data-qualification/dukascopy_usatech_<YEAR>_calendar_audit.md`

Previously created date-specific reports remain authoritative historical evidence.

## 5. Governance rule 1 — irreducible historical broker evidence gap

Contract:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict:

**PASS**

Only three routes may create a date-level PASS:

- **PASS-A:** exact primary/live official broker witness for target date + target instrument + relevant hours;
- **PASS-B:** exact archived broker witness with verified provenance;
- **PASS-C:** exact-date broker event explicitly covering target instrument + explicit broker special-session mapping contract + exact same-date verified exchange/reference timing.

Corroborative-only evidence cannot accumulate into PASS, including:

- another year;
- another date in the same holiday period;
- exchange-only timing;
- current regular hours;
- missing `.bi5` / ticks;
- HTTP failures;
- inaccessible archives;
- generic holiday names;
- majority-of-sources reasoning.

When retrieval is materially exhausted and no PASS route is satisfied, the correct verdict is:

`BLOCKED — IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

## 6. Governance rule 2 — coverage / execution / acquisition boundary

Contract:

`COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict:

**PASS**

The following decisions remain separate:

1. continue later qualification;
2. declare global coverage PASS;
3. freeze an execution window;
4. authorize massive acquisition.

End-of-day permission matrix:

- continue later annual qualification: **PASS**;
- global 2018–2026 coverage PASS: **BLOCKED**;
- execution-window freeze: **BLOCKED**;
- massive `.bi5` acquisition: **BLOCKED**.

An earlier unresolved date does not prevent later annual research, but every unresolved date must remain visible. No window may be chosen merely to evade known gaps.

## 7. Historical gap preserved from 2019

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

Verdict:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Exact exchange/reference timing exists, but no admissible exact broker witness or mapping chain was recovered.

This remains the first global unresolved candidate.

Do not reopen generic searches unless materially new broker evidence appears.

## 8. 2020 date-by-date work completed before annual batching

### `2020-01-01 — NEW_YEARS_OBSERVED`

Final verdict:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Important adversarial correction: an initial candidate tried to combine generic Dukascopy Christmas/New-Year CFD context, exact CME timing and same-event identity. That route was broken because the broker source did not explicitly identify `USATECH.IDX/USD` for Jan 1 and no broker special-session mapping contract existed.

Never resurrect this false-PASS route:

`generic broker context + exact exchange timing + same holiday event = PASS`

Transient false-candidate commits retained only for audit history:

- `9b6160ddf81813fd23b6c3ae8a1c508532fdf67a`
- `7d5789c87fd2946b449f8f6428ae2ebb70dd282b`
- `c79a2a7caf0b96e86f9ce94c04fae2581b47062a`

Correction commits:

- `8170c4b5b638373a5967cd382d3929b89e048d51`
- `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582`

No current Jan-1 executable record remains.

### `2020-01-20 — MARTIN_LUTHER_KING_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Exact CME/Globex evidence exists; no admissible 2020 Dukascopy USATECH B0/B1/PASS-C route was recovered.

### `2020-02-17 — PRESIDENTS_DAY`

**PASS**

Already-qualified locked record:

`SPECIAL_PRESIDENTS_DAY_2020`

Do not reopen merely to reconstruct chronology.

### `2020-04-10 — GOOD_FRIDAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Exact CME/Globex evidence exists; no qualifying exact 2020 Dukascopy USATECH link was recovered.

### `2020-05-25 — MEMORIAL_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Exact CME/Globex evidence exists; no qualifying exact 2020 Dukascopy USATECH link was recovered.

Date-specific reports preserved:

- `reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`
- `reports/data-qualification/dukascopy_usatech_2020_01_20_gap_application.md`
- `reports/data-qualification/dukascopy_usatech_2020_04_10_gap_application.md`
- `reports/data-qualification/dukascopy_usatech_2020_05_25_gap_application.md`

## 9. Complete 2020 annual batch completed today

Annual qualification report:

`reports/data-qualification/dukascopy_usatech_2020_calendar_qualification.md`

Commit:

`04a51fb509d73ed3ed3748fff539d78e9e54cc95`

Complete 2020 candidate set: **13**.

Final matrix:

- PASS: **1**
- FAIL: **0**
- BLOCKED: **12**

Sole PASS:

- `2020-02-17 — PRESIDENTS_DAY`

BLOCKED:

- `2020-01-01 — NEW_YEARS_OBSERVED`
- `2020-01-20 — MARTIN_LUTHER_KING_DAY`
- `2020-04-10 — GOOD_FRIDAY`
- `2020-05-25 — MEMORIAL_DAY`
- `2020-07-02 — INDEPENDENCE_PRE_HOLIDAY_SESSION`
- `2020-07-03 — INDEPENDENCE_DAY_OBSERVED`
- `2020-09-07 — LABOR_DAY`
- `2020-11-26 — THANKSGIVING_DAY`
- `2020-11-27 — THANKSGIVING_FRIDAY`
- `2020-12-24 — CHRISTMAS_PRE_HOLIDAY_SESSION`
- `2020-12-25 — CHRISTMAS_OBSERVED`
- `2020-12-31 — NEW_YEARS_EVE_CANDIDATE`

2020 annual calendar coverage verdict:

**BLOCKED — `2020_HAS_UNRESOLVED_BROKER_SESSION_EVIDENCE_GAPS`**

Annual research recovered strong exact exchange/reference material for U.S. holidays, plus some Dukascopy 2020 context including daylight-saving and Christmas/New-Year notices. No new exact/archived 2020 broker witness explicitly naming `USATECH.IDX/USD` with the target holiday hours was recovered for the remaining candidates.

## 10. 2020 annual audit completed today

Audit report:

`reports/data-qualification/dukascopy_usatech_2020_calendar_audit.md`

Commit:

`a5495e234d45263d98c9b15c6d004bf24b62537d`

Audit verdict:

**PASS**

Reason:

`ALL_2020_CANDIDATES_ACCOUNTED_FOR_WITH_DATE_LEVEL_VERDICTS_AND_NO_FALSE_PASS_BYPASS`

The audit verified:

- 13/13 candidates accounted for;
- exactly one PASS/FAIL/BLOCKED verdict per candidate;
- prior locked verdicts preserved;
- no candidate silently omitted;
- no cross-date inference;
- no cross-year substitution;
- no exchange-only promotion to broker truth;
- no generic holiday notice promoted to exact USATECH hours;
- no executable calendar record without date-level PASS;
- unresolved dates remain visible;
- annual-audit PASS not misrepresented as calendar-coverage PASS.

Critical distinction:

- `2020_ANNUAL_AUDIT = PASS`
- `2020_CALENDAR_COVERAGE = BLOCKED`
- `GLOBAL_2018_2026_COVERAGE = BLOCKED`

## 11. Executable state at end of day

No new 2020 candidate earned PASS during the annual batch, so no executable calendar change was justified.

Latest observed state remains:

- calendar tests: **34 PASS**;
- global `SPECIAL_SESSION_EVIDENCE`: **24** records;
- global candidates: **111**;
- globally resolved: **24**;
- globally unresolved: **87**;
- contradictions: none in latest observed coverage;
- evidence-shape errors: none in latest observed coverage;
- global coverage: **BLOCKED**;
- reason: `SPECIAL_SESSION_EVIDENCE_COVERAGE_INCOMPLETE`.

Tests were intentionally not rerun because executable calendar/test code did not change.

## 12. Failure / correction / cleanup debt to remember

### False-PASS attempt on `2020-01-01`

Detected adversarially and fully revoked. Never reuse the rejected inference route without materially new PASS-bearing broker evidence.

### Accidental auxiliary branch

Tooling mistake:

`__noop_should_not_exist__`

Rules:

- MUST NOT use it;
- delete only when a supported branch-deletion path becomes available;
- do not create more auxiliary branches for this calendar work;
- treat as cleanup debt, not architecture.

### Archive/network limitations

Unavailable Wayback/CDX/archive routes, HTTP failures and missing pages are not evidence of broker closure/opening or witness non-existence.

## 13. Work that must not be repeated tomorrow without new evidence

Do not repeat generic searches for:

- `2019-07-03`;
- any of the 12 BLOCKED 2020 dates;
- `2020-02-17` PASS.

Reopen a locked date only if materially new evidence can affect B0/B1/PASS-C or reveals a contradiction/provenance defect.

Do not rerun the 2020 annual audit just to refresh timestamps.

## 14. Global project boundaries still in force

- global 2018–2026 calendar coverage: **BLOCKED**;
- execution/backtest window: undefined and NOT frozen;
- massive native `.bi5` acquisition: **FORBIDDEN**;
- real backtest execution: **BLOCKED**;
- B02–B09 historical qualification: locked;
- B09 final: historical PASS;
- 3.1.1 Momentum V1 definition: PASS;
- 3.1.2 baseline protocol: PASS;
- 3.1.2 actual execution: BLOCKED until verified >=5-year native ticks and realistic execution environment exist;
- no OHLC M1, interpolation, synthetic ticks or substituted ticks are authorized.

## 15. Exactly one next governed action for tomorrow

**Begin and complete the 2021 annual calendar qualification batch.**

Required sequence:

1. Verify the branch is identical to the Recovery Checkpoint HEAD.
2. Use `candidate_special_dates()` to enumerate the complete 2021 candidate set.
3. Freeze that exact list before researching outcomes.
4. Identify any 2021 candidate already qualified in current `SPECIAL_SESSION_EVIDENCE`; preserve it unless materially new evidence requires reopening.
5. Research all remaining 2021 candidates together as one annual evidence campaign.
6. Apply `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1` independently to every candidate date.
7. Give every candidate exactly one verdict: PASS / FAIL / BLOCKED.
8. Only dates earning an admissible PASS may modify executable calendar evidence.
9. If executable calendar evidence changes, rerun relevant calendar tests and coverage before audit.
10. If executable code does not change, do not rerun tests merely for timestamp freshness.
11. Create/update `reports/data-qualification/dukascopy_usatech_2021_calendar_qualification.md`.
12. Perform the separate 2021 annual audit and create `reports/data-qualification/dukascopy_usatech_2021_calendar_audit.md`.
13. Preserve every 2019/2020 gap and locked verdict unless materially new evidence appears.
14. Update this backup and `RECOVERY-CHECKPOINT.md` at the end of the 2021 batch.

Do NOT during this action:

- freeze an execution window;
- choose a window to avoid gaps;
- download massive `.bi5` data;
- begin a real backtest;
- use exchange-only timing as broker truth;
- infer one 2021 candidate from another date or year.

## 16. End-of-day locked summary

At close of 13 September 2026:

- working methodology is durably documented;
- historical broker-evidence-gap governance rule = PASS;
- coverage/execution-boundary governance rule = PASS;
- annual qualification protocol is adopted and versioned;
- `2019-07-03` remains BLOCKED;
- all 13 candidates for 2020 have explicit date-level verdicts;
- 2020 = **1 PASS / 0 FAIL / 12 BLOCKED**;
- 2020 annual audit = **PASS**;
- 2020 annual calendar coverage = **BLOCKED**;
- global coverage = **111 candidates / 24 resolved / 87 unresolved / BLOCKED**;
- execution window remains unfrozen;
- `.bi5` acquisition remains forbidden;
- no real backtest is authorized;
- tomorrow starts directly with the full 2021 annual batch.

There is no need tomorrow to reconstruct today's work from chat history. This snapshot, the Recovery Checkpoint and the annual protocol are sufficient to resume safely.
