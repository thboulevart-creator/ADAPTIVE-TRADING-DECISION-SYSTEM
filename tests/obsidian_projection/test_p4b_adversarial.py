from __future__ import annotations

import unittest
from pathlib import Path


class P4BAdversarialStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "native_view_bundle.py"
        )
        cls.cli_path = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p4b_verify.py"
        )
        cls.module = cls.module_path.read_text(
            encoding="utf-8"
        )
        cls.cli = cls.cli_path.read_text(
            encoding="utf-8"
        )

    def test_exact_projection_digest_is_pinned(self) -> None:
        self.assertIn(
            "bf67fb65d42de58f394a21a884ca180665b3ba550be101ac2d410b0aa425e2e0",
            self.module,
        )

    def test_p4a_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            "699cbaf60141d8ecbb4f7f1afad214b6dd51f92b",
            self.module,
        )

    def test_exact_seven_paths_are_pinned(self) -> None:
        for required in (
            "views/HOME.md",
            "views/dashboards/PROJECT-SNAPSHOT.md",
            "views/dashboards/QUALIFICATION-STATUS.md",
            "views/maps/SYSTEM-ARCHITECTURE.md",
            "views/maps/GOVERNANCE.md",
            "views/maps/RESEARCH-LIFECYCLE.md",
            "views/canvas/ATDS-OVERVIEW.canvas",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.module)

    def test_only_views_are_write_targets(self) -> None:
        self.assertIn(
            "with target.open(\"xb\") as handle:",
            self.module,
        )
        self.assertIn(
            "views must be empty before initial seed",
            self.module,
        )
        self.assertNotIn(
            "generated.open(",
            self.module,
        )
        self.assertNotIn(
            "obsidian.open(",
            self.module,
        )

    def test_no_overwrite_primitive(self) -> None:
        for forbidden in (
            ".write_text(",
            ".write_bytes(",
            "open(\"wb\")",
            "open('wb')",
            "shutil.copy",
            "copytree(",
            "copy2(",
            ".rename(",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    self.module,
                )

    def test_no_plugin_or_sync_enablement(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "community-plugins.json",
            "obsidian://",
            "os.startfile",
            "subprocess.Popen",
            "import dataview",
            "from dataview",
            "import excalidraw",
            "from excalidraw",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_no_external_network_dependency(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "requests.",
            "urllib.",
            "http://",
            "https://",
            "socket.",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_generated_is_snapshotted_both_sides(self) -> None:
        self.assertIn(
            "generated_before",
            self.module,
        )
        self.assertIn(
            "generated_after",
            self.module,
        )
        self.assertIn(
            "generated changed during P4-B seed",
            self.module,
        )

    def test_obsidian_config_is_snapshotted_both_sides(
        self,
    ) -> None:
        self.assertIn(
            "obsidian_before",
            self.module,
        )
        self.assertIn(
            ".obsidian changed during P4-B seed",
            self.module,
        )

    def test_repository_state_is_snapshotted_both_sides(
        self,
    ) -> None:
        self.assertIn(
            "repo_before",
            self.module,
        )
        self.assertIn(
            "repository state changed during P4-B seed",
            self.module,
        )

    def test_obsidian_must_be_closed(self) -> None:
        self.assertIn(
            "_obsidian_running",
            self.module,
        )
        self.assertIn(
            "Obsidian must be fully closed before P4-B seed",
            self.module,
        )

    def test_native_reparse_guard_is_used_for_views(
        self,
    ) -> None:
        self.assertIn(
            "_file_native_state",
            self.module,
        )
        self.assertIn(
            "IO_REPARSE_TAG_CLOUD_6",
            self.module,
        )

    def test_frontmatter_keeps_view_non_authoritative(
        self,
    ) -> None:
        self.assertIn(
            '("authority_role", "VIEW")',
            self.module,
        )
        self.assertIn(
            '("semantic_authority", "NONE")',
            self.module,
        )
        self.assertIn(
            '("projection_freshness", "BOUND")',
            self.module,
        )

    def test_qualification_and_scientific_axes_stay_separate(
        self,
    ) -> None:
        self.assertIn(
            "Distribution — qualification",
            self.module,
        )
        self.assertIn(
            "Distribution — statut scientifique",
            self.module,
        )

    def test_canvas_edges_have_no_semantic_labels(
        self,
    ) -> None:
        self.assertIn(
            '"fromNode": home_id',
            self.module,
        )
        self.assertIn(
            '"toNode": _stable_id',
            self.module,
        )
        self.assertNotIn(
            '"label":',
            self.module,
        )

    def test_preview_never_authorizes_seed(self) -> None:
        self.assertIn(
            '"seed_authorized_by_preview": False',
            self.cli,
        )

    def test_blocked_report_denies_qualification(self) -> None:
        self.assertIn(
            '"p4b_seed_qualified": False',
            self.cli,
        )
        self.assertIn(
            '"vault_write_authorized": False',
            self.cli,
        )

    def test_success_report_denies_future_overwrite(self) -> None:
        self.assertIn(
            '"automatic_overwrite_authorized": False',
            self.module,
        )


if __name__ == "__main__":
    unittest.main()
