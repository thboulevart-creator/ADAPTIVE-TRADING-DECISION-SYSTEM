# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN AUTHORITY TEST-FIRST RED

Date: 2026-09-27

Persisted preregistration HEAD:

`2e1c7d4f556367fb5f4a33d44b74d359dc7b39a9`

Frozen authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Authority canonical content SHA-256:

`5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492`

Preregistered manifest blob:

`be8c1c0c805c86d376517ec11da744763c48143c`

Preregistered breaker blob:

`e3620ac348a8042fe1d04cfc9b32c16060fce4a3`

Execution workflow run:

`36340271687`

## Ordering proof

The independent test family MG00..MG21 was persisted on the governed branch before its first execution.

Preregistration commit:

`2e1c7d4f556367fb5f4a33d44b74d359dc7b39a9`

The sandbox workflow was created only after that persistence.

AF04 remained excluded from the breaker. The AF04 metric literal is absent from the breaker source.

## Preserved governed suite

`85/85 PASS`

No historical/V0.1/V0.2/V0.3/V0.4 test was modified.

The A0 runtime was not modified.

## RED result

Target qualifier:

```
src/a0_metric_domain_authority.py
validate_measurement_domain(...)
```

Target kind:

`QUALIFIER_ONLY_NO_RUNTIME_BINDING`

Observed result:

```
MG00..MG21 = 22/22 RED
```

Common failure reason:

`A0_METRIC_DOMAIN_QUALIFIER_REQUIRED`

The qualifier module does not yet exist.

Therefore:

`A0_METRIC_DOMAIN_AUTHORITY_TEST_FIRST_RED = PASS_RED_22_OF_22`

## Interpretation ceiling

The 22 failures do NOT establish 22 independent runtime defects.

They establish that the preregistered qualifier contract has no implementation yet.

No individual mutation guard may be claimed qualified or defective until a qualifier candidate exists and the persisted test family is re-run unchanged.

## Current authority state

```
METRIC_DOMAIN_GOVERNANCE_DECISION = ADOPTED
METRIC_DOMAIN_AUTHORITY = FROZEN_UNQUALIFIED
METRIC_DOMAIN_AUTHORITY_TEST_FIRST_RED = PASS_RED_22_OF_22
METRIC_DOMAIN_QUALIFIER = NOT_IMPLEMENTED
METRIC_DOMAIN_RUNTIME_BINDING = NOT_AUTHORIZED
AF04_READJUDICATION = NOT_AUTHORIZED
ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

## Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN AUTHORITY MINIMAL QUALIFIER CANDIDATE`

That boundary may implement only the minimum standalone qualifier needed to satisfy MG00..MG21.

Constraints:

- preserve MG00..MG21 unchanged;
- preserve the existing 85 tests unchanged;
- do not modify `src/a0_research_authority.py`;
- do not bind the authority into A0 runtime;
- do not re-run AF04 as an adjudication test;
- do not open A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01.
