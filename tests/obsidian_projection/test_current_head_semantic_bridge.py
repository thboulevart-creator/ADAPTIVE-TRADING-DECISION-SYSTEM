from __future__ import annotations

import copy
import hashlib
import json
import unittest

from tools.obsidian_projection.classification import (
    records_digest_sha256,
)
from tools.obsidian_projection.current_head_semantic_bridge import (
    CONTRACT_BLOB,
    ENTRY_SCHEMA,
    RESULT_SCHEMA,
    CurrentHeadSemanticBridgeError,
    build_current_head_semantic_bridge,
)
from tools.obsidian_projection.dynamic_inventory import (
    DynamicInventory,
    DynamicInventoryEntry,
)


HEAD = "1" * 40
TREE = "2" * 40
BLOB_A = "a" * 40
BLOB_B = "b" * 40
BLOB_C = "c" * 40


def entry(
    path: str,
    blob: str,
    *,
    size: int = 10,
    mode: str = "100644",
    zone: str = "OTHER_TRACKED",
    content_mode: str = "FULL_TEXT",
) -> DynamicInventoryEntry:
    return DynamicInventoryEntry(
        source_path=path,
        source_blob_sha=blob,
        source_blob_size=size,
        git_mode=mode,
        selection_zone=zone,
        content_mode=content_mode,
    )


def inventory(
    entries: tuple[DynamicInventoryEntry, ...],
    *,
    repository: str = (
        "thboulevart-creator/"
        "ADAPTIVE-TRADING-DECISION-SYSTEM"
    ),
    branch: str = "integration/system-v1",
    source_commit: str = HEAD,
    source_tree: str = TREE,
) -> DynamicInventory:
    return DynamicInventory(
        source_repository=repository,
        source_branch=branch,
        source_commit=source_commit,
        source_tree=source_tree,
        entries=entries,
    )


class CurrentHeadSemanticBridgeTests(unittest.TestCase):
    def test_single_markdown_full_text_record(self) -> None:
        inv = inventory(
            (
                entry(
                    "docs/a.md",
                    BLOB_A,
                    zone="DOCUMENTATION",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)

        self.assertEqual(result.as_dict()["schema"], RESULT_SCHEMA)
        self.assertEqual(len(result.entries), 1)

        item = result.entries[0]
        self.assertEqual(item.source_path, "docs/a.md")
        self.assertEqual(item.disposition, "SEMANTIC_FULL_TEXT")
        self.assertEqual(item.artifact_family, "DOCUMENT")
        self.assertFalse(item.semantic_body_read)
        self.assertTrue(item.downstream_body_read_allowed)

        record = item.semantic_record
        self.assertEqual(record.source_repository, inv.source_repository)
        self.assertEqual(record.source_branch, inv.source_branch)
        self.assertEqual(record.source_commit, HEAD)
        self.assertEqual(record.source_tree, TREE)
        self.assertEqual(record.source_path, "docs/a.md")
        self.assertEqual(record.source_blob_sha, BLOB_A)
        self.assertEqual(record.source_blob_size, 10)
        self.assertEqual(record.artifact_family, "DOCUMENT")

    def test_metadata_only_is_preserved_without_body_authority(
        self,
    ) -> None:
        inv = inventory(
            (
                entry(
                    "evidence/large.bin",
                    BLOB_A,
                    size=2_000_000,
                    zone="EVIDENCE",
                    content_mode="METADATA_ONLY",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        item = result.entries[0]

        self.assertEqual(
            item.disposition,
            "SEMANTIC_METADATA_ONLY",
        )
        self.assertEqual(
            item.artifact_family,
            "METADATA_ONLY",
        )
        self.assertFalse(item.semantic_body_read)
        self.assertFalse(item.downstream_body_read_allowed)

    def test_metadata_only_markdown_stays_metadata_only(
        self,
    ) -> None:
        inv = inventory(
            (
                entry(
                    "docs/huge.md",
                    BLOB_A,
                    size=2_000_000,
                    zone="DOCUMENTATION",
                    content_mode="METADATA_ONLY",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.entries[0].artifact_family,
            "METADATA_ONLY",
        )

    def test_full_text_extension_registry(self) -> None:
        cases = {
            "a.md": "DOCUMENT",
            "a.py": "CODE",
            "a.js": "CODE",
            "a.ts": "CODE",
            "a.json": "STRUCTURED_DATA",
            "a.yaml": "STRUCTURED_DATA",
            "a.csv": "STRUCTURED_DATA",
            "a.xml": "STRUCTURED_DATA",
            "a.html": "WEB_ASSET",
            "a.css": "WEB_ASSET",
            "a.txt": "TEXT",
        }
        for source_path, expected in cases.items():
            with self.subTest(source_path=source_path):
                inv = inventory(
                    (
                        entry(
                            source_path,
                            BLOB_A,
                            content_mode="FULL_TEXT",
                        ),
                    )
                )
                result = build_current_head_semantic_bridge(inv)
                self.assertEqual(
                    result.entries[0].artifact_family,
                    expected,
                )

    def test_unregistered_full_text_extension_fails_closed(
        self,
    ) -> None:
        inv = inventory(
            (
                entry(
                    "artifact.bin",
                    BLOB_A,
                    content_mode="FULL_TEXT",
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_arbitrary_source_count_is_allowed(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("b.py", BLOB_B),
                entry(
                    "c.bin",
                    BLOB_C,
                    content_mode="METADATA_ONLY",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(len(result.entries), 3)
        self.assertEqual(len(result.semantic_records), 3)

    def test_empty_inventory_is_deterministic_and_not_count_bound(
        self,
    ) -> None:
        inv = inventory(())
        first = build_current_head_semantic_bridge(inv)
        second = build_current_head_semantic_bridge(inv)
        self.assertEqual(first.as_dict(), second.as_dict())
        self.assertEqual(first.as_dict()["source_blob_count"], 0)
        self.assertEqual(first.semantic_records, ())

    def test_output_count_matches_input_count(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("b.py", BLOB_B),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        payload = result.as_dict()
        self.assertEqual(payload["source_blob_count"], 2)
        self.assertEqual(payload["semantic_record_count"], 2)
        self.assertEqual(len(payload["entries"]), 2)

    def test_conservative_semantic_axes_are_exact(self) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        record = (
            build_current_head_semantic_bridge(inv)
            .entries[0]
            .semantic_record
        )
        self.assertEqual(record.semantic_role, "UNKNOWN")
        self.assertEqual(record.procedure_role, "NONE")
        self.assertEqual(record.authority_role, "CANONICAL")
        self.assertEqual(record.qualification_status, "UNKNOWN")
        self.assertIsNone(record.qualification_scope)
        self.assertEqual(record.scientific_status, "UNKNOWN")
        self.assertEqual(record.epistemic_role, "UNKNOWN")
        self.assertEqual(record.temporal_role, "UNKNOWN")
        self.assertEqual(
            record.persistence_state,
            "TRACKED_IN_GIT_TREE",
        )
        self.assertEqual(record.limitations, ())
        self.assertEqual(record.non_claims, ())

    def test_selection_zone_does_not_change_semantic_record(
        self,
    ) -> None:
        inv_a = inventory(
            (
                entry(
                    "a.py",
                    BLOB_A,
                    zone="IMPLEMENTATION",
                ),
            )
        )
        inv_b = inventory(
            (
                entry(
                    "a.py",
                    BLOB_A,
                    zone="TOOL",
                ),
            )
        )
        result_a = build_current_head_semantic_bridge(inv_a)
        result_b = build_current_head_semantic_bridge(inv_b)

        self.assertEqual(
            result_a.semantic_records,
            result_b.semantic_records,
        )
        self.assertEqual(
            result_a.semantic_record_digest_sha256,
            result_b.semantic_record_digest_sha256,
        )
        self.assertNotEqual(
            result_a.bridge_entry_digest_sha256,
            result_b.bridge_entry_digest_sha256,
        )

    def test_selection_zone_is_preserved_in_binding(
        self,
    ) -> None:
        inv = inventory(
            (
                entry(
                    "tools/a.py",
                    BLOB_A,
                    zone="TOOL",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.entries[0].selection_zone,
            "TOOL",
        )
        self.assertEqual(
            result.as_dict()["entries"][0]["selection_zone"],
            "TOOL",
        )

    def test_content_mode_is_preserved_in_binding(
        self,
    ) -> None:
        inv = inventory(
            (
                entry(
                    "a.bin",
                    BLOB_A,
                    content_mode="METADATA_ONLY",
                ),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.entries[0].content_mode,
            "METADATA_ONLY",
        )

    def test_entry_schema_is_exact(self) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        payload = (
            build_current_head_semantic_bridge(inv)
            .entries[0]
            .as_dict()
        )
        self.assertEqual(payload["schema"], ENTRY_SCHEMA)

    def test_dynamic_inventory_digest_is_bound(self) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.dynamic_inventory_digest_sha256,
            inv.digest_sha256,
        )
        self.assertEqual(
            result.as_dict()[
                "dynamic_inventory_digest_sha256"
            ],
            inv.digest_sha256,
        )

    def test_semantic_record_digest_reuses_qualified_function(
        self,
    ) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("b.py", BLOB_B),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.semantic_record_digest_sha256,
            records_digest_sha256(
                result.semantic_records
            ),
        )

    def test_bridge_contract_version_is_exact(self) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        result = build_current_head_semantic_bridge(inv)
        self.assertEqual(
            result.as_dict()["bridge_contract_version"],
            CONTRACT_BLOB,
        )

    def test_bridge_entry_digest_binds_disposition(
        self,
    ) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        result = build_current_head_semantic_bridge(inv)
        payload = [
            result.entries[0].as_dict()
        ]
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        self.assertEqual(
            result.bridge_entry_digest_sha256,
            hashlib.sha256(canonical).hexdigest(),
        )

    def test_canonical_json_is_stable_and_lf_terminated(
        self,
    ) -> None:
        inv = inventory((entry("a.md", BLOB_A),))
        first = build_current_head_semantic_bridge(inv)
        second = build_current_head_semantic_bridge(inv)
        raw_a = first.canonical_json_bytes()
        raw_b = second.canonical_json_bytes()

        self.assertEqual(raw_a, raw_b)
        self.assertTrue(raw_a.endswith(b"\n"))
        self.assertNotIn(b": ", raw_a)
        self.assertNotIn(b", ", raw_a)
        self.assertEqual(
            json.loads(raw_a.decode("utf-8")),
            first.as_dict(),
        )

    def test_repository_mismatch_is_rejected(self) -> None:
        inv = inventory(
            (entry("a.md", BLOB_A),),
            repository="wrong/repo",
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_branch_mismatch_is_rejected(self) -> None:
        inv = inventory(
            (entry("a.md", BLOB_A),),
            branch="main",
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_malformed_commit_is_rejected(self) -> None:
        inv = inventory(
            (entry("a.md", BLOB_A),),
            source_commit="A" * 40,
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_malformed_tree_is_rejected(self) -> None:
        inv = inventory(
            (entry("a.md", BLOB_A),),
            source_tree="x" * 40,
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_unsorted_entries_are_rejected(self) -> None:
        inv = inventory(
            (
                entry("b.py", BLOB_B),
                entry("a.md", BLOB_A),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_duplicate_source_path_is_rejected(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("a.md", BLOB_B),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_invalid_blob_sha_is_rejected(self) -> None:
        inv = inventory(
            (
                entry("a.md", "A" * 40),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_boolean_blob_size_is_rejected(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A, size=True),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_negative_blob_size_is_rejected(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A, size=-1),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_unsupported_git_mode_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "a.md",
                    BLOB_A,
                    mode="120000",
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_unknown_content_mode_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "a.md",
                    BLOB_A,
                    content_mode="UNKNOWN",
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_empty_selection_zone_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "a.md",
                    BLOB_A,
                    zone="",
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_absolute_path_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "/a.md",
                    BLOB_A,
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_parent_traversal_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "docs/../a.md",
                    BLOB_A,
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_backslash_path_is_rejected(self) -> None:
        inv = inventory(
            (
                entry(
                    "docs\\a.md",
                    BLOB_A,
                ),
            )
        )
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(inv)

    def test_input_inventory_is_not_mutated(self) -> None:
        inv = inventory(
            (
                entry(
                    "a.md",
                    BLOB_A,
                    zone="DOCUMENTATION",
                ),
                entry(
                    "b.bin",
                    BLOB_B,
                    content_mode="METADATA_ONLY",
                ),
            )
        )
        before = copy.deepcopy(inv)
        build_current_head_semantic_bridge(inv)
        self.assertEqual(inv, before)

    def test_same_input_produces_same_result(self) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("b.py", BLOB_B),
            )
        )
        first = build_current_head_semantic_bridge(inv)
        second = build_current_head_semantic_bridge(inv)
        self.assertEqual(first, second)
        self.assertEqual(
            first.canonical_json_bytes(),
            second.canonical_json_bytes(),
        )

    def test_source_provenance_is_identical_across_records(
        self,
    ) -> None:
        inv = inventory(
            (
                entry("a.md", BLOB_A),
                entry("b.py", BLOB_B),
            )
        )
        result = build_current_head_semantic_bridge(inv)
        for record in result.semantic_records:
            self.assertEqual(
                record.source_repository,
                inv.source_repository,
            )
            self.assertEqual(
                record.source_branch,
                inv.source_branch,
            )
            self.assertEqual(
                record.source_commit,
                inv.source_commit,
            )
            self.assertEqual(
                record.source_tree,
                inv.source_tree,
            )

    def test_input_must_be_dynamic_inventory(self) -> None:
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_current_head_semantic_bridge(  # type: ignore[arg-type]
                {"entries": []}
            )


if __name__ == "__main__":
    unittest.main()
