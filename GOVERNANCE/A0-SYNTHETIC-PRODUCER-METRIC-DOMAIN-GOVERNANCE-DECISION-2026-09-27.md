# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN GOVERNANCE DECISION

Date: 2026-09-27

Repository:
`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Governed branch:
`integration/system-v1`

Decision base HEAD:
`b4d8c169578a2bdd960e9568b01e6caa86100d84`

A0 V0.3 contract blob:
`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Prior authority-resolution report blob:
`936172106db089228fc0dd404ab629b218db6658`

## 1. Decision

A dedicated source-specific metric-domain authority SHALL be created for the current A0 synthetic producer fixture.

The frozen authority identity is:

`ATDS_A0_SYNTHETIC_PRODUCER_METRIC_DOMAIN_AUTHORITY_V0_1`

Version:

`V0_1`

Scope:

`SYNTHETIC_FIXTURE_ONLY`

Status at adoption:

`FROZEN_UNQUALIFIED`

This authority is intentionally narrow. It does not apply to C01 real confirmation data, MT5, trading, production research producers, DecisionPolicy, Decision or ACTION.

## 2. Governed artifact

Path:

`GOVERNANCE/A0-SYNTHETIC-PRODUCER-METRIC-DOMAIN-AUTHORITY-V0.1.json`

Git blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Canonical content SHA-256:

`5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492`

The exact bytes are authoritative. Semantic reconstruction from a different byte representation does not create the same authority.

## 3. Producer/source binding

The authority applies only when both are exact:

```
producer_identity =
ATDS_A0_SYNTHETIC_PRODUCER_V0_1

source_schema =
ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1
```

No caller-selected producer or schema may substitute this binding.

## 4. Metric identity domain

The closed admitted metric-identity set is:

```
M = { SYNTHETIC_SCORE }
```

Metric identity comparison is case-sensitive.

No aliases are admitted.

Therefore, after this authority is independently qualified and bound into A0:

- `SYNTHETIC_SCORE` may be admitted;
- any other metric identity fails closed;
- an unknown metric identity produces NO AUTHORITATIVE OUTPUT;
- no spelling normalization, aliasing or fuzzy matching is authorized.

## 5. Numeric value domain

For `SYNTHETIC_SCORE`, V0.1 defines only:

`FINITE_JSON_NUMBER`

with:

- bool forbidden as numeric;
- numeric string forbidden;
- NaN forbidden;
- +Infinity forbidden;
- -Infinity forbidden.

No producer-specific minimum is defined.

No producer-specific maximum is defined.

Therefore:

```
minimum = null
maximum = null
```

This is deliberate. Existing evidence does not justify inventing a bounded interval.

The authority does NOT assert that larger or smaller finite values are scientifically better, worse, plausible or implausible.

## 6. Binding fields

This authority governs only:

```
findings[*].measurement.metric
findings[*].measurement.value
```

It does not redefine:

- sample-size semantics;
- fold-role authority;
- measurement scope;
- applicability;
- scientific status;
- evidence level;
- research class;
- confirmatory status;
- downstream permissions.

Those remain governed by their existing A0 authorities.

## 7. Fail-closed semantics

After independent qualification and implementation binding:

```
unknown metric identity
→ NO AUTHORITATIVE OUTPUT

invalid metric value
→ NO AUTHORITATIVE OUTPUT
```

No permissive fallback exists.

## 8. Relationship to Source Profile

The metric-domain authority is a producer/protocol authority, not a competing Source Profile semantics layer.

The current relationship is:

`BOUND_BY_ACCEPTED_PRODUCER_AND_SOURCE_SCHEMA`

The Source Profile may identify/extract the governed measurement but MUST NOT:

- add a new admitted metric;
- add an alias;
- widen the metric domain;
- override fail-closed behavior;
- redefine numeric-domain semantics.

A later change to the admitted metric domain requires a new governed authority version.

## 9. Relationship to Global Normalization Policy

This authority is orthogonal to the Global Normalization Policy.

It has:

```
permission_semantics = NONE
scientific_normalization_semantics = NONE
```

It creates:

- no scientific conclusion;
- no N0–N4 evidence level;
- no permission;
- no seventh permission dimension;
- no Decision;
- no ACTION authority.

The Global Normalization Policy cannot be modified implicitly by this decision.

## 10. Post-observation status

AF04 was observed before this authority was created.

Therefore this authority MUST NOT be represented as pre-observation relative to AF04.

Frozen status:

`ADOPTED_AFTER_AF04_OBSERVATION`

Consequences:

- AF04 cannot itself qualify this authority;
- passing AF04 after implementation would be only a regression observation;
- AF04 remains unadjudicated until the authority passes an independent preregistered qualification;
- the authority is frozen before those future qualification mutants are executed.

## 11. Independent preregistered qualification requirement

Before any AF04 re-adjudication, the next qualification boundary MUST pre-register and execute mutants independent from AF04.

At minimum the frozen mutation family SHALL include:

### Authority identity/binding
- wrong authority schema;
- wrong authority version;
- wrong producer identity;
- wrong source schema;
- one-byte authority modification;
- semantically equal but byte-different authority reconstruction.

### Metric identity
- unknown metric `SYNTH_SCORE`;
- wrong-case metric `synthetic_score`;
- version-like metric `SYNTHETIC_SCORE_V2`;
- added second admitted metric `ALT_SCORE`;
- alias introduction after freeze.

### Numeric semantics
- bool metric value;
- numeric-string metric value;
- NaN;
- +Infinity;
- -Infinity.

### Boundary isolation
- Source Profile attempts to add an admitted metric;
- Source Profile attempts to alias a metric;
- Global Normalization Policy attempts to create metric-domain authority;
- metric-domain authority attempts to add a permission;
- metric-domain authority attempts to alter scientific normalization.

These mutants must be persisted before observing their execution results.

## 12. AF04 adjudication rule

Only after the independent metric-domain qualification is PASS may AF04 be re-run.

If the qualified exact authority is active and bound, then the AF04 mutation:

`SYNTHETIC_SCORE → FOREIGN_METRIC`

has a valid governed oracle:

`FOREIGN_METRIC ∉ M`

and must fail closed.

Until then:

`AF04_IMPLEMENTATION_FAIL = NOT_ESTABLISHED`

## 13. Current authorization state

```
METRIC_DOMAIN_GOVERNANCE_DECISION = ADOPTED
METRIC_DOMAIN_AUTHORITY = FROZEN_UNQUALIFIED
METRIC_DOMAIN_RUNTIME_BINDING = NOT_AUTHORIZED
AF04_READJUDICATION = NOT_AUTHORIZED
ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

The existing governed A0 suite remains 85 tests.

## 14. Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN AUTHORITY TEST-FIRST RED`

That boundary must:

1. preserve the current 85 tests unchanged;
2. persist the independent mutation set before execution;
3. test the frozen authority artifact itself and its intended producer/source binding;
4. make no runtime correction;
5. keep AF04 separate from the independent qualification set;
6. establish PASS/FAIL/BLOCKED from persisted evidence before any AF04 re-adjudication.

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority is opened.
