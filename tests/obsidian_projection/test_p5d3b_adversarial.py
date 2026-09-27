from __future__ import annotations

import ast
import unittest
from pathlib import Path


class P5D3BAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "current_head_semantic_bridge.py"
        )
        cls.module = cls.module_path.read_text(
            encoding="utf-8"
        )
        cls.tree = ast.parse(cls.module)

    def test_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            (
                'CONTRACT_BLOB = '
                '"d1018443ce4dbbac614f0a65185ffd51ca7ffd69"'
            ),
            self.module,
        )

    def test_legacy_inventory_is_not_imported(self) -> None:
        for forbidden in (
            "FrozenInventory",
            "InventoryEntry",
            "load_inventory",
            "pilot_inventory_v0_1",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_legacy_classifier_execution_is_not_imported(
        self,
    ) -> None:
        for forbidden in (
            "classify_inventory",
            "classify_record",
            "semantic_classification_rules_v0_1",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_only_safe_classification_symbols_are_imported(
        self,
    ) -> None:
        self.assertIn(
            "SemanticRecord",
            self.module,
        )
        self.assertIn(
            "records_digest_sha256",
            self.module,
        )

    def test_no_relation_or_builder_execution_import(self) -> None:
        for forbidden in (
            "extract_relations",
            "build_projection_from_records",
            ".relations import",
            ".builder import",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_source_body_read_surface(self) -> None:
        for forbidden in (
            "read_blob",
            "read_bytes",
            "read_text",
            "open(",
            ".decode(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_filesystem_or_network_runtime_modules(
        self,
    ) -> None:
        imported: set[str] = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                imported.update(
                    alias.name.split(".", 1)[0]
                    for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(
                        node.module.split(".", 1)[0]
                    )

        forbidden = {
            "os",
            "pathlib",
            "shutil",
            "subprocess",
            "socket",
            "urllib",
            "requests",
            "http",
            "asyncio",
            "threading",
            "multiprocessing",
            "winreg",
            "ctypes",
            "tempfile",
        }
        self.assertEqual(
            imported & forbidden,
            set(),
        )

    def test_no_environment_time_randomness(self) -> None:
        for forbidden in (
            "os.environ",
            "getenv(",
            "time.",
            "datetime",
            "sleep(",
            "random",
            "uuid",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_fixed_pilot_or_reference_count(self) -> None:
        for forbidden in (
            "== 74",
            "!= 74",
            "== 908",
            "!= 908",
            "pilot_source_count",
            "source_artifact_count",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_artifact_family_ignores_selection_zone(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_artifact_family"
        )
        source = ast.get_source_segment(
            self.module,
            target,
        )
        self.assertIsNotNone(source)
        self.assertNotIn(
            "selection_zone",
            source or "",
        )

    def test_semantic_record_ignores_selection_zone(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_semantic_record"
        )
        source = ast.get_source_segment(
            self.module,
            target,
        )
        self.assertIsNotNone(source)
        self.assertNotIn(
            "selection_zone",
            source or "",
        )

    def test_semantic_axes_are_literal_conservative_defaults(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "_semantic_record"
        )
        source = ast.get_source_segment(
            self.module,
            target,
        ) or ""
        for literal in (
            'semantic_role="UNKNOWN"',
            'procedure_role="NONE"',
            'qualification_status="UNKNOWN"',
            'scientific_status="UNKNOWN"',
            'epistemic_role="UNKNOWN"',
            'temporal_role="UNKNOWN"',
            'authority_role="CANONICAL"',
            'persistence_state="TRACKED_IN_GIT_TREE"',
        ):
            with self.subTest(literal=literal):
                self.assertIn(literal, source)

    def test_metadata_only_family_is_explicit(self) -> None:
        self.assertIn(
            'return "METADATA_ONLY"',
            self.module,
        )

    def test_metadata_only_downstream_body_read_is_false(
        self,
    ) -> None:
        self.assertIn(
            'entry.content_mode == "FULL_TEXT"',
            self.module,
        )
        self.assertIn(
            "semantic_body_read=False",
            self.module,
        )

    def test_bridge_entry_digest_includes_full_binding(
        self,
    ) -> None:
        target = next(
            node
            for node in self.tree.body
            if isinstance(node, ast.ClassDef)
            and node.name == "CurrentHeadBridgeEntry"
        )
        source = ast.get_source_segment(
            self.module,
            target,
        ) or ""
        for field in (
            '"selection_zone"',
            '"content_mode"',
            '"disposition"',
            '"semantic_record"',
        ):
            with self.subTest(field=field):
                self.assertIn(field, source)

    def test_input_is_not_mutated_by_assignment(self) -> None:
        for forbidden in (
            "inventory.source_repository =",
            "inventory.source_branch =",
            "inventory.source_commit =",
            "inventory.source_tree =",
            "inventory.entries =",
            "entry.source_path =",
            "entry.content_mode =",
            "entry.selection_zone =",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_vault_or_promotion_surface(self) -> None:
        for forbidden in (
            "CURRENT.md",
            "ATDS-OBSIDIAN-PROJECTION",
            "production_promotion",
            "promote(",
            "pointer",
            "OneDrive",
            "Start-Process",
            "schtasks",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_background_loop_or_daemon_surface(
        self,
    ) -> None:
        defs = {
            node.name
            for node in self.tree.body
            if isinstance(node, ast.FunctionDef)
        }
        for forbidden in (
            "run_forever",
            "poll_loop",
            "daemon",
            "observe_forever",
            "main",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    defs,
                )

        while_nodes = [
            node
            for node in ast.walk(self.tree)
            if isinstance(node, ast.While)
        ]
        self.assertEqual(while_nodes, [])


if __name__ == "__main__":
    unittest.main()
