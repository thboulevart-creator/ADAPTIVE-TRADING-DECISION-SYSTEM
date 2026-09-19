# I_A + I_B — ADVERSARIAL BREAK OF FIRST NATIVE-BI5 IMPLEMENTATION-BOUNDARY CANDIDATE

**Date:** 2026-09-19  
**Candidate commit under attack:** `90e81819434f559e17568660bebb0f72c4e945b6`  
**Candidate blob:** `f2bdf83f4cfe4dbfa7b275bc620a33eea0460c07`  
**Candidate artifact:** `reports/data-qualification/iab_native_bi5_implementation_boundary_candidate_2026-09-19.md`

No I_A/I_B code, BI5 download, real-data processing or backtest occurred.

## 1. Attack basis

The persisted candidate was attacked against:

- corrected/re-broken D/R/M/B/A/Q/F/O candidate chain;
- Q-RM-12 reconstruction/determinism requirements;
- qualification input register requirement that I_B be independently implemented with no shared semantic shortcut capable of masking the same defect;
- no-partial-universe behavior;
- strict duplicate preservation;
- no temporal authority from traversal/serialization order;
- no implementation default as normative authority.

A defect is recorded only when the candidate allows materially different conforming implementations or cannot provide evidence for a required independence/conformance claim.

---

# 2. Shared-semantic-code attacks that survive

## IAB-A01 — I_B imports I_A semantic helper directly

**SURVIVES.**

Explicitly forbidden.

## IAB-A02 — both paths import the same project BI5 semantic decoder

**SURVIVES.**

Shared project semantic modules for B/A/Q/F decisions are explicitly forbidden.

## IAB-A03 — both paths consume the same precomputed B candidates

**SURVIVES.**

Each path must derive B semantics independently from the same raw/common immutable inputs.

## IAB-A04 — both paths consume the same A outcomes or Q membership

**SURVIVES.**

These are semantic intermediate results and cannot be shared.

## IAB-A05 — I_B reconstructs from I_A F artifact

**SURVIVES.**

I_B is forbidden from reading I_A F semantic output before its own result is sealed.

---

# 3. Demonstrated defect IAB-F01 — TERMINAL_STATUS_DOMAIN_UNDERSPECIFIED

The candidate requires the final harness to distinguish expected semantic BLOCKED outcomes from missing-environment BLOCKED states, and its abstract result mentions:

```text
execution terminal status
semantic qualification status
```

but it never defines exact disjoint status domains or precedence.

Attack A:

I_A reaches Q and correctly derives:

```text
QUALIFICATION_BLOCKED
```

because of a non-localisable anomaly.

Attack B:

I_B never reaches Q because its runtime dependency is unavailable.

Both paths can currently be summarized loosely as "BLOCKED".

A harness could then report:

```text
A BLOCKED
B BLOCKED
→ agreement
```

even though only A produced the governed semantic Q outcome and B suffered an execution-environment failure.

Attack C:

I_A raises an unhandled implementation exception after partially interpreting records.

If this is projected into the same generic BLOCKED label, a real implementation defect can be mistaken for expected fail-closed qualification behavior.

This violates the Q-RM-12 PASS/FAIL/BLOCKED distinction because:

```text
semantic qualification BLOCKED
≠ executable environment unavailable
≠ implementation non-conformance/error
```

Result:

```text
BREAK — IAB-F01
TERMINAL_STATUS_DOMAIN_UNDERSPECIFIED
```

Required minimal correction:

Define independent status axes with exact closed enums.

At minimum:

```text
execution_status =
COMPLETED
ENVIRONMENT_BLOCKED
IMPLEMENTATION_ERROR

semantic_status =
QUALIFIED
QUALIFICATION_BLOCKED
ACQUISITION_REJECTED
NOT_REACHED

freeze_status =
FROZEN
NOT_CREATED
NOT_REACHED
```

Required invariants include:

```text
execution_status != COMPLETED
→ semantic_status = NOT_REACHED
→ freeze_status = NOT_REACHED

semantic_status = QUALIFIED
→ execution_status = COMPLETED

semantic Q/F BLOCKED
→ execution_status = COMPLETED
→ semantic_status = QUALIFICATION_BLOCKED
→ freeze_status = NOT_CREATED
```

An implementation error must never be normalized into a semantic qualification BLOCKED result.

---

# 4. Demonstrated defect IAB-F02 — INDEPENDENT_DERIVATION_EVIDENCE_UNDERSPECIFIED

The candidate correctly forbids shared project semantic modules and requires separate implementation units.

However, structural separation alone still permits:

```text
I_A semantic source
→ copy/paste
→ rename symbols
→ save under I_B files
```

The two paths then:

- have different files;
- have different import graphs;
- can have different source digests after superficial renaming;
- do not import one another;
- pass a forbidden-shared-module scan;
- can still reproduce the exact same implementation mistake because I_B was not independently derived.

The candidate itself acknowledges:

```text
structural code separation
does not mathematically prove
absence of every common conceptual bug
```

but the qualification input register requires an **independently implemented path**, not merely runtime module separation.

The current required evidence set does not include any derivation/provenance control capable of distinguishing independent reimplementation from copied semantic implementation.

Result:

```text
BREAK — IAB-F02
INDEPENDENT_DERIVATION_EVIDENCE_UNDERSPECIFIED
```

Required minimal correction:

For project-owned semantic stages, require implementation-provenance evidence stating that I_B was independently derived from the pinned normative contracts rather than copied/generated/transformed from I_A semantic source.

At minimum, require:

```text
independent_derivation_attestation
semantic source provenance
no-copy/no-generated-from-other-path declaration
source similarity review result
independent stage-level test inventory
```

The source-similarity control is not a proof of conceptual independence and must not reject unavoidable common literals/constants from the same normative contract.

Its purpose is to detect whole-function/module semantic copying disguised by renaming.

Shared normative constants/IDs are permitted.

A later qualification must classify unresolved derivation provenance as BLOCKED, not PASS.

---

# 5. Demonstrated defect IAB-F03 — CROSS_PATH_INFORMATION_FLOW_PROOF_UNDERSPECIFIED

The candidate normatively says I_B must not read I_A semantic outputs before sealing, but the proposed evidence set is mainly:

- source/import manifests;
- dependency graph evidence;
- semantic-sharing scan;
- result seals;
- one-sided mutants.

This does not prove the runtime information-flow property.

Attack:

I_A writes an intermediate semantic result to:

```text
/tmp/reference_result.json
```

I_B has no source import dependency on I_A.

I_B reads that file through a generic JSON/file API.

Static import/source scans show no forbidden shared semantic module.

Both manifests can still look structurally independent.

A similar leak can occur through:

```text
environment variable
shared cache
temporary database
IPC socket
network endpoint
shared memory
pre-existing workspace artifact
```

The candidate forbids semantic sharing in principle, but does not require a closed runtime read-set or isolation evidence capable of demonstrating that I_B had access only to the common immutable input package before sealing.

Therefore the core claim:

```text
I_A output ≠ I_B input
```

is not yet executable/falsifiable enough.

Result:

```text
BREAK — IAB-F03
CROSS_PATH_INFORMATION_FLOW_PROOF_UNDERSPECIFIED
```

Required minimal correction:

The final determinism harness must execute I_A and I_B in isolated execution domains before sealing.

Each pre-seal path must receive only:

```text
common immutable input package
its own implementation/runtime files
explicitly allowed non-semantic external dependencies
its own private writable workspace
```

and must not have read access to the other path's workspace/output.

Required evidence must include:

```text
pre-seal input allowlist
workspace isolation identity
network/IPC policy
environment-variable allowlist
cache policy
runtime read/dependency trace or equivalent sandbox proof
seal timestamp/order evidence
```

Only after both seals may the harness expose both semantic results to O.

A simple statement in source code that I_B "does not read I_A" is insufficient.

---

# 6. Attacks that survive

## IAB-A06 — shared schema contains semantic defaults/builders

**SURVIVES conceptually.**

The candidate permits a shared schema but forbids a shared semantic builder.

After IAB-F03 correction, runtime evidence must also show that no hidden generated semantic object enters through a shared cache/artifact.

## IAB-A07 — standard compression primitive shared

**SURVIVES.**

A generic LZMA bytes→bytes primitive is not itself the project B semantic stage.

The independently owned B stages must still separately enforce envelope/framing/field semantics.

## IAB-A08 — O used during construction

**SURVIVES.**

Explicitly forbidden.

## IAB-A09 — same result object compared through two wrappers

**SURVIVES normatively.**

I_B may not consume I_A semantic result.

IAB-F03 is required to make this runtime prohibition evidentially closed.

## IAB-A10 — traversal order differs

**SURVIVES.**

Traversal is non-semantic.

## IAB-A11 — one path adds hidden market-value filters

**SURVIVES as a semantic attack.**

The path becomes non-conforming and O must detect divergence against the other conforming path.

## IAB-A12 — one path sorts timestamps normatively

**SURVIVES.**

Forbidden by upstream contracts and must produce divergence/non-conformance.

## IAB-A13 — one path collapses strict duplicates

**SURVIVES.**

O's multiset/source→logical relation exposes the defect.

## IAB-A14 — implementation defaults fill missing normative inputs

**SURVIVES.**

Explicitly forbidden.

## IAB-A15 — permission leakage

**SURVIVES.**

No acquisition/backtest permission is created.

---

# 7. One-sided mutant attack

The candidate requires at least one I_A-only and one I_B-only semantic mutation.

This is useful evidence that the harness compares two semantic products rather than one shared product.

However it does not by itself prove independent derivation and cannot replace IAB-F02.

**NO ADDITIONAL BREAK.**

---

# 8. Verdict

The first persisted I_A/I_B implementation-boundary candidate is not promoted.

```text
I_A/I_B FIRST NATIVE-BI5 IMPLEMENTATION BOUNDARY CANDIDATE
FAIL
```

Demonstrated defects:

1. `IAB-F01 — TERMINAL_STATUS_DOMAIN_UNDERSPECIFIED`
2. `IAB-F02 — INDEPENDENT_DERIVATION_EVIDENCE_UNDERSPECIFIED`
3. `IAB-F03 — CROSS_PATH_INFORMATION_FLOW_PROOF_UNDERSPECIFIED`

No D/R/M/B/A/Q/F/O mutation is authorized.

No I_A/I_B implementation is authorized yet.

No acquisition or real backtest is authorized.

---

# 9. Authorized minimal correction

Correct only the I_A/I_B boundary candidate:

1. define disjoint execution / semantic / freeze status domains and invariants;
2. require independent-derivation provenance for project-owned semantic stages;
3. require pre-seal runtime isolation / closed input-read boundary for I_A and I_B;
4. keep generic non-semantic shared primitives allowed;
5. keep O strictly post-seal;
6. preserve all upstream semantics and permissions.

Then persist the corrected candidate and re-break the complete attack set from a freshly verified HEAD.
