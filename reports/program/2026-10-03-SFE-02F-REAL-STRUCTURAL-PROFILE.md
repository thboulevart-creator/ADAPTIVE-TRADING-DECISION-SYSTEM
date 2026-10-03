# SFE-02F — REAL STRUCTURAL CONTINUITY PROFILE V0.2

**Date:** 2026-10-03  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Status:** `STRUCTURAL_PROFILE_PRODUCED_ON_EXPOSED_SURFACE`

## 1. Execution boundary

This report records the authorized real execution of the human-adopted SFE-02F V0.2 structural continuity diagnostic.

```text
EVIDENCE = EXPLORATORY / EXPOSED
PRISTINE_CONFIRMATORY = FALSE
STRATEGY_CONFIRMATION = FORBIDDEN
```

Execution base and protected identities:

```text
HEAD = 1c2a1ecf9eddb5566fed0b692f1c38ea67b1a405
TREE = 66cddc96ec2ac8c50f5f51a71024bec09e7ab077
DESIGN_BLOB = 9d822cc829a0a8360cbd4533ffa87889e9730440
READINESS_CONTRACT_BLOB = 05c28bf23c0df7f39e8545d1ff6b7c4001d9f2e0
RUNTIME_BLOB = c68b07c3290e86d374bd8c967dc216e64ab1b13f
BREAKER_BLOB = 4b7bea90ae22df7f41e84ec02f43b75a35d9f30f
E1_03_RUNTIME_BLOB = 38d481755e00ce3c2ed9c66c4db710500ca0911a
```

Frozen breaker replay immediately before real execution:

```text
PASS = 34
FAIL = 0
```

## 2. Dataset identity gate

```text
DATASET = USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1
RECORDED_JSONL_SHA256 = 94ccb7c78e2e21cb3baa2dfe0945e7b39e20f74300c3c72addb89135d5af1ca0
CANONICAL_STREAM_SHA256 = 15cbc898814c6128ca05b27735626e225c1eda3e45f882b166b654886967e59f
N_ROWS = 27677
N_BLOCKS = 1436
FIRST_H1 = 2021-05-25T01:00:00Z
LAST_H1 = 2026-05-24T22:00:00Z
```

All frozen dataset-identity checks passed before structural output.

## 3. Calendar identity gate

```json
{
  "america_new_york_tzif_sha256": "d7f2206b3a45989fc9ad63d558922532fa7352280d5f87176bf1db79cb1d1fa9",
  "iana_tzdb_release": "2026c",
  "python_implementation": "cpython",
  "python_version": "3.13.14",
  "timezone_key": "America/New_York",
  "timezone_library": "stdlib.zoneinfo",
  "tzdata_package_version": "2026.3",
  "zoneinfo_tzpath_exact": []
}
```

`G-05 = PASS` on the exact frozen runtime/calendar identity.

## 4. Determinism and continuity integrity

```text
RUNTIME_PROFILE_STATUS = SYNTHETIC_PROFILE_PRODUCED
DETERMINISTIC_REPLAY_EXACT_EQUAL = TRUE
N_INTERNAL_BOUNDARIES = 1435
N_TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT = 0
```

No canonical-integrity or upstream-semantics blocker fired.

## 5. Dataset / block totals

```text
N_ROWS = 27677
N_BLOCKS = 1436
N_INTERNAL_BOUNDARIES = 1435
N_DATASET_START_TRUNCATED_BLOCKS = 1
N_DATASET_END_TRUNCATED_BLOCKS = 1
N_DATASET_END_TERMINALS = 1
```

## 6. Block-length geometry

```text
BLOCK_LENGTH_MIN = 1
BLOCK_LENGTH_MAX = 22
BLOCK_LENGTH_MEDIAN = 22
BLOCK_LENGTH_Q25 = 21
BLOCK_LENGTH_Q75 = 22
N_BLOCKS_LENGTH_1 = 17
N_BLOCKS_LENGTH_2_TO_20 = 316
N_BLOCKS_LENGTH_21 = 279
N_BLOCKS_LENGTH_GE_22 = 824
FRACTION_BLOCKS_LENGTH_LE_20 = 0.2318941504178273
FRACTION_BLOCKS_LENGTH_GE_21 = 0.7681058495821727
```

Exact block-length histogram:

```json
{
  "1": 17,
  "2": 11,
  "3": 13,
  "4": 26,
  "5": 18,
  "6": 22,
  "7": 10,
  "8": 13,
  "9": 15,
  "10": 11,
  "11": 12,
  "12": 12,
  "13": 8,
  "14": 17,
  "15": 18,
  "16": 20,
  "17": 21,
  "18": 29,
  "19": 20,
  "20": 20,
  "21": 279,
  "22": 824
}
```

Interior-only block-length summary:

```text
INTERIOR_BLOCK_LENGTH_MIN = 1
INTERIOR_BLOCK_LENGTH_MAX = 22
INTERIOR_BLOCK_LENGTH_MEDIAN = 22
INTERIOR_BLOCK_LENGTH_Q25 = 21
INTERIOR_BLOCK_LENGTH_Q75 = 22
```

Interior exact histogram:

```json
{
  "1": 16,
  "2": 11,
  "3": 13,
  "4": 26,
  "5": 18,
  "6": 22,
  "7": 10,
  "8": 13,
  "9": 15,
  "10": 11,
  "11": 12,
  "12": 12,
  "13": 8,
  "14": 17,
  "15": 18,
  "16": 20,
  "17": 21,
  "18": 29,
  "19": 19,
  "20": 20,
  "21": 279,
  "22": 824
}
```

## 7. Ending-ordinal geometry

```text
BLOCK_END_ORDINAL_MIN = 0
BLOCK_END_ORDINAL_MAX = 21
BLOCK_END_ORDINAL_MEDIAN = 21
```

```json
{
  "0": 16,
  "1": 11,
  "2": 13,
  "3": 26,
  "4": 18,
  "5": 22,
  "6": 10,
  "7": 13,
  "8": 15,
  "9": 11,
  "10": 12,
  "11": 12,
  "12": 8,
  "13": 17,
  "14": 18,
  "15": 20,
  "16": 21,
  "17": 29,
  "18": 20,
  "19": 20,
  "20": 279,
  "21": 824
}
```

## 8. Frozen 20-H1 warmup / same-block t+1 availability

```text
N_WARMUP_MATURE_ROWS = 1927
N_WARMUP_MATURE_ROWS_WITH_SAME_BLOCK_T1 = 824
N_WARMUP_MATURE_INTERNAL_BLOCK_END_ROWS = 1103
N_WARMUP_MATURE_DATASET_END_ROWS = 0
FRACTION_WARMUP_MATURE_WITH_SAME_BLOCK_T1 = 0.4276076803321225
FRACTION_WARMUP_MATURE_AT_INTERNAL_BLOCK_END = 0.5723923196678775
```

These values describe mechanical structural availability only. No strategy-event membership was read.

## 9. Boundary mechanisms

```json
{
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP": 1435,
  "SOURCE_SEGMENT_CHANGE_ONLY": 0,
  "TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT": 0
}
```

The preregistered expectation `TEMPORAL_GAP_WITHIN_SOURCE_SEGMENT = 0` is satisfied.

## 10. Calendar / schedule geometry

UTC weekday counts:

```json
{
  "1": 292,
  "2": 286,
  "3": 281,
  "4": 288,
  "5": 287,
  "7": 1
}
```

UTC hour counts:

```json
{
  "0": 4,
  "1": 3,
  "2": 2,
  "3": 5,
  "4": 12,
  "5": 5,
  "6": 5,
  "7": 6,
  "8": 4,
  "9": 7,
  "10": 10,
  "11": 3,
  "12": 10,
  "13": 15,
  "14": 16,
  "15": 14,
  "16": 24,
  "17": 24,
  "18": 10,
  "19": 4,
  "20": 825,
  "21": 417,
  "23": 10
}
```

UTC weekday × hour:

```json
{
  "1|01": 1,
  "1|03": 2,
  "1|04": 3,
  "1|05": 1,
  "1|06": 2,
  "1|07": 4,
  "1|09": 2,
  "1|10": 4,
  "1|11": 1,
  "1|12": 2,
  "1|13": 1,
  "1|14": 5,
  "1|15": 3,
  "1|16": 13,
  "1|17": 12,
  "1|18": 3,
  "1|19": 2,
  "1|20": 153,
  "1|21": 76,
  "1|23": 2,
  "2|04": 1,
  "2|05": 1,
  "2|06": 1,
  "2|07": 1,
  "2|08": 1,
  "2|10": 4,
  "2|11": 1,
  "2|12": 2,
  "2|13": 4,
  "2|14": 1,
  "2|15": 2,
  "2|16": 4,
  "2|17": 1,
  "2|18": 1,
  "2|19": 1,
  "2|20": 169,
  "2|21": 89,
  "2|23": 2,
  "3|04": 4,
  "3|05": 1,
  "3|08": 2,
  "3|12": 2,
  "3|13": 3,
  "3|14": 5,
  "3|15": 2,
  "3|17": 3,
  "3|18": 1,
  "3|20": 170,
  "3|21": 86,
  "3|23": 2,
  "4|00": 3,
  "4|04": 3,
  "4|07": 1,
  "4|09": 3,
  "4|10": 2,
  "4|11": 1,
  "4|12": 1,
  "4|13": 5,
  "4|14": 3,
  "4|15": 1,
  "4|16": 4,
  "4|17": 7,
  "4|19": 1,
  "4|20": 168,
  "4|21": 82,
  "4|23": 3,
  "5|00": 1,
  "5|01": 2,
  "5|02": 2,
  "5|03": 3,
  "5|04": 1,
  "5|05": 2,
  "5|06": 2,
  "5|08": 1,
  "5|09": 2,
  "5|12": 3,
  "5|13": 2,
  "5|14": 2,
  "5|15": 6,
  "5|16": 3,
  "5|17": 1,
  "5|18": 5,
  "5|20": 165,
  "5|21": 84,
  "7|23": 1
}
```

UTC calendar month:

```json
{
  "1": 116,
  "2": 108,
  "3": 132,
  "4": 121,
  "5": 124,
  "6": 113,
  "7": 121,
  "8": 133,
  "9": 123,
  "10": 116,
  "11": 115,
  "12": 113
}
```

UTC calendar year:

```json
{
  "2021": 171,
  "2022": 279,
  "2023": 290,
  "2024": 280,
  "2025": 283,
  "2026": 132
}
```

## 11. Mandatory structural cross-tabs

NY DST state × UTC weekday × hour:

```json
{
  "DST|1|04": 3,
  "DST|1|05": 1,
  "DST|1|06": 1,
  "DST|1|07": 3,
  "DST|1|09": 1,
  "DST|1|10": 4,
  "DST|1|11": 1,
  "DST|1|13": 1,
  "DST|1|14": 5,
  "DST|1|15": 3,
  "DST|1|16": 13,
  "DST|1|17": 4,
  "DST|1|19": 2,
  "DST|1|20": 153,
  "DST|1|23": 2,
  "DST|2|04": 1,
  "DST|2|05": 1,
  "DST|2|06": 1,
  "DST|2|07": 1,
  "DST|2|08": 1,
  "DST|2|10": 3,
  "DST|2|12": 2,
  "DST|2|13": 2,
  "DST|2|14": 1,
  "DST|2|15": 2,
  "DST|2|16": 3,
  "DST|2|19": 1,
  "DST|2|20": 169,
  "DST|2|23": 2,
  "DST|3|04": 4,
  "DST|3|05": 1,
  "DST|3|08": 2,
  "DST|3|12": 2,
  "DST|3|13": 2,
  "DST|3|14": 4,
  "DST|3|15": 1,
  "DST|3|17": 3,
  "DST|3|20": 169,
  "DST|3|23": 2,
  "DST|4|00": 3,
  "DST|4|04": 2,
  "DST|4|07": 1,
  "DST|4|09": 1,
  "DST|4|10": 1,
  "DST|4|13": 2,
  "DST|4|14": 2,
  "DST|4|15": 1,
  "DST|4|16": 3,
  "DST|4|17": 3,
  "DST|4|20": 168,
  "DST|4|23": 3,
  "DST|5|00": 1,
  "DST|5|01": 1,
  "DST|5|02": 1,
  "DST|5|03": 2,
  "DST|5|04": 1,
  "DST|5|05": 2,
  "DST|5|06": 2,
  "DST|5|08": 1,
  "DST|5|09": 1,
  "DST|5|12": 2,
  "DST|5|13": 2,
  "DST|5|14": 2,
  "DST|5|15": 5,
  "DST|5|16": 3,
  "DST|5|18": 1,
  "DST|5|20": 165,
  "DST|7|23": 1,
  "STANDARD|1|01": 1,
  "STANDARD|1|03": 2,
  "STANDARD|1|06": 1,
  "STANDARD|1|07": 1,
  "STANDARD|1|09": 1,
  "STANDARD|1|12": 2,
  "STANDARD|1|17": 8,
  "STANDARD|1|18": 3,
  "STANDARD|1|21": 76,
  "STANDARD|2|10": 1,
  "STANDARD|2|11": 1,
  "STANDARD|2|13": 2,
  "STANDARD|2|16": 1,
  "STANDARD|2|17": 1,
  "STANDARD|2|18": 1,
  "STANDARD|2|21": 89,
  "STANDARD|3|13": 1,
  "STANDARD|3|14": 1,
  "STANDARD|3|15": 1,
  "STANDARD|3|18": 1,
  "STANDARD|3|20": 1,
  "STANDARD|3|21": 86,
  "STANDARD|4|04": 1,
  "STANDARD|4|09": 2,
  "STANDARD|4|10": 1,
  "STANDARD|4|11": 1,
  "STANDARD|4|12": 1,
  "STANDARD|4|13": 3,
  "STANDARD|4|14": 1,
  "STANDARD|4|16": 1,
  "STANDARD|4|17": 4,
  "STANDARD|4|19": 1,
  "STANDARD|4|21": 82,
  "STANDARD|5|01": 1,
  "STANDARD|5|02": 1,
  "STANDARD|5|03": 1,
  "STANDARD|5|09": 1,
  "STANDARD|5|12": 1,
  "STANDARD|5|15": 1,
  "STANDARD|5|17": 1,
  "STANDARD|5|18": 4,
  "STANDARD|5|21": 84
}
```

NY UTC offset × UTC weekday × hour:

```json
{
  "-14400|1|04": 3,
  "-14400|1|05": 1,
  "-14400|1|06": 1,
  "-14400|1|07": 3,
  "-14400|1|09": 1,
  "-14400|1|10": 4,
  "-14400|1|11": 1,
  "-14400|1|13": 1,
  "-14400|1|14": 5,
  "-14400|1|15": 3,
  "-14400|1|16": 13,
  "-14400|1|17": 4,
  "-14400|1|19": 2,
  "-14400|1|20": 153,
  "-14400|1|23": 2,
  "-14400|2|04": 1,
  "-14400|2|05": 1,
  "-14400|2|06": 1,
  "-14400|2|07": 1,
  "-14400|2|08": 1,
  "-14400|2|10": 3,
  "-14400|2|12": 2,
  "-14400|2|13": 2,
  "-14400|2|14": 1,
  "-14400|2|15": 2,
  "-14400|2|16": 3,
  "-14400|2|19": 1,
  "-14400|2|20": 169,
  "-14400|2|23": 2,
  "-14400|3|04": 4,
  "-14400|3|05": 1,
  "-14400|3|08": 2,
  "-14400|3|12": 2,
  "-14400|3|13": 2,
  "-14400|3|14": 4,
  "-14400|3|15": 1,
  "-14400|3|17": 3,
  "-14400|3|20": 169,
  "-14400|3|23": 2,
  "-14400|4|00": 3,
  "-14400|4|04": 2,
  "-14400|4|07": 1,
  "-14400|4|09": 1,
  "-14400|4|10": 1,
  "-14400|4|13": 2,
  "-14400|4|14": 2,
  "-14400|4|15": 1,
  "-14400|4|16": 3,
  "-14400|4|17": 3,
  "-14400|4|20": 168,
  "-14400|4|23": 3,
  "-14400|5|00": 1,
  "-14400|5|01": 1,
  "-14400|5|02": 1,
  "-14400|5|03": 2,
  "-14400|5|04": 1,
  "-14400|5|05": 2,
  "-14400|5|06": 2,
  "-14400|5|08": 1,
  "-14400|5|09": 1,
  "-14400|5|12": 2,
  "-14400|5|13": 2,
  "-14400|5|14": 2,
  "-14400|5|15": 5,
  "-14400|5|16": 3,
  "-14400|5|18": 1,
  "-14400|5|20": 165,
  "-14400|7|23": 1,
  "-18000|1|01": 1,
  "-18000|1|03": 2,
  "-18000|1|06": 1,
  "-18000|1|07": 1,
  "-18000|1|09": 1,
  "-18000|1|12": 2,
  "-18000|1|17": 8,
  "-18000|1|18": 3,
  "-18000|1|21": 76,
  "-18000|2|10": 1,
  "-18000|2|11": 1,
  "-18000|2|13": 2,
  "-18000|2|16": 1,
  "-18000|2|17": 1,
  "-18000|2|18": 1,
  "-18000|2|21": 89,
  "-18000|3|13": 1,
  "-18000|3|14": 1,
  "-18000|3|15": 1,
  "-18000|3|18": 1,
  "-18000|3|20": 1,
  "-18000|3|21": 86,
  "-18000|4|04": 1,
  "-18000|4|09": 2,
  "-18000|4|10": 1,
  "-18000|4|11": 1,
  "-18000|4|12": 1,
  "-18000|4|13": 3,
  "-18000|4|14": 1,
  "-18000|4|16": 1,
  "-18000|4|17": 4,
  "-18000|4|19": 1,
  "-18000|4|21": 82,
  "-18000|5|01": 1,
  "-18000|5|02": 1,
  "-18000|5|03": 1,
  "-18000|5|09": 1,
  "-18000|5|12": 1,
  "-18000|5|15": 1,
  "-18000|5|17": 1,
  "-18000|5|18": 4,
  "-18000|5|21": 84
}
```

Boundary reason × UTC weekday × hour:

```json
{
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|01": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|03": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|04": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|05": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|06": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|07": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|09": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|10": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|11": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|12": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|13": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|14": 5,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|15": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|16": 13,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|17": 12,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|18": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|19": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|20": 153,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|21": 76,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|1|23": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|04": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|05": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|06": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|07": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|08": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|10": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|11": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|12": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|13": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|14": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|15": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|16": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|17": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|18": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|19": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|20": 169,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|21": 89,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|2|23": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|04": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|05": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|08": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|12": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|13": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|14": 5,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|15": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|17": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|18": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|20": 170,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|21": 86,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|3|23": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|00": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|04": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|07": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|09": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|10": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|11": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|12": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|13": 5,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|14": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|15": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|16": 4,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|17": 7,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|19": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|20": 168,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|21": 82,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|4|23": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|00": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|01": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|02": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|03": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|04": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|05": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|06": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|08": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|09": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|12": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|13": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|14": 2,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|15": 6,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|16": 3,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|17": 1,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|18": 5,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|20": 165,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|5|21": 84,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|7|23": 1
}
```

Boundary reason × NY DST state:

```json
{
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|DST": 960,
  "SOURCE_SEGMENT_CHANGE_AND_TEMPORAL_GAP|STANDARD": 475
}
```

The machine evidence artifact persists all 1435 per-boundary calendar annotations.

## 12. Upstream Source-B context

```text
ROW_LEVEL_UPSTREAM_CLASSIFICATION = UNRESOLVED
```

Only already-persisted aggregate upstream facts are restated:

```json
{
  "DEMONSTRATED_HISTORICAL_ACQUISITION_LOSSES": 13,
  "HISTORICAL_UNKNOWN_GAPS": 9,
  "IN_REGULAR_SESSION_PRE_HOLIDAY_OVERLAY": 315,
  "REGULAR_SESSION_BOUNDARIES": 1290,
  "SOURCE_B_GAPS_GT_60S": 1605
}
```

These aggregate categories are not assumed mutually exclusive.

## 13. Firewalls preserved

```text
TD03B_CONSUMED = FALSE
C01_RESERVED_EVIDENCE_CONSUMED = FALSE
STRATEGY_SIGNAL_CONSUMED = FALSE
PNL_CONSUMED = FALSE
```

No strategy-event statistic from SFE-02D is reproduced or juxtaposed here.

No causal claim is made about SFE-02D non-decision, strategy performance, provider defect, missingness neutrality, or continuity redesign.

## 14. Machine evidence identity

```text
LOCAL_CANONICAL_EVIDENCE_SHA256 = bf95435742f8ccb920e3ceeb69839b4b178f11ebbf088b55e6ab90e7cd6abfe5
GIT_EVIDENCE_BLOB = 1511df635588f1cc25a99aff945765d40f41e29f
```

Evidence path:

`reports/program/evidence/sfe-02f/SFE-02F-REAL-STRUCTURAL-PROFILE-V0.2.json`

## 15. Terminal status

```text
SFE_02F_V0_2_REAL_EXECUTION = STRUCTURAL_PROFILE_PRODUCED_ON_EXPOSED_SURFACE
STOP = TRUE
NEXT = HUMAN_ADJUDICATION_OR_DEFER
```

No SFE-02G, continuity redesign, strategy replication, strategy revision, new response horizon, or new backtest is opened by this result.
