# REAL P5-E — PRE-EXECUTION READINESS V0.1 — SELF-CONTAINED EXTERNAL REVIEW PACKET

Date: 2026-10-02

## Independent reviewer mandate

Review the proposed prerequisite architecture for opening REAL P5-E.

Current adopted state:

`P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL = QUALIFIED_AND_HUMAN_ADOPTED`

Current real state:

`REAL_P5E = CLOSED`

This packet does NOT ask you to review or authorize a real execution.

It asks whether the proposed readiness decomposition correctly closes all retained prerequisites before any real preregistration or network experiment.

## Candidate readiness identity

Repository:
`thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`

Readiness branch:
`feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.1`

Readiness HEAD:
`2c74b64c7e05b08103a2974ae918753526b1e354`

Readiness JSON blob:
`9ee1e02cf371cc990097af0ae6e31317ed083a69`

Readiness report blob:
`5434397e87fe0f204891d230b03832c625e01368`

Adopted P5-E contract:
`43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9`

Adopted synthetic timing model:
`c0f16baa151c1466e30ba5778f1fca8184cd4aac`

## Proposed dependency chain

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

## Mandatory review questions

### N4 / RPE-01

1. Is closed-schema hardening truly required before later amendments?
2. Is a separate schema guard preferable to mutating the already adopted P5-E contract?
3. Which nested blocks must be closed to prevent authority/claim/timing/queue expansion?
4. Are exact-key checks sufficient, or must list enums/duplicates and type constraints also be frozen?
5. Can you construct an added-key attack not covered by the proposed N4 closure?

### N5 / RPE-02

6. Are the currently observed equality/rounding semantics coherent?
7. Is release exactly on a scheduled slot correctly treated as eligible?
8. Is completion exactly at the next slot correctly non-overrun?
9. Is previous completion equal to next attempt start correctly non-overlap?
10. Is `latency <= 60` the correct boundary under the adopted contract?
11. What other edge cases must be frozen before a real scheduler consumes these semantics?
12. Can N5 be closed around the unchanged adopted model, or is a model change required?

### NB5 / RPE-03

13. Is the proposed ancestry classifier complete and fail-closed?
14. Is `previous verified commit is not ancestor of new verified commit → NON_FAST_FORWARD` appropriate for both rollback and divergent history?
15. Which failures must map to UNKNOWN rather than NON_FAST_FORWARD?
16. Should the classifier be network-free and operate only on a verified local object domain?
17. Is any already-qualified repository component sufficient to reuse directly instead of creating this classifier?

### NB2 + NB3 / RPE-04

18. Does one observation adapter correctly couple the two findings?
19. Is exact successful remote-read SHA the only thing that may be called an observed remote tip?
20. Must ancestry-enumerated intermediate commits remain CONTENT_CONTAINED_NOT_OBSERVED?
21. How should the adapter handle a race where the remote advances between ls-remote and exact commit materialization?
22. Is fail-closed UNKNOWN the correct result when the exact observed SHA cannot be materialized/proven?
23. Does the adapter architecture preserve P5-D2 as a deterministic normalized-event consumer?
24. Does any proposed behavior silently introduce queue coalescing, retargeting, evaluation, or promotion authority?

### NB9 / RPE-05

25. Is a dedicated experimental remote ref the safest first real experiment?
26. Does that experiment legitimately qualify runner/transport/adapter timing while explicitly not qualifying production-branch-specific SLA?
27. Is recording `CONTROLLED_SOURCE_RELEASE_MONOTONIC` immediately before starting the explicitly authorized push a conservative, falsifiable origin?
28. Would another release point be better without relying on inaccessible server time?
29. Must the release recorder and observer share one host/monotonic clock domain?
30. What exact conditions are required before any experiment against `integration/system-v1`?
31. Is it correct to forbid creating a meaningless canonical commit solely for timing measurement?

### Architecture / order

32. Is RPE-01→RPE-05 the correct dependency order?
33. Can any stages safely be combined without weakening test-first isolation?
34. Is any prerequisite missing between RPE-04 and real execution?
35. Are there hidden authority leaks in the proposed plan?
36. Does the plan preserve the adopted contract/model identity unnecessarily rigidly, or appropriately?

## Required adversarial checks

Try to falsify at least:

- unknown authority key added and then contract blob intentionally rebound;
- timing equality at exactly 30/60;
- release just after a poll;
- read completing exactly at and just after next slot;
- rollback B→A;
- divergent B/C histories;
- missing new commit object;
- remote advances after ls-remote before fetch/materialization;
- remote returns malformed/multiple/unexpected refs;
- contained intermediate commit mistaken for observed tip;
- repeated same head;
- network failure;
- cross-host clock mismatch;
- push failure after release timestamp;
- experiment branch vs production branch claim laundering;
- canonical worktree mutation;
- implicit force push;
- hidden evaluation/promotion/Vault/P6 authority.

## Required output

Return exactly one:

`VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL`

Then provide:

- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- N4_CHECK
- N5_CHECK
- NB5_CHECK
- NB2_NB3_CHECK
- NB9_CHECK
- DEPENDENCY_ORDER_CHECK
- MISSING_PREREQUISITES
- AUTHORITY_LEAKAGE_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_NEXT_ACTION

For each finding:
- identify the exact packet section / field / function involved;
- distinguish OBSERVED from INFERENCE;
- state BLOCKING or NON_BLOCKING;
- give a minimal falsification case where possible.

This review creates no authority.

`REAL_P5E = CLOSED`

---

# SOURCE: READINESS JSON
Path: tools/obsidian_projection/real_p5e_pre_execution_readiness_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_REAL_P5E_PRE_EXECUTION_READINESS_V0_1",
  "status": "CANDIDATE_REQUIREMENT_EXTRACTION_AND_BLOCKER_MAP",
  "date": "2026-10-02",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-real-p5e-pre-execution-readiness-v0.1",
  "opening_head": "15047e3e60a7973b341bbb05b859cfa26ef71f3f",
  "authority": {
    "purpose": "Map and order the prerequisites that must close before any REAL P5-E preregistration or execution.",
    "requirements_only": true,
    "runtime_modification_authorized": false,
    "real_remote_polling_authorized": false,
    "real_head_evaluation_authorized": false,
    "vault_or_current_mutation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "daemon_or_service_registration_authorized": false,
    "p6_authorized": false
  },
  "adopted_predecessor": {
    "human_adjudication_blob": "76defeedea7ca7cff6af40534e479e7bc2bdd95a",
    "contract_blob": "43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9",
    "synthetic_model_blob": "c0f16baa151c1466e30ba5778f1fca8184cd4aac",
    "state": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED_AND_HUMAN_ADOPTED",
    "real_p5e": "CLOSED"
  },
  "reusable_qualified_or_observed_surfaces": {
    "p5a_continuous_projection_contract": {
      "blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
      "use": "remote source identity, read-only remote observation intent, 30s candidate poll / 60s target, isolated control checkout principle"
    },
    "p5d1_observer_core_contract": {
      "blob": "a20999ae991e07447e25ecd1592964f2d333449b",
      "use": "explicit transition classes and fail-closed NON_FAST_FORWARD/UNKNOWN semantics"
    },
    "p5d2_observer_tick": {
      "blob": "fd212f61ec38332b677110f40265638af55a73e2",
      "use": "deterministic normalized-event consumer; transition_class is caller supplied and is not independently proven"
    },
    "p5d4_bounded_loop_contract": {
      "blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
      "use": "injected observation_adapter boundary; real read-only Git permitted; timing/sleep explicitly deferred to P5-E"
    },
    "p5d4_bounded_loop_runtime": {
      "blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
      "use": "bounded orchestration only; no time scheduler; no real P5-E authority"
    },
    "p5d3f_real_remote_ref_pattern": {
      "blob": "9228ea75d269c9bfc89537374dec5990498c3e4a",
      "use": "existing proof pattern for exact git ls-remote --heads origin refs/heads/integration/system-v1 identity validation; not a qualified P5-E observation adapter"
    },
    "frozen_git_source": {
      "blob": "aef3a232980fa6ceb5253d38616419e41182162a",
      "use": "read-only access to an already frozen exact commit/tree/blob domain; not remote-ref observation or ancestry classification"
    }
  },
  "blockers": {
    "N4": {
      "title": "CLOSED_SCHEMA_AND_ADDED_KEY_HARDENING",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "A future amendment can add a new authority/claim/timing/queue key and rebind object identity while existing semantic guards do not reject the new key.",
      "observed_evidence": [
        "authority_boundary.pending_head_evaluation_override=true survives current assert_contract_invariants",
        "claim_boundary.additional_current_claims=[P5E_REAL_END_TO_END_QUALIFIED] survives",
        "near_real_time_timing.poll_interval_seconds_override=300 survives",
        "queue_and_supersession.coalescing_authorized_v0_2=true survives"
      ],
      "recommended_closure": {
        "preserve_adopted_contract_bytes_if_possible": true,
        "artifact": "P5E_V0_1_CLOSED_SCHEMA_GUARD",
        "requirements": [
          "exact top-level key set",
          "exact key sets for every nested object used by current or future authority/claim/timing/queue logic",
          "unexpected keys fail closed independent of covered-object blob binding",
          "authority and claim lists reject duplicates and unknown enum members where applicable",
          "added-key adversarial sweep"
        ],
        "exit_criterion": "ALL_PREREGISTERED_ADDED_KEY_BREAKERS_REJECTED_WITH_OBJECT_BINDING_TESTS_EXCLUDED"
      },
      "dependencies": []
    },
    "N5": {
      "title": "EXACT_TIMING_AND_IDENTITY_BOUNDARY_FREEZE",
      "status": "OPEN_BEHAVIOR_EXISTS_NOT_FULLY_NORMATIVELY_FROZEN",
      "observed_current_behavior": {
        "source_release_exactly_on_slot_is_eligible": true,
        "source_release_non_aligned_31_first_required_slot": 60,
        "completion_exactly_on_next_slot_is_allowed": true,
        "previous_completion_equal_to_next_attempt_start_is_not_overlap": true,
        "completion_after_next_slot_is_blocked": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
        "latency_equal_to_bound_is_eligible_for_pass": true,
        "uppercase_sha_is_rejected": true,
        "read_completion_before_attempt_start_is_blocked": true
      },
      "failure_mode": "Off-by-one or rounding changes can alter real SLA classification without changing the high-level 30s/60s contract.",
      "recommended_closure": {
        "preserve_synthetic_model_bytes_unless_a_test_exposes_inconsistency": true,
        "artifact": "REAL_P5E_TIMING_BOUNDARY_CONTRACT_V0_1",
        "tests_required": [
          "release exactly at 30 and 60",
          "release immediately after a slot / non-aligned release ceiling rule",
          "completion exactly at next fixed-rate slot",
          "completion one unit after next fixed-rate slot",
          "previous read completion exactly equals next attempt start",
          "previous read completion exceeds next attempt start",
          "latency exactly 60 versus greater than 60",
          "first required slot rounding",
          "lowercase exact SHA accepted and uppercase/malformed SHA rejected"
        ],
        "exit_criterion": "ALL_EQUALITY_AND_ROUNDING_BOUNDARIES_HAVE_EXPLICIT_CONTRACT_RULE_AND_EXECUTABLE_TEST"
      },
      "dependencies": ["N4"]
    },
    "NB5": {
      "title": "QUALIFIED_ANCESTRY_CLASSIFIER",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "P5-D2 trusts caller-supplied INITIAL/SAME/FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN and cannot prove whether that classification matches the Git graph.",
      "observed_evidence": [
        "Aâ†’Bâ†’A can be supplied to P5-D2 with the second A mislabeled FAST_FORWARD; P5-D2 accepts the class because classification is outside its authority.",
        "No qualified ancestry classifier exists under tools/obsidian_projection.",
        "A one-off merge-base use elsewhere in the repository is not qualified as an Obsidian P5-E component."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_ANCESTRY_CLASSIFIER_V0_1",
        "network_inside_classifier_forbidden": true,
        "input": [
          "previous_observed_head_or_null",
          "new_exact_observed_head",
          "verified_local_git_object_domain"
        ],
        "output": [
          "INITIAL",
          "SAME",
          "FAST_FORWARD",
          "NON_FAST_FORWARD",
          "UNKNOWN"
        ],
        "classification_rules": {
          "no_previous_head": "INITIAL",
          "same_head": "SAME",
          "previous_is_ancestor_of_new": "FAST_FORWARD",
          "both_commits_verified_but_previous_is_not_ancestor_of_new": "NON_FAST_FORWARD",
          "missing_object_invalid_type_git_error_or_unprovable_relation": "UNKNOWN"
        },
        "local_fixture_cases": [
          "Aâ†’B fast-forward",
          "Bâ†’A rollback",
          "B and C divergent siblings",
          "same Aâ†’A",
          "initial nullâ†’A",
          "missing/unreadable commit object",
          "non-commit object"
        ],
        "exit_criterion": "CLASSIFICATION_IS_DERIVED_FROM_VERIFIED_GIT_GRAPH_AND_CANNOT_BE_CALLER_FORGED"
      },
      "dependencies": ["N4"]
    },
    "NB2_NB3": {
      "title": "REAL_REMOTE_OBSERVATION_ADAPTER_AND_TIP_VISIBILITY",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "A real remote observation is not yet converted into a normalized P5-D2 event with independently proven ancestry; intermediate contained commits can otherwise be confused with actually observed remote tips.",
      "observed_evidence": [
        "P5-D4 already exposes an injected observation_adapter boundary and permits read-only Git outside P5-D2.",
        "P5-D3F contains an exact ls-remote ref validation pattern but does not emit P5-D2 events or classify ancestry.",
        "P5-E classify_tip_visibility is stateless and trusts caller-supplied fast_forward_contains_target."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_REMOTE_OBSERVATION_ADAPTER_V0_1",
        "initial_qualification_environment": "LOCAL_BARE_REMOTE_OR_SYNTHETIC_NETWORK_ADAPTER_NO_REAL_GITHUB_POLLING",
        "requirements": [
          "read exactly one configured remote ref and validate exact ref plus lowercase 40-hex head",
          "record attempt-start and read-completion monotonic timestamps outside deterministic P5-D2 state",
          "network/read failure emits REMOTE_OBSERVATION_FAILED and cannot create a CURRENT claim",
          "same exact head emits SAME",
          "new exact observed head must be materialized/proven in isolated control Git object storage before ancestry classification",
          "invoke only the qualified NB5 ancestry classifier",
          "emit normalized P5-D2 REMOTE_HEAD_OBSERVED event with independently derived transition_class",
          "only the SHA returned by the successful remote read is an observed remote tip",
          "intermediate commits discovered by ancestry/history enumeration are CONTENT_CONTAINED_NOT_OBSERVED and must not be injected into the queue unless independently observed on a successful remote read",
          "exact-fetch/materialization race or inability to prove the observed SHA results in UNKNOWN/BLOCKED rather than retargeting to a newer head",
          "no canonical worktree mutation, no Vault mutation, no evaluation/promotion authority"
        ],
        "NB2_resolution_semantics": "Do not infer motive such as lag, rollback, or third-party push. Classify only the observed sequence and provable Git graph relation. A later observed head that is not a descendant of the previous observed head is NON_FAST_FORWARD; unprovable relation is UNKNOWN.",
        "NB3_resolution_semantics": "Observation and containment are distinct evidence classes. Containment never becomes exact tip observation.",
        "exit_criterion": "ADAPTER_OUTPUT_IS_EXACT_REMOTE_EVIDENCE_PLUS_QUALIFIED_ANCESTRY_WITH_NO_CALLER_SUPPLIED_CONTAINMENT_OR_TRANSITION_AUTHORITY"
      },
      "dependencies": ["NB5", "N5"]
    },
    "NB9": {
      "title": "CONTROLLED_REAL_EXPERIMENT_PROTOCOL",
      "status": "OPEN_CONFIRMED",
      "failure_mode": "There is no preregistered real protocol binding source release, observer schedule, clock domain, target ref, push authority, and read completion into one falsifiable real experiment.",
      "observed_evidence": [
        "P5-E adopted metric requires CONTROLLED_SOURCE_RELEASE_MONOTONIC â†’ SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC.",
        "No REAL P5-E observation adapter currently records that protocol.",
        "Existing time.monotonic uses elsewhere in Obsidian tooling do not qualify this P5-E experiment.",
        "Current authority forbids silent mutation of integration/system-v1."
      ],
      "recommended_closure": {
        "artifact": "REAL_P5E_CONTROLLED_EXPERIMENT_PREREGISTRATION_V0_1",
        "same_clock_domain_required": true,
        "same_host_preferred": true,
        "fixed_rate_schedule": {
          "interval_seconds": 30,
          "bound_seconds": 60,
          "attempt_start_and_completion_recorded_separately": true
        },
        "source_release_definition_candidate": "MONOTONIC_TIMESTAMP_CAPTURED_IMMEDIATELY_BEFORE_STARTING_THE_EXPLICITLY_AUTHORIZED_PUSH_OF_A_PRECOMPUTED_TARGET_COMMIT",
        "reason_for_release_definition": "Conservative and locally falsifiable; includes push transport time and cannot detect the target before the recorded release point without exposing an inconsistency.",
        "safest_first_real_experiment": {
          "remote_ref": "DEDICATED_EXPERIMENT_REF_NOT_INTEGRATION_SYSTEM_V1",
          "force_push_forbidden": true,
          "one_explicit_push_authorization_required": true,
          "target_commit_precomputed_before_release": true,
          "producer_clone_isolated_from_canonical_user_worktree": true,
          "remote_ref_deletion_not_implicitly_authorized": true,
          "claim_limit": "Qualifies runner/transport/adapter timing on the GitHub remote path but does not by itself qualify branch-specific production behavior for integration/system-v1."
        },
        "production_ref_gate_after_safe_experiment": {
          "integration_system_v1_mutation_may_not_be_created_only_for_measurement": true,
          "preferred_source_event": "A separately authorized legitimate governed update whose target commit is known before push.",
          "separate_human_authorization_required": true,
          "production_ref_sla_claim_requires_its_own_evidence": true
        },
        "forbidden": [
          "silent push to integration/system-v1",
          "force push",
          "using GitHub/server wall-clock as the normative measurement origin",
          "cross-host clocks without proven common monotonic domain",
          "real Vault/CURRENT mutation",
          "evaluation, promotion, publication",
          "daemon/startup/service registration"
        ],
        "exit_criterion": "A SELF_CONTAINED_PREREGISTRATION EXISTS_FOR_ONE_FINITE_REAL_EXPERIMENT_WITH_EXACT_REF_RELEASE_CLOCK_SCHEDULE_ADAPTER_AND_STOP_CONDITIONS"
      },
      "dependencies": ["N4", "N5", "NB5", "NB2_NB3"]
    }
  },
  "recommended_sequence": [
    {
      "id": "RPE-01",
      "closes": ["N4"],
      "name": "CLOSED_SCHEMA_GUARD",
      "reason": "Prevent future prerequisite amendments from creating new unguarded authority keys."
    },
    {
      "id": "RPE-02",
      "closes": ["N5"],
      "name": "TIMING_BOUNDARY_FREEZE",
      "reason": "Freeze exact equality/rounding semantics before any real scheduler or adapter consumes them."
    },
    {
      "id": "RPE-03",
      "closes": ["NB5"],
      "name": "ANCESTRY_CLASSIFIER",
      "reason": "Remove caller authority over FAST_FORWARD/NON_FAST_FORWARD/UNKNOWN before building the real adapter."
    },
    {
      "id": "RPE-04",
      "closes": ["NB2", "NB3"],
      "name": "REMOTE_OBSERVATION_ADAPTER",
      "reason": "Bind exact remote observation evidence to the qualified ancestry classifier and preserve observed-tip versus contained-content semantics."
    },
    {
      "id": "RPE-05",
      "closes": ["NB9"],
      "name": "CONTROLLED_REAL_EXPERIMENT_PREREGISTRATION",
      "reason": "Only after static/runtime prerequisites are qualified should a real network experiment be specified."
    }
  ],
  "post_readiness_gate": {
    "real_experiment_execution_authorized_by_this_map": false,
    "required_before_real_experiment": [
      "RPE-01 QUALIFIED",
      "RPE-02 QUALIFIED",
      "RPE-03 QUALIFIED",
      "RPE-04 QUALIFIED",
      "RPE-05 PREREGISTERED_AND_HUMAN_ADOPTED",
      "separate one-shot human execution authorization"
    ],
    "mandatory_stop": true
  }
}

~~~~

# SOURCE: READINESS REPORT
Path: reports/program/2026-10-02-OBSIDIAN-REAL-P5E-PRE-EXECUTION-READINESS-V0.1.md
~~~~
# REAL P5-E â€” PRE-EXECUTION READINESS V0.1

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
RPE-01 â€” N4 CLOSED SCHEMA
        â†“
RPE-02 â€” N5 TIMING BOUNDARIES
        â†“
RPE-03 â€” NB5 ANCESTRY CLASSIFIER
        â†“
RPE-04 â€” NB2 + NB3 REAL OBSERVATION ADAPTER
        â†“
RPE-05 â€” NB9 CONTROLLED REAL EXPERIMENT PREREGISTRATION
        â†“
SEPARATE HUMAN AUTHORIZATION
        â†“
ONE FINITE REAL EXPERIMENT
```

This order minimizes rework because each later layer consumes the semantics frozen by the previous layer.

## VERIFIED â€” N4

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
## VERIFIED â€” N5

The synthetic model currently behaves coherently, but the equality and rounding semantics are not fully frozen by dedicated contract language/tests.

Read-only probes of the adopted model produced:

```text
release exactly at 30 â†’ slot 30 eligible â†’ PASS latency 0
release exactly at 60 â†’ slot 60 eligible â†’ PASS latency 0
release at 31 â†’ first required slot 60 â†’ PASS latency 29

attempt 30 completing at 60 â†’ allowed
previous completion 60 and next attempt start 60 â†’ allowed / not overlap
attempt 30 completing at 61 â†’ BLOCKED ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT

uppercase SHA â†’ rejected
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
## VERIFIED â€” NB5

P5-D2 is a deterministic consumer of a normalized event.

Its input requires an explicit:

`transition_class`

but P5-D2 does not prove that class against the Git graph.

A read-only probe demonstrated that an Aâ†’Bâ†’A sequence can be supplied with the second A mislabeled `FAST_FORWARD`; P5-D2 accepts the caller-provided class because classification is outside its authority.

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
- no previous â†’ INITIAL;
- same SHA â†’ SAME;
- previous is ancestor of new â†’ FAST_FORWARD;
- both commits verified but previous is not ancestor of new â†’ NON_FAST_FORWARD;
- missing object, non-commit object, Git error, or unprovable relation â†’ UNKNOWN.

Qualify against a temporary local Git graph containing fast-forward, rollback, divergence, same, initial, missing-object, and non-commit cases.
## VERIFIED â€” NB2 + NB3

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
â†’ CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED

caller supplies containment=false
â†’ UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION
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

The system does not need to decide whether a Bâ†’A observation was caused by lag, rollback, or a third-party push. It needs only to prove the Git graph relation:
- descendant â†’ FAST_FORWARD;
- verified not-descendant â†’ NON_FAST_FORWARD;
- unprovable â†’ UNKNOWN.

NB3 is closed when exact tip observation and content containment become distinct runtime evidence classes rather than caller assertions.
## VERIFIED â€” NB9

The adopted timing metric requires:

```text
CONTROLLED_SOURCE_RELEASE_MONOTONIC
â†’
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
â†’ source identity
â†’ read-only Git intent
â†’ isolated checkout principle
â†’ candidate 30s / 60s target

P5-D1 / P5-D2
â†’ deterministic state machine
â†’ normalized event schema
â†’ fail-closed NON_FAST_FORWARD / UNKNOWN

P5-D4
â†’ bounded orchestration
â†’ injected observation adapter boundary
â†’ single-writer / persistent state discipline

P5-D3F real runner pattern
â†’ exact ls-remote ref validation pattern

FrozenGitSource
â†’ exact frozen commit/tree/blob reads after identity is already frozen
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

### RPE-01 â€” CLOSED SCHEMA GUARD

Scope:
`N4 only`

Mode:
`CONTRACT_FIRST / TEST_FIRST / NO_RUNTIME_COUPLING`

STOP after qualification.

### RPE-02 â€” TIMING BOUNDARY FREEZE

Scope:
`N5 only`

Prefer tests/contract around unchanged model.

STOP after qualification.

### RPE-03 â€” ANCESTRY CLASSIFIER

Scope:
`NB5 only`

Use local finite Git fixtures.

No network.

STOP after qualification.

### RPE-04 â€” REAL OBSERVATION ADAPTER

Scope:
`NB2 + NB3`

First qualify against local bare remote/injected I/O.

No real GitHub polling.

STOP after qualification.

### RPE-05 â€” CONTROLLED REAL EXPERIMENT PREREGISTRATION

Scope:
`NB9 only`

Define exact release/ref/clock/schedule/stop protocol.

STOP before execution.

### Final execution gate

Only after RPE-01â†’RPE-05 are closed:

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

~~~~

# SOURCE: P5-E HUMAN ADOPTION
Path: GOVERNANCE/P5-E-V0.1-CONTRACT-SYNTHETIC-TIMING-MODEL-HUMAN-ADJUDICATION-2026-10-02.md
~~~~
# P5-E V0.1 â€” CONTRACT + SYNTHETIC TIMING MODEL â€” HUMAN ADJUDICATION

Date: 2026-10-02

## Human decision

The human authority adopts:

`P5-E V0.1 â€” CONTRACT + SYNTHETIC TIMING MODEL`

as:

`P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL = QUALIFIED_AND_HUMAN_ADOPTED`

This adoption follows:

- external B1â†’B5 closure;
- BB1 `NORMATIVE GUARD COVERAGE` closure;
- BB1 external re-review `PASS_WITH_NON_BLOCKING_NOTES`;
- `FINAL PRE-ADOPTION EVIDENCE HYGIENE`;
- final external delta-review `PASS_WITH_NON_BLOCKING_NOTES`;
- final internal adjudication of D1â†’D4.
## Binding pre-adoption identity

This adoption is bound to the exact pre-adoption repository state:

```text
PRE-ADOPTION HEAD
= 3aca84cea6edf17e337015c195c91a4195bc6dfc

CONTRACT
= 43d2e45b40c6c1cf81f0e79d7650e6dc00be0da9

SYNTHETIC MODEL
= c0f16baa151c1466e30ba5778f1fca8184cd4aac

EVIDENCE MATRIX
= 454889848803bdaeed70a6fdfd80033ff22b8e72
```

Branch at adoption:

`feat/obsidian-projection-p5e-v0.1-final-pre-adoption-evidence-hygiene`

Pre-adoption local HEAD and remote HEAD were equal.

Pre-adoption worktree was clean.
## Adopted scope

The human adoption covers only:

- the P5-E V0.1 contract;
- the P5-E synthetic timing model;
- the evidence and guard structure used to qualify that contract/model candidate;
- the current bounded claim scope established by the reviewed candidate.

This adoption does not convert synthetic qualification into real execution qualification.

## Explicitly not qualified or authorized

This adoption does not qualify:

- real P5-E behavior;
- a real 60-second SLA;
- continuous synchronization;
- detection of every transient remote tip;
- a real observation adapter;
- ancestry-classifier correctness.

This adoption does not authorize:

- automatic evaluation;
- Stage A;
- Stage B;
- promotion;
- publication;
- Vault mutation;
- `CURRENT.md` mutation;
- daemon execution;
- Scheduled Task registration;
- Windows Service registration;
- startup registration;
- P6.
## Mandatory prerequisites before any REAL P5-E preregistration or execution

The following remain mandatory prerequisites:

- `N4` â€” closed-schema / added-key hardening;
- `N5` â€” exact real timing-boundary semantics;
- `NB2` â€” Bâ†’A / rollback / lag ambiguity;
- `NB3` â€” real tip-visibility adapter semantics;
- `NB5` â€” ancestry-classifier correctness;
- `NB9` â€” controlled-release real experiment protocol.

These prerequisites are not waived by this adoption.

They remain outside the adopted synthetic candidate and must be explicitly resolved or preregistered before REAL P5-E can be opened.
## Retained non-blocking notes

### D1 â€” N1 fixture discrimination

The current N1 test correctly verifies:

`READ_COMPLETION_PRECEDES_ATTEMPT_START`

and kills removal of that guard through its exact failure-code assertion.

A future hardening may use a more discriminating fixture such as a valid prior slot followed by an impossible completion-before-start record.

This is a test-quality note only.

### D2 â€” external packet completeness

Future external-review packets should embed every source required for independent reproduction even when a source is unchanged from a previous packet.

This is a packaging / provenance note only.

### D3 â€” current semantic sweep count

The current contract includes the N1 field and therefore has:

```text
CURRENT SEMANTIC SWEEP
= 162 leaves
= 13 survivors
= all 13 non-normative
= 0 normative survivors
```

The earlier `161 / 13 / 0 normative` evidence remains historical evidence for the prior BB1 candidate state.

The full qualification surface with object binding produced zero survivors because object identity drift is rejected.

These two measurements answer different questions and must not be conflated.
### D4 â€” reused evidence provenance granularity

`REUSED_QUALIFIED_P5D2_P5D4` is interpreted at the level of the reused behavioral method, not as a claim that the entire current test file is byte-identical to its historical qualified file.

Current evidence-matrix count:

```text
REUSED_QUALIFIED_P5D2_P5D4
= 11 entries total

7 entries â†’ P5-D2 test_observer_tick.py methods
4 entries â†’ P5-D4 bounded-loop runtime test methods
```

The two newly introduced pending-non-active D2-file mappings remain:

`DIRECT_P5E`

This note does not change the qualification verdict.
## Review and qualification state at adoption

The latest external delta-review returned:

`PASS_WITH_NON_BLOCKING_NOTES`

with:

`BLOCKING_FINDINGS = NONE`

The internally adjudicated result before adoption is:

```text
BB1_EXTERNAL_REVIEW
= PASS_WITH_NON_BLOCKING_NOTES

FINAL_HYGIENE_DELTA_REVIEW
= PASS_WITH_NON_BLOCKING_NOTES

TECHNICAL_CORRECTION_REQUIRED_BEFORE_ADOPTION
= NONE

P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= READY_FOR_HUMAN_NORMATIVE_ADJUDICATION
```

The human decision in this record closes that adjudication gate.
## Authority boundary after adoption

The adopted state is:

```text
P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL
= QUALIFIED_AND_HUMAN_ADOPTED

REAL_P5E
= CLOSED

REAL_HEAD_EVALUATION
= CLOSED

STAGE_A
= CLOSED

STAGE_B
= CLOSED

PROMOTION
= CLOSED

PUBLICATION
= CLOSED

VAULT_OR_CURRENT_MUTATION
= CLOSED

DAEMON_OR_SERVICE_REGISTRATION
= CLOSED

P6
= CLOSED
```

No authority is created beyond the exact synthetic-contract adoption recorded here.

## Persistence authority

The only operation authorized after this human statement is:

- persist this adjudication record;
- commit and push it;
- verify final repository consistency;
- STOP.

No contract, model, matrix, runtime, Vault, CURRENT, P5-D4 control state, or real P5-E execution surface may be mutated by this persistence step.

~~~~

# SOURCE: ADOPTED P5-E CONTRACT
Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW",
  "qualification_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5a_qualification_report_blob": "8954475370494ff00f77af8331b2e54b80cf3f70",
    "p5d1_observer_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d1_static_review_blob": "d10a6659e8deec917803f53c652fc7e4d4d19458",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_static_review_blob": "023cc210facdbc4b571b88bd257057c67a3df46b",
    "p5d4_loop_contract_blob": "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
    "p5d4_runtime_blob": "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
    "p5d4_real_v0_2_qualification_blob": "660a679532d1bb122b0df382230d4d249a0cac1f",
    "p5d4_human_adjudication_blob": "ef5e07c6641db94e91d9f2bc0e8093b244baa507"
  },
  "objective": {
    "name": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "purpose": "Define the temporal and authority contract required before any real repeated observation experiment may claim bounded near-real-time behavior around the already-qualified P5-D4 bounded loop.",
    "this_stage_is_not_real_end_to_end_execution": true,
    "this_stage_may_not_claim_continuous_synchronization": true
  },
  "near_real_time_timing": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "poll_interval_seconds": 30,
    "detection_latency_seconds_max": 60,
    "instantaneous_realtime_claim_forbidden": true,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true,
    "detection_latency_definition": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "FIXED_RATE_30_SECOND_GRID",
    "single_transient_read_failure_may_still_meet_60_second_bound": false,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true,
    "real_measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
    "schedule_semantics": "FIXED_RATE",
    "remote_head_available_time_is_measurable_origin": false,
    "real_latency_metric": "REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC",
    "attempt_start_and_read_completion_are_distinct": true,
    "read_duration_is_included_in_detection_latency": true,
    "eligible_detection_attempt_must_start_at_or_after_release": true,
    "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation.",
    "schedule_semantics": "FIXED_RATE",
    "schedule_origin_seconds": 0,
    "observation_record_fields": [
      "scheduled_at_seconds",
      "completed_at_seconds",
      "outcome",
      "observed_head"
    ],
    "head_identity_required_on_successful_remote_observation": true,
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "explicit_non_pass_statuses": [
      "INCOMPLETE_SYNTHETIC_WINDOW"
    ],
    "attempt_overruns_next_required_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "attempt_overruns_next_required_slot_failure_code": "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT",
    "duplicate_fixed_rate_slot_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "duplicate_fixed_rate_slot_failure_code": "DUPLICATE_FIXED_RATE_SLOT",
    "read_completion_before_attempt_start_forbidden": true
  },
  "authority_boundary": {
    "observer_may_create_governance_authority": false,
    "pending_head_evaluation_authorized": false,
    "evaluation_authorized": false,
    "stage_a_authorized": false,
    "stage_b_authorized": false,
    "promotion_authorized": false,
    "publication_authorized": false,
    "real_vault_mutation_authorized": false,
    "current_mutation_authorized": false,
    "current_tmp_mutation_authorized": false,
    "real_polling_loop_authorized": false,
    "daemon_authorized": false,
    "startup_registration_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "p6_authorized": false
  },
  "head_transition_policy": {
    "same_head_result": "NOOP",
    "same_head_queue_growth_forbidden": true,
    "initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics": true,
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "non_fast_forward_auto_continue_forbidden": true,
    "unknown_ancestry_auto_continue_forbidden": true,
    "active_or_pending_candidate_retarget_forbidden": true
  },
  "queue_and_supersession": {
    "precedence_rule": "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT",
    "p5a_supersession_intent_preserved_as_future_design_debt": true,
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "coalescing_authorized": false,
    "new_coalescing_semantic_event_authorized": false,
    "pending_head_retarget_forbidden": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_mutate_p5d2_state": true,
    "burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification": true
  },
  "failure_and_freshness": {
    "fail_closed_default": true,
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved": true,
    "latency_bound_breach_result": "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED",
    "queue_capacity_exhaustion_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "timing_inconsistency_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "skipped_required_attempt_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "cadence_gap_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "pre_source_target_observation_result": "BLOCKED_REQUIRES_ADJUDICATION"
  },
  "end_to_end_definition": {
    "real_end_to_end_stages": [
      "SOURCE_HEAD_BECOMES_OBSERVABLE",
      "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
      "HEAD_TRANSITION_CLASSIFIED",
      "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
      "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
      "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
      "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
      "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED"
    ],
    "current_stage_may_qualify_only": [
      "TIMING_CONTRACT",
      "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
      "AUTHORITY_BOUNDARIES",
      "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true,
    "transient_tip_exact_detection_sla_not_qualified": true,
    "real_remote_availability_to_detection_sla_not_qualified": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED",
      "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
      "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED"
    ]
  },
  "real_context_evidence_only": {
    "live_projection_head_at_opening": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head_at_opening": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_observed_during_contract_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "must_not_be_used_as_real_experiment_execution": true,
    "must_not_be_mutated_by_contract_qualification": true
  },
  "required_synthetic_cases": [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD"
  ],
  "required_breakers": [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS"
  ],
  "next_gate_after_candidate_qualification": {
    "external_adversarial_review_required_before_normative_adoption": true,
    "human_adjudication_required_after_external_review": true,
    "real_p5e_execution_requires_separate_human_authorization": true,
    "p6_remains_closed": true,
    "external_adversarial_rereview_required": true,
    "human_adjudication_before_external_rereview_forbidden": true
  },
  "tip_visibility_semantics": {
    "observed_remote_tip_definition": "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ",
    "intermediate_fast_forward_commit_definition": "COMMIT_CONTAINED_BY_LATER_OBSERVED_FAST_FORWARD_HEAD_BUT_NOT_ITSELF_OBSERVED_AS_REMOTE_TIP",
    "unobserved_intermediate_tip_may_be_claimed_observed": false,
    "unobserved_intermediate_tip_may_be_queued": false,
    "fast_forward_content_containment_is_queue_coalescing": false,
    "already_observed_queued_head_replacement_forbidden": true,
    "already_observed_queued_head_retarget_forbidden": true,
    "per_transient_tip_detection_sla_authorized": false,
    "future_ancestry_enumeration_requires_separate_qualification": true,
    "unobserved_intermediate_tip_non_injection_is_future_adapter_rule": true,
    "unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property": false
  },
  "external_review_targeted_closure": {
    "findings": {
      "B1": "CONFIRMED_BLOCKING_WITH_UPSTREAM_COVERAGE_NUANCE",
      "B2": "CONFIRMED_BLOCKING",
      "B3": "CONFIRMED_BLOCKING",
      "B4": "CONFIRMED_BLOCKING",
      "B5": "PARTIALLY_CONFIRMED_BLOCKING_SEMANTIC_GAP"
    },
    "required_breakers": [
      "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
      "CADENCE_GAP_ACCEPTED",
      "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
      "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
      "READ_COMPLETION_LATENCY_HIDDEN",
      "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
      "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
      "REQUIRED_CASE_OR_BREAKER_UNMAPPED"
    ],
    "requirement_to_executable_evidence_matrix_required": true,
    "all_required_cases_must_be_mapped": true,
    "all_base_breakers_must_be_mapped": true,
    "all_targeted_closure_breakers_must_be_mapped": true,
    "unmapped_requirement_result": "BLOCKED",
    "external_rereview_required_before_human_normative_adoption": true
  }
}

~~~~

# SOURCE: ADOPTED P5-E SYNTHETIC MODEL
Path: tools/obsidian_projection/p5e_near_real_time_model.py
~~~~
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1_AMENDED"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1_AMENDED"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_SCHEDULE_ORIGIN_SECONDS = 0
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "REMOTE_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def _valid_head(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 40:
        return False
    return all(ch in "0123456789abcdef" for ch in value)


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
    schedule_origin_seconds: int = _SCHEDULE_ORIGIN_SECONDS,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    if schedule_origin_seconds != _SCHEDULE_ORIGIN_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 synthetic fixed-rate origin must remain exactly zero"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": _POLL_INTERVAL_SECONDS,
        "detection_latency_seconds_max": _DETECTION_LATENCY_SECONDS_MAX,
        "schedule_origin_seconds": _SCHEDULE_ORIGIN_SECONDS,
        "schedule_semantics": "FIXED_RATE",
        "clock_source": "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY",
        "measurement_origin": "CONTROLLED_SOURCE_RELEASE_MONOTONIC",
        "measurement_endpoint": "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC",
        "real_execution_authorized": False,
    }


def _validate_plan(plan: dict[str, Any]) -> None:
    if not isinstance(plan, dict):
        raise P5ETimingModelError("plan must be an object")
    if plan != make_timing_plan(
        poll_interval_seconds=plan.get("poll_interval_seconds"),
        detection_latency_seconds_max=plan.get(
            "detection_latency_seconds_max"
        ),
        schedule_origin_seconds=plan.get("schedule_origin_seconds"),
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _blocked(failure_code: str) -> dict[str, Any]:
    return _result(
        status="BLOCKED_REQUIRES_ADJUDICATION",
        failure_code=failure_code,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )


def _result(
    *,
    status: str,
    failure_code: str | None,
    detection_latency_seconds: int | None,
    first_detection_scheduled_at_seconds: int | None,
    first_detection_completed_at_seconds: int | None,
    observed_head: str | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "failure_code": failure_code,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_scheduled_at_seconds": (
            first_detection_scheduled_at_seconds
        ),
        "first_detection_completed_at_seconds": (
            first_detection_completed_at_seconds
        ),
        "observed_head": observed_head,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def _first_fixed_rate_slot_at_or_after(
    *,
    instant_seconds: int,
    interval: int,
    origin: int,
) -> int:
    first_slot = origin + interval
    if instant_seconds <= first_slot:
        return first_slot
    delta = instant_seconds - origin
    quotient, remainder = divmod(delta, interval)
    return origin + (quotient + (1 if remainder else 0)) * interval


def _validate_observation_shapes(
    observations: list[dict[str, Any]],
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    required_fields = {
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    }
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != required_fields:
            raise P5ETimingModelError("observation fields mismatch")
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]
        outcome = observation["outcome"]
        observed_head = observation["observed_head"]
        if not _is_nonnegative_int(scheduled):
            raise P5ETimingModelError("scheduled time must be nonnegative")
        if not _is_nonnegative_int(completed):
            raise P5ETimingModelError("completion time must be nonnegative")
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        if outcome == "READ_FAILURE":
            if observed_head is not None:
                raise P5ETimingModelError(
                    "read failure may not carry a head identity"
                )
        elif not _valid_head(observed_head):
            raise P5ETimingModelError(
                "successful remote observation requires exact head identity"
            )


def classify_tip_visibility(
    *,
    target_head: str,
    observed_head: str,
    fast_forward_contains_target: bool,
) -> str:
    if not _valid_head(target_head) or not _valid_head(observed_head):
        raise P5ETimingModelError("tip identity must be a lowercase 40-hex SHA")
    if not isinstance(fast_forward_contains_target, bool):
        raise P5ETimingModelError("containment fact must be boolean")
    if observed_head == target_head:
        return "EXACT_TIP_OBSERVED"
    if fast_forward_contains_target:
        return "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED"
    return "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION"


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_release_at_seconds: int,
    target_head: str,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_release_at_seconds):
        raise P5ETimingModelError(
            "controlled source release time must be a nonnegative integer"
        )
    if not _valid_head(target_head):
        raise P5ETimingModelError(
            "target head must be a lowercase 40-hex SHA"
        )
    _validate_observation_shapes(observations)

    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    origin = plan["schedule_origin_seconds"]

    previous_scheduled: int | None = None
    previous_completed: int | None = None
    for observation in observations:
        scheduled = observation["scheduled_at_seconds"]
        completed = observation["completed_at_seconds"]

        if scheduled <= origin or (scheduled - origin) % interval != 0:
            return _blocked("ATTEMPT_OFF_FIXED_RATE_GRID")
        if completed < scheduled:
            return _blocked("READ_COMPLETION_PRECEDES_ATTEMPT_START")
        if previous_scheduled is not None:
            if scheduled == previous_scheduled:
                return _blocked("DUPLICATE_FIXED_RATE_SLOT")
            if scheduled - previous_scheduled != interval:
                return _blocked("CADENCE_GAP")
            if previous_completed is not None and previous_completed > scheduled:
                return _blocked("ATTEMPT_OVERLAP")
        previous_scheduled = scheduled
        previous_completed = completed

        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
            and scheduled < source_release_at_seconds
        ):
            return _blocked(
                "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE"
            )

    last_observation = observations[-1]
    if (
        last_observation["completed_at_seconds"]
        > last_observation["scheduled_at_seconds"] + interval
    ):
        return _blocked("ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT")

    first_required_slot = _first_fixed_rate_slot_at_or_after(
        instant_seconds=source_release_at_seconds,
        interval=interval,
        origin=origin,
    )
    scheduled_slots = {
        observation["scheduled_at_seconds"] for observation in observations
    }
    if (
        any(slot >= first_required_slot for slot in scheduled_slots)
        and first_required_slot not in scheduled_slots
    ):
        return _blocked("SKIPPED_REQUIRED_ATTEMPT")

    first_detection: dict[str, Any] | None = None
    for observation in observations:
        if observation["scheduled_at_seconds"] < source_release_at_seconds:
            continue
        if (
            observation["outcome"] == "REMOTE_HEAD_OBSERVED"
            and observation["observed_head"] == target_head
        ):
            first_detection = observation
            break

    if first_detection is not None:
        completed = first_detection["completed_at_seconds"]
        latency = completed - source_release_at_seconds
        if latency <= bound:
            status = "PASS_DETECTED_WITHIN_BOUND"
            failure_code = None
        else:
            status = "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED"
            failure_code = "DETECTION_COMPLETION_EXCEEDED_BOUND"
        return _result(
            status=status,
            failure_code=failure_code,
            detection_latency_seconds=latency,
            first_detection_scheduled_at_seconds=(
                first_detection["scheduled_at_seconds"]
            ),
            first_detection_completed_at_seconds=completed,
            observed_head=first_detection["observed_head"],
        )

    last_scheduled = observations[-1]["scheduled_at_seconds"]
    next_required_slot = last_scheduled + interval
    if next_required_slot - source_release_at_seconds > bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            failure_code="NO_FUTURE_FIXED_RATE_ATTEMPT_CAN_MEET_BOUND",
            detection_latency_seconds=None,
            first_detection_scheduled_at_seconds=None,
            first_detection_completed_at_seconds=None,
            observed_head=None,
        )

    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        failure_code=None,
        detection_latency_seconds=None,
        first_detection_scheduled_at_seconds=None,
        first_detection_completed_at_seconds=None,
        observed_head=None,
    )

~~~~

# SOURCE: P5-E ADVERSARIAL INVARIANT TESTS
Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py
~~~~
import ast
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
MODEL = ROOT / "tools" / "obsidian_projection" / "p5e_near_real_time_model.py"

TARGET = "a" * 40
OTHER = "b" * 40

EXPECTED_CASES = [
    "SAME_HEAD_NOOP",
    "CHANGE_JUST_AFTER_POLL_DETECTED_AT_NEXT_30_SECOND_SLOT",
    "ONE_TRANSIENT_READ_FAILURE_THEN_DETECTED_BY_60_SECONDS",
    "DETECTION_AFTER_60_SECONDS_REJECTED",
    "NO_DETECTION_BY_60_SECONDS_REJECTED",
    "NON_FAST_FORWARD_BLOCKED",
    "UNKNOWN_ANCESTRY_BLOCKED",
    "PENDING_QUEUE_FULL_NEWER_HEAD_FAILS_CLOSED",
    "SAME_HEAD_DOES_NOT_GROW_QUEUE",
    "SECOND_HEAD_DOES_NOT_RETARGET_PENDING_HEAD",
]

EXPECTED_BASE_BREAKERS = [
    "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
    "DETECTION_BOUND_ABOVE_60_ACCEPTED",
    "INSTANTANEOUS_REALTIME_CLAIM_ACCEPTED",
    "WALL_CLOCK_USED_AS_SYNTHETIC_CONTROL_CLOCK",
    "SLEEP_USED_IN_SYNTHETIC_MODEL",
    "NETWORK_USED_IN_SYNTHETIC_MODEL",
    "FILESYSTEM_STATE_USED_IN_SYNTHETIC_MODEL",
    "PROCESS_LAUNCH_USED_IN_SYNTHETIC_MODEL",
    "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
    "NO_SUCCESS_BY_60_SECONDS_CLASSIFIED_PASS",
    "SAME_HEAD_GROWS_QUEUE",
    "NON_FAST_FORWARD_AUTO_CONTINUES",
    "UNKNOWN_ANCESTRY_AUTO_CONTINUES",
    "QUEUE_FULL_SILENTLY_DROPS_HEAD",
    "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
    "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
    "PENDING_HEAD_RETARGETED_TO_NEWER_HEAD",
    "EVALUATION_AUTHORITY_BECOMES_TRUE",
    "PROMOTION_AUTHORITY_BECOMES_TRUE",
    "PUBLICATION_AUTHORITY_BECOMES_TRUE",
    "REAL_VAULT_MUTATION_AUTHORITY_BECOMES_TRUE",
    "REAL_POLLING_AUTHORITY_BECOMES_TRUE",
    "DAEMON_OR_SERVICE_AUTHORITY_BECOMES_TRUE",
    "P6_AUTHORITY_BECOMES_TRUE",
    "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
]

EXPECTED_CLOSURE_BREAKERS = [
    "SKIPPED_REQUIRED_ATTEMPT_ACCEPTED",
    "CADENCE_GAP_ACCEPTED",
    "PRE_SOURCE_TARGET_OBSERVATION_IGNORED",
    "REMOTE_AVAILABILITY_TIME_TREATED_AS_MEASURABLE_ORIGIN",
    "READ_COMPLETION_LATENCY_HIDDEN",
    "OBSERVATION_WITHOUT_HEAD_IDENTITY_ACCEPTED",
    "UNOBSERVED_TRANSIENT_TIP_CLAIMED_EXACTLY_OBSERVED",
    "REQUIRED_CASE_OR_BREAKER_UNMAPPED",
]


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model_adv", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def obs(scheduled, completed, outcome, head=None):
    return {
        "scheduled_at_seconds": scheduled,
        "completed_at_seconds": completed,
        "outcome": outcome,
        "observed_head": head,
    }


def assert_contract_invariants(contract):
    assert contract["schema"] == "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1"
    assert contract["status"] == "CANDIDATE_TARGETED_CLOSURE_PENDING_EXTERNAL_REREVIEW"
    assert contract["qualification_stage"] == "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY"
    assert contract["real_p5e_execution_authorized"] is False
    assert contract["source_repository"] == "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"

    source = contract["monitored_source"]
    assert source["remote"] == "origin"
    assert source["branch"] == "integration/system-v1"
    assert source["canonical_authority"] == "GITHUB_REMOTE_BRANCH"
    assert source["local_working_tree_is_not_authority"] is True

    objective = contract["objective"]
    assert objective["this_stage_is_not_real_end_to_end_execution"] is True
    assert objective["this_stage_may_not_claim_continuous_synchronization"] is True

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True
    assert timing["delivery_semantics"] == "NEAR_REAL_TIME_BOUNDED_LATENCY"
    assert timing["detection_latency_definition"] == (
        "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC_MINUS_CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    )
    assert timing["future_real_bound_clock"] == "MONOTONIC_ELAPSED_TIME"
    assert timing["future_real_wall_clock_may_be_recorded_as_evidence_only"] is True
    assert timing["latency_bound_breach_must_not_be_reported_as_near_real_time_pass"] is True
    assert timing["real_measurement_origin"] == "CONTROLLED_SOURCE_RELEASE_MONOTONIC"
    assert timing["measurement_endpoint"] == "SUCCESSFUL_REMOTE_READ_COMPLETION_MONOTONIC"
    assert timing["schedule_semantics"] == "FIXED_RATE"
    assert timing["future_real_poll_schedule_semantics"] == "FIXED_RATE_30_SECOND_GRID"
    assert timing["remote_head_available_time_is_measurable_origin"] is False
    assert timing["attempt_start_and_read_completion_are_distinct"] is True
    assert timing["read_duration_is_included_in_detection_latency"] is True
    assert timing["eligible_detection_attempt_must_start_at_or_after_release"] is True
    assert timing["single_transient_read_failure_may_still_meet_60_second_bound"] is False
    assert timing[
        "single_transient_read_failure_may_meet_bound_only_if_read_completion_is_within_60_seconds"
    ] is True

    synthetic = contract["synthetic_timing_model"]
    assert synthetic["required"] is True
    assert synthetic["clock_source"] == "EXPLICIT_INJECTED_MONOTONIC_SECONDS_ONLY"
    assert synthetic["schedule_semantics"] == "FIXED_RATE"
    assert synthetic["schedule_origin_seconds"] == 0
    assert synthetic["sleep_forbidden"] is True
    assert synthetic["network_forbidden"] is True
    assert synthetic["filesystem_state_forbidden"] is True
    assert synthetic["process_launch_forbidden"] is True
    assert synthetic["environment_read_forbidden"] is True
    assert synthetic["real_p5d4_control_state_access_forbidden"] is True
    assert synthetic["real_vault_access_forbidden"] is True
    assert synthetic["observation_record_fields"] == [
        "scheduled_at_seconds",
        "completed_at_seconds",
        "outcome",
        "observed_head",
    ]
    assert synthetic["head_identity_required_on_successful_remote_observation"] is True
    assert synthetic["explicit_non_pass_statuses"] == ["INCOMPLETE_SYNTHETIC_WINDOW"]
    assert synthetic["attempt_overruns_next_required_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["attempt_overruns_next_required_slot_failure_code"] == "ATTEMPT_OVERRUNS_NEXT_FIXED_RATE_SLOT"
    assert synthetic["duplicate_fixed_rate_slot_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["duplicate_fixed_rate_slot_failure_code"] == "DUPLICATE_FIXED_RATE_SLOT"
    assert synthetic["read_completion_before_attempt_start_forbidden"] is True
    assert synthetic["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert synthetic["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    transition = contract["head_transition_policy"]
    assert transition["same_head_result"] == "NOOP"
    assert transition["same_head_queue_growth_forbidden"] is True
    assert transition["initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
    assert transition["fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics"] is True
    assert transition["non_fast_forward_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["non_fast_forward_auto_continue_forbidden"] is True
    assert transition["unknown_ancestry_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert transition["unknown_ancestry_auto_continue_forbidden"] is True
    assert transition["active_or_pending_candidate_retarget_forbidden"] is True

    queue = contract["queue_and_supersession"]
    assert queue["fifo_required"] is True
    assert queue["unique_heads_required"] is True
    assert queue["silent_drop_forbidden"] is True
    assert queue["silent_reorder_forbidden"] is True
    assert queue["latest_only_replacement_forbidden"] is True
    assert queue["coalescing_authorized"] is False
    assert queue["new_coalescing_semantic_event_authorized"] is False
    assert queue["pending_head_retarget_forbidden"] is True
    assert queue["capacity_exhausted_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert queue["capacity_exhausted_must_not_mutate_p5d2_state"] is True
    assert queue["burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification"] is True
    assert queue["precedence_rule"] == (
        "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_"
        "EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT"
    )

    failure = contract["failure_and_freshness"]
    assert failure["fail_closed_default"] is True
    assert failure["network_failure_must_not_create_current_claim"] is True
    assert failure["last_known_good_live_projection_preserved"] is True
    assert failure["latency_bound_breach_result"] == "NEAR_REAL_TIME_BOUND_NOT_QUALIFIED"
    assert failure["queue_capacity_exhaustion_result"] == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    assert failure["non_fast_forward_or_unknown_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["unexpected_state_or_timing_ambiguity_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["timing_inconsistency_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["skipped_required_attempt_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["cadence_gap_result"] == "BLOCKED_REQUIRES_ADJUDICATION"
    assert failure["pre_source_target_observation_result"] == "BLOCKED_REQUIRES_ADJUDICATION"

    authority = contract["authority_boundary"]
    for field in (
        "observer_may_create_governance_authority",
        "pending_head_evaluation_authorized",
        "evaluation_authorized",
        "stage_a_authorized",
        "stage_b_authorized",
        "promotion_authorized",
        "publication_authorized",
        "real_vault_mutation_authorized",
        "current_mutation_authorized",
        "current_tmp_mutation_authorized",
        "real_polling_loop_authorized",
        "daemon_authorized",
        "startup_registration_authorized",
        "scheduled_task_authorized",
        "windows_service_authorized",
        "p6_authorized",
    ):
        assert authority[field] is False

    real_context = contract["real_context_evidence_only"]
    assert real_context["must_not_be_used_as_real_experiment_execution"] is True
    assert real_context["must_not_be_mutated_by_contract_qualification"] is True

    tips = contract["tip_visibility_semantics"]
    assert tips["observed_remote_tip_definition"] == "HEAD_IDENTITY_RETURNED_BY_A_SUCCESSFUL_REMOTE_READ"
    assert tips["unobserved_intermediate_tip_may_be_claimed_observed"] is False
    assert tips["unobserved_intermediate_tip_may_be_queued"] is False
    assert tips["fast_forward_content_containment_is_queue_coalescing"] is False
    assert tips["already_observed_queued_head_replacement_forbidden"] is True
    assert tips["already_observed_queued_head_retarget_forbidden"] is True
    assert tips["per_transient_tip_detection_sla_authorized"] is False
    assert tips["future_ancestry_enumeration_requires_separate_qualification"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_future_adapter_rule"] is True
    assert tips["unobserved_intermediate_tip_non_injection_is_current_runtime_qualified_property"] is False

    end_to_end = contract["end_to_end_definition"]
    assert end_to_end["real_end_to_end_stages"] == [
        "SOURCE_HEAD_BECOMES_OBSERVABLE",
        "REMOTE_HEAD_DETECTED_WITHIN_BOUND",
        "HEAD_TRANSITION_CLASSIFIED",
        "EXACT_HEAD_ENTERED_GOVERNED_QUEUE_OR_FAIL_CLOSED",
        "EXACT_HEAD_EVALUATED_IF_SEPARATELY_AUTHORIZED",
        "PROMOTION_DECISION_IF_SEPARATELY_AUTHORIZED",
        "PUBLICATION_IF_SEPARATELY_AUTHORIZED",
        "LIVE_GENERATION_VERIFIED_IF_PUBLICATION_AUTHORIZED",
    ]
    assert end_to_end["current_stage_may_qualify_only"] == [
        "TIMING_CONTRACT",
        "SYNTHETIC_FIXED_RATE_DETECTION_MODEL",
        "AUTHORITY_BOUNDARIES",
        "REUSED_MAPPED_P5D2_P5D4_FAIL_CLOSED_QUEUE_BEHAVIOR",
    ]
    assert end_to_end["real_end_to_end_pass_requires_all_authorized_applicable_stages"] is True
    assert end_to_end["omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass"] is True
    assert end_to_end["transient_tip_exact_detection_sla_not_qualified"] is True
    assert end_to_end["real_remote_availability_to_detection_sla_not_qualified"] is True

    claims = contract["claim_boundary"]
    assert claims["maximum_current_claim"] == (
        "P5E_V0_1_TARGETED_CLOSURE_CANDIDATE_QUALIFIED_PENDING_EXTERNAL_REREVIEW"
    )
    assert claims["real_end_to_end_qualification_requires_separate_authorization"] is True
    forbidden = set(claims["forbidden_current_claims"])
    for claim in (
        "P5E_REAL_END_TO_END_QUALIFIED",
        "REAL_60_SECOND_SLA_QUALIFIED",
        "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
        "REMOTE_HEAD_AVAILABLE_TIME_TO_DETECTION_SLA_QUALIFIED",
        "PER_TRANSIENT_TIP_DETECTION_SLA_QUALIFIED",
    ):
        assert claim in forbidden

    gate = contract["next_gate_after_candidate_qualification"]
    assert gate["external_adversarial_review_required_before_normative_adoption"] is True
    assert gate["human_adjudication_required_after_external_review"] is True
    assert gate["p6_remains_closed"] is True
    assert gate["real_p5e_execution_requires_separate_human_authorization"] is True
    assert gate["external_adversarial_rereview_required"] is True
    assert gate["human_adjudication_before_external_rereview_forbidden"] is True

    assert contract["required_synthetic_cases"] == EXPECTED_CASES
    assert contract["required_breakers"] == EXPECTED_BASE_BREAKERS
    closure = contract["external_review_targeted_closure"]
    assert closure["required_breakers"] == EXPECTED_CLOSURE_BREAKERS
    assert closure["requirement_to_executable_evidence_matrix_required"] is True
    assert closure["all_required_cases_must_be_mapped"] is True
    assert closure["all_base_breakers_must_be_mapped"] is True
    assert closure["all_targeted_closure_breakers_must_be_mapped"] is True
    assert closure["unmapped_requirement_result"] == "BLOCKED"
    assert closure["external_rereview_required_before_human_normative_adoption"] is True


class TestP5EAdversarialV01(unittest.TestCase):
    def setUp(self):
        self.contract = load_contract()
        assert_contract_invariants(self.contract)

    def assert_mutation_rejected(self, mutator):
        candidate = copy.deepcopy(self.contract)
        mutator(candidate)
        with self.assertRaises(AssertionError):
            assert_contract_invariants(candidate)

    def test_timing_mutations_are_rejected(self):
        mutations = [
            lambda c: c["near_real_time_timing"].__setitem__("poll_interval_seconds", 31),
            lambda c: c["near_real_time_timing"].__setitem__("detection_latency_seconds_max", 61),
            lambda c: c["near_real_time_timing"].__setitem__("instantaneous_realtime_claim_forbidden", False),
            lambda c: c["near_real_time_timing"].__setitem__("schedule_semantics", "FIXED_DELAY"),
            lambda c: c["near_real_time_timing"].__setitem__("remote_head_available_time_is_measurable_origin", True),
            lambda c: c["near_real_time_timing"].__setitem__("read_duration_is_included_in_detection_latency", False),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_previously_surviving_contract_mutations_are_rejected(self):
        mutations = [
            lambda c: c["head_transition_policy"].__setitem__("non_fast_forward_result", "AUTO_CONTINUE"),
            lambda c: c["head_transition_policy"].__setitem__("unknown_ancestry_auto_continue_forbidden", False),
            lambda c: c["head_transition_policy"].__setitem__("same_head_queue_growth_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_must_not_mutate_p5d2_state", False),
            lambda c: c["synthetic_timing_model"].__setitem__("clock_source", "WALL_CLOCK"),
            lambda c: c["authority_boundary"].__setitem__("observer_may_create_governance_authority", True),
            lambda c: c["next_gate_after_candidate_qualification"].__setitem__("p6_remains_closed", False),
            lambda c: c.__setitem__("required_breakers", [f"FAKE_{i}" for i in range(25)]),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_authority_mutations_are_rejected(self):
        for field in (
            "evaluation_authorized",
            "promotion_authorized",
            "publication_authorized",
            "real_vault_mutation_authorized",
            "real_polling_loop_authorized",
            "daemon_authorized",
            "startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p6_authorized",
        ):
            self.assert_mutation_rejected(
                lambda c, field=field: c["authority_boundary"].__setitem__(field, True)
            )

    def test_queue_mutations_are_rejected(self):
        mutations = [
            lambda c: c["queue_and_supersession"].__setitem__("coalescing_authorized", True),
            lambda c: c["queue_and_supersession"].__setitem__("latest_only_replacement_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("pending_head_retarget_forbidden", False),
            lambda c: c["queue_and_supersession"].__setitem__("capacity_exhausted_result", "CONTINUE"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_claim_and_tip_mutations_are_rejected(self):
        mutations = [
            lambda c: c["claim_boundary"].__setitem__("maximum_current_claim", "P5E_REAL_END_TO_END_QUALIFIED"),
            lambda c: c["tip_visibility_semantics"].__setitem__("unobserved_intermediate_tip_may_be_claimed_observed", True),
            lambda c: c["tip_visibility_semantics"].__setitem__("per_transient_tip_detection_sla_authorized", True),
            lambda c: c["end_to_end_definition"]["current_stage_may_qualify_only"].append("REAL_END_TO_END"),
        ]
        for mutator in mutations:
            self.assert_mutation_rejected(mutator)

    def test_required_lists_cannot_be_reduced_or_replaced(self):
        self.assert_mutation_rejected(
            lambda c: c.__setitem__("required_synthetic_cases", ["SAME_HEAD_NOOP"])
        )
        self.assert_mutation_rejected(
            lambda c: c["external_review_targeted_closure"].__setitem__(
                "required_breakers", ["FAKE"]
            )
        )

    def test_synthetic_model_imports_are_ast_allowlisted(self):
        tree = ast.parse(MODEL.read_text(encoding="utf-8"))
        allowed = {"__future__", "typing"}
        forbidden_calls = {
            "open", "eval", "exec", "__import__", "compile", "input"
        }
        forbidden_attributes = {
            "sleep", "wait", "system", "popen", "Popen", "run",
            "connect", "request", "urlopen", "FileIO", "environ"
        }
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name.split(".")[0], allowed)
            elif isinstance(node, ast.ImportFrom):
                self.assertIn((node.module or "").split(".")[0], allowed)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_calls)
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attributes)
            elif isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, forbidden_attributes)

    def test_exact_60_second_completion_boundary_passes(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=0,
            target_head=TARGET,
            observations=[
                obs(30, 30, "READ_FAILURE"),
                obs(60, 60, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_pre_source_target_observation_blocks(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=45,
            target_head=TARGET,
            observations=[
                obs(30, 31, "REMOTE_HEAD_OBSERVED", TARGET),
                obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(
            result["failure_code"],
            "TARGET_HEAD_OBSERVED_BEFORE_CONTROLLED_RELEASE",
        )

    def test_invalid_source_release_values_are_rejected(self):
        m = load_model()
        for value in (-1, True):
            with self.assertRaises(m.P5ETimingModelError):
                m.qualify_detection(
                    plan=m.make_timing_plan(),
                    source_release_at_seconds=value,
                    target_head=TARGET,
                    observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
                )

    def test_empty_observation_list_is_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[],
            )

    def test_invalid_observation_shape_and_head_are_rejected(self):
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "REMOTE_HEAD_OBSERVED", None)],
            )
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=0,
                target_head=TARGET,
                observations=[obs(30, 30, "PROMOTE", None)],
            )

    def test_cadence_duplicate_and_gap_are_blocked(self):
        m = load_model()
        for observations, code in (
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "DUPLICATE_FIXED_RATE_SLOT",
            ),
            (
                [
                    obs(30, 30, "READ_FAILURE"),
                    obs(90, 90, "REMOTE_HEAD_OBSERVED", TARGET),
                ],
                "CADENCE_GAP",
            ),
        ):
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
            self.assertEqual(result["failure_code"], code)

    def test_attempt_overlap_is_blocked(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[
                obs(30, 61, "READ_FAILURE"),
                obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET),
            ],
        )
        self.assertEqual(result["status"], "BLOCKED_REQUIRES_ADJUDICATION")
        self.assertEqual(result["failure_code"], "ATTEMPT_OVERLAP")

    def test_incomplete_window_does_not_claim_pass(self):
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_release_at_seconds=1,
            target_head=TARGET,
            observations=[obs(30, 31, "READ_FAILURE")],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertFalse(result["real_end_to_end_qualified"])
        self.assertFalse(result["continuous_synchronization_qualified"])

    def test_all_result_paths_keep_downstream_authority_false(self):
        m = load_model()
        cases = [
            [obs(30, 30, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(30, 31, "READ_FAILURE"), obs(60, 60, "READ_FAILURE")],
            [obs(30, 31, "READ_FAILURE"), obs(60, 62, "REMOTE_HEAD_OBSERVED", TARGET)],
            [obs(60, 61, "REMOTE_HEAD_OBSERVED", TARGET)],
        ]
        for observations in cases:
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_release_at_seconds=1,
                target_head=TARGET,
                observations=observations,
            )
            self.assertFalse(result["automatic_evaluation_authorized"])
            self.assertFalse(result["automatic_promotion_authorized"])
            self.assertFalse(result["automatic_publication_authorized"])

    def test_tip_visibility_does_not_launder_containment_into_exact_observation(self):
        m = load_model()
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=True,
            ),
            "CONTENT_CONTAINED_TRANSIENT_TIP_NOT_OBSERVED",
        )
        self.assertEqual(
            m.classify_tip_visibility(
                target_head=TARGET,
                observed_head=OTHER,
                fast_forward_contains_target=False,
            ),
            "UNRELATED_OR_UNPROVEN_REQUIRES_ADJUDICATION",
        )


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-D1 CONTINUOUS OBSERVER CORE CONTRACT
Path: tools/obsidian_projection/continuous_observer_core_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_CONTINUOUS_OBSERVER_CORE_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "qualified_predecessors": {
    "p5a_continuous_projection_contract_blob": "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
    "p5b2_dynamic_inventory_qualification_report_blob": "286a81a4f3f71a1d857631c2388d7894908acb5f",
    "p5c2_promotion_qualification_report_blob": "a928598182b25d110c9040c62d846bf9018ac3ed",
    "p5c3r2_final_qualification_report_blob": "fd54a78abde8342c6da708d3a4096b4d0b267905",
    "p5c3r2_qualified_runtime_candidate": "b5f3a8de061772e15bc94b20095d419130c20781",
    "p5c3r2_final_qualification_commit": "00ca2946ce30b0e319658f8d5b903357b7ccfc5e"
  },
  "objective": {
    "name": "DETERMINISTIC_AUDITABLE_OBSERVER_STATE_MACHINE",
    "purpose": "Define the pure observer state transition model before any background loop, scheduler, startup registration, or production continuous write authority exists.",
    "one_shot_first": true,
    "background_loop_deferred": true,
    "time_based_behavior_deferred": true,
    "production_runtime_deferred": true
  },
  "authority_boundary": {
    "github_remote_branch": "CANONICAL",
    "observer_core": "DERIVED_DECISION_ENGINE",
    "projection": "DERIVED",
    "obsidian": "OBSERVE_NAVIGATE_QUERY_VISUALIZE_UNDERSTAND",
    "observer_may_push_to_github": false,
    "observer_may_commit_to_github": false,
    "observer_may_modify_canonical_worktree": false,
    "observer_may_create_governance_authority": false,
    "observer_may_modify_human_views": false,
    "observer_may_modify_obsidian_config": false
  },
  "deterministic_core": {
    "pure_transition_required": true,
    "transition_signature": "next_state_and_decision = TRANSITION(previous_state, normalized_input)",
    "network_io_inside_transition_forbidden": true,
    "filesystem_io_inside_transition_forbidden": true,
    "process_launch_inside_transition_forbidden": true,
    "wall_clock_read_inside_transition_forbidden": true,
    "randomness_inside_transition_forbidden": true,
    "environment_variable_read_inside_transition_forbidden": true,
    "same_inputs_must_produce_byte_identical_normalized_outputs": true,
    "canonical_json_encoding": "UTF8_SORTED_KEYS_COMPACT_LF",
    "state_digest_algorithm": "SHA256",
    "decision_digest_algorithm": "SHA256",
    "volatile_event_envelope_excluded_from_state_digest": true
  },
  "state_schema": {
    "schema": "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1",
    "required_fields": [
      "repository",
      "branch",
      "observer_phase",
      "remote_freshness",
      "latest_observed_head",
      "last_qualified_head",
      "live_projection_head",
      "projection_state",
      "pending_heads",
      "blocked_head",
      "last_failure_code",
      "last_event_sequence"
    ],
    "observer_phase_allowed": [
      "IDLE",
      "CANDIDATE_PENDING",
      "EVALUATING",
      "BLOCKED",
      "STOPPED"
    ],
    "remote_freshness_allowed": [
      "KNOWN",
      "UNKNOWN"
    ],
    "projection_state_allowed": [
      "CURRENT",
      "STALE",
      "BLOCKED",
      "ORPHAN",
      "MISSING"
    ],
    "head_format": "LOWERCASE_40_HEX_SHA1",
    "pending_heads_order": "OBSERVATION_ORDER_FIFO_UNIQUE",
    "last_event_sequence_monotonic_nonnegative_integer": true,
    "timestamps_forbidden_in_deterministic_state": true,
    "pid_forbidden_in_deterministic_state": true,
    "host_paths_forbidden_in_deterministic_state": true
  },
  "input_schema": {
    "schema": "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1",
    "event_types": [
      "BOOTSTRAP",
      "REMOTE_HEAD_OBSERVED",
      "REMOTE_OBSERVATION_FAILED",
      "EVALUATION_STARTED",
      "EVALUATION_PASSED",
      "EVALUATION_FAILED",
      "PROMOTION_CONFIRMED",
      "PROMOTION_FAILED",
      "LOCK_CONTENDED",
      "SHUTDOWN_REQUESTED"
    ],
    "remote_head_transition_classes": [
      "INITIAL",
      "SAME",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "transition_classification_must_be_explicit": true,
    "implicit_history_rewrite_acceptance_forbidden": true
  },
  "decision_schema": {
    "schema": "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1",
    "allowed_actions": [
      "NOOP",
      "QUEUE_EXACT_HEAD_FOR_EVALUATION",
      "START_EXACT_HEAD_EVALUATION",
      "RETAIN_LAST_KNOWN_GOOD",
      "BLOCK_REQUIRES_ADJUDICATION",
      "CANDIDATE_QUALIFIED_PENDING_PROMOTION",
      "CONFIRM_LIVE_PROJECTION",
      "STOP"
    ],
    "required_fields": [
      "action",
      "reason_code",
      "observed_head",
      "candidate_head",
      "previous_live_head",
      "next_projection_state",
      "automatic_promotion_authorized",
      "production_write_authorized"
    ],
    "automatic_promotion_authorized_must_be_false_in_p5d1": true,
    "production_write_authorized_must_be_false_in_p5d1": true
  },
  "transition_rules": {
    "bootstrap_without_live_projection": {
      "observer_phase": "IDLE",
      "remote_freshness": "UNKNOWN",
      "projection_state": "MISSING",
      "action": "NOOP"
    },
    "remote_observation_failed": {
      "remote_freshness": "UNKNOWN",
      "live_projection_head_must_not_change": true,
      "pending_heads_must_not_gain_unverified_head": true,
      "projection_state_if_previous_current": "STALE",
      "other_noncurrent_projection_states_are_retained": true,
      "action": "RETAIN_LAST_KNOWN_GOOD",
      "new_current_claim_forbidden": true
    },
    "same_head": {
      "queue_growth_forbidden": true,
      "evaluation_start_forbidden": true,
      "action": "NOOP",
      "current_allowed_only_if_live_projection_head_equals_observed_head_and_last_qualified_head_equals_observed_head": true
    },
    "initial_head": {
      "automatic_evaluation_queue_allowed": true,
      "projection_state_if_live_missing": "MISSING",
      "projection_state_if_live_exists": "STALE",
      "action": "QUEUE_EXACT_HEAD_FOR_EVALUATION"
    },
    "fast_forward_head": {
      "automatic_evaluation_queue_allowed": true,
      "projection_state": "STALE",
      "action": "QUEUE_EXACT_HEAD_FOR_EVALUATION"
    },
    "non_fast_forward_head": {
      "automatic_evaluation_queue_allowed": false,
      "automatic_promotion_forbidden": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "action": "BLOCK_REQUIRES_ADJUDICATION"
    },
    "unknown_ancestry_head": {
      "automatic_evaluation_queue_allowed": false,
      "automatic_promotion_forbidden": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "action": "BLOCK_REQUIRES_ADJUDICATION"
    },
    "evaluation_started": {
      "candidate_must_equal_pending_head": true,
      "observer_phase": "EVALUATING",
      "live_projection_head_must_not_change": true,
      "action": "START_EXACT_HEAD_EVALUATION"
    },
    "evaluation_passed": {
      "candidate_must_equal_evaluating_head": true,
      "observer_phase": "CANDIDATE_PENDING",
      "last_qualified_head_becomes_candidate": true,
      "live_projection_head_must_not_change": true,
      "action": "CANDIDATE_QUALIFIED_PENDING_PROMOTION",
      "promotion_still_requires_separate_authority": true
    },
    "evaluation_failed": {
      "candidate_must_equal_evaluating_head": true,
      "live_projection_head_must_not_change": true,
      "observer_phase": "BLOCKED",
      "projection_state": "BLOCKED",
      "action": "RETAIN_LAST_KNOWN_GOOD"
    },
    "promotion_confirmed_model_semantics": {
      "candidate_must_equal_last_qualified_head": true,
      "live_projection_head_becomes_candidate": true,
      "current_only_if_remote_freshness_known_and_latest_observed_head_equals_candidate": true,
      "otherwise_projection_state": "STALE",
      "action": "CONFIRM_LIVE_PROJECTION",
      "p5d1_execution_authorized": false
    },
    "promotion_failed_model_semantics": {
      "live_projection_head_must_not_change": true,
      "projection_state": "BLOCKED",
      "action": "RETAIN_LAST_KNOWN_GOOD",
      "p5d1_execution_authorized": false
    },
    "lock_contended": {
      "state_mutation_forbidden_except_event_sequence": true,
      "action": "NOOP",
      "production_write_authorized": false
    },
    "shutdown_requested": {
      "observer_phase": "STOPPED",
      "action": "STOP",
      "pending_heads_must_be_preserved": true
    }
  },
  "freshness_semantics": {
    "network_failure_may_not_present_projection_as_fresh_current": true,
    "current_requires_remote_freshness_known": true,
    "current_requires_latest_observed_head_equals_live_projection_head": true,
    "current_requires_live_projection_head_equals_last_qualified_head": true,
    "unknown_remote_freshness_must_be_visible_to_later_health_reporting": true
  },
  "queue_and_coalescing": {
    "every_unique_observed_head_must_have_append_only_event": true,
    "pending_head_identity_is_exact_sha": true,
    "duplicate_pending_head_forbidden": true,
    "observation_order_preserved": true,
    "active_evaluation_bound_to_exact_head": true,
    "newer_head_may_not_retarget_active_evaluation": true,
    "superseded_head_may_be_removed_only_after_proven_fast_forward_containment": true,
    "superseded_status": "SUPERSEDED_NOT_PROMOTED",
    "latest_observed_eligible_head_must_eventually_be_evaluated": true,
    "runtime_queue_capacity_policy_deferred_to_p5d4": true
  },
  "event_and_audit_model": {
    "append_only_event_required": true,
    "event_schema": "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1",
    "minimum_fields": [
      "sequence",
      "event_type",
      "previous_state_digest",
      "input_digest",
      "decision_digest",
      "next_state_digest",
      "reason_code"
    ],
    "optional_volatile_envelope_fields": [
      "observed_at",
      "host_id",
      "process_id"
    ],
    "volatile_envelope_fields_must_not_affect_deterministic_digests": true,
    "event_log_is_not_semantic_authority": true,
    "event_sequence_must_be_strictly_monotonic": true
  },
  "single_writer_model": {
    "required": true,
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "lock_acquisition_is_outside_pure_transition": true,
    "lock_owner_identity_must_not_enter_deterministic_state_digest": true,
    "stale_lock_recovery_policy_deferred_to_p5d3": true
  },
  "last_known_good": {
    "required": true,
    "live_projection_head_may_change_only_after_separate_confirmed_promotion": true,
    "failed_observation_must_not_change_live_projection_head": true,
    "failed_evaluation_must_not_change_live_projection_head": true,
    "failed_promotion_must_not_change_live_projection_head": true,
    "recursive_delete_of_last_known_good_forbidden": true
  },
  "qualified_component_boundaries": {
    "dynamic_inventory_contract_must_be_reused_not_reimplemented": true,
    "atomic_pointer_primitive_must_be_reused_not_reimplemented": true,
    "p5c3r2_reader_retry_policy_must_be_reused_not_weakened": true,
    "human_views_remain_protected": true,
    "obsidian_config_remains_protected": true,
    "graph_search_current_semantics_remain_deferred_to_p6": true
  },
  "p5d1_boundary": {
    "contract_and_breakers_only": true,
    "observer_core_implementation_authorized": false,
    "network_observation_execution_authorized": false,
    "remote_fetch_execution_authorized": false,
    "background_observer_execution_authorized": false,
    "polling_loop_execution_authorized": false,
    "production_promotion_authorized": false,
    "continuous_vault_write_authorized": false,
    "windows_startup_registration_authorized": false,
    "scheduled_task_creation_authorized": false,
    "windows_service_creation_authorized": false,
    "graph_search_semantics_authorized": false
  },
  "required_breakers": [
    "same HEAD triggers queue growth",
    "same HEAD triggers evaluation",
    "network failure changes live projection head",
    "network failure creates a new CURRENT freshness claim",
    "remote freshness UNKNOWN is presented as fresh CURRENT",
    "CURRENT accepted when observed head differs from live projection head",
    "CURRENT accepted when live projection head differs from last qualified head",
    "INITIAL head is silently ignored",
    "FAST_FORWARD head is silently ignored",
    "NON_FAST_FORWARD enters automatic evaluation",
    "NON_FAST_FORWARD enters automatic promotion",
    "UNKNOWN ancestry enters automatic evaluation",
    "UNKNOWN ancestry enters automatic promotion",
    "active evaluation retargeted to newer observed head",
    "duplicate pending head accepted",
    "observation order silently reordered",
    "superseded head dropped without proven fast-forward containment",
    "latest eligible queued head never evaluated",
    "evaluation starts for head not in pending queue",
    "evaluation PASS mutates live projection head",
    "evaluation FAIL mutates live projection head",
    "promotion failure mutates last-known-good live head",
    "promotion confirmation accepted for head different from last qualified head",
    "second writer receives production write authority",
    "lock owner PID changes deterministic state digest",
    "wall clock changes deterministic state digest",
    "environment variable changes deterministic state digest",
    "randomness changes deterministic state digest",
    "transition performs network IO",
    "transition performs filesystem IO",
    "transition launches process",
    "observer pushes to GitHub",
    "observer commits to GitHub",
    "observer mutates canonical worktree",
    "observer overwrites human views",
    "observer modifies .obsidian",
    "observer enables Obsidian Sync",
    "observer installs community plugin",
    "dynamic inventory is reimplemented instead of reused",
    "atomic pointer primitive is reimplemented instead of reused",
    "P5-C3R2 reader retry policy is weakened",
    "background polling starts during P5-D1",
    "production promotion occurs during P5-D1",
    "Windows startup registration occurs during P5-D1",
    "scheduled task is created during P5-D1",
    "Windows service is created during P5-D1",
    "Graph/Search CURRENT semantics are claimed during P5-D1",
    "event sequence is not strictly monotonic",
    "event log loses previous state digest",
    "volatile envelope data changes deterministic decision digest"
  ],
  "next_gates": {
    "p5d2": "ONE_SHOT_OBSERVER_TICK_IMPLEMENTATION",
    "p5d3": "CONTROLLED_CANDIDATE_EVALUATION_PIPELINE",
    "p5d4": "BOUNDED_OBSERVER_LOOP_CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "p6": "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE"
  }
}

~~~~

# SOURCE: P5-D2 OBSERVER TICK
Path: tools/obsidian_projection/observer_tick.py
~~~~
from __future__ import annotations

import hashlib
import json
import re
from typing import Any


class ObserverTickError(RuntimeError):
    pass


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"
CONTRACT_BLOB = "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3"

STATE_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1"
INPUT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1"
DECISION_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"

OBSERVER_PHASES = frozenset(
    {
        "IDLE",
        "CANDIDATE_PENDING",
        "EVALUATING",
        "BLOCKED",
        "STOPPED",
    }
)
REMOTE_FRESHNESS = frozenset({"KNOWN", "UNKNOWN"})
PROJECTION_STATES = frozenset(
    {
        "CURRENT",
        "STALE",
        "BLOCKED",
        "ORPHAN",
        "MISSING",
    }
)
EVENT_TYPES = frozenset(
    {
        "BOOTSTRAP",
        "REMOTE_HEAD_OBSERVED",
        "REMOTE_OBSERVATION_FAILED",
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
        "LOCK_CONTENDED",
        "SHUTDOWN_REQUESTED",
    }
)
TRANSITION_CLASSES = frozenset(
    {
        "INITIAL",
        "SAME",
        "FAST_FORWARD",
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }
)

_STATE_KEYS = frozenset(
    {
        "schema",
        "repository",
        "branch",
        "observer_phase",
        "remote_freshness",
        "latest_observed_head",
        "last_qualified_head",
        "live_projection_head",
        "projection_state",
        "pending_heads",
        "blocked_head",
        "last_failure_code",
        "last_event_sequence",
    }
)
_INPUT_KEYS = frozenset(
    {
        "schema",
        "event_type",
        "sequence",
        "observed_head",
        "transition_class",
        "candidate_head",
        "failure_code",
    }
)

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")


def _canonical_json_bytes(value: Any) -> bytes:
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ObserverTickError(
            "value is not canonical JSON"
        ) from exc
    return (encoded + "\n").encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(
        _canonical_json_bytes(value)
    ).hexdigest()


def _clone(value: Any) -> Any:
    try:
        return json.loads(
            _canonical_json_bytes(value).decode("utf-8")
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ObserverTickError(
            "canonical clone failed"
        ) from exc


def _is_head(value: Any) -> bool:
    return (
        isinstance(value, str)
        and _HEAD_RE.fullmatch(value) is not None
    )


def _require_optional_head(
    value: Any,
    field: str,
) -> None:
    if value is not None and not _is_head(value):
        raise ObserverTickError(
            f"{field} must be lowercase 40-hex SHA-1 or null"
        )


def _require_failure_code(
    value: Any,
    *,
    required: bool,
) -> None:
    if required:
        if (
            not isinstance(value, str)
            or not value
            or value.strip() != value
        ):
            raise ObserverTickError(
                "failure_code required"
            )
        return
    if value is not None:
        raise ObserverTickError(
            "failure_code must be null"
        )


def _validate_state(state: dict[str, Any]) -> None:
    if not isinstance(state, dict):
        raise ObserverTickError("state must be an object")
    if frozenset(state) != _STATE_KEYS:
        raise ObserverTickError("state fields mismatch")
    if state["schema"] != STATE_SCHEMA:
        raise ObserverTickError("state schema mismatch")
    if state["repository"] != EXPECTED_REPOSITORY:
        raise ObserverTickError("repository mismatch")
    if state["branch"] != EXPECTED_BRANCH:
        raise ObserverTickError("branch mismatch")
    if state["observer_phase"] not in OBSERVER_PHASES:
        raise ObserverTickError("invalid observer phase")
    if state["remote_freshness"] not in REMOTE_FRESHNESS:
        raise ObserverTickError("invalid remote freshness")
    if state["projection_state"] not in PROJECTION_STATES:
        raise ObserverTickError("invalid projection state")

    _require_optional_head(
        state["latest_observed_head"],
        "latest_observed_head",
    )
    _require_optional_head(
        state["last_qualified_head"],
        "last_qualified_head",
    )
    _require_optional_head(
        state["live_projection_head"],
        "live_projection_head",
    )
    _require_optional_head(
        state["blocked_head"],
        "blocked_head",
    )

    pending = state["pending_heads"]
    if not isinstance(pending, list):
        raise ObserverTickError(
            "pending_heads must be an array"
        )
    if not all(_is_head(item) for item in pending):
        raise ObserverTickError(
            "pending_heads contains invalid HEAD"
        )
    if len(pending) != len(set(pending)):
        raise ObserverTickError(
            "pending_heads contains duplicate HEAD"
        )

    failure = state["last_failure_code"]
    if failure is not None and (
        not isinstance(failure, str)
        or not failure
        or failure.strip() != failure
    ):
        raise ObserverTickError(
            "invalid last_failure_code"
        )

    sequence = state["last_event_sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence < 0
    ):
        raise ObserverTickError(
            "invalid last_event_sequence"
        )

    if state["projection_state"] == "CURRENT":
        if state["remote_freshness"] != "KNOWN":
            raise ObserverTickError(
                "CURRENT requires KNOWN remote freshness"
            )
        live = state["live_projection_head"]
        if live is None:
            raise ObserverTickError(
                "CURRENT requires live projection HEAD"
            )
        if state["latest_observed_head"] != live:
            raise ObserverTickError(
                "CURRENT requires observed == live"
            )
        if state["last_qualified_head"] != live:
            raise ObserverTickError(
                "CURRENT requires live == qualified"
            )

    if (
        state["observer_phase"] == "EVALUATING"
        and not pending
    ):
        raise ObserverTickError(
            "EVALUATING requires pending queue head"
        )

    if (
        state["observer_phase"] == "CANDIDATE_PENDING"
        and state["last_qualified_head"] is None
    ):
        raise ObserverTickError(
            "CANDIDATE_PENDING requires qualified HEAD"
        )

    if state["observer_phase"] == "BLOCKED":
        if state["projection_state"] != "BLOCKED":
            raise ObserverTickError(
                "BLOCKED phase requires BLOCKED projection"
            )
        if state["blocked_head"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires blocked HEAD"
            )
        if state["last_failure_code"] is None:
            raise ObserverTickError(
                "BLOCKED phase requires failure code"
            )


def _validate_input(
    previous_state: dict[str, Any],
    event: dict[str, Any],
) -> None:
    if not isinstance(event, dict):
        raise ObserverTickError("input must be an object")
    if frozenset(event) != _INPUT_KEYS:
        raise ObserverTickError("input fields mismatch")
    if event["schema"] != INPUT_SCHEMA:
        raise ObserverTickError("input schema mismatch")
    if event["event_type"] not in EVENT_TYPES:
        raise ObserverTickError("invalid event type")

    sequence = event["sequence"]
    if (
        isinstance(sequence, bool)
        or not isinstance(sequence, int)
        or sequence
        != previous_state["last_event_sequence"] + 1
    ):
        raise ObserverTickError(
            "input sequence must advance exactly once"
        )

    _require_optional_head(
        event["observed_head"],
        "observed_head",
    )
    _require_optional_head(
        event["candidate_head"],
        "candidate_head",
    )

    transition_class = event["transition_class"]
    if (
        transition_class is not None
        and transition_class not in TRANSITION_CLASSES
    ):
        raise ObserverTickError(
            "invalid transition class"
        )

    event_type = event["event_type"]

    if event_type == "REMOTE_HEAD_OBSERVED":
        if event["observed_head"] is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires observed_head"
            )
        if transition_class is None:
            raise ObserverTickError(
                "REMOTE_HEAD_OBSERVED requires transition_class"
            )
        if event["candidate_head"] is not None:
            raise ObserverTickError(
                "remote observation forbids candidate_head"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type == "REMOTE_OBSERVATION_FAILED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
        ):
            raise ObserverTickError(
                "remote failure carries no HEAD"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type in {
        "EVALUATION_STARTED",
        "EVALUATION_PASSED",
        "PROMOTION_CONFIRMED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=False,
        )
        return

    if event_type in {
        "EVALUATION_FAILED",
        "PROMOTION_FAILED",
    }:
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is None
        ):
            raise ObserverTickError(
                f"{event_type} normalized fields invalid"
            )
        _require_failure_code(
            event["failure_code"],
            required=True,
        )
        return

    if event_type == "LOCK_CONTENDED":
        if (
            event["observed_head"] is not None
            or transition_class is not None
            or event["candidate_head"] is not None
            or event["failure_code"] != "LOCK_CONTENDED"
        ):
            raise ObserverTickError(
                "LOCK_CONTENDED normalized fields invalid"
            )
        return

    if (
        event["observed_head"] is not None
        or transition_class is not None
        or event["candidate_head"] is not None
    ):
        raise ObserverTickError(
            f"{event_type} carries unexpected HEAD"
        )
    _require_failure_code(
        event["failure_code"],
        required=False,
    )


def make_initial_state() -> dict[str, Any]:
    state = {
        "schema": STATE_SCHEMA,
        "repository": EXPECTED_REPOSITORY,
        "branch": EXPECTED_BRANCH,
        "observer_phase": "IDLE",
        "remote_freshness": "UNKNOWN",
        "latest_observed_head": None,
        "last_qualified_head": None,
        "live_projection_head": None,
        "projection_state": "MISSING",
        "pending_heads": [],
        "blocked_head": None,
        "last_failure_code": None,
        "last_event_sequence": 0,
    }
    _validate_state(state)
    return state


def _decision(
    *,
    action: str,
    reason_code: str,
    observed_head: str | None,
    candidate_head: str | None,
    previous_live_head: str | None,
    next_projection_state: str,
) -> dict[str, Any]:
    return {
        "schema": DECISION_SCHEMA,
        "action": action,
        "reason_code": reason_code,
        "observed_head": observed_head,
        "candidate_head": candidate_head,
        "previous_live_head": previous_live_head,
        "next_projection_state": next_projection_state,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }


def _apply_remote_observed(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    observed = event["observed_head"]
    transition_class = event["transition_class"]
    previous_live = state["live_projection_head"]
    previous_observed = state["latest_observed_head"]

    if transition_class == "INITIAL":
        if previous_observed is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
    elif transition_class == "SAME":
        if previous_observed != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
    else:
        if previous_observed is None:
            raise ObserverTickError(
                f"{transition_class} requires previous observed HEAD"
            )
        if previous_observed == observed:
            raise ObserverTickError(
                f"{transition_class} requires a new observed HEAD"
            )

    if state["observer_phase"] == "BLOCKED":
        if (
            transition_class == "SAME"
            and state["latest_observed_head"] != observed
        ):
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code="OBSERVER_ALREADY_BLOCKED",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if transition_class == "SAME":
        if state["latest_observed_head"] != observed:
            raise ObserverTickError(
                "SAME requires previous observed HEAD equality"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if (
            next_state["observer_phase"] != "BLOCKED"
            and next_state["live_projection_head"] is not None
            and next_state["live_projection_head"] == observed
            and next_state["last_qualified_head"] == observed
        ):
            next_state["projection_state"] = "CURRENT"
        decision = _decision(
            action="NOOP",
            reason_code="REMOTE_HEAD_SAME",
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if transition_class == "INITIAL":
        if state["latest_observed_head"] is not None:
            raise ObserverTickError(
                "INITIAL requires no previous observed HEAD"
            )
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = (
            "MISSING"
            if next_state["live_projection_head"] is None
            else "STALE"
        )
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_INITIAL_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if state["latest_observed_head"] is None:
        raise ObserverTickError(
            f"{transition_class} requires previous observed HEAD"
        )
    if state["latest_observed_head"] == observed:
        raise ObserverTickError(
            f"{transition_class} requires a new observed HEAD"
        )

    if transition_class == "FAST_FORWARD":
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["last_failure_code"] = None
        if observed not in next_state["pending_heads"]:
            next_state["pending_heads"].append(observed)
        next_state["projection_state"] = "STALE"
        decision = _decision(
            action="QUEUE_EXACT_HEAD_FOR_EVALUATION",
            reason_code="REMOTE_HEAD_FAST_FORWARD_QUEUED",
            observed_head=observed,
            candidate_head=observed,
            previous_live_head=previous_live,
            next_projection_state="STALE",
        )
        return next_state, decision

    if transition_class in {
        "NON_FAST_FORWARD",
        "UNKNOWN",
    }:
        next_state = _clone(state)
        next_state["remote_freshness"] = "KNOWN"
        next_state["latest_observed_head"] = observed
        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = observed
        next_state["last_failure_code"] = (
            "NON_FAST_FORWARD_REQUIRES_ADJUDICATION"
            if transition_class == "NON_FAST_FORWARD"
            else "UNKNOWN_ANCESTRY_REQUIRES_ADJUDICATION"
        )
        decision = _decision(
            action="BLOCK_REQUIRES_ADJUDICATION",
            reason_code=next_state["last_failure_code"],
            observed_head=observed,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    raise ObserverTickError(
        "unsupported remote transition class"
    )


def _apply_transition(
    state: dict[str, Any],
    event: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    event_type = event["event_type"]
    previous_live = state["live_projection_head"]

    if state["observer_phase"] == "STOPPED":
        raise ObserverTickError(
            "STOPPED observer accepts no further events"
        )

    if event_type == "BOOTSTRAP":
        if state["last_event_sequence"] != 0:
            raise ObserverTickError(
                "BOOTSTRAP allowed only at sequence zero"
            )
        if state != make_initial_state():
            raise ObserverTickError(
                "BOOTSTRAP requires canonical initial state"
            )
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="BOOTSTRAP_ACCEPTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "REMOTE_HEAD_OBSERVED":
        return _apply_remote_observed(state, event)

    if event_type == "REMOTE_OBSERVATION_FAILED":
        next_state = _clone(state)
        next_state["remote_freshness"] = "UNKNOWN"
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        if next_state["projection_state"] == "CURRENT":
            next_state["projection_state"] = "STALE"
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="REMOTE_OBSERVATION_FAILED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "EVALUATION_STARTED":
        candidate = event["candidate_head"]
        if state["observer_phase"] != "IDLE":
            raise ObserverTickError(
                "evaluation may start only from IDLE"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["observer_phase"] = "EVALUATING"
        decision = _decision(
            action="START_EXACT_HEAD_EVALUATION",
            reason_code="EVALUATION_STARTED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state=next_state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type in {
        "EVALUATION_PASSED",
        "EVALUATION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "EVALUATING":
            raise ObserverTickError(
                f"{event_type} requires EVALUATING phase"
            )
        if (
            not state["pending_heads"]
            or state["pending_heads"][0] != candidate
        ):
            raise ObserverTickError(
                "evaluation result candidate must equal queue head"
            )
        next_state = _clone(state)
        next_state["pending_heads"] = (
            next_state["pending_heads"][1:]
        )

        if event_type == "EVALUATION_PASSED":
            next_state["last_qualified_head"] = candidate
            next_state["observer_phase"] = (
                "CANDIDATE_PENDING"
            )
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            decision = _decision(
                action=(
                    "CANDIDATE_QUALIFIED_PENDING_PROMOTION"
                ),
                reason_code="EVALUATION_PASSED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="EVALUATION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type in {
        "PROMOTION_CONFIRMED",
        "PROMOTION_FAILED",
    }:
        candidate = event["candidate_head"]
        if state["observer_phase"] != "CANDIDATE_PENDING":
            raise ObserverTickError(
                f"{event_type} requires CANDIDATE_PENDING"
            )
        if state["last_qualified_head"] != candidate:
            raise ObserverTickError(
                "promotion candidate must equal last qualified HEAD"
            )
        next_state = _clone(state)

        if event_type == "PROMOTION_CONFIRMED":
            next_state["live_projection_head"] = candidate
            next_state["observer_phase"] = "IDLE"
            next_state["blocked_head"] = None
            next_state["last_failure_code"] = None
            if (
                next_state["remote_freshness"] == "KNOWN"
                and next_state["latest_observed_head"]
                == candidate
            ):
                next_state["projection_state"] = "CURRENT"
            else:
                next_state["projection_state"] = "STALE"
            decision = _decision(
                action="CONFIRM_LIVE_PROJECTION",
                reason_code="PROMOTION_CONFIRMED",
                observed_head=None,
                candidate_head=candidate,
                previous_live_head=previous_live,
                next_projection_state=next_state[
                    "projection_state"
                ],
            )
            return next_state, decision

        next_state["observer_phase"] = "BLOCKED"
        next_state["projection_state"] = "BLOCKED"
        next_state["blocked_head"] = candidate
        next_state["last_failure_code"] = event[
            "failure_code"
        ]
        decision = _decision(
            action="RETAIN_LAST_KNOWN_GOOD",
            reason_code="PROMOTION_FAILED",
            observed_head=None,
            candidate_head=candidate,
            previous_live_head=previous_live,
            next_projection_state="BLOCKED",
        )
        return next_state, decision

    if event_type == "LOCK_CONTENDED":
        next_state = _clone(state)
        decision = _decision(
            action="NOOP",
            reason_code="LOCK_CONTENDED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    if event_type == "SHUTDOWN_REQUESTED":
        next_state = _clone(state)
        next_state["observer_phase"] = "STOPPED"
        decision = _decision(
            action="STOP",
            reason_code="SHUTDOWN_REQUESTED",
            observed_head=None,
            candidate_head=None,
            previous_live_head=previous_live,
            next_projection_state=state[
                "projection_state"
            ],
        )
        return next_state, decision

    raise ObserverTickError("unsupported event type")


def one_shot_tick(
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
) -> dict[str, Any]:
    previous = _clone(previous_state)
    event = _clone(normalized_input)

    _validate_state(previous)
    _validate_input(previous, event)

    next_state, decision = _apply_transition(
        previous,
        event,
    )
    next_state["last_event_sequence"] = event["sequence"]

    _validate_state(next_state)

    audit = {
        "schema": EVENT_SCHEMA,
        "sequence": event["sequence"],
        "event_type": event["event_type"],
        "previous_state_digest": _digest(previous),
        "input_digest": _digest(event),
        "decision_digest": _digest(decision),
        "next_state_digest": _digest(next_state),
        "reason_code": decision["reason_code"],
    }

    result = {
        "schema": RESULT_SCHEMA,
        "next_state": next_state,
        "decision": decision,
        "audit": audit,
    }

    _canonical_json_bytes(result)
    return result


def canonical_result_bytes(
    result: dict[str, Any],
) -> bytes:
    return _canonical_json_bytes(result)

~~~~

# SOURCE: P5-D2 OBSERVER TICK TESTS
Path: tests/obsidian_projection/test_observer_tick.py
~~~~
from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tools.obsidian_projection.observer_tick import (
    DECISION_SCHEMA,
    EVENT_SCHEMA,
    INPUT_SCHEMA,
    RESULT_SCHEMA,
    STATE_SCHEMA,
    ObserverTickError,
    canonical_result_bytes,
    make_initial_state,
    one_shot_tick,
)


H1 = "1" * 40
H2 = "2" * 40
H3 = "3" * 40
H4 = "4" * 40


def event(
    sequence: int,
    event_type: str,
    *,
    observed_head: str | None = None,
    transition_class: str | None = None,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": sequence,
        "observed_head": observed_head,
        "transition_class": transition_class,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }


def tick(
    state: dict,
    event_type: str,
    **kwargs,
) -> dict:
    payload = event(
        state["last_event_sequence"] + 1,
        event_type,
        **kwargs,
    )
    return one_shot_tick(state, payload)


def bootstrap() -> dict:
    state = make_initial_state()
    return tick(
        state,
        "BOOTSTRAP",
    )["next_state"]


def observe_initial(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "REMOTE_HEAD_OBSERVED",
        observed_head=head,
        transition_class="INITIAL",
    )["next_state"]


def begin_evaluation(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_STARTED",
        candidate_head=head,
    )["next_state"]


def qualify(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "EVALUATION_PASSED",
        candidate_head=head,
    )["next_state"]


def promote(
    state: dict,
    head: str = H1,
) -> dict:
    return tick(
        state,
        "PROMOTION_CONFIRMED",
        candidate_head=head,
    )["next_state"]


def make_current_state() -> dict:
    state = bootstrap()
    state = observe_initial(state, H1)
    state = begin_evaluation(state, H1)
    state = qualify(state, H1)
    state = promote(state, H1)
    return state


class ObserverTickTests(unittest.TestCase):
    def test_initial_state_is_canonical(self) -> None:
        state = make_initial_state()
        self.assertEqual(state["schema"], STATE_SCHEMA)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(
            state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            state["projection_state"],
            "MISSING",
        )
        self.assertEqual(state["pending_heads"], [])
        self.assertEqual(state["last_event_sequence"], 0)

    def test_bootstrap_changes_only_sequence(self) -> None:
        state = make_initial_state()
        result = tick(state, "BOOTSTRAP")
        next_state = result["next_state"]
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] = 1
        self.assertEqual(next_state, expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )
        self.assertEqual(
            result["decision"]["reason_code"],
            "BOOTSTRAP_ACCEPTED",
        )

    def test_bootstrap_rejects_noncanonical_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["remote_freshness"] = "KNOWN"
        with self.assertRaises(ObserverTickError):
            tick(state, "BOOTSTRAP")

    def test_initial_head_is_queued_exactly_once(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["latest_observed_head"],
            H1,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1],
        )
        self.assertEqual(
            next_state["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "MISSING",
        )
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )

    def test_initial_rejected_after_previous_observation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="INITIAL",
            )

    def test_same_head_is_strict_noop_for_queue(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        before_pending = copy.deepcopy(
            state["pending_heads"]
        )
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            before_pending,
        )
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_same_requires_previous_observed_equality(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_network_failure_from_current_becomes_stale(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["remote_freshness"],
            "UNKNOWN",
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            "NETWORK_UNAVAILABLE",
        )

    def test_same_head_restores_current_after_network_failure(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_OBSERVATION_FAILED",
            failure_code="NETWORK_UNAVAILABLE",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["remote_freshness"],
            "KNOWN",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "CURRENT",
        )

    def test_same_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="SAME",
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_new_remote_head_does_not_clear_blocked_state(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )["next_state"]
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        blocked_before = state["blocked_head"]
        failure_before = state["last_failure_code"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H3,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["blocked_head"],
            blocked_before,
        )
        self.assertEqual(
            next_state["last_failure_code"],
            failure_before,
        )
        self.assertEqual(
            next_state["latest_observed_head"],
            H3,
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )

    def test_fast_forward_preserves_existing_pending_fifo_without_active_evaluation(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        self.assertEqual(state["observer_phase"], "IDLE")
        self.assertEqual(state["pending_heads"], [H1])
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(next_state["observer_phase"], "IDLE")
        self.assertEqual(next_state["pending_heads"], [H1, H2])
        self.assertEqual(
            result["decision"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )
        self.assertEqual(result["decision"]["candidate_head"], H2)

    def test_fast_forward_queues_without_retargeting_active(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            next_state["pending_heads"],
            [H1, H2],
        )
        self.assertEqual(
            next_state["projection_state"],
            "STALE",
        )

    def test_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="NON_FAST_FORWARD",
            )

    def test_unknown_rejects_unchanged_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="UNKNOWN",
            )

    def test_fast_forward_requires_previous_observed_head(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="FAST_FORWARD",
            )

    def test_non_fast_forward_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="NON_FAST_FORWARD",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            next_state["blocked_head"],
            H2,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertNotIn(H2, next_state["pending_heads"])

    def test_unknown_ancestry_blocks_without_queueing(
        self,
    ) -> None:
        state = make_current_state()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="UNKNOWN",
        )
        self.assertEqual(
            result["decision"]["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )
        self.assertNotIn(
            H2,
            result["next_state"]["pending_heads"],
        )

    def test_evaluation_start_binds_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        result = tick(
            state,
            "EVALUATION_STARTED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["observer_phase"],
            "EVALUATING",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H1],
        )
        self.assertEqual(
            result["decision"]["candidate_head"],
            H1,
        )

    def test_evaluation_start_rejects_non_queue_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H2,
            )

    def test_evaluation_start_requires_idle(self) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "EVALUATION_STARTED",
                candidate_head=H1,
            )

    def test_evaluation_pass_advances_qualified_not_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["last_qualified_head"],
            H1,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            next_state["pending_heads"],
            [],
        )
        self.assertEqual(
            next_state["observer_phase"],
            "CANDIDATE_PENDING",
        )

    def test_evaluation_pass_preserves_newer_queued_head(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        result = tick(
            state,
            "EVALUATION_PASSED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )
        self.assertEqual(
            result["next_state"]["last_qualified_head"],
            H1,
        )

    def test_evaluation_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "EVALUATION_FAILED",
            candidate_head=H2,
            failure_code="CANDIDATE_INVALID",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )
        self.assertEqual(
            result["next_state"]["blocked_head"],
            H2,
        )

    def test_promotion_confirmation_is_logical_only(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["live_projection_head"],
            H1,
        )
        self.assertEqual(
            next_state["projection_state"],
            "CURRENT",
        )
        self.assertEqual(
            result["decision"][
                "production_write_authorized"
            ],
            False,
        )
        self.assertEqual(
            result["decision"][
                "automatic_promotion_authorized"
            ],
            False,
        )

    def test_promotion_confirmation_stays_stale_if_newer_remote(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = qualify(state, H1)
        result = tick(
            state,
            "PROMOTION_CONFIRMED",
            candidate_head=H1,
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            H1,
        )
        self.assertEqual(
            result["next_state"]["latest_observed_head"],
            H2,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "STALE",
        )
        self.assertEqual(
            result["next_state"]["pending_heads"],
            [H2],
        )

    def test_promotion_rejects_nonqualified_candidate(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = begin_evaluation(state, H1)
        state = qualify(state, H1)
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "PROMOTION_CONFIRMED",
                candidate_head=H2,
            )

    def test_promotion_failure_preserves_live_head(
        self,
    ) -> None:
        state = make_current_state()
        state = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H2,
            transition_class="FAST_FORWARD",
        )["next_state"]
        state = begin_evaluation(state, H2)
        state = qualify(state, H2)
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "PROMOTION_FAILED",
            candidate_head=H2,
            failure_code="POINTER_NOT_CONFIRMED",
        )
        self.assertEqual(
            result["next_state"]["live_projection_head"],
            live_before,
        )
        self.assertEqual(
            result["next_state"]["projection_state"],
            "BLOCKED",
        )

    def test_lock_contended_changes_only_sequence(
        self,
    ) -> None:
        state = make_current_state()
        expected = copy.deepcopy(state)
        expected["last_event_sequence"] += 1
        result = tick(
            state,
            "LOCK_CONTENDED",
            failure_code="LOCK_CONTENDED",
        )
        self.assertEqual(result["next_state"], expected)
        self.assertEqual(
            result["decision"]["action"],
            "NOOP",
        )

    def test_shutdown_preserves_pending_and_live(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        pending_before = copy.deepcopy(
            state["pending_heads"]
        )
        live_before = state["live_projection_head"]
        result = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )
        next_state = result["next_state"]
        self.assertEqual(
            next_state["observer_phase"],
            "STOPPED",
        )
        self.assertEqual(
            next_state["pending_heads"],
            pending_before,
        )
        self.assertEqual(
            next_state["live_projection_head"],
            live_before,
        )

    def test_stopped_state_accepts_no_further_event(
        self,
    ) -> None:
        state = observe_initial(bootstrap(), H1)
        state = tick(
            state,
            "SHUTDOWN_REQUESTED",
        )["next_state"]
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_input_sequence_skip_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 2,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_input_sequence_replay_is_rejected(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"],
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_boolean_sequence_is_rejected(self) -> None:
        state = make_initial_state()
        payload = event(
            True,
            "BOOTSTRAP",
        )
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_extra_input_field_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["unexpected"] = "x"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_wrong_input_schema_is_rejected(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        payload["schema"] = "WRONG"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(state, payload)

    def test_remote_observed_requires_head(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                transition_class="INITIAL",
            )

    def test_remote_observed_requires_transition_class(
        self,
    ) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
            )

    def test_invalid_repository_is_rejected(self) -> None:
        state = make_initial_state()
        state["repository"] = "wrong/repo"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_invalid_branch_is_rejected(self) -> None:
        state = make_initial_state()
        state["branch"] = "main"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_uppercase_head_is_rejected(self) -> None:
        state = bootstrap()
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head="A" * 40,
                transition_class="INITIAL",
            )

    def test_duplicate_pending_heads_are_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["pending_heads"] = [H1, H1]
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_current_unknown_freshness_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["remote_freshness"] = "UNKNOWN"
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H1,
                transition_class="SAME",
            )

    def test_current_head_mismatch_is_rejected(
        self,
    ) -> None:
        state = make_current_state()
        state["latest_observed_head"] = H2
        with self.assertRaises(ObserverTickError):
            tick(
                state,
                "REMOTE_HEAD_OBSERVED",
                observed_head=H2,
                transition_class="SAME",
            )

    def test_evaluating_empty_queue_is_rejected(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "EVALUATING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_candidate_pending_requires_qualified_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "CANDIDATE_PENDING"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_consistent_block_state(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "STALE"
        state["blocked_head"] = H1
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_blocked_phase_requires_blocked_head(
        self,
    ) -> None:
        state = make_initial_state()
        state["observer_phase"] = "BLOCKED"
        state["projection_state"] = "BLOCKED"
        state["last_failure_code"] = "BLOCKED_FOR_TEST"
        with self.assertRaises(ObserverTickError):
            one_shot_tick(
                state,
                event(1, "BOOTSTRAP"),
            )

    def test_caller_inputs_are_not_mutated(self) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        state_before = copy.deepcopy(state)
        payload_before = copy.deepcopy(payload)
        one_shot_tick(state, payload)
        self.assertEqual(state, state_before)
        self.assertEqual(payload, payload_before)

    def test_result_schemas_and_authority_flags(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        self.assertEqual(result["schema"], RESULT_SCHEMA)
        self.assertEqual(
            result["next_state"]["schema"],
            STATE_SCHEMA,
        )
        self.assertEqual(
            result["decision"]["schema"],
            DECISION_SCHEMA,
        )
        self.assertEqual(
            result["audit"]["schema"],
            EVENT_SCHEMA,
        )
        self.assertFalse(
            result["decision"][
                "automatic_promotion_authorized"
            ]
        )
        self.assertFalse(
            result["decision"][
                "production_write_authorized"
            ]
        )

    def test_same_inputs_are_byte_deterministic(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        first = one_shot_tick(state, payload)
        second = one_shot_tick(state, payload)
        self.assertEqual(first, second)
        self.assertEqual(
            canonical_result_bytes(first),
            canonical_result_bytes(second),
        )

    def test_canonical_result_is_compact_sorted_lf(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        raw = canonical_result_bytes(result)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertNotIn(b": ", raw)
        self.assertNotIn(b", ", raw)
        decoded = json.loads(raw.decode("utf-8"))
        self.assertEqual(decoded, result)

    def test_audit_digests_match_canonical_values(
        self,
    ) -> None:
        state = bootstrap()
        payload = event(
            state["last_event_sequence"] + 1,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        result = one_shot_tick(state, payload)

        def digest(value: dict) -> str:
            raw = (
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                )
                + "\n"
            ).encode("utf-8")
            return hashlib.sha256(raw).hexdigest()

        audit = result["audit"]
        self.assertEqual(
            audit["previous_state_digest"],
            digest(state),
        )
        self.assertEqual(
            audit["input_digest"],
            digest(payload),
        )
        self.assertEqual(
            audit["decision_digest"],
            digest(result["decision"]),
        )
        self.assertEqual(
            audit["next_state_digest"],
            digest(result["next_state"]),
        )

    def test_audit_has_no_volatile_host_fields(
        self,
    ) -> None:
        state = bootstrap()
        result = tick(
            state,
            "REMOTE_HEAD_OBSERVED",
            observed_head=H1,
            transition_class="INITIAL",
        )
        audit = result["audit"]
        for forbidden in (
            "observed_at",
            "timestamp",
            "host_id",
            "process_id",
            "pid",
            "path",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, audit)


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-D4 BOUNDED LOOP CONTRACT
Path: tools/obsidian_projection/p5d4_bounded_observer_loop_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_P5D4_BOUNDED_OBSERVER_LOOP_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "frontier": "P5-D4-BOUNDED-OBSERVER-LOOP-CANDIDATE",
  "title": "BOUNDED_OBSERVER_LOOP_CONTRACT",
  "purpose": "Define a finite, persistent and auditable orchestration envelope around already-qualified P5-D2/P5-D3 one-shot primitives without creating implicit promotion authority, permanent background execution, or P5-E near-real-time authority.",
  "qualified_predecessors": {
    "p5d1_observer_core_contract_blob": "a20999ae991e07447e25ecd1592964f2d333449b",
    "p5d2_one_shot_contract_blob": "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
    "p5d2_observer_tick_blob": "fd212f61ec38332b677110f40265638af55a73e2",
    "p5d3d_finite_evaluator_contract_blob": "b6c17167875874db30a575be95e8e6aa33d630dd",
    "p5d3d_finite_evaluator_blob": "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
    "p5d3e_real_exact_head_sandbox_contract_blob": "ae4b1691fae16fcd1616e265a089670b9654db4a",
    "p5d3e_verifier_blob": "bd7f63b08432a53eaff5deeb2147396eb60d723f",
    "p5d3f_handoff_contract_blob": "64744325251db350d26c0269090ce62d5fa5f2e8",
    "p5d3f_handoff_blob": "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60",
    "p5d3g_live_publication_contract_blob": "64997ddd9977229961387f66af4de356c045c0ac",
    "p5d3g_live_publication_blob": "956ccb7274cea366b1a414df5a9239cbf580e3bf",
    "p5d3g_stage_b_gate_contract_blob": "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead",
    "p5d3g_stage_b_prestate_rebind_amendment_blob": "441fea40d33aa85dcfc6305d4d32cef39c42388e",
    "p5d3g_stage_b_runtime_blob": "077ea7a428f90d64122f15fe6b52f342f329f7b6"
  },
  "core_authority_model": {
    "observer_semantic_state_mutation_authority": "P5D2_ONE_SHOT_TICK_ONLY",
    "direct_observer_state_mutation_forbidden": true,
    "p5d3_primitive_reimplementation_forbidden": true,
    "loop_authority_is_not_promotion_authority": true,
    "qualified_candidate_requires_separate_promotion_authority": true,
    "candidate_pending_without_separate_authority_result": "PROMOTION_AUTHORITY_REQUIRED",
    "automatic_live_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "historical_stage_a_or_stage_b_authority_reuse_forbidden": true
  },
  "schemas": {
    "loop_plan": "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1",
    "loop_checkpoint": "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1",
    "loop_event": "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1",
    "ownership_record": "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1",
    "reconciliation_report": "ATDS_OBSIDIAN_P5D4_RECONCILIATION_REPORT_V0_1"
  },
  "bounded_loop_envelope": {
    "every_run_requires_explicit_canonical_plan": true,
    "plan_digest_required": true,
    "unbounded_defaults_forbidden": true,
    "required_limits": {
      "max_cycles": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_remote_observations": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_evaluations": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      },
      "max_pending_heads": {
        "type": "POSITIVE_INTEGER",
        "minimum": 1
      },
      "max_consecutive_failures": {
        "type": "NONNEGATIVE_INTEGER",
        "minimum": 0
      }
    },
    "cycle_budget_consumed_exactly_once_per_started_cycle": true,
    "budget_check_required_before_starting_next_cycle": true,
    "bound_reached_must_not_inject_p5d2_shutdown_event": true,
    "bound_reached_is_runner_stop_not_semantic_state_transition": true,
    "loop_construct_without_verified_budget_forbidden": true,
    "allowed_terminal_reasons": [
      "BOUND_REACHED",
      "NO_PENDING_WORK",
      "BLOCKED_REQUIRES_ADJUDICATION",
      "PROMOTION_AUTHORITY_REQUIRED",
      "SHUTDOWN_REQUESTED",
      "LOCK_CONTENDED",
      "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
      "RECONCILIATION_REQUIRED",
      "FATAL_INCONSISTENCY"
    ],
    "terminal_reason_must_be_persisted": true,
    "new_cycle_after_terminal_reason_forbidden": true
  },
  "durable_observer_state_checkpoint": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "candidate_root_expression": "%LOCALAPPDATA%\\ATDS-OBSIDIAN-PROJECTION\\P5D4",
    "inside_real_vault_forbidden": true,
    "inside_canonical_repository_forbidden": true,
    "canonical_json_required": true,
    "utf8_required": true,
    "terminal_lf_required": true,
    "sha256_required": true,
    "required_fields": [
      "schema",
      "loop_plan_digest_sha256",
      "observer_state",
      "observer_state_digest_sha256",
      "last_event_sequence",
      "last_event_digest_sha256",
      "checkpoint_generation"
    ],
    "observer_state_must_validate_under_p5d2": true,
    "last_event_sequence_must_equal_observer_state_last_event_sequence": true,
    "volatile_host_data_excluded_from_observer_state_digest": [
      "pid",
      "hostname",
      "wall_clock_time",
      "absolute_runtime_path",
      "process_start_time"
    ],
    "commit_protocol": [
      "BUILD_NEXT_STATE_ONLY_VIA_P5D2_ONE_SHOT_TICK",
      "BUILD_CANONICAL_LOOP_EVENT",
      "APPEND_AND_DURABLY_FLUSH_LOOP_EVENT",
      "WRITE_CHECKPOINT_TO_SIBLING_TEMP",
      "DURABLY_FLUSH_CHECKPOINT_TEMP",
      "ATOMIC_REPLACE_CHECKPOINT",
      "VERIFY_CHECKPOINT_READ_AFTER_WRITE"
    ],
    "checkpoint_may_not_be_committed_before_corresponding_event": true,
    "direct_in_place_checkpoint_overwrite_forbidden": true
  },
  "append_only_observer_event_log": {
    "required": true,
    "location_class": "LOCALAPPDATA_OUTSIDE_VAULT",
    "format": "CANONICAL_JSONL",
    "append_only": true,
    "truncate_forbidden": true,
    "rewrite_prior_record_forbidden": true,
    "durable_flush_required_before_checkpoint_replace": true,
    "every_accepted_p5d2_tick_requires_record": true,
    "required_fields": [
      "schema",
      "sequence",
      "loop_id",
      "cycle_index",
      "normalized_input",
      "p5d2_audit",
      "previous_state_digest_sha256",
      "next_state_digest_sha256",
      "previous_record_digest_sha256",
      "record_digest_sha256",
      "record_origin"
    ],
    "record_origin_allowed": [
      "LIVE_BOUNDED_LOOP",
      "EVIDENCE_RECONSTRUCTION"
    ],
    "hash_chain_required": true,
    "sequence_strictly_monotonic": true,
    "duplicate_sequence_forbidden": true,
    "unterminated_or_noncanonical_tail_requires_reconciliation": true,
    "event_log_is_evidence_not_source_authority": true
  },
  "queue_capacity_policy": {
    "runtime_capacity_source": "loop_plan.max_pending_heads",
    "fifo_required": true,
    "unique_heads_required": true,
    "silent_drop_forbidden": true,
    "silent_reorder_forbidden": true,
    "latest_only_replacement_forbidden": true,
    "direct_queue_mutation_outside_p5d2_forbidden": true,
    "coalescing_authorized": false,
    "reason_coalescing_closed": "P5-D2 has no qualified queue-coalescing semantic event in V0.1",
    "preflight_capacity_check_required_before_event_that_would_append": true,
    "capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "capacity_exhausted_must_not_feed_mutating_event_to_p5d2": true,
    "active_evaluation_candidate_retargeting_forbidden": true
  },
  "single_instance_ownership": {
    "required": true,
    "scope": "P5D4_CONTROL_STATE_ROOT",
    "exclusive_ownership_record_required": true,
    "ownership_record_outside_vault": true,
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "second_instance_may_observe_only": false,
    "second_instance_may_advance_sequence": false,
    "second_instance_may_modify_checkpoint": false,
    "second_instance_may_append_event": false,
    "second_instance_may_start_evaluation": false,
    "stale_or_ambiguous_lock_auto_steal_authorized": false,
    "stale_or_ambiguous_lock_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "volatile_ownership_metadata_must_not_enter_semantic_observer_digest": true
  },
  "restart_reconciliation_protocol": {
    "required_before_any_loop_continuation_after_restart": true,
    "authority_order": [
      "GITHUB_REMOTE_BRANCH_SOURCE_AUTHORITY",
      "VERIFIED_PHYSICAL_CURRENT_PUBLICATION_FACT",
      "P5D4_CHECKPOINT_DERIVED_OPERATIONAL_STATE",
      "P5D4_EVENT_LOG_AUDIT_EVIDENCE"
    ],
    "fresh_remote_read_only_observation_required": true,
    "physical_current_verification_required": true,
    "checkpoint_validation_required_if_present": true,
    "event_log_tail_validation_required_if_present": true,
    "allowed_checkpoint_log_relation": [
      "EXACTLY_ALIGNED",
      "LOG_EXACTLY_ONE_RECORD_AHEAD_WITH_REPLAYABLE_TRANSITION"
    ],
    "checkpoint_ahead_of_log_forbidden": true,
    "log_more_than_one_record_ahead_forbidden": true,
    "one_record_ahead_recovery": {
      "requires_previous_state_digest_match_checkpoint": true,
      "requires_deterministic_replay_via_p5d2_one_shot_tick": true,
      "requires_replayed_next_state_digest_match_log": true,
      "action": "ADVANCE_CHECKPOINT_ONLY_AFTER_REPLAY_MATCH"
    },
    "current_head_checkpoint_live_head_mismatch_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "event_tail_checkpoint_sequence_mismatch_unrecoverable_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "remote_non_fast_forward_or_unknown_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "restart_may_not_repeat_completed_evaluation_without_evidence": true,
    "restart_may_not_repeat_completed_promotion_without_evidence": true,
    "no_checkpoint_no_log_current_absent_result": "INITIALIZE_CANONICAL_P5D2_STATE",
    "no_checkpoint_no_log_current_present_result": "EVIDENCE_RECONSTRUCTION_REQUIRED",
    "evidence_reconstruction": {
      "direct_state_assignment_forbidden": true,
      "must_start_from_p5d2_make_initial_state": true,
      "must_use_p5d2_one_shot_tick_for_each_semantic_transition": true,
      "verified_current_identity_required": true,
      "matching_p5d3g_physical_and_logical_receipts_required": true,
      "reconstructed_event_records_must_use_origin": "EVIDENCE_RECONSTRUCTION",
      "reconstruction_must_not_claim_new_evaluation_or_new_publication_execution": true,
      "missing_or_ambiguous_p5d3g_evidence_result": "BLOCKED_REQUIRES_ADJUDICATION"
    }
  },
  "observation_adapter_boundary": {
    "remote_io_outside_p5d2_required": true,
    "normalized_event_injection_required": true,
    "one_shot_tick_network_io_remains_forbidden": true,
    "real_remote_observation_may_use_read_only_git": true,
    "time_based_polling_in_p5d4_v0_1_authorized": false,
    "sleep_or_timer_authorized": false,
    "p5e_owns_near_real_time_polling_qualification": true
  },
  "evaluation_orchestration": {
    "evaluation_may_start_only_on_p5d2_action": "START_EXACT_HEAD_EVALUATION",
    "evaluation_candidate_must_equal_queue_head": true,
    "candidate_head_frozen_for_entire_finite_evaluation": true,
    "new_remote_head_may_be_observed_while_evaluation_active_only_as_separately_queued_work": true,
    "active_evaluation_retarget_forbidden": true,
    "finite_evaluator_reuse_required": true,
    "qualified_evaluator_reimplementation_forbidden": true,
    "blocked_and_rejected_semantics_must_remain_distinct": true,
    "evaluation_result_must_reenter_state_only_via_p5d2_one_shot_tick": true
  },
  "promotion_boundary": {
    "candidate_pending_is_terminal_for_automatic_p5d4_orchestration": true,
    "required_stop_reason_without_separate_authority": "PROMOTION_AUTHORITY_REQUIRED",
    "p5d3f_or_p5d3g_invocation_from_loop_without_separate_authority_forbidden": true,
    "automatic_stage_a_authority_forbidden": true,
    "automatic_stage_b_authority_forbidden": true,
    "old_authorization_reuse_forbidden": true,
    "promotion_confirmed_may_enter_observer_state_only_from_verified_external_promotion_evidence": true,
    "promotion_failed_may_enter_observer_state_only_from_verified_external_failure_evidence": true
  },
  "failure_and_stop_semantics": {
    "fail_closed_default": true,
    "state_or_log_corruption_result": "FATAL_INCONSISTENCY",
    "unexpected_exception_result": "FATAL_INCONSISTENCY",
    "network_failure_must_not_create_current_claim": true,
    "last_known_good_live_projection_preserved_on_failure": true,
    "loop_stop_must_not_delete_checkpoint_or_event_log": true,
    "loop_stop_must_not_delete_last_known_good_generation": true
  },
  "contract_only_boundary": {
    "contract_and_tests_only": true,
    "loop_runtime_creation_authorized": false,
    "loop_runtime_modification_authorized": false,
    "bounded_loop_execution_authorized": false,
    "repeated_real_polling_authorized": false,
    "sleep_authorized": false,
    "timer_authorized": false,
    "permanent_daemon_authorized": false,
    "windows_startup_authorized": false,
    "scheduled_task_authorized": false,
    "windows_service_authorized": false,
    "real_vault_mutation_authorized": false,
    "automatic_publication_authorized": false,
    "implicit_stage_a_authority_authorized": false,
    "implicit_stage_b_authority_authorized": false,
    "p5e_authorized": false,
    "p6_authorized": false
  },
  "required_breakers": [
    "UNBOUNDED_LOOP_PLAN_ACCEPTED",
    "ZERO_OR_NEGATIVE_MAX_CYCLES_ACCEPTED",
    "CYCLE_STARTED_AFTER_BUDGET_EXHAUSTED",
    "BOUND_REACHED_INJECTS_P5D2_SHUTDOWN_EVENT",
    "NEW_CYCLE_AFTER_TERMINAL_REASON",
    "DIRECT_OBSERVER_STATE_MUTATION",
    "CHECKPOINT_INSIDE_REAL_VAULT",
    "CHECKPOINT_INSIDE_CANONICAL_REPOSITORY",
    "CHECKPOINT_DIRECT_IN_PLACE_OVERWRITE",
    "CHECKPOINT_COMMITTED_BEFORE_EVENT_APPEND",
    "CHECKPOINT_STATE_DIGEST_MISMATCH",
    "CHECKPOINT_SEQUENCE_DIFFERS_FROM_OBSERVER_STATE",
    "VOLATILE_HOST_DATA_LAUNDERED_INTO_SEMANTIC_DIGEST",
    "EVENT_LOG_TRUNCATED",
    "EVENT_LOG_PRIOR_RECORD_REWRITTEN",
    "EVENT_SEQUENCE_DUPLICATED",
    "EVENT_SEQUENCE_SKIPPED",
    "EVENT_HASH_CHAIN_BROKEN",
    "CHECKPOINT_AHEAD_OF_EVENT_LOG",
    "EVENT_LOG_MORE_THAN_ONE_RECORD_AHEAD",
    "ONE_RECORD_AHEAD_REPLAY_DIGEST_MISMATCH",
    "QUEUE_OVERFLOW_SILENT_DROP",
    "QUEUE_OVERFLOW_LATEST_ONLY_REPLACEMENT",
    "QUEUE_REORDERED",
    "QUEUE_DUPLICATE_HEAD",
    "QUEUE_MUTATED_OUTSIDE_P5D2",
    "QUEUE_COALESCING_WITHOUT_QUALIFIED_P5D2_EVENT",
    "ACTIVE_EVALUATION_RETARGETED",
    "SECOND_LOOP_RUNNER_ADVANCES_SEQUENCE",
    "SECOND_LOOP_RUNNER_WRITES_CHECKPOINT",
    "SECOND_LOOP_RUNNER_STARTS_EVALUATION",
    "STALE_LOCK_AUTO_STOLEN",
    "RESTART_CONTINUES_WITHOUT_RECONCILIATION",
    "CURRENT_DIFFERS_FROM_CHECKPOINT_LIVE_HEAD",
    "CHECKPOINT_LOG_TAIL_UNRECOVERABLE_MISMATCH_CONTINUES",
    "RESTART_REPEATS_COMPLETED_EVALUATION",
    "RESTART_REPEATS_COMPLETED_PROMOTION",
    "BOOTSTRAP_CURRENT_PRESENT_DIRECT_STATE_ASSIGNMENT",
    "BOOTSTRAP_CURRENT_PRESENT_WITHOUT_P5D3G_EVIDENCE",
    "EVIDENCE_RECONSTRUCTION_CLAIMS_NEW_PUBLICATION",
    "SAME_HEAD_TRIGGERS_EVALUATION",
    "REMOTE_NETWORK_FAILURE_MARKS_CURRENT",
    "NON_FAST_FORWARD_CONTINUES_AUTOMATICALLY",
    "UNKNOWN_ANCESTRY_CONTINUES_AUTOMATICALLY",
    "BLOCKED_RESULT_RELABELED_REJECTED",
    "REJECTED_RESULT_RELABELED_BLOCKED",
    "P5D3_FINITE_EVALUATOR_REIMPLEMENTED",
    "CANDIDATE_PENDING_AUTO_PUBLISHED",
    "P5D3F_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "P5D3G_CALLED_WITHOUT_SEPARATE_AUTHORITY",
    "OLD_STAGE_A_AUTHORITY_REUSED",
    "OLD_STAGE_B_AUTHORITY_REUSED",
    "PROMOTION_CONFIRMED_WITHOUT_VERIFIED_EXTERNAL_EVIDENCE",
    "LOOP_PUSHES_TO_GITHUB",
    "LOOP_COMMITS_CANONICAL_REPOSITORY",
    "LOOP_MUTATES_CANONICAL_WORKTREE",
    "LOOP_OVERWRITES_HUMAN_VIEWS",
    "LOOP_MODIFIES_OBSIDIAN_CONFIG",
    "REAL_VAULT_WRITE_SURFACE_INTRODUCED",
    "PERMANENT_DAEMON_SURFACE_INTRODUCED",
    "SLEEP_OR_TIMER_SURFACE_INTRODUCED",
    "WINDOWS_STARTUP_SURFACE_INTRODUCED",
    "SCHEDULED_TASK_SURFACE_INTRODUCED",
    "WINDOWS_SERVICE_SURFACE_INTRODUCED",
    "P5E_AUTHORITY_LEAK",
    "P6_AUTHORITY_LEAK"
  ],
  "qualification_requirements": {
    "static_contract_tests_required": true,
    "predecessor_pin_tests_required": true,
    "breaker_coverage_tests_required": true,
    "directly_affected_predecessor_contract_tests_required": [
      "P5D1_CONTINUOUS_OBSERVER_CORE_CONTRACT",
      "P5D2_ONE_SHOT_OBSERVER_TICK_CONTRACT",
      "P5D3A_CANDIDATE_EVALUATION_CONTRACT",
      "P5D3D_FINITE_CANDIDATE_EVALUATOR_CONTRACT",
      "P5D3G_LIVE_PUBLICATION_TRANSACTION_CONTRACT"
    ],
    "runtime_tests_required": false,
    "real_loop_execution_required": false,
    "real_vault_access_required": false
  },
  "next_gate": {
    "after_contract_qualification": "P5-D4-BOUNDED-OBSERVER-LOOP-RUNTIME-IMPLEMENTATION-CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
    "p6": "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
    "mandatory_human_stop_before_runtime": true
  }
}

~~~~

# SOURCE: P5-D4 BOUNDED LOOP RUNTIME
Path: tools/obsidian_projection/p5d4_bounded_observer_loop.py
~~~~
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

from .observer_tick import (
    INPUT_SCHEMA,
    _validate_state,
    make_initial_state,
    one_shot_tick,
)

PLAN_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_PLAN_V0_1"
CHECKPOINT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_CHECKPOINT_V0_1"
EVENT_SCHEMA = "ATDS_OBSIDIAN_P5D4_LOOP_EVENT_V0_1"
OWNERSHIP_SCHEMA = "ATDS_OBSIDIAN_P5D4_OWNERSHIP_RECORD_V0_1"
EVIDENCE_SCHEMA = "ATDS_OBSIDIAN_P5D4_VERIFIED_PUBLICATION_EVIDENCE_V0_1"
RUN_RESULT_SCHEMA = "ATDS_OBSIDIAN_P5D4_BOUNDED_LOOP_RESULT_V0_1"

_HEAD_RE = re.compile(r"^[0-9a-f]{40}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PLAN_KEYS = frozenset({
    "schema","loop_id","max_cycles","max_remote_observations",
    "max_evaluations","max_pending_heads","max_consecutive_failures",
    "plan_digest_sha256",
})

class P5D4RuntimeError(RuntimeError):
    pass

class LoopPlanError(P5D4RuntimeError):
    pass

class PersistenceError(P5D4RuntimeError):
    pass

class ReconciliationError(P5D4RuntimeError):
    pass

class OwnershipError(P5D4RuntimeError):
    pass

class OwnershipContended(OwnershipError):
    pass

class QueueCapacityError(P5D4RuntimeError):
    pass

class ControlRootBindingError(P5D4RuntimeError):
    pass

def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"), allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise PersistenceError("value is not canonical JSON") from exc
    return (text + "\n").encode("utf-8")

def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()

def _is_int(value: Any, minimum: int) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value >= minimum

def _is_head(value: Any) -> bool:
    return isinstance(value, str) and _HEAD_RE.fullmatch(value) is not None

def _is_sha256(value: Any) -> bool:
    return isinstance(value, str) and _SHA256_RE.fullmatch(value) is not None

def _plan_payload(plan: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in plan.items() if key != "plan_digest_sha256"}

def make_loop_plan(
    *,
    loop_id: str,
    max_cycles: int,
    max_remote_observations: int,
    max_evaluations: int,
    max_pending_heads: int,
    max_consecutive_failures: int,
) -> dict[str, Any]:
    plan = {
        "schema": PLAN_SCHEMA,
        "loop_id": loop_id,
        "max_cycles": max_cycles,
        "max_remote_observations": max_remote_observations,
        "max_evaluations": max_evaluations,
        "max_pending_heads": max_pending_heads,
        "max_consecutive_failures": max_consecutive_failures,
    }
    plan["plan_digest_sha256"] = _digest(plan)
    return validate_loop_plan(plan)

def validate_loop_plan(plan: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(plan, dict) or frozenset(plan) != _PLAN_KEYS:
        raise LoopPlanError("loop plan fields mismatch")
    if plan["schema"] != PLAN_SCHEMA:
        raise LoopPlanError("loop plan schema mismatch")
    loop_id = plan["loop_id"]
    if not isinstance(loop_id, str) or not loop_id or loop_id.strip() != loop_id:
        raise LoopPlanError("invalid loop_id")
    for field, minimum in (
        ("max_cycles", 1),
        ("max_remote_observations", 1),
        ("max_evaluations", 0),
        ("max_pending_heads", 1),
        ("max_consecutive_failures", 0),
    ):
        if not _is_int(plan[field], minimum):
            raise LoopPlanError(f"invalid {field}")
    expected = _digest(_plan_payload(plan))
    if plan["plan_digest_sha256"] != expected:
        raise LoopPlanError("loop plan digest mismatch")
    return json.loads(_canonical_bytes(plan).decode("utf-8"))

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _resolved(path: Path) -> Path:
    try:
        return Path(path).resolve(strict=False)
    except OSError as exc:
        raise P5D4RuntimeError("path resolution unavailable") from exc

def _intersects(first: Path, second: Path) -> bool:
    return (
        first == second
        or first in second.parents
        or second in first.parents
    )

def _normcase_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(str(path)))

def _path_is_within(path: Path, anchor: Path) -> bool:
    candidate = _normcase_path(path)
    parent = _normcase_path(anchor)
    try:
        return os.path.commonpath([candidate, parent]) == parent
    except ValueError:
        return False

def _existing_chain_has_reparse_point(path: Path) -> bool:
    current = Path(path)
    visited: set[str] = set()
    for _ in range(512):
        key = _normcase_path(current)
        if key in visited:
            raise ControlRootBindingError("control root path chain loop detected")
        visited.add(key)
        try:
            if current.exists() or current.is_symlink():
                info = os.lstat(current)
                attributes = getattr(info, "st_file_attributes", 0)
                reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
                if current.is_symlink() or (reparse_flag and attributes & reparse_flag):
                    return True
                is_junction = getattr(current, "is_junction", None)
                if callable(is_junction) and is_junction():
                    return True
        except OSError as exc:
            raise ControlRootBindingError(
                "control root path chain inspection unavailable"
            ) from exc
        if current.parent == current:
            return False
        current = current.parent
    raise ControlRootBindingError("control root path depth exceeds bound")

def _userprofile_root() -> Path:
    value = os.environ.get("USERPROFILE")
    if not isinstance(value, str) or not value.strip():
        raise ControlRootBindingError("USERPROFILE unavailable")
    profile = Path(value)
    if not profile.is_absolute():
        raise ControlRootBindingError("USERPROFILE is not absolute")
    return _resolved(profile)

def canonical_production_control_root() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "OBSIDIAN-PROJECTION" / "P5D4"

def _qualification_control_anchor() -> Path:
    return _userprofile_root() / "ATDS-CONTROL" / "_QUALIFICATION"

def resolve_and_validate_control_root(root: Path) -> Path:
    requested = Path(root)
    if not requested.is_absolute():
        raise ControlRootBindingError("control root must be absolute")
    if _existing_chain_has_reparse_point(requested):
        raise ControlRootBindingError(
            "control root path chain contains reparse point"
        )

    resolved = _resolved(requested)
    canonical = _resolved(canonical_production_control_root())
    qualification = _resolved(_qualification_control_anchor())
    temp_root = _resolved(Path(tempfile.gettempdir()))

    requested_norm = _normcase_path(resolved)
    canonical_norm = _normcase_path(canonical)
    is_production = requested_norm == canonical_norm
    is_qualification = _path_is_within(resolved, qualification)
    is_temp = _path_is_within(resolved, temp_root)

    if not (is_production or is_qualification or is_temp):
        raise ControlRootBindingError(
            "control root is outside canonical or synthetic qualification namespaces"
        )

    if is_production:
        localappdata = os.environ.get("LOCALAPPDATA")
        appdata = os.environ.get("APPDATA")
        for forbidden in (localappdata, appdata):
            if isinstance(forbidden, str) and forbidden.strip():
                if _path_is_within(canonical, _resolved(Path(forbidden))):
                    raise ControlRootBindingError(
                        "production control root depends on AppData"
                    )
        lowered = _normcase_path(canonical)
        if (
            os.path.normcase("\\packages\\") in lowered
            or os.path.normcase("\\localcache\\") in lowered
        ):
            raise ControlRootBindingError(
                "production control root is Store-redirectable"
            )
        return canonical

    return resolved

def _validate_control_root(
    root: Path,
    *,
    forbidden_roots: Iterable[Path] = (),
) -> Path:
    resolved = resolve_and_validate_control_root(root)
    protected = (_resolved(_repo_root()),) + tuple(_resolved(x) for x in forbidden_roots)
    if any(_intersects(resolved, item) for item in protected):
        raise P5D4RuntimeError("control root intersects protected root")
    try:
        resolved.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise P5D4RuntimeError("control root unavailable") from exc
    if not resolved.is_dir():
        raise P5D4RuntimeError("control root is not a directory")
    return resolved

def _write_durable(path: Path, raw: bytes, *, exclusive: bool = False) -> None:
    flags = os.O_WRONLY | os.O_CREAT
    flags |= os.O_EXCL if exclusive else os.O_TRUNC
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(fd)
def acquire_ownership(
    control_root: Path,
    *,
    loop_id: str,
    owner_token: str,
) -> dict[str, Any]:
    root = _validate_control_root(control_root)
    if not isinstance(loop_id, str) or not loop_id:
        raise OwnershipError("invalid loop id")
    if not isinstance(owner_token, str) or not owner_token:
        raise OwnershipError("invalid owner token")
    record = {
        "schema": OWNERSHIP_SCHEMA,
        "loop_id": loop_id,
        "owner_token": owner_token,
    }
    path = root / "ownership.lock"
    try:
        _write_durable(path, _canonical_bytes(record), exclusive=True)
    except FileExistsError as exc:
        raise OwnershipContended("ownership already held") from exc
    return record

def release_ownership(control_root: Path, ownership: dict[str, Any]) -> None:
    root = _validate_control_root(control_root)
    path = root / "ownership.lock"
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise OwnershipError("ownership record unavailable") from exc
    try:
        current = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise OwnershipError("ownership record invalid") from exc
    if raw != _canonical_bytes(current) or current != ownership:
        raise OwnershipError("ownership mismatch")
    try:
        path.unlink()
    except OSError as exc:
        raise OwnershipError("ownership release failed") from exc

def _event_record_digest(record: dict[str, Any]) -> str:
    body = dict(record)
    body.pop("record_digest_sha256", None)
    return _digest(body)

def load_event_log(control_root: Path) -> list[dict[str, Any]]:
    root = _validate_control_root(control_root)
    path = root / "observer-events.jsonl"
    if not path.exists():
        return []
    raw = path.read_bytes()
    if not raw:
        return []
    if not raw.endswith(b"\n"):
        raise PersistenceError("event log has unterminated record")
    records: list[dict[str, Any]] = []
    previous_digest: str | None = None
    expected_sequence = 1
    for line in raw.splitlines(keepends=True):
        try:
            record = json.loads(line.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PersistenceError("event log record invalid") from exc
        if line != _canonical_bytes(record):
            raise PersistenceError("event log record noncanonical")
        required = {
            "schema","sequence","loop_id","cycle_index","normalized_input",
            "p5d2_audit","previous_state_digest_sha256",
            "next_state_digest_sha256","previous_record_digest_sha256",
            "record_digest_sha256","record_origin",
        }
        if set(record) != required or record.get("schema") != EVENT_SCHEMA:
            raise PersistenceError("event log fields mismatch")
        if record["record_origin"] not in {
            "LIVE_BOUNDED_LOOP",
            "EVIDENCE_RECONSTRUCTION",
        }:
            raise PersistenceError("event log record origin invalid")
        if record["sequence"] != expected_sequence:
            raise PersistenceError("event log sequence mismatch")
        if record["previous_record_digest_sha256"] != previous_digest:
            raise PersistenceError("event log hash chain mismatch")
        if record["record_digest_sha256"] != _event_record_digest(record):
            raise PersistenceError("event log digest mismatch")
        event = record["normalized_input"]
        audit = record["p5d2_audit"]
        if (
            not isinstance(event, dict)
            or event.get("sequence") != expected_sequence
            or not isinstance(audit, dict)
            or audit.get("sequence") != expected_sequence
            or audit.get("next_state_digest") != record["next_state_digest_sha256"]
            or audit.get("previous_state_digest") != record["previous_state_digest_sha256"]
        ):
            raise PersistenceError("event log P5-D2 binding mismatch")
        previous_digest = record["record_digest_sha256"]
        expected_sequence += 1
        records.append(record)
    return records

def load_checkpoint(control_root: Path) -> dict[str, Any] | None:
    root = _validate_control_root(control_root)
    path = root / "observer-checkpoint.json"
    if not path.exists():
        return None
    raw = path.read_bytes()
    try:
        checkpoint = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PersistenceError("checkpoint invalid") from exc
    if raw != _canonical_bytes(checkpoint):
        raise PersistenceError("checkpoint noncanonical")
    required = {
        "schema","loop_plan_digest_sha256","observer_state",
        "observer_state_digest_sha256","last_event_sequence",
        "last_event_digest_sha256","checkpoint_generation",
    }
    if set(checkpoint) != required or checkpoint.get("schema") != CHECKPOINT_SCHEMA:
        raise PersistenceError("checkpoint fields mismatch")
    state = checkpoint["observer_state"]
    try:
        _validate_state(state)
    except Exception as exc:
        raise PersistenceError("checkpoint observer state invalid") from exc
    if checkpoint["observer_state_digest_sha256"] != _digest(state):
        raise PersistenceError("checkpoint state digest mismatch")
    if checkpoint["last_event_sequence"] != state["last_event_sequence"]:
        raise PersistenceError("checkpoint sequence mismatch")
    if not _is_int(checkpoint["checkpoint_generation"], 1):
        raise PersistenceError("checkpoint generation invalid")
    if not _is_sha256(checkpoint["loop_plan_digest_sha256"]):
        raise PersistenceError("checkpoint plan digest invalid")
    if not _is_sha256(checkpoint["last_event_digest_sha256"]):
        raise PersistenceError("checkpoint event digest invalid")
    return checkpoint

def _checkpoint_value(
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
    generation: int,
) -> dict[str, Any]:
    return {
        "schema": CHECKPOINT_SCHEMA,
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "observer_state": state,
        "observer_state_digest_sha256": _digest(state),
        "last_event_sequence": state["last_event_sequence"],
        "last_event_digest_sha256": event_digest,
        "checkpoint_generation": generation,
    }

def _write_checkpoint(
    root: Path,
    *,
    plan: dict[str, Any],
    state: dict[str, Any],
    event_digest: str,
) -> dict[str, Any]:
    existing = load_checkpoint(root)
    generation = 1 if existing is None else existing["checkpoint_generation"] + 1
    value = _checkpoint_value(
        plan=plan, state=state, event_digest=event_digest, generation=generation)
    temp = root / "observer-checkpoint.tmp"
    final = root / "observer-checkpoint.json"
    _write_durable(temp, _canonical_bytes(value))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("checkpoint atomic replace failed") from exc
    verified = load_checkpoint(root)
    if verified != value:
        raise PersistenceError("checkpoint read-after-write mismatch")
    return verified
def _append_event(root: Path, record: dict[str, Any]) -> None:
    path = root / "observer-events.jsonl"
    raw = _canonical_bytes(record)
    try:
        with path.open("ab") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise PersistenceError("event append failed") from exc

def _would_append_queue(state: dict[str, Any], event: dict[str, Any]) -> bool:
    return (
        event.get("event_type") == "REMOTE_HEAD_OBSERVED"
        and event.get("transition_class") in {"INITIAL", "FAST_FORWARD"}
        and event.get("observed_head") not in state.get("pending_heads", [])
    )

def persist_tick(
    *,
    control_root: Path,
    plan: dict[str, Any],
    previous_state: dict[str, Any],
    normalized_input: dict[str, Any],
    loop_id: str,
    cycle_index: int,
    record_origin: str = "LIVE_BOUNDED_LOOP",
    fault_injector: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    try:
        _validate_state(previous_state)
    except Exception as exc:
        raise PersistenceError("previous observer state invalid") from exc
    if loop_id != plan["loop_id"]:
        raise PersistenceError("loop id mismatch")
    if record_origin not in {"LIVE_BOUNDED_LOOP", "EVIDENCE_RECONSTRUCTION"}:
        raise PersistenceError("record origin invalid")
    if _would_append_queue(previous_state, normalized_input):
        if len(previous_state["pending_heads"]) >= plan["max_pending_heads"]:
            raise QueueCapacityError("pending queue capacity exhausted")

    log = load_event_log(root)
    if log:
        tail = log[-1]
        if tail["sequence"] != previous_state["last_event_sequence"]:
            raise PersistenceError("event log/state sequence mismatch")
        if tail["next_state_digest_sha256"] != _digest(previous_state):
            raise PersistenceError("event log/state digest mismatch")
    elif previous_state["last_event_sequence"] != 0:
        raise PersistenceError("noninitial state has no event history")
    tick = one_shot_tick(previous_state, normalized_input)
    audit = tick["audit"]
    previous_record_digest = log[-1]["record_digest_sha256"] if log else None
    record = {
        "schema": EVENT_SCHEMA,
        "sequence": normalized_input["sequence"],
        "loop_id": loop_id,
        "cycle_index": cycle_index,
        "normalized_input": normalized_input,
        "p5d2_audit": audit,
        "previous_state_digest_sha256": audit["previous_state_digest"],
        "next_state_digest_sha256": audit["next_state_digest"],
        "previous_record_digest_sha256": previous_record_digest,
        "record_origin": record_origin,
    }
    record["record_digest_sha256"] = _event_record_digest(record)
    _append_event(root, record)
    if fault_injector is not None:
        fault_injector("AFTER_EVENT_DURABLE_BEFORE_CHECKPOINT_REPLACE")
    checkpoint = _write_checkpoint(
        root,
        plan=plan,
        state=tick["next_state"],
        event_digest=record["record_digest_sha256"],
    )
    return {
        "tick_result": tick,
        "event_record": record,
        "checkpoint": checkpoint,
    }

def _replay_record(
    state: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    if record["previous_state_digest_sha256"] != _digest(state):
        raise ReconciliationError("replay previous-state digest mismatch")
    try:
        tick = one_shot_tick(state, record["normalized_input"])
    except Exception as exc:
        raise ReconciliationError("P5-D2 replay rejected") from exc
    if tick["audit"] != record["p5d2_audit"]:
        raise ReconciliationError("replay audit mismatch")
    if _digest(tick["next_state"]) != record["next_state_digest_sha256"]:
        raise ReconciliationError("replay next-state digest mismatch")
    return tick["next_state"]

def _validate_evidence(
    verified_current_head: str,
    evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    if not _is_head(verified_current_head):
        raise ReconciliationError("verified CURRENT head invalid")
    if not isinstance(evidence, dict):
        raise ReconciliationError("verified publication evidence required")
    required = {
        "schema","candidate_head","status","transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256","logical_receipt_digest_sha256",
        "p5d2_promotion_confirmed_emitted",
    }
    if set(evidence) != required or evidence.get("schema") != EVIDENCE_SCHEMA:
        raise ReconciliationError("publication evidence fields mismatch")
    if evidence["candidate_head"] != verified_current_head:
        raise ReconciliationError("publication evidence head mismatch")
    if evidence["status"] != "PASS_LIVE_PUBLICATION_CONFIRMED":
        raise ReconciliationError("publication evidence status mismatch")
    for field in (
        "transaction_plan_digest_sha256",
        "physical_receipt_digest_sha256",
        "logical_receipt_digest_sha256",
    ):
        if not _is_sha256(evidence[field]):
            raise ReconciliationError("publication evidence digest invalid")
    if evidence["p5d2_promotion_confirmed_emitted"] is not True:
        raise ReconciliationError("promotion confirmation evidence missing")
    return evidence

def reconstruct_from_verified_publication_evidence(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    if load_checkpoint(root) is not None or load_event_log(root):
        raise ReconciliationError("evidence reconstruction requires empty control state")
    _validate_evidence(verified_current_head, promotion_evidence)
    state = make_initial_state()
    events = (
        {
            "schema": INPUT_SCHEMA, "event_type": "REMOTE_HEAD_OBSERVED",
            "sequence": 1, "observed_head": verified_current_head,
            "transition_class": "INITIAL", "candidate_head": None, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_STARTED",
            "sequence": 2, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "EVALUATION_PASSED",
            "sequence": 3, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
        {
            "schema": INPUT_SCHEMA, "event_type": "PROMOTION_CONFIRMED",
            "sequence": 4, "observed_head": None, "transition_class": None,
            "candidate_head": verified_current_head, "failure_code": None,
        },
    )
    for event in events:
        persisted = persist_tick(
            control_root=root,
            plan=plan,
            previous_state=state,
            normalized_input=event,
            loop_id=plan["loop_id"],
            cycle_index=0,
            record_origin="EVIDENCE_RECONSTRUCTION",
        )
        state = persisted["tick_result"]["next_state"]
    return {
        "status": "PASS_RECONSTRUCTED_VERIFIED_PUBLICATION_EVIDENCE",
        "observer_state": state,
        "evidence": promotion_evidence,
    }

def reconcile_control_state(
    *,
    control_root: Path,
    plan: dict[str, Any],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root)
    log = load_event_log(root)
    checkpoint = load_checkpoint(root)

    if checkpoint is None and not log:
        if verified_current_head is None:
            return {
                "status": "PASS_CANONICAL_INITIAL_STATE",
                "observer_state": make_initial_state(),
            }
        return reconstruct_from_verified_publication_evidence(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )

    if checkpoint is None:
        if len(log) != 1:
            raise ReconciliationError("event log too far ahead without checkpoint")
        base = make_initial_state()
        next_state = _replay_record(base, log[0])
        _write_checkpoint(
            root,
            plan=plan,
            state=next_state,
            event_digest=log[0]["record_digest_sha256"],
        )
        return {
            "status": "PASS_RECONCILED_ONE_RECORD_AHEAD",
            "observer_state": next_state,
        }

    if checkpoint["loop_plan_digest_sha256"] != plan["plan_digest_sha256"]:
        raise ReconciliationError("checkpoint loop-plan mismatch")
    cp_seq = checkpoint["last_event_sequence"]
    if cp_seq > len(log):
        raise ReconciliationError("checkpoint ahead of event log")
    delta = len(log) - cp_seq
    if delta > 1:
        raise ReconciliationError("event log more than one record ahead")
    state = checkpoint["observer_state"]
    if cp_seq:
        tail_at_checkpoint = log[cp_seq - 1]
        if checkpoint["last_event_digest_sha256"] != tail_at_checkpoint["record_digest_sha256"]:
            raise ReconciliationError("checkpoint event digest mismatch")
        if checkpoint["observer_state_digest_sha256"] != tail_at_checkpoint["next_state_digest_sha256"]:
            raise ReconciliationError("checkpoint/log state digest mismatch")
    if delta == 1:
        record = log[-1]
        state = _replay_record(state, record)
        _write_checkpoint(
            root,
            plan=plan,
            state=state,
            event_digest=record["record_digest_sha256"],
        )
        status = "PASS_RECONCILED_ONE_RECORD_AHEAD"
    else:
        status = "PASS_RECONCILED_ALIGNED"

    live = state["live_projection_head"]
    if verified_current_head is None:
        if live is not None:
            raise ReconciliationError("checkpoint live head has no physical CURRENT")
    elif live != verified_current_head:
        raise ReconciliationError("physical CURRENT differs from checkpoint live head")

    return {"status": status, "observer_state": state}

def _normalized_event(
    state: dict[str, Any],
    event_type: str,
    *,
    candidate_head: str | None = None,
    failure_code: str | None = None,
) -> dict[str, Any]:
    return {
        "schema": INPUT_SCHEMA,
        "event_type": event_type,
        "sequence": state["last_event_sequence"] + 1,
        "observed_head": None,
        "transition_class": None,
        "candidate_head": candidate_head,
        "failure_code": failure_code,
    }

def _write_run_result(root: Path, result: dict[str, Any]) -> None:
    temp = root / "last-run.tmp"
    final = root / "last-run.json"
    _write_durable(temp, _canonical_bytes(result))
    try:
        os.replace(str(temp), str(final))
    except OSError as exc:
        raise PersistenceError("run-result replace failed") from exc

def _base_run_result(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": RUN_RESULT_SCHEMA,
        "loop_id": plan["loop_id"],
        "loop_plan_digest_sha256": plan["plan_digest_sha256"],
        "terminal_reason": None,
        "cycles_started": 0,
        "remote_observations": 0,
        "evaluations_started": 0,
        "consecutive_failures": 0,
        "observer_state": None,
        "automatic_promotion_authorized": False,
        "production_write_authorized": False,
    }

def run_bounded_loop(
    *,
    plan: dict[str, Any],
    control_root: Path,
    observation_adapter: Callable[[dict[str, Any]], dict[str, Any]],
    evaluation_adapter: Callable[[str, dict[str, Any]], dict[str, Any]],
    verified_current_head: str | None,
    promotion_evidence: dict[str, Any] | None,
    forbidden_roots: Iterable[Path] = (),
    owner_token: str,
) -> dict[str, Any]:
    plan = validate_loop_plan(plan)
    root = _validate_control_root(control_root, forbidden_roots=forbidden_roots)
    result = _base_run_result(plan)
    try:
        ownership = acquire_ownership(
            root, loop_id=plan["loop_id"], owner_token=owner_token)
    except OwnershipContended:
        result["terminal_reason"] = "LOCK_CONTENDED"
        return result

    state: dict[str, Any] | None = None
    try:
        reconciled = reconcile_control_state(
            control_root=root,
            plan=plan,
            verified_current_head=verified_current_head,
            promotion_evidence=promotion_evidence,
        )
        state = reconciled["observer_state"]

        if state["observer_phase"] == "CANDIDATE_PENDING":
            result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
        elif state["observer_phase"] == "BLOCKED":
            result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
        elif state["observer_phase"] == "EVALUATING":
            result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        elif state["observer_phase"] == "STOPPED":
            result["terminal_reason"] = "SHUTDOWN_REQUESTED"

        for cycle_index in range(1, plan["max_cycles"] + 1):
            if result["terminal_reason"] is not None:
                break
            result["cycles_started"] += 1

            if state["pending_heads"]:
                if result["evaluations_started"] >= plan["max_evaluations"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
                candidate = state["pending_heads"][0]
                started = persist_tick(
                    control_root=root,
                    plan=plan,
                    previous_state=state,
                    normalized_input=_normalized_event(
                        state, "EVALUATION_STARTED", candidate_head=candidate),
                    loop_id=plan["loop_id"],
                    cycle_index=cycle_index,
                )
                state = started["tick_result"]["next_state"]
                result["evaluations_started"] += 1
                outcome = evaluation_adapter(candidate, started["tick_result"])
                if not isinstance(outcome, dict):
                    raise P5D4RuntimeError("evaluation adapter result invalid")
                classification = outcome.get("outcome")
                failure_code = outcome.get("failure_code")
                if classification == "QUALIFIED":
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_PASSED", candidate_head=candidate),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "PROMOTION_AUTHORITY_REQUIRED"
                elif classification == "REJECTED":
                    if not isinstance(failure_code, str) or not failure_code:
                        raise P5D4RuntimeError("rejected evaluation requires failure code")
                    finished = persist_tick(
                        control_root=root, plan=plan, previous_state=state,
                        normalized_input=_normalized_event(
                            state, "EVALUATION_FAILED",
                            candidate_head=candidate, failure_code=failure_code),
                        loop_id=plan["loop_id"], cycle_index=cycle_index)
                    state = finished["tick_result"]["next_state"]
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                elif classification == "BLOCKED":
                    result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                else:
                    raise P5D4RuntimeError("evaluation outcome invalid")
                continue

            if result["remote_observations"] >= plan["max_remote_observations"]:
                result["terminal_reason"] = "BOUND_REACHED"
                break
            event = observation_adapter(state)
            result["remote_observations"] += 1
            observed = persist_tick(
                control_root=root,
                plan=plan,
                previous_state=state,
                normalized_input=event,
                loop_id=plan["loop_id"],
                cycle_index=cycle_index,
            )
            state = observed["tick_result"]["next_state"]
            if event.get("event_type") == "REMOTE_OBSERVATION_FAILED":
                result["consecutive_failures"] += 1
                if result["consecutive_failures"] > plan["max_consecutive_failures"]:
                    result["terminal_reason"] = "BOUND_REACHED"
                    break
            else:
                result["consecutive_failures"] = 0

            if state["observer_phase"] == "BLOCKED":
                result["terminal_reason"] = "BLOCKED_REQUIRES_ADJUDICATION"
                break
            if (
                observed["tick_result"]["decision"]["action"] == "NOOP"
                and not state["pending_heads"]
            ):
                result["terminal_reason"] = "NO_PENDING_WORK"
                break

        if result["terminal_reason"] is None:
            result["terminal_reason"] = "BOUND_REACHED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except QueueCapacityError:
        result["terminal_reason"] = "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except ReconciliationError:
        result["terminal_reason"] = "RECONCILIATION_REQUIRED"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    except Exception:
        result["terminal_reason"] = "FATAL_INCONSISTENCY"
        result["observer_state"] = state
        _write_run_result(root, result)
        return result
    finally:
        release_ownership(root, ownership)

~~~~

# SOURCE: P5-A CONTINUOUS PROJECTION CONTRACT
Path: tools/obsidian_projection/continuous_projection_contract_v0_1.json
~~~~
{
  "schema": "ATDS_OBSIDIAN_CONTINUOUS_PROJECTION_CONTRACT_V0_1",
  "status": "CANDIDATE_PREREGISTRATION_ONLY",
  "source_repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "predecessor_p4c_head": "10355f467ccf8f87070ab18839b96ba6fc547d9d",
  "monitored_source": {
    "remote": "origin",
    "branch": "integration/system-v1",
    "observed_head_at_preregistration": "6aef3b1304313c3446c08a3a37b51ea61733f41e",
    "canonical_authority": "GITHUB_REMOTE_BRANCH",
    "local_working_tree_is_not_authority": true
  },
  "objective": {
    "name": "CONTINUOUS_GITHUB_TO_OBSIDIAN_PROJECTION",
    "user_goal": "Every governed GitHub update on the monitored ATDS branch becomes visible in Obsidian without manual projection rebuild.",
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "instantaneous_realtime_claim_forbidden": true,
    "target_detection_latency_seconds_max": 60,
    "implementation_poll_interval_seconds_candidate": 30
  },
  "architecture_choice": {
    "selected_candidate": "LOCAL_REMOTE_REF_OBSERVER",
    "rationale": [
      "The qualified Vault is local Windows/OneDrive storage.",
      "GitHub Actions cannot directly mutate the user's local Vault.",
      "A GitHub webhook would require an inbound endpoint and additional infrastructure.",
      "Obsidian Git automation would violate the existing authority and persistence boundary.",
      "A local remote-ref observer can remain read-only toward GitHub and write only the derived projection."
    ],
    "rejected_initial_mechanisms": [
      "OBSIDIAN_GIT_AUTO_PULL_PUSH",
      "GITHUB_ACTION_DIRECT_TO_LOCAL_VAULT",
      "PUBLIC_WEBHOOK_ENDPOINT_REQUIRED"
    ],
    "webhook_may_be_reconsidered_later": true
  },
  "authority_boundary": {
    "github_remote_branch": "CANONICAL",
    "canonical_local_checkout": "READ_ONLY_EXECUTION_INPUT",
    "projection": "DERIVED",
    "obsidian": "OBSERVE_NAVIGATE_QUERY_VISUALIZE_UNDERSTAND",
    "observer_may_push_to_github": false,
    "observer_may_commit_to_github": false,
    "observer_may_modify_canonical_worktree": false,
    "observer_may_create_operational_authority": false
  },
  "runtime_isolation": {
    "canonical_user_repo_mutation_forbidden": true,
    "build_checkout_location": "OS_TEMP_OR_DEDICATED_NON_VAULT_CONTROL_ROOT",
    "build_checkout_must_be_disposable": true,
    "build_checkout_must_resolve_exact_repo_origin": true,
    "build_checkout_must_resolve_exact_target_commit": true,
    "build_must_not_use_user_worktree_registry": true,
    "vault_must_not_contain_git_directory": true
  },
  "remote_observation": {
    "operation_class": "READ_ONLY_REMOTE_REF_CHECK",
    "permitted_examples": [
      "git ls-remote origin refs/heads/integration/system-v1",
      "git fetch --no-tags origin integration/system-v1"
    ],
    "full_fetch_on_every_poll_required": false,
    "credentials_must_not_be_logged": true,
    "network_failure_result": "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
    "repeated_same_head_result": "NOOP",
    "new_head_result": "QUEUE_EXACT_HEAD_FOR_QUALIFICATION"
  },
  "head_transition_policy": {
    "classify_transition": [
      "INITIAL",
      "FAST_FORWARD",
      "NON_FAST_FORWARD",
      "UNKNOWN"
    ],
    "automatic_promotion_allowed_for": [
      "INITIAL",
      "FAST_FORWARD"
    ],
    "non_fast_forward_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "unknown_ancestry_result": "BLOCKED_REQUIRES_ADJUDICATION",
    "silent_history_rewrite_acceptance_forbidden": true
  },
  "event_coalescing": {
    "every_observed_head_must_be_logged": true,
    "active_build_may_finish_against_its_exact_head": true,
    "newer_head_arriving_during_build_must_be_queued": true,
    "superseded_heads_may_skip_projection_only_if_fast_forward_contained_by_later_head": true,
    "skipped_head_status": "SUPERSEDED_NOT_PROMOTED",
    "latest_head_must_eventually_be_evaluated": true
  },
  "current_head_projection_prerequisite": {
    "frozen_pilot_inventory_is_insufficient_for_continuous_mode": true,
    "continuous_mode_requires_dynamic_inventory_for_each_exact_head": true,
    "inventory_scope_candidate": [
      "GOVERNANCE",
      "docs",
      "evidence",
      "reports",
      "requirements",
      "src",
      "tests",
      "tools",
      "breakers",
      ".github/workflows"
    ],
    "binary_or_large_artifact_policy_must_be_explicit": true,
    "secrets_and_credentials_must_never_be_projected": true,
    "source_selection_contract_required_before_runtime": true
  },
  "qualification_pipeline": {
    "ordered_gates": [
      "OBSERVE_REMOTE_HEAD",
      "VERIFY_REPOSITORY_IDENTITY",
      "CLASSIFY_HEAD_TRANSITION",
      "FETCH_EXACT_HEAD",
      "CREATE_ISOLATED_CHECKOUT",
      "BUILD_DYNAMIC_INVENTORY",
      "CLASSIFY_ARTIFACTS",
      "BUILD_DETERMINISTIC_PROJECTION_A",
      "BUILD_DETERMINISTIC_PROJECTION_B",
      "REQUIRE_A_EQUALS_B",
      "RUN_PROJECTION_BREAKERS",
      "BUILD_MACHINE_VIEW_LAYER_IF_AUTHORIZED",
      "STAGE_COMPLETE_GENERATION",
      "VERIFY_STAGED_GENERATION",
      "PROMOTE_ATOMICALLY_OR_BLOCK",
      "VERIFY_LIVE_GENERATION",
      "RECORD_EVENT_AND_STATE"
    ],
    "any_gate_failure_result": "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
    "partial_success_may_not_be_promoted": true
  },
  "generation_identity": {
    "required_fields": [
      "repository",
      "branch",
      "source_head",
      "source_tree",
      "projection_contract_version",
      "inventory_digest",
      "semantic_record_digest",
      "projection_tree_digest",
      "generated_file_count",
      "qualified_at_state_transition"
    ],
    "volatile_host_data_in_deterministic_tree_forbidden": true,
    "source_head_must_match_built_checkout_head": true
  },
  "projection_states": {
    "allowed": [
      "CURRENT",
      "STALE",
      "BLOCKED",
      "ORPHAN",
      "MISSING"
    ],
    "current_definition": "LIVE_PROJECTION_SOURCE_HEAD_EQUALS_LATEST_QUALIFIED_MONITORED_REMOTE_HEAD",
    "stale_definition": "REMOTE_HEAD_IS_NEWER_THAN_LIVE_PROJECTION_HEAD_OR_LATEST_HEAD_NOT_YET_PROMOTED",
    "blocked_definition": "LATEST_OBSERVED_HEAD_FAILED_OR_REQUIRES_ADJUDICATION",
    "orphan_definition": "DERIVED_ARTIFACT_SOURCE_NO_LONGER_EXISTS_IN_CURRENT_QUALIFIED_SOURCE_TREE",
    "missing_definition": "EXPECTED_DERIVED_ARTIFACT_IS_ABSENT",
    "unknown_must_not_be_mapped_to_current": true
  },
  "last_known_good": {
    "required": true,
    "live_projection_must_remain_usable_on_failure": true,
    "failed_candidate_must_not_modify_live_projection": true,
    "failed_candidate_evidence_must_be_preserved_outside_live_projection": true,
    "last_known_good_source_head_must_be_recorded": true
  },
  "promotion_atomicity": {
    "mixed_generation_visibility_forbidden": true,
    "direct_in_place_multi_file_overwrite_forbidden": true,
    "staging_required": true,
    "candidate_mechanism": "STAGED_GENERATION_SWAP_OR_EQUIVALENT_ATOMIC_VISIBILITY_PRIMITIVE",
    "exact_windows_onedrive_mechanism_not_yet_qualified": true,
    "obsidian_open_during_promotion_not_yet_authorized": true,
    "empirical_promotion_primitive_qualification_required": true
  },
  "vault_policy": {
    "vault_path": "C:\\Users\\Boulevart\\OneDrive\\Bureau\\ATDS\\ATDS-OBSIDIAN-PROJECTION",
    "generated_owner": "MACHINE",
    "views_owner": "HUMAN",
    "obsidian_config_owner": "OBSIDIAN_UI",
    "observer_may_write_generated_only_after_promotion_gate": true,
    "observer_may_overwrite_human_views": false,
    "observer_may_modify_obsidian_config": false,
    "observer_may_enable_obsidian_sync": false,
    "observer_may_install_plugins": false
  },
  "machine_visual_layer_future_policy": {
    "continuous_visual_refresh_required_for_final_goal": true,
    "current_human_views_must_not_be_silently_overwritten": true,
    "future_machine_managed_visual_namespace_required": true,
    "candidate_namespace": "generated/live",
    "bases_graph_canvas_dashboards_may_be_generated_only_after_separate_contract": true,
    "human_views_may_link_to_machine_live_views": true
  },
  "runtime_state_storage": {
    "deterministic_projection_state_inside_generated_allowed": true,
    "volatile_daemon_state_location": "LOCALAPPDATA_OUTSIDE_VAULT",
    "append_only_event_log_required": true,
    "minimum_event_fields": [
      "observed_at",
      "remote_head",
      "previous_live_head",
      "transition_class",
      "pipeline_result",
      "live_head_after",
      "projection_state",
      "failure_code"
    ],
    "event_log_is_not_semantic_authority": true
  },
  "concurrency": {
    "single_promotion_writer_required": true,
    "lock_scope": "CONTINUOUS_PROJECTION_ENGINE",
    "second_instance_result": "NO_WRITE_BLOCKED_BY_LOCK",
    "obsidian_readers_must_never_observe_partial_generation": true
  },
  "recovery": {
    "crash_before_promotion": "DISCARD_OR_PRESERVE_STAGING_NO_LIVE_CHANGE",
    "crash_during_unqualified_atomic_primitive": "BLOCK_CONTINUOUS_MODE_UNTIL_ADJUDICATED",
    "crash_after_promotion_before_state_log": "RECONSTRUCT_STATE_FROM_LIVE_GENERATION_IDENTITY",
    "no_recursive_delete_of_last_known_good": true
  },
  "observability": {
    "health_report_required": true,
    "fields": [
      "observer_running",
      "latest_remote_head",
      "live_projection_head",
      "projection_state",
      "last_success_time",
      "last_failure_time",
      "last_failure_code",
      "queued_head_count"
    ],
    "current_state_must_be_visible_in_obsidian_later": true,
    "current_state_visibility_must_not_create_authority": true
  },
  "p5a_boundary": {
    "contract_tests_and_architecture_only": true,
    "background_observer_execution_authorized": false,
    "remote_polling_loop_authorized": false,
    "vault_continuous_write_authorized": false,
    "generated_replacement_authorized": false,
    "human_views_overwrite_authorized": false,
    "windows_startup_registration_authorized": false,
    "scheduled_task_creation_authorized": false
  },
  "required_breakers": [
    "observer pushes to GitHub",
    "observer commits to canonical repository",
    "canonical user working tree is mutated",
    "wrong repository origin accepted",
    "wrong monitored branch accepted",
    "build checkout HEAD differs from observed remote HEAD",
    "same HEAD triggers rebuild",
    "non-fast-forward silently auto-promoted",
    "unknown ancestry silently auto-promoted",
    "frozen 74-artifact pilot treated as sufficient dynamic inventory",
    "secret or credential projected",
    "single build accepted without deterministic double-build comparison",
    "failed candidate mutates live projection",
    "partial candidate promoted",
    "mixed generations visible",
    "direct in-place multi-file overwrite used as promotion",
    "last-known-good deleted before new generation verified",
    "human views overwritten",
    ".obsidian modified by observer",
    "Obsidian Sync enabled",
    "community plugin required",
    "Git automation inside Vault enabled",
    "volatile daemon data changes deterministic digest",
    "remote network failure marks projection CURRENT",
    "UNKNOWN mapped to CURRENT",
    "STALE silently presented as CURRENT",
    "second writer bypasses engine lock",
    "event history lost for observed HEAD",
    "superseded HEAD omitted without fast-forward containment",
    "latest queued HEAD never evaluated",
    "atomic promotion primitive assumed without Windows/OneDrive evidence",
    "Obsidian-open promotion assumed safe without empirical qualification"
  ],
  "next_gates": {
    "p5b": "DYNAMIC_CURRENT_HEAD_INVENTORY_AND_SOURCE_SELECTION_CONTRACT",
    "p5c": "WINDOWS_ONEDRIVE_ATOMIC_PROMOTION_PRIMITIVE_QUALIFICATION",
    "p5d": "CONTINUOUS_OBSERVER_IMPLEMENTATION_CANDIDATE",
    "p5e": "END_TO_END_NEAR_REAL_TIME_QUALIFICATION"
  }
}

~~~~

# SOURCE: P5-D3F REAL REMOTE REF PATTERN
Path: tools/obsidian_projection/p5d3f_recovery_real_execution_v0_4.py
~~~~
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from tools.obsidian_projection.persistent_production_handoff import (
    PERSISTENT_STAGING,
    REAL_VAULT,
    PersistentHandoffPostSuccessCleanupBlockedError,
    execute_persistent_production_handoff,
    validate_persistent_paths,
    validate_staging_prestate,
)


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
RUNNER_BRANCH = (
    "feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.4-monitored-head-pin"
)
MONITORED_BRANCH = "integration/system-v1"
EXPECTED_IMPLEMENTATION_BLOB = (
    "dcd70a9d9794675eab90e41df560f8b030b5dbf3"
)
EXPECTED_RECOVERY_IMPLEMENTATION_TEST_BLOB = (
    "242305bc0f95bbe243158b5c806255508093a357"
)
EXPECTED_RECOVERY_GATE_CONTRACT_BLOB = (
    "aef627936b6f745017bcace7e8a3e44270f95674"
)
EXPECTED_GATE_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)
EXPECTED_QUALIFIED_P5D3F_BLOB = (
    "2108131914cf65bb076b80f5bb63cd63267567fa"
)
RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB = (
    "3667488c6cb7a348eab6564b7152049e0ba32d3b"
)
EFFECTIVE_RUNNER_BRANCH = (
    "feat/obsidian-projection-p5d3f-recovery-v04-qualified-blob-rebind-amendment-v0.1"
)
EFFECTIVE_IMPLEMENTATION_BLOB = (
    "375607d88bc926e4fd4c297ddc6fedba5506642a"
)
EFFECTIVE_QUALIFIED_P5D3F_BLOB = (
    "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60"
)

AUTHORIZATION_LITERAL = (
    "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF"
)
AUTHORIZED_STAGING_PRESTATE = (
    "PRESENT_EMPTY_PACKAGES_RECOVERY"
)

OID40 = re.compile(r"^[0-9a-f]{40}$")
RUNNER_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d3f_recovery_real_execution_v0_4.py"
)


class RealExecutionRunnerError(RuntimeError):
    pass


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run(
    *args: str,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=str(cwd),
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        env={
            **os.environ,
            "GIT_OPTIONAL_LOCKS": "0",
        },
    )


def _git(
    repo: Path,
    *args: str,
) -> str:
    result = _run(
        "git",
        *args,
        cwd=repo,
    )
    if result.returncode != 0:
        details = (
            (result.stderr or "").strip()
            or (result.stdout or "").strip()
        )
        raise RealExecutionRunnerError(
            "git command failed"
            + (f": {details}" if details else "")
        )
    return (result.stdout or "").strip()


def _normalize_origin(origin: str) -> str:
    value = origin.strip()
    for prefix in (
        "git@github.com:",
        "https://github.com/",
        "ssh://git@github.com/",
    ):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    else:
        raise RealExecutionRunnerError(
            f"unsupported origin form: {origin}"
        )

    if value.endswith(".git"):
        value = value[:-4]

    return value.strip("/")


def _require_clean(repo: Path) -> None:
    dirty = _git(
        repo,
        "status",
        "--porcelain",
        "--untracked-files=all",
    )
    if dirty:
        raise RealExecutionRunnerError(
            "BLOCKED_CONTROL_CLONE_DIRTY: "
            + dirty
        )


def _committed_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "rev-parse",
        f"HEAD:{relative}",
    )


def _worktree_blob(
    repo: Path,
    relative: str,
) -> str:
    return _git(
        repo,
        "hash-object",
        "--no-filters",
        relative,
    )


def _verify_exact_runtime(
    repo: Path,
    expected_runner_head: str,
    expected_runner_blob: str,
) -> None:
    if _normalize_origin(
        _git(
            repo,
            "remote",
            "get-url",
            "origin",
        )
    ) != EXPECTED_REPOSITORY:
        raise RealExecutionRunnerError(
            "repository identity mismatch"
        )

    _require_clean(repo)

    local_head = _git(
        repo,
        "rev-parse",
        "HEAD",
    )
    if local_head != expected_runner_head:
        raise RealExecutionRunnerError(
            "local HEAD is not the authorized runner HEAD"
        )

    _git(
        repo,
        "fetch",
        "--no-tags",
        "origin",
        EFFECTIVE_RUNNER_BRANCH,
    )
    fetched = _git(
        repo,
        "rev-parse",
        "FETCH_HEAD",
    )
    if fetched != expected_runner_head:
        raise RealExecutionRunnerError(
            "BLOCKED_RUNNER_REMOTE_HEAD_RACE"
        )

    if _committed_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner committed blob mismatch"
        )

    if _worktree_blob(
        repo,
        RUNNER_RELATIVE,
    ) != expected_runner_blob:
        raise RealExecutionRunnerError(
            "governed runner worktree blob mismatch"
        )

    expected_blobs = {
        (
            "tools/obsidian_projection/"
            "p5d3f_recovery_v04_qualified_blob_rebind_amendment_contract_v0_1.json"
        ): RECOVERY_V04_REBIND_AMENDMENT_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff.py"
        ): EFFECTIVE_IMPLEMENTATION_BLOB,
        (
            "tests/obsidian_projection/"
            "test_p5d3f_persistent_handoff_recovery_implementation_v0_3.py"
        ): EXPECTED_RECOVERY_IMPLEMENTATION_TEST_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_2.json"
        ): EXPECTED_RECOVERY_GATE_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "persistent_production_handoff_gate_contract_v0_1.json"
        ): EXPECTED_GATE_CONTRACT_BLOB,
        (
            "tools/obsidian_projection/"
            "p5d3f_promotion_handoff.py"
        ): EFFECTIVE_QUALIFIED_P5D3F_BLOB,
    }

    for relative, expected_blob in (
        expected_blobs.items()
    ):
        actual = _committed_blob(
            repo,
            relative,
        )
        if actual != expected_blob:
            raise RealExecutionRunnerError(
                "qualified blob mismatch: "
                + relative
            )


def _verify_expected_monitored_head(
    repo: Path,
    expected_monitored_head: str,
) -> None:
    ref = (
        "refs/heads/"
        + MONITORED_BRANCH
    )
    parts = _git(
        repo,
        "ls-remote",
        "--heads",
        "origin",
        ref,
    ).split()

    if (
        len(parts) != 2
        or parts[1] != ref
        or parts[0] != expected_monitored_head
    ):
        raise RealExecutionRunnerError(
            "BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH"
        )


def _require_authorized_prestate(
    prestate: str,
) -> None:
    if prestate != AUTHORIZED_STAGING_PRESTATE:
        raise RealExecutionRunnerError(
            "BLOCKED_UNAUTHORIZED_STAGING_PRESTATE: "
            + prestate
        )


def _validate_final_success_result(
    result: dict[str, object],
    expected_monitored_head: str,
) -> None:
    if result.get("candidate_head") != expected_monitored_head:
        raise RealExecutionRunnerError(
            "result candidate head differs from authorized monitored head"
        )

    if result.get("status") != (
        "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED"
    ):
        raise RealExecutionRunnerError(
            "unexpected persistent handoff status"
        )

    if result.get(
        "publication_authorized"
    ) is not False:
        raise RealExecutionRunnerError(
            "publication authority unexpectedly true"
        )

    if result.get(
        "live_publication_executed"
    ) is not False:
        raise RealExecutionRunnerError(
            "live publication unexpectedly executed"
        )

    if result.get(
        "mandatory_stop"
    ) is not True:
        raise RealExecutionRunnerError(
            "mandatory STOP missing"
        )

    zero = result.get(
        "zero_mutation_proof"
    )
    if (
        not isinstance(zero, dict)
        or zero.get("unchanged") is not True
        or zero.get("status")
        != "PASS_REAL_VAULT_ZERO_MUTATION"
    ):
        raise RealExecutionRunnerError(
            "real Vault zero-mutation proof missing"
        )


def _post_success_cleanup_block_details(
    exc: PersistentHandoffPostSuccessCleanupBlockedError,
    expected_monitored_head: str,
) -> dict[str, object]:
    temp_root = getattr(
        exc,
        "p5d3f_temp_root",
        None,
    )
    success_result = getattr(
        exc,
        "p5d3f_success_result",
        None,
    )

    if (
        not isinstance(temp_root, str)
        or not temp_root
    ):
        raise RealExecutionRunnerError(
            "post-success cleanup block missing temp root"
        )

    if not isinstance(
        success_result,
        dict,
    ):
        raise RealExecutionRunnerError(
            "post-success cleanup block missing success result"
        )

    _validate_final_success_result(
        success_result,
        expected_monitored_head,
    )

    return {
        "temp_root": temp_root,
        "success_result": success_result,
    }


def _snapshot_staging_residual(
    staging: Path,
) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "path": str(staging),
        "exists": False,
        "state": "ABSENT",
        "entries": [],
    }

    try:
        if not staging.exists():
            return snapshot

        snapshot["exists"] = True

        if not staging.is_dir():
            snapshot["state"] = (
                "PRESENT_NON_DIRECTORY"
            )
            return snapshot

        rows: list[dict[str, object]] = []
        for path in sorted(
            staging.rglob("*"),
            key=lambda p: p.relative_to(
                staging
            ).as_posix(),
        ):
            relative = path.relative_to(
                staging
            ).as_posix()

            try:
                if path.is_dir():
                    rows.append(
                        {
                            "path": relative,
                            "type": "DIRECTORY",
                        }
                    )
                elif path.is_file():
                    info = path.stat()
                    rows.append(
                        {
                            "path": relative,
                            "type": "FILE",
                            "size": int(
                                info.st_size
                            ),
                        }
                    )
                else:
                    rows.append(
                        {
                            "path": relative,
                            "type": "OTHER",
                        }
                    )
            except OSError as exc:
                rows.append(
                    {
                        "path": relative,
                        "type": "UNREADABLE",
                        "error_type":
                            type(exc).__name__,
                        "error": str(exc),
                    }
                )

        snapshot["entries"] = rows
        snapshot["state"] = (
            "PRESENT_EMPTY"
            if not rows
            else "PRESENT_NONEMPTY"
        )
        return snapshot

    except Exception as exc:
        snapshot["state"] = (
            "SNAPSHOT_UNAVAILABLE"
        )
        snapshot["snapshot_error_type"] = (
            type(exc).__name__
        )
        snapshot["snapshot_error"] = str(exc)
        return snapshot

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--expected-runner-head",
        required=True,
    )
    parser.add_argument(
        "--expected-runner-blob",
        required=True,
    )
    parser.add_argument(
        "--expected-monitored-head",
        required=True,
    )
    parser.add_argument(
        "--authorization",
        required=True,
    )
    args = parser.parse_args()

    if OID40.fullmatch(
        args.expected_runner_head
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-head"
        )

    if OID40.fullmatch(
        args.expected_runner_blob
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-runner-blob"
        )

    if OID40.fullmatch(
        args.expected_monitored_head
    ) is None:
        raise RealExecutionRunnerError(
            "invalid --expected-monitored-head"
        )

    if args.authorization != (
        AUTHORIZATION_LITERAL
    ):
        raise RealExecutionRunnerError(
            "explicit one-shot human authorization literal missing"
        )

    repo = _repo_root()

    print(
        "=== P5-D3F PERSISTENT PRODUCTION HANDOFF "
        "REAL EXECUTION ==="
    )
    print(
        "AUTHORITY=ONE_FINITE_READY_UNAUTHORIZED_HANDOFF_ONLY"
    )
    print(
        "REAL_VAULT_WRITE_AUTHORIZED=FALSE"
    )
    print(
        "LIVE_PUBLICATION_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_A_AUTHORIZED=FALSE"
    )
    print(
        "STAGE_B_AUTHORIZED=FALSE"
    )

    _verify_exact_runtime(
        repo,
        args.expected_runner_head,
        args.expected_runner_blob,
    )
    print(
        "P5D3F_PERSISTENT_REAL_EXECUTION_RUNTIME_IDENTITY=PASS"
    )

    _verify_expected_monitored_head(
        repo,
        args.expected_monitored_head,
    )
    print(
        "P5D3F_EXPECTED_MONITORED_HEAD="
        + args.expected_monitored_head
    )
    print(
        "P5D3F_MONITORED_HEAD_AUTHORITY=PASS"
    )

    staging, vault = (
        validate_persistent_paths()
    )

    if staging != PERSISTENT_STAGING.resolve(
        strict=False
    ):
        raise RealExecutionRunnerError(
            "persistent staging identity mismatch"
        )

    if vault != REAL_VAULT.resolve(
        strict=True
    ):
        raise RealExecutionRunnerError(
            "real Vault identity mismatch"
        )

    prestate = validate_staging_prestate(
        staging
    )
    print(
        "P5D3F_PERSISTENT_STAGING_PRESTATE="
        + prestate
    )
    _require_authorized_prestate(
        prestate
    )
    print(
        "P5D3F_RECOVERY_PRESTATE_AUTHORIZED=PASS"
    )

    try:
        result = execute_persistent_production_handoff(
            control_repo=repo,
        )
    except PersistentHandoffPostSuccessCleanupBlockedError as cleanup_exc:
        details = (
            _post_success_cleanup_block_details(
                cleanup_exc,
                args.expected_monitored_head,
            )
        )
        residual = _snapshot_staging_residual(
            staging
        )
        print(
            "P5D3F_POST_SUCCESS_CLEANUP_BLOCKED=TRUE",
            file=sys.stderr,
        )
        print(
            "P5D3F_POST_SUCCESS_TEMP_ROOT="
            + str(details["temp_root"]),
            file=sys.stderr,
        )
        print(
            "P5D3F_POST_SUCCESS_RESULT_JSON="
            + json.dumps(
                details["success_result"],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON="
            + json.dumps(
                residual,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        raise
    except Exception as original_exc:
        residual = _snapshot_staging_residual(
            staging
        )
        print(
            "P5D3F_PERSISTENT_FAILURE_ORIGINAL="
            + type(original_exc).__name__
            + ": "
            + str(original_exc),
            file=sys.stderr,
        )
        temp_root = getattr(
            original_exc,
            "p5d3f_temp_root",
            None,
        )
        if isinstance(
            temp_root,
            str,
        ) and temp_root:
            print(
                "P5D3F_PERSISTENT_FAILURE_TEMP_ROOT="
                + temp_root,
                file=sys.stderr,
            )
        print(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON="
            + json.dumps(
                residual,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
            file=sys.stderr,
        )
        raise

    _validate_final_success_result(
        result,
        args.expected_monitored_head,
    )

    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION=PASS"
    )
    print(
        "REAL_VAULT_ZERO_MUTATION=PASS"
    )
    print(
        "LIVE_PUBLICATION_EXECUTED=FALSE"
    )
    print(
        "MANDATORY_STOP=TRUE"
    )
    print(
        "RESULT_JSON="
        + json.dumps(
            result,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    )

    _require_clean(repo)
    print(
        "CONTROL_CLONE_CLEAN=PASS"
    )
    print(
        "P5D3F_PERSISTENT_HANDOFF_REAL_EXECUTION_COMPLETED=PASS"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        RealExecutionRunnerError,
        Exception,
    ) as exc:
        if isinstance(
            exc,
            KeyboardInterrupt,
        ):
            raise
        print(
            f"BLOCKED: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)

~~~~

# SOURCE: FROZEN GIT SOURCE
Path: tools/obsidian_projection/git_source.py
~~~~
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping, Sequence

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_FORBIDDEN_GIT_OPTIONS = frozenset({"--filters", "--textconv"})


class GitSourceError(RuntimeError):
    """Base error for the canonical Git source boundary."""


class RepositoryIdentityError(GitSourceError):
    """Raised when the local repository is not the expected repository."""


class FrozenSourceError(GitSourceError):
    """Raised when the frozen commit/tree/blob contract is not satisfied."""


class UnsafeGitInvocationError(GitSourceError):
    """Raised when a working-tree transforming Git mode is requested."""


@dataclass(frozen=True)
class TreeEntry:
    path: str
    mode: str
    object_type: str
    oid: str
    size: int | None


GitRunner = Callable[[Path, Sequence[str]], bytes]


def normalize_origin(origin: str) -> str:
    """Normalize supported GitHub origin forms to owner/repository."""
    value = origin.strip()
    if value.startswith("git@github.com:"):
        value = value[len("git@github.com:") :]
    elif value.startswith("https://github.com/"):
        value = value[len("https://github.com/") :]
    elif value.startswith("ssh://git@github.com/"):
        value = value[len("ssh://git@github.com/") :]
    else:
        raise RepositoryIdentityError(f"unsupported GitHub origin form: {origin!r}")

    if value.endswith(".git"):
        value = value[:-4]
    value = value.strip("/")
    if value.count("/") != 1 or not all(value.split("/", 1)):
        raise RepositoryIdentityError(f"invalid normalized GitHub origin: {value!r}")
    return value


def validate_git_args(args: Sequence[str]) -> None:
    """Reject modes that transform canonical Git-object bytes."""
    for arg in args:
        if (
            arg in _FORBIDDEN_GIT_OPTIONS
            or arg.startswith("--filters=")
            or arg.startswith("--textconv=")
        ):
            raise UnsafeGitInvocationError(
                f"forbidden Git transformation option: {arg}"
            )


def _default_git_runner(repo_root: Path, args: Sequence[str]) -> bytes:
    validate_git_args(args)
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        raise GitSourceError(f"git {' '.join(args)} failed: {stderr}")
    return completed.stdout


class FrozenGitSource:
    """Read-only access to an exact governed Git commit/tree/blob domain."""

    def __init__(
        self,
        repo_root: str | Path,
        expected_repository: str,
        source_commit: str,
        expected_tree: str,
        *,
        runner: GitRunner | None = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.expected_repository = expected_repository
        self.source_commit = self._require_oid(source_commit, "source_commit")
        self.expected_tree = self._require_oid(expected_tree, "expected_tree")
        self._runner = runner or _default_git_runner

    @staticmethod
    def _require_oid(value: str, field: str) -> str:
        lowered = value.lower()
        if not _HEX40.fullmatch(lowered):
            raise ValueError(
                f"{field} must be a full 40-character hexadecimal Git object id"
            )
        return lowered

    def _git(self, *args: str) -> bytes:
        validate_git_args(args)
        return self._runner(self.repo_root, args)

    def verify_repository(self) -> None:
        top_level = (
            self._git("rev-parse", "--show-toplevel")
            .decode("utf-8")
            .strip()
        )
        if Path(top_level).resolve() != self.repo_root:
            raise RepositoryIdentityError(
                f"repo_root mismatch: configured={self.repo_root} "
                f"git={Path(top_level).resolve()}"
            )

        origin = (
            self._git("remote", "get-url", "origin")
            .decode("utf-8")
            .strip()
        )
        actual_repository = normalize_origin(origin)
        if actual_repository != self.expected_repository:
            raise RepositoryIdentityError(
                f"repository mismatch: expected={self.expected_repository} "
                f"actual={actual_repository}"
            )

    def verify_frozen_source(self) -> None:
        object_type = (
            self._git("cat-file", "-t", self.source_commit)
            .decode("ascii")
            .strip()
        )
        if object_type != "commit":
            raise FrozenSourceError(
                f"frozen source is not a commit: "
                f"{self.source_commit} type={object_type}"
            )

        actual_tree = (
            self._git("rev-parse", f"{self.source_commit}^{{tree}}")
            .decode("ascii")
            .strip()
        )
        if actual_tree != self.expected_tree:
            raise FrozenSourceError(
                f"tree mismatch: expected={self.expected_tree} actual={actual_tree}"
            )

    def read_blob(self, oid: str) -> bytes:
        blob_oid = self._require_oid(oid, "blob_oid")
        object_type = (
            self._git("cat-file", "-t", blob_oid)
            .decode("ascii")
            .strip()
        )
        if object_type != "blob":
            raise FrozenSourceError(
                f"object is not a blob: {blob_oid} type={object_type}"
            )
        return self._git("cat-file", "blob", blob_oid)

    def blob_size(self, oid: str) -> int:
        blob_oid = self._require_oid(oid, "blob_oid")
        raw = self._git("cat-file", "-s", blob_oid).decode("ascii").strip()
        try:
            return int(raw)
        except ValueError as exc:
            raise FrozenSourceError(
                f"invalid blob size for {blob_oid}: {raw!r}"
            ) from exc

    def tree_entries(self) -> tuple[TreeEntry, ...]:
        raw = self._git("ls-tree", "-rz", "-l", self.source_commit)
        entries: list[TreeEntry] = []

        for record in raw.split(b"\0"):
            if not record:
                continue
            try:
                header, path_raw = record.split(b"\t", 1)
            except ValueError as exc:
                raise FrozenSourceError(
                    "malformed git ls-tree record"
                ) from exc

            fields = header.split()
            if len(fields) != 4:
                raise FrozenSourceError(
                    f"malformed git ls-tree header: {header!r}"
                )

            mode_b, type_b, oid_b, size_b = fields
            try:
                oid = oid_b.decode("ascii").lower()
            except UnicodeDecodeError as exc:
                raise FrozenSourceError(
                    "non-ASCII Git object id in tree"
                ) from exc

            self._require_oid(oid, "tree_entry_oid")
            size = None if size_b == b"-" else int(size_b)

            entries.append(
                TreeEntry(
                    path=path_raw.decode(
                        "utf-8",
                        errors="surrogateescape",
                    ),
                    mode=mode_b.decode("ascii"),
                    object_type=type_b.decode("ascii"),
                    oid=oid,
                    size=size,
                )
            )

        return tuple(entries)

    def tree_entry_map(self) -> Mapping[str, TreeEntry]:
        result: dict[str, TreeEntry] = {}
        for entry in self.tree_entries():
            if entry.path in result:
                raise FrozenSourceError(
                    f"duplicate path in Git tree: {entry.path}"
                )
            result[entry.path] = entry
        return result

    def read_path(self, path: str) -> bytes:
        entry = self.tree_entry_map().get(path)
        if entry is None:
            raise FrozenSourceError(
                f"path not present in frozen tree: {path}"
            )
        if entry.object_type != "blob" or entry.mode == "120000":
            raise FrozenSourceError(
                f"path is not an admissible regular blob: {path} "
                f"type={entry.object_type} mode={entry.mode}"
            )
        return self.read_blob(entry.oid)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

~~~~
