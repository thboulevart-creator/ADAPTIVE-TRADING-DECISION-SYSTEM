# I_A + I_B — FIRST CONCRETE NATIVE-BI5 IMPLEMENTATION BOUNDARY CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `b2c564f7e4e19f47ef463436c3ff5c71103a0b75`  
**Scope:** formalization only — no I_A/I_B code, no acquisition, no real BI5 processing, no backtest, no permission increase.

## 0. Status and strict separations

This artifact creates the first concrete candidate boundary for:

```text
I_A — reference qualification implementation
+
I_B — independent comparison qualification implementation
```

It consumes the corrected/re-broken candidate chain:

```text
D/R/M candidate blob
2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9

B/A candidate blob
25400abcc3a2a24438954ff27b970bd934313ae3

Q candidate blob
9e15cfb86716894131485a15a180cc170a230287

F/O candidate blob
fe62da06e63a51c336f9a447e7f1e0f3d89cad3b
```

Official gates remain:

```text
I_A = BLOCKED
I_B = BLOCKED
```

Candidate formalization does not qualify either implementation.

Strict separations:

```text
same normative input
≠ shared semantic implementation

independent implementation
≠ different filename only
≠ different traversal order only
≠ wrapper around the same semantic core

I_A output
≠ I_B input

F artifact from I_A
≠ semantic authority for I_B

O comparison
≠ construction rule for either implementation

implementation existence
≠ implementation PASS

candidate
≠ PASS
```

---

# 1. Candidate identities

## 1.1 I_A

```text
implementation_id =
I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER

implementation_version =
I_A_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_REFERENCE_QUALIFIER_V0_1_CANDIDATE
```

## 1.2 I_B

```text
implementation_id =
I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER

implementation_version =
I_B_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_INDEPENDENT_QUALIFIER_V0_1_CANDIDATE
```

Neither version exists as code yet.

---

# 2. Common immutable input set

For one same-state determinism run, both implementations receive the exact same immutable input set:

```text
D materialization
R determinant
M determinant
B determinant
A determinant
Q determinant
F determinant
O determinant reference
raw declared component payloads
qualification-relevant evidence bindings
```

Every determinant must be bound by:

```text
normative_id
normative_version
immutable content reference
integrity digest/reference
```

Both implementations must reject:

- missing determinant;
- version mismatch;
- same ID/version with different expected content;
- ambient fallback configuration;
- parser defaults that substitute for a normative determinant;
- filesystem discovery used to expand/shrink D.

The O determinant is supplied so both implementations know the expected comparison contract, but O is not permitted to construct their qualification result.

---

# 3. Normative execution boundary

Each implementation must independently perform the complete semantic chain:

```text
materialized D
→ verify declared component membership/completeness inputs
→ R selection check
→ B physical interpretation
→ A anomaly classification
→ M candidate logical occurrence construction
→ Q qualification membership/outcome
→ F semantic freeze construction or terminal non-freeze evidence
```

Then, and only then:

```text
I_A result + I_B result
→ O semantic comparison
```

No implementation may skip a semantic stage by consuming the other implementation's stage result.

---

# 4. I_A responsibilities

I_A is the project reference path.

It MUST:

1. consume the exact pinned common input set;
2. independently verify determinant integrity before semantic work;
3. materialize only D-declared components;
4. implement B decoding exactly;
5. construct M candidate logical occurrences without content deduplication;
6. classify A outcomes without silent repair;
7. enforce Q total slot accounting and outcome precedence;
8. produce either:
   - qualified F semantic state, or
   - terminal non-freeze evidence;
9. preserve strict duplicates;
10. preserve exact source→logical conformance witnesses without promoting them to canonical identity;
11. avoid normative temporal ordering;
12. expose a complete execution manifest and semantic result for later O comparison.

I_A MUST NOT derive authority from:

- current V4.3 parser behavior;
- filenames;
- traversal order;
- array order;
- runtime defaults;
- I_B behavior;
- O expected answer.

---

# 5. I_B responsibilities

I_B is an independently implemented qualification path.

I_B MUST perform the same normative semantic responsibilities as I_A from the same raw/common immutable inputs.

Before I_B has finalized its own semantic result, it MUST NOT consume:

```text
I_A decoded records
I_A candidate occurrences
I_A anomaly classifications
I_A Q membership decisions
I_A retained/rejected slot sets
I_A F semantic state
I_A serialized freeze artifact
I_A semantic fingerprints
I_A O-normalized projection
I_A expected cardinality
I_A expected anomaly counts
I_A expected retained count
```

I_B may read I_A output only after its own result is sealed for O comparison/debugging.

I_B MUST fail closed if its own independent path cannot establish the required semantic state.

---

# 6. Shared-code boundary

The purpose of I_B is to prevent a project semantic shortcut from reproducing the same defect in both paths.

## 6.1 Shareable non-semantic primitives

The two implementations MAY share generic infrastructure that does not encode a D/R/M/B/A/Q/F semantic decision, for example:

```text
filesystem byte-read primitive
immutable-byte container
SHA-256 primitive
UTF-8 / JSON library
generic integer/byte utilities
generic logging
generic process/CLI plumbing
standard compression primitive/library
```

A shared primitive is admissible only if its API does not already return a project-semantic object or outcome.

Examples:

```text
allowed:
lzma_decompress(bytes) → bytes

forbidden shared shortcut:
decode_dukascopy_bi5_component(...) → candidate ticks

allowed:
sha256(bytes) → digest

forbidden shared shortcut:
load_verified_B_contract_and_apply_defaults(...) → semantic binding state
```

## 6.2 Forbidden shared semantic modules

I_A and I_B MUST NOT import/call the same project module/helper for any semantic decision involving:

```text
D membership/completeness
R compatibility
B framing/field interpretation/scaling
A anomaly classification/localisability/outcome
M occurrence construction/individuality
Q accounting/membership/outcome
F semantic freeze construction
semantic numeric normalization
source→logical accounting relation
```

They must not call each other transitively for those decisions.

## 6.3 O is shared only after sealing

O may be one common independently reviewable comparator.

Neither I_A nor I_B may call O during semantic construction to obtain:

- a normalization answer;
- expected output;
- target counts;
- target anomalies;
- target membership.

O receives both already-sealed results.

## 6.4 Independent derivation requirement

Separate files/import graphs are necessary but not sufficient.

For every project-owned semantic stage, I_B must be independently derived from the pinned normative contracts rather than copied, generated, mechanically transformed or ported from I_A semantic source.

Required future derivation evidence:

```text
independent_derivation_attestation
semantic_source_provenance
no_copy_or_generated_from_other_path declaration
source_similarity_review_result
independent_stage_level_test_inventory
```

The source-similarity review is a detection control, not a proof of conceptual independence.

It MUST tolerate unavoidable common normative literals such as:

- contract IDs/versions;
- field names;
- exact constants mandated by B/Q/F;
- anomaly class IDs;
- status enum literals.

It MUST specifically look for substantial shared semantic control flow or whole-function/module copying disguised by renaming.

Unresolved semantic derivation provenance keeps I_B BLOCKED.

---

# 7. Independent implementation manifests

Each implementation candidate must eventually expose an immutable implementation manifest containing at minimum:

```text
implementation_id
implementation_version
entrypoint
source file inventory
source content digests
project dependency/import inventory
external dependency versions
semantic-stage ownership map
semantic source provenance
independent-derivation evidence reference
build/runtime environment identity
```

The manifests must make it reviewable whether:

- I_A imports I_B;
- I_B imports I_A;
- both import a forbidden shared semantic module;
- either uses a precomputed semantic artifact from the other;
- the executed source matches the qualified source.

Manifest equality is not required.

---

# 8. Semantic-stage ownership map

Both implementation manifests MUST explicitly identify which implementation-owned code performs:

```text
D preflight/materialization validation
R compatibility check
B decompression-envelope validation
B 20-byte framing
B >IIIff decoding
B timestamp reconstruction
B price scaling
B finite binary32 volume interpretation
A anomaly classification
M logical occurrence construction
Q target binding/accounting/outcome
F semantic state construction
F serialization handoff
```

For every semantic stage, I_A and I_B must name different project-owned implementation units.

A generic external primitive may appear in both dependency graphs, but it must not replace the independently owned semantic stage.

---

# 9. Result sealing and pre-seal runtime isolation

Each implementation result must be sealed before the other implementation's semantic result becomes readable by that execution domain.

Conceptual sequence:

```text
same immutable input package
      ↓                    ↓
isolated I_A domain    isolated I_B domain
      ↓                    ↓
semantic result A      semantic result B
      ↓                    ↓
seal A                 seal B
       \                  /
        \                /
         → O comparison ←
```

Before both seals exist, each execution domain may receive only:

```text
common immutable input package
its own implementation/runtime files
explicitly allowed non-semantic external dependencies
its own private writable workspace
```

Pre-seal forbidden cross-path channels include:

```text
other implementation workspace/output
shared semantic cache
temporary semantic files
shared mutable database
IPC carrying semantic results
network endpoint carrying semantic results
shared memory carrying semantic results
environment variables carrying semantic results
pre-existing semantic artifact produced by the other path
```

The final harness must enforce or evidence this boundary through an explicit pre-seal input/read allowlist and isolated workspaces/execution domains.

Required future isolation evidence includes:

```text
preseal_input_allowlist
workspace_isolation_identity
network_and_IPC_policy
environment_variable_allowlist
cache_policy
runtime_read_or_dependency_trace_or_equivalent_sandbox_proof
seal timestamp/order evidence
```

Only after both seals exist may the harness expose both semantic results to O or to cross-path debugging.

The seal binds:

```text
implementation manifest digest
input determinant digests
materialized D identity
execution_status
semantic_status
freeze_status
F semantic result or terminal non-freeze state
execution evidence
isolation evidence reference
```

The seal is execution provenance/integrity only.

It is not occurrence identity.

---

# 10. Exact terminal status model

I_A and I_B MUST expose three disjoint status axes.

## 10.1 Execution status

Closed enum:

```text
execution_status =
COMPLETED
ENVIRONMENT_BLOCKED
IMPLEMENTATION_ERROR
```

Meaning:

- `COMPLETED`: the implementation executed the governed semantic path to a normative terminal semantic state;
- `ENVIRONMENT_BLOCKED`: a required executable resource/environment was unavailable before a governed semantic terminal state could be reached;
- `IMPLEMENTATION_ERROR`: implementation non-conformance, unhandled exception, invariant breach or other implementation failure prevented legitimate semantic completion.

## 10.2 Semantic status

Closed enum:

```text
semantic_status =
QUALIFIED
QUALIFICATION_BLOCKED
ACQUISITION_REJECTED
NOT_REACHED
```

## 10.3 Freeze status

Closed enum:

```text
freeze_status =
FROZEN
NOT_CREATED
NOT_REACHED
```

## 10.4 Mandatory invariants

```text
execution_status != COMPLETED
→ semantic_status = NOT_REACHED
→ freeze_status = NOT_REACHED

semantic_status = QUALIFIED
→ execution_status = COMPLETED
→ freeze_status = FROZEN

semantic_status = QUALIFICATION_BLOCKED
→ execution_status = COMPLETED
→ freeze_status = NOT_CREATED

semantic_status = ACQUISITION_REJECTED
→ execution_status = COMPLETED
→ freeze_status = NOT_CREATED

freeze_status = FROZEN
→ semantic_status = QUALIFIED
```

An `IMPLEMENTATION_ERROR` or `ENVIRONMENT_BLOCKED` outcome MUST NOT be normalized into semantic `QUALIFICATION_BLOCKED`.

A partial qualified universe is forbidden for every status other than legitimate `COMPLETED + QUALIFIED + FROZEN`.

## 10.5 Same-state comparison implications

Examples:

```text
A: COMPLETED + QUALIFIED
B: IMPLEMENTATION_ERROR + NOT_REACHED
→ implementation non-conformance / executable test FAIL
  if B was expected to execute in the qualified environment

A: COMPLETED + QUALIFICATION_BLOCKED
B: ENVIRONMENT_BLOCKED + NOT_REACHED
→ not semantic agreement
→ executable test BLOCKED/FAIL according to whether the environment absence
  is itself an unresolved prerequisite or an implementation-side defect

A: COMPLETED + QUALIFICATION_BLOCKED
B: COMPLETED + QUALIFICATION_BLOCKED
→ terminal semantic agreement may be checked
→ no qualified-universe equality PASS exists

A: COMPLETED + ACQUISITION_REJECTED
B: COMPLETED + ACQUISITION_REJECTED
→ compare terminal semantics
→ no qualified universe exists
```

The final harness must preserve these axes independently and must never collapse them into one generic `BLOCKED` label.

---

# 11. Traversal / parallelism / cache independence

I_A and I_B MAY intentionally use different:

```text
component traversal order
slot iteration strategy
worker partition
parallel/sequential execution
internal collection type
cache strategy
serialization order
```

These variations are encouraged for Q-RM-12 attacks.

They may not change semantic output.

Any cache used by either path must be keyed/validated against the complete normative determinant/input state necessary to avoid stale semantic reuse.

A cache hit may not import semantic results produced under a different determinant set.

---

# 12. No implementation defaults as authority

Implementation convenience never closes a contract gap.

Examples forbidden:

```text
missing price scale
→ use current parser /1000 default

missing hour provenance
→ infer filename

unknown anomaly
→ drop record

missing Q parameter
→ use implementation default

missing D component
→ shrink domain

missing evidence
→ trust I_A result

F serialization conflict
→ use row order
```

Any missing required normative input produces BLOCKED.

---

# 13. I_A output contract

I_A produces:

```text
ImplementationQualificationResult
- implementation_id/version
- implementation_manifest_digest
- exact input determinant bindings
- execution terminal status
- semantic qualification status
- complete semantic stage evidence
- F semantic result if legitimately created
- terminal non-freeze evidence otherwise
- result seal
```

No canonical occurrence enumeration is introduced.

---

# 14. I_B output contract

I_B produces the same abstract result shape independently.

The common abstract schema may be specified normatively.

The code that populates semantic fields must remain independently implemented.

A shared schema definition does not authorize a shared semantic builder.

---

# 15. O handoff

O receives both sealed abstract results.

Before semantic comparison, O validates:

```text
same normative input state
same materialized D identity/input state
expected implementation identities
valid implementation/result seals
no determinant integrity conflict
valid F semantics where qualification is QUALIFIED
```

Then O applies the corrected F/O semantic equality rules.

O does not mutate either result.

---

# 16. Independence evidence required before executable PASS

An eventual I_A/I_B qualification candidate must provide at least:

```text
I_A implementation manifest
I_B implementation manifest
dependency/import graph evidence
source digest evidence
forbidden-semantic-sharing scan/result
independent-derivation attestation/provenance
source-similarity review result
independent stage-level test inventories
pre-seal runtime-isolation evidence
closed pre-seal input/read allowlists
result-sealing evidence
one-sided semantic fault-injection evidence
Q-RM-12 adversarial execution evidence
```

The one-sided fault-injection requirement means:

- mutate or substitute one semantic behavior in only I_A while I_B remains unchanged;
- demonstrate that O detects semantic divergence or the affected implementation blocks/fails;
- repeat with at least one I_B-only semantic mutation.

These are breaker/qualification attacks, not production behavior.

They prove the harness is not merely comparing one shared semantic product to itself.

---

# 17. Independence non-claims

This boundary does NOT claim that structural code separation mathematically proves the absence of every common conceptual bug.

Both implementations are governed by the same normative contracts and may make the same independently authored mistake.

The purpose of I_B is to remove shared project semantic execution shortcuts and create a genuinely falsifiable second derivation.

Therefore final confidence depends on:

```text
independent semantic code path
+
adversarial diversity
+
O comparison
+
contract-level attacks
```

not source-file difference alone.

---

# 18. Implementation eligibility gate

I_A code may be implemented only after this boundary survives governed adversarial qualification.

I_B code may be implemented only after this boundary survives governed adversarial qualification.

Even then, executable qualification remains BLOCKED while upstream concrete execution prerequisites remain unavailable.

No implementation code is authorized by candidate persistence alone.

---

# 19. Permission boundary

Nothing in I_A/I_B formalization changes:

```text
real data acquisition       = NOT AUTHORIZED
native BI5 download         = NOT AUTHORIZED
real BI5 processing         = NOT AUTHORIZED
real backtest               = NOT AUTHORIZED
positive P1.1 AUTHORIZED    = BLOCKED
paper / broker / live       = NOT AUTHORIZED
```

---

# 20. Pre-break verdict state

```text
I_A/I_B implementation boundary candidate
= PERSISTED CANDIDATE once committed

I_A official gate
= BLOCKED

I_B official gate
= BLOCKED
```

No code exists or is claimed.

---

# 21. Next governed action

Adversarially break this exact persisted I_A/I_B boundary candidate before any implementation.

Attack at minimum:

- I_B imports I_A semantic helper directly;
- both paths import same project BI5 decoder;
- both paths consume same precomputed B candidates;
- both paths consume same A anomaly decisions;
- both paths consume same Q membership result;
- I_B reconstructs from I_A F artifact instead of raw common inputs;
- shared schema secretly contains semantic defaults/builders;
- shared cache contains semantic results;
- O normalization used during construction by both paths;
- same result object compared to itself through two wrappers;
- copied/aliased entrypoint masquerades as I_B;
- runtime monkeypatch makes I_B call I_A;
- dependency graph incomplete or dynamic import hides sharing;
- result of one implementation becomes readable before the other seals;
- different traversal order changes result;
- one path silently applies market-value filters;
- one path sorts timestamps;
- one path collapses strict duplicates;
- one-sided mutant is not detected by O/harness;
- missing environment is mislabeled as deterministic BLOCKED agreement;
- both BLOCKED is falsely promoted to PASS;
- code/source digest differs from implementation manifest;
- implementation defaults close missing normative inputs;
- permission leakage.

No I_A/I_B code, acquisition or real backtest is permitted during the break.
