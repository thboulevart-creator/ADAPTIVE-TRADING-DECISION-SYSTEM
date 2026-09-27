from __future__ import annotations

import unittest

from tools.obsidian_projection.p5d3d_verify import (
    REPORT_SCHEMA,
    run_synthetic_qualification,
)


class P5D3DSyntheticQualificationTests(
    unittest.TestCase
):
    def test_full_synthetic_finite_evaluation_passes(
        self,
    ) -> None:
        report = run_synthetic_qualification()

        self.assertEqual(
            report["schema"],
            REPORT_SCHEMA,
        )
        self.assertEqual(
            report["status"],
            "PASS_SYNTHETIC_FINITE_EVALUATION",
        )
        self.assertEqual(
            report["outcome"],
            "QUALIFIED",
        )
        self.assertEqual(
            report[
                "candidate_generation_verification_status"
            ],
            "PASS_SEALED_UNPROMOTED",
        )
        self.assertTrue(
            report["projection_a_equals_b"]
        )
        self.assertEqual(
            report["source_record_count"],
            4,
        )
        self.assertEqual(
            report["full_text_count"],
            3,
        )
        self.assertEqual(
            report["metadata_only_count"],
            1,
        )
        self.assertEqual(
            report["artifact_record_count"],
            4,
        )
        self.assertEqual(
            report["relation_record_count"],
            2,
        )
        self.assertEqual(
            report[
                "relation_source_body_read_count"
            ],
            2,
        )
        self.assertEqual(
            report[
                "metadata_only_body_read_count"
            ],
            0,
        )
        self.assertTrue(
            report["p5d2_result_event_emitted"]
        )
        self.assertTrue(
            report["live_projection_head_unchanged"]
        )
        self.assertFalse(
            report["real_vault_modified"]
        )
        self.assertFalse(
            report["current_pointer_created"]
        )
        self.assertFalse(
            report[
                "production_promotion_authorized"
            ]
        )
        self.assertFalse(
            report["network_fetch_performed"]
        )
        self.assertFalse(
            report["real_candidate_evaluated"]
        )
        self.assertFalse(
            report[
                "synthetic_repository_retained"
            ]
        )
        self.assertFalse(
            report[
                "synthetic_workspace_retained"
            ]
        )


if __name__ == "__main__":
    unittest.main()
