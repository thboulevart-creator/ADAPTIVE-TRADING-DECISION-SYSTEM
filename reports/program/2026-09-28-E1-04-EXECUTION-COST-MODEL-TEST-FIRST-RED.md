# E1-04 — EXECUTION / COST MODEL — TEST-FIRST RED PREREGISTRATION

Date: 2026-09-28

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
Branch: `integration/system-v1`

Pre-persistence HEAD:

`6763453795c1cc08744de407f800fa6785246f94`

Pre-persistence TREE:

`4655bb3445d4b6c408342f17ba0691d9049ab718`

## 1. Scope

This artifact preregisters the executable E1-04 boundary before any E1-04 runtime exists.

The boundary is limited to the already human-adopted execution/cost semantics.

It does not implement Momentum, compute PnL, create E1-05, run a backtest or authorize paper/broker/live/capital activity.

## 2. Persisted test-first artifacts

Machine-readable contract:

`GOVERNANCE/E1-04-EXECUTION-COST-MODEL-CONTRACT-V0.1.json`

Independent breaker:

`breakers/e1_04_execution_cost_model_red_breaker.py`

Future runtime target:

`tools/e1_04_execution_cost_model.py`

At this preregistration point that runtime target must remain absent.

## 3. Frozen executable semantics

The test surface covers:

- H1 MID as signal source only, never execution price;
- same-H1 execution forbidden;
- search from the exact end of signal H1 t;
- first admissible RAW Source-B tick;
- exact BID/ASK side for all six position-changing transitions;
- HOLD semantics;
- no pyramiding;
- no forward fill;
- no last-price carry;
- no MID substitution;
- no silent traversal of a forbidden continuity boundary;
- no admissible execution price => NOT_EXECUTED;
- observed spread intrinsically included through RAW BID/ASK;
- commission/slippage/financing excluded but not assumed zero;
- forbidden execution-model claims.

## 4. Test inventory

Exactly 22 cases are preregistered:

`E4-01 → E4-22`

The test file must not be altered after first RED merely to accommodate an implementation candidate.

## 5. Authority state

```text
E1_04_TEST_FIRST_CONTRACT = PERSISTED_CANDIDATE
E1_04_RUNTIME = ABSENT
E1_04_IMPLEMENTATION_AUTHORIZED = FALSE
E1_05_AUTHORIZED = FALSE
PNL_AUTHORIZED = FALSE
E1_RUN_AUTHORIZED = FALSE
```

The first execution after persistence is expected to produce an interpretable RED caused by:

`E1_04_RUNTIME_ABSENT_EXPECTED_RED`

At persistence time:

```text
E4_01_TO_E4_22_EXECUTION = NOT_YET
```

No implementation correction is authorized by this artifact.
