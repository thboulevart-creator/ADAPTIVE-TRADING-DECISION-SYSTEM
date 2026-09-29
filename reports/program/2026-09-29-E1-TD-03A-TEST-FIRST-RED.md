# E1-TD-03A — TEST-FIRST RED

Date: 2026-09-29

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `integration/system-v1`

## Protected preregistration

Contract:

`GOVERNANCE/E1-TD-03A-SOURCE-B-PROVENANCE-COLLECTOR-QUALIFICATION-CONTRACT-V0.1.json`

Breaker:

`breakers/e1_td_03a_acquisition_collector_red_breaker.py`

Workflow:

`.github/workflows/e1-td-03a-synthetic-qualification.yml`

Persisted workflow-triggering HEAD:

`a44a9181c36d12325149c0a589af73cadd9864d3`

GitHub Actions run:

`36563504475`

Job:

`109389763051`

## Observed RED

```text
TOTAL = 30
PASS = 0
FAIL = 30

COMMON_FAILURE =
E1_TD_03A_TARGET_ABSENT_EXPECTED_RED
```

All 30 preregistered cases reached the intentionally absent runtime target:

`tools/e1_td_03a_acquisition_collector.py`

The failure is therefore causal and expected.

The workflow also verified the exact persisted HEAD and clean worktree.

## Provenance recovery observation

Governed historical evidence identifies Source-B as:

```text
publisher dataset = CarlosSilva1/ustech-ticks
instrument = USTECH / Nasdaq 100 Index CFD
timestamp semantics = UTC tick time, millisecond precision
publisher declared provenance = Dukascopy via Tickstory
license = CC-BY-4.0
```

Protected provenance evidence:

`reports/data-qualification/e0_source_b_public_provenance_identity_2026-09-25.md`

blob:

`c3b74951d8c774bd761b5295c082ba3dfe8589cf`

Data-truth closure:

`reports/data-qualification/source_b_price_core_data_truth_closure_2026-09-25.md`

blob:

`62e9bd1e0892dab7273eed35c8704a9e05611112`

Limitation preserved:

```text
native Dukascopy tick-for-tick equivalence = NOT PROVEN
exact Tickstory transformations = NOT PROVEN
third-party broker feed equivalence = NOT PROVEN
```

This is documentary publisher provenance, not native-feed equivalence.

## Adjudication

```text
E1_TD_03A_PROVENANCE_RECOVERY =
PASS_DOCUMENTARY_PROVENANCE_WITH_LIMITATIONS

E1_TD_03A_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

RUNTIME_IMPLEMENTATION =
NOT_YET_PRESENT

ACTUAL_DATA_ACQUISITION =
NOT_AUTHORIZED

NEW_DATA_OBSERVATION =
NOT_AUTHORIZED

H1_BUILD =
NOT_AUTHORIZED

MOMENTUM_EXECUTION =
NOT_AUTHORIZED

PERFORMANCE_COMPUTATION =
NOT_AUTHORIZED

BACKTEST =
NOT_AUTHORIZED
```

The next permitted mutation is the minimal synthetic collector runtime required by the frozen 30-case breaker.

No performance authority is granted.
