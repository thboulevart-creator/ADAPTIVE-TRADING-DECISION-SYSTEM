from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection import (
    persistent_production_handoff as handoff,
)


class P5D3FPersistentHandoffRecoveryImplementationV03Tests(
    unittest.TestCase
):
    def test_recovery_contract_authority_pin_is_exact(self) -> None:
        self.assertEqual(
            handoff.RECOVERY_GATE_CONTRACT_BLOB,
            "aef627936b6f745017bcace7e8a3e44270f95674",
        )

    def test_exact_empty_packages_recovery_state_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-empty-packages-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            (staging / "packages").mkdir()

            self.assertEqual(
                handoff.validate_staging_prestate(
                    staging
                ),
                "PRESENT_EMPTY_PACKAGES_RECOVERY",
            )

    def test_nonempty_packages_recovery_state_blocks(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-nonempty-packages-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            packages = staging / "packages"
            packages.mkdir()
            (packages / "residual.txt").write_text(
                "residual\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                handoff.PersistentHandoffBlockedError
            ):
                handoff.validate_staging_prestate(
                    staging
                )

    def test_extra_top_level_entry_blocks_recovery(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-extra-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            (staging / "packages").mkdir()
            (staging / "extra").mkdir()

            with self.assertRaises(
                handoff.PersistentHandoffBlockedError
            ):
                handoff.validate_staging_prestate(
                    staging
                )

    def test_promotion_handoff_record_blocks_recovery(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-handoff-record-"
        ) as temp:
            staging = Path(temp) / "staging"
            staging.mkdir()
            (staging / "packages").mkdir()
            (
                staging / "PROMOTION-HANDOFF.json"
            ).write_text(
                "{}\n",
                encoding="utf-8",
            )

            with self.assertRaises(
                handoff.PersistentHandoffBlockedError
            ):
                handoff.validate_staging_prestate(
                    staging
                )

    def test_absent_prestate_may_transition_to_present_empty_after_setup(
        self,
    ) -> None:
        self.assertTrue(
            handoff._staging_prestate_transition_allowed(
                "ABSENT",
                "PRESENT_EMPTY",
            )
        )

    def test_recovery_prestate_must_remain_exact(self) -> None:
        self.assertTrue(
            handoff._staging_prestate_transition_allowed(
                "PRESENT_EMPTY_PACKAGES_RECOVERY",
                "PRESENT_EMPTY_PACKAGES_RECOVERY",
            )
        )

    def test_unexpected_staging_prestate_transition_is_rejected(
        self,
    ) -> None:
        self.assertFalse(
            handoff._staging_prestate_transition_allowed(
                "PRESENT_EMPTY",
                "PRESENT_EMPTY_PACKAGES_RECOVERY",
            )
        )

    def test_body_failure_annotation_preserves_original_exception(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-body-failure-"
        ) as temp:
            temp_root = Path(temp)
            original = ValueError(
                "FIRST_FAILURE"
            )

            returned = handoff._annotate_body_failure(
                original,
                temp_root,
            )

            self.assertIs(
                returned,
                original,
            )
            self.assertEqual(
                str(returned),
                "FIRST_FAILURE",
            )
            self.assertEqual(
                getattr(
                    returned,
                    "p5d3f_temp_root",
                ),
                str(temp_root),
            )
            self.assertTrue(
                temp_root.exists()
            )

    def test_post_success_cleanup_failure_is_distinct_and_binds_result(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="p5d3f-recovery-cleanup-"
        ) as temp:
            temp_root = Path(temp)
            result = {
                "status":
                    "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED",
                "generation_id": "gen-test",
            }

            with patch(
                "tools.obsidian_projection."
                "persistent_production_handoff.shutil.rmtree",
                side_effect=PermissionError(
                    "cleanup denied"
                ),
            ):
                with self.assertRaises(
                    handoff.PersistentHandoffPostSuccessCleanupBlockedError
                ) as caught:
                    handoff._cleanup_temp_root_after_success(
                        temp_root,
                        result,
                    )

            exc = caught.exception
            self.assertEqual(
                str(exc),
                "BLOCKED_TEMPORARY_CLEANUP_AFTER_BODY_SUCCESS",
            )
            self.assertEqual(
                getattr(
                    exc,
                    "p5d3f_temp_root",
                ),
                str(temp_root),
            )
            self.assertEqual(
                getattr(
                    exc,
                    "p5d3f_success_result",
                ),
                result,
            )

    def test_success_cleanup_removes_temp_root(self) -> None:
        root_parent = Path(
            tempfile.mkdtemp(
                prefix="p5d3f-recovery-cleanup-success-"
            )
        )
        temp_root = (
            root_parent / "temp-root"
        )
        temp_root.mkdir()
        (
            temp_root / "evidence.txt"
        ).write_text(
            "temporary\n",
            encoding="utf-8",
        )

        try:
            handoff._cleanup_temp_root_after_success(
                temp_root,
                {
                    "status":
                        "PASS_PERSISTENT_PRODUCTION_HANDOFF_READY_UNAUTHORIZED"
                },
            )
            self.assertFalse(
                temp_root.exists()
            )
        finally:
            if root_parent.exists():
                root_parent.rmdir()

    def test_source_has_no_unconditional_finally_cleanup(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "persistent_production_handoff.py"
        ).read_text(encoding="utf-8")

        marker = (
            "def execute_persistent_production_handoff"
        )
        execute_source = source[
            source.index(marker):
        ]

        self.assertNotIn(
            'raise PersistentHandoffBlockedError(\n                "BLOCKED_TEMPORARY_CLEANUP"',
            execute_source,
        )
        self.assertIn(
            "_cleanup_temp_root_after_success(",
            execute_source,
        )
        self.assertIn(
            "_annotate_body_failure(",
            execute_source,
        )

    def test_live_publication_authority_remains_absent(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "persistent_production_handoff.py"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "STAGE_A",
            "STAGE_B",
            "os.replace(",
            "threading.Thread",
            "while True",
            "schtasks",
            "CreateService",
        ):
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
