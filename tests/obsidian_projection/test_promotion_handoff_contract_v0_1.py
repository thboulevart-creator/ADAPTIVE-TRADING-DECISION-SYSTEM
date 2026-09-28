from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "obsidian_projection"
    / "promotion_handoff_contract_v0_1.json"
)

EXPECTED_CONTRACT_BLOB = (
    "349d180478af0efd56ea1a4eb0b21d119833c1dc"
)


def _git_blob_oid(raw: bytes) -> str:
    return hashlib.sha1(
        f"blob {len(raw)}\0".encode("ascii") + raw
    ).hexdigest()


class PromotionHandoffContractV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CONTRACT_PATH.read_bytes()
        cls.contract = json.loads(
            cls.raw.decode("utf-8")
        )

    def test_contract_blob_and_schema_are_exact(self) -> None:
        self.assertEqual(
            _git_blob_oid(self.raw),
            EXPECTED_CONTRACT_BLOB,
        )
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3F_PROMOTION_HANDOFF_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D3F",
        )

    def test_architecture_preserves_p5d4_name(self) -> None:
        architecture = self.contract[
            "architecture_decision"
        ]
        self.assertTrue(
            architecture[
                "p5d3e_package_is_ephemeral"
            ]
        )
        self.assertTrue(
            architecture[
                "finite_handoff_required_before_live_publication"
            ]
        )
        self.assertTrue(
            architecture[
                "p5d4_remains_bounded_observer_loop_candidate"
            ]
        )
        self.assertEqual(
            self.contract["next_gates"]["p5d4"],
            "BOUNDED_OBSERVER_LOOP_CANDIDATE",
        )

    def test_p5c2_authority_is_exact_and_bounded(self) -> None:
        authority = self.contract[
            "qualified_authorities"
        ]["p5c2"]
        self.assertEqual(
            authority["promotion_contract_blob"],
            "36e49e72a867e30a69f63eb413fd924d0e56297b",
        )
        self.assertEqual(
            authority["qualification_report_blob"],
            "a928598182b25d110c9040c62d846bf9018ac3ed",
        )
        self.assertEqual(
            authority["selected_primitive"],
            "IMMUTABLE_GENERATION_ATOMIC_POINTER",
        )
        self.assertFalse(
            authority["production_promotion_authorized"]
        )

    def test_p5c3r2_authority_is_exact_and_bounded(self) -> None:
        authority = self.contract[
            "qualified_authorities"
        ]["p5c3r2"]
        self.assertEqual(
            authority["qualified_runtime_candidate"],
            "b5f3a8de061772e15bc94b20095d419130c20781",
        )
        self.assertEqual(
            authority["qualification_report_blob"],
            "fd54a78abde8342c6da708d3a4096b4d0b267905",
        )
        self.assertEqual(
            authority["current_entrypoint"],
            "CURRENT.md",
        )
        self.assertFalse(
            authority["production_promotion_authorized"]
        )
        self.assertFalse(
            authority["continuous_observer_authorized"]
        )
        self.assertFalse(
            authority["graph_current_pointer_semantics_qualified"]
        )

    def test_p5d2_authority_keeps_physical_and_logical_promotion_separate(
        self,
    ) -> None:
        authority = self.contract[
            "qualified_authorities"
        ]["p5d2"]
        self.assertEqual(
            authority["observer_tick_blob"],
            "fd212f61ec38332b677110f40265638af55a73e2",
        )
        self.assertTrue(
            authority[
                "promotion_confirmed_is_external_logical_confirmation_only"
            ]
        )
        self.assertFalse(
            authority["physical_promotion_io_performed"]
        )

    def test_p5d3c2_package_authority_is_exact(self) -> None:
        authority = self.contract[
            "qualified_authorities"
        ]["p5d3c2"]
        self.assertEqual(
            authority["packager_verifier_blob"],
            "e2e5867536f4f9c7dec475c6696737249536ff39",
        )
        self.assertEqual(
            authority["accepted_package_status"],
            "PASS_SEALED_UNPROMOTED",
        )

    def test_p5d3e_cleanup_boundary_is_preserved(self) -> None:
        authority = self.contract[
            "qualified_authorities"
        ]["p5d3e"]
        self.assertEqual(
            authority["harness_blob"],
            "bd7f63b08432a53eaff5deeb2147396eb60d723f",
        )
        self.assertFalse(
            authority[
                "candidate_repository_retained_on_success"
            ]
        )
        self.assertFalse(
            authority[
                "evaluation_workspace_retained_on_success"
            ]
        )
        self.assertTrue(
            self.contract["architecture_decision"][
                "reopening_p5d3e_cleanup_semantics_forbidden"
            ]
        )

    def test_first_real_candidate_is_lineage_only(self) -> None:
        lineage = self.contract[
            "first_real_evidence_lineage"
        ]
        self.assertEqual(
            lineage["candidate_head"],
            "89710b879751d7fcebccf75cd03e64368f1b0e96",
        )
        self.assertEqual(
            lineage["candidate_tree"],
            "dc85bdb0708f4980e3a0cead0f15c6d077f90290",
        )
        self.assertEqual(
            lineage["role"],
            "EVIDENCE_LINEAGE_ONLY_NOT_A_HARDCODED_RUNTIME_CANDIDATE",
        )

    def test_handoff_core_is_network_free_and_exact_head_bound(
        self,
    ) -> None:
        scope = self.contract["input_scope"]
        self.assertTrue(
            scope["exact_candidate_head_required"]
        )
        self.assertTrue(
            scope["exact_candidate_tree_required"]
        )
        self.assertTrue(
            scope[
                "candidate_repo_head_must_equal_input"
            ]
        )
        self.assertTrue(
            scope[
                "candidate_repo_tree_must_equal_input"
            ]
        )
        self.assertTrue(
            scope[
                "network_resolution_must_occur_outside_handoff_core"
            ]
        )
        self.assertTrue(
            scope["handoff_core_network_io_forbidden"]
        )

    def test_evaluation_gate_requires_real_qualification_properties(
        self,
    ) -> None:
        gate = self.contract["evaluation_gate"]
        self.assertTrue(
            gate["fresh_finite_evaluation_required"]
        )
        self.assertEqual(
            gate["evaluator_outcome_required"],
            "QUALIFIED",
        )
        self.assertIsNone(
            gate["evaluator_failure_code_required"]
        )
        self.assertTrue(
            gate["projection_a_must_equal_projection_b"]
        )
        self.assertEqual(
            gate["metadata_only_body_read_count_required"],
            0,
        )
        self.assertEqual(
            gate[
                "candidate_generation_verification_status_required"
            ],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertGreaterEqual(
            len(gate["required_scientific_digests"]),
            8,
        )

    def test_staging_is_strictly_outside_live_vault(self) -> None:
        staging = self.contract[
            "staging_environment"
        ]
        self.assertTrue(
            staging["staging_must_not_equal_live_vault"]
        )
        self.assertTrue(
            staging["staging_must_not_be_inside_live_vault"]
        )
        self.assertTrue(
            staging["live_vault_must_not_be_inside_staging"]
        )
        self.assertTrue(
            staging["staging_root_alias_rejected"]
        )
        self.assertTrue(
            staging[
                "symlink_junction_reparse_in_path_chain_rejected"
            ]
        )

    def test_inner_package_remains_unchanged(self) -> None:
        layout = self.contract["handoff_layout"]
        self.assertTrue(
            layout["p5d3c2_package_subtree_exact"]
        )
        self.assertTrue(
            layout["p5d3c2_package_must_not_be_mutated"]
        )
        self.assertTrue(
            layout["handoff_record_outside_sealed_package"]
        )
        self.assertTrue(
            layout["handoff_record_written_last"]
        )
        self.assertTrue(
            layout["no_current_file_allowed"]
        )

    def test_copy_semantics_reject_aliasing(self) -> None:
        copy = self.contract["copy_semantics"]
        self.assertTrue(copy["byte_exact_copy_required"])
        self.assertTrue(copy["path_exact_copy_required"])
        self.assertTrue(copy["hard_links_forbidden"])
        self.assertTrue(copy["symlinks_forbidden"])
        self.assertTrue(copy["junctions_forbidden"])
        self.assertTrue(copy["reparse_points_forbidden"])
        self.assertTrue(
            copy["destination_files_single_link_required"]
        )

    def test_handoff_record_never_grants_publication_authority(
        self,
    ) -> None:
        record = self.contract["handoff_record"]
        self.assertFalse(
            record["publication_authorized_required"]
        )
        self.assertFalse(
            record[
                "current_pointer_mutation_authorized_required"
            ]
        )
        self.assertFalse(
            record["real_vault_write_authorized_required"]
        )
        self.assertFalse(
            record[
                "promotion_confirmed_event_authorized_required"
            ]
        )
        self.assertEqual(
            record["handoff_status_required"],
            "READY_UNAUTHORIZED",
        )

    def test_handoff_record_exact_fields_bind_scientific_identity(
        self,
    ) -> None:
        fields = set(
            self.contract["handoff_record"][
                "required_fields"
            ]
        )
        required = {
            "candidate_head",
            "candidate_tree",
            "generation_id",
            "candidate_generation_digest_sha256",
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "projection_tree_digest_sha256",
            "breaker_manifest_digest_sha256",
            "breaker_result_digest_sha256",
            "determinism_evidence_digest_sha256",
            "payload_file_map_digest_sha256",
            "package_byte_tree_digest_sha256",
            "handoff_contract_blob",
        }
        self.assertTrue(required.issubset(fields))

    def test_handoff_verifier_is_read_only_and_recomputes_identity(
        self,
    ) -> None:
        verify = self.contract[
            "verification_semantics"
        ]
        self.assertTrue(
            verify["handoff_verifier_read_only"]
        )
        self.assertTrue(
            verify["p5d3c2_package_reverification_required"]
        )
        self.assertTrue(
            verify["package_byte_tree_digest_recomputed"]
        )
        self.assertTrue(
            verify[
                "all_identity_fields_recomputed_or_cross_checked"
            ]
        )
        self.assertTrue(
            verify["publication_authority_must_remain_false"]
        )

    def test_success_status_remains_explicitly_unauthorized(
        self,
    ) -> None:
        success = self.contract["success_semantics"]
        self.assertEqual(
            success["success_status"],
            "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
        )
        self.assertEqual(
            success["package_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertEqual(
            success["copied_package_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertFalse(
            success["real_vault_modified"]
        )
        self.assertFalse(
            success["current_pointer_created"]
        )
        self.assertFalse(
            success["production_promotion_authorized"]
        )
        self.assertFalse(
            success["p5d2_promotion_confirmed_emitted"]
        )

    def test_failure_semantics_keep_rejected_and_blocked_distinct(
        self,
    ) -> None:
        failure = self.contract["failure_semantics"]
        self.assertEqual(
            failure["candidate_rejected"],
            "FAIL_CANDIDATE_REJECTED",
        )
        self.assertEqual(
            failure["candidate_evaluation_blocked"],
            "BLOCKED_CANDIDATE_EVALUATION",
        )
        self.assertTrue(
            failure[
                "rejected_must_not_be_relabelled_blocked"
            ]
        )
        self.assertTrue(
            failure[
                "blocked_must_not_be_relabelled_rejected"
            ]
        )

    def test_contract_boundary_is_contract_only(self) -> None:
        boundary = self.contract["p5d3f_boundary"]
        self.assertTrue(
            boundary["contract_tests_only"]
        )
        for field in (
            "handoff_runtime_implementation_authorized",
            "sacrificial_handoff_execution_authorized",
            "production_handoff_execution_authorized",
            "real_vault_write_authorized",
            "current_pointer_creation_authorized",
            "current_pointer_mutation_authorized",
            "p5c2_pointer_primitive_invocation_authorized",
            "p5c3r2_current_writer_invocation_authorized",
            "p5d2_promotion_confirmed_event_authorized",
            "production_promotion_authorized",
            "automatic_promotion_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(boundary[field])

    def test_required_breakers_are_unique_and_cover_authority_crossings(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )
        self.assertGreaterEqual(len(breakers), 60)

        required = {
            "P5D3E ephemeral package assumed to survive cleanup",
            "evaluator REJECTED accepted as handoff-ready",
            "evaluator BLOCKED accepted as handoff-ready",
            "promotion staging overlaps live Vault",
            "sealed package mutated to add handoff metadata",
            "publication_authorized true in handoff",
            "CURRENT file created by handoff",
            "real Vault modified by handoff",
            "P5D2 PROMOTION_CONFIRMED emitted by handoff",
            "background observer introduced",
            "polling introduced",
            "Graph/Search CURRENT semantics claimed",
            "P5D4 name reused for finite handoff",
        }
        self.assertTrue(
            required.issubset(set(breakers))
        )

    def test_next_gate_is_implementation_not_live_publication(
        self,
    ) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            gates["p5d3f_implementation"],
            "FINITE_PROMOTION_HANDOFF_IMPLEMENTATION_AND_SACRIFICIAL_STAGING_QUALIFICATION",
        )
        self.assertEqual(
            gates["p5d3g"],
            "FINITE_LIVE_PUBLICATION_TRANSACTION_CONTRACT",
        )


if __name__ == "__main__":
    unittest.main()
