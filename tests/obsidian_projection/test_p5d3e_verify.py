from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.p5d3e_verify import (
    CANONICAL_ORIGIN,
    REMOTE_TRACKING_REF,
    RealExactHeadSandboxGovernanceError,
    resolve_real_candidate,
    run_pre_resolved_sandbox,
)


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return completed.stdout.strip()


def _make_control_repo(root: Path) -> tuple[Path, str, str]:
    repo = root / "control"
    repo.mkdir()

    _git(repo, "init")
    _git(repo, "config", "user.email", "p5d3e@example.invalid")
    _git(repo, "config", "user.name", "P5-D3E Test")
    _git(repo, "remote", "add", "origin", CANONICAL_ORIGIN)

    (repo / "docs").mkdir()
    (repo / "data").mkdir()
    (repo / "src").mkdir()
    (repo / "assets").mkdir()

    (repo / "docs" / "source.md").write_bytes(
        b"# Source\n\nBinary target: `assets/blob.bin`\n"
    )
    (repo / "data" / "refs.json").write_bytes(
        b'{"reference":"docs/source.md"}\n'
    )
    (repo / "src" / "code.py").write_bytes(
        b"VALUE = 1\n"
    )
    (repo / "assets" / "blob.bin").write_bytes(
        b"\x00\x01\x02\x03"
    )

    _git(repo, "add", "--all")
    _git(repo, "commit", "-m", "p5d3e synthetic control")

    head = _git(repo, "rev-parse", "HEAD")
    tree = _git(repo, "rev-parse", "HEAD^{tree}")

    _git(
        repo,
        "update-ref",
        REMOTE_TRACKING_REF,
        head,
    )
    return repo, head, tree


class P5D3EVerifyTests(unittest.TestCase):
    def test_pre_resolved_sandbox_exercises_full_qualified_core(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3e-test-"
        ) as temp:
            root = Path(temp)
            control, head, tree = _make_control_repo(root)
            vault = root / "real-vault"
            vault.mkdir()
            (vault / "sentinel.txt").write_text(
                "UNCHANGED\n",
                encoding="utf-8",
            )

            report = run_pre_resolved_sandbox(
                control_repo_root=control,
                candidate_head=head,
                candidate_tree=tree,
                real_vault_root=vault,
                candidate_resolution_network_fetch_performed=False,
                real_candidate_evaluated=False,
            )

            self.assertEqual(
                report["status"],
                "PASS_SYNTHETIC_PRE_RESOLVED_SANDBOX",
            )
            self.assertEqual(
                report["candidate_outcome"],
                "QUALIFIED",
            )
            self.assertEqual(
                report[
                    "candidate_generation_verification_status"
                ],
                "PASS_SEALED_UNPROMOTED",
            )
            self.assertEqual(
                report["source_record_count"],
                4,
            )
            self.assertEqual(
                report["artifact_record_count"],
                4,
            )
            self.assertEqual(
                report["metadata_only_count"],
                1,
            )
            self.assertEqual(
                report["metadata_only_body_read_count"],
                0,
            )
            self.assertEqual(
                report["relation_record_count"],
                2,
            )
            self.assertEqual(
                report["relation_source_body_read_count"],
                2,
            )
            self.assertTrue(
                report["p5d2_result_event_emitted"]
            )
            self.assertTrue(
                report["live_projection_head_unchanged"]
            )
            self.assertFalse(
                report[
                    "candidate_resolution_network_fetch_performed"
                ]
            )
            self.assertFalse(
                report["evaluation_network_fetch_performed"]
            )
            self.assertFalse(
                report["real_candidate_evaluated"]
            )
            self.assertFalse(
                report["candidate_repository_retained"]
            )
            self.assertFalse(
                report["evaluation_workspace_retained"]
            )
            self.assertEqual(
                (vault / "sentinel.txt").read_text(
                    encoding="utf-8"
                ),
                "UNCHANGED\n",
            )

    def test_pre_resolved_candidate_must_equal_remote_tracking_ref(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3e-test-"
        ) as temp:
            root = Path(temp)
            control, _head, tree = _make_control_repo(root)
            vault = root / "real-vault"
            vault.mkdir()

            with self.assertRaises(
                RealExactHeadSandboxGovernanceError
            ):
                run_pre_resolved_sandbox(
                    control_repo_root=control,
                    candidate_head="a" * 40,
                    candidate_tree=tree,
                    real_vault_root=vault,
                    candidate_resolution_network_fetch_performed=False,
                    real_candidate_evaluated=False,
                )

    def test_resolver_uses_exact_single_governed_fetch(self) -> None:
        calls: list[tuple[str, ...]] = []
        head = "1" * 40
        tree = "2" * 40

        def fake_git(
            _repo: Path,
            *args: str,
        ) -> str:
            calls.append(tuple(args))
            if args[:2] == (
                "status",
                "--porcelain",
            ):
                return ""
            if args == (
                "remote",
                "get-url",
                "origin",
            ):
                return CANONICAL_ORIGIN
            if args[:3] == (
                "fetch",
                "--no-tags",
                "origin",
            ):
                return ""
            if args == (
                "rev-parse",
                REMOTE_TRACKING_REF,
            ):
                return head
            if args == (
                "rev-parse",
                f"{head}^{{tree}}",
            ):
                return tree
            raise AssertionError(args)

        with tempfile.TemporaryDirectory(
            prefix="p5d3e-resolve-"
        ) as temp:
            with patch(
                "tools.obsidian_projection.p5d3e_verify._git",
                side_effect=fake_git,
            ):
                actual = resolve_real_candidate(
                    Path(temp)
                )

        self.assertEqual(actual, (head, tree))
        fetches = [
            call
            for call in calls
            if call and call[0] == "fetch"
        ]
        self.assertEqual(len(fetches), 1)
        self.assertEqual(
            fetches[0],
            (
                "fetch",
                "--no-tags",
                "origin",
                "+refs/heads/integration/system-v1:refs/remotes/origin/integration/system-v1",
            ),
        )

    def test_real_success_status_cannot_be_claimed_without_real_flags(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3e-test-"
        ) as temp:
            root = Path(temp)
            control, head, tree = _make_control_repo(root)
            vault = root / "real-vault"
            vault.mkdir()

            report = run_pre_resolved_sandbox(
                control_repo_root=control,
                candidate_head=head,
                candidate_tree=tree,
                real_vault_root=vault,
                candidate_resolution_network_fetch_performed=False,
                real_candidate_evaluated=False,
            )

            self.assertNotEqual(
                report["status"],
                "PASS_REAL_EXACT_HEAD_FINITE_EVALUATION",
            )


if __name__ == "__main__":
    unittest.main()
