from __future__ import annotations

import json
import unittest
from pathlib import Path


class MaterializationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[2]
        path = (
            root
            / "tools"
            / "obsidian_projection"
            / "materialization_contract_v0_1.json"
        )
        cls.contract = json.loads(
            path.read_text(encoding="utf-8")
        )

    def test_bound_to_qualified_p2b(self) -> None:
        self.assertEqual(
            self.contract["qualified_p2b_head"],
            "157b519dafb226e53ae13a281f7dc294d584cc0d",
        )
        self.assertEqual(
            self.contract["p2a_contract_blob_sha"],
            "c546b7116c68ee17fd0ff5868748bb4b1bbae1f3",
        )
        self.assertEqual(
            self.contract["frozen_source_commit"],
            "7bd8c1312430dfc3def5523eb65397a5d6a5ae05",
        )
        self.assertEqual(
            self.contract["frozen_source_tree"],
            "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b",
        )
        self.assertEqual(
            self.contract["pilot_artifact_count"],
            74,
        )

    def test_p2_core_is_blob_pinned(self) -> None:
        pinned = self.contract[
            "qualified_p2_core_blobs"
        ]
        self.assertEqual(
            set(pinned),
            {
                "tools/obsidian_projection/rendering.py",
                "tools/obsidian_projection/relations.py",
                "tools/obsidian_projection/integrity.py",
                "tools/obsidian_projection/builder.py",
                "tools/obsidian_projection/p2_verify.py",
            },
        )
        for sha in pinned.values():
            self.assertRegex(
                sha,
                r"^[0-9a-f]{40}$",
            )

    def test_p3a_itself_authorizes_no_materialization(self) -> None:
        boundary = self.contract["p3a_boundary"]
        self.assertTrue(
            boundary[
                "documentation_and_breakers_only"
            ]
        )
        self.assertFalse(
            boundary[
                "materialization_code_authorized"
            ]
        )
        self.assertFalse(
            boundary["appdata_write_authorized"]
        )
        self.assertFalse(
            boundary[
                "final_vault_creation_authorized"
            ]
        )
        self.assertFalse(
            boundary[
                "incoming_directory_creation_authorized"
            ]
        )

    def test_destination_is_exact_and_must_not_exist(self) -> None:
        destination = self.contract["destination"]
        self.assertEqual(
            destination["expression"],
            (
                "%LOCALAPPDATA%\\"
                "ATDS-OBSIDIAN-PROJECTION"
            ),
        )
        self.assertEqual(
            destination["observed_resolved_path"],
            (
                "C:\\Users\\Boulevart\\AppData\\Local\\"
                "ATDS-OBSIDIAN-PROJECTION"
            ),
        )
        self.assertEqual(
            destination["expected_filesystem"],
            "NTFS",
        )
        self.assertTrue(
            destination[
                "final_path_must_not_exist_before_attempt"
            ]
        )

    def test_destination_alias_and_sync_conditions_fail_closed(
        self,
    ) -> None:
        destination = self.contract["destination"]
        self.assertTrue(
            destination[
                "known_sync_root_containment_forbidden"
            ]
        )
        self.assertTrue(
            destination[
                "reparse_symlink_junction_ancestor_forbidden"
            ]
        )
        self.assertEqual(
            destination[
                "path_resolution_ambiguity"
            ],
            "BLOCK",
        )

    def test_arbitrary_temp_build_is_not_authority(self) -> None:
        source = self.contract[
            "source_build_authority"
        ]
        self.assertFalse(
            source[
                "arbitrary_temp_directory_allowed"
            ]
        )
        self.assertFalse(
            source[
                "human_supplied_path_alone_sufficient"
            ]
        )
        self.assertTrue(
            source[
                "source_must_be_fresh_p2_execution"
            ]
        )
        self.assertEqual(
            source[
                "source_execution_required_status"
            ],
            "PASS",
        )
        self.assertEqual(
            source[
                "source_execution_required_artifact_record_count"
            ],
            74,
        )
        self.assertTrue(
            source[
                "source_execution_required_double_build_byte_match"
            ]
        )

    def test_source_identity_freezes_all_p2_digests_and_counts(
        self,
    ) -> None:
        fields = set(
            self.contract[
                "source_build_authority"
            ][
                "frozen_source_projection_identity_fields"
            ]
        )
        self.assertEqual(
            fields,
            {
                "semantic_record_digest_sha256",
                "artifact_set_digest_sha256",
                "relation_set_digest_sha256",
                "integrity_manifest_sha256",
                "projection_tree_digest_sha256",
                "artifact_record_count",
                "relation_record_count",
                "generated_file_count",
            },
        )

    def test_incoming_is_sibling_and_not_final(self) -> None:
        incoming = self.contract[
            "incoming_materialization"
        ]
        self.assertEqual(
            incoming["location"],
            (
                "SIBLING_UNDER_LOCALAPPDATA_"
                "SAME_PARENT_AS_FINAL"
            ),
        )
        self.assertEqual(
            incoming["preexisting_incoming_path"],
            "BLOCK",
        )
        self.assertTrue(
            incoming[
                "create_directory_exclusively"
            ]
        )
        self.assertTrue(
            incoming[
                "capture_filesystem_identity_immediately"
            ]
        )

    def test_incoming_structure_has_empty_views_no_obsidian(
        self,
    ) -> None:
        incoming = self.contract[
            "incoming_materialization"
        ]
        self.assertIn(
            "views/",
            incoming[
                "required_initial_structure"
            ],
        )
        self.assertTrue(
            incoming["views_must_be_empty"]
        )
        self.assertTrue(
            incoming[
                "obsidian_directory_must_be_absent"
            ]
        )

    def test_incoming_copy_is_exclusive_byte_copy_only(
        self,
    ) -> None:
        incoming = self.contract[
            "incoming_materialization"
        ]
        self.assertEqual(
            incoming["copy_file_mode"],
            "CREATE_NEW_EXCLUSIVE",
        )
        self.assertTrue(
            incoming["overwrite_forbidden"]
        )
        self.assertTrue(
            incoming["hard_link_copy_forbidden"]
        )
        self.assertTrue(
            incoming["symlink_copy_forbidden"]
        )
        self.assertTrue(
            incoming[
                "junction_reparse_copy_forbidden"
            ]
        )
        self.assertTrue(
            incoming[
                "source_file_bytes_must_be_copied_exactly"
            ]
        )

    def test_incoming_must_verify_before_final_name(self) -> None:
        verify = self.contract[
            "incoming_verification"
        ]
        self.assertTrue(
            verify[
                "before_final_rename_required"
            ]
        )
        self.assertTrue(
            verify[
                "exact_generated_relative_path_set_match"
            ]
        )
        self.assertTrue(
            verify["exact_file_sha256_match"]
        )
        self.assertEqual(
            verify["hard_link_count_required"],
            1,
        )
        self.assertTrue(
            verify[
                "integrity_manifest_must_verify_all_entries_clean"
            ]
        )
        self.assertEqual(
            verify["any_mismatch"],
            "BLOCK_BEFORE_FINAL_NAME",
        )

    def test_final_promotion_is_single_same_volume_rename(
        self,
    ) -> None:
        promotion = self.contract[
            "final_promotion"
        ]
        self.assertEqual(
            promotion["operation"],
            (
                "SINGLE_DIRECTORY_RENAME_"
                "WITHIN_SAME_NTFS_VOLUME"
            ),
        )
        self.assertTrue(
            promotion[
                "target_must_be_absent_immediately_before_rename"
            ]
        )
        self.assertTrue(
            promotion[
                "overwrite_existing_final_forbidden"
            ]
        )
        self.assertTrue(
            promotion[
                "cross_volume_rename_forbidden"
            ]
        )
        self.assertTrue(
            promotion[
                "copy_directly_to_final_forbidden"
            ]
        )

    def test_post_promotion_verification_is_mandatory(
        self,
    ) -> None:
        verify = self.contract[
            "post_promotion_verification"
        ]
        self.assertTrue(verify["mandatory"])
        self.assertTrue(
            verify[
                "same_filesystem_identity_as_incoming_object_required"
            ]
        )
        self.assertTrue(
            verify["exact_file_sha256_match"]
        )
        self.assertTrue(
            verify[
                "integrity_manifest_all_clean"
            ]
        )
        self.assertTrue(
            verify[
                "repository_branch_unchanged"
            ]
        )
        self.assertTrue(
            verify["repository_head_unchanged"]
        )
        self.assertTrue(
            verify[
                "repository_working_tree_unchanged"
            ]
        )

    def test_pre_rename_cleanup_requires_identity_match(
        self,
    ) -> None:
        failure = self.contract[
            "failure_protocol"
        ]["before_final_rename"]
        self.assertTrue(
            failure[
                "incoming_may_be_cleaned_only_if_current_attempt_identity_matches"
            ]
        )
        self.assertEqual(
            failure[
                "incoming_cleanup_identity_mismatch"
            ],
            "DO_NOT_DELETE_BLOCK",
        )

    def test_post_rename_failure_is_never_qualified(
        self,
    ) -> None:
        failure = self.contract[
            "failure_protocol"
        ]["after_final_rename"]
        self.assertTrue(
            failure[
                "final_is_unqualified_until_post_promotion_verification_passes"
            ]
        )
        self.assertFalse(
            failure[
                "automatic_recursive_delete_forbidden"
            ]
            is False
        )
        self.assertEqual(
            failure["preferred_action"],
            "QUARANTINE_BY_SAME_VOLUME_RENAME",
        )
        self.assertEqual(
            failure["quarantine_failure"],
            (
                "LEAVE_IN_PLACE_MARK_OPERATION_"
                "BLOCKED_DO_NOT_OPEN"
            ),
        )

    def test_crash_recovery_never_inferrs_qualification(
        self,
    ) -> None:
        crash = self.contract[
            "failure_protocol"
        ]["power_loss_or_process_crash"]
        self.assertTrue(
            crash[
                "never_infer_qualification_from_folder_name"
            ]
        )
        self.assertEqual(
            crash[
                "incoming_path_present_means"
            ],
            (
                "UNQUALIFIED_INCOMPLETE_OR_"
                "UNADJUDICATED"
            ),
        )

    def test_qualification_is_external_to_vault_bytes(
        self,
    ) -> None:
        q = self.contract[
            "qualification_record"
        ]
        self.assertFalse(q["stored_inside_vault"])
        self.assertFalse(
            q[
                "deterministic_generated_tree_modified_by_materialization"
            ]
        )
        self.assertTrue(
            q["folder_name_is_not_qualification"]
        )
        self.assertTrue(
            q[
                "build_manifest_is_not_materialization_qualification"
            ]
        )
        self.assertTrue(
            q[
                "integrity_manifest_is_not_materialization_qualification"
            ]
        )

    def test_obsidian_plugins_sync_remain_forbidden(self) -> None:
        boundary = self.contract["p3a_boundary"]
        self.assertFalse(
            boundary["obsidian_launch_authorized"]
        )
        self.assertFalse(
            boundary[
                "obsidian_config_creation_authorized"
            ]
        )
        self.assertFalse(
            boundary["plugins_authorized"]
        )
        self.assertFalse(
            boundary["sync_authorized"]
        )

    def test_next_gate_is_materialization_candidate_only(
        self,
    ) -> None:
        gate = self.contract["next_action_gate"]
        self.assertEqual(
            gate["allowed_after_persisted_rebreak"],
            (
                "P3B_MATERIALIZATION_"
                "IMPLEMENTATION_CANDIDATE"
            ),
        )
        self.assertFalse(
            gate["may_create_obsidian_directory"]
        )
        self.assertFalse(
            gate["may_launch_obsidian"]
        )
        self.assertFalse(
            gate["may_install_plugins"]
        )
        self.assertFalse(
            gate["may_enable_sync"]
        )
        self.assertFalse(
            gate["may_modify_p2_core"]
        )

    def test_critical_breakers_are_preregistered(self) -> None:
        breakers = set(
            self.contract["acceptance_breakers"]
        )
        expected = {
            "final destination already exists",
            "destination filesystem not NTFS",
            "qualified P2 core blob changed",
            "arbitrary TEMP folder substituted",
            "incoming path preexists",
            "direct copy to final attempted",
            "hard-link used instead of byte copy",
            "incoming hash mismatch",
            "final appears before incoming verification completes",
            "cross-volume promotion attempted",
            "post-rename file hash mismatch",
            "repository working tree changed",
            "rollback tries to delete identity-mismatched directory",
            "post-rename failure still reported qualified",
            "folder name treated as qualification",
        }
        self.assertTrue(
            expected.issubset(breakers)
        )


if __name__ == "__main__":
    unittest.main()
