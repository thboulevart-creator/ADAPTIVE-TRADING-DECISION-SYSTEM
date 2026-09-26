from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.builder import (
    build_projection_from_records,
)
from tools.obsidian_projection.classification import (
    SemanticRecord,
    git_blob_oid,
    records_digest_sha256,
)
from tools.obsidian_projection.materialize import (
    FilesystemIdentity,
    MaterializationError,
    _assert_exact_projection_layout,
    _copy_qualified_generated_tree,
    _create_incoming_structure,
    _digest_map,
    _quarantine_after_failed_post_verify,
    validate_fresh_p2_report,
    verify_materialized_projection,
    verify_p2_core_blobs,
)


ROOT = Path(__file__).resolve().parents[2]
PACKAGE_DIR = (
    ROOT / "tools" / "obsidian_projection"
)
PROJECTION_CONTRACT = json.loads(
    (
        PACKAGE_DIR
        / "deterministic_projection_contract_v0_1.json"
    ).read_text(encoding="utf-8")
)
MATERIALIZATION_CONTRACT = json.loads(
    (
        PACKAGE_DIR
        / "materialization_contract_v0_1.json"
    ).read_text(encoding="utf-8")
)

REPOSITORY = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)
COMMIT = "7bd8c1312430dfc3def5523eb65397a5d6a5ae05"
TREE = "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b"
FAKE_IDENTITY = FilesystemIdentity(
    volume_serial=1234,
    file_identity=5678,
    filesystem="NTFS",
)


class FakeSource:
    def __init__(
        self,
        blobs: dict[str, bytes],
    ) -> None:
        self.blobs = blobs

    def read_blob(self, oid: str) -> bytes:
        return self.blobs[oid]


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


def build_p2_pair(
    parent: Path,
) -> tuple[
    dict[str, object],
    Path,
    Path,
]:
    records_list: list[SemanticRecord] = []
    blobs: dict[str, bytes] = {}

    source_raw = (
        b"# Source\n\n"
        b"Evidence: \x60reports/item-001.md\x60\n"
    )
    source_record = make_record(
        "reports/item-000.md",
        source_raw,
    )
    records_list.append(source_record)
    blobs[
        source_record.source_blob_sha
    ] = source_raw

    for index in range(1, 74):
        path = f"reports/item-{index:03d}.md"
        raw = (
            f"# Item {index:03d}\n"
        ).encode("utf-8")
        record = make_record(
            path,
            raw,
        )
        records_list.append(record)
        blobs[record.source_blob_sha] = raw

    records = tuple(records_list)
    if len(records) != 74:
        raise AssertionError(
            "synthetic P2 fixture must contain 74 records"
        )

    source = FakeSource(blobs)

    semantic_digest = records_digest_sha256(
        records
    )

    build_a = parent / "build-a"
    build_b = parent / "build-b"

    result_a = build_projection_from_records(
        source=source,
        records=records,
        pilot_inventory_digest_sha256="a" * 64,
        semantic_record_digest_sha256=semantic_digest,
        contract=PROJECTION_CONTRACT,
        stage_root=build_a,
    )
    result_b = build_projection_from_records(
        source=source,
        records=records,
        pilot_inventory_digest_sha256="a" * 64,
        semantic_record_digest_sha256=semantic_digest,
        contract=PROJECTION_CONTRACT,
        stage_root=build_b,
    )

    if _digest_map(build_a) != _digest_map(build_b):
        raise AssertionError(
            "synthetic P2 pair unexpectedly differs"
        )

    relation_count = (
        result_a.relation_record_count
    )
    clean_count = (
        result_a.artifact_record_count
        + relation_count
    )

    report = {
        "status": "PASS",
        "repository": REPOSITORY,
        "source_commit": COMMIT,
        "source_tree": TREE,
        "semantic_record_count": 74,
        "semantic_record_digest_sha256":
            semantic_digest,
        "artifact_record_count":
            result_a.artifact_record_count,
        "relation_record_count":
            relation_count,
        "artifact_set_digest_sha256":
            result_a.artifact_set_digest_sha256,
        "relation_set_digest_sha256":
            result_a.relation_set_digest_sha256,
        "integrity_manifest_sha256":
            result_a.integrity_manifest_sha256,
        "projection_tree_digest_sha256":
            result_a.projection_tree_digest_sha256,
        "generated_file_count":
            result_a.generated_file_count,
        "double_build": {
            "relative_path_count":
                result_a.generated_file_count,
            "byte_identical_file_count":
                result_a.generated_file_count,
            "mismatched_files": [],
        },
        "build_a_integrity_clean_count":
            clean_count,
        "build_b_integrity_clean_count":
            clean_count,
        "build_a": str(build_a),
        "build_b": str(build_b),
        "real_vault_created": False,
        "obsidian_config_created": False,
    }

    return report, build_a, build_b


class P3MaterializationTests(unittest.TestCase):
    def test_qualified_p2_core_blob_pins_match_package(
        self,
    ) -> None:
        verify_p2_core_blobs(
            PACKAGE_DIR,
            MATERIALIZATION_CONTRACT,
        )

    def test_tampered_p2_core_blob_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_package = Path(tmp)

            (
                temp_package
                / "deterministic_projection_contract_v0_1.json"
            ).write_bytes(
                (
                    PACKAGE_DIR
                    / "deterministic_projection_contract_v0_1.json"
                ).read_bytes()
            )

            for relative in MATERIALIZATION_CONTRACT[
                "qualified_p2_core_blobs"
            ]:
                name = relative.split(
                    "tools/obsidian_projection/",
                    1,
                )[1]
                (
                    temp_package / name
                ).write_bytes(
                    (PACKAGE_DIR / name).read_bytes()
                )

            (
                temp_package / "builder.py"
            ).write_bytes(b"tampered\n")

            with self.assertRaises(
                MaterializationError
            ):
                verify_p2_core_blobs(
                    temp_package,
                    MATERIALIZATION_CONTRACT,
                )

    def test_tampered_p2a_contract_blob_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            temp_package = Path(tmp)

            (
                temp_package
                / "deterministic_projection_contract_v0_1.json"
            ).write_bytes(b"tampered contract\n")

            for relative in MATERIALIZATION_CONTRACT[
                "qualified_p2_core_blobs"
            ]:
                name = relative.split(
                    "tools/obsidian_projection/",
                    1,
                )[1]
                (
                    temp_package / name
                ).write_bytes(
                    (PACKAGE_DIR / name).read_bytes()
                )

            with self.assertRaises(
                MaterializationError
            ):
                verify_p2_core_blobs(
                    temp_package,
                    MATERIALIZATION_CONTRACT,
                )

    def test_fresh_p2_report_reverification_accepts_equal_pair(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, build_a, _ = build_p2_pair(
                Path(tmp)
            )
            selected = validate_fresh_p2_report(
                report
            )
            self.assertEqual(
                selected.resolve(),
                build_a.resolve(),
            )

    def test_fresh_p2_report_rejects_wrong_source_identity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, _ = build_p2_pair(
                Path(tmp)
            )

            for field, mutant in (
                ("repository", "example/wrong"),
                ("source_commit", "9" * 40),
                ("source_tree", "8" * 40),
            ):
                with self.subTest(field=field):
                    changed = dict(report)
                    changed[field] = mutant
                    with self.assertRaises(
                        MaterializationError
                    ):
                        validate_fresh_p2_report(
                            changed
                        )

    def test_fresh_p2_report_rejects_double_build_mismatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report, _, build_b = build_p2_pair(
                Path(tmp)
            )
            artifact = next(
                (
                    build_b
                    / "generated"
                    / "artifacts"
                ).glob("*.md")
            )
            artifact.write_bytes(
                artifact.read_bytes()
                + b"mutant\n"
            )

            with self.assertRaises(
                MaterializationError
            ):
                validate_fresh_p2_report(
                    report
                )

    def test_incoming_preexisting_path_blocks(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            incoming = Path(tmp) / "incoming"
            incoming.mkdir()

            with self.assertRaises(
                MaterializationError
            ):
                _create_incoming_structure(
                    incoming
                )

    def test_exact_byte_copy_from_qualified_generated_tree(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            _, build_a, _ = build_p2_pair(
                parent
            )
            incoming = parent / "incoming"

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                _create_incoming_structure(
                    incoming
                )

            _copy_qualified_generated_tree(
                build_a,
                incoming,
            )

            self.assertEqual(
                _digest_map(build_a),
                _digest_map(incoming),
            )
            self.assertTrue(
                (incoming / "views").is_dir()
            )
            self.assertFalse(
                (incoming / ".obsidian").exists()
            )

    def test_materialized_projection_verifies_against_p2_identity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            report, build_a, _ = build_p2_pair(
                parent
            )
            incoming = parent / "incoming"

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                _create_incoming_structure(
                    incoming
                )
                _copy_qualified_generated_tree(
                    build_a,
                    incoming,
                )
                identity = (
                    verify_materialized_projection(
                        root=incoming,
                        source_build=build_a,
                        p2_report=report,
                        expected_identity=FAKE_IDENTITY,
                    )
                )

            self.assertEqual(
                identity,
                FAKE_IDENTITY,
            )

    def test_extra_empty_directory_blocks_layout(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "projection"
            for relative in (
                "generated/artifacts",
                "generated/relations",
                "generated/manifests",
                "views",
                "generated/artifacts/extra",
            ):
                (root / relative).mkdir(
                    parents=True,
                    exist_ok=True,
                )

            with self.assertRaises(
                MaterializationError
            ):
                _assert_exact_projection_layout(
                    root
                )

    def test_tampered_incoming_file_blocks_verification(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            report, build_a, _ = build_p2_pair(
                parent
            )
            incoming = parent / "incoming"

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                _create_incoming_structure(
                    incoming
                )
                _copy_qualified_generated_tree(
                    build_a,
                    incoming,
                )

                artifact = next(
                    (
                        incoming
                        / "generated"
                        / "artifacts"
                    ).glob("*.md")
                )
                artifact.write_bytes(
                    artifact.read_bytes()
                    + b"mutant\n"
                )

                with self.assertRaises(
                    MaterializationError
                ):
                    verify_materialized_projection(
                        root=incoming,
                        source_build=build_a,
                        p2_report=report,
                        expected_identity=FAKE_IDENTITY,
                    )

    def test_post_failure_quarantine_renames_only_matching_identity(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            final = parent / "final"
            quarantine = parent / "failed"
            final.mkdir()

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=FAKE_IDENTITY,
            ):
                status = (
                    _quarantine_after_failed_post_verify(
                        final_path=final,
                        expected_identity=FAKE_IDENTITY,
                        quarantine_path=quarantine,
                    )
                )

            self.assertEqual(
                status,
                "QUARANTINED",
            )
            self.assertFalse(final.exists())
            self.assertTrue(quarantine.exists())

    def test_post_failure_quarantine_refuses_identity_mismatch(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            final = parent / "final"
            quarantine = parent / "failed"
            final.mkdir()

            other = FilesystemIdentity(
                volume_serial=999,
                file_identity=999,
                filesystem="NTFS",
            )

            with patch(
                "tools.obsidian_projection.materialize."
                "filesystem_identity",
                return_value=other,
            ):
                status = (
                    _quarantine_after_failed_post_verify(
                        final_path=final,
                        expected_identity=FAKE_IDENTITY,
                        quarantine_path=quarantine,
                    )
                )

            self.assertEqual(
                status,
                "IDENTITY_MISMATCH_LEFT_IN_PLACE",
            )
            self.assertTrue(final.exists())
            self.assertFalse(quarantine.exists())


if __name__ == "__main__":
    unittest.main()
