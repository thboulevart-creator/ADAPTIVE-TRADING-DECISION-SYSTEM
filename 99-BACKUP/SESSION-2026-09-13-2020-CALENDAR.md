# SESSION BACKUP — 2026-09-13 — 2020 CALENDAR QUALIFICATION

## Recovery identity

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Active branch: `feat/multi-year-dukascopy-acquisition`
- Starting checkpoint: `9ed768cdfb07bb099eb966244764d5aab1fac567`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Execution/backtest window: NOT frozen
- Massive native `.bi5` acquisition: FORBIDDEN
- Governing boundary: `COVERAGE_ENVELOPE_EXECUTION_WINDOW_BOUNDARY_V1`
- Governing historical-gap rule: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`

## Starting governed permission

The prior qualified boundary allows chronological qualification to continue into 2020 while preserving unresolved historical gaps.

It does NOT authorize:

- global coverage PASS;
- execution-window freeze;
- massive `.bi5` acquisition.

`2019-07-03` remains explicitly BLOCKED and was not modified in this continuation.

## Target processed

`2020-01-01 — NEW_YEARS_OBSERVED`

The intended fact was the exact Dukascopy `USATECH.IDX/USD` special-session classification at hourly UTC BI5 granularity.

## Evidence recovered

Dukascopy official period context:

`https://www.dukascopy.com/swiss/arabic/about/ournews/market-closures-on-christmas-and-new-year-dbl201708`

Published 20 Dec 2019. The retrievable text states that detailed FX/Bullion/CFD closures are in the Trading Breaks Calendar and warns of Christmas/New-Year liquidity/closures.

Exact exchange-side historical schedule mirror:

`https://www.cannontrading.com/tools/support-resistance-levels/new-years-2020-holiday-schedule-cme-globex-ice-exchange/`

This supports the exchange-side New-Year holiday schedule for Dec-31-2019 / Jan-1-2020.

No retrievable Dukascopy source was found that explicitly identifies `USATECH.IDX/USD` on `2020-01-01` with exact treatment, and no official broker special-session mapping contract to CME was found.

## Adversarial break

An initial candidate treated Jan 1 as the second day of the same Dec-31/Jan-1 event already used for `2019-12-31`, combining generic Dukascopy Christmas/New-Year context with exact CME timing.

This candidate was broken against `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`:

- generic holiday-period broker context is not B2 because the target instrument is not explicit;
- no B3 special-session mapping contract exists;
- exchange-only timing cannot become broker truth;
- `same event` cannot silently replace the exact broker/instrument link required by the qualified rule.

Therefore the candidate was rejected.

## Transient commits and correction

Transient false-PASS path:

- `9b6160ddf81813fd23b6c3ae8a1c508532fdf67a` — added `2020-01-01` calendar record;
- `7d5789c87fd2946b449f8f6428ae2ebb70dd282b` — restored four historical comment lines accidentally lost during full-file replacement;
- `c79a2a7caf0b96e86f9ce94c04fae2581b47062a` — added a transient 2020 test.

Correction:

- `8170c4b5b638373a5967cd382d3929b89e048d51` — restored the calendar exactly to authoritative pre-candidate blob `971999e86090267464b794b9427f379dddd89060`;
- `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582` — removed the transient 2020 test.

After correction GitHub compare against starting checkpoint showed no effective file diff before the qualification report was added.

The rejected candidate remains only as auditable Git history, not current calendar truth.

## Durable application report

`reports/data-qualification/dukascopy_usatech_2020_01_01_gap_application.md`

Report commit:

`a2c79dd728fa5b886d9cf0e7bdcede36eee92004`

## Final `2020-01-01` verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

Evidence classes under V1:

- B0: absent
- B1: absent
- B2 explicit target instrument: absent
- B3 special-session mapping contract: absent
- exact exchange timing: present
- exchange provenance: accepted for strongest favorable application
- retrieval materially exhausted: yes

Observed executable gate result:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

No calendar record currently exists for `2020-01-01`.

## Current executable state

After full correction, current GitHub calendar blob is again exactly:

`971999e86090267464b794b9427f379dddd89060`

The transient file `tests/test_dukascopy_usatech_calendar_2020.py` is absent from GitHub.

Observed local current-state materialisation:

```text
..................................                                       [100%]
34 passed, 1 deselected in 0.04s
```

The deselected item exists only in the local scratch materialisation; GitHub contains the original 34 calendar tests only.

Current coverage:

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

## Auxiliary branch incident

An auxiliary branch `__noop_should_not_exist__` was accidentally created while preparing the correction path.

The available GitHub connector did not expose branch-ref deletion. The branch was aligned to correction commit `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582`, whose tree is the same technical calendar/test state as the starting checkpoint.

This branch MUST NOT be used. It should be deleted when branch deletion is available. Its existence is a recorded tooling mistake, not a project architecture decision.

## Locked consequences

- `2019-07-03`: BLOCKED, unchanged.
- `2020-01-01`: BLOCKED, irreducible broker-evidence gap.
- global coverage: BLOCKED.
- execution window: not frozen.
- massive `.bi5`: forbidden.
- no calendar/test PASS claimed for Jan 1 2020.

## Exactly one next governed action

**Continue chronological 2020 qualification with `2020-01-20` — Martin Luther King Jr. Day — under the same date-specific broker evidence threshold, while preserving both `2019-07-03` and `2020-01-01` as explicit BLOCKED global-envelope records. Do not freeze an execution window and do not download `.bi5`.**
