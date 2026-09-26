from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


class OneDriveFirstOpenSafetyContractV02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "first_open_safety_contract_v0_2.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_FIRST_OPEN_SAFETY_CONTRACT_V0_2",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_predecessor_pins(self) -> None:
        self.assertEqual(
            self.contract["predecessor_p3c_head"],
            "fa1e24e20acbfba60de2c3ebaaa7dc5427778851",
        )
        self.assertEqual(
            self.contract["predecessor_p3d_head"],
            "3cafa6e98ec45236aba48ddf60e55957e49bed76",
        )
        self.assertEqual(
            self.contract["qualified_p3b_head"],
            "bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba",
        )
        self.assertEqual(
            self.contract["qualified_p2b_head"],
            "157b519dafb226e53ae13a281f7dc294d584cc0d",
        )

    def test_predecessor_v01_blob_is_unchanged(self) -> None:
        predecessor = (
            self.root
            / "tools"
            / "obsidian_projection"
            / "first_open_safety_contract_v0_1.json"
        )
        raw = predecessor.read_bytes()
        oid = hashlib.sha1(
            f"blob {len(raw)}\0".encode("ascii") + raw
        ).hexdigest()
        self.assertEqual(
            oid,
            "5cd11e9512249da26adf4b6f86e79259af725809",
        )

    def test_new_vault_path_is_exact_onedrive_destination(self) -> None:
        vault = self.contract["materialized_vault"]
        self.assertEqual(
            vault["observed_resolved_path"],
            (
                "C:\\Users\\Boulevart\\OneDrive\\Bureau\\ATDS\\"
                "ATDS-OBSIDIAN-PROJECTION"
            ),
        )
        self.assertEqual(
            vault["authority_role"],
            "DERIVED",
        )
        self.assertEqual(
            vault["canonical_source"],
            "GitHub/ATDS",
        )

    def test_host_sync_and_obsidian_sync_are_distinct(self) -> None:
        vault = self.contract["materialized_vault"]
        boundary = self.contract["p3c2_boundary"]
        self.assertEqual(
            vault["host_storage_environment"],
            "ONEDRIVE_CLOUD_FILES",
        )
        self.assertTrue(
            boundary[
                "onedrive_host_sync_environment_accepted_for_candidate_requalification"
            ]
        )
        self.assertFalse(
            vault["obsidian_sync_authorized"]
        )
        self.assertFalse(
            boundary["obsidian_sync_authorized"]
        )

    def test_relocation_evidence_binds_qualified_projection(self) -> None:
        evidence = self.contract["relocation_evidence"]
        self.assertEqual(
            evidence["evidence_status"],
            "REPORTED_LOCAL_EXECUTION",
        )
        self.assertEqual(
            evidence["generated_file_count"],
            92,
        )
        self.assertEqual(
            evidence["projection_tree_entry_count"],
            91,
        )
        self.assertEqual(
            evidence["integrity_manifest_sha256"],
            "a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b",
        )
        self.assertEqual(
            evidence["projection_tree_digest_sha256"],
            "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0",
        )

    def test_native_reparse_observation_is_exact(self) -> None:
        evidence = self.contract["relocation_evidence"]
        self.assertEqual(
            evidence["native_reparse_file_count"],
            92,
        )
        self.assertEqual(
            evidence["native_reparse_tag_hex"],
            "0x9000601A",
        )
        self.assertEqual(
            evidence["native_reparse_tag_name"],
            "IO_REPARSE_TAG_CLOUD_6",
        )
        self.assertEqual(
            evidence["native_reparse_tag_count"],
            92,
        )

    def test_relocation_evidence_has_no_unsafe_file_state(self) -> None:
        evidence = self.contract["relocation_evidence"]
        for field in (
            "symlink_files",
            "junction_files",
            "offline_files",
            "sparse_files",
            "unreadable_files",
        ):
            self.assertEqual(
                evidence[field],
                0,
                field,
            )

    def test_file_reparse_allowlist_is_narrow(self) -> None:
        policy = self.contract["onedrive_reparse_policy"]
        self.assertEqual(
            policy["allowed_regular_file_reparse_classes"],
            [
                "NO_REPARSE_POINT",
                "IO_REPARSE_TAG_CLOUD_6:0x9000601A",
            ],
        )
        self.assertFalse(
            policy["other_reparse_tags_allowed"]
        )
        self.assertFalse(
            policy["directory_reparse_points_allowed"]
        )
        self.assertFalse(
            policy["symlinks_allowed"]
        )
        self.assertFalse(
            policy["junctions_allowed"]
        )
        self.assertFalse(
            policy["mount_points_allowed"]
        )

    def test_offline_sparse_unreadable_remain_forbidden(self) -> None:
        policy = self.contract["onedrive_reparse_policy"]
        self.assertFalse(
            policy["offline_files_allowed"]
        )
        self.assertFalse(
            policy["sparse_files_allowed"]
        )
        self.assertFalse(
            policy["unreadable_files_allowed"]
        )

    def test_reparse_metadata_cannot_replace_byte_integrity(self) -> None:
        policy = self.contract["onedrive_reparse_policy"]
        self.assertTrue(
            policy[
                "exact_bytes_still_authoritative_for_projection_integrity"
            ]
        )
        self.assertEqual(
            policy[
                "metadata_class_change_between_no_reparse_and_cloud_6"
            ],
            "ALLOWED_ONLY_IF_ALL_OTHER_GATES_PASS",
        )

    def test_p3c2_does_not_authorize_execution(self) -> None:
        boundary = self.contract["p3c2_boundary"]
        self.assertTrue(
            boundary["contract_and_tests_only"]
        )
        for field in (
            "obsidian_launch_authorized",
            "obsidian_directory_creation_authorized",
            "vault_write_authorized",
            "generated_write_authorized",
            "views_write_authorized",
            "community_plugins_authorized",
            "obsidian_sync_authorized",
            "git_automation_authorized",
        ):
            self.assertFalse(
                boundary[field],
                field,
            )

    def test_fresh_p2_reconstruction_remains_mandatory(self) -> None:
        gate = self.contract["pre_open_reconstruction"]
        self.assertTrue(gate["mandatory"])
        self.assertTrue(
            gate["fresh_p2_execution_required"]
        )
        self.assertTrue(
            gate["fresh_p2_double_build_required"]
        )
        self.assertTrue(
            gate[
                "fresh_p2_double_build_byte_match_required"
            ]
        )
        self.assertTrue(
            gate[
                "current_vault_generated_must_equal_fresh_p2_build_a"
            ]
        )
        self.assertEqual(
            gate["expected_generated_file_count"],
            92,
        )

    def test_preopen_native_gate_requires_native_inspection(self) -> None:
        gate = self.contract["pre_open_filesystem_gate"]
        self.assertTrue(
            gate["native_reparse_inspection_required"]
        )
        self.assertEqual(
            gate["inspection_mechanism"],
            (
                "WINDOWS_NATIVE_FSUTIL_REPARSEPOINT_QUERY_"
                "OR_EQUIVALENT_NATIVE_API"
            ),
        )
        self.assertEqual(
            gate["unexpected_reparse_tag_result"],
            "BLOCK_FIRST_OPEN",
        )

    def test_snapshot_includes_reparse_policy_summary(self) -> None:
        snapshot = self.contract["pre_open_snapshot"]
        self.assertEqual(
            snapshot["storage_location"],
            "OS_TEMP_OUTSIDE_VAULT",
        )
        self.assertFalse(
            snapshot["deterministic_vault_bytes_modified"]
        )
        self.assertIn(
            "generated_reparse_policy_summary",
            snapshot["required_fields"],
        )

    def test_first_open_remains_manual(self) -> None:
        operation = self.contract["first_open_operation"]
        self.assertEqual(
            operation["execution_model"],
            "TWO_PHASE_MANUAL_OPEN",
        )
        self.assertTrue(
            operation["automatic_obsidian_launch_forbidden"]
        )
        self.assertTrue(
            operation[
                "obsidian_must_be_fully_closed_before_post_check"
            ]
        )

    def test_obsidian_directory_policy_accepts_only_bounded_cloud_metadata(self) -> None:
        policy = self.contract["obsidian_directory_policy"]
        self.assertEqual(
            policy["regular_json_file_reparse_classes_allowed"],
            [
                "NO_REPARSE_POINT",
                "IO_REPARSE_TAG_CLOUD_6:0x9000601A",
            ],
        )
        self.assertFalse(
            policy["directory_reparse_points_allowed"]
        )
        self.assertFalse(
            policy["other_reparse_tags_allowed"]
        )
        self.assertFalse(policy["offline_allowed"])
        self.assertFalse(policy["sparse_allowed"])

    def test_community_plugins_and_obsidian_sync_remain_forbidden(self) -> None:
        policy = self.contract["obsidian_directory_policy"]
        self.assertTrue(
            policy["plugins_directory_forbidden"]
        )
        self.assertTrue(
            policy[
                "community_plugins_file"
            ][
                "allowed_if_present_only_when_valid_json_empty_array"
            ]
        )
        self.assertTrue(
            policy[
                "core_plugins_file"
            ][
                "obsidian_sync_enablement_forbidden"
            ]
        )

    def test_generated_gate_is_still_byte_exact(self) -> None:
        gate = self.contract["generated_before_after_gate"]
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
        self.assertEqual(
            gate["any_byte_change_result"],
            "BLOCK_FIRST_OPEN_QUALIFICATION",
        )

    def test_repository_gate_is_unchanged(self) -> None:
        gate = self.contract["repository_before_after_gate"]
        self.assertTrue(gate["branch_equal"])
        self.assertTrue(gate["head_equal"])
        self.assertTrue(
            gate["status_porcelain_equal"]
        )

    def test_failure_protocol_never_repairs_evidence(self) -> None:
        failure = self.contract["failure_protocol"]
        self.assertTrue(
            failure["no_recursive_delete"]
        )
        self.assertTrue(
            failure["no_generated_auto_restore"]
        )
        self.assertTrue(
            failure["no_obsidian_config_auto_cleanup"]
        )
        self.assertTrue(
            failure["preserve_evidence_for_adjudication"]
        )

    def test_next_gate_is_p3d2_only(self) -> None:
        gate = self.contract["next_action_gate"]
        self.assertEqual(
            gate["allowed_after_persisted_rebreak"],
            (
                "P3D2_ONEDRIVE_FIRST_OPEN_SAFETY_"
                "HARNESS_IMPLEMENTATION_CANDIDATE"
            ),
        )
        self.assertFalse(
            gate["may_launch_obsidian"]
        )
        self.assertFalse(
            gate["may_modify_generated"]
        )
        self.assertFalse(
            gate["may_modify_views"]
        )
        self.assertFalse(
            gate["may_enable_obsidian_sync"]
        )


if __name__ == "__main__":
    unittest.main()
