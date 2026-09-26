from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.promotion_experiment import (
    EntryPointMissingError,
    MixedGenerationError,
    PromotionExperimentError,
    _write_pointer,
    assert_sandbox_boundary,
    build_generation,
    run_negative_control,
    run_pointer_swap,
    validate_generation_dir,
    validate_pointer_entry,
)


class PromotionExperimentTests(unittest.TestCase):
    def test_generation_build_and_validation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "GEN_A"
            manifest = build_generation(
                root,
                "GEN_A",
                files_per_generation=8,
                nested_directories=2,
            )

            result = validate_generation_dir(
                root
            )

            self.assertEqual(
                result["generation_id"],
                "GEN_A",
            )
            self.assertEqual(
                result["file_count"],
                8,
            )
            self.assertEqual(
                result[
                    "tree_digest_sha256"
                ],
                manifest[
                    "tree_digest_sha256"
                ],
            )

    def test_generation_ids_produce_different_digests(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            a = build_generation(
                Path(td) / "A",
                "GEN_A",
                files_per_generation=8,
                nested_directories=2,
            )
            b = build_generation(
                Path(td) / "B",
                "GEN_B",
                files_per_generation=8,
                nested_directories=2,
            )
            self.assertNotEqual(
                a["tree_digest_sha256"],
                b["tree_digest_sha256"],
            )

    def test_partial_per_file_replace_is_detected_as_mixed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a = root / "A"
            b = root / "B"
            live = root / "live"

            build_generation(
                a,
                "GEN_A",
                files_per_generation=8,
                nested_directories=2,
            )
            build_generation(
                b,
                "GEN_B",
                files_per_generation=8,
                nested_directories=2,
            )

            import shutil

            shutil.copytree(a, live)

            b_manifest = json.loads(
                (b / "MANIFEST.json").read_text(
                    encoding="utf-8"
                )
            )
            first = Path(
                b_manifest["files"][0]["path"]
            )
            shutil.copyfile(
                b / first,
                live / first,
            )

            with self.assertRaises(
                MixedGenerationError
            ):
                validate_generation_dir(
                    live
                )

    def test_pointer_switch_resolves_one_complete_generation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / "candidate"
            generations = (
                candidate / "generations"
            )
            generations.mkdir(parents=True)

            build_generation(
                generations / "GEN_A",
                "GEN_A",
                files_per_generation=8,
                nested_directories=2,
            )
            build_generation(
                generations / "GEN_B",
                "GEN_B",
                files_per_generation=8,
                nested_directories=2,
            )

            _write_pointer(
                candidate,
                "GEN_A",
                "generations/GEN_A",
            )
            self.assertEqual(
                validate_pointer_entry(
                    candidate
                )["generation_id"],
                "GEN_A",
            )

            _write_pointer(
                candidate,
                "GEN_B",
                "generations/GEN_B",
            )
            self.assertEqual(
                validate_pointer_entry(
                    candidate
                )["generation_id"],
                "GEN_B",
            )

    def test_pointer_rejects_staging_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            candidate = Path(td) / "candidate"
            candidate.mkdir()

            (candidate / "CURRENT.json").write_text(
                json.dumps(
                    {
                        "generation_id":
                            "GEN_A",
                        "generation_path":
                            "stage/GEN_A",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(
                PromotionExperimentError
            ):
                validate_pointer_entry(
                    candidate
                )

    def test_missing_pointer_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(
                EntryPointMissingError
            ):
                validate_pointer_entry(
                    Path(td)
                )

    def test_negative_control_probe_detects_non_atomicity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fixtures = {
                "GEN_A": root / "fixtures" / "GEN_A",
                "GEN_B": root / "fixtures" / "GEN_B",
            }
            build_generation(
                fixtures["GEN_A"],
                "GEN_A",
                files_per_generation=24,
                nested_directories=4,
            )
            build_generation(
                fixtures["GEN_B"],
                "GEN_B",
                files_per_generation=24,
                nested_directories=4,
            )

            with (
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "NEGATIVE_CONTROL_CYCLES",
                    4,
                ),
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "NEGATIVE_CONTROL_MIN_SAMPLES",
                    40,
                ),
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "READER_INTERVAL_SECONDS",
                    0.0005,
                ),
            ):
                metrics = run_negative_control(
                    root / "negative",
                    fixtures,
                )

            self.assertEqual(
                metrics.result,
                "PASS",
            )
            self.assertFalse(
                metrics.qualification_allowed
            )
            anomalies = (
                metrics.mixed_generation_count
                + metrics.missing_entrypoint_count
                + metrics.partial_generation_count
                + metrics.parse_error_count
            )
            self.assertGreater(
                anomalies,
                0,
            )

    def test_pointer_candidate_has_zero_anomalies(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fixtures = {
                "GEN_A": root / "fixtures" / "GEN_A",
                "GEN_B": root / "fixtures" / "GEN_B",
            }
            build_generation(
                fixtures["GEN_A"],
                "GEN_A",
                files_per_generation=12,
                nested_directories=3,
            )
            build_generation(
                fixtures["GEN_B"],
                "GEN_B",
                files_per_generation=12,
                nested_directories=3,
            )

            with (
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "QUALIFIABLE_CYCLES",
                    20,
                ),
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "MIN_READER_SAMPLES",
                    100,
                ),
                patch(
                    "tools.obsidian_projection.promotion_experiment."
                    "READER_INTERVAL_SECONDS",
                    0.0005,
                ),
            ):
                metrics = run_pointer_swap(
                    root / "pointer",
                    fixtures,
                )

            self.assertEqual(
                metrics.result,
                "PASS",
            )
            self.assertTrue(
                metrics.qualifies_primitive
            )
            self.assertEqual(
                metrics.mixed_generation_count,
                0,
            )
            self.assertEqual(
                metrics.missing_entrypoint_count,
                0,
            )
            self.assertEqual(
                metrics.partial_generation_count,
                0,
            )
            self.assertEqual(
                metrics.parse_error_count,
                0,
            )

    @unittest.skipUnless(
        os.name == "nt",
        "Windows boundary test",
    )
    def test_exact_sandbox_boundary_accepts_expected_path(
        self,
    ) -> None:
        from tools.obsidian_projection.promotion_experiment import (
            LIVE_VAULT,
            SANDBOX,
        )

        assert_sandbox_boundary(
            SANDBOX,
            LIVE_VAULT,
        )

    def test_overlap_boundary_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            live = Path(td) / "vault"
            child = live / "sandbox"
            with self.assertRaises(
                PromotionExperimentError
            ):
                assert_sandbox_boundary(
                    child,
                    live,
                )


if __name__ == "__main__":
    unittest.main()
