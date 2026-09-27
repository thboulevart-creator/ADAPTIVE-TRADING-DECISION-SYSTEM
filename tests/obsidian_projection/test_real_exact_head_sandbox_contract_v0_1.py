from __future__ import annotations

import json
import unittest
from pathlib import Path


class RealExactHeadSandboxContractTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "real_exact_head_sandbox_contract_v0_1.json"
        )
        cls.contract = json.loads(
            cls.path.read_text(encoding="utf-8")
        )

    def test_schema_status_repository_branch(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_SANDBOX_CONTRACT_V0_1",
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

    def test_p5d3d_qualification_is_exactly_pinned(self) -> None:
        p = self.contract["qualified_predecessor"]
        self.assertEqual(
            p["p5d3d_qualification_commit"],
            "7c244f8ab77d3497a16447b9257c8b204f3e048f",
        )
        self.assertEqual(
            p["p5d3d_qualification_report_blob"],
            "49890581b7c377b26cc4f2379e37b69fc4250c4b",
        )
        self.assertEqual(
            p["p5d3d_functional_candidate"],
            "6efa84c657bbea4edaa56d643d2b9dc0150bcdb1",
        )
        self.assertEqual(
            p["finite_candidate_evaluator_blob"],
            "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
        )

    def test_success_requires_real_exact_head_qualified_outcome(
        self,
    ) -> None:
        o = self.contract["objective"]
        self.assertTrue(o["real_candidate_required"])
        self.assertTrue(o["exact_head_required"])
        self.assertTrue(o["exact_tree_required"])
        self.assertEqual(
            o["outcome_required_for_qualification"],
            "QUALIFIED",
        )
        self.assertEqual(
            o["required_package_status"],
            "PASS_SEALED_UNPROMOTED",
        )

    def test_candidate_resolution_freezes_one_exact_head(
        self,
    ) -> None:
        r = self.contract["candidate_resolution"]
        self.assertTrue(r["performed_outside_evaluator"])
        self.assertTrue(
            r[
                "network_fetch_allowed_only_for_initial_branch_resolution"
            ]
        )
        self.assertEqual(
            r["required_refspec"],
            "+refs/heads/integration/system-v1:refs/remotes/origin/integration/system-v1",
        )
        self.assertTrue(
            r["candidate_head_and_tree_frozen_for_entire_run"]
        )
        self.assertTrue(
            r[
                "branch_movement_after_capture_does_not_change_evaluated_candidate"
            ]
        )
        self.assertTrue(
            r["second_network_fetch_during_evaluation_forbidden"]
        )

    def test_control_clone_must_stay_clean(self) -> None:
        s = self.contract["source_control_clone"]
        self.assertTrue(s["working_tree_clean_before_required"])
        self.assertTrue(s["working_tree_clean_after_required"])
        self.assertTrue(s["canonical_origin_required"])
        self.assertTrue(
            s[
                "candidate_remote_tracking_ref_must_equal_candidate_head"
            ]
        )
        self.assertTrue(
            s["source_candidate_tree_must_equal_candidate_tree"]
        )
        self.assertTrue(
            s["runtime_source_files_must_not_be_modified"]
        )

    def test_sacrificial_repo_is_local_independent_detached(
        self,
    ) -> None:
        s = self.contract["sacrificial_repository"]
        self.assertEqual(s["root"], "OS_TEMP_ONLY")
        self.assertEqual(
            s["creation"],
            "LOCAL_GIT_CLONE_NO_HARDLINKS_NO_CHECKOUT",
        )
        self.assertFalse(
            s[
                "network_transport_during_local_clone_or_local_fetch"
            ]
        )
        self.assertEqual(
            s["origin_after_local_transfer"],
            "CANONICAL_GITHUB_ORIGIN",
        )
        self.assertEqual(
            s["checkout"],
            "DETACHED_EXACT_CANDIDATE_HEAD",
        )
        self.assertTrue(s["git_alternates_forbidden"])
        self.assertTrue(s["hardlinked_object_store_forbidden"])
        self.assertFalse(
            s["candidate_repository_retained_after_run"]
        )

    def test_workspace_is_fresh_and_separate(self) -> None:
        w = self.contract["evaluation_workspace"]
        self.assertEqual(w["root"], "OS_TEMP_ONLY")
        self.assertTrue(
            w[
                "must_be_sibling_not_ancestor_or_descendant_of_candidate_repository"
            ]
        )
        self.assertTrue(w["fresh_empty_before_evaluation"])
        self.assertTrue(
            w["build_a_root_absent_before_evaluation"]
        )
        self.assertTrue(
            w["build_b_root_absent_before_evaluation"]
        )
        self.assertTrue(
            w["candidate_package_root_absent_before_evaluation"]
        )
        self.assertFalse(w["workspace_retained_after_run"])

    def test_activation_uses_p5d2_but_is_not_live_observer_state(
        self,
    ) -> None:
        a = self.contract["activation"]
        self.assertTrue(
            a["sandbox_generated_with_qualified_p5d2"]
        )
        self.assertEqual(
            a["event_1"]["event_type"],
            "REMOTE_HEAD_OBSERVED",
        )
        self.assertEqual(
            a["event_2"]["event_type"],
            "EVALUATION_STARTED",
        )
        self.assertEqual(
            a["required_activation_decision_action"],
            "START_EXACT_HEAD_EVALUATION",
        )
        self.assertEqual(
            a["required_activation_phase"],
            "EVALUATING",
        )
        self.assertTrue(
            a["activation_is_sandbox_control_not_live_observer_state"]
        )

    def test_evaluator_is_exact_qualified_p5d3d_core(self) -> None:
        e = self.contract["evaluator"]
        self.assertEqual(
            e["implementation"],
            "qualified P5-D3D evaluate_candidate_finitely",
        )
        self.assertEqual(
            e["implementation_blob"],
            "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
        )
        self.assertTrue(
            e["network_fetch_inside_evaluator_forbidden"]
        )
        self.assertTrue(
            e["candidate_repository_mutation_forbidden"]
        )
        self.assertTrue(
            e["canonical_control_repository_mutation_forbidden"]
        )
        self.assertTrue(e["real_vault_mutation_forbidden"])

    def test_success_invariants_require_full_real_path(self) -> None:
        q = self.contract["qualification_success"]
        self.assertEqual(
            q["required_evaluator_outcome"],
            "QUALIFIED",
        )
        self.assertIsNone(q["required_failure_code"])
        self.assertTrue(q["p5d2_result_event_emitted"])
        self.assertEqual(
            q["candidate_generation_verification_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            q[
                "projection_a_tree_digest_equals_projection_b_tree_digest"
            ]
        )
        self.assertEqual(
            q["metadata_only_body_read_count_must_equal"],
            0,
        )
        self.assertTrue(
            q["post_evaluation_package_read_only_reverify_required"]
        )

    def test_rejected_and_blocked_are_not_pass(self) -> None:
        r = self.contract["rejected_semantics"]
        b = self.contract["blocked_semantics"]
        self.assertEqual(
            r["qualification_status"],
            "FAIL_REAL_CANDIDATE_REJECTED",
        )
        self.assertTrue(
            r["p5d2_result_event_emitted_must_be_true"]
        )
        self.assertEqual(
            b["qualification_status"],
            "BLOCKED_REAL_EXACT_HEAD_EVALUATION",
        )
        self.assertTrue(
            b["p5d2_result_event_emitted_must_be_false"]
        )

    def test_post_checks_reverify_package_and_repositories(
        self,
    ) -> None:
        p = self.contract["post_evaluation_checks"]
        for field in (
            "candidate_repo_head_unchanged",
            "candidate_repo_tree_unchanged",
            "candidate_repo_worktree_clean",
            "source_control_worktree_clean",
            "build_a_and_b_manifest_identity_matches_candidate",
            "build_a_and_b_metadata_only_body_read_count_zero",
            "build_a_and_b_artifact_count_equals_source_count",
            "build_a_and_b_projection_tree_digest_equal",
            "package_reverification_must_pass",
            "package_reverification_digest_must_equal_evaluator_report",
            "package_must_contain_no_current_views_obsidian_or_git_surface",
        ):
            with self.subTest(field=field):
                self.assertTrue(p[field])

    def test_report_has_no_host_paths(self) -> None:
        r = self.contract["report"]
        self.assertEqual(
            r["schema"],
            "ATDS_OBSIDIAN_P5D3E_REAL_EXACT_HEAD_QUALIFICATION_REPORT_V0_1",
        )
        self.assertEqual(
            r["success_status"],
            "PASS_REAL_EXACT_HEAD_FINITE_EVALUATION",
        )
        self.assertTrue(r["absolute_host_paths_forbidden"])
        self.assertTrue(r["host_identity_forbidden"])
        for field in (
            "candidate_head",
            "candidate_tree",
            "candidate_outcome",
            "candidate_generation_digest_sha256",
            "package_reverification_status",
            "real_candidate_evaluated",
            "evaluation_network_fetch_performed",
            "real_vault_modified",
            "current_pointer_created",
            "production_promotion_authorized",
        ):
            self.assertIn(field, r["required_fields"])

    def test_boundary_never_authorizes_publication_or_background(
        self,
    ) -> None:
        b = self.contract["p5d3e_boundary"]
        self.assertTrue(
            b[
                "real_exact_head_sandbox_execution_authorized_after_contract_qualification"
            ]
        )
        for field in (
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
        self.assertGreaterEqual(len(breakers), 60)
        self.assertEqual(len(breakers), len(set(breakers)))


if __name__ == "__main__":
    unittest.main()
