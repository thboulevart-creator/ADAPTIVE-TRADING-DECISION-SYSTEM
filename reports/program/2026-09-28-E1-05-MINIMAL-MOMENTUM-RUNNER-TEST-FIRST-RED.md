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

## 5. Observed persisted-head RED

The exact persisted E1-05 breaker was executed after preregistration against the exact persisted contract, with the E1-05 runtime target still absent.

Observed source identities:

```text
HEAD =
a9b28cad2461abf820c1d1b283274343a6627792

TREE =
92fcd23adc8c4f492c7a1b84afaea31e807924d9

E1-05 contract blob =
51dc1152808ec9e841924976eac572cc4ec2ff93

E1-05 breaker blob =
4308e3360f3cd834e863eb740a2eb7f087e242c0
```

Observed compile result:

```text
PY_COMPILE = PASS
```

Observed breaker result:

```text
M5-01 → M5-33

TOTAL = 33
PASS = 0
FAIL = 33
```

All 33 failures shared exactly one preregistered cause:

`E1_05_RUNTIME_ABSENT_EXPECTED_RED`

No alternate failure family was observed.

Observed runtime state:

```text
tools/e1_05_minimal_momentum_runner.py = ABSENT
```

Adjudication:

```text
E1_05_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_05_RUNTIME = ABSENT
E1_05_IMPLEMENTATION = NOT_AUTHORIZED
E1_05 = BLOCKED
```

This RED proves the E1-05 test-first surface exists before implementation.

It does not establish that any future runner implementation is correct.

No real Momentum run, PnL, performance calculation, backtest, E1-06, E1-07, E1-08, MT5, paper, broker, live or capital authority was opened.

## 6. Next governed boundary

Subject to fresh persisted-head verification, the next candidate boundary is:

`E1-05 — MINIMAL IMPLEMENTATION CANDIDATE`

That boundary requires separate explicit human authorization.

Any future candidate must preserve the persisted E1-05 contract and breaker unchanged and may implement only the minimum runtime surface required by the preregistered 33 cases.

