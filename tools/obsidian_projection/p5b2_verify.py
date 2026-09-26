from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dynamic_inventory import (
    DynamicInventoryError,
    build_from_repository,
    inventory_summary,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "ATDS Obsidian P5-B2 dynamic exact-head "
            "inventory verifier"
        )
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        type=Path,
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
    parser.add_argument(
        "--summary",
        action="store_true",
    )
    return parser


def _blocked(exc: Exception) -> dict[str, object]:
    return {
        "schema":
            "ATDS_OBSIDIAN_P5B2_BLOCKED_REPORT_V0_1",
        "status": "BLOCKED",
        "inventory_qualified": False,
        "error_type": type(exc).__name__,
        "error": str(exc),
        "vault_modified": False,
        "projection_modified": False,
    }


def main() -> int:
    args = _parser().parse_args()

    try:
        inventory = build_from_repository(
            repo_root=args.repo_root,
            source_head=args.source_head,
            source_tree=args.source_tree,
            observed_remote_head=args.observed_remote_head,
        )

        if args.summary:
            report: dict[str, object] = (
                inventory_summary(inventory)
            )
        else:
            report = inventory.as_dict()

        report["status"] = "PASS"
        report["inventory_qualified"] = True

    except (
        DynamicInventoryError,
        OSError,
        ValueError,
    ) as exc:
        print(
            json.dumps(
                _blocked(exc),
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2

    print(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
