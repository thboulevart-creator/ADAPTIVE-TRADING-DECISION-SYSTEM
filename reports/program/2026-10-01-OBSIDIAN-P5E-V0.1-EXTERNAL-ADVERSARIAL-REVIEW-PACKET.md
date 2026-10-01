# P5-E V0.1 — SELF-CONTAINED EXTERNAL ADVERSARIAL REVIEW PACKET

Date: 2026-10-01

## Reviewer mandate

You are performing an independent adversarial review of the candidate:

P5-E — END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1

Review only what is contained in this packet. Do not assume missing authority, tests, runtime behavior, or real-world evidence.

The current candidate claim is deliberately limited to:

P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED

The candidate does not claim that real P5-E end-to-end near-real-time synchronization is qualified.

### Required review questions

1. Are the inherited timing constraints (30-second candidate observation interval, 60-second maximum detection latency) preserved without silent widening?
2. Is detection latency defined rigorously enough to support a future real experiment?
3. Is monotonic elapsed time the correct future enforcement clock, and is wall-clock evidence clearly separated from bound enforcement?
4. Does the synthetic model accidentally prove less or more than the contract claims?
5. Can a synthetic PASS be laundered into a real P5-E PASS?
6. Are transient read failures, late success, no success, malformed schedules, and boundary equality handled correctly?
7. Is the conflict between historical P5-A supersession intent and current P5-D4 FIFO/no-coalescing semantics resolved safely?
8. Can queue saturation, multiple newer HEADs, or candidate retargeting cause silent data loss or authority leakage?
9. Can observation trigger evaluation, Stage A, Stage B, promotion, publication, Vault mutation, or P6 without separate authority?
10. Do the tests genuinely break the contract/model, or are they overly coupled to implementation wording?
11. Are important failure families missing?
12. Are any PASS statements broader than the actually tested surface?
13. Is the proposed next step safe: human adjudication of the contract/synthetic candidate before any separately authorized real P5-E experiment?

### Required output format

Return:

VERDICT = PASS | PASS_WITH_NON_BLOCKING_NOTES | FAIL

Then provide:

- BLOCKING_FINDINGS
- NON_BLOCKING_FINDINGS
- MISSING_ADVERSARIAL_CASES
- AUTHORITY_LEAKAGE_CHECK
- TIMING_SEMANTICS_CHECK
- QUEUE_SEMANTICS_CHECK
- CLAIM_SCOPE_CHECK
- RECOMMENDED_TARGETED_CORRECTIONS

For every finding, cite the exact packet section and the exact field/function/test involved.

Do not authorize real execution. Do not treat your review as human adoption. Do not infer that a synthetic timing result proves a real 60-second SLA.

## Packet identities

- P5-E preregistration blob: 6ef788532a1e945a42ca524af823710ae4f14ed6
- P5-E base test blob: 2305e0768182d82657c34a7cb53c502714a2ab81
- P5-E contract blob: e5c3d7a9d451aba65e8062078c6c10d23e586f39
- P5-E synthetic model blob: 8662dd97a1c8a1af33d6593ae923384e96404b5a
- P5-E adversarial test blob: 6235c4b2addc16acd043832664440ec76f6dada2
- P5-D4 runtime blob: 1825e53d195ba2a63b5b646a5b78eb77939b94b5

---

# SOURCE: P5-E PREREGISTRATION

Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_preregistration_v0_1.json

~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_PREREGISTRATION_V0_1",
  "status": "PREREGISTERED_BEFORE_RED",
  "repository": "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
  "branch": "feat/obsidian-projection-p5e-end-to-end-near-real-time-qualification-v0.1",
  "opening_base_head": "11c6c5e1a009b171466f26e295f812030015d655",
  "authorized_stage": "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
  "real_p5e_execution_authorized": false,
  "predecessor_identities": {
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
  "inherited_timing_constraints": {
    "delivery_semantics": "NEAR_REAL_TIME_BOUNDED_LATENCY",
    "instantaneous_realtime_claim_forbidden": true,
    "target_detection_latency_seconds_max": 60,
    "candidate_poll_interval_seconds": 30,
    "silent_interval_widening_forbidden": true,
    "silent_latency_bound_widening_forbidden": true
  },
  "timing_semantics_to_freeze": {
    "detection_latency_definition": "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
    "future_real_clock_requirement": "MONOTONIC_ELAPSED_TIME_FOR_BOUND_ENFORCEMENT",
    "synthetic_model_clock": "EXPLICIT_INJECTED_SECONDS_ONLY",
    "synthetic_model_may_sleep": false,
    "synthetic_model_may_use_network": false,
    "synthetic_model_may_use_filesystem_state": false,
    "synthetic_model_may_launch_processes": false,
    "source_change_just_after_poll_must_be_covered": true,
    "one_transient_read_failure_then_success_by_60_seconds_must_be_covered": true,
    "first_success_after_60_seconds_must_fail_latency_qualification": true,
    "no_success_by_60_seconds_must_fail_latency_qualification": true
  },
  "authority_boundary": {
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
  "queue_semantics_resolution": {
    "p5a_historical_supersession_intent": "NON_NORMATIVE_WHERE_IT_CONFLICTS_WITH_CURRENT_EXECUTABLE_P5D4_QUEUE_SEMANTICS",
    "p5d4_fifo_required": true,
    "p5d4_silent_drop_forbidden": true,
    "p5d4_silent_reorder_forbidden": true,
    "p5d4_latest_only_replacement_forbidden": true,
    "p5d4_coalescing_authorized": false,
    "p5d4_queue_capacity_exhausted_result": "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
    "newer_head_must_not_retarget_active_or_pending_head": true,
    "no_new_coalescing_event_may_be_invented_in_p5e_v0_1": true
  },
  "observed_real_context_read_only": {
    "live_projection_head": "59f1dc26973b0b50efefccf12b26784d1e41f546",
    "queued_unevaluated_head": "1d4c2f3d657b36ecaa6ab25b967e46b3620190d1",
    "remote_head_at_opening": "fcca78571a26955ae3fe462746ef49557e4e84e5",
    "queued_head_is_ancestor_of_remote_head": true,
    "p5d4_event_log_sha256": "54223895a720e98e0f686e4882f098f2d93324d0e0d4a06164e58ac864eda4af",
    "p5d4_checkpoint_sha256": "c737e064461bd8562cbfe21ff68e28556bc2ce0cb74abe2d59c89c9b0cca13d4",
    "p5d4_last_run_sha256": "eb555cadff72152553b460068cb89964b8b9cd40b7b47e8a82594e26fc47d259",
    "context_is_evidence_only_not_test_input_authority": true,
    "real_context_must_not_be_mutated_or_evaluated_in_this_stage": true
  },
  "claim_boundary": {
    "contract_pass_may_claim": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED",
    "contract_pass_may_not_claim": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED"
    ],
    "real_end_to_end_claim_requires_separate_human_authorization_and_real_experiment": true
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
  "test_first_sequence": [
    "PERSIST_PREREGISTRATION",
    "ADD_TESTS_EXPECTING_ABSENT_CONTRACT_AND_MODEL",
    "RUN_RED_AND_PERSIST_EVIDENCE",
    "ADD_MINIMAL_CONTRACT_AND_PURE_SYNTHETIC_MODEL",
    "RUN_TARGETED_GREEN",
    "ADD_ADVERSARIAL_TESTS",
    "MECHANICAL_CORRECTIONS_ONLY_IF_DEMONSTRATED",
    "RUN_TARGETED_REGRESSIONS",
    "RUN_ONE_FULL_OBSIDIAN_REBREAK",
    "BUILD_SELF_CONTAINED_EXTERNAL_REVIEW_PACKET",
    "PERSIST_QUALIFICATION_EVIDENCE",
    "STOP_BEFORE_REAL_P5E"
  ],
  "mandatory_stop": "AFTER_CONTRACT_SYNTHETIC_QUALIFICATION_AND_EXTERNAL_REVIEW_PACKET_BEFORE_ANY_REAL_P5E_EXECUTION"
}

~~~~

# SOURCE: P5-E CONTRACT CANDIDATE

Path: tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json

~~~~
{
  "schema": "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
  "status": "CANDIDATE_CONTRACT_NOT_NORMATIVE",
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
    "detection_latency_definition": "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
    "future_real_bound_clock": "MONOTONIC_ELAPSED_TIME",
    "future_real_wall_clock_may_be_recorded_as_evidence_only": true,
    "future_real_poll_schedule_semantics": "ATTEMPTS_AT_BOUNDED_30_SECOND_INTERVALS_WITH_NO_UNBOUNDED_RETRY",
    "single_transient_read_failure_may_still_meet_60_second_bound": true,
    "latency_bound_breach_must_not_be_reported_as_near_real_time_pass": true
  },
  "synthetic_timing_model": {
    "required": true,
    "clock_source": "EXPLICIT_INJECTED_SECONDS_ONLY",
    "sleep_forbidden": true,
    "network_forbidden": true,
    "filesystem_state_forbidden": true,
    "process_launch_forbidden": true,
    "environment_read_forbidden": true,
    "real_p5d4_control_state_access_forbidden": true,
    "real_vault_access_forbidden": true,
    "purpose": "Prove timing arithmetic and claim boundaries without performing repeated real observation."
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
    "unexpected_state_or_timing_ambiguity_result": "BLOCKED_REQUIRES_ADJUDICATION"
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
      "SYNTHETIC_DETECTION_BOUND_ARITHMETIC",
      "AUTHORITY_BOUNDARIES",
      "FAIL_CLOSED_QUEUE_INTERACTION"
    ],
    "real_end_to_end_pass_requires_all_authorized_applicable_stages": true,
    "omitted_unauthorized_downstream_stages_may_not_be_relabelled_pass": true
  },
  "claim_boundary": {
    "maximum_current_claim": "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED",
    "real_end_to_end_qualification_requires_separate_authorization": true,
    "forbidden_current_claims": [
      "P5E_REAL_END_TO_END_QUALIFIED",
      "CONTINUOUS_SYNCHRONIZATION_QUALIFIED",
      "REAL_60_SECOND_SLA_QUALIFIED",
      "AUTOMATIC_EVALUATION_QUALIFIED",
      "AUTOMATIC_PROMOTION_QUALIFIED",
      "AUTOMATIC_PUBLICATION_QUALIFIED"
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
    "p6_remains_closed": true
  }
}

~~~~

# SOURCE: P5-E PURE SYNTHETIC TIMING MODEL

Path: tools/obsidian_projection/p5e_near_real_time_model.py

~~~~
from __future__ import annotations

from typing import Any


PLAN_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_PLAN_V0_1"
RESULT_SCHEMA = "ATDS_OBSIDIAN_P5E_SYNTHETIC_TIMING_RESULT_V0_1"

_POLL_INTERVAL_SECONDS = 30
_DETECTION_LATENCY_SECONDS_MAX = 60
_ALLOWED_OUTCOMES = frozenset({"READ_FAILURE", "EXACT_HEAD_OBSERVED"})


class P5ETimingModelError(ValueError):
    pass


def _is_nonnegative_int(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, int)
        and value >= 0
    )


def make_timing_plan(
    *,
    poll_interval_seconds: int = _POLL_INTERVAL_SECONDS,
    detection_latency_seconds_max: int = _DETECTION_LATENCY_SECONDS_MAX,
) -> dict[str, Any]:
    if poll_interval_seconds != _POLL_INTERVAL_SECONDS:
        raise P5ETimingModelError(
            "P5-E V0.1 poll interval must remain exactly 30 seconds"
        )
    if detection_latency_seconds_max != _DETECTION_LATENCY_SECONDS_MAX:
        raise P5ETimingModelError(
            "P5-E V0.1 detection bound must remain exactly 60 seconds"
        )
    return {
        "schema": PLAN_SCHEMA,
        "poll_interval_seconds": poll_interval_seconds,
        "detection_latency_seconds_max": detection_latency_seconds_max,
        "clock_source": "EXPLICIT_INJECTED_SECONDS_ONLY",
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
    ):
        raise P5ETimingModelError("plan fields mismatch")


def _validate_observations(
    observations: list[dict[str, Any]],
    *,
    interval: int,
) -> None:
    if not isinstance(observations, list) or not observations:
        raise P5ETimingModelError("observations must be a non-empty list")
    previous: int | None = None
    for observation in observations:
        if not isinstance(observation, dict):
            raise P5ETimingModelError("observation must be an object")
        if set(observation) != {"at_seconds", "outcome"}:
            raise P5ETimingModelError("observation fields mismatch")
        at_seconds = observation["at_seconds"]
        outcome = observation["outcome"]
        if not _is_nonnegative_int(at_seconds):
            raise P5ETimingModelError("observation time must be nonnegative")
        if at_seconds % interval != 0:
            raise P5ETimingModelError(
                "observation time must lie on the exact 30-second schedule"
            )
        if previous is not None and at_seconds <= previous:
            raise P5ETimingModelError(
                "observation times must be strictly increasing"
            )
        if outcome not in _ALLOWED_OUTCOMES:
            raise P5ETimingModelError("observation outcome invalid")
        previous = at_seconds


def _result(
    *,
    status: str,
    detection_latency_seconds: int | None,
    first_detection_at_seconds: int | None,
) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA,
        "status": status,
        "detection_latency_seconds": detection_latency_seconds,
        "first_detection_at_seconds": first_detection_at_seconds,
        "real_end_to_end_qualified": False,
        "continuous_synchronization_qualified": False,
        "automatic_evaluation_authorized": False,
        "automatic_promotion_authorized": False,
        "automatic_publication_authorized": False,
    }


def qualify_detection(
    *,
    plan: dict[str, Any],
    source_available_at_seconds: int,
    observations: list[dict[str, Any]],
) -> dict[str, Any]:
    _validate_plan(plan)
    if not _is_nonnegative_int(source_available_at_seconds):
        raise P5ETimingModelError(
            "source availability time must be a nonnegative integer"
        )
    interval = plan["poll_interval_seconds"]
    bound = plan["detection_latency_seconds_max"]
    _validate_observations(observations, interval=interval)

    first_detection: int | None = None
    for observation in observations:
        at_seconds = observation["at_seconds"]
        if at_seconds < source_available_at_seconds:
            continue
        if observation["outcome"] == "EXACT_HEAD_OBSERVED":
            first_detection = at_seconds
            break

    if first_detection is not None:
        latency = first_detection - source_available_at_seconds
        if latency <= bound:
            return _result(
                status="PASS_DETECTED_WITHIN_BOUND",
                detection_latency_seconds=latency,
                first_detection_at_seconds=first_detection,
            )
        return _result(
            status="FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
            detection_latency_seconds=latency,
            first_detection_at_seconds=first_detection,
        )

    last_observation = observations[-1]["at_seconds"]
    elapsed_without_detection = (
        last_observation - source_available_at_seconds
    )
    if elapsed_without_detection >= bound:
        return _result(
            status="FAIL_NO_DETECTION_BY_BOUND",
            detection_latency_seconds=None,
            first_detection_at_seconds=None,
        )
    return _result(
        status="INCOMPLETE_SYNTHETIC_WINDOW",
        detection_latency_seconds=None,
        first_detection_at_seconds=None,
    )

~~~~

# SOURCE: P5-E BASE TESTS

Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py

~~~~
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_end_to_end_near_real_time_contract_v0_1.json"
)
PREREG = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_end_to_end_near_real_time_preregistration_v0_1.json"
)
MODEL = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_near_real_time_model.py"
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestP5EContractV01(unittest.TestCase):
    def test_preregistration_is_present_and_frozen_before_contract(self) -> None:
        p = load_json(PREREG)
        self.assertEqual(
            p["status"],
            "PREREGISTERED_BEFORE_RED",
        )
        self.assertFalse(p["real_p5e_execution_authorized"])

    def test_contract_exists(self) -> None:
        self.assertTrue(CONTRACT.is_file())

    def test_contract_schema_and_stage_are_exact(self) -> None:
        c = load_json(CONTRACT)
        self.assertEqual(
            c["schema"],
            "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1",
        )
        self.assertEqual(
            c["qualification_stage"],
            "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY",
        )
        self.assertFalse(c["real_p5e_execution_authorized"])

    def test_predecessor_blobs_are_exact(self) -> None:
        c = load_json(CONTRACT)
        self.assertEqual(
            c["predecessors"]["p5a_continuous_projection_contract_blob"],
            "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_loop_contract_blob"],
            "6980de1eb55e49c0c2bd2f91620aeb75640753b6",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_runtime_blob"],
            "1825e53d195ba2a63b5b646a5b78eb77939b94b5",
        )
        self.assertEqual(
            c["predecessors"]["p5d4_human_adjudication_blob"],
            "ef5e07c6641db94e91d9f2bc0e8093b244baa507",
        )

    def test_timing_inheritance_is_exact_30_and_60(self) -> None:
        c = load_json(CONTRACT)
        t = c["near_real_time_timing"]
        self.assertEqual(t["poll_interval_seconds"], 30)
        self.assertEqual(t["detection_latency_seconds_max"], 60)
        self.assertTrue(t["instantaneous_realtime_claim_forbidden"])
        self.assertTrue(t["silent_interval_widening_forbidden"])
        self.assertTrue(t["silent_latency_bound_widening_forbidden"])

    def test_detection_latency_definition_is_explicit(self) -> None:
        c = load_json(CONTRACT)
        t = c["near_real_time_timing"]
        self.assertEqual(
            t["detection_latency_definition"],
            "FIRST_SUCCESSFUL_EXACT_REMOTE_HEAD_OBSERVATION_TIME_MINUS_SOURCE_HEAD_AVAILABLE_TIME",
        )
        self.assertEqual(
            t["future_real_bound_clock"],
            "MONOTONIC_ELAPSED_TIME",
        )

    def test_contract_forbids_authority_expansion(self) -> None:
        c = load_json(CONTRACT)
        a = c["authority_boundary"]
        for field in (
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
            self.assertFalse(a[field], field)

    def test_queue_conflict_resolves_in_favor_of_current_p5d4_semantics(self) -> None:
        c = load_json(CONTRACT)
        q = c["queue_and_supersession"]
        self.assertFalse(q["coalescing_authorized"])
        self.assertTrue(q["fifo_required"])
        self.assertTrue(q["silent_drop_forbidden"])
        self.assertTrue(q["latest_only_replacement_forbidden"])
        self.assertEqual(
            q["capacity_exhausted_result"],
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
        )
        self.assertTrue(q["pending_head_retarget_forbidden"])

    def test_contract_cannot_launder_synthetic_pass_into_real_p5e_pass(self) -> None:
        c = load_json(CONTRACT)
        claims = c["claim_boundary"]
        self.assertEqual(
            claims["maximum_current_claim"],
            "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED",
        )
        self.assertTrue(claims["real_end_to_end_qualification_requires_separate_authorization"])
        forbidden = set(claims["forbidden_current_claims"])
        self.assertIn("P5E_REAL_END_TO_END_QUALIFIED", forbidden)
        self.assertIn("REAL_60_SECOND_SLA_QUALIFIED", forbidden)
        self.assertIn("CONTINUOUS_SYNCHRONIZATION_QUALIFIED", forbidden)

    def test_required_breakers_cover_latency_queue_and_authority(self) -> None:
        c = load_json(CONTRACT)
        breakers = set(c["required_breakers"])
        required = {
            "POLL_INTERVAL_NOT_EXACTLY_30_ACCEPTED",
            "DETECTION_BOUND_ABOVE_60_ACCEPTED",
            "SUCCESS_AFTER_60_SECONDS_CLASSIFIED_PASS",
            "QUEUE_FULL_REPLACES_OLDER_PENDING_HEAD",
            "QUEUE_FULL_COALESCES_WITHOUT_P5D2_EVENT",
            "EVALUATION_AUTHORITY_BECOMES_TRUE",
            "PROMOTION_AUTHORITY_BECOMES_TRUE",
            "PUBLICATION_AUTHORITY_BECOMES_TRUE",
            "CONTRACT_PASS_LAUNDERS_INTO_REAL_P5E_PASS",
        }
        self.assertTrue(required.issubset(breakers))

    def test_synthetic_model_exists_and_has_no_real_runtime_primitives(self) -> None:
        self.assertTrue(MODEL.is_file())
        source = MODEL.read_text(encoding="utf-8")
        forbidden = (
            "import time",
            "from time",
            "sleep(",
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "pathlib",
            "open(",
            "os.",
        )
        for token in forbidden:
            self.assertNotIn(token, source, token)

    def test_model_freezes_exact_plan(self) -> None:
        m = load_model()
        plan = m.make_timing_plan()
        self.assertEqual(plan["poll_interval_seconds"], 30)
        self.assertEqual(plan["detection_latency_seconds_max"], 60)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(poll_interval_seconds=31)
        with self.assertRaises(m.P5ETimingModelError):
            m.make_timing_plan(detection_latency_seconds_max=61)

    def test_change_just_after_poll_detected_at_next_slot_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 29)
        self.assertFalse(result["real_end_to_end_qualified"])

    def test_one_transient_failure_then_success_by_60_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 59)

    def test_detection_after_60_seconds_is_rejected(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_DETECTION_LATENCY_BOUND_EXCEEDED",
        )
        self.assertEqual(result["detection_latency_seconds"], 89)

    def test_no_detection_by_bound_is_rejected(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=0,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(
            result["status"],
            "FAIL_NO_DETECTION_BY_BOUND",
        )
        self.assertIsNone(result["detection_latency_seconds"])

    def test_model_rejects_non_30_second_schedule(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=1,
                observations=[
                    {"at_seconds": 31, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )


if __name__ == "__main__":
    unittest.main()

~~~~

# SOURCE: P5-E ADVERSARIAL TESTS

Path: tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py

~~~~
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_end_to_end_near_real_time_contract_v0_1.json"
)
MODEL = (
    ROOT
    / "tools"
    / "obsidian_projection"
    / "p5e_near_real_time_model.py"
)


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def load_model():
    spec = importlib.util.spec_from_file_location("p5e_near_real_time_model_adv", MODEL)
    if spec is None or spec.loader is None:
        raise AssertionError("P5-E synthetic timing model unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_contract_invariants(contract: dict) -> None:
    assert (
        contract["schema"]
        == "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1"
    )
    assert contract["qualification_stage"] == (
        "CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY"
    )
    assert contract["real_p5e_execution_authorized"] is False

    timing = contract["near_real_time_timing"]
    assert timing["poll_interval_seconds"] == 30
    assert timing["detection_latency_seconds_max"] == 60
    assert timing["instantaneous_realtime_claim_forbidden"] is True
    assert timing["silent_interval_widening_forbidden"] is True
    assert timing["silent_latency_bound_widening_forbidden"] is True

    authority = contract["authority_boundary"]
    for field in (
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

    queue = contract["queue_and_supersession"]
    assert queue["fifo_required"] is True
    assert queue["silent_drop_forbidden"] is True
    assert queue["silent_reorder_forbidden"] is True
    assert queue["latest_only_replacement_forbidden"] is True
    assert queue["coalescing_authorized"] is False
    assert queue["new_coalescing_semantic_event_authorized"] is False
    assert queue["pending_head_retarget_forbidden"] is True
    assert (
        queue["capacity_exhausted_result"]
        == "QUEUE_CAPACITY_REQUIRES_ADJUDICATION"
    )
    assert queue["precedence_rule"] == (
        "CURRENT_QUALIFIED_P5D4_EXECUTABLE_QUEUE_SEMANTICS_OVERRIDE_"
        "EARLIER_P5A_DESIGN_INTENT_WHERE_THEY_CONFLICT"
    )

    claims = contract["claim_boundary"]
    assert claims["maximum_current_claim"] == (
        "P5E_V0_1_CONTRACT_AND_SYNTHETIC_TIMING_MODEL_QUALIFIED"
    )
    assert claims["real_end_to_end_qualification_requires_separate_authorization"]
    forbidden = set(claims["forbidden_current_claims"])
    assert "P5E_REAL_END_TO_END_QUALIFIED" in forbidden
    assert "REAL_60_SECOND_SLA_QUALIFIED" in forbidden
    assert "CONTINUOUS_SYNCHRONIZATION_QUALIFIED" in forbidden


class TestP5EAdversarialV01(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = load_contract()
        assert_contract_invariants(self.contract)

    def assert_mutation_rejected(self, mutator) -> None:
        candidate = copy.deepcopy(self.contract)
        mutator(candidate)
        with self.assertRaises(AssertionError):
            assert_contract_invariants(candidate)

    def test_poll_interval_31_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["near_real_time_timing"].__setitem__(
                "poll_interval_seconds", 31
            )
        )

    def test_detection_bound_61_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["near_real_time_timing"].__setitem__(
                "detection_latency_seconds_max", 61
            )
        )

    def test_real_execution_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c.__setitem__("real_p5e_execution_authorized", True)
        )

    def test_evaluation_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "evaluation_authorized", True
            )
        )

    def test_promotion_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "promotion_authorized", True
            )
        )

    def test_publication_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "publication_authorized", True
            )
        )

    def test_real_polling_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "real_polling_loop_authorized", True
            )
        )

    def test_p6_authority_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["authority_boundary"].__setitem__(
                "p6_authorized", True
            )
        )

    def test_coalescing_reintroduction_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "coalescing_authorized", True
            )
        )

    def test_latest_only_replacement_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "latest_only_replacement_forbidden", False
            )
        )

    def test_capacity_exhaustion_silent_continue_is_rejected(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "capacity_exhausted_result", "CONTINUE_WITH_LATEST"
            )
        )

    def test_p5a_design_intent_cannot_override_current_p5d4(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["queue_and_supersession"].__setitem__(
                "precedence_rule", "P5A_SUPERSESSION_WINS"
            )
        )

    def test_synthetic_pass_cannot_be_relabelled_real_pass(self) -> None:
        self.assert_mutation_rejected(
            lambda c: c["claim_boundary"].__setitem__(
                "maximum_current_claim", "P5E_REAL_END_TO_END_QUALIFIED"
            )
        )

    def test_real_pass_must_remain_forbidden_claim(self) -> None:
        def mutate(c):
            c["claim_boundary"]["forbidden_current_claims"].remove(
                "P5E_REAL_END_TO_END_QUALIFIED"
            )

        self.assert_mutation_rejected(mutate)

    def test_required_breakers_are_unique_and_broad(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertEqual(len(breakers), len(set(breakers)))
        self.assertGreaterEqual(len(breakers), 25)

    def test_synthetic_model_has_no_dynamic_import_escape(self) -> None:
        source = MODEL.read_text(encoding="utf-8")
        for token in (
            "__import__",
            "importlib",
            "eval(",
            "exec(",
            "globals(",
            "locals(",
        ):
            self.assertNotIn(token, source)

    def test_exact_60_second_boundary_passes(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=0,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        )
        self.assertEqual(result["status"], "PASS_DETECTED_WITHIN_BOUND")
        self.assertEqual(result["detection_latency_seconds"], 60)

    def test_success_before_source_availability_is_not_detection(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=31,
            observations=[
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertIsNone(result["detection_latency_seconds"])

    def test_negative_source_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=-1,
                observations=[
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_boolean_source_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=True,
                observations=[
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_empty_observation_list_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[],
            )

    def test_duplicate_observation_time_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[
                    {"at_seconds": 30, "outcome": "READ_FAILURE"},
                    {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
                ],
            )

    def test_invalid_observation_outcome_is_rejected(self) -> None:
        m = load_model()
        with self.assertRaises(m.P5ETimingModelError):
            m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=[
                    {"at_seconds": 30, "outcome": "PROMOTE"},
                ],
            )

    def test_incomplete_window_does_not_claim_pass(self) -> None:
        m = load_model()
        result = m.qualify_detection(
            plan=m.make_timing_plan(),
            source_available_at_seconds=1,
            observations=[
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
            ],
        )
        self.assertEqual(result["status"], "INCOMPLETE_SYNTHETIC_WINDOW")
        self.assertFalse(result["real_end_to_end_qualified"])
        self.assertFalse(result["continuous_synchronization_qualified"])

    def test_all_model_results_keep_downstream_authority_false(self) -> None:
        m = load_model()
        cases = [
            [
                {"at_seconds": 30, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
            [
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
            ],
            [
                {"at_seconds": 30, "outcome": "READ_FAILURE"},
                {"at_seconds": 60, "outcome": "READ_FAILURE"},
                {"at_seconds": 90, "outcome": "EXACT_HEAD_OBSERVED"},
            ],
        ]
        for observations in cases:
            result = m.qualify_detection(
                plan=m.make_timing_plan(),
                source_available_at_seconds=0,
                observations=observations,
            )
            self.assertFalse(result["automatic_evaluation_authorized"])
            self.assertFalse(result["automatic_promotion_authorized"])
            self.assertFalse(result["automatic_publication_authorized"])


if __name__ == "__main__":
    unittest.main()

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

# SOURCE: P5-D4 HUMAN ADJUDICATION V0.2

Path: GOVERNANCE/P5-D4-REAL-BOUNDED-LOOP-REQUALIFICATION-V0.2-HUMAN-ADJUDICATION-2026-10-01.md

~~~~
# P5-D4 â€” REAL BOUNDED LOOP REQUALIFICATION V0.2

## HUMAN ADJUDICATION â€” ADOPT

Date: 2026-10-01

Repository: `thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM`
Branch: `feat/obsidian-projection-p5d4-control-root-binding-remediation-v0.1`

Human decision supplied in conversation:

```text
P5D4_REAL_REQUALIFICATION_V0_2 = HUMAN_ADOPTED
```

This record persists the human decision. It is not represented as independent cryptographic proof of human identity.

## 1. Persistence base

Fresh-verified immediately before persistence:

```text
PRE_PERSISTENCE_HEAD =
bc70768d0966fed15af9ebd653bf9ff255df3095

PRE_PERSISTENCE_REMOTE_HEAD =
bc70768d0966fed15af9ebd653bf9ff255df3095

WORKTREE =
CLEAN
```

Qualification artifact:

`reports/program/2026-10-01-OBSIDIAN-P5D4-REAL-BOUNDED-LOOP-REQUALIFICATION-V0.2.md`

Qualification artifact blob:

`660a679532d1bb122b0df382230d4d249a0cac1f`

Qualified P5-D4 runtime blob:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

## 2. Human adjudication

The human adopts the persisted P5-D4 V0.2 qualification within the surface actually tested.

```text
P5-D4 REAL BOUNDED LOOP REQUALIFICATION V0.2
= HUMAN_ADOPTED

QUALIFICATION_SCOPE
= ACTUALLY_TESTED_SURFACE_ONLY
```

This adoption does not convert a scoped PASS into a claim that no material failure exists outside the tested surface.

## 3. Preserved pending state

The observed source HEAD remains:

`1d4c2f3d657b36ecaa6ab25b967e46b3620190d1`

Its governed state remains:

```text
PENDING_HEAD
= QUEUED

EVALUATED
= FALSE

PROMOTED
= FALSE

PUBLISHED
= FALSE
```

No authority to evaluate, promote, or publish that HEAD is created by this adjudication.

## 4. Explicit non-authorizations

This human adoption does not authorize:

```text
PENDING_HEAD_EVALUATION = FALSE
PROMOTION = FALSE
PUBLICATION = FALSE
P5-E = CLOSED
P6 = CLOSED
STAGE_A = CLOSED
STAGE_B = CLOSED
REAL_VAULT_MUTATION = FALSE
CURRENT_MUTATION = FALSE
CURRENT_TMP_MUTATION = FALSE
DAEMON = FALSE
PERIODIC_POLLING = FALSE
SCHEDULED_TASK = FALSE
WINDOWS_SERVICE = FALSE
```

## 5. Authority boundary

This decision changes only the governance status of the already-qualified P5-D4 V0.2 result.

It does not modify:

- the P5-D4 runtime;
- P5-D2 observer semantics;
- the live Vault;
- `CURRENT.md`;
- `CURRENT.tmp`;
- the queued HEAD;
- any evaluation or publication state.

Any subsequent frontier requires separate human authorization.

## 6. Adopted state

```text
P5D4_REAL_REQUALIFICATION_V0_2
= HUMAN_ADOPTED

P5D4_REAL_BOUNDED_LOOP
= QUALIFIED_AND_HUMAN_ADOPTED

PENDING_SOURCE_HEAD
= 1d4c2f3d657b36ecaa6ab25b967e46b3620190d1

PENDING_SOURCE_HEAD_STATUS
= QUEUED_NOT_EVALUATED

P5-E
= CLOSED

P6
= CLOSED
```

## 7. Stop boundary

After persistence and post-persistence verification:

```text
NEW_RUNTIME_EXECUTION
= NOT_AUTHORIZED

PENDING_HEAD_EVALUATION
= NOT_AUTHORIZED

P5-E_OPENING
= NOT_AUTHORIZED

P6_OPENING
= NOT_AUTHORIZED

STOP
= TRUE
```

~~~~

# SOURCE: P5-E RED EVIDENCE

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-RED-TEST-FIRST-EVIDENCE.md

~~~~
# P5-E V0.1 â€” RED TEST-FIRST EVIDENCE

Date: 2026-10-01

## Scope

This record persists the first RED execution for:

`P5-E â€” END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1`

Authorized stage:

`CONTRACT_AND_SYNTHETIC_QUALIFICATION_ONLY`

No real P5-E polling, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was authorized or executed.

## Preregistration basis

Preregistration HEAD:

`7843a5b6a35f08d9e14572d7ecd24f15e2ffce46`

Preregistration blob:

`6ef788532a1e945a42ca524af823710ae4f14ed6`

Artifact:

`tools/obsidian_projection/p5e_end_to_end_near_real_time_preregistration_v0_1.json`

## RED test artifact

`tests/obsidian_projection/test_p5e_end_to_end_near_real_time_contract_v0_1.py`

The test was created before the P5-E contract and before the synthetic timing model.

## RED execution

Command:

```text
python -B -m unittest tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1
```

Observed result:

```text
Ran 17 tests in 0.014s

FAILED (failures=2, errors=14)

RED_EXIT=1
```

Classification:

- 1 test passed: preregistration presence/status;
- 2 tests failed because the expected P5-E contract/model files did not yet exist;
- 14 tests errored because contract loading or synthetic-model loading reached those intentionally absent files.

The RED signal therefore demonstrates that the new P5-E requirements were not already satisfied by pre-existing files.

## What the RED test freezes

The test surface requires at minimum:

- exact P5-A inherited 30-second candidate interval;
- exact 60-second maximum detection latency;
- explicit detection-latency definition;
- no instantaneous-realtime claim;
- no silent widening of timing bounds;
- no evaluation/promotion/publication/P6 authority;
- current P5-D4 FIFO/no-coalescing queue semantics;
- queue-capacity exhaustion -> `QUEUE_CAPACITY_REQUIRES_ADJUDICATION`;
- no synthetic sleep/network/filesystem/process primitive;
- detection just after a poll;
- one transient read failure with success by 60 seconds;
- rejection after 60 seconds;
- rejection when no detection exists by the bound;
- rejection of a non-30-second synthetic observation schedule;
- no laundering of synthetic qualification into a real P5-E PASS.

## Mandatory next step

Only the minimal P5-E contract and pure synthetic timing model needed to satisfy these already-persisted tests may now be added.

Real P5-E execution remains closed.

~~~~

# SOURCE: P5-E MINIMAL GREEN EVIDENCE

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-MINIMAL-GREEN-EVIDENCE.md

~~~~
# P5-E V0.1 â€” MINIMAL GREEN EVIDENCE

Date: 2026-10-01

## Scope

This record persists the first GREEN transition for the preregistered P5-E V0.1 contract-first/test-first surface.

No real P5-E polling, network observer loop, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was authorized or executed.

## RED predecessor

RED HEAD:

`cc00dfd14b5592f81afa3756f9bfbd84120b5ed1`

RED test blob:

`2305e0768182d82657c34a7cb53c502714a2ab81`

RED report blob:

`6de316c3c968c2b73122170bb2b86fbec6093951`

## Minimal additions

Only these new implementation artifacts were added:

- `tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json`
- `tools/obsidian_projection/p5e_near_real_time_model.py`

The model is synthetic and pure. It has no sleep, network, filesystem-state access, process launch, or real P5-D4/Vault access.

## Validation

Contract JSON parse:

`PASS`

Synthetic model compile:

`PASS`

Targeted test command:

```text
python -B -m unittest tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1
```

Observed clean recheck:

```text
Ran 17 tests in 0.009s

OK
```

## Qualified properties at this intermediate point

The minimal candidate now enforces/tests:

- exact 30-second inherited poll interval;
- exact 60-second detection-latency bound;
- explicit synthetic detection latency arithmetic;
- PASS for change just after a poll detected at the next 30-second slot;
- PASS for one transient read failure followed by success at the 60-second slot;
- FAIL for first detection after the 60-second bound;
- FAIL for no detection by the bound;
- rejection of non-30-second synthetic schedule points;
- no synthetic-to-real PASS laundering;
- no evaluation/promotion/publication/P6 authority;
- P5-D4 FIFO/no-coalescing queue semantics over earlier P5-A supersession design intent.

## Status

```text
P5E_V0_1_MINIMAL_GREEN
= 17 / 17 PASS

ADVERSARIAL_EXPANSION
= PENDING

REAL_P5E
= CLOSED
```

~~~~

# SOURCE: P5-E ADVERSARIAL QUALIFICATION

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-ADVERSARIAL-QUALIFICATION.md

~~~~
# P5-E V0.1 â€” ADVERSARIAL QUALIFICATION

Date: 2026-10-01

## Scope

Adversarial qualification of the P5-E V0.1 candidate contract and pure synthetic timing model.

No real polling, network observation loop, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was executed.

## Candidate identity before adversarial expansion

Minimal GREEN HEAD:

`2f7b16479149602da94c8434ddefe2104adfe4f9`

Contract blob:

`e5c3d7a9d451aba65e8062078c6c10d23e586f39`

Synthetic timing model blob:

`8662dd97a1c8a1af33d6593ae923384e96404b5a`

## Adversarial harness

`tests/obsidian_projection/test_p5e_end_to_end_near_real_time_adversarial_v0_1.py`

The harness independently mutates copies of the contract and requires those mutations to violate frozen invariants.

Mutation families include:

- poll interval 30 -> 31 seconds;
- detection bound 60 -> 61 seconds;
- real P5-E authority activation;
- evaluation authority activation;
- promotion authority activation;
- publication authority activation;
- real polling authority activation;
- P6 authority activation;
- queue coalescing reintroduction;
- latest-only pending-head replacement;
- queue-capacity silent continuation;
- P5-A historical supersession intent overriding qualified P5-D4 semantics;
- synthetic qualification relabelled as real P5-E qualification;
- removal of real-PASS claim prohibition.

Synthetic timing edge cases include:

- exactly 60-second detection boundary;
- apparent observation before source availability;
- negative/boolean source time;
- empty observation surface;
- duplicate observation time;
- invalid synthetic outcome;
- incomplete timing window;
- downstream authority remaining false for all model verdicts.

## Result

Command:

```text
python -B -m unittest \
  tests.obsidian_projection.test_p5e_end_to_end_near_real_time_contract_v0_1 \
  tests.obsidian_projection.test_p5e_end_to_end_near_real_time_adversarial_v0_1
```

Observed:

```text
Ran 42 tests in 0.027s

OK
```

No mechanical correction was required.

## Adjudication

```text
P5E_V0_1_BASE_TESTS
= 17 / 17 PASS

P5E_V0_1_COMBINED_ADVERSARIAL_SURFACE
= 42 / 42 PASS

CONTRACT_CORRECTION_REQUIRED
= FALSE

REAL_P5E
= CLOSED
```

~~~~

# SOURCE: P5-D4 LIFECYCLE REGRESSION CORRECTION

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-PREDECESSOR-REGRESSION-LIFECYCLE-CORRECTION.md

~~~~
# P5-E V0.1 â€” PREDECESSOR REGRESSION LIFECYCLE CORRECTION

Date: 2026-10-01

## Trigger

The first targeted predecessor regression after P5-E adversarial qualification executed 208 tests and returned 2 failures.

Both failures were in the already-qualified P5-D4 control-root remediation test surface:

- `test_03_exact_canonical_root_resolves_without_creating_it`
- `test_00_production_root_remains_absent_during_remediation`

Both asserted that the canonical P5-D4 production control root must be absent.

## Classification

This is not a P5-E runtime regression.

Those assertions were correct only during the earlier P5-D4 remediation qualification stage, when real production-root creation was explicitly forbidden.

After that stage:

- P5-D4 real bounded-loop requalification V0.2 was separately authorized;
- the canonical USERPROFILE root was created by exactly one real P5-D4 invocation;
- its physical binding was qualified;
- P5-D4 V0.2 was then human-adopted.

Therefore permanent root absence is now a stale phase-local assumption and contradicts the adopted lifecycle state.

## Mechanical correction

Only the two stale lifecycle assertions were changed.

The corrected tests now require:

- exact canonical USERPROFILE binding;
- resolver non-mutation of root existence state;
- if the root already exists, it must remain a directory;
- it must not be a symlink;
- where supported, it must not be a junction;
- resolving an existing root must not change its child-name set.

No runtime code was changed.

No old LocalAppData/Store redirect allowance was introduced.

No reparse protection was weakened.

No cross-interpreter binding check was removed.

## Targeted regression after correction

Command surface:

- P5-A continuous projection contract;
- P5-D1 observer core;
- P5-D2 one-shot observer tick;
- P5-D4 bounded-loop contract/runtime/adversarial;
- P5-D4 control-root remediation/base/adversarial;
- P5-E base/adversarial.

Observed result:

```text
Ran 208 tests in 3.159s

OK
```

Three Python bytecode files were generated by subprocess interpreter tests. They are runtime residue only and are removed before persistence.

The run also emitted non-failing `ResourceWarning` messages for unclosed subprocess text streams in the historical test harness. They did not change the test verdict.

## Adjudication

```text
P5E_TARGETED_PREDECESSOR_REGRESSION
= 208 / 208 PASS

P5D4_RUNTIME_MODIFICATION
= NONE

P5D4_BINDING_PROTECTION_WEAKENED
= FALSE

LIFECYCLE_ASSERTION_CORRECTION
= MECHANICAL_AND_REQUIRED

REAL_P5E
= CLOSED
```

~~~~

# SOURCE: P5-E TARGETED REGRESSION QUALIFICATION

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-TARGETED-REGRESSION-QUALIFICATION.md

~~~~
# P5-E V0.1 â€” TARGETED REGRESSION QUALIFICATION

Date: 2026-10-01

## Scope

This record consolidates the predecessor and cross-cutting regression evidence before the single preregistered full Obsidian re-break.

No real P5-E execution was performed.

## First targeted predecessor surface

Covered:

- P5-A continuous projection contract;
- P5-D1 observer core;
- P5-D2 one-shot observer tick;
- P5-D4 bounded-loop contract/runtime/adversarial;
- P5-D4 control-root binding base/adversarial;
- P5-E base/adversarial.

The initial run exposed two stale P5-D4 remediation-only assumptions that the production root must remain absent forever.

Those tests were mechanically corrected to reflect the later human-adopted P5-D4 V0.2 lifecycle without weakening binding, reparse, old-root rejection, or cross-interpreter controls.

Post-correction result:

```text
Ran 208 tests in 3.159s

OK
```

## Cross-cutting static/regression surface

Before consuming the one full re-break, 53 test modules containing cross-cutting tokens or repository-wide/static inspection behavior were selected.

Observed result:

```text
Ran 876 tests in 174.833s

OK
```

Non-failing observations:

- one sample-worktree LF/CRLF warning;
- existing `ResourceWarning` messages for historical subprocess text streams.

Neither changed the unittest verdict.

## Runtime identity preservation

P5-D4 runtime blob remained:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

No P5-D4 runtime implementation change was made.

## Adjudication

```text
P5E_TARGETED_PREDECESSOR_REGRESSION
= 208 / 208 PASS

P5E_CROSS_CUTTING_REGRESSION
= 876 / 876 PASS

P5D4_RUNTIME_CHANGE
= NONE

FULL_OBSIDIAN_REBREAK
= NOT_YET_CONSUMED

REAL_P5E
= CLOSED
```

The next operation is the one preregistered full `tests/obsidian_projection/test_*.py` re-break.

## Worktree provenance anomaly before full re-break

After the 876/876 cross-cutting PASS, a pre-persistence status check observed temporary worktree divergence in exactly:

- `tools/obsidian_projection/p5e_end_to_end_near_real_time_contract_v0_1.json`
- `tools/obsidian_projection/p5e_near_real_time_model.py`

Observed transient worktree blobs were:

- contract: `ec54aaee33fc5c56be3636392856766097ae3e50`
- model: `de9ad391664a2cb249ac28b1622814442092b27a`

The committed authoritative blobs remained:

- contract: `e5c3d7a9d451aba65e8062078c6c10d23e586f39`
- model: `8662dd97a1c8a1af33d6593ae923384e96404b5a`

No persistence of the transient content was attempted.

A subsequent 42-test P5-E run passed and the worktree files returned byte-for-byte to the committed authoritative blobs without a restoration action being issued by this qualification flow.

The cause is not proven and is therefore recorded as:

```text
WORKTREE_PROVENANCE_ANOMALY
= OBSERVED

CAUSE
= UNKNOWN

TRANSIENT_CONTENT_ADOPTED
= FALSE

TRANSIENT_CONTENT_PERSISTED
= FALSE
```

Because provenance is not established, the primary worktree is not used as the execution surface for the final full re-break.

The final full re-break must instead use a fresh disposable control clone fetched from the exact remote P5-E branch HEAD, verify clean state and exact origin identity before execution, and be discarded afterward.

~~~~

# SOURCE: P5-E FULL OBSIDIAN RE-BREAK

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-FULL-OBSIDIAN-REBREAK.md

~~~~
# P5-E V0.1 â€” FULL OBSIDIAN RE-BREAK

Date: 2026-10-01

## Scope

This is the single preregistered full Obsidian re-break for:

`P5-E â€” END-TO-END NEAR-REAL-TIME QUALIFICATION V0.1`

No real P5-E polling, remote observation loop, evaluation, promotion, publication, Vault mutation, Stage A, Stage B, P6, daemon, Scheduled Task, Windows Service, or startup registration was executed.

## Start identity

Full re-break started at:

`0e568da338043654de84949488413763f56d9cd9`

P5-D4 runtime blob before execution:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

The worktree contained no tracked modification. A targeted-regression report was concurrently being persisted by another authorized execution on the same branch.

## Concurrent documentation-only commit

During the full run, the branch advanced to:

`f146201301b150efb35713e7aed3f0105821d41c`

Commit:

`obsidian p5e: persist targeted regression qualification`

Patch scope:

```text
A reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-TARGETED-REGRESSION-QUALIFICATION.md
```

No runtime, test, contract, or model file changed in that concurrent commit.

Therefore the executable/test surface used by the full run remained unchanged.

## Command

```text
python -B -m unittest discover -s tests/obsidian_projection -p 'test_*.py'
```

## Result

```text
Ran 1466 tests in 250.650s

OK

FULL_EXIT=0
FULL_SECONDS=251.353
```

P5-D4 runtime blob after execution:

`1825e53d195ba2a63b5b646a5b78eb77939b94b5`

Runtime identity therefore remained unchanged.

## Non-failing observations

The run emitted:

- one sample-worktree LF/CRLF warning;
- historical `ResourceWarning` messages for unclosed subprocess text streams.

Neither altered the unittest result.

Three Python `__pycache__` files were generated by subprocess interpreter tests. They were classified as runtime residue and removed after the run.

## Adjudication

```text
FULL_OBSIDIAN_REBREAK
= 1466 / 1466 PASS

P5D4_RUNTIME_BLOB
= UNCHANGED

REAL_P5E
= CLOSED
```

This re-break is evidence for the contract/synthetic qualification stage only.

~~~~

# SOURCE: P5-E CONSOLIDATED QUALIFICATION

Path: reports/program/2026-10-01-OBSIDIAN-P5E-V0.1-CONTRACT-SYNTHETIC-QUALIFICATION.md

~~~~
# P5-E V0.1 â€” CONTRACT + SYNTHETIC QUALIFICATION

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

~~~~
