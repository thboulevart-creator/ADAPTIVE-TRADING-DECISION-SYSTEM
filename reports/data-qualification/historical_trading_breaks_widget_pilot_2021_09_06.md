# HISTORICAL TRADING BREAKS WIDGET — UNRESOLVED-DATE PILOT 2021-09-06

## Verdict

**PASS — `EXACT_PRIMARY_BROKER_USATECH_HISTORICAL_BREAK_WITNESS_RECOVERED`**

Contract:

`HISTORICAL_TRADING_BREAKS_WIDGET_UNRESOLVED_DATE_PILOT_V1`

This is the single unresolved-date pilot mandated after the independent gold-standard calibration of the Dukascopy Trading Breaks historical route.

## 1. Pilot selection

Pilot date:

`2021-09-06 — LABOR_DAY`

Selection rule:

`EARLIEST_UNRESOLVED_IN_FROZEN_EXECUTION_WINDOW_CANDIDATE`

The date was not selected because it looked easy to resolve. It is mechanically the first unresolved date in the already-versioned candidate ordering for:

`2021-08-14 → 2026-08-14`.

Before this pilot, the annual 2021 qualification had correctly classified this date:

**BLOCKED — `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP`**

because no exact broker-native `USATECH.IDX/USD` historical timing witness had yet been recovered.

## 2. Qualified route used

Gold-standard calibration report:

`reports/data-qualification/historical_trading_breaks_widget_calibration_2020_02_17.md`

Calibration verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Calibrated representation rule:

- `BREAK START TIME` = first closed minute;
- `BREAK END TIME` = final closed minute;
- reopen instant at minute resolution = `break_end + 60 seconds`.

No acceptance criterion was changed for this pilot.

## 3. Runtime execution

Official widget builder page:

`https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

Official runtime:

`https://freeserv.dukascopy.com/2.0/`

Historical addressing:

- `path=trading_breaks/index`;
- `currentDate=false`;
- `date=1630886400000` (`2021-09-06T00:00:00Z`).

GitHub Actions execution:

- run ID: `34866699952`;
- job ID: `104052206522`;
- run head: `2c875805ef554e0f65c4021ed5ecedadcce48a6f`;
- artifact ID: `10357256669`;
- artifact SHA-256: `8d8b568e17fd0e8d5d8c448742290313f78614ccd95c915aef5b978ed7f90ddc`.

Runtime controls:

- official Dukascopy page: HTTP `200`;
- current-date widget control: HTTP `200`;
- historical target widget: HTTP `200`;
- historical date actually honored: YES;
- runtime errors: NONE.

## 4. Exact broker-native identity

The Dukascopy instrument catalogue maps:

- instrument ID: `9016`;
- instrument: `USATECH.IDX/USD`.

This is explicit target-instrument identity, not generic CFD or exchange inference.

## 5. Exact broker-native historical break record

The historical Dukascopy breaks payload returned:

```json
{
  "id": "28743",
  "instrument": "9016",
  "start": "1630947600000",
  "end": "1630965540000",
  "reason": "Labor Day"
}
```

UTC interpretation:

- break start = `2021-09-06T17:00:00Z`;
- break end / final closed minute = `2021-09-06T21:59:00Z`;
- derived reopen = `2021-09-06T22:00:00Z`.

Therefore the complete UTC hourly buckets proven closed are exactly:

`17, 18, 19, 20, 21`.

Hour `16` remains tradable before the break. Hour `22` is tradable again from its first minute.

## 6. DOM cross-check

The rendered widget independently displayed:

`USATECH.IDX/USD    06-Sep-21 17:00:00    06-Sep-21 21:59:00    Labor Day`

DOM and structured broker payload therefore agree on:

- date;
- exact instrument;
- start;
- end;
- holiday reason.

## 7. Date-level gate application

Under `IRREDUCIBLE_HISTORICAL_BROKER_EVIDENCE_GAP_V1`, this satisfies PASS-A:

- exact primary broker witness: YES;
- exact target date: YES;
- exact target instrument: YES;
- exact special-session timing: YES;
- reproducible retrieval: YES;
- no exchange-only substitution: YES;
- no cross-year inference: YES;
- no adjacent-date inference: YES.

Date-level verdict:

**PASS — PASS-A / exact primary broker historical witness.**

The old BLOCKED verdict remains historically correct for the earlier annual campaign; this new runtime evidence supersedes it for the current state.

## 8. Route implication

The historical Trading Breaks route has now passed both required stages:

1. gold-standard calibration on independently known `2020-02-17` — PASS;
2. one mechanically selected unresolved in-window date `2021-09-06` — PASS.

Therefore the route itself is eligible for final PASS for the historical-holiday recovery purpose.

This does **not** mean that absence of a break record proves regular hours. Positive break records are admissible; negative/empty responses require separate completeness/absence semantics before they can become `NO_SPECIAL_CHANGE_EVIDENCE`.

## 9. Executable consequence for this date only

This pilot authorizes adding exactly one date-level special-session record:

- date: `2021-09-06`;
- reason: `SPECIAL_LABOR_DAY_2021`;
- `fully_closed_hours_utc = frozenset(range(17, 22))`.

It does not authorize adding any other date without its own recovered evidence.

## 10. Downstream boundaries

Even after this date is added:

- global coverage remains BLOCKED;
- candidate execution window remains NOT frozen;
- massive `.bi5` acquisition remains forbidden;
- real backtest remains unauthorized.

The next systematic step must be governed separately before applying the route across the remaining in-window gaps.
