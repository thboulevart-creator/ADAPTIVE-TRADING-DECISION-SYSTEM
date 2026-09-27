from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D3CCandidateGenerationStagingContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_CANDIDATE_GENERATION_STAGING_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_repository_and_branch_are_exact(self) -> None:
        self.assertEqual(
            self.contract["source_repository"],
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )
        self.assertEqual(
            self.contract["monitored_branch"],
            "integration/system-v1",
        )

    def test_p5d3b_predecessor_is_pinned(self) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5d3b_qualification_commit"],
            "51dfa30a9fcca4f012f80410f24f95007d2cf2e6",
        )
        self.assertEqual(
            p["p5d3b_qualification_report_blob"],
            "94fbe40ffde900040c9a784b205c37e76b7ef834",
        )
        self.assertEqual(
            p["p5d3b_bridge_contract_blob"],
            "7015db1206cd40b703795d12519707a6455b4fc3",
        )

    def test_p5c2_reuse_is_property_not_fixture(self) -> None:
        p = self.contract["p5c2_reuse_boundary"]
        self.assertEqual(
            p["qualified_property_reused"],
            "IMMUTABLE_COMPLETE_GENERATION_BEFORE_ATOMIC_POINTER_PUBLICATION",
        )
        self.assertFalse(
            p["build_generation_fixture_reuse_as_real_packager"]
        )
        self.assertFalse(
            p["validate_generation_dir_fixture_reuse_as_real_candidate_verifier"]
        )
        self.assertFalse(
            p["synthetic_generation_id_embedded_in_each_payload_file_required"]
        )
        self.assertFalse(
            p["synthetic_fixed_128_file_fixture_required"]
        )
        self.assertTrue(
            p["pointer_creation_during_p5d3c_forbidden"]
        )

    def test_objective_separates_seal_and_promotion(self) -> None:
        objective = self.contract["objective"]
        self.assertTrue(
            objective["package_must_be_complete_before_seal"]
        )
        self.assertTrue(objective["seal_created_last"])
        self.assertTrue(
            objective["sealed_package_is_logically_immutable"]
        )
        self.assertTrue(objective["verification_is_read_only"])
        self.assertTrue(objective["publication_forbidden"])
        self.assertTrue(objective["promotion_forbidden"])
        self.assertTrue(
            objective["current_pointer_mutation_forbidden"]
        )

    def test_input_requires_exact_candidate_identity(self) -> None:
        i = self.contract["input_contract"]
        required = set(i["required_identity_fields"])
        for field in (
            "repository",
            "branch",
            "candidate_head",
            "candidate_tree",
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "projection_contract_version",
            "projection_tree_digest_sha256",
            "generated_file_count",
            "breaker_status",
            "determinism_status",
            "breaker_manifest_digest_sha256",
            "breaker_result_digest_sha256",
            "determinism_evidence_digest_sha256",
        ):
            with self.subTest(field=field):
                self.assertIn(field, required)

        self.assertEqual(
            i["candidate_breaker_status_must_equal"],
            "PASS",
        )
        self.assertEqual(
            i["deterministic_double_build_status_must_equal"],
            "PASS",
        )
        self.assertTrue(
            i["projection_a_and_b_must_be_byte_identical"]
        )

    def test_staging_is_fresh_isolated_and_no_alias(self) -> None:
        s = self.contract["staging_boundary"]
        for field in (
            "fresh_empty_root_required",
            "root_outside_canonical_worktree",
            "root_outside_real_vault",
            "root_outside_any_live_generation_directory",
            "root_must_not_be_git_repository",
            "root_must_not_contain_symlink_junction_or_reparse_escape",
            "hard_linked_payload_files_forbidden",
            "payload_files_must_be_regular_single_link_files",
            "preexisting_target_forbidden",
            "overwrite_in_place_forbidden",
            "canonical_worktree_mutation_forbidden",
            "source_checkout_mutation_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(s[field])

    def test_package_layout_has_no_current_pointer(self) -> None:
        layout = self.contract["package_layout"]
        self.assertEqual(
            layout["payload_root"],
            "generated",
        )
        self.assertEqual(
            layout["machine_manifest_root"],
            "_atds_generation",
        )
        self.assertEqual(
            layout["payload_manifest_path"],
            "_atds_generation/payload-manifest.json",
        )
        self.assertEqual(
            layout["generation_manifest_path"],
            "_atds_generation/generation-manifest.json",
        )
        self.assertEqual(
            layout["seal_path"],
            "_atds_generation/SEAL.json",
        )
        for forbidden in (
            "CURRENT",
            "CURRENT.md",
            "CURRENT.json",
            "CURRENT.tmp",
            "views",
            ".obsidian",
            ".git",
        ):
            self.assertIn(
                forbidden,
                layout["forbidden_paths"],
            )

    def test_payload_is_exact_copy_of_verified_generated_tree(
        self,
    ) -> None:
        p = self.contract["payload_contract"]
        self.assertTrue(p["payload_is_exact_generated_tree_copy"])
        self.assertTrue(p["payload_relative_paths_preserved_exactly"])
        self.assertTrue(p["payload_bytes_preserved_exactly"])
        self.assertTrue(
            p["payload_file_count_must_equal_input_generated_file_count"]
        )
        self.assertTrue(p["payload_must_include_all_generated_files"])
        self.assertTrue(
            p["payload_may_not_include_source_repository_files"]
        )
        self.assertTrue(p["payload_may_not_include_raw_source_blobs"])
        self.assertTrue(p["duplicate_path_forbidden"])

    def test_payload_manifest_is_self_excluding_and_complete(
        self,
    ) -> None:
        m = self.contract["payload_manifest"]
        self.assertEqual(
            m["schema"],
            "ATDS_OBSIDIAN_CANDIDATE_PAYLOAD_MANIFEST_V0_1",
        )
        self.assertTrue(m["includes_all_payload_files"])
        self.assertTrue(m["excludes_machine_manifest_files"])
        self.assertTrue(m["excludes_itself"])
        self.assertEqual(
            m["file_entry_fields"],
            ["relative_path", "size_bytes", "sha256"],
        )

    def test_generation_identity_binds_all_scientific_inputs(
        self,
    ) -> None:
        g = self.contract["generation_identity"]
        required = set(g["identity_basis_required_fields"])
        for field in (
            "candidate_head",
            "candidate_tree",
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "projection_contract_version",
            "projection_tree_digest_sha256",
            "payload_file_map_digest_sha256",
            "payload_manifest_digest_sha256",
            "breaker_status",
            "determinism_status",
            "breaker_manifest_digest_sha256",
            "breaker_result_digest_sha256",
            "determinism_evidence_digest_sha256",
            "staging_contract_blob",
        ):
            with self.subTest(field=field):
                self.assertIn(field, required)

    def test_generation_id_is_deterministic_digest_based(
        self,
    ) -> None:
        g = self.contract["generation_identity"]
        self.assertEqual(
            g["generation_id"],
            "gen-<generation_identity_digest_sha256>",
        )
        for field in (
            "wall_clock_in_generation_id_forbidden",
            "uuid_in_generation_id_forbidden",
            "randomness_in_generation_id_forbidden",
            "host_identity_in_generation_id_forbidden",
            "absolute_path_in_generation_id_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(g[field])

    def test_generation_manifest_binds_pass_statuses(
        self,
    ) -> None:
        m = self.contract["generation_manifest"]
        self.assertEqual(
            m["breaker_status_required"],
            "PASS",
        )
        self.assertEqual(
            m["determinism_status_required"],
            "PASS",
        )
        self.assertIn(
            "breaker_status",
            m["required_fields"],
        )
        self.assertIn(
            "determinism_status",
            m["required_fields"],
        )
        self.assertEqual(
            m["package_status_before_seal"],
            "COMPLETE_PENDING_SEAL",
        )

    def test_generation_manifest_forbids_volatile_fields(
        self,
    ) -> None:
        forbidden = set(
            self.contract["generation_manifest"][
                "volatile_fields_forbidden"
            ]
        )
        for field in (
            "generated_at",
            "timestamp",
            "host",
            "user",
            "pid",
            "absolute_stage_path",
            "absolute_repo_path",
        ):
            self.assertIn(field, forbidden)

    def test_seal_is_last_exclusive_and_unpromoted(
        self,
    ) -> None:
        s = self.contract["seal_contract"]
        self.assertTrue(s["created_last"])
        self.assertTrue(s["exclusive_create_required"])
        self.assertEqual(
            s["seal_status"],
            "SEALED_UNPROMOTED",
        )
        self.assertTrue(
            s["seal_may_not_reference_current_pointer"]
        )
        self.assertTrue(
            s["seal_may_not_grant_promotion_authority"]
        )
        self.assertTrue(
            s["seal_may_not_claim_live_visibility"]
        )

    def test_seal_binds_candidate_and_manifests(self) -> None:
        fields = set(
            self.contract["seal_contract"]["required_fields"]
        )
        for field in (
            "generation_id",
            "generation_identity_digest_sha256",
            "payload_manifest_digest_sha256",
            "generation_manifest_digest_sha256",
            "payload_file_map_digest_sha256",
            "projection_tree_digest_sha256",
            "candidate_head",
            "candidate_tree",
            "staging_contract_blob",
            "seal_status",
        ):
            self.assertIn(field, fields)

    def test_sealing_sequence_orders_seal_last(self) -> None:
        seq = self.contract["sealing_sequence"]
        self.assertEqual(
            seq[-3:],
            [
                "WRITE_SEAL_EXCLUSIVELY_AS_FINAL_MUTATION",
                "VERIFY_SEALED_PACKAGE_READ_ONLY",
                "EMIT_CANDIDATE_GENERATION_DESCRIPTOR",
            ],
        )
        self.assertLess(
            seq.index("VERIFY_EVERY_PAYLOAD_FILE"),
            seq.index("WRITE_SEAL_EXCLUSIVELY_AS_FINAL_MUTATION"),
        )
        self.assertLess(
            seq.index("WRITE_GENERATION_MANIFEST_EXCLUSIVELY"),
            seq.index("WRITE_SEAL_EXCLUSIVELY_AS_FINAL_MUTATION"),
        )

    def test_post_seal_semantics_are_fail_closed(
        self,
    ) -> None:
        p = self.contract["post_seal_semantics"]
        self.assertTrue(
            p["logical_immutability_begins_when_valid_seal_exists"]
        )
        self.assertFalse(
            p["os_level_immutable_attribute_claimed"]
        )
        for field in (
            "any_payload_mutation_invalidates_package",
            "any_manifest_mutation_invalidates_package",
            "any_file_deletion_invalidates_package",
            "any_unmanifested_extra_file_invalidates_package",
            "seal_rewrite_forbidden",
            "seal_deletion_invalidates_package",
            "reseal_in_place_forbidden",
            "repair_in_place_forbidden",
            "failed_package_requires_new_fresh_root",
        ):
            with self.subTest(field=field):
                self.assertTrue(p[field])

    def test_verification_is_read_only_and_exhaustive(
        self,
    ) -> None:
        v = self.contract["verification_contract"]
        self.assertTrue(v["read_only"])
        self.assertTrue(
            v["verification_may_not_modify_package"]
        )
        checks = set(v["required_checks"])
        for check in (
            "EXACT_ALLOWED_FILE_SET",
            "BREAKER_STATUS_IS_PASS",
            "DETERMINISM_STATUS_IS_PASS",
            "PAYLOAD_FILE_COUNT_MATCH",
            "EVERY_PAYLOAD_FILE_SIZE_MATCH",
            "EVERY_PAYLOAD_FILE_SHA256_MATCH",
            "PAYLOAD_FILE_MAP_DIGEST_MATCH",
            "PAYLOAD_MANIFEST_DIGEST_MATCH",
            "GENERATION_MANIFEST_DIGEST_MATCH",
            "NO_EXTRA_FILES",
        ):
            self.assertIn(check, checks)

    def test_descriptor_cannot_grant_promotion(self) -> None:
        d = self.contract["candidate_generation_descriptor"]
        self.assertEqual(
            d["verification_status_required"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            d["promotion_authorized_must_be_false"]
        )
        self.assertTrue(d["absolute_stage_path_forbidden"])
        self.assertTrue(d["volatile_host_data_forbidden"])

    def test_existing_integrity_primitives_are_reused_narrowly(
        self,
    ) -> None:
        r = self.contract[
            "relationship_to_existing_integrity_primitives"
        ]
        for field in (
            "sha256_bytes_may_be_reused",
            "file_digest_semantics_may_be_reused",
            "digest_entries_semantics_may_be_reused",
            "regular_single_link_checks_may_be_reused",
            "reparse_symlink_junction_checks_may_be_reused",
            "legacy_projection_tree_digest_semantics_may_be_bound_as_upstream_evidence",
        ):
            self.assertTrue(r[field])
        self.assertTrue(
            r[
                "legacy_builder_manifest_field_names_may_not_define_new_candidate_generation_identity"
            ]
        )
        self.assertTrue(
            r[
                "legacy_pilot_inventory_digest_name_may_not_replace_dynamic_inventory_digest"
            ]
        )

    def test_failure_classes_keep_candidate_and_infra_separate(
        self,
    ) -> None:
        f = self.contract["failure_classification"]
        self.assertTrue(
            f["candidate_failure_must_not_be_relabelled_blocked"]
        )
        self.assertTrue(
            f[
                "infrastructure_block_must_not_be_relabelled_candidate_failure_without_candidate_evidence"
            ]
        )
        self.assertGreaterEqual(
            len(f["candidate_evidence_failures"]),
            6,
        )
        self.assertGreaterEqual(
            len(f["infrastructure_blocked_examples"]),
            4,
        )

    def test_promotion_boundary_is_explicit(self) -> None:
        p = self.contract["promotion_boundary"]
        self.assertTrue(p["package_is_not_live"])
        self.assertTrue(p["package_is_not_current"])
        self.assertTrue(p["sealed_does_not_mean_promoted"])
        self.assertTrue(
            p["sealed_does_not_mean_obsidian_visible"]
        )
        self.assertTrue(p["current_pointer_absent"])
        self.assertTrue(p["pointer_write_forbidden"])
        self.assertTrue(
            p["promotion_primitive_invocation_forbidden"]
        )
        self.assertTrue(p["real_vault_write_forbidden"])
        self.assertFalse(
            p["production_promotion_authorized"]
        )

    def test_p5d3c_authorizes_no_runtime(self) -> None:
        b = self.contract["p5d3c_boundary"]
        self.assertTrue(b["contract_and_breakers_only"])
        for field in (
            "staging_packager_implementation_authorized",
            "staging_verifier_implementation_authorized",
            "staging_execution_authorized",
            "current_head_builder_adaptation_authorized",
            "relation_adapter_execution_authorized",
            "evaluation_orchestrator_authorized",
            "production_promotion_authorized",
            "current_pointer_mutation_authorized",
            "real_vault_write_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(b[field])

    def test_breaker_registry_is_large_and_unique(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 100)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gates_include_implementation_before_orchestrator(
        self,
    ) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            list(gates.keys()),
            [
                "p5d3c2",
                "p5d3d",
                "p5d3e",
                "p5d4",
                "p5e",
                "p6",
            ],
        )
        self.assertEqual(
            gates["p5d3c2"],
            "CANDIDATE_GENERATION_STAGING_IMPLEMENTATION_AND_SANDBOX_QUALIFICATION",
        )


if __name__ == "__main__":
    unittest.main()
