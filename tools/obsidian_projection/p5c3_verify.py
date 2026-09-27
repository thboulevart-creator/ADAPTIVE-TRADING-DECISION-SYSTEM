from __future__ import annotations

import argparse
import json
from pathlib import Path

from .obsidian_open_compatibility import (
    ObsidianOpenCompatibilityError,
    diagnose_open_preconditions,
    post_close_verify,
    prepare_open_experiment,
    run_while_obsidian_open,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "ATDS Obsidian P5-C3 open-Vault "
            "compatibility verifier"
        )
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )
    mode.add_argument(
        "--prepare",
        action="store_true",
    )
    mode.add_argument(
        "--run-open",
        action="store_true",
    )
    mode.add_argument(
        "--post-close",
        action="store_true",
    )
    mode.add_argument(
        "--diagnose-open",
        action="store_true",
    )

    parser.add_argument(
        "--snapshot",
        type=Path,
    )
    parser.add_argument(
        "--manual-visual-accepted",
        action="store_true",
    )
    return parser


def _blocked(exc: Exception) -> dict[str, object]:
    return {
        "schema":
            "ATDS_OBSIDIAN_P5C3_BLOCKED_REPORT_V0_1",
        "status": "BLOCKED",
        "error_type": type(exc).__name__,
        "error": str(exc),
        "production_promotion_authorized": False,
        "continuous_observer_authorized": False,
        "p5c3_qualified": False,
    }


def main() -> int:
    args = _parser().parse_args()

    try:
        if args.prepare:
            if args.snapshot is not None:
                raise ObsidianOpenCompatibilityError(
                    "--snapshot is forbidden with --prepare"
                )
            report = prepare_open_experiment()

        elif args.diagnose_open:
            if args.snapshot is None:
                raise ObsidianOpenCompatibilityError(
                    "--snapshot required with --diagnose-open"
                )
            if args.manual_visual_accepted:
                raise ObsidianOpenCompatibilityError(
                    "manual acceptance flag is forbidden during --diagnose-open"
                )
            report = diagnose_open_preconditions(
                args.snapshot
            )

        elif args.run_open:
            if args.snapshot is None:
                raise ObsidianOpenCompatibilityError(
                    "--snapshot required with --run-open"
                )
            if args.manual_visual_accepted:
                raise ObsidianOpenCompatibilityError(
                    "manual acceptance flag is forbidden during --run-open"
                )
            report = run_while_obsidian_open(
                args.snapshot
            )

        else:
            if args.snapshot is None:
                raise ObsidianOpenCompatibilityError(
                    "--snapshot required with --post-close"
                )
            report = post_close_verify(
                args.snapshot,
                manual_visual_accepted=
                    args.manual_visual_accepted,
            )

    except (
        ObsidianOpenCompatibilityError,
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

    if args.diagnose_open:
        return (
            0
            if report.get("status") == "PASS"
            else 2
        )

    if args.run_open:
        return (
            0
            if report.get("status")
            == "PASS_AUTOMATED_OPEN_EXPERIMENT"
            else 2
        )

    if args.post_close:
        return (
            0
            if report.get("status") == "PASS"
            else 2
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
