# A0 — ADVERSARIAL BREAK EXPANSION V0.1 — FAIL

Date: 2026-09-27

Governed base HEAD:

`884b7af4f068bcf9162362b15a81414744da5485`

Target candidate implementation blob:

`737f041b7b083f832f475b2aab607fb417c74fe0`

Governing contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Historical six-test breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial expansion breaker:

`breakers/a0_research_authority_adversarial_breaker_v01.py`

Breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Sandbox workflow run:

`36324627870`

## Scope

This phase expands the adversarial surface without modifying the historical six tests.

The expansion contains exactly 18 contract-derived attacks across:

- strict parsing / coercion;
- completeness / cherry-picking;
- missing / unknown permission authorities;
- epistemic laundering;
- native-status / authority binding;
- canonical reconstruction / tampering.

No A1/A2/Decision/ACTION scope is introduced.

## Historical regression

The unchanged initial RED suite remains:

`6/6 PASS`

Therefore the new failures are not regressions of the already-closed initial RED transition.

## Adversarial result

```
TOTAL = 18
PASS  = 9
FAIL  = 9
```

Candidate verdict:

`FAIL`

Break status:

`A0_ADVERSARIAL_BREAK_EXPANSION = BREAK_CONFIRMED`

## Passing attacks

The candidate resisted:

- AB01 duplicate JSON key;
- AB02 non-finite JSON number;
- AB05 missing expected finding;
- AB06 foreign finding;
- AB07 duplicate finding;
- AB09 unknown permission token;
- AB12 missing permission dimension → empty effective set;
- AB17 deterministic derivation;
- AB18 foreign inputs cannot verify an existing projection.

These PASS results are local to these attacks and do not establish full qualification.

## Failing attacks

### AB03 — BOOL SAMPLE SIZE IGNORED

A finding carrying:

`measurement.sample_size = true`

was accepted instead of rejected.

Finding:

`MEASUREMENT_STRICT_TYPING_NOT_ENFORCED`

### AB04 — NUMERIC-STRING SAMPLE SIZE IGNORED

A finding carrying:

`measurement.sample_size = "100"`

was accepted instead of rejected.

Finding:

`MEASUREMENT_NUMERIC_COERCION_BOUNDARY_NOT_ENFORCED`

AB03 and AB04 jointly show that the current candidate ignores measurement semantics rather than validating the strict numeric boundary required by contract §§31–32.

### AB08 — FORGED PREREGISTRATION CAN HIDE REFUTED MEMBER

The source was reduced from H1/H2/H3 to H1/H3 while the supplied preregistration was changed consistently to the same reduced family.

The candidate accepted the pair.

Finding:

`EXPECTED_FAMILY_AUTHORITY_NOT_PINNED`

The current completeness check is internally coherent but accepts a caller-substituted expected-family authority.

### AB10 — UNDETERMINED EVIDENCE LEVEL CAN RECEIVE POSITIVE PERMISSION

The governed evidence level was removed.

The policy then assigned:

`UNDETERMINED → HYPOTHESIS_INPUT`

The candidate emitted:

`{"HYPOTHESIS_INPUT"}`

instead of the contract-required empty set.

Finding:

`D1_UNDETERMINED_PERMISSION_FAILS_OPEN`

### AB11 — NOT_REPRESENTED PROMOTION LIMIT CAN RECEIVE POSITIVE PERMISSION

The source promotion limit was removed.

The policy then assigned:

`NOT_REPRESENTED → HYPOTHESIS_INPUT`

The candidate emitted a positive permission instead of the contract-required empty set.

Finding:

`MC2_NOT_REPRESENTED_PROMOTION_LIMIT_FAILS_OPEN`

### AB13 — SYNTHETIC CONFIRMED LAUNDERED TO SUPPORTED

With:

- `raw_status = CONFIRMED`;
- `data_class = SYNTHETIC_ONLY`;
- `confirmatory_claim_status = NOT_CONFIRMATORY`;

the supplied normalization map produced:

`SUPPORTED`

instead of:

`NO_SCIENTIFIC_CLAIM`

Finding:

`D3_SYNTHETIC_CONFIRMED_LAUNDERING`

### AB14 — REAL BUT NOT-ESTABLISHED CONFIRMED LAUNDERED TO SUPPORTED

With:

- `raw_status = CONFIRMED`;
- `data_class = REAL`;
- `confirmatory_claim_status = NOT_ESTABLISHED`;

the candidate again emitted:

`SUPPORTED`

instead of:

`NO_SCIENTIFIC_CLAIM`

Finding:

`D3_UNESTABLISHED_CONFIRMED_LAUNDERING`

### AB15 — FOREIGN NORMALIZATION POLICY IDENTITY ACCEPTED

A policy whose schema was changed to:

`FOREIGN_NORMALIZATION_POLICY`

was still accepted.

Finding:

`GLOBAL_NORMALIZATION_POLICY_AUTHORITY_NOT_PINNED`

### AB16 — CO-FORGED REGISTRY + PROFILE ACCEPTED

The profile contract ID was changed and the supplied registry was modified to point to the new profile/hash.

The candidate accepted the self-consistent pair.

Finding:

`SOURCE_PROFILE_REGISTRY_AUTHORITY_NOT_PINNED`

The candidate currently verifies internal registry/profile consistency but not that the registry itself is the governed registry authority.

## Consolidated defect set

The nine failures reduce to six material correction groups:

```
A0-ABF-01
MEASUREMENT STRICT TYPING / EXTRACTION ABSENT
(AB03, AB04)

A0-ABF-02
EXPECTED-FAMILY AUTHORITY NOT PINNED
(AB08)

A0-ABF-03
D1 / MC2 FAIL-CLOSED PERMISSION OVERRIDES MISSING
(AB10, AB11)

A0-ABF-04
D3 CONFIRMED GUARD MISSING
(AB13, AB14)

A0-ABF-05
GLOBAL NORMALIZATION POLICY AUTHORITY NOT PINNED
(AB15)

A0-ABF-06
SOURCE PROFILE REGISTRY AUTHORITY NOT PINNED
(AB16)
```

## Scientific / downstream boundary

No scientific source result is changed by this test.

No DecisionPolicy, Decision, ACTION or trading authority is opened.

## Verdict

`A0_MINIMAL_IMPLEMENTATION_CANDIDATE = FAIL_ADVERSARIAL_EXPANSION_V0_1`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = FAIL_NOT_CLOSED`

## Next governed action

First persist this exact breaker/finding set and re-break it from the persisted HEAD.

Only after the persisted-head failure profile is reproduced may a minimal correction candidate be designed.

The correction scope must be limited to A0-ABF-01 through A0-ABF-06 and must preserve the original six historical tests plus all 18 adversarial tests.
