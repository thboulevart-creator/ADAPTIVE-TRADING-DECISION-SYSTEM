from __future__ import annotations

import json
import unittest

from tools.obsidian_projection.candidate_generation_staging import (
    CandidateGenerationInfrastructureError,
)
from tools.obsidian_projection.p5d3c2_verify import (
    REPORT_SCHEMA,
    _REQUIRED_MUTATIONS,
    run_sandbox_qualification,
)


class P5D3C2SandboxQualificationTests(
    unittest.TestCase
):
    def run_report(self) -> dict[str, object]:
        try:
            return run_sandbox_qualification()
        except CandidateGenerationInfrastructureError as exc:
            self.skipTest(
                f"sandbox filesystem capability unavailable: {exc}"
            )

    def test_sandbox_qualification_passes(self) -> None:
        report = self.run_report()

        self.assertEqual(
            report["schema"],
            REPORT_SCHEMA,
        )
        self.assertEqual(
            report["status"],
            "PASS_SANDBOX_SEALED_UNPROMOTED",
        )
        self.assertEqual(
            report["package_verification_status"],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            report["control_verify_repeat_equal"]
        )
        self.assertTrue(
            report["control_content_digest_unchanged"]
        )
        self.assertFalse(
            report["real_vault_modified"]
        )
        self.assertFalse(
            report["current_pointer_created"]
        )
        self.assertFalse(
            report["production_promotion_authorized"]
        )
        self.assertFalse(report["sandbox_retained"])

    def test_all_required_mutations_are_rejected(
        self,
    ) -> None:
        report = self.run_report()

        self.assertEqual(
            tuple(
                report[
                    "required_mutation_breakers_passed"
                ]
            ),
            _REQUIRED_MUTATIONS,
        )
        self.assertEqual(
            report[
                "required_mutation_breaker_count"
            ],
            len(_REQUIRED_MUTATIONS),
        )

    def test_reparse_probe_is_explicit(self) -> None:
        report = self.run_report()
        self.assertIn(
            report["reparse_probe_status"],
            {
                "REJECTED_AS_INVALID",
                "CAPABILITY_UNAVAILABLE",
            },
        )

    def test_report_contains_no_host_path_fields(
        self,
    ) -> None:
        report = self.run_report()
        serialized = json.dumps(
            report,
            sort_keys=True,
        )
        for forbidden in (
            "sandbox_path",
            "package_root",
            "absolute_path",
            "hostname",
            "host_id",
            "pid",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(
                    forbidden,
                    serialized,
                )

    def test_identity_is_stable_across_sandboxes(
        self,
    ) -> None:
        first = self.run_report()
        second = self.run_report()

        self.assertEqual(
            first["generation_id"],
            second["generation_id"],
        )
        self.assertEqual(
            first[
                "candidate_generation_digest_sha256"
            ],
            second[
                "candidate_generation_digest_sha256"
            ],
        )
        self.assertEqual(
            first[
                "payload_file_map_digest_sha256"
            ],
            second[
                "payload_file_map_digest_sha256"
            ],
        )


if __name__ == "__main__":
    unittest.main()
