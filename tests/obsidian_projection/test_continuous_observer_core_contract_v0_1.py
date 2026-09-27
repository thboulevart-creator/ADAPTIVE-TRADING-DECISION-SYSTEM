from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D1ContinuousObserverCoreContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "continuous_observer_core_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_CONTINUOUS_OBSERVER_CORE_CONTRACT_V0_1",
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
        monitored = self.contract["monitored_source"]
        self.assertEqual(monitored["remote"], "origin")
        self.assertEqual(
            monitored["branch"],
            "integration/system-v1",
        )
        self.assertTrue(
            monitored[
                "local_working_tree_is_not_authority"
            ]
        )

    def test_qualified_predecessors_are_pinned(
        self,
    ) -> None:
        predecessors = self.contract[
            "qualified_predecessors"
        ]
        self.assertEqual(
            predecessors[
                "p5a_continuous_projection_contract_blob"
            ],
            "96ec1a768b8e9ff77d94bbcd36ee513678c258e6",
        )
        self.assertEqual(
            predecessors[
                "p5b2_dynamic_inventory_qualification_report_blob"
            ],
            "286a81a4f3f71a1d857631c2388d7894908acb5f",
        )
        self.assertEqual(
            predecessors[
                "p5c2_promotion_qualification_report_blob"
            ],
            "a928598182b25d110c9040c62d846bf9018ac3ed",
        )
        self.assertEqual(
            predecessors[
                "p5c3r2_final_qualification_report_blob"
            ],
            "fd54a78abde8342c6da708d3a4096b4d0b267905",
        )
        self.assertEqual(
            predecessors[
                "p5c3r2_qualified_runtime_candidate"
            ],
            "b5f3a8de061772e15bc94b20095d419130c20781",
        )

    def test_p5d1_is_contract_only(self) -> None:
        objective = self.contract["objective"]
        self.assertTrue(objective["one_shot_first"])
        self.assertTrue(
            objective["background_loop_deferred"]
        )
        self.assertTrue(
            objective["time_based_behavior_deferred"]
        )
        self.assertTrue(
            objective["production_runtime_deferred"]
        )

    def test_transition_core_is_pure_and_deterministic(
        self,
    ) -> None:
        core = self.contract["deterministic_core"]
        self.assertTrue(core["pure_transition_required"])
        self.assertTrue(
            core[
                "same_inputs_must_produce_byte_identical_normalized_outputs"
            ]
        )
        for field in (
            "network_io_inside_transition_forbidden",
            "filesystem_io_inside_transition_forbidden",
            "process_launch_inside_transition_forbidden",
            "wall_clock_read_inside_transition_forbidden",
            "randomness_inside_transition_forbidden",
            "environment_variable_read_inside_transition_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(core[field])

    def test_state_axes_are_separate(self) -> None:
        state = self.contract["state_schema"]
        self.assertEqual(
            state["projection_state_allowed"],
            [
                "CURRENT",
                "STALE",
                "BLOCKED",
                "ORPHAN",
                "MISSING",
            ],
        )
        self.assertEqual(
            state["remote_freshness_allowed"],
            ["KNOWN", "UNKNOWN"],
        )
        self.assertIn(
            "observer_phase",
            state["required_fields"],
        )
        self.assertIn(
            "remote_freshness",
            state["required_fields"],
        )
        self.assertIn(
            "projection_state",
            state["required_fields"],
        )

    def test_volatile_host_data_is_excluded_from_state(
        self,
    ) -> None:
        state = self.contract["state_schema"]
        self.assertTrue(
            state[
                "timestamps_forbidden_in_deterministic_state"
            ]
        )
        self.assertTrue(
            state["pid_forbidden_in_deterministic_state"]
        )
        self.assertTrue(
            state[
                "host_paths_forbidden_in_deterministic_state"
            ]
        )

    def test_transition_classes_are_exact(self) -> None:
        inputs = self.contract["input_schema"]
        self.assertEqual(
            inputs["remote_head_transition_classes"],
            [
                "INITIAL",
                "SAME",
                "FAST_FORWARD",
                "NON_FAST_FORWARD",
                "UNKNOWN",
            ],
        )
        self.assertTrue(
            inputs[
                "implicit_history_rewrite_acceptance_forbidden"
            ]
        )

    def test_same_head_is_strict_noop(self) -> None:
        rule = self.contract[
            "transition_rules"
        ]["same_head"]
        self.assertTrue(rule["queue_growth_forbidden"])
        self.assertTrue(
            rule["evaluation_start_forbidden"]
        )
        self.assertEqual(rule["action"], "NOOP")

    def test_network_failure_keeps_last_known_good(
        self,
    ) -> None:
        rule = self.contract[
            "transition_rules"
        ]["remote_observation_failed"]
        self.assertEqual(
            rule["remote_freshness"],
            "UNKNOWN",
        )
        self.assertTrue(
            rule["live_projection_head_must_not_change"]
        )
        self.assertTrue(
            rule["new_current_claim_forbidden"]
        )
        self.assertEqual(
            rule["action"],
            "RETAIN_LAST_KNOWN_GOOD",
        )

    def test_current_claim_requires_three_way_equality(
        self,
    ) -> None:
        freshness = self.contract[
            "freshness_semantics"
        ]
        self.assertTrue(
            freshness[
                "current_requires_remote_freshness_known"
            ]
        )
        self.assertTrue(
            freshness[
                "current_requires_latest_observed_head_equals_live_projection_head"
            ]
        )
        self.assertTrue(
            freshness[
                "current_requires_live_projection_head_equals_last_qualified_head"
            ]
        )

    def test_initial_and_fast_forward_can_queue(
        self,
    ) -> None:
        rules = self.contract["transition_rules"]
        self.assertTrue(
            rules["initial_head"][
                "automatic_evaluation_queue_allowed"
            ]
        )
        self.assertTrue(
            rules["fast_forward_head"][
                "automatic_evaluation_queue_allowed"
            ]
        )
        self.assertEqual(
            rules["initial_head"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )
        self.assertEqual(
            rules["fast_forward_head"]["action"],
            "QUEUE_EXACT_HEAD_FOR_EVALUATION",
        )

    def test_non_fast_forward_and_unknown_block(
        self,
    ) -> None:
        rules = self.contract["transition_rules"]
        for key in (
            "non_fast_forward_head",
            "unknown_ancestry_head",
        ):
            with self.subTest(key=key):
                rule = rules[key]
                self.assertFalse(
                    rule[
                        "automatic_evaluation_queue_allowed"
                    ]
                )
                self.assertTrue(
                    rule[
                        "automatic_promotion_forbidden"
                    ]
                )
                self.assertEqual(
                    rule["observer_phase"],
                    "BLOCKED",
                )
                self.assertEqual(
                    rule["action"],
                    "BLOCK_REQUIRES_ADJUDICATION",
                )

    def test_evaluation_never_changes_live_head(
        self,
    ) -> None:
        rules = self.contract["transition_rules"]
        for key in (
            "evaluation_started",
            "evaluation_passed",
            "evaluation_failed",
        ):
            with self.subTest(key=key):
                self.assertTrue(
                    rules[key][
                        "live_projection_head_must_not_change"
                    ]
                )

    def test_promotion_is_modelled_but_not_authorized(
        self,
    ) -> None:
        rules = self.contract["transition_rules"]
        self.assertFalse(
            rules[
                "promotion_confirmed_model_semantics"
            ]["p5d1_execution_authorized"]
        )
        self.assertFalse(
            rules[
                "promotion_failed_model_semantics"
            ]["p5d1_execution_authorized"]
        )

    def test_queue_preserves_exact_head_identity(
        self,
    ) -> None:
        queue = self.contract[
            "queue_and_coalescing"
        ]
        self.assertEqual(
            queue["pending_head_identity_is_exact_sha"],
            True,
        )
        self.assertTrue(queue["duplicate_pending_head_forbidden"])
        self.assertTrue(queue["observation_order_preserved"])
        self.assertTrue(
            queue[
                "newer_head_may_not_retarget_active_evaluation"
            ]
        )
        self.assertTrue(
            queue[
                "superseded_head_may_be_removed_only_after_proven_fast_forward_containment"
            ]
        )

    def test_event_log_is_audit_not_authority(
        self,
    ) -> None:
        model = self.contract[
            "event_and_audit_model"
        ]
        self.assertTrue(model["append_only_event_required"])
        self.assertTrue(
            model["event_log_is_not_semantic_authority"]
        )
        self.assertTrue(
            model["event_sequence_must_be_strictly_monotonic"]
        )
        self.assertTrue(
            model[
                "volatile_envelope_fields_must_not_affect_deterministic_digests"
            ]
        )

    def test_single_writer_is_required(self) -> None:
        model = self.contract["single_writer_model"]
        self.assertTrue(model["required"])
        self.assertEqual(
            model["second_instance_result"],
            "NO_WRITE_BLOCKED_BY_LOCK",
        )
        self.assertTrue(
            model[
                "lock_acquisition_is_outside_pure_transition"
            ]
        )

    def test_last_known_good_cannot_be_destroyed(
        self,
    ) -> None:
        lkg = self.contract["last_known_good"]
        self.assertTrue(lkg["required"])
        for field in (
            "failed_observation_must_not_change_live_projection_head",
            "failed_evaluation_must_not_change_live_projection_head",
            "failed_promotion_must_not_change_live_projection_head",
            "recursive_delete_of_last_known_good_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(lkg[field])

    def test_qualified_components_must_be_reused(
        self,
    ) -> None:
        boundaries = self.contract[
            "qualified_component_boundaries"
        ]
        self.assertTrue(
            boundaries[
                "dynamic_inventory_contract_must_be_reused_not_reimplemented"
            ]
        )
        self.assertTrue(
            boundaries[
                "atomic_pointer_primitive_must_be_reused_not_reimplemented"
            ]
        )
        self.assertTrue(
            boundaries[
                "p5c3r2_reader_retry_policy_must_be_reused_not_weakened"
            ]
        )

    def test_p5d1_authorizes_no_runtime(self) -> None:
        boundary = self.contract["p5d1_boundary"]
        self.assertTrue(
            boundary["contract_and_breakers_only"]
        )
        for field in (
            "observer_core_implementation_authorized",
            "network_observation_execution_authorized",
            "remote_fetch_execution_authorized",
            "background_observer_execution_authorized",
            "polling_loop_execution_authorized",
            "production_promotion_authorized",
            "continuous_vault_write_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_creation_authorized",
            "windows_service_creation_authorized",
            "graph_search_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_breaker_registry_is_broad_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 45)
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
            ["p5d2", "p5d3", "p5d4", "p5e", "p6"],
        )
        self.assertEqual(
            gates["p5d2"],
            "ONE_SHOT_OBSERVER_TICK_IMPLEMENTATION",
        )
        self.assertEqual(
            gates["p5d3"],
            "CONTROLLED_CANDIDATE_EVALUATION_PIPELINE",
        )
        self.assertEqual(
            gates["p5d4"],
            "BOUNDED_OBSERVER_LOOP_CANDIDATE",
        )
        self.assertEqual(
            gates["p5e"],
            "END_TO_END_NEAR_REAL_TIME_QUALIFICATION",
        )
        self.assertEqual(
            gates["p6"],
            "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
        )


if __name__ == "__main__":
    unittest.main()
