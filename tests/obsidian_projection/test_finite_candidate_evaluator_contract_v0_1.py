from __future__ import annotations

import json
import unittest
from pathlib import Path


class FiniteCandidateEvaluatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "finite_candidate_evaluator_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_status_repository_branch(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3D_FINITE_CANDIDATE_EVALUATOR_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["source_repository"],
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )
        self.assertEqual(
            self.contract["monitored_branch"],
            "integration/system-v1",
        )

    def test_qualified_chain_is_pinned(self) -> None:
        p = self.contract["qualified_predecessors"]
        self.assertEqual(
            p["p5d2_contract_blob"],
            "5f6a0e223714bb894eddf4ece7c95e6a8ad1e3a3",
        )
        self.assertEqual(
            p["p5d2_implementation_blob"],
            "fd212f61ec38332b677110f40265638af55a73e2",
        )
        self.assertEqual(
            p["p5b2_dynamic_inventory_contract_blob"],
            "80729156f4ac51b760c4347f581f052a175b88b3",
        )
        self.assertEqual(
            p["p5d3b_bridge_contract_blob"],
            "7015db1206cd40b703795d12519707a6455b4fc3",
        )
        self.assertEqual(
            p["p5d3c2_qualification_commit"],
            "205d09e22430e60324b76f2713024e36527e5dba",
        )
        self.assertEqual(
            p["p5d3c2_packager_verifier_blob"],
            "e2e5867536f4f9c7dec475c6696737249536ff39",
        )
        self.assertEqual(
            p["current_head_projection_contract_blob"],
            "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2",
        )

    def test_objective_is_one_finite_nonpromoting_evaluation(
        self,
    ) -> None:
        o = self.contract["objective"]
        self.assertTrue(o["one_candidate_per_invocation"])
        self.assertTrue(o["finite_execution_required"])
        self.assertTrue(o["background_loop_forbidden"])
        self.assertTrue(o["periodic_polling_forbidden"])
        self.assertTrue(o["automatic_promotion_forbidden"])
        self.assertTrue(o["current_pointer_mutation_forbidden"])
        self.assertTrue(o["live_projection_mutation_forbidden"])
        self.assertTrue(o["real_vault_mutation_forbidden"])

    def test_activation_is_exact_p5d2_evaluation_started_result(
        self,
    ) -> None:
        a = self.contract["activation"]
        self.assertEqual(
            a["required_tick_result_schema"],
            "ATDS_OBSIDIAN_ONE_SHOT_TICK_RESULT_V0_1",
        )
        self.assertEqual(
            a["required_decision_action"],
            "START_EXACT_HEAD_EVALUATION",
        )
        self.assertEqual(
            a["required_next_observer_phase"],
            "EVALUATING",
        )
        self.assertTrue(
            a["candidate_head_must_equal_decision_candidate_head"]
        )
        self.assertTrue(
            a["candidate_head_must_equal_next_state_pending_queue_head"]
        )
        self.assertTrue(
            a["source_tick_result_digest_required"]
        )

    def test_orchestrator_requires_prepared_isolated_repo(
        self,
    ) -> None:
        w = self.contract["workspace_boundary"]
        self.assertFalse(w["orchestrator_creates_git_checkout"])
        self.assertTrue(
            w["isolated_candidate_repo_root_is_required_input"]
        )
        self.assertTrue(
            w[
                "isolated_candidate_repo_root_must_be_outside_canonical_worktree"
            ]
        )
        self.assertTrue(
            w["isolated_candidate_repo_root_must_be_outside_real_vault"]
        )
        self.assertTrue(w["candidate_repo_mutation_forbidden"])
        self.assertTrue(w["network_fetch_inside_orchestrator_forbidden"])

    def test_pipeline_order_is_exact(self) -> None:
        self.assertEqual(
            self.contract["ordered_pipeline"],
            [
                "VALIDATE_P5D2_ACTIVATION",
                "VERIFY_ISOLATED_CANDIDATE_REPOSITORY",
                "VERIFY_EXACT_CANDIDATE_HEAD_AND_TREE",
                "BUILD_P5B2_DYNAMIC_INVENTORY",
                "VERIFY_DYNAMIC_INVENTORY_IDENTITY",
                "BUILD_P5D3B_CURRENT_HEAD_SEMANTIC_BRIDGE",
                "VERIFY_BRIDGE_IDENTITY_AND_BODY_READ_POLICY",
                "BUILD_CURRENT_HEAD_PROJECTION_A",
                "BUILD_CURRENT_HEAD_PROJECTION_B",
                "REQUIRE_DETERMINISTIC_DOUBLE_BUILD_EQUALITY",
                "RUN_PREREGISTERED_CURRENT_HEAD_PROJECTION_BREAKERS",
                "CREATE_P5D3C2_VERIFIED_PROJECTION_CANDIDATE",
                "STAGE_P5D3C2_SEALED_UNPROMOTED_GENERATION",
                "VERIFY_P5D3C2_SEALED_UNPROMOTED_GENERATION",
                "CLASSIFY_QUALIFIED_REJECTED_OR_BLOCKED",
                "EMIT_P5D2_RESULT_EVENT_ONLY_IF_DETERMINATE",
                "APPLY_RESULT_ONLY_THROUGH_P5D2_ONE_SHOT_TICK",
                "EMIT_FINITE_EVALUATION_REPORT",
            ],
        )

    def test_inventory_and_bridge_bind_candidate_identity(
        self,
    ) -> None:
        i = self.contract["dynamic_inventory"]
        self.assertTrue(i["source_commit_must_equal_candidate_head"])
        self.assertTrue(i["source_tree_must_equal_candidate_tree"])
        self.assertEqual(i["secret_detection_failure"], "REJECTED")

        b = self.contract["semantic_bridge"]
        self.assertTrue(b["source_commit_must_equal_candidate_head"])
        self.assertTrue(b["source_tree_must_equal_candidate_tree"])
        self.assertTrue(b["dynamic_inventory_digest_must_match"])
        self.assertTrue(
            b["metadata_only_downstream_body_read_allowed_must_be_false"]
        )
        self.assertTrue(
            b["bridge_semantic_body_read_must_be_false_for_all_entries"]
        )

    def test_projection_forbids_legacy_builder_and_relation_extractor(
        self,
    ) -> None:
        p = self.contract["current_head_projection"]
        self.assertEqual(
            p["required_contract_blob"],
            "6bc5286367890a8c393e4f5bea2b4ecb0fb20af2",
        )
        self.assertTrue(p["legacy_builder_direct_reuse_forbidden"])
        self.assertTrue(
            p["legacy_relation_extractor_direct_reuse_forbidden"]
        )
        self.assertTrue(p["legacy_renderer_reuse_allowed"])
        self.assertTrue(
            p["legacy_integrity_primitive_reuse_allowed"]
        )
        self.assertEqual(
            p["metadata_only_body_read_count_must_equal"],
            0,
        )
        self.assertTrue(p["fixed_source_count_forbidden"])

    def test_double_build_requires_exact_bytes(self) -> None:
        d = self.contract["double_build"]
        self.assertTrue(d["required"])
        self.assertTrue(
            d["build_a_root_and_build_b_root_must_be_distinct"]
        )
        self.assertTrue(
            d["exact_generated_relative_path_set_equality"]
        )
        self.assertTrue(
            d["exact_each_generated_file_bytes_equality"]
        )
        self.assertTrue(
            d["exact_each_generated_file_sha256_equality"]
        )
        self.assertEqual(
            d["mismatch_outcome"],
            "REJECTED",
        )
        self.assertEqual(
            d["mismatch_failure_code"],
            "DETERMINISTIC_DOUBLE_BUILD_MISMATCH",
        )

    def test_projection_breaker_manifest_is_exact_and_finite(
        self,
    ) -> None:
        b = self.contract["projection_breaker_manifest"]
        breakers = b["breakers"]
        self.assertEqual(
            [item["id"] for item in breakers],
            [
                "CHP-B01",
                "CHP-B02",
                "CHP-B03",
                "CHP-B04",
                "CHP-B05",
                "CHP-B06",
                "CHP-B07",
                "CHP-B08",
                "CHP-B09",
                "CHP-B10",
                "CHP-B11",
                "CHP-B12",
            ],
        )
        self.assertTrue(b["manifest_digest_required"])
        self.assertTrue(b["result_digest_required"])
        self.assertEqual(
            b["candidate_breaker_failure_outcome"],
            "REJECTED",
        )
        self.assertEqual(
            b["infrastructure_failure_outcome"],
            "BLOCKED",
        )
        self.assertTrue(b["breakers_read_only_after_build"])

    def test_packaging_maps_all_scientific_identity(self) -> None:
        p = self.contract["packaging_mapping"]
        fields = p["verified_projection_candidate_fields"]
        self.assertEqual(
            fields["dynamic_inventory_digest_sha256"],
            "P5-B2 inventory digest",
        )
        self.assertEqual(
            fields["semantic_bridge_digest_sha256"],
            "P5-D3B bridge entry digest",
        )
        self.assertEqual(
            fields["semantic_record_digest_sha256"],
            "P5-D3B semantic record digest",
        )
        self.assertEqual(
            fields["breaker_status"],
            "PASS",
        )
        self.assertEqual(
            fields["determinism_status"],
            "PASS",
        )
        self.assertEqual(
            p["required_package_verification_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            p["promotion_authorized_must_be_false"]
        )

    def test_outcome_model_keeps_blocked_distinct(self) -> None:
        o = self.contract["outcome_model"]
        self.assertEqual(
            o["allowed"],
            ["QUALIFIED", "REJECTED", "BLOCKED"],
        )
        self.assertTrue(o["partial_success_forbidden"])
        self.assertTrue(
            o["blocked_must_not_be_relabelled_rejected"]
        )
        self.assertTrue(
            o["rejected_must_not_be_relabelled_blocked"]
        )

    def test_p5d2_event_mapping_is_exact(self) -> None:
        e = self.contract["p5d2_result_event"]
        self.assertEqual(
            e["qualified_event_type"],
            "EVALUATION_PASSED",
        )
        self.assertEqual(
            e["rejected_event_type"],
            "EVALUATION_FAILED",
        )
        self.assertIsNone(e["blocked_event_type"])
        self.assertIsNone(e["observed_head"])
        self.assertIsNone(e["transition_class"])
        self.assertIsNone(e["qualified_failure_code"])
        self.assertTrue(e["direct_state_mutation_forbidden"])
        self.assertTrue(
            e["blocked_event_sequence_does_not_advance"]
        )

    def test_live_projection_never_changes_during_evaluation(
        self,
    ) -> None:
        p = self.contract["post_result_invariants"]
        self.assertTrue(
            p["qualified_live_projection_head_unchanged"]
        )
        self.assertTrue(
            p["rejected_live_projection_head_unchanged"]
        )
        self.assertTrue(
            p["blocked_live_projection_head_unchanged"]
        )
        self.assertTrue(p["qualified_does_not_promote"])
        self.assertTrue(
            p["real_vault_modified_must_be_false"]
        )
        self.assertTrue(
            p["current_pointer_created_must_be_false"]
        )

    def test_evaluation_report_binds_all_major_evidence(
        self,
    ) -> None:
        r = self.contract["evaluation_report"]
        fields = set(r["required_fields"])
        for field in (
            "source_tick_result_digest_sha256",
            "dynamic_inventory_digest_sha256",
            "semantic_bridge_digest_sha256",
            "semantic_record_digest_sha256",
            "projection_a_tree_digest_sha256",
            "projection_b_tree_digest_sha256",
            "projection_breaker_manifest_digest_sha256",
            "projection_breaker_result_digest_sha256",
            "determinism_evidence_digest_sha256",
            "candidate_generation_digest_sha256",
            "outcome",
            "p5d2_result_tick_digest_sha256",
            "live_projection_head_before",
            "live_projection_head_after",
        ):
            self.assertIn(field, fields)
        self.assertTrue(
            r["live_projection_head_after_must_equal_before"]
        )
        self.assertTrue(r["absolute_host_paths_forbidden"])

    def test_retry_requires_fresh_builds_and_package(self) -> None:
        r = self.contract["retry_semantics"]
        self.assertTrue(
            r["blocked_may_retry_same_exact_candidate_head"]
        )
        self.assertTrue(
            r["retry_must_revalidate_activation_and_all_identity_gates"]
        )
        self.assertTrue(r["retry_must_use_fresh_build_a_root"])
        self.assertTrue(r["retry_must_use_fresh_build_b_root"])
        self.assertTrue(
            r["retry_must_use_fresh_candidate_package_root"]
        )

    def test_p5d3d_contract_authorizes_no_runtime_yet(
        self,
    ) -> None:
        b = self.contract["p5d3d_boundary"]
        self.assertTrue(b["contract_only_until_qualified"])
        for field in (
            "current_head_projection_builder_implementation_authorized",
            "current_head_relation_adapter_implementation_authorized",
            "finite_orchestrator_implementation_authorized",
            "candidate_breaker_runner_implementation_authorized",
            "orchestrator_execution_authorized",
            "network_fetch_execution_authorized",
            "git_checkout_creation_authorized",
            "production_promotion_authorized",
            "current_pointer_mutation_authorized",
            "real_vault_write_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(b[field])

    def test_next_gate_reserves_real_candidate_for_p5d3e(
        self,
    ) -> None:
        g = self.contract["next_action_gate"]
        self.assertEqual(
            g["after_contract_qualification"],
            "P5_D3D_IMPLEMENTATION_CANDIDATE",
        )
        self.assertTrue(
            g["orchestrator_execution_in_synthetic_fixture_only"]
        )
        self.assertEqual(
            g["real_candidate_sandbox_execution_reserved_for"],
            "P5-D3E",
        )
        self.assertFalse(g["network_fetch_allowed"])
        self.assertFalse(g["production_promotion_allowed"])

    def test_evaluator_breaker_registry_is_large_and_unique(
        self,
    ) -> None:
        breakers = self.contract["required_breakers"]
        self.assertGreaterEqual(len(breakers), 90)
        self.assertEqual(len(breakers), len(set(breakers)))


if __name__ == "__main__":
    unittest.main()
