from __future__ import annotations

import unittest
from pathlib import Path


class P5B2AdversarialStaticTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "dynamic_inventory.py"
        ).read_text(encoding="utf-8")
        cls.cli = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5b2_verify.py"
        ).read_text(encoding="utf-8")

    def test_p5b_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            "80729156f4ac51b760c4347f581f052a175b88b3",
            self.module,
        )

    def test_repository_and_branch_are_exact(self) -> None:
        self.assertIn(
            "ADAPTIVE-TRADING-DECISION-SYSTEM",
            self.module,
        )
        self.assertIn(
            'EXPECTED_BRANCH = "integration/system-v1"',
            self.module,
        )

    def test_exact_git_source_boundary_is_reused(
        self,
    ) -> None:
        self.assertIn(
            "FrozenGitSource",
            self.module,
        )
        self.assertIn(
            "source.verify_repository()",
            self.module,
        )
        self.assertIn(
            "source.verify_frozen_source()",
            self.module,
        )
        self.assertIn(
            "source.tree_entries()",
            self.module,
        )

    def test_no_working_tree_enumeration(self) -> None:
        for forbidden in (
            ".rglob(",
            ".glob(",
            "os.walk(",
            "Path.cwd(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_write_primitive_in_implementation(
        self,
    ) -> None:
        for forbidden in (
            ".write_text(",
            ".write_bytes(",
            'open("w',
            "open('w",
            'open("a',
            "open('a",
            'open("x',
            "open('x",
            "shutil.copy",
            "shutil.move",
            ".rename(",
            ".replace(",
            ".unlink(",
            ".rmdir(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )
                self.assertNotIn(
                    forbidden,
                    self.cli,
                )

    def test_no_git_mutation_commands(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            '"push"',
            '"commit"',
            '"checkout"',
            '"reset"',
            '"clean"',
            '"merge"',
            '"rebase"',
            '"switch"',
            '"add"',
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_no_vault_or_obsidian_mutation_surface(
        self,
    ) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "ATDS-OBSIDIAN-PROJECTION",
            ".obsidian",
            "seed_native_views",
            "generated/live",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_full_text_limit_is_pinned(self) -> None:
        self.assertIn(
            "MAX_FULL_TEXT_BYTES = 1_048_576",
            self.module,
        )

    def test_secret_scanner_version_is_pinned(
        self,
    ) -> None:
        self.assertIn(
            'SECRET_SCANNER_VERSION = "ATDS_HIGH_CONFIDENCE_SECRET_SCAN_V0_1"',
            self.module,
        )

    def test_secret_errors_use_path_hash(self) -> None:
        self.assertIn(
            "path_sha256=",
            self.module,
        )
        self.assertNotIn(
            "sensitive tracked path blocks HEAD: {entry.path}",
            self.module,
        )

    def test_unknown_zone_falls_back_instead_of_drop(
        self,
    ) -> None:
        self.assertIn(
            'return "OTHER_TRACKED"',
            self.module,
        )

    def test_selection_zone_is_not_semantic_classifier(
        self,
    ) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "qualification_status",
            "scientific_status",
            "epistemic_status",
            "artifact_family",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_symlink_and_gitlink_are_blocking(
        self,
    ) -> None:
        self.assertIn(
            'entry.mode == "120000"',
            self.module,
        )
        self.assertIn(
            'entry.mode == "160000"',
            self.module,
        )
        self.assertIn(
            "symlink tracked object blocks HEAD",
            self.module,
        )
        self.assertIn(
            "gitlink tracked object blocks HEAD",
            self.module,
        )

    def test_forbidden_recursive_surfaces_are_pinned(
        self,
    ) -> None:
        for required in (
            "generated/",
            "views/",
            ".obsidian/",
            "__pycache__",
            "node_modules",
            ".pyc",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_metadata_only_does_not_read_large_blob(
        self,
    ) -> None:
        size_guard = self.module.index(
            "entry.size > MAX_FULL_TEXT_BYTES"
        )
        read_call = self.module.index(
            "raw = read_blob(entry.oid)"
        )
        self.assertLess(size_guard, read_call)

    def test_full_text_length_is_verified(self) -> None:
        self.assertIn(
            "full-text raw blob length mismatch",
            self.module,
        )

    def test_inventory_digest_uses_only_entries(
        self,
    ) -> None:
        self.assertIn(
            "def canonical_entry_bytes",
            self.module,
        )
        self.assertIn(
            "self.canonical_entry_bytes()",
            self.module,
        )

    def test_cli_blocked_report_denies_qualification(
        self,
    ) -> None:
        self.assertIn(
            '"inventory_qualified": False',
            self.cli,
        )
        self.assertIn(
            '"vault_modified": False',
            self.cli,
        )
        self.assertIn(
            '"projection_modified": False',
            self.cli,
        )

    def test_cli_has_summary_mode(self) -> None:
        self.assertIn(
            '"--summary"',
            self.cli,
        )
        self.assertIn(
            "inventory_summary(inventory)",
            self.cli,
        )


if __name__ == "__main__":
    unittest.main()
