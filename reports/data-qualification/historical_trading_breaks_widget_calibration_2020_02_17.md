# HISTORICAL TRADING BREAKS WIDGET — CALIBRATION 2020-02-17

## Verdict

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

Contract:

`HISTORICAL_TRADING_BREAKS_WIDGET_CALIBRATION_V1`

This verdict qualifies only the gold-standard calibration step required by `HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`.

It does **not** yet grant a final PASS to the route for systematic application to the 67 unresolved in-window dates. One unresolved in-window date must be probed next under the unchanged acceptance rules.

## 1. Locked witness

Calibration date:

`2020-02-17 — PRESIDENTS_DAY`

Target instrument:

`USATECH.IDX/USD`

Independent locked Dukascopy witness already present before this experiment:

- special close: `18:00 GMT`;
- reopen: `23:00 GMT`;
- governed fully closed UTC hours: `18, 19, 20, 21, 22`;
- reason: `SPECIAL_PRESIDENTS_DAY_2020`.

The widget calibration was therefore falsifiable before execution.

## 2. Runtime mechanism

Official widget builder page:

`https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

Official widget runtime domain:

`https://freeserv.dukascopy.com/2.0/`

Historical widget request used:

`path=trading_breaks/index`

with:

- `currentDate=false`;
- `date=1581897600000` (`2020-02-17T00:00:00Z`);
- language `en`.

The browser execution was performed by GitHub Actions in Chromium through Xvfb with network capture enabled.

Final authoritative workflow run:

- run ID: `34866241511`;
- workflow: `Dukascopy Trading Breaks Widget Calibration`;
- branch: `feat/multi-year-dukascopy-acquisition`;
- head: `231867ae6a78a5db640b84351073ef3835bbb4a3`;
- artifact ID: `10356927580`;
- artifact SHA-256: `f49fb3aa5b66c22127eda3ac4593a387f6f83d3ab1d1d31eb742d44c49fb6a91`.

## 3. Network truth

The historical widget document returned HTTP `200` and actually honored the historical date.

The runtime called the broker-native endpoint:

`group=trading&method=breaks`

for the February 2020 interval:

- `start=1580515200000`;
- `end=1583020799999`.

The runtime also called the broker-native instrument catalogue:

`group=widgets&method=instruments`.

That catalogue maps:

- instrument ID `9016`;
- name `USATECH.IDX/USD`;
- description `US 100 Tech Index`;
- historical filename `USATECHIDXUSD`.

## 4. Structured witness

The historical breaks payload returned the following record for instrument ID `9016`:

```json
{
  "id": "15516",
  "instrument": "9016",
  "start": "1581962400000",
  "end": "1581980340000",
  "reason": "President's Day"
}
```

UTC interpretation:

- break start = `2020-02-17T18:00:00Z`;
- break end value = `2020-02-17T22:59:00Z`;
- the widget represents this as the last closed minute;
- therefore next minute / reopen = `2020-02-17T23:00:00Z`.

This exactly reproduces the independently locked broker witness and the governed fully closed hours `18–22 UTC`.

## 5. DOM cross-check

The rendered widget DOM independently displayed:

`USATECH.IDX/USD    17-Feb-20 18:00:00    17-Feb-20 22:59:00    President's Day`

Therefore both the structured network payload and the rendered DOM agree on:

- historical date;
- exact instrument;
- exact special break start;
- exact last closed minute;
- event reason.

## 6. Adversarial execution history

The route was not promoted on the first plausible signal.

### Attempt 1

Direct headless embed propagated the historical date but the widget document returned HTTP `403`.

Correct governed interpretation:

**BLOCKED**, not FAIL and not proof of historical absence.

### Attempt 2

The official widget-builder page returned HTTP `200`, but its current relative `app.js` / stylesheet assets returned HTTP `404`, so no preview iframe was instantiated.

Correct governed interpretation:

**BLOCKED**.

### Attempt 3

Headed Chromium with a normal browser UA and official referer returned HTTP `200` for both the current control and the historical widget. The widget rendered `USATECH.IDX/USD 18:00 → 22:59`.

The first automated comparator incorrectly expected a literal `23:00` string and emitted FAIL.

This was a comparator defect: it confused **last closed minute** with **reopen instant**.

The raw evidence was preserved and inspected before changing the comparator.

### Attempt 4 — corrected re-break

The comparator was corrected to use the structured payload semantics:

`break_end_last_closed_minute + 60 seconds = reopen`.

The rerun independently reproduced:

- DOM match = true;
- structured payload match = true;
- derived reopen = `23:00:00Z`;
- runtime errors = none;
- verdict = PASS.

This correction did not change the witness or acceptance threshold; it fixed only the representation error in the probe.

## 7. Calibration conclusion

The official Dukascopy Trading Breaks widget demonstrates all calibration properties required at this stage:

- official broker provenance: YES;
- historical-date addressability: YES;
- historical request actually observed: YES;
- exact `USATECH.IDX/USD` identity: YES;
- exact special-session timing: YES;
- reproducible network path: YES;
- agreement with independent locked witness: YES;
- contradiction with locked witness: NO.

Calibration verdict:

**PASS — `HISTORICAL_WIDGET_REPRODUCES_LOCKED_2020_02_17_USATECH_WITNESS`**

## 8. Boundary

This PASS does **not**:

- resolve any of the 67 current in-window gaps;
- freeze the execution window;
- authorize `.bi5` acquisition;
- authorize a real backtest;
- authorize systematic batch application yet.

Exactly one unresolved in-window date must now be tested through the same route before a final route-level PASS can be considered.

To avoid evidence cherry-picking, that pilot date is selected mechanically as the earliest unresolved candidate in the already-frozen candidate ordering:

`2021-09-06 — LABOR_DAY`.
