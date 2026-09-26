from __future__ import annotations

import json
import unittest
from pathlib import Path


class FirstOpenSafetyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[2]
        path = (
            root
            / "tools"
            / "obsidian_projection"
            / "first_open_safety_contract_v0_1.json"
        )
        cls.contract = json.loads(
            path.read_text(encoding="utf-8")
        )

    def test_bound_to_qualified_p3b(self) -> None:
        self.assertEqual(
            self.contract["qualified_p3b_head"],
            "bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba",
        )

    def test_materialized_vault_remains_derived(self) -> None:
        vault = self.contract["materialized_vault"]
        self.assertEqual(
            vault["authority_role"],
            "DERIVED",
        )
        self.assertEqual(
            vault["canonical_source"],
            "GitHub/ATDS",
        )
        self.assertEqual(
            vault["generated_owner"],
            "MACHINE",
        )
        self.assertEqual(
            vault["views_owner"],
            "HUMAN",
        )

    def test_missing_p3b_digests_are_not_invented(self) -> None:
        basis = self.contract[
            "p3b_adjudication_basis"
        ]
        self.assertFalse(
            basis[
                "p3b_json_report_available_in_conversation"
            ]
        )
        self.assertFalse(
            basis[
                "p3b_digest_values_available_in_conversation"
            ]
        )
        self.assertEqual(
            basis["bounded_materialization_status"],
            (
                "PASS_WITH_CRYPTOGRAPHIC_"
                "RECONSTRUCTION_REQUIRED_BEFORE_FIRST_OPEN"
            ),
        )

    def test_p3c_itself_cannot_open_or_write_vault(self) -> None:
        boundary = self.contract["p3c_boundary"]
        self.assertTrue(
            boundary[
                "adjudication_and_contract_only"
            ]
        )
        self.assertFalse(
            boundary[
                "first_open_harness_code_authorized"
            ]
        )
        self.assertFalse(
            boundary["obsidian_launch_authorized"]
        )
        self.assertFalse(
            boundary[
                "obsidian_directory_creation_authorized"
            ]
        )
        self.assertFalse(
            boundary["vault_write_authorized"]
        )
        self.assertFalse(
            boundary["generated_write_authorized"]
        )
        self.assertFalse(
            boundary["views_write_authorized"]
        )

    def test_fresh_p2_reconstruction_is_required(self) -> None:
        reconstruction = self.contract[
            "pre_open_reconstruction"
        ]
        self.assertTrue(
            reconstruction["mandatory"]
        )
        self.assertTrue(
            reconstruction[
                "fresh_p2_execution_required"
            ]
        )
        self.assertTrue(
            reconstruction[
                "fresh_p2_double_build_required"
            ]
        )
        self.assertTrue(
            reconstruction[
                "fresh_p2_double_build_byte_match_required"
            ]
        )
        self.assertTrue(
            reconstruction[
                "current_vault_generated_must_equal_fresh_p2_build_a"
            ]
        )
        self.assertEqual(
            reconstruction["mismatch_result"],
            "BLOCK_FIRST_OPEN",
        )

    def test_pre_open_snapshot_lives_outside_vault(self) -> None:
        snapshot = self.contract[
            "pre_open_snapshot"
        ]
        self.assertEqual(
            snapshot["storage_location"],
            "OS_TEMP_OUTSIDE_VAULT",
        )
        self.assertFalse(
            snapshot[
                "deterministic_vault_bytes_modified"
            ]
        )

    def test_pre_open_requires_clean_empty_unopened_state(self) -> None:
        state = self.contract[
            "pre_open_snapshot"
        ]["required_state"]
        self.assertTrue(
            state["final_vault_exists"]
        )
        self.assertTrue(
            state["generated_exists"]
        )
        self.assertTrue(
            state["views_exists"]
        )
        self.assertEqual(
            state["views_entry_count"],
            0,
        )
        self.assertFalse(
            state["obsidian_directory_present"]
        )
        self.assertEqual(
            state["vault_top_level_entries"],
            ["generated", "views"],
        )
        self.assertEqual(
            state["generated_integrity"],
            "ALL_CLEAN",
        )

    def test_first_open_is_two_phase_manual(self) -> None:
        op = self.contract[
            "first_open_operation"
        ]
        self.assertEqual(
            op["execution_model"],
            "TWO_PHASE_MANUAL_OPEN",
        )
        self.assertTrue(
            op[
                "automatic_obsidian_launch_forbidden"
            ]
        )
        self.assertTrue(
            op[
                "user_content_edits_during_first_open_forbidden"
            ]
        )
        self.assertTrue(
            op[
                "views_edits_during_first_open_forbidden"
            ]
        )
        self.assertTrue(
            op[
                "generated_edits_during_first_open_forbidden"
            ]
        )
        self.assertTrue(
            op[
                "obsidian_must_be_fully_closed_before_post_check"
            ]
        )
        self.assertEqual(
            op["post_check_while_obsidian_running"],
            "BLOCK",
        )

    def test_obsidian_directory_has_no_semantic_authority(self) -> None:
        policy = self.contract[
            "obsidian_directory_policy"
        ]
        self.assertTrue(
            policy[
                "may_be_created_during_first_open"
            ]
        )
        self.assertEqual(
            policy["semantic_authority"],
            "NONE",
        )
        self.assertFalse(
            policy["may_be_semantic_input"]
        )

    def test_obsidian_policy_is_root_json_only(self) -> None:
        policy = self.contract[
            "obsidian_directory_policy"
        ]
        self.assertTrue(
            policy[
                "root_regular_json_files_allowed"
            ]
        )
        self.assertFalse(
            policy[
                "root_non_json_files_allowed"
            ]
        )
        self.assertEqual(
            policy["subdirectories_allowed"],
            [],
        )
        self.assertTrue(
            policy[
                "symlink_junction_reparse_forbidden"
            ]
        )
        self.assertTrue(
            policy["non_regular_files_forbidden"]
        )

    def test_community_plugins_must_be_absent_or_empty(self) -> None:
        community = self.contract[
            "obsidian_directory_policy"
        ]["community_plugins_file"]
        self.assertTrue(
            community["allowed_if_absent"]
        )
        self.assertTrue(
            community[
                "allowed_if_present_only_when_valid_json_empty_array"
            ]
        )
        self.assertEqual(
            community["non_empty_or_unparseable"],
            "BLOCK",
        )

    def test_sync_enablement_is_forbidden(self) -> None:
        core = self.contract[
            "obsidian_directory_policy"
        ]["core_plugins_file"]
        self.assertTrue(
            core["sync_enablement_forbidden"]
        )
        self.assertEqual(
            core["sync_plugin_id"],
            "sync",
        )
        self.assertEqual(
            core[
                "if_shape_or_sync_state_cannot_be_interpreted"
            ],
            "BLOCK",
        )

    def test_generated_before_after_is_exact(self) -> None:
        gate = self.contract[
            "generated_before_after_gate"
        ]
        self.assertTrue(
            gate["exact_relative_path_set_equal"]
        )
        self.assertTrue(
            gate["exact_file_size_equal"]
        )
        self.assertTrue(
            gate["exact_file_sha256_equal"]
        )
        self.assertTrue(
            gate["exact_tree_digest_equal"]
        )
        self.assertTrue(
            gate[
                "integrity_manifest_all_clean_after"
            ]
        )
        self.assertTrue(
            gate["build_manifest_unchanged"]
        )

    def test_views_must_stay_empty(self) -> None:
        gate = self.contract[
            "views_before_after_gate"
        ]
        self.assertEqual(
            gate["required_entry_count_before"],
            0,
        )
        self.assertEqual(
            gate["required_entry_count_after"],
            0,
        )

    def test_vault_after_open_has_only_three_top_entries(self) -> None:
        structure = self.contract[
            "vault_structure_after_first_open"
        ]
        self.assertEqual(
            structure["allowed_top_level_entries"],
            [
                "generated",
                "views",
                ".obsidian",
            ],
        )
        self.assertTrue(
            structure["git_directory_forbidden"]
        )
        self.assertTrue(
            structure[
                "vault_filesystem_identity_must_equal_pre_open"
            ]
        )

    def test_repository_must_be_identical_before_after(self) -> None:
        gate = self.contract[
            "repository_before_after_gate"
        ]
        self.assertTrue(gate["branch_equal"])
        self.assertTrue(gate["head_equal"])
        self.assertTrue(
            gate["status_porcelain_equal"]
        )

    def test_first_open_pass_is_external_post_close_only(self) -> None:
        qualification = self.contract[
            "first_open_qualification"
        ]
        self.assertEqual(
            qualification["source"],
            "POST_CLOSE_EXTERNAL_VERIFICATION_ONLY",
        )
        self.assertFalse(
            qualification["stored_inside_vault"]
        )
        self.assertTrue(
            qualification["requires_all_gates"]
        )
        self.assertFalse(
            qualification[
                "folder_name_not_qualification"
            ]
            is False
        )
        self.assertFalse(
            qualification[
                "obsidian_opened_not_qualification"
            ]
            is False
        )

    def test_failure_never_auto_repairs_or_cleans(self) -> None:
        failure = self.contract[
            "failure_protocol"
        ]
        self.assertTrue(
            failure["no_recursive_delete"]
        )
        self.assertTrue(
            failure["no_generated_auto_restore"]
        )
        self.assertTrue(
            failure[
                "no_obsidian_config_auto_cleanup"
            ]
        )
        self.assertTrue(
            failure[
                "preserve_evidence_for_adjudication"
            ]
        )

    def test_next_gate_is_harness_only_not_open(self) -> None:
        gate = self.contract[
            "next_action_gate"
        ]
        self.assertEqual(
            gate["allowed_after_persisted_rebreak"],
            (
                "P3D_FIRST_OPEN_SAFETY_"
                "HARNESS_IMPLEMENTATION_CANDIDATE"
            ),
        )
        self.assertEqual(
            gate["implementation_scope"],
            (
                "PREPARE_SNAPSHOT_AND_"
                "POST_CLOSE_VERIFY_ONLY"
            ),
        )
        self.assertFalse(
            gate["may_launch_obsidian"]
        )
        self.assertFalse(
            gate[
                "may_create_obsidian_directory"
            ]
        )
        self.assertFalse(
            gate["may_modify_generated"]
        )
        self.assertFalse(
            gate["may_modify_views"]
        )

    def test_critical_breakers_are_preregistered(self) -> None:
        breakers = set(
            self.contract["acceptance_breakers"]
        )
        expected = {
            "P3-B digest values invented from terminal marker",
            "first open attempted without fresh P2 reconstruction",
            "current generated tree differs from fresh P2 build",
            "pre-open .obsidian already exists",
            "pre-open views not empty",
            "Obsidian launched automatically by harness",
            "post-check executed while Obsidian still running",
            "generated file hash changed",
            "views changed during first open",
            ".obsidian/plugins exists",
            "community-plugins.json non-empty",
            "core-plugins.json enables sync",
            ".git appears in Vault",
            "Vault filesystem identity changes",
            "repository working tree changes",
            "first-open failure triggers automatic generated repair",
        }
        self.assertTrue(
            expected.issubset(breakers)
        )


if __name__ == "__main__":
    unittest.main()
