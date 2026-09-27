# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN AUTHORITY MINIMAL QUALIFIER — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`905b2b0440cfbc798e4a53d3948f6318bfa494bd`

Standalone qualifier:

`src/a0_metric_domain_authority.py`

Qualifier blob:

`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Frozen authority blob:

`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Authority content SHA-256:

`5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492`

Preregistered manifest blob:

`be8c1c0c805c86d376517ec11da744763c48143c`

Preregistered independent breaker blob:

`e3620ac348a8042fe1d04cfc9b32c16060fce4a3`

Pre-persistence sandbox qualification run:

`36340760039`

Fresh persisted-head re-break run:

`36340903575`

## Persistence scope

The governed candidate commit adds exactly:

`src/a0_metric_domain_authority.py`

It does not modify:

- `src/a0_research_authority.py`;
- historical/V0.1/V0.2/V0.3/V0.4 breakers;
- the MG00..MG21 breaker;
- the frozen authority artifact;
- the preregistration manifest;
- the A0 V0.3 contract.

## Qualifier behavior

The standalone qualifier accepts only when all are true:

- authority bytes match the frozen authority SHA-256 exactly;
- producer identity is `ATDS_A0_SYNTHETIC_PRODUCER_V0_1`;
- source schema is `ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1`;
- metric identity is exactly `SYNTHETIC_SCORE`;
- metric value is an int/float finite JSON number;
- bool is rejected;
- numeric strings are rejected;
- NaN and infinities are rejected;
- non-empty Source Profile takeover claims are rejected;
- non-empty Global Normalization Policy takeover claims are rejected.

The qualifier creates no permission, scientific normalization, Decision or ACTION authority.

## Qualification

Sandbox candidate:

`107/107 PASS`

Fresh persisted-head re-break:

`107/107 PASS`

Composition:

```
existing A0 suite = 85/85 PASS
independent metric-domain family MG00..MG21 = 22/22 PASS
TOTAL = 107/107 PASS
```

AF04 remained excluded.

## Verdict

`A0_METRIC_DOMAIN_MINIMAL_QUALIFIER = PASS_107_OF_107`

`A0_METRIC_DOMAIN_MINIMAL_QUALIFIER_PERSISTED_REBREAK = PASS_107_OF_107`

`A0_METRIC_DOMAIN_AUTHORITY_STANDALONE_QUALIFICATION = PASS`

The authority artifact itself remains byte-immutable with its historical adoption field:

`status = FROZEN_UNQUALIFIED`

That field records its status at adoption and is not rewritten post hoc.

Qualification state is carried externally by this report/checkpoint.

## Authorization ceiling

This PASS qualifies only the standalone authority/qualifier pair relative to the preregistered MG00..MG21 family.

It does NOT bind the authority into `src/a0_research_authority.py`.

Therefore:

```
METRIC_DOMAIN_RUNTIME_BINDING = NOT_AUTHORIZED
AF04_READJUDICATION = NOT_AUTHORIZED
ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

## Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING GOVERNANCE DECISION`

That boundary must decide the exact integration contract before any runtime mutation, including:

- where the qualifier is invoked;
- which producer/source combinations require it;
- whether absence of the metric-domain authority is fail-closed;
- exact carrier/trace representation;
- how Source Profile extraction and metric-domain validation compose;
- proof that Global Normalization Policy receives no new authority;
- AF04 remains excluded until the binding itself is implemented and independently qualified.

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority is opened.
