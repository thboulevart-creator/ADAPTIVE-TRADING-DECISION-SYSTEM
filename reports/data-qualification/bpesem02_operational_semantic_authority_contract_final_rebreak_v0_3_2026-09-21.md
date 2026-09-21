# B-PE-SEM-02 — FINAL PERSISTED-HEAD RE-BREAK OF V0.3 COMPOSITE

**Date:** 2026-09-21  
**Repository:** thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM  
**Branch:** integration/system-v1  
**Persisted corrected HEAD attacked:** 5c0eaf700cb2b550ed9b4efbb0b4e42b743af4ef

Persisted composite re-read from GitHub:

~~~text
V0.1 candidate blob =
092aae41821afb69d7fb84da095d1c8c0bfacb3d

initial adversarial-break blob =
f18a6bad6cb17e75800dbd58d69d5f721280d8cd

V0.2 correction blob =
09f13707a51b4957cf28e4ae48b2e52e90e96343

V0.2 persisted-head re-break blob =
26517003233b48d7c7ff35a5458b6749add516e9

V0.3 correction blob =
1181bdf09a4310d514e3a096f76843cfc2a7bf97
~~~

No conversational reconstruction is authority for this re-break.

## 1. Re-break status of R01-R04

The direct V0.2 residual exploits are closed:

~~~text
R01 basis weakening / arbitrary semantic deferral
  -> direct exploit closed by DimensionAuthorityBasisRegister
     and signedness-only conditional-semantic exception

R02 warmup/calendar scope drift
  -> direct exploit closed by exact session-calendar and IntervalInventory binding

R03 self-selected reviewed_evidence_ids
  -> materially improved by SemanticEvidenceReviewUniverse

R04 implicit scope/lineage digest domains
  -> closed by exact formulas
~~~

Extended attacks still demonstrate four material residual/new defects.

## 2. BPESEM02-R05 — REVIEW-UNIVERSE BASELINE IS STILL SELF-DECLARED

SemanticEvidenceReviewUniverse contains:

~~~text
mandatory_inherited_evidence_refs[]
~~~

but the object itself supplies that list.

The contract names BPE02, B-PE-SEM-01 and B-ERD-02 when reused, but it does not bind a complete governed evidence baseline for all already-versioned material scope/semantic evidence.

Concrete already-versioned example:

~~~text
B-PE-03 final adjudication / evidence bundle
adjudication seal =
90c240c2aea78fed5fd1509daecf390fd439b38376e3c3a4fc4368d19d6af2be

evidence-set digest =
5cdf41debc110d5b5de0cedd552643300e75b2a03b305cfb9220f18c62fdf30c
~~~

B-PE-03 established provider-primary legacy-hourly family existence and preserved explicit target-epoch continuity limitations:

~~~text
C08-D4 = BLOCKED
C08-D5 = BLOCKED
no provider proof of legacy-hourly continuity through 2021-2026
~~~

Although B-PE-03 did not reopen C01-C07 documentary dimensions, its scope/version evidence is materially relevant to any C01-C07 SemanticScopeApplicabilityDecision.

Exploit:

~~~text
future review-universe object
-> populate mandatory_inherited_evidence_refs without B-PE-03
-> claim complete inherited review
-> scope applicability is evaluated without an already-governed
   continuity limitation
~~~

Rule text saying that existing governed evidence cannot be silently omitted is not enough when the completeness universe is supplied by the same future adjudicator.

Required correction:

~~~text
GovernedSemanticEvidenceBaseline
or equivalent immutable baseline register

-> exact baseline HEAD/tree identity
-> exact mandatory governed adjudication/evidence lineages
-> exact inclusion/exclusion policy
-> SemanticEvidenceReviewUniverse must bind baseline ID + digest
-> missing baseline member = BLOCKED
~~~

At minimum the baseline must preserve relevant lineages from:

~~~text
BPE02
BPE03
B-PE-01R boundary
B-PE-SEM-01
current B-FIQ semantic-block state
B-ERD-02 when reused
~~~

plus any current-adjudication evidence.

## 3. BPESEM02-R06 — REVIEW EXCLUSION CAN LAUNDER A KNOWN MATERIAL ALTERNATIVE

V0.3 permits ReviewUniverseExclusionDecision dispositions including:

~~~text
INADMISSIBLE
WRONG_SCOPE
HISTORICAL_ONLY
COMMON_LINEAGE
NONDECISIVE
BLOCKED_UNRESOLVED
~~~

but the exclusion is not defined as a pure projection of already-sealed source admissibility, scope and lineage decisions.

Worse, KnownMaterialAlternativeRegistry is required to derive candidate interpretations from the "effective review universe".

Exploit:

~~~text
material conflicting source is inherited
-> create exclusion disposition INADMISSIBLE or NONDECISIVE
   without binding the exact controlling source/scope/lineage decision
-> remove it from effective review evidence
-> competing interpretation disappears from KnownMaterialAlternativeRegistry
-> one remaining hypothesis survives
~~~

This can convert evidentiary weakness into hypothesis disappearance.

Required correction:

Create two distinct projections:

~~~text
VISIBILITY_UNIVERSE
  = all governed material evidence/interpretations that must remain visible
    to contradiction and known-alternative analysis

POSITIVE_AUTHORITY_UNIVERSE
  = only evidence currently admissible for positive PASS support
~~~

A source can have zero positive authority while its material interpretation remains visible.

An exclusion from VISIBILITY_UNIVERSE is allowed only when a sealed controlling decision positively establishes that it is non-target / non-material, not merely non-authoritative.

ReviewUniverseExclusionDecision must bind the exact controlling:

~~~text
OperationalSemanticEvidenceAdmissibilityDecision
SemanticScopeApplicabilityDecision when applicable
OperationalSemanticLineageResolution when applicable
~~~

and cannot contradict those decisions.

## 4. BPESEM02-R07 — CURRENT-AUTHORITY FRESHNESS DEPENDS ON REOPEN EVENT EXISTENCE

Current authority currently requires:

~~~text
no OPEN material reopen event exists
~~~

But a new material artifact can be versioned after adjudication without anyone creating the reopen event.

Exploit:

~~~text
semantic adjudication PASS at HEAD H0
-> later commit H1 introduces materially contradictory target evidence
-> no OperationalSemanticReopenEvent is persisted
-> current-authority predicate sees "no OPEN event"
-> stale H0 PASS remains reusable
~~~

This is a reopen-detection gap, not merely an event-integrity gap.

Required correction:

A use-time current-authority freshness control must compare the adjudication evidence horizon to the consumer HEAD.

At minimum:

~~~text
CurrentAuthorityEvidenceDeltaReview
  prior adjudication cutoff/baseline
  consumer HEAD
  descendant/history relation
  changed/new governed semantic-evidence artifacts
  relevance triage
  resulting reopen events or explicit non-material dispositions
  PASS / BLOCKED
~~~

Any unreviewed potentially relevant evidence after the adjudication cutoff:

~~~text
current authority = BLOCKED
~~~

Non-descendant/re-written evidence history:

~~~text
current authority = BLOCKED
~~~

Historical PASS remains immutable but is not current promotion authority until the delta is reviewed.

## 5. BPESEM02-R08 — SEMANTIC SCOPE APPLICABILITY CAN BE CONFUSED WITH C08 REPRESENTATION PRESENCE

The contract correctly preserves that B-PE-01R C08 supersession cannot authorize C01-C07.

The reverse boundary is not yet equally explicit.

SemanticScopeApplicabilityDecision requires the semantic authority to cover the target K1 regime and complete intended epoch.

That can be read as either:

~~~text
A. conditional semantic applicability:
   IF an object is classified as K1 in the target domain,
   these qualified semantic rules govern it

or

B. representation-presence authority:
   K1 is actually the provider representation present/served
   for every relevant interval in that epoch
~~~

B is the later C08/FULL_INTERVAL problem.

Exploit/circularity:

~~~text
BPE-SEM C01-C07 scope PASS
-> treated as proof K1 applies throughout 2021-2026
-> bypass C08-D4-OP / C08-D5-OP / FULL_INTERVAL
~~~

or inversely:

~~~text
C01-C07 semantic authority is made to require FULL_INTERVAL K1 continuity
before FULL_INTERVAL is authorized
-> circular gate
~~~

Required correction:

Formalize two separate predicates:

~~~text
SEMANTIC_RULE_SCOPE_APPLICABILITY
  = conditional applicability of the semantic rule to an object already
    independently classified as the target representation/regime

REPRESENTATION_PRESENCE_CONTINUITY
  = whether the provider actually serves/uses that representation across
    the governed interval
  = outside B-PE-SEM-02
  = governed later by C08/FULL_INTERVAL
~~~

A BPE-SEM C01-C07 PASS must never satisfy, imply or contribute positive authority to C08-D4-OP/C08-D5-OP except as a prerequisite semantic rule consumed by the later FULL_INTERVAL adjudication.

## 6. Attacks that remain fail-closed

No material defect was demonstrated for:

~~~text
registered dimension omission
DimensionAuthorityBasis weakening after V0.3
semantic meaning deferred outside signedness exception
calendar identity substitution
IntervalInventory substitution
post-hoc B-ERD-02 decisive discrimination without eligibility record
digest/seal ambiguity already corrected for prior objects
lineage omission in positive semantic authority
execution-obligation dropping
I_A/I_B/F/O self-authority
CFD 0.01 -> raw /1000 inference
positive spread -> ask/bid authority
offset range -> timestamp semantic authority
volume removal
signedness high-bit-one silent acceptance
B-FIQ-02 in-place reinterpretation
~~~

## 7. V0.3 final re-break verdict

~~~text
B-PE-SEM-02 V0.3 CORRECTED COMPOSITE = FAIL

demonstrated material residual/new defects =
R05
R06
R07
R08
~~~

No semantic proposition is promoted.

Required next movement:

~~~text
minimal correction V0.4 for R05-R08 only
-> persist
-> final persisted-head re-break
-> PASS / FAIL / BLOCKED
~~~

Still prohibited:

~~~text
provider contact
provider BI5 GET
new semantic-discrimination execution
FULL_INTERVAL execution
D materialization
backtest
paper/broker/live
~~~

STOP.
