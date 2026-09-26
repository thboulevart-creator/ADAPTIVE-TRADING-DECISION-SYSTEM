from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.obsidian_projection.git_source import TreeEntry
from tools.obsidian_projection.inventory import (
    FrozenInventory,
    InventoryEntry,
    InventoryError,
    load_inventory,
    verify_inventory,
    verify_inventory_blob_bytes,
)

COMMIT = "1" * 40
TREE = "2" * 40
BLOB_A = "3" * 40
BLOB_B = "4" * 40


class FakeSource:
    expected_repository = (
        "thboulevart-creator/"
        "ADAPTIVE-TRADING-DECISION-SYSTEM"
    )
    source_commit = COMMIT
    expected_tree = TREE

    def __init__(self, entries):
        self._entries = entries
        self.repository_verified = False
        self.source_verified = False
        self.blobs = {}

    def verify_repository(self):
        self.repository_verified = True

    def verify_frozen_source(self):
        self.source_verified = True

    def tree_entry_map(self):
        return {
            entry.path: entry
            for entry in self._entries
        }

    def read_blob(self, oid):
        return self.blobs[oid]


def inventory(entries) -> FrozenInventory:
    return FrozenInventory(
        schema="ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1",
        source_repository=FakeSource.expected_repository,
        source_branch="integration/system-v1",
        source_commit=COMMIT,
        source_tree=TREE,
        source_artifact_count=len(entries),
        entries=tuple(entries),
    )


class InventoryTests(unittest.TestCase):
    def test_exact_inventory_verifies_and_extra_tree_entry_is_not_admitted(
        self,
    ):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "100644",
                    "blob",
                    BLOB_A,
                    5,
                ),
                TreeEntry(
                    "outside.md",
                    "100644",
                    "blob",
                    BLOB_B,
                    9,
                ),
            ]
        )

        verified = verify_inventory(
            source,
            inventory([declared]),
        )

        self.assertEqual(len(verified), 1)
        self.assertEqual(
            verified[0].inventory.source_path,
            "a.md",
        )
        self.assertTrue(source.repository_verified)
        self.assertTrue(source.source_verified)

    def test_blob_mismatch_blocks(self):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "100644",
                    "blob",
                    BLOB_B,
                    5,
                )
            ]
        )

        with self.assertRaises(InventoryError):
            verify_inventory(
                source,
                inventory([declared]),
            )

    def test_symlink_mode_blocks_even_when_git_reports_blob(
        self,
    ):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "120000",
                    "blob",
                    BLOB_A,
                    5,
                )
            ]
        )

        with self.assertRaises(InventoryError):
            verify_inventory(
                source,
                inventory([declared]),
            )

    def test_inventory_commit_mismatch_blocks(self):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        bad = FrozenInventory(
            schema=(
                "ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1"
            ),
            source_repository=(
                FakeSource.expected_repository
            ),
            source_branch="integration/system-v1",
            source_commit="9" * 40,
            source_tree=TREE,
            source_artifact_count=1,
            entries=(declared,),
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "100644",
                    "blob",
                    BLOB_A,
                    5,
                )
            ]
        )

        with self.assertRaises(InventoryError):
            verify_inventory(source, bad)

    def test_loader_rejects_duplicate_path(self):
        payload = {
            "schema": (
                "ATDS_OBSIDIAN_PILOT_INVENTORY_V0_1"
            ),
            "source_repository": (
                FakeSource.expected_repository
            ),
            "source_branch":
                "integration/system-v1",
            "source_commit": COMMIT,
            "source_tree": TREE,
            "source_artifact_count": 2,
            "entries": [
                {
                    "source_path": "a.md",
                    "source_blob_sha": BLOB_A,
                    "source_blob_size": 5,
                    "inventory_class":
                        "AP_PROGRAM",
                },
                {
                    "source_path": "a.md",
                    "source_blob_sha": BLOB_B,
                    "source_blob_size": 7,
                    "inventory_class":
                        "EVIDENCE",
                },
            ],
        }

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.json"
            path.write_text(
                json.dumps(payload),
                encoding="utf-8",
            )

            with self.assertRaises(InventoryError):
                load_inventory(path)

    def test_inventory_digest_is_order_independent(
        self,
    ):
        a = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        b = InventoryEntry(
            "b.md",
            BLOB_B,
            7,
            "EVIDENCE",
        )

        self.assertEqual(
            inventory([a, b]).digest_sha256,
            inventory([b, a]).digest_sha256,
        )

    def test_verify_inventory_blob_bytes_reads_declared_blobs(
        self,
    ):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "100644",
                    "blob",
                    BLOB_A,
                    5,
                )
            ]
        )
        source.blobs[BLOB_A] = b"12345"

        verified = verify_inventory(
            source,
            inventory([declared]),
        )

        self.assertEqual(
            verify_inventory_blob_bytes(
                source,
                verified,
            ),
            5,
        )

    def test_verify_inventory_blob_bytes_blocks_length_mismatch(
        self,
    ):
        declared = InventoryEntry(
            "a.md",
            BLOB_A,
            5,
            "AP_PROGRAM",
        )
        source = FakeSource(
            [
                TreeEntry(
                    "a.md",
                    "100644",
                    "blob",
                    BLOB_A,
                    5,
                )
            ]
        )
        source.blobs[BLOB_A] = b"1234"

        verified = verify_inventory(
            source,
            inventory([declared]),
        )

        with self.assertRaises(InventoryError):
            verify_inventory_blob_bytes(
                source,
                verified,
            )


if __name__ == "__main__":
    unittest.main()
