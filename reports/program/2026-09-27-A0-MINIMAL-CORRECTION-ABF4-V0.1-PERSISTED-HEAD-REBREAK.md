# A0 — MINIMAL CORRECTION ABF4 V0.1 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`83eded5ecd1a073a8c44f61975b8e14664a0ced2`

Correction implementation blob:

`18246b818c6c6af8c5412c3b0a515f76c5d5ddc8`

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

Pre-persistence sandbox qualification run:

`36331313770`

Fresh persisted-head re-break run:

`36331412143`

## Persistence scope

The governed correction commit modifies exactly:

`src/a0_research_authority.py`

No contract or breaker was modified by the correction commit.

## Correction scope

The runtime correction is limited to the four persisted V0.4 defect groups:

- A0-ABF4-01 — preregistration content is pinned to the admitted schema + exact expected-family carrier shape;
- A0-ABF4-02 — an explicitly represented evidence level for the admitted synthetic authority must remain N0, while absent evidence remains UNDETERMINED; research class remains N0_EXPLORATORY_SYNTHETIC;
- A0-ABF4-03 — admitted data/confirmatory combinations are limited to the two combinations already exercised by the closed suite: SYNTHETIC_ONLY + NOT_CONFIRMATORY and REAL + NOT_ESTABLISHED;
- A0-ABF4-04 — the N0 evidence guard prevents CONFIRMED from creating N4 authority.

The existing REAL + NOT_ESTABLISHED + CONFIRMED V0.1 case remains accepted as an input and remains normalized to NO_SCIENTIFIC_CLAIM.

## Fresh persisted-head verification

Structural verification:

`PASS`

Compilation:

- runtime = PASS;
- historical breaker = PASS;
- adversarial V0.1 = PASS;
- adversarial V0.2 = PASS;
- adversarial V0.3 = PASS;
- adversarial V0.4 = PASS.

Closed combined suite:

`85/85 PASS`

Therefore:

- historical = 6/6 PASS;
- V0.1 = 18/18 PASS;
- V0.2 = 18/18 PASS;
- V0.3 = 22/22 PASS;
- V0.4 = 21/21 PASS.

The six attacks previously failing in V0.4 now pass without changing their expectations:

AE09, AE10, AE11, AE12, AE13, AE14.

## Local verdict

`A0_MINIMAL_CORRECTION_ABF4_V0_1 = PASS_85_OF_85`

`A0_MINIMAL_CORRECTION_ABF4_V0_1_PERSISTED_REBREAK = PASS`

The groups A0-ABF4-01..04 are closed relative to the current 85-test suite.

## Qualification ceiling

This does NOT yet establish full A0 V0.3 implementation qualification.

Mandatory V0.3 mutation families remain untested or materially under-tested, including examples such as diagnostic-to-primary promotion, source-specific invalid metric domains, removed-permission reappearance and SUPPORTED-driven permission addition.

Therefore:

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1, A2, DecisionPolicy, Decision, ACTION, trading, MT5 or real C01 access/scoring is authorized.

## Next governed boundary

`A0 — ADVERSARIAL BREAK EXPANSION V0.5`

V0.5 must derive only from remaining already-adopted V0.3 mutation requirements, preserve all 85 current tests unchanged, and introduce no new normative decision.
