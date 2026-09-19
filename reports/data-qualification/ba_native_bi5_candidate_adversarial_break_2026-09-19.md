# B + A — ADVERSARIAL BREAK OF FIRST NATIVE BI5 CANDIDATE

**Date:** 2026-09-19  
**Candidate commit under attack:** `f2a0ae0e038bc3014a2e24a05e55b914783f37b6`  
**Candidate artifact:** `reports/data-qualification/ba_native_bi5_binding_anomaly_candidate_2026-09-19.md`

No acquisition, BI5 download, real-data read, or backtest occurred.

## 1. Attack basis

The persisted candidate was attacked against:

- corrected/re-broken D/R/M candidate;
- Q-RM-04 fail-closed/localisability rule;
- Q-RM-05 acquisition-domain ownership;
- Q-RM-06 binding precedence;
- Q-RM-09 concrete binding completeness;
- Q-RM-10 anomaly matrix requirements;
- acquisition-scoped occurrence identity;
- non-temporal/non-canonical M semantics.

The central rule under attack is:

```text
D owns acquisition membership
R owns representation selection
M owns logical occurrence semantics
B owns representation-specific physical→logical mapping
A classifies anomalies under B/Q-RM-10
Q owns retained qualification membership / quality policy
```

A lower layer must not silently legislate an upstream or downstream semantic rule.

---

# 2. B framing / decoding attacks

## B-A01 — Filename used as hour authority

Attack:

Implementation derives the UTC hour from `YYYY/MM/DD/HHh_ticks.bi5` and ignores declared provenance.

Candidate result:

**SURVIVES.**

The candidate requires a declared UTC hour bucket and explicitly rejects filename/path authority.

## B-A02 — Missing/conflicting hour provenance

Attack:

BI5 payload is valid but no unique declared UTC hour is available.

Candidate result:

**SURVIVES.**

Outcome is `QUALIFICATION BLOCKED`.

## B-A03 — Alternate codec fallback

Attack:

LZMA-Alone fails; implementation retries another codec.

Candidate result:

**SURVIVES.**

Fallback is forbidden.

## B-A04 — Concatenated/trailing compressed stream

Attack:

One valid LZMA-Alone stream is followed by another stream or undeclared compressed material.

Candidate result:

**SURVIVES as a candidate rule.**

The binding requires exactly one declared stream; ambiguity blocks.

## B-A05 — Zero decompressed bytes

Attack:

Implementation treats empty decompressed output as valid `C=0`.

Candidate result:

**SURVIVES.**

The candidate correctly blocks because no normative no-tick encoding has been established.

## B-A06 — Shifted framing origin

Attack:

Implementation starts 20-byte segmentation at byte 1 or after guessed header bytes.

Candidate result:

**SURVIVES.**

Binding fixes byte-zero origin and no header/footer.

## B-A07 — Terminal remainder

Attack:

`N mod 20 != 0`.

Candidate distinguishes:

- without constructive completeness proof → `QUALIFICATION BLOCKED`;
- with exact completeness/locality proof → `REJECT RECORD`.

This matches Q-RM-04's terminal-truncation rule.

**SURVIVES.**

## B-A08 — Cross-component fragment join

Attack:

Trailing bytes from component A are combined with leading bytes from B to make 20 bytes.

Candidate result:

**SURVIVES.**

Cross-component records are forbidden.

## B-A09 — Endianness / field-order substitution

Attack:

Little-endian, signed integer or reordered fields are accepted because values look plausible.

Candidate result:

**SURVIVES as an internally precise candidate.**

The factual correctness of `>IIIff` remains a separate evidence blocker because the repository currently has only one implementation-derived source for this candidate semantic.

## B-A10 — Price-scale substitution

Attack:

Implementation chooses /100, /10000 or symbol-dependent guess instead of /1000.

Candidate result:

**SURVIVES as an internally precise candidate.**

Again, external/independent corroboration remains required before B can PASS.

## B-A11 — ms boundary

Attack:

`3_599_999` and `3_600_000`.

Candidate result:

```text
3_599_999 → valid within hour
3_600_000 → local invalid slot → REJECT RECORD
```

Fixed 20-byte framing proves neighboring boundaries unaffected.

**SURVIVES.**

---

# 3. Boundary-leak attacks

## BA-F01 — MARKET_SEMANTIC_VALIDITY_LEAK_INTO_BINDING

Candidate currently makes the following B/A rules:

```text
ask_price_raw > 0
bid_price_raw > 0
ask_price >= bid_price

negative volume → REJECT RECORD
```

Attack:

Construct complete structurally valid 20-byte slots with:

- raw ask or bid equal to zero;
- decoded ask < bid;
- finite negative binary32 volume.

All fields still have one unambiguous deterministic binary interpretation under B.

Question:

Does the corrected upstream M contract say that such logical values are not market-tick occurrences?

Answer:

No.

M defines the logical fields and occurrence semantics, but does not currently declare price positivity, non-crossed quote semantics, or non-negative source volume as record-existence conditions.

The existing V4.3 probe flags some such conditions as data-integrity/quote checks, but that implementation is not normative authority and those checks are downstream quality semantics, not necessary byte-decoding semantics.

If B/A reject these slots now, the lower format layer silently changes the M candidate universe before Q exists.

Result:

**BREAK — MAJOR LAYERING DEFECT.**

Required correction:

B must decode deterministic field values without inventing market-quality membership.

At B/A level:

- raw uint32 price zero remains decodable;
- ask < bid remains decodable;
- finite negative binary32 volume remains decodable;
- these may later be classified by Q/quality policy, not rejected by B/A.

Only values that prevent construction of the declared logical numeric field itself — e.g. NaN/±Infinity if M requires a numeric real-valued volume — may remain binding-invalid, and even that must be stated as an interpretation-domain rule rather than market-quality rule.

---

## BA-F02 — PHYSICAL_SLOT_ORDER_USED_AS_TEMPORAL_AUTHORITY

Candidate currently defines:

```text
timestamp[i] < timestamp[i-1]
→ NATIVE_COMPONENT_TIMESTAMP_REGRESSION
→ QUALIFICATION BLOCKED
```

while simultaneously asserting:

```text
component-local slot index
≠ temporal ordering authority
```

Attack:

Two complete valid slots decode to timestamps 10:00:02 then 10:00:01 in physical source order.

B can still deterministically decode two logical tick candidates.

The corrected M contract is explicitly non-temporal, and the repository keeps final temporal ordering as a separate authority.

Using physical slot adjacency to block qualification assumes a representation-level chronology guarantee that has not been established by R or B evidence.

This is internally inconsistent:

```text
slot order is not temporal authority
but
slot order determines a temporal failure
```

Result:

**BREAK — TEMPORAL AUTHORITY LEAK.**

Required correction:

B must preserve source slot index as provenance and decoded market timestamps without silently sorting.

B/A must not declare timestamp regression an anomaly unless a separately evidenced representation contract establishes source sequence chronology as normative.

Temporal ordering/continuity remains a later Q/temporal-contract concern.

---

## BA-F03 — SAME_HOUR_COMPONENT_CARDINALITY_LEAKS D OWNERSHIP

Candidate states:

> the selected candidate representation does not support multiple normative components for the same instrument/hour unless D later supplies an explicit non-ambiguous role...

and A13 blocks unexplained same-hour multiplicity.

Attack:

A future D materialization explicitly declares two distinct components for the same hour with distinct manifest entry identities, but D has not yet frozen whether such physical partitioning is permitted.

Q-RM-05 says D owns acquisition component membership. Physical partitioning must not create or destroy the domain by B preference.

B may state how each declared component is decoded and whether records can cross component boundaries.

It must not silently decide how many declared components D may own for one hour unless that constraint is already part of R/D.

Current R candidate says "hourly BI5 component" but does not freeze a one-component-per-hour acquisition cardinality rule.

Result:

**BREAK — ACQUISITION-MEMBERSHIP OWNERSHIP LEAK.**

Required correction:

Remove the general one-component-per-hour prohibition from B.

Replace A13 with a narrower condition:

```text
AMBIGUOUS_COMPONENT_ROLE_OR_PROVENANCE
→ QUALIFICATION BLOCKED
```

If D explicitly declares multiple components with unique roles/provenance under a compatible representation, B interprets each independently. Whether their combined membership is valid belongs to D/Q.

---

# 4. A/Q-RM-10 attacks that survive

## A-A01 — missing declared component

**SURVIVES:** `QUALIFICATION BLOCKED`.

## A-A02 — undeclared component offered

**SURVIVES:** no silent admission; blocking is conservative while D membership is unresolved.

## A-A03 — repeated/conflicting delivery for same manifest entry

**SURVIVES:** no content-hash deduplication or arbitrary winner.

## A-A04 — decompression failure

**SURVIVES:** framing scope unknown → blocked.

## A-A05 — invalid millisecond offset in complete fixed slot

**SURVIVES:** constructively local → `REJECT RECORD`.

## A-A06 — NaN/Inf binary32 volume

The bit pattern is structurally decodable, but it cannot produce an ordinary finite real-valued logical volume without introducing non-real numeric semantics.

Candidate may retain this as a binding-level invalid field interpretation if M's logical volume is treated as a real numeric quantity.

**SURVIVES CONDITIONALLY**, but wording should be narrowed to NaN/±Infinity only and must not include finite negative values.

## A-A07 — strict duplicate slots

**SURVIVES:** separate slot provenance → separate candidate occurrences.

## A-A08 — same millisecond multiple occurrences

**SURVIVES:** permitted, distinct occurrences.

## A-A09 — unknown anomaly

**SURVIVES:** `QUALIFICATION BLOCKED`.

## A-A10 — parser disagreement

**SURVIVES:** parser behavior is non-authoritative; one implementation is non-conforming or the binding evidence is insufficient.

---

# 5. Qualification-evidence attack

## E-A01 — Single implementation evidence

Current concrete candidate facts:

```text
LZMA-Alone
20-byte width
>IIIff
field order
price /1000
binary32 volumes
```

are currently evidenced inside the repository by the V4.3 implementation surface.

That is enough to construct a falsifiable candidate, but not enough by itself to claim provider-semantic truth.

Result:

```text
candidate may remain formalized
official B gate must remain BLOCKED
```

This is not a candidate-internal contradiction and therefore is not classified as a formalization FAIL by itself.

---

# 6. Permission attacks

Any attempt to infer:

```text
B/A candidate exists
→ acquire BI5
→ process real BI5
→ backtest
```

is invalid.

Candidate result:

**SURVIVES.**

Permissions remain closed.

---

# 7. Verdict

The first persisted B/A candidate is not promoted.

```text
B/A FIRST NATIVE BI5 CANDIDATE
FAIL
```

Demonstrated defects:

1. `BA-F01 — MARKET_SEMANTIC_VALIDITY_LEAK_INTO_BINDING`
2. `BA-F02 — PHYSICAL_SLOT_ORDER_USED_AS_TEMPORAL_AUTHORITY`
3. `BA-F03 — SAME_HOUR_COMPONENT_CARDINALITY_LEAKS_D_OWNERSHIP`

No D/R/M mutation is authorized.

No runtime mutation is authorized.

No acquisition is authorized.

## 8. Authorized minimal correction

Correct only the B/A candidate:

1. remove price positivity, ask≥bid and finite-negative-volume rejection from B/A; defer those quality semantics to Q;
2. retain NaN/±Infinity handling only as a field-interpretation issue, with exact wording;
3. remove physical-slot timestamp regression as an A anomaly; preserve source slot index and timestamp without sorting;
4. remove the general one-component-per-hour prohibition;
5. replace A13 with ambiguity/conflicting-role blocking that respects explicit D membership.

Then persist and re-break the corrected candidate before opening Q.


---

# 9. Persisted-head re-break after minimal correction

**Corrected candidate HEAD:** `678a8052c5b73fad8247d6a3f92173171c09111e`  
**Corrected candidate blob:** `25400abcc3a2a24438954ff27b970bd934313ae3`

The branch was verified identical to that HEAD before re-break.

The same attack set was re-applied without changing the candidate during the attack.

## 9.1 Re-break BA-F01

Original defect:

`MARKET_SEMANTIC_VALIDITY_LEAK_INTO_BINDING`

Corrected candidate now separates deterministic decoding from later market-quality policy.

At B level:

```text
raw uint32 zero price
→ deterministic decoded price value

ask < bid
→ deterministic decoded pair

finite negative binary32 volume
→ deterministic decoded source-volume value
```

No record is rejected merely because of those market-quality properties.

Q or another later explicit market-quality contract may classify them.

NaN/±Infinity remain a B/A field-interpretation anomaly only because the current candidate logical volume is an ordinary finite real-valued quantity; no finite market-quality predicate is imported.

**RE-BREAK RESULT: SURVIVES.**

## 9.2 Re-break BA-F02

Original defect:

`PHYSICAL_SLOT_ORDER_USED_AS_TEMPORAL_AUTHORITY`

Corrected B preserves:

```text
component_local_slot_index
decoded market timestamp
```

without sorting and without declaring source slot order chronological.

Therefore:

```text
timestamp[i] < timestamp[i-1]
```

is physically decodable and no longer an A anomaly by itself.

Any chronological/continuity rule must be introduced later by Q/temporal authority.

**RE-BREAK RESULT: SURVIVES.**

## 9.3 Re-break BA-F03

Original defect:

`SAME_HOUR_COMPONENT_CARDINALITY_LEAKS_D_OWNERSHIP`

Corrected B now states:

```text
D owns component membership and multiplicity
B interprets each D-declared component independently
```

Multiple same-hour components are not rejected merely for multiplicity.

A now blocks only:

`AMBIGUOUS_COMPONENT_ROLE_OR_PROVENANCE`

where D/provenance cannot uniquely distinguish the declared roles.

**RE-BREAK RESULT: SURVIVES.**

## 9.4 Full adversarial re-break

```text
filename/path as hour authority                         REJECTED / SURVIVES
missing/conflicting declared hour provenance            BLOCKED / SURVIVES
alternate codec fallback                                REJECTED / SURVIVES
concatenated/trailing undeclared compression            BLOCKED / SURVIVES
zero decompressed bytes                                 BLOCKED / SURVIVES
shifted framing origin                                  REJECTED / SURVIVES
terminal partial without completeness proof             BLOCKED / SURVIVES
terminal partial with constructive completeness proof   REJECT RECORD / SURVIVES
little-endian/signed/reordered fields                    NON-CONFORMING / SURVIVES
price scale substitution                                NON-CONFORMING / SURVIVES
ms = 3_599_999                                          VALID B OFFSET / SURVIVES
ms = 3_600_000                                          LOCAL REJECT RECORD / SURVIVES
NaN / ±Infinity volume                                  LOCAL REJECT RECORD / SURVIVES
finite negative volume                                  DECODED; Q DEFERRED / SURVIVES
zero price                                              DECODED; Q DEFERRED / SURVIVES
ask < bid                                               DECODED; Q DEFERRED / SURVIVES
strict duplicate slots                                  DISTINCT OCCURRENCES / SURVIVES
same-ms distinct slots                                  DISTINCT OCCURRENCES / SURVIVES
timestamp regression in physical slot sequence          DECODED; TEMPORAL Q DEFERRED / SURVIVES
missing declared component                              BLOCKED / SURVIVES
undeclared offered component                            BLOCKED / SURVIVES
repeated/conflicting manifest entry                     BLOCKED / SURVIVES
multiple same-hour components with clear D roles        ALLOWED BY B / SURVIVES
ambiguous component roles/provenance                    BLOCKED / SURVIVES
cross-component fragment joining                        FORBIDDEN / SURVIVES
unknown anomaly                                         BLOCKED / SURVIVES
physical slot index promoted to canonical identity      FORBIDDEN / SURVIVES
physical slot index promoted to temporal authority      FORBIDDEN / SURVIVES
parser/library disagreement                             CONFORMANCE FAILURE / SURVIVES
acquisition/backtest permission inference               FORBIDDEN / SURVIVES
```

No additional internal candidate defect was demonstrated.

## 9.5 Remaining evidence blocker

The candidate is now structurally precise enough to serve as the governed B/A candidate input to the next block.

However, the repository currently has only implementation-derived evidence for these provider-sensitive facts:

```text
LZMA-Alone envelope
20-byte decompressed slot width
>IIIff big-endian layout
field order
price raw / 1000
source binary32 volume fields
```

Therefore the result is deliberately:

```text
B/A candidate formalization
= PERSISTED + CORRECTED + RE-BROKEN
= NO NEW INTERNAL DEFECT DEMONSTRATED

B official gate
= BLOCKED

A official gate
= BLOCKED
```

The remaining B/A BLOCKED state is not caused by an unresolved internal contradiction in the current candidate.

It is caused by insufficient independent/provider-sensitive qualification evidence plus the still-unmaterialized D acquisition.

No factual BI5 claim is upgraded to PASS by repetition of the V4.3 implementation.

## 9.6 Boundary for next work

The corrected B/A candidate may be consumed as candidate input for:

```text
Q — concrete qualification contract + parameters
```

but Q must not:

- silently validate provider-sensitive B facts;
- redefine B decoding semantics;
- make physical slot order temporal authority;
- introduce D membership rules;
- authorize acquisition or backtesting.

If Q requires a semantic change to D/R/M/B/A, Q must FAIL/BLOCK rather than mutate upstream contracts silently.
