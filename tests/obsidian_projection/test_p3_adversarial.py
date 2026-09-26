from __future__ import annotations

import inspect
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.materialize import (
    EXPECTED_FINAL_NAME,
    FilesystemIdentity,
    MaterializationError,
    _assert_exact_projection_layout,
    _quarantine_after_failed_post_verify,
    materialize_once,
    validate_destination,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = (
    ROOT / "tools" / "obsidian_projection"
)
MATERIALIZER_SOURCE = (
    PACKAGE_DIR / "materialize.py"
).read_text(encoding="utf-8")
CLI_SOURCE = (
    PACKAGE_DIR / "p3_verify.py"
).read_text(encoding="utf-8")

FAKE_IDENTITY = FilesystemIdentity(
    volume_serial=111,
    file_identity=222,
    filesystem="NTFS",
)


def destination_contract(
    parent: Path,
) -> dict:
    final_path = parent / EXPECTED_FINAL_NAME
    return {
        "destination": {
            "observed_resolved_path":
                str(final_path),
            "expected_filesystem":
                "NTFS",
        }
    }


class P3AdversarialTests(unittest.TestCase):
    def test_materializer_has_no_destination_or_source_build_parameter(
        self,
    ) -> None:
        parameters = inspect.signature(
            materialize_once
        ).parameters
        self.assertEqual(
            list(parameters),
            ["repo_root"],
        )
        self.assertNotIn(
            "--destination",
            CLI_SOURCE,
        )
        self.assertNotIn(
            "--source-build",
            CLI_SOURCE,
        )

    def test_cli_requires_explicit_materialize_flag(
        self,
    ) -> None:
        self.assertIn(
            '"--materialize"',
            CLI_SOURCE,
        )
        self.assertIn(
            "--materialize is required",
            CLI_SOURCE,
        )

    def test_exact_final_name_is_fixed(
        self,
    ) -> None:
        self.assertEqual(
            EXPECTED_FINAL_NAME,
            "ATDS-OBSIDIAN-PROJECTION",
        )

    def test_materializer_uses_fresh_internal_p2_execution(
        self,
    ) -> None:
        self.assertIn(
            "build_p2_report(",
            MATERIALIZER_SOURCE,
        )
        self.assertIn(
            "validate_fresh_p2_report(",
            MATERIALIZER_SOURCE,
        )
        self.assertNotIn(
            "source_build: Path",
            inspect.getsource(
                materialize_once
            ).split(
                "def materialize_once",
                1,
            )[0],
        )

    def test_final_is_created_by_incoming_rename_not_direct_copy(
        self,
    ) -> None:
        self.assertIn(
            "incoming.rename(",
            MATERIALIZER_SOURCE,
        )
        self.assertNotIn(
            "copytree(",
            MATERIALIZER_SOURCE,
        )
        self.assertNotIn(
            "copy2(",
            MATERIALIZER_SOURCE,
        )

    def test_no_automatic_recursive_delete_exists(
        self,
    ) -> None:
        forbidden = (
            "shutil.rmtree",
            ".unlink(",
            ".rmdir(",
            "os.remove(",
            "os.unlink(",
            "Remove-Item",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    MATERIALIZER_SOURCE,
                )

    def test_no_obsidian_launch_plugin_or_sync_action(
        self,
    ) -> None:
        forbidden = (
            "os.startfile",
            "Start-Process",
            "subprocess.Popen",
            "obsidian://",
            "community-plugins.json",
            "Obsidian Sync",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    MATERIALIZER_SOURCE,
                )
                self.assertNotIn(
                    token,
                    CLI_SOURCE,
                )

    def test_layout_rejects_extra_top_level_file(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projection"

            for relative in (
                "generated/artifacts",
                "generated/relations",
                "generated/manifests",
                "views",
            ):
                (root / relative).mkdir(
                    parents=True,
                    exist_ok=True,
                )

            (
                root / "unexpected.txt"
            ).write_text(
                "unexpected",
                encoding="utf-8",
            )

            with self.assertRaises(
                MaterializationError
            ):
                _assert_exact_projection_layout(
                    root
                )

    def test_quarantine_target_preexisting_leaves_final_in_place(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            final = parent / "final"
            quarantine = parent / "failed"
            final.mkdir()
            quarantine.mkdir()

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                status = (
                    _quarantine_after_failed_post_verify(
                        final_path=final,
                        expected_identity=FAKE_IDENTITY,
                        quarantine_path=quarantine,
                    )
                )

            self.assertEqual(
                status,
                "QUARANTINE_TARGET_EXISTS_LEFT_IN_PLACE",
            )
            self.assertTrue(final.exists())

    @unittest.skipUnless(
        os.name == "nt",
        "Windows destination preflight",
    )
    def test_destination_existing_final_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            repo_root = (
                parent.parent
                / "synthetic-repo-p3b"
            )
            repo_root.mkdir(
                exist_ok=True
            )
            final_path = (
                parent / EXPECTED_FINAL_NAME
            )
            final_path.mkdir()

            contract = destination_contract(
                parent
            )

            with patch.dict(
                os.environ,
                {"LOCALAPPDATA": str(parent)},
                clear=False,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_known_sync_roots",
                return_value=(),
            ), patch(
                "tools.obsidian_projection.materialize."
                "_assert_no_reparse_ancestors",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_windows_volume_information",
                return_value=(123, "NTFS"),
            ):
                with self.assertRaises(
                    MaterializationError
                ):
                    validate_destination(
                        repo_root,
                        contract,
                    )

    @unittest.skipUnless(
        os.name == "nt",
        "Windows destination preflight",
    )
    def test_non_ntfs_destination_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            repo_root = (
                parent.parent
                / "synthetic-repo-p3b-fat"
            )
            repo_root.mkdir(
                exist_ok=True
            )

            contract = destination_contract(
                parent
            )

            with patch.dict(
                os.environ,
                {"LOCALAPPDATA": str(parent)},
                clear=False,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_known_sync_roots",
                return_value=(),
            ), patch(
                "tools.obsidian_projection.materialize."
                "_assert_no_reparse_ancestors",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_windows_volume_information",
                return_value=(123, "FAT32"),
            ):
                with self.assertRaises(
                    MaterializationError
                ):
                    validate_destination(
                        repo_root,
                        contract,
                    )

    @unittest.skipUnless(
        os.name == "nt",
        "Windows destination preflight",
    )
    def test_sync_root_destination_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            repo_root = (
                parent.parent
                / "synthetic-repo-p3b-sync"
            )
            repo_root.mkdir(
                exist_ok=True
            )

            contract = destination_contract(
                parent
            )

            with patch.dict(
                os.environ,
                {"LOCALAPPDATA": str(parent)},
                clear=False,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_known_sync_roots",
                return_value=(parent,),
            ), patch(
                "tools.obsidian_projection.materialize."
                "_assert_no_reparse_ancestors",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_windows_volume_information",
                return_value=(123, "NTFS"),
            ):
                with self.assertRaises(
                    MaterializationError
                ):
                    validate_destination(
                        repo_root,
                        contract,
                    )

    @unittest.skipUnless(
        os.name == "nt",
        "Windows destination preflight",
    )
    def test_repository_vault_containment_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp).resolve()
            repo_root = parent
            contract = destination_contract(
                parent
            )

            with patch.dict(
                os.environ,
                {"LOCALAPPDATA": str(parent)},
                clear=False,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_known_sync_roots",
                return_value=(),
            ), patch(
                "tools.obsidian_projection.materialize."
                "_assert_no_reparse_ancestors",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.materialize."
                "_windows_volume_information",
                return_value=(123, "NTFS"),
            ):
                with self.assertRaises(
                    MaterializationError
                ):
                    validate_destination(
                        repo_root,
                        contract,
                    )


if __name__ == "__main__":
    unittest.main()
