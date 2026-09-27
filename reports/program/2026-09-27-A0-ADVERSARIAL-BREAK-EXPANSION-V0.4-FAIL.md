# A0 — ADVERSARIAL BREAK EXPANSION V0.4 — FAIL

Date: 2026-09-27

Governed base HEAD:

`c358fe46701be10cfb7059a934318a61206a7ade`

Target implementation blob:

`4b4737238d01be0b1017b07cf33742797cb995eb`

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

Sandbox workflow run:

`36330306803`

## Scope

V0.4 adds 21 attacks derived only from already-adopted V0.3 requirements that remained untested or materially under-tested.

The expansion covers:

- +Infinity / -Infinity parsing;
- bool and numeric-string measurement values;
- zero/negative exact-int sample sizes;
- post-observation profile applicability/status-path mutation;
- pinned preregistration content;
- cross-dimension N0 / research-class / data-class / confirmatory consistency;
- CONFIRMED != N4;
- SUPPORTED with zero permissions;
- monotonic permission restriction;
- recomputed-hash reconstruction;
- exact source-byte verification;
- narrative confinement;
- caller-selected profile confinement;
- foreign producer artifact rejection.

No historical/V0.1/V0.2/V0.3 test was modified. Runtime and contract were not modified.

## Preserved closed suite

`64/64 PASS`

## V0.4 result

```
TOTAL = 21
PASS  = 15
FAIL  = 6
```

PASS:

AE01, AE02, AE03, AE04, AE05, AE06, AE07, AE08, AE15, AE16, AE17, AE18, AE19, AE20, AE21.

FAIL:

AE09, AE10, AE11, AE12, AE13, AE14.

## Consolidated material defect groups

```
A0-ABF4-01
PREREGISTRATION EXACT CONTENT AUTHORITY NOT PINNED
(AE09)

A0-ABF4-02
N0 EVIDENCE / RESEARCH-CLASS CROSS-DIMENSION CONSISTENCY NOT ENFORCED
(AE10, AE11)

A0-ABF4-03
SYNTHETIC DATA / CONFIRMATORY CROSS-DIMENSION CONSISTENCY NOT ENFORCED
(AE12, AE13)

A0-ABF4-04
CONFIRMED != N4 FAIL-CLOSED GUARD INCOMPLETE
(AE14)
```

## Verdict

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_4 = BREAK_CONFIRMED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_4`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed action

Persist this exact V0.4 breaker and failure profile, then reproduce from the persisted governed HEAD:

- existing suite = 64/64 PASS;
- V0.4 = 15 PASS / 6 FAIL;
- failed set = AE09, AE10, AE11, AE12, AE13, AE14.

No runtime correction before that persisted-head reproduction.
