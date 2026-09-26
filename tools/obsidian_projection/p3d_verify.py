from __future__ import annotations

import argparse
import json
from pathlib import Path

from .first_open import (
    FirstOpenError,
    prepare_first_open,
    verify_first_open,
)


def _emit(value: dict[str, object]) -> None:
    print(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "P3-D first-open safety harness. "
            "It never launches Obsidian and never writes "
            "to the materialized Vault."
        )
    )
    parser.add_argument(
        "--repo-root",
        default=".",
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )
    mode.add_argument(
        "--prepare-first-open",
        action="store_true",
        help=(
            "Reconstruct fresh P2, verify the unopened Vault, "
            "and persist an external TEMP snapshot."
        ),
    )
    mode.add_argument(
        "--verify-first-open",
        action="store_true",
        help=(
            "After manually opening and fully closing Obsidian, "
            "verify the Vault against the external snapshot "
            "and a new fresh P2 reconstruction."
        ),
    )

    parser.add_argument(
        "--snapshot",
        default=None,
        help=(
            "Snapshot path returned by --prepare-first-open. "
            "Required only for --verify-first-open."
        ),
    )

    args = parser.parse_args()

    try:
        if args.prepare_first_open:
            if args.snapshot is not None:
                parser.error(
                    "--snapshot is not accepted with "
                    "--prepare-first-open"
                )
            report = prepare_first_open(
                Path(args.repo_root)
            )
        else:
            if not args.snapshot:
                parser.error(
                    "--snapshot is required with "
                    "--verify-first-open"
                )
            report = verify_first_open(
                Path(args.repo_root),
                Path(args.snapshot),
            )
    except Exception as exc:
        _emit(
            {
                "schema":
                    "ATDS_OBSIDIAN_P3D_BLOCKED_REPORT_V0_1",
                "status":
                    "BLOCKED",
                "first_open_qualified":
                    False,
                "error_type":
                    type(exc).__name__,
                "error":
                    str(exc),
                "automatic_obsidian_launch":
                    False,
                "vault_written_by_harness":
                    False,
            }
        )
        return 1

    _emit(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
