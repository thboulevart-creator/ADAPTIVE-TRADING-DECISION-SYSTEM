# B-PE-04 — PROVIDER-AUTHORITATIVE TRANSITION CLARIFICATION PACKAGE — FINAL PERSISTED-HEAD RE-BREAK

**Date:** 2026-09-20  
**Repository:** `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`  
**Branch:** `integration/system-v1`  
**Final candidate HEAD:** `50d8d16fd05bb1270293071ae44143e4541e9c3d`

## 1. Qualified artifacts

Canonical provider request:

`evidence/bpe04/canonical_provider_request_template_v0_3.txt`

Git blob:

`c5789a6022aad951dec5ff665945f9c69ee08a90`

Raw UTF-8 SHA-256:

`8931b8304ce0e2d0c6fd7502fe50a772b5b1f4e936b12eba8989e64ecf27a52a`

Question manifest:

`evidence/bpe04/question_manifest_v0_4.json`

Git blob:

`46666cd9f110f24189dfe3a541287d5a12356f8c`

Question-manifest seal:

`269fd3d2c062e110fec54c04b3c0ca174d2e14585887641c367cbad2d0e9c5ea`

Final package document:

`reports/data-qualification/bpe04_provider_transition_clarification_package_candidate_2026-09-20.md`

Git blob:

`6309a2e3053dd3d7fc76e4e71e724dd7f7af33d1`

## 2. Adversarial defects closed

Initial break:

```text
BPE04-F01 — DATA_TIMESTAMP_VS_RETRIEVAL_TIME_CONFLATION
BPE04-F02 — OBJECT_BUCKETING_AND_PHYSICAL_LAYOUT_AXES_CONFLATED
BPE04-F03 — DAILY_TICK_OBJECT_NOT_EXACTLY_IDENTIFIED
BPE04-F04 — TRANSITION_BOUNDARY_PRECISION_UNDERSPECIFIED
BPE04-F05 — CHANNEL_AUTHENTICITY_RULES_NOT_FAIL_CLOSED_ENOUGH
BPE04-F06 — NO_ATOMIC_ANSWER_TO_DIMENSION_RESPONSE_SCHEMA
```

First persisted-head residuals:

```text
BPE04-R01 — OPTIONAL_Q4_BREAKS_MINIMALITY
BPE04-R02 — RELATIVE_TODAY_RETRIEVAL_TIME_IS_AMBIGUOUS
BPE04-R03 — ANSWER_RECORD_NOT_BOUND_TO_EXACT_QUESTION_TEXT
```

Final residual:

```text
BPE04-R04 — QUESTION_HASH_BYTE_BOUNDARY_UNDEFINED
```

All are closed.

## 3. Final persisted-head verification

Canonical request:

```text
Q1 count = 1
Q2 count = 1
Q3 count = 1
Q4 count = 0
send-time placeholder count = 1
relative "today" wording = absent
tick-vs-candle exclusion = explicit
USATECHIDXUSD target = explicit
external-state boundary = closed
```

Question-manifest validation:

```text
manifest seal = exact
Q1 start marker count = 1
Q1 end marker count = 1
Q1 hash = exact

Q2 start marker count = 1
Q2 end marker count = 1
Q2 hash = exact

Q3 start marker count = 1
Q3 end marker count = 1
Q3 hash = exact
```

Question hashes:

```text
Q1 eb20a2fc2addfae78710da4178bc80cca35497684b9c0c14b471435addcc4705
Q2 0c8e23e9bab1abe128cee564847afa901a212cf722c9a64febe7ef590a904787
Q3 814534404fa8d46579f3de4f506d87eff4b4896ea5bf5c7542952b6a3154b259
```

No new package defect was demonstrated.

## 4. Qualified semantics

B-PE-04 now provides a minimal non-leading provider request that asks only:

```text
Q1 exact historical hourly/daily/coexistence boundary
Q2 current retrieval rule versus historical market-date rule
Q3 USATECHIDXUSD applicability
```

It explicitly distinguishes:

```text
market-data timestamp
vs retrieval/deployment date

tick object bucket/path
vs candle files

generic tick history
vs USATECH-specific applicability
```

It also defines:

- channel-specific provider authenticity;
- exact capture package;
- send-time timestamp materialization;
- closed CaptureRecord;
- closed atomic AnswerRecord;
- deterministic question extraction/hashing;
- partial/ambiguous answer behavior;
- conflict/supersession rules.

## 5. Verdict

```text
B-PE-04 PROVIDER-AUTHORITATIVE
HOURLY→DAILY TRANSITION CLARIFICATION PACKAGE = PASS
```

This PASS applies only to the request/capture/admissibility package.

It does not mean:

```text
Dukascopy contacted
provider response received
C08-D4 PASS
C08-D5 PASS
BPE-C08 PASS
B global executable gate PASS
```

Current evidence state remains:

```text
C08-D4 = BLOCKED
C08-D5 = BLOCKED
BPE-C08 = BLOCKED
B global executable gate = BLOCKED
FINAL EXECUTABLE DATA GATE = BLOCKED
```

No provider contact occurred.
No BI5 project data was downloaded or processed.
No acquisition/backtest/paper/broker/live execution occurred.

## 6. Next external-state boundary

The next possible action is:

```text
B-PE-05 — governed provider clarification dispatch
```

This action must not execute without explicit user authorization because it creates external state.

If authorized, it must:

1. materialize `REQUEST_SENT_AT_UTC`;
2. persist exact sent-request bytes;
3. compute exact sent-request + question hashes;
4. send only the qualified Q1-Q3 request;
5. preserve channel/ticket/message identity;
6. stop after dispatch persistence.

No evidence adjudication occurs until a provider response is actually received.
