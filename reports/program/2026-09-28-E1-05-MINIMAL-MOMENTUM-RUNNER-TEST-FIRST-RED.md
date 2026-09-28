# E1-05 — MINIMAL MOMENTUM RUNNER — TEST-FIRST RED PREREGISTRATION

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Pre-persistence HEAD:

`f99270487c69d016c6f5933eb4d84875f96053c3`

Pre-persistence TREE:

`2d095d5a6bfee499425eb910e8fa206c2009a2f9`

## 1. Scope

This artifact preregisters E1-05 before any E1-05 runtime exists.

E1-05 is limited to deterministic orchestration of the already-qualified E1-01 through E1-04 boundaries:

```text
E1-01 Momentum V1 semantics
→ E1-02 frozen temporal split
→ E1-03 admissible gap-aware H1 identity
→ E1-04 RAW BID/ASK execution semantics
→ E1-05 minimal runner
```

No real E1 run, PnL, performance calculation, E1-06, E1-07, E1-08, MT5, paper, broker, live or capital authority is opened.

## 2. Persisted test-first artifacts

Machine-readable contract:

`GOVERNANCE/E1-05-MINIMAL-MOMENTUM-RUNNER-CONTRACT-V0.1.json`

Independent breaker:

`breakers/e1_05_minimal_momentum_runner_red_breaker.py`

Future runtime target:

`tools/e1_05_minimal_momentum_runner.py`

At preregistration time that runtime target must remain absent.

## 3. Preregistered executable surface

Exactly 33 synthetic cases are preregistered:

`M5-01 → M5-33`

The surface covers:

- exact Momentum V1 formula and LONG/SHORT/NEUTRAL/UNDEFINED mapping;
- exact 20-H1 same-continuity lookback;
- warmup reset across continuity rupture;
- no artificial reset at the frozen OOS boundary;
- no lookahead;
- post-H1 execution timing;
- strict delegation to qualified E1-04 HOLD/EXECUTED/NOT_EXECUTED semantics;
- target exposure bounded to -1/0/+1;
- deterministic repeatability;
- E1-03 identity fail-closed;
- E1-04 runtime identity/surface fail-closed;
- duplicate/order/continuity/non-finite/missing-field fail-closed;
- explicit prohibition of optimization, regime, discretion, pyramiding, SL/TP/trailing/BE and sizing optimization;
- no runner-level execution-cost extension;
- no PnL/performance outputs;
- forbidden claims bounded;
- minimal deterministic per-H1 trace.

## 4. Test-first authority

```text
E1_05_TEST_FIRST_CONTRACT = PERSISTED_CANDIDATE
E1_05_RUNTIME = ABSENT
E1_05_IMPLEMENTATION_AUTHORIZED = FALSE
REAL_E1_RUN_AUTHORIZED = FALSE
PNL_AUTHORIZED = FALSE
E1_06_07_08_AUTHORIZED = FALSE
```

The first persisted-head execution is expected to fail only because:

`E1_05_RUNTIME_ABSENT_EXPECTED_RED`

At persistence time:

```text
M5_01_TO_M5_33_EXECUTION = NOT_YET
```

No implementation correction is authorized by this artifact.
