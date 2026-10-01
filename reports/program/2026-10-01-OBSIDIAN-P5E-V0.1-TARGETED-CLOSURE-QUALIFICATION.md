# P5-E V0.1 — EXTERNAL REVIEW TARGETED CLOSURE QUALIFICATION

Date: 2026-10-01

## Qualification verdict

```text
EXTERNAL_REVIEW_B1_B5_INTERNAL_ADJUDICATION
= COMPLETE

TARGETED_CLOSURE_PREREGISTRATION
= PASS

TARGETED_CLOSURE_RED
= PASS

B1_TO_B5_TARGETED_GREEN
= 45 / 45 PASS

REQUIREMENT_EVIDENCE_MATRIX
= 43 / 43 MAPPED
= 0 UNMAPPED
= 0 DEFERRED

MATRIX_TEST
= 5 / 5 PASS

COMBINED_P5E_TARGETED_SURFACE
= 50 / 50 PASS

TARGETED_PREDECESSOR_REGRESSION
= 270 / 270 PASS

FULL_OBSIDIAN_REBREAK
= 1474 / 1474 PASS

P5E_V0_1_TARGETED_CLOSURE_CANDIDATE
= QUALIFIED_FOR_EXTERNAL_REREVIEW

EXTERNAL_REREVIEW
= PENDING

HUMAN_NORMATIVE_ADOPTION
= NOT_AUTHORIZED_YET

REAL_P5E
= CLOSED
```

## Corrected candidate identities

Contract:

`tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json`

blob:

`b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd`

Synthetic model:

`tools/obsidian_projection/p5e_near_real_time_model.py`

blob:

`b783717c9e9596b585b7b1686835c73fffbd1a7c`

Base tests blob:

`a4fbd35987b4abb4fe185f8ceee3f75bd749e23d`

Adversarial tests blob:

`3c0f556a02e8a8b5eae2e755116138d34a6c8ed8`

External-review closure tests blob:

`15c3e44ab9c1c40873110d88ff42cebb13a2643e`

Evidence-matrix test blob:

`ff9db4c6faca038e061a4247fe1cbccc466db254`

Evidence matrix blob:

`0440175fbb79877e466119cb973ea82389a4ecd8`

P5-D4 runtime remains:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## B1 closure — executable coverage

The former P5-E invariant gaps were closed.

Normative blocks now guarded include:

- timing;
- synthetic clock/model purity;
- head transition;
- queue/supersession;
- failure/freshness;
- authority;
- tip visibility;
- end-to-end claim scope;
- next-gate controls;
- exact required cases;
- exact base breakers;
- exact closure breakers.

The evidence matrix maps every required case/breaker to a concrete executable method and exact test-file Git blob.

Qualified P5-D2/P5-D4 behavior is reused when it is the actual owner of the semantic behavior.

## B2 closure — cadence

The timing model now requires a fixed-rate 30-second grid.

It separates:

- `scheduled_at_seconds`;
- `completed_at_seconds`.

Skipped required attempts and cadence gaps fail closed with:

`BLOCKED_REQUIRES_ADJUDICATION`

A schedule point merely divisible by 30 is no longer sufficient.

## B3 closure — impossible pre-release observation

The model no longer silently ignores an exact target observation from an attempt started before the controlled release.

Result:

`BLOCKED_REQUIRES_ADJUDICATION`

Failure code:

`TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE`

## B4 closure — falsifiable timing metric

The corrected candidate explicitly rejects `REMOTE_HEAD_AVAILABLE_TIME` as a directly measurable local monotonic origin.

The future real metric is:

```text
SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC
-
CONTROLLED_SOURCE_RELEASE_MONOTONIC
```

The schedule is fixed-rate.

Read duration is included in the latency.

The inherited bounds remain unchanged:

```text
POLL_INTERVAL = 30 seconds
MAX_LATENCY   = 60 seconds
```

This is a protocol for a future separately authorized real experiment.

It is not a real SLA result.

## B5 closure — remote-tip identity

The corrected candidate distinguishes:

```text
EXACT_TIP_OBSERVED
CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED
UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION
```

A commit contained by a later fast-forward head is not claimed to have been observed as a remote tip.

No unobserved intermediate tip may be injected into the P5-D2/P5-D4 queue.

A head already observed and queued remains protected by FIFO/no-replacement/no-retarget semantics.

No per-transient-tip detection SLA is claimed.

## Claim boundary

The maximum current claim is:

`P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW`

Explicitly not qualified:

- real P5-E end-to-end synchronization;
- continuous synchronization;
- a real 60-second SLA;
- remote-availability-to-detection SLA;
- per-transient-tip detection SLA;
- automatic evaluation;
- automatic promotion;
- automatic publication.

## Next gate

The corrected candidate must now undergo a new external adversarial review.

That review does not create authority.

Only after external re-review can human normative adjudication be considered.

## Mandatory STOP

```text
EXTERNAL_REREVIEW = NEXT

HUMAN_NORMATIVE_ADOPTION = CLOSED_PENDING_REREVIEW

REAL_P5E_EXECUTION = CLOSED

P6 = CLOSED

STOP = TRUE
```
