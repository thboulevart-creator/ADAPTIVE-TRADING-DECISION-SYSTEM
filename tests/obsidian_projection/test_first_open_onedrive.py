from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.first_open_onedrive import (
    CLOUD_6_TAG,
    EXPECTED_GENERATED_COUNT,
    EXPECTED_INTEGRITY_MANIFEST_SHA256,
    EXPECTED_TREE_DIGEST,
    EXPECTED_VAULT,
    FILE_ATTRIBUTE_OFFLINE,
    FILE_ATTRIBUTE_REPARSE_POINT,
    FILE_ATTRIBUTE_SPARSE_FILE,
    FIRST_OPEN_CONTRACT_V02_BLOB,
    FirstOpenOneDriveError,
    _assert_safe_directory,
    _file_native_state,
    _generated_map_from_snapshot,
    _generated_snapshot_fields,
    _projection_tree_digest_from_map,
    _snapshot_envelope,
    _verify_obsidian_directory,
    verify_harness_dependencies,
)


class P3D2OneDriveUnitTests(unittest.TestCase):
    def test_contract_blob_pin_is_exact(self) -> None:
        self.assertEqual(
            FIRST_OPEN_CONTRACT_V02_BLOB,
            "ddda9eb0abac4ff3fae02f459e16a1fa70bf907d",
        )

    def test_expected_vault_is_exact(self) -> None:
        self.assertEqual(
            EXPECTED_VAULT,
            (
                "C:\\Users\\Boulevart\\OneDrive\\Bureau\\ATDS\\"
                "ATDS-OBSIDIAN-PROJECTION"
            ),
        )

    def test_qualified_projection_constants_are_exact(self) -> None:
        self.assertEqual(
            EXPECTED_GENERATED_COUNT,
            92,
        )
        self.assertEqual(
            EXPECTED_TREE_DIGEST,
            "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0",
        )
        self.assertEqual(
            EXPECTED_INTEGRITY_MANIFEST_SHA256,
            "a23d009aa4ba668ea2e8d049b5496e05b42235ac1735fa8373ce07d2b2a1fc1b",
        )

    def test_persisted_dependencies_are_pinned(self) -> None:
        package = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
        )
        contract, _ = verify_harness_dependencies(
            package
        )
        self.assertEqual(
            contract["schema"],
            "ATDS_OBSIDIAN_FIRST_OPEN_SAFETY_CONTRACT_V0_2",
        )

    def test_cloud6_regular_file_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.md"
            path.write_bytes(b"abc")

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                    return_value=FILE_ATTRIBUTE_REPARSE_POINT,
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._native_reparse_tag",
                    return_value=CLOUD_6_TAG,
                ),
            ):
                state = _file_native_state(path)

            self.assertEqual(
                state["class"],
                "IO_REPARSE_TAG_CLOUD_6",
            )
            self.assertEqual(
                state["tag_hex"],
                "0x9000601A",
            )
            self.assertEqual(
                state["sha256"],
                hashlib.sha256(b"abc").hexdigest(),
            )

    def test_plain_regular_file_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.md"
            path.write_bytes(b"abc")

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                    return_value=0,
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._native_reparse_tag",
                    return_value=None,
                ),
            ):
                state = _file_native_state(path)

            self.assertEqual(
                state["class"],
                "NO_REPARSE_POINT",
            )

    def test_unexpected_reparse_tag_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.md"
            path.write_bytes(b"abc")

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                    return_value=FILE_ATTRIBUTE_REPARSE_POINT,
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._native_reparse_tag",
                    return_value=0x9000001A,
                ),
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _file_native_state(path)

    def test_offline_file_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.md"
            path.write_bytes(b"abc")

            with patch(
                "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                return_value=FILE_ATTRIBUTE_OFFLINE,
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _file_native_state(path)

    def test_sparse_file_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "x.md"
            path.write_bytes(b"abc")

            with patch(
                "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                return_value=FILE_ATTRIBUTE_SPARSE_FILE,
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _file_native_state(path)

    def test_directory_reparse_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._get_file_attributes",
                    return_value=FILE_ATTRIBUTE_REPARSE_POINT,
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._native_reparse_tag",
                    return_value=CLOUD_6_TAG,
                ),
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _assert_safe_directory(path)

    def test_projection_tree_digest_excludes_build_manifest(self) -> None:
        digest_map = {
            "generated/a.md": (
                3,
                hashlib.sha256(b"abc").hexdigest(),
            ),
            "generated/manifests/build-manifest.json": (
                1,
                hashlib.sha256(b"x").hexdigest(),
            ),
        }

        expected_payload = [
            [
                "generated/a.md",
                hashlib.sha256(b"abc").hexdigest(),
                3,
            ]
        ]
        expected = hashlib.sha256(
            json.dumps(
                expected_payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

        self.assertEqual(
            _projection_tree_digest_from_map(
                digest_map
            ),
            expected,
        )

    def test_snapshot_fields_preserve_sorted_map(self) -> None:
        digest_map = {
            "generated/a": (1, "a" * 64),
            "generated/b": (2, "b" * 64),
        }
        paths, sizes, hashes = (
            _generated_snapshot_fields(
                digest_map
            )
        )
        self.assertEqual(
            paths,
            ["generated/a", "generated/b"],
        )
        self.assertEqual(sizes["generated/b"], 2)
        self.assertEqual(
            hashes["generated/a"],
            "a" * 64,
        )

    def test_snapshot_map_rejects_duplicate_paths(self) -> None:
        payload = {
            "generated_relative_path_set": [
                "generated/a",
                "generated/a",
            ],
            "generated_file_sizes": {
                "generated/a": 1,
            },
            "generated_file_sha256": {
                "generated/a": "a" * 64,
            },
        }
        with self.assertRaises(
            FirstOpenOneDriveError
        ):
            _generated_map_from_snapshot(
                payload
            )

    def test_snapshot_envelope_binds_payload(self) -> None:
        payload = {"x": 1}
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

    def test_obsidian_sync_list_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            path = obsidian / "core-plugins.json"
            path.write_text(
                json.dumps(["sync"]),
                encoding="utf-8",
            )

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._assert_safe_directory"
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._file_native_state",
                    return_value={
                        "class": "NO_REPARSE_POINT",
                        "tag_hex": None,
                        "size_bytes": path.stat().st_size,
                        "sha256": "0" * 64,
                    },
                ),
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _verify_obsidian_directory(
                        vault
                    )

    def test_obsidian_sync_object_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            path = obsidian / "core-plugins.json"
            path.write_text(
                json.dumps(
                    {"sync": True}
                ),
                encoding="utf-8",
            )

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._assert_safe_directory"
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._file_native_state",
                    return_value={
                        "class": "NO_REPARSE_POINT",
                        "tag_hex": None,
                        "size_bytes": path.stat().st_size,
                        "sha256": "0" * 64,
                    },
                ),
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _verify_obsidian_directory(
                        vault
                    )

    def test_nonempty_community_plugins_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            path = (
                obsidian
                / "community-plugins.json"
            )
            path.write_text(
                json.dumps(["x"]),
                encoding="utf-8",
            )

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._assert_safe_directory"
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._file_native_state",
                    return_value={
                        "class": "NO_REPARSE_POINT",
                        "tag_hex": None,
                        "size_bytes": path.stat().st_size,
                        "sha256": "0" * 64,
                    },
                ),
            ):
                with self.assertRaises(
                    FirstOpenOneDriveError
                ):
                    _verify_obsidian_directory(
                        vault
                    )

    def test_safe_core_plugin_list_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            path = obsidian / "core-plugins.json"
            path.write_text(
                json.dumps(["file-explorer"]),
                encoding="utf-8",
            )

            with (
                patch(
                    "tools.obsidian_projection.first_open_onedrive._assert_safe_directory"
                ),
                patch(
                    "tools.obsidian_projection.first_open_onedrive._file_native_state",
                    return_value={
                        "class": "NO_REPARSE_POINT",
                        "tag_hex": None,
                        "size_bytes": path.stat().st_size,
                        "sha256": "0" * 64,
                    },
                ),
            ):
                result = _verify_obsidian_directory(
                    vault
                )

            self.assertFalse(
                result["obsidian_sync_enabled"]
            )
            self.assertFalse(
                result["community_plugins_enabled"]
            )


if __name__ == "__main__":
    unittest.main()
