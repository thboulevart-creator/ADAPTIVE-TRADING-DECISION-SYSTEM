# A0 — ADVERSARIAL BREAK EXPANSION V0.4 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`c37805255e7a06ea18a17aa8e5c2660f80a31bd7`

Implementation blob:

`4b4737238d01be0b1017b07cf33742797cb995eb`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Adversarial V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

Adversarial V0.3 breaker blob:

`d23e3c72dd8bd2200cb392edc6c80b4e744d4751`

Adversarial V0.4 breaker blob:

`efcc3ca7927b29b45f5d0dc0180b81176dbed51e`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Workflow run:

`36330491802`

## Structural verification

PASS:

- exact persisted V0.4 break HEAD checked out;
- persistence scope limited to checkpoint + V0.4 breaker + V0.4 FAIL report;
- runtime unchanged;
- historical/V0.1/V0.2/V0.3 breakers unchanged;
- V0.4 breaker exact;
- A0 V0.3 contract unchanged;
- runtime and all breakers compile.

## Preserved existing suite

`64/64 PASS`

## Persisted V0.4 failure profile

Reproduced exactly:

```
TOTAL = 21
PASS  = 15
FAIL  = 6
```

PASS:

AE01, AE02, AE03, AE04, AE05, AE06, AE07, AE08, AE15, AE16, AE17, AE18, AE19, AE20, AE21.

FAIL:

AE09, AE10, AE11, AE12, AE13, AE14.

## Confirmed defect groups

- `A0-ABF4-01` preregistration exact content authority not pinned;
- `A0-ABF4-02` N0 evidence/research-class cross-dimension consistency not enforced;
- `A0-ABF4-03` synthetic data/confirmatory cross-dimension consistency not enforced;
- `A0-ABF4-04` CONFIRMED != N4 fail-closed guard incomplete.

No additional defect group is introduced by the persisted-head re-break.

## Verdict

`A0_ADVERSARIAL_V0_4_PERSISTED_REBREAK = PASS_FAILURE_PROFILE_REPRODUCED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_4`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed boundary

`A0 — MINIMAL CORRECTION CANDIDATE FOR A0-ABF4-01..04`

The correction must preserve all current 85 tests unchanged:

- historical = 6;
- V0.1 = 18;
- V0.2 = 18;
- V0.3 = 22;
- V0.4 = 21.

No test expectation or V0.3 contract text may be changed after observation.
