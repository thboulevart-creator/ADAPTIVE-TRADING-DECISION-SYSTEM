from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


class P3D2AdversarialStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "first_open_onedrive.py"
        )
        cls.cli_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p3d2_verify.py"
        )
        cls.module = cls.module_path.read_text(
            encoding="utf-8"
        )
        cls.cli = cls.cli_path.read_text(
            encoding="utf-8"
        )

    @staticmethod
    def _git_blob_oid(path: Path) -> str:
        raw = path.read_bytes()
        return hashlib.sha1(
            f"blob {len(raw)}\0".encode("ascii")
            + raw
        ).hexdigest()

    def test_p3c2_contract_blob_is_unchanged(self) -> None:
        path = (
            self.root
            / "tools"
            / "obsidian_projection"
            / "first_open_safety_contract_v0_2.json"
        )
        self.assertEqual(
            self._git_blob_oid(path),
            "ddda9eb0abac4ff3fae02f459e16a1fa70bf907d",
        )

    def test_p3d_v01_harness_blob_is_unchanged(self) -> None:
        path = (
            self.root
            / "tools"
            / "obsidian_projection"
            / "first_open.py"
        )
        self.assertEqual(
            self._git_blob_oid(path),
            "acc146137f8f1b77a6c851a7f18a86137941f50f",
        )

    def test_p3d_v01_cli_blob_is_unchanged(self) -> None:
        path = (
            self.root
            / "tools"
            / "obsidian_projection"
            / "p3d_verify.py"
        )
        self.assertEqual(
            self._git_blob_oid(path),
            "fe9003251832c90ee4a6316fcfa0a5f561ede3e5",
        )

    def test_cli_uses_successor_module_only(self) -> None:
        self.assertIn(
            "from .first_open_onedrive import",
            self.cli,
        )
        self.assertNotIn(
            "from .first_open import",
            self.cli,
        )

    def test_no_obsidian_launch_primitive(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "os.startfile",
            "subprocess.Popen",
            "ShellExecute",
            "obsidian://",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_no_vault_mutation_primitive(self) -> None:
        for forbidden in (
            ".write_text(",
            ".write_bytes(",
            "shutil.copy",
            "copytree(",
            "copy2(",
            ".rename(",
            ".unlink(",
            ".rmdir(",
            "os.remove(",
            "os.unlink(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_only_external_snapshot_write_is_present(self) -> None:
        self.assertIn(
            "tempfile.mkdtemp(",
            self.module,
        )
        self.assertIn(
            'with path.open("xb") as handle:',
            self.module,
        )
        self.assertIn(
            "ATDS-OBSIDIAN-FIRST-OPEN-",
            self.module,
        )

    def test_native_windows_reparse_api_is_required(self) -> None:
        for required in (
            "GetFileAttributesW",
            "DeviceIoControl",
            "FSCTL_GET_REPARSE_POINT",
            "FILE_ATTRIBUTE_REPARSE_POINT",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_cloud6_allowlist_is_exact(self) -> None:
        self.assertIn(
            "CLOUD_6_TAG = 0x9000601A",
            self.module,
        )
        self.assertIn(
            "tag not in (None, CLOUD_6_TAG)",
            self.module,
        )
        self.assertIn(
            "unexpected reparse tag",
            self.module,
        )

    def test_directory_reparse_is_fail_closed(self) -> None:
        self.assertIn(
            "directory reparse point forbidden",
            self.module,
        )

    def test_offline_and_sparse_are_fail_closed(self) -> None:
        self.assertIn(
            "offline file forbidden",
            self.module,
        )
        self.assertIn(
            "sparse file forbidden",
            self.module,
        )

    def test_exact_onedrive_path_is_pinned(self) -> None:
        self.assertIn(
            r"C:\Users\Boulevart\OneDrive\Bureau\ATDS",
            self.module,
        )
        self.assertIn(
            r"\ATDS-OBSIDIAN-PROJECTION",
            self.module,
        )

    def test_qualified_projection_digests_are_pinned(self) -> None:
        self.assertIn(
            "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0",
            self.module,
        )
        self.assertIn(
            "a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b",
            self.module,
        )

    def test_fresh_p2_is_required_in_prepare_and_verify(self) -> None:
        self.assertGreaterEqual(
            self.module.count(
                "_fresh_p2_and_compare("
            ),
            3,
        )
        self.assertIn(
            "validate_fresh_p2_report",
            self.module,
        )

    def test_generated_byte_comparison_is_explicit(self) -> None:
        self.assertIn(
            "fresh_map != vault_map",
            self.module,
        )
        self.assertIn(
            "current_generated != snapshot_generated",
            self.module,
        )

    def test_obsidian_sync_is_explicitly_blocked(self) -> None:
        self.assertIn(
            "Obsidian Sync core plugin enabled",
            self.module,
        )
        self.assertIn(
            '"explicit Obsidian Sync artifact "',
            self.module,
        )
        self.assertIn(
            'f"forbidden: {entry.name}"',
            self.module,
        )
        self.assertIn(
            '"obsidian_sync_enabled": False',
            self.module,
        )

    def test_community_plugins_are_explicitly_blocked(self) -> None:
        self.assertIn(
            "community-plugins.json must be []",
            self.module,
        )
        self.assertIn(
            '"community_plugins_enabled": False',
            self.module,
        )

    def test_views_must_remain_empty(self) -> None:
        self.assertIn(
            "views must be empty before first open",
            self.module,
        )
        self.assertIn(
            "views changed during first open",
            self.module,
        )

    def test_repository_state_is_checked_both_sides(self) -> None:
        self.assertIn(
            '"ATDS repository changed during "',
            self.module,
        )
        self.assertIn(
            '"pre-open reconstruction"',
            self.module,
        )
        self.assertIn(
            '"ATDS repository changed "',
            self.module,
        )
        self.assertIn(
            '"during post-check"',
            self.module,
        )

    def test_cli_blocked_report_denies_qualification(self) -> None:
        self.assertIn(
            '"first_open_qualified":',
            self.cli,
        )
        self.assertIn(
            "False",
            self.cli,
        )
        self.assertIn(
            '"vault_written_by_harness":',
            self.cli,
        )


if __name__ == "__main__":
    unittest.main()
