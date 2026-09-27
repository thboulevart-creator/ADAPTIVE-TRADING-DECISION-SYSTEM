# A0 — ADVERSARIAL BREAK EXPANSION V0.5 — BLOCKED METRIC-DOMAIN ORACLE

Date: 2026-09-27

Governed base HEAD:

`8207458d2be02da09691cd8d76bc12ead0e51292`

Runtime blob:

`18246b818c6c6af8c5412c3b0a515f76c5d5ddc8`

Historical breaker blob:

`e02ecfa6d30c2877a33f5c5d81b161ee562202b6`

V0.1 breaker blob:

`2911d5b282ccbb6147b2b54a7db5c357c2d315b6`

V0.2 breaker blob:

`9833ce563305cfb6d6fe1de8907e8aa9fc96fda4`

V0.3 breaker blob:

`d23e3c72dd8bd2200cb392edc6c80b4e744d4751`

V0.4 breaker blob:

`efcc3ca7927b29b45f5d0dc0180b81176dbed51e`

A0 V0.3 contract blob:

`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Unqualified sandbox V0.5 breaker candidate:

`f02eae836b79403673f8a43292cca19eab0c6b33`

Sandbox breaker commit:

`f5f902339ddcf0f838790ca154001f91261f9d52`

Sandbox workflow run:

`36332006554`

## Preserved governed suite

The existing governed suite remained unchanged:

`85/85 PASS`

No existing test, runtime file or governed breaker was modified.

## Sandbox V0.5 candidate execution

The candidate contained 22 additional attacks.

Observed sandbox result:

```
PASS = 21
FAIL = 1
```

The sole pytest failure was:

`AF04 — foreign metric identity rejected for admitted synthetic producer`

The runtime accepted a source measurement whose metric identity was changed from the fixture value `SYNTHETIC_SCORE` to `FOREIGN_METRIC`.

## Governance adjudication of AF04

AF04 is NOT promoted to an implementation FAIL.

Reason:

A0 V0.3 states that producer-specific numeric domains remain producer/protocol responsibilities and requires the adversarial family `source-specific invalid metric domain`.

However, no pinned producer/protocol authority located in the governed A0/research artifacts establishes:

- an allowed metric-identity set for the synthetic producer;
- a numeric domain for `SYNTHETIC_SCORE`;
- a rule proving that `FOREIGN_METRIC` is invalid for that producer.

A targeted read-only search was performed across the A0 contract, A0 reports, research producer/interprocess contracts, research foundation/charter/findings artifacts, C01 producer/charter reports and research runtime artifacts. No explicit metric-domain authority was located.

Therefore the AF04 rejection oracle is not currently governed.

Changing the runtime to hardcode `SYNTHETIC_SCORE`, or inventing a numeric range, would introduce a new normative decision after observation.

That is forbidden by the current boundary.

## Status

`A0_EXISTING_85 = PASS_UNCHANGED`

`A0_V0_5_SANDBOX_CANDIDATE = 21_PASS_1_UNADJUDICABLE`

`AF04_IMPLEMENTATION_FAIL = NOT_ESTABLISHED`

`A0_ADVERSARIAL_BREAK_EXPANSION_V0_5 = BLOCKED_METRIC_DOMAIN_ORACLE`

`A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET`

`BLOCKED != PASS`

`BLOCKED != FAIL`

The V0.5 breaker candidate is intentionally NOT persisted into the governed breaker set.

No runtime correction is authorized.

## Next governed boundary

`A0 — SOURCE-SPECIFIC METRIC-DOMAIN AUTHORITY RESOLUTION`

Objective:

1. determine whether an already-qualified producer/protocol artifact can establish the metric identity/domain for the synthetic A0 fixture;
2. if such authority exists, bind it exactly before re-adjudicating AF04;
3. if it does not exist, record the authority gap and require an explicit governance decision before any new normative metric-domain contract is introduced.

Until that boundary is resolved:

- no ABF5 runtime correction;
- no full A0 V0.3 qualification;
- no A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority.
