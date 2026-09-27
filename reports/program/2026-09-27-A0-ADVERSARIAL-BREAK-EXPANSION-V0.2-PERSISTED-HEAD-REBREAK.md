# A0 — ADVERSARIAL BREAK EXPANSION V0.2 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`fc8b45efa4118ceb6ac9d50470ca985babcb3acd`

Implementation blob:

`c7c1f37d9d306e0424274b276d42ab422beac560`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Adversarial V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Workflow run:

`36327135044`

## Structural verification

PASS:

- exact persisted V0.2 break HEAD checked out;
- persistence scope limited to checkpoint + V0.2 breaker + V0.2 FAIL report;
- runtime unchanged;
- historical breaker unchanged;
- V0.1 breaker unchanged;
- V0.2 breaker exact;
- A0 V0.3 contract unchanged;
- all four Python artifacts compile.

## Preserved existing suite

`24/24 PASS`

The previously closed historical + V0.1 suite remains unchanged.

## Persisted V0.2 failure profile

Reproduced exactly:

```
TOTAL = 18
PASS  = 4
FAIL  = 14
```

PASS:

- AC05;
- AC07;
- AC08;
- AC18.

FAIL:

- AC01;
- AC02;
- AC03;
- AC04;
- AC06;
- AC09;
- AC10;
- AC11;
- AC12;
- AC13;
- AC14;
- AC15;
- AC16;
- AC17.

## Confirmed defect groups

The persisted failure profile confirms the nine groups already recorded:

- `A0-ABF2-01` mandatory carrier/extraction representation absent;
- `A0-ABF2-02` control-state authority / critical precedence absent;
- `A0-ABF2-03` native-status conflict fail-closed rule absent;
- `A0-ABF2-04` source supersession enforcement absent;
- `A0-ABF2-05` exact registry-content authority not pinned;
- `A0-ABF2-06` post-observation profile widening not blocked;
- `A0-ABF2-07` exact normalization-policy content authority not pinned;
- `A0-ABF2-08` exact six-dimension permission schema not enforced;
- `A0-ABF2-09` operational-semantic permission guard absent.

No additional defect group is introduced by the persisted-head re-break.

## Verdict

`A0_ADVERSARIAL_V0_2_PERSISTED_REBREAK = PASS_FAILURE_PROFILE_REPRODUCED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_2`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed boundary

`A0 — MINIMAL CORRECTION CANDIDATE FOR A0-ABF2-01..09`

The correction must preserve, unchanged:

- the historical six tests;
- adversarial V0.1;
- adversarial V0.2;
- contract V0.3.

No test expectation may be changed after observation.
