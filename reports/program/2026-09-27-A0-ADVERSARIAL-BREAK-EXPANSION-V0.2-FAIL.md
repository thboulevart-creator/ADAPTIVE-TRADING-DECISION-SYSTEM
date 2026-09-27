# A0 — ADVERSARIAL BREAK EXPANSION V0.2 — FAIL

Date: 2026-09-27

Governed base HEAD:

`a493c4824775b63480b5fe3c07220c9df271fb1b`

Target implementation blob:

`c7c1f37d9d306e0424274b276d42ab422beac560`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial breaker V0.1 blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Sandbox workflow run:

`36326986380`

## Scope

V0.2 adds 18 contract-derived attacks without modifying the historical six tests, the 18 V0.1 tests, the runtime candidate, or the A0 V0.3 contract.

The new coverage targets:

- mandatory carrier representation and source-native extraction;
- critical-control precedence and four-state control authority;
- native-status conflict handling;
- source supersession;
- measurement/fold/applicability/lineage preservation;
- exact registry/profile/policy content authority;
- post-observation authority widening;
- exact six-dimension permission closure;
- operational-semantic exclusion from the A0 permission universe;
- semantic caller-field confinement.

## Preserved closed suite

Historical + V0.1:

`24/24 PASS`

No regression was introduced in the existing closed suite.

## V0.2 result

```
TOTAL = 18
PASS  = 4
FAIL  = 14
```

Passing attacks:

- AC05 — downstream status redeclaration cannot replace native status;
- AC07 — NOT_INTERPRETABLE strong metric remains non-positive;
- AC08 — REFUTED strong metric remains non-positive;
- AC18 — caller Decision/ACTION/BUY/knowledge fields create no A0 authority.

Failing attacks:

- AC01 — mandatory governed carrier properties not represented;
- AC02 — critical EVIDENCED_FAIL can be rescued/ignored;
- AC03 — four-state caller-asserted control not preserved;
- AC04 — unresolved native-status conflict accepted;
- AC06 — explicitly superseded source accepted;
- AC09 — measurement identity/reference not preserved;
- AC10 — governed fold roles not represented;
- AC11 — applicability domain not preserved;
- AC12 — lineage/shared-corpus identity not preserved;
- AC13 — same-version registry content mutation accepted;
- AC14 — post-observation profile permission widening accepted;
- AC15 — same-schema normalization-policy mapping mutation accepted;
- AC16 — seventh permission dimension accepted/ignored;
- AC17 — operational token BUY admitted to the permission universe.

## Consolidated material defect groups

```
A0-ABF2-01
MANDATORY CARRIER / EXTRACTION REPRESENTATION ABSENT
(AC01, AC09, AC10, AC11, AC12)

A0-ABF2-02
CONTROL-STATE AUTHORITY / CRITICAL PRECEDENCE ABSENT
(AC02, AC03)

A0-ABF2-03
NATIVE-STATUS CONFLICT FAIL-CLOSED RULE ABSENT
(AC04)

A0-ABF2-04
SOURCE SUPERSESSION ENFORCEMENT ABSENT
(AC06)

A0-ABF2-05
SOURCE PROFILE REGISTRY EXACT-CONTENT AUTHORITY NOT PINNED
(AC13)

A0-ABF2-06
POST-OBSERVATION PROFILE WIDENING NOT BLOCKED
(AC14)

A0-ABF2-07
GLOBAL NORMALIZATION POLICY EXACT-CONTENT AUTHORITY NOT PINNED
(AC15)

A0-ABF2-08
EXACT SIX-DIMENSION PERMISSION SCHEMA NOT ENFORCED
(AC16)

A0-ABF2-09
A0 PERMISSION UNIVERSE OPERATIONAL-SEMANTIC GUARD ABSENT
(AC17)
```

## Verdict

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_2 = BREAK_CONFIRMED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_2`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed action

Persist this exact V0.2 breaker and failure profile, then reproduce the same:

- existing suite = 24/24 PASS;
- V0.2 = 4 PASS / 14 FAIL;
- exact failed set = AC01, AC02, AC03, AC04, AC06, AC09, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17;

from the persisted governed HEAD before any correction implementation.
