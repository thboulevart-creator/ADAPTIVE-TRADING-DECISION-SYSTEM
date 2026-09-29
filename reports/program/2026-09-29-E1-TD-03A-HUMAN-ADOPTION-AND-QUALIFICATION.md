# E1-TD-03A — HUMAN ADOPTION + SOURCE-B PROVENANCE RECOVERY + SYNTHETIC COLLECTOR QUALIFICATION

Date: 2026-09-29

## Decision

```text
DECISION = ADOPT

FRONTIER =
E1-TD-03A
SOURCE-B PROVENANCE RECOVERY
+ ACQUISITION COLLECTOR TEST-FIRST QUALIFICATION

PERFORMANCE_STOP = TRUE
```

## Protected bindings

```text
E1-TD-03 contract blob =
c66c36bb5f01cb0a13e22eb9210abfdac74b35d3

E1-TD-03 human adoption blob =
0573472825af96938bab260c8d0b78431350c6ea

E1-TD-03A contract blob =
c6ed450ae0c6b36ae2412cc367261504980d5b43

E1-TD-03A breaker blob =
59593f273c45276f4af8e410ab05768ee730d6a6

E1-TD-03A workflow blob =
c6328148b7f4edc7a3e08ed624bc0eceed8dc9ec

E1-TD-03A RED report blob =
db2caa9cdffc00c4352430030b0537a099f577bd

E1-TD-03A runtime blob =
a90903320a168a845b2b72bafba15b8d8abb2950
```

## Source-B provenance recovery

Governed evidence supports:

```text
publisher dataset =
CarlosSilva1/ustech-ticks

economic instrument =
USTECH / Nasdaq 100 Index CFD

timestamp semantics =
UTC tick time, millisecond precision

publisher-declared provenance =
Dukascopy via Tickstory

license =
CC-BY-4.0
```

Protected provenance source:

`reports/data-qualification/e0_source_b_public_provenance_identity_2026-09-25.md`

blob:

`c3b74951d8c774bd761b5295c082ba3dfe8589cf`

Protected Source-B data-truth closure:

`reports/data-qualification/source_b_price_core_data_truth_closure_2026-09-25.md`

blob:

`62e9bd1e0892dab7273eed35c8704a9e05611112`

The following limitations remain binding:

```text
NATIVE_DUKASCOPY_TICK_FOR_TICK_EQUIVALENCE = NOT_PROVEN
EXACT_TICKSTORY_TRANSFORMATIONS = NOT_PROVEN
THIRD_PARTY_BROKER_FEED_EQUIVALENCE = NOT_PROVEN
VOLUMES_FOR_THIS_RESEARCH_PATH = NOT_QUALIFIED
```

Therefore:

```text
SOURCE_B_PROVENANCE_RECOVERY =
PASS_DOCUMENTARY_PROVENANCE_WITH_LIMITATIONS
```

This PASS does not convert publisher documentation into native-feed equivalence.

## Test-first chronology

Preregistered contract was persisted before implementation.

Frozen breaker was persisted before implementation.

Workflow-triggering preregistration HEAD:

`a44a9181c36d12325149c0a589af73cadd9864d3`

RED run:

```text
GitHub Actions run = 36563504475
job = 109389763051
TOTAL = 30
PASS = 0
FAIL = 30
COMMON_FAILURE = E1_TD_03A_TARGET_ABSENT_EXPECTED_RED
```

Adjudication:

```text
TEST_FIRST_RED = PASS_EXPECTED_FAILURE
```

The minimal runtime was then added without changing the frozen breaker.

Implementation HEAD:

`1d116f23f265c44e8bbc265a51afab27670f5e2f`

Qualification run:

```text
GitHub Actions run = 36563729419
job = 109390506668
TOTAL = 30
PASS = 30
FAIL = 0
WORKTREE = CLEAN
```

Adjudication:

```text
E1_TD_03A_SYNTHETIC_COLLECTOR_QUALIFICATION =
PASS_30_OF_30
```

## Qualified surface

The synthetic collector qualification covers only:

```text
documentary Source-B provenance
canonical JSON serialization
exact-byte SHA-256 verification
raw-object identity checking
source-row integrity checks
>60s gap inventory semantics
append-only acquisition ledger hash chaining
ledger tamper detection
visible retry events
performance-field rejection
canonical inventory digest
deterministic manifest construction
manifest validation
logical-window eligibility
premature-seal blocking
final seal binding
post-seal mutation detection
absence of strategy/performance runtime surface
absence of network acquisition implementation
absence of H1 construction
absence of automatic provider substitution
```

All fixtures were synthetic.

## Explicit non-authorizations

```text
ACTUAL_DATA_ACQUISITION = NOT_AUTHORIZED
NEW_DATA_OBSERVATION = NOT_AUTHORIZED
DATASET_MATERIALIZATION = NOT_AUTHORIZED
DATASET_BUILD = NOT_AUTHORIZED
H1_BUILD = NOT_AUTHORIZED
MOMENTUM_EXECUTION = NOT_AUTHORIZED
PERFORMANCE_COMPUTATION = NOT_AUTHORIZED
PNL_OBSERVATION = NOT_AUTHORIZED
BACKTEST = NOT_AUTHORIZED

STRATEGY_CHANGE = NOT_AUTHORIZED
PARAMETER_CHANGE = NOT_AUTHORIZED
LONG_ONLY = NOT_AUTHORIZED
SHORT_REMOVAL = NOT_AUTHORIZED
REGIME_FILTER = NOT_AUTHORIZED
OPTIMIZATION = NOT_AUTHORIZED

MT5 = NOT_AUTHORIZED
PAPER = NOT_AUTHORIZED
BROKER = NOT_AUTHORIZED
LIVE = NOT_AUTHORIZED
CAPITAL = NOT_AUTHORIZED
```

## Final state

```text
E1_TD_03 = ADOPTED

E1_TD_03A =
ADOPTED_AND_SYNTHETICALLY_QUALIFIED

SOURCE_B_PROVENANCE_GATE =
PASS_DOCUMENTARY_PROVENANCE_WITH_LIMITATIONS

ACQUISITION_COLLECTOR =
QUALIFIED_SYNTHETIC_ONLY

PROSPECTIVE_DATASET_ID =
SOURCE_B_USTECH_TD01_PROSPECTIVE_20261001_20271001_V0_1

PROSPECTIVE_DATASET =
NOT_MATERIALIZED

PERFORMANCE_STOP =
TRUE
```

## STOP

No authority to collect or inspect real prospective data is created by this record.

Any next frontier must be separately human-authorized.

```text
STOP = TRUE
```
