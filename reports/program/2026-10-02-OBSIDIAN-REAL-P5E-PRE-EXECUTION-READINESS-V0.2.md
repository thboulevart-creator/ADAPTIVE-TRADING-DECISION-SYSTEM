# REAL P5-E — PRE-EXECUTION READINESS V0.2

Date: 2026-10-02

## Purpose

Amend V0.1 after external review `FAIL` without opening any implementation.

V0.2 closes the two decomposition gaps:

- BF1 — missing finite timed runner;
- BF2 — missing qualified real-time evidence representation.

It also incorporates NF1→NF7 into the appropriate readiness stages.

```text
P5-E V0.1 CONTRACT + SYNTHETIC MODEL
= QUALIFIED_AND_HUMAN_ADOPTED
= UNCHANGED

REAL P5-E
= CLOSED

RPE-01→RPE-06
= NOT OPENED
```

## Lineage

Base checkpoint:
`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`

V0.1 readiness:
```text
JSON   = 9ee1e02cf371cc990097af0ae6e31317ed083a69
REPORT = 5434397e87fe0f204891d230b03832c625e01368
```

Internal V0.2 adjudication:
`BF1/BF2 confirmed; NF1→NF7 accepted as stage requirements.`
## Corrected dependency architecture

V0.1 incorrectly behaved like a total order and omitted one runtime layer.

V0.2 uses the following DAG:

```text
                         RPE-01
                  N4 GOVERNED CLOSED SCHEMA
                       /                 \
                      /                   \
                     ↓                     ↓
             RPE-02                        RPE-03
      N5 + REAL-TIME                  NB5 ANCESTRY
       REPRESENTATION                  CLASSIFIER
                     \                   /
                      \                 /
                       ↓               ↓
                          RPE-04
                    NB2 + NB3 REAL
                   OBSERVATION ADAPTER
                             ↓
                          RPE-05
                    FINITE FIXED-RATE
                       TIMED RUNNER
                             ↓
                          RPE-06
                     NB9 CONTROLLED
                 EXPERIMENT PREREGISTRATION
                             ↓
                 SEPARATE HUMAN EXECUTION
                        AUTHORIZATION
```

Exact dependency edges:

```text
RPE-01 → RPE-02
RPE-01 → RPE-03
RPE-02 + RPE-03 → RPE-04
RPE-04 → RPE-05
RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 → RPE-06
```

RPE-02 and RPE-03 may progress independently once RPE-01 is qualified.
## RPE-01 — N4 GOVERNED CLOSED SCHEMA

### Why it comes first

Future REAL P5-E artifacts will add configuration and authority surfaces.

If the schema guard is not qualified first, authority can migrate from the adopted contract into:
- adapter config;
- runner config;
- experiment preregistration;
- evidence envelope.

### Required protection

The guard must operate on raw JSON bytes plus parsed structure.

It must reject:
- duplicate object member names before normal JSON dictionary construction;
- unknown keys at every object depth;
- wrong types;
- boolean-as-integer laundering;
- float-as-integer coercion;
- duplicate normative list values;
- unknown enum/list members;
- normative list reordering where order matters.

The guard and its schema specification must themselves be versioned and blob-bound.

A change to the allowed schema is an amendment, not an incidental edit.

### Exit criterion

`ALL_SCHEMA_AND_ADDED_KEY_BREAKERS_REJECTED_WITHOUT_COVERED_OBJECT_BINDING_AS_THE_ONLY_DEFENSE`
## RPE-02 — N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE

### BF2 correction

The adopted synthetic model is intentionally integer-second and synthetic.

It cannot safely serve as the raw real-time evidence model.

V0.2 therefore separates:

```text
synthetic adopted semantics
≠
raw real-time evidence representation
```

Preferred raw unit:
`integer monotonic nanoseconds`

Floating-point seconds are not the normative evidence format.

Lossy truncation to seconds is forbidden for pass/fail classification.

### Candidate evidence fields

```text
schedule_origin_ns
scheduled_at_ns
attempt_started_at_ns
remote_observation_completed_at_ns
attempt_completed_at_ns
controlled_source_release_started_at_ns
```

These separate:
- intended slot;
- actual start;
- remote evidence completion;
- total local attempt completion.

### Boundary decisions that must be frozen

RPE-02 must explicitly decide and test:
- release exactly on a slot;
- release immediately after a slot;
- first-slot ceiling rule;
- permitted scheduler start lag or missed-slot rule;
- completion exactly on next slot;
- completion just after next slot;
- completion equal to next attempt start;
- true overlap;
- exactly 60 seconds;
- strictly greater than 60 seconds;
- exact SHA format;
- how remote-completion and full-attempt-completion interact.

### Architecture decision

RPE-02 begins with RED cases that expose the real/synthetic mismatch.

Then choose between:

A. qualified conservative conversion layer; or
B. separate native real-time model V0.2.

The adopted synthetic model is not modified unless a separately authorized future decision explicitly says so.
## RPE-03 — NB5 QUALIFIED ANCESTRY CLASSIFIER

P5-D2 remains a deterministic consumer.

RPE-03 removes caller authority over transition classification.

### Verified object domain

Before any ancestry claim:
- no replace objects;
- no shallow state;
- no grafts;
- both SHA identities resolve to commits;
- missing objects fail to UNKNOWN;
- timeout/corruption fail to UNKNOWN.

### Classification

```text
no previous head
→ INITIAL

same head
→ SAME

merge-base --is-ancestor previous new
exit 0
→ FAST_FORWARD

exit 1 after both commits verified
→ NON_FAST_FORWARD

anything else
→ UNKNOWN
```

Rollback and sibling divergence remain one D2 class:
`NON_FAST_FORWARD`

Optional sub-evidence may distinguish them, but cannot change D2 authority semantics.
## RPE-04 — NB2 + NB3 REAL OBSERVATION ADAPTER

RPE-04 binds real remote evidence to RPE-03.

### Preferred remote observation design

One governed fetch transaction per attempt into an isolated namespace/object domain.

This is preferred over:
`ls-remote → independent fetch`

because the latter creates two remote observations and a race between them.

RPE-04 must still preregister exactly:
- the fetch command;
- the refspec;
- how the observed SHA is extracted;
- when remote observation completion is timestamped;
- when total attempt completion is timestamped;
- timeout behavior;
- zero/multiple/unexpected-ref behavior;
- namespace/object-domain lifecycle.

### Git environment isolation

Required:
- pinned URL or equivalently governed verified remote config;
- no inherited global/system config;
- hooks disabled;
- terminal prompt disabled;
- explicit timeout;
- no inherited `url.insteadOf`;
- no canonical user worktree mutation.

### Evidence semantics

Only the exact SHA produced by the successful governed remote transaction is:

`OBSERVED_REMOTE_TIP`

A commit only discovered through history/ancestry is:

`CONTENT_CONTAINED_NOT_OBSERVED`

and cannot be queued as though it had been independently observed.
## RPE-05 — FINITE FIXED-RATE TIMED RUNNER

This is the new BF1-closing stage missing from V0.1.

### Qualification environment

```text
NO NETWORK
INJECTED CLOCK
INJECTED SLEEP
FAKE ADAPTER
```

The runner must be fully qualifiable without GitHub.

### Responsibilities

The runner owns only:
- fixed-rate scheduling;
- finite horizon;
- actual attempt start;
- wait/sleep;
- exactly one active attempt;
- terminal stop.

It consumes RPE-02 timing semantics and the RPE-04 adapter interface.

It must prove:
- 30-second anchored fixed-rate schedule;
- no fixed-delay drift;
- separate scheduled and actual start;
- separate remote and total completion;
- single active attempt;
- no overlap;
- exact late-start/overrun policy from RPE-02;
- deterministic terminal reason;
- deterministic STOP;
- finite maximum horizon;
- fail-closed adapter failure;
- no implicit retry beyond schedule.

It must not gain:
- evaluation;
- Stage A/B;
- promotion;
- publication;
- Vault/CURRENT mutation;
- queue coalescing;
- retargeting;
- daemon/service/startup authority.

### Exit criterion

`FINITE_FIXED_RATE_RUNNER_IS_DETERMINISTIC_FAIL_CLOSED_AND_QUALIFIED_WITHOUT_NETWORK`
## RPE-06 — NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION

RPE-06 happens only after RPE-01→RPE-05 are qualified.

It remains a preregistration, not execution.

### Experiment contract

A sandbox experiment uses a different source from the adopted production source.

Therefore it requires an explicit experiment contract.

It must define:
- exact repository URL;
- exact experiment ref;
- isolated producer clone;
- isolated observer/control root;
- claim boundary;
- `p5d4_real_state_mutation_authorized = false`.

### Clock domain

For Pilot A:
`SAME HOST = REQUIRED`

Release recorder, runner and adapter must share one qualified monotonic clock domain.

The pilot must invalidate itself if sleep/hibernation/suspend continuity is not proven.

Current local observation only:
Python reports `monotonic` as `QueryPerformanceCounter()`, monotonic, non-adjustable, reported resolution `1e-7 s`.

That observation is not qualification and must be captured again during the actual RPE-02/RPE-06 qualification environment.

### Push protocol

Record:
- target commit before release;
- release-start monotonic time immediately before push;
- push completion;
- explicit refspec;
- creation-only guard;
- no force push.

Minimum experiment classification:

```text
push success + observed within bound
→ VALID_PASS_CANDIDATE

push success + not observed by bound
→ SLA_FAIL_CANDIDATE

push failure + not observed
→ INVALID_EXPERIMENT

push failure + target nevertheless observed
→ INCONCLUSIVE_OR_BLOCKED
```

Exact labels remain to be frozen in the preregistration.

### Side-effect audit

Before push, inspect:
- workflows triggered by push;
- branch/ref filters;
- secret-bearing automation;
- external side effects.

Do not run a pilot whose side effects are not bounded.

Preferred first surface:
a dedicated sandbox repository or equivalently isolated experiment surface.

Sandbox success does not qualify `integration/system-v1`-specific SLA.
## Production-source gate after sandbox

A later observation against `integration/system-v1` requires:

- separate human authorization;
- a legitimate governed update, not a dummy measurement commit;
- target commit known before push;
- explicit adjudication of real P5-D4 pending state and queue capacity;
- production-specific evidence;
- no inference that sandbox latency automatically equals production-branch latency.

## Governance efficiency

RPE-01 and RPE-02 may share a future macro-authorization only if:
- preregistrations remain separate;
- RED families remain separate;
- RPE-01 is qualified before RPE-02 artifacts rely on its schema authority.

RPE-03 remains a separate code/runtime qualification.

## V0.2 readiness verdict

```text
BF1 = MAPPED_TO_RPE_05
BF2 = MAPPED_TO_RPE_02

NF1 = INTEGRATED_RPE_01
NF2 = INTEGRATED_RPE_03
NF3 = INTEGRATED_RPE_04
NF4 = INTEGRATED_RPE_06
NF5 = INTEGRATED_RPE_06
NF6 = INTEGRATED_RPE_02_AND_RPE_06
NF7 = INTEGRATED_AS_DAG

RPE-01 = NOT OPENED
RPE-02 = NOT OPENED
RPE-03 = NOT OPENED
RPE-04 = NOT OPENED
RPE-05 = NOT OPENED
RPE-06 = NOT OPENED

REAL_P5E = CLOSED
P6 = CLOSED
```

Next gate:
external delta-review of this V0.2 readiness amendment.

No implementation may begin before that review is adjudicated.
