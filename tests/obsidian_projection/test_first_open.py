from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from tools.obsidian_projection.first_open import (
    FIRST_OPEN_CONTRACT_BLOB,
    MATERIALIZATION_CONTRACT_BLOB,
    QUALIFIED_MATERIALIZE_HELPER_BLOB,
    FirstOpenError,
    _expected_vault_path,
    _generated_map_from_snapshot,
    _load_snapshot,
    _snapshot_envelope,
    _verify_obsidian_directory,
    verify_harness_dependencies,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = (
    ROOT / "tools" / "obsidian_projection"
)


class FirstOpenHarnessUnitTests(unittest.TestCase):
    def test_dependency_blob_pins_match_persisted_package(
        self,
    ) -> None:
        first_open, materialization = (
            verify_harness_dependencies(
                PACKAGE_DIR
            )
        )
        self.assertEqual(
            first_open["qualified_p3b_head"],
            "bb5fc55c8a7f51a58f9a53b27bb499f5b6d381ba",
        )
        self.assertEqual(
            materialization[
                "qualified_p2b_head"
            ],
            "157b519dafb226e53ae13a281f7dc294d584cc0d",
        )

    def test_pin_constants_are_full_git_oids(self) -> None:
        for value in (
            FIRST_OPEN_CONTRACT_BLOB,
            MATERIALIZATION_CONTRACT_BLOB,
            QUALIFIED_MATERIALIZE_HELPER_BLOB,
        ):
            self.assertRegex(
                value,
                r"^[0-9a-f]{40}$",
            )

    def test_tampered_first_open_contract_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp)

            names = (
                "materialization_contract_v0_1.json",
                "materialize.py",
                "deterministic_projection_contract_v0_1.json",
                "rendering.py",
                "relations.py",
                "integrity.py",
                "builder.py",
                "p2_verify.py",
            )
            for name in names:
                (
                    package / name
                ).write_bytes(
                    (PACKAGE_DIR / name).read_bytes()
                )

            (
                package
                / "first_open_safety_contract_v0_1.json"
            ).write_bytes(b"{}\n")

            with self.assertRaises(FirstOpenError):
                verify_harness_dependencies(package)

    def test_tampered_materialize_helper_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp)

            names = (
                "first_open_safety_contract_v0_1.json",
                "materialization_contract_v0_1.json",
                "deterministic_projection_contract_v0_1.json",
                "rendering.py",
                "relations.py",
                "integrity.py",
                "builder.py",
                "p2_verify.py",
            )
            for name in names:
                (
                    package / name
                ).write_bytes(
                    (PACKAGE_DIR / name).read_bytes()
                )

            (
                package / "materialize.py"
            ).write_bytes(b"tampered\n")

            with self.assertRaises(FirstOpenError):
                verify_harness_dependencies(package)

    @unittest.skipUnless(
        os.name == "nt",
        "Windows contractual Vault path",
    )
    def test_msix_localappdata_virtualization_does_not_redirect_vault(
        self,
    ) -> None:
        contract = json.loads(
            (
                PACKAGE_DIR
                / "first_open_safety_contract_v0_1.json"
            ).read_text(encoding="utf-8")
        )

        virtualized = (
            "C:\\Users\\Boulevart\\AppData\\Local\\Packages\\"
            "PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\"
            "LocalCache\\Local"
        )

        with patch.dict(
            os.environ,
            {"LOCALAPPDATA": virtualized},
            clear=False,
        ):
            actual = _expected_vault_path(
                contract
            )

        self.assertEqual(
            str(actual),
            (
                "C:\\Users\\Boulevart\\AppData\\Local\\"
                "ATDS-OBSIDIAN-PROJECTION"
            ),
        )

    def test_contractual_vault_path_must_keep_fixed_final_name(
        self,
    ) -> None:
        contract = {
            "materialized_vault": {
                "observed_resolved_path":
                    r"C:\Users\Boulevart\AppData\Local\WRONG"
            }
        }

        with patch(
            "tools.obsidian_projection.first_open.os.name",
            "nt",
        ):
            with self.assertRaises(
                FirstOpenError
            ):
                _expected_vault_path(
                    contract
                )

    def test_snapshot_envelope_binds_payload_digest(
        self,
    ) -> None:
        payload = {
            "a": 1,
            "b": ["x", "y"],
        }
        envelope, digest = _snapshot_envelope(
            payload
        )
        self.assertEqual(
            envelope["payload_sha256"],
            digest,
        )
        self.assertEqual(
            envelope["payload"],
            payload,
        )
        self.assertRegex(
            digest,
            r"^[0-9a-f]{64}$",
        )

    def test_snapshot_tamper_blocks(self) -> None:
        payload = {
            "phase":
                "PREPARED_FOR_MANUAL_FIRST_OPEN",
            "generated_files": [],
        }
        envelope, digest = _snapshot_envelope(
            payload
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = (
                Path(tmp)
                / f"first-open-snapshot-{digest}.json"
            )
            path.write_text(
                json.dumps(envelope),
                encoding="utf-8",
            )

            loaded, token = _load_snapshot(
                path
            )
            self.assertEqual(loaded, payload)
            self.assertEqual(token, digest)

            envelope["payload"]["phase"] = (
                "TAMPERED"
            )
            path.write_text(
                json.dumps(envelope),
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _load_snapshot(path)

    def test_snapshot_filename_digest_binding_blocks(
        self,
    ) -> None:
        payload = {"generated_files": []}
        envelope, _digest = (
            _snapshot_envelope(payload)
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = (
                Path(tmp)
                / "first-open-snapshot-wrong.json"
            )
            path.write_text(
                json.dumps(envelope),
                encoding="utf-8",
            )
            with self.assertRaises(FirstOpenError):
                _load_snapshot(path)

    def test_snapshot_generated_map_rejects_duplicates(
        self,
    ) -> None:
        payload = {
            "generated_files": [
                {
                    "relative_path":
                        "generated/a.md",
                    "size_bytes": 1,
                    "sha256": "a" * 64,
                },
                {
                    "relative_path":
                        "generated/a.md",
                    "size_bytes": 1,
                    "sha256": "a" * 64,
                },
            ]
        }
        with self.assertRaises(FirstOpenError):
            _generated_map_from_snapshot(
                payload
            )

    def test_obsidian_root_json_only_valid_configuration(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()

            (
                obsidian / "app.json"
            ).write_text(
                "{}",
                encoding="utf-8",
            )
            (
                obsidian / "community-plugins.json"
            ).write_text(
                "[]",
                encoding="utf-8",
            )
            (
                obsidian / "core-plugins.json"
            ).write_text(
                json.dumps(
                    {
                        "file-explorer": True,
                        "sync": False,
                    }
                ),
                encoding="utf-8",
            )

            result = _verify_obsidian_directory(
                vault
            )

            self.assertFalse(
                result["community_plugins_enabled"]
            )
            self.assertFalse(
                result["sync_enabled"]
            )
            self.assertEqual(
                result["subdirectory_count"],
                0,
            )

    def test_obsidian_subdirectory_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            (obsidian / "plugins").mkdir(
                parents=True
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )

    def test_obsidian_non_json_root_file_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "state.txt"
            ).write_text(
                "x",
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )

    def test_community_plugin_nonempty_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "community-plugins.json"
            ).write_text(
                '["example-plugin"]',
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )

    def test_core_sync_enabled_array_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "core-plugins.json"
            ).write_text(
                '["file-explorer","sync"]',
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )

    def test_core_sync_enabled_object_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "core-plugins.json"
            ).write_text(
                '{"sync":true}',
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )

    def test_explicit_sync_artifact_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (
                obsidian / "sync-settings.json"
            ).write_text(
                "{}",
                encoding="utf-8",
            )

            with self.assertRaises(FirstOpenError):
                _verify_obsidian_directory(
                    vault
                )


if __name__ == "__main__":
    unittest.main()
