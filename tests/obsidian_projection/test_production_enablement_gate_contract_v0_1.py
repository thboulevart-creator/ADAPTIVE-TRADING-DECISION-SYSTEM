from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "production_enablement_gate_contract_v0_1.json"
)
CONTRACT_PATH = REPO_ROOT / CONTRACT_RELATIVE

EXPECTED_CONTRACT_BLOB = (
    "5de65f5d13a93d1325d53e1b58536ed0860921f2"
)


def _committed_blob() -> str:
    result = subprocess.run(
        [
            "git",
            "rev-parse",
            f"HEAD:{CONTRACT_RELATIVE}",
        ],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def _clean() -> bool:
    result = subprocess.run(
        [
            "git",
            "status",
            "--porcelain",
            "--",
            CONTRACT_RELATIVE,
        ],
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0 and not result.stdout.strip()


class ProductionEnablementGateContractV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            CONTRACT_PATH.read_text(encoding="utf-8")
        )

    def test_identity_and_blob_are_exact(self) -> None:
        self.assertTrue(_clean())
        self.assertEqual(
            _committed_blob(),
            EXPECTED_CONTRACT_BLOB,
        )
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3G_PRODUCTION_ENABLEMENT_GATE_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D3G-PRODUCTION-ENABLEMENT",
        )

    def test_source_qualification_is_exact(self) -> None:
        q = self.contract["qualified_source"]
        self.assertEqual(
            q["p5d3g_contract_blob"],
            "64997ddd9977229961387f66af4de356c045c0ac",
        )
        self.assertEqual(
            q["p5d3g_implementation_qualification_commit"],
            "87c189cd3b0fe6ce40845214a943a14407618ece",
        )
        self.assertEqual(
            q["p5d3g_qualified_functional_candidate"],
            "f725854a7539d1a3b589ca2e49d45c22f6699d3d",
        )
        self.assertEqual(
            q["p5d3g_qualified_implementation_blob"],
            "b8875f8973ddf1076ff20d8e725ce04abbb814a8",
        )
        self.assertTrue(
            q["currently_qualified_runtime_is_sacrificial_only"]
        )

    def test_production_vault_is_read_only_candidate_scope(self) -> None:
        p = self.contract["protected_production_vault"]
        self.assertTrue(p["path_must_resolve_exactly"])
        self.assertTrue(
            p["symlink_or_reparse_alias_forbidden"]
        )
        self.assertTrue(
            p["read_only_inspection_candidate_scope_only"]
        )
        self.assertFalse(p["mutation_authorized"])

    def test_two_stage_human_authority_is_mandatory(self) -> None:
        a = self.contract["architecture_decision"]
        self.assertTrue(a["two_stage_human_authority_required"])
        self.assertTrue(a["stage_a_is_plan_approval_only"])
        self.assertTrue(
            a["stage_b_is_distinct_execution_authorization"]
        )
        self.assertTrue(a["stage_a_must_not_imply_stage_b"])
        self.assertTrue(
            a["exact_plan_precedes_any_human_approval"]
        )

    def test_sacrificial_guard_may_not_be_weakened(self) -> None:
        a = self.contract["architecture_decision"]
        self.assertTrue(
            a["current_sacrificial_guard_must_not_be_deleted_or_bypassed"]
        )
        self.assertTrue(
            a["production_planning_entrypoint_must_be_distinct"]
        )
        breakers = set(self.contract["required_breakers"])
        self.assertIn("SACRIFICIAL_GUARD_DELETED", breakers)
        self.assertIn("SACRIFICIAL_GUARD_BYPASSED", breakers)

    def test_production_plan_is_deterministic_and_read_only(self) -> None:
        p = self.contract["production_plan"]
        self.assertEqual(
            p["schema"],
            "ATDS_OBSIDIAN_P5D3G_REAL_LIVE_PUBLICATION_PLAN_V0_1",
        )
        self.assertTrue(p["deterministic"])
        self.assertTrue(p["timestamp_free_digest_semantics"])
        self.assertTrue(p["read_only"])
        self.assertFalse(p["planning_may_create_real_vault_file"])
        self.assertFalse(p["planning_may_create_real_vault_directory"])
        self.assertFalse(p["planning_may_create_current_tmp"])
        self.assertFalse(p["planning_may_create_writer_lock"])
        self.assertFalse(p["planning_may_materialize_generation"])
        self.assertFalse(p["planning_may_emit_promotion_confirmed"])

    def test_plan_binds_exact_prestate_and_identity(self) -> None:
        p = self.contract["production_plan"]
        for field in (
            "exact_real_vault_identity_required",
            "exact_qualified_handoff_identity_required",
            "exact_candidate_head_required",
            "exact_candidate_tree_required",
            "exact_generation_id_required",
            "exact_candidate_generation_digest_required",
            "exact_publication_generation_digest_required",
            "exact_current_state_required",
            "exact_current_tmp_state_required",
            "exact_target_generation_state_required",
            "exact_publication_mode_required",
            "exact_operation_sequence_digest_required",
            "exact_qualified_contract_blob_required",
            "exact_qualified_implementation_blob_required",
        ):
            self.assertTrue(p[field])

    def test_plan_modes_are_bounded(self) -> None:
        self.assertEqual(
            set(self.contract["production_plan"]["publication_modes"]),
            {
                "BOOTSTRAP_NO_CURRENT",
                "REPLACE_EXISTING_CURRENT",
            },
        )

    def test_stage_a_approval_is_exact_one_shot_and_nonexecuting(self) -> None:
        a = self.contract["stage_a_plan_approval"]
        self.assertTrue(a["required"])
        self.assertTrue(a["occurs_after_plan"])
        self.assertEqual(
            a["authorized_action"],
            "APPROVE_ONE_EXACT_REAL_LIVE_PUBLICATION_PLAN_FOR_FUTURE_EXECUTION_REVIEW",
        )
        self.assertTrue(a["exact_plan_digest_binding_required"])
        self.assertTrue(a["one_shot_nonce_required"])
        self.assertTrue(a["wildcard_approval_forbidden"])
        self.assertTrue(a["prior_session_approval_reuse_forbidden"])
        self.assertTrue(a["implicit_cli_approval_forbidden"])
        self.assertTrue(a["automatic_approval_forbidden"])
        self.assertTrue(a["approval_is_not_execution_authority"])
        self.assertTrue(
            a["approval_consumption_may_not_mutate_real_vault"]
        )

    def test_stage_a_approval_binds_prestate(self) -> None:
        a = self.contract["stage_a_plan_approval"]
        for field in (
            "exact_candidate_head_binding_required",
            "exact_candidate_tree_binding_required",
            "exact_generation_id_binding_required",
            "exact_publication_mode_binding_required",
            "exact_expected_current_state_binding_required",
            "exact_expected_current_sha256_binding_required_when_present",
            "exact_target_state_binding_required",
        ):
            self.assertTrue(a[field])

    def test_zero_mutation_proof_is_strict(self) -> None:
        z = self.contract["zero_mutation_proof"]
        self.assertTrue(z["required"])
        self.assertTrue(z["capture_before_plan"])
        self.assertTrue(z["capture_after_plan"])
        self.assertTrue(
            z["before_after_content_tree_digest_must_match"]
        )
        self.assertTrue(z["no_real_vault_path_created"])
        self.assertTrue(z["no_real_vault_path_deleted"])
        self.assertTrue(z["no_real_vault_file_bytes_changed"])
        self.assertTrue(z["no_current_pointer_change"])
        self.assertTrue(z["no_generation_materialization"])
        self.assertTrue(
            z["evidence_may_be_persisted_only_outside_real_vault"]
        )

    def test_stage_b_is_reserved_and_unavailable(self) -> None:
        b = self.contract["stage_b_execution_authorization"]
        self.assertEqual(
            b["status"],
            "RESERVED_FUTURE_GATE_ONLY",
        )
        self.assertFalse(b["issuable_in_this_gate"])
        self.assertFalse(b["consumable_in_this_gate"])
        self.assertTrue(
            b["requires_prior_stage_a_gate_qualification"]
        )
        self.assertTrue(
            b["requires_separate_later_human_instruction"]
        )
        self.assertTrue(
            b["must_bind_exact_stage_a_plan_digest"]
        )
        self.assertTrue(
            b["must_bind_exact_stage_a_approval_digest"]
        )

    def test_qualification_may_read_later_but_never_write(self) -> None:
        q = self.contract["qualification_execution"]
        self.assertFalse(
            q["contract_qualification_may_touch_real_vault"]
        )
        self.assertTrue(
            q["future_gate_implementation_may_read_real_vault"]
        )
        self.assertFalse(
            q["future_gate_implementation_may_write_real_vault"]
        )
        self.assertFalse(
            q["future_gate_implementation_may_issue_stage_b_authorization"]
        )
        self.assertFalse(
            q["future_gate_implementation_may_execute_publication"]
        )
        self.assertTrue(q["stop_after_qualification"])

    def test_success_means_zero_mutation_and_stop(self) -> None:
        s = self.contract["success_semantics"]
        self.assertEqual(
            s["qualification_status"],
            "PASS_PRODUCTION_ENABLEMENT_READ_ONLY_GATE_QUALIFIED",
        )
        self.assertTrue(s["real_vault_read_only_plan_verified"])
        self.assertTrue(
            s["stage_a_plan_approval_validation_verified"]
        )
        self.assertTrue(s["zero_real_vault_mutation_verified"])
        self.assertFalse(s["real_publication_executed"])
        self.assertFalse(s["production_current_mutated"])
        self.assertFalse(s["production_generation_materialized"])
        self.assertFalse(
            s["production_promotion_confirmed_emitted"]
        )
        self.assertFalse(s["stage_b_execution_authority_issued"])
        self.assertTrue(s["mandatory_stop"])

    def test_boundary_is_closed_to_runtime_and_execution(self) -> None:
        b = self.contract["boundary"]
        self.assertTrue(b["contract_tests_only"])
        for field in (
            "production_planning_runtime_implementation_authorized",
            "real_vault_read_only_execution_authorized",
            "real_vault_write_authorized",
            "production_current_pointer_creation_authorized",
            "production_current_pointer_mutation_authorized",
            "production_generation_materialization_authorized",
            "production_p5d2_promotion_confirmed_authorized",
            "stage_b_execution_authorization_issue_authorized",
            "stage_b_execution_authorization_consumption_authorized",
            "automatic_publication_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p5d4_authorized",
            "p6_graph_search_current_semantics_authorized",
        ):
            self.assertFalse(b[field], field)

    def test_failure_semantics_cover_authority_and_mutation(self) -> None:
        f = self.contract["failure_semantics"]
        self.assertEqual(
            f["zero_mutation_proof_failed"],
            "FAIL_ZERO_REAL_VAULT_MUTATION_PROOF",
        )
        self.assertEqual(
            f["execution_surface_reachable"],
            "FAIL_PRODUCTION_EXECUTION_SURFACE_REACHABLE",
        )
        self.assertEqual(
            f["stage_b_authority_present"],
            "FAIL_STAGE_B_AUTHORITY_PREMATURE",
        )

    def test_required_breakers_cover_critical_families(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertEqual(len(breakers), len(set(breakers)))
        self.assertGreaterEqual(len(breakers), 60)
        for name in (
            "PLAN_CREATES_CURRENT_TMP",
            "PLAN_MATERIALIZES_GENERATION",
            "STAGE_A_APPROVAL_TREATED_AS_EXECUTION_AUTHORITY",
            "REAL_VAULT_CONTENT_TREE_CHANGED_DURING_PLAN",
            "STAGE_B_AUTHORIZATION_ISSUED_PREMATURELY",
            "PRODUCTION_EXECUTION_ENTRYPOINT_REACHABLE",
            "AUTOMATIC_PUBLICATION_SURFACE",
            "P5D4_AUTHORITY_LEAK",
            "P6_AUTHORITY_LEAK",
        ):
            self.assertIn(name, breakers)

    def test_next_gate_is_read_only_and_stops(self) -> None:
        n = self.contract["next_gate"]
        self.assertEqual(
            n["name"],
            "P5-D3G-PRODUCTION-ENABLEMENT-IMPLEMENTATION",
        )
        self.assertEqual(
            n["description"],
            "READ_ONLY_REAL_VAULT_PLAN_AND_STAGE_A_APPROVAL_VALIDATION_WITH_ZERO_MUTATION_QUALIFICATION",
        )
        self.assertTrue(
            n["mandatory_stop_after_gate_qualification"]
        )
        self.assertIn(
            "SEPARATE_HUMAN_AUTHORIZATION_REQUIRED",
            n["stage_b_after_success"],
        )


if __name__ == "__main__":
    unittest.main()
