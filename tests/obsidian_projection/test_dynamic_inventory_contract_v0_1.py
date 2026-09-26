from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5BDynamicInventoryContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "dynamic_inventory_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_candidate_status(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_DYNAMIC_INVENTORY_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_exact_repository_branch_and_predecessor(
        self,
    ) -> None:
        self.assertEqual(
            self.contract["source_repository"],
            (
                "thboulevart-creator/"
                "ADAPTIVE-TRADING-DECISION-SYSTEM"
            ),
        )
        self.assertEqual(
            self.contract["monitored_branch"],
            "integration/system-v1",
        )
        self.assertEqual(
            self.contract["predecessor_p5a_head"],
            "343d253074abe603eb61bebab29ba58f0bd9301c",
        )

    def test_git_tree_is_inventory_authority(self) -> None:
        authority = self.contract[
            "authority_boundary"
        ]
        self.assertEqual(
            authority["git_tree_of_exact_head"],
            "SOURCE_OF_INVENTORY_TRUTH",
        )
        self.assertEqual(
            authority["local_working_tree"],
            "NOT_INVENTORY_AUTHORITY",
        )

    def test_inventory_is_not_semantic_authority(self) -> None:
        authority = self.contract[
            "authority_boundary"
        ]
        self.assertFalse(
            authority[
                "inventory_may_qualify_artifact"
            ]
        )
        self.assertFalse(
            authority[
                "inventory_may_infer_scientific_status"
            ]
        )
        self.assertFalse(
            authority[
                "inventory_may_infer_epistemic_status"
            ]
        )

    def test_enumeration_is_exact_tree_nul_delimited(
        self,
    ) -> None:
        enum = self.contract["enumeration"]
        self.assertEqual(
            enum["source"],
            "EXACT_GIT_TREE_OBJECT",
        )
        self.assertTrue(
            enum[
                "working_tree_enumeration_forbidden"
            ]
        )
        self.assertTrue(
            enum[
                "git_index_enumeration_as_authority_forbidden"
            ]
        )
        self.assertTrue(enum["nul_delimited_required"])
        self.assertEqual(
            enum["accepted_modes"],
            ["100644", "100755"],
        )

    def test_symlink_and_gitlink_block_head(self) -> None:
        enum = self.contract["enumeration"]
        self.assertEqual(
            enum["symlink_result"],
            "BLOCK_HEAD",
        )
        self.assertEqual(
            enum["gitlink_result"],
            "BLOCK_HEAD",
        )

    def test_no_silent_drop(self) -> None:
        policy = self.contract["selection_policy"]
        self.assertTrue(policy["no_silent_drop"])
        self.assertEqual(
            policy["unknown_top_level_zone"],
            "OTHER_TRACKED",
        )
        self.assertIn(
            "EVERY_TRACKED_REGULAR_BLOB",
            policy["baseline_rule"],
        )

    def test_selection_zone_is_not_semantics(self) -> None:
        policy = self.contract["selection_policy"]
        self.assertTrue(
            policy[
                "selection_zone_is_not_artifact_family"
            ]
        )
        self.assertTrue(
            policy[
                "selection_zone_is_not_authority"
            ]
        )
        self.assertTrue(
            policy[
                "selection_zone_is_not_qualification"
            ]
        )

    def test_core_known_zones_are_present(self) -> None:
        zones = {
            item["prefix"]: item["selection_zone"]
            for item in self.contract[
                "selection_policy"
            ]["known_zones"]
        }
        expected = {
            "GOVERNANCE/": "GOVERNANCE",
            "docs/": "DOCUMENTATION",
            "evidence/": "EVIDENCE",
            "reports/": "REPORT",
            "requirements/": "REQUIREMENT",
            "src/": "IMPLEMENTATION",
            "tests/": "TEST",
            "tools/": "TOOL",
            "breakers/": "BREAKER",
            ".github/":
                "GITHUB_AUTOMATION_OR_CONFIG",
            "04-REFERENCE/": "REFERENCE",
            "99-BACKUP/":
                "HISTORICAL_LINEAGE",
        }
        self.assertEqual(zones, expected)

    def test_root_regular_blob_is_not_dropped(self) -> None:
        self.assertEqual(
            self.contract["selection_policy"][
                "root_regular_blob_zone"
            ],
            "ROOT_DOCUMENT",
        )

    def test_recursive_projection_surfaces_block_head(
        self,
    ) -> None:
        forbidden = self.contract[
            "forbidden_tracked_surfaces"
        ]
        self.assertEqual(
            forbidden["result"],
            "BLOCK_HEAD",
        )
        for prefix in (
            "generated/",
            "views/",
            ".obsidian/",
            "__pycache__/",
            "node_modules/",
        ):
            with self.subTest(prefix=prefix):
                self.assertIn(
                    prefix,
                    forbidden["prefixes"],
                )
        self.assertIn(
            ".pyc",
            forbidden["suffixes"],
        )

    def test_sensitive_path_never_projects(self) -> None:
        policy = self.contract[
            "sensitive_path_policy"
        ]
        self.assertEqual(
            policy["result"],
            "BLOCK_HEAD_NO_PROJECTION",
        )
        self.assertTrue(
            policy[
                "plaintext_sensitive_path_in_live_projection_forbidden"
            ]
        )
        self.assertEqual(
            policy["operational_recording"],
            "COUNT_PLUS_SHA256_OF_PATH_ONLY",
        )

    def test_full_text_size_limit_is_one_mib(self) -> None:
        full = self.contract[
            "content_modes"
        ]["FULL_TEXT"]
        self.assertEqual(
            full["max_blob_size_bytes"],
            1048576,
        )

    def test_full_text_requires_utf8_no_nul_and_secret_scan(
        self,
    ) -> None:
        req = set(
            self.contract[
                "content_modes"
            ]["FULL_TEXT"]["byte_requirements"]
        )
        self.assertEqual(
            req,
            {
                "VALID_UTF8",
                "NO_NUL_BYTE",
                "SECRET_SCAN_PASS",
            },
        )

    def test_full_text_body_copy_is_forbidden(self) -> None:
        full = self.contract[
            "content_modes"
        ]["FULL_TEXT"]
        self.assertTrue(
            full[
                "source_body_copy_to_inventory_forbidden"
            ]
        )
        self.assertTrue(
            full[
                "downstream_semantic_read_allowed"
            ]
        )

    def test_metadata_only_never_exposes_body(self) -> None:
        meta = self.contract[
            "content_modes"
        ]["METADATA_ONLY"]
        self.assertFalse(
            meta[
                "source_bytes_may_be_copied_to_projection"
            ]
        )
        self.assertFalse(
            meta[
                "downstream_semantic_body_read_allowed"
            ]
        )
        self.assertEqual(
            meta["default_semantic_status"],
            "UNKNOWN_UNLESS_SEPARATE_PARSER_IS_QUALIFIED",
        )

    def test_large_blob_becomes_metadata_only(self) -> None:
        triggers = self.contract[
            "content_modes"
        ]["METADATA_ONLY"]["triggers"]
        self.assertIn(
            "BLOB_SIZE_GT_1_MIB",
            triggers,
        )

    def test_secret_scanner_is_fail_closed(self) -> None:
        scan = self.contract["secret_scan"]
        self.assertTrue(
            scan["scanner_version_must_be_pinned"]
        )
        self.assertEqual(
            scan["unavailable_scanner_result"],
            "BLOCK_HEAD",
        )
        self.assertEqual(
            scan[
                "high_confidence_secret_match_result"
            ],
            "BLOCK_HEAD_NO_PROJECTION",
        )
        self.assertTrue(
            scan["secret_value_must_never_be_logged"]
        )
        self.assertTrue(
            scan["secret_value_must_never_enter_inventory"]
        )

    def test_inventory_entry_fields_are_exact(self) -> None:
        fields = self.contract[
            "inventory_record"
        ]["entry_fields"]
        self.assertEqual(
            fields,
            [
                "source_path",
                "source_blob_sha",
                "source_blob_size",
                "git_mode",
                "selection_zone",
                "content_mode",
            ],
        )

    def test_inventory_forbids_volatile_host_fields(
        self,
    ) -> None:
        record = self.contract[
            "inventory_record"
        ]
        self.assertTrue(record["timestamps_forbidden"])
        self.assertTrue(record["hostname_forbidden"])
        self.assertTrue(record["username_forbidden"])
        self.assertTrue(
            record["absolute_paths_forbidden"]
        )

    def test_inventory_digest_is_host_deterministic(
        self,
    ) -> None:
        digest = self.contract["digest"]
        self.assertEqual(
            digest["algorithm"],
            "SHA256",
        )
        self.assertTrue(
            digest[
                "deterministic_across_hosts_required"
            ]
        )
        self.assertFalse(
            digest[
                "include_source_commit_in_entry_digest"
            ]
        )
        self.assertTrue(
            digest[
                "source_commit_bound_at_inventory_top_level"
            ]
        )

    def test_exact_head_binding_is_complete(self) -> None:
        binding = self.contract[
            "exact_head_binding"
        ]
        for key in (
            "repository_must_match",
            "branch_must_match",
            "commit_must_match_observed_remote_head",
            "tree_oid_must_match_commit_tree",
            "every_entry_blob_oid_must_match_tree",
            "every_entry_size_must_match_git_tree",
            "raw_blob_length_verification_required_for_full_text",
        ):
            with self.subTest(key=key):
                self.assertTrue(binding[key])

    def test_delta_semantics_do_not_create_semantic_rename(
        self,
    ) -> None:
        delta = self.contract["delta_semantics"]
        self.assertEqual(delta["added_path"], "ADDED")
        self.assertEqual(delta["removed_path"], "REMOVED")
        self.assertEqual(
            delta["same_path_new_blob"],
            "MODIFIED",
        )
        self.assertEqual(
            delta["same_path_same_blob"],
            "UNCHANGED",
        )
        self.assertEqual(
            delta[
                "rename_inference_from_same_blob"
            ],
            "INFORMATIONAL_ONLY_NOT_SEMANTIC",
        )

    def test_reference_census_is_non_normative(
        self,
    ) -> None:
        census = self.contract[
            "observed_reference_census"
        ]
        self.assertTrue(census["non_normative"])
        self.assertEqual(
            census["tracked_regular_blob_count"],
            908,
        )
        self.assertEqual(
            census["full_text_candidate_count_under_contract"],
            890,
        )
        self.assertEqual(
            census["metadata_only_count_under_contract"],
            18,
        )
        self.assertEqual(
            census["sensitive_path_match_count"],
            0,
        )

    def test_reference_census_zone_sum_is_908(
        self,
    ) -> None:
        census = self.contract[
            "observed_reference_census"
        ]
        self.assertEqual(
            sum(census["zone_counts"].values()),
            census["tracked_regular_blob_count"],
        )

    def test_largest_blob_is_metadata_only(self) -> None:
        largest = self.contract[
            "observed_reference_census"
        ]["largest_blob"]
        self.assertGreater(
            largest["source_blob_size"],
            1048576,
        )
        self.assertEqual(
            largest["expected_content_mode"],
            "METADATA_ONLY",
        )

    def test_p5b_itself_authorizes_no_runtime(
        self,
    ) -> None:
        boundary = self.contract["p5b_boundary"]
        self.assertTrue(
            boundary[
                "contract_tests_and_census_only"
            ]
        )
        for key in (
            "dynamic_inventory_runtime_implementation_authorized",
            "continuous_observer_authorized",
            "vault_write_authorized",
            "projection_rebuild_authorized",
            "semantic_classifier_change_authorized",
            "existing_pilot_inventory_mutation_authorized",
        ):
            with self.subTest(key=key):
                self.assertFalse(boundary[key])

    def test_breakers_are_broad_and_unique(self) -> None:
        breakers = self.contract[
            "required_breakers"
        ]
        self.assertGreaterEqual(len(breakers), 40)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gate_is_dynamic_inventory_implementation(
        self,
    ) -> None:
        self.assertEqual(
            self.contract["next_gate"],
            "P5B2_DYNAMIC_INVENTORY_IMPLEMENTATION_CANDIDATE",
        )


if __name__ == "__main__":
    unittest.main()
