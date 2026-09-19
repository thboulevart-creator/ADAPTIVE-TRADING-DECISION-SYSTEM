# D + R + M — FIRST CONCRETE PRE-BACKTEST CANDIDATE FORMALIZATION

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `1cbe48d5df52bc60369804158a2531cbbdb8692a`  
**Scope:** formalization only — no acquisition, no real data, no backtest, no permission increase.

## 0. Governing constraints

This artifact instantiates the first candidate design for the concrete pre-backtest block:

```text
D + R + M
```

It does not close the historical gates.

The current official gate verdicts remain:

```text
D = BLOCKED
R = BLOCKED
M = BLOCKED
```

until the candidate survives its governed adversarial process and the required downstream dependencies exist.

Strict separations:

```text
acquisition declaration contract / expected membership rule
≠ actual acquired component manifest

representation selection
≠ parser implementation

record-model version
≠ format-specific binding

candidate design
≠ qualification PASS
```

No `.bi5` file is downloaded or read by this formalization.

---

# 1. Current authoritative inputs

The candidate is bounded by the following already-qualified/current repository evidence.

## 1.1 Frozen temporal research boundary

`04-REFERENCE/EXECUTION-WINDOW-FREEZE.json`

Current frozen facts:

```text
instrument = USATECHIDXUSD
window_start = 2021-08-14
window_end = 2026-08-14
first_included_open_slot_utc = 2021-08-15T22:00:00+00:00
last_included_open_slot_utc = 2026-08-14T20:00:00+00:00
warmup_h1_bars = 20
window_candidate_count = 68
window_resolved_count = 68
window_unresolved_count = 0
massive_acquisition_authorized = false
real_backtest_authorized = false
```

This freeze is a temporal/calendar boundary, not a component manifest.

## 1.2 Universal acquisition-domain contract

Q-RM-08 requires the eventual concrete declaration to bind:

```text
acquisition_declaration_version
acquisition_domain_id
representation_id
representation_version
record_model_version
format_binding_id
format_binding_version
qualification_contract_id
qualification_contract_version
component_manifest
component_membership_policy
completeness_evidence
acquisition_state
```

This formalization deliberately does not fabricate the fields that require later B/Q/materialization evidence.

## 1.3 Existing representation evidence

The current repository already contains read-only compatibility knowledge for Dukascopy BI5 in:

`tools/probe_research_execution_compatibility_v4_3.py`

It currently treats Dukascopy BI5 as native hourly compressed tick material and contains one implementation capable of decoding it.

That executable is evidence that the representation is technically relevant to the current project.

It is not normative authority for the representation or binding semantics.

## 1.4 Record-model architecture

Q-RM-01 validated RB-A:

```text
universal semantic record model
+
explicit versioned binding per declared representation
```

Q-RM-02..05 require:

- occurrence-based, not content-based individuality;
- strict duplicate preservation;
- cardinality distinct from invalidity/ambiguity;
- qualification after physical→logical interpretation;
- acquisition-scoped identity semantics;
- no temporal precedence created by record membership;
- no parser/library default as normative semantics.

---

# 2. D candidate — bounded acquisition declaration family

## 2.1 Candidate identity

```text
candidate_contract_id =
D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1
```

Status:

`FORMALIZED CANDIDATE — NOT MATERIALISED — NOT QUALIFIED`

## 2.2 Intended semantic domain

The candidate declaration family applies only to a future explicitly authorized acquisition satisfying all of the following:

```text
provider/source family = Dukascopy
instrument             = USATECHIDXUSD
temporal authority     = EXECUTION_WINDOW_FREEZE_V1
representation         = R candidate defined in this artifact
record model           = M candidate defined in this artifact
purpose                = bounded research qualification for the first governed backtest path
```

The candidate does not create an acquisition merely because files later appear on disk.

## 2.3 Acquisition-domain identity rule

The eventual concrete `acquisition_domain_id` must be:

- assigned explicitly to one acquisition instance;
- immutable for that declared acquisition;
- independent of traversal/worker/file ordering;
- not derived solely from payload content;
- not reused automatically for a later reacquisition of the same observations.

Therefore:

```text
same intended time window
+
same visible market content
≠
same acquisition_domain_id across independent reacquisitions
```

No concrete `acquisition_domain_id` is fabricated now because no acquisition instance exists.

## 2.4 Expected membership rule

The future acquisition is intended to consist only of declared provider-native components belonging to the bounded Dukascopy USATECHIDXUSD research domain.

Membership must be established by a later concrete declaration/manifest mechanism.

The following are explicitly insufficient by themselves:

- directory membership;
- filename continuity;
- URL continuity;
- provider continuity;
- timestamp continuity;
- filesystem traversal;
- presence on disk.

The exact expected physical component set is not enumerated in this artifact.

In particular, this formalization does not infer from the execution-window calendar that one file must exist for every wall-clock hour or every open slot.

### Deterministic warmup-domain rule

The declared research acquisition domain is not limited to the five-year evaluation interval alone.

For the first Momentum V1 baseline path it contains:

```text
A. evaluation domain
   = the already-frozen contiguous execution window

PLUS

B. warmup prefix
   = the minimal immediately preceding market-open source interval
     required to construct exactly 20 completed H1 bars
     before the first evaluation-dependent Momentum value,
     under the already-governed Dukascopy USATECH session-calendar contract.
```

This rule fixes the semantic temporal membership of the acquisition domain without fabricating physical files.

The warmup prefix:

- is mandatory for this first baseline acquisition declaration;
- is not part of the evaluated five-year performance interval;
- may not be lengthened or shortened by data availability, download convenience, or observed strategy results;
- must be derived deterministically from the frozen `warmup_h1_bars=20` requirement and the governed session calendar;
- must later be translated by D/B/Q into exact expected physical components before completeness can be claimed.

Therefore:

```text
five-year evaluation window
≠ complete acquisition domain by itself

complete candidate acquisition temporal domain
=
mandatory warmup prefix
+
five-year evaluation window
```

The physical file/object enumeration remains a later concrete D/B/Q obligation.

## 2.5 Manifest state

```text
actual component_manifest = NOT MATERIALISED
completeness_evidence      = NOT AVAILABLE
acquisition_state          = CANDIDATE_DECLARATION_ONLY
```

Therefore D remains BLOCKED.

The candidate only fixes what the future declaration is allowed to mean.

## 2.6 Missing / extra / repeated components

The future declaration must fail closed:

```text
missing declared component
→ never silently shrink domain

extra undeclared component
→ never silently admit

repeated delivery
→ never silently deduplicate or create extra logical occurrence

ambiguous membership
→ QUALIFICATION BLOCKED
```

The exact anomaly classification belongs to B/A and is not invented here.

---

# 3. R candidate — selected acquisition representation

## 3.1 Candidate identity

```text
representation_id =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS

representation_version =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE
```

Status:

`SELECTED CANDIDATE — NOT QUALIFIED`

## 3.2 Selection rationale

The candidate selects the Dukascopy provider-native BI5 research representation because it preserves the upstream acquisition material without first requiring a CSV/Parquet conversion.

This reduces the number of pre-qualification transformations whose semantics would otherwise have to be justified.

The selection is not justified by:

```text
"the current parser already supports BI5"
```

Parser support is only corroborating implementation evidence.

The semantic rationale is:

```text
provider-native research representation
+
no mandatory pre-qualification format conversion
+
preservation of exact source bytes/provenance
```

## 3.3 Representation component concept

The candidate representation is conceptualized as a provider-native hourly BI5 component coupled to explicit declared provenance sufficient to identify its intended UTC hour bucket.

Conceptually:

```text
R component
=
(native BI5 payload bytes,
 declared UTC hour-bucket provenance,
 acquisition-component provenance)
```

The exact physical locator, URI/path encoding, compression framing, internal 20-byte segmentation, field decoding, price scaling and malformed behavior are intentionally not defined by R.

Those belong to B.

## 3.4 No filename authority

The current V4.3 implementation can recover the hour from a filename/path.

That implementation behavior is not promoted into normative representation semantics.

Therefore:

```text
filename contains YYYY/MM/DD/HH
≠
hour provenance is normatively established
```

The future D/B package must bind the hour bucket through declared provenance that remains reviewable independently of parser convenience.

## 3.5 No representation equivalence by inference

A CSV or Parquet transformation of the same intended observations is not automatically the same representation/version.

```text
BI5 → CSV
BI5 → Parquet
```

would require explicit transformation/provenance contracts and cannot inherit R identity silently.

R therefore selects only native BI5 for the first candidate path.

---

# 4. M candidate — format-neutral primary market tick record model

## 4.1 Candidate identity

```text
record_model_version =
PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE
```

Status:

`FORMALIZED CANDIDATE — NOT FROZEN / NOT QUALIFIED`

## 4.2 Semantic object

A candidate primary logical record occurrence is:

> one individual candidate primary market-tick observation produced by deterministic interpretation of the declared representation under the applicable versioned binding, before qualification membership and before canonical enumeration.

M does not define the physical byte boundary that produces the occurrence.

Q alone later determines whether a candidate occurrence becomes part of the retained qualified logical universe.

## 4.3 Candidate logical payload

The tick-oriented logical payload contains the semantic values required to represent a primary market tick:

```text
market timestamp
ask price
bid price
ask volume
bid volume
```

M defines these as logical semantic fields.

It does not define:

- BI5 byte offsets;
- BI5 struct layout;
- endianness;
- compression;
- millisecond reconstruction mechanics;
- numeric storage types;
- price scaling;
- volume decoding;
- physical field units.

Those are B responsibilities.

## 4.4 Occurrence individuality

Individuality is occurrence-based, never content-based.

Therefore:

```text
payload(A) = payload(B)
```

does not imply:

```text
A = B
```

when B determines two distinct candidate occurrences.

No content-based deduplication is permitted by M.

## 4.5 Cardinality boundary

M permits:

```text
0 / 1 / N candidate primary occurrences
```

only as determined by the concrete representation binding.

M itself does not say:

```text
1 BI5 file = 1 record
1 decompressed payload = 1 record
20 bytes = 1 logical record
```

The eventual B binding may establish a physical mapping, but M cannot assume it.

## 4.6 Qualification boundary

M distinguishes candidate occurrence interpretation from retained qualification membership:

```text
physical material
→ deterministic B interpretation
→ candidate logical occurrence(s)
→ Q qualification membership
→ retained logical universe
```

An excluded candidate occurrence is not retroactively redefined as nonexistent physical interpretation.

## 4.7 Failure semantics

M preserves:

```text
VALID + no primary observation → cardinality 0
INVALID                       → not cardinality 0
AMBIGUOUS                     → not cardinality 0
```

Exact anomaly classes and outcomes belong to B/A/Q.

## 4.8 Temporal and identity non-claims

M does not establish:

- canonical record position;
- source ordinal as normative identity;
- byte offset as identity;
- content hash as identity;
- temporal precedence;
- cross-acquisition identity continuity.

Observation identity remains acquisition-scoped under the already-adjudicated identity-scope decision.

```text
record occurrence semantics
≠ temporal order

record occurrence semantics
≠ canonical enumeration
```

---

# 5. Candidate D/R/M composition

The candidate composition is:

```text
D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1
    ↓ binds
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE
    ↓ interpreted into
PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE
```

But physical interpretation is intentionally still absent:

```text
D + R + M
≠
B
```

and therefore:

```text
D + R + M candidate
≠ qualified logical universe
≠ acquisition authorization
≠ real backtest authorization
```

---

# 6. Explicit unresolved dependencies

The candidate deliberately leaves unresolved:

```text
B — exact native BI5 physical→logical binding
A — concrete BI5 anomaly matrix
Q — concrete qualification contract / parameters
F — qualified-universe freeze artifact
O — semantic comparison oracle
I_A / I_B — executable deterministic implementations
```

D also remains materially incomplete because no actual acquisition component manifest or completeness evidence exists.

---

# 7. Pre-break verdict state

No PASS is declared.

```text
D gate verdict = BLOCKED
R gate verdict = BLOCKED
M gate verdict = BLOCKED

D/R/M FORMALIZATION = PERSISTED CANDIDATE
ADVERSARIAL QUALIFICATION = NOT YET PERFORMED
```

No permission increases.

---

# 8. Next governed action

Adversarially break this exact persisted D/R/M candidate before any correction or downstream B work.

The break must attack at minimum:

- acquisition-domain over-merge / over-split;
- missing/extra/repeated components;
- window/warmup membership ambiguity;
- filename/path/provider inference;
- reacquisition identity;
- BI5 selection by implementation convenience;
- hour-bucket provenance;
- format conversion equivalence;
- physical 20-byte assumptions leaking into M;
- strict duplicates;
- parser failure becoming zero cardinality;
- qualification exclusion collapsing into physical cardinality;
- canonical/temporal ordering leakage;
- cross-acquisition identity leakage.

No data acquisition is permitted during the break.


---

# 9. Correction record after first adversarial break

Adversarial break artifact:

`reports/data-qualification/drm_first_candidate_adversarial_break_2026-09-19.md`

The first persisted candidate failed on exactly two demonstrated defects:

```text
DRM-F01 — WARMUP_DOMAIN_MEMBERSHIP_UNDERSPECIFIED
DRM-F02 — RECORD_MODEL_RETAINED_CANDIDATE_WORDING_LEAK
```

Corrections applied:

1. D now defines the mandatory warmup prefix as part of the semantic acquisition domain using the frozen 20-H1 requirement and the governed session-calendar contract, while still refusing to fabricate physical components.
2. M now defines only a pre-Q candidate logical occurrence; retention is explicitly owned by Q.

No R semantics were changed.

Official gate verdicts remain:

```text
D = BLOCKED
R = BLOCKED
M = BLOCKED
```

The corrected candidate requires a persisted-head adversarial re-break before any further work.
