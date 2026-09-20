# B-PE-04 — PROVIDER CLARIFICATION PACKAGE — ADVERSARIAL BREAK

**Date:** 2026-09-20  
**Candidate commit:** `f5316e3fbffc66343dbaea1f13a2b7c445bbd060`  
**Candidate blob:** `9491cc90fa256b540dce44a615c924c1a2a2207b`  
**Scope:** package attack only. No provider contact occurred.

## 1. Attack objective

Attempt to obtain a provider-authored response that appears to answer Q1-Q3 while still being unusable for C08-D4/D5.

---

## 2. Demonstrated defects

### BPE04-F01 — DATA_TIMESTAMP_VS_RETRIEVAL_TIME_CONFLATION

Attack:

Dukascopy replies:

```text
Hourly files were used through 2025.
```

This can mean either:

1. historical records whose market timestamps fall in 2021-2025 were represented hourly; or
2. the server happened to expose hourly objects when queried during calendar year 2025.

Those are not equivalent if the provider later rebuckets historical data retroactively.

The candidate request asks about the "target interval" but does not force the provider to distinguish:

```text
market-data timestamp/date
vs
date on which the client downloads/requests that historical data.
```

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Explicitly state that the project needs the representation used to retrieve records **whose market timestamps fall in the target interval**, and separately ask whether current retrieval of those same historical dates has been rebucketed.

---

### BPE04-F02 — OBJECT_BUCKETING_AND_PHYSICAL_LAYOUT_AXES_CONFLATED

Attack:

Dukascopy replies:

```text
We moved from hourly to daily files in 2025, but the decompressed tick record format did not change.
```

or the inverse:

```text
Hourly paths remained, but record semantics changed earlier.
```

The candidate uses "representation" broadly enough that a response can collapse:

- path/bucket granularity;
- compression/envelope;
- physical record layout/time-base.

C08-D5 needs scope continuity, while C01-C07 concern physical semantics. These axes must not silently inherit the same transition date.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Ask the provider to answer **object-addressing/bucket transition** separately from **physical payload/record semantic transition**.

---

### BPE04-F03 — DAILY_TICK_OBJECT_NOT_EXACTLY_IDENTIFIED

Attack:

Provider interprets "daily BI5 objects" as daily candle BI5.

The message says tick-only, but it gives an exact legacy path and no exact daily tick object/path/documentation identifier.

A support answer can therefore refer to the wrong daily BI5 family while technically answering the wording.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Bind "daily" to the exact Dukascopy current historical **tick** representation/documentation/source locator, and state that `*_candles_day_1.bi5` is explicitly out of scope.

---

### BPE04-F04 — TRANSITION_BOUNDARY_PRECISION_UNDERSPECIFIED

Attack:

Provider says:

```text
The change happened on 2025-01-01.
```

The answer still leaves unresolved:

- UTC versus provider local time;
- whether 2025-01-01 is first daily date or last hourly date;
- whether transition is by market date, object availability date, or software release date.

This can shift an entire boundary day/hour.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Ask for:

```text
boundary timezone
last market timestamp/date using old representation
first market timestamp/date using new representation
whether boundary is data-date or retrieval/deployment-date
```

---

### BPE04-F05 — CHANNEL_AUTHENTICITY_RULES_NOT FAIL-CLOSED ENOUGH

Attack:

A copied email body from `support@dukascopy.com` is persisted without full headers.

The candidate allows verifiable `@dukascopy.com` email but does not make full message headers / DKIM-SPF or provider portal provenance mandatory when email is the channel.

Likewise a copied support-ticket answer without ticket export/authenticated metadata may look provider-authored without durable proof.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define channel-specific mandatory authenticity evidence:

- official ticket: stable ticket ID + authenticated export/page metadata;
- email: raw `.eml` or equivalent full headers, including authentication results where available;
- official forum: post URL + author/provider-role evidence + persisted page snapshot;
- provider document: exact provider locator/version/archive snapshot.

If channel authentication cannot be sealed:

`response admissibility = BLOCKED`.

---

### BPE04-F06 — NO ATOMIC ANSWER-TO-DIMENSION RESPONSE SCHEMA

Attack:

Provider replies in prose containing:

- a clear Q1;
- an ambiguous Q2;
- no Q3;
- optional Q4 details.

The package describes partial answers but defines no closed future `ProviderClarificationAnswerRecord` binding each answer unit to question ID, exact provider quote/anchor, target dimension and disposition.

Result:

future adjudication can accidentally treat thread-level authority as if every question were answered.

Verdict:

`DEMONSTRATED DEFECT`.

Required correction:

Define one closed answer record per question/sub-question with:

```text
question_id
answer_status
exact_anchor
normalized_proposition
scope
candidate_dimension_ids
NO_ANSWER / ANSWERED / AMBIGUOUS / CONTRADICTORY
```

No thread-level PASS projection is permitted.

---

## 3. Attacks that did not demonstrate defects

The candidate already resists:

- assuming a transition necessarily occurred;
- forcing YES instead of NO/COEXISTED/DEPENDED;
- treating silence as confirmation;
- using third-party/project material as provider-primary;
- turning an optional Q4 answer directly into C01-C07 PASS;
- silently rewriting a provider answer that disproves the project hypothesis;
- sending the request inside B-PE-04.

---

## 4. Verdict

```text
B-PE-04 CLARIFICATION PACKAGE CANDIDATE = FAIL
```

Six package defects are demonstrated.

## 5. Authorized correction scope

Correct only:

```text
BPE04-F01
BPE04-F02
BPE04-F03
BPE04-F04
BPE04-F05
BPE04-F06
```

Do not contact Dukascopy and do not change any B/runtime/data surface.
