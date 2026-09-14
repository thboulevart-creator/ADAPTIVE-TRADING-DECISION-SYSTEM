# HISTORICAL BROKER EVIDENCE ROUTE EXPLORATION V1

## 1. Scope

Execution-window candidate:

`2021-08-14` → `2026-08-14`

Current in-window state:

- candidates: 68;
- resolved: 1;
- unresolved: 67;
- FAIL: 0.

Objective of this exploration:

> Determine whether a materially new broker-native historical evidence mechanism exists that could resolve the 67 gaps without repeating date-by-date generic web research and without moving the execution window.

Gate:

`HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFICATION_V1`

## 2. Overall verdict

**BLOCKED — `NO_NEW_HISTORICAL_BROKER_EVIDENCE_ROUTE_QUALIFIED`**

Meaning:

- no newly investigated mechanism currently satisfies all route-PASS properties;
- this is not a claim that no historical broker evidence can ever be recovered;
- execution-window boundaries remain unchanged;
- the window remains unfrozen;
- massive `.bi5` acquisition remains forbidden;
- real backtest remains unauthorized.

## 3. Candidate-route matrix

| Candidate route | Provenance | Historical addressing | Explicit USATECH + exact holiday timing | Reproducible now | Verdict |
|---|---|---|---|---|---|
| Official Trading Breaks widget with `date` parameter | Dukascopy official | parameter exists, semantics not yet proven | not yet captured historically | no | BLOCKED |
| JForex `IDataService.getOfflineTimeDomains(...)` | Dukascopy official API | yes | authoritative support says weekday holidays are not included | yes | FAIL |
| Dukascopy `marketwatch/market-news/News` archive | Dukascopy official | yes, archive/search/date pages exist | tested in-window notices remain generic and delegate detail to Trading Breaks Calendar | partially | BLOCKED |
| Archived Trading Breaks/widget snapshot (e.g. Wayback) | potentially official archived content | potentially | no verified usable snapshot recovered | no | BLOCKED |
| Direct Dukascopy support / archived support answer for target dates | Dukascopy if obtained | potentially | no qualifying target-date response collected | no | BLOCKED |

## 4. Route A — Trading Breaks widget

Official Dukascopy widget page:

`https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks`

The official embed configuration exposes parameters including:

- `type: trading_breaks`;
- `currentDate`;
- `date` represented as milliseconds;
- Dukascopy widget loader under `freeserv-static.dukascopy.com`.

This is materially different from the previously exhausted holiday-news searches because it indicates a programmatic date-addressable mechanism behind the Trading Breaks UI.

However, the existence of a `date` field does not establish that:

- historical state is retained;
- `currentDate=false` causes a historical lookup;
- the backend returns the requested historical date rather than present state;
- historical output includes `USATECH.IDX/USD`;
- exact close/reopen/break timing is returned;
- the retrieval can be reproduced and archived.

Current route verdict:

**BLOCKED — `HISTORICAL_WIDGET_SEMANTICS_AND_PAYLOAD_NOT_VERIFIED`**

Required next test:

calibrate against locked PASS date `2020-02-17 — PRESIDENTS_DAY` in a JavaScript/network-capable browser environment and capture endpoint + params + payload/DOM.

## 5. Route B — JForex offline-time domains

Official JForex API exposes instrument-aware historical offline intervals via `IDataService`, including methods such as:

- `getOfflineTimeDomain(Instrument instrument)`;
- shifted offline domains;
- `getOfflineTimeDomains(long from, long to, Instrument instrument)`.

At first sight this was a strong broker-native route candidate.

Adversarial break:

Dukascopy API Support was asked whether a weekday holiday interval is included by `getOfflineTimeDomains()`.

Official answer: **No.**

The follow-up states that such functionality was not available at that time. Current Javadoc language also characterizes the returned offline domains as weekend intervals.

Therefore using this mechanism to infer holiday special sessions would be a false promotion of a weekend-domain API into holiday evidence.

Route verdict:

**FAIL — `OFFLINE_TIME_DOMAIN_DOES_NOT_COVER_WEEKDAY_HOLIDAY_SESSIONS`**

This route must not be used for the 67 holiday/special-session gaps unless new authoritative Dukascopy documentation explicitly changes the semantics and that change is separately qualified.

## 6. Route C — Dukascopy Market News archive

Official archive:

`https://www.dukascopy.com/swiss/english/marketwatch/market-News/News/`

This archive is materially separate from the `about/ournews` pages used extensively during the annual qualification campaigns. It provides historical news items and date/search filters.

Recovered example:

`New Year’s trading breaks`, 30 December 2021, Dukascopy Bank SA.

The bulletin identifies an exact broad period during which various instruments/markets are scheduled for trading breaks, but directs users to the Trading Breaks Calendar for detailed information.

This proves that the archive can preserve historical broker context, but the tested in-window material does not yet provide the required combination:

`historical date + USATECH.IDX/USD + exact special-session timing`.

Absence from tested search results is not proof that no qualifying bulletin exists.

Route verdict:

**BLOCKED — `OFFICIAL_ARCHIVE_EXISTS_BUT_TARGET_INSTRUMENT_TIMING_NOT_RECOVERED`**

## 7. Historical exact-evidence pattern

Older Dukascopy publications demonstrate that exact instrument-specific historical holiday evidence has existed publicly. Known examples include exact `USATECH.IDX/USD` holiday timing pages in 2016–2020, including the locked `2020-02-17` Presidents Day witness.

Later notices increasingly delegate details to the Trading Breaks Calendar rather than publishing all instrument rows in article text.

This pattern is contextual only. It must not be converted into either of these unsupported claims:

- “there is definitely no historical detail after 2020”;
- “the current Trading Breaks Calendar necessarily preserves every historical row”.

## 8. Route D — archived widget/calendar snapshots

Searches did not recover a verifiable archived Trading Breaks payload/snapshot suitable for qualification.

That search/access result is not proof that no snapshot exists.

Route verdict:

**BLOCKED — `NO_VERIFIED_ARCHIVED_TRADING_BREAKS_SNAPSHOT_RECOVERED`**

## 9. Route E — direct support / archived broker response

Current Dukascopy Trading Breaks pages expose support channels for schedule questions. A contemporaneous or archived official broker response that explicitly binds a target historical date to `USATECH.IDX/USD` and exact hours could in principle satisfy broker-evidence requirements depending on provenance and specificity.

No such new response was obtained in this exploration.

Route verdict:

**BLOCKED — `NO_TARGET_DATE_INSTRUMENT_SPECIFIC_SUPPORT_WITNESS_OBTAINED`**

## 10. Adversarial conclusions

The following false shortcuts are explicitly rejected:

- treating the widget `date` parameter as proof of historical retention;
- treating inability to access a backend endpoint as proof that it does not exist;
- treating JForex weekend offline periods as holiday periods;
- treating a generic historical Market News bulletin as instrument-specific timing;
- treating other-year exact Dukascopy pages as target-year broker truth;
- treating exchange evidence as a substitute for missing broker evidence;
- treating missing tick data as session evidence.

## 11. Boundary state after exploration

No date-level calendar evidence changed.

Therefore the execution candidate remains:

`2021-08-14` → `2026-08-14`

with:

- 68 candidates;
- 1 resolved;
- 67 unresolved;
- 0 FAIL.

Boundary actions remain:

- `FREEZE_EXECUTION_WINDOW = BLOCKED`;
- `AUTHORIZE_MASSIVE_ACQUISITION = BLOCKED`;
- `REAL_BACKTEST = BLOCKED`.

## 12. Exactly one next governed action

**Technically qualify the official Dukascopy Trading Breaks widget historical-date route against the locked `2020-02-17` gold-standard witness in an environment capable of JavaScript execution and network/DOM capture.**

Required evidence to persist:

1. exact widget configuration;
2. actual endpoint/request path;
3. actual historical-date parameter semantics;
4. response payload or rendered historical row;
5. explicit `USATECH.IDX/USD` identity;
6. exact special-session timing;
7. comparison with the locked 2020 witness;
8. PASS/FAIL/BLOCKED route verdict.

Do not probe all 67 dates before the calibration witness passes.
