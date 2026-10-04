# P1-17 — SYNTHETIC IMPLEMENTATION READINESS DOSSIER V0.1

**Target boundary:** `P1.12C — CLAIM-SCOPED QUALIFIED PRODUCER EXECUTION V1`  
**Selected architecture:** `OPTION A — P1 INVOKES QUALIFIED PRODUCER`  
**Implementation status:** `NOT AUTHORIZED`

## 1. Readiness summary

```text
ARCHITECTURE =
SELECTED

FROZEN BREAKER DESIGN =
READY

GENERIC SYNTHETIC P1.12C IMPLEMENTATION =
READY FOR A SEPARATE TEST-FIRST AUTHORIZATION

EXACT AP1 SMALL-SYNTHETIC QUALIFICATION =
BLOCKED

EXACT AP1 REAL EXECUTION =
NOT AUTHORIZED

END-TO-END P1.13B COMPATIBILITY =
BLOCKED BY DOWNSTREAM TYPE CONTRACT
```

## 2. Why OPTION A was selected

A checksum-bound external result is integrity evidence, not execution authority.

The repository's existing P0.5 inter-process design already resolves this class of problem by deterministic replay. If OPTION B is made safe through replay, P1 must execute the exact producer anyway. OPTION B then becomes OPTION A plus an extra persistence layer.

Therefore OPTION A is the minimal primary execution architecture.

## 3. Why P1.12C is a sibling

P1.12B is semantically BI5-specific. Its result model includes decoded tick counts/timestamps and a BI5 stream hash.

Mapping AP1 output into those fields would change their meaning.

```text
P1.12B =
UNCHANGED

P1.12C =
NEW CLAIM-SCOPED PRODUCER EXECUTION BOUNDARY
```

## 4. Synthetic implementation path that is ready

A future separately authorized P1.12C implementation can use a dedicated **test-only synthetic producer** with:

- exact test producer code identity;
- exact synthetic input bytes;
- exact pre-result producer plan;
- exact runtime lock;
- isolated output;
- pre/post source hashes;
- deterministic output;
- content-addressed result identity;
- no network;
- no real market data;
- no AP1 semantics.

That synthetic producer can attack all generic P1.12C controls without duplicating AP1 logic.

This can qualify the **boundary mechanics** only.

## 5. Why exact AP1 cannot be qualified on a small synthetic fixture today

The exact AP1 helper hard-codes the real first-use surface:

```text
61 files
1,709,180 minute rows
376,003,618 source ticks
1,606 segments
exact AP0 manifest SHA-256
exact F2 spread reconciliation constants
```

A small synthetic fixture would fail by design.

Changing AP1 to parameterize those constants would modify the producer owner and is outside P1-17.

Constructing a huge synthetic corpus merely to satisfy those real-surface constants is not the minimal architecture and would not add meaningful assurance proportional to its complexity.

Therefore:

```text
P1.12C GENERIC SYNTHETIC QUALIFICATION =
FEASIBLE

P1.12C + EXACT AP1 SYNTHETIC QUALIFICATION =
BLOCKED_BY_PRODUCER_TESTABILITY
```

## 6. Runtime/dependency prerequisite

Exact AP1 execution depends materially on:

- CPython behavior;
- NumPy percentile implementation;
- PyArrow Parquet behavior;
- timezone database used by `zoneinfo`.

AP1 currently records NumPy/PyArrow versions in its output, but post-result observation is not a pre-execution lock.

A future exact AP1 execution plan must freeze these identities before result exposure.

## 7. Downstream P1 prerequisite

P1.13B currently accepts only exact currently-attested `LinkedExperimentExecutionResult` from P1.12B.

A distinct P1.12C result therefore cannot legally enter P1.13B today.

This is not solved by coercion.

A future separately authorized downstream design must select either:

```text
A. P1.13C producer-aware evaluation sibling

or

B. a common qualified-execution-result interface
   adopted by the relevant P1 downstream boundaries
```

P1-17 does not adjudicate that later downstream choice because neither is necessary to define the P1.12C execution boundary itself.

## 8. Implementation prerequisites frozen by P1-17

Before any exact AP1 execution:

1. executable P1-17 breakers must be materialized unchanged;
2. RED must be observed and persisted;
3. P1.12C generic synthetic implementation must pass;
4. producer runtime lock must be exact;
5. DATA-02 admission must be exact and current;
6. producer code blob must match the frozen plan;
7. source immutability must be proven pre/post invocation;
8. output identity/schema/status must pass;
9. no downstream finding may be created from P1.12C until a qualified P1 downstream boundary accepts its result type;
10. separate human authorization is required for any real AP1 execution.

## 9. STOP state

```text
P1-18 =
NOT AUTHORIZED

P1.12C IMPLEMENTATION =
NOT AUTHORIZED BY P1-17

P1 DOWNSTREAM MODIFICATION =
NOT AUTHORIZED

RVO-06 =
NOT AUTHORIZED

DATA-03 =
NOT AUTHORIZED

REAL AP1 =
NOT AUTHORIZED

NEW MARKET RESULT =
NONE

BACKTEST =
NONE

OOS =
NONE

TRADING / CAPITAL =
NONE
```
