from __future__ import annotations

import copy
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.obsidian_projection.current_head_semantic_bridge import (
    CurrentHeadSemanticBridgeError,
)
from tools.obsidian_projection.dynamic_inventory import (
    DynamicInventory,
    DynamicInventoryEntry,
)
from tools.obsidian_projection.p5d3b_verify import (
    BLOCKED_SCHEMA,
    REPORT_SCHEMA,
    _blocked,
    _summary_from_inventory,
    build_report,
)


HEAD = "1" * 40
TREE = "2" * 40
BLOB_A = "a" * 40
BLOB_B = "b" * 40


def inventory() -> DynamicInventory:
    return DynamicInventory(
        source_repository=(
            "thboulevart-creator/"
            "ADAPTIVE-TRADING-DECISION-SYSTEM"
        ),
        source_branch="integration/system-v1",
        source_commit=HEAD,
        source_tree=TREE,
        entries=(
            DynamicInventoryEntry(
                source_path="docs/a.md",
                source_blob_sha=BLOB_A,
                source_blob_size=10,
                git_mode="100644",
                selection_zone="DOCUMENTATION",
                content_mode="FULL_TEXT",
            ),
            DynamicInventoryEntry(
                source_path="evidence/b.bin",
                source_blob_sha=BLOB_B,
                source_blob_size=2_000_000,
                git_mode="100644",
                selection_zone="EVIDENCE",
                content_mode="METADATA_ONLY",
            ),
        ),
    )


class P5D3BVerifyTests(unittest.TestCase):
    def test_summary_is_pass_and_count_complete(self) -> None:
        inv = inventory()
        report = _summary_from_inventory(inv)

        self.assertEqual(report["schema"], REPORT_SCHEMA)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["source_blob_count"], 2)
        self.assertEqual(report["full_text_count"], 1)
        self.assertEqual(report["metadata_only_count"], 1)
        self.assertEqual(report["semantic_record_count"], 2)
        self.assertTrue(
            report["all_semantic_body_read_false"]
        )
        self.assertTrue(
            report[
                "all_metadata_only_downstream_body_read_false"
            ]
        )

    def test_summary_binds_exact_inventory_digest(
        self,
    ) -> None:
        inv = inventory()
        report = _summary_from_inventory(inv)
        self.assertEqual(
            report["dynamic_inventory_digest_sha256"],
            inv.digest_sha256,
        )

    def test_summary_contains_no_entry_or_body_payload(
        self,
    ) -> None:
        report = _summary_from_inventory(inventory())
        for forbidden in (
            "entries",
            "semantic_records",
            "source_body",
            "source_bytes",
            "raw",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, report)

    def test_summary_preserves_non_mutation_claims(
        self,
    ) -> None:
        report = _summary_from_inventory(inventory())
        self.assertFalse(report["real_vault_modified"])
        self.assertFalse(report["projection_modified"])
        self.assertFalse(
            report["canonical_worktree_write_required"]
        )
        self.assertFalse(
            report["fixed_expected_source_count_used"]
        )

    def test_summary_does_not_mutate_inventory(self) -> None:
        inv = inventory()
        before = copy.deepcopy(inv)
        _summary_from_inventory(inv)
        self.assertEqual(inv, before)

    def test_build_report_rejects_head_observation_mismatch(
        self,
    ) -> None:
        with self.assertRaises(CurrentHeadSemanticBridgeError):
            build_report(
                repo_root=Path("."),
                source_head=HEAD,
                source_tree=TREE,
                observed_remote_head="3" * 40,
            )

    def test_build_report_reuses_p5b2_inventory_builder(
        self,
    ) -> None:
        inv = inventory()
        with patch(
            "tools.obsidian_projection.p5d3b_verify."
            "build_from_repository",
            return_value=inv,
        ) as mocked:
            report = build_report(
                repo_root=Path("."),
                source_head=HEAD,
                source_tree=TREE,
                observed_remote_head=HEAD,
            )

        mocked.assert_called_once()
        kwargs = mocked.call_args.kwargs
        self.assertEqual(kwargs["source_head"], HEAD)
        self.assertEqual(kwargs["source_tree"], TREE)
        self.assertEqual(
            kwargs["observed_remote_head"],
            HEAD,
        )
        self.assertEqual(report["source_head"], HEAD)
        self.assertEqual(report["source_tree"], TREE)

    def test_build_report_rejects_inventory_head_drift(
        self,
    ) -> None:
        inv = inventory()
        drifted = DynamicInventory(
            source_repository=inv.source_repository,
            source_branch=inv.source_branch,
            source_commit="4" * 40,
            source_tree=inv.source_tree,
            entries=inv.entries,
        )
        with patch(
            "tools.obsidian_projection.p5d3b_verify."
            "build_from_repository",
            return_value=drifted,
        ):
            with self.assertRaises(
                CurrentHeadSemanticBridgeError
            ):
                build_report(
                    repo_root=Path("."),
                    source_head=HEAD,
                    source_tree=TREE,
                    observed_remote_head=HEAD,
                )

    def test_build_report_rejects_inventory_tree_drift(
        self,
    ) -> None:
        inv = inventory()
        drifted = DynamicInventory(
            source_repository=inv.source_repository,
            source_branch=inv.source_branch,
            source_commit=inv.source_commit,
            source_tree="5" * 40,
            entries=inv.entries,
        )
        with patch(
            "tools.obsidian_projection.p5d3b_verify."
            "build_from_repository",
            return_value=drifted,
        ):
            with self.assertRaises(
                CurrentHeadSemanticBridgeError
            ):
                build_report(
                    repo_root=Path("."),
                    source_head=HEAD,
                    source_tree=TREE,
                    observed_remote_head=HEAD,
                )

    def test_blocked_report_is_summary_only(self) -> None:
        report = _blocked(
            CurrentHeadSemanticBridgeError(
                "synthetic failure"
            )
        )
        self.assertEqual(
            report["schema"],
            BLOCKED_SCHEMA,
        )
        self.assertEqual(report["status"], "BLOCKED")
        self.assertEqual(
            report["error_type"],
            "CurrentHeadSemanticBridgeError",
        )
        self.assertEqual(
            report["error_message"],
            "synthetic failure",
        )
        self.assertFalse(report["real_vault_modified"])
        self.assertFalse(report["projection_modified"])


if __name__ == "__main__":
    unittest.main()
