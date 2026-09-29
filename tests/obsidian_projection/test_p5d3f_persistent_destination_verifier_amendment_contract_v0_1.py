from __future__ import annotations

import json
import unittest
from pathlib import Path


CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "persistent_destination_verifier_amendment_contract_v0_1.json"
)
EXPECTED_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3F_PERSISTENT_DESTINATION_VERIFIER_AMENDMENT_CONTRACT_V0_1"
)


class P5D3FPersistentDestinationVerifierAmendmentContractV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[2]
        cls.contract = json.loads(
            (root / CONTRACT_RELATIVE).read_text(
                encoding="utf-8"
            )
        )

    def test_schema_and_frontier_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            EXPECTED_SCHEMA,
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D3F-PERSISTENT-DESTINATION-VERIFIER-AMENDMENT",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_incident_basis_is_exact(self) -> None:
        incident = self.contract["incident_basis"]
        self.assertEqual(
            incident["observed_error"],
            "PromotionHandoffGovernanceError: destination package verification failed",
        )
        self.assertIn(
            "tempfile.gettempdir()",
            incident["underlying_static_cause"],
        )
        self.assertEqual(
            incident["incident_report"],
            "reports/program/2026-09-29-OBSIDIAN-P5D3F-RECOVERY-V0.4-DESTINATION-PACKAGE-VERIFICATION-INCIDENT-V1.md",
        )

    def test_authority_blobs_are_pinned(self) -> None:
        pins = self.contract["pinned_authorities"]
        self.assertEqual(
            pins["candidate_generation_staging_blob"],
            "e2e5867536f4f9c7dec475c6696737249536ff39",
        )
        self.assertEqual(
            pins["qualified_p5d3f_runtime_blob"],
            "2108131914cf65bb076b80f5bb63cd63267567fa",
        )
        self.assertEqual(
            pins["qualified_persistent_handoff_blob"],
            "dcd70a9d9794675eab90e41df560f8b030b5dbf3",
        )
        self.assertEqual(
            pins["persistent_gate_contract_v0_1_blob"],
            "59ce9e079d256799d072405fa4a623ba58b75c0d",
        )
        self.assertEqual(
            pins["persistent_recovery_contract_v0_2_blob"],
            "aef627936b6f745017bcace7e8a3e44270f95674",
        )

    def test_historical_temp_verifier_must_remain_closed(self) -> None:
        history = self.contract["historical_preservation"]
        self.assertEqual(
            history["existing_verify_candidate_generation_name"],
            "verify_candidate_generation",
        )
        self.assertIs(
            history["existing_temp_only_policy_must_remain"],
            True,
        )
        self.assertIs(
            history["existing_temp_only_behavior_may_not_be_broadened"],
            True,
        )
        self.assertIs(
            history["historical_tests_may_not_be_weakened_or_rewritten_to_accept_persistent_roots"],
            True,
        )

    def test_new_surface_is_explicit_and_read_only(self) -> None:
        surface = self.contract["required_new_surface"]
        self.assertEqual(
            surface["verifier_name"],
            "verify_persistent_candidate_generation",
        )
        self.assertIs(
            surface["explicit_authorized_staging_root_argument_required"],
            True,
        )
        self.assertIs(
            surface["forbidden_roots_argument_required"],
            True,
        )
        self.assertIs(
            surface["verifier_is_read_only"],
            True,
        )
        self.assertIs(
            surface["verifier_may_not_create_or_delete_paths"],
            True,
        )

    def test_exact_persistent_location_is_narrow(self) -> None:
        policy = self.contract[
            "exact_persistent_location_policy"
        ]
        self.assertEqual(
            policy["production_staging_root"],
            r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING",
        )
        self.assertEqual(
            policy["protected_real_vault_root"],
            r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION",
        )
        self.assertEqual(
            policy["required_wrapper_shape"],
            "<staging>/packages/<generation_id>/package",
        )
        for key in (
            "package_must_be_descendant_of_explicit_authorized_staging_root",
            "package_may_not_be_below_real_vault",
            "package_may_not_intersect_real_vault",
            "package_may_not_intersect_candidate_repo",
            "package_may_not_intersect_evaluation_workspace",
            "package_may_not_be_symlink_junction_or_reparse",
            "staging_chain_may_not_contain_symlink_junction_or_reparse",
            "arbitrary_non_temp_root_must_block",
            "arbitrary_persistent_root_must_block",
        ):
            self.assertIs(
                policy[key],
                True,
                key,
            )

    def test_shared_integrity_semantics_are_not_weakened(self) -> None:
        shared = self.contract[
            "shared_verification_semantics"
        ]
        self.assertIs(
            shared["same_semantic_verification_core_required"],
            True,
        )
        self.assertIs(
            shared["content_checks_may_not_be_duplicated_with_divergent_logic"],
            True,
        )
        self.assertEqual(
            shared["package_status_required"],
            "PASS_SEALED_UNPROMOTED",
        )
        for key in (
            "top_level_package_layout_exact",
            "canonical_payload_manifest_required",
            "canonical_generation_manifest_required",
            "canonical_seal_required",
            "payload_exact_file_set_required",
            "payload_file_sizes_required",
            "payload_sha256_required",
            "payload_file_map_digest_required",
            "projection_tree_digest_required",
            "generation_identity_digest_required",
            "generation_id_required",
            "seal_binding_required",
            "seal_byte_binding_required",
            "hard_links_forbidden",
            "symlinks_forbidden",
            "junctions_forbidden",
            "reparse_points_forbidden",
            "non_regular_files_forbidden",
        ):
            self.assertIs(
                shared[key],
                True,
                key,
            )

    def test_p5d3f_source_and_destination_roles_are_distinct(self) -> None:
        integration = self.contract[
            "p5d3f_integration_requirement"
        ]
        self.assertIs(
            integration[
                "source_package_must_continue_using_temp_only_verifier"
            ],
            True,
        )
        self.assertIs(
            integration[
                "destination_package_must_use_persistent_verifier"
            ],
            True,
        )
        self.assertIs(
            integration[
                "source_and_destination_descriptors_must_match"
            ],
            True,
        )
        self.assertIs(
            integration[
                "source_and_destination_byte_tree_digest_must_match"
            ],
            True,
        )
        self.assertIs(
            integration[
                "destination_verification_must_occur_before_PROMOTION_HANDOFF_write"
            ],
            True,
        )

    def test_adversarial_families_are_preregistered(self) -> None:
        required = set(
            self.contract["required_adversarial_tests"]
        )
        expected = {
            "HISTORICAL_TEMP_VERIFIER_STILL_REJECTS_NON_TEMP_ROOT",
            "PERSISTENT_VERIFIER_REJECTS_ARBITRARY_NON_TEMP_ROOT",
            "PERSISTENT_VERIFIER_REJECTS_WRONG_STAGING_ROOT",
            "PERSISTENT_VERIFIER_REJECTS_REAL_VAULT_INTERSECTION",
            "PERSISTENT_VERIFIER_REJECTS_ALIAS_REPARSE_CHAIN",
            "PERSISTENT_VERIFIER_REJECTS_HARDLINK",
            "PERSISTENT_VERIFIER_REJECTS_TAMPERED_PAYLOAD",
            "PERSISTENT_VERIFIER_REJECTS_TAMPERED_MANIFEST",
            "PERSISTENT_VERIFIER_REJECTS_TAMPERED_SEAL",
            "PERSISTENT_VERIFIER_REJECTS_WRONG_WRAPPER_LAYOUT",
            "PERSISTENT_VERIFIER_ACCEPTS_EXACT_AUTHORIZED_PERSISTENT_PACKAGE_EQUIVALENT",
            "TEMP_AND_PERSISTENT_VERIFIERS_RETURN_IDENTICAL_DESCRIPTOR_FOR_IDENTICAL_VALID_PACKAGE",
            "P5D3F_DESTINATION_CALL_USES_PERSISTENT_VERIFIER_ONLY",
            "NO_REAL_VAULT_WRITE_AUTHORITY_ADDED",
        }
        self.assertEqual(
            required,
            expected,
        )

    def test_red_boundary_and_stop_are_exact(self) -> None:
        red = self.contract["red_phase"]
        self.assertIs(
            red["implementation_must_be_absent_at_contract_adoption"],
            True,
        )
        self.assertIs(
            red["red_tests_must_fail_before_implementation"],
            True,
        )
        self.assertIs(
            red["implementation_not_authorized_by_contract_adoption"],
            True,
        )

        boundary = self.contract["boundary"]
        self.assertIs(
            boundary["contract_tests_only"],
            True,
        )
        self.assertIs(
            boundary["red_tests_authorized"],
            True,
        )

        for key in (
            "implementation_authorized",
            "persistent_staging_real_access_authorized",
            "real_vault_read_authorized",
            "real_vault_write_authorized",
            "persistent_handoff_real_execution_authorized",
            "live_publication_authorized",
            "current_pointer_mutation_authorized",
            "promotion_confirmed_authorized",
            "stage_a_authorized",
            "stage_b_authorized",
            "p5d4_authorized",
            "p6_authorized",
        ):
            self.assertIs(
                boundary[key],
                False,
                key,
            )

        self.assertEqual(
            self.contract["next_gate"]["after_contract_and_red"],
            "P5-D3F-PERSISTENT-DESTINATION-VERIFIER-AMENDMENT-MINIMAL-IMPLEMENTATION-V0.1",
        )
        self.assertIs(
            self.contract["next_gate"]["mandatory_stop_after_red"],
            True,
        )


if __name__ == "__main__":
    unittest.main()
