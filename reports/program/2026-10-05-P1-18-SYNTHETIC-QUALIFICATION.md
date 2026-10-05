# P1-18 — P1.12C TEST-FIRST SYNTHETIC QUALIFICATION

**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Boundary:** `P1.12C — CLAIM-SCOPED QUALIFIED PRODUCER EXECUTION V1`  
**Status before final persisted-head rebreak:** `QUALIFICATION_CANDIDATE`

## 1. Fresh preflight and parent reconciliation

The authorization expected:

```text
HEAD =
761cb696ea9e58f437efb320f96e8adb574e38e4

TREE =
94040f1b04cbf7b5e170ff936d5b9ffe6a7268d3
```

Fresh preflight found a three-commit descendant:

```text
HEAD =
07a54720284acbfd0a94a727ebd58468d26a1e06

TREE =
eda1b8e995182c0d6e63ac0bdd5c98efdbb8e3d6
```

The delta contained only AO-E0 EXEC-02 cost/platform evidence artifacts. Every exact P1-17, P1.10B, P1.11B, P1.12B, DATA-02, Research Execution and Research Engine identity required by P1-18 was re-fetched and remained unchanged.

The drift was therefore persisted as:

```text
NON_MATERIAL_TO_P1_18
```

rather than ignored.

## 2. Test-first RED

The P1-17 documentary breaker contract remained byte-identical:

```text
P1_17_FROZEN_BREAKER_CONTRACT =
9ab0f9018dd6e9def4a5e35b8e9a35c3beb556bc
```

The executable breaker materialized all 32 frozen cases before P1.12C existed:

```text
EXECUTABLE_BREAKER =
7f40b525e16ca06306cba3ae59f03cb08c71d0cd
```

Observed pre-implementation RED:

```text
COMMIT =
644f22d6785aa0373f39d1a4715b28b05ceee2f4

WORKFLOW RUN =
37293347906

JOB =
111708717662

RESULT =
32 failed

MARKER =
P1_12C_RUNTIME_ABSENT_EXPECTED_RED
```

No frozen case ID, attack intent or expected fail-closed reason was modified after observing RED.

## 3. Minimal P1.12C implementation

The implementation adds a new sibling boundary only:

```text
P1.12B =
UNCHANGED

P1.12C =
NEW SIBLING BOUNDARY
```

Exact runtime:

```text
src/p1_12c_qualified_producer_execution.py

BLOB =
6d634ed1adab21ce31a55289d8d6e5b288e70005
```

Support runner:

```text
tools/p1_12c_sandbox_runner.py

BLOB =
08fbd6f4b2cd4db9cb714f583c1459d0753a9112
```

The boundary creates two process-local factory-attested P1 types:

```text
QualifiedProducerExecutionPlan
QualifiedProducerExecutionResult
```

It does not create evaluations, findings, scientific authority, trading authority or capital authority.

## 4. Synthetic producer

The test-only producer is:

```text
PRODUCER_ID =
ATDS_P1_18_SYNTHETIC_PRODUCER_V0_1

CODE BLOB =
06d48e6253e6f94cb3eebf3aa53f3fd96a5ad7b0

OUTPUT SCHEMA =
ATDS_P1_18_SYNTHETIC_PRODUCER_OUTPUT_V0_1
```

Its only positive behavior is a deterministic byte inventory over the synthetic DATA-02 fixture.

It contains:

```text
MARKET SEMANTICS =
NONE

AP1 LOGIC =
NONE

PNL =
NONE

SIGNALS =
NONE

OOS =
NONE
```

Special negative modes exist only to exercise fail-closed behavior for source mutation, network attempts, child-process attempts and invalid output status.

## 5. Pre-result producer plan

Before producer execution P1.12C binds:

- exact P1.11B execution-input identity;
- execution-binding / experiment-spec / request / revision / audit / scope IDs;
- exact DATA-02 admission digest;
- claim scope and dataset identity;
- exact producer Git blob;
- exact producer semantic-parameter digest;
- exact invocation-contract digest;
- exact runtime-lock digest;
- exact expected output schema/status/contract;
- exact output-size ceiling.

Transport paths are stored for execution but explicitly excluded from the producer-plan identity.

A positive test places byte-identical producer code at two different paths and obtains the same plan digest and plan ID.

Therefore:

```text
PATH != IDENTITY
```

is executable behavior, not merely documentation.

## 6. Runtime lock

The successful qualification environment bound before result exposure:

```text
RUNTIME_LOCK_DIGEST =
9040a208046cd59e559d136d06db8cceffe9310b9309f0db042ff55b45000bf9

PYTHON =
3.12.14

PYTHON_EXECUTABLE_SHA256 =
bef88f140b625959f8af25c7b75cce2cd5d4b29cc2f2b079befd7f68eda4dba0

MATERIAL THIRD-PARTY DEPENDENCIES =
NONE

TIMEZONE DATABASE =
NOT_USED_BY_SYNTHETIC_PRODUCER
```

The synthetic producer is stdlib-only. NumPy, PyArrow and timezone data are therefore not silently inserted into this qualification envelope.

That does **not** qualify the future AP1 runtime lock.

## 7. Controlled producer invocation

P1.12C invokes only the bound Python-file protocol using a structured argument list and:

```text
shell =
false
```

The subprocess receives an explicitly bounded environment and an isolated output location.

A dedicated sandbox runner installs a Python audit hook that blocks:

- socket operations;
- nested subprocess creation;
- exec/spawn/fork operations;
- ctypes dynamic-loading escape paths.

The positive suite explicitly attempts both a socket creation and a child-process creation. Both are blocked and no qualified P1.12C result is minted.

This is the qualified synthetic boundary behavior; it is not a claim of universal OS sandboxing against arbitrary native code.

## 8. Source immutability

Immediately before execution P1.12C recomputes the exact P1 source inventory hash.

Immediately after producer termination it recomputes it again.

Positive execution requires:

```text
PRE_SOURCE_IDENTITY
==
POST_SOURCE_IDENTITY
```

A special synthetic attack producer actually modifies one fixture source file.

Observed behavior:

```text
BLOCKED_SOURCE_MUTATION_DURING_PRODUCER_EXECUTION
```

No result is minted.

## 9. Output and Data binding

A qualified result requires:

- process return code 0;
- exact canonical UTF-8 JSON bytes;
- exact output schema;
- exact expected status;
- exact producer ID;
- exact source inventory identity;
- exact producer parameter digest;
- output within the frozen byte ceiling;
- exact output SHA-256;
- successful DATA-02 `validate_result_binding`.

The output path and filename do not participate in result authority.

The final P1 result ID is content-bound and deterministic:

```text
QPER-...
```

Two executions of the same exact plan, source, producer, parameters and runtime lock produced the same:

- P1.12C result ID;
- output SHA-256;
- reconstruction descriptor digest;
- stdout digest;
- stderr digest.

## 10. Reconstructibility scope

P1-18 demonstrates deterministic re-execution for the exact synthetic surface.

It records:

```text
RECONSTRUCTION CLASS =
EVIDENCE_REPLAY
```

but does **not** implement a persisted cross-process re-attestation proof for P1.12C.

Therefore:

```text
DETERMINISTIC RE-EXECUTION =
QUALIFIED WITHIN SYNTHETIC SURFACE

PERSISTED DURABLE REPLAY PROOF =
NOT IMPLEMENTED

DURABLE CROSS-PROCESS RE-ATTESTATION =
UNRESOLVED FUTURE CAPABILITY

RUNTIME ATTESTATION
!=
DURABLE RECONSTRUCTION
```

No stronger claim is made.

## 11. Downstream firewall

P1.13B remains unchanged and still requires exact `LinkedExperimentExecutionResult` from P1.12B.

P1-18 explicitly creates a valid P1.12C result and attempts to present it to P1.13B.

Observed result:

```text
P1.12C RESULT
→ P1.13B
=
BLOCKED_BY_EXISTING_DOWNSTREAM_CONTRACT
```

This BLOCKED state is expected and does not invalidate P1.12C itself.

No P1.14B, P1.15B or P1.16 object is created from the P1.12C result.

## 12. Qualification run

Successful pre-persistence qualification:

```text
COMMIT =
151520efcad14430e3c4c5597b4ed4d2db77ce89

TREE =
2766af8439be51790942687035da690a93558fc5

WORKFLOW RUN =
37294383240

JOB =
111712043318

CONCLUSION =
SUCCESS
```

Observed:

```text
FROZEN P1-17 BREAKERS =
32 passed

P1-18 POSITIVE / FAIL-CLOSED SYNTHETIC TESTS =
16 passed

P1.10B → P1.16 PROTECTED REGRESSIONS =
229 passed

DATA-02 PROTECTED REGRESSION =
32 passed

P0.4 PRODUCER-JUNCTION REGRESSION =
16 passed

P0.5 INTERPROCESS REGRESSION =
15 passed

P1-18 DELTA =
PASS — STRICTLY BOUNDED

AP1 EXECUTION =
NOT EXECUTED
```

## 13. Existing P0.4 / P0.6 workflow observations

The implementation commit also triggered older repository-level P0.4 and P0.6 workflows.

Those workflows first confirmed their immutable historical closure evidence, then failed on the already-existing BERD02 body-file expectation:

```text
evidence/berd02/gha_run_35533153289/bodies/*.bi5
```

This is recorded rather than hidden.

The direct P0.4 and P0.5 protected regression suites executed inside the P1-18 qualification both passed. No P1-18 mutation of those owners or of the historical BERD02 evidence was performed.

## 14. Success semantics

Subject to the final persisted-head rebreak, P1-18 may conclude only:

```text
P1_12C_GENERIC_SYNTHETIC_EXECUTION_BOUNDARY =
QUALIFIED
```

It does not conclude:

```text
AP1 =
QUALIFIED

FIRST_REAL_CC02 =
READY

P1_FINDING_CHAIN =
READY

STRATEGY =
VALIDATED

TRADING =
AUTHORIZED
```

## 15. Authority and STOP

```text
REAL AP0 EXECUTION =
NONE

REAL AP1 EXECUTION =
NONE

NEW MARKET RESULT =
NONE

BACKTEST =
NONE

OOS =
NONE

P1.13B MODIFICATION =
NONE

SCIENTIFIC AUTHORITY =
NONE

OPERATIONAL AUTHORITY =
NONE

TRADING AUTHORITY =
NONE

CAPITAL AUTHORITY =
NONE

UNKNOWN_UNKNOWN_COVERAGE =
NOT_CLAIMED

P1-19 =
NOT_AUTHORIZED

RVO-06 =
NOT_AUTHORIZED

DATA-03 =
NOT_AUTHORIZED
```

The next action is only to persist this qualification evidence and rebreak the exact persisted HEAD.
