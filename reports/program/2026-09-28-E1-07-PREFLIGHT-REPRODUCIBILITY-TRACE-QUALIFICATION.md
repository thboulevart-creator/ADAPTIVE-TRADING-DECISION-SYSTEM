# E1-07 — EXACT PREFLIGHT + REPRODUCIBILITY + TRACE

Date: 2026-09-28

Base HEAD:
`c658f769dcf5e6b7e44ef455290f65fe21ef69e6`

Base TREE:
`a26711112ad132ba7ac5c11ebeac7c19900ef308`

## 1. Human authority

E1-07 is authorized under accelerated governed mode for construction and qualification only.

Real E1 execution, E1-08, real-data performance interpretation, MT5, paper, broker, live and capital remain closed.

## 2. Frozen preregistration

Contract:
`GOVERNANCE/E1-07-EXACT-PREFLIGHT-REPRODUCIBILITY-TRACE-CONTRACT-V0.1.json`

Preflight schema:
`GOVERNANCE/E1-07-PREFLIGHT-MANIFEST-SCHEMA-V0.1.json`

Result envelope schema:
`GOVERNANCE/E1-07-RESULT-ENVELOPE-SCHEMA-V0.1.json`

Breaker:
`breakers/e1_07_preflight_reproducibility_trace_red_breaker.py`

Future target:
`tools/e1_07_preflight_trace.py`

Frozen tests:
`Q7-01 → Q7-30`

Expected initial execution:
`RED — E1_07_TARGET_ABSENT_EXPECTED_RED`

No PASS is claimed at preregistration.

## 3. Test-first RED — observed

Persisted HEAD under test:
`b5bc2b5147620a296c808160bfcf9f4876d29619`

Persisted TREE under test:
`47df68d512419b6ef9ef45a99f236926df128a1a`

Exact breaker blob:
`40a02b99488039949dcde8483af01db7767f5075`

Exact-byte local materialization:
`PASS — git hash-object matched persisted breaker blob`

Execution:

```text
PY_COMPILE = PASS
Q7-01 → Q7-30
TOTAL = 30
PASS = 0
FAIL = 30
UNIQUE_FAILURE = E1_07_TARGET_ABSENT_EXPECTED_RED
```

Adjudication:

```text
E1_07_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_07_TARGET = ABSENT
E1_07_IMPLEMENTATION_CANDIDATE = NOT_YET
E1_07 = OPEN_IN_PROGRESS
```

No real E1 run, E1-08, real-data performance interpretation, MT5, paper, broker, live or capital authority is created.
