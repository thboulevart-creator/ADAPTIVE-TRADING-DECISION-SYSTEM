from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection import (
    p5d3f_persistent_production_handoff_real_execution as runner,
)


class P5D3FPersistentRealExecutionRunnerTests(
    unittest.TestCase
):
    def test_authorization_literal_is_exact_and_narrow(self) -> None:
        self.assertEqual(
            runner.AUTHORIZATION_LITERAL,
            "AUTHORIZE_ONE_P5D3F_PERSISTENT_READY_UNAUTHORIZED_HANDOFF",
        )

    def test_runner_branch_is_exact(self) -> None:
        self.assertEqual(
            runner.RUNNER_BRANCH,
            "feat/obsidian-projection-p5d3f-persistent-real-execution-failure-preservation-v0.2",
        )

    def test_runtime_authority_pins_are_exact(self) -> None:
        self.assertEqual(
            runner.EXPECTED_IMPLEMENTATION_BLOB,
            "d2f40c8b2c8fb06b37bb34442c59d78222046452",
        )
        self.assertEqual(
            runner.EXPECTED_TEST_BLOB,
            "7da1fadeb1b3e9efee54b7ca09f0735277af345c",
        )
        self.assertEqual(
            runner.EXPECTED_GATE_CONTRACT_BLOB,
            "59ce9e079d256799d072405fa4a623ba58b75c0d",
        )
        self.assertEqual(
            runner.EXPECTED_QUALIFIED_P5D3F_BLOB,
            "2108131914cf65bb076b80f5bb63cd63267567fa",
        )

    def test_normalize_origin_accepts_expected_https(self) -> None:
        self.assertEqual(
            runner._normalize_origin(
                "https://github.com/"
                "thboulevart-creator/"
                "ADAPTIVE-TRADING-DECISION-SYSTEM.git"
            ),
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )

    def test_residual_snapshot_preserves_empty_staging(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-empty-"
        ) as temp:
            root = Path(temp)
            staging = root / "staging"
            staging.mkdir()

            snapshot = runner._snapshot_staging_residual(
                staging
            )

            self.assertTrue(staging.exists())
            self.assertEqual(
                snapshot["state"],
                "PRESENT_EMPTY",
            )
            self.assertEqual(
                snapshot["entries"],
                [],
            )

    def test_residual_snapshot_preserves_nonempty_evidence(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-residual-"
        ) as temp:
            root = Path(temp)
            staging = root / "staging"
            staging.mkdir()
            packages = staging / "packages"
            packages.mkdir()
            residual = packages / "residual.txt"
            residual.write_bytes(b"EVIDENCE\n")

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
                        "path": "packages/residual.txt",
                        "type": "FILE",
                        "size": 9,
                    },
                ],
            )

    def test_residual_snapshot_reports_absent_without_creation(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-absent-"
        ) as temp:
            staging = Path(temp) / "staging"

            snapshot = runner._snapshot_staging_residual(
                staging
            )

            self.assertFalse(staging.exists())
            self.assertEqual(
                snapshot["state"],
                "ABSENT",
            )
            self.assertFalse(
                snapshot["exists"]
            )

    def test_failure_path_contains_no_cleanup_delete(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_persistent_production_handoff_real_execution.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "P5D3F_PERSISTENT_FAILURE_ORIGINAL=",
            source,
        )
        self.assertIn(
            "P5D3F_PERSISTENT_FAILURE_RESIDUAL_JSON=",
            source,
        )
        self.assertNotIn(
            "staging.rmdir()",
            source,
        )
        self.assertNotIn(
            "packages.rmdir()",
            source,
        )

    def test_source_requires_explicit_runner_blob_binding(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_persistent_production_handoff_real_execution.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "--expected-runner-blob",
            source,
        )
        self.assertIn(
            "governed runner committed blob mismatch",
            source,
        )
        self.assertIn(
            "governed runner worktree blob mismatch",
            source,
        )

    def test_source_has_no_live_publication_or_later_authority_call(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_persistent_production_handoff_real_execution.py"
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
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
