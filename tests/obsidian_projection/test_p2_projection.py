from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.builder import (
    BuilderError,
    _render_artifacts,
    build_projection_from_records,
)
from tools.obsidian_projection.classification import (
    SemanticRecord,
    git_blob_oid,
    records_digest_sha256,
)
from tools.obsidian_projection.integrity import (
    IntegrityError,
    file_digest,
    verify_integrity_manifest,
)
from tools.obsidian_projection.relations import (
    RelationError,
    extract_relations,
)
from tools.obsidian_projection.rendering import (
    RenderingError,
    artifact_record_id,
    render_artifact,
    render_frontmatter,
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
COMMIT = "1" * 40
TREE = "2" * 40


class FakeSource:
    def __init__(self, blobs: dict[str, bytes]) -> None:
        self.blobs = blobs

    def read_blob(self, oid: str) -> bytes:
        return self.blobs[oid]


def make_record(
    source_path: str,
    raw: bytes,
    *,
    semantic_role: str = "UNKNOWN",
    procedure_role: str = "NONE",
) -> SemanticRecord:
    return SemanticRecord(
        record_schema=(
            "ATDS_OBSIDIAN_SEMANTIC_RECORD_V0_1"
        ),
        record_type="ARTIFACT",
        source_repository=REPOSITORY,
        source_branch="integration/system-v1",
        source_commit=COMMIT,
        source_tree=TREE,
        source_path=source_path,
        source_blob_sha=git_blob_oid(raw),
        source_blob_size=len(raw),
        artifact_family=(
            "EVIDENCE"
            if source_path.endswith(".json")
            else "DOCUMENT"
        ),
        semantic_role=semantic_role,
        procedure_role=procedure_role,
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


def build_fixture(
    records: tuple[SemanticRecord, ...],
    blobs: dict[str, bytes],
    stage: Path,
):
    source = FakeSource(blobs)
    return build_projection_from_records(
        source=source,
        records=records,
        pilot_inventory_digest_sha256="a" * 64,
        semantic_record_digest_sha256=(
            records_digest_sha256(records)
        ),
        contract=CONTRACT,
        stage_root=stage,
    )


class RenderingTests(unittest.TestCase):
    def test_artifact_id_is_deterministic(self) -> None:
        first = artifact_record_id(
            REPOSITORY,
            "docs/example.md",
        )
        second = artifact_record_id(
            REPOSITORY,
            "docs/example.md",
        )
        self.assertEqual(first, second)
        self.assertRegex(first, r"^A-[0-9a-f]{16}$")

    def test_artifact_markdown_is_utf8_lf_no_bom_and_fixed_order(
        self,
    ) -> None:
        raw = b"# Source body never copied\n"
        record = make_record(
            "docs/example.md",
            raw,
        )
        rendered = render_artifact(
            record,
            CONTRACT,
        )

        self.assertNotIn(b"\r", rendered.content)
        self.assertFalse(
            rendered.content.startswith(
                b"\xef\xbb\xbf"
            )
        )
        self.assertTrue(
            rendered.content.endswith(b"\n")
        )

        text = rendered.content.decode("utf-8")
        frontmatter = text.split("---\n", 2)[1]
        fields = [
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
        ]
        self.assertEqual(
            fields,
            CONTRACT["artifact_record"][
                "frontmatter_field_order"
            ],
        )
        self.assertNotIn(
            "Source body never copied",
            text,
        )

    def test_source_path_is_not_output_path(self) -> None:
        raw = b"# x\n"
        record = make_record(
            "reports/program/deep/file.md",
            raw,
        )
        rendered = render_artifact(
            record,
            CONTRACT,
        )
        self.assertTrue(
            rendered.relative_path.startswith(
                "generated/artifacts/A-"
            )
        )
        self.assertNotIn(
            "reports/program",
            rendered.relative_path,
        )

    def test_absolute_or_parent_source_path_blocks(self) -> None:
        raw = b"# x\n"

        for source_path in (
            "C:/Users/test/file.md",
            "/tmp/file.md",
            "../escape.md",
            "docs/../escape.md",
            "docs\\file.md",
        ):
            with self.subTest(source_path=source_path):
                record = make_record(
                    source_path,
                    raw,
                )
                with self.assertRaises(
                    RenderingError
                ):
                    render_artifact(
                        record,
                        CONTRACT,
                    )

    def test_unknown_frontmatter_field_blocks(self) -> None:
        with self.assertRaises(RenderingError):
            render_frontmatter(
                {
                    "record_schema": "x",
                    "generated_at": "now",
                },
                ["record_schema"],
            )


class RelationTests(unittest.TestCase):
    def _records_and_source(
        self,
        source_raw: bytes,
    ):
        target_raw = b"# target\n"
        source_record = make_record(
            "reports/source.md",
            source_raw,
        )
        target_record = make_record(
            "reports/target.md",
            target_raw,
        )
        source = FakeSource(
            {
                source_record.source_blob_sha:
                    source_raw,
                target_record.source_blob_sha:
                    target_raw,
            }
        )
        return (
            source,
            (source_record, target_record),
        )

    def test_explicit_labeled_markdown_path_emits_reference(
        self,
    ) -> None:
        source, records = self._records_and_source(
            b"# Source\n\n"
            b"Evidence: \x60reports/target.md\x60\n"
        )
        relations = extract_relations(
            source,
            records,
            CONTRACT,
        )
        self.assertEqual(len(relations), 1)
        relation = relations[0]
        self.assertEqual(
            relation.relation_type,
            "REFERENCES",
        )
        self.assertEqual(
            relation.basis,
            "EXPLICIT_TEXT",
        )
        self.assertEqual(
            relation.evidence_source_path,
            "reports/source.md",
        )

    def test_structured_exact_json_path_emits_reference(
        self,
    ) -> None:
        source_raw = json.dumps(
            {
                "evidence":
                    "reports/target.md"
            }
        ).encode()
        target_raw = b"# target\n"
        source_record = make_record(
            "reports/source.json",
            source_raw,
        )
        target_record = make_record(
            "reports/target.md",
            target_raw,
        )
        source = FakeSource(
            {
                source_record.source_blob_sha:
                    source_raw,
                target_record.source_blob_sha:
                    target_raw,
            }
        )
        relations = extract_relations(
            source,
            (
                source_record,
                target_record,
            ),
            CONTRACT,
        )
        self.assertEqual(len(relations), 1)
        self.assertEqual(
            relations[0].basis,
            "EXPLICIT_STRUCTURED",
        )

    def test_wikilink_filename_similarity_and_unlabeled_text_do_not_emit(
        self,
    ) -> None:
        source, records = self._records_and_source(
            b"# Source\n\n"
            b"[[reports/target.md]]\n"
            b"reports/target.md\n"
            b"target.md\n"
        )
        relations = extract_relations(
            source,
            records,
            CONTRACT,
        )
        self.assertEqual(relations, ())

    def test_unresolved_labeled_target_is_not_guessed(
        self,
    ) -> None:
        source, records = self._records_and_source(
            b"# Source\n\n"
            b"Evidence: \x60reports/missing.md\x60\n"
        )
        relations = extract_relations(
            source,
            records,
            CONTRACT,
        )
        self.assertEqual(relations, ())

    def test_relation_id_collision_blocks(self) -> None:
        source_raw = (
            b"# Source\n\n"
            b"A: \x60reports/a.md\x60\n"
            b"B: \x60reports/b.md\x60\n"
        )
        a_raw = b"# a\n"
        b_raw = b"# b\n"

        source_record = make_record(
            "reports/source.md",
            source_raw,
        )
        a_record = make_record(
            "reports/a.md",
            a_raw,
        )
        b_record = make_record(
            "reports/b.md",
            b_raw,
        )

        source = FakeSource(
            {
                source_record.source_blob_sha:
                    source_raw,
                a_record.source_blob_sha:
                    a_raw,
                b_record.source_blob_sha:
                    b_raw,
            }
        )

        with patch(
            "tools.obsidian_projection.relations."
            "relation_record_id",
            return_value="R-" + "0" * 16,
        ):
            with self.assertRaises(RelationError):
                extract_relations(
                    source,
                    (
                        source_record,
                        a_record,
                        b_record,
                    ),
                    CONTRACT,
                )


class BuilderIntegrityTests(unittest.TestCase):
    def _fixture(self):
        source_raw = (
            b"# Source\n\n"
            b"Evidence: \x60reports/target.md\x60\n"
            b"SECRET_SOURCE_BODY\n"
        )
        target_raw = b"# Target\nTARGET_SECRET\n"

        source_record = make_record(
            "reports/source.md",
            source_raw,
        )
        target_record = make_record(
            "reports/target.md",
            target_raw,
        )

        records = (
            source_record,
            target_record,
        )
        blobs = {
            source_record.source_blob_sha:
                source_raw,
            target_record.source_blob_sha:
                target_raw,
        }
        return records, blobs

    def test_two_fresh_builds_are_byte_identical(self) -> None:
        records, blobs = self._fixture()

        with tempfile.TemporaryDirectory() as parent:
            parent_path = Path(parent)
            stage_a = parent_path / "build-a"
            stage_b = parent_path / "build-b"

            result_a = build_fixture(
                records,
                blobs,
                stage_a,
            )
            result_b = build_fixture(
                records,
                blobs,
                stage_b,
            )

            files_a = {
                path.relative_to(stage_a).as_posix():
                    path.read_bytes()
                for path in (
                    stage_a / "generated"
                ).rglob("*")
                if path.is_file()
            }
            files_b = {
                path.relative_to(stage_b).as_posix():
                    path.read_bytes()
                for path in (
                    stage_b / "generated"
                ).rglob("*")
                if path.is_file()
            }

            self.assertEqual(files_a, files_b)
            self.assertEqual(
                result_a.projection_tree_digest_sha256,
                result_b.projection_tree_digest_sha256,
            )
            self.assertEqual(
                result_a.artifact_set_digest_sha256,
                result_b.artifact_set_digest_sha256,
            )
            self.assertEqual(
                result_a.relation_set_digest_sha256,
                result_b.relation_set_digest_sha256,
            )

    def test_build_creates_only_allowed_generated_roots(self) -> None:
        records, blobs = self._fixture()

        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            result = build_fixture(
                records,
                blobs,
                stage,
            )

            self.assertEqual(
                result.artifact_record_count,
                2,
            )
            self.assertEqual(
                result.relation_record_count,
                1,
            )
            self.assertFalse(
                (stage / "views").exists()
            )
            self.assertFalse(
                (stage / ".obsidian").exists()
            )

            all_bytes = b"".join(
                path.read_bytes()
                for path in (
                    stage / "generated"
                ).rglob("*")
                if path.is_file()
            )
            self.assertNotIn(
                str(stage).encode(),
                all_bytes,
            )
            self.assertNotIn(
                b"SECRET_SOURCE_BODY",
                all_bytes,
            )
            self.assertNotIn(
                b"TARGET_SECRET",
                all_bytes,
            )
            self.assertNotIn(
                b"generated_at",
                all_bytes,
            )

    def test_manual_edit_and_missing_file_are_detected(self) -> None:
        records, blobs = self._fixture()

        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            build_fixture(
                records,
                blobs,
                stage,
            )

            artifact = next(
                (
                    stage
                    / "generated"
                    / "artifacts"
                ).glob("*.md")
            )

            artifact.write_bytes(
                artifact.read_bytes()
                + b"mutation\n"
            )

            statuses = verify_integrity_manifest(
                stage
            )
            relative = artifact.relative_to(
                stage
            ).as_posix()
            self.assertEqual(
                statuses[relative],
                "MODIFIED",
            )

            artifact.unlink()
            statuses = verify_integrity_manifest(
                stage
            )
            self.assertEqual(
                statuses[relative],
                "MISSING",
            )

    def test_preexisting_stage_blocks(self) -> None:
        records, blobs = self._fixture()

        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            stage.mkdir()

            with self.assertRaises(
                IntegrityError
            ):
                build_fixture(
                    records,
                    blobs,
                    stage,
                )

    def test_hard_link_anomaly_blocks(self) -> None:
        records, blobs = self._fixture()

        with tempfile.TemporaryDirectory() as parent:
            stage = Path(parent) / "build"
            build_fixture(
                records,
                blobs,
                stage,
            )

            artifact = next(
                (
                    stage
                    / "generated"
                    / "artifacts"
                ).glob("*.md")
            )
            alias = Path(parent) / "hardlink-alias"

            try:
                os.link(artifact, alias)
            except OSError as exc:
                self.fail(
                    "hard-link capability unavailable "
                    f"during breaker: {exc}"
                )

            with self.assertRaises(
                IntegrityError
            ):
                file_digest(
                    stage,
                    artifact,
                )

    def test_artifact_id_collision_blocks(self) -> None:
        raw_a = b"# a\n"
        raw_b = b"# b\n"
        records = (
            make_record("a.md", raw_a),
            make_record("b.md", raw_b),
        )

        with patch(
            "tools.obsidian_projection.rendering."
            "artifact_record_id",
            return_value="A-" + "0" * 16,
        ):
            with self.assertRaises(
                BuilderError
            ):
                _render_artifacts(
                    records,
                    CONTRACT,
                )


if __name__ == "__main__":
    unittest.main()
