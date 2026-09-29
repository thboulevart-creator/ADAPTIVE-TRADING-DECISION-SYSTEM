from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]

CONTRACT_RELATIVE = (
    "tools/obsidian_projection/"
    "live_publication_transaction_contract_v0_1.json"
)
CONTRACT_PATH = REPO_ROOT / CONTRACT_RELATIVE

EXPECTED_CONTRACT_BLOB = (
    "64997ddd9977229961387f66af4de356c045c0ac"
)


def _committed_contract_blob() -> str:
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


def _working_tree_contract_is_clean() -> bool:
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


class LivePublicationTransactionContractV01Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CONTRACT_PATH.read_bytes()
        cls.contract = json.loads(
            cls.raw.decode("utf-8")
        )

    def test_contract_blob_schema_and_frontier_are_exact(
        self,
    ) -> None:
        self.assertTrue(
            _working_tree_contract_is_clean()
        )
        self.assertEqual(
            _committed_contract_blob(),
            EXPECTED_CONTRACT_BLOB,
        )
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3G_LIVE_PUBLICATION_TRANSACTION_CONTRACT_V0_1",
        )
        self.assertEqual(
            self.contract["frontier"],
            "P5-D3G",
        )
        self.assertEqual(
            self.contract["status"],
            "CANDIDATE_PREREGISTRATION_ONLY",
        )

    def test_architecture_is_finite_human_authorized_and_single_writer(
        self,
    ) -> None:
        a = self.contract[
            "architecture_decision"
        ]
        self.assertTrue(a["finite_transaction_only"])
        self.assertTrue(
            a["read_only_plan_precedes_authorization"]
        )
        self.assertTrue(
            a["explicit_human_authorization_required"]
        )
        self.assertTrue(
            a["single_writer_ownership_required"]
        )
        self.assertTrue(
            a[
                "physical_publication_precedes_logical_confirmation"
            ]
        )

    def test_p5d3f_authority_is_exact(self) -> None:
        a = self.contract[
            "qualified_authorities"
        ]["p5d3f"]
        self.assertEqual(
            a["handoff_contract_blob"],
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
            a["required_handoff_status"],
            "READY_UNAUTHORIZED",
        )

    def test_p5c2_only_selected_pointer_primitive_survives(
        self,
    ) -> None:
        a = self.contract[
            "qualified_authorities"
        ]["p5c2"]
        self.assertEqual(
            a["selected_primitive"],
            "IMMUTABLE_GENERATION_ATOMIC_POINTER",
        )
        self.assertFalse(
            a["directory_two_rename_swap_qualified"]
        )
        self.assertFalse(
            a["movefileex_directory_replace_qualified"]
        )

    def test_p5c3r2_semantics_are_exact_but_synthetic_writer_not_reused(
        self,
    ) -> None:
        a = self.contract[
            "qualified_authorities"
        ]["p5c3r2"]
        self.assertEqual(
            a["retry_implementation_blob"],
            "df1a6988c5ce09d52941793a98f2a88728aaed41",
        )
        self.assertEqual(
            a["retry_contract_blob"],
            "a3fb7736f2c25f144b1d9bc4a50cbf4029e3dc33",
        )
        self.assertEqual(
            a["write_retry_winerrors"],
            [5, 32],
        )
        self.assertFalse(
            a["exact_synthetic_writer_direct_reuse_authorized"]
        )

    def test_p5d2_confirmation_is_after_physical_publication(
        self,
    ) -> None:
        a = self.contract[
            "qualified_authorities"
        ]["p5d2"]
        self.assertTrue(
            a[
                "promotion_confirmed_is_external_logical_confirmation_only"
            ]
        )
        self.assertTrue(
            a[
                "physical_publication_must_precede_promotion_confirmed"
            ]
        )

    def test_handoff_is_reverified_before_plan_and_mutation(
        self,
    ) -> None:
        h = self.contract["input_handoff"]
        self.assertTrue(
            h["fresh_read_only_verification_before_planning"]
        )
        self.assertTrue(
            h[
                "fresh_read_only_reverification_immediately_before_first_mutation"
            ]
        )
        self.assertEqual(
            h["handoff_status_required"],
            "READY_UNAUTHORIZED",
        )
        for field in (
            "publication_authorized_required",
            "current_pointer_mutation_authorized_required",
            "real_vault_write_authorized_required",
            "promotion_confirmed_event_authorized_required",
        ):
            self.assertFalse(h[field])

    def test_publication_plan_is_read_only_and_prestate_bound(
        self,
    ) -> None:
        p = self.contract["publication_plan"]
        self.assertTrue(p["read_only"])
        self.assertTrue(
            p["plan_must_capture_current_prestate"]
        )
        self.assertTrue(
            p[
                "plan_must_capture_target_absence_or_exact_recovery_state"
            ]
        )
        self.assertTrue(
            p["planning_may_not_create_live_files"]
        )
        self.assertEqual(
            set(p["publication_modes"]),
            {
                "REPLACE_EXISTING_CURRENT",
                "BOOTSTRAP_NO_CURRENT",
            },
        )

    def test_human_authorization_is_one_shot_exact_and_nonimplicit(
        self,
    ) -> None:
        a = self.contract[
            "human_authorization"
        ]
        self.assertTrue(a["required"])
        self.assertTrue(a["occurs_after_plan"])
        self.assertEqual(
            a["authorized_action_required"],
            "EXECUTE_ONE_FINITE_LIVE_PUBLICATION_TRANSACTION",
        )
        self.assertTrue(
            a["exact_plan_digest_binding_required"]
        )
        self.assertTrue(
            a["one_shot_nonce_required"]
        )
        self.assertTrue(
            a["wildcard_authorization_forbidden"]
        )
        self.assertTrue(
            a[
                "implicit_authorization_from_cli_invocation_forbidden"
            ]
        )
        self.assertTrue(
            a["automatic_authorization_forbidden"]
        )

    def test_single_writer_cannot_be_stolen_or_shared(
        self,
    ) -> None:
        s = self.contract["single_writer"]
        self.assertTrue(
            s[
                "exclusive_writer_ownership_required_before_first_mutation"
            ]
        )
        self.assertTrue(
            s["concurrent_second_writer_must_block"]
        )
        self.assertTrue(
            s[
                "stale_writer_ownership_must_not_be_silently_stolen"
            ]
        )

    def test_current_prestate_modes_are_explicit(self) -> None:
        c = self.contract["current_prestate"]
        self.assertTrue(
            c[
                "replace_mode_requires_valid_existing_current"
            ]
        )
        self.assertTrue(
            c[
                "bootstrap_mode_requires_current_absent"
            ]
        )
        self.assertTrue(
            c[
                "bootstrap_mode_requires_explicit_bootstrap_authorization"
            ]
        )
        self.assertTrue(
            c[
                "changed_current_prestate_blocks_without_mutation"
            ]
        )

    def test_live_generation_wrapper_preserves_sealed_package(
        self,
    ) -> None:
        g = self.contract[
            "live_generation_wrapper"
        ]
        layout = set(g["relative_layout"])
        self.assertIn(
            "generations/<generation_id>/package/generated/",
            layout,
        )
        self.assertIn(
            "generations/<generation_id>/package/_atds_generation/",
            layout,
        )
        self.assertIn(
            "generations/<generation_id>/PUBLICATION-MANIFEST.json",
            layout,
        )
        self.assertIn(
            "generations/<generation_id>/INDEX.md",
            layout,
        )
        self.assertTrue(
            g["sealed_package_subtree_byte_exact"]
        )
        self.assertTrue(
            g["sealed_package_must_not_be_mutated"]
        )
        self.assertTrue(
            g[
                "target_verification_required_before_current_mutation"
            ]
        )

    def test_existing_target_policy_is_fail_closed(self) -> None:
        g = self.contract[
            "live_generation_wrapper"
        ]
        self.assertTrue(
            g[
                "existing_target_exact_match_may_be_reused_only_for_recovery"
            ]
        )
        self.assertTrue(
            g[
                "existing_target_partial_or_mismatch_must_block"
            ]
        )
        self.assertTrue(
            g["overwrite_existing_target_forbidden"]
        )
        self.assertTrue(
            g[
                "recursive_delete_existing_target_forbidden"
            ]
        )

    def test_current_pointer_preserves_qualified_retry_semantics(
        self,
    ) -> None:
        p = self.contract["current_pointer"]
        self.assertEqual(
            p["current_relative_path"],
            "CURRENT.md",
        )
        self.assertEqual(
            p["temporary_relative_path"],
            "CURRENT.tmp",
        )
        self.assertTrue(
            p["temporary_exclusive_create_required"]
        )
        self.assertTrue(
            p["temporary_fsync_required"]
        )
        self.assertEqual(
            p["atomic_replace_primitive"],
            "os.replace(CURRENT.tmp,CURRENT.md)",
        )
        self.assertEqual(
            p["retryable_write_errors_only_winerror"],
            [5, 32],
        )
        self.assertEqual(
            p["retry_deadline_seconds"],
            5.0,
        )
        self.assertTrue(
            p[
                "reader_retry_must_preserve_p5c3r2_eacces_semantics"
            ]
        )

    def test_target_is_verified_before_current_tmp(self) -> None:
        order = self.contract["operation_order"]
        self.assertLess(
            order.index("VERIFY_COMPLETE_TARGET"),
            order.index(
                "CREATE_AND_VERIFY_CURRENT_TMP_EXCLUSIVELY"
            ),
        )
        self.assertLess(
            order.index(
                "READ_AFTER_WRITE_VERIFY_CURRENT_AND_TARGET"
            ),
            order.index(
                "PERSIST_PHYSICAL_PUBLICATION_RECEIPT"
            ),
        )
        self.assertLess(
            order.index(
                "PERSIST_PHYSICAL_PUBLICATION_RECEIPT"
            ),
            order.index(
                "EMIT_P5D2_PROMOTION_CONFIRMED"
            ),
        )

    def test_physical_and_logical_success_are_not_laundered(
        self,
    ) -> None:
        o = self.contract[
            "physical_logical_ordering"
        ]
        self.assertTrue(
            o[
                "physical_publication_verified_before_promotion_confirmed"
            ]
        )
        self.assertTrue(
            o[
                "physical_receipt_persisted_before_promotion_confirmed"
            ]
        )
        self.assertTrue(
            o[
                "physical_success_logical_pending_is_distinct_terminal_recovery_state"
            ]
        )
        self.assertTrue(
            o[
                "duplicate_promotion_confirmed_for_same_transaction_forbidden"
            ]
        )

    def test_evidence_is_append_only_and_outside_live_vault(
        self,
    ) -> None:
        e = self.contract["evidence"]
        self.assertTrue(
            e["evidence_must_be_outside_real_vault"]
        )
        self.assertTrue(
            e["append_only_required"]
        )
        self.assertGreaterEqual(
            len(e["required_identity_bindings"]),
            7,
        )

    def test_crash_recovery_is_state_based_and_forward_completes_new_current(
        self,
    ) -> None:
        r = self.contract["crash_recovery"]
        self.assertTrue(r["required"])
        self.assertGreaterEqual(
            len(r["crash_points"]),
            6,
        )
        self.assertTrue(
            r[
                "current_and_target_must_be_reinspected_before_any_recovery_action"
            ]
        )
        self.assertTrue(
            r[
                "if_current_is_new_and_target_exact_forward_completion_required"
            ]
        )
        self.assertTrue(
            r[
                "last_known_good_generation_must_not_be_deleted"
            ]
        )

    def test_rollback_is_bounded_to_exact_previous_current(
        self,
    ) -> None:
        r = self.contract["rollback"]
        self.assertTrue(r["replace_mode_only"])
        self.assertTrue(
            r["exact_previous_current_bytes_required"]
        )
        self.assertTrue(
            r[
                "exact_previous_current_target_must_verify"
            ]
        )
        self.assertTrue(
            r[
                "rollback_must_not_emit_promotion_confirmed_for_failed_candidate"
            ]
        )

    def test_success_semantics_distinguish_physical_pending_and_final(
        self,
    ) -> None:
        s = self.contract["success_semantics"]
        self.assertEqual(
            s["physical_success_status"],
            "PASS_PHYSICAL_LIVE_PUBLICATION_VERIFIED",
        )
        self.assertEqual(
            s["logical_pending_status"],
            "PASS_PHYSICAL_PUBLICATION_LOGICAL_CONFIRMATION_PENDING",
        )
        self.assertEqual(
            s["final_success_status"],
            "PASS_LIVE_PUBLICATION_CONFIRMED",
        )
        self.assertFalse(
            s["automatic_publication_authorized"]
        )
        self.assertFalse(
            s["background_observer_authorized"]
        )

    def test_contract_authorizes_no_runtime_or_live_write(
        self,
    ) -> None:
        b = self.contract["p5d3g_boundary"]
        self.assertTrue(b["contract_tests_only"])
        for field in (
            "live_publication_runtime_implementation_authorized",
            "sacrificial_live_vault_execution_authorized",
            "production_live_vault_execution_authorized",
            "real_vault_write_authorized",
            "current_pointer_creation_authorized",
            "current_pointer_mutation_authorized",
            "p5d2_promotion_confirmed_event_authorized",
            "automatic_publication_authorized",
            "background_observer_authorized",
            "polling_loop_authorized",
            "windows_startup_registration_authorized",
            "scheduled_task_authorized",
            "windows_service_authorized",
            "graph_search_current_semantics_authorized",
        ):
            with self.subTest(field=field):
                self.assertFalse(b[field])

    def test_breakers_are_unique_and_cover_critical_crossings(
        self,
    ) -> None:
        breakers = self.contract[
            "required_breakers"
        ]
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )
        self.assertGreaterEqual(
            len(breakers),
            75,
        )
        required = {
            "human authorization omitted",
            "single-writer ownership omitted",
            "synthetic GEN_A GEN_B restriction treated as production authority",
            "sealed P5D3F package mutated during materialization",
            "CURRENT.tmp created before target verification",
            "PROMOTION_CONFIRMED emitted before physical verification",
            "rollback emits PROMOTION_CONFIRMED for failed candidate",
            "background observer introduced",
            "Graph/Search CURRENT semantics claimed",
            "P5D4 name reused for finite publication",
        }
        self.assertTrue(
            required.issubset(set(breakers))
        )

    def test_next_gate_is_implementation_not_p5d4(
        self,
    ) -> None:
        gates = self.contract["next_gates"]
        self.assertEqual(
            gates["p5d3g_implementation"],
            "FINITE_LIVE_PUBLICATION_TRANSACTION_IMPLEMENTATION_AND_SACRIFICIAL_LIVE_VAULT_QUALIFICATION",
        )
        self.assertEqual(
            gates["p5d4"],
            "BOUNDED_OBSERVER_LOOP_CANDIDATE",
        )
        self.assertEqual(
            gates["p6"],
            "CONTROLLED_KNOWLEDGE_GRAPH_ARCHITECTURE",
        )


if __name__ == "__main__":
    unittest.main()
