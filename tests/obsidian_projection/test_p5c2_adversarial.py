from __future__ import annotations

import unittest
from pathlib import Path


class P5C2AdversarialStaticTests(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "promotion_experiment.py"
        ).read_text(encoding="utf-8")
        cls.cli = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5c2_verify.py"
        ).read_text(encoding="utf-8")

    def test_p5c_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            "36e49e72a867e30a69f63eb413fd924d0e56297b",
            self.module,
        )

    def test_live_vault_and_sandbox_are_distinct(
        self,
    ) -> None:
        self.assertIn(
            "ATDS-OBSIDIAN-PROJECTION",
            self.module,
        )
        self.assertIn(
            "ATDS-P5C-PROMOTION-SANDBOX",
            self.module,
        )
        self.assertIn(
            "sandbox overlaps live Vault",
            self.module,
        )

    def test_experiment_scale_is_pinned(self) -> None:
        self.assertIn(
            "FILES_PER_GENERATION = 128",
            self.module,
        )
        self.assertIn(
            "NESTED_DIRECTORIES = 8",
            self.module,
        )
        self.assertIn(
            "QUALIFIABLE_CYCLES = 250",
            self.module,
        )
        self.assertIn(
            "MIN_READER_SAMPLES = 5000",
            self.module,
        )
        self.assertIn(
            "READER_INTERVAL_SECONDS = 0.001",
            self.module,
        )

    def test_negative_control_is_required_before_candidates(
        self,
    ) -> None:
        negative_index = self.module.index(
            "negative = run_negative_control("
        )
        two_rename_index = self.module.index(
            "two_rename = run_two_rename_swap("
        )
        self.assertLess(
            negative_index,
            two_rename_index,
        )
        self.assertIn(
            "NEGATIVE_CONTROL_DID_NOT_DETECT_NON_ATOMICITY",
            self.module,
        )

    def test_all_three_qualifiable_candidates_exist(
        self,
    ) -> None:
        for required in (
            "DIRECTORY_TWO_RENAME_SWAP",
            "WINDOWS_MOVEFILEEX_DIRECTORY_REPLACE",
            "IMMUTABLE_GENERATION_ATOMIC_POINTER",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_reader_classifies_all_required_anomalies(
        self,
    ) -> None:
        for required in (
            "mixed_generation_count",
            "missing_entrypoint_count",
            "partial_generation_count",
            "parse_error_count",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_pointer_uses_replace_not_in_place_write(
        self,
    ) -> None:
        start = self.module.index(
            "def _write_pointer("
        )
        end = self.module.index(
            "\ndef validate_pointer_entry",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            "os.replace(temporary, pointer)",
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

    def test_two_rename_has_explicit_missing_window_candidate(
        self,
    ) -> None:
        start = self.module.index(
            "def run_two_rename_swap("
        )
        end = self.module.index(
            "\ndef _movefileex",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            "os.replace(live, backup)",
            body,
        )
        self.assertIn(
            "os.replace(stage, live)",
            body,
        )

    def test_movefileex_is_measured_not_assumed(
        self,
    ) -> None:
        self.assertIn(
            "MOVEFILE_REPLACE_EXISTING",
            self.module,
        )
        self.assertIn(
            "MOVEFILE_WRITE_THROUGH",
            self.module,
        )
        self.assertIn(
            "NOT_SUPPORTED",
            self.module,
        )
        self.assertIn(
            "MOVEFILEEX_ERROR_",
            self.module,
        )

    def test_all_fail_is_preserved(self) -> None:
        self.assertIn(
            "ALL_CANDIDATES_REJECTED",
            self.module,
        )
        self.assertIn(
            'status = "FAIL"',
            self.module,
        )

    def test_multiple_passes_require_adjudication(
        self,
    ) -> None:
        self.assertIn(
            "MULTIPLE_CANDIDATES_REQUIRE_ADJUDICATION",
            self.module,
        )
        self.assertIn(
            'status = "BLOCKED"',
            self.module,
        )

    def test_filesystem_pass_does_not_authorize_production(
        self,
    ) -> None:
        self.assertIn(
            '"obsidian_open_qualified": False',
            self.module,
        )
        self.assertIn(
            '"production_promotion_authorized":',
            self.module,
        )
        self.assertIn(
            "False",
            self.module,
        )

    def test_metrics_are_append_only(self) -> None:
        start = self.module.index(
            "def append_metrics_event("
        )
        end = self.module.index(
            "\ndef prepare_sandbox",
            start,
        )
        body = self.module[start:end]
        self.assertIn(
            'path.open("ab")',
            body,
        )
        self.assertNotIn(
            'path.open("wb")',
            body,
        )

    def test_metrics_are_outside_live_vault(self) -> None:
        self.assertIn(
            '"LOCALAPPDATA"',
            self.module,
        )
        self.assertIn(
            '"promotion-events.jsonl"',
            self.module,
        )

    def test_sandbox_must_be_absent(self) -> None:
        self.assertIn(
            "sandbox must be absent before experiment",
            self.module,
        )
        self.assertIn(
            "sandbox already exists",
            self.cli,
        )

    def test_cli_preflight_cannot_authorize_experiment(
        self,
    ) -> None:
        self.assertIn(
            '"experiment_authorized_by_preflight":',
            self.cli,
        )
        self.assertIn(
            "False",
            self.cli,
        )

    def test_cli_blocked_report_denies_production(
        self,
    ) -> None:
        self.assertIn(
            '"production_promotion_authorized": False',
            self.cli,
        )
        self.assertIn(
            '"live_vault_modified": False',
            self.cli,
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

    def test_no_obsidian_or_plugin_automation(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "obsidian://",
            "community-plugins.json",
            "core-plugins.json",
            "os.startfile",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )


if __name__ == "__main__":
    unittest.main()
