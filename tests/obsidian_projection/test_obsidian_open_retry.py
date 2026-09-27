from __future__ import annotations

import errno
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.obsidian_open_compatibility import (
    OpenPointerPartialError,
    build_markdown_generation,
    validate_current_pointer,
    write_current_atomic,
)
from tools.obsidian_projection.obsidian_open_retry import (
    ReaderAccessRetryDeadlineExceeded,
    ReaderAccessTelemetry,
    ReplaceRetryDeadlineExceeded,
    RetryReaderProbe,
    _semantic_partial_signature,
    run_synthetic_lock_breaker,
    validate_current_with_access_retry,
    write_current_atomic_with_retry,
)


class WinError5(PermissionError):
    def __init__(self) -> None:
        super().__init__(13, "Access denied")
        self.winerror = 5


class WinError32(PermissionError):
    def __init__(self) -> None:
        super().__init__(13, "Sharing violation")
        self.winerror = 32


class WinError33(PermissionError):
    def __init__(self) -> None:
        super().__init__(13, "Lock violation")
        self.winerror = 33


class P5C3RRetryTests(unittest.TestCase):
    def _fixture(
        self,
        root: Path,
    ) -> dict[str, dict]:
        generations = root / "generations"
        generations.mkdir()
        manifests = {}
        for generation_id in (
            "GEN_A",
            "GEN_B",
        ):
            manifests[generation_id] = (
                build_markdown_generation(
                    generations / generation_id,
                    generation_id,
                )
            )

        write_current_atomic(
            root,
            "GEN_A",
            manifests["GEN_A"][
                "generation_tree_digest_sha256"
            ],
        )
        return manifests

    def test_write_retry_absorbs_one_winerror5(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifests = self._fixture(root)

            real_replace = os.replace
            calls = 0

            def flaky_replace(
                source,
                destination,
            ) -> None:
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise WinError5()
                real_replace(
                    source,
                    destination,
                )

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_retry.os.replace",
                side_effect=flaky_replace,
            ):
                stats = (
                    write_current_atomic_with_retry(
                        root,
                        "GEN_B",
                        manifests["GEN_B"][
                            "generation_tree_digest_sha256"
                        ],
                        expected_old_generation_id=
                            "GEN_A",
                    )
                )

            self.assertEqual(
                stats.attempts,
                2,
            )
            self.assertEqual(
                stats.access_denied_conflicts,
                1,
            )
            self.assertEqual(
                validate_current_pointer(
                    root
                )["generation_id"],
                "GEN_B",
            )
            self.assertFalse(
                (root / "CURRENT.tmp").exists()
            )

    def test_write_retry_absorbs_one_winerror32(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifests = self._fixture(root)

            real_replace = os.replace
            calls = 0

            def flaky_replace(
                source,
                destination,
            ) -> None:
                nonlocal calls
                calls += 1
                if calls == 1:
                    raise WinError32()
                real_replace(
                    source,
                    destination,
                )

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_retry.os.replace",
                side_effect=flaky_replace,
            ):
                stats = (
                    write_current_atomic_with_retry(
                        root,
                        "GEN_B",
                        manifests["GEN_B"][
                            "generation_tree_digest_sha256"
                        ],
                        expected_old_generation_id=
                            "GEN_A",
                    )
                )

            self.assertEqual(
                stats.attempts,
                2,
            )
            self.assertEqual(
                stats.access_denied_conflicts,
                1,
            )
            self.assertEqual(
                validate_current_pointer(
                    root
                )["generation_id"],
                "GEN_B",
            )

    def test_write_retry_does_not_retry_other_winerror(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifests = self._fixture(root)

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_retry.os.replace",
                side_effect=WinError33(),
            ):
                with self.assertRaises(
                    WinError33
                ):
                    write_current_atomic_with_retry(
                        root,
                        "GEN_B",
                        manifests["GEN_B"][
                            "generation_tree_digest_sha256"
                        ],
                        expected_old_generation_id=
                            "GEN_A",
                    )

            self.assertEqual(
                validate_current_pointer(
                    root
                )["generation_id"],
                "GEN_A",
            )

    def test_write_retry_rejects_reader_only_eacces_fallback(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifests = self._fixture(root)
            denied = PermissionError(
                errno.EACCES,
                "Permission denied",
            )

            with patch(
                "tools.obsidian_projection."
                "obsidian_open_retry.os.replace",
                side_effect=denied,
            ):
                with self.assertRaises(
                    PermissionError
                ):
                    write_current_atomic_with_retry(
                        root,
                        "GEN_B",
                        manifests["GEN_B"][
                            "generation_tree_digest_sha256"
                        ],
                        expected_old_generation_id=
                            "GEN_A",
                    )

            self.assertEqual(
                validate_current_pointer(
                    root
                )["generation_id"],
                "GEN_A",
            )

    def test_write_retry_deadline_is_terminal(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifests = self._fixture(root)

            with (
                patch(
                    "tools.obsidian_projection."
                    "obsidian_open_retry.os.replace",
                    side_effect=WinError5(),
                ),
                patch(
                    "tools.obsidian_projection."
                    "obsidian_open_retry."
                    "WRITE_RETRY_DEADLINE_SECONDS",
                    0.015,
                ),
                patch(
                    "tools.obsidian_projection."
                    "obsidian_open_retry."
                    "WRITE_INITIAL_BACKOFF_SECONDS",
                    0.005,
                ),
                patch(
                    "tools.obsidian_projection."
                    "obsidian_open_retry."
                    "WRITE_MAX_BACKOFF_SECONDS",
                    0.005,
                ),
            ):
                with self.assertRaises(
                    ReplaceRetryDeadlineExceeded
                ):
                    write_current_atomic_with_retry(
                        root,
                        "GEN_B",
                        manifests["GEN_B"][
                            "generation_tree_digest_sha256"
                        ],
                        expected_old_generation_id=
                            "GEN_A",
                    )

            self.assertEqual(
                validate_current_pointer(
                    root
                )["generation_id"],
                "GEN_A",
            )
            self.assertTrue(
                (root / "CURRENT.tmp").exists()
            )

    def test_reader_access_denied_is_retried(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()
        calls = 0

        def flaky_validator(_root):
            nonlocal calls
            calls += 1
            if calls == 1:
                try:
                    raise WinError5()
                except WinError5 as exc:
                    raise OpenPointerPartialError(
                        "CURRENT.md unreadable"
                    ) from exc
            return {
                "generation_id": "GEN_A",
                "generation_tree_digest_sha256":
                    "a" * 64,
            }

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_pointer",
            side_effect=flaky_validator,
        ):
            result = (
                validate_current_with_access_retry(
                    Path("unused"),
                    telemetry,
                )
            )

        self.assertEqual(
            result["generation_id"],
            "GEN_A",
        )
        self.assertEqual(
            telemetry.access_denied_retry_count,
            1,
        )
        self.assertEqual(
            telemetry.terminal_access_error_count,
            0,
        )

    def test_reader_retries_permissionerror_eacces_without_winerror(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()
        calls = 0

        def flaky_validator(_root):
            nonlocal calls
            calls += 1
            if calls == 1:
                try:
                    raise PermissionError(
                        errno.EACCES,
                        "Permission denied",
                    )
                except PermissionError as exc:
                    self.assertIsNone(
                        getattr(
                            exc,
                            "winerror",
                            None,
                        )
                    )
                    raise OpenPointerPartialError(
                        "CURRENT.md unreadable"
                    ) from exc
            return {
                "generation_id": "GEN_A",
                "generation_tree_digest_sha256":
                    "a" * 64,
            }

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_pointer",
            side_effect=flaky_validator,
        ):
            result = validate_current_with_access_retry(
                Path("unused"),
                telemetry,
            )

        self.assertEqual(
            result["generation_id"],
            "GEN_A",
        )
        self.assertEqual(
            telemetry.access_denied_retry_count,
            1,
        )
        self.assertEqual(
            telemetry.eacces_without_winerror_retry_count,
            1,
        )
        self.assertEqual(
            telemetry.terminal_access_error_count,
            0,
        )

    def test_reader_eacces_deadline_is_terminal(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()

        def denied(_root):
            try:
                raise PermissionError(
                    errno.EACCES,
                    "Permission denied",
                )
            except PermissionError as exc:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from exc

        with (
            patch(
                "tools.obsidian_projection."
                "obsidian_open_retry."
                "validate_current_pointer",
                side_effect=denied,
            ),
            patch(
                "tools.obsidian_projection."
                "obsidian_open_retry."
                "READ_RETRY_DEADLINE_SECONDS",
                0.015,
            ),
            patch(
                "tools.obsidian_projection."
                "obsidian_open_retry."
                "READ_INITIAL_BACKOFF_SECONDS",
                0.005,
            ),
            patch(
                "tools.obsidian_projection."
                "obsidian_open_retry."
                "READ_MAX_BACKOFF_SECONDS",
                0.005,
            ),
        ):
            with self.assertRaises(
                ReaderAccessRetryDeadlineExceeded
            ):
                validate_current_with_access_retry(
                    Path("unused"),
                    telemetry,
                )

        self.assertGreater(
            telemetry.access_denied_retry_count,
            0,
        )
        self.assertEqual(
            telemetry.eacces_without_winerror_retry_count,
            telemetry.access_denied_retry_count,
        )
        self.assertEqual(
            telemetry.terminal_access_error_count,
            1,
        )

    def test_reader_does_not_retry_eacces_with_nonretryable_winerror(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()

        def denied(_root):
            try:
                raise WinError33()
            except WinError33 as exc:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from exc

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_pointer",
            side_effect=denied,
        ):
            with self.assertRaises(
                OpenPointerPartialError
            ):
                validate_current_with_access_retry(
                    Path("unused"),
                    telemetry,
                )

        self.assertEqual(
            telemetry.access_denied_retry_count,
            0,
        )
        self.assertEqual(
            telemetry.eacces_without_winerror_retry_count,
            0,
        )

    def test_reader_does_not_retry_nonpermission_eacces(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()

        def denied(_root):
            try:
                raise OSError(
                    errno.EACCES,
                    "Permission denied",
                )
            except OSError as exc:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from exc

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_pointer",
            side_effect=denied,
        ):
            with self.assertRaises(
                OpenPointerPartialError
            ):
                validate_current_with_access_retry(
                    Path("unused"),
                    telemetry,
                )

        self.assertEqual(
            telemetry.access_denied_retry_count,
            0,
        )
        self.assertEqual(
            telemetry.eacces_without_winerror_retry_count,
            0,
        )

    def test_reader_semantic_partial_is_not_retried(
        self,
    ) -> None:
        telemetry = ReaderAccessTelemetry()

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_pointer",
            side_effect=OpenPointerPartialError(
                "semantic digest mismatch"
            ),
        ):
            with self.assertRaises(
                OpenPointerPartialError
            ):
                validate_current_with_access_retry(
                    Path("unused"),
                    telemetry,
                )

        self.assertEqual(
            telemetry.access_denied_retry_count,
            0,
        )

    def test_semantic_partial_signature_captures_file_not_found_cause(
        self,
    ) -> None:
        captured = None
        try:
            try:
                raise FileNotFoundError(
                    2,
                    "No such file or directory",
                )
            except FileNotFoundError as cause:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from cause
        except OpenPointerPartialError as exc:
            captured = _semantic_partial_signature(
                exc
            )

        self.assertEqual(
            captured,
            (
                "message=CURRENT.md unreadable"
                "|cause_type=FileNotFoundError"
                "|errno=2"
                "|winerror=None"
            ),
        )

    def test_reader_records_semantic_partial_signature_without_retrying(
        self,
    ) -> None:
        reader = RetryReaderProbe()

        def one_partial(_root, _telemetry):
            reader._stop.set()
            try:
                raise FileNotFoundError(
                    2,
                    "No such file or directory",
                )
            except FileNotFoundError as cause:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from cause

        with patch(
            "tools.obsidian_projection."
            "obsidian_open_retry."
            "validate_current_with_access_retry",
            side_effect=one_partial,
        ):
            reader._run()

        self.assertEqual(
            reader.metrics.samples,
            1,
        )
        self.assertEqual(
            reader.metrics.semantic_partial_generation_count,
            1,
        )
        self.assertEqual(
            sum(
                reader.metrics.semantic_partial_signatures.values()
            ),
            1,
        )
        self.assertEqual(
            reader.access.access_denied_retry_count,
            0,
        )
        self.assertIn(
            (
                "message=CURRENT.md unreadable"
                "|cause_type=FileNotFoundError"
                "|errno=2"
                "|winerror=None"
            ),
            reader.metrics.semantic_partial_signatures,
        )

    def test_semantic_partial_signature_captures_nonretryable_winerror(
        self,
    ) -> None:
        captured = None
        try:
            try:
                raise WinError33()
            except WinError33 as cause:
                raise OpenPointerPartialError(
                    "CURRENT.md unreadable"
                ) from cause
        except OpenPointerPartialError as exc:
            captured = _semantic_partial_signature(
                exc
            )

        self.assertIn(
            "|cause_type=WinError33",
            captured,
        )
        self.assertIn(
            "|winerror=33",
            captured,
        )

    @unittest.skipUnless(
        os.name == "nt",
        "Windows sharing-lock breaker",
    )
    def test_real_windows_no_delete_share_lock_is_retried(
        self,
    ) -> None:
        report = run_synthetic_lock_breaker()

        self.assertEqual(
            report["status"],
            "PASS",
        )
        self.assertGreater(
            report[
                "replace_stats"
            ]["access_denied_conflicts"],
            0,
        )
        self.assertEqual(
            report["final_generation"],
            "GEN_B",
        )
        self.assertFalse(
            report["stale_temp_present"]
        )


if __name__ == "__main__":
    unittest.main()
