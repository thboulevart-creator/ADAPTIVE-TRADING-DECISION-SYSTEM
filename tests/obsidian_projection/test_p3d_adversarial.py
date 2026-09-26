from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.first_open import (
    FilesystemIdentity,
    FirstOpenError,
    _assert_pre_open_vault,
    _load_snapshot,
    _obsidian_running,
    _snapshot_envelope,
    _verify_obsidian_directory,
    prepare_first_open,
    verify_first_open,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = (
    ROOT / "tools" / "obsidian_projection"
)
HARNESS_SOURCE = (
    PACKAGE_DIR / "first_open.py"
).read_text(encoding="utf-8")
CLI_SOURCE = (
    PACKAGE_DIR / "p3d_verify.py"
).read_text(encoding="utf-8")

FAKE_IDENTITY = FilesystemIdentity(
    volume_serial=10,
    file_identity=20,
    filesystem="NTFS",
)


class P3DAdversarialTests(unittest.TestCase):
    def test_harness_contains_no_obsidian_launch_primitive(
        self,
    ) -> None:
        forbidden = (
            "os.startfile",
            "subprocess.Popen",
            "obsidian://",
            "Start-Process",
            "ShellExecute",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    HARNESS_SOURCE,
                )
                self.assertNotIn(
                    token,
                    CLI_SOURCE,
                )

    def test_harness_contains_no_vault_cleanup_or_repair(
        self,
    ) -> None:
        forbidden = (
            "shutil.rmtree",
            ".unlink(",
            ".rmdir(",
            "os.remove(",
            "os.unlink(",
            ".rename(",
            "copytree(",
            "copy2(",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    HARNESS_SOURCE,
                )

    def test_only_binary_create_write_is_external_snapshot(
        self,
    ) -> None:
        self.assertEqual(
            HARNESS_SOURCE.count('.open("xb")'),
            1,
        )
        self.assertIn(
            "tempfile.mkdtemp(",
            HARNESS_SOURCE,
        )
        self.assertNotIn(
            ".mkdir(",
            HARNESS_SOURCE,
        )

    def test_cli_has_no_launch_destination_or_vault_override(
        self,
    ) -> None:
        for token in (
            "--destination",
            "--vault",
            "--open-obsidian",
            "--launch",
        ):
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    CLI_SOURCE,
                )

        self.assertIn(
            '"--prepare-first-open"',
            CLI_SOURCE,
        )
        self.assertIn(
            '"--verify-first-open"',
            CLI_SOURCE,
        )
        self.assertIn(
            '"--snapshot"',
            CLI_SOURCE,
        )

    def test_obsidian_running_detection_true(
        self,
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=(
                b'"Obsidian.exe","1234","Console",'
                b'"1","100,000 K"\r\n'
            ),
            stderr=b"",
        )

        with patch(
            "tools.obsidian_projection.first_open."
            "subprocess.run",
            return_value=completed,
        ), patch(
            "tools.obsidian_projection.first_open."
            "os.name",
            "nt",
        ):
            self.assertTrue(
                _obsidian_running()
            )

    def test_obsidian_running_detection_false(
        self,
    ) -> None:
        completed = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout=b"INFO: No tasks are running\r\n",
            stderr=b"",
        )

        with patch(
            "tools.obsidian_projection.first_open."
            "subprocess.run",
            return_value=completed,
        ), patch(
            "tools.obsidian_projection.first_open."
            "os.name",
            "nt",
        ):
            self.assertFalse(
                _obsidian_running()
            )

    def test_prepare_blocks_when_obsidian_running(
        self,
    ) -> None:
        with patch(
            "tools.obsidian_projection.first_open."
            "verify_harness_dependencies",
            return_value=({}, {}),
        ), patch(
            "tools.obsidian_projection.first_open."
            "_obsidian_running",
            return_value=True,
        ):
            with self.assertRaises(
                FirstOpenError
            ):
                prepare_first_open(
                    Path(".")
                )

    def test_verify_blocks_when_obsidian_running(
        self,
    ) -> None:
        with patch(
            "tools.obsidian_projection.first_open."
            "verify_harness_dependencies",
            return_value=({}, {}),
        ), patch(
            "tools.obsidian_projection.first_open."
            "_obsidian_running",
            return_value=True,
        ):
            with self.assertRaises(
                FirstOpenError
            ):
                verify_first_open(
                    Path("."),
                    Path("snapshot.json"),
                )

    def test_preopen_obsidian_directory_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "generated").mkdir()
            (vault / "views").mkdir()
            (vault / ".obsidian").mkdir()

            with patch(
                "tools.obsidian_projection.first_open."
                "_assert_tree_no_aliases",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.first_open."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                with self.assertRaises(
                    FirstOpenError
                ):
                    _assert_pre_open_vault(
                        vault
                    )

    def test_preopen_nonempty_views_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "generated").mkdir()
            (vault / "views").mkdir()
            (
                vault / "views" / "note.md"
            ).write_text(
                "x",
                encoding="utf-8",
            )

            with patch(
                "tools.obsidian_projection.first_open."
                "_assert_tree_no_aliases",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.first_open."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                with self.assertRaises(
                    FirstOpenError
                ):
                    _assert_pre_open_vault(
                        vault
                    )

    def test_preopen_extra_top_level_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "generated").mkdir()
            (vault / "views").mkdir()
            (vault / "extra").mkdir()

            with patch(
                "tools.obsidian_projection.first_open."
                "_assert_tree_no_aliases",
                return_value=None,
            ), patch(
                "tools.obsidian_projection.first_open."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                with self.assertRaises(
                    FirstOpenError
                ):
                    _assert_pre_open_vault(
                        vault
                    )

    def test_core_plugins_invalid_shape_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "core-plugins.json"
            ).write_text(
                '{"sync":"false"}',
                encoding="utf-8",
            )

            with self.assertRaises(
                FirstOpenError
            ):
                _verify_obsidian_directory(
                    vault
                )

    def test_invalid_json_config_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "app.json"
            ).write_text(
                "{invalid",
                encoding="utf-8",
            )

            with self.assertRaises(
                FirstOpenError
            ):
                _verify_obsidian_directory(
                    vault
                )

    def test_snapshot_outside_declared_temp_root_blocks(
        self,
    ) -> None:
        payload = {
            "generated_files": [],
        }
        envelope, digest = _snapshot_envelope(
            payload
        )

        with tempfile.TemporaryDirectory() as allowed:
            with tempfile.TemporaryDirectory() as other:
                path = (
                    Path(other)
                    / f"first-open-snapshot-{digest}.json"
                )
                path.write_text(
                    __import__("json").dumps(
                        envelope
                    ),
                    encoding="utf-8",
                )

                with patch(
                    "tools.obsidian_projection.first_open."
                    "tempfile.gettempdir",
                    return_value=allowed,
                ):
                    with self.assertRaises(
                        FirstOpenError
                    ):
                        _load_snapshot(path)


if __name__ == "__main__":
    unittest.main()
