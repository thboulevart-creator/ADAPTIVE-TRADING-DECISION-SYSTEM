from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection import p5d3f_contract_rebreak


class P5D3FContractRebreakRunnerTests(unittest.TestCase):
    def test_repo_root_is_derived_from_runner_not_cwd(self) -> None:
        expected = Path(
            p5d3f_contract_rebreak.__file__
        ).resolve().parents[2]

        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as td:
            os.chdir(td)
            try:
                observed = (
                    p5d3f_contract_rebreak._repo_root()
                )
            finally:
                os.chdir(previous)

        self.assertEqual(observed, expected)


    def test_committed_contract_blob_uses_git_authority(self) -> None:
        repo = p5d3f_contract_rebreak._repo_root()
        observed = (
            p5d3f_contract_rebreak._committed_blob(
                repo,
                "tools/obsidian_projection/"
                "promotion_handoff_contract_v0_1.json",
            )
        )
        self.assertEqual(
            observed,
            p5d3f_contract_rebreak.EXPECTED_CONTRACT_BLOB,
        )

    def test_reexec_argv_reloads_runner_from_target_checkout(
        self,
    ) -> None:
        repo = p5d3f_contract_rebreak._repo_root()
        argv = p5d3f_contract_rebreak._build_reexec_argv(
            repo,
            original_argv=[
                "old-runner.py",
                "--expected-remote-head",
                "a" * 40,
                "--expected-candidate-head",
                "b" * 40,
            ],
            dont_write_bytecode=True,
        )
        self.assertEqual(argv[0], p5d3f_contract_rebreak.sys.executable)
        self.assertEqual(argv[1], "-B")
        self.assertEqual(
            Path(argv[2]),
            repo
            / "tools"
            / "obsidian_projection"
            / "p5d3f_contract_rebreak.py",
        )
        self.assertEqual(
            argv[3:],
            [
                "--expected-remote-head",
                "a" * 40,
                "--expected-candidate-head",
                "b" * 40,
            ],
        )

    def test_origin_normalization_accepts_supported_github_forms(
        self,
    ) -> None:
        expected = (
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM"
        )

        for value in (
            "https://github.com/"
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM.git",
            "git@github.com:"
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM.git",
            "ssh://git@github.com/"
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM.git",
        ):
            with self.subTest(value=value):
                self.assertEqual(
                    p5d3f_contract_rebreak._normalize_origin(
                        value
                    ),
                    expected,
                )

    def test_origin_normalization_rejects_unknown_form(self) -> None:
        with self.assertRaises(
            p5d3f_contract_rebreak.GovernedRunError
        ):
            p5d3f_contract_rebreak._normalize_origin(
                "C:/Users/Boulevart"
            )


if __name__ == "__main__":
    unittest.main()
