from __future__ import annotations

import json
import unittest
from pathlib import Path


class P5D3C2StagingImplementationContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging_implementation_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_and_status_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3C2_STAGING_IMPLEMENTATION_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_p5d3c_predecessor_is_exact(self) -> None:
        p = self.contract["qualified_predecessor"]
        self.assertEqual(
            p["p5d3c_qualification_commit"],
            "437ab790f2a1fa4b490344d28cb7b7a2e8116db3",
        )
        self.assertEqual(
            p["p5d3c_qualification_report_blob"],
            "7390a01e9f7af1bdf9d2f5c5251765ce68faf533",
        )
        self.assertEqual(
            p["p5d3c_staging_contract_blob"],
            "79c6a3380a1dcefc49aa4619259baaa8eeadb535",
        )

    def test_objective_is_real_packager_plus_read_only_verifier(
        self,
    ) -> None:
        o = self.contract["objective"]
        self.assertTrue(o["implement_real_generic_packager"])
        self.assertTrue(o["implement_read_only_verifier"])
        self.assertTrue(o["sandbox_qualification_required"])
        self.assertTrue(
            o[
                "synthetic_projection_fixture_may_be_used_only_as_packager_input"
            ]
        )
        self.assertTrue(
            o[
                "synthetic_fixture_does_not_qualify_current_head_builder"
            ]
        )
        self.assertEqual(
            o["package_success_state"],
            "PASS_SEALED_UNPROMOTED",
        )

    def test_runtime_is_temp_only_and_nonpublishing(
        self,
    ) -> None:
        r = self.contract["runtime_scope"]
        for field in (
            "package_root_must_be_below_os_temp",
            "fresh_package_root_required",
            "canonical_worktree_forbidden",
            "real_vault_forbidden",
            "live_generation_namespace_forbidden",
            "current_pointer_creation_forbidden",
            "promotion_primitive_invocation_forbidden",
            "network_io_forbidden",
            "git_mutation_forbidden",
            "background_execution_forbidden",
            "polling_forbidden",
        ):
            with self.subTest(field=field):
                self.assertTrue(r[field])

    def test_input_recomputes_projection_identity(self) -> None:
        i = self.contract["input_scope"]
        self.assertTrue(
            i["verified_projection_directory_required"]
        )
        self.assertTrue(
            i["input_projection_generated_subtree_only"]
        )
        self.assertTrue(
            i["projection_tree_digest_recomputed"]
        )
        self.assertTrue(
            i["generated_file_count_recomputed"]
        )
        self.assertTrue(
            i["breaker_status_pass_required"]
        )
        self.assertTrue(
            i["determinism_status_pass_required"]
        )

    def test_packager_orders_manifests_and_seal(self) -> None:
        p = self.contract["packager_semantics"]
        self.assertTrue(p["payload_copy_byte_exact"])
        self.assertTrue(p["payload_copy_path_exact"])
        self.assertTrue(
            p["exclusive_file_creation_required"]
        )
        self.assertTrue(
            p["payload_manifest_written_after_payload"]
        )
        self.assertTrue(
            p[
                "generation_manifest_written_after_payload_manifest"
            ]
        )
        self.assertTrue(p["seal_written_last"])
        self.assertTrue(
            p["seal_exclusive_create_required"]
        )
        self.assertTrue(
            p["post_seal_verification_required"]
        )

    def test_verifier_recomputes_all_critical_identity(
        self,
    ) -> None:
        v = self.contract["verifier_semantics"]
        self.assertTrue(v["read_only"])
        for field in (
            "canonical_manifest_bytes_required",
            "exact_manifest_field_sets_required",
            "exact_top_level_layout_required",
            "exact_file_set_required",
            "payload_file_size_and_sha256_recomputed",
            "payload_file_map_digest_recomputed",
            "generation_identity_recomputed",
            "generation_id_recomputed",
            "seal_recomputed",
            "hard_link_alias_rejected",
            "symlink_junction_reparse_rejected",
            "promotion_authorized_always_false",
        ):
            with self.subTest(field=field):
                self.assertTrue(v[field])

    def test_sandbox_requires_repeat_read_only_control(
        self,
    ) -> None:
        s = self.contract["sandbox_qualification"]
        self.assertTrue(s["control_package_required"])
        self.assertTrue(
            s["control_package_verify_twice_required"]
        )
        self.assertTrue(
            s[
                "control_package_content_digest_unchanged_across_verification"
            ]
        )
        self.assertGreaterEqual(
            s["minimum_payload_files"],
            4,
        )
        self.assertTrue(
            s["fixture_must_include_nested_paths"]
        )
        self.assertTrue(
            s["fixture_must_not_use_p5c2_build_generation"]
        )

    def test_required_runtime_mutations_are_exact(self) -> None:
        self.assertEqual(
            self.contract["sandbox_qualification"][
                "required_mutation_breakers"
            ],
            [
                "PAYLOAD_BYTE_MUTATION",
                "PAYLOAD_FILE_DELETION",
                "UNMANIFESTED_EXTRA_FILE",
                "PAYLOAD_MANIFEST_MUTATION",
                "GENERATION_MANIFEST_MUTATION",
                "SEAL_MUTATION",
                "HARD_LINK_ALIAS",
            ],
        )

    def test_reparse_probe_has_explicit_capability_policy(
        self,
    ) -> None:
        p = self.contract["sandbox_qualification"][
            "reparse_symlink_runtime_probe"
        ]
        self.assertTrue(p["attempt_required"])
        self.assertTrue(
            p["pass_if_verifier_rejects_created_link"]
        )
        self.assertTrue(
            p["capability_unavailable_may_be_reported"]
        )
        self.assertTrue(
            p[
                "capability_unavailable_does_not_waive_static_and_synthetic_breakers"
            ]
        )

    def test_report_is_path_and_host_free(self) -> None:
        r = self.contract["qualification_report"]
        self.assertEqual(
            r["schema"],
            "ATDS_OBSIDIAN_P5D3C2_SANDBOX_REPORT_V0_1",
        )
        self.assertEqual(
            r["success_status"],
            "PASS_SANDBOX_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            r["absolute_sandbox_path_forbidden"]
        )
        self.assertTrue(r["host_identity_forbidden"])

    def test_failure_semantics_are_distinct(self) -> None:
        f = self.contract["failure_semantics"]
        self.assertEqual(
            f["package_contract_violation"],
            "FAIL_INVALID_CANDIDATE_GENERATION",
        )
        self.assertEqual(
            f["sandbox_infrastructure_unavailable"],
            "BLOCKED_SANDBOX_INFRASTRUCTURE",
        )
        self.assertEqual(
            f["mutation_breaker_not_rejected"],
            "FAIL_BREAKER_SURVIVED",
        )
        self.assertTrue(f["partial_success_forbidden"])

    def test_p5d3c2_authorizes_only_staging_runtime(self) -> None:
        b = self.contract["p5d3c2_boundary"]
        self.assertTrue(
            b["packager_implementation_authorized"]
        )
        self.assertTrue(
            b["read_only_verifier_implementation_authorized"]
        )
        self.assertTrue(
            b["sacrificial_sandbox_execution_authorized"]
        )
        for field in (
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

    def test_breaker_registry_is_broad_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 70)
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )

    def test_next_gate_is_orchestrator_not_promotion(
        self,
    ) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            list(gates.keys()),
            [
                "p5d3d",
                "p5d3e",
                "p5d4",
                "p5e",
                "p6",
            ],
        )
        self.assertEqual(
            gates["p5d3d"],
            "FINITE_CANDIDATE_EVALUATION_ORCHESTRATOR_WITH_CURRENT_HEAD_BUILDER_ADAPTATION",
        )


if __name__ == "__main__":
    unittest.main()
