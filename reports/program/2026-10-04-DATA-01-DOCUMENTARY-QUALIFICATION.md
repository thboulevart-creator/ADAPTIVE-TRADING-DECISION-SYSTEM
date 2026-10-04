# DATA-01 — FIRST-USE DATA SURFACE + CLAIM-SCOPED CONTRACT — DOCUMENTARY QUALIFICATION

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Date:** 2026-10-04  
**Mode:** `DOCUMENTARY / STATIC / NO DATA RUNTIME IMPLEMENTATION`

## 1. Authorized parent

```text
AUTHORIZED_PARENT_HEAD =
1a4ea7f19a4bdee0cd632f8f42adb40fa1f0fe86

AUTHORIZED_PARENT_TREE =
b84b4a8538be3eb4a34d81665202e217cf3c483f
```

Fresh preflight verified the exact branch state and the required RVO-01 through RVO-04 identities before DATA-01 mutation.

## 2. Exact first-use selection

DATA-01 did not choose a dataset merely because it already had a runtime or because a later strategy-specific derivation existed.

The selected first-use surface is:

```text
CLAIM CLASS =
CC02_DESCRIPTIVE_MARKET_BEHAVIOR

SEMANTIC LIMIT =
RETROSPECTIVE_DESCRIPTIVE_ONLY

FIRST CANONICAL CONSUMER =
ATDS_AP1_INTRADAY_SPREAD_CENSUS_V0_1

SELECTED DATASET IDENTITY =
USTECH_PROFILE_MINUTE_CORE_V0_1

DATASET FAMILY =
AP0_GAP_AWARE_1_MINUTE_MONTHLY_PARQUET

AP0 MANIFEST SHA-256 =
62cccc5bbcb6dde00d5a1bd69616ba1fe7794839055d668772b3d367f826a5ce
```

The selection is derived from the canonical Asset Behavioral Profile route:

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
        ↓
AP0 USTECH_PROFILE_MINUTE_CORE_V0_1
        ↓
AP1 INTRADAY / SPREAD CENSUS
```

The Asset Behavioral Profile protocol requires AP0 before behavioral statistics, and the AP0 adjudication explicitly authorizes AP1 as the next strictly descriptive consumer.

## 3. Why the alternatives were not selected

### Raw Source-B Parquet

```text
SOURCE_B_USTECH_PRICE_CORE_V0_1
```

remains the qualified parent/source truth and contains the raw timestamp/bid/ask information.

It remains necessary for genuinely sub-minute questions.

It is not selected as the minimum first-use consumer surface because the canonical first descriptive AP1 census consumes the already-qualified AP0 minute representation directly.

### E1 H1

```text
USTECH_E1_H1_MID_CLOSE_GAP_AWARE_V0_1
```

is technically qualified in its E1-specific boundary, but it is downstream of AP0 and removes minute/spread structure required by the first descriptive consumer.

```text
QUALIFIED
!=
MINIMUM REQUIRED FIRST-USE SURFACE
```

### Generic tick CSV runtime

```text
src/data/dataset_admissibility.py
```

is executable and tested, but it addresses a separate five-column tick-CSV representation.

```text
AVAILABLE
!=
SELECTED
```

It does not identify the canonical AP0 corpus or its transformation lineage.

## 4. Selected AP0 identity

The selected AP0 dataset is already canonically adjudicated as a derived DatasetIdentity:

```text
FILES =
61 monthly Parquet

MINUTE ROWS =
1,709,180

SOURCE TICKS ACCOUNTED =
376,003,618

SOURCE IDENTITY =
SOURCE_B_USTECH_PRICE_CORE_V0_1

TRANSFORMER BLOB =
42fcb38809a1cc0365cd4027fae5154e1d6d3b4f

AP0 ADJUDICATION BLOB =
94bba3315e3569993623b8cd2a2bf4264f4ab6f8
```

The exact full schema remains material even though the AP1 consumer reads only a subset of columns.

This prevents an unread-field schema drift from being silently treated as equivalent input.

## 5. DATA-01 documentary artifacts

```text
FIRST-USE REQUIREMENTS MAP =
2d6d43d783281ee3dfd4028bc9b84c4dce495b87

CLAIM-SCOPED DATA CONTRACT =
ec013c8db53b482770a62016db50b113b19ecd7f

DATA ↔ TEMPORAL BOUNDARY =
4bdb9d6c7448759c0349048fd4f48abba296c0cf

FROZEN ADVERSARIAL BREAKER CONTRACT =
d9cafc53c863341ca827097014411702c26633f2

DOCUMENTARY / STATIC BREAKER =
8bce54c4964d970cd703e803f55ccae089d814da

QUALIFICATION WORKFLOW =
11df8a56e95e783240439f343196e50ccf2d6234
```

## 6. Provenance minimum frozen by DATA-01

For this first-use claim, the contract requires at minimum:

```text
- immutable dataset identity;
- frozen dataset/content state;
- exact AP0 manifest SHA-256;
- exact 61-file path/size/hash set;
- exact schema identity;
- exact SOURCE_B parent identity;
- transformation identity;
- material transformation parameters;
- coverage / integrity evidence;
- usage envelope;
- exact result-to-dataset binding;
- reproducibility reference;
- explicit LINEAGE UNKNOWN if unresolved.
```

A derived dataset cannot inherit the parent PASS.

```text
PARENT DATASET PASS
!=
CHILD DATASET PASS
```

## 7. Data / Temporal firewall

The first-use claim is retrospective descriptive only.

Therefore:

```text
TEMPORAL STATUS =
NOT_APPLICABLE_WITH_EXPLICIT_BASIS
```

This is not a Temporal PASS.

DATA-01 may validate encoded market timestamps, period coverage, ordering and gap/segment metadata.

It may not adjudicate:

```text
known_from
historical PIT availability
decision-time admissibility
vintage availability
publication delay
temporal dependency leakage
historical tradability
```

If a future predictive, historical, economic or OOS claim requires those predicates:

```text
TEMPORAL_OWNER_REQUIRED
```

## 8. Frozen adversarial target

The DATA-01 breaker contract freezes:

```text
32 CASES
9 FAILURE-MODE CLASSES
```

including the mandated attacks on:

- same filename / different bytes;
- same dataset ID / different bytes;
- silent substitution;
- parent-PASS inheritance;
- missing provenance;
- missing lineage;
- schema drift;
- row/domain corruption;
- ordering corruption;
- gap/transformation ambiguity;
- unverifiable-source laundering;
- usage overreach;
- cross-claim reuse;
- Temporal authority laundering;
- latest-data-as-historical laundering;
- missing result binding;
- immutable/mutable identity confusion;
- UNKNOWN/UNVERIFIED laundering;
- RVO-over-owner authority;
- scientific/trading authority laundering;
- non-minimal H1/tick/raw surface selection;
- false universal sufficiency of AP0.

## 9. Initial static qualification failure and correction

The first workflow run was:

```text
COMMIT =
e4729577d494e71c76e558130227e4d49e3d0405

RUN_ID =
37219602383

JOB_ID =
111487078884

RESULT =
FAILURE

STATIC TESTS =
24 passed / 1 failed
```

The failure did not identify a semantic defect in the frozen DATA-01 contract.

The static meta-test searched for the literal phrase:

```text
usage envelope
```

inside the natural-language attack strings, while the frozen `DATA01-B18` already encoded the same failure mode through its attack semantics and expected result:

```text
BLOCKED_USAGE_ENVELOPE_VIOLATION
```

The correction therefore changed only the static assertion wording and its workflow-pinned blob.

The frozen breaker contract remained byte-identical:

```text
d9cafc53c863341ca827097014411702c26633f2
```

No breaker intent was weakened after observing results.

## 10. Successful documentary qualification

Corrected commit:

```text
17186ae4d9403978fdbf85f3bed832ee12cb59d4

TREE =
951d7daa349ca4b65f5ba0222c924cb2e4f33dfa

WORKFLOW RUN =
37219696461

JOB =
111487357463

CONCLUSION =
SUCCESS
```

Observed counts:

```text
DATA-01 DOCUMENTARY / STATIC BREAKER =
25 passed

RVO-04 ROUTING BREAKER =
25 passed

EXISTING TICK-CSV DATA BOUNDARY TESTS =
9 passed

DATA-01 DELTA CHECK =
PASS_DOCUMENTARY_STATIC_ONLY
```

## 11. Candidate verdict

```text
DATA_01_FIRST_USE_SURFACE_SELECTION =
PASS

SELECTED_SURFACE =
USTECH_PROFILE_MINUTE_CORE_V0_1

DATA_01_CLAIM_SCOPED_CONTRACT =
PASS_DOCUMENTARY

DATA_01_DATA_TEMPORAL_BOUNDARY =
PASS_DOCUMENTARY

DATA_01_FROZEN_BREAKER_DESIGN =
PASS_DOCUMENTARY

DATA_RUNTIME_IMPLEMENTATION =
NOT_PERFORMED

DATA_RUNTIME_MODIFICATION =
NONE

REAL_DATA_CONSUMPTION =
NONE

REAL_EMPIRICAL_EXPERIMENT =
NONE

OOS_CONSUMPTION =
NONE

RVO_AUTHORITY =
NONE

DATA_01_QUALIFICATION =
PASS_CANDIDATE
```

This verdict remains subject to an exact persisted-HEAD rebreak after persistence of this report and the machine-readable receipt.

## 12. STOP

```text
DATA-02 =
NOT_AUTHORIZED

RVO-05 =
NOT_AUTHORIZED

NEW DATA IMPLEMENTATION =
NOT_AUTHORIZED

MODIFICATION OF src/data/* =
NOT_AUTHORIZED

REAL EMPIRICAL EXPERIMENT =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED

OOS =
NOT_AUTHORIZED

PAPER / BROKER / LIVE / CAPITAL =
NOT_AUTHORIZED
```
