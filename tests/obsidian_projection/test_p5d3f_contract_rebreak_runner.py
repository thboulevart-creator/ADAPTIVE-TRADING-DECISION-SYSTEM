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
