# REAL P5-E — PRE-EXECUTION READINESS V0.1

Date: 2026-10-02

## Purpose

Transform the six retained prerequisites:

`N4 / N5 / NB2 / NB3 / NB5 / NB9`

into an executable closure order before any REAL P5-E preregistration or network execution.

This stage is requirements/readiness only.

```text
REAL P5-E = CLOSED
REAL HEAD EVALUATION = CLOSED
VAULT / CURRENT MUTATION = CLOSED
P6 = CLOSED
```

## Opening identity

Branch:
`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.1`

Opening HEAD:
`15047e3e60a7973b341bbb05b859cfa26ef71f3f`

Adopted P5-E human adjudication blob:
`76defeedea7ca7cff6af40534e479e7bc2bdd95a`

Adopted contract blob:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted synthetic model blob:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
## Executive blocker map

The six prerequisites should not be implemented as six unrelated workstreams.

Recommended dependency chain:

```text
RPE-01 — N4 CLOSED SCHEMA
        ↓
RPE-02 — N5 TIMING BOUNDARIES
        ↓
RPE-03 — NB5 ANCESTRY CLASSIFIER
        ↓
RPE-04 — NB2 + NB3 REAL OBSERVATION ADAPTER
        ↓
RPE-05 — NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
        ↓
SEPARATE HUMAN AUTHORIZATION
        ↓
ONE FINITE REAL EXPERIMENT
```

This order minimizes rework because each later layer consumes the semantics frozen by the previous layer.

## VERIFIED — N4

Current P5-E invariant checks validate expected values but do not enforce a closed schema.

Read-only mutation probes confirmed that the following added keys survive current semantic invariants:

```text
authority_boundary.pending_head_evaluation_override = true
claim_boundary.additional_current_claims = ["P5E_REAL_END_TO_END_QUALIFIED"]
near_real_time_timing.poll_interval_seconds_override = 300
queue_and_supersession.coalescing_authorized_v0_2 = true
```

Therefore:

`N4 = OPEN_CONFIRMED`

The current blob binding detects byte drift, but it does not independently prevent a future amendment from intentionally rebinding a contract containing an unexpected authority key.

### Recommended closure

Do not rewrite the adopted contract merely to add schema metadata.

Prefer a separate closed-schema guard/verifier that:
- pins exact top-level and nested key sets;
- rejects unknown keys independently of blob binding;
- rejects unknown authority/claim enum members;
- rejects duplicates where list semantics require uniqueness.

Exit criterion:

`ADDED_KEY_BREAKERS = 0 survivors without relying on object-binding tests`
## VERIFIED — N5

The synthetic model currently behaves coherently, but the equality and rounding semantics are not fully frozen by dedicated contract language/tests.

Read-only probes of the adopted model produced:

```text
release exactly at 30 → slot 30 eligible → PASS latency 0
release exactly at 60 → slot 60 eligible → PASS latency 0
release at 31 → first required slot 60 → PASS latency 29

attempt 30 completing at 60 → allowed
previous completion 60 and next attempt start 60 → allowed / not overlap
attempt 30 completing at 61 → BLOCKED ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT

uppercase SHA → rejected
```

The current algorithm also uses:
- ceiling-to-grid for non-aligned release;
- `latency <= 60` as within bound;
- `previous_completed > next_scheduled` as overlap;
- `completed > scheduled + interval` as overrun.

Therefore:

`N5 = OPEN_BEHAVIOR_EXISTS_NOT_FULLY_NORMATIVELY_FROZEN`

### Recommended closure

Create a timing-boundary contract and dedicated tests around the unchanged adopted model first.

Freeze explicitly:
- equality at a poll slot;
- non-aligned release rounding;
- completion exactly on the next slot;
- completion one unit after;
- overlap equality versus strict exceedance;
- latency exactly 60 versus >60;
- lower-case exact SHA format.

Only change the model if the new tests expose an actual inconsistency.
## VERIFIED — NB5

P5-D2 is a deterministic consumer of a normalized event.

Its input requires an explicit:

`transition_class`

but P5-D2 does not prove that class against the Git graph.

A read-only probe demonstrated that an A→B→A sequence can be supplied with the second A mislabeled `FAST_FORWARD`; P5-D2 accepts the caller-provided class because classification is outside its authority.

Repository search found no qualified ancestry classifier under:

`tools/obsidian_projection`

A one-off `git merge-base --is-ancestor` use elsewhere in the repository does not constitute a qualified P5-E component.

Therefore:

`NB5 = OPEN_CONFIRMED`

### Recommended closure

Create a standalone ancestry classifier with no network access.

Inputs:
- previous observed head or null;
- new exact observed head;
- verified local Git object domain.

Outputs:
- INITIAL;
- SAME;
- FAST_FORWARD;
- NON_FAST_FORWARD;
- UNKNOWN.

Rules:
- no previous → INITIAL;
- same SHA → SAME;
- previous is ancestor of new → FAST_FORWARD;
- both commits verified but previous is not ancestor of new → NON_FAST_FORWARD;
- missing object, non-commit object, Git error, or unprovable relation → UNKNOWN.

Qualify against a temporary local Git graph containing fast-forward, rollback, divergence, same, initial, missing-object, and non-commit cases.
## VERIFIED — NB2 + NB3

P5-D4 already exposes an injected `observation_adapter` boundary.

Its contract already establishes:
- remote I/O occurs outside P5-D2;
- real remote observation may use read-only Git;
- timing/sleep are not P5-D4 authority and belong to P5-E.

There is also a prior real-execution pattern that validates exactly:

`git ls-remote --heads origin refs/heads/integration/system-v1`

against an expected HEAD.

That pattern is useful evidence for exact remote-ref parsing, but it is not a P5-E observation adapter.

The adopted P5-E helper:

`classify_tip_visibility(..., fast_forward_contains_target=bool)`

is intentionally insufficient for real authority because containment is supplied by the caller.

Observed probe:

```text
caller supplies containment=true
→ CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED

caller supplies containment=false
→ UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION
```

Therefore:

`NB2 + NB3 = OPEN_CONFIRMED_AND_COUPLED`

### Recommended closure

Build one real-observation adapter only after NB5 is qualified.

Initial qualification should use a local bare Git remote or injected network fixture, not GitHub polling.

The adapter must:
1. read one exact configured remote ref;
2. validate the returned exact ref and lower-case 40-hex SHA;
3. record attempt start/completion monotonic timestamps outside P5-D2 state;
4. emit REMOTE_OBSERVATION_FAILED on read/network failure;
5. classify SAME directly;
6. for a changed SHA, prove/materialize the exact observed commit in isolated control storage;
7. invoke only the qualified ancestry classifier;
8. emit a normalized P5-D2 event with independently derived transition class;
9. treat only the SHA returned by the successful remote read as an observed remote tip;
10. never queue ancestry-enumerated intermediate commits unless independently observed.

NB2 should be resolved without guessing motive.

The system does not need to decide whether a B→A observation was caused by lag, rollback, or a third-party push. It needs only to prove the Git graph relation:
- descendant → FAST_FORWARD;
- verified not-descendant → NON_FAST_FORWARD;
- unprovable → UNKNOWN.

NB3 is closed when exact tip observation and content containment become distinct runtime evidence classes rather than caller assertions.
## VERIFIED — NB9

The adopted timing metric requires:

```text
CONTROLLED_SOURCE_RELEASE_MONOTONIC
→
SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC
```

No current P5-E runtime records that real protocol.

Search confirms that other Obsidian tools use `time.monotonic()`, but those uses do not qualify P5-E timing.

No REAL P5-E adapter/scheduler exists yet.

Therefore:

`NB9 = OPEN_CONFIRMED`

### Recommended safest real-experiment protocol

Do not begin by mutating `integration/system-v1` solely for measurement.

First qualify one finite experiment on a dedicated experimental remote ref.

Candidate rules:

- precompute the target commit before release;
- isolated producer clone;
- force=false;
- one explicit human push authorization;
- capture the release monotonic timestamp immediately before starting the authorized push;
- observer and release recorder share the same host/monotonic clock domain;
- fixed-rate 30-second attempts;
- record start and completion separately;
- bound = 60 seconds;
- no evaluation, promotion, publication, Vault/CURRENT mutation;
- no daemon/service/startup registration;
- no implicit remote-ref deletion authority.

This first experiment can qualify the real runner/transport/adapter timing path, but it must not overclaim branch-specific production behavior for `integration/system-v1`.

A later production-ref claim should use a separately authorized legitimate governed update whose target commit is known before push. Do not create a meaningless canonical commit solely to satisfy a measurement.
## Reuse versus new construction

### Reuse

```text
P5-A
→ source identity
→ read-only Git intent
→ isolated checkout principle
→ candidate 30s / 60s target

P5-D1 / P5-D2
→ deterministic state machine
→ normalized event schema
→ fail-closed NON_FAST_FORWARD / UNKNOWN

P5-D4
→ bounded orchestration
→ injected observation adapter boundary
→ single-writer / persistent state discipline

P5-D3F real runner pattern
→ exact ls-remote ref validation pattern

FrozenGitSource
→ exact frozen commit/tree/blob reads after identity is already frozen
```

### New construction required

```text
RPE-01 closed-schema guard
RPE-02 timing-boundary freeze
RPE-03 qualified ancestry classifier
RPE-04 qualified real observation adapter
RPE-05 controlled real experiment preregistration
```

No existing component should be relabeled to pretend those five surfaces are already qualified.
## Recommended implementation sequence

### RPE-01 — CLOSED SCHEMA GUARD

Scope:
`N4 only`

Mode:
`CONTRACT_FIRST / TEST_FIRST / NO_RUNTIME_COUPLING`

STOP after qualification.

### RPE-02 — TIMING BOUNDARY FREEZE

Scope:
`N5 only`

Prefer tests/contract around unchanged model.

STOP after qualification.

### RPE-03 — ANCESTRY CLASSIFIER

Scope:
`NB5 only`

Use local finite Git fixtures.

No network.

STOP after qualification.

### RPE-04 — REAL OBSERVATION ADAPTER

Scope:
`NB2 + NB3`

First qualify against local bare remote/injected I/O.

No real GitHub polling.

STOP after qualification.

### RPE-05 — CONTROLLED REAL EXPERIMENT PREREGISTRATION

Scope:
`NB9 only`

Define exact release/ref/clock/schedule/stop protocol.

STOP before execution.

### Final execution gate

Only after RPE-01→RPE-05 are closed:

`ONE FINITE REAL P5-E EXPERIMENT`

requires a new explicit human authorization.

## Current verdict

```text
P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED_AND_HUMAN_ADOPTED

REAL_P5E_PRE_EXECUTION_READINESS_MAP
= PRODUCED_CANDIDATE

RPE-01 = NOT_OPENED
RPE-02 = NOT_OPENED
RPE-03 = NOT_OPENED
RPE-04 = NOT_OPENED
RPE-05 = NOT_OPENED

REAL_P5E = CLOSED
P6 = CLOSED
```

The next decision should be review/adoption of this readiness ordering, not real execution.
