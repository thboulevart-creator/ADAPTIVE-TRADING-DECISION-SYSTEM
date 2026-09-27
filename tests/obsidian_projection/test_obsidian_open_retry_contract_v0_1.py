from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5C3RContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.contract = json.loads(
            (
                cls.root
                / "tools"
                / "obsidian_projection"
                / "obsidian_open_retry_contract_v0_1.json"
            ).read_text(encoding="utf-8")
        )

    def test_schema_and_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_OPEN_RETRY_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_failed_p5c3_predecessor_is_pinned(self) -> None:
        self.assertEqual(
            self.contract[
                "failed_predecessor_p5c3_head"
            ],
            "65003f36eef5bb8b4759d62735d7bf9f08e90ddb",
        )

    def test_observed_failure_is_exact(self) -> None:
        failure = self.contract[
            "observed_failure"
        ]
        self.assertEqual(
            failure["phase"],
            "PROMOTION_LOOP",
        )
        self.assertEqual(
            failure[
                "cycle_completed_count"
            ],
            8,
        )
        self.assertEqual(
            failure["winerror"],
            5,
        )
        self.assertEqual(
            failure["current_after_failure"],
            "GEN_A",
        )

    def test_write_retry_is_narrow_and_bounded(
        self,
    ) -> None:
        policy = self.contract[
            "retry_policy"
        ]
        self.assertEqual(
            policy[
                "retryable_exception_type"
            ],
            "PermissionError",
        )
        self.assertEqual(
            policy["retryable_winerror_only"],
            5,
        )
        self.assertEqual(
            policy[
                "retryable_operation_only"
            ],
            "os.replace(CURRENT.tmp, CURRENT.md)",
        )
        self.assertEqual(
            policy["deadline_ms"],
            5000,
        )
        self.assertEqual(
            policy["initial_backoff_ms"],
            10,
        )
        self.assertEqual(
            policy["max_backoff_ms"],
            500,
        )
        self.assertTrue(
            policy["infinite_retry_forbidden"]
        )
        self.assertFalse(
            policy[
                "rewrite_temp_between_replace_attempts"
            ]
        )

    def test_temp_integrity_is_required_between_attempts(
        self,
    ) -> None:
        policy = self.contract[
            "retry_policy"
        ]
        self.assertTrue(
            policy[
                "temp_integrity_sha256_check_after_each_retryable_failure"
            ]
        )
        self.assertTrue(
            policy[
                "current_must_remain_valid_old_generation_while_waiting"
            ]
        )
        self.assertTrue(
            policy[
                "successful_replace_must_match_exact_candidate_bytes"
            ]
        )

    def test_reader_access_retry_is_separate_and_bounded(
        self,
    ) -> None:
        policy = self.contract[
            "reader_access_retry_policy"
        ]
        self.assertTrue(
            policy[
                "retryable_only_when_underlying_cause_is_PermissionError_winerror_5"
            ]
        )
        self.assertEqual(
            policy["deadline_ms"],
            500,
        )
        self.assertEqual(
            policy["initial_backoff_ms"],
            5,
        )
        self.assertEqual(
            policy["max_backoff_ms"],
            50,
        )
        self.assertTrue(
            policy[
                "transient_access_denied_not_classified_as_partial_generation"
            ]
        )
        self.assertEqual(
            policy[
                "terminal_reader_access_error_count_must_equal"
            ],
            0,
        )
        self.assertEqual(
            policy[
                "semantic_partial_generation_count_must_equal"
            ],
            0,
        )

    def test_synthetic_lock_breaker_is_required(
        self,
    ) -> None:
        breaker = self.contract[
            "synthetic_windows_lock_breaker"
        ]
        self.assertTrue(
            breaker["required"]
        )
        self.assertTrue(
            breaker[
                "destination_current_opened_without_FILE_SHARE_DELETE"
            ]
        )
        self.assertGreaterEqual(
            breaker[
                "lock_release_delay_ms_minimum"
            ],
            150,
        )
        self.assertTrue(
            breaker[
                "retry_conflict_count_must_be_greater_than_zero"
            ]
        )
        self.assertTrue(
            breaker[
                "final_replace_must_succeed"
            ]
        )

    def test_recovery_is_narrow(self) -> None:
        recovery = self.contract["recovery"]
        self.assertTrue(
            recovery["obsidian_must_be_closed"]
        )
        self.assertTrue(
            recovery["reuse_existing_sandbox"]
        )
        self.assertTrue(
            recovery[
                "rebuild_generations_forbidden"
            ]
        )
        self.assertEqual(
            recovery["current_must_be"],
            "GEN_A",
        )

        stale = recovery[
            "stale_temp_handling"
        ]
        self.assertEqual(
            stale[
                "if_present_expected_generation"
            ],
            "GEN_B",
        )
        self.assertTrue(
            stale[
                "exact_expected_bytes_required"
            ]
        )
        self.assertTrue(
            stale[
                "deletion_authorized_only_after_exact_match"
            ]
        )

    def test_open_experiment_preserves_scale(
        self,
    ) -> None:
        experiment = self.contract[
            "open_experiment"
        ]
        self.assertEqual(
            experiment["promotion_cycles"],
            250,
        )
        self.assertEqual(
            experiment[
                "reader_samples_minimum"
            ],
            5000,
        )
        self.assertEqual(
            experiment[
                "initial_generation"
            ],
            "GEN_A",
        )
        self.assertEqual(
            experiment["final_generation"],
            "GEN_A",
        )

    def test_terminal_errors_and_semantic_anomalies_are_zero(
        self,
    ) -> None:
        experiment = self.contract[
            "open_experiment"
        ]
        for field in (
            "terminal_pointer_write_error_count_must_equal",
            "retry_deadline_exceeded_count_must_equal",
            "mixed_generation_count_must_equal",
            "missing_entrypoint_count_must_equal",
            "partial_generation_count_must_equal",
            "parse_error_count_must_equal",
            "reader_terminal_access_error_count_must_equal",
        ):
            with self.subTest(field=field):
                self.assertEqual(
                    experiment[field],
                    0,
                )

    def test_transient_access_denied_may_be_nonzero(
        self,
    ) -> None:
        experiment = self.contract[
            "open_experiment"
        ]
        self.assertTrue(
            experiment[
                "access_denied_retry_conflict_count_may_be_nonzero"
            ]
        )
        self.assertTrue(
            experiment[
                "reader_access_denied_retry_count_may_be_nonzero"
            ]
        )

    def test_pass_still_does_not_authorize_production(
        self,
    ) -> None:
        qualification = self.contract[
            "qualification"
        ]
        self.assertFalse(
            qualification[
                "production_promotion_authorized_on_pass"
            ]
        )
        self.assertFalse(
            qualification[
                "continuous_observer_authorized_on_pass"
            ]
        )
        self.assertTrue(
            qualification[
                "manual_visual_acceptance_required"
            ]
        )
        self.assertTrue(
            qualification[
                "post_close_pass_required"
            ]
        )

    def test_graph_problem_remains_open(self) -> None:
        graph = self.contract[
            "graph_indexing_boundary"
        ]
        self.assertFalse(
            graph[
                "native_graph_current_pointer_semantics_qualified"
            ]
        )
        self.assertEqual(
            graph["deferred_to"],
            "P6_CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
        )

    def test_breakers_are_unique_and_broad(self) -> None:
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


if __name__ == "__main__":
    unittest.main()
