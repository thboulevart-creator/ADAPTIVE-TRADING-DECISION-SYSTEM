# B-PE-04 — CORRECTED CLARIFICATION PACKAGE — PERSISTED-HEAD ADVERSARIAL RE-BREAK

**Date:** 2026-09-20  
**Corrected candidate HEAD:** `d9d76fdeb49cfa449bb013b8eb8a79094a6e893e`  
**Corrected candidate blob:** `609a8c49875869a30cfdc4b7ef68478de76564b6`

## 1. Closure of initial defects

The corrected candidate closes:

```text
BPE04-F01 — DATA_TIMESTAMP_VS_RETRIEVAL_TIME_CONFLATION
BPE04-F02 — OBJECT_BUCKETING_AND_PHYSICAL_LAYOUT_AXES_CONFLATED
BPE04-F03 — DAILY_TICK_OBJECT_NOT_EXACTLY_IDENTIFIED
BPE04-F04 — TRANSITION_BOUNDARY_PRECISION_UNDERSPECIFIED
BPE04-F05 — CHANNEL_AUTHENTICITY_RULES_NOT_FAIL_CLOSED_ENOUGH
BPE04-F06 — NO_ATOMIC_ANSWER_TO_DIMENSION_RESPONSE_SCHEMA
```

No regression of those six defects was demonstrated.

## 2. Residual defects

### BPE04-R01 — OPTIONAL_Q4_BREAKS_MINIMALITY

The governed B-PE-04 objective is to ask exactly for:

```text
hourly→daily transition
target-interval continuity
USATECH applicability
```

The corrected request still includes a broad Q4 asking for compression, framing, signedness, timestamp rules, price scaling and volume semantics.

Even though Q4 is technically separable, it:

- exceeds the minimum clarification scope;
- creates avoidable support burden;
- can cause escalation/refusal/no-answer on the three decisive C08 questions;
- mixes the next narrow blocker with C01-C07 research.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Correction:

Remove Q4 entirely from the canonical provider request. Preserve a note that unsolicited provider physical-format details may be captured later, but do not solicit them in B-PE-04.

---

### BPE04-R02 — RELATIVE_TODAY_RETRIEVAL_TIME_IS_AMBIGUOUS

Q2 asks:

`If I request today...`

A support response may arrive days/weeks later and interpret "today" relative to response time rather than request time.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Correction:

Use an explicit request-time placeholder:

```text
REQUEST_SENT_AT_UTC = <filled at send time>
```

and ask about retrieval as of that exact timestamp/date.

The exact sent request must materialize the placeholder before transmission.

---

### BPE04-R03 — ANSWER_RECORD_NOT_BOUND_TO_EXACT_QUESTION_TEXT

`ProviderClarificationAnswerRecord` contains `question_id` and `subquestion_id`, but not the hash of the exact canonical/sent question text.

Attack:

After package revision, an answer can be accidentally mapped to a reused question ID whose wording changed.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Correction:

Add:

```text
question_text_sha256
sent_request_sha256
```

to every AnswerRecord.

An answer record is invalid unless both hashes bind the exact question wording and exact sent request that generated the provider answer.

---

## 3. Re-break verdict

```text
B-PE-04 CORRECTED CLARIFICATION PACKAGE = FAIL
```

Only BPE04-R01 through R03 are authorized for correction.

No provider contact occurred.
