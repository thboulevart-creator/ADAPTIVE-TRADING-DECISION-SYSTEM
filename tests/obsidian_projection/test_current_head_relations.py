from __future__ import annotations

import unittest
from dataclasses import replace

from tools.obsidian_projection.classification import (
    git_blob_oid,
)
from tools.obsidian_projection.current_head_projection import (
    load_current_head_projection_contract,
)
from tools.obsidian_projection.current_head_relations import (
    CurrentHeadRelationError,
    extract_current_head_relations,
)
from tools.obsidian_projection.current_head_semantic_bridge import (
    build_current_head_semantic_bridge,
)
from tools.obsidian_projection.dynamic_inventory import (
    DynamicInventory,
    DynamicInventoryEntry,
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


def fixture() -> tuple[
    FakeSource,
    object,
    dict[str, bytes],
]:
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
    blob_map: dict[str, bytes] = {}
    for path in sorted(
        raw_by_path,
        key=lambda item: item.encode("utf-8"),
    ):
        raw = raw_by_path[path]
        oid = git_blob_oid(raw)
        blob_map[oid] = raw
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
    bridge = build_current_head_semantic_bridge(
        inventory
    )
    return FakeSource(blob_map), bridge, raw_by_path


class CurrentHeadRelationAdapterTests(
    unittest.TestCase
):
    def test_reads_only_full_text_md_and_json(
        self,
    ) -> None:
        source, bridge, _ = fixture()
        result = extract_current_head_relations(
            source=source,
            bridge=bridge,
            contract=load_current_head_projection_contract(),
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
        self.assertEqual(len(source.reads), 2)
        self.assertEqual(
            result.relation_source_body_read_count,
            2,
        )
        self.assertEqual(
            result.metadata_only_body_read_count,
            0,
        )

    def test_emits_two_exact_references(self) -> None:
        source, bridge, _ = fixture()
        result = extract_current_head_relations(
            source=source,
            bridge=bridge,
            contract=load_current_head_projection_contract(),
        )

        self.assertEqual(
            len(result.relations),
            2,
        )
        self.assertEqual(
            {item.basis for item in result.relations},
            {
                "EXPLICIT_STRUCTURED",
                "EXPLICIT_TEXT",
            },
        )
        self.assertEqual(
            {item.relation_type for item in result.relations},
            {"REFERENCES"},
        )

    def test_metadata_only_may_be_target_without_read(
        self,
    ) -> None:
        source, bridge, _ = fixture()
        result = extract_current_head_relations(
            source=source,
            bridge=bridge,
            contract=load_current_head_projection_contract(),
        )

        metadata_entry = next(
            entry
            for entry in bridge.entries
            if entry.content_mode == "METADATA_ONLY"
        )
        metadata_oid = metadata_entry.source_blob_sha

        text_relation = next(
            item
            for item in result.relations
            if item.basis == "EXPLICIT_TEXT"
        )
        self.assertNotIn(
            metadata_oid,
            source.reads,
        )
        self.assertEqual(
            text_relation.evidence_source_path,
            "docs/source.md",
        )

    def test_metadata_only_downstream_authority_is_fail_closed(
        self,
    ) -> None:
        source, bridge, _ = fixture()
        entries = list(bridge.entries)
        index = next(
            i
            for i, entry in enumerate(entries)
            if entry.content_mode == "METADATA_ONLY"
        )
        entries[index] = replace(
            entries[index],
            downstream_body_read_allowed=True,
        )
        mutant = replace(
            bridge,
            entries=tuple(entries),
        )

        with self.assertRaises(
            CurrentHeadRelationError
        ):
            extract_current_head_relations(
                source=source,
                bridge=mutant,
                contract=load_current_head_projection_contract(),
            )

        self.assertEqual(source.reads, [])

    def test_blob_identity_mismatch_is_rejected(
        self,
    ) -> None:
        source, bridge, _ = fixture()
        eligible = next(
            entry
            for entry in bridge.entries
            if entry.source_path == "docs/source.md"
        )
        source.blobs[
            eligible.source_blob_sha
        ] = b"mutated\n"

        with self.assertRaises(
            CurrentHeadRelationError
        ):
            extract_current_head_relations(
                source=source,
                bridge=bridge,
                contract=load_current_head_projection_contract(),
            )

    def test_whitespace_wrapped_paths_are_not_normalized(
        self,
    ) -> None:
        source, bridge, _ = fixture()

        json_entry = next(
            entry
            for entry in bridge.entries
            if entry.source_path == "data/refs.json"
        )
        md_entry = next(
            entry
            for entry in bridge.entries
            if entry.source_path == "docs/source.md"
        )

        json_raw = b'{"reference":" docs/source.md "}\n'
        md_raw = (
            b"# Source\n\nBinary target: "
            b"\x60 assets/blob.bin \x60\n"
        )

        from tools.obsidian_projection.classification import (
            git_blob_oid as _oid,
        )

        json_oid = _oid(json_raw)
        md_oid = _oid(md_raw)
        source.blobs[json_oid] = json_raw
        source.blobs[md_oid] = md_raw

        entries = []
        for entry in bridge.entries:
            if entry.source_path == "data/refs.json":
                entries.append(
                    replace(
                        entry,
                        source_blob_sha=json_oid,
                        source_blob_size=len(json_raw),
                        semantic_record=replace(
                            entry.semantic_record,
                            source_blob_sha=json_oid,
                            source_blob_size=len(json_raw),
                        ),
                    )
                )
            elif entry.source_path == "docs/source.md":
                entries.append(
                    replace(
                        entry,
                        source_blob_sha=md_oid,
                        source_blob_size=len(md_raw),
                        semantic_record=replace(
                            entry.semantic_record,
                            source_blob_sha=md_oid,
                            source_blob_size=len(md_raw),
                        ),
                    )
                )
            else:
                entries.append(entry)

        mutant = replace(
            bridge,
            entries=tuple(entries),
        )
        result = extract_current_head_relations(
            source=source,
            bridge=mutant,
            contract=load_current_head_projection_contract(),
        )
        self.assertEqual(
            result.relations,
            (),
        )
        self.assertEqual(
            result.relation_source_body_read_count,
            2,
        )

    def test_audit_contains_only_full_text_rows(
        self,
    ) -> None:
        source, bridge, _ = fixture()
        result = extract_current_head_relations(
            source=source,
            bridge=bridge,
            contract=load_current_head_projection_contract(),
        )

        self.assertEqual(
            len(result.body_read_audit_rows),
            2,
        )
        self.assertTrue(
            all(
                row.content_mode == "FULL_TEXT"
                for row in result.body_read_audit_rows
            )
        )
        self.assertEqual(
            [
                row.source_path
                for row in result.body_read_audit_rows
            ],
            [
                "data/refs.json",
                "docs/source.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
