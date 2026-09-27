# A0 — ADVERSARIAL BREAK EXPANSION V0.3 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`64d4c8d4dac39264045e8dca1326fdac79da6025`

Implementation blob:

`f0015894d001c0ced7d0edf881947e3a435ab5ca`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Adversarial V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

Adversarial V0.3 breaker blob:

`d23e3c72dd8bd2200cb392edc6c80b4e744d4751`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Workflow run:

`36328583961`

## Structural verification

PASS:

- exact persisted V0.3 break HEAD checked out;
- persistence scope limited to checkpoint + V0.3 breaker + V0.3 FAIL report;
- runtime unchanged;
- historical/V0.1/V0.2 breakers unchanged;
- V0.3 breaker exact;
- A0 V0.3 contract unchanged;
- runtime and all breakers compile.

## Preserved existing suite

`42/42 PASS`

## Persisted V0.3 failure profile

Reproduced exactly:

```
TOTAL = 22
PASS  = 12
FAIL  = 10
```

PASS:

AD01, AD02, AD03, AD11, AD12, AD14, AD17, AD18, AD19, AD20, AD21, AD22.

FAIL:

AD04, AD05, AD06, AD07, AD08, AD09, AD10, AD13, AD15, AD16.

## Confirmed defect groups

- `A0-ABF3-01` exact persistent authority bytes not pinned;
- `A0-ABF3-02` registry supersession metadata authority not pinned;
- `A0-ABF3-03` profile-declared native-status completeness/preservation incomplete;
- `A0-ABF3-04` measurement scope binding not preserved;
- `A0-ABF3-05` opaque narrative identity/reference not preserved;
- `A0-ABF3-06` Global Normalization Policy permission-table content not exactly pinned.

No additional defect group is introduced by the persisted-head re-break.

## Verdict

`A0_ADVERSARIAL_V0_3_PERSISTED_REBREAK = PASS_FAILURE_PROFILE_REPRODUCED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_3`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed boundary

`A0 — MINIMAL CORRECTION CANDIDATE FOR A0-ABF3-01..06`

The correction must preserve all current 64 tests unchanged:

- historical = 6;
- V0.1 = 18;
- V0.2 = 18;
- V0.3 = 22.

No test expectation or V0.3 contract text may be changed after observation.
