from __future__ import annotations

import unittest
from pathlib import Path


class P5C3AdversarialStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "obsidian_open_compatibility.py"
        ).read_text(encoding="utf-8")
        cls.cli = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5c3_verify.py"
        ).read_text(encoding="utf-8")
        cls.prepare_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3_prepare_control.ps1"
        ).read_text(encoding="utf-8")
        cls.open_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3_open.ps1"
        ).read_text(encoding="utf-8")
        cls.post_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3_post_close.ps1"
        ).read_text(encoding="utf-8")
        cls.legacy_p5c2_test = (
            cls.root
            / "tests"
            / "obsidian_projection"
            / "test_promotion_experiment.py"
        ).read_text(encoding="utf-8")

    def test_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            "4974302509a989fbd296ee7052ca15f22a0750a6",
            self.module,
        )

    def test_real_and_sandbox_vaults_are_distinct(
        self,
    ) -> None:
        self.assertIn(
            "ATDS-OBSIDIAN-PROJECTION",
            self.module,
        )
        self.assertIn(
            "ATDS-P5C3-OBSIDIAN-OPEN-SANDBOX",
            self.module,
        )
        self.assertIn(
            "sandbox overlaps real Vault",
            self.module,
        )

    def test_no_automatic_obsidian_launch(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "os.startfile",
            "obsidian://",
            "Start-Process",
            "subprocess.Popen",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_snapshot_persistence_has_verified_backup(
        self,
    ) -> None:
        self.assertIn(
            "ATDS-P5C3-CONTROL-EVIDENCE",
            self.module,
        )
        self.assertIn(
            "snapshot copies differ after write",
            self.module,
        )
        self.assertIn(
            "snapshot copies differ",
            self.module,
        )
        self.assertIn(
            "both snapshot copies are missing",
            self.module,
        )
        self.assertIn(
            "snapshot path is not a verified persisted copy",
            self.module,
        )

    def test_prepare_does_not_require_obsidian_open(
        self,
    ) -> None:
        start = self.module.index(
            "def prepare_open_experiment("
        )
        end = self.module.index(
            "\n@dataclass\nclass OpenReaderMetrics",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            "Obsidian must be closed during P5-C3 prepare",
            body,
        )
        self.assertNotIn(
            "Obsidian is not running at end of P5-C3 open experiment",
            body,
        )

    def test_run_open_contains_end_process_check(
        self,
    ) -> None:
        start = self.module.index(
            "def run_while_obsidian_open("
        )
        end = self.module.index(
            "\ndef post_close_verify(",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            "Obsidian must be running during P5-C3 open experiment",
            body,
        )
        self.assertIn(
            "Obsidian is not running at end of P5-C3 open experiment",
            body,
        )

    def test_prepare_requires_obsidian_closed(self) -> None:
        self.assertIn(
            "Obsidian must be closed during P5-C3 prepare",
            self.module,
        )

    def test_open_experiment_requires_obsidian_running(
        self,
    ) -> None:
        self.assertIn(
            "Obsidian must be running during P5-C3 open experiment",
            self.module,
        )
        self.assertIn(
            "Obsidian stopped during P5-C3 open experiment",
            self.module,
        )
        self.assertIn(
            "Obsidian is not running at end of P5-C3 open experiment",
            self.module,
        )

    def test_workspace_current_is_required(self) -> None:
        self.assertIn(
            "workspace does not reference CURRENT.md",
            self.module,
        )
        self.assertIn(
            "require_workspace_current=True",
            self.module,
        )

    def test_sync_and_community_plugins_are_blocked(
        self,
    ) -> None:
        self.assertIn(
            "Obsidian Sync core plugin enabled",
            self.module,
        )
        self.assertIn(
            "community plugins enabled",
            self.module,
        )
        self.assertIn(
            'b"[]\\n"',
            self.module,
        )

    def test_plugin_subdirectory_is_not_accepted(
        self,
    ) -> None:
        self.assertIn(
            ".obsidian subdirectory forbidden",
            self.module,
        )

    def test_fixture_scale_is_exact(self) -> None:
        self.assertIn(
            "NOTES_PER_GENERATION = 128",
            self.module,
        )
        self.assertIn(
            "NESTED_DIRECTORIES = 8",
            self.module,
        )
        self.assertIn(
            "PROMOTION_CYCLES = 250",
            self.module,
        )
        self.assertIn(
            "MIN_READER_SAMPLES = 5000",
            self.module,
        )

    def test_current_pointer_uses_atomic_replace(self) -> None:
        start = self.module.index(
            "def write_current_atomic("
        )
        end = self.module.index(
            "\ndef _parse_simple_frontmatter",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            'temporary.open("wb")',
            body,
        )
        self.assertIn(
            "os.fsync(handle.fileno())",
            body,
        )
        self.assertIn(
            "os.replace(",
            body,
        )
        self.assertNotIn(
            'pointer.open("wb")',
            body,
        )
        self.assertNotIn(
            "pointer.write_text(",
            body,
        )
        self.assertNotIn(
            "pointer.write_bytes(",
            body,
        )

    def test_generation_directories_are_verified_immutable(
        self,
    ) -> None:
        self.assertIn(
            "def _require_generation_immutability",
            self.module,
        )
        self.assertIn(
            "immutable generation changed",
            self.module,
        )

    def test_live_vault_digests_are_verified(self) -> None:
        self.assertIn(
            "real live generated digest changed",
            self.module,
        )
        self.assertIn(
            "real live views digest changed",
            self.module,
        )

    def test_reader_progress_is_per_cycle(self) -> None:
        self.assertIn(
            "before_samples = (",
            self.module,
        )
        self.assertIn(
            "reader.wait_for_progress(",
            self.module,
        )
        self.assertIn(
            "samples_during_promotions",
            self.module,
        )

    def test_reader_anomalies_are_all_tracked(
        self,
    ) -> None:
        for field in (
            "mixed_generation_count",
            "missing_entrypoint_count",
            "partial_generation_count",
            "parse_error_count",
        ):
            with self.subTest(field=field):
                self.assertIn(
                    field,
                    self.module,
                )

    def test_final_generation_is_gen_a(self) -> None:
        self.assertIn(
            'current["generation_id"]',
            self.module,
        )
        self.assertIn(
            '== "GEN_A"',
            self.module,
        )

    def test_automated_open_pass_is_not_full_p5c3_pass(
        self,
    ) -> None:
        self.assertIn(
            '"manual_visual_acceptance_required":',
            self.module,
        )
        self.assertIn(
            '"p5c3_qualified": False',
            self.module,
        )
        self.assertIn(
            '"obsidian_open_qualified": False',
            self.module,
        )

    def test_post_close_requires_manual_acceptance(
        self,
    ) -> None:
        self.assertIn(
            "manual visual acceptance not supplied",
            self.module,
        )
        self.assertIn(
            "--manual-visual-accepted",
            self.cli,
        )

    def test_post_close_requires_obsidian_closed(
        self,
    ) -> None:
        self.assertIn(
            "Obsidian must be fully closed before P5-C3 post-close verify",
            self.module,
        )

    def test_p5c3_never_authorizes_production(
        self,
    ) -> None:
        joined = self.module + "\n" + self.cli
        self.assertIn(
            '"production_promotion_authorized":',
            joined,
        )
        self.assertIn(
            '"continuous_observer_authorized":',
            joined,
        )
        self.assertNotIn(
            '"production_promotion_authorized": True',
            joined,
        )
        self.assertNotIn(
            '"continuous_observer_authorized": True',
            joined,
        )

    def test_graph_pointer_semantics_remain_unqualified(
        self,
    ) -> None:
        self.assertIn(
            '"graph_current_pointer_semantics_qualified":',
            self.module,
        )
        self.assertIn(
            "False",
            self.module,
        )

    def test_metrics_are_append_only_outside_vault(
        self,
    ) -> None:
        start = self.module.index(
            "def _append_event("
        )
        end = self.module.index(
            "\ndef prepare_open_experiment",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            'path.open("ab")',
            body,
        )
        self.assertIn(
            '"LOCALAPPDATA"',
            self.module,
        )

    def test_qualified_p5c2_implementation_blob_is_unchanged(
        self,
    ) -> None:
        import subprocess

        path = (
            "tools/obsidian_projection/"
            "promotion_experiment.py"
        )
        completed = subprocess.run(
            ["git", "hash-object", path],
            cwd=self.root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        self.assertEqual(
            completed.stdout.strip(),
            "b5ba13a6aa9ddf1690842aafea422973e15cdf2d",
        )

    def test_inherited_pointer_unit_is_deterministic(
        self,
    ) -> None:
        start = self.legacy_p5c2_test.index(
            "def test_pointer_candidate_has_zero_anomalies("
        )
        end = self.legacy_p5c2_test.index(
            "\n    @unittest.skipUnless(",
            start,
        )
        body = self.legacy_p5c2_test[start:end]
        self.assertIn(
            "class DeterministicReaderProbe:",
            body,
        )
        self.assertIn(
            '"ReaderProbe",',
            body,
        )
        self.assertIn(
            '"_wait_for_reader_progress",',
            body,
        )
        self.assertNotIn(
            '"READER_INTERVAL_SECONDS",',
            body,
        )

    def test_prepare_runner_orders_tests_before_prepare(
        self,
    ) -> None:
        targeted = self.prepare_runner.index(
            "=== TARGETED TESTS ==="
        )
        full = self.prepare_runner.index(
            "=== FULL OBSIDIAN SUITE ==="
        )
        prepare = self.prepare_runner.index(
            "=== P5-C3 PREPARE ==="
        )
        self.assertLess(targeted, full)
        self.assertLess(full, prepare)

    def test_runners_disable_bytecode(self) -> None:
        for runner in (
            self.prepare_runner,
            self.open_runner,
            self.post_runner,
        ):
            with self.subTest():
                self.assertIn(
                    'PYTHONDONTWRITEBYTECODE = "1"',
                    runner,
                )
                self.assertIn(
                    "python -B",
                    runner,
                )

    def test_runners_never_launch_obsidian(self) -> None:
        joined = (
            self.prepare_runner
            + "\n"
            + self.open_runner
            + "\n"
            + self.post_runner
        )
        for forbidden in (
            "Start-Process",
            "Invoke-Item",
            "obsidian://",
            "os.startfile",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_post_runner_requires_manual_acceptance_switch(
        self,
    ) -> None:
        self.assertIn(
            "[switch]$ManualVisualAccepted",
            self.post_runner,
        )
        self.assertIn(
            "--manual-visual-accepted",
            self.post_runner,
        )

    def test_no_git_mutation_commands(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "git push",
            "git commit",
            "git checkout",
            "git reset",
            "git clean",
            "git merge",
            "git rebase",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )


if __name__ == "__main__":
    unittest.main()
