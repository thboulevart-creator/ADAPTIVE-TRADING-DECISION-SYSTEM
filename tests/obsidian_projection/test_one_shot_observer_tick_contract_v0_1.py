from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D2OneShotObserverTickContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "one_shot_observer_tick_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_ONE_SHOT_OBSERVER_TICK_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_p5d1_predecessor_is_pinned(self) -> None:
        predecessor = self.contract[
            "qualified_predecessor"
        ]
        self.assertEqual(
            predecessor["p5d1_contract_blob"],
            "a20999ae991e07447e25ecd1592964f2d333449b",
        )
        self.assertEqual(
            predecessor["p5d1_qualification_report_blob"],
            "fbe4a60f2349a96bf7a1f4c5dea0eb28328af841",
        )
        self.assertEqual(
            predecessor["p5d1_qualification_commit"],
            "dce36303982d73a37d8498400f0a13e708e841b6",
        )

    def test_tick_is_exactly_one_transition(self) -> None:
        objective = self.contract["objective"]
        self.assertTrue(
            objective["exactly_one_transition_per_invocation"]
        )
        for field in (
            "repeated_tick_loop_forbidden",
            "sleep_forbidden",
            "background_execution_forbidden",
            "network_io_forbidden",
            "filesystem_io_forbidden",
            "process_launch_forbidden",
            "environment_read_forbidden",
            "wall_clock_read_forbidden",
            "randomness_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(objective[field])

    def test_schemas_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schemas"],
            {
                "state": "ATDS_OBSIDIAN_OBSERVER_STATE_V0_1",
                "input": "ATDS_OBSIDIAN_OBSERVER_INPUT_V0_1",
                "decision": "ATDS_OBSIDIAN_OBSERVER_DECISION_V0_1",
                "audit": "ATDS_OBSIDIAN_OBSERVER_EVENT_V0_1",
                "tick_result": (
                    "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1"
                ),
            },
        )

    def test_canonicalization_is_pinned(self) -> None:
        canonical = self.contract["canonicalization"]
        self.assertEqual(canonical["encoding"], "UTF-8")
        self.assertEqual(canonical["json"], "SORT_KEYS_COMPACT")
        self.assertEqual(
            canonical["line_termination"],
            "LF",
        )
        self.assertTrue(
            canonical["terminal_lf_required"]
        )
        self.assertEqual(
            canonical["digest_algorithm"],
            "SHA256",
        )

    def test_current_requires_three_way_identity(self) -> None:
        required = set(
            self.contract["state_validation"][
                "current_requires"
            ]
        )
        self.assertIn(
            "remote_freshness == KNOWN",
            required,
        )
        self.assertIn(
            "latest_observed_head == live_projection_head",
            required,
        )
        self.assertIn(
            "live_projection_head == last_qualified_head",
            required,
        )

    def test_input_sequence_is_strictly_next(self) -> None:
        self.assertEqual(
            self.contract["normalized_input"][
                "sequence_rule"
            ],
            (
                "input.sequence == "
                "previous_state.last_event_sequence + 1"
            ),
        )
        self.assertTrue(
            self.contract["normalized_input"][
                "extra_fields_forbidden"
            ]
        )

    def test_bootstrap_requires_canonical_initial_state(
        self,
    ) -> None:
        bootstrap = self.contract[
            "transition_semantics"
        ]["BOOTSTRAP"]
        self.assertTrue(
            bootstrap["requires_canonical_initial_state"]
        )
        self.assertTrue(
            bootstrap["state_unchanged_except_sequence"]
        )

    def test_blocked_phase_is_sticky(self) -> None:
        blocked = self.contract[
            "transition_semantics"
        ]["REMOTE_HEAD_OBSERVED_WHILE_BLOCKED"]
        self.assertEqual(
            blocked["action"],
            "BLOCK_REQUIRES_ADJUDICATION",
        )
        self.assertTrue(blocked["queue_unchanged"])
        self.assertTrue(
            blocked["blocked_head_unchanged"]
        )
        self.assertTrue(
            blocked["blocking_failure_code_unchanged"]
        )
        self.assertEqual(
            blocked["observer_phase"],
            "BLOCKED",
        )
        self.assertEqual(
            blocked["projection_state"],
            "BLOCKED",
        )

    def test_state_phase_invariants_are_explicit(self) -> None:
        validation = self.contract["state_validation"]
        self.assertTrue(
            validation[
                "candidate_pending_requires_last_qualified_head"
            ]
        )
        self.assertTrue(
            validation[
                "blocked_phase_requires_projection_blocked"
            ]
        )
        self.assertTrue(
            validation[
                "blocked_phase_requires_blocked_head"
            ]
        )
        self.assertTrue(
            validation[
                "blocked_phase_requires_failure_code"
            ]
        )

    def test_same_head_is_noop(self) -> None:
        same = self.contract[
            "transition_semantics"
        ]["REMOTE_HEAD_OBSERVED_SAME"]
        self.assertEqual(same["action"], "NOOP")
        self.assertTrue(same["queue_unchanged"])
        self.assertTrue(same["evaluation_not_started"])
        self.assertTrue(
            same["blocked_state_may_not_be_auto_cleared"]
        )

    def test_eligible_heads_are_queued_only(self) -> None:
        semantics = self.contract[
            "transition_semantics"
        ]
        for key in (
            "REMOTE_HEAD_OBSERVED_INITIAL",
            "REMOTE_HEAD_OBSERVED_FAST_FORWARD",
        ):
            with self.subTest(key=key):
                self.assertEqual(
                    semantics[key]["action"],
                    "QUEUE_EXACT_HEAD_FOR_EVALUATION",
                )
                self.assertTrue(
                    semantics[key]["queue_append_if_absent"]
                )

    def test_non_ff_and_unknown_block(self) -> None:
        semantics = self.contract[
            "transition_semantics"
        ]
        for key in (
            "REMOTE_HEAD_OBSERVED_NON_FAST_FORWARD",
            "REMOTE_HEAD_OBSERVED_UNKNOWN",
        ):
            with self.subTest(key=key):
                self.assertEqual(
                    semantics[key]["action"],
                    "BLOCK_REQUIRES_ADJUDICATION",
                )
                self.assertTrue(
                    semantics[key]["queue_append_forbidden"]
                )
                self.assertTrue(
                    semantics[key][
                        "live_projection_head_unchanged"
                    ]
                )

    def test_network_failure_preserves_live_head(self) -> None:
        failure = self.contract[
            "transition_semantics"
        ]["REMOTE_OBSERVATION_FAILED"]
        self.assertEqual(
            failure["remote_freshness"],
            "UNKNOWN",
        )
        self.assertTrue(
            failure["live_projection_head_unchanged"]
        )
        self.assertTrue(
            failure["previous_current_becomes_stale"]
        )

    def test_evaluation_start_is_exact_queue_head(
        self,
    ) -> None:
        started = self.contract[
            "transition_semantics"
        ]["EVALUATION_STARTED"]
        self.assertEqual(
            started["requires_observer_phase"],
            "IDLE",
        )
        self.assertTrue(
            started[
                "candidate_must_equal_pending_queue_head"
            ]
        )
        self.assertTrue(
            started["live_projection_head_unchanged"]
        )

    def test_evaluation_pass_separates_qualification(
        self,
    ) -> None:
        passed = self.contract[
            "transition_semantics"
        ]["EVALUATION_PASSED"]
        self.assertTrue(
            passed[
                "last_qualified_head_becomes_candidate"
            ]
        )
        self.assertTrue(
            passed["live_projection_head_unchanged"]
        )
        self.assertEqual(
            passed["observer_phase"],
            "CANDIDATE_PENDING",
        )

    def test_promotion_is_external_confirmation_only(
        self,
    ) -> None:
        rules = self.contract[
            "normalized_input"
        ]["event_specific_rules"]
        self.assertTrue(
            rules["PROMOTION_CONFIRMED"][
                "external_confirmation_only"
            ]
        )
        self.assertTrue(
            rules["PROMOTION_FAILED"][
                "external_confirmation_only"
            ]
        )
        semantics = self.contract[
            "transition_semantics"
        ]
        self.assertTrue(
            semantics["PROMOTION_CONFIRMED"][
                "actual_promotion_io_forbidden"
            ]
        )
        self.assertTrue(
            semantics["PROMOTION_FAILED"][
                "actual_promotion_io_forbidden"
            ]
        )

    def test_stopped_is_terminal(self) -> None:
        self.assertTrue(
            self.contract["transition_semantics"][
                "STOPPED_TERMINAL"
            ]["further_events_forbidden"]
        )

    def test_decision_authority_is_always_false(
        self,
    ) -> None:
        decision = self.contract[
            "decision_invariants"
        ]
        self.assertTrue(
            decision[
                "automatic_promotion_authorized_always_false"
            ]
        )
        self.assertTrue(
            decision[
                "production_write_authorized_always_false"
            ]
        )

    def test_audit_has_no_volatile_fields(self) -> None:
        audit = self.contract["audit_invariants"]
        self.assertTrue(audit["volatile_fields_forbidden"])
        for field in (
            "previous_state_digest",
            "input_digest",
            "decision_digest",
            "next_state_digest",
        ):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    audit["required_fields"],
                )

    def test_failure_model_is_fail_closed(self) -> None:
        failure = self.contract["failure_model"]
        self.assertEqual(
            failure["invalid_state"],
            "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
        )
        self.assertEqual(
            failure["invalid_input"],
            "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
        )
        self.assertEqual(
            failure["invalid_transition"],
            "RAISE_OBSERVER_TICK_ERROR_NO_OUTPUT",
        )
        self.assertTrue(
            failure["partial_result_forbidden"]
        )

    def test_p5d2_authorizes_only_pure_tick(self) -> None:
        boundary = self.contract["p5d2_boundary"]
        self.assertTrue(
            boundary[
                "pure_one_shot_transition_implementation_authorized"
            ]
        )
        for field in (
            "network_adapter_authorized",
            "git_adapter_authorized",
            "filesystem_state_store_authorized",
            "append_only_disk_event_log_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "sleep_or_timer_authorized",
            "production_promotion_authorized",
            "continuous_vault_write_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_breaker_registry_is_broad_unique(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 55)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gates_remain_ordered(self) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            list(gates.keys()),
            ["p5d3", "p5d4", "p5e", "p6"],
        )


if __name__ == "__main__":
    unittest.main()
