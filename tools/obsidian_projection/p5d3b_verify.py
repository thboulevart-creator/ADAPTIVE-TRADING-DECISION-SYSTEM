from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .current_head_semantic_bridge import (
    CurrentHeadSemanticBridgeError,
    build_current_head_semantic_bridge,
)
from .dynamic_inventory import (
    DynamicInventoryError,
    build_from_repository,
)


REPORT_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3B_REAL_HEAD_BRIDGE_REPORT_V0_1"
)
BLOCKED_SCHEMA = (
    "ATDS_OBSIDIAN_P5D3B_REAL_HEAD_BRIDGE_BLOCKED_V0_1"
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "P5-D3B real-head qualification harness. "
            "Builds P5-B2 inventory, applies the pure bridge, "
            "and emits summary-only evidence."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
    )
    parser.add_argument(
        "--source-head",
        required=True,
    )
    parser.add_argument(
        "--source-tree",
        required=True,
    )
    parser.add_argument(
        "--observed-remote-head",
        required=True,
    )
    return parser


def _summary_from_inventory(
    inventory: Any,
) -> dict[str, Any]:
    bridge = build_current_head_semantic_bridge(
        inventory
    )

    entries = bridge.entries
    metadata_entries = tuple(
        item
        for item in entries
        if item.content_mode == "METADATA_ONLY"
    )

    all_semantic_body_read_false = all(
        item.semantic_body_read is False
        for item in entries
    )
    all_metadata_only_downstream_body_read_false = all(
        item.downstream_body_read_allowed is False
        for item in metadata_entries
    )

    if len(entries) != len(inventory.entries):
        raise CurrentHeadSemanticBridgeError(
            "bridge/source entry count mismatch"
        )
    if (
        len(bridge.semantic_records)
        != len(inventory.entries)
    ):
        raise CurrentHeadSemanticBridgeError(
            "bridge semantic record count mismatch"
        )
    if (
        bridge.full_text_count
        != inventory.full_text_count
    ):
        raise CurrentHeadSemanticBridgeError(
            "bridge FULL_TEXT count mismatch"
        )
    if (
        bridge.metadata_only_count
        != inventory.metadata_only_count
    ):
        raise CurrentHeadSemanticBridgeError(
            "bridge METADATA_ONLY count mismatch"
        )
    if not all_semantic_body_read_false:
        raise CurrentHeadSemanticBridgeError(
            "bridge semantic body read invariant failed"
        )
    if (
        not all_metadata_only_downstream_body_read_false
    ):
        raise CurrentHeadSemanticBridgeError(
            "metadata-only downstream read invariant failed"
        )

    return {
        "schema": REPORT_SCHEMA,
        "repository": bridge.source_repository,
        "branch": bridge.source_branch,
        "source_head": bridge.source_commit,
        "source_tree": bridge.source_tree,
        "dynamic_inventory_digest_sha256":
            bridge.dynamic_inventory_digest_sha256,
        "bridge_contract_version":
            bridge.as_dict()["bridge_contract_version"],
        "source_blob_count":
            len(inventory.entries),
        "full_text_count":
            bridge.full_text_count,
        "metadata_only_count":
            bridge.metadata_only_count,
        "semantic_record_count":
            len(bridge.semantic_records),
        "semantic_record_digest_sha256":
            bridge.semantic_record_digest_sha256,
        "bridge_entry_digest_sha256":
            bridge.bridge_entry_digest_sha256,
        "all_semantic_body_read_false":
            all_semantic_body_read_false,
        "all_metadata_only_downstream_body_read_false":
            all_metadata_only_downstream_body_read_false,
        "fixed_expected_source_count_used": False,
        "real_vault_modified": False,
        "projection_modified": False,
        "canonical_worktree_write_required": False,
        "status": "PASS",
    }


def build_report(
    *,
    repo_root: Path,
    source_head: str,
    source_tree: str,
    observed_remote_head: str,
) -> dict[str, Any]:
    if source_head != observed_remote_head:
        raise CurrentHeadSemanticBridgeError(
            "source HEAD differs from observed remote HEAD"
        )

    inventory = build_from_repository(
        repo_root=repo_root,
        source_head=source_head,
        source_tree=source_tree,
        observed_remote_head=observed_remote_head,
    )

    report = _summary_from_inventory(inventory)

    if report["source_head"] != source_head:
        raise CurrentHeadSemanticBridgeError(
            "report source HEAD mismatch"
        )
    if report["source_tree"] != source_tree:
        raise CurrentHeadSemanticBridgeError(
            "report source tree mismatch"
        )

    return report


def _blocked(exc: BaseException) -> dict[str, Any]:
    return {
        "schema": BLOCKED_SCHEMA,
        "status": "BLOCKED",
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "real_vault_modified": False,
        "projection_modified": False,
        "canonical_worktree_write_required": False,
    }


def main() -> int:
    args = _parser().parse_args()

    try:
        report = build_report(
            repo_root=Path(args.repo_root),
            source_head=args.source_head,
            source_tree=args.source_tree,
            observed_remote_head=(
                args.observed_remote_head
            ),
        )
    except (
        CurrentHeadSemanticBridgeError,
        DynamicInventoryError,
        OSError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                _blocked(exc),
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
        return 2

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
