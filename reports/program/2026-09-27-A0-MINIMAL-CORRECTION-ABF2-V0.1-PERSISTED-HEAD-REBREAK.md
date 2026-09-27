# A0 — MINIMAL CORRECTION ABF2 V0.1 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`7f607b4fab9df7e3976f62ede748d0ae97d5166b`

Correction implementation blob:

`f0015894d001c0ced7d0edf881947e3a435ab5ca`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

Adversarial V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Pre-persistence sandbox qualification run:

`36327697595`

Fresh persisted-head re-break run:

`36327769069`

## Persistence scope

The governed correction commit modifies exactly:

`src/a0_research_authority.py`

No contract, checkpoint, historical breaker, V0.1 breaker or V0.2 breaker was modified by the correction commit.

## Correction scope

The runtime correction is limited to the nine defect groups established by the persisted V0.2 break:

- A0-ABF2-01 — mandatory carrier / extraction representation;
- A0-ABF2-02 — control-state authority / critical precedence;
- A0-ABF2-03 — native-status conflict fail-closed;
- A0-ABF2-04 — source supersession enforcement;
- A0-ABF2-05 — registry content authority;
- A0-ABF2-06 — post-observation profile widening;
- A0-ABF2-07 — normalization-policy content authority;
- A0-ABF2-08 — exact permission-dimension closure;
- A0-ABF2-09 — operational-semantic permission guard.

## Fresh persisted-head verification

Structural verification:

`PASS`

Compilation:

- runtime = PASS;
- historical breaker = PASS;
- adversarial V0.1 = PASS;
- adversarial V0.2 = PASS.

Closed combined suite:

`42/42 PASS`

Therefore:

- historical = 6/6 PASS;
- V0.1 = 18/18 PASS;
- V0.2 = 18/18 PASS.

The fourteen attacks that previously failed in V0.2 now pass without changing their expectations:

AC01, AC02, AC03, AC04, AC06, AC09, AC10, AC11, AC12, AC13, AC14, AC15, AC16, AC17.

The four V0.2 attacks already passing remain green:

AC05, AC07, AC08, AC18.

## Local verdict

`A0_MINIMAL_CORRECTION_ABF2_V0_1 = PASS_42_OF_42`

`A0_MINIMAL_CORRECTION_ABF2_V0_1_PERSISTED_REBREAK = PASS`

The groups A0-ABF2-01..09 are closed relative to the current 42-test suite.

## Qualification ceiling

This does NOT establish full A0 V0.3 implementation qualification.

The contract V0.3 still contains mandatory adversarial families not yet exhausted by the historical, V0.1 and V0.2 breakers.

Therefore:

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1, A2, DecisionPolicy, Decision, ACTION, trading, MT5 or real C01 access/scoring is authorized.

## Next governed boundary

`A0 — ADVERSARIAL BREAK EXPANSION V0.3`

V0.3 must derive additional attacks only from already-adopted contract V0.3 requirements that remain untested or materially under-tested, preserve all 42 current tests unchanged, and introduce no new normative decision.
