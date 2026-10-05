# P1-19 — DOWNSTREAM COMPATIBILITY ARCHITECTURE V0.1

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `integration/system-v1`
Parent reviewed: `66f914b867fe9182a1604eba47e07eaab194ac52`
Status: `OPTION B SELECTED — VERSIONED COMMON DOWNSTREAM — IMPLEMENTATION NOT AUTHORIZED`

## Current state

P1.12C produces `QualifiedProducerExecutionResult`. The existing scientific path accepts only the P1.12B `LinkedExperimentExecutionResult` family.

```text
P1.12B → P1.13B → P1.14B → P1.15B → P1.16
P1.12C → BLOCKED
```

P1.13B requires the exact P1.12B type and factory attestation, then carries BI5-specific fields such as file/tick counts, timestamps and `stream_sha256`.

P1.14B also requires the exact P1.12B result and uses `stream_sha256` / `input_stream_sha256` as the measurement-input content identity.

P1.15B and P1.16 have no direct BI5 algorithmic dependency; their incompatibility is inherited through exact upstream types.

## Option comparison

### Option A — producer-specific downstream sibling

Rejected. It would copy evaluation, provenance, authority and finding semantics for each execution owner and create avoidable semantic drift risk.

### Option C — direct compatibility layer into the legacy B chain

Rejected. The legacy B chain requires exact P1.12B type/attestation and BI5-specific measurement-input semantics. A compatibility layer cannot satisfy those requirements for P1.12C without changing their meaning.

### Option B — selected

Create one common, versioned downstream evidence model:

```text
P1.12B native result ─┐
                     ├→ P1.12D QualifiedExecutionEvidenceEnvelope
P1.12C native result ─┘
                              ↓
                     P1.13C Common Evaluation
                              ↓
                     P1.14C Common Measurement Provenance
                              ↓
                     P1.15C Common Evaluator Authority
                              ↓
                     P1.16C Common Qualified Finding
```

The existing B chain remains unchanged during migration.

## Common evidence rule

A structural interface alone is insufficient. P1.12D must create a new factory-attested common envelope only after:

- exact native owner is known;
- exact native result type is verified;
- exact native owner factory attestation succeeds;
- exact experiment identities match.

```text
TYPE COMPATIBILITY != SEMANTIC EQUIVALENCE
COMMON INTERFACE != COMMON AUTHORITY
```

The common core must retain:

- experiment lifecycle identities;
- native owner / contract / type;
- native result ID;
- exact input evidence identity;
- exact measurement-input content identity;
- exact result-content identity;
- execution-procedure identity;
- native execution status;
- reconstruction evidence reference;
- owner-native evidence refs.

Owner-specific fields remain owner-specific.

```text
P1.12B measurement_input_identity = stream_sha256
P1.12C measurement_input_identity = output_sha256
```

## Experiment definition

P1.12C does not carry the complete hypothesis/protocol/measurement-plan text. The future common envelope must therefore bind an exact `experiment_definition_digest` derived from the qualified experiment input/specification.

## Measurement provenance

The future common provenance boundary must bind each measurement to:

```text
measurement_id
execution_evidence_envelope_id
native_result_id
measurement_input_identity
procedure_ref
procedure_sha256
```

An output/result identity by itself is not measurement provenance.

## Downstream preservation

P1.15C should preserve the present evaluator/method-authority semantics.

P1.16C should preserve the existing interpretation policy. Execution-owner compatibility is not a reason to alter scientific finding semantics.

## Verdict

```text
OPTION A = REJECTED
OPTION C DIRECT-TO-LEGACY = REJECTED
OPTION B = SELECTED

TARGET =
P1.12D → P1.13C → P1.14C → P1.15C → P1.16C

LEGACY B CHAIN MODIFIED = NO
REAL AP1 EXECUTION = NOT AUTHORIZED
```

P1-19 stops before implementation.
