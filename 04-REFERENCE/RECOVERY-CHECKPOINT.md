# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `92d9de87dc596277034f842bc50850916487f7eb`
- **Latest durable backup:** `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
  - latest update commit `15fa513eecd3fb2279443a12218bf2a2f6d750e4`
- **2020-01-01 report:** `reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`
- **2020-01-20 report:** `reports/data-qualification/dukascopy_usatech_2020_01_20_gap_application.md`
  - commit `5aba402419cd345247c92b695c14b9e8a0ffb260`
- **Coverage envelope:** `2018-05-01` → `2026-08-14`
- **Execution/backtest window frozen:** no
- **Massive native `.bi5` acquisition:** forbidden
- **Global coverage verdict:** BLOCKED
- **Global unresolved candidates:** 87
- **First global unresolved:** `2019-07-03`

## 2. RECOVERY ORDER

1. `04-REFERENCE/AI-OPERATING-MEMORY.md`
2. this checkpoint
3. `99-BACKUP/README.md`
4. `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
5. `04-REFERENCE/IRREDUCIBLE-HISTORICAL-BROKER-EVIDENCE-GAP.md`
6. `04-REFERENCE/COVERAGE-ENVELOPE-EXECUTION-WINDOW-BOUNDARY.md`
7. `reports/data-qualification/dukascopy_usatech_2019_07_03_gap_application.md`
8. `reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`
9. `reports/data-qualification/dukascopy_usatech_2020_01_20_gap_application.md`
10. `tools/dukascopy_usatech_calendar.py`
11. `tools/dukascopy_usatech_calendar_coverage.py`
12. calendar/governance tests and actual GitHub state

## 3. LOCKED UPSTREAM STATE — DO NOT REOPEN

- B02–B09 historical qualification remains locked.
- B09 final remains historical PASS.
- 3.1.1 Momentum V1 definition remains PASS.
- 3.1.2 baseline protocol remains PASS.
- 3.1.2 actual execution remains BLOCKED until a verified >=5-year native-tick corpus and realistic execution environment exist.
- No partial/synthetic/fabricated backtest is authorized.
- No OHLC M1, interpolation, synthetic ticks, or substituted ticks are authorized.

## 4. GOVERNANCE RULES — QUALIFIED

### `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

Rule verdict: **PASS**.

Only three PASS routes exist:

- PASS-A exact primary broker witness;
- PASS-B exact archived broker witness with verified provenance;
- PASS-C exact-date broker event explicitly covering target instrument + official broker special-session mapping contract + exact same-date verified exchange/reference timing.

Exchange-only timing, generic broker holiday context, cross-year analogy, missing data, HTTP failures, or majority-of-sources reasoning do not create PASS.

### `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`

Rule verdict: **PASS**.

Current permission matrix:

- continue later chronological qualification: **PASS**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive acquisition: **BLOCKED**.

Later qualification may continue while earlier BLOCKED dates remain explicitly preserved.

## 5. CALENDAR STATE

The authoritative calendar remains unchanged from the prior checkpoint and still contains **24** date-specific special-session evidence records.

There is no current special-session record for:

- `2020-01-01`;
- `2020-01-20`.

No calendar or test code changed during the `2020-01-20` qualification.

Therefore calendar tests/coverage were not rerun merely to create a newer timestamp.

Latest observed executable calendar state remains **34 tests PASS**.

Latest observed global coverage remains:

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
- coverage BLOCKED exit-code semantics: `2`

## 6. LOCKED HISTORICAL GAPS

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

No new qualifying evidence appeared. Do not reopen generic searches without materially new evidence.

### `2020-01-01 — NEW_YEARS_OBSERVED`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

The prior false-PASS candidate was broken and fully revoked. No current calendar/test artifact encodes Jan 1 as resolved.

### `2020-01-20 — MARTIN_LUTHER_KING_DAY`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Recovered same-date exchange/reference evidence:

- official CME Group MLK 2020 advisory:
  `https://www.cmegroup.com/tools-information/holiday-calendar/files/2020-mlk-day-advisory.pdf`
- preserved CME Globex Control Center summary:
  `https://www.ampfutures.com/news/holiday-trading-schedule-mlk-2020`
  - records Monday 20 Jan 2020 `Market HALT - Noon Chicago (CST)`.

Targeted Dukascopy retrieval did **not** recover a qualifying 2020 USATECH witness.

Missing PASS-bearing broker evidence:

- B0 exact primary Dukascopy USATECH witness: absent;
- B1 exact archived broker witness with verified provenance: absent;
- B2 exact-date broker event explicitly naming `USATECH.IDX/USD`: absent;
- B3 official Dukascopy special-session mapping contract to CME: absent.

Official Dukascopy MLK/USATECH schedules from other years are corroborative only and cannot substitute for 2020.

The gate was applied under the strongest favorable exchange assumption and returned:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

This is an absence-of-proof verdict, not a claim that Dukascopy was open or closed at a particular hour.

## 7. ALREADY-QUALIFIED 2020 DATE — DO NOT REOPEN

`2020-02-17 — PRESIDENTS_DAY` is already versioned as `SPECIAL_PRESIDENTS_DAY_2020` with exact Dukascopy evidence.

It remains locked. Do not rerun or re-research it merely to reconstruct chronology.

## 8. AUXILIARY BRANCH INCIDENT

The accidental branch `__noop_should_not_exist__` remains a tooling cleanup debt. It is not an authorized work branch and MUST NOT be used. Delete it only when a supported branch-deletion route is available.

## 9. ACQUISITION / WINDOW STATE

- Global coverage remains BLOCKED.
- Execution window remains undefined and unfrozen.
- No window may be selected merely to evade historical gaps.
- Massive native `.bi5` acquisition remains forbidden.
- No `.bi5` was downloaded during this continuation.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Continue chronological 2020 qualification with `2020-04-10` — Good Friday — under the same date-specific broker evidence threshold. Preserve `2019-07-03`, `2020-01-01`, and `2020-01-20` as explicit BLOCKED global-envelope records; keep `2020-02-17` locked as already qualified. Do not freeze an execution window and do not download `.bi5`.**
