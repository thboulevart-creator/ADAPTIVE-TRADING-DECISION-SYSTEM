# SESSION BACKUP — 2026-09-19 — NATIVE BI5 B/A FORMALIZATION

## 0. Purpose

Durable snapshot for the first concrete native-BI5 `B + A` formalization block.

Repository:
`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Branch:
`integration/system-v1`

GitHub and the current Recovery Checkpoint remain authoritative.

---

## 1. Starting state

Starting HEAD:

`ab988bee21abc06eb43998f7ed61a911bc47e45d`

Input corrected D/R/M candidate:

- artifact: `reports/data-qualification/drm_first_concrete_candidate_formalization_2026-09-19.md`;
- blob: `2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9`;
- final D/R/M adversarial artifact blob: `8e29d132d8a2eaf28bd9901f2bed33392cccfc79`.

Official upstream gate verdicts remained:

```text
D = BLOCKED
R = BLOCKED
M = BLOCKED
```

No acquisition or real backtest was authorized.

---

## 2. First B/A candidate

Candidate artifact:

`reports/data-qualification/ba_native_bi5_binding_anomaly_candidate_2026-09-19.md`

Initial candidate commit:

`f2a0ae0e038bc3014a2e24a05e55b914783f37b6`

Candidate binding identity:

```text
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

Candidate anomaly matrix identity:

```text
A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD
A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

### Component envelope

B consumes conceptually:

```text
acquisition_domain_id
component_manifest_entry_id
instrument_id = USATECHIDXUSD
declared_hour_bucket_utc
compressed_payload_bytes
content_hash / provenance reference
```

A bare filesystem path is not sufficient semantic input.

Filename/path syntax is not normative UTC-hour authority.

### Candidate physical BI5 semantics

Selected as candidate from current repository implementation evidence:

```text
compression = one LZMA-Alone stream
framing origin = decompressed byte 0
record width = 20 bytes
layout = >IIIff
field order =
  millisecond_offset
  ask_price_raw
  bid_price_raw
  ask_volume_raw
  bid_volume_raw
```

Timestamp candidate:

```text
0 <= millisecond_offset < 3_600_000

market_timestamp
=
declared_hour_bucket_utc
+
millisecond_offset milliseconds
```

Price candidate:

```text
ask = ask_raw / 1000
bid = bid_raw / 1000
```

Volume candidate:

exact source IEEE-754 binary32 value with no scaling.

Opaque unit identity:

`DUKASCOPY_SOURCE_VOLUME_UNIT_V1_CANDIDATE`

No claim of lots/contracts/shares/exchange volume.

### Cardinality

Every complete, deterministically interpretable 20-byte slot:

```text
→ exactly one candidate M occurrence
```

Invalid/ambiguous input never becomes `C=0`.

Empty decompressed payload is BLOCKED, not presumed zero observations.

Cross-component record joining is forbidden.

### Occurrence provenance

Candidate physical locator:

```text
(component_manifest_entry_id, component_local_slot_index)
```

This is not:

- canonical record position;
- temporal precedence;
- market-event identity;
- cross-acquisition identity.

---

## 3. First B/A adversarial break

Artifact:

`reports/data-qualification/ba_native_bi5_candidate_adversarial_break_2026-09-19.md`

Initial break commit:

`5a48fb531d26323a5b22e52568c318161443ae14`

Initial candidate verdict:

`FAIL`

Exactly three demonstrated layering defects:

```text
BA-F01 — MARKET_SEMANTIC_VALIDITY_LEAK_INTO_BINDING
BA-F02 — PHYSICAL_SLOT_ORDER_USED_AS_TEMPORAL_AUTHORITY
BA-F03 — SAME_HOUR_COMPONENT_CARDINALITY_LEAKS_D_OWNERSHIP
```

### BA-F01

Initial B/A incorrectly rejected:

- zero price;
- ask < bid;
- finite negative volume.

These are deterministically decodable values and the upstream M contract does not define them as record-nonexistence conditions.

Market-quality semantics belong to Q or another explicit quality contract.

### BA-F02

Initial A treated:

```text
timestamp[i] < timestamp[i-1]
```

as qualification-blocking while also saying physical slot order is not temporal authority.

That was a temporal-layer leak.

### BA-F03

Initial B/A imposed a general one-component-per-hour assumption.

D owns acquisition component membership/multiplicity, so B cannot invent this upstream policy.

---

## 4. Minimal correction

Correction commit:

`678a8052c5b73fad8247d6a3f92173171c09111e`

Corrected candidate blob:

`25400abcc3a2a24438954ff27b970bd934313ae3`

Corrections:

1. zero/crossed prices are decoded by B and deferred to Q quality policy;
2. finite negative volume is decoded by B and deferred to Q;
3. only NaN/±Infinity remain B/A non-finite field anomalies;
4. timestamp regression in physical slot sequence is not a B/A anomaly by itself;
5. slot index remains provenance only;
6. D retains ownership of component multiplicity;
7. multiple same-hour components are allowed when D roles/provenance are explicit and non-ambiguous;
8. A blocks only ambiguous/conflicting component role/provenance.

No D/R/M artifact was changed.

No runtime was changed.

---

## 5. Final persisted-head re-break

Corrected candidate HEAD under re-break:

`678a8052c5b73fad8247d6a3f92173171c09111e`

Final adversarial re-break commit:

`e95583dab2a87d6ef1a19b57599f5f01118a19f1`

Final adversarial artifact blob:

`484860e09305a3088edb6b8b914803b8717a5627`

No additional internal candidate defect was demonstrated.

The full re-break covered:

- hour provenance;
- filename/path inference;
- compression fallback;
- concatenated/trailing stream ambiguity;
- empty decompressed payload;
- framing origin;
- terminal partial slot with/without completeness proof;
- field endian/order substitution;
- price scale substitution;
- millisecond boundary;
- non-finite volume;
- finite negative volume;
- zero/crossed price;
- strict duplicates;
- same-ms occurrences;
- timestamp regression;
- missing/extra/repeated components;
- multiple same-hour components;
- ambiguous component roles;
- cross-component fragment joining;
- unknown anomaly;
- parser disagreement;
- physical slot index leakage;
- permission leakage.

---

## 6. Current concrete A matrix

Current candidate classes include:

```text
BI5-A01 MISSING_DECLARED_COMPONENT
BI5-A02 UNDECLARED_COMPONENT_PRESENT
BI5-A03 REPEATED_OR_CONFLICTING_COMPONENT_DELIVERY
BI5-A04 AMBIGUOUS_OR_MISSING_HOUR_PROVENANCE
BI5-A05 DECOMPRESSION_FAILURE_OR_UNSUPPORTED_ENVELOPE
BI5-A06 ZERO_DECOMPRESSED_BYTES
BI5-A07 TERMINAL_PARTIAL_SLOT_WITHOUT_COMPLETENESS_PROOF
BI5-A08 TERMINAL_PARTIAL_SLOT_WITH_CONSTRUCTIVE_COMPLETENESS_PROOF
BI5-A09 MILLISECOND_OFFSET_OUT_OF_RANGE
BI5-A10 NON_FINITE_VOLUME_ENCODING
BI5-A11 AMBIGUOUS_COMPONENT_ROLE_OR_PROVENANCE
BI5-A12 REPRESENTATION_OR_BINDING_IDENTITY_MISMATCH
BI5-A13 UNKNOWN_ANOMALY_CLASS
```

Q-RM-10 mapping:

```text
constructively local INVALID
→ REJECT RECORD

non-local / ambiguous / unknown scope
→ QUALIFICATION BLOCKED
```

No default acquisition-fatal class has been introduced.

---

## 7. Remaining evidence blocker

The following provider-sensitive candidate facts currently have only implementation-derived evidence inside the repository:

```text
LZMA-Alone
20-byte width
>IIIff
field order
price /1000
binary32 volume fields
```

Therefore:

```text
B candidate formalization
= PERSISTED + CORRECTED + RE-BROKEN
= NO NEW INTERNAL DEFECT DEMONSTRATED

A candidate formalization
= PERSISTED + CORRECTED + RE-BROKEN
= NO NEW INTERNAL DEFECT DEMONSTRATED

B official gate = BLOCKED
A official gate = BLOCKED
```

No implementation-derived BI5 fact is promoted to provider truth merely because the candidate is internally consistent.

---

## 8. Global audit

The pre-backtest reconciliation audit was updated after B/A closure.

Commit:

`367472d4239db8cb3fc9242dd8d7bb266e1b0f1e`

Artifact:

`reports/data-qualification/pre_backtest_concrete_gate_reconciliation_2026-09-19.md`

---

## 9. Safety truth

```text
real data acquisition       = NOT AUTHORIZED
native BI5 download         = NOT AUTHORIZED
real BI5 processing         = NOT AUTHORIZED
massive acquisition         = NOT AUTHORIZED
real backtest               = NOT AUTHORIZED
positive P1.1 AUTHORIZED    = BLOCKED
paper / broker / live       = NOT AUTHORIZED
```

No real BI5 was downloaded or opened in this block.

---

## 10. Exactly one next governed action

Use the corrected, re-broken D/R/M/B/A candidate package only as input to formalize:

```text
Q — concrete qualification contract + parameters
```

Q must define the exact deterministic rule that maps B-produced candidate occurrences and A outcomes into the retained qualified logical universe.

Q must not:

- redefine B decoding;
- silently validate provider-sensitive B facts;
- use physical slot order as temporal authority;
- rewrite D membership;
- silently repair A anomalies;
- authorize acquisition;
- authorize real backtesting.

Provider-sensitive B evidence remains a separate blocker that must be closed before the final executable data gate can PASS.
