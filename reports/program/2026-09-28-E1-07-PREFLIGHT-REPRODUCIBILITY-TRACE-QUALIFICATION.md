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

## 4. Minimal implementation candidate and persisted-HEAD qualification

Qualified candidate HEAD:

`ebdbfdf72993a55897374fd2127d162f72989adf`

Qualified candidate TREE:

`3b13e2954cf7c5d395a53dea453ae46630da5ef2`

Exact frozen identities:

```text
contract = b19f9b5a4505f50d77f1cbd09b2b6381241b5205
breaker = 40a02b99488039949dcde8483af01db7767f5075
preflight schema = 50630a8404f8c1c7c8283ba1f356b961980aecc9
result schema = f129797ec5eb229f70ca3293670bc13c542633e3
preflight/trace runtime = 88ca1f1ae89d1a2cfac1ae35becb3ea6209755f5
```

Exact-byte materialization:

`PASS — git hash-object matched both persisted breaker and persisted runtime blobs`

Execution:

```text
PY_COMPILE = PASS
Q7-01 → Q7-30
TOTAL = 30
PASS = 30
FAIL = 0
```

Qualified dimensions include:

- deterministic canonical preflight;
- exact repository / branch / HEAD / TREE / tool binding;
- E1-01 scope and strategy identity;
- E1-02 raw window and OOS split;
- raw Source-B identity and manifest digest;
- H1 identity and content digests;
- execution/cost-model identity and cost scope;
- E1-05 runner identity;
- E1-06 qualification identity;
- environment/dependency descriptor identity;
- result-envelope schema identity;
- substitution blocking;
- result-payload tamper detection;
- preflight-digest tamper detection;
- bound dataset/repository tamper detection;
- trace-digest tamper detection;
- unknown-field fail-closed behavior;
- absence of real-run delegation in the E1-07 runtime.

## 5. Qualification fixture trace evidence

The following values are from the **synthetic E1-07 qualification fixture only**. They are not a real E1 run and do not represent the actual future E1 execution environment.

```text
PREFLIGHT_VERIFY = PASS
PREFLIGHT_DIGEST =
9a9c16226f7364dbb02ccba00a38b46a64c291c97b89fe43c9caa530d4dc9c41

FIXTURE_ENVIRONMENT_IDENTITY =
613caa0abbba3314b3b84c0d368e1063228a8dceea482a6090a84631c056da6a

RESULT_VERIFY = PASS
RESULT_DIGEST =
f2144c380b700f5c3f28cdec15856d920b04d641e63eee561d27e0949bdbd35f

TRACE_DIGEST =
7832b145838fa2d3496070c152719bb9abd61529f4d1092aa0b5bd8b14a6d255
```

Adversarial spot checks:

```text
HEAD_SUBSTITUTION = BLOCKED
ENV_SUBSTITUTION = BLOCKED
PAYLOAD_TAMPER = BLOCKED
TRACE_TAMPER = BLOCKED
```

The canonical schema digests were independently recomputed before candidate persistence:

```text
E1_PREFLIGHT_MANIFEST_V0 =
dfef55de3b29f165d60fac5c814be4bd81d0c3674768a3775f4fc6c532e8a99d

E1_RESULT_ENVELOPE_SCHEMA_V0 =
d3da7e97b533ce1930e7d4c4ea7d9e5224a737bcef452db951b69c789d853f7c
```

## 6. Final adjudication

```text
E1_07_TEST_FIRST_RED = PASS_EXPECTED_FAILURE
E1_07_EXACT_PERSISTED_HEAD_REBREAK = PASS_30_OF_30
E1_07_REPRODUCIBILITY = PASS
E1_07_CANONICALIZATION = PASS
E1_07_SUBSTITUTION_TAMPER_CONTROLS = PASS
E1_07_TRACE_ENVELOPE = PASS

E1-07 = PASS
E1-08 = NOT_OPENED
E1_READINESS = NOT_READY
```

Authority remains:

```text
REAL_E1_RUN = NOT_AUTHORIZED
REAL_DATA_PERFORMANCE = NOT_AUTHORIZED
PROFITABILITY_INTERPRETATION = NOT_AUTHORIZED
MT5/PAPER/BROKER/LIVE/CAPITAL = CLOSED
```

Accelerated governed E1-07 control cycle:

`CLOSED — STOP AT END OF E1-07`
