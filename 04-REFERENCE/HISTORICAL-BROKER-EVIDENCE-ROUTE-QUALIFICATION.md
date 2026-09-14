# HISTORICAL BROKER EVIDENCE ROUTE QUALIFICATION

## Status

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

## 1. Purpose

This gate determines whether a materially new Dukascopy-native historical evidence route can be used to recover exact historical special-session evidence for `USATECH.IDX/USD` inside the already-selected execution-window candidate.

The route is now qualified for **positive historical break recovery**.

This PASS does not change the execution-window boundaries and does not by itself resolve any date that has not been individually queried and evidenced.

Current candidate window remains:

`2021-08-14` → `2026-08-14`.

## 2. Required PASS properties

The qualified route demonstrates all required properties:

1. **Verified Dukascopy provenance** — PASS
   - official Dukascopy widget/runtime and broker-native API responses.
2. **Historical-date addressability** — PASS
   - `currentDate=false` plus explicit historical epoch was observed in real runtime requests.
3. **Explicit target-instrument identity** — PASS
   - broker instrument catalogue maps ID `9016` to `USATECH.IDX/USD`.
4. **Exact special-session timing** — PASS
   - broker-native historical break records provide exact start/end timestamps.
5. **Reproducible retrieval** — PASS
   - GitHub Actions/Playwright captures request, response, DOM, artifact hash and run identity.
6. **Gold-standard calibration** — PASS
   - independently known `2020-02-17 — PRESIDENTS_DAY` reproduced exactly.
7. **Unresolved-date pilot** — PASS
   - mechanically selected `2021-09-06 — LABOR_DAY` recovered exact broker evidence.
8. **No contradiction with locked evidence** — PASS
   - calibration agrees with the independently locked witness.

## 3. Forbidden interpretations remain forbidden

Route PASS does not authorize any of the following shortcuts:

- holiday name alone;
- exchange-only timings;
- current regular trading hours;
- other-year or adjacent-date inference;
- missing `.bi5` / ticks;
- HTTP failures interpreted as market closure;
- empty widget/API response interpreted as regular hours;
- generic broker notices without target-instrument timing;
- JForex weekend offline intervals reused as holiday evidence.

In particular, **absence of a positive Trading Breaks record is not yet qualified as proof that regular hours applied**. A separate completeness/negative-evidence contract would be required before populating `NO_SPECIAL_CHANGE_EVIDENCE` from empty responses.

## 4. Gold-standard calibration — PASS

Report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Final authoritative calibration run:

- run ID: `34866241511`;
- probe head: `231867ae6a78a5db640b84351073ef3835bbb4a3`;
- artifact ID: `10356927580`;
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`.

Locked witness:

`2020-02-17 — PRESIDENTS_DAY`

Recovered broker truth:

- instrument: `USATECH.IDX/USD` / ID `9016`;
- break start: `2020-02-17T18:00:00Z`;
- break end / final closed minute: `2020-02-17T22:59:00Z`;
- derived reopen: `2020-02-17T23:00:00Z`;
- reason: `President's Day`.

Calibration verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Calibrated representation rule:

- `BREAK START TIME` = first closed minute;
- `BREAK END TIME` = final closed minute;
- for these minute-resolution records, reopen instant = `break_end + 60 seconds`.

## 5. Adversarial calibration history

The route was not promoted from the first plausible response:

- headless direct historical document returned HTTP `403` → BLOCKED;
- official builder page returned HTTP `200` but current relative application assets returned `404` → BLOCKED;
- headed Chromium then returned the historical witness, but the first comparator incorrectly demanded a literal `23:00` string and emitted a false negative;
- preserved raw evidence showed `18:00 → 22:59`;
- comparator was corrected to structured interval semantics calibrated against the independently known witness;
- corrected re-break reproduced both DOM and broker-native payload → PASS.

No acceptance threshold or witness date was moved to obtain PASS.

## 6. Unresolved-date pilot — PASS

Report:

`reports/data-qualification/historical_trading_breaks_widget_pilot_2021_09_06.md`

Selection rule:

`EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE`

Pilot date:

`2021-09-06 — LABOR_DAY`

Authoritative run:

- run ID: `34866699952`;
- job ID: `104052206522`;
- run head: `2c875805ef554e0f65c4021ed5ecedadcce48a6f`;
- artifact ID: `10357256669`;
- artifact SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`.

Recovered exact broker record:

```json
{
  "id": "28743",
  "instrument": "9016",
  "start": "1630947600000",
  "end": "1630965540000",
  "reason": "Labor Day"
}
```

UTC semantics:

- break start: `2021-09-06T17:00:00Z`;
- final closed minute: `2021-09-06T21:59:00Z`;
- reopen: `2021-09-06T22:00:00Z`;
- fully closed hourly buckets: `17, 18, 19, 20, 21`.

Rendered DOM independently showed:

`USATECH.IDX/USD    06-Sep-21 17:00:00    06-Sep-21 21:59:00    Labor Day`

Date-level gate:

**PASS-A — exact primary broker date/instrument/timing witness.**

Pilot verdict:

**PASS — `EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED`**

## 7. Final route verdict

Both mandatory falsification stages succeeded under unchanged acceptance rules:

`gold-standard calibration PASS → first unresolved pilot PASS`

Final route verdict:

**PASS — `CALIBRATED_WIDGET_ROUTE_RESOLVES_IN_WINDOW_USATECH_HISTORICAL_SPECIAL_SESSION`**

This PASS means the route is admissible for recovering **positive** historical special-session records for individually addressed candidate dates.

It does not mean every remaining candidate necessarily has a break record.

## 8. Executable consequence already authorized

The pilot itself supplies admissible PASS-A evidence for exactly one previously unresolved date:

`2021-09-06 — LABOR_DAY`

Executable record authorized for that date:

- reason: `SPECIAL_LABOR_DAY_2021`;
- `fully_closed_hours_utc = frozenset(range(17, 22))`.

No other date is authorized merely by route PASS.

## 9. Boundary consequences

Even after the pilot date is incorporated:

- global coverage remains BLOCKED;
- execution-window freeze remains BLOCKED while any in-window unresolved date exists;
- massive `.bi5` acquisition remains BLOCKED;
- real backtest remains BLOCKED.

## 10. Exactly one next governed action after pilot integration

After the pilot record has been added and calendar/coverage tests have passed, formalize a **systematic historical Trading Breaks recovery protocol** before querying the remaining in-window candidates in bulk.

That protocol must preserve at least:

- frozen candidate ordering/scope;
- exact-date addressing;
- broker instrument identity mapping;
- raw payload + DOM or equivalent broker-native evidence capture;
- calibrated end-time semantics;
- positive-record date-level PASS independently per date;
- no inference from empty/no-record responses until negative-evidence completeness is separately qualified;
- deterministic artifact provenance and auditability;
- no change to execution-window boundaries based on outcomes.

Do not begin `.bi5` acquisition or real backtesting.
