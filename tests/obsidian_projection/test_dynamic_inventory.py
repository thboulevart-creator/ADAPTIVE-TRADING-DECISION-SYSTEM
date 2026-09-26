from __future__ import annotations

import hashlib
import json
import unittest

from tools.obsidian_projection.dynamic_inventory import (
    DynamicInventoryError,
    SecretDetectedError,
    SensitivePathError,
    build_dynamic_inventory,
    inventory_summary,
)
from tools.obsidian_projection.git_source import TreeEntry


REPO = (
    "thboulevart-creator/"
    "ADAPTIVE-TRADING-DECISION-SYSTEM"
)
BRANCH = "integration/system-v1"
COMMIT = "1" * 40
TREE = "2" * 40


def oid(seed: str) -> str:
    return hashlib.sha1(
        seed.encode("utf-8")
    ).hexdigest()


class FakeSource:
    def __init__(
        self,
        entries: list[TreeEntry],
        blobs: dict[str, bytes],
        *,
        repository: str = REPO,
        commit: str = COMMIT,
        tree: str = TREE,
    ) -> None:
        self.expected_repository = repository
        self.source_commit = commit
        self.expected_tree = tree
        self._entries = tuple(entries)
        self._blobs = blobs
        self.repository_verified = False
        self.source_verified = False
        self.read_oids: list[str] = []

    def verify_repository(self) -> None:
        self.repository_verified = True

    def verify_frozen_source(self) -> None:
        self.source_verified = True

    def tree_entries(self) -> tuple[TreeEntry, ...]:
        return self._entries

    def read_blob(self, blob_oid: str) -> bytes:
        self.read_oids.append(blob_oid)
        return self._blobs[blob_oid]


def blob_entry(
    path: str,
    raw: bytes,
    *,
    mode: str = "100644",
    object_type: str = "blob",
    size: int | None = None,
) -> tuple[TreeEntry, dict[str, bytes]]:
    blob_oid = oid(path + ":" + str(len(raw)))
    entry = TreeEntry(
        path=path,
        mode=mode,
        object_type=object_type,
        oid=blob_oid,
        size=len(raw) if size is None else size,
    )
    return entry, {blob_oid: raw}


def source_for(
    *items: tuple[TreeEntry, dict[str, bytes]],
) -> FakeSource:
    entries: list[TreeEntry] = []
    blobs: dict[str, bytes] = {}
    for entry, mapping in items:
        entries.append(entry)
        blobs.update(mapping)
    return FakeSource(entries, blobs)


class DynamicInventoryTests(unittest.TestCase):
    def build(
        self,
        source: FakeSource,
        *,
        branch: str = BRANCH,
        observed: str = COMMIT,
    ):
        return build_dynamic_inventory(
            source=source,
            source_branch=branch,
            observed_remote_head=observed,
        )

    def test_regular_tracked_text_is_inventoried(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "docs/a.md",
                b"# A\n",
            )
        )
        inventory = self.build(source)

        self.assertTrue(
            source.repository_verified
        )
        self.assertTrue(source.source_verified)
        self.assertEqual(len(inventory.entries), 1)
        item = inventory.entries[0]
        self.assertEqual(
            item.selection_zone,
            "DOCUMENTATION",
        )
        self.assertEqual(
            item.content_mode,
            "FULL_TEXT",
        )

    def test_unknown_zone_is_not_dropped(self) -> None:
        source = source_for(
            blob_entry(
                "new-zone/a.md",
                b"# A\n",
            )
        )
        item = self.build(source).entries[0]
        self.assertEqual(
            item.selection_zone,
            "OTHER_TRACKED",
        )

    def test_root_file_is_inventoried(self) -> None:
        source = source_for(
            blob_entry(
                "README.md",
                b"# Repo\n",
            )
        )
        item = self.build(source).entries[0]
        self.assertEqual(
            item.selection_zone,
            "ROOT_DOCUMENT",
        )

    def test_executable_regular_blob_is_allowed(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "tools/run.sh",
                b"#!/bin/sh\n",
                mode="100755",
            )
        )
        item = self.build(source).entries[0]
        self.assertEqual(item.git_mode, "100755")
        self.assertEqual(
            item.content_mode,
            "FULL_TEXT",
        )

    def test_large_text_is_metadata_only_without_body_read(
        self,
    ) -> None:
        raw = b"x" * (1_048_576 + 1)
        item, blobs = blob_entry(
            "evidence/large.json",
            raw,
        )
        source = FakeSource([item], blobs)

        inventory = self.build(source)

        self.assertEqual(
            inventory.entries[0].content_mode,
            "METADATA_ONLY",
        )
        self.assertEqual(source.read_oids, [])

    def test_non_allowlisted_extension_is_metadata_only(
        self,
    ) -> None:
        item, blobs = blob_entry(
            "evidence/raw.bi5",
            b"\x00\x01\x02",
        )
        source = FakeSource([item], blobs)

        inventory = self.build(source)
        self.assertEqual(
            inventory.entries[0].content_mode,
            "METADATA_ONLY",
        )
        self.assertEqual(source.read_oids, [])

    def test_invalid_utf8_becomes_metadata_only(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "docs/a.txt",
                b"\xff\xfe",
            )
        )
        self.assertEqual(
            self.build(source)
            .entries[0]
            .content_mode,
            "METADATA_ONLY",
        )

    def test_nul_text_becomes_metadata_only(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "docs/a.txt",
                b"a\x00b",
            )
        )
        self.assertEqual(
            self.build(source)
            .entries[0]
            .content_mode,
            "METADATA_ONLY",
        )

    def test_full_text_length_mismatch_blocks(
        self,
    ) -> None:
        entry, blobs = blob_entry(
            "docs/a.md",
            b"abc",
            size=4,
        )
        source = FakeSource([entry], blobs)
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_private_key_signature_blocks_without_value(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "docs/a.txt",
                (
                    b"-----BEGIN PRIVATE KEY-----\n"
                    b"TOP_SECRET_PAYLOAD_123\n"
                ),
            )
        )
        with self.assertRaises(
            SecretDetectedError
        ) as ctx:
            self.build(source)

        message = str(ctx.exception)
        self.assertIn(
            "PRIVATE_KEY_BLOCK",
            message,
        )
        self.assertIn(
            "path_sha256=",
            message,
        )
        self.assertNotIn(
            "TOP_SECRET_PAYLOAD_123",
            message,
        )

    def test_sensitive_path_blocks_without_plaintext_path(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "config/.env",
                b"VALUE=x\n",
            )
        )
        with self.assertRaises(
            SensitivePathError
        ) as ctx:
            self.build(source)

        message = str(ctx.exception)
        self.assertIn("path_sha256=", message)
        self.assertNotIn("config/.env", message)

    def test_forbidden_generated_surface_blocks(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "generated/a.md",
                b"# derived\n",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_forbidden_nested_runtime_cache_blocks(
        self,
    ) -> None:
        source = source_for(
            blob_entry(
                "tools/__pycache__/a.pyc",
                b"x",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_symlink_blocks_head(self) -> None:
        source = source_for(
            blob_entry(
                "docs/link",
                b"target",
                mode="120000",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_gitlink_blocks_head(self) -> None:
        entry = TreeEntry(
            path="vendor/submodule",
            mode="160000",
            object_type="commit",
            oid=oid("gitlink"),
            size=None,
        )
        source = FakeSource([entry], {})
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_wrong_repository_blocks(self) -> None:
        source = source_for(
            blob_entry(
                "docs/a.md",
                b"# A\n",
            )
        )
        source.expected_repository = "other/repo"
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_wrong_branch_blocks(self) -> None:
        source = source_for(
            blob_entry(
                "docs/a.md",
                b"# A\n",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(
                source,
                branch="main",
            )

    def test_wrong_observed_head_blocks(self) -> None:
        source = source_for(
            blob_entry(
                "docs/a.md",
                b"# A\n",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(
                source,
                observed="9" * 40,
            )

    def test_duplicate_path_blocks(self) -> None:
        first = blob_entry(
            "docs/a.md",
            b"A",
        )
        second_entry, second_blobs = blob_entry(
            "docs/a.md",
            b"BB",
        )
        source = FakeSource(
            [first[0], second_entry],
            {
                **first[1],
                **second_blobs,
            },
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_backslash_path_blocks(self) -> None:
        source = source_for(
            blob_entry(
                "docs\\a.md",
                b"A",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_parent_traversal_blocks(self) -> None:
        source = source_for(
            blob_entry(
                "docs/../a.md",
                b"A",
            )
        )
        with self.assertRaises(
            DynamicInventoryError
        ):
            self.build(source)

    def test_entries_are_utf8_bytewise_sorted(
        self,
    ) -> None:
        source = source_for(
            blob_entry("docs/z.md", b"z"),
            blob_entry("docs/a.md", b"a"),
        )
        inventory = self.build(source)
        self.assertEqual(
            [item.source_path for item in inventory.entries],
            ["docs/a.md", "docs/z.md"],
        )

    def test_digest_is_order_independent_for_same_tree_entries(
        self,
    ) -> None:
        a = blob_entry("docs/a.md", b"a")
        z = blob_entry("docs/z.md", b"z")

        one = self.build(source_for(a, z))
        two = self.build(source_for(z, a))

        self.assertEqual(
            one.digest_sha256,
            two.digest_sha256,
        )

    def test_inventory_json_contains_no_host_volatility(
        self,
    ) -> None:
        inventory = self.build(
            source_for(
                blob_entry(
                    "docs/a.md",
                    b"a",
                )
            )
        )
        value = json.loads(
            inventory.canonical_json_bytes()
        )
        encoded = json.dumps(value)

        for forbidden in (
            "timestamp",
            "hostname",
            "username",
            "absolute_path",
        ):
            self.assertNotIn(
                forbidden,
                encoded,
            )

    def test_summary_counts_zones_and_modes(
        self,
    ) -> None:
        inventory = self.build(
            source_for(
                blob_entry(
                    "docs/a.md",
                    b"a",
                ),
                blob_entry(
                    "src/a.py",
                    b"print('x')\n",
                ),
                blob_entry(
                    "evidence/a.bi5",
                    b"\x00",
                ),
            )
        )
        summary = inventory_summary(inventory)

        self.assertEqual(
            summary["source_blob_count"],
            3,
        )
        self.assertEqual(
            summary["full_text_count"],
            2,
        )
        self.assertEqual(
            summary["metadata_only_count"],
            1,
        )
        self.assertEqual(
            summary["selection_zone_counts"],
            {
                "DOCUMENTATION": 1,
                "EVIDENCE": 1,
                "IMPLEMENTATION": 1,
            },
        )
        self.assertFalse(
            summary["vault_modified"]
        )
        self.assertFalse(
            summary["projection_modified"]
        )


if __name__ == "__main__":
    unittest.main()
