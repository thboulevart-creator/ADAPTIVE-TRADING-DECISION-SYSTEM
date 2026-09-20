# SESSION BACKUP — 2026-09-20 — B-ERD-01 CONTRACT PASS

## Recovery

Repository:

thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM

Branch:

integration/system-v1

Starting HEAD:

4e969db19f852e00dc219b084163fbf4b5397c87

## B-ERD-01 candidate

Commit:

a2452d9dbe43952d1837f85ffa74864201ca2152

Blob:

c9d8c0ab270050f373607fb9f6800335582dd29a

## Initial adversarial break

Commit:

52aa2b7b90484597d745c3e148a66f321dd6bc0b

Defects:

~~~text
BERD01-F01 comparison window
BERD01-F02 absence/refutation
BERD01-F03 HTTP/retry
BERD01-F04 overall verdict
BERD01-F05 unknown trigger
BERD01-F06 seal canonicalization
BERD01-F07 warmup coverage
~~~

## First correction

Commit:

9f5c5981ca7ef60031c7b15bfc9a432fabbd2cd1

Blob:

ce67994d1ba325bff632beb77b29024caa9d4512

## Residual re-break

Commit:

0855f46a0978877af9e52b1bfa77c8c65895df3a

Residuals:

~~~text
BERD01-R01 target proposition not project premise
BERD01-R02 HTTP body hash/request policy not deterministic
~~~

## Final correction

Commit:

21248f59e2f9f4f169619e86cf080fc84f7effc5

Blob:

ac83ff40c080913de29ba74c3b7423a8f858c2fd

Final contract uses:

~~~text
T_HOURLY
PW + P0-P7 exact H1 comparison windows
TransportPolicy V0.2
GET
zero automatic retry
Accept-Encoding identity
no automatic content decoding
positive-evidence unknown representation
no sample extrapolation
full-D warmup coverage requirement
~~~

## Verdict

~~~text
B-ERD-01 = PASS
~~~

No provider contact, BI5 download, processing, acquisition or backtest occurred.

## Next possible action

~~~text
B-ERD-02 — bounded empirical representation-discrimination execution
~~~

Explicit authorization required because it downloads real provider bytes.
