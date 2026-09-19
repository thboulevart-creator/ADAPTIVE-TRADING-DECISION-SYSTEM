# D + R + M — ADVERSARIAL BREAK OF FIRST PERSISTED CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Candidate commit under attack:** `ed1a55047df1d3402fa35ef19f3a662070d590db`  
**Candidate artifact:** `reports/data-qualification/drm_first_concrete_candidate_formalization_2026-09-19.md`

No acquisition, network access, BI5 download, dataset processing or backtest occurred.

## 1. Attack rule

The candidate is attacked against:

- Q-RM-01 RB-A;
- Q-RM-02 cardinality;
- Q-RM-04 malformed/ambiguous fail-closed semantics;
- Q-RM-05 acquisition-domain semantics;
- Q-RM-06 binding/versioning separation;
- Q-RM-08 concrete declaration requirements;
- acquisition-scoped observation identity;
- current frozen execution-window evidence;
- Momentum V1 20-H1-bar horizon.

A candidate defect is recorded only when the candidate itself allows two incompatible conforming interpretations or crosses an already-governed semantic boundary.

---

## 2. D attacks

### D-A01 — Files appear on disk without declaration

Attack:

A directory contains a plausible continuous set of Dukascopy BI5 files.

Required:

No implicit acquisition domain.

Candidate result:

**SURVIVES.**

The candidate explicitly rejects filesystem/directory presence as membership authority.

### D-A02 — Filename/provider/timestamp continuity

Attack:

Files have continuous-looking names, all come from Dukascopy, and timestamps appear contiguous.

Required:

No implicit component completeness.

Candidate result:

**SURVIVES.**

The candidate explicitly states filename, provider and timestamp continuity are insufficient.

### D-A03 — Missing / extra / repeated physical components

Attack:

One expected component is absent, one undeclared component is present, or one component is delivered twice.

Required:

No silent shrink, admission or deduplication.

Candidate result:

**SURVIVES at the D semantic level.**

Exact anomaly outcomes remain correctly deferred to B/A.

### D-A04 — Warmup boundary ambiguity

Attack:

Two implementations both accept:

```text
execution window = 2021-08-14 → 2026-08-14
warmup_h1_bars = 20
```

Implementation A acquires only components whose represented time lies inside the five-year execution window.

Implementation B additionally acquires the minimum pre-window source material needed to construct the 20 completed H1 warmup bars before first evaluation.

Candidate text currently says:

```text
Any rule translating the frozen temporal boundary and warmup requirement
into an exact expected component set remains a later concrete D/B/Q obligation.
```

Problem:

This postpones a fact that changes the acquisition-domain temporal membership itself.

The frozen Momentum protocol requires 20 completed H1 bars for the signal, while the execution-window contract defines the outer evaluation window. If D does not state whether the warmup source prefix is inside the declared acquisition domain, two future component manifests can differ materially while claiming the same D candidate.

Result:

**BREAK — MAJOR FORMALIZATION DEFECT.**

Required correction:

D must define a deterministic warmup-domain rule now, without enumerating actual files:

```text
acquisition domain
=
frozen five-year evaluation window
+
the minimal immediately preceding market-open source interval
required to construct exactly 20 completed H1 bars under the already-governed
session-calendar contract
```

The exact physical components remain a later D/B materialization question.

No calendar-derived exact file list is required now.

### D-A05 — Reacquisition of identical content

Attack:

A later independent acquisition reproduces byte-identical/content-identical observations.

Required:

No automatic acquisition-domain identity reuse.

Candidate result:

**SURVIVES.**

The candidate requires an explicitly assigned acquisition-instance identity and forbids automatic reuse across reacquisitions.

### D-A06 — Worker/partition order changes

Attack:

The same future declared acquisition is processed with different worker partitioning/traversal.

Required:

Same D membership.

Candidate result:

**SURVIVES.**

---

## 3. R attacks

### R-A01 — BI5 selected only because parser exists

Attack:

Existing V4.3 BI5 code is treated as normative reason to choose BI5.

Required:

Representation selection must not come from implementation convenience.

Candidate result:

**SURVIVES.**

The candidate explicitly uses provider-native / no mandatory pre-qualification conversion / source-provenance preservation as rationale and labels parser support only corroborating.

### R-A02 — Filename is treated as UTC-hour authority

Attack:

A parser reconstructs the hour solely from a path pattern.

Required:

Path parsing must not silently become normative provenance.

Candidate result:

**SURVIVES.**

The candidate explicitly rejects filename authority and requires declared UTC-hour provenance.

### R-A03 — Same BI5 bytes, conflicting hour provenance

Attack:

The same payload bytes are associated with two different declared UTC hour buckets.

Required:

No silent interpretation.

Candidate result:

**SURVIVES CONDITIONALLY.**

The candidate already makes hour-bucket provenance required contextual information, but the concrete conflict/rejection semantics remain correctly deferred to B/A.

### R-A04 — BI5 converted to CSV/Parquet

Attack:

A later transformation preserves visible ticks.

Required:

No automatic representation identity continuity.

Candidate result:

**SURVIVES.**

The candidate rejects inferred representation equivalence.

### R-A05 — Compression / 20-byte layout leaks into R

Attack:

R starts defining LZMA framing, `>IIIff`, price scaling or malformed behavior.

Required:

Those are B semantics.

Candidate result:

**SURVIVES.**

The candidate explicitly defers them to B.

---

## 4. M attacks

### M-A01 — Physical 20-byte block becomes the logical-record definition

Attack:

Because V4.3 uses 20-byte BI5 records, M states `20 bytes = one logical record`.

Required:

M remains format-neutral; B owns the physical mapping.

Candidate result:

**SURVIVES.**

M explicitly refuses the 20-byte assumption.

### M-A02 — Strict duplicates collapse by content

Attack:

Two distinct candidate ticks have identical timestamp/quote/volume payloads.

Required:

Distinct occurrences remain distinct if B yields two occurrences.

Candidate result:

**SURVIVES.**

M is occurrence-based and prohibits content deduplication.

### M-A03 — Parser failure becomes cardinality zero

Attack:

Invalid physical material yields no parsed ticks.

Required:

`INVALID ≠ C=0`.

Candidate result:

**SURVIVES.**

### M-A04 — Qualification exclusion is confused with physical interpretation

Attack:

A B-produced candidate occurrence is later rejected by Q.

Required:

The original candidate interpretation remains distinct from retained membership.

Candidate result:

The detailed §4.6 rule **SURVIVES**, but §4.2 currently defines a candidate record as:

> "one individually retained candidate primary market-tick observation ..."

The word `retained` incorrectly imports post-Q membership into the pre-Q record-model definition.

Result:

**BREAK — SEMANTIC WORDING DEFECT.**

Required correction:

Replace the definition with:

> one individual candidate primary market-tick observation produced by deterministic interpretation of the declared representation under the applicable versioned binding, before qualification membership and before canonical enumeration.

Then state separately that Q alone decides whether a candidate occurrence becomes retained.

### M-A05 — Canonical order leakage

Attack:

M uses source position/order as identity or temporal precedence.

Candidate result:

**SURVIVES.**

### M-A06 — Cross-acquisition identity leakage

Attack:

Same visible tick in two independent acquisitions is assigned automatic identity continuity.

Candidate result:

**SURVIVES.**

---

## 5. Cross-boundary attacks

### X-A01 — D defines B

Candidate result:

**SURVIVES.**

Physical BI5 framing/decoding is not defined in D.

### X-A02 — R defines B

Candidate result:

**SURVIVES.**

R selects the representation but does not define BI5 byte semantics.

### X-A03 — M defines B

Candidate result:

**SURVIVES.**

M defines the logical tick object while delegating physical segmentation/scaling to B.

### X-A04 — M defines Q

Candidate result:

**BREAKS only through the §4.2 wording defect identified in M-A04.**

The rest of the candidate correctly separates candidate occurrence from retained membership.

### X-A05 — candidate implies acquisition/backtest permission

Candidate result:

**SURVIVES.**

All permissions remain explicitly closed.

---

## 6. Verdict

The persisted candidate is not promoted.

```text
D/R/M FIRST CANDIDATE FORMALIZATION
FAIL
```

Demonstrated defects:

1. `DRM-F01 — WARMUP_DOMAIN_MEMBERSHIP_UNDERSPECIFIED`
2. `DRM-F02 — RECORD_MODEL_RETAINED_CANDIDATE_WORDING_LEAK`

No defect requires changing Q-RM-01..12 or any runtime.

No defect requires acquisition.

## 7. Authorized minimal correction

Only the candidate formalization may be corrected:

1. define the deterministic D warmup-domain rule using the frozen `warmup_h1_bars=20` and governed session calendar, without fabricating a file manifest;
2. remove `retained` from the M pre-Q candidate-occurrence definition and make Q retention explicitly downstream.

Do not modify R unless the correction itself demonstrates a new R defect.

After correction:

- persist the corrected candidate;
- re-break the same attacks;
- keep official D/R/M gate verdicts BLOCKED;
- do not start B until the corrected formalization survives the persisted-head re-break.


---

# 8. Persisted-head re-break after minimal correction

**Corrected candidate HEAD:** `45b0db9a1b73ca233c6d966cfe409bb72c4cce63`  
**Corrected candidate blob:** `2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9`

The branch was verified identical to that HEAD before re-break.

The same attack set was re-applied without changing the candidate during the attack.

## 8.1 Re-break of DRM-F01

Original defect:

`WARMUP_DOMAIN_MEMBERSHIP_UNDERSPECIFIED`

Corrected rule now states that the semantic acquisition domain contains:

```text
mandatory warmup prefix
+
frozen five-year evaluation window
```

where the warmup prefix is the minimal immediately preceding market-open source interval required to construct the frozen `20 completed H1 bars` requirement under the governed session-calendar contract.

Repository re-check confirms the current authoritative surfaces establish:

```text
warmup_h1_bars = 20

Momentum horizon = 20 completed H1 bars
M_t = Close_t / Close_{t-20} - 1
signal usable only from t+1
```

The repository does not yet define the concrete raw-BI5 component translation of that warmup.

That does not re-break D because the corrected candidate does not claim that translation exists. It explicitly leaves physical component enumeration/completeness to later D/B/Q materialization.

Adversarial variant:

Two implementations choose different physical BI5 file prefixes while claiming the same completed-H1 warmup semantics.

Result:

```text
not both conforming yet
→ B/Q must later derive one deterministic physical translation
→ until then actual D materialization remains BLOCKED
```

The semantic D candidate no longer allows omission of the warmup obligation itself.

**RE-BREAK RESULT: SURVIVES.**

## 8.2 Re-break of DRM-F02

Original defect:

`RECORD_MODEL_RETAINED_CANDIDATE_WORDING_LEAK`

Corrected M definition now states:

> one individual candidate primary market-tick observation produced by deterministic interpretation of the declared representation under the applicable versioned binding, before qualification membership and before canonical enumeration.

and separately:

> Q alone later determines whether a candidate occurrence becomes part of the retained qualified logical universe.

The attack:

```text
B produces candidate occurrence
Q rejects candidate
```

no longer changes the M interpretation.

**RE-BREAK RESULT: SURVIVES.**

## 8.3 Full attack-set re-break

```text
D-A01 disk presence                    SURVIVES
D-A02 filename/provider continuity     SURVIVES
D-A03 missing/extra/repeated           SURVIVES
D-A04 warmup-domain ambiguity          SURVIVES AFTER CORRECTION
D-A05 reacquisition identity           SURVIVES
D-A06 worker/traversal order           SURVIVES

R-A01 parser-convenience selection     SURVIVES
R-A02 filename hour authority          SURVIVES
R-A03 conflicting hour provenance      SURVIVES CONDITIONALLY / B+A REQUIRED
R-A04 CSV/Parquet equivalence          SURVIVES
R-A05 BI5 binding leakage into R       SURVIVES

M-A01 20-byte leakage into M           SURVIVES
M-A02 strict duplicate collapse        SURVIVES
M-A03 parser failure = C0              SURVIVES
M-A04 qualification/membership leak    SURVIVES AFTER CORRECTION
M-A05 canonical/temporal leakage       SURVIVES
M-A06 cross-acquisition identity       SURVIVES

X-A01 D defines B                      SURVIVES
X-A02 R defines B                      SURVIVES
X-A03 M defines B                      SURVIVES
X-A04 M defines Q                      SURVIVES AFTER CORRECTION
X-A05 implicit permission increase     SURVIVES
```

No additional candidate defect was demonstrated.

## 8.4 Final D/R/M block state

The formalization is adversarially stable enough to become the governed input to the next specification block.

This does **not** convert the concrete gates to PASS.

```text
D gate = BLOCKED
  reason: no actual acquisition instance, component manifest or completeness evidence

R gate = BLOCKED
  reason: selected candidate representation still lacks qualified concrete B semantics

M gate = BLOCKED
  reason: selected candidate model still depends on qualified B/Q semantics before concrete freeze

D/R/M candidate formalization
= PERSISTED + CORRECTED + RE-BROKEN
= NO NEW DEFECT DEMONSTRATED
```

No acquisition authorization is created.

No real backtest authorization is created.

## 8.5 Boundary for next work

The D/R/M candidate may now be consumed only as candidate input for:

```text
B — concrete native BI5 format binding
+
A — concrete anomaly matrix
```

The next block must not reinterpret:

- the acquisition-domain warmup obligation;
- native BI5 as the selected first-path representation candidate;
- the format-neutral occurrence-based M semantics.

If B/A cannot make those candidate semantics deterministic, B/A must FAIL or remain BLOCKED rather than mutating D/R/M silently.
