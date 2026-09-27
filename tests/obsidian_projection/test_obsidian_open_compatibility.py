from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.obsidian_open_compatibility import (
    CURRENT_SCHEMA,
    ObsidianOpenCompatibilityError,
    OpenPointerMixedError,
    OpenPointerPartialError,
    _core_plugins_sync_disabled,
    _current_note_bytes,
    _load_snapshot,
    _write_snapshot,
    _parse_simple_frontmatter,
    _safe_obsidian_state,
    build_markdown_generation,
    validate_current_pointer,
    validate_markdown_generation,
    write_current_atomic,
)


class P5C3OpenCompatibilityTests(unittest.TestCase):
    def test_generation_build_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "GEN_A"
            manifest = build_markdown_generation(
                root,
                "GEN_A",
            )
            validated = validate_markdown_generation(
                root
            )

            self.assertEqual(
                validated["generation_id"],
                "GEN_A",
            )
            self.assertEqual(
                validated["file_count"],
                129,
            )
            self.assertEqual(
                validated[
                    "generation_tree_digest_sha256"
                ],
                manifest[
                    "generation_tree_digest_sha256"
                ],
            )

    def test_generation_directory_digest_changes_on_mutation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "GEN_A"
            build_markdown_generation(
                root,
                "GEN_A",
            )
            before = validate_markdown_generation(
                root
            )["directory_tree_digest_sha256"]

            target = (
                root
                / "d00"
                / "artifact-0000.md"
            )
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nmutation\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                OpenPointerPartialError
            ):
                validate_markdown_generation(
                    root
                )

            self.assertNotEqual(
                before,
                __import__(
                    "tools.obsidian_projection."
                    "obsidian_open_compatibility",
                    fromlist=["_tree_digest"],
                )._tree_digest(root),
            )

    def test_current_note_frontmatter_is_exact(self) -> None:
        raw = _current_note_bytes(
            "GEN_A",
            "a" * 64,
        )
        text = raw.decode("utf-8")
        frontmatter = _parse_simple_frontmatter(
            text
        )

        self.assertEqual(
            frontmatter["schema"],
            CURRENT_SCHEMA,
        )
        self.assertEqual(
            frontmatter["generation_id"],
            "GEN_A",
        )
        self.assertEqual(
            frontmatter[
                "generation_tree_digest_sha256"
            ],
            "a" * 64,
        )
        self.assertIn(
            "[[generations/GEN_A/INDEX|Open active generation]]",
            text,
        )

    def test_atomic_pointer_switch_validates(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            generations = (
                vault / "generations"
            )
            generations.mkdir()

            a = build_markdown_generation(
                generations / "GEN_A",
                "GEN_A",
            )
            b = build_markdown_generation(
                generations / "GEN_B",
                "GEN_B",
            )

            write_current_atomic(
                vault,
                "GEN_A",
                a[
                    "generation_tree_digest_sha256"
                ],
            )
            self.assertEqual(
                validate_current_pointer(
                    vault
                )["generation_id"],
                "GEN_A",
            )

            write_current_atomic(
                vault,
                "GEN_B",
                b[
                    "generation_tree_digest_sha256"
                ],
            )
            self.assertEqual(
                validate_current_pointer(
                    vault
                )["generation_id"],
                "GEN_B",
            )
            self.assertFalse(
                (vault / "CURRENT.tmp").exists()
            )

    def test_pointer_target_mismatch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            generations = (
                vault / "generations"
            )
            generations.mkdir()

            a = build_markdown_generation(
                generations / "GEN_A",
                "GEN_A",
            )
            build_markdown_generation(
                generations / "GEN_B",
                "GEN_B",
            )

            raw = _current_note_bytes(
                "GEN_A",
                a[
                    "generation_tree_digest_sha256"
                ],
            ).decode("utf-8")
            raw = raw.replace(
                "generations/GEN_A/INDEX",
                "generations/GEN_B/INDEX",
            )
            (vault / "CURRENT.md").write_text(
                raw,
                encoding="utf-8",
            )

            with self.assertRaises(
                OpenPointerMixedError
            ):
                validate_current_pointer(
                    vault
                )

    def test_core_plugin_object_sync_true_is_blocked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "core-plugins.json"
            path.write_text(
                json.dumps(
                    {
                        "sync": True,
                        "graph": True,
                    }
                ),
                encoding="utf-8",
            )
            self.assertFalse(
                _core_plugins_sync_disabled(
                    path
                )
            )

    def test_core_plugin_object_sync_false_is_safe(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "core-plugins.json"
            path.write_text(
                json.dumps(
                    {
                        "sync": False,
                        "graph": True,
                    }
                ),
                encoding="utf-8",
            )
            self.assertTrue(
                _core_plugins_sync_disabled(
                    path
                )
            )

    def test_community_plugin_list_must_be_empty(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (obsidian / "core-plugins.json").write_text(
                json.dumps({"sync": False}),
                encoding="utf-8",
            )
            (
                obsidian
                / "community-plugins.json"
            ).write_text(
                json.dumps(["example"]),
                encoding="utf-8",
            )

            with self.assertRaises(
                ObsidianOpenCompatibilityError
            ):
                _safe_obsidian_state(
                    vault,
                    require_workspace_current=False,
                )

    def test_workspace_must_reference_current(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (obsidian / "core-plugins.json").write_text(
                json.dumps({"sync": False}),
                encoding="utf-8",
            )
            (
                obsidian
                / "community-plugins.json"
            ).write_text(
                "[]",
                encoding="utf-8",
            )
            (obsidian / "workspace.json").write_text(
                json.dumps(
                    {
                        "main": {
                            "state": {
                                "file": "CURRENT.md"
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            state = _safe_obsidian_state(
                vault,
                require_workspace_current=True,
            )
            self.assertTrue(
                state[
                    "workspace_references_current"
                ]
            )

    def test_workspace_without_current_is_blocked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (obsidian / "core-plugins.json").write_text(
                json.dumps({"sync": False}),
                encoding="utf-8",
            )
            (obsidian / "workspace.json").write_text(
                json.dumps(
                    {
                        "main": {
                            "state": {
                                "file": "OTHER.md"
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(
                ObsidianOpenCompatibilityError
            ):
                _safe_obsidian_state(
                    vault,
                    require_workspace_current=True,
                )

    def test_obsidian_subdirectory_is_blocked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            obsidian = vault / ".obsidian"
            obsidian.mkdir()
            (obsidian / "plugins").mkdir()
            (obsidian / "core-plugins.json").write_text(
                json.dumps({"sync": False}),
                encoding="utf-8",
            )

            with self.assertRaises(
                ObsidianOpenCompatibilityError
            ):
                _safe_obsidian_state(
                    vault,
                    require_workspace_current=False,
                )

    def test_snapshot_is_written_redundantly(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            primary = root / "primary"
            backup = root / "backup"

            payload = {
                "schema": "TEST",
                "value": 1,
            }

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_compatibility."
                "_snapshot_directories",
                return_value=(primary, backup),
            ):
                (
                    primary_path,
                    backup_path,
                    digest,
                ) = _write_snapshot(payload)

                self.assertTrue(
                    primary_path.is_file()
                )
                self.assertTrue(
                    backup_path.is_file()
                )
                self.assertEqual(
                    primary_path.read_bytes(),
                    backup_path.read_bytes(),
                )

                loaded_primary, token_primary = (
                    _load_snapshot(
                        primary_path
                    )
                )
                loaded_backup, token_backup = (
                    _load_snapshot(
                        backup_path
                    )
                )

            self.assertEqual(
                loaded_primary,
                payload,
            )
            self.assertEqual(
                loaded_backup,
                payload,
            )
            self.assertEqual(
                token_primary,
                digest,
            )
            self.assertEqual(
                token_backup,
                digest,
            )

    def test_identical_content_addressed_snapshot_is_reused(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            primary = root / "primary"
            backup = root / "backup"

            payload = {
                "schema": "TEST",
                "value": 3,
            }

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_compatibility."
                "_snapshot_directories",
                return_value=(primary, backup),
            ):
                first = _write_snapshot(payload)
                second = _write_snapshot(payload)

            self.assertEqual(
                first,
                second,
            )
            self.assertEqual(
                first[0].read_bytes(),
                first[1].read_bytes(),
            )

    def test_snapshot_copy_divergence_is_blocked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            primary = root / "primary"
            backup = root / "backup"

            payload = {
                "schema": "TEST",
                "value": 2,
            }

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_compatibility."
                "_snapshot_directories",
                return_value=(primary, backup),
            ):
                (
                    primary_path,
                    backup_path,
                    _digest,
                ) = _write_snapshot(payload)

                backup_path.write_bytes(
                    b'{"corrupted":true}\n'
                )

                with self.assertRaises(
                    ObsidianOpenCompatibilityError
                ):
                    _load_snapshot(
                        primary_path
                    )

    def test_pointer_write_uses_replace(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            vault = Path(td)
            with patch(
                "tools.obsidian_projection."
                "obsidian_open_compatibility.os.replace"
            ) as replace:
                write_current_atomic(
                    vault,
                    "GEN_A",
                    "a" * 64,
                )

            replace.assert_called_once()
            self.assertTrue(
                (vault / "CURRENT.tmp").exists()
            )


if __name__ == "__main__":
    unittest.main()
