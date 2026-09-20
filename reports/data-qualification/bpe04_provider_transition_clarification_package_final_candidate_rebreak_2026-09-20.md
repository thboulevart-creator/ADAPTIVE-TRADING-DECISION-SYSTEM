# B-PE-04 — FINAL-CORRECTED PACKAGE — PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Candidate HEAD:** `0ffecd0af63152547280214595b292735300e1a6`  
**Canonical request blob:** `c5789a6022aad951dec5ff665945f9c69ee08a90`  
**Canonical request SHA-256:** `8931b8304ce0e2d0c6fd7502fe50a772b5b1f4e936b12eba8989e64ecf27a52a`  
**Candidate document blob:** `65427ed98cd1c666bd3992591fa2ea8ec546330c`

## 1. Content re-break

Persisted canonical request checks:

```text
request SHA-256 matches package          = PASS
send-time placeholder count = 1         = PASS
Q1 count = 1                            = PASS
Q2 count = 1                            = PASS
Q3 count = 1                            = PASS
Q4 count = 0                            = PASS
relative "today" wording absent          = PASS
tick-vs-candle exclusion explicit        = PASS
USATECHIDXUSD target explicit             = PASS
request timestamp referenced by Q2       = PASS
AnswerRecord has question_text_sha256     = PASS
AnswerRecord has sent_request_sha256      = PASS
```

Initial F01-F06 and residual R01-R03 are not reproduced.

## 2. Residual defect

### BPE04-R04 — QUESTION_HASH_BYTE_BOUNDARY_UNDEFINED

The package requires:

`question_text_sha256`

but does not close the extraction rule for the exact question bytes.

Attack:

Two valid auditors take the same `sent_request_exact.bin`.

Auditor A hashes:

`Q1 heading + Q1 body`

Auditor B hashes:

`Q1 body only`

or one includes/excludes the blank line immediately before Q2.

Both can claim to have hashed "the exact question text."

Result:

AnswerRecord binding is not deterministic across independent implementations.

Verdict:

`DEMONSTRATED RESIDUAL DEFECT`.

Required correction:

Persist a versioned QuestionManifest defining for each Q1/Q2/Q3:

```text
question_id
start_marker_inclusive
end_marker_exclusive
template_question_sha256
```

At send time, after timestamp materialization:

- extract each question using those exact markers;
- require exactly one start and one end marker;
- hash the exact UTF-8 slice;
- persist the resulting sent-question SHA-256 in the AnswerRecord;
- reject if extraction is non-unique.

The final Q3 end marker must also be explicit.

## 3. Verdict

```text
B-PE-04 FINAL-CORRECTED CANDIDATE = FAIL
```

Only BPE04-R04 is authorized for correction.

No provider contact occurred.
