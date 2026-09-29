# E1 — EXPERIMENTAL MEMORY FINAL V0.1

## Status

```text
RECORD_ID = ATDS_E1_EXPERIMENTAL_MEMORY_FINAL_V0_1
EXPERIMENT_ID = ATDS_E1_MOMENTUM_V1_SOURCE_B_EXPLORATORY_N0_V0
STATUS = ADOPTED_FOR_PERSISTENCE
E1 = CLOSED_AS_EXPLORATORY_EXPERIMENT
STRATEGY_VALIDATED = FALSE
NEXT_EXPERIMENT_AUTHORIZED = FALSE
```

This record is the durable experimental memory produced by E1. It preserves observations, hypotheses, unknowns, unsupported claims, execution failures and methodological learnings as distinct epistemic classes.

## Canonical binding

```text
repository = thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM
branch = integration/system-v1
pre-persistence HEAD = 6554e19d3313bbafb1f6afde4d1a0dcb2548af56
pre-persistence TREE = 7ad0db08503d599a8efbbe90ecd0aad273574de0
executor blob = 5a91f7b072fb37e8653027c387096ced6da9c053
```

## Experiment identity

```text
strategy = MOMENTUM_V1
mode = OFFLINE
class = EXPLORATORY
research level = N0
dataset = SOURCE_B_USTECH_PRICE_CORE_V0_1
timeframe = H1
lookback = 20 completed admissible H1 bars
OOS = 2025-05-25T00:00:00Z → 2026-05-24T23:59:59.963Z
```

Frozen strategy semantics: momentum = Close_t / Close_t-20 - 1; positive → LONG, negative → SHORT, zero → NEUTRAL; same-bar execution forbidden; earliest execution t+1; no pyramiding, stop-loss, take-profit, trailing stop, break-even, regime filter, discretionary override or parameter optimization.

## Execution history

### E1-REAL-001

```text
STATUS = ABORTED_PRE_OOS
CAUSE = AUTHORITY_EXECUTOR_MISMATCH
AUTHORITY_CONSUMED = FALSE
OOS_EXPOSED = FALSE
```

Windows worktree byte materialization differed from canonical Git bytes. No recoverable OOS result was produced.

### E1-REAL-002

```text
STATUS = ABORTED_AFTER_OOS_COMPUTATION
AUTHORITY_CONSUMED = TRUE
EXPOSURE_RECORD_CREATED = TRUE
RESULT_PERSISTED = FALSE
TRACE_PERSISTED = FALSE
OOS_EXPOSED = TRUE
OOS_UNTOUCHED = FALSE
```

Failure: `E1_07_INVALID_ENVIRONMENT_DESCRIPTOR`.

The OOS metrics were computed in memory before persistence failed. They are not a recoverable result, but the OOS became exposed permanently at this point.

### E1-REAL-003

```text
STATUS = PASS
CLASSIFICATION = REPRODUCTION_OF_EXPOSED_OOS
OOS_EXPOSED = TRUE
OOS_UNTOUCHED = FALSE
OOS_CLEAN = FALSE
HARD_STOP = TRUE
AUTOMATIC_RERUN = FORBIDDEN
```

E1-REAL-003 is not independent confirmation. It is the first persisted reproduction of an OOS already exposed during E1-REAL-002.

## Evidence identities

```text
AUTHORITY_DIGEST = c0c29cfd836cab34a42d76524377d4958ba7cecb97596594b8ef1963bacb2dfc
EXPOSURE_DIGEST  = b47fe0ec3c057b5de60858b2e35717be5274bf56d27eb07a01ad66913d39af35
RESULT_DIGEST    = 56eaf2626629bff2ff7b6dcd13e2ca178edddf06aade81f9480c4e3d142cf738
TRACE_DIGEST     = b29b50b61f6b6a9c58aaecb7dcf5fdd896b8e8414a64f2316f243dd38605ed35
```

Read-only evidence audit:

```text
AUTHORITY_DIGEST = VERIFIED
EXPOSURE_DIGEST = VERIFIED
RESULT_DIGEST = VERIFIED
TRACE_DIGEST = VERIFIED
USED_MARKER_BINDING = VERIFIED
AUTHORITY→EXPOSURE→RESULT→TRACE = PASS
TRADE_LEDGER_INTERNAL_INTEGRITY = PASS
METRICS_RECONSTRUCTION = PASS
GIT_BINDING = PASS
OOS_CLASSIFICATION = PASS
EVIDENCE_INTEGRITY = PASS_WITH_DOCUMENTED_LIMITATIONS
```

Limitations: the evidence ZIP does not contain the 212 Source-B Parquet files, complete H1 dataset, or complete E1-05 runner records. Internal result integrity and metrics-from-ledger are independently verifiable; full tick-level reproduction from that ZIP alone is not available.

## Cost scope

```text
RAW BID/ASK SPREAD = INCLUDED
COMMISSION = EXCLUDED, NOT ASSUMED ZERO
SLIPPAGE = EXCLUDED, NOT ASSUMED ZERO
FINANCING = EXCLUDED, NOT ASSUMED ZERO
```

No broker-net, all-in-cost, live-profitability or full broker execution realism claim is supported.

## Primary result

### Full sample

```text
closed trades = 650
wins / losses = 234 / 416
win rate = 36.00 %
aggregate realized unit PnL = -3653.772
expectancy per closed trade = -5.6211876923
realized max drawdown = 11107.239
LONG = 325 trades / +5944.401
SHORT = 325 trades / -9598.173
```

### PRE-OOS

```text
closed trades = 535
aggregate realized unit PnL = -5940.314
expectancy per closed trade = -11.1033906542
win rate = 34.9533 %
realized max drawdown = 8362.472
LONG = 268 trades / +637.517
SHORT = 267 trades / -6577.831
```

### Exposed / reproduced OOS

```text
closed trades = 114
aggregate realized unit PnL = +2856.668
expectancy per closed trade = +25.0584912281
win rate = 41.2281 %
realized max drawdown = 3471.246
LONG = 57 trades / +5306.884
SHORT = 57 trades / -2450.216
```

This OOS result is descriptive and non-confirmatory.

One CROSS_BOUNDARY SHORT trade has realized unit PnL -570.126 and is excluded from both PRE-OOS and OOS aggregates.

A LONG position remains open/unrealized at the end of the execution sequence. Reported PnL is realized closed-trade PnL, not terminal mark-to-market portfolio value.

## OBSERVED

### OBSERVED-01 — Full sample negative
650 trades; PnL -3653.772; expectancy -5.6211876923.

### OBSERVED-02 — PRE-OOS negative
535 trades; PnL -5940.314; expectancy -11.1033906542.

### OBSERVED-03 — Exposed OOS positive
114 trades; PnL +2856.668; expectancy +25.0584912281. Non-confirmatory because the OOS was already exposed.

### OBSERVED-04 — Expectancy sign reversal
PRE-OOS expectancy is negative while reproduced OOS expectancy is positive. Cause unknown.

### OBSERVED-05 — OOS performance concentration
Largest OOS winner = +3617.517 LONG. Removing that observation descriptively leaves the other 113 OOS trades at -760.849. OOS median closed trade is negative. This is descriptive only and does not authorize alteration or optimization.

### OBSERVED-06 — Temporal concentration
OOS exits in 2025: 75 trades / -1022.906. OOS exits in 2026: 39 trades / +3879.574. Positive OOS performance is not temporally uniform.

### OBSERVED-07 — Persistent SHORT drag
PRE-OOS SHORT = -6577.831. OOS SHORT = -2450.216. Cause unknown.

### OBSERVED-08 — LONG/SHORT asymmetry
PRE-OOS LONG = +637.517; OOS LONG = +5306.884, while SHORT is negative in both partitions. This does not establish that LONG-only is superior.

### OBSERVED-09 — Raw data consumption
All 212 Source-B files were rehashed before execution. During the demand-driven run, 375600973 raw rows were yielded and 211 files fully consumed. The final file did not need complete consumption after the last required transition.

## HYPOTHESIS — OPEN / UNCONFIRMED

```text
HYPOTHESIS-01 = REGIME DEPENDENCE
HYPOTHESIS-02 = TAIL DEPENDENCE
HYPOTHESIS-03 = DIRECTIONAL ASYMMETRY
HYPOTHESIS-04 = STRUCTURAL USTECH DIRECTIONAL BIAS
HYPOTHESIS-05 = PERIOD-SPECIFIC 2026 EFFECT
```

None is demonstrated by E1.

## UNKNOWN

```text
UNKNOWN-01 = cause of PRE-OOS → OOS expectancy sign reversal
UNKNOWN-02 = future persistence
UNKNOWN-03 = commission effect
UNKNOWN-04 = slippage effect
UNKNOWN-05 = financing effect
UNKNOWN-06 = terminal mark-to-market effect
UNKNOWN-07 = statistical stability of positive OOS aggregate
UNKNOWN-08 = behaviour on genuinely independent future period
UNKNOWN-09 = behaviour on independent instruments
UNKNOWN-10 = exact regime/volatility/direction/trend-amplitude attribution
UNKNOWN-11 = whether LONG/SHORT asymmetry is structural or sample-dependent
UNKNOWN-12 = whether tail dependence persists outside exposed data
```

## NOT_SUPPORTED

```text
STRATEGY_QUALIFIED
EDGE_CONFIRMED
ROBUST
CONFIRMATORY_RESULT
LONG_ONLY_IS_BETTER
SHORTS_SHOULD_BE_REMOVED
PARAMETERS_VALIDATED
REGIME_FILTER_VALIDATED
BROKER_NET_PNL
ALL_IN_COST_PROFITABILITY
LIVE_PROFITABILITY
FULL_BROKER_EXECUTION_REALISM
MT5_AUTHORIZED
PAPER_AUTHORIZED
BROKER_AUTHORIZED
LIVE_AUTHORIZED
CAPITAL_AUTHORIZED
DECISION_AUTHORITY
ACTION_AUTHORITY
```

## OOS contamination / reuse policy

The E1 OOS window is permanently exposed. It may support reproduction, debugging, mechanistic analysis, descriptive decomposition and hypothesis generation. It must never regain untouched-OOS or independent-confirmation status.

Any strategy change motivated by E1 creates a new hypothesis family or strategy candidate requiring independent evidence.

## FAILURE / LEARNING MEMORY

1. Windows worktree byte materialization can invalidate raw local-byte Git blob verification; canonical line-ending materialization must be controlled where raw-file verification is used.
2. Environment variables used in an environment descriptor require parity between qualification and execution. For E1: `PYTHONHASHSEED=0`, `TZ=UTC`.
3. A technically failed run may irreversibly expose OOS if performance computation occurred before persistence failure; exposure semantics cannot depend only on presence of RESULT.json.
4. Future evidence packaging should ideally include enough material to reconstruct the intermediate runner-record digest. This is an improvement candidate, not authorization to rerun E1.

## Durable interpretation

MOMENTUM_V1, under frozen E1 execution and cost assumptions, is negative over the complete evaluated sample and PRE-OOS. The already exposed and reproduced OOS partition is positive, but that positive aggregate is temporally concentrated, materially influenced by a small number of large winners, and predominantly supported by LONG performance while SHORT performance remains negative. E1 establishes heterogeneous behaviour across time and direction, but does not establish a durable trading edge, robustness, causal mechanism, broker-net profitability or production readiness.

## Closure

```text
E1_EXPERIMENTAL_MEMORY = ADOPTED_FOR_PERSISTENCE
E1_EVIDENCE_REVIEW = CLOSED
E1_EXPLORATORY_EXPERIMENT = CLOSED
STRATEGY_CHANGE = NOT_AUTHORIZED
NEW_BACKTEST = NOT_AUTHORIZED
NEXT_EXPERIMENT = NOT_AUTHORIZED
NEXT_DATASET = NOT_SELECTED
```
