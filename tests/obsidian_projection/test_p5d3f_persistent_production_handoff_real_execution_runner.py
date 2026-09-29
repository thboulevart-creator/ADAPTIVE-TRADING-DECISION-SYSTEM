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
            "feat/obsidian-projection-p5d3f-persistent-production-handoff-real-execution-v0.1",
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

    def test_cleanup_removes_empty_staging_created_by_run(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-empty-"
        ) as temp:
            root = Path(temp)
            staging = root / "staging"
            staging.mkdir()

            runner._cleanup_empty_staging_after_failure(
                staging,
                "ABSENT",
            )

            self.assertFalse(staging.exists())

    def test_cleanup_restores_empty_preexisting_staging(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-preexisting-"
        ) as temp:
            root = Path(temp)
            staging = root / "staging"
            staging.mkdir()
            packages = staging / "packages"
            packages.mkdir()

            runner._cleanup_empty_staging_after_failure(
                staging,
                "PRESENT_EMPTY",
            )

            self.assertTrue(staging.is_dir())
            self.assertEqual(
                list(staging.iterdir()),
                [],
            )

    def test_cleanup_refuses_nonempty_residual(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-real-runner-residual-"
        ) as temp:
            root = Path(temp)
            staging = root / "staging"
            staging.mkdir()
            packages = staging / "packages"
            packages.mkdir()
            residual = packages / "residual"
            residual.mkdir()

            with self.assertRaises(
                runner.RealExecutionRunnerError
            ):
                runner._cleanup_empty_staging_after_failure(
                    staging,
                    "ABSENT",
                )

            self.assertTrue(residual.exists())

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
