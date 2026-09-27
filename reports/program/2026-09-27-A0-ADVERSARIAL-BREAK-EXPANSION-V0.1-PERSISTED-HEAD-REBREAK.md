# A0 — ADVERSARIAL BREAK EXPANSION V0.1 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`bc0d83ef757b0abbea21c2cea6fa3fc6a18dd920`

Candidate implementation blob:

`737f041b7b083f832f475b2aab607fb417c74fe0`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial expansion breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Workflow run:

`36324774812`

## Structural verification

PASS:

- exact governed break HEAD checkout;
- break persistence scope exact;
- candidate implementation unchanged;
- historical six-test breaker unchanged;
- adversarial expansion breaker exact;
- A0 V0.3 contract unchanged.

## Historical regression

`6/6 PASS`

The initial RED transition remains closed and unchanged.

## Persisted adversarial failure profile

Reproduced exactly:

```
TOTAL = 18
PASS  = 9
FAIL  = 9
```

The same nine attacks fail:

- AB03 bool sample size rejected-not-ignored;
- AB04 numeric-string sample size rejected-not-ignored;
- AB08 forged preregistration cannot hide REFUTED member;
- AB10 UNDETERMINED evidence level must contribute empty set;
- AB11 NOT_REPRESENTED promotion limit must contribute empty set;
- AB13 synthetic CONFIRMED cannot normalize to SUPPORTED;
- AB14 real but NOT_ESTABLISHED CONFIRMED cannot normalize to SUPPORTED;
- AB15 foreign normalization-policy identity must be rejected;
- AB16 co-forged registry/profile must not create new authority.

The same nine attacks pass:

- AB01;
- AB02;
- AB05;
- AB06;
- AB07;
- AB09;
- AB12;
- AB17;
- AB18.

## Material defect groups

The persisted failure profile confirms exactly six material correction groups:

```
A0-ABF-01
MEASUREMENT STRICT TYPING / EXTRACTION ABSENT

A0-ABF-02
EXPECTED-FAMILY AUTHORITY NOT PINNED

A0-ABF-03
D1 / MC2 FAIL-CLOSED PERMISSION OVERRIDES MISSING

A0-ABF-04
D3 CONFIRMED GUARD MISSING

A0-ABF-05
GLOBAL NORMALIZATION POLICY AUTHORITY NOT PINNED

A0-ABF-06
SOURCE PROFILE REGISTRY AUTHORITY NOT PINNED
```

No additional defect group is introduced by this re-break.

## Candidate status

`A0_MINIMAL_IMPLEMENTATION_CANDIDATE = FAIL_ADVERSARIAL_EXPANSION_V0_1`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = FAIL_NOT_CLOSED`

## Next governed action

Create one minimal correction candidate limited to A0-ABF-01 through A0-ABF-06.

The correction MUST:

- leave the historical six-test breaker unchanged;
- leave the 18-test adversarial breaker unchanged;
- preserve the governing A0 V0.3 contract;
- make no A1/A2/Decision/ACTION changes;
- introduce no real C01 access or scoring.

The correction candidate must then execute:

`6 historical + 18 adversarial = 24 tests`

before any persisted-head qualification may be considered.
