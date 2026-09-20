# B-PE-04 — PROVIDER-AUTHORITATIVE HOURLY→DAILY TRANSITION CLARIFICATION PACKAGE — CANDIDATE

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Starting HEAD:** `5fa2468f937454b42944a13ff2ab9da092a1ef4e`  
**Status:** PERSISTED CANDIDATE — NOT YET QUALIFIED  
**Scope:** provider clarification package only. This artifact does not contact Dukascopy, does not download BI5, and does not alter C01-C08 truth.

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

The remaining provider-primary evidence gap cannot be closed by another independent parser.

B-PE-04 therefore defines one exact provider-facing clarification request and the admissibility/capture rules for a future Dukascopy-authored response.

B-PE-04 does **not** send the request.

---

## 1. Clarification-package identity

```text
clarification_package_id =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION

clarification_package_version =
B_PE_04_DUKASCOPY_HISTORICAL_TICK_REPRESENTATION_CLARIFICATION_V0_1_CANDIDATE
```

Target project representation:

```text
provider = Dukascopy
instrument = USATECHIDXUSD / USATECH.IDX/USD
historical tick object family = public datafeed BI5
target research interval = 2021-08-14 through 2026-08-14
legacy path form = .../<YYYY>/<MM>/<DD>/<HH>h_ticks.bi5
current documented daily form = provider current historical-tick daily BI5 documentation
```

The request concerns **tick history**, not candle BI5 files.

---

## 2. Provider-facing request — English canonical text

### Subject

```text
Technical clarification: Dukascopy historical tick BI5 hourly vs daily representation
```

### Message

```text
Hello Dukascopy Support,

I am documenting the historical public Dukascopy tick-data representation available through datafeed.dukascopy.com.

I need an authoritative clarification about the historical tick BI5 object format and its applicability to USATECH.IDX/USD (datafeed symbol USATECHIDXUSD).

This request concerns tick-history BI5 objects only, not candle files.

For reference, the legacy hourly object family is of the form:

.../<instrument>/<YYYY>/<MM>/<DD>/<HH>h_ticks.bi5

Please answer the following questions separately.

Q1 — Hourly versus daily object boundary

Did Dukascopy public historical tick data change from hour-addressed
<HH>h_ticks.bi5 objects to day-addressed tick BI5 objects?

Please answer one of:
- YES — and provide the effective date and, if applicable, JForex/datafeed version;
- NO — the hourly object family remained applicable;
- COEXISTED / DEPENDED — and specify the exact periods, instruments, endpoints or conditions.

Please do not infer the answer from current documentation; I need the historical applicability boundary.

Q2 — Target interval continuity

For the public historical tick datafeed between 2021-08-14 and 2026-08-14,
what tick-object representation was authoritative during each applicable period?

Please identify the period(s) during which <HH>h_ticks.bi5 was the applicable public tick-history object family and, if it changed, the exact boundary to the later representation.

Q3 — USATECH.IDX/USD applicability

For USATECH.IDX/USD (datafeed symbol USATECHIDXUSD), did the same
<HH>h_ticks.bi5 representation apply during the relevant portion of
2021-08-14 through 2026-08-14?

Please answer YES / NO / DEPENDED and provide the applicable date range(s).

Q4 — Optional physical-format confirmation

If available, please also confirm the legacy hourly tick BI5 physical semantics:
- compression/envelope;
- decompressed record width;
- field order and primitive types/signedness;
- timestamp-offset unit and reference point;
- USATECHIDXUSD raw price scaling/divisor;
- volume-field primitive representation and any representation-level scaling.

If Q4 is not documented or cannot be confirmed, please state that explicitly.
The answers to Q1-Q3 are the minimum required clarification.

For reproducibility, please include any internal/public documentation name,
version, release number, archive reference, or technical-team confirmation
on which the answer is based, if available.

Thank you.
```

---

## 3. Non-leading semantics

The request must not coerce Dukascopy into confirming the project's current hypothesis.

Accepted semantic outcomes include:

```text
YES transition
NO transition
COEXISTED
instrument-dependent
endpoint-dependent
period-dependent
unknown / cannot confirm
```

A provider response saying the premise is wrong is admissible evidence.

The package must never rewrite such a response into the project's preferred interpretation.

---

## 4. Minimum response content required for each target dimension

### C08-D4 — USATECH legacy-hourly applicability

A future provider response can support or contradict C08-D4 only if it explicitly binds:

```text
USATECH.IDX/USD or USATECHIDXUSD
+
historical tick data
+
hourly h_ticks.bi5 or an explicitly identified replacement representation
+
an applicable date range intersecting the target interval
```

A generic statement about indices is insufficient unless Dukascopy explicitly states the generic rule applies to USATECH.

### C08-D5 — target temporal/version continuity

A future provider response can support or contradict C08-D5 only if it explicitly establishes:

```text
hourly/daily/coexistence state
+
effective date/range/boundary
+
public historical tick datafeed scope
+
applicability to the target 2021-08-14 → 2026-08-14 interval
```

A JForex client release date alone is insufficient.

---

## 5. Optional Q4 mapping

If Dukascopy answers Q4 with adequate exact scope, the response may later be considered for:

```text
compression/envelope                  → C01
record width/framing                  → C02
field layout/types/signedness         → C03
timestamp offset semantics            → C04
ask/bid raw roles                     → C05
USATECH raw price scaling             → C06
volume primitive/scale                → C07
```

B-PE-04 itself does not adjudicate any Q4 answer.

---

## 6. Provider response admissibility

A future response is eligible for `EC-P1 PROVIDER-PRIMARY` review only if all are true:

1. the response is authored or transmitted through a Dukascopy-controlled support/documentation channel;
2. provider identity is verifiable;
3. the response date/time is captured;
4. the exact question text sent is captured;
5. the exact answer text received is captured;
6. the complete relevant thread/context is captured;
7. attachments/linked provider documents used as authority are captured or immutably referenced;
8. no project-side paraphrase substitutes for the provider's actual words;
9. source bytes are persisted and SHA-256 bound before adjudication;
10. the response can be mapped to exact B-PE-01 claim/dimension assertions.

A response is `BLOCKED` if authenticity, completeness, scope or exact bytes cannot be established.

A response is `REJECTED` as provider-primary evidence if it originates from:

- community users;
- third-party repositories;
- AI-generated support summaries with no provider-authored underlying answer;
- copied text whose Dukascopy origin cannot be proven;
- project code/tests.

---

## 7. Acceptable provider channels

Preferred, in descending order of durability:

```text
A. versioned/archived Dukascopy technical documentation
B. authenticated Dukascopy support ticket with stable ticket/thread ID
C. email response from a verifiable @dukascopy.com provider address
D. Dukascopy API Support / official forum post by identifiable provider staff
```

Channel rank does not override scope.

A precise authenticated ticket answer may be more useful than an unrelated versioned manual.

---

## 8. Capture package

A future response capture must persist:

```text
request/
  canonical_request.txt
  sent_request_exact.txt

response/
  provider_response_exact.*
  provider_attachments/*

metadata/
  capture_record.json
  source_headers_or_ticket_metadata.*
  provider_identity_evidence.*
```

### capture_record.json minimum fields

```text
schema
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
request_exact_sha256
response_exact_sha256
attachment_records
thread_context_sha256
capture_operator
capture_created_at_utc
capture_seal
```

Every attachment record contains:

```text
filename
media_type
byte_length
sha256
provider_locator_or_attachment_id
```

---

## 9. Capture integrity

Raw request, response, thread export and attachments use:

```text
SHA-256(exact bytes)
lowercase 64-hex
```

Structured capture metadata uses B-PE-01 canonical JSON:

```text
UTF-8
sorted object keys
compact separators
ensure_ascii=false
allow_nan=false
duplicate keys rejected
```

`capture_seal`:

```text
SHA256(canonical_json(capture_record_without_capture_seal))
```

No screenshot-only response is sufficient when machine-readable/source bytes can be obtained.

If the provider portal exposes only rendered UI, the capture must preserve:

- full-page export/PDF or raw downloaded thread if available;
- screenshots;
- ticket ID;
- exact copied text;
- retrieval time;
- source locator;

and the admissibility decision remains BLOCKED if exact provider content cannot be made sufficiently reproducible.

---

## 10. Future response adjudication states

The package distinguishes **response capture** from **truth adjudication**.

### CAPTURED

Provider material was obtained and sealed.

### ADMISSIBLE

The captured provider response satisfies Section 6 and can enter B-PE-01 evidence adjudication.

### REJECTED

The material is positively not provider-primary or not applicable to the requested evidence role.

### BLOCKED

Authenticity/completeness/scope cannot be established.

No response content automatically becomes PASS.

B-PE-01 still requires:

```text
provider-primary exact claim support
+
distinct independent corroborating lineage
+
no unresolved contradiction
```

---

## 11. Partial and ambiguous answers

Questions are adjudicated independently.

Examples:

```text
Q1 answered, Q2/Q3 omitted
→ only Q1-derived assertions may be considered

"we still support historical data"
→ insufficient to identify object representation

"hourly files were used before"
→ insufficient without applicable period for C08-D5

"USATECH is supported"
→ insufficient without historical tick representation/date binding for C08-D4

"it changed around 2025"
→ BLOCKED unless boundary precision is enough to classify the target interval
```

Silence is not confirmation.

---

## 12. Provider conflict handling

If the response conflicts with B-PE-03 or independent B-PE-02 evidence:

```text
do not edit old evidence
→ persist new provider response
→ create exact SUPPORT/CONTRADICT assertions
→ apply B-PE-01 conflict semantics
→ BLOCKED or FAIL as warranted
```

A provider answer can disprove the current candidate.

---

## 13. Request execution boundary

This package does not authorize sending the request.

Sending requires a separately governed action because it creates external state.

B-PE-04 qualification means only:

```text
the exact request + response admissibility/capture protocol
is fit to be used later
```

It does not mean:

```text
Dukascopy was contacted
a response exists
C08-D4/D5 passed
B passed
```

---

## 14. Pre-break verdict

```text
B-PE-04 CLARIFICATION PACKAGE = PERSISTED CANDIDATE / NOT YET QUALIFIED

C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
```

Next within this block:

```text
adversarially break this exact clarification package
```
