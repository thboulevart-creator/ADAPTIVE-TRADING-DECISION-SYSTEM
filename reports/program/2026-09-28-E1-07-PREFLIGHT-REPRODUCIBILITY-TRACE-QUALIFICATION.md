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
