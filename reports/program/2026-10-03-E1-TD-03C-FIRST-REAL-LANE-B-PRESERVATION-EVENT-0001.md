# E1-TD-03C — FIRST REAL LANE-B PRESERVATION EVENT — EVENT 0001

**Date:** 2026-10-03  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Execution authority binding

The real event was executed under the exact human-authorized canonical state:

```text
AUTHORIZED_PARENT_HEAD =
caad9412a3cfb3301d8255e1dee4e615bd379101

AUTHORIZED_PARENT_TREE =
ee70fe09f77aaa5ab2cc298a372a2c760be5ab47

RUNTIME_BLOB =
150a54ea3571dbf13619215f7015c2da46de699b

FROZEN_BREAKER_BLOB =
610f2eb3fbc55565de47a5f360c810f051d29918

EVENT_BUDGET =
1 REAL PRESERVATION EVENT MAXIMUM
```

Before evidence persistence, the canonical branch advanced independently to:

```text
PERSISTENCE_PARENT_HEAD =
c842289b9896c0d19030e91e842b9479e61a7a68

PERSISTENCE_PARENT_TREE =
b0b4b4d1d65beb5e99d067af3f5ddaf8093e466b
```

The intervening diff contains only RTMA-01 contract/breaker/RED artifacts and does not modify E1-TD-03C, its runtime, its breaker, its authority bindings, TD01 or Lane-B evidence semantics.

No event authority was rebased or rewritten.

## 2. Authorized boundary

```text
AUTHORITY = BOUNDED RAW PRESERVATION ONLY

AUTHORIZED =
PROVENANCE
EXACT RAW BYTES
SHA-256
SIZE
REQUEST IDENTITY
INTEGRITY CHECK
INDEPENDENT LANE-B LEDGER
EVIDENCE PERSISTENCE

FORBIDDEN =
SOURCE-B EQUIVALENCE
SOURCE-B SUBSTITUTION
TD01 MERGE
HISTORICAL OVERLAP ANALYSIS
H1
SIGNALS
STRATEGIES
PNL
PERFORMANCE
BACKTEST
SECOND COLLECTION EVENT
CONTINUOUS COLLECTION
```

## 3. Predeclared request target

Before reading any market bytes, the target was fixed as:

```text
RUN_ID =
E1TD03C-LANEB-REAL-0001-20261001T140000Z

LANE =
LANE_B_DUKASCOPY_PROSPECTIVE_INSURANCE

DATASET_ID =
DUKASCOPY_USATECH_PROSPECTIVE_INSURANCE_20261001_20271001_V0_1

PROVIDER =
Dukascopy Bank SA

INSTRUMENT_ID =
USATECH.IDX/USD

PROVIDER_SYMBOL_PATH =
USATECHIDXUSD

REQUESTED_INTERVAL =
[2026-10-01T14:00:00Z,
 2026-10-01T15:00:00Z)

REQUEST_URL =
https://datafeed.dukascopy.com/datafeed/USATECHIDXUSD/2026/09/01/14h_ticks.bi5

NETWORK_RETRIES =
0
```

Selection was clock-based and fixed before byte observation. No market or strategy result was used.

The exact availability of the requested legacy datafeed object was not established before the request.

## 4. Non-self-referential authority instance

The one-shot authority instance was created outside the repository before the network request.

```text
AUTHORITY_SHA256 =
390ffe1ec8c5f8a7d3aec9c4264a2a5ee019d4fecc22534e0ab92205dbfad6f8
```

## 5. Real request result

```text
REQUEST_STARTED_AT_UTC =
2026-10-03T09:35:49.3679957Z

REQUEST_ENDED_AT_UTC =
2026-10-03T09:36:04.4261261Z

CURL_EXIT_CODE =
28

HTTP_CODE =
000

SIZE_DOWNLOAD =
0

OUTCOME =
ACQUISITION_FAILURE_NETWORK_TIMEOUT
```

No HTTP response was established before the configured connection timeout.

This result establishes only a network-level failure for this one request. It does not establish object non-existence, provider unavailability, source-continuity failure or instrument unavailability.

## 6. Raw preservation result

```text
RAW_OBJECT_RECEIVED = FALSE
RAW_FILE_PRESENT = FALSE
RAW_OBJECT_SIZE = NONE
RAW_OBJECT_SHA256 = NONE
```

No market-data hash or identity is invented.

The response-header evidence file remained empty:

```text
RESPONSE_HEADERS_BYTES =
0

RESPONSE_HEADERS_SHA256 =
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

## 7. Independent append-only Lane-B ledger

The ledger records two internal states of the single governed event:

```text
1 = ACQUISITION_REQUEST
2 = ACQUISITION_FAILURE
```

```text
LEDGER_VALIDATION =
PASS_LEDGER

LEDGER_SHA256 =
4fadcff146c35f5fe791b0bcb775f1cfcdb1bc64224949e247658828a90b50bb

LEDGER_FINAL_DIGEST =
c25d204699293c9946aaefda056652fd2b0b85bbe408ec19173108c4e399adf0
```

These are ledger records inside one preservation event, not two collection events.

## 8. Fail-closed event-budget adjudication

```text
EVENTS_AUTHORIZED =
1

EVENTS_CONSUMED =
1

FIRST_REAL_LANE_B_EVENT =
CONSUMED

EVENT_OUTCOME =
ACQUISITION_FAILURE_NETWORK_TIMEOUT

RETRY =
NOT_PERFORMED

SECOND_COLLECTION_EVENT =
NOT_AUTHORIZED

CONTINUOUS_COLLECTION =
NOT_AUTHORIZED
```

No alternate URL, second hour, retry or substitute provider was attempted.

## 9. Protected scientific boundaries

```text
SOURCE_B_EQUIVALENCE = NOT_EVALUATED
SOURCE_B_SUBSTITUTION = NOT_AUTHORIZED
TD01_MERGE = NOT_AUTHORIZED
HISTORICAL_OVERLAP_ANALYSIS = NOT_RUN

H1 = NOT_BUILT
SIGNALS = NOT_RUN
STRATEGIES = NOT_RUN
PNL = NOT_OBSERVED
PERFORMANCE = NOT_COMPUTED
BACKTEST = NOT_RUN
```

## 10. Evidence identities

```text
LOCAL_MACHINE_EVIDENCE_SHA256 =
54eb8c60a08a181d98ae69099b9f0c36ad25f036e924f2e244e82cf1b1dc2689

AUTHORITY_GIT_BLOB =
eca71fc11b162e5baeadca48b07c8411ecd02593

LEDGER_GIT_BLOB =
c4cbfa4a4ee8b541be053854f788aae1f0c7fc7c

MACHINE_EVIDENCE_GIT_BLOB =
99a4e0850e2acf6d3e29bc9efbb30b268d50073f
```

## 11. Terminal state

```text
E1_TD_03C_FIRST_REAL_LANE_B_PRESERVATION_EVENT =
CONSUMED

OUTCOME =
ACQUISITION_FAILURE_NETWORK_TIMEOUT

RAW_OBJECT_PRESERVED =
FALSE

EVENT_BUDGET =
1 / 1 CONSUMED

STOP =
TRUE

NEXT =
HUMAN_ADJUDICATION
```

No further real-data request is authorized by this result.
