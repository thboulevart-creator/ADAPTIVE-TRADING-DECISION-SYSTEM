# A0 — TEST-FIRST RED

Date: 2026-09-27

Governed base HEAD:

`5ba550a736aadc80749d30956c3ca046a31cc50f`

Persisted governing contract:

`GOVERNANCE/A0-RESEARCH-FINDINGS-AUTHORITY-INTERPRETATION-CONTRACT-V0.3.md`

Contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Human adjudication blob:

`d8c5a930ce7b88de8b8d8e3acded625f8794d47f`

## Scope

This phase is TEST-FIRST RED only.

No A0 implementation exists or is authorized by this artifact.

The breaker defines the smallest initial executable surface required to prove the current repository lacks the protections required by A0 V0.3.

## Breaker

Path:

`breakers/a0_research_authority_red_breaker.py`

Qualified breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Default implementation target used by the breaker:

`src/a0_research_authority.py`

Environment override:

`A0_AUTHORITY_MODULE_PATH`

The breaker requires only the minimal candidate surface:

- `CONTRACT`;
- `derive_authoritative_projection(case)`;
- `verify_authoritative_projection(case, projection)`.

Invalid paths may fail closed through `None` or controlled `TypeError / ValueError / KeyError`; the RED does not prescribe one transport mechanism.

## Initial RED cases

The breaker contains exactly six tests:

1. positive synthetic projection;
2. registry/profile authority rejects a profile-hash mismatch;
3. strict source binding rejects a foreign producer;
4. closed permission intersection produces the exact intersection;
5. downstream verification rejects a tampered reconstruction;
6. fail-closed semantics reject an ambiguous registry with multiple ACTIVE profiles.

These cases target the initial causal kernel authorized for RED:

- registry/profile authority;
- strict source binding;
- closed permission intersection;
- downstream authority reconstruction;
- fail-closed semantics.

## Synthetic fixture

The fixture is entirely synthetic.

It contains:

- one synthetic scientific source schema;
- one synthetic producer identity;
- a closed expected family H1/H2/H3;
- SUPPORTED_N0 / REFUTED_N0 / NOT_INTERPRETABLE;
- a pinned profile SHA-256 through the registry;
- a closed permission universe;
- six governed permission dimensions represented through source/policy/profile semantics.

No real research artifact, C01 confirmation data or trading data is accessed.

## RED execution

Sandbox branch:

`sandbox/a0-test-first-red`

Workflow run:

`36323465488`

Results:

- breaker `py_compile = PASS`;
- pytest result = `6 FAILED`;
- each failure reason = `A0_AUTHORITY_MODULE_ABSENT_EXPECTED_RED`;
- sandbox expected-failure workflow verdict = `PASS_EXPECTED_FAILURE`.

Observed current repository state:

`src/a0_research_authority.py = ABSENT`

Therefore the protections required by the adopted A0 V0.3 contract are not implemented.

## RED verdict

`A0_TEST_FIRST_RED = PASS_EXPECTED_FAILURE`

`A0_IMPLEMENTATION = ABSENT`

`A0_IMPLEMENTATION_QUALIFICATION = NOT_STARTED`

This RED is successful because the preregistered breaker fails for the expected current-state reason.

## Non-authorizations

This RED does not authorize:

- treating any A0 implementation as PASS;
- weakening or changing the six tests after implementation observation;
- DecisionPolicy;
- Decision production from A0;
- P1.1 positive authorization;
- ACTION;
- trading/execution;
- C01 real confirmation activity.

## Next governed action

The next phase may create only the smallest A0 implementation candidate required to make this persisted RED progress from module-absence failure to semantic qualification.

The persisted breaker is now the upstream executable constraint.

Any implementation change must be judged against this breaker and the adopted V0.3 contract.
