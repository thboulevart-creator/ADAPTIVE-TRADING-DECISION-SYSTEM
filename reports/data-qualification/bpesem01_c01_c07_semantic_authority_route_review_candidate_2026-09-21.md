# B-PE-SEM-01 — C01-C07 PROVIDER-SEMANTIC AUTHORITY NECESSITY / CLOSURE-ROUTE REVIEW — CANDIDATE

**Date:** 2026-09-21  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting live HEAD:** `bf070aa9fc8fde9793430a2deea1757f103a8763`  
**Status:** PERSISTED FORMALIZATION CANDIDATE — NOT YET QUALIFIED

## 0. Permission boundary

This block is a formalization/review block only.

Explicitly prohibited here:

```text
provider contact
provider BI5 GET
FULL_INTERVAL execution
D materialization
real Q/F/Q-RM-12 execution
backtest
paper/broker/live
```

No current C01-C07 BLOCKED adjudication is rewritten by this candidate.

## 1. Inputs actually reviewed

Current-authority inputs:

```text
B-PE-01 V0.1 provider-sensitive semantics contract
BPE02-ADJ-2026-09-20-V0_2
B-PE-01R PASS / VERSIONED_EMPIRICAL_SUPERSESSION
B-FIQ-01 V0.2 corrected contract
B-FIQ-02 SemanticInvariantManifest
B-FIQ-02 final persisted-head re-break / closeout
I_A / I_B current parser semantics
O current semantic-universe comparison semantics
```

Relevant exact current identities include:

```text
BPE02 adjudication seal
d27771bc8c2023571b4fbbe66238dbc28b29ca69949a1db114480346f1c90a76

B-FIQ-02 SemanticInvariantManifest seal
e0181475e7b0213eba625182b3556c39b2a4790b5491173de3dec92e60ca9f6b

B-FIQ-02 package final re-break report blob
806bc101b8c24ba121e04c66ed159f80477f300f
```

Current state remains:

```text
BPE-C01..C07 = BLOCKED
decisive_invariants = []
B-FIQ-02 pre-execution eligibility = BLOCKED
FULL_INTERVAL execution = NOT AUTHORIZED / NOT RUN
```

## 2. Governing separations

The review preserves all of the following:

```text
provider normative statement
!=
provider-served empirical bytes

provider-served empirical bytes
!=
semantic meaning by themselves

two decoder agreement
!=
independent semantic truth

plausible price/time/volume values
!=
semantic proof

operational representation authority
!=
documentary provider-primary authority

C08 operational supersession
!=
automatic C01-C07 supersession
```

B-PE-01 V0.1 and BPE02 remain the documentary/provider-truth axis.

A future operational successor, if justified, must be separately versioned and must not retroactively relabel BPE02 as PASS.

## 3. Exact C01-C07 necessity review

The question is not whether the historical B-PE-01 dimensions were reasonable. The question is which semantic facts are actually required for the operational FULL_INTERVAL path, which parts are evidence-method requirements rather than semantic content, and which ambiguity can be converted into a fail-closed empirical condition.

### C01 — compression / envelope

Current dimensions:

```text
C01-D1 LZMA family
C01-D2 LZMA-Alone envelope
C01-D3 stream/wrapper admission semantics
C01-D4 decompressed output role
```

Operational assessment:

```text
D1 REQUIRED
D2 REQUIRED
D3 REQUIRED
D4 REQUIRED
```

Reason:

The parser cannot reach physical framing without an exact admissible decompression/envelope rule. However the future operational proposition need only establish the exact accepted representation behavior for the target provider-served object family; it must not claim that Dukascopy normatively names that behavior unless provider-primary documentation actually proves it.

Direct decompression success under one preselected implementation is insufficient. A successor must predeclare competing envelope hypotheses and fail closed when more than one materially distinct hypothesis remains compatible.

### C02 — physical framing

Current dimensions:

```text
C02-D1 20-byte slot width
C02-D2 frame origin byte zero
C02-D3 residual/trailing-byte semantics
C02-D4 delimiter/header semantics
```

Operational assessment:

```text
D1 REQUIRED
D2 REQUIRED
D3 REQUIRED
D4 REQUIRED
```

Reason:

All four determine record boundaries and therefore Q membership, anomaly classification and the frozen logical universe.

### C03 — primitive field layout

Current dimensions:

```text
C03-D1 big-endian
C03-D2 five-field order
C03-D3 first three fields unsigned uint32
C03-D4 final two fields IEEE-754 binary32
```

Operational assessment:

```text
D1 REQUIRED
D2 REQUIRED
D4 REQUIRED

D3 NORMATIVE SIGNEDNESS LABEL IS NOT ALWAYS OPERATIONALLY DECISIVE
but the numeric interpretation domain IS REQUIRED
```

A separately versioned operational successor may replace the normative signed/unsigned label by a stricter behavioral condition:

```text
for every accepted first/second/third 32-bit field whose semantic use
would differ between signed and unsigned interpretations,
the high bit must be zero;
otherwise qualification is BLOCKED
```

When the high bit is zero, signed and unsigned 32-bit interpretations are numerically identical. This does not prove provider-declared signedness; it proves behavioral equivalence for the exact qualified byte domain.

No sampled-probe extrapolation is allowed. The condition must be checked on every accepted record of the qualified capture set before the operational successor can authorize downstream use.

### C04 — timestamp offset meaning

Current dimensions:

```text
C04-D1 millisecond unit
C04-D2 represented-hour origin
C04-D3 UTC/provider-equivalent hour basis
C04-D4 valid offset domain/range
```

Operational assessment:

```text
D1 REQUIRED
D2 REQUIRED
D3 REQUIRED
D4 REQUIRED
```

Reason:

These dimensions determine event timestamps and therefore ordering, session membership, warmup/evaluation allocation and downstream research chronology.

Range plausibility alone cannot prove the unit/origin/basis.

A future successor therefore requires at least one non-circular semantic anchor capable of discriminating the timestamp interpretation, plus complete per-record domain checking.

### C05 — ask/bid raw roles

Current dimensions:

```text
C05-D1 field 2/3 roles = ask then bid
C05-D2 unsigned raw-price interpretation
C05-D3 provider-owned prerequisite metadata before conversion
```

Operational assessment:

```text
D1 REQUIRED

D2 same behavioral-equivalence treatment as C03-D3:
   exact signedness label need not be asserted when high bit = 0
   on every accepted target-domain price field

D3 AS WRITTEN is evidence-method coupling, not independent semantic content
```

The necessary operational content is not “provider-owned metadata must exist”. The necessary content is that the raw price fields can be converted under a separately qualified instrument/scale binding without unresolved prerequisite semantics.

Ask>=bid plausibility alone is not sufficient proof of D1.

### C06 — USATECHIDXUSD price scaling

Current dimensions:

```text
C06-D1 USATECH applicability
C06-D2 divisor /1000
C06-D3 scale authority = exact provider rule/metadata source
C06-D4 temporal/version applicability
```

Operational assessment:

```text
D1 REQUIRED
D2 REQUIRED
D4 REQUIRED

D3 AS WRITTEN is an evidence-authority requirement, not the scale fact itself
```

For the operational path, the semantic proposition that matters is:

```text
for the exact target instrument and qualified representation regime,
logical price = raw price / 1000
```

A future successor may prove that proposition through a separately qualified non-circular semantic calibration route rather than by silently relabeling current CFD point-value metadata as raw-BI5 scale evidence.

The current Dukascopy CFD “0.01 point value” observation is explicitly insufficient to prove the BI5 raw divisor.

### C07 — volume primitive / role / representation transform

Current dimensions:

```text
C07-D1 ask-volume then bid-volume roles
C07-D2 IEEE-754 binary32 primitive
C07-D3 representation-level transform/scale
```

Operational assessment under the CURRENT logical record model:

```text
D1 REQUIRED
D2 REQUIRED
D3 REQUIRED
```

Reason:

I_A and I_B currently emit ask_volume and bid_volume into each logical payload, and O compares the complete logical payload. Therefore this review cannot declare volume semantics irrelevant without changing the normative record model / B / Q / F / O chain.

Economic interpretation such as lots/contracts/notional remains unnecessary unless it changes decoding, Q membership or downstream governed research semantics.

## 4. What may be empirically qualified versus what needs an external semantic anchor

### 4.1 Empirically discriminable physical compatibility

Potentially qualifiable from exact provider-origin bytes under predeclared competing hypotheses:

```text
compression/envelope acceptance
physical frame width/origin/residual behavior
byte order
field count/order at the physical level
binary32 decodability
per-record offset admissibility
per-record signed/unsigned behavioral equivalence condition
```

This evidence can establish operational compatibility only if candidate hypotheses are frozen before observation and ambiguous multi-hypothesis compatibility remains BLOCKED.

### 4.2 Semantic-anchor-required dimensions

Cannot be promoted merely from two project decoders agreeing:

```text
timestamp unit/origin/time basis
ask versus bid semantic role
USATECH raw-price scale
volume semantic role/order
volume representation transform/scale
```

These require a non-circular anchor independent of the candidate project interpretation.

Acceptable future anchor classes must be defined prospectively. Examples may include provider-direct alternate representations or exact version-pinned non-project fixtures/reference implementations whose expected meaning is independently established.

No anchor may be generated from I_A, I_B, F, O or another transformation of the same candidate decoder output.

## 5. Candidate closure-route comparison

### Route A — KEEP_PROVIDER_PRIMARY only

Effect:

```text
preserves B-PE-01 exactly
C01-C07 remain BLOCKED until qualifying provider-primary evidence is found
B-FIQ pre-execution remains BLOCKED
```

This is semantically strongest but is not the only logically legitimate operational route because some B-PE-01 dimensions encode evidence-method requirements rather than irreducible semantic facts.

### Route B — silently reuse B-PE-01R C08 supersession

```text
REJECTED
```

Reason:

B-PE-01R explicitly excludes C01-C07 from its EC-P3 replacement authority.

### Route C — remove C01-C07 broadly because K1 probes decode

```text
REJECTED
```

Reason:

bounded compatibility and two-decoder agreement do not establish timestamp, side, price-scale or volume semantics.

### Route D — separately versioned operational semantic successor

```text
CANDIDATE SELECTED
```

The successor must preserve:

```text
B-PE-01/BPE02 documentary axis unchanged
no retroactive PASS
no project self-authorization
no sampled-probe extrapolation
no common-premise two-decoder promotion
no plausibility-as-semantics
positive contradiction fail-closed
exact target/instrument/regime binding
current-authority / reopen semantics
```

It may replace evidence-method-specific dimensions with operational propositions only when the replacement is at least as fail-closed for the intended historical-backtest use.

## 6. Candidate successor shape

Proposed next contract family:

```text
B-PE-SEM-02 —
OPERATIONAL NATIVE-BI5 SEMANTIC AUTHORITY CONTRACT
```

The contract should create a new authority axis, e.g.:

```text
BPE-SEM-C01-OP
...
BPE-SEM-C07-OP
```

These are NOT aliases for BPE-C01..C07.

Required evidence classes should distinguish:

```text
physical hypothesis discrimination evidence
semantic anchor evidence
target-domain behavioral-equivalence evidence
contradiction evidence
```

Required fail-closed rules include at least:

```text
multiple surviving material hypotheses -> BLOCKED
semantic anchor lineage unresolved -> BLOCKED
anchor derived from project decoder -> REJECTED
signedness high-bit observed -> BLOCKED until exact signedness is resolved
price scale ambiguity -> BLOCKED
timestamp interpretation ambiguity -> BLOCKED
ask/bid role ambiguity -> BLOCKED
volume role/scale ambiguity under current logical model -> BLOCKED
material contradiction -> reopen / BLOCKED
```

## 7. Relationship to B-FIQ

Even if B-PE-SEM-02 later qualifies an operational semantic adjudication, the existing B-FIQ-02 SemanticInvariantManifest does not mutate automatically.

A later governed refresh must:

```text
bind the exact operational semantic adjudication ID + seal
re-materialize SemanticInvariantManifest
rebuild any authority-scope tuple whose semantic authority identity changes
re-break the pre-execution package on the persisted refreshed HEAD
```

No current B-FIQ execution authorization follows from this review.

## 8. Candidate decision

```text
B-PE-SEM-01 review candidate =
SEPARATELY_VERSIONED_OPERATIONAL_SEMANTIC_SUCCESSOR

documentary BPE-C01..C07 =
UNCHANGED / BLOCKED

operational C01-C07 authority =
NOT YET CREATED

B-FIQ-02 pre-execution eligibility =
BLOCKED
```

## 9. Mandatory adversarial attacks before qualification

Attack at minimum:

```text
F01 signedness ambiguity hidden by sampled low values
F02 semantic anchor secretly derived from project decoder/common lineage
F03 price divisor inferred from CFD point value or visual plausibility
F04 volume semantics improperly removed despite current logical payload
F05 LZMA-Alone selected because both project decoders share the premise
F06 successor mistaken for automatic authority in existing B-FIQ scope
F07 timestamp semantics inferred from offset range only
F08 ask/bid orientation inferred from spread sign only
```

No final route PASS may be issued before persisted-head adversarial re-break.

## 10. Candidate next action if this review qualifies

Only after B-PE-SEM-01 final PASS:

```text
B-PE-SEM-02 —
formalize the separately versioned operational semantic authority contract
only

no provider contact
no provider GET
no semantic execution
no FULL_INTERVAL execution
```

STOP.
