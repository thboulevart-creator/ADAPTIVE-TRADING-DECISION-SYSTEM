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
        cls.r2_cli = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "p5c3r2_verify.py"
        ).read_text(encoding="utf-8")
        cls.r2_open_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3r2_open.ps1"
        ).read_text(encoding="utf-8")
        cls.r2_post_runner = (
            cls.root
            / "tools"
            / "obsidian_projection"
            / "run_p5c3r2_post_close.ps1"
        ).read_text(encoding="utf-8")

    def test_retry_contract_blob_is_pinned(self) -> None:
        self.assertIn(
            'CONTRACT_BLOB = "a3fb7736f2c25f144b1d9bc4a50cbf4029e3dc33"',
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

    def test_write_retry_only_accepts_sharing_conflicts_5_and_32(
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
            'not in {5, 32}',
            body,
        )
        self.assertIn(
            "raise",
            body,
        )

    def test_write_path_does_not_accept_reader_eacces_fallback(
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
            'not in {5, 32}',
            body,
        )
        self.assertNotIn(
            "errno.EACCES",
            body,
        )
        self.assertNotIn(
            "_is_retryable_reader_access_conflict(",
            body,
        )

    def test_reader_helper_requires_permissionerror_for_eacces(
        self,
    ) -> None:
        start = self.module.index(
            "def _is_retryable_reader_access_conflict("
        )
        end = self.module.index(
            "\ndef _is_reader_eacces_without_winerror(",
            start,
        )
        body = self.module[start:end]

        self.assertIn(
            "isinstance(current, PermissionError)",
            body,
        )
        self.assertIn(
            "winerror in {5, 32}",
            body,
        )
        self.assertIn(
            "winerror is None",
            body,
        )
        self.assertIn(
            "errno.EACCES",
            body,
        )

    def test_p5c3r2_runtime_identity_is_separate(
        self,
    ) -> None:
        self.assertIn(
            'RETRY_METRICS_SCHEMA = "ATDS_OBSIDIAN_P5C3R2_OPEN_METRICS_V0_1"',
            self.module,
        )
        event_start = self.module.index(
            "def _event_log_path("
        )
        event_end = self.module.index(
            "\ndef _append_event(",
            event_start,
        )
        event_body = self.module[
            event_start:event_end
        ]
        self.assertIn(
            '/ "p5c3r2"',
            event_body,
        )
        self.assertNotIn(
            '/ "p5c3r"\n',
            event_body,
        )

    def test_p5c3r2_auxiliary_report_schemas_are_separate(
        self,
    ) -> None:
        self.assertIn(
            'LOCK_BREAKER_SCHEMA = "ATDS_OBSIDIAN_P5C3R2_SYNTHETIC_LOCK_BREAKER_V0_1"',
            self.module,
        )
        self.assertIn(
            'POST_CLOSE_SCHEMA = "ATDS_OBSIDIAN_P5C3R2_POST_CLOSE_REPORT_V0_1"',
            self.module,
        )

    def test_predecessor_open_runner_is_unchanged(
        self,
    ) -> None:
        path = (
            "tools/obsidian_projection/"
            "run_p5c3r_open.ps1"
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
            "ea6dc7d45d98df9507db4015d4e15b76fbc1fd52",
        )

    def test_p5c3r2_cli_exposes_no_recovery_mode(
        self,
    ) -> None:
        for required in (
            "--synthetic-lock-breaker",
            "--run-open",
            "--post-close",
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.r2_cli,
                )
        self.assertNotIn(
            '"--recover"',
            self.r2_cli,
        )

    def test_p5c3r2_runner_binds_new_cli(
        self,
    ) -> None:
        diagnostic = self.r2_open_runner.index(
            "=== P5-C3R2 READ-ONLY PRECHECK ==="
        )
        experiment = self.r2_open_runner.index(
            "=== P5-C3R2 READER-EACCES OPEN EXPERIMENT ==="
        )
        self.assertLess(
            diagnostic,
            experiment,
        )
        self.assertIn(
            "tools.obsidian_projection."
            "p5c3_verify --diagnose-open",
            self.r2_open_runner,
        )
        self.assertIn(
            "tools.obsidian_projection."
            "p5c3r2_verify --run-open",
            self.r2_open_runner,
        )
        self.assertNotIn(
            "tools.obsidian_projection."
            "p5c3r_verify --run-open",
            self.r2_open_runner,
        )

    def test_predecessor_post_close_runner_is_unchanged(
        self,
    ) -> None:
        path = (
            "tools/obsidian_projection/"
            "run_p5c3r_post_close.ps1"
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
            "1409ed062e7a1546ad0d7afa42168d8c47312840",
        )

    def test_p5c3r2_post_close_runner_binds_new_cli(
        self,
    ) -> None:
        self.assertIn(
            "[switch]$ManualVisualAccepted",
            self.r2_post_runner,
        )
        self.assertIn(
            "tools.obsidian_projection."
            "p5c3r2_verify",
            self.r2_post_runner,
        )
        self.assertIn(
            "--post-close",
            self.r2_post_runner,
        )
        self.assertNotIn(
            "tools.obsidian_projection."
            "p5c3r_verify --post-close",
            self.r2_post_runner,
        )

    def test_p5c3r2_post_close_preserves_predecessor_failure(
        self,
    ) -> None:
        start = self.module.index(
            "def post_close_retry_verify("
        )
        body = self.module[start:]
        self.assertIn(
            '"p5c3r_qualified": False',
            body,
        )
        self.assertIn(
            '"p5c3r2_qualified": True',
            body,
        )
        self.assertIn(
            '"production_promotion_authorized": False',
            body,
        )
        self.assertIn(
            '"continuous_observer_authorized": False',
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

    def test_reader_retry_policy_is_distinct_from_write_policy(
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
            "if not _is_retryable_reader_access_conflict(",
            body,
        )
        self.assertIn(
            "ReaderAccessRetryDeadlineExceeded",
            body,
        )
        self.assertIn(
            "_is_reader_eacces_without_winerror(",
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
            '"reader_eacces_without_winerror_retry_count":',
            '"semantic_partial_generation_count":',
            '"semantic_partial_signature_total_count":',
            '"semantic_partial_signatures":',
        ):
            with self.subTest(required=required):
                self.assertIn(
                    required,
                    self.module,
                )

    def test_forensic_instrumentation_does_not_relax_failure_policy(
        self,
    ) -> None:
        self.assertIn(
            "metrics.semantic_partial_generation_count == 0",
            self.module,
        )
        self.assertIn(
            "except OpenPointerPartialError as exc:",
            self.module,
        )
        self.assertIn(
            "_semantic_partial_signature(",
            self.module,
        )
        self.assertIn(
            "not in {5, 32}",
            self.module,
        )
        self.assertIn(
            "metrics.semantic_partial_generation_count == 0",
            self.module,
        )
        self.assertIn(
            "reader_eacces_without_winerror_retry_count",
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
            "\ndef _is_retryable_sharing_conflict(",
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
            "python -B -m tools.obsidian_projection."
            "p5c3_verify --diagnose-open",
            self.open_runner,
        )
        self.assertIn(
            "python -B -m tools.obsidian_projection."
            "p5c3r_verify --run-open",
            self.open_runner,
        )
        self.assertNotIn(
            "tools.obsidian_projection."
            "p5c3r_verify --diagnose-open",
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
            + "\n"
            + self.r2_open_runner
            + "\n"
            + self.r2_post_runner
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
        joined = (
            self.module
            + "\n"
            + self.cli
            + "\n"
            + self.r2_cli
            + "\n"
            + self.r2_open_runner
            + "\n"
            + self.r2_post_runner
        )
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
