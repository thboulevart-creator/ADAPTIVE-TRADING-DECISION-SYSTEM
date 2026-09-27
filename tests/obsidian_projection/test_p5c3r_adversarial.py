from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


class P5C3RAdversarialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[2]
        cls.module = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "obsidian_open_retry.py"
        ).read_text(encoding="utf-8")
        cls.cli = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5c3r_verify.py"
        ).read_text(encoding="utf-8")
        cls.recover_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3r_recover_control.ps1"
        ).read_text(encoding="utf-8")
        cls.open_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3r_open.ps1"
        ).read_text(encoding="utf-8")
        cls.post_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3r_post_close.ps1"
        ).read_text(encoding="utf-8")

    def test_retry_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            'CONTRACT_BLOB = "5648b2f7d3d3beb528539cd7c711c39210270064"',
            self.module,
        )

    def test_failed_base_open_harness_is_unchanged(
        self,
    ) -> None:
        path = (
            "tools/obsidian_projection/"
            "obsidian_open_compatibility.py"
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
            "b970e65f21792cccc6ee2e4271d630f371102ff7",
        )

    def test_write_retry_deadline_and_backoff_are_bounded(
        self,
    ) -> None:
        self.assertIn(
            "WRITE_RETRY_DEADLINE_SECONDS = 5.0",
            self.module,
        )
        self.assertIn(
            "WRITE_INITIAL_BACKOFF_SECONDS = 0.010",
            self.module,
        )
        self.assertIn(
            "WRITE_MAX_BACKOFF_SECONDS = 0.500",
            self.module,
        )

    def test_reader_retry_deadline_and_backoff_are_bounded(
        self,
    ) -> None:
        self.assertIn(
            "READ_RETRY_DEADLINE_SECONDS = 0.500",
            self.module,
        )
        self.assertIn(
            "READ_INITIAL_BACKOFF_SECONDS = 0.005",
            self.module,
        )
        self.assertIn(
            "READ_MAX_BACKOFF_SECONDS = 0.050",
            self.module,
        )

    def test_write_retry_only_accepts_winerror5(
        self,
    ) -> None:
        start = self.module.index(
            "def write_current_atomic_with_retry("
        )
        end = self.module.index(
            "\ndef recover_failed_p5c3(",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "except PermissionError as exc:",
            body,
        )
        self.assertIn(
            'getattr(exc, "winerror", None) != 5',
            body,
        )
        self.assertIn(
            "raise",
            body,
        )

    def test_atomic_temp_is_written_once_before_replace_loop(
        self,
    ) -> None:
        start = self.module.index(
            "def write_current_atomic_with_retry("
        )
        end = self.module.index(
            "\ndef recover_failed_p5c3(",
            start,
        )
        body = self.module[start:end]

        write_index = body.index(
            'with temporary.open("xb")'
        )
        loop_index = body.index(
            "while True:"
        )
        self.assertLess(
            write_index,
            loop_index,
        )
        self.assertEqual(
            body.count('temporary.open("xb")'),
            1,
        )
        self.assertIn(
            "os.replace(temporary, pointer)",
            body,
        )

    def test_temp_integrity_checked_after_retryable_failure(
        self,
    ) -> None:
        start = self.module.index(
            "def write_current_atomic_with_retry("
        )
        end = self.module.index(
            "\ndef recover_failed_p5c3(",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "CURRENT.tmp missing after retryable replace failure",
            body,
        )
        self.assertIn(
            "CURRENT.tmp changed after retryable replace failure",
            body,
        )
        self.assertIn(
            "CURRENT changed despite failed atomic replace",
            body,
        )

    def test_success_requires_exact_candidate_bytes(
        self,
    ) -> None:
        self.assertIn(
            "successful CURRENT replace bytes differ from candidate",
            self.module,
        )
        self.assertIn(
            "successful CURRENT replace generation mismatch",
            self.module,
        )
        self.assertIn(
            "successful CURRENT replace digest mismatch",
            self.module,
        )

    def test_reader_retries_only_underlying_winerror5(
        self,
    ) -> None:
        start = self.module.index(
            "def validate_current_with_access_retry("
        )
        end = self.module.index(
            "\n@dataclass\nclass ReplaceRetryStats",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "if not _is_winerror_5(exc):",
            body,
        )
        self.assertIn(
            "ReaderAccessRetryDeadlineExceeded",
            body,
        )

    def test_recovery_requires_obsidian_closed(
        self,
    ) -> None:
        start = self.module.index(
            "def recover_failed_p5c3("
        )
        end = self.module.index(
            "\ndef _open_no_delete_share(",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "Obsidian must be closed during P5-C3R recovery",
            body,
        )
        self.assertNotIn(
            "build_markdown_generation(",
            body,
        )
        self.assertIn(
            "stale CURRENT.tmp does not match expected failed GEN_B candidate",
            body,
        )
        self.assertIn(
            "temporary.unlink()",
            body,
        )

    def test_synthetic_lock_denies_delete_share(
        self,
    ) -> None:
        start = self.module.index(
            "def _open_no_delete_share("
        )
        end = self.module.index(
            "\ndef _close_handle(",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "FILE_SHARE_READ | FILE_SHARE_WRITE",
            body,
        )
        self.assertNotIn(
            "FILE_SHARE_DELETE",
            body,
        )

    def test_synthetic_lock_must_observe_conflict(
        self,
    ) -> None:
        self.assertIn(
            "synthetic lock breaker observed zero access-denied conflicts",
            self.module,
        )
        self.assertIn(
            "lock_release_delay_ms",
            self.module,
        )

    def test_open_experiment_preserves_250_and_5000(
        self,
    ) -> None:
        self.assertIn(
            "PROMOTION_CYCLES = 250",
            self.module,
        )
        self.assertIn(
            "MIN_READER_SAMPLES = 5000",
            self.module,
        )

    def test_open_experiment_tracks_retry_metrics(
        self,
    ) -> None:
        for required in (
            '"total_replace_attempts":',
            '"access_denied_retry_conflict_count":',
            '"max_retry_depth":',
            '"max_promotion_latency_ms":',
            '"reader_access_denied_retry_count":',
            '"reader_terminal_access_error_count":',
            '"semantic_partial_generation_count":',
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_open_experiment_persists_failure_evidence(
        self,
    ) -> None:
        self.assertIn(
            '"failure_phase":',
            self.module,
        )
        self.assertIn(
            '"failure_cycle":',
            self.module,
        )
        self.assertIn(
            '"failure_type":',
            self.module,
        )
        self.assertIn(
            '"failure_message":',
            self.module,
        )
        self.assertIn(
            "event_log = _append_event(report)",
            self.module,
        )

    def test_event_log_is_append_only(self) -> None:
        start = self.module.index(
            "def _append_event("
        )
        end = self.module.index(
            "\ndef _is_winerror_5(",
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

    def test_post_close_still_denies_production(
        self,
    ) -> None:
        self.assertIn(
            '"production_promotion_authorized": False',
            self.module,
        )
        self.assertIn(
            '"continuous_observer_authorized": False',
            self.module,
        )
        self.assertIn(
            '"graph_current_pointer_semantics_qualified": False',
            self.module,
        )

    def test_cli_exposes_only_governed_modes(
        self,
    ) -> None:
        for mode in (
            "--recover",
            "--synthetic-lock-breaker",
            "--run-open",
            "--post-close",
        ):
            with self.subTest(mode=mode):
                self.assertIn(
                    mode,
                    self.cli,
                )

    def test_recovery_runner_orders_qualification_before_recovery(
        self,
    ) -> None:
        targeted = self.recover_runner.index(
            "=== TARGETED TESTS ==="
        )
        full = self.recover_runner.index(
            "=== FULL OBSIDIAN SUITE ==="
        )
        lock = self.recover_runner.index(
            "=== SYNTHETIC WINDOWS LOCK BREAKER ==="
        )
        recovery = self.recover_runner.index(
            "=== RECOVER FAILED P5-C3 STATE ==="
        )
        self.assertLess(targeted, full)
        self.assertLess(full, lock)
        self.assertLess(lock, recovery)

    def test_recovery_runner_requires_obsidian_closed(
        self,
    ) -> None:
        self.assertIn(
            'Get-Process -Name "Obsidian"',
            self.recover_runner,
        )
        self.assertIn(
            "close Obsidian completely before P5-C3R recovery",
            self.recover_runner,
        )

    def test_open_runner_prechecks_before_retry_experiment(
        self,
    ) -> None:
        diagnostic = self.open_runner.index(
            "=== P5-C3R READ-ONLY PRECHECK ==="
        )
        experiment = self.open_runner.index(
            "=== P5-C3R RETRY OPEN EXPERIMENT ==="
        )
        self.assertLess(
            diagnostic,
            experiment,
        )
        self.assertIn(
            "--diagnose-open",
            self.open_runner,
        )
        self.assertIn(
            "--run-open",
            self.open_runner,
        )

    def test_post_runner_requires_manual_acceptance(
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

    def test_runners_have_no_obsidian_launch_or_reset(
        self,
    ) -> None:
        joined = (
            self.recover_runner
            + "\n"
            + self.open_runner
            + "\n"
            + self.post_runner
        )
        for forbidden in (
            "Start-Process",
            "Invoke-Item",
            "obsidian://",
            "run_p5c3_reset.ps1",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )

    def test_no_git_mutation_or_obsidian_launch(self) -> None:
        joined = self.module + "\n" + self.cli
        for forbidden in (
            "git push",
            "git commit",
            "git checkout",
            "git reset",
            "git clean",
            "Start-Process",
            "obsidian://",
            "os.startfile",
            "subprocess.Popen",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    joined,
                )


if __name__ == "__main__":
    unittest.main()
