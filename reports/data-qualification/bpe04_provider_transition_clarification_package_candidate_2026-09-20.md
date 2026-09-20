# B-PE-04 — PROVIDER-AUTHORITATIVE HOURLY→DAILY TRANSITION CLARIFICATION PACKAGE — CORRECTED CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Initial candidate commit:** `f5316e3fbffc66343dbaea1f13a2b7c445bbd060`  
**Initial candidate blob:** `9491cc90fa256b540dce44a615c924c1a2a2207b`  
**Adversarial break commit:** `b0dee3943d06a039db43f1d93997877f9a8e551b`  
**Status:** CORRECTED PERSISTED CANDIDATE — NOT YET QUALIFIED  
**Scope:** request/admissibility/capture protocol only. No provider contact, BI5 download, acquisition, backtest or trading execution.

---

## 0. Purpose

B-PE-03 qualified:

```text
C08-D1 provider identity applicability            = PASS
C08-D2 legacy hourly BI5 family existence         = PASS
C08-D3 historical tick file-object family binding = PASS
```

and left:

```text
C08-D4 USATECH legacy-hourly applicability = BLOCKED
C08-D5 target temporal/version continuity  = BLOCKED
```

B-PE-04 defines one provider-facing clarification package that can later obtain a Dukascopy-authored answer without conflating:

```text
market-data timestamp
≠ retrieval/deployment date

object path/bucket granularity
≠ physical payload semantics

tick BI5
≠ candle BI5
```

B-PE-04 itself does not send the request.

---

## 1. Package identity

```text
clarification_package_id =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION

clarification_package_version =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION_V0_2_CORRECTED
```

Target:

```text
provider = Dukascopy
instrument = USATECHIDXUSD / USATECH.IDX/USD
market-data timestamp interval = 2021-08-14T00:00:00Z through 2026-08-14T23:59:59.999Z
legacy tick path family = .../<instrument>/<YYYY>/<MM>/<DD>/<HH>h_ticks.bi5
current provider documentation locator =
https://www.dukascopy.com/wiki/en/development/data-export/
out-of-scope candle example = *_candles_day_1.bi5
```

The clarification concerns **public historical tick objects**, not OHLC/candle files.

---

## 2. Provider-facing canonical request

### Subject

```text
Technical clarification: Dukascopy public historical tick BI5 hourly/daily representation
```

### Message

```text
Hello Dukascopy Support,

I am documenting the public Dukascopy historical tick-data representation
served through datafeed.dukascopy.com.

I need an authoritative clarification for historical TICK data only.
This request does NOT concern candle/OHLC BI5 files such as
*_candles_day_1.bi5.

Instrument:
USATECH.IDX/USD
datafeed symbol: USATECHIDXUSD

Target market-data timestamp interval:
2021-08-14T00:00:00Z through 2026-08-14T23:59:59.999Z.

Legacy public tick object family:
.../<instrument>/<YYYY>/<MM>/<DD>/<HH>h_ticks.bi5

By "daily tick representation" below, I mean the daily historical TICK
representation described by Dukascopy's current Historical Price Data /
data-export documentation, not daily candles.

Please answer Q1-Q4 separately.

Q1 — Public tick-object addressing / bucket boundary

For records whose MARKET-DATA timestamps fall in the target interval,
was the authoritative public historical tick object family hour-addressed
(<HH>h_ticks.bi5), day-addressed, or did both forms coexist / depend on
instrument, endpoint, or period?

Please do not assume that a single transition occurred.

Please answer one of:
- HOURLY ONLY
- DAILY ONLY
- TRANSITIONED
- COEXISTED
- DEPENDED
- CANNOT CONFIRM

If TRANSITIONED / COEXISTED / DEPENDED, please provide:
a) exact old object/path form;
b) exact new object/path form;
c) boundary timezone;
d) last MARKET-DATA timestamp/date governed by the old form;
e) first MARKET-DATA timestamp/date governed by the new form;
f) whether that boundary is a market-data-date boundary or merely a
   server deployment/retrieval date.

Q2 — Current retrieval versus historical market-date representation

If I request today historical tick records whose MARKET-DATA timestamps
fall between 2021-08-14 and 2026-08-14, are those records still retrieved
through the same object/bucket form that applied to those market dates,
or has Dukascopy retroactively rebucketed/repackaged older history?

Please identify any current-retrieval rule separately from the historical
market-date rule.

Q3 — USATECH.IDX/USD applicability

For USATECH.IDX/USD / USATECHIDXUSD specifically, which public historical
TICK object/path form applied to records in the target market-data interval?

Please answer:
- same rule as the generic tick history;
- different rule;
- period dependent;
- cannot confirm.

If different or period dependent, please provide exact UTC date/timestamp
ranges and object/path forms.

Q4 — Physical payload/record semantics, separately from bucket/path changes

Independently of Q1-Q3, did any change in hourly/day object addressing also
change the physical tick payload semantics?

If known, please identify separate effective boundaries for:
- compression/envelope;
- decompressed record width/framing;
- field order and primitive types/signedness;
- timestamp offset unit/reference point;
- USATECHIDXUSD raw price scale/divisor;
- volume primitive representation or representation-level scaling.

If the physical record semantics did NOT change when object bucketization
changed, please state that explicitly.

If any point is not documented or cannot be confirmed, please state
"CANNOT CONFIRM" rather than infer.

For reproducibility, please include the documentation name/version,
release/build number, archive reference, technical-team confirmation,
or other provider basis for the answer where available.

Thank you.
```

---

## 3. Non-leading response domain

The provider is explicitly free to establish any of:

```text
no transition
hourly only
daily only
one transition
multiple transitions
coexistence
instrument-specific behavior
endpoint-specific behavior
retroactive rebucketing
unchanged physical semantics despite bucket change
physical semantics changed independently of bucket change
cannot confirm
```

No provider answer is rewritten to fit the project's current hypothesis.

---

## 4. Exact evidence targets

### C08-D4 — USATECH target applicability

An answer can contribute to C08-D4 only if it binds:

```text
USATECH.IDX/USD or USATECHIDXUSD
+
public historical TICK data
+
exact object/path representation
+
market-data timestamp/date range intersecting target interval
```

Generic index support is insufficient.

### C08-D5 — temporal/version continuity

An answer can contribute to C08-D5 only if it binds:

```text
public historical TICK object/path state
+
market-data timestamp/date range or exact boundary
+
timezone/boundary semantics
+
distinction from retrieval/deployment date
+
target interval applicability
```

A software release date alone is insufficient.

### C01-C07 — optional physical semantics

Q4 answers are separately mapped.

An object/bucket transition date does not automatically become a physical-format transition date.

---

## 5. Channel-specific provider authenticity

A future provider answer is not ADMISSIBLE until its channel-specific authenticity requirements are met.

### 5.1 Authenticated Dukascopy support ticket

Required:

```text
stable ticket/thread ID
authenticated portal/account context
full thread export or equivalent provider-rendered record
provider author/support identity
exact timestamps
exact request + response content
```

A copied ticket paragraph without ticket provenance is BLOCKED.

### 5.2 Provider email

Required:

```text
raw .eml or equivalent original-message export
complete headers
From/To/Date/Message-ID
Received chain where available
DKIM/SPF/DMARC Authentication-Results where available
exact body bytes
attachments
```

A copied email body or screenshot of an email alone is BLOCKED.

### 5.3 Dukascopy official support/forum post

Required:

```text
exact post URL/thread ID
provider author/account identity
provider-role evidence
post timestamp
full relevant thread context
persisted page/export snapshot
```

### 5.4 Versioned/archived provider documentation

Required:

```text
exact provider locator
document/version/release/archive identity
exact relevant bytes/snapshot
exact anchors
publication/effective date where available
```

If channel authenticity cannot be sealed, response admissibility = BLOCKED.

---

## 6. Response capture package

A future capture must persist:

```text
request/
  canonical_request.txt
  sent_request_exact.bin

response/
  provider_response_original.*
  provider_thread_export.*
  provider_attachments/*

metadata/
  channel_authenticity_evidence/*
  capture_record.json
  answer_records.json
```

No screenshot substitutes for raw/original export where that export exists.

---

## 7. CaptureRecord — closed schema

```text
schema =
B_PE_04_PROVIDER_CLARIFICATION_CAPTURE_V0_2

capture_id
clarification_package_id
clarification_package_version
channel_type
provider_channel_locator
ticket_or_message_id
request_sent_at_utc
response_received_at_utc
provider_sender_identity
provider_sender_domain_or_account
provider_authenticity_artifact_ids
request_exact_sha256
response_original_sha256
thread_context_sha256
attachment_records
capture_operator
capture_created_at_utc
capture_seal
```

Attachment record:

```text
artifact_id
filename
media_type
byte_length
sha256
provider_locator_or_attachment_id
```

Integrity:

```text
raw artifact = SHA256(exact bytes)
capture_seal =
SHA256(B-PE-01 canonical_json(capture_record_without_capture_seal))
```

---

## 8. ProviderClarificationAnswerRecord — closed atomic schema

Exactly one answer record exists per question/sub-question that is evaluated.

```text
schema =
B_PE_04_PROVIDER_CLARIFICATION_ANSWER_V0_2

answer_record_id
capture_id
question_id
subquestion_id
answer_status =
  ANSWERED |
  NO_ANSWER |
  AMBIGUOUS |
  CONTRADICTORY_INTERNAL |
  CANNOT_CONFIRM

provider_exact_anchor_artifact_id
provider_exact_anchor_locator
provider_exact_text_sha256
normalized_proposition
market_data_time_scope
retrieval_time_scope
instrument_scope
object_path_scope
physical_semantics_scope
candidate_dimension_ids
adjudicator_identity
created_at_utc
answer_record_seal
```

Rules:

- `normalized_proposition` cannot contain a fact absent from the exact provider anchor;
- thread-level authority never implies that every question was answered;
- each dimension assertion must cite one or more exact `answer_record_id`;
- NO_ANSWER / AMBIGUOUS / CANNOT_CONFIRM carry zero positive evidentiary weight;
- CONTRADICTORY_INTERNAL forces BLOCKED until resolved.

Seal:

```text
answer_record_seal =
SHA256(B-PE-01 canonical_json(answer_record_without_answer_record_seal))
```

---

## 9. Provider response admissibility decision

A captured response package is eligible for EC-P1 review only when all hold:

1. channel-specific authenticity requirements pass;
2. exact sent request is preserved;
3. exact original response is preserved;
4. full relevant thread context is preserved;
5. exact timestamps/IDs are preserved;
6. attachments/basis documents are preserved or immutably pinned;
7. source bytes and structured records rehash correctly;
8. each used proposition has a closed atomic AnswerRecord;
9. scope can be mapped without inference beyond provider text.

Disposition:

```text
ADMISSIBLE
REJECTED
BLOCKED
```

No weaker "probably provider-authored" state can contribute positive weight.

---

## 10. Partial-answer semantics

Examples:

```text
Q1 precise, Q2 omitted, Q3 precise
→ Q1/Q3 AnswerRecords may be used; Q2 = NO_ANSWER

"hourly files were used until 2025"
without market-data-vs-retrieval distinction
→ AMBIGUOUS

"change was 2025-01-01"
without old-last/new-first/timezone
→ AMBIGUOUS for exact boundary

"USATECH is supported"
without historical tick/path/date scope
→ insufficient for C08-D4

"we cannot confirm historical file format"
→ CANNOT_CONFIRM, not negative evidence
```

Silence is not confirmation.

---

## 11. Conflict and supersession

A future provider clarification never mutates B-PE-02/B-PE-03 evidence.

If it conflicts:

```text
persist new provider response
→ exact AnswerRecords
→ exact SUPPORT/CONTRADICT ClaimEvidenceAssertions
→ B-PE-01 conflict semantics
→ PASS / FAIL / BLOCKED dimension adjudication
```

Provider authority does not bypass exact scope/version matching.

---

## 12. External-state boundary

B-PE-04 qualification does **not** authorize contacting Dukascopy.

Sending the request is a separate external-state action.

Until separately authorized:

```text
no ticket opened
no email sent
no forum post
no provider contact
```

---

## 13. Correction record

Adversarial break demonstrated:

```text
BPE04-F01 — DATA_TIMESTAMP_VS_RETRIEVAL_TIME_CONFLATION
BPE04-F02 — OBJECT_BUCKETING_AND_PHYSICAL_LAYOUT_AXES_CONFLATED
BPE04-F03 — DAILY_TICK_OBJECT_NOT_EXACTLY_IDENTIFIED
BPE04-F04 — TRANSITION_BOUNDARY_PRECISION_UNDERSPECIFIED
BPE04-F05 — CHANNEL_AUTHENTICITY_RULES_NOT_FAIL_CLOSED_ENOUGH
BPE04-F06 — NO_ATOMIC_ANSWER_TO_DIMENSION_RESPONSE_SCHEMA
```

Corrections are limited to those six defects.

---

## 14. Corrected candidate verdict

```text
B-PE-04 CLARIFICATION PACKAGE =
CORRECTED PERSISTED CANDIDATE / NOT YET QUALIFIED

C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
```

Next:

```text
persisted-HEAD adversarial re-break of this corrected package
```
