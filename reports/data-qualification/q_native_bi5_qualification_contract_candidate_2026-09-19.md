# Q — FIRST CONCRETE NATIVE-BI5 QUALIFICATION CONTRACT CANDIDATE

**Date:** 2026-09-19  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `68e4563369d47b370464014bae867e63256a3846`  
**Input D/R/M candidate blob:** `2249bea6dbf6b5a8e0d49b99a93bf16248f9c0e9`  
**Input B/A candidate blob:** `25400abcc3a2a24438954ff27b970bd934313ae3`  
**Scope:** formalization only — no acquisition, no real BI5 processing, no freeze implementation, no backtest, no permission increase.

## 0. Purpose

This artifact defines the first concrete candidate for:

```text
B candidate occurrences
+
A normative anomaly outcomes
+
complete D materialization state
        ↓
Q deterministic qualification membership
        ↓
retained qualified logical occurrence universe
or
qualification BLOCKED / acquisition rejected
```

Official gate verdict remains:

```text
Q = BLOCKED
```

until the candidate survives governed adversarial qualification and the upstream concrete evidence required by D/B/A exists.

---

# 1. Strict ownership boundaries

Q may decide:

- whether the complete declared acquisition is eligible to produce a qualified universe;
- whether a B-produced candidate occurrence belongs to the retained qualified logical universe;
- how A outcomes affect qualification;
- qualification parameters capable of changing membership.

Q may not redefine:

- D component membership;
- R representation identity;
- M logical payload semantics;
- B decompression/framing/field decoding/cardinality;
- A anomaly trigger/localisability/outcome;
- canonical enumeration;
- temporal precedence;
- observation identity composition;
- acquisition or backtest authorization.

Therefore:

```text
Q membership
≠ B decoding

Q membership
≠ canonical position

Q membership
≠ temporal ordering

Q qualification PASS
≠ acquisition authorization
≠ real backtest authorization
```

---

# 2. Candidate identity

```text
qualification_contract_id =
Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP

qualification_contract_version =
Q_DUKASCOPY_USATECHIDXUSD_NATIVE_BI5_STRUCTURAL_MEMBERSHIP_V0_1_CANDIDATE
```

Applicable only with the exact candidate tuple:

```text
D =
D_DUKASCOPY_USATECHIDXUSD_BOUNDED_RESEARCH_ACQUISITION_DECLARATION_V0_1

R =
DUKASCOPY_NATIVE_BI5_HOURLY_TICKS_V1_CANDIDATE

M =
PRIMARY_MARKET_TICK_LOGICAL_RECORD_MODEL_V1_CANDIDATE

B =
B_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE

A =
A_DUKASCOPY_NATIVE_BI5_USATECHIDXUSD_V0_1_CANDIDATE
```

No nearest-version fallback or implicit upgrade is permitted.

---

# 3. Qualification parameters

The candidate parameters are explicit and immutable for this Q version:

```text
unknown_anomaly_policy
= QUALIFICATION_BLOCKED

qualification_blocked_policy
= NO_QUALIFIED_UNIVERSE

reject_acquisition_policy
= NO_QUALIFIED_UNIVERSE

reject_record_policy
= EXCLUDE_ONLY_NORMATIVELY_TARGETED_PHYSICAL_RECORD_OR_FRAGMENT

strict_duplicate_policy
= PRESERVE_DISTINCT_OCCURRENCES

same_timestamp_policy
= PRESERVE_DISTINCT_OCCURRENCES

market_value_filter_policy
= NONE_IN_Q_V0_1

source_slot_temporal_policy
= NO_TEMPORAL_AUTHORITY

canonical_enumeration_policy
= NONE_IN_Q

partial_domain_policy
= FORBIDDEN

warmup_membership_policy
= RETAIN_IF_D_MEMBER_AND_B_CANDIDATE

evaluation_window_filter_policy
= NOT_A_Q_MEMBERSHIP_FILTER

silent_repair_policy
= FORBIDDEN
```

Any change capable of changing retained membership requires a distinct Q version.

---

# 4. Required complete qualification input

Q operates only on a complete declared acquisition qualification package.

Conceptually:

```text
QualificationInput
- exact D declaration/materialization identity
- exact R identity/version
- exact M version
- exact B identity/version
- exact A identity/version
- complete declared component manifest
- completeness evidence
- B interpretation report for every declared materialized component
- A outcome registry for every detected anomaly
- all B candidate occurrences
- all rejected physical record/fragment diagnostics
```

Q does not infer missing components from directories, filenames, URLs or traversal.

If D is not materially complete:

`QUALIFICATION BLOCKED`.

The current repository has no actual D materialization, so this candidate cannot yet execute against real data.

---

# 5. Normative outcome domains

## 5.1 Acquisition qualification outcome

Exactly one:

```text
QUALIFIED
QUALIFICATION_BLOCKED
ACQUISITION_REJECTED
```

No `UNKNOWN` result may later be treated as qualified.

## 5.2 Candidate occurrence membership

When and only when acquisition outcome is `QUALIFIED`, each B-produced candidate occurrence has exactly one membership outcome:

```text
RETAINED
REJECTED_BY_Q
```

For Q V0.1 candidate:

`REJECTED_BY_Q` has no active value-based rule.

Therefore, absent a future explicit Q-version change, every valid B-produced candidate occurrence is retained unless a consistency contradiction prevents qualification.

## 5.3 A `REJECT RECORD` is not automatically a Q candidate occurrence

A local malformed slot/fragment may never have produced a valid B candidate occurrence.

Q must preserve the distinction:

```text
physical record/fragment rejected by A
≠
B candidate occurrence rejected by Q
```

Q records the A rejection evidence but does not manufacture a logical occurrence merely to reject it.

---

# 6. Total acquisition-level decision rule

Q evaluates acquisition-level outcomes before producing a normative retained universe.

Precedence:

```text
1. any acquisition-fatal A outcome
   → ACQUISITION_REJECTED
   → no qualified universe

2. else any QUALIFICATION BLOCKED A outcome
   → QUALIFICATION_BLOCKED
   → no qualified universe

3. else incomplete / contradictory D/B/A qualification package
   → QUALIFICATION_BLOCKED
   → no qualified universe

4. else
   → QUALIFIED
   → candidate membership may be finalized
```

Current A candidate declares no default acquisition-fatal class, so path 1 is reserved for future compatible A versions and is not activated by inference.

No successfully parsed prefix may survive as the normative qualified universe when the acquisition outcome is blocked/rejected.

---

# 7. Exact A-target binding

Q accepts an A outcome only when its target is normatively bound to the B/D framing domain.

Permitted target forms are:

## 7.1 Complete fixed-width slot target

```text
target_scope = COMPLETE_SLOT

component_manifest_entry_id
component_local_slot_index
```

The index must satisfy:

```text
0 <= component_local_slot_index < complete_slot_count
```

for that exact component/B interpretation report.

## 7.2 Terminal fragment target

```text
target_scope = TERMINAL_FRAGMENT

component_manifest_entry_id
terminal_fragment_start_offset
terminal_fragment_length
```

For B V0.1 candidate:

```text
terminal_fragment_start_offset = 20 * complete_slot_count
terminal_fragment_length       = decompressed_length mod 20
```

A terminal fragment is not a complete slot and receives no candidate logical occurrence.

## 7.3 Whole-component target

```text
target_scope = COMPONENT

component_manifest_entry_id
```

Used only for anomalies whose normative scope is the entire declared component.

## 7.4 Acquisition-scope target

```text
target_scope = ACQUISITION

acquisition_domain_id
```

Used for acquisition-membership/completeness anomalies where no narrower target is normative.

The following are never sufficient normative targets:

- filename/path;
- traversal index;
- worker-local index;
- parser row number;
- free-text diagnostic;
- diagnostic list order;
- content equality/hash alone.

Target locators are provenance/anomaly evidence only.

They are not promoted to canonical observation identity or temporal authority.

If an A outcome target is absent, ambiguous, out of range, contradictory, or incompatible with its declared scope:

`QUALIFICATION BLOCKED`.

---

# 8. Per-component physical accounting invariant

For every D-declared component whose B framing is deterministically available and whose component-level semantics are not already globally blocked, Q requires exhaustive accounting of every complete B slot.

For B V0.1 candidate, define:

```text
S_all
=
{0, 1, ..., complete_slot_count - 1}

S_candidate
=
slot indices that produced valid B candidate occurrences

S_rejected
=
slot indices targeted by A outcome REJECT RECORD
```

Before acquisition outcome may become `QUALIFIED`, Q requires:

```text
S_candidate ∩ S_rejected = ∅

S_candidate ∪ S_rejected = S_all
```

and additionally:

- every index occurs at most once in `S_candidate`;
- every index occurs at most once in `S_rejected`;
- no index lies outside `S_all`;
- every candidate occurrence references exactly one member of `S_candidate`;
- every slot-level `REJECT RECORD` outcome references exactly one member of `S_rejected`;
- terminal partial fragments are accounted separately and never inserted into `S_all`;
- component/acquisition blocking outcomes prevent qualification and therefore prevent a normative partial accounting result from becoming U.

This is a conservation/conformance rule over B/A output.

It does not redefine B framing.

If one complete slot is omitted from both sides, appears in both sides, appears twice, or is targeted inconsistently:

`QUALIFICATION BLOCKED`.

---

# 9. A outcome consumption

Current A outcomes are consumed exactly as follows.

## 7.1 `REJECT RECORD`

Examples under current A:

- terminal partial slot with constructive completeness/locality proof;
- millisecond offset outside hour;
- NaN / ±Infinity source volume.

Q rule:

```text
A = REJECT RECORD
→ preserve rejection diagnostic
→ targeted physical record/fragment contributes no retained occurrence
→ continue only if no acquisition-level blocking condition exists
```

No repair, substitution or invented replacement occurrence.

## 7.2 `QUALIFICATION BLOCKED`

Examples:

- missing declared component;
- undeclared offered component;
- repeated/conflicting component delivery;
- missing/ambiguous hour provenance;
- decompression/envelope ambiguity;
- zero decompressed bytes;
- terminal partial without constructive completeness proof;
- ambiguous component role/provenance;
- version mismatch;
- unknown anomaly class.

Q rule:

```text
one QUALIFICATION BLOCKED outcome anywhere in declared D
→ whole Q result = QUALIFICATION_BLOCKED
→ no normative retained universe
→ no partial/prefix freeze
```

## 7.3 `REJECT ACQUISITION`

If a future compatible A version explicitly marks an anomaly acquisition-fatal:

```text
→ ACQUISITION_REJECTED
→ no normative retained universe
```

Q cannot invent acquisition-fatality.

---

# 10. Candidate occurrence consistency checks

Before retention, Q verifies conformance relationships without redefining B.

## 10.1 Exact upstream tuple

Every candidate and diagnostic must refer to the exact D/R/M/B/A versions selected by this Q contract.

Mismatch:

`QUALIFICATION BLOCKED`.

## 10.2 Declared component provenance

Every B candidate occurrence must trace to one D-declared `component_manifest_entry_id`.

Undeclared provenance:

`QUALIFICATION BLOCKED`.

## 10.3 One B slot source cannot appear twice by execution duplication

A B candidate occurrence carries physical provenance sufficient to identify its source slot inside its declared component:

```text
(component_manifest_entry_id, component_local_slot_index)
```

Q may use this tuple as a **conformance uniqueness key for one qualification execution** only.

If the exact same source slot is emitted twice by the qualification implementation:

`QUALIFICATION BLOCKED`.

This does not make the tuple the final normative observation identity.

## 10.4 Strict logical duplicates remain distinct

If two different source slots produce identical logical payloads:

```text
source_locator(A) != source_locator(B)
payload(A) = payload(B)
```

then both are retained when acquisition qualification succeeds.

No content deduplication.

## 10.5 Candidate/rejection contradiction

If the same physical source slot is simultaneously presented as:

- a valid B candidate occurrence; and
- an A `REJECT RECORD` target,

then upstream interpretation is contradictory.

Outcome:

`QUALIFICATION BLOCKED`.

Q does not choose one interpretation.

---

# 11. Q V0.1 market-value policy

Q V0.1 intentionally introduces **no additional market-value membership filter**.

Therefore these B-decoded finite values are not rejected solely by Q:

```text
ask = 0
bid = 0
ask < bid
finite negative source volume
same timestamp as another occurrence
timestamp decrease relative to previous physical slot
```

This is deliberate, not accidental permissiveness.

Reason:

- B can decode these values deterministically;
- current authoritative corpus does not yet establish a concrete market-quality membership rule for them;
- physical slot order is not temporal authority;
- silently rejecting them would invent a Q policy from V4.3 implementation checks.

If the first real research consumer requires stricter price/quote/volume admissibility, that policy must be explicitly versioned either:

1. as a new Q qualification version if it changes retained membership; or
2. as a separately governed consumer eligibility contract if it does not redefine the qualified universe.

No hidden threshold or parser default is permitted.

---

# 12. Warmup and evaluation-window semantics

The D candidate acquisition domain contains:

```text
mandatory warmup prefix
+
frozen five-year evaluation window
```

Q does not discard warmup occurrences merely because they are outside the evaluated performance interval.

If they belong to D and satisfy B/A/Q:

`RETAINED`.

Therefore:

```text
qualified logical universe
may contain warmup occurrences
+
evaluation-window occurrences
```

The later research run must use the frozen evaluation-window boundary when computing reported performance.

Q membership does not silently redefine the research evaluation interval.

---

# 13. Temporal non-authority

Q V0.1 does not establish chronology.

It does not sort by:

- market timestamp;
- component hour;
- slot index;
- manifest order;
- filename/path;
- runtime traversal order.

It does not reject a candidate solely because its timestamp is lower than a previously traversed candidate timestamp.

Temporal ordering remains owned by the applicable temporal/ordered-ticks contract.

Thus:

```text
Q retained membership
≠ ordered tick sequence
```

---

# 14. No canonical enumeration / identity invention

Q decides membership and preserves candidate individuality.

Q does not assign:

- `CANONICAL_RECORD_POSITION`;
- global ordinal;
- stable row number;
- content-derived ID;
- market-event identity;
- cross-acquisition identity.

The physical source locator may be preserved as provenance/conformance evidence.

It is not silently promoted to canonical observation identity.

---

# 15. Determinism requirements

Given the same complete normative input tuple:

```text
D + R + M + B + A + Q
```

two conforming qualification implementations must produce the same:

- acquisition outcome;
- set/multiset of retained logical candidate occurrences;
- set of A-rejected physical record/fragment diagnostics;
- strict duplicate multiplicity;
- no-qualified-universe state when blocked/rejected.

They may differ in:

- traversal order;
- worker allocation;
- memory layout;
- output serialization order;
- parser/library implementation;

provided semantic membership/individuality is unchanged.

---

# 16. Q output concept

A future executable Q implementation must produce enough structured result to support F/O without introducing canonical enumeration.

Conceptually:

```text
QualificationResult
- qualification_contract_id
- qualification_contract_version
- exact D/R/M/B/A references
- acquisition_outcome
- retained_occurrence_count
- rejected_physical_record_count
- anomaly_outcome_summary
- retained occurrence snapshots/provenance sufficient for later F
- rejection diagnostics
- qualification limitations
```

When acquisition outcome is not `QUALIFIED`:

```text
retained_occurrence_count
must not be presented as a normative qualified-universe count

no frozen qualified universe may be emitted
```

Exact F serialization is deliberately not selected here.

---

# 17. Version-change triggers

A new Q version is mandatory if a change can alter:

- acquisition qualification precedence;
- interpretation of A outcomes;
- retained candidate membership;
- market-value filters;
- strict duplicate handling;
- warmup membership;
- partial-domain policy;
- candidate/rejection contradiction policy;
- any membership-affecting parameter.

A reporting-only change proven not to affect membership may retain Q version.

---

# 18. Evidence limitations / current blocked state

Even if this Q candidate is internally coherent, real Q execution currently remains impossible because:

1. D has no materialized acquisition instance, manifest or completeness evidence;
2. B/A provider-sensitive semantics remain officially BLOCKED pending independent/provider-sensitive evidence;
3. no executable Q implementation exists;
4. no F persistence artifact exists.

Therefore:

```text
Q candidate formalization
≠ Q PASS

Q official gate
= BLOCKED
```

---

# 19. Pre-break verdict state

```text
Q candidate
= PERSISTED FORMALIZATION CANDIDATE

Q official gate
= BLOCKED

real acquisition
= NOT AUTHORIZED

real BI5 processing
= NOT AUTHORIZED

real backtest
= NOT AUTHORIZED
```

---

# 20. Next governed action

Adversarially break this exact persisted Q candidate before any F/O work.

Attack at minimum:

- one A `QUALIFICATION BLOCKED` after many valid candidates;
- one future `REJECT ACQUISITION`;
- local A `REJECT RECORD` with no B candidate object;
- same source slot emitted twice;
- strict duplicate payloads from different source slots;
- same source slot both candidate and rejected;
- missing D component with otherwise valid prefix;
- undeclared component silently ignored;
- warmup occurrence silently dropped;
- evaluation-window occurrence silently extended/filtered;
- zero/crossed price hidden rejection;
- finite negative volume hidden rejection;
- timestamp regression hidden rejection/sort;
- traversal-order dependence;
- content-hash deduplication;
- blocked acquisition emitting partial U;
- Q inventing canonical identity;
- Q overriding A outcome;
- Q repairing B value;
- upstream version mismatch;
- permission leakage.

No data acquisition is permitted during the break.


---

# 21. Correction record after first adversarial break

Adversarial artifact:

`reports/data-qualification/q_native_bi5_qualification_contract_adversarial_break_2026-09-19.md`

The first persisted Q candidate failed on exactly two demonstrated completeness defects:

```text
Q-F01 — ANOMALY_TARGET_BINDING_UNDERSPECIFIED
Q-F02 — PHYSICAL_SLOT_ACCOUNTING_NOT_TOTAL
```

Corrections applied:

1. every A outcome now requires an exact normative target scope;
2. complete-slot targets use exact `component_manifest_entry_id + component_local_slot_index`;
3. terminal fragments use exact component + start offset + length;
4. component/acquisition anomalies use explicit component/acquisition targets;
5. filename/path/free-text/runtime-order targeting is forbidden;
6. every deterministically framed complete slot must be accounted exactly once as B candidate or A `REJECT RECORD`;
7. candidate and rejected slot sets must be disjoint and exhaustive;
8. terminal fragments remain outside complete-slot accounting;
9. any accounting contradiction or omission blocks qualification.

No D/R/M/B/A semantics were changed.

Official gate verdict remains:

```text
Q = BLOCKED
```

The corrected candidate requires persisted-head adversarial re-break before any F/O work.
