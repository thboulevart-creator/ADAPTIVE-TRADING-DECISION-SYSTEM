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


---

# 10. Persisted-head re-break after minimal correction

**Corrected candidate HEAD:** `00b87a1a817046ad0f1510420ef098d117a39559`  
**Corrected candidate blob:** `fac8d143a836b0c02538c607ac5ab71357824537`

The branch was freshly verified identical to that HEAD before re-break.

The corrected candidate blob was re-read from GitHub and matched the expected blob before the attack set was reapplied.

No candidate mutation occurred during this re-break.

## 10.1 Re-break IAB-F01

Original defect:

`TERMINAL_STATUS_DOMAIN_UNDERSPECIFIED`

Corrected candidate now exposes three closed axes:

```text
execution_status
= COMPLETED
| ENVIRONMENT_BLOCKED
| IMPLEMENTATION_ERROR

semantic_status
= QUALIFIED
| QUALIFICATION_BLOCKED
| ACQUISITION_REJECTED
| NOT_REACHED

freeze_status
= FROZEN
| NOT_CREATED
| NOT_REACHED
```

Attack:

I_A reaches semantic `QUALIFICATION_BLOCKED`; I_B cannot load a required runtime dependency.

Result:

```text
I_A:
COMPLETED
QUALIFICATION_BLOCKED
NOT_CREATED

I_B:
ENVIRONMENT_BLOCKED
NOT_REACHED
NOT_REACHED
```

The two states cannot be collapsed into generic BLOCKED agreement.

Attack:

I_B throws an unhandled exception after partial interpretation.

Result:

```text
IMPLEMENTATION_ERROR
NOT_REACHED
NOT_REACHED
```

No semantic qualification outcome may be synthesized from the partial execution.

**RE-BREAK RESULT: SURVIVES.**

## 10.2 Re-break IAB-F02

Original defect:

`INDEPENDENT_DERIVATION_EVIDENCE_UNDERSPECIFIED`

Corrected candidate now requires:

```text
independent_derivation_attestation
semantic_source_provenance
no_copy_or_generated_from_other_path declaration
source_similarity_review_result
independent_stage_level_test_inventory
```

for project-owned semantic stages.

Attack:

I_A semantic implementation is copied into I_B and identifiers are mechanically renamed.

Result:

The path cannot satisfy the declared no-copy/independent-derivation provenance, and substantial semantic source similarity must be surfaced by review.

Unresolved provenance keeps I_B BLOCKED.

Attack:

Both paths contain the same normative constant such as `20`, `>IIIff`, anomaly IDs, or contract version strings.

Result:

This does not itself violate independence; the similarity review is required to distinguish common mandated literals from copied semantic control flow.

Attack:

Both teams independently derive the same simple branch from the same explicit contract rule.

Result:

Semantic equivalence alone is not treated as evidence of copying.

**RE-BREAK RESULT: SURVIVES.**

## 10.3 Re-break IAB-F03

Original defect:

`CROSS_PATH_INFORMATION_FLOW_PROOF_UNDERSPECIFIED`

Corrected candidate requires pre-seal isolated execution domains with explicit input/read boundaries.

Attack:

I_A writes `/tmp/reference_result.json`; I_B tries to read it.

Result:

The file is outside I_B's pre-seal common-input allowlist/private workspace and violates the isolation contract.

Attack:

I_A leaks expected retained count through an environment variable.

Result:

The variable is outside the explicit environment allowlist and violates the pre-seal boundary.

Attack:

I_B reaches I_A through IPC/network/shared cache.

Result:

The network/IPC/cache policy must deny or surface the channel before a valid isolation proof can exist.

Only after both result seals are created may both semantic results become visible to O.

**RE-BREAK RESULT: SURVIVES.**

## 10.4 Full attack-set re-break

```text
I_B imports I_A semantic helper directly             FORBIDDEN / SURVIVES
same project BI5 semantic decoder shared              FORBIDDEN / SURVIVES
same precomputed B candidates shared                  FORBIDDEN / SURVIVES
same precomputed A decisions shared                   FORBIDDEN / SURVIVES
same precomputed Q membership shared                  FORBIDDEN / SURVIVES
I_B consumes I_A F artifact                           FORBIDDEN / SURVIVES

separate files but copied semantic implementation     DERIVATION BLOCKED / SURVIVES
mechanical rename / generated port from I_A           DERIVATION BLOCKED / SURVIVES
common normative literals                             PERMITTED / SURVIVES
independent same contract-derived simple rule         PERMITTED / SURVIVES

I_A temp semantic file readable by I_B                ISOLATION VIOLATION / SURVIVES
semantic result leaked through environment            ISOLATION VIOLATION / SURVIVES
semantic result leaked through shared cache           ISOLATION VIOLATION / SURVIVES
semantic result leaked through IPC/network            ISOLATION VIOLATION / SURVIVES
other-path output visible before both seals            ISOLATION VIOLATION / SURVIVES

shared generic byte reader                            PERMITTED / SURVIVES
shared SHA-256 primitive                              PERMITTED / SURVIVES
shared JSON library                                   PERMITTED / SURVIVES
shared generic LZMA bytes→bytes primitive             PERMITTED / SURVIVES
shared semantic B/A/Q/F builder                       FORBIDDEN / SURVIVES

O called during construction                          FORBIDDEN / SURVIVES
same semantic result compared through two wrappers    FORBIDDEN + ISOLATED / SURVIVES
O receives both only after seals                      REQUIRED / SURVIVES

semantic Q BLOCKED vs environment BLOCKED             DISTINCT AXES / SURVIVES
implementation exception normalized to Q BLOCKED      FORBIDDEN / SURVIVES
both semantic Q BLOCKED                               TERMINAL AGREEMENT ONLY / SURVIVES
both environment BLOCKED                              NO SEMANTIC PASS / SURVIVES
QUALIFIED + implementation error                      EXECUTABLE FAILURE / SURVIVES

different traversal order                             NON-SEMANTIC / SURVIVES
parallel vs sequential                                NON-SEMANTIC / SURVIVES
cache hit vs cold parse                               NON-SEMANTIC IF VALIDATED / SURVIVES
stale cache under different determinants              FORBIDDEN / SURVIVES

hidden market-value filter in one path                DIVERGENCE/NON-CONFORMING / SURVIVES
timestamp sort as normative behavior                  FORBIDDEN / SURVIVES
strict duplicate collapse                             DIVERGENCE/NON-CONFORMING / SURVIVES
source→logical mapping mutation                       O DIVERGENCE / SURVIVES

one-sided I_A semantic mutant                         MUST BE DETECTED / SURVIVES
one-sided I_B semantic mutant                         MUST BE DETECTED / SURVIVES
fault injection affecting both paths                  NOT VALID ONE-SIDED EVIDENCE / SURVIVES

dynamic/import dependency omitted from manifest       QUALIFICATION BLOCKED / SURVIVES
executed source differs from manifest                 QUALIFICATION BLOCKED / SURVIVES
runtime read trace/isolation proof missing            QUALIFICATION BLOCKED / SURVIVES
independent derivation provenance missing             I_B BLOCKED / SURVIVES

implementation default supplies missing B/Q fact      FORBIDDEN / SURVIVES
filename supplies missing hour provenance             FORBIDDEN / SURVIVES
missing D component silently removed                  FORBIDDEN / SURVIVES

acquisition permission inferred                       FORBIDDEN / SURVIVES
real BI5 processing permission inferred               FORBIDDEN / SURVIVES
real backtest permission inferred                     FORBIDDEN / SURVIVES
```

No additional internal I_A/I_B boundary defect was demonstrated.

## 10.5 Final candidate state

```text
I_A/I_B implementation boundary
= PERSISTED
= ADVERSARIALLY BROKEN
= FAIL ON IAB-F01..IAB-F03
= MINIMALLY CORRECTED
= PERSISTED-HEAD RE-BROKEN
= NO NEW INTERNAL DEFECT DEMONSTRATED
```

Official gates remain:

```text
I_A = BLOCKED
I_B = BLOCKED
```

because no implementation code has been created or qualified, and the upstream concrete execution prerequisites remain BLOCKED.

The corrected boundary is internally stable enough to govern a future implementation block.

## 10.6 Important authorization boundary

This re-break does **not** authorize I_A/I_B implementation in this work block because the governed action was formalization only.

Before implementation begins, this formalization block must be durably closed through:

1. persisted re-break;
2. global reconciliation audit update;
3. durable backup;
4. Recovery Checkpoint update.

The next checkpoint must explicitly name the next governed action.

No acquisition, BI5 download, real BI5 processing or real backtest is authorized.
