# REAL P5-E — PRE-EXECUTION READINESS V0.2 — INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Base checkpoint:
`90189ac1ddddc8d81b12eeaa2a4241969a7dc405`

Branch:
`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.2-targeted-amendment`

Opening worktree:
`CLEAN`

V0.1 readiness JSON:
`9ee1e02cf371cc990097af0ae6e31317ed083a69`

V0.1 readiness report:
`5434397e87fe0f204891d230b03832c625e01368`

Adopted P5-E contract:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted P5-E synthetic model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`
## External review result

External verdict:
`FAIL`

The external review states that the general ordering is directionally correct, but two indispensable prerequisites are absent from the decomposition.

Internal adjudication:

```text
BF1 = CONFIRMED_BLOCKING
BF2 = CONFIRMED_BLOCKING

NF1 = ACCEPTED_REQUIREMENT
NF2 = ACCEPTED_REQUIREMENT
NF3 = ACCEPTED_REQUIREMENT
NF4 = ACCEPTED_REQUIREMENT
NF5 = ACCEPTED_REQUIREMENT
NF6 = ACCEPTED_REQUIREMENT
NF7 = ACCEPTED_WITH_DAG_REFINEMENT
```

This adjudication does not authorize implementation.

`REAL_P5E = CLOSED`
## BF1 — missing finite timed runner

Verdict:
`CONFIRMED_BLOCKING`

V0.1 contains:
- RPE-04 — remote observation adapter;
- RPE-05 — real experiment preregistration.

It does not contain the component that owns:
- fixed-rate scheduling;
- timer/sleep;
- actual attempt start;
- finite horizon;
- single active attempt / single-writer timing discipline;
- terminal-stop reasons;
- scheduler stop.

P5-D4 explicitly forbids time-based polling and sleep/timer in D4 and assigns near-real-time polling qualification to P5-E.

Therefore the V0.1 claim that the future real experiment would qualify runner/transport/adapter timing was structurally incomplete.

### V0.2 decision

Add:

`RPE-05 — FINITE FIXED-RATE TIMED RUNNER`

Move controlled real-experiment preregistration to:

`RPE-06`

RPE-05 must be qualified first without network using:
- injected monotonic clock;
- injected sleeper/wait primitive;
- fake observation adapter;
- deterministic terminal outcomes.

No real GitHub polling is authorized by this amendment.
## BF2 — real-time evidence representation incompatible with adopted synthetic representation

Verdict:
`CONFIRMED_BLOCKING`

Local reproduction on the adopted synthetic model confirmed:

```text
source_release_at_seconds = 1.37
→ P5ETimingModelError

scheduled=30, completed=55
→ PASS latency 54
→ no actual-start field exists

a real 60.4 second latency naively truncated to 60
→ can be misclassified as PASS
```

The adopted synthetic model is intentionally integer-second and synthetic.

It must not silently become the real-time evidence representation.

### V0.2 decision

RPE-02 becomes:

`N5 + REAL-TIME REPRESENTATION AND BOUNDARY FREEZE`

The preferred real evidence representation is integer monotonic nanoseconds, not floating-point seconds and not truncated integer seconds.

Candidate real evidence fields:

```text
schedule_origin_ns
scheduled_at_ns
attempt_started_at_ns
remote_observation_completed_at_ns
attempt_completed_at_ns
controlled_source_release_started_at_ns
```

Exact field names remain preregistration candidates until RPE-02 is opened.

The separation is normative:
- `scheduled_at_ns` = intended fixed-rate slot;
- `attempt_started_at_ns` = actual execution start;
- `remote_observation_completed_at_ns` = completion of the remote operation that produced the observed remote-ref evidence;
- `attempt_completed_at_ns` = completion of local materialization/classification/event construction.

RPE-02 must decide, test-first, whether:
1. a qualified conversion layer can preserve the adopted synthetic semantics; or
2. a separate real-time model V0.2 is required.

No choice is made by this readiness amendment beyond requiring that decision gate.
## NF1 — closed-schema hardening

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-01 must be strengthened beyond key-set equality on parsed dictionaries.

Requirements:

1. Reject duplicate JSON object member names during parsing, before dictionary construction.
2. Close every object level of each governed JSON schema, not a selected subset.
3. Enforce strict types:
   - booleans are booleans;
   - integers exclude booleans and float coercion;
   - strings are exact strings;
   - nullability is explicit.
4. Freeze list vocabularies where list entries are normative enums.
5. Enforce list uniqueness where duplicates would change or launder meaning.
6. Freeze order where order is normative, including `real_end_to_end_stages`.
7. Bind/version the schema guard itself by exact object identity.
8. Treat any change to allowed-key sets or type/vocabulary rules as a governed amendment.
9. Apply the same governed-schema discipline to future REAL P5-E JSON artifacts:
   - adapter configuration;
   - runner configuration;
   - experiment preregistration;
   - execution evidence envelopes.

RPE-01 must therefore defend against authority moving from the adopted contract into an adjacent configuration file.
## NF2 — verified Git ancestry domain

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-03 ancestry classification may return FAST_FORWARD only from a controlled local Git object domain.

Required domain conditions:

- `GIT_NO_REPLACE_OBJECTS=1`;
- no shallow repository state;
- no `.git/info/grafts`;
- both identities resolve to Git object type `commit`;
- previous head missing from the object domain → UNKNOWN;
- new head missing from the object domain → UNKNOWN;
- timeout → UNKNOWN;
- corruption → UNKNOWN;
- any Git execution error other than the defined ancestry negative result → UNKNOWN.

For:

`git merge-base --is-ancestor PREVIOUS NEW`

interpretation must be:

```text
exit 0 → FAST_FORWARD
exit 1 → NON_FAST_FORWARD
other  → UNKNOWN
```

only after both objects have independently passed commit-type/domain verification.

Rollback and divergent sibling history share the top-level class NON_FAST_FORWARD.

Optional sub-evidence may record rollback/divergence, but it must not alter D2's five-class authority surface.
## NF3 — remote observation transaction and Git environment

Verdict:
`ACCEPTED_REQUIREMENT`

V0.2 prefers one controlled `git fetch` transaction for the observed ref into an isolated namespace/object domain rather than:
`ls-remote → second independent fetch`.

Reason:
the single transaction reduces the race between the remote-ref observation and materialization of the corresponding objects.

RPE-04 must preregister the exact Git command/environment before implementation.

At minimum:

- pinned remote URL, not an inherited symbolic remote name unless that remote config itself is governed and verified;
- neutralize global/system Git configuration;
- empty/disabled hooks path;
- `GIT_TERMINAL_PROMPT=0`;
- explicit timeout;
- no inherited `url.*.insteadOf` authority;
- no user hooks;
- no canonical user worktree mutation;
- fetch into an isolated namespace/object domain.

The exact SHA evidenced by the successful controlled remote operation is the observed remote tip.

Intermediate commits learned from its history are:
`CONTENT_CONTAINED_NOT_OBSERVED`

unless independently evidenced by another successful remote observation.

If the exact advertised/observed SHA cannot be proven/materialized under the preregistered transaction semantics:
`UNKNOWN / BLOCKED`

rather than retargeting to a newer SHA.
## NF4 — experiment source contract and isolated state

Verdict:
`ACCEPTED_REQUIREMENT`

A sandbox/ref experiment is not the adopted monitored source `integration/system-v1`.

RPE-06 must therefore define a distinct experiment contract, not silently amend the adopted P5-E source identity.

Mandatory:
- experiment source identity;
- remote URL/repository identity;
- exact experiment ref;
- separate claim boundary;
- isolated experiment control root;
- no reuse/mutation of the production P5-D4 control root;
- explicit:
  `p5d4_real_state_mutation_authorized = false`.

A sandbox qualification may support:
- runner timing;
- adapter transaction semantics;
- transport path;
- evidence envelope.

It may not qualify an SLA specific to `integration/system-v1`.
## NF5 — push outcome protocol and CI side effects

Verdict:
`ACCEPTED_REQUIREMENT`

RPE-06 must freeze a push outcome matrix.

Minimum semantics:

```text
push succeeds + target observed within bound
→ VALID_PASS_CANDIDATE

push succeeds + target not observed by bound
→ SLA_FAIL_CANDIDATE

push fails + target not observed
→ INVALID_EXPERIMENT

push fails + target observed
→ INCONCLUSIVE_OR_BLOCKED
```

The exact final labels must be preregistered before execution.

Push requirements for a new experiment ref:
- explicit commit/refspec;
- no force push;
- creation-only semantics;
- use a creation guard such as an explicit empty expected lease when technically validated;
- record controlled release start before push;
- record push completion;
- preserve both timestamps as evidence.

Before any real remote push:
- audit repository workflows triggered by `push`;
- identify branch filters;
- identify any workflow capable of secret-bearing or external side effects;
- do not execute if experiment-ref push side effects are not bounded.

Preferred Pilot A:
a dedicated sandbox repository or equivalently isolated experiment surface.

A canonical ATDS branch must not be mutated solely to create a timing sample.
## NF6 — clock domain and host continuity

Verdict:
`ACCEPTED_REQUIREMENT`

For the first real pilot:

`SAME_HOST = REQUIRED`

not merely preferred.

Release recorder, timed runner, and observation adapter must use one process/host monotonic clock domain or a directly demonstrated equivalent in the same runtime environment.

RPE-02 must record actual clock capability and precision during qualification.

RPE-06 must define a fail-closed policy for:
- sleep;
- hibernation;
- host suspend/resume;
- clock-domain discontinuity or unverified continuity.

The real pilot is invalid if host continuity cannot be established for the measurement window.

No assumption about Windows sleep semantics of a particular clock source may be made without qualification evidence.
## NF7 — dependency order / governance cost

Verdict:
`ACCEPTED_WITH_DAG_REFINEMENT`

The architecture must not be represented as a false total order.

Dependency DAG:

```text
RPE-01 — N4 GOVERNED CLOSED SCHEMA
       ├──────────────→ RPE-02 — N5 + REAL-TIME REPRESENTATION
       │                         │
       └──────────────→ RPE-03 — NB5 ANCESTRY CLASSIFIER
                                 │
RPE-02 ──────────────────────────┤
                                 ↓
                       RPE-04 — NB2 + NB3
                       REAL OBSERVATION ADAPTER
                                 ↓
                       RPE-05 — FINITE TIMED RUNNER
                                 ↓
                       RPE-06 — NB9
                       CONTROLLED REAL EXPERIMENT
                       PREREGISTRATION
```

More explicitly:

```text
RPE-01 → RPE-02
RPE-01 → RPE-03
RPE-02 + RPE-03 → RPE-04
RPE-04 → RPE-05
RPE-01 + RPE-02 + RPE-03 + RPE-04 + RPE-05 → RPE-06
```

RPE-01 and RPE-02 may later share one macro-authorization for efficiency only if:
- their preregistrations remain separate;
- their RED families remain separate;
- RPE-01's schema guard is qualified before any RPE-02 governed artifact relies on it.

RPE-03 remains a separate runtime/code qualification because it introduces new executable Git-graph logic.
## RPE-05 — finite fixed-rate timed runner requirement

New blocker-closing stage.

Purpose:
provide the timing/scheduler authority explicitly delegated to P5-E but absent from V0.1.

Initial qualification environment:
`NO_NETWORK / INJECTED_CLOCK / INJECTED_SLEEP / FAKE_ADAPTER`

Required properties:

1. Fixed-rate schedule anchored to one origin, never fixed-delay drift.
2. Interval target:
   `30_000_000_000 ns`.
3. Bound target:
   `60_000_000_000 ns`.
4. Separate:
   - scheduled slot;
   - actual attempt start;
   - remote observation completion;
   - total attempt completion.
5. Exactly one active attempt.
6. No overlapping observation operation.
7. Late start is classified according to the exact RPE-02 policy.
8. Previous attempt crossing a required slot is handled according to the exact RPE-02 policy.
9. Finite maximum slots / finite terminal horizon.
10. Terminal reason causes deterministic STOP.
11. Injected adapter exception/network-equivalent failure becomes fail-closed evidence, not loop crash or implicit retry authority.
12. No queue coalescing.
13. No candidate retargeting.
14. No evaluation authority.
15. No Stage A/B authority.
16. No promotion/publication/Vault/CURRENT authority.
17. No daemon/service/startup registration authority.
18. No real P5-D4 production control-state mutation.
19. Scheduler state/evidence is isolated from production P5-D4 state.
20. Runner can be fully qualified without network using deterministic fake-clock traces.

RPE-05 does not itself authorize real polling.
## RPE-02 decision gate — conversion layer versus real-time model V0.2

The readiness amendment does not choose implementation prematurely.

RPE-02 must begin with RED cases that cannot be represented safely by the adopted integer-second synthetic model, including:

- non-integer monotonic release;
- non-integer attempt start;
- non-integer remote completion;
- latency just above 60 seconds;
- actual start delayed from scheduled slot;
- two-phase observation/classification completion.

Then compare two candidate architectures:

### Candidate A — qualified conservative conversion layer

Requirements:
- real evidence stored losslessly in integer nanoseconds;
- conversion to synthetic semantics only for parity/reference comparison;
- no conversion result may turn a real >bound measurement into PASS;
- conversion does not erase actual-start evidence;
- real runner decisions are not based on lossy synthetic conversion.

### Candidate B — separate real-time model V0.2

Requirements:
- native integer-nanosecond representation;
- explicit actual-start field;
- explicit remote-completion and attempt-completion fields;
- independently qualified parity against adopted synthetic semantics on the common exact-grid domain.

Decision criterion:

Choose the smallest architecture that can satisfy all RED cases without weakening conservative classification.

No mutation of the adopted synthetic model is implied.
## RPE-04 — controlled single-fetch observation candidate

Readiness preference:

one governed fetch transaction per attempt into an isolated Git namespace.

The future contract must answer before implementation:

- exact command form;
- how the ref's observed SHA is extracted;
- whether SHA extraction is from fetch protocol evidence, isolated fetched ref, or another exact governed surface;
- what timestamp constitutes remote observation completion;
- what timestamp constitutes full attempt completion;
- how timeout is represented;
- how zero/multiple/unexpected ref results are represented;
- how the isolated object domain is reset or retained between attempts;
- how previous observed commits remain available for ancestry checks without inheriting untrusted Git configuration.

If a two-read design is retained instead, it requires separate explicit justification and race semantics.

No choice of Git command is executable authority at this readiness stage.
## RPE-06 — controlled experiment preregistration strengthened

RPE-06 is now the final preregistration gate, not the runner qualification stage.

It requires prior qualification of RPE-01 through RPE-05.

It must define:

- experiment contract distinct from production monitored-source contract;
- sandbox repository/ref identity;
- isolated producer clone;
- isolated observer/control root;
- exact release operation;
- exact push refspec;
- creation-only guard;
- same-host monotonic clock domain;
- release-start timestamp;
- push-completion timestamp;
- scheduled attempt timeline;
- actual-start evidence;
- remote observation completion evidence;
- total attempt completion evidence;
- push outcome matrix;
- terminal experiment outcome matrix;
- sleep/hibernate invalidation;
- CI/workflow side-effect audit result;
- cleanup policy and separate cleanup authority;
- claim limits;
- STOP conditions.

RPE-06 may be human-adopted as a preregistration only.

Actual execution still requires a separate one-shot human authorization.
## Internal verdict

```text
REAL_P5E_READINESS_V0_1_EXTERNAL_REVIEW
= FAIL

BF1
= CONFIRMED_BLOCKING_AND_MAPPED_TO_NEW_RPE_05

BF2
= CONFIRMED_BLOCKING_AND_MAPPED_TO_EXTENDED_RPE_02

NF1_TO_NF6
= ACCEPTED_AS_STAGE_REQUIREMENTS

NF7
= ACCEPTED_WITH_EXPLICIT_DAG

P5E_V0_1_ADOPTED_CONTRACT
= UNCHANGED

P5E_V0_1_ADOPTED_SYNTHETIC_MODEL
= UNCHANGED

REAL_P5E
= CLOSED
```

Next authorized work under the current amendment:
- produce V0.2 machine-readable readiness map;
- produce V0.2 human report;
- produce self-contained external delta-review packet;
- commit/push;
- STOP before RPE-01.
