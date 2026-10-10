# E1-TD-03C-JF02-D2 — ROOT-CAUSE FORENSIC ASSESSMENT V0.1

## Verdict

`ROOT_CAUSE = SUPPORTED_BUT_NOT_PROVEN`

Most supported cause:

`C07 — CACHE_PATH / CACHE_STATE_DEPENDENCY`

Coupled initiating event:

`C11 — TRANSIENT_PROVIDER_HISTORY_SERVICE_FAILURE`

## Core causal sequence supported by evidence

1. The initial JForex history attempt authenticated and subscribed `USATECH.IDX/USD`.
2. During the history load, `CurvesJsonProtocolHandler` raised a read timeout / `SocketTimeoutException`.
3. At essentially the same time, JForex created the exact cache chunk:
   `AppData\Local\JForex\.cache\USATECHIDXUSD\2025\09\01\14h_ticks.bi5`
4. That chunk is exactly 0 bytes and SHA-256 equals the empty-file hash.
5. The later `READ_A-R1` used `IHistory.getTicks(...)` and returned zero ticks with no JFException.
6. The zero-byte chunk remained unchanged across the retry.
7. Static SDK inspection shows:
   `History.getTicks -> HistoryData.getTicksSecured -> loadTicksDataSynched -> LoadDataAction -> CurvesDataLoader.loadInCache -> LocalCacheManager.readData`.
8. Independent official Dukascopy Historical Data Export proves the interval actually contains 22,985 BID ticks.

The strongest supported interpretation is therefore that the first timeout left a stale/invalid zero-byte persistent cache chunk which was subsequently reused by the synchronous history path, producing a false empty result.

## Why this is not PROVEN

D2 intentionally forbids:
- cache deletion/purge;
- cache-directory change;
- configuration mutation;
- new JForex history requests.

Therefore D2 cannot execute the counterfactual needed to isolate cache state as the unique cause.

## Material rejections

- Incorrect instrument binding: rejected.
- DEMO historical-data absence: rejected by official Dukascopy documentation.
- API implementation mismatch: rejected; dependency/runtime both 2.13.99.
- Subscription race: rejected; blocking subscription was used and observed.
- from/to boundary misuse: rejected.
- Collector defect as primary cause: rejected by static call-path and invariant checks.

## Repair necessity

A repair/controlled experiment is necessary before the JForex path can be qualified.

No repair is selected or implemented in D2.

## Minimum next experiment proposal

`E1-TD-03C-JF02-D3 — CACHE-NEUTRAL CONTROLLED CAUSAL TEST V0.1`

Use a new isolated empty cache directory via `IClient.setCacheDirectory(...)`, preserve the existing cache untouched, and perform exactly one same-interval `getTicks` request under the same SDK/API/account-mode/instrument bindings.

This is a proposal only. D3 is not authorized.

## STOP

No market-data request, login, export, code mutation, cache mutation, trading, strategy, PnL, or performance execution occurred during D2.
