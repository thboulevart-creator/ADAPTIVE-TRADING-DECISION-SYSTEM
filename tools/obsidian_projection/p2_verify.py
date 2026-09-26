from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from .builder import build_projection_from_records
from .classification import (
    classify_inventory,
    records_digest_sha256,
)
from .git_source import FrozenGitSource
from .integrity import (
    all_generated_files,
    verify_integrity_manifest,
)
from .inventory import load_inventory

EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
SOURCE_COMMIT = "7bd8c1312430dfc3def5523eb65397a5d6a5ae05"
SOURCE_TREE = "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b"


def _load_json(path: Path) -> dict:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def _file_map(
    stage_root: Path,
) -> dict[str, bytes]:
    result: dict[str, bytes] = {}

    for digest in all_generated_files(
        stage_root
    ):
        path = stage_root / digest.relative_path
        result[digest.relative_path] = (
            path.read_bytes()
        )

    return result


def _compare_builds(
    build_a: Path,
    build_b: Path,
) -> dict[str, object]:
    files_a = _file_map(build_a)
    files_b = _file_map(build_b)

    paths_a = set(files_a)
    paths_b = set(files_b)

    if paths_a != paths_b:
        raise RuntimeError(
            "double-build path-set mismatch"
        )

    mismatched = [
        path
        for path in sorted(paths_a)
        if files_a[path] != files_b[path]
    ]
    if mismatched:
        raise RuntimeError(
            "double-build byte mismatch: "
            + ", ".join(mismatched)
        )

    return {
        "relative_path_count": len(paths_a),
        "byte_identical_file_count":
            len(paths_a),
        "mismatched_files": mismatched,
    }


def build_report(
    repo_root: Path,
) -> dict[str, object]:
    package_dir = Path(__file__).resolve().parent

    inventory = load_inventory(
        package_dir
        / "pilot_inventory_v0_1.json"
    )
    rules = _load_json(
        package_dir
        / "semantic_classification_rules_v0_1.json"
    )
    contract = _load_json(
        package_dir
        / "deterministic_projection_contract_v0_1.json"
    )

    if contract["p1_classifier_head"] != (
        "26e541c0aedc85440bb069cdc767b2075b56317c"
    ):
        raise RuntimeError(
            "projection contract P1 binding mismatch"
        )

    source = FrozenGitSource(
        repo_root=repo_root,
        expected_repository=EXPECTED_REPOSITORY,
        source_commit=SOURCE_COMMIT,
        expected_tree=SOURCE_TREE,
    )

    records = classify_inventory(
        source,
        inventory,
        rules,
    )

    if len(records) != 74:
        raise RuntimeError(
            f"expected 74 semantic records, got "
            f"{len(records)}"
        )

    semantic_digest = records_digest_sha256(
        records
    )

    temp_parent = Path(
        tempfile.mkdtemp(
            prefix="ATDS-OBSIDIAN-P2B-"
        )
    )
    build_a_path = temp_parent / "build-a"
    build_b_path = temp_parent / "build-b"

    result_a = build_projection_from_records(
        source=source,
        records=records,
        pilot_inventory_digest_sha256=(
            inventory.digest_sha256
        ),
        semantic_record_digest_sha256=(
            semantic_digest
        ),
        contract=contract,
        stage_root=build_a_path,
    )

    result_b = build_projection_from_records(
        source=source,
        records=records,
        pilot_inventory_digest_sha256=(
            inventory.digest_sha256
        ),
        semantic_record_digest_sha256=(
            semantic_digest
        ),
        contract=contract,
        stage_root=build_b_path,
    )

    compare = _compare_builds(
        build_a_path,
        build_b_path,
    )

    for field in (
        "artifact_record_count",
        "relation_record_count",
        "semantic_record_digest_sha256",
        "artifact_set_digest_sha256",
        "relation_set_digest_sha256",
        "integrity_manifest_sha256",
        "projection_tree_digest_sha256",
        "deterministic_file_count",
        "generated_file_count",
    ):
        if getattr(result_a, field) != getattr(
            result_b,
            field,
        ):
            raise RuntimeError(
                f"double-build result mismatch: "
                f"{field}"
            )

    if result_a.artifact_record_count != 74:
        raise RuntimeError(
            "artifact record count must equal 74"
        )

    integrity_a = verify_integrity_manifest(
        build_a_path
    )
    integrity_b = verify_integrity_manifest(
        build_b_path
    )

    if any(
        status != "CLEAN"
        for status in integrity_a.values()
    ):
        raise RuntimeError(
            "build A integrity is not CLEAN"
        )
    if any(
        status != "CLEAN"
        for status in integrity_b.values()
    ):
        raise RuntimeError(
            "build B integrity is not CLEAN"
        )

    return {
        "schema":
            "ATDS_OBSIDIAN_P2B_VERIFY_REPORT_V0_1",
        "repository":
            EXPECTED_REPOSITORY,
        "source_commit":
            SOURCE_COMMIT,
        "source_tree":
            SOURCE_TREE,
        "semantic_record_count":
            len(records),
        "semantic_record_digest_sha256":
            semantic_digest,
        "artifact_record_count":
            result_a.artifact_record_count,
        "relation_record_count":
            result_a.relation_record_count,
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
        "double_build":
            compare,
        "build_a_integrity_clean_count":
            sum(
                status == "CLEAN"
                for status in integrity_a.values()
            ),
        "build_b_integrity_clean_count":
            sum(
                status == "CLEAN"
                for status in integrity_b.values()
            ),
        "temporary_parent":
            str(temp_parent),
        "build_a":
            str(build_a_path),
        "build_b":
            str(build_b_path),
        "renderer_used":
            True,
        "relations_generated":
            result_a.relation_record_count,
        "real_vault_created":
            False,
        "obsidian_config_created":
            False,
        "status":
            "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "P2-B deterministic projection verification. "
            "Builds twice under OS TEMP only."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
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
