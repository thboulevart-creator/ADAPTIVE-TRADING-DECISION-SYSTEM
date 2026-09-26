from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5AContinuousProjectionContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "continuous_projection_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_is_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_CONTINUOUS_PROJECTION_CONTRACT_V0_1",
        )

    def test_status_is_candidate_only(self) -> None:
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_predecessor_is_exact_p4c_closure(self) -> None:
        self.assertEqual(
            self.contract["predecessor_p4c_head"],
            "10355f467ccf8f87070ab18839b96ba6fc547d9d",
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
        monitored = self.contract["monitored_source"]
        self.assertEqual(
            monitored["remote"],
            "origin",
        )
        self.assertEqual(
            monitored["branch"],
            "integration/system-v1",
        )

    def test_observed_head_is_evidence_not_fixed_runtime_head(
        self,
    ) -> None:
        monitored = self.contract["monitored_source"]
        self.assertEqual(
            monitored["observed_head_at_preregistration"],
            "6aef3b1304313c3446c08a3a37b51ea61733f41e",
        )
        self.assertTrue(
            monitored[
                "local_working_tree_is_not_authority"
            ]
        )

    def test_delivery_is_bounded_near_realtime(
        self,
    ) -> None:
        objective = self.contract["objective"]
        self.assertEqual(
            objective["delivery_semantics"],
            "NEAR_REAL_TIME_BOUNDED_LATENCY",
        )
        self.assertTrue(
            objective[
                "instantaneous_realtime_claim_forbidden"
            ]
        )
        self.assertLessEqual(
            objective[
                "target_detection_latency_seconds_max"
            ],
            60,
        )

    def test_local_remote_ref_observer_selected(
        self,
    ) -> None:
        architecture = self.contract[
            "architecture_choice"
        ]
        self.assertEqual(
            architecture["selected_candidate"],
            "LOCAL_REMOTE_REF_OBSERVER",
        )
        self.assertIn(
            "OBSIDIAN_GIT_AUTO_PULL_PUSH",
            architecture["rejected_initial_mechanisms"],
        )
        self.assertIn(
            "GITHUB_ACTION_DIRECT_TO_LOCAL_VAULT",
            architecture["rejected_initial_mechanisms"],
        )

    def test_github_remains_canonical(self) -> None:
        authority = self.contract[
            "authority_boundary"
        ]
        self.assertEqual(
            authority["github_remote_branch"],
            "CANONICAL",
        )
        self.assertEqual(
            authority["projection"],
            "DERIVED",
        )
        self.assertFalse(
            authority["observer_may_push_to_github"]
        )
        self.assertFalse(
            authority["observer_may_commit_to_github"]
        )

    def test_canonical_worktree_mutation_forbidden(
        self,
    ) -> None:
        isolation = self.contract[
            "runtime_isolation"
        ]
        self.assertTrue(
            isolation[
                "canonical_user_repo_mutation_forbidden"
            ]
        )
        self.assertTrue(
            isolation[
                "build_checkout_must_be_disposable"
            ]
        )
        self.assertTrue(
            isolation[
                "build_must_not_use_user_worktree_registry"
            ]
        )

    def test_remote_observation_is_read_only(self) -> None:
        observation = self.contract[
            "remote_observation"
        ]
        self.assertEqual(
            observation["operation_class"],
            "READ_ONLY_REMOTE_REF_CHECK",
        )
        self.assertEqual(
            observation[
                "repeated_same_head_result"
            ],
            "NOOP",
        )
        self.assertEqual(
            observation["new_head_result"],
            "QUEUE_EXACT_HEAD_FOR_QUALIFICATION",
        )

    def test_network_failure_never_promotes(self) -> None:
        observation = self.contract[
            "remote_observation"
        ]
        self.assertEqual(
            observation["network_failure_result"],
            "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
        )

    def test_fast_forward_policy_is_explicit(self) -> None:
        policy = self.contract[
            "head_transition_policy"
        ]
        self.assertEqual(
            policy["automatic_promotion_allowed_for"],
            [
                "INITIAL",
                "FAST_FORWARD",
            ],
        )
        self.assertEqual(
            policy["non_fast_forward_result"],
            "BLOCKED_REQUIRES_ADJUDICATION",
        )
        self.assertEqual(
            policy["unknown_ancestry_result"],
            "BLOCKED_REQUIRES_ADJUDICATION",
        )

    def test_head_events_are_not_silently_lost(self) -> None:
        policy = self.contract[
            "event_coalescing"
        ]
        self.assertTrue(
            policy[
                "every_observed_head_must_be_logged"
            ]
        )
        self.assertTrue(
            policy[
                "newer_head_arriving_during_build_must_be_queued"
            ]
        )
        self.assertTrue(
            policy[
                "latest_head_must_eventually_be_evaluated"
            ]
        )

    def test_frozen_pilot_is_insufficient_for_continuous_mode(
        self,
    ) -> None:
        prerequisite = self.contract[
            "current_head_projection_prerequisite"
        ]
        self.assertTrue(
            prerequisite[
                "frozen_pilot_inventory_is_insufficient_for_continuous_mode"
            ]
        )
        self.assertTrue(
            prerequisite[
                "continuous_mode_requires_dynamic_inventory_for_each_exact_head"
            ]
        )

    def test_dynamic_inventory_scope_includes_core_zones(
        self,
    ) -> None:
        scope = set(
            self.contract[
                "current_head_projection_prerequisite"
            ]["inventory_scope_candidate"]
        )
        for expected in (
            "GOVERNANCE",
            "docs",
            "evidence",
            "reports",
            "src",
            "tests",
            "tools",
            "breakers",
            ".github/workflows",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, scope)

    def test_secrets_must_never_be_projected(self) -> None:
        prerequisite = self.contract[
            "current_head_projection_prerequisite"
        ]
        self.assertTrue(
            prerequisite[
                "secrets_and_credentials_must_never_be_projected"
            ]
        )

    def test_double_build_is_mandatory(self) -> None:
        pipeline = self.contract[
            "qualification_pipeline"
        ]["ordered_gates"]
        self.assertIn(
            "BUILD_DETERMINISTIC_PROJECTION_A",
            pipeline,
        )
        self.assertIn(
            "BUILD_DETERMINISTIC_PROJECTION_B",
            pipeline,
        )
        self.assertIn(
            "REQUIRE_A_EQUALS_B",
            pipeline,
        )

    def test_failure_keeps_last_known_good(self) -> None:
        pipeline = self.contract[
            "qualification_pipeline"
        ]
        self.assertEqual(
            pipeline["any_gate_failure_result"],
            "NO_PROMOTION_KEEP_LAST_KNOWN_GOOD",
        )
        self.assertTrue(
            self.contract["last_known_good"][
                "required"
            ]
        )

    def test_partial_success_cannot_promote(self) -> None:
        self.assertTrue(
            self.contract[
                "qualification_pipeline"
            ][
                "partial_success_may_not_be_promoted"
            ]
        )

    def test_generation_identity_binds_exact_head(self) -> None:
        identity = self.contract[
            "generation_identity"
        ]
        self.assertIn(
            "source_head",
            identity["required_fields"],
        )
        self.assertIn(
            "projection_tree_digest",
            identity["required_fields"],
        )
        self.assertTrue(
            identity[
                "source_head_must_match_built_checkout_head"
            ]
        )

    def test_projection_state_vocabulary_is_exact(
        self,
    ) -> None:
        states = self.contract[
            "projection_states"
        ]
        self.assertEqual(
            states["allowed"],
            [
                "CURRENT",
                "STALE",
                "BLOCKED",
                "ORPHAN",
                "MISSING",
            ],
        )
        self.assertTrue(
            states[
                "unknown_must_not_be_mapped_to_current"
            ]
        )

    def test_current_requires_head_equality(self) -> None:
        definition = self.contract[
            "projection_states"
        ]["current_definition"]
        self.assertIn(
            "LIVE_PROJECTION_SOURCE_HEAD_EQUALS",
            definition,
        )

    def test_failed_candidate_cannot_mutate_live_projection(
        self,
    ) -> None:
        lkg = self.contract["last_known_good"]
        self.assertTrue(
            lkg[
                "failed_candidate_must_not_modify_live_projection"
            ]
        )
        self.assertTrue(
            lkg[
                "live_projection_must_remain_usable_on_failure"
            ]
        )

    def test_mixed_generation_visibility_forbidden(
        self,
    ) -> None:
        atomicity = self.contract[
            "promotion_atomicity"
        ]
        self.assertTrue(
            atomicity[
                "mixed_generation_visibility_forbidden"
            ]
        )
        self.assertTrue(
            atomicity[
                "direct_in_place_multi_file_overwrite_forbidden"
            ]
        )
        self.assertTrue(
            atomicity["staging_required"]
        )

    def test_atomic_primitive_is_not_assumed_qualified(
        self,
    ) -> None:
        atomicity = self.contract[
            "promotion_atomicity"
        ]
        self.assertTrue(
            atomicity[
                "exact_windows_onedrive_mechanism_not_yet_qualified"
            ]
        )
        self.assertTrue(
            atomicity[
                "empirical_promotion_primitive_qualification_required"
            ]
        )
        self.assertTrue(
            atomicity[
                "obsidian_open_during_promotion_not_yet_authorized"
            ]
        )

    def test_human_views_are_not_auto_overwritten(
        self,
    ) -> None:
        policy = self.contract["vault_policy"]
        self.assertEqual(
            policy["views_owner"],
            "HUMAN",
        )
        self.assertFalse(
            policy[
                "observer_may_overwrite_human_views"
            ]
        )

    def test_observer_cannot_modify_obsidian_config(
        self,
    ) -> None:
        policy = self.contract["vault_policy"]
        self.assertFalse(
            policy[
                "observer_may_modify_obsidian_config"
            ]
        )
        self.assertFalse(
            policy[
                "observer_may_enable_obsidian_sync"
            ]
        )
        self.assertFalse(
            policy[
                "observer_may_install_plugins"
            ]
        )

    def test_machine_live_visual_namespace_is_separate(
        self,
    ) -> None:
        policy = self.contract[
            "machine_visual_layer_future_policy"
        ]
        self.assertTrue(
            policy[
                "future_machine_managed_visual_namespace_required"
            ]
        )
        self.assertEqual(
            policy["candidate_namespace"],
            "generated/live",
        )
        self.assertTrue(
            policy[
                "current_human_views_must_not_be_silently_overwritten"
            ]
        )

    def test_runtime_state_is_outside_vault(self) -> None:
        storage = self.contract[
            "runtime_state_storage"
        ]
        self.assertEqual(
            storage[
                "volatile_daemon_state_location"
            ],
            "LOCALAPPDATA_OUTSIDE_VAULT",
        )
        self.assertTrue(
            storage[
                "append_only_event_log_required"
            ]
        )
        self.assertFalse(
            storage[
                "event_log_is_not_semantic_authority"
            ]
            is False
        )

    def test_single_writer_lock_is_required(self) -> None:
        concurrency = self.contract[
            "concurrency"
        ]
        self.assertTrue(
            concurrency[
                "single_promotion_writer_required"
            ]
        )
        self.assertEqual(
            concurrency[
                "second_instance_result"
            ],
            "NO_WRITE_BLOCKED_BY_LOCK",
        )

    def test_recovery_never_deletes_last_known_good(
        self,
    ) -> None:
        recovery = self.contract["recovery"]
        self.assertTrue(
            recovery[
                "no_recursive_delete_of_last_known_good"
            ]
        )

    def test_health_report_is_required(self) -> None:
        observability = self.contract[
            "observability"
        ]
        self.assertTrue(
            observability[
                "health_report_required"
            ]
        )
        for field in (
            "observer_running",
            "latest_remote_head",
            "live_projection_head",
            "projection_state",
            "last_failure_code",
            "queued_head_count",
        ):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    observability["fields"],
                )

    def test_p5a_itself_authorizes_no_runtime(self) -> None:
        boundary = self.contract[
            "p5a_boundary"
        ]
        for field in (
            "background_observer_execution_authorized",
            "remote_polling_loop_authorized",
            "vault_continuous_write_authorized",
            "generated_replacement_authorized",
            "human_views_overwrite_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_creation_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_breaker_registry_is_broad_and_unique(
        self,
    ) -> None:
        breakers = self.contract[
            "required_breakers"
        ]
        self.assertGreaterEqual(
            len(breakers),
            30,
        )
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gates_are_ordered(self) -> None:
        gates = self.contract[
            "next_gates"
        ]
        self.assertEqual(
            list(gates.keys()),
            ["p5b", "p5c", "p5d", "p5e"],
        )
        self.assertEqual(
            gates["p5b"],
            "DYNAMIC_CURRENT_HEAD_INVENTORY_AND_SOURCE_SELECTION_CONTRACT",
        )
        self.assertEqual(
            gates["p5c"],
            "WINDOWS_ONEDRIVE_ATOMIC_PROMOTION_PRIMITIVE_QUALIFICATION",
        )
        self.assertEqual(
            gates["p5d"],
            "CONTINUOUS_OBSERVER_IMPLEMENTATION_CANDIDATE",
        )
        self.assertEqual(
            gates["p5e"],
            "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
        )


if __name__ == "__main__":
    unittest.main()
