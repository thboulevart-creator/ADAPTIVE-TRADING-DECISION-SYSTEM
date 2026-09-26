from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5COneDrivePromotionContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "onedrive_promotion_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_ONEDRIVE_PROMOTION_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_predecessor_is_exact_p5b2_closure(self) -> None:
        self.assertEqual(
            self.contract["predecessor_p5b2_head"],
            "eb7b3202c8c3c9ced8cb6d068051e0a922da5e22",
        )

    def test_live_vault_is_immutable_in_p5c_contract(
        self,
    ) -> None:
        live = self.contract["live_vault"]
        self.assertFalse(live["mutation_authorized"])
        self.assertFalse(
            live["generated_mutation_authorized"]
        )
        self.assertFalse(
            live["views_mutation_authorized"]
        )
        self.assertFalse(
            live["obsidian_config_mutation_authorized"]
        )

    def test_sandbox_is_same_onedrive_root_and_sacrificial(
        self,
    ) -> None:
        sandbox = self.contract["sandbox"]
        self.assertTrue(
            sandbox["same_onedrive_root_required"]
        )
        self.assertTrue(sandbox["sacrificial"])
        self.assertTrue(
            sandbox["must_not_be_git_repository"]
        )
        self.assertTrue(
            sandbox["must_not_overlap_live_vault"]
        )

    def test_primary_objective_is_zero_mixed_generation(
        self,
    ) -> None:
        objective = self.contract["objective"]
        self.assertEqual(
            objective["primary"],
            "ZERO_MIXED_GENERATION_VISIBILITY",
        )
        self.assertTrue(
            objective[
                "no_atomicity_claim_without_empirical_evidence"
            ]
        )

    def test_fixture_is_nontrivial(self) -> None:
        fixture = self.contract[
            "generation_fixture"
        ]
        self.assertEqual(
            fixture["generation_ids"],
            ["GEN_A", "GEN_B"],
        )
        self.assertGreaterEqual(
            fixture["files_per_generation"],
            128,
        )
        self.assertGreaterEqual(
            fixture["nested_directories"],
            8,
        )
        self.assertTrue(
            fixture[
                "each_file_must_embed_generation_id"
            ]
        )
        self.assertTrue(
            fixture["manifest_required"]
        )

    def test_reader_probe_is_concurrent_and_strict(
        self,
    ) -> None:
        probe = self.contract["reader_probe"]
        self.assertTrue(
            probe[
                "continuous_concurrent_reader_required"
            ]
        )
        self.assertLessEqual(
            probe["sample_interval_ms_max"],
            10,
        )
        self.assertGreaterEqual(
            probe["minimum_samples_per_candidate"],
            5000,
        )
        self.assertEqual(
            probe[
                "mixed_generation_count_must_equal"
            ],
            0,
        )
        self.assertEqual(
            probe[
                "missing_entrypoint_count_must_equal"
            ],
            0,
        )
        self.assertEqual(
            probe[
                "partial_generation_count_must_equal"
            ],
            0,
        )
        self.assertEqual(
            probe[
                "parse_error_count_must_equal"
            ],
            0,
        )

    def test_negative_control_is_not_qualifiable(
        self,
    ) -> None:
        candidates = {
            item["id"]: item
            for item in self.contract[
                "candidate_primitives"
            ]
        }
        negative = candidates[
            "DIRECT_IN_PLACE_PER_FILE_REPLACE"
        ]
        self.assertEqual(
            negative["expected_role"],
            "NEGATIVE_CONTROL",
        )
        self.assertFalse(
            negative["qualification_allowed"]
        )

    def test_three_real_candidates_are_present(
        self,
    ) -> None:
        candidates = {
            item["id"]
            for item in self.contract[
                "candidate_primitives"
            ]
            if item.get("qualification_allowed")
        }
        self.assertEqual(
            candidates,
            {
                "DIRECTORY_TWO_RENAME_SWAP",
                "WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE",
                "IMMUTABLE_GENERATION_ATOMIC_POINTER",
            },
        )

    def test_experiment_scale_is_bounded_and_bidirectional(
        self,
    ) -> None:
        scale = self.contract["experiment_scale"]
        self.assertGreaterEqual(
            scale[
                "minimum_promotion_cycles_per_qualifiable_candidate"
            ],
            250,
        )
        self.assertGreaterEqual(
            scale[
                "minimum_reader_samples_per_candidate"
            ],
            5000,
        )
        self.assertTrue(
            scale["both_directions_required"]
        )
        self.assertTrue(
            scale["gen_a_to_b_and_b_to_a"]
        )

    def test_qualification_requires_zero_reader_failures(
        self,
    ) -> None:
        required = set(
            self.contract[
                "qualification_rules"
            ]["primitive_pass_requires"]
        )
        self.assertEqual(
            required,
            {
                "ZERO_MIXED_GENERATION",
                "ZERO_MISSING_ENTRYPOINT",
                "ZERO_PARTIAL_GENERATION",
                "ZERO_PARSE_ERRORS",
                "ALL_CYCLES_COMPLETED",
                "POST_CYCLE_TREE_DIGEST_MATCH",
                "SANDBOX_ONLY_MUTATION",
            },
        )

    def test_one_cycle_and_static_review_are_insufficient(
        self,
    ) -> None:
        rules = self.contract[
            "qualification_rules"
        ]
        self.assertTrue(
            rules[
                "one_successful_cycle_is_insufficient"
            ]
        )
        self.assertTrue(
            rules[
                "static_code_review_is_insufficient"
            ]
        )
        self.assertTrue(
            rules[
                "undocumented_assumption_is_insufficient"
            ]
        )

    def test_environment_bounded_pass(self) -> None:
        rules = self.contract[
            "qualification_rules"
        ]
        self.assertTrue(
            rules["pass_is_environment_bounded"]
        )
        for field in (
            "windows_version",
            "filesystem_type",
            "onedrive_path",
            "reparse_state_summary",
            "python_version",
        ):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    rules[
                        "pass_environment_fields_required"
                    ],
                )

    def test_crash_recovery_is_required(self) -> None:
        crash = self.contract[
            "crash_recovery_probe"
        ]
        self.assertTrue(
            crash["required_for_selected_candidate"]
        )
        self.assertTrue(
            crash[
                "last_known_good_must_remain_identifiable"
            ]
        )
        self.assertTrue(
            crash[
                "no_recursive_delete_of_only_good_generation"
            ]
        )
        self.assertTrue(
            crash["recovery_must_be_deterministic"]
        )

    def test_obsidian_open_requires_separate_subqualification(
        self,
    ) -> None:
        policy = self.contract[
            "obsidian_open_policy"
        ]
        self.assertTrue(
            policy[
                "filesystem_primitive_must_pass_before_any_obsidian_open_test"
            ]
        )
        self.assertTrue(
            policy[
                "live_user_vault_must_not_be_used_for_open_state_experiment"
            ]
        )
        self.assertTrue(
            policy[
                "sacrificial_sandbox_vault_required"
            ]
        )
        self.assertTrue(
            policy[
                "filesystem_pass_alone_does_not_authorize_live_promotion_while_obsidian_open"
            ]
        )

    def test_all_fail_is_valid(self) -> None:
        evidence = self.contract["evidence"]
        self.assertTrue(
            evidence["all_fail_is_valid_outcome"]
        )
        self.assertTrue(
            evidence[
                "no_candidate_may_be_selected_by_preference_without_metrics"
            ]
        )

    def test_p5c_contract_authorizes_no_execution(
        self,
    ) -> None:
        boundary = self.contract[
            "p5c_boundary"
        ]
        self.assertTrue(
            boundary["contract_tests_only"]
        )
        for key in (
            "live_vault_experiment_authorized",
            "sandbox_experiment_authorized",
            "background_observer_authorized",
            "continuous_projection_authorized",
            "windows_task_registration_authorized",
        ):
            with self.subTest(key=key):
                self.assertFalse(boundary[key])

    def test_breakers_are_unique_and_sufficient(
        self,
    ) -> None:
        breakers = self.contract[
            "required_breakers"
        ]
        self.assertGreaterEqual(
            len(breakers),
            25,
        )
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gate_is_p5c2(self) -> None:
        self.assertEqual(
            self.contract["next_gate"],
            "P5C2_PROMOTION_EXPERIMENT_HARNESS_CANDIDATE",
        )


if __name__ == "__main__":
    unittest.main()
