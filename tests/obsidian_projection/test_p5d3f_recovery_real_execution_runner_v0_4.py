from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection import (
    p5d3f_recovery_real_execution_v0_4 as runner,
)
from tools.obsidian_projection.persistent_production_handoff import (
    PersistentHandoffPostSuccessCleanupBlockedError,
)


AUTHORIZED_HEAD = (
    "fda1d9724165192385fed1c22817d9c33334fde8"
)
OTHER_HEAD = (
    "f05707250f7d33c9ecf998ddb7123d5e345280c9"
)


class P5D3FRecoveryRealExecutionRunnerV04Tests(
    unittest.TestCase
):
    def test_runner_branch_is_exact_v04(self) -> None:
        self.assertEqual(
            runner.RUNNER_BRANCH,
            "feat/obsidian-projection-p5d3f-recovery-real-execution-runner-v0.4-monitored-head-pin",
        )
        self.assertEqual(
            runner.MONITORED_BRANCH,
            "integration/system-v1",
        )

    def test_recovery_authority_pins_remain_exact(self) -> None:
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

    def test_expected_monitored_head_accepts_exact_remote(self) -> None:
        ref = (
            "refs/heads/integration/system-v1"
        )
        with patch.object(
            runner,
            "_git",
            return_value=(
                AUTHORIZED_HEAD
                + "\t"
                + ref
            ),
        ):
            runner._verify_expected_monitored_head(
                Path("."),
                AUTHORIZED_HEAD,
            )

    def test_expected_monitored_head_rejects_changed_remote(self) -> None:
        ref = (
            "refs/heads/integration/system-v1"
        )
        with patch.object(
            runner,
            "_git",
            return_value=(
                OTHER_HEAD
                + "\t"
                + ref
            ),
        ):
            with self.assertRaisesRegex(
                runner.RealExecutionRunnerError,
                "BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH",
            ):
                runner._verify_expected_monitored_head(
                    Path("."),
                    AUTHORIZED_HEAD,
                )

    def test_success_validator_requires_authorized_candidate_head(
        self,
    ) -> None:
        valid = {
            "status":
                "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
            "candidate_head": AUTHORIZED_HEAD,
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
            valid,
            AUTHORIZED_HEAD,
        )

        wrong = json.loads(
            json.dumps(valid)
        )
        wrong["candidate_head"] = OTHER_HEAD

        with self.assertRaises(
            runner.RealExecutionRunnerError
        ):
            runner._validate_final_success_result(
                wrong,
                AUTHORIZED_HEAD,
            )

    def test_post_success_cleanup_block_revalidates_authorized_head(
        self,
    ) -> None:
        success = {
            "status":
                "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
            "candidate_head": AUTHORIZED_HEAD,
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

        details = (
            runner._post_success_cleanup_block_details(
                exc,
                AUTHORIZED_HEAD,
            )
        )

        self.assertEqual(
            details["success_result"]["candidate_head"],
            AUTHORIZED_HEAD,
        )

        exc.p5d3f_success_result = {
            **success,
            "candidate_head": OTHER_HEAD,
        }
        with self.assertRaises(
            runner.RealExecutionRunnerError
        ):
            runner._post_success_cleanup_block_details(
                exc,
                AUTHORIZED_HEAD,
            )

    def test_failure_snapshot_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-v04-residual-"
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

            self.assertTrue(
                residual.exists()
            )
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

    def test_source_requires_explicit_monitored_head_binding(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_recovery_real_execution_v0_4.py"
        ).read_text(encoding="utf-8")

        for token in (
            "--expected-monitored-head",
            "BLOCKED_MONITORED_HEAD_AUTHORITY_MISMATCH",
            "P5D3F_EXPECTED_MONITORED_HEAD=",
            "P5D3F_MONITORED_HEAD_AUTHORITY=PASS",
            "result candidate head differs from authorized monitored head",
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
            / "p5d3f_recovery_real_execution_v0_4.py"
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
