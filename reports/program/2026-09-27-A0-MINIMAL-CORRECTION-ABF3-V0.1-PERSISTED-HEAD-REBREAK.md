# A0 — MINIMAL CORRECTION ABF3 V0.1 — PERSISTED-HEAD RE-BREAK

Date: 2026-09-27

Reviewed governed HEAD:

`a3d36fa417293bd6b436f622df73d157f36e41d8`

Correction implementation blob:

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

Pre-persistence sandbox qualification run:

`36329233204`

Fresh persisted-head re-break run:

`36329309592`

## Persistence scope

The governed correction commit modifies exactly:

`src/a0_research_authority.py`

No contract or breaker was modified by the correction commit.

## Correction scope

The runtime correction is limited to the six defect groups established by the persisted V0.3 break:

- A0-ABF3-01 — canonical exact-byte representation for the governed preregistration, registry, profile and normalization-policy authorities;
- A0-ABF3-02 — admitted registry supersession metadata remains pinned;
- A0-ABF3-03 — profile-declared global native status is mandatory and preserved;
- A0-ABF3-04 — present measurement scope is preserved in the authoritative carrier;
- A0-ABF3-05 — present narrative text contributes only an opaque content-identity reference;
- A0-ABF3-06 — currently admitted permission-table entries are content-pinned while already-qualified missing-source fail-closed cases remain valid.

## Fresh persisted-head verification

Structural verification:

`PASS`

Compilation:

- runtime = PASS;
- historical breaker = PASS;
- adversarial V0.1 = PASS;
- adversarial V0.2 = PASS;
- adversarial V0.3 = PASS.

Closed combined suite:

`64/64 PASS`

Therefore:

- historical = 6/6 PASS;
- V0.1 = 18/18 PASS;
- V0.2 = 18/18 PASS;
- V0.3 = 22/22 PASS.

The ten attacks previously failing in V0.3 now pass without changing their expectations:

AD04, AD05, AD06, AD07, AD08, AD09, AD10, AD13, AD15, AD16.

The twelve V0.3 attacks already passing remain green.

## Local verdict

`A0_MINIMAL_CORRECTION_ABF3_V0_1 = PASS_64_OF_64`

`A0_MINIMAL_CORRECTION_ABF3_V0_1_PERSISTED_REBREAK = PASS`

The groups A0-ABF3-01..06 are closed relative to the current 64-test suite.

## Qualification ceiling

This does NOT yet establish full A0 V0.3 implementation qualification.

Mandatory V0.3 adversarial families still contain untested or materially under-tested cases beyond the current 64-test suite.

Therefore:

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

No A1, A2, DecisionPolicy, Decision, ACTION, trading, MT5 or real C01 access/scoring is authorized.

## Next governed boundary

`A0 — ADVERSARIAL BREAK EXPANSION V0.4`

V0.4 must derive only from remaining already-adopted V0.3 requirements, preserve all 64 current tests unchanged, and introduce no new normative decision.
