# A0 — ADVERSARIAL BREAK EXPANSION V0.3 — FAIL

Date: 2026-09-27

Governed base HEAD:

`731380d8f1dd851c52de732c1edaf70f28ecc3c5`

Target implementation blob:

`f0015894d001c0ced7d0edf881947e3a435ab5ca`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Adversarial V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Sandbox workflow run:

`36328425957`

## Scope

V0.3 adds 22 attacks derived only from mandatory V0.3 requirements that were still untested or materially under-tested.

No historical, V0.1 or V0.2 test was modified. The runtime and contract were not modified.

## Preserved closed suite

`42/42 PASS`

## V0.3 result

```
TOTAL = 22
PASS  = 12
FAIL  = 10
```

Passing attacks:

- AD01 — missing SUPPORTED member rejected;
- AD02 — missing NOT_INTERPRETABLE member rejected;
- AD03 — zero ACTIVE profile rejected;
- AD11 — NOT_REPRESENTED control preserved;
- AD12 — caller control replacement ignored;
- AD14 — caller measurement substitution ignored;
- AD17 — caller N4 redeclaration cannot upgrade native N0;
- AD18 — caller REAL redeclaration cannot upgrade native SYNTHETIC_ONLY;
- AD19 — caller confirmatory redeclaration cannot establish claim;
- AD20 — deepcopy reconstruction verifies only through exact governed re-derivation;
- AD21 — serialized reconstruction verifies through exact governed re-derivation;
- AD22 — hash-only object carries no authority.

Failing attacks:

- AD04 — semantically equal but byte-different registry can re-pin authority;
- AD05 — semantically equal but byte-different profile plus rehashed registry is accepted;
- AD06 — semantically equal but byte-different normalization policy is accepted;
- AD07 — semantically equal but byte-different preregistration is accepted;
- AD08 — forged registry supersession metadata is accepted;
- AD09 — configured global native artifact status is not preserved;
- AD10 — missing profile-declared native status path does not fail closed;
- AD13 — measurement scope is not preserved in the authoritative carrier;
- AD15 — present narrative has no opaque identity/reference in the carrier;
- AD16 — same-schema permission-table mutation is accepted.

## Consolidated material defect groups

```
A0-ABF3-01
EXACT PERSISTENT AUTHORITY BYTES NOT PINNED
(AD04, AD05, AD06, AD07)

A0-ABF3-02
REGISTRY SUPERSESSION METADATA AUTHORITY NOT PINNED
(AD08)

A0-ABF3-03
PROFILE-DECLARED NATIVE STATUS COMPLETENESS / PRESERVATION INCOMPLETE
(AD09, AD10)

A0-ABF3-04
MEASUREMENT SCOPE BINDING NOT PRESERVED
(AD13)

A0-ABF3-05
OPAQUE NARRATIVE IDENTITY / REFERENCE NOT PRESERVED
(AD15)

A0-ABF3-06
GLOBAL POLICY PERMISSION-TABLE CONTENT NOT EXACTLY PINNED
(AD16)
```

## Verdict

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_3 = BREAK_CONFIRMED`

`A0_CURRENT_IMPLEMENTATION = FAIL_ADVERSARIAL_EXPANSION_V0_3`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5 or real-C01 authority is opened.

## Next governed action

Persist this exact V0.3 breaker and failure profile, then reproduce from the persisted governed HEAD:

- existing suite = 42/42 PASS;
- V0.3 = 12 PASS / 10 FAIL;
- failed set = AD04, AD05, AD06, AD07, AD08, AD09, AD10, AD13, AD15, AD16.

No runtime correction is authorized before that persisted-head reproduction.
