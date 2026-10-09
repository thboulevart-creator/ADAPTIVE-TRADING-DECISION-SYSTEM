# E1-TD-03C-JF02 — END-OF-DAY CHECKPOINT — 2026-10-09

## Canonical repository state before checkpoint

- Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
- Branch: `integration/system-v1`
- HEAD before checkpoint: `543214b05f72ed9fb72fc165a9ed89b73e67fef5`
- TREE before checkpoint: `387aa1dc3bb851ecc2fbd50974b7730306be358b`
- `force=false`

## Scope

This checkpoint is for the SECURE_THE_FUTURE Lane-B JForex / Dukascopy acquisition-evidence qualification only.

Do not conflate with FC01:
- FC01 = operational historical Dukascopy transport/source qualification.
- E1-TD-03C-JF02 = AWS-independent Dukascopy provider-history evidence substitute qualification.

## Frozen AWS state

AWS is preserved but frozen:
- Bucket: `cfg-public-proper-wallaby`
- Region: `eu-west-1`
- Requester Pays: true
- Candidate key: `USATECHIDXUSD/2026/09/01_ticks.bi5`
- Candidate key status: `UNVERIFIED`
- No new ListObjectsV2 / HeadObject / GetObject authorized.
- No new AWS cost.
- No new market bytes.

## JF01 documentary conclusion

Documentary direction accepted in principle:
- Primary AWS-independent candidate: official JForex historical API.
- JForex evidence model is provider-history-response evidence, NOT provider raw-object evidence.
- Historical Data Export is a second official delivery-path validator, not an independent provider.
- datafeed BI5 remains legacy/raw-byte fallback candidate only.
- AWS cannot yet be demoted from critical dependency.

## JF02 preregistration / pre-real state

JF02 was preregistered and persisted.

Core fixed request:
- Provider: Dukascopy Bank SA
- Environment: DEMO
- Instrument: `USATECH.IDX/USD`
- ATDS instrument: `USATECH.IDX-USD`
- Frozen interval:
  - start = `2025-10-01T14:00:00.000Z`
  - end exclusive = `2025-10-01T15:00:00.000Z`
  - JForex from_ms = `1759327200000`
  - JForex to_ms inclusive = `1759330799999`
- Interval is historical and outside the prospective window.
- No strategy, PnL, performance, trading, capital, Source-B equivalence or raw-object equivalence claims allowed.

Relevant commits:
- JF02 pre-real freeze: `da319db3d7a9de09da4e28d7d5613d92af6bc512`
- JF02 runtime readiness: `b0f0ef6...`
- JF02 synchronous repair qualification: `07e2fb4f4196e438b3f5607a795511b2a2bfc1df`
- READ_A-R1 authorization: `4244b1d10d93b3fc068c7d7600836809577c2377`
- D1 authorization: `3c213577a8a2d5a870234abbd6440b12b56a8081`
- D1 export diagnostic contract: `543214b05f72ed9fb72fc165a9ed89b73e67fef5`

## JForex runtime

Portable isolated runtime prepared:
- Eclipse Temurin JDK 8u504-b01
- Maven 3.10.0
- Dukascopy SDK `DDS2-jClient-JForex:3.6.51`
- JForex API implementation version observed during real session: `2.13.99`

No trading/order logic is present in the collector.

## JForex DEMO capability

Human confirmed successful graphical JForex DEMO login.

Credentials must never be sent in chat or committed to GitHub.

## READ_A initial real attempt

Result:
- Authentication: PASS
- DEMO connection: PASS
- Instrument subscription `USATECH.IDX/USD`: PASS
- Historical request attempted: 1
- Automatic retries: 0
- Valid ticks received: 0
- Canonical payload produced: NO

Observed provider-side failure:
- `CurvesJsonProtocolHandler - Read timed out`
- `java.net.SocketTimeoutException: Read timed out`

Original terminal breaker:
- `BLOCKED_JF02_EMPTY_RESPONSE`

Corrected interpretation:
- history network timeout proven
- empty market interval NOT proven
- READ_A consumed and failed closed
- no automatic retry

The first full local provider debug log was purged after it was discovered that it contained the DEMO account identifier in a technical URL. Password was not observed in that log.

## CR1 repair

Authorized and executed:
- Replace asynchronous `IHistory.readTicks(...)` with synchronous `IHistory.getTicks(...)`.
- Preserve exact instrument.
- Preserve exact interval.
- Preserve canonical serialization.
- Preserve source order.
- No sort.
- No deduplication.
- No repair.

New explicit breaker semantics include:
- `BLOCKED_JF02_HISTORY_NETWORK_TIMEOUT`
- `BLOCKED_JF02_HISTORY_LOAD_FAILURE`
- `BLOCKED_JF02_HISTORY_LOAD_NULL`
- `BLOCKED_JF02_HISTORY_RUNTIME_FAILURE`
- `BLOCKED_JF02_OUTPUT_WRITE`
- `BLOCKED_JF02_EMPTY_RESPONSE` remains distinct.

Qualification:
- Python tests: 18/18 PASS
- Java compile: PASS
- Real JForex reads during CR1: 0

## READ_A-R1 single controlled retry

Human authorized exactly one real retry.

Observed output:
- `JF02_SDK_DEPENDENCY=3.6.51`
- `JF02_API_IMPLEMENTATION_VERSION=2.13.99`
- `JF02_RUN_LABEL=READ_A`
- `JF02_INSTRUMENT=USATECH.IDX/USD`
- `JF02_FROM_MS=1759327200000`
- `JF02_TO_MS_INCLUSIVE=1759330799999`
- terminal result: `JF02_FAILED=BLOCKED_JF02_EMPTY_RESPONSE`
- exit code: 1
- automatic retry: 0

Interpretation:
- synchronous `getTicks(...)` completed without the previously observed timeout/JFException
- returned zero ticks
- no valid canonical payload
- no SHA256 market payload
- `READ_A-R1` budget consumed
- additional JForex retry is NOT authorized
- `READ_B` remains CLOSED

Current diagnostic status:
- `READ_A initial = FAILED_NETWORK_TIMEOUT`
- `READ_A_R1 = COMPLETED_WITH_ZERO_TICKS`
- `ZERO_TICKS = REAL_OBSERVATION`
- `TRUE_EMPTY_MARKET_INTERVAL = NOT_YET_PROVEN`
- `JFOREX_PATH_QUALIFIED = NO`
- `READ_B = CLOSED`

## JF02-D1 — next active frontier

Authorized purpose:
Use the official Dukascopy Historical Data Export as a second official delivery path on the exact same frozen interval to determine whether provider historical ticks exist.

Frozen D1 request:
- Provider: Dukascopy Bank SA
- Path: official web Historical Data Export
- Instrument: `USATECH.IDX/USD`
- Granularity intended: TICK
- Timezone: UTC
- Exact target interval:
  - `2025-10-01T14:00:00.000Z`
  - to `2025-10-01T15:00:00.000Z`
- Export budget: 1
- No JForex SDK read
- No AWS
- No datafeed
- No strategy
- No PnL
- No performance
- No trading
- No capital

Decision rule:
- Export has ticks => JForex delivery-path discrepancy candidate.
- Export also has zero ticks => exact-interval data availability issue candidate.
- Malformed/ambiguous export => inconclusive fail-closed.
- No automatic repair.

## UI observation at STOP point

A screenshot of the official Dukascopy Historical Data Export UI was provided by the human.

Visible controls:
- Instrument selected: `USATECH.IDX/USD`
- Period shown as:
  - numeric selector: `1`
  - unit selector currently: `Minute`
- Date selector only: `Oct 9, 2026` shown in the screenshot
- Timezone: `UTC`
- Offer side toggle: `Bid` or `Ask`
- Download button

Important observation:
- No exact start/end time selector is visible in this dialog.
- No direct tick option is visible in the screenshot at the current dropdown state.
- Only one offer side appears selectable at a time.
- Therefore the preregistered D1 exact interval / tick / both-side request is NOT YET shown to be executable by this UI.

## STOP

No D1 export has been downloaded yet.

Current budgets:
- READ_A initial: consumed
- READ_A-R1: consumed
- READ_B: 0 / forbidden
- D1 Historical Data Export: 0 / 1
- AWS requests: 0
- datafeed requests: 0
- prospective market reads: 0
- strategy reads: 0
- PnL reads: 0
- trading/orders: 0

## Exact next action for next session

Do NOT download anything yet.

Resume by adjudicating the D1 web UI capability:
1. Inspect whether the `Minute` unit dropdown contains `Tick`.
2. Determine whether the export UI can bind an exact hour or only a whole date.
3. Determine whether Bid and Ask require separate exports.
4. If exact interval + tick + both sides cannot be requested in a single export, amend D1 preregistration BEFORE any download.
5. Preserve the one-export budget until that amendment is explicit.
6. Do not reopen JForex READ_A or READ_B while D1 capability is unresolved.

END CHECKPOINT.
