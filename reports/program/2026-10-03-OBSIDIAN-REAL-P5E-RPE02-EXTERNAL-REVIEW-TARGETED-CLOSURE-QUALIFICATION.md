# RPE-02 — EXTERNAL REVIEW TARGETED CLOSURE V0.1 — QUALIFICATION

Date: 2026-10-03

## Result

`RPE-02 TARGETED CLOSURE = QUALIFIED_FOR_EXTERNAL_DELTA_REVIEW`

The prior external verdict was `FAIL`. No human adoption is created by this qualification.

## Closure identities

External review blob:
`45766b0ad21a62447b9233ec1563eb85825f221d`

Internal adjudication:
`836450b88ae69254dda77f548ede19bfaae1cb86`

Targeted preregistration:
`cafee7194155944eb059ead466fd6bc517edde58`

Targeted preregistration schema:
`d67da710e63643c26c0a004cc38109ff4e301b25`

Targeted RED HEAD:
`afaafb9f3b9fb3a4d90cfa912b7eb176abc19161`

Targeted RED test:
`0756598131911168a7cb5944c0ed465c7ebbd2a0`

Targeted RED report:
`b558fceaf0b214715ef65cd710ebb391464778d0`

Final candidate HEAD:
`4a28540eafa82fd136dd4a402ef552f22f817f36`

Final implementation:
`31db5d944a25e54db81bd901a087cdc2039925ad`

Targeted mutation tests:
`c00bb49ffa930aefcdce794c5b7a7c68211e586f`

## BF-1

Observation integrity is now closed before business verdicting.

Allowed outcome vocabulary is exactly:
- READ_FAILURE;
- REMOTE_HEAD_OBSERVED.

REMOTE_HEAD_OBSERVED requires a lowercase 40-hex head.
READ_FAILURE requires observed_head = null.
Unknown outcomes and incoherent outcome/head combinations raise RPE02TimingError before any SLA status can be produced.

## NB-1

The actual attempt start is test-locked as the release-eligibility field in both:
- first-detection eligibility;
- pre-release target handling.

Mutation tests also lock:
- actual start before scheduled;
- remote completion before actual start;
- attempt completion before remote completion;
- duplicate slot;
- cadence gap;
- skipped required attempt.

## NB-2

No-detection semantics now follow fixed-rate feasibility:

`next_required_slot_ns - release_ns > bound_ns`
→ `FAIL_NO_DETECTION_BY_BOUND`
with `NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND`.

At exact equality, the result remains INCOMPLETE because a future attempt can still meet the bound exactly.

Both external-review counterexamples now converge with the adopted synthetic reference.

## NB-3

Observations are no longer silently sorted.

A supplied scheduled timestamp lower than the preceding supplied timestamp returns:
`BLOCKED_REQUIRES_ADJUDICATION / OBSERVATION_ORDER_NOT_STRICTLY_INCREASING`.

Duplicate slots retain their dedicated failure code.

## NB-4 adjudication

The SLA endpoint remains:
`remote_observation_completed_at_ns`.

`attempt_completed_at_ns` remains timeline/overlap evidence only.

The runtime execution guarantee `NO REAL ATTEMPT OVERLAP` is explicitly carried to RPE-05.

## Evidence

Targeted closure:
`15 / 15 PASS`

Targeted mutation discrimination:
`12 / 12 PASS; 12 / 12 mutants killed`

P5-E + RPE-01 + RPE-02 regression:
`162 / 162 PASS`

Protected diffs:
- P5-E contract = 0;
- P5-E synthetic model = 0;
- P5-D4 runtime = 0.

## Packet-fidelity rule

The rebuilt delta-review packet must distinguish:
- original historical RED test blob `089a72c736302abd08ea1267c149e2ef771240db`;
- original final test blob `23618a9317c554099670e84482641a8014f8682d`;
- targeted historical RED test blob `0756598131911168a7cb5944c0ed465c7ebbd2a0`.

No final test may be labeled as a historical RED copy.

## Authority

RPE-02 human adoption = pending.
RPE-04/05/06 = closed.
REAL P5-E = closed.
