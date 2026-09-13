# DUKASCOPY USATECH — 2020-01-01 EVIDENCE-GAP APPLICATION

## 1. Target

- Instrument: `USATECHIDXUSD` / Dukascopy `USATECH.IDX/USD`
- Date: `2020-01-01`
- Candidate reason: `NEW_YEARS_OBSERVED`
- Fact to prove: exact broker special-session treatment at hourly UTC BI5 granularity.
- Governance contract applied: `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`
- Global coverage envelope: `2018-05-01` through `2026-08-14`
- Execution window: NOT frozen
- Native `.bi5` acquisition: NOT authorized

## 2. Evidence recovered

### Dukascopy broker context

Dukascopy published `Market closures on Christmas and New Year` on 20 December 2019:

`https://www.dukascopy.com/swiss/arabic/about/ournews/market-closures-on-christmas-and-new-year-dbl201708`

The publication states that detailed FX, Bullion and CFD closures are in the Trading Breaks Calendar and warns about low liquidity throughout the Christmas/New-Year period.

This is genuine exact-period Dukascopy context. However, the retrievable publication text does **not** explicitly name `USATECH.IDX/USD` for `2020-01-01` and does not expose the exact USATECH close/reopen hours.

Therefore it is not B0, not B1, and not B2 under the qualified governance rule.

### Exchange/reference timing

A preserved New Year 2020 CME/Globex schedule is available at:

`https://www.cannontrading.com/tools/support-resistance-levels/new-years-2020-holiday-schedule-cme-globex-ice-exchange/`

The preserved schedule identifies the Dec-31-2019 / Jan-1-2020 holiday window and supports the exchange-side conclusion that Equity Products are closed on January 1 until the evening reopening. At UTC hourly granularity this would support `00-22 UTC` closed and `23 UTC` reopened.

This is useful exact-date exchange evidence, but exchange timing cannot become Dukascopy broker truth without a valid broker linkage route.

## 3. Evidence classes under V1

- B0 exact primary broker witness: **ABSENT**
- B1 exact archived broker witness: **ABSENT**
- B1 provenance verified: **N/A**
- B2 exact-date broker event explicitly covering target instrument: **ABSENT**
- target instrument explicitly identified by broker source: **NO**
- B3 official broker-to-exchange special-session mapping contract: **ABSENT**
- X0/X1 exact same-date exchange/reference timing: **PRESENT**
- exchange/reference provenance: **treated as verified for strongest favorable application**
- strong broker contradiction: **NO**
- witness identity mismatch: **NO qualifying broker witness to mismatch**
- retrieval materially exhausted: **YES**

Search/retrieval covered the exact Dukascopy 2019 Christmas/New-Year announcement, exact `USATECH` + `2020-01-01` / `1 January 2020` variants, New-Year wording, multilingual Dukascopy indexing, and preserved exchange schedules. No exact broker/instrument witness was recovered. Direct historical widget reconstruction remains a closed path unless materially new evidence appears; archive/network limitations are not treated as evidence of absence.

## 4. Adversarial break of the initial candidate

An initial candidate attempted to reuse the exact Dec-31-2019 / Jan-1-2020 event already used to qualify `2019-12-31` and combine the generic Dukascopy holiday announcement with exact CME timing.

That candidate was attacked against `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`.

It failed because:

1. the Dukascopy 20-Dec-2019 retrievable text does not explicitly identify `USATECH.IDX/USD` for Jan 1;
2. no B3 contract proves that Dukascopy USATECH special/holiday timing automatically inherits the CME equity-index holiday schedule;
3. `same holiday event` is not a substitute for the missing exact broker/instrument link;
4. exchange-only timing remains corroborative without B0/B1 or complete PASS-C.

Therefore the apparent route:

`same holiday event + generic Dukascopy CFD context + exact CME timing -> PASS`

is rejected as a false-PASS route.

## 5. Transient implementation and full correction

The false candidate briefly produced these commits before the adversarial break completed:

- `9b6160ddf81813fd23b6c3ae8a1c508532fdf67a` — transient `2020-01-01` calendar record;
- `7d5789c87fd2946b449f8f6428ae2ebb70dd282b` — restored four baseline comment lines accidentally lost during full-file replacement;
- `c79a2a7caf0b96e86f9ce94c04fae2581b47062a` — transient 2020 test.

The candidate was then fully revoked:

- `8170c4b5b638373a5967cd382d3929b89e048d51` — restored `tools/dukascopy_usatech_calendar.py` exactly to prior authoritative blob `971999e86090267464b794b9427f379dddd89060`;
- `f3b5974e83e0a6dbedbdbe3bed3e28227f1cb582` — removed the transient 2020 test.

GitHub comparison after correction shows **no effective file diff** versus checkpoint `9ed768cdfb07bb099eb966244764d5aab1fac567` before this report was added.

The failed candidate remains in Git history as an auditable experiment; it is not current calendar truth.

## 6. Executable gate application

The qualified gate was applied using the strongest favorable exchange-side bundle:

- `exact_exchange_schedule=True`
- `exchange_provenance_verified=True`
- `retrieval_exhausted=True`
- all B0/B1/B2/B3 PASS-bearing broker fields absent

Observed decision:

```text
GapDecision(
    verdict='BLOCKED',
    reason='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP',
    route=None,
    contract='IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1'
)
```

## 7. Current executable state after correction

The restored current calendar state was re-executed locally from the versioned classification logic:

```text
..................................                                       [100%]
34 passed, 1 deselected in 0.04s
```

The deselected item was the transient rejected `2020-01-01` test in the local scratch materialisation only; it is absent from GitHub.

Current coverage after removing the rejected candidate:

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
- conceptual coverage exit code: `2`

The first global unresolved date remains `2019-07-03`.

## 8. Final date verdict

**BLOCKED**

Reason:

`IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`

`2020-01-01` is not added to `SPECIAL_SESSION_EVIDENCE` and is not marked resolved.

## 9. Auxiliary branch incident

During the correction workflow an accidental auxiliary branch named `__noop_should_not_exist__` was created. The currently available GitHub connector exposes branch creation/ref movement but no branch-ref deletion action.

The auxiliary branch was therefore force-aligned to the then-current governed HEAD so it carries no divergent technical state. It MUST NOT be used as a work branch and should be deleted when a supported branch-deletion path is available.

This incident does not alter the active branch state or calendar verdict but is recorded for recovery transparency.

## 10. Governance consequences

- `2019-07-03` remains BLOCKED and untouched.
- `2020-01-01` is now also BLOCKED as an irreducible broker-evidence gap.
- The boundary rule still permits later chronological qualification while prior BLOCKED dates remain visible.
- Global coverage remains BLOCKED.
- No execution window is frozen.
- Massive `.bi5` acquisition remains forbidden.

## 11. Next chronological action

Proceed to `2020-01-20` — Martin Luther King Jr. Day — under the same date-specific evidence threshold, while preserving both historical BLOCKED gaps explicitly.
