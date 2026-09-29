from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "persistent_production_handoff_gate_contract_v0_1.json"
)
CONTRACT_PATH = REPO_ROOT / CONTRACT_RELATIVE

EXPECTED_CONTRACT_BLOB = (
    "59ce9e079d256799d072405fa4a623ba58b75c0d"
)


def _blob() -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{CONTRACT_RELATIVE}"],
        cwd=str(REPO_ROOT),
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def _clean() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", CONTRACT_RELATIVE],
        cwd=str(REPO_ROOT),
        check=False,
        text=True,
        capture_output=True,
    )
    return result.returncode == 0 and not result.stdout.strip()


class PersistentProductionHandoffGateContractV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            CONTRACT_PATH.read_text(encoding="utf-8")
        )

    def test_identity_and_blob(self) -> None:
        self.assertTrue(_clean())
        self.assertEqual(_blob(), EXPECTED_CONTRACT_BLOB)
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3F_PERSISTENT_PRODUCTION_HANDOFF_GATE_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D3F-PERSISTENT-PRODUCTION-HANDOFF",
        )

    def test_p5d3f_authority_is_exact(self) -> None:
        a = self.contract["qualified_authorities"]["p5d3f"]
        self.assertEqual(
            a["contract_blob"],
            "64744325251db350d26c0269090ce62d5fa5f2e8",
        )
        self.assertEqual(
            a["implementation_candidate"],
            "a41c5b150168c2e4eb06648237022a4974868423",
        )
        self.assertEqual(
            a["implementation_blob"],
            "2108131914cf65bb076b80f5bb63cd63267567fa",
        )
        self.assertEqual(
            a["accepted_success_status"],
            "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
        )

    def test_exact_paths_are_siblings_and_nonintersecting(self) -> None:
        p = self.contract["exact_paths"]
        self.assertEqual(
            p["production_staging_root"],
            r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROMOTION-STAGING",
        )
        self.assertEqual(
            p["protected_real_vault_root"],
            r"C:\Users\Boulevart\OneDrive\Bureau\ATDS\ATDS-OBSIDIAN-PROJECTION",
        )
        self.assertTrue(p["roots_must_be_siblings"])
        self.assertTrue(p["roots_may_not_intersect"])
        self.assertTrue(p["staging_git_repository_root_forbidden"])

    def test_source_candidate_is_fresh_remote_not_local_checkout(self) -> None:
        s = self.contract["source_candidate"]
        self.assertEqual(
            s["selection"],
            "FRESH_REMOTE_HEAD_OF_MONITORED_BRANCH",
        )
        self.assertTrue(s["fresh_fetch_required"])
        self.assertTrue(s["exact_remote_head_binding_required"])
        self.assertTrue(s["exact_remote_tree_binding_required"])
        self.assertTrue(
            s["stale_preflight_head_may_not_be_execution_authority"]
        )
        self.assertTrue(
            s["local_checked_out_head_may_not_select_candidate"]
        )
        self.assertTrue(
            s["onedrive_dirty_repository_may_not_be_candidate"]
        )
        self.assertTrue(
            s["temporary_clean_detached_repository_required"]
        )

    def test_setup_authority_is_exact_and_bounded(self) -> None:
        s = self.contract["setup_authority"]
        self.assertTrue(
            s["may_create_exact_staging_root_if_absent"]
        )
        self.assertFalse(s["may_create_parent"])
        self.assertTrue(
            s["staging_parent_must_already_exist"]
        )
        self.assertFalse(
            s["may_create_any_other_persistent_root"]
        )
        self.assertTrue(
            s["may_create_temp_candidate_repository"]
        )
        self.assertTrue(
            s["may_create_temp_evaluation_workspace"]
        )

    def test_execution_is_one_finite_handoff_only(self) -> None:
        e = self.contract["execution"]
        self.assertTrue(e["one_finite_handoff_only"])
        self.assertTrue(
            e["invoke_only_qualified_p5d3f_runtime"]
        )
        self.assertTrue(
            e["candidate_head_and_tree_must_match_fresh_remote"]
        )
        self.assertTrue(
            e["persistent_output_limited_to_exact_staging_root"]
        )
        self.assertEqual(
            e["expected_wrapper_layout"],
            ["package", "PROMOTION-HANDOFF.json"],
        )
        self.assertTrue(
            e["post_materialization_read_only_verification_required"]
        )
        self.assertTrue(
            e["temporary_candidate_cleanup_required"]
        )
        self.assertTrue(
            e["temporary_evaluation_cleanup_required"]
        )

    def test_real_vault_zero_mutation_is_independent_and_exact(self) -> None:
        z = self.contract["real_vault_zero_mutation"]
        for field in (
            "required",
            "independent_before_fingerprint_required",
            "independent_after_fingerprint_required",
            "fingerprint_binds_relative_path",
            "fingerprint_binds_path_type",
            "fingerprint_binds_regular_file_length",
            "fingerprint_binds_regular_file_sha256",
            "before_after_fingerprint_must_match",
            "no_generation_materialization",
            "no_path_creation",
            "no_path_deletion",
            "no_byte_change",
        ):
            self.assertTrue(z[field], field)

    def test_success_remains_ready_unauthorized(self) -> None:
        s = self.contract["success_semantics"]
        self.assertEqual(
            s["runtime_status"],
            "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
        )
        self.assertEqual(
            s["handoff_status"],
            "READY_UNAUTHORIZED",
        )
        self.assertEqual(
            s["package_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertFalse(s["publication_authorized"])
        self.assertFalse(s["real_vault_modified"])
        self.assertFalse(s["current_pointer_created"])
        self.assertFalse(
            s["production_promotion_authorized"]
        )
        self.assertFalse(
            s["p5d2_promotion_confirmed_emitted"]
        )
        self.assertTrue(
            s["independent_zero_mutation_verified"]
        )
        self.assertTrue(s["mandatory_stop"])

    def test_failure_semantics_are_fail_closed(self) -> None:
        f = self.contract["failure_semantics"]
        self.assertEqual(
            f["remote_freshness_mismatch"],
            "BLOCKED_REMOTE_HEAD_RACE",
        )
        self.assertEqual(
            f["staging_preexisting_conflict"],
            "BLOCKED_PERSISTENT_STAGING_CONFLICT",
        )
        self.assertEqual(
            f["real_vault_mutation"],
            "FAIL_REAL_VAULT_MUTATED",
        )
        self.assertEqual(
            f["cleanup_failure"],
            "BLOCKED_TEMPORARY_CLEANUP",
        )

    def test_contract_boundary_is_closed(self) -> None:
        b = self.contract["boundary"]
        self.assertTrue(b["contract_tests_only"])
        for field in (
            "persistent_handoff_execution_authorized",
            "persistent_staging_creation_authorized",
            "real_vault_read_authorized",
            "real_vault_write_authorized",
            "current_pointer_creation_authorized",
            "current_pointer_mutation_authorized",
            "generation_materialization_in_real_vault_authorized",
            "live_publication_transaction_authorized",
            "p5d2_promotion_confirmed_authorized",
            "stage_a_authority_authorized",
            "stage_b_authority_authorized",
            "automatic_publication_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "p5d4_authorized",
            "p6_authorized",
        ):
            self.assertFalse(b[field], field)

    def test_breakers_are_unique_and_cover_critical_families(self) -> None:
        breakers = self.contract["required_breakers"]
        self.assertEqual(len(breakers), len(set(breakers)))
        self.assertGreaterEqual(len(breakers), 45)
        for name in (
            "STALE_REMOTE_HEAD",
            "LOCAL_HEAD_IMPLICIT_SELECTION",
            "DIRTY_ONEDRIVE_REPOSITORY_SELECTION",
            "STAGING_REAL_VAULT_INTERSECTION",
            "SECOND_HANDOFF_IN_ONE_RUN",
            "HANDOFF_RECORD_TAMPER",
            "HANDOFF_PACKAGE_TAMPER",
            "REAL_VAULT_BYTE_CHANGED",
            "REAL_VAULT_CURRENT_CHANGED",
            "REAL_VAULT_GENERATION_MATERIALIZED",
            "LIVE_PUBLICATION_SURFACE",
            "STAGE_A_AUTHORITY_SURFACE",
            "STAGE_B_AUTHORITY_SURFACE",
            "TEMP_CANDIDATE_NOT_CLEANED",
            "TEMP_EVALUATION_NOT_CLEANED",
        ):
            self.assertIn(name, breakers)

    def test_next_gate_returns_to_real_vault_read_only_plan(self) -> None:
        n = self.contract["next_gate"]
        self.assertEqual(
            n["after_contract_qualification"],
            "P5-D3F-PERSISTENT-PRODUCTION-HANDOFF-EXECUTION-HARNESS",
        )
        self.assertEqual(
            n["after_execution_success"],
            "P5-D3G-EXACT-REAL-VAULT-READ-ONLY-PLAN-QUALIFICATION",
        )
        self.assertTrue(
            n["mandatory_stop_after_persistent_handoff"]
        )


if __name__ == "__main__":
    unittest.main()
