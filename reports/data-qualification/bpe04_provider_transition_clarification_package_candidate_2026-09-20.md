# B-PE-04 — PROVIDER-AUTHORITATIVE HOURLY→DAILY TRANSITION CLARIFICATION PACKAGE — FINAL CORRECTED CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Initial candidate commit:** `f5316e3fbffc66343dbaea1f13a2b7c445bbd060`  
**Initial adversarial break commit:** `b0dee3943d06a039db43f1d93997877f9a8e551b`  
**First corrected commit:** `d9d76fdeb49cfa449bb013b8eb8a79094a6e893e`  
**Persisted-head re-break commit:** `b388ba54af075f45921fbe43896affc06db92a82`  
**Status:** FINAL CORRECTED CANDIDATE — NOT YET QUALIFIED  
**Scope:** request/admissibility/capture protocol only. No provider contact and no data execution.

---

## 0. Package identity

```text
clarification_package_id =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION

clarification_package_version =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION_V0_3_FINAL_CANDIDATE
```

B-PE-03 remains:

```text
C08-D1 = PASS
C08-D2 = PASS
C08-D3 = PASS
C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
```

B-PE-04 seeks only the minimum provider clarification needed for D4/D5.

---

## 1. Canonical provider request artifact

Authoritative request template:

`evidence/bpe04/canonical_provider_request_template_v0_3.txt`

Raw UTF-8 SHA-256:

`8931b8304ce0e2d0c6fd7502fe50a772b5b1f4e936b12eba8989e64ecf27a52a`

The template contains exactly three questions:

```text
Q1 — historical hourly/daily/coexistence boundary
Q2 — retrieval rule as of exact request timestamp versus market-data-date rule
Q3 — USATECHIDXUSD applicability
```

No C01-C07 physical-format question is solicited in B-PE-04.

If Dukascopy volunteers additional physical-format information, it may be captured exactly but is outside B-PE-04's requested scope and cannot be adjudicated until separately governed.

---

## 2. Send-time materialization rule

The canonical template contains:

```text
REQUEST_SENT_AT_UTC = <MATERIALIZE_EXACT_UTC_TIMESTAMP_BEFORE_SEND>
```

Before any future send action:

1. copy the canonical template;
2. replace the placeholder exactly once with an RFC3339 UTC timestamp;
3. persist the exact sent-request bytes;
4. compute `sent_request_sha256 = SHA256(exact sent bytes)`;
5. verify no other text differs from the canonical template;
6. only then may an externally authorized send occur.

A request containing the unresolved placeholder is invalid and must not be sent.

"Today", "currently" or equivalent unbound relative-time wording must not replace the materialized timestamp.

---

## 3. Exact evidence targets

### C08-D4 — USATECH applicability

Positive/negative provider evidence must bind:

```text
USATECH.IDX/USD or USATECHIDXUSD
+
public historical TICK data
+
exact object/path rule
+
market-data timestamp/date scope intersecting target interval
```

### C08-D5 — temporal/version continuity

Provider evidence must distinguish:

```text
market-data timestamp/date rule
from
retrieval/deployment date rule
```

and establish:

```text
hourly/daily/coexistence/depended state
+
object/path form
+
boundary timezone
+
old-last/new-first market-data boundary when a transition exists
+
applicability to 2021-08-14 → 2026-08-14
```

A JForex/client release date alone is insufficient.

---

## 4. Non-leading answer domain

The provider may validly answer:

```text
HOURLY ONLY
DAILY ONLY
TRANSITIONED
COEXISTED
DEPENDED
DIFFERENT FOR USATECH
RETROACTIVELY REBUCKETED
NO RETROACTIVE REBUCKETING
CANNOT CONFIRM
```

A response disproving the project's current assumption is valid evidence.

No transition is presumed.

---

## 5. Channel-specific provider authenticity

A future response is not ADMISSIBLE unless its channel requirements pass.

### Authenticated Dukascopy support ticket

Required:

```text
stable ticket/thread ID
authenticated portal/account context
full relevant thread export/provider-rendered record
provider author/support identity
exact timestamps
exact sent request
exact response
```

### Provider email

Required:

```text
raw .eml or equivalent original export
complete headers
From / To / Date / Message-ID
Received chain where available
DKIM/SPF/DMARC Authentication-Results where available
body bytes
attachments
```

Copied body/screenshot alone = BLOCKED.

### Official provider forum/support post

Required:

```text
exact URL/thread/post ID
provider author/account identity
provider-role evidence
timestamp
full relevant context
persisted page/export snapshot
```

### Versioned/archived provider document

Required:

```text
exact provider locator
document/version/release/archive identity
exact persisted source bytes/snapshot
exact anchors
effective/publication date where available
```

Unverifiable provider origin = BLOCKED.

---

## 6. Capture package

Persist:

```text
request/
  canonical_request_template.bin
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

Raw artifacts:

```text
SHA256(exact bytes)
```

Structured records use B-PE-01 canonical JSON.

---

## 7. CaptureRecord — closed schema

```text
schema =
B_PE_04_PROVIDER_CLARIFICATION_CAPTURE_V0_3

capture_id
clarification_package_id
clarification_package_version
canonical_request_template_sha256
sent_request_sha256
channel_type
provider_channel_locator
ticket_or_message_id
request_sent_at_utc
response_received_at_utc
provider_sender_identity
provider_sender_domain_or_account
provider_authenticity_artifact_ids
response_original_sha256
thread_context_sha256
attachment_records
capture_operator
capture_created_at_utc
capture_seal
```

Rules:

- `canonical_request_template_sha256` must equal `8931b8304ce0e2d0c6fd7502fe50a772b5b1f4e936b12eba8989e64ecf27a52a`;
- `request_sent_at_utc` must exactly equal the materialized timestamp in the sent request;
- `sent_request_sha256` binds the exact transmitted bytes.

Seal:

```text
capture_seal =
SHA256(B-PE-01 canonical_json(capture_record_without_capture_seal))
```

---

## 8. ProviderClarificationAnswerRecord — closed atomic schema

Exactly one record per evaluated question/sub-question:

```text
schema =
B_PE_04_PROVIDER_CLARIFICATION_ANSWER_V0_3

answer_record_id
capture_id
question_id
subquestion_id
question_text_sha256
sent_request_sha256
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
candidate_dimension_ids
adjudicator_identity
created_at_utc
answer_record_seal
```

Mandatory rules:

- `question_text_sha256` hashes the exact materialized question/sub-question text from `sent_request_exact.bin`;
- `sent_request_sha256` must equal the parent CaptureRecord;
- an AnswerRecord whose question hash does not match the sent request is invalid;
- `normalized_proposition` may contain no fact absent from the provider anchor;
- thread-level authority never implies all questions were answered;
- NO_ANSWER / AMBIGUOUS / CANNOT_CONFIRM have zero positive evidentiary weight;
- CONTRADICTORY_INTERNAL forces BLOCKED until resolved.

Seal:

```text
answer_record_seal =
SHA256(B-PE-01 canonical_json(answer_record_without_answer_record_seal))
```

---

## 9. Provider response admissibility

A future response package can become ADMISSIBLE only when all hold:

1. channel-specific authenticity passes;
2. canonical template identity matches;
3. exact materialized sent request is preserved;
4. exact original response is preserved;
5. full relevant thread context is preserved;
6. exact IDs/timestamps are preserved;
7. referenced provider attachments/basis documents are preserved or immutably pinned;
8. every used proposition has a valid atomic AnswerRecord;
9. all hashes/seals recompute;
10. scope maps without inference beyond provider wording.

Disposition:

```text
ADMISSIBLE
REJECTED
BLOCKED
```

No weaker authenticity state contributes positive evidence.

---

## 10. Partial/ambiguous answer semantics

```text
Q1 exact, Q2 missing, Q3 exact
→ Q1/Q3 may be used; Q2 = NO_ANSWER

"hourly until 2025"
without market-date vs retrieval-date distinction
→ AMBIGUOUS

"changed on 2025-01-01"
without timezone and old-last/new-first market boundary
→ AMBIGUOUS for exact transition

"USATECH supported"
without tick/path/date binding
→ insufficient for C08-D4

"CANNOT CONFIRM"
→ zero positive weight, not contradiction
```

Silence is never confirmation.

---

## 11. Unsolicited physical-format information

B-PE-04 does not solicit C01-C07.

If Dukascopy volunteers such information:

```text
capture exact bytes
preserve authenticity
do not adjudicate C01-C07 in B-PE-04
open a later explicitly governed evidence action if needed
```

This keeps the provider request minimal without discarding potentially useful provider evidence.

---

## 12. Conflict handling

Future response evidence never mutates B-PE-02/B-PE-03.

If a valid provider clarification conflicts:

```text
persist exact answer
→ exact AnswerRecords
→ exact ClaimEvidenceAssertions
→ apply B-PE-01 conflict semantics
→ PASS / FAIL / BLOCKED
```

---

## 13. External-state boundary

B-PE-04 qualification does not send anything.

Until a separate governed external-state action:

```text
no ticket
no email
no forum post
no provider contact
```

---

## 14. Correction record

Initial defects closed:

```text
BPE04-F01 — DATA_TIMESTAMP_VS_RETRIEVAL_TIME_CONFLATION
BPE04-F02 — OBJECT_BUCKETING_AND_PHYSICAL_LAYOUT_AXES_CONFLATED
BPE04-F03 — DAILY_TICK_OBJECT_NOT_EXACTLY_IDENTIFIED
BPE04-F04 — TRANSITION_BOUNDARY_PRECISION_UNDERSPECIFIED
BPE04-F05 — CHANNEL_AUTHENTICITY_RULES_NOT_FAIL_CLOSED_ENOUGH
BPE04-F06 — NO_ATOMIC_ANSWER_TO_DIMENSION_RESPONSE_SCHEMA
```

Residual defects closed:

```text
BPE04-R01 — OPTIONAL_Q4_BREAKS_MINIMALITY
BPE04-R02 — RELATIVE_TODAY_RETRIEVAL_TIME_IS_AMBIGUOUS
BPE04-R03 — ANSWER_RECORD_NOT_BOUND_TO_EXACT_QUESTION_TEXT
```

---

## 15. Final corrected pre-rebreak verdict

```text
B-PE-04 CLARIFICATION PACKAGE =
FINAL CORRECTED CANDIDATE / NOT YET QUALIFIED

C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
```

Next:

`persisted-HEAD final adversarial re-break`.
