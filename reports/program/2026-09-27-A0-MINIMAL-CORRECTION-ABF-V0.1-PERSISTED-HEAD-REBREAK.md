# A0 — MINIMAL CORRECTION ABF V0.1 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`7e2a0052e99669ed42e55bbd9a81cf0a23a4c0f2`

Correction implementation blob:

`c7c1f37d9d306e0424274b276d42ab422beac560`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

Adversarial breaker V0.1 blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Pre-persistence sandbox qualification run:

`36326117765`

Fresh persisted-head re-break run:

`36326229769`

## Persistence scope

The governed correction commit modifies exactly:

`src/a0_research_authority.py`

No contract, adjudication, historical breaker or adversarial breaker was modified.

## Correction scope

The candidate is limited to the six defect groups established by the persisted adversarial V0.1 failure profile:

- A0-ABF-01 — measurement strict typing / extraction absent;
- A0-ABF-02 — expected-family authority not pinned;
- A0-ABF-03 — D1 / MC2 fail-closed permission overrides missing;
- A0-ABF-04 — D3 CONFIRMED guard missing;
- A0-ABF-05 — Global Normalization Policy authority not pinned;
- A0-ABF-06 — Source Profile Registry / profile authority not pinned.

The implementation adds only synthetic-V0.1 authority bindings and the minimum validation/guard logic needed to close these groups.

## Fresh persisted-head verification

Structural verification:

`PASS`

Compilation:

- `src/a0_research_authority.py` = PASS;
- historical breaker = PASS;
- adversarial breaker V0.1 = PASS.

Historical suite:

`6/6 PASS`

Adversarial expansion V0.1:

`18/18 PASS`

Closed combined suite:

`24/24 PASS`

The previously failing attacks now pass:

- AB03;
- AB04;
- AB08;
- AB10;
- AB11;
- AB13;
- AB14;
- AB15;
- AB16.

The nine attacks that already passed remain green:

- AB01;
- AB02;
- AB05;
- AB06;
- AB07;
- AB09;
- AB12;
- AB17;
- AB18.

## Local verdict

`A0_MINIMAL_CORRECTION_ABF_V0_1 = PASS_24_OF_24`

`A0_MINIMAL_CORRECTION_ABF_V0_1_PERSISTED_REBREAK = PASS`

The six A0-ABF-01..06 defect groups are closed relative to the current 24-test suite.

## Qualification ceiling

This is NOT full A0 V0.3 implementation qualification.

The V0.3 contract contains additional mandatory adversarial families that are not exhausted by the current 18-test expansion.

Therefore:

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1, A2, DecisionPolicy, Decision, ACTION, trading, MT5, real C01 access or C01 scientific scoring is authorized.

## Next governed boundary

Continue A0 only.

Next boundary:

`A0 — ADVERSARIAL BREAK EXPANSION V0.2`

V0.2 must derive additional attacks only from already-adopted V0.3 requirements, preserve the historical six tests and adversarial V0.1 tests unchanged, and must not introduce new normative decisions.
