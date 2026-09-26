from __future__ import annotations

import argparse
import json
from pathlib import Path

from .classification import (
    classify_inventory,
    records_digest_sha256,
)
from .git_source import FrozenGitSource
from .inventory import load_inventory

EXPECTED_REPOSITORY = (
    "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM"
)
SOURCE_COMMIT = "7bd8c1312430dfc3def5523eb65397a5d6a5ae05"
SOURCE_TREE = "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b"


def _load_rules(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report(
    repo_root: Path,
    temp_output_dir: Path | None = None,
) -> dict[str, object]:
    package_dir = Path(__file__).resolve().parent

    inventory = load_inventory(
        package_dir / "pilot_inventory_v0_1.json"
    )
    rules = _load_rules(
        package_dir
        / "semantic_classification_rules_v0_1.json"
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
            f"expected 74 semantic records, got {len(records)}"
        )

    by_path = {
        record.source_path: record
        for record in records
    }

    fixture_checks = []
    for fixture in rules["exact_fixtures"]:
        path = fixture["source_path"]
        record = by_path.get(path)
        if record is None:
            raise RuntimeError(
                f"fixture source missing from records: {path}"
            )

        actual = record.to_dict()
        mismatches = {}

        for field, expected in fixture["expected"].items():
            if actual.get(field) != expected:
                mismatches[field] = {
                    "expected": expected,
                    "actual": actual.get(field),
                }

        fixture_checks.append(
            {
                "id": fixture["id"],
                "source_path": path,
                "pass": not mismatches,
                "mismatches": mismatches,
            }
        )

    failed_fixtures = [
        check
        for check in fixture_checks
        if not check["pass"]
    ]
    if failed_fixtures:
        raise RuntimeError(
            "adversarial fixture mismatch: "
            + json.dumps(
                failed_fixtures,
                ensure_ascii=False,
                sort_keys=True,
            )
        )

    qualification_counts: dict[str, int] = {}
    procedure_counts: dict[str, int] = {}
    semantic_counts: dict[str, int] = {}

    for record in records:
        qualification_counts[record.qualification_status] = (
            qualification_counts.get(
                record.qualification_status,
                0,
            )
            + 1
        )
        procedure_counts[record.procedure_role] = (
            procedure_counts.get(
                record.procedure_role,
                0,
            )
            + 1
        )
        semantic_counts[record.semantic_role] = (
            semantic_counts.get(
                record.semantic_role,
                0,
            )
            + 1
        )

    temp_records_path = None
    if temp_output_dir is not None:
        temp_output_dir.mkdir(
            parents=True,
            exist_ok=False,
        )
        temp_records_path = (
            temp_output_dir
            / "semantic-records-v0.1.json"
        )
        temp_records_path.write_text(
            json.dumps(
                [record.to_dict() for record in records],
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

    return {
        "schema":
            "ATDS_OBSIDIAN_P1_CLASSIFIER_VERIFY_REPORT_V0_1",
        "repository":
            EXPECTED_REPOSITORY,
        "source_commit":
            SOURCE_COMMIT,
        "source_tree":
            SOURCE_TREE,
        "record_count":
            len(records),
        "record_digest_sha256":
            records_digest_sha256(records),
        "fixture_count":
            len(fixture_checks),
        "fixture_pass_count":
            sum(
                1
                for check in fixture_checks
                if check["pass"]
            ),
        "qualification_status_counts":
            dict(sorted(qualification_counts.items())),
        "procedure_role_counts":
            dict(sorted(procedure_counts.items())),
        "semantic_role_counts":
            dict(sorted(semantic_counts.items())),
        "temp_records_path":
            str(temp_records_path)
            if temp_records_path is not None
            else None,
        "renderer_used":
            False,
        "relations_generated":
            False,
        "vault_created":
            False,
        "status":
            "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "P1-B read-only semantic classifier verification "
            "for the frozen 74-source ATDS pilot."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
    )
    parser.add_argument(
        "--temp-output-dir",
        default=None,
        help=(
            "Optional NEW temporary directory for JSON semantic "
            "records. No Markdown/Obsidian rendering occurs."
        ),
    )
    args = parser.parse_args()

    report = build_report(
        Path(args.repo_root),
        (
            Path(args.temp_output_dir)
            if args.temp_output_dir
            else None
        ),
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
