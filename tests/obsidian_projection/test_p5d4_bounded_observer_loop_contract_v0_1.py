import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "p5d4_bounded_observer_loop_contract_v0_1.json"
)
EXPECTED_CONTRACT_BLOB = "6980de1eb55e49c0c2bd2f91620aeb75640753b6"


def _blob(relative: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


class P5D4BoundedObserverLoopContractV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.path = REPO_ROOT / CONTRACT_RELATIVE
        cls.contract = json.loads(cls.path.read_text(encoding="utf-8"))

    def test_contract_blob_is_exact(self) -> None:
        self.assertEqual(_blob(CONTRACT_RELATIVE), EXPECTED_CONTRACT_BLOB)

    def test_schema_status_repository_and_frontier_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D4_BOUNDED_OBSERVER_LOOP_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["source_repository"],
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D4-BOUNDED-OBSERVER-LOOP-CANDIDATE",
        )

    def test_monitored_source_is_remote_authority(self) -> None:
        monitored = self.contract["monitored_source"]
        self.assertEqual(monitored["remote"], "origin")
        self.assertEqual(monitored["branch"], "integration/system-v1")
        self.assertEqual(
            monitored["canonical_authority"],
            "GITHUB_REMOTE_BRANCH",
        )
        self.assertTrue(monitored["local_working_tree_is_not_authority"])

    def test_qualified_predecessors_are_exactly_pinned(self) -> None:
        expected = {
            "p5d1_observer_core_contract_blob":
                "a20999ae991e07447e25ecd1592964f2d333449b",
            "p5d2_one_shot_contract_blob":
                "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
            "p5d2_observer_tick_blob":
                "fd212f61ec38332b677110f40265638af55a73e2",
            "p5d3d_finite_evaluator_contract_blob":
                "b6c17167875874db30a575be95e8e6aa33d630dd",
            "p5d3d_finite_evaluator_blob":
                "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
            "p5d3e_real_exact_head_sandbox_contract_blob":
                "ae4b1691fae16fcd1616e265a089670b9654db4a",
            "p5d3e_verifier_blob":
                "bd7f63b08432a53eaff5deeb2147396eb60d723f",
            "p5d3f_handoff_contract_blob":
                "64744325251db350d26c0269090ce62d5fa5f2e8",
            "p5d3f_handoff_blob":
                "23a4cc69b3b9f6fab1a6d77bed0247fce9b69c60",
            "p5d3g_live_publication_contract_blob":
                "64997ddd9977229961387f66af4de356c045c0ac",
            "p5d3g_live_publication_blob":
                "956ccb7274cea366b1a414df5a9239cbf580e3bf",
            "p5d3g_stage_b_gate_contract_blob":
                "c5c7fbb52f3dd2e3d3f5d1c1bbdc1069e2dabead",
            "p5d3g_stage_b_prestate_rebind_amendment_blob":
                "441fea40d33aa85dcfc6305d4d32cef39c42388e",
            "p5d3g_stage_b_runtime_blob":
                "077ea7a428f90d64122f15fe6b52f342f329f7b6",
        }
        self.assertEqual(self.contract["qualified_predecessors"], expected)

    def test_only_p5d2_may_mutate_observer_semantic_state(self) -> None:
        authority = self.contract["core_authority_model"]
        self.assertEqual(
            authority["observer_semantic_state_mutation_authority"],
            "P5D2_ONE_SHOT_TICK_ONLY",
        )
        self.assertTrue(authority["direct_observer_state_mutation_forbidden"])
        self.assertTrue(authority["p5d3_primitive_reimplementation_forbidden"])

    def test_loop_authority_is_not_promotion_authority(self) -> None:
        authority = self.contract["core_authority_model"]
        self.assertTrue(authority["loop_authority_is_not_promotion_authority"])
        self.assertTrue(
            authority["qualified_candidate_requires_separate_promotion_authority"]
        )
        self.assertEqual(
            authority["candidate_pending_without_separate_authority_result"],
            "PROMOTION_AUTHORITY_REQUIRED",
        )
        self.assertFalse(authority["automatic_live_publication_authorized"])
        self.assertFalse(authority["implicit_stage_a_authority_authorized"])
        self.assertFalse(authority["implicit_stage_b_authority_authorized"])
        self.assertTrue(
            authority["historical_stage_a_or_stage_b_authority_reuse_forbidden"]
        )

    def test_six_new_contract_surfaces_exist(self) -> None:
        for key in (
            "bounded_loop_envelope",
            "durable_observer_state_checkpoint",
            "append_only_observer_event_log",
            "queue_capacity_policy",
            "single_instance_ownership",
            "restart_reconciliation_protocol",
        ):
            with self.subTest(key=key):
                self.assertIn(key, self.contract)

    def test_bounded_loop_requires_finite_explicit_limits(self) -> None:
        loop = self.contract["bounded_loop_envelope"]
        self.assertTrue(loop["every_run_requires_explicit_canonical_plan"])
        self.assertTrue(loop["plan_digest_required"])
        self.assertTrue(loop["unbounded_defaults_forbidden"])
        limits = loop["required_limits"]
        self.assertEqual(limits["max_cycles"]["minimum"], 1)
        self.assertEqual(limits["max_remote_observations"]["minimum"], 1)
        self.assertEqual(limits["max_evaluations"]["minimum"], 0)
        self.assertEqual(limits["max_pending_heads"]["minimum"], 1)
        self.assertEqual(limits["max_consecutive_failures"]["minimum"], 0)
        self.assertTrue(
            loop["cycle_budget_consumed_exactly_once_per_started_cycle"]
        )
        self.assertTrue(loop["budget_check_required_before_starting_next_cycle"])
        self.assertTrue(loop["loop_construct_without_verified_budget_forbidden"])

    def test_bound_stop_does_not_forge_p5d2_shutdown(self) -> None:
        loop = self.contract["bounded_loop_envelope"]
        self.assertTrue(loop["bound_reached_must_not_inject_p5d2_shutdown_event"])
        self.assertTrue(loop["bound_reached_is_runner_stop_not_semantic_state_transition"])
        self.assertTrue(loop["new_cycle_after_terminal_reason_forbidden"])

    def test_terminal_reasons_are_explicit_and_include_authority_stop(self) -> None:
        reasons = set(self.contract["bounded_loop_envelope"]["allowed_terminal_reasons"])
        required = {
            "BOUND_REACHED",
            "NO_PENDING_WORK",
            "BLOCKED_REQUIRES_ADJUDICATION",
            "PROMOTION_AUTHORITY_REQUIRED",
            "LOCK_CONTENDED",
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
            "RECONCILIATION_REQUIRED",
            "FATAL_INCONSISTENCY",
        }
        self.assertTrue(required.issubset(reasons))

    def test_checkpoint_is_outside_vault_and_transactional(self) -> None:
        checkpoint = self.contract["durable_observer_state_checkpoint"]
        self.assertEqual(
            checkpoint["location_class"],
            "LOCALAPPDATA_OUTSIDE_VAULT",
        )
        self.assertTrue(checkpoint["inside_real_vault_forbidden"])
        self.assertTrue(checkpoint["inside_canonical_repository_forbidden"])
        self.assertTrue(checkpoint["canonical_json_required"])
        self.assertTrue(checkpoint["sha256_required"])
        self.assertTrue(checkpoint["direct_in_place_checkpoint_overwrite_forbidden"])
        self.assertTrue(
            checkpoint["checkpoint_may_not_be_committed_before_corresponding_event"]
        )

    def test_checkpoint_commit_protocol_is_write_ahead_event_then_atomic_state(self) -> None:
        checkpoint = self.contract["durable_observer_state_checkpoint"]
        self.assertEqual(
            checkpoint["commit_protocol"],
            [
                "BUILD_NEXT_STATE_ONLY_VIA_P5D2_ONE_SHOT_TICK",
                "BUILD_CANONICAL_LOOP_EVENT",
                "APPEND_AND_DURABLY_FLUSH_LOOP_EVENT",
                "WRITE_CHECKPOINT_TO_SIBLING_TEMP",
                "DURABLY_FLUSH_CHECKPOINT_TEMP",
                "ATOMIC_REPLACE_CHECKPOINT",
                "VERIFY_CHECKPOINT_READ_AFTER_WRITE",
            ],
        )

    def test_checkpoint_excludes_volatile_host_data_from_semantic_digest(self) -> None:
        excluded = set(
            self.contract["durable_observer_state_checkpoint"][
                "volatile_host_data_excluded_from_observer_state_digest"
            ]
        )
        self.assertEqual(
            excluded,
            {
                "pid",
                "hostname",
                "wall_clock_time",
                "absolute_runtime_path",
                "process_start_time",
            },
        )

    def test_event_log_is_append_only_hash_chained_evidence(self) -> None:
        log = self.contract["append_only_observer_event_log"]
        self.assertEqual(log["format"], "CANONICAL_JSONL")
        self.assertTrue(log["append_only"])
        self.assertTrue(log["truncate_forbidden"])
        self.assertTrue(log["rewrite_prior_record_forbidden"])
        self.assertTrue(log["durable_flush_required_before_checkpoint_replace"])
        self.assertTrue(log["every_accepted_p5d2_tick_requires_record"])
        self.assertTrue(log["hash_chain_required"])
        self.assertTrue(log["sequence_strictly_monotonic"])
        self.assertTrue(log["duplicate_sequence_forbidden"])
        self.assertTrue(log["event_log_is_evidence_not_source_authority"])

    def test_event_log_binds_state_and_previous_record(self) -> None:
        required = set(
            self.contract["append_only_observer_event_log"]["required_fields"]
        )
        for field in (
            "sequence",
            "normalized_input",
            "p5d2_audit",
            "previous_state_digest_sha256",
            "next_state_digest_sha256",
            "previous_record_digest_sha256",
            "record_digest_sha256",
            "record_origin",
        ):
            with self.subTest(field=field):
                self.assertIn(field, required)

    def test_queue_is_fifo_unique_bounded_and_never_silently_rewritten(self) -> None:
        queue = self.contract["queue_capacity_policy"]
        self.assertEqual(queue["runtime_capacity_source"], "loop_plan.max_pending_heads")
        self.assertTrue(queue["fifo_required"])
        self.assertTrue(queue["unique_heads_required"])
        self.assertTrue(queue["silent_drop_forbidden"])
        self.assertTrue(queue["silent_reorder_forbidden"])
        self.assertTrue(queue["latest_only_replacement_forbidden"])
        self.assertTrue(queue["direct_queue_mutation_outside_p5d2_forbidden"])
        self.assertFalse(queue["coalescing_authorized"])
        self.assertEqual(
            queue["capacity_exhausted_result"],
            "QUEUE_CAPACITY_REQUIRES_ADJUDICATION",
        )
        self.assertTrue(queue["active_evaluation_candidate_retargeting_forbidden"])

    def test_single_instance_ownership_fails_closed(self) -> None:
        ownership = self.contract["single_instance_ownership"]
        self.assertTrue(ownership["required"])
        self.assertTrue(ownership["exclusive_ownership_record_required"])
        self.assertEqual(
            ownership["second_instance_result"],
            "NO_WRITE_BLOCKED_BY_LOCK",
        )
        self.assertFalse(ownership["second_instance_may_advance_sequence"])
        self.assertFalse(ownership["second_instance_may_modify_checkpoint"])
        self.assertFalse(ownership["second_instance_may_append_event"])
        self.assertFalse(ownership["second_instance_may_start_evaluation"])
        self.assertFalse(ownership["stale_or_ambiguous_lock_auto_steal_authorized"])
        self.assertEqual(
            ownership["stale_or_ambiguous_lock_result"],
            "BLOCKED_REQUIRES_ADJUDICATION",
        )

    def test_reconciliation_authority_order_is_explicit(self) -> None:
        restart = self.contract["restart_reconciliation_protocol"]
        self.assertEqual(
            restart["authority_order"],
            [
                "GITHUB_REMOTE_BRANCH_SOURCE_AUTHORITY",
                "VERIFIED_PHYSICAL_CURRENT_PUBLICATION_FACT",
                "P5D4_CHECKPOINT_DERIVED_OPERATIONAL_STATE",
                "P5D4_EVENT_LOG_AUDIT_EVIDENCE",
            ],
        )
        self.assertTrue(restart["fresh_remote_read_only_observation_required"])
        self.assertTrue(restart["physical_current_verification_required"])

    def test_only_one_log_record_ahead_is_recoverable(self) -> None:
        restart = self.contract["restart_reconciliation_protocol"]
        self.assertEqual(
            restart["allowed_checkpoint_log_relation"],
            [
                "EXACTLY_ALIGNED",
                "LOG_EXACTLY_ONE_RECORD_AHEAD_WITH_REPLAYABLE_TRANSITION",
            ],
        )
        self.assertTrue(restart["checkpoint_ahead_of_log_forbidden"])
        self.assertTrue(restart["log_more_than_one_record_ahead_forbidden"])
        replay = restart["one_record_ahead_recovery"]
        self.assertTrue(replay["requires_previous_state_digest_match_checkpoint"])
        self.assertTrue(
            replay["requires_deterministic_replay_via_p5d2_one_shot_tick"]
        )
        self.assertTrue(replay["requires_replayed_next_state_digest_match_log"])

    def test_existing_current_first_bootstrap_requires_evidence_reconstruction(self) -> None:
        restart = self.contract["restart_reconciliation_protocol"]
        self.assertEqual(
            restart["no_checkpoint_no_log_current_present_result"],
            "EVIDENCE_RECONSTRUCTION_REQUIRED",
        )
        reconstruction = restart["evidence_reconstruction"]
        self.assertTrue(reconstruction["direct_state_assignment_forbidden"])
        self.assertTrue(reconstruction["must_start_from_p5d2_make_initial_state"])
        self.assertTrue(
            reconstruction["must_use_p5d2_one_shot_tick_for_each_semantic_transition"]
        )
        self.assertTrue(reconstruction["verified_current_identity_required"])
        self.assertTrue(
            reconstruction["matching_p5d3g_physical_and_logical_receipts_required"]
        )
        self.assertTrue(
            reconstruction["reconstruction_must_not_claim_new_evaluation_or_new_publication_execution"]
        )

    def test_remote_io_stays_outside_p5d2_and_time_polling_stays_closed(self) -> None:
        boundary = self.contract["observation_adapter_boundary"]
        self.assertTrue(boundary["remote_io_outside_p5d2_required"])
        self.assertTrue(boundary["normalized_event_injection_required"])
        self.assertTrue(boundary["one_shot_tick_network_io_remains_forbidden"])
        self.assertTrue(boundary["real_remote_observation_may_use_read_only_git"])
        self.assertFalse(boundary["time_based_polling_in_p5d4_v0_1_authorized"])
        self.assertFalse(boundary["sleep_or_timer_authorized"])
        self.assertTrue(boundary["p5e_owns_near_real_time_polling_qualification"])

    def test_evaluation_reuses_finite_evaluator_and_may_not_retarget(self) -> None:
        evaluation = self.contract["evaluation_orchestration"]
        self.assertEqual(
            evaluation["evaluation_may_start_only_on_p5d2_action"],
            "START_EXACT_HEAD_EVALUATION",
        )
        self.assertTrue(evaluation["evaluation_candidate_must_equal_queue_head"])
        self.assertTrue(evaluation["candidate_head_frozen_for_entire_finite_evaluation"])
        self.assertTrue(evaluation["active_evaluation_retarget_forbidden"])
        self.assertTrue(evaluation["finite_evaluator_reuse_required"])
        self.assertTrue(evaluation["qualified_evaluator_reimplementation_forbidden"])
        self.assertTrue(evaluation["blocked_and_rejected_semantics_must_remain_distinct"])

    def test_candidate_pending_stops_without_separate_promotion_authority(self) -> None:
        promotion = self.contract["promotion_boundary"]
        self.assertTrue(
            promotion["candidate_pending_is_terminal_for_automatic_p5d4_orchestration"]
        )
        self.assertEqual(
            promotion["required_stop_reason_without_separate_authority"],
            "PROMOTION_AUTHORITY_REQUIRED",
        )
        self.assertTrue(
            promotion["p5d3f_or_p5d3g_invocation_from_loop_without_separate_authority_forbidden"]
        )
        self.assertTrue(promotion["automatic_stage_a_authority_forbidden"])
        self.assertTrue(promotion["automatic_stage_b_authority_forbidden"])
        self.assertTrue(promotion["old_authorization_reuse_forbidden"])

    def test_promotion_result_can_reenter_state_only_from_verified_external_evidence(self) -> None:
        promotion = self.contract["promotion_boundary"]
        self.assertTrue(
            promotion["promotion_confirmed_may_enter_observer_state_only_from_verified_external_promotion_evidence"]
        )
        self.assertTrue(
            promotion["promotion_failed_may_enter_observer_state_only_from_verified_external_failure_evidence"]
        )

    def test_contract_only_boundary_closes_all_runtime_and_future_authority(self) -> None:
        boundary = self.contract["contract_only_boundary"]
        self.assertTrue(boundary["contract_and_tests_only"])
        closed = (
            "loop_runtime_creation_authorized",
            "loop_runtime_modification_authorized",
            "bounded_loop_execution_authorized",
            "repeated_real_polling_authorized",
            "sleep_authorized",
            "timer_authorized",
            "permanent_daemon_authorized",
            "windows_startup_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "real_vault_mutation_authorized",
            "automatic_publication_authorized",
            "implicit_stage_a_authority_authorized",
            "implicit_stage_b_authority_authorized",
            "p5e_authorized",
            "p6_authorized",
        )
        for field in closed:
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_required_breakers_cover_all_authorized_adversarial_families(self) -> None:
        breakers = set(self.contract["required_breakers"])
        required = {
            "UNBOUNDED_LOOP_PLAN_ACCEPTED",
            "CYCLE_STARTED_AFTER_BUDGET_EXHAUSTED",
            "DIRECT_OBSERVER_STATE_MUTATION",
            "CHECKPOINT_COMMITTED_BEFORE_EVENT_APPEND",
            "CHECKPOINT_STATE_DIGEST_MISMATCH",
            "EVENT_LOG_TRUNCATED",
            "EVENT_HASH_CHAIN_BROKEN",
            "CHECKPOINT_AHEAD_OF_EVENT_LOG",
            "QUEUE_OVERFLOW_SILENT_DROP",
            "QUEUE_REORDERED",
            "QUEUE_MUTATED_OUTSIDE_P5D2",
            "ACTIVE_EVALUATION_RETARGETED",
            "SECOND_LOOP_RUNNER_ADVANCES_SEQUENCE",
            "STALE_LOCK_AUTO_STOLEN",
            "RESTART_CONTINUES_WITHOUT_RECONCILIATION",
            "CURRENT_DIFFERS_FROM_CHECKPOINT_LIVE_HEAD",
            "RESTART_REPEATS_COMPLETED_PROMOTION",
            "BOOTSTRAP_CURRENT_PRESENT_DIRECT_STATE_ASSIGNMENT",
            "SAME_HEAD_TRIGGERS_EVALUATION",
            "NON_FAST_FORWARD_CONTINUES_AUTOMATICALLY",
            "UNKNOWN_ANCESTRY_CONTINUES_AUTOMATICALLY",
            "BLOCKED_RESULT_RELABELED_REJECTED",
            "REJECTED_RESULT_RELABELED_BLOCKED",
            "P5D3_FINITE_EVALUATOR_REIMPLEMENTED",
            "CANDIDATE_PENDING_AUTO_PUBLISHED",
            "P5D3G_CALLED_WITHOUT_SEPARATE_AUTHORITY",
            "OLD_STAGE_B_AUTHORITY_REUSED",
            "LOOP_PUSHES_TO_GITHUB",
            "LOOP_MUTATES_CANONICAL_WORKTREE",
            "LOOP_OVERWRITES_HUMAN_VIEWS",
            "LOOP_MODIFIES_OBSIDIAN_CONFIG",
            "REAL_VAULT_WRITE_SURFACE_INTRODUCED",
            "PERMANENT_DAEMON_SURFACE_INTRODUCED",
            "SLEEP_OR_TIMER_SURFACE_INTRODUCED",
            "SCHEDULED_TASK_SURFACE_INTRODUCED",
            "WINDOWS_SERVICE_SURFACE_INTRODUCED",
            "P5E_AUTHORITY_LEAK",
            "P6_AUTHORITY_LEAK",
        }
        self.assertTrue(required.issubset(breakers))

    def test_qualification_requires_contract_and_predecessor_tests_only(self) -> None:
        q = self.contract["qualification_requirements"]
        self.assertTrue(q["static_contract_tests_required"])
        self.assertTrue(q["predecessor_pin_tests_required"])
        self.assertTrue(q["breaker_coverage_tests_required"])
        self.assertFalse(q["runtime_tests_required"])
        self.assertFalse(q["real_loop_execution_required"])
        self.assertFalse(q["real_vault_access_required"])

    def test_next_gate_is_runtime_candidate_but_requires_human_stop(self) -> None:
        next_gate = self.contract["next_gate"]
        self.assertEqual(
            next_gate["after_contract_qualification"],
            "P5-D4-BOUNDED-OBSERVER-LOOP-RUNTIME-IMPLEMENTATION-CANDIDATE",
        )
        self.assertEqual(
            next_gate["p5e"],
            "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
        )
        self.assertEqual(
            next_gate["p6"],
            "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
        )
        self.assertTrue(next_gate["mandatory_human_stop_before_runtime"])

    def test_no_p5d4_runtime_python_surface_exists(self) -> None:
        tools = REPO_ROOT / "tools" / "obsidian_projection"
        runtime_candidates = sorted(
            path.name for path in tools.glob("p5d4*.py")
        )
        self.assertEqual(runtime_candidates, [])


if __name__ == "__main__":
    unittest.main()
