# F — NATIVE BI5 FREEZE-PERSISTENCE IMPLEMENTATION CANDIDATE — ADVERSARIAL BREAK

**Date:** 2026-09-19  
**Initial implementation commit:** `e83169226578040eb52bef45e65813e54c44b3f5`  
**Initial qualification-runner commit:** `0b09b8055c88f829d0f1ebac29b834d62730b56c`

Production source:

`src/native_bi5_freeze_persistence.py`

Initial source blob:

`7bf05f9383252f8bcfe3db06d08b2d0c2cc550ad`

Frozen F breaker:

`breakers/native_bi5_f_freeze_persistence_breaker.py`

Frozen breaker blob:

`3d9eb75c2f4e988c984da67af0af344d3dc24148`

Executable O implementation remains absent.

No real BI5 input, acquisition or backtest was used.

## 1. Initial executable qualification

Workflow:

`Native BI5 F Freeze Persistence Candidate`

Run:

```text
run = 35454862558
job = 105928242031
```

Controls:

```text
exact F source / frozen breaker / contract locks = PASS
O implementation absent                          = PASS
qualification environment                        = PASS
clean worktree                                   = PASS
```

Frozen breaker result:

```text
24 passed
12 failed
```

Initial candidate verdict:

```text
F FREEZE-PERSISTENCE IMPLEMENTATION CANDIDATE = FAIL
```

## 2. F-F01 — ACCOUNTING_WITNESS_SHAPE_OVERRESTRICTION

### Demonstrated behavior

A valid qualified synthetic input was emitted as:

```text
QUALIFICATION_TERMINAL_EVIDENCE
NOT_CREATED
```

instead of:

```text
QUALIFIED_UNIVERSE_FREEZE
FROZEN
```

The failure propagated into the duplicate, ordering, serialization, determinant-change and validation tests.

### Root cause

The candidate helper for a pure source witness requires exactly:

```text
component_manifest_entry_id
component_local_slot_index
```

That exact-shape rule is correct for:

```text
retained_occurrence.source_witness
```

but the same helper was incorrectly reused for:

```text
source_accounting entry
```

whose normative shape also contains:

```text
disposition
anomaly_class_id
```

Therefore valid complete-slot accounting was rejected merely because it carried its required disposition semantics.

The same over-reuse also affects COMPLETE_SLOT anomaly targets, whose shape additionally contains `target_scope`.

### Why this is a real implementation defect

F owns persistence of several different relations that share a source locator but do not share the same object shape.

Therefore:

```text
source locator fields
≠ whole-object schema
```

Requiring the whole accounting/anomaly object to equal the pure witness schema confuses locator validation with relation-schema validation.

### Verdict

```text
F-F01 = FAIL
```

### Authorized minimal correction

Keep the exact-shape rule for retained-occurrence `source_witness`.

For accounting and COMPLETE_SLOT anomaly targets:

- validate their own full relation shape;
- extract and validate only the two locator fields as a locator;
- do not force the whole object through the pure-witness schema.

No F contract semantics, frozen breaker, O implementation or permission boundary may change.

## 3. Current state

```text
F test-first breaker/harness = PASS
F production candidate       = FAIL
F global gate                = BLOCKED
O implementation             = ABSENT
O global gate                = BLOCKED
```

Exactly authorized next action:

```text
fresh HEAD
→ correct F-F01 only
→ update candidate workflow source lock
→ persisted frozen-breaker re-run
→ adversarially attack the corrected implementation
```

No real BI5 data/acquisition/backtest is authorized.


---

## 4. Supplemental adversarial break

Supplemental breaker:

`breakers/native_bi5_f_freeze_persistence_adversarial.py`

Initial supplemental breaker blob:

`ebbaa838a86e52066d40265a3d86fa57175077ec`

Workflow:

`Native BI5 F Freeze Persistence Adversarial`

Run:

```text
run = 35455081310
job = 105928820762
```

Results:

```text
frozen F breaker       = 36 passed
supplemental adversary = 22 failed
```

All exact source/breaker locks, O-absence proof, qualification-environment checks and clean-worktree checks passed.

The supplemental failures demonstrate the following additional implementation defects.

### F-F02 — UNQUALIFIED_A08_PROOF_ACCEPTANCE

A self-described A08 evidence object with the right field names and target binding is accepted as if constructive completeness had been independently qualified.

Current behavior:

```text
shape-valid self-described proof
→ BI5-A08 accepted
→ QUALIFIED_UNIVERSE_FREEZE
```

Required current behavior:

```text
A08 constructive-proof verifier not qualified
→ positive A08 path unavailable
→ NOT_CREATED
```

This preserves the already-governed fail-closed limitation shared by I_A/I_B.

### F-F03 — QUALIFIED_STATE_ACCEPTS_BLOCKING_OR_INVALID_ANOMALY

A `QUALIFIED` input can currently freeze while containing:

- BI5-A06 with `QUALIFICATION_BLOCKED`;
- BI5-A13 recast as `REJECT_RECORD`.

F therefore does not prove that the anomaly relation is compatible with the claimed Q outcome.

For the current candidate and current A08 limitation, a qualified freeze may contain local record rejections only for the exact locally rejectable classes already authorized by A/Q.

### F-F04 — NORMATIVE_DETERMINANT_ID_VERSION_NOT_BOUND

The reconstruction tuple currently validates:

- exact stage set;
- non-empty strings;
- exact F identity/version;

but D/R/M/B/A/Q identities can otherwise be replaced by arbitrary non-empty values.

Demonstrated attacks include wrong normative IDs for D/R/M/B/A/Q, wrong versions for R/M/B/A/Q, and a D binding version inconsistent with `acquisition_declaration_version`.

This violates reconstruction of the exact concrete qualification state.

### F-F05 — ANOMALY_MATRIX_VERSION_NOT_BOUND

A local A09 rejection can be frozen with an arbitrary `anomaly_matrix_version`.

The anomaly relation must bind the exact A determinant version already frozen in the reconstruction tuple.

### F-F06 — RFC3339_SHAPE_WITHOUT_CALENDAR_VALIDITY

The timestamp validator currently accepts strings that match the textual pattern but do not denote a real UTC instant, for example:

`2026-99-99T99:99:99.999Z`

F must preserve an exact valid RFC3339 UTC timestamp, not merely its visual shape.

### F-F07 — BINARY32_NORMAL_FORM_NOT_PROVEN_REPRESENTABLE

The candidate checks:

- integer coefficient/exponent;
- odd non-zero coefficient;
- canonical zero.

It does not prove that the pair is representable by a finite binary32 source value.

Demonstrated invalid accepted examples include:

```text
16777217 * 2^0
1 * 2^128
1 * 2^-150
```

The exact finite binary32 normal form must remain inside the representable binary32 domain.

### F-F08 — PRICE_NUMERATOR_UINT32_DOMAIN_NOT_ENFORCED

The current price-rational validator accepts arbitrary Python integers with denominator 1000.

But B defines ask/bid raw prices from unsigned 32-bit integers before division by 1000.

Demonstrated accepted invalid values:

```text
-1
4294967296
```

F must reject any numerator outside:

```text
0 <= numerator <= 4294967295
```

## 5. Corrected candidate status before next mutation

```text
frozen F breaker = PASS
supplemental adversarial breaker = FAIL
F implementation candidate = FAIL
F global gate = BLOCKED
O implementation = ABSENT
```

Exactly authorized next correction:

```text
correct F-F02..F-F08 only
→ keep frozen F breaker unchanged
→ keep supplemental attacks unchanged
→ update source hash locks only
→ run frozen + supplemental breakers on persisted HEAD
→ adversarial re-break
```

No production O implementation, real BI5 input, acquisition or backtest is authorized.


---

## 6. Residual adversarial re-break after F-F02..F-F08

Correction commit:

`a2a1c57a5a3d412a49bc9d2e43cb9e74b7f1c672`

Corrected source blob:

`631a17f60a58112819529294db2c35546a2edfd7`

Executable results:

```text
candidate run = 35455182386
frozen F breaker = 36 passed

adversarial run = 35455182381
frozen F breaker       = 36 passed
supplemental adversary = 22 passed
```

All exact source/breaker locks, O-absence checks, qualification-environment checks and clean-worktree checks passed.

F-F02..F-F08 are materially corrected.

A fresh adversarial review nevertheless demonstrates additional residual defects.

### F-R01 — ANOMALY_RELATION_IS_NOT_EXACTLY_EQUAL_TO_REJECT_ACCOUNTING

The implementation proves:

```text
every rejected accounting slot
has a matching anomaly relation
```

but it does not prove the converse.

Therefore a `QUALIFIED` state may include an extra BI5-A09/A10 anomaly targeting a source slot that accounting still marks `CANDIDATE_RETAINED`.

It may also preserve duplicate local anomaly entries for one rejected source.

F requires the exact physical→logical accounting/anomaly relation, not a superset.

Verdict:

```text
F-R01 = FAIL
```

Required correction:

the normalized local anomaly relation must be duplicate-free and exactly equal to the rejected-slot accounting relation.

### F-R02 — COMPONENT_SNAPSHOT_CONCRETE_DOMAIN_NOT_ENFORCED

Component reconstruction currently requires non-empty:

- `declared_role`;
- `instrument_source_identity`;
- `declared_hour_bucket_utc`.

It does not enforce the concrete F candidate domain:

```text
declared_role = HOURLY_NATIVE_BI5_TICKS
instrument/source = DUKASCOPY/USATECHIDXUSD
declared hour = valid exact UTC hour bucket
```

Arbitrary non-empty replacements can therefore be frozen.

Verdict:

```text
F-R02 = FAIL
```

### F-R03 — ZERO_SLOT_NO_FRAGMENT_QUALIFIED_COMPONENT_BYPASSES_A06

For this fixed 20-byte framing:

```text
complete_slot_count = 0
terminal_fragment = null
```

represents no decompressed framed bytes.

Under the frozen A matrix that is the A06 zero-decompressed-bytes blocking condition, not a valid qualified zero-cardinality component.

The current F validator accepts it in a `QUALIFIED` construction.

Verdict:

```text
F-R03 = FAIL
```

### F-R04 — JSON_DUPLICATE_KEY_AMBIGUITY_ACCEPTED

`deserialize_freeze_artifact` currently delegates to the default JSON object parser.

Duplicate object keys are therefore resolved by parser behavior rather than rejected as ambiguous persistence input.

That violates the no-parser-default authority boundary.

Verdict:

```text
F-R04 = FAIL
```

Required correction:

reject duplicate JSON object keys during deserialization.

### F-R05 — NONFINITE_OR_NONSTRICT_JSON_VALUE_CAN_ESCAPE_PERSISTENCE_BOUNDARY

Python JSON defaults permit non-standard `NaN` serialization/parsing.

A non-finite value placed in a persisted non-semantic field such as qualification parameters can therefore produce a nominal F artifact that is not strict interoperable JSON.

The selected persistence envelope is UTF-8 JSON; F must fail closed on non-strict JSON values.

Verdict:

```text
F-R05 = FAIL
```

Required correction:

- use strict JSON encoding with `allow_nan=False`;
- reject `NaN`, `Infinity`, and `-Infinity` on deserialize;
- if a qualified construction cannot be represented as strict JSON, emit terminal `NOT_CREATED` rather than escape with an exception or non-standard artifact.

## 7. Second authorized implementation correction

Correct only F-R01..F-R05.

The frozen F breaker remains unchanged.

Extend the supplemental adversarial breaker only to encode these newly demonstrated residual attacks.

O remains absent.

No real BI5 data/acquisition/backtest is authorized.


---

## 8. Executable residual break

Extended supplemental breaker blob:

`78dd9b8d35214fe5723986b51d44ff574257353b`

Workflow run:

```text
run = 35455338472
job = 105929494462
```

Results:

```text
frozen F breaker = 36 passed
extended supplemental breaker = 8 failed / 22 passed
```

The eight failures map exactly to the previously identified residual defect set:

```text
F-R01 — extra/duplicate local anomaly relation accepted
F-R02 — wrong role/source/hour accepted
F-R03 — qualified zero-slot/no-fragment component accepted
F-R04 — duplicate JSON object key accepted
F-R05 — NaN accepted into nominal JSON freeze
```

All source/breaker hash locks, O-absence checks, qualification-environment checks and clean-worktree checks passed.

The implementation remains:

```text
F candidate = FAIL
F global gate = BLOCKED
O implementation = ABSENT
```

Only F-R01..F-R05 are authorized for correction.


---

## 9. Final manual residual after green F-R01..F-R05 re-break

Corrected HEAD:

`9f905fa59556dc132dc190f4abd4766809504af4`

Green execution:

```text
candidate run = 35455420818
frozen F breaker = 36 passed

adversarial run = 35455420790
frozen F breaker       = 36 passed
supplemental adversary = 30 passed
```

A final source→logical reconstruction attack demonstrates one further defect.

### F-R06 — SOURCE_TIMESTAMP_OUTSIDE_DECLARED_HOUR_ACCEPTED

F persists both:

```text
component.declared_hour_bucket_utc
+
retained occurrence source witness
+
logical market_timestamp_utc
```

For the current B contract, the retained logical timestamp is reconstructed from:

```text
declared UTC hour + millisecond offset in [0, 3_600_000)
```

Therefore a retained source slot cannot legitimately map to a logical timestamp outside its component's declared hour.

The current runtime validates:

- component hour syntax;
- occurrence timestamp syntax;
- source witness component/slot;
- B-candidate/Q-retained equality;

but does not connect the timestamp back to the declared hour.

Attack:

change the same retained occurrence in both B-candidate and Q-retained relations from:

```text
2026-01-02T10:00:02.000Z
```

to:

```text
2026-01-02T11:00:02.000Z
```

while keeping its source witness bound to the component declared as:

```text
2026-01-02T10:00:00Z
```

The two upstream relations still agree with each other, but the frozen physical→logical relation violates B.

Verdict:

```text
F-R06 = FAIL
```

Required correction:

for every B-candidate/retained occurrence, prove:

```text
declared_hour_bucket_utc
<= market_timestamp_utc
< declared_hour_bucket_utc + 1 hour
```

without sorting or creating temporal precedence.

This is a local conformance check only.

Exactly authorized next action:

```text
encode F-R06 in supplemental breaker
→ demonstrate RED
→ correct F-R06 only
→ final persisted-head re-break
```

O remains absent and no real data is authorized.
