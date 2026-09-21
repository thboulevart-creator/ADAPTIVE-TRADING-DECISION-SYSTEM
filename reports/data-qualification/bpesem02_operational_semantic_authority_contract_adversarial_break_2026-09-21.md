# B-PE-SEM-02 — OPERATIONAL SEMANTIC AUTHORITY CONTRACT — ADVERSARIAL BREAK

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Candidate commit attacked:** b24b85740ed1d2a060ec3a9a2a254dbe332edccc  
**Candidate blob:** 092aae41821afb69d7fb84da095d1c8c0bfacb3d

## 1. Attack objective

Attack the persisted V0.1 candidate for routes that could create a formally valid but semantically weak operational PASS.

The attack does not evaluate whether any native-BI5 proposition is actually true.

No provider contact, provider GET, semantic execution, FULL_INTERVAL execution, D materialization or backtest was performed.

## 2. Candidate verdict

~~~text
B-PE-SEM-02 V0.1 CANDIDATE = FAIL
~~~

Seven material contract defects are demonstrated.

## 3. Demonstrated defects

### BPESEM02-F01 — CLAIM/DIMENSION REGISTER IS NOT CRYPTOGRAPHICALLY CLOSED

The candidate defines the required claim/dimension register in prose, but a future
OperationalSemanticRuleAdjudication carries its own claim_adjudications[].mandatory_dimension_ids[]
without binding an immutable register identity/digest.

Exploit:

~~~text
future adjudication
-> omit C06-D4-OP from mandatory_dimension_ids
-> mark remaining C06 dimensions PASS
-> claim BPE-SEM-C06-OP PASS
~~~

The object could satisfy its own schema while silently weakening this contract.

Required correction:

~~~text
persist/fix a ClaimDimensionRegister identity
bind exact mandatory dimensions and dimension classes
hash it
require exact register_id + digest in every adjudication
derive claim status from the bound register, never from adjudicator-supplied lists
~~~

### BPESEM02-F02 — SOURCE ADMISSIBILITY AND EVIDENCE SUFFICIENCY ARE UNDER-SPECIFIED

OperationalSemanticEvidenceRecord contains descriptive status fields, but there is no separately sealed source-level admissibility decision.

Dimension PASS then requires only that required evidence/anchor/hypothesis/rule objects are admissible without a closed minimum authority basis per dimension class.

Exploit:

~~~text
single non-project implementation
+ self-described provenance
+ one anchor manifest
-> adjudicator labels it sufficient
-> semantic dimension PASS
~~~

even when its semantic meaning is not independently established strongly enough for the proposition.

Required correction:

~~~text
OperationalSemanticEvidenceAdmissibilityDecision
+
class-specific DimensionAuthorityBasis
~~~

At minimum:

~~~text
PHYSICAL_HYPOTHESIS
  -> predeclared hypotheses/discriminators + admissible exact evidence;
     unique survival under authorized discriminator(s);
     compatibility never upgraded to unstated meaning

SEMANTIC_ANCHOR
  -> at least one admissible anchor whose independently established
     semantic-source lineage entails the exact proposition and exact scope

CONDITIONAL_RULE
  -> rule proof/identity + exact affected fields + fail-closed obligation

PREREQUISITE_CLOSURE
  -> all enumerated prerequisite authority identities current PASS

SCOPE_APPLICABILITY
  -> separately closed applicability proof
~~~

No source may self-authorize its admissibility.

### BPESEM02-F03 — TEMPORAL / REGIME APPLICABILITY IS NOT CLOSED FOR EVERY DIMENSION

The candidate scope contains a free-text temporal_applicability_statement, while exact applicability is made explicit mainly for C06.

Nothing forces every PASS dimension to prove that its authority applies to:

~~~text
DUKASCOPY
USATECHIDXUSD
K1_LEGACY_HOURLY_TICK_BI5
the exact governed warmup + evaluation epoch
~~~

Exploit:

~~~text
current daily provider source
-> supports 20-byte or timestamp claim
-> dimension scope_mapping says target
-> historical K1 dimension PASS
~~~

without an exact continuity/applicability proof.

Required correction:

~~~text
OperationalSemanticScopeSignature must bind exact machine-readable
provider/instrument/regime/object-family/epoch identities
+
every dimension adjudication must bind a SemanticScopeApplicabilityDecision
for that exact scope
+
any uncovered epoch/regime segment => BLOCKED
~~~

The scope must bind the exact execution-window freeze identity and exact representation-regime identity or an equally strict successor identity.

### BPESEM02-F04 — B-ERD-02 REUSE CAN BECOME RETROSPECTIVE HYPOTHESIS LEAKAGE

Section 7 requires a SemanticHypothesisSet to be sealed before the observation it discriminates.

Section 10 nevertheless allows the already-observed BERD02-GHA-35533153289-1 to be reused as bounded hypothesis-discrimination evidence.

The contract does not require proof that the exact relevant hypotheses and discriminator semantics were fixed before that historical observation.

The persisted B-ERD-02 ProbePlan fixed the windows and representation candidates, while the runner source fixed concrete diagnostics such as FORMAT_ALONE and parsing behavior. That is useful evidence, but it does not automatically prove that every future semantic hypothesis set was prospectively precommitted.

Exploit:

~~~text
observe B-ERD-02 bytes/results
-> design a new hypothesis set that the known results uniquely satisfy
-> cite B-ERD-02 as decisive discriminator
~~~

Required correction:

~~~text
HistoricalObservationEligibilityRecord
~~~

must prove, for each decisive reuse:

~~~text
observation identity
pre-observation commit/time
exact hypothesis/discriminator identity already fixed before observation
relationship between historical discriminator and current dimension
no post-hoc broadening
~~~

If this cannot be proven, historical evidence may be:

~~~text
background / compatibility / contradiction evidence
~~~

but not decisive unique-hypothesis evidence.

### BPESEM02-F05 — KNOWN MATERIAL ALTERNATIVES CAN BE OMITTED FROM A HYPOTHESIS SET

SemanticHypothesisSet contains completeness_rationale and an open-world rule, but does not require all already-known material alternatives to be included before sealing.

Exploit:

~~~text
known H1 and H2 exist
-> seal only H1
-> H1 is the only surviving registered hypothesis
-> dimension becomes eligible for PASS
~~~

The later open-world rule only reacts when an unregistered interpretation is discovered, not when it was already known and omitted.

Required correction:

~~~text
KnownMaterialAlternativeRegistry
~~~

or equivalent closed field binding:

~~~text
all known material alternatives from the admissible evidence review
included_hypothesis_ids
excluded_candidate_ids + explicit non-material rationale
review cut-off identity
~~~

A known material alternative omitted without a qualified non-materiality decision makes the hypothesis set BLOCKED.

### BPESEM02-F06 — DIGEST / SEAL DOMAINS ARE NOT EXACTLY DEFINED

The candidate gives canonical JSON rules and names several digests, but does not define the exact projection for:

~~~text
evidence_set_digest
anchor_set_digest
hypothesis_set_digest
rule_set_digest
adjudication_seal
reopen_event_seal
~~~

Nor does it require the set digests to bind the source-level admissibility decisions that should control evidentiary weight.

Exploit:

Two implementations can both claim conformance while hashing different member fields, or an adjudication can hash evidence IDs but omit their decision seals/content hashes.

Required correction:

Define the exact canonical member projection and exact self-seal exclusion rule for every digest/seal.

### BPESEM02-F07 — EXECUTION OBLIGATIONS CAN BE DROPPED BETWEEN DIMENSION PASS AND B-FIQ HANDOFF

A dimension adjudication can contain execution_obligations[] while the overall object separately contains execution_obligation_set[].

No exact derivation/bijection is required.

B-FIQ-02R is instructed to copy only explicitly authorized obligations.

Exploit:

~~~text
C03-D3-OP PASS under SIGNEDNESS_EQUIVALENCE_RULE_V0_1
dimension record contains SIGNEDNESS_HIGH_BIT_ZERO_REQUIRED
overall execution_obligation_set omits it
-> B-FIQ-02R copies no signedness check
~~~

Required correction:

~~~text
every obligation has a stable obligation_id
global execution_obligation_set =
exact canonical union of all dimension execution obligations
no duplicates / no omissions / no orphans
obligation_set_digest required
B-FIQ-02R must bind exact obligation_set_digest
~~~

## 4. Attacks that did NOT demonstrate defects

The following candidate protections held:

~~~text
C08 empirical supersession cannot directly authorize C01-C07
I_A/I_B/F/O cannot be semantic anchors
current CFD point value 0.01 is not /1000 authority
positive spread is not ask/bid authority
timestamp range is not timestamp semantic authority
volume cannot be removed from the current logical model
signedness high-bit-one remains fail-closed
current B-FIQ-02 cannot be silently reinterpreted
historical PASS alone is not current authority
~~~

## 5. Required correction boundary

Correction must address only F01-F07.

No new provider evidence may be collected and no semantic proposition may be promoted.

After correction:

~~~text
persist correction
-> re-read persisted candidate + break + correction
-> final persisted-HEAD adversarial re-break
-> PASS / FAIL / BLOCKED
~~~

STOP.
