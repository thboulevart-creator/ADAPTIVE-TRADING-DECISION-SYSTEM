# E1-TD-03B — POST-WINDOW SOURCE-B AVAILABILITY PREFLIGHT V0.1

**Date:** 2026-10-11  
**Mode:** PUBLIC METADATA ONLY  
**Market-data download:** NONE  
**Collection event consumed:** NO

## 1. Canonical state

```
HEAD =
d188b0262b18f2b1f841fed9d4557a0b37db0c2e

TREE =
a3993ac52e44bd5474df386767dc1c15097a8c5a

FORCE =
FALSE
```

The only concurrent repository change observed since the preceding governed state was FC01 material unrelated to E1-TD-03B.

The E1-TD-03 / E1-TD-03A / E1-TD-03B protected bindings remain byte-identical to the authority contract.

## 2. Prospective target

```
DATASET_ID =
SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1

SOURCE =
CarlosSilva1/ustech-ticks

WINDOW =
[2026-10-01T00:00:00Z,
 2027-10-01T00:00:00Z)

SOURCE_POLICY =
SOURCE_B_CONTINUATION_OR_BLOCK
```

The temporal gate has now been reached.

## 3. Current public provider metadata

Current public Hugging Face metadata for `CarlosSilva1/ustech-ticks` was inspected without downloading Parquet market-data objects.

Observed:

```
REPOSITORY =
CarlosSilva1/ustech-ticks

VISIBLE_REVISION_LABEL =
30996ad

TOTAL_FILE_SIZE =
3.94 GB

ROWS =
376,003,618

DECLARED_PERIOD =
2021-05-25 → 2026-05-24

PARTITIONING =
Hive-style year/month

LATEST_OBSERVED_TICK =
2026-05-24T23:59:59.963Z
```

No provider-defined object or partition containing timestamps on or after:

```
2026-10-01T00:00:00Z
```

was identified from the current public metadata.

This is a bounded availability finding, not a claim that no unpublished, hidden, or not-yet-indexed object exists.

## 4. Eligibility gate

```
NOT_BEFORE_REACHED =
TRUE

ELIGIBLE_PROSPECTIVE_SOURCE_OBJECT_IDENTIFIED =
FALSE

FIRST_REAL_ACQUISITION_REQUEST_STARTED =
FALSE

FIRST_GOVERNED_COLLECTION_EVENT_CONSUMED =
FALSE

EVENTS_CONSUMED =
0

EVENTS_AUTHORIZED =
1
```

Because the authority contract requires an eligible provider-defined request target before a real event may begin, no one-shot execution authority instance was created.

## 5. Execution firewall

No action in this preflight performed:

```
PARQUET_DOWNLOAD
MARKET_DATA_BYTE_DOWNLOAD
E1_TD_03A_COLLECTOR_EXECUTION
RAW_OBJECT_PRESERVATION
H1_BUILD
SIGNAL_GENERATION
TRADE_GENERATION
PERFORMANCE_COMPUTATION
PNL_OBSERVATION
BACKTEST
AWS_ACTION
JFOREX_ACTION
```

## 6. Verdict

```
E1_TD_03B_POSTWINDOW_PREFLIGHT =
WAITING_SOURCE_CONTINUATION

SOURCE_B_PROSPECTIVE_OBJECT =
NOT_IDENTIFIED

FIRST_COLLECTION_EVENT =
NOT_STARTED

EVENT_BUDGET =
0 / 1 CONSUMED

REAL_COLLECTION_NOW =
NOT_PERMITTED
```

## 7. Next boundary

The next permitted operation is another **read-only Source-B availability preflight** at a later time.

Only if a provider-defined object intersecting the prospective window is identified may ATDS proceed to:

1. fresh HEAD/TREE verification;
2. exact eligible-object selection under the frozen lexicographic rule;
3. creation of the non-self-referential one-shot authority instance;
4. exactly one governed real collection event;
5. STOP for human adjudication.

Until then:

```
WAITING_SOURCE_CONTINUATION
STOP = TRUE
```
