# HISTORICAL BROKER EVIDENCE ROUTE QUALIFICATION

## Status

**ACTIVE GATE — widget calibration PASS; one unresolved-date pilot still required before final route PASS.**

Contract:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

## 1. Purpose

This gate determines whether a materially new Dukascopy-native historical evidence route can be used to resolve special-session calendar gaps inside the already-selected execution-window candidate.

It does **not** reopen the 67 unresolved dates individually and it does **not** authorize changing the execution-window boundaries.

Current candidate window remains:

`2021-08-14` → `2026-08-14`

Current calendar state inside that window remains:

- candidates: 68;
- resolved: 1;
- unresolved: 67;
- FAIL: 0.

## 2. Required PASS properties for a route

A historical broker evidence route may receive final PASS only if all of the following are demonstrated reproducibly:

1. **Verified Dukascopy provenance**
   - official Dukascopy domain/service/API/widget/archive, or an archived official Dukascopy artifact with verifiable provenance;
   - third-party summaries are not sufficient.

2. **Historical-date addressability**
   - the mechanism can request or identify a specific historical date/interval;
   - a current page containing a stale `date` parameter is not by itself evidence that historical state can be recovered.

3. **Explicit target-instrument identity**
   - returned evidence explicitly identifies `USATECH.IDX/USD`, or another exact canonical identity already governed as equivalent;
   - generic `CFD`, `indexes`, `US markets`, or exchange-product context is insufficient.

4. **Exact special-session timing**
   - evidence provides exact special open/close/break/reopen timing sufficient to construct the governed hourly truth;
   - a generic statement that trading hours change is insufficient.

5. **Reproducible retrieval**
   - request path/parameters or retrieval procedure can be recorded and repeated;
   - returned historical date semantics must be observable rather than inferred.

6. **Calibration against a gold-standard historical witness**
   - before using the route on an unresolved in-window date, it must reproduce a date already independently qualified from exact Dukascopy evidence.

7. **Unresolved-date pilot**
   - after calibration, exactly one pre-existing BLOCKED date from the candidate window must be tested without changing the acceptance criteria;
   - only after that pilot succeeds may the route receive final PASS for systematic application.

8. **No contradiction with locked evidence**
   - if the route contradicts the gold-standard witness or returns current/regular hours for the historical special date, it cannot receive PASS without separately governed contradiction resolution.

## 3. Immediate FAIL conditions

A candidate route is FAIL for the intended historical-holiday purpose if authoritative evidence establishes that the mechanism does not cover weekday holiday/special-session intervals, or if a technically successful historical calibration contradicts the locked witness.

## 4. BLOCKED conditions

A route remains BLOCKED when it is plausible but one or more required PASS properties cannot yet be demonstrated.

HTTP access failure, missing assets, missing historical snapshots, or an unexecuted date parameter remain BLOCKED conditions, not semantic FAILs.

## 5. Forbidden false-PASS shortcuts

None of the following may qualify a historical broker route:

- holiday name alone;
- exchange-only timings;
- current regular trading hours;
- other-year Dukascopy holiday schedules;
- adjacent-date inference;
- missing BI5/ticks;
- HTTP 403/404/503;
- empty search results;
- inaccessible Wayback/CDX results;
- generic broker notices without `USATECH.IDX/USD` and exact timing;
- JForex weekend offline intervals used as holiday intervals without explicit broker support;
- a widget parameter whose historical behavior was never observed.

## 6. Qualification sequence

For every candidate mechanism:

`mechanism discovery → provenance check → semantic break → gold-standard calibration → unresolved-date pilot → route verdict`

The route must be qualified before any systematic application to the 67 gaps.

## 7. Trading Breaks widget calibration — PASS

Calibration report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Final authoritative run:

- GitHub Actions run: `34866241511`;
- probe head: `231867ae6a78a5db640b84351073ef3835bbb4a3`;
- artifact ID: `10356927580`;
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`.

Known witness:

`2020-02-17 — PRESIDENTS_DAY`

The official historical widget reproduced:

- `USATECH.IDX/USD`;
- break start `2020-02-17 18:00:00 UTC`;
- break end / last closed minute `2020-02-17 22:59:00 UTC`;
- derived reopen `2020-02-17 23:00:00 UTC`;
- reason `President's Day`.

The rendered DOM and structured broker-native JSONP payload independently agree.

Calibration verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Important representation rule learned by calibration:

- the widget's `BREAK END TIME` is the final closed minute;
- for minute-resolution records, governed reopen instant = `break_end + 60 seconds`;
- therefore `22:59:00` is consistent with an explicit broker reopen at `23:00:00`.

This is a representation finding calibrated against an independently known witness, not an assumption introduced to rescue a blocked date.

## 8. Earlier widget attempts retained for auditability

- headless direct request reached the historical URL but received HTTP `403` → BLOCKED, not FAIL;
- the current official builder page loaded in HTTP `200` while its relative application assets returned `404` → BLOCKED;
- first headed run loaded the historical widget and produced the correct raw `18:00 → 22:59` record, but an overly literal comparator expected the string `23:00` and emitted a false negative;
- the comparator was corrected to structured break semantics and re-run without changing the locked witness or acceptance threshold;
- corrected re-break = PASS.

## 9. Current route verdict

The widget route has passed its **gold-standard calibration**, but the route-level qualification is not complete until the mandated unresolved-date pilot succeeds.

Current route state:

**BLOCKED — `UNRESOLVED_DATE_PILOT_NOT_YET_EXECUTED`**

This BLOCKED state is procedural, not a failure of calibration.

## 10. Exactly one next governed action

Probe exactly one existing unresolved date inside the candidate window through the now-calibrated widget route.

Selection must not cherry-pick an easy date. Therefore choose mechanically the earliest unresolved candidate in the frozen candidate ordering:

`2021-09-06 — LABOR_DAY`

Required evidence chain:

`historical date request → broker runtime/API payload → exact USATECH identity → exact break interval or explicit absence → DOM cross-check → date-level gate → route verdict`

Do not test a second unresolved date unless this pilot first receives a governed verdict.

## 11. Boundary consequences

Calibration PASS does **not** freeze the execution window and does **not** authorize `.bi5` acquisition.

Until the one-date pilot succeeds and all in-window unresolved dates are eventually resolved:

- `FREEZE_EXECUTION_WINDOW = BLOCKED`;
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`;
- `REAL_BACKTEST = BLOCKED`.
