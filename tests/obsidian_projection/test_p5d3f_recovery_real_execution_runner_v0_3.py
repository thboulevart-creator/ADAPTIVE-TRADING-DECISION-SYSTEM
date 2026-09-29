from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection import (
    p5d3f_recovery_real_execution_v0_3 as runner,
)
from tools.obsidian_projection.persistent_production_handoff import (
    PersistentHandoffPostSuccessCleanupBlockedError,
)


class P5D3FRecoveryRealExecutionRunnerV03Tests(
    unittest.TestCase
):
    def test_runner_branch_is_exact_v03(self) -> None:
        self.assertEqual(
            runner.RUNNER_BRANCH,
            "feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.3",
        )

    def test_recovery_authority_pins_are_exact(self) -> None:
        self.assertEqual(
            runner.EXPECTED_IMPLEMENTATION_BLOB,
            "dcd70a9d9794675eab90e41df560f8b030b5dbf3",
        )
        self.assertEqual(
            runner.EXPECTED_RECOVERY_IMPLEMENTATION_TEST_BLOB,
            "242305bc0f95bbe243158b5c806255508093a357",
        )
        self.assertEqual(
            runner.EXPECTED_RECOVERY_GATE_CONTRACT_BLOB,
            "aef627936b6f745017bcace7e8a3e44270f95674",
        )
        self.assertEqual(
            runner.EXPECTED_GATE_CONTRACT_BLOB,
            "59ce9e079d256799d072405fa4a623ba58b75c0d",
        )
        self.assertEqual(
            runner.EXPECTED_QUALIFIED_P5D3F_BLOB,
            "2108131914cf65bb076b80f5bb63cd63267567fa",
        )

    def test_only_exact_recovery_prestate_is_authorized(self) -> None:
        self.assertEqual(
            runner.AUTHORIZED_STAGING_PRESTATE,
            "PRESENT_EMPTY_PACKAGES_RECOVERY",
        )
        runner._require_authorized_prestate(
            "PRESENT_EMPTY_PACKAGES_RECOVERY"
        )
        for other in (
            "ABSENT",
            "PRESENT_EMPTY",
            "PRESENT_NONEMPTY",
        ):
            with self.assertRaises(
                runner.RealExecutionRunnerError
            ):
                runner._require_authorized_prestate(
                    other
                )

    def test_authorization_literal_remains_narrow(self) -> None:
        self.assertEqual(
            runner.AUTHORIZATION_LITERAL,
            "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF",
        )

    def test_failure_snapshot_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-v03-residual-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            packages = staging / "packages"
            packages.mkdir()
            residual = packages / "evidence.txt"
            residual.write_bytes(
                b"evidence\n"
            )

            snapshot = runner._snapshot_staging_residual(
                staging
            )

            self.assertTrue(residual.exists())
            self.assertEqual(
                snapshot["state"],
                "PRESENT_NONEMPTY",
            )
            self.assertEqual(
                snapshot["entries"],
                [
                    {
                        "path": "packages",
                        "type": "DIRECTORY",
                    },
                    {
                        "path": "packages/evidence.txt",
                        "type": "FILE",
                        "size": 9,
                    },
                ],
            )

    def test_post_success_cleanup_block_extracts_bound_result(
        self,
    ) -> None:
        success = {
            "status":
                "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
            "generation_id": "gen-test",
            "zero_mutation_proof": {
                "status":
                    "PASS_REAL_VAULT_ZERO_MUTATION",
                "unchanged": True,
            },
            "publication_authorized": False,
            "live_publication_executed": False,
            "mandatory_stop": True,
        }
        exc = (
            PersistentHandoffPostSuccessCleanupBlockedError(
                "BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS"
            )
        )
        exc.p5d3f_temp_root = r"C:\Temp\surviving"
        exc.p5d3f_success_result = success

        extracted = (
            runner._post_success_cleanup_block_details(
                exc
            )
        )

        self.assertEqual(
            extracted["temp_root"],
            r"C:\Temp\surviving",
        )
        self.assertEqual(
            extracted["success_result"],
            success,
        )

    def test_post_success_cleanup_block_requires_valid_success_result(
        self,
    ) -> None:
        exc = (
            PersistentHandoffPostSuccessCleanupBlockedError(
                "BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS"
            )
        )
        exc.p5d3f_temp_root = r"C:\Temp\surviving"
        exc.p5d3f_success_result = {
            "status": "WRONG",
        }

        with self.assertRaises(
            runner.RealExecutionRunnerError
        ):
            runner._post_success_cleanup_block_details(
                exc
            )

    def test_success_validator_requires_zero_mutation(self) -> None:
        valid = {
            "status":
                "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
            "publication_authorized": False,
            "live_publication_executed": False,
            "mandatory_stop": True,
            "zero_mutation_proof": {
                "status":
                    "PASS_REAL_VAULT_ZERO_MUTATION",
                "unchanged": True,
            },
        }
        runner._validate_final_success_result(
            valid
        )

        invalid = json.loads(
            json.dumps(valid)
        )
        invalid[
            "zero_mutation_proof"
        ]["unchanged"] = False
        with self.assertRaises(
            runner.RealExecutionRunnerError
        ):
            runner._validate_final_success_result(
                invalid
            )

    def test_source_preserves_failure_and_cleanup_block_markers(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_recovery_real_execution_v0_3.py"
        ).read_text(encoding="utf-8")

        for token in (
            "P5D3F_PERSISTENT_FAILURE_ORIGINAL=",
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON=",
            "P5D3F_POST_SUCCESS_CLEANUP_BLOCKED=TRUE",
            "P5D3F_POST_SUCCESS_RESULT_JSON=",
            "P5D3F_POST_SUCCESS_TEMP_ROOT=",
        ):
            self.assertIn(
                token,
                source,
            )

    def test_no_later_authority_surface(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_recovery_real_execution_v0_3.py"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "consume_stage_a_plan_approval",
            "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
            "os.replace(",
            "threading.Thread",
            "while True",
            "schtasks",
            "CreateService",
        ):
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
