from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


CONTRACT_PATH = (
    Path(__file__).resolve().parents[2]
    / "tools"
    / "obsidian_projection"
    / "persistent_production_handoff_gate_contract_v0_2.json"
)
EXPECTED_CONTRACT_BLOB = (
    "aef627936b6f745017bcace7e8a3e44270f95674"
)


def _git_blob_sha1(raw: bytes) -> str:
    header = (
        f"blob {len(raw)}\0"
    ).encode("ascii")
    return hashlib.sha1(
        header + raw
    ).hexdigest()


class P5D3FPersistentHandoffRecoveryContractV02Tests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CONTRACT_PATH.read_bytes()
        cls.contract = json.loads(
            cls.raw.decode("utf-8")
        )

    def test_contract_blob_is_exact(self) -> None:
        self.assertEqual(
            _git_blob_sha1(self.raw),
            EXPECTED_CONTRACT_BLOB,
        )

    def test_schema_and_prior_contract_are_exact(self) -> None:
        self.assertEqual(
            self.contract["schema"],
            "ATDS_OBSIDIAN_P5D3F_PERSISTENT_PRODUCTION_HANDOFF_GATE_CONTRACT_V0_2",
        )
        self.assertEqual(
            self.contract[
                "prior_contract"
            ]["blob"],
            "59ce9e079d256799d072405fa4a623ba58b75c0d",
        )
        self.assertEqual(
            self.contract[
                "prior_contract"
            ]["relation"],
            "NARROW_RECOVERY_AMENDMENT_ONLY",
        )

    def test_only_exact_empty_packages_residual_is_recoverable(
        self,
    ) -> None:
        recovery = self.contract[
            "recovery_basis"
        ]
        self.assertEqual(
            recovery["observed_persistent_state"],
            "PRESENT_EMPTY_PACKAGES",
        )
        self.assertEqual(
            recovery["required_top_level"],
            ["packages"],
        )
        self.assertTrue(
            recovery["packages_must_be_directory"]
        )
        self.assertTrue(
            recovery["packages_must_be_empty"]
        )
        self.assertTrue(
            recovery[
                "promotion_handoff_record_must_be_absent"
            ]
        )
        self.assertTrue(
            recovery[
                "no_other_top_level_entries"
            ]
        )

    def test_setup_authority_allows_no_general_nonempty_staging(
        self,
    ) -> None:
        setup = self.contract[
            "setup_authority"
        ]
        self.assertEqual(
            setup[
                "preexisting_nonempty_staging_root"
            ],
            "BLOCK_UNLESS_EXACT_PRIOR_GATE_STATE",
        )
        self.assertEqual(
            setup[
                "preexisting_packages_root_without_exact_verified_handoff"
            ],
            "BLOCK_UNLESS_EXACT_EMPTY_PACKAGES_RECOVERY_STATE",
        )
        self.assertTrue(
            setup[
                "exact_empty_packages_recovery_state_allowed"
            ]
        )
        self.assertTrue(
            setup[
                "recovery_state_may_not_be_deleted_or_normalized"
            ]
        )

    def test_body_failure_cannot_be_masked_by_cleanup(self) -> None:
        execution = self.contract[
            "execution"
        ]
        self.assertTrue(
            execution[
                "temporary_cleanup_may_not_mask_body_failure"
            ]
        )
        self.assertTrue(
            execution[
                "body_failure_must_preserve_temporary_roots"
            ]
        )
        self.assertTrue(
            execution[
                "body_failure_original_exception_must_remain_primary"
            ]
        )

    def test_post_success_cleanup_failure_is_distinct(self) -> None:
        execution = self.contract[
            "execution"
        ]
        self.assertTrue(
            execution[
                "post_success_cleanup_failure_must_be_distinct"
            ]
        )
        self.assertTrue(
            execution[
                "post_success_cleanup_failure_must_preserve_handoff_evidence"
            ]
        )

    def test_failure_semantics_are_fail_closed(self) -> None:
        failure = self.contract[
            "failure_semantics"
        ]
        self.assertEqual(
            failure["cleanup_failure"],
            "BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS_ONLY",
        )
        self.assertEqual(
            failure[
                "body_failure_cleanup_policy"
            ],
            "PRESERVE_TEMP_ROOT_AND_ORIGINAL_EXCEPTION",
        )
        self.assertEqual(
            failure[
                "exact_empty_packages_recovery_state"
            ],
            "ALLOW_AS_EXACT_PRIOR_GATE_STATE",
        )

    def test_execution_authority_remains_closed(self) -> None:
        boundary = self.contract[
            "boundary"
        ]
        self.assertTrue(
            boundary["contract_tests_only"]
        )
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
            self.assertFalse(
                boundary[field],
                field,
            )

    def test_new_recovery_breakers_are_present_and_unique(
        self,
    ) -> None:
        breakers = self.contract[
            "required_breakers"
        ]
        self.assertEqual(
            len(breakers),
            len(set(breakers)),
        )
        for breaker in (
            "EMPTY_PACKAGES_RECOVERY_EXTRA_TOP_LEVEL_ENTRY",
            "EMPTY_PACKAGES_RECOVERY_NONEMPTY_PACKAGES",
            "EMPTY_PACKAGES_RECOVERY_HANDOFF_RECORD_PRESENT",
            "BODY_FAILURE_MASKED_BY_TEMP_CLEANUP",
            "BODY_FAILURE_TEMP_ROOT_DELETED",
            "POST_SUCCESS_CLEANUP_FAILURE_AMBIGUOUS_HANDOFF_STATE",
        ):
            self.assertIn(
                breaker,
                breakers,
            )

    def test_next_gate_is_recovery_implementation_v03(
        self,
    ) -> None:
        self.assertEqual(
            self.contract[
                "next_gate"
            ][
                "after_contract_qualification"
            ],
            "P5-D3F-PERSISTENT-HANDOFF-RECOVERY-IMPLEMENTATION-V0.3",
        )
        self.assertTrue(
            self.contract[
                "next_gate"
            ][
                "mandatory_stop_after_persistent_handoff"
            ]
        )


if __name__ == "__main__":
    unittest.main()
