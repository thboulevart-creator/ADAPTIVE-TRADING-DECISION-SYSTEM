from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D3ACandidateEvaluationContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "candidate_evaluation_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_CANDIDATE_EVALUATION_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_exact_repository_and_branch_are_pinned(
        self,
    ) -> None:
        self.assertEqual(
            self.contract["source_repository"],
            (
                "thboulevart-creator/"
                "ADAPTIVE-TRADING-DECISION-SYSTEM"
            ),
        )
        self.assertEqual(
            self.contract["monitored_branch"],
            "integration/system-v1",
        )

    def test_p5d2_predecessor_is_exact(self) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5d2_contract_blob"],
            "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
        )
        self.assertEqual(
            p["p5d2_implementation_blob"],
            "fd212f61ec38332b677110f40265638af55a73e2",
        )
        self.assertEqual(
            p["p5d2_qualification_report_blob"],
            "68cda09d273f19a2a93e1fcd9b0c393e72cd5a35",
        )
        self.assertEqual(
            p["p5d2_qualification_commit"],
            "6096984eec9f923c31f70508cc7000408290fb56",
        )

    def test_dynamic_inventory_and_promotion_dependencies_are_pinned(
        self,
    ) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5b2_dynamic_inventory_implementation_blob"],
            "5f6ed61f36e889dc27ef14ef09467ada9f9f0f58",
        )
        self.assertEqual(
            p["p5b2_qualification_report_blob"],
            "286a81a4f3f71a1d857631c2388d7894908acb5f",
        )
        self.assertEqual(
            p["p5c2_promotion_qualification_report_blob"],
            "a928598182b25d110c9040c62d846bf9018ac3ed",
        )

    def test_p5d3a_is_finite_and_non_promoting(self) -> None:
        objective = self.contract["objective"]
        self.assertTrue(
            objective["one_candidate_per_invocation"]
        )
        self.assertTrue(
            objective["finite_execution_required"]
        )
        self.assertTrue(
            objective["background_loop_forbidden"]
        )
        self.assertTrue(
            objective["periodic_polling_forbidden"]
        )
        self.assertTrue(
            objective["automatic_promotion_forbidden"]
        )
        self.assertTrue(
            objective[
                "live_projection_mutation_during_evaluation_forbidden"
            ]
        )

    def test_activation_requires_p5d2_start_decision(
        self,
    ) -> None:
        activation = self.contract[
            "activation_contract"
        ]
        self.assertEqual(
            activation["required_decision_action"],
            "START_EXACT_HEAD_EVALUATION",
        )
        self.assertEqual(
            activation["required_observer_phase"],
            "EVALUATING",
        )
        self.assertTrue(
            activation[
                "candidate_head_must_equal_decision_candidate_head"
            ]
        )
        self.assertTrue(
            activation[
                "candidate_head_must_equal_pending_queue_head"
            ]
        )
        self.assertTrue(
            activation[
                "automatic_promotion_authorized_must_be_false"
            ]
        )
        self.assertTrue(
            activation[
                "production_write_authorized_must_be_false"
            ]
        )

    def test_live_authority_remains_unchanged(self) -> None:
        boundary = self.contract["authority_boundary"]
        self.assertEqual(
            boundary["live_projection"],
            "LAST_KNOWN_GOOD_UNCHANGED",
        )
        self.assertEqual(
            boundary["observer_state_mutation"],
            "ONLY_VIA_QUALIFIED_P5D2_ONE_SHOT_TICK",
        )
        self.assertFalse(
            boundary["evaluator_may_modify_real_vault"]
        )
        self.assertFalse(
            boundary["evaluator_may_promote_candidate"]
        )

    def test_workspace_isolation_is_explicit(self) -> None:
        isolation = self.contract[
            "workspace_isolation"
        ]
        for field in (
            "candidate_checkout_must_be_disposable",
            "candidate_checkout_outside_canonical_worktree",
            "candidate_checkout_outside_vault",
            "staging_root_outside_real_vault",
            "exact_repository_origin_required",
            "exact_branch_required",
            "exact_candidate_commit_required",
            "checkout_head_must_equal_candidate_head",
            "candidate_tree_identity_must_be_recorded",
            "canonical_worktree_status_must_remain_unchanged",
        ):
            with self.subTest(field=field):
                self.assertTrue(isolation[field])
        self.assertTrue(
            isolation[
                "git_worktree_registry_dependency_forbidden"
            ]
        )

    def test_pipeline_order_is_exact(self) -> None:
        self.assertEqual(
            self.contract["ordered_pipeline"],
            [
                "VALIDATE_P5D2_EVALUATION_ACTIVATION",
                "VERIFY_REPOSITORY_IDENTITY",
                "RESOLVE_EXACT_CANDIDATE_HEAD",
                "CREATE_ISOLATED_DISPOSABLE_CHECKOUT",
                "VERIFY_CHECKOUT_HEAD_AND_TREE",
                "BUILD_P5B2_DYNAMIC_INVENTORY",
                "VERIFY_DYNAMIC_INVENTORY_IDENTITY",
                "ADAPT_DYNAMIC_INVENTORY_TO_SEMANTIC_PROJECTION_INPUT",
                "CLASSIFY_CURRENT_HEAD_ARTIFACTS",
                "BUILD_DETERMINISTIC_PROJECTION_A",
                "BUILD_DETERMINISTIC_PROJECTION_B",
                "REQUIRE_A_EQUALS_B",
                "RUN_PREREGISTERED_PROJECTION_BREAKERS",
                "PACKAGE_COMPLETE_CANDIDATE_GENERATION",
                "VERIFY_COMPLETE_CANDIDATE_GENERATION",
                "CLASSIFY_EVALUATION_OUTCOME",
                "EMIT_P5D2_EVALUATION_RESULT_EVENT_IF_DETERMINATE",
                "APPLY_RESULT_ONLY_THROUGH_P5D2_ONE_SHOT_TICK",
                "RECORD_FINITE_EVALUATION_REPORT",
            ],
        )

    def test_any_failure_stops_later_gates(self) -> None:
        failure = self.contract[
            "pipeline_failure_rule"
        ]
        self.assertTrue(
            failure["any_gate_failure_stops_later_gates"]
        )
        self.assertTrue(
            failure[
                "partial_candidate_may_not_be_treated_as_qualified"
            ]
        )
        self.assertTrue(
            failure[
                "live_projection_head_must_remain_unchanged"
            ]
        )
        self.assertTrue(
            failure["real_vault_must_remain_unchanged"]
        )

    def test_dynamic_inventory_is_exact_head_bound(
        self,
    ) -> None:
        binding = self.contract[
            "dynamic_inventory_binding"
        ]
        self.assertEqual(
            binding["required_schema"],
            "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1",
        )
        self.assertTrue(
            binding[
                "source_commit_must_equal_candidate_head"
            ]
        )
        self.assertTrue(
            binding[
                "source_tree_must_equal_checkout_tree"
            ]
        )
        self.assertTrue(
            binding["inventory_digest_must_be_recorded"]
        )

    def test_semantic_bridge_gap_is_explicit(self) -> None:
        gap = self.contract[
            "current_head_semantic_bridge_gap"
        ]
        self.assertEqual(
            gap["status"],
            "OPEN_REQUIRED_SUBFRONTIER",
        )
        self.assertEqual(
            gap["dynamic_inventory_schema"],
            "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_V0_1",
        )
        self.assertEqual(
            gap["legacy_classifier_input_type"],
            "FrozenInventory",
        )
        self.assertEqual(
            gap["legacy_pilot_inventory_schema"],
            "ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1",
        )
        self.assertEqual(
            gap["legacy_p2_exact_record_count"],
            74,
        )
        self.assertTrue(
            gap["implicit_conversion_forbidden"]
        )
        self.assertTrue(
            gap[
                "hardcoded_74_record_expectation_for_continuous_candidate_forbidden"
            ]
        )
        self.assertTrue(
            gap["bridge_contract_required_before_orchestrator"]
        )

    def test_semantic_bridge_must_explicitly_dispose_every_entry(
        self,
    ) -> None:
        bridge = self.contract[
            "semantic_projection_bridge_requirements"
        ]
        self.assertTrue(
            bridge[
                "every_dynamic_inventory_entry_must_receive_explicit_disposition"
            ]
        )
        self.assertTrue(bridge["silent_drop_forbidden"])
        self.assertTrue(
            bridge["source_path_identity_must_be_preserved"]
        )
        self.assertTrue(
            bridge["source_blob_identity_must_be_preserved"]
        )
        self.assertTrue(
            bridge["source_commit_identity_must_be_preserved"]
        )
        self.assertTrue(
            bridge["source_tree_identity_must_be_preserved"]
        )
        self.assertTrue(
            bridge["unsupported_artifact_must_fail_closed"]
        )

    def test_double_build_is_strict(self) -> None:
        db = self.contract[
            "deterministic_double_build"
        ]
        self.assertTrue(db["required"])
        for field in (
            "build_a_and_b_use_same_candidate_head",
            "build_a_and_b_use_same_candidate_tree",
            "build_a_and_b_use_same_inventory_digest",
            "build_a_and_b_use_same_semantic_input_digest",
            "build_a_and_b_use_same_projection_contract_version",
            "independent_stage_roots_required",
            "exact_file_map_equality_required",
            "projection_tree_digest_equality_required",
            "semantic_record_digest_equality_required",
            "manifest_digest_equality_required",
            "generated_file_count_equality_required",
            "any_mismatch_is_candidate_rejection",
        ):
            with self.subTest(field=field):
                self.assertTrue(db[field])

    def test_breakers_require_preregistered_manifest(
        self,
    ) -> None:
        boundary = self.contract[
            "projection_breaker_boundary"
        ]
        self.assertTrue(
            boundary[
                "preregistered_breaker_manifest_required"
            ]
        )
        self.assertTrue(
            boundary["breaker_manifest_digest_required"]
        )
        self.assertTrue(
            boundary[
                "vague_run_all_tests_instruction_insufficient"
            ]
        )
        self.assertTrue(
            boundary[
                "breaker_failure_is_candidate_rejection"
            ]
        )
        self.assertTrue(
            boundary[
                "breaker_infrastructure_failure_is_blocked_not_rejected"
            ]
        )

    def test_generation_packaging_gap_is_explicit(
        self,
    ) -> None:
        gap = self.contract[
            "candidate_generation_packaging_gap"
        ]
        self.assertEqual(
            gap["status"],
            "OPEN_REQUIRED_SUBFRONTIER",
        )
        self.assertTrue(
            gap[
                "p5c2_fixture_generation_may_not_be_relabelled_as_real_projection_packaging"
            ]
        )
        self.assertTrue(
            gap[
                "real_candidate_generation_contract_required_before_orchestrator"
            ]
        )
        self.assertTrue(
            gap[
                "promotion_primitive_invocation_during_p5d3_forbidden"
            ]
        )

    def test_candidate_generation_identity_is_complete(
        self,
    ) -> None:
        generation = self.contract[
            "candidate_generation_requirements"
        ]
        required = set(
            generation[
                "generation_identity_required_fields"
            ]
        )
        for field in (
            "candidate_head",
            "candidate_tree",
            "dynamic_inventory_digest",
            "semantic_bridge_digest",
            "semantic_record_digest",
            "projection_contract_version",
            "projection_tree_digest",
            "generated_file_count",
            "breaker_manifest_digest",
        ):
            with self.subTest(field=field):
                self.assertIn(field, required)
        self.assertTrue(
            generation[
                "generation_must_be_staged_outside_live_vault"
            ]
        )
        self.assertTrue(
            generation["pointer_or_current_mutation_forbidden"]
        )

    def test_outcome_model_separates_rejected_and_blocked(
        self,
    ) -> None:
        outcomes = self.contract["outcome_model"]
        self.assertEqual(
            outcomes["allowed_outcomes"],
            ["QUALIFIED", "REJECTED", "BLOCKED"],
        )
        self.assertTrue(
            outcomes[
                "blocked_must_not_be_relabelled_rejected"
            ]
        )
        self.assertTrue(
            outcomes[
                "rejected_must_not_be_relabelled_blocked_to_hide_candidate_failure"
            ]
        )

    def test_blocked_emits_no_p5d2_result_event(self) -> None:
        policy = self.contract[
            "p5d2_result_event_policy"
        ]
        self.assertEqual(
            policy["qualified_emits"],
            "EVALUATION_PASSED",
        )
        self.assertEqual(
            policy["rejected_emits"],
            "EVALUATION_FAILED",
        )
        self.assertIsNone(policy["blocked_emits"])
        self.assertEqual(
            policy["blocked_observer_state_remains"],
            "EVALUATING",
        )
        self.assertTrue(
            policy["blocked_event_sequence_does_not_advance"]
        )
        self.assertTrue(
            policy[
                "result_event_must_be_applied_by_qualified_p5d2_one_shot_tick"
            ]
        )
        self.assertTrue(
            policy["direct_observer_state_mutation_forbidden"]
        )

    def test_report_preserves_live_head_and_vault(
        self,
    ) -> None:
        report = self.contract["evaluation_report"]
        self.assertTrue(
            report[
                "live_projection_head_after_must_equal_before"
            ]
        )
        self.assertTrue(
            report["real_vault_modified_must_be_false"]
        )
        self.assertTrue(
            report[
                "production_promotion_authorized_must_be_false"
            ]
        )

    def test_retry_semantics_are_fail_closed(self) -> None:
        retry = self.contract[
            "recovery_and_retry"
        ]
        self.assertTrue(
            retry[
                "blocked_evaluation_may_be_retried_against_same_exact_candidate_head"
            ]
        )
        self.assertTrue(
            retry["retry_must_revalidate_all_identity_gates"]
        )
        self.assertTrue(
            retry[
                "retry_must_not_reuse_unverified_partial_candidate_as_qualified"
            ]
        )
        self.assertTrue(
            retry[
                "qualified_staged_candidate_still_requires_separate_promotion_authority"
            ]
        )

    def test_p5d3a_authorizes_no_runtime(self) -> None:
        boundary = self.contract["p5d3a_boundary"]
        self.assertTrue(
            boundary["contract_and_breakers_only"]
        )
        for field in (
            "semantic_bridge_implementation_authorized",
            "candidate_generation_packager_authorized",
            "evaluation_orchestrator_implementation_authorized",
            "network_fetch_execution_authorized",
            "isolated_checkout_execution_authorized",
            "candidate_breaker_execution_authorized",
            "p5d2_result_event_execution_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "production_promotion_authorized",
            "continuous_vault_write_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_breaker_registry_is_broad_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 80)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gates_are_exact_and_ordered(
        self,
    ) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            list(gates.keys()),
            [
                "p5d3b",
                "p5d3c",
                "p5d3d",
                "p5d3e",
                "p5d4",
                "p5e",
                "p6",
            ],
        )
        self.assertEqual(
            gates["p5d3b"],
            "CURRENT_HEAD_SEMANTIC_PROJECTION_BRIDGE",
        )
        self.assertEqual(
            gates["p5d3c"],
            "CANDIDATE_GENERATION_STAGING_CONTRACT",
        )
        self.assertEqual(
            gates["p5d3d"],
            "FINITE_CANDIDATE_EVALUATION_ORCHESTRATOR",
        )
        self.assertEqual(
            gates["p5d3e"],
            "SANDBOX_CANDIDATE_EVALUATION_QUALIFICATION",
        )


if __name__ == "__main__":
    unittest.main()
