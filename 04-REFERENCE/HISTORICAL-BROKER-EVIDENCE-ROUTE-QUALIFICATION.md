# HISTORICAL BROKER EVIDENCE ROUTE QUALIFICATION

## Status

**ACTIVE GATE — no route qualified yet.**

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

A historical broker evidence route may receive PASS only if all of the following are demonstrated reproducibly:

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
   - before using the route on an unresolved in-window date, it must reproduce a date already independently qualified from exact Dukascopy evidence;
   - preferred calibration witness: `2020-02-17 — PRESIDENTS_DAY`, which already has explicit Dukascopy `USATECH.IDX/USD` timing evidence.

7. **No contradiction with locked evidence**
   - if the route contradicts the gold-standard witness or returns current/regular hours for the historical special date, it cannot receive PASS without a separately governed contradiction resolution.

## 3. Immediate FAIL conditions

A candidate route is FAIL for the intended historical-holiday purpose if authoritative documentation explicitly establishes that the mechanism does not cover weekday holiday/special-session intervals.

Example:

- a broker API documented or officially confirmed as weekend-only cannot be repurposed into holiday evidence.

## 4. BLOCKED conditions

A route remains BLOCKED when it is plausible but one or more required PASS properties cannot yet be demonstrated.

Examples:

- an official widget exposes a `date` parameter but historical retrieval semantics have not been observed;
- an official archive contains historical holiday notices but the tested notices only point to another calendar and do not expose instrument-specific hours;
- a historical snapshot may exist but no verifiable snapshot has been retrieved;
- access/search failure prevents observing the response.

BLOCKED is an absence of sufficient proof, not a claim that the route does not exist.

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

`mechanism discovery → provenance check → semantic break → gold-standard calibration → unresolved-date probe → route verdict`

The route is qualified before any systematic application to the 67 gaps.

## 7. Widget-route calibration protocol

For the official Dukascopy Trading Breaks widget candidate:

1. execute the official widget in an environment capable of JavaScript/network capture;
2. set historical mode deliberately (`currentDate=false` if supported by the actual implementation) and address the known witness date `2020-02-17`;
3. capture the actual request endpoint, request parameters, returned payload/DOM and date semantics;
4. verify that `USATECH.IDX/USD` and the already-known special close/reopen timing are reproduced;
5. if calibration does not reproduce the locked witness, route verdict = **FAIL** for historical qualification;
6. if calibration succeeds, probe exactly one unresolved in-window holiday date without changing the acceptance criteria;
7. only after both steps succeed may the route receive PASS and be considered for systematic application.

## 8. Boundary consequences

A route PASS does **not** itself freeze the execution window and does **not** authorize `.bi5` acquisition.

After a route PASS, each recovered date still requires date-level admissible evidence and the existing calendar gate.

Until all in-window unresolved dates are resolved:

- `FREEZE_EXECUTION_WINDOW = BLOCKED`;
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`;
- `REAL_BACKTEST = BLOCKED`.
