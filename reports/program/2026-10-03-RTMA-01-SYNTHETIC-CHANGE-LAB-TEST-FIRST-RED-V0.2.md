# RTMA-01 — SYNTHETIC CHANGE LAB — TEST-FIRST RED V0.2

**Date:** 2026-10-03  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`

## 1. Boundary

This artifact records only the human-authorized preregistration and expected test-first RED for:

`RTMA-01 — SYNTHETIC CHANGE LAB V0.2`

The authorized block is:

```text
PREREGISTRATION PERSISTENCE
+ FROZEN TEST-FIRST BREAKER
+ EXPECTED RED EXECUTION
+ RED EVIDENCE PERSISTENCE
+ STOP
```

No synthetic-lab runtime implementation, GREEN qualification, detector benchmark, RTMA-02 execution, real-market-data access, news/event retrieval, backtest, PnL, production integration, decision authority or adaptation authority is authorized by this evidence.

## 2. Human-authorized base

```text
AUTHORIZED_PARENT_HEAD =
caad9412a3cfb3301d8255e1dee4e615bd379101

AUTHORIZED_PARENT_TREE =
ee70fe09f77aaa5ab2cc298a372a2c760be5ab47
```

## 3. Persisted preregistration identity

```text
PREREGISTRATION_COMMIT =
456162f636edaa96faaacea14dbb234f506573a2

PREREGISTRATION_TREE =
de6310ce4310eb3567d1228e74dd4fb90234f296

CONTRACT =
GOVERNANCE/RTMA-01-SYNTHETIC-CHANGE-LAB-CONTRACT-V0.2.json

CONTRACT_BLOB =
b0a2d00bd51ec99e34601f8404d6cca8a8d28a67

BREAKER =
breakers/rtma_01_synthetic_change_lab_red_breaker_v0_2.py

BREAKER_BLOB =
e62c2011e39e7fe46790de325113d137cec8a885

RUNTIME_TARGET =
tools/rtma_01_synthetic_change_lab.py
```

The contract and breaker were persisted atomically in the preregistration commit before any runtime implementation.

## 4. Runtime precondition

Before RED execution:

```text
TARGET_EXISTS =
FALSE
```

The runtime target returned no repository file and was also absent in the isolated detached worktree.

## 5. Execution environment

```text
Python =
3.13.14

pytest =
9.1.1

execution =
isolated detached git worktree

worktree HEAD =
456162f636edaa96faaacea14dbb234f506573a2

worktree TREE =
de6310ce4310eb3567d1228e74dd4fb90234f296
```

A preliminary shell command used only to inspect the tree was aborted before pytest because PowerShell misparsed the literal Git expression `HEAD^{tree}`. It produced no breaker result and made no repository change. The RED execution was then rerun with the tree obtained via `git show -s --format=%T HEAD`.

## 6. RED result

```text
PREREGISTERED_NODES =
63

PASS =
0

FAIL =
63

UNIQUE_EXPECTED_FAILURE =
RTMA_01_RUNTIME_ABSENT_EXPECTED_RED

PYTEST_EXECUTION_TIME =
0.33 s
```

All 63 preregistered nodes reached the same expected runtime-absence failure.

No unexpected syntax, collection, contract-parse, namespace, case-registry or other semantic failure occurred before the intended RED condition.

Therefore:

```text
RTMA_01_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE
```

## 7. Frozen breaker surface

The persisted breaker freezes the design families adopted for RTMA-01 V0.2, including:

```text
exact RTMA runtime / generator identities
task-class separation
online / retrospective / memory / edge lanes
SYN-00 through SYN-22 case-family registry
deterministic generation
seed / semantic separation
opaque detector-visible run identity
ground-truth invisibility
online prefix-only access
retrospective status separation
raw score != alert
explicit decision-adapter identity
input-view identity
case-family truth semantics
novelty relative to reference memory
no self-match
no future-memory use
one truth event <= one primary alert match
duplicate / false-alert / miss retention
deterministic overlapping-event assignment
drift interval geometry
mechanical scorer control fixtures
future-leakage protection
truth / observation seal integrity
deterministic scoring replay
development / holdout separation
A0 synthetic namespace isolation
existing ExperimentSpecification preservation
mechanical scorer != scientific evaluator authority
absence of operational / real-data / adaptation surfaces
```

The breaker is now frozen for a later implementation qualification unless a separately governed RTMA-01 version is created.

## 8. Explicit non-actions

```text
RTMA_01_RUNTIME_IMPLEMENTATION =
NOT_STARTED

RTMA_01_SYNTHETIC_GREEN =
NOT_RUN

RTMA_02 =
NOT_OPEN

DETECTOR_SELECTION =
NOT_PERFORMED

REAL_MARKET_DATA =
NOT_ACCESSED

REAL_HISTORICAL_MARKET_MINING =
NOT_PERFORMED

EVENT_OR_NEWS_RETRIEVAL =
NOT_PERFORMED

STRATEGY_BACKTEST =
NOT_RUN

PNL =
NOT_COMPUTED

PRODUCTION_INTEGRATION =
NOT_PERFORMED

DECISION_AUTHORITY =
NONE

ADAPTATION_AUTHORITY =
NONE
```

## 9. Terminal state

```text
RTMA_01_V0_2_DESIGN =
HUMAN_ADOPTED

RTMA_01_PREREGISTRATION =
PERSISTED

RTMA_01_BREAKER =
PERSISTED_AND_FROZEN

RTMA_01_TEST_FIRST_RED =
PASS_EXPECTED_FAILURE

NEXT_POSSIBLE_FRONTIER =
MINIMAL SYNTHETIC LAB RUNTIME IMPLEMENTATION
+ FROZEN BREAKER REPLAY
+ SYNTHETIC GREEN QUALIFICATION

NEXT_FRONTIER_AUTHORIZED =
FALSE

STOP =
TRUE
```

A separate human authorization is required before implementing `tools/rtma_01_synthetic_change_lab.py`.
