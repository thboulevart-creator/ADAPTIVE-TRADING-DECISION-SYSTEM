# A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING GOVERNANCE DECISION

Date: 2026-09-27

Repository:
`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Governed branch:
`integration/system-v1`

Decision base HEAD:
`6f55748df1abbc72e437b077ed7912d6e15803a1`

A0 V0.3 contract blob:
`f1168481879f33f8762dcb1e19e2ad35211c8ec2`

Frozen metric-domain authority blob:
`dd205d3e7b4a522a5ba23cef1e665d51c196acb8`

Standalone qualifier blob:
`9bd05f2a2a97f092c0fc2988319f15caff57dda3`

Standalone qualification report blob:
`fd89cea2fffa4a15cddf27bb8d90cdaa0d694b1a`

## 1. Decision

A runtime binding MAY be introduced in a later implementation boundary, but only under the exact integration contract frozen here.

This document authorizes TEST-FIRST specification of the binding.

It does NOT itself authorize mutation of `src/a0_research_authority.py`.

It does NOT authorize AF04 re-adjudication.

## 2. Applicable producer/source pair

The binding is applicable only when both exact identities are already established by existing A0 authority:

```
producer_identity =
ATDS_A0_SYNTHETIC_PRODUCER_V0_1

source_schema =
ATDS_A0_SYNTHETIC_SCIENTIFIC_RESULT_V0_1
```

No caller may select, replace, widen or disable this applicability rule.

Any future producer/source pair requires a separate governance decision.

## 3. Authority resolution

The metric-domain authority SHALL NOT become a new caller-supplied A0 case input.

The runtime binding SHALL resolve the authority only from the fixed governed repository path:

`GOVERNANCE/A0-SYNTHETIC-PRODUCER-METRIC-DOMAIN-AUTHORITY-V0.1.json`

Expected authority identity:

`ATDS_A0_SYNTHETIC_PRODUCER_METRIC_DOMAIN_AUTHORITY_V0_1`

Expected authority content SHA-256:

`5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492`

The exact frozen authority bytes are validated by:

`src/a0_metric_domain_authority.py::validate_measurement_domain`

No environment variable, caller path, caller bytes, case key, Source Profile field or Global Normalization Policy field may select an alternate metric-domain authority.

## 4. Fail-closed authority availability

For the applicable producer/source pair, the exact frozen authority is mandatory for every A0 derivation, even when the source contains no measurement.

If the authority file is:

- missing;
- unreadable;
- byte-different;
- reconstructed with different bytes;
- wrong schema/version;
- otherwise rejected by the qualified standalone authority logic;

then:

`NO AUTHORITATIVE OUTPUT`

No permissive fallback is authorized.

This rule ensures that a projection cannot be produced under an applicable source family while silently losing its producer-specific metric-domain authority.

## 5. Exact runtime invocation point

The future binding in `derive_authoritative_projection(case)` SHALL occur only after existing A0 has successfully established:

1. exact source schema;
2. exact producer identity;
3. exact source/producer agreement;
4. exact Source Profile Registry resolution;
5. exact Source Profile binding;
6. exact expected-family authority.

The frozen authority SHALL then be resolved and verified before scientific normalization, permission derivation and canonical output construction.

For each present `finding.measurement`, the existing strict parsing of:

- `measurement.metric`;
- `measurement.value`;

remains in force.

Immediately after those values are extracted/strictly parsed, and before they can enter authoritative measurement references, the runtime SHALL call the standalone qualifier using:

```
authority_raw = exact frozen governed authority bytes
producer_identity = already-governed A0 producer identity
source_schema = already-governed A0 source schema
metric_identity = source-native measurement.metric
metric_value = source-native measurement.value
source_profile_claim = None
normalization_policy_claim = None
```

A qualifier result other than exact `True` produces:

`NO AUTHORITATIVE OUTPUT`

## 6. Source Profile composition

The Source Profile remains extraction/binding authority only.

It may continue to identify `findings[*].measurement` as an extraction path where the rich profile applies.

It MUST NOT supply any of the following to the metric-domain qualifier:

- admitted metric identity;
- alias;
- metric-domain widening;
- numeric bound;
- fallback;
- alternate authority path/hash;
- validation override.

Existing Source Profile structural validation remains earlier fail-closed protection.

The metric-domain qualifier validates source-native metric/value after extraction. It does not read a metric-domain definition from the Source Profile.

## 7. Global Normalization Policy isolation

The Global Normalization Policy remains authoritative only for its existing scientific-normalization and A0 permission semantics.

The runtime SHALL NOT pass metric-domain authority from the Global Normalization Policy into the qualifier.

The metric-domain binding MUST NOT add:

- raw-status mappings;
- scientific conclusions;
- evidence levels;
- permission dimensions;
- permission tokens;
- Decision semantics;
- ACTION semantics.

The exact six-dimension permission intersection remains unchanged.

## 8. Measurement coverage

For the applicable producer/source pair, every present `finding.measurement` is subject to the metric-domain qualifier.

This applies whether the current Source Profile is the base admissible profile or the rich admissible profile.

The binding MUST NOT validate only SUPPORTED findings.

It MUST also validate measurements attached to:

- REFUTED;
- NOT_INTERPRETABLE;
- NO_SCIENTIFIC_CLAIM;

because measurement identity remains authoritative trace data even when positive evidence consumability is false.

## 9. Carrier / trace representation

A successfully derived A0 projection for the applicable producer/source pair SHALL add exactly these represented properties:

```
metric_domain_authority_identity
metric_domain_authority_sha256
metric_domain_validation
```

Required values:

```
metric_domain_authority_identity =
ATDS_A0_SYNTHETIC_PRODUCER_METRIC_DOMAIN_AUTHORITY_V0_1

metric_domain_authority_sha256 =
5813f9d75395308386b4561b13c4eae889a4565cca3289f08a30d81657057492
```

`metric_domain_validation` is a mapping keyed by finding id.

For every finding with a present measurement:

```
finding_id -> "PASS"
```

Findings without a measurement are absent from that mapping.

The authority identity/hash are still present when the mapping is empty.

These fields are trace properties only. They create no scientific or operational authority.

They participate in the canonical projection hash through the existing canonical payload derivation.

## 10. Caller confinement

Caller-provided fields such as:

- `metric_domain_authority`;
- `metric_domain_authority_path`;
- `metric_domain_authority_sha256`;
- `metric_domain_validation`;
- `metric_identity_domain`;
- `metric_aliases`;

carry no authority and MUST NOT alter binding selection, qualifier inputs, carrier values or permissions.

No caller-provided field may disable metric-domain validation.

## 11. Verification / reconstruction

`verify_authoritative_projection(case, projection)` continues to establish authority only through deterministic re-derivation.

A projection with altered:

- metric-domain authority identity;
- authority SHA-256;
- validation mapping;
- measurement metric/value;

must fail verification even if a caller recomputes `canonical_projection_sha256`.

No separately reconstructed metric-domain trace object carries authority.

## 12. Missing / corrupt authority semantics

The integration is fail-closed for the applicable pair:

```
authority missing
→ NO AUTHORITATIVE OUTPUT

authority bytes mismatch
→ NO AUTHORITATIVE OUTPUT

qualifier unavailable
→ NO AUTHORITATIVE OUTPUT

qualifier exception
→ NO AUTHORITATIVE OUTPUT

qualifier False
→ NO AUTHORITATIVE OUTPUT
```

The future implementation MAY express this through the current A0 fail-closed exception path. No permissive return object is required.

## 13. AF04 separation

AF04 remains outside the runtime-binding qualification family.

The literal used by AF04 MUST NOT appear in the independent runtime-binding breaker.

Passing the future binding test family does not itself constitute AF04 re-adjudication.

AF04 may be re-run only after:

1. the runtime-binding test family is preregistered and persisted before execution;
2. a binding candidate is implemented without changing those expectations;
3. the full frozen pre-existing suite remains PASS;
4. the binding candidate receives a fresh persisted-head re-break PASS.

## 14. Existing qualification preservation

The future binding MUST preserve unchanged:

```
existing A0 suite = 85 tests
metric-domain standalone authority family = 22 tests
TOTAL EXISTING = 107 tests
```

No historical test expectation may be modified to accommodate the binding.

## 15. Runtime implementation ceiling

The later implementation boundary may modify only the minimum necessary integration surface.

Expected primary runtime file:

`src/a0_research_authority.py`

The already-qualified standalone qualifier:

`src/a0_metric_domain_authority.py`

MUST remain unchanged unless a separate breaker establishes a defect in that qualifier.

The frozen authority artifact MUST remain unchanged.

## 16. Current authorization state

```
METRIC_DOMAIN_AUTHORITY_STANDALONE_QUALIFICATION = PASS
METRIC_DOMAIN_RUNTIME_BINDING_GOVERNANCE_DECISION = ADOPTED
METRIC_DOMAIN_RUNTIME_BINDING = NOT_IMPLEMENTED
METRIC_DOMAIN_RUNTIME_BINDING_QUALIFICATION = NOT_YET
AF04_READJUDICATION = NOT_AUTHORIZED
ABF5_RUNTIME_CORRECTION = NOT_AUTHORIZED
A0_V0_3_FULL_IMPLEMENTATION_QUALIFICATION = NOT_YET
```

## 17. Next governed boundary

`A0 — SYNTHETIC PRODUCER METRIC-DOMAIN RUNTIME BINDING TEST-FIRST RED`

That boundary MUST, before any runtime binding implementation:

- preregister and persist an independent integration breaker;
- preserve all 107 current tests unchanged;
- include a positive exact-binding control;
- test missing/corrupt authority fail-closed behavior;
- test runtime metric validation with independent metric mutations;
- test carrier authority identity/hash/validation-map preservation;
- test caller inability to select or disable the authority;
- test Source Profile / Global Normalization Policy isolation;
- test canonical reconstruction/tampering;
- exclude AF04 and its observed metric literal.

No runtime mutation is authorized until that persisted RED exists.

No A1/A2/DecisionPolicy/Decision/ACTION/trading/MT5/real-C01 authority is opened.
