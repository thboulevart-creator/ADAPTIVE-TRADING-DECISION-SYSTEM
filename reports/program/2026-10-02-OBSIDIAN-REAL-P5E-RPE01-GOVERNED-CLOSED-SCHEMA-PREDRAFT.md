# RPE-01 — N4 GOVERNED CLOSED SCHEMA — PRE-DRAFT

Date: 2026-10-02

## Objective

Qualify a reusable, fail-closed JSON schema guard before any later REAL P5-E stage introduces adapter, runner, experiment, or evidence configuration.

RPE-01 closes the structural failure mode identified by N4/NF-D:

> authority must not enter through an unknown key, duplicate key, permissive numeric parsing, list laundering, or an adjacent ungoverned configuration source.

## Starting authority

Base HEAD:
`d904eb61d9b704dc8ac38da445eb1cd491a58b33`

Readiness V0.2:
`QUALIFIED_AND_HUMAN_ADOPTED`

RPE-01 is the only implementation stage opened by the current user instruction.

All later RPE stages remain closed.

## Architecture

The guard is a pure boundary:

```text
explicit raw JSON bytes/text
        +
explicit governed schema
        ↓
strict parser
        ↓
closed recursive schema validator
        ↓
VALIDATED DOCUMENT
or
FAIL-CLOSED
```

The guard does not discover configuration.

It must not read:
- environment variables;
- CLI arguments;
- Git configuration;
- network state;
- P5-D4 control state;
- Vault/CURRENT state.

This makes configuration provenance the caller's explicit responsibility and prevents the guard itself from becoming an alternate authority channel.

## Strict parser requirements

Before dictionary construction:
- reject duplicate object member names;
- reject `NaN`;
- reject `Infinity`;
- reject `-Infinity`;
- require UTF-8 JSON.

Standard JSON floats may parse as floats, but a schema node of type `integer` must reject every float, including `30.0` and `1e2`.

A boolean must never satisfy an integer schema merely because Python `bool` subclasses `int`.

## Schema language V0.1

Supported node kinds:
- object;
- array;
- string;
- integer;
- boolean;
- null.

Object nodes are closed: the exact key set is normative.

Array nodes can freeze:
- item schema;
- minimum/maximum length;
- uniqueness;
- allowed scalar vocabulary;
- exact ordered content when order itself is normative.

Scalar nodes can freeze:
- type;
- const;
- enum;
- regex pattern;
- integer min/max.

The schema definition itself must be strictly validated so an unknown schema-language key cannot silently widen the guard.

## P5-E adopted-contract schema

RPE-01 will create a governed schema for the already adopted P5-E V0.1 contract without modifying the contract bytes.

The schema closes every object depth.

Normative lists will be unique and use a closed vocabulary.

`real_end_to_end_stages` will additionally freeze exact order.

The guard is not a replacement for semantic invariants or object binding.

It provides an independent structural defense against intentionally re-bound future amendments.

## Future REAL P5-E artifacts

The same guard API is intended for later governed JSON artifacts:
- RPE-02 real-time contract/config;
- RPE-04 adapter configuration;
- RPE-05 runner configuration;
- RPE-06 experiment preregistration;
- execution evidence envelopes.

Those future schemas are not created in RPE-01.

RPE-01 only qualifies the guard capability and one concrete schema for the adopted P5-E contract.

## Test-first plan

1. Persist preregistration.
2. Create RED tests while implementation/schema are absent.
3. Persist RED.
4. Implement the minimum pure guard.
5. Generate/review the concrete P5-E schema.
6. Run mandatory adversarial breakers.
7. Run a programmatic mutation sweep over every object node/key and selected typed/list mutations.
8. Re-run targeted existing P5-E tests.
9. Persist qualification evidence with exact blobs.
10. Produce external-review packet.
11. STOP before human adoption/RPE-02.

## Maximum claim

If successful:

`RPE01_GOVERNED_CLOSED_SCHEMA_CANDIDATE = QUALIFIED_FOR_EXTERNAL_REVIEW`

Not claimed:
- RPE-02 readiness or implementation;
- real-time timing qualification;
- ancestry classification;
- remote adapter;
- timed runner;
- real experiment;
- REAL P5-E.

`REAL_P5E = CLOSED`
