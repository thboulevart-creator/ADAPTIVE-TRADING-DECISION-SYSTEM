from __future__ import annotations

import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from tools.obsidian_projection.current_head_breakers import (
    run_current_head_projection_breakers,
)
from tools.obsidian_projection.current_head_projection import (
    build_current_head_projection,
)
from tools.obsidian_projection.current_head_relations import (
    BodyReadAuditRow,
)
from tests.obsidian_projection.test_current_head_projection import (
    make_bridge,
)


class CurrentHeadBreakerRunnerTests(
    unittest.TestCase
):
    def build_pair(self) -> tuple[
        object,
        object,
        object,
        tempfile.TemporaryDirectory,
    ]:
        source, bridge = make_bridge()
        temp = tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-breakers-"
        )
        root = Path(temp.name)

        build_a = build_current_head_projection(
            source=source,
            bridge=bridge,
            stage_root=root / "a",
        )
        build_b = build_current_head_projection(
            source=source,
            bridge=bridge,
            stage_root=root / "b",
        )
        return bridge, build_a, build_b, temp

    def test_clean_pair_passes_all_twelve(
        self,
    ) -> None:
        bridge, build_a, build_b, temp = (
            self.build_pair()
        )
        try:
            result = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=build_a,
                    build_b=build_b,
                )
            )
        finally:
            temp.cleanup()

        self.assertTrue(result.all_pass)
        self.assertEqual(
            result.status,
            "PASS",
        )
        self.assertEqual(
            len(result.breaker_statuses),
            12,
        )
        self.assertEqual(
            [item[0] for item in result.breaker_statuses],
            [
                f"CHP-B{index:02d}"
                for index in range(1, 13)
            ],
        )
        self.assertTrue(
            all(
                status == "PASS"
                for _, status
                in result.breaker_statuses
            )
        )

    def test_generated_byte_mutation_fails_b10(
        self,
    ) -> None:
        bridge, build_a, build_b, temp = (
            self.build_pair()
        )
        try:
            target = (
                Path(build_b.stage_root)
                / "generated"
                / "artifacts"
            )
            artifact = next(
                target.glob("*.md")
            )
            artifact.write_bytes(
                artifact.read_bytes()
                + b"mutated\n"
            )

            result = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=build_a,
                    build_b=build_b,
                )
            )
        finally:
            temp.cleanup()

        statuses = dict(
            result.breaker_statuses
        )
        self.assertEqual(
            result.status,
            "FAIL",
        )
        self.assertEqual(
            statuses["CHP-B10"],
            "FAIL",
        )

    def test_metadata_only_audit_row_fails_b02(
        self,
    ) -> None:
        bridge, build_a, build_b, temp = (
            self.build_pair()
        )
        metadata = next(
            entry
            for entry in bridge.entries
            if entry.content_mode == "METADATA_ONLY"
        )
        mutant_row = BodyReadAuditRow(
            source_path=metadata.source_path,
            source_blob_sha=metadata.source_blob_sha,
            content_mode="METADATA_ONLY",
            purpose="RELATION_EXPLICIT_PATH_EXTRACTION",
        )
        mutant_a = replace(
            build_a,
            metadata_only_body_read_count=1,
            body_read_audit_rows=(
                *build_a.body_read_audit_rows,
                mutant_row,
            ),
        )

        try:
            result = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=mutant_a,
                    build_b=build_b,
                )
            )
        finally:
            temp.cleanup()

        statuses = dict(
            result.breaker_statuses
        )
        self.assertEqual(
            statuses["CHP-B02"],
            "FAIL",
        )
        self.assertEqual(
            result.status,
            "FAIL",
        )

    def test_shared_stage_root_fails_b12(
        self,
    ) -> None:
        bridge, build_a, _build_b, temp = (
            self.build_pair()
        )
        try:
            result = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=build_a,
                    build_b=build_a,
                )
            )
        finally:
            temp.cleanup()

        statuses = dict(
            result.breaker_statuses
        )
        self.assertEqual(
            statuses["CHP-B12"],
            "FAIL",
        )

    def test_manifest_and_result_digests_are_stable(
        self,
    ) -> None:
        bridge, build_a, build_b, temp = (
            self.build_pair()
        )
        try:
            first = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=build_a,
                    build_b=build_b,
                )
            )
            second = (
                run_current_head_projection_breakers(
                    bridge=bridge,
                    build_a=build_a,
                    build_b=build_b,
                )
            )
        finally:
            temp.cleanup()

        self.assertEqual(
            first.manifest_digest_sha256,
            second.manifest_digest_sha256,
        )
        self.assertEqual(
            first.result_digest_sha256,
            second.result_digest_sha256,
        )


if __name__ == "__main__":
    unittest.main()
