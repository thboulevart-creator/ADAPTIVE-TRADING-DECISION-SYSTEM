from __future__ import annotations

import unittest
from pathlib import Path

from tools.obsidian_projection import candidate_generation_staging


class P5D3FPersistentDestinationVerifierAmendmentRedV01Tests(
    unittest.TestCase
):
    def test_red_persistent_verifier_surface_exists(self) -> None:
        self.assertTrue(
            hasattr(
                candidate_generation_staging,
                "verify_persistent_candidate_generation",
            ),
            "RED_EXPECTED: persistent verifier surface absent",
        )

    def test_red_p5d3f_imports_persistent_verifier(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_promotion_handoff.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "verify_persistent_candidate_generation",
            source,
            "RED_EXPECTED: P5-D3F has no persistent verifier binding",
        )

    def test_red_destination_uses_persistent_verifier(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_promotion_handoff.py"
        ).read_text(encoding="utf-8")

        destination_marker = (
            "destination_descriptor ="
        )
        start = source.index(
            destination_marker
        )
        window = source[
            start:start + 1200
        ]

        self.assertIn(
            "verify_persistent_candidate_generation(",
            window,
            "RED_EXPECTED: destination still uses temp-only verifier",
        )

    def test_red_persistent_verifier_requires_explicit_staging_root(
        self,
    ) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "authorized_staging_root",
            source,
            "RED_EXPECTED: no explicit persistent staging authority surface",
        )

    def test_historical_temp_verifier_remains_temp_only(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "candidate_generation_staging.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "def verify_candidate_generation(",
            source,
        )
        self.assertIn(
            "package root must be below OS temp root",
            source,
        )

    def test_no_later_authority_is_introduced_in_red_phase(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "tools"
            / "obsidian_projection"
            / "p5d3f_promotion_handoff.py"
        ).read_text(encoding="utf-8")

        for forbidden in (
            "execute_finite_live_publication",
            "PROMOTION_CONFIRMED",
            "consume_stage_a_plan_approval",
            "EXECUTE_ONE_FINITE_REAL_LIVE_PUBLICATION_TRANSACTION",
            "threading.Thread",
            "schtasks",
            "CreateService",
        ):
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
