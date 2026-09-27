from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5C3R2ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.contract = json.loads(
            (
                cls.root
                / "tools"
                / "obsidian_projection"
                / "obsidian_open_retry_contract_v0_2.json"
            ).read_text(encoding="utf-8")
        )

    def test_schema_and_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_OPEN_RETRY_CONTRACT_V0_2",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_forensic_failure_is_pinned(self) -> None:
        failure = self.contract["observed_reader_failure"]
        self.assertEqual(
            failure["forensic_run_status"],
            "FAIL",
        )
        self.assertEqual(
            failure["semantic_partial_generation_count"],
            12,
        )
        self.assertEqual(
            failure["semantic_partial_signature_total_count"],
            12,
        )
        self.assertEqual(
            failure["signature_count"],
            12,
        )
        self.assertEqual(
            failure["signature"],
            (
                "message=CURRENT.md unreadable"
                "|cause_type=PermissionError"
                "|errno=13"
                "|winerror=None"
            ),
        )

    def test_write_retry_policy_is_unchanged(self) -> None:
        policy = self.contract["write_retry_policy"]
        self.assertEqual(
            policy["retryable_winerrors_only"],
            [5, 32],
        )
        self.assertTrue(
            policy[
                "errno_eacces_without_winerror_retry_forbidden"
            ]
        )
        self.assertEqual(
            policy["deadline_ms"],
            5000,
        )
        self.assertEqual(
            policy["max_backoff_ms"],
            500,
        )

    def test_reader_eacces_fallback_is_narrow(self) -> None:
        policy = self.contract[
            "reader_access_retry_policy"
        ]
        self.assertEqual(
            policy["retryable_if_winerror_in"],
            [5, 32],
        )
        self.assertEqual(
            policy[
                "retryable_if_winerror_is_none_and_errno_equals"
            ],
            13,
        )
        self.assertEqual(
            policy["errno_symbol"],
            "EACCES",
        )
        self.assertEqual(
            policy["retryable_errno_fallback_scope"],
            "reader_only",
        )
        self.assertTrue(
            policy[
                "non_permission_error_errno_13_retry_forbidden"
            ]
        )
        self.assertTrue(
            policy[
                "permission_error_errno_13_with_nonnull_nonretryable_winerror_retry_forbidden"
            ]
        )

    def test_reader_bounds_and_failure_criteria_unchanged(
        self,
    ) -> None:
        reader = self.contract[
            "reader_access_retry_policy"
        ]
        self.assertEqual(reader["deadline_ms"], 500)
        self.assertEqual(reader["initial_backoff_ms"], 5)
        self.assertEqual(reader["max_backoff_ms"], 50)
        self.assertEqual(
            reader[
                "terminal_reader_access_error_count_must_equal"
            ],
            0,
        )
        self.assertEqual(
            reader[
                "semantic_partial_generation_count_must_equal"
            ],
            0,
        )

    def test_open_scale_and_zero_anomalies_unchanged(
        self,
    ) -> None:
        experiment = self.contract["open_experiment"]
        self.assertEqual(
            experiment["promotion_cycles"],
            250,
        )
        self.assertEqual(
            experiment["reader_samples_minimum"],
            5000,
        )
        self.assertEqual(
            experiment["initial_generation"],
            "GEN_A",
        )
        self.assertEqual(
            experiment["final_generation"],
            "GEN_A",
        )
        for field in (
            "terminal_pointer_write_error_count_must_equal",
            "retry_deadline_exceeded_count_must_equal",
            "mixed_generation_count_must_equal",
            "missing_entrypoint_count_must_equal",
            "semantic_partial_generation_count_must_equal",
            "parse_error_count_must_equal",
            "reader_terminal_access_error_count_must_equal",
        ):
            with self.subTest(field=field):
                self.assertEqual(
                    experiment[field],
                    0,
                )

    def test_eacces_retry_telemetry_is_required(self) -> None:
        telemetry = self.contract["telemetry"]
        self.assertTrue(
            telemetry[
                "reader_eacces_without_winerror_retry_count_required"
            ]
        )
        reader = self.contract[
            "reader_access_retry_policy"
        ]
        self.assertTrue(
            reader[
                "eacces_without_winerror_retry_count_must_be_telemetried"
            ]
        )

    def test_pass_still_does_not_authorize_production(
        self,
    ) -> None:
        qualification = self.contract["qualification"]
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


if __name__ == "__main__":
    unittest.main()
