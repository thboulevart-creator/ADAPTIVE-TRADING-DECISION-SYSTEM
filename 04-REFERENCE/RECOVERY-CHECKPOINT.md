# RECOVERY CHECKPOINT — 13 SEPTEMBRE 2026 — MULTI-YEAR DUKASCOPY CALENDAR COVERAGE

## 1. CURRENT STATE

- **Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- **Active branch:** `feat/multi-year-dukascopy-acquisition`
- **Prior checkpoint:** `9ed768cdfb07bb099eb966244764d5aab1fac567`
- **Latest durable backup:** `99-BACKUP/SESSION-2026-09-13-2020-CALENDAR.md`
  - commit `c960d978995f991f9f473d8bc8b0c6c93dfb934d`
- **2020-01-01 qualification report:** `reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`
  - commit `a2c79dd728fa5b886d9cf0e7bdcede36eee92004`
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
9. `tools/dukascopy_usatech_calendar.py`
10. `tools/dukascopy_usatech_calendar_coverage.py`
11. calendar/governance tests and actual GitHub state

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

Current permission matrix remains:

- continue later chronological qualification: **PASS**;
- declare global coverage PASS: **BLOCKED**;
- freeze execution window: **BLOCKED**;
- authorize massive acquisition: **BLOCKED**.

Later qualification may continue while earlier BLOCKED dates remain explicitly preserved.

## 5. CALENDAR STATE

The authoritative current calendar blob is again exactly:

`971999e86090267464b794b9427f379dddd89060`

It contains **24** date-specific special-session evidence records inside the global coverage envelope.

There is **no current `2020-01-01` special-session record**.

The transient test `tests/test_dukascopy_usatech_calendar_2020.py` has been removed and is absent from GitHub.

Current-state local materialisation after correction:

```text
..................................                                       [100%]
34 passed, 1 deselected in 0.04s
```

The deselected rejected-candidate test exists only in local scratch materialisation. The current GitHub calendar suite remains the original 34 tests.

Current coverage execution:

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
- coverage exit-code semantics: `2`

The first global unresolved remains `2019-07-03`.

## 6. LOCKED HISTORICAL GAPS

### `2019-07-03 — INDEPENDENCE_PRE_HOLIDAY_SESSION`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

No new qualifying evidence appeared in this continuation. Do not reopen generic searches without materially new evidence.

### `2020-01-01 — NEW_YEARS_OBSERVED`

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

Recovered evidence:

- official Dukascopy 20-Dec-2019 Christmas/New-Year CFD context;
- exact preserved 2019/2020 CME/Globex New-Year schedule.

Missing PASS-bearing broker evidence:

- no B0 exact primary USATECH witness for `2020-01-01`;
- no B1 exact archived USATECH witness;
- no B2 exact-date broker event explicitly naming `USATECH.IDX/USD`;
- no B3 official special-session mapping contract from Dukascopy USATECH to CME.

Therefore exact exchange timing cannot be promoted to broker truth.

Observed gate decision:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## 7. FALSE-PASS CANDIDATE — BROKEN AND REVOKED

A transient candidate initially treated `2020-01-01` as the second day of the exact Dec-31-2019 / Jan-1-2020 event already used for `2019-12-31`.

That route was broken because:

- the retrievable Dukascopy announcement is generic to Christmas/New-Year CFD closures and does not explicitly name USATECH for Jan 1;
- no B3 special-session mapping contract exists;
- same-event identity does not replace the broker/instrument linkage required by the qualified governance rule.

Transient commits retained only for audit history:

- `9b6160ddf81813fd23b6c3ae8a1c508532fdf67a` — false candidate calendar record;
- `7d5789c87fd2946b449f8f6428ae2ebb70dd282b` — restoration of four historical comment lines accidentally lost during replacement;
- `c79a2a7caf0b96e86f9ce94c04fae2581b47062a` — false candidate test.

Correction commits:

- `8170c4b5b638373a5967cd382d3929b89e048d51` — restored calendar to exact authoritative blob `971999e...`;
- `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582` — removed false candidate test.

Before adding reports/backups, GitHub comparison against checkpoint `9ed768...` showed no effective file diff, proving the executable baseline was fully restored.

Do not resurrect the rejected route without materially new evidence that satisfies B0/B1/PASS-C.

## 8. AUXILIARY BRANCH INCIDENT

An accidental auxiliary branch exists:

`__noop_should_not_exist__`

It was created during the correction workflow. The available connector exposed branch ref movement but no branch-ref deletion operation.

It was aligned to correction commit `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582`, whose technical calendar/test tree matches the governed baseline. It is not an authorized work branch and MUST NOT be used.

Delete it when a supported branch-deletion route becomes available. Its existence is a tooling cleanup debt, not project architecture.

## 9. ACQUISITION / WINDOW STATE

- Global coverage remains BLOCKED.
- Execution window remains undefined and unfrozen.
- No window may be chosen merely to evade `2019-07-03` or `2020-01-01`.
- Massive native `.bi5` acquisition remains forbidden.
- No `.bi5` was downloaded during this continuation.

## 10. EXACTLY ONE NEXT GOVERNED ACTION

**Continue chronological 2020 calendar qualification with `2020-01-20` — Martin Luther King Jr. Day — using the same date-specific broker evidence threshold. Preserve `2019-07-03` and `2020-01-01` as explicit BLOCKED global-envelope records. Do not freeze an execution window and do not download `.bi5`.**
