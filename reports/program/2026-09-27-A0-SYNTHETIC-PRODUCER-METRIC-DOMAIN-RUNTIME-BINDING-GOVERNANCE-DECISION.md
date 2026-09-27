# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING GOVERNANCE DECISION — VERIFICATION

Date: 2026-09-27

Reviewed governed base HEAD:

`6f55748df1abbc72e437b077ed7912d6e15803a1`

Decision document blob:

`82b399f06c41fa740a3676d0272cb39759911a7f`

Frozen authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Standalone qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Preregistered standalone breaker blob:

`e3620ac348a8042fe1d04cfc9b32c16060fce4a3`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Verification run:

`36341764050`

## Scope verification

PASS.

The sandbox candidate added only:

`GOVERNANCE/A0-SYNTHETIC-PRODUCER-METRIC-DOMAIN-RUNTIME-BINDING-GOVERNANCE-DECISION-2026-09-27.md`

No `src` file was modified.

## Frozen surface preservation

`107/107 PASS`

Composition remains:

```
existing A0 suite = 85
standalone metric-domain authority family = 22
TOTAL = 107
```

## Adopted integration contract

The decision freezes the later binding semantics as follows:

- exact applicable pair = synthetic producer V0.1 + synthetic scientific result V0.1;
- authority resolved from fixed governed repository path, never caller-supplied;
- exact frozen authority mandatory and fail-closed;
- binding occurs after existing schema/producer/profile/expected-family authority is established;
- every present measurement metric/value is validated before authoritative measurement-reference use;
- Source Profile remains extraction-only for this concern;
- Global Normalization Policy receives no metric-domain authority;
- carrier adds exactly:
  - `metric_domain_authority_identity`;
  - `metric_domain_authority_sha256`;
  - `metric_domain_validation`;
- caller cannot select, disable or override the authority;
- verification remains deterministic re-derivation;
- AF04 remains excluded until the binding has its own preregistered independent qualification.

## Current status

```
METRIC_DOMAIN_AUTHORITY_STANDALONE_QUALIFICATION = PASS
METRIC_DOMAIN_RUNTIME_BINDING_GOVERNANCE_DECISION = ADOPTED
METRIC_DOMAIN_RUNTIME_BINDING = NOT_IMPLEMENTED
METRIC_DOMAIN_RUNTIME_BINDING_QUALIFICATION = NOT_YET
AF04_READJUDICATION = NOT_AUTHORIZED
ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

## Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING TEST-FIRST RED`

That boundary must persist its independent integration breaker before any runtime binding implementation or first execution.
