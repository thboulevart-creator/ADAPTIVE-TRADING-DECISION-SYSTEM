# AO-E0-B12-DATA-01-ACQ-01 — execution / qualification

Date: 2026-10-06

## Verdict

`ACQ01 = BLOCKED`

Exact blocker:

`BLOCKED_SOURCE_CONTINUATION_NOT_EXACT`

## Authorization binding

Human authorization SHA-256:

`71dcffb521f5353ca09e3857dea08e9e41281cc756603d6ad582e84fc3e49d6a`

The authorization required exact source continuation on the frozen 2026-05-18 through 2026-05-24 overlap before any October forward acquisition.

## Test-first implementation

Local deterministic replay:

`30 / 30 PASS`

No CI pass is claimed by this report.

## Reference lineage

Reference: `CarlosSilva1/ustech-ticks`.

Three May-2026 Parquet objects were reacquired from the public historical lineage.

- part0000: `0b374bf24b40659b0c30406c80ff519e8de5d2495e4bfb0c83ea1293e93c88bc`
- part0001: `9ae9e557cb5120093eaa36a6cfb46168c2a426234fbb90a994b7e4a92b838b98`
- part0002: `ebfb07931bd5385bbd2a3f6e9d75919237db5eb3ef4d6cb79f474570febcd35a`

Reference rows inside the frozen overlap: `2,058,942`.

## Dukascopy candidate lineage

Provider: `DUKASCOPY`

Instrument: `USATECH.IDX-USD`

Transport: `https://jetta.dukascopy.com/v1/ticks`

The legacy `datafeed.dukascopy.com` route remained unavailable during reconnaissance, but the Jetta route was reachable without requester-pays.

The complete frozen overlap was acquired as 168 hourly raw JSON objects.

Total raw candidate bytes: `47,769,010`.

Candidate inventory digest:

`026ab6505bc1a7367f1d6dcb2828d3cf8f20421d2964b647bb97824a43422fd1`

Candidate rows inside the exact overlap: `2,058,942`.

## Exact comparison

```text
TIMESTAMP_MISMATCH_COUNT = 0
BID_MISMATCH_COUNT       = 264431
ASK_MISMATCH_COUNT       = 245864
```

The timestamp universe is exact across the frozen overlap, but the bid/ask values are not byte/value-equivalent after the preregistered normalization.

Therefore:

`SOURCE_B_CONTINUATION = BLOCKED_SOURCE_CONTINUATION_NOT_EXACT`

No tolerance, alternate divisor, repair, rescaling, filtering or post-observation semantic substitution is introduced.

## Forward firewall

```text
B8 = CLOSED
B12 = CLOSED
EXACT_FORWARD_INSTANCE = NOT_YET_AVAILABLE
DATA01_INSTANCE_STATE = WAIT_NOT_READY
FORWARD_OCTOBER_ACQUIRED = FALSE
PERFORMANCE_BEARING_READ = FALSE
PNL_OBSERVED = FALSE
STRATEGY_CALCULATED = FALSE
```

No October forward object was acquired because the prerequisite source-continuation gate did not pass.

## Consequence

ACQ-01 terminates as `BLOCKED`, exactly as permitted by the human authorization.

A new explicit human authorization is required before either:

1. a source-semantic reconciliation of the observed historical differences; or
2. qualification of another candidate lineage as an exact continuation.

No B12 opening, forward observation, strategy qualification, trading or capital authority is created.
