from __future__ import annotations

import argparse
import json
from pathlib import Path

from .git_source import FrozenGitSource, sha256_bytes
from .inventory import (
    load_inventory,
    verify_inventory,
    verify_inventory_blob_bytes,
)

EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
SOURCE_COMMIT = "7bd8c1312430dfc3def5523eb65397a5d6a5ae05"
SOURCE_TREE = "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b"

AP4_SENTINEL_PATH = (
    "reports/program/evidence/"
    "2026-09-25-AP4-PRICE-STRUCTURE.json"
)
AP4_SENTINEL_SHA256 = (
    "c66a2e8631330a54929c8a30b1b64112a8603489dd5572b8e7414c4e17e3baad"
)


def build_report(repo_root: Path) -> dict[str, object]:
    inventory_path = (
        Path(__file__).with_name(
            "pilot_inventory_v0_1.json"
        )
    )
    inventory = load_inventory(
        inventory_path
    )

    source = FrozenGitSource(
        repo_root=repo_root,
        expected_repository=EXPECTED_REPOSITORY,
        source_commit=SOURCE_COMMIT,
        expected_tree=SOURCE_TREE,
    )

    verified = verify_inventory(
        source,
        inventory,
    )

    total_bytes = verify_inventory_blob_bytes(
        source,
        verified,
    )

    ap4_entry = next(
        item.inventory
        for item in verified
        if item.inventory.source_path
        == AP4_SENTINEL_PATH
    )

    ap4_bytes = source.read_blob(
        ap4_entry.source_blob_sha
    )
    ap4_sha256 = sha256_bytes(
        ap4_bytes
    )

    if ap4_sha256 != AP4_SENTINEL_SHA256:
        raise RuntimeError(
            "AP4 raw-blob sentinel SHA-256 mismatch: "
            f"expected={AP4_SENTINEL_SHA256} "
            f"actual={ap4_sha256}"
        )

    return {
        "schema":
            "ATDS_OBSIDIAN_P0_VERIFY_REPORT_V0_1",
        "repository":
            EXPECTED_REPOSITORY,
        "repo_root":
            str(repo_root.resolve()),
        "source_commit":
            SOURCE_COMMIT,
        "source_tree":
            SOURCE_TREE,
        "inventory_count":
            inventory.source_artifact_count,
        "inventory_digest_sha256":
            inventory.digest_sha256,
        "verified_blob_count":
            len(verified),
        "verified_blob_bytes":
            total_bytes,
        "ap4_sentinel_path":
            AP4_SENTINEL_PATH,
        "ap4_sentinel_blob_sha":
            ap4_entry.source_blob_sha,
        "ap4_sentinel_sha256":
            ap4_sha256,
        "status":
            "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only P0 verification of the "
            "frozen ATDS Obsidian pilot source boundary."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help=(
            "Path to the ATDS Git repository "
            "(default: current directory)."
        ),
    )
    args = parser.parse_args()

    report = build_report(
        Path(args.repo_root)
    )

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
