# B-PE-04R — EVIDENCE PROPORTIONALITY / NECESSITY REVIEW — CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `acec807a5a92d1cb1b22182460e5e588b286b729`  
**Scope:** review/formalization only. No provider contact, no BI5 download, no real acquisition, no backtest, no paper/broker/live execution.

## 0. Decision question

Determine whether the unresolved provider-documentary dimensions:

```text
C08-D4 — USATECH legacy-hourly applicability
C08-D5 — target temporal/version continuity 2021–2026
```

must remain a hard pre-acquisition blocker requiring direct Dukascopy clarification, or whether their protected risk can be controlled more proportionally by a bounded empirical representation qualification.

Candidate outcomes:

```text
CONTINUE
SIMPLIFY
KEEP BLOCKED
```

B-PE-05 provider dispatch is not executed during this review.

---

## 1. What C08-D4 and C08-D5 actually protect

### C08-D4

Protected failure:

```text
generic Dukascopy legacy-hourly BI5 knowledge
→ silently assumed to apply to USATECHIDXUSD
→ acquisition manifest built for the wrong object family
→ missing/partial/wrong material enters research
```

### C08-D5

Protected failure:

```text
legacy hourly BI5 proven historically
→ silently assumed continuous through the 2021–2026 target market-data interval
→ component membership/path expectations become wrong after an unmodelled representation change
→ backtest sees omitted, duplicated or misinterpreted observations
```

These dimensions protect the **expected acquisition representation/component universe**, not trading logic.

---

## 2. Material counterexample

Construct an adversarial provider behavior:

```text
2021–2024:
  USATECH historical ticks exposed as hourly HHh_ticks.bi5

2025 onward:
  provider changes USATECH archival bucketization

legacy hourly locator remains partially compatible:
  HTTP success
  valid LZMA payload
  structurally decodable 20-byte records
  but only a subset / compatibility projection of the authoritative history
```

Project incorrectly assumes hourly continuity.

Consequences:

1. D creates an hourly manifest from the wrong representation premise.
2. Every expected hourly object can appear materialized.
3. B can decode each returned payload successfully.
4. Q can conserve every physical slot with no anomaly.
5. I_A and I_B can independently produce identical qualified universes.
6. O can report semantic equality.
7. The resulting universe can still omit authoritative ticks after the provider transition.

Therefore:

```text
D/Q/I_A/I_B agreement alone
≠ proof that the selected provider object family is complete/correct
```

This is the same common-premise limitation already recognized by the global reconciliation:

```text
two independent implementations agree
≠ external provider representation is correctly understood
```

So C08-D4/D5 protect a real risk.

---

## 3. Can existing controls detect the risk?

### D

Strength:

- missing declared component blocks;
- extra undeclared component blocks;
- ambiguous membership blocks;
- completeness evidence is mandatory.

Limitation:

D checks completeness **relative to its declared component universe**.

If the component-universe rule itself assumes the wrong hourly/daily representation, D can be internally complete and externally incomplete.

Verdict:

`PARTIAL DETECTION ONLY`.

### B / A / Q

Strength:

- decompression ambiguity blocks;
- malformed/residual/offset anomalies are explicit;
- physical accounting is conserved;
- incomplete/contradictory qualification package blocks.

Limitation:

A wrong representation can remain structurally valid.

Q V0.1 deliberately has:

```text
market_value_filter_policy = NONE_IN_Q_V0_1
```

and retains every valid B candidate occurrence absent consistency contradiction.

Therefore B/A/Q cannot independently prove provider-family applicability.

Verdict:

`PARTIAL DETECTION ONLY`.

### I_A / I_B / O

Strength:

- independent raw-payload decoding;
- independent anomaly/membership derivation;
- independent private F construction;
- semantic equality comparison;
- strong protection against implementation divergence.

Limitation:

Both implementations are bound to the same declared D/R/M/B/A/Q semantics.

A shared false representation premise can produce deterministic equality.

Verdict:

`DOES NOT FALSIFY SHARED EXTERNAL PREMISE`.

---

## 4. Why provider dispatch is disproportionate as the next action

A perfect B-PE-05/B-PE-04 provider answer could close C08-D4/D5 documentary uncertainty.

But:

1. it does not directly validate the exact bytes the project will actually acquire;
2. support may answer ambiguously or not at all;
3. it creates an external dependency and waiting loop;
4. even perfect Q1-Q3 answers do not by themselves close C01-C07 physical semantics;
5. the backtest's operational input is the **actual provider material acquired for the frozen historical dates**, not a forensic reconstruction of every historical server migration;
6. no explicit repository requirement was found that the backtest must reproduce the exact point-in-time archival representation as served on each historical date.

Important scope condition:

If the project later requires:

```text
point-in-time archival fidelity
=
reproduce the exact feed representation as it existed at historical time T
```

then provider/version-history evidence becomes materially necessary again.

That is not the currently declared objective.

---

## 5. More proportional control

Do not infer C08-D4/D5 away.

Instead introduce a separate pre-D empirical representation discriminator whose job is to test the external premise **before** a full acquisition manifest is trusted.

Required properties of that future discriminator:

```text
A. bounded real-data scope only
B. exact provider locator/status/headers/bytes/hash capture
C. no prior assumption that hourly is authoritative
D. probe all plausible provider object families allowed by evidence
E. explicit USATECHIDXUSD binding
F. dates stratified across the target interval
G. representation classification from observed material
H. detect simultaneous/coexisting locator families
I. compare coverage/cardinality across competing successful representations
J. fail closed if more than one materially different representation remains plausible
K. independently validate decoded time/price semantics
L. no backtest
M. no silent promotion to full D
```

This new discriminator is logically prior to D materialization.

It closes the hole that D/Q/I_A/I_B cannot close themselves:

```text
external representation premise
→ empirically discriminate
→ only then construct concrete D representation/component membership
→ B/A/Q
→ I_A/I_B
```

---

## 6. Empirical falsification examples

The future bounded discriminator must detect at minimum:

### E1 — hourly locator absent, daily locator present

```text
hourly expected family invalid
→ reject hourly premise
```

### E2 — both hourly and daily locators succeed

```text
compare semantic coverage
→ if equivalent alias can be proven, record alias relation
→ otherwise BLOCKED
```

### E3 — hourly payload structurally decodes but omits observations

```text
cross-family coverage/cardinality mismatch
→ BLOCKED
```

### E4 — bucket/path changed but physical payload semantics stayed constant

```text
do not falsely version B physical semantics solely because path changed
```

### E5 — physical semantics changed without path change

```text
candidate decoders/independent semantic checks disagree or plausibility invariants fail
→ BLOCKED
```

### E6 — USATECH differs from generic provider rule

```text
instrument-specific observed representation wins over generic inference
```

---

## 7. Information-cost comparison

### Route A — provider clarification

Information gained:

```text
historical/provider documentary authority
transition narrative
USATECH scope statement
```

Weakness:

```text
may not describe exact bytes currently served
may be incomplete
does not close all C01-C07
external dependency
```

### Route B — bounded empirical qualification

Information gained:

```text
actual provider objects currently retrievable
actual USATECH applicability
actual target-date behavior
actual payload bytes
actual coverage relationship between candidate object families
direct falsification of operational acquisition premise
```

Weakness:

```text
does not prove historical provider policy
bounded sample can miss epoch-local transitions
requires carefully stratified probe design
requires future explicit real-data authorization
```

For the currently declared backtest objective, Route B has higher direct decision value.

---

## 8. Scope of simplification

This review does **not** declare:

```text
C08-D4 = PASS
C08-D5 = PASS
BPE-C08 = PASS
B = PASS
```

They remain documentary BLOCKED under B-PE-01 V0.1.

The simplification is narrower:

```text
C08-D4/D5 documentary BLOCKED
≠ mandatory reason to contact provider before any bounded empirical probe
```

B-PE-01 is not silently weakened.

Before any later global B promotion based on empirical evidence, governance must explicitly decide whether to:

```text
version/supersede B-PE-01 sufficiency rules
or
retain provider-primary documentary PASS as mandatory
```

No hidden threshold relaxation is allowed.

---

## 9. Candidate decision

```text
B-PE-04R PROPORTIONALITY DECISION = SIMPLIFY
```

Meaning:

```text
B-PE-05 provider dispatch = DO NOT EXECUTE NOW

do not KEEP BLOCKED solely waiting for provider clarification

replace immediate provider-contact path with
a formalized bounded empirical representation-discrimination contract
```

Provider clarification remains an optional fallback if empirical discrimination is ambiguous, contradictory or unable to establish the needed operational scope.

---

## 10. Proposed next governed action

Open only:

```text
B-ERD-01 — bounded empirical representation-discrimination contract
```

Formalization only.

Scope:

```text
fresh HEAD
→ define exact empirical hypotheses
→ define minimal stratified USATECH target-date sample
→ define candidate hourly/daily locator families without choosing a winner
→ define exact raw response/provenance capture
→ define representation/coverage comparison
→ define independent semantic plausibility checks
→ define PASS / FAIL / BLOCKED
→ adversarially break the contract
→ persisted-HEAD re-break
→ audit + backup + checkpoint
→ STOP
```

Still prohibited in B-ERD-01 formalization:

```text
real BI5 download
real BI5 processing
real acquisition
backtest
paper/broker/live
provider contact
```

A later bounded empirical execution would require its own explicit authorization.

---

## 11. Candidate status

```text
B-PE-04R = CANDIDATE / NOT YET ADVERSARIALLY RE-BROKEN
B-PE-05 = NOT EXECUTED
C08-D4 = BLOCKED
C08-D5 = BLOCKED
B global gate = BLOCKED
```
