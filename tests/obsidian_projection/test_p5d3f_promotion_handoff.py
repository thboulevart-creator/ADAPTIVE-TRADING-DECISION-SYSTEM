from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.p5d3d_verify import (
    _build_synthetic_repo,
)
from tools.obsidian_projection.p5d3f_promotion_handoff import (
    HANDOFF_CONTRACT_BLOB,
    P5D3C2_VERIFIER_BLOB,
    P5D3D_EVALUATOR_BLOB,
    PromotionHandoffBlockedError,
    PromotionHandoffGovernanceError,
    _package_byte_tree_digest,
    run_finite_promotion_handoff,
    verify_promotion_handoff,
)


EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
EXPECTED_BRANCH = "integration/system-v1"


def _fingerprint(root: Path) -> tuple[tuple[str, int, str], ...]:
    rows: list[tuple[str, int, str]] = []
    for path in sorted(
        (p for p in root.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(root).as_posix(),
    ):
        raw = path.read_bytes()
        rows.append(
            (
                path.relative_to(root).as_posix(),
                len(raw),
                hashlib.sha256(raw).hexdigest(),
            )
        )
    return tuple(rows)


class P5D3FPromotionHandoffTests(unittest.TestCase):
    def _inputs(
        self,
        root: Path,
    ) -> tuple[Path, str, str, Path, Path, Path]:
        repo = root / "candidate"
        head, tree = _build_synthetic_repo(repo)

        workspace = root / "workspace"
        workspace.mkdir()

        staging = root / "promotion-staging"
        staging.mkdir()

        vault = root / "real-vault"
        vault.mkdir()
        (vault / "sentinel.txt").write_text(
            "UNCHANGED\n",
            encoding="utf-8",
        )

        return repo, head, tree, workspace, staging, vault

    def test_qualified_tooling_identities_are_frozen(self) -> None:
        self.assertEqual(
            HANDOFF_CONTRACT_BLOB,
            "64744325251db350d26c0269090ce62d5fa5f2e8",
        )
        self.assertEqual(
            P5D3C2_VERIFIER_BLOB,
            "c80df2b594fa55e65699f3db6212598c71a26f6d",
        )
        self.assertEqual(
            P5D3D_EVALUATOR_BLOB,
            "bff5f51abbb344c1ccc5e9c669a11cf0e26c2562",
        )

    def test_successful_synthetic_handoff_is_ready_unauthorized(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-impl-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            vault_before = _fingerprint(vault)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )

            self.assertEqual(
                report["status"],
                "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
            )
            self.assertEqual(
                report["evaluator_outcome"],
                "QUALIFIED",
            )
            self.assertEqual(
                report["package_status"],
                "PASS_SEALED_UNPROMOTED",
            )
            self.assertEqual(
                report["copied_package_status"],
                "PASS_SEALED_UNPROMOTED",
            )
            self.assertFalse(
                report["production_promotion_authorized"]
            )
            self.assertFalse(
                report["current_pointer_created"]
            )
            self.assertFalse(
                report["real_vault_modified"]
            )
            self.assertFalse(
                report["p5d2_promotion_confirmed_emitted"]
            )

            target = (
                staging
                / "packages"
                / report["generation_id"]
            )
            self.assertEqual(
                {p.name for p in target.iterdir()},
                {"package", "PROMOTION-HANDOFF.json"},
            )
            self.assertFalse(
                (target / "CURRENT").exists()
            )
            self.assertFalse(
                (target / "CURRENT.md").exists()
            )
            self.assertFalse(
                (target / "CURRENT.tmp").exists()
            )

            verified = verify_promotion_handoff(
                target,
                live_vault_root=vault,
            )
            self.assertEqual(
                verified["status"],
                "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
            )
            self.assertEqual(
                verified["generation_id"],
                report["generation_id"],
            )
            self.assertEqual(
                _fingerprint(vault),
                vault_before,
            )

    def test_rejected_candidate_creates_no_handoff(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-rejected-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            evaluator_report = {
                "repository": EXPECTED_REPOSITORY,
                "branch": EXPECTED_BRANCH,
                "candidate_head": head,
                "candidate_tree": tree,
                "outcome": "REJECTED",
                "failure_code": "SYNTHETIC_REJECTION",
                "p5d2_result_event_emitted": True,
                "live_projection_head_before": None,
                "live_projection_head_after": None,
                "real_vault_modified": False,
                "current_pointer_created": False,
                "production_promotion_authorized": False,
            }

            with patch(
                "tools.obsidian_projection."
                "p5d3f_promotion_handoff."
                "evaluate_candidate_finitely",
                return_value=evaluator_report,
            ):
                report = run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                    promotion_staging_root=staging,
                    live_vault_root=vault,
                )

            self.assertEqual(
                report["status"],
                "FAIL_CANDIDATE_REJECTED",
            )
            self.assertFalse(
                (staging / "packages").exists()
            )

    def test_blocked_candidate_creates_no_handoff(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-blocked-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            evaluator_report = {
                "repository": EXPECTED_REPOSITORY,
                "branch": EXPECTED_BRANCH,
                "candidate_head": head,
                "candidate_tree": tree,
                "outcome": "BLOCKED",
                "failure_code": "SYNTHETIC_BLOCK",
                "p5d2_result_event_emitted": False,
                "live_projection_head_before": None,
                "live_projection_head_after": None,
                "real_vault_modified": False,
                "current_pointer_created": False,
                "production_promotion_authorized": False,
            }

            with patch(
                "tools.obsidian_projection."
                "p5d3f_promotion_handoff."
                "evaluate_candidate_finitely",
                return_value=evaluator_report,
            ):
                report = run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                    promotion_staging_root=staging,
                    live_vault_root=vault,
                )

            self.assertEqual(
                report["status"],
                "BLOCKED_CANDIDATE_EVALUATION",
            )
            self.assertFalse(
                (staging / "packages").exists()
            )

    def test_staging_overlap_with_live_vault_fails_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-overlap-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                _staging,
                vault,
            ) = self._inputs(root)

            overlapping_staging = vault / "staging"
            overlapping_staging.mkdir()

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                    promotion_staging_root=overlapping_staging,
                    live_vault_root=vault,
                )

    def test_staging_and_live_vault_require_same_parent_context(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-parent-context-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                _staging,
                vault,
            ) = self._inputs(root)

            other_parent = root / "other-parent"
            other_parent.mkdir()
            staging = other_parent / "promotion-staging"
            staging.mkdir()

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                    promotion_staging_root=staging,
                    live_vault_root=vault,
                )

    def test_ancestor_git_worktree_does_not_make_staging_a_repository(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-ancestor-git-"
        ) as temp:
            root = Path(temp)

            completed = subprocess.run(
                ["git", "init", str(root)],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            if completed.returncode != 0:
                self.skipTest("git init unavailable")

            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )

            self.assertEqual(
                report["status"],
                "PASS_PROMOTION_HANDOFF_READY_UNAUTHORIZED",
            )

    def test_staging_that_is_git_repository_fails_closed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-staging-git-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            completed = subprocess.run(
                ["git", "init", str(staging)],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            if completed.returncode != 0:
                self.skipTest("git init unavailable")

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=workspace,
                    promotion_staging_root=staging,
                    live_vault_root=vault,
                )

    def test_handoff_wrapper_name_matches_generation_id(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-wrapper-name-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )

            target = (
                staging
                / "packages"
                / report["generation_id"]
            )
            wrong = (
                staging
                / "packages"
                / ("0" * 64)
            )
            target.rename(wrong)

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                verify_promotion_handoff(
                    wrong,
                    live_vault_root=vault,
                )

    def test_existing_generation_target_blocks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-collision-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            first = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )

            second_workspace = root / "workspace-2"
            second_workspace.mkdir()

            with self.assertRaises(
                PromotionHandoffBlockedError
            ):
                run_finite_promotion_handoff(
                    candidate_head=head,
                    candidate_tree=tree,
                    candidate_repo_root=repo,
                    evaluation_workspace_root=second_workspace,
                    promotion_staging_root=staging,
                    live_vault_root=vault,
                )

            target = (
                staging
                / "packages"
                / first["generation_id"]
            )
            self.assertTrue(target.is_dir())

    def test_tampered_copied_payload_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-tamper-package-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )
            target = (
                staging
                / "packages"
                / report["generation_id"]
            )

            payload = next(
                path
                for path in (
                    target / "package" / "generated"
                ).rglob("*")
                if path.is_file()
            )
            payload.write_bytes(
                payload.read_bytes() + b"TAMPER"
            )

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                verify_promotion_handoff(
                    target,
                    live_vault_root=vault,
                )

    def test_tampered_handoff_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-tamper-record-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )
            target = (
                staging
                / "packages"
                / report["generation_id"]
            )
            handoff = target / "PROMOTION-HANDOFF.json"

            value = json.loads(
                handoff.read_text(encoding="utf-8")
            )
            value["candidate_head"] = "0" * 40
            handoff.write_bytes(
                json.dumps(
                    value,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("utf-8")
                + b"\n"
            )

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                verify_promotion_handoff(
                    target,
                    live_vault_root=vault,
                )

    def test_handoff_verifier_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-readonly-"
        ) as temp:
            root = Path(temp)
            (
                repo,
                head,
                tree,
                workspace,
                staging,
                vault,
            ) = self._inputs(root)

            report = run_finite_promotion_handoff(
                candidate_head=head,
                candidate_tree=tree,
                candidate_repo_root=repo,
                evaluation_workspace_root=workspace,
                promotion_staging_root=staging,
                live_vault_root=vault,
            )
            target = (
                staging
                / "packages"
                / report["generation_id"]
            )
            before = _fingerprint(target)

            verify_promotion_handoff(
                target,
                live_vault_root=vault,
            )

            self.assertEqual(
                _fingerprint(target),
                before,
            )

    def test_package_byte_tree_rejects_hard_links(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-hardlink-"
        ) as temp:
            root = Path(temp)
            package = root / "package"
            package.mkdir()
            first = package / "a.bin"
            second = package / "b.bin"
            first.write_bytes(b"x")

            try:
                os.link(first, second)
            except OSError as exc:
                self.skipTest(
                    f"hard links unavailable: {exc}"
                )

            with self.assertRaises(
                PromotionHandoffGovernanceError
            ):
                _package_byte_tree_digest(package)


if __name__ == "__main__":
    unittest.main()
