# REAL P5-E — PRE-EXECUTION READINESS V0.2 — HUMAN ADJUDICATION

Date: 2026-10-02

## Human decision

The human authority adopts:

`REAL P5-E — PRE-EXECUTION READINESS V0.2`

after external delta-review:

`VERDICT = PASS_WITH_NON_BLOCKING_NOTES`

with no blocking finding.

The adopted normative state is:

`REAL_P5E_PRE_EXECUTION_READINESS_V0_2 = QUALIFIED_AND_HUMAN_ADOPTED`

This adoption does not open or qualify REAL P5-E execution.
## Binding pre-adoption identity

This adoption is bound to:

```text
PRE-ADOPTION HEAD
= 878a0a6f0fbf65914dfa04b21ec0c6bdb9992d2b

READINESS V0.2 JSON
= 7708709840f2f3b4317a7968987b1a280f143b70

READINESS V0.2 REPORT
= 0ba9af17f0d62045fec4c5923cc876aedd772fb7

P5-E ADOPTED CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

P5-E ADOPTED SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac
```

Branch at adoption:

`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.
## Adopted dependency DAG

```text
RPE-01 — N4 GOVERNED CLOSED SCHEMA
       ├→ RPE-02 — N5 + REAL-TIME REPRESENTATION
       └→ RPE-03 — NB5 ANCESTRY CLASSIFIER

RPE-02 + RPE-03
       → RPE-04 — NB2 + NB3 REAL OBSERVATION ADAPTER
       → RPE-05 — FINITE FIXED-RATE TIMED RUNNER
       → RPE-06 — NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
       → separate human execution authorization
```

The DAG is adopted as the normative readiness ordering.

RPE-02 and RPE-03 may progress independently only after RPE-01.

RPE-04 requires both RPE-02 and RPE-03.

RPE-05 follows RPE-04.

RPE-06 remains the final preregistration gate before any separately authorized real experiment.
## Mandatory preregistration requirements from final external review

The non-blocking findings NF-A through NF-K are adopted as mandatory preregistration requirements.

### NF-A — local integrated rehearsal before network experiment

RPE-05 must end with a local no-network integrated rehearsal using:
- the real qualified runner;
- the real qualified adapter;
- the real qualified ancestry classifier;
- a local bare Git repository;
- the host's real clock;
- the host's real sleep/wait mechanism;
- an isolated control root.

The integrated rehearsal must exercise the production-oriented orchestration path through P5-D4 on an isolated control root.

Direct P5-D2 calls remain acceptable for unit tests, but are insufficient as the final integrated-path proof.

### NF-B — schedule origin, release phase, and sample-size claim

RPE-06 must:
- freeze `schedule_origin_ns` before source release;
- make the schedule origin independent of the release event;
- preregister the release phase relative to the polling grid;
- include a worst-case or otherwise explicitly selected phase;
- state that one real execution is a demonstration, not a general SLA qualification.

No single favorable-phase execution may be presented as proof of a worst-case 60-second SLA.
### NF-C — temporal eligibility based on actual start

RPE-02 must define attempt eligibility using:

`attempt_started_at_ns`

not merely the planned `scheduled_at_ns`.

Any rule forbidding observation before source release must also be evaluated against actual attempt start / actual evidence timing, not only against the nominal schedule.

### NF-D — remaining closed-schema vectors

RPE-01 must additionally:
- reject non-standard JSON constants such as `NaN` and `Infinity`;
- reject non-integer numeric values where integers are required, including scientific-notation values that parse as floats;
- prohibit normative authority/configuration from ungoverned environment variables;
- prohibit normative authority/configuration from ungoverned CLI arguments;
- prohibit normative authority/configuration from unlisted/unprotected files.

Runner and adapter configuration authority must come only from schema-guarded governed artifacts.

The schema guard itself remains versioned and blob-bound.
### NF-E — ancestry-classifier environment isolation

RPE-03 must additionally neutralize or fail closed on:
- `objects/info/alternates`;
- `GIT_ALTERNATE_OBJECT_DIRECTORIES`;
- inherited `GIT_DIR`;
- inherited `GIT_OBJECT_DIRECTORY`;
- other inherited `GIT_*` variables capable of changing the Git object domain or repository context;
- unverified commit-graph influence.

The classifier must disable commit-graph use, for example with `core.commitGraph=false`, unless commit-graph integrity is explicitly qualified.

The rule:

`merge-base --is-ancestor exit 1 → NON_FAST_FORWARD`

applies only after both objects and the verified domain have passed all preregistered checks.

### NF-F — remote fetch transaction details

RPE-04 must preregister:
- explicit repository URL;
- explicit refspec;
- no inherited remote fetch rules;
- `--no-tags`;
- `--no-recurse-submodules`;
- `--no-write-fetch-head`;
- `gc.auto=0`;
- exact source of the observed SHA evidence;
- initialization of the object domain before `schedule_origin_ns`;
- isolated namespace update semantics sufficient to observe NON_FAST_FORWARD transitions.

Any local refspec `+` used to update an isolated observation namespace is distinct from and does not authorize force-push to the remote.
### NF-G — runner / P5-D4 integration

The integrated RPE-05 qualification must orchestrate the P5-D4 path against an isolated control root.

This requirement exists to validate:
- persistence discipline;
- single-writer behavior;
- normalized-event handoff;
- production-path state-machine integration.

A runner that calls P5-D2 directly may be used for lower-level tests, but that alone does not qualify the integrated production-oriented path.

### NF-H — experiment contract inherits adopted semantics

RPE-06 must not create an unconstrained modified copy of the adopted P5-E contract.

The experiment contract must:
- bind by exact blob to the adopted timing/metric semantics;
- explicitly identify what is inherited unchanged;
- substitute only the experiment-specific source identity and explicitly preregistered experiment fields;
- fail closed if the inherited adopted contract identity drifts.

### NF-I — expanded push-outcome matrix

RPE-06 must also preregister:

```text
push outcome unknown because of timeout/process termination
+ target later observed
→ INCONCLUSIVE

push outcome unknown
+ target not observed
→ INVALID_EXPERIMENT

foreign/unexpected head observed on experiment ref
→ INVALID_EXPERIMENT

creation-only guard fails
→ STOP_BEFORE_RELEASE
```

Exact terminal labels may differ only if separately preregistered before execution.
### NF-J — sandbox technical safety and authority

Sandbox repository creation is not implicitly authorized.

Until separately authorized:

`sandbox_repository_creation_authorized = false`

Where technically possible, credentials used by the pilot must be scoped so that they cannot write to the canonical ATDS repository.

Before any real sandbox push, the side-effect audit must cover:
- workflow files and exact blobs;
- workflow `on:` triggers and ref filters;
- repository webhooks;
- organization webhooks relevant to the repository;
- installed GitHub Apps;
- repository/organization rulesets applicable to the experiment ref;
- any other automation capable of side effects.

### NF-K — real verdict component

RPE-02 must explicitly recognize that the real timing verdict will be produced by a new nanosecond-native component.

The adopted synthetic model remains immutable and serves as:
- semantic reference;
- parity reference on the common exact-grid domain.

No real pass/fail classification may depend on lossy conversion into the adopted integer-second synthetic model.
## Readiness interpretation after adoption

The final external review established:

```text
BLOCKING_FINDINGS = NONE

BF1
= CLOSED_AT_REQUIREMENT_LEVEL

BF2
= CLOSED_AT_REQUIREMENT_LEVEL
```

This adoption accepts the V0.2 decomposition and the NF-A→NF-K requirements.

It does not assert that any RPE stage is implemented or qualified.

Current stage state remains:

```text
RPE-01 = NOT_OPENED
RPE-02 = NOT_OPENED
RPE-03 = NOT_OPENED
RPE-04 = NOT_OPENED
RPE-05 = NOT_OPENED
RPE-06 = NOT_OPENED
```
## Explicitly not authorized

This adoption does not authorize:

- implementation of RPE-01;
- implementation of RPE-02;
- implementation of RPE-03;
- implementation of RPE-04;
- implementation of RPE-05;
- implementation of RPE-06;
- real GitHub P5-E polling;
- sandbox repository creation;
- sandbox ref creation;
- experimental push;
- real HEAD evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- real P5-D4 control-state mutation;
- daemon registration;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.

`REAL_P5E = CLOSED`

## Persistence authority

The only operation authorized by the human adoption statement is:

- persist this adjudication record;
- commit and push it;
- verify repository consistency;
- STOP.

No readiness JSON/report, adopted P5-E contract/model, runtime, control state, Vault, or CURRENT artifact may be mutated by the persistence step.
