from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.builder import (
    BuilderError,
    _render_artifacts,
)
from tools.obsidian_projection.classification import (
    SemanticRecord,
    git_blob_oid,
)
from tools.obsidian_projection.integrity import (
    FileDigest,
    IntegrityError,
    create_stage_directories,
    exclusive_write,
    make_integrity_manifest,
)
from tools.obsidian_projection.relations import (
    RelationRecord,
)
from tools.obsidian_projection.rendering import (
    RenderedFile,
    RenderingError,
    render_relation,
)


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = json.loads(
    (
        ROOT
        / "tools"
        / "obsidian_projection"
        / "deterministic_projection_contract_v0_1.json"
    ).read_text(encoding="utf-8")
)

REPOSITORY = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)


def make_record(
    source_path: str,
    raw: bytes,
) -> SemanticRecord:
    return SemanticRecord(
        record_schema=(
            "ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1"
        ),
        record_type="ARTIFACT",
        source_repository=REPOSITORY,
        source_branch="integration/system-v1",
        source_commit="1" * 40,
        source_tree="2" * 40,
        source_path=source_path,
        source_blob_sha=git_blob_oid(raw),
        source_blob_size=len(raw),
        artifact_family="DOCUMENT",
        semantic_role="UNKNOWN",
        procedure_role="NONE",
        authority_role="CANONICAL",
        qualification_status="UNKNOWN",
        qualification_scope=None,
        scientific_status="UNKNOWN",
        epistemic_role="UNKNOWN",
        temporal_role="UNKNOWN",
        persistence_state="TRACKED_IN_GIT_TREE",
        limitations=(),
        non_claims=(),
    )


class FakeSource:
    def __init__(self, record: SemanticRecord, raw: bytes):
        self.record = record
        self.raw = raw

    def read_blob(self, oid: str) -> bytes:
        if oid != self.record.source_blob_sha:
            raise KeyError(oid)
        return self.raw


class P2AdversarialTests(unittest.TestCase):
    def test_writer_rejects_crlf_bom_and_missing_final_lf(self) -> None:
        cases = (
            b"x\r\n",
            b"\xef\xbb\xbfx\n",
            b"x",
        )

        for payload in cases:
            with self.subTest(payload=payload):
                with tempfile.TemporaryDirectory() as parent:
                    stage = Path(parent) / "build"
                    create_stage_directories(stage)

                    with self.assertRaises(IntegrityError):
                        exclusive_write(
                            stage,
                            RenderedFile(
                                relative_path=(
                                    "generated/artifacts/"
                                    "A-0000000000000000.md"
                                ),
                                content=payload,
                            ),
                        )

    def test_writer_rejects_in_place_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            create_stage_directories(stage)

            rendered = RenderedFile(
                relative_path=(
                    "generated/artifacts/"
                    "A-0000000000000000.md"
                ),
                content=b"x\n",
            )

            exclusive_write(stage, rendered)

            with self.assertRaises(IntegrityError):
                exclusive_write(stage, rendered)

    def test_writer_rejects_views_obsidian_and_outside_generated(self) -> None:
        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            create_stage_directories(stage)

            for relative in (
                "views/x.md",
                ".obsidian/x.json",
                "outside.md",
            ):
                with self.subTest(relative=relative):
                    with self.assertRaises(
                        IntegrityError
                    ):
                        exclusive_write(
                            stage,
                            RenderedFile(
                                relative_path=relative,
                                content=b"x\n",
                            ),
                        )

    def test_reparse_alias_guard_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            create_stage_directories(stage)

            with patch(
                "tools.obsidian_projection.integrity."
                "_is_reparse_or_link",
                return_value=True,
            ):
                with self.assertRaises(
                    IntegrityError
                ):
                    exclusive_write(
                        stage,
                        RenderedFile(
                            relative_path=(
                                "generated/artifacts/"
                                "A-0000000000000000.md"
                            ),
                            content=b"x\n",
                        ),
                    )

    def test_integrity_manifest_self_inclusion_blocks(self) -> None:
        self_entry = FileDigest(
            relative_path=(
                "generated/manifests/"
                "integrity-manifest.json"
            ),
            size_bytes=1,
            sha256="0" * 64,
        )

        with self.assertRaises(IntegrityError):
            make_integrity_manifest(
                (self_entry,)
            )

    def test_inferred_relation_is_rejected_at_renderer_boundary(self) -> None:
        relation = RelationRecord(
            projection_relation_id=(
                "R-" + "0" * 16
            ),
            source_record_id=(
                "A-" + "1" * 16
            ),
            relation_type="REFERENCES",
            target_record_id=(
                "A-" + "2" * 16
            ),
            basis="INFERRED",
            evidence_source_path=(
                "reports/source.md"
            ),
            evidence_source_blob_sha=(
                "3" * 40
            ),
            source_commit="4" * 40,
        )

        with self.assertRaises(RenderingError):
            render_relation(
                relation,
                CONTRACT,
            )

    def test_relation_missing_provenance_blocks(self) -> None:
        for evidence_path, blob_sha in (
            ("", "3" * 40),
            ("reports/source.md", ""),
            ("reports/source.md", "x" * 40),
        ):
            with self.subTest(
                evidence_path=evidence_path,
                blob_sha=blob_sha,
            ):
                relation = RelationRecord(
                    projection_relation_id=(
                        "R-" + "0" * 16
                    ),
                    source_record_id=(
                        "A-" + "1" * 16
                    ),
                    relation_type="REFERENCES",
                    target_record_id=(
                        "A-" + "2" * 16
                    ),
                    basis="EXPLICIT_TEXT",
                    evidence_source_path=evidence_path,
                    evidence_source_blob_sha=blob_sha,
                    source_commit="4" * 40,
                )

                with self.assertRaises(
                    RenderingError
                ):
                    render_relation(
                        relation,
                        CONTRACT,
                    )

    def test_source_text_copy_mutant_blocks(self) -> None:
        raw = (
            b"# source\n"
            b"FULL_CANONICAL_SOURCE_BYTES\n"
        )
        record = make_record(
            "reports/source.md",
            raw,
        )
        source = FakeSource(
            record,
            raw,
        )

        mutant = RenderedFile(
            relative_path=(
                "generated/artifacts/"
                "A-0000000000000000.md"
            ),
            content=(
                b"---\n"
                b"record_schema: "
                b"\"ATDS_OBSIDIAN_ARTIFACT_V0_1\"\n"
                b"---\n"
                + raw
            ),
        )

        with patch(
            "tools.obsidian_projection.builder."
            "render_artifact",
            return_value=mutant,
        ):
            with self.assertRaises(BuilderError):
                _render_artifacts(
                    (record,),
                    CONTRACT,
                    source=source,
                )


if __name__ == "__main__":
    unittest.main()
