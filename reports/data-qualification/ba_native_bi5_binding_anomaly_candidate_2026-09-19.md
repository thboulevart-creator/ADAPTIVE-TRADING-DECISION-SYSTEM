# B + A — FIRST CONCRETE NATIVE BI5 BINDING / ANOMALY CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `ab988bee21abc06eb43998f7ed61a911bc47e45d`  
**Input D/R/M candidate blob:** `2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9`  
**Scope:** formalization only — no acquisition, no real BI5 processing, no backtest, no permission increase.

## 0. Status and strict separations

This artifact creates the first concrete candidate for:

```text
B — native Dukascopy BI5 physical→logical binding
+
A — native BI5 anomaly matrix
```

Official gate verdicts remain:

```text
B = BLOCKED
A = BLOCKED
```

until the candidate survives governed adversarial qualification and its factual/provider-sensitive semantics receive sufficient evidence.

Strict separations:

```text
existing V4.3 parser behavior
≠ normative binding authority

physical component locator
≠ logical occurrence identity

physical slot index
≠ canonical record position
≠ temporal precedence

B physical interpretation
≠ Q qualification membership

A anomaly classification
≠ silent repair

candidate
≠ PASS
```

No real BI5 file is acquired or opened by this formalization.

---

# 1. Upstream candidate inputs

## 1.1 D

Candidate declaration family:

`D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1`

The future acquisition domain contains:

```text
mandatory deterministic 20-H1 warmup prefix
+
frozen five-year evaluation window
```

No actual component manifest exists yet.

## 1.2 R

Selected candidate representation:

```text
representation_id =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS

representation_version =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE
```

R requires explicit declared UTC-hour provenance and rejects filename/path authority.

## 1.3 M

Candidate logical model:

`PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE`

Logical payload:

```text
market timestamp
ask price
bid price
ask volume
bid volume
```

Candidate occurrence interpretation is pre-Q, occurrence-based, strict-duplicate preserving, non-canonical and non-temporal.

---

# 2. Existing BI5 evidence class

The repository currently contains one read-only implementation surface in:

`tools/probe_research_execution_compatibility_v4_3.py`

Its current BI5 behavior includes:

```text
compression candidate      = LZMA FORMAT_ALONE
decompressed record width  = 20 bytes
binary layout candidate    = >IIIff
field order candidate      = millisecond_offset, ask_raw, bid_raw, ask_volume_raw, bid_volume_raw
timestamp reconstruction   = declared hour + millisecond_offset
price candidate            = raw uint32 / 1000
volume candidate           = source float32 value
```

This is **implementation evidence for candidate selection**, not independent proof of provider semantics.

The B candidate below deliberately freezes those semantics as a proposition to be adversarially qualified; it does not claim that V4.3 itself is normative authority.

---

# 3. B candidate identity

```text
format_binding_id =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD

format_binding_version =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

Applicable only to:

```text
D candidate:
D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1

R candidate:
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE

M candidate:
PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE
```

No fallback to another symbol, provider, representation or binding version is permitted.

---

# 4. Normative candidate component input

B does not accept a bare filesystem path as sufficient semantic input.

A physical component presented to B is conceptually:

```text
Bi5ComponentInput
- acquisition_domain_id
- component_manifest_entry_id
- instrument_id = USATECHIDXUSD
- declared_hour_bucket_utc
- compressed_payload_bytes
- content_hash / provenance reference supplied by later D materialization
```

The exact serialization of this envelope is not selected here.

Required properties:

1. `component_manifest_entry_id` is supplied by D materialization and is immutable inside one declared acquisition.
2. `declared_hour_bucket_utc` is an exact UTC hour boundary.
3. the hour is not inferred normatively from filename/path syntax;
4. the compressed payload belongs to that manifest entry;
5. B may verify physical metadata but may not manufacture missing D provenance.

If hour provenance is absent or contradictory:

`QUALIFICATION BLOCKED`.

---

# 5. Compression / envelope semantics

Candidate rule:

```text
compressed_payload_bytes
→ exactly one LZMA-Alone stream
→ decompressed_payload_bytes
```

Candidate decompression semantics correspond to the current V4.3 `lzma.FORMAT_ALONE` behavior.

Binding requirements:

- decompression must be deterministic;
- no silent byte repair;
- no implicit alternate compression fallback;
- no concatenated second stream unless a later binding version explicitly permits it;
- no trailing compressed material outside the one declared stream;
- decompression failure is not cardinality zero;
- empty decompressed output is not automatically a valid zero-observation component.

Compression-library choice is implementation-specific; output semantics are not.

---

# 6. Decompressed framing

Candidate framing:

```text
decompressed payload starts at byte offset 0
record width = exactly 20 bytes
no decompressed header
no decompressed footer
no inter-record delimiter
no record may cross a physical component boundary
```

For a decompressed byte length `N`:

```text
complete_slot_count = floor(N / 20)
terminal_remainder  = N mod 20
```

Every complete slot has boundary:

```text
[start = 20*i, end = 20*i + 20)
```

for zero-based component-local slot index `i`.

The slot index is physical provenance / individuation evidence only.

It is not:

- canonical record position;
- market-event identity;
- temporal ordering authority;
- cross-acquisition identity.

---

# 7. Binary field layout

Each complete 20-byte slot is interpreted candidate-normatively as big-endian:

```text
>IIIff
```

Exact fields:

```text
bytes  0..3   uint32 big-endian  millisecond_offset
bytes  4..7   uint32 big-endian  ask_price_raw
bytes  8..11  uint32 big-endian  bid_price_raw
bytes 12..15  IEEE-754 binary32 big-endian ask_volume_raw
bytes 16..19  IEEE-754 binary32 big-endian bid_volume_raw
```

No implementation may substitute signed integers, little-endian decoding, binary64 source fields, or field reordering.

A semantic change to any of these rules requires another B version.

---

# 8. Timestamp interpretation

For a valid record:

```text
0 <= millisecond_offset < 3_600_000
```

Logical market timestamp:

```text
market_timestamp
=
declared_hour_bucket_utc
+
millisecond_offset milliseconds
```

Consequences:

- the record timestamp must remain within the declared UTC hour;
- filename/path text is irrelevant to normative timestamp reconstruction;
- a slot with offset outside the hour is invalid but independently framed;
- same-millisecond occurrences are permitted and remain distinct;
- component-local physical slot order is not by itself temporal authority.

---

# 9. Price interpretation

Candidate USATECHIDXUSD scaling rule:

```text
ask_price = ask_price_raw / 1000
bid_price = bid_price_raw / 1000
```

The division is an exact rational/decimal semantic transformation, not a floating-point rounding policy.

Logical price unit:

`USATECHIDXUSD quote-price unit with 1/1000 raw integer scale`.

Required basic validity:

```text
ask_price_raw > 0
bid_price_raw > 0
ask_price >= bid_price
```

A future provider/source evidence review may falsify the candidate scale or field order. If so, B must FAIL and version/change explicitly; an implementation may not silently adapt.

---

# 10. Volume interpretation

Candidate rule:

```text
ask_volume
=
exact numeric value represented by source IEEE-754 binary32 ask_volume_raw

bid_volume
=
exact numeric value represented by source IEEE-754 binary32 bid_volume_raw
```

No scaling is applied.

The unit is deliberately identified as:

`DUKASCOPY_SOURCE_VOLUME_UNIT_V1_CANDIDATE`

This unit means:

> the opaque source-native quantity encoded by the BI5 binary32 field, preserved without conversion.

It does not claim lots, contracts, shares, currency or exchange volume.

Validity:

```text
finite
and
>= 0
```

NaN, ±Infinity and negative volume are invalid.

A later unit reinterpretation capable of changing logical payload meaning requires a new B version.

---

# 11. Physical→logical cardinality

For each complete 20-byte slot:

```text
valid deterministic slot
→ exactly 1 candidate logical primary market-tick occurrence

invalid but constructively localisable slot
→ anomaly outcome from A
→ not C=0

ambiguous/non-localisable slot or framing
→ no normative qualified universe
```

A component with zero decompressed bytes is **not** declared to have cardinality zero under this candidate because the repository does not establish that empty BI5 is the normative no-tick encoding.

Therefore empty output is an anomaly, not `C=0`.

---

# 12. Candidate occurrence individuation / provenance

Within one materialized acquisition component, every complete physical slot is a distinct physical occurrence source.

Candidate provenance locator:

```text
(component_manifest_entry_id, component_local_slot_index)
```

This tuple exists only to preserve physical provenance and strict duplicate individuality through interpretation.

It is not promoted to the final normative observation identity formula.

Thus:

```text
same decoded payload in slot i and slot j
with i != j
→ two candidate occurrences

same bytes reacquired in another acquisition
→ no automatic identity continuity
```

---

# 13. Cross-component semantics

Candidate rule:

```text
one 20-byte logical-source slot may never cross component boundaries
```

Each component is decompressed/framed independently.

A trailing partial fragment in component A cannot be combined with leading bytes from component B.

D owns which components belong to the acquisition.

B owns how each declared component is physically interpreted.

The selected candidate representation does not support multiple normative components for the same instrument/hour unless D later supplies an explicit non-ambiguous role under a compatible representation/binding revision.

Unexplained same-hour component multiplicity is an A anomaly.

---

# 14. Ordering semantics

B preserves component-local slot index as provenance but does not silently sort records.

Same timestamp:

`allowed`.

Strict timestamp regression inside one declared hourly component:

```text
timestamp[i] < timestamp[i-1]
```

is treated as a qualification-relevant anomaly because the current project has no normative permission to repair/reorder the provider-native sequence before qualification.

This does not make physical slot order universal temporal authority.

It means only:

> the binding refuses to silently repair a native component whose represented timestamps regress relative to its own source sequence.

The later temporal contract remains the authority for final ordered research structures.

---

# 15. A candidate identity

```text
anomaly_matrix_id =
A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD

anomaly_matrix_version =
A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

Binding dependency:

`B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE`

Unless explicitly stated, no class is acquisition-fatal.

Unknown/unregistered anomaly:

`QUALIFICATION BLOCKED`.

---

# 16. Concrete anomaly matrix

## BI5-A01 — MISSING_DECLARED_COMPONENT

Trigger:

A component required by the future D manifest cannot be materialized.

Evidence:

D manifest entry exists; payload/provenance object absent or inaccessible.

Scope:

declared acquisition membership/completeness.

Localisable:

NO for qualification membership.

Outcome:

`QUALIFICATION BLOCKED`.

Acquisition-fatal:

NO.

Diagnostic:

manifest entry + absence/access evidence.

---

## BI5-A02 — UNDECLARED_COMPONENT_PRESENT

Trigger:

Physical BI5 material is offered to the acquisition but has no D manifest entry.

Scope:

acquisition membership.

Localisable:

NO for acquisition completeness/membership.

Outcome:

`QUALIFICATION BLOCKED`.

No silent admission and no silent deletion.

---

## BI5-A03 — REPEATED_OR_CONFLICTING_COMPONENT_DELIVERY

Trigger:

The same `component_manifest_entry_id` is supplied more than once, or multiple payloads/provenance claims compete for the same declared component identity.

Scope:

component identity / acquisition membership.

Localisable:

NO unless a later D contract provides a unique authoritative delivery rule.

Outcome:

`QUALIFICATION BLOCKED`.

No deduplication by hash/content.

---

## BI5-A04 — AMBIGUOUS_OR_MISSING_HOUR_PROVENANCE

Trigger:

`declared_hour_bucket_utc` is absent, malformed, non-hour-aligned, conflicts across authoritative provenance records, or does not uniquely bind the payload to one UTC hour.

Scope:

all timestamps in the component.

Localisable:

NO.

Outcome:

`QUALIFICATION BLOCKED`.

Filename/path cannot resolve it.

---

## BI5-A05 — DECOMPRESSION_FAILURE_OR_UNSUPPORTED_ENVELOPE

Trigger:

Payload cannot be deterministically decoded as exactly the B-declared single LZMA-Alone stream, or alternate/trailing/concatenated envelope semantics are required.

Scope:

whole component framing.

Localisable:

NO.

Outcome:

`QUALIFICATION BLOCKED`.

No fallback codec.

---

## BI5-A06 — ZERO_DECOMPRESSED_BYTES

Trigger:

Valid envelope decoding yields zero decompressed bytes.

Possible interpretations include:

- valid no-tick hour;
- empty/corrupt source artifact;
- acquisition failure.

Because the repository does not yet normatively distinguish these meanings:

Localisable:

NO / ambiguous semantic cardinality.

Outcome:

`QUALIFICATION BLOCKED`.

Not `C=0`.

---

## BI5-A07 — TERMINAL_PARTIAL_SLOT_WITHOUT_COMPLETENESS_PROOF

Trigger:

```text
len(decompressed_payload) mod 20 != 0
```

and acquisition/component completeness evidence cannot prove that the terminal remainder is the entire available malformed record rather than evidence of a truncated transport/source component.

Scope:

terminal framing plus possible missing membership.

Localisable:

NO.

Outcome:

`QUALIFICATION BLOCKED`.

---

## BI5-A08 — TERMINAL_PARTIAL_SLOT_WITH_CONSTRUCTIVE_COMPLETENESS_PROOF

Trigger:

```text
len(decompressed_payload) mod 20 != 0
```

but independent D/provenance evidence constructively proves:

- the component delivery is complete;
- byte zero is the framing origin;
- every preceding 20-byte slot boundary is unaffected;
- the terminal remainder cannot alter any preceding occurrence;
- no missing unseen suffix can change acquisition membership.

Scope:

one terminal malformed physical fragment.

Localisable:

YES.

Outcome:

`REJECT RECORD`.

Required diagnostic:

component hash/provenance + decompressed length + remainder bytes + completeness proof reference.

---

## BI5-A09 — MILLISECOND_OFFSET_OUT_OF_RANGE

Trigger:

```text
millisecond_offset >= 3_600_000
```

for one complete 20-byte slot.

Boundaries of neighboring fixed-width slots are unaffected.

Localisable:

YES.

Outcome:

`REJECT RECORD`.

---

## BI5-A10 — INVALID_PRICE

Trigger on one complete slot:

- `ask_price_raw == 0`;
- `bid_price_raw == 0`;
- after exact /1000 mapping, `ask_price < bid_price`.

Localisable:

YES.

Outcome:

`REJECT RECORD`.

No clipping, inversion, carry-forward or repair.

---

## BI5-A11 — INVALID_VOLUME

Trigger:

decoded ask/bid source binary32 volume is:

- NaN;
- +Infinity;
- -Infinity;
- negative.

Localisable:

YES.

Outcome:

`REJECT RECORD`.

Zero is permitted.

---

## BI5-A12 — NATIVE_COMPONENT_TIMESTAMP_REGRESSION

Trigger:

for adjacent complete valid slots in source sequence:

```text
timestamp[i] < timestamp[i-1]
```

Same timestamps are not an anomaly.

Scope:

source sequence / temporal interpretation.

Localisable:

NO under the current candidate because silent sorting could change within-component sequence semantics and later execution behavior.

Outcome:

`QUALIFICATION BLOCKED`.

No sort/reorder repair.

---

## BI5-A13 — UNEXPLAINED_MULTIPLE_COMPONENTS_FOR_SAME_HOUR

Trigger:

D materialization presents more than one normative native-BI5 component for the same acquisition/instrument/UTC hour without an explicit disjoint role defined by the representation/binding contract.

Scope:

acquisition membership and occurrence multiplicity.

Localisable:

NO.

Outcome:

`QUALIFICATION BLOCKED`.

No merge, concatenate, winner-selection or content deduplication.

---

## BI5-A14 — REPRESENTATION_OR_BINDING_IDENTITY_MISMATCH

Trigger:

component claims or required declaration versions do not match the exact D/R/M/B tuple for which this binding is valid.

Scope:

normative interpretation identity.

Localisable:

NO.

Outcome:

`QUALIFICATION BLOCKED`.

No nearest-version fallback.

---

## BI5-A15 — UNKNOWN_ANOMALY_CLASS

Trigger:

physical or semantic condition affects framing, field interpretation, cardinality, provenance or membership but is not captured by the versioned A matrix.

Scope:

unknown.

Localisable:

not constructively proven.

Outcome:

`QUALIFICATION BLOCKED`.

---

# 17. Explicitly permitted conditions

The following are not anomalies under this candidate solely by themselves:

```text
two distinct slots with byte-identical payload
two distinct decoded ticks with identical logical payload
same millisecond timestamp on multiple occurrences
zero ask volume
zero bid volume
different runtime traversal order across components
different implementation/library producing semantically identical output
```

Strict duplicates remain distinct candidate occurrences.

---

# 18. No silent repair policy

The binding/anomaly candidate forbids:

- filename-derived hour substitution;
- alternate codec fallback;
- byte padding;
- dropping arbitrary leading/trailing material without A classification;
- endian guessing;
- field-order guessing;
- price-scale guessing;
- NaN/Infinity coercion;
- negative-volume absolute value;
- bid/ask swapping;
- timestamp clipping;
- timestamp sorting;
- duplicate removal;
- cross-component fragment joining;
- undeclared component merging.

---

# 19. Binding version-change triggers

A new B version is mandatory if any change can alter:

- compression/envelope interpretation;
- framing origin or record width;
- field layout/order/types/endianness;
- price scaling;
- volume semantic unit/conversion;
- hour/timestamp reconstruction;
- cardinality;
- cross-component rules;
- occurrence provenance/individuation;
- anomaly localisability or failure scope;
- qualification-relevant ordering treatment.

A parser/library refactor with proven semantic equivalence need not change B.

---

# 20. Evidence limitations

The following candidate facts currently come from the existing V4.3 implementation surface, not independent provider evidence inside the repository:

```text
LZMA-Alone
20-byte width
>IIIff
ask/bid field ordering
price /1000
raw float32 volume semantics
```

Therefore this artifact does not itself promote B to PASS.

Future qualification must either:

1. independently corroborate these semantics; or
2. demonstrate them through sufficiently strong controlled evidence/conformance;

otherwise B remains BLOCKED or FAILS.

---

# 21. Pre-break state

```text
B candidate formalization = PERSISTED CANDIDATE
A candidate formalization = PERSISTED CANDIDATE

B official gate = BLOCKED
A official gate = BLOCKED

real acquisition = NOT AUTHORIZED
real BI5 processing = NOT AUTHORIZED
real backtest = NOT AUTHORIZED
```

---

# 22. Next governed action

Adversarially break this exact persisted B/A candidate.

Attack at minimum:

- filename/path used as hour authority;
- missing/conflicting hour provenance;
- alternate codec fallback;
- concatenated/trailing LZMA streams;
- zero-length output;
- shifted framing origin;
- terminal truncation with and without completeness proof;
- field endianness/order confusion;
- price-scale confusion;
- NaN/Inf/negative volume;
- ask < bid;
- ms boundary 3_599_999 vs 3_600_000;
- strict duplicates;
- same-ms occurrences;
- timestamp regression;
- repeated/missing/extra/same-hour components;
- cross-component fragment joining;
- parser/library disagreement;
- unknown anomaly class;
- accidental promotion of physical slot index to canonical/temporal identity;
- acquisition/backtest permission leakage.

No data acquisition is permitted during the break.
