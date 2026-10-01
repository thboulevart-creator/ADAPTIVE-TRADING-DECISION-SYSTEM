# P5-E V0.1 — CONTRACT + SYNTHETIC QUALIFICATION

Date: 2026-10-01

## Verdict

```text
P5E_V0_1_PREREGISTRATION
= PASS

P5E_V0_1_RED_TEST_FIRST
= PASS

P5E_V0_1_MINIMAL_GREEN
= 17 / 17 PASS

P5E_V0_1_ADVERSARIAL_SURFACE
= 42 / 42 PASS

P5E_TARGETED_PREDECESSOR_REGRESSION
= 208 / 208 PASS

P5E_CROSS_CUTTING_REGRESSION
= 876 / 876 PASS

FULL_OBSIDIAN_REBREAK
= 1466 / 1466 PASS

P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED

P5E_REAL_END_TO_END
= NOT_QUALIFIED

HUMAN_NORMATIVE_ADOPTION
= PENDING
```

## Scope

This qualification is deliberately narrower than the phase name.

It qualifies:

- the P5-E temporal contract;
- exact inherited 30-second observation interval;
- exact inherited 60-second maximum detection latency;
- explicit detection-latency semantics;
- a pure synthetic timing model;
- authority boundaries;
- P5-D4 queue interaction under burst/newer-head pressure;
- fail-closed behavior;
- synthetic-to-real claim separation.

It does not qualify a real repeated polling system.

## Artifact identities

Preregistration:

`6ef788532a1e945a42ca524af823710ae4f14ed6`

RED test:

`2305e0768182d82657c34a7cb53c502714a2ab81`

Contract:

`e5c3d7a9d451aba65e8062078c6c10d23e586f39`

Synthetic timing model:

`8662dd97a1c8a1af33d6593ae923384e96404b5a`

Adversarial test:

`6235c4b2addc16acd043832664440ec76f6dada2`

RED evidence:

`6de316c3c968c2b73122170bb2b86fbec6093951`

Minimal GREEN evidence:

`10bddb856462d16c6a214ccb3f31a2a8a554e748`

Adversarial qualification:

`7068dacade8c7263ab6a6f70dab360f1b53cc6f9`

P5-D4 lifecycle regression correction:

`1d015548ad69b790494da42d29c6167e65cbc624`

Targeted regression qualification:

`d3f089762f84368e4f071890af4b1be55d19b896`

## Timing contract

Inherited P5-A parameters are preserved exactly:

```text
POLL_INTERVAL_SECONDS
= 30

DETECTION_LATENCY_SECONDS_MAX
= 60
```

Detection latency is defined as:

```text
FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME
-
SOURCE_HEAD_AVAILABLE_TIME
```

The future real timing implementation must use monotonic elapsed time for bound enforcement.

The synthetic model uses explicit injected seconds only.

No `sleep`, network, filesystem state, process launch, real P5-D4 state, or real Vault access is part of the synthetic model.

## Queue semantics resolution

A conflict was identified between:

- earlier P5-A design intent allowing superseded-head skipping/coalescing;
- current qualified executable P5-D4 V0.1 semantics forbidding silent drop, latest-only replacement, direct queue mutation, and coalescing.

P5-E V0.1 resolves this in favor of the current qualified P5-D4 semantics.

Therefore:

```text
FIFO
= REQUIRED

SILENT_DROP
= FORBIDDEN

LATEST_ONLY_REPLACEMENT
= FORBIDDEN

COALESCING
= NOT_AUTHORIZED

QUEUE_CAPACITY_EXHAUSTED
= QUEUE_CAPACITY_REQUIRES_ADJUDICATION

PENDING_HEAD_RETARGET
= FORBIDDEN
```

## Current real context observed read-only

At P5-E opening:

```text
LIVE_PROJECTION_HEAD
= 59f1dc26973b0b50efefccf12b26784d1e41f546

QUEUED_UNEVALUATED_HEAD
= 1d4c2f3d657b36ecaa6ab25b967e46b3620190d1
```

The remote branch later observed read-only was:

`fcca78571a26955ae3fe462746ef49557e4e84e5`

and the queued HEAD is an ancestor of that remote HEAD.

This real context was evidence only. It was not used as authorization to evaluate either HEAD.

## Authority boundary

Throughout this stage:

```text
REAL_POLLING_LOOP
= NOT_AUTHORIZED

PENDING_HEAD_EVALUATION
= NOT_AUTHORIZED

EVALUATION
= NOT_AUTHORIZED

STAGE_A
= CLOSED

STAGE_B
= CLOSED

PROMOTION
= NOT_AUTHORIZED

PUBLICATION
= NOT_AUTHORIZED

REAL_VAULT_MUTATION
= NOT_AUTHORIZED

CURRENT_MUTATION
= NOT_AUTHORIZED

P6
= CLOSED
```

## Claim boundary

The maximum claim supported by this evidence is exactly:

`P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED`

The following claims remain forbidden:

- `P5E_REAL_END_TO_END_QUALIFIED`;
- `CONTINUOUS_SYNCHRONIZATION_QUALIFIED`;
- `REAL_60_SECOND_SLA_QUALIFIED`;
- automatic evaluation qualified;
- automatic promotion qualified;
- automatic publication qualified.

## External adversarial review gate

Before normative human adoption, the candidate must be reviewed externally using the persisted self-contained review packet.

The external reviewer is asked to attack:

- timing semantics;
- 30/60-second inheritance;
- the meaning of end-to-end;
- clock choice;
- transient network failure logic;
- queue saturation and multi-head arrival;
- P5-A/P5-D4 conflict resolution;
- authority leakage;
- synthetic-to-real evidence laundering;
- hidden paths to evaluation/promotion/publication;
- missing adversarial cases.

External review does not itself create authority.

## Mandatory stop

```text
REAL_P5E_EXECUTION
= CLOSED

HUMAN_NORMATIVE_ADOPTION
= PENDING

STOP
= TRUE
```

No real P5-E execution is authorized by this qualification.
