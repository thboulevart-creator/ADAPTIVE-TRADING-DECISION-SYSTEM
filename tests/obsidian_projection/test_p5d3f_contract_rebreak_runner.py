from __future__ import annotations

import os
import tempfile
import unittest
from unittest import mock
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

    def test_historical_raw_byte_pinned_dependencies_are_in_compatibility_surface(
        self,
    ) -> None:
        required = {
            "tools/obsidian_projection/materialization_contract_v0_1.json",
            "tools/obsidian_projection/materialize.py",
            "tools/obsidian_projection/rendering.py",
            "tools/obsidian_projection/relations.py",
            "tools/obsidian_projection/integrity.py",
            "tools/obsidian_projection/builder.py",
            "tools/obsidian_projection/p2_verify.py",
        }

        self.assertTrue(
            required.issubset(
                set(
                    p5d3f_contract_rebreak.
                    BYTE_PIN_COMPATIBILITY_PATHS
                )
            )
        )

    def test_lf_checkout_policy_and_byte_pins_are_canonical(
        self,
    ) -> None:
        repo = p5d3f_contract_rebreak._repo_root()

        self.assertEqual(
            p5d3f_contract_rebreak._committed_blob(
                repo,
                ".gitattributes",
            ),
            p5d3f_contract_rebreak.EXPECTED_GITATTRIBUTES_BLOB,
        )

        for relative in (
            p5d3f_contract_rebreak.BYTE_PIN_COMPATIBILITY_PATHS
        ):
            with self.subTest(relative=relative):
                self.assertEqual(
                    p5d3f_contract_rebreak._raw_worktree_blob(
                        repo,
                        relative,
                    ),
                    p5d3f_contract_rebreak._committed_blob(
                        repo,
                        relative,
                    ),
                )

    def test_exact_blob_materialization_restores_committed_bytes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            init = p5d3f_contract_rebreak.subprocess.run(
                ["git", "init"],
                cwd=str(repo),
                check=False,
                capture_output=True,
            )
            self.assertEqual(init.returncode, 0)

            p5d3f_contract_rebreak.subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=str(repo),
                check=True,
            )
            p5d3f_contract_rebreak.subprocess.run(
                ["git", "config", "user.name", "ATDS Test"],
                cwd=str(repo),
                check=True,
            )

            sample = repo / "sample.txt"
            sample.write_bytes(b"alpha\nbeta\n")

            p5d3f_contract_rebreak.subprocess.run(
                ["git", "add", "sample.txt"],
                cwd=str(repo),
                check=True,
            )
            p5d3f_contract_rebreak.subprocess.run(
                ["git", "commit", "-m", "fixture"],
                cwd=str(repo),
                check=True,
                capture_output=True,
            )

            sample.write_bytes(b"alpha\r\nbeta\r\n")

            self.assertNotEqual(
                p5d3f_contract_rebreak._raw_worktree_blob(
                    repo,
                    "sample.txt",
                ),
                p5d3f_contract_rebreak._committed_blob(
                    repo,
                    "sample.txt",
                ),
            )

            p5d3f_contract_rebreak._write_committed_blob_exact(
                repo,
                "sample.txt",
            )

            self.assertEqual(
                sample.read_bytes(),
                b"alpha\nbeta\n",
            )
            self.assertEqual(
                p5d3f_contract_rebreak._raw_worktree_blob(
                    repo,
                    "sample.txt",
                ),
                p5d3f_contract_rebreak._committed_blob(
                    repo,
                    "sample.txt",
                ),
            )

    def test_index_stat_refresh_accepts_observed_return_one_when_index_unchanged(
        self,
    ) -> None:
        fake_refresh = (
            p5d3f_contract_rebreak.subprocess.CompletedProcess(
                args=["git", "update-index", "--really-refresh"],
                returncode=1,
                stdout="sample.txt: needs update\n",
                stderr="",
            )
        )

        with (
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_index_stage_snapshot",
                side_effect=["a" * 40, "a" * 40],
            ),
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_git",
                return_value=fake_refresh,
            ),
        ):
            p5d3f_contract_rebreak._refresh_index_stat_cache(
                Path(".")
            )

    def test_index_stat_refresh_is_individually_pathscoped(
        self,
    ) -> None:
        fake_refresh = (
            p5d3f_contract_rebreak.subprocess.CompletedProcess(
                args=["git", "update-index", "--really-refresh"],
                returncode=1,
                stdout="sample.txt: needs update\n",
                stderr="",
            )
        )

        with (
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_index_stage_snapshot",
                side_effect=["a" * 40, "a" * 40],
            ),
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_git",
                return_value=fake_refresh,
            ) as git_mock,
        ):
            p5d3f_contract_rebreak._refresh_index_stat_cache(
                Path(".")
            )

        self.assertEqual(
            git_mock.call_args_list,
            [
                mock.call(
                    Path("."),
                    "update-index",
                    "--really-refresh",
                    "--",
                    relative,
                )
                for relative in (
                    p5d3f_contract_rebreak.
                    BYTE_PIN_COMPATIBILITY_PATHS
                )
            ],
        )

    def test_index_stat_refresh_rejects_index_stage_mutation(
        self,
    ) -> None:
        fake_refresh = (
            p5d3f_contract_rebreak.subprocess.CompletedProcess(
                args=["git", "update-index", "--really-refresh"],
                returncode=0,
                stdout="",
                stderr="",
            )
        )

        with (
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_index_stage_snapshot",
                side_effect=["a" * 40, "b" * 40],
            ),
            mock.patch.object(
                p5d3f_contract_rebreak,
                "_git",
                return_value=fake_refresh,
            ),
        ):
            with self.assertRaises(
                p5d3f_contract_rebreak.GovernedRunError
            ):
                p5d3f_contract_rebreak._refresh_index_stat_cache(
                    Path(".")
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
