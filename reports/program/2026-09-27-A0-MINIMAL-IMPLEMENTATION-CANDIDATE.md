# A0 — MINIMAL IMPLEMENTATION CANDIDATE

Date: 2026-09-27

Governed base HEAD:

`287f4f3134315404053a545ec032c2365142db41`

Governing contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Persisted RED breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Candidate implementation:

`src/a0_research_authority.py`

Candidate implementation blob:

`737f041b7b083f832f475b2aab607fb417c74fe0`

## Scope

This is the smallest implementation candidate intended to satisfy the six persisted A0 TEST-FIRST RED cases.

It is not a claim of full A0 V0.3 conformance.

The persisted breaker was not modified.

## Public candidate surface

Exactly:

- `CONTRACT`;
- `derive_authoritative_projection(case)`;
- `verify_authoritative_projection(case, projection)`.

No DecisionPolicy, Decision, ACTION, broker, MT5, trading, knowledge-promotion or C01-real surface is introduced.

## Implemented causal kernel

The candidate implements enough semantics to cover:

1. exact source/profile/registry byte identities;
2. exactly-one-ACTIVE profile resolution for the source schema;
3. profile SHA-256 verification;
4. exact producer/source/profile binding;
5. closed expected-family completeness for the synthetic fixture;
6. policy-based native-status normalization;
7. exact six-source permission intersection represented by the fixture;
8. canonical deterministic projection hashing;
9. downstream verification by deterministic re-derivation and exact equality;
10. fail-closed rejection of ambiguous registry state.

The candidate also uses strict JSON duplicate-key and non-finite parsing for the artifacts it parses. These behaviors are within the adopted V0.3 contract but are not yet broadly adversarially qualified.

## Deliberately not claimed

This candidate does NOT establish complete qualification of:

- every V0.3 invariant;
- CR1 real profile admission;
- CR2 real profile admission;
- C01 profile admission;
- all control-state semantics;
- fold semantics;
- applicability/lineage/supersession semantics;
- all strict numeric/coercion cases;
- all epistemic-laundering attacks;
- all permission attacks;
- all reconstruction attacks;
- all semantic escape attacks.

Those require the next adversarial phase.

## Sandbox execution

Sandbox branch:

`sandbox/a0-minimal-implementation-candidate`

Workflow run:

`36323985814`

Verified:

- candidate `py_compile = PASS`;
- persisted breaker `py_compile = PASS`;
- persisted breaker blob = exact `e02ecfa6d30c2877a33f5c5d81b161ee562202b6`;
- exact persisted RED suite = `6/6 PASS`.

## Status

`A0_MINIMAL_IMPLEMENTATION_CANDIDATE = GREEN_ON_INITIAL_RED`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

## Next governed action

Persist exactly:

1. the candidate module;
2. this candidate report;
3. checkpoint update.

Then perform a fresh persisted-head re-break of the exact candidate commit against the unchanged persisted six-test breaker.

A PASS of that re-break may close only the initial RED transition. It MUST NOT be interpreted as full A0 V0.3 qualification.
