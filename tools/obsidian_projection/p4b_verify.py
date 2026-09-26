from __future__ import annotations

import argparse
import json
from pathlib import Path

from .native_view_bundle import (
    EXPECTED_VAULT,
    NativeViewBundleError,
    build_view_bundle,
    bundle_manifest,
    seed_native_views,
    verify_p4a_contract,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "ATDS Obsidian P4-B native view bundle verifier"
        )
    )
    parser.add_argument(
        "--repo-root",
        required=True,
        type=Path,
    )
    mode = parser.add_mutually_exclusive_group(
        required=True
    )
    mode.add_argument(
        "--preview",
        action="store_true",
    )
    mode.add_argument(
        "--seed-native-views",
        action="store_true",
    )
    return parser


def _blocked(exc: Exception) -> dict[str, object]:
    return {
        "schema":
            "ATDS_OBSIDIAN_P4B_BLOCKED_REPORT_V0_1",
        "status": "BLOCKED",
        "p4b_seed_qualified": False,
        "error_type": type(exc).__name__,
        "error": str(exc),
        "vault_write_authorized": False,
        "generated_modified_by_harness": False,
        "obsidian_config_modified_by_harness": False,
    }


def main() -> int:
    args = _parser().parse_args()
    vault = Path(EXPECTED_VAULT)

    try:
        package_dir = Path(__file__).resolve().parent
        verify_p4a_contract(package_dir)

        if args.preview:
            bundle = build_view_bundle(vault)
            report: dict[str, object] = {
                "schema":
                    "ATDS_OBSIDIAN_P4B_PREVIEW_REPORT_V0_1",
                "status": "PASS",
                "vault_modified": False,
                "view_file_count": len(bundle),
                "view_manifest":
                    bundle_manifest(bundle),
                "seed_authorized_by_preview": False,
            }
        else:
            report = seed_native_views(
                repo_root=args.repo_root,
                vault=vault,
            )

    except (
        NativeViewBundleError,
        OSError,
        ValueError,
        KeyError,
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
