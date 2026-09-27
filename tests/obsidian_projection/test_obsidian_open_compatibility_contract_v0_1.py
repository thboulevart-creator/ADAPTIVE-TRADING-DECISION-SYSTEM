from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5C3ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "obsidian_open_compatibility_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_OPEN_COMPATIBILITY_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_exact_p5c2_predecessor_is_pinned(self) -> None:
        self.assertEqual(
            self.contract[
                "qualified_predecessor_p5c2_head"
            ],
            "33c6184d8404b6cb0f59dbb0ead68949ece27544",
        )

    def test_selected_primitive_is_exact(self) -> None:
        self.assertEqual(
            self.contract[
                "selected_filesystem_primitive"
            ],
            "IMMUTABLE_GENERATION_ATOMIC_POINTER",
        )

    def test_real_vault_is_never_experiment_target(
        self,
    ) -> None:
        live = self.contract["live_vault"]
        self.assertFalse(live["experiment_target"])
        self.assertFalse(live["mutation_authorized"])
        self.assertFalse(
            live["generated_mutation_authorized"]
        )
        self.assertFalse(
            live["views_mutation_authorized"]
        )
        self.assertFalse(
            live[
                "obsidian_config_mutation_authorized"
            ]
        )

    def test_sacrificial_vault_is_separate(self) -> None:
        sandbox = self.contract[
            "sacrificial_vault"
        ]
        self.assertIn(
            "ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX",
            sandbox["path"],
        )
        self.assertTrue(
            sandbox["same_onedrive_root_required"]
        )
        self.assertTrue(sandbox["sacrificial"])
        self.assertTrue(
            sandbox["must_not_overlap_live_vault"]
        )
        self.assertTrue(
            sandbox["must_be_absent_before_prepare"]
        )

    def test_safe_obsidian_seed_forbids_sync_plugins(
        self,
    ) -> None:
        seed = self.contract[
            "safe_obsidian_seed"
        ]
        self.assertTrue(
            seed[
                "live_core_plugins_must_show_sync_disabled"
            ]
        )
        self.assertEqual(
            seed["community_plugins_seed"],
            "EMPTY_LIST",
        )
        self.assertFalse(
            seed["obsidian_sync_authorized"]
        )
        self.assertFalse(
            seed["community_plugin_authorized"]
        )

    def test_fixture_is_full_markdown_generation(
        self,
    ) -> None:
        fixture = self.contract["fixture"]
        self.assertEqual(
            fixture["generation_ids"],
            ["GEN_A", "GEN_B"],
        )
        self.assertEqual(
            fixture["notes_per_generation"],
            128,
        )
        self.assertEqual(
            fixture["nested_directories"],
            8,
        )
        self.assertTrue(
            fixture["index_note_required"]
        )
        self.assertTrue(
            fixture[
                "each_note_embeds_generation_id"
            ]
        )
        self.assertTrue(
            fixture["immutable_after_prepare"]
        )

    def test_current_note_uses_atomic_replace(self) -> None:
        pointer = self.contract[
            "live_pointer_note"
        ]
        self.assertEqual(
            pointer["path"],
            "CURRENT.md",
        )
        self.assertEqual(
            pointer["update_primitive"],
            "WRITE_TEMP_FSYNC_OS_REPLACE",
        )
        self.assertTrue(
            pointer["direct_in_place_write_forbidden"]
        )

    def test_snapshot_persistence_is_redundant(
        self,
    ) -> None:
        snapshot = self.contract[
            "snapshot_persistence"
        ]
        self.assertTrue(
            snapshot[
                "localappdata_primary_required"
            ]
        )
        self.assertTrue(
            snapshot[
                "onedrive_control_backup_required"
            ]
        )
        self.assertIn(
            "ATDS-P5C3-CONTROL-EVIDENCE",
            snapshot[
                "onedrive_control_root"
            ],
        )
        self.assertTrue(
            snapshot[
                "both_copies_must_be_byte_identical"
            ]
        )
        self.assertTrue(
            snapshot[
                "run_open_may_use_either_verified_copy"
            ]
        )
        self.assertTrue(
            snapshot[
                "single_copy_disappearance_must_not_force_sandbox_rebuild"
            ]
        )
        self.assertTrue(
            snapshot[
                "both_copies_missing_blocks"
            ]
        )

    def test_prepare_requires_obsidian_closed(self) -> None:
        prepare = self.contract["prepare_phase"]
        self.assertTrue(
            prepare["obsidian_must_be_closed"]
        )
        self.assertFalse(
            prepare["automatic_obsidian_launch"]
        )
        self.assertEqual(
            prepare["initializes_current_to"],
            "GEN_A",
        )

    def test_open_proof_requires_running_obsidian_and_workspace(
        self,
    ) -> None:
        proof = self.contract["open_proof"]
        self.assertTrue(
            proof[
                "obsidian_process_must_be_running"
            ]
        )
        self.assertTrue(
            proof["workspace_json_required"]
        )
        self.assertEqual(
            proof["workspace_must_reference"],
            "CURRENT.md",
        )
        self.assertTrue(
            proof["sync_must_be_disabled"]
        )
        self.assertTrue(
            proof[
                "community_plugins_must_be_empty_or_absent"
            ]
        )

    def test_open_experiment_scale_is_exact(self) -> None:
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
        self.assertLessEqual(
            experiment[
                "reader_interval_ms_max"
            ],
            10,
        )
        self.assertTrue(
            experiment[
                "at_least_one_fresh_reader_sample_per_cycle"
            ]
        )

    def test_open_experiment_requires_zero_anomalies(
        self,
    ) -> None:
        experiment = self.contract[
            "open_experiment"
        ]
        for field in (
            "pointer_write_error_count_must_equal",
            "mixed_generation_count_must_equal",
            "missing_entrypoint_count_must_equal",
            "partial_generation_count_must_equal",
            "parse_error_count_must_equal",
        ):
            with self.subTest(field=field):
                self.assertEqual(
                    experiment[field],
                    0,
                )

    def test_final_generation_is_pre_registered(
        self,
    ) -> None:
        self.assertEqual(
            self.contract[
                "open_experiment"
            ]["final_generation_expected"],
            "GEN_A",
        )

    def test_manual_visual_acceptance_is_required(
        self,
    ) -> None:
        manual = self.contract[
            "manual_visual_acceptance"
        ]
        self.assertTrue(manual["required"])
        self.assertTrue(
            manual["while_obsidian_still_open"]
        )
        self.assertEqual(
            manual["expected_visible_note"],
            "CURRENT.md",
        )
        self.assertEqual(
            manual[
                "expected_final_generation"
            ],
            "GEN_A",
        )
        self.assertTrue(
            manual[
                "automated_filesystem_pass_alone_is_insufficient"
            ]
        )

    def test_post_close_is_mandatory(self) -> None:
        post = self.contract[
            "post_close_phase"
        ]
        self.assertTrue(
            post["obsidian_must_be_fully_closed"]
        )
        self.assertTrue(
            post[
                "pointer_final_state_must_match_expected"
            ]
        )
        self.assertTrue(
            post[
                "both_generation_tree_digests_must_match_prepare_snapshot"
            ]
        )

    def test_graph_semantics_remain_open(self) -> None:
        graph = self.contract[
            "graph_indexing_boundary"
        ]
        self.assertTrue(
            graph[
                "p5c3_does_not_qualify_native_graph_current_generation_semantics"
            ]
        )
        self.assertTrue(
            graph[
                "duplicate_generation_indexing_problem_remains_open"
            ]
        )
        self.assertEqual(
            graph["resolution_deferred_to"],
            "P6_CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
        )

    def test_pass_does_not_authorize_production(
        self,
    ) -> None:
        result = self.contract[
            "qualification_result"
        ]
        self.assertTrue(
            result[
                "filesystem_only_pass_is_insufficient"
            ]
        )
        self.assertFalse(
            result[
                "production_promotion_authorized_on_p5c3_pass"
            ]
        )
        self.assertFalse(
            result[
                "continuous_observer_authorized_on_p5c3_pass"
            ]
        )

    def test_p5c3_boundary_is_narrow(self) -> None:
        boundary = self.contract[
            "p5c3_boundary"
        ]
        self.assertTrue(
            boundary[
                "contract_and_sandbox_harness_only"
            ]
        )
        for field in (
            "real_vault_experiment_authorized",
            "automatic_obsidian_launch_authorized",
            "continuous_observer_authorized",
            "production_promotion_authorized",
            "windows_task_registration_authorized",
            "human_views_overwrite_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(
                    boundary[field]
                )

    def test_required_breakers_are_unique_and_broad(
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

    def test_next_gate_is_p5d(self) -> None:
        self.assertEqual(
            self.contract["next_gate_on_pass"],
            "P5D_CONTINUOUS_OBSERVER_IMPLEMENTATION_CANDIDATE",
        )


if __name__ == "__main__":
    unittest.main()
