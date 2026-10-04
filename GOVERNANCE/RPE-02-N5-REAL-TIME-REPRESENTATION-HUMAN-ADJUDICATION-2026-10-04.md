# RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1 — HUMAN ADJUDICATION

Date: 2026-10-04

## Human decision

The human authority adopts:

`RPE-02 — N5 + REAL-TIME REPRESENTATION V0.1`

in its final qualified state after:
- initial qualification;
- independent external review;
- external-review targeted closure;
- BF-1 closure;
- NB-1, NB-2, NB-3 and NB-5 closure;
- NB-6 test-only closure;
- explicit retention of NB-4 as an RPE-05 execution guarantee.

The adopted normative state is:

`RPE02_REAL_TIME_REPRESENTATION = QUALIFIED_AND_HUMAN_ADOPTED`

After persistence and verification of this record:

`RPE-02 = CLOSED`

This adoption does not open RPE-04.

## Binding pre-adoption identity

```text
FINAL PRE-ADOPTION HEAD
= c2722291bc52b50b58a58006120b81bb4ffbeffa

RPE-02 REAL-TIME MODEL
= 31db5d944a25e54db81bd901a087cdc2039925ad

NB-6 TEST
= a2e834dbf68d50c24d53e3ef95f6a671abad8426

FINAL PRE-ADOPTION QUALIFICATION
= bb1c2b1c748879dddf6030c6cd29c94e494dc98a

FINAL PRE-ADOPTION QUALIFICATION REPORT
= 637eb0745b62cb0cf85173ecc12f2f83220944cf

FINAL EXTERNAL REVIEW RETURN
= 71886d9f3d7288f22caf2378b0b204672750348c

FINAL INTERNAL ADJUDICATION
= c0a12763b1687a9ef9afc990f16b8d8e56ed8a3b
```

Branch at adoption:

`feat/obsidian-projection-rpe02-real-time-representation-v0.1`

Pre-adoption local and remote HEAD were equal.

Pre-adoption worktree was clean.

## Final evidence accepted

```text
RPE-02 DEDICATED SURFACE
= 51 / 51 PASS

P5-E + RPE-01 + RPE-02 TARGETED REGRESSION
= 164 / 164 PASS

P5-E CONTRACT DIFF
= 0

P5-E SYNTHETIC MODEL DIFF
= 0

P5-D4 RUNTIME DIFF
= 0
```

## Adopted real-time representation

```text
NORMATIVE TIME UNIT
= INTEGER MONOTONIC NANOSECONDS
```

Qualified distinct temporal fields:

```text
schedule_origin_ns
scheduled_at_ns
attempt_started_at_ns
remote_observation_completed_at_ns
attempt_completed_at_ns
controlled_source_release_started_at_ns
```

Qualified constants:

```text
POLL INTERVAL
= 30 seconds
= 30000000000 ns

DETECTION LATENCY BOUND
= 60 seconds
= 60000000000 ns
```

## Adopted observation vocabulary and integrity

```text
READ_FAILURE
REMOTE_HEAD_OBSERVED
```

Normative coherence:

```text
REMOTE_HEAD_OBSERVED
→ observed_head MUST be lowercase 40-hex

READ_FAILURE
→ observed_head MUST be null

MALFORMED OBSERVATION
!= NORMAL SLA FAILURE

MALFORMED OBSERVATION
→ FAIL CLOSED BEFORE BUSINESS VERDICT
```

`BF-1 = CLOSED`

## Adopted eligibility semantics

```text
RELEASE ELIGIBILITY
= attempt_started_at_ns

DETECTION ELIGIBILITY
= based on attempt_started_at_ns

PRE-RELEASE TARGET HANDLING
= based on attempt_started_at_ns
```

The scheduled slot alone does not determine release eligibility.

## Adopted temporal and structural guards

The qualified behavior includes:

```text
ACTUAL START BEFORE SCHEDULED SLOT
→ BLOCKED

ACTUAL START MISSED FIXED-RATE SLOT
→ BLOCKED

REMOTE COMPLETION BEFORE ACTUAL START
→ BLOCKED

REMOTE COMPLETION AFTER NEXT FIXED-RATE SLOT
→ BLOCKED

ATTEMPT COMPLETION BEFORE REMOTE COMPLETION
→ BLOCKED

ATTEMPT OVERLAP IN QUALIFIED TIMELINE EVIDENCE
→ BLOCKED

DUPLICATE FIXED-RATE SLOT
→ BLOCKED

CADENCE GAP
→ BLOCKED

SKIPPED REQUIRED ATTEMPT
→ BLOCKED

OUT-OF-ORDER SUPPLIED OBSERVATIONS
→ BLOCKED
```

Input observation order is evidence and must not be silently sorted.

## Adopted fixed-rate grid rule

```text
(scheduled_at_ns - schedule_origin_ns)
% poll_interval_ns
= 0
```

An off-grid attempt must produce:

```text
BLOCKED_REQUIRES_ADJUDICATION

failure_code
= ATTEMPT_OFF_FIXED_RATE_GRID
```

NB-6 is adopted as:

`NB-6 = CLOSED TEST-ONLY`

The qualified test demonstrates that a shifted sequence at 15, 45, 75 and 105 seconds is blocked under a 30-second normative grid even when the target would otherwise be detected within the latency bound.

The RPE-02 implementation was not modified during this test-only closure.

## Adopted next-slot feasibility rule

```text
next_required_slot_ns
= last_valid_scheduled_slot_ns + poll_interval_ns
```

If:

```text
next_required_slot_ns
- controlled_source_release_started_at_ns
> detection_latency_bound_ns
```

then the qualified result is:

```text
FAIL_NO_DETECTION_BY_BOUND

failure_code
= NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND
```

At exact equality with the bound, the system must not conclude failure prematurely.

The result remains:

`INCOMPLETE_REAL_TIME_WINDOW`

because a future attempt can still satisfy the bound exactly.

The human authority adopts the qualified convergence with the adopted synthetic model for the covered exact-grid cases.

## Adopted finding closures

```text
BF-1
= CLOSED

NB-1
= CLOSED

NB-2
= CLOSED

NB-3
= CLOSED

NB-5
= CLOSED

NB-6
= CLOSED
```

## NB-4 — retained scope boundary

The human authority explicitly maintains:

```text
remote_observation_completed_at_ns
= SLA DETECTION ENDPOINT

attempt_completed_at_ns
= TIMELINE / OVERLAP EVIDENCE ONLY

NO REAL ATTEMPT OVERLAP
= RPE-05 EXECUTION GUARANTEE
```

RPE-02 does not claim that the future real runtime itself prevents overlapping executions.

That property remains mandatory for RPE-05 qualification.

## Stage state after verified persistence

The human decision closes RPE-02 only:

```text
RPE-01
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-02
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-03
= CLOSED
= QUALIFIED_AND_HUMAN_ADOPTED

RPE-04
= CLOSED

RPE-05
= CLOSED

RPE-06
= CLOSED

REAL P5-E
= CLOSED
```

The closure of RPE-02 and RPE-03 may make RPE-04 structurally eligible under the adopted readiness DAG, but this record does not open or authorize RPE-04.

## Explicitly not authorized

This adoption does not authorize:
- RPE-04 implementation or execution;
- RPE-05 implementation or execution;
- RPE-06 implementation or execution;
- real GitHub observation;
- real polling;
- remote fetch;
- sandbox creation;
- experimental repository/ref creation;
- experimental push;
- P5-D4 real-state mutation;
- Stage A;
- Stage B;
- promotion or publication;
- Vault mutation;
- CURRENT mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6;
- REAL P5-E.

```text
RPE-04 = CLOSED
RPE-05 = CLOSED
RPE-06 = CLOSED
REAL P5-E = CLOSED
```

## Persistence authority

The only operations authorized by the human adoption statement are:
- persist this human-adoption record;
- commit it;
- push it;
- verify final local/remote repository consistency;
- STOP.

This record persists pre-existing human authority. It does not create or enlarge that authority.

No real-time model, test, qualification, P5-E artifact, P5-D4 artifact, control state, Vault/CURRENT artifact, or future RPE artifact may be modified by this persistence step.
