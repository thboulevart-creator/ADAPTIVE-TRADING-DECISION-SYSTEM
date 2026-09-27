from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.classification import (
    git_blob_oid,
)
from tools.obsidian_projection.current_head_projection import (
    CurrentHeadProjectionInvalidError,
    PROJECTION_CONTRACT_BLOB,
    build_current_head_projection,
)
from tools.obsidian_projection.current_head_semantic_bridge import (
    build_current_head_semantic_bridge,
)
from tools.obsidian_projection.dynamic_inventory import (
    DynamicInventory,
    DynamicInventoryEntry,
)
from tools.obsidian_projection.integrity import (
    all_generated_files,
)


REPOSITORY = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)
HEAD = "1" * 40
TREE = "2" * 40


class FakeSource:
    def __init__(self, blobs: dict[str, bytes]) -> None:
        self.blobs = dict(blobs)
        self.reads: list[str] = []

    def read_blob(self, oid: str) -> bytes:
        self.reads.append(oid)
        return self.blobs[oid]


def make_bridge() -> tuple[FakeSource, object]:
    raw_by_path = {
        "assets/blob.bin": b"\x00\x01\x02\x03",
        "data/refs.json":
            b'{"reference":"docs/source.md"}\n',
        "docs/source.md":
            b"# Source\n\nBinary target: "
            b"\x60assets/blob.bin\x60\n",
        "src/code.py": b"VALUE = 1\n",
    }

    entries = []
    blobs: dict[str, bytes] = {}
    for path in sorted(
        raw_by_path,
        key=lambda item: item.encode("utf-8"),
    ):
        raw = raw_by_path[path]
        oid = git_blob_oid(raw)
        blobs[oid] = raw
        entries.append(
            DynamicInventoryEntry(
                source_path=path,
                source_blob_sha=oid,
                source_blob_size=len(raw),
                git_mode="100644",
                selection_zone="SYNTHETIC",
                content_mode=(
                    "METADATA_ONLY"
                    if path.endswith(".bin")
                    else "FULL_TEXT"
                ),
            )
        )

    inventory = DynamicInventory(
        source_repository=REPOSITORY,
        source_branch="integration/system-v1",
        source_commit=HEAD,
        source_tree=TREE,
        entries=tuple(entries),
    )
    return (
        FakeSource(blobs),
        build_current_head_semantic_bridge(
            inventory
        ),
    )


def generated_bytes(root: Path) -> dict[str, bytes]:
    return {
        entry.relative_path:
            root.joinpath(
                *entry.relative_path.split("/")
            ).read_bytes()
        for entry in all_generated_files(root)
    }


class CurrentHeadProjectionBuilderTests(
    unittest.TestCase
):
    def test_build_counts_and_identity(self) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-test-"
        ) as temp:
            stage = Path(temp) / "build"
            result = build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage,
            )

            self.assertEqual(
                result.source_record_count,
                4,
            )
            self.assertEqual(
                result.full_text_count,
                3,
            )
            self.assertEqual(
                result.metadata_only_count,
                1,
            )
            self.assertEqual(
                result.artifact_record_count,
                4,
            )
            self.assertEqual(
                result.relation_record_count,
                2,
            )
            self.assertEqual(
                result.relation_source_body_read_count,
                2,
            )
            self.assertEqual(
                result.metadata_only_body_read_count,
                0,
            )
            self.assertEqual(
                result.projection_contract_version,
                PROJECTION_CONTRACT_BLOB,
            )
            self.assertEqual(
                result.generated_file_count,
                8,
            )

    def test_builder_reads_only_relation_eligible_blobs(
        self,
    ) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-read-"
        ) as temp:
            stage = Path(temp) / "build"
            build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage,
            )

        eligible = {
            entry.source_blob_sha
            for entry in bridge.entries
            if entry.source_path in {
                "data/refs.json",
                "docs/source.md",
            }
        }
        self.assertEqual(
            set(source.reads),
            eligible,
        )
        self.assertEqual(
            len(source.reads),
            2,
        )

    def test_build_manifest_has_current_head_identity_only(
        self,
    ) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-manifest-"
        ) as temp:
            stage = Path(temp) / "build"
            result = build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage,
            )
            manifest = json.loads(
                (
                    stage
                    / "generated"
                    / "manifests"
                    / "build-manifest.json"
                ).read_text(encoding="utf-8")
            )

        self.assertEqual(
            manifest[
                "dynamic_inventory_digest_sha256"
            ],
            bridge.dynamic_inventory_digest_sha256,
        )
        self.assertEqual(
            manifest[
                "semantic_bridge_digest_sha256"
            ],
            bridge.bridge_entry_digest_sha256,
        )
        self.assertEqual(
            manifest[
                "semantic_record_digest_sha256"
            ],
            bridge.semantic_record_digest_sha256,
        )
        self.assertEqual(
            manifest[
                "projection_contract_version"
            ],
            PROJECTION_CONTRACT_BLOB,
        )
        self.assertEqual(
            manifest[
                "metadata_only_body_read_count"
            ],
            0,
        )
        self.assertNotIn(
            "pilot_inventory_digest_sha256",
            manifest,
        )
        self.assertNotIn(
            "pilot_source_count",
            manifest,
        )
        self.assertEqual(
            result.projection_tree_digest_sha256,
            result.projection_tree_digest_sha256,
        )

    def test_two_builds_are_byte_identical(self) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-ab-"
        ) as temp:
            root = Path(temp)
            stage_a = root / "a"
            stage_b = root / "b"

            result_a = build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage_a,
            )
            result_b = build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage_b,
            )

            self.assertEqual(
                generated_bytes(stage_a),
                generated_bytes(stage_b),
            )
            self.assertEqual(
                result_a.projection_tree_digest_sha256,
                result_b.projection_tree_digest_sha256,
            )
            self.assertEqual(
                result_a.body_read_audit_digest_sha256,
                result_b.body_read_audit_digest_sha256,
            )

    def test_artifact_notes_do_not_copy_source_bodies(
        self,
    ) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-body-"
        ) as temp:
            stage = Path(temp) / "build"
            build_current_head_projection(
                source=source,
                bridge=bridge,
                stage_root=stage,
            )

            artifact_bytes = b"\n".join(
                path.read_bytes()
                for path in (
                    stage
                    / "generated"
                    / "artifacts"
                ).glob("*.md")
            )

        self.assertNotIn(
            b'{"reference":"docs/source.md"}',
            artifact_bytes,
        )
        self.assertNotIn(
            b"VALUE = 1",
            artifact_bytes,
        )

    def test_preexisting_stage_root_is_rejected(
        self,
    ) -> None:
        source, bridge = make_bridge()

        with tempfile.TemporaryDirectory(
            prefix="atds-p5d3d-build-preexisting-"
        ) as temp:
            stage = Path(temp) / "build"
            stage.mkdir()

            with self.assertRaises(
                CurrentHeadProjectionInvalidError
            ):
                build_current_head_projection(
                    source=source,
                    bridge=bridge,
                    stage_root=stage,
                )


if __name__ == "__main__":
    unittest.main()
