# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — QUALIFICATION

Date: 2026-10-03

## Verdict

`RPE-02 = QUALIFIED_FOR_EXTERNAL_REVIEW`

Human adoption is pending. RPE-04/RPE-05/RPE-06 and REAL P5-E remain closed.

## Canonical base

RPE-01 adoption commit:
`8ed3ec4079f3f996a5159b78fc40d0f32a917b25`

RPE-01 adoption blob:
`49203ebc2fb208c5dd23ded140295ac00c0afab6`

The adopted P5-E contract, synthetic timing model and P5-D4 runtime remain byte-identical to the RPE-01 base.

## Preregistration and RED

Preregistration HEAD:
`c42a0f3df48807b3681db782f0a6fd58bd5c7aea`

Preregistration blob:
`614d3724c5c36bbdb6afbf9b49a31f88da465719`

Closed-schema blob:
`923671b1539585b5c32c8e2d284598b521fc0bba`

The preregistration validates through the adopted RPE-01 public entrypoint.

RED HEAD:
`03394a8a85680ca24a2593d14466c192fd208e8e`

Observed RED:
`17 tests / 15 failures / 2 passes`.

The failures were caused by the preregistered real-time module not yet existing.

## Final implementation

Implementation HEAD:
`c17d68b04de9dca13f9d9ed655e034b13436484d`

Module:
`db5dcfe8ad3b7ce93099368b459bb09ac25f933b`

Main tests:
`23618a9317c554099670e84482641a8014f8682d`

Mutation tests:
`77cdadb376320c4e8f591a3a80105feac250b716`

The implementation is a separate nanosecond-native real timing component. The adopted synthetic model is unchanged and is used only as semantic/exact-grid parity reference.

## Qualified timing semantics

Normative representation:
`INTEGER_MONOTONIC_NANOSECONDS`

Preregistered exact constants:
- poll interval = 30,000,000,000 ns;
- detection bound = 60,000,000,000 ns.

Required evidence fields include:
- schedule_origin_ns;
- scheduled_at_ns;
- attempt_started_at_ns;
- remote_observation_completed_at_ns;
- attempt_completed_at_ns;
- controlled_source_release_started_at_ns.

The qualified component distinguishes scheduled slot from actual attempt start. A scheduled-on-time attempt cannot hide an actual start at or after the next fixed-rate slot.

Detection eligibility uses actual attempt start. A target observation produced by an attempt started before controlled source release is blocked for adjudication.

Detection latency is:
`remote_observation_completed_at_ns - controlled_source_release_started_at_ns`.

Full attempt completion is retained for timeline/overlap validity but does not replace the remote-observation completion endpoint.

Equality boundaries are frozen:
- exactly 60 seconds = PASS;
- 60 seconds + 1 ns = FAIL;
- remote completion exactly at the next slot = allowed;
- remote completion after the next slot = blocked;
- previous attempt completion exactly at next attempt start = allowed;
- previous completion greater than next start = overlap blocked.

## Governed configuration provenance

RPE-02's preregistration and schema are governed RPE-01 artifacts.

A dedicated parity test proves the implementation constants equal the governed preregistration values.

No environment variable, CLI argument or unlisted file supplies normative timing authority.

## Mutation/discrimination

Four targeted mutants were killed:

1. exact latency bound `<=` changed to `<`;
2. actual-start next-slot `>=` changed to `>`;
3. remote-completion next-slot `>` changed to `>=`;
4. latency endpoint changed from remote completion to full attempt completion.

Result:
`4 / 4 KILLED`.

## Test result

Dedicated RPE-02 surface:
`22 / 22 PASS`

P5-E + RPE-01 + RPE-02 targeted regression:
`135 / 135 PASS`

Protected diffs:
```text
P5-E CONTRACT = 0
P5-E SYNTHETIC MODEL = 0
P5-D4 RUNTIME = 0
```

## Host monotonic-clock capability evidence

Observed on the qualification host:
- API: `time.monotonic_ns`;
- monotonic: true;
- adjustable: false;
- resolution: 1e-7 seconds;
- implementation: `QueryPerformanceCounter()`;
- samples were integer nanoseconds and non-decreasing;
- same-process host domain: true.

Environment:
`CPython 3.13.14 / Windows-11-10.0.22631-SP0`.

This host evidence is non-normative context; the verdict semantics remain integer-nanosecond based.

## Authority boundary

This qualification does not authorize:
- RPE-04/05/06;
- network observation;
- GitHub polling;
- P5-D4 real-state mutation;
- Vault/CURRENT mutation;
- REAL P5-E;
- human adoption of RPE-02.

Maximum claim:
`RPE02_REAL_TIME_REPRESENTATION = QUALIFIED_FOR_EXTERNAL_REVIEW`.
