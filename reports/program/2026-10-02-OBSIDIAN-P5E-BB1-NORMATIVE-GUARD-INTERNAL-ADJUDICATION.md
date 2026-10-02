# P5-E V0.1 — BB1 NORMATIVE GUARD COVERAGE — INTERNAL ADJUDICATION

Date: 2026-10-02

## Opening identity

Branch:
`feat/obsidian-projection-p5e-v0.1-bb1-normative-guard-closure`

Opening checkpoint:
`fe622489e9b822a987a1ec571f99b180fcfa5fb5`

Opening worktree:
`CLEAN`

Contract blob:
`b0668b4dff65b8e30ee0d93a3e5a3fe42c4421dd`

Model blob:
`b783717c9e9596b585b7b1686835c73fffbd1a7c`

Matrix blob:
`0440175fbb79877e466119cb973ea82389a4ecd8`
## BB1 local reproduction

The external reviewer reported that a combination of normative regressions could survive the 50-test P5-E targeted surface.

The exact defect was reproduced locally on the governed checkpoint without mutating repository files.

Baseline:
```text
50 tests
0 failures
0 errors
```

Combined BB1 mutation:
```text
50 tests
0 failures
0 errors
```

Therefore:
`BB1 = CONFIRMED_BLOCKING`

The defect is guard coverage, not an incorrect current value.
## Full leaf mutation sweep

A read-only sweep mutated every contract leaf independently in a temporary copy.

Observed:
```text
TOTAL_LEAF_MUTATIONS = 154
SURVIVING_FULL_50_MUTATIONS = 36
```

The 36 survivors divide into:
```text
NORMATIVE_SURVIVORS = 23
NON_NORMATIVE_OR_HISTORICAL_SURVIVORS = 13
```

The exit criterion for this closure is not zero total survivors.

The binding exit criterion is:
`NORMATIVE_LEAF_MUTATIONS_SURVIVING = 0`
## Normative survivor set — 23 leaves

1. `source_repository`
2. `monitored_source.remote`
3. `monitored_source.branch`
4. `monitored_source.canonical_authority`
5. `monitored_source.local_working_tree_is_not_authority`
6. `objective.this_stage_is_not_real_end_to_end_execution`
7. `objective.this_stage_may_not_claim_continuous_synchronization`
8. `near_real_time_timing.delivery_semantics`
9. `near_real_time_timing.detection_latency_definition`
10. `near_real_time_timing.future_real_bound_clock`
11. `near_real_time_timing.future_real_wall_clock_may_be_recorded_as_evidence_only`
12. `near_real_time_timing.latency_bound_breach_must_not_be_reported_as_near_real_time_pass`
13. `synthetic_timing_model.required`
14. `synthetic_timing_model.observation_record_fields`
15. `head_transition_policy.initial_head_may_queue_exact_head_only_under_existing_p5d2_semantics`
16. `head_transition_policy.fast_forward_head_may_queue_exact_head_only_under_existing_p5d2_semantics`
17. `queue_and_supersession.burst_catch_up_claim_forbidden_without_separate_queue_semantics_qualification`
18. `end_to_end_definition.real_end_to_end_stages`
19. `end_to_end_definition.real_end_to_end_pass_requires_all_authorized_applicable_stages`
20. `real_context_evidence_only.must_not_be_used_as_real_experiment_execution`
21. `real_context_evidence_only.must_not_be_mutated_by_contract_qualification`
22. `tip_visibility_semantics.future_ancestry_enumeration_requires_separate_qualification`
23. `external_review_targeted_closure.external_rereview_required_before_human_normative_adoption`

All 23 require strict protection or semantic de-duplication.
## Explicit non-normative / historical survivor set — 13 leaves

These may survive the normative mutation criterion:

- `objective.name`
- `objective.purpose`
- `synthetic_timing_model.purpose`
- `queue_and_supersession.p5a_supersession_intent_preserved_as_future_design_debt`
- `real_context_evidence_only.live_projection_head_at_opening`
- `real_context_evidence_only.queued_unevaluated_head_at_opening`
- `real_context_evidence_only.remote_head_observed_during_contract_opening`
- `real_context_evidence_only.queued_head_is_ancestor_of_remote_head`
- `external_review_targeted_closure.findings.B1`
- `external_review_targeted_closure.findings.B2`
- `external_review_targeted_closure.findings.B3`
- `external_review_targeted_closure.findings.B4`
- `external_review_targeted_closure.findings.B5`

They are descriptive, historical, or debt-tracking metadata rather than current behavioral authority.
## Matrix binding defect

The current evidence matrix contains no exact binding for:
- the covered P5-E contract blob;
- the covered P5-E model blob.

Its tests validate mapped test-file blobs but not the exact contract/model objects being qualified.

This is independently confirmed as part of BB1.

## Adjudicated same-pass corrections

NB1:
`VALID — CLOSE IN THIS PASS`
A read that crosses the next required fixed-rate slot must fail closed rather than silently terminalize as PASS.

NB4:
`VALID — CLAIM CORRECTION ONLY`
The non-injection of an unobserved intermediate tip is a future adapter rule, not a currently qualified runtime property.
NB6:
`VALID — MATRIX EVIDENCE REMAP`
Mappings must point to semantically exact behavioral evidence. Add a dedicated pending-non-active test only if no exact existing test exists.

NB7:
`PARTIAL — SMALL SEMANTIC CLEANUP`
- `INCOMPLETE_SYNTHETIC_WINDOW` must be explicitly NON-PASS.
- duplicate fixed-rate slot must have a distinct failure code from `CADENCE_GAP`.
- theoretical AST bypass is not part of this closure because no current model defect was demonstrated.

## Deferred by scope

NB2, NB3, NB5, and NB9 remain recorded for future real-observation / ancestry-classifier preregistration.

They are not reopened here.
## Real-state fingerprint before closure work

P5-D4 control files at opening:
```text
observer-events.jsonl
= 54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af

observer-checkpoint.json
= c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4

last-run.json
= eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259
```

The closure must not mutate these files.

## Internal verdict

```text
BB1 = CONFIRMED_BLOCKING
BB1_LOCAL_REPRODUCTION = COMPLETE
NORMATIVE_SURVIVORS = 23
MATRIX_CONTRACT_BINDING = ABSENT
MATRIX_MODEL_BINDING = ABSENT
REAL_P5E = CLOSED
```
